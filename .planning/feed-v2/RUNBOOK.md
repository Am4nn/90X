# Feed v2 — production runbook

> **Status 2026-10-03: Feed v2 is live.** The first release (everything from "Before you
> start" down) is history. It is kept because the reasoning is still true, not because
> the steps should be run again. **What to do now is the next section.**

## Operating the corpus now

How a card gets from staging to a reader today, and the rules that were paid for finding
out. Written after the production push, from what went wrong in it.

### The loop

1. **Generate or repair into staging.** Nothing here touches production.
2. **Gate it, in this order.**
   - `pipeline wellformed` (free, in code): limits, duplicates, answer-key shape.
   - `pipeline card-regate --no-blind`: the model gate. It sees every primitive's options.
   - `pipeline refile --apply`: moves a card rejected for the wrong archetype. It now
     **confirms its own moves** with the gate (`--check-tier smart`); `--no-check` leaves
     them unverified and they must not be published.
   - `uv run python scripts/key_audit.py`: does each answer key agree with its own
     explanation. Nothing else checks this. See `KEY-AUDIT.md`. **It writes nothing by
     itself**: read the confirmed list it prints, then reject them with `--from FILE` (or
     rerun with `--apply`), *before* the rebatch below, or the contradicting cards stay `kept`
     and get published. A card either pass called `unclear` or `missing` was not judged: resolve
     it, or leave it out of the batch. The cheap first pass also misses some (4.7% on a sample
     of 300, about half of those false on reading), and its recall over the whole corpus is
     unmeasured, so for a card that matters, confirm with a second model family (`--retest`).
   - `pipeline card-validate --drop-dupes --apply`: near-duplicates across topics.
3. **Archive before anything destructive.** `uv run python scripts/archive_rejects.py`
   writes every rejected card, with its reason, to `.data/review/rejected-cards.jsonl`.
4. **`pipeline rebatch`, then `pipeline publish`.** `rebatch` is not optional: publish only
   sends batched cards, and a dry run without it offered 943 of 6,316.
5. **Take cards live.** Normally `pipeline swap` (dry run first, read the counts).
   **Not yet: see the next rule.**

### Rules that were learned the hard way

- **Do not run `pipeline swap` until PR #76's migration is applied and a publish has
  stamped the corpus.** Today's swap activates every archetyped card that is draft, live
  *or retired*, so it puts back anything retired on purpose. Until then, take a published
  draft live with a targeted `update public.cards set status='live' where id = any(...)`.
  See `SWAP-BUG.md`.
- **A gate has to see what the reader sees.** `prompt_only` once showed options only for the
  legacy `mcq` format, so 6,702 of 7,063 cards were judged without their options and 1,035
  were rejected as "options are missing". The model was right every time.
- **A validator checks shape, not meaning.** A key can be well formed and wrong: a grid
  with a ticked cell on the wrong row passes `wellformed`. Anything that edits a key
  (a repair, a trim) must carry it, or refuse. `scripts/repair_limits.py` shows how.
- **A step that cannot verify its own output should not write it.** `refile` printed "run
  card-regate to confirm" and left it to the caller; 34 cards went live under an archetype
  that did not fit.
- **Back up before deleting from production.** 103 of 2,292 cards removed on 2026-10-03
  existed nowhere else. `scripts/prune_retired.py` writes the full rows and reads the file
  back before it issues a delete, and runs in a transaction that rolls back on any
  unexpected count. The four tables that reference a card all `ON DELETE CASCADE`, so a card
  with history is never deleted.
- **One DuckDB writer at a time.** Stopping a background job can orphan its Python child,
  which keeps the lock; the next run dies on `staging.connect()` and exits 0. Find the PID in
  the error and kill it.
- **`PIPELINE_MAX_USD` is a cap on lifetime spend, not on the run.** Set it above what the
  ledger already shows, or every call raises `BudgetExceeded` at once.
- **Open the database read-write for any run that calls a model**, even a dry one. Cost is
  logged there; opened read-only, every call fails *after* the API has answered and been paid.
- **Production's `DATABASE_URL` is what `tests/test_publish.py` runs against** (rolled
  back). After a migration they fail until it is applied. `tests/test_swap.py` is different:
  it needs `TEST_DATABASE_URL`, a **local** database, and refuses a hosted one.

### Running on OpenCode Go instead of paying per token

OpenCode Go is a $10/month subscription over 36 models. Calls to it are logged with their
tokens at a cost of **$0**, so they do not touch the lifetime ceiling.

```
AI_API_KEY=<OPENCODE_GO_API_KEY from pipeline/.env> AI_BASE_URL=https://opencode.ai/zen/go/v1 AI_MODEL_FAST=deepseek-v4-flash AI_MODEL_SMART=deepseek-v4-pro uv run python ...
```

The client sends the `x-opencode-session` header and a `90x-pipeline` user agent it requires.
The 5-hour window is 20% of the month's allowance and the week is 50%. At a limit it falls
back to free models only, **unless "Use balance" is on in the console, which spends Zen
credits. Leave it off.** The model list is `GET /models`.

---

# The first release (history)

Rewritten 2026-10-02 after the corpus review and the rebalance run. The four
production steps were a human's, in this order. Everything before them was done and
local when this was written.

## Before you start: one thing to know about the tests

`pipeline/.env`'s `DATABASE_URL` points at **production**, so `pytest
tests/test_publish.py` connects to the live database. It only ever runs inside a
transaction it rolls back, but it means the four failures you will see there
(`column "archetype" of relation "cards" does not exist`) are not a local setup
problem — they are production telling you **step 1 has not been run yet.** Those
tests pass against the local stack today, and they will pass against production
once the migration is applied.

## What is already done, locally

1. **Corpus rebalanced and extended.** `run_feed_v2.py --reconcile` trims each
   topic's surplus archetypes and writes only its shortfall, then gates and
   repairs. Run under `run_id="feed-v2-rebalance"`, capped at `PIPELINE_MAX_USD`,
   waits for the DeepSeek off-peak window before spending anything.
2. **The catalogue covers every area.** 56 archetypes over 11 primitives across
   all eight domains; `ai`, `lld` and `behavioral` were excluded by a missing area
   tag through the whole first run.
3. **219 unanswerable cards rejected** by `pipeline wellformed --apply`, and the
   gate now runs that check over every primitive rather than `pick_one` alone.
4. **Swap prep.** `pipeline swap` is dry-run by default and retires only within
   the areas the catalogue covers.

Staging is backed up at `.data/staging.duckdb.before-reconcile`.

## Production steps, in order — the order is not a preference

### 1. Apply the migration

`supabase/migrations/20260930000024_feed_v2.sql` — purely additive: adds
`cards.archetype`, `picked`, `constraints`, `pairs`, `value`, `tolerance`,
`why_step`, `observed_attempts`, `observed_correct`; drops `cards_format_check`.

Apply it through the normal migration path. Confirm with:

```
select count(*) from information_schema.columns
where table_name = 'cards' and column_name = 'archetype';
```

### 2. Deploy the app

Parts A–D must be live **before** the flip, because the new corpus cannot be
rendered by code that does not exist yet. Publishing before deploying was the
2026-09-29 outage.

What this deploy must include, beyond A–D:

- the `compose` primitive and its answer path (behavioural written answers)
- `FEED_AREAS` covering eight areas — without it `cardView` returns null for every
  ai, lld and behavioural card and the Feed silently serves none of them

### 3. Publish the new corpus as `draft`

```
cd pipeline
uv run python -m pipeline publish
```

Upserts with `status='draft'`, which is invisible: the `cards_read` policy is
`status='live' and not hidden`. **Nothing becomes live.**

This step used to be unable to complete. `_retire_superseded_cards` deleted every
published card staging no longer had, and since regeneration removes a topic's old
cards from staging, it raised `StudyHistoryAtRisk` over the entire old corpus and
rolled the whole transaction back. It now deletes only `draft` cards staging has
dropped and leaves `live` and `retired` alone, because:

- a card a reader could have seen is **retired, not deleted** — `card_state` stays,
  so nobody's readiness dial drops on release day; and
- publish must not retire them either, or the Feed has nothing live between this
  step and the flip.

**Do not pass `--force`.** If it raises, stop and read what it names: the guard is
scoped to drafts now, so a raise means a draft card genuinely carries answers.

### 4. Flip

```
uv run python -m pipeline swap            # dry run: prints the counts
uv run python -m pipeline swap --apply    # retire old, activate new
```

One transaction. It retires live cards **only in the areas the catalogue covers**
and activates every `draft` card with an archetype. `card_state` on retired cards
is kept, unscheduled.

The dry run prints `kept_live_uncovered_area`. That number should be **0** once
the rebalance run has covered all eight areas; if it is not, it is naming cards in
an area no archetype reached, and they stay in their old format rather than being
retired into nothing.

## Verify before step 4

- [ ] `cards.archetype` exists in production (step 1)
- [ ] the app is deployed, and a behavioural card renders its write-in box (step 2)
- [ ] the `swap` dry run's `activate_draft_archetyped` is close to the corpus size
      the run reported, not zero
- [ ] `kept_live_uncovered_area` is 0, or you know which area it names

## After the flip

- `pipeline status` for the corpus and the spend.
- Answer a few cards per area, including one behavioural write-in: that is the only
  path where a model runs at answer time, and the one most worth seeing work.
- The Gate 3 review pack is **112 cards**, two per archetype. The question per card
  is *does this archetype earn a place*, not *is this correct* — the gates answered
  that. The first thing to judge is whether a why-step's wrong reasons are
  genuinely plausible: right-answer-wrong-reason is the harshest rule in the design
  and the most likely to be wrong in practice.

## Spend

Read it off the pipeline rather than assuming:

```
uv run python -c "import duckdb; c=duckdb.connect('../.data/staging.duckdb', read_only=True); print(c.execute('select run_id, round(sum(cost_usd),4) from llm_calls group by 1 order by 2 desc').fetchall())"
```

First run `feed-v2-full` $17.19. The rebalance runs under `feed-v2-rebalance` with
its own cap, so its figure is separate rather than counting against the first.
