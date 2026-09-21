"""
tts_service.py
---------------
Wraps the underlying Text-to-Speech engine.

This project uses **espeak-ng** (via command line) as the default TTS
engine because it:
  - works completely offline (no API key, no external network calls)
  - supports all the languages required by the spec (English, Hindi,
    Gujarati, Marathi, Spanish, French, German)
  - is free to install on any machine (`apt-get install espeak-ng`)

The service is intentionally written behind a small abstraction
(`synthesize`, `list_voices`) so a real cloud provider (Google Cloud
TTS, Azure Speech, Amazon Polly, ElevenLabs) can be swapped in later
by changing only this file — the routes and frontend never talk to
the engine directly. See the README for how to plug in a cloud
provider using the TTS_API_KEY / TTS_REGION / TTS_ENDPOINT variables
already defined in .env.
"""

import os
import subprocess
import uuid
from pathlib import Path

# ---------------------------------------------------------------------------
# Supported languages and voices
# ---------------------------------------------------------------------------
# Maps the language codes shown in the UI to the espeak-ng language codes.
LANGUAGE_MAP = {
    "en-US": "en-us",
    "en-GB": "en-gb",
    "hi-IN": "hi",
    "gu-IN": "gu",
    "mr-IN": "mr",
    "es-ES": "es",
    "fr-FR": "fr-fr",
    "de-DE": "de",
}

# Voice variants available for every language above.
# (espeak-ng variants control pitch/tone to approximate male/female voices)
VOICE_MAP = {
    "female": "f3",
    "male": "m3",
}

LANGUAGES = [
    {"code": "en-US", "name": "English (US)"},
    {"code": "en-GB", "name": "English (UK)"},
    {"code": "hi-IN", "name": "Hindi"},
    {"code": "gu-IN", "name": "Gujarati"},
    {"code": "mr-IN", "name": "Marathi"},
    {"code": "es-ES", "name": "Spanish"},
    {"code": "fr-FR", "name": "French"},
    {"code": "de-DE", "name": "German"},
]

VOICES = [
    {"id": "female", "name": "Female Voice", "languages": list(LANGUAGE_MAP.keys())},
    {"id": "male", "name": "Male Voice", "languages": list(LANGUAGE_MAP.keys())},
]

MAX_TEXT_LENGTH = int(os.environ.get("MAX_TEXT_LENGTH", 1000))

AUDIO_DIR = Path(__file__).resolve().parent.parent / "generated_audio"
AUDIO_DIR.mkdir(exist_ok=True)


class TTSServiceError(Exception):
    """Raised when the TTS engine fails to produce audio."""


def is_valid_language(language: str) -> bool:
    return language in LANGUAGE_MAP


def is_valid_voice(voice: str) -> bool:
    return voice in VOICE_MAP


def get_languages():
    return LANGUAGES


def get_voices():
    return VOICES


def synthesize(text: str, language: str, voice: str) -> str:
    """
    Generates an audio file for the given text/language/voice.

    Returns the filename (relative to AUDIO_DIR) of the generated .wav file.
    Raises TTSServiceError on failure.
    """
    espeak_lang = LANGUAGE_MAP.get(language)
    espeak_variant = VOICE_MAP.get(voice)

    if not espeak_lang or not espeak_variant:
        raise TTSServiceError("Unsupported language or voice.")

    filename = f"{uuid.uuid4().hex}.wav"
    output_path = AUDIO_DIR / filename

    espeak_voice = f"{espeak_lang}+{espeak_variant}"

    try:
        subprocess.run(
            [
                "espeak-ng",
                "-v", espeak_voice,
                "-s", "160",       # speaking speed (words per minute)
                "-w", str(output_path),
                text,
            ],
            check=True,
            capture_output=True,
            timeout=30,
        )
    except FileNotFoundError as exc:
        raise TTSServiceError(
            "TTS engine (espeak-ng) is not installed on this server."
        ) from exc
    except subprocess.TimeoutExpired as exc:
        raise TTSServiceError("TTS generation timed out.") from exc
    except subprocess.CalledProcessError as exc:
        raise TTSServiceError(
            f"TTS engine failed: {exc.stderr.decode(errors='ignore')}"
        ) from exc

    if not output_path.exists() or output_path.stat().st_size == 0:
        raise TTSServiceError("TTS engine did not produce any audio.")

    return filename
