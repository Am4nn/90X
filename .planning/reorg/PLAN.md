# 90x — Simplify "Me" and fix Coach's "Lessons" — Plan

> **This is the oldest document in this folder, and parts of it are superseded.**
> `DECISIONS.md` is binding where the two disagree, and §11 below records the mock
> review. Read `plans/README.md` for the precedence order before building anything.

**Branch:** `simplify-me-and-coach` (off latest `main`)
**Date:** 2026-09-29
**Status:** Decisions locked via menu; mock phase is next.

---

## 1. Goal

Two connected problems:

1. **"Me" is a junk drawer.** It renders readiness, weakest patterns, a
   scoreboard, friends (activity + invites), interview practice (story bank +
   mocks), LeetCode sync, notifications, "What Coach knows", and sign out — all
   on one page. Several of these get ignored because they're buried.
2. **Coach's "Lessons" mode is a lie.** On the Coach page, the "Lessons" entry
   just links to `/library`, which is confusing (it's not a lessons list, it's
   the whole catalog). The weekly "Coach's read" is also buried under a tiny
   link on Me even though it carries the coach's score, a written summary, and
   *suggested plan changes*.

The fix: split "Me" into focused surfaces, give Friends its own tab, build a
real Coach "Lessons" page, move Settings into its own sub-page, and surface the
Coach's weekly read on Today where it belongs.

---

## 2. Current state (what exists today)

**Tabs** (`web/src/components/shell/nav.tsx`, `TABS`): Today · Feed · Library ·
Coach · Me. Mobile `TabBar` is `grid-cols-5`.

**`/me`** (`web/src/app/(app)/me/page.tsx`) renders, in order:
1. `PendingRequests` (friend invites)
2. Readiness dial + trend + "Coach's read" link + `AreaBars`
3. Weakest patterns
4. "This week" `Scoreboard` (You + friends)
5. Friends `Activity` (check-ins + mocks)
6. `InviteForm` (invite + sent invites)
7. "Interview practice" (Story bank link + Mock interviews link)
8. LeetCode (sync status, `SyncButton`, easy/med/hard totals, pending-time form)
9. Notifications (`PushSettings`)
10. "What Coach knows" link
11. Sign out

Sub-pages under Me: `/me/coach` (What Coach knows), `/me/plan`, `/me/stories`
(Story bank), `/me/weekly/[id]` (weekly review).

**`/coach`** (`web/src/app/(app)/coach/page.tsx`) has a `MODES` nav:
- Chat → `/coach?new=1`
- **Lessons → `/library`** ← the redirect that confuses
- Mocks → `/coach/mocks`

**Weekly review** (`/me/weekly/[id]`) holds: readiness formula score, Coach's
own score, a Markdown summary, and suggested template changes that need Accept.

---

## 3. Decisions (locked, 2026-09-29)

| # | Decision |
|---|---|
| D1 | ~~Add **Friends as a 6th top-level tab**.~~ **Superseded** by DECISIONS.md → Navigation: the **desktop sidebar** gains Friends (six entries); the **mobile tab bar stays five** and Friends is reached from Me. Six tabs were too tight. |
| D2 | **Friends page holds everything friends**: scoreboard, activity feed, invites (send/accept/refuse/dismiss/revoke), unfriend. |
| D3 | **Coach's weekly read → Today**, highly visible. Present **2–3 mock directions** to choose from (not decided in code yet). |
| D4 | **Build a real "Lessons" page** under Coach (no more redirect to Library). |
| D5 | **Settings = sub-page of Me** (`/me/settings`), a gear/link on Me. |
| D6 | Settings contains: Notifications/push, LeetCode sync, Sign out, Account/profile, "What Coach knows" link. |
| D7 | **"What Coach knows"** reachable from **both** the Coach header and Settings. |
| D8 | **Interview practice (Story bank + Mock interviews) → under Coach.** Mocks already live at `/coach/mocks`; Story bank joins them there. |
| D9 | **Me keeps:** readiness dial + area bars, weakest patterns, Plan link. No friends content. Readiness also stays on Today (do not remove). |
| D10 | **"This week" scoreboard:** keep only "You" on Me (or drop it — decide via mocks). The friends comparison lives on the Friends page. |
| D11 | **Plan link stays on both** Today and Me. |
| D12 | **Scope: reorg + visual polish.** Respect spec §7 (tokens, borders not shadows, dark only). |

---

## 4. Target information architecture

```
Today       — the day's missions + readiness strip + (NEW) Coach's weekly read
Feed        — unchanged
Library     — unchanged (full catalog, Pattern Map, problems)
Coach       — Chat · Lessons (real page) · Mocks · Story bank
Friends     — NEW: scoreboard, activity, invites, unfriend
Me          — readiness + areas, weakest patterns, personal "this week", Plan, Settings
  └ Settings — Notifications · LeetCode · Account · What Coach knows · Sign out
  └ What Coach knows (also linked from Coach header)
```

---

## 5. Route-by-route changes

### 5.1 Navigation — `web/src/components/shell/nav.tsx`
- Add `FriendsIcon` to `web/src/components/icons.tsx` (a two-person / users
  icon, matching the existing 24×24 stroke style).
- Add `{ href: "/friends", label: "Friends", Icon: FriendsIcon }` to the **sidebar's**
  entries.
- Mobile `TabBar`: **unchanged, `grid-cols-5` stays.** (This line used to say
  `grid-cols-6`; DECISIONS.md settled on five mobile tabs and it wins.)

### 5.2 NEW `/friends` — `web/src/app/(app)/friends/page.tsx` (+ `loading.tsx`, `error.tsx`)
Reuses existing server queries and client components; no new schema.
- **Data:** `scoreboard(viewer.id)` + `friendActivity(viewer.id)` +
  `friendMocks(viewer.id)` + `pendingFor(viewer.email)` + `sentBy(viewer.id)`
  (all in `web/src/lib/tracker/me.ts` / `web/src/lib/friends/service.ts`).
- **Layout (mock to finalize):**
  - Pending requests (`PendingRequests`) at top.
  - Scoreboard (`Scoreboard`) — You + friends, with `UnfriendButton`.
  - Friend activity (`Activity`) — check-ins + mocks.
  - Invite form (`InviteForm`) with sent invites + revoke.
- Empty state when no friends yet: drive to `InviteForm` prominently.

### 5.3 NEW Settings — `web/src/app/(app)/me/settings/page.tsx` (+ `loading.tsx`, `error.tsx`)
- Moves from Me: `PushSettings`, the LeetCode block (`leetcodeStatus`,
  `syncedWithoutTime`, `SyncButton`, totals, pending-time `setMinutes` form),
  and Sign out.
- Adds Account/profile (name, email, avatar — read-only for now) and a
  "What Coach knows" link.
- Entry: a Settings/gear link in Me's header action (next to Plan) and/or in
  the Me page footer. Exact placement decided in mocks.

### 5.4 "What Coach knows" — `/me/coach` (keep path, minimal churn)
- Keep the page as-is. Remove the link from Me (D7: it lives in Settings + Coach header).
- Coach header already links it (`coach/page.tsx` line 102) — keep.
- Add a link to it from Settings.

### 5.5 Coach page — `web/src/app/(app)/coach/page.tsx`
- `MODES` becomes: **Chat**, **Lessons → `/coach/lessons`**, **Mocks → `/coach/mocks`**.
- Add **Story bank** under Coach (D8): a mode entry linking to `/me/stories`
  (or move stories under `/coach/stories` — see §6.2 open item).
- Keep "What Coach knows" header action.

### 5.6 NEW real Lessons page — `web/src/app/(app)/coach/lessons/page.tsx` (+ `loading.tsx`, `error.tsx`)
- No new schema. Reuse `patternMap(viewer.id)` (DSA patterns with mastery
  state, `web/src/lib/library/queries.ts`) and `areaTopics(domain)` +
  `roadmapsFor(...)` for non-DSA authored lessons.
- Each pattern row links to **"Teach me this pattern"** →
  `/coach?kind=lesson&ref=<slug>` (the existing Coach lesson flow) and/or the
  topic lesson page `/library/topic/<slug>`.
- Design direction to finalize via mocks (see §6.3).

### 5.7 Me page — `web/src/app/(app)/me/page.tsx` (big simplification)
Keep only:
- Readiness dial + trend + area bars (readiness also stays on Today).
- Weakest patterns.
- Plan link (header action — already there).
- "This week" — **personal** summary only (You row), or removed (D10, decide
  via mocks). Friends comparison is gone (it lives on /friends).

Remove from Me: `PendingRequests`, Friends `Activity`, `InviteForm`,
"Interview practice", LeetCode block, Notifications, "What Coach knows" link,
Sign out (all relocated per §5.2–5.4).

### 5.8 Today — surface Coach's weekly read (D3)
- Add the weekly review card/banner to `web/src/app/(app)/today/page.tsx`,
  using `latestWeekly(viewer.id)` (`web/src/lib/coach/weekly.ts`) — the same
  call Me uses today.
- **2–3 mock directions** (see §6.1) before committing to one.
- Readiness strip on Today is untouched (D9).

---

## 6. Open design directions (mock phase decides)

### 6.1 Coach's weekly read on Today (D3 — pick from 2–3 mocks)
- **Direction A — Full inline card:** score + one-line summary + "Open review /
  Accept changes" actions, shown while the review is fresh.
- **Direction B — Compact strip under the coach line:** "Coach's read: 72 · read
  it →" next to the existing "C" coach line, expanding to the full page.
- **Direction C — Replace the daily "C" line:** when a fresh weekly exists, the
  coach's opening line on Today becomes the weekly read summary instead of the
  mission reason.

### 6.2 Story bank location (D8)
- **Option A:** keep `/me/stories`, add a link in Coach modes (minimal churn).
- **Option B:** move to `/coach/stories` for a clean "everything practice lives
  under Coach" story. Requires moving the route + updating back-links and the
  behavioral-topic link in `library/topic/[slug]`.

### 6.3 Coach "Lessons" page shape (D4)
- **Option A (recommended):** "Pick a pattern to learn" — a grouped list of DSA
  patterns with your mastery state, each with "Teach me this pattern", plus a
  link to the full Library for topic lessons.
- **Option B:** all authored lessons across every area (patterns + topics),
  grouped by area, each linking to the topic lesson page and a Coach "teach me"
  action.
- **Option C:** a focused "Pattern Map"-lite under Coach (the pattern map
  rendered in the Coach context with teach actions).

### 6.4 "This week" on Me (D10)
- **Option A:** a compact personal card (solved this week, streak, last mock).
- **Option B:** drop it entirely; Me stays minimal (readiness + weakest patterns).

---

## 7. File-level implementation map

### New files
- `web/src/app/(app)/friends/page.tsx` (+ `loading.tsx`, `error.tsx`)
- `web/src/app/(app)/me/settings/page.tsx` (+ `loading.tsx`, `error.tsx`)
- `web/src/app/(app)/coach/lessons/page.tsx` (+ `loading.tsx`, `error.tsx`)
- `web/src/components/icons.tsx` — add `FriendsIcon`

### Changed files
- `web/src/components/shell/nav.tsx` — 6 tabs, grid-cols-6
- `web/src/app/(app)/me/page.tsx` — strip down (§5.7)
- `web/src/app/(app)/coach/page.tsx` — MODES, add Story bank (§5.5)
- `web/src/app/(app)/today/page.tsx` — weekly read card (§5.8)
- `web/src/app/(app)/me/friends-actions.ts` — revalidate `/friends` (see §8)

---

## 8. Things to watch

- **Revalidation:** `me/friends-actions.ts` calls `revalidatePath("/me")` and
  `revalidatePath("/today")`. After the move these must also revalidate
  `/friends`. `PendingRequests` still renders on Today, so keep `/today`.
- **`PendingRequests` on Today:** Today intentionally shows pending invites even
  in `no_campaign`/`ended` states (a user with no campaign still needs to see
  friend requests). Keep that behavior; only *Me* loses it.
- **RLS:** no new tables; all queries are already scoped to the viewer. New
  pages must keep using the existing `requireViewer()` + server queries (never
  expose friends' notes — `friendActivity` already excludes them).
- **Icons:** `FriendsIcon` must match the 24×24 `base` SVG props used by the
  other icons.
- **Mobile tab bar:** 6 labels need `grid-cols-6`; check text truncation at
  `text-tag` on narrow phones.
- **Design tokens:** spec §7 only — six text sizes, token colours, borders not
  shadows, dark only, no native selects on desktop. `check:tokens` enforces.
- **Accessibility:** new links need accessible names; `InviteForm` already
  carries an `aria-label` (keep it).

---

## 9. Verification

From `web/`, no secrets: `typecheck`, `lint`, `test`, `format:check`,
`check:tokens`, `check:dead`, `check:dupes`, `check:cycles`, `check:coverage`,
`check:deps`, `check:actions`, `build` + `check:bundle`, `bun audit`.
Real-DB checks (lead only): `check:rls`, `check:tracker`, `check:friends`
(exists in `package.json`), `check:coach-tools`.

Manual: sign in, verify Friends tab shows scoreboard/activity/invites; Me is
minimal; Settings holds notifications + LeetCode + sign out; Coach has a real
Lessons page and no redirect; Today surfaces the weekly read.

---

## 10. Handoff to mock phase (deepseek flash)

Produce mockups (HTML, matching the existing `web/src` Tailwind design language)
for these screens, with **multiple directions where flagged** so I can choose:

1. **Today with Coach's weekly read** — 2–3 directions (§6.1).
2. **Simplified Me** — with personal "this week" (A) vs without (B) (§6.4).
3. **Friends page** — full layout (scoreboard + activity + invites).
4. **Coach modes** — Chat / Lessons / Mocks / Story bank.
5. **Coach Lessons page** — 2–3 directions (§6.3).
6. **Settings page** — Notifications, LeetCode, Account, What Coach knows, Sign out.

Deliver mocks in `.planning/mockups/` (HTML) following the existing
`desktop-*` / `mobile-*` convention.

---

## 11. Decisions from the mock review (2026-09-29, binding)

Mocks built in `.planning/reorg/mocks/`; the owner chose a direction per screen and the rejected
directions were removed. Recorded here as binding.

| Screen | Locked |
|---|---|
| Today | **Full card** for Coach's read, above the missions. **No inline Accept** — accept/decline lives on the weekly review. Card gets a **dismiss ✕** that holds until next week. |
| Me | Keeps readiness (dial, trend, areas), weakest patterns, personal “This week”, a **LeetCode status line**, and explicit **Plan + Settings** header buttons. |
| Friends | **Comparison leads**: pending → scoreboard → activity → invites. A little more colour: status colour on readiness/results and an identity tint per person — restrained, no slop. |
| Coach modes | Chat · Lessons · Mocks · Story bank; “What Coach knows” stays in the header. |
| Lessons | **Pick a pattern**, **weakest-first** (not roadmap order). |
| Settings | Account · Notifications · LeetCode controls · What Coach knows · Sign out. |
| Coach mark | **Ren**, the shared character from Curfew, rendered in 90x greys (DESIGN.md → Signature Components). |

**LeetCode placement:** entirely on **Me** — sync status, the easy/medium/hard totals and the
time capture. Settings no longer carries LeetCode at all.

**New redesigns, as separate briefs** (not on this branch):
- `.planning/reorg/dsa-problem-page.brief.md` — the DSA problem / check-in page.
- `.planning/reorg/plan.brief.md` — the Plan page and Set up.
- Library roadmap UX: raised, not yet scoped.

