import httpx
import os
from typing import Optional
from typing import Dict


class OpenAIClient:

    api_version = "v1"
    base = "https://api.openai.com/"

    def __init__(self, api_key: Optional[str] = None):
        self.base_url = f"{self.base}{self.api_version}/"
        self.set_api_key(api_key)  # Initialize the API key
        self.headers = self._get_headers()  # Get the headers for requests

    def set_api_key(self, api_key: Optional[str] = None):
        """
        Sets the API key for OpenAI API requests.
        This method can be used to update the API key dynamically.

        :param api_key: Optional API key to override the existing one.
        If not provided, it will attempt to read from the environment variable 'OPENAI_API_KEY'.
        :raises ValueError: If no API key is provided and not set in the environment variable.
        """
        if api_key:
            # override the API key if provided
            self.api_key = api_key
            self._set_env_var("OPENAI_API_KEY", api_key)
        else:
            self.api_key = os.getenv("OPENAI_API_KEY", None)
            if not self.api_key:
                raise ValueError(
                    "API key must be provided either as an argument or set in the environment variable 'OPENAI_API_KEY'."
                )

    def _set_env_var(self, key: str, value: str):
        """
        Sets an environment variable with the given key and value.
        This is useful for configuring the OpenAI API key.
        """
        if not key or not value:
            raise ValueError(
                "Both key and value must be provided to set an environment variable."
            )
        os.environ[key] = value

    def _get_headers(self) -> Dict[str, str]:
        """
        Returns the headers required for OpenAI API requests.
        The headers include the Authorization token, content type, organization ID, and project ID.

        :return: A dictionary containing the headers for the OpenAI API request.
        :raises ValueError: If the API key is not set or if the required environment variables are not set.
        :raises ValueError: If the organization or project ID is not set in the environment variables.
        """
        if not self.api_key:
            raise ValueError("API key is required for OpenAI API requests.")

        openai_api_organization = os.environ.get("OPENAI_API_ORGANIZATION", None)
        openai_api_project = os.environ.get("OPENAI_API_PROJECT", None)

        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "OpenAI-Organization": openai_api_organization,
            "OpenAI-Project": openai_api_project,
        }

    def request(
        self, method: str, endpoint: str, data: Optional[Dict] = None
    ) -> httpx.Response:
        """
        Makes a request to the OpenAI API.

        :param method: HTTP method (e.g., 'GET', 'POST').
        :param endpoint: The API endpoint to which the request is made.
        :param data: Optional dictionary containing the data to be sent in the request body.
        :return: The response from the OpenAI API.
        """
        url = f"{self.base_url}{endpoint}"
        response = httpx.request(
            method, url, headers=self.headers, data=data, timeout=30
        )
        return response
