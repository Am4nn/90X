# Research notes

Supporting evidence for REVIEW.md and IDEAS.md. Two tracks: the competitive
landscape (what the rest of the market actually ships) and learner-model
techniques (what "build a learner model" concretely means). The landscape track
informs *what to build*; the technique track informs *how, given 90x's cohort*.

---

## 1. Competitive landscape — is adaptive readiness still a differentiator?

Collected 2026. Sources are product sites, Wikipedia, and primary blog/help pages
(URLs inline). Web search returned nothing this session, so this is direct-fetch.

### Per product

| Product | Readiness / personalization | Outcome loop |
|---|---|---|
| **LeetCode** (leetcode.com) | Difficulty tiers, company tags (premium), an Elo-like **contest rating**; Study Plan; a separate "LeetCode Interview" AI mock (leetcode.com/interview) | None — contest rating is a rank, not "ready for *your* target" |
| **NeetCode** (neetcode.io/roadmap) | NeetCode 150 roadmap; AI assessments, Versus mode; static lists | None |
| **AlgoExpert** (algoexpert.io) | ~165 hand-picked questions, 4 timed assessments, certificate | None |
| **HelloInterview** (hellointerview.com) | Company/role-specific "what to expect" guides, tracks, AI tutor; readiness is self-assessed | None |
| **Interviewing.io** (interviewing.io) | Real anonymous mocks + expert post-interview feedback; a mock→real-interview→offer funnel via a jobs portal; publishes outcome data-science | **Closest thing to a loop**, but outcomes are not fed back to a personalized model |
| **Pramp / Aced** (pramp.com) | Peer mocks; acquired by Exponent (2024), effectively sunset | None |
| **CodeSignal** (codesignal.com) | "Certified Coding Score"; 2025–26 pivot to "agentic skills intelligence" with role-benchmarked gap analysis | Employer-side; no learner loop |
| **Duolingo** (blog.duolingo.com/how-we-learn-how-you-learn) | Per-word **student model + half-life regression (HLR)** for spaced repetition (Settles & Meeder 2016, ACL) | Technique reference — language, not interviews |
| **Khan Academy** (support.khanacademy.org) | **Mastery learning** levels + adaptive gap diagnosis + gating | Technique reference |

### Direct answers

1. **Is "adaptive, evidence-based readiness" a differentiator or table stakes?**
   The *techniques* are table stakes (spaced-repetition learner models and mastery
   learning are 20-year-old solved tech), but **no interview-prep product ships a
   per-user adaptive readiness model** (predicted readiness + a failure fingerprint
   + a plan that re-routes around it). LeetCode's contest rating is the nearest
   quantitative score, and it is a competitive rank, not interview readiness. So a
   *real, evidence-based* learner model is still open space — provided it's not just
   an "AI mock" wrapper.

2. **Who is closest to "learner model + failure fingerprint + adaptive planner"?**
   Two products each hold a piece, nobody holds all three:
   - **Duolingo** has the learner model (skill decay + "what to practice next").
   - **Interviewing.io** has the failure fingerprint + evidence (expert diagnosis of
     *exactly* what to improve) and real-outcome data.
   - **CodeSignal** has role-benchmarked gap analysis, but employer-facing.
   The fusion is unclaimed.

3. **Is "feedback from real interview outcomes" shipped anywhere?**
   Mostly open space. Interviewing.io is the only player that genuinely closes
   mock→real→offer on-platform, and even it uses outcomes for research/matching,
   **not** to update a personalized readiness model. Feeding real pass/fail/offer
   data back into the model is open space — and the hardest part to replicate,
   because only interviewing.io has the real-outcome data. A private cohort has
   even less, which is exactly why IDEAS.md parks it.

4. **Is "AI mock / AI chat coach" a moat?**
   No. Fully commoditized: LeetCode Interview, interviewing.io AI Interviewer,
   CodeSignal AI Interviewer, HelloInterview AI tutor, plus a long tail (LadeAI,
   LeetDuck, CrackTheOffer, FinalRound AI, …). The moat is the *evidence/outcome
   loop + adaptive model behind* the mock, not the mock itself.

### What this means for 90x

- Voice / AI-mock is not the next move; it's the layer on top.
- The failure fingerprint + learner model is the defensible core — and it's
  unclaimed.
- The outcome loop is real long-term moat but needs real-outcome data 90x won't
  have while invite-only.

---

## 2. Learner-model techniques — what's right for a small, private cohort

Collected 2026. Primary sources are academic (inline). The through-line: **every
statistical family needs many learners × many attempts per skill; a private cohort
has neither. The right first move is a transparent, evidence-counted skill model
that borrows the *ideas* of the psychometric models without their estimation
machinery.**

### The techniques, one paragraph each

- **Bayesian Knowledge Tracing (BKT)** — 2-state hidden Markov per skill
  (learned/not-learned), four params (prior, learn rate, guess, slip), updated per
  attempt. *Explainable* (P(know) is literally "probability they know it"), but
  "cannot be reliably fit unless there is a sufficiently large pool of students with
  ≥3 opportunities per skill" ([cold-start analysis](https://ceur-ws.org/Vol-3051/UGR_7.pdf);
  [identifiability](https://jedm.educationaldatamining.org/index.php/JEDM/article/download/35/pdf_27)).
  ❌ as-is. *Borrow:* the forward-update intuition (correct ⇒ P(know)↑, slip-tolerant).
- **Item Response Theory (IRT)** — latent ability θ vs item difficulty b; P(correct)
  is logistic in a(θ−b). Item-parameter estimation needs n≈500–1000+ examinees,
  person estimates want 20–30 items each
  ([PLOS One](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0347684);
  [SAGE](https://journals.sagepub.com/doi/10.1177/25152459251314798)). ❌. *Borrow:*
  the learner-vs-difficulty framing only.
- **Elo rating** — online paired update per interaction; the *most* cold-start-robust
  of the family (≈0.70 correlation by n=5, ≈0.85–0.90 by n=50;
  [Pelánek survey](https://dl.acm.org/doi/10.1007/s11257-016-9185-7)). ⚠️ single
  unanchored scalar, no built-in "why". *Use:* a light fallback for problem-difficulty
  ordering only.
- **Deep Knowledge Tracing (DKT)** — RNN over answer sequences (Piech 2015,
  [arXiv:1506.05908](https://arxiv.org/abs/1506.05908)). ❌ needs hundreds of
  thousands of interactions and is opaque. Non-starter here.
- **Mastery learning thresholds** (Khan / Bloom) — no model, just a gate: reach a
  threshold to advance. ✅ maximally legible ("4/7 on linked lists, need 90%"). *Use:*
  the display/decision layer, backed by a better estimator.
- **FSRS** — per-*card* memory model: Difficulty D, Stability S, Retrievability
  R(t,S). 90x already runs it (`web/src/lib/feed/srs.ts`). ✅ **The strongest raw
  asset**: D is "how hard for you", S/lapses are "how durable"; roll up cleanly to a
  per-skill *memory* signal. *Caveat:* FSRS measures recall/retention, not
  problem-solving/application, so it undercounts synthesis skills
  ([FSRS wiki](https://github.com/open-spaced-repetition/awesome-fsrs/wiki/The-Algorithm)).
- **SPARFA / empirical Bayes** — sparse factor analysis + Bayesian shrinkage of noisy
  per-skill estimates toward a pooled prior; explicitly built for the sparse regime
  ([SPARFA arXiv:1303.5685](https://arxiv.org/abs/1303.5685);
  [cold-start mitigation](https://link.springer.com/article/10.1007/s11257-024-09401-5)).
  ✅/⚠️ the *shrinkage idea* transfers even if the full model is overkill for ~50 users.
- **Mastery Grids / Open Learner Models** — not an algorithm, an *interface*: per-topic
  mastery rendered as a grid of colored cells, driven by a topic score
  ([Brusilovsky et al., IEEE TLT 2016](https://doi.org/10.1109/TLT.2015.2508643)).
  ✅ steal the visualization.

### The recommendation (what IDEAS.md #2 should concretely be)

A **transparent, multi-signal skill-strength estimator with empirical-Bayes
shrinkage and a per-signal evidence breakdown** — not a black-box score. For each
skill tag, combine five signals we already store, each surfaced as a sentence so
"why do I think you're weak here" *is* the list of contributing signals:

1. **FSRS roll-up (memory)** — mean/median D (inverted), stability, lapse rate →
   "recall is shaky: 3 lapses on hash-table cards, stability 2 days".
2. **Check-ins (application)** — weighted accuracy that *penalizes hints and
   failures*, not just solved rate.
3. **Solution reviews (understanding)** — complexity-comparison delta →
   "missed the O(n log n) angle".
4. **Mock rubric (calibrated anchor)** — the 1–5 per-criterion scores, high-signal
   but low-frequency.
5. **Coach memory (hand-authored prior)** — a coach's `strength`/`habit` note is a
   prior, exactly what a small cohort can afford to hand-curate.

Each signal carries **confidence = f(evidence count)**; when n is small the score
shrinks toward a neutral prior (0.5, or the coach's prior) — empirical Bayes, not a
fragile per-skill fit. Render it like a Mastery Grid with a Khan-style threshold and
a per-signal "why".

**Net:** deterministic and fully enumerable now; BKT/SPARFA only add value if the
cohort ever reaches the hundreds with dense per-skill evidence.

*Skepticism note:* the exact sample-size cutoffs (500/1000/3000) are simulation
guidelines, not hard limits — but every source agrees a ~50-user, sparse-evidence
regime sits far below IRT/BKT/DKT's comfortable operating point.*
