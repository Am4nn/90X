/** A 14px check or cross, drawn so it never depends on a font. */
export function Glyph({ ok, size = "size-3.5" }: { ok: boolean; size?: string }) {
  return (
    <svg
      viewBox="0 0 16 16"
      className={size}
      fill="none"
      stroke="currentColor"
      strokeWidth={2}
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden
    >
      {ok ? <path d="M3 8.5l3.2 3.2L13 4.8" /> : <path d="M4.5 4.5l7 7M11.5 4.5l-7 7" />}
    </svg>
  );
}

/** The mark line under a result row: glyph and word, never colour alone. */
export function MarkLine({ ok, children }: { ok: boolean; children: React.ReactNode }) {
  return (
    <span className={`flex items-center gap-1.5 text-tag font-bold ${ok ? "text-ok" : "text-bad"}`}>
      <Glyph ok={ok} />
      {children}
    </span>
  );
}
