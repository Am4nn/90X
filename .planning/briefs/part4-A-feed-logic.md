# Brief A — Feed pure logic (Part 4, Tasks 3–5, 8 pure parts)

You are building pure, unit-tested TypeScript modules for the 90x Feed. Another engineer is building the server and UI in parallel against **exactly the interfaces below** — do not rename or reshape them.

**Read `.planning/briefs/README.md` first** — it has how we write code, verify, open PRs, and when to ask. This brief adds only what is specific to this task.

## Setup and rules

- Repo root has `web/` (Next.js 16, Bun). Work in `web/`. Run `bun install`.
- Branch: `feed-logic` from `main`. Open a pull request to `main` when done; do not merge.
- No secrets, no database, no network calls in code or tests. Pure functions only (plus the `ts-fsrs` dependency).
- TDD: write each test file first, run it, see it fail, then implement. Tests are Vitest, next to the code (`*.test.ts`).
- Before the PR, all of these must pass in `web/`: `bun run typecheck`, `bun run lint`, `bun run test`, `bun run format:check` (run `bunx oxfmt` to fix), `bun run check:dead`, `bun run check:tokens`.
  - `check:dead` (knip) flags unused exports: these modules are consumed later, so add a single line per file to `web/knip.json` `ignore` only if knip complains, and say so in the PR.
- Read first: `.planning/plans/2026-09-27-part4-feed.md` (Decisions section is binding), `.planning/SPEC.md` §6.3 and §6.4, and `web/src/lib/tracker/*.ts` for house style (small pure functions, short comments that explain why, no `any`, `noUncheckedIndexedAccess` is on).
- Commit messages end with:
  ```
  Co-Authored-By: Claude <noreply@anthropic.com>
  ```

## Modules and exact interfaces (all in `web/src/lib/feed/`)

### `grade.ts`
```ts
export type CardFormat = "typed" | "flash" | "mcq" | "output" | "bug";
export type CardForGrading = { format: CardFormat; answer: string; keyPoints: string[]; options: string[] | null };
export const PASS_MARK = 0.7;
export const OPTIONS_SCORE = 0.7; // correct pick after "Show options"
export function normalize(text: string): string;              // lowercase, strip markdown (`*_~>#[]()`), code fences, punctuation, collapse whitespace, trim
export function exactMatch(answer: string, card: CardForGrading): boolean; // normalized answer === normalized card.answer, OR every normalized key point is a substring of the normalized answer (needs ≥1 key point)
export function gradeOutput(answer: string, card: CardForGrading): number; // 1 if normalize(answer) === normalize(card.answer), ignoring all whitespace differences; else 0
export function gradeOption(choice: number, card: CardForGrading): number; // OPTIONS_SCORE if options[choice] normalizes equal to card.answer (or card.answer is that option's letter "A"/"B"/… / index), else 0; 0 when options is null or choice out of range
export type Outcome = "correct" | "wrong" | "skipped";
export function outcomeOf(score: number, skipped: boolean): Outcome;       // skipped → "skipped"; score ≥ PASS_MARK → "correct"; else "wrong"
export type Rating = 1 | 2 | 3 | 4;                                        // Again, Hard, Good, Easy (same numbers as ts-fsrs Rating)
export function scoreToRating(score: number, skipped: boolean): Rating;    // skipped or < 0.7 → 1; 0.7–0.849 → 2; 0.85–0.999 → 3; 1 → 4
export function keyPointScore(hits: boolean[]): number;                    // hits.filter(Boolean).length / hits.length; 0 for empty
```
Tests must cover: markdown/punctuation noise, key-point substring match, output whitespace/newline differences, option by text and by letter, boundary scores 0.699/0.7/0.85/1.

### `srs.ts` (add dependency `ts-fsrs` with `bun add ts-fsrs`)
```ts
export type SrsState = { stability: number; difficulty: number; dueAt: Date; reps: number; lapses: number; state: number; lastReview: Date | null };
export function nextState(prev: SrsState | null, rating: Rating, now: Date): SrsState; // null = new card; wraps ts-fsrs `fsrs()` with default params, enable_fuzz false (deterministic)
export function isDue(state: SrsState | null, now: Date): boolean;                     // null → false (new cards are not "due", they're "new")
```
Tests: new card rated Good is due in the future; Again on a reviewed card increments lapses and makes it due sooner than Good would; Easy's due date is later than Good's.

### `queue.ts`
```ts
export type QueueCard = { id: string; topic: string; area: string };
export type QueueReason = "weak" | "due" | "new";
export type QueueItem = { id: string; reason: QueueReason };
export function buildQueue(input: {
  weak: QueueCard[];  // weakest topics' cards first
  due: QueueCard[];   // most overdue first
  fresh: QueueCard[]; // never-seen cards, priority order
  size?: number;      // default 30
  lastTopic?: string; // topic of the card the user just saw
}): QueueItem[];
```
Rules: target mix 50% weak / 30% due / 20% new (for 30: 15/9/6); if a pool runs short, fill from the others in order weak → due → new; never the same card twice (a card may sit in several pools — first pick wins); never two consecutive items with the same topic when any other ordering is possible (including against `lastTopic` for the first item); preserve each pool's order otherwise; deterministic. Tests for: exact mix, shortfall backfill, dedupe across pools, topic alternation, a single-topic input (then repeats are allowed), empty input → `[]`.

### `diagnostic.ts`
```ts
export const DIAGNOSTIC_AREAS = ["dsa", "system_design", "cs", "java", "sql"] as const;
export function pickDiagnostic(pool: { id: string; area: string; difficulty: "Easy" | "Medium" | "Hard" | null; topic: string }[], perArea?: number, seed?: number): string[];
```
Rules: default 4 per area; within an area prefer one Easy, two Medium, one Hard (fill from any difficulty when missing); no two cards from the same topic within an area when avoidable; output interleaves areas (dsa, system_design, cs, java, sql, dsa, …); deterministic for a given seed (use a tiny seeded PRNG, e.g. mulberry32, not `Math.random`). Areas with no cards are skipped.

### `review-sample.ts`
```ts
export const SAMPLE_SIZE = 20;
export const PASS_AT = 18;
export function pickReviewSample(cards: { id: string; risk: number | null }[], seed: number, size?: number): string[]; // half (rounded up) = lowest `risk` first (null risk counts as 1.0, i.e. safest), rest = seeded-random from the remainder; no duplicates; fewer cards than size → all of them
export function batchVerdict(verdicts: ("good" | "bad")[], size?: number, passAt?: number): "pending" | "published" | "rejected"; // pending until `size` verdicts (or all cards if the batch is smaller than size, pass `size` accordingly); published if goods ≥ passAt scaled: ceil(passAt/size * n)
```

## Definition of done

- The five modules and their tests exist with the exact exports above.
- All checks listed in Setup pass.
- PR description: what each module does, any rule you had to interpret, and the check results.
