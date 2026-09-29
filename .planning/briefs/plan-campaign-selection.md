# Brief — campaign selection on the Plan page

**Branch:** `plan-campaign-selection` (or your session's own branch; say so in the PR).
**Read first:** `.planning/briefs/README.md`. It wins over the plan; the plan wins over the spec.

## Why

`/me/plan` (`web/src/app/(app)/me/plan/page.tsx`, `web/src/components/tracker/plan-forms.tsx`) is
two disconnected steps: `StartCampaignForm` asks for a length and two time budgets, and only
*after* a campaign exists does `TemplateEditor` let you shape the days. The owner's words:
*"we have to redesign the campaign selection the plan page."*

The problems:

1. **No preview.** You pick "90 days, 2h weekday, 3h weekend" and the app silently decides how
   many new problems, reviews, design topics, cards and mocks each day gets. You cannot see what
   you are committing to until after you start.
2. **The time budgets are abstract.** "120" and "180" minutes mean nothing next to five slot types
   that each cost minutes (`SLOT_MINUTES` in `lib/tracker/template.ts`).
3. **Length is a separate screen from the plan that length produces.** Changing length mid-campaign
   (`LengthForm`) says nothing about what it does to the remaining days.
4. **The focus block is fine.** Leave `FocusForm` alone.

## Definition of done

1. **One screen, with a live plan preview.** Choosing length and time budgets updates a preview of
   the generated weekday/weekend plan — the slot counts per day and the daily minutes — before
   you start. Compute it from the existing template rules (`lib/tracker/template.ts`,
   `templateMinutes`, `SLOT_MINUTES`, `MAX_PER_SLOT`); do not change those rules.
2. **Show the trade.** Make the length↔intensity trade visible: a longer campaign spreads the same
   catalog thinner per day. One plain sentence, no hype.
3. **Start, then still edit.** Starting a campaign leads into the same preview/editor so the first
   thing a new user sees is their actual week, not a second form.
4. **Mid-campaign length change is explained.** Changing length on an active campaign states what
   happens to remaining days and the end date (the copy already exists in the page hint — keep it
   truthful to `setLengthAction`).
5. **Keep the weekday editor.** `TemplateEditor` (phone cards + desktop table) stays; it is the
   editor the preview opens into.
6. **No new data or logic.** No schema change, no new migration, no change to
   `startCampaignAction` / `setLengthAction` / `setTemplatesAction` behaviour. This is a UI
   brief.

## Constraints

- DESIGN.md and spec §7 only: six text sizes, token colours, borders not shadows, dark only, no
  native selects. Chips come from `@/components/button-styles` `chip()`; grouped choices use
  `ChipGroup`.
- Mobile first (390px), then desktop. The preview must not overflow on a phone.
- Every numeric commitment shown (minutes, counts, days) is computed from the template rules, never
  hard-coded. If a value is estimated, label it as such.

## Out of scope

- The scheduling/selection algorithm itself, and any migration.
- The Today page and the missions it renders.
- Company focus (`FocusForm`).

## Verification

From `web/`: `typecheck`, `lint`, `test`, `format:check`, `check:tokens`, `check:dead`, `build`.
Add a unit test for any pure helper you introduce that maps budgets to slot counts
(`lib/tracker/`), TDD'd. `check:tracker` needs the database — say so; the lead runs it. Attach
before/after screenshots at 390px and 1440px to the PR.
