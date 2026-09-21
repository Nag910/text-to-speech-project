"""
validators.py
--------------
Backend-side validation. The rule throughout this project is:
"never trust data received from the frontend" — every request is
re-validated here even if the React app already validated it.
"""

from services.tts_service import (
    MAX_TEXT_LENGTH,
    is_valid_language,
    is_valid_voice,
)


class ValidationError(Exception):
    """Raised when a request fails validation. Carries an HTTP status code."""

    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


def validate_tts_request(data: dict):
    if not isinstance(data, dict):
        raise ValidationError("Request body must be a JSON object.", 400)

    text = data.get("text", "")
    language = data.get("language", "")
    voice = data.get("voice", "")

    if not isinstance(text, str) or not text.strip():
        raise ValidationError("Text must not be empty.", 400)

    if len(text) > MAX_TEXT_LENGTH:
        raise ValidationError(
            f"Text exceeds the maximum allowed length of {MAX_TEXT_LENGTH} characters.",
            400,
        )

    if not language or not is_valid_language(language):
        raise ValidationError(f"Unsupported language: '{language}'.", 400)

    if not voice or not is_valid_voice(voice):
        raise ValidationError(f"Unsupported voice: '{voice}'.", 400)

    return text.strip(), language, voice
