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
disagrees with the answer they were marked against. All 162 were retired from
production (3,760 to 3,598 live), each confirmed by two independent passes: a cheap
model, then a stronger one re-reading only what the first flagged. The first 87 were
retired after three were read by hand; the other 75 after six more were.

**Reading those nine showed two different defects, and they want different repairs.**
Some cards have a genuinely wrong key (a subquery card marks "non-correlated" correct
while its own explanation says it is correlated). Others have a key that looks right and
an explanation that is misnumbered or garbled ("statements 1 and 3 are true" above text
that makes statement 1 false). The audit cannot tell them apart, it only says the two
disagree. The second kind is repairable by rewriting the explanation, which is why the
cards are archived, not deleted.

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

## Not done

- **The 162 retired cards are not repaired.** They are rejected in staging, retired in
  production, and in `.data/review/rejected-cards.jsonl`. Some need a corrected key, some
  only a corrected explanation; deciding which is the work. For grids the key can be
  re-derived from the prose: the model names, per row, which columns the explanation
  supports, and the code computes the indices.
- **54 cards came back `unclear` on the first pass** and were not acted on. The
  explanation did not say enough to tell. They are not known to be wrong.
- **The cheap first pass can miss.** A card the cheap pass called `agrees` was never
  re-read by the stronger model. Measured recall is unknown; sampling a few hundred of the
  `agrees` with the strong model would give it.
- Retiring cards re-arms the swap bug (`SWAP-BUG.md`) until the `published_at` fix is in.
  **Do not run `pipeline swap`.**

## Running it again

```
cd pipeline
PIPELINE_MAX_USD=<lifetime spend + headroom> uv run python scripts/key_audit.py --pilot 120
```

The cap is on lifetime spend, not on the run, so set it above what the ledger already shows.
The script opens the database read-write even for a dry run, because the LLM client records
each call's cost there; opened read-only, every call fails after the API has already
answered and been paid for.
