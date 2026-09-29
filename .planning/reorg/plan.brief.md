# Brief — Plan (campaign selection) + Set up

**Branch:** `plan-setup` (or your session's branch; say so in the PR).
**Read first:** `.planning/briefs/README.md`.

## Rule one: this is an add-on

The mocks are **visual references, not final designs**. Keep the **manual day-by-day editor** and
the company-focus form — they stay, they just move behind an "Adjust" link. Do not remove controls;
reorganise them, and make the page lead with something simple.

## Plan page (`/me/plan`)

1. **One word: Plan.** The page and the thing are both "Plan". Remove "campaign" from every
   user-facing string (labels, hints, errors, the empty state). Internal names may stay.
2. **Lead with four simple things**, then a preview:
   - **Your level** — First time / Some practice / Interview-ready. Sets starting difficulty and
     the slot mix so an experienced person isn't handed Two Sum.
   - **How long** — 30 / 60 / 90 / custom (today's control).
   - **Time a day** — plain language (Light · 1h / Standard · 2h / Hard · 3h) mapped to today's
     budgets, plus the exact value somewhere.
   - **Your week** — a **live preview**: weekday and weekend mission counts and minutes, computed
     from the existing template rules (`lib/tracker/template.ts`). Recompute as choices change.
3. **The manual editor moves behind "Adjust the week"** — `TemplateEditor` unchanged, just
   progressive.
4. **Mid-campaign edits explain themselves**: changing length states what happens to remaining days
   and the end date, truthfully to `setLengthAction`.
5. **Company focus** (`FocusForm`) stays, tidied but not redesigned.
6. **No new data or logic**: no migrations; no behaviour change to `startCampaignAction`,
   `setLengthAction`, `setTemplatesAction`. This is a UI brief.

## Set up (`/setup`)

Today it is one long form called "Set up your campaign". Turn it into a **stepped flow** with a
short reason on each step, keeping **every field**:

- **Welcome** → what 90x does, one line, "Get started".
- **You** → name, target role, DSA language.
- **Level** → the same level control, asked once (stored where setup stores the rest; if that needs
  a profile column, say so — do not add a migration yourself).
- **Time** → length + time, with the **same preview as the Plan page**.
- **LeetCode** → username + Premium toggle (today's fields), optional.
- Then the existing diagnostic, unchanged.

## Verification

From `web/`: `typecheck`, `lint`, `test`, `format:check`, `check:tokens`, `check:dead`, `build`.
Add a unit test for the budget → slot-count / minutes helper (TDD). `check:tracker` needs the
database — say so. Screenshots at 390px and 1440px.
