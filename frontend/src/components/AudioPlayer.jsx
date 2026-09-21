export default function AudioPlayer({ audioUrl }) {
  if (!audioUrl) return null;

  return (
    <div className="rounded-lg border border-slate-200 bg-slate-50 p-4">
      <p className="mb-2 text-sm font-medium text-slate-700">Generated Audio</p>
      {/* Native <audio> element already provides play/pause/seek/volume controls */}
      <audio controls src={audioUrl} className="w-full">
        Your browser does not support the audio element.
      </audio>
    </div>
  );
}
