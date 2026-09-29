# The Feed v2 wave — ten parts, one set of rules

Feed v2 replaces every Feed card: typed answers are gone, the Feed becomes **47 archetypes
over 10 primitives and 4 answer shapes, every answer graded by a pure function**, and the
whole 2,808-card corpus is regenerated. This directory turns `PLAN.md` into executable work.

## Reading order

1. **This file** — the wave's rules.
2. **`.planning/briefs/README.md`** — how we code here. It wins over everything below.
3. **`.planning/feed-v2/DECISIONS.md`** — every decision, four rounds. **Wins over PLAN.md**
   and this file wherever they disagree.
4. **`.planning/feed-v2/PRIMITIVES.md`** — the 11 primitives and the 4 answer shapes.
5. **`.planning/feed-v2/CATALOGUE.md`** — the 47 archetypes, with eligible areas.
6. **`.planning/feed-v2/EXAMPLES.md`** — one worked example per archetype (owner-approved).
7. **`.planning/feed-v2/OPEN-QUESTIONS.md`** — the four things left as measurements.
8. **Your plan** — `.planning/feed-v2/plans/<part>.md`.

Precedence when two disagree: `briefs/README.md` → `DECISIONS.md` → your plan → PRIMITIVES.md
→ CATALOGUE.md → PLAN.md. `PLAN.md` is the strategy document and has no signatures; your plan
has them.

## The one rule that keeps this from drifting

**`archetypes.json` at the repo root is the single file both the pipeline and the app read.**
The app gets a generated typed module from it — the same pattern as `db/pulled` — and
`check:archetypes` fails when the generated file is stale. Part A owns this file; every other
part consumes the generated module and never edits the JSON or the generated TS by hand.

## The answer contract — 4 shapes, nothing else

```ts
type Answer =
  | { shape: "chosen"; picked: number[] }        // pick one, grid toggle, tap in place
  | { shape: "ordered"; order: number[] }        // order, assemble
  | { shape: "mapping"; pairs: [number, number][] } // match, bucket, claim grid
  | { shape: "number"; value: number };          // numeric entry
```

A why-step, where present, is a **second `chosen` answer**. A Hard card answered correctly
with the wrong reason is marked **wrong** — see DECISIONS.md round 4 and judge it in review
before trusting it.

**"11 primitives" = 10 screens + the why-step modifier.** DECISIONS.md round 4 settled that
pick-then-justify is a card-level modifier, not a screen. The `primitive` enum has 10 values;
the why-step is the `why_step` field on a card. See Part A.

## Your worktree and branch

| Part | Plan | Branch | Worktree | Playwright spec |
|---|---|---|---|---|
| A | `A-schema-registry.md` | `feed-v2-schema` | `../90X-wt-fv2/a` | — |
| B | `B-grader.md` | `feed-v2-grader` | `../90X-wt-fv2/b` | rewrites `e2e/feed.spec.ts` |
| C1 | `C1-ui-existing.md` | `feed-v2-ui-c1` | `../90X-wt-fv2/c1` | `e2e/tapspot.spec.ts` |
| C2 | `C2-ui-mapping-ordering.md` | `feed-v2-ui-c2` | `../90X-wt-fv2/c2` | `ordering` `pairing` `bucketing` `assembling` `claimgrid` |
| C3 | `C3-ui-numeric-grid-why.md` | `feed-v2-ui-c3` | `../90X-wt-fv2/c3` | `keypad` `gridtoggle` `whystep` |
| D | `D-selection-difficulty.md` | `feed-v2-selection` | `../90X-wt-fv2/d` | — (Vitest over the pure function) |
| E | `E-generation.md` | `feed-v2-generation` | `../90X-wt-fv2/e` | — (pipeline) |
| F | `F-gates.md` | `feed-v2-gates` | `../90X-wt-fv2/f` | — (pipeline) |
| G | `G-review.md` | `feed-v2-review` | `../90X-wt-fv2/g` | — (admin render) |
| H | `H-publish-swap.md` | `feed-v2-swap` | `../90X-wt-fv2/h` | — (pipeline) |

You work **only in your own worktree**. Never switch its branch, never touch another
worktree, never push to `main`, never force-push anything.

## Files no part may touch — the orchestrator's

- `web/scripts/check-*.ts` — **all of them**, including `check-feed.ts`, `check-shards.ts`,
  `check-archetypes.ts`, `check-tokens.ts`, `check-bundle.ts`, `check-coverage.ts`. The
  orchestrator extends `check-feed.ts` with per-primitive database cases after B lands, and
  `check-archetypes.ts` already exists. A diff that touches a `check-*.ts` is sent back.
- `.github/workflows/ci.yml` — the shard matrix is already written for this wave. Do not edit.
- `web/e2e/*.spec.ts` that your plan does not name. `feed.spec.ts` is B's, then C1's. Each new
  spec file belongs to exactly one part.
- `supabase/migrations/` — **except Part A**, which owns its one migration. Any other part
  that thinks it needs a column stops and says so in the PR.
- Generated, except where a part regenerates them on purpose: `web/src/db/pulled/**`,
  `web/src/lib/supabase/database.types.ts` — Part A regenerates them via `db:pull`/`db:types`;
  no other part edits them.

**If a ceiling fails, do not raise it.** Report the number you measured in the PR. The
orchestrator re-measures on merged `main`.

## Your Playwright spec name is fixed

Every shard in `.github/workflows/ci.yml` already names your spec, so the file must be called
exactly what your plan says. **Playwright takes its positional arguments as substring filters
on the path**, so a name that contains `feed`, `coach`, `today`, `friends`, `admin`, `checkin`,
`offline`, `brand`, `a11y`, `roadmap` or `mock-picker` would be claimed by two shards and
`check:shards` would refuse it. The names above are chosen to avoid every existing one. Do not
rename, do not add a second spec file.

## Verification — all of it, by you

You have the database and a browser (or, for pipeline parts, the local staging DuckDB). Nothing
is handed to the orchestrator. From `web/`:

```bash
bunx oxfmt                 # first: it sorts imports and Tailwind classes
bun run typecheck
bun run lint
bun run test
bun run format:check
bun run check:tokens       # report the number; never edit the ceiling
bun run check:dead
bun run check:dupes
bun run check:cycles
bun run check:coverage
bun run check:deps
bun run check:actions
bun run build && bun run check:bundle     # report the KB; never edit the ceiling
bunx playwright test e2e/<your-spec>.spec.ts --project=desktop --retries=0
```

Plus the database checks your plan names (`check:rls`, `check:tracker`, `check:feed`,
`check:friends`), `check:archetypes`, and screenshots at **390px and 1440px** of every screen
you changed. Pipeline parts run `uv run pytest` in `pipeline/`.

TDD for logic: write the test, run it, watch it fail, implement, watch it pass. **Always
`--retries=0`, and run your spec at least three times.** A test that passes on a retry is a
failing test.

## Three hard rules — not negotiable

1. **No agent touches production.** Migrations: write the file, apply to the local Supabase
   stack only. Never `supabase db push` against `DIRECT_URL` from `.env.local` — that is
   production. Never run `pipeline publish` against production. Part H is prepared and verified
   locally, then stops and reports. Reason, not superstition: applying a migration ahead of the
   deploy took this app down on 2026-09-29.
2. **No full generation run without a costed go-ahead.** Gate 1: generate one topic, report the
   measured cost per card, stop. Gate 2: blind gate over 50 cards, report the rejection rate,
   stop. Set `PIPELINE_MAX_USD` on every pipeline invocation. $20 total approved; report
   cumulative spend in every status report.
3. **Only the orchestrator touches the shared files** listed above.

## Cross-cutting decisions — settled, do not reopen

1. **Tap-to-place everywhere, never drag.** Tap the item, tap its destination.
2. **No partial credit.** A card is right or wrong. Four of five pairs matched is wrong.
3. **The reader's difficulty toggle shifts the mix, never filters it.** No card becomes
   unreachable; FSRS scheduling is untouched.
4. **Typed dies in the Feed only.** `gradeWithAi` stays in `grader.ts` for mocks, the Coach and
   reviews; it leaves every Feed path.
5. **FSRS history is kept, orphaned on retired cards.** Retire, never delete.
6. **Difficulty is generated and selected for**, not just labelled: the rubric at write time,
   calibration from outcomes at n ≥ 20, and an adaptive session mix.
7. **The Feed is a designed surface, not a scaffold.** UI parts (B's base card, C1/C2/C3) load
   the `impeccable` skill and follow its craft floor — this is an **Operate** surface: scanability,
   consistency, tap ergonomics and the real phone-in-hand scene outrank ornament. But the repo's
   own rules win over any generic UI preference, and they are not negotiable:
   - six text sizes only (`text-display/title/heading/body/small/tag` + `text-dial`);
   - colours only from tokens (`text-text/2/mute`, `bg-surface/2`, `border-line/2`,
     `text-cyan/bg-cyan/bg-cyan-bg/text-on-cyan`, `bg-topic-*`, `text-ok/warn/bad`), no hex, no
     Tailwind palette;
   - borders on cards, no shadows (except floating layers); dark theme only;
   - mobile-first at 390px; tap targets ≥ 44px; keyboard- and screen-reader-reachable;
   - motion via `tw-animate-css` (already a dependency), never decorative-only, and honour
     `prefers-reduced-motion`.
   A card answered on a phone in a gap between other things is the product; make each primitive
   feel immediate, legible and satisfying without one unnecessary pixel of chrome.

## The PR

Open one PR to `main`, titled as a sentence about what changed. Sections:

- **What** — one line per file or area.
- **Decisions** — anything you interpreted, and what it costs if you got it wrong.
- **Checks** — every command above with pass/fail, plus the **measured token count and bundle
  KB**.
- **Not verified** — anything you could not prove (database, a real browser, a real model).
- **Screenshots** — 390px and 1440px.
- **Suggestions** — optional, never done in this PR.

End every commit message with:

```
Co-Authored-By: Claude <noreply@anthropic.com>
```

## Accept a part as done only when

- its PR is open against `main` and every CI check passes, and
- no test passed on a retry (open the `e2e feed` / `e2e coach` job log and grep
  for `retry #`), and
- the agent reported: every gate's result, the measured token count and bundle KB, how many
  times it ran its spec, its decisions with what each costs if wrong, and anything unverified.

If a part reports a gate failure it cannot fix inside its scope, it does not widen scope or
weaken the gate. It stops and reports; the orchestrator collects it.
