# 90x Part 3: Tracker — Implementation Plan

> For agentic workers: execute with superpowers:executing-plans (inline) task by task; TDD for every pure module. Copy this file to `.planning/plans/2026-09-27-part3-tracker.md` as the first execution step.

**Goal:** Make 90x a daily habit: a campaign with a per-weekday template, missions filled every day, a 90 Grid with streaks, a review ladder for weak problems, honest readiness, a Me dashboard with friends, web push reminders, and app-wide loading/error polish.

**Architecture:** Pure logic in `web/src/lib/tracker/*` (dates, template, ladder, planner, day status, streak, readiness), unit-tested with Vitest. Server services read/write Supabase (Drizzle for server jobs, supabase-js under RLS for user actions). Today's plan is built lazily on open (idempotent) and by one hourly QStash job that handles each user's local midnight, morning push and 8 pm reminder.

**Tech stack:** Next.js 16 App Router, React 19, Supabase (migrations + RLS), Drizzle, Upstash QStash + Redis, `web-push`, Vitest.

**Spec:** `.planning/SPEC.md` (§2 part 3, §3 decisions, §5.2, §6.1, §6.2, §6.6, §7). Rulings from the 2026-09-27 menus below override the spec where they differ.

## Decisions from this session (binding)

- **Review ladder:** only problems checked in as **failed** or **with hints** enter it. Due after 3, 7, 21 days; a clean solve advances a step, solving at step 3 graduates it; a failed/hints re-attempt resets to step 1. Review missions offer **Not today** (moves to tomorrow) and **I've got this** (removes it for good).
- **Card slots before Feed (Part 4):** shown on Today as "Coming soon" (disabled), never counted for day completion.
- **No throwaway UI:** build only final features. Areas with no data show an explicit empty state ("No data yet — …") instead of fake numbers. Topic missions link to the Library topic; they tick when the user taps **Mark studied** there (a permanent Library feature that also feeds coverage). Part 4 adds card-based accuracy.
- **Template:** setup asks weekday and weekend time (1h/2h/3h/4h chips); 90x proposes slots; the Plan page in Me edits counts per weekday.
- **Streak:** only fully done days extend it. **Revive:** a missed day can be revived within the next 2 days by finishing its unfinished missions as extra work; it then counts for the streak and its square shows a revive mark.
- **Push:** in Part 3 (8 pm streak reminder, morning plan at a user-chosen time, friend activity off by default).
- **Name:** the product is written **90x** everywhere users see it (titles, manifest, sign-in, brand). Repo/folder names stay.
- **Polish:** loading and error states across the whole app, modelled on Curfew (see Task 13).

## Global constraints

- Day boundary = midnight in the user's `profiles.timezone`; all dates are `YYYY-MM-DD` local strings.
- Slot counts never grow to catch up; review slots carry over, new-item slots are re-picked (§3 Missed day).
- Premium problems are skipped unless `has_leetcode_premium`.
- Readiness area weights (backend default): DSA 35, Design 25, CS 20, Java 15, SQL 5; bands <40 red, 40–69 yellow, ≥70 green.
- Friends see: readiness, streak, day squares, check-ins (no notes). Owner-only: missions, reviews ladder, push subscriptions, notes.
- Redis keys `90x:`; QStash schedules `90x-…`, signature verified with URL (`web/src/lib/upstash/qstash.ts`).
- Type scale / tokens from spec §7 only; no native select/checkbox on desktop (reuse `ChipGroup`, `Switch` in `web/src/components/chip-group.tsx`); motion respects `prefers-reduced-motion`.

## Review focus (tests pinned in owning tasks)

1. Timezone edges: a user in UTC-8 and one in UTC+5:30 around midnight get the right "today" and yesterday is closed once (Task 2, 8).
2. Idempotency: opening Today twice, or the hourly job racing the lazy build, never duplicates missions (unique keys + `on conflict do nothing`) (Task 7).
3. Empty catalog slices: no unsolved problem in the weakest pattern, all topics studied, premium-only pattern → planner falls back to the next pattern/area, never an empty or crashing slot (Task 5).
4. Campaign length change mid-way: grid redraws, past squares keep status, end date moves (Task 9).
5. A sync that imports 10 check-ins at once ticks each matching mission once and updates the ladder once per problem (Task 6).

---

## Task P (first, pipeline): Cheap Gemini review, then resume the card run
Context: the card run is paused at 278/1803 sources (953 cards saved). Google billed ~₹551 (~$6.2) while our log shows $1.24: Gemini 3.x "thinking" tokens are billed as output but missing from `completion_tokens` over the OpenAI-compatible endpoint. Reviewer keeps 99% of cards.
- `pipeline/src/pipeline/llm.py`: pass `reasoning_effort="low"` (lowest Gemini accepts; try `"minimal"`/`"none"` first) for the `review` tier; log `completion_tokens_details.reasoning_tokens` into cost (add column `tokens_reasoning` in `staging.py`, priced as output); add a `gemini-3.5-flash` price entry from Google's pricing page.
- `pipeline/src/pipeline/cards/check.py`: `review_set(llm, cards, source_text)` → one call returns a verdict per card (pydantic list, index-aligned; missing index = drop). Keep the same keep rule (all scores ≥ 4) and allow-standard-knowledge wording.
- `cards/run.py` `_one` uses `review_set`. Tests: fake LLM returning a list; misaligned/missing verdicts drop the card; cost includes reasoning tokens.
- Trial: `pipeline cards --limit 20`, record logged cost, then compare against the Google AI Studio usage page after it updates; resume the full run only if they match within ~20% and projected total stays under the $20 cap. Also report the new keep rate (99% was suspiciously lenient).

## Task 0: Rename to 90x + copy plan
- Replace user-visible "90X" with "90x": `web/src/app/layout.tsx` (metadata title template), `web/src/app/manifest.ts`, `web/src/components/brand.tsx`, sign-in/pending pages, page titles. Grep `90X` in `web/src` and keep only code identifiers/comments where harmless.
- Copy this plan to `.planning/plans/2026-09-27-part3-tracker.md`, start ledger `.superpowers/sdd/2026-09-27-part3-tracker/progress.md`.
- Verify: `bun run typecheck && bun run build`. Commit.

## Task 1: Schema `supabase/migrations/20260927000006_tracker.sql`
- `profiles` add `weekday_minutes int`, `weekend_minutes int` (check in 30..480), `morning_push_hour int` (0–23, null = off).
- `campaigns` (id, user_id, start_date date, length_days int 7–365, status active|ended, templates jsonb, company_focus jsonb null, created_at). Partial unique index: one active campaign per user.
- `days` (user_id, date, campaign_id, status pending|done|partial|missed|revived, closed_at) PK (user_id, date).
- `missions` (id, user_id, date, slot_type new_problem|review|topic|cards, ref text, est_minutes int, status open|done|skipped|coming_soon, reason text, done_at, checkin_id null, is_revive bool default false) unique (user_id, date, slot_type, ref).
- `problem_reviews` (user_id, problem_slug, step int 1–3, due_date date, status active|graduated|dismissed, updated_at) PK (user_id, problem_slug).
- `topic_progress` (user_id, topic_slug, studied_at) PK (user_id, topic_slug).
- `readiness_snapshots` (user_id, date, overall int null, per_area jsonb) PK (user_id, date).
- `push_subscriptions` (id, user_id, endpoint unique, p256dh, auth, created_at).
- RLS: owner all on every table; approved users **select** `days`, `readiness_snapshots`, `campaigns` (for "day 17 of 90"). Missions, reviews, topic_progress, push owner-only.
- Extend `web/scripts/check-rls.ts`: friend reads days/snapshots, cannot read missions/problem_reviews/push, cannot write others' rows.
- Run `bun run db:push`, `db:pull`, `db:types` (needs the new Supabase access token; if still missing, `db:types` is skipped and ledgered), `check:rls`. Commit.

## Task 2: Dates `web/src/lib/tracker/dates.ts`
- `localDate(tz: string, now = new Date()): string`, `addDays(date: string, n: number): string`, `weekday(date: string): 0..6`, `daysBetween(a, b): number`, `localHour(tz, now): number`.
- Tests: Asia/Kolkata 18:29Z vs 18:31Z crosses midnight; America/Los_Angeles; DST day in LA; addDays across month/year.

## Task 3: Template `web/src/lib/tracker/template.ts`
- Types: `Slots = { new_problem: number; review: number; topic: number; cards: number }`, `Templates = Record<0|1|2|3|4|5|6, Slots>`.
- `SLOT_MINUTES = { new_problem: 40, review: 25, topic: 30, cards: 15 }`.
- `proposeTemplate(weekdayMin, weekendMin): Templates` — fills in priority order new_problem → review → topic → cards within budget (e.g. 150 min → 1 new, 1 review, 1 topic, 1 cards ≈ spec §6.2 example). `templateMinutes(slots)`.
- `parseTemplates` (Zod) for the Plan page.
- Tests: 60/120/180/240 budgets; never exceeds budget; min 1 slot.

## Task 4: Review ladder `web/src/lib/tracker/ladder.ts`
- `LADDER_DAYS = [3, 7, 21]`.
- `applyCheckin(prev: Review | null, result: "solved"|"hints"|"failed", today): Review | null` — failed/hints → step 1 due today+3 (new or reset); solved on active → next step or graduated after step 3; solved with no prev → null (not entered).
- `postpone(r, today)` → due tomorrow; `dismiss(r)` → dismissed.
- Tests for each transition, including "solved first try never enters".

## Task 5: Planner `web/src/lib/tracker/planner.ts`
- Input: `{ date, slots, dueReviews: {slug, due_date, title}[], carriedReviews, patterns: {slug, name, mastery, solvedCount}[], problems: {slug, pattern_slug, importance, premium, companies}[], solvedSlugs: Set, topics: {slug, area, importance}[], studied: Set, hasPremium, companyFocus?: {company, from, to} }`.
- Output: `PlannedMission[] = { slot_type, ref, est_minutes, reason, status }`.
- Rules (§6.2): reviews most-overdue first (carry-overs count against review slots); new problem = weakest pattern (weak > started > untouched order by importance; reuse `masteryState` from `web/src/lib/library/map-layout.ts`) then most important unsolved eligible problem, company focus boosts companies[company]; topic = weakest-area most important unstudied topic (areas Design, CS, Java, SQL); cards slot → one `coming_soon` mission.
- Reasons are one line, e.g. "Sliding window is your weakest pattern (1 of 4 solved)".
- Tests: premium filtering, company focus, empty pattern fallback, no duplicate problem across slots, review carry-over never increases count, all topics studied → next area.

## Task 6: Mission ticking `web/src/lib/tracker/tick.ts` + wiring
- Pure `matchMission(open: Mission[], checkin: {slug, pattern_slug})`: exact ref match first, else an open `new_problem` mission in the same pattern (spec "extra work ticks a matching mission").
- Server `web/src/lib/tracker/service.ts` `onCheckins(userId, checkins[])`: for each (deduped per problem) → tick mission, `applyCheckin` ladder upsert, recompute today's day status. Called from `web/src/app/actions/checkin.ts` and `syncUser` in `web/src/lib/activity/service.ts`.
- Tests: pure matcher; one sync with 10 check-ins (Review focus 5).

## Task 7: Day lifecycle `web/src/lib/tracker/days.ts` + service
- Pure `dayStatus(missions)`: ignore coming_soon; all done → done; some → partial; none → missed (only when closing); open day → pending.
- Pure `streak(days: {date,status}[], today)`: counts consecutive done|revived back from yesterday (today counts once done). `revivable(days, today)`: missed days within last 2 days.
- Service `ensureToday(userId)`: loads profile tz + active campaign; closes any unclosed past days (status via `dayStatus`, carries unfinished review missions forward as tomorrow's review candidates); if today has no missions, runs planner and inserts with `on conflict do nothing`. Returns today's view model.
- `startRevive(userId, date)`: copies that day's unfinished missions into today with `is_revive = true`; when all revive missions are done the old day becomes `revived`.
- Tests: pure status/streak/revive; idempotent double call (integration test against a test schema or mocked db layer, Review focus 2).

## Task 8: Readiness `web/src/lib/tracker/readiness.ts`
- `areaScore({ coverage, accuracy }): number | null` = coverage × accuracy × 100; null when no attempts.
- DSA coverage = importance-weighted share of important problems (nc150 ∪ blind75 ∪ importance ≥ 0.5) with any check-in; accuracy from check-ins (solved 1, hints 0.5, failed 0), last 14 days weight 2.
- Design/CS/Java/SQL coverage = importance-weighted share of that area's approved topics marked studied; accuracy = null until Part 4 cards → area shows "No data yet".
- `overall(areas, role)`: weighted mean over areas **with data**, returns null if none; band helper.
- Snapshot written by the hourly job at local midnight and on demand (`readiness_snapshots`).
- Tests: weighting, 14-day doubling, null handling, bands.

## Task 9: Setup + Plan page
- Setup (`web/src/app/setup/*`, `web/src/lib/setup.ts`): add weekday/weekend time chips; on save create the active campaign (start = local today, length = campaign_days, templates = proposeTemplate).
- `web/src/app/(app)/me/plan/page.tsx`: per-weekday steppers for the 4 slot types with minutes total; campaign length chips (30/60/90/custom) → updates length, grid redraws (Review focus 4); optional company focus (company chips from problem companies + from/to dates). Server actions validate with Zod; changes apply from tomorrow.

## Task 10: Today
- `web/src/app/(app)/today/page.tsx` via `ensureToday`: header "Day N · S-day streak · L days left", 90 Grid (`web/src/components/tracker/grid.tsx`, 15 columns, today outlined, done = X stamp animation, missed dim, revived mark), coach line = first open mission's reason, missions list (`mission-row.tsx`): new problem → Library problem (check-in there ticks it), review → same + Not today / I've got this, topic → Library topic with Mark studied, cards → Coming soon. Revive banner when `revivable`.
- Desktop: missions left; grid + Readiness / Solved / Reviews due right (mockup `mobile-today-feed-desktop-today.html`).
- Library topic page gets **Mark studied** (server action → `topic_progress` → ticks topic mission).

## Task 11: Me dashboard
- `web/src/app/(app)/me/page.tsx`: readiness dial (band colour) + 14-day trend from snapshots, area bars in topic colours (empty state per area), weakest patterns (from check-ins), You vs friends table (readiness, streak, solved this week), friends' recent check-ins (title, result, minutes; never notes), existing LeetCode card, links to Plan and Notifications.

## Task 12: Web push + hourly job
- `public/sw.js` (push + notificationclick), `web/src/components/push/enable-push.tsx` (subscribe with `NEXT_PUBLIC_VAPID_PUBLIC_KEY`, store in `push_subscriptions`), settings on Me: 8 pm reminder switch, morning plan hour chips, friend activity switch (stored in `profiles.notifications`).
- `web/src/lib/push.ts` (`web-push`, VAPID env), removes subscriptions that return 404/410.
- `web/src/app/api/jobs/hourly/route.ts` (QStash-verified): per user by local hour — 0h: close yesterday + ensureToday + readiness snapshot; morning hour: "Today: 4 missions, ~2h 30m"; 20h: reminder if today not done. Add `90x-hourly` (`5 * * * *`) to `web/scripts/schedule-jobs.ts`.
- Tests: pure `dueNotifications(users, nowUtc)` selecting who gets what.

## Task 13: Loading and error states (Curfew-style polish, whole app)
Modelled on `../curfew/src/app/{_skeleton.tsx,_route-error.tsx,global-error.tsx,not-found.tsx,ui.tsx}`; 90x has none of these today.
- `web/src/components/skeleton.tsx`: `Bar({w,h})`, `RowsSkeleton({n})`, `TilesSkeleton({n})`, `PageSkeleton({title, children})` (real `PageHeader` title so nothing jumps; `aria-busy`), `InnerSkeleton`. One `animate-pulse` wrapper + `motion-reduce:animate-none`; bars use `bg-surface-2`.
- `loading.tsx` per segment, each shaped like its page: `(app)/today` (grid + 4 mission rows), `feed`, `coach`, `me`, `me/plan`, `library` (tabs + map + rows), `library/problem/[slug]`, `library/topic/[slug]`, `library/doc/[id]`, `admin/users`, `setup`. No root `(app)/loading.tsx` (Curfew lesson: it flashes the wrong shape on every route).
- `web/src/components/route-error.tsx` (`"use client"`): keeps the header, "This didn't load. Nothing was changed.", `Reference {digest}`, **Try again** (`reset`) + optional back link; `useEffect` → `Sentry.captureException` when DSN set, else `console.error`. Thin `error.tsx` per segment above; `app/global-error.tsx` with inline styles (theme unavailable); `app/not-found.tsx` + `library/problem/[slug]` `notFound()` for unknown slugs.
- `web/src/components/form.tsx`: `FormState = { ok?; error?; note? }`, `SubmitButton` (`useFormStatus`, disabled + `aria-busy` + pending label), `useServerAction()` (transition + `router.refresh()`, error message), `ActionForm` (`useActionState`, inline error/note). Retrofit: setup form, check-in panel, sync button, admin approve/reject, sign-out, Mark studied, Plan page, mission actions (optimistic tick via `useOptimistic`).
- `web/src/components/empty-state.tsx`: title + one line + optional action; used for no-data readiness areas, empty friend activity, no missions (campaign ended), empty search.
- Server actions return `{ error }` instead of throwing (wrap in try/catch like Curfew `actions.ts`).
- Minimal `@sentry/nextjs` (client + server init from `NEXT_PUBLIC_SENTRY_DSN`), no-op without DSN.
- Tests: Vitest for `useServerAction` error path is optional; verification is manual: throttle network → skeletons match layout; force a thrown server error → retry card with reference; reduced motion → no pulse.

## Task 14: Verification + review
- `bun run typecheck`, `lint`, `test`, `build`; `check:rls`.
- Manual on https://90x.amanarya.com after deploy: setup → Today shows missions + grid → check in a problem → mission ticks, day done → X stamps; fail one → review appears 3 days later (simulate by date override in test); Plan edit applies tomorrow; push test notification on phone; friend (alt account) sees streak/readiness, not missions/notes; every tab shows skeleton on slow network and a retry card when a server error is forced.
- Final whole-branch review (fresh reviewer), fix Critical/Important.
