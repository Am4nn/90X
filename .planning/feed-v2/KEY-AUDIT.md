# Answer keys that contradict their own explanations

Found 2026-10-03 while checking a repaired grid card. Not caught by any gate, because no
gate checks it.

## What was wrong

A card has a question, a key (what it is marked against) and an explanation (what the
reader sees afterwards). They are written together, so they should agree. For two
primitives they often did not:

| primitive | audited | key contradicts explanation |
|---|---|---|
| `grid_toggle` | 109 | **55** (50%) |
| `assemble` | 181 | **32** (18%) |
| `claim_grid` | 335 | 26 (8%) |
| `tap_in_place` | 218 | 17 (8%) |
| `pick_one` | 1,480 | 21 (1.4%) |
| `match` | 406 | 3 |
| `numeric` | 98 | 3 |
| `order` | 385 | 3 |
| `bucket` | 297 | 2 |
| **all keyed primitives** | **3,509** | **162 (4.6%)** |

A reader who knows the answer is marked wrong, or is shown an explanation that
disagrees with the answer they were marked against.

**The first audit over-flagged, and the correction is part of the result.** It retired 162
cards, each flagged by a cheap model and then confirmed by a stronger one *from the same family
reading a key worded the same way*. Reading nine by hand, and then fourteen more the strong
model flagged on cards the cheap pass had called clean, showed that a share were false flags
caused by the wording of the key, not by the cards:

- a tap-the-bug card's key was rendered "Marked correct: `lock.lock();`", but that line IS the
  bug and the explanation says so; the auditor read "correct" as "correct code";
- a rebuilt assemble line was joined with spaces and flagged against an explanation written
  without them ("-XX: MaxMetaspaceSize = 256m" against "-XX:MaxMetaspaceSize");
- a numeric key of 2.0 was flagged against "O(n^2)" when the question asked for the exponent.

Both passes made the same misreading, so their agreement proved less than it looked. The key
wording and the auditor's instructions were fixed, and every flagged card was re-judged by two
models of **different families** (`deepseek-v4-pro` and `kimi-k3`, over OpenCode Go):

| outcome of the independent retest | cards | what happened |
|---|---|---|
| both models say the key agrees | 22 | 14 were retired and are **restored**; 8 were live and stay |
| both models say it contradicts | 102 | stay out (101 already retired, 1 live card newly retired) |
| the two disagree, or either is unsure | 52 | left where they were: 47 stay retired, 5 stay live |

So of the 162 first retired, 14 were false flags and are back; 101 are confirmed genuine by two
families; 47 are unresolved and left retired, the safe side. Production is **3,612 live**.

Reading them also shows two real defects that want different repairs. Some cards have a
genuinely wrong key (a subquery card marks "non-correlated" correct while its explanation says
it is correlated). Others have a right key under an explanation that is misnumbered or garbled.
The audit cannot tell them apart, it only says the two disagree. The second kind is repairable
by rewriting the explanation, which is why the cards are archived, not deleted.

## Why nothing caught it

`gate.judge` compares a blind reviewer's pick with the key, but only inside
`if card.format == "mcq"`, the legacy format. It is the same guard that once hid every
primitive's options from the gate. For `pick_one` and everything after it, the key
passes `wellformed`, which asks whether a key is *well formed*, not whether it is
*right*.

## Why grids in particular

`write.py` told the model: "Set `picked` to the 0-based cell indices, row-major, that are
correct." A cell's flat index is `row * columns + column`, and the model was doing that
multiplication in its head. It got it wrong in about half the grids, and the errors are
quiet: an index outside the grid is caught, but one that lands on the wrong cell is just
another valid cell. `write.py:212` already carried a comment about models leaking "I need
to adjust the picked indices" into this field, which is what struggling with it looks like.

Assemble stores ordering constraints over tokens, with the same failure shape: an index
the validator accepts that points at the wrong token.

## What changed

- **The writer names cells, the code multiplies.** `grid_toggle` now asks for
  `cells: [[row, column], ...]` and `write.grid_picked` computes the flat indices,
  refusing anything outside the grid. A grid that still sends flat `picked` is refused.
- **`cards/key_audit.py`** renders every key as plain sentences (a grid decoded cell by
  cell, an order as its rules, an assemble as the line it builds) and asks a model
  whether the explanation agrees. Three-valued on purpose: `agrees`, `contradicts`,
  `unclear`. An explanation that is silent about part of a key is not a contradiction,
  and rejecting on silence would discard good cards. A missing verdict is a schema
  error, so it is retried and never read as agreement.
- **`scripts/key_audit.py`** runs it: `--pilot N` for a stratified sample,
  `--formats grid_toggle,assemble` to narrow, `--from FILE` to apply a saved result
  without paying for the calls again. Nothing is rejected without `--apply` or `--from`.

## What re-reading the cheap pass found

The cheap first pass only had its *flags* double-checked, so a card it called clean was never
re-read. Sampling 300 of those with the strong model flagged 14 (4.7%), and on reading, about
half of the 14 were the wording false flags above. After the wording fix the independent retest
cleared 8 of them and confirmed 1; 5 stay unresolved. The honest reading is that the cheap
pass misses a small share, in the low single digits of a percent, and that this has not been
measured over the whole clean corpus.

## Not done

- **The 149 cards still retired for a key/explanation mismatch are not repaired.** Some need a
  corrected key, some only a corrected explanation; deciding which is the work. For grids the
  key can be re-derived from the prose: the model names, per row, which columns the explanation
  supports, and the code computes the indices.
- **47 retired cards and 5 live ones are unresolved**: the two models disagreed or were unsure.
  They are not known to be wrong.
- **The strong pass has not been run over every card the cheap pass called clean**, only over a
  sample of 300 and over everything flagged. Running it everywhere (about 3,300 cards, free on
  OpenCode Go) would close the remaining gap.

## Running it again

```
cd pipeline
PIPELINE_MAX_USD=<lifetime spend + headroom> uv run python scripts/key_audit.py --pilot 120
```

The cap is on lifetime spend, not on the run, so set it above what the ledger already shows.
The script opens the database read-write even for a dry run, because the LLM client records
each call's cost there; opened read-only, every call fails after the API has already
answered and been paid for.

## Running it on OpenCode Go, and its limit

The audits ran on OpenCode Go (a $10 subscription, $0 on the ledger; see `RUNBOOK.md`), which
has a 5-hour window of 20% of the month's allowance. The first full audit, the recheck and the
retest together used it up in one sitting: the next call came back `429 GoUsageLimitError`
with `Retry-After: 14203`, about four hours. The script prints each failed call but carries
on, so a run that hits the limit looks like many `FAILED RateLimitError` lines and a result
of zero, not a crash. Check the first few lines before waiting on a long run, and budget a
full audit as most of a window.

The retest wants two model families (`AI_MODEL_FAST=deepseek-v4-pro`,
`AI_MODEL_SMART=kimi-k3` worked). Using one family twice is what let a wording flaw be
"confirmed" in the first place.

## Repairing the retired cards

`cards/key_repair.py` and `scripts/repair_keys.py` re-derive a retired card's key from its own
explanation, validate it with `wellformed`, then audit the *repaired* card with two families
and write it only if both agree. Built and unit-tested (`tests/test_key_repair.py`); a pilot on
20 cards hit the limit above and returned nothing, so **it has not yet run against real
cards**. Order cards are left out (three of them; their key is rules, not a sequence).
