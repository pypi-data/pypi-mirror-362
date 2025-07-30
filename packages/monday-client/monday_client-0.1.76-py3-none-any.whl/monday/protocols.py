# This file is part of monday-client.
#
# Copyright (C) 2024 Leet Cyber Security <https://leetcybersecurity.com/>
#
# monday-client is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# monday-client is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with monday-client. If not, see <https://www.gnu.org/licenses/>.

"""
Protocols for dependency injection in monday-client.

This module defines the interfaces that services depend on, allowing for
better testability and flexibility in HTTP backend implementations.
"""

from typing import Any, Protocol


class HTTPClient(Protocol):
    """
    Protocol defining the interface for HTTP clients used by monday services.

    This allows services to depend on an abstract interface rather than
    concrete implementations, enabling easier testing and backend swapping.
    """

    async def post_request(self, query: str) -> dict[str, Any]:
        """
        Execute a POST request to the monday.com API.

        Args:
            query: The GraphQL query string to execute

        Returns:
            Response data from the API

        Raises:
            Various exceptions for different error conditions

        """
        ...


class MondayClientProtocol(HTTPClient, Protocol):
    """
    Extended protocol for MondayClient that includes additional properties
    that services might need.
    """

    @property
    def api_key(self) -> str:
        """The API key used for authentication."""
        ...

    @property
    def url(self) -> str:
        """The API endpoint URL."""
        ...

    @property
    def version(self) -> str | None:
        """The API version being used."""
        ...

    @property
    def headers(self) -> dict[str, Any]:
        """HTTP headers used for requests."""
        ...

    @property
    def max_retries(self) -> int:
        """Maximum number of retry attempts."""
        ...


class ConfigProvider(Protocol):
    """
    Protocol for configuration providers.

    This allows for different configuration sources (files, environment,
    databases, etc.) to be used interchangeably.
    """

    def get_config(self) -> Any:  # MondayConfig
        """Get the Monday configuration."""
        ...

    def validate_config(self) -> bool:
        """Validate the configuration."""
        ...

    def reload_config(self) -> None:
        """Reload configuration from source."""
        ...


class LoggerProvider(Protocol):
    """
    Protocol for logging providers.

    This allows for different logging implementations to be used.
    """

    def get_logger(self, name: str) -> Any:
        """Get a logger instance."""
        ...

    def set_level(self, level: str) -> None:
        """Set the logging level."""
        ...

    def add_handler(self, handler: Any) -> None:
        """Add a logging handler."""
        ...


class RateLimiter(Protocol):
    """
    Protocol for rate limiting implementations.

    This allows for different rate limiting strategies to be used.
    """

    async def acquire(self) -> None:
        """Acquire a rate limit token."""
        ...

    async def release(self) -> None:
        """Release a rate limit token."""
        ...

    def get_reset_time(self) -> float:
        """Get the time until rate limit resets."""
        ...

    def is_limited(self) -> bool:
        """Check if currently rate limited."""
        ...


class CacheProvider(Protocol):
    """
    Protocol for cache implementations.

    This allows for different caching backends to be used.
    """

    async def get(self, key: str) -> Any | None:
        """Get a value from cache."""
        ...

    async def set(self, key: str, value: Any, ttl: int | None = None) -> None:
        """Set a value in cache."""
        ...

    async def delete(self, key: str) -> None:
        """Delete a value from cache."""
        ...

    async def clear(self) -> None:
        """Clear all cached values."""
        ...


class MetricsProvider(Protocol):
    """
    Protocol for metrics collection.

    This allows for different metrics backends to be used.
    """

    def increment(
        self, metric: str, value: int = 1, tags: dict[str, str] | None = None
    ) -> None:
        """Increment a counter metric."""
        ...

    def timing(
        self, metric: str, value: float, tags: dict[str, str] | None = None
    ) -> None:
        """Record a timing metric."""
        ...

    def gauge(
        self, metric: str, value: float, tags: dict[str, str] | None = None
    ) -> None:
        """Set a gauge metric."""
        ...
