# Part F — the gates (pipeline)

**Branch** `feed-v2-gates` · **Worktree** `../90X-wt-fv2/f` · **No Playwright spec** — Python
pipeline. Depends on **A** (registry). Runs after E produces cards; the blind gate is new.

F is where guessability is checked before a card ships. Three layers: the **blind gate** (new),
**structural rules** (free), and the **difficulty rubric** (DECISIONS round 3). `fix.py` repairs
rejects and `regate.py` re-judges, as today.

## Scope

- **Blind gate, new**: show a model only the options (no lesson, no topic, no area), ask it to
  answer. **Three samples; reject at two or more correct.** If the reader could guess it, the
  model can too, and it gets rewritten.
- **Structural rules, free**: options within a length band, no option that is the only one of its
  kind, no "all of the above".
- **Difficulty rubric**: assign Easy/Medium/Hard by the round-3 table, not the writer's label.
- **Gate 2 lives here**: run the blind gate over 50 cards, report the rejection rate, stop.

## Files

**Create**
- `pipeline/src/pipeline/cards/blind_gate.py` — the options-only reviewer.
- `pipeline/src/pipeline/cards/structure.py` — the free structural rules.
- `pipeline/src/pipeline/cards/rubric.py` — the difficulty rubric.
- `pipeline/src/pipeline/cards/gate2.py` — the 50-card trial that reports the rejection rate.

**Modify**
- `pipeline/src/pipeline/cards/gate.py` — keep `review`/`judge`/`malformed`; add the blind and
  structural stages ahead of them.
- `pipeline/src/pipeline/cards/fix.py` — repair rejects (blind-gate rejections reuse the
  rewrite path).
- `pipeline/src/pipeline/cards/regate.py` — re-judge against the lesson, as today.

## Reuse, do not rewrite

```
# gate.py (today)
def review(llm, topic, cards, tier="review") -> GateResult;
def judge(cards, result) -> list[(card, reason)];
def malformed(card) -> str;
def prompt_only(card) -> str;          # the reader's view; blind gate shows even less
def confidence_by_card(cards, result) -> dict[int, float];

# from_lessons.py
def rewrite(llm, topic, lesson_md, rejected, tier) -> list[Card];

# fix.py / regate.py — the repair and re-judge loops; extend, do not replace
# llm.py — LLM, complete_json, spend_usd, PIPELINE_MAX_USD
```

## The blind gate — the new thing

- Input to the model: **the options only** for a chosen/mapping/ordering card — no prompt, no
  lesson, no topic, no area. For a non-chosen card (numeric, tap-in-place), the gate sees only
  what a reader without the lesson sees (the snippet, the tokens) — never the source.
- **Three samples per card** (three independent model calls or one call asked three times).
  **Reject at two or more correct.** One sample would reject a quarter of good cards by luck;
  three brings a false reject to ~16%, and a false reject only costs a rewrite (DECISIONS round 4).
- The rejection reason is "guessable", which `fix.py` turns into a rewrite with the options
  made genuinely competitive.

## The structural rules — free, in code, before any model call

- options within a length band (none absurdly longer or shorter than the rest),
- no option that is the only one of its kind (the one number, the one code block),
- no "all of the above" / "none of the above".

These catch elimination-by-shape, the giveaway the blind gate cannot see.

## The difficulty rubric

Encode the DECISIONS round-3 table as a scoring function over the card's stated properties
(reasoning steps, whether a stated constraint changes the answer, whether it spans multiple
facts, whether distractors encode real misconceptions, whether it needs a calculation):

| | Easy | Medium | Hard |
|---|---|---|---|
| reasoning steps | 1 | 2 | 3+ |
| a stated constraint changes the answer | no | sometimes | yes |
| spans more than one fact | no | no | yes |
| distractors encode real misconceptions | not required | yes | yes |
| needs a calculation | no | maybe | yes |

The rubric writes `difficulty`; the writer's label is ignored.

## Gate 2 — validate before you spend the rest

- Take 50 freshly generated cards through the **blind gate**.
- Report the **rejection rate**.
- **Stop.** If it rejects half, the gate is wrong, not the corpus — the number goes to the
  orchestrator, not into more generation.
- Set `PIPELINE_MAX_USD` on the invocation and report cumulative `spend_usd`.

## Tests (pytest)

- `structure.py` — a sole-of-kind option, an out-of-band length option, and an "all of the
  above" option each fail; a clean set passes.
- `blind_gate.py` — the model is shown options and nothing else (assert the prompt contains no
  lesson/topic/area text); 3 samples; reject-at-2 logic.
- `rubric.py` — each row of the round-3 table maps to the expected difficulty for a synthetic
  card.

## Traps

- **No production, no `publish`.** This is staging only.
- **The blind gate is a pipeline check and changes nothing the reader sees.** `answerMd` and the
  key points stay exactly as they are.
- **If the Gate-2 rejection rate is implausible, report it; do not weaken the gate.** A gate
  that rejects half is wrong, and fixing it is a separate decision, not something F resolves by
  loosening thresholds.
- **Three samples, reject at two.** Do not "optimise" to one sample to save money; the false
  reject is the point of three.

## Verification

`uv run pytest`. Run Gate 2 over 50 cards, report the rejection rate and cumulative spend.
No web checks apply.

## Decisions (with cost if wrong)

- **Blind gate is a separate reviewer call, not a prompt tweak to `gate.review`.** Cost if
  wrong: folding it in would let the source text leak into the guess, defeating the gate.
- **Structural rules run before the model** (free, deterministic, and they catch the giveaway
  the blind gate cannot). Cost if wrong: none — they only add rejections the repair pass fixes.
