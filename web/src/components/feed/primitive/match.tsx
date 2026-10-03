"use client";

import { useState } from "react";
import { CheckBar } from "./check-bar";
import { Eyebrow, Hint } from "./hint";
import type { PrimitiveAnswerProps } from "./types";

const LETTERS = "ABCDEFGH";

/** Match: tap a term to arm it, tap a meaning to lock the pair. A paired term
 *  unpairs when tapped again. Terms are lettered; a meaning shows the letter of
 *  the term paired to it. */
export function Match({ card, pending, busy, onSubmit }: PrimitiveAnswerProps) {
  const items = card.options?.shape === "match" ? card.options.left : [];
  const targets = card.options?.shape === "match" ? card.options.right : [];
  const [pairs, setPairs] = useState<[number, number][]>([]);
  const [armed, setArmed] = useState<number | null>(null);

  const pairedLeft = new Set(pairs.map(([left]) => left));
  const ownerOf = new Map(pairs.map(([left, right]) => [right, left]));
  const matchedTo = new Map(pairs.map(([left, right]) => [left, right]));
  const complete = pairs.length === items.length;

  const armLeft = (index: number) => {
    if (pairedLeft.has(index)) {
      setPairs((current) => current.filter(([left]) => left !== index));
      setArmed(index);
      return;
    }
    setArmed((current) => (current === index ? null : index));
  };

  const lockRight = (right: number) => {
    if (armed === null) return;
    const left = armed;
    setPairs((current) => [...current.filter(([l, r]) => l !== left && r !== right), [left, right]]);
    setArmed(null);
  };

  return (
    <div className="flex flex-col gap-4">
      <Hint>
        {armed !== null ? `Now tap the meaning for ${items[armed] ?? ""}.` : "Tap a term, then its meaning. Tap a paired term to undo it."}
      </Hint>

      <div className="flex flex-col gap-2">
        <Eyebrow>Terms</Eyebrow>
        <ul aria-label="Terms" className="flex flex-wrap gap-2">
          {items.map((item, index) => {
            const locked = pairedLeft.has(index);
            const on = armed === index;
            return (
              <li key={index}>
                <button
                  type="button"
                  disabled={pending}
                  aria-pressed={on}
                  aria-label={locked ? `${item} — matched to ${targets[matchedTo.get(index) ?? 0] ?? ""}` : item}
                  onClick={() => armLeft(index)}
                  className={`flex min-h-11 items-center gap-2.5 rounded-xl border py-2 pr-3 pl-2 text-left text-body font-semibold transition-colors disabled:opacity-60 ${
                    on
                      ? "border-cyan bg-cyan-bg text-text"
                      : locked
                        ? "border-line bg-surface text-mute"
                        : "border-line-2 bg-surface text-text hover:border-mute"
                  }`}
                >
                  <span aria-hidden className="grid size-6.5 shrink-0 place-items-center rounded-lg bg-line text-tag font-bold text-text">
                    {LETTERS[index]}
                  </span>
                  {item}
                </button>
              </li>
            );
          })}
        </ul>
      </div>

      <div className="flex flex-col gap-2">
        <Eyebrow>Meanings</Eyebrow>
        <ul aria-label="Meanings" className="flex flex-col gap-2">
          {targets.map((target, index) => {
            const owner = ownerOf.get(index);
            const paired = owner !== undefined;
            return (
              <li key={index}>
                <button
                  type="button"
                  disabled={pending || armed === null}
                  onClick={() => lockRight(index)}
                  aria-label={target}
                  className={`flex min-h-12 w-full items-start gap-3 rounded-xl border py-2.5 pr-3.5 pl-2.5 text-left text-body transition-colors disabled:opacity-100 ${
                    paired
                      ? "border-cyan bg-cyan-bg text-text"
                      : armed !== null
                        ? "border-dashed border-cyan bg-surface text-text hover:bg-cyan-bg"
                        : "border-line-2 bg-surface text-text"
                  }`}
                >
                  <span
                    aria-hidden
                    className={`grid size-6.5 shrink-0 place-items-center rounded-lg border text-tag font-bold ${
                      paired ? "border-cyan bg-background text-cyan" : "border-dashed border-line-2 text-mute"
                    }`}
                  >
                    {paired ? LETTERS[owner] : ""}
                  </span>
                  <span className="text-pretty">{target}</span>
                </button>
              </li>
            );
          })}
        </ul>
      </div>

      <CheckBar pending={pending} busy={busy} complete={complete} onCheck={() => onSubmit({ cardId: card.id, shape: "mapping", pairs })} />
    </div>
  );
}
