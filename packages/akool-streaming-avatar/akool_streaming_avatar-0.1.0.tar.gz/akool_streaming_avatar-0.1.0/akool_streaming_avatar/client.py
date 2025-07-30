"""
Main client class for the Akool Streaming Avatar SDK.
"""

import asyncio
import logging
import time
from typing import Optional, List, Dict, Any, Callable

from .service_discovery import ServiceDiscovery, ServiceInstance
from .websocket_client import WebSocketClient
from .exceptions import (
    AkoolStreamingAvatarError,
    AuthenticationError,
    ConnectionError,
    ServiceDiscoveryError,
    AudioStreamError,
    RetryError,
    ConfigurationError,
)

logger = logging.getLogger(__name__)


class StreamingAvatarClient:
    """
    Main client for connecting to Akool streaming avatar services.

    This client handles:
    - Service discovery and load balancing
    - WebSocket connection management
    - Audio streaming
    - Automatic retry and failover
    - Authentication
    """

    def __init__(
        self,
        api_key: str,
        discovery_url: str,
        avatar_id: str,
        session_id: Optional[str] = None,
        max_retry_attempts: int = 3,
        heartbeat_interval: int = 30,
        connection_timeout: int = 30,
        discovery_timeout: int = 10,
    ):
        """
        Initialize the streaming avatar client.

        Args:
            api_key: API key for authentication (used as token)
            discovery_url: Base URL for service discovery
            avatar_id: Avatar ID to connect to
            session_id: Session ID (will be generated if not provided)
            max_retry_attempts: Maximum number of retry attempts on failure
            heartbeat_interval: Heartbeat interval in seconds
            connection_timeout: Connection timeout in seconds
            discovery_timeout: Service discovery timeout in seconds
        """
        # Validate required parameters
        if not api_key:
            raise ConfigurationError("api_key is required")
        if not discovery_url:
            raise ConfigurationError("discovery_url is required")
        if not avatar_id:
            raise ConfigurationError("avatar_id is required")

        self.api_key = api_key
        self.discovery_url = discovery_url.rstrip("/")
        self.avatar_id = avatar_id
        self.max_retry_attempts = max_retry_attempts

        # Initialize service discovery
        self.service_discovery = ServiceDiscovery(api_key=api_key, timeout=discovery_timeout)

        # Initialize WebSocket client
        self.websocket_client = WebSocketClient(
            api_key=api_key,
            session_id=session_id,
            heartbeat_interval=heartbeat_interval,
            connection_timeout=connection_timeout,
        )

        # Connection state
        self.connected = False
        self.current_service: Optional[ServiceInstance] = None
        self.available_services: List[ServiceInstance] = []

        # Event handlers
        self.on_connected: Optional[Callable] = None
        self.on_disconnected: Optional[Callable] = None
        self.on_agora_connected: Optional[Callable[[str], None]] = None
        self.on_error: Optional[Callable[[Exception], None]] = None
        self.on_message: Optional[Callable[[Dict[str, Any]], None]] = None

        # Set up WebSocket client event handlers
        self.websocket_client.on_connected = self._on_websocket_connected
        self.websocket_client.on_disconnected = self._on_websocket_disconnected
        self.websocket_client.on_agora_connected = self._on_agora_connected
        self.websocket_client.on_error = self._on_websocket_error
        self.websocket_client.on_message = self._on_websocket_message

    @property
    def session_id(self) -> str:
        """Get the current session ID."""
        return self.websocket_client.session_id

    @property
    def is_connected(self) -> bool:
        """Check if connected to a streaming avatar service."""
        return self.connected and self.websocket_client.connected

    @property
    def is_agora_connected(self) -> bool:
        """Check if Agora connection is established."""
        return self.websocket_client.agora_connected

    async def connect(self) -> None:
        """
        Connect to a streaming avatar service.

        This method:
        1. Discovers available services
        2. Attempts to connect to a service
        3. Retries with different services on failure

        Raises:
            ServiceDiscoveryError: If no services are available
            ConnectionError: If all connection attempts fail
            AuthenticationError: If authentication fails
        """
        logger.info(f"Connecting to streaming avatar service: avatar_id={self.avatar_id}")

        retry_count = 0
        last_exception = None

        while retry_count < self.max_retry_attempts:
            try:
                # Discover available services
                await self._discover_services()

                if not self.available_services:
                    raise ServiceDiscoveryError(f"No available services found for avatar_id: {self.avatar_id}")

                # Try to connect to the first available service
                service = self.available_services[0]
                logger.info(f"Attempting to connect to service: {service}")

                await self.websocket_client.connect(service, self.avatar_id)

                self.current_service = service
                self.connected = True

                logger.info(f"Successfully connected to streaming avatar service: {service}")
                return

            except (ConnectionError, AuthenticationError) as e:
                last_exception = e
                retry_count += 1

                logger.warning(f"Connection attempt {retry_count} failed: {e}")

                # Remove the failed service from available services
                if self.current_service and self.current_service in self.available_services:
                    self.available_services.remove(self.current_service)

                if retry_count < self.max_retry_attempts:
                    if self.available_services:
                        logger.info(f"Retrying with next available service...")
                    else:
                        logger.info(f"No more services available, re-discovering...")
                        # Clear available services to force re-discovery
                        self.available_services = []
                else:
                    logger.error(f"All connection attempts failed")

            except Exception as e:
                logger.error(f"Unexpected error during connection: {e}")
                last_exception = e
                break

        # All retry attempts failed
        if last_exception:
            raise RetryError(f"Failed to connect after {self.max_retry_attempts} attempts: {last_exception}")
        else:
            raise ConnectionError(f"Failed to connect after {self.max_retry_attempts} attempts")

    async def disconnect(self) -> None:
        """Disconnect from the streaming avatar service."""
        if not self.connected:
            return

        logger.info("Disconnecting from streaming avatar service")

        try:
            await self.websocket_client.disconnect()
        except Exception as e:
            logger.warning(f"Error during disconnect: {e}")
        finally:
            self.connected = False
            self.current_service = None

    async def set_agora_params(
        self,
        agora_app_id: str,
        agora_channel: str,
        agora_token: str,
        agora_uid: str,
        voice_id: Optional[str] = None,
        language: str = "en",
        background_url: Optional[str] = None,
    ) -> None:
        """
        Set Agora parameters for the streaming avatar.

        Args:
            agora_app_id: Agora application ID
            agora_channel: Agora channel ID
            agora_token: Agora token
            agora_uid: Agora user ID
            voice_id: Voice ID for the avatar (optional)
            language: Language code (default: "en")
            background_url: Background image/video URL (optional)

        Raises:
            ConnectionError: If not connected
            AudioStreamError: If setting parameters fails
        """
        if not self.is_connected:
            raise ConnectionError("Not connected to streaming avatar service")

        additional_params = {
            "vid": voice_id or "",
            "lang": language,
            "mode": 3,  # Streaming mode
            "bgurl": background_url or "",
        }

        await self.websocket_client.set_agora_params(
            agora_app_id=agora_app_id,
            agora_channel=agora_channel,
            agora_token=agora_token,
            agora_uid=agora_uid,
            additional_params=additional_params,
        )

    async def send_audio(self, audio_data: bytes) -> None:
        """
        Send audio data to the streaming avatar.

        Args:
            audio_data: PCM audio data (16-bit, 16kHz, mono)

        Raises:
            ConnectionError: If not connected
            AudioStreamError: If sending audio fails
        """
        if not self.is_connected:
            raise ConnectionError("Not connected to streaming avatar service")

        await self.websocket_client.send_audio(audio_data)

    async def send_audio_stream(self, audio_chunks: List[bytes]) -> None:
        """
        Send multiple audio chunks in sequence.

        Args:
            audio_chunks: List of PCM audio data chunks

        Raises:
            ConnectionError: If not connected
            AudioStreamError: If sending audio fails
        """
        if not self.is_connected:
            raise ConnectionError("Not connected to streaming avatar service")

        for i, chunk in enumerate(audio_chunks):
            try:
                await self.send_audio(chunk)
                logger.debug(f"Sent audio chunk {i+1}/{len(audio_chunks)}")
            except Exception as e:
                logger.error(f"Failed to send audio chunk {i+1}: {e}")
                raise

    async def interrupt(self) -> None:
        """
        Send interrupt command to stop current avatar response.

        Raises:
            ConnectionError: If not connected
        """
        if not self.is_connected:
            raise ConnectionError("Not connected to streaming avatar service")

        await self.websocket_client.interrupt()

    def get_connection_info(self) -> Dict[str, Any]:
        """
        Get information about the current connection.

        Returns:
            Dictionary with connection information
        """
        return {
            "connected": self.is_connected,
            "agora_connected": self.is_agora_connected,
            "session_id": self.session_id,
            "avatar_id": self.avatar_id,
            "current_service": (
                {
                    "ip": self.current_service.ip,
                    "port": self.current_service.port,
                    "status": self.current_service.status,
                    "healthy": self.current_service.healthy,
                }
                if self.current_service
                else None
            ),
            "available_services_count": len(self.available_services),
        }

    async def _discover_services(self) -> None:
        """Discover available streaming avatar services."""
        try:
            logger.info(f"Discovering services for avatar_id: {self.avatar_id}")

            # Find multiple services for failover
            services = self.service_discovery.find_multiple_services(
                base_url=self.discovery_url, avatar_id=self.avatar_id, count=self.max_retry_attempts
            )

            self.available_services = services
            logger.info(f"Discovered {len(services)} available services")

        except Exception as e:
            logger.error(f"Service discovery failed: {e}")
            raise

    def _on_websocket_connected(self) -> None:
        """Handle WebSocket connection event."""
        logger.info("WebSocket connected")
        if self.on_connected:
            self.on_connected()

    def _on_websocket_disconnected(self) -> None:
        """Handle WebSocket disconnection event."""
        logger.info("WebSocket disconnected")
        self.connected = False
        if self.on_disconnected:
            self.on_disconnected()

    def _on_agora_connected(self, channel_id: str) -> None:
        """Handle Agora connection event."""
        logger.info(f"Agora connected: channel={channel_id}")
        if self.on_agora_connected:
            self.on_agora_connected(channel_id)

    def _on_websocket_error(self, error: Exception) -> None:
        """Handle WebSocket error event."""
        logger.error(f"WebSocket error: {error}")
        if self.on_error:
            self.on_error(error)

    def _on_websocket_message(self, message: Dict[str, Any]) -> None:
        """Handle WebSocket message event."""
        if self.on_message:
            self.on_message(message)


# Async context manager support
class AsyncStreamingAvatarClient(StreamingAvatarClient):
    """Async context manager version of StreamingAvatarClient."""

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.disconnect()


# Convenience function for simple usage
async def create_client(api_key: str, discovery_url: str, avatar_id: str, **kwargs) -> StreamingAvatarClient:
    """
    Create and connect a streaming avatar client.

    Args:
        api_key: API key for authentication
        discovery_url: Base URL for service discovery
        avatar_id: Avatar ID to connect to
        **kwargs: Additional arguments for StreamingAvatarClient

    Returns:
        Connected StreamingAvatarClient instance
    """
    client = StreamingAvatarClient(api_key=api_key, discovery_url=discovery_url, avatar_id=avatar_id, **kwargs)

    await client.connect()
    return client
