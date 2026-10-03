"use client";

import { useState } from "react";
import { CheckBar } from "./check-bar";
import { ClaimSwitch } from "./claim-switch";
import { Hint } from "./hint";
import type { PrimitiveAnswerProps } from "./types";

/** Claim grid: a true/false judgement on every statement, forced. Both states stay
 *  reachable and the form refuses to submit until every statement is answered. */
export function ClaimGrid({ card, pending, busy, onSubmit }: PrimitiveAnswerProps) {
  const rows = card.options?.shape === "list" ? card.options.items : [];
  const [answers, setAnswers] = useState<(0 | 1 | null)[]>(() => rows.map(() => null));

  const marked = answers.filter((answer) => answer !== null).length;
  const complete = marked === rows.length;

  const set = (row: number, value: 0 | 1 | null) => setAnswers((current) => current.map((answer, i) => (i === row ? value : answer)));

  return (
    <div className="flex flex-col gap-4">
      <Hint>
        Each statement is judged on its own. {marked} of {rows.length} marked.
      </Hint>
      <ul className="flex flex-col gap-4" aria-label="Statements">
        {rows.map((row, index) => (
          <li key={index} className="flex items-center justify-between gap-4 border-b border-line pb-4 last:border-0 last:pb-0">
            <p className="min-w-0 text-body text-text">{row}</p>
            <ClaimSwitch
              label={row}
              value={answers[index] ?? null}
              tone={answers[index] === null ? "idle" : "selected"}
              disabled={pending}
              onSet={(next) => set(index, next)}
            />
          </li>
        ))}
      </ul>

      <CheckBar
        pending={pending}
        busy={busy}
        complete={complete}
        onCheck={() =>
          onSubmit({
            cardId: card.id,
            shape: "mapping",
            pairs: answers.flatMap((answer, i) => (answer === null ? [] : [[i, answer] as [number, number]])),
          })
        }
      />
    </div>
  );
}
