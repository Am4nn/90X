# Sample card data, one short and one long per primitive

For populating a design. 22 cards: each of the 11 primitives twice, once at the short
end of what the corpus produces and once at the long end. Companion to
`CARD-DATA-BRIEF.md`, which says what each primitive is. This file is the content.

Archetype names are the registry's own (`archetypes.json`). Topic names and the wording
of questions are illustrative. Everything here is written to the limits the pipeline enforces, and the result wording
is the app's real copy, so a design built from it will not meet a longer string or a
bigger grid in production than it has already seen.

## How to read a card

```
Topic · Difficulty · Archetype            who it is and how hard
Served because                            the "Why this card" line
Prompt                                    markdown; code appears in fences
Content                                   what the primitive puts on screen
Correct                                   the answer key (hidden until answered)
A wrong answer                            a realistic miss, to design the marked-up state
Answer text                               the written answer shown after
Key points                                shown after answering, where a card has them
Source                                    a pill linking to the lesson it came from
```

Option order below is the order **stored on the card**, which is the order the reader
sees. Correct answers are not first.

## Rules that apply to every card (read these before the cards)

1. **Grading is all-or-nothing.** Every primitive except `compose` scores 0 or 100%.
   `pick_one`, `tap_in_place` and `grid_toggle` need the exact set. `match`, `bucket`
   and `claim_grid` need every pair right. One wrong pair is a wrong card. There is
   no "3 of 4".
2. **`compose` is the only fractional score**, marked by a model against the rubric,
   passing at 70%. The result reads "N of M key points" with each point ticked or
   crossed.
3. **`order` accepts every order the rules allow.** Two steps with no rule between
   them may come either way round, and neither is wrong. See card 3b.
4. **A correct answer with the wrong reason is wrong.** Hard cards can carry a
   second question, the why-step. See card 1b.

---

## 1. pick_one

### 1a. Short

```
SQL · Transactions & ACID  ·  Easy  ·  Concept
Served because: New card on Transactions & ACID.

Prompt
  Which ACID property guarantees a transaction's writes are all applied or none are?

Content (4 options, stored order)
  Durability
  Atomicity
  Isolation
  Consistency

Correct:        Atomicity
A wrong answer: Durability
Answer text:    Atomicity means all-or-nothing: if any part of the transaction fails,
                every change is rolled back. Durability is a different promise: once
                committed, a write survives a crash.
Source:         Transactions & ACID
```

### 1b. Long, with a why-step

```
System design · Caching  ·  Hard  ·  Which approach
Served because: Caching is one of your weak spots. Another go should help it stick.

Prompt
  A read-heavy product catalogue sits behind a Redis cache in front of Postgres. A
  back-office tool updates one product's price while a flash sale drives 20,000
  reads per second for that same product. Readers must never see a price older
  than the one just saved, and the database must not be flooded when the entry is
  refreshed. Which approach meets both requirements?

Content (4 options, stored order)
  Write the new price to Postgres, then delete the cache key and let each reader
  that misses query the database and repopulate it
  Set a 60 second TTL on the key and let it expire naturally after the update
  Write the new price to Postgres, then overwrite the cache key with the new value
  in the same code path, keeping a short TTL as a safety net
  Write the price to the cache only and flush it to Postgres in a nightly batch

Correct:        the third option
A wrong answer: the first option

WHY-STEP, asked only after a correct main answer. A separate question, its own
options, labelled "Reason 1" to "Reason 4" so it cannot be confused with the letters
above.
  Why is the first option a poor fit here?
  Reason 1  Deleting the key makes every concurrent reader miss at once and hit
            Postgres together, a cache stampede
  Reason 2  Redis cannot delete a key while it is being read
  Reason 3  A deleted key is always repopulated with the old price
  Reason 4  Deletes are slower than overwrites in Redis
  Correct reason: Reason 1

If the reader picks the third option and then Reason 3, the card is marked wrong.

Answer text:    Overwriting in place keeps the entry hot, so there is no moment when
                20,000 readers all miss. Deleting the key invites a stampede.
Key points:     - Update the cache in the same path as the write
                - A hot key must never be empty under load
                - A TTL is a safety net, not the consistency mechanism
Source:         Caching
```

---

## 2. match

### 2a. Short

```
CS · HTTP  ·  Easy  ·  Term meaning
Served because: Due for review: you've seen this card before and it's time to recall it again.

Prompt
  Pair each HTTP status code with its meaning.

Content: 4 terms on the left, 4 meanings on the right (stored order)
  Left:   301      401                404         503
  Right:  Not found | Service unavailable | Moved permanently | Not authenticated

Correct pairs:  301 → Moved permanently    401 → Not authenticated
                404 → Not found            503 → Service unavailable
A wrong answer: 401 → Not found, 404 → Not authenticated (two swapped)
Answer text:    401 means the request lacks valid credentials; 404 means the server
                has no such resource.
```

### 2b. Long, 5 pairs, sentence-length meanings

```
SQL · Index types  ·  Medium  ·  Term meaning
Served because: New card on Index types.

Prompt
  Pair each kind of index with the description of what it does to the data.

Content: 5 terms, 5 meanings (stored order)
  Left:
    Clustered index
    Non-clustered index
    Covering index
    Composite index
    Partial index
  Right:
    Contains every column a query needs, so the query is answered without touching
    the table at all
    Built over several columns, so how useful it is depends on the order of those
    columns in the key
    Stores the table's rows in the index's own key order, so there can be only one
    per table
    Indexes only the rows matching a predicate, keeping it small when most rows are
    never queried
    A separate structure of keys and row pointers, so a lookup costs an extra hop to
    fetch the row

Correct pairs:  Clustered → "Stores the table's rows…"
                Non-clustered → "A separate structure of keys and row pointers…"
                Covering → "Contains every column a query needs…"
                Composite → "Built over several columns…"
                Partial → "Indexes only the rows matching a predicate…"
A wrong answer: Clustered ↔ Non-clustered swapped, the rest right
Source:         Index types
```

---

## 3. order

### 3a. Short, one valid order

```
CS · TCP  ·  Easy  ·  Sequence
Served because: New card on TCP.

Prompt
  Put the steps of a TCP connection in order.

Content: 5 steps (stored order)
  Data transfer
  FIN
  SYN
  ACK
  SYN-ACK

Rules:          SYN before SYN-ACK before ACK before Data transfer before FIN
                (one valid order)
A wrong answer: SYN, ACK, SYN-ACK, Data transfer, FIN
Answer text:    The three-way handshake is SYN, SYN-ACK, ACK. Data flows only once it
                completes, and FIN closes the connection.
```

### 3b. Long, several valid orders (the special case)

```
System design · Write-ahead logging  ·  Hard  ·  Sequence
Served because: Write-ahead logging is one of your weak spots. Another go should help it stick.

Prompt
  A database commits a transaction under write-ahead logging. Put these five steps
  into an order the protocol permits.

Content: 5 steps (stored order)
  Acknowledge the successful commit to the client that issued the transaction
  Release the transaction's locks so waiting transactions can proceed
  Execute the transaction's reads and writes against pages held in the in-memory
  buffer pool
  Write the modified pages from the buffer pool back to the main data files, at some
  later point
  Append a log record describing each change and force it to stable storage, waiting
  for the acknowledgement

Rules (only these four; nothing else is constrained):
  Execute before Append the log record
  Append the log record before Acknowledge the commit
  Append the log record before Write the pages back
  Append the log record before Release the locks

Valid orders include:
  Execute, Append log, Acknowledge, Write pages, Release locks
  Execute, Append log, Write pages, Release locks, Acknowledge
  Execute, Append log, Release locks, Acknowledge, Write pages
Invalid:        Execute, Acknowledge, Append log, … (acknowledged before it was durable)

THE DESIGN POINT: after a miss, the answered state cannot show "the right order",
because there is not one. It must mark the pairs the reader put the wrong way round
("Append the log record has to come before Acknowledge the commit") and nothing else.
Answer text:    The log record must be durable before anything depends on it. The
                rest of the order is free.
```

---

## 4. claim_grid

### 4a. Short, 3 statements

```
Java · equals and hashCode  ·  Medium  ·  All that apply
Served because: New card on equals and hashCode.

Prompt
  Mark each statement as true or false.

Content (3 statements)
  Two equal objects must return the same hashCode.
  Two objects with the same hashCode must be equal.
  Overriding equals without hashCode can break HashMap lookups.

Correct:        True, False, True
A wrong answer: True, True, True
Answer text:    Equal objects must agree on hashCode, but a shared hashCode is only a
                collision and does not imply equality.
```

The prompt is boilerplate. The question is entirely in the statements.

### 4b. Long, 4 sentence-length statements

```
System design · Quorums  ·  Hard  ·  All that apply
Served because: Due for review: you've seen this card before and it's time to recall it again.

Prompt
  A key is replicated on N = 3 nodes. Mark each statement as true or false.

Content (4 statements)
  With a write quorum of 2 and a read quorum of 2, every read is guaranteed to
  include the latest acknowledged write.
  With a write quorum of 1 and a read quorum of 1, a read can return a value older
  than a write that was already acknowledged.
  Raising the read quorum to 3 while keeping the write quorum at 1 still guarantees
  every read includes the latest acknowledged write.
  Quorum reads and writes alone make concurrent writes to the same key settle into
  one agreed order.

Correct:        True, True, True, False
A wrong answer: True, True, False, False
Answer text:    A read sees the latest write whenever read quorum plus write quorum
                exceeds N. Quorums say nothing about how concurrent writes are
                ordered; that needs versioning or conflict resolution.
```

---

## 5. bucket

### 5a. Short, 2 columns, 4 items

```
CS · TCP and UDP  ·  Easy  ·  Two-way
Served because: New card on TCP and UDP.

Prompt
  Sort each use by the transport it normally runs over.

Content
  Items:   DNS query | HTTP/1.1 request | Live video call | SSH session
  Columns: UDP | TCP

Correct:        DNS query → UDP    HTTP/1.1 request → TCP
                Live video call → UDP    SSH session → TCP
A wrong answer: SSH session → UDP (the other three right)
Answer text:    Ordered, reliable delivery needs TCP. DNS and live media trade
                reliability for low latency.
```

### 5b. Long, 3 columns, 6 sentence-length items

```
Java · Collections  ·  Hard  ·  Three-way
Served because: Collections is one of your weak spots. Another go should help it stick.

Prompt
  Sort each iteration by the order it is guaranteed to produce.

Content
  Items (6):
    Iterating a LinkedHashSet after adding c, a, b
    Iterating a TreeSet after adding c, a, b
    Iterating a HashSet after adding c, a, b
    Iterating an ArrayList after adding c, a, b
    Iterating a TreeMap's keys after putting c, a, b
    Iterating a HashMap's keys after putting c, a, b
  Columns (3):  Insertion order | Sorted order | No guaranteed order

Correct:        LinkedHashSet → Insertion      TreeSet → Sorted
                HashSet → No guarantee         ArrayList → Insertion
                TreeMap → Sorted               HashMap → No guarantee
A wrong answer: HashSet → Insertion order
Answer text:    A hash-based collection's order is an implementation detail and may
                change between runs. Only the Linked and Tree variants, and lists,
                promise one.
```

---

## 6. self_rate

No options. The reader recalls the answer in their head, rates themselves, then sees
the answer. The only primitive the reader grades.

### 6a. Short

```
DSA · Arrays & Hashing  ·  Easy  ·  Flash
Served because: New card on Arrays & Hashing.

Prompt
  What is the time complexity of indexed access into an array, and why?

Reader sees:    two buttons, "Missed it" and "Got it"
Answer text:    O(1). The address is computed from the base pointer and the index, so
                no element is examined on the way.
After "Missed it": score 0%, "Not quite", answer shown, back soon.
```

### 6b. Long

```
System design · Caching  ·  Medium  ·  Flash
Served because: Caching is one of your weak spots. Another go should help it stick.

Prompt
  What is a cache stampede, what makes it dangerous on a hot key, and what are two
  different ways to prevent one?

Answer text:    When a popular entry expires or is deleted, many concurrent readers
                all miss together and each queries the database for the same value,
                which can overload it. Prevent it by letting only one reader rebuild
                the entry while the rest wait (a lock or request coalescing), or by
                refreshing the entry before it expires (early or probabilistic
                refresh), or by adding jitter to TTLs so keys do not expire together.
```

---

## 7. tap_in_place

Code, one line per tap target. The answer is a single line.

### 7a. Short, 6 lines

```
DSA · Arrays & Hashing  ·  Easy  ·  Tap the bug
Served because: New card on Arrays & Hashing.

Prompt
  This function should return the largest number in the list. Tap the line that
  makes it wrong for some inputs.

Content (6 lines)
  1  def find_max(nums):
  2      best = 0
  3      for n in nums:
  4          if n > best:
  5              best = n
  6      return best

Correct:        line 2
A wrong answer: line 4
Answer text:    Starting at 0 means a list of only negative numbers returns 0, which
                is not in the list. Start from nums[0].
```

### 7b. Long, 14 lines (the maximum), indentation matters

```
Java · Concurrency  ·  Hard  ·  Tap the unsafe line
Served because: Due for review: you've seen this card before and it's time to recall it again.

Prompt
  This lazily created singleton uses double-checked locking. Tap the line that makes
  it unsafe under concurrent access.

Content (14 lines)
  1   public class Config {
  2       private static Config instance;
  3       private Config() { load(); }
  4       public static Config get() {
  5           if (instance == null) {
  6               synchronized (Config.class) {
  7                   if (instance == null) {
  8                       instance = new Config();
  9                   }
  10              }
  11          }
  12          return instance;
  13      }
  14  }

Correct:        line 2 (the field must be volatile)
A wrong answer: line 6
Answer text:    Without volatile, another thread can see a non-null reference to a
                partly constructed Config. volatile forbids that reordering.
```

Lines 9 to 11 and 13 to 14 are only closing braces: valid tap targets with almost no
text, which a design has to make tappable all the same.

---

## 8. assemble

Build a line from tokens. Some slots can be pre-filled and fixed.

### 8a. Short, 5 tokens, nothing pre-filled

```
DSA · Basics  ·  Easy  ·  Fill a code blank
Served because: New card on Basics.

Prompt
  Assemble the statement that returns x plus one.

Content: 5 tokens (stored order, shuffled), no pre-filled slots
  x   return   1   +   ;

Correct:        return x + 1 ;
A wrong answer: x return + 1 ;
```

### 8b. Long, clause-length tokens, two slots pre-filled

```
SQL · Transactions & ACID  ·  Hard  ·  Fill a definition
Served because: Due for review: you've seen this card before and it's time to recall it again.

Prompt
  Assemble the statement that defines isolation.

Content: 7 slots, two already filled and fixed
  [ Isolation means that ]   (fixed)
  [ ]  [ ]  [ ]  [ ]  [ ]
  [ until they commit. ]     (fixed)

  Pool of 5 tokens to place, stored order:
    each other's
    uncommitted
    concurrent transactions
    intermediate writes
    cannot observe

Correct:        Isolation means that concurrent transactions cannot observe each
                other's uncommitted intermediate writes until they commit.
A wrong answer: … cannot observe concurrent transactions each other's uncommitted …
```

---

## 9. grid_toggle

A truth grid. The reader ticks cells. The answer is the exact set of ticked cells.

### 9a. Short, 2 × 2

```
DSA · Stacks & Queues  ·  Easy  ·  Method semantics
Served because: New card on Stacks & Queues.

Prompt
  Tick the order each structure removes items in.

Content
  Rows:    Stack | Queue
  Columns: LIFO | FIFO

Correct ticks:  Stack × LIFO,  Queue × FIFO
A wrong answer: Stack × LIFO,  Queue × LIFO
```

### 9b. Long, 5 rows × 3 columns (the largest), long row labels

```
DSA · Complexity  ·  Hard  ·  Complexity table
Served because: Complexity is one of your weak spots. Another go should help it stick.

Prompt
  Tick the time complexity each operation has in the typical case.

Content
  Rows (5):
    Reading an element of an array by its index
    Reading an element of a linked list by its position
    Looking up a key in a hash table
    Looking up a key in a balanced binary search tree
    Reading the minimum of a binary min-heap
  Columns (3):  O(1) | O(log n) | O(n)

Correct ticks:  array × O(1)            linked list × O(n)
                hash table × O(1)       BST × O(log n)
                min-heap peek × O(1)
A wrong answer: hash table × O(log n) instead of O(1), the rest right
```

Three columns is the hard ceiling. A fourth does not fit a phone.

---

## 10. numeric

A number, judged against an expected value within a tolerance. The card says whether
the keypad offers a decimal point and a minus sign.

### 10a. Short, integers only

```
CS · Binary  ·  Easy  ·  Estimate
Served because: New card on Binary.

Prompt
  How many bits are needed to give 200 distinct values their own pattern?

Expected: 8     Tolerance: 0
Keypad:   digits only. No decimal point. No minus sign.
A wrong answer: 7
Answer text:    7 bits give 128 patterns, which is too few. 8 bits give 256.
```

### 10b. Long, decimals and a tolerance

```
CS · Storage  ·  Hard  ·  Estimate
Served because: Due for review: you've seen this card before and it's time to recall it again.

Prompt
  A hard disk spins at 7,200 revolutions per minute. On average the sector you want
  is half a revolution away from the head when a request arrives. What is the
  average rotational latency in milliseconds, to two decimal places?

Expected: 4.17     Tolerance: 0.05
Keypad:   digits and a decimal point. No minus sign.
A wrong answer: 8.33 (a full revolution)
Answer text:    7,200 rpm is 120 revolutions per second, so one revolution takes
                8.33 ms and half of one takes 4.17 ms.
```

Answered state shows the reader's value beside the expected one and the tolerance:
"the answer is 4.17, within 0.05".

---

## 11. compose

A written answer, 40 to 300 characters. The rubric is shown **before** answering. A
model marks it point by point. The result reads "N of M key points", with each point
ticked or crossed, and passes at 70%.

### 11a. Short, 3 rubric points

```
Behavioural · Feedback  ·  Medium  ·  Your own story
Served because: New card on Feedback.

Prompt
  Tell me about a time you received difficult feedback.

Rubric (shown first, 3 points)
  Names a specific piece of feedback
  States what you changed in response
  Says what happened afterwards

The reader types (118 characters):
  My lead said my pull requests were too large to review. I started splitting work
  into smaller changes.
Result:         "2 of 3 key points", below the 70% pass mark → "Not quite"
                ✓ Names a specific piece of feedback
                ✓ States what you changed in response
                ✕ Says what happened afterwards
```

### 11b. Long, 4 rubric points, long prompt

```
Behavioural · Conflict  ·  Hard  ·  Your own story
Served because: Conflict is one of your weak spots. Another go should help it stick.

Prompt
  Tell me about a time you disagreed with a teammate about a technical decision that
  mattered to the project. Walk me through how you handled it, and what you would do
  the same or differently if it happened again.

Rubric (shown first, 4 points)
  Describes a specific situation with enough context to understand the disagreement
  States what you personally did, in the first person, rather than what the team did
  Includes a concrete outcome, with a number or an observable change where there is one
  Says what you would repeat and what you would change

The reader types (287 characters):
  On the payments rewrite I wanted retries in the client and our tech lead wanted them
  in the gateway. I built both behind a flag and we measured failure rates for a week.
  The gateway version cut duplicate charges to zero, so I switched. Next time I would
  propose the experiment on day one.
Result:         "4 of 4 key points", above the pass mark → "Correct"
```

---

## What is special, beyond the eleven primitives

Everything below changes what a card has to be able to show. Wording is the app's own.

### Result states (the same card, five endings)

| The reader… | Heading | Score shown? | Answer shown? |
|---|---|---|---|
| answers right | "Correct" | yes, 100% | yes |
| answers wrong | "Not quite" | yes, 0% | yes |
| skips | "Skipped" | no | yes |
| taps "New to me" | "New to you — here's the answer" | no | yes |
| taps "I already know this" | "Marked as known" | no | yes |

"Next review tomorrow" or "Next review in N days" appears after any graded or
declared result.

### "Why this card" lines (four, verbatim)

- New: `New card on {Topic}.`
- Due: `Due for review: you've seen this card before and it's time to recall it again.`
- Weak: `{Topic} is one of your weak spots. Another go should help it stick.`
- Diagnostic: `Part of your diagnostic: it sets your starting readiness.`

Topic names run long ("Segment Tree & Fenwick", "2-D Dynamic Programming"), so this
line wraps.

### "I already know this"

Offered only once the reader has a record on the topic. After tapping it the card
shows "Marked as known" and a one-time offer to retire the rest of the topic's
unseen cards, with the count remaining.

### The diagnostic (first visit)

A fixed number of cards per area (4), easiest first. Each shows its position in the
sequence and the diagnostic line above. At the end, a summary by area: answered and correct
per area. It seeds the readiness score.

### Offline

If the connection drops mid-answer the answer is queued and the card shows:
"Saved. It'll be graded when you're back online." with a Next card button, and no
result.

### Compose when the grader is unavailable

The reader has already typed two or three sentences, so the card does not error. It
says "The automatic mark is unavailable. Judge your answer against what it had to
cover.", shows the rubric as a plain list, and offers "Missed it" / "Got it".

### The Today panel

Three numbers: Answered, Correct (a rounded percentage), Skipped. Correct has no
value until the first answer. After 20 answers, if a mission is still open, a banner
about that mission appears.

### Smaller things

- Any prompt may carry a fenced code block or inline `code`; `tap_in_place` is all code.
- Source pills: some link to a lesson, some are plain text.
- Enter on a result goes to the next card on desktop.
- A "Report" link sits under every card.
- Empty states: no cards, all areas switched off, nothing left to ask today.
