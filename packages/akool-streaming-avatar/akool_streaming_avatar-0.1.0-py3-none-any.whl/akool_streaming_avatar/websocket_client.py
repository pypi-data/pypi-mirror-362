"""
WebSocket client for connecting to Akool streaming avatar services.
"""

import asyncio
import json
import logging
import time
import uuid
from typing import Optional, Callable, Dict, Any
from urllib.parse import urlencode
import websockets
from websockets.exceptions import ConnectionClosed, WebSocketException

from .exceptions import ConnectionError, AuthenticationError, AudioStreamError
from .service_discovery import ServiceInstance

logger = logging.getLogger(__name__)


class WebSocketClient:
    """WebSocket client for streaming avatar services."""

    def __init__(
        self,
        api_key: str,
        session_id: Optional[str] = None,
        heartbeat_interval: int = 30,
        connection_timeout: int = 30,
        message_timeout: int = 10,
    ):
        """
        Initialize WebSocket client.

        Args:
            api_key: API key for authentication
            session_id: Session ID (will be generated if not provided)
            heartbeat_interval: Heartbeat interval in seconds
            connection_timeout: Connection timeout in seconds
            message_timeout: Message response timeout in seconds
        """
        self.api_key = api_key
        self.session_id = session_id or str(uuid.uuid4())
        self.heartbeat_interval = heartbeat_interval
        self.connection_timeout = connection_timeout
        self.message_timeout = message_timeout

        self.websocket: Optional[websockets.WebSocketServerProtocol] = None
        self.connected = False
        self.agora_connected = False

        # Event handlers
        self.on_connected: Optional[Callable] = None
        self.on_disconnected: Optional[Callable] = None
        self.on_agora_connected: Optional[Callable[[str], None]] = None
        self.on_error: Optional[Callable[[Exception], None]] = None
        self.on_message: Optional[Callable[[Dict[str, Any]], None]] = None

        # Background tasks
        self._heartbeat_task: Optional[asyncio.Task] = None
        self._message_handler_task: Optional[asyncio.Task] = None

        # Message tracking
        self._pending_responses: Dict[str, asyncio.Future] = {}
        self._audio_count = 0

        # Connection state
        self._shutdown = False

    async def connect(self, service_instance: ServiceInstance, avatar_id: str) -> None:
        """
        Connect to a streaming avatar service.

        Args:
            service_instance: Service instance to connect to
            avatar_id: Avatar ID to use

        Raises:
            ConnectionError: If connection fails
            AuthenticationError: If authentication fails
        """
        # Build WebSocket URL with query parameters
        params = {"session_id": self.session_id, "avatar_id": avatar_id}
        url = f"{service_instance.websocket_url}?{urlencode(params)}"

        # WebSocket headers
        headers = {"api_key": self.api_key}

        try:
            logger.info(f"Connecting to WebSocket: {url}")

            # Connect to WebSocket
            self.websocket = await asyncio.wait_for(
                websockets.connect(
                    url, extra_headers=headers, ping_interval=None, ping_timeout=None  # We handle ping/pong manually
                ),
                timeout=self.connection_timeout,
            )

            self.connected = True
            logger.info(f"WebSocket connected successfully: session_id={self.session_id}")

            # Start background tasks
            self._heartbeat_task = asyncio.create_task(self._heartbeat_loop())
            self._message_handler_task = asyncio.create_task(self._message_handler_loop())

            # Wait for initial connection confirmation
            await self._wait_for_websocket_connected()

            if self.on_connected:
                self.on_connected()

        except asyncio.TimeoutError:
            raise ConnectionError(f"Connection timeout after {self.connection_timeout} seconds")
        except websockets.exceptions.InvalidStatusCode as e:
            if e.status_code == 4001:
                raise AuthenticationError("Invalid or missing API key")
            elif e.status_code == 4003:
                raise ConnectionError("Service is occupied, only one connection allowed")
            elif e.status_code == 4004:
                raise ConnectionError("Reconnection too soon, please wait")
            else:
                raise ConnectionError(f"Connection failed with status {e.status_code}")
        except Exception as e:
            raise ConnectionError(f"Failed to connect to WebSocket: {e}")

    async def disconnect(self) -> None:
        """Disconnect from the streaming avatar service."""
        if not self.connected:
            return

        logger.info("Disconnecting from WebSocket")
        self._shutdown = True

        # Cancel background tasks
        if self._heartbeat_task:
            self._heartbeat_task.cancel()
        if self._message_handler_task:
            self._message_handler_task.cancel()

        # Send leave channel event
        try:
            await self.send_leave_channel_event("client_disconnect")
        except Exception as e:
            logger.warning(f"Failed to send leave channel event: {e}")

        # Close WebSocket connection
        if self.websocket:
            try:
                await self.websocket.close()
            except Exception as e:
                logger.warning(f"Error closing WebSocket: {e}")

        self.connected = False
        self.agora_connected = False
        self.websocket = None

        # Cancel any pending responses
        for future in self._pending_responses.values():
            if not future.done():
                future.cancel()
        self._pending_responses.clear()

        if self.on_disconnected:
            self.on_disconnected()

        logger.info("WebSocket disconnected")

    async def set_agora_params(
        self,
        agora_app_id: str,
        agora_channel: str,
        agora_token: str,
        agora_uid: str,
        additional_params: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Set Agora parameters for the streaming avatar.

        Args:
            agora_app_id: Agora application ID
            agora_channel: Agora channel ID
            agora_token: Agora token
            agora_uid: Agora user ID
            additional_params: Additional parameters (vid, lang, mode, bgurl, etc.)

        Raises:
            ConnectionError: If not connected
            AudioStreamError: If setting parameters fails
        """
        if not self.connected:
            raise ConnectionError("Not connected to WebSocket")

        # Default parameters
        params = additional_params or {}

        # Build set-params message
        message = {
            "v": 2,
            "type": "command",
            "mid": f"cmd-set-params-{int(time.time() * 1000)}",
            "pld": {
                "cmd": "set-params",
                "data": {
                    "vid": params.get("vid", ""),
                    "lang": params.get("lang", "en"),
                    "mode": params.get("mode", 3),  # Must be 3 for streaming mode
                    "bgurl": params.get("bgurl", ""),
                },
                "metadata": {
                    "agora_data": {
                        "appid": agora_app_id,
                        "channel_id": agora_channel,
                        "token": agora_token,
                        "uid": agora_uid,
                    }
                },
            },
        }

        try:
            logger.info(f"Setting Agora parameters: channel={agora_channel}")

            # Send set-params command and wait for acknowledgment
            response = await self._send_message_and_wait_response(message, "ack")

            # Wait for Agora connection confirmation
            await self._wait_for_agora_connected()

            logger.info("Agora parameters set successfully")

        except Exception as e:
            raise AudioStreamError(f"Failed to set Agora parameters: {e}")

    async def send_audio(self, audio_data: bytes) -> None:
        """
        Send audio data to the streaming avatar.

        Args:
            audio_data: PCM audio data (16-bit, 16kHz, mono)

        Raises:
            ConnectionError: If not connected
            AudioStreamError: If sending audio fails
        """
        if not self.connected:
            raise ConnectionError("Not connected to WebSocket")

        import base64

        # Encode audio data as base64
        audio_b64 = base64.b64encode(audio_data).decode("utf-8")

        # Build chat message with audio
        message = {"v": 2, "type": "chat", "mid": f"audio-{int(time.time() * 1000)}", "pld": {"audio": audio_b64}}

        try:
            await self._send_message(message)
            self._audio_count += 1

            logger.debug(f"Sent audio data: size={len(audio_data)} bytes, count={self._audio_count}")

        except Exception as e:
            raise AudioStreamError(f"Failed to send audio data: {e}")

    async def interrupt(self) -> None:
        """
        Send interrupt command to stop current avatar response.

        Raises:
            ConnectionError: If not connected
        """
        if not self.connected:
            raise ConnectionError("Not connected to WebSocket")

        message = {
            "v": 2,
            "type": "command",
            "mid": f"cmd-interrupt-{int(time.time() * 1000)}",
            "pld": {"cmd": "interrupt"},
        }

        try:
            logger.info("Sending interrupt command")
            await self._send_message_and_wait_response(message, "ack")
            logger.info("Interrupt command sent successfully")

        except Exception as e:
            logger.error(f"Failed to send interrupt command: {e}")
            raise

    async def send_leave_channel_event(self, reason: str = "user_left") -> None:
        """
        Send leave channel event.

        Args:
            reason: Reason for leaving
        """
        message = {
            "v": 2,
            "type": "event",
            "mid": f"event-leave-{int(time.time() * 1000)}",
            "pld": {"event": "leave_channel", "reason": reason},
        }

        try:
            await self._send_message_and_wait_response(message, "ack", timeout=5)
        except Exception as e:
            logger.warning(f"Failed to send leave channel event: {e}")

    async def _send_message(self, message: Dict[str, Any]) -> None:
        """Send a message to the WebSocket."""
        if not self.websocket:
            raise ConnectionError("WebSocket not connected")

        message_str = json.dumps(message)
        await self.websocket.send(message_str)
        logger.debug(f"Sent message: {message.get('type')} - {message.get('mid')}")

    async def _send_message_and_wait_response(
        self, message: Dict[str, Any], expected_type: str, timeout: Optional[int] = None
    ) -> Dict[str, Any]:
        """Send a message and wait for a specific response type."""
        mid = message.get("mid")
        if not mid:
            raise ValueError("Message must have a 'mid' field")

        # Create future for response
        response_future = asyncio.Future()
        self._pending_responses[mid] = response_future

        try:
            # Send message
            await self._send_message(message)

            # Wait for response
            timeout = timeout or self.message_timeout
            response = await asyncio.wait_for(response_future, timeout=timeout)

            return response

        except asyncio.TimeoutError:
            raise ConnectionError(f"Timeout waiting for {expected_type} response")
        finally:
            # Clean up
            self._pending_responses.pop(mid, None)

    async def _heartbeat_loop(self) -> None:
        """Background task for sending heartbeat pings."""
        while not self._shutdown and self.connected:
            try:
                # Send ping
                ping_mid = f"ping-{int(time.time() * 1000)}"
                ping_message = {"v": 2, "type": "ping", "mid": ping_mid, "pld": {}}

                await self._send_message(ping_message)
                logger.debug("Sent heartbeat ping")

                # Wait for heartbeat interval
                await asyncio.sleep(self.heartbeat_interval)

            except Exception as e:
                if not self._shutdown:
                    logger.error(f"Heartbeat error: {e}")
                    if self.on_error:
                        self.on_error(e)
                break

    async def _message_handler_loop(self) -> None:
        """Background task for handling incoming messages."""
        while not self._shutdown and self.connected and self.websocket:
            try:
                # Receive message
                message_str = await self.websocket.recv()
                message = json.loads(message_str)

                await self._handle_message(message)

            except ConnectionClosed:
                logger.info("WebSocket connection closed")
                break
            except WebSocketException as e:
                logger.error(f"WebSocket error: {e}")
                if self.on_error:
                    self.on_error(e)
                break
            except Exception as e:
                if not self._shutdown:
                    logger.error(f"Message handler error: {e}")
                    if self.on_error:
                        self.on_error(e)

    async def _handle_message(self, message: Dict[str, Any]) -> None:
        """Handle incoming WebSocket message."""
        msg_type = message.get("type")
        mid = message.get("mid", "")

        logger.debug(f"Received message: {msg_type} - {mid}")

        if msg_type == "system":
            await self._handle_system_message(message)
        elif msg_type == "ack":
            await self._handle_ack_message(message)
        elif msg_type == "pong":
            await self._handle_pong_message(message)
        elif msg_type == "error":
            await self._handle_error_message(message)
        else:
            logger.debug(f"Unhandled message type: {msg_type}")

        # Call user message handler
        if self.on_message:
            self.on_message(message)

    async def _handle_system_message(self, message: Dict[str, Any]) -> None:
        """Handle system messages."""
        pld = message.get("pld", {})
        status = pld.get("status")

        if status == "websocket_connected":
            logger.info("WebSocket connection confirmed")
            self._resolve_pending_response(message.get("mid"), message)
        elif status == "agora_connected":
            channel_id = pld.get("channel_id", "")
            logger.info(f"Agora connection confirmed: channel={channel_id}")
            self.agora_connected = True
            if self.on_agora_connected:
                self.on_agora_connected(channel_id)
            self._resolve_pending_response(message.get("mid"), message)

    async def _handle_ack_message(self, message: Dict[str, Any]) -> None:
        """Handle acknowledgment messages."""
        pld = message.get("pld", {})
        original_mid = pld.get("original_mid")

        if original_mid:
            self._resolve_pending_response(original_mid, message)

    async def _handle_pong_message(self, message: Dict[str, Any]) -> None:
        """Handle pong messages."""
        logger.debug("Received pong response")

    async def _handle_error_message(self, message: Dict[str, Any]) -> None:
        """Handle error messages."""
        pld = message.get("pld", {})
        error_code = pld.get("error_code")
        error_message = pld.get("error_message", "Unknown error")

        logger.error(f"Received error from server: code={error_code}, message={error_message}")

        error = ConnectionError(f"Server error {error_code}: {error_message}")
        if self.on_error:
            self.on_error(error)

    def _resolve_pending_response(self, mid: str, response: Dict[str, Any]) -> None:
        """Resolve a pending response future."""
        if mid in self._pending_responses:
            future = self._pending_responses[mid]
            if not future.done():
                future.set_result(response)

    async def _wait_for_websocket_connected(self) -> None:
        """Wait for WebSocket connection confirmation."""
        start_time = time.time()
        while not self._shutdown and time.time() - start_time < self.connection_timeout:
            if self.connected:
                return
            await asyncio.sleep(0.1)

        raise ConnectionError("Timeout waiting for WebSocket connection confirmation")

    async def _wait_for_agora_connected(self) -> None:
        """Wait for Agora connection confirmation."""
        start_time = time.time()
        while not self._shutdown and time.time() - start_time < self.connection_timeout:
            if self.agora_connected:
                return
            await asyncio.sleep(0.1)

        raise ConnectionError("Timeout waiting for Agora connection confirmation")
