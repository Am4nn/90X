"use client";

import { useState } from "react";
import { codeLanguage } from "@/lib/feed/code";
import { ChosenCheckBar } from "./check-bar";
import { Hint } from "./hint";
import type { PrimitiveAnswerProps } from "./types";

/** The panel's header bar: the language when the question names one, and the line count. */
export function editorLabel(promptMd: string, lineCount: number): string {
  const language = codeLanguage(promptMd);
  return `${language ? `${language} · ` : ""}${lineCount} ${lineCount === 1 ? "line" : "lines"}`;
}

/** Tap in place: the reader taps the one correct line in a snippet, then Check
 *  answer. Targets are the card's option lines, never JSX: one option string per
 *  snippet line, and the submitted `picked` is the 0-based line index (the
 *  registry's tap_in_place contract). */
export function TapInPlace({ card, pending, busy, onSubmit }: PrimitiveAnswerProps) {
  const lines = card.options?.shape === "list" ? card.options.items : [];
  const [selected, setSelected] = useState<number | null>(null);

  return (
    <div className="flex flex-col gap-4">
      <Hint>{selected === null ? "Tap a line." : `Line ${selected + 1} picked. Tap another line to change it.`}</Hint>
      <div className="overflow-hidden rounded-xl border border-line bg-background">
        <div className="flex items-center justify-between border-b border-line px-3.5 py-2 font-mono text-tag text-mute">
          <span>{editorLabel(card.promptMd, lines.length)}</span>
        </div>
        <ol className="overflow-x-auto" aria-label="Options">
          {lines.map((line, index) => {
            const on = selected === index;
            return (
              <li key={index}>
                <button
                  type="button"
                  disabled={pending}
                  aria-pressed={on}
                  aria-label={`Line ${index + 1}: ${line}`}
                  onClick={() => setSelected(index)}
                  className={`flex min-h-11 w-max min-w-full items-center border-l-3 font-mono text-small leading-relaxed transition-colors disabled:opacity-60 ${
                    on ? "border-cyan bg-cyan-bg text-text" : "border-transparent text-text-2 hover:bg-surface"
                  }`}
                >
                  <span aria-hidden className={`w-11 shrink-0 pr-3 text-right select-none ${on ? "text-cyan" : "text-mute"}`}>
                    {index + 1}
                  </span>
                  <span className="pr-4 whitespace-pre">{line || " "}</span>
                  {on && <span className="mr-3 ml-auto shrink-0 text-tag font-bold text-cyan">Your pick</span>}
                </button>
              </li>
            );
          })}
        </ol>
      </div>
      <ChosenCheckBar card={card} selected={selected} pending={pending} busy={busy} onSubmit={onSubmit} />
    </div>
  );
}
