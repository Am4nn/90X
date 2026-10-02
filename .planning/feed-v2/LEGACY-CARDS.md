# The 2,137 pre-Feed-v2 cards: retired from production, kept locally

Retired 2026-10-03, the same day Feed v2 went live.

## What they are

The card corpus from before Feed v2. They have no `archetype`, which is the one
thing that matters here: `pipeline swap` activates `where archetype is not null`,
so these were never going to be shown to a reader. They sat in production as
`status = 'draft'` — inert, unserved, and 36% of the rows in `public.cards`.

Published alongside the new corpus because `publish` sends everything
`where kept`, and nothing had yet decided what they were for.

## Where they are now

**Production:** `status = 'retired'`. Not served, not deleted.

**Staging** (`.data/staging.duckdb`): every row intact, marked

```sql
kept = false,
reject_reason = 'legacy: no archetype, retired from production 2026-10-03 (kept here for reuse)'
```

Marked rather than deleted for two reasons. A future `rebatch` leaves them out, so
a later `publish` cannot quietly reinstate them. And every column survives, so
nothing has been lost.

They are also in `.data/review/rejected-cards.jsonl`, written by
`scripts/archive_rejects.py`, which is the copy that survives a staging rebuild.

## Bringing them back

```sql
update cards set kept = true, status = 'draft', reject_reason = null
 where reject_reason like 'legacy: no archetype%';
```

Then `rebatch` and `publish`. But note what that alone does **not** do: without an
`archetype` they still will not go live, because `swap` will not activate them.

## If you actually want them in the Feed

They need an archetype, and `pipeline refile` is the tool — it moves a card to an
archetype that fits, bounded by area, primitive, difficulty, and the model answer
validating against the candidate list. Two things to know before trying:

- Refile is written for cards **rejected for the wrong archetype**, not for cards
  with no archetype at all. Check `refile.eligible()` handles a null archetype
  before assuming it will.
- Their formats are the pre-Feed-v2 vocabulary — `mcq`, `multiple_choice`, `flash`,
  `flashcard`, `short_answer`, `multi_select`, `mc`, `select_all`, `typed_answer`,
  `typed_snippet`. Feed v2's primitives are a different set, and `wellformed` only
  checks cards that have an archetype. Mapping the old formats onto the new
  primitives is the real work, not the refiling.

The cheaper source of new cards is the rejected Feed v2 corpus: 533 cards turned
down for a well-formedness limit (an `order` card with 7 steps against a maximum of
6, duplicate option text) are already in the right vocabulary and mostly need
mechanical repair. Start there.

## Why this is written down

`swap` activating only archetyped cards is the reason these were harmless, and that
is one line of SQL in `cards/swap.py`. Anyone who widens it — to publish legacy
cards, say — reinstates 2,137 cards into the Feed that no gate in Feed v2 has ever
judged: not `wellformed`, not the six gate verdicts, not the blind gate. That is the
risk this file exists to name.
