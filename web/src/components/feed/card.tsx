"use client";

import { useEffect, useRef, useState } from "react";
import { type AnswerState, retireTopicAction, submitAnswer } from "@/app/actions/feed";
import { PRIMARY } from "@/components/button-styles";
import { useServerAction } from "@/components/form";
import { Markdown } from "@/components/markdown";
import type { Answer } from "@/lib/feed/grade";
import {
  AREA_LABEL,
  AREA_TEXT,
  type FeedArea,
  type AnswerInput,
  type AnswerResult,
  type CardView,
  nextReviewText,
  scoreLine,
  type SessionStats,
  verdictText,
} from "@/lib/feed/view";
import { dropCard, queueAnswer } from "@/lib/offline/store";
import { CardFooter } from "./footer";
import { Assemble } from "./primitive/assemble";
import { Bucket } from "./primitive/bucket";
import { SkipContext } from "./primitive/check-bar";
import { ClaimGrid } from "./primitive/claim-grid";
import { Compose } from "./primitive/compose";
import { GridToggle } from "./primitive/grid-toggle";
import { Glyph } from "./primitive/marks";
import { Match } from "./primitive/match";
import { NotBuilt } from "./primitive/not-built";
import { Numeric } from "./primitive/numeric";
import { Order } from "./primitive/order";
import { PickOne } from "./primitive/pick-one";
import { AnswerReview } from "./primitive/review";
import { SelfRate } from "./primitive/self-rate";
import { TapInPlace } from "./primitive/tap-in-place";
import type { PrimitiveAnswerProps } from "./primitive/types";
import { WhyStep } from "./primitive/why-step";
import { TodayBlock, WhyBlock } from "./side";

/** The main answer held between the two screens of a why-step card. */
type WhyMain = Answer & { cardId: string; why?: number };

type Phase =
  | { kind: "ask" }
  | { kind: "why"; main: WhyMain; choice: number | null }
  | { kind: "result"; result: AnswerResult; choice: number | null; nextReview: string }
  /** A written answer the model could not mark, so the reader marks it. Reached
   *  when the grade's rate limit trips or the model's output is unusable. */
  | { kind: "selfMark"; answer: string }
  /** Answered offline: stored on this device until it can be graded. */
  | { kind: "saved" };

type Busy = "check" | "skip" | "self" | "new_to_me" | "known" | null;

/** The pill names the whole area where the toggles use a short form. */
const AREA_PILL: Partial<Record<FeedArea, string>> = { system_design: "System design" };

/** Quiet text links under the answer: choices about the card, not answers. */
const QUIET = "text-small font-medium text-mute underline decoration-line-2 underline-offset-4 hover:text-text-2 disabled:opacity-60";

/** These primitives end in the shared Check bar, which carries Skip beside it. */
const HAS_CHECK_BAR = new Set([
  "pick_one",
  "tap_in_place",
  "numeric",
  "compose",
  "order",
  "match",
  "bucket",
  "assemble",
  "claim_grid",
  "grid_toggle",
]);

const isTyping = (target: EventTarget | null) =>
  target instanceof HTMLElement && (target.isContentEditable || ["INPUT", "TEXTAREA", "BUTTON", "A"].includes(target.tagName));

/** The answer area for a card, dispatched by primitive so each C part owns one
 *  file and never edits this switch. */
function AnswerArea(props: PrimitiveAnswerProps) {
  switch (props.card.primitive) {
    case "pick_one":
      return <PickOne {...props} />;
    case "self_rate":
      return <SelfRate {...props} />;
    case "order":
      return <Order {...props} />;
    case "match":
      return <Match {...props} />;
    case "bucket":
      return <Bucket {...props} />;
    case "tap_in_place":
      return <TapInPlace {...props} />;
    case "assemble":
      return <Assemble {...props} />;
    case "numeric":
      return <Numeric {...props} />;
    case "claim_grid":
      return <ClaimGrid {...props} />;
    case "grid_toggle":
      return <GridToggle {...props} />;
    case "compose":
      return <Compose {...props} />;
    default:
      // A legacy typed/mcq/output card that has not been regenerated yet.
      return <NotBuilt />;
  }
}

/**
 * One card from question to result. Keyed by card id, so every card starts
 * fresh. The question stays put while the answer area turns into the result.
 * Offline, the answer is stored on the device instead and graded on reconnect.
 */
export function FeedCard({
  card,
  userId,
  session,
  onAnswered,
  onNext,
  nextPending,
  nextError,
}: {
  card: CardView;
  userId: string;
  /** Today's running numbers, shown on a phone only once the card is answered. */
  session: SessionStats;
  onAnswered: (session: SessionStats) => void;
  /** Null after an answer saved offline: there is no result to show yet. */
  onNext: (result: AnswerResult | null) => void;
  nextPending: boolean;
  nextError: string | null;
}) {
  const { run, pending, error } = useServerAction({ refresh: false });
  const [phase, setPhase] = useState<Phase>({ kind: "ask" });
  const [busy, setBusy] = useState<Busy>(null);
  const nextRef = useRef<HTMLButtonElement>(null);

  const saveForLater = async (input: AnswerInput & { clientId: string }) => {
    const saved = await queueAnswer({ clientId: input.clientId, userId, input, queuedAt: Date.now() });
    if (!saved) return { error: "Your answer couldn't be saved on this device. Try again when you're online." };
    setPhase({ kind: "saved" });
  };

  /** Offline, the reason is asked before the answer is queued, so the queued copy
   *  carries both halves and grades in one go on reconnect. */
  const submitOffline = (input: AnswerInput, choice: number | null, sent: AnswerInput & { clientId: string }) => {
    if (card.whyOptions && "shape" in input && !("why" in input)) {
      setPhase({ kind: "why", main: input, choice });
      return;
    }
    return saveForLater(sent);
  };

  const submit = (label: NonNullable<Busy>, input: AnswerInput, choice: number | null = null) => {
    setBusy(label);
    // One id per answer: if the connection drops mid-send, the queued copy
    // carries the same id and the server grades it once.
    const sent = { ...input, clientId: crypto.randomUUID() };
    run(async () => {
      if (!navigator.onLine) return submitOffline(input, choice, sent);
      let state: AnswerState;
      try {
        state = await submitAnswer(sent);
      } catch (e) {
        if (!navigator.onLine) return submitOffline(input, choice, sent);
        throw e;
      }
      if ("error" in state) return state;
      if ("duplicate" in state) return { error: "That answer is already saved. Go to the next card." };
      // A written answer the grader could not mark: the rate limit tripped, or the
      // model returned something unusable. The reader has already typed two or
      // three sentences, so an error and a Skip button throws that away - they
      // mark it themselves against the rubric instead, which is the fallback
      // `gradeWithAi` returns `selfMark` for in the first place.
      if ("needsSelfMark" in state) {
        if ("answer" in input && typeof input.answer === "string" && input.answer) {
          setPhase({ kind: "selfMark", answer: input.answer });
          return;
        }
        return { error: "This card can't be graded. Skip it to move on." };
      }
      // A correct main answer on a why-step card: ask for the reason before the
      // answer is recorded, so the card is graded once with both halves.
      if ("needsWhyStep" in state) {
        if ("shape" in input) setPhase({ kind: "why", main: input, choice });
        return;
      }
      onAnswered(state.session);
      void dropCard(userId, card.id);
      // Skip means "not now": straight to the next card, the answer unseen.
      // "New to me" is how a reader asks to be shown it.
      if (label === "skip") {
        onNext(state.result);
        return;
      }
      setPhase({ kind: "result", result: state.result, choice, nextReview: nextReviewText(state.result.nextDue, new Date()) });
    });
  };

  const onSubmit = (input: AnswerInput, choice: number | null = null) => {
    const label: NonNullable<Busy> = "shape" in input || "answer" in input ? "check" : "selfMark" in input ? "self" : "skip";
    submit(label, input, choice);
  };

  const result = phase.kind === "result" ? phase.result : null;
  const finished = phase.kind === "result" || phase.kind === "saved";

  useEffect(() => {
    if (finished) nextRef.current?.focus({ preventScroll: true });
  }, [finished]);

  // Enter on the result goes to the next card (desktop), unless focus is in a field or on a control.
  useEffect(() => {
    if (!finished) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key !== "Enter" || e.isComposing || isTyping(e.target)) return;
      e.preventDefault();
      onNext(result);
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [finished, result, onNext]);

  const label = busy && pending ? busy : null;

  return (
    <>
      <article className="flex flex-col gap-5 rounded-2xl border border-line bg-surface p-5 md:p-7">
        {phase.kind === "result" && (
          <div className="flex flex-col gap-4 border-b border-line pb-4">
            <Verdict
              outcome={phase.result.outcome}
              detail={phase.result.pointsHit?.length ? `${scoreLine(phase.result)}, pass mark 70%` : null}
            />
          </div>
        )}
        <header className="flex flex-col gap-3">
          <div className="flex items-center justify-between gap-3">
            <span className="flex min-w-0 items-center gap-2.5">
              <span
                className={`inline-flex h-6 shrink-0 items-center rounded-full border border-line-2 px-2.5 text-tag font-bold ${AREA_TEXT[card.topic.area]}`}
              >
                {AREA_PILL[card.topic.area] ?? AREA_LABEL[card.topic.area]}
              </span>
              <span className="truncate text-small font-semibold text-text">{card.topic.name}</span>
            </span>
            {card.diagnostic ? (
              <span className="tabular shrink-0 text-small text-mute">
                Diagnostic {card.diagnostic.index} of {card.diagnostic.total}
              </span>
            ) : (
              card.difficulty && <span className="shrink-0 text-tag font-bold text-text-2 capitalize">{card.difficulty}</span>
            )}
          </div>
          {card.diagnostic && (
            <div className="h-1 overflow-hidden rounded-full bg-surface-2" aria-hidden>
              <div className="h-full rounded-full bg-cyan" style={{ width: `${(card.diagnostic.index / card.diagnostic.total) * 100}%` }} />
            </div>
          )}
        </header>

        <div className="font-sans text-heading leading-normal font-semibold [&_p]:text-text">
          <Markdown>{card.promptMd}</Markdown>
        </div>

        {phase.kind === "ask" && (
          <div className="flex flex-col gap-4">
            <SkipContext.Provider
              value={{ pending, skipping: label === "skip", skip: () => submit("skip", { cardId: card.id, skipped: true }) }}
            >
              <AnswerArea card={card} pending={pending} busy={label} onSubmit={onSubmit} />
            </SkipContext.Provider>

            {/* The two things a card cannot work out about its reader. "New to me"
              is always offered: only they know whether they have met this idea.
              "I already know this" is earned, so it appears once they have a
              real record on the topic. */}
            <div className="flex flex-wrap items-center justify-center gap-x-5 gap-y-2">
              {!(card.primitive && HAS_CHECK_BAR.has(card.primitive)) && (
                <button
                  type="button"
                  disabled={pending}
                  aria-busy={label === "skip" || undefined}
                  onClick={() => submit("skip", { cardId: card.id, skipped: true })}
                  className={QUIET}
                >
                  {label === "skip" ? "Skipping…" : "Skip"}
                </button>
              )}
              <button
                type="button"
                disabled={pending}
                aria-busy={label === "new_to_me" || undefined}
                onClick={() => submit("new_to_me", { cardId: card.id, declare: "new_to_me" })}
                className={QUIET}
              >
                {label === "new_to_me" ? "Opening…" : "New to me"}
              </button>
              {card.canDeclareKnown && (
                <button
                  type="button"
                  disabled={pending}
                  aria-busy={label === "known" || undefined}
                  onClick={() => submit("known", { cardId: card.id, declare: "known" })}
                  className={QUIET}
                >
                  {label === "known" ? "Retiring…" : "I already know this"}
                </button>
              )}
            </div>
          </div>
        )}

        {phase.kind === "why" && (
          <WhyStep
            options={card.whyOptions ?? []}
            pending={pending}
            busy={label}
            onSubmit={(why) => submit("check", { ...phase.main, why }, phase.choice)}
          />
        )}

        {phase.kind === "selfMark" && (
          <div className="flex flex-col gap-4">
            <p className="text-small text-text-2">The automatic mark is unavailable. Judge your answer against what it had to cover.</p>
            {(card.rubric?.length ?? 0) > 0 && (
              <ul className="flex flex-col gap-1 rounded-xl border border-line bg-surface-2 px-3.5 py-3">
                {(card.rubric ?? []).map((point) => (
                  <li key={point} className="text-small text-text-2">
                    {point}
                  </li>
                ))}
              </ul>
            )}
            <SelfRate card={card} pending={pending} busy={label} onSubmit={(input) => submit("self", { ...input, answer: phase.answer })} />
          </div>
        )}

        {phase.kind === "result" && (
          <Result
            result={phase.result}
            choice={phase.choice}
            primitive={card.primitive}
            promptMd={card.promptMd}
            onNext={() => onNext(phase.result)}
            nextPending={nextPending}
            nextRef={nextRef}
          />
        )}

        {phase.kind === "saved" && (
          <div className="flex flex-col gap-5">
            <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
              <span role="status" className="text-text-2">
                Saved. It&apos;ll be graded when you&apos;re back online.
              </span>
              <button ref={nextRef} type="button" onClick={() => onNext(null)} className={`w-full md:w-auto ${PRIMARY}`}>
                Next card
              </button>
            </div>
          </div>
        )}

        {(error ?? (phase.kind === "result" ? nextError : null)) && (
          <p role="alert" className="text-small text-bad">
            {error ?? nextError}
          </p>
        )}
      </article>
      {phase.kind === "result" && (
        <>
          <CardFooter card={card} result={phase.result} nextReview={phase.nextReview} />
          {/* On a phone the side blocks follow the answer, never sit between the reader and the question. */}
          <div className="flex flex-col gap-4 md:hidden">
            <TodayBlock session={session} />
            <WhyBlock card={card} />
          </div>
          <div aria-hidden className="h-20 md:hidden" />
        </>
      )}
    </>
  );
}

function Result({
  result,
  choice,
  primitive,
  promptMd,
  onNext,
  nextPending,
  nextRef,
}: {
  result: AnswerResult;
  choice: number | null;
  primitive: CardView["primitive"];
  promptMd: string;
  onNext: () => void;
  nextPending: boolean;
  nextRef: React.RefObject<HTMLButtonElement | null>;
}) {
  return (
    <div className="flex flex-col gap-5">
      {result.retireOffer && <RetireOffer offer={result.retireOffer} />}

      <AnswerReview
        content={result.content}
        submitted={result.submitted}
        correct={result.correct}
        primitive={primitive}
        explanation={result.answerMd}
        promptMd={promptMd}
      />

      {/* The legacy list, for a card with no structured answer to redraw: an
          mcq row that predates the primitives, or a skip, where there is no
          submission to mark. `AnswerReview` returns null in both cases. */}
      {result.options && !result.correct && (
        <ul className="flex flex-col gap-2" aria-label="Options">
          {result.options.map((option, index) => {
            const correct = index === result.correctOption;
            const picked = index === choice;
            return (
              <li
                key={index}
                className={`flex items-start gap-3 rounded-xl border px-4 py-3 ${correct ? "border-ok/50 text-text" : picked ? "border-bad/50 text-text-2" : "border-line text-mute"}`}
              >
                <span className={`font-display font-semibold ${correct ? "text-ok" : picked ? "text-bad" : ""}`}>
                  {correct ? "✓" : picked ? "✕" : String.fromCharCode(65 + index)}
                </span>
                <span>{option}</span>
              </li>
            );
          })}
        </ul>
      )}

      {result.keyPoints.length > 0 && (
        <section className="flex flex-col gap-2.5">
          <h2 className="text-tag font-bold tracking-wider text-mute uppercase">Key points</h2>
          <ul className="flex flex-col gap-2.5 border-l border-line-2 pl-3">
            {result.keyPoints.map((point, index) => {
              const hit = result.pointsHit?.[index];
              return (
                <li key={index} className="grid grid-cols-[20px_1fr] gap-2.5">
                  {hit === undefined ? (
                    <span className="text-mute" aria-hidden>
                      •
                    </span>
                  ) : (
                    <span className={hit ? "text-ok" : "text-bad"} role="img" aria-label={hit ? "Covered" : "Missed"}>
                      {hit ? "✓" : "✕"}
                    </span>
                  )}
                  <span className={hit === false ? "text-text-2" : "text-text"}>{point}</span>
                </li>
              );
            })}
          </ul>
        </section>
      )}

      {/* tap_in_place explains itself inline, under the right line. */}
      {primitive !== "tap_in_place" && (
        <section className="flex flex-col gap-2.5">
          <h2 className="text-tag font-bold tracking-wider text-mute uppercase">Answer</h2>
          <Markdown>{result.answerMd}</Markdown>
        </section>
      )}

      <div className="above-tabbar fixed inset-x-0 z-30 border-t border-line bg-background px-5 py-3 md:static md:z-auto md:border-0 md:bg-transparent md:p-0">
        <button
          ref={nextRef}
          type="button"
          disabled={nextPending}
          aria-busy={nextPending || undefined}
          onClick={onNext}
          className={`w-full md:w-auto ${PRIMARY}`}
        >
          {nextPending ? "Loading…" : result.diagnosticSummary ? "See your results" : "Next card"}
        </button>
      </div>
    </div>
  );
}

/** The first thing a result says: a ring with a glyph, then the word. Colour is never
 *  the only signal. No percentage on a binary verdict; a written answer adds its
 *  key-point count beneath. */
function Verdict({ outcome, detail }: { outcome: AnswerResult["outcome"]; detail: string | null }) {
  const judged = outcome === "correct" || outcome === "wrong";
  const tone = outcome === "correct" ? "border-ok text-ok" : "border-bad text-bad";
  return (
    <div className="flex flex-col gap-1" aria-live="polite">
      <div className="flex items-center gap-3">
        {judged && (
          <span aria-hidden className={`flex size-7 shrink-0 items-center justify-center rounded-full border-2 ${tone}`}>
            <Glyph ok={outcome === "correct"} size="size-3.5" />
          </span>
        )}
        <span className="font-display text-title font-semibold text-text">{verdictText(outcome)}</span>
      </div>
      {detail && <span className="text-small text-text-2">{detail}</span>}
    </div>
  );
}

/** Offered once after "I already know this", because the saving is the rest of
 *  the topic, not the one card. Never taken automatically: retiring eight
 *  cards on one tap is a big, invisible action. */
function RetireOffer({ offer }: { offer: NonNullable<AnswerResult["retireOffer"]> }) {
  const [done, setDone] = useState<number | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  if (done !== null) {
    return (
      <p className="rounded-xl border border-line bg-surface px-4 py-3 text-small text-text-2">
        Retired {done} more {done === 1 ? "card" : "cards"} on {offer.topicName}.
      </p>
    );
  }
  return (
    <div className="flex flex-col gap-2 rounded-xl border border-line bg-surface px-4 py-3">
      <p className="text-small text-text-2">
        You have {offer.remaining} more {offer.remaining === 1 ? "card" : "cards"} on {offer.topicName}.
      </p>
      <button
        type="button"
        disabled={busy}
        onClick={() => {
          setBusy(true);
          setError(null);
          // Always clears busy: a rejected request used to leave the button
          // disabled with nothing said, so the reader could neither tell what
          // happened nor try again.
          retireTopicAction(offer.topicSlug)
            .then((r) => ("retired" in r ? setDone(r.retired) : setError(r.error)))
            .catch(() => setError("That didn't save. Try again."))
            .finally(() => setBusy(false));
        }}
        className="self-start text-small font-semibold text-cyan underline-offset-2 hover:underline disabled:opacity-60"
      >
        {busy ? "Retiring…" : "Retire them too"}
      </button>
      {error && (
        <span role="alert" className="text-small text-bad">
          {error}
        </span>
      )}
    </div>
  );
}
