You are building **Part H of Feed v2: publish and the swap**.

**Worktree** `../90X-wt-fv2/h` · **Branch** `feed-v2-swap` · **No Playwright spec** — Python
pipeline. **H is prepared and verified locally, then stops and reports.** It never publishes to
production.

The rollout order is not a preference: publish new cards as `draft` (invisible), deploy the app,
then one statement flips new → `live` and old → `retired`. Publishing before deploying is the
mistake that took production down on 2026-09-29.

## Read these first, in this order

1. `.planning/feed-v2/plans/prompts/SETUP.md` — §3 (pipeline parts) especially.
2. **`.planning/feed-v2/plans/H-publish-swap.md` — your plan.** The swap statement, the
   `card_state` rule, the traps.
3. `.planning/feed-v2/plans/README.md`
4. `.planning/feed-v2/DECISIONS.md` round 4 — the draft-then-flip rollout and the FSRS-history
   rule.
5. `pipeline/src/pipeline/publish.py` — read before changing; keep the `StudyHistoryAtRisk` guard.

## The traps that will cost you most

1. **Never `pipeline publish` against a real `DATABASE_URL`.** Local stack only.
2. **The flip runs after the deploy, never before.** The new corpus cannot be rendered by code
   that does not exist yet.
3. **`swap` defaults to dry-run.** `--apply` exists but H does not run it against anything but
   the local stack. The production flip is a human's.
4. **Do not delete `card_state`.** "Retired" means unscheduled, not gone. If
   `StudyHistoryAtRisk` fires, the corpus is not staged as expected — stop and report.

## Verification

`uv run pytest`, then against the **local** stack: publish a small draft corpus, run
`swap --dry-run` and confirm the SQL flips exactly new-draft→live and old-live→retired and leaves
`card_state` untouched; then run it locally and confirm the local Feed shows the new cards and no
readiness dial moved. Report every step and stop.

Report back as SETUP.md §10 describes — and state explicitly that the production publish and the
flip remain a human step.
