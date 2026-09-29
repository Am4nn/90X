# Part B — the grader, pure

**Branch** `feed-v2-grader` · **Worktree** `../90X-wt-fv2/b` · **Spec** rewrites `e2e/feed.spec.ts`.

Read `.planning/feed-v2/plans/README.md` first. Depends on **A** (the `archetypes.ts` module and
the `archetype`/answer columns it defines). Do not start until A is merged.

B removes typed from the Feed. Every Feed answer is now marked by a pure function; `gradeWithAi`
stays in `grader.ts` for mocks and reviews and leaves every Feed path. This part is all pure
functions and must be the best-tested code in the app.

## Scope

Rewrite the grading layer to route by **primitive** (from `@/lib/feed/archetypes`), implement
one pure grader per shape, grade orderings against **constraints**, grade numbers by
`|given − expected| <= tolerance`, and enforce the why-step rule (both halves right, or wrong).
Update the answer input/output contract, the service's `grade()` path, the minimal card UI to
send the new shapes, and the e2e seed + spec so the Feed keeps working on the new contract.

## Files

**Modify**
- `web/src/lib/feed/grade.ts` — `CardFormat` goes; add the four `Answer` shapes, the
  `CardAnswer` (per-shape correct-answer fields), and pure graders.
- `web/src/lib/feed/grader.ts` — `gradeWithAi` stays exported; it is no longer imported by the
  Feed path (nothing to change in the function itself unless you trim now-dead imports).
- `web/src/lib/feed/view.ts` — `AnswerInput` gains the four shapes (+ optional `why`); `CardView`
  carries `primitive`, `archetype`, and the answer-definition the UI needs (options, options per
  shape, `whyStep`).
- `web/src/lib/feed/service.ts` — `grade()` routes by primitive; `gradeAndSave()` serialises the
  structured answer into `card_reviews.answer`; remove the `gradeWithAi` import/use.
- `web/src/components/feed/card.tsx` — dispatch on `card.primitive`; remove the typed textarea and
  "Show options" fallback; submit the four shapes.
- `web/e2e/seed-data.ts` — re-cast the live cards to `pick_one` (chosen) and `self_rate`; no
  `typed`, no `output`.
- `web/e2e/feed.spec.ts` — replace the typed/output assertions with the new shapes.

**Create**
- `web/src/lib/feed/grade.test.ts` — the named cases below.
- `web/src/components/feed/primitive/` with `pick-one.tsx`, `self-rate.tsx` (you implement),
  `not-built.tsx`, and stubs `order.tsx`, `match.tsx`, `bucket.tsx`, `tap-in-place.tsx`,
  `assemble.tsx`, `numeric.tsx`, `claim-grid.tsx`, `grid-toggle.tsx` — each stub exports a
  component rendering `<NotBuilt/>`. This is the seam that lets C1/C2/C3 own disjoint files;
  `card.tsx`'s switch already references all ten, so no C part ever edits `card.tsx`'s dispatch.

## Reuse, do not rewrite

```
// grade.ts — today (you are replacing these; keep outcomeOf / scoreToRating / isGraded / Outcome / Rating)
export type Outcome = "correct" | "wrong" | "skipped" | "new_to_me" | "known";
export const isGraded = (outcome: string): boolean => outcome === "correct" || outcome === "wrong";
export type Rating = 1 | 2 | 3 | 4;
export const PASS_MARK = 0.7;
export function outcomeOf(score: number, skipped: boolean): Outcome;
export function scoreToRating(score: number, skipped: boolean): Rating;

// srs.ts — untouched
export function nextState(prev: SrsState | null, rating: Rating, now: Date): SrsState;

// view.ts — today (you widen these)
export type AnswerInput = ({ cardId; answer } | { cardId; choice } | { cardId; skipped }
  | { cardId; selfMark: "got"|"missed"; answer? } | { cardId; declare }) & { clientId?: string };
export function cardView(row, reason, diagnostic, canDeclareKnown): CardView | null;
export function sourceLinks(value): SourceLink[];

// service.ts — today (you change grade() and gradeAndSave() only)
async function grade(userId, input, card): Promise<Graded | { needsSelfMark: true }>;
async function gradeAndSave(userId, input, q, store, now): Promise<AnswerResult | ...>;
export async function answerCard(userId, input, q?, store?, now?): Promise<AnswerResult | ...>;

// archetypes.ts — from Part A (consume, never edit)
export function shapeOf(primitive: Primitive): AnswerShape | null;
export function archetype(id: ArchetypeId): ... | undefined;
```

`card.tsx` today submits `{ cardId, answer }` / `{ cardId, choice }` / `{ cardId, selfMark }`;
you keep the `submit`/`useServerAction`/offline `saveForLater` skeleton and change only the
answer it builds. `PRIMARY`/`SECONDARY` from `@/components/button-styles`, `Markdown` from
`@/components/markdown`, `areaDot` from `@/lib/admin/review`.

## The pure graders (the contract)

One function per shape, all total and deterministic. Ordering grades against **constraints** —
every genuinely correct order passes, not one blessed sequence (DECISIONS round 2). Numeric
grades `|given − expected| <= tolerance`. Mapping requires an exact one-to-one match. Chosen
requires the exact set. The why-step is a second `chosen`: **both halves right, or the card is
wrong.**

```ts
export type Answer =
  | { shape: "chosen";  picked: number[] }
  | { shape: "ordered"; order: number[] }
  | { shape: "mapping"; pairs: [number, number][] }
  | { shape: "number";  value: number };

// card.whyStep ? { options, correct } : null — present only on Hard cards (pipeline's job).
export function gradeCard(card: CardAnswer, answer: Answer & { why?: number }): 0 | 1;
```

## Tests — named cases (Vitest, pure)

- **chosen** — exact set correct; subset wrong; superset wrong; empty wrong; `why` missing on a
  card that has a `whyStep` is wrong; `why` correct + answer correct is right.
- **right-answer-wrong-reason** — answer correct but `why` wrong → `gradeCard` returns 0. This is
  the decision under review at Gate 3; the test pins the current behaviour so it is visible when
  it changes.
- **ordered, two valid orderings** — a card whose constraints permit `[a,b,c]` and `[b,a,c]`
  accepts both; a third that violates the constraint is wrong. This is the two-valid-orderings
  case PLAN.md names.
- **mapping** — exact one-to-one match right; one pair wrong right, all wrong; a pair pointing at
  two targets rejected at the type level (use the tuple type).
- **number, boundary at exactly the tolerance** — `expected=10, tolerance=0.5`: `10.5` right,
  `10.500001` wrong, `9.5` right, `9.499999` wrong.
- **self_rate** — `got` → 1, `missed` → 0, and neither reaches the numeric/chosen paths.
- **outcome/rating** — keep the existing `outcomeOf`/`scoreToRating` tests green; a 1 (wrong) and
  a 0-score never count as "correct".

The existing `grade.test.ts` already has cases for `normalize`, `exactMatch`, `gradeOutput`,
`correctOptionIndex`, `gradeOption`, `keyPointScore`, `outcomeOf`, `scoreToRating`. Delete the
typed/output/mcq ones as you delete the functions; keep `outcomeOf`/`scoreToRating`/`isGraded`.

## Traps

- **`gradeWithAi` must stay in `grader.ts` and stay exported.** Mocks and the Coach call it.
  Remove it from `service.ts` only. `web/scripts/check-grading.ts` (the orchestrator's) still
  imports it and must keep compiling.
- **You do not touch `web/scripts/check-feed.ts`.** The orchestrator extends it after you land.
  Your database-level proof is `feed.spec.ts` + the existing `check:feed` still passing.
- **The `AnswerInput` union is strict-zod-validated in `app/actions/feed.ts`.** Widen the zod
  schema there in lockstep with `view.ts`, or every answer 400s. Add `why` as optional on the
  four shaped shapes only.
- **`card_reviews.answer` is text.** Serialise the structured answer as JSON; keep
  `answer.slice(0, MAX_ANSWER_CHARS)` for the legacy bound or drop it deliberately and say so.
- **`cardView` must never leak the answer.** It already returns options-but-not-answer; keep the
  same split now that options live per shape.
- **The seed drives `feed.spec.ts`.** Re-cast `LIVE_CARDS` (in `seed-data.ts`) to `pick_one`
  chosen sets and `self_rate`; the "output" card becomes a pick-one. Do not add numeric/order/etc
  — those are C2/C3's to seed.
- **`card.tsx` must keep the reload-re-serves-same-card and offline-save paths.** Do not break
  `nextCard`'s `currentKey` semantics or the offline outbox; the spec still asserts them.

## Verification

Full README list. Run `e2e/feed.spec.ts` with `--retries=0` at least three times. Also run
`bun run check:feed` (should still pass — the migration is additive and the seed still answers).
Report the token count and bundle KB. The grader is the one place where "no test passes on a
retry" must be visibly true: run the Vitest suite three times too.

## Decisions (with cost if wrong)

- **B stubs the eight not-yet-built primitives rather than leaving a hole in the dispatch.**
  Cost if wrong: none — C1/C2/C3 replace the stubs in place. This is what keeps them parallel.
- **B does not render the why-step UI; it implements the why-step grading.** The UI is C3's.
  Cost if wrong: a Hard card cannot be answered end-to-end until C3 lands, which is the planned
  order.
- **Ordering constraints are expressed as a list of required `before` pairs** unless the card
  needs richer constraints; Part A's `constraints` jsonb is your freedom. Cost if wrong: an
  ordering card with a free clause order marks a correct answer wrong — the exact bug PRIMITIVES
  warns about, so test it.
