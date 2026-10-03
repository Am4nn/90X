"use client";

import { useState } from "react";
import { dropIndex, placeAt, without } from "@/lib/feed/drag";
import { CheckBar } from "./check-bar";
import { Eyebrow, Hint } from "./hint";
import { Grip } from "./marks";
import type { PrimitiveAnswerProps } from "./types";
import { useDrag } from "./use-drag";

/** Order: tap the steps in the order you want them, or drag them into place. They fill
 *  numbered slots. Tapping a placed step sends it back to the pool; dragging one moves it. */
export function Order({ card, pending, busy, onSubmit }: PrimitiveAnswerProps) {
  const items = card.options?.shape === "list" ? card.options.items : [];
  const [placed, setPlaced] = useState<number[]>([]);

  const remaining = items.map((_, i) => i).filter((i) => !placed.includes(i));
  const complete = remaining.length === 0;

  const place = (index: number) => setPlaced((current) => [...current, index]);
  const remove = (index: number) => setPlaced((current) => without(current, index));

  const { dragging, over, drag } = useDrag({
    onDrop: (source, target, side) => {
      const item = source.startsWith("p") ? Number(source.slice(1)) : placed[Number(source.slice(1))];
      if (item === undefined) return;
      if (target === "pool") return remove(item);
      if (!target.startsWith("slot")) return;
      const slot = Number(target.slice(4));
      let at = dropIndex(slot, side, slot < placed.length);
      const from = placed.indexOf(item);
      if (from !== -1 && from < at) at -= 1;
      setPlaced((current) => placeAt(current, item, at));
    },
  });

  return (
    <div className="flex flex-col gap-4">
      <Hint>Tap the steps in order, or drag them into place. Drag a placed step to reorder it; tap it to take it back.</Hint>

      <div className="flex flex-col gap-2">
        <Eyebrow>Your order</Eyebrow>
        <ol aria-label="Your order" className="flex flex-col gap-2">
          {items.map((_, slot) => {
            const index = placed[slot];
            const target = over?.id === `slot${slot}` ? over : null;
            const insert = target && index !== undefined ? target.side : undefined;
            return (
              <li
                key={slot}
                data-drop={`slot${slot}`}
                data-insert={insert}
                className="rounded-xl data-[insert=after]:shadow-[0_6px_0_0_var(--color-cyan)] data-[insert=before]:shadow-[0_-6px_0_0_var(--color-cyan)]"
              >
                {index === undefined ? (
                  <div
                    aria-hidden
                    className={`flex min-h-12 items-center gap-3 rounded-xl border py-0 pr-3.5 pl-2.5 text-small text-mute ${
                      target ? "border-cyan bg-cyan-bg" : dragging !== null ? "border-dashed border-cyan" : "border-dashed border-line-2"
                    }`}
                  >
                    <span className="tabular grid size-6.5 shrink-0 place-items-center rounded-lg border border-line font-display text-small font-semibold">
                      {slot + 1}
                    </span>
                    {slot === placed.length ? "Tap or drag a step here" : ""}
                  </div>
                ) : (
                  <div
                    {...drag(`s${slot}`, true)}
                    className={`flex min-h-12 items-start gap-1 rounded-xl border border-cyan bg-cyan-bg pr-1 pl-2.5 select-none ${
                      dragging === `s${slot}` ? "opacity-35" : ""
                    }`}
                  >
                    <button
                      type="button"
                      disabled={pending}
                      onClick={() => remove(index)}
                      aria-label={`Remove ${items[index]} from the order`}
                      className="flex min-w-0 flex-1 items-start gap-3 py-2.5 text-left text-body text-text disabled:opacity-60"
                    >
                      <span className="tabular grid size-6.5 shrink-0 place-items-center rounded-lg bg-on-cyan font-display text-small font-semibold text-cyan">
                        {slot + 1}
                      </span>
                      <span className="min-w-0 flex-1 text-pretty">{items[index]}</span>
                    </button>
                    <span data-grip className="flex w-8 shrink-0 cursor-grab touch-none items-center justify-center self-stretch text-mute">
                      <Grip className="" />
                    </span>
                  </div>
                )}
              </li>
            );
          })}
        </ol>
      </div>

      {(remaining.length > 0 || dragging !== null) && (
        <div
          data-drop="pool"
          className={`-m-2 flex flex-col gap-2 rounded-2xl border p-2 ${
            over?.id === "pool" ? "border-cyan bg-cyan-bg" : dragging?.startsWith("s") ? "border-dashed border-cyan" : "border-transparent"
          }`}
        >
          <Eyebrow>Steps</Eyebrow>
          <ul aria-label="Items to place" className="flex flex-col gap-2">
            {remaining.map((index) => (
              <li key={index}>
                <div
                  {...drag(`p${index}`, true)}
                  className={`flex min-h-12 items-start rounded-xl border border-line-2 bg-surface pr-1 pl-3.5 transition-colors select-none hover:border-mute ${
                    dragging === `p${index}` ? "opacity-35" : ""
                  }`}
                >
                  <button
                    type="button"
                    disabled={pending}
                    onClick={() => place(index)}
                    className="min-w-0 flex-1 py-2.5 text-left text-body text-text disabled:opacity-60"
                  >
                    <span className="text-pretty">{items[index]}</span>
                  </button>
                  <span className="flex w-8 shrink-0 cursor-grab touch-none items-center justify-center self-stretch text-mute">
                    <Grip className="" />
                  </span>
                </div>
              </li>
            ))}
            {remaining.length === 0 && dragging !== null && <li className="py-1.5 text-small text-text-2">Drop here to take it back</li>}
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
