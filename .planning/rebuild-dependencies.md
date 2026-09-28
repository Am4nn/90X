# What else touches what we are changing

Written 2026-09-27, after Aman asked whether the rebuild was planned well
enough, given how much was being discovered mid-flight.

The checking mechanisms are working: tests, the fact checker, CodeRabbit and
CI have each caught real defects. What was missing is a pass over *second
order* consequences - what else depends on the things being deleted. This is
that pass. Six areas, checked against the live database and the code.

## 1. The Sources line was decided and never built

**Severity: a decision dropped.** Aman's ruling was "retrieval only + link to
real sources": documents disappear from the library, and each lesson shows a
Sources line naming the real books and repos, linking to the originals.

Three things are wrong:

- Nothing renders a Sources line. It was never built.
- `lessons.source_refs` holds document ids (`ostep:67e179be074f96fd`), and
  documents no longer exist in Supabase. The references dangle.
- ~~`_source_rows` may not publish OSTEP's row at all.~~ **Wrong when
  written:** `_source_rows` always publishes every entry in `sources.py`, so
  the rows were there. Only the refs were broken.

**Proposed:** resolve `source_refs` at publish into
`{source_id, name, url}` by looking up each document's source in staging, and
render them under the lesson. Restore documents' source ids to
`_source_rows`, read from staging where documents still live.

## 2. Regenerating cards would have destroyed study history

**Severity: harmless today, purely by luck.** Every table hanging off a card
cascades on delete:

| Child | On delete |
|---|---|
| `card_reviews` | CASCADE |
| `card_state` | CASCADE |
| `card_flags` | CASCADE |
| `batch_review_items` | CASCADE |

Scrapping 8,556 cards to regenerate them therefore erases every answer, every
spaced-repetition interval and every flag. It costs nothing **only because
`card_reviews` and `card_state` both hold 0 rows** - the Feed has never been
used. Three weeks into real study, the same command would have silently wiped
the history and nobody would have noticed until the ladder went empty.

**Proposed:** a guard in the card runner that refuses to delete cards when
`card_reviews` is non-empty, unless explicitly forced. The safety should come
from a rule, not from the Feed happening to be unused.

## 3. Lesson cards cannot reach the admin review screen

**Severity: blocks Aman's card review.** `/admin/cards` lists *batches* and
samples within them: `sampleIds` reads `cards.risk`, the listing counts by
`batch_id`, and `sourceTitles` renders `cards.source_refs`.

Cards generated from lessons are written with none of those - no `batch_id`,
no `risk`, no `source_refs`. They would not appear on the review screen at
all, which is exactly where Aman said he wants to review a sample before bulk
generation.

**Proposed:** group lesson cards into review batches by domain as they are
written, carry the gate's confidence into `risk` so the sample is drawn from
the doubtful ones first, and set `source_refs` to the lesson they came from.

## 4. Readiness and the diagnostic assume cards exist

**Severity: none, but worth stating.** Area accuracy comes from card attempts
(`readiness.ts`), and the first-visit diagnostic draws from live cards. With
cards regenerated and no attempts yet, both fall back to "No data yet", which
is the designed behaviour for an empty area. No action.

## 5. Two summaries, no rule for which wins

**Severity: cosmetic.** `topics.description` came from the taxonomy;
`lessons.summary` is derived from the lesson's opening sentence. The library
renders `summary ?? description`, so which one a reader sees depends on
whether a lesson published. They will drift.

**Proposed:** the lesson's summary is the one users see, and
`topics.description` becomes pipeline-only input to lesson generation. One
line of intent, not a migration.

## 6. Coach tools are clean

**Severity: none.** `find_cards`, `get_weak_spots` and the rest reference
cards, problems and topics - not documents. `search_knowledge` reads the
vector index, which now carries lessons with absolute links to their own
pages. Nothing to change.

---

## What this says about the planning

Items 4 and 6 were fine. Item 5 is cosmetic. Items 1, 2 and 3 are real, and
they share a shape: each is a consequence of *deleting* something, and none
of them would have been caught by a test, because nothing is broken - the
Sources line simply does not exist, the cascade simply does not fire, and the
admin screen simply shows nothing.

Tests catch what breaks. They do not catch what quietly stops happening. That
is the gap, and a dependency pass like this one is the thing that closes it.
Worth repeating before the next deletion, not after it.


---

## Fixed 2026-09-28

All three, plus two bugs the fixes uncovered.

1. **Sources line.** `source_refs` resolve at publish into `{id, name, url}`
   from the source id prefix, and the lesson page renders a "Written from"
   line with real titles ("Operating Systems: Three Easy Pieces", not
   "ostep"). One bullet above was wrong: the `sources` rows were always
   published.
2. **The cascade guard.** `publish` now removes cards staging no longer has,
   and refuses when any of them holds a card answer, naming the count. The
   safety is a rule, not the Feed happening to be unused. `--force` exists
   and says what it costs.
3. **Lesson cards reach the review screen.** They carry `kept`, `quality`,
   `source_refs`, and batch through the existing `rebatch` into ~16 area
   batches, inside Aman's 20-25 cap.

Uncovered on the way:

- **`risk` is not risk.** `pickReviewSample` sorts ascending and reviews the
  first half, treating an unscored card as safest, so the column holds
  *confidence*: low means doubtful. The first version of the gate mapping
  inverted it, which would have put the cards the gate liked most in front of
  the reviewer and hidden the doubtful ones. Pinned by a test.
- **Card ids must be uuids.** `public.cards.id` is a uuid, so the readable
  `sliding-window:l0` ids would never have published. They are uuid5 of the
  slug and index now, so regenerating a topic reuses ids rather than
  duplicating every card.
