# The card catalogue

29 question archetypes, carried by 8 interaction primitives, stored as 3 answer
shapes. Nothing here is built.

Read [DECISIONS.md](DECISIONS.md) first for why any of it exists.

## Why three layers and not one list

A flat list of "20+ formats" would hide the thing that decides what this costs.
Matching and bucketing are the same interaction wearing different clothes;
complexity and which-approach are the same interaction as plain multiple choice.

So: **archetypes** are what a card asks, **primitives** are how you answer, and
**answer shapes** are what the database stores. You build eight UIs and three
columns, and get twenty-nine kinds of question.

## The 3 answer shapes

Everything a reader does reduces to one of these.

| shape | stores | used by |
|---|---|---|
| **Chosen set** | the ids they picked | pick one, pick many, tap in place |
| **Ordered list** | ids in their order | order |
| **Mapping** | left id → right id | match, bucket, word bank |

Match and bucket are the same shape: bucketing is matching where the right-hand
side has three entries and repeats.

## The 8 primitives

| # | primitive | how you answer | status |
|---|---|---|---|
| 1 | Pick one | tap an option | **exists** (`mcq`) |
| 2 | Pick many | tap several, submit | new |
| 3 | Order | tap-to-place (not drag — see DECISIONS risk 4) | new |
| 4 | Match | tap left, tap right | new |
| 5 | Bucket | tap item, tap column | new |
| 6 | Tap in place | tap a line or token inside a snippet | partly (`bug` exists as typed) |
| 7 | Word bank | tap words into gaps | new |
| 8 | Self-rate | "knew it / didn't" | **exists** (`flash`) |

## The 29 archetypes

Areas: **D**SA · **S**ystem design · **C**S fundamentals · **J**ava · **Q** SQL ·
**B**ehavioural.

### Pick one — 14

| archetype | tests | areas | example |
|---|---|---|---|
| Concept | a single fact or rule | all | *(the existing `mcq`)* |
| **Complexity** | the reflex an interviewer probes first | D J Q | "Time complexity of this loop?" |
| Which approach | choosing a technique under a constraint | D S Q | "n up to 1e5, must be O(n). Which pattern?" |
| What breaks first | failure reasoning under load | S | a design + stated traffic; pick the component that gives |
| Output prediction | reading code exactly | D J Q | convert the existing typed `output` to options |
| **Counter-example** | edge cases, the way they actually bite | D J Q | "Which input breaks this solution?" |
| Trace the value | following state through a loop | D J | "After the loop, what is `lo`?" |
| Failure diagnosis | debugging from a symptom | S C Q | "This query got slow. Most likely why?" |
| Threshold | when a rule stops applying | S C Q | "At what point does an index stop helping?" |
| Consequence of a diff | noticing what a small change does | D J C | two near-identical snippets; pick the effect |
| **Estimate** | back-of-envelope, which design rests on | S | "Storage for 1M users at 2KB each?" |
| Missing step | knowing a sequence well enough to spot a hole | S C Q | a protocol with one step removed |
| Next step | the same, forward | D S C | "Given these three steps, what comes next?" |
| Which invariant | correctness reasoning | D | "Which of these stays true through the loop?" |

### Pick many — 2

| archetype | tests | areas |
|---|---|---|
| All that apply | boundaries, not just the happy case | all |
| Odd one out | category understanding | all |

### Order — 3

| archetype | tests | areas |
|---|---|---|
| Sequence | protocols and algorithms as ordered things | S C D Q |
| Rank by a metric | relative cost, latency or complexity | D S Q |
| Timeline | when in a process something happens | S C |

### Match — 3

| archetype | tests | areas |
|---|---|---|
| Term ↔ meaning | terminology-dense areas | J Q C |
| Error ↔ cause | debugging vocabulary | J C S |
| Pattern ↔ signal | the cue that suggests a technique | D |

### Bucket — 2

| archetype | tests | areas |
|---|---|---|
| Two-way | a clean binary rule | S C Q |
| Three-way | a rule with a genuine middle | S Q |

### Tap in place — 2

| archetype | tests | areas |
|---|---|---|
| Tap the bug | debugging, on a phone | D J Q |
| Tap the bottleneck | reading a plan or a diagram | S Q |

### Word bank — 2

| archetype | tests | areas |
|---|---|---|
| Fill a code blank | precision without typing | D J Q |
| Fill a definition | exact wording where it matters | C J Q |

### Self-rate — 1

| archetype | tests | areas |
|---|---|---|
| Flash | "do I actually know this term" | all |

## The three worth building first

**Complexity**, **counter-example** and **estimate**. All three are pick-one, so
they need no new UI, and all three test reflexes an interviewer actually probes
rather than facts a lesson stated.

## Every DSA card that names a problem links to it

`/library/problem/<slug>` already exists. This is not a new feature, it is a
field on the card and an anchor in the UI, and it is what makes naming a problem
safe.
