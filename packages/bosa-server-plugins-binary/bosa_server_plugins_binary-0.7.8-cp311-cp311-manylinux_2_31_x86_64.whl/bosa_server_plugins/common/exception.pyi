from bosa_core.exception import BosaException

class IntegrationExistsException(BosaException):
    """Exception raised when an integration already exists for a user and client."""
    def __init__(self, plugin_name: str) -> None:
        """Initialize the exception with the plugin name.

        Args:
            plugin_name (str): The name of the plugin that already exists.
        """

class IntegrationDoesNotExistException(BosaException):
    """Exception raised when an integration does not exist for a user and client."""
    def __init__(self, plugin_name: str) -> None:
        """Initialize the exception with the plugin name.

        Args:
            plugin_name (str): The name of the plugin that does not exist.
        """
