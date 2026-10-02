# Feed v2 — production runbook

Rewritten 2026-10-02 after the corpus review and the rebalance run. The four
production steps are a human's, in this order. Everything before them is done and
local; nothing here has touched production.

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
