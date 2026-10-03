import type { Answer } from "@/lib/feed/grade";
import type { CardOptions } from "@/lib/feed/options";
import type { CorrectAnswer } from "@/lib/feed/view";
import { ClaimSwitch } from "./claim-switch";

/**
 * The question again, after it has been answered, marked up in place.
 *
 * A reader who has just answered wants one thing first: what was right, what
 * they put, and where those differ. Replacing the card with prose makes them
 * rebuild the question from memory to read the answer. Only the chosen shape
 * ever did this - every other primitive dropped its layout the moment it was
 * answered and explained itself in a paragraph instead.
 *
 * So each primitive is redrawn in its own shape, read-only, with the same
 * borders and spacing it had while it was being answered: a tick on what was
 * right, a cross on what the reader put that was not.
 */

const OK = "border-ok/50 bg-ok/5 text-text";
const BAD = "border-bad/50 bg-bad/5 text-text-2";
const IDLE = "border-line text-mute";
const CELL = "flex items-start gap-3 rounded-xl border px-4 py-3 text-body";

/** The tick, cross, or nothing that goes at the head of a row. */
function Mark({ state }: { state: "ok" | "bad" | "idle" }) {
  if (state === "idle") {
    return (
      <span className="text-mute" aria-hidden>
        •
      </span>
    );
  }
  return (
    <span
      className={state === "ok" ? "font-semibold text-ok" : "font-semibold text-bad"}
      role="img"
      aria-label={state === "ok" ? "Correct" : "Wrong"}
    >
      {state === "ok" ? "✓" : "✕"}
    </span>
  );
}

function Legend({ children }: { children: string }) {
  return <h2 className="text-small font-semibold text-mute">{children}</h2>;
}

/** The glyph and word that mark a row: never colour alone. */
function MarkLine({ ok, children }: { ok: boolean; children: string }) {
  return (
    <span className={`flex items-center gap-1.5 text-tag font-bold ${ok ? "text-ok" : "text-bad"}`}>
      <span aria-hidden>{ok ? "\u2713" : "\u2715"}</span>
      {children}
    </span>
  );
}

/** pick_one: the options again, lettered. The right one is marked, the reader's wrong pick is marked, the rest fade. */
function PickReview({ items, picked, correct }: { items: string[]; picked: number[]; correct: number[] }) {
  const chose = new Set(picked);
  const truth = new Set(correct);
  return (
    <ul className="flex flex-col gap-2" aria-label="Your answer">
      {items.map((item, index) => {
        const right = truth.has(index);
        const wrongPick = !right && chose.has(index);
        const tone = right ? "border-ok bg-surface" : wrongPick ? "border-bad bg-surface" : "border-line text-mute";
        return (
          <li key={index} className={`flex items-start gap-3 rounded-xl border px-4 py-3 ${tone}`}>
            <span
              aria-hidden
              className={`flex size-7 shrink-0 items-center justify-center rounded-lg border font-display text-small font-semibold ${
                right ? "border-ok text-ok" : wrongPick ? "border-bad text-bad" : "border-line text-mute"
              }`}
            >
              {String.fromCharCode(65 + index)}
            </span>
            <span className="flex min-w-0 flex-1 flex-col gap-1">
              <span className={right || wrongPick ? "text-body text-text" : "text-body"}>{item}</span>
              {right && <MarkLine ok>Correct</MarkLine>}
              {wrongPick && <MarkLine ok={false}>You chose</MarkLine>}
            </span>
          </li>
        );
      })}
    </ul>
  );
}

/** tap_in_place: the snippet again, the right line barred in green with the explanation under it,
 *  the reader's wrong line barred in red. */
function TapReview({ items, picked, correct, explanation }: { items: string[]; picked: number[]; correct: number[]; explanation: string }) {
  const chose = new Set(picked);
  const truth = new Set(correct);
  return (
    <div className="overflow-hidden rounded-xl border border-line bg-background" role="group" aria-label="Your answer">
      <ol>
        {items.map((line, index) => {
          const right = truth.has(index);
          const mine = chose.has(index);
          const bar = right ? "border-ok bg-ok/5" : mine ? "border-bad bg-bad/5" : "border-transparent";
          return (
            <li key={index}>
              <div className={`flex min-h-11 items-center border-l-3 font-mono text-small ${bar}`}>
                <span
                  aria-hidden
                  className={`w-11 shrink-0 pr-3 text-right select-none ${right ? "text-ok" : mine ? "text-bad" : "text-mute"}`}
                >
                  {right ? "\u2713" : mine ? "\u2715" : index + 1}
                </span>
                <span className={`overflow-x-auto pr-4 whitespace-pre ${right || mine ? "text-text" : "text-mute"}`}>{line || " "}</span>
                {mine && !right && (
                  <span className="mr-3 ml-auto shrink-0 rounded-full border border-bad px-2 py-0.5 text-tag font-bold text-bad">
                    Your pick
                  </span>
                )}
              </div>
              {right && (
                <div className="mx-3 mb-3 flex max-w-xs flex-col gap-1 rounded-xl border border-ok bg-surface px-3.5 py-3 font-sans">
                  <MarkLine ok>{`Line ${index + 1}${mine ? ", your pick" : ""}`}</MarkLine>
                  {explanation && <p className="text-small text-text-2">{explanation}</p>}
                </div>
              )}
            </li>
          );
        })}
      </ol>
    </div>
  );
}

/** claim_grid: every statement with its switch frozen where the reader left it, and whether that was right. */
function ClaimReview({ items, pairs, correct }: { items: string[]; pairs: [number, number][]; correct: [number, number][] }) {
  const mine = new Map(pairs);
  const truth = new Map(correct);
  const answered = pairs.length > 0;
  return (
    <ul className="flex flex-col gap-4" aria-label="Your answer">
      {items.map((statement, index) => {
        const want = (truth.get(index) ?? 0) as 0 | 1;
        const chose = mine.get(index);
        const ok = chose === want;
        return (
          <li key={index} className="flex flex-col gap-2 border-b border-line pb-4 last:border-0 last:pb-0">
            <div className="flex items-center justify-between gap-4">
              <p className="min-w-0 text-body text-text">{statement}</p>
              <ClaimSwitch
                label={statement}
                value={answered ? ((chose ?? want) as 0 | 1) : want}
                tone={answered ? (ok ? "right" : "wrong") : "neutral"}
              />
            </div>
            {answered && <MarkLine ok={ok}>{ok ? "Right" : `Wrong. It is ${want ? "true" : "false"}.`}</MarkLine>}
          </li>
        );
      })}
    </ul>
  );
}

/** order and assemble: the reader's sequence, with the rules it broke named. */
function OrderedReview({ items, order, constraints }: { items: string[]; order: number[]; constraints: [number, number][] }) {
  // The card stores the constraints it claims, not one blessed sequence, so
  // every genuinely correct order passes. The review says the same thing: it
  // marks the pairs this order got the wrong way round, and nothing else.
  const at = new Map(order.map((item, position) => [item, position]));
  const broken = constraints.filter(([before, after]) => (at.get(before) ?? -1) > (at.get(after) ?? -1));
  const inBroken = new Set(broken.flat());
  return (
    <div className="flex flex-col gap-3">
      <ol className="flex flex-col gap-2" aria-label="Your order">
        {order.map((item, position) => {
          const state = inBroken.has(item) ? "bad" : "ok";
          return (
            <li key={position} className={`${CELL} ${state === "ok" ? OK : BAD}`}>
              <span className="tabular w-5 shrink-0 text-mute">{position + 1}</span>
              <Mark state={state} />
              <span className="flex-1">{items[item] ?? ""}</span>
            </li>
          );
        })}
      </ol>
      {broken.length > 0 && (
        <ul className="flex flex-col gap-1.5">
          {broken.map(([before, after], index) => (
            <li key={index} className="text-small text-text-2">
              <span className="text-bad">✕</span> “{items[before] ?? ""}” has to come before “{items[after] ?? ""}”
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

/** match: each term with what the reader paired it to, and the right one beside it. */
function MatchReview({
  left,
  right,
  pairs,
  correct,
}: {
  left: string[];
  right: string[];
  pairs: [number, number][];
  correct: [number, number][];
}) {
  const mine = new Map(pairs);
  const truth = new Map(correct);
  return (
    <ul className="flex flex-col gap-2" aria-label="Your pairs">
      {left.map((term, index) => {
        const chose = mine.get(index);
        const want = truth.get(index);
        const ok = chose !== undefined && chose === want;
        return (
          <li key={index} className={`${CELL} flex-col items-stretch gap-1.5 sm:flex-row sm:items-start ${ok ? OK : BAD}`}>
            <span className="flex items-start gap-3 sm:flex-1">
              <Mark state={ok ? "ok" : "bad"} />
              <span>{term}</span>
            </span>
            <span className="flex flex-col gap-0.5 pl-7 sm:pl-0 sm:text-right">
              <span className={ok ? "text-text" : "text-bad"}>{chose === undefined ? "— not paired" : (right[chose] ?? "")}</span>
              {!ok && want !== undefined && <span className="text-small text-ok">{right[want] ?? ""}</span>}
            </span>
          </li>
        );
      })}
    </ul>
  );
}

/** bucket: the columns again, each holding what the reader put in it. */
function BucketReview({
  items,
  columns,
  pairs,
  correct,
}: {
  items: string[];
  columns: string[];
  pairs: [number, number][];
  correct: [number, number][];
}) {
  const mine = new Map(pairs);
  const truth = new Map(correct);
  return (
    <div role="group" className="grid gap-3 sm:grid-cols-2" aria-label="Your buckets">
      {columns.map((column, columnIndex) => {
        const inside = items.map((_, index) => index).filter((index) => mine.get(index) === columnIndex);
        return (
          <section key={columnIndex} className="flex flex-col gap-2 rounded-xl border border-line bg-surface-2 px-3.5 py-3">
            <h3 className="text-small font-semibold text-text-2">{column}</h3>
            {inside.length === 0 && <p className="text-small text-mute">nothing</p>}
            {inside.map((index) => {
              const ok = truth.get(index) === columnIndex;
              return (
                <p key={index} className="flex items-start gap-2 text-small">
                  <Mark state={ok ? "ok" : "bad"} />
                  <span className={ok ? "text-text" : "text-text-2"}>
                    {items[index] ?? ""}
                    {!ok && <span className="text-ok"> → {columns[truth.get(index) ?? 0] ?? ""}</span>}
                  </span>
                </p>
              );
            })}
          </section>
        );
      })}
    </div>
  );
}

const cellKey = (row: number, column: number) => `${row}:${column}`;

/** grid_toggle: the same grid, with each cell marked. */
function GridReview({
  rows,
  columns,
  pairs,
  correct,
}: {
  rows: string[];
  columns: string[];
  pairs: [number, number][];
  correct: [number, number][];
}) {
  const mine = new Set(pairs.map(([row, column]) => cellKey(row, column)));
  const truth = new Set(correct.map(([row, column]) => cellKey(row, column)));
  return (
    <div className="overflow-x-auto">
      <table className="w-full border-collapse text-small" aria-label="Your grid">
        <thead>
          <tr>
            <th scope="col" className="px-2 py-2">
              <span className="sr-only">Row</span>
            </th>
            {columns.map((column, index) => (
              <th key={index} className="px-2 py-2 text-left font-semibold text-text-2">
                {column}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, rowIndex) => (
            <tr key={rowIndex}>
              <th scope="row" className="py-2 pr-3 text-left font-normal text-text-2">
                {row}
              </th>
              {columns.map((_, columnIndex) => {
                const on = mine.has(cellKey(rowIndex, columnIndex));
                const want = truth.has(cellKey(rowIndex, columnIndex));
                return (
                  <td key={columnIndex} className="px-2 py-2">
                    <span
                      className={`flex min-h-9 min-w-9 items-center justify-center rounded-lg border ${
                        on === want ? (on ? OK : IDLE) : BAD
                      }`}
                    >
                      {on === want ? (
                        on ? (
                          <span className="text-ok">✓</span>
                        ) : (
                          <span className="text-mute" aria-hidden>
                            ·
                          </span>
                        )
                      ) : (
                        // The two ways to be wrong, told apart: on where it should
                        // be off, and off where it should be on.
                        <span className="text-bad">{on ? "✕" : "○"}</span>
                      )}
                    </span>
                  </td>
                );
              })}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function NumberReview({ value, correct, tolerance }: { value: number; correct: number; tolerance: number }) {
  const ok = Math.abs(value - correct) <= tolerance;
  return (
    <div role="group" aria-label="Your answer" className="flex flex-col gap-3">
      <div className={`flex h-18 items-center justify-center rounded-2xl border bg-background px-4 ${ok ? "border-ok" : "border-bad"}`}>
        <span className="tabular font-display text-display font-semibold text-text">{value}</span>
      </div>
      <MarkLine ok={ok}>{ok ? "In range" : "Out of range"}</MarkLine>
      {!ok && (
        <p className="rounded-xl bg-surface-2 px-4 py-3 text-small text-text-2">
          <span className="text-tag font-bold tracking-wider text-mute uppercase">Answer</span>{" "}
          <span className="tabular font-semibold text-text">{correct}</span> {tolerance > 0 ? `within ${tolerance}` : "exactly"}
        </p>
      )}
    </div>
  );
}

export function AnswerReview({
  content,
  submitted,
  correct,
  primitive,
  explanation,
}: {
  content: CardOptions | null;
  submitted: Answer | null;
  correct: CorrectAnswer | null;
  primitive: string | null;
  /** The card's explanation, shown inline under the right line for tap_in_place. */
  explanation: string;
}) {
  // A card the reader asked to be shown ("New to me") has no submission; a claim grid
  // still redraws, its switches resting at the truth.
  if (correct && !submitted && correct.shape === "mapping" && content?.shape === "list" && primitive === "claim_grid") {
    return (
      <section className="flex flex-col gap-2.5">
        <Legend>The answer</Legend>
        <ClaimReview items={content.items} pairs={[]} correct={correct.pairs} />
      </section>
    );
  }
  if (!correct || !submitted) return null;

  const body = (() => {
    if (correct.shape === "number" && submitted.shape === "number") {
      return <NumberReview value={submitted.value} correct={correct.value} tolerance={correct.tolerance} />;
    }
    if (!content) return null;
    if (correct.shape === "chosen" && submitted.shape === "chosen" && content.shape === "list") {
      return primitive === "tap_in_place" ? (
        <TapReview items={content.items} picked={submitted.picked} correct={correct.picked} explanation={explanation} />
      ) : (
        <PickReview items={content.items} picked={submitted.picked} correct={correct.picked} />
      );
    }
    if (correct.shape === "ordered" && submitted.shape === "ordered") {
      const items = content.shape === "list" ? content.items : content.shape === "assemble" ? content.tokens : null;
      return items && <OrderedReview items={items} order={submitted.order} constraints={correct.constraints} />;
    }
    if (correct.shape === "mapping" && submitted.shape === "mapping") {
      if (content.shape === "list") {
        return <ClaimReview items={content.items} pairs={submitted.pairs} correct={correct.pairs} />;
      }
      if (content.shape === "match") {
        return <MatchReview left={content.left} right={content.right} pairs={submitted.pairs} correct={correct.pairs} />;
      }
      if (content.shape === "bucket") {
        return <BucketReview items={content.items} columns={content.columns} pairs={submitted.pairs} correct={correct.pairs} />;
      }
      if (content.shape === "grid") {
        return <GridReview rows={content.rows} columns={content.columns} pairs={submitted.pairs} correct={correct.pairs} />;
      }
    }
    return null;
  })();

  if (!body) return null;
  return (
    <section className="flex flex-col gap-2.5">
      <Legend>Your answer</Legend>
      {body}
    </section>
  );
}
