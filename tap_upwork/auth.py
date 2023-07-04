"""UpWork Authentication."""

from __future__ import annotations

from singer_sdk.authenticators import OAuthAuthenticator, SingletonMeta


class UpWorkAuthenticator(OAuthAuthenticator, metaclass=SingletonMeta):
    """Authenticator class for UpWork."""

    @property
    def oauth_request_body(self) -> dict:
        """Define the OAuth request body for the AutomaticTestTap API.

        Returns:
            A dict with the request body
        """
        return {
            'grant_type': 'client_credentials',
            'scope': self.oauth_scopes,
            'client_id': self.config['client_id'],
            'client_secret': self.config['client_secret'],
        }

    @classmethod
    def create_for_stream(cls, stream) -> UpWorkAuthenticator:
        """Instantiate an authenticator for a specific Singer stream.

        Args:
            stream: The Singer stream instance.

        Returns:
            A new UpWorkAuthenticator.
        """
        return cls(
            stream=stream,
            auth_endpoint='https://www.upwork.com/api/v3/oauth2/token',
        )
