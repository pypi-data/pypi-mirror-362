"""
Basic usage example for the Akool Streaming Avatar SDK.

This example shows how to:
1. Connect to a streaming avatar service
2. Set up Agora parameters
3. Send audio data
4. Handle events and errors
"""

import asyncio
import logging
import wave
from pathlib import Path

from akool_streaming_avatar import StreamingAvatarClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def basic_example():
    """Basic example of using the streaming avatar client."""

    # Configuration
    API_KEY = "your_api_key_here"  # Replace with your actual API key
    DISCOVERY_URL = "http://your-discovery-server.com"  # Replace with actual discovery URL
    AVATAR_ID = "dvp_Tristan_cloth2_1080P"  # Replace with your avatar ID

    # Agora configuration (replace with your actual Agora credentials)
    AGORA_APP_ID = "your_agora_app_id"
    AGORA_CHANNEL = "test_channel_123"
    AGORA_TOKEN = "your_agora_token"
    AGORA_UID = "12345"

    # Create client
    client = StreamingAvatarClient(
        api_key=API_KEY, discovery_url=DISCOVERY_URL, avatar_id=AVATAR_ID, max_retry_attempts=3
    )

    # Set up event handlers
    def on_connected():
        logger.info("🎉 Connected to streaming avatar service!")

    def on_agora_connected(channel_id: str):
        logger.info(f"🎥 Agora connected to channel: {channel_id}")

    def on_error(error: Exception):
        logger.error(f"❌ Error occurred: {error}")

    def on_disconnected():
        logger.info("👋 Disconnected from streaming avatar service")

    # Register event handlers
    client.on_connected = on_connected
    client.on_agora_connected = on_agora_connected
    client.on_error = on_error
    client.on_disconnected = on_disconnected

    try:
        # Connect to the service
        logger.info("🔗 Connecting to streaming avatar service...")
        await client.connect()

        # Set Agora parameters
        logger.info("⚙️ Setting Agora parameters...")
        await client.set_agora_params(
            agora_app_id=AGORA_APP_ID,
            agora_channel=AGORA_CHANNEL,
            agora_token=AGORA_TOKEN,
            agora_uid=AGORA_UID,
            language="en",
            voice_id="1",  # Optional: specify voice ID
        )

        # Load and send audio data
        audio_file = Path(__file__).parent / "sample_audio.wav"  # You need to provide this file
        if audio_file.exists():
            logger.info("🎵 Sending audio data...")
            await send_audio_file(client, audio_file)
        else:
            logger.info("🎵 Sending sample audio data...")
            await send_sample_audio(client)

        # Keep connection alive for a while
        logger.info("⏳ Keeping connection alive for 10 seconds...")
        await asyncio.sleep(10)

    except Exception as e:
        logger.error(f"❌ Example failed: {e}")
    finally:
        # Disconnect
        logger.info("🔌 Disconnecting...")
        await client.disconnect()


async def send_audio_file(client: StreamingAvatarClient, audio_file: Path):
    """Send audio from a WAV file."""
    with wave.open(str(audio_file), "rb") as wav_file:
        # Validate audio format
        if wav_file.getnchannels() != 1:
            raise ValueError("Audio must be mono (1 channel)")
        if wav_file.getsampwidth() != 2:
            raise ValueError("Audio must be 16-bit")
        if wav_file.getframerate() != 16000:
            raise ValueError("Audio must be 16kHz sample rate")

        # Read audio data in chunks
        chunk_size = 1024  # 64ms at 16kHz
        frames_read = 0
        total_frames = wav_file.getnframes()

        while frames_read < total_frames:
            chunk = wav_file.readframes(chunk_size)
            if not chunk:
                break

            await client.send_audio(chunk)
            frames_read += len(chunk) // wav_file.getsampwidth()

            # Small delay to simulate real-time streaming
            await asyncio.sleep(0.064)  # 64ms

        logger.info(f"✅ Sent {frames_read} audio frames")


async def send_sample_audio(client: StreamingAvatarClient):
    """Send sample audio data (silence)."""
    # Generate 2 seconds of silence (16kHz, 16-bit, mono)
    sample_rate = 16000
    duration = 2.0
    chunk_size = 1024  # 64ms chunks

    total_samples = int(sample_rate * duration)
    samples_sent = 0

    while samples_sent < total_samples:
        # Create chunk of silence (16-bit PCM)
        chunk_samples = min(chunk_size, total_samples - samples_sent)
        chunk = b"\x00" * (chunk_samples * 2)  # 2 bytes per sample

        await client.send_audio(chunk)
        samples_sent += chunk_samples

        # Small delay to simulate real-time streaming
        await asyncio.sleep(0.064)  # 64ms

    logger.info(f"✅ Sent {samples_sent} audio samples (silence)")


async def context_manager_example():
    """Example using async context manager for automatic connection management."""

    from akool_streaming_avatar import AsyncStreamingAvatarClient

    API_KEY = "your_api_key_here"
    DISCOVERY_URL = "http://your-discovery-server.com"
    AVATAR_ID = "dvp_Tristan_cloth2_1080P"

    async with AsyncStreamingAvatarClient(api_key=API_KEY, discovery_url=DISCOVERY_URL, avatar_id=AVATAR_ID) as client:
        # Client is automatically connected
        logger.info("🎉 Using context manager - connected!")

        # Get connection info
        info = client.get_connection_info()
        logger.info(f"📊 Connection info: {info}")

        # Do work with the client...
        await asyncio.sleep(2)

    # Client is automatically disconnected when exiting the context


if __name__ == "__main__":
    print("🚀 Starting Akool Streaming Avatar SDK Basic Example")

    # Run the basic example
    asyncio.run(basic_example())

    print("\n" + "=" * 50)
    print("🔄 Running context manager example")

    # Run the context manager example
    asyncio.run(context_manager_example())

    print("✅ Examples completed!")
