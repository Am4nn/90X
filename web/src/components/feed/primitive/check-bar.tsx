"use client";

import { createContext, useContext } from "react";
import { PRIMARY, SECONDARY } from "@/components/button-styles";
import type { PrimitiveAnswerProps } from "./types";

/** Skip lives in the card; the Check bar shows it beside Check so the two share a row. */
export const SkipContext = createContext<{ pending: boolean; skipping: boolean; skip: () => void } | null>(null);

/** The row every answer ends in: Skip (a third of it) beside Check answer (two thirds).
 *  Check stays grey until the answer is complete. */
export function CheckBar({
  pending,
  busy,
  complete,
  onCheck,
}: {
  pending: boolean;
  busy: string | null;
  complete: boolean;
  onCheck: () => void;
}) {
  const skip = useContext(SkipContext);
  return (
    <div className="grid grid-cols-[1fr_2fr] gap-2">
      {skip && (
        <button type="button" disabled={skip.pending} aria-busy={skip.skipping || undefined} onClick={skip.skip} className={SECONDARY}>
          {skip.skipping ? "Skipping…" : "Skip"}
        </button>
      )}
      <button
        type="button"
        disabled={pending || !complete}
        aria-busy={busy === "check" || undefined}
        onClick={onCheck}
        className={`${PRIMARY} disabled:bg-surface-2 disabled:text-mute disabled:opacity-100 ${skip ? "" : "col-span-2"}`}
      >
        {busy === "check" ? "Checking…" : "Check answer"}
      </button>
    </div>
  );
}

/** The Check row for a one-of-many pick: grey until something is selected, then it submits that pick. */
export function ChosenCheckBar({ card, selected, pending, busy, onSubmit }: PrimitiveAnswerProps & { selected: number | null }) {
  return (
    <CheckBar
      pending={pending}
      busy={busy}
      complete={selected !== null}
      onCheck={() => selected !== null && onSubmit({ cardId: card.id, shape: "chosen", picked: [selected] }, selected)}
    />
  );
}
