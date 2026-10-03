"use client";

import { SECONDARY } from "@/components/button-styles";
import { Hint } from "./hint";
import type { PrimitiveAnswerProps } from "./types";

/** Self-rate: the reader judges whether they knew this one. No right answer, so
 *  got counts as a hit and missed as a miss. The pair is the whole screen; Skip
 *  moves to the quiet row beneath the card. */
export function SelfRate({ card, pending, busy, onSubmit }: PrimitiveAnswerProps) {
  return (
    <div className="flex flex-col gap-4">
      <Hint>Answer it in your head, then say how it went.</Hint>
      <div role="group" aria-label="Rate yourself" className="grid grid-cols-2 gap-2">
        <button
          type="button"
          disabled={pending}
          aria-busy={busy === "self" || undefined}
          onClick={() => onSubmit({ cardId: card.id, selfMark: "missed" })}
          className={SECONDARY}
        >
          Missed it
        </button>
        <button
          type="button"
          disabled={pending}
          aria-busy={busy === "self" || undefined}
          onClick={() => onSubmit({ cardId: card.id, selfMark: "got" })}
          className={SECONDARY}
        >
          Got it
        </button>
      </div>
    </div>
  );
}
