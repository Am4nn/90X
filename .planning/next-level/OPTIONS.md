# Options — the flat inventory

Every development option surfaced for 90x, from the GPT strategy, the review
(REVIEW.md), the research (RESEARCH.md), and the discussion. One line each,
grouped. This is the complete inventory; IDEAS.md is the *prioritized* subset.

Legend: **ship** = worth building near-term · **later** = right but sequenced ·
**park** = right idea, wrong cohort/time · **no** = deliberately not doing.

## Learner model & inference (ChatGPT's core)

- Personal mastery graph: per-topic/pattern mastery instead of one area score — **ship**
- Decompose each skill into sub-dimensions (recognize / choose invariant / implement / explain complexity) — **later**
- Per-skill state: mastery, confidence, evidence count, last-proved, forgetting risk, transfer strength, failure modes — **ship**
- Personalized cognitive map: render the Pattern Map with your mastery + evidence per node — **later**
- Interpretable skill-strength estimator aggregating existing evidence, confidence = evidence count — **ship**
- FSRS roll-up as a per-skill memory signal (difficulty, stability, lapse rate) — **ship**
- Empirical-Bayes shrinkage: pull thin-evidence scores toward a neutral/coach prior — **ship**
- Coach memory as a hand-authored prior on a skill — **ship**
- Mastery Grid visualization (open learner model: colored cells per topic) — **later**
- Bayesian Knowledge Tracing (needs many learners × attempts) — **park**
- Item Response Theory (needs ~500+ examinees to calibrate) — **park**
- Deep Knowledge Tracing (needs huge datasets, opaque) — **park**
- SPARFA sparse factor analysis (better, still overkill at this N) — **park**
- Elo rating as a light fallback for problem-difficulty ordering only — **park**

## Diagnosis & adaptive planning

- Failure fingerprint: infer *why* you fail (recognition / approach / edge cases / complexity / communication) — **ship**
- Map failure modes onto existing signals (points_hit, complexity delta, rubric criteria) — **ship**
- Replace "weakest area" with expected-gain-per-minute mission selection — **later**
- Adaptive planner reacting to behavior (completion rate, missed days, restart days) — **later**
- Add forgetting risk + transfer value to mission scoring, keep the one-line reason — **later**
- Transfer testing: known → related → altered → novel progression — **later**
- Thin transfer first: "same technique, different pattern" selector — **later**
- Better mission reasons: a real diagnosis sentence, not "weakest pattern" — **ship**

## Readiness & explainability

- Explainable readiness: "why is my number 74?" (reasons list under the dial) — **ship**
- Readiness confidence: show score + confidence-in-score separately — **ship**
- Target-specific readiness: different score per company/role — **later**
- Readiness change explanations: "+4 DSA (2 verified attempts, 1 transfer)" — **ship**

## Content intelligence

- Measure card performance (attempts, correct %, time, flag rate) — **later**
- Classify cards (too easy / ambiguous / poor discriminator / duplicate) and retire/repair/regenerate — **park**
- Content pipeline as part of the learner loop (behavior → correction → new version) — **park**
- Keep counting observed_attempts/correct (seeds already exist) — **ship** (calibration: **park**)

## Target & outcomes (interview)

- Target interview mode: company + role + date + JD + resume → target profile + plan — **later**
- Extend company_focus into a full target (role, JD, resume, competencies) — **later**
- Interview outcome capture: record round, result, questions, gaps — **later**
- Reality loop: reconcile 90x's readiness prediction with the real outcome, per person — **ship**
- Re-target the plan from real interview results for the next one — **ship**
- Spec the outcome-loop schema hook now, build the flywheel only if it opens up — **ship** (spec) / **park** (build)

## Coach

- Make the Coach read the learner model (diagnosis instead of "practice more") — **ship**
- Voice as a layer over personalization, not a generic mock — **park**
- More chat modes / features for their own sake — **no**

## New surfaces

- Timed live coding drill: solve a problem under the clock with review (reverses "no editor" scope) — **later**
- Interview-day simulation: a full multi-round dry run built from your weakest evidence — **later**
- Spoken retrieval practice for weak cards/lessons (short, daily, not a full mock) — **later**

## Deliberately not doing (a choice, not an omission)

- More card archetypes (feed-v2 already consolidated) — **no**
- Public signup / scale-dependent features — **no**
- XP, badges, streak inflation — anything that rewards activity over evidence — **no**
