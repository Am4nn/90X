# Next level — taking 90x past the tracker

A discussion round, written down. **Nothing here is built or approved for building.**
It is a review of the GPT-generated strategy in
`90x-next-level-product-strategy.md` (kept outside the repo, in Downloads) plus a
curated, prioritized list of what could actually be built next.

## Read in this order

1. **[REVIEW.md](REVIEW.md)** — my assessment of the strategy. What it gets right,
   what it gets wrong, and the one correction that changes the whole shape of the
   work. Start here.
2. **[IDEAS.md](IDEAS.md)** — the ideas that survived review, each written as a
   candidate implementation: what it is, what it builds on, what's net-new, how
   big it is, and when to do it.
3. **[RESEARCH.md](RESEARCH.md)** — research notes (learner-model techniques and
   the competitive landscape), so the recommendations here are grounded in more
   than opinion.
4. **[OPTIONS.md](OPTIONS.md)** — the flat inventory of every option, one line
   each, tagged ship / later / park / no.

## The short version

The GPT strategy's **diagnosis is right**: 90x already has the full closed loop
(content → practice → grading → FSRS → readiness → weak spots → plan), so the
next lever is *inference* — making the data we already capture intelligent — not
more surface features.

Its **near-term prescription is wrong for who 90x actually is**. The doc is
written as if 90x will soon have thousands of users ("2,431 attempts", item
discrimination, model calibration). It won't. 90x is invite-only — a handful of
people. A statistically-calibrated learner model (IRT / BKT / DKT) is the wrong
first move: there will never be enough data to calibrate it, and it would be
*less* trustworthy than the transparent rules we already ship.

The correction, in one line:

> **Build an interpretable learner model first — a rule-based layer that
> aggregates the evidence 90x already has and always explains itself — and only
> calibrate it statistically if 90x ever opens up.**

From that, the first four things worth building, in order:

1. **Explainable readiness** — "why is my number 74?" Extends `readiness.ts`
   with a derived `reasons` list. Cheap, high trust, extends a core brand promise
   ("checked, not claimed").
2. **Skill-level mastery state** — the missing layer the whole strategy hangs on:
   per-topic/per-pattern mastery + confidence (confidence = evidence count),
   aggregated from the evidence we already store. Deterministic, explainable.
3. **Failure fingerprint** — recurring *failure modes* (recognition vs approach vs
   edge cases vs complexity vs communication), not "practice more DSA". 90x's
   most differentiated idea, mapped onto signals we already capture.
4. **Adaptive planner v2** — reweight mission choice by expected value
   (weakness × importance × forgetting risk ÷ minutes), while keeping the reason
   one sentence a human can read.

Two ideas are right but **not now**: *target interview mode* (strong, but large,
and it needs the learner model first) and the *interview outcome loop* (the real
flywheel, but sparse data + privacy make it a later-phase design).

Two ideas are right-but-just-count for now: *content intelligence* (the
`observed_attempts` / `observed_correct` columns already exist — keep counting,
park the calibration) and *voice* (a layer over the learner model, not a moat on
its own).

## Status

- Branch: `next-level-strategy` (this worktree).
- Feeds a PR against `main` for review and discussion — nothing here changes
  shipped code.
