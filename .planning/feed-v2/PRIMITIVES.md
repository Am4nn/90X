# The primitives, walked through

Round 1 had 8. Round 2 adds 6, for **14 primitives over 5 answer shapes**.

The count that matters is the answer shapes, not the primitives. A shape is a thing the
grader, the stored attempt and every consumer of an answer must understand. A primitive is a
screen. Screens are cheap and independent; shapes are load-bearing and shared.

| shape | what is stored | used by |
|---|---|---|
| chosen set | indices picked | pick one, pick many, grid toggle, pick-then-justify |
| ordered list | indices in order | order, assemble |
| mapping | item → target | match, bucket, claim grid |
| **number** *(new)* | a value + the tolerance it was judged against | numeric entry |
| **span** *(new)* | start and end token index | highlight a span |

Everything below is graded by a pure function. That is the admission test from round 2, and
all six clear it.

---

## 9. Numeric entry

**The reader** taps a number on a keypad. No prose, no options.

**Shape** number. **Graded by** `|given - expected| <= tolerance`, with the tolerance stored on
the card — exact for a count, an order of magnitude for an estimate.

**Needs** a numeric fact with a defensible tolerance. We hold plenty: complexities as
exponents, storage estimates, row counts, latencies.

**Unlocks** *Estimate* and *Complexity* properly. Both are currently four options, and four
options teach the reader to eliminate rather than to calculate — which is exactly the skill an
interviewer is probing when they ask for a back-of-envelope number.

**Risk** it is typing, and typing is what we removed. The defence: a keypad is not prose. It is
three taps, there is nothing to phrase, and no model is needed to mark it. If it still feels
like work in practice, this is the first one to drop.

---

## 10. Claim grid — true or false on every row

**The reader** marks each of four or five statements true or false. Every row needs an answer.

**Shape** mapping (claim → boolean). **Graded by** every row matching.

**Needs** statements with a known truth value about one topic — which is what a lesson's key
points already are, plus their negations.

**Unlocks** the thing *pick many* cannot do. "Select the true ones" lets a reader ignore the
options they are unsure about; a grid makes them commit on all of them. Same content, much
harder to pass by recognition, and it exposes the half-knowledge that multiple choice hides.

**Risk** five forced judgements marked all-or-nothing is the harshest card in the catalogue
under the no-partial-credit rule. Three or four rows, not six.

---

## 11. Grid toggle — a small matrix

**The reader** ticks cells in a table: structures down the side, operations across the top,
tick where the operation is O(1).

**Shape** chosen set, where each cell is one key. No new shape needed.

**Needs** a 2D fact table. DSA is full of them — the complexity table every interview assumes
you know — and so is SQL isolation behaviour.

**Unlocks** facts that are genuinely two-dimensional. Bucketing flattens them into one
dimension and loses the point: "which of these is O(1)" is a much weaker question than "O(1)
*for which structure*".

**Risk** the smallest viable grid is 3×3 and that is already nine taps and a scroll on a
phone. Keep it to 3×3, and never on a phone in landscape only.

---

## 12. Highlight a span

**The reader** taps the first token, then the last. The range between them is the answer.

**Shape** span (start, end). **Graded by** the span matching, with an allowance of a token at
each end so an off-by-one tap is not a wrong answer.

**Needs** a snippet with a meaningful region: the sliding window, the critical section, the
subquery that scans.

**Unlocks** "where is it" questions that a single tap cannot express. *Tap in place* finds a
point — the bug is on line 7. A span finds an extent, and extents are how you actually read
code: the window, the lock's scope, the transaction's boundary.

**Risk** the second new shape, and the fiddliest interaction on a small screen. Worth it only
if the span is short; selecting eleven lines by tapping two ends is worse than picking from
four options.

---

## 13. Assemble from a token pool

**The reader** taps tokens in order to build a line: a SQL statement, a method signature, a
regex.

**Shape** ordered list. **Graded by** the sequence matching, or satisfying declared constraints
where clause order genuinely does not matter.

**Needs** a correct line and a pool of plausible distractor tokens.

**Unlocks** syntax precision without typing — which is the whole reason typing died. *Word
bank* fills gaps in text that is already there; assembling builds the statement from nothing,
which is a much better test of whether someone can actually write `GROUP BY ... HAVING` rather
than recognise it.

**Risk** SQL clause order is partly free, so this leans hard on the constraint model from round
2. Get that wrong and readers get marked wrong for correct SQL, which is the most annoying
possible bug.

---

## 14. Pick, then justify

**The reader** picks an answer, then picks the reason from a second set of options. Both must
be right.

**Shape** chosen set of two. **Graded by** both picks matching.

**Needs** an answer and a set of plausible reasons, one of which is the real one — and the
distractor reasons must each be a reason somebody actually gives.

**Unlocks** the one thing pick-one can never do: **detect being right by accident.** On four
options a reader is right 25% of the time knowing nothing. Requiring the reason collapses that
to 6%, and the second half is where the learning is — "right answer, wrong reason" is the most
useful thing a card can ever tell somebody.

**Risk** two screens for one card, so it is slower, and the Feed is built on cards being fast.
Best used sparingly, on the cards where the reasoning is the point.

---

## Deliberately not adding

**Connect the edges** — build a dependency graph by joining nodes. Genuinely good on a desktop
and genuinely miserable at 390px, where the Feed mostly lives.

**Stepwise simulation** — step through code answering at each step. It is several cards
pretending to be one, and it breaks the "a card is one question with one mark" model the whole
Feed rests on.

**Slider** — a scale you drag. Collapses into numeric entry with a worse input, and drag fights
the page scroll, which is the same reason ordering is tap-to-place.

---

## What this does to the build

The 8 round-1 primitives are 8 screens. These 6 are 6 more, of which **four need no new answer
shape** and so no new grading concept: claim grid and grid toggle are a mapping and a chosen
set, assemble is an ordered list, pick-then-justify is two chosen sets.

**Numeric entry and highlight-a-span are the only two that widen the contract.** If the build
needs trimming, trim those two — and note that numeric entry is also the one that most improves
existing archetypes, so the trim is not free.

---

## The final set — 11 primitives, 4 answer shapes

Aman kept five of the six new ones (**highlight a span is out**, so the span shape goes with
it), then asked whether any of the thirteen should be cut. Two should, and in both cases
because they were not distinct interactions — they were special cases of something else on the
list.

**Cut: pick many.** Its three archetypes rehome with nothing lost and two of them improved.
*All that apply* is a **claim grid** done properly: "select the true ones" lets a reader
silently skip every option they are unsure about, and the grid makes them commit on each.
*Odd one out* is a **pick one** — one item selected, it was only ever grouped here by
association. *Which invariants hold* is a claim grid. Pick many's only remaining argument was
that it is a lighter interaction, and "lighter" here means "lets you dodge the hard rows".

**Merged: word bank into assemble.** The same interaction at two difficulty settings, both
storing an ordered list. A word bank is assemble with most of the answer pre-filled. One
primitive with a template: empty is assemble, mostly-full is a word bank. One screen, one
grading function, and **difficulty becomes a property of the card rather than a fork in the
codebase** — so the pipeline can dial it per topic without a new format.

| # | primitive | shape | status |
|---|---|---|---|
| 1 | Pick one | chosen set | exists (`mcq`) |
| 2 | Order | ordered list | new |
| 3 | Match | mapping | new |
| 4 | Bucket | mapping | new |
| 5 | Tap in place | chosen set | partly (`bug`, as typed) |
| 6 | Self-rate | — | exists (`flash`) |
| 7 | Assemble *(templated)* | ordered list | new |
| 8 | Numeric entry | **number** | new |
| 9 | Claim grid | mapping | new |
| 10 | Grid toggle | chosen set | new |
| 11 | Pick, then justify | chosen set ×2 | new, **build last** |

**44 archetypes, all rehomed. Four answer shapes**, one of them new.

### Two things kept on purpose

**Bucket is technically a constrained grid toggle** — an M×N grid with exactly one tick per
row — and it stays a separate screen anyway, because a five-item bucket list works at 390px
and a 5×3 grid does not. Share the grading function, not the UI.

**Self-rate has no right answer**, which makes it look like the odd one out. It stays: it is
free, it already exists, and "do I know this term" is a different question from "can I answer
about it".

### Pick-then-justify is last for a reason

It may not be a primitive at all. It is two pick-ones chained, which makes it a **card-level**
feature — *any card may have a follow-up step* — and framed that way it would give "right
order, wrong reason" for free on ordering and matching too. That is the better design and it
touches the card contract rather than adding a screen, so it goes last, once the shape of an
attempt has settled. The value is worth waiting for: it is the only thing in the catalogue that
takes a lucky 25% down to 6%.
