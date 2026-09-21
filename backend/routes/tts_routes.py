"""
tts_routes.py
-------------
Defines the three endpoints described in the project spec:

    POST /api/tts      -> generate speech from text
    GET  /api/voices    -> list available languages + voices
    GET  /api/health    -> health check
"""

from flask import Blueprint, jsonify, request, send_from_directory

from services import tts_service
from services.tts_service import AUDIO_DIR, TTSServiceError
from utils.validators import ValidationError, validate_tts_request

tts_bp = Blueprint("tts", __name__, url_prefix="/api")


@tts_bp.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


@tts_bp.route("/voices", methods=["GET"])
def voices():
    return (
        jsonify(
            {
                "success": True,
                "languages": tts_service.get_languages(),
                "voices": tts_service.get_voices(),
            }
        ),
        200,
    )


@tts_bp.route("/tts", methods=["POST"])
def generate_speech():
    if not request.is_json:
        return (
            jsonify({"success": False, "error": "Content-Type must be application/json."}),
            400,
        )

    try:
        text, language, voice = validate_tts_request(request.get_json(silent=True) or {})
    except ValidationError as exc:
        return jsonify({"success": False, "error": exc.message}), exc.status_code

    try:
        filename = tts_service.synthesize(text, language, voice)
    except TTSServiceError as exc:
        return jsonify({"success": False, "error": str(exc)}), 503
    except Exception:  # pragma: no cover - safety net for unexpected errors
        return (
            jsonify({"success": False, "error": "Internal server error while generating speech."}),
            500,
        )

    audio_url = f"/api/audio/{filename}"
    return jsonify({"success": True, "audio_url": audio_url}), 201


@tts_bp.route("/audio/<path:filename>", methods=["GET"])
def get_audio(filename):
    # send_from_directory prevents path traversal (e.g. ../../etc/passwd)
    try:
        return send_from_directory(AUDIO_DIR, filename, mimetype="audio/wav")
    except FileNotFoundError:
        return jsonify({"success": False, "error": "Audio file not found."}), 404
