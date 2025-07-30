"""
Error handling and retry example for the Akool Streaming Avatar SDK.

This example demonstrates:
1. Handling various error scenarios
2. Retry logic and failover
3. Graceful error recovery
4. Connection monitoring
"""

import asyncio
import logging
from typing import Optional

from akool_streaming_avatar import (
    StreamingAvatarClient,
    AuthenticationError,
    ConnectionError,
    ServiceDiscoveryError,
    AudioStreamError,
    RetryError,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def error_handling_example():
    """Demonstrate comprehensive error handling."""

    # Test configuration with intentionally problematic values
    API_KEY = "test_api_key"  # This might be invalid
    DISCOVERY_URL = "http://localhost:8080"  # This might not exist
    AVATAR_ID = "test_avatar"  # This might not exist

    client = StreamingAvatarClient(
        api_key=API_KEY,
        discovery_url=DISCOVERY_URL,
        avatar_id=AVATAR_ID,
        max_retry_attempts=3,
        connection_timeout=10,
        discovery_timeout=5,
    )

    # Set up comprehensive error handling
    def on_error(error: Exception):
        if isinstance(error, AuthenticationError):
            logger.error(f"🔐 Authentication failed: {error}")
            logger.info("💡 Please check your API key")
        elif isinstance(error, ConnectionError):
            logger.error(f"🔌 Connection failed: {error}")
            logger.info("💡 The service might be busy or unavailable")
        elif isinstance(error, ServiceDiscoveryError):
            logger.error(f"🔍 Service discovery failed: {error}")
            logger.info("💡 Check your discovery URL and network connection")
        elif isinstance(error, AudioStreamError):
            logger.error(f"🎵 Audio streaming error: {error}")
            logger.info("💡 Check your audio format and connection")
        else:
            logger.error(f"❌ Unexpected error: {error}")

    client.on_error = on_error

    try:
        logger.info("🔗 Attempting to connect with error handling...")
        await client.connect()
        logger.info("✅ Connection successful!")

        # Try to send audio and handle potential errors
        await send_audio_with_retry(client)

    except AuthenticationError as e:
        logger.error(f"🔐 Authentication failed permanently: {e}")
        logger.info("💡 Solution: Verify your API key is correct")

    except ServiceDiscoveryError as e:
        logger.error(f"🔍 No services available: {e}")
        logger.info("💡 Solution: Check if services are running and avatar_id is correct")

    except RetryError as e:
        logger.error(f"🔄 All retry attempts failed: {e}")
        logger.info("💡 Solution: Try again later or contact support")

    except ConnectionError as e:
        logger.error(f"🔌 Connection failed: {e}")
        logger.info("💡 Solution: Check network connectivity and service availability")

    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")

    finally:
        # Always disconnect
        if client.is_connected:
            await client.disconnect()


async def send_audio_with_retry(client: StreamingAvatarClient, max_retries: int = 3):
    """Send audio with retry logic for handling temporary failures."""

    # Sample audio data
    audio_chunk = b"\x00" * 1024  # 1024 bytes of silence

    for attempt in range(max_retries + 1):
        try:
            logger.info(f"🎵 Sending audio (attempt {attempt + 1}/{max_retries + 1})...")
            await client.send_audio(audio_chunk)
            logger.info("✅ Audio sent successfully!")
            return

        except AudioStreamError as e:
            if attempt < max_retries:
                logger.warning(f"⚠️ Audio send failed (attempt {attempt + 1}): {e}")
                logger.info(f"🔄 Retrying in 2 seconds...")
                await asyncio.sleep(2)
            else:
                logger.error(f"❌ Audio send failed after {max_retries + 1} attempts: {e}")
                raise

        except ConnectionError as e:
            logger.error(f"🔌 Connection lost while sending audio: {e}")
            # Try to reconnect
            if attempt < max_retries:
                logger.info("🔄 Attempting to reconnect...")
                try:
                    await client.disconnect()
                    await client.connect()
                    logger.info("✅ Reconnected successfully!")
                except Exception as reconnect_error:
                    logger.error(f"❌ Reconnection failed: {reconnect_error}")
                    if attempt == max_retries:
                        raise
            else:
                raise


async def connection_monitoring_example():
    """Example of monitoring connection health and handling disconnections."""

    API_KEY = "your_api_key_here"
    DISCOVERY_URL = "http://localhost:8080"
    AVATAR_ID = "test_avatar"

    client = StreamingAvatarClient(
        api_key=API_KEY,
        discovery_url=DISCOVERY_URL,
        avatar_id=AVATAR_ID,
        heartbeat_interval=10,  # Shorter interval for monitoring
    )

    # Connection monitoring state
    connection_state = {"connected": False, "last_error": None, "reconnect_attempts": 0}

    def on_connected():
        logger.info("✅ Connection established")
        connection_state["connected"] = True
        connection_state["reconnect_attempts"] = 0

    def on_disconnected():
        logger.warning("⚠️ Connection lost")
        connection_state["connected"] = False

    def on_error(error: Exception):
        logger.error(f"❌ Connection error: {error}")
        connection_state["last_error"] = error

    # Register handlers
    client.on_connected = on_connected
    client.on_disconnected = on_disconnected
    client.on_error = on_error

    # Monitor connection for 30 seconds
    monitor_duration = 30
    check_interval = 5

    try:
        logger.info("🔗 Starting connection monitoring...")
        await client.connect()

        for i in range(0, monitor_duration, check_interval):
            await asyncio.sleep(check_interval)

            # Check connection health
            if client.is_connected:
                logger.info(f"💚 Connection healthy (uptime: {i + check_interval}s)")

                # Get detailed connection info
                info = client.get_connection_info()
                logger.debug(f"📊 Connection details: {info}")

            else:
                logger.warning(f"💔 Connection unhealthy (downtime detected)")

                # Attempt automatic reconnection
                if connection_state["reconnect_attempts"] < 3:
                    connection_state["reconnect_attempts"] += 1
                    logger.info(f"🔄 Attempting reconnection #{connection_state['reconnect_attempts']}...")

                    try:
                        await client.connect()
                        logger.info("✅ Automatic reconnection successful!")
                    except Exception as e:
                        logger.error(f"❌ Automatic reconnection failed: {e}")
                else:
                    logger.error("❌ Maximum reconnection attempts reached")
                    break

    except KeyboardInterrupt:
        logger.info("⏹️ Monitoring stopped by user")
    except Exception as e:
        logger.error(f"❌ Monitoring failed: {e}")
    finally:
        await client.disconnect()


async def service_discovery_error_demo():
    """Demonstrate service discovery error scenarios."""

    test_cases = [
        {
            "name": "Invalid API Key",
            "api_key": "invalid_key",
            "discovery_url": "http://localhost:8080",
            "avatar_id": "test_avatar",
        },
        {
            "name": "Invalid Discovery URL",
            "api_key": "test_key",
            "discovery_url": "http://nonexistent-server.com",
            "avatar_id": "test_avatar",
        },
        {
            "name": "Non-existent Avatar ID",
            "api_key": "test_key",
            "discovery_url": "http://localhost:8080",
            "avatar_id": "nonexistent_avatar",
        },
    ]

    for test_case in test_cases:
        logger.info(f"\n🧪 Testing: {test_case['name']}")

        client = StreamingAvatarClient(
            api_key=test_case["api_key"],
            discovery_url=test_case["discovery_url"],
            avatar_id=test_case["avatar_id"],
            max_retry_attempts=1,  # Quick failure for demo
            discovery_timeout=3,  # Short timeout for demo
        )

        try:
            await client.connect()
            logger.info("✅ Unexpected success - this test should have failed")
        except AuthenticationError as e:
            logger.info(f"🔐 Expected authentication error: {e}")
        except ServiceDiscoveryError as e:
            logger.info(f"🔍 Expected service discovery error: {e}")
        except ConnectionError as e:
            logger.info(f"🔌 Expected connection error: {e}")
        except Exception as e:
            logger.warning(f"⚠️ Unexpected error type: {e}")
        finally:
            await client.disconnect()


if __name__ == "__main__":
    print("🚀 Starting Error Handling Examples")

    # Run error handling example
    print("\n" + "=" * 50)
    print("📋 1. Basic Error Handling")
    asyncio.run(error_handling_example())

    # Run connection monitoring example
    print("\n" + "=" * 50)
    print("📊 2. Connection Monitoring")
    asyncio.run(connection_monitoring_example())

    # Run service discovery error demo
    print("\n" + "=" * 50)
    print("🔍 3. Service Discovery Error Demo")
    asyncio.run(service_discovery_error_demo())

    print("\n✅ Error handling examples completed!")
