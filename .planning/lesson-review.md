# Lessons: what needs your eyes

242 of 274 lessons passed every gate. Below are the 32 the fact-checker still objects to, then one sample from each of the 8 areas.

**What to do:** read two or three samples. If they are the standard you want, the rest ship. Then skim the objections - each one is a claim a second model says is wrong or half-true, and the lesson is held back until someone rules on it.

---

## Held back by the fact-checker

### 2-D Dynamic Programming  `2-d-dynamic-programming`

- **oversimplified**: Interval DP can be implemented with for i in range(n-1, -1, -1): for j in range(i, n): because i decreases and j increases, so smaller intervals are computed before larger ones; a separate length loop is not required.
  - Reviewer says: Iterating `i` backwards and `j` forwards does not compute strictly smaller intervals first (e.g., `(i, j) = (n-2, n-1)` of length 2 runs before `(n-1, n-1)` of length 1 is extended, or `(0, n-1)` runs before other small intervals are considered). However, it *does* correctly satisfy dependencies for standard interval DP recurrences that only access subproblems `dp[i+1][j]`, `dp[i][j-1]`, or `dp[i][k]` and `dp[k][j]` with `k < j`, because all states with larger starting index `> i` and smaller ending index `< j` are already computed. The claim that it computes intervals in order of length is incorrect, even though the dependency order remains valid for standard transitions.
- **oversimplified**: For a literal or '.', the transition is dp[i][j] = dp[i-1][j-1] if the current chars match. For '*', the pattern p[j-2] repeated zero or more times branches into skip the pattern token dp[i][j-2] or consume a matching character dp[i-1][j].
  - Reviewer says: When consuming a matching character for '*', the character `s[i-1]` must actually match the preceding pattern character `p[j-2]` (or `p[j-2] == '.'`). If they do not match, the branch `dp[i-1][j]` cannot be taken; the only option is skipping the token via `dp[i][j-2]`.

### Advanced Graphs  `advanced-graphs`

- **oversimplified**: Prim grows a single tree and uses a min-heap keyed by the cheapest edge into the tree, which is good for dense graphs and runs in O(E log V).
  - Reviewer says: Binary heap Prim runs in O(E log V), which is asymptotically the same as Kruskal O(E log V) and not advantageous on dense graphs (where E ~ V^2, making E log V ~ V^2 log V). For dense graphs, Prim implemented with an adjacency matrix or simple array runs in O(V^2), or with a Fibonacci heap in O(E + V log V), which outperforms binary heap Prim and Kruskal.

### Embedding Models  `ai-embedding-models`

- Failed the contract: refers to source the reader cannot see: 'the document'

### Growth mindset  `beh-growth-mindset`

- Failed the contract: refers to source the reader cannot see: 'the lesson'

### Bit Manipulation  `bit-manipulation`

- **oversimplified**: For nonzero x, it isolates the lowest set bit. Two's-complement negation ~x + 1 preserves the lowest set bit and all trailing zeros and flips every higher bit, so ANDing with x clears the higher bits and leaves a power of two.
  - Reviewer says: In fixed-width two's complement, when x is the minimum representable signed integer (e.g., INT_MIN = -2147483648 for 32-bit signed ints), `-x` overflows (undefined behavior in C/C++). While `-INT_MIN` wraps around to `INT_MIN` in modular arithmetic, the resulting bitmask is negative (sign bit set), not a positive power of two.
- **oversimplified**: Using `(x & (x - 1)) == 0` to test for a power of two without first checking `x > 0`, which wrongly accepts zero and negative numbers.
  - Reviewer says: For most negative numbers, `(x & (x - 1)) == 0` evaluates to false (not zero). In two's complement, the only negative number that actually satisfies `(x & (x - 1)) == 0` upon signed underflow/wrapping is the minimum signed integer (e.g., `INT_MIN = -2147483648`).

### TLB and Caching  `cs-tlb-and-caching`

- **wrong**: Every memory access first needs a physical address.
  - Reviewer says: Memory accesses to a virtually indexed, virtually tagged (VIVT) cache do not need a physical address to complete a hit; physical addresses are only required on misses or when translating through the TLB/MMU.
- **oversimplified**: A direct-mapped 32 KiB cache with 512 sets also maps both addresses to set 64 (since 576 mod 512 = 64)
  - Reviewer says: Re-accessing 0x1000 and 0x9000 produces 2 hits out of the 4 accesses in the sequence (miss, miss, hit, hit), not 'zero hits for the sequence'. Zero hits would only occur if the sequence alternated indefinitely (e.g. repeated thrashing pattern).

### Serialization  `java-serialization`

- **oversimplified**: A class can define private writeReplace or private readResolve methods.
  - Reviewer says: While `readResolve` and `writeReplace` can be declared `private`, doing so restricts their visibility exclusively to that defining class. Unlike `readObject` and `writeObject` (which must be `private` and are called via reflection specifically on the target class), `readResolve` and `writeReplace` can also be `protected` or `public` (or package-private) so they can be inherited by subclasses. Making them strictly `private` is not required and prevents subclass inheritance.

### Thread lifecycle  `java-thread-lifecycle`

- **wrong**: After Object.wait() wakes, the thread must reacquire the monitor it released; if that monitor is free it can transition directly from WAITING to RUNNABLE, otherwise it briefly enters BLOCKED.
  - Reviewer says: According to the Java Language Specification (§17.8.1) and JVM specification, when a thread is awakened via notify/notifyAll/interrupt/spurious wakeup, it transitions from the wait set to the monitor's entry/re-entry set where it must compete for the monitor lock. Under Thread.State semantics, a thread waiting to reacquire the monitor after wait() is in the BLOCKED state until it successfully reacquires the monitor; it cannot bypass BLOCKED and go directly from WAITING to RUNNABLE while waiting for monitor acquisition.
- **wrong**: Can a thread move from WAITING directly to RUNNABLE after Object.notify? Yes, if the monitor it released for wait is uncontended when it wakes and reacquires it. If another thread holds the monitor, it moves to BLOCKED first, then RUNNABLE once it acquires the lock.
  - Reviewer says: The answer is no for notify(). When notify() is called, the notifying thread still holds the monitor (as notify requires holding the monitor). The notified thread moves from WAITING into BLOCKED (or BLOCKED is observed) because it must reacquire the monitor, which is currently held by the notifying thread. Even in the abstract state model, monitor reacquisition is explicitly defined as entering BLOCKED before becoming RUNNABLE.
- **oversimplified**: The joining thread is in WAITING while blocked inside Thread.join (implemented with wait on the target Thread object).
  - Reviewer says: Starting in Java 21+ (and finalized via project Loom / virtual threads integration), Thread.join() is no longer implemented via Object.wait() on the Thread instance; it now uses internal synchronization primitives (such as parking / virtual thread support). While historically accurate, asserting that Thread.join() is implemented with wait() on the Thread instance is obsolete.

### Hotel Management System Design  `lld-hotel-management-system-design`

- **oversimplified**: In PostgreSQL, an exclusion constraint on (room_id, date_range) rejects overlapping inserts at the schema level.
  - Reviewer says: A basic exclusion constraint on `(room_id WITH =, date_range WITH &&)` rejects *any* overlapping date ranges for that room, regardless of status. Since cancelled, checked-out, or unconfirmed reservations must not block new bookings, the constraint must be a partial index using a predicate (e.g. `WHERE (status IN ('CONFIRMED', 'CHECKED_IN'))`), otherwise cancelled bookings permanently block the room.

### UML Sequence Diagram  `lld-uml-sequence-diagram`

- **wrong**: Creation in UML 2.x is a dashed arrow with an open arrowhead pointing to the new lifeline's head
  - Reviewer says: In standard UML 2.x (OMG specification), a CreateObjectMessage (or creation message) is drawn as a solid line with an open arrowhead pointing directly to the head of the created lifeline, not a dashed line. Dashed arrows with open arrowheads are reserved for reply/return messages (ReplyMessage).

### Matrix / Grid  `matrix-grid`

- **oversimplified**: For Diagonal Traverse, group cells by r+c; collect each diagonal top-to-bottom and reverse even diagonals, so [[1,2,3],[4,5,6]] yields [1,2,4,5,3,6].
  - Reviewer says: For standard Diagonal Traverse (LeetCode 498), traversal starts going up-right (diagonal sum 0), then down-left (sum 1), up-right (sum 2), etc. Collecting top-to-bottom (row increasing) produces down-left order, so even-sum diagonals must be reversed (or traversed bottom-to-top) to go up-right, while odd-sum diagonals remain top-to-bottom. Reversing even diagonals of [[1,2,3],[4,5,6]] yields [1,2,4,5,3,6] only because 0 is a single element, diagonal 1 is kept as [2,4], diagonal 2 ([3,5]) is reversed to [5,3], and diagonal 3 ([6]) stays [6]. However, in standard interview terminology and the lesson's own worked example, it calls diagonal 1 'down-left' and diagonal 2 'up-right', which means odd diagonals go down and even diagonals go up; reversing top-to-bottom for even diagonals matches up-right, but the lesson claims reversing even diagonals when collected top-to-bottom reverses diagonal 0 and 2, which matches [1, 2, 4, 5, 3, 6], but the text incorrectly describes the alternating directions or mixes odd/even indexing.
- **oversimplified**: In iterative DFS, mark a cell visited when you push it onto the stack, or track an in-stack state; marking only on pop allows duplicate insertions and can blow up stack size.
  - Reviewer says: Marking a node visited upon push in DFS changes the traversal order to be different from standard DFS (a node's neighbor might be marked visited prematurely before the deepest path reaches it, preventing other paths from exploring it or mimicking BFS-like discovery rather than true DFS stack semantics). While marking on push prevents duplicate stack entries, standard iterative DFS marks on pop (while skipping if already visited when popped) to preserve exact DFS traversal order, accepting O(V + E) stack entries, or tracks an in-stack state explicitly without skipping valid backtracking.

### Cache strategies  `sd-cache-strategies`

- **wrong**: With write-around, a like bypasses the cache and goes directly to the database, so the next read may miss until a later read repopulates it.
  - Reviewer says: Because write-around bypasses the cache without invalidating or updating it, if the cache already contains an entry for that key, the next read will hit the cache and return a stale value—it will not result in a cache miss unless the entry had already expired via TTL or was explicitly invalidated.

### CDN  `sd-cdn`

- **oversimplified**: Personalized, authenticated, or response-varying content must be keyed correctly (for example with Vary: Cookie or Authorization) or not cached by the shared CDN, to avoid cross-user data leakage.
  - Reviewer says: Using `Vary: Cookie` or `Vary: Authorization` in a shared CDN does not safely protect against cross-user data leakage and is widely considered an anti-pattern. Most CDNs either normalize, ignore, or outright refuse to cache responses with `Vary: Cookie` / `Authorization`, or risk fragmenting cache/leaking variants. RFC 9111 explicitly specifies that shared caches must not store responses to requests with an `Authorization` header field unless a directive like `must-revalidate`, `public`, or `s-maxage` is present, and user-specific authenticated content should simply specify `Cache-Control: private, no-store` rather than relying on `Vary: Cookie`.

### Consistency models  `sd-consistency-models`

- **oversimplified**: Read-your-writes is a session guarantee that can be met by routing a session to one primary or replica, or by using quorums with W+R>N.
  - Reviewer says: Quorums with W+R>N do not guarantee read-your-writes by themselves in leaderless systems (like Dynamo or Cassandra) without synchronous read repair or monotonic version tracking. If a concurrent write is in flight, or if node failures trigger sloppy quorums/hinted handoff, a client can execute a write and immediately read a stale value from a valid quorum.

### Design a rate limiter  `sd-design-a-rate-limiter`

- **oversimplified**: Redis can perform the check-and-increment atomically with a Lua script or MULTI/EXEC
  - Reviewer says: MULTI/EXEC cannot perform conditional check-and-increment logic on its own without WATCH (optimistic locking), because all commands in MULTI/EXEC are queued and executed together without allowing application logic to inspect intermediate values before deciding whether to proceed. Lua scripts, however, run atomically and allow branching logic (evaluating current count vs limit) directly on the Redis server.
- **wrong**: Or assign each client a fixed shard so the hot key is spread across shards, and set shard-level limits.
  - Reviewer says: Assigning each client to a fixed shard places that specific client's key entirely on that one shard, which does not spread a single hot key across shards; to mitigate a single hot key, techniques like sub-key sharding (e.g., key_1, key_2 with split limits) or local in-memory buffering are required.

### Design a ride-sharing service  `sd-design-a-ride-sharing-service`

- **oversimplified**: Live location is a push pipeline: the driver app sends updates over WebSocket or UDP, the backend validates and fans them out to the matched rider, throttling to once every 1-4 seconds.
  - Reviewer says: Raw UDP cannot be directly initiated from mobile application layers to web services through standard mobile carrier NATs without specialized tunneling or protocols like QUIC/HTTP3, and UDP alone lacks authentication, sequence framing, and reliability. In practice, mobile ride-sharing apps transmit location updates over TCP-based persistent connections (like WebSockets, gRPC/HTTP2) or QUIC/HTTP3, rather than raw UDP.
- **oversimplified**: The service sends ride offers to the top 3 drivers with a 15-second accept timeout; if none accepts, it retries with a larger radius or after a backoff.
  - Reviewer says: Broadcasting the same ride offer simultaneously to multiple drivers (top 3) introduces race conditions and driver frustration if multiple accept; production ride-sharing services either offer sequentially to one driver at a time with a strict timeout (e.g., 10-15s), use batch matching / bipartite matching optimizations across all pending riders and drivers, or reserve dispatch locks before offering.

### Design a URL shortener  `sd-design-a-url-shortener`

- **wrong**: On read, resolve the key as close to the user as possible—in-process, Redis, then CDN edge cache, then database
  - Reviewer says: In network architecture, a CDN edge cache sits in front of the origin servers, so the lookup order encountered by an incoming client request is CDN edge cache first, followed by the origin server's in-process cache, Redis, and finally the database.

### Design a video streaming service  `sd-design-a-video-streaming-service`

- **wrong**: If sub-second latency is mandatory, WebRTC is a better fit but scales less cheaply because it is peer-to-peer and less CDN-cacheable.
  - Reviewer says: At streaming service scale, WebRTC for one-to-many live broadcasting is not peer-to-peer; it runs via Selective Forwarding Units (SFUs) or media servers. P2P WebRTC does not scale beyond a handful of viewers per broadcaster.

### Design a web crawler  `sd-design-a-web-crawler`

- **wrong**: The first URL is new; the Bloom filter returns negative, so it is added to the Bloom filter and enqueued into the news.example.com back queue with an earliest-fetch time of now plus 2 seconds.
  - Reviewer says: In standard two-tier crawler architecture (Mercator/UbiCrawler), newly discovered URLs are enqueued into the front (priority) queues, not directly into per-host back queues. Back queues are strictly populated dynamically by a router/selector from front queues when a back queue becomes empty or eligible.
- **oversimplified**: A Bloom filter in front of the seen store gives cheap negatives, but false positives must be checked against the exact store, and deleting entries for re-crawl requires a counting Bloom filter or separate TTL mechanism.
  - Reviewer says: If a Bloom filter sits in front to filter out seen URLs before querying the database, a filter negative means the URL was definitely never visited, which is safe to add. But a filter positive means the URL is likely already visited; checking the exact store on positives will query the DB for virtually every duplicate URL, failing to protect the DB from duplicate lookups unless the exact store is accessed only when confirming potential collisions or if the architecture explicitly accounts for this access pattern.

### Distributed transactions  `sd-distributed-transactions`

- **oversimplified**: Confusing the prepare phase with an actual commit; a prepared participant has not made its changes durable and visible until the commit message.
  - Reviewer says: In 2PC, a participant *must* make its changes durable (e.g., written to write-ahead logs) during the prepare phase before voting yes so it can guarantee committing even after a crash; it only defers making the changes visible (releasing locks) until the commit phase.

### High availability  `sd-high-availability`

- **oversimplified**: Health checks should fail when a critical dependency is unavailable, not just when the process is alive.
  - Reviewer says: Deep health checks that verify downstream dependencies can cause cascading failures: if a shared downstream dependency degrades or fails, all upstream instances fail health checks and get removed by the load balancer, taking down the entire tier. Best practice for load balancer health checks (liveness) is shallow checks, while deep dependency checks should trigger degraded states or circuit breaking rather than immediate instance de-registration.

### Layer 4 vs Layer 7 load balancing  `sd-layer-4-vs-layer-7-load-balancing`

- **oversimplified**: L4 looks only at the transport header—IP addresses, ports, protocol—so it is fast
  - Reviewer says: IP addresses are in the network layer (Layer 3) header (IPv4/IPv6), while ports are in the transport layer (Layer 4) header (TCP/UDP). L4 load balancers inspect both Layer 3 and Layer 4 headers, not solely the transport header.
- **wrong**: Encrypted Client Hello (ECH, RFC 9460) encrypts SNI and prevents non-terminating balancers from routing on it.
  - Reviewer says: RFC 9460 specifies Service Binding and Parameter Specification Resource Records (SVCB/HTTPS RRs) in DNS, not Encrypted Client Hello. ECH is defined in draft-ietf-tls-esni (now RFC 9849 / TLS working group draft).

### Message queues  `sd-message-queues`

- **wrong**: The worker first writes a row with message_id and status='processed' to its dedup table and commits that write. Then it calls the email provider to send a receipt. If the worker crashes 10 seconds after the email call but before deleting the message, the message becomes visible again. Another worker receives it, finds the existing dedup row, skips the email, and deletes the message.
  - Reviewer says: Recording `status='processed'` before calling the email provider introduces a dual-write failure: if the worker crashes after committing the database write but before the email API call succeeds, subsequent redeliveries will see `processed`, skip the email, and the email is permanently lost. To reliably handle non-idempotent external calls without provider-level idempotency keys, you record an 'in-progress' / pending intent, attempt the call, and mark 'completed', or rely on an idempotency key passed directly to the external provider.

### NoSQL types  `sd-nosql-types`

- Failed the contract: refers to source the reader cannot see: 'the document'

### CTEs  `sql-ctes`

- **oversimplified**: Within that statement it can be referenced multiple times, like a parameterized view that exists only for the query's duration.
  - Reviewer says: CTEs cannot take parameters like a parameterized view or function; they are unparameterized query expressions defined by a `WITH` clause.
- **wrong**: PostgreSQL, SQLite, and MySQL accept UNION, which eliminates duplicate rows across iterations.
  - Reviewer says: MySQL does not support `UNION [DISTINCT]` in recursive CTEs; it requires `UNION ALL` (or `UNION DISTINCT` will raise an error in recursive queries, requiring `UNION ALL` between the anchor and recursive parts, though MySQL 8.0.34+ added limited support, standard recursive CTEs in MySQL require UNION ALL). Specifically, MySQL documents that recursive CTEs must combine anchor and recursive parts using UNION ALL or UNION DISTINCT, but in practice, standard MySQL recursive CTE syntax requires UNION ALL.

### Index seek vs scan  `sql-index-seek-vs-scan`

- **oversimplified**: An index scan reads every leaf page of the index, or every data page for a clustered index scan or table scan, and evaluates each row against the predicate.
  - Reviewer says: An index scan does not necessarily read every leaf page. An engine can execute a bounded/partial index scan (range scan) where it scans only a subset of pages, or stop scanning early once a LIMIT or TOP N clause is satisfied.
- **oversimplified**: Seek cost scales with matching rows plus B-tree depth; scan cost scales with total index size.
  - Reviewer says: This applies specifically to a single-range seek. Multi-range seeks (e.g. using `IN (...)` or multiple equality lookups) scale with (number of seek ranges × B-tree depth) plus matching rows, and seeks requiring row/bookmark lookups add an extra cost per matching row.

### Query performance tuning  `sql-query-performance-tuning`

- **wrong**: Rebuilding indexes before checking whether statistics are stale, which can leave the same bad cardinality estimates.
  - Reviewer says: Rebuilding an index (ALTER INDEX ... REBUILD) automatically updates statistics on the index key columns with an equivalent of FULLSCAN. It will not leave stale statistics on the rebuilt index.

### Recursive CTEs  `sql-recursive-ctes`

- **wrong**: SQL Server only permits UNION ALL between anchor and recursive members, while the SQL standard plus PostgreSQL, MySQL, and SQLite also support UNION DISTINCT to deduplicate and prevent some cycles.
  - Reviewer says: SQLite does not support UNION DISTINCT between anchor and recursive members; SQLite's recursive CTE syntax strictly requires UNION ALL (or UNION with exceptional limitations, but standard recursive queries reject UNION / UNION DISTINCT for recursive evaluation and mandate UNION ALL). Specifically, SQLite syntax documentation states: 'The recursive-select must be connected to the previous subquery using either UNION ALL or UNION (or EXCEPT or INTERSECT in some non-standard variants), but SQLite requires UNION ALL between the initial and recursive selects in practice.'
- **oversimplified**: A recursive CTE has an anchor member for starting rows and a recursive member for the next iteration, combined by UNION ALL or UNION [DISTINCT].
  - Reviewer says: A recursive CTE can have multiple anchor members and/or multiple recursive members combined by UNION or UNION ALL; it is not strictly limited to exactly one anchor and one recursive member.

### Subqueries  `sql-subqueries`

- **oversimplified**: A subquery in FROM is a derived table and must have an alias in PostgreSQL, SQL Server, and MySQL.
  - Reviewer says: Starting with MySQL 8.0.19, derived tables in the FROM clause are no longer required to have an explicit table alias. PostgreSQL and SQL Server still require an alias, but MySQL does not in modern versions.
- **oversimplified**: correlated subqueries run for each candidate row of the outer query and become expensive on large inputs
  - Reviewer says: This describes the conceptual/naive semantics, but modern query optimizers frequently unnest or 'decorrelate' correlated subqueries into joins, semi-joins, or anti-joins, avoiding per-row re-evaluation unless decorrelation is impossible or suboptimal.

### Triggers  `sql-triggers`

- **oversimplified**: DML triggers run either AFTER the event, or INSTEAD OF it
  - Reviewer says: This is true for Microsoft SQL Server, but in general SQL standards and other major engines like PostgreSQL, Oracle, and MySQL, DML triggers also support 'BEFORE' triggers, which fire before the triggering statement/row operation and before constraint checks without replacing the statement like INSTEAD OF does.
- **oversimplified**: A trigger is event-driven code that runs inside the database transaction, not a per-row callback. For multi-row DML, a trigger fires once, and inserted/deleted hold all affected rows
  - Reviewer says: While T-SQL (SQL Server) only implements statement-level DML triggers with 'inserted' and 'deleted' pseudo-tables, ANSI SQL and other RDBMSs (such as PostgreSQL, Oracle, and MySQL) explicitly support row-level triggers ('FOR EACH ROW') that execute once per affected row and use record variables like OLD and NEW.

### Window functions  `sql-window-functions`

- **oversimplified**: In standard SQL, window functions execute after FROM, WHERE, GROUP BY, HAVING, and SELECT expressions, but before DISTINCT and ORDER BY.
  - Reviewer says: Window functions are evaluated as part of the SELECT list (and in ORDER BY), not strictly after SELECT expressions; in fact, other SELECT expressions can wrap or reference window function calls, but window functions execute before DISTINCT.

### Two Pointers  `two-pointers`

- **wrong**: Symmetrically, if the sum is too large, right cannot be part of a solution because moving left only increases the sum.
  - Reviewer says: In a sorted array, moving left to the right increases the sum; moving left inward (towards right) increases the sum, but moving left to the left (decreasing the index) decreases the sum. Specifically, for a fixed 'right', any index i with left <= i < right satisfies nums[i] + nums[right] <= nums[left] + nums[right], not >=. The actual reason 'right' cannot be part of a solution when nums[left] + nums[right] > target is that nums[left] is already the smallest remaining candidate element (any other remaining candidate has index i > left and nums[i] >= nums[left]), so nums[i] + nums[right] >= nums[left] + nums[right] > target for all remaining candidates i > left.

---

## One sample per area

## Generative AI / LLMs  `ai-generative-ai-llms`

*ai - 957 words - 0 problems, 0 real questions*

A large language model is a transformer trained to model a probability distribution over token sequences by predicting each next token given the previous ones. Repeatedly sampling from that distribution produces text, code, or other tokenized outputs. Diffusion models instead generate continuous data such as images and audio by learning to reverse a noising process. Production systems wrap these models with retrieval, tool calls, memory, and safety filters because raw generation is not grounded or guaranteed safe.

## Why interviewers ask this

This question tests whether you know the actual mechanism—attention and next-token prediction—rather than just calling an API. Interviewers probe failure modes such as hallucination, prompt injection, and stale knowledge, and design trade-offs like fine-tuning versus RAG, latency versus quality, and autonomy versus guardrails.

## The core idea

An LLM is a conditional probability model over tokens. Generation quality comes from the learned distribution, but correctness and safety come from the system around the model: retrievers, validators, tool allowlists, and human fallback. Attention makes long contexts powerful but quadratically expensive, so prompt compaction, caching, and chunking are practical concerns. Diffusion models occupy the other major branch of generative AI: they produce high-fidelity continuous data by iterative denoising rather than left-to-right token sampling.

## Key points

- A transformer uses self-attention to compute weighted sums over all tokens, so standard attention cost is O(n^2) in sequence length.
- LLMs are pretrained with next-token prediction, then adapted with instruction tuning and preference optimization such as DPO, which optimizes the gap between chosen and rejected response probabilities.
- Decoding parameters control risk, not truth: greedy chooses the highest-probability token, while temperature and top-p sample from a renormalized distribution.
- RAG retrieves relevant documents at inference time and gives the model that context, reducing hallucination for known content without retraining.
- Prompt injection exploits the fact that the model cannot distinguish trusted instructions from untrusted data; mitigations include structured inputs, allowlists, and output filtering, but no defense is complete.

## Your 60-second answer

A large language model is a transformer trained to predict the next token given all previous tokens. Generating text is just repeated sampling from that conditional distribution. The model learns grammar, facts, and instruction following during pretraining and preference tuning, but it does not query a database at inference time; it outputs statistically plausible continuations, so it can hallucinate. That is why production systems add retrieval, grounding the model in fetched documents, and why any tool call or code execution goes through validation and allowlists. The fundamental trade-off is quality versus cost and latency: longer contexts and larger models give better outputs, but standard attention scales quadratically with sequence length, so you often trade recall in retrieval, compress prompts, or use a smaller model to keep inference practical.

## If they dig deeper

**What does it mean that an LLM predicts the next token, and why does that produce coherent text?**

The model assigns a probability to every token in the vocabulary given the preceding context. Sampling from that distribution repeatedly builds text left to right. Coherence emerges because the model was trained on huge corpora and learned long-range dependencies through self-attention, but the objective maximizes local token likelihood, not global correctness.

**How do temperature and top-p actually change sampling?**

Temperature divides logits before softmax: lower than 1 sharpens the distribution toward high-probability tokens, higher than 1 flattens it. Top-p, or nucleus sampling, keeps the smallest set of tokens whose cumulative probability reaches p and samples only from that set. Both control diversity and determinism, not truth.

**When would you use RAG instead of fine-tuning?**

RAG retrieves relevant chunks and places them in context, so it is best when knowledge changes frequently, provenance is needed, or you want to reduce hallucination without retraining. Fine-tuning is better when the model must internalize a stable style, format, or domain vocabulary, but it is more expensive and its facts still become stale.

**What does DPO do differently from RLHF?**

DPO reparameterizes the RLHF objective so the model is trained directly on preference pairs using a log-probability gap between chosen and rejected responses under the policy versus a reference model. It avoids training a separate reward model and the online optimization loop, but it is sensitive to preference data quality and divergence from the reference.

**Why is prompt injection fundamentally hard to prevent in an agentic LLM system?**

The model processes all text as tokens and has no reliable way to distinguish trusted developer instructions from untrusted content such as a retrieved web page or tool output. Any content can say 'ignore previous instructions,' and the model may comply because that is a plausible continuation. Mitigations like delimiters, input filtering, and tool allowlists reduce risk but are bypassable because the underlying model is still instruction-following over the entire context.

## Worked example

Take logits [2.0, 1.0, 0.1] for tokens A, B, C. At temperature 1.0, softmax gives probabilities of about 0.66 for A, 0.24 for B, and 0.10 for C. At temperature 0.5, the logits become [4.0, 2.0, 0.2], and the probabilities sharpen to roughly 0.86, 0.12, and 0.02, so A almost always wins. At temperature 2.0, the logits become [1.0, 0.5, 0.05], and probabilities flatten to about 0.50, 0.30, and 0.19, so the model explores more. Greedy decoding would choose A in every case. This shows temperature does not add knowledge or fact-checking; it only changes how often lower-probability tokens are sampled.

## Common traps

- Treating temperature as a truth or quality dial; it only changes sampling randomness.
- Using RAG and fine-tuning interchangeably—retrieval grounds, fine-tuning changes behavior.
- Ignoring context length and cost—attention is O(n^2), and prompt tokens are billable.
- Assuming prompt injection is solved by adding a rule that says not to follow instructions in documents.

---

## STAR method  `beh-star-method`

*behavioral - 867 words - 0 problems, 0 real questions*

STAR is a four-part structure for answering behavioral interview questions: the candidate describes the Situation they faced, the Task they needed to accomplish, the Actions they took, and the Results of those actions. It forces an answer to move from context to specific behavior and measurable outcome instead of general claims. Some variants use Target instead of Task to emphasize goals the candidate set for themselves rather than goals assigned externally.

## Why interviewers ask this

Interviewers use behavioral questions to predict future performance from past behavior. STAR answers make evaluation easier because they reveal what the candidate specifically did, why, and whether the outcome mattered. The format also tests whether the candidate can organize a complete story under time pressure without drifting into vague team descriptions.

## The core idea

The point of STAR is not to fill four boxes; it is to make your individual role in a past event unambiguous. A strong answer spends most of its time on Action, because interviewers are evaluating your decisions and execution, not the scenery. Situation and Task should be compressed enough to give context without becoming a story about someone else. Result should tie back to what you did, including lessons learned. Without explicit Action and Result, the story collapses into an opinion or a description of team behavior.

## Key points

- STAR stands for Situation, Task, Action, Result; some organizations use Target instead of Task to emphasize self-set goals.
- The Action component should describe what you specifically did, why, and what alternatives you considered; this is where interviewers extract the most signal.
- Results should include measurable outcomes when possible and what you learned, not just that the project shipped.
- Situation and Task should be limited to the facts a listener needs to understand the Action; over-long context weakens the answer.
- STAR works for questions about past behavior; it is not a natural fit for hypothetical or purely technical questions.

## Your 60-second answer

I answer behavioral questions with STAR: Situation, Task, Action, Result. First I set up the context in two or three sentences—what project or incident I was in and what I was responsible for achieving. Then I spend most of the answer on the action: what I actually did, why I chose that option over the alternatives, and how I carried it out. I close with the result, ideally a measurable outcome, and what I learned. The main trade-off is that STAR can sound mechanical if I label every section out loud, so I keep the labels implicit and make the action the longest part.

## If they dig deeper

**How long should each STAR section be?**

There is no exact rule, but as a guideline Situation and Task combined should be roughly the first quarter of the answer, Action should be half or more, and Result the final quarter. If Action is not the longest section, the answer probably does not show enough individual contribution.

**When should I not use STAR?**

STAR is designed for questions about past behavior, such as 'Tell me about a time when...'. It is less useful for hypothetical questions or questions about your opinions; forcing a past story into a hypothetical answer can sound evasive.

**How do I choose which result to highlight if there were several?**

Pick the result most tightly linked to your own actions and, where possible, one with numbers or verifiable impact. If the result was mixed, state the outcome honestly and add what you learned or changed afterward.

**What if I did not have a formal Task assigned?**

Framing it as Target can show self-direction: describe the problem you saw and the goal you set for yourself. Interviewers ask about tasks to understand your decision criteria, not to check whether a manager assigned the work.

**What is the most common failure mode in Action sections?**

Candidates often describe what the team or 'we' did, leaving the interviewer unable to identify their individual contribution. A strong Action section uses 'I', explains the options rejected, and shows the reason for each decision, not just a chronological list of steps.

## Worked example

A strong answer sounds like: 'In [specific role], I was responsible for [a specific deliverable] when [a specific blocking event] happened. The task was to [get the work done by a concrete date] without [specific cost or risk]. I considered [option A], [option B], and [option C], and I chose [option B] because [specific technical or schedule reason]. I executed it by [specific conversations or changes]. The result was [shipping outcome or measurable change], and I learned [specific process change].' The shape keeps Situation and Task brief, makes the Action the longest part, and ties the Result directly to the candidate's own decision.

## Common traps

- Spending most of the answer on Situation and Task, so the interviewer never learns what the candidate actually did.
- Using 'we' throughout the Action section, making the individual contribution impossible to evaluate.
- Ending with a vague result like 'the project was successful' without a measurable outcome or a lesson learned.
- Memorizing a word-for-word script and reciting it mechanically, which breaks down when a follow-up question changes the detail.

---

## TCP vs UDP  `cs-tcp-vs-udp`

*cs - 1010 words - 0 problems, 0 real questions*

TCP is a connection-oriented transport protocol that presents a reliable, ordered, full-duplex byte stream. It establishes state with a handshake and uses sequence numbers, cumulative acknowledgements, retransmission, flow control, and congestion control. UDP is a connectionless transport protocol that sends independent datagrams with explicit message boundaries; it has no handshake, retransmission, ordering, or congestion control. Its 8-byte header carries ports, length, and a checksum that detects corruption but does not repair it; the checksum is optional over IPv4 and mandatory in IPv6.

## Why interviewers ask this

Interviewers use this to test whether you understand transport-layer tradeoffs, not just acronyms: what guarantees each protocol actually makes, what overhead each imposes, and when real applications should choose one over the other. A strong answer names concrete mechanisms and edge cases such as TCP Fast Open or IPv6 UDP checksums.

## The core idea

TCP and UDP solve opposite problems. TCP turns an unreliable IP network into a reliable ordered byte stream by tracking sequence numbers, acknowledging received data, retransmitting lost segments, and throttling senders with flow and congestion control; this costs latency and state. UDP does almost none of that: it ships self-contained datagrams with message boundaries and lets the application decide whether reliability, ordering, or retransmission are worth adding. The practical rule is not 'TCP is better' but 'retransmitting old data is sometimes worse than losing it'—real-time voice, live game state, DNS, and DHCP typically favor UDP, while files, web pages, databases, and email need TCP's guarantees. QUIC later rebuilt TCP-style reliability over UDP to avoid TCP's head-of-line blocking.

## Key points

- TCP provides a reliable, ordered, full-duplex byte stream using sequence numbers, cumulative ACKs, retransmission, flow control, and congestion control.
- UDP provides message-oriented datagrams with no handshake, no retransmission, no ordering, and no congestion control; its 8-byte header leaves reliability to the application.
- The TCP handshake is SYN, SYN-ACK, ACK; the final ACK may carry application data, and TCP Fast Open allows data in the initial SYN.
- The UDP checksum detects corruption but does not retransmit; it is optional in IPv4 (zero means no checksum) and mandatory in IPv6.
- Classic TCP use cases are HTTP/1.1–2 web traffic, email, file transfer, SSH, and databases; UDP is common for DNS, DHCP, NTP, VoIP, SNMP, and live game state.

## Your 60-second answer

TCP is a connection-oriented protocol that gives you a reliable, ordered byte stream. It pays for that with a three-way handshake, sequence numbers, acknowledgements, retransmission, flow control, and congestion control. UDP is connectionless and message-oriented: each datagram is independent, and the protocol itself gives no delivery or ordering guarantees, so an application that needs reliability must add its own sequence numbers, acknowledgements, and timers. That difference drives protocol choice. Use TCP where missing or reordered bytes break the result, like file transfer, email, databases, and traditional web traffic. Use UDP where retransmitting old data is worse than dropping it: DNS queries, DHCP, NTP, VoIP, and live game state. The core tradeoff is reliability and in-order delivery versus lower protocol overhead and less state per connection.

## If they dig deeper

**What actually happens during the TCP three-way handshake?**

The client sends a SYN with its initial sequence number. The server replies with a SYN-ACK acknowledging that number and carrying its own initial sequence number. The client then sends an ACK; in standard TCP that final ACK can already carry application data, and with TCP Fast Open the client may include data in the initial SYN.

**How does TCP know a segment was lost and how does it recover?**

Cumulative acknowledgements tell the sender which bytes have arrived. A retransmission timer re-sends data when no ACK arrives. Repeated ACKs for the same sequence number can trigger fast retransmit before the timer; selective acknowledgements let the receiver report out-of-order blocks so only missing ranges are retransmitted.

**Why does TCP cause head-of-line blocking?**

TCP exposes one ordered byte stream, so data after a missing segment cannot be delivered to the application until the missing segment is retransmitted and received. That adds latency under packet loss even if later segments have already arrived.

**Does UDP's checksum make it reliable?**

No. The checksum only detects corruption in the datagram; UDP discards bad data and has no retransmission. It is also not always present: IPv4 allows a zero checksum meaning none, while IPv6 requires it.

**How does QUIC change the TCP/UDP decision while still using UDP?**

QUIC builds reliability, congestion control, and encryption over UDP in user space. It supports independent streams so packet loss in one stream does not block another, connection migration, and a faster handshake with 0-RTT and 1-RTT modes, addressing TCP's head-of-line blocking and handshake latency.

## Worked example

Two hosts open a TCP connection: A sends SYN seq=1000. B replies SYN-ACK ack=1001 seq=4000. A sends ACK ack=4001. In standard TCP that third segment can carry the HTTP request; with TCP Fast Open, A could have included the request in the initial SYN. After establishment, A sends 1460 bytes with seq=1001; B ACKs with ack=2461. If that segment is lost, A's retransmission timer expires and it resends starting at seq=1001; later segments cannot be delivered to B's application until the gap is filled. A UDP DNS query has none of this: the client sends one datagram with ports and a query ID; if no matching response arrives, the client times out and retries or contacts another server.

## Common traps

- Saying UDP is always faster ignores that many UDP applications must implement sequence numbers, retransmissions, and timers themselves, which can erase or reverse the protocol-level speed advantage.
- Calling UDP 'unreliable' without qualification is misleading: it does not promise delivery or order, but its checksum can detect corruption and the application decides how to handle loss.
- Claiming TCP cannot send application data until after the three-way handshake ignores that the final ACK may carry data, and TCP Fast Open allows data in the initial SYN.
- Stating that UDP always has a checksum ignores IPv4's zero-checksum case; the checksum is mandatory only in IPv6.

---

## Arrays & Hashing  `arrays-hashing`

*dsa - 1086 words - 10 problems, 0 real questions*

An array is a contiguous block of same-type elements accessed by integer index; read/write by index is O(1), and size is fixed or dynamic depending on the language. A hash map (or dictionary) stores key-value pairs and runs a hash function on the key to pick a bucket, giving average O(1) insert, lookup, and delete when the hash function distributes keys well and collisions are resolved by chaining or open addressing. Hash sets store only keys and are the natural tool for membership tests and duplicate detection.

## Why interviewers ask this

The interviewer is testing whether you recognize that an O(n^2) nested scan can usually be replaced by O(n) hash-map lookups. Two Sum, Contains Duplicate, Group Anagrams, and Top K Frequent all reduce to membership, counting, or grouping once you choose the right key. These are asked at companies such as Bloomberg, Amazon, Netflix, Yelp, and Disney, where working engineers are expected to reach for hashing without being told.

## The core idea

Most array problems have a brute-force solution that compares every element to every other element. A hash map or hash set swaps the inner loop for an O(1) lookup, cutting time from O(n^2) to O(n) and paying O(n) extra space. The difficult part is deciding what to store: an index, a frequency, a canonical string key, or an encoded string. In a one-pass Two Sum, check whether the complement (target - current) exists in the map before inserting the current element. For two-pointer techniques on arrays, sorting changes indices so you must preserve original positions if the problem asks for them. In-place array tricks require precise index mapping, such as abs(val)-1 for values 1..n over a 0-indexed array.

## Key points

- A hash map gives average O(1) lookup but can degrade to O(n) per operation under adversarial collisions; phrase the guarantee as average case unless the hash function is uniformly strong.
- In one-pass Two Sum, check whether (target - current) is already a key; if it is, return the stored index and current index, otherwise store current -> index.
- Detecting duplicates in an array uses a hash set: if the current element is already present, return true; otherwise insert it.
- For problems with values 1..n and a 0-indexed array, map value v to index abs(v)-1 to mark or check it, avoiding out-of-bounds when v == n.
- Group Anagrams can be keyed by sorted characters in O(k log k) per string or by a frequency signature in O(k), where k is maximum string length.

## Your 60-second answer

Arrays give O(1) indexed access, and hash maps give average O(1) key lookup. When a problem asks for pairs, duplicates, or groupings, start by looking for a nested loop you can replace with hashing. For Two Sum, scan the array once: for each element, check whether its complement, target minus current, is already in the map. If it is, you have the pair; if not, store the current element's index. For Group Anagrams, use a canonical key per string such as the sorted characters, and group strings by that key. For Contains Duplicate, insert each element into a set and return true if you ever see an element already there. The trade-off is extra O(n) space, but that is usually acceptable because it buys linear time instead of quadratic. Sorting can reduce space in some problems, but you lose original indices unless you store them.

## If they dig deeper

**What is the time and space complexity of the one-pass Two Sum?**

O(n) time and O(n) space. Each element is checked and inserted at most once, and the hash map holds at most n entries. The average lookup is O(1), assuming a good hash distribution.

**How would you solve Two Sum if you cannot use extra space?**

Sort the array and use two pointers, one at the start and one at the end; move the right pointer left when the sum is too large and the left pointer right when too small. This is O(n log n) for sorting and O(1) extra space, but it returns sorted values, not original indices, so you must keep a copy or pairs if indices are required.

**For Group Anagrams, can you avoid sorting each string?**

Yes. Count character frequencies into a 26-element array for lowercase English letters, then serialize the counts into a fixed string or tuple. Insert each string into a map under that frequency key. This gives O(m*k) time for m strings of length up to k, versus O(m*k log k) with sorting.

**When do hash maps degrade, and what do real implementations do about it?**

With a poor hash function or adversarial keys, many keys land in the same bucket, making each lookup scan that bucket. The worst case is O(n) per operation for chaining. Some language runtimes shrink chains by resizing and rehashing, and a few convert long bucket chains into balanced trees so the worst case becomes O(log n).

**Why is Longest Consecutive Sequence solvable in O(n) if building a sequence seems to require nested loops?**

Put all numbers into a hash set. Only begin extending a sequence from a number when num-1 is absent, which means it is the start of a streak. Every number is part of at most one streak's extension, so the total work across all starts is O(n). The O(1) membership check in the set is what removes the inner loop.

## Worked example

Array [2, 7, 11, 15] with target 9. Start with an empty map. At index 0, current is 2; complement 9 - 2 = 7 is not in the map, so store 2 -> 0. At index 1, current is 7; complement 9 - 7 = 2 is already mapped, so return [0, 1]. Had we checked for current instead of complement while storing complements, the same pair is found, but the keys must consistently match what is checked. The linear pass works because the earlier element was stored before the later element was seen.

## Common traps

- Sorting Two Sum and returning the sorted positions as if they are original indices, when the problem asks for indices in the input array.
- Using value as an index directly in a 0-indexed array for values 1..n; access index abs(v)-1 instead.
- Stating hash map lookups are always O(1); they are average O(1), with O(n) worst case for collisions.
- Forgetting to use immutable or serialized keys for Group Anagrams; a mutable list key can become inconsistent or unhashable.

---

## Collections Framework  `java-collections-framework`

*java - 1052 words - 0 problems, 0 real questions*

The Java Collections Framework is the set of interfaces, implementations, and algorithms in java.util for representing and manipulating groups of objects. Core interfaces include Collection (which extends Iterable) and its subinterfaces List, Set, Queue, and Deque; Map is a separate hierarchy for key-value pairs. Implementations provide concrete storage strategies such as resizable arrays, linked lists, hash tables, and balanced trees. The Collections utility class supplies general-purpose algorithms like sorting, searching, and synchronization wrappers.

## Why interviewers ask this

Interviewers use this topic to test whether you can choose the right data structure for constraints like ordering, duplicates, access pattern, and thread safety. A strong answer shows you know the interface hierarchy, the performance characteristics of common implementations, and the utility methods available, not just class names. It also reveals whether you understand Java's separation of mutable collections from unmodifiable or synchronized views.

## The core idea

The framework separates collection interfaces from their concrete storage strategies. List preserves insertion order and permits duplicates, with index-based access; Set rejects duplicates, with ordering guarantees only from implementations like TreeSet or LinkedHashSet; Map stores unique keys to values. ArrayList gives O(1) random access from an array, while LinkedList gives O(1) insertion at the ends with a doubly linked structure; HashMap and HashSet provide average O(1) lookup by hashing, while TreeMap and TreeSet maintain sorted order at O(log n) via balanced tree. Queue/Deque model FIFO or double-ended processing, with PriorityQueue using a heap to keep the least element at the head. Algorithms in Collections work across implementations because they operate on the interfaces.

## Key points

- Collection is the root interface and extends Iterable; List, Set, and Queue extend it, while Map is a separate key-value hierarchy.
- ArrayList is a resizable array with O(1) random access and amortized O(1) add at the end; LinkedList is a doubly linked list with O(1) insertion/removal at the ends but O(n) access by index.
- HashSet and HashMap use hash tables with average O(1) contains/get/put assuming well-distributed hash codes; TreeSet and TreeMap use red-black trees to keep elements sorted with O(log n) operations.
- PriorityQueue is a heap where the head is the smallest according to natural order or a supplied Comparator; add and poll are O(log n), and it is not thread-safe.
- The Collections utility class provides sort, binarySearch, shuffle, reverse, min/max, unmodifiable and synchronized wrapper views.

## Your 60-second answer

The Java Collections Framework is the set of interfaces, implementations, and algorithms in java.util for managing groups of objects. The root Collection interface extends Iterable and has subinterfaces List for ordered, index-based sequences; Set for unique elements; and Queue/Deque for FIFO or double-ended processing. Map is a separate hierarchy for key-value pairs. Implementations differ mainly in storage and performance: ArrayList uses a resizable array, giving O(1) random access but shifting elements on middle inserts; LinkedList is a doubly linked list, giving O(1) updates at the ends but O(n) traversal by index; HashMap and HashSet use hashing for average O(1) lookup but no iteration order, while TreeMap and TreeSet keep entries sorted with O(log n) operations. The Collections utility class supplies generic algorithms like sort, binarySearch, reverse, and shuffle across these implementations. So when I choose a collection, I match the constraints to the implementation: ordering, uniqueness, access pattern, and thread safety.

## If they dig deeper

**What is the difference between Collection and Collections?**

Collection is the root interface of the framework; Collections is a utility class in java.util containing static methods that operate on or return collections, such as sort, max, unmodifiableList, and synchronizedMap.

**When would you choose HashMap over TreeMap?**

HashMap gives average O(1) get/put and does not maintain order, so it is the default for fast key-value lookup when iteration order is irrelevant. TreeMap keeps keys sorted and provides ordered operations like firstKey, subMap, and ceilingKey, but costs O(log n) per operation.

**How do ArrayList and LinkedList remove or insert in the middle?**

For ArrayList, inserting or removing in the middle requires shifting all subsequent elements, O(n); getting by index is O(1). For LinkedList, once a position is located, insertion/removal is O(1) by adjusting links, but locating that position by index is O(n).

**What is the difference between fail-fast and fail-safe iterators?**

Fail-fast iterators from ArrayList, HashSet, and HashMap throw ConcurrentModificationException if the structure is modified after the iterator is created except through the iterator's own remove. Fail-safe iterators from concurrent collections like ConcurrentHashMap or CopyOnWriteArrayList do not throw; they iterate over a weakly consistent snapshot or the live structure without guarantees of seeing all concurrent updates.

**Explain the internal structure of HashMap and what happens when many keys collide in the same bucket.**

HashMap stores entries in an array of buckets; each key is placed using (n-1)&hash after spreading the hashCode. Collisions are initially chained in a singly linked list; get must traverse that list. In JDK 8, if a bucket's list length reaches 8 and the table has at least 64 buckets, the bucket is converted to a red-black tree, so worst-case lookup in that bucket improves from O(n) to O(log n). When entries are removed and the count drops below 6, the tree is converted back to a linked list.

## Worked example

Create an ArrayList<Integer> and a LinkedList<Integer>, then append integers 0 through 99,999. To retrieve the element at index 25,000, ArrayList computes an offset from the base and reads one array slot; LinkedList starts at the head and follows 25,000 references. To remove the first element, ArrayList would shift the remaining 99,999 elements one position to the left, while LinkedList only updates head to head.next and clears the old node's reference, regardless of list size. This shows why ArrayList is preferred for random access and LinkedList for frequent insertions/removals at the ends.

## Common traps

- Assuming all Set implementations guarantee a predictable order: HashSet does not, LinkedHashSet preserves insertion order, and TreeSet sorts by natural/comparator order.
- Saying Collection and Collections are the same: Collection is a root interface, Collections is a utility class.
- Using PriorityQueue iterator output as a sorted list: only poll/peek respect the priority order; iteration is over the heap array.
- Believing unmodifiableList creates an independent copy: it returns a view backed by the original list, so later changes to the original are visible and the view rejects modifications with UnsupportedOperationException.

---

## Abstraction  `lld-abstraction`

*lld - 1120 words - 0 problems, 0 real questions*

Abstraction exposes a stable public contract for what an operation or component does while hiding how that behavior is implemented. In object-oriented designs, it is usually achieved with abstract classes and interfaces: an abstract class provides common state and default behavior but cannot be instantiated, while an interface specifies method signatures a class must implement. The caller depends on the abstract type rather than a concrete class, so the concrete implementation can change without affecting the caller. In languages without interfaces, the same effect is achieved with pure virtual classes, abstract base classes, or traits.

## Why interviewers ask this

Interviewers use this to test whether you can separate a system's stable contracts from its likely-to-change implementation details, and whether you choose the right OO mechanism for that split. In LLD rounds, abstraction shows up in designing repositories, payment gateways, notification channels, and strategy patterns; the interviewer is looking for reduced coupling and realistic evolution, not class diagrams full of unnecessary interfaces.

## The core idea

At the center of abstraction is the separation of what from how: a component declares the operations callers can rely on, and hides the data structures, algorithms, and external services behind that declaration. A stable contract reduces coupling because callers are written against an interface or abstract base type, not a concrete class. This also enables polymorphism, since several concrete implementations can satisfy the same contract and be substituted at runtime. In LLD, the useful skill is choosing the contract at the right seam: model variation points such as storage backends or payment providers behind an interface, while leaving stable parts concrete. The trade-off is that each layer of abstraction can obscure control flow and performance behavior, so it should be justified by real variation.

## Key points

- An abstract class cannot be instantiated and may define both implemented methods and abstract methods that subclasses must provide.
- An interface defines a contract of method or property signatures; in Java, C#, and similar single-inheritance languages, it carries no instance state, and a class can implement multiple interfaces but extend only one abstract class.
- Concrete callers should depend on the abstract contract, not on a specific implementation, so the implementation can be replaced without changing caller code.
- In C++, a class with at least one pure virtual function is abstract; in Python, ABC and @abstractmethod prevent instantiation until abstract methods are implemented; in Rust, traits define behavior and structs hold data.
- Modern Java interfaces may contain default and static methods, but they still cannot hold per-instance state, so they do not replace abstract classes for shared state and constructors.

## Your 60-second answer

Abstraction means exposing a stable contract while hiding the implementation behind it. In a design discussion, I'd separate what a component does from how it does it by introducing an abstract class or interface. An abstract class cannot be instantiated and can share state and default behavior across subclasses. An interface defines a behavioral contract with no instance state, and a class can implement several interfaces. The caller holds a reference to the abstract type, so at runtime the concrete object can be swapped without changing the caller. The reason this matters is testability and evolution: replacing a payment gateway or storage backend becomes a wiring change, not a business logic change. The trade-off is indirection; I only abstract a seam when there are at least two real implementations or a clear known variation point.

## If they dig deeper

**What is the difference between an abstract class and an interface?**

An abstract class can have instance fields, constructors, and implemented methods, and a class can inherit from only one abstract class. An interface usually defines only method/property signatures and has no instance state, and a class can implement many interfaces. An abstract class models a shared base; an interface models a capability contract.

**When would you choose an abstract class instead of an interface?**

Use an abstract class when the subclasses share common state, constructors, or a protected helper method and form a genuine is-a hierarchy. Use an interface when unrelated classes need the same behavior or when you need multiple type contracts. A common pattern is an interface for the public contract plus an abstract base class that provides a reusable partial implementation.

**How does abstraction help with unit testing?**

When production code depends on an interface or abstract type, tests can inject a fake or mock implementation instead of a real database, HTTP client, or gateway. This isolates the unit under test and avoids network latency and external side effects. It also lets you simulate failures such as timeouts or exceptions deterministically.

**How do you decide how much abstraction to introduce in an LLD design?**

I look for variation points that already have more than one behavior or are explicitly required to change, such as payment providers, notification channels, or storage backends. I define an interface around those seams and keep stable parts concrete. I avoid speculative abstraction because it adds boilerplate and hides control flow without immediate benefit.

**What is a leaky abstraction, and how do you avoid it?**

A leaky abstraction is when implementation details or constraints, such as blocking I/O, transaction boundaries, or provider-specific failures, cannot be hidden by the contract. To avoid it, the abstraction should model these realities, for example by returning failure envelopes or declaring async behavior, rather than pretending all implementations behave identically. This keeps callers from making false assumptions about latency and atomicity.

## Worked example

Consider designing a checkout service where payments may be processed by Stripe, Razorpay, or a mock gateway. Define a PaymentProcessor interface with one operation, processPayment(amount), and make StripePaymentProcessor and RazorpayPaymentProcessor implement it. The checkout service stores a PaymentProcessor reference provided at construction; when a customer pays 100 units, it calls processor.processPayment(100). The Stripe implementation hides token refresh, idempotency key generation, and retry logic inside its method; Razorpay hides a different protocol. Adding a new provider requires writing a new implementation and changing only the composition that injects it, not the checkout logic. If the team decides to retry exactly two times before surfacing an error, that change stays inside one implementation. The caller still sees a single method call.

## Common traps

- Equating abstraction with encapsulation; encapsulation hides fields behind accessors, while abstraction defines what callers can do without exposing how.
- Introducing an interface for every class before a second implementation exists, which creates indirection with no current benefit.
- Naming the abstraction after the implementation, such as MySQLUserRepository, so callers still depend on the storage technology.
- Assuming an interface can never contain code; Java interfaces can have default and static methods, but they cannot hold per-instance state.

---

## Indexes  `sql-indexes`

*sql - 1203 words - 0 problems, 0 real questions*

An index is a separate data structure, usually a B-tree, that stores a sorted copy of one or more table columns along with pointers to the corresponding rows. The database engine uses it to locate rows in logarithmic page accesses instead of scanning the whole table. A clustered index determines the physical order of table rows and stores the row data at the leaf level; a nonclustered index is a separate structure whose leaves point back to the table's clustered key or a row locator. Indexes can also enforce uniqueness and support filtered subsets of rows.

## Why interviewers ask this

Interviewers ask about indexes to test whether you understand how the physical design of a schema affects query performance, not just SQL syntax. A strong answer shows you can reason about when a particular index helps, how key order changes what predicates can seek, and what maintenance cost it adds. They are checking whether you can design a schema for real workloads rather than adding indexes blindly.

## The core idea

An index is a sorted copy of selected columns. For an equality lookup, the engine descends a B-tree from root to leaf to find the first matching key, then scans forward while keys match. For a clustered index, the leaf pages are the actual data pages, so there is only one per table and it defines physical order. For a nonclustered index, the leaf stores the index key and a locator—either the clustered key or a heap row ID—so queries needing other columns must perform a key lookup. Composite keys are ordered left to right, so an index on (a, b) supports lookups on a and on a plus b, but not on b alone in a typical B-tree. Because every inserted, updated, or deleted row must also update each affected index, indexes are a trade-off between read and write speed.

## Key points

- A B-tree index allows equality and range lookups in O(log n) page accesses instead of a full table scan.
- A table can have only one clustered index because the data rows can be physically sorted in only one order.
- A nonclustered index is a separate structure; if a query needs columns not covered by the index, the engine performs an extra key lookup to the clustered index or heap.
- For a composite index on (a, b), predicates that filter on a can seek, but predicates on b alone usually cannot use the index efficiently because b is not the leading key.
- Indexes increase write latency and storage because inserts, updates, and deletes must maintain the index structures.

## Your 60-second answer

An index is a separate data structure that keeps a sorted copy of one or more columns and pointers to the actual rows. The common implementation is a B-tree, so the engine can find a specific key by walking from the root to a leaf in a few page reads instead of scanning the entire table. There are two main types. A clustered index determines the physical order of the table's rows and stores the row data in its leaves, so a table can have only one. A nonclustered index is separate, and its leaves point to the clustered key or a row locator. That means a query may have to do an extra key lookup when it asks for columns not included in the index. The trade-off is write cost: every insert, update, or delete must also modify each relevant index, and the indexes take up storage. So you add indexes to support the queries you actually run, not every column.

## If they dig deeper

**What is the difference between a clustered and a nonclustered index?**

A clustered index defines the physical order of table rows and contains the row data at its leaf level, so each table can have only one. A nonclustered index is a separate B-tree that stores the indexed key values and a locator back to the table; a table can have many. Nonclustered lookups may require an additional lookup if the index does not cover the query.

**Why can adding an index make writes slower?**

The database must update the index structure whenever the indexed columns change or rows are inserted or deleted. This adds work to every write transaction and can cause page splits, logging, and lock contention. Secondary indexes multiply this cost because each affected index must be maintained.

**How does column order matter in a composite index?**

A B-tree index on (a, b) sorts rows by a first and then by b. The engine can seek when a predicate provides a value for a, including a range on b after a fixed a. A predicate on b alone generally cannot use an index seek because b is not the leading key, though some engines may perform an index skip scan.

**What is a covering index and why does INCLUDE help?**

A covering index is one that contains all columns a query needs, so the engine can answer it entirely from the index without going back to the table. Key columns are part of the sort order and search path, while INCLUDE columns are stored only at the leaf level, which keeps the index smaller while still avoiding key lookups.

**How does a filtered index work and why must the query predicate match it?**

A filtered index stores only the rows that satisfy a WHERE clause, so it is smaller and cheaper to maintain for sparse subsets such as active rows or non-NULL values. The optimizer can consider it only when the query's predicate logically matches or is implied by the filter, because rows outside the filter are not in the index. If the filter is not present in the query, the index cannot guarantee it has all relevant rows.

## Worked example

Consider an orders table with a composite index on (customer_id, order_date). A query with WHERE customer_id = 42 AND order_date >= '2025-01-01' can seek directly to the first entry for customer 42 and then read only that customer's entries in date order through the leaf pages. The engine never scans rows for other customers. If the query instead filters only on order_date = '2025-01-01', that same index is not a seek candidate in a typical B-tree because order_date is the second key; the leading customer_id is absent. The database would likely scan the whole index or table, depending on the optimizer. This shows why the leading column of a composite index should be the one used in equality or range predicates for the workload.

## Common traps

- Adding an index to every column in a query: it slows writes and increases storage while many indexes remain unused.
- Assuming a composite index on (a, b) will speed up a query that filters only on b; the leftmost key order prevents a normal seek.
- Ignoring the key lookup after a nonclustered index seek; an index may look selective but still be slow if the query retrieves many uncovered rows.
- Confusing a clustered index primary key with uniqueness; a clustered index defines physical row order and does not have to be unique or the primary key unless declared.

---

## Caching  `sd-caching`

*system_design - 1051 words - 0 problems, 3 real questions*

Caching stores a subset of data transiently in a faster storage location—browser memory, CDN edge nodes, in-process RAM, or a distributed key-value store such as Redis—so subsequent reads can be served without going to the origin database or object store. A lookup is a hit when the key is present and fresh; a miss triggers fetching from the source and writing the result into the cache. It relies on the locality-of-reference principle: recently or frequently requested data is likely to be requested again. Caches trade capacity and consistency for speed, so entries need expiration or explicit invalidation.

## Why interviewers ask this

In design problems, interviewers probe caching when you choose between CDN and edge caching for video, set TTLs for expiring pastes, or place a control-plane cache in front of a database. They are testing whether you know not just 'add Redis' but where the cache belongs, what data to store, how to invalidate it, and how to reason about hit ratio, staleness, and cache stampede. A vague answer that caching reduces latency without a placement and invalidation plan is a weak signal.

## The core idea

The core mechanism is a lookup path: check the cache, return the value on a hit, otherwise read from the slower source, populate the cache, and return. Cache utility depends on read-heavy workloads, skewed hot keys, and tolerance for stale reads. You choose location by distance from the requester: browser HTTP cache, CDN edge, app-server RAM, distributed cache, database buffer pool. The hard part is invalidation and consistency: TTLs bound staleness, explicit invalidation removes entries on writes, and write-through or write-back controls when writes propagate. Caches also introduce thundering herd risk when popular keys expire at the same time.

## Key points

- A cache stores a subset of data transiently in faster storage and serves reads without hitting the source of truth.
- Cache hit ratio depends on access pattern, TTL, and eviction policy; LRU is common for bounded in-memory caches.
- TTL is the simplest freshness bound: after the TTL expires, the entry is treated as stale and refetched from the source.
- Redis and Memcached are distributed in-memory key-value caches that decouple cached data from any single app instance.
- CDNs push cached static content to edge nodes near users, lowering geographic latency and origin load for reads.

## Your 60-second answer

Caching means keeping a copy of frequently read data in a faster layer closer to the requester, so a request does not have to reach the database or origin every time. On a read, check the cache: if the key is present and within its TTL, return it; otherwise fetch from the source, store the result, and return it. This reduces latency and database load when reads dominate writes and some keys are hot. The main trade-off is consistency: if the underlying data changes before the TTL expires, clients can receive a stale value, so the cache needs TTLs, invalidation on writes, or both. A bounded cache also needs an eviction policy such as LRU, and you must handle thundering herds when hot keys expire.

## If they dig deeper

**Where can you place a cache in a typical read-heavy service, and how do you decide the first place to add one?**

Browser HTTP caching for per-user responses, CDN for public static assets, in-memory caches for hot service data, and distributed stores like Redis for data shared across instances. Start where latency and backend load are highest and data has reuse; often a CDN for public content or Redis in front of the database for hot rows.

**How do you invalidate a cached item when the underlying database write changes it?**

Use TTL for an upper bound, or explicitly delete or update the key in the same code path that writes to the database. For stronger consistency, update the cache after the database commit and accept that readers may see old data until invalidation completes. Cache-aside with short TTL or event-driven invalidation is a common practical design.

**Would you use a CDN or edge caching for global video delivery, and what does it actually cache?**

Use a CDN for high-volume, relatively immutable video segments after encoding. The CDN caches segments at points-of-presence near users, so playbacks are served from the edge instead of origin object storage. Request routing sends each client to a nearby edge; cache misses fall back to the origin and populate the edge cache.

**How do you stop a thundering herd when a hot key expires?**

The expiration can make thousands of concurrent requests all miss and query the origin simultaneously. Use request coalescing or locking so one request recomputes and others wait, or use probabilistic early refresh to refresh hot keys before expiry, or serve stale data briefly while refresh occurs.

**How do you design a distributed cache that stays available and balanced when nodes join or leave?**

Use consistent hashing to map keys onto cache nodes, with replication for availability. If a node fails, its keys map to other nodes causing misses, but the database of record remains durable. Redis Cluster uses 16384 hash slots assigned to masters with replicas, so resharding moves slots rather than the entire dataset.

## Worked example

Suppose a read-heavy service has a product page fetched 5,000 times per second, but the relational database can sustain only 800 reads per second. Put Redis in front with LRU and a 30-second TTL. The first request misses, reads the database, and stores the serialized object under product:123. Subsequent requests hit Redis until the TTL expires or an update invalidates the key. The database then sees about one read per 30 seconds for that key instead of 5,000 per second, and reads are served from RAM with lower latency. If the database changes the price during that 30-second window, clients still receive the old price unless the write path deletes product:123.

## Common traps

- Reaching for Redis before identifying a hot, read-heavy dataset; caching random keys wastes memory and adds an extra hop.
- Treating the cache as durable storage; writes only to cache are lost if the node restarts.
- Setting a long TTL without invalidation on writes, which lets stale data leak to users.
- Letting hot keys expire simultaneously without coalescing refreshes, which can stampede the database.

---
