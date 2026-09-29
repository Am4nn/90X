# Decisions — Me/Coach reorg and page redesigns

Every choice taken while reviewing the mocks. Where a mock and today's behaviour differ, **today's
behaviour wins** unless a line here says otherwise.

## Process

- **Mocks first, then briefs, then build.** The mocks showed options; the briefs are the execution
  spec.
- **Mocks are visual references, not final designs.** The build is an **add-on** — keep existing
  behaviour, add around it.
- Impeccable is used for the design work; `PRODUCT.md`, `DESIGN.md` and `.impeccable/design.json`
  sit at the repo root.

## Navigation

- **Desktop sidebar: six** — Today · Feed · Library · Coach · Friends · Me.
- **Mobile tab bar: five** — Today · Feed · Library · Coach · Me. **Friends is not a mobile tab**;
  six are too compact.
- Friends is reached **from Me** on a phone (a clear, labelled entry).

## Friends

- New route **`/friends`**: pending requests, scoreboard, activity feed, invites, unfriend.
- Order: **comparison leads** (pending → scoreboard → activity → invite).
- Colour: status colour on readiness and results, plus an identity tint per person. The **activity
  feed stays neutral** (the extra colour there looked cheap).
- **`PendingRequests` stays on Today** (it must show even with no campaign).

## Me

- **Keeps**: readiness dial + trend + areas, weakest patterns, personal "This week".
- **Adds**: a Friends entry (mobile), and a **LeetCode** block that is **collapsible** — a status
  row that expands to totals + time capture.
- **Moves off**: friends activity/invites → Friends; interview practice → Coach; notifications,
  "What Coach knows", sign out → Settings.
- Header actions: **Plan** and **Settings**.
- Readiness stays on **both** Me and Today.

## Settings — new route `/me/settings`

- Account, Notifications, a "What Coach knows" link, Sign out.
- **No LeetCode** (it lives on Me).

## Coach

- Modes: **Chat · Lessons · Mocks · Story bank**. "What Coach knows" stays in the header.
- **Lessons** is a real page (`/coach/lessons`), not a redirect to Library.
- **Story bank** keeps today's page (tags, Edit / Improve with Coach / Delete) — just linked here.

## Today

- The Coach's weekly read is a **full card above the missions**.
- **No inline Accept** — deciding on the suggested changes happens on `/me/weekly/[id]`.
- A **dismiss ✕** that holds until next week.
- Mobile drops the change rows and shows the count; desktop keeps them.

## The coach mark: Ren

- The coach is **Ren**, the shared character from Curfew: a shaded sphere with two eyes, red.
- Used wherever the Coach speaks (chat, Today's read card, the coach line).
- **Not in the nav** — the nav keeps the chat-bubble icon.

## Coach chat

- **Quiet inline working state** (one line: "Checking your weak spots…" + "3 of 4 checks done"),
  not the flat "Looked up…" list.
- The **"you can close the app"** note is **muted and set apart** from the reply.
- Replies: a bold lead, then short bullets, plus a **"Checked N things"** line that expands.

## Library

- **Today's behaviour is the default.** Same area tabs, Pattern Map, topic cards, roadmap
  accordions.
- A **new `List / Roadmap` segmented toggle** (not chips), default **List**. Switch to **Roadmap**
  for a roadmap.sh-style graph: spine, main nodes, dashed branches to sub-topics, one highlighted
  path, coverage ticks.
- **Dashed nodes are lessons we haven't written yet** — still tickable, marked "soon".
- **DSA has no toggle** (no roadmap); it stays exactly as today.
- The **area navigation stays as today** — a bordered container with rounded items, **not pill
  tags**.

## Problem page (DSA)

- **LeetCode-first**: **Open on LeetCode** is the first, obvious action; on a phone it sits **above
  the statement**.
- **Sync with LeetCode** auto-logs the attempt (solved, time, hints). **Manual check-in** stays as
  the fallback "so no one can lie".
- The **note is always visible**; time and hints stay **editable after sync**.
- Each outcome **offers the next step** (review the solution / learn the pattern).

## Plan

- One word: **Plan** everywhere; "campaign" disappears from the UI.
- Leads with **level · length · time**, then a **live preview** of the week.
- The manual day-by-day editor **stays**, behind **"Adjust the week"**.
- **Level**: First time / Some practice / Interview-ready — so an experienced person isn't handed
  Two Sum.

## Set up (onboarding)

- Becomes a **stepped flow**: Welcome → You → Level → Time (with the same preview) → LeetCode
  (optional) → the existing diagnostic. Every existing field is kept.

## Coach mocks

- The design-topic picker becomes a **single search input with a dropdown** (not a wall of tags).
- The behavioural mock, when there are **no stories**, explains **why** it needs one and links to
  the Story bank; once there is a story, the **Story bank link stays**.

## Out of scope

- **Feed** — no changes at all.
- **Story bank** — keep today's tags and actions.
