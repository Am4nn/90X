# Brief C — Feed service + screen + diagnostic (Part 4, Tasks 4–6, 8)

**Read `.planning/briefs/README.md` first** (how we code, verify, open PRs, when to ask). This brief adds only what is specific to this task. Plan: `.planning/plans/2026-09-27-part4-feed.md` — its **Decisions** are binding.

Branch: `feed-screen` (or whatever your session is pinned to). PR to `main`.

## What already exists (use it, don't rewrite it)

- Pure logic (`web/src/lib/feed/`): `grade.ts` (`normalize`, `exactMatch`, `gradeOutput`, `gradeOption`, `outcomeOf`, `scoreToRating`, `keyPointScore`, `PASS_MARK`, `OPTIONS_SCORE`), `srs.ts` (`nextState`, `isDue`, `SrsState`), `queue.ts` (`buildQueue`), `diagnostic.ts` (`pickDiagnostic`, `DIAGNOSTIC_AREAS`), `flags.ts`.
- Server: `lib/feed/grader.ts` → `gradeWithAi({ userId, prompt, answer, referenceAnswer, keyPoints }): Promise<{ hits: boolean[] } | { selfMark: true }>` (logs AI cost itself). `lib/feed/flag-service.ts` → `reportCard(userId, cardId, reason)`. `lib/tracker/service.ts` → `onCardAnswered(userId)` (ticks Today's "10 cards" missions) and `snapshotReadiness(userId, date)`.
- Tables (see `web/src/db/pulled/schema.ts`): `cards` (live when `status='live' and not hidden`), `card_reviews`, `card_state`, `card_flags`, `profiles.feed_topics` (jsonb, null = all areas on), `profiles.diagnostic_done_at`, `topics` (`domain` is the area: `dsa`, `system_design`, `cs`, `java`, `sql`), `problems`.
- Redis helper `redis()` from `@/lib/upstash/redis`, keys via `key(...)` from `@/lib/upstash/keys` (always `90x:` prefixed).
- Patterns to copy: `web/src/lib/tracker/service.ts` (server service style, `Db` param for tests), `web/src/app/actions/today.ts` (guarded actions), `web/src/components/tracker/missions.tsx` (client component with `useServerAction` + `useOptimistic`), Today page for layout.

## Build

### 1. `web/src/lib/feed/service.ts` (`server-only`)
- `feedAreas(userId)` → enabled areas (from `profiles.feed_topics` `{ areas: string[] }`, null → all five). `setFeedAreas(userId, areas)`.
- Pools for `buildQueue` (only live, non-hidden cards in enabled areas):
  - **due**: the user's `card_state` rows with `due_at <= now`, most overdue first (limit 100).
  - **weak**: cards from the user's weakest topics — topic weakness = recent wrong/skip rate in `card_reviews` (last 30 days, ≥2 answers) plus, for DSA, patterns whose mastery is `weak` (see `patternMap` in `lib/library/queries.ts`); cards the user hasn't answered in the last 3 days; limit 100.
  - **fresh**: cards with no `card_state` for this user, ordered by topic importance then problem importance, limit 200.
  - Put this pool logic in pure helpers where possible (e.g. `topicWeakness(reviews)`), with tests.
- Queue in Redis `key("feed", userId)` as a list of `{ id, reason }` JSON; `nextCard(userId)` pops until it finds a card that is still live and not hidden (Review focus 5), refills with `buildQueue` when fewer than 10 remain (pass the last topic shown as `lastTopic`). Returns a **CardView without the answer**: `{ id, format, difficulty, promptMd, options (only for mcq), topic: { slug, name, area }, reason, sourceTitle }`. Never send `answer_md` or `key_points` to the client before the user answers.
- `answerCard(userId, input)` where input is one of: `{ cardId, answer }` (typed/flash/mcq-typed/output), `{ cardId, choice }` (mcq after Show options), `{ cardId, skipped: true }`, `{ cardId, selfMark: "got" | "missed" }`.
  - Grading order (spec §6.4 + plan decisions): skipped → 0 (`graded_by 'skip'`); choice → `gradeOption` (`'options'`, `used_options=true`); format `output` → `gradeOutput` (`'match'`); `exactMatch` → 1 (`'match'`); otherwise `gradeWithAi` → `keyPointScore(hits)` (`'ai'`); `{ selfMark: true }` from the AI → return `{ needsSelfMark: true }` without saving; a later selfMark input saves 1 or 0 (`'self'`).
  - Save `card_reviews` (outcome via `outcomeOf`), then `card_state` via `nextState(prev, scoreToRating(score, skipped), now)` as an upsert on (user_id, card_id) so two tabs answering the same card never corrupt state (Review focus 4). Then `onCardAnswered(userId)` (catch and log its errors).
  - Return the result: `{ score, outcome, pointsHit: boolean[] | null, answerMd, keyPoints, options, correctOption (index or null), sourceRefs, nextDue }`.
- Diagnostic: `diagnosticState(userId)` → `'offer' | 'running' | 'done'` (offer when `diagnostic_done_at` is null and live cards exist); `startDiagnostic(userId)` picks with `pickDiagnostic` (seed from user id) and stores ids in Redis `key("diag", userId)`; `nextCard` serves diagnostic cards first while running; answers are saved with `diagnostic=true`; when the list is empty set `diagnostic_done_at` and return a per-area summary (answered, correct). `skipDiagnostic(userId)` sets `diagnostic_done_at` too.
- Session count: answers today (non-skip) for the "after 20 with missions open → banner" rule.

### 2. Readiness gets card accuracy (`web/src/lib/tracker/readiness.ts` + `snapshotReadiness` in `service.ts`)
- `topicArea(topics, studied, cardAttempts?)`: coverage stays importance-weighted studied topics **or topics with answered cards**; accuracy = card scores (last 14 days count double, same rule as `dsaArea`), `null` when no card answers → score stays `null`. DSA accuracy blends check-ins and DSA card scores (weight by count). Add tests first (extend `readiness.test.ts`).

### 3. Actions `web/src/app/actions/feed.ts`
`getNextCard()`, `submitAnswer(input)`, `reportCardAction(cardId, reason)`, `saveFeedAreas(areas)`, `startDiagnosticAction()`, `skipDiagnosticAction()` — `requireViewer()`, Zod, `FormState`-style errors, never throw.

### 4. Feed screen `web/src/app/(app)/feed/` (replace the placeholder page; keep/adjust its `loading.tsx`, `error.tsx`)
Mockups: `.planning/mockups/mobile-today-feed-desktop-today.html` (Feed frame) and `desktop-feed-library-coach-me.html`.
- Header "Feed" + one action: topic toggle (chips for the five areas in a popover/sheet; at least one must stay on).
- Card: area dot + topic name · difficulty tag; prompt (`Markdown`); textarea "Type your answer"; buttons **Skip** / **Check**; for mcq a **Show options** link that swaps the textarea for option buttons (then a pick submits).
- Result: score as "3 of 4 key points" (or "Correct"/"Not quite"), each key point with hit/miss mark, the reference answer (`Markdown`), source title, "Next review in N days"; **Next** button; **Report** (small, opens a reason field). Self-mark fallback when grading is unavailable: "Grading is unavailable right now. Did you get it?" **Got it** / **Missed it**.
- "Why this card" line (weak area / due for review / new / diagnostic).
- Desktop: right column with session progress (answered today, correct %), and the why line.
- Banner after 20 answers today when Today still has open missions: "You've done 20 cards. Your missions are waiting." → link to /today.
- Diagnostic: when `offer`, show an intro card ("A 15-minute check, 20 cards across your areas. It sets your starting readiness.") with **Start** / **Skip for now**; while running show "Diagnostic 7 of 20"; at the end a summary per area and **Continue to your feed**.
- Empty states: no live cards yet ("Cards are being reviewed. Check back soon."), all areas off, nothing left right now.
- Keyboard on desktop: Ctrl/Cmd+Enter = Check, Enter on result = Next.
- Pending states on every button; errors inline; no layout jump between card and result.

### 5. Tests
- Vitest for every pure helper you add (weakness, readiness accuracy, any view mapping).
- Add cases to `web/scripts/check-feed.ts` (rolled-back transaction, like the existing ones) for: answering a typed card stores a review + state and a second answer updates the same state row; a hidden card in the Redis queue is skipped; the diagnostic picks ≤20 and marks done at the end. You can't run it (no database) — write it carefully; the lead runs it.

## Definition of done
Everything above, all README checks passing, PR with **How to test** steps for the lead (approve a batch at `/admin/cards` first so live cards exist).
