# Akool Streaming Avatar SDK

A Python SDK for connecting to Akool's streaming avatar services via WebSocket. This SDK provides easy-to-use interfaces for real-time audio streaming, automatic load balancing, and robust error handling.

## Features

- 🔐 **Token-based Authentication** - Secure API key authentication
- ⚖️ **Automatic Load Balancing** - Service discovery with random server selection
- 🔄 **Retry Logic** - Automatic reconnection with configurable retry attempts
- 🎵 **Audio Streaming** - Real-time PCM audio transmission
- 💓 **Built-in Heartbeat** - Automatic connection health monitoring
- 🛡️ **Error Handling** - Comprehensive exception handling with user-friendly messages
- 📝 **Event-driven** - Callback-based architecture for real-time responses

## Installation

```bash
pip install akool-streaming-avatar
```

## Quick Start

### Method 1: Manual Connection Management

```python
import asyncio
from akool_streaming_avatar import StreamingAvatarClient

async def main():
    # Initialize client
    client = StreamingAvatarClient(
        api_key="your-api-key",
        discovery_url="https://api.akool.com/streamingAvatar/service_status",
        avatar_id="your-avatar-id"
    )
    
    try:
        # Connect to service
        await client.connect()
        
        # Set Agora parameters (required)
        await client.set_agora_params(
            agora_app_id="your-agora-app-id",
            agora_channel="your-channel",
            agora_token="your-rtc-token",
            agora_uid="12345"
        )
        
        # Send audio data
        audio_data = b"..."  # PCM 16-bit, 16kHz, mono
        await client.send_audio(audio_data)
        
    finally:
        # Always disconnect when done
        await client.disconnect()

# Run the client
asyncio.run(main())
```

### Method 2: Using Async Context Manager (Recommended)

```python
import asyncio
from akool_streaming_avatar import AsyncStreamingAvatarClient

async def main():
    # Using async context manager for automatic connection handling
    async with AsyncStreamingAvatarClient(
        api_key="your-api-key",
        discovery_url="https://api.akool.com/streamingAvatar/service_status",
        avatar_id="your-avatar-id"
    ) as client:
        # Client is automatically connected
        
        # Set Agora parameters (required)
        await client.set_agora_params(
            agora_app_id="your-agora-app-id",
            agora_channel="your-channel",
            agora_token="your-rtc-token",
            agora_uid="12345"
        )
        
        # Send audio data
        audio_data = b"..."  # PCM 16-bit, 16kHz, mono
        await client.send_audio(audio_data)
        
    # Client is automatically disconnected when exiting the context

# Run the client
asyncio.run(main())
```

## API Reference

### StreamingAvatarClient

Main client class for connecting to Akool streaming avatar services.

#### Constructor

```python
StreamingAvatarClient(
    api_key: str,
    discovery_url: str,
    avatar_id: str,
    session_id: Optional[str] = None,
    max_retry_attempts: int = 3,
    heartbeat_interval: int = 30,
    connection_timeout: int = 30,
    discovery_timeout: int = 10
)
```

**Parameters:**
- `api_key`: Your Akool API key
- `discovery_url`: Service discovery endpoint URL
- `avatar_id`: Target avatar identifier
- `session_id`: Session ID (will be generated if not provided)
- `max_retry_attempts`: Maximum retry attempts (default: 3)
- `heartbeat_interval`: Heartbeat interval in seconds (default: 30)
- `connection_timeout`: Connection timeout in seconds (default: 30)
- `discovery_timeout`: Service discovery timeout in seconds (default: 10)

#### Methods

##### connect()
```python
async def connect() -> None
```
Establish connection to the streaming avatar service with automatic service discovery and retry logic.

**Raises:**
- `AuthenticationError`: Invalid API key
- `ServiceDiscoveryError`: No available services
- `ConnectionError`: Connection failed
- `RetryError`: All retry attempts exhausted

##### disconnect()
```python
async def disconnect() -> None
```
Close the WebSocket connection gracefully.

##### set_agora_params()
```python
async def set_agora_params(
    agora_app_id: str,
    agora_channel: str,
    agora_token: str,
    agora_uid: str,
    voice_id: Optional[str] = None,
    language: str = "en",
    background_url: Optional[str] = None
) -> None
```
Configure Agora RTC parameters (required before sending audio).

**Parameters:**
- `agora_app_id`: Agora application ID
- `agora_channel`: Agora channel name
- `agora_token`: Agora RTC token
- `agora_uid`: Agora user ID
- `voice_id`: Voice ID for the avatar (optional)
- `language`: Language code (default: "en")
- `background_url`: Background image/video URL (optional)

**Raises:**
- `ConnectionError`: Not connected to server
- `AudioStreamError`: If setting parameters fails

##### send_audio()
```python
async def send_audio(audio_data: bytes) -> None
```
Send PCM audio data to the avatar.

**Parameters:**
- `audio_data`: PCM audio bytes (16-bit, 16kHz, mono)

**Raises:**
- `ConnectionError`: Not connected to server
- `AudioStreamError`: Audio transmission failed

##### send_audio_stream()
```python
async def send_audio_stream(audio_chunks: List[bytes]) -> None
```
Send multiple audio chunks in sequence.

**Parameters:**
- `audio_chunks`: List of PCM audio data chunks

**Raises:**
- `ConnectionError`: Not connected to server
- `AudioStreamError`: If sending audio fails

##### interrupt()
```python
async def interrupt() -> None
```
Send interrupt command to stop current avatar response.

**Raises:**
- `ConnectionError`: If not connected

##### Event Handlers

The client supports event-driven programming through callback properties:

```python
# Set event handlers
client.on_connected = lambda: print("Connected!")
client.on_disconnected = lambda: print("Disconnected!")
client.on_agora_connected = lambda channel: print(f"Agora connected: {channel}")
client.on_error = lambda error: print(f"Error: {error}")
client.on_message = lambda message: print(f"Message: {message}")
```

**Available event handlers:**
- `on_connected`: Called when WebSocket connection is established
- `on_disconnected`: Called when connection is lost
- `on_agora_connected`: Called when Agora connection is established (receives channel ID)
- `on_error`: Called when errors occur (receives Exception)
- `on_message`: Called when receiving messages from server (receives Dict)

##### get_connection_info()
```python
def get_connection_info() -> Dict[str, Any]
```
Get information about the current connection.

**Returns:**
- Dictionary with connection information including status, session ID, service details

##### Connection Status Properties

The client provides several properties to check connection status:

```python
# Check WebSocket connection status
if client.is_connected:
    print("✅ WebSocket connected")

# Check Agora connection status  
if client.is_agora_connected:
    print("✅ Agora connected")

# Get detailed connection information
connection_info = client.get_connection_info()
print(f"📊 Connection details: {connection_info}")
```

**Connection Status Properties:**
- `client.is_connected`: Boolean indicating if WebSocket is connected
- `client.is_agora_connected`: Boolean indicating if Agora connection is established
- `client.session_id`: Current session ID string

## Monitoring Connection Status

### Real-time Connection Monitoring

```python
import asyncio
from akool_streaming_avatar import StreamingAvatarClient

async def monitor_connection():
    client = StreamingAvatarClient(
        api_key="your-api-key",
        discovery_url="https://api.akool.com/streamingAvatar/service_status", 
        avatar_id="your-avatar-id"
    )
    
    # Set up event handlers for real-time monitoring
    def on_connected():
        print("🔗 WebSocket connected!")
        
    def on_agora_connected(channel_id: str):
        print(f"🎥 Agora connected to channel: {channel_id}")
        
    def on_message_received(message):
        msg_type = message.get("type")
        print(f"📨 Received message: {msg_type}")
        
        # Handle different message types
        if msg_type == "system":
            handle_system_message(message)
        elif msg_type == "ack":
            handle_acknowledgment(message)
        elif msg_type == "error":
            handle_error_message(message)
            
    def on_error_occurred(error):
        print(f"❌ Error: {error}")
        
    def on_disconnected():
        print("🔌 Connection lost!")
    
    # Register event handlers
    client.on_connected = on_connected
    client.on_agora_connected = on_agora_connected
    client.on_message = on_message_received
    client.on_error = on_error_occurred
    client.on_disconnected = on_disconnected
    
    try:
        # Connect to service
        await client.connect()
        print(f"✅ Initial connection: {client.is_connected}")
        
        # Set Agora parameters and wait for connection
        await client.set_agora_params(
            agora_app_id="your-agora-app-id",
            agora_channel="your-channel", 
            agora_token="your-rtc-token",
            agora_uid="12345"
        )
        
        # Check status after Agora setup
        print(f"🎥 Agora connected: {client.is_agora_connected}")
        
        # Monitor connection for 30 seconds
        for i in range(6):
            await asyncio.sleep(5)
            
            # Check connection health
            info = client.get_connection_info()
            print(f"📊 Status check {i+1}: WebSocket={info['connected']}, "
                  f"Agora={info['agora_connected']}")
            
    finally:
        await client.disconnect()

def handle_system_message(message):
    """Handle system messages from the server."""
    pld = message.get("pld", {})
    status = pld.get("status")
    
    if status == "websocket_connected":
        print("✅ WebSocket connection confirmed by server")
    elif status == "agora_connected": 
        channel_id = pld.get("channel_id", "")
        print(f"✅ Agora connection confirmed: {channel_id}")
    else:
        print(f"ℹ️ System status: {status}")

def handle_acknowledgment(message):
    """Handle acknowledgment messages."""
    pld = message.get("pld", {})
    original_mid = pld.get("original_mid")
    print(f"✅ Command acknowledged: {original_mid}")

def handle_error_message(message):
    """Handle error messages from server."""
    pld = message.get("pld", {})
    error_code = pld.get("error_code")
    error_message = pld.get("error_message", "Unknown error")
    print(f"❌ Server error {error_code}: {error_message}")

asyncio.run(monitor_connection())
```

### Polling Connection Status

```python
async def check_connection_status(client):
    """Periodically check connection status."""
    while True:
        try:
            # Get current status
            info = client.get_connection_info()
            
            print(f"📊 Connection Status:")
            print(f"   WebSocket: {'✅' if info['connected'] else '❌'}")
            print(f"   Agora: {'✅' if info['agora_connected'] else '❌'}")
            print(f"   Session: {info['session_id']}")
            print(f"   Service: {info['current_service']}")
            
            # Wait before next check
            await asyncio.sleep(10)
            
        except Exception as e:
            print(f"❌ Status check failed: {e}")
            break
```

## WebSocket Message Types

The SDK receives various message types from the server. Here are the common message types and their meanings:

### System Messages
```json
{
    "v": 2,
    "type": "system", 
    "mid": "system-123",
    "pld": {
        "status": "websocket_connected" | "agora_connected",
        "channel_id": "channel-name"  // Only for agora_connected
    }
}
```

### Acknowledgment Messages
```json
{
    "v": 2,
    "type": "ack",
    "mid": "ack-123", 
    "pld": {
        "original_mid": "cmd-set-params-456",
        "status": "success"
    }
}
```

### Error Messages
```json
{
    "v": 2,
    "type": "error",
    "mid": "error-123",
    "pld": {
        "error_code": 4001,
        "error_message": "Authentication failed"
    }
}
```

### Pong Messages (Heartbeat Response)
```json
{
    "v": 2,
    "type": "pong",
    "mid": "pong-123",
    "pld": {}
}
```

## Advanced Usage

### Manual Connection Management

```python
client = StreamingAvatarClient(api_key, discovery_url, avatar_id)

try:
    await client.connect()
    await client.set_agora_params(
        agora_app_id=agora_app_id,
        agora_channel=channel,
        agora_token=rtc_token,
        agora_uid=user_id
    )
    
    # Your audio streaming logic here
    while streaming:
        audio_data = get_audio_data()
        await client.send_audio(audio_data)
        
finally:
    await client.disconnect()
```

### Event Callbacks

```python
def on_message_received(message):
    print(f"Received: {message}")

def on_error_occurred(error):
    print(f"Error: {error}")

def on_connection_lost():
    print("Connection lost")

# Set event handlers
client.on_message = on_message_received
client.on_error = on_error_occurred
client.on_disconnected = on_connection_lost
```

### Custom Retry Configuration

```python
client = StreamingAvatarClient(
    api_key="your-api-key",
    discovery_url="https://api.akool.com/streamingAvatar/service_status",
    avatar_id="your-avatar-id",
    max_retry_attempts=5,  # Try up to 5 times
    heartbeat_interval=15  # Ping every 15 seconds
)
```

## Error Handling

The SDK provides specific exception types for different error scenarios:

```python
from akool_streaming_avatar.exceptions import (
    AuthenticationError,
    ServiceDiscoveryError,
    ConnectionError,
    AudioStreamError,
    RetryError,
    ConfigurationError
)

try:
    await client.connect()
except AuthenticationError:
    print("Invalid API key")
except ServiceDiscoveryError:
    print("No available services")
except ConnectionError:
    print("Failed to connect")
except RetryError:
    print("All retry attempts failed")
```

## Audio Format Requirements

The SDK expects audio data in the following format:
- **Format**: PCM (uncompressed)
- **Sample Rate**: 16,000 Hz
- **Bit Depth**: 16-bit
- **Channels**: Mono (1 channel)
- **Encoding**: Little-endian

### Converting Audio

```python
import wave
import numpy as np

# Load and convert audio file
with wave.open('input.wav', 'rb') as wav_file:
    frames = wav_file.readframes(-1)
    sound_info = np.frombuffer(frames, dtype=np.int16)
    
    # Convert to mono if stereo
    if wav_file.getnchannels() == 2:
        sound_info = sound_info.reshape(-1, 2).mean(axis=1).astype(np.int16)
    
    # Resample to 16kHz if needed
    # (use librosa or scipy for resampling)
    
    # Send to avatar
    await client.send_audio(sound_info.tobytes())
```

## Service Discovery

The SDK automatically discovers available streaming avatar services by calling the service status endpoint. The discovery process:

1. Makes HTTP GET request to `discovery_url`
2. Parses the response to extract available services
3. Randomly selects a service for load balancing
4. Attempts WebSocket connection
5. Falls back to other services if connection fails

### Expected Service Response Format

```json
{
    "success": true,
    "data": {
        "services": [
            {
                "host": "avatar1.akool.com",
                "port": 8080,
                "status": "active"
            },
            {
                "host": "avatar2.akool.com", 
                "port": 8080,
                "status": "active"
            }
        ]
    }
}
```

## WebSocket Protocol

The SDK uses WebSocket protocol version 2 with the following message format:

### Authentication
```json
{
    "type": "auth",
    "token": "your-api-key",
    "avatar_id": "your-avatar-id"
}
```

### Agora Configuration
```json
{
    "type": "agora_params",
    "data": {
        "channel": "channel-name",
        "userId": 12345,
        "rtcToken": "agora-rtc-token"
    }
}
```

### Audio Data
```json
{
    "type": "audio_data",
    "data": "base64-encoded-pcm-audio"
}
```

### Heartbeat
```json
{
    "type": "ping"
}
```

## Development

### Setting up Development Environment

```bash
git clone https://github.com/akoolteam/akool-streaming-avatar-sdk.git
cd akool-streaming-avatar-sdk
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest tests/
```

### Code Formatting

```bash
black akool_streaming_avatar/
flake8 akool_streaming_avatar/
```

## Examples

See the `examples/` directory for more usage examples:

- `basic_usage.py` - Simple connection and audio streaming
- `error_handling.py` - Comprehensive error handling patterns

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Run the test suite
6. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support, please contact [support@akool.com](mailto:support@akool.com) or visit our [documentation](https://docs.akool.com).

## Changelog

### v0.1.0 (2024-01-XX)

- Initial release
- Basic WebSocket connection and authentication
- Service discovery and load balancing
- Audio streaming support
- Retry logic and error handling
- Event callback system 