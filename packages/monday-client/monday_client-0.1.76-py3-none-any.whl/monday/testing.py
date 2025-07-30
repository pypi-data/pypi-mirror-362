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
Testing utilities for monday-client.

This module provides mock implementations and testing utilities for the
monday-client library.
"""

# ruff: noqa: S101

from collections.abc import Callable
from typing import Any
from unittest.mock import AsyncMock


class MockHTTPClient:
    """
    Mock HTTP client for testing purposes.

    This class implements the HTTPClient protocol and allows for easy
    testing of services without making actual HTTP requests.
    """

    def __init__(
        self,
        responses: dict[str, dict[str, Any]] | None = None,
        side_effect: Callable[[str], dict[str, Any]] | None = None,
        exception: Exception | None = None,
    ):
        """
        Initialize the mock client.

        Args:
            responses: Dictionary mapping query strings to response data
            side_effect: Callable that takes a query string and returns response data
            exception: Exception to raise on all requests

        """
        self.responses = responses or {}
        self.side_effect = side_effect
        self.exception = exception
        self.request_history: list[str] = []
        self._mock = AsyncMock()

    async def post_request(self, query: str) -> dict[str, Any]:
        """
        Mock implementation of post_request.

        Args:
            query: The GraphQL query string

        Returns:
            Mock response data

        Raises:
            The configured exception if set

        """
        self.request_history.append(query)

        if self.exception:
            raise self.exception

        if self.side_effect:
            return self.side_effect(query)

        # Try exact match first
        if query in self.responses:
            return self.responses[query]

        # Try partial match for common patterns
        for pattern, response in self.responses.items():
            if pattern in query or query in pattern:
                return response

        # Default response
        return {'data': {'mock': 'response'}}

    def assert_called_with(self, query: str) -> None:
        """Assert that the client was called with the specified query."""
        assert query in self.request_history, (
            f'Query "{query}" not found in request history'
        )

    def assert_called_times(self, expected_count: int) -> None:
        """Assert that the client was called the expected number of times."""
        actual_count = len(self.request_history)
        assert actual_count == expected_count, (
            f'Expected {expected_count} calls, got {actual_count}'
        )

    def reset(self) -> None:
        """Reset the mock state."""
        self.request_history.clear()
        self._mock.reset_mock()


class MockMondayClient:
    """
    Mock MondayClient for testing purposes.

    This class provides a complete mock implementation of MondayClient
    that can be used to test services without making actual API calls.
    """

    def __init__(  # noqa: PLR0913
        self,
        api_key: str = 'test_api_key',
        url: str = 'https://api.monday.com/v2',
        version: str | None = '2024-01',
        headers: dict[str, Any] | None = None,
        max_retries: int = 4,
        responses: dict[str, dict[str, Any]] | None = None,
        side_effect: Callable[[str], dict[str, Any]] | None = None,
        exception: Exception | None = None,
    ):
        """
        Initialize the mock client.

        Args:
            api_key: Mock API key
            url: Mock API URL
            version: Mock API version
            headers: Mock headers
            max_retries: Mock max retries
            responses: Responses for the HTTP client
            side_effect: Side effect for the HTTP client
            exception: Exception to raise

        """
        self.api_key = api_key
        self.url = url
        self.version = version
        self.headers = headers or {
            'Content-Type': 'application/json',
            'Authorization': api_key,
        }
        self.max_retries = max_retries

        # Create mock HTTP client
        self._http_client = MockHTTPClient(responses, side_effect, exception)

        # Initialize service instances with mock client
        from monday.services.boards import Boards  # noqa: PLC0415
        from monday.services.groups import Groups  # noqa: PLC0415
        from monday.services.items import Items  # noqa: PLC0415
        from monday.services.subitems import Subitems  # noqa: PLC0415
        from monday.services.users import Users  # noqa: PLC0415

        self.boards = Boards(self)  # pyright: ignore [reportArgumentType]
        self.items = Items(self, self.boards)  # pyright: ignore [reportArgumentType]
        self.subitems = Subitems(self, self.items, self.boards)  # pyright: ignore [reportArgumentType]
        self.groups = Groups(self, self.boards)  # pyright: ignore [reportArgumentType]
        self.users = Users(self)  # pyright: ignore [reportArgumentType]

    async def post_request(self, query: str) -> dict[str, Any]:
        """Delegate to the mock HTTP client."""
        return await self._http_client.post_request(query)

    def assert_called_with(self, query: str) -> None:
        """Assert that the client was called with the specified query."""
        self._http_client.assert_called_with(query)

    def assert_called_times(self, expected_count: int) -> None:
        """Assert that the client was called the expected number of times."""
        self._http_client.assert_called_times(expected_count)

    def reset(self) -> None:
        """Reset the mock state."""
        self._http_client.reset()


# Convenience function for creating mock clients
def create_mock_client(
    responses: dict[str, dict[str, Any]] | None = None,
    **kwargs: Any,
) -> MockMondayClient:
    """
    Create a mock MondayClient for testing.

    Args:
        responses: Dictionary mapping query strings to response data
        **kwargs: Additional arguments for MockMondayClient

    Returns:
        Configured MockMondayClient instance

    """
    return MockMondayClient(responses=responses, **kwargs)
