"""Unit tests for the Embeddings module."""

import pytest
import httpx
import respx

# import numpy as np  # Removed to avoid dependency

from pyvenice.embeddings import Embeddings, EmbeddingRequest, EmbeddingResponse
from pyvenice.client import VeniceClient
from pyvenice.exceptions import InvalidRequestError


def setup_embeddings_mocks(respx_mock):
    """Helper to set up common mocks for embeddings tests."""
    # Mock compatibility mapping endpoint
    respx_mock.get("https://api.venice.ai/api/v1/models/compatibility_mapping").mock(
        return_value=httpx.Response(
            200, json={"data": {}, "object": "list", "type": "text"}
        )
    )


@pytest.mark.unit
class TestEmbeddings:
    """Test Embeddings class functionality."""

    def test_embeddings_init(self, client):
        """Test Embeddings initialization."""
        embeddings = Embeddings(client)
        assert embeddings.client == client

    @respx.mock
    def test_create_embeddings_single_string(self, respx_mock, client):
        """Test creating embeddings for a single string."""
        setup_embeddings_mocks(respx_mock)

        mock_response = {
            "object": "list",
            "data": [
                {
                    "object": "embedding",
                    "index": 0,
                    "embedding": [0.1, 0.2, 0.3, -0.1, 0.5],
                }
            ],
            "model": "text-embedding-3-large",
            "usage": {"prompt_tokens": 5, "total_tokens": 5},
        }

        respx_mock.post("https://api.venice.ai/api/v1/embeddings").mock(
            return_value=httpx.Response(200, json=mock_response)
        )

        embeddings = Embeddings(client)
        response = embeddings.create(
            input="Hello world", model="text-embedding-3-large"
        )

        assert isinstance(response, EmbeddingResponse)
        assert response.object == "list"
        assert len(response.data) == 1
        assert response.data[0].object == "embedding"
        assert response.data[0].index == 0
        assert len(response.data[0].embedding) == 5
        assert response.model == "text-embedding-3-large"
        assert response.usage["prompt_tokens"] == 5

    @respx.mock
    def test_create_embeddings_multiple_strings(self, respx_mock, client):
        """Test creating embeddings for multiple strings."""
        setup_embeddings_mocks(respx_mock)

        mock_response = {
            "object": "list",
            "data": [
                {"object": "embedding", "index": 0, "embedding": [0.1, 0.2, 0.3]},
                {"object": "embedding", "index": 1, "embedding": [0.4, 0.5, 0.6]},
            ],
            "model": "text-embedding-3-large",
            "usage": {"prompt_tokens": 8, "total_tokens": 8},
        }

        respx_mock.post("https://api.venice.ai/api/v1/embeddings").mock(
            return_value=httpx.Response(200, json=mock_response)
        )

        embeddings = Embeddings(client)
        response = embeddings.create(
            input=["Hello world", "Goodbye world"], model="text-embedding-3-large"
        )

        assert len(response.data) == 2
        assert response.data[0].index == 0
        assert response.data[1].index == 1
        assert response.usage["prompt_tokens"] == 8

    @respx.mock
    def test_create_embeddings_with_dimensions(self, respx_mock, client):
        """Test creating embeddings with specific dimensions."""
        setup_embeddings_mocks(respx_mock)

        mock_response = {
            "object": "list",
            "data": [
                {
                    "object": "embedding",
                    "index": 0,
                    "embedding": [0.1, 0.2],  # 2 dimensions
                }
            ],
            "model": "text-embedding-3-large",
            "usage": {"prompt_tokens": 3, "total_tokens": 3},
        }

        respx_mock.post("https://api.venice.ai/api/v1/embeddings").mock(
            return_value=httpx.Response(200, json=mock_response)
        )

        embeddings = Embeddings(client)
        response = embeddings.create(
            input="Test text", model="text-embedding-3-large", dimensions=2
        )

        # Verify request was made with correct parameters
        request = respx_mock.calls[-1].request  # Get the last call (embeddings call)
        import json

        request_body = json.loads(request.content)

        assert request_body["dimensions"] == 2
        assert len(response.data[0].embedding) == 2

    @respx.mock
    def test_create_embeddings_with_encoding_format(self, respx_mock, client):
        """Test creating embeddings with different encoding formats."""
        setup_embeddings_mocks(respx_mock)

        mock_response = {
            "object": "list",
            "data": [{"object": "embedding", "index": 0, "embedding": [0.1, 0.2, 0.3]}],
            "model": "text-embedding-3-large",
            "usage": {"prompt_tokens": 3, "total_tokens": 3},
        }

        respx_mock.post("https://api.venice.ai/api/v1/embeddings").mock(
            return_value=httpx.Response(200, json=mock_response)
        )

        embeddings = Embeddings(client)
        response = embeddings.create(
            input="Test text", model="text-embedding-3-large", encoding_format="base64"
        )

        # Verify request was made with correct parameters
        request = respx_mock.calls[-1].request  # Get the last call (embeddings call)
        import json

        request_body = json.loads(request.content)

        assert request_body["encoding_format"] == "base64"
        assert isinstance(response, EmbeddingResponse)

    @pytest.mark.asyncio
    @respx.mock
    async def test_create_embeddings_async(self, respx_mock, client):
        """Test async embedding creation."""
        setup_embeddings_mocks(respx_mock)

        mock_response = {
            "object": "list",
            "data": [{"object": "embedding", "index": 0, "embedding": [0.1, 0.2, 0.3]}],
            "model": "text-embedding-3-large",
            "usage": {"prompt_tokens": 3, "total_tokens": 3},
        }

        respx_mock.post("https://api.venice.ai/api/v1/embeddings").mock(
            return_value=httpx.Response(200, json=mock_response)
        )

        embeddings = Embeddings(client)
        response = await embeddings.create_async(
            input="Hello async world", model="text-embedding-3-large"
        )

        assert isinstance(response, EmbeddingResponse)
        assert len(response.data) == 1
        assert response.data[0].embedding == [0.1, 0.2, 0.3]


@pytest.mark.unit
class TestEmbeddingRequest:
    """Test EmbeddingsRequest validation."""

    def test_valid_request_single_string(self):
        """Test valid request with single string."""
        request = EmbeddingRequest(input="Hello world", model="text-embedding-3-large")

        assert request.input == "Hello world"  # Should remain as string
        assert request.model == "text-embedding-3-large"
        assert request.encoding_format == "float"  # Default
        assert request.dimensions is None

    def test_valid_request_multiple_strings(self):
        """Test valid request with multiple strings."""
        request = EmbeddingRequest(
            input=["Hello", "world"], model="text-embedding-3-large"
        )

        assert request.input == ["Hello", "world"]
        assert request.model == "text-embedding-3-large"

    def test_request_with_dimensions(self):
        """Test request with dimensions parameter."""
        request = EmbeddingRequest(
            input="Test", model="text-embedding-3-large", dimensions=512
        )

        assert request.dimensions == 512

    def test_request_with_encoding_format(self):
        """Test request with different encoding formats."""
        request = EmbeddingRequest(
            input="Test", model="text-embedding-3-large", encoding_format="base64"
        )

        assert request.encoding_format == "base64"

    def test_request_validation_empty_input(self):
        """Test validation with empty input."""

        # Empty string should be invalid
        with pytest.raises(ValueError, match="Input string cannot be empty"):
            EmbeddingRequest(input="", model="text-embedding-3-large")

        # Empty list should be invalid
        with pytest.raises(ValueError, match="Input array cannot be empty"):
            EmbeddingRequest(input=[], model="text-embedding-3-large")

    def test_request_validation_invalid_encoding(self):
        """Test validation with invalid encoding format."""
        from pydantic import ValidationError

        with pytest.raises(ValidationError):
            EmbeddingRequest(
                input="Test", model="text-embedding-3-large", encoding_format="invalid"
            )

    def test_request_validation_dimensions_bounds(self):
        """Test validation of dimensions bounds."""
        from pydantic import ValidationError

        # Valid dimensions
        request = EmbeddingRequest(
            input="Test", model="text-embedding-3-large", dimensions=1536
        )
        assert request.dimensions == 1536

        # Too small dimensions
        with pytest.raises(ValidationError):
            EmbeddingRequest(input="Test", model="text-embedding-3-large", dimensions=0)


@pytest.mark.unit
class TestEmbeddingResponse:
    """Test EmbeddingsResponse parsing."""

    def test_response_parsing(self):
        """Test parsing embeddings response."""
        response_data = {
            "object": "list",
            "data": [
                {
                    "object": "embedding",
                    "index": 0,
                    "embedding": [0.1, 0.2, 0.3, -0.1, 0.5],
                },
                {
                    "object": "embedding",
                    "index": 1,
                    "embedding": [0.4, 0.5, 0.6, -0.2, 0.8],
                },
            ],
            "model": "text-embedding-3-large",
            "usage": {"prompt_tokens": 10, "total_tokens": 10},
        }

        response = EmbeddingResponse(**response_data)

        assert response.object == "list"
        assert len(response.data) == 2
        assert response.model == "text-embedding-3-large"

        # Check first embedding
        embedding1 = response.data[0]
        assert embedding1.object == "embedding"
        assert embedding1.index == 0
        assert len(embedding1.embedding) == 5
        assert embedding1.embedding[0] == 0.1

        # Check second embedding
        embedding2 = response.data[1]
        assert embedding2.index == 1
        assert len(embedding2.embedding) == 5

        # Check usage
        assert response.usage["prompt_tokens"] == 10
        assert response.usage["total_tokens"] == 10

    def test_embedding_as_list(self):
        """Test that embedding is returned as a list."""
        response_data = {
            "object": "list",
            "data": [{"object": "embedding", "index": 0, "embedding": [0.1, 0.2, 0.3]}],
            "model": "text-embedding-3-large",
            "usage": {"prompt_tokens": 3, "total_tokens": 3},
        }

        response = EmbeddingResponse(**response_data)
        embedding_list = response.data[0].embedding

        assert isinstance(embedding_list, list)
        assert len(embedding_list) == 3
        assert embedding_list == [0.1, 0.2, 0.3]


@pytest.mark.unit
class TestErrorHandling:
    """Test error handling in embeddings."""

    @respx.mock
    def test_invalid_model_error(self, respx_mock, client):
        """Test error when using invalid model."""
        setup_embeddings_mocks(respx_mock)

        error_response = {
            "error": "Invalid model specified",
            "details": {"model": {"_errors": ["Model not found"]}},
        }
        respx_mock.post("https://api.venice.ai/api/v1/embeddings").mock(
            return_value=httpx.Response(400, json=error_response)
        )

        embeddings = Embeddings(client)
        with pytest.raises(InvalidRequestError) as exc_info:
            embeddings.create(input="Test text", model="invalid-model")

        assert "Invalid model specified" in str(exc_info.value)

    @respx.mock
    def test_empty_input_error(self, respx_mock, client):
        """Test error when input is too long or empty."""
        setup_embeddings_mocks(respx_mock)

        error_response = {
            "error": "Input validation failed",
            "details": {"input": {"_errors": ["Input cannot be empty"]}},
        }
        respx_mock.post("https://api.venice.ai/api/v1/embeddings").mock(
            return_value=httpx.Response(400, json=error_response)
        )

        embeddings = Embeddings(client)
        # The validation happens at the request level, not the API level
        # So we don't need to mock the API response for this test
        try:
            embeddings.create(input="", model="text-embedding-3-large")  # Empty input
            assert False, "Should have raised an exception"
        except ValueError as e:
            assert "Input string cannot be empty" in str(e)


@pytest.mark.unit
class TestUtilityMethods:
    """Test utility methods for embeddings."""

    def test_cosine_similarity_calculation(self):
        """Test cosine similarity calculation between embeddings."""
        import math

        # Create two embeddings as lists
        embedding1 = [1.0, 0.0, 0.0]
        embedding2 = [0.0, 1.0, 0.0]
        embedding3 = [1.0, 0.0, 0.0]  # Same as embedding1

        # Calculate cosine similarity
        def cosine_similarity(a, b):
            dot_product = sum(x * y for x, y in zip(a, b))
            norm_a = math.sqrt(sum(x * x for x in a))
            norm_b = math.sqrt(sum(x * x for x in b))
            return dot_product / (norm_a * norm_b)

        # Orthogonal vectors should have similarity 0
        sim_12 = cosine_similarity(embedding1, embedding2)
        assert abs(sim_12 - 0.0) < 1e-10

        # Identical vectors should have similarity 1
        sim_13 = cosine_similarity(embedding1, embedding3)
        assert abs(sim_13 - 1.0) < 1e-10


@pytest.mark.integration
class TestEmbeddingsIntegration:
    """Integration tests for Embeddings (requires API key)."""

    def test_real_embeddings_single_string(
        self, skip_if_no_api_key, integration_api_key
    ):
        """Test real embedding creation with single string."""
        client = VeniceClient(api_key=integration_api_key)
        embeddings = Embeddings(client)

        response = embeddings.create(
            input="This is a test sentence for embedding.",
            model="text-embedding-3-large",
        )

        assert isinstance(response, EmbeddingResponse)
        assert len(response.data) == 1
        assert len(response.data[0].embedding) > 0
        assert response.usage["prompt_tokens"] > 0
        assert response.usage["total_tokens"] > 0

    def test_real_embeddings_multiple_strings(
        self, skip_if_no_api_key, integration_api_key
    ):
        """Test real embedding creation with multiple strings."""
        client = VeniceClient(api_key=integration_api_key)
        embeddings = Embeddings(client)

        response = embeddings.create(
            input=[
                "First test sentence.",
                "Second test sentence.",
                "Third test sentence.",
            ],
            model="text-embedding-3-large",
        )

        assert len(response.data) == 3
        assert all(len(emb.embedding) > 0 for emb in response.data)

        # Check that different sentences have different embeddings
        emb1 = response.data[0].embedding
        emb2 = response.data[1].embedding

        # They shouldn't be identical
        assert emb1 != emb2

    def test_real_embeddings_with_dimensions(
        self, skip_if_no_api_key, integration_api_key
    ):
        """Test real embedding creation with specific dimensions."""
        client = VeniceClient(api_key=integration_api_key)
        embeddings = Embeddings(client)

        response = embeddings.create(
            input="Test with dimensions parameter.",
            model="text-embedding-3-large",
            dimensions=512,
        )

        # Should return embeddings with requested dimensions
        assert len(response.data[0].embedding) == 512
