"use client";

import { useState } from "react";
import { CheckBar } from "./check-bar";
import { Eyebrow, Hint } from "./hint";
import type { PrimitiveAnswerProps } from "./types";

const CHIP =
  "flex min-h-11 items-center gap-2.5 rounded-xl border py-2.5 pr-3 pl-3.5 text-left text-body transition-colors disabled:opacity-60";

/** Bucket: tap an item to arm it, tap a column to place it there. Each item lands
 *  in exactly one column. Tapping a placed item arms it again to move it. */
export function Bucket({ card, pending, busy, onSubmit }: PrimitiveAnswerProps) {
  const items = card.options?.shape === "bucket" ? card.options.items : [];
  const columns = card.options?.shape === "bucket" ? card.options.columns : [];
  const [assigned, setAssigned] = useState<(number | null)[]>(() => items.map(() => null));
  const [armed, setArmed] = useState<number | null>(null);

  const complete = assigned.every((column) => column !== null);
  const loose = items.map((_, i) => i).filter((i) => assigned[i] === null);

  const armItem = (index: number) => setArmed((current) => (current === index ? null : index));

  const placeIn = (column: number) => {
    if (armed === null) return;
    const item = armed;
    setAssigned((current) => current.map((c, i) => (i === item ? column : c)));
    setArmed(null);
  };

  const chip = (index: number) => {
    const column = assigned[index];
    const on = armed === index;
    return (
      <button
        type="button"
        disabled={pending}
        aria-pressed={on}
        aria-label={column != null ? `${items[index]} — in ${columns[column]}` : items[index]}
        onClick={() => armItem(index)}
        className={`${CHIP} ${on ? "border-cyan bg-cyan-bg text-text" : "border-line-2 bg-surface text-text hover:border-mute"}`}
      >
        {items[index]}
      </button>
    );
  };

  return (
    <div className="flex flex-col gap-4">
      <Hint>
        {armed !== null ? `Tap the column for "${items[armed] ?? ""}".` : "Tap an item, then its column. Tap a placed item to move it."}
      </Hint>

      {loose.length > 0 && (
        <div className="flex flex-col gap-2">
          <Eyebrow>To sort</Eyebrow>
          <ul aria-label="Items" className="flex min-h-11 flex-wrap gap-2">
            {loose.map((index) => (
              <li key={index}>{chip(index)}</li>
            ))}
          </ul>
        </div>
      )}

      <ul aria-label="Columns" className="flex flex-col gap-3">
        {columns.map((column, columnIndex) => {
          const inside = items.map((_, i) => i).filter((i) => assigned[i] === columnIndex);
          return (
            <li key={columnIndex}>
              <div
                className={`flex min-h-19 flex-col gap-2 rounded-xl border p-3 ${
                  armed !== null ? "border-dashed border-cyan bg-surface" : "border-line-2 bg-surface"
                }`}
              >
                <button
                  type="button"
                  disabled={pending || armed === null}
                  onClick={() => placeIn(columnIndex)}
                  aria-label={column}
                  className="flex items-center justify-between gap-2 text-left disabled:opacity-100"
                >
                  <span className="font-display text-heading font-semibold text-text">{column}</span>
                  {armed !== null && <span className="text-tag font-bold text-cyan">Place here</span>}
                </button>
                {inside.length > 0 && (
                  <ul aria-label={`In ${column}`} className="flex flex-wrap gap-2">
                    {inside.map((index) => (
                      <li key={index}>{chip(index)}</li>
                    ))}
                  </ul>
                )}
              </div>
            </li>
          );
        })}
      </ul>

      <CheckBar
        pending={pending}
        busy={busy}
        complete={complete}
        onCheck={() =>
          onSubmit({
            cardId: card.id,
            shape: "mapping",
            pairs: assigned.flatMap((c, i) => (c === null ? [] : [[i, c] as [number, number]])),
          })
        }
      />
    </div>
  );
}
