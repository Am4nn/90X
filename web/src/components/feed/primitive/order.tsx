"use client";

import { useState } from "react";
import { CheckBar } from "./check-bar";
import { Eyebrow, Hint } from "./hint";
import type { PrimitiveAnswerProps } from "./types";

/** Order: tap the steps in the order you want them; they fill numbered slots.
 *  Tapping a placed step sends it back to the pool. */
export function Order({ card, pending, busy, onSubmit }: PrimitiveAnswerProps) {
  const items = card.options?.shape === "list" ? card.options.items : [];
  const [placed, setPlaced] = useState<number[]>([]);

  const remaining = items.map((_, i) => i).filter((i) => !placed.includes(i));
  const complete = remaining.length === 0;

  const place = (index: number) => setPlaced((current) => [...current, index]);
  const remove = (index: number) => setPlaced((current) => current.filter((i) => i !== index));

  return (
    <div className="flex flex-col gap-4">
      <Hint>Tap the steps in order. Tap a placed step to take it back.</Hint>

      <div className="flex flex-col gap-2">
        <Eyebrow>Your order</Eyebrow>
        <ol aria-label="Your order" className="flex flex-col gap-2">
          {items.map((_, slot) => {
            const index = placed[slot];
            return (
              <li key={slot}>
                {index === undefined ? (
                  <div
                    aria-hidden
                    className="flex min-h-12 items-center gap-3 rounded-xl border border-dashed border-line-2 py-0 pr-3.5 pl-2.5 text-small text-mute"
                  >
                    <span className="tabular grid size-6.5 shrink-0 place-items-center rounded-lg border border-line font-display text-small font-semibold">
                      {slot + 1}
                    </span>
                    {slot === placed.length ? "Tap a step" : ""}
                  </div>
                ) : (
                  <button
                    type="button"
                    disabled={pending}
                    onClick={() => remove(index)}
                    aria-label={`Remove ${items[index]} from the order`}
                    className="flex min-h-12 w-full items-start gap-3 rounded-xl border border-cyan bg-cyan-bg py-2.5 pr-3.5 pl-2.5 text-left text-body text-text disabled:opacity-60"
                  >
                    <span className="tabular grid size-6.5 shrink-0 place-items-center rounded-lg bg-on-cyan font-display text-small font-semibold text-cyan">
                      {slot + 1}
                    </span>
                    <span className="min-w-0 flex-1 text-pretty">{items[index]}</span>
                  </button>
                )}
              </li>
            );
          })}
        </ol>
      </div>

      {remaining.length > 0 && (
        <div className="flex flex-col gap-2">
          <Eyebrow>Steps</Eyebrow>
          <ul aria-label="Items to place" className="flex flex-col gap-2">
            {remaining.map((index) => (
              <li key={index}>
                <button
                  type="button"
                  disabled={pending}
                  onClick={() => place(index)}
                  className="flex min-h-12 w-full items-start rounded-xl border border-line-2 bg-surface py-2.5 pr-3.5 pl-3.5 text-left text-body text-text transition-colors hover:border-mute disabled:opacity-60"
                >
                  <span className="min-w-0 flex-1 text-pretty">{items[index]}</span>
                </button>
              </li>
            ))}
          </ul>
        </div>
      )}

      <CheckBar
        pending={pending}
        busy={busy}
        complete={complete}
        onCheck={() => onSubmit({ cardId: card.id, shape: "ordered", order: placed })}
      />
    </div>
  );
}
