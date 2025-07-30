"""
Akool Streaming Avatar SDK - A Python client for connecting to Akool's streaming avatar services.

This SDK provides a simple interface to:
- Discover available streaming avatar services
- Connect to streaming avatar services via WebSocket
- Send audio streams to animate avatars
- Handle authentication and connection management
"""

__version__ = "0.1.0"
__author__ = "Akool"
__email__ = "support@akool.com"

from .client import StreamingAvatarClient, AsyncStreamingAvatarClient
from .exceptions import (
    AkoolStreamingAvatarError,
    AuthenticationError,
    ConnectionError,
    ServiceDiscoveryError,
    AudioStreamError,
    RetryError,
    ConfigurationError,
)

__all__ = [
    "StreamingAvatarClient",
    "AsyncStreamingAvatarClient",
    "AkoolStreamingAvatarError", 
    "AuthenticationError",
    "ConnectionError",
    "ServiceDiscoveryError",
    "AudioStreamError",
    "RetryError",
    "ConfigurationError",
]
