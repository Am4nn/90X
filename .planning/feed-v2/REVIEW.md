# Feed v2 — owner's review of the full run

Reviewed 2026-10-02 against `.data/staging.duckdb`, `archetypes.json`,
`web/src/lib/feed/grade.ts` and the primitive components — not against the run
report. Every number below was measured, and where it disagrees with the
orchestrator's summary the measurement is cited.

**Verdict: the corpus is good and the difficulty problem is genuinely fixed.
Do not run the four production steps yet.** Step 3 cannot succeed as written,
step 4 retires content a decision said to keep, and 112 cards cannot be
answered correctly by any reader.

---

## What is right

| | old | new |
|---|---|---|
| Hard cards | 26 of 2,808 (**0.9%**) | 448 of 2,401 (**18.7%**) |
| difficulty mix | Easy-dominated | 27.7 Easy · 53.6 Medium · 18.7 Hard |
| model at answer time | typed cards graded by a model | none |

The mix holds across all five domains (15–20% Hard everywhere), so the
reviewer's "too easy" complaint is addressed structurally rather than by
relabelling. Spend was $17.19 against a $25 cap, every call off-peak,
`tokens_reasoning = 0` throughout. Cards per topic 6–19, median 14.

---

## Blocking — fix before publishing

### 1. `pipeline publish` (step 3) will abort and publish nothing

`run_lessons.py:158` deletes a topic's lesson cards before rewriting them, so
the old corpus is **gone from staging** for all 177 regenerated topics.
`publish.py:177` then calls `_retire_superseded_cards`, which **deletes**
production cards staging no longer has — and raises `StudyHistoryAtRisk` if any
of them carry `card_reviews` or `card_state` rows. Production has both.

The raise happens inside the `with pg.transaction()` block, so the whole
publish rolls back. The runbook describes this as a warning to "stop and
reconcile"; measured, it is a step that cannot complete. Resolve it before
production, not during.

### 2. The swap retires `behavioral`, against the Round 2 decision

`swap.py` runs `update cards set status='retired' where status='live'` — every
live card. Round 2 settled "behavioural: none retired". The flip must exempt
the areas that were never regenerated, or the decision has to be reopened
explicitly.

### 3. 112 cards (4.7%) cannot be answered correctly

| n | defect | why it is fatal |
|---|---|---|
| 54 | `grid_toggle` exceeds the 3×3 cap (up to **5×7 = 35 cells**) | `grid-toggle.tsx:8` says "capped at 3×3 by the pipeline" and has no guard — it renders whatever it is given, at 390px |
| 18 | `grid_toggle` with **1 column** | not a grid; it is `all-that-apply` wearing the wrong screen |
| 22 | `tap_in_place` with two **identical lines** | only one index is `picked`; a reader who taps the other identical line is marked wrong |
| 13 | `assemble` with **duplicate tokens** | the same token at two indices makes the constraint set ambiguous |
| 5 | `match` whose `pairs` reuse a right-hand item | `match.tsx:32` enforces a bijection, so **no answer the UI can produce is correct** |
| 5 | `tap_in_place` with an empty/non-string option | |
| 4 | Hard card with no why-step where the archetype allows one | loses the 25%→6% guess floor |
| 3 | `claim_grid` with 5 rows (cap is 4) | |
| 1 | `assemble` with **cyclic** constraints | `7→2→8→9→10→11→7`: no permutation satisfies them, the card is always wrong |

All of these are checkable in code for free. None needs a model.

### 4. The structural gate covers 23% of the corpus

`structure.py:76` returns early unless `format in ("pick_one", "mcq")`. The
docstring argues the *elimination-by-shape* rules don't apply elsewhere, which
is true — but it means that for nine of the ten primitives **nothing checks
shape at all**: no item caps, no duplicate detection, no bijection check, no
cycle check, no tolerance sanity. That is why the table above exists. The fix
is a well-formedness pass for every primitive, separate from the guessability
rules, run as code before any model call.

---

## Decisions you owe (and what the data says)

### A. The 96 skipped topics — the shortfall is not what the report says

The report attributes 2,401-vs-2,500 to the writer under-producing. Measured,
the cause is that **96 topics received zero cards**:

| domain | topics skipped | cards left in old format | avg `importance` |
|---|---|---|---|
| `ai` | 40 | 416 | 0.81 |
| `lld` | 34 | 342 | 0.77 |
| `behavioral` | 22 | 222 | 0.80 |

177 topics got new cards; 273 have cards. These are **high-importance** topics
(0.77–0.81), not the long tail. At the measured 13.6 cards/topic they would
have added ~1,300 cards and landed the corpus near 3,700.

The real cause is `archetypes.json`: all 47 archetypes list `areas` of
`dsa · system_design · cs · java · sql` only. Nothing could have generated
them. This is a catalogue gap, not a generation failure.

**Recommended: keep them, exempt them from the flip, and add archetypes for
`ai`/`lld`/`behavioral` as a follow-up run.** Retiring them removes a third of
the topic catalogue from the Feed to fix a format problem, and `behavioral` was
already decided as never-retired.

### B. Six archetypes produced nothing, and the distribution is not equal

41 of 47 archetypes are represented. Missing entirely: `estimate`,
`which-test-catches`, `read-query-plan`, `error-cause-pick`, `impossible-bound`,
`odd-one-out`.

Round 4 settled "equal within each area's eligible archetypes". Measured spread
is **1 to 173** (median 48):

- top: `flash` 173 · `concept` 169 · `all-that-apply` 168
- bottom: `pattern-signal` 1 · `which-invariant` 2 · `fill-clause` 5

The three largest archetypes are the three closest to the old easy formats
(`flash` is self-rate — no grading at all, 173 cards), and the long tail is
starved. Worth a rebalance before the flip, or an explicit decision to accept
an unequal distribution.

### C. 104 of 107 numeric cards have `tolerance = 0.0`

Exact float match. For "how many comparisons" that is correct, and the sampled
prompts are mostly exact-answer questions, so this is probably fine — but the
`estimate` archetype produced **zero** cards, which is the one that needed a
real tolerance. Confirm that nothing asking for an approximation is being
graded exactly.

### D. The review pack is 81 cards, not 94

The pack states this itself ("Below: 81 cards, two per archetype"). 41
archetypes × 2, minus the one with a single card. The six empty archetypes
cannot be reviewed because nothing exists to review — so the Gate 3 question
"does this archetype earn a place" is unanswerable for all six.

---

## Soft findings

- **21 bucket cards place >8 items** all-or-nothing, up to 14. `OPEN-QUESTIONS.md`
  item 4 flagged exactly this ("eight pairs marked all-or-nothing is
  punishing") and left it to be decided from the mocks. It was never decided;
  the writer chose.
- **9 `grid_toggle` cards have every cell true**, **8 `claim_grid` cards give
  every claim the same verdict** — gradeable, but a reader who toggles
  everything scores 1.
- **25 cards share the prompt "Mark each statement as true or false."** across 25
  topics (and 6 share "Which line contains the bug?"). Not a dedupe failure —
  the content is in `options` — but the Feed will show an identical header on
  25 cards with no topic context in the stem.
- **The blind gate ran on `smart`, not `fast`.** The orchestrator disclosed
  this. Cost: $4.92 of the $17.19 across 9,949 calls, ~29% of the run, at the
  expensive tier. The ~9% refined rejection rate was measured on `smart`, so it
  does not transfer to `fast` — if the gate is moved, re-measure it.

---

## Suggested order

1. Add the well-formedness pass for all ten primitives (free, no model).
2. Re-run it over the corpus; repair or drop the 112.
3. Decide A (keep/retire the 980 legacy cards) and amend `swap.py` accordingly.
4. Decide B (rebalance archetypes, or accept 41 of 47 and the 1–173 spread).
5. Resolve the `publish` / `_retire_superseded_cards` collision.
6. Then the four production steps.
