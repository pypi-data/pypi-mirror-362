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

"""Base service class for common Monday.com API operations."""

import logging
from typing import TYPE_CHECKING, Any, Literal

from monday.services.utils.error_handlers import check_query_result
from monday.services.utils.fields import Fields
from monday.services.utils.query_builder import (
    build_graphql_query,
    build_query_params_string,
)

if TYPE_CHECKING:
    from monday.client import MondayClient


class BaseService:
    """Base class for Monday.com service operations."""

    _logger: logging.Logger = logging.getLogger(__name__)

    def __init__(self, client: 'MondayClient'):
        """Initialize the base service with a client."""
        self.client = client

    async def execute_query(
        self,
        operation: str,
        args: dict[str, Any] | None = None,
        query_type: Literal['query', 'mutation'] = 'query',
    ) -> dict[str, Any]:
        """
        Execute a GraphQL query or mutation.

        Args:
            operation: The GraphQL operation name (e.g., 'boards', 'items')
            args: Arguments for the operation
            query_type: Type of operation ('query' or 'mutation')

        Returns:
            The response data from the API

        """
        query_string = build_graphql_query(operation, query_type, args)
        query_result = await self.client.post_request(query_string)
        return check_query_result(query_result)

    async def execute_paginated_query(  # noqa: PLR0913
        self,
        operation: str,
        args: dict[str, Any],
        data_key: str,
        *,
        paginate: bool = True,
        limit_key: str = 'limit',
        page_key: str = 'page',
    ) -> list[dict[str, Any]]:
        """
        Execute a paginated query.

        Args:
            operation: The GraphQL operation name
            args: Arguments for the operation
            data_key: Key in response data containing the results
            paginate: Whether to paginate results
            limit_key: Key for the limit parameter
            page_key: Key for the page parameter

        Returns:
            List of all results from pagination

        """
        results = []
        last_response = None

        while True:
            query_result = await self.execute_query(operation, args, 'query')
            data = query_result.get('data', {})
            current_items = data.get(data_key, [])

            if not current_items:
                break

            if current_items == last_response:
                break

            results.extend(current_items)
            last_response = current_items

            if len(current_items) < args.get(limit_key, 25):
                break

            if not paginate:
                break

            args[page_key] = args.get(page_key, 1) + 1

        return results

    def process_column_values(
        self,
        column_values: list[Any] | dict[str, Any] | None,
    ) -> dict[str, Any]:
        """
        Process column values for API requests.

        Args:
            column_values: Column values as list of objects or dict

        Returns:
            Processed column values as dict

        """
        if not column_values:
            return {}

        if isinstance(column_values, dict):
            return column_values

        if isinstance(column_values, list):
            processed = {}
            for column_input in column_values:
                if hasattr(column_input, 'column_id') and hasattr(
                    column_input, 'column_values'
                ):
                    processed[column_input.column_id] = column_input.column_values
                elif isinstance(column_input, dict):
                    processed[column_input['column_id']] = column_input['column_values']
            return processed

        return {}

    def build_fields_with_temp(
        self,
        fields: str | Fields,
        temp_fields: list[str] | None = None,
    ) -> Fields:
        """
        Build fields with temporary fields for deduplication.

        Args:
            fields: Base fields
            temp_fields: Temporary fields to add

        Returns:
            Fields object with temp fields added

        """
        fields_obj = Fields(fields)
        if temp_fields:
            fields_obj = fields_obj.add_temp_fields(temp_fields)
        return fields_obj

    def cleanup_temp_fields(
        self,
        data: list[dict[str, Any]] | dict[str, Any],
        original_fields: str | Fields,
        temp_fields: list[str],
    ) -> list[dict[str, Any]] | dict[str, Any]:
        """
        Clean up temporary fields from response data.

        Args:
            data: Response data
            original_fields: Original fields requested
            temp_fields: Temporary fields to remove

        Returns:
            Cleaned data

        """
        return Fields.manage_temp_fields(data, original_fields, temp_fields)

    def normalize_id_list(
        self, ids: int | str | list[int | str] | None
    ) -> list[int | str] | None:
        """Normalize ID parameters to always be a list."""
        if ids is None:
            return None
        if isinstance(ids, list):
            return ids
        return [ids]

    def build_pagination_args(
        self,
        limit: int = 25,
        page: int = 1,
        *,
        paginate: bool = True,
    ) -> dict[str, Any]:
        """Build common pagination arguments."""
        args = {'limit': limit}
        if paginate:
            args['page'] = page
        return args

    def build_filter_args(
        self,
        *,
        state: str | None = None,
        kind: str | None = None,
        order_by: str | None = None,
    ) -> dict[str, Any]:
        """Build common filter arguments."""
        args = {}
        if state and state != 'all':
            args['state'] = state
        if kind and kind != 'all':
            args['kind'] = kind
        if order_by:
            args['order_by'] = f'{order_by}_at'
        return args

    def deduplicate_results(
        self, results: list[dict[str, Any]], id_key: str = 'id'
    ) -> list[dict[str, Any]]:
        """Remove duplicate results by ID."""
        seen_ids = set()
        unique_results = []
        for result in results:
            if result.get(id_key) not in seen_ids:
                seen_ids.add(result.get(id_key))
                unique_results.append(result)
        return unique_results

    def convert_to_dataclass_list(
        self, data: list[dict[str, Any]], dataclass_type: type
    ) -> list[Any]:
        """Convert list of dictionaries to list of dataclass instances."""
        return [dataclass_type.from_dict(item) for item in data]

    def convert_to_dataclass(self, data: dict[str, Any], dataclass_type: type) -> Any:
        """Convert dictionary to dataclass instance."""
        return dataclass_type.from_dict(data)

    def build_mutation_args(
        self,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Build common mutation arguments."""
        args = {}
        for key, value in kwargs.items():
            if value is not None:
                if key == 'column_values':
                    args[key] = self.process_column_values(value)
                else:
                    args[key] = value
        return args

    def build_query_with_fields(
        self,
        fields: str | Fields,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Build query arguments with fields."""
        return {**kwargs, 'fields': fields}

    def handle_temp_fields(
        self,
        data: list[dict[str, Any]] | dict[str, Any],
        original_fields: str | Fields,
        temp_fields: list[str],
    ) -> list[dict[str, Any]] | dict[str, Any]:
        """Handle temporary fields for deduplication and cleanup."""
        if not temp_fields:
            return data

        # Deduplicate if it's a list
        if isinstance(data, list):
            data = self.deduplicate_results(data)

        # Clean up temp fields
        return self.cleanup_temp_fields(data, original_fields, temp_fields)

    def build_items_query_args(
        self,
        board_ids: int | str | list[int | str],
        fields: str | Fields,
        limit: int = 25,
        query_params: Any = None,
        group_id: str | None = None,
    ) -> dict[str, Any]:
        """Build arguments for items queries."""
        args = {
            'ids': self.normalize_id_list(board_ids),
            'limit': limit,
            'fields': f'id items_page {{ cursor items {{ {fields} }} }}',
        }

        if query_params:
            args['query_params'] = build_query_params_string(query_params)

        if group_id:
            args['group_id'] = group_id

        return args
