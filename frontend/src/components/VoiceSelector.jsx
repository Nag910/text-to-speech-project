export default function VoiceSelector({ voices, language, voice, setVoice, disabled }) {
  const availableVoices = voices.filter((v) => v.languages.includes(language));

  return (
    <div>
      <label htmlFor="voice-select" className="block text-sm font-medium text-slate-700 mb-1">
        Voice
      </label>
      <select
        id="voice-select"
        value={voice}
        disabled={disabled}
        onChange={(e) => setVoice(e.target.value)}
        className="w-full rounded-lg border border-slate-300 p-2.5 text-slate-800 shadow-sm focus:outline-none focus:ring-2 focus:ring-brand-500 disabled:bg-slate-100 disabled:text-slate-400"
      >
        {availableVoices.length === 0 && <option>No voices available</option>}
        {availableVoices.map((v) => (
          <option key={v.id} value={v.id}>
            {v.name}
          </option>
        ))}
      </select>
    </div>
  );
}
