# Part D — session selection and difficulty

**Branch** `feed-v2-selection` · **Worktree** `../90X-wt-fv2/d` · **No Playwright spec** — the
proof is a Vitest test over the pure selection function.

Read `.planning/feed-v2/plans/README.md` first. Depends on **B** (the answer shapes, for rolling
accuracy). Runs in parallel with C1/C2/C3.

D gives a session a deliberate difficulty mix instead of "whatever FSRS surfaces": rolling
accuracy over the last ~20 answers, target 70–85% correct, `profiles.level` as the starting
point. The reader's toggle **shifts the mix, never filters it** — no card becomes unreachable,
and FSRS scheduling is untouched.

## Scope

- A pure function that maps (rolling accuracy, level, toggle) → an Easy/Medium/Hard share.
- The queue refill biases the pool toward that share.
- A reader toggle ("Harder / Standard / Easier") that shifts the share, living beside
  `topic-toggle.tsx`.
- The `observed_attempts`/`observed_correct` columns (Part A) become the calibration source once
  n ≥ 20; the rubric label is used until then.

## Files

**Create**
- `web/src/lib/feed/difficulty.ts` — the pure mix function + its test.
- `web/src/components/feed/difficulty-toggle.tsx` — the reader toggle.

**Modify**
- `web/src/lib/feed/service.ts` — `pools()`/`refill()` bias by the difficulty mix.
- `web/src/lib/feed/queue.ts` — `buildQueue` takes a difficulty share (additive, keep the topic
  no-two-in-a-row rule).
- `web/src/lib/feed/view.ts` — `CardView` already carries `difficulty`; read `profiles.level`
  into the session view or a new server read.
- `web/src/app/actions/feed.ts` — a `saveDifficultyPreference` action and a `getDifficulty`
  read, mirroring `saveFeedAreas`.
- `web/src/components/feed/feed.tsx` — render the toggle in the header next to `TopicToggle`.

## Reuse, do not rewrite

```
// service.ts — today
async function pools(userId, areas, now, q);      // due/weak/fresh pools — bias here
async function refill(userId, areas, shownTopic, now, q, store, below?);
export async function nextCard(userId, q?, store?, now?);
export async function setFeedAreas(userId, areas, q?, store?);   // the precedent for the new preference

// queue.ts — today
export function buildQueue(input: { weak; due; fresh; size?; lastTopic? }): QueueItem[];

// view.ts — today
export type FeedArea; export const FEED_AREAS; export const AREA_LABEL;
export function parseFeedAreas(value: unknown): FeedArea[];

// profiles.level — already in the schema (Part A did not change it); read over the Drizzle conn
// topic-toggle.tsx — the precedent for the header toggle (Popover + chip)
```

`profiles.feedTopics` is `{ areas }` jsonb; store the difficulty preference the same way
(append a key, e.g. `profiles.feed_topics.difficulty: "harder" | "standard" | "easier"`), so the
existing `setFeedAreas` write path is the template rather than a new column.

## The pure function — the heart of D

```ts
// web/src/lib/feed/difficulty.ts
export type DifficultyMix = { easy: number; medium: number; hard: number }; // shares sum to 1
export type DifficultyPreference = "harder" | "standard" | "easier";
export function difficultyMix(
  rollingAccuracy: number | null,      // last ~20 graded answers; null = no data yet
  level: "first_time" | "some_practice" | "ready" | null,
  preference: DifficultyPreference,
): DifficultyMix;
```

`standard` targets ~75%: a reader well above 85% gets a harder mix, one near 50% an easier one.
`level` seeds the mix before any answers exist. `harder`/`easier` shift the shares but **never
push any share to zero** — every difficulty stays reachable.

## Tests — named cases (Vitest, pure)

- **95% vs 50% accuracy** — the same seed serves a measurably harder mix to the 95% reader than
  the 50% reader; assert `hard(95%) > hard(50%)` and `easy(50%) > easy(95%)`.
- **no data yet** — `null` accuracy falls back to `level`: `ready` harder than `first_time`.
- **the toggle shifts, never filters** — `harder` raises `hard` and lowers `easy`, but both stay
  `> 0`; same for `easier` in the other direction.
- **bounds** — every returned mix sums to 1 within 1e-9, and every share is in `[0, 1]`.
- **queue integration** — `buildQueue` with a hard-heavy mix emits more hard cards and still
  never two cards in a row on the same topic (the existing `queue.test.ts` property).

## Traps

- **Never filter.** The toggle and the mix change probabilities, not membership. A card the mix
  deprioritises must still be reachable — otherwise you have rebuilt a filter and the
  "nothing left" empty state lies.
- **FSRS is untouched.** `srs.ts` and `cardState` scheduling are not yours; you bias which cards
  enter the queue, not their intervals.
- **`observed_attempts`/`observed_correct` are global, not per-user.** The calibration ("above
  85% correct it is Easy") reads the card's aggregate rate, not this reader's. Use them only as a
  per-card prior, never to gate this reader's queue.
- **Rolling accuracy counts `correct`/`wrong` only** — skip, `new_to_me`, `known` carry no
  performance signal (`isGraded` already encodes this; reuse it).
- **Do not touch `card.tsx`, the C parts' files, `check-*.ts`, or `ci.yml`.** The toggle is a
  new header action beside `TopicToggle`, not inside the card.

## Verification

Full README list. No new Playwright spec, but run `e2e/feed.spec.ts` to confirm the queue change
did not break it. Screenshots at 390px and 1440px of the Feed header with the toggle open.
Report token count and bundle KB.

## Decisions (with cost if wrong)

- **Preference stored inside `profiles.feed_topics` rather than a new column.** Cost if wrong:
  `parseFeedAreas` must learn to ignore the extra key (it reads `.areas`), and a future column
  split is a one-line migration. This avoids a migration D was not given.
- **The mix biases the pool, not the queue order.** Cost if wrong: reordering the queue breaks
  the no-two-in-a-row guarantee and the due-before-new priority; biasing the pool keeps both.
