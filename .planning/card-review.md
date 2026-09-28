# 90x card review

2805 cards are ready to publish. An automated gate read 2810 and objected to 92 of them (3%): 87 were rewritten and passed on the second look, 5 could not be saved and were dropped (0%). Mix: 1379 typed, 768 mcq, 596 flash, 62 output.

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

## 1. Dealing with ambiguity · mcq · Easy

*behavioral · gate confidence 0.7*

**Question**

At the senior level, an ambiguous project story should typically involve leading work across what scope of people?

**Options**

- Your own task
- Multiple people
- Multiple teams
- The entire company

**Reference answer**

Multiple people

**Graded on**

- Senior-level ambiguity involves leading a project with multiple people.
- Junior-level ambiguity is typically self-directed.
- Staff-level ambiguity involves multiple teams.
- Company-wide ambiguity is not typical for senior.

<details><summary>The lesson this came from</summary>

Dealing with ambiguity is the ability to make progress on a task when goals, constraints, or success criteria are unclear. It involves identifying what is unknown, asking targeted questions, documenting assumptions, and iterating as new information arrives. Interviewers evaluate it through stories of underspecified work, where the candidate took ownership and drove alignment.

## Why interviewers ask this

The interviewer is testing whether you can operate without a complete spec, since senior work is often assigned as a problem statement rather than a task list. They want evidence you can reduce ambiguity by gathering requirements, making decisions explicit, and bringing others along. At higher levels the scope changes: junior stories involve self-directed tasks, senior stories involve leading three or more people, staff stories involve multiple teams.

## The core idea

Ambiguity is reduced by turning hidden assumptions into explicit decisions. A strong candidate does not wait for clarity; they ask questions that resolve the highest-impact unknowns first, document what they assume, and revisit those assumptions when new data appears. The goal is not to eliminate uncertainty but to make enough of it concrete to move. Ownership means driving consensus, not just doing the work yourself. The scope of ambiguity you can handle grows with level: own task for junior, three-plus people for senior, two-plus teams for staff.

## Key points

- Junior-level stories typically involve taking ownership of an underspecified task and driving consensus among a few teammates.
- Senior-level stories typically involve an ambiguous project requiring three or more people to work on.
- Staff-level stories typically involve an ambiguous project requiring two or more teams to work on.
- Ask questions that resolve the highest-impact unknowns before accepting assumptions.
- Document assumptions and revisit them at checkpoints as new information arrives.

## Your 60-second answer

When I face ambiguity, I start by identifying what is actually unknown and which unknown, if resolved, would unblock the most work. I ask the stakeholder or manager targeted questions about goals, constraints, and success criteria, and I write down my assumptions so the team can correct them. For example, in an underspecified project, I proposed a minimum viable version, got agreement from the people affected, and then iterated as we learned more. The reason this works is that most ambiguity is not total; there are a few decisions that matter, and the rest can be deferred. The trade-off is that moving with explicit assumptions risks building the wrong thing, so I keep decisions reversible where possible and revisit them at checkpoints. Ownership means driving consensus, not just asking for clarity.

## If they dig deeper

**How do you decide what to work on next when there is no clear priority?**

I list the open tasks, then score each by impact and risk. Impact is what user or business goal it moves; risk is what happens if it is wrong or late. I also check dependencies and whether a task will clarify other unknowns. Then I pick the highest leverage task and communicate the reasoning so others can correct it.

**Tell me about a time a project was underspecified and what you did.**

In one project, I was given a vague request to improve a service. I started by interviewing the main stakeholders to understand the actual pain and constraints. I wrote a one-page problem statement with assumptions and a proposed milestone, then got agreement. That let us start on the highest-confidence part while we resolved the rest.

**How would you drive consensus when stakeholders disagree on what 'done' means?**

I would make the disagreement explicit by listing each stakeholder's success criteria and where they conflict. Then I would look for a minimal set of requirements everyone accepts and propose a decision rule, such as deferring disputed features behind a flag or giving priority to the user-facing outcome. If needed, escalate to the decision-maker with a clear trade-off table.

**What do you do when you discover midway that an assumption you made was wrong?**

I treat assumptions as reversible decisions. When one is falsified, I go back to the checkpoint where it was made, communicate the change to stakeholders, and adjust scope or direction. The key is to fail small: schedule assumptions to be tested early, so the cost of changing is low.

**How does your approach to ambiguity change at staff level, when you are coordinating multiple teams?**

At that level the ambiguity is often in ownership and interfaces, not just requirements. I define the problem boundary, identify which teams need to agree on contracts, and set up a lightweight decision log so cross-team assumptions are visible. I also delegate the parts that are unambiguous and spend my time on the unresolved interfaces. The hardest part is not solving the problem yourself; it is maintaining momentum when no one reports to you.

## Worked example

A strong answer sounds like: 'We were asked to make a checkout flow faster, with no target or constraints. I listed the unknowns: current latency, acceptable threshold, and whether we could change the payment provider. I measured p95 at 4 seconds and proposed a goal of under 2 seconds for the card flow. I documented that we would keep the existing provider initially and only revisit if batching calls was not enough. I took that proposal to the product lead and two backend engineers, got agreement, and broke the work into three pieces. We shipped the first piece, measured p95 at 2.8 seconds, and used that data to decide the next step.' The story shows identifying unknowns, attaching numbers, making assumptions explicit, and driving agreement.

## Common traps

- Waiting for a complete spec instead of reducing ambiguity yourself, which signals you need hand-holding.
- Asking broad questions like 'What do you want?' instead of targeted questions about goals, constraints, and trade-offs.
- Picking a story where someone else resolved the ambiguity, so the interviewer cannot see your ownership.
- Claiming you removed all ambiguity, when strong answers show how you managed irreducible uncertainty with checkpoints.

</details>

---

## 2. Lock interface and ReentrantLock · flash · Easy

*java · gate confidence 0.7*

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

The Lock interface in java.util.concurrent.locks, added in Java 5, is an explicit mutual-exclusion mechanism. ReentrantLock is its primary implementation: a reentrant, exclusive lock with the same memory-synchronization semantics as synchronized, but with timed acquisition via tryLock, interruptible locking via lockInterruptibly, multiple condition objects via newCondition, and optional fairness. Unlike synchronized, lock and unlock are not restricted to one block or method; the programmer must release the lock in a finally block.

## Why interviewers ask this

The interviewer is checking whether you can choose between synchronized and explicit locks, and whether you understand the lifecycle hazards of manual locking. They may also probe tryLock, interruptibility, fairness, and Condition, because those are the reasons an experienced engineer reaches for ReentrantLock.

## The core idea

ReentrantLock is a manual, feature-rich alternative to synchronized. It supports timed acquisition with tryLock, interruptible acquisition with lockInterruptibly, multiple condition queues through newCondition, and an optional fair mode. The cost is that you own both acquisition and release, so failing to call unlock in a finally block can leak the lock and deadlock other threads. Use synchronized for simple critical sections; reach for ReentrantLock when you need a timeout, need interruption, or want separate wait queues for different conditions. Reentrancy means a thread already holding the lock may acquire it again without deadlocking, and it must release once per acquisition.

## Key points

- Lock and ReentrantLock were introduced in Java 5 as part of java.util.concurrent.locks.
- ReentrantLock provides tryLock(long, TimeUnit) and lockInterruptibly(); a thread blocked entering a synchronized block cannot be timed out or interrupted.
- ReentrantLock can be constructed with fairness=true, which grants access to the longest-waiting thread and generally reduces throughput.
- Unlike synchronized, a ReentrantLock must be explicitly unlocked, typically in a finally block, and each successful lock() must be matched by an unlock().
- ReentrantLock supports multiple Condition objects via newCondition(), unlike a synchronized monitor's single wait set.

## Your 60-second answer

Lock is an interface in java.util.concurrent.locks, added in Java 5, for explicit mutual exclusion. Its main implementation, ReentrantLock, gives you the same basic mutual exclusion and memory visibility as synchronized, but it adds timed acquisition with tryLock(long, TimeUnit), interruptible acquisition with lockInterruptibly(), multiple condition variables through newCondition(), and an optional fair mode. You would use it when a thread should not block forever: it can try for a lock for a few hundred milliseconds and do fallback work, or it should abort if interrupted. The trade-off is that unlike synchronized, you must release it manually. If an exception occurs after lock() and before unlock(), the lock leaks, so the unlock must be in a finally block. For most simple critical sections synchronized is simpler and safer; ReentrantLock is for when you need those extra controls.

## If they dig deeper

**What is the difference between ReentrantLock and synchronized?**

Synchronized is built into the language and tied to a block or method; the JVM releases the monitor automatically on any exit, including exceptions. ReentrantLock is an explicit API: you call lock() and must call unlock() in a finally block. ReentrantLock adds timed tryLock, interruptible locking, multiple Condition objects, and optional fair scheduling; synchronized has none of those.

**When would you use tryLock instead of lock()?**

Use tryLock when a thread should not wait indefinitely. For example, a task can try for 500 milliseconds and then either do fallback work, retry later, or abandon the operation. A plain lock() blocks uninterruptibly until the lock is available; tryLock(long, TimeUnit) returns false if the timeout elapses and throws InterruptedException if the thread is interrupted while waiting.

**What does it mean that ReentrantLock is reentrant, and what can go wrong with a non-reentrant lock?**

Reentrant means a thread that already owns the lock can call lock() again without deadlocking; the lock keeps a hold count, and every lock() must be matched by an unlock(). In a non-reentrant lock, a recursive or callback path that reacquires the lock would block itself forever. With reentrancy, you can have one method call another that also locks the same lock.

**How do ReentrantLock and Conditions support more than wait/notify?**

A single synchronized monitor has one wait set, so wait() and notifyAll() wake all waiters, and you often need a condition predicate to recheck. ReentrantLock.newCondition() creates separate Condition objects, each with its own wait queue. A producer can signal only consumers waiting for 'not empty' rather than waking every thread. With multiple conditions you can model more precise state transitions and avoid unnecessary wakeups.

**What is the underlying mechanism behind ReentrantLock's blocking and acquisition?**

ReentrantLock delegates to an internal synchronizer that extends AbstractQueuedSynchronizer. An uncontended non-fair tryLock does a CAS on the synchronizer state from 0 to 1 and records the current thread as owner. If the same thread already holds the lock, the hold count is incremented. If another thread holds it, blocking lock() enqueues the thread in a CLH-like queue and uses LockSupport.park; timed tryLock returns false if the timeout expires.

## Worked example

Suppose a cache refresh task runs on a background thread while request threads read the cache. With a synchronized block, a request thread that reaches the refresh method blocks until the refresh completes, adding latency. With a ReentrantLock, the request thread can call lock.tryLock(200, TimeUnit.MILLISECONDS). If it returns true, the thread updates the cache and calls unlock() in a finally block. If it returns false, the thread serves the last completed value instead of blocking. If the thread is interrupted while waiting, tryLock throws InterruptedException, so the code can restore the interrupt flag and abort cleanly. A synchronized block cannot provide this timeout or interruptible behavior for a thread blocked on monitor entry.

## Common traps

- Forgetting to call unlock() in a finally block, which leaks the lock and can deadlock every other thread.
- Calling unlock() when the current thread does not hold the lock, which throws IllegalMonitorStateException.
- Using fairness=true by default; it grants near-FIFO ordering but reduces throughput and is only needed when strict ordering is required.
- Assuming ReentrantLock is always faster than synchronized; since Java 6, intrinsic locks have been optimized, so choose based on features, not performance folklore.

</details>

---

## 3. Supervised Learning · typed · Medium

*ai · gate confidence 0.8*

**Question**

Why is data quality important in supervised learning?

**Reference answer**

A model learns whatever patterns exist in the labels, so it inherits any bias or noise in the training data. Data collection and preprocessing are therefore part of model design, not separate chores.

**Graded on**

- Model inherits label bias and noise
- Data quality affects performance
- Preprocessing is part of model design

<details><summary>The lesson this came from</summary>

Supervised learning trains a model from a dataset of paired examples, each containing input features and a known target label. The learning algorithm searches for a function that maps inputs to outputs by minimizing a loss between predictions and known targets. The two main tasks are regression, where the target is a continuous value, and classification, where the target is a discrete class. The trained model is evaluated on examples not used during training.

## Why interviewers ask this

Interviewers use this topic to verify that you understand the core machine learning workflow rather than just API calls. They test whether you can choose an appropriate model and loss for a given target type, avoid overfitting, and evaluate results correctly under class imbalance. Follow-ups usually separate candidates who memorized definitions from those who can reason about generalization and metrics.

## The core idea

Supervised learning is an optimization problem: choose a function from a hypothesis space to minimize expected loss on unseen data. Because the true expected loss is unavailable, we approximate it with a training set and use a separate validation or test set to estimate generalization. Regression typically uses squared error loss for continuous targets; classification typically uses cross-entropy for discrete classes. The model matters only by its performance on new examples, not on training examples. Simpler models may underfit while complex models may overfit; regularization and validation manage this trade-off.

## Key points

- Supervised learning fits a function from labeled pairs (x, y) by minimizing a loss such as squared error for regression or cross-entropy for classification.
- Classification predicts discrete labels; regression predicts continuous values; logistic regression outputs a probability and becomes a classifier only after thresholding.
- Generalization is estimated on held-out data, not training data; training error alone overstates model quality.
- Overfitting means low training error but much higher validation error; regularization, early stopping, and cross-validation reduce it.
- For imbalanced classification, accuracy misleads; precision, recall, F1, and precision-recall AUC are preferred, while ROC-AUC can be optimistic because false positive rate is diluted by many true negatives.

## Your 60-second answer

Supervised learning trains a model on labeled examples: each input has a known target. The model learns a function from inputs to outputs by minimizing a loss, such as mean squared error for regression or cross-entropy for classification. Classification predicts a discrete class—spam or not spam—while regression predicts a continuous value like price. The point is to generalize to unseen data, so we evaluate on a held-out set. Overfitting is when the model memorizes training data and performs poorly on new data; regularization and cross-validation help. A practical trade-off is bias versus variance: simple models may underfit, complex models may overfit. In imbalanced classification, accuracy can be misleading; use precision, recall, F1, and precision-recall AUC rather than relying on ROC-AUC for the minority class.

## If they dig deeper

**What is the difference between supervised and unsupervised learning?**

Supervised learning uses labeled examples, so each input has a known target and the model learns to map inputs to outputs. Unsupervised learning has no labels and looks for structure such as clusters or low-dimensional representations. Clustering is unsupervised; spam detection with labeled emails is supervised.

**How do you tell whether a supervised model is overfitting?**

Compare performance on training and validation sets. If training loss is much lower than validation loss, the model is memorizing training details. Cross-validation, regularization, reducing model capacity, or early stopping can close that gap.

**Why is accuracy a poor metric for imbalanced classification, and what should you use instead?**

Accuracy counts correct predictions across all classes, so a model that always predicts the majority class can score high—for example, 99% accuracy when only 1% of examples are positive. Precision, recall, F1, and precision-recall AUC focus on the positive or minority class and are more informative.

**How does logistic regression output a class if it is a regression model?**

Logistic regression estimates P(y=1|x) using a linear combination passed through the sigmoid function. A decision threshold, often 0.5, assigns the positive class when the probability exceeds it. The threshold can be tuned to trade precision against recall based on misclassification costs.

**For a highly imbalanced binary classifier, why can ROC-AUC look optimistic while precision-recall AUC is more informative?**

ROC-AUC plots true positive rate versus false positive rate, and false positive rate divides false positives by all true negatives. When negatives dominate, even many false positives keep the false positive rate small, so ROC-AUC can stay high despite poor minority-class performance. Precision-recall AUC uses precision = TP/(TP+FP), which punishes every false positive relative to the small positive set, so it tracks the minority class more directly. For imbalance, PR-AUC is generally the more informative summary.

## Worked example

Consider a test set of 100 emails: 5 are spam (positive) and 95 are not. A model flags 3 emails as spam; 2 are actually spam and 1 is not. Accuracy is (2 true positives + 94 true negatives) / 100 = 96%, which looks strong. Precision is 2/(2+1) ≈ 0.67 and recall is 2/5 = 0.40, so the model misses 3 of every 5 spam emails. At this threshold the false positive rate is 1/95 ≈ 0.011 while the true positive rate is 0.40—a point well above the ROC diagonal. Lowering the threshold to catch more spam adds false positives; precision drops sharply because there are so few true positives, which precision-recall AUC captures more directly than ROC-AUC.

## Common traps

- Calling logistic regression a classifier without noting it outputs probabilities and requires a threshold.
- Evaluating a model on the same data used for training, which inflates performance.
- Using accuracy alone on imbalanced data and concluding the model is strong.
- Treating ROC-AUC as the default metric for imbalanced problems when precision-recall AUC is generally more informative for the minority class.

</details>

---

## 4. Unsupervised Learning · flash · Easy

*ai · gate confidence 0.85*

**Question**

Name the three main tasks of unsupervised learning.

**Reference answer**

Clustering, dimensionality reduction, and density estimation.

**Graded on**

- Clustering groups similar observations
- Dimensionality reduction produces a lower-dimensional representation
- Density estimation learns the probability distribution over inputs

<details><summary>The lesson this came from</summary>

Unsupervised learning is a machine learning paradigm that models structure in data without labels or target outputs. Its main tasks are clustering, which groups similar observations; dimensionality reduction, which produces a lower-dimensional representation while preserving relevant structure; and density estimation, which learns the probability distribution over the input space. Common algorithms include k-means, hierarchical clustering, DBSCAN, Gaussian mixture models, PCA, t-SNE, and kernel density estimation, each optimizing an objective such as within-cluster variance, reconstruction error, or likelihood rather than label accuracy.

## Why interviewers ask this

Interviewers ask this to test whether you can choose and justify an algorithm when there is no ground truth. They are checking that you know the assumptions behind clustering and dimensionality reduction, how to evaluate results without labels, and where methods fail on scaled, high-dimensional, or non-spherical data.

## The core idea

In supervised learning, labels define what the model must learn. Unsupervised learning must supply that definition through assumptions: similar points belong together, high-dimensional data often lies near a lower-dimensional manifold, or the data can be described by a probability distribution. Each algorithm encodes a different assumption. K-means assumes spherical, similarly sized clusters; DBSCAN assumes clusters are dense regions separated by sparse ones; PCA assumes the directions with largest variance are informative. When the assumption matches the data, the method works; when it does not, the output may be an artifact.

## Key points

- Clustering groups unlabeled data by similarity; common approaches include centroid-based k-means, connectivity-based hierarchical clustering, density-based DBSCAN, and probabilistic Gaussian mixture models.
- K-means minimizes within-cluster squared distance to centroids, requires k in advance, and assumes roughly spherical, similarly sized clusters; it is sensitive to feature scaling and outliers.
- PCA constructs orthogonal linear components that maximize variance, so features with larger numeric ranges dominate unless the data are standardized first.
- t-SNE is a nonlinear visualization method that preserves local neighborhoods, not global distances; distances, cluster sizes, and densities in a t-SNE plot are unreliable.
- With no labels, clustering is usually evaluated with internal measures such as the silhouette coefficient or by measuring performance on a downstream task.

## Your 60-second answer

Unsupervised learning finds structure in data that has no labels or target values. Instead of learning an input-to-output mapping, it models the data itself. The three main tasks are clustering, dimensionality reduction, and density estimation. Clustering groups similar points: k-means is fast and simple but requires the number of clusters and assumes round clusters; DBSCAN finds arbitrarily shaped clusters and outliers but needs density parameters; hierarchical clustering builds a tree of nested groups. Dimensionality reduction compresses features: PCA projects onto directions of maximum variance, and t-SNE is nonlinear and used mostly for visualization. Density estimation learns the data distribution, for example with Gaussian mixture models. The hard part is evaluation because there is no ground truth, so you rely on internal metrics such as silhouette score or a downstream task. The main trade-off is that simpler assumptions scale and interpret well but miss structure the data doesn't satisfy.

## If they dig deeper

**What is the difference between supervised and unsupervised learning?**

Supervised learning trains on input-output pairs and evaluates predictive accuracy; unsupervised learning has only inputs and must discover structure such as clusters, components, or density. Unsupervised evaluation is harder because there is no ground-truth label to score against.

**How does k-means work and how do you choose k?**

K-means alternates between assigning each point to the nearest centroid and recomputing centroids as cluster means until convergence. It minimizes within-cluster sum of squares. Choose k using the elbow method, silhouette score, or domain requirements, but the method always assumes spherical clusters.

**When would you use DBSCAN instead of k-means?**

Use DBSCAN when clusters are non-spherical, outliers should be flagged, or the number of clusters is unknown. It identifies dense regions with the eps and minPts parameters and labels sparse points as noise. Avoid it when clusters vary widely in density because a single eps may not fit all of them.

**Why does feature scaling matter for PCA?**

PCA finds the directions of maximum variance in the data. If one feature has a much larger numerical range, its variance dominates the covariance matrix, so early principal components align with that feature rather than reflecting correlation structure. Standardizing features to zero mean and unit variance makes each feature contribute comparably.

**Why can t-SNE show clusters that are not present in the original data?**

t-SNE minimizes the Kullback-Leibler divergence between high-dimensional pairwise similarities and low-dimensional similarities, using a heavy-tailed Student-t distribution to handle crowding. It preserves local neighborhoods but distorts global distances and densities, so the perplexity parameter can make separated groups appear or disappear. It is a visualization tool, not proof that clusters exist.

## Worked example

For a point in a compact cluster, suppose the mean distance to points in its own cluster is a=1.3 and the mean distance to points in the nearest other cluster is b=10. Its silhouette score is (10-1.3)/10≈0.87, near +1, indicating the point lies well inside its cluster. If the same point sat halfway between the clusters, with a=5 and b=5, the score is 0. If it were placed among points of the other cluster, a=10 and b=1, the score is (1-10)/10=-0.9. Averaging per-point scores gives the cluster-level silhouette; high positive averages mean dense and well-separated clusters, while near-zero averages suggest overlap. The metric therefore measures separation relative to compactness, not just closeness.

## Common traps

- Saying k-means can find any cluster shape; it is a centroid method that favors convex, roughly spherical clusters and fails on elongated or ring-shaped groups.
- Ignoring feature scale before PCA or k-means, so high-range features dominate distances or variance and the result is driven by units rather than structure.
- Treating a t-SNE plot as a reliable map of global distances or cluster sizes; t-SNE preserves local neighborhoods and can create misleading separations.
- Choosing the number of clusters only from an elbow plot without checking silhouette or domain interpretability, which often leaves ambiguous cases unresolved.

</details>

---

## 5. Leadership · flash · Medium

*behavioral · gate confidence 0.85*

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

In behavioral interviews, leadership is the ability to guide a team or group toward a shared outcome without relying on formal authority. It includes vision-setting, stakeholder influence, thought leadership, and critical-situation leadership. Strong answers describe the concrete mechanisms—communication cadence, decision frameworks, relationship building—rather than claiming a title or listing team size.

## Why interviewers ask this

Interviewers ask leadership questions to test whether a candidate can operate at the expected level of scope and ambiguity: can they influence across teams, think systematically, and keep a group effective under pressure? They are probing judgment, self-awareness, and communication, not checking whether the candidate held a manager title. Senior candidates are also watched for common failures like unstructured stories, actions without frameworks, and answers that bury the signal in detail.

## The core idea

Leadership in a behavioral answer means showing influence without authority: you changed what people did or believed by building credibility, communicating a clear direction, and managing relationships. Interviewers care less about your title than about the mechanisms you used—how you made a decision, how you brought others along, and how you maintained morale during uncertainty. Strong answers deliberately cover multiple dimensions of leadership: people, strategy, stakeholders, risk, and change management, not just a technical or product win. They also state the decision-making framework behind the actions, because listing actions alone makes a senior candidate sound like an executor.

## Key points

- Product managers and senior engineers typically lead through vision, credibility, and relationships rather than direct authority.
- Critical-situation leadership requires clear communication, decisive action, and deliberate attention to team morale while navigating uncertainty.
- Thought leadership—publishing, speaking, or contributing original perspectives—builds personal and company credibility over time.
- Senior behavioral answers are expected to cover multiple leadership dimensions: people, strategy, stakeholders, risk, and change management, not only technical or product outcomes.
- A common senior failure is narrating actions without naming the decision-making framework that produced them, which makes the candidate sound like an executor.

## Your 60-second answer

Leadership in an interview means influence without formal authority: you moved a group toward a better outcome by setting direction, building credibility, and managing relationships. I'd answer with a specific situation where I had to align people who didn't report to me. I would open with the decision I needed to make and the framework I used, then describe how I communicated it and handled resistance or pressure. The trade-off is that influence without authority is slower; you have to earn trust first, so a strong answer also shows the upfront investment in listening and adjusting the plan. I would close with what actually changed—adoption, risk, morale, or delivery—so the interviewer sees scope, not just activity.

## If they dig deeper

**Tell me about a time you influenced a team without formal authority.**

A strong answer names the specific stakeholder or team, what they initially believed, the mechanism used to change their position—data, framing, relationships, or a pilot—and the observable result. It avoids saying 'I convinced them' and instead shows the steps that led to changed behavior.

**How do you handle a high-pressure crisis or significant disruption?**

A strong answer describes clear communication cadence, prioritization of what not to do, preserving team morale, and a defined owner for decisions. It often includes a simple triage framework: stabilize, communicate, decide, and review afterward.

**How do you demonstrate thought leadership?**

A strong answer cites concrete artifacts—internal design docs, blog posts, talks, or open-source contributions—and ties them to a distinctive point of view that influenced a real decision. It focuses on changed thinking or adoption, not just visibility or publication count.

**What was the most difficult leadership decision you made, and what framework did you use?**

A strong answer names the explicit trade-offs, the decision criteria, who was consulted, and how the decision was communicated to stakeholders who disagreed. It avoids listing actions and instead reconstructs the reasoning.

**Tell me about a time you led through change when the team was resistant.**

A strong answer diagnoses the actual source of resistance—loss of autonomy, extra work, unclear benefit—then describes aligning incentives, sequencing a small reversible pilot, and creating visible early wins. It also shows how the candidate managed upward and adjusted the plan rather than pushing the original agenda unchanged.

## Worked example

A strong answer sounds like: 'As a senior engineer, I saw that [specific cross-team problem] was causing repeated delays. I had no authority over the other teams, so I started by documenting the actual pain in [a short internal note] and framing the proposal around [what those teams cared about]. I met each lead individually, collected their objections, and changed the rollout order so the lowest-risk team could go first. I made the decision criteria explicit: if we hit [specific threshold], we would escalate or adjust scope. I communicated that plan in a weekly update and kept a visible risk list. When one lead resisted, I asked what they would need to feel safe proceeding, and we turned that into a smaller pilot. In the end I measured whether [the actual pain] changed, not just whether people said yes.'

## Common traps

- Confusing a management title with leadership, so the story relies on authority and reporting lines instead of influence and persuasion.
- Listing actions chronologically without naming the decision framework or trade-offs, which makes a senior answer sound like project execution.
- Telling the story from only one leadership dimension, such as technical design, and omitting people, stakeholder, risk, or change management aspects.
- Being verbose and letting interviewer interruptions pull the story into rabbit holes, so the core signal about scope and judgment never lands.

</details>

---

## 6. Handling feedback · typed · Easy

*behavioral · gate confidence 0.85*

**Question**

When receiving feedback as a software engineer, what sequence of steps helps you handle it effectively?

**Reference answer**

Pause before responding to separate the substance from your emotional reaction, clarify by restating the feedback and asking for a concrete example if it is vague, then act or negotiate: either make the change or propose an alternative that addresses the same concern. Finally, close the loop by telling the person what changed or what decision was reached.

**Graded on**

- Pause before responding
- Restate and clarify the feedback
- Act or negotiate based on the underlying concern
- Close the loop with the person who gave feedback

<details><summary>The lesson this came from</summary>

Handling feedback is the behavioral skill of receiving an evaluation of your work or behavior, understanding the underlying concern, deciding whether and how to change, and closing the loop with the person who gave it. In SDE work this happens in code review comments, design review discussions, and manager or peer conversations. It covers both technical feedback, such as a cache invalidation being wrong, and behavioral feedback, such as interrupting a junior engineer in a meeting. The mechanism that matters is not agreeing with everything, but making a deliberate choice after understanding the point.

## Why interviewers ask this

Interviewers use feedback questions to probe coachability and self-awareness. A developer who becomes defensive or cannot name a concrete change they made after feedback is a retention and velocity risk. The question also tests whether the candidate can disagree productively, which is what actually happens in design and code review.

## The core idea

Feedback is signal about a specific artifact or behavior, not a verdict on your worth. The reliable pattern is pause, clarify, act or negotiate, and close the loop. Pausing matters because the first instinct under criticism is to defend; if you answer in that state, you will argue instead of listening. Clarifying means restating the concern in your own words and asking for a concrete example when the feedback is vague. Acting or negotiating means you either make the change or explain the trade-off and propose an alternative that addresses the same concern. Closing the loop means telling the reviewer or manager what you changed and why, so the feedback has a recorded outcome.

## Key points

- Good feedback handling begins by separating the substance of feedback from the emotional reaction to being criticized.
- A strong response restates the feedback to confirm understanding before defending or acting.
- In code review, responding to feedback by explaining intent without addressing the concern is perceived as defensive.
- Acting on feedback means closing the loop: implementing the change and telling the reviewer or manager what changed.
- Behavioral feedback is often harder to assess than technical feedback and requires asking for specific examples.

## Your 60-second answer

When I get feedback, I focus on understanding the specific change being requested and the reason behind it before I respond. I pause long enough to separate the substance of the comment from my own reaction, and if the feedback is vague, I ask for a concrete example or the failure case the person is worried about. Then I act. If I agree, I make the change and close the loop by telling the reviewer or manager what I did; if I disagree, I explain the trade-off concretely and try to offer an alternative that resolves their underlying concern. The main risk I watch for is defensiveness: explaining why I wrote it that way without addressing their concern. That reads as resistance even when I think I am being helpful.

## If they dig deeper

**Tell me about a time you received feedback you disagreed with.**

I start by separating the reviewer's underlying concern from the specific suggestion. I ask what failure they are trying to prevent, then explain my approach's trade-off and offer an alternative that addresses that failure. If we still disagree, I record the decision and move on rather than relitigating the point.

**How do you get feedback when people are not giving it?**

I ask narrow questions about a recent artifact, such as 'Which part of this design is hardest to operate?' instead of asking for general feedback. In one-on-ones I bring a specific situation and ask what the manager would have done differently. That produces actionable answers more reliably than a broad request.

**What do you do after receiving feedback you know you will not act on?**

I acknowledge the feedback and state clearly that I have decided not to apply it, with the reason and the trade-off I am accepting. If the concern is real but the suggested fix is wrong, I propose a different way to solve the same problem. I never silently ignore it, because that leaves the other person waiting and breaks trust.

**How do you handle conflicting feedback from two senior engineers?**

I put both suggestions against the actual constraint: correctness, maintainability, schedule, or a documented requirement. Then I ask each person what problem they are trying to prevent, which often shows the conflict is about priorities rather than facts. If it remains unresolved, I bring the decision to the owner or team lead with the trade-offs laid out.

**Have you ever had to give feedback to someone more senior than you?**

Yes, I frame it as an observation with a concrete impact, not a judgment about their ability. I say what I saw, what effect it had, and ask whether that was the intent. I do it privately and tie it to a shared goal, like unblocking an on-call issue.

## Worked example

A strong answer sounds like: 'In a previous role, I opened a pull request that added an in-memory cache to a read-heavy endpoint. A senior engineer commented that an admin update would leave the cache stale. My first reaction was that the admin path was rare, but I waited a few minutes before replying. I asked whether the concern was stale data for all users or only for the admin view. She said all users, because the public page used the same record. I changed the cache key to include a version number, added integration tests for the admin update path, and linked the new tests in the comment. She approved the change. I later used the same versioned-cache idea in another service.' That shows a pause, a clarifying question, a technical fix aimed at the real concern, and a closed loop with concrete evidence.

## Common traps

- Treating feedback as an attack on personal ability rather than a claim about an artifact or behavior.
- Responding only by explaining intent instead of addressing the concern, which reads as defensive.
- Accepting vague feedback without asking for a concrete example, then guessing what to change.
- Silently ignoring feedback you disagree with instead of surfacing the disagreement and aligning on a decision.

</details>

---

## 7. CPU Scheduling · typed · Medium

*cs · gate confidence 0.85*

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

CPU scheduling is the policy an operating system uses to decide which ready thread runs on which CPU core and for how long before being preempted or yielding. It mediates between runnable threads using algorithms such as First-Come First-Served (FCFS), Shortest Job First (SJF), Round Robin (RR), priority queues, and multi-level feedback queues (MLFQ). Schedulers optimize different metrics: response time for interactivity, turnaround time for batch work, throughput, and fairness. A scheduler may be non-preemptive, letting a job run until it blocks or terminates, or preemptive, interrupting a running job at a time quantum or higher-priority event.

## Why interviewers ask this

Interviewers use CPU scheduling questions to see whether candidates can reason about a system tradeoff instead of memorizing an algorithm. A strong answer names the metric being optimized, the cost of context switching, and what the scheduler must know to achieve a given bound. They may push with follow-ups about starvation, I/O, or multicore cache effects to test operating-systems depth.

## The core idea

CPU scheduling is a tradeoff between responsiveness and turnaround time, and the algorithm's value depends on whether the workload is interactive, batch, or mixed. FCFS is simple but suffers convoy effects. SJF minimizes average turnaround for known runtimes but starves long jobs. Round robin guarantees short response by rotating a fixed quantum, but pays context-switch overhead and can degrade throughput. Real schedulers use MLFQ to infer whether a thread is I/O-bound or CPU-bound by observing how much of a quantum it uses, rather than requiring job lengths. On multicore systems, good schedulers also preserve cache affinity by keeping a thread on its last core when possible; migration does not invalidate caches, but causes cold misses in the new core's cache and TLB.

## Key points

- FCFS runs jobs in arrival order and performs poorly when a long CPU-bound job arrives before many short jobs, creating a convoy effect that inflates average waiting time.
- SJF minimizes average waiting and turnaround when all jobs are available and runtimes are known, but long jobs can starve if short jobs keep arriving.
- Round robin rotates runnable jobs in units of a time quantum; it lowers response time, but a quantum that is too small causes excessive context switches and reduced throughput.
- MLFQ approximates SJF-like turnaround for short jobs and Round Robin-like responsiveness for interactive jobs by demoting jobs that use full quanta and boosting jobs that wait too long.
- On multicore systems, moving a thread to another core does not invalidate the old core's cache, but loses cache affinity and causes cold cache misses on the new core; per-core TLB entries must be reloaded as pages are touched.

## Your 60-second answer

CPU scheduling is the policy that decides which runnable thread gets a CPU core and for how long. The classic algorithms are FCFS, SJF, and Round Robin, with multi-level feedback queues as a common practical combination. FCFS is simple but creates convoy effects: a long CPU-bound job makes every shorter job queue behind it. SJF, or shortest-job-first, minimizes average turnaround time if job lengths are known in advance, because finishing short jobs first reduces everyone's waiting time, but it can starve long jobs. Round robin gives each job a small time slice and cycles through the ready queue, which keeps response time low for interactive work but adds context-switch overhead and can hurt throughput if the quantum is too small. Practical schedulers often use MLFQ, treating jobs that block early as interactive and high priority, while CPU-bound jobs get demoted, so the system adapts without knowing runtimes in advance.

## If they dig deeper

**What is the difference between preemptive and non-preemptive scheduling?**

Preemptive scheduling can interrupt a running job to run a higher-priority job or when its time quantum expires; non-preemptive scheduling lets a job keep the CPU until it blocks, yields, or completes. Round robin and most modern OS schedulers are preemptive, while FCFS and non-preemptive SJF are examples of non-preemptive policies.

**How does the round-robin time quantum affect performance?**

A very long quantum makes Round Robin behave like FCFS and hurts response time for interactive jobs. A very short quantum increases the number of context switches, consuming CPU time on saving and restoring state, lowering throughput, and increasing average turnaround. The quantum should be long enough to amortize context-switch overhead but short enough to provide interactive responsiveness.

**Why can't the OS simply use SJF at all times?**

SJF requires knowing future CPU burst lengths, which a general-purpose OS typically does not have. It can predict runtimes using exponential averaging of past bursts, but predictions can be wrong. SJF also risks starving long-running jobs if a steady stream of shorter jobs arrives.

**How does an MLFQ schedule without knowing job lengths?**

MLFQ maintains multiple priority queues. A new job starts in the highest queue; if it uses a full time slice it is demoted to a lower queue, and if it blocks or yields before the slice ends it stays or is promoted. Jobs that wait too long are periodically boosted to the top to prevent starvation. This lets interactive I/O-bound jobs stay responsive while CPU-bound jobs run in the background, approximating SJF for short jobs and Round Robin for interactive ones.

**Why does a multicore scheduler care about cache affinity?**

A thread that repeatedly runs on the same core keeps its working set in that core's private caches and has valid per-core TLB entries. Moving threads does not invalidate caches, but the old core's cached lines stop helping that thread, the new core starts with cold caches, and per-core TLB entries must be refilled by page walks. Schedulers often use per-core run queues and keep threads on the same core when possible, migrating only to balance load.

## Worked example

Take three CPU-bound jobs arriving at time 0 with runtimes P1 = 24 ms, P2 = 3 ms, P3 = 3 ms. Under FCFS in that order, completions are 24, 27, 30 ms; waiting times are 0, 24, 27 ms, so average waiting is 17 ms. If the scheduler uses non-preemptive SJF, it runs P2, then P3, then P1: completions are 3, 6, 30 ms, and waiting times are 0, 3, 6 ms, for an average of 3 ms. Round Robin with a 3 ms quantum runs P1 for 3 ms, then P2 and P3 to completion, then P1 in remaining 3 ms slices until 30 ms; waiting times are 6, 3, and 6 ms, for an average of 5 ms. Round Robin's response time is much better than FCFS and close to SJF here, but its average turnaround is worse than SJF because P1 is repeatedly preempted.

## Common traps

- Saying SJF always minimizes response time or is generally the best scheduler; it minimizes average waiting and turnaround only with known runtimes and all jobs available, and it can damage interactive response or starve long jobs.
- Assuming a shorter Round Robin quantum always improves performance; below some point context-switch overhead dominates and throughput drops.
- Conflating latency and throughput; a batch scheduler can maximize throughput while individual jobs wait a long time, and a low-latency scheduler may sacrifice total work completed per second.
- Claiming that moving a thread to another core invalidates that core's cache; cache coherence keeps lines consistent, but the thread loses cache affinity and pays cold-cache and TLB miss costs on the new core.

</details>

---

## 8. Design · typed · Medium

*dsa · gate confidence 0.85*

**Question**

What is your first step when designing a data structure for a list of required methods, and how do you choose the structures?

**Reference answer**

List every method and its required complexity, choose a primary structure for the hot-path operation, then add an auxiliary structure only for outlier operations.

**Graded on**

- start from operations and complexities
- primary structure for hot path
- auxiliary structure for outlier
- state worst-case and amortized costs

<details><summary>The lesson this came from</summary>

In DSA interviews, "Design" usually means data-structure design: implement a small stateful class such as a hit counter, logger rate limiter, snapshot array, allocator, or max stack with a fixed API. The solution is a composition of standard structures—arrays, hash maps, queues, iterators, and balanced trees—plus rules that keep every operation inside its time and space bounds. It is not distributed-system design; it is about class invariants, lazy eviction, duplicate handling, and amortized costs.

## Why interviewers ask this

Interviewers use these problems to test whether you can turn a list of method requirements into concrete data structures instead of reaching for a familiar class. Frequency data shows design tasks appearing at companies such as Databricks, Dropbox, Spotify, Meta, OpenAI, Snowflake, Coinbase, LinkedIn, and Apple, so interviewers expect clean trade-off reasoning and edge-case handling.

## The core idea

Start from the operation list and required complexities, not from a favorite data structure. Pick a primary structure for the hot-path operation, then add an auxiliary structure only for the outlier operation—an array plus hash map for getRandom, a queue with lazy pruning for sliding windows, a stack plus balanced BST and cached max for max stack. Keep invariants explicit: what is stored, when it is removed, and how duplicates are represented. For versioned or snapshot data, store per-index change history instead of copying the whole structure. The strongest answers state worst-case and amortized costs for each method, not just the design.

## Key points

- Time-window designs like a hit counter or logger rate limiter store only the entries or per-bucket counts needed for the window and lazy-evict expired items, giving O(1) writes and often amortized O(1) reads.
- A moving average from a stream uses a fixed-size circular array and a running sum, so update and query are both O(1).
- For O(1) insert/delete/getRandom, keep a dynamic array plus a hash map from value to a set of indices, and on remove swap the selected element with the last element.
- A flatten nested list iterator can avoid eager flattening by using an explicit stack of iterators, making next/hasNext O(1) amortized and using O(depth) extra space.
- A max stack uses a doubly linked list for stack order, a balanced BST keyed by value, and a cached maximum; peekMax is O(1), while push/pop/popMax are O(log n).

## Your 60-second answer

A design question asks me to implement a small stateful class with a fixed API, so I start by listing every method and its required complexity, then choose a primary structure and augment it for any operation that does not fit. For a sliding-window counter I would keep timestamps in a queue and prune expired entries; for a moving average I would keep a circular array and a running sum; for getRandom I would pair an array with a hash map and swap with the last element; for a max stack I would combine a doubly linked list with a balanced BST and a cached max, so peekMax is O(1) and push/pop/popMax are O(log n). I also check duplicates, empty states, and concurrency. The trade-off is usually extra bookkeeping space or update cost in exchange for making the hot-path operation fast.

## If they dig deeper

**How do you reduce memory in a hit counter that receives thousands of hits per second?**

Bucket hits by second. Keep a circular array of 300 one-second buckets plus a running total; on getHits, drop buckets older than 300 seconds and return the total. Memory is bounded by the window, and both hit and getHits become O(1).

**Why does the swap-with-last trick fail for duplicates if you only store one index per value?**

The same value can appear in multiple array slots, so a single index cannot update all affected positions when one occurrence is removed. Store a value to a set of indices; on remove pick any index from the set, swap the last element into it, update the swapped element's index in its set, and remove the chosen index. This keeps expected O(1) operations.

**How do you make a nested list iterator lazy instead of flattening in the constructor?**

Keep an explicit stack of iterators over the nested structure. hasNext advances until the top points at an integer; next returns that integer. Work is distributed across calls, so next/hasNext are O(1) amortized per element and memory is O(depth) rather than O(total elements).

**How do you implement a max stack with popMax and peekMax without scanning the stack?**

Use a doubly linked list for stack order and a balanced BST keyed by value to a list of nodes, plus a cached max. peekMax reads the cached max in O(1). push inserts into both structures; pop removes the head and its map entry; popMax removes the most recent node for the current maximum. Map updates keep push/pop/popMax at O(log n).

**How would you design a memory allocator to support allocate and free without O(n) scans?**

Keep free blocks in an ordered structure—by size for allocation and by address for coalescing—rather than one unsorted list. On free, look up neighboring blocks and merge them into a single free segment to reduce fragmentation. This turns allocate into a logarithmic or constant-time search in the chosen free list, while coalescing keeps the free list useful over time.

## Worked example

Design a hit counter for a 300-second window. Keep a double-ended queue of hit timestamps. hit(t) appends t. getHits(now) first removes from the front while the front timestamp is <= now - 300, then returns the queue size. If hits arrive at 1, 2, and 301, then getHits(302) has cutoff 2; it dequeues 1 and 2, leaves 301, and returns 1. The key is that each timestamp is dequeued at most once, so repeated getHits calls are amortized O(1) per returned hit.

## Common traps

- Picking a data structure before enumerating the API; this causes hidden O(n) operations such as getRandom after choosing only a hash set.
- Storing one index per value in Insert Delete GetRandom; duplicate values need a value -> set of indices, or remove corrupts the mapping for other occurrences.
- Claiming peekMax on a max stack is O(log n); with a cached maximum it is O(1), while push/pop/popMax are O(log n) because of the balanced BST.
- Rescanning the entire window on every hit counter or logger call instead of lazy-evicting expired entries once, which changes amortized O(1) reads to O(n).

</details>

---

## 9. Memory leaks · typed · Medium

*java · gate confidence 0.85*

**Question**

What is the key trade-off of garbage collection with respect to memory leaks?

**Reference answer**

The garbage collector prevents manual deallocation bugs but cannot infer that an object is no longer needed. If a strong reference path exists, the object is considered reachable and survives; managing reachability is the developer's responsibility.

**Graded on**

- GC gives memory safety
- GC cannot detect intent
- strong reachability means survival

<details><summary>The lesson this came from</summary>

In Java, a memory leak is the unintended retention of objects the application no longer needs because a strong reference path from a GC root keeps them alive. The garbage collector only reclaims objects that are unreachable from the root set, so these objects remain on the heap. Over time this can exhaust the Java heap or, for classloader leaks, Metaspace, and the JVM throws OutOfMemoryError.

## Why interviewers ask this

The interviewer is checking whether you understand that the garbage collector does not guarantee freedom from memory leaks, and whether you can reason about object reachability and GC roots. A strong answer names concrete leak patterns and diagnosis steps rather than just reciting a definition.

## The core idea

A Java memory leak is not lost memory; it is an object that the application no longer needs but that remains strongly reachable from at least one GC root. In HotSpot, GC roots include static fields of loaded classes, active thread stacks, and JNI global references, so any object reachable from them survives collection. The classic leak is an unbounded static collection; a more subtle one is a leaked classloader, where one retained instance or class keeps an entire custom classloader, all its classes, and all static data alive. That case affects both heap and Metaspace since Java 8.

## Key points

- A Java leak means objects are reachable but unused; the GC cannot free objects with a live strong reference path from a GC root.
- Static fields, active thread stack references, JNI global references, and thread-locals under a thread pool are common roots that pin objects.
- Classic causes: static collections/caches without eviction, unclosed resources, callbacks/listeners registered globally, inner classes holding outer references, and ThreadLocal misuse.
- A classloader leak retains not only class metadata in Metaspace (since Java 8) but also the ClassLoader, Class objects, and all static fields in the Java heap.
- Diagnosis uses heap dumps and histogram analysis (jmap/MAT/VisualVM) and GC logs; compare object counts by class across time to find growth.

## Your 60-second answer

In Java, a memory leak is not memory that becomes unreachable; it is the opposite: objects the application no longer needs remain strongly reachable from a GC root, so the garbage collector cannot reclaim them. The classic example is a static HashMap that you keep adding request data to without removing entries. The static field is a GC root; the map is reachable from that field, and every entry pins its value in the heap. Over time the heap fills up and the JVM throws OutOfMemoryError. The trade-off is that the garbage collector gives you memory safety, but it cannot detect that you intended to discard an object; as long as a reference path exists, the object survives. Diagnosis usually means taking a heap dump and finding which classes and reference chains are growing.

## If they dig deeper

**How is a Java memory leak different from a C or C++ memory leak?**

In C/C++ you can allocate memory and then lose the pointer, so the memory remains allocated but unreachable; that is a leak. In Java an object is only collectible when no strong reference path from a GC root exists, so a Java leak is the reverse: the object is still reachable, but the application never uses it again. The GC cannot distinguish 'still referenced' from 'still needed'.

**What steps do you take when you suspect a memory leak in production?**

First observe GC logs and heap usage over time to confirm growth and see whether it is heap or Metaspace. Then capture a heap dump with jcmd or jmap and analyze it in Eclipse MAT or VisualVM, looking at the histogram and dominator tree for object counts that grow. Trace the GC root path for the largest retained objects, identify the unintended reference, and remove it with proper eviction, unregistration, or resource closing.

**Why does a static HashMap cause a memory leak?**

A static field on a loaded class is a GC root. The HashMap instance is reachable from that field, and every key and value in the map is strongly reachable through the entry array. If entries are never removed, the map grows without bound. The HashMap itself is not the root; the static reference on the class is the root that keeps it alive.

**Explain how a classloader leak happens and whether it shows up as heap or Metaspace OutOfMemoryError.**

A custom classloader and its loaded classes reference each other: each Class points to its defining ClassLoader, and the loader points to all its classes. If any instance or class from that loader remains reachable—such as a background thread, listener, or static field—the entire loader graph stays alive. Since Java 8, class metadata is stored in Metaspace, so repeated redeploys can exhaust Metaspace. But the ClassLoader object, Class objects, and all static field values live in the Java heap, so a classloader leak often exhausts the heap as well, not just Metaspace.

**How can ThreadLocal values leak in a thread pool, and why is that leak harder to see?**

Each thread stores its ThreadLocal values in a map owned by the thread. A thread pool keeps worker threads alive for the lifetime of the application, so values set by a task stay referenced by that worker's ThreadLocalMap until the task calls remove(). The thread itself is a GC root, so the values remain reachable even after the task completes. It is harder to see because the retained objects are associated with long-lived worker threads, not with a global static field, so heap dumps show many thread-owned entries rather than one obvious collection.

## Worked example

A request handler caches every request body in a static `Map<Long, byte[]>`:

```java
static final Map<Long, byte[]> BODIES = new HashMap<>();
void handle(long id, byte[] body) {
    BODIES.put(id, body);
}
```

After 500,000 requests, the map has 500,000 entries and none are removed. The GC root is not the HashMap instance; it is the static field `BODIES` on the loaded class. The reference chain is `BODIES -> HashMap -> entry array -> Node -> byte[]`. Because the chain is all strong references, every byte array remains reachable and cannot be collected. The retained bytes grow with traffic until the heap limit is reached and the JVM throws OutOfMemoryError. The fix is to remove the entry after processing or use a bounded cache with eviction.

## Common traps

- Saying Java cannot leak because the garbage collector handles cleanup.
- Calling the static collection itself a GC root: the static field on the loaded class is the root, and the collection is reachable from it.
- Treating every OOM as a sign to increase heap size; unreachable retention will eventually fail again with a larger heap, and Metaspace or native memory may be the real limit.
- Using System.gc() to fix leaks; it does not collect objects that are still strongly reachable.

</details>

---

## 10. Elevator System Design · mcq · Easy

*lld · gate confidence 0.85*

**Question**

In a low-level design for an elevator car, which state set explicitly separates the car's direction of travel from whether the door is open, using mutually exclusive states?

**Options**

- Idle, MovingUp, MovingDown, DoorOpen
- Idle, Moving, Stopped, DoorOpen
- Up, Down, Waiting, Boarding, Unloading
- Moving, Stopped, Off, Maintenance

**Reference answer**

Idle, MovingUp, MovingDown, DoorOpen

**Graded on**

- Idle, MovingUp, and MovingDown are mutually exclusive motion states.
- DoorOpen is separate from motion states, so a car cannot be moving and have the door open at the same time.
- The decomposition includes idle so the car can wait when no pending requests exist.
- Direction is encoded in the moving states, allowing hall requests to be matched by direction.

<details><summary>The lesson this came from</summary>

Elevator system design models floors, hall and car requests, elevator cars with direction and state, and a controller that assigns and orders floor visits. Each car is a finite state machine (idle, moving up, moving down, door open), and a scheduler decides the next floor from pending requests. The design separates input handling from movement policy so scheduling can be swapped independently.

## Why interviewers ask this

This question tests object modeling, state machines, concurrency, and strategy selection under constraints. Interviewers watch whether the candidate separates request ingestion from car movement, avoids a god controller, and can justify a scheduling policy instead of just naming one.

## The core idea

Treat each elevator car as an independent state machine; state changes must be explicit and atomic. Model a request as an immutable value: hall requests carry source floor and direction, car requests carry destination floor. Keep a Scheduler interface so FCFS, SCAN, LOOK, or SSTF can be selected without changing the controller. For a single car, LOOK usually dominates plain SCAN because it reverses at the last pending request instead of always traveling to terminal floors. For multiple elevators, separate assignment—which car should serve a new hall request—from each car's own movement policy; assignment minimizes estimated waiting time or distance, movement follows LOOK per car.

## Key points

- A car's states are mutually exclusive; a safe implementation guards transitions so a car cannot be moving and door-open at the same time.
- Hall requests carry direction because a passenger can only board a car going that way; car requests carry only destination.
- LOOK reverses at the farthest pending request in the current direction, while SCAN always travels to the physical end floors before reversing.
- In single-elevator systems LOOK generally gives lower empty travel than SCAN; FCFS is simple but can cause severe zig-zag movement.
- Multiple-elevator dispatch is a separate assignment layer that can use estimated wait time or distance, while each selected car still runs its own movement policy.

## Your 60-second answer

I’d model the system with floors, requests, elevator cars, and a controller. Each car is a finite state machine: idle, moving up, moving down, and door open. Requests come from hall buttons with a floor and direction, or from car buttons with just a destination. I’d define a scheduler interface and use LOOK for a single elevator: the car keeps moving in one direction until there are no pending requests ahead, then reverses. That avoids unnecessary trips to terminal floors like SCAN. For multiple elevators, I’d separate assignment from movement: a dispatcher assigns each new hall request to the car with the lowest estimated wait or travel cost, then that car runs LOOK locally. The main trade-off is between simple predictable FCFS and better average wait time with direction-aware scheduling.

## If they dig deeper

**What are the main classes and interfaces you would create?**

I would create ElevatorCar, Floor, Request, Direction, ElevatorState, Door, Button, Scheduler, and Dispatcher/Controller. Scheduler is an interface with concrete FCFS, SCAN, LOOK, and possibly SSTF implementations so policies can be swapped without touching the controller.

**How do you model the elevator car's state transitions?**

The car has states Idle, MovingUp, MovingDown, and DoorOpen. On arrival at a scheduled floor, it transitions from moving to door-open only after stopping; a timer or sensor triggers closing, then the scheduler picks the next direction from pending requests. Invalid transitions, such as opening while moving, are rejected.

**Which scheduling algorithm would you use and why?**

I would default to LOOK for a single elevator. It serves requests in the current direction up to the farthest pending request and then reverses, avoiding empty travel to terminal floors that plain SCAN incurs. FCFS is simpler but can bounce between distant floors and gives poor wait times.

**How do you handle concurrent requests so floor presses are not lost?**

Use a thread-safe request queue or synchronized per-elevator command list. Producers enqueue immutable requests and notify the dispatcher; the car thread processes its own state transitions. Per-car synchronization is enough because each car moves independently, while a shared pending collection must be safe for cross-car assignment.

**How would the design change for destination dispatch, where passengers enter their destination at the hall?**

The hall request becomes floor-to-destination instead of floor-plus-direction, and the dispatcher assigns a car before the passenger enters. This lets the system group passengers by destination or zone and reduce stops, but it removes the ability for a passenger to choose any car and requires reliable assignment feedback at the hall panel.

## Worked example

Consider one elevator at floor 2 moving up, with an up hall request at 6 and a car destination at 9. LOOK builds an upward target list [6, 9]. It stops at 6, opens the door, then continues to 9. While the car is between 6 and 9, a down hall request arrives at floor 4. The request is stored but not inserted into the current upward pass because it is below the car and opposite direction. After serving 9, the car finds no pending requests above 9, reverses direction, and visits 4 on the way down. If the scheduler were SCAN, it would first go to the top floor before reversing, adding empty travel unless the building top coincides with 9.

## Common traps

- Treating the door as a boolean isOpen; a real transition needs opening/open/closing states and a timer or sensor guard, otherwise safety interlocks cannot be modeled.
- Making one controller that both assigns and moves elevators; without a separate policy interface, changing from FCFS to LOOK touches car logic.
- Overlooking direction in hall requests; treating a hall request as just a floor makes it impossible to decide whether the car should stop when moving the opposite way.
- Saying LOOK and SCAN are the same; SCAN travels to terminal floors, which is only beneficial if ends are likely request points or you need very predictable coverage.

</details>

---

## 11. Factory Method Pattern · flash · Easy

*lld · gate confidence 0.85*

**Question**

What is the defining structure of the Factory Method pattern?

**Reference answer**

An abstract creator class declares a factory method whose return type is a product interface or abstract class, and concrete creator subclasses override it to return different concrete products.

**Graded on**

- abstract creator class
- factory method returns product abstraction
- concrete creators override the method

<details><summary>The lesson this came from</summary>

Factory Method is a creational design pattern. It defines a method in a creator class that returns a product abstraction, and concrete creator subclasses override that method to instantiate and return a specific concrete product. The client depends only on the creator and product abstractions, so new product types can be added by introducing a new creator subclass without changing existing client code. In the classic GoF formulation, this is a 'virtual constructor' that defers instantiation to subclasses.

## Why interviewers ask this

Interviewers use this to test whether you understand how to decouple object creation from use, keep code open for extension without modifying existing classes, and invert dependencies so high-level modules rely on abstractions rather than concrete types. A strong answer should distinguish Factory Method from Simple Factory and Abstract Factory and describe a concrete extension scenario.

## The core idea

The core mechanism is a method whose return type is an abstraction (interface or abstract class) but whose implementation is supplied by subclasses. Because the creator class calls its own factory method rather than a constructor, the selection of concrete product moves from compile-time code to runtime polymorphism. This gives client code a stable interface while allowing new product classes to be introduced alongside new creator subclasses. The trade-off is extra classes and indirection: each product family or variant typically requires its own creator subclass. Use it when the class cannot anticipate the class of objects it must create or when subclasses should specify objects.

## Key points

- The defining structure is an abstract creator class with a factory method whose declared return type is a product interface or abstract class; concrete creators override it to return different concrete products.
- It is not the same as a Simple Factory, which centralizes creation in one parameterized class without inheritance and is not one of the GoF patterns.
- Factory Method supports the Open/Closed Principle because new product types can be introduced through new creator subclasses rather than by changing existing code.
- Clients depend only on the abstract creator and product types, applying the Dependency Inversion Principle.
- Android's ViewModelProvider.Factory decouples custom ViewModel construction by providing a factory interface, but its one-method signature with a Class parameter is a factory abstraction rather than the classic GoF creator hierarchy.

## Your 60-second answer

Factory Method is a creational pattern where a creator class defines a method that returns an interface, and subclasses override that method to decide which concrete class to instantiate. This removes direct new calls from the code that uses the object, so you can add a new product type by adding a new creator subclass without touching existing client logic. It's often used when a class cannot predict which of several related classes it must create, such as a document framework that lets subclasses create different document types. The main trade-off is complexity: every new product usually requires a new creator subclass, which can bloat the class hierarchy. It's also distinct from a Simple Factory, which centralizes creation in one class without inheritance, and from Abstract Factory, which creates families of related objects.

## If they dig deeper

**What core problem does the Factory Method pattern solve?**

It removes the need for client code to name concrete product classes, so the client depends only on a product abstraction. New product variants can then be added by creating a new creator subclass without modifying existing client code, which preserves the Open/Closed Principle.

**How is Factory Method different from Simple Factory and Abstract Factory?**

Simple Factory centralizes creation in one parameterized class and is not a GoF pattern, whereas Factory Method relies on inheritance so subclasses override a creation method. Abstract Factory uses composition: an abstract factory interface returns families of related products, implemented by concrete factories.

**When would you use Factory Method instead of a plain constructor?**

Use it when the exact class to instantiate should be decided by a subclass, when creation requires variant-specific logic, or when the creator wants to run extra steps around creation such as caching, validation, or reuse without changing the client.

**How does Factory Method compare to Dependency Injection for managing dependencies?**

Factory Method lets a class obtain its product by calling its own overridable method, keeping the creation knowledge inside the class hierarchy. Dependency Injection passes the dependency in from outside, which makes dependencies explicit, improves testability, and is often preferred when the caller or a container should select the implementation.

**What maintenance problems can appear with parallel creator and product hierarchies, and how can you reduce them?**

Parallel hierarchies can explode in number of classes and couple the creator and product families tightly, so changing one often requires updating many subclasses. You can reduce this by having fewer creators with parameterized creation, using configuration or registration instead of subclassing, or accepting the parallel hierarchy only where product types genuinely vary by creator type.

## Worked example

Consider a document application. The abstract class Application declares protected abstract Document createDocument(). Its concrete newDocument() method calls createDocument(), then calls open() on the returned Document and adds it to a list of open documents. TextApplication implements createDocument() to return a TextDocument; SpreadsheetApplication returns a SpreadsheetDocument. Client code calls application.newDocument() and never refers to TextDocument or SpreadsheetDocument directly. Later, adding a PresentationApplication that returns PresentationDocument requires no edits to newDocument or existing subclasses. The choice of concrete product is deferred to the subclass and resolved at runtime.

## Common traps

- Calling any class that returns an object a Factory Method, even when there is no creator subclass and no overridden method — that is typically a Simple Factory or a helper method, not the GoF pattern.
- Confusing Factory Method with Abstract Factory because both deal with object creation; Abstract Factory creates families of related products through composition, not by having subclasses override a single creation method.
- Overusing the pattern by making a creator subclass for every product variant when a constructor parameter or registration would suffice, causing class explosion.
- Declaring the factory method static, which prevents dynamic dispatch and therefore removes the polymorphism that is the pattern's core mechanism in languages like Java and C#.

</details>

---

## 12. DDL/DML/DCL/TCL · flash · Easy

*sql · gate confidence 0.85*

**Question**

What do the four SQL command families DDL, DML, DCL, and TCL classify?

**Reference answer**

They classify SQL statements by what they affect: DDL acts on schema, DML on row data, DCL on privileges, and TCL on transaction scope.

**Graded on**

- Classification is by effect, not syntax
- DDL changes schema objects
- DML changes row data
- DCL controls access and TCL controls transaction boundaries

<details><summary>The lesson this came from</summary>

DDL, DML, DCL, and TCL are four SQL command families classified by what they affect. DDL changes schema objects through CREATE, ALTER, DROP, and TRUNCATE. DML reads and modifies rows through SELECT, INSERT, UPDATE, DELETE, and MERGE where the engine supports it; SELECT is sometimes separated out as DQL. DCL manages access through GRANT and REVOKE, plus DENY in SQL Server and Sybase. TCL groups work into atomic units through BEGIN/START TRANSACTION, COMMIT, ROLLBACK, and savepoints.

## Why interviewers ask this

The interviewer is testing whether you can classify SQL by effect, understand the privilege boundary between changing schema and changing data, and reason about transaction boundaries. Strong candidates go beyond listing commands and explain implicit commit differences and partial rollback.

## The core idea

The four categories classify SQL by effect: DDL acts on schema, DML acts on row data, DCL acts on privileges, and TCL acts on transaction scope. The interview-relevant edge cases are engine-specific commit behavior and partial undo. MySQL and Oracle implicitly commit DDL, ending any open transaction; PostgreSQL lets ordinary DDL such as CREATE TABLE be rolled back, but CREATE INDEX CONCURRENTLY cannot run inside a transaction block. SQL Server often allows DDL inside explicit transactions. A savepoint is a named rollback target inside a transaction, not a new transaction.

## Key points

- DDL changes schema objects with CREATE, ALTER, DROP, and TRUNCATE; DML changes rows with INSERT, UPDATE, DELETE, MERGE, and usually SELECT.
- DCL controls permissions with GRANT and REVOKE; DENY is SQL Server/Sybase-specific rather than universal SQL.
- TCL delimits atomic units with BEGIN TRANSACTION/START TRANSACTION, COMMIT, ROLLBACK, and savepoints.
- DDL commit behavior is engine-specific: MySQL and Oracle implicitly commit DDL, while PostgreSQL allows ordinary DDL rollback and SQL Server often allows DDL in explicit transactions.
- In SQL Server, SAVE TRANSACTION creates a named savepoint; ROLLBACK TRANSACTION savepoint_name undoes only later work and leaves the outer transaction open.

## Your 60-second answer

SQL statements are usually divided into four families by what they act on. DDL defines or changes schema objects: CREATE, ALTER, DROP, and TRUNCATE. DML reads and changes rows: SELECT, INSERT, UPDATE, DELETE, and MERGE where supported. DCL controls access: GRANT and REVOKE, plus DENY in SQL Server. TCL controls transaction boundaries: BEGIN or START TRANSACTION, COMMIT, ROLLBACK, and savepoints. The important operational difference is durability and implicit commit behavior. MySQL and Oracle implicitly commit DDL, while PostgreSQL lets ordinary DDL participate in a transaction and roll back, though CREATE INDEX CONCURRENTLY cannot run inside one. SQL Server often allows DDL in explicit transactions. When I need partial undo, I mark a savepoint and roll back to it without discarding the whole transaction.

## If they dig deeper

**What is the practical difference between TRUNCATE and DELETE?**

TRUNCATE is DDL that removes all rows; DELETE is DML that removes rows one at a time, supports WHERE, and fires delete triggers. In SQL Server, TRUNCATE deallocates data pages and resets IDENTITY; in PostgreSQL, TRUNCATE is transactional and does not restart a sequence unless RESTART IDENTITY is specified.

**Why do some databases commit DDL implicitly while PostgreSQL does not?**

It is an implementation choice about whether catalog changes are made with the same transaction atomicity as row changes. MySQL and Oracle issue implicit commits before and after DDL, so an existing open transaction is ended. PostgreSQL records catalog changes transactionally, so ordinary DDL can be rolled back; exceptions such as CREATE INDEX CONCURRENTLY are blocked inside transaction blocks instead of breaking atomicity.

**How do savepoints change rollback behavior?**

A savepoint creates a named mark inside an open transaction. ROLLBACK to that savepoint undoes only the statements after the mark; earlier work remains pending and locks are not released. The transaction remains open, so a final COMMIT or full ROLLBACK is still required.

**What privileges separate DDL from DML, and why does that matter?**

DML needs table-level, and sometimes column-level, SELECT/INSERT/UPDATE/DELETE privileges on existing objects. DDL needs broader object-creation rights, such as CREATE on a schema in PostgreSQL, CREATE on a database in MySQL, or CREATE TABLE plus ALTER on a schema in SQL Server. The separation lets a reporting or application user modify rows without being able to change the schema.

**How does TCL interact with isolation levels when a transaction spans several reads and writes?**

TCL defines the atomic unit, while the isolation level determines what uncommitted data and changes are visible inside it. PostgreSQL and SQL Server default to READ COMMITTED; MySQL InnoDB defaults to REPEATABLE READ. In SQL Server, SERIALIZABLE adds key-range locking to prevent phantoms; in PostgreSQL, SERIALIZABLE uses predicate locking and aborts unsafe transactions. The chosen level does not remove the need for COMMIT: only commit makes the writes durable.

## Worked example

A PostgreSQL example shows both DDL rollback and the concurrent-index exception. Start with BEGIN; CREATE TABLE order_archive (LIKE orders); INSERT INTO order_archive SELECT * FROM orders WHERE shipped_at < now() - interval '90 days'; ROLLBACK;. Because PostgreSQL records DDL in the transaction catalog, the table creation and the inserted rows are both undone after ROLLBACK, so order_archive does not exist. If the same transaction instead ran CREATE INDEX CONCURRENTLY idx_orders_customer ON orders(customer_id); PostgreSQL would reject it immediately with ERROR: CREATE INDEX CONCURRENTLY cannot run inside a transaction block. The workaround is to run the concurrent index build outside any explicit transaction.

## Common traps

- Claiming all DDL implicitly commits: PostgreSQL allows ordinary DDL rollback, and SQL Server often permits DDL inside explicit transactions.
- Treating TRUNCATE as DML: it is DDL, removes all rows, and has engine-specific behavior around identity counters and triggers.
- Assuming rolling back to a savepoint ends the transaction: the outer transaction remains open and still needs COMMIT or ROLLBACK.
- Using DENY as a universal DCL command: DENY is SQL Server/Sybase-specific; standard and most engines use GRANT and REVOKE.

</details>

---

## 13. ROW_NUMBER/RANK/DENSE_RANK · typed · Medium

*sql · gate confidence 0.85*

**Question**

How can you express RANK() and DENSE_RANK() in terms of preceding rows or distinct values?

**Reference answer**

RANK() equals 1 plus the number of rows in the partition whose ORDER BY value is strictly less than the current row's value. DENSE_RANK() equals 1 plus the number of distinct ORDER BY values that are strictly less than the current row's value.

**Graded on**

- RANK = 1 + count of rows with strictly smaller ORDER BY value
- DENSE_RANK = 1 + count of distinct smaller ORDER BY values
- ties share the same count of preceding rows and distinct values

<details><summary>The lesson this came from</summary>

ROW_NUMBER(), RANK(), and DENSE_RANK() are SQL window functions that assign an integer to each row within a window defined by OVER. They differ only in how they treat rows whose ORDER BY keys are equal. ROW_NUMBER() always gives a unique sequential number, so tied rows receive arbitrary distinct numbers. RANK() gives tied rows the same value and leaves gaps: the next rank equals the current rank plus the number of tied rows. DENSE_RANK() also gives tied rows the same value, but the next rank is always the previous rank plus 1. PARTITION BY is optional and restarts numbering per partition; ORDER BY normally determines the ranking order, but engine behavior varies when it is omitted.

## Why interviewers ask this

Interviewers use these functions to test whether you understand window semantics beyond basic aggregates: partition scope, ordering, and tie handling. The decision among the three maps directly to requirements like one row per group, top N including ties with gaps, or top N distinct values with no gaps. A precise answer shows you know both the output shape and when nondeterminism appears.

## The core idea

All three ranking functions produce a number for each row in a window; the only real distinction is what happens when multiple rows tie on the ORDER BY expression. ROW_NUMBER simply enumerates rows, so every value is unique and tie order is arbitrary. RANK counts rows that are strictly ahead: a rank of r means r-1 rows precede this one, which creates gaps after groups of ties. DENSE_RANK counts distinct values ahead, so the next value after a tie is always one greater than the tie's rank. If PARTITION BY is present, each partition is ranked independently as if it were the whole table. Without ORDER BY, the functions either require an ORDER BY on some engines or rank all rows as a single peer group on others, so meaningful ranking always needs an explicit order.

## Key points

- ROW_NUMBER() returns a unique sequential integer for every row in its partition; tied rows get arbitrary distinct numbers unless extra ORDER BY columns break the tie.
- RANK() assigns equal values to ties and skips: after two rows tied at rank 2, the next row receives rank 4.
- DENSE_RANK() assigns equal values to ties but does not skip: after two rows tied at rank 2, the next row receives rank 3.
- PARTITION BY restarts numbering at 1 for each partition; without it the entire result set is one partition.
- ORDER BY is required or effectively required for meaningful ranking; PostgreSQL, MySQL, and SQLite allow ROW_NUMBER() OVER () as an arbitrary sequence and RANK/DENSE_RANK then return 1 for every row, while SQL Server requires ORDER BY.

## Your 60-second answer

ROW_NUMBER assigns a distinct sequential number to every row in the window; tied rows get arbitrary different numbers, so there are no gaps. RANK assigns the same rank to tied rows and then skips ahead: if two rows are tied at rank 2, the next row is rank 4. DENSE_RANK also gives tied rows the same rank, but it does not skip: after two rank-2 rows, the next row is rank 3. All three accept an optional PARTITION BY, which restarts numbering at 1 for each partition. Use ROW_NUMBER when you need exactly one row per group; use DENSE_RANK when you want top-N results with ties counted without gaps; use RANK when the gap itself is meaningful, but know that rank filters can skip values because rank counts rows, not distinct values.

## If they dig deeper

**If three rows share the same salary, what ranks do RANK and DENSE_RANK assign to the next row?**

If the tied rows are assigned rank r, RANK gives the next row r+3, because rank equals one plus the number of preceding rows. DENSE_RANK gives the next row r+1, because it counts preceding distinct values, not rows. ROW_NUMBER still assigns three distinct numbers, so its next row is r+3 if numbering was contiguous.

**Which function would you use to return exactly one highest-paid employee per department?**

Use ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) and filter for row number 1. This returns exactly one row per department even when several employees tie for the top salary; the tie is broken arbitrarily unless you add a unique column to the ORDER BY. RANK or DENSE_RANK would return all tied first rows.

**When would RANK be preferable to DENSE_RANK?**

Use RANK when the gap should encode how many rows are strictly ahead. For example, if two people tie for first place, the next person is third, not second. DENSE_RANK is better for distinct-value rankings, such as top 3 salary levels, where you want no skipped positions among distinct values.

**Can you express RANK and DENSE_RANK as counts of preceding rows or values?**

Yes. RANK() = 1 + number of rows in the partition whose ORDER BY value is strictly less than the current row's value. DENSE_RANK() = 1 + number of distinct ORDER BY values that are strictly less than the current row's value. Ties have the same number of strictly preceding rows and values, so they receive the same rank.

**What happens if the OVER clause has no ORDER BY, and is that allowed in all engines?**

In PostgreSQL, MySQL, and SQLite, ROW_NUMBER() OVER () returns an arbitrary sequential number for the whole partition, while RANK() and DENSE_RANK() return 1 for every row because all rows form one peer group. SQL Server requires ORDER BY for these ranking functions. Without an ORDER BY, the ranking is not meaningful and the tie-breaking order is nondeterministic.

## Worked example

For salaries 90000, 85000, 85000, 75000 ordered descending: ROW_NUMBER gives 1,2,3,4 because it simply enumerates rows, and the two 85000 rows receive different numbers in an engine-dependent order. RANK gives 1,2,2,4: both 85000 rows tie at rank 2, and the next rank is 4 because rank skips one place for the extra tied row. DENSE_RANK gives 1,2,2,3: the two 85000 rows still share rank 2, but the next distinct salary gets rank 3 because dense_rank advances by one distinct value rather than row count. If you add PARTITION BY department, the same sequence restarts at 1 within each department.

## Common traps

- Assuming ROW_NUMBER breaks ties deterministically; without a unique column in ORDER BY, tied rows can be ordered arbitrarily and may change across runs or engines.
- Including PARTITION BY when a global rank is desired, which silently restarts numbering inside each group and produces many rows with rank 1 instead of one top row.
- Using RANK() where the requirement is 'top 3 salary levels' and filtering rank <= 3: two rows tied at rank 2 make the next distinct salary rank 4, so the third salary level is excluded; DENSE_RANK avoids this.
- Stating that RANK and DENSE_RANK require PARTITION BY or that ORDER BY is never optional across all engines; actual behavior varies, and without ORDER BY ranking collapses to a single peer group where supported.

</details>

---

## 14. Idempotency · flash · Easy

*system_design · gate confidence 0.85*

**Question**

How long should idempotency keys be retained?

**Reference answer**

Longer than the client's maximum retry window, including timeouts and backoff, but they can be deleted after that business-defined retention period.

**Graded on**

- retain beyond max retry window
- not forever
- deleting too early recreates duplicate side effects

<details><summary>The lesson this came from</summary>

Idempotency in API design is the property that multiple identical requests have the same effect as a single request. For naturally idempotent operations such as HTTP PUT and DELETE this is part of the method semantics. For non-idempotent POSTs such as payment or order creation, clients send a unique idempotency key, often a UUID in an Idempotency-Key header; the server stores the key with its processing state and response, then returns the stored response on duplicate requests instead of re-executing the work. Safe retries require persisting the key before any external side effect, but external calls cannot be part of that same database transaction.

## Why interviewers ask this

Interviewers use idempotency questions in payment, order, and messaging designs to test whether the candidate understands retries in distributed systems. The real risk is duplicate side effects: a timed-out request retried by a client or load balancer must not charge a card twice or create two accounts. They are checking whether you know that client retries alone are not enough and that the server needs an explicit key or deduplication mechanism.

## The core idea

Retries are unavoidable in any network; the system must make repetition harmless. The mechanism is to assign the client's intent a unique key before any side effect runs, store that key with the request state and final response, and return the stored response when the key repeats. Local database consistency and external side effects have different boundaries: you cannot hold a transaction open across a payment gateway call, so you persist a processing state first, commit, call the external system, then record success or failure in a later transaction. This ordering avoids both double charges and long-lived transactions. For at-least-once delivery systems, the same principle appears as deduplicating messages by an event or message ID.

## Key points

- HTTP GET, PUT, and DELETE are idempotent by method semantics; POST is not automatically idempotent but can be made idempotent for a specific operation with an idempotency key.
- An idempotency key is a client-generated unique value, usually a UUID, sent in an Idempotency-Key header; Stripe and PayPal recommend UUIDs for this purpose.
- The server must persist the key and enough state/response before performing the side effect, and duplicates return the stored response without re-executing the work.
- External side effects such as charging a card cannot participate in a local database transaction; commit a processing record first, call the external gateway, then update the final status in a separate transaction.
- At-least-once message delivery requires handler idempotency by deduplicating message IDs or making the operation itself idempotent.

## Your 60-second answer

Idempotency means a client can safely retry the same call and the server ends up in the same state and returns the same result as if the call ran once. For non-idempotent operations like payment or order creation, the standard approach is an idempotency key. The client generates a UUID and sends it in an Idempotency-Key header. The server stores that key before doing the work. If it sees the same key again, it returns the stored response instead of executing the operation a second time. The subtle part is how you order the work when there is an external side effect. You cannot hold a database transaction open while calling a payment gateway; that ties up connections and risks timeouts. Instead, insert a row with status processing, commit, call the gateway, and then update the row to success or failure in a separate transaction. That prevents double charges while keeping the database available.

## If they dig deeper

**Which HTTP methods are idempotent and how does that differ from safety?**

GET, PUT, and DELETE are idempotent: repeated identical requests produce the same result. GET and HEAD are also safe, meaning no side effects, while PUT and DELETE are idempotent but not safe because they change state. POST is not idempotent by default because it usually creates a new resource each time.

**How would you implement idempotent payment retries end to end?**

The client generates a UUID and sends it as Idempotency-Key. The server uses a unique constraint on the key in a dedicated table and first inserts a row with status processing, then commits. It calls the payment gateway; on success it stores charge_id and status success. A duplicate request with the same key sees the existing row and returns the stored response without calling the gateway again.

**What happens if two requests with the same key arrive at the same time?**

The server inserts both in a table with a unique constraint on the key; one insert wins, the other violates the constraint. The losing request then reads the existing row. If the row is still processing, it can return a 409 or processing status or poll; if it is success or failure, it returns the stored result. The unique constraint is the atomic guard.

**When should idempotency keys expire?**

They should live longer than the client's maximum retry window, including timeout and backoff, but not forever. After the business-defined retention window, old keys can be deleted to reclaim storage, because retries beyond that window are treated as new intent. Expiring too early recreates the duplicate side effect.

**How do you handle idempotency in an at-least-once message consumer that can crash midway?**

Store the event ID in the database with a unique constraint, and process the event and record its ID in a transaction where all local effects are transactional. For external side effects, use an outbox pattern: write the event ID and outgoing message in one transaction, then send from the outbox; a redelivered event will be ignored because its ID already exists.

## Worked example

A client sends POST /v1/payments with header Idempotency-Key: 0f8fad5b and an amount of $49.00. The server begins a transaction, inserts a row in idempotency_keys with key 0f8fad5b, status processing, and request payload, and commits that transaction before any external action. It then calls the payment gateway. Suppose the gateway returns success with charge_id ch_123; the server opens a second transaction, updates the row to status success and stores the response with charge_id ch_123, and commits. The client's connection times out before it receives the 200, so it retries with the same key. The server finds the existing row in status success and returns the stored response. No second gateway call is made, so the card is charged once.

## Common traps

- Wrapping the external payment gateway call in the same database transaction as the idempotency-key insert and final update, which holds locks and connections open across a network call.
- Assuming the client will not retry if it does not receive a response; timeouts happen after the server has committed the side effect, so server-side deduplication is required.
- Using business fields such as email or order amount as the idempotency key; that conflates intent with payload and can incorrectly reject legitimate independent requests.
- Returning success from the gateway call without persisting the response; if the client retries after a crash, the server cannot know whether the prior call succeeded and may charge again.

</details>

---

## 15. Database sharding · typed · Medium

*system_design · gate confidence 0.85*

**Question**

How do you choose a sharding key?

**Reference answer**

Choose a high-cardinality key that spreads writes evenly and matches the dominant query pattern so most reads and writes hit exactly one shard; avoid low-cardinality keys such as country or status.

**Graded on**

- high cardinality
- matches dominant access pattern
- most operations single-shard
- avoid low-cardinality keys

<details><summary>The lesson this came from</summary>

Sharding is horizontal partitioning: the rows of a logical database are split into disjoint subsets called shards, and each shard runs on its own database server or cluster. A sharding key determines which row goes to which shard; all shards together contain the entire dataset. It scales writes and storage by adding machines, unlike vertical scaling which adds CPU or RAM to one box. Each shard is independent, so joins and transactions that span shards become distributed operations.

## Why interviewers ask this

Interviewers use sharding questions to see whether you can move from a single database to many without hand-waving. They test choosing a sharding key that matches access patterns, avoiding hot shards, and handling cross-shard queries. In system design prompts like a job scheduler or A/B test backend, scaling the data layer is where candidates either get concrete or stay vague.

## The core idea

Sharding is a late-stage scaling tool: first exhaust indexing, caching, read replicas, and vertical scaling, then shard when one node cannot hold the write load or data volume. The sharding key decides almost everything: a good key spreads writes evenly and lets most queries hit exactly one shard; a bad key creates a hot shard or forces scatter-gather queries. Hash-based sharding distributes uniformly but destroys range locality; range-based sharding preserves locality but risks hotspots; directory-based sharding lets you map keys manually. Cross-shard joins, transactions, and constraints are hard, so schemas are designed so most access is single-shard. Adding shards later is expensive, so resharding must be planned from day one.

## Key points

- Sharding partitions rows across separate database servers, while replication copies the same rows to multiple servers; they are often combined so each shard has replicas.
- Range-based sharding keeps ordered data together and allows efficient range scans on the sharding key, but risks hot shards when ranges are unbalanced.
- Hash-based sharding spreads keys uniformly and gives O(1) point lookups, but range queries across the key must fan out to all shards.
- Directory-based sharding routes through a lookup table, which allows flexible rebalancing at the cost of an extra lookup and a metadata store to maintain.
- Cross-shard joins and distributed transactions are expensive, so schemas are typically denormalized or partitioned so most access is single-shard.

## Your 60-second answer

Sharding means splitting one logical database into multiple physical database servers, where each server holds a disjoint subset of the rows. A row is placed on a shard based on a sharding key—for example a user ID—so a query for a single user hits exactly one shard. You shard because one server eventually cannot hold the data or absorb the write throughput, and adding more servers is the only way to keep scaling. The cost is that anything spanning shards gets harder: joins, transactions, and aggregate queries either must be avoided in the schema or executed as scatter-gather operations across shards. The key decision is choosing a sharding key that spreads writes evenly and matches the most frequent access pattern; a bad key creates a hot shard and brings back the exact bottleneck you were trying to remove.

## If they dig deeper

**What is the difference between sharding and replication?**

Replication copies the same data to multiple nodes, usually for read scale and failover; writes still go to a primary. Sharding partitions different rows across nodes so each node stores only part of the data. In practice they are combined: each shard often has one or more replicas for availability.

**How do you choose a sharding key?**

Pick a key with high cardinality so data spreads evenly, and one that matches the dominant query pattern so most reads and writes hit a single shard. For multi-tenant apps, tenant ID is common; for user-centric apps, user ID. Avoid low-cardinality keys like country or status, which cause uneven shards.

**What are range-based, hash-based, and directory-based sharding, and when would you use each?**

Range-based uses contiguous key intervals, which is good when you need ordered scans or time-range queries but can create hotspots if writes concentrate at one end. Hash-based applies a hash function and modulo to get a shard, which spreads data evenly but loses range locality, so range queries fan out to all shards. Directory-based looks up the key-to-shard mapping in a separate metadata service, giving you flexibility to move data manually at the cost of an extra hop and a lookup system to maintain.

**How do you handle a query that needs data from multiple shards?**

First, design the schema to avoid it: denormalize related data into the same shard, or colocate by a shared key. If unavoidable, do scatter-gather: send the query to all relevant shards in parallel and merge the results in the application or proxy. Cross-shard joins and distributed transactions are generally avoided because they require protocols like two-phase commit or sagas and can severely hurt latency.

**How do you rebalance or add a shard without downtime?**

A common approach is to use consistent hashing with many virtual shards per physical node, so adding a node moves only a fraction of keys instead of rehashing everyone. For range or directory sharding, you can split a range or update the directory while copying data in the background, then switch reads and writes once the new shard is in sync. Live migration generally requires dual reads/writes or checking replication lag, and the hardest part is preserving consistency during the cutover.

## Worked example

Take a users table with sharding key user_id and four shards. With hash-based sharding, the router computes user_id % 4: user 1001 goes to shard 1, 1002 to shard 2, and so on. A lookup by user_id is a single point query: compute the hash, connect to one shard, done. A query for all users who signed up in January has no user_id predicate, so the query layer must run it on all four shards and merge results. If the table instead used range-based sharding on created_at, the January query could hit only the shard containing that date range, but every new signup would hammer the newest range. This contrast is why key choice follows access patterns.

## Common traps

- Sharding too early, before indexing, caching, read replicas, or vertical scaling are exhausted, adds distributed-systems complexity without need.
- Choosing a low-cardinality sharding key, such as status or country, so a few shards receive most writes and become hotspots.
- Assuming sharding alone provides high availability; a shard is still a single point of failure unless each shard has replicas.
- Designing queries that join across shards as if the database were still one node, then discovering at scale that latency and consistency are unmanageable.

</details>

---

## 16. Supervised Fine-Tuning of LLM · mcq · Easy

*ai · gate confidence 0.9*

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

Supervised fine-tuning (SFT) is a post-training stage in which a pre-trained large language model is trained further on a labeled dataset of prompt-response demonstrations. The objective is the usual causal language-modeling loss, typically computed only on the response tokens so the model learns to produce the target answer for each prompt. It changes behavior such as instruction following, formatting, tone, tool-calling, or domain-specific procedures, rather than serving primarily as a mechanism for adding new facts.

## Why interviewers ask this

Interviewers are testing whether you know when to apply SFT instead of prompting, RAG, or preference optimization, and whether you can run it under real data and compute constraints. They look for practical dataset construction, hyperparameter choices, and an understanding of failure modes like catastrophic forgetting.

## The core idea

Pre-training gives a model broad next-token prediction ability, not reliable instruction-following. SFT converts that ability into a specific output policy by increasing the probability of demonstrated responses for their prompts. Because the model imitates the dataset, the quality, coverage, and consistency of the demonstrations determine the resulting behavior. In many post-training pipelines, SFT comes first to teach basic instruction following and formatting, after which preference methods such as DPO or RLHF can refine ranking. On limited hardware, parameter-efficient fine-tuning with adapters such as LoRA reduces memory and the risk of destroying general abilities.

## Key points

- SFT continues training a pre-trained LLM on prompt-response pairs with a next-token loss, often masking prompt tokens to compute loss only on the response.
- SFT changes behavior, style, and instruction following rather than adding up-to-date facts; dynamic external knowledge is usually better served by RAG.
- Full fine-tuning updates every parameter and is memory-intensive and prone to catastrophic forgetting, while LoRA/QLoRA freeze the base and train small adapters.
- Dataset quality dominates SFT results: demonstrations must be diverse, consistent, and include negative or refusal examples if the model must abstain.
- Core hyperparameters include learning rate, number of epochs, batch size, and for LoRA the rank, alpha, and target modules.

## Your 60-second answer

Supervised fine-tuning is a second training stage where a pre-trained language model is trained on curated prompt-response pairs to change how it behaves. The reason it is needed is that pre-training only gives the model next-token prediction; it does not reliably produce a desired format, tone, or instruction-following policy. I would choose SFT when the target behavior is stable and I can demonstrate it with labeled examples, and when prompting or retrieval cannot enforce it consistently. The main trade-off is cost versus control: full fine-tuning updates all weights and can damage general abilities, while parameter-efficient methods such as LoRA train only adapters, which is cheaper but may leave less room to learn a very different task. Dataset quality matters more than raw size because the model will imitate whatever patterns are in the examples.

## If they dig deeper

**When would you choose supervised fine-tuning over prompt engineering or RAG?**

SFT is the better choice when the desired behavior is stable and can be shown with examples, and prompting alone does not reliably enforce format, tone, tool-calling, or instruction following. RAG is for accessing external or frequently changing facts; SFT is for changing model behavior on a static task. In real systems they often stack: SFT for style and call format, RAG for retrieval.

**How do you create a fine-tuning dataset for a Q&A assistant?**

Collect prompt-response pairs that match the production distribution. Each response must be exactly what you want the model to output, including consistent formatting and refusal behavior. Include paraphrases, edge cases, and negative examples where the model should say it lacks information. Structure records as message lists and mask prompt tokens during training so only response tokens contribute to the loss.

**What hyperparameters do you set for LoRA fine-tuning, and why?**

I choose a low rank, typically 8 to 16, with alpha around twice the rank, and target the attention projection matrices. A small learning rate, often in the range of 1e-5 to 2e-4 for adapters, and only a few epochs help avoid overfitting and instability. I use the largest batch size that fits memory with gradient accumulation and monitor a held-out validation set for early stopping.

**What is catastrophic forgetting in LLM fine-tuning?**

Catastrophic forgetting is the loss of general capabilities that occurs when a model is trained further on a narrow distribution. Full fine-tuning on a small specialized dataset can overwrite weights that supported broad language or reasoning skills. Mitigations include parameter-efficient adapters with a frozen base, mixing general data into the fine-tuning set, low learning rates, and early stopping.

**How do you make a fine-tuned model answer only when there is enough context?**

Add demonstrations where the model declines to answer or asks a clarifying question when the provided context lacks the needed facts. State the grounding rule explicitly in the system prompt and include such cases in evaluation. SFT alone is not a reliable abstention mechanism; pair it with retrieval confidence scores or a separate critique step that checks whether the answer is supported by the evidence.

## Worked example

Suppose a base model is asked: "How do I reset my password?" and it gives a long generic explanation with several follow-up questions. An SFT record for a support assistant would be a message list with a system instruction such as "Answer only using the supplied knowledge base. If the answer is not present, say you do not know", the user prompt, and the desired assistant response: "Go to Settings > Security > Reset password. A link will be sent to your registered email." During training, the causal language-modeling loss is computed only on the assistant response tokens; the system and user tokens are masked. With LoRA on a 7B model using rank 16 and alpha 32, only adapter weights are updated. Over many such pairs, the model learns to produce direct procedural answers and to abstain when the knowledge base lacks the answer.

## Common traps

- Treating SFT as a way to inject up-to-date facts instead of teaching behavior and format.
- Ignoring prompt loss masking, which makes the model train on tokens it should not need to reproduce.
- Assuming full fine-tuning is always best; with small data or limited hardware, LoRA/QLoRA is often more practical.
- Using inconsistent or low-quality demonstrations, then blaming the optimizer when the model imitates those flaws.

</details>

---

## 17. Deadlocks · flash · Easy

*cs · gate confidence 0.9*

**Question**

Name two common recovery actions after a deadlock is detected.

**Reference answer**

Terminate one or more processes and preempt resources, often with rollback to a checkpoint.

**Graded on**

- process termination
- resource preemption
- rollback to checkpoint

<details><summary>The lesson this came from</summary>

A deadlock is a state where two or more processes are permanently blocked because each holds a resource and waits for another resource held by another process in the set. Deadlock requires four conditions to hold simultaneously: mutual exclusion, hold and wait, no preemption, and circular wait. Handling strategies include prevention (breaking a condition statically), avoidance (making dynamic safe-state decisions such as Banker's algorithm), and detection and recovery (allowing deadlocks, detecting cycles, then terminating or preempting).

## Why interviewers ask this

The interviewer is testing whether the candidate understands the Coffman conditions and can reason about real system trade-offs between prevention, avoidance, and detection. It also probes knowledge of classic algorithms like Banker's algorithm and the ability to apply wait-for graph cycle detection.

## The core idea

Deadlock is a permanent blocking among processes that each hold some resources and wait for others. All four Coffman conditions are necessary; eliminating any one prevents deadlock. Avoidance is more dynamic: Banker's algorithm uses each process's declared maximum needs to grant a request only if the resulting state is safe, meaning some sequence of completions exists. Detection allows deadlocks to occur and then breaks them by finding a cycle in a wait-for graph or resource allocation graph. The fundamental trade-off is between restricting concurrency upfront and paying detection and recovery overhead later.

## Key points

- Deadlock requires four Coffman conditions: mutual exclusion, hold and wait, no preemption, and circular wait; eliminating any one prevents deadlock.
- In a resource allocation graph, a cycle guarantees deadlock only when every resource in the cycle has a single instance; with multiple instances, a cycle is necessary but not sufficient.
- Banker's algorithm is a deadlock avoidance method that grants a request only if the resulting state is safe, requiring each process to declare its maximum resource needs in advance.
- Deadlock detection for systems with only single-instance resources reduces to finding a cycle in a wait-for graph; for multiple instances, detection checks whether all processes in the cycle can finish using current requests.
- Recovery options are terminating processes (all or selective victims) and resource preemption, usually combined with rollback to a checkpoint.

## Your 60-second answer

A deadlock occurs when a set of processes each holds a resource and waits for another resource held by a member of the set, so none can make progress. Four conditions must hold simultaneously: mutual exclusion, hold and wait, no preemption, and circular wait. Deadlock can be handled by prevention, which statically guarantees at least one condition never holds, or avoidance, which makes dynamic decisions—Banker's algorithm grants a request only if the resulting state is safe given each process's declared maximum needs. Alternatively, you can allow deadlocks, detect them via a wait-for graph cycle, and recover by terminating processes or preempting resources. The trade-off is that prevention and avoidance restrict concurrency and may require advance knowledge, while detection has runtime overhead and imposes recovery cost; many practical systems combine detection with timeouts.

## If they dig deeper

**What are the four necessary conditions for deadlock to occur?**

Mutual exclusion, hold and wait, no preemption, and circular wait. Each must hold simultaneously; preventing any one of them eliminates the possibility of deadlock.

**What is the difference between deadlock prevention and avoidance?**

Prevention statically guarantees that at least one Coffman condition never holds, often by requiring all resources at once or imposing resource ordering. Avoidance is dynamic: it allows the conditions but checks each request against a safe-state criterion before granting it, as in Banker's algorithm.

**How does the Banker's algorithm decide whether to grant a resource request?**

It provisionally allocates the request, recomputes each process's remaining need, and then tries to find a sequence in which every process can finish with the remaining available resources. If such a safe sequence exists, the request is granted; otherwise it is denied and the system stays in the previous safe state.

**What are the practical limitations of Banker's algorithm in real operating systems?**

It requires each process to declare its maximum resource needs in advance, assumes a fixed number of processes and resource types, and performing a safe-state check on every request is expensive. As a result, general-purpose operating systems rarely use it; databases more often rely on deadlock detection plus victim rollback.

## Worked example

Suppose a system has four units of each of three resource types A, B, C. Initially available = [2,2,2]. Processes: P0 allocated [1,1,1] max [3,3,3]; P1 allocated [1,1,1] max [2,2,2]; P2 allocated [0,0,0] max [2,2,2]. Need = max - allocation: P0 [2,2,2], P1 [1,1,1], P2 [2,2,2]. Current available [2,2,2] is safe because P1 finishes first (need [1,1,1] <= available), releasing [1,1,1] to make [3,3,3], then P2 finishes, then P0. If P0 requests [1,1,1], the Banker's algorithm temporarily grants it: P0 allocation becomes [2,2,2], need [1,1,1], available drops to [1,1,1]. The new state is still safe (P1, then P2, then P0), so the request is granted.

## Common traps

- Confusing avoidance with prevention: prevention breaks a statically defined condition, while avoidance uses a dynamic safe-state test on each request.
- Claiming any cycle in a resource allocation graph means deadlock; with multiple instances of resource types, a cycle can be resolved if an outside process releases a resource.
- Forgetting that Banker's algorithm requires advance knowledge of each process's maximum needs and a fixed number of processes; it is not a general runtime deadlock detector.
- Assuming an unsafe state always means deadlock has occurred; an unsafe state only means a deadlock could occur if subsequent requests are mishandled.

</details>

---

## 18. Matrix / Grid · flash · Easy

*dsa · gate confidence 0.9*

**Question**

For an R x C grid, what are the four-direction neighbors of cell (i,j), and when is a neighbor valid?

**Reference answer**

The four neighbors are (i-1,j), (i+1,j), (i,j-1), and (i,j+1); a neighbor (r,c) is valid when 0 <= r < R and 0 <= c < C.

**Graded on**

- List the four row/column offsets
- Check row bounds
- Check column bounds

<details><summary>The lesson this came from</summary>

In DSA, a matrix/grid problem is a two-dimensional array of cells indexed by row and column, where each cell can hold a value, obstacle, or state. A cell is the graph node and movement directions define adjacency, usually four or eight neighbors. The core work is boundary-checked iteration, BFS/DFS, in-place marking, diagonal index math, or dynamic programming when transitions are acyclic.

## Why interviewers ask this

Interviewers assign medium grid problems such as Diagonal Traverse, Number of Distinct Islands, and Rotating the Box—asked by companies including Meta, Uber, Snap, and TikTok—because they reveal whether you handle boundaries, index transformations, and graph/DP selection under pressure. A strong answer separates the traversal primitive from the higher-level state machine; many candidates crash on edge cells or pick a cyclic DP recurrence.

## The core idea

A grid is a lattice graph: rows and columns give coordinates, and almost every problem starts with generating valid neighbors without going out of bounds. From there, choose the algorithm by the goal: BFS for shortest unweighted paths, DFS for connected components and flood fill, and Dijkstra when cell costs are non-negative but not uniform. DP over the grid is only safe when movement is restricted so the dependency graph becomes a DAG, usually right/down movement. Diagonal, rotation, and reshape problems are index transformations: cells on an anti-diagonal share row+col, while cells on a main diagonal share row-col.

## Key points

- On an R x C grid, 4-direction neighbors of (i,j) are (i-1,j), (i+1,j), (i,j-1), (i,j+1), and each must satisfy 0 <= row < R and 0 <= col < C.
- BFS and DFS both visit a grid in O(R*C) time and O(R*C) worst-case space; recursive DFS risks call-stack overflow on very large grids, so an explicit stack or BFS avoids that risk without reducing asymptotic memory.
- DP with a recurrence based on left/top neighbors is valid only when movement is restricted to right and down; with four-direction movement, cyclic dependencies require BFS for unit costs or Dijkstra for non-negative weighted costs.
- Diagonal traversals rely on constant row+col for anti-diagonals or row-col for main diagonals, so sorting by that key or iterating that sum solves diagonal matrix problems.
- Many grid problems can be solved in-place by marking visited cells with a sentinel value, but this mutates the input and is invalid if the original grid must be preserved.

## Your 60-second answer

For a matrix or grid question I model the grid as a graph: each cell is a node, and its valid neighbors are the in-bounds four-direction moves. I always write a helper that checks boundaries before generating neighbors, because most bugs in these problems come from out-of-bounds access. Then I choose the algorithm by the goal: DFS for connected components and flood fill, BFS when I need shortest path with uniform cell costs, and Dijkstra if entering a cell has varying non-negative cost. If movement is restricted to right and down, the dependency graph is a DAG, so DP in row-major order with a left/top recurrence is enough. The main trade-off is recursive DFS is concise but can overflow the call stack on a large grid, while BFS or an explicit-stack iterative DFS uses heap memory.

## If they dig deeper

**How do you generate valid neighbors for a cell?**

Iterate over the four direction offsets, compute (r+dr, c+dc), and only accept the neighbor when 0 <= r+dr < R and 0 <= c+dc < C. For eight-direction movement add the four diagonal offsets with the same bounds check.

**When would you choose BFS over DFS in a grid?**

Use BFS when the problem asks for shortest path in an unweighted grid or minimum number of steps, because BFS explores in nondecreasing distance. DFS is fine for exploring connected components or flood fill, but it does not guarantee shortest paths and recursion may overflow on large grids.

**Why doesn't the standard left/top DP work when movement is allowed in all four directions?**

Because dp[i][j] can depend on dp[i+1][j] and dp[i][j+1] as well as earlier cells, creating cyclic dependencies in the recurrence. With those cycles you cannot process cells in simple row-major order; you need BFS for uniform costs or Dijkstra for non-negative weighted costs.

**How would you count the number of distinct islands rather than just connected components?**

After finding each island with DFS or BFS, record a canonical form such as the sorted relative coordinates from a fixed starting cell, or a path signature of directions taken during traversal. Insert each canonical form into a hash set; the set size is the number of distinct islands. If rotations or reflections count as identical, normalize the shape before hashing.

**How do you solve a minimum-cost grid path with non-negative cell costs and four-direction movement?**

Run Dijkstra's algorithm from the source. The priority queue stores (current_cost, row, col), and when you pop a cell, relax its four neighbors with cost = current_cost + neighbor_cost. This runs in O(R*C log(R*C)) and avoids the cycles that break DP.

## Worked example

Count paths from (0,0) to (2,2) in a 3x3 grid with movement only right and down, and an obstacle at (1,1). Initialize dp[0][0] = 1. The first row and first column are all 1 until an obstacle appears: dp[0][1] = 1, dp[0][2] = 1, dp[1][0] = 1, dp[2][0] = 1. At the obstacle dp[1][1] = 0. Fill row-major: dp[1][2] = dp[0][2] + dp[1][1] = 1 + 0 = 1. dp[2][1] = dp[1][1] + dp[2][0] = 0 + 1 = 1. Finally dp[2][2] = dp[1][2] + dp[2][1] = 1 + 1 = 2. The two valid paths are RRDD and DDRR, both bypassing the center obstacle.

## Common traps

- Without checking both row and column bounds, a neighbor like (row-1, col) can access a negative index that is valid in Python but points to the wrong row, causing silent logic errors.
- Applying a left/top DP recurrence to a grid that allows up or left moves, which creates cycles and double counts.
- Using recursive DFS on a grid large enough to exceed the call stack, causing a crash instead of switching to an explicit stack or BFS.
- Treating visited cells as optional by reusing cell values as markers, then losing the distinction between original and visited cells when the same value appears elsewhere.

</details>

---

## 19. Intervals · mcq · Hard

*dsa · gate confidence 0.9*

**Question**

For half-open intervals [start, end), what condition should be used to decide whether to merge the next interval with the current merged interval during a sweep?

**Options**

- next_start <= current_end
- next_start < current_end
- next_start < current_start
- next_end > current_start

**Reference answer**

next_start < current_end

**Graded on**

- Half-open intervals require strict inequality
- Touching intervals should not merge
- Overlap condition is a < d and c < b

<details><summary>The lesson this came from</summary>

Interval problems represent ranges as [start, end] and manipulate sets of such ranges. The standard technique sorts intervals by start or end, then performs a linear sweep to merge overlaps, count active intervals, or find gaps. Overlap for closed intervals [a,b] and [c,d] holds when a <= d and c <= b. Harder variants answer queries by sorting queries and intervals together and maintaining a min-heap keyed by interval end or size.

## Why interviewers ask this

Interviewers ask Merge Intervals, Meeting Rooms II, and interval query variants at companies like Meta, Netflix, Grammarly, and MongoDB to test whether you can reduce O(n^2) pairwise overlap checks to an O(n log n) or O((n+m) log(n+m)) sweep. They also probe whether you can handle active-set logic with heaps and boundary edge cases under pressure.

## The core idea

Sorting is what makes overlap checks cheap. Once intervals are sorted by start, any interval that can merge with the current result must be adjacent to it, so one comparison with the last end suffices. For concurrent-overlap problems such as Meeting Rooms II, sort start and end times separately or maintain a min-heap of ends; a start increases the active count, an end decreases it, and the maximum active count is the answer. Query variants add another dimension: sort the queries, then sweep intervals by start and keep a min-heap over candidates by the metric being asked for, discarding intervals whose right end falls before the current query. The time complexity includes all heap operations: with n intervals and m queries, O(n log n + m log m + m log n), which is usually expressed as O((n+m) log(n+m)).

## Key points

- For closed intervals [a,b] and [c,d], overlap iff a <= d and c <= b; correct equality handling decides whether touching intervals merge.
- Merge Intervals sorts by start and merges by comparing each interval's start to the last merged interval's end, giving O(n log n) time and O(n) space for output.
- Meeting Rooms II can use sorted start and end arrays and sweep: increment on start, decrement on end, and track the maximum active count in O(n log n) time and O(n) space.
- Point-query interval problems usually sort queries as well, sweep intervals by start, and use a min-heap keyed by interval size or end to answer each query in O(log n).
- Total query-variant time is O(n log n + m log m + m log n), not just sort-dominated; heap pushes and pops across m queries can be O((n+m) log n).

## Your 60-second answer

When I get an interval problem, I first sort by start time. For Merge Intervals, I sort, then keep a result list; if the next interval starts before or at the current end, I extend the current end, otherwise I push a new interval. For a maximum-overlap problem like Meeting Rooms II, I sort the start times and end times separately and sweep: start means one more room, end means one fewer, and the max active count is the answer. For query-based interval problems, I sort both queries and intervals, sweep by query order, and keep a min-heap keyed by the property the query asks for, discarding intervals whose right end is already behind the current query. Total time is O((n+m) log(n+m)) including heap operations, not O(n log n) alone when there are many queries; the trade-off is O(n+m) extra space.

## If they dig deeper

**For closed intervals, when do two intervals overlap, and when are they merely adjacent?**

Two closed intervals [a,b] and [c,d] overlap iff a <= d and c <= b. They are adjacent in discrete terms if b + 1 == c or d + 1 == a; they are overlapping only when both inequalities are true, so touching endpoints with equality overlap.

**Why does sorting by start make Merge Intervals linear apart from the sort itself?**

After sorting by start, any interval that can overlap the interval currently being merged must start no later than the current interval's end. Because all later intervals have starts at least as large, only the immediate next interval needs to be checked against the current end; once a start exceeds that end, no further interval can overlap.

**How would you solve Meeting Rooms II without a heap, and where would a heap version differ?**

Sort start times and end times separately, then sweep with two pointers: increment rooms at a start, decrement at an end, and keep the maximum. A heap version instead pushes each meeting end, pops all ends <= current start, and takes the max heap size; both are O(n log n), but the heap explicitly retains current meeting end times in order.

**What changes when intervals are half-open, such as [start,end), or when endpoints can be equal and touching should not merge?**

The overlap condition becomes a < d and c < b for half-open intervals, because no point is shared at the closed endpoint. In a merge implementation you would use nextStart < currentEnd instead of <= to avoid merging touching ranges, and in event sweeps you decide the tie order for same-time start and end events to match the intended interval semantics.

**In Minimum Interval to Include Each Query, why sort by interval start and keep a heap by interval size rather than sorting intervals by size alone?**

Sorting intervals by size alone is not enough because a very small interval may end before the current query and be invalid. The correct sweep sorts queries and intervals by left endpoint; for each query, push all intervals whose left <= query into a min-heap keyed by size, pop intervals whose right < query, and the heap top is the smallest valid interval for that query. The full complexity including sorting intervals and queries plus heap pushes/pops is O(n log n + m log m + n log n), safely O((n+m) log(n+m)).

## Worked example

Take intervals [[1,3],[2,6],[8,10],[15,18]]. Sorting by start keeps them in this order. Initialize merged with [1,3]. The next interval [2,6] starts at 2, which is <= current end 3, so extend end to max(3,6)=6. [8,10] starts at 8, which is > 6, so push it as a new interval. [15,18] starts at 15, which is > 10, so push it too. The result is [[1,6],[8,10],[15,18]]; each boundary check needed only one comparison with the last interval's end.

## Common traps

- Using nested pairwise comparisons to check every interval against every other, producing O(n^2) time instead of sorting and scanning.
- Forgetting that sort cost and heap cost both matter in query variants; stating O(n log n) while m queries each cause heap pushes/pops misses O(m log n).
- Getting the overlap condition wrong at equality: using < versus <= or mixing closed and half-open endpoints can either merge touching intervals incorrectly or leave overlaps unmerged.
- Treating Meeting Rooms II like Merge Intervals by sorting by start and comparing adjacent intervals; an early-starting long interval can overlap many later intervals, so you need endpoint sweep or a heap.

</details>

---

## 20. HashMap internals · output · Medium

*java · gate confidence 0.9*

**Question**

What is the exact output of the following Java code?

```java
Map<String,Integer> map = new HashMap<>();
map.put("Aa", 1);
map.put("BB", 2);
System.out.println("Aa".hashCode());
System.out.println("BB".hashCode());
System.out.println(map.size());
```

**Reference answer**

2112
2112
2

**Graded on**

- "Aa" and "BB" both have hash code 2112
- the two keys collide into the same bucket
- HashMap still stores both distinct keys, so size is 2

<details><summary>The lesson this came from</summary>

HashMap is a hash-table implementation backed by an array of buckets. On put it computes the key's hashCode(), spreads the result by XORing with its unsigned right shift by 16, and selects a bucket using (table.length - 1) & hash. Since Java 8, each bucket is initially a linked list of Node entries, but a bucket with more than 8 entries is converted to a red-black tree when the table has at least 64 buckets. The table defaults to capacity 16 and load factor 0.75, doubling when the number of entries exceeds the current threshold.

## Why interviewers ask this

Interviewers use this to test whether the candidate understands the actual data structure behind the API, not just method names. They are listening for collision handling, the hashCode/equals contract, Java 8's treeify change, resize cost, and why HashMap is unsuitable for concurrent use.

## The core idea

HashMap trades memory for speed by keeping entries in an array whose index is derived from the key's hash. Average lookup is O(1) only if hash values are well distributed and the table is sized properly. Equal keys must produce the same hash, but unequal keys may still collide, so after finding the bucket HashMap must compare hashes and equals. Java 8 limits the cost of pathological collisions by treeifying long bucket chains into red-black trees, and by resizing the whole table when collision counts are high but the table is still small. Resizing happens when entries exceed capacity times load factor, and every live entry may be redistributed into the doubled table. HashMap has no ordering guarantee and is not thread-safe.

## Key points

- HashMap defaults to an initial bucket array of 16 and a load factor of 0.75, resizing to double the capacity when the number of entries exceeds 0.75 times the current capacity.
- In Java 8 and later, a collided bucket uses a linked list until it has more than 8 entries; it becomes a red-black tree only if the table already has at least 64 buckets, otherwise the table resizes instead.
- The bucket index is (table.length - 1) & hash, where hash is key.hashCode() XOR (key.hashCode() >>> 16).
- Lookup recomputes the hash, picks the bucket, then compares each candidate's hash and key with equals, so a matching hash alone is not enough.
- HashMap is not synchronized, does not preserve insertion order, and is fail-fast: structural modification during an iterator's lifetime may throw ConcurrentModificationException.

## Your 60-second answer

HashMap is backed by an array of buckets. A put calls key.hashCode(), spreads the result by XORing it with a 16-bit shift, and masks against the array length minus one to pick a bucket. If different keys land in the same bucket, Java 8 and later starts with a linked list there. Once a bucket would grow beyond eight entries and the table has at least 64 buckets, HashMap converts that list into a red-black tree, so that worst-case lookup drops from O(n) to O(log n). Get repeats the hash and then walks the bucket, comparing hash values and calling equals on keys. When the map's size exceeds capacity times load factor—the defaults are 16 and 0.75—it doubles the table and rehashes entries. The main trade-off is memory and upfront overhead for fast average access, and the map is not thread-safe by itself.

## If they dig deeper

**What happens when two different keys have the same hashCode?**

They are stored in the same bucket because the bucket index is derived from the hash. The entries form a linked list, and lookup walks that chain, using equals to distinguish the keys. Java 8 and later may treeify the bucket if the chain becomes long enough.

**Why do hashCode and equals need to be consistent with each other?**

HashMap relies on equal keys hashing to the same bucket. If two objects are equal but have different hashCodes, a get with one object may not even reach the bucket containing the other, so the mapping cannot be found. If hashCodes match but equals is inconsistent, the wrong key may be returned.

**Why did Java 8 add treeification for collided buckets?**

A sufficiently long linked list makes get and put degrade to O(n). A red-black tree gives O(log n) worst-case traversal. The threshold of 8 and table capacity of 64 are a balance: tree nodes cost more memory and CPU than list nodes, and with a good hash such long chains are rare.

**What happens to existing entries when the HashMap resizes?**

The table capacity doubles, so the bit mask gains one bit. Each entry's bucket is recomputed as its hash against the new mask; depending on that extra bit an entry either stays at the same index or moves to oldIndex + oldCapacity. Java 8 may split tree bins back into linked lists if they become small.

**Why can unsynchronized resize corrupt HashMap, or even cause an infinite loop in older Java?**

In Java 7, concurrent resizes could rearrange linked nodes into cycles, causing infinite gets. Java 8 builds lo/hi lists in order and uses trees, so that specific cycle is much less likely, but concurrent puts can still lose updates or corrupt state. HashMap remains unsafe for multi-threaded access.

## Worked example

Take a HashMap with default capacity 16 and put the keys "Aa" and "BB". Both strings have a hashCode of 2112. With a 16-bucket table, index = 2112 & 15 = 0, so both entries land in bucket 0. The first put stores a single Node at bucket 0. The second put chains another Node in the same bucket. A get for "BB" recomputes 2112, goes to bucket 0, then compares the two entries: hash matches, equals is false for "Aa" and true for "BB", so it returns the second entry. If a custom key class overrode equals without hashCode, two equal keys could be sent to different buckets and get would miss.

## Common traps

- Saying HashMap is O(1) in the worst case; it is O(1) average, with O(n) list degradation and O(log n) tree degradation in Java 8+.
- Stating that a bucket treeifies at exactly 8 entries while ignoring the 64-bucket minimum table size.
- Conflating matching hash values with matching keys, and forgetting that equals is what ultimately identifies the key.
- Believing HashMap maintains insertion order or behaves like a thread-safe map.

</details>

---

## 21. Movie Ticket Booking System Design · typed · Hard

*lld · gate confidence 0.9*

**Question**

How does the system handle pricing if a seat type's price changes after a user locks seats but before they pay?

**Reference answer**

The reservation stores the unit price at lock time, so the quoted price remains stable even if the theater changes pricing before payment completes. This prevents surprise charges and disputes.

**Graded on**

- Price snapshot at lock time.
- Reservation stores unit price.
- Quoted price does not change after lock.
- Avoids price-change disputes.

<details><summary>The lesson this came from</summary>

A low-level design exercise for a movie ticket booking service. It models cities, cinemas, halls, movies, shows, seats, bookings, and payments. The system must keep seat availability per show, prevent two users from reserving the same seat, and only confirm the booking after payment succeeds.

## Why interviewers ask this

Interviewers probe class modeling, state transitions for bookings, and concurrency control. They want to see whether you can map requirements to entities and enforce invariants under parallel requests.

## The core idea

The central object is a show, which joins a movie, a hall, and a start time; seats belong to the hall, but their availability is tracked per show. Bookings move through a state machine: reserved (locked), payment pending, confirmed, and cancelled, with a timer releasing unpaid holds. Concurrency is handled by locking individual seat rows or using conditional status updates, so a seat can be taken only when it is currently free. Payment is an external step; the booking is confirmed only after a successful payment, and failure or timeout releases the seats.

## Key points

- Each show is identified by a movie, hall, and start time; a hall can have only one show at a time.
- Seats are physical entities of a hall, and availability is tracked per show, so the same seat can be booked for different showtimes.
- The booking flow creates a short-lived reservation that locks selected seats for a few minutes while payment happens; expiration releases them.
- Use a conditional update or row lock so a seat transitions from FREE to LOCKED only if it is currently FREE, preventing double-booking.
- Payment is recorded against a reservation; a booking becomes confirmed only after payment success, and failed or expired payments cancel the reservation.

## Your 60-second answer

A movie ticket booking system has cities, cinemas, halls, shows, seats, bookings, and payments. I would model a show as movie plus hall plus start time, and track seat availability per show. When a user picks seats, the server creates a short reservation that locks those seats so other users see them as blocked. Payment then runs against that reservation; on success the booking is confirmed and the seats stay booked, and on failure or timeout the lock expires and the seats become available again. The main trade-off is lock duration: a long hold reduces the chance that a paying user loses their seat, but it can leave seats blocked by abandoned checkouts, so you need a TTL and a cleanup job.

## If they dig deeper

**What are the main classes and their relationships?**

Cinema has many halls; hall has many seats and can host many shows over time, one at a time. Movie has many shows. A show belongs to one movie and one hall, with a start time. A booking references one show and many seat IDs; a payment references one booking. Seat availability is stored in a per-show seat table or entity keyed by showId and seatId.

**How do you prevent two users from booking the same seat?**

Use a conditional update such as UPDATE show_seat SET status='LOCKED', lock_until=? WHERE show_id=? AND seat_id=? AND status='FREE'. If zero rows are affected, the seat is already taken. In a single-node in-memory model, you can synchronize on a key made of showId and seatId, but the database conditional update works across replicas.

**What happens when a user never completes payment?**

A scheduled job finds LOCKED seats whose lock_until is before the current time and sets them back to FREE, but only where status is LOCKED. This prevents an expired hold from being confirmed later. The user may retry, but they must re-select seats because the reservation is gone.

**How does pricing work with different seat types?**

Seats have a type such as regular, premium, or recliner. Pricing is per show and per seat type, so premium seats cost more for the same show. The reservation stores the unit price at lock time to keep the quoted price stable even if the theater changes pricing before payment.

**What if a show is cancelled after seats are booked?**

Mark the show as CANCELLED first, then cancel all bookings for that show, refund successful payments idempotently, and notify users. Seat rows are released to FREE for historical consistency, but no new bookings can be created because the show is cancelled.

## Worked example

Assume show S1 in hall H1 with three rows and four seats per row. User A requests seats B2 and B3. The server starts a transaction and runs conditional updates on the per-show seat rows for S1, B2 and S1, B3; both move from FREE to LOCKED with lock_until set to now plus five minutes. At the same moment User B requests B3; his conditional update matches zero rows because B3 is already LOCKED, so B sees the seat as unavailable. User A completes payment, the payment service returns success, and the system creates booking 58, changing those two seat rows from LOCKED to BOOKED. If A's payment had failed or the five minutes had elapsed, a cleanup job would set the rows back to FREE only if their lock_until was in the past.

## Common traps

- Storing seat availability as a boolean on the Seat entity instead of per show, which leads to false conflicts across different showtimes.
- Locking an entire hall or show during seat selection, which serializes all users even when they pick different seats.
- Marking a booking as confirmed before payment succeeds; then you must handle refunds for unpaid checkouts and the audit trail becomes messy.
- Displaying LOCKED seats the same as BOOKED to users, so they cannot tell a temporary hold from a sold seat.

</details>

---

## 22. Unique ID generation · output · Easy

*system_design · gate confidence 0.9*

**Question**

What is printed by this code?
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

**Reference answer**

4C92

**Graded on**

- base62 conversion uses 0-9, A-Z, a-z
- 1000000 maps to 4C92
- output contains no '+' or '/'

<details><summary>The lesson this came from</summary>

Unique ID generation is the process of creating identifiers that are unique across a system without requiring every request to check a central source of truth. Common mechanisms are 128-bit UUIDs produced locally, Snowflake's 64-bit time-ordered IDs split into timestamp, worker ID, and sequence fields, and ticket servers that hand out monotonically increasing values or ranges from a central counter. The central design tension is choosing how much coordination to accept in exchange for ordering, compactness, and failure tolerance.

## Why interviewers ask this

Interviewers use this topic to test whether you can avoid collisions and central bottlenecks in distributed services. It appears in common designs like URL shorteners and distributed tracing, where IDs become primary keys or trace identifiers. A strong answer compares generation strategies by ordering, index locality, failure modes, and size.

## The core idea

Globally unique IDs in a distributed system require either a source of local uniqueness or an out-of-band coordination mechanism. Snowflake partitions the ID space so each worker can generate IDs independently: the classic Twitter layout uses 1 sign bit, 41 timestamp bits, 10 worker ID bits, and 12 sequence bits, giving roughly time-ordered 64-bit values. UUIDs use 128 bits and need no coordination, but random UUIDv4 values are not sequential, which can degrade B-tree index performance by scattering inserts. Ticket servers and DB auto-increment give centrally ordered numeric IDs when issued one at a time, but the central allocation point becomes a bottleneck; batching ranges reduces round trips at the cost of perfect generation-time ordering. The right choice depends on whether you need compact sortable numeric IDs, whether you can tolerate a central dependency, and how you handle clock rollback or worker ID assignment.

## Key points

- A standard UUID is 128 bits; UUIDv4 is generated from random bits and UUIDv7 adds a time-ordered prefix, but neither guarantees uniqueness—it only makes accidental collisions extremely unlikely.
- Twitter Snowflake's classic 64-bit layout is 1 unused sign bit, 41 timestamp bits, 10 worker ID bits, and 12 bits for the per-millisecond sequence.
- Snowflake remains unique only if every worker ID is unique and the system never reuses the same timestamp for the same worker, so implementations must handle clock rollback.
- A central ticket server or database auto-increment produces centrally ordered numeric IDs but becomes a bottleneck and single point of failure unless ranges are preallocated to callers.
- For URL shorteners, generating a 64-bit ID and base62-encoding it avoids URL-unsafe characters; hashing the original URL instead requires collision handling and uniqueness checks in storage.

## Your 60-second answer

For globally unique IDs I look at three mechanisms. UUIDs are 128-bit and can be generated locally, but random UUIDv4 values are not sequential and cause poor index locality. Snowflake gives me 64-bit IDs that sort roughly by time; the classic Twitter layout is one sign bit, 41 timestamp bits, a ten-bit worker ID, and a twelve-bit sequence. It works without a network call as long as worker IDs are unique and the system handles clock rollback by waiting or using a monotonic clock. A ticket server using database auto-increment or range allocation gives centrally allocated numeric IDs, but it is a central dependency. For a URL shortener, I typically generate a Snowflake-style ID and base62 encode it to a short code; if someone proposed hashing the URL, I would store the mapping and resolve collisions by retrying or using a unique constraint.

## If they dig deeper

**How do you generate a unique short ID for a URL shortener?**

I would generate a 64-bit Snowflake-style ID or take an allocated range from a ticket server and base62-encode the numeric ID. If I hash the original URL, I need to handle collisions by checking a unique indexed short code and retrying with salt or length change.

**How do you avoid ID collisions across many servers?**

Each server gets a unique worker ID from a coordination service or static config, and the per-millisecond sequence avoids collisions on one worker. With a ticket server, each instance gets a disjoint range, so no two instances issue the same value.

**What happens if a Snowflake node's clock moves backward?**

The node can wait until its clock catches up with the last timestamp it used, or use a monotonic time source. Without that, the same timestamp plus worker ID plus sequence can repeat and create duplicate IDs.

**How do you keep generating IDs if the central ticket server is down?**

You cannot hand out new ranges once the central ticket server is unavailable, unless callers have preallocated enough local range to ride out the outage. That is the main reason some designs prefer local generation like Snowflake for availability.

**How do trace IDs differ from short URL IDs, and what priority changes?**

Trace IDs usually need to be unique but not necessarily sequential or compact; they often use 128-bit random values, and they must propagate across services with parent/span IDs. For tracing, probabilistic uniqueness and low overhead matter more than index locality, while URL IDs want short, dense, base62-encodable values.

## Worked example

Suppose a ticket server allocates ranges by atomically incrementing a high-water mark in a database. Server A requests 1,000 IDs and receives 1000000–1000999, then server B receives 1001000–1001999. Each server generates from its own range without further network calls until it runs out, so collisions are impossible as long as ranges never overlap. Server A takes numeric ID 1000000 and base62-encodes it with the alphabet 0-9, A-Z, a-z; the result is '4C92'. The mapping between that code and the original URL is stored with a unique index, which rejects any duplicate code if a bug ever caused one. If the service used Snowflake instead, two IDs generated in the same millisecond on the same worker would differ only in the 12-bit sequence field.

## Common traps

- Saying UUIDs guarantee uniqueness: they make collisions probabilistically negligible but cannot guarantee it, and weak randomness or implementation bugs raise the risk.
- Ignoring Snowflake clock rollback: if a node's wall clock moves backward, it can reuse a timestamp and produce duplicate IDs unless it waits or uses a monotonic clock.
- Using database auto-increment as a global ID service without batching: every ID generation becomes a network or database round trip, creating a central bottleneck.
- Generating short codes with base64 instead of base62: base64 includes '+' and '/', which need URL encoding and break clean short URLs.

</details>

---

## 23. Memory Allocation · mcq · Hard

*cs · gate confidence 0.92*

**Question**

What is the consequence of calling free on the original pointer after a successful realloc?

**Options**

- Always safe because realloc may not move the block
- Undefined behavior; may cause a double free if the block was moved
- Safe only if realloc returned the same pointer
- Safe because the original pointer is automatically updated

**Reference answer**

Undefined behavior; may cause a double free if the block was moved

**Graded on**

- realloc invalidates original pointer
- double free if block moved

<details><summary>The lesson this came from</summary>

Dynamic memory allocation reserves blocks on the heap at runtime from a region managed by an allocator. In C, malloc, calloc, and realloc request blocks and free returns them; in managed runtimes, a garbage collector reclaims unreachable heap objects automatically. The allocator tracks free blocks in a free list and selects blocks using strategies such as first fit, best fit, or worst fit. Because blocks are allocated and freed in any order, the heap can become fragmented into unusable holes.

## Why interviewers ask this

The interviewer wants to know whether you understand what happens under malloc and free: how the allocator tracks free memory, why fragmentation occurs, and how leaks, double frees, and use-after-free arise. Strong candidates also connect these ideas to system design choices such as memory pools and compacting collectors.

## The core idea

Heap allocation is a request to an allocator that carves blocks out of a larger memory region and later recycles them. The allocator needs to know which parts are free and which are in use; a typical design keeps a free list of available blocks and splits, coalesces, or merges them as allocations occur. Allocation policy matters because it determines speed and fragmentation: first fit is usually fast but leaves many small holes; best fit leaves the smallest remainder but can be slower and create tiny slivers; worst fit preserves large blocks but can exhaust them. External fragmentation means enough total free memory exists but no single contiguous block is large enough for a request, while internal fragmentation is wasted space inside an allocated block, often from rounding up or metadata overhead. In C, the programmer is responsible for matching every allocation with exactly one free and for never using memory after freeing it; realloc invalidates the original pointer even when the block does not move. Managed languages like Java use a garbage collector to identify and free unreachable objects, eliminating manual free but adding pauses and overhead.

## Key points

- In C, malloc returns uninitialized memory, calloc zero-initializes it, and realloc may move a block; every successful allocation must eventually be freed exactly once, with only the returned realloc pointer valid.
- A free list stores available heap blocks, and first-fit chooses the first adequate block, best-fit chooses the smallest adequate block, and worst-fit chooses the largest adequate block.
- External fragmentation is free memory split into non-contiguous holes, causing allocation failures even when total free bytes exceed the request; internal fragmentation is wasted space inside an allocated block due to rounding or metadata.
- Coalescing merges adjacent free blocks to create larger blocks, reducing external fragmentation; compaction moves allocated blocks to eliminate holes but requires updating all pointers and is usually only practical in managed or relocatable heaps.
- Freeing a pointer not returned by an allocation, double-freeing, or using memory after free is undefined behavior in C; after a successful realloc, the original pointer is invalid and may not be freed or dereferenced.

## Your 60-second answer

Dynamic memory allocation reserves space on the heap at runtime, while the stack is for automatic local variables. In C, malloc and calloc request a block, free returns it, and realloc may resize or move it. The allocator maintains a free list and picks a block using first fit, best fit, or worst fit. Because blocks are freed in any order, the heap can fragment: external fragmentation is free memory split into holes too small for a request, and internal fragmentation is wasted space inside a block. Allocators reduce this by coalescing adjacent free blocks. The core trade-off is speed versus memory efficiency: first fit is usually fast but leaves more small holes; best fit minimizes leftover but is slower. The contract is strict: every allocation must be freed exactly once, and after a successful realloc only the returned pointer is valid.

## If they dig deeper

**What is the difference between stack and heap allocation?**

The stack is a LIFO region per thread where local variables and return addresses live; allocation is just moving the stack pointer, so it is fast and freed automatically on function return. The heap is a larger shared region for objects whose size is unknown at compile time or whose lifetime extends beyond the current call; allocation requires a runtime allocator, and in C the programmer must free it manually.

**What causes external fragmentation, and how does an allocator reduce it?**

External fragmentation arises when free memory is split into many non-contiguous holes interleaved with allocated blocks, so a large request can fail even though total free memory is sufficient. Allocators reduce it by coalescing adjacent free blocks when memory is freed, using strategies like best-fit to keep large blocks intact, and sometimes by compacting allocated blocks together—though compaction requires updating all pointers and is uncommon in unmanaged languages.

**How does realloc behave, and why can't you keep the old pointer?**

realloc attempts to resize a previously allocated block, possibly in place if adjacent space is free; if not, it allocates a new block, copies the old contents, and frees the old block. After a successful realloc, the original pointer value is invalid regardless of whether the block moved or was resized in place; using or freeing it is undefined behavior and may be a double-free if the block moved. Only the returned pointer is valid and must eventually be freed once.

**Compare first fit, best fit, and worst fit allocation strategies.**

First fit picks the first free block large enough, which is fast but tends to leave many small holes near the beginning and may increase fragmentation. Best fit scans the whole free list and picks the smallest block that fits, wasting the least space but leaving very small unusable fragments and requiring a full scan, so it can be slower. Worst fit picks the largest block, leaving a big remainder for future requests but can quickly deplete large contiguous blocks and cause failures for large allocations. Modern allocators often use segregated size classes rather than a single linear strategy to balance speed and fragmentation.

**How would you design malloc and free for a fixed-size memory pool?**

Preallocate a contiguous memory region and divide it into equal blocks of the requested size, maintaining a free list of unallocated blocks. Allocation pops an index or pointer from the free list in O(1), and free pushes it back, optionally using a bitmask or canary to detect double frees. Because all blocks are the same size, there is no external fragmentation and no splitting or coalescing; you need to handle thread safety and alignment. This works when the application has a bounded number of fixed-size objects, such as network buffers or connection state.

## Worked example

Suppose a simple heap of 1 KB starts as one free block and an allocator places three calls sequentially: malloc(200), malloc(100), and malloc(150) return addresses 0, 200, and 300. The remaining free block is 574 bytes at address 450. If the program frees the 100-byte block, the free list now has a 100-byte hole at address 200 between two allocated blocks and the 574-byte tail at 450. A subsequent malloc(600) fails, even though total free memory is 674 bytes, because no contiguous free block is 600 bytes; that is external fragmentation. If the program also frees the 200-byte block, the allocator can coalesce the adjacent 200-byte and 100-byte free blocks into a 300-byte block, but the largest contiguous free block remains 574 bytes, so a 600-byte request still fails. Only after freeing the 150-byte block and coalescing everything would the allocator have a single 1024-byte block and be able to satisfy the request. This sequence shows why allocators coalesce on free and why they sometimes split larger blocks to retain usable holes.

## Common traps

- Freeing the original pointer after a successful realloc is undefined behavior even if the block was resized in place; only the returned pointer is valid and must be freed.
- Assigning realloc's return value directly to the original pointer without checking for NULL leaks the original block when realloc fails, because the old block remains allocated.
- Assuming that enough total free memory guarantees malloc success is wrong: external fragmentation can cause failure when free blocks are too small and non-adjacent.
- Reading memory returned by malloc without first writing to it yields indeterminate values, because malloc does not initialize the allocated block.

</details>

---

## 24. SQL · output · Medium

*ai · gate confidence 0.95*

**Question**

Given the tables:
customers(id, name): (10, 'Ada'), (20, 'Bob'), (30, 'Cara')
orders(id, customer_id, amount): (1, 10, 100), (2, 20, 50)

What is the exact output of:
```sql
SELECT customers.name, orders.amount
FROM customers
LEFT JOIN orders ON customers.id = orders.customer_id
ORDER BY customers.id;
```
Assume each row prints as `name amount`, with NULL shown as `NULL`.

**Reference answer**

Ada 100
Bob 50
Cara NULL

**Graded on**

- Ada matches order 100
- Bob matches order 50
- Cara has no match, so amount is NULL

<details><summary>The lesson this came from</summary>

SQL is a declarative language for querying and modifying data in relational databases. The core DML statements are SELECT for retrieval and INSERT, UPDATE, and DELETE for mutation. JOIN clauses combine rows from two or more tables based on a related column. Transactions control when writes become permanent and when other sessions can see them.

## Why interviewers ask this

Interviewers test whether you can translate a business question into set-based SQL rather than row-by-row logic. They also probe semantics that cause silent wrong results: join cardinality, NULL comparisons, inclusive ranges, and transaction isolation behavior across engines.

## The core idea

SQL expresses operations over sets of rows, so a query describes the result, not the algorithm. Filtering happens in WHERE, grouping in GROUP BY, and ordering in ORDER BY. Joins match rows by key values; an inner join keeps only matches, while outer joins preserve unmatched rows from one or both sides by filling missing columns with NULL. Writes such as INSERT, UPDATE, and DELETE are transactional, but visibility of uncommitted writes depends on the isolation level: READ UNCOMMITTED permits dirty reads in MySQL and SQL Server, whereas PostgreSQL treats that level as READ COMMITTED.

## Key points

- SELECT lists columns and WHERE filters rows; without ORDER BY, result order is not guaranteed.
- BETWEEN is inclusive, so WHERE price BETWEEN 10 AND 100 includes both 10 and 100, while IN matches a discrete list.
- INNER JOIN returns only rows with matching keys in both tables; LEFT, RIGHT, and FULL OUTER JOIN preserve unmatched rows from one or both sides and fill missing columns with NULL.
- INSERT, UPDATE, and DELETE are transactional in PostgreSQL, MySQL InnoDB, and SQL Server; under READ UNCOMMITTED, MySQL and SQL Server may expose uncommitted changes as dirty reads, while PostgreSQL maps that level to READ COMMITTED.
- NULL is unknown, so '= NULL' is never true; use IS NULL, and note that joins do not match NULL keys.

## Your 60-second answer

SQL is a declarative language for querying and modifying relational data. You describe the rows you want, not the access path. SELECT reads rows and can filter with WHERE, aggregate with GROUP BY, and combine tables with JOINs. An inner join keeps only rows with matching keys; left and right joins preserve unmatched rows from one side and fill the other side with NULL. BETWEEN is inclusive, so BETWEEN 10 and 100 includes both endpoints, while IN matches a discrete list. INSERT, UPDATE, and DELETE are transactional and not permanent until commit, but visibility of uncommitted writes depends on isolation level: MySQL and SQL Server allow dirty reads under READ UNCOMMITTED, while PostgreSQL treats that level as READ COMMITTED. The main trade-off is that set-based SQL requires care with duplicates, NULLs, and join cardinality to avoid silently wrong results.

## If they dig deeper

**What is the difference between WHERE and HAVING?**

WHERE filters individual rows before grouping and aggregation. HAVING filters groups after GROUP BY, so it can reference aggregate functions like COUNT(*) or SUM(amount). A predicate on non-aggregated columns can go in either, but WHERE is usually more efficient because fewer rows reach grouping.

**How do BETWEEN and IN differ, and are the endpoints in BETWEEN included?**

BETWEEN is inclusive: WHERE price BETWEEN 10 AND 100 includes 10 and 100. It applies to ordered ranges such as numbers, dates, and strings. IN matches a value against a discrete list and is often used for categorical values, though it works for any type. BETWEEN is not safe for floating-point boundaries where equality is unstable.

**How do NULLs behave in comparisons and joins?**

NULL represents unknown, so col = NULL is never true; use IS NULL or IS NOT NULL. Aggregates skip NULL inputs except COUNT(*). In joins, NULL keys never match, so rows with NULL join keys are excluded from inner joins and appear as unmatched in outer joins.

**Under which isolation levels can other sessions see uncommitted writes, and how do MySQL, PostgreSQL, and SQL Server differ?**

READ UNCOMMITTED permits dirty reads: a session can see another session's uncommitted INSERT, UPDATE, or DELETE. MySQL and SQL Server implement this behavior. PostgreSQL accepts READ UNCOMMITTED syntactically but treats it as READ COMMITTED, so dirty reads do not occur. MySQL InnoDB defaults to REPEATABLE READ, while PostgreSQL defaults to READ COMMITTED.

**A LEFT JOIN returns more rows than the left table. What should you check first?**

Check whether the join key is unique in the right table. If multiple right-side rows share the same key, each match duplicates the left row. Also confirm you joined on the intended key and that the left table actually has duplicates. Run SELECT key, COUNT(*) FROM right_table GROUP BY key HAVING COUNT(*) > 1 to find the offending keys, then either deduplicate the right side or accept the one-to-many cardinality explicitly.

## Worked example

Two tables: orders(id, customer_id, amount) with rows (1, 10, 100), (2, 20, 50); customers(id, name) with (10, 'Ada'), (20, 'Bob'), (30, 'Cara'). SELECT customers.name, orders.amount FROM customers LEFT JOIN orders ON customers.id = orders.customer_id ORDER BY customers.id; returns three rows: Ada 100, Bob 50, Cara NULL. The id 10 matches the first order and id 20 matches the second; Cara has no matching order, so LEFT JOIN preserves her with NULL amount. If customers had two rows with id 10, each would match the same order and produce two rows. A filter WHERE price BETWEEN 10 AND 100 includes 10 and 100 exactly.

## Common traps

- Assuming SQL result order is deterministic without an ORDER BY clause.
- Using `= NULL` instead of `IS NULL` when checking for null values.
- Assuming a LEFT JOIN cannot increase row count when the right table has duplicate join keys.
- Claiming uncommitted writes are never visible, without qualifying the isolation level and engine.

</details>

---

## 25. Lambda expressions · mcq · Hard

*java · gate confidence 0.95*

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

A lambda expression in Java 8 and later is a concise anonymous function that can be used wherever a functional interface (an interface with exactly one abstract method) is expected. It consists of a parameter list, the arrow token ->, and a body that is either a single expression or a statement block. The compiler infers the target functional interface type from the surrounding context, so a lambda is not a new kind of object but a shorthand implementation of that interface's single method.

## Why interviewers ask this

Interviewers use lambda questions to check whether you actually understand functional interfaces, target typing, and variable capture rather than just remembering syntax. They often ask you to rewrite a comparator, Runnable, or listener with a lambda, then probe how it differs from an anonymous class. The follow-ups reveal whether you can reason about scoping and type inference, not just produce code.

## The core idea

A lambda expression is syntax over an instance of a functional interface; it does not introduce a new function type but implements the interface's one abstract method. The compiler infers parameter types and the target type from the assignment, method argument, or cast context. A lambda body may be an expression, whose value is returned implicitly when the interface method returns a value, or a block with an explicit return. Lambdas capture effectively final local variables, while instance fields and static variables remain mutable. Unlike an anonymous inner class, this inside a lambda refers to the enclosing instance, and lambdas cannot access the functional interface's default methods through their own implicit receiver.

## Key points

- A Java lambda requires a functional interface: exactly one abstract method, with default, static, and Object methods not counting toward that limit.
- Local variables captured by a lambda must be effectively final, but instance fields and static variables may be mutated.
- The body can be a single expression (implicitly returned for a non-void method) or a block that uses an explicit return statement.
- Lambdas differ from anonymous classes: this inside a lambda refers to the enclosing instance rather than the lambda object.
- Parameter types can be omitted, and parentheses around a single untyped parameter can also be omitted.

## Your 60-second answer

A lambda expression is a concise way to implement a functional interface, which is an interface with exactly one abstract method. For example, instead of writing an anonymous Comparator class, you can write Comparator<String> byLength = (a, b) -> Integer.compare(a.length(), b.length());. The compiler treats the lambda as an instance of that interface and infers parameter types from the target context. Lambdas can capture effectively final local variables and instance fields, and unlike anonymous classes, this refers to the enclosing object, not the lambda. The main trade-off is that lambdas only work with single-method interfaces, so richer callbacks still require an anonymous or named class.

## If they dig deeper

**What is a functional interface, and what does @FunctionalInterface do?**

A functional interface has exactly one abstract method. The @FunctionalInterface annotation is not required but causes a compile-time error if you try to add a second abstract method, similar to @Override. Default and static methods are allowed with the annotation since they are not abstract.

**What variables can a lambda expression access from its surrounding scope?**

A lambda can read local variables that are effectively final, meaning they are never reassigned after initialization, even if not declared final. It can also read and write instance fields and static variables. The lambda cannot call default methods of the functional interface it is implementing because it has no implicit this referring to the lambda instance.

**How does this behave differently in a lambda compared to an anonymous inner class?**

In an anonymous inner class, this refers to the anonymous class instance itself. In a lambda, this is lexically scoped and refers to the enclosing object where the lambda is written. As a result, a lambda cannot define its own instance fields or use this to call the functional interface's default methods.

**Can a lambda that implements a void method use an expression body?**

Only if the expression is a statement expression, such as a method invocation or assignment. An arbitrary non-void expression like () -> 42 is not compatible with a void functional interface because the body would not be a valid statement expression. For a block body implementing a void method, no return statement is needed.

**How does target typing work when a lambda is passed to an overloaded method?**

The compiler uses the parameter type of the chosen method as the target functional interface. If multiple overloads have argument types that are different functional interfaces and the lambda body is compatible with more than one of them, the call is ambiguous and fails to compile. Explicitly casting the lambda or assigning it to a typed variable resolves the ambiguity.

## Worked example

Consider a list of strings: List<String> names = Arrays.asList("Ada", "Bob", "Charlie");. To sort it by length, you can write Collections.sort(names, (a, b) -> Integer.compare(a.length(), b.length()));. The target type is Comparator<String>, so the compiler infers that a and b are String parameters. If you then use a stream, int minLength = 3; List<String> longNames = names.stream().filter(s -> s.length() >= minLength).collect(Collectors.toList());, the lambda inside filter captures minLength. Since minLength is never reassigned, it is effectively final, and the code compiles. After the sort, names is ordered by string length, with equal-length entries retaining their relative order because the sort algorithm is stable.

## Common traps

- Assuming a lambda can implement any interface; it only works with functional interfaces that have exactly one abstract method.
- Trying to reassign a local variable captured by a lambda after the lambda is created; the variable must be effectively final.
- Expecting this inside a lambda to refer to the lambda object itself, like it does in an anonymous inner class.
- Using a block body without an explicit return when the functional interface method returns a non-void value.

</details>

---

## Cards the gate rejected

Judge whether it was right. Each was thrown away.

- **java-equals-and-hashcode-contract** (typed): What rules must an equals implementation itself obey?
  - Gate said: wrong_format: The honest answer is an enumeration of five specific contract properties (reflexive, symmetric, transitive, consistent, non-nullity).

- **java-heap-vs-stack** (flash): What exactly is stored in a Java stack frame?
  - Gate said: wrong_format: The complete contents of a Java stack frame require listing multiple components (local variables, operand stack, frame data/reference to runtime constant pool), which does not fit a single crisp sentence.

- **lld-atm-system-design** (flash): During a normal ATM session, at what points is the customer's card returned or released by the machine?
  - Gate said: wrong_format: Listing multiple points during a session requires an enumeration rather than one crisp flashcard sentence.

- **lld-restaurant-management-system-design** (flash): In an object-oriented restaurant management system, a Branch object is composed of which two main domain components?
  - Gate said: not answerable: Points to a specific proprietary or textbook design class model without standard universal domain components.

- **sd-indexes** (flash): What is the default index structure in most relational engines, and why is it broadly useful?
  - Gate said: wrong_format: Answering both what the default structure is and explaining why it is broadly useful cannot be done in a single crisp sentence.

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

- **ai-prediction-service** (mcq): Which technique does NOT reduce inference compute for an existing model?
  - Gate said: not answerable: All listed techniques (quantization, pruning, operator fusion, knowledge distillation) can reduce inference compute for a model.

- **ai-probability-and-statistics** (flash): State the three axioms that any probability measure must satisfy.
  - Gate said: wrong_format: Stating three distinct mathematical axioms cannot fit into a single crisp sentence.

- **ai-python** (mcq): Python's list and tuple are ordered sequences, while dict and set are hash-based containers. Which pair of properties primarily explains why a tuple can be a dictionary key but a list cannot, and why dict/set membership is average O(1) while list membership is O(n)?
  - Gate said: a competent answer disagrees with the marked option

- **ai-recommendation-systems** (typed): How would you design a video recommendation system?
  - Gate said: wrong_format: An end-to-end system design question cannot be answered in 1-3 sentences.

- **ai-sql** (flash): What are the core DML statements in SQL for retrieving and modifying data?
  - Gate said: wrong_format: Asking for an enumeration of multiple core DML statements does not fit a single-sentence flash card format.

- **ai-training-and-optimization** (flash): Name two alternative update rules beyond vanilla gradient descent that alter how the raw gradient is applied.
  - Gate said: not answerable: The question asks to name any two alternatives out of many possibilities, making grading unpredictable.

- **beh-company-and-motivation** (mcq): In a behavioral interview, which impact signal is most appropriate for a senior engineer describing a proudest project?
  - Gate said: a competent answer disagrees with the marked option

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

- **beh-leadership** (flash): What is the real measure of thought leadership in an interview answer?
  - Gate said: not answerable: The question is too vague and subjective with no single standard definition of the 'real measure' of thought leadership.

- **beh-leadership** (flash): What common senior failure makes a candidate sound like an executor instead of a leader?
  - Gate said: not answerable: The question points to a specific unspecified failure mode from a curriculum rather than a universally unique answer.

- **beh-leadership** (flash): In behavioral interviews, what does leadership mean independent of formal authority?
  - Gate said: a human reviewer objected: In behavioral interviews, what does leadership mean independent of formal author

- **beh-leadership** (mcq): Which set of behaviors best describes effective leadership during a high-pressure crisis or significant disruption?
  - Gate said: a human reviewer objected: Which set of behaviors best describes effective leadership during a high-pressur

- **beh-leadership** (mcq): A senior candidate is preparing a behavioral story about leadership. Which set of dimensions should the story cover to avoid sounding like a single-dimensional executor?
  - Gate said: not answerable: Multiple option lists are arbitrary frameworks that could defensibly be considered valid dimensions of leadership without an external syllabus.

- **beh-ownership** (mcq): In behavioral interviews, ownership stories often scale with seniority: junior changes affect the candidate's own focus area, senior changes require coordinating several people (often three or more) on a team, and staff changes require multiple teams across the organization. According to this framework, which story best demonstrates senior-level ownership?
  - Gate said: refers to unseen material: 'According to this'

- **beh-story-craft** (mcq): Which opening best separates team context from your personal contribution in a behavioral story?
  - Gate said: a competent answer disagrees with the marked option

- **beh-story-craft** (typed): What is defensive framing in story craft, and why is it useful?
  - Gate said: not answerable: 'Defensive framing' is specialized jargon specific to an unseen source text rather than standard interview prep terminology.

- **cs-file-systems** (flash): What is a hard link, and why can it not cross filesystems?
  - Gate said: wrong_format: Answering both what a hard link is and why it cannot cross filesystems requires more than one crisp sentence.

- **cs-locking-mechanisms** (typed): What are intent locks and why are they needed?
  - Gate said: a human reviewer objected: What are intent locks and why are they needed?

- **cs-osi-model** (flash): Name the seven OSI layers from bottom to top.
  - Gate said: wrong_format: Enumerating a seven-item ordered list does not fit a single-sentence flash card format.

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

- **java-collections-framework** (flash): What iteration order guarantees do HashSet, LinkedHashSet, and TreeSet provide?
  - Gate said: wrong_format: Explaining the order guarantees for three distinct set implementations exceeds a single crisp sentence.

- **java-collections-framework** (flash): How does PriorityQueue order its elements, and what are its add and poll costs?
  - Gate said: wrong_format: Asking for ordering mechanism plus multiple asymptotic complexities exceeds a single crisp flashcard sentence.

- **java-collections-framework** (flash): In the Java Collections Framework, which interfaces extend Collection, and where does Map fit?
  - Gate said: wrong_format: Answering all interfaces extending Collection plus Map's position cannot be crisply answered in a single sentence.

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

- **lld-elevator-system-design** (mcq): Which set of states correctly models an elevator car as a finite state machine in an object-oriented elevator control system?
  - Gate said: not answerable: There is no single universally correct state modeling; multiple state decompositions (such as combining moving with direction or separating them) are defensible.

- **lld-interfaces** (flash): What is a traditional interface not allowed to define in Java or C#?
  - Gate said: not answerable: Too open-ended and ambiguous with multiple valid answers (instance state/fields, method implementations, constructors, etc.).

- **lld-parking-lot-design** (flash): What are the typical parking spot types modeled in a parking garage?
  - Gate said: wrong_format: Enumerating a list of spot types does not fit a single-sentence flash card.

- **lld-ride-sharing-service-design** (typed): What happens in the dispatch flow when a driver does not accept an offer before the timeout expires?
  - Gate said: a human reviewer objected: What happens in the dispatch flow when a driver does not accept an offer before 

- **lld-ride-sharing-service-design** (flash): Why should driver availability be a separate state rather than being derived only from trip status?
  - Gate said: a human reviewer objected: Why should driver availability be a separate state rather than being derived onl

- **lld-uml-sequence-diagram** (flash): What is a UML sequence diagram, and what do the vertical and horizontal axes represent?
  - Gate said: wrong_format: Asking for definition plus both axes typically requires multiple sentences or clauses beyond a single crisp sentence.

- **prefix-sum** (typed): Using a prefix-sum map initialized with {0: -1}, find the length of the longest zero-sum subarray in [2, -1, -1, 3, -3].
  - Gate said: wrong_format: The question asks for a single numeric result or calculation rather than free prose explanation.

- **sd-caching** (mcq): In the worked example, a product page is fetched 5,000 times per second and the database sustains 800 reads per second. After the Redis cache is warm with a 30-second TTL, how many database reads per second does that single product key cause?
  - Gate said: not answerable: References an unseen 'worked example'.

- **sd-consistent-hashing** (typed): How is replication placed on a consistent hash ring?
  - Gate said: a human reviewer objected: How is replication placed on a consistent hash ring?

- **sd-consistent-hashing** (typed): Why are virtual nodes added to a consistent hash ring?
  - Gate said: a human reviewer objected: Why are virtual nodes added to a consistent hash ring?

- **sd-design-a-chat-system** (typed): In a real-time chat system, what are the two primary subsystems of the architecture, and why are they separated?
  - Gate said: not answerable: Asking for 'the two primary subsystems' without context expects specific terminology from an unseen text.

- **sd-design-a-notification-system** (typed): How do you handle machine failures in a notification worker system?
  - Gate said: a human reviewer objected: How do you handle machine failures in a notification worker system?

- **sd-design-a-notification-system** (typed): When would you use a persistent WebSocket connection for in-app notifications instead of APNS/FCM push?
  - Gate said: a human reviewer objected: When would you use a persistent WebSocket connection for in-app notifications in

- **sd-design-case-studies** (typed): How do you mark a payment as completed and prevent a duplicate webhook from double-applying the update?
  - Gate said: a human reviewer objected: How do you mark a payment as completed and prevent a duplicate webhook from doub

- **sd-design-case-studies** (flash): What mechanism is appropriate for counting current active page viewers?
  - Gate said: not answerable: There are many valid mechanisms (Redis HyperLogLog, sliding window bucket counters, sorted sets) with no single correct answer.

- **sd-design-case-studies** (mcq): How should you shard an idempotency store so that uniqueness checks on idempotency keys are local?
  - Gate said: a competent answer disagrees with the marked option

- **sd-design-case-studies** (typed): Two concurrent requests with the same Idempotency-Key and merchant_id arrive at the payment API. What ensures only one provider call is made?
  - Gate said: a human reviewer objected: Two concurrent requests with the same Idempotency-Key and merchant_id arrive at 

- **sd-jwt** (mcq): Where should a JWT be stored to prevent JavaScript on the page from reading it?
  - Gate said: a human reviewer objected: Where should a JWT be stored to prevent JavaScript on the page from reading it?

- **sd-microservices** (typed): How should a ranking and personalization component be integrated into a microservices system?
  - Gate said: not answerable: The question is too vague and lacks system context, allowing for dozens of mutually distinct correct integration patterns.

- **sd-object-storage** (mcq): In Amazon S3 multipart upload, what is the minimum part size for every part except the last one?
  - Gate said: wrong_format: AWS documentation defines the minimum part size as 5 MB, making both '5 MiB' and '5 MB' ambiguously close or technically disputable.

- **sd-object-storage** (flash): Name the three major managed object storage services.
  - Gate said: wrong_format: Flash cards require a single crisp sentence, not a list of named entities which is open to varying company selections.

- **sd-rate-limiting** (flash): What HTTP status and response headers should a rate limiter use when a caller exceeds its limit?
  - Gate said: wrong_format: Asking for the HTTP status and multiple response headers requires listing items rather than a single crisp sentence.

- **sd-rest-api** (flash): Which HTTP methods are idempotent in REST, and which one is not?
  - Gate said: wrong_format: Enumerating multiple idempotent and non-idempotent HTTP methods exceeds a single crisp sentence.

- **sd-service-discovery** (flash): Name common service registry implementations used for service discovery.
  - Gate said: not answerable: Asking to list multiple implementations is an open-ended enumeration poorly suited for a single-sentence flash card.

- **sd-sql-vs-nosql** (flash): What are the four common NoSQL database models?
  - Gate said: wrong_format: The answer requires enumerating four distinct items rather than a single crisp sentence.

- **sd-unique-id-generation** (flash): What is the classic Twitter Snowflake 64-bit ID layout?
  - Gate said: wrong_format: Listing the exact bit allocation across four fields requires a structured or multi-part answer that does not fit a single crisp flash sentence.

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

- **sql-constraints** (mcq): Which of the following is a separate column requirement often grouped with SQL constraints, rather than one of the common declarative constraints?
  - Gate said: not answerable: NOT NULL is standardly defined as a declarative constraint in SQL, making the question ambiguous and poorly defined.

- **sql-constraints** (typed): What is the difference between a PRIMARY KEY and a FOREIGN KEY?
  - Gate said: a human reviewer objected: What is the difference between a PRIMARY KEY and a FOREIGN KEY?

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

- **sql-recursive-ctes** (flash): What are the three structural parts of a recursive CTE?
  - Gate said: wrong_format: Asking for three structural parts requires enumerating multiple components rather than a single crisp statement.

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
