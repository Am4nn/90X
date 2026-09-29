# What is wrong with the Feed, and what we decided

2026-09-29. A discussion round, not a build order.

## What Aman said

> "Typing a asnwer doesnt really work - no one will use that mcq is fine but
> typing is really boring and dsa questions still assume I know a quesiton
> name ?"

Two complaints, and the second turned out to be the more interesting one.

## The first: typing is the wrong ask

The Feed is quick reps, often on a phone, often in a gap between other things.
Typing a paragraph there is work, and work is what the Feed exists to make
frictionless. Nobody types the answer; they skip.

Measured, this is not a minor format problem:

| | |
|---|---|
| Typed cards | **1,383 of 2,808** — 49% of the corpus |
| Cost to grade | every typed answer is a model call; every other format is free |

So half the Feed is a format that will not be used, and it is precisely the
expensive half.

**Decided: typed dies in the Feed only.** Mocks and the Coach keep it, because
there you have sat down on purpose and a paragraph is the point. This is a
statement about the *moment*, not about typing.

## The second: named problems were treated as a defect, and are not

A card reading "In Two Sum, why does a hash map beat sorting?" is useless if you
have never seen Two Sum. The obvious fix is to stop naming problems.

Aman rejected that:

> "Yes and can have named problems but be smart about it like have a link to the
> problem so they can read about it even solve it"

Which is better than the obvious fix. **A named problem is only a dead end
because the card gives you nowhere to go.** `/library/problem/<slug>` already
exists. With a link, "I don't know this one" becomes a doorway rather than a
wall, and the card has taught you something either way.

**Decided: DSA stays in the Feed, problems keep their names, and every card that
names one links to it.**

A hypothesis was floated and rejected in passing, worth recording because it
sounds plausible and is wrong for this app: that DSA is procedural, cannot be
tested by recall, and should live only in the problem/check-in loop. Aman's
answer is that the Feed can carry DSA as long as it routes you to the problem
rather than assuming you have done it.

## The third thing, which Aman asked for rather than agreed to

> "I think we can have a lot more types of quesitons - mcq, match things,
> ordering things, fill in the blanks and even more you come with full catelog
> of thigns we can have and hence making the feed intersting"

The Feed being *interesting* is a goal in its own right, separate from being
correct. One format is monotonous however good each card is.

**Decided: the full catalogue in [CATALOGUE.md](CATALOGUE.md).** 29 archetypes
over 8 interaction primitives. The distinction matters: "20+ formats" as a flat
list would mean building the same drag interaction five times. Eight UIs carry
twenty-nine kinds of question.

## What follows from all of it

- **Grading becomes deterministic.** Every archetype in the catalogue is checked
  against a stored answer. No model call per answer, so the Feed's running cost
  goes to zero and `check:grading` retires.
- **The 1,383 typed cards get regenerated** into the new formats. Decided over
  the alternatives of retiring them, or leaving them unserved. Costs a pipeline
  run; keeps the coverage.
- **The gate needs rules per archetype.** An ordering card with two valid orders
  is as broken as a typed card with no key points, and the current gate would
  not notice either.

## Four risks raised, none settled

Recorded here so they are not rediscovered, and expanded in
[OPEN-QUESTIONS.md](OPEN-QUESTIONS.md):

1. **Distractor quality is the whole game.** A pick-one card is only as good as
   its wrong answers. Three implausible options and you eliminate by shape
   rather than by thinking. It is invisible: the card reads well beside its
   lesson and is trivial in the Feed.
2. **Format balance will not happen on its own.** Ask a model for a card and you
   get multiple choice, every time. Without something assigning the format, the
   database ends up 85% MCQ with 29 formats in the schema.
3. **Not every archetype fits every area.** Estimate suits system design and is
   meaningless for Java syntax. Ordering suits protocols, not behavioural.
4. **Drag is bad on a phone.** Ordering, matching and bucketing all suggest
   drag-and-drop, which fights the scroll. Tap-to-place is the same data model
   and much better on the device this is actually used on.
