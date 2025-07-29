from typing import Optional
from aos8_api.ApiClient import AosApiClient

class AosApiClientBuilder:
    """
    A builder class for creating and configuring an instance of `AosApiClient`.
    """

    def __init__(self):
        """
        Initialize the builder with default configuration.
        """
        self._username: Optional[str] = None
        self._password: Optional[str] = None
        self._base_url: Optional[str] = None
        self._verify_ssl: bool = False
        self._debug: bool = False

    def setUsername(self, username: str) -> 'AosApiClientBuilder':
        """
        Set the API username.

        Args:
            username: The API username.

        Returns:
            The builder instance.
        """
        self._username = username
        return self

    def setPassword(self, password: str) -> 'AosApiClientBuilder':
        """
        Set the API password.

        Args:
            password: The API password.

        Returns:
            The builder instance.
        """
        self._password = password
        return self

    def setBaseUrl(self, base_url: str) -> 'AosApiClientBuilder':
        """
        Set the base URL for the API.

        Args:
            base_url: The base URL of the API.

        Returns:
            The builder instance.
        """
        self._base_url = base_url.rstrip('/')
        return self

    def setVerifySSL(self, verify: bool) -> 'AosApiClientBuilder':
        """
        Enable or disable SSL verification.

        Args:
            verify: Whether to verify SSL certificates.

        Returns:
            The builder instance.
        """
        self._verify_ssl = verify
        return self

    def setDebug(self, debug: bool) -> 'AosApiClientBuilder':
        """
        Enable or disable debug mode.

        Args:
            debug: Whether to enable debug logging.

        Returns:
            The builder instance.
        """
        self._debug = debug
        return self

    def build(self) -> AosApiClient:
        """
        Finalize the builder and return an instance of `AosApiClient`.

        Returns:
            A configured `AosApiClient` instance.

        Raises:
            ValueError: If any required fields are missing.
        """
        if not all([self._username, self._password, self._base_url]):
            raise ValueError("Username, password, and base URL must all be set")

        return AosApiClient(
            username=self._username,
            password=self._password,
            base_url=self._base_url,
            verify_ssl=self._verify_ssl,
            debug=self._debug
        )
