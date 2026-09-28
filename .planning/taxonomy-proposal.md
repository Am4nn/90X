# Proposed taxonomy cut

You asked me to propose and you to approve. This is my read of the 94-item
shortlist in `taxonomy-gaps.md`, against the 274 topics 90x already has.

**To approve: delete any line you don't want and tell me.** What survives gets a
lesson written at about $0.04 each, through the same contract, fact check and
answerability gates as the existing 274.

**Recommendation: write 46.** Struck: 27 we already cover under another name,
and 7 that are ML-specialist maths rather than SDE-interview material.

---

## Strike — we already have these (27)

Exact-name matching missed them because the names differ slightly. Your
reviewer was right that this was happening; these are what is left of it.

| Candidate | We already have |
|---|---|
| ACID (0.9) | ACID Properties `cs-acid-properties`, ACID vs BASE `sd-acid-vs-base` |
| Transactions (0.9, ×3 areas) | Transaction Isolation Levels, Distributed transactions |
| REST (0.8, ×2) | REST API `sd-rest-api` |
| Sharding (0.8, ×2) | Database sharding, Sharding strategies |
| Load Balancer (0.8) | Load balancing, Layer 4 vs Layer 7 |
| OAuth2 (0.7) | OAuth 2.0 `sd-oauth-2-0` |
| GoF Design Patterns (0.8) | Design Patterns `lld-design-patterns` |
| BASE (0.7) | ACID vs BASE |
| Array / Arrays (0.9, ×3) | Arrays & Hashing `arrays-hashing` |
| Heap (0.9, ×2) | Heap / Priority Queue |
| Queue / Queues (0.9, ×4) | Heap / Priority Queue, Message queues |
| Indexing (0.8) | Indexes `sd-indexes`, `sql-indexes` |
| Array vs ArrayList (0.8) | ArrayList vs LinkedList `java-arraylist-vs-linkedlist` |
| RAG vs Fine-tuning (0.85) | RAG and Production Systems, Supervised Fine-Tuning |
| Fine-Tuning vs Prompt Engg. (0.75) | same two |

## Strike — ML-specialist maths, not an SDE loop (7)

You said not to remove anything we already have, and I haven't. These are only
about what to *add*. You already hold 50+ AI topics and 411 AI cards; a backend
loop asks about RAG and serving, not about Hessians. Say the word if you want an
ML track and these come straight back.

- Chain rule of derivation (0.8)
- Derivatives, Partial Derivatives (0.8)
- Matrix & Matrix Operations (0.8)
- Gradient, Jacobian, Hessian (0.75)
- Scalars, Vectors, Tensors (0.75)
- Singular Value Decomposition (0.7)
- Linear Regression / Logistic Regression (0.7) — borderline; keep if you want
  classical-ML questions, strike if your loops are backend

---

## Write — behavioural (10)

The best value on the list. All are asked directly, none exist yet, and
behavioural lessons need no engine or version caveats.

- Production issues management (0.9)
- Incident Management (0.7) and Post-incident analysis (0.7) — consider one lesson
- Code Review Best Practices (0.8)
- Critical situation leadership (0.8)
- Stakeholder management (0.8)
- Stress management (0.8)
- Cross-functional Collaboration (0.7)
- Scope Management (0.7)
- Trust / Influence Building (0.7)

## Write — DSA named fundamentals (12)

A judgement call worth stating plainly: 90x covers DSA as **patterns**
(`arrays-hashing`, `trees`, `graphs`), not as named structures and algorithms.
An interviewer does ask "explain BFS versus DFS" and "what is the complexity of
quicksort" directly, and no current lesson answers those as its subject.

- Breadth First Search (1.0), Depth First Search (1.0)
- Big O / Asymptotic Notation / Big-Theta (0.9) — one lesson
- Time vs Space Complexity (0.9) and Algorithmic Complexity (0.8) — one lesson
- Hash Table (0.9)
- Binary Tree (0.9) and Binary Search Tree (0.9) — one lesson
- Merge Sort (0.9), Quick Sort (0.9), Heap Sort (0.7) — one lesson on sorting
- Adjacency List (0.8) and Adjacency Matrix (0.8) — one lesson on representation
- Directed / Undirected Graph (0.9) — one lesson
- Prim's Algorithm (0.9) and Spanning Tree (0.7) — one lesson on MST
- Recursion (0.8)
- Bitwise Operators (0.7)

Strike if you'd rather keep DSA purely pattern-shaped: Full Binary Tree, AVL
Trees, Balanced Search Trees, Insertion Sort, Selection Sort, Pre/Post-Order
Traversal, Knuth-Morris-Pratt, Rabin-Karp, Huffman Coding, Knapsack, and the
three near-duplicate string-search entries. They are real topics but a 90-day
plan does not need them, and several are already inside pattern lessons.

## Write — system design and backend (12)

- Horizontal vs Vertical Scaling (0.9)
- SQL vs NoSQL Databases (0.8)
- Schema Design Patterns / Anti-patterns (0.8)
- Webhooks vs Polling (0.8)
- TCP/IP Stack (0.8) — distinct from our OSI model lesson
- Error Handling / Retries (0.7)
- HTTP Versions (0.7)
- Leader Election (0.7)
- Serverless Concepts (0.7)
- MVCC (0.7)
- Soft Links / Hard Links (0.7)
- Understand TCP / IP (0.7) — fold into TCP/IP Stack

## Write — Java and Spring (8)

- Pass by Value / Pass by Reference (0.9)
- Virtual Threads (0.8)
- Spring IOC (0.8), Spring MVC (0.8), Spring AOP (0.7)
- Authorization (0.7) — authn versus authz
- JWT Authentication (0.7)
- Composition over Inheritance (0.8)
- Repositories (0.7)

## Write — applied AI (4)

- Prompt Injection (0.7) — named in two lessons but taught in neither as its
  own subject, and it is the LLM security question that gets asked
- Bias and Fairness (0.8)
- Conducting adversarial testing (0.7)

---

## If you approve all of it

46 lessons at roughly $0.04 each is about **$2**, plus cards at roughly $0.02 a
topic, so **under $3 in total**. That takes 90x from 274 topics to 320.

My own view: the behavioural ten and the Java/Spring eight are the clearest
wins, because they are asked constantly and nothing covers them. The DSA twelve
are the ones to think hardest about — they may duplicate what your pattern
lessons already teach, and you are the one who has read those.
