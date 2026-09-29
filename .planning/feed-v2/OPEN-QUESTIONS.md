# What is still open

Round 1 left seven. Round 2 (2026-09-30) closed all seven — see DECISIONS.md. What remains is
plan-level detail, not design disagreement: each one can be decided while writing the plan
without changing the shape of the thing.

## Closed in round 2

| # | was | settled as |
|---|---|---|
| 1 | what stops a guessable card | blind-answer gate in the pipeline + free structural rules |
| 2 | how format gets assigned | per-topic budget, one named format per writer call, writer may refuse |
| 3 | which archetypes are eligible where | the areas column in CATALOGUE.md; behavioural stays exactly as today |
| 4 | tap-to-place, partial credit, comparability | tap-to-place never drag; **no partial credit**; outcomes unchanged |
| 5 | two valid answers | the card declares its constraints; the grader checks them |
| 6 | regeneration | fresh from the lesson to budget; typed retired not deleted; ~$2.30 + ~$1 |
| 7 | the problem link | not an answer, not a skip; `currentKey` already re-serves the card |

The answer to 5 also changed the architecture: **no model in the loop when a Feed answer is
marked.** That is now the admission test for every archetype.

## Still open, all plan-level

### 1. The blind gate's false-negative rate

A model shown four options with no context is **right 25% of the time by luck**, so a single
attempt would reject a quarter of perfectly good cards. Needs one of: an explicit "cannot
tell" answer and reject only a confident correct answer; or three samples, rejecting at two or
more correct. The second is three times the cost of a $1 pass, which is still $3. Decide with
a measurement on 50 cards, not by argument.

### 2. What "retired" is, in the schema

`cards.status` is `live | draft` today. Retiring 1,383 cards needs a third value, which is a
migration, which means the lead writes it. Also: does a retired card keep its `card_state`
rows, so a reader's history survives? Probably yes — deleting FSRS history to change a card's
format would be a real loss.

### 3. Budget numbers

How many cards per topic, and what mix. "2 complexity, 2 counter-example, 1 ordering…" was an
illustration, not a proposal. Wants looking at against real topic sizes, and it is the kind of
number that should be easy to change afterwards.

### 4. Item counts per primitive

How many pairs in a match, columns in a bucket, steps in an order. Five pairs was an example.
On a 390px phone this is a layout question as much as a pedagogy one, and it interacts with
the no-partial-credit decision: eight pairs marked all-or-nothing would be punishing.

### 5. The two extra primitives

Numeric keypad and grid toggle, raised in round 2 and not decided. Both need a **fourth answer
shape** — a number, and a set of cells — which is the real cost. Estimate and Complexity would
both be better as a keypad than as four options, so this is worth settling before the grader's
answer types are fixed rather than after.
