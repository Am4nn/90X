# 90X Spec

> **Superseded for product, architecture and design by [`specs/2026-09-26-90x-mvp-design.md`](specs/2026-09-26-90x-mvp-design.md).** Sections 3 (Data sources) and 4 (Stack) here are still current; the rest is kept for history.

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
- Typed answers: exact/normalized match first (instant, free). If no match, the AI judges against the key points.
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
All 42 sources were verified on 2026-09-26 (they exist, fields checked, sizes known). The full list with roles lives in `pipeline/src/pipeline/sources.py`; run `uv run pipeline sources` to print it. Total is ~19 GB, most of it the three competitive sets. Those are big because they ship full hidden test suites (99% of their bytes), not because they have more problems.

Roles:
- **cards:** cards generated in v1
- **enrich:** adds importance, pattern, video or solutions to other sources
- **reference:** downloaded, no cards yet

Competitive programming is its own domain (`competitive`), separate from interview DSA: contest-style problems with stdin/stdout and huge test suites. Downloaded, low weight, no cards yet.

Key sources:

| Domain | Source | Role | Why |
|---|---|---|---|
| DSA | `newfacade/LeetCodeDataset` (HF) | cards | ~2.6K problems with tags, difficulty, solution, tests, explanation |
| DSA | `neetcode-gh/leetcode` → `.problemSiteData.json` | enrich | 450 problems: NeetCode pattern, NC150/Blind75 flags, YouTube video id |
| DSA | `kaysss/leetcode-problem-detailed` (HF) | enrich | Topic tags, acceptance rate, submission counts |
| DSA | `greengerong/leetcode` (HF) | enrich | Java/C++/Python/JS solutions |
| DSA | liquidslr, snehasishroy, LeetMap-Pro | enrich | Company-wise frequency |
| DSA | Chanda-Abdul coding patterns | enrich | Pattern explainers |
| Competitive | PrimeIntellect, open-r1, livecodebench | reference | ~18 GB, mostly hidden test cases |
| System design | System Design Primer, karanpratapsingh/system-design | cards | Structured guides + solved scenarios |
| System design | ByteByteGo 101, Grokking SD, awesome-scalability, others | reference | |
| LLD | Grokking OOD, awesome-low-level-design | reference | Case studies with code |
| OS | OSTEP (68 chapter PDFs) | cards | |
| CS | LastMinuteNotes, CS-Fundamentals-Interview, devops-exercises, Java/SQL Q&A repos, Little Book of Semaphores | reference | CN, DBMS, OOP, OS, Java, SQL |
| AI | AIMLInterviews, ml-interviews-book, LLM questions, data science Q&A | reference | |
| Behavioral | tech-interview-handbook, big-companies questions, others | reference | Behavioral questions for the mock interviewer |

### DSA enrichment
- **Pattern:** start from NeetCode's pattern label where the problem is in its 450. For the rest, the AI tags the pattern from the solution code. Hand-check ~50 before trusting.
- **Importance:** high if in NeetCode 150 / Blind 75, then company frequency, then acceptance/submission counts.
- **Videos:** NeetCode's YouTube id where available.
- **Pattern explainers:** one link per pattern (~20), starting from the coding-patterns repo.

### Card generation (offline)
Scrape → normalize → enrich → the AI generates cards in batches → a second AI pass checks each answer against the source → drop failures → store.

- Scrolling never waits on generation.
- Top up weekly.

### Links
- The AI never writes URLs. It writes a search query; the app resolves it via YouTube Data API or a trusted-site list.
- DSA and source-based cards link to the source directly.

## 4. Stack

| Layer | Choice |
|---|---|
| Web app | Next.js (App Router) + React 19 + TypeScript, React Compiler |
| UI | Tailwind CSS + shadcn/ui |
| Mobile | Installable PWA: `manifest.ts` + `public/sw.js`, web-push for nudges |
| Database | Supabase Postgres, Row Level Security on all user tables |
| Migrations | Supabase CLI SQL files in `supabase/migrations/` (source of truth, includes RLS) + `seed.sql` |
| DB access | Drizzle ORM for typed server-side queries (schema pulled with `drizzle-kit pull`); supabase-js for auth, realtime and client reads under RLS |
| Auth | Supabase Auth with Google login |
| Realtime | Supabase Realtime for the friend view and challenges |
| Client data | TanStack Query |
| Validation / dates | Zod, Luxon |
| AI in app | Vercel AI SDK (`ai`) in Next.js API routes, provider set in `web/src/lib/ai.ts` from env: DeepSeek, Anthropic or any OpenAI-compatible endpoint. `AI_MODEL_FAST` (deepseek-flash) for grading and quizzes, `AI_MODEL_SMART` (deepseek-v4-pro) for the mock interviewer |
| Data pipeline | Python in `pipeline/`: download, normalize, enrich, card generation. `openai` SDK against any OpenAI-compatible endpoint (DeepSeek by default), run off-peak for half price |
| Testing / lint | Vitest, Playwright, ESLint, knip |
| Package managers | Bun for the app (package manager + scripts; Next.js runs on Node), uv for Python |
| Env files | One environment. `web/.env.local` (Next.js loads it; same values go into Vercel) and `pipeline/.env`. Templates in each `.env.example` |
| Jobs, cache, search | Upstash: QStash (schedules, queue), Workflow (multi-step AI jobs), Redis (rate limits, cost meter, feed queue), Vector (coach search, built-in embeddings) |
| Monitoring | Sentry, Vercel Analytics, `ai_usage` table |
| Hosting | Vercel (app), Supabase cloud (DB), Upstash; pipeline runs locally |

Reference projects:
- `../Owe`: Supabase setup (CLI migrations, RLS, Google OAuth, TanStack Query)
- `../curfew`: Next.js app structure, PWA manifest + service worker, web-push

### Repo layout
```
90X/
├── .planning/     spec and research
├── .data/         raw downloads (git-ignored)
├── pipeline/      Python data pipeline (uv)
├── supabase/      migrations, seed.sql, config
└── web/           Next.js app (bun)
```

## 5. Out of scope for now

- In-app code editor (use LeetCode)
- Design canvas (use Excalidraw)
- XP/badges, native mobile app, browser extension
- Embeddings / vector search

## 6. Build order

1. Verify data sources, record exact fields
2. Shared DB schema (agree before splitting)
3. Data pipeline (Claude Code) + core app
4. AI mock interviewer
5. Feed: 3 domains (DSA patterns, CS core, system design), 3 formats (typed, flashcard, multiple choice)
6. Use for a week, then decide what to add

## Open questions

- Which LeetCode-style dataset has usable tags and solutions? (Step 1 answers this)
- Readiness formula weights per area
- Pattern list: final set of ~20
