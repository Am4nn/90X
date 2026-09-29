# Part H — publish and the swap

**Branch** `feed-v2-swap` · **Worktree** `../90X-wt-fv2/h` · **No Playwright spec** — Python
pipeline + one prepared, verified statement. **H is prepared and verified locally, then stops
and reports.** It never publishes to production.

H is the rollout. The order is not a preference: **publish new cards as `draft` (invisible),
deploy the app, then one statement flips new → `live` and old → `retired`.** Publishing before
deploying is the mistake that took production down on 2026-09-29.

## Scope

- Make `publish.py` write the new corpus as `draft` and never flip anything to `live`.
- Prepare the single flip statement (new `draft` → `live`, old `live` → `retired`).
- Keep `card_state` on retired cards — **unscheduled, not deleted** — so nobody's readiness dial
  drops on release day.
- Verify the whole sequence against the local stack; report and stop.

## Files

**Modify**
- `pipeline/src/pipeline/publish.py` — publish cards as `draft` only (it already does); add the
  archetype/answer columns to the card upsert (Part A added them to Supabase).
- `pipeline/src/pipeline/cards/swap.py` (new) — the prepared, idempotent flip: new `draft` →
  `live`, old `live` → `retired`, `card_state` rows left in place.
- `pipeline/src/pipeline/commands.py` — a `swap` command that prints what it would do and, with
  an explicit `--apply`, runs it. Default is dry-run.

## Reuse, do not rewrite

```
# publish.py (today)
def publish(con, pg, dry_run=False, force=False) -> dict;
def _publish_cards(con, cur) -> dict;       # writes cards as 'draft' — keep, extend columns
def staged_card_ids(con) -> list[str];
def _retire_superseded_cards(con, cur, force) -> int;  # the StudyHistoryAtRisk guard
def run(con, url, dry_run=False, force=False) -> dict;

# commands.py
def publish(args, con) -> None;             # the existing publish path; leave it

# staging.py — cards.status already has 'draft'/'live'/'retired'; card_state mirrors Supabase
```

The flip is data, not a new schema: an `UPDATE public.cards SET status = ...` guarded to run once.

## The swap, exactly

1. `pipeline publish` upserts the new corpus with `status = 'draft'`. Draft cards are invisible
   (`cards_read` policy: `status = 'live' and not hidden`). **Nothing becomes live.**
2. The app deploys (a human does this — not H).
3. One statement, run after the deploy and only after it:

```sql
update public.cards set status = 'retired' where status = 'live';
update public.cards set status = 'live'    where status = 'draft' and archetype is not null;
```

`card_state` and `card_reviews` on the retired cards are **kept**. They are orphaned (the card
is retired) but still readable; deleting them would drop everyone's readiness dial and erase the
only record of what people actually practised (DECISIONS round 4).

## Traps

- **Never run `pipeline publish` against `DATABASE_URL` from a real `.env.local`.** The local
  stack only. The orchestrator reports the production publish and the flip as a human step.
- **The flip runs after the deploy, never before.** The new corpus cannot be rendered by code
  that does not exist yet; publishing-before-deploying is the outage.
- **`swap` defaults to dry-run.** `--apply` exists but H does not run it against anything but
  the local stack. The production flip is a human's.
- **Do not delete `card_state`.** "Retired" means unscheduled, not gone. The
  `StudyHistoryAtRisk` guard in `_retire_superseded_cards` exists precisely to stop a delete
  that erases history — respect it; if it fires, the corpus is not staged as expected.

## Verification

`uv run pytest` in `pipeline/`, then against the **local** stack: publish a small draft corpus,
run `swap --dry-run` and confirm the SQL it prints flips exactly new-draft→live and old-live→
retired and leaves `card_state` untouched; then run it locally and confirm the local Feed shows
the new cards and no readiness dial moved. Report every step and stop.

## Decisions (with cost if wrong)

- **The flip is one idempotent statement, not a per-card loop.** Cost if wrong: a partial flip
  leaves some cards live and some retired with no way to know which, mid-release.
- **Retired cards keep their `card_state`.** Cost if wrong (deleting): every reader's readiness
  dial drops on release day with no explanation — the exact complaint the plan names.
