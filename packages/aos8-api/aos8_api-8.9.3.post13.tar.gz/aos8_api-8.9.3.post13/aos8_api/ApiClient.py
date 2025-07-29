import httpx
from aos8_api.models import ApiResult
from aos8_api.endpoints.cli import CLIEndpoint
from aos8_api.endpoints.vlan import VlanEndpoint
from aos8_api.endpoints.vpa import VlanPortAssociation
from aos8_api.endpoints.ip import IPInterfaceEndpoint
from aos8_api.endpoints.system import SystemEndpoint
from aos8_api.endpoints.interface import InterfaceEndpoint
from aos8_api.endpoints.mvrp import MvrpEndpoint
from aos8_api.endpoints.mac import MacLearningEndpoint

class AosApiClient:
    """
    API client for interacting with Alcatel-Lucent OmniSwitch AOS8 HTTP API.

    This client provides a high-level interface for authentication and making
    GET, POST, PUT, and DELETE requests to various AOS8 API endpoints.
    """

    def __init__(self, username: str, password: str, base_url: str, verify_ssl: bool = False, debug: bool = False):
        """
        Initialize the AOS API client and log in.

        Args:
            username: AOS API username.
            password: AOS API password.
            base_url: Base URL of the AOS device.
            verify_ssl: Whether to verify SSL certificates.
            debug: Enable debug logging.
        """
        self.username = username
        self.password = password
        self.base_url = base_url.rstrip('/')
        self.debug = debug
        self._client = httpx.Client(
            base_url=self.base_url,
            verify=verify_ssl,
            timeout=httpx.Timeout(10.0),
            headers={
                "Accept": "application/vnd.alcatellucentaos+json",
                "User-Agent": "AOSApiClient/1.0"
            }
        )
        self._login()

        self.cli = CLIEndpoint(self)
        self.vlan = VlanEndpoint(self)
        self.vpa = VlanPortAssociation(self)
        self.ip = IPInterfaceEndpoint(self)
        self.system = SystemEndpoint(self)
        self.interface = InterfaceEndpoint(self)
        self.mvrp = MvrpEndpoint(self)
        self.mac = MacLearningEndpoint(self)

    def _login(self):
        """
        Authenticate with the AOS API using provided credentials.

        Raises:
            Exception: If login fails or session cookie is not returned.
        """
        url = f"/auth/"
        params = {
            "username": self.username,
            "password": self.password,
        }
        response = self._client.get(url, params=params)
        if self.debug:
            print(f"🔐 Login response {response.status_code}: {response.text}")
        if response.status_code != 200:
            raise Exception("Login failed")
        if "wv_sess" not in self._client.cookies:
            raise Exception("Login succeeded but 'wv_sess' cookie not found")

    def _request(self, method: str, path: str, **kwargs) -> httpx.Response:
        """
        Send an HTTP request and handle re-authentication if necessary.

        Args:
            method: HTTP method (GET, POST, etc.)
            path: API endpoint path.
            **kwargs: Additional httpx request arguments.

        Returns:
            Response object.
        """
        if self.debug:
            print(f"➡️ {method} {path}")
            if "params" in kwargs:
                print("Params:", kwargs["params"])
            if "data" in kwargs:
                print("Form Data:", kwargs["data"])
            if "json" in kwargs:
                print("JSON:", kwargs["json"])

        response = self._client.request(method, path, **kwargs)

        if response.status_code == 401:
            print("🔁 401 Unauthorized. Re-authenticating...")
            self._login()
            response = self._client.request(method, path, **kwargs)

        if self.debug:
            print("⬅️ Response:", response.status_code, response.text)

        return self._handle_response(response)

    def _handle_response(self, response: httpx.Response) -> ApiResult:
        """
        Convert HTTP response into an ApiResult object.

        Args:
            response: httpx.Response object.

        Returns:
            Parsed ApiResult object.
        """
        try:
            result = response.json()
        except ValueError:
            return ApiResult(success=False, diag=response.status_code, error="Non-JSON response", output=response.text)

        r = result.get("result", {})
        diag = r.get("diag", 0)
        success = diag == 200

        return ApiResult(
            success=success,
            diag=diag,
            error=r.get("error"),
            output=r.get("output"),
            data=r.get("data")
        )

    def get(self, path: str, **kwargs) -> httpx.Response:
        """
        Send a GET request.

        Args:
            path: API endpoint path.
            **kwargs: Additional parameters for the request.

        Returns:
            Response object.
        """
        return self._request("GET", path, **kwargs)

    def post(self, path: str, data: dict = None, **kwargs) -> httpx.Response:
        """
        Send a POST request.

        Args:
            path: API endpoint path.
            data: Dictionary to send in the body.
            **kwargs: Additional parameters for the request.

        Returns:
            Response object.
        """
        kwargs.setdefault("data", data)
        return self._request("POST", path, **kwargs)

    def put(self, path: str, data: dict = None, **kwargs) -> httpx.Response:
        """
        Send a PUT request.

        Args:
            path: API endpoint path.
            data: Dictionary to send in the body.
            **kwargs: Additional parameters for the request.

        Returns:
            Response object.
        """
        kwargs.setdefault("data", data)
        return self._request("PUT", path, **kwargs)

    def delete(self, path: str, **kwargs) -> httpx.Response:
        """
        Send a DELETE request.

        Args:
            path: API endpoint path.
            **kwargs: Additional parameters for the request.

        Returns:
            Response object.
        """
        return self._request("DELETE", path, **kwargs)

    def close(self):
        """
        Close the underlying HTTP connection pool.
        """
        self._client.close()
