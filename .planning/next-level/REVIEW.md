# Review — the GPT "Next-Level Product Strategy"

My assessment of `90x-next-level-product-strategy.md` (the GPT-researched strategy
attached in Downloads). I read it against the actual repo at HEAD
(`main` = `bdfab38`), not against the repo as the doc claims to have reviewed.
That matters: the doc is already stale on the one point it spends the most words on.

## 0. TL;DR

- **Diagnosis: correct.** 90x is past the "MVP feature" problem; the next lever is
  *inference* over data we already capture, not more surface.
- **Direction: correct.** The learner-model → failure-fingerprint → adaptive-planner
  → transfer → target-interview → outcome-loop chain is the right shape and the
  right dependency order.
- **Near-term prescription: wrong for who 90x is.** It assumes the cohort will
  scale, so it reaches for statistical calibration (IRT / BKT / DKT, item
  discrimination) too early. 90x is invite-only with a handful of users. The first
  learner model must be **interpretable and rule-based**, and its confidence must
  come from *evidence count*, not from a calibrated latent-trait estimate.
- **It is stale on feed-v2.** The doc treats typed-answer grading as the core cost
  centre ("1,383 typed cards… cost money"). That work already shipped: the Feed is
  now deterministic tap-answer formats, and grading at answer time costs nothing.

## 1. What it gets right

**The closed loop is real.** The doc's inventory (content → practice → grading →
FSRS → readiness → weak spots → plan) matches the code. 90x genuinely already has
the adaptive-learning loop most "adaptive" products only claim to have. That is a
strong and correct foundation for the whole strategy.

**"Make the existing data intelligent" is the right move.** The best ROI in 90x is
not a new feature; it's connecting the evidence that already exists. We already
store: per-card FSRS state (`card_state`), per-answer outcomes and `points_hit`
(`card_reviews`), per-problem check-ins (`checkins`), solution reviews with
complexity comparison (`solution_reviews`), per-criterion mock rubrics
(`mock_details.rubricScores`), and coach memory with evidence links
(`coach_memory`). None of it is aggregated into a *per-skill* statement yet. That
is the gap, and the doc identifies it exactly.

**Explainability is the right value, not precision.** §38 ("Why did my readiness
change?") is the single most on-brand idea in the doc. It extends the existing
principles "readiness is earned" and "checked, not claimed". A number that explains
itself is *more* valuable to a small cohort than a more accurate number that
doesn't.

**The discipline is right.** §22–24 ("don't add more card types", "don't keep
expanding the coach", "voice is a layer") is exactly the restraint 90x needs. The
natural instinct after an MVP is to add; the right instinct is to make what exists
smarter.

**The dependency order is right.** Learner model before failure fingerprint before
adaptive planner before target mode. You cannot diagnose *why* you fail without a
model of what you know; you cannot plan by expected gain without a diagnosis.

## 2. Where it is stale or wrong

### 2.1 It reviewed a repo that no longer exists on this one point

The doc leans on feed-v2 as *in planning* (§18, §22 cite `feed-v2/PLAN.md` and
`CATALOGUE.md` as future). At HEAD, feed-v2 is **shipped and merged**:

- `web/src/lib/feed/grade.ts` is explicit: *"Typed answers left the Feed, so there
  is no model call at answer time and the same answer always gets the same mark."*
- `cards` now carries the deterministic answer columns (`picked`, `constraints`,
  `pairs`, `value`, `tolerance`, `why_step`) and the content-intelligence seeds
  (`observed_attempts`, `observed_correct`).

Consequences for the strategy:

- The "Feed's running cost goes to zero" win it anticipates has **already happened**.
  Any cost-driven argument for changing the Feed is done.
- The "47 archetypes + learner model > 60 archetypes" argument (§22) is slightly
  off-target: the archetype work is already a *consolidation*, not an expansion, and
  it's the *content* side. The learner model is the *user* side. They're different
  axes and can proceed independently.

This is not a fatal flaw, but it is the exact "verify against the code before
acting" failure the `HANDOFF.md` warns about, and I want it on the record.

### 2.2 The cohort-size assumption is the real error

The strategy is written for a product that is about to have thousands of users. It
talks about "2,431 attempts", "item discrimination", "calibration as data
accumulates". 90x is invite-only — Aman plus a few friends. Concrete consequences:

- **Per-skill evidence will be near-zero for months.** The proposed
  `learner_skill_state` (mastery, confidence, forgetting_risk, transfer_strength,
  failure_modes) with 5 skills × ~200 patterns/topics × a handful of users means
  most rows have 0–2 observations. A model that needs `evidence_count` to *do*
  anything will be empty.
- **IRT / BKT / DKT are non-starters right now.** They each need many responses per
  item and many items per learner to estimate parameters. They are the right tools
  for a *public* product, not for a private cohort. (RESEARCH.md has the detail.)
- **"Content intelligence" is meaningless at this N.** "2,431 attempts, 68% correct,
  12% flagged" will never happen. The *columns* exist and should keep counting, but
  any decision (retire / repair / generate variant) made on aggregate signal will be
  noise for a long time.

This is the one correction that reshapes the plan: **the learner model must be
interpretable and evidence-count-driven first, and statistical second (or never).**

### 2.3 The skill decomposition is asserted, not built

§4–5's example — `recognize pattern / choose invariant / derive window state /
implementation / explain complexity` — is the most interesting idea in the doc and
the least specified. That decomposition has to come from *somewhere*:

- It is not in the schema today. The closest existing signals are `points_hit`
  (per-card key points), `solution_reviews.complexity` (yours vs best), mock rubric
  criteria, and `problems.techniques` (a technique tag, not a skill dimension).
- Mapping heterogeneous evidence onto a clean set of failure/skill dimensions is
  real work and the doc hand-waves it.

I don't think that's a reason to drop the idea — I think it's the *hard part* and
it should be planned honestly. (See IDEAS.md §3.)

### 2.4 The planner idea risks losing explainability

§7's "expected gain / minute" is directionally right, but today's planner is
transparent: *"Sliding Window is your weakest pattern (2 solved, 1 failed)"*. A
planner that multiplies four latent scores and divides by minutes will produce a
number nobody can read, which fights "checked, not claimed". The fix is to keep the
optimization internal and **render the decision as a one-line reason**, exactly as
`planner.ts` already does today. (IDEAS.md §4.)

### 2.5 The outcome loop is real but not near-term

§16–17 (interview outcomes feeding back into the model) is the genuine flywheel and
the strongest *long-term* moat claim in the doc. But for an invite-only cohort:

- Interview outcomes are extraordinarily sparse — a person has a few interview
  loops a year.
- Recording "the questions they asked me, round by round" is a privacy and
  self-report-reliability problem, and it sits awkwardly next to "private by
  default".

Right call: **design the schema hook now, build nothing.** A `target_interviews` /
`interview_outcomes` table is cheap to spec and expensive to regret not having. But
treating it as a Phase 6 deliverable is fantasy with this cohort.

## 3. The correction, stated once

> **Start with an interpretable, rule-based learner model whose confidence is
> literally the count of evidence behind it. Calibrate it statistically only if the
> product ever opens beyond the invite circle.**

This is the difference between "a number that says what it knows and what it
doesn't" and "a black box nobody trusts". The former is on-brand and buildable now.
The latter is neither.

## 4. Idea-by-idea verdicts

| Idea (doc section) | Verdict | Why |
|---|---|---|
| Personal mastery graph (§4–5) | **Build, interpretable** | The missing layer. Rule-based mastery + confidence = evidence count. |
| Failure fingerprint (§6) | **Build, after mastery** | Most differentiated. Hard part is the failure-mode taxonomy. |
| Expected-gain planner (§7–8) | **Build, after fingerprint** | Keep the reason one sentence. Preserve explainability. |
| Transfer testing (§9–10) | **Build, thin first** | Depends on `problems.techniques` (already present). Start with "same technique, altered constraint". |
| Evidence-based readiness (§11–12) | **Build first** | Cheapest, highest trust, extends `readiness.ts`. |
| Adaptive testing / IRT / BKT (§13) | **Park** | Wrong N. Revisit only if public. |
| Target interview mode (§14–15, 28–29) | **Build, later** | Strong, but large and needs the learner model. Extends `campaigns.company_focus`. |
| Interview outcome loop (§16–17) | **Spec now, build later** | The flywheel, but sparse + private. Schema hook only. |
| Content intelligence (§18–21) | **Count now, calibrate later** | Seeds already exist (`observed_*`). Aggregate decisions are noise at this N. |
| More card types (§22) | **Correctly skip** | Already consolidated by feed-v2. |
| More coach features (§23) | **Correctly skip** | Instead: make the coach *read* the learner model. |
| Voice (§24) | **Correctly defer** | A layer over personalization, not a moat. |

## 5. What I would actually do first

1. **Explainable readiness** (extend `readiness.ts` to emit reasons). ~small.
2. **Skill mastery state** (new `topic`/`pattern` mastery view over existing rows).
   ~medium. This is the foundation.
3. **Failure fingerprint v1** (a small, fixed failure-mode taxonomy over
   `points_hit`, `complexity`, rubric criteria, check-in results). ~medium.
4. **Adaptive planner v2** (reweight + one-line reasons). ~medium, after 2–3.

Everything else in IDEAS.md is ranked "later" or "parked" with the reasoning.
