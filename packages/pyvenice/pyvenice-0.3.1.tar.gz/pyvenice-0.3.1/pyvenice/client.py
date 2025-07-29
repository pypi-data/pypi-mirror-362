"""
Base client for Venice.ai API with authentication and common functionality.
"""

import os
from typing import Optional, Dict, Any, Union
from urllib.parse import urljoin
import httpx
from datetime import datetime

from .exceptions import (
    VeniceAPIError,
    AuthenticationError,
    InsufficientBalanceError,
    RateLimitError,
    ModelCapacityError,
    TimeoutError,
    InvalidRequestError,
    InferenceError,
)


class VeniceClient:
    """Base client for Venice.ai API operations."""

    DEFAULT_BASE_URL = "https://api.venice.ai/api/v1"
    DEFAULT_TIMEOUT = 120.0

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: Optional[float] = None,
        max_retries: int = 3,
        enable_compression: bool = True,
    ):
        """
        Initialize Venice.ai client.

        Args:
            api_key: API key for authentication. Defaults to VENICE_API_KEY env var.
            base_url: Base URL for API. Defaults to https://api.venice.ai/api/v1
            timeout: Request timeout in seconds. Defaults to 120.
            max_retries: Maximum number of retries for failed requests.
            enable_compression: Whether to request compressed responses.
        """
        self.api_key = api_key or os.environ.get("VENICE_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key required. Set VENICE_API_KEY env var or pass api_key parameter."
            )

        self.base_url = (base_url or self.DEFAULT_BASE_URL).rstrip("/")
        self.timeout = timeout or self.DEFAULT_TIMEOUT
        self.max_retries = max_retries
        self.enable_compression = enable_compression

        # Create HTTP client
        self._client = httpx.Client(
            timeout=httpx.Timeout(self.timeout),
            headers=self._get_default_headers(),
            follow_redirects=True,
        )

        # Create async HTTP client
        self._async_client = httpx.AsyncClient(
            timeout=httpx.Timeout(self.timeout),
            headers=self._get_default_headers(),
            follow_redirects=True,
        )

        # Cache for model capabilities
        self._model_capabilities_cache: Optional[Dict[str, Any]] = None
        self._capabilities_cache_time: Optional[datetime] = None

    def _get_default_headers(self) -> Dict[str, str]:
        """Get default headers for all requests."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": "venice-python/0.1.0",
        }

        if self.enable_compression:
            headers["Accept-Encoding"] = "gzip"

        return headers

    def _handle_error_response(self, response: httpx.Response) -> None:
        """Handle error responses from the API."""
        try:
            error_data = response.json()
            error_message = error_data.get("error", "Unknown error")
            details = error_data.get("details", {})
        except (ValueError, KeyError):
            error_message = response.text or f"HTTP {response.status_code} error"
            details = {}

        status_code = response.status_code

        if status_code == 400:
            raise InvalidRequestError(error_message, details=details)
        elif status_code == 401:
            raise AuthenticationError(error_message)
        elif status_code == 402:
            raise InsufficientBalanceError(error_message)
        elif status_code == 415:
            raise InvalidRequestError(f"Invalid content type: {error_message}")
        elif status_code == 429:
            raise RateLimitError(error_message)
        elif status_code == 500:
            raise InferenceError(error_message)
        elif status_code == 503:
            raise ModelCapacityError(error_message)
        elif status_code == 504:
            raise TimeoutError(error_message)
        else:
            raise VeniceAPIError(f"API error ({status_code}): {error_message}")

    def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        stream: bool = False,
    ) -> Union[httpx.Response, Any]:
        """Make a synchronous request to the API."""
        url = urljoin(self.base_url + "/", endpoint.lstrip("/"))

        request_headers = self._client.headers.copy()
        if headers:
            request_headers.update(headers)

        for attempt in range(self.max_retries):
            try:
                response = self._client.request(
                    method=method,
                    url=url,
                    json=data,
                    params=params,
                    headers=request_headers,
                )

                if response.status_code >= 400:
                    self._handle_error_response(response)

                if stream:
                    return response

                return response.json()

            except httpx.TimeoutException:
                if attempt == self.max_retries - 1:
                    raise TimeoutError("Request timed out")
            except (httpx.ConnectError, httpx.ReadError) as e:
                if attempt == self.max_retries - 1:
                    raise VeniceAPIError(f"Connection error: {str(e)}")

    async def _request_async(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        stream: bool = False,
    ) -> Union[httpx.Response, Any]:
        """Make an asynchronous request to the API."""
        url = urljoin(self.base_url + "/", endpoint.lstrip("/"))

        request_headers = self._async_client.headers.copy()
        if headers:
            request_headers.update(headers)

        for attempt in range(self.max_retries):
            try:
                response = await self._async_client.request(
                    method=method,
                    url=url,
                    json=data,
                    params=params,
                    headers=request_headers,
                )

                if response.status_code >= 400:
                    self._handle_error_response(response)

                if stream:
                    return response

                return response.json()

            except httpx.TimeoutException:
                if attempt == self.max_retries - 1:
                    raise TimeoutError("Request timed out")
            except (httpx.ConnectError, httpx.ReadError) as e:
                if attempt == self.max_retries - 1:
                    raise VeniceAPIError(f"Connection error: {str(e)}")

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """Make a GET request."""
        return self._request("GET", endpoint, params=params)

    def post(self, endpoint: str, data: Dict[str, Any], stream: bool = False) -> Any:
        """Make a POST request."""
        return self._request("POST", endpoint, data=data, stream=stream)

    async def get_async(
        self, endpoint: str, params: Optional[Dict[str, Any]] = None
    ) -> Any:
        """Make an async GET request."""
        return await self._request_async("GET", endpoint, params=params)

    async def post_async(
        self, endpoint: str, data: Dict[str, Any], stream: bool = False
    ) -> Any:
        """Make an async POST request."""
        return await self._request_async("POST", endpoint, data=data, stream=stream)

    def close(self) -> None:
        """Close the HTTP clients."""
        self._client.close()

    async def close_async(self) -> None:
        """Close the async HTTP client."""
        await self._async_client.aclose()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()

    async def __aenter__(self):
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close_async()


class BaseResource:
    """Base class for API resources."""

    def __init__(self, client: VeniceClient):
        """Initialize resource with client."""
        self.client = client

    def _validate_params(
        self, params: Dict[str, Any], allowed_params: set
    ) -> Dict[str, Any]:
        """Validate and filter parameters."""
        filtered = {}
        for key, value in params.items():
            if key in allowed_params and value is not None:
                filtered[key] = value
        return filtered
