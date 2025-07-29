"""Unit tests for the Audio module."""

import pytest
import httpx
import respx

from pyvenice.audio import Audio, SpeechRequest
from pyvenice.client import VeniceClient

# from pyvenice.exceptions import InvalidRequestError


def setup_audio_mocks(respx_mock):
    """Helper to set up common mocks for audio tests."""
    # Mock compatibility mapping endpoint
    respx_mock.get("https://api.venice.ai/api/v1/models/compatibility_mapping").mock(
        return_value=httpx.Response(
            200, json={"data": {}, "object": "list", "type": "text"}
        )
    )


@pytest.mark.unit
class TestAudio:
    """Test Audio class functionality."""

    def test_audio_init(self, client):
        """Test Audio initialization."""
        audio = Audio(client)
        assert audio.client == client

    @respx.mock
    def test_create_speech_basic(self, respx_mock, client):
        """Test basic speech creation."""
        setup_audio_mocks(respx_mock)

        # Mock binary audio response
        fake_audio_data = b"fake-audio-data-content"
        respx_mock.post("https://api.venice.ai/api/v1/audio/speech").mock(
            return_value=httpx.Response(
                200, content=fake_audio_data, headers={"content-type": "audio/mpeg"}
            )
        )

        audio = Audio(client)
        response = audio.create_speech(input="Hello, this is a test.", voice="af_alloy")

        assert response == fake_audio_data

    @respx.mock
    def test_create_speech_with_model(self, respx_mock, client):
        """Test speech creation with custom model."""
        setup_audio_mocks(respx_mock)

        fake_audio_data = b"fake-audio-data-content"
        respx_mock.post("https://api.venice.ai/api/v1/audio/speech").mock(
            return_value=httpx.Response(
                200, content=fake_audio_data, headers={"content-type": "audio/mpeg"}
            )
        )

        audio = Audio(client)
        response = audio.create_speech(
            input="Hello, this is a test.", voice="af_alloy", model="tts-kokoro"
        )

        # Verify request was made with correct parameters
        request = respx_mock.calls[-1].request
        import json

        request_body = json.loads(request.content)

        assert request_body["model"] == "tts-kokoro"
        assert request_body["voice"] == "af_alloy"
        assert request_body["input"] == "Hello, this is a test."
        assert response == fake_audio_data

    @respx.mock
    def test_create_speech_with_speed(self, respx_mock, client):
        """Test speech creation with custom speed."""
        setup_audio_mocks(respx_mock)

        fake_audio_data = b"fake-audio-data"
        respx_mock.post("https://api.venice.ai/api/v1/audio/speech").mock(
            return_value=httpx.Response(
                200, content=fake_audio_data, headers={"content-type": "audio/mpeg"}
            )
        )

        audio = Audio(client)
        response = audio.create_speech(
            input="Test with speed", voice="af_nova", speed=1.5
        )

        # Verify request was made with correct parameters
        request = respx_mock.calls[-1].request
        import json

        request_body = json.loads(request.content)

        assert request_body["speed"] == 1.5
        assert response == fake_audio_data

    @respx.mock
    def test_create_speech_with_response_format(self, respx_mock, client):
        """Test speech creation with different response format."""
        setup_audio_mocks(respx_mock)

        fake_audio_data = b"fake-audio-data"
        respx_mock.post("https://api.venice.ai/api/v1/audio/speech").mock(
            return_value=httpx.Response(
                200, content=fake_audio_data, headers={"content-type": "audio/wav"}
            )
        )

        audio = Audio(client)
        response = audio.create_speech(
            input="Test with WAV format", voice="am_echo", response_format="wav"
        )

        # Verify request was made with correct parameters
        request = respx_mock.calls[-1].request
        import json

        request_body = json.loads(request.content)

        assert request_body["response_format"] == "wav"
        assert response == fake_audio_data

    @respx.mock
    def test_create_speech_streaming(self, respx_mock, client):
        """Test streaming speech creation."""
        setup_audio_mocks(respx_mock)

        fake_audio_chunks = [b"chunk1", b"chunk2", b"chunk3"]

        def mock_streaming_response(request):
            def generate_chunks():
                for chunk in fake_audio_chunks:
                    yield chunk

            return httpx.Response(
                200,
                content=b"".join(fake_audio_chunks),
                headers={"content-type": "audio/mpeg"},
            )

        respx_mock.post("https://api.venice.ai/api/v1/audio/speech").mock(
            side_effect=mock_streaming_response
        )

        audio = Audio(client)
        stream = audio.create_speech_streaming(input="Test streaming", voice="af_alloy")

        # Collect all chunks
        collected_chunks = b""
        for chunk in stream:
            collected_chunks += chunk

        assert collected_chunks == b"".join(fake_audio_chunks)

    @pytest.mark.asyncio
    @respx.mock
    async def test_create_speech_async(self, respx_mock, client):
        """Test async speech creation."""
        setup_audio_mocks(respx_mock)

        fake_audio_data = b"fake-async-audio-data"
        respx_mock.post("https://api.venice.ai/api/v1/audio/speech").mock(
            return_value=httpx.Response(
                200, content=fake_audio_data, headers={"content-type": "audio/mpeg"}
            )
        )

        audio = Audio(client)
        response = await audio.create_speech_async(input="Async test", voice="af_sky")

        assert response == fake_audio_data

    @pytest.mark.asyncio
    @respx.mock
    async def test_create_speech_streaming_async(self, respx_mock, client):
        """Test async streaming speech creation."""
        setup_audio_mocks(respx_mock)

        fake_audio_chunks = [b"async_chunk1", b"async_chunk2"]

        def mock_streaming_response(request):
            return httpx.Response(
                200,
                content=b"".join(fake_audio_chunks),
                headers={"content-type": "audio/mpeg"},
            )

        respx_mock.post("https://api.venice.ai/api/v1/audio/speech").mock(
            side_effect=mock_streaming_response
        )

        audio = Audio(client)
        stream = await audio.create_speech_streaming_async(
            input="Async streaming test", voice="am_fable"
        )

        # Collect all chunks
        collected_chunks = b""
        async for chunk in stream:
            collected_chunks += chunk

        assert collected_chunks == b"".join(fake_audio_chunks)


@pytest.mark.unit
class TestSpeechRequest:
    """Test SpeechRequest validation."""

    def test_valid_request_basic(self):
        """Test valid basic audio request."""
        request = SpeechRequest(input="Hello world", voice="af_alloy")

        assert request.input == "Hello world"
        assert request.voice == "af_alloy"
        assert request.model == "tts-kokoro"  # Default
        assert request.response_format == "mp3"  # Default
        assert request.speed == 1.0  # Default

    def test_valid_request_with_params(self):
        """Test valid request with all parameters."""
        request = SpeechRequest(
            input="Test with all parameters",
            voice="af_nova",
            model="tts-kokoro",
            response_format="wav",
            speed=1.25,
        )

        assert request.input == "Test with all parameters"
        assert request.voice == "af_nova"
        assert request.model == "tts-kokoro"
        assert request.response_format == "wav"
        assert request.speed == 1.25

    def test_voice_validation_valid(self):
        """Test valid voice values."""
        valid_voices = [
            "af_alloy",
            "am_echo",
            "am_fable",
            "am_onyx",
            "af_nova",
            "af_sky",
        ]

        for voice in valid_voices:
            request = SpeechRequest(input="Test", voice=voice)
            assert request.voice == voice

    def test_voice_validation_invalid(self):
        """Test invalid voice values."""
        from pydantic import ValidationError

        with pytest.raises(ValidationError):
            SpeechRequest(input="Test", voice="invalid_voice")

    def test_response_format_validation_valid(self):
        """Test valid response format values."""
        valid_formats = ["mp3", "opus", "aac", "flac", "wav", "pcm"]

        for format in valid_formats:
            request = SpeechRequest(
                input="Test", voice="af_alloy", response_format=format
            )
            assert request.response_format == format

    def test_response_format_validation_invalid(self):
        """Test invalid response format values."""
        from pydantic import ValidationError

        with pytest.raises(ValidationError):
            SpeechRequest(
                input="Test", voice="af_alloy", response_format="invalid_format"
            )

    def test_speed_validation_bounds(self):
        """Test speed validation bounds."""
        from pydantic import ValidationError

        # Valid speeds
        request1 = SpeechRequest(input="Test", voice="af_alloy", speed=0.25)
        assert request1.speed == 0.25

        request2 = SpeechRequest(input="Test", voice="af_alloy", speed=4.0)
        assert request2.speed == 4.0

        # Invalid speeds (too low)
        with pytest.raises(ValidationError):
            SpeechRequest(input="Test", voice="af_alloy", speed=0.1)

        # Invalid speeds (too high)
        with pytest.raises(ValidationError):
            SpeechRequest(input="Test", voice="af_alloy", speed=5.0)

    def test_input_validation_length(self):
        """Test input text length validation."""
        from pydantic import ValidationError

        # Valid length (exactly 4096 characters)
        long_text = "a" * 4096
        request = SpeechRequest(input=long_text, voice="af_alloy")
        assert len(request.input) == 4096

        # Invalid length (too long)
        too_long_text = "a" * 4097
        with pytest.raises(ValidationError):
            SpeechRequest(input=too_long_text, voice="af_alloy")

    def test_input_validation_empty(self):
        """Test input validation with empty string."""
        from pydantic import ValidationError

        with pytest.raises(ValidationError):
            SpeechRequest(input="", voice="af_alloy")


@pytest.mark.unit
class TestErrorHandling:
    """Test error handling in audio generation."""

    @respx.mock
    def test_invalid_voice_error(self, respx_mock, client):
        """Test error when using invalid voice."""
        setup_audio_mocks(respx_mock)

        error_response = {
            "error": "Invalid voice specified",
            "details": {"voice": {"_errors": ["Voice not supported"]}},
        }
        respx_mock.post("https://api.venice.ai/api/v1/audio/speech").mock(
            return_value=httpx.Response(400, json=error_response)
        )

        audio = Audio(client)
        from pydantic import ValidationError

        with pytest.raises(ValidationError) as exc_info:
            audio.create_speech(input="Test text", voice="invalid_voice")

        assert "Invalid voice" in str(exc_info.value)

    @respx.mock
    def test_text_too_long_error(self, respx_mock, client):
        """Test error when input text is too long."""
        setup_audio_mocks(respx_mock)

        error_response = {
            "error": "Input text too long",
            "details": {"input": {"_errors": ["Text exceeds maximum length"]}},
        }
        respx_mock.post("https://api.venice.ai/api/v1/audio/speech").mock(
            return_value=httpx.Response(400, json=error_response)
        )

        audio = Audio(client)
        long_text = "a" * 5000  # Longer than 4096 limit

        # The validation should happen at the request level
        from pydantic import ValidationError

        with pytest.raises(ValidationError) as exc_info:
            audio.create_speech(input=long_text, voice="af_alloy")

        assert "4096 characters" in str(exc_info.value)


@pytest.mark.unit
class TestUtilityMethods:
    """Test utility methods for audio."""

    def test_audio_formats_mapping(self):
        """Test that different audio formats map to appropriate content types."""
        format_mapping = {
            "mp3": "audio/mpeg",
            "wav": "audio/wav",
            "flac": "audio/flac",
            "aac": "audio/aac",
            "opus": "audio/opus",
            "pcm": "audio/pcm",
        }

        for format_name, expected_content_type in format_mapping.items():
            # This is more of a documentation test - in real usage,
            # the server would return appropriate content-type headers
            assert expected_content_type.startswith("audio/")

    def test_save_audio_to_file(self):
        """Test saving audio data to a file."""
        import tempfile
        import os

        fake_audio_data = b"fake-audio-content"

        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
            temp_file.write(fake_audio_data)
            temp_file_path = temp_file.name

        try:
            # Read back the file to verify it was saved correctly
            with open(temp_file_path, "rb") as f:
                saved_data = f.read()

            assert saved_data == fake_audio_data
        finally:
            # Clean up
            os.unlink(temp_file_path)


@pytest.mark.integration
class TestAudioIntegration:
    """Integration tests for Audio (requires API key)."""

    def test_real_speech_generation(self, skip_if_no_api_key, integration_api_key):
        """Test real speech generation with API."""
        client = VeniceClient(api_key=integration_api_key)
        audio = Audio(client)

        response = audio.create_speech(
            input="Hello, this is a test of the Venice AI text-to-speech system.",
            voice="af_alloy",
        )

        # Should return bytes of audio data
        assert isinstance(response, bytes)
        assert len(response) > 0

        # Audio data should start with typical MP3 header
        # MP3 files typically start with ID3 tag or frame sync
        assert response[:3] == b"ID3" or response[0] == 0xFF

    def test_real_speech_streaming(self, skip_if_no_api_key, integration_api_key):
        """Test real streaming speech generation."""
        client = VeniceClient(api_key=integration_api_key)
        audio = Audio(client)

        stream = audio.create_speech_streaming(
            input="This is a streaming test.", voice="af_nova"
        )

        # Collect all chunks
        total_data = b""
        chunk_count = 0
        for chunk in stream:
            total_data += chunk
            chunk_count += 1

        assert len(total_data) > 0
        assert chunk_count > 0  # Should have received multiple chunks

    def test_real_speech_with_different_voices(
        self, skip_if_no_api_key, integration_api_key
    ):
        """Test speech generation with different voices."""
        client = VeniceClient(api_key=integration_api_key)
        audio = Audio(client)

        voices_to_test = ["af_alloy", "am_echo", "af_nova"]
        audio_responses = {}

        for voice in voices_to_test:
            response = audio.create_speech(
                input=f"This is {voice} speaking.", voice=voice
            )
            audio_responses[voice] = response

            assert isinstance(response, bytes)
            assert len(response) > 0

        # Different voices should produce different audio data
        # (Though this isn't guaranteed, it's likely for different voice models)
        alloy_data = audio_responses["af_alloy"]
        echo_data = audio_responses["am_echo"]

        # They shouldn't be completely identical
        assert alloy_data != echo_data

    def test_real_speech_with_different_formats(
        self, skip_if_no_api_key, integration_api_key
    ):
        """Test speech generation with different audio formats."""
        client = VeniceClient(api_key=integration_api_key)
        audio = Audio(client)

        formats_to_test = ["mp3", "wav"]

        for format_type in formats_to_test:
            response = audio.create_speech(
                input=f"Testing {format_type} format.",
                voice="af_alloy",
                response_format=format_type,
            )

            assert isinstance(response, bytes)
            assert len(response) > 0

            # Different formats should have different file headers
            if format_type == "wav":
                # WAV files start with "RIFF" header
                assert response[:4] == b"RIFF"
            elif format_type == "mp3":
                # MP3 files typically start with ID3 tag or frame sync
                assert response[:3] == b"ID3" or response[0] == 0xFF
