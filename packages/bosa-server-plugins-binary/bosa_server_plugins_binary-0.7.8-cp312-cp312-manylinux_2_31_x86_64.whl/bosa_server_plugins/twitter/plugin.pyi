from .router import TwitterApiRoutes as TwitterApiRoutes
from bosa_core import ConfigService as ConfigService
from bosa_server_plugins.common.plugin import ThirdPartyIntegrationPlugin as ThirdPartyIntegrationPlugin
from bosa_server_plugins.handler.header import ExposedDefaultHeaders as ExposedDefaultHeaders
from bosa_server_plugins.twitter.auth.auth import TwitterClient as TwitterClient

class TwitterApiPlugin(ThirdPartyIntegrationPlugin):
    """Twitter API Plugin."""
    name: str
    version: str
    description: str
    routes: TwitterApiRoutes
    config: ConfigService
    def __init__(self) -> None:
        """Initializes Twitter API plugin."""
    def initialize_authorization(self, callback_url: str, headers: ExposedDefaultHeaders):
        """Initializes the plugin authorization.

        Args:
            callback_url: The callback URL.
            headers: The headers.

        Returns:
            The authorization URL.

        Notes:
            This implementation does not support multiple users yet.
            Currently, the request is using the master key.
        """
    def success_authorize_callback(self, client_id: str, user_id: str, **kwargs):
        """Callback for successful authorization.

        Args:
            client_id: The client ID.
            user_id: The user ID.
            **kwargs: The keyword arguments.
        """
    def remove_integration(self, headers: ExposedDefaultHeaders):
        """Removes the integration.

        Args:
            headers: The headers.
        """
    def user_has_integration(self, headers: ExposedDefaultHeaders):
        """Checks if the user has an integration.

        Args:
            headers: The headers.

        Returns:
            True if the user has an integration, False otherwise.
        """
