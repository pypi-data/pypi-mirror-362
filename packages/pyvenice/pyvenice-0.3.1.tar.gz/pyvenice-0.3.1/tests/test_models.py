"""Unit tests for the Models module."""

import pytest
import httpx
import respx
from freezegun import freeze_time

from pyvenice.models import Models, ModelListResponse
from pyvenice.client import VeniceClient


@pytest.mark.unit
class TestModels:
    """Test Models class functionality."""

    def test_models_init(self, client):
        """Test Models initialization."""
        models = Models(client)
        assert models.client == client
        assert models._models_cache is None
        assert models._models_cache_time is None

    @respx.mock
    def test_list_models(self, respx_mock, mock_models_response, client):
        """Test listing models."""
        respx_mock.get("https://api.venice.ai/api/v1/models").mock(
            return_value=httpx.Response(200, json=mock_models_response)
        )

        models = Models(client)
        response = models.list()

        assert isinstance(response, ModelListResponse)
        assert len(response.data) == 2
        assert response.data[0].id == "venice-uncensored"
        assert response.data[1].id == "qwen-2.5-qwq-32b"

    @respx.mock
    def test_list_models_with_type_filter(
        self, respx_mock, mock_models_response, client
    ):
        """Test listing models with type filter."""
        respx_mock.get("https://api.venice.ai/api/v1/models").mock(
            return_value=httpx.Response(200, json=mock_models_response)
        )

        models = Models(client)
        response = models.list(type="text")

        # Verify the request was made with type parameter
        request = respx_mock.calls[0].request
        assert "type=text" in str(request.url)
        assert isinstance(response, ModelListResponse)

    @respx.mock
    def test_list_models_caching(self, respx_mock, mock_models_response, client):
        """Test that model listings are cached."""
        respx_mock.get("https://api.venice.ai/api/v1/models").mock(
            return_value=httpx.Response(200, json=mock_models_response)
        )

        models = Models(client)

        # First call
        response1 = models.list()
        assert len(respx_mock.calls) == 1

        # Second call should use cache
        response2 = models.list()
        assert len(respx_mock.calls) == 1  # No additional request
        assert response1.data[0].id == response2.data[0].id

    @respx.mock
    def test_list_models_force_refresh(self, respx_mock, mock_models_response, client):
        """Test force refresh bypasses cache."""
        respx_mock.get("https://api.venice.ai/api/v1/models").mock(
            return_value=httpx.Response(200, json=mock_models_response)
        )

        models = Models(client)

        # First call
        models.list()
        assert len(respx_mock.calls) == 1

        # Force refresh should make new request
        models.list(force_refresh=True)
        assert len(respx_mock.calls) == 2

    @respx.mock
    def test_list_models_cache_expiry(self, respx_mock, mock_models_response, client):
        """Test that cache expires after 24 hours."""
        respx_mock.get("https://api.venice.ai/api/v1/models").mock(
            return_value=httpx.Response(200, json=mock_models_response)
        )

        models = Models(client)

        with freeze_time("2024-01-01 12:00:00"):
            # First call
            models.list()
            assert len(respx_mock.calls) == 1

        # 23 hours later - should still use cache
        with freeze_time("2024-01-02 11:00:00"):
            models.list()
            assert len(respx_mock.calls) == 1

        # 25 hours later - cache expired, should make new request
        with freeze_time("2024-01-02 13:00:00"):
            models.list()
            assert len(respx_mock.calls) == 2

    @pytest.mark.asyncio
    @respx.mock
    async def test_list_models_async(self, respx_mock, mock_models_response, client):
        """Test async model listing."""
        respx_mock.get("https://api.venice.ai/api/v1/models").mock(
            return_value=httpx.Response(200, json=mock_models_response)
        )

        models = Models(client)
        response = await models.list_async()

        assert isinstance(response, ModelListResponse)
        assert len(response.data) == 2

    @respx.mock
    def test_get_model(self, respx_mock, mock_models_response, client):
        """Test getting a specific model by ID."""
        respx_mock.get("https://api.venice.ai/api/v1/models").mock(
            return_value=httpx.Response(200, json=mock_models_response)
        )

        models = Models(client)
        model = models.get_model("venice-uncensored")

        assert model is not None
        assert model.id == "venice-uncensored"
        assert model.model_spec.capabilities.supportsWebSearch is True

    @respx.mock
    def test_get_model_not_found(self, respx_mock, mock_models_response, client):
        """Test getting a non-existent model."""
        respx_mock.get("https://api.venice.ai/api/v1/models").mock(
            return_value=httpx.Response(200, json=mock_models_response)
        )

        models = Models(client)
        model = models.get_model("non-existent-model")

        assert model is None

    @respx.mock
    def test_get_capabilities(self, respx_mock, mock_models_response, client):
        """Test getting model capabilities."""
        respx_mock.get("https://api.venice.ai/api/v1/models").mock(
            return_value=httpx.Response(200, json=mock_models_response)
        )

        models = Models(client)
        capabilities = models.get_capabilities("qwen-2.5-qwq-32b")

        assert capabilities is not None
        assert capabilities.supportsFunctionCalling is True
        assert capabilities.supportsResponseSchema is True
        assert capabilities.supportsLogProbs is True

    @respx.mock
    def test_get_capabilities_no_model(self, respx_mock, mock_models_response, client):
        """Test getting capabilities for non-existent model."""
        respx_mock.get("https://api.venice.ai/api/v1/models").mock(
            return_value=httpx.Response(200, json=mock_models_response)
        )

        models = Models(client)
        capabilities = models.get_capabilities("non-existent-model")

        assert capabilities is None

    @respx.mock
    def test_supports_parameter(self, respx_mock, mock_models_response, client):
        """Test checking if model supports specific parameters."""
        respx_mock.get("https://api.venice.ai/api/v1/models").mock(
            return_value=httpx.Response(200, json=mock_models_response)
        )

        models = Models(client)

        # qwen model supports function calling
        assert (
            models.supports_parameter("qwen-2.5-qwq-32b", "parallel_tool_calls") is True
        )
        assert models.supports_parameter("qwen-2.5-qwq-32b", "tools") is True
        assert models.supports_parameter("qwen-2.5-qwq-32b", "logprobs") is True

        # venice-uncensored doesn't support function calling
        assert (
            models.supports_parameter("venice-uncensored", "parallel_tool_calls")
            is False
        )
        assert models.supports_parameter("venice-uncensored", "tools") is False
        assert models.supports_parameter("venice-uncensored", "logprobs") is False

        # But it does support web search
        assert models.supports_parameter("venice-uncensored", "web_search") is True

    @respx.mock
    def test_supports_parameter_unknown_param(
        self, respx_mock, mock_models_response, client
    ):
        """Test checking support for unknown parameters."""
        respx_mock.get("https://api.venice.ai/api/v1/models").mock(
            return_value=httpx.Response(200, json=mock_models_response)
        )

        models = Models(client)

        # Unknown parameters should default to True
        assert models.supports_parameter("venice-uncensored", "unknown_param") is True

    @respx.mock
    def test_supports_parameter_no_model(
        self, respx_mock, mock_models_response, client
    ):
        """Test checking parameter support for non-existent model."""
        respx_mock.get("https://api.venice.ai/api/v1/models").mock(
            return_value=httpx.Response(200, json=mock_models_response)
        )

        models = Models(client)

        # Non-existent model should return False
        assert models.supports_parameter("non-existent", "parallel_tool_calls") is False


@pytest.mark.unit
class TestModelTraits:
    """Test model traits functionality."""

    @respx.mock
    def test_get_traits(self, respx_mock, client):
        """Test getting model traits."""
        traits_response = {
            "model_types": ["text", "image", "embedding"],
            "model_tags": ["reasoning", "function-calling", "vision"],
        }
        respx_mock.get("https://api.venice.ai/api/v1/models/traits").mock(
            return_value=httpx.Response(200, json=traits_response)
        )

        models = Models(client)
        traits = models.get_traits()

        assert traits.model_types == ["text", "image", "embedding"]
        assert traits.model_tags == ["reasoning", "function-calling", "vision"]

    @respx.mock
    def test_get_traits_caching(self, respx_mock, client):
        """Test that traits are cached."""
        traits_response = {"model_types": ["text"], "model_tags": ["test"]}
        respx_mock.get("https://api.venice.ai/api/v1/models/traits").mock(
            return_value=httpx.Response(200, json=traits_response)
        )

        models = Models(client)

        # First call
        traits1 = models.get_traits()
        assert len(respx_mock.calls) == 1

        # Second call should use cache
        traits2 = models.get_traits()
        assert len(respx_mock.calls) == 1
        assert traits1.model_types == traits2.model_types


@pytest.mark.unit
class TestCompatibilityMapping:
    """Test model compatibility mapping functionality."""

    @respx.mock
    def test_get_compatibility_mapping(
        self, respx_mock, mock_compatibility_mapping, client
    ):
        """Test getting compatibility mapping."""
        respx_mock.get(
            "https://api.venice.ai/api/v1/models/compatibility_mapping"
        ).mock(return_value=httpx.Response(200, json=mock_compatibility_mapping))

        models = Models(client)
        mapping = models.get_compatibility_mapping()

        assert mapping["gpt-4o"] == "venice-uncensored"
        assert mapping["gpt-3.5-turbo"] == "qwen-2.5-qwq-32b"
        assert mapping["claude-3-5-sonnet"] == "venice-uncensored"

    @respx.mock
    def test_map_model_name(self, respx_mock, mock_compatibility_mapping, client):
        """Test mapping model names."""
        respx_mock.get(
            "https://api.venice.ai/api/v1/models/compatibility_mapping"
        ).mock(return_value=httpx.Response(200, json=mock_compatibility_mapping))

        models = Models(client)

        # Known mappings
        assert models.map_model_name("gpt-4o") == "venice-uncensored"
        assert models.map_model_name("gpt-3.5-turbo") == "qwen-2.5-qwq-32b"

        # Unknown model should return original name
        assert models.map_model_name("unknown-model") == "unknown-model"

    @respx.mock
    def test_compatibility_mapping_caching(
        self, respx_mock, mock_compatibility_mapping, client
    ):
        """Test that compatibility mapping is cached."""
        respx_mock.get(
            "https://api.venice.ai/api/v1/models/compatibility_mapping"
        ).mock(return_value=httpx.Response(200, json=mock_compatibility_mapping))

        models = Models(client)

        # First call
        mapping1 = models.get_compatibility_mapping()
        assert len(respx_mock.calls) == 1

        # Second call should use cache
        mapping2 = models.get_compatibility_mapping()
        assert len(respx_mock.calls) == 1
        assert mapping1 == mapping2


@pytest.mark.unit
class TestModelDataClasses:
    """Test model data classes and validation."""

    def test_model_capabilities_validation(self):
        """Test ModelCapabilities validation."""
        from pyvenice.models import ModelCapabilities

        capabilities = ModelCapabilities(
            optimizedForCode=True,
            quantization="fp8",
            supportsFunctionCalling=True,
            supportsReasoning=False,
            supportsResponseSchema=True,
            supportsVision=False,
            supportsWebSearch=False,
            supportsLogProbs=True,
        )

        assert capabilities.optimizedForCode is True
        assert capabilities.quantization == "fp8"
        assert capabilities.supportsFunctionCalling is True

    def test_model_capabilities_invalid_quantization(self):
        """Test ModelCapabilities with invalid quantization."""
        from pyvenice.models import ModelCapabilities
        from pydantic import ValidationError

        with pytest.raises(ValidationError):
            ModelCapabilities(
                optimizedForCode=True,
                quantization="invalid",  # Should be fp8, fp16, or not-available
                supportsFunctionCalling=True,
                supportsReasoning=False,
                supportsResponseSchema=True,
                supportsVision=False,
                supportsWebSearch=False,
                supportsLogProbs=True,
            )

    def test_model_list_response_validation(self, mock_models_response):
        """Test ModelListResponse validation."""
        response = ModelListResponse(**mock_models_response)

        assert len(response.data) == 2
        assert response.object == "list"
        assert response.type == "text"

        # Check individual model
        model = response.data[0]
        assert model.id == "venice-uncensored"
        assert model.object == "model"
        assert model.owned_by == "venice"


@pytest.mark.integration
class TestModelsIntegration:
    """Integration tests for Models (requires API key)."""

    def test_real_models_list(self, skip_if_no_api_key, integration_api_key):
        """Test listing real models from API."""
        client = VeniceClient(api_key=integration_api_key)
        models = Models(client)

        response = models.list()

        assert isinstance(response, ModelListResponse)
        assert len(response.data) > 0
        assert response.object == "list"

        # Check first model has required fields
        model = response.data[0]
        assert model.id
        assert model.object == "model"
        assert model.model_spec

    def test_real_model_capabilities(self, skip_if_no_api_key, integration_api_key):
        """Test getting real model capabilities."""
        client = VeniceClient(api_key=integration_api_key)
        models = Models(client)

        # Get first available model
        model_list = models.list()
        first_model = model_list.data[0]

        capabilities = models.get_capabilities(first_model.id)

        if capabilities:  # Some models might not have capabilities
            assert hasattr(capabilities, "supportsFunctionCalling")
            assert hasattr(capabilities, "supportsWebSearch")
