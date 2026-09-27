# Content rebuild: from scraped chunks to an authored lesson layer

Written 2026-09-27 after Aman reviewed the library and card drafts and found
them unusable. This document records what is actually wrong, why, and the plan
we agreed. It supersedes the content half of `.planning/SPEC.md` part 1.

## What we shipped, measured

`documents` (5,290 rows) is raw scraped source text rendered to users verbatim.

| Symptom | Count |
|---|---|
| Documents over 8,000 chars (book chapters, not lessons) | 196 |
| Documents under 400 chars (fragments) | 398 |
| Documents containing raw HTML tags | 1,115 |
| Documents with PDF ligature corruption (`deﬁnition`, `tr ansforming`) | 91 |
| Documents that are pipe tables (often just link lists) | 322 |
| Topics with no document at all | 41 of 274 |

Worked examples Aman hit:

- `ostep:67e179be074f96fd` — a whole OSTEP chapter, 25,148 chars, with a stray
  page number as line one. The `ostep` source averages 22,925 chars/doc;
  `little-book-of-semaphores` averages 38,551.
- `ml-interviews-book:574a52e0936d2f4a` — not prose. A *list of questions* from
  the book, stored as something to read.
- `awesome-lld:97ce13dc0928f2e3` — a markdown table of links to algomaster.io.

## Three structural faults

**1. We published the retrieval corpus as the reading experience.** The pipeline
was built to collect and chunk. Chunks are fine for grounding Coach — an
embedding model does not care about ligatures — and worthless for a human who
wants to learn a topic. Nobody ever wrote the layer in between.

**2. Cards were generated from a chunk, with the chunk in context**, so they
reference text the learner never sees: *"In the reference solution, after
removing the run starting at x up to y-1…"*. 83 cards match that phrasing
directly; 147 typed cards are plainly MCQ-shaped.

**3. Card coverage follows scraping volume, not importance.** This is the one
that would have bitten hardest in week 3:

| Domain | Cards | Topics covered |
|---|---|---|
| system_design | 2,755 | 54/55 |
| dsa | 2,488 | 24/24 (attached to problems) |
| cs | 1,969 | 25/26 |
| java | 797 | 38/38 |
| sql | 547 | 32/34 |
| **ai** | **0** | **0/40** |
| **lld** | **0** | **0/35** |
| **behavioral** | **0** | **0/22** |

`cs-http-https` alone holds 476 cards because we scraped a lot of HTTP pages.
97 topics hold none because the run hit the $22 cap before reaching them.

## What is not broken

- **Nothing reached the Feed.** All 8,556 cards are still `draft`. The admin
  review gate did the job it was built for.
- **Card quality is bimodal, not uniformly bad.** Sampled at random: *"How does
  the CAP theorem define availability?"* and *"…at most two non-overlapping
  transactions — which algorithmic pattern fits, and why?"* are good,
  self-contained questions. The generator works; it was fed the wrong input.
- The collection work — 3,693 problems, the taxonomy, the vector index — is
  sound. **The sources are not the problem. Our treatment of them is.**

## The plan

### Phase 0 — product fixes, no AI spend

- DSA topic pages render the pattern trick and its problems. They have no
  documents by design and should never have shown an empty page.
- Behavioural topics render the story builder, not a lesson. That content is
  the user's own, and `stories` already exists.
- The library stops linking raw documents entirely.

### Phase 1 — author a lesson layer

One lesson per content topic (~233), generated from that topic's chunks via the
existing vector index, to a fixed contract:

- What it is · why interviewers ask it · the mental model · 3–5 key points ·
  one worked example · common traps · "you should be able to answer"
- 600–900 words, no HTML, no ligatures, no link tables, no reference to "the
  passage" or "the text", citations back to source ids.

Validated structurally before it is ever stored. A lesson that fails the
contract is regenerated, not published.

### Phase 2 — regenerate cards from lessons

Budget per topic by importance (~8–12), not by how much we happened to scrape.
Generated from the lesson, so the card cannot reference invisible context.

**The gate we never had:** an independent model must answer the card correctly
given *only the lesson and the question*. If it cannot, the card leaks context
or is unanswerable, and is dropped. This is automatable and cheap.

### Phase 3 — raw chunks become retrieval-only

`documents` stays in the database for Coach's `search_knowledge` and for lesson
generation. It is never rendered to a user again.

## Sources Aman proposed

Both are useful, neither can be imported.

- **roadmap.sh** (`kamranahmedse/developer-roadmap`, GitHub license
  `NOASSERTION`): *"You are allowed to use this material for personal use but
  are not allowed to use it for any other purpose including publishing … the
  content … in any form."* 90x is multi-user, so importing the content is out.
- **systemdesign.io**: states no license, which means all rights reserved.

Use both as **taxonomy validators** — check our 274 topics against their
coverage, find the gaps, author our own material for them. Structure and "what
real interviews ask" are facts; the prose is theirs.

## Taxonomy questions for Aman

- The `ai` domain re-declares other domains: `ai-python`, `ai-sql`,
  `ai-data-structures-and-algorithms`, `ai-software-engineering` overlap the
  `sql`, `dsa` and `java` domains. Merge, or keep as ML-flavoured variants?
- 55 system_design topics with 35 of them roots is flat — likely needs grouping.
- `beh-company-specific-questions` holds 42 documents, more than any other
  behavioural topic combined. Probably a dumping ground.

## Pilot before spend

Five topics chosen to hit every hard input, not the easy ones:

| Topic | Why it is in the pilot |
|---|---|
| `cs-http-https` | 162 docs / 179K chars — can we author from too much? |
| `ai-rag-and-production-systems` | 1 doc / 1,386 chars — too little? |
| `beh-teamwork` | 0 docs — does the fallback hold? |
| `java-hashmap-internals` | 6 docs / 9,794 chars — the normal case |
| `sd-cap-theorem` | already has decent cards — do lessons make them better? |

Aman and Claude both read all five before anything scales. Budget approved up
to $30; the pilot costs cents.
