"""
Custom exceptions for the Akool Streaming Avatar SDK.
"""


class AkoolStreamingAvatarError(Exception):
    """Base exception for all Akool Streaming Avatar SDK errors."""

    pass


class AuthenticationError(AkoolStreamingAvatarError):
    """Raised when authentication fails."""

    pass


class ConnectionError(AkoolStreamingAvatarError):
    """Raised when connection to the streaming avatar service fails."""

    pass


class ServiceDiscoveryError(AkoolStreamingAvatarError):
    """Raised when service discovery fails or no available services found."""

    pass


class AudioStreamError(AkoolStreamingAvatarError):
    """Raised when audio streaming encounters an error."""

    pass


class RetryError(AkoolStreamingAvatarError):
    """Raised when all retry attempts are exhausted."""

    pass


class ConfigurationError(AkoolStreamingAvatarError):
    """Raised when there's an issue with SDK configuration."""

    pass
