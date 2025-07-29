"""Unit tests for the VeniceClient base class."""

import os
import pytest
import httpx
import respx
from unittest.mock import patch

from pyvenice.client import VeniceClient, BaseResource
from pyvenice.exceptions import (
    VeniceAPIError,
    AuthenticationError,
    InvalidRequestError,
    InsufficientBalanceError,
    RateLimitError,
    ModelCapacityError,
    TimeoutError,
    InferenceError,
)


@pytest.mark.unit
class TestVeniceClient:
    """Test VeniceClient initialization and basic functionality."""

    def test_client_init_with_api_key(self):
        """Test client initialization with API key."""
        client = VeniceClient(api_key="test-key")
        assert client.api_key == "test-key"
        assert client.base_url == "https://api.venice.ai/api/v1"
        assert client.timeout == 120.0
        assert client.max_retries == 3
        assert client.enable_compression is True

    def test_client_init_from_env(self):
        """Test client initialization from environment variable."""
        with patch.dict(os.environ, {"VENICE_API_KEY": "env-key"}):
            client = VeniceClient()
            assert client.api_key == "env-key"

    def test_client_init_no_api_key(self):
        """Test client initialization fails without API key."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="API key required"):
                VeniceClient()

    def test_client_init_custom_settings(self):
        """Test client initialization with custom settings."""
        client = VeniceClient(
            api_key="test-key",
            base_url="https://custom.api.com",
            timeout=60.0,
            max_retries=5,
            enable_compression=False,
        )
        assert client.base_url == "https://custom.api.com"
        assert client.timeout == 60.0
        assert client.max_retries == 5
        assert client.enable_compression is False

    def test_get_default_headers(self):
        """Test default headers generation."""
        client = VeniceClient(api_key="test-key")
        headers = client._get_default_headers()

        assert headers["Authorization"] == "Bearer test-key"
        assert headers["Content-Type"] == "application/json"
        assert headers["User-Agent"] == "venice-python/0.1.0"
        assert headers["Accept-Encoding"] == "gzip"

    def test_get_default_headers_no_compression(self):
        """Test default headers without compression."""
        client = VeniceClient(api_key="test-key", enable_compression=False)
        headers = client._get_default_headers()

        assert "Accept-Encoding" not in headers

    @respx.mock
    def test_successful_get_request(self, respx_mock):
        """Test successful GET request."""
        respx_mock.get("https://api.venice.ai/api/v1/test").mock(
            return_value=httpx.Response(200, json={"success": True})
        )

        client = VeniceClient(api_key="test-key")
        response = client.get("/test")

        assert response == {"success": True}

    @respx.mock
    def test_successful_post_request(self, respx_mock):
        """Test successful POST request."""
        respx_mock.post("https://api.venice.ai/api/v1/test").mock(
            return_value=httpx.Response(200, json={"created": True})
        )

        client = VeniceClient(api_key="test-key")
        response = client.post("/test", {"data": "test"})

        assert response == {"created": True}

    @respx.mock
    def test_get_with_params(self, respx_mock):
        """Test GET request with query parameters."""
        respx_mock.get("https://api.venice.ai/api/v1/test").mock(
            return_value=httpx.Response(200, json={"success": True})
        )

        client = VeniceClient(api_key="test-key")
        client.get("/test", params={"limit": 10, "offset": 0})

        # Verify the request was made with correct params
        request = respx_mock.calls[0].request
        assert "limit=10" in str(request.url)
        assert "offset=0" in str(request.url)

    def test_context_manager(self):
        """Test client as context manager."""
        with VeniceClient(api_key="test-key") as client:
            assert client.api_key == "test-key"
        # Should not raise an exception when exiting

    @pytest.mark.asyncio
    async def test_async_context_manager(self):
        """Test client as async context manager."""
        async with VeniceClient(api_key="test-key") as client:
            assert client.api_key == "test-key"
        # Should not raise an exception when exiting


@pytest.mark.unit
class TestErrorHandling:
    """Test error handling for different HTTP status codes."""

    @respx.mock
    def test_400_error(self, respx_mock, mock_400_error):
        """Test 400 Bad Request error handling."""
        respx_mock.get("https://api.venice.ai/api/v1/test").mock(
            return_value=httpx.Response(400, json=mock_400_error)
        )

        client = VeniceClient(api_key="test-key")
        with pytest.raises(InvalidRequestError) as exc_info:
            client.get("/test")

        assert "Invalid request parameters" in str(exc_info.value)
        assert exc_info.value.details == mock_400_error["details"]

    @respx.mock
    def test_401_error(self, respx_mock, mock_401_error):
        """Test 401 Authentication error handling."""
        respx_mock.get("https://api.venice.ai/api/v1/test").mock(
            return_value=httpx.Response(401, json=mock_401_error)
        )

        client = VeniceClient(api_key="test-key")
        with pytest.raises(AuthenticationError) as exc_info:
            client.get("/test")

        assert "Authentication failed" in str(exc_info.value)

    @respx.mock
    def test_402_error(self, respx_mock):
        """Test 402 Payment Required error handling."""
        error_response = {"error": "Insufficient USD or VCU balance"}
        respx_mock.get("https://api.venice.ai/api/v1/test").mock(
            return_value=httpx.Response(402, json=error_response)
        )

        client = VeniceClient(api_key="test-key")
        with pytest.raises(InsufficientBalanceError):
            client.get("/test")

    @respx.mock
    def test_415_error(self, respx_mock):
        """Test 415 Unsupported Media Type error handling."""
        error_response = {"error": "Invalid request content-type"}
        respx_mock.get("https://api.venice.ai/api/v1/test").mock(
            return_value=httpx.Response(415, json=error_response)
        )

        client = VeniceClient(api_key="test-key")
        with pytest.raises(InvalidRequestError):
            client.get("/test")

    @respx.mock
    def test_429_error(self, respx_mock, mock_429_error):
        """Test 429 Rate Limit error handling."""
        respx_mock.get("https://api.venice.ai/api/v1/test").mock(
            return_value=httpx.Response(429, json=mock_429_error)
        )

        client = VeniceClient(api_key="test-key")
        with pytest.raises(RateLimitError):
            client.get("/test")

    @respx.mock
    def test_500_error(self, respx_mock):
        """Test 500 Internal Server Error handling."""
        error_response = {"error": "Inference processing failed"}
        respx_mock.get("https://api.venice.ai/api/v1/test").mock(
            return_value=httpx.Response(500, json=error_response)
        )

        client = VeniceClient(api_key="test-key")
        with pytest.raises(InferenceError):
            client.get("/test")

    @respx.mock
    def test_503_error(self, respx_mock, mock_503_error):
        """Test 503 Service Unavailable error handling."""
        respx_mock.get("https://api.venice.ai/api/v1/test").mock(
            return_value=httpx.Response(503, json=mock_503_error)
        )

        client = VeniceClient(api_key="test-key")
        with pytest.raises(ModelCapacityError):
            client.get("/test")

    @respx.mock
    def test_504_error(self, respx_mock):
        """Test 504 Gateway Timeout error handling."""
        error_response = {"error": "Request timed out"}
        respx_mock.get("https://api.venice.ai/api/v1/test").mock(
            return_value=httpx.Response(504, json=error_response)
        )

        client = VeniceClient(api_key="test-key")
        with pytest.raises(TimeoutError):
            client.get("/test")

    @respx.mock
    def test_unknown_error_code(self, respx_mock):
        """Test handling of unknown error codes."""
        error_response = {"error": "Unknown error"}
        respx_mock.get("https://api.venice.ai/api/v1/test").mock(
            return_value=httpx.Response(418, json=error_response)
        )

        client = VeniceClient(api_key="test-key")
        with pytest.raises(VeniceAPIError) as exc_info:
            client.get("/test")

        assert "API error (418)" in str(exc_info.value)

    @respx.mock
    def test_non_json_error_response(self, respx_mock):
        """Test handling of non-JSON error responses."""
        respx_mock.get("https://api.venice.ai/api/v1/test").mock(
            return_value=httpx.Response(500, text="Internal Server Error")
        )

        client = VeniceClient(api_key="test-key")
        with pytest.raises(VeniceAPIError) as exc_info:
            client.get("/test")

        assert "Internal Server Error" in str(exc_info.value)


@pytest.mark.unit
class TestRetryLogic:
    """Test retry logic for failed requests."""

    @respx.mock
    def test_retry_on_connection_error(self, respx_mock):
        """Test retry logic on connection errors."""
        # First two requests fail, third succeeds
        respx_mock.get("https://api.venice.ai/api/v1/test").mock(
            side_effect=[
                httpx.ConnectError("Connection failed"),
                httpx.ConnectError("Connection failed"),
                httpx.Response(200, json={"success": True}),
            ]
        )

        client = VeniceClient(api_key="test-key", max_retries=3)
        response = client.get("/test")

        assert response == {"success": True}
        assert len(respx_mock.calls) == 3

    @respx.mock
    def test_retry_exhausted(self, respx_mock):
        """Test behavior when all retries are exhausted."""
        respx_mock.get("https://api.venice.ai/api/v1/test").mock(
            side_effect=httpx.ConnectError("Connection failed")
        )

        client = VeniceClient(api_key="test-key", max_retries=2)
        with pytest.raises(VeniceAPIError, match="Connection error"):
            client.get("/test")

        assert len(respx_mock.calls) == 2

    @respx.mock
    def test_no_retry_on_4xx_errors(self, respx_mock):
        """Test that 4xx errors are not retried."""
        respx_mock.get("https://api.venice.ai/api/v1/test").mock(
            return_value=httpx.Response(400, json={"error": "Bad request"})
        )

        client = VeniceClient(api_key="test-key", max_retries=3)
        with pytest.raises(InvalidRequestError):
            client.get("/test")

        # Should only make one request, no retries
        assert len(respx_mock.calls) == 1


@pytest.mark.unit
class TestBaseResource:
    """Test BaseResource class functionality."""

    def test_base_resource_init(self, client):
        """Test BaseResource initialization."""
        resource = BaseResource(client)
        assert resource.client == client

    def test_validate_params(self, client):
        """Test parameter validation."""
        resource = BaseResource(client)

        params = {
            "valid_param": "value",
            "another_valid": 123,
            "invalid_param": "should_be_removed",
            "none_value": None,
        }

        allowed = {"valid_param", "another_valid", "none_value"}
        filtered = resource._validate_params(params, allowed)

        assert filtered == {"valid_param": "value", "another_valid": 123}
        assert "invalid_param" not in filtered
        assert "none_value" not in filtered  # None values excluded


@pytest.mark.unit
class TestAsyncClient:
    """Test async client functionality."""

    @pytest.mark.asyncio
    @respx.mock
    async def test_async_get_request(self, respx_mock):
        """Test async GET request."""
        respx_mock.get("https://api.venice.ai/api/v1/test").mock(
            return_value=httpx.Response(200, json={"success": True})
        )

        client = VeniceClient(api_key="test-key")
        response = await client.get_async("/test")

        assert response == {"success": True}

    @pytest.mark.asyncio
    @respx.mock
    async def test_async_post_request(self, respx_mock):
        """Test async POST request."""
        respx_mock.post("https://api.venice.ai/api/v1/test").mock(
            return_value=httpx.Response(200, json={"created": True})
        )

        client = VeniceClient(api_key="test-key")
        response = await client.post_async("/test", {"data": "test"})

        assert response == {"created": True}

    @pytest.mark.asyncio
    @respx.mock
    async def test_async_error_handling(self, respx_mock):
        """Test async error handling."""
        respx_mock.get("https://api.venice.ai/api/v1/test").mock(
            return_value=httpx.Response(401, json={"error": "Unauthorized"})
        )

        client = VeniceClient(api_key="test-key")
        with pytest.raises(AuthenticationError):
            await client.get_async("/test")
