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

---

# Round 2 — 2026-09-30

Seven things were open. Six are now settled, and one of Aman's answers changed the
architecture rather than just answering the question.

## The one that changed the design: no model in the loop

> "with these deterministic questions we are mostly going away from model in loop for feed
> except for text/short-text questions if left any. so do think in that direction."

Typed was the only Feed format that needed `gradeWithAi`. Kill typed in the Feed and there
are no text answers left, so **every Feed answer is marked by a pure function.** What that
buys, in order of how much it matters:

- **The same answer always gets the same mark.** A model grader can disagree with itself
  between two readers who typed the same thing, and nobody ever finds out.
- **It is testable in Vitest** rather than observable only in production.
- No cost and no latency at answer time.

This becomes the admission test for every archetype — see CATALOGUE.md, round 2. An
archetype a pure function cannot mark is not a Feed card; it may still be a good mock
question.

`gradeWithAi` stays in the codebase for the mock and review paths. It leaves the Feed.

## Distractor quality — a blind-answer gate, plus structural rules

Before a card ships, the pipeline shows a model **only the options** — no lesson, no topic,
no area — and asks it to answer. If it picks the right one, the card was guessable and gets
rewritten. Roughly $1 across the corpus, judging by what `card-regate` cost.

Plus structural rules, which are free and catch the most common giveaway, elimination by
shape: options within a length band, no option that is the only one of its kind, no "all of
the above".

**This is a pipeline check and changes nothing the reader sees.** In particular the detailed
explanation after an answer — `answerMd` and the key points — stays exactly as it is. The new
formats need it more, not less: "why was this the right *order*" is less self-evident than
"why was this the right option".

## Format assignment — a per-topic budget, filled one card at a time

The pipeline decides a topic's mix before writing anything, then asks the writer for one
named format per call. **The writer never chooses**, because asked for "a card" it returns
multiple choice every time.

A writer may **refuse**: a topic with no natural sequence says so, and the budget refills
with another format. A strained ordering card is worse than an absent one.

## Partial credit — none. A card is right or wrong

Four of five pairs matched is wrong. An ordering with two items swapped is wrong.

The reason is downstream: FSRS schedules on a right/wrong signal and readiness moves on it.
A score would mean every consumer of an answer has to learn what a partial mark means, and
the dial's meaning would shift under it. The outcome vocabulary
(`correct | wrong | skipped | new_to_me | known`) does not change.

It costs some fairness on the harder formats, and a five-pair match marked all-or-nothing may
read as harsh. Accepted.

## Two valid answers — the card declares its constraints

Following the deterministic direction: an ordering card stores **the constraints it claims**,
not one blessed sequence. `parse < plan`, `plan < execute`, cache-warm independent. The
grader asks whether the reader's order satisfies them, so every genuinely correct order is
accepted. Matching gets the mirror rule: a strict one-to-one mapping, checked at write time.

A card whose writer cannot state constraints that make exactly one answer *class* correct is
rejected. The ambiguity is declared rather than discovered by a reader being marked wrong for
an answer that was fine.

## Regeneration — fresh from the lesson, to the budget

The 1,383 typed cards are **retired, not deleted**, and new cards are written from the lesson
in whatever format the budget asks for. Converting a typed prompt carries the shape of having
been typed into a format that does not suit it.

Cost: card generation was ~$4.70 for 2,808 cards, so roughly **$2.30** for this share, plus
~$1 for the blind gate. The human review sample is redone from scratch — the old objections
name prompts that will no longer exist.

## Behavioural — unchanged

> "we can keep them as is and anyways they can be deselected if someone doesnt need them"

Right: `feedAreas` already lets a reader turn it off, so a thin area costs only the people who
want it. No behavioural cards are generated in the new formats and none are retired.

## Scope — all eight primitives in the first build

Aman asked for everything, and the catalogue grew to 44 archetypes to match. The count is
affordable because **archetypes are prompts and grading rules; the UI cost is the 8
primitives**, and that number does not move whether there are 29 archetypes or 44.

## Two things decided here rather than asked

**Tap-to-place, never drag.** Ordering, matching and bucketing all suggest drag-and-drop, and
drag inside a scrolling page on a phone fights the scroll. Tap the item, tap where it goes —
same data model, better on the device, and it is keyboard- and screen-reader-reachable, which
drag is not without real work.

**Following a problem link does not consume the card.** It is not an answer and not a skip.
This needs no new mechanism: `nextCard` already serves `90x:feed:<uid>:current` before the
queue, so a reader who taps through to a problem and comes back is served the same card. The
only requirement is that the Feed does not clear `currentKey` on navigation — worth a test,
since nothing states it today.

## Six more primitives — 14 over 5 answer shapes

Aman asked for the two raised in round 2 plus anything else interesting. Six went in;
three were turned down. The walkthrough is PRIMITIVES.md; the reasoning that matters:

**The primitive count is not the cost. The answer-shape count is.** A shape is understood by
the grader, the stored attempt and every consumer of an answer. A primitive is one screen.
Four of the six reuse an existing shape and so add no new grading concept — claim grid and
grid toggle are a mapping and a chosen set, assemble is an ordered list, pick-then-justify is
two chosen sets. Only **numeric entry** (a number) and **highlight a span** (start, end) widen
the contract, from three shapes to five.

Two of them do something nothing else in the catalogue can:

- **Claim grid** forces a judgement on every statement. Pick-many lets a reader quietly skip
  the options they are unsure of; a true/false grid does not, which is how half-knowledge stops
  hiding.
- **Pick, then justify** is the only primitive that detects being right by accident. Four
  options means 25% from knowing nothing; requiring the reason takes that to 6%, and "right
  answer, wrong reason" is the most useful thing a card can report.

**Numeric entry is typing, and typing is what we removed from the Feed.** The distinction held
here: a keypad is three taps with nothing to phrase and no model to mark it, where a typed
answer was prose that cost money to grade. If it still feels like work when it exists, it is
the first thing to drop.

Turned down: **connect the edges** (good on a desktop, miserable at 390px), **stepwise
simulation** (several cards pretending to be one, which breaks one question/one mark), and a
**slider** (numeric entry with a worse input, and drag fights the page scroll for the same
reason ordering is tap-to-place).

---

# Round 3 — "too easy", and difficulty as a real thing

A reviewer said the current Feed is too easy: the questions they saw did not make them think.
Measured before arguing, and the measurement changed the conclusion.

## What the database says

```
attempts, all time:  4 wrong · 3 skipped  (7 total)
live cards: 129      typed 66 · flash 32 · mcq 29 · output 2
```

**"Too easy" cannot be a usage claim — there are seven attempts in the whole database.** It is
a judgement from reading the cards, and read that way it is right, for reasons nobody had
named:

- **A quarter of the live Feed is flashcards**, 28 of 32 labelled Easy, and flash is
  self-rated: there is no wrong answer. Take out the 66 typed cards that are leaving and the
  part of the live Feed that actually tests anybody is 29 multiple-choice cards.
- **A four-option card has a 25% floor** and nothing notices a reader riding it.
- **`cards.difficulty` is a text label the writer assigned itself**, never checked against
  whether anyone got the card wrong. An opinion stored as data, with no loop closing it.

## The finding that matters: the hard cards are the typed ones

```
Hard:    typed 20 · mcq 5 · output 0 · flash 0
Medium:  typed 44 · mcq 13 · output 1 · flash 4
Easy:    typed  2 · mcq 11 · output 1 · flash 28
```

**25 of the 26 Hard cards are typed**, and typed is the format Feed v2 removes. Done naively,
this redesign would delete almost all the hard content and leave a Feed of 11 Easy multiple
choice and 28 Easy flashcards — making the complaint it was meant to answer worse.

So difficulty is not a polish item to handle after the formats. It is a constraint on the
regeneration.

## Difficulty gets a rubric now and calibration later

Aman chose both, and they fit together: the rubric gives an immediate, consistent estimate,
and observed outcomes correct it once there is volume to correct it with.

**The rubric**, applied by the pipeline at write time, against stated criteria rather than
vibes:

| | Easy | Medium | Hard |
|---|---|---|---|
| reasoning steps | 1 | 2 | 3+ |
| a stated constraint changes the answer | no | sometimes | yes |
| spans more than one fact | no | no | yes |
| distractors encode real misconceptions | not required | yes | yes |
| needs a calculation | no | maybe | yes |

**The calibration**, once a card has enough attempts: above 85% correct it is Easy whatever the
writer thought, and it gets flagged for review; below 25% it is probably broken or ambiguous
rather than hard, and gets flagged too. Selection uses the observed rate once n ≥ 20 and the
rubric until then. With 7 attempts in the database this job does nothing on day one, which is
fine — it is the loop that has been missing, not the number.

## Two levers, because neither exists today

1. **Generate for difficulty.** The per-topic budget carries a difficulty target, not only a
   format mix. Without it regeneration reproduces whatever the writer finds easiest to write,
   which is Easy.
2. **Select for difficulty.** Nothing in the Feed picks by difficulty; it serves what FSRS
   surfaces. A session wants a deliberate mix.

And **cap flash**. It is the cheapest single fix: a Feed that is a quarter self-rated cards
feels like review because it is.

## The three empty primitives are filled

Numeric entry, grid toggle and pick-then-justify had no archetypes — screens with nothing to
render.

- **Estimate, Complexity, Impossible bound and Trace the value move to numeric entry**, where
  a keypad tests calculation instead of elimination. They stay available as pick-one too: same
  archetype, two primitives, and the pipeline picks.
- **Grid toggle gets three new archetypes**: the complexity table, SQL isolation behaviour,
  HTTP method semantics. All three are two-dimensional facts that bucketing flattens.
- **Pick-then-justify is a modifier, not an archetype.** Any card may carry a why-step. That is
  the cleaner framing and it means ordering and matching get "right answer, wrong reason" free.

**47 archetypes** over 11 primitives and 4 answer shapes.

---

# Round 4 — everything else, settled

Twelve questions, twelve answers. Typed is gone entirely; the Feed is 47 archetypes over 11
primitives, and the whole corpus is rewritten.

## The corpus

- **All 2,808 cards are replaced**, including the batch Aman approved on 2026-09-28. That
  approval was of cards written with no format budget, no difficulty rubric and no blind gate;
  keeping them would leave a corpus where nothing in the data distinguishes a vetted card from
  an unvetted one, so every future quality question would have to be asked twice.
- **Size is weighted by `topics.importance`**, not flat. Popular topics carry more cards than
  obscure ones, landing near **3,000**.
- **"Equally distributed" means equal within each area's eligible archetypes**, per
  CATALOGUE.md's areas column. No Estimate card for a Java syntax topic; equal is measured per
  area, not globally.
- **Hard content may be written from problem statements and pattern tricks**, not only the
  lesson. A three-step question needs a concrete situation, and we hold 3,693 problem
  statements; a lesson's four claims usually cannot support one. This widens which sources
  count, exactly as the lesson rebuild did — it does not weaken the sourcing rule.

## Difficulty

- **Rubric at write time** (round 3 table), **calibrated from outcomes** at n >= 20.
- **A session adapts to the reader's rolling accuracy**, targeting roughly 70-85% correct, with
  `profiles.level` as the starting point.
- **Plus a reader-facing difficulty toggle that shifts the mix, never filters it.** Choosing
  "harder" raises the share of Hard in the pool; it does not remove Easy cards, and it does not
  touch FSRS scheduling.
- **A why-step on every Hard card.** That takes a Hard card's guess floor from 25% to about 6%,
  and "right answer, wrong reason" is the most useful thing a card can report.

## The gates

- **Blind gate: three samples, reject at two or more correct.** One attempt would reject a
  quarter of good cards by luck alone. Three brings a false reject to ~16%, and a false reject
  only costs a rewrite. ~$3 corpus-wide. **Validate on 50 cards before spending the rest** — if
  the rejection rate comes back implausible, the gate is wrong, not the corpus.
- **Human review: two cards per archetype, ~94, once.** The question per card is not "is this
  correct" — the gates answer that — it is **"does this archetype earn a place"**. Afterwards a
  ~15-card spot check per batch, plus everything the gates flagged.

## Schema and rollout

- `cards.format` becomes **the primitive**, and **archetype is a separate field**. `typed` is
  gone; `output` becomes the Output prediction archetype on pick one; `bug` becomes Tap the bug
  on tap-in-place, which is what it always wanted to be and could not be as a typed answer.
- `cards.status` gains **`retired`**. That is a migration, so the lead writes it.
- **FSRS history is kept, orphaned on retired cards.** Not scheduled, still readable. Deleting
  it would make everybody's readiness dial drop on release day with no explanation, and it is
  the only record of what people have actually practised.
- **One release, not a flag** — with the sequencing made safe: new cards publish as `draft`
  (invisible), the code deploys, and then a single statement flips new to `live` and old to
  `retired`. The corpus cannot be rendered by code that does not exist yet, which is the
  mistake that took production down on 2026-09-29.
- **Parameterised cards: not now.** A stored card is a fact with an answer; a parameterised one
  is a generator plus a solver, and it breaks FSRS's assumption that a card is a stable thing
  being remembered. Revisit if repeats actually become the complaint.

## One consequence worth stating, because it follows rather than being chosen

**A Hard card answered correctly with the wrong reason is marked wrong.** That falls out of no
partial credit plus a required why-step, and the alternative — scoring the answer and ignoring
the reason — would make the why-step decorative.

It is the harshest rule in the design. It is also the one most likely to be wrong in practice,
so it is the first thing to look at in the ~94-card review: if the wrong reasons are not
genuinely plausible, this rule punishes readers for a writing failure rather than a knowledge
gap.

## Money

| step | estimate |
|---|---|
| generate ~3,000 cards in structured formats | ~$5-7 |
| blind gate, three samples | ~$3 |
| difficulty rubric pass | ~$1 |
| repair pass for rejects | ~$1 |
| **total** | **~$10-12** |

Against $20 newly available. The one number that could move is generation: structured formats
carry more fields than a prose answer, so a card may cost more than the ~$0.0017 the original
pass averaged. **Measure on one topic before running 274.**

## Model tiers and thinking

Thinking is a per-step choice, not a global switch. DeepSeek thinks by default and bills the
reasoning tokens as output; `llm.complete_json(..., thinking=…)` turns it on or off per call, and
each step states its choice rather than inheriting a default.

| step | tier | thinking | why |
|---|---|---|---|
| card writer | smart | **off** | measured 2026-09-30: thinking on gave the same blind-gate rejection at ~4.7x the cost (see below). |
| blind gate | fast | **off** | correctness, not cost. A model reasoning for thousands of tokens is a far stronger guesser than a reader skimming four options on a phone; with thinking on it becomes a false-positive machine, and every false rejection costs a smart repair pass. |
| difficulty rubric | — (pure code) | off | classification against stated criteria; it makes no model call at all. |
| answerability gate | smart | off | classification against stated criteria. |
| repair pass | smart | **on** | it is diagnosing *why* a card failed. |

The writer on/off question is settled: on `arrays-hashing`, thinking on and off produced the same
blind-gate rejection (55% each, gate on smart with thinking off), while thinking on cost ~4.7x per
card ($0.0135 vs $0.0029, both off-peak) and ~17x the wall-clock. Thinking on does not write better
distractors and does not earn back its tokens in avoided repair passes — the writer stays off.

The one that matters is the blind gate. It reads like a cost-saving, so the next person who
touches it may be tempted to turn thinking on to make it "better". Do not: a stronger guesser
is a false-positive machine, and every false rejection it produces spends a smart repair pass to
fix a card that was never broken. Leave the blind gate's thinking off, on purpose.

---

# Round 5 — the run, settled (2026-10-01)

Operational decisions for the generation run, after the first Gate 2 measurements came back.
The gate measured **62% rejection** on 50 cards, found the per-topic budget was skewing to
`pick_one` (fixed, #55), and found the why-step wrong-reasons were LLM straw men (fixed, #56,
which brought rejection to **46%**). A follow-up pass is tightening `match`/`numeric` why-step
scoping and answer-consistency.

## Go-ahead is manual

The full run never starts on a threshold. I report the final Gate 2 number plus a costed plan
(card count, estimated cost, ETA), and Aman approves explicitly. No auto-proceed.

## The full run waits for off-hours

Generation runs in the off-peak price window, not at peak. And the cards already generated
during the Gate 2 / re-measure runs are **real corpus cards** — they are kept and published, not
discarded as test data.

## A floor on the corpus

Repair-once-then-drop will shrink the ~2,900. If the final count would fall below **~2,500**,
stop and check before shrinking further.

## The swap is prepared, not executed here

Build and verify the draft → live → retired mechanics, run a staging dry-run, and write the
production runbook — then stop. The production migration and the final publish are Aman's.

## Gate 3 in two forms

The ~94-card human review ships as both the web review pack and a markdown file.

---

# Round 6 — the blind gate and Gemini, settled (2026-10-01)

Measurement forced two corrections after the first Gate 2 numbers.

## The blind gate was false-rejecting "known", not "guessable"

The blind gate showed a model only the options and rejected when it answered correctly. After
the distractor and shape-leak fixes (62% → 46% → 51% on the old gate), the remaining rejection
turned out to be **false rejects**: fundamental-topics cards ("primary purpose of an index",
"B-tree is O(log n)") that a *knowledgeable* model answers trivially but a *learner* — the
actual Feed reader — does not. Left alone, repair-then-drop would have discarded ~half the
corpus, far below the ~2,500 floor.

**Decided: the gate rejects "guessable by elimination/structure", not "a knowledgeable model
answers it".** Its prompt now rules on *can a reader with no knowledge of the topic get this
right by eliminating options*. Result: **~9%** rejection (was 51%), and the rejects are all
structural tells ("items already in the correct order", "one option qualitatively different").
19 of the 22 cards the old gate rejected are now correctly let through.

## Gemini stays out of card generation

A 10-card spike plus a 20-card reviewer run, all off-peak:

- **Writer** — par. Gemini's cards were less guessable (30% vs 46%) but that is one noisy topic,
  ~28% dearer, and it emits U+FFFD in math notation. Not worth switching.
- **Blind gate** — Gemini agrees 9/10 with DeepSeek but costs ~4.7× (it emits hidden thought
  tokens even at `reasoning_effort=none`). Keep DeepSeek.
- **Independent reviewer (Gemini)** — flagged 0/20 errors `gate.py` missed. No value for Feed
  cards (the lessons they are built from were already independently reviewed at the lesson
  stage). Not wired into the card path.

**Decided: generation stays all DeepSeek; no independent-reviewer step in the Feed v2 card flow.**
The blind gate plus the deterministic shape rules are doing that job.
