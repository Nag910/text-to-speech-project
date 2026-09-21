"""
app.py
------
Flask application entry point.

Run locally:
    python app.py

The server starts on http://localhost:5000 by default.
"""

import os

from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from routes.tts_routes import tts_bp

load_dotenv()


def create_app():
    app = Flask(__name__)

    # --- CORS -------------------------------------------------------------
    # Only allow the configured frontend origin(s) to call this API.
    allowed_origins = os.environ.get("ALLOWED_ORIGINS", "http://localhost:5173").split(",")
    CORS(app, resources={r"/api/*": {"origins": allowed_origins}})

    # --- Rate limiting ------------------------------------------------------
    # Protects the TTS engine from abuse (see spec section 16: Security).
    limiter = Limiter(
        get_remote_address,
        app=app,
        default_limits=[os.environ.get("RATE_LIMIT", "30 per minute")],
        storage_uri="memory://",
    )
    limiter.limit(os.environ.get("TTS_RATE_LIMIT", "10 per minute"))(tts_bp)

    app.register_blueprint(tts_bp)

    # --- Generic error handlers --------------------------------------------
    @app.errorhandler(404)
    def not_found(_e):
        return jsonify({"success": False, "error": "Resource not found."}), 404

    @app.errorhandler(405)
    def method_not_allowed(_e):
        return jsonify({"success": False, "error": "Method not allowed."}), 405

    @app.errorhandler(429)
    def rate_limited(_e):
        return jsonify({"success": False, "error": "Too many requests. Please slow down."}), 429

    @app.errorhandler(500)
    def server_error(_e):
        return jsonify({"success": False, "error": "Internal server error."}), 500

    return app


app = create_app()

if __name__ == "__main__":
    debug = os.environ.get("FLASK_DEBUG", "true").lower() == "true"
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=debug)
