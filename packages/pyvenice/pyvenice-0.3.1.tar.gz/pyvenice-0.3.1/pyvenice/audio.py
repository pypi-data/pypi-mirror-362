"""
Audio/Speech endpoints wrapper for Venice.ai API.
"""

from typing import Optional, Literal, Union, Generator, AsyncGenerator
from pathlib import Path
from pydantic import BaseModel, Field, field_validator

from .client import BaseResource, VeniceClient
from .models import Models


# Voice options
FEMALE_VOICES = [
    "af_alloy",
    "af_aoede",
    "af_bella",
    "af_heart",
    "af_jadzia",
    "af_jessica",
    "af_kore",
    "af_nicole",
    "af_nova",
    "af_river",
    "af_sarah",
    "af_sky",
]

MALE_VOICES = [
    "am_adam",
    "am_echo",
    "am_fable",
    "am_marcus",
    "am_michael",
    "am_onyx",
    "am_orion",
    "am_wade",
]

ALL_VOICES = FEMALE_VOICES + MALE_VOICES


class SpeechRequest(BaseModel):
    """Request model for text-to-speech."""

    input: str = Field(..., min_length=1, max_length=4096)
    model: Literal["tts-kokoro"] = "tts-kokoro"
    voice: str = Field(..., description="Voice to use for speech")
    response_format: Literal["mp3", "opus", "aac", "flac", "wav", "pcm"] = "mp3"
    speed: float = Field(1.0, ge=0.25, le=4.0)
    streaming: bool = False

    @field_validator("voice")
    @classmethod
    def validate_voice(cls, v):
        if v not in ALL_VOICES:
            raise ValueError(f"Invalid voice. Must be one of: {', '.join(ALL_VOICES)}")
        return v


class Audio(BaseResource):
    """
    Interface for Venice.ai audio/speech endpoints.

    Provides text-to-speech functionality with multiple voices and formats.
    """

    def __init__(self, client: VeniceClient):
        super().__init__(client)
        self.models = Models(client)

    def create_speech(
        self,
        input: str,
        voice: str = "af_nova",
        *,
        model: Literal["tts-kokoro"] = "tts-kokoro",
        response_format: Literal["mp3", "opus", "aac", "flac", "wav", "pcm"] = "mp3",
        speed: float = 1.0,
        streaming: bool = False,
    ) -> Union[bytes, Generator[bytes, None, None]]:
        """
        Convert text to speech.

        Args:
            input: The text to convert to speech (max 4096 characters).
            voice: Voice to use (see FEMALE_VOICES and MALE_VOICES).
            model: TTS model to use.
            response_format: Audio format for the output.
            speed: Speech speed (0.25 to 4.0, default 1.0).
            streaming: Stream audio sentence by sentence.

        Returns:
            Audio data as bytes, or generator if streaming.
        """
        request = SpeechRequest(
            input=input,
            model=model,
            voice=voice,
            response_format=response_format,
            speed=speed,
            streaming=streaming,
        )

        headers = {"Accept": self._get_audio_content_type(response_format)}

        if streaming:
            return self._stream_speech(request.model_dump(), headers)
        else:
            response = self.client._request(
                "POST",
                "/audio/speech",
                data=request.model_dump(),
                headers=headers,
                stream=True,
            )
            return response.content

    def create_speech_streaming(
        self,
        input: str,
        voice: str = "af_nova",
        *,
        model: Literal["tts-kokoro"] = "tts-kokoro",
        response_format: Literal["mp3", "opus", "aac", "flac", "wav", "pcm"] = "mp3",
        speed: float = 1.0,
    ) -> Generator[bytes, None, None]:
        """Convenience method for streaming speech creation."""
        return self.create_speech(
            input=input,
            voice=voice,
            model=model,
            response_format=response_format,
            speed=speed,
            streaming=True,
        )

    def _get_audio_content_type(self, format: str) -> str:
        """Get the appropriate content type for audio format."""
        content_types = {
            "mp3": "audio/mpeg",
            "opus": "audio/opus",
            "aac": "audio/aac",
            "flac": "audio/flac",
            "wav": "audio/wav",
            "pcm": "audio/pcm",
        }
        return content_types.get(format, "audio/mpeg")

    def _stream_speech(
        self, payload: dict, headers: dict
    ) -> Generator[bytes, None, None]:
        """Handle streaming speech response."""
        response = self.client._request(
            "POST", "/audio/speech", data=payload, headers=headers, stream=True
        )

        for chunk in response.iter_bytes(chunk_size=4096):
            if chunk:
                yield chunk

    async def create_speech_async(
        self,
        input: str,
        voice: str = "af_nova",
        *,
        model: Literal["tts-kokoro"] = "tts-kokoro",
        response_format: Literal["mp3", "opus", "aac", "flac", "wav", "pcm"] = "mp3",
        speed: float = 1.0,
        streaming: bool = False,
    ) -> Union[bytes, AsyncGenerator[bytes, None]]:
        """Async version of create_speech()."""
        request = SpeechRequest(
            input=input,
            model=model,
            voice=voice,
            response_format=response_format,
            speed=speed,
            streaming=streaming,
        )

        headers = {"Accept": self._get_audio_content_type(response_format)}

        if streaming:
            return self._stream_speech_async(request.model_dump(), headers)
        else:
            response = await self.client._request_async(
                "POST",
                "/audio/speech",
                data=request.model_dump(),
                headers=headers,
                stream=True,
            )
            return response.content

    async def create_speech_streaming_async(
        self,
        input: str,
        voice: str = "af_nova",
        *,
        model: Literal["tts-kokoro"] = "tts-kokoro",
        response_format: Literal["mp3", "opus", "aac", "flac", "wav", "pcm"] = "mp3",
        speed: float = 1.0,
    ) -> AsyncGenerator[bytes, None]:
        """Convenience method for async streaming speech creation."""
        return await self.create_speech_async(
            input=input,
            voice=voice,
            model=model,
            response_format=response_format,
            speed=speed,
            streaming=True,
        )

    async def _stream_speech_async(
        self, payload: dict, headers: dict
    ) -> AsyncGenerator[bytes, None]:
        """Handle async streaming speech response."""
        response = await self.client._request_async(
            "POST", "/audio/speech", data=payload, headers=headers, stream=True
        )

        async for chunk in response.aiter_bytes(chunk_size=4096):
            if chunk:
                yield chunk

    def save_speech(
        self,
        input: str,
        output_path: Union[str, Path],
        voice: str = "af_nova",
        **kwargs,
    ) -> Path:
        """
        Convert text to speech and save to file.

        Args:
            input: The text to convert to speech.
            output_path: Path to save the audio file.
            voice: Voice to use.
            **kwargs: Additional parameters for create_speech().

        Returns:
            Path to the saved file.
        """
        output_path = Path(output_path)

        # Determine format from file extension
        if "response_format" not in kwargs:
            extension = output_path.suffix.lower().lstrip(".")
            if extension in ["mp3", "opus", "aac", "flac", "wav", "pcm"]:
                kwargs["response_format"] = extension

        audio_data = self.create_speech(input, voice, **kwargs)

        # Handle streaming response
        if isinstance(audio_data, Generator):
            with open(output_path, "wb") as f:
                for chunk in audio_data:
                    f.write(chunk)
        else:
            with open(output_path, "wb") as f:
                f.write(audio_data)

        return output_path

    def list_voices(
        self, gender: Optional[Literal["male", "female"]] = None
    ) -> list[str]:
        """
        List available voices.

        Args:
            gender: Filter by gender ("male" or "female").

        Returns:
            List of voice IDs.
        """
        if gender == "male":
            return MALE_VOICES.copy()
        elif gender == "female":
            return FEMALE_VOICES.copy()
        else:
            return ALL_VOICES.copy()
