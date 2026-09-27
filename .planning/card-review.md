# Cards: the sample before a bulk run

91 kept, 5 rejected by the gate (5%). Format mix: 48 typed, 23 flash, 18 mcq, 2 output.

**What to check:** could you answer each one having read the lesson and nothing else? Is the format right - typed for explanation, flash for a fact, mcq where the options matter? Then skim the rejections and tell me whether the gate threw away anything good.

---

## ai-generative-ai-llms

**typed** (Medium) - Why does repeated next-token prediction produce coherent text even though the model only maximizes local token likelihood?

> Coherence emerges because the model is trained on huge corpora and learns long-range dependencies through self-attention. The training objective maximizes local token likelihood, not global correctness.

*Graded on: Trained on large corpora, Self-attention captures long-range dependencies, Objective is local token likelihood, not global truth*

**flash** (Easy) - What is a large language model at its core?

> A transformer trained to model a probability distribution over token sequences by predicting each next token given the previous tokens.

*Graded on: Transformer architecture, Next-token prediction over token sequences*

**mcq** (Easy) - Which claim about temperature is correct?

- Temperature increases factual accuracy
- Temperature only changes sampling randomness
- Temperature expands the context window
- Temperature trains preference pairs

> Temperature only changes sampling randomness

*Graded on: Temperature scales logits, It does not change truth or knowledge*

---

## arrays-hashing

**typed** (Easy) - When would you choose a hash map over a hash set in an array problem, and what kind of value would you store?

> Use a hash map when you need to associate each element with extra information such as its original index, frequency, or group. For example, one-pass Two Sum stores each value's index so it can return original positions.

*Graded on: Hash set only stores keys, Hash map stores key-value pairs, Example: store indices for Two Sum*

**flash** (Medium) - What are the average and worst-case lookup complexities of a hash map with chaining under adversarial collisions?

> Average O(1), worst-case O(n) per lookup; some runtimes convert long bucket chains to balanced trees to achieve O(log n) worst-case.

*Graded on: Average O(1), Worst-case O(n) for collisions, Balanced tree bucket conversion gives O(log n)*

**mcq** (Easy) - Which data structure is the natural choice for detecting duplicates while scanning an array once?

- Hash set
- Balanced binary search tree
- Priority queue
- Linked list

> Hash set

*Graded on: Set membership check is O(1) average, Insert each element and detect if already present*

---

## beh-star-method

**typed** (Medium) - Why do interviewers find STAR answers easier to evaluate than unstructured stories?

> STAR reveals what the candidate specifically did, why they did it, and whether the outcome mattered, which makes past behavior a clearer predictor of future performance.

*Graded on: reveals specific individual actions, explains reasoning and decision, includes measurable or meaningful outcome, predicts future performance from past behavior*

**flash** (Easy) - What does the acronym STAR stand for in behavioral interviewing?

> Situation, Task, Action, Result; some organizations replace Task with Target to emphasize self-set goals.

*Graded on: Situation, Task, Action, Result, Target variant emphasizes self-set goals*

**mcq** (Medium) - A candidate spends 70% of a STAR answer describing the project, team, and background. Which sections are over-expanded relative to the guideline?

- Situation and Task
- Action and Result
- Task and Action
- Result alone

> Situation and Task

*Graded on: Situation and Task should be the first quarter combined, Action should be half or more, Over-long context weakens the answer*

---

## cs-tcp-vs-udp

**typed** (Medium) - What is the fundamental tradeoff between TCP and UDP?

> TCP provides a reliable, ordered, full-duplex byte stream at the cost of handshake, sequence numbers, acknowledgements, retransmission, flow control, and congestion control. UDP is connectionless and message-oriented with no delivery or ordering guarantees, so it has lower protocol overhead and less per-connection state, but applications must add any required reliability themselves.

*Graded on: TCP is connection-oriented, reliable, and ordered, TCP adds handshake, ACK, retransmission, flow and congestion control overhead, UDP is connectionless, message-oriented, with no delivery or ordering guarantees, Applications choose based on whether retransmitting old data is harmful*

**flash** (Easy) - What are the three messages of the TCP three-way handshake?

> The TCP three-way handshake is SYN from the client, SYN-ACK from the server, then ACK from the client.

*Graded on: Client sends SYN, Server replies SYN-ACK, Client sends ACK, Final ACK may carry data; TCP Fast Open allows data in SYN*

**output** (Easy) - Given the following handshake exchange, what ACK value does A send in the final ACK?
```
A -> B: SYN seq=1000
B -> A: SYN-ACK ack=1001 seq=4000
A -> B: ACK ack=?
```

> 4001

*Graded on: Server's initial sequence number is 4000, ACK acknowledges server's sequence number plus 1, Final ACK value is 4001, In standard TCP this ACK may carry application data*

---

## java-collections-framework

**typed** (Medium) - What is the core design principle of the Java Collections Framework, and why does it matter for algorithms?

> The framework separates collection interfaces from concrete storage strategies, and utility algorithms operate on those interfaces. This lets the same sort, search, or wrapper method work across ArrayList, LinkedList, HashSet, and other implementations.

*Graded on: Interfaces define behavior, implementations define storage, Algorithms operate on interfaces, Same algorithm works across implementations*

**flash** (Easy) - What is the difference between Collection and Collections?

> Collection is the root interface of the framework, while Collections is a utility class with static methods like sort, max, unmodifiableList, and synchronizedMap.

*Graded on: Collection is a root interface, Collections is a utility class, Collections methods are static*

**mcq** (Medium) - What order does the iterator of a PriorityQueue return elements in?

- Ascending priority order
- Descending priority order
- Arbitrary heap-array order
- Insertion order

> Arbitrary heap-array order

*Graded on: Only poll/peek return the least element, Iterator traverses the underlying heap array, Iteration order is not sorted*

---

## lld-abstraction

**typed** (Medium) - Why should callers depend on an abstract type rather than a concrete class?

> Callers written against an abstract type are not coupled to a specific implementation, so the concrete class can be replaced without changing caller code. This also enables polymorphism, since several concrete implementations can satisfy the same contract and be substituted at runtime.

*Graded on: reduces coupling to a concrete implementation, enables runtime substitution and polymorphism*

**flash** (Easy) - What does abstraction expose and hide in a component or operation?

> Abstraction exposes a stable public contract for what an operation or component does while hiding how that behavior is implemented.

*Graded on: exposes a stable public contract, hides implementation details*

**mcq** (Medium) - Which statement correctly contrasts an abstract class and an interface in Java-style OO languages?

- An interface can be instantiated but an abstract class cannot.
- An interface carries no instance state and a class can implement multiple interfaces but extend only one abstract class.
- An abstract class cannot contain implemented methods, while an interface can.
- A class can extend multiple abstract classes but can implement only one interface.

> An interface carries no instance state and a class can implement multiple interfaces but extend only one abstract class.

*Graded on: abstract class cannot be instantiated and may have state/implemented methods, class implements multiple interfaces but extends one abstract class*

**output** (Easy) - What does this code print?
```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

class Square(Shape):
    def area(self):
        return 4

try:
    s = Shape()
except TypeError:
    print('TypeError')
print(Square().area())
```

> TypeError
4

*Graded on: Shape cannot be instantiated because it is abstract, Square implements area and returns 4*

---

## sd-caching

**typed** (Easy) - Why does caching reduce latency and database load only for certain workloads?

> It relies on locality of reference, so there must be repeated reads of the same data; workloads need to be read-heavy with hot skewed keys and tolerate stale reads for the cache to provide benefit.

*Graded on: locality of reference, read-heavy and skewed hot keys, tolerance for stale reads*

**flash** (Easy) - What is a cache hit and a cache miss?

> A hit is when the requested key is present in the cache and fresh; a miss triggers fetching the value from the source of truth and writing it into the cache.

*Graded on: hit means key present and fresh, miss triggers source fetch, miss populates cache*

**mcq** (Easy) - Which cache placement is best for serving public static assets to users around the world?

- Browser HTTP cache
- CDN edge
- Application-server RAM
- Database buffer pool

> CDN edge

*Graded on: CDN pushes static content to edge nodes near users, lowers geographic latency and origin load, best for public static assets*

---

## sql-indexes

**typed** (Medium) - Why can adding an index make write operations slower?

> Every insert, update, or delete that affects indexed columns must also modify each affected index. This adds I/O and CPU to write transactions and can cause page splits, logging overhead, and lock contention.

*Graded on: writes must maintain affected indexes, adds I/O and CPU to writes, can cause page splits and logging overhead, many indexes multiply maintenance*

**flash** (Easy) - What is an index in a relational database?

> An index is a separate data structure, usually a B-tree, that stores a sorted copy of one or more table columns along with pointers to the corresponding rows.

*Graded on: separate data structure from table, usually a B-tree, sorted copy of columns, pointers to rows*

**mcq** (Medium) - A composite index is created on (a, b). Which predicate is least able to use a normal B-tree index seek?

- WHERE a = 10
- WHERE a = 10 AND b = 5
- WHERE b = 5
- WHERE a > 10

> WHERE b = 5

*Graded on: index is sorted by a then b, a predicate on the leading column can seek, a predicate on b alone cannot seek normally, b is not the leftmost key*

---

## What the gate rejected

- **arrays-hashing** (flash): What is the main transformation that replaces an O(n^2) nested array scan with an O(n) solution?
  - ambiguous: There is no single 'main transformation' that reduces O(n^2) nested scans to O(n) (e.g., hash lookups, two pointers, prefix sums).
- **arrays-hashing** (output): What is the exact output of the following code?
```python
def two_sum(nums, target):
    seen = {}
    for i, v in enumerate(nums):
        if target - v in seen:
            return [seen[target - v], i]
        seen[v] = i

print(two_sum([2, 7, 11, 15], 9))
```
  - wrong_format: Format 'output' is not one of the allowed card formats (flash, typed, mcq).
- **beh-star-method** (flash): What is the main trade-off of using STAR in a behavioral interview?
  - ambiguous: STAR is a framework without a standard, universally agreed upon 'main trade-off'.
- **java-collections-framework** (flash): In the Java Collections Framework, which interfaces extend Collection, and where does Map fit?
  - wrong_format: Asking to list which interfaces extend Collection requires enumeration and is too long for a crisp one-sentence flashcard.
- **sd-caching** (mcq): In the worked example, a product page is fetched 5,000 times per second and the database sustains 800 reads per second. After the Redis cache is warm with a 30-second TTL, how many database reads per second does that single product key cause?
  - needs_context: Refers to a specific "worked example" that the candidate cannot see.