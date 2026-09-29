You are building **Part E of Feed v2: generation (pipeline)**.

**Worktree** `../90X-wt-fv2/e` · **Branch** `feed-v2-generation` · **No Playwright spec** — this
is the Python pipeline. You depend on **A** (the pipeline reads `archetypes.json` directly).

You change how cards are written: the writer **never chooses the format**. It is asked for one
named archetype and writes exactly that one thing, and may refuse (the budget refills). Hard
cards may draw on `problems.statement_md` and `pattern_tricks`.

## Read these first, in this order

1. `.planning/feed-v2/plans/prompts/SETUP.md` — §3 (pipeline parts) especially.
2. **`.planning/feed-v2/plans/E-generation.md` — your plan.** The budget, the writer, the Gate 1
   trial, the traps.
3. `.planning/feed-v2/plans/README.md`
4. `.planning/feed-v2/DECISIONS.md` round 3 — the difficulty rubric and the sourcing rule.
5. `pipeline/src/pipeline/cards/from_lessons.py`, `run_lessons.py`, `generate.py` — read before
   changing; the plan lists what to split and what to keep.

## The traps that will cost you most

1. **Never run `pipeline publish`.** You write staging (`.data/staging.duckdb`) only.
2. **The writer must never choose the format.** If the prompt lets the model pick, the corpus
   becomes 85% MCQ.
3. **A refusal refills, it does not abort.** A strained ordering card is worse than an absent one.
4. **`PIPELINE_MAX_USD` on every invocation**, and report cumulative `spend_usd(con)`.

## Gate 1 — measure before you spend

Pick the highest-`importance` topic with an `ok` lesson, generate its full budget, and report
cards written, tokens, `spend_usd`, and **measured cost per card**. **Then stop.** No further
generation until a human gives the go-ahead on the number you measured.

## Verification

`uv run pytest` in `pipeline/`, then run the Gate 1 trial and report the measured cost per card
and cumulative spend. No web checks apply.

Report back as SETUP.md §10 describes — and make the Gate 1 number the first line.
