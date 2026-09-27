# 90x card review

2783 cards are ready to publish. An automated gate read 2810 and objected to 27 of them (1%): 0 were rewritten and passed on the second look, 27 could not be saved and were dropped (1%). Mix: 1366 typed, 736 mcq, 612 flash, 69 output.

*No card here is recorded as caught-and-rewritten. Card runs before 2026-09-28 did not keep that record, so on an older run the rewrite pass is invisible rather than idle, and the drop rate is the only measured number above.*

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

## 1. Leadership · flash · Easy

*behavioral · gate confidence 0.8*

**Question**

What is the real measure of thought leadership in an interview answer?

**Reference answer**

Concrete artifacts such as internal design docs, blog posts, talks, or open-source contributions tied to a distinctive point of view that influenced a real decision, with focus on changed thinking or adoption rather than visibility or publication count.

**Graded on**

- Concrete artifacts with point of view
- Influenced a real decision
- Changed thinking or adoption, not publication count

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

## 2. Story craft · typed · Medium

*behavioral · gate confidence 0.8*

**Question**

What is defensive framing in story craft, and why is it useful?

**Reference answer**

Defensive framing means proactively explaining constraints and mistakes as decisions with reasons, so the interviewer hears your rationale instead of forming an uncharitable interpretation. It is useful because it prevents avoidable problems from being read as carelessness or poor judgment.

**Graded on**

- Proactively explain constraints and mistakes
- Frame decisions with reasons
- Avoid uncharitable interpretations

<details><summary>The lesson this came from</summary>

Story craft in behavioral interviews is the deliberate selection, structuring, and framing of a real work experience to demonstrate a specific engineering or leadership signal. It combines a clear sequence—situation, the action you personally took, and the result—with details chosen to anticipate interviewer follow-ups. It is not inventing events or memorizing a monologue; it is preparing multiple true stories and adjusting their emphasis to the question and company values.

## Why interviewers ask this

Interviewers use behavioral stories to infer how you will behave on their team, not just what you know. They are testing whether you can communicate a complex situation in a short answer, own your decisions, show impact, and fit the company's stated values. Weak story craft usually signals either lack of relevant experience or lack of self-awareness, regardless of technical strength.

## The core idea

A strong behavioral story is specific, personal, and narrow enough to explain in two minutes. The interviewer should be able to separate what you did from what the team did, so use 'I' for decisions and actions you owned. The event itself matters less than the reasoning you show: why you chose one option, what you learned, and how you adjusted. Prepare a story catalog mapped to common signal areas—conflict, disagreement, failure, leadership, ambiguous requirements—and to the company's values. Be defensive in framing: omit irrelevant details that invite uncharitable interpretations, and for unavoidable problems explain the rationale rather than hoping the interviewer will not ask. Do not fight the question; adapt the same true experience to the signal being probed.

## Key points

- A well-crafted answer names a specific situation, the action you personally took, and a result the interviewer can verify through follow-ups.
- Story selection should match the signal in the question—leadership, conflict, failure, ambiguity—rather than defaulting to the largest project.
- Preparing a catalog of true stories mapped to common signals and company values is more reliable than improvising each answer.
- Defensive framing means proactively explaining constraints and mistakes as decisions with reasons rather than waiting for the interviewer to interpret them badly.
- Saying 'I' for your own actions and 'we' only for team context preserves credibility and helps the interviewer assess you, not your team.

## Your 60-second answer

Story craft for behavioral interviews is the work of turning a real experience into a short, structured answer that shows what you personally did and why. I use a situation-action-result shape, but I change the emphasis depending on what the question is actually testing—conflict, leadership, ambiguity, or a mistake. For example, the same delayed project can be told as a story about aligning a stakeholder if the question is about disagreement, or as a story about changing process if the question is about learning from failure. The reason this matters is that the interviewer is evaluating my judgment and communication, not the event itself. The trade-off is polish versus authenticity: if the story is too scripted, I stop answering the actual follow-up and start performing.

## If they dig deeper

**How do you decide which story to tell when a question could fit several experiences?**

I pick the story whose central action best matches the signal in the question, not the most impressive project. I keep short notes on my experiences mapped to conflict, leadership, failure, ambiguity, and impact, so I can choose quickly. Then I spend the first sentence setting up the part of the experience that answers that specific signal.

**What structure do you use when telling the story itself?**

I use a situation-action-result structure, but I treat it as a logical order rather than a formula. I give just enough context to make the decision understandable, say what I personally did and why, then give a result with numbers or observable consequences. I also think about what follow-up question my ending invites and can extend the story backward or forward.

**How do you tell a story where the outcome was partly bad or you made a real mistake?**

I don't hide the mistake if the question is about a failure, because an unforced admission followed by what I changed is usually stronger than a defensive answer. I state the mistake briefly, explain what I misjudged at the time, describe the concrete fix or process change, and end with how I acted differently later. The key is to take individual ownership for the part I controlled rather than blaming the team or the circumstances.

**How do you avoid sounding rehearsed when you have prepared the story in advance?**

I prepare the key beats, the one decision I want to emphasize, and the numbers or facts, not word-for-word scripts. In the interview I speak in short sentences and adjust to the follow-up instead of delivering a memorized paragraph. If I notice myself performing, I stop and ask the interviewer whether that addressed their question.

**A lot of your impact happened through a team. How do you tell that story without either claiming team credit or disappearing into 'we'?**

I separate team context from personal contribution at the start: 'The team owned X; I personally led Y.' I describe my own decisions, disagreements, and trade-offs in the first person, and only use 'we' for shared outcomes. If I designed and drove a process, I say so; if I only supported, I say exactly what support I gave. That lets the interviewer see individual judgment inside a collaborative result, which is what they are actually hiring for.

## Worked example

A strong answer sounds like: 'In my last role, [the system I owned] started returning errors for a subset of requests after [a change I had shipped]. I first [immediate containment action], then traced the failure to [specific cause]. I fixed it by [your change], and error rates returned to baseline. The mistake I made was [a specific planning or review gap]. I now [process change you actually made].' This shape works because it opens with a concrete situation the interviewer can probe, uses 'I' only for decisions the speaker made, gives a checkable result, and converts the flaw into a reusable process change. It also creates a natural follow-up about the process change rather than leaving the interviewer to ask whether the candidate blamed someone.

## Common traps

- Reciting a memorized answer word-for-word and then freezing when a follow-up breaks from the script.
- Using 'we' so consistently that the interviewer cannot identify which decisions were the candidate's.
- Choosing the most technically impressive project instead of the experience that best demonstrates the question's signal.
- Claiming no mistakes or failures, which reads as lack of self-awareness and ends the story before any learning is shown.

</details>

---

## 3. Unsupervised Learning · flash · Easy

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

## 4. Regularization · output · Easy

*ai · gate confidence 0.85*

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

Regularization is any modification to a learning algorithm that reduces generalization error by constraining or perturbing the model rather than by fitting the training data better. In neural networks the common forms are L1 and L2 weight penalties, which add a function of the weights to the loss; dropout, which randomly disables units during training; and early stopping, which halts optimization before the training loss reaches its minimum. These changes shrink the effective hypothesis space or add noise so the model cannot memorize training examples.

## Why interviewers ask this

Interviewers use regularization to test whether you understand overfitting as a capacity problem and know the mechanism behind each technique, not just the names. They want to see you can choose a regularizer, explain training-versus-inference differences, and reason about sparsity and optimization. A candidate who knows L2 and weight decay diverge under Adam signals deeper optimization knowledge.

## The core idea

The core idea is to trade a little training fit for better validation performance. L1 adds the absolute value of each weight, and its constant-magnitude gradient can push irrelevant weights exactly to zero. L2 adds the squared weight, which shrinks all weights continuously and rarely reaches zero. Dropout forces redundant representations by randomly removing units and scaling the survivors during training. Early stopping keeps parameters closer to their initialization by limiting the number of optimization steps. In plain SGD, L2 is equivalent to weight decay, but under adaptive optimizers such as Adam the two differ, so AdamW applies decoupled weight decay separately.

## Key points

- L1 regularization adds λ times the sum of absolute weights to the loss; its constant-magnitude gradient can push many weights exactly to zero, producing sparse models.
- L2 regularization adds λ times the sum of squared weights to the loss and shrinks all weights toward zero, but rarely to exactly zero.
- For standard SGD, L2 regularization is equivalent to weight decay; in adaptive methods like Adam they diverge because L2 is scaled by the preconditioner, so AdamW decouples weight decay.
- Dropout randomly sets units to zero with probability p during training and scales survivors by 1/(1-p); at inference the full network is used without dropout.
- Early stopping halts training when validation loss stops improving, and weights from the lowest-validation-loss epoch are typically restored.

## Your 60-second answer

Regularization is a set of techniques for reducing overfitting by constraining model complexity. For neural networks, the main ones are L1, L2, dropout, and early stopping. L1 adds the absolute values of the weights to the loss; its constant gradient can drive irrelevant weights exactly to zero, producing a sparse model. L2 adds the squared weights, which shrinks all weights toward zero but rarely to zero. In standard SGD that L2 penalty is equivalent to weight decay, but under Adam they behave differently, which is why AdamW applies decoupled weight decay. Dropout randomly drops units during training and scales the survivors, then uses the full network at inference. Early stopping halts training when validation error stops improving. The trade-off is bias: too much regularization underfits, so the penalty strength, dropout probability, and patience must be tuned.

## If they dig deeper

**What is the difference between L1 and L2 regularization?**

L1 adds a penalty proportional to the sum of absolute weight values, so its gradient has constant magnitude and can push some weights exactly to zero. L2 adds a penalty proportional to the sum of squared weights, so its gradient is proportional to the weight itself; it shrinks large weights more aggressively but usually never removes any weight completely.

**Why does L1 regularization produce exact zeros while L2 does not?**

For a small weight, L1 still applies a nonzero penalty gradient, so the optimizer can reduce the weight all the way to zero if that lowers the total objective. L2's penalty gradient vanishes as the weight approaches zero, so the optimizer sees less and less pressure to continue shrinking it exactly to zero.

**How does dropout behave during training versus inference?**

During training, dropout randomly sets each unit to zero with probability p and scales the remaining units by 1/(1-p), so the expected activation stays the same. At inference, dropout is disabled and the full network is used, which avoids adding noise to predictions and makes inference faster.

**Is early stopping really a form of regularization?**

Yes. By stopping optimization when validation loss stops improving, early stopping limits how far the parameters move from their initialization and from the high-capacity solutions that fit training noise. It does not add a penalty to the loss, but it still reduces variance on unseen data.

**Why are L2 regularization and weight decay not equivalent in Adam?**

In plain SGD, the L2 gradient penalty is scaled by the same learning rate as the weight decay step, so they are equivalent. In Adam, the L2 penalty is divided by the per-parameter adaptive preconditioner before being applied, so its effective strength varies per weight. Decoupled weight decay subtracts a constant fraction of the weight directly before the Adam update, producing uniform shrinkage; this distinction is the motivation for AdamW.

## Worked example

Consider two weights w1=4.0 and w2=0.005, with learning rate 0.01 and regularization λ=0.1, ignoring the data gradient for one step. Under L2, w2 is multiplied by (1 - 0.01 * 2 * 0.1) = 0.998 each step: it becomes 0.00499 and, even after many steps, approaches but never reaches zero. Under L1, w2 loses 0.01 * 0.1 = 0.001 per step, so after five steps it hits exactly zero. L1's constant penalty can zero small weights, while L2 shrinks large weights more aggressively relative to their magnitude but preserves them.

## Common traps

- Saying L2 regression forces weights to exactly zero; it only shrinks them toward zero.
- Equating L2 regularization and weight decay without mentioning the optimizer; under Adam they diverge, and AdamW decouples them.
- Leaving dropout enabled at inference or forgetting the 1/(1-p) scaling during training, which changes expected activations.
- Tuning regularization by watching only training loss; the point is to improve validation performance, so training loss alone misleads.

</details>

---

## 5. Recommendation Systems · typed · Hard

*ai · gate confidence 0.85*

**Question**

How would you design a video recommendation system?

**Reference answer**

First define the objective, such as predicted watch time or completion, and log user-video interaction data. Build candidate sources including collaborative embeddings, content similarity, trending, and previously watched series. A ranker scores the candidates with features like user genre affinities, item age, predicted watch time, and diversity constraints, then returns the top items. Evaluate offline with held-out interaction data and online with A/B tests on watch time and retention.

**Graded on**

- Define objective and log interaction data
- Use hybrid candidate sources: collaborative embeddings, content similarity, trending, series
- Ranker uses richer engagement and diversity features
- Evaluate offline and online with A/B tests

<details><summary>The lesson this came from</summary>

A recommendation system predicts which items a user is most likely to engage with from a catalog, then ranks a small subset for display. The core approaches differ by signal: content-based filtering scores items by similarity between item attributes and a user profile built from the user's own history; collaborative filtering scores items using patterns across many users' interactions, such as user-user or item-item similarity; hybrid systems combine both. Production systems often split the work into candidate generation, which reduces millions of items to hundreds, and ranking, which orders those candidates with richer features.

## Why interviewers ask this

The interviewer is testing whether you can choose the right recommendation approach under data and cold-start constraints, and whether you can design a retrieval-plus-ranking pipeline that stays fast as the catalog grows. The question often appears for video feeds, product recommendations, or friend suggestions, where the real challenge is balancing relevance, novelty, and latency.

## The core idea

All recommenders are ranking systems: they reduce a large catalog to an ordered list. Content-based filtering uses item features and one user's own history, so it works for new items but depends on feature quality and can become narrow. Collaborative filtering learns from the interaction matrix across many users, so it needs little domain knowledge but suffers cold starts for new users and items. Hybrid recommenders combine both signals, which is what most production systems do. At scale, a two-stage design dominates: a cheap candidate generation stage retrieves a few hundred or thousand items, then a more expensive ranker scores only those candidates to produce the final top-n.

## Key points

- Content-based filtering scores items by similarity between item attributes and a user profile built from their own history; it avoids item cold start but requires domain knowledge and tends toward overspecialization.
- Collaborative filtering learns from the interaction matrix across users and items using techniques such as user-user similarity, item-item similarity, or matrix factorization; it needs no item metadata but cannot handle brand-new users or items.
- Hybrid recommenders combine content and collaborative signals, typically by feeding both into a single ranker or blending multiple candidate generation sources.
- Large-scale production systems usually use two stages: candidate generation narrows millions of items to hundreds or thousands, then a ranking model with richer features orders the final recommendations.
- Embeddings enable scalable nearest-neighbor retrieval by representing users and items in a shared vector space, but their quality depends on training data and the chosen objective.

## Your 60-second answer

A recommender system reduces a large item catalog to a small ordered list a user is most likely to engage with. The classic split is content-based, collaborative, and hybrid. Content-based scoring compares item attributes with a user profile built from that user's own past activity; it avoids cold start for new items but needs good features and can become narrow. Collaborative filtering uses the interaction matrix across many users and items, with user-user or item-item similarity, matrix factorization, or neural embeddings; it needs little domain knowledge, but new users and new items have no interaction history. Hybrid methods combine both, which is what most production systems do. At scale, you usually don't score every item: you run a candidate-generation stage to retrieve a few hundred items, then a ranker with richer features to produce the final top-n. The main trade-off is relevance versus cold-start coverage and latency.

## If they dig deeper

**What is the difference between content-based and collaborative filtering?**

Content-based filtering scores items by comparing item attributes to a profile built from that user's own activity, so it can recommend a new item as soon as its metadata exists but requires good features. Collaborative filtering learns from the interaction matrix across users and items, so it needs no domain knowledge but cannot score a brand-new user or item until some interactions exist.

**How do you handle cold start for new users and new items?**

For new items, use content or metadata embeddings and hybrid scoring so they can still be retrieved without interaction history. For new users, fall back to popularity, trending, or explicit preference capture, and run exploration to collect early signals. Blend the fallback with learned models as data accumulates.

**Why do production recommenders split candidate generation and ranking?**

Because scoring millions of items with a rich model is too slow and expensive. Candidate generation cheaply reduces the catalog to a few hundred or thousand items using approximate nearest neighbor or rule-based sources; the ranker then applies expensive features and a more accurate model only to that small set. This also lets teams iterate on retrieval and ranking independently.

**How would you design a video recommendation system?**

Define the objective first, such as predicted watch time or completion, and log training data from user-video interactions. Build candidate sources: collaborative embeddings, content similarity, trending, and previously watched series. A ranker scores candidates with features like user genre affinities, item age, predicted watch time, and diversity constraints, then returns the top items. Evaluate offline with held-out interaction data and online with A/B tests on watch time and retention.

**How do embedding-based collaborative filtering methods work and what are their main limitations?**

They map users and items into a shared vector space, usually with a two-tower model or matrix factorization, and retrieve nearest neighbors by vector similarity. This makes retrieval scalable with approximate nearest neighbor indexes but the embeddings can suffer from cold start, popularity bias, feedback loops, and staleness; they also need periodic retraining to capture new items and changing behavior.

## Worked example

Suppose a catalog has 10 million videos. Candidate generation uses a two-tower model that embeds a user and each video into a 128-dimensional space. For a returning user, the system retrieves the 500 nearest video embeddings by approximate nearest neighbor under cosine similarity; this runs in milliseconds because the index pre-partitions the embedding space. The ranker then scores those 500 candidates with a gradient-boosted model using features like genre affinity, video age, predicted watch time, and a collaborative-filtering score. It orders by predicted probability of watching at least 70% of the video, multiplies by predicted watch-time weight, and the top 20 are shown. A brand-new video has no interaction history, so the collaborative embedding is unavailable; content embeddings from its tags and description let it still enter candidate generation and be ranked by metadata features.

## Common traps

- Saying collaborative filtering requires no domain knowledge and ignoring its cold-start problem and popularity bias.
- Treating a two-stage recommender as one giant model that scores the full catalog; this misses why candidate generation exists.
- Recommending by raw similarity only, without considering business constraints like freshness, diversity, or prohibited items.
- Overfitting to clicks when the product goal is watch time, completion, or another engagement metric, so the objective does not match the real outcome.

</details>

---

## 6. Dealing with ambiguity · mcq · Easy

*behavioral · gate confidence 0.85*

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

## 8. Object-Oriented Programming Principles · flash · Easy

*cs · gate confidence 0.85*

**Question**

What is polymorphism in Java primarily?

**Reference answer**

Polymorphism in Java is primarily dynamic dispatch: a call through a base type or interface invokes the overridden method of the actual object at runtime.

**Graded on**

- dynamic dispatch
- overridden methods
- actual object type

<details><summary>The lesson this came from</summary>

Object-oriented programming organizes code into classes that combine state (fields) and behaviour (methods). Encapsulation restricts direct access to state and exposes controlled operations; inheritance lets a subclass acquire and override superclass members; abstraction hides implementation behind interfaces or abstract classes; polymorphism lets one reference type invoke behaviour that is dispatched to the actual object's implementation.

## Why interviewers ask this

Interviewers use this to check whether you can do more than recite definitions: they want to see you map each principle to concrete Java mechanisms (private fields, getters, extends, @Override, interface vs abstract class) and discuss trade-offs such as tight coupling from inheritance or leaky abstractions. They also probe the difference between abstraction (what) and encapsulation (how), a common confusion.

## The core idea

The four principles work together. Encapsulation is the mechanism: fields are private, access is through methods that can validate and preserve invariants. Inheritance should model an is-a relationship and enable override points; composition is often safer for reuse. Polymorphism is the payoff: code written against a base type or interface works with any subtype, and Java dispatches overridden methods dynamically at runtime. Abstraction separates what callers depend on from how a class implements it; in Java, interfaces define pure contracts while abstract classes provide partial implementations. A strong answer names the Java feature behind each principle and states the trade-off.

## Key points

- In Java, encapsulation is enforced with access modifiers: private fields plus public/protected methods control how state changes.
- Inheritance creates an is-a relationship; Java supports single class inheritance, but multiple interface implementation, avoiding the diamond problem for state.
- Polymorphism in Java is primarily runtime (dynamic dispatch) through overridden methods, while overloaded methods are resolved at compile time.
- Abstraction is achieved with abstract classes (partial implementation, can have constructors/state) and interfaces (a contract; since Java 8 interfaces can also have default and static methods).
- Encapsulation hides how and protects data; abstraction hides implementation complexity and exposes what.

## Your 60-second answer

Object-oriented programming is a paradigm built on objects that combine data and methods. Its four core principles are encapsulation, inheritance, polymorphism, and abstraction. Encapsulation means hiding internal state behind a controlled interface; in Java, I make fields private and expose getters or setters that validate. Inheritance lets a subclass reuse and override superclass behavior, but I prefer composition when there is no true is-a relationship. Polymorphism lets code written against a base type or interface work with any subtype because Java dispatches overridden methods at runtime. Abstraction means depending on a contract, like an interface or abstract class, instead of a concrete implementation. The main trade-off is that inheritance creates coupling between parent and child, so I use it for stable, well-understood hierarchies and interfaces for flexibility.

## If they dig deeper

**How is encapsulation different from abstraction?**

Encapsulation is a mechanism: it bundles fields with the methods that manipulate them and restricts direct access, typically with private fields and public mutators. Abstraction is a design outcome: it exposes only the essential behaviour through an interface or abstract class and hides implementation details. Encapsulation protects how state changes; abstraction hides what the caller does not need.

**When would you use an abstract class instead of an interface in Java?**

Use an abstract class when related subclasses should share instance state, constructors, or a partial implementation that cannot be expressed well in an interface. Use an interface when unrelated classes need to implement the same capability. Since Java 8 interfaces can have default and static methods with bodies, but they still cannot store per-instance state, shared state remains a reason for an abstract class.

**What is the diamond problem and how does Java handle it?**

The diamond problem arises when a class inherits from two superclasses that define the same method or field, so the compiler cannot decide which one to use. Java avoids it for classes by forbidding multiple class inheritance: a class can extend exactly one superclass. Multiple interface inheritance is allowed; if two interfaces provide default methods with the same signature, the implementing class must override the method and resolve the conflict. State ambiguity is avoided because interfaces cannot have instance fields, only static final constants.

**Explain static versus dynamic polymorphism with an overload and an override.**

Static polymorphism in Java is overloaded methods: signature includes name and parameter types, so the compiler chooses the method at compile time based on argument types. Dynamic polymorphism is overridden methods: the call is dispatched at runtime to the implementation of the actual object even when the reference type is a superclass or interface. For instance, print(Object o) has multiple overloads selected at compile time, while toString() on an Object reference invokes the subclass override at runtime.

**How does the Liskov Substitution Principle constrain inheritance?**

LSP requires that a subclass be usable in any context that expects a superclass without surprising behavior. Formally, an overriding method cannot strengthen preconditions (reject inputs the superclass accepts), weaken postconditions (return results weaker than the superclass promises), or violate invariants of the superclass. If a subclass would need to throw unexpected exceptions or change the meaning of a method, the hierarchy is not a true is-a relationship and composition should be preferred.

## Worked example

Take a BankAccount with a private double balance and a public deposit(double amount) that throws IllegalArgumentException if amount <= 0. Suppose a SavingsAccount extends BankAccount and overrides monthlyFee() to return 5.0, while a CheckingAccount overrides it to return 10.0. A method chargeFees(List<BankAccount> accounts) iterates and calls account.monthlyFee(); when the list contains both subtypes, the JVM invokes each object's own override. The balance field remains encapsulated because the only mutations go through deposit and withdraw, which validate amounts and prevent a negative balance. For example, withdraw(30) when balance is 100 leaves 70, while withdraw(150) is rejected. The caller sees a BankAccount contract, so it is abstracted from concrete fee calculations. This single invocation shows inheritance (shared balance handling), abstraction (caller depends on type), and dynamic polymorphism (same call different implementations).

## Common traps

- Treating abstraction and encapsulation as synonyms: abstraction is about hiding implementation complexity behind a contract; encapsulation is about restricting direct access to state.
- Claiming Java supports multiple inheritance for classes because it allows multiple interfaces; classes extend one superclass, and default method conflicts still require explicit resolution.
- Saying interfaces are always 100% abstract without noting that since Java 8 default and static methods can have bodies.
- Reaching for inheritance as the default reuse mechanism; without an is-a relationship, inheritance couples subclasses to superclass internals and is usually worse than composition.

</details>

---

## 9. Sliding Window · typed · Medium

*dsa · gate confidence 0.85*

**Question**

What general property must a problem have for sliding window to be correct, and what limitation follows from that?

**Reference answer**

Sliding window requires a contiguous sequence and validity that is monotonic as the window expands or shrinks. It therefore does not apply to non-contiguous subsequences or validity conditions that can oscillate as more elements are added.

**Graded on**

- The window must be contiguous
- Validity must change monotonically with expansion or shrinking
- Non-contiguous or non-monotonic validity is out of scope

<details><summary>The lesson this came from</summary>

Sliding window maintains two boundaries over a contiguous sequence, typically a left and right pointer. The right pointer adds an element and updates incremental state; the left pointer removes an element when the window must shrink. For fixed-size windows, width stays k; for variable-size windows, the shrink rule depends on whether the problem seeks a longest valid window or a shortest valid window. It avoids rescanning subarrays and reduces many O(n^2) solutions to O(n).

## Why interviewers ask this

Interviewers ask sliding window problems to test whether you can recognize a contiguous subarray/substring constraint and maintain correct state as the window moves. Real questions such as Minimum Window Substring, Sliding Window Maximum, and Longest Substring Without Repeating Characters appear at companies including Lyft, Snap, Snowflake, Citadel, and Walmart Labs. The focus is on O(n) correctness, not brute force.

## The core idea

Keep one pointer expanding and another pointer shrinking. For longest-valid-window problems, expand the right side while the constraint holds, and shrink the left only when it breaks. For minimum-valid-window problems, expand until the window first becomes valid, then shrink from the left while the window still satisfies the constraint, recording each valid minimum. Maintain aggregate data such as a sum, frequency map, or monotonic deque that can be updated in O(1) when the boundaries move. For Sliding Window Maximum, a monotonic deque stores indices in decreasing value, keeping the current maximum at the front; remove the front when it leaves the window and pop smaller values from the back before adding a new index.

## Key points

- Fixed-size windows keep exactly k elements and update an aggregate in O(1) per slide, for example sum = sum - arr[left] + arr[right].
- For longest-valid-window problems, shrink the left pointer only when the current window violates the constraint; for minimum-valid-window problems, shrink left while the window remains valid.
- Longest Substring Without Repeating Characters uses a hash map from character to last index and moves left to last_index + 1 only when last_index >= left.
- Sliding Window Maximum uses a monotonic deque of indices in decreasing value; before pushing a new index, pop from the back while those values are <= the new value, and drop the front when it is outside the window.
- A correct sliding window is O(n) even with an inner loop, because each index enters and leaves the window at most once.

## Your 60-second answer

Sliding window is a two-pointer technique for finding an optimal contiguous subarray or substring in O(n). The right pointer expands the window, and the left pointer contracts it based on validity. For a longest valid window, expand while the constraint holds and shrink only when it breaks; for a minimum valid window, expand until the constraint is satisfied, then shrink while it remains satisfied. The key is incremental state: a running sum, frequency map, or monotonic deque, so moving a boundary costs constant time instead of rescanning the window. Fixed-size windows keep width k. For Sliding Window Maximum, a monotonic deque keeps indices in decreasing value, so the front is always the max for the current window. The trade-off is that sliding window only applies to contiguous subsequences with monotonic validity. If the array has negative values in a sum constraint, the standard two-pointer shrink rule can fail.

## If they dig deeper

**How do you implement a fixed-size window, such as maximum sum of k consecutive elements?**

Compute the sum of the first k elements. Then for each next index, add arr[right] and subtract arr[left] to maintain the sum in O(1), updating the answer after each slide.

**How does the hash map avoid counting a repeat that is outside the current window?**

Store the last index where each character appeared. When the right character is seen again, check that stored index against left; only if last_index >= left does the repeat lie inside the window, so set left = last_index + 1. Otherwise the earlier occurrence is already excluded and left does not move.

**Why does Minimum Window Substring shrink while valid instead of shrinking only when invalid?**

Because the goal is the shortest window. You first expand right until all required characters are present, then each time validity holds, you can try to move left forward and record the smaller candidate. Shrinking only when invalid would skip valid shorter windows.

**Why is a monotonic deque better than a max heap for Sliding Window Maximum?**

A heap gives the maximum in O(1) but each insert and delete is O(log k), and lazy deletion of out-of-window elements adds state. A monotonic deque gives O(1) amortised per index because each index is pushed and popped at most once, total O(n).

**Can you use standard sliding window for longest subarray with sum <= k if the array contains negative numbers? Why or why not?**

No. The shrink rule relies on the sum being monotone as the window expands: with non-negative values, adding an element never decreases the sum, so an over-limit window can be fixed by shrinking. With negative numbers, adding a negative value can bring a window back under the limit, so an invalid prefix does not imply all larger windows are invalid. You need prefix sums and an ordered structure instead.

## Worked example

For longest substring without repeating characters, take s = 'abcabcbb' with 0-based indices: a at 0, b at 1, c at 2, a at 3, b at 4, c at 5, b at 6, b at 7. Start with left = 0, an empty last-seen map, and best = 0. Process each right index. At right=3 the character 'a' was last seen at index 0; since 0 >= left, left becomes 1. At right=4, 'b' was last seen at index 1; since 1 >= left, left becomes 2. At right=5, 'c' was last seen at index 2, so left becomes 3. At right=6, 'b' was last seen at index 4, so left becomes 5. At right=7 the character is 'b' and its recorded last index is 6; since 6 >= left, left becomes 7, leaving a window of only the final 'b'. The best length stays 3, recorded from windows such as indices 3-5, which contain 'abc'. The answer is 3.

## Common traps

- Confusing the shrink rule between longest and minimum window problems, which reverses when the left pointer should move.
- Updating the longest-substring map without checking last_index >= left, so an old duplicate outside the window causes an unnecessary shrink and a wrong answer.
- Forgetting to pop the deque front when its index falls outside [left, right], letting a stale maximum from a previous window dominate the current one.
- Applying standard sliding window to a sum constraint over an array with negative numbers, where shrinking an invalid window does not monotonically restore validity.

</details>

---

## 10. Collections Framework · typed · Medium

*java · gate confidence 0.85*

**Question**

What is the core design principle of the Java Collections Framework, and why does it matter for algorithms?

**Reference answer**

The framework separates collection interfaces from concrete storage strategies, and utility algorithms operate on those interfaces. This lets the same sort, search, or wrapper method work across ArrayList, LinkedList, HashSet, and other implementations.

**Graded on**

- Interfaces define behavior, implementations define storage
- Algorithms operate on interfaces
- Same algorithm works across implementations

<details><summary>The lesson this came from</summary>

The Java Collections Framework is a unified architecture in java.util for representing and manipulating groups of objects. It provides core interfaces—Collection with List, Set, Queue, and Deque, plus the separate Map interface—and concrete implementations such as ArrayList, LinkedList, HashSet, TreeSet, HashMap, and TreeMap. The framework also includes utility algorithms in the Collections class for sorting, searching, shuffling, and creating unmodifiable or synchronized views.

## Why interviewers ask this

Interviewers ask about collections to test whether you can choose the right data structure under constraints like ordering, duplicates, null handling, and concurrency, and whether you understand the contracts behind equality, hashing, and comparison. They also probe knowledge of common implementations and the Collections utility methods, because real code often fails on subtle data-structure choices.

## The core idea

The framework separates interfaces (what operations a collection supports) from implementations (how data is stored and accessed) and from algorithms (reusable methods in Collections). Deciding which collection to use is driven by the needs: List preserves insertion order and permits duplicates; Set rejects duplicates; Queue/Deque model FIFO, LIFO, or priority order; Map stores key-value pairs. Ordering and uniqueness are enforced through equals/hashCode for hash-based collections and through compareTo/Comparator for sorted collections. Complexity profiles differ: ArrayList gives O(1) indexed access but O(n) middle insertion; HashMap gives O(1) average lookup with no order; TreeMap gives O(log n) operations while keeping keys sorted. A strong candidate knows both the contract of each interface and the performance and null behavior of the main implementations.

## Key points

- The Java Collections Framework includes the Collection hierarchy (List, Set, Queue, Deque) and the separate Map interface, with concrete classes like ArrayList, LinkedList, HashMap, TreeMap, HashSet, and TreeSet.
- ArrayList provides O(1) random access and O(n) insertion/removal from the middle, while LinkedList provides O(1) insertion/removal at the ends and O(n) random access.
- HashMap and HashSet offer O(1) average contains/get/put with a good hash function, but make no order guarantee; TreeMap and TreeSet are O(log n) for those operations and maintain sorted order.
- Hash-based collections rely on correct equals() and hashCode(); TreeMap/TreeSet rely on Comparable or a supplied Comparator and reject null keys/elements under natural ordering.
- Collections is a utility class with static methods like sort, binarySearch, reverse, shuffle, unmodifiable wrappers, and synchronized wrappers; it is distinct from the Collection interface.

## Your 60-second answer

The Java Collections Framework is a set of interfaces, implementations, and algorithms in java.util for storing and manipulating groups of objects. The core interfaces are Collection with List, Set, Queue, and Deque, plus the separate Map interface. Concrete classes provide different trade-offs: ArrayList gives O(1) indexed access but O(n) middle insertion; LinkedList gives O(1) insertion at the ends but O(n) random access; HashMap gives O(1) average get/put with no order; TreeMap gives O(log n) operations while keeping keys sorted. Map stores key-value pairs and exposes keySet, values, and entrySet views. The Collections utility class provides algorithms like sort, binarySearch, reverse, and shuffle. So the choice depends on whether you need order, duplicates, fast lookup, sorted iteration, or null tolerance. The framework also offers unmodifiable and synchronized wrapper views through Collections.

## If they dig deeper

**What is the difference between Collection and Collections?**

Collection is the root interface in java.util for groups of elements and is extended by List, Set, and Queue; Collections is a utility class with static methods like sort, binarySearch, reverse, and unmodifiableList that operate on Collection instances.

**When would you choose HashSet instead of TreeSet?**

Use HashSet when you need O(1) average add/remove/contains and do not care about iteration order; it permits one null element. Use TreeSet when you need elements kept sorted by natural order or a Comparator, and accept O(log n) operations; under natural ordering it rejects null.

**How do you make a collection read-only or thread-safe?**

For read-only, wrap with Collections.unmodifiableList, unmodifiableSet, or unmodifiableMap to get a view that throws UnsupportedOperationException on mutation. For thread safety, Collections.synchronized* wrappers synchronize each method, but compound operations still need external synchronization; java.util.concurrent collections like ConcurrentHashMap offer better concurrency.

**Why should keys in a HashMap be immutable?**

If the key's hash code changes after insertion, the entry may no longer be found in its original bucket, so containsKey or get fails even though the object is present. Immutable keys like String and Integer preserve the bucket placement and are safe to use.

**How does OpenJDK 8+ HashMap handle hash collisions and resizing?**

It uses separate chaining: each bucket holds a linked list of nodes with equal hash. When a bucket's list reaches the treeification threshold (8 entries) and the table capacity is at least 64, that bin is converted to a balanced tree to keep worst-case operations O(log n) instead of O(n). When the number of entries exceeds load factor times capacity (default 0.75), the table is resized to roughly double capacity and existing entries are rehashed.

## Worked example

Consider designing an LRU cache with fixed capacity. A standard design uses a HashMap<K, Node> for average O(1) lookup by key and a doubly linked list of Node objects to maintain recency order. On get(key), if the key is present, the cache unlinks its node and moves it to the head in O(1) because the node already holds references to previous and next. On put(key, value), a new node is added at the head; if the size exceeds capacity, the tail node is removed and its key deleted from the map. The map provides O(1) average access, and the list updates are constant-time pointer changes. If a TreeMap were used instead, lookup would be O(log n); if only an ArrayList were used, evicting the least recently used element would be O(n) because of shifting.

## Common traps

- Assuming Map extends Collection: Map is a separate interface in java.util, not a subinterface of Collection.
- Using mutable objects as HashMap/HashSet keys and then modifying the fields used by equals() or hashCode(), which can make the element unfindable.
- Expecting HashSet or HashMap iteration to be insertion-ordered or sorted; HashSet/HashMap have no order guarantee, and LinkedHashSet/LinkedHashMap/TreeSet/TreeMap are needed for those behaviors.
- Using Collections.sort on a Set or assuming PriorityQueue's iterator returns elements in priority order; sort requires a List, and PriorityQueue iteration order is not the priority order.

</details>

---

## 11. Hotel Management System Design · flash · Easy

*lld · gate confidence 0.85*

**Question**

What is the role of the CancellationPolicy interface in the reservation state machine?

**Reference answer**

It decouples cancellation rules, such as the 24-hour window, from the Reservation entity by providing a canCancel method that can be swapped without changing the state machine.

**Graded on**

- Decouples policy from entity
- canCancel method
- Allows different rules

<details><summary>The lesson this came from</summary>

A hotel management system LLD models a hotel as a set of room types and physical rooms, each with status and inventory; reservations as stateful bookings that enforce check-in, check-out, and cancellation policies; and guest services as billable line items attached to a reservation's folio. The main mechanism is a Reservation aggregate that transitions between states, a RoomCatalog that answers availability by checking overlap against active reservations, and a Folio that accumulates room, food, amenity, and service charges until payment. Housekeeping tasks are logged against room status changes. This design separates configuration (rooms, rates), transactions (bookings, payments), and operational logs.

## Why interviewers ask this

The interviewer is testing whether you can identify entities and invariants for a real stateful workflow: preventing double bookings, enforcing a 24-hour cancellation window, keeping an auditable bill, and handling multiple payment methods without coupling. It also reveals whether you model behavior over time (availability is a query over date ranges) instead of a static flag.

## The core idea

The Reservation is the central aggregate: it can be Confirmed, CheckedIn, CheckedOut, or Cancelled, and each transition checks a rule (e.g., cancel only if now is more than 24 hours before check-in). Room availability must be derived by querying non-cancelled reservations whose date ranges overlap the requested stay; a room_id plus status alone is insufficient because availability is time-dependent. All monetary charges belong to a Folio attached to a reservation; room service, food, amenities, and room rate line items are appended immutably so the bill can be audited. Payment is modeled behind a strategy interface so Cash, Check, and Card settle the same folio without branching on payment type. The booking operation must be atomic; checking availability then inserting as a separate step is a race. A housekeeping log is append-only and records room status transitions and task assignments.

## Key points

- A room is unavailable for a requested date range if any non-cancelled reservation's [checkIn, checkOut) interval overlaps it.
- Cancellation returns a full refund only when it occurs more than 24 hours before the check-in date; otherwise the policy may charge a penalty or deny cancellation.
- Reservation status should be an explicit state machine (e.g., Confirmed -> CheckedIn -> CheckedOut, with Cancelled possible before check-in), not inferred from dates.
- Folio line items are immutable; refunds and discounts are recorded as counter-line items so the original charge history remains auditable.
- Payment is polymorphic (credit card, check, cash) and acts against the folio, not against a room or reservation total field.

## Your 60-second answer

I'd model this as four core groups: inventory, reservations, folios, and operations. A room belongs to a room type like standard or suite, and has a current status—available, occupied, dirty, or out of order. Availability isn't a boolean; it's computed by checking whether any confirmed or checked-in reservation overlaps the requested dates. The reservation is a state machine: confirmed to checked in to checked out, with cancellation allowed only before the policy deadline, in this spec more than 24 hours before check-in. All charges—room nights, food, amenities—are appended as line items to a folio attached to the reservation, so the bill stays auditable. Payment is a strategy for cash, card, or check that settles the folio. Housekeeping gets a task log when a room becomes dirty at checkout. The main trade-off is that deriving availability from date ranges is precise but requires careful transaction or constraint handling to avoid double bookings.

## If they dig deeper

**What are the main classes or entities in this design?**

Hotel, RoomType, Room, Guest, Reservation, Folio, FolioLineItem, Payment, RoomServiceItem, Amenity, HousekeepingLog, and NotificationService. RoomType captures category and base rate; Guest holds contact and identity; Reservation links one or more rooms, a guest, dates, and a folio.

**How do you prevent two guests from booking the same room for overlapping dates?**

The booking operation must check availability and insert the reservation atomically. In a relational database, that means a transaction with an appropriate isolation level or a database constraint such as PostgreSQL's exclusion constraint on room_id with a date range; if a conflicting row already exists the insert fails. In a distributed system you would use a per-room lock or a consensus-based reservation service.

**How do you represent the 24-hour cancellation policy so it can change later?**

Define a CancellationPolicy interface with a method like canCancel(reservation, now). The default implementation returns true when now is more than 24 hours before the check-in timestamp. The Reservation holds a reference to the policy or a policy type, so another hotel can inject a 48-hour or non-refundable policy without changing the Reservation state machine.

**How do you handle room rates that change seasonally without corrupting old bills?**

RoomType or Room has a list of RoomRate entries with effective from/to dates and an amount. When a reservation is made, the system resolves the applicable rate for each night and copies those amounts onto the folio as snapshot line items. Future rate changes do not affect existing reservations because the charges reference the snapshot, not the current rate table.

**How would you make check-in idempotent if a guest retries the same request after a network timeout?**

Generate an idempotency key with each reservation or check-in request and store it on the reservation. On receipt, first look up the key: if it already exists, return the existing result without changing state. Otherwise perform the state transition in a transaction that compares the current status before updating, so a concurrent duplicate sees the status as already checked in and becomes a no-op.

## Worked example

A search for Room 101 for Oct 1 to Oct 2 fails because an existing reservation checks out Oct 2, overlapping the night of Oct 1. The system treats check-out as exclusive; the room is not offered for an Oct 2 check-in until housekeeping marks it available. For Room 102 at $100/night, an Oct 1-3 booking creates a Folio with two night charges totaling $200. If the guest orders breakfast for $15 and an amenity for $5, the folio total becomes $220. Payment by card settles the folio as a $220 payment, and the Reservation transitions to CheckedOut.

## Common traps

- Modeling room availability as a boolean field on Room; availability depends on dates and reservation status.
- Storing only an outstanding balance as a mutable number on a reservation, so refunds and service charges cannot be audited.
- Forgetting to make booking atomic and checking availability before inserting in a separate race-prone step.
- Coupling payment details into the reservation or room instead of using a folio-level payment strategy.

</details>

---

## 12. Ride Sharing Service Design · typed · Medium

*lld · gate confidence 0.85*

**Question**

How is pricing calculated in a ride-sharing service, and how is double charging prevented?

**Reference answer**

Before the ride, the pricing service returns a quoted estimate: base fare plus per-mile and per-minute rates adjusted by a surge multiplier. After completion, the final fare is recalculated from actual route distance and time, and the payment charge uses an idempotency key so retries do not double-bill the rider.

**Graded on**

- Quote includes base, per-mile, and per-minute rates
- Surge multiplier is applied
- Final fare is recalculated from actual distance and time
- Idempotency key prevents duplicate charge

<details><summary>The lesson this came from</summary>

A low-level design for a ride-sharing service models the core domain objects—Rider, Driver, Trip, Location, and Fare—and the interactions among them. It specifies a geospatial index for finding nearby available drivers, a time-boxed dispatch flow where a driver's acceptance commits the trip, and a trip state machine. It also defines pricing calculation and the concurrency controls needed for correct assignment and payment.

## Why interviewers ask this

The interviewer is testing whether the candidate can decompose a multi-entity workflow into clean service boundaries and state transitions. They also want to see how the candidate handles concurrency, driver availability, and failure cases such as duplicate offers or timed-out dispatches. Strong answers show explicit state machines and atomic transitions rather than vague 'assign closest driver' logic.

## The core idea

A ride request is matched by querying a geospatial index such as geohash cells or a grid for nearby drivers whose status is AVAILABLE. The system does not hard-assign the closest driver before acceptance; it sends a short-lived offer with a timeout, sometimes to one candidate at a time, and only the driver's acceptance transitions the driver from OFFER_PENDING to ON_TRIP and the trip to DRIVER_ASSIGNED. If an offer times out, the driver returns to AVAILABLE and the service tries the next candidate or expands the search radius. Pricing is estimated before the ride and finalized after completion using actual distance and time. Idempotency keys and conditional status updates guard against duplicate rides, double assignment, and double payment.

## Key points

- A geospatial index such as geohash or a grid partitions driver locations so nearby-driver queries do not scan the entire fleet.
- Dispatch is offer-based: the system sends a time-boxed offer and marks the driver OFFER_PENDING; only the driver's acceptance commits the driver to ON_TRIP and the trip to DRIVER_ASSIGNED.
- The trip state machine enforces allowed transitions such as SEARCHING to DRIVER_ASSIGNED to DRIVER_EN_ROUTE to PICKED_UP to COMPLETED, with cancellation possible at specific points.
- Pricing uses a quoted fare estimate before the ride and recalculates the final fare from actual route distance and time, applying a surge multiplier when demand exceeds supply.
- Idempotency keys and conditional status/version checks prevent duplicate ride requests, multiple drivers being committed to the same trip, and duplicate payment charges.

## Your 60-second answer

A ride-sharing design centers on a trip state machine and a dispatch service. A rider creates a ride request with pickup, dropoff, and an idempotency key. The pricing service returns a fare estimate, then matching starts. The matching service queries a geospatial index—usually geohash cells—for nearby drivers whose status is AVAILABLE. It sends a time-boxed offer to one or a few candidate drivers, not a hard assignment. Only when a driver accepts does the system transition that driver from OFFER_PENDING to ON_TRIP and the trip to DRIVER_ASSIGNED. If the offer times out, the service tries the next candidate or expands the search radius. This avoids committing a driver before acceptance. The main trade-off is latency versus utilization: offering to one driver at a time minimizes duplicate acceptances but can be slow; broadcasting to several drivers fills rides faster but requires reconciling multiple accepts.

## If they dig deeper

**How do you find nearby drivers efficiently?**

Use a geospatial index such as geohash or a grid. The service encodes the pickup location to a cell, queries that cell and its neighboring cells for drivers, filters by status=AVAILABLE, and ranks by estimated pickup distance. If too few candidates are found, it expands to the next ring of cells.

**What happens if no driver accepts an offer?**

After the offer timeout, the dispatch service marks the driver AVAILABLE again and tries the next candidate from the ranked list, or expands the search radius. If no driver accepts after a configured number of attempts, the request is cancelled or the rider is given a longer wait or a higher surge price.

**How do you prevent two different riders from being assigned the same driver?**

Driver records maintain a status and version. When dispatch sends an offer, it uses an atomic compare-and-set to move the driver from AVAILABLE to OFFER_PENDING, so a second concurrent dispatch cannot offer the same driver. On acceptance, the driver transitions from OFFER_PENDING to ON_TRIP; if the offer lease expired, the acceptance is rejected.

**How is pricing calculated?**

Pricing is computed as a quote before the ride: base fare plus per-mile and per-minute rates adjusted by a dynamic surge multiplier. The final fare is recalculated after trip completion using actual distance and time. Payment uses an idempotent charge so retries do not double-bill the rider.

**How do you make driver assignment and payment exactly-once when a node fails?**

Use idempotency and transactional state changes. Each ride request has an idempotency key with a unique constraint. Driver assignment is a compare-and-set on driver status and version; a crashed dispatcher relies on the offer lease timeout to release the driver. Payment charges use an idempotency key, and trip completion emits exactly one event via an outbox pattern so no duplicate completion or charge is processed.

## Worked example

A rider at (37.7749, -122.4194) requests a ride to (37.7847, -122.4094). Pricing quotes $18.50 using base $2.50 plus $1.80 per mile for 5.1 miles plus $0.35 per minute for 12 minutes, with a 1.3x surge. MatchingService computes geohash 9q8yy and scans its own cell plus eight neighbors, finding D1 0.4 miles away, D2 0.6 miles away, and D3 1.1 miles away. All are AVAILABLE. It sends a 15-second offer to D1 and marks D1 OFFER_PENDING. D1 does not accept; the lease expires and D1 returns to AVAILABLE. The service sends an offer to D2, who accepts at t+9 seconds. D2 transitions from OFFER_PENDING to ON_TRIP, and the trip moves from SEARCHING to DRIVER_ASSIGNED. After pickup and a 12.4-minute, 5.3-mile ride, the trip is COMPLETED and the final fare is recalculated to $18.90.

## Common traps

- Treating dispatch as an atomic assignment and marking the driver ON_TRIP before the driver accepts; this loses the acceptance window and makes timed-out offers impossible.
- Using a naive 'select closest driver and assign' without checking status and version, which can double-book a driver who already accepted another trip.
- Deriving driver status only from trip status instead of maintaining a separate driver availability state, causing stale or inconsistent views.
- Computing the fare only at the end without quoting an estimate, or failing to make the final charge idempotent so retries double-charge the rider.

</details>

---

## 13. DDL/DML/DCL/TCL · typed · Medium

*sql · gate confidence 0.85*

**Question**

What privilege boundary separates DDL from DML, and why does it matter?

**Reference answer**

DML requires table-level and sometimes column-level SELECT/INSERT/UPDATE/DELETE privileges on existing objects, while DDL requires broader object-creation rights such as CREATE on a schema or database. This separation lets application and reporting users modify rows without being able to change the schema.

**Graded on**

- DML uses table/column privileges
- DDL requires schema/database creation rights
- Separation supports least privilege

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

## 14. Constraints · mcq · Easy

*sql · gate confidence 0.85*

**Question**

Which of the following is a separate column requirement often grouped with SQL constraints, rather than one of the common declarative constraints?

**Options**

- PRIMARY KEY
- FOREIGN KEY
- CHECK
- NOT NULL

**Reference answer**

NOT NULL

**Graded on**

- Common declarative SQL constraints include PRIMARY KEY, FOREIGN KEY, UNIQUE, CHECK, and DEFAULT.
- NOT NULL is a separate column requirement that is often discussed with constraints.
- PRIMARY KEY, FOREIGN KEY, and CHECK are constraints enforced by the database on writes.

<details><summary>The lesson this came from</summary>

Constraints are declarative schema rules attached to columns or tables that the database engine enforces on every INSERT and UPDATE, rejecting any statement that would violate them. The common SQL constraints are PRIMARY KEY, FOREIGN KEY, UNIQUE, CHECK, and DEFAULT, with NOT NULL as a separate column requirement. A PRIMARY KEY gives a unique non-null row identifier; a FOREIGN KEY maintains a relationship to a primary or unique key in another table. DEFAULT is not an integrity check that rejects data, but it supplies missing or explicitly requested default values.

## Why interviewers ask this

Interviewers ask about constraints to see whether you can use the database for data integrity instead of relying only on application code. They also probe your understanding of the difference between primary key, unique, foreign key, and not null, and edge cases like null handling, cascade actions, and write-time costs. The common 'difference between primary and foreign key' question is a quick filter for schema design fundamentals.

## The core idea

Constraints move data integrity into the database engine, making invalid states impossible regardless of which application path wrote the row. The main types enforce different rules: PRIMARY KEY provides one non-null unique row identifier; UNIQUE blocks duplicate values but allows nulls; FOREIGN KEY guarantees each non-null child value points to an existing parent; CHECK rejects rows where a predicate is false; DEFAULT fills values when omitted or when DEFAULT is specified explicitly. These checks run on every write and often require indexes, so they are both an integrity guarantee and a performance decision.

## Key points

- A PRIMARY KEY uniquely identifies each row, is implicitly NOT NULL, and is limited to one per table; it usually creates a unique index.
- A FOREIGN KEY enforces referential integrity by requiring each non-NULL value to match a primary key or unique key in the referenced table; NULL is allowed unless the column is also NOT NULL.
- A UNIQUE constraint prevents duplicate non-NULL values; PostgreSQL and MySQL allow multiple NULLs, while SQL Server's unfiltered unique constraint permits just one NULL.
- CHECK rejects only rows where its expression evaluates to FALSE, so NULL results are allowed because `NULL > 0` is UNKNOWN.
- DEFAULT supplies a value when a column is omitted from an INSERT column list or when INSERT/UPDATE explicitly specifies the DEFAULT keyword for that column; omitted columns in UPDATE are left unchanged.

## Your 60-second answer

SQL constraints are declarative rules enforced by the database engine on every insert and update, so invalid data is rejected at the source rather than waiting for application checks. A primary key uniquely identifies each row, is implicitly not null, and there can be only one per table. A foreign key references a primary or unique key in another table, so each non-null child value must point to an existing parent row; null foreign keys are allowed unless not null is added. Unique constraints block duplicate non-null values, though null handling varies by engine. Check constraints reject rows where the expression is false, and defaults supply a value when a column is omitted or when DEFAULT is written explicitly. The benefit is guaranteed integrity across all code paths; the main cost is write-time checking and index maintenance, so the decision is about data-criticality versus throughput.

## If they dig deeper

**What is the difference between a primary key and a unique constraint?**

A primary key uniquely identifies each row, cannot contain NULL, and is limited to one per table. A unique constraint also prevents duplicates but can be created multiple times per table and allows NULLs under most engines; both create unique indexes. A primary key is the table's standard row identifier, while unique constraints guard alternate keys like usernames or emails.

**What happens when you delete or update a parent row referenced by a foreign key?**

The declared referential action controls it. RESTRICT or NO ACTION blocks the operation if matching child rows exist; CASCADE deletes or updates the child rows automatically; SET NULL or SET DEFAULT assigns NULL or the column default to child rows. Engines differ in which actions they support, especially ON UPDATE, so verify the target database.

**Why might a CHECK constraint such as price > 0 still allow a row with a NULL price?**

SQL CHECK constraints are satisfied when the predicate evaluates to TRUE or UNKNOWN, and any comparison with NULL is UNKNOWN. So `NULL > 0` is unknown and the row is accepted. To reject NULL, add `price IS NOT NULL` or declare the column NOT NULL.

**When does DEFAULT apply on INSERT versus UPDATE, and what does the DEFAULT keyword do?**

On INSERT, the default is used when the column is omitted from the column list or when the statement explicitly provides DEFAULT for that column. On UPDATE, omitting the column simply leaves its current value; the default applies only if the statement sets it to DEFAULT, as in `UPDATE t SET status = DEFAULT`. In all cases DEFAULT evaluates the column's default expression at statement time.

**What performance or concurrency costs do constraints introduce?**

Every INSERT/UPDATE must validate CHECK and foreign key constraints; UNIQUE and PRIMARY KEY constraints maintain an index, adding write overhead. Foreign key checks may acquire shared locks on the referenced parent row, which can cause blocking or deadlocks under concurrent writes. Cascading deletes can also amplify a single parent delete into many child writes, so constraints must be chosen with both integrity and access patterns in mind.

## Worked example

In PostgreSQL, define `dept(id integer PRIMARY KEY)` and `emp(id integer PRIMARY KEY, dept_id integer REFERENCES dept(id) ON DELETE SET NULL, email text UNIQUE, salary numeric CHECK (salary > 0), status text DEFAULT 'pending' NOT NULL)`. Insert department 1, then `INSERT INTO emp(id, dept_id, email, salary) VALUES (10, 1, 'ana@example.com', 100)` succeeds with `status` becoming `pending` because the column was omitted. A second insert with `email = 'ana@example.com'` fails with a unique violation, even though its employee id is different. An insert with `dept_id = NULL` and `salary = NULL` can succeed: foreign keys allow NULL and the check passes because `NULL > 0` is UNKNOWN, not false. `UPDATE emp SET status = DEFAULT WHERE id = 10` explicitly applies the default to an existing row, and deleting department 1 sets emp 10's `dept_id` to NULL.

## Common traps

- Saying a UNIQUE constraint rejects all NULLs; most engines allow multiple NULLs and SQL Server's unfiltered unique constraint allows one.
- Assuming every omitted UPDATE column is reset to its DEFAULT; DEFAULT only applies on UPDATE when the statement sets the column to DEFAULT.
- Believing CHECK constraints catch NULL values; CHECK passes on UNKNOWN, so NULLs can get past a simple comparison.
- Treating a foreign key column as automatically NOT NULL; standard SQL allows NULL foreign keys unless the column itself is declared NOT NULL.

</details>

---

## 15. Design a notification system · typed · Hard

*system_design · gate confidence 0.85*

**Question**

How do you handle machine failures in a notification worker system?

**Reference answer**

Leave messages unacknowledged until the provider call and tracker update both succeed, so the broker redelivers them if a worker dies. After the maximum retry count, move the message to a dead-letter queue. Keep WebSocket session state in a shared store such as Redis so another node can resume, and use multi-region replicas for availability.

**Graded on**

- ack only after provider call and tracker update
- broker redelivery after worker death
- dead-letter queue after max retries
- shared session state for WebSocket resume

<details><summary>The lesson this came from</summary>

A notification system is an asynchronous ingest-and-fan-out pipeline. Product services publish typed events; a notification service enriches them with user preferences and templates, then enqueues them on a message broker. Channel workers consume notifications and call external providers—APNS for iOS push, FCM for Android, SMTP/SES for email, Twilio for SMS—or deliver in-app messages over persistent WebSocket connections. The system tracks delivery status, retries failures, batches per user, and deduplicates events so one business event does not become multiple user-visible notifications.

## Why interviewers ask this

The interviewer is testing whether you can design an asynchronous fan-out system that decouples noisy, bursty producers from slow third-party providers. They probe idempotency, retries, failure isolation, horizontal scaling of consumers, and user preference enforcement. Real follow-ups often escalate from provider choice to exactly-once semantics and machine failure recoverability.

## The core idea

The durable message queue is the backbone: it absorbs traffic spikes, allows independent scaling per channel, and preserves messages when workers die. Mobile push is delegated to APNS and FCM because only platform-controlled services can wake or reach installed apps reliably; your server is a client to those providers. Idempotency cannot be assumed from a single DB write after the provider call—if the worker crashes after the provider accepts but before tracking success, a retry can duplicate unless you collapse or dedupe on the device. Batching and per-user preference checks are product requirements, not optimizations; they reduce provider throttling and notification fatigue. Multi-region routing and dead-letter queues keep the system available and auditable under failure.

## Key points

- APNS and FCM are the two dominant mobile push providers; APNS is required for iOS notifications and FCM for Android.
- A message broker/queue such as Kafka, RabbitMQ, or SQS sits between producers and channel workers to absorb bursts and isolate third-party latency.
- A globally unique notification id or idempotency key is required; exactly-once delivery to APNS/FCM is not guaranteed, so design at-least-once with collapse keys or client-side dedupe.
- For online users, in-app notifications should use a persistent WebSocket connection to the notification service; offline users fall back to APNS/FCM push.
- Channel workers must respect per-provider rate limits, retry with exponential backoff and jitter, and move poison messages to a dead-letter queue after a maximum attempt count.

## Your 60-second answer

A notification system is an async fan-out pipeline. Business services publish events to a message queue; a notification service consumes them, applies user preferences and templates, and routes each notification to one or more channel workers—mobile push via APNS or FCM, email via SMTP or SES, SMS via a provider like Twilio, and in-app via WebSockets when the user is online. The queue decouples traffic spikes from slow third parties and lets you scale each channel independently. The hardest part is idempotency: a provider can accept a push and then your worker can crash before recording success, so a retry would send a second notification. You mitigate that with a unique notification id, collapse keys on the provider, client-side deduping, and at-least-once delivery. For online users, WebSockets are faster and cheaper than a push round trip; offline users fall back to APNS or FCM. The trade-off: batching reduces provider throttling and user fatigue but adds delivery latency.

## If they dig deeper

**Which channels would you support and how do you integrate them?**

In-app via WebSocket for online users, mobile push via FCM for Android and APNS for iOS, email through SMTP/SES/SendGrid, SMS through Twilio or similar. Each channel gets its own adapter because auth, payload format, retry and rate limit behavior differ; the notification core stays provider-agnostic.

**How do you handle a large burst of notifications?**

Producers publish to a durable queue so bursts do not call providers synchronously. Channel workers are horizontally scalable and consume at their own pace. For mobile push, group per-user events and send a collapsed notification instead of one per event. The provider-facing adapter uses connection pools, bounded queues, and per-provider rate limiting with exponential backoff; poison messages go to a dead-letter queue.

**How do you ensure the same notification is not sent twice?**

Exactly-once is not available from APNS/FCM as a server guarantee, so use at-least-once with idempotency. Assign a unique notification_id at ingest; before calling provider, record it as in progress with a unique constraint; on success mark sent. If the worker dies after provider success but before the update, the retry sees in progress and may duplicate; use collapse keys or client-side dedupe so a duplicate payload replaces the previous one on the device.

**How do you handle machine failures?**

Queue messages are durable and remain until acknowledged. Workers acknowledge only after provider call and tracker update. If a worker dies, the broker redelivers to another worker; after max retries it goes to a dead-letter queue. Push connections should be pooled and reconnected; WebSocket servers maintain session state in Redis or similar so another node can resume. Multi-region deployment with replicas prevents single-region outage.

**How do you handle global users and data residency?**

Use regional clusters for ingest, queue, and channel workers; route users to the nearest cluster. Store device tokens and contact data in the user's home region for latency and privacy; templates and preferences are globally replicated. APNS/FCM endpoints are global but providers apply per-app rate limits per region; track quotas per region. For SMS/email, choose providers local to the recipient to improve delivery and comply with local regulations.

## Worked example

User A likes User B's post, generating a `like_created` event with `notification_id = n_123`. The notification service fetches B's preferences: push on for likes and do-not-disturb off. It enriches the event with a template 'A liked your post' and publishes it to the `push` queue. A push worker consumes it, checks B's online status: B is offline, so it calls FCM with `collapse_key = post_456`, meaning repeated likes on the same post collapse into one notification on the device. FCM returns `provider_id = fcm_789`. The worker then writes a tracker row `(n_123, outbox, fcm_789, sent)`. If that worker crashes after FCM accepted but before the tracker write, the message is redelivered; the retry does not find `fcm_789` and calls FCM again. Because the request uses the same `collapse_key = post_456`, FCM replaces the first notification on the device, so the user still sees only one alert for that post.

## Common traps

- Claiming that a queue plus a DB 'sent' flag gives exactly-once delivery to external providers; a crash between provider success and the flag write still produces a duplicate.
- Sending notifications synchronously from the business service; one slow SMS or SMTP call then affects user-facing latency and backpressures the application.
- Ignoring provider rate limits and per-user batching; bursts trigger throttling, dropped messages, and users turning off notifications.
- Treating device tokens as stable; tokens rotate, and failure responses must trigger token removal or refresh to avoid repeatedly pushing dead devices.

</details>

---

## 16. Consistent hashing · mcq · Medium

*system_design · gate confidence 0.85*

**Question**

Which of the following distributed storage systems does NOT use a consistent hash ring for data placement?

**Options**

- Apache Cassandra
- Amazon Dynamo as described in the original paper
- Amazon DynamoDB
- Riak

**Reference answer**

Amazon DynamoDB

**Graded on**

- Amazon DynamoDB routes requests through a partition management service and maps hash ranges to nodes via a partition-to-node table.
- Apache Cassandra and the original Amazon Dynamo paper use consistent-hash token rings.
- Riak uses consistent hashing with virtual nodes.

<details><summary>The lesson this came from</summary>

Consistent hashing maps each key and each storage node to a position on the same hash ring. A key is assigned to the first node encountered clockwise from the key's position, wrapping around as needed. When a node is added or removed, only keys between that node and its predecessor change owners, instead of invalidating every mapping. It is a partitioning technique used to reduce data movement in distributed caches, sharded stores, and some replication schemes.

## Why interviewers ask this

Interviewers use this question to test whether a candidate can reason about data distribution under scale and node churn. They want to see you move beyond static modulo hashing, explain the remapping cost, and handle load imbalance with virtual nodes. It also reveals whether you know which real systems actually use the technique.

## The core idea

The key insight is to remove the dependence on a global node count. By placing nodes and keys on a ring and assigning each key to its clockwise successor, a node change only disturbs the local arc between the new or removed node and the previous node. Under uniform hashing that arc holds about k/n of all keys, so resizing costs drop from 'almost every key' to a small fraction. This property makes scaling and failure recovery more predictable. Basic ring-based hashing can still be skewed, so systems add virtual nodes, giving each physical node many positions on the ring. Consistent hashing is not a complete balancing solution; it must be combined with replication and node-health logic.

## Key points

- Consistent hashing hashes nodes and keys onto the same ring; a key is stored on the first node clockwise from its hash position.
- Adding or removing one node remaps only the keys in the affected arc, roughly k/n keys under uniform hashing, rather than all keys as in hash(key) % N.
- Virtual nodes map each physical node to multiple ring positions to reduce hot spots and smooth load distribution.
- Apache Cassandra and the original Amazon Dynamo paper use consistent hashing with token rings; Amazon DynamoDB does not—it maps partition key ranges through a partition-to-node table.
- Replication in a ring is typically placed on the next N distinct nodes clockwise, so losing adjacent nodes can affect multiple replicas.

## Your 60-second answer

Consistent hashing is a partitioning strategy that hashes both keys and servers onto the same ring. A key is assigned to the first server you meet moving clockwise from the key's hash position. The reason it matters is that with basic modulo hashing, hash(key) % N remaps almost every key when N changes. Consistent hashing only remaps the keys in the arc between the server that was added or removed and its predecessor, roughly k/n keys for n servers and k total keys. That makes resizing and node failures much cheaper. The trade-off is that one position per server can lead to very uneven load, so real systems add virtual nodes, where each physical server owns many ring positions. Cassandra and the original Amazon Dynamo paper use this ring model; DynamoDB itself uses a different partition management scheme.

## If they dig deeper

**Why does simple modulo hashing break when the number of servers changes?**

Because serverIndex = hash(key) % N depends on N. When N changes, the index for nearly every key changes, causing a mass migration or cache miss storm. Modulo hashing is only reasonable when the server pool is fixed.

**How do virtual nodes reduce hot spots?**

Each physical node is hashed to many positions on the ring, so it owns a larger number of smaller arcs. As the number of virtual nodes grows, keys spread more evenly across physical nodes; the cost is extra metadata and slightly more management complexity.

**How does replication work on a consistent hash ring?**

A key is written to the node it maps to and to the next R-1 distinct nodes clockwise, where R is the replication factor. If the owner fails, a successor can serve reads. But because replicas are adjacent on the ring, simultaneous loss of neighbouring nodes can reduce availability for that key.

**Which real systems use consistent hashing and which do not?**

Apache Cassandra uses a consistent hashing token ring with virtual nodes. The original Amazon Dynamo paper also describes a consistent-hash ring. Amazon DynamoDB, despite the shared name, does not use consistent hashing; it uses a partition management service that maps primary key hash ranges to storage nodes via a partition-to-node table.

**How would you handle a very skewed key distribution or a few large nodes?**

Virtual nodes help with random skew but cannot fix keys that are intrinsically hot, such as a celebrity user's posts. For those, you need to split hot keys, cache them, or replicate them more. Some systems use consistent hashing with bounded loads, where each node has a capacity and overloaded nodes shed keys to less loaded successors.

## Worked example

Take a 100-position ring. Three servers hash to S0=20, S1=50, S2=80. A key with hash 30 belongs to S1, because clockwise from 30 the first server is 50; key 70 belongs to S2 and key 90 wraps to S0. Now add S3 at position 40. Only keys in the arc (20, 40] change owners, so key 30 moves from S1 to S3; key 45 remains on S1; key 70 remains on S2. With 10 keys spread uniformly, about 2 keys remap instead of nearly all keys if the modulo modulus changed. This shows how resizing stays local.

## Common traps

- Claiming Amazon DynamoDB uses consistent hashing: production DynamoDB routes requests through a partition management service and hash-range-to-node mapping, not a hash ring.
- Treating the k/n remapping figure as guaranteed for any dataset; it is an expected value only when the hash distributes keys uniformly across the ring.
- Using one ring point per physical node and expecting balanced load; with few nodes the arcs are large and uneven, so virtual nodes are needed.
- Placing all replicas on strictly adjacent ring nodes without rack/topology awareness; two adjacent node failures can then remove multiple replicas of the same key.

</details>

---

## 17. Design case studies · flash · Easy

*system_design · gate confidence 0.85*

**Question**

What mechanism is appropriate for counting current active page viewers?

**Reference answer**

Use a cache of user IDs with a sliding 5-minute window and accept an approximate count.

**Graded on**

- use a cache
- store user IDs
- sliding 5-minute window
- approximate count is acceptable

<details><summary>The lesson this came from</summary>

A design case study is an interview format where you are given a vague product or infrastructure request (e.g., 'design a credit card processing system', 'show users viewing a page', 'design a database control plane') and must produce an end-to-end architecture. The answer starts with clarifying scope and non-functional requirements, then moves through API contracts, data model, core components, and scaling/consistency trade-offs. Strong answers explicitly separate critical-path synchronous work from asynchronous work and state which parts can tolerate approximate data.

## Why interviewers ask this

Interviewers use these open-ended scenarios to test whether you can reduce ambiguity by asking about level (such as whether you are building on Stripe or card networks), then reason about correctness, failure handling, and scale. The companies in real loops—Stripe, Booking.com, Netflix—are probing for structured decomposition and for avoiding mistakes like double-processing payments or over-engineering an approximate counter.

## The core idea

The core skill is scoping: ask what level you are building at, what consistency is required, and what the read/write pattern is before drawing boxes. For payments, correctness hinges on idempotency—the application generates and stores an idempotency key before calling any provider, and the store must be sharded by a composite key such as (merchant_id, idempotency_key) so the uniqueness check is local. Currency conversion must be computed and locked before or during authorization, not deferred. For metrics like current viewers, strong consistency is unnecessary; a cache with user IDs and a sliding time window yields an approximate but useful count. For a control plane, separate metadata operations (provisioning, scaling, auth, monitoring) from the data path so control-plane load does not affect query performance.

## Key points

- Clarify the implementation level first—for payments ask whether you are integrating with Stripe or building on card networks, because the rest of the design changes fundamentally.
- In payment systems, the client application must generate, store, and deduplicate idempotency keys even when using Stripe; the provider does not remove this responsibility.
- Shard the idempotency store by a composite of merchant_id and idempotency_key so the uniqueness check is local to one shard, not by merchant_id alone.
- For multi-currency payments, lock the conversion rate and calculate the exact charge amount before or during authorization; only multi-currency settlement is asynchronous.
- For approximate counts like active page viewers, use a cache of user IDs with a sliding 5-minute window and accept temporary inconsistency across regions.

## Your 60-second answer

When I get a design case study, I first clarify the level and scope, because the answer changes completely depending on whether we are integrating with an existing provider or building the primitive ourselves. Then I separate the critical path from everything asynchronous. For a payment system, I would ask if we are using Stripe or going to card networks, then design the API and data model around an idempotency key that the application generates and stores before calling the provider. That key must be sharded by a composite of merchant ID and idempotency key so retries are caught locally. For currency, I lock the rate before authorization, not after. For something like current viewers, I would accept an approximate count using a time-windowed cache with user IDs, because strong consistency is not worth the cost. The trade-off is consistency versus availability and latency; I choose the weakest guarantee that still meets requirements.

## If they dig deeper

**To clarify: what level are we implementing? For example, are we using Stripe or building on card networks?**

I would ask whether we are a merchant on top of a payment provider or a processor connected to card networks. The design changes from API orchestration, webhook handling, and a local ledger to acquiring, issuer messaging, and settlement.

**How will you handle the case where the payment is successful? How will you mark the payment as completed?**

After authorization, the provider sends a webhook or we poll for the final state. We update our ledger from pending to captured only upon a confirmed provider event, and the event handler is idempotent so a duplicate webhook does not double-apply.

**How do you ensure a payment doesn't get processed twice?**

The application generates a unique idempotency key per payment intent and stores it with the request state before calling the provider. Incoming retries and provider webhooks are deduplicated against this key, and the idempotency store is sharded by a composite of merchant_id and idempotency_key so the uniqueness check is local to one shard.

**How do you handle global payments and currency conversion?**

The conversion rate is locked and applied before or during authorization so the exact charge amount presented to the issuer is correct. Only multi-currency settlement and FX settlement happen asynchronously after authorization.

**How do you handle a burst of payments?**

I decouple synchronous authorization from asynchronous settlement and ledger updates with queues, horizontally scale the stateless API tier, and partition the ledger and idempotency store by the composite key. Edge throttling and queue backpressure absorb bursts without overloading downstream acquirers.

## Worked example

A client sends POST /payments with header Idempotency-Key: 7f8c2a and body {merchant_id: 42, amount: 99.99, currency: USD}. The API server computes the composite shard key (42, '7f8c2a') and checks the idempotency table on that shard. If no row exists, it inserts a row with status PENDING and calls the payment provider; if a row already exists, it returns the stored status without calling the provider. When the provider's authorization webhook arrives, the handler updates the row from PENDING to CAPTURED only if the current status is PENDING, so a duplicate webhook is ignored. A client retry with the same key hits the same shard, sees CAPTURED, and returns the original result instead of charging again.

## Common traps

- Delegating idempotency to a payment provider: Stripe requires the application to generate, track, and deduplicate idempotency keys; using Stripe does not remove that responsibility.
- Sharding the idempotency store by merchant_id alone, then expecting a uniqueness check on idempotency_key to be local: without the merchant_id in the query/key, the check becomes a scatter-gather across all shards.
- Delaying currency conversion until after authorization: the exact charge amount must be known and locked before or at authorization; only settlement is asynchronous.
- Overengineering consistency for approximate metrics like current page viewers: using user IDs with a sliding window in a cache is enough; persistent storage across regions is unnecessary.

</details>

---

## 18. Prediction Service · mcq · Medium

*ai · gate confidence 0.9*

**Question**

Which technique does NOT reduce inference compute for an existing model?

**Options**

- Quantization
- Pruning
- Operator fusion
- Knowledge distillation

**Reference answer**

Knowledge distillation

**Graded on**

- Quantization, pruning, and operator fusion reduce compute of the existing model
- Knowledge distillation replaces the model with a smaller student
- Distillation is not an inference optimization for the same model

<details><summary>The lesson this came from</summary>

A prediction service is the deployed system that applies a trained model to new inputs and returns predictions to callers. It includes request validation, feature assembly and preprocessing, model invocation, postprocessing, and often candidate retrieval and ranking. The service may be online (per-request, low latency) or batch (precomputed and stored), and it must be designed around throughput, tail latency, cost, and model-update safety.

## Why interviewers ask this

The interviewer is testing whether the candidate can move from a trained model in a notebook to a production serving design. They look for concrete latency-reduction levers, an understanding of the difference between replacing a model and optimizing inference for an existing model, and the ability to reason about candidate retrieval versus ranking.

## The core idea

A production prediction service is a pipeline, not just model.predict. When cutting latency without changing the model, profile the path and target specific stages: cache repeated requests, prefetch features, batch model calls, quantize or prune model compute, and move work offline. For large item corpora, the standard pattern is a two-stage funnel: an inexpensive candidate-generation stage (rules, ANN, or filters) reduces millions of candidates to hundreds or thousands, then a heavier ranking model scores only those candidates. Latency gains must be measured by tail percentiles against an explicit SLO, because average latency hides timeouts.

## Key points

- Online prediction serves each request with a low-latency SLO, while batch prediction precomputes predictions for later retrieval and trades freshness for throughput.
- A two-stage funnel combines cheap candidate generation with expensive ranking so the expensive model never scores the entire corpus.
- Quantization, pruning, and operation fusion can reduce inference compute for an existing model, but knowledge distillation replaces the model with a smaller student.
- Request batching improves throughput on GPU or SIMD hardware, but can increase tail latency unless batch size and timeout are bounded.
- A large ANN index is not automatically millisecond-fast: a 100M high-dimensional HNSW index may require hundreds of gigabytes of RAM and tens to over a hundred milliseconds per node unless sharded, quantized, or cached with a relaxed recall target.

## Your 60-second answer

A prediction service is the serving layer that exposes a trained model to production traffic, including request parsing, feature assembly, model inference, postprocessing, and often candidate retrieval plus ranking. If I need to reduce latency, I start by profiling where time actually goes: feature store calls, serialization, model compute, and candidate search usually dominate. Without replacing the model, I can cache repeated requests, prefetch features, batch model inference, and apply quantization or pruning where accuracy loss is acceptable. For large-scale search or recommendations, I would use a two-stage funnel: cheap candidate generation narrows the corpus, then a heavier model ranks only the candidates. I would also define p95 or p99 latency SLOs and monitor tail latency rather than just average response time.

## If they dig deeper

**What is the difference between batch and online prediction, and when would you use each?**

Online prediction computes results as requests arrive, so it must meet a tight latency SLO and is used for interactive product surfaces. Batch prediction precomputes and stores predictions on a schedule, which gives high throughput and lower cost when freshness can be minutes or hours old, such as nightly recommendations or catalog enrichment.

**How would you cut inference latency without changing the model?**

I would profile request traces to find the bottleneck, then cache identical or similar requests, reduce feature-store round trips with batching or prefetch, use request batching for GPU saturation, quantize weights and activations to lower precision, prune inactive connections, fuse operators, and tune the serving runtime. Distillation is not in this list because it replaces the model with a smaller student.

**How does candidate generation and ranking help in a large-scale recommendation or search system?**

Candidate generation uses cheap rules, coarse indexes, or ANN to reduce a huge corpus to a few hundred or thousand items. Ranking then applies a heavier model and richer features only to that shortlist. This keeps response time and cost sane without forcing the expensive model to score millions of items per request.

**Where does approximate nearest neighbor search become a bottleneck, and how do you manage it?**

For large high-dimensional vector sets, a single-node HNSW index can require hundreds of gigabytes of RAM and tens to over a hundred milliseconds because graph traversal is random access. To manage it, shard vectors across nodes, quantize the vectors with product or scalar quantization, cache frequent query results, lower efSearch where recall permits, or use a smaller candidate shortlist; but you must state these conditions rather than claiming millisecond retrieval universally.

**How do you safely deploy and update a prediction service without degrading users?**

Start with offline evaluation on held-out data, then shadow the new model on live traffic without returning its responses, then canary to a small percentage with automated rollback triggers, and A/B test against the current model. Monitor business metrics plus latency and prediction distributions, and check for feature or label drift before rollback.

## Worked example

A video search request spends 15 ms encoding the text query, 70 ms retrieving 500 candidate video IDs from a sharded 50M-vector ANN index, 20 ms batch-fetching features, 30 ms scoring those candidates, and 5 ms applying diversity rules. The total is 140 ms, but a slow ANN shard can push latency past 200 ms. Instead of changing the ranker, the service caches frequent query embeddings and candidate lists, quantizes the ANN vectors to reduce memory access, and falls back to a precomputed popular-candidate list when ANN latency exceeds a 90 ms cutoff. This keeps the same ranking model and removes the slow ANN lookup from the critical path for cached or fallback requests.

## Common traps

- Talking about model inference as if it were the whole service; feature fetching, serialization, network, and postprocessing often dominate latency.
- Recommending knowledge distillation as a way to speed up the existing model; distillation gives you a different, smaller student model.
- Claiming a large HNSW index returns thousands of candidates in low single-digit milliseconds without specifying sharding, quantization, recall target, and hardware.
- Quoting average latency instead of p95/p99; average hides the timeouts caused by slow ANN shards, garbage collection pauses, or cold caches.

</details>

---

## 19. Math & Geometry · flash · Medium

*dsa · gate confidence 0.9*

**Question**

How can Set Matrix Zeroes run in O(1) extra space?

**Reference answer**

Record whether the first row and column originally contain zero, then use those cells as flags to zero the rest of the matrix.

**Graded on**

- Save original zero state of first row and column
- Use first row and column as flags
- O(1) extra space

<details><summary>The lesson this came from</summary>

Math & geometry in DSA interviews means algorithmic problems where the hard part is a numerical or spatial relationship rather than a generic data-structure search. Typical tasks include walking a 2D array in spiral order, rotating a matrix in place, zeroing rows and columns, converting between numeral systems, detecting cycles in integer sequences, and computing powers. Most solutions depend on one algebraic identity or index invariant, such as transpose-plus-reverse for rotation or Floyd's cycle detection for digit-sum sequences.

## Why interviewers ask this

Interviewers use these problems as 20-30 minute screens because they expose index arithmetic, edge handling, and whether a candidate finds the one simplifying observation or defaults to brute force. Frequency data shows they are asked at a wide range: banks and trading firms like Capital One, Citigroup, SIG, Jump Trading, and Two Sigma, and product companies like Meta, Bloomberg, and LinkedIn. The signal is problem-solving maturity under tight constraints, not advanced mathematics.

## The core idea

These problems are not a single pattern; they reward reducing the operation to a small set of arithmetic or index updates. For matrices, keep explicit boundary variables and update them after each row or column pass. For numbers, use digit extraction and modular arithmetic to process from one end and avoid overflow. For iterative sequences such as Happy Number, recognize that deterministic functions on a finite state space either reach a target or enter a cycle, so two pointers can detect the cycle in constant space. For powers, exponentiation by squaring turns the exponent into binary powers. The recurring discipline is: find the invariant before coding.

## Key points

- Spiral Matrix uses four boundary variables; after walking one side, shrink that boundary and keep going until top > bottom or left > right, giving O(mn) time and O(1) space.
- Rotate Image clockwise 90° in place equals transpose across the main diagonal followed by reversing each row; O(n²) time, O(1) extra space, and counterclockwise reverses columns instead.
- Set Matrix Zeroes can run in O(1) extra space by recording whether the first row and column originally contain zero, then using them as flags for the rest of the matrix.
- Happy Number uses the sum of squares of digits; the sequence either reaches 1 or enters a cycle, so Floyd's two-pointer detection avoids a hash set.
- Pow(x,n) uses exponentiation by squaring in O(log n); for negative n, compute with 1/x and negate n only after guarding the 32-bit minimum value.

## Your 60-second answer

Math and geometry problems are solved by finding the mathematical invariant that lets you avoid brute-force simulation. For matrices, index arithmetic and transformations such as transpose-then-reverse make rotation O(n²) in-place; for numbers, digit extraction and modular arithmetic let you check a palindrome, convert a Roman numeral, or detect a Happy Number cycle without storing the whole number. The interviewer is testing whether you can reduce the operation to a few arithmetic updates and boundary checks, not just simulate the process. The trade-off is between low extra memory and readable boundary logic; off-by-one errors in indices are the usual failure. I start by stating the invariant for boundaries or numeric state, test it on a 3x3 matrix or a two-digit number, then code.

## If they dig deeper

**How do you traverse a non-square matrix in spiral order?**

Use top = 0, bottom = m-1, left = 0, right = n-1. After each side, shrink that boundary; after top and bottom rows, check top <= bottom; after left and right columns, check left <= right. Repeat until boundaries cross. This handles all m × n shapes.

**Why does transpose-then-reverse rotate an image 90 degrees, and what reverses it?**

Transpose maps (i,j) to (j,i); reversing each row maps (j,i) to (j, n-1-i). The composition is (i,j) -> (j, n-1-i), exactly a clockwise rotation. To undo, reverse rows then transpose; for counterclockwise, transpose then reverse columns.

**How does Floyd's cycle detection decide Happy Number?**

Advance slow by one sum-of-squares step and fast by two. If fast reaches 1, return true. If slow equals fast before reaching 1, the deterministic sequence has entered a cycle that never hits 1, so return false. This uses O(1) space instead of storing every seen value.

**What is exponentiation by squaring and its complexity?**

Write n in binary; x^n is the product of x^(2^i) for each set bit i. Maintain result = 1 and current_power = x; while n > 0, if n is odd, multiply result by current_power; then square current_power and right-shift n. Loop count equals the bit length of n, so O(log n) multiplications.

**How would you count axis-aligned squares for a query point in Detect Squares?**

Maintain a map from x-coordinate to a map from y-coordinate to point count. For the query point (qx,qy), iterate each existing point with x = qx and y' ≠ qy; side length d = |y' - qy|. The other two corners are (qx±d, qy) and (qx±d, y') for each sign, so add count(qx+d, qy)*count(qx+d, y') plus the same for qx-d. Sum over all such points.

## Worked example

Take a 3×3 matrix [[1,2,3],[4,5,6],[7,8,9]] and rotate it 90° clockwise in place. First transpose across the main diagonal: rows become columns, giving [[1,4,7],[2,5,8],[3,6,9]]. Then reverse each row: [7,4,1], [8,5,2], [9,6,3]. Check the corners of the original: 1 moves to the top-right, 3 to the bottom-right, 9 to the bottom-left, and 7 to the top-left. That matches clockwise rotation. No extra matrix is used, so the space is O(1).

## Common traps

- Off-by-one in Spiral Matrix: not checking boundary conditions after each side causes duplicate or missing elements in the last row or column.
- Set Matrix Zeroes: using the first row and column as flags before saving their original zero state destroys the information needed to zero them later.
- Negating the minimum 32-bit integer in a language like Java or C++ overflows when n = -2147483648; cast to long or handle that case before doing n = -n.
- Assuming every sequence in Happy Number either hits 1 immediately or never cycles; non-happy sequences always enter a cycle, so cycle detection is required, not optional.

</details>

---

## 20. Backtracking · mcq · Easy

*dsa · gate confidence 0.9*

**Question**

What three things do you need to define when designing a backtracking search?

**Options**

- The choices at each step, a validity check, and a termination condition
- The recursion depth, a pruning function, and sorted input
- A greedy choice, a memo table, and a target sum
- An include branch, an exclude branch, and an undo operation

**Reference answer**

The choices at each step, a validity check, and a termination condition

**Graded on**

- Possible choices at each step
- Validity check for the current partial state
- Termination condition

<details><summary>The lesson this came from</summary>

Backtracking is a controlled exhaustive search over an implicit tree of partial solutions. At each step it makes a choice, recurses deeper, then undoes that choice when the branch is exhausted or pruned. It uses problem-specific validity checks to stop exploring a branch early; without pruning it degenerates into brute force. Common targets are all valid configurations: permutations, subsets, combinations, and constraint-satisfaction puzzles.

## Why interviewers ask this

Interviewers ask Word Search, Combination Sum, Subsets, Permutations, N-Queens, and Sudoku Solver at companies including Amazon, Meta, Uber, Bloomberg, Snap, and LinkedIn to see whether a candidate can convert a constraints problem into a recursive search and prune it under time pressure. The signal is not mainly finishing the code; it is whether the candidate maintains and restores state, avoids duplicate configurations, and explains the exponential worst case honestly.

## The core idea

Backtracking is DFS over a tree of partial candidates. At a node, verify the current partial candidate against the problem's constraints; if it cannot lead to a solution, prune that subtree. Otherwise, extend the candidate by one choice and recurse. After returning, undo the last change so sibling branches see the same state. The essential difference from ordinary brute force is early pruning. Most variations are different choice sets, costs, and validity predicates.

## Key points

- Backtracking explores a search tree with recursive calls and undoes each candidate after returning, so sibling branches see the unchanged state.
- Pruning occurs when a partial candidate violates a constraint or cannot reach the target, and it is what separates backtracking from plain exhaustive brute force.
- The recursive call often carries a start index or remaining target so the same combination is not generated in multiple orders.
- For distinct elements, generating all permutations is O(n*n!) and generating all subsets is O(n*2^n) in typical output-sensitive analyses.
- Duplicate elements require sorting and skipping duplicates at the same recursion level, or a used/visited marker, to avoid duplicate output groups.

## Your 60-second answer

Backtracking is a recursive search strategy that builds a solution one choice at a time, and when a partial choice cannot work, it abandons that branch and undoes the last decision. The reason it is used for problems like permutations, subsets, combination sums, and N-Queens is that these require enumerating all valid configurations, and backtracking explores only the branches that are still viable. You define three things: the set of possible choices at each step, a validity check for the current partial state, and a termination condition. The main trade-off is exponential worst-case time, because the solution space itself is often exponential; pruning reduces the number of calls and branches but does not remove the worst-case bound. So the job is to design the strongest prune rule without skipping a valid answer.

## If they dig deeper

**How would you generate all subsets of an array without duplicates?**

Use include/exclude recursion with an index. At each index, either add the current element and recurse, or skip it and recurse. Once the index reaches the array length, copy the current list into the result. Undo the add before the skip branch so the two branches start with the same list.

**How do you handle duplicate values in problems like Subsets II or Combination Sum II?**

Sort the input first. In a loop over choices at each recursion level, skip an element when it is equal to the element just tried at the same level, unless it is the first candidate at this level. This prevents duplicate branches that would start with the same value at the same depth while still allowing valid repeated choices if the problem permits them.

**When would you choose backtracking instead of dynamic programming or greedy?**

Backtracking is for enumerating all valid configurations or any valid solution in a constraint space where order matters and there is no local best choice. Dynamic programming needs overlapping subproblems and optimal substructure, usually for counting or optimizing without returning configurations. Greedy is only safe when locally optimal choices are globally optimal, which is not true for most search and puzzle problems.

**What is the time complexity of the N-Queens backtracking solution?**

A standard row-by-row placement with column/diagonal conflict checks has an O(N!) upper bound on the number of placements before pruning, so the backtracking search is exponential in N. Early pruning removes many partial placements but does not make it polynomial.

**Can backtracking be combined with memoization, and why does it not always help?**

Yes, when the same state can be reached through different paths and the remaining subproblem is identical from that state, memoization can cache results. But many backtracking problems encode path-specific state such as the current ordering, used set, or board position, so the number of distinct states is nearly as large as the search space. Memoization then adds memory without reducing the branching meaningfully.

## Worked example

Generate all subsets of [1,2,3] with include/exclude recursion. Start with path [] at index 0. Include 1: path becomes [1], recurse to index 1. Include 2: path becomes [1,2], recurse to index 2. Include 3: path becomes [1,2,3]; output it, then remove 3 to restore [1,2]. Exclude 3: path is [1,2]; output it. Return, remove 2 to restore [1]. Exclude 2: path [1], recurse to index 2, then similarly produce [1,3] and [1]. Return to index 0, remove 1 to restore [] before the exclude-1 branch, which produces [2], [2,3], [3], and []. Each output is copied into the result rather than storing the mutable path reference.

## Common traps

- Forgetting to undo a choice after returning from recursion, so later sibling branches see corrupted state.
- Pruning too aggressively or applying duplicate-skip logic without sorting, which either misses valid branches or still emits duplicate answers.
- Storing references to mutable partial candidates in the result instead of copying them.
- Calling any recursive traversal 'backtracking' when it does not maintain and restore a candidate solution.

</details>

---

## 21. HashMap internals · mcq · Medium

*java · gate confidence 0.9*

**Question**

Which statement best describes the time complexity of get in a Java 8 HashMap?

**Options**

- O(1) in the worst case
- O(1) average and O(log n) worst case
- O(n) worst case in all cases
- O(log n) average and O(1) worst case

**Reference answer**

O(1) average and O(log n) worst case

**Graded on**

- average lookup is O(1)
- treeified buckets give O(log n) worst-case traversal
- O(1) worst case is a common trap

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

## 22. Generics · flash · Medium

*java · gate confidence 0.9*

**Question**

After erasure, what methods exist in a class that implements `Comparable<String>`?

**Reference answer**

The class has its declared `compareTo(String)` method plus a synthetic bridge method `compareTo(Object)` added by the compiler.

**Graded on**

- compareTo(String) remains
- compiler adds compareTo(Object) bridge

<details><summary>The lesson this came from</summary>

Java generics let a class, interface, or method be written once with type parameters such as `T`; the compiler enforces that only compatible reference types are used and inserts casts at call sites. Wildcards (`?`, `? extends T`, `? super T`) express unknown type arguments where a generic type is used, especially in method parameters. Java implements generics by erasure: after compilation, type variables are replaced by their leftmost bound (or `Object`), and the compiler generates casts and bridge methods as needed. As a result, generic type arguments are generally not known at runtime for objects.

## Why interviewers ask this

Interviewers use generics to test whether you understand compile-time safety versus runtime representation, and whether you can apply variance correctly. Many candidates know `List<String>` is not a `List<Object>` but cannot articulate why or choose between `extends` and `super`. It also exposes practical Java issues: raw types, unchecked casts, and erasure limitations.

## The core idea

The central idea is that Java generics are a compile-time abstraction. `List<String>` and `List<Integer>` are both just `List` at runtime; the compiler uses the generic arguments to reject bad `add` calls and remove manual casts. Generic types are invariant by default: even though `String` is an `Object`, `List<String>` is not a `List<Object>`, because treating it as one would permit inserting an `Integer`. Wildcards add use-site variance: `? extends T` lets you read from a producer and returns a `T` view, while `? super T` lets you write into a consumer but only guarantees `Object` on read. Erasure keeps compatibility with pre-Java-5 raw bytecode and creates bridge methods to support polymorphic overrides.

## Key points

- Java 5 introduced generics; unbounded type parameters erase to `Object`, bounded ones to their first bound.
- Java generic types are invariant: `List<String>` is not a `List<Object>`, unlike covariant arrays.
- Apply PECS: `? extends T` for producers you read from, `? super T` for consumers you write to.
- Erasure forbids `new T[10]`, `instanceof List<String>`, and methods overloaded only by generic argument.
- For `Comparable<String>`, the real `compareTo(String)` method stays; a synthetic bridge `compareTo(Object)` is added.

## Your 60-second answer

Java generics let you write a class, interface, or method once and use it with many reference types while the compiler checks the types. A type parameter like `T` is a placeholder; when you write `List<String>`, the compiler treats that list as accepting only strings and returning strings without explicit casts. Wildcards handle unknown types: `? extends T` is for reading from a producer, and `? super T` is for writing to a consumer. At runtime, generics are erased—the JVM sees the raw `List`, type parameters are replaced by their bounds, and the compiler inserts casts and bridge methods. The trade-off is that generic type arguments are not fully available at runtime, so you cannot create an array like `new T[10]` or test `instanceof List<String>`; safety is a compile-time guarantee, not a runtime one.

## If they dig deeper

**What is wrong with using raw types like `List` if the code compiles?**

Raw types are allowed only for backward compatibility with pre-Java-5 code. They turn off generic checks, so you can add mixed types and later get a `ClassCastException` at a cast site. They also produce unchecked warnings; a parameterized `List<String>` makes the compiler catch the mistake instead.

**Why is `List<String>` not a subtype of `List<Object>` even though `String` is a subtype of `Object`?**

Because generics are invariant. If `List<String>` were assignable to `List<Object>`, you could add an `Integer` through the `List<Object>` reference to a collection whose real element type is `String`, causing heap pollution. The compiler rejects the assignment to preserve type safety.

**When do you use `? extends T` versus `? super T`?**

Use `? extends T` when the generic object is a producer: you only read items and they can be treated as `T` or a supertype. Use `? super T` when it is a consumer: you only write items of type `T` or subtypes, and reading returns `Object` unless you cast. This is the PECS rule—Producer Extends, Consumer Super.

**What does type erasure actually erase, and what remains at runtime?**

The compiler replaces unbounded type parameters with `Object`, and bounded parameters with their first bound, so `class Box<T>` becomes a raw `Box` with an `Object` field. It inserts casts where code uses the type parameter and may generate bridge methods. The runtime does not know whether a particular `ArrayList` was declared as `ArrayList<String>` or `ArrayList<Integer>`; both share the same class object, though class-file signature metadata can describe declarations.

**How do bridge methods preserve polymorphism under erasure, for example in a class that implements `Comparable<String>`?**

The class's declared `compareTo(String)` is not changed to `compareTo(Object)`. Erasure of `Comparable<T>` makes the interface method `compareTo(Object)`, so the compiler generates an additional synthetic `compareTo(Object)` in the implementing class. That bridge method casts its `Object` argument to `String` and delegates to the real `compareTo(String)`. This keeps the class implementing the raw interface and preserves polymorphic dispatch when callers have a `Comparable` reference.

## Worked example

Consider a generic `Box<T>` with `private T value`, `void set(T value)`, and `T get()`. Writing `Box<String> s = new Box<>(); s.set("hi"); String x = s.get();` compiles with no cast in the source, but after erasure the field is `Object`, `set` takes `Object`, and `get` returns `Object`; the compiler inserts `(String) s.get()` at the call site. Now take `List<? extends Number> nums = new ArrayList<Integer>();`. `Number n = nums.get(0)` is allowed because every element is at least a `Number`, but `nums.add(1)` fails to compile: the list might really be a `List<Double>`, so adding an `Integer` would violate its actual element type. Conversely, `List<? super Integer> ints = new ArrayList<Number>();` accepts `ints.add(1)` because any supertype of `Integer` can hold an `Integer`, but `Integer i = ints.get(0)` does not compile because the compiler cannot guarantee the returned value is `Integer`—it could be any `Object`.

## Common traps

- Using raw types to silence generics errors; this disables compile-time checks and defers failures to runtime `ClassCastException`s.
- Treating `List<String>` as a `List<Object>` because `String` extends `Object`; Java generic types are invariant.
- Trying `new T[10]`, `instanceof List<String>`, or overloading methods that differ only by a generic argument—these fail because type arguments are erased.
- Claiming `compareTo(String)` in a class implementing `Comparable<String>` is erased to `compareTo(Object)`; the concrete method stays and a synthetic bridge is added.

</details>

---

## 23. Pub/Sub System Design · mcq · Medium

*lld · gate confidence 0.9*

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

A publish-subscribe system is a messaging pattern where publishers emit messages to named topics and subscribers receive only messages for topics they have registered interest in. A broker or topic object sits between the two groups, owning the routing table and delivery queues, so publishers and subscribers are not directly coupled. Multiple subscribers to the same topic each receive an independent copy of the message, and delivery is usually asynchronous through per-subscriber work queues.

## Why interviewers ask this

The interviewer is testing whether you can translate a messaging pattern into a small object-oriented design with clear responsibilities and thread safety. They are also probing how you handle slow consumers, failure, ordering, and delivery guarantees, because those are the actual complexity in any real pub/sub implementation.

## The core idea

The core mechanism is a Topic object that owns a thread-safe subscriber registry and a per-subscriber delivery queue. On publish, the Topic enqueues the message into each current subscriber's queue and returns quickly; a per-subscriber worker drains its queue and calls the subscriber's callback on that worker thread. Decoupling is achieved because the Topic exposes only subscribe/unsubscribe/publish, while publishers and subscribers never reference each other. Concurrency control belongs at the registry and queue boundaries, not in a global broker lock. Backpressure and delivery guarantees are then choices about the queue policy: block, drop, or retry.

## Key points

- Use a broker map keyed by topic name; each Topic keeps a thread-safe subscriber registry and one queue per subscriber, never one shared queue.
- A subscriber's worker thread drains its queue and invokes the callback, so one slow or throwing subscriber cannot block another subscriber or the publisher.
- Ordering is only guaranteed per topic per subscriber when a single producer enqueues in FIFO order and a single consumer drains FIFO; concurrent producers or multiple queues remove total order.
- Delivery guarantees must be explicit: an in-memory design can choose block, drop, or retry, while exactly-once processing requires idempotent consumers or message-ID deduplication, plus durable offsets if the process can restart.
- Thread safety uses a concurrent map, copy-on-write or synchronized subscriber-list snapshots, and bounded blocking queues with put/take or offer/timeout.

## Your 60-second answer

A pub/sub system has producers publish to topics and consumers subscribe to topics, with a broker in between so neither side knows about the other. In an object-oriented design I'd define Topic, Publisher, Subscriber, and Broker. The broker keeps a map from topic name to Topic. Each Topic holds a thread-safe collection of subscribers and a bounded queue per subscriber. publish appends the message to every subscriber's queue; each subscriber has a worker that pulls messages and invokes its callback. This gives decoupling, fan-out, and independent delivery. The main trade-off is backpressure: if a subscriber is slow and its queue fills, the broker must block the publisher, drop messages, or disconnect that subscriber. I'd specify at-least-once with retries or at-most-once with drops for the in-memory version; exactly-once requires deduplication or idempotent consumers.

## If they dig deeper

**How do you make the broker thread-safe when publishers and subscribers run on different threads?**

I use a concurrent map for the topic registry, copy-on-write or synchronized snapshots for each topic's subscriber list, and a bounded blocking queue per subscriber. publish iterates a snapshot and enqueues with offer or put; each subscriber worker uses take to drain its own queue. This avoids synchronizing the entire publish path.

**What happens when a subscriber is slow or throws an exception?**

If the subscriber is slow, its bounded queue fills. The broker has to apply backpressure: block the publisher, drop the oldest or newest message, or disconnect the subscriber. If the callback throws, the broker catches the exception and either retries, sends to a dead-letter location, or logs and skips, ensuring other subscribers are not affected.

**How do you preserve message ordering?**

Within one topic and one subscriber, a single FIFO queue gives per-topic order if one producer thread enqueues and one consumer thread dequeues. Multiple concurrent publishers to the same topic can reorder messages, so you would use a per-topic lock, a single writer thread, or assign sequence numbers. Ordering across topics or across different subscribers does not exist in this design.

**How would you extend this design to multiple broker instances or durable persistence?**

I would partition topics across broker instances and replicate an append-only log for each partition, similar to Kafka's model. Subscribers become consumer groups with stored offsets. A failed consumer restarts from its last committed offset, giving at-least-once delivery, while a durable log prevents message loss when a broker dies.

**Can you guarantee exactly-once delivery in this system?**

Exactly-once delivery is not a real broker guarantee across process failures; what is achievable is effectively-once processing. You need idempotent subscribers or message-ID deduplication, plus coordination between consuming a message and committing its side effects, often through a transactional outbox. In a single-process in-memory design you can dedupe by message ID per subscriber, but across restarts or network partitions you cannot guarantee exactly-once without distributed transaction coordination.

## Worked example

Suppose Topic orders has subscribers A and B, each with a bounded queue of capacity 10. Publisher thread calls broker.publish("orders", OrderEvent(42)). Broker resolves orders, snapshots [A, B], then calls queue.offer(event, 50ms) on each. A's queue has room so the event is enqueued; B's queue is full, so offer times out and the broker can either log-and-drop for B or apply a retry policy. A's worker takes the event and calls A.onMessage(OrderEvent(42)); B misses that copy if it was dropped. If the code used blocking put instead of offer, the publisher would wait when B's queue fills, creating backpressure that also delays A. This shows why per-subscriber queues plus a chosen queue policy are the real design decisions.

## Common traps

- Routing messages through a single shared queue causes one slow subscriber to stall every other subscriber; each subscriber needs its own queue.
- Assuming exactly-once delivery just because messages are sent once; without idempotent consumers or deduplication, retries after failure produce duplicates.
- Calling subscriber callbacks synchronously inside publish() couples publisher latency and failure to the slowest subscriber and can deadlock if a callback publishes or unsubscribes.
- Synchronizing the whole broker on publish serializes independent topics and reduces throughput; lock only the topic registry or per-topic structures.

</details>

---

## 24. CHAR vs VARCHAR · flash · Easy

*sql · gate confidence 0.9*

**Question**

What does VARCHAR(n) store compared with CHAR(n)?

**Reference answer**

VARCHAR(n) stores up to n characters but only the actual data plus length metadata; it does not pad shorter values.

**Graded on**

- Stores actual data only
- Adds length metadata
- No padding

<details><summary>The lesson this came from</summary>

CHAR(n) declares a fixed-length character column: inputs shorter than n are right-padded with spaces in SQL Server, PostgreSQL, and MySQL, so each value occupies the declared width. VARCHAR(n) declares a variable-length column that stores up to n characters and keeps only the actual data plus length metadata. Exact limits differ by engine: SQL Server caps ordinary CHAR and VARCHAR at 8,000 bytes and offers VARCHAR(MAX) up to 2 GB; PostgreSQL and MySQL also treat n as a character count and enforce row-size limits.

## Why interviewers ask this

This question tests whether you choose data types based on the data shape rather than habit, and whether you understand padding, comparison semantics, and engine limits. A strong answer separates logical schema from physical storage and update tradeoffs.

## The core idea

Use CHAR only for values that are genuinely fixed-width, such as ISO country codes; it makes row width predictable but can waste space. Use VARCHAR for variable text because it stores fewer bytes for short strings and preserves trailing spaces. The physical tradeoff is that VARCHAR saves space but requires variable-length handling, while CHAR can reduce page density because rows are wider. In PostgreSQL, both types receive the same MVCC treatment: an UPDATE creates a new tuple version unless HOT can avoid a new index entry, which happens only when no indexed column changes and the new version fits on the same page.

## Key points

- CHAR(n) right-pads shorter values with spaces to the declared width in SQL Server, PostgreSQL, and MySQL; in MySQL those trailing spaces are stripped on retrieval unless PAD_CHAR_TO_FULL_LENGTH is set.
- VARCHAR(n) stores up to n characters but only the actual data plus overhead; on SQL Server ordinary VARCHAR adds 2 bytes per row for its length, so short values use less space than CHAR(n).
- SQL Server caps regular CHAR/VARCHAR at 8,000 bytes; VARCHAR(MAX) can store up to 2 GB, with values larger than 8,000 bytes stored off-row as LOB data.
- PostgreSQL does not make VARCHAR cheaper to update in the MVCC sense: every UPDATE creates a new tuple version; HOT can avoid adding new index entries only when no indexed column changes and the new tuple fits on the same page.
- The declared n is a byte count in SQL Server CHAR/VARCHAR but a character count in PostgreSQL and MySQL; check the character set and collation when estimating physical size.

## Your 60-second answer

CHAR(n) is fixed-length: a CHAR(10) column always uses the full ten-character width and pads shorter values with spaces. VARCHAR(n) is variable-length; it stores only the characters you insert plus a small length prefix, so 'alice' in VARCHAR(100) uses five characters of data, not one hundred. Use CHAR only for truly fixed-width data like ISO country codes; use VARCHAR for names and descriptions. The main tradeoff is that VARCHAR saves space for short strings, which can fit more rows per page, but adds variable-length handling. Know your engine: SQL Server limits ordinary CHAR and VARCHAR to 8,000 bytes, and PostgreSQL gives both types the same MVCC update behavior—HOT can avoid index bloat only when no indexed column changes and the new tuple stays on the same page.

## If they dig deeper

**What happens to trailing spaces in CHAR versus VARCHAR?**

SQL Server stores CHAR padded to n, so DATALENGTH includes trailing spaces; VARCHAR stores the exact text and preserves trailing spaces. MySQL strips trailing spaces from CHAR on retrieval by default, while PostgreSQL treats them as insignificant in comparisons. VARCHAR generally preserves trailing spaces in all three.

**When can VARCHAR use more space than CHAR?**

A VARCHAR value at or near the declared maximum may be slightly larger because of the length prefix. For example, a full 8,000-byte VARCHAR(8000) uses 8,002 bytes in SQL Server, while CHAR(8000) uses 8,000. If most values are full-width, CHAR avoids that overhead; otherwise VARCHAR usually wins because short values use less space.

**How does PostgreSQL handle UPDATEs to CHAR or VARCHAR columns?**

Both types get the same MVCC behavior. Every UPDATE writes a new tuple version, so the old version remains until VACUUM regardless of column type or whether the length changed. If no indexed column changes and the new tuple fits on the same page, PostgreSQL can use a Heap-Only Tuple and avoid new index entries.

**What are SQL Server's limits for CHAR and VARCHAR, and how does VARCHAR(MAX) work?**

Regular CHAR(n) and VARCHAR(n) are limited to n = 8,000 bytes. VARCHAR(MAX) raises the payload limit to 2 GB; values larger than 8,000 bytes are stored as off-row LOB data with a pointer in the row. That makes MAX useful for large text but changes I/O behavior and some operations.

**If a table stores 10-character values in either CHAR(100) or VARCHAR(100), which one typically scans faster?**

Usually VARCHAR, because shorter rows mean more rows per 8 KB page and therefore fewer page reads. CHAR(100) forces a fixed 100-byte data area per value, reducing page density. If values actually approach 100 bytes, the difference shrinks, but the dominant cost is usually pages scanned.

## Worked example

In SQL Server, `CREATE TABLE Demo (Code CHAR(10), Username VARCHAR(100)); INSERT Demo VALUES ('ABC', 'alice');` returns `DATALENGTH(Code) = 10` because 'ABC' is blank-padded, and `DATALENGTH(Username) = 5` because only five bytes are stored. SQL Server adds two length bytes per ordinary VARCHAR row, so the username uses 7 payload bytes versus 10 for CHAR(10), a 3-byte saving per row. In PostgreSQL, an equivalent `UPDATE ... SET Username = 'alice.smith'` writes a new tuple version regardless of type; if no indexed column changes and the new tuple fits on the same page, HOT avoids creating new index entries.

## Common traps

- Saying VARCHAR is always smaller than CHAR; when values are consistently at or near the declared length, VARCHAR's length bytes can make it slightly larger.
- Assuming n means characters everywhere; in SQL Server CHAR/VARCHAR n is a byte limit, while PostgreSQL and MySQL use character counts.
- Ignoring trailing-space semantics during comparisons or unique constraints: CHAR padding makes 'ABC' and 'ABC ' compare equal in many engines, while VARCHAR preserves the difference.
- Applying a general 'fixed length is faster' rule without measuring page density and workload; a wide CHAR row can reduce rows per page and slow scans.

</details>

---

## 25. Locking Mechanisms · mcq · Easy

*cs · gate confidence 0.95*

**Question**

Which storage engine uses table-level locking by default?

**Options**

- InnoDB
- MyISAM
- PostgreSQL
- SQL Server

**Reference answer**

MyISAM

**Graded on**

- MyISAM uses table-level locking
- InnoDB uses row-level locking
- PostgreSQL uses row-level locks with MVCC
- SQL Server uses row-level with lock escalation

<details><summary>The lesson this came from</summary>

A lock is a mechanism that serializes access to shared state. In a database, pessimistic locking acquires a lock on a row or table before a transaction reads or writes, and holds it until commit or rollback; optimistic locking holds no transaction-long lock, instead validating at commit with a version, timestamp, or a compare-and-set primitive such as Redis WATCH. Row-level and table-level locks differ in the granularity of the protected resource, and many engines layer intent locks on the table to track lower-level row locks.

## Why interviewers ask this

Interviewers ask about locking to test whether you can reason about concurrency, data races, deadlocks, isolation, and throughput tradeoffs. They want to see that you know when to choose optimistic versus pessimistic locking and at what granularity, and that you understand what happens when multiple transactions touch the same data.

## The core idea

Locks trade concurrency for correctness. Pessimistic locking prevents conflicts by blocking early; optimistic locking assumes conflicts are rare and detects them at commit time. Granularity determines how much concurrency is lost: row-level locks let different transactions modify different rows concurrently, while table-level locks serialize all writers to the table. Most production row stores combine MVCC for lock-free reads with row-level write locks and intent locks to coordinate table-level operations. Choosing a strategy depends on contention, transaction length, and retry cost.

## Key points

- Pessimistic locking acquires a lock before reading or writing and holds it until the transaction ends, typically via SELECT ... FOR UPDATE in PostgreSQL or InnoDB.
- Optimistic locking uses a version, timestamp, or CAS check at commit time and retries on conflict rather than blocking; Redis WATCH implements this for transactions.
- Row-level locks protect individual rows and allow higher concurrency, while table-level locks protect the whole relation and reduce concurrency but also lock overhead.
- InnoDB uses row-level locking by default, MyISAM uses table-level locking, and PostgreSQL supports row-level locks plus MVCC so ordinary reads do not block on writers.
- Intent locks at the table level, such as IS and IX, let a table-lock request check a single table lock instead of scanning all row locks.

## Your 60-second answer

Pessimistic locking acquires a lock before touching the data, usually with something like SELECT ... FOR UPDATE, and holds it until the transaction commits or rolls back. Optimistic locking does not hold a transaction-long lock; it validates at commit time using a version number, timestamp, or compare-and-swap, and the transaction retries if another writer changed the row. Row-level locks only block other accesses to the same row, so different transactions can update different rows concurrently, while table-level locks serialize all writers on the entire table, reducing concurrency but also lock overhead. Engines differ: InnoDB and PostgreSQL use row-level write locks with MVCC for non-blocking reads, while MyISAM locks the whole table. Choose optimistic when conflicts are rare and retries are cheap; choose pessimistic when contention is high or the critical section is long.

## If they dig deeper

**What is the difference between a shared lock and an exclusive lock?**

A shared (S) lock allows other transactions to acquire shared locks on the same resource, but blocks exclusive locks. An exclusive (X) lock blocks both shared and exclusive locks by others. Some engines add an update (U) lock to prevent deadlocks when a transaction intends to upgrade a read to a write.

**When would you use optimistic locking instead of pessimistic locking?**

Optimistic locking works well under low contention, short transactions, and applications where retrying the whole transaction is cheap, such as a user editing a form. Pessimistic locking is better when conflicts are frequent, transactions are long, or retrying is expensive, because waiting once on a lock can cost less than repeated rollbacks.

**What are intent locks and why are they needed?**

Intent locks are table-level locks in modes like IS and IX that signal a transaction intends to take shared or exclusive locks on rows. A request for a table-level exclusive lock can check the table's intent locks instead of scanning all row locks, making multiple-granularity locking efficient and safe.

**What is two-phase locking and how does it relate to deadlocks?**

Two-phase locking (2PL) requires each transaction to have a growing phase where it only acquires locks and a shrinking phase where it only releases locks. Once it releases any lock it cannot acquire new ones. This guarantees conflict serializability but can lead to deadlocks because transactions may hold some locks while waiting for others, forming a cycle.

**How does MVCC interact with row-level locking in engines like PostgreSQL or InnoDB?**

MVCC keeps multiple row versions so ordinary readers see a consistent snapshot without acquiring row locks, which means writers do not block readers. Write operations still take row-level locks to resolve write conflicts, and SELECT ... FOR UPDATE or SELECT ... FOR SHARE acquires explicit row locks when the application needs current, locked data. This combination keeps reads lock-free while serializing writes on the same row.

## Worked example

Suppose two transactions update the same bank account row with id=1, balance=1000, version=5. Under pessimistic locking, Transaction A executes SELECT balance, version FROM accounts WHERE id=1 FOR UPDATE and gets the row lock; Transaction B tries the same select and blocks until A commits. A sets balance=900, version=6, and commits; B then reads the new version and proceeds. Under optimistic locking, both A and B read balance=1000, version=5 without any lock. A updates balance=900 and version=6 WHERE id=1 AND version=5; B then attempts balance=1100, version=6 WHERE id=1 AND version=5, but zero rows are affected because A already changed the version. B must reload the row, see version=6, reapply its business logic, and retry or report a conflict.

## Common traps

- Confusing row-level security (RLS) with row-level locking: RLS filters which rows a user can see, while row locks control concurrent modification.
- Saying optimistic locking never blocks: it avoids a transaction-long lock, but the final UPDATE still takes a brief row lock under the covers.
- Assuming SELECT ... FOR UPDATE is a table lock: in row-storage engines it locks only the selected rows, sometimes with gap locks under InnoDB repeatable read.
- Ignoring lock escalation: SQL Server can escalate many row locks to one table lock under memory pressure, so a row-level strategy may become table-level.

</details>

---

## Cards the gate rejected

Judge whether it was right. Each was thrown away.

- **ai-generative-model-evaluation** (flash): Which retrieval metrics are commonly used to evaluate the fetching step in RAG systems?
  - Gate said: wrong_format: Flash cards require a single crisp sentence, but this asks for an open-ended enumeration of metrics.

- **ai-probability-and-statistics** (flash): State the three axioms that any probability measure must satisfy.
  - Gate said: wrong_format: Listing all three Kolmogorov axioms cannot be crisply answered in one flash sentence.

- **ai-python** (mcq): Python's list and tuple are ordered sequences, while dict and set are hash-based containers. Which pair of properties primarily explains why a tuple can be a dictionary key but a list cannot, and why dict/set membership is average O(1) while list membership is O(n)?
  - Gate said: ambiguous: The question asks for a pair of properties explaining both traits, but the options conflate immutability/hashability and underlying data structures, making multiple options partially correct or debatable.

- **ai-software-engineering** (flash): When structuring an ML training codebase, what is the recommended core discipline for separating testable logic from orchestration?
  - Gate said: ambiguous: There is no single universally standardized phrase or pattern for this discipline, making an exact one-sentence flashcard answer overly ambiguous.

- **ai-training-and-optimization** (flash): Name two alternative update rules beyond vanilla gradient descent that alter how the raw gradient is applied.
  - Gate said: wrong_format: Flash cards should not ask to enumerate multiple items.

- **arrays-hashing** (flash): What is the main transformation that replaces an O(n^2) nested array scan with an O(n) solution?
  - Gate said: ambiguous: There is no single 'main transformation' that reduces O(n^2) nested scans to O(n) (e.g., hash lookups, two pointers, prefix sums).

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
  - Gate said: wrong_format: Format 'output' is not one of the allowed card formats (flash, typed, mcq).

- **beh-company-and-motivation** (mcq): In a behavioral interview, which impact signal is most appropriate for a senior engineer describing a proudest project?
  - Gate said: a competent answer disagrees with the marked option

- **beh-delivering-results** (typed): In the middle of a delivery, a load test fails or a deadline slips. What is the strongest response, and how do you decide among cutting scope, adding resources, or moving the date?
  - Gate said: wrong_format: This two-part, multi-faceted scenario question requires a detailed multi-paragraph response exceeding the typed format limits.

- **beh-failure-and-learning** (typed): What pattern can signal that you are about to repeat a past mistake?
  - Gate said: ambiguous: The question is overly vague and open-ended without a clear target concept.

- **beh-failure-and-learning** (flash): What four elements make a complete failure answer?
  - Gate said: wrong_format: Asking to list four specific elements requires an exact framework the candidate cannot guess.

- **beh-growth-mindset** (flash): When answering a behavioral interview question about growth mindset, what four elements should the story include to demonstrate that the change stuck?
  - Gate said: wrong_format: Flash cards expect one crisp sentence, but this asks to enumerate four specific elements from a specific framework.

- **beh-handling-feedback** (flash): When receiving feedback as a software engineer, what sequence of steps helps you handle it effectively?
  - Gate said: wrong_format: Describing a full sequence of steps requires multiple sentences or a paragraph, exceeding flash format constraints.

- **beh-leadership** (mcq): A senior candidate is preparing a behavioral story about leadership. Which set of dimensions should the story cover to avoid sounding like a single-dimensional executor?
  - Gate said: ambiguous: Both option 1 and option 4 are valid frameworks for holistic leadership, making the correct choice subjective and ambiguous without a specific source framework.

- **beh-ownership** (mcq): In behavioral interviews, ownership stories often scale with seniority: junior changes affect the candidate's own focus area, senior changes require coordinating several people (often three or more) on a team, and staff changes require multiple teams across the organization. According to this framework, which story best demonstrates senior-level ownership?
  - Gate said: refers to unseen material: 'According to this'

- **beh-ownership** (mcq): Which preparation technique is specifically recommended for finding weak spots in ownership stories before an interview?
  - Gate said: needs_context: Refers to a 'specifically recommended' technique from source text without general consensus.

- **beh-star-method** (flash): What is the main trade-off of using STAR in a behavioral interview?
  - Gate said: ambiguous: STAR is a framework without a standard, universally agreed upon 'main trade-off'.

- **beh-story-craft** (mcq): Which opening best separates team context from your personal contribution in a behavioral story?
  - Gate said: a competent answer disagrees with the marked option

- **java-checked-vs-unchecked-exceptions** (output): Consider this Java method:

```java
String firstLine() {
    FileReader reader = new FileReader("data.txt");
    return new BufferedReader(reader).readLine();
}
```

What does javac report when compiling it?
  - Gate said: wrong_format: Compiler error messages vary by JDK version and cannot be graded via exact match in output format.

- **java-collections-framework** (flash): In the Java Collections Framework, which interfaces extend Collection, and where does Map fit?
  - Gate said: wrong_format: Asking to list which interfaces extend Collection requires enumeration and is too long for a crisp one-sentence flashcard.

- **java-equals-and-hashcode-contract** (typed): How should equals and hashCode be implemented for a value class with several fields?
  - Gate said: ambiguous: The question is too broad and open-ended about general implementation guidance.

- **java-equals-and-hashcode-contract** (typed): What rules must an equals implementation itself obey?
  - Gate said: wrong_format: Answering requires enumerating the five specific contract properties (reflexive, symmetric, transitive, consistent, non-null).

- **lld-restaurant-management-system-design** (flash): In an object-oriented restaurant management system, a Branch object is composed of which two main domain components?
  - Gate said: ambiguous: Arbitrary schema design: different object-oriented designs decompose a Branch differently (e.g., Kitchen, Tables, Menu).

- **sd-caching** (mcq): In the worked example, a product page is fetched 5,000 times per second and the database sustains 800 reads per second. After the Redis cache is warm with a 30-second TTL, how many database reads per second does that single product key cause?
  - Gate said: needs_context: Refers to a specific "worked example" that the candidate cannot see.

- **sd-service-discovery** (flash): Name common service registry implementations used for service discovery.
  - Gate said: wrong_format: Asking to name/enumerate examples is an open list poorly suited to a one-sentence flash card.

- **sql-aggregate-functions** (typed): What are two important consequences of using SQL aggregate functions for reporting?
  - Gate said: ambiguous: Asking for 'two important consequences' without context is highly open to interpretation and could refer to NULL handling, performance, loss of row detail, grouping rules, etc.

- **sql-window-functions** (output): What is the output of the following SQL? Assume the employees table contains rows (name, salary): ('Ann', 80), ('Bob', 70), ('Cal', 70).

```sql
SELECT name, RANK() OVER (ORDER BY salary DESC) AS rnk
FROM employees
ORDER BY rnk, name;
```
  - Gate said: ambiguous: The exact textual format expected for the SQL result set (e.g., delimiters, headers) is unspecified for an exact-match output card.
