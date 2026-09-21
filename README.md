# Text-to-Speech Application (Python Stack)

A full-stack web application that converts written text into natural-sounding
speech. Built with **React** (frontend) and **Flask** (backend), as a
learning project for understanding frontend/backend communication, REST
APIs, and third-party service integration.

This is the **Level 1 (Basic)** implementation:

- Text input with character/word count
- Language selection (English, Hindi, Gujarati, Marathi, Spanish, French, German)
- Voice selection (Male / Female)
- Generate speech via a backend REST API
- Play the generated audio in the browser
- Download the generated audio
- Full error handling (empty text, over-length text, invalid language/voice,
  network failures, rate limiting, server errors)

## How speech is generated

The backend uses **[espeak-ng](https://github.com/espeak-ng/espeak-ng)**, a
free, open-source, completely offline speech synthesizer, instead of a paid
cloud API. This means:

- No API key or account is required to run the project.
- It works without an internet connection.
- It already supports every language required by the spec.

The code is structured so a cloud provider (Google Cloud TTS, Azure Speech,
Amazon Polly, ElevenLabs, ...) can be swapped in later — see
`backend/services/tts_service.py`. Only that one file would need to change;
the routes, validation, and frontend stay the same. `.env.example` already
includes placeholders (`TTS_API_KEY`, `TTS_REGION`, `TTS_ENDPOINT`) for that
future step.

## Project Structure

```
text-to-speech/
├── frontend/                  React application (Vite + Tailwind CSS)
│   ├── src/
│   │   ├── components/        TextInput, LanguageSelector, VoiceSelector,
│   │   │                      GenerateButton, AudioPlayer, DownloadButton,
│   │   │                      ErrorMessage
│   │   ├── api.js             Fetch wrapper for the backend API
│   │   ├── App.jsx            Main application component
│   │   └── main.jsx
│   └── package.json
│
├── backend/                   Flask application
│   ├── app.py                 App factory, CORS, rate limiting, error handlers
│   ├── routes/
│   │   └── tts_routes.py      /api/tts, /api/voices, /api/health, /api/audio
│   ├── services/
│   │   └── tts_service.py     Wraps the TTS engine (espeak-ng)
│   ├── utils/
│   │   └── validators.py      Backend-side request validation
│   └── generated_audio/       Generated .wav files (not committed to git)
│
├── requirements.txt
├── .env.example
└── README.md
```

## Prerequisites

- **Node.js** 18+ and npm
- **Python** 3.10+
- **espeak-ng** (the offline TTS engine)

Install espeak-ng:

```bash
# Ubuntu / Debian
sudo apt-get update && sudo apt-get install -y espeak-ng

# macOS
brew install espeak-ng

# Windows
# Download the installer from https://github.com/espeak-ng/espeak-ng/releases
# and make sure espeak-ng.exe is on your PATH.
```

## Backend Setup

```bash
cd text-to-speech
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env            # review/edit values if needed

cd backend
python app.py
```

The API will be available at `http://localhost:5000`.

## Frontend Setup

In a separate terminal:

```bash
cd text-to-speech/frontend
npm install

echo "VITE_API_BASE_URL=http://localhost:5000" > .env

npm run dev
```

The app will be available at `http://localhost:5173`.

## API Reference

### `POST /api/tts`

Request:
```json
{
  "text": "Welcome to our application.",
  "language": "en-US",
  "voice": "female"
}
```

Response (201):
```json
{
  "success": true,
  "audio_url": "/api/audio/<generated-file>.wav"
}
```

Error response (400 / 503 / 500):
```json
{
  "success": false,
  "error": "Text must not be empty."
}
```

### `GET /api/voices`

Returns the available languages and voices.

### `GET /api/health`

```json
{ "status": "ok" }
```

### `GET /api/audio/<filename>`

Streams the generated audio file.

## HTTP Status Codes Used

| Status | Meaning |
|---|---|
| 200 | Successful request |
| 201 | Audio resource created |
| 400 | Invalid request (empty text, unsupported language/voice, wrong Content-Type) |
| 404 | Resource not found |
| 405 | Method not allowed |
| 429 | Too many requests (rate limit) |
| 500 | Internal server error |
| 503 | TTS engine unavailable / failed |

## Security Notes

- API credentials (for a future cloud TTS provider) live only in the
  backend's `.env` file, which is git-ignored — never in frontend code.
- All input is re-validated on the backend, regardless of what the frontend
  already checked.
- Requests to `/api/tts` are rate-limited (`flask-limiter`) to prevent abuse.
- CORS is restricted to the configured frontend origin.
- Generated audio filenames are random UUIDs served through
  `send_from_directory`, which prevents path-traversal.

## Testing

- **Frontend:** manually test empty input, long input, language/voice
  switching, loading state, audio playback, and download.
- **API:** import the endpoints into Postman and test:
  - `POST /api/tts` (valid + invalid payloads)
  - `GET /api/voices`
  - `GET /api/health`
- **Error cases:** empty text, text over the character limit, invalid
  language, invalid voice, malformed JSON, and repeated rapid requests
  (rate limiting).

## Possible Next Steps (Level 2 / 3)

- Add a database (PostgreSQL / SQLite) and user accounts to store speech
  history and favorites.
- Swap `tts_service.py` to call a cloud TTS provider for higher-quality,
  more natural voices.
- Add file upload (TXT/PDF/DOCX) and extract text before synthesis.
- Add AI-based text enhancement (summarization, grammar correction) before
  sending text to the TTS engine.
- Deploy the frontend (Vercel/Netlify) and backend (Render/Railway/AWS/Azure).
