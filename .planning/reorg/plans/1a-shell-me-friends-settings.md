# Unit 1a — the shell, Friends, Me and Settings

**Branch** `me-shell-friends` · **Worktree** `../90X-wt/1a` · **Spec** `e2e/me-reorg.spec.ts`
**Brief** `.planning/reorg/me-coach-reorg.brief.md` (the shell/Friends/Me/Settings parts only)

Read `.planning/reorg/plans/README.md` first.

## Scope

Me is a junk drawer: eleven blocks on one page. This unit moves friends to their own
route, notifications and sign-out to a Settings page, and leaves Me with readiness,
weakest patterns, this week, and a LeetCode block that collapses.

**Not yours:** Coach modes, the Lessons page, Today, the chat. Those are units 1b–1d.

## Files

**Create**
- `web/src/app/(app)/friends/page.tsx`, `loading.tsx`, `error.tsx`
- `web/src/app/(app)/me/settings/page.tsx`, `loading.tsx`, `error.tsx`
- `web/src/components/leetcode/leetcode-card.tsx` — client, the collapsible LeetCode block
- `web/e2e/me-reorg.spec.ts`

**Modify**
- `web/src/components/shell/nav.tsx` — Friends in the **sidebar only**
- `web/src/components/icons.tsx` — add `FriendsIcon`
- `web/src/components/page-header.tsx` — allow up to two actions
- `web/src/app/(app)/me/page.tsx` — strip it down, add the Friends entry and the card
- `web/src/app/(app)/me/friends-actions.ts` — revalidate `/friends`
- `web/src/app/actions/push.ts` — revalidate `/me/settings`

## Reuse, do not rewrite

Everything below already exists at the path given. Nothing here needs a new query.

```
requireViewer()                     @/lib/auth/viewer
  -> Viewer { id, email: string|null, name, avatarUrl, approval, isAdmin,
              setupDone, language, hasPremium, timezone }

scoreboard(viewerId, q?)            @/lib/tracker/me
  -> PersonRow[] { userId, name, isMe, readiness, streak, solvedThisWeek, lastMock }
friendActivity(viewerId, limit=8)   @/lib/tracker/me
friendMocks(viewerId, limit=8)      @/lib/tracker/me
myDashboard(userId, timezone)       @/lib/tracker/me
  -> { today, overall, areas, trend, weakest }

pendingFor(email, q?)               @/lib/friends/service
  -> PendingInvite[] { id, inviterName, createdAt }
sentBy(inviterId, q?)               @/lib/friends/service
  -> SentInvite[] { id, email, status, createdAt, respondedAt }

leetcodeStatus(userId)              @/lib/activity/queries
  -> { lastSuccessAt, unavailable, totals } | null
syncedWithoutTime(userId)           @/lib/activity/queries
  -> { id, title, result, attempts, suggested }[]
syncEnabled()                       @/lib/activity/service
pushEnabled(), settingsOf(raw)      @/lib/push

Dial value / Trend points / AreaBars areas / Scoreboard people / Activity items mocks
                                    @/components/tracker/scoreboard   (server components)
InviteForm sent yourName / PendingRequests requests / UnfriendButton otherId otherName
                                    @/components/tracker/friends-ui   (client)
SyncButton                          @/components/leetcode/sync-button (client, no props)
PushSettings vapidKey initial       @/components/push/push-settings   (client)
setMinutes(form)                    @/app/actions/sync
signOut()                           @/app/actions/auth
PageHeader, EmptyState, RouteError, SubmitButton, button(), chip()
```

`me/page.tsx` today is the reference for every one of these call sites — read it before
you move anything, and move the markup rather than rewriting it.

## What goes where

**`/friends`** — order is fixed by DECISIONS.md: **comparison leads.**

1. `PendingRequests`
2. `Scoreboard` (it already carries `UnfriendButton`)
3. `Activity`
4. `InviteForm`

Colour: status colour on readiness and results, plus an identity tint per person. The
**activity feed stays neutral** — the extra colour there looked cheap. No friends yet:
`EmptyState` that drives to the invite form.

**`/me/settings`** — Account (name, email, timezone; **read-only**, no edit form),
Notifications (`PushSettings`), a "What Coach knows" link to `/me/coach`, Sign out.
**No LeetCode here** — it stays on Me.

**`/me`** keeps, in order: header (Plan + Settings), the readiness card (`Dial`, `Trend`,
the `/me/weekly/<id>` link, `AreaBars`), weakest patterns, "This week" `Scoreboard`, the
**LeetCode card**, and — **mobile only** — a labelled Friends entry linking to `/friends`.

Me loses: `PendingRequests`, `Activity`, `InviteForm`, "Interview practice", Notifications,
the "What Coach knows" card, Sign out. **Delete none of those components.**

**The LeetCode card** (`leetcode-card.tsx`) wraps today's inline block: collapsed to one
status row (`Synced 2h ago · 412 solved`), expanding to the totals grid, `SyncButton` and
the pending-time forms. It is a client component because it holds open/closed state; keep
the `form action={setMinutes}` markup exactly as it is, hidden `checkinId` input and
`name="minutes"` buttons included. Use `details` or a button with `aria-expanded`.

**`nav.tsx`** — `TABS` currently feeds both `TabBar` and `Sidebar`. Split it: keep the
five-entry array for `TabBar` (**`grid-cols-5` does not change**) and give `Sidebar` those
five plus Friends. One `isActive` helper, unchanged.

**`PageHeader`** — its comment says "at most one action (spec §7.3)" and Me already breaks
it with an ad-hoc `flex gap-2` div. Give it a real contract: accept either one node or a
small list, handle the spacing and the mobile wrap inside, and update the comment to say
two. Then Me passes Plan and Settings through it, and the Admin link keeps its
`md:hidden`.

## Do not touch

`today/page.tsx` (1c) · `coach/page.tsx` (1b) · `components/coach/**` (1b/1d) ·
`app/actions/sync.ts` (unit 3 owns it; you only *call* `setMinutes`) · `library/**` (2/3) ·
`me/plan/**` and `setup/**` (4) · plus everything in the README's forbidden list.

## Tests

`e2e/me-reorg.spec.ts`, against a seeded user:

- Me shows readiness, weakest patterns, This week and the LeetCode row, and **does not**
  show the invite form, the friends activity list, Notifications or Sign out.
- The Friends entry on Me reaches `/friends`; `/friends` shows the scoreboard and the
  invite form.
- At 1440px the sidebar has six entries; the mobile tab bar has **five**.
- `/me/settings` shows Notifications and Sign out, and **no LeetCode**.
- The LeetCode card starts collapsed and expands to reveal the totals.
- Accepting a pending request on `/friends` updates the page — this is what proves the
  `revalidatePath` change, and it is the one most likely to be wrong.

Unit tests: only if you extract a pure helper. Do not test components with Vitest here.

## Traps

- **Mobile stays five tabs.** `PLAN.md` says six. It is wrong.
- **`revalidatePath`**: `friends-actions.ts` revalidates `/me` and `/today` today. Every
  action there needs `/friends` **added** and `/today` **kept** — `PendingRequests` still
  renders on Today. `revokeAction` revalidates `/me` only; it needs `/friends` too. In
  `app/actions/push.ts`, three `revalidatePath("/me")` calls become `/me/settings`.
- **`pendingFor` takes an email** and `viewer.email` is `string | null`; today's page
  passes `viewer.email ?? ""`. Keep that.
- **`Scoreboard` shows an EmptyState when `people.length < 2`** and its copy says "Invite
  a friend below". On `/friends` the invite form *is* below it, so it finally reads true.
- **There is no "list my friends" query.** `scoreboard` is the only thing returning friends
  with names, and only approved, setup-done ones. Do not write a new one to make the page
  prettier.
- `loading.tsx` shaped like the page, `error.tsx` via `RouteError` — and in **Next 16 an
  error boundary receives `retry`, not `reset`**.
- No native `select` or checkbox on desktop; six text sizes only; borders not shadows.

## Verification

The README's full list, plus `bun run check:rls`, `check:tracker` and `check:friends`.
Screenshots at 390px and 1440px of `/me`, `/friends` and `/me/settings`.
