"use client";

import { useState } from "react";
import { CheckBar } from "./check-bar";
import type { PrimitiveAnswerProps } from "./types";

/** Pick one: tap the single option you think is right, then Check answer. */
export function PickOne({ card, pending, busy, onSubmit }: PrimitiveAnswerProps) {
  const options = card.options?.shape === "list" ? card.options.items : [];
  const [selected, setSelected] = useState<number | null>(null);

  return (
    <div className="flex flex-col gap-4">
      <ul className="flex flex-col gap-2" aria-label="Options">
        {options.map((option, index) => {
          const on = selected === index;
          return (
            <li key={index}>
              <button
                type="button"
                disabled={pending}
                aria-pressed={on}
                onClick={() => setSelected(index)}
                className={`flex min-h-11 w-full items-center gap-3 rounded-xl border px-4 py-3 text-left text-body text-text transition-colors disabled:opacity-60 ${
                  on ? "border-cyan bg-cyan-bg" : "border-line-2 bg-surface hover:border-mute"
                }`}
              >
                <span
                  aria-hidden
                  className={`flex size-7 shrink-0 items-center justify-center rounded-lg border font-display text-small font-semibold ${
                    on ? "border-cyan text-cyan" : "border-line-2 text-mute"
                  }`}
                >
                  {String.fromCharCode(65 + index)}
                </span>
                <span className="min-w-0">{option}</span>
              </button>
            </li>
          );
        })}
      </ul>
      <CheckBar
        pending={pending}
        busy={busy}
        complete={selected !== null}
        onCheck={() => selected !== null && onSubmit({ cardId: card.id, shape: "chosen", picked: [selected] }, selected)}
      />
    </div>
  );
}
