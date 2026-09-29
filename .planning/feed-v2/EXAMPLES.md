# One example per archetype

Sketches, to make the catalogue concrete — **not generated cards**. Real cards come from
lessons and problem statements we hold, per the sourcing rule. These are here so a reader of
CATALOGUE.md can tell two archetypes apart.

Grouped by primitive, so the UI cost is visible: everything in a section shares one screen.

## Pick one — 14

| archetype | prompt | answer |
|---|---|---|
| Concept | A cache-aside read misses. What happens next? | The app reads the store, writes the cache, returns the value |
| Complexity | `for (i=0;i<n;i++) for (j=i;j<n;j++)` — time? | O(n²) |
| Which approach | n ≤ 1e5, find any pair summing to k, must be O(n). Which? | A hash set of seen values |
| What breaks first | 3 app servers, one Postgres primary, 50k writes/s | The primary's write throughput |
| Output prediction | `System.out.println(0.1 + 0.2 == 0.3);` | `false` |
| Counter-example | Which input breaks this two-pointer sum on an *unsorted* array? | `[3,1,2]`, target 5 |
| Trace the value | Binary search over `[1,3,5,7]` for 6. What is `lo` when the loop ends? | 3 |
| Failure diagnosis | A query was fast; 10× the rows and the index is now unused. Why? | The predicate wraps the column in a function |
| Threshold | At what point does a B-tree index stop helping a range scan? | When it matches a large share of the table |
| Consequence of a diff | Two snippets differing only by `<` and `<=` | The loop never terminates on equal bounds |
| Estimate | 1M users, 2KB of profile each. Storage? | ~2 GB |
| Missing step | A TCP handshake listed with one step removed | SYN-ACK |
| Next step | Client sends SYN, server replies SYN-ACK. Then? | The client ACKs |
| Which invariant | In binary search, which statement stays true every iteration? | If the target exists, it lies within `[lo, hi]` |

## Pick many — 2

| archetype | prompt | answer |
|---|---|---|
| All that apply | Which are true of a hash map at load factor 0.9? | Collisions are frequent · lookups degrade toward O(n) |
| Odd one out | quicksort · mergesort · heapsort · counting sort | Counting sort — the only one not comparison-based |

## Order — 3

| archetype | prompt | answer |
|---|---|---|
| Sequence | Put the steps of a TLS handshake in order | ClientHello → ServerHello → certificate → key exchange → Finished |
| Rank by a metric | Rank by growth: O(n log n) · O(log n) · O(n²) · O(n) | log n → n → n log n → n² |
| Timeline | When is the browser cache consulted, among DNS, TCP and TLS? | Before DNS |

## Match — 3

| archetype | prompt | answer |
|---|---|---|
| Term ↔ meaning | Match A, C, I, D to their meanings | Atomicity ↔ all-or-nothing, and so on |
| Error ↔ cause | Match each Java exception to what causes it | `ConcurrentModificationException` ↔ mutating a collection while iterating it |
| Pattern ↔ signal | Match each problem cue to the technique it suggests | "sorted array, find a pair" ↔ two pointers |

## Bucket — 2

| archetype | prompt | answer |
|---|---|---|
| Two-way | Sort these SQL functions: deterministic or not | `upper()` deterministic · `now()` not |
| Three-way | Sort these HTTP codes: redirect · client error · server error | 301 · 404 · 503 |

## Tap in place — 2

| archetype | prompt | answer |
|---|---|---|
| Tap the bug | A loop written `i <= arr.length`. Tap the line that is wrong. | that line |
| Tap the bottleneck | An EXPLAIN plan. Tap the line costing the most. | the `Seq Scan` |

## Word bank — 2

| archetype | prompt | answer |
|---|---|---|
| Fill a code blank | `Map<String, ___> counts = new HashMap<>();` | `Integer` |
| Fill a definition | A ___ index stores keys in sorted order and supports range scans. | B-tree |

## Self-rate — 1

| archetype | prompt | answer |
|---|---|---|
| Flash | Idempotency | knew it / didn't |

## What this shows

Fourteen pick-one archetypes are **fourteen different questions on one screen**. That is the
argument for counting archetypes separately from primitives: the reader meets variety, the
build does not pay for it.

It also shows where the primitives strain. *Estimate* as four options is weaker than a number
pad would be, and *Rank by a metric* is an ordering whose answer is a fact rather than a
judgement — both are the strongest arguments for the two extra primitives raised in round 2.
