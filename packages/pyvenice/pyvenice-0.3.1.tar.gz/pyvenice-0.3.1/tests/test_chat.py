"""Unit tests for the ChatCompletion module."""

import json
import pytest
import httpx
import respx

from pyvenice.chat import (
    ChatCompletion,
    ChatCompletionRequest,
    ChatCompletionResponse,
    ChatCompletionChunk,
    VeniceParameters,
)
from pyvenice.client import VeniceClient
from pyvenice.exceptions import InvalidRequestError


def setup_chat_mocks(
    respx_mock,
    mock_models_response,
    mock_compatibility_mapping,
    mock_chat_response=None,
    mock_streaming_response=None,
):
    """Helper to set up common mocks for chat tests."""
    # Always mock models and compatibility mapping
    respx_mock.get("https://api.venice.ai/api/v1/models").mock(
        return_value=httpx.Response(200, json=mock_models_response)
    )
    respx_mock.get("https://api.venice.ai/api/v1/models/compatibility_mapping").mock(
        return_value=httpx.Response(200, json=mock_compatibility_mapping)
    )

    # Mock chat completions if provided
    if mock_chat_response:
        respx_mock.post("https://api.venice.ai/api/v1/chat/completions").mock(
            return_value=httpx.Response(200, json=mock_chat_response)
        )

    # Mock streaming response if provided
    if mock_streaming_response:
        respx_mock.post("https://api.venice.ai/api/v1/chat/completions").mock(
            return_value=httpx.Response(
                200,
                content=mock_streaming_response,
                headers={"content-type": "text/event-stream"},
            )
        )


@pytest.mark.unit
class TestChatCompletion:
    """Test ChatCompletion class functionality."""

    def test_chat_completion_init(self, client):
        """Test ChatCompletion initialization."""
        chat = ChatCompletion(client)
        assert chat.client == client
        assert hasattr(chat, "models")

    @respx.mock
    def test_create_chat_completion(
        self,
        respx_mock,
        mock_chat_response,
        mock_compatibility_mapping,
        mock_models_response,
        client,
    ):
        """Test creating a chat completion."""
        setup_chat_mocks(
            respx_mock,
            mock_models_response,
            mock_compatibility_mapping,
            mock_chat_response,
        )

        chat = ChatCompletion(client)
        response = chat.create(
            model="venice-uncensored", messages=[{"role": "user", "content": "Hello!"}]
        )

        assert isinstance(response, ChatCompletionResponse)
        assert response.id == "chatcmpl-test123"
        assert response.model == "venice-uncensored"
        assert len(response.choices) == 1
        assert (
            response.choices[0].message["content"] == "Hello! How can I help you today?"
        )

    @respx.mock
    def test_create_chat_completion_with_parameters(
        self,
        respx_mock,
        mock_chat_response,
        mock_compatibility_mapping,
        mock_models_response,
        client,
    ):
        """Test creating chat completion with additional parameters."""
        # Mock endpoints
        respx_mock.get("https://api.venice.ai/api/v1/models").mock(
            return_value=httpx.Response(200, json=mock_models_response)
        )
        respx_mock.get(
            "https://api.venice.ai/api/v1/models/compatibility_mapping"
        ).mock(return_value=httpx.Response(200, json=mock_compatibility_mapping))
        respx_mock.post("https://api.venice.ai/api/v1/chat/completions").mock(
            return_value=httpx.Response(200, json=mock_chat_response)
        )

        chat = ChatCompletion(client)
        response = chat.create(
            model="venice-uncensored",
            messages=[{"role": "user", "content": "Hello!"}],
            temperature=0.7,
            max_completion_tokens=100,
            stop=["END"],
        )

        # Verify request was made with correct parameters
        request = respx_mock.calls[-1].request
        request_body = json.loads(request.content)

        assert request_body["temperature"] == 0.7
        assert request_body["max_completion_tokens"] == 100
        assert request_body["stop"] == ["END"]
        assert isinstance(response, ChatCompletionResponse)

    @respx.mock
    def test_create_with_web_search(
        self,
        respx_mock,
        mock_chat_response,
        mock_compatibility_mapping,
        mock_models_response,
        client,
    ):
        """Test creating chat completion with web search."""
        setup_chat_mocks(
            respx_mock,
            mock_models_response,
            mock_compatibility_mapping,
            mock_chat_response,
        )

        chat = ChatCompletion(client)
        response = chat.create_with_web_search(
            model="venice-uncensored",
            messages=[{"role": "user", "content": "What's new in AI?"}],
            enable_citations=True,
            search_mode="auto",
        )

        # Verify request included Venice parameters
        request = respx_mock.calls[-1].request
        request_body = json.loads(request.content)

        venice_params = request_body.get("venice_parameters", {})
        assert venice_params["enable_web_search"] == "auto"
        assert venice_params["enable_web_citations"] is True
        assert isinstance(response, ChatCompletionResponse)

    @respx.mock
    def test_streaming_chat_completion(
        self,
        respx_mock,
        mock_streaming_response,
        mock_compatibility_mapping,
        mock_models_response,
        client,
    ):
        """Test streaming chat completion."""
        setup_chat_mocks(
            respx_mock,
            mock_models_response,
            mock_compatibility_mapping,
            mock_streaming_response=mock_streaming_response,
        )

        chat = ChatCompletion(client)
        stream = chat.create(
            model="venice-uncensored",
            messages=[{"role": "user", "content": "Write a haiku"}],
            stream=True,
        )

        chunks = list(stream)
        assert len(chunks) > 0

        # Check that we get ChatCompletionChunk objects
        for chunk in chunks:
            if hasattr(chunk, "choices") and chunk.choices:
                assert isinstance(chunk, ChatCompletionChunk)

    @pytest.mark.asyncio
    @respx.mock
    async def test_async_chat_completion(
        self,
        respx_mock,
        mock_chat_response,
        mock_compatibility_mapping,
        mock_models_response,
        client,
    ):
        """Test async chat completion."""
        setup_chat_mocks(
            respx_mock,
            mock_models_response,
            mock_compatibility_mapping,
            mock_chat_response,
        )

        chat = ChatCompletion(client)
        response = await chat.create_async(
            model="venice-uncensored", messages=[{"role": "user", "content": "Hello!"}]
        )

        assert isinstance(response, ChatCompletionResponse)
        assert response.id == "chatcmpl-test123"

    @pytest.mark.asyncio
    @respx.mock
    async def test_async_streaming_chat_completion(
        self,
        respx_mock,
        mock_streaming_response,
        mock_compatibility_mapping,
        mock_models_response,
        client,
    ):
        """Test async streaming chat completion."""
        setup_chat_mocks(
            respx_mock,
            mock_models_response,
            mock_compatibility_mapping,
            mock_streaming_response=mock_streaming_response,
        )

        chat = ChatCompletion(client)
        stream = await chat.create_async(
            model="venice-uncensored",
            messages=[{"role": "user", "content": "Write a haiku"}],
            stream=True,
        )

        chunks = []
        async for chunk in stream:
            chunks.append(chunk)

        assert len(chunks) > 0


@pytest.mark.unit
class TestChatCompletionRequest:
    """Test ChatCompletionRequest validation."""

    def test_valid_request(self):
        """Test valid chat completion request."""
        request = ChatCompletionRequest(
            model="venice-uncensored", messages=[{"role": "user", "content": "Hello"}]
        )

        assert request.model == "venice-uncensored"
        assert len(request.messages) == 1
        assert request.temperature == 0.3  # Default value
        assert request.stream is False
        assert request.parallel_tool_calls is None  # Should default to None

    def test_request_with_optional_params(self):
        """Test request with optional parameters."""
        request = ChatCompletionRequest(
            model="venice-uncensored",
            messages=[{"role": "user", "content": "Hello"}],
            temperature=0.8,
            max_completion_tokens=150,
            frequency_penalty=0.1,
            presence_penalty=-0.1,
            top_p=0.9,
            stream=True,
        )

        assert request.temperature == 0.8
        assert request.max_completion_tokens == 150
        assert request.frequency_penalty == 0.1
        assert request.presence_penalty == -0.1
        assert request.top_p == 0.9
        assert request.stream is True

    def test_request_with_venice_parameters(self):
        """Test request with Venice-specific parameters."""
        venice_params = VeniceParameters(
            enable_web_search="auto", enable_web_citations=True, character_slug="venice"
        )

        request = ChatCompletionRequest(
            model="venice-uncensored",
            messages=[{"role": "user", "content": "Hello"}],
            venice_parameters=venice_params,
        )

        assert request.venice_parameters.enable_web_search == "auto"
        assert request.venice_parameters.enable_web_citations is True
        assert request.venice_parameters.character_slug == "venice"

    def test_request_validation_temperature_bounds(self):
        """Test temperature validation."""
        from pydantic import ValidationError

        # Valid temperature
        request = ChatCompletionRequest(
            model="test",
            messages=[{"role": "user", "content": "Hello"}],
            temperature=1.5,
        )
        assert request.temperature == 1.5

        # Invalid temperature (too high)
        with pytest.raises(ValidationError):
            ChatCompletionRequest(
                model="test",
                messages=[{"role": "user", "content": "Hello"}],
                temperature=3.0,
            )

        # Invalid temperature (negative)
        with pytest.raises(ValidationError):
            ChatCompletionRequest(
                model="test",
                messages=[{"role": "user", "content": "Hello"}],
                temperature=-1.0,
            )

    def test_request_validation_penalty_bounds(self):
        """Test penalty parameter validation."""
        from pydantic import ValidationError

        # Valid penalties
        request = ChatCompletionRequest(
            model="test",
            messages=[{"role": "user", "content": "Hello"}],
            frequency_penalty=1.5,
            presence_penalty=-1.5,
        )
        assert request.frequency_penalty == 1.5
        assert request.presence_penalty == -1.5

        # Invalid frequency penalty (too high)
        with pytest.raises(ValidationError):
            ChatCompletionRequest(
                model="test",
                messages=[{"role": "user", "content": "Hello"}],
                frequency_penalty=3.0,
            )

        # Invalid presence penalty (too low)
        with pytest.raises(ValidationError):
            ChatCompletionRequest(
                model="test",
                messages=[{"role": "user", "content": "Hello"}],
                presence_penalty=-3.0,
            )

    def test_request_validation_stop_sequences(self):
        """Test stop sequences validation."""
        from pydantic import ValidationError

        # Valid stop sequences
        request1 = ChatCompletionRequest(
            model="test", messages=[{"role": "user", "content": "Hello"}], stop="END"
        )
        assert request1.stop == "END"

        request2 = ChatCompletionRequest(
            model="test",
            messages=[{"role": "user", "content": "Hello"}],
            stop=["END", "STOP", "DONE"],
        )
        assert request2.stop == ["END", "STOP", "DONE"]

        # Too many stop sequences
        with pytest.raises(ValidationError):
            ChatCompletionRequest(
                model="test",
                messages=[{"role": "user", "content": "Hello"}],
                stop=["1", "2", "3", "4", "5"],  # Max is 4
            )


@pytest.mark.unit
class TestChatCompletionResponse:
    """Test ChatCompletionResponse parsing."""

    def test_response_parsing(self, mock_chat_response):
        """Test parsing chat completion response."""
        response = ChatCompletionResponse(**mock_chat_response)

        assert response.id == "chatcmpl-test123"
        assert response.object == "chat.completion"
        assert response.model == "venice-uncensored"
        assert len(response.choices) == 1

        choice = response.choices[0]
        assert choice.index == 0
        assert choice.finish_reason == "stop"
        assert choice.message["role"] == "assistant"
        assert choice.message["content"] == "Hello! How can I help you today?"

        assert response.usage.prompt_tokens == 10
        assert response.usage.completion_tokens == 15
        assert response.usage.total_tokens == 25


@pytest.mark.unit
class TestParameterValidation:
    """Test parameter validation with model capabilities."""

    @respx.mock
    def test_parallel_tool_calls_validation(
        self, respx_mock, mock_models_response, client
    ):
        """Test that parallel_tool_calls is handled correctly based on model capabilities."""
        # Mock models endpoint
        respx_mock.get("https://api.venice.ai/api/v1/models").mock(
            return_value=httpx.Response(200, json=mock_models_response)
        )

        # Mock compatibility mapping
        respx_mock.get(
            "https://api.venice.ai/api/v1/models/compatibility_mapping"
        ).mock(return_value=httpx.Response(200, json={"data": {}}))

        # Mock successful chat response
        respx_mock.post("https://api.venice.ai/api/v1/chat/completions").mock(
            return_value=httpx.Response(
                200,
                json={
                    "id": "test",
                    "object": "chat.completion",
                    "created": 1234567890,
                    "model": "venice-uncensored",
                    "choices": [
                        {
                            "index": 0,
                            "message": {"role": "assistant", "content": "test"},
                            "finish_reason": "stop",
                            "logprobs": None,
                        }
                    ],
                    "usage": {
                        "prompt_tokens": 1,
                        "completion_tokens": 1,
                        "total_tokens": 2,
                    },
                },
            )
        )

        chat = ChatCompletion(client)

        # Test with model that doesn't support function calling (venice-uncensored)
        chat.create(
            model="venice-uncensored",
            messages=[{"role": "user", "content": "Hello"}],
            parallel_tool_calls=True,  # Should be filtered out
        )

        # Verify the request was made without parallel_tool_calls
        request = respx_mock.calls[-1].request
        request_body = json.loads(request.content)
        assert (
            "parallel_tool_calls" not in request_body
            or request_body["parallel_tool_calls"] is None
        )

    @respx.mock
    def test_function_calling_parameters(
        self, respx_mock, mock_models_response, client
    ):
        """Test that function calling parameters are handled correctly."""
        # Mock models endpoint
        respx_mock.get("https://api.venice.ai/api/v1/models").mock(
            return_value=httpx.Response(200, json=mock_models_response)
        )

        # Mock compatibility mapping
        respx_mock.get(
            "https://api.venice.ai/api/v1/models/compatibility_mapping"
        ).mock(return_value=httpx.Response(200, json={"data": {}}))

        # Mock successful chat response
        respx_mock.post("https://api.venice.ai/api/v1/chat/completions").mock(
            return_value=httpx.Response(
                200,
                json={
                    "id": "test",
                    "object": "chat.completion",
                    "created": 1234567890,
                    "model": "qwen-2.5-qwq-32b",
                    "choices": [
                        {
                            "index": 0,
                            "message": {"role": "assistant", "content": "test"},
                            "finish_reason": "stop",
                            "logprobs": None,
                        }
                    ],
                    "usage": {
                        "prompt_tokens": 1,
                        "completion_tokens": 1,
                        "total_tokens": 2,
                    },
                },
            )
        )

        chat = ChatCompletion(client)

        # Test with model that supports function calling (qwen-2.5-qwq-32b)
        tools = [{"type": "function", "function": {"name": "test_function"}}]
        chat.create(
            model="qwen-2.5-qwq-32b",
            messages=[{"role": "user", "content": "Hello"}],
            tools=tools,
            parallel_tool_calls=True,
        )

        # Verify the request included function calling parameters
        request = respx_mock.calls[-1].request
        request_body = json.loads(request.content)
        assert request_body["tools"] == tools
        assert request_body["parallel_tool_calls"] is True


@pytest.mark.unit
class TestErrorHandling:
    """Test error handling in chat completions."""

    @respx.mock
    def test_invalid_model_error(self, respx_mock, mock_models_response, client):
        """Test error when using invalid model."""
        # Mock endpoints
        respx_mock.get("https://api.venice.ai/api/v1/models").mock(
            return_value=httpx.Response(200, json=mock_models_response)
        )
        respx_mock.get(
            "https://api.venice.ai/api/v1/models/compatibility_mapping"
        ).mock(return_value=httpx.Response(200, json={"data": {}}))

        # Mock error response
        error_response = {
            "error": "Model not found",
            "details": {"model": {"_errors": ["Invalid model specified"]}},
        }
        respx_mock.post("https://api.venice.ai/api/v1/chat/completions").mock(
            return_value=httpx.Response(400, json=error_response)
        )

        chat = ChatCompletion(client)
        with pytest.raises(InvalidRequestError) as exc_info:
            chat.create(
                model="invalid-model", messages=[{"role": "user", "content": "Hello"}]
            )

        assert "Model not found" in str(exc_info.value)

    @respx.mock
    def test_malformed_streaming_response(
        self, respx_mock, mock_compatibility_mapping, mock_models_response, client
    ):
        """Test handling of malformed streaming responses."""
        # Mock endpoints
        respx_mock.get("https://api.venice.ai/api/v1/models").mock(
            return_value=httpx.Response(200, json=mock_models_response)
        )
        respx_mock.get(
            "https://api.venice.ai/api/v1/models/compatibility_mapping"
        ).mock(return_value=httpx.Response(200, json=mock_compatibility_mapping))

        # Mock malformed streaming response
        malformed_stream = "data: {invalid json}\ndata: [DONE]"
        respx_mock.post("https://api.venice.ai/api/v1/chat/completions").mock(
            return_value=httpx.Response(
                200,
                content=malformed_stream,
                headers={"content-type": "text/event-stream"},
            )
        )

        chat = ChatCompletion(client)
        stream = chat.create(
            model="venice-uncensored",
            messages=[{"role": "user", "content": "Hello"}],
            stream=True,
        )

        # Should handle malformed JSON gracefully
        chunks = list(stream)
        # Malformed chunks should be skipped, so we might get empty list
        assert isinstance(chunks, list)


@pytest.mark.integration
class TestChatIntegration:
    """Integration tests for ChatCompletion (requires API key)."""

    def test_real_chat_completion(self, skip_if_no_api_key, integration_api_key):
        """Test real chat completion with API."""
        client = VeniceClient(api_key=integration_api_key)
        chat = ChatCompletion(client)

        response = chat.create(
            model="venice-uncensored",
            messages=[{"role": "user", "content": "Say 'test' exactly once."}],
            max_completion_tokens=10,
        )

        assert isinstance(response, ChatCompletionResponse)
        assert response.id
        assert len(response.choices) > 0
        assert response.choices[0].message["content"]
        assert response.usage.total_tokens > 0

    def test_real_streaming_chat(self, skip_if_no_api_key, integration_api_key):
        """Test real streaming chat completion."""
        client = VeniceClient(api_key=integration_api_key)
        chat = ChatCompletion(client)

        stream = chat.create(
            model="venice-uncensored",
            messages=[{"role": "user", "content": "Count from 1 to 3."}],
            stream=True,
            max_completion_tokens=20,
        )

        chunks = list(stream)
        assert len(chunks) > 0

        # At least one chunk should have content
        has_content = any(
            chunk.choices and chunk.choices[0].get("delta", {}).get("content")
            for chunk in chunks
        )
        assert has_content
