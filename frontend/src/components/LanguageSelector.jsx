export default function LanguageSelector({ languages, language, setLanguage, disabled }) {
  return (
    <div>
      <label htmlFor="language-select" className="block text-sm font-medium text-slate-700 mb-1">
        Language
      </label>
      <select
        id="language-select"
        value={language}
        disabled={disabled}
        onChange={(e) => setLanguage(e.target.value)}
        className="w-full rounded-lg border border-slate-300 p-2.5 text-slate-800 shadow-sm focus:outline-none focus:ring-2 focus:ring-brand-500 disabled:bg-slate-100 disabled:text-slate-400"
      >
        {languages.length === 0 && <option>Loading...</option>}
        {languages.map((lang) => (
          <option key={lang.code} value={lang.code}>
            {lang.name}
          </option>
        ))}
      </select>
    </div>
  );
}
