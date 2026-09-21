import { useEffect, useState } from "react";
import TextInput from "./components/TextInput";
import LanguageSelector from "./components/LanguageSelector";
import VoiceSelector from "./components/VoiceSelector";
import GenerateButton from "./components/GenerateButton";
import AudioPlayer from "./components/AudioPlayer";
import DownloadButton from "./components/DownloadButton";
import ErrorMessage from "./components/ErrorMessage";
import { fetchVoices, generateSpeech, ApiError } from "./api";

const MAX_LENGTH = 1000;

export default function App() {
  const [languages, setLanguages] = useState([]);
  const [voices, setVoices] = useState([]);
  const [language, setLanguage] = useState("en-US");
  const [voice, setVoice] = useState("female");

  const [text, setText] = useState("");
  const [audioUrl, setAudioUrl] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [loadError, setLoadError] = useState(null);

  // Load available languages/voices from the backend on mount.
  useEffect(() => {
    let cancelled = false;
    fetchVoices()
      .then((data) => {
        if (cancelled) return;
        setLanguages(data.languages);
        setVoices(data.voices);
      })
      .catch((err) => {
        if (cancelled) return;
        setLoadError(
          err instanceof ApiError
            ? err.message
            : "Could not load languages and voices from the server."
        );
      });
    return () => {
      cancelled = true;
    };
  }, []);

  const handleGenerate = async () => {
    setError(null);

    if (!text.trim()) {
      setError("Please enter some text before generating speech.");
      return;
    }
    if (text.length > MAX_LENGTH) {
      setError(`Text is too long. Maximum allowed is ${MAX_LENGTH} characters.`);
      return;
    }

    setLoading(true);
    setAudioUrl(null);
    try {
      const url = await generateSpeech({ text, language, voice });
      setAudioUrl(url);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Unexpected error. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setText("");
    setAudioUrl(null);
    setError(null);
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-brand-50 to-white">
      <div className="mx-auto max-w-xl px-4 py-10">
        <header className="mb-6 text-center">
          <h1 className="text-3xl font-bold text-slate-900">Text to Speech</h1>
          <p className="mt-1 text-sm text-slate-500">
            Convert written text into natural-sounding speech.
          </p>
        </header>

        <main className="space-y-5 rounded-2xl bg-white p-6 shadow-lg ring-1 ring-slate-100">
          {loadError && <ErrorMessage message={loadError} onDismiss={() => setLoadError(null)} />}
          {error && <ErrorMessage message={error} onDismiss={() => setError(null)} />}

          <TextInput text={text} setText={setText} maxLength={MAX_LENGTH} />

          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <LanguageSelector
              languages={languages}
              language={language}
              setLanguage={(lang) => {
                setLanguage(lang);
                setAudioUrl(null);
              }}
              disabled={languages.length === 0}
            />
            <VoiceSelector
              voices={voices}
              language={language}
              voice={voice}
              setVoice={setVoice}
              disabled={voices.length === 0}
            />
          </div>

          <div className="flex gap-3">
            <GenerateButton
              onClick={handleGenerate}
              loading={loading}
              disabled={languages.length === 0}
            />
            <button
              type="button"
              onClick={handleClear}
              className="shrink-0 rounded-lg border border-slate-300 px-4 py-3 font-medium text-slate-600 transition hover:bg-slate-50"
            >
              Clear
            </button>
          </div>

          <AudioPlayer audioUrl={audioUrl} />
          <DownloadButton audioUrl={audioUrl} />
        </main>

        <footer className="mt-6 text-center text-xs text-slate-400">
          React + Flask · Text-to-Speech demo project
        </footer>
      </div>
    </div>
  );
}
