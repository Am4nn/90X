# Part G — review (the ~94-card sample, rendered for humans)

**Branch** `feed-v2-review` · **Worktree** `../90X-wt-fv2/g` · **No new Playwright spec** — the
admin render is covered by `e2e/admin.spec.ts`, which must keep passing. Depends on **B** (the
answer shapes) and **C** (the primitives, so a reviewer can see what a reader sees).

G makes the review sample per-archetype and makes the admin review screen render every
primitive. The verdict is per archetype — *does this earn a place* — not per card.

## Scope

- `review_pack.py` samples **two cards per archetype, ~94 cards**, grouped by archetype, not
  shuffled.
- `web/src/app/admin/cards/**` renders every primitive: chosen, ordered (constraints), mapping
  (pairs), number (value ± tolerance), the why-step, tap-in-place and assemble snippets.

## Files

**Modify**
- `pipeline/src/pipeline/cards/review_pack.py` — the sample becomes two-per-archetype, grouped.
- `web/src/lib/admin/cards.ts` — `batchForReview`/`ReviewCard` carry the new answer-definition
  fields and the why-step.
- `web/src/app/admin/cards/[batchId]/review.tsx` — render the new fields per primitive.
- `web/src/app/admin/cards/[batchId]/page.tsx` — the verdict UI notes the archetype.

## Reuse, do not rewrite

```
# review_pack.py (today)
def sample(con, size=SAMPLE) -> list[dict];   # replace the selection, keep report() shape
def selector(con, slug, prompt) -> str;
def report(con) -> str;

# web/src/lib/admin/cards.ts (today)
export async function batchForReview(batchId) -> { batch, sample: ReviewCard[] };
export type ReviewCard = ...;                 # add archetype, picked, constraints, pairs, value, tolerance, whyStep
# web/src/lib/admin/review.ts
export function stringList(value): string[];  # reuse for the jsonb columns
# web/src/components/markdown.tsx — Markdown
# web/src/components/feed/primitive/* — the real screens, so the admin render can mirror them
```

`batchForReview` already reads `cards.*`; add the new columns to its select. The review screen
today renders `options` as an `<ol>` and `keyPoints` as a `<ul>`; add a per-primitive block that
shows the answer-definition (e.g. ordered constraints as "before: a → b · b → c", mapping as
"left ↔ right" rows, number as "10 ± 0.5", why-step as "reason: the correct option, with the
distractors"). Read the C parts' components to keep the vocabulary identical.

## The sample — two per archetype

`review_pack.py` today picks 25 cards, one per topic, least-confident first. Replace that with:
**two cards per archetype, across the 47 archetypes → 94**, grouped by archetype (not shuffled),
still showing each card's lesson and gate confidence, still ending with the rejected cards and
the gate's reasons.

## Traps

- **The review question is "does this archetype earn a place", not "is this correct".** The
  gates answer correctness. The sample must be grouped by archetype so a human can judge a
  *kind* of question, not 94 individual cards.
- **Do not touch `e2e/admin.spec.ts`** unless your render change breaks it; if it does, update it
  and say so prominently. It is the existing contract for `/admin/cards`.
- **The why-step distractors must be visible and honest.** The first thing the owner judges at
  Gate 3 is whether wrong reasons are genuinely plausible — the review screen must show them
  plainly, not bury them in raw JSON.
- **Do not touch the pipeline's `gate.py`/`fix.py`/`regate.py`.** You consume the staged cards,
  you do not re-gate them.

## Verification

`uv run pytest` in `pipeline/`, then the full web README list, plus `e2e/admin.spec.ts` with
`--retries=0` three times. Screenshots at 390px and 1440px of the review screen showing one card
of each of the new shapes. Report token count and bundle KB.

## Decisions (with cost if wrong)

- **94 = 47 × 2.** Two per archetype, not a flat 100. Cost if wrong: a flat sample over-represents
  pick-one (20 of 47) and under-represents the new primitives, which is exactly the bias the
  review exists to catch.
