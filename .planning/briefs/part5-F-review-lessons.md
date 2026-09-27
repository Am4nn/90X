# Brief F — Solution review + pattern lessons (Part 5)

**Read `.planning/briefs/README.md` first**, then the plan `.planning/plans/2026-09-28-part5-coach.md` (Decisions + Foundation are binding) and spec §6.9, §6.11.

Branch: `coach-review` (or your pinned branch). PR to `main`. Brief E builds the chat route/UI in parallel; you build **modes** that plug into it (`lib/coach/mode.ts`) plus your own pages. Add `import "./lesson"; import "./review";` to `web/src/lib/coach/modes/index.ts` (the lead resolves the one-line conflict with E and G).

## Use what exists
- `coachModel()`, `trackCoachUsage` (`lib/coach/model.ts`); `extractMemory`, `memoryForPrompt` (`lib/coach/memory.ts`); `fastModel`, `NO_THINKING` (`@/lib/ai`).
- Data: `problems` (statement_md, solutions jsonb by language, pattern_slug, techniques, difficulty, importance), `pattern_tricks` (pattern_slug, name, idea_md, snippets jsonb by language, problem_slugs), `checkins` (+ `external_id` = LeetCode submission id when synced), `solution_reviews` table, `profiles.language`. Queries style: `lib/library/queries.ts`.
- UI patterns: problem page `web/src/app/(app)/library/problem/[slug]/page.tsx` and check-in panel `components/library/checkin-panel.tsx`, Pattern Map `components/library/pattern-map.tsx`.

## Build

### 1. Solution review (spec §6.9)
- Entry points: **Review my solution** on the problem page and after a check-in (check-in panel success state); both open `/library/problem/<slug>/review` (optionally `?checkin=<id>`).
- Form: language chips (pre-filled from the check-in's source or `profiles.language`), code textarea (monospace, ≤20k chars), and for LeetCode-synced check-ins an **Open my submission** link to `https://leetcode.com/submissions/detail/<external_id>/`.
- Server `web/src/lib/coach/solution-review.ts`: builds the prompt from the code, the problem (statement, pattern, difficulty), reference solutions in the user's language (fallback any), the check-in (result, minutes), and the user's memory; calls `generateText` with `Output.object` on `coachModel()` and a Zod schema: `{ correct: boolean, complexity: { yours: { time, space }, best: { time, space } }, betterApproach: string, lineNotes: { line?: number, note: string }[] (≤8), patternLesson: string, nextProblemSlug: string | null }`. Retry once on invalid output; then a friendly error. Validate `nextProblemSlug` exists and isn't already solved (else pick the next unsolved problem in the same pattern by importance). Save to `solution_reviews`; `trackCoachUsage`; then `extractMemory(userId, { kind: "review", id }, summary)` (don't await failures).
- Review page: verdict + complexity side by side (yours vs best), better approach, your code with line notes (show line numbers), the pattern lesson with a link to the pattern's lesson, **Queue next problem** (adds a mission for today via existing tracker helpers, or links to the problem if a mission can't be added), and **Discuss with Coach** → `/coach?kind=review&ref=<reviewId>`.
- `review` mode (`modes/review.ts`): system prompt carries the saved review + code + problem so the user can ask follow-ups; no action tools.

### 2. Pattern lessons (spec §6.11)
- Entry points: **Teach me this pattern** on the problem page (its pattern), on a Pattern Map node (popover/button), and the Coach page links (brief E) → `/coach?kind=lesson&ref=<patternSlug>`.
- `lesson` mode (`modes/lesson.ts`): the system prompt is assembled **from our data only** — the pattern's name, 3–4 line core idea (from `pattern_tricks` + the pattern topic description), the trick catalog (name, idea, snippet in the user's language, linked problems), one **easy worked example** chosen from our problems in that pattern (lowest difficulty, highest importance, with its reference solution), and a **ladder** of 3–5 problems easy→hard by importance skipping ones the user solved. Instructions: teach step by step, at each step ask the user for the next move and correct them; never invent problems or examples not in the provided material; end by offering to queue the ladder.
- Tools for the lesson mode: `queue_ladder` (proposal → confirm adds up to 3 missions for today/tomorrow via a server action) and `finish_lesson` (records a short summary; the lead-side memory extraction runs from the thread).
- Lesson cards to the feed: out of scope (cards are pipeline-generated); instead the finish step suggests the pattern's existing live cards via Redis feed queue front (reuse brief E's `queue_cards` confirm action if merged; otherwise leave a TODO note in the PR, not in code).

### 3. Tests
Vitest for: prompt builders (given fixtures, the lesson prompt contains only provided problems/tricks; the review prompt includes the user's language solution), the review schema post-processing (`nextProblemSlug` fallback), ladder selection (skips solved, easy→hard). DB/AI paths can't run here — say so.

## Definition of done
All above; README checks pass; PR with **How to test** (a problem to review with a buggy snippet you provide; a pattern lesson walkthrough).
