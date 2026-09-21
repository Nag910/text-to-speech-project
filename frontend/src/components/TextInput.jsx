export default function TextInput({ text, setText, maxLength }) {
  const charCount = text.length;
  const wordCount = text.trim() === "" ? 0 : text.trim().split(/\s+/).length;
  const isOverLimit = charCount > maxLength;

  return (
    <div>
      <label htmlFor="tts-text" className="block text-sm font-medium text-slate-700 mb-1">
        Enter your text
      </label>
      <textarea
        id="tts-text"
        value={text}
        onChange={(e) => setText(e.target.value)}
        rows={6}
        placeholder="Hello! Welcome to the Text-to-Speech App."
        className={`w-full resize-y rounded-lg border p-3 text-slate-800 shadow-sm focus:outline-none focus:ring-2 transition
          ${isOverLimit ? "border-red-400 focus:ring-red-300" : "border-slate-300 focus:ring-brand-500"}`}
      />
      <div className="mt-1 flex justify-between text-xs text-slate-500">
        <span>Words: {wordCount}</span>
        <span className={isOverLimit ? "text-red-500 font-medium" : ""}>
          Characters: {charCount} / {maxLength}
        </span>
      </div>
    </div>
  );
}
