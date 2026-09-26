# 90X Spec

Personal interview-prep app for two users (me + friend). Goal: interview-ready in a set number of days.

Status: planning. Last updated 2026-09-26.

The ChatGPT research in `chatgpt-research/` is reference only. Parts of it are outdated or wrong (license claims conflict, some dataset names are unverified). This file wins where they disagree.

## Principles

- Prep hours beat build hours. If building starts eating prep time, stop adding features.
- Build small, use it for a week, then add.
- Log manually where needed. No integration is a hard dependency.

## 1. Core app

### Setup
- Name, target role, main language
- Duration: 30 / 60 / 90 days (variable)
- Hours per day available

### Today page
- 2–3 DSA problems, chosen by pattern order and difficulty
- 1 system design or CS topic
- 1 behavioral question
- Up to 2 review problems (ones I missed earlier)
- Duration controls pace: shorter campaign = more per day

### Where work happens
| Area | Where I do it | How the app knows |
|---|---|---|
| DSA | LeetCode (app links out) | I log it. Optional check via LeetCode's public recent-accepted-submissions (unofficial, may break) |
| System design | In-app AI mock interviewer | The chat and score are saved |
| Behavioral | In-app, typed STAR answer | AI score and feedback saved |
| CS topics | In-app 5-question quiz | Answers saved |

### Attempt log (DSA)
- Result: solved / with hints / failed
- Time taken
- Mistake type: missed pattern, logic bug, edge case, too slow
- One-line note

### Review rules
- Failed or needed hints → back in 3 days, then 7
- Solved clean twice → done
- 3+ misses in one pattern → more of that pattern next week

### Dashboard
- Readiness % per area (DSA, system design, CS, behavioral)
- Formula: clean solves ÷ total, weighted by difficulty
- Weakest 3 patterns
- Streak and day count

### Friend view
- Side-by-side streaks, solves, readiness

### AI mock interviewer
- Modes: system design, behavioral
- System design flow: requirements → API → data model → architecture → scaling, with follow-ups
- Ends with a rubric score and 3 things to fix, saved to the log

## 2. Feed (v1.5)

Infinite scroll of question cards. Every card needs an answer before it reveals anything.

### Card formats
- **Typed recall (default):** "Which pattern?", "Why X over Y?"
- **Flashcard:** think → reveal → self-mark (fast mode)
- **Multiple choice:** warm-up or when stuck on a topic
- **Output prediction:** code snippet → type what prints
- **Spot the bug:** tap the broken line

Format is chosen by what fits the content, not at random.

### Judging
- Each card stores a reference answer and 2–4 key points, generated offline.
- Typed answers: exact/normalized match first (instant, free). If no match, Claude judges against the key points.
- Judge returns which key points were hit. Score = points hit ÷ total. Missed points are highlighted.
- Multiple choice and output cards: compared to the stored answer, no AI.

### After answering (same screen)
- Score %
- Reference answer
- Sources: original problem link + pattern explainer link (DSA), source section link (other topics)
- Save for later / send to friend

### Feed mix
- ~50% weak areas
- ~30% review of missed cards
- ~20% new topics
- Topics can be added or muted in settings
- Full feed unlocks after today's missions; 10 cards before that

### Social
- See friend's answer on shared cards
- Challenge: send a card to friend
- Weekly feed accuracy score

## 3. Data

### Storage
- Raw downloads go in `.data/` (git-ignored).
- Every record keeps `source`, `source_url`, `ingested_at`.

### Sources
Download everything below in one run, including the multi-GB competitive sets. Only sources marked **cards** get cards generated in v1. The rest sit in the DB tagged with a low weight until we decide.

| Domain | Source | v1 |
|---|---|---|
| DSA | LeetCode-style dataset with tags + solutions (~2–3K) | cards |
| DSA | Company frequency lists (e.g. LeetMap-Pro) | importance only |
| DSA | NeetCode 150 / Blind 75 lists | importance only |
| DSA | PrimeIntellect, open-r1, livecodebench (competitive) | download only, tag `competitive` |
| System design | System Design Primer | cards |
| LLD / OOD | Grokking OOD repo | later |
| OS | OSTEP | cards |
| Concurrency | Little Book of Semaphores | later |
| CN, DB, AI, others | Source TBD | added once a real source is found |
| Behavioral | Hand-written list (~30) | mock interviewer only |

All sources must be verified (exists, fields, license) before writing ingestion code.

### DSA enrichment
- **Pattern:** Claude tags each problem from its solution code (not just topic tags). Hand-check ~50 before trusting.
- **Importance:** high if the problem is in NeetCode 150, Blind 75, or company frequency lists.
- **Pattern explainers:** one hand-picked link per pattern (~20 patterns).

### Card generation (offline)
Scrape → normalize → enrich → Claude generates cards in batches → second Claude pass checks each answer against the source → drop failures → store.

- Scrolling never waits on generation.
- Top up weekly.

### Links
- The AI never writes URLs. It writes a search query; the app resolves it via YouTube Data API or a trusted-site list.
- DSA and source-based cards link to the source directly.

## 4. Stack

- Next.js + Supabase (auth, Postgres, sync between two users)
- Claude API: Haiku for card generation and judging, a stronger model for the mock interviewer
- Python for the data pipeline
- Vercel for hosting

## 5. Out of scope for now

- In-app code editor (use LeetCode)
- Design canvas (use Excalidraw)
- XP/badges, native mobile app, browser extension
- Embeddings / vector search

## 6. Build order

1. Verify data sources, record exact fields
2. Shared DB schema (agree before splitting)
3. In parallel: data pipeline (friend) + core app (me)
4. AI mock interviewer
5. Feed: 3 domains (DSA patterns, CS core, system design), 3 formats (typed, flashcard, multiple choice)
6. Use for a week, then decide what to add

## Open questions

- Which LeetCode-style dataset has usable tags and solutions? (Step 1 answers this)
- Readiness formula weights per area
- Pattern list: final set of ~20
