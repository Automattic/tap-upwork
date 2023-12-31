"""GraphQL client handling, including UpWorkStream base class."""

from __future__ import annotations

from typing import Any

from singer_sdk.streams import GraphQLStream
from singer_sdk.typing import ObjectType, PropertiesList

from tap_upwork.auth import UpWorkAuthenticator


class UpWorkStream(GraphQLStream):
    """UpWork stream class."""

    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        return 'https://api.upwork.com/graphql'

    @property
    def authenticator(self) -> UpWorkAuthenticator:
        """Return a new authenticator object.

        Returns:
            An authenticator instance.
        """
        return UpWorkAuthenticator.create_for_stream(self)

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed.

        Returns:
            A dictionary of HTTP headers.
        """
        headers = {}
        if 'user_agent' in self.config:
            headers['User-Agent'] = self.config.get('user_agent')
        return headers

    def prepare_request_payload(
        self,
        context: dict | None,
        next_page_token: Any | None,
    ) -> dict | None:
        """Prepare the data payload for the GraphQL API request and print the
        request data.

        Args:
            context: Stream partition or context dictionary.
            next_page_token: Token, page number or any request argument to request the
                next page of data.

        Returns:
            Dictionary with the body to use for the request.

        Raises:
            ValueError: If the `query` property is not set in the request body.
        """
        request_data = super().prepare_request_payload(context, next_page_token)
        self.logger.info(f'Request payload (query and variables): {request_data}')
        return request_data

    @staticmethod
    def property_list_to_graphql_query(properties: ObjectType) -> str:
        """Convert a list of properties to a fraction GraphQL query string.

        Args:
            properties: A list of properties to convert to a GraphQL query string.

        Returns:
            A fraction of GraphQL query string extract from all properties.
        """
        query = []
        for _, prop in properties.wrapped.items():
            query.append(prop.name)
            if isinstance(prop.wrapped, (PropertiesList, ObjectType)):
                query.append(
                    f'{{ {UpWorkStream.property_list_to_graphql_query(prop.wrapped)} }}'
                )
        return ' '.join(query)
