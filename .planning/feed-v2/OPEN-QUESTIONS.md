# What we did not settle

Explicitly open, so nobody later reads silence in the other two files as
agreement. Each one would change the design, which is why none of them were
guessed at.

## 1. What stops a card being answerable by someone who knows nothing

The risk with the highest cost and the lowest visibility. A pick-one card is
only as good as its wrong answers: three implausible options and the reader
eliminates by shape — the long one, the one with a number, the one that is not
like the others — without thinking about the subject at all.

It does not look broken. Beside its lesson the card reads perfectly well. It is
only trivial in the Feed, where nobody is watching.

The current gate asks *"is this answerable without the lesson in front of you?"*
That is a different question from *"is this answerable without knowing
anything?"*, and the second is the one that matters here. Nobody has proposed
how to check it.

Sketches raised but not chosen:
- a model answers the card with the topic withheld; if it gets it right, the
  distractors are too weak
- structural rules — options within a length band of each other, no option that
  is the only one of its kind
- generate distractors from *other* lessons' real claims, so each is something
  somebody actually believes

## 2. How format gets assigned

Ask a model for a card and you get multiple choice, every time — it is the
easiest thing to produce. Leave the choice to the writer and the database ends
up 85% multiple choice with 29 formats in the schema.

So something has to assign it. Unsettled:
- a per-topic budget the pipeline fills, or the format picked first and the
  writer asked for that specific thing
- whether the budget is per topic, per area, or per batch
- what happens when a topic genuinely has no good ordering question — is a
  strained card worse than an absent one?

## 3. Which archetypes are eligible where

[CATALOGUE.md](CATALOGUE.md) suggests areas per archetype, but that is a first
pass and nobody has checked it against real topics. Estimate is meaningless for
Java syntax; ordering suits protocols, not behavioural.

Related and unasked: does behavioural belong in the Feed at all? Almost nothing
in the catalogue fits it.

## 4. Tap-to-place, and what a wrong answer means

Ordering, matching and bucketing all suggest drag-and-drop, and drag inside a
scrolling page on a phone fights the scroll. Tap-to-place — tap the item, tap
where it goes — is the same data model and better on the device.

Not settled, and cheap now but annoying after three UIs exist. Also unsettled:

**Partial credit.** Four of five pairs matched — right or wrong? An ordering
with two items swapped is nearly right; an MCQ is never nearly right. If partial
credit exists, every consumer of the answer has to understand it.

**Whether formats are comparable.** Does a wrong ordering mean the same about
the reader as a wrong multiple choice? FSRS schedules on a right/wrong signal
and readiness moves on it. If an ordering card is simply harder, the same signal
means something different, and neither the scheduler nor the dial knows.

## 5. Two valid answers

An ordering card can have two correct orders where steps are independent. A
matching card can have a term that honestly fits two definitions. Both are as
broken as a typed card with no key points, and the gate would not notice either.

Nothing proposed. It probably needs a rule per primitive rather than one rule.

## 6. What regenerating 1,383 cards actually costs

Decided that they get regenerated. Not decided:
- the cost, which nobody has estimated
- whether it is a conversion per card or a fresh generation from the lesson
- whether the human review sample has to be redone from scratch, which it
  probably does, since the formats are new
- what happens to the review already done on cards that survive

## 7. The link, mechanically

Every DSA card naming a problem links to `/library/problem/<slug>`. Unsettled:
does following the link count as answering? Does it pause the card, or abandon
it? A reader who taps through to read the problem and comes back should not have
lost their place, and nothing currently describes that.
