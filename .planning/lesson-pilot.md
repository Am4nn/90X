# Lesson pilot - 5 topics

Generated 2026-09-27. Read these and tell me what is wrong with them.

## RAG and Production Systems  `ai-rag-and-production-systems`

*572 words, 5 sources, contract: none*

Retrieval-augmented generation (RAG) is an architecture that first retrieves relevant documents or data snippets from a knowledge base, then passes them to a language model to generate a grounded response. Production RAG systems add deployment practices such as routing traffic between identical environments to roll out new versions without downtime. The result is a system that can answer questions, summarize, or converse using up-to-date external information.

## Why interviewers ask this

Interviewers want to see whether you understand how to make LLM outputs reliable by grounding them in retrieval rather than relying only on parametric memory. They also test whether you can improve retrieval quality and deploy changes to a live system safely. The question probes both model architecture and production engineering.

## The mental model

Think of RAG as a two-stage pipeline: a search engine narrows a large corpus to a few relevant passages, and a language model acts as an editor that writes an answer using only those passages as evidence. Production deployment adds a traffic switch: keep the old version fully running while the new version is tested, then move users over atomically. When answers are wrong, first inspect retrieval precision and recall, then generation faithfulness; improving search often gives the largest gain. When retrieval misses, combine keyword matches with embedding similarity and re-rank the merged candidates.

## Key points

- RAG retrieves relevant information from a knowledge base and conditions the language model on that information to produce grounded responses.
- Generation uses the retrieved text plus the model's language ability to create coherent, context-aware output rather than answering from memory alone.
- Retrieval quality is usually the bottleneck; common improvements include hybrid search, re-ranking, query rewriting, and better embeddings.
- Blue-green deployment runs old and new versions in parallel and switches traffic after the new version passes testing, avoiding downtime.
- Evaluation should combine retrieval metrics such as recall and precision with generation quality and task-specific success criteria.

## Worked example

Suppose a support chatbot handles 10,000 product questions. A pure LLM answers 65% correctly from memory. After adding RAG, the retriever returns the correct FAQ passage in the top 3 for 80% of queries. Since generation uses the retrieved passage, end-to-end correct answers rise to 78%. To roll out the improved retriever, the team runs the old blue version and new green version side by side, sends 5% traffic to green, measures 12% fewer wrong answers, then switches 100% traffic to green with no downtime.

## Common traps

- Treating RAG as a reasoner: it cannot compensate for bad retrieval; if the right passage is not returned, the model often cannot recover.
- Evaluating only generation quality and ignoring retrieval recall, precision, or latency, which hides the real bottleneck.
- Switching all traffic to a new model at once without a staged rollout or rollback path, causing user-facing failures.
- Assuming one retriever is enough instead of combining lexical and semantic search or re-ranking candidates.

## You should be able to answer

- What two main stages make up a RAG pipeline and what does each stage do?
- Why does RAG produce more up-to-date and factual answers than a standalone language model?
- What is blue-green deployment and how does it reduce downtime during a model update?
- What are the most common places to look when a RAG system gives inaccurate answers?
- How does hybrid search improve retrieval over keyword-only or embedding-only search?

---

## Teamwork  `beh-teamwork`

*462 words, 0 sources, contract: none*

Teamwork is the ability to work with others toward shared goals, including communication, conflict resolution, shared accountability, and adapting to others' working styles. In behavioral interviews, candidates prove it by describing specific situations where they contributed to or led a group effort. Interviewers evaluate how the candidate helped the team succeed, not just whether they were present. Strong answers show awareness of others' contributions and trade-offs.

## Why interviewers ask this

Interviewers ask teamwork questions to test whether you can operate effectively with diverse people, handle disagreement, and put team outcomes above personal credit. They want evidence you won't be a bottleneck or source of friction. Past behavior predicts future collaboration.

## The mental model

Think of teamwork as a system where the team's output is the product, and you are one component whose value comes from making the whole system work. When answering, structure the story around the team's objective, your specific role, interactions with others, and the result. Use a simple framework: situation, task, action, result (STAR), but focus the 'action' on what you did with or for others. This helps avoid rambling and keeps the interviewer able to follow your contribution.

## Key points

- Use specific examples with a clear shared goal and your individual role in achieving it.
- Highlight how you communicated, handled disagreement, or supported a teammate, not just the final outcome.
- Give credit to others and describe the group's result, not only your personal achievement.
- Use the STAR structure to keep the story concise and easy to follow.
- Choose examples where the team faced a real challenge and your actions influenced the collaboration.

## Worked example

A strong answer sounds like: 'In a previous role, our team needed to fix a recurring production issue. I proposed we pair a senior and junior engineer to investigate, and I volunteered to coordinate updates with the support team. We resolved the issue in two days, and the junior engineer later said the pairing helped them learn the system.'

## Common traps

- Claiming credit for the whole result without mentioning what others contributed.
- Choosing a story where you worked mostly alone and calling it teamwork.
- Describing conflict but saying only that you avoided it, rather than how you addressed it.
- Reciting generic platitudes like 'I'm a team player' without a concrete situation.

## You should be able to answer

- What is the purpose of asking teamwork questions in an interview?
- How should you structure a teamwork story to keep it concise?
- What specific elements make a teamwork example stronger than a solo achievement?
- What mistake should you avoid when describing conflict in a team?
- Why is it important to mention others' contributions in a teamwork answer?

---

## HTTP/HTTPS  `cs-http-https`

*562 words, 12 sources, contract: none*

HTTP is an application-layer protocol built on TCP that defines how clients and servers exchange request and response messages, using port 80 by default. HTTPS is the secure version that wraps HTTP in TLS/SSL encryption, using port 443 by default. Each message has a start line, headers, and an optional body; responses include a status code such as 200, 400, or 500.

## Why interviewers ask this

Interviewers use HTTP/HTTPS to test whether you understand web communication fundamentals: the difference between plaintext and encrypted transport, how a request-response cycle works, and why the protocol is designed to be stateless. They also probe API design through status codes, headers, and authentication requirements.

## The mental model

Think of HTTP as a conversation of independent postcards: each request is a complete, self-contained message asking for or submitting information, and the server responds without remembering earlier postcards. HTTPS puts those postcards in a sealed, tamper-evident envelope, so an observer can see the endpoints but not the contents. Every request has a verb and a target; every response has a status code that tells you whether the card was delivered, rejected, or mishandled. Statelessness means each postcard must contain everything needed, such as authentication headers, because no shared memory is assumed.

## Key points

- HTTP is stateless: each request is independent and must carry all information needed for the server to process it.
- An HTTP request has a start line with method and target, headers, an empty line, and an optional body.
- Status codes are grouped by class: 2xx success, 3xx redirect, 4xx client error, and 5xx server error.
- HTTPS adds TLS/SSL encryption on top of HTTP, using port 443 by default instead of HTTP's port 80.
- TLS provides confidentiality, integrity, and authentication, protecting data from eavesdropping and tampering.

## Worked example

A client sends POST /orders HTTP/1.1 with Host: api.example.com, Content-Type: application/json, and Authorization: Bearer abc123. The body is { "items": [{"sku":"A1","qty":2}] }. The server creates order id 123 and responds HTTP/1.1 201 Created with Content-Type: application/json and Location: /orders/123, body { "id": 123, "status": "pending" }. Because HTTP is stateless, the client must repeat the Authorization token on the next request; the server does not remember it. If the same request is sent over HTTPS, the TLS handshake first negotiates encryption with api.example.com on port 443, so the token and order data cannot be read in transit.

## Common traps

- Confusing 'stateless' with 'no state anywhere': state can live in cookies or tokens, but the protocol itself does not maintain a session between requests.
- Saying HTTPS is only encryption and forgetting that TLS also provides integrity and server authentication.
- Assuming HTTPS hides the destination IP or port; observers can still see the host, packet size, and timing, though not the message contents.
- Returning 200 OK for every response, even errors; a validation failure should be 400, not 200 with an error field in the body.

## You should be able to answer

- What are the main components of an HTTP request and an HTTP response?
- Why is HTTP called stateless, and what does that require from a client?
- What are the default ports for HTTP and HTTPS?
- What security guarantees does TLS add to HTTP?
- Which status code should be returned for a validation error and for a missing resource?

---

## HashMap internals  `java-hashmap-internals`

*652 words, 9 sources, contract: none*

HashMap is a hash-table-based Map implementation that stores key-value pairs in an internal array of buckets. It uses the key's hashCode() to compute a bucket index and stores a Map.Entry object containing the key and value. Collisions are handled by chaining entries in the same bucket; from Java 8 onward, a chain longer than 8 entries is converted to a balanced tree. When a duplicate key is put, its old value is replaced and returned; the internal array is resized when the number of entries passes a load-factor threshold.

## Why interviewers ask this

An interviewer asks this to see whether you understand how HashMap achieves average O(1) operations and when it degrades. They want to know that you can reason about hashCode, equals, bucket selection, and the cost of collisions. This reveals whether you can choose appropriate keys and avoid performance surprises.

## The mental model

Think of a HashMap as a filing cabinet with numbered drawers. The key's hash code chooses a drawer, but keys are not guaranteed unique drawers. Inside a drawer, entries are stored as a list or tree; to retrieve, you go directly to the drawer and then scan the contents using equals. This is why a good hash function spreads keys across drawers and a bad one turns the cabinet into one long list. Resizing is like moving to a bigger cabinet with renumbered drawers; existing entries are rehashed to new drawers.

## Key points

- HashMap stores entries in an internal bucket array and computes the bucket index from the key's hashCode(), giving average O(1) get and put operations.
- A collision occurs when two different keys map to the same bucket; before Java 8 the bucket held a linked list, making worst-case operations O(n).
- In Java 8, a bucket's linked list is replaced by a balanced tree when the number of entries in that bucket exceeds 8, reducing worst-case lookup from O(n) to O(log n).
- Lookup first finds the bucket by hashCode, then uses equals() to identify the exact key within the bucket chain or tree.
- Resizing occurs when the entry count exceeds the load factor times the current capacity; it creates a larger bucket array and redistributes existing entries.

## Worked example

Consider a HashMap with an internal array of size 4 and a key class whose hashCode returns the string length. Keys 'a' and 'b' both hash to 1, so they collide in bucket 1. After put(new Key("a"), 10), bucket 1 contains a node for key 'a'. After put(new Key("b"), 20), bucket 1 becomes a linked list: ['a' -> 'b']. A get(new Key("b")) computes hashCode 1, goes to bucket 1, then calls equals on each node's key until it matches 'b', returning 20. If the bucket had more than 8 entries under Java 8, the linked list would be converted to a balanced tree to keep lookups at O(log n).

## Common traps

- Assuming every distinct key gets its own bucket and forgetting that collisions can make operations linear or logarithmic rather than constant.
- Overriding equals() but not hashCode(), which breaks HashMap because two equal keys can hash to different buckets and be treated as absent.
- Thinking Java 8 always uses a tree for collisions; small collision chains remain linked lists until the threshold is exceeded.
- Ignoring that duplicate keys replace values and return the previous value, which can hide overwritten data if the return value is not checked.

## You should be able to answer

- How does HashMap compute the bucket index for a key?
- What happens internally when two keys collide in the same bucket?
- How does Java 8 improve the worst-case lookup time for heavily colliding buckets?
- What role does equals() play during a get() operation after the bucket has been found?
- What triggers a resize, and what happens to existing entries when the bucket array grows?

---

## CAP theorem  `sd-cap-theorem`

*677 words, 12 sources, contract: none*

The CAP theorem, also called Brewer's theorem, says a distributed data system can provide at most two of three guarantees at once: consistency (every read gets the latest write or an error), availability (every request gets a non-error response, though it may be stale), and partition tolerance (the system keeps operating despite lost or delayed messages between nodes). Since real networks can always partition, partition tolerance is effectively required, so the live design choice is between consistency and availability when a partition happens.

## Why interviewers ask this

Interviewers use CAP to see whether you can reason about distributed data trade-offs and classify databases. They want to know if you understand that no distributed system can give perfect consistency and perfect availability during a network partition. They also test whether you can choose between CP and AP behavior for a concrete product, such as banking versus social media.

## The mental model

Imagine a network partition as a cut separating two groups of nodes. A write arrives on one side. The system can either accept it immediately and risk the other side reading old data, which is availability, or refuse the write/timeout until both sides can agree, which is consistency. Partition tolerance is already forced by the unreliable network, so you are really choosing only between consistency and availability during the failure. Outside a partition, the same system can provide both consistent reads and fast responses. Remember it as: pick P first, then choose C or A when the network splits.

## Key points

- CAP means a distributed system can guarantee at most two of consistency, availability, and partition tolerance at the same time.
- Network partitions are unavoidable in real distributed systems, so partition tolerance is usually mandatory and the real trade-off is between consistency and availability during a partition.
- The CAP trade-off applies only when a partition occurs; outside partitions, a system can provide both consistency and availability.
- CP systems reject requests or return errors during a partition to avoid stale or conflicting data, while AP systems keep serving requests even if some responses are stale.
- CAP is not a complete database selection guide; latency, consistency model, operational needs, and other properties also matter.

## Worked example

Consider two replicas of a bank account with a balance of $100, split by a network partition into node A and node B. A client deposits $50 to node A. A CP banking system cannot replicate the write to node B, so node A rejects the write or times out instead of confirming success, preserving a single known balance. An AP social feed in the same situation accepts the write on node A and returns success to the poster immediately, storing the new post locally. A second user reading from node B during the partition may still see the old feed without the new post. Once the partition heals, node A synchronizes to node B, and both sides show the new post. The CP system chose consistency and sacrificed availability; the AP system chose availability and accepted temporary staleness.

## Common traps

- Claiming a system must permanently abandon either consistency or availability; the trade-off only applies during a network partition.
- Treating CA as a realistic distributed option; a truly distributed system cannot ignore network partitions, so CA only describes single-node or non-distributed setups.
- Assuming an available response contains the latest data; availability only promises a non-error response, not freshness.
- Choosing a database solely by its CAP label; real database selection depends on many more properties such as latency, data model, and operational behavior.

## You should be able to answer

- What do consistency, availability, and partition tolerance mean in the CAP theorem?
- Why is partition tolerance considered effectively mandatory in a real distributed system?
- What exact trade-off does a system face when a network partition occurs?
- How does a CP system behave differently from an AP system during a partition?
- Why is CAP alone not enough to decide which database to use for a product?

---
