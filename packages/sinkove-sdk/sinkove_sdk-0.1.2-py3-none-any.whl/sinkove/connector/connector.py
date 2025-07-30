import os
import requests


class Connector:
    """
    A class to handle connections and requests to the Sinkove API.

    Attributes:
        api_key (str): The API key for authentication.
        base_url (str): The base URL for the Sinkove API.
    """

    def __init__(self, api_key: str | None = None):
        """
        Initializes a new Connector instance.

        Args:
            api_key (str | None): The API key for authentication, optional. Can be set through SINKOVE_API_KEY environment variable.

        Raises:
            ValueError: If no API key is provided or set in the environment variable.
        """
        self.api_key = api_key or os.getenv("SINKOVE_API_KEY")
        if not self.api_key:
            raise ValueError(
                "An API key is required. Provide it as a parameter or set it in the 'SINKOVE_API_KEY' environment variable."
            )
        self.base_url = os.getenv("SINKOVE_API_URL", "https://api.sinkove.com")

    def make_request(
        self, endpoint: str, method: str = "GET", params: dict = {}, data: dict = {}
    ):
        """
        Simulate a request to the Sinkove API endpoint.

        Parameters:
        - endpoint: The API endpoint to send the request to.
        - method: HTTP method (GET, POST, etc.).
        - params: URL query parameters.
        - data: Request payload for POST requests.

        Returns:
        - Simulated response data (here as a dictionary).
        """
        response = self._make_http_request(endpoint, method, params, data)
        return response.json()

    def _make_http_request(self, endpoint: str, method: str, params: dict, data: dict):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"

        # Execute HTTP request
        response = requests.request(
            method, url, headers=headers, params=params, json=data
        )

        # Check status code for 500 error
        if response.status_code == 500:
            request_id = response.headers.get("X-Request-ID", "Unavailable")
            raise Exception(
                f"Internal server error. Request ID for troubleshooting: {request_id}"
            )
        if response.status_code not in [200, 201]:
            raise Exception(str(response.json()))

        return response
