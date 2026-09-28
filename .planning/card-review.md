# 90x card review

2808 cards are ready to publish. An automated gate read 2813 and objected to 108 of them (4%): 103 were rewritten and passed on the second look, 5 could not be saved and were dropped (0%). Mix: 1383 typed, 768 mcq, 598 flash, 59 output.

## What these are

90x is an interview-prep app. Each topic has one authored lesson, and cards are generated from that lesson to test recall. A reader answers a card **without** the lesson in front of them: typed answers are graded by a model against the listed key points, multiple choice by the marked option, and output cards by exact match.

## What to judge

1. **Could a competent engineer who studied this lesson answer this, with nothing else in front of them?** A card that needs the lesson open is broken, however good it looks beside it.
2. **Is the format right?** Typed for explanation and trade-offs, flash for one crisp fact, multiple choice where the options matter, output where a snippet has one unambiguous result.
3. **Are the key points gradable?** They are what a model checks a typed answer against.
4. **Are the wrong options real mistakes?** A distractor nobody would pick makes the card a reading test.
5. **Was the gate right?** The rejected cards are at the end with its reasons. It has been wrong before: an earlier version rejected 40 good cards out of 42 because it misread conceptual questions as malformed.

Below: 25 cards, spread across areas and formats, weighted toward the ones the gate was least sure about. Each is shown with the lesson it came from.

---

## 1. Design · flash · Easy

*dsa · gate confidence 0.8*

<sub>to object to this card: `## design` then `match: In DSA interviews, what kind of problem does a 'Design' ques`</sub>

**Question**

In DSA interviews, what kind of problem does a 'Design' question usually ask you to solve?

**Reference answer**

Implement a small stateful data-structure class with a fixed API, built from standard structures and explicit invariants.

**Graded on**

- small stateful class
- fixed API
- standard structures composition
- not distributed-systems design

<details><summary>The lesson this came from</summary>

Design problems ask you to implement a class interface—hit counter, logger rate limiter, moving average, snapshot array, in-memory file system, getRandom collection, max stack—with exact time and space requirements. The mechanism is choosing a backing structure such as a queue, circular buffer, hash map, stack, or tree, then defining the invariant for eviction, deduplication, or version lookup. You justify each operation's worst or amortized cost, including how same-timestamp events and non-monotonic input are handled.

## Why interviewers ask this

These questions appear at Databricks, Dropbox, Apple, Snowflake, MongoDB, and LinkedIn because they test whether you can translate a requirement into a data layout rather than recall an algorithm. The interviewer watches whether you identify the relevant constraint—monotonic timestamps, out-of-order calls, duplicate elements, or snapshot frequency—and whether you state complexity honestly.

## The core idea

Start with the smallest structure that supports the eviction or version rule. For a fixed 300-second hit counter with monotonic timestamps, a deque of (timestamp, count) pairs gives O(1) hit and, with a running total and non-decreasing getHits calls, O(1) amortized getHits; without a running total, summing remaining entries is O(distinct timestamps in the window). A circular buffer of timestamped buckets gives O(1) hit but O(B) getHits because every bucket must be scanned. For per-key rate limiting, a hash map from message to next-allowed timestamp is O(1) expected. For versioned arrays, do not copy the array; store only changes per index and binary search by snap_id. Always say what happens for identical timestamps and whether out-of-order input can invalidate the structure.

## Key points

- HitCounter with monotonically increasing timestamps can use a deque of (timestamp, count) pairs, aggregating hits that share the same timestamp.
- The circular-buffer HitCounter has O(1) hit and O(B) getHits; each slot needs a stored timestamp so stale counts from a previous cycle can be cleared on hit and skipped on get.
- A fixed circular buffer indexed by timestamp % 300 assumes hits fall into the current 300-second window cycle; arbitrary out-of-order delays spanning multiple cycles can overwrite or drop hits without a different structure such as a sorted map.
- Logger Rate Limiter stores each unique message's next-allowed timestamp in a hash map and returns true only when the current timestamp reaches that value.
- Snapshot Array stores a list of (snap_id, value) changes per index and binary searches to answer get(index, snap_id).

## Your 60-second answer

For a hit counter, I would first clarify whether timestamps are monotonic. If they are, I would use a deque of (timestamp, count) pairs. hit(t) checks the back: if it has the same timestamp I increment its count, otherwise I push a new entry with count one. getHits(t) evicts from the front all entries with timestamp <= t - 300 and returns the sum of remaining counts, or a maintained running total if I keep one. That gives O(1) amortized hit and O(1) getHits after eviction when calls are chronological. The trade-off is that destructive eviction assumes getHits is called with non-decreasing timestamps. If timestamps can arrive out of order, I would switch to a circular buffer of timestamped buckets; then hit is O(1) but getHits scans all 300 buckets, so O(300).

## If they dig deeper

**How do you handle several hits at the same timestamp?**

Aggregate them as a count in one deque entry or bucket. On hit(t), if the latest timestamp equals t, increment its count; otherwise add a new entry. This prevents a burst of same-second hits from creating one node per hit.

**What changes if timestamps are not monotonic?**

A 300-slot circular buffer indexed by timestamp % 300 still works only if out-of-order hits stay within the same 300-second cycle. Each slot must keep its timestamp; on hit, if the stored timestamp is outside the current window or belongs to an older cycle, clear the slot. getHits must scan all slots and sum only valid timestamps. For arbitrary delays spanning multiple cycles, use a sorted map or deque keyed by timestamp instead of assuming modulo alignment.

**Why is getHits O(300) in the circular buffer version?**

You cannot know which of the 300 slots are valid without examining each slot's timestamp. Even if you maintain a total, stale buckets must be subtracted or ignored per query, so the scan is O(B) where B is the buffer size.

**How would you design a Logger Rate Limiter that expires old messages to bound memory?**

Keep a hash map of message to next-allowed timestamp. For cleanup, use a queue or min-heap of (timestamp, message) and evict entries whose timestamp is older than current time minus 10. This keeps expected O(1) operations and bounds memory by active messages.

**Design Snapshot Array without copying the full array on each snap.**

Store for each index a list of (snap_id, value) pairs added only on set. snap just increments a global id. get(index, snap_id) binary searches that index's list for the last entry with snap_id <= requested id; if none, return 0.

## Worked example

For a HitCounter using a deque with monotonic calls: hit(1), hit(2), hit(3) produce entries [(1,1), (2,1), (3,1)]. getHits(4) evicts timestamps <= -296, none removed, and sums to 3. hit(300) pushes (300,1). getHits(300) evicts <=0, none removed, and returns 4. getHits(301) evicts <=1, removing (1,1), leaving counts that sum to 3. With the circular buffer, getHits(301) would instead scan buckets with timestamps in (1,301], counting only valid ones.

## Common traps

- Saying getHits for the circular buffer is O(1). It is O(300) because all buckets must be scanned.
- Using timestamp % 300 without storing per-slot timestamps. You cannot distinguish a hit at t from one at t+300, so stale hits are counted or valid hits dropped.
- Copying the whole array in SnapshotArray.snap(). This is O(length) time per snap and O(length times number of snaps) space, failing large constraints.
- Destructively popping from a deque in getHits when timestamps can be called out of order. That evicts data that later calls may still need.

</details>

---

## 2. Lock interface and ReentrantLock · flash · Easy

*java · gate confidence 0.8*

<sub>to object to this card: `## java-lock-interface-and-reentrantlock` then `match: What is ReentrantLock in Java?`</sub>

**Question**

What is ReentrantLock in Java?

**Reference answer**

A reentrant, exclusive lock implemented in java.util.concurrent.locks (Java 5) with timed tryLock, interruptible lockInterruptibly, multiple Condition objects, and optional fairness.

**Graded on**

- Reentrant exclusive lock
- Part of java.util.concurrent.locks since Java 5
- Supports tryLock and lockInterruptibly
- Provides Condition and optional fairness

<details><summary>The lesson this came from</summary>

Lock is an interface in java.util.concurrent.locks that defines explicit mutual-exclusion operations: lock(), unlock(), tryLock(), lockInterruptibly(), and newCondition(). ReentrantLock, available since Java 5, is its most widely used implementation. It allows a thread to acquire the same lock multiple times and requires an equal number of releases. Unlike a synchronized block, the lock is not automatically released, so usage follows lock(); try { ... } finally { unlock(); }.

## Why interviewers ask this

Interviewers ask about Lock and ReentrantLock to test whether you understand explicit locking beyond the synchronized keyword. They are checking that you can explain the advanced features (timed, interruptible, non-blocking acquisition) and understand the trade-off: more control versus manual release and the risk of deadlocks or forgotten unlocks.

## The core idea

ReentrantLock is built on an internal synchronizer (AbstractQueuedSynchronizer in OpenJDK) that maintains an atomic state count and a queue of waiting threads. lock() atomically sets the state, increments a hold count, and records the owner; if the state is already held by another thread, the caller is enqueued and may block. unlock() decrements the hold count and, when it reaches zero, clears the owner and wakes one waiting thread. Reentrancy means the same thread can re-enter without deadlock. The unlock-to-lock transition has the same happens-before guarantee as monitor exit/entry, so data written before unlock is visible to the next locker. The API adds features synchronized lacks: tryLock, timed tryLock, lockInterruptibly, fairness, and multiple Condition waits.

## Key points

- Lock is an interface; ReentrantLock is its primary implementation and is reentrant, allowing a thread to acquire it multiple times and requiring an equal number of releases.
- Unlike synchronized blocks, ReentrantLock provides tryLock(), timed tryLock(timeout, unit), and interruptible lockInterruptibly() acquisition.
- A ReentrantLock must be released in a finally block because unlock is not automatic; an exception before unlock leaves the lock held and blocks other threads.
- The unlock-to-lock transition creates a happens-before edge, so writes made before unlock are visible to the thread that next acquires the lock.
- ReentrantLock offers optional fair acquisition via its constructor and multiple Condition objects per lock via newCondition(), unlike synchronized's single monitor wait set.

## Your 60-second answer

Lock is an interface in java.util.concurrent.locks for explicit mutual exclusion, and ReentrantLock is its most common implementation. The main difference from synchronized is control: you can attempt to acquire without blocking using tryLock(), wait only for a bounded time with tryLock(timeout, unit), or respond to interruption with lockInterruptibly(). ReentrantLock is reentrant, so the thread holding the lock can acquire it again; it must call unlock once for each acquisition. You can also create multiple Condition objects for separate wait/notify queues, choose fair queuing, and check whether the lock is held. The trade-off is that there is no automatic release, so the correct pattern is lock(); try { ... } finally { unlock(); }. For simple mutual exclusion, synchronized is usually the right default because it is structured and less error-prone; use ReentrantLock only when you need one of these advanced features.

## If they dig deeper

**How does ReentrantLock implement reentrancy?**

It keeps a hold count and the owning thread. When the current owner calls lock() again, the count increments and the method returns immediately. Each unlock() decrements the count; the lock is released to other threads only when the count reaches zero and the owner is cleared.

**When would you use synchronized instead of ReentrantLock?**

Use synchronized when the critical section is block-structured and you do not need timed, interruptible, or non-blocking acquisition. synchronized automatically releases on exit, including exceptions, so it avoids forgotten unlock bugs. Modern JVMs optimize uncontended synchronized well, so performance alone is rarely a reason to prefer ReentrantLock.

**What is lock fairness and when does it matter?**

Fairness means the lock attempts to grant access in roughly FIFO order of waiting threads, reducing starvation. ReentrantLock's constructor accepts a boolean for fairness; by default it is nonfair. Fair mode can be useful for long-held locks or when some threads should not be starved, but it generally reduces throughput because of more context switches and less barging.

**Explain how a Condition differs from Object.wait and notify.**

A ReentrantLock can create multiple Condition objects via newCondition(), each acting as a separate wait queue. Threads call await() to release the lock and wait, and another thread can call signal() or signalAll() to wake one or all waiters. This allows finer-grained signaling than a synchronized block, which has only one implicit wait set per object and uses wait/notify/notifyAll.

**What happens internally when a thread contends for ReentrantLock?**

The acquiring thread attempts an atomic compare-and-set on the synchronizer state. If it fails, it is added to a FIFO queue and may be parked. When the owner unlocks and the state reaches zero, the synchronizer wakes a queued thread, which then attempts to acquire. This queue and state are provided by AbstractQueuedSynchronizer in OpenJDK.

## Worked example

Suppose two threads each increment a shared counter 1,000 times without synchronization. Because the read-modify-write operation is not atomic, the final value can be below 2,000 due to lost updates. Wrapping the increment with a ReentrantLock fixes this: each thread calls lock.lock(); try { count++; } finally { lock.unlock(); }. The lock serializes the critical sections, and the final value is exactly 2,000. Reentrancy can be seen when a method holding the lock calls another method that also acquires the same lock; the second acquisition succeeds immediately because the thread already owns it, increasing the hold count from 1 to 2. A timed acquisition example is tryLock(1, TimeUnit.SECONDS): if the lock is not available, the thread waits up to one second, then either enters the critical section or takes an alternate path rather than blocking indefinitely.

## Common traps

- Forgetting to put unlock() in a finally block; if the critical section throws, the lock remains held forever and other threads block.
- Placing lock() inside the try block can lead to calling unlock() even if acquisition failed, which throws IllegalMonitorStateException; the lock() call should precede the try.
- Believing a fair ReentrantLock prevents tryLock() from barging ahead of waiting threads; tryLock() can still acquire immediately even in fair mode.
- Assuming ReentrantLock is automatically faster than synchronized; modern JVMs have optimized synchronized heavily, so complexity should drive the choice, not raw performance.

</details>

---

## 3. UML Class Diagram · typed · Medium

*lld · gate confidence 0.8*

<sub>to object to this card: `## lld-uml-class-diagram` then `match: Why does an LRU cache implementation require both a hash map`</sub>

**Question**

Why does an LRU cache implementation require both a hash map and a doubly linked list? Explain the role each plays.

**Reference answer**

The hash map provides O(1) lookup by key, while the doubly linked list maintains ordering by recency and allows O(1) removal and insertion, enabling moving a node to the front and evicting the tail when capacity is exceeded.

**Graded on**

- map gives O(1) lookup
- list gives O(1) reordering
- evict tail

<details><summary>The lesson this came from</summary>

A UML class diagram is a static structural description of an object-oriented system. Each class is shown as a rectangle with three compartments: name, attributes, and operations. Relationships such as association, aggregation, composition, generalization, realization, and dependency are drawn as distinct line styles and arrows, often annotated with multiplicities.

## Why interviewers ask this

Interviewers ask for class diagrams in low-level design rounds to see whether you can turn requirements into a maintainable object model before coding. They are testing if you assign responsibilities cleanly, choose the correct relationship strength, and express cardinality and visibility precisely enough for another engineer to implement.

## The core idea

A class diagram captures the static skeleton: what classes exist, what data they hold, and how they are permanently connected. The key decision is relationship semantics: composition means the part is owned and dies with the whole, aggregation means the part can be shared or outlive the whole, and association is any peer link. Inheritance expresses an is-a hierarchy, while realization expresses an interface contract. Multiplicity on each end of an association constrains how many instances participate. Getting these arrows right is more important than drawing every attribute.

## Key points

- In UML 2, a class is drawn as a rectangle with three compartments for name, attributes, and operations, with visibility markers +, -, #, ~.
- Associations are solid lines and may include navigation arrows and multiplicity labels like 1, 0..1, 1..*, or *.
- Aggregation is shown with a hollow diamond on the whole side and means the part can exist independently; composition has a filled diamond and ties the part's lifetime to the whole.
- Generalization is a solid line with a hollow triangle arrow pointing to the parent class; realization is a dashed line with a hollow triangle arrow pointing to the interface.
- A dependency is a dashed arrow and indicates a weaker relationship where a change in one class may affect another.

## Your 60-second answer

A UML class diagram is a static structural view of a system. It shows the classes, their attributes and operations, and the relationships among them. Each class is a rectangle with three compartments: the name, the attributes, and the methods. The relationships communicate design intent: an association is a solid line, often with multiplicities like one-to-many; aggregation has a hollow diamond on the whole side and means the part can outlive the whole; composition has a filled diamond and means the part is owned and destroyed with the whole. Inheritance is drawn with a solid line and a hollow triangle pointing at the parent, and implementing an interface uses a dashed line with the same triangle. When I draw one in a design interview, I focus on getting the cardinalities and ownership right first, then add only the attributes and methods that affect the structure.

## If they dig deeper

**What is the difference between aggregation and composition?**

Composition has a filled diamond and means the part is owned by the whole; if the whole is destroyed, the part is destroyed. Aggregation has a hollow diamond and means the part can be shared by other objects or continue to exist without the whole. For example, an engine in a car is composition, while a team having players is aggregation.

**How do you show multiplicity in a class diagram, and what does 0..* mean?**

Multiplicity labels appear on the association ends. 0..* means zero to many instances of that class may be associated with one instance of the opposite class; 1 means exactly one, 0..1 zero or one, 1..* one or more. The label is read from the perspective of the opposite end.

**When would you model a relationship as a dependency instead of an association?**

Use a dependency when one class uses another briefly, for example a parameter type or a return type, but does not hold a reference. A dependency is weaker and only says that changing the target may require changing the source. Association implies a more durable link, typically as a field.

**Can you sketch a class diagram for an LRU cache?**

I would have an LRUCache class with capacity, size, a map from keys to nodes, and head and tail references; operations include get(key), put(key, value), moveToFront(node), and evict(). Node would have key, value, prev:Node, next:Node. The cache has a composition relationship to Node because it creates and destroys nodes, and Node has a self-association for prev and next with multiplicity 0..1 on each end.

**How do you avoid over-engineering a class diagram in an interview?**

I only add classes that have a real responsibility in the current problem; I skip utility classes and getters/setters. I mark abstract classes and interfaces with italics or stereotypes, and I use composition only when there is clear ownership. The goal is to make the structure implementable without turning the diagram into code.

## Worked example

Consider designing a class diagram for an LRU cache. Start with two classes: LRUCache and Node. LRUCache holds attributes capacity:int, size:int, map: Map<Key,Node>, head:Node, tail:Node and operations get(key), put(key,value), moveToFront(node), evict(). Node holds key, value, prev:Node, next:Node. Draw a filled-diamond composition from LRUCache to Node with multiplicity 0..* on the Node side, because the cache owns its nodes and they are not shared. On Node, draw a self-association labeled prev and next with multiplicity 0..1 on both ends, showing each node points to at most one neighbor. Now the diagram communicates O(1) lookup via the map and O(1) reordering via the doubly linked list.

## Common traps

- Using aggregation for all whole-part pairs without checking whether the part can exist independently, which weakens the ownership signal.
- Overusing inheritance to reuse code, when association or composition would better model the relationship.
- Cluttering the diagram with getters, setters, and implementation collection types, obscuring the actual responsibilities.
- Leaving off multiplicities because they seem obvious; later the reader cannot distinguish one-to-one from one-to-many.

</details>

---

## 4. Unsupervised Learning · flash · Easy

*ai · gate confidence 0.85*

<sub>to object to this card: `## ai-unsupervised-learning` then `match: Name the three main tasks of unsupervised learning.`</sub>

**Question**

Name the three main tasks of unsupervised learning.

**Reference answer**

Clustering, dimensionality reduction, and density estimation.

**Graded on**

- Clustering groups similar observations
- Dimensionality reduction produces a lower-dimensional representation
- Density estimation learns the probability distribution over inputs

<details><summary>The lesson this came from</summary>

Unsupervised learning finds structure in data without labels by modeling the data distribution or grouping similar observations. The main families are clustering (k-means, hierarchical clustering, DBSCAN, Gaussian mixture models), dimensionality reduction (PCA, ICA, t-SNE), and density estimation (kernel density estimation, Gaussian mixture models). Unlike supervised learning, there is no target variable to evaluate against directly, so algorithms optimize internal criteria such as variance, density connectivity, or reconstruction error.

## Why interviewers ask this

Interviewers use this topic to test whether you can recognize problems where labels are unavailable or expensive, choose an algorithm appropriate for the data's shape and scale, and judge success without ground-truth accuracy. They also probe practical details such as why PCA requires scaling, what k-means assumes, and when t-SNE is useful.

## The core idea

Unsupervised learning extracts structure from unlabeled data; success is measured by internal coherence or downstream usefulness rather than labels. Clustering partitions data by similarity: k-means minimizes within-cluster variance but assumes roughly spherical clusters and needs k, while DBSCAN finds density-connected regions and marks outliers. Dimensionality reduction projects data to fewer dimensions—PCA retains directions of maximum variance, and t-SNE preserves local neighborhoods for visualization. Density estimation learns the probability distribution itself, with Gaussian mixture models as a common parametric choice. Because there is no ground truth, evaluation relies on metrics like silhouette score or on the performance of a downstream supervised task.

## Key points

- k-means minimizes the within-cluster sum of squares; it requires choosing k, is sensitive to feature scaling, and tends to find spherical clusters.
- PCA is a linear projection onto orthogonal axes of maximum variance; standardize features when they have different units or ranges, otherwise the first component can be dominated by the largest-scale feature.
- t-SNE is a nonlinear method that minimizes KL divergence between high- and low-dimensional similarities; it is mainly for visualization, and global distances between clusters are not meaningful.
- DBSCAN clusters points in dense regions and marks sparse points as noise; it does not need k but has eps and min_samples parameters and can find arbitrarily shaped clusters.
- The silhouette coefficient ranges from -1 to +1, measuring cohesion vs separation; Dunn's Index is the minimum inter-cluster distance divided by the maximum cluster diameter.

## Your 60-second answer

Unsupervised learning finds structure in data without labels. The main families are clustering, dimensionality reduction, and density estimation. Clustering groups similar points: k-means minimizes within-cluster variance and needs k, while DBSCAN finds density-connected regions and marks outliers; hierarchical clustering builds a tree. Dimensionality reduction projects data to fewer dimensions. PCA finds linear directions of maximum variance and is used for compression and noise reduction; t-SNE is nonlinear and mainly visualization. Density estimation with Gaussian mixture models or kernel density estimation learns the data distribution. The core trade-off is that without labels, there's no ground truth to optimize directly; you choose based on data shape, scale, and the downstream goal, and evaluate with internal metrics like silhouette score or by downstream performance.

## If they dig deeper

**Why do we need dimensionality reduction?**

It reduces computational cost and memory, removes noise and redundancy, helps visualize high-dimensional data, and can mitigate the curse of dimensionality. In practice it often improves downstream model training and makes patterns interpretable.

**Will PCA work on a dataset where one feature ranges 0-1 and another 10-1000?**

Yes, but only after scaling. PCA is not scale-invariant; if you apply it directly, the feature with the larger range can dominate the first principal component. Features with different units or ranges should be standardized to zero mean and unit variance before PCA.

**What is the relationship between PCA and SVD?**

For a centered data matrix X, the principal components are the right singular vectors of X. The singular values squared, divided by n-1, are the eigenvalues of the covariance matrix X^T X/(n-1). So PCA can be computed via the SVD of the centered data, avoiding an explicit covariance matrix.

**How does t-SNE work and why do we need it?**

t-SNE converts pairwise Euclidean distances in high dimension to probabilities using Gaussian kernels, then minimizes the KL divergence between those and probabilities from a Student-t distribution in low dimension. The heavy tails of the t-distribution reduce the crowding problem. It is used when linear methods like PCA cannot reveal nonlinear local structure, mostly for visualization.

**How do you evaluate clustering when you have no labels?**

Use internal metrics like the silhouette coefficient, which compares a point's mean distance to its own cluster versus the next nearest cluster, or Dunn's Index, the ratio of minimum inter-cluster distance to maximum cluster diameter. If clustering is preprocessing, you can also measure downstream supervised performance; high downstream performance suggests the clustering retained useful structure.

## Worked example

Consider the points 2, 4, 6, 20, 22, 24 on a line. k-means with k=2 and initial centroids 3 and 21 assigns 2,4,6 to the first cluster and 20,22,24 to the second. The updated centroids are 4 and 22, and the within-cluster sum of squares is (2^2 + 0^2 + 2^2) + (2^2 + 0^2 + 2^2) = 16. For point 4, a is the mean distance to points in its own cluster: (2 + 2)/2 = 2. The mean distance to the next nearest cluster (20,22,24) is (16 + 18 + 20)/3 = 18. Its silhouette score is (18 - 2)/18 ≈ 0.89, indicating a well-separated point. Repeating for all points gives an average silhouette score for the clustering.

## Common traps

- Applying PCA without standardizing features when they have different scales; the first principal component can simply reflect the highest-range feature rather than meaningful structure.
- Treating t-SNE distances between clusters as quantitatively meaningful; only local neighborhoods are somewhat stable, and global arrangement depends on perplexity and initialization.
- Choosing k in k-means arbitrarily without comparing inertia, silhouette, or domain requirements; the result can be misleading, and different initializations can find different local optima.
- Using silhouette or Dunn's Index to evaluate density-based clusters with arbitrary shapes; these metrics favor compact, convex clusters and may penalize DBSCAN results even when they are correct.

</details>

---

## 5. Supervised Learning · typed · Medium

*ai · gate confidence 0.85*

<sub>to object to this card: `## ai-supervised-learning` then `match: Why is data quality important in supervised learning?`</sub>

**Question**

Why is data quality important in supervised learning?

**Reference answer**

A model learns whatever patterns exist in the labels, so it inherits any bias or noise in the training data. Data collection and preprocessing are therefore part of model design, not separate chores.

**Graded on**

- Model inherits label bias and noise
- Data quality affects performance
- Preprocessing is part of model design

<details><summary>The lesson this came from</summary>

Supervised learning trains a model on a dataset of examples, each consisting of an input feature vector and a known target label or value. The training algorithm adjusts model parameters to minimize a loss function that measures the difference between predicted and true outputs. The two main task families are classification, where the target is a discrete class, and regression, where the target is a continuous quantity. A trained model is evaluated on unseen data to estimate how well the learned mapping generalizes.

## Why interviewers ask this

Interviewers ask this to test whether you understand the core ML workflow end-to-end: formulating a task from labeled data, choosing an appropriate algorithm and loss, preventing overfitting, and evaluating with metrics that match the problem. They also probe whether you can diagnose issues like imbalanced classes, feature scaling, or violated assumptions before applying a model.

## The core idea

The model is not given rules; it is shown examples and learns a function f(x) ≈ y. Training means searching for parameters that minimize a loss on the training set, while regularization or validation constraints try to keep it from memorizing noise. Classification predicts probabilities or classes, regression predicts real numbers; the boundary is the output type and choice of loss, such as cross-entropy versus squared error. Generalization is the goal, so the model is judged on held-out data, not on how well it fits the training examples. Most supervised failures come from mismatched data, label leakage, or evaluating with a metric that hides the problem, such as accuracy on imbalanced classes.

## Key points

- In supervised learning, every training example has an input and a known target; the goal is generalization to unseen inputs, not memorization.
- Classification predicts discrete labels and uses losses such as binary cross-entropy; regression predicts continuous values and commonly uses mean squared error.
- Logistic regression outputs a probability via the sigmoid function and becomes a binary classifier only after a threshold, commonly 0.5, is applied.
- Linear regression assumes a roughly linear relationship, independent residuals with constant variance, and normally distributed residuals for valid inference; multicollinearity inflates coefficient variance.
- For imbalanced classification, accuracy is misleading; precision, recall, F1, and ROC/AUC are better, and techniques include resampling or class weights.

## Your 60-second answer

Supervised learning is training a model on labeled examples—each input paired with a known output—so it can predict outputs for new inputs. The two main tasks are classification, where the output is a discrete label, and regression, where it's a continuous number. The model learns a mapping by minimizing a loss function: for regression, squared error is common; for classification, cross-entropy. The key criterion is generalization: it must perform well on unseen data, not just training data. So we hold out a test set or use cross-validation. A common trade-off is bias versus variance—too simple a model underfits, too complex a model overfits. Also, the metric must match the problem; accuracy is misleading for imbalanced classes, where precision, recall, and F1 are more informative.

## If they dig deeper

**What is the difference between classification and regression?**

Classification predicts a discrete class label, such as spam or not spam, and is optimized with losses like cross-entropy. Regression predicts a continuous numeric value, such as house price, and is optimized with losses like mean squared error. The output type determines the appropriate loss and evaluation metric.

**How do you handle imbalanced training data for a binary classifier?**

First, choose an appropriate metric like precision-recall or F1, not accuracy. Then consider resampling: oversampling the minority class, undersampling the majority, or a hybrid; SMOTE is a common synthetic oversampling method. Alternatively, use class weights in the loss or adjust the decision threshold based on the precision-recall curve.

**What assumptions does linear regression make, and how would you check them?**

It assumes a linear relationship between features and target, independent residuals with constant variance, and normally distributed residuals for inference; also low multicollinearity among features. Check with residual vs fitted plots for patterns, Q-Q plots or Shapiro-Wilk for normality, and VIF for multicollinearity.

**Why is logistic regression called regression if it is used for classification?**

It estimates a continuous probability P(y=1|x) by applying the sigmoid function to a linear combination of inputs. Classification only happens when you apply a threshold to that probability. This distinction matters because the decision threshold can be tuned independently of model training.

**How do you decide between precision and recall in a real product?**

Precision matters when false positives are costly, such as flagging legitimate transactions as fraud; recall matters when false negatives are costly, such as missing a serious disease. The F-beta score weights these according to the cost ratio. The right choice depends on business impact, not just the dataset.

## Worked example

Suppose a validation set has 10,000 transactions: 9,900 legitimate and 100 fraud. A naive model that predicts every transaction as legitimate gets 99% accuracy, but recall for fraud is 0/100 = 0, so no fraud is caught. If a logistic regression model trained with class weights outputs fraud probabilities, lowering the decision threshold from 0.5 to 0.3 might produce 80 true positives and 120 false positives. Then precision is 80/200 = 0.40, recall is 80/100 = 0.80, and F1 = 2 × (0.40 × 0.80) / (0.40 + 0.80) ≈ 0.533. This shows why accuracy hides the failure and why threshold tuning or class weighting is necessary.

## Common traps

- Saying logistic regression is a classifier without noting it outputs a probability and requires a threshold.
- Using accuracy on imbalanced data and concluding the model is good.
- Treating linear regression assumptions as optional for prediction, when violations affect coefficient inference and sometimes prediction reliability.
- Training on the entire dataset and reporting training performance as evidence of generalization.

</details>

---

## 6. Supervised Fine-Tuning of LLM · mcq · Easy

*ai · gate confidence 0.85*

<sub>to object to this card: `## ai-supervised-fine-tuning-of-llm` then `match: Which rank range is typical for LoRA adapters in supervised `</sub>

**Question**

Which rank range is typical for LoRA adapters in supervised fine-tuning?

**Options**

- 1–2
- 8–16
- 64–128
- 256–512

**Reference answer**

8–16

**Graded on**

- LoRA rank typically 8–16
- Alpha around twice the rank
- Target attention projection matrices

<details><summary>The lesson this came from</summary>

Supervised fine-tuning continues training a pre-trained language model on a curated dataset of labeled prompt–response pairs. The objective is next-token cross-entropy, typically computed only on the target response tokens and not the prompt tokens. SFT adapts a model to an instruction format, output schema, style, or domain behavior; it does not reliably inject new factual knowledge.

## Why interviewers ask this

Interviewers test whether the candidate knows when to choose SFT over prompting or RAG, how to build clean instruction data, how to set training hyperparameters, and how to estimate memory. They also probe PEFT methods such as LoRA/QLoRA and awareness of catastrophic forgetting.

## The core idea

SFT is the first post-training step: a base model is shown prompt–response examples and optimized only on the response tokens. It changes how the model follows instructions, formats output, and behaves in a domain, but the pre-trained weights still supply most knowledge. In practice, full fine-tuning is expensive because weights, gradients, and Adam states all must be stored, so low-rank or quantized adaptations such as LoRA/QLoRA are the common route. The method is deliberately low-data and low-epoch; after SFT, preference alignment such as DPO can further shape the model.

## Key points

- SFT uses labeled prompt–response pairs with next-token cross-entropy, typically masking prompt tokens so only target response tokens contribute to the loss.
- For a 7B model in bf16 with AdamW, static weights, gradients, and optimizer states are roughly 56–84 GB before activations; activation memory and long context can still push a naive full run above 100 GB.
- LoRA freezes base weights and trains low-rank update matrices A and B; QLoRA quantizes the frozen base to 4-bit, making SFT feasible on a single consumer GPU.
- SFT is suited to instruction following, output format, tone, and stable domain behavior, not to injecting new or frequently changing facts; retrieval augments facts.
- Catastrophic forgetting of general capabilities is mitigated by low learning rate, few epochs, early stopping, and PEFT methods that limit updates.

## Your 60-second answer

Supervised fine-tuning is continuing to train an already pre-trained LLM on a dataset of prompt–response pairs, using next-token cross-entropy and usually masking the prompt so only response tokens contribute. It adapts the model to an instruction style, output format, or stable domain behavior. It is not a reliable way to inject new facts; use retrieval for that. The first practical decision is whether to full fine-tune or use a parameter-efficient method. Full fine-tuning is memory-heavy: for a 7B model in bf16 with AdamW, weights, gradients, and optimizer states are roughly 56–84 GB before activations, so on consumer hardware you normally use LoRA or QLoRA. The trade-off is that fine-tuning changes the model's behavior and can cause catastrophic forgetting, so you keep learning rates low, epochs few, and validate carefully.

## If they dig deeper

**When would you fine-tune an LLM instead of using prompt engineering or RAG?**

Use prompt engineering first for quick iteration and few-shot adaptation. Use RAG when the model needs up-to-date or verifiable external knowledge. Fine-tune when you need to change stable behavior: instruction following, output schema, tone, or a narrow domain task, and you have hundreds to thousands of curated prompt–response examples. RAG is for facts; SFT is for behavior.

**How do you build a supervised fine-tuning dataset for Q&A?**

Collect real prompts from logs or task templates, then write high-quality canonical responses that follow the exact output format. Include edge cases, refused or low-context prompts where the correct behavior is to abstain, and deduplicate/near-deduplicate. Split train/validation, sanity-check with the base model, and mask prompt tokens in the loss so only response tokens train.

**What hyperparameters do you set when fine-tuning, and why?**

For full fine-tuning start with a learning rate around 1e-5 to 5e-5; LoRA can often use 1e-4 to 3e-4 because only adapters update. Train for one to three epochs with a warmup and cosine decay, batch size as large as memory allows. Set LoRA rank around 8–64 with alpha about double the rank and target attention query/value projections. Use early stopping on validation loss.

**How do you estimate infrastructure requirements for fine-tuning a 7B model?**

Account for weights, gradients, optimizer states, and activations. In bf16 with AdamW, a 7B model has 14 GB weights, 14 GB gradients, and roughly 28–56 GB Adam states depending on precision/master weights, so static state is about 56–84 GB before activations. Activations and long context can push total beyond 100 GB, so full fine-tuning usually needs sharding such as ZeRO/FSDP. LoRA/QLoRA reduces this enough for consumer GPUs.

**What are the reparameterized PEFT methods, and how do they differ from additive adaptation?**

LoRA freezes the base weights and learns low-rank matrices A and B such that the update is B times A added to the original weight. DoRA extends LoRA by decomposing the update into magnitude and direction; variants like AdaLoRA allocate rank adaptively. They differ from additive methods like adapters or prefix tuning, which insert extra parameters or virtual tokens instead of reparameterizing the existing weight update.

## Worked example

Suppose you fine-tune a 7B model for German translation. You collect 5,000 prompt-response pairs, such as 'Translate: The book is on the table' / 'Das Buch liegt auf dem Tisch'. Loss is computed only on the German tokens. Full fine-tuning in bf16 with AdamW needs 14 GB for weights, 14 GB for gradients, and 28–56 GB for optimizer states, so roughly 56–84 GB before activations, which exceeds a single 24 GB consumer card. Instead, you apply QLoRA: quantize the base model to 4-bit, then add LoRA rank 16 to q/k/v/o projections, creating about 16.7 million trainable parameters. AdamW state for the adapters is around 130–200 MB, keeping the run within consumer VRAM. You train for one epoch at 2e-4 with cosine decay and evaluate BLEU/format adherence.

## Common traps

- Treating SFT as knowledge insertion; candidates often claim it can replace RAG for factual updates, but it predominantly teaches format, style, and task behavior, not reliable new facts.
- Underestimating memory by quoting only the 14 GB of bf16 weights and ignoring gradients, Adam states, and activations; for 7B the static state is roughly 56–84 GB before activations.
- Fine-tuning with too many epochs or too high a learning rate, which overfits and degrades general capabilities through catastrophic forgetting.
- Giving vague PEFT answers without naming rank/alpha/target modules or recognizing that higher rank is not automatically better and increases overfitting risk.

</details>

---

## 7. Leadership · flash · Medium

*behavioral · gate confidence 0.85*

<sub>to object to this card: `## beh-leadership` then `match: In a behavioral interview about a difficult decision, what s`</sub>

**Question**

In a behavioral interview about a difficult decision, what should a senior candidate explicitly include to avoid sounding like an executor instead of a leader?

**Reference answer**

The decision-making framework and trade-offs that produced the actions, rather than only narrating actions chronologically.

**Graded on**

- Name the decision-making framework used.
- State the explicit trade-offs considered.
- Avoid only listing actions in chronological order.
- Reconstruct the reasoning behind choices.

<details><summary>The lesson this came from</summary>

Leadership in engineering and product contexts is the ability to move a team and stakeholders toward a shared outcome without relying on formal authority. It works through vision, credibility, and relationship building rather than direct control; in a critical situation it adds clear communication, decisive action, and active maintenance of morale and productivity. At senior levels it also includes thought leadership: contributing original ideas and analysis through publishing, speaking, and technical discussions to build personal and company credibility over time.

## Why interviewers ask this

Interviewers are testing whether you can create alignment and momentum without authority, and whether you stay effective under pressure. At senior levels they are also checking that you cover the full leadership spectrum—people, stakeholders, strategy, risk, capacity, and change—not just technical decisions. They expect you to articulate the decision-making framework behind your actions, not simply list what you did.

## The core idea

Leadership without formal authority runs on credibility, vision, and relationships; those are the actual levers when you cannot assign work. In a crisis, the same skill becomes clarity, decisiveness, and stability: communicate what is known, make the call, and keep the team functional. Thought leadership compounds that credibility over time by putting original analysis into the community through writing, speaking, and discussion. In senior interviews, a leadership story must show the full spectrum of influence and the reasoning framework, not just the actions. Strong candidates stay structured and preempt uncharitable readings by naming constraints, objections, and trade-offs explicitly.

## Key points

- Leadership without formal authority operates through vision, credibility, and relationships rather than direct control.
- In a critical situation, effective leadership requires clear communication, decisive action, and maintaining team morale and productivity.
- Thought leadership is built by publishing, speaking, and participating in technical discussions with original analysis, and it increases personal and company credibility over time.
- Senior behavioral interviews expect candidates to cover people leadership, stakeholder management, strategy, and change, risk, or capacity—not only technical or product outcomes.
- Strong senior answers pair actions with the decision-making framework that produced them; listing actions alone reads as execution rather than strategy.

## Your 60-second answer

I'd define leadership as getting a group of people to a shared outcome without needing formal authority over them. In practice that means building credibility through good technical and product judgment, being clear about the outcome, and investing in relationships before you need them. In a crisis, the same skill shows up as clear communication, making a decision instead of stalling, and keeping the team stable and productive. The trade-off is speed versus buy-in: you can force a decision quickly, but without relationship and reasoning you'll get compliance now and resistance later. Strong leadership often looks slower up front because it spends time aligning people, but execution becomes much faster afterward.

## If they dig deeper

**Tell me about a time you influenced a team or stakeholder without formal authority.**

In my last role, I needed another team to change how they consumed an API my team owned. I wrote a short memo tying the change to an incident we had already had, then met each engineer on their team individually to hear their objection. I adjusted the plan to include a fallback and a two-week spike with clear go/no-go metrics; they agreed once the criteria were explicit.

**How do you handle resistance from a senior engineer or executive?**

I first diagnose the real objection—risk, effort, ownership, or priority—by asking directly rather than arguing. Then I bring data or a trade-off analysis that addresses that specific concern. If we still disagree after that, I either escalate to the right decision-maker or commit to the decision and help execute.

**Walk me through leading a team through an incident or high-pressure situation.**

I separate immediate mitigation from root cause, name one person as the decision-maker for the incident, and set a clear communication channel so status is visible without interrupting the responders. I keep the team focused on the next few actions while making the call when we have enough information. Afterward we do a blameless postmortem.

**What framework do you use to decide how to delegate or escalate work?**

I use four criteria: urgency, reversibility, who has the context, and whether the task develops someone on the team. Reversible, low-context work is delegated; irreversible or urgent decisions with limited context are escalated quickly. I can point to a specific example where the framework changed what I did.

**How do you build thought leadership without letting it distract from delivery or team leadership?**

I only publish or speak about work I have already done, so it reuses existing material instead of creating a second job. I also use internal forums and mentor teammates before seeking external visibility. If an opportunity would consume time my team needs, I decline it.

## Worked example

A strong answer sounds like: 'In my last role, I needed to change how [named team] consumed [specific API/queue], but I had no authority over them. I wrote a one-page memo tying the change to an outage or cost we had already experienced, then met each engineer individually to hear their specific objection—one was migration effort, another was missing runbooks. I adjusted the proposal to include a fallback and a two-week spike with explicit go/no-go metrics. Once the objections were addressed by name, the discussion shifted from whether to how. The team agreed to the spike, and the change later landed because the success criteria were agreed before the decision.' The shape is: a specific target, named stakeholders, a real mechanism (memo, private meetings, reversible trial), and a decision that changed.

## Common traps

- Listing only actions and outcomes without explaining the decision framework, which makes a leadership story sound like execution rather than strategy.
- Telling a story from only one dimension—such as technical design—while omitting people, stakeholder, risk, or change management.
- Letting the interviewer's questions pull the story into rabbit holes and failing to redirect toward the leadership signal the question is really probing.
- Being verbose or defensive, which creates openings for an uncharitable interpretation that a senior candidate is expected to preempt.

</details>

---

## 8. Questions to ask the interviewer · typed · Medium

*behavioral · gate confidence 0.85*

<sub>to object to this card: `## beh-questions-to-ask-the-interviewer` then `match: What is the core trade-off a candidate faces when choosing w`</sub>

**Question**

What is the core trade-off a candidate faces when choosing which questions to ask at the end of an interview?

**Reference answer**

There is limited time, so the candidate must choose two or three questions that yield the highest signal about whether they would actually want the job, rather than asking many low-value questions.

**Graded on**

- limited time
- high signal
- fit evaluation
- typically two or three questions

<details><summary>The lesson this came from</summary>

The candidate-led closing portion of a software engineering interview, usually the last five to ten minutes, where the interviewer says 'Do you have any questions?' It is a two-way evaluation: the candidate gathers evidence about the role, team, engineering practices, and company direction while the interviewer observes what the candidate cares about and how well they listen.

## Why interviewers ask this

Interviewers expect questions and treat silence as disinterest or lack of preparation. The specific questions reveal whether a candidate is evaluating real work, team health, and growth—or just perks and logistics—so the segment is a final signal of judgment and motivation.

## The core idea

Prepare different questions for different interviewers. Individual contributors can speak to technical decisions, on-call, the stack, and maintenance; engineering managers can speak to ramp-up, performance measurement, team composition, and conflict; executives can speak to company priorities and competitive position. The highest-signal questions ask for concrete evidence: 'What was the worst technical blunder recently and what did you change?' beats 'What's the culture like?' Listen to the answer and ask for a recent example rather than moving to the next prepared question. Do not ask about compensation unless the interviewer raises it; leave that to the recruiter after an offer.

## Key points

- Candidates who ask no questions risk being read as uninterested or unprepared.
- The best questions uncover concrete evidence: 'What was the worst technical blunder and what did you change?' beats 'What's the culture like?'
- Ask different questions of an individual contributor, a hiring manager, and an executive: technical health, performance and growth, and company strategy respectively.
- Do not ask about compensation unless the interviewer raises it; some hiring managers treat it as a red flag.
- Follow up on an answer with 'Can you give a recent example?' to turn a vague claim into evidence.

## Your 60-second answer

When the interviewer says 'Do you have any questions?', the answer is yes: have three to five prepared. Silence reads as disinterest, and the questions reveal what you optimize for, so ask about actual engineering work and team health rather than perks. For an individual contributor, ask 'What is the most important problem you'd want me to solve in the first six months?' or 'What was the worst technical blunder recently and what did the team change?' For a manager, ask 'What does success look like for this team?' or 'How do you ramp up new engineers?' For an executive, ask 'What are the highest priorities right now: new features, stability, or reducing operational overhead?' Avoid compensation unless the interviewer raises it. The trade-off is that asking about frustrations or costly decisions can be uncomfortable, but it signals seriousness and surfaces red flags.

## If they dig deeper

**Is it really mandatory to ask questions at the end of an interview?**

Yes, in practice. The interviewer's 'any questions?' is not rhetorical; having none reads as disinterest or lack of preparation. Prepare at least three questions so you can adapt if some are answered earlier.

**Should I ask the same questions to every interviewer?**

No. An individual contributor can answer concrete engineering questions: worst technical blunder, stack rationale, on-call load. A hiring manager can answer ramp-up, performance measurement, team composition, and conflict resolution. An executive can answer company priorities and competitive differentiation.

**What single question best uncovers red flags?**

'What is the most frustrating part about working here?' or 'What is something you wish were different about your job?' Both are direct but fair, and a defensive or evasive answer is itself information. Follow up with 'Can you give a recent example?' to get evidence.

**How do I bring up compensation without hurting my candidacy?**

Do not raise it in the closing questions unless the interviewer does. If the interviewer asks about your expectations, answer with a researched range and say you are flexible pending the whole offer. Otherwise wait for the recruiter after an offer, when the evaluation is largely complete.

**If I only have five minutes, how do I prioritize among role, team, and company questions?**

Ask one question that reveals actual work, like 'What is the most important problem I would solve in the first six months?'; one that reveals management or team health, like 'How do you measure success for this team?'; and one that reveals company direction, like 'What are the highest priorities right now?' Then spend remaining time following up on the most revealing answer.

## Worked example

A strong end-of-interview question sequence sounds like: after the interviewer asks for questions, the candidate says, 'What is the most important problem you would want me to solve in my first six months?' After the interviewer answers, the candidate follows up with 'Can you give a recent example of how that problem showed up?' Then they ask, 'What was the worst technical blunder in the past year, and what did the team change to prevent it?' Finally, they ask the manager, 'How do you ramp up engineers who are new to the team?' The candidate does not ask about free lunches, and does not ask about salary unless the interviewer brings it up. The sequence works because each question requests evidence, not a slogan, and the follow-up tests whether the positive claim is real.

## Common traps

- Asking about compensation or perks in the closing questions; some hiring managers read it as money-first, and it is better left to the recruiter after an offer.
- Asking 'What is the culture like?' or 'Do you like working here?' produces yes/no or vague answers; ask for a specific frustration or a recent change instead.
- Treating the list as a script: moving from question to question without acknowledging the answer signals poor listening and wastes the opportunity to follow up.
- Using questions that are already answered by the job description or the company's public engineering blog, which signals lack of preparation.

</details>

---

## 9. Conflict resolution · mcq · Easy

*behavioral · gate confidence 0.85*

<sub>to object to this card: `## beh-conflict-resolution` then `match: A teammate violates an agreed engineering standard during a `</sub>

**Question**

A teammate violates an agreed engineering standard during a dispute. What is the most consistent response?

**Options**

- Mediate to find common ground because the relationship matters most.
- Apply the agreed consequence the same way it would be applied to anyone else.
- Treat it as a technical disagreement and reframe around shared goals.
- Ask the rest of the team to vote on whether the standard should be enforced.

**Reference answer**

Apply the agreed consequence the same way it would be applied to anyone else.

**Graded on**

- standards exist
- consistent application
- avoid perception of bias

<details><summary>The lesson this came from</summary>

Conflict resolution is the deliberate process of addressing a disagreement between individuals or teams by understanding each party's position, identifying shared goals, and reaching an outcome—agreement, compromise, or an enforced decision—that lets work continue. In engineering contexts it ranges from a code review dispute to competing architectural directions across teams. The core mechanism is structured conversation, often with a neutral facilitator, rather than avoiding the conflict or declaring a winner by authority alone.

## Why interviewers ask this

The interviewer is testing whether you can handle interpersonal friction without damaging working relationships or output. They want evidence you can diagnose the underlying interests, separate people from the problem, and take ownership of reaching a resolution rather than escalating or avoiding. Strong answers show you treat conflict as a normal part of collaboration, not a personal failure.

## The core idea

Conflict becomes destructive when it is ignored, personalized, or resolved by authority without buy-in. A strong resolution process starts by making each side's position and underlying interests explicit, then reframes the disagreement around the shared goal, and finally agrees on a concrete next step with owners and a check-in. The goal is not to make everyone happy; it is to restore enough trust and clarity that the work moves forward. Mediation works when the facilitator stays neutral, enforces respectful communication, and holds parties accountable to what they agreed. In interviews, the best evidence is a specific story with named stakeholders, what you did, and the observable outcome.

## Key points

- Unaddressed conflict degrades trust and output because people stop raising issues and start working around each other.
- Separate positions (what each side wants) from interests (why they want it), since interests often overlap even when positions conflict.
- A neutral facilitator improves outcomes by structuring the conversation, enforcing respect, and restating each side accurately, but the parties must own the resolution.
- Escalating to a manager should be a step in a defined process, not the first move, unless safety or policy is at stake.
- After a resolution, document the agreement, assign owners, and schedule a follow-up, otherwise the conflict often recurs.

## Your 60-second answer

In my last role, I disagreed with [person/team] over [decision]. I set up a direct conversation, asked what outcome they were worried about, and restated it back to them. Their real concern was [underlying interest], which was different from the surface position. I proposed a middle path—[compromise]—and we agreed to try it with a written follow-up in [doc/tracker]. The trade-off was [cost, e.g., extra abstraction or slower first milestone], but it unblocked the work and kept trust intact. I would do the same again, but I would involve the other person earlier next time.

## If they dig deeper

**What specifically did you do to move the disagreement toward a resolution?**

I started by scheduling a one-on-one rather than continuing over email or chat, because tone is hard to read asynchronously. I asked open questions about what outcome they were worried about, restated their concern back to confirm, and then proposed two or three options that addressed that concern while still meeting the project's goal. We picked one together and wrote down who would do what by when.

**How did you make sure the other person actually felt heard, rather than just waiting for their turn to talk?**

I restated their position in my own words and asked for corrections until they said I had it right. I also acknowledged the part of their argument that was valid before introducing my own view. That separated the personal friction from the technical disagreement.

**What would you do differently if you faced that same conflict again?**

I would involve the other person earlier, before positions hardened and before the team lost time. I would also document the decision criteria up front, so the conversation stayed about the problem rather than who had more seniority.

**What do you do when the other person won't engage, or keeps avoiding the conversation?**

I would give them a clear, private invitation with a specific agenda and a low-stakes framing, like asking for their help on a design question. If they still avoid it, I would ask my manager to facilitate a short meeting, because unresolved conflict that blocks work is exactly what managers should help with. I wouldn't keep pushing unilaterally or start working around them without saying so.

**When do you escalate a conflict to a manager instead of resolving it yourself?**

I escalate when the disagreement is blocking committed work and we've had at least one direct attempt without progress, or when the conflict involves harassment, policy violations, or a pattern of bad faith. Escalation isn't a failure; it's the next step in a defined process, and I would bring the specific decision needed rather than just venting.

## Worked example

A strong answer sounds like: 'Two teams disagreed about whether to reuse an internal queue or adopt a managed pub/sub for a new pipeline. I set up a meeting with the tech leads and asked each to name the risk they were most worried about. Team A worried about operational load; Team B worried about vendor lock-in. I restated both concerns, then reframed the decision around the shared goal of shipping on schedule without adding on-call burden. We agreed to use the managed service behind an interface, with a fallback adapter to the internal queue if costs grew. I wrote the decision in the design doc and scheduled a follow-up review. The trade-off was an extra abstraction layer, but it let both teams proceed.'

## Common traps

- Talking only about how the other person was wrong, without describing your own contribution to the disagreement.
- Choosing a story with no real resolution or where you just gave in to keep the peace.
- Describing the conflict in vague terms ('we had different opinions') instead of naming the specific technical decision and trade-offs.
- Saying you avoid conflict or never have disagreements, which signals either low self-awareness or no experience working in a team.

</details>

---

## 10. CPU Scheduling · typed · Medium

*cs · gate confidence 0.85*

<sub>to object to this card: `## cs-cpu-scheduling` then `match: What is the central tradeoff in CPU scheduling, and which cl`</sub>

**Question**

What is the central tradeoff in CPU scheduling, and which classic algorithms represent each side?

**Reference answer**

The central tradeoff is between responsiveness and turnaround time. Round Robin improves responsiveness by rotating a quantum but adds context-switch overhead and can reduce throughput; SJF minimizes average turnaround for known runtimes but can harm interactive response and starve long jobs. FCFS is simple but creates convoy effects.

**Graded on**

- responsiveness vs turnaround
- RR improves response but has overhead
- SJF minimizes turnaround but can starve
- FCFS suffers convoy effects

<details><summary>The lesson this came from</summary>

CPU scheduling is the OS policy that selects which runnable thread or process gets a core at each context switch. FCFS uses arrival order; non-preemptive SJF uses the shortest known CPU burst; Round Robin is preemptive with a fixed time slice; MLFQ uses multiple priority queues and CPU-time accounting. These policies trade off turnaround time (finish minus arrival), response time (first CPU time minus arrival), throughput, and fairness.

## Why interviewers ask this

Interviewers use CPU scheduling questions to test whether you can compute turnaround and response times for a small batch and reason about trade-offs rather than recite names. They also probe whether you understand how MLFQ learns job behavior without knowing runtimes, which separates candidates who know the mechanisms from those who only know definitions.

## The core idea

No single algorithm wins on all metrics. FCFS is simple but suffers convoy effects when short jobs queue behind a long CPU-bound job. Non-preemptive SJF minimizes average turnaround for a batch when all jobs are ready and runtimes are known, but it requires future knowledge and can starve long jobs under continuous arrivals. Round Robin adds preemption with a time slice to bound how long any job can monopolize the CPU; this improves response for later jobs under a first-arrived long job but often raises average turnaround and adds context-switch cost. MLFQ approximates SJF without knowing runtimes by keeping multiple priority queues: jobs that block or yield before exhausting their CPU allocation tend to stay at higher priority, CPU-bound jobs are demoted as they consume CPU, and per-level CPU accounting stops early yielding from gaming the scheduler. The central trade is turnaround versus response, with fairness as a third axis.

## Key points

- Non-preemptive SJF minimizes average turnaround when all jobs arrive together and their CPU bursts are known; it does not need preemption for that batch, but real OSes seldom know burst lengths in advance.
- FCFS runs jobs in arrival order and creates the convoy effect: many short jobs accumulate behind a long CPU-bound job, inflating average waiting and turnaround.
- Round Robin preempts each job after a fixed quantum to bound response time and guarantee fair progress, but context-switch overhead and interleaving often make average turnaround worse than SJF for the same batch.
- MLFQ approximates SJF without a priori runtimes by using several priority levels, running the highest-priority non-empty queue first, demoting jobs that consume CPU, and using per-level CPU-time accounting so early yielding cannot prevent demotion.
- Latency and throughput measure different things: a batch scheduler can have high throughput but poor individual response time, while RR caps the time a job waits behind one long job at the cost of extra context switches.

## Your 60-second answer

CPU scheduling is the policy that picks which runnable thread gets the core next. The baseline policies are FCFS, SJF, and Round Robin. FCFS is simple and fair in order, but a long job at the front makes short jobs wait, causing a convoy effect and poor average turnaround. SJF minimizes average turnaround if all jobs are ready and runtimes are known, but it requires future knowledge and can starve long jobs. Round Robin adds preemption with a fixed time slice, so no job monopolizes the CPU and later jobs get a first chance quickly; the cost is context-switch overhead and often higher average turnaround than SJF. Real systems often use MLFQ, which keeps multiple priority queues and demotes CPU-bound jobs while keeping I/O-bound jobs at higher priority, approximating SJF without knowing job lengths. The core trade-off is turnaround time versus response time.

## If they dig deeper

**How do you calculate turnaround time and response time for a job?**

Turnaround is completion time minus arrival time; response is first time the job gets the CPU minus arrival. For example, a job that arrives at 0, first runs at 5, and finishes at 20 has response 5 and turnaround 20. Average these over all jobs to evaluate a policy.

**Why does SJF minimize average turnaround, and when does it break down?**

When all jobs are available at time 0 and runtimes are known, swapping a longer job that is ahead of a shorter job moves the shorter finish earlier by more than it delays the longer one, lowering the sum of completion times. It breaks down because the OS usually does not know burst lengths and continuous arrivals of short jobs can starve long jobs.

**What is the convoy effect in FCFS scheduling?**

A long CPU-bound job runs first while many small jobs wait; afterward all small jobs run quickly, but their aggregate waiting and turnaround times are inflated. It is the canonical argument against FCFS for general-purpose CPU scheduling.

**How does MLFQ prevent a process from gaming the scheduler by yielding just before its quantum expires?**

A naïve MLFQ might let a yielding job stay at its current priority, but a process could then yield at 99% of each quantum and monopolize high priority. Real MLFQs track cumulative CPU time consumed at each level and demote the job once it exhausts that level's allocation, regardless of how many times it yielded early.

**What happens to Round Robin if the time quantum is too small or too large?**

Too small relative to context-switch cost makes the CPU spend a large fraction of time switching, lowering effective throughput and increasing completion times. Too large makes it behave like FCFS for long jobs, so later jobs wait a long time and response time suffers.

## Worked example

Take A=24 ms, B=3 ms, C=3 ms, all arriving at 0. FCFS runs A 0-24, B 24-27, C 27-30; turnaround times 24, 27, 30 ms, average 27 ms. SJF runs B 0-3, C 3-6, A 6-30; turnaround times 3, 6, 30 ms, average 13 ms, and B and C first get CPU at 0 and 3 ms. Round Robin with quantum 4 ms runs A 0-4, B 4-7, C 7-10, then A in 4 ms slices to 30; completions are A=30, B=7, C=10, average turnaround 15.67 ms, and B and C first get CPU at 4 and 7 ms. SJF beats FCFS on average turnaround and starts short jobs earlier than RR; RR's benefit is bounding each job's slice, not putting short jobs before they would run under SJF.

## Common traps

- Claiming that Round Robin puts short jobs on the CPU earlier than SJF; in the batch example, SJF starts B and C at 0 and 3 ms, while RR starts them at 4 and 7 ms.
- Saying MLFQ always lets a job stay at its current level if it yields before its time slice ends; robust MLFQs use per-level CPU accounting to demote after the allocation is consumed.
- Using completion time instead of first-run time when computing response time; a job that waits 10 ms and then runs finishes later, but its response time is only 10 ms.
- Ignoring context-switch overhead when picking a Round Robin quantum; a very small quantum can waste most CPU time switching and destroy throughput.

</details>

---

## 11. Object-Oriented Programming Principles · flash · Easy

*cs · gate confidence 0.85*

<sub>to object to this card: `## cs-object-oriented-programming-principles` then `match: What is polymorphism in Java primarily?`</sub>

**Question**

What is polymorphism in Java primarily?

**Reference answer**

Polymorphism in Java is primarily dynamic dispatch: a call through a base type or interface invokes the overridden method of the actual object at runtime.

**Graded on**

- dynamic dispatch
- overridden methods
- actual object type

<details><summary>The lesson this came from</summary>

Object-oriented programming organizes code into classes and objects that combine state (fields) and behavior (methods). The four central principles are encapsulation, which restricts direct access to an object's internal state; inheritance, which allows a class to derive from another to reuse and extend functionality; polymorphism, which lets objects of different types respond to the same method call; and abstraction, which hides implementation details behind a simplified interface. Languages such as Java, C++, Python, and C# implement these concepts with varying syntax and capabilities.

## Why interviewers ask this

Interviewers ask about OOP principles because they underpin most software design and many design patterns. They test whether you can explain these concepts clearly, apply them to real design problems, and recognize trade-offs such as inheritance versus composition. A strong answer shows not just definitions but practical judgment about when and how to use each principle.

## The core idea

Encapsulation protects an object's invariants by making fields private and exposing controlled methods; this prevents invalid state and reduces coupling. Inheritance creates 'is-a' relationships and supports code reuse, but it also introduces tight coupling, so composition is often preferred for flexibility. Polymorphism enables one interface to represent many forms, typically through method overriding and interfaces, allowing code to be written against abstractions rather than concrete types. Abstraction reduces complexity by exposing only essential behavior, whether through abstract classes or interfaces, and lets the implementation evolve independently. These principles work together: abstraction defines what an object does, encapsulation hides how it does it, and inheritance and polymorphism provide reuse and extensibility.

## Key points

- In Java, access modifiers control encapsulation: private members are accessible only within the same class, protected also allows subclasses and same package, and public is universally accessible.
- Java does not support multiple class inheritance to avoid the diamond problem, but a class can implement multiple interfaces.
- Polymorphism in Java appears in two forms: compile-time overloading (same method name, different parameters) and runtime overriding (subclass provides a specific implementation of a superclass method).
- Abstraction is achieved through abstract classes (which can have concrete methods) and interfaces (which, since Java 8, can have default and static methods).
- Composition is often favored over inheritance because it provides looser coupling and easier change; the Liskov Substitution Principle states that subclasses must be substitutable for their base class without breaking correctness.

## Your 60-second answer

OOP is a programming paradigm where programs are built from objects that bundle data and behavior. The four core principles are encapsulation, inheritance, polymorphism, and abstraction. Encapsulation bundles state and methods into a class and hides internals with access modifiers like private, protecting invariants. Inheritance lets a subclass reuse and extend a parent class, giving code reuse but also tight coupling. Polymorphism means a single method call can behave differently depending on the runtime type, typically via overriding and interfaces. Abstraction hides implementation details behind an interface or abstract class, so callers depend on what an object does, not how. A key trade-off is that inheritance can make code rigid; often composition is more flexible. In Java, multiple inheritance of classes is disallowed to avoid the diamond problem, but multiple interfaces are allowed.

## If they dig deeper

**What is the difference between abstraction and encapsulation?**

Encapsulation is about bundling data and methods and restricting access to protect state; abstraction is about providing a simplified interface that hides implementation details. You encapsulate by making fields private and exposing getters/setters; you abstract by defining an interface or abstract class that specifies behavior without revealing how it works.

**What is the diamond problem and how does Java avoid it?**

The diamond problem occurs when a class inherits from two classes that have a common ancestor with the same method, causing ambiguity about which implementation to use. Java disallows multiple inheritance of classes, so the problem cannot occur with classes. However, a class can implement multiple interfaces, and if two interfaces declare the same default method, the implementing class must override it to resolve the conflict.

**When would you prefer composition over inheritance?**

Composition is preferred when you want to reuse functionality without an 'is-a' relationship, or when the parent class is likely to change in ways that would break subclasses. Composition gives you more flexibility because you can swap components at runtime and avoid inheriting unnecessary members. A common rule of thumb is 'prefer composition over inheritance' unless there is a clear is-a relationship and the base class is stable.

**Explain compile-time vs runtime polymorphism with examples.**

Compile-time polymorphism is method overloading: multiple methods with the same name but different parameter lists, and the compiler chooses which one to call based on the arguments at compile time. Runtime polymorphism is method overriding: a subclass provides a different implementation of a superclass method, and the JVM dispatches to the subclass version based on the actual object type at runtime. For instance, overloading Math.max for int and double, versus overriding toString() in a subclass.

**How does the Liskov Substitution Principle relate to inheritance, and what can go wrong if violated?**

LSP says that objects of a superclass should be replaceable with objects of a subclass without altering the correctness of the program. If a subclass overrides a method to throw an exception or changes the postcondition, code that works with the superclass may break. A classic violation is a Square class extending Rectangle and overriding setWidth to also set height, so a test expecting a rectangle's area to change only with width fails when given a square.

## Worked example

Consider a simple shape hierarchy: an interface Shape with a method double area(). A Circle class has a private radius field and implements area() as Math.PI * radius * radius. A Rectangle class has private width and height and implements area() as width * height. A method printArea(Shape s) calls s.area() without knowing the concrete type. When passed a Circle with radius 2, output is approximately 12.57; when passed a Rectangle 3 by 4, output is 12.0. This demonstrates abstraction through the Shape contract, polymorphism through dynamic dispatch, and encapsulation by keeping fields private.

## Common traps

- Confusing abstraction with encapsulation: abstraction hides implementation details behind a contract, while encapsulation protects internal state and bundles data with methods.
- Assuming multiple inheritance is universally bad: C++ and Python support it (with mechanisms like virtual inheritance), while Java and C# omit it for classes but allow multiple interfaces.
- Overusing inheritance just to reuse code, leading to fragile base class problems and tight coupling; composition is often a better default.
- Saying 'polymorphism' without distinguishing overloading (compile-time) from overriding (runtime), which can mislead about when the method is resolved.

</details>

---

## 12. Trees · typed · Hard

*dsa · gate confidence 0.85*

<sub>to object to this card: `## trees` then `match: Compute the maximum path sum for the tree: root -10, left ch`</sub>

**Question**

Compute the maximum path sum for the tree: root -10, left child 9, right child 20, where 20's left child is 15 and right child is 7.

**Reference answer**

42. Leaf 15 returns 15, leaf 7 returns 7. At node 20, the split path is 15 + 20 + 7 = 42, and it returns 35 to the root. At root -10, the split path is -10 + 9 + 35 = 34, so the global maximum remains 42.

**Graded on**

- Leaf gains are 15 and 7
- Node 20 split path is 42
- Node 20 returns 35 to root
- Global maximum is 42

<details><summary>The lesson this came from</summary>

In an interview context, a tree is a rooted, acyclic graph of nodes; each node stores a value and, in a binary tree, up to two child pointers labeled left and right. Many tree problems reduce to processing the root and then recursively processing the two subtrees. A binary search tree adds an ordering invariant: all values in the left subtree are less than the root and all values in the right subtree are greater. Balanced variants such as red-black trees and B-trees keep height logarithmic for systems work, but interview problems usually present plain binary trees or BSTs and ask you to reason about shape and order.

## Why interviewers ask this

Interviewers use tree problems to test whether you can decompose a recursive structure and avoid visiting nodes repeatedly, because hierarchical data appears in parsers, file systems, and database indexes. The frequency data here shows maximum path sum, BST validation, LCA, and serialization asked by companies such as DoorDash, LinkedIn, Bloomberg, Citadel, Uber, and Yahoo, so these questions also test whether you can keep per-node state and convert recursive structure to a flat format.

## The core idea

Trees are recursive by definition: the answer for a node can usually be expressed from the answers for its left and right children plus the node's own value. Pick the traversal that matches the problem; DFS is the default for recursive tree work, while BFS uses a queue when level order or breadth-related questions are asked. For a BST, inorder traversal produces sorted order, and a search can eliminate one entire subtree at every step. The biggest performance risk is shape: a tree that is unbalanced behaves like a linked list, so common tree algorithms degrade from O(log n) to O(n) in depth and sometimes O(n) stack space. Therefore, state the base case for null first, then define exactly what each recursive call returns.

## Key points

- Recursive DFS on a binary tree visits n nodes in O(n) time and uses O(h) call-stack space, where h is the tree height; for a balanced tree h is O(log n) and for a skewed tree h is O(n).
- In-order traversal of a BST yields values in strictly increasing order when duplicates are absent.
- A BST is not valid just because each immediate child is on the correct side; a node's left subtree must contain only values less than the node, which is checked by passing range bounds.
- A binary tree can be serialized with preorder traversal plus explicit null markers, and the original structure can be reconstructed in O(n) time.
- Preorder plus inorder traversal uniquely determines a binary tree when values are distinct because preorder's first element is the root and inorder splits the remaining nodes into left and right subtrees.

## Your 60-second answer

A tree is a hierarchical data structure where nodes are connected by edges, with a single root and no cycles. In coding interviews, this usually means a binary tree: each node has at most two children, and the tree is either null or a node plus two subtrees. Most problems are solved by picking a traversal, usually recursive DFS for depth-based questions or BFS with a queue for level-order questions, and then computing a result per node that gets returned up the tree. A binary search tree adds the invariant that all keys in the left subtree are less than the root and all keys in the right subtree are greater. The main trade-off is that an unbalanced tree can make DFS use O(n) stack or recursion space, while a balanced tree keeps height at O(log n) and search, insertion, and deletion in a BST become O(log n).

## If they dig deeper

**How do you compute the maximum depth of a binary tree?**

Recurse: if the node is null, return 0. Otherwise return 1 plus the maximum of the depths of the left and right children. This visits every node once, so it is O(n) time and O(h) call-stack space.

**How do you check whether a binary tree is a valid BST?**

Pass a valid range down the tree: left subtree values must be in (min, root.val) and right subtree values in (root.val, max). Comparing each node only to its direct children is not enough, because a grandchild can violate the root's bound. An inorder traversal can also work by requiring the previous value to be strictly smaller.

**How do you find the lowest common ancestor of two nodes in a BST?**

Walk from the root; if both p and q are less than the current value, move left, and if both are greater, move right. Otherwise, one value is on each side or equals the current value, so current must be the LCA. This is O(h) time and O(1) extra space.

**How do you serialize and deserialize a binary tree?**

Use preorder traversal and write a marker, often '#', for null nodes, with a delimiter between values. Deserialization consumes tokens in preorder: a marker returns null, and a value creates a node, then recursively builds left and right subtrees. That runs in O(n) time and O(n) space.

**How do you solve Binary Tree Maximum Path Sum in O(n)?**

Do a postorder traversal. At each node, clamp left and right child gains to 0 so negative single-direction paths are ignored, update the global answer with node.val + left_gain + right_gain, and return node.val + max(left_gain, right_gain) to the parent. This handles negative values correctly because an all-negative tree falls back to the largest single node.

## Worked example

Take root = [-10, 9, 20, null, null, 15, 7] from the maximum path sum problem. At leaf 15, clamped left and right gains are 0, so it returns 15; at leaf 7, it returns 7. At node 20, the left gain is 15 and the right gain is 7, so the best path that passes through 20 and splits is 15 + 20 + 7 = 42, and node 20 returns 20 + max(15, 7) = 35 to root. At root -10, the left gain from node 9 is 9 and the right gain is 35, so the best split path through root is -10 + 9 + 35 = 34. The global maximum stays 42, which is the correct answer.

## Common traps

- Checking a BST by only comparing each node with its immediate children; a value can be on the correct side of its parent and still violate an ancestor's bound.
- Using recursive DFS without acknowledging that a skewed tree of 10^4 or 10^5 nodes may exceed the call stack in some language runtimes.
- Returning the root-splitting sum from Maximum Path Sum instead of the best single-direction gain; the final path does not need to pass through the root.
- Choosing DFS where BFS is required for level-order output; DFS does not preserve sibling grouping by level.

</details>

---

## 13. Collections Framework · typed · Medium

*java · gate confidence 0.85*

<sub>to object to this card: `## java-collections-framework` then `match: What is the core design principle of the Java Collections Fr`</sub>

**Question**

What is the core design principle of the Java Collections Framework, and why does it matter for algorithms?

**Reference answer**

The framework separates collection interfaces from concrete storage strategies, and utility algorithms operate on those interfaces. This lets the same sort, search, or wrapper method work across ArrayList, LinkedList, HashSet, and other implementations.

**Graded on**

- Interfaces define behavior, implementations define storage
- Algorithms operate on interfaces
- Same algorithm works across implementations

<details><summary>The lesson this came from</summary>

The Java Collections Framework is the set of interfaces, implementations, and algorithms in java.util for representing and manipulating groups of objects as a single unit. Its core interfaces are Collection (extending Iterable) with subinterfaces List, Set, Queue, and Deque; Map is part of the framework but does not extend Collection. Concrete classes include ArrayList, LinkedList, HashSet, TreeSet, PriorityQueue, HashMap, TreeMap, and concurrent variants. The Collections utility class provides static methods such as sort, binarySearch, shuffle, and unmodifiable views.

## Why interviewers ask this

Interviewers use Collections questions to test whether you know which data structure to choose under real constraints: ordering, duplicates, null handling, thread safety, and time complexity. They also probe whether you understand the difference between interface contracts and implementation guarantees, because that is what prevents production bugs. The framework is so central to Java code that weak answers here signal weak practical Java.

## The core idea

The framework separates contracts from implementations: program to List, Set, or Map rather than to ArrayList or HashMap, so you can swap implementations. The four main data structure shapes are ordered sequences with index access (List), unique unordered or sorted elements (Set), key-value mappings (Map), and FIFO/priority task queues (Queue/Deque). Each implementation has a specific backing structure: ArrayList is a resizable array, LinkedList is a doubly-linked list, HashSet is a hash table, TreeSet is a red-black tree. Choosing a collection means matching expected operations to these underlying structures: O(1) get by index for ArrayList versus O(1) insertion at ends for LinkedList. The Collections utility class supplies polymorphic algorithms that operate on these interfaces, such as sort and binarySearch.

## Key points

- The Collection interface extends Iterable and is the root of List, Set, Queue, and Deque; Map is part of the Collections Framework but does not extend Collection.
- ArrayList is a resizable array with O(1) get/set by index and amortized O(1) add at the end, while LinkedList is a doubly-linked list with O(1) add/remove at either end.
- HashSet and HashMap provide average O(1) contains/get/put with good hash distribution but no iteration-order guarantee; LinkedHashSet and LinkedHashMap preserve insertion order.
- TreeSet and TreeMap store elements in sorted order in a red-black tree, giving O(log n) operations; a comparator or natural ordering defines the order.
- Collections is a utility class of static methods such as sort (for lists), binarySearch, shuffle, reverse, and unmodifiableList.

## Your 60-second answer

The Java Collections Framework is the set of interfaces, implementations, and algorithms in java.util for storing and manipulating groups of objects. The core interfaces are Collection, with subinterfaces List, Set, Queue, and Deque, plus Map, which is part of the framework but does not extend Collection. List gives ordered, index-based access; Set enforces uniqueness; Map stores key-value pairs; Queue handles FIFO or priority access. Choosing the right implementation depends on your operation pattern: ArrayList is a resizable array with O(1) get by index, LinkedList is a doubly-linked list with O(1) insertion at the ends, HashSet gives average O(1) contains without order, and TreeSet gives sorted order at O(log n). One trade-off is that ArrayList's fast random access costs O(n) insertion or removal in the middle, so a LinkedList may be better for frequent additions at the head or tail.

## If they dig deeper

**What is the difference between Collection and Collections?**

Collection is the root interface of most collection types, extended by List, Set, and Queue. Collections is a utility class in java.util containing static methods such as sort, binarySearch, shuffle, and unmodifiableList that operate on Collection instances. Mixing them up is a common interview slip.

**How do ArrayList and LinkedList differ in performance and when should you use each?**

ArrayList is backed by a dynamic array, so get and set by index are O(1), but inserting or removing in the middle is O(n) because elements shift. LinkedList is a doubly-linked list, so get by index is O(n), but inserting or removing at either end is O(1) and removal of a known node is O(1). Use ArrayList for random access and typical iteration, and LinkedList for frequent add/remove at the ends, like a queue or deque.

**Why is HashMap not ordered and what do LinkedHashMap and TreeMap do differently?**

HashMap spreads entries across buckets using the key's hash code, so iteration order depends on hash distribution and capacity, not insertion or sort order. LinkedHashMap maintains a doubly-linked list through entries to preserve insertion order (or access order if configured). TreeMap stores entries in a red-black tree sorted by natural key order or a comparator, giving O(log n) operations and sorted views.

**What does Collections.unmodifiableList return and can the original list still change?**

unmodifiableList returns a read-only view backed by the original list; any mutating method on the view throws UnsupportedOperationException. Changes to the underlying list are still visible through the unmodifiable view, so it is not a deep immutable copy. To prevent external mutation, do not retain a reference to the backing list.

**How is PriorityQueue different from a sorted list, and is it thread-safe?**

PriorityQueue is a heap-based queue where the head is always the least element according to natural order or a supplied comparator, but the rest of the elements are not necessarily sorted; add and poll are O(log n) and peek is O(1). Unlike a TreeSet, it allows duplicates and does not store all elements in sorted order. It is not thread-safe; use PriorityBlockingQueue for concurrent access.

## Worked example

Given an ArrayList<Integer> with five elements [10,20,30,40,50], inserting 15 at index 1 shifts elements 20 through 50 one position right, which is O(n) because all trailing elements move. A LinkedList<Integer> with the same five elements inserts at index 1 by adjusting two node references, but to reach index 1 it must traverse from the head, making add(index, element) O(n) as well. The LinkedList's O(1) insertion advantage only applies at the ends using addFirst/addLast or with an iterator at the insertion point. For a PriorityQueue<Integer> with [5,1,3], peek returns 1, the least element; after poll, the heap internally adjusts and peek returns 3.

## Common traps

- Saying Map extends Collection; Map is part of the framework but is a separate interface hierarchy, so methods like add or iterator do not apply.
- Claiming HashMap iteration order is insertion or sorted; HashMap makes no order guarantee, while LinkedHashMap preserves insertion order and TreeMap sorts keys.
- Assuming unmodifiable views are deeply immutable copies; they are backed by the original collection and reflect later changes to it.
- Using PriorityQueue for sorted iteration; it only guarantees the head is the least element, and iterating with its Iterator may yield elements in no particular order.

</details>

---

## 14. ATM System Design · flash · Easy

*lld · gate confidence 0.85*

<sub>to object to this card: `## lld-atm-system-design` then `match: During a normal ATM session, at what points is the customer'`</sub>

**Question**

During a normal ATM session, at what points is the customer's card returned or released by the machine?

**Reference answer**

The card is returned on normal session completion, when the customer cancels, or when the session times out.

**Graded on**

- The ATM retains the card for the entire active session.
- Normal completion causes card return.
- Cancellation causes card return.
- Timeout causes card return.

<details><summary>The lesson this came from</summary>

An ATM design models a single-user session as a state machine that moves from idle through card reading, PIN authentication, transaction selection, and completion or abort. A central controller coordinates hardware components such as the card reader, keypad, screen, cash dispenser, deposit slot, receipt printer, and bank network link. Transactions are represented as objects with state and amount, and money movement must stay consistent across both ATM hardware and the bank system.

## Why interviewers ask this

The interviewer is testing whether you can model a finite-state machine with valid and invalid transitions, keep authentication separate from transaction execution, and preserve correctness under hardware failures like a cash jam or lost network response. They also want to see how you handle partial operations where the ATM and bank must agree on what actually happened.

## The core idea

Keep two layers of state: the ATM session state and the per-transaction state. Authentication is a gate: the card and entered PIN are sent to the bank, and no transaction is allowed before authentication succeeds. For withdrawal, the bank authorizes and holds funds first, the dispenser delivers the exact amount, and only then does the ATM send a completion so the bank settles the debit. Deposits, especially checks, are recorded but not immediately credited to the account. The ATM serves one customer at a time and must return to idle after cancel, eject, or transaction completion.

## Key points

- The ATM session usually moves through Idle, CardInserted, Authenticated, TransactionSelected, Processing, and EjectCard states, with cancel returning toward idle.
- PIN authentication is done by sending the card data and entered PIN to the bank, and the ATM keeps the card until the session ends.
- A withdrawal must reserve or hold funds at the bank, dispense the requested amount exactly, and then send completion so the bank settles the debit.
- Cash and check deposits are not immediately added to the account balance; they are recorded and require bank verification.
- The card reader, keypad, screen, cash dispenser, deposit slot, printer, and network link are coordinated by a transaction/state controller.

## Your 60-second answer

An ATM is a finite-state machine. The machine starts in Idle. A card insert moves it to CardInserted; the user enters a PIN on the keypad, and the ATM sends the card and PIN to the bank for authentication. Only after authentication can the user select balance inquiry, withdrawal, deposit, or transfer. For withdrawal, the ATM asks the bank to authorize and hold the amount, then the cash dispenser dispenses the exact amount using available note denominations, and only then does the ATM send a completion message so the bank settles the debit. If dispensing fails, the ATM logs the failure and reverses the hold or flags it for reconciliation. Deposits are recorded but not credited until the bank verifies them. Cancel or eject returns the machine to Idle. The main trade-off is that adding user-friendly state transitions must still protect the cash and the account balance under hardware failure.

## If they dig deeper

**What states does an ATM session go through?**

A typical session moves through Idle, CardInserted, Authenticated, TransactionSelected, Processing, and EjectCard. Card insertion moves from Idle to CardInserted; successful PIN authentication moves to Authenticated; after choosing a transaction it enters TransactionSelected and then Processing; completion or cancel moves to EjectCard and back to Idle. Invalid PIN usually returns to CardInserted or ejects the card after a small retry limit.

**How is authentication separated from transactions?**

The card and entered PIN are sent to the bank for verification before any transaction is offered. The ATM does not trust the card alone; the authenticated session is a precondition guard on transaction objects. No balance inquiry, withdrawal, deposit, or transfer can execute until that guard is satisfied.

**Why are check deposits not credited instantly?**

Checks must be verified by the bank, so the ATM records the deposit amount and captured check data but leaves the account balance unchanged until the bank approves it. Cash deposits may be counted immediately, but many banks still defer availability until the cash is verified.

**What happens if cash is counted but a note gets stuck in the dispenser?**

This is a partial dispensing failure. The ATM logs the dispensed note count versus the requested amount and does not send success if the count is short. The bank authorization should be reversed or moved to manual reconciliation, because the physical cash and bank ledger no longer match.

**How do you handle a crash or reboot halfway through a withdrawal?**

Persist a unique transaction id and the current state before calling the bank or driving hardware. On restart, query the bank for open authorizations: if cash was not dispensed, reverse the hold; if cash was dispensed but completion was not sent, send completion; if the outcome is unknown, block the transaction and create a manual reconciliation record.

## Worked example

A customer inserts a card and enters a PIN. The ATM sends the card and PIN to the bank and receives an authenticated session. The customer selects withdraw $100 from checking. The ATM first checks the cash dispenser inventory and finds five $20 notes available. It sends a withdrawal authorization for $100; the bank places a hold and returns an approval code. The dispenser dispenses five $20 notes, totaling exactly $100. It then sends a completion message with the transaction id, and the bank settles the $100 debit. If the dispenser had only four $20 notes, the ATM would reject the withdrawal or offer a different amount before authorization, rather than debiting $100 and dispensing only $80.

## Common traps

- Allowing any transaction before PIN authentication succeeds, which breaks the security boundary.
- Saying the bank debits the account at authorization time for a withdrawal; it is a hold until completion.
- Treating cash dispensing as atomic and ignoring partial failures such as a note jam or short dispense.
- Describing check deposits as immediately available in the account balance before bank verification.

</details>

---

## 15. DDL/DML/DCL/TCL · typed · Medium

*sql · gate confidence 0.85*

<sub>to object to this card: `## sql-ddl-dml-dcl-tcl` then `match: What privilege boundary separates DDL from DML, and why does`</sub>

**Question**

What privilege boundary separates DDL from DML, and why does it matter?

**Reference answer**

DML requires table-level and sometimes column-level SELECT/INSERT/UPDATE/DELETE privileges on existing objects, while DDL requires broader object-creation rights such as CREATE on a schema or database. This separation lets application and reporting users modify rows without being able to change the schema.

**Graded on**

- DML uses table/column privileges
- DDL requires schema/database creation rights
- Separation supports least privilege

<details><summary>The lesson this came from</summary>

SQL statements are conventionally divided into four categories based on what they affect. DDL (Data Definition Language) includes CREATE, ALTER, DROP, and TRUNCATE, which define or remove schema objects such as tables, indexes, and views. DML (Data Manipulation Language) includes SELECT, INSERT, UPDATE, DELETE, and MERGE, which read or modify rows inside existing objects; some taxonomies split SELECT into a separate Data Query Language. DCL (Data Control Language) includes GRANT, REVOKE, and in SQL Server/Sybase DENY, which manage privileges. TCL (Transaction Control Language) includes COMMIT, ROLLBACK, and SAVEPOINT (SAVE TRANSACTION in SQL Server), which determine whether a multi-statement unit becomes permanent.

## Why interviewers ask this

Interviewers use this question to separate candidates who know SQL syntax from those who understand operational consequences. The real signals are whether you know which statements can be rolled back, which cause implicit commits on a given engine, and why TRUNCATE behaves like a schema change rather than a row delete. A strong answer names the categories and then immediately attaches the engine-specific transaction behavior.

## The core idea

The useful distinction is what each category changes: DDL changes the catalog or schema, DML changes row data, DCL changes authorization, and TCL changes when other work becomes durable. The categories matter because their runtime behavior differs: DDL acts on metadata, may implicitly commit, and does not accept a WHERE clause, while DML can participate in an explicit transaction. In Oracle and MySQL DDL usually causes implicit commits; PostgreSQL allows many DDL statements inside transactions. Misclassifying TRUNCATE as DML therefore leads to wrong assumptions about rollback, filtering, and identity reset behavior.

## Key points

- DDL includes CREATE, ALTER, DROP, and TRUNCATE; these change schema objects, and in Oracle and MySQL they usually cause implicit commits.
- DML includes SELECT, INSERT, UPDATE, DELETE, and MERGE; it reads or modifies row data and stays within an open transaction in engines that support transactional DML.
- DCL includes GRANT and REVOKE; DENY is a SQL Server/Sybase extension, not part of standard SQL.
- TCL includes COMMIT, ROLLBACK, and SAVEPOINT (SAVE TRANSACTION in SQL Server); rolling back to a savepoint undoes only later work and does not end the outer transaction.
- TRUNCATE is DDL rather than DML: it removes all rows, does not accept a WHERE clause, and its rollback and reset behavior differs from DELETE by engine.

## Your 60-second answer

SQL is split into four groups by effect. DDL — CREATE, ALTER, DROP, TRUNCATE — changes the schema: tables, indexes, views. DML — INSERT, UPDATE, DELETE, and often SELECT — reads or changes rows inside existing objects. DCL — GRANT, REVOKE, and in SQL Server DENY — controls permissions. TCL — COMMIT, ROLLBACK, and SAVEPOINT — controls whether a group of statements becomes permanent. The practical distinction is rollback behavior: DML runs inside transactions, while DDL often implicitly commits in Oracle and MySQL, though PostgreSQL allows more transactional DDL. TRUNCATE removes all rows but is DDL, so its logging and rollback behavior differ from DELETE. That distinction is usually what the interviewer is checking.

## If they dig deeper

**Is SELECT a DML command or a separate category?**

Most working summaries group SELECT with DML because it manipulates data, but a stricter taxonomy separates reads into DQL (Data Query Language). In an interview, say it is often included under DML; the important point is that SELECT does not modify data and usually participates in the same transaction model as other DML.

**Why is TRUNCATE considered DDL instead of DML?**

TRUNCATE acts on the table as a whole rather than on individual rows; it has no WHERE clause and often resets identity values. Because it is DDL, engines like Oracle and MySQL may treat it as an implicit-commit operation, whereas DELETE is transactional DML and can filter rows.

**What happens to an active transaction when you run a DDL statement in Oracle versus PostgreSQL?**

In Oracle, DDL issues an implicit commit before and after the statement, so prior work cannot be rolled back afterward. In PostgreSQL, CREATE, ALTER, DROP, and TRUNCATE can run inside a transaction block and be rolled back normally. MySQL also causes implicit commits for most DDL.

**How does a savepoint differ from COMMIT or ROLLBACK?**

COMMIT makes the entire transaction durable, and ROLLBACK undoes the whole transaction. A savepoint marks a point inside the transaction; ROLLBACK TO SAVEPOINT, or ROLLBACK TRANSACTION savepoint_name in SQL Server, undoes only later statements and leaves the outer transaction open, so you still must COMMIT or ROLLBACK the whole unit.

**Can you combine DDL, DML, DCL, and TCL into one transaction in a portable way?**

Not portably. DML and TCL work together in all transactional engines, but DDL and DCL transaction behavior varies sharply: PostgreSQL generally supports transactional DDL, Oracle and MySQL often commit implicitly, and SQL Server supports many but not all DDL operations transactionally. You need to check the engine's rules before relying on rollback of schema or permission changes.

## Worked example

In SQL Server, a warehouse application first creates an inventory table with DDL: `CREATE TABLE Inventory (id INT PRIMARY KEY, qty INT NOT NULL);`. DCL gives the app access: `GRANT SELECT, UPDATE ON Inventory TO warehouse_app;`. A transaction then inserts and later updates a row using DML: `BEGIN TRANSACTION; INSERT INTO Inventory (id, qty) VALUES (1, 100); SAVE TRANSACTION after_insert; UPDATE Inventory SET qty = 90 WHERE id = 1;`. Rolling back to the savepoint with `ROLLBACK TRANSACTION after_insert;` undoes the UPDATE but keeps the INSERT; a final `COMMIT;` makes the inserted row durable. This separates schema creation, permission, row changes, and transaction control to show why each category exists.

## Common traps

- Listing TRUNCATE as DML because it deletes data; it is DDL, has no WHERE clause, and may implicitly commit, so its failure behavior is very different from DELETE.
- Claiming all DDL can never be rolled back; PostgreSQL allows many DDL statements inside transactions, while Oracle and MySQL usually do not.
- Presenting DENY as standard SQL DCL; DENY is a SQL Server/Sybase extension, and standard SQL defines GRANT and REVOKE.
- Ignoring that SELECT is often separated as DQL in stricter taxonomies; if you insist it is DML without noting the split, you can look unaware of the common classification debate.

</details>

---

## 16. Idempotency · flash · Easy

*system_design · gate confidence 0.85*

<sub>to object to this card: `## sd-idempotency` then `match: How long should idempotency keys be retained?`</sub>

**Question**

How long should idempotency keys be retained?

**Reference answer**

Longer than the client's maximum retry window, including timeouts and backoff, but they can be deleted after that business-defined retention period.

**Graded on**

- retain beyond max retry window
- not forever
- deleting too early recreates duplicate side effects

<details><summary>The lesson this came from</summary>

Idempotency is a property of an operation: executing it once or many times leaves the system in the same state and returns an equivalent result, so retries do not create extra side effects. In HTTP, PUT and DELETE are idempotent by design, while POST is not idempotent unless the client supplies an idempotency key. For non-idempotent operations such as payments, the server stores the key and the original response, then replays that response on retries instead of re-executing the business logic. Proper handling includes atomic key insertion and explicit handling of requests that arrive while the original is still in progress.

## Why interviewers ask this

Interviewers use idempotency questions to test whether a candidate can design APIs that tolerate network failures, client retries, and duplicated messages without corrupting state. The signal is practical distributed-systems judgment: knowing which HTTP methods are naturally idempotent, when an idempotency key is required, and how to close race conditions around concurrent duplicate requests. Real systems such as payment processing and order management depend on this to avoid double charges and duplicate inventory deductions.

## The core idea

The core mechanism is a client-generated idempotency key, usually a UUID, sent with each non-idempotent request. The server must insert a record for that key atomically—under a unique constraint—with a status such as PENDING or IN_PROGRESS before performing the side effect. If a retry arrives while the first request is still running, the server must handle the in-flight state explicitly, typically by returning HTTP 409 Conflict or waiting, not by assuming the stored response is ready. Once the operation completes, the server records the response and maps it to the key; subsequent retries return that stored response without re-executing the operation. Keys should expire after a limited time to bound storage, and clients should generate a new key for a genuinely new operation. This pattern converts an unsafe retry into a safe replay.

## Key points

- PUT and DELETE are idempotent by HTTP semantics; GET is both safe and idempotent; POST is not idempotent unless an idempotency key is supplied.
- For payment-like POST operations, the server must insert the idempotency key with a PENDING status under a unique constraint before calling external systems, so concurrent duplicates are caught by the database.
- If a duplicate request finds the key in PENDING, the server should return HTTP 409 Conflict, wait, or expose the pending state rather than reading an incomplete row or executing again.
- Idempotency keys are typically UUIDs generated by clients and are usually stored with a TTL to bound storage; Stripe and PayPal recommend UUID-based keys for payment APIs.
- At-least-once message delivery requires consumer-side deduplication: storing processed message IDs with a unique constraint so reprocessing a message does not repeat its side effects.

## Your 60-second answer

Idempotency means that calling an operation many times has the same effect as calling it once, so a client can retry safely when a response is lost. In HTTP, PUT and DELETE are naturally idempotent, and GET is safe, but POST usually is not. For POST, especially payments, the client generates a unique idempotency key, often a UUID, and sends it in a header. The server stores that key in a database with a PENDING status before doing the work, using a unique constraint to make the insert atomic. If the same key arrives again and the operation is done, the server returns the stored response instead of charging again. If the original request is still in flight, the server returns a conflict or waits rather than executing twice. That prevents double charges when a network timeout causes a retry.

## If they dig deeper

**What is the difference between a safe HTTP method and an idempotent HTTP method?**

A safe method, like GET, does not modify server state at all. An idempotent method may modify state, but repeating the same request produces the same result as one request. PUT and DELETE are idempotent but not safe because they change resource state.

**How would you make a POST /payments endpoint idempotent from scratch?**

Require clients to send a unique idempotency key, often in a header like Idempotency-Key. On the server, insert a row with that key and status PENDING in a table with a unique constraint before calling the payment provider. If the operation completes, update the row with the response and transaction ID; on duplicate keys return the stored response or, if the row is still PENDING, return HTTP 409 Conflict.

**What race condition occurs if you only record the idempotency key after the payment succeeds?**

Two concurrent requests with the same key can both look up the key, find it missing, and both execute the payment before either writes it. The fix is to reserve the key first by inserting it with PENDING status, relying on the database's unique constraint to let only one request win and making the other observe a conflict.

**How do you apply idempotency in an at-least-once message queue consumer?**

Store processed message IDs in a deduplication table with a unique constraint, or use the message key as the primary key when writing the result. Process the message and mark the ID processed atomically where possible, such as in the same transaction as the side effect, so a redelivered message is recognized and skipped instead of duplicating state changes.

## Worked example

Client A sends POST /payments with Idempotency-Key: 8f14... and body amount=50. Before calling the payment gateway, the server runs INSERT INTO idempotency_keys(key, status) VALUES('8f14...', 'PENDING') under a UNIQUE constraint on key. The insert succeeds, and the server calls the gateway. The gateway debits the customer but the response times out, so the client retries with the same key. The server's INSERT fails with a duplicate-key error; it reads the row, sees status PENDING, and returns HTTP 409 with Retry-After instead of calling the gateway again. When the original request completes, it updates the row to SUCCESS with gateway_txn_id=t_123. A third retry with the same key finds the row SUCCESS and immediately returns the stored 200 response and t_123 without a second charge.

## Common traps

- Storing the idempotency key only after the side effect succeeds leaves a race window where two concurrent requests can both execute the operation before either writes the key.
- Assuming a duplicate key means the stored response is ready can cause the server to read a missing or PENDING row while the first request is still running.
- Making every endpoint idempotent by changing POST to PUT without respecting PUT's full-resource replacement semantics can corrupt data and confuse clients.

</details>

---

## 17. CAP theorem · typed · Medium

*system_design · gate confidence 0.85*

<sub>to object to this card: `## sd-cap-theorem` then `match: Why do interviewers ask about CAP in system design problems?`</sub>

**Question**

Why do interviewers ask about CAP in system design problems?

**Reference answer**

To see whether you can reason about behavior under failure rather than recite labels. They expect an explicit per-operation CP or AP choice, justified by the impact of stale data, and tied back to replication and partitioning decisions.

**Graded on**

- Reason under failure, not just recite labels
- Choose CP or AP per operation
- Justify by data-staleness impact and replication/partitioning

<details><summary>The lesson this came from</summary>

CAP theorem, also known as Brewer's theorem, was formalized by Gilbert and Lynch and says an asynchronous distributed data store cannot simultaneously guarantee linearizable consistency, 100% availability, and partition tolerance. Consistency here means all operations appear to execute atomically in a single total order, so every read returns the value of the most recent completed write. Availability means every request to a non-failed node receives a non-error response, even if it contains stale data. Since network partitions happen in any multi-node deployment, real systems choose consistency by rejecting some requests or availability by serving possibly stale data during a partition.

## Why interviewers ask this

In design interviews, CAP is used to probe whether you can articulate the real operational tradeoff instead of reciting database categories. The interviewer wants to hear which guarantee you give up under a network partition and why, especially in questions like a key-value store, distributed queue, or live page-view counter. A strong answer demonstrates that the choice is conditional on partitions and not a permanent property of every request.

## The core idea

CAP is not a static two-of-three menu. When no partition exists, a replicated system can be both linearizable and available: reads can follow writes and nodes can answer. The conflict appears only when messages between nodes are lost or delayed: a node that answers immediately may not know about a newer write on the other side of the partition, so it must either return stale data or refuse to answer. Because partition tolerance is effectively mandatory for any useful distributed system in a real network, the practical decision is CP versus AP during a partition. The theorem is also about absolute guarantees; production systems typically tune quorums, timeouts, and bounded staleness rather than choosing perfect C or perfect A. PACELC extends this by adding the normal-case latency-versus-consistency tradeoff.

## Key points

- In CAP, consistency is linearizability: operations behave as if executed atomically in a single total order, and every read returns the value of the most recent completed write.
- Availability means every request to a non-failed node receives a non-error response; returning an error because a partition prevents consistency is an availability sacrifice, not part of the consistency definition.
- Partition tolerance is the ability to keep operating despite arbitrary dropped or delayed messages between nodes, and it is effectively mandatory in a multi-node system.
- CAP only forces a choice between consistency and availability when a partition exists; without a partition, a system can provide both at once.
- 'CA' is not a real distributed-system option because partitions can occur; it typically describes a single-node or non-replicated system.

## Your 60-second answer

CAP says that during a network partition, a distributed system has to choose between consistency and availability; it cannot guarantee both perfectly at the same time on both sides of the partition. Consistency in CAP is linearizability: every read must return the value of the most recent completed write, with operations appearing to happen atomically. Availability means every request to a node that hasn't crashed gets a non-error response. If I keep answering during a partition, I may not know about a newer write on the other side, so I risk returning stale data. If I insist on linearizability, I may reject or time out requests until the partition heals. The choice only exists during a partition; when the network is healthy, the same system can be both consistent and available. That is why a banking ledger typically favors CP, while a social media feed or page-view counter can favor AP and tolerate temporary staleness.

## If they dig deeper

**What do the C, A, and P in CAP actually mean?**

C is linearizability, not 'all replicas are identical at all times': operations must appear to take effect atomically in a single total order, with every read returning the most recent completed write. A means every request to a non-failed node receives a non-error response. P means the system continues operating despite arbitrary network partitions where messages are dropped or delayed. The common phrase 'or an error' describes a system sacrificing availability, not part of the consistency definition.

**Why is CA not a real option for a distributed system?**

A CA system would require every request to succeed and every read to be linearizable even when nodes cannot communicate. If a write reaches one side of a partition, the other side would have to serve stale data or block; those violate C or A. Since practical multi-node systems can experience partitions, CA is effectively limited to a single node or a non-replicated system.

**In a distributed key-value store, how do you decide between CP and AP?**

If stale reads or lost writes cause real harm—balances, inventory, coordination—choose CP, so the system rejects requests it cannot make consistent. If the product can tolerate temporary divergence—profiles, likes, view counts—choose AP and resolve conflicts later. A store can also tune behavior per operation: strongly consistent reads for single items and eventual consistency elsewhere.

**What is the relationship between AP and eventual consistency?**

AP means you stay responsive under partition, but it does not define how copies are reconciled. Eventual consistency is one AP strategy where replicas converge after the partition heals if no new updates occur. It typically needs conflict resolution such as last-write-wins or CRDTs, and it does not provide linearizable reads during the partition.

**Why do many systems claim they provide all three, and what does PACELC add?**

Because CAP only forbids all three during a partition and is about perfect 100% guarantees. When there is no partition, a system can be both linearizable and available. PACELC refines the model: if Partition, choose A or C; Else, choose Latency or Consistency in normal operation. This lets engineers reason about ongoing quorum latency, read repair, and bounded staleness instead of only partition behavior.

## Worked example

Consider a two-node key-value store with replicas A and B. A network partition isolates the two nodes. A client writes key='balance' with value 40 to A, and A acknowledges it; if the system is AP, this write is durable locally but B cannot see it. Another client reads key='balance' from B. An AP design returns the old value 30 immediately, remaining available but stale. A CP design makes B reject or time out the read because it cannot prove this is the most recent completed write, preserving linearizability at the cost of availability. After the partition heals, A and B exchange version metadata and B converges to 40 under a last-writer-wins or application-defined merge rule.

## Common traps

- Saying consistency means 'every read receives the most recent write or an error' misstates CAP: linearizability does not include an error option, and returning that error is an availability sacrifice.
- Claiming a distributed system must permanently give up one of C, A, or P even when there is no partition; CAP only forces the C/A choice during a network partition.
- Calling every RDBMS CP or every NoSQL store AP without checking configuration; behavior depends on replication mode, consistency settings, and whether the system tolerates partitions.
- Assuming an AP system can never return stale data after a partition heals or that a CP system can never be available; AP may have stale reads until convergence, and CP may be fully available when no partition exists.

</details>

---

## 18. Pub/Sub System Design · mcq · Medium

*lld · gate confidence 0.9*

<sub>to object to this card: `## lld-pub-sub-system-design` then `match: In a single-process in-memory pub/sub system with one produc`</sub>

**Question**

In a single-process in-memory pub/sub system with one producer enqueuing FIFO and one consumer draining FIFO, what ordering is guaranteed?

**Options**

- Total order across all topics
- Per-topic per-subscriber order only
- Global order across all subscribers
- No ordering guarantee at all

**Reference answer**

Per-topic per-subscriber order only

**Graded on**

- Single FIFO queue
- One producer and one consumer
- Ordering is per topic per subscriber

<details><summary>The lesson this came from</summary>

Publish-subscribe decouples senders from receivers: publishers send messages to named topics, and a broker delivers a copy to every subscriber of that topic. In a low-level design this is typically modeled as a Topic class holding a subscriber collection, with publication iterating over subscribers and each subscriber having its own queue consumed by a worker thread.

## Why interviewers ask this

The interviewer is testing whether you can turn a messaging pattern into concrete classes, thread safety, and delivery semantics. They want to see that you understand fan-out, backpressure, and the tradeoffs between blocking, dropping, and unbounded queues.

## The core idea

The broker maintains a registry that maps topic names to subscriber lists. When a message is published, the broker fans it out to each subscriber for that topic. If a subscriber is invoked synchronously, one slow subscriber blocks all later subscribers in the loop. Giving each subscriber its own queue and worker thread makes consumption asynchronous, but bounded blocking queues do not fully isolate subscribers: if one subscriber's queue is full, a blocking put stalls the publisher and prevents later subscribers from receiving the message. The choice of queue policy is therefore the central design decision.

## Key points

- A Topic holds the current subscriber list; a publish operation delivers one copy to every subscriber present at the start of that publish.
- Per-subscriber queues and worker threads decouple subscriber speed from publisher speed only when the queue is unbounded or the publisher uses a non-blocking or drop policy.
- With a bounded BlockingQueue and put(), a full queue blocks the publish thread, so subscribers later in the fan-out loop do not receive the message until space is freed.
- Thread-safe collections such as a concurrent map for topics and CopyOnWriteArrayList for subscriber lists are required for concurrent publish and subscribe operations.
- Dropping messages on a full queue gives at-most-once delivery; at-least-once delivery requires acknowledgements, retries, and durable storage.

## Your 60-second answer

I'd model a PubSubBroker with a concurrent map from topic name to Topic. Topic holds a thread-safe list of Subscriber objects. Publish looks up the topic and fans the message out to each subscriber. To keep delivery asynchronous, each subscriber gets its own BlockingQueue and worker thread; publish enqueues rather than invoking the subscriber directly. The tradeoff is the queue policy. If I use a bounded queue with blocking put, one slow subscriber can fill its queue and block the publish thread, which then blocks later subscribers in the fan-out loop. If I use offer with drop, I get at-most-once delivery and fast non-blocking publish. So I'd choose based on whether the system can lose messages or must apply backpressure.

## If they dig deeper

**What is the difference between calling a subscriber directly and using per-subscriber queues?**

Direct invocation makes processing synchronous with the publish call, so a slow subscriber blocks the publisher and all subscribers after it. Per-subscriber queues and worker threads make consumption asynchronous, but the enqueue operation can still block if the queue is bounded and full.

**How do you stop one slow subscriber from affecting other subscribers?**

You choose a backpressure policy. Unbounded queues isolate speed but risk memory exhaustion. Bounded queues with non-blocking offers avoid head-of-line blocking but can drop messages. A separate dispatcher per subscriber can also isolate slow consumers, at the cost of more threads and complexity.

**What delivery semantics can this basic design provide?**

A basic in-memory broker with bounded queues and drop-on-full gives at-most-once delivery. At-least-once requires persistent storage plus subscriber acknowledgements and retries. Exactly-once is much harder and usually requires idempotent subscriber processing and deduplication.

**How do you make subscribe and unsubscribe safe while publishing concurrently?**

Use a thread-safe subscriber list such as CopyOnWriteArrayList. A publish iterates over a snapshot, so a subscriber added mid-publish may not receive that message, and a removed one may still receive it if it was already in the snapshot. This gives clear but weak consistency with no locking around iteration.

**How would this extend to multiple broker nodes, and what happens to ordering?**

You partition topics across nodes. A single topic on one node with a single writer preserves FIFO per subscriber, but concurrent publishers can interleave messages unless serialized. Global ordering across partitions requires sequence numbers and a total order mechanism, which is a much harder distributed systems problem.

## Worked example

A broker has topic orders with subscribers A and B, each using an ArrayBlockingQueue of capacity 1. Publication uses put(). A's worker is stalled; B's worker drains immediately. P publishes m1: put to A succeeds and fills A's queue; put to B succeeds and B's worker immediately takes m1, leaving B's queue empty. P then publishes m2: the fan-out loop reaches A first, and put on A's full queue blocks. B never receives m2, even though B has capacity, until A's worker removes m1 and frees space. This shows independent queues do not isolate subscribers when the publisher uses a blocking bounded queue in a single-threaded fan-out.

## Common traps

- Calling subscriber.onMessage directly inside publish: one slow subscriber blocks the publisher and every subscriber after it in the loop.
- Believing per-subscriber queues fully isolate slow consumers even when using bounded blocking queues; a full queue blocks the publish thread and stalls later subscribers.
- Using unbounded queues as an obvious fix without acknowledging the risk of memory exhaustion under sustained slow subscribers.
- Claiming at-least-once or exactly-once delivery when the basic design simply drops messages on a full queue.

</details>

---

## 19. Indexes · flash · Easy

*sql · gate confidence 0.9*

<sub>to object to this card: `## sql-indexes` then `match: What is a clustered index?`</sub>

**Question**

What is a clustered index?

**Reference answer**

An index that determines the physical order of table rows and stores the row data at its leaf level; a table can have only one.

**Graded on**

- determines physical row order
- leaf pages contain row data
- only one per table

<details><summary>The lesson this came from</summary>

An index is a separate data structure, usually a B-tree, that stores a sorted copy of one or more columns from a database table plus a pointer to the row the values came from. It lets the query planner seek or range-scan on key columns instead of scanning the entire table. Engines differ in clustering: SQL Server has one clustered index that determines physical row order and non-clustered indexes as separate B-trees; MySQL InnoDB always clusters by the primary key; PostgreSQL stores table rows in an unordered heap and all standard indexes are secondary.

## Why interviewers ask this

Interviewers use indexes to test whether you understand real database performance, not just syntax. They want to see you can choose a good index for a given query, reason about composite key order and covering indexes, and explain the write/storage tradeoff. Many candidates can recite CREATE INDEX but cannot predict when an index helps or hurts.

## The core idea

An index is a copy of data organized for search: it speeds up reads because the engine can walk a B-tree instead of scanning every row, but it adds storage and every insert/update/delete must keep the copies in sync. Composite indexes work left-to-right: equality columns position the seek, a range column bounds the scan, and later columns cannot narrow the seek range but can still be applied as predicates inside the index scan before row lookups in engines that support index condition pushdown. Write cost is engine-dependent: in PostgreSQL's append-only MVCC, an UPDATE creates a new tuple version and unless HOT optimization applies, all secondary indexes on the table receive entries for the new version, even when no indexed column changed.

## Key points

- Most general-purpose SQL indexes are B-trees that support O(log n + rows returned) seeks and range scans, compared with O(n) full table scans.
- A composite index on (a, b, c) can only be used efficiently for lookups that include leading columns; a query filtering only on b or c usually cannot use that index for a seek.
- For a WHERE clause with equality on a and range on b, c cannot narrow the seek range, but engines such as MySQL, SQL Server, PostgreSQL and Oracle can still apply c as an index filter while scanning the index.
- In SQL Server, clustered indexes define physical row order and are limited to one per table; MySQL InnoDB always has a clustered primary key; PostgreSQL has no clustered indexes and stores rows in a heap with secondary indexes pointing to row locations.
- In PostgreSQL's MVCC, an UPDATE writes a new tuple version and, unless HOT is possible on the same page, all secondary indexes are updated to point to the new version even if the updated columns are not part of any index.

## Your 60-second answer

A database index is a separate data structure, typically a B-tree, that keeps a sorted copy of one or more columns and pointers to the corresponding rows. It lets the optimizer find rows by seeking or scanning a small range instead of reading the whole table. In exchange, indexes consume storage and write operations must keep them in sync, so write-heavy tables can slow down significantly. How the columns are ordered matters: for a composite index, equality columns must come before range columns, and any column after the range cannot narrow the seek but can still be applied as a filter during the index scan in modern engines. Clustered indexes, where supported, define the table's physical order; non-clustered indexes are separate structures.

## If they dig deeper

**What are the main costs of creating too many indexes?**

Each index duplicates the key columns and adds storage. Writes must update indexes, increasing insert/update/delete latency. In MVCC engines like PostgreSQL, even updating a non-indexed column can force writes to every secondary index unless HOT optimization is possible on the same page.

**Given an index on (a, b, c) and WHERE a = 1 AND b > 2 AND c = 3, how much of the index is used?**

The B-tree can use a as an equality seek and then range scan b > 2. C cannot narrow the start or end of that b range because the index is sorted first by a, then b, so c values are not consecutive for all b > 2. Modern engines such as MySQL, SQL Server, PostgreSQL and Oracle still apply c as a residual predicate inside the index scan, avoiding base table lookups for rows that fail c = 3.

**Explain the difference between clustered and non-clustered indexes.**

A clustered index determines the physical order of table rows; SQL Server allows at most one per table and the leaf level is the data pages. MySQL InnoDB always stores rows in the primary key's clustered B-tree, with secondary indexes holding primary key values to find rows. PostgreSQL has no clustered index concept in its normal storage: rows live in an unordered heap, and every index, including the primary key, is a secondary structure pointing to row locations.

**Why does PostgreSQL update every secondary index when you change a non-indexed column?**

PostgreSQL uses MVCC: an UPDATE does not overwrite the old row, it writes a new physical tuple version. Every secondary index entry points to the physical tuple location, so the database must add entries for the new version into all indexes on the table. The HOT optimization avoids this only when the new tuple fits on the same heap page and no indexed column changes; then old index entries can be redirected via the line pointer, so secondary indexes remain unchanged.

## Worked example

Take an orders table with columns customer_id, order_date, status, and amount, and an index on (customer_id, order_date, status). A query asks: SELECT * FROM orders WHERE customer_id = 42 AND order_date BETWEEN '2024-01-01' AND '2024-06-30' AND status = 'shipped'. The B-tree descends to customer_id 42, then scans the order_date range as a contiguous block. Because the next key column status comes after order_date, it cannot start the scan at the first 'shipped' row inside that range; the scan visits all rows with order_date in that range. With index condition pushdown, the engine evaluates status = 'shipped' on the index entries and only performs base table lookups for rows that pass, avoiding I/O for rows that do not match. Without ICP, every row in the order_date range would trigger a lookup to check status.

## Common traps

- Believing an index on (a,b,c) can speed up a query that filters only on b or c; without leading column a, the B-tree cannot provide a direct seek.
- Over-indexing because each index helps a read; on a write-heavy table, the accumulated index maintenance can dominate and even hurt overall workload.
- Assuming 'c' is useless after a range on 'b' in a composite index; it cannot narrow the seek range but can still be used as an index filter before table access.
- Confusing clustered with unique: a clustered index concerns physical storage order, while a unique index is a constraint that rejects duplicate key values.

</details>

---

## 20. Index seek vs scan · mcq · Hard

*sql · gate confidence 0.9*

<sub>to object to this card: `## sql-index-seek-vs-scan` then `match: An Orders table has 5 million rows and a nonclustered index `</sub>

**Question**

An Orders table has 5 million rows and a nonclustered index on OrderDate. A predicate OrderDate >= '2020-01-01' matches about 4.5 million rows. Which access path is the optimizer most likely to choose?

**Options**

- Nonclustered index seek with key lookups
- Nonclustered index scan only
- Table scan or clustered index scan
- Index seek reading only matching rows

**Reference answer**

Table scan or clustered index scan

**Graded on**

- Large fraction favors sequential scan
- Sequential I/O avoids many random lookups

<details><summary>The lesson this came from</summary>

An index seek traverses the B-tree from root to leaf to locate the first index entry that satisfies a predicate on the leading key column(s), then reads a contiguous subset of leaf entries in key order. An index scan reads the leaf level end-to-end and evaluates a residual predicate on each entry or row; a clustered index scan reads the data rows themselves, while a table scan reads a heap. In SQL Server, a range predicate on a leading index key column produces an Index Seek with Seek Predicates, not an Index Scan.

## Why interviewers ask this

The interviewer is checking whether you can read an execution plan and diagnose why a query is slow. They want to see that you understand how B-tree indexes are navigated and that you can rewrite predicates so the optimizer can choose a seek. It is a practical SQL tuning signal, not just a definition.

## The core idea

A B-tree index is sorted by its key, so equality and range predicates on a leading key let the engine navigate directly to the first matching entry. A seek is cheap when few rows qualify because it reads a narrow slice of the leaf level. A scan touches all leaf pages, so it is the right call when the predicate is not seekable or when most rows are needed. The boundary between seek and scan is governed by predicate shape, called SARGability, and by estimated selectivity. In SQL Server, only an Index Seek uses Seek Predicates to start and stop a range; an Index Scan applies residual predicates while traversing leaf pages.

## Key points

- An index seek uses root-to-leaf B-tree navigation to start at the first qualifying key and then reads only the matching leaf range, while an index scan reads all leaf pages and applies a residual predicate per row.
- In SQL Server, a bounded range on the leading key column is represented as an Index Seek with Seek Predicates, not an Index Scan.
- A predicate is non-SARGable when the indexed column is wrapped in a function or expression or undergoes an implicit data type conversion, which prevents a seek.
- Low selectivity or a missing index can cause the optimizer to choose a scan even when a seek is technically possible.
- A scan can be faster than a seek when the query returns most of the table, because sequential leaf reads may beat many random bookmark lookups.

## Your 60-second answer

An index seek walks the B-tree from root to leaf and starts reading at the first key that satisfies a predicate on the leading index columns, so it reads only the matching slice of the index. An index scan reads the leaf level from one end to the other and evaluates a predicate against every entry. In SQL Server, a bounded range on the leading key appears as an Index Seek with Seek Predicates, not an Index Scan. Scans occur when the predicate is non-SARGable, like applying a function to the indexed column or an implicit type conversion, or when the optimizer estimates that a large fraction of rows will be returned and sequential reading is cheaper than many random lookups. The main trade-off is I/O: seeks are excellent for selective queries, but scanning can win when you are retrieving most of the table.

## If they dig deeper

**What does SARGable mean?**

It means Search ARGument ABLE: the predicate is written so the optimizer can use the indexed column directly without wrapping it in a function or expression. WHERE OrderDate >= '2024-01-01' is SARGable; WHERE YEAR(OrderDate) = 2024 is not, because YEAR must be evaluated on every row before comparison.

**How does the optimizer decide between an Index Seek and an Index Scan?**

It uses statistics about value distribution to estimate the number of rows that qualify and the cost of reading those rows. If selectivity is high, a seek plus any lookups is usually cheaper; if the predicate matches a large percentage of the table, a scan may be cheaper than doing many random key lookups.

**In SQL Server, how is a range predicate on the leading index column represented?**

As an Index Seek operator that lists the range boundaries in its Seek Predicates property. An Index Scan does not have seek predicates; it may show a residual predicate that is evaluated on each row after the leaf page is read.

**Can an index seek still be slow?**

Yes. If the seek returns many rows and a nonclustered index does not cover the query, each row may require a separate bookmark lookup into the clustered index or heap, causing a lot of random I/O. A covering index, included columns, or a scan can be better in that case.

**How would you tune a query with WHERE last_name = ? AND first_name = ? and ORDER BY hire_date?**

A composite index on (last_name, first_name, hire_date) may allow an equality seek on the first two columns and return rows already sorted by hire_date. If the query also selects other columns, add them as included columns to make the index covering. Key column order matters: leading columns must be in equality predicates to make later columns seekable.

## Worked example

Suppose Orders has millions of rows and a nonclustered index on OrderDate. WHERE YEAR(OrderDate) = 2024 is non-SARGable: the engine cannot map 2024 to index bounds because the column is inside YEAR(), so it scans the index's leaf level and applies YEAR() as a residual predicate. Rewriting to WHERE OrderDate >= '2024-01-01' AND OrderDate < '2025-01-01' exposes the range; SQL Server then performs an Index Seek that descends the B-tree to the first key on or after 2024-01-01 and follows forward pointers through the leaf pages until 2025-01-01. If only a small fraction of rows are in 2024, it reads far fewer pages. If 2024 represents most of the table, the optimizer may still pick a clustered index scan because sequential reads beat a large number of bookmark lookups.

## Common traps

- Calling a bounded range read on a leading key column an Index Scan; in SQL Server that is an Index Seek.
- Assuming a seek always returns one row or is always faster than a scan.
- Ignoring implicit conversion: comparing a VARCHAR indexed column to a number can force a scan without a syntax error.
- Saying an Index Scan can use key bounds to start and stop a range; only an Index Seek uses Seek Predicates for that.

</details>

---

## 21. Layer 4 vs Layer 7 load balancing · mcq · Medium

*system_design · gate confidence 0.9*

<sub>to object to this card: `## sd-layer-4-vs-layer-7-load-balancing` then `match: Which statement about modern Layer 4 load balancers is corre`</sub>

**Question**

Which statement about modern Layer 4 load balancers is correct?

**Options**

- They cannot inspect TLS ClientHello extensions.
- They can inspect SNI/ALPN and terminate TLS without parsing HTTP.
- They can parse HTTP headers and route based on cookies.
- They always have higher per-request latency than L7 load balancers.

**Reference answer**

They can inspect SNI/ALPN and terminate TLS without parsing HTTP.

**Graded on**

- Modern L4 can inspect SNI/ALPN
- Can terminate TLS
- Does not parse HTTP application data

<details><summary>The lesson this came from</summary>

Layer 4 load balancing operates at the transport layer (TCP/UDP), using source/destination IP address, ports, and protocol to distribute connections via NAT or direct routing without looking inside packet payloads. Layer 7 load balancing operates at the application layer, terminates the client connection, parses protocols like HTTP/HTTPS, and chooses a backend based on request content such as URL path, headers, cookies, or method. L4 is faster and protocol-agnostic; L7 enables content-based routing, rewriting, caching, and other application-aware features. TLS termination itself is available at both layers: an L4 proxy can terminate TLS and pass decrypted bytes over a new TCP connection without parsing the application protocol, while an L7 proxy typically decrypts to inspect and route.

## Why interviewers ask this

System design questions such as designing a weather ingestion API or a photo-heavy app like Instagram force candidates to decide how incoming traffic reaches backend services. The interviewer wants to see whether you know that content-based routing, header inspection, and path-based routing require Layer 7, while simple TCP/UDP distribution can be done faster at Layer 4. They also probe whether you overclaim L7 features like TLS termination, which belongs to both layers depending on configuration.

## The core idea

The OSI layer determines what information a load balancer can use to make a routing decision. L4 sees only the network and transport headers—client IP, server IP, client port, server port, protocol—so it can distribute traffic cheaply and transparently, but cannot distinguish GET /api from GET /images. L7 terminates the client connection, parses the application protocol, and can route on URL path, Host header, cookies, or other content; this enables canary deployments, A/B tests, API version routing, and cache/rewrite policies, at higher per-request CPU cost and latency. Both can handle TLS termination, but only L7 can use the decrypted HTTP content for decisions. Choose L4 when you need raw speed, protocol transparency, or non-HTTP protocols; choose L7 when routing must be content-aware.

## Key points

- Layer 4 load balancers route at the transport layer using source/destination IP, ports, and protocol, without inspecting payloads.
- Layer 7 load balancers terminate client connections, parse HTTP protocols, and route based on URL path, headers, cookies, or method.
- TLS termination is not exclusive to L7: an L4 TCP proxy can terminate TLS (e.g., AWS NLB with a TLS listener), but only L7 can use decrypted HTTP for routing decisions.
- L4 has lower per-connection CPU cost and latency than L7, but cannot do content-based routing, request rewriting, or header-aware session persistence.
- AWS Application Load Balancer is L7; AWS Network Load Balancer is L4.

## Your 60-second answer

A Layer 4 load balancer routes traffic using only transport information—source and destination IP, ports, and protocol—so it can forward TCP or UDP packets very fast without looking inside. A Layer 7 load balancer terminates the client connection, parses the application protocol like HTTP, and picks a backend based on content: URL path, headers, cookies. That's why if you want /api to go to one service and /images to another, you need L7. The trade-off is overhead: L7 does more work per request, so it adds latency and CPU, while L4 is nearly transparent but cannot make content decisions. Also, TLS termination alone is not a clear differentiator—an L4 TCP proxy can terminate TLS too; it just won't inspect the HTTP payload.

## If they dig deeper

**What information does a Layer 4 load balancer actually use to route?**

It reads only the transport header: source IP, destination IP, source port, destination port, and protocol (TCP or UDP). It does not parse the payload, so two HTTP requests with different URL paths but same destination port are indistinguishable to it.

**When would you choose Layer 4 over Layer 7?**

Use L4 for non-HTTP protocols like database connections (PostgreSQL, MySQL), or when you need extremely low latency and don't need content routing. An L4 balance also preserves the original client connection semantics, which some protocols rely on.

**How does TLS termination fit into this comparison?**

TLS termination can be done at both layers. An L4 load balancer can accept a TLS connection, decrypt it, and open a new TCP connection to the backend without reading HTTP; an L7 load balancer decrypts and then parses HTTP to route based on headers or path. So TLS termination is not a differentiator, but content inspection after decryption is.

**What does path-based routing require and which layer provides it?**

Path-based routing requires reading the HTTP request line or headers, which means Layer 7. For example, routing /api/* to API servers and /static/* to CDN origins cannot be done by L4 because it never sees the path.

**How would you handle a mix of HTTP and raw TCP traffic to the same public endpoint?**

You can use a Layer 4 load balancer to distribute connections by port and protocol, then send HTTP traffic onward to a Layer 7 tier for content routing and send raw TCP to dedicated backend pools. Alternatively, some proxies can run in TCP mode for non-HTTP ports and HTTP mode for others, but then those TCP connections lose application-aware routing.

## Worked example

Suppose an endpoint receives HTTP requests for /api and /images, plus PostgreSQL replication on port 5432. An L4 load balancer sees only IP/port pairs: client 203.0.113.5:49152 to 198.51.100.10:80 and 198.51.100.10:5432. It routes all port 80 traffic to one pool, regardless of path. An L7 load balancer reads the request line GET /api/users HTTP/1.1 and GET /images/logo.png and routes them to separate upstream pools. For port 5432, the same appliance can run in L4 TCP mode to pass binary protocol bytes without parsing them. Reasoning: content-based routing becomes possible only when the balancer parses HTTP, which adds per-request CPU cost.

## Common traps

- Claiming L4 can route on HTTP headers 'because the header is in the packet'; L4 does not inspect payload, so it cannot see headers or paths.
- Saying TLS termination is a Layer 7-only feature; an L4 TCP proxy can terminate TLS without parsing the application protocol.
- Assuming L7 is always better because modern CPUs are fast; it adds per-request parsing overhead and may be unnecessary for simple TCP services.
- Forgetting that L7 requires a known application protocol; non-HTTP protocols usually need L4.

</details>

---

## 22. Regularization · output · Easy

*ai · gate confidence 0.95*

<sub>to object to this card: `## ai-regularization` then `match: Given the Python code below, what is printed? The code simul`</sub>

**Question**

Given the Python code below, what is printed? The code simulates one L2 update and five L1 updates with λ=0.1, learning rate=0.01, and no data gradient.

```python
w2 = 0.005
# One L2 update: multiply by (1 - lr * 2 * λ)
w2 *= (1 - 0.01 * 2 * 0.1)
print(round(w2, 5))

w = 0.005
# Five L1 updates: subtract lr * λ each step
for _ in range(5):
    w -= 0.01 * 0.1
print(w)
```

**Reference answer**

0.00499\n0.0

**Graded on**

- The L2 update multiplies the weight by 0.998, so 0.005 becomes 0.00499.
- Each L1 update subtracts 0.001, so after five steps 0.005 becomes 0.0.
- The first print rounds to five decimal places, showing 0.00499.
- The second print shows exactly zero.

<details><summary>The lesson this came from</summary>

Regularization is a set of modifications to the learning objective or training procedure that constrain model complexity and reduce generalization error at the expense of increased training error. L2 adds a squared L2 norm penalty on weights, so optimization shrinks all weights toward zero. L1 adds an absolute-value penalty; when paired with proximal or coordinate-descent optimization it can produce exactly zero weights, making the model sparse. Dropout injects noise by randomly disabling activations during training, and early stopping terminates training before the validation error degrades.

## Why interviewers ask this

Interviewers use regularization questions to test whether you understand overfitting as a capacity problem, not just a vocabulary list. They want to hear the optimization mechanics, the train/inference distinction for dropout, and the trade-off between bias and variance. Weak answers name techniques without explaining how they constrain the model or when they fail.

## The core idea

The goal of regularization is to keep a high-capacity model from fitting the training sample's noise. L2's quadratic penalty makes the gradient of the penalty proportional to the weight itself, so large weights shrink quickly and small weights shrink gently; this rarely produces exact zeros. L1's absolute penalty has a constant-magnitude subgradient sign(w), which gives it the ability to zero some weights under proximal/coordinate updates, but plain fixed-step gradient descent oscillates around zero because the update is discrete. Dropout approximates an ensemble by training different random subnetworks, and early stopping limits the effective number of iterations, keeping parameters closer to their initialization.

## Key points

- L2 adds a squared weight penalty whose gradient is proportional to the weight, shrinking large weights harder but rarely making weights exactly zero.
- L1 adds an absolute-value penalty; exact zeros appear with soft-thresholding/coordinate descent, whereas fixed-step vanilla SGD typically oscillates across zero rather than pinning weights there.
- Dropout randomly zeroes activations with probability p during training and scales the survivors by 1/(1-p), and is disabled at inference.
- Early stopping monitors validation performance and halts training before the model fully fits training-set noise, effectively limiting the parameter space explored.
- These methods increase bias and reduce variance; setting their strength too high causes underfitting.

## Your 60-second answer

Regularization is any change to the learning algorithm that reduces overfitting by constraining the model's effective capacity. L2 adds a squared penalty on weights, so each gradient step shrinks weights toward zero, but the penalty gradient also shrinks as weights get small, so they rarely become exactly zero. L1 adds an absolute-value penalty; with proximal soft-thresholding or coordinate descent it can drive some weights exactly to zero for a sparse model, while plain fixed-step stochastic gradient descent oscillates across zero rather than pinning there. Dropout randomly zeroes a fraction of activations during training and scales the rest by 1/(1-p), acting as an ensemble of thinned networks; it is disabled at inference. Early stopping halts training when validation error stops improving, preventing the model from fitting sample-specific noise. Too much regularization causes underfitting, so the bias-variance trade-off is the core tension.

## If they dig deeper

**Why doesn't L2 normally produce exact zero weights?**

Because the penalty gradient is λw, which shrinks in proportion to the current weight. As w approaches zero, the update becomes arbitrarily small, so the weight decays geometrically toward zero but, barring floating-point underflow, never reaches exactly zero.

**How does L1 create sparse weights, and why can vanilla SGD fail to keep them at zero?**

With proximal soft-thresholding or coordinate descent, a weight becomes exactly zero when its magnitude after the data-gradient step is below the threshold ηλ. The update sign(w)·max(|w|-ηλ, 0) explicitly sets it to zero. Fixed-step subgradient SGD instead applies a constant step -ηλ·sign(w), so a small weight crosses to the opposite sign and oscillates unless a thresholding operator is used.

**Why does dropout use the 1/(1-p) scaling?**

Without scaling, the expected total activation into the next layer would be multiplied by (1-p), so inference-time full network would see a systematically different scale. Inverted dropout scales surviving activations at training so the expectation matches the full network, allowing dropout to be turned off at inference.

**How does early stopping act as a regularizer?**

It stops optimization before the parameters can reach minima that fit idiosyncratic training examples. For linear least-squares optimized by gradient descent starting near zero, early stopping is approximately equivalent to L2 regularization, and more generally it limits the effective capacity of the model.

**What is Monte Carlo dropout and what does it estimate?**

Instead of turning dropout off at test time, you keep it enabled and run the same input through the network many times. The spread of the resulting predictions approximates model uncertainty; this interpretation follows a variational-inference view of dropout over the network weights.

## Worked example

Take a single scalar weight w with no data gradient, λ=0.1, and η=0.1. Under L2, the update is w ← (1 - ηλ)w = 0.99w, so w moves 0.400, 0.396, 0.392, ... toward zero but does not hit it. Under L1 with fixed-step SGD, starting at w=0.005 gives w ← 0.005 - 0.01·sign(0.005) = -0.005; the next iteration gives +0.005, so the weight oscillates rather than remaining at zero. With soft-thresholding, the same w is replaced by sign(0.005)·max(0.005 - 0.01, 0) = 0, making it exactly zero. This is why sparse L1 solvers rely on proximal or coordinate updates instead of naive SGD.

## Common traps

- Saying dropout randomly zeroes weights; it zeroes activations, leaving weights unchanged.
- Claiming plain L1 gradient descent keeps weights exactly at zero; fixed-step SGD oscillates unless a proximal/soft-threshold step is used.
- Tuning regularization strength against the test set; the test set must remain unused until final evaluation or the generalization estimate is contaminated.
- Forgetting to disable dropout at inference, which changes the activation scale and degrades the model.

</details>

---

## 23. Linked List · mcq · Medium

*dsa · gate confidence 0.95*

<sub>to object to this card: `## linked-list` then `match: To remove the nth node from the end of a singly linked list `</sub>

**Question**

To remove the nth node from the end of a singly linked list in one pass using a dummy node, how many steps should the first pointer advance from the dummy before moving both pointers together?

**Options**

- n
- n + 1
- n - 1
- 2n

**Reference answer**

n + 1

**Graded on**

- Start from dummy node
- First pointer advances n + 1 steps
- Second pointer ends before target
- Return dummy.next

<details><summary>The lesson this came from</summary>

A linked list is a linear collection of nodes, each storing a value and a reference to its successor; a singly linked list has only a next pointer, while a doubly linked list also has a prev pointer. Nodes are allocated individually and are not guaranteed to be contiguous, so finding the kth element requires following k links from the head. This pointer structure makes insertion and deletion by known predecessor or successor pointers constant-time rewiring operations, but it removes constant-time random access.

## Why interviewers ask this

Interviewers use linked list questions to test pointer manipulation, edge-case handling at the head and tail, and in-place algorithms that avoid extra memory. Companies such as Amazon, Bloomberg, Meta, and Microsoft frequently ask variants like merging sorted lists, cycle detection, and node removal because they reveal whether a candidate can trace pointer updates correctly. The fast/slow, dummy node, and reversal patterns also carry over to tree and graph traversal.

## The core idea

Nearly every singly linked list problem reduces to re-wiring next pointers correctly, so draw the node boxes and arrows before touching code. A dummy head node turns the first real node into an ordinary middle-of-list case, eliminating head-update branches. Fast and slow pointers detect cycles, find midpoints, and enable one-pass removals; they work because the gap changes predictably. Reverse a sublist by keeping the previous, current, and next nodes so you never lose the remaining list when you redirect a pointer. Deletion is O(1) only when you have the node before the target or a doubly linked list's prev pointer; with only the target node in a singly linked list, the copy-next trick works for a non-tail node but fails at the tail.

## Key points

- A singly linked list node stores a value and a next pointer; accessing the kth element requires following k pointers from the head, so access is O(k).
- Inserting after a known node is O(1); deleting a node in a singly linked list generally requires a pointer to its predecessor, though the copy-next trick deletes a non-tail node in O(1).
- A doubly linked list supports O(1) insertion and deletion at a known node, including the tail, because the node has both prev and next pointers.
- A dummy head node turns head insertion and deletion into regular cases, eliminating many special-case branches.
- Floyd's fast-slow pointers detect cycles in O(n) time and O(1) space: if a cycle exists, the pointers eventually meet because the fast pointer closes the gap by one node per step.

## Your 60-second answer

A linked list is a linear collection of nodes, each holding a value and a reference to the next node. The reason interviewers ask about it is that the problems test pointer rewiring and edge cases at the head, tail, and empty list. I usually start by putting a dummy node before the head so every deletion and insertion uses the same logic. For cycle detection or finding the middle, I use two pointers, one moving one step and the other two steps. For reordering, I reverse a sublist by maintaining previous, current, and next pointers. The main trade-off is that inserting and deleting after a known node are constant-time operations, but reading the k-th element takes O(k) time because there is no random access. In a singly linked list, deleting a given node in constant time generally requires its predecessor; copying the successor's value and removing the successor is an exception and fails for the tail.

## If they dig deeper

**What is the difference between a singly linked list and a doubly linked list?**

A singly linked list node has only a value and a next pointer, while a doubly linked list node also has a prev pointer. The extra prev pointer enables O(1) insertion and deletion at a known node, including the tail, and backward traversal, at the cost of extra memory and more pointer updates.

**How do you reverse a singly linked list in place?**

Maintain three pointers: previous, current, and next. At each step, save current.next, set current.next to previous, then advance previous to current and current to the saved next pointer. After the loop, previous is the new head; the time complexity is O(n) and space is O(1).

**How do you detect a cycle and find the node where the cycle begins?**

Use two pointers, slow moving one step and fast moving two steps. If they meet, a cycle exists. To find the start, reset one pointer to the head and move both pointers one step at a time; they will meet at the node where the cycle begins.

**You are given only a pointer to a non-tail node in a singly linked list; how do you delete it?**

Copy the value from the successor node into the target node, then update target.next to successor.next. This effectively removes the successor in O(1) time. It cannot be used on the tail because there is no successor to copy, and it may break external references to the successor.

**How would you merge k sorted linked lists in less than O(kN) time?**

Use a min-heap initialized with the head of each list. Repeatedly extract the smallest node, append it to the result, and push its next node into the heap. This runs in O(N log k) time and O(k) auxiliary space, where N is the total number of nodes. Alternatively, pair-wise merging of lists also achieves O(N log k) time.

## Worked example

To reverse 1 -> 2 -> 3 -> null, start with prev = null and curr = 1. Save next = curr.next (2), set curr.next = prev (null), then advance prev = 1 and curr = 2. At the next iteration, save next = 3, set curr.next = prev (1), then prev = 2 and curr = 3. In the final iteration, save next = null, set 3.next = 2, then prev = 3 and curr = null. Return prev, which is the new head: 3 -> 2 -> 1 -> null.

## Common traps

- Using the copy-successor deletion trick on the tail node, which dereferences null and cannot remove the tail.
- Trying to delete a node from a singly linked list with only a pointer to that node and no predecessor, without using the successor trick; this is not O(1) in general.
- Forgetting to update the head when the first node is removed or reversed, returning the old head.
- Advancing the fast pointer without checking both fast and fast.next, causing a null pointer exception on even-length lists.

</details>

---

## 24. Lambda expressions · mcq · Hard

*java · gate confidence 0.95*

<sub>to object to this card: `## java-lambda-expressions` then `match: A lambda is passed to an overloaded method where two overloa`</sub>

**Question**

A lambda is passed to an overloaded method where two overloads accept different functional interfaces, and the lambda body is compatible with both. What is the result?

**Options**

- The first overload is chosen
- The most specific overload is chosen
- The call fails to compile as ambiguous
- The call compiles and infers a shared return type

**Reference answer**

The call fails to compile as ambiguous

**Graded on**

- Overload resolution cannot distinguish between the target types
- Explicit cast or typed variable resolves the ambiguity

<details><summary>The lesson this came from</summary>

A lambda expression is a syntactic construct that creates an instance of a functional interface by supplying the body of its single abstract method inline. The arrow operator separates an optional parameter list from a body, which can be a single expression or a block. Lambda expressions were introduced in Java 8 as a concise alternative to anonymous classes that implement exactly one method.

## Why interviewers ask this

Interviewers ask about lambdas to check whether you understand Java 8's shift toward passing behavior as data and how lambdas relate to functional interfaces. They probe target typing, capture rules, and the common java.util.function interfaces because those feed directly into streams and collection pipelines.

## The core idea

In Java, a lambda expression is the body of the one abstract method in a target functional interface. The compiler uses the expected type from the assignment, cast, or method argument to infer parameter types and check return compatibility. A lambda can capture local variables only if they are effectively final—never reassigned anywhere in their scope—but it can always read and modify instance fields and static fields. At runtime, the JVM uses invokedynamic and the LambdaMetafactory to create the call site rather than generating a separate anonymous class file at compile time. A lambda body may be a single expression whose value is returned automatically, or a block with explicit returns and statements.

## Key points

- A lambda expression always implements a functional interface, which has exactly one abstract method; default and static methods do not count toward that one.
- Target typing determines the lambda's type from the surrounding context—assignment, cast, or method argument—not from the lambda's own body.
- Parameter types may be omitted, a single untyped parameter may drop parentheses, and the body can be an expression returning a value or a block with statements and explicit returns.
- Captured local variables must be effectively final, meaning they are never reassigned anywhere in their scope, while instance fields and static variables may be read and modified freely.
- Common functional interfaces include Predicate<T> with boolean test(T), Function<T,R> with R apply(T), Consumer<T> with void accept(T), and Supplier<T> with T get().

## Your 60-second answer

A lambda expression is Java's concise syntax for implementing a functional interface inline. You write the parameter list, an arrow, and a body, and the compiler treats that as providing the single abstract method of whatever functional interface is expected at that spot. For example, `Runnable r = () -> System.out.println(42);` creates a Runnable without the boilerplate of an anonymous class. Lambdas matter because they let you pass behavior as data to methods like `forEach`, `filter`, and `map`, especially with the Streams API added in Java 8. One trade-off is that they can only target interfaces with exactly one abstract method, so if you need to implement two methods you still write an anonymous class. Another trade-off is captured local variables must be effectively final, which sometimes forces a workaround like using a single-element array or a field.

## If they dig deeper

**What is a functional interface, and how does @FunctionalInterface work?**

A functional interface is an interface with exactly one abstract method. Default and static methods do not count toward that one. The @FunctionalInterface annotation is optional but when present it makes the compiler fail if the interface has zero or more than one abstract method.

**Can you assign a lambda to Object or use var with it? Why not?**

No. A lambda expression needs a target type that is a functional interface because it supplies the body of that interface's single abstract method. Object has no abstract method, so the compiler cannot infer a functional interface; you need a cast like `(Runnable) () -> ...` or an explicit functional interface target such as a variable declaration.

**What are the rules for capturing variables in a lambda expression?**

Local variables and parameters from the enclosing method can be read only if they are effectively final—never reassigned anywhere in their scope. Instance fields and static fields can always be read and modified. A lambda cannot access default methods of the functional interface it implements because there is no interface instance `this` available inside the lambda.

**How does the JVM implement lambdas differently from anonymous inner classes?**

At compile time, the compiler emits an invokedynamic call site with a method handle to a synthetic private method containing the lambda body. At runtime, the LambdaMetafactory uses that method handle to generate or return a class implementing the functional interface; no separate class file is created for each lambda, unlike anonymous inner classes which generate a distinct class at compile time.

**What are the scoping differences between a lambda and an anonymous inner class?**

A lambda is lexically scoped: `this` and `super` refer to the enclosing instance, not the lambda object, and a lambda parameter cannot shadow a local variable from the enclosing method. An anonymous inner class has its own `this`, and its parameters and locals can shadow enclosing variables because it introduces a new nested scope.

## Worked example

Take `List<String> words = Arrays.asList("apple", "pear", "kiwi");` and the call `Collections.sort(words, (a, b) -> a.length() - b.length());`. The second argument's expected type is `Comparator<String>`, whose `compare` method takes two `String` parameters and returns `int`, so the compiler infers `a` and `b` as `String` and accepts the expression body as the returned difference. If you tried to assign that same lambda to a `Function<String, Integer>`—a one-parameter interface—the parameter count mismatches and compilation fails even though an int is returned. For capturing, `int limit = 5; List<Integer> xs = Arrays.asList(1, 2, 3); xs.replaceAll(x -> x * limit);` compiles because `limit` is never reassigned; adding `limit = 6` anywhere in the method makes `limit` not effectively final and the lambda will not compile. These two examples show target typing and effective final capture.

## Common traps

- Assigning a lambda to Object or using var without a functional interface target: compilation fails because a lambda has no independent type.
- Thinking a captured local variable can be reassigned as long as the reassignment happens before the lambda: any reassignment in scope breaks effective finality, even before the lambda is created.
- Conflating lambda with anonymous inner class for `this`: inside a lambda `this` is the enclosing object, not the lambda instance.
- Using a zero-argument lambda as a Consumer: Consumer's accept method takes one argument, so `() -> list.add(x)` targets a zero-argument void interface such as Runnable, not Consumer.

</details>

---

## 25. Subnetting and CIDR · mcq · Medium

*cs · gate confidence 1.0*

<sub>to object to this card: `## cs-subnetting-and-cidr` then `match: Can 192.168.8.0/24 and 192.168.9.0/24 be advertised as one a`</sub>

**Question**

Can 192.168.8.0/24 and 192.168.9.0/24 be advertised as one aggregate prefix? If so, which?

**Options**

- Yes, 192.168.8.0/23
- Yes, 192.168.8.0/22
- No, they are not contiguous
- No, the lower /24 is not aligned

**Reference answer**

Yes, 192.168.8.0/23

**Graded on**

- the two /24s are contiguous
- their first 23 bits are identical
- the aggregate is /23
- the lower third octet is even and aligned

<details><summary>The lesson this came from</summary>

An IPv4 address is a 32-bit number usually written in dotted decimal. A subnet mask or CIDR prefix length marks the first n bits as the network portion and the remaining 32 − n bits as hosts. CIDR notation writes this as address/prefix, such as 192.168.1.0/24, replacing the fixed class A/B/C boundaries with variable-length prefixes for subnetting and route aggregation.

## Why interviewers ask this

Interviewers use subnetting questions to test whether you can do fast binary-to-decimal conversions and boundary arithmetic under pressure. They also check that you understand how networks are partitioned in real systems: cloud VPCs, container CIDR ranges, firewall rules, and routing tables all require correct network, broadcast, and usable host calculations.

## The core idea

The mask is applied with a bitwise AND to clear host bits, leaving the network address. The inverse mask sets the host bits to all ones to give the broadcast address. The number of usable hosts for a normal IPv4 /n is 2^(32−n) − 2 because the all-zero and all-one host addresses are reserved. CIDR removes the old classful octet boundaries; a prefix can split an octet, which is why block size in the relevant octet is 256 minus the mask value. Route aggregation works by combining adjacent CIDR blocks whose binary prefixes share a common shorter prefix.

## Key points

- An IPv4 address is 32 bits; a /n prefix means n network bits and 32 − n host bits.
- Network address = IP AND mask; broadcast address = IP OR (NOT mask).
- Usable IPv4 hosts in a normal /n network are 2^(32−n) − 2, because all-zero and all-one host bits are reserved.
- Private IPv4 ranges are 10.0.0.0/8, 172.16.0.0/12, and 192.168.0.0/16; these are not publicly routable.
- CIDR enables route aggregation and VLSM by allowing arbitrary prefix lengths instead of only /8, /16, or /24.

## Your 60-second answer

An IP address is just a 32-bit number, and the prefix length tells you how many leading bits identify the subnet. A /24 means the first 24 bits are network bits, leaving 8 bits for hosts. To find the network address, apply a bitwise AND between the IP and the subnet mask; the broadcast address sets all host bits to one. The usable range is everything between them, so a /24 has 2^8 minus 2, or 254 usable addresses. CIDR generalizes this by allowing any prefix length, not just the old classful /8, /16, and /24 boundaries. That lets you allocate a /26 for 62 hosts or summarize four /26 routes into one /24 route. The trade-off is that smaller subnets waste fewer addresses but increase the number of routes and therefore routing table size.

## If they dig deeper

**What is the subnet mask for /26, and how many usable host addresses does it allow?**

/26 has 26 network bits and 6 host bits. The mask is 255.255.255.192, and it provides 2^6 − 2 = 62 usable IPv4 host addresses because the network and broadcast addresses consume two addresses.

**Given 10.10.34.129/20, what are the network address, broadcast address, and usable host range?**

With /20, the mask is 255.255.240.0, so the block size in the third octet is 16. 34 falls in the 32 block, giving network 10.10.32.0, broadcast 10.10.47.255, and usable range 10.10.32.1 to 10.10.47.254.

**Can you combine 192.168.8.0/24 and 192.168.9.0/24 into a single route? If so, what is the route?**

Yes. The third octets are 8 (00001000) and 9 (00001001), which share the first seven bits and differ only in the last bit, so the common prefix is 23 bits. The aggregate is 192.168.8.0/23, covering 192.168.8.0 through 192.168.9.255.

**How would you allocate 192.168.1.0/24 to support subnets of 100, 50, and 25 hosts using VLSM?**

Allocate a /25 for 100 hosts, which gives 126 usable addresses from 192.168.1.0 to 192.168.1.127. Then allocate a /26 for 50 hosts, giving 62 usable addresses from 192.168.1.128 to 192.168.1.191. Finally allocate a /27 for 25 hosts, giving 30 usable addresses from 192.168.1.192 to 192.168.1.223. Remaining space stays unallocated.

**When a router has multiple matching CIDR routes, how does it choose which one to use?**

It uses longest prefix match: the route with the largest prefix length that matches the destination address is selected. This allows a more specific route, such as a /26, to override a less specific aggregate route like a /24 without removing the aggregate.

## Worked example

Take 10.10.34.129/20. The /20 mask is 255.255.240.0 because the first 20 bits are ones: 16 ones in the first two octets plus four ones in the third octet, 11110000 = 240. The block size in the third octet is 256 − 240 = 16, so the subnets in that octet are 0, 16, 32, 48, and so on. The address's third octet is 34, which falls in the 32 block, so the network address is 10.10.32.0. There are 12 host bits, so the broadcast address is 10.10.47.255, and the usable host range is 10.10.32.1 through 10.10.47.254.

## Common traps

- Forgetting to subtract the network and broadcast addresses when stating usable host count.
- Using classful boundaries and assuming every subnet must be /8, /16, or /24 instead of any CIDR prefix.
- Computing the block size in the wrong octet when the prefix splits an octet.
- Trying to summarize non-adjacent or misaligned CIDR blocks, producing an aggregate that covers addresses outside both original ranges.

</details>

---

## Cards the gate rejected

Judge whether it was right. Each was thrown away.

- **java-equals-and-hashcode-contract** (typed): What rules must an equals implementation itself obey?
  - Gate said: wrong_format: The question asks to enumerate the five specific equivalence relation properties without specifying how many or which rules are expected.

- **lld-decorator-pattern** (mcq): Assume `Compressor` and `Encryptor` are `OutputStream` decorators. `Compressor.write(data)` compresses the data and then delegates the compressed bytes to the wrapped stream. `Encryptor.write(data)` encrypts the data and then delegates the encrypted bytes to the wrapped stream. Which construction writes data to the destination `stream` in the order: compressed first, then encrypted?
  - Gate said: a competent answer disagrees with the marked option

- **lld-restaurant-management-system-design** (flash): In an object-oriented restaurant management system, a Branch object is composed of which two main domain components?
  - Gate said: not answerable: The question assumes a specific textbook or proprietary schema design where a Branch has 'two main domain components'.

- **sql-row-number-rank-dense-rank** (typed): Explain what RANK() and DENSE_RANK() return when the OVER() clause has no ORDER BY in PostgreSQL/MySQL/SQLite, contrast this with SQL Server, and state whether such a ranking is meaningful.
  - Gate said: wrong_format: The question asks for a multi-part cross-database comparison requiring several paragraphs.

- **two-pointers** (output): What is the exact output of the following Python code?

arr = [2, 7, 11, 15]
target = 9
left, right = 0, len(arr) - 1
while left < right:
    current = arr[left] + arr[right]
    if current == target:
        print(left + 1, right + 1)
        break
    elif current < target:
        left += 1
    else:
        right -= 1
  - Gate said: malformed: an output card must show the snippet it is asking about

## Cards the gate caught and the rewrite fixed

These are the questions as first written. The gate objected, a rewrite pass replaced each one, and the replacement passed - so these are not in the app. They are here because the gate is on trial too: if its objections below look wrong, it is throwing away good work, and if they look right, it is earning its cost.

- **ai-data-structures-and-algorithms** (flash): What is the expected time complexity of hash map get and put operations, and what assumptions are needed for that bound?
  - Gate said: wrong_format: Explaining both the expected complexity and the underlying assumptions takes more than one crisp sentence.

- **ai-data-structures-and-algorithms** (flash): Why does a binary heap retrieve the minimum or maximum in O(1), while inserting or extracting that element takes O(log n)?
  - Gate said: wrong_format: Answering both parts fully requires more than a single crisp sentence.

- **ai-embedding-models** (flash): Which similarity measures are typically used to compare embedding vectors?
  - Gate said: wrong_format: Asking for multiple similarity measures typically requires a list rather than a single crisp sentence.

- **ai-metrics-offline-and-online** (flash): Which offline metrics are more informative than accuracy for imbalanced classification?
  - Gate said: wrong_format: Asking to list multiple metrics is unconstrained and fits poorly into a one-sentence flash card.

- **ai-model-selection-and-validation** (flash): What is the core rule about using data to make model or hyperparameter decisions?
  - Gate said: not answerable: The phrasing 'the core rule' is overly vague and open to multiple distinct formulations.

- **ai-prediction-service** (mcq): Which technique does NOT reduce inference compute for an existing model?
  - Gate said: not answerable: All listed techniques (quantization, pruning, operator fusion, knowledge distillation) can reduce inference compute for a model.

- **ai-probability-and-statistics** (flash): State the three axioms that any probability measure must satisfy.
  - Gate said: wrong_format: Stating three distinct mathematical axioms cannot fit into a single crisp sentence.

- **ai-python** (mcq): Python's list and tuple are ordered sequences, while dict and set are hash-based containers. Which pair of properties primarily explains why a tuple can be a dictionary key but a list cannot, and why dict/set membership is average O(1) while list membership is O(n)?
  - Gate said: a competent answer disagrees with the marked option

- **ai-recommendation-systems** (typed): How would you design a video recommendation system?
  - Gate said: wrong_format: An end-to-end system design question cannot be answered in 1-3 sentences.

- **ai-recommendation-systems** (flash): Name the three classic recommendation approaches.
  - Gate said: wrong_format: Asking to list multiple items does not fit the one-sentence flashcard format.

- **ai-sql** (flash): What are the core DML statements in SQL for retrieving and modifying data?
  - Gate said: wrong_format: Asking for an enumeration of multiple core DML statements does not fit a single-sentence flash card format.

- **ai-training-and-optimization** (flash): Name two alternative update rules beyond vanilla gradient descent that alter how the raw gradient is applied.
  - Gate said: not answerable: The question asks to name any two alternatives out of many possibilities, making grading unpredictable.

- **arrays-hashing** (flash): What is the main transformation that replaces an O(n^2) nested array scan with an O(n) solution?
  - Gate said: not answerable: The question is too vague and open-ended to have a single clear answer (could be hash table lookup, sorting, two pointers, prefix sums).

- **beh-company-and-motivation** (mcq): In a behavioral interview, which impact signal is most appropriate for a senior engineer describing a proudest project?
  - Gate said: a competent answer disagrees with the marked option

- **beh-dealing-with-ambiguity** (mcq): At the senior level, an ambiguous project story should typically involve leading work across what scope of people?
  - Gate said: a human reviewer objected: At the senior level, an ambiguous project story should typically involve leading

- **beh-dealing-with-ambiguity** (typed): What is the core idea behind reducing ambiguity on a task?
  - Gate said: a human reviewer objected: What is the core idea behind reducing ambiguity on a task?

- **beh-delivering-results** (typed): In the middle of a delivery, a load test fails or a deadline slips. What is the strongest response, and how do you decide among cutting scope, adding resources, or moving the date?
  - Gate said: wrong_format: The compound question requires multiple detailed considerations that cannot be adequately answered in one to three sentences.

- **beh-failure-and-learning** (typed): What pattern can signal that you are about to repeat a past mistake?
  - Gate said: not answerable: The question is too vague and likely refers to a specific framework or heuristic from the source material that cannot be deduced.

- **beh-failure-and-learning** (flash): What four elements make a complete failure answer?
  - Gate said: not answerable: Asking to list four specific elements refers to a specific unseen framework and does not fit a one-sentence flash format.

- **beh-growth-mindset** (flash): When answering a behavioral interview question about growth mindset, what four elements should the story include to demonstrate that the change stuck?
  - Gate said: not answerable: Asking for an exact list of four specific elements from an unseen framework cannot be answered or graded reliably in a one-sentence flash format.

- **beh-handling-feedback** (flash): When receiving feedback as a software engineer, what sequence of steps helps you handle it effectively?
  - Gate said: wrong_format: Describing a sequence of steps requires multiple sentences or a multi-part explanation that exceeds a single crisp flash sentence.

- **beh-leadership** (flash): What common senior failure makes a candidate sound like an executor instead of a leader?
  - Gate said: not answerable: The question points to a specific unspecified failure mode from a curriculum rather than a universally unique answer.

- **beh-leadership** (flash): What is the real measure of thought leadership in an interview answer?
  - Gate said: not answerable: The question is too vague and subjective with no single standard definition of the 'real measure' of thought leadership.

- **beh-leadership** (mcq): A senior candidate is preparing a behavioral story about leadership. Which set of dimensions should the story cover to avoid sounding like a single-dimensional executor?
  - Gate said: not answerable: Multiple option lists are arbitrary frameworks that could defensibly be considered valid dimensions of leadership without an external syllabus.

- **beh-leadership** (mcq): Which set of behaviors best describes effective leadership during a high-pressure crisis or significant disruption?
  - Gate said: a human reviewer objected: Which set of behaviors best describes effective leadership during a high-pressur

- **beh-leadership** (flash): In behavioral interviews, what does leadership mean independent of formal authority?
  - Gate said: a human reviewer objected: In behavioral interviews, what does leadership mean independent of formal author

- **beh-ownership** (mcq): In behavioral interviews, ownership stories often scale with seniority: junior changes affect the candidate's own focus area, senior changes require coordinating several people (often three or more) on a team, and staff changes require multiple teams across the organization. According to this framework, which story best demonstrates senior-level ownership?
  - Gate said: refers to unseen material: 'According to this'

- **beh-story-craft** (mcq): Which opening best separates team context from your personal contribution in a behavioral story?
  - Gate said: a competent answer disagrees with the marked option

- **beh-story-craft** (typed): What is defensive framing in story craft, and why is it useful?
  - Gate said: not answerable: 'Defensive framing' is specialized jargon specific to an unseen source text rather than standard interview prep terminology.

- **cs-file-systems** (flash): What is a hard link, and why can it not cross filesystems?
  - Gate said: wrong_format: Answering both what a hard link is and why it cannot cross filesystems requires more than one crisp sentence.

- **cs-locking-mechanisms** (mcq): Which storage engine uses table-level locking by default?
  - Gate said: a human reviewer objected: Which storage engine uses table-level locking by default?

- **cs-locking-mechanisms** (typed): What are intent locks and why are they needed?
  - Gate said: a human reviewer objected: What are intent locks and why are they needed?

- **cs-osi-model** (flash): Name the seven OSI layers from bottom to top.
  - Gate said: wrong_format: Enumerating a seven-item ordered list does not fit a single-sentence flash card format.

- **cs-tlb-and-caching** (typed): Why do memory access times vary, and how do caches and TLBs exploit that variation?
  - Gate said: not answerable: The premise is backwards or confusing: caches and TLBs cause memory access variation to exploit locality, rather than exploiting pre-existing variation in access times.

- **cs-transaction-isolation-levels** (flash): List the four SQL standard transaction isolation levels from weakest to strongest.
  - Gate said: wrong_format: Asking to list multiple items does not fit the one-sentence flash format.

- **java-checked-vs-unchecked-exceptions** (output): Consider this Java method:

```java
String firstLine() {
    FileReader reader = new FileReader("data.txt");
    return new BufferedReader(reader).readLine();
}
```

What does javac report when compiling it?
  - Gate said: wrong_format: The exact compiler error message has multiple variations/lines and cannot be graded via exact string match.

- **java-collections-framework** (flash): In the Java Collections Framework, which interfaces extend Collection, and where does Map fit?
  - Gate said: wrong_format: Answering all interfaces extending Collection plus Map's position cannot be crisply answered in a single sentence.

- **java-collections-framework** (flash): What iteration order guarantees do HashSet, LinkedHashSet, and TreeSet provide?
  - Gate said: wrong_format: Explaining the order guarantees for three distinct set implementations exceeds a single crisp sentence.

- **java-collections-framework** (flash): How does PriorityQueue order its elements, and what are its add and poll costs?
  - Gate said: wrong_format: Asking for ordering mechanism plus multiple asymptotic complexities exceeds a single crisp flashcard sentence.

- **java-equals-and-hashcode-contract** (mcq): Which statement about equal objects and hash collisions is correct?
  - Gate said: a human reviewer objected: Which statement about equal objects and hash collisions is correct?

- **java-generics** (flash): After erasure, what methods exist in a class that implements `Comparable<String>`?
  - Gate said: not answerable: The class may declare arbitrary other methods, and describing bridge methods exceeds a single crisp sentence.

- **java-hashmap-internals** (mcq): During a get, what identifies the intended key inside a bucket?
  - Gate said: a human reviewer objected: During a get, what identifies the intended key inside a bucket?

- **java-hashset-vs-treeset** (output): What is printed when the following Java code runs?
TreeSet<Integer> ts = new TreeSet<>();
ts.add(3);
ts.add(1);
ts.add(2);
System.out.println(ts);
  - Gate said: malformed: an output card must show the snippet it is asking about

- **java-heap-vs-stack** (mcq): Which JVM flag mainly controls the size of a thread's stack?
  - Gate said: wrong_format: The options list descriptions rather than actual JVM flags, making the question poorly formed.

- **java-heap-vs-stack** (flash): What exactly is stored in a Java stack frame?
  - Gate said: wrong_format: Asking what 'exactly' is stored requires enumerating multiple components (local variable array, operand stack, frame data/constant pool reference) which exceeds a single crisp sentence and is hard to grade strictly.

- **java-streams-api** (output): What is the output of the following code?

```java
Stream.of(1, 2, 3, 4, 5)
    .filter(n -> n % 2 == 0)
    .map(n -> n * n)
    .collect(Collectors.toList())
```
  - Gate said: not answerable: The snippet evaluates an expression rather than printing anything, so there is no standard output.

- **java-strings** (output): What is the exact output of this Java code?

String s = "hello";
s.toUpperCase();
System.out.println(s);
  - Gate said: malformed: an output card must show the snippet it is asking about

- **lld-atm-system-design** (flash): What is the main trade-off of debit-first versus authorize-then-settle in ATM withdrawal?
  - Gate said: wrong_format: Explaining the trade-off between two transaction flow paradigms requires more than a single crisp sentence.

- **lld-elevator-system-design** (mcq): In a low-level design for an elevator car, which state set explicitly separates the car's direction of travel from whether the door is open, using mutually exclusive states?
  - Gate said: not answerable: The question asks which state set separates direction from door state, but all options combine or conflate them in non-standard ways.

- **lld-elevator-system-design** (mcq): Which set of states correctly models an elevator car as a finite state machine in an object-oriented elevator control system?
  - Gate said: not answerable: There is no single universally correct state modeling; multiple state decompositions (such as combining moving with direction or separating them) are defensible.

- **lld-interfaces** (flash): What is a traditional interface not allowed to define in Java or C#?
  - Gate said: not answerable: Too open-ended and ambiguous with multiple valid answers (instance state/fields, method implementations, constructors, etc.).

- **lld-parking-lot-design** (flash): What are the typical parking spot types modeled in a parking garage?
  - Gate said: wrong_format: Enumerating a list of spot types does not fit a single-sentence flash card.

- **lld-ride-sharing-service-design** (flash): Why should driver availability be a separate state rather than being derived only from trip status?
  - Gate said: a human reviewer objected: Why should driver availability be a separate state rather than being derived onl

- **lld-ride-sharing-service-design** (typed): What happens in the dispatch flow when a driver does not accept an offer before the timeout expires?
  - Gate said: a human reviewer objected: What happens in the dispatch flow when a driver does not accept an offer before 

- **lld-uml-sequence-diagram** (flash): What is a UML sequence diagram, and what do the vertical and horizontal axes represent?
  - Gate said: wrong_format: Asking for definition plus both axes typically requires multiple sentences or clauses beyond a single crisp sentence.

- **prefix-sum** (typed): Using a prefix-sum map initialized with {0: -1}, find the length of the longest zero-sum subarray in [2, -1, -1, 3, -3].
  - Gate said: wrong_format: The question asks for a single numeric result or calculation rather than free prose explanation.

- **sd-caching** (mcq): In the worked example, a product page is fetched 5,000 times per second and the database sustains 800 reads per second. After the Redis cache is warm with a 30-second TTL, how many database reads per second does that single product key cause?
  - Gate said: not answerable: References an unseen 'worked example'.

- **sd-consistent-hashing** (typed): Why are virtual nodes added to a consistent hash ring?
  - Gate said: a human reviewer objected: Why are virtual nodes added to a consistent hash ring?

- **sd-consistent-hashing** (typed): How is replication placed on a consistent hash ring?
  - Gate said: a human reviewer objected: How is replication placed on a consistent hash ring?

- **sd-design-a-chat-system** (typed): In a real-time chat system, what are the two primary subsystems of the architecture, and why are they separated?
  - Gate said: not answerable: Asking for 'the two primary subsystems' without context expects specific terminology from an unseen text.

- **sd-design-a-notification-system** (typed): How do you handle machine failures in a notification worker system?
  - Gate said: a human reviewer objected: How do you handle machine failures in a notification worker system?

- **sd-design-a-notification-system** (typed): When would you use a persistent WebSocket connection for in-app notifications instead of APNS/FCM push?
  - Gate said: a human reviewer objected: When would you use a persistent WebSocket connection for in-app notifications in

- **sd-design-case-studies** (flash): What mechanism is appropriate for counting current active page viewers?
  - Gate said: not answerable: There are many valid mechanisms (Redis HyperLogLog, sliding window bucket counters, sorted sets) with no single correct answer.

- **sd-design-case-studies** (mcq): How should you shard an idempotency store so that uniqueness checks on idempotency keys are local?
  - Gate said: a competent answer disagrees with the marked option

- **sd-design-case-studies** (typed): How do you mark a payment as completed and prevent a duplicate webhook from double-applying the update?
  - Gate said: a human reviewer objected: How do you mark a payment as completed and prevent a duplicate webhook from doub

- **sd-design-case-studies** (typed): Two concurrent requests with the same Idempotency-Key and merchant_id arrive at the payment API. What ensures only one provider call is made?
  - Gate said: a human reviewer objected: Two concurrent requests with the same Idempotency-Key and merchant_id arrive at 

- **sd-indexes** (flash): What is the default index structure in most relational engines, and why is it broadly useful?
  - Gate said: wrong_format: Answering both the structure and why it is broadly useful typically requires more than one crisp sentence.

- **sd-jwt** (mcq): Where should a JWT be stored to prevent JavaScript on the page from reading it?
  - Gate said: a human reviewer objected: Where should a JWT be stored to prevent JavaScript on the page from reading it?

- **sd-jwt** (typed): When a server verifies a JWT, what should it check?
  - Gate said: a human reviewer objected: When a server verifies a JWT, what should it check?

- **sd-microservices** (typed): How should a ranking and personalization component be integrated into a microservices system?
  - Gate said: not answerable: The question is too vague and lacks system context, allowing for dozens of mutually distinct correct integration patterns.

- **sd-nosql-types** (flash): What are the four main NoSQL database models?
  - Gate said: wrong_format: Flash cards expect one crisp sentence rather than enumerating a list of four items.

- **sd-object-storage** (flash): Name the three major managed object storage services.
  - Gate said: wrong_format: Flash cards require a single crisp sentence, not a list of named entities which is open to varying company selections.

- **sd-object-storage** (mcq): In Amazon S3 multipart upload, what is the minimum part size for every part except the last one?
  - Gate said: wrong_format: AWS documentation defines the minimum part size as 5 MB, making both '5 MiB' and '5 MB' ambiguously close or technically disputable.

- **sd-rate-limiting** (flash): What HTTP status and response headers should a rate limiter use when a caller exceeds its limit?
  - Gate said: wrong_format: Asking for the HTTP status and multiple response headers requires listing items rather than a single crisp sentence.

- **sd-rest-api** (flash): Which HTTP methods are idempotent in REST, and which one is not?
  - Gate said: wrong_format: Enumerating multiple idempotent and non-idempotent HTTP methods exceeds a single crisp sentence.

- **sd-rest-api** (flash): Name three HTTP headers commonly used for caching in REST APIs.
  - Gate said: wrong_format: Asking for a list of items to enumerate does not fit the single-sentence flashcard format.

- **sd-service-discovery** (flash): Name common service registry implementations used for service discovery.
  - Gate said: not answerable: Asking to list multiple implementations is an open-ended enumeration poorly suited for a single-sentence flash card.

- **sd-sql-vs-nosql** (flash): What are the four common NoSQL database models?
  - Gate said: wrong_format: The answer requires enumerating four distinct items rather than a single crisp sentence.

- **sd-unique-id-generation** (flash): What is the classic Twitter Snowflake 64-bit ID layout?
  - Gate said: wrong_format: Listing the exact bit allocation across four fields requires a structured or multi-part answer that does not fit a single crisp flash sentence.

- **sd-unique-id-generation** (output): What is printed by this code?
```python
BASE62 = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
def base62_encode(n):
    if n == 0:
        return BASE62[0]
    chars = []
    while n > 0:
        n, r = divmod(n, 62)
        chars.append(BASE62[r])
    return ''.join(reversed(chars))
print(base62_encode(1000000))
```
  - Gate said: not answerable: Calculating 1000000 into base 62 by hand is unreasonable mental arithmetic for an interview flashcard.

- **sliding-window** (typed): Walk through Longest Substring Without Repeating Characters on the input abcabcbb.
  - Gate said: wrong_format: Tracing step-by-step through an 8-character string requires a lengthy trace that exceeds the 1-3 sentence typed format.

- **sql-aggregate-functions** (typed): Given a sales table with rows ('North', 100), ('North', NULL), ('South', 50), ('South', 150), what rows and column values are returned by this query?
```sql
SELECT region, COUNT(*), COUNT(amount), SUM(amount), AVG(amount)
FROM sales
GROUP BY region
ORDER BY region;
```
  - Gate said: wrong_format: Asking for exact multi-column tabular result sets does not fit prose typed grading.

- **sql-aggregate-functions** (typed): What are two important consequences of using SQL aggregate functions for reporting?
  - Gate said: not answerable: The question is completely unconstrained and asks for an arbitrary list of two consequences.

- **sql-aggregate-functions** (mcq): In PostgreSQL with ONLY_FULL_GROUP_BY enabled, a table employees has id INTEGER PRIMARY KEY, dept_id INTEGER, name TEXT. Which query is valid?
  - Gate said: a human reviewer objected: In PostgreSQL with ONLY_FULL_GROUP_BY enabled, a table employees has id INTEGER 

- **sql-case-expression** (output): Given the table and query below, what is the exact output?
```sql
CREATE TABLE orders(order_id INT, status TEXT, amount INT);
INSERT INTO orders VALUES (1, 'paid', 50), (2, 'refunded', 20), (3, 'paid', 30);

SELECT
  SUM(CASE WHEN status = 'paid' THEN 1 ELSE 0 END) AS paid_count,
  SUM(CASE WHEN status = 'refunded' THEN amount ELSE 0 END) AS refunded_total
FROM orders;
```
  - Gate said: not gradable: SQL tabular output has no single obvious string representation or delimiter format.

- **sql-char-vs-varchar** (flash): What does VARCHAR(n) store compared with CHAR(n)?
  - Gate said: a human reviewer objected: What does VARCHAR(n) store compared with CHAR(n)?

- **sql-constraints** (typed): What happens when you delete or update a parent row referenced by a foreign key, and which referential actions can you declare?
  - Gate said: wrong_format: Asking to list which referential actions can be declared requires an open-ended enumeration.

- **sql-constraints** (typed): What is the difference between a PRIMARY KEY and a FOREIGN KEY?
  - Gate said: a human reviewer objected: What is the difference between a PRIMARY KEY and a FOREIGN KEY?

- **sql-constraints** (mcq): Which of the following is a separate column requirement often grouped with SQL constraints, rather than one of the common declarative constraints?
  - Gate said: not answerable: NOT NULL is standardly defined as a declarative constraint in SQL, making the question ambiguous and poorly defined.

- **sql-ddl-dml-dcl-tcl** (flash): In SQL, which command family includes CREATE, ALTER, DROP, and TRUNCATE?
  - Gate said: a human reviewer objected: In SQL, which command family includes CREATE, ALTER, DROP, and TRUNCATE?

- **sql-ddl-dml-dcl-tcl** (mcq): In SQL Server, after ROLLBACK TRANSACTION savepoint_name, what is the state of the outer transaction?
  - Gate said: a human reviewer objected: In SQL Server, after ROLLBACK TRANSACTION savepoint_name, what is the state of t

- **sql-group-by-and-having** (output): What is the exact output of this SQL query (do not include a row-count footer)?
```sql
CREATE TABLE t (team TEXT, salary INT);
INSERT INTO t VALUES ('red', 100), ('red', 200), ('blue', 50);
SELECT team FROM t GROUP BY team HAVING COUNT(*) > 1 ORDER BY team;
```
  - Gate said: not gradable: SQL query output lacks a standardized plain-text format across clients and engines (e.g. headers, delimiters).

- **sql-inner-vs-outer-join** (typed): What is a practical trade-off of using `LEFT JOIN` instead of `INNER JOIN` when you need all customers?
  - Gate said: not answerable: If you need all customers, an INNER JOIN does not satisfy the requirement, making the trade-off premise confusing or undefined.

- **sql-inner-vs-outer-join** (output): What is the exact output of this SQL query? Rows are shown as tab-separated values, ordered by `d.dept_name`.

```sql
WITH employees AS (
  SELECT 1 AS id, 'Alice' AS name, 10 AS dept_id
  UNION ALL SELECT 2, 'Bob', NULL
  UNION ALL SELECT 3, 'Carol', 20
),
departments AS (
  SELECT 10 AS id, 'HR' AS dept_name
  UNION ALL SELECT 20, 'Finance'
  UNION ALL SELECT 30, 'Legal'
)
SELECT e.name, d.dept_name
FROM employees e
RIGHT JOIN departments d ON e.dept_id = d.id
ORDER BY d.dept_name;
```
  - Gate said: not gradable: Exact representation of NULL in tabular output varies (e.g. NULL vs empty string vs None).

- **sql-null-handling** (output): What is the output of the following query?

Assume `employees` contains:
- Alice: phone = NULL, bonus = NULL
- Bob: phone = '555-0100', bonus = 100
- Carol: phone = '555-0101', bonus = 200

```sql
SELECT COUNT(*), COUNT(phone), AVG(bonus)
FROM employees;
```
  - Gate said: wrong_format: SQL query results have no standard textual formatting for column delimiters or tabular representation to allow exact-match grading.

- **sql-recursive-ctes** (flash): What are the three structural parts of a recursive CTE?
  - Gate said: wrong_format: Asking for three structural parts requires enumerating multiple components rather than a single crisp statement.

- **sql-recursive-ctes** (output): What is the exact output of this query?

```sql
WITH Numbers(n) AS (
    SELECT 1
    UNION ALL
    SELECT n + 1 FROM Numbers WHERE n < 3
)
SELECT * FROM Numbers;
```
  - Gate said: not gradable: Tabular SQL query results lack a standard single text representation for exact-match grading.

- **sql-row-number-rank-dense-rank** (typed): What happens if you use RANK() or DENSE_RANK() with an empty OVER clause, and is that allowed on all engines?
  - Gate said: not answerable: Engine-specific support for RANK() without an ORDER BY clause varies and is ambiguous without a specified SQL dialect or standard reference.

- **sql-running-totals-and-moving-averages** (flash): Write the window expression for a running total over rows ordered by sale_date.
  - Gate said: not answerable: The column to sum is unspecified, and there are multiple valid syntax variations for the window specification.

- **sql-subqueries** (output): What is the exact output of this query?

```sql
CREATE TABLE employees(id INT, name TEXT, dept_id INT, salary INT);
INSERT INTO employees VALUES
  (1, 'Alice', 10, 100),
  (2, 'Bob', 10, 150),
  (3, 'Chloe', 20, 120);

SELECT name
FROM employees e
WHERE salary > (SELECT AVG(salary)
                FROM employees d
                WHERE d.dept_id = e.dept_id);
```
  - Gate said: not gradable: SQL output formatting (header, borders, row delimiters) lacks a single standard plain-text representation for exact match.

- **sql-union-vs-union-all** (output): Given:
- orders_a rows: (1, 'East'), (2, 'West'), (2, 'West')
- orders_b rows: (2, 'West'), (3, 'North')

What is the output of this query?

```sql
SELECT order_id, region FROM orders_a
UNION
SELECT order_id, region FROM orders_b
ORDER BY order_id;
```
  - Gate said: not gradable: SQL tabular output lacks a single standardized plain-text format for exact matching.

- **sql-window-functions** (output): What is the output of the following SQL? Assume the employees table contains rows (name, salary): ('Ann', 80), ('Bob', 70), ('Cal', 70).

```sql
SELECT name, RANK() OVER (ORDER BY salary DESC) AS rnk
FROM employees
ORDER BY rnk, name;
```
  - Gate said: wrong_format: SQL tabular output has no single obvious text formatting or delimiter for exact-match grading.

- **two-pointers** (output): What is the exact output of this snippet?

```python
arr = [2, 7, 11, 15]
target = 9
left, right = 0, len(arr) - 1
while left < right:
    current = arr[left] + arr[right]
    if current == target:
        print(left + 1, right + 1)
        break
    elif current < target:
        left += 1
    else:
        right -= 1
```
  - Gate said: refers to unseen material: 'this snippet'
