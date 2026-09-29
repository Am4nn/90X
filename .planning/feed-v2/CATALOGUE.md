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

## The 8 primitives (round 1 — 6 more in PRIMITIVES.md, for 14)

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

## The 29 archetypes (round 1 — 15 more in round 2, below)

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

### Pick many — 2 — **rehomed, see PRIMITIVES.md final set**

Pick many was cut. *All that apply* becomes a **claim grid** (a forced true/false on every
row, instead of letting the reader skip the ones they are unsure of). *Odd one out* is a
**pick one** — it always was, one item selected. Both archetypes survive; neither loses
anything.

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

### Word bank — 2 — **now templated Assemble cards**

Word bank merged into Assemble: one primitive, one grading function, with the template
carrying the difficulty. A mostly-filled template is a word bank; an empty one is an
assemble. Both archetypes stay.

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

---

## Round 2 — the bar, and 15 more

### The bar every archetype now has to clear

Typed was the only Feed format that needed a model to mark it. With typed gone from the
Feed, **every Feed answer is graded by a pure function**: no model call at answer time, no
cost, no latency, no variance between two readers who gave the same answer — and the whole
grader becomes testable in Vitest instead of observable only in production.

That is worth protecting, so it is the admission test for any new archetype:

1. **A pure function can mark it.** If marking needs judgement, it is not a Feed card. It
   may still be a good mock question or a Coach exchange.
2. **Exactly one answer class is correct**, and the card declares what makes it so — for
   ordering, the constraints; for matching, a one-to-one mapping. Not "the writer's favourite
   sequence".
3. **The content exists in what we hold.** A lesson, a problem statement, a trick, an
   EXPLAIN plan. No archetype that can only be filled by a model inventing material.
4. **It tests something the others do not.** Two archetypes with the same primitive and the
   same skill are one archetype with two prompts.

Rule 1 is what makes the count cheap. Archetypes are prompts and grading rules; **the UI
cost is the 8 primitives, and that number does not move.** 44 archetypes cost the same to
build as 29.

### Pick one — 5 more (19 total)

| archetype | tests | areas | why a pure function can mark it |
|---|---|---|---|
| Which is not true | holding four claims at once, not recognising one | all | one option is flagged false at write time |
| Which test catches it | testing sense, which interviews probe and nobody practises | D J Q | the failing test is known when the bug is written |
| Read the query plan | the skill SQL interviews actually test | Q | we hold real EXPLAIN output; the problem in it is a fact |
| Error → cause | the vocabulary of debugging, from a real message | J Q C | the message came from a known cause |
| Impossible bound | knowing what no algorithm can do, not just what one does | D | a stated lower bound is a fact about the problem |

### Pick many — 1 more, now a claim grid

| archetype | tests | areas | why a pure function can mark it |
|---|---|---|---|
| Which invariants hold | correctness reasoning at loop level | D C | each claim is true or false of the given loop |

### Order — 2 more (5 total)

| archetype | tests | areas | why a pure function can mark it |
|---|---|---|---|
| Dependency order | partial order — migrations, builds, deploys | S C Q | the constraints are the answer; several orders pass |
| Interleaving | the concurrency bug you cannot see by reading one thread | C J | one interleaving produces the stated symptom |

### Match — 2 more (5 total)

| archetype | tests | areas | why a pure function can mark it |
|---|---|---|---|
| Operation ↔ complexity | the table every DSA interview assumes you know | D J | a one-to-one mapping of facts |
| API ↔ guarantee | what a primitive actually promises | S | each promise belongs to one primitive |

### Bucket — 1 more (3 total)

| archetype | tests | areas | why a pure function can mark it |
|---|---|---|---|
| Which layer | where a concern belongs: client, edge, app, store | S | each item has one home under the stated rule |

### Tap in place — 2 more (4 total)

| archetype | tests | areas | why a pure function can mark it |
|---|---|---|---|
| Tap the insertion point | knowing where a missing line goes, not just that one is missing | D J Q | the line was removed from a known position |
| Tap the unsafe line | injection and concurrency risks, where they live | J Q S | the unsafe line is the one that was planted |

### Word bank — 2 more, now templated Assemble cards

| archetype | tests | areas | why a pure function can mark it |
|---|---|---|---|
| Fill the signature | Java precision without typing | J | the signature is in the source |
| Fill the clause | SQL precision without typing | Q | the clause is in the source |

### Where that leaves us

**44 archetypes over the same 8 primitives and 3 answer shapes.** Self-rate stays at 1,
because "do I know this term" has one shape.

The count is not the goal and it is not a target to keep raising. Two things make it worth
having: a reader who meets a different *kind* of question keeps paying attention, and a
topic whose budget can be filled from nineteen pick-one archetypes is far less likely to get
four near-identical cards. Anything that cannot clear the four rules above does not go in,
however good it sounds in a list.

---

## Round 3 additions — grid toggle gets its archetypes

| archetype | tests | areas | why a pure function can mark it |
|---|---|---|---|
| Complexity table | the table every DSA interview assumes you know | D J | each cell is a fact |
| Isolation behaviour | which anomaly each isolation level permits | Q | defined by the standard |
| Method semantics | safe, idempotent, cacheable, per HTTP method | S | defined by the spec |

**Moved to numeric entry** (still available as pick one — same archetype, two primitives):
Estimate, Complexity, Impossible bound, Trace the value. A keypad tests the calculation; four
options test elimination.

**Pick-then-justify is a modifier, not an archetype.** Any card may carry a why-step, which
gives ordering and matching "right answer, wrong reason" for free.

**47 archetypes, 11 primitives, 4 answer shapes.**
