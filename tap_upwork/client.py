"""GraphQL client handling, including UpWorkStream base class."""

from __future__ import annotations

from typing import Iterable

import requests  # noqa: TCH002
from singer_sdk.streams import GraphQLStream

from tap_upwork.auth import UpWorkAuthenticator


class UpWorkStream(GraphQLStream):
    """UpWork stream class."""

    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        return "https://api.upwork.com/graphql"

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
        if "user_agent" in self.config:
            headers["User-Agent"] = self.config.get("user_agent")
        return headers

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result records.

        Args:
            response: The HTTP ``requests.Response`` object.

        Yields:
            Each record from the source.
        """
        yield from response.json().get("data", {}).get(self.name, [])
