# Part E — generation (pipeline)

**Branch** `feed-v2-generation` · **Worktree** `../90X-wt-fv2/e` · **No Playwright spec** — this
is the Python pipeline. Depends on **A** (the registry; the pipeline reads `archetypes.json`
directly). Can run alongside F once A is in.

E changes how cards are written. Today the writer chooses the format and writes a mixed
`CardSet`. From now on the writer **never chooses**: it is asked for one named archetype and
writes exactly that one thing. A writer may **refuse** (no natural sequence for this topic), and
the budget refills with another archetype.

## Scope

- Load the registry into the pipeline (`archetypes.json`).
- A per-topic budget: count ∝ `topics.importance`, spread **equally across the archetypes
  eligible for that area**, with a difficulty target per card.
- One writer call per archetype; the archetype carries its primitive and answer shape.
- Hard cards may draw on `problems.statement_md` and `pattern_tricks`, not only the lesson.
- **Gate 1 lives here**: generate one topic, measure the cost per card, stop, report.

## Files

**Create**
- `pipeline/src/pipeline/cards/archetypes.py` — parse `archetypes.json`; `eligible(area)`,
  `budget(topic)` → `list[(archetype_id, difficulty)]`.
- `pipeline/src/pipeline/cards/write.py` — write one card for one archetype, or refuse.
- `pipeline/src/pipeline/cards/trial.py` — generate **one** topic and print measured cost per
  card (Gate 1). Extend or replace the existing `cards/trial.py`.

**Modify**
- `pipeline/src/pipeline/cards/from_lessons.py` — keep `rewrite`; the generation entry point
  becomes per-archetype, not a mixed `CardSet`.
- `pipeline/src/pipeline/cards/run_lessons.py` — drive `budget` → per-archetype writes → save.
- `pipeline/src/pipeline/staging.py` — the `cards` table already has the columns (Part A added
  them to Supabase; add the matching `archetype`/answer columns to the staging DDL if absent).
- `pipeline/src/pipeline/commands.py` — `lesson-cards`/`cards` write the new columns.

## Reuse, do not rewrite

```
# llm.py
class LLM: complete_json(system, user, schema, tier, purpose) -> T;  # logs cost, enforces cap
spend_usd(con) -> float                                             # total $ in staging
BudgetExceeded, LLMError
# config.py
REPO_DIR, DATA_DIR
# staging.py
connect(path=DB_PATH) -> con;  # cards table: id, topic_slug, format, difficulty, prompt_md,
                               # options, answer_md, key_points, source_refs, quality, status, kept
# from_lessons.py (today)
def card_budget(importance: float) -> int;   # replace with per-archetype spread
def for_lesson(llm, topic, lesson_md, tier) -> list[Card];  # split into one-archetype writer
# run_lessons.py (today)
def card_id(topic_slug, prompt, kind="") -> str;
def topics_with_lessons(con, only, limit, redo) -> list[dict];
def save(con, topic, kept, rejected, confidence, sent_back=None);
# generate.py — Card pydantic model (extend with archetype + per-shape answer fields)
```

The registry is read **directly from `archetypes.json` at the repo root** — do not copy it into
Python. `shapeOf`-equivalent logic lives in `archetypes.py`.

## The budget and the writer

- `budget(topic)` returns a list of `(archetype_id, difficulty)` whose length is
  `count ∝ importance`, spread equally across the archetypes eligible for the topic's `domain`,
  and whose difficulties follow the per-topic target (Easy/Medium/Hard). `topics.importance` and
  `topics.domain` come from staging.
- The writer gets one `(archetype_id, difficulty)` and returns one card, or a refusal. A refusal
  is not an error: the budget refills with the next eligible archetype, and a later card in the
  same topic may come back around.
- The card's `format` = the primitive id, `archetype` = the archetype id, and the per-shape
  answer columns (`picked` / `constraints` / `pairs` / `value`+`tolerance`) are populated from the
  writer's answer. The `key_points` stay (the result screen uses them).
- Hard cards may read `problems.statement_md` (join `problems` on the topic's pattern) and
  `pattern_tricks`; credit them in `source_refs` as they already are credited.

## Gate 1 — measure before you spend

The original pass averaged ~$0.0017/card; structured cards carry more fields. **Do not run 274
topics on an estimate.**

- Pick the highest-`importance` topic with an `ok` lesson.
- `uv run pipeline trial` (or your `trial.py`) generates that one topic's full budget.
- Report: cards written, tokens in/out, `spend_usd`, and **measured cost per card**.
- **Stop.** No further generation until the orchestrator reports the number and a human gives
  the go-ahead.
- Every pipeline invocation sets `PIPELINE_MAX_USD` (the env var `LLM.__init__` already reads).
  Do not rely on the default.

## Tests (pytest)

- `archetypes.py` — 47 archetypes parse; `eligible(area)` returns the documented sets; `budget`
  length tracks importance and never names an ineligible archetype for the area; the four
  dual-primitive archetypes offer both `pick_one` and `numeric`.
- `write.py` — a refusal is a valid return, not an exception; a produced card's `format` is a
  known primitive and its answer columns match its shape.

## Traps

- **Never run against production.** `publish` reads `DATABASE_URL`; you are not publishing, only
  writing staging (`.data/staging.duckdb`). Do not run `pipeline publish` at all.
- **The writer must never choose the format.** If the prompt lets the model pick, it returns
  multiple choice every time (DECISIONS round 2) and the corpus becomes 85% MCQ.
- **A refusal refills, it does not abort.** A strained ordering card is worse than an absent one.
- **`PIPELINE_MAX_USD` on every invocation**, and report cumulative spend from `spend_usd(con)`.

## Verification

`uv run pytest` in `pipeline/`. Then run the Gate 1 trial and report the measured cost per card
and the cumulative `spend_usd`. No web checks apply.

## Decisions (with cost if wrong)

- **Budget difficulty target follows the DECISIONS round-3 rubric applied by the pipeline, not a
  flat Easy/Medium/Hard third.** Cost if wrong: the corpus reproduces whatever is easiest to
  write (Easy), the exact failure the plan names.
- **The writer is one-card-one-archetype, not a batch.** Cost if wrong: a batch call lets the
  model drift back to mixing formats and hides the per-archetype budget.
