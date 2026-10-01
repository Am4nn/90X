# Feed v2 — production runbook

Written 2026-10-02 by the orchestrator, after the autonomous full run and the
Part H swap prep. The owner (Aman) runs the four production steps below, **in
order**, after reviewing the Gate 3 pack. This file is the "stop" of the
prepare-and-stop handoff.

## What is already done (local only, no production touched)

1. **Full generation run** — `run_feed_v2.py`: write → regate (answerability +
   blind gate) → validate, `run_id="feed-v2-full"`, hard cap **$25**
   (`PIPELINE_MAX_USD`), resumable. Writer is DeepSeek V4 Pro, thinking off.
2. **Gate 3 review pack** — ~94 cards (2 per archetype) as both a web pack and
   a markdown file (see `review_pack` output).
3. **Swap prep (Part H)** — `publish.py` now carries the archetype/answer
   columns; new `pipeline/src/pipeline/cards/swap.py` + `pipeline swap` command
   (dry-run by default).

## Production steps (in order — the order is not a preference)

### 1. Apply the migration

`supabase/migrations/20260930000024_feed_v2.sql` — purely additive: adds
`cards.archetype`, `picked`, `constraints`, `pairs`, `value`, `tolerance`,
`why_step`, `observed_attempts`, `observed_correct`; drops `cards_format_check`.
Apply it to production Supabase through the normal migration path.

### 2. Deploy the app

Make sure the Feed v2 app code (parts A–D: schema/grader/UI/selection) is
deployed to Vercel. **The flip must run only after the app can render the new
cards.** Publishing before deploying was the 2026-09-29 outage.

### 3. Publish the new corpus (as `draft`)

```
cd pipeline
uv run python -m pipeline publish
```

Upserts the new corpus with `status='draft'` (invisible: the `cards_read` policy
is `status='live' and not hidden`). **Nothing becomes live.**

### 4. Flip (swap)

```
uv run python -m pipeline swap            # dry-run: shows the counts
uv run python -m pipeline swap --apply    # retire old live, activate new draft
```

One transaction retires every `live` card and activates every `draft` +
`archetype is not null` card. `card_state` on retired cards is **kept**
(unscheduled), so nobody's readiness dial drops.

## Verify before step 4

- [ ] Migration applied (step 1): `cards.archetype` exists in prod.
- [ ] App deployed (step 2): the new card UIs render.
- [ ] `swap` dry-run shows the expected counts — old live ≈ 2,808, new draft ≈ ~2,900.

## Warnings (read before running anything against prod)

- **Order: deploy before flip, never the reverse.** The new corpus cannot be
  rendered by code that does not exist yet.
- **Retire, not delete.** The generation run replaced the old cards in staging,
  so `publish`'s `_retire_superseded_cards` may try to *delete* prod cards that
  staging no longer has (the old corpus), and its `StudyHistoryAtRisk` guard
  will refuse if those cards hold answers or schedules. That guard is doing its
  job. **Do not pass `--force`** to work around it — that erases study history.
  The retirement is meant to be the `swap` flip (status → `retired`), which
  keeps `card_state`. If `publish` raises `StudyHistoryAtRisk`, stop and
  reconcile whether the old cards should be retained in staging or retired by
  the flip before continuing.
- **`swap` defaults to dry-run.** Only `--apply` writes, and only against the
  database `DATABASE_URL` points at. Never point that at prod from a real
  `.env.local` by accident.
- **Budget.** This run's spend is recorded against `run_id="feed-v2-full"` and
  is capped at $25. Read the figure off the pipeline's own spend line before
  assuming anything.

## Run results (filled in 2026-10-02)

- **Final corpus: 2,401 archetyped `draft` cards.** Below the ~2,500 floor the
  plan named — see the finding below.
- Gate: 2,607 judged · 456 objected (17%) · 250 repaired · **206 dropped (8%)**.
- **Spend: $17.19** against `run_id="feed-v2-full"`, within the $25 cap
  (lifetime $19.42 including the $2.22 of pre-run legacy calls).
- **1,301 old cards remain** (`archetype IS NULL`): `ai` 416 · `lld` 342 ·
  `behavioral` 222 · ~321 across dsa/system_design/cs/java/sql. These areas have
  **no eligible archetype** in the Feed v2 catalog, so they were not regenerated.
  Decide whether the swap should retire them (it retires every `live` card) or
  leave them be — the behavioural cards were meant to stay ("none retired").
