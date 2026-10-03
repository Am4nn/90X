# Answer keys that contradict their own explanations

Found 2026-10-03 while checking a repaired grid card. Not caught by any gate, because no
gate checks it.

## What was wrong

A card has a question, a key (what it is marked against) and an explanation (what the
reader sees afterwards). They are written together, so they should agree. For two
primitives they often did not:

| primitive | audited | key contradicts explanation |
|---|---|---|
| `grid_toggle` | 109 live | **55** |
| `assemble` | 181 live | **32** |
| the other eight, sampled 13 each | 104 | 0 |

A reader who knows the answer is marked wrong. 87 live cards were retired from
production on this evidence, each confirmed by two independent passes (a cheap model,
then a stronger one re-reading only what the first flagged) and three read by hand
against their explanations before anything was retired.

The other eight primitives came back 0 of 13 each. That is a sample, not a
clean bill: 13 clean cards cannot rule out a rate of 15 to 20%. The remaining
corpus has not been audited in full.

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

- **The remaining ~3,000 cards are unaudited.** Estimated at under $1 on the cheap tier.
- **The 87 retired cards are not repaired.** Their explanations are probably right and
  their keys wrong, so the key can be re-derived from the prose: the model names, per
  row, which columns the explanation supports, and the code computes the indices. Then
  re-audit. Not yet built.
- **The 54 grids and 149 assembles still live passed both passes.** A cheap first pass can
  miss, so they have only been read once by a strong model, and only if the cheap one
  flagged them.
- Retiring the 87 re-armed the swap bug (see `SWAP-BUG.md`): there are now archetyped
  retired cards for `pipeline swap` to resurrect. **Do not run it.**

## Running it again

```
cd pipeline
PIPELINE_MAX_USD=<lifetime spend + headroom> uv run python scripts/key_audit.py --pilot 120
```

The cap is on lifetime spend, not on the run, so set it above what the ledger already shows.
The script opens the database read-write even for a dry run, because the LLM client records
each call's cost there; opened read-only, every call fails after the API has already
answered and been paid for.
