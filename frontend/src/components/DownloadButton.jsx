export default function DownloadButton({ audioUrl }) {
  if (!audioUrl) return null;

  return (
    <a
      href={audioUrl}
      download="generated-speech.wav"
      className="block w-full text-center rounded-lg border border-brand-600 px-4 py-2.5 font-medium text-brand-600 transition hover:bg-brand-50"
    >
      Download Audio
    </a>
  );
}
