import type { Answer } from "@/lib/feed/grade";
import type { CardOptions } from "@/lib/feed/options";
import { brokenRules, onlyOrder, sampleOrder } from "@/lib/feed/order";
import type { CorrectAnswer } from "@/lib/feed/view";
import { ClaimSwitch } from "./claim-switch";
import { Eyebrow } from "./hint";
import { Glyph, MarkLine } from "./marks";
import { editorLabel } from "./tap-in-place";

/**
 * The question again, after it has been answered, marked up in place.
 *
 * A reader who has just answered wants one thing first: what was right, what
 * they put, and where those differ. Replacing the card with prose makes them
 * rebuild the question from memory to read the answer. So each primitive is
 * redrawn in its own shape, read-only: a mark and a word on what was right, and
 * on what the reader put that was not. Never colour alone.
 *
 * A card the reader asked to be shown ("New to me") has no submission; each
 * shape then draws the right answer on its own.
 */

const LETTERS = "ABCDEFGH";
const ROW = "rounded-xl border px-3.5 py-3";

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
              {LETTERS[index]}
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
function TapReview({
  items,
  picked,
  correct,
  explanation,
  promptMd,
}: {
  items: string[];
  picked: number[];
  correct: number[];
  explanation: string;
  promptMd: string;
}) {
  const chose = new Set(picked);
  const truth = new Set(correct);
  return (
    <div className="overflow-hidden rounded-xl border border-line bg-background" role="group" aria-label="Your answer">
      <div className="border-b border-line px-3.5 py-2 font-mono text-tag text-mute">{editorLabel(promptMd, items.length)}</div>
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
                  {right ? "✓" : mine ? "✕" : index + 1}
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
            {answered && <MarkLine ok={ok}>{ok ? "Right" : `Wrong. It's ${want ? "true" : "false"}.`}</MarkLine>}
          </li>
        );
      })}
    </ul>
  );
}

/** order: the reader's sequence, the rules it broke named, and the rules that are actually fixed. */
function OrderReview({
  items,
  order,
  constraints,
  revealed,
}: {
  items: string[];
  order: number[];
  constraints: [number, number][];
  revealed: boolean;
}) {
  const broken = revealed ? [] : brokenRules(order, constraints);
  const fixed = onlyOrder(items.length, constraints) !== null;
  return (
    <div className="flex flex-col gap-5">
      <div className="flex flex-col gap-2">
        <Eyebrow>{revealed ? "One order that works" : "Your order"}</Eyebrow>
        <ol aria-label="Your order" className="flex flex-col gap-1.5">
          {order.map((item, position) => (
            <li key={position} className="flex items-start gap-3 rounded-xl border border-line py-2.5 pr-3.5 pl-2.5 text-body text-text">
              <span className="tabular grid size-6.5 shrink-0 place-items-center rounded-lg bg-line font-display text-small font-semibold">
                {position + 1}
              </span>
              <span className="text-pretty">{items[item] ?? ""}</span>
            </li>
          ))}
        </ol>
      </div>

      {broken.length > 0 && (
        <div className="flex flex-col gap-2">
          <Eyebrow>The wrong way round</Eyebrow>
          <ul className="flex flex-col gap-2">
            {broken.map(([before, after], index) => (
              <li key={index} className="flex items-start gap-2.5 rounded-xl border border-bad px-3.5 py-3 text-body text-text">
                <span className="mt-1 text-bad">
                  <Glyph ok={false} />
                </span>
                <span className="text-pretty">
                  {items[before] ?? ""} has to come before {items[after] ?? ""}.
                </span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {constraints.length > 0 && (
        <div className="flex flex-col gap-1.5">
          <p className="text-small text-text-2">
            {fixed ? "The order is fixed by these rules:" : "Several orders are right. Only these rules are fixed:"}
          </p>
          {constraints.map(([before, after], index) => (
            <span key={index} className="border-l border-line-2 pl-3 text-small text-mute">
              {items[before] ?? ""} has to come before {items[after] ?? ""}.
            </span>
          ))}
        </div>
      )}
    </div>
  );
}

/** assemble: the line the reader built with misplaced pieces crossed, then the right line. */
function AssembleReview({
  tokens,
  fixed,
  order,
  constraints,
  revealed,
}: {
  tokens: string[];
  fixed: (number | null)[];
  order: number[];
  constraints: [number, number][];
  revealed: boolean;
}) {
  const right = onlyOrder(tokens.length, constraints);
  const sequence = revealed && right ? right : order;
  const wrong = right && !revealed ? sequence.filter((token, position) => token !== right[position]).length : 0;
  const line = (seq: number[], bad: (position: number) => boolean) =>
    seq.map((token, position) =>
      fixed[position] != null ? (
        <span key={position} className="flex min-h-9 items-center rounded-lg bg-surface-2 px-2.5 font-mono text-small text-text-2">
          {tokens[token]}
        </span>
      ) : (
        <span
          key={position}
          className={`flex min-h-9 items-center gap-1.5 rounded-lg border px-2.5 font-mono text-small text-text ${bad(position) ? "border-bad" : "border-line-2"}`}
        >
          {bad(position) && (
            <span className="text-bad">
              <Glyph ok={false} size="size-3" />
            </span>
          )}
          {tokens[token]}
        </span>
      ),
    );
  return (
    <div className="flex flex-col gap-3.5" role="group" aria-label="Your answer">
      <div className="flex flex-col gap-2">
        <Eyebrow>{revealed ? "The answer" : "What you built"}</Eyebrow>
        <div className="flex flex-wrap items-center gap-1.5">
          {line(sequence, (position) => Boolean(right && !revealed && sequence[position] !== right[position]))}
        </div>
        {wrong > 0 && <MarkLine ok={false}>{`${wrong} ${wrong === 1 ? "piece is" : "pieces are"} in the wrong place`}</MarkLine>}
      </div>
      {wrong > 0 && right && (
        <div className="flex flex-col gap-2">
          <Eyebrow>Right</Eyebrow>
          <span className="rounded-xl border border-ok px-3.5 py-2.5 font-mono text-small text-text">
            {right.map((token) => tokens[token]).join(" ")}
          </span>
        </div>
      )}
    </div>
  );
}

/** match: each term with what the reader paired it to, and the right meaning where they differ. */
function MatchReview({
  left,
  right,
  pairs,
  correct,
  revealed,
}: {
  left: string[];
  right: string[];
  pairs: [number, number][];
  correct: [number, number][];
  revealed: boolean;
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
          <li key={index} className={`${ROW} flex flex-col gap-2 ${revealed ? "border-line" : ok ? "border-ok" : "border-bad"}`}>
            <div className="flex items-center justify-between gap-2.5">
              <span className="text-body font-semibold text-text">{term}</span>
              {!revealed && <MarkLine ok={ok}>{ok ? "Right" : "Wrong pairing"}</MarkLine>}
            </div>
            {!revealed && (
              <div className="flex flex-col gap-0.5">
                <span className="text-tag font-bold text-mute">You paired</span>
                <span className={`text-body text-pretty ${ok ? "text-text" : "text-text-2"}`}>
                  {chose === undefined ? "Nothing" : (right[chose] ?? "")}
                </span>
              </div>
            )}
            {(revealed || !ok) && want !== undefined && (
              <div className="flex flex-col gap-0.5">
                <span className="text-tag font-bold text-mute">{revealed ? "Meaning" : "Right meaning"}</span>
                <span className="text-body text-pretty text-text">{right[want] ?? ""}</span>
              </div>
            )}
          </li>
        );
      })}
    </ul>
  );
}

/** bucket: the columns again, each holding what the reader put in it, wrong ones told where they belong. */
function BucketReview({
  items,
  columns,
  pairs,
  correct,
  revealed,
}: {
  items: string[];
  columns: string[];
  pairs: [number, number][];
  correct: [number, number][];
  revealed: boolean;
}) {
  const truth = new Map(correct);
  const mine = revealed ? truth : new Map(pairs);
  return (
    <div role="group" className="flex flex-col gap-3" aria-label="Your buckets">
      {columns.map((column, columnIndex) => {
        const inside = items.map((_, index) => index).filter((index) => mine.get(index) === columnIndex);
        return (
          <section key={columnIndex} className="flex flex-col gap-2 rounded-xl border border-line p-3">
            <h3 className="font-display text-heading font-semibold text-text">{column}</h3>
            {inside.length === 0 && <p className="text-small text-mute">Nothing placed here</p>}
            {inside.map((index) => {
              const ok = truth.get(index) === columnIndex;
              return (
                <div
                  key={index}
                  className={`flex flex-col gap-2 rounded-xl border px-3.5 py-2.5 ${revealed || ok ? (revealed ? "border-line" : "border-ok") : "border-bad"}`}
                >
                  <span className="text-body text-pretty text-text">{items[index] ?? ""}</span>
                  {!revealed && <MarkLine ok={ok}>{ok ? "Right" : `Wrong. Belongs in ${columns[truth.get(index) ?? 0] ?? ""}`}</MarkLine>}
                </div>
              );
            })}
          </section>
        );
      })}
    </div>
  );
}

/** grid_toggle "Lights": the same grid, each cell marked. Right is green, lit by mistake is red, missed is a dashed red ring. */
function GridReview({
  rows,
  columns,
  picked,
  correct,
  revealed,
}: {
  rows: string[];
  columns: string[];
  picked: number[];
  correct: number[];
  revealed: boolean;
}) {
  const mine = new Set(revealed ? [] : picked);
  const truth = new Set(correct);
  const track =
    ({ 1: "grid-cols-1", 2: "grid-cols-2", 3: "grid-cols-3", 4: "grid-cols-4", 5: "grid-cols-5" } as Record<number, string>)[
      columns.length
    ] ?? "grid-cols-3";
  const wrongSomewhere = !revealed && (picked.some((cell) => !truth.has(cell)) || correct.some((cell) => !mine.has(cell)));
  return (
    <div role="group" aria-label="Your grid" className="flex flex-col rounded-2xl border border-line bg-background px-3.5 pt-1 pb-1.5">
      <div className={`grid ${track} border-b border-line pt-3 pb-2.5`}>
        {columns.map((column) => (
          <span key={column} className="text-center font-display text-small font-semibold whitespace-nowrap text-text-2">
            {column}
          </span>
        ))}
      </div>
      {rows.map((row, rowIndex) => {
        const missed: string[] = [];
        const extra: string[] = [];
        return (
          <div key={rowIndex} className="flex flex-col gap-0.5 border-b border-line pt-3 pb-1.5 last:border-0">
            <span className="text-body text-pretty text-text">{row}</span>
            <div className={`relative grid ${track}`}>
              <span aria-hidden className="absolute inset-x-0 top-1/2 h-px bg-line" />
              {columns.map((column, columnIndex) => {
                const cell = rowIndex * columns.length + columnIndex;
                const on = mine.has(cell);
                const want = truth.has(cell);
                let node = "size-3.5 border-2 border-line bg-background";
                let glyph: boolean | null = null;
                if (revealed) {
                  if (want) {
                    node = "size-5.5 bg-ok text-background";
                    glyph = true;
                  }
                } else if (on && want) {
                  node = "size-5.5 bg-ok text-background";
                  glyph = true;
                } else if (on) {
                  node = "size-5.5 bg-bad text-background";
                  glyph = false;
                  extra.push(column);
                } else if (want) {
                  node = "size-5.5 border-2 border-dashed border-bad bg-background";
                  missed.push(column);
                }
                return (
                  <span
                    key={column}
                    className="relative grid h-12 place-items-center"
                    role="img"
                    aria-label={`${row}, ${column}: ${revealed ? (want ? "on" : "off") : on === want ? (on ? "right" : "off") : on ? "on, should be off" : "missed"}`}
                  >
                    <span className={`grid place-items-center rounded-full ${node}`}>
                      {glyph !== null && <Glyph ok={glyph} size="size-3" />}
                    </span>
                  </span>
                );
              })}
            </div>
            {(missed.length > 0 || extra.length > 0) && (
              <span className="pb-1 text-tag font-bold text-bad">
                {[missed.length > 0 ? `Missed ${missed.join(", ")}.` : "", ...extra.map((c) => `${c} shouldn't be on.`)]
                  .filter(Boolean)
                  .join(" ")}
              </span>
            )}
          </div>
        );
      })}
      {wrongSomewhere && (
        <div className="flex flex-wrap gap-x-4 gap-y-2 border-t border-line pt-3 pb-2 text-tag text-text-2">
          <span className="flex items-center gap-2">
            <span className="grid size-4 place-items-center rounded-full bg-ok text-background">
              <Glyph ok size="size-2.5" />
            </span>
            Right
          </span>
          <span className="flex items-center gap-2">
            <span className="grid size-4 place-items-center rounded-full bg-bad text-background">
              <Glyph ok={false} size="size-2.5" />
            </span>
            On, shouldn&apos;t be
          </span>
          <span className="flex items-center gap-2">
            <span className="size-4 rounded-full border-2 border-dashed border-bad" />
            Missed
          </span>
        </div>
      )}
    </div>
  );
}

function NumberReview({ value, correct, tolerance }: { value: number; correct: number; tolerance: number }) {
  const ok = Math.abs(value - correct) <= tolerance;
  return (
    <div role="group" aria-label="Your answer" className="flex flex-col gap-3">
      <div
        className={`flex h-18 items-center justify-between gap-3 rounded-2xl border bg-background px-5 ${ok ? "border-ok" : "border-bad"}`}
      >
        <span className="tabular font-display text-display font-semibold text-text">{value}</span>
        <MarkLine ok={ok}>{ok ? "In range" : "Out of range"}</MarkLine>
      </div>
      {!ok && (
        <div className="flex items-center justify-between gap-3 rounded-xl bg-surface-2 px-5 py-3">
          <span className="text-tag font-bold tracking-wider text-mute uppercase">Answer</span>
          <span className="flex items-baseline gap-2">
            <span className="tabular font-display text-title font-semibold text-text">{correct}</span>
            <span className="text-small text-text-2">{tolerance > 0 ? `within ${tolerance}` : "exactly"}</span>
          </span>
        </div>
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
  promptMd,
}: {
  content: CardOptions | null;
  submitted: Answer | null;
  correct: CorrectAnswer | null;
  primitive: string | null;
  /** The card's explanation, shown inline under the right line for tap_in_place. */
  explanation: string;
  promptMd: string;
}) {
  if (!correct) return null;
  // A number card has no options to redraw: its answer is the display itself.
  if (correct.shape === "number") {
    return submitted?.shape === "number" ? (
      <section className="flex flex-col gap-2.5">
        <NumberReview value={submitted.value} correct={correct.value} tolerance={correct.tolerance} />
      </section>
    ) : null;
  }
  if (!content) return null;
  // No submission: the reader asked to be shown. Draw the right answer on its own.
  const revealed = submitted === null;

  const body = (() => {
    if (correct.shape === "chosen") {
      const picked = submitted?.shape === "chosen" ? submitted.picked : [];
      if (content.shape === "list") {
        return primitive === "tap_in_place" ? (
          <TapReview items={content.items} picked={picked} correct={correct.picked} explanation={explanation} promptMd={promptMd} />
        ) : (
          <PickReview items={content.items} picked={picked} correct={correct.picked} />
        );
      }
      if (content.shape === "grid") {
        return <GridReview rows={content.rows} columns={content.columns} picked={picked} correct={correct.picked} revealed={revealed} />;
      }
      return null;
    }
    if (correct.shape === "ordered") {
      const given = submitted?.shape === "ordered" ? submitted.order : null;
      if (content.shape === "list") {
        const order = given ?? sampleOrder(content.items.length, correct.constraints) ?? content.items.map((_, i) => i);
        return <OrderReview items={content.items} order={order} constraints={correct.constraints} revealed={revealed} />;
      }
      if (content.shape === "assemble") {
        return (
          <AssembleReview
            tokens={content.tokens}
            fixed={content.fixed}
            order={given ?? content.tokens.map((_, i) => i)}
            constraints={correct.constraints}
            revealed={revealed}
          />
        );
      }
      return null;
    }
    if (correct.shape === "mapping") {
      const pairs = submitted?.shape === "mapping" ? submitted.pairs : [];
      if (content.shape === "list") return <ClaimReview items={content.items} pairs={pairs} correct={correct.pairs} />;
      if (content.shape === "match") {
        return <MatchReview left={content.left} right={content.right} pairs={pairs} correct={correct.pairs} revealed={revealed} />;
      }
      if (content.shape === "bucket") {
        return <BucketReview items={content.items} columns={content.columns} pairs={pairs} correct={correct.pairs} revealed={revealed} />;
      }
    }
    return null;
  })();

  if (!body) return null;
  return <section className="flex flex-col gap-2.5">{body}</section>;
}
