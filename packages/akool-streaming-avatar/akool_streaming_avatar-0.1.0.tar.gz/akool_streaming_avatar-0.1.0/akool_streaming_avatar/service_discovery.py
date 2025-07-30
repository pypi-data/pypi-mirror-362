"""
Service discovery module for finding available streaming avatar services.
"""

import logging
import random
import requests
from typing import List, Dict, Optional, Tuple
from urllib.parse import urljoin

from .exceptions import ServiceDiscoveryError, AuthenticationError

logger = logging.getLogger(__name__)


class ServiceInstance:
    """Represents a single streaming avatar service instance."""

    def __init__(self, ip: str, port: int, avatar_id: str, status: str, healthy: bool, index: int):
        self.ip = ip
        self.port = port
        self.avatar_id = avatar_id
        self.status = status
        self.healthy = healthy
        self.index = index

    @property
    def base_url(self) -> str:
        """Get the base URL for this service instance."""
        return f"http://{self.ip}:{self.port}"

    @property
    def websocket_url(self) -> str:
        """Get the WebSocket URL for this service instance."""
        return f"ws://{self.ip}:{self.port}/streamingAvatar/ws/v1"

    @property
    def is_available(self) -> bool:
        """Check if this service instance is available for new connections."""
        return self.healthy and self.status == "available"

    def __str__(self):
        return f"ServiceInstance(ip={self.ip}, port={self.port}, avatar_id={self.avatar_id}, status={self.status}, healthy={self.healthy})"

    def __repr__(self):
        return self.__str__()


class ServiceDiscovery:
    """Service discovery client for finding available streaming avatar services."""

    def __init__(self, api_key: str, timeout: int = 10):
        """
        Initialize service discovery client.

        Args:
            api_key: API key for authentication
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.timeout = timeout

    def discover_services(self, base_url: str, avatar_id: Optional[str] = None) -> List[ServiceInstance]:
        """
        Discover available streaming avatar services.

        Args:
            base_url: Base URL of the service discovery endpoint
            avatar_id: Filter services by avatar ID (optional)

        Returns:
            List of available service instances

        Raises:
            ServiceDiscoveryError: If service discovery fails
            AuthenticationError: If authentication fails
        """
        url = urljoin(base_url.rstrip("/"), "/streamingAvatar/service_status")
        headers = {"api_key": self.api_key, "Content-Type": "application/json"}

        try:
            logger.info(f"Discovering services from {url}")
            response = requests.get(url, headers=headers, timeout=self.timeout)

            if response.status_code == 401:
                raise AuthenticationError("Invalid or missing API key")
            elif response.status_code != 200:
                raise ServiceDiscoveryError(
                    f"Service discovery failed with status {response.status_code}: {response.text}"
                )

            data = response.json()

            if data.get("code") != 1000:
                error_msg = data.get("msg", "Unknown error")
                if data.get("code") == 4001:
                    raise AuthenticationError(f"Authentication failed: {error_msg}")
                else:
                    raise ServiceDiscoveryError(f"Service discovery failed: {error_msg}")

            instances_data = data.get("data", {})
            instances = []

            for instance_data in instances_data.get("instances", []):
                instance = ServiceInstance(
                    ip=instance_data["ip"],
                    port=instance_data["port"],
                    avatar_id=instance_data["avatar_id"],
                    status=instance_data["status"],
                    healthy=instance_data["healthy"],
                    index=instance_data["index"],
                )

                # Filter by avatar_id if specified
                if avatar_id is None or instance.avatar_id == avatar_id:
                    instances.append(instance)

            logger.info(f"Discovered {len(instances)} service instances")
            return instances

        except requests.exceptions.Timeout:
            raise ServiceDiscoveryError(f"Service discovery request timed out after {self.timeout} seconds")
        except requests.exceptions.ConnectionError as e:
            raise ServiceDiscoveryError(f"Failed to connect to service discovery endpoint: {e}")
        except requests.exceptions.RequestException as e:
            raise ServiceDiscoveryError(f"Service discovery request failed: {e}")
        except Exception as e:
            raise ServiceDiscoveryError(f"Unexpected error during service discovery: {e}")

    def find_available_service(
        self, base_url: str, avatar_id: str, prefer_random: bool = True
    ) -> Optional[ServiceInstance]:
        """
        Find an available service instance for the specified avatar.

        Args:
            base_url: Base URL of the service discovery endpoint
            avatar_id: Avatar ID to find services for
            prefer_random: Whether to randomly select from available services to avoid conflicts

        Returns:
            Available service instance or None if no services available

        Raises:
            ServiceDiscoveryError: If service discovery fails
            AuthenticationError: If authentication fails
        """
        instances = self.discover_services(base_url, avatar_id)

        # Filter for available instances
        available_instances = [instance for instance in instances if instance.is_available]

        if not available_instances:
            logger.warning(f"No available service instances found for avatar_id: {avatar_id}")
            return None

        if prefer_random:
            # Randomly select to avoid conflicts when multiple clients connect simultaneously
            selected = random.choice(available_instances)
            logger.info(f"Randomly selected service instance: {selected}")
        else:
            # Select the first available instance
            selected = available_instances[0]
            logger.info(f"Selected first available service instance: {selected}")

        return selected

    def find_multiple_services(self, base_url: str, avatar_id: str, count: int = 3) -> List[ServiceInstance]:
        """
        Find multiple available service instances for fallback/retry purposes.

        Args:
            base_url: Base URL of the service discovery endpoint
            avatar_id: Avatar ID to find services for
            count: Maximum number of service instances to return

        Returns:
            List of available service instances (up to 'count' instances)

        Raises:
            ServiceDiscoveryError: If service discovery fails
            AuthenticationError: If authentication fails
        """
        instances = self.discover_services(base_url, avatar_id)

        # Filter for available instances
        available_instances = [instance for instance in instances if instance.is_available]

        if not available_instances:
            logger.warning(f"No available service instances found for avatar_id: {avatar_id}")
            return []

        # Shuffle to randomize selection order
        random.shuffle(available_instances)

        # Return up to 'count' instances
        selected_instances = available_instances[:count]
        logger.info(f"Selected {len(selected_instances)} service instances for fallback")

        return selected_instances
