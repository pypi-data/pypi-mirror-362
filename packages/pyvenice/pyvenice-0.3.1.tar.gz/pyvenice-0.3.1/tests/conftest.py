"""Test configuration and shared fixtures."""

import os
import pytest
import respx

from pyvenice import VeniceClient


@pytest.fixture
def mock_api_key():
    """Mock API key for testing."""
    return "test-api-key-12345"


@pytest.fixture
def client(mock_api_key):
    """Create a test client."""
    return VeniceClient(api_key=mock_api_key, enable_compression=False)


@pytest.fixture
def mock_models_response():
    """Mock response for /models endpoint."""
    return {
        "data": [
            {
                "created": 1742262554,
                "id": "venice-uncensored",
                "model_spec": {
                    "availableContextTokens": 32768,
                    "beta": False,
                    "capabilities": {
                        "optimizedForCode": False,
                        "quantization": "fp16",
                        "supportsFunctionCalling": False,
                        "supportsReasoning": True,
                        "supportsResponseSchema": False,
                        "supportsVision": False,
                        "supportsWebSearch": True,
                        "supportsLogProbs": False,
                    },
                    "description": "Venice's uncensored model",
                    "humanName": "Venice Uncensored",
                },
                "object": "model",
                "owned_by": "venice",
            },
            {
                "created": 1742262554,
                "id": "qwen-2.5-qwq-32b",
                "model_spec": {
                    "availableContextTokens": 32768,
                    "beta": False,
                    "capabilities": {
                        "optimizedForCode": True,
                        "quantization": "fp8",
                        "supportsFunctionCalling": True,
                        "supportsReasoning": True,
                        "supportsResponseSchema": True,
                        "supportsVision": False,
                        "supportsWebSearch": False,
                        "supportsLogProbs": True,
                    },
                    "description": "Qwen reasoning model",
                    "humanName": "Qwen QwQ 32B",
                },
                "object": "model",
                "owned_by": "qwen",
            },
        ],
        "object": "list",
        "type": "text",
    }


@pytest.fixture
def mock_chat_response():
    """Mock response for /chat/completions endpoint."""
    return {
        "id": "chatcmpl-test123",
        "object": "chat.completion",
        "created": 1742262554,
        "model": "venice-uncensored",
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": "Hello! How can I help you today?",
                },
                "finish_reason": "stop",
                "logprobs": None,
            }
        ],
        "usage": {"prompt_tokens": 10, "completion_tokens": 15, "total_tokens": 25},
    }


@pytest.fixture
def mock_image_response():
    """Mock response for /image/generate endpoint."""
    return {
        "id": "generate-image-test123",
        "images": [
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChAGA0"
        ],
        "timing": {
            "inferenceDuration": 2500,
            "inferencePreprocessingTime": 100,
            "inferenceQueueTime": 50,
            "total": 2650,
        },
    }


@pytest.fixture
def mock_compatibility_mapping():
    """Mock response for /models/compatibility_mapping endpoint."""
    return {
        "data": {
            "gpt-4o": "venice-uncensored",
            "gpt-3.5-turbo": "qwen-2.5-qwq-32b",
            "claude-3-5-sonnet": "venice-uncensored",
        },
        "object": "list",
        "type": "text",
    }


@pytest.fixture
def mock_embedding_response():
    """Mock response for /embeddings endpoint."""
    return {
        "data": [
            {
                "object": "embedding",
                "embedding": [0.1, 0.2, 0.3, -0.1, -0.2],
                "index": 0,
            }
        ],
        "model": "text-embedding-3-small",
        "object": "list",
        "usage": {"prompt_tokens": 5, "total_tokens": 5},
    }


@pytest.fixture
def mock_characters_response():
    """Mock response for /characters endpoint."""
    return {
        "data": [
            {
                "adult": False,
                "createdAt": "2024-12-20T21:28:08.934Z",
                "description": "A helpful AI assistant",
                "emoji": "🤖",
                "hidden": False,
                "humanName": "Venice Assistant",
                "id": "venice-assistant-123",
                "slug": "venice",
                "tags": ["helpful", "assistant"],
                "updatedAt": "2024-12-20T21:28:08.934Z",
            }
        ],
        "object": "list",
    }


@pytest.fixture
def mock_billing_response():
    """Mock response for /billing/usage endpoint."""
    return {
        "data": [
            {
                "timestamp": "2024-12-20T21:28:08.934Z",
                "sku": "venice-uncensored-llm-output-mtoken",
                "pricePerUnitUsd": 2.0,
                "units": 0.000015,
                "amount": 0.001,
                "currency": "USD",
                "notes": "API Inference",
                "inferenceDetails": {
                    "requestId": "test-inference-123",
                    "inferenceExecutionTime": 1500,
                    "promptTokens": 10,
                    "completionTokens": 15,
                },
            }
        ],
        "pagination": {"page": 1, "limit": 200, "total": 1, "total_pages": 1},
    }


@pytest.fixture
def respx_mock():
    """Create a respx mock for HTTP requests."""
    with respx.mock() as mock:
        yield mock


@pytest.fixture
def integration_api_key():
    """Get real API key for integration tests."""
    return os.environ.get("VENICE_API_KEY")


@pytest.fixture
def integration_admin_key():
    """Get real admin API key for integration tests."""
    return os.environ.get("VENICE_ADMIN_KEY")


@pytest.fixture
def skip_if_no_api_key(integration_api_key):
    """Skip test if no real API key is available."""
    if not integration_api_key:
        pytest.skip("No VENICE_API_KEY environment variable set")


@pytest.fixture
def skip_if_no_admin_key(integration_admin_key):
    """Skip test if no real admin API key is available."""
    if not integration_admin_key:
        pytest.skip("No VENICE_ADMIN_KEY environment variable set")


# Error response fixtures
@pytest.fixture
def mock_400_error():
    """Mock 400 error response."""
    return {
        "error": "Invalid request parameters",
        "details": {"_errors": [], "model": {"_errors": ["Model is required"]}},
    }


@pytest.fixture
def mock_401_error():
    """Mock 401 error response."""
    return {"error": "Authentication failed"}


@pytest.fixture
def mock_429_error():
    """Mock 429 error response."""
    return {"error": "Rate limit exceeded"}


@pytest.fixture
def mock_503_error():
    """Mock 503 error response."""
    return {"error": "The model is at capacity. Please try again later."}


# Streaming response fixtures
@pytest.fixture
def mock_streaming_response():
    """Mock streaming chat response."""
    chunks = [
        'data: {"id":"chatcmpl-test","object":"chat.completion.chunk","created":1742262554,"model":"venice-uncensored","choices":[{"index":0,"delta":{"role":"assistant","content":"Hello"}}]}',
        'data: {"id":"chatcmpl-test","object":"chat.completion.chunk","created":1742262554,"model":"venice-uncensored","choices":[{"index":0,"delta":{"content":" there"}}]}',
        'data: {"id":"chatcmpl-test","object":"chat.completion.chunk","created":1742262554,"model":"venice-uncensored","choices":[{"index":0,"delta":{"content":"!"}}]}',
        'data: {"id":"chatcmpl-test","object":"chat.completion.chunk","created":1742262554,"model":"venice-uncensored","choices":[{"index":0,"finish_reason":"stop"}]}',
        "data: [DONE]",
    ]
    return "\n".join(chunks)
