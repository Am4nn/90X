You are building **Part G of Feed v2: the review sample and the admin render**.

**Worktree** `../90X-wt-fv2/g` · **Branch** `feed-v2-review` · **No new Playwright spec** — the
admin render is covered by `e2e/admin.spec.ts`, which must keep passing. You depend on **B** (the
answer shapes) and **C** (the primitives).

You make the review sample per-archetype (two cards each, ~94, grouped) and make the admin
review screen render every primitive so a human can judge a card they can actually see.

## Read these first, in this order

1. `.planning/feed-v2/plans/prompts/SETUP.md` — §3 (pipeline) and §5 (web) both apply.
2. `.planning/briefs/README.md`
3. **`.planning/feed-v2/plans/G-review.md` — your plan.**
4. `.planning/feed-v2/plans/README.md`
5. `pipeline/src/pipeline/cards/review_pack.py` and `web/src/lib/admin/cards.ts` — read before
   changing.
6. `.planning/feed-v2/DECISIONS.md` round 4 — the "does this archetype earn a place" question.

## The traps that will cost you most

1. **The review question is per-archetype, not per-card.** The sample must be grouped by
   archetype, not shuffled.
2. **The why-step distractors must be visible and honest.** The first thing the owner judges is
   whether wrong reasons are plausible — render them plainly, not as raw JSON.
3. **Do not touch the pipeline's `gate.py`/`fix.py`/`regate.py`.** You consume staged cards, you
   do not re-gate them.
4. **Do not touch `e2e/admin.spec.ts` unless your render change breaks it**; if it does, update it
   and say so prominently.

## Verification

`uv run pytest` in `pipeline/`, then the full web SETUP.md §5 list, plus `e2e/admin.spec.ts`
with `--retries=0` three times. Screenshots at 390px and 1440px of the review screen showing one
card of each new shape. Report token count and bundle KB.

Report back as SETUP.md §10 describes.
