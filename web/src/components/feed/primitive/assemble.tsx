"use client";

import { useState } from "react";
import { CheckBar } from "./check-bar";
import { Hint } from "./hint";
import type { PrimitiveAnswerProps } from "./types";

const CODE = "font-mono text-small leading-relaxed";
const PROSE = "text-body";

/** Pieces that are code (a symbol, a keyword in capitals) read in monospace; sentence fragments do not. */
const looksLikeCode = (tokens: string[]) => tokens.some((token) => /[;(){}[\]=<>*+/\\.,_]|^[A-Z]{2,}$/.test(token));

/** Assemble: tap pieces from the pool into the line, left to right. Pre-filled
 *  pieces (a word-bank template) stay put in grey; only the gaps are asked for. */
export function Assemble({ card, pending, busy, onSubmit }: PrimitiveAnswerProps) {
  const tokens = card.options?.shape === "assemble" ? card.options.tokens : [];
  const fixed = card.options?.shape === "assemble" ? card.options.fixed : tokens.map(() => null);

  const [slots, setSlots] = useState<(number | null)[]>(() => tokens.map((_, i) => fixed[i] ?? null));

  const gaps = tokens.map((_, i) => i).filter((i) => fixed[i] === null);
  const inPool = (index: number) => slots.every((slot) => slot !== index);
  const pool = gaps.filter(inPool);
  const nextGap = gaps.find((slot) => slots[slot] === null);
  const complete = slots.every((slot) => slot !== null);
  const templated = fixed.some((f) => f !== null);
  const TOKEN = looksLikeCode(tokens) ? CODE : PROSE;

  const place = (index: number) => {
    if (nextGap === undefined) return;
    setSlots((current) => current.map((slot, i) => (i === nextGap ? index : slot)));
  };

  const remove = (slot: number) => {
    setSlots((current) => current.map((value, i) => (i === slot ? null : value)));
  };

  return (
    <div className="flex flex-col gap-4">
      <Hint>
        {templated
          ? "Tap pieces to fill the blanks in order. Grey parts are fixed. Tap a placed piece to take it back."
          : "Tap pieces to build the line in order. Tap a placed piece to take it back."}
      </Hint>

      <div className="flex min-h-17 flex-wrap items-center gap-2 rounded-xl border border-line bg-background p-3" aria-label="Your answer">
        {slots.map((placed, slot) => {
          const pre = fixed[slot] ?? null;
          if (pre !== null) {
            return (
              <span key={slot} className={`flex min-h-11 items-center rounded-lg bg-surface-2 px-3 text-text-2 ${TOKEN}`}>
                {tokens[pre]}
              </span>
            );
          }
          if (placed === null) {
            return <span key={slot} aria-hidden className="h-11 w-13 rounded-lg border border-dashed border-line-2" />;
          }
          return (
            <button
              key={slot}
              type="button"
              disabled={pending}
              onClick={() => remove(slot)}
              aria-label={`Remove ${tokens[placed]} from the answer`}
              className={`flex min-h-11 items-center rounded-lg border border-cyan bg-cyan-bg px-3 text-text disabled:opacity-60 ${TOKEN}`}
            >
              {tokens[placed]}
            </button>
          );
        })}
      </div>

      {pool.length > 0 && (
        <ul aria-label="Tokens" className="flex min-h-15 flex-wrap gap-2">
          {pool.map((index) => (
            <li key={index}>
              <button
                type="button"
                disabled={pending}
                onClick={() => place(index)}
                className={`flex min-h-11 min-w-11 items-center rounded-lg border border-line-2 bg-surface px-3.5 text-text transition-colors hover:border-mute disabled:opacity-60 ${TOKEN}`}
              >
                {tokens[index]}
              </button>
            </li>
          ))}
        </ul>
      )}

      <CheckBar
        pending={pending}
        busy={busy}
        complete={complete}
        onCheck={() => onSubmit({ cardId: card.id, shape: "ordered", order: slots.map((placed) => placed ?? 0) })}
      />
    </div>
  );
}
