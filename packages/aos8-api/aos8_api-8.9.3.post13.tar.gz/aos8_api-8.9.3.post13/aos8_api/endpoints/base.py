class BaseEndpoint:
    """
    Base class for all API endpoint classes.

    This class holds a reference to the shared API client used to send requests.
    All specific endpoint implementations should inherit from this base class.

    Attributes:
        _client: The API client instance used for sending HTTP requests.
    """

    def __init__(self, client):
        """
        Initialize the BaseEndpoint.

        Args:
            client: An instance of the API client that provides request methods (e.g., get, post).
        """
        self._client = client
