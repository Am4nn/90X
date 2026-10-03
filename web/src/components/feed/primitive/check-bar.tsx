"use client";

import { createContext, useContext } from "react";
import { PRIMARY, SECONDARY } from "@/components/button-styles";

/** Skip lives in the card; the Check bar shows it beside Check so the two share a row. */
export const SkipContext = createContext<{ pending: boolean; skipping: boolean; skip: () => void } | null>(null);

/** The footer every mapping/ordering answer shares: a hint on the left and the
 *  Check button on the right. The hint warns (rather than mutes) when the grid
 *  is forcing a judgement the reader has not given yet. */
export function CheckBar({
  pending,
  busy,
  hint,
  warn,
  complete,
  onCheck,
}: {
  pending: boolean;
  busy: string | null;
  hint: string;
  /** Emphasise the hint when the answer is incomplete (the claim grid's "answer every row"). */
  warn?: boolean;
  complete: boolean;
  onCheck: () => void;
}) {
  const skip = useContext(SkipContext);
  return (
    <div className="flex flex-col gap-2.5">
      <span className={`text-small ${!complete && warn ? "text-warn" : "text-mute"}`}>{hint}</span>
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
          className={`${PRIMARY} ${skip ? "" : "col-span-2"}`}
        >
          {busy === "check" ? "Checking…" : "Check answer"}
        </button>
      </div>
    </div>
  );
}
