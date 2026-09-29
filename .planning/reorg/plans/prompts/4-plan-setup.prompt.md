You are building **unit 4 of the 90x reorg wave: Plan, Set up, and a level that means something**.

**Worktree** `../90X-wt/4` · **Branch** `plan-setup` · **Playwright spec** `web/e2e/plan-setup.spec.ts`

Other agents may be building units 1a, 1b, 1c, 1d and 3 at the same time in their own
worktrees. Never touch their files.

## Read these first, in this order

1. `.planning/reorg/plans/prompts/SETUP.md` — your environment, how to test, every gate, the
   forbidden files, the PR format. **Read it before you write any code**; it contains the one
   flag (`E2E=1`) without which no test can sign in.
2. `.planning/briefs/README.md` — how this codebase is written. Wins over everything.
3. **`.planning/reorg/plans/4-plan-setup.md` — your plan.** Exact files, the existing functions
   to reuse with their real signatures, the tests, the traps.
4. `.planning/reorg/plans/README.md` — the wave's cross-cutting decisions.
5. `.planning/reorg/plan.brief.md` — the intent.
6. `.planning/reorg/DECISIONS.md` — the Plan and "Set up" sections.
7. `.planning/reorg/mocks/plan.html` and `onboarding.html` — visual references.
8. `web/AGENTS.md` — **this is Next.js 16**; read the guide under
   `web/node_modules/next/dist/docs/` before writing routing or server-action code.

Existing tests that are your model: `web/src/lib/tracker/template.test.ts` and
`planner.test.ts`. Read them before changing either module.

## What you are doing

Three things, plus one that changes behaviour:

1. **One word: Plan.** "campaign" leaves every user-facing string. Your plan lists all of them.
2. **Plan leads with four choices then a live week preview** — level, how long, time a day, and
   the week. The manual day-by-day editor moves behind "Adjust the week", unchanged.
3. **Set up becomes a stepped flow**, keeping every existing field.
4. **Level does something.** This is the part that is not just UI.

**This is an add-on.** The manual editor and the company-focus form stay — they move behind a
link, they are not removed or redesigned.

## Level — read this before anything else

**The column already exists**, added by the prep PR:

```
profiles.level  text null  check (level in ('first_time','some_practice','ready'))
```

**Null means "never asked" — every existing account — and null must behave exactly as the app
behaves today.** That is the property that makes this safe, and it is the **first test you
write**: `proposeSlots(minutes)` with no level must return byte-identical output to today for
60, 120, 180 and 240.

The brief says level "sets starting difficulty and the slot mix" and then says "no behaviour
change". It cannot be both. **The owner chose behaviour**, so wire it up for real and say so in
the PR under Decisions. Two places, both pure and both tested:

- **The slot mix** — `proposeSlots` and `proposeTemplate` in `web/src/lib/tracker/template.ts`
  take an **optional trailing `level`**, so every existing caller compiles and behaves
  identically. `first_time` leans to review and topics; `ready` leans to new problems;
  `some_practice` and null keep today's round-robin. A level may change the *mix*, **never the
  total minutes**.
- **The starting difficulty** — `planDay` in `web/src/lib/tracker/planner.ts` picks the next new
  problem by `importance` and carries **no difficulty at all** today. Add `difficulty: string`
  to `PlannerInput["problems"]` (values are exactly `'Easy' | 'Medium' | 'Hard'`, a database
  check constraint) and `level` to `PlannerInput`; in `web/src/lib/tracker/service.ts` around
  line 153 add `difficulty: problems.difficulty` to the select and pass `level` into the
  `planDay({...})` call below it.

**It stays a preference, never a filter.** The comment already in that branch — "It is a
preference, never an automatic schedule" — is the standard. A `first_time` user on a day when
only Hard problems remain must still get a problem. Test that.

## The four other traps that will cost you most

1. **`BUDGETS` values are the strings `"60" | "120" | "180" | "240"`** and
   `startCampaignAction` refuses anything else. The friendly labels (Light · 1h and so on) are
   presentation over those exact values.
2. **`TemplatesSchema` requires `new_problem + review + topic > 0`.** A level that zeroed all
   three would make the editor unsubmittable.
3. **`today/page.tsx` says "No campaign yet" and belongs to unit 1c.** Leave it and note it in
   your PR; the lead will take it.
4. **The diagnostic is not part of Set up.** It lives on the Feed (`diagnosticState` →
   `startDiagnosticAction`), and the brief is wrong to imply otherwise. Setup redirects to
   `/today`. **Do not touch the Feed.** Say this in your PR.

`plan-forms.tsx` is a client component importing `template.ts`; do not add a `server-only`
import to that file.

## Verification

Everything in SETUP.md, plus these database checks: `bun run check:tracker`, `check:rls`.

TDD in this order, and the first one is the safety net for the whole unit:

1. `proposeSlots` with no level is unchanged for every budget
2. `planDay` with a null level makes exactly today's choice
3. then the level-specific cases, including a day where only Hard problems remain

Your spec must be `web/e2e/plan-setup.spec.ts`, run with `--retries=0` at least three times,
and it must include **an existing account with a null level using `/me/plan` unchanged**.

Screenshots at 390px and 1440px: Plan with the preview, Plan with "Adjust the week" open, and
each Set up step.

Report back as SETUP.md section 8 describes.
