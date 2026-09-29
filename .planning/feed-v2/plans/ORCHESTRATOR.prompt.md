You are the orchestrator for **Feed v2** in the 90x repo:
`C:\Aman\Coding-Bamzii\Web Development\90X`, branch `main`.

Feed v2 replaces every Feed card. Typed answers are gone; the Feed becomes **47 archetypes over
11 primitives and 4 answer shapes, every answer graded by a pure function**. The whole corpus of
2,808 cards is regenerated.

The design is finished and is not yours to reopen. Your job is to turn it into executable work,
dispatch it, and report.

## Read these first, in this order

1. **`.planning/feed-v2/PLAN.md`** — the eight parts, the sequencing, the three measurement
   gates, the budget, the risks.
2. **`.planning/feed-v2/DECISIONS.md`** — every decision with its reasoning, four rounds of it.
   **This wins over PLAN.md wherever they disagree.**
3. `.planning/feed-v2/PRIMITIVES.md` — the 11 primitives, what each one is, what it costs.
4. `.planning/feed-v2/CATALOGUE.md` — the 47 archetypes, with eligible areas per archetype.
5. `.planning/feed-v2/EXAMPLES.md` — one worked example per archetype. The owner has approved
   these as representative of what the real cards should be like.
6. `.planning/feed-v2/OPEN-QUESTIONS.md` — the four things deliberately left as measurements.
7. `.planning/briefs/README.md` — how this codebase is written. Wins over everything.

## Your first job: write the part plans

`PLAN.md` is a strategy document. It is **not executable** — it names files but not the
functions and signatures to reuse, has no named tests, no traps, no branch names. An agent given
only `PLAN.md` will invent that layer, and eight agents will invent it eight different ways.

**Use `.planning/reorg/plans/` as your template.** That set was executed successfully by two
agents; copy its shape exactly. Each part plan needs:

1. **Scope** — what this part owns, and what it must not change.
2. **Files** — create / modify, exact paths.
3. **Reuse, do not rewrite** — the existing functions and components with **file path and full
   signature**. This is the section that makes the difference; go and read the code to write it.
4. **Do not touch** — the other parts' files by name, plus the forbidden list below.
5. **Tests** — named cases.
6. **Traps** — the specific ones for that part.
7. **Verification** — the gate list, and which database checks apply.

Write them to `.planning/feed-v2/plans/`, one per part, plus a `prompts/` directory with one
paste-ready prompt per part. `.planning/reorg/plans/prompts/SETUP.md` is the shared environment
recipe and mostly carries over — **read it, and note it contains the four conditions the test
sign-in route needs, including `ALLOW_TEST_SIGN_IN=1`.**

Commit the plans to `main` before dispatching anything.

## Dependency order, and how much to run at once

```
A schema + registry
  └─ B grader ──┬─ C1 C2 C3 UIs
                └─ D selection
A ─ E generation ─[GATE 1]─ F gates ─[GATE 2]─ full run ─ G review ─[GATE 3]─ H swap
```

**A lands first and alone.** Everything codes against the contract it defines; a change to it
after B exists invalidates work.

Then **B**, then **C1/C2/C3 and D in parallel**. **E and F** can proceed alongside once A is in.
**G** needs B and C. **H** is last.

**Run two or three agents at a time, not eight.** Playwright's `baseURL` is hardcoded to
`localhost:3000` and they share one local Supabase stack, so only one can run its e2e suite at a
time. More than three in flight and they queue on the port.

## Three hard rules. These are not negotiable.

**1. No agent touches production.**
- Migrations: write the file, apply it to the **local** Supabase stack only. **Never**
  `supabase db push` against `DIRECT_URL` from `.env.local` — that is the production database.
  Production application is a separate step a human runs.
- **Never** run `pipeline publish` against production. Part H is prepared and verified locally,
  then stops and reports.
- Reason, not superstition: applying a migration ahead of the deploy took this app down on
  2026-09-29.

**2. No full generation run without a costed go-ahead.**
- **Gate 1**: generate **one topic**, report the measured cost per card, and **stop**. The
  original pass averaged ~$0.0017 a card; structured formats carry more fields. 274 topics on an
  estimate is how a budget disappears.
- **Gate 2**: run the blind gate over **50 cards**, report the rejection rate, and **stop**. If
  it rejects half, the gate is wrong, not the corpus.
- Always set `PIPELINE_MAX_USD` on every pipeline invocation.
- Total approved for this work is **$20**. Report cumulative spend in every status report.

**3. Only you touch the shared files.**
- `web/scripts/check-*.ts` and `.github/workflows/ci.yml` are yours alone. Unit agents never edit
  them, and a diff that does is sent back.
- New Playwright specs need their names registered in the `e2e-shard` matrix **before** the agent
  starts, plus a `PENDING` entry in `check-shards.ts`. A name is a **substring filter on the
  path**, so it must not contain `feed`, `coach`, `today`, `friends`, `admin`, `checkin`,
  `offline`, `brand`, `a11y`, `roadmap` or `mock-picker` — otherwise two shards claim one spec and
  `check:shards` refuses it.
- If a ceiling fails, the agent reports the number it measured. It does not raise it.

## Accept a part as done only when

- Its PR is open against `main` and **every CI check passes**, and
- **no test passed on a retry.** Open the `e2e feed` / `e2e coach` job log and grep for
  `retry #`. A retry-passing test is a failing test — one survived three all-green CI runs on
  this repo before anyone read the log.
- The agent reported: every gate's result, the measured token count and bundle KB, how many times
  it ran its spec, its decisions with what each costs if wrong, and anything unverified.

If an agent reports a gate failure it cannot fix inside its scope, do not let it widen scope or
weaken the gate. Collect it and report.

## What to report

A table: part, branch, PR, CI state, retries seen, gate failures, spend so far, decisions needing
a human. Then one line on what is left, and **explicitly name anything waiting on a human**: the
production migration, the costed go-aheads at Gates 1 and 2, the 94-card review at Gate 3, and
the final publish.

## The one thing to judge, not just build

At Gate 3, the ~94-card review samples **two cards per archetype**, and the question per card is
not "is this correct" — the gates answer that — it is **"does this archetype earn a place"**.

The first thing to look at: a Hard card carries a why-step, and a correct answer with the wrong
reason is marked **wrong**. That rule follows from two other decisions rather than being chosen,
and if the wrong reasons are not genuinely plausible it punishes readers for a writing failure.
Flag it for the owner rather than shipping it on the strength of the plan.
