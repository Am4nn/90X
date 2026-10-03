# `swap` activates cards the corpus has dropped

Found 2026-10-03, during the repair pass, by a dry run that did not reconcile.

## What happens

`cards/swap.py` activates with:

```sql
update public.cards set status = 'live'
 where archetype is not null and status in ('draft', 'live', 'retired')
```

Including `retired` is deliberate, and the comment says why: a regenerated card
whose question did not change keeps its id, and `publish` leaves `status` alone,
so a swap that looked only at `draft` would leave it retired.

What it does not check is whether the card is still **in** the corpus. A card
deliberately retired because staging rejected it is archetyped and retired, so
the next swap puts it straight back in front of readers.

## How it surfaced

After the refile verification retired 51 cards that did not fit their archetype,
and 40 repaired cards were published, the dry run read:

```
would retire 3721 live cards and activate 3812 draft archetyped cards
```

Production held 3,721 live, 2,316 retired and **40** archetyped drafts. 3812 is
3721 + 40 + 51 — the 51 being exactly the cards just retired for not fitting.
Applying it would have undone the verification that found them.

Worked around by activating the 40 drafts directly. The swap itself is unchanged
and **must not be run until this is fixed**.

## Why the obvious fix does not work

Batch membership does not separate them: all 51 still belong to batches that
exist in production, because they were published in an earlier round and
`_retire_superseded_cards` is scoped to drafts.

## What a fix needs

Production has to be able to tell "this card is in the current corpus" from "this
card was in it once". Options, roughly in order of preference:

1. **Have `publish` mark the corpus it just sent** — a publish id or a timestamp
   stamped on every upserted row — and have `swap` activate only rows carrying the
   latest one. This makes the question answerable in production, which is where
   `swap` runs.
2. **Have `publish` retire what it no longer sends**, widening
   `_retire_superseded_cards` past drafts. Closer to correct in principle, but it
   was narrowed to drafts for a reason and widening it needs its own test.
3. Pass the kept id list from staging into `swap`. Works, but makes `swap` depend
   on staging, which it currently does not.

Whichever is chosen, the test is the case above: a card retired for a reason, a
later publish that does not include it, and a swap that leaves it retired.
