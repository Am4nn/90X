# Ideas — what could actually be built next

The survivors of REVIEW.md, written as discrete candidate implementations. Each is
scored on: **what it is**, **what it builds on** (so effort is real, not a guess),
**what's net-new**, **size**, and **when**.

Ranking rule (from REVIEW.md §3): *interpretable first, statistical later*; and
anything that would need more evidence than an invite-only cohort will ever produce
is parked, not built.

## Principles that filter everything

1. **A number must explain itself.** Any score we add ships with its reasons.
2. **Confidence is evidence count.** "I think you're weak here" is only honest if
   it says *how much it's seen*.
3. **Deterministic where possible.** Answer-time AI is gone from the Feed; the
   learner model should cost nothing to compute. AI belongs in diagnosis text, not
   in the score.
4. **One sentence per mission reason.** The planner may optimize internally, but
   what it renders is the current style: *"Sliding Window is your weakest pattern
   (2 solved, 1 failed)."*
5. **Respect the cohort.** Never build a feature whose value needs thousands of
   users.

---

## Ship first (small, high-trust, extends shipped code)

### 1. Explainable readiness — "why is my number 74?"

**What.** `readiness.ts` already computes `coverage × accuracy × 100` per area and a
weighted overall. Add a parallel `reasons` list derived from the *same inputs*:
which areas drag the number down, which improved over 14 days, which have no data
("SQL: no practice yet"). Render it under the dial on Me and in the Coach's
`get_progress` read.

**Builds on.** `web/src/lib/tracker/readiness.ts` (all inputs already in scope:
`important`, `attempts`, `cardAttempts`), `lib/tracker/me.ts`, `lib/coach/tools-data.ts`.

**Net-new.** A pure function `readinessReasons(...)` + a small Me section + coach
prompt wiring. No schema, no model.

**Size.** Small. A day of work plus tests.

**When.** Now. It is the cheapest thing that makes the existing number *trustworthy*
— and it directly extends "checked, not claimed".

**Why first.** Every later idea (mastery, fingerprint, planner) inherits the
"explain yourself" contract. Building it first sets the pattern.

### 2. Skill-level mastery state — the missing layer

**What.** A per-`(user, topic_or_pattern)` mastery read, aggregated from evidence we
already store, with **confidence = evidence count** and **empirical-Bayes shrinkage**
(when evidence is thin, the score pulls toward a neutral/coach prior rather than
pretending precision). It is a transparent, multi-signal estimator — each signal
kept *decomposable* so "why" is just the list of contributing signals:

1. **FSRS roll-up (memory)** — mean card Difficulty, Stability, lapse rate per skill,
   from `card_state`. *(FSRS is 90x's strongest raw asset; the research confirms D/S/R
   roll up cleanly — see RESEARCH.md §2.)*
2. **Check-ins (application)** — weighted accuracy that penalizes hints and failures,
   not just solved rate.
3. **Solution reviews (understanding)** — complexity-comparison delta (yours vs best).
4. **Mock rubric (anchor)** — the 1–5 per-criterion scores, high-signal, low-frequency.
5. **Coach memory (prior)** — a `strength`/`habit` note acts as a hand-authored prior.

Each returns `mastery` (bounded, rule-based), `confidence` (count + recency),
`lastProved`, and a plain-language `state` (mastered / started / weak / untouched —
the four states `planner.ts` already reasons in). Render it like a **Mastery Grid**
(colored cells per topic) with a Khan-style threshold and a per-signal "why". It is a
*view* first, not a new black-box; if we add a table it is a denormalized cache of the
view, never a second source of truth.

**Builds on.** `lib/tracker/planner.ts` (`WEAKNESS` states), `lib/tracker/readiness.ts`,
`lib/feed/weakness.ts`, `lib/feed/srs.ts` (FSRS stability/difficulty/lapses),
`lib/library/queries.ts` (`patternMap` already computes per-pattern solved/failed),
`lib/coach/tools-data.ts` (`weakSpotsData`), `lib/coach/memory.ts` (coach prior).

**Net-new.** One aggregation module + tests. Optionally a `skill_state` table as a
cache. The hard part is *not* the math — it is the rule for blending heterogeneous
signals into one `mastery` without pretending more precision than exists (the
empirical-Bayes part).

**Size.** Medium.

**When.** Immediately after (1). This is the foundation every other idea stands on.

**Why now.** It is the strategy's single biggest idea (§4), and it is buildable
deterministically *today*. Without it, "failure fingerprint" and "adaptive planner"
have nothing to attach to.

### 3. Failure fingerprint v1 — *why* you fail, not just where

**What.** A small, fixed failure-mode taxonomy, inferred per pattern/topic from
existing signals, not a model call:

| Mode | Signal we already store |
|---|---|
| Recognition (wrong problem family) | repeated `wrong` on the same pattern across *different* problems |
| Approach / invariant selection | `solution_reviews.review` line notes + `complexity` mismatch when `correct=false` |
| Edge-case completeness | `card_reviews.points_hit` misses on the "edge case" key points |
| Complexity analysis | `solution_reviews.complexity` (yours vs best) consistently off |
| Communication / explanation | mock rubric `communication` / behavioral criteria low |

**Builds on.** `card_reviews.points_hit`, `solution_reviews` (`correct`,
`complexity`, `review.lineNotes`), `mock_details.rubricScores`, `checkins.result`.
All already captured.

**Net-new.** (a) A fixed taxonomy (this is the *real* work — see REVIEW.md §2.3);
(b) an inference module that maps evidence → mode with a confidence that is,
again, evidence count; (c) surfacing it: on the Pattern Map node, in the Coach's
`get_weak_spots`, and as a mission reason.

**Size.** Medium. The taxonomy definition is the long pole; the inference is modest.

**When.** After (2). It is 90x's most differentiated idea and the thing a generic
"AI mock" can't fake — but it reads *from* mastery, so it waits for (2).

**Why it's the moat.** The landscape research is unambiguous: "AI mock interview"
is fully commoditized, and no product fuses learner-model + failure-fingerprint +
adaptive-planner. This is the fusion.

---

## Ship later (build on the above)

### 4. Adaptive planner v2 — expected value, rendered in one sentence

**What.** Extend `planner.ts`'s selection from
`weakest-pattern → most-important-problem` to a score that adds **forgetting risk**
(from FSRS `stability`/`dueAt` — already in `card_state`) and **expected gain**
(weakness × importance × a transfer/novelty factor). Internally it is a weighted
sort; externally the reason stays one line.

**Builds on.** `lib/tracker/planner.ts` (the `score` fn already does
`importance + company + difficulty`), `lib/feed/srs.ts` for decay, (2) for weakness.

**Net-new.** A scoring function + tests + richer reasons. No new model.

**Size.** Medium.

**When.** After (2) and (3). Do not do this before the fingerprint exists — the
planner's "gain" is meaningless without knowing *what kind* of weakness it is
closing.

### 5. Transfer testing — "do you know it, or just this problem?"

**What.** The progression the strategy §9–10 wants — known → related → altered →
novel — but built thin first. `problems.techniques` already tags each problem with
1–4 techniques (hash-map, prefix-sum, monotonic-stack, …). A "transfer" problem is
one that shares a technique but not the primary pattern, or the same pattern under
a changed constraint (premium, company, or a missing `why_step` explanation).

**Builds on.** `problems.techniques` (already indexed), `problems.pattern_slug`,
`lib/library/checkin.ts` (next-problem selection), `lib/coach/solution-review.ts`
(`pickNextProblem` already picks a *same-pattern* next problem).

**Net-new.** A "transfer" candidate selector (share technique ≠ pattern) + the
ability to render "explain why this works" (the `why_step` is already a card
primitive). This is partly a *content* feature (need a small "transfer" tag), so it
couples with the pipeline.

**Size.** Medium–large (touches content + app).

**When.** After (2), parallel with (4). Lower urgency than the planner; higher cost
because it crosses the content/app boundary.

### 6. Target interview mode — "how ready am I for *this*?"

**What.** Extend the existing `campaigns.company_focus` (company + date range) into a
full target: company, role, date, job description, resume, and a **target profile**
(mapped from company frequency + role expectations). Then a *target-specific*
readiness: the same learner model re-weighted toward what that company/role
actually probes, rendered as "Google SWE II: 68" beside the general 74.

**Builds on.** `campaigns.company_focus` (schema exists), `problems.companies`
(company-frequency jsonb exists), the learner model (2), the fingerprint (3).

**Net-new.** Target table (or jsonb on campaign), JD/resume ingestion, target
weighting, a target profile UI. Large.

**Size.** Large.

**When.** Later. It is the strategy's best *product* idea, but it is a full feature
that pays off only once the learner model it re-weights is real.

### 7. Make the Coach read the learner model

**What.** The strategy's §23 in one move: the Coach's read tools already return
weakness and activity; wire in (2) and (3) so the coach can say *"your
implementation is fine; the recurring problem is choosing the invariant"* instead
of *"practice more DSA"*.

**Builds on.** `lib/coach/tools-data.ts` (`weakSpotsData`, `progressData`),
`lib/coach/tools.ts`.

**Net-new.** Prompt/tool wiring only, once (2)/(3) exist. No new surface.

**Size.** Small (given 2 and 3).

**When.** Immediately after (2)/(3). It is how the learner model becomes visible
without building a new screen.

---

## Park (right idea, wrong cohort or wrong time)

### 8. Interview outcome loop — spec the hook, don't build

**What.** `target_interviews` + `interview_outcomes` tables and a "how did it go?"
capture after a real interview, so 90x can later compare predicted vs actual
readiness.

**Why park.** The flywheel needs real outcomes, which an invite-only cohort produces
a few times a year. The *schema hook* is cheap and worth spec'ing now so we don't
regret the shape later; the *product* is fantasy at this scale. The landscape
research confirms this is genuinely open space — and the hardest part (real-outcome
data) is exactly what a private cohort doesn't have.

**When.** Spec the tables now; build when there's a reason.

### 9. Content intelligence — keep counting, park the calibration

**What.** §18–21: calibrate difficulty, retire ambiguous cards, generate variants
from aggregate behavior.

**Why park.** `cards.observed_attempts` / `observed_correct` already exist and should
keep counting. But decisions like "probably ambiguous / poor discriminator" need
per-card N in the hundreds; 90x has single-digit users. Counting is free and right;
calibrating is noise.

**When.** Revisit if/when 90x opens up.

### 10. Adaptive testing / IRT / BKT / DKT — the statistical layer

**What.** §13: formal item calibration and latent-ability estimation once data
accumulates.

**Why park.** Each needs many responses per item × many learners. Wrong N today.
This is the *last* layer, not the first — and only if 90x ever becomes public.

### 11. Voice mocks — a layer, not a moat

**What.** §24: voice mock interviews.

**Why park.** The research is unambiguous: "AI mock" (voice or text) is now a
commodity every incumbent ships. The differentiator is the *personalization behind*
the mock (targeting the three least-proven capabilities), which is (2)+(3)+(7), not
the voice layer itself. Add voice only after the personalization exists, and even
then it's a feature, not the strategy.

---

## The one-line roadmap

```
(1) explainable readiness
      → (2) skill mastery state ──→ (3) failure fingerprint ──→ (4) adaptive planner v2
                                            └───────────────→ (7) coach reads the model
                                                               (5) transfer testing (parallel)
                                                               (6) target interview mode (later)
      (8)(9)(10)(11) parked — spec hooks, keep counting, wait for the cohort to matter
```
