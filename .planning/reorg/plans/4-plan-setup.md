# Unit 4 — Plan, Set up, and a level that means something

**Branch** `plan-setup` · **Worktree** `../90X-wt/4` · **Spec** `e2e/plan-setup.spec.ts`
**Brief** `.planning/reorg/plan.brief.md`

Read `.planning/reorg/plans/README.md` first.

## Scope

Three things: the word "campaign" leaves the UI, Plan leads with four simple choices and a
live week preview, and Set up becomes a stepped flow. Plus **level**, which is new
behaviour — see the section on it, and note it **contradicts the brief**, deliberately.

This is the largest unit after 1a and the only one that changes planning logic.

## Files

**Create**
- `web/src/components/tracker/week-preview.tsx` — the live preview
- `web/src/lib/tracker/level.ts` + `level.test.ts` — the level rules, pure
- `web/e2e/plan-setup.spec.ts`

**Modify**
- `web/src/app/(app)/me/plan/page.tsx`
- `web/src/components/tracker/plan-forms.tsx`
- `web/src/app/actions/plan.ts`
- `web/src/lib/tracker/template.ts` — `proposeSlots` / `proposeTemplate` take a level
- `web/src/lib/tracker/planner.ts` — level-aware new-problem choice
- `web/src/lib/tracker/service.ts` — select `difficulty`, pass `level` to `planDay`
- `web/src/lib/tracker/campaign.ts` — `startCampaign` stores the level
- `web/src/app/setup/page.tsx`, `setup-form.tsx`, `actions.ts`
- `web/src/lib/setup.ts` — a `LEVELS` const and the schema field
- the matching `*.test.ts` files for every rule you change

## Level — read this first

**The column already exists.** The lead added it before this wave:

```
profiles.level  text null  check (level in ('first_time','some_practice','ready'))
```

Null means "not asked" — every existing account. **Null must behave exactly as the app
behaves today.** That is the property that keeps this change safe, and the first test you
write.

The brief says level "sets starting difficulty and the slot mix" and then says "no
behaviour change to `startCampaignAction`". It cannot be both. **Aman chose behaviour**, so
this unit wires it up for real. Say so in the PR under **Decisions**.

Two places it acts, both pure and both tested:

**1. The slot mix.** `lib/tracker/template.ts`:

```ts
SLOT_TYPES = ["new_problem","review","topic","cards"]
Slots = Record<SlotType, number>       Templates = Record<Weekday, Slots>   // 0 = Sunday
SLOT_MINUTES = { new_problem: 40, review: 25, topic: 30, cards: 15 }
MAX_PER_SLOT = 6
templateMinutes(slots): number
proposeSlots(minutes): Slots                              // 1 new_problem, then round-robin
proposeTemplate(weekdayMinutes, weekendMinutes): Templates // weekend = days 0 and 6
```

Give both an **optional trailing `level`** so every existing caller keeps compiling and
behaving identically. `first_time` leans to review and topic over new problems;
`ready` leans the other way; `some_practice` and null keep today's round-robin. Keep the
minute budget exactly as binding as it is now — a level may change the *mix*, never the
total.

**2. The starting difficulty.** `lib/tracker/planner.ts` `planDay(input: PlannerInput)`
picks the next new problem by `score = importance + company focus`, and `PlannerInput`
carries **no difficulty at all** today. So:

- Add `difficulty: string` to `PlannerInput["problems"]` (values are exactly `'Easy'`,
  `'Medium'`, `'Hard'` — a database check constraint) and `level` to `PlannerInput`.
- In `service.ts` around line 153, add `difficulty: problems.difficulty` to the select, and
  pass `level` into the `planDay({...})` call at ~186.
- In the new-problem branch, let level bias the ordering: `first_time` prefers Easy then
  Medium, `ready` prefers Medium and Hard, `some_practice` and **null keep today's
  importance-only order**.
- It stays a **preference, not a filter.** The comment already in that branch — "It is a
  preference, never an automatic schedule" — is the standard. A level must never leave a
  day with no problem to work on.

`planner.test.ts` exists and is the model for these cases.

## The Plan page

**One word: Plan.** Remove "campaign" from every user-facing string. Internal names stay.
The ones that exist today:

- `me/plan/page.tsx`: "Start a new campaign", "Start your campaign", the "Your last
  campaign is over…" hint, `title="Campaign"` and its `Day N of M · ends …` hint
- `plan-forms.tsx`: the "Start campaign" button
- `app/actions/plan.ts`: the note "Campaign started. Today is day 1."
- `setup/page.tsx`: "Set up your campaign"
- `setup-form.tsx`: the legend "Campaign length", the button "Start my campaign"
- `setup/actions.ts`: "Saved, but the campaign didn't start. Start it from Me → Plan."
- `today/page.tsx`: **"No campaign yet"** — this file belongs to **unit 1c**. Leave it and
  note it in the PR; the lead will take it.

**Lead with four things, then the preview:**

1. **Your level** — First time / Some practice / Interview-ready
2. **How long** — 30 / 60 / 90 / custom (today's control, unchanged)
3. **Time a day** — Light · 1h / Standard · 2h / Hard · 3h, mapped onto the existing
   `BUDGETS` (`"60" | "120" | "180" | "240"`), with the exact number still visible
4. **Your week** — the live preview

**The preview** (`week-preview.tsx`) recomputes from the pure rules as the choices change:
`proposeTemplate(weekday, weekend, level)`, then `templateMinutes(templates[d])` per day,
with `DAY_NAMES` / `Weekday` from `lib/tracker/dates`. Show weekday and weekend mission
counts and minutes. `template.ts` is already pure with no `server-only` import and is
already imported by the client `plan-forms.tsx`, so this needs no new plumbing. The
`hours()` helper inside `plan-forms.tsx` is not exported — if the preview needs it, export
it or move it, do not copy it.

**The manual editor moves behind "Adjust the week".** `TemplateEditor` is unchanged, just
progressive. `FocusForm` stays, tidied, not redesigned.

**Mid-plan edits explain themselves.** Changing the length should state what happens to the
remaining days and the end date, truthfully to `setLengthAction` — which has **no Zod** and
passes `Number(form.get("length"))` to `setLength`, which validates and returns an error
string. Read `setLength` before writing the copy; do not describe behaviour it does not
have.

## Set up

One long form today, with every field in `SetupForm`: `name`, `role`, `language`,
`campaign_days`, `weekday_minutes`, `weekend_minutes`, `timezone`, `leetcode_username`,
`has_leetcode_premium`. Turn it into steps, **keeping every field**:

**Welcome** → what 90x does, one line · **You** → name, role, language · **Level** → the
same control as Plan · **Time** → length + daily time with the **same preview component** ·
**LeetCode** → username + Premium, optional.

Then it redirects to `/today` exactly as it does now. Note: the diagnostic is **not** part
of setup — it lives on the Feed (`diagnosticState` → `startDiagnosticAction`) and the brief
is wrong about it being "the existing diagnostic" at the end of this flow. Do not touch the
Feed. Say this in the PR.

`parseSetup` in `lib/setup.ts` holds the Zod schema and `saveSetup` spreads `parsed.data`
straight onto `profiles`, so adding `level` to the schema is enough for it to persist.
Add the `LEVELS` const next to `ROLES` and `LANGUAGES`, and **use the same const on the Plan
page** — one definition of the three values.

`startCampaignAction`'s Zod is `{ length: 7..365, weekday: budget, weekend: budget }`;
add `level` as an optional enum, and thread it through `startCampaign(userId, length,
weekday, weekend, level?)`.

## Do not touch

`today/page.tsx` (1c — including "No campaign yet") · `feed/**` and `lib/feed/**` ·
`me/page.tsx`, `nav.tsx` (1a) · `library/**` (2, 3) · `coach/**` (1b, 1d, 5) ·
`supabase/migrations/**` — **the level column already exists; do not add another** ·
plus the README's forbidden list.

## Tests

TDD, and these come first:

`lib/tracker/level.test.ts` and `template.test.ts`:
- **`proposeSlots(minutes)` with no level returns byte-identical output to today** for 60,
  120, 180 and 240. Write this one first; it is the safety net for the whole unit.
- `first_time` shifts toward review/topic, `ready` toward new problems, at the same total
  minutes.
- `templateMinutes` never exceeds the budget at any level.
- `proposeTemplate` still treats days 0 and 6 as the weekend at every level.

`planner.test.ts`:
- **A null level produces exactly today's new-problem choice.**
- `first_time` prefers an Easy problem over a Medium one of equal importance; `ready` the
  reverse.
- A day where only Hard problems remain still plans a new problem for a `first_time` user
  — preference, not filter.

`e2e/plan-setup.spec.ts`:
- The word "campaign" appears nowhere on `/me/plan` or `/setup`.
- Changing the daily time updates the preview without a reload.
- The day-by-day editor is hidden until "Adjust the week", then works as before.
- Setup walks the steps, keeps every field, and lands on `/today` with a plan.
- An existing account with a null level sees `/me/plan` working unchanged.

## Traps

- **Null level must behave as today.** Every optional parameter defaults to that.
- `BUDGETS` values are the strings `"60" | "120" | "180" | "240"` and
  `startCampaignAction` refuses anything else. The friendly labels are a presentation
  layer over those exact values.
- `setTemplatesAction` parses JSON from a hidden field and `TemplatesSchema` requires
  `new_problem + review + topic > 0`. A level that zeroed all three would make the editor
  unsubmittable.
- `MAX_PER_SLOT = 6` and the editor's `Stepper` both cap at 6.
- `startCampaignAction` and friends return `FormState` and must never throw to the UI.
- `plan-forms.tsx` is a client component importing `template.ts`. Do not add a
  `server-only` import to that file.
- No native `select` or checkbox on desktop — `ChipGroup` / `Switch`. Six text sizes.

## Verification

The README's full list, plus `bun run check:tracker` and `check:rls`. Screenshots at 390px
and 1440px: Plan with the preview, Plan with the week adjusted open, and each Set up step.
