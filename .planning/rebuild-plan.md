# Content rebuild: everything left, in order

Written 2026-09-28. The decisions are all made; this is the execution list.
Two tracks run in parallel because only one of them needs the staging
database, which is held by whatever pipeline command is running.

Nothing here is optional or "later". A thing that is not worth doing gets
deleted from this file, not left in it.

## Track A — content pipeline (serialised: one holds the database)

| # | Step | Needs | Cost | State |
|---|---|---|---|---|
| A1 | Rewrite the 32 held-back lessons under the new policy | — | ~$0.90 | running |
| A2 | Cross-lesson consistency check per area, then fix what it names | A1 | ~$2 | built, not run |
| A3 | Cards for every topic with a lesson (8-12 by importance) | A1 | ~$3 | built, piloted |
| A4 | Rebatch cards into area batches (~16, inside the 20-25 cap) | A3 | free | built, not run |
| A5 | Retire the 8,556 chunk-generated cards from staging | A4 | free | guard built |
| A6 | Publish everything to Supabase | A5 | free | built, run once |
| A7 | Re-embed the vector index: lessons plus chunks | A6 | free tier | built, not run |
| A8 | Taxonomy gap report for Aman to cut down | A6 | ~$1 | built, not run |

## Track B — Feed declarations (web only, no database lock)

| # | Step | State |
|---|---|---|
| B1 | `outcome` gains `new_to_me` and `known`, kept out of every score | done |
| B2 | Eligibility rule for "I already know this" | done |
| B3 | `declareCard` service and server action | **next** |
| B4 | Two buttons in the card UI, with teach-mode reveal | **next** |
| B5 | Weak pool restricted to topics with a real answer | to do |
| B6 | Coach reads declared gaps in `get_weak_spots` | to do |
| B7 | Planner pulls declared gaps into tomorrow's missions | to do |
| B8 | Weekly review counts declarations | to do |

## Track C — quality passes on the generators

| # | Step | Why | State |
|---|---|---|---|
| C1 | Rewrite a rejected card once before discarding it | recovers ~160 cards across the run | to do |
| C2 | Version and engine labels on SQL/Java/network claims | "in PostgreSQL 16", "Java 17+" | to do |
| C3 | MCQ distractors must test a misconception, not pad the list | second reviewer's point | to do |
| C4 | Spread difficulty within a topic: recall, explain, apply | second reviewer's point | to do |

C1 must land before A3 runs, or the rejected cards are lost rather than
rewritten. C2-C4 also belong before A3, since they change what gets written.

## Track D — verification and merge

| # | Step | State |
|---|---|---|
| D1 | Read a topic page, the roadmap and the Feed in a browser with real data | nothing has rendered yet |
| D2 | Full check suite plus the four real-database checks | passing |
| D3 | Merge PR #19 to main, which deploys | after D1 |

## Order of work

1. **C1-C4 now** — they change A3's output, so they come first.
2. **A2 as soon as the database frees**, then A3, A4, A5, A6, A7, A8 in order.
3. **B3-B8 in parallel throughout**, since they never touch the database.
4. **D1 once A6 has published**, then D3.

## Known open items, tracked so they are not lost

- Six system-design lessons were written before company evidence existed.
  A1 may already have rewritten them; verify after A1 rather than assuming.
- `lessons.summary` is derived from the first sentence at publish. The model
  generates a better one that is currently discarded. Worth wiring properly
  if a summary ever reads badly.
- Nothing has been checked in a browser. Typecheck and e2e prove the code
  compiles and the fixtures work, not that a 1,100-word lesson reads well on
  a phone.
