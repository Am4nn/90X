# Brief E — Coach chat, tools and memory page (Part 5)

**Read `.planning/briefs/README.md` first**, then the plan `.planning/plans/2026-09-28-part5-coach.md` (Decisions + Foundation are binding) and spec §6.8, §6.10.

Branch: `coach-chat` (or your pinned branch). PR to `main`. **You own the chat route and UI**; briefs F and G only add modes that plug into it.

## Use what exists
- `web/src/lib/coach/mode.ts` (Mode contract, `registerMode`, `modeFor`), `modes/index.ts` (import registry — add `import "./chat";`; when done, remove the two coach entries from `web/knip.json` `ignore`).
- `web/src/lib/coach/model.ts` (`coachModel`, `trackCoachUsage`), `memory.ts` (`memoryForPrompt`, `extractMemory`, `listMemory`).
- Existing data helpers to build tools on: `lib/tracker/me.ts` (`myDashboard`, `scoreboard`), `lib/tracker/service.ts` (`ensureToday`, `todayStats`), `lib/library/queries.ts` (`patternMap`, `problemList`, `problemDetail`), `lib/tracker/campaign.ts`. Vercel AI SDK v7 (`ai`, `@ai-sdk/react` — add it): `streamText` with `tools`, `stopWhen: stepCountIs(n)`, UI message streams; read `web/node_modules/ai` docs/types for v7 APIs before coding (they differ from v4/v5).

## Build

### 1. Chat route `web/src/app/api/coach/chat/route.ts`
- POST `{ threadId?, kind?, ref?, message }` (AI SDK UI message format). `requireViewer()`-equivalent for route handlers (reuse `getViewer`; 401 when not approved + set up).
- Creates the thread on first message (`coach_threads`, title from the first line), loads its last ~30 messages, builds `ModeContext`, gets the mode via `modeFor(kind)`, streams with `coachModel()`; `stopWhen: stepCountIs(mode.maxSteps ?? 5)`.
- Persists the user message and the final assistant message (`parts`, `citations`) to `coach_messages`; logs usage with `trackCoachUsage`. Rate-limit per user with Redis (`key("coach", "rl", userId)`, e.g. 30 messages / 10 min) → friendly error.
- After a thread goes quiet (next visit, or explicit "End"), run `extractMemory(userId, { kind: "thread", id }, transcript)` once (`memory_extracted_at`).

### 2. `chat` mode `web/src/lib/coach/modes/chat.ts`
System prompt: who the coach is (direct, specific, short answers, asks one question at a time when teaching), today's date, the user's memory block, live progress summary (readiness, streak, day N of M, today's open missions). Tools (spec §6.8), each scoped to `ctx.userId`, results summarized (small JSON, no raw dumps):
- Read: `get_progress`, `get_weak_spots`, `get_recent_activity` (check-ins, card results, mocks — never other users'), `get_plan`, `search_knowledge` (Upstash Vector `query-data`, topK 5; return title, url, snippet; the answer must cite sources), `find_problems` (pattern / difficulty / company / solved-or-not), `find_cards` (topic / format / the user's missed cards), `get_friend_summary` (public stats only: name, readiness, streak, solved this week, mock scores — never notes, memory, chats, reviews).
- Action tools **only propose**: they return `{ proposal: { type, summary, payload } }` and the UI renders a confirm button; nothing changes until the user taps it. Types: `queue_cards`, `add_mission`, `suggest_template_change`, `save_memory`, `start_mock`. Confirming calls a server action (`web/src/app/actions/coach.ts`) that validates the payload with Zod and performs it for the viewer (`queue_cards` → push card ids to the front of Redis `key("feed", userId)`; `add_mission` → insert a mission for today; `suggest_template_change` → show the diff and on Accept save via `setTemplates`; `save_memory` → insert/update `coach_memory` with `source: 'user'`; `start_mock` → link to `/coach?kind=mock&ref=<topic>` — brief G implements the mock mode).
- At most 5 tool calls per message.

### 3. UI `web/src/app/(app)/coach/` (replace placeholder; keep loading/error)
Mockups: Coach frames in `.planning/mockups/`. Mobile: thread list → thread view. Desktop: left column modes (Chat, Lessons, Mocks — link out to F/G pages) + recent threads, right column the conversation.
- Message list with markdown, streaming, tool activity shown as small muted lines ("Looked up your weak spots"), citations as links under the answer, proposal cards with **Confirm** / **Dismiss**.
- Composer: textarea, Enter to send (Shift+Enter newline), Stop while streaming, disabled when rate-limited or offline; starter chips on an empty thread ("What should I focus on this week?", "Why am I weak at sliding window?", "Plan my next 3 days").
- `/coach?kind=<kind>&ref=<ref>` opens a new thread of that kind (F and G link here).
- Budget: when `coachModel()` reports degraded, a small line "Coach is on the lighter model until next month."

### 4. "What Coach knows" `web/src/app/(app)/me/coach/page.tsx` + link from Me
Facts grouped by kind with status chips (active / improving / resolved), edit text inline, delete, and "Add a note for Coach" (source `user`). Server actions scoped to the viewer.

### 5. Tests
Vitest for pure pieces (tool result summarizers, proposal payload schemas, title-from-message, rate-limit window math). Add `web/scripts/check-coach-tools.ts` (rolled-back transaction style like `check-feed.ts`) calling each read tool's data function for a seeded user and a second user, asserting results never include the other user's private rows. You can't run DB scripts; the lead does.

## Definition of done
All above; README checks pass; PR with **How to test** (a short script of chat messages that exercise each tool and a proposal).
