# Brief — shell + the Me/Coach reorg

**Branch:** `me-coach-reorg` (or your session's branch; say so in the PR).
**Read first:** `.planning/briefs/README.md`. It wins over the plan; the plan wins over the spec.

## Rule one: this is an add-on

The mocks in `.planning/reorg/mocks/` are **visual references, not final designs**. Keep every
existing behaviour, feature and control. Add and refactor around them. Where a mock differs from
today's behaviour, **today's behaviour wins unless this brief says otherwise**. Do not rewrite a
page from scratch; move things, don't delete them, unless listed under "moves off".

## Shell / navigation

- **Mobile tab bar stays five tabs** — Today · Feed · Library · Coach · Me. **Friends is not a
  mobile tab** (six tabs are too tight). 
- **Desktop sidebar gains Friends** (six entries).
- **On Me (mobile only)**, add a clear, labelled **Friends** entry that links to `/friends`.
- Files: `web/src/components/shell/nav.tsx`, `web/src/components/icons.tsx` (add `FriendsIcon`).

## Friends — new route `/friends`

- Everything friends-related, out of Me: pending requests, scoreboard, activity, invites, unfriend.
- Reuse, do not rewrite: `lib/tracker/me.ts` (`scoreboard`, `friendActivity`, `friendMocks`),
  `lib/friends/service.ts` (`pendingFor`, `sentBy`), `components/tracker/scoreboard.tsx`,
  `components/tracker/friends-ui.tsx`.
- **Keep `PendingRequests` on Today** — it already renders there for people with no campaign.
- Update `me/friends-actions.ts` `revalidatePath` to include `/friends`.
- Add `loading.tsx` + `error.tsx` for the segment.

## Me — moves out, adds in

- **Keep**: readiness dial + trend + areas, weakest patterns, personal "This week".
- **Add**: the Friends entry (mobile) and a **LeetCode** block. LeetCode is **collapsible**, the
  default state collapsed to one status row ("Synced 2h ago · 412 solved") that expands to the
  existing totals + time capture + Sync button.
- **Moves off Me** (do not delete the components): friends activity/invites → Friends; interview
  practice → Coach; notifications, "What Coach knows" link, sign out → Settings.
- Header actions: **Plan** and **Settings**.

## Settings — new route `/me/settings`

- Account (name, email, timezone), Notifications (`PushSettings`), a "What Coach knows" link, and
  Sign out. **No LeetCode** (it lives on Me now).
- Reached from Me's Settings button. Add `loading.tsx` + `error.tsx`.

## Coach

- Modes: **Chat · Lessons · Mocks · Story bank**. "What Coach knows" stays in the header.
- **Lessons** now points at the real page (`/coach/lessons`), not `/library`.
- **Story bank** keeps today's page (tags, Edit / Improve with Coach / Delete) — just linked from
  Coach. Do not change it.
- **Chat upgrade** (the one annotated surface):
  - Working state: **one quiet inline line** ("Checking your weak spots…" + "3 of 4 checks done"),
    not the flat "Looked up…" list.
  - The "You can close the app" note is **muted and set apart** from the reply.
  - Replies lead with a bold line, then short bullets.
  - **Keep** everything else: Stop, offline/paused, rate-limit pause, cut-off and stop-failed
    warnings, End, proposal cards, citations, tool-step semantics.

## Lessons — new route `/coach/lessons`

- "Pick a pattern", weakest-first, one "Teach me" each, full pattern index below, a link to the
  Library for topic lessons. Reuse `patternMap` (`lib/library/queries.ts`) and the existing
  `?kind=lesson&ref=<slug>` flow. Add `loading.tsx` + `error.tsx`.

## Today — the Coach's read

- Add the weekly read as a card **above the missions**, from `latestWeekly` (`lib/coach/weekly.ts`).
- **No inline Accept**: show the score, the read and the suggested changes; deciding happens on
  `/me/weekly/[id]`.
- Add a **dismiss ✕** that holds until the next weekly review.
- On mobile, drop the change rows and show the count; desktop keeps the list.
- **Keep** the day line, the 90 Grid, the readiness strip and the missions exactly as they are.

## Ren — the coach mark

- New `web/src/components/coach/ren.tsx`: the shared character (a shaded sphere with two eyes),
  rendered as SVG. Red identity tint, as recorded in DESIGN.md.
- Use it wherever the Coach speaks (chat messages, Today's read card, the coach line). **Not in the
  nav** — the nav keeps the chat-bubble `CoachIcon`.

## Out of scope

Feed, Story bank content, Library, the problem page, Plan, onboarding, admin.

## Verification

From `web/`: `typecheck`, `lint`, `test`, `format:check`, `check:tokens`, `check:dead`, `build`.
`check:rls`, `check:tracker`, `check:friends`, `check:coach-tools` need the database — say so; the
lead runs them. Attach before/after screenshots at 390px and 1440px.
