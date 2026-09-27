# Brief G — Mock interviews, STAR story bank, weekly review (Part 5)

**Read `.planning/briefs/README.md` first**, then the plan `.planning/plans/2026-09-28-part5-coach.md` (Decisions + Foundation are binding) and spec §3 (Behavioral, Mock format, Readiness row), §6.1 (readiness bullets incl. the coach's weekly read), §6.2 (template changes need Accept).

Branch: `coach-mocks` (or your pinned branch). PR to `main`. Brief E builds the chat route/UI in parallel; your mock conversation is a **mode** that plugs into it (`lib/coach/mode.ts`). Add `import "./mock";` to `web/src/lib/coach/modes/index.ts` (the lead resolves the one-line conflict with E and F).

## Use what exists
- `coachModel()`, `trackCoachUsage`; `extractMemory`, `ageMemory`, `memoryForPrompt`; `fastModel`, `NO_THINKING`.
- Tables: `mocks` (public: type, topic, status, score, started_at, ended_at), `mock_details` (private: thread_id, prompt, rubric_scores, feedback_md), `stories`, `weekly_reviews`, `readiness_snapshots`, `campaigns.templates` + `lib/tracker/template.ts` (`parseTemplates`), `lib/tracker/campaign.ts` (`setTemplates`), `lib/tracker/me.ts`.
- The hourly job `web/src/app/api/jobs/hourly/route.ts` and `lib/tracker/notify.ts` (`dueJobs`) — per-user local hours; push via `lib/push.ts` `sendToUser`.
- Me page `web/src/app/(app)/me/page.tsx` and `components/tracker/scoreboard.tsx` (Dial).

## Build

### 1. Mock interviews
- Page `/coach/mocks`: pick **Design** (topic chips from system-design topics, e.g. "URL shortener", "Rate limiter"; case-study topics first) or **Behavioral** (a common question list; needs ≥1 story, else prompt to add stories). Past mocks list with score and date.
- Start → creates `mocks` + `mock_details` rows and a `coach_threads` row (kind `mock`, ref = mock id) → opens `/coach?kind=mock&ref=<mockId>` (brief E's UI) — also render a slim header on mock threads: stage + countdown timer (Design 35 min: requirements 5 → high-level 10 → deep dive 15 → wrap-up 5; Behavioral 20 min: question → follow-ups → reflection). Timer is client-side from `started_at`; stage prompts come from the mode.
- `mock` mode (`modes/mock.ts`): interviewer persona; asks one question at a time; follows the stage plan; for behavioral uses the user's stories (titles + STAR summaries) to probe; never gives the answer during the mock; tool `end_mock` (proposal → confirm).
- Ending (button or `end_mock` confirm or timer end): scoring call on `coachModel()` with `Output.object`: rubric per type (Design: requirements, high-level design, deep dive, trade-offs, communication; Behavioral: situation clarity, ownership, action detail, result/impact, reflection) each 1–5 with one-line evidence, overall score 0–100, 3 strengths, 3 improvements. Save to `mock_details` + `mocks.score/status/ended_at`; `extractMemory(userId, { kind: "mock", id }, transcript + feedback)`.
- Result page `/coach/mocks/<id>`: rubric bars, score, strengths/improvements, link to the thread transcript.
- Friends see mock type/topic/score (already allowed by RLS) — add mocks to Me's friend activity list and scoreboard ("Last mock").

### 2. STAR story bank
- `/me/stories`: list + editor (title, Situation, Task, Action, Result, tags chips like leadership, conflict, failure, impact, ambiguity). Target 6–8 stories (spec §3) — show progress "5 of 8". Owner-only server actions.
- **Improve with Coach** on a story → `/coach?kind=chat&ref=story:<id>`... (brief E's chat mode doesn't read refs; instead put a short prefilled first message in the URL `?q=` and let E's composer accept `q` — if E hasn't merged, leave the link as `/coach` and note it in the PR).

### 3. Weekly review (Sunday)
- In the hourly job: for each user at local **Sunday 18:00**, generate the week's review once (unique `(user_id, week_start)`):
  - `formula_score` = latest readiness overall; inputs: the week's check-ins, card accuracy, mocks, days done/missed, weakest patterns/areas, memory block.
  - `coachModel()` with `Output.object`: `{ coachScore 0–100, summary (markdown, ≤180 words, specific), suggestedChanges: [{ weekday 0–6, slot: 'new_problem'|'review'|'topic'|'cards', from, to, why }] (≤3, must stay valid per parseTemplates) }`.
  - Then `ageMemory(userId)`; push "Your weekly review is ready" (respect a new `notifications.weekly` flag, default on — add it to push settings UI).
  - Put the weekday/hour rule in `lib/tracker/notify.ts` `dueJobs` as a new job kind `weekly` with tests.
- Me: beside the dial, "Coach's read: 52 · week of Sep 21" linking to `/me/weekly/<id>`: the summary, formula vs coach score, suggested changes as a diff with **Accept** (applies via `setTemplates`, sets `accepted=true`) / **Decline** (`accepted=false`).

### 4. Tests
Vitest: `dueJobs` weekly rule (time zones), rubric → score math, template-suggestion validation (invalid suggestions dropped), stage/timer schedule. DB/AI paths can't run here — say so.

## Definition of done
All above; README checks pass; PR with **How to test** (start/end a design mock; add stories and run a behavioral mock; trigger a weekly review for a user by calling the job function directly).
