You are building **Part F of Feed v2: the gates (pipeline)**.

**Worktree** `../90X-wt-fv2/f` · **Branch** `feed-v2-gates` · **No Playwright spec** — Python
pipeline. You depend on **A** (the registry) and run after E produces cards.

You check guessability before a card ships: the **blind gate** (new), **structural rules**
(free), and the **difficulty rubric** (DECISIONS round 3). `fix.py` repairs rejects and
`regate.py` re-judges.

## Read these first, in this order

1. `.planning/feed-v2/plans/prompts/SETUP.md` — §3 (pipeline parts) especially.
2. **`.planning/feed-v2/plans/F-gates.md` — your plan.** The blind gate, the structural rules,
   the rubric table, the Gate 2 trial, the traps.
3. `.planning/feed-v2/plans/README.md`
4. `.planning/feed-v2/DECISIONS.md` round 4 — the three-sample blind gate reasoning.
5. `pipeline/src/pipeline/cards/gate.py`, `fix.py`, `regate.py` — read before changing.

## The traps that will cost you most

1. **No production, no `publish`.** Staging only.
2. **The blind gate shows options and nothing else** — no lesson, no topic, no area. Fold the
   source text in and the gate is defeated.
3. **Three samples, reject at two or more correct.** Do not "optimise" to one sample to save
   money; the false-reject protection is the point of three.
4. **Structural rules run before the model**, free and deterministic.

## Gate 2 — validate before you spend the rest

Run 50 freshly generated cards through the blind gate, report the **rejection rate**, and
**stop**. If it rejects half, the gate is wrong, not the corpus — the number goes to the
orchestrator, not into more generation. `PIPELINE_MAX_USD` on the invocation; report cumulative
spend.

## Verification

`uv run pytest`, then run Gate 2 over 50 cards and report the rejection rate and cumulative
spend. No web checks apply.

Report back as SETUP.md §10 describes — and make the Gate 2 rejection rate the first line.
