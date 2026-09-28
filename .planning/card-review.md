# 90x card review

2804 cards are ready to publish. An automated gate read 2810 and objected to 66 of them (2%): 60 were rewritten and passed on the second look, 6 could not be saved and were dropped (0%). Mix: 1373 typed, 763 mcq, 605 flash, 63 output.

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

## 1. Supervised Learning · mcq · Medium

*ai · gate confidence 0.5*

**Question**

Which of the following is NOT an assumption of linear regression?

**Options**

- Linear relationship between features and target
- Independent and homoscedastic residuals
- Low multicollinearity among features
- The target variable is normally distributed

**Reference answer**

The target variable is normally distributed

**Graded on**

- Linear regression assumes normally distributed residuals, not the target
- Other options are standard assumptions listed in the lesson

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

## 2. A/B Testing · typed · Medium

*ai · gate confidence 0.5*

**Question**

Why does peeking at an A/B test and stopping as soon as the p-value crosses 0.05 inflate the type I error rate?

**Reference answer**

Each peek is a repeated test, so the probability of seeing at least one false positive across all peeks exceeds the nominal 0.05 level. A standard fixed-sample test assumes the sample size was chosen in advance; stopping early violates that assumption.

**Graded on**

- repeated tests accumulate false positive probability
- fixed-sample test assumes pre-specified sample size
- stopping early violates assumptions

<details><summary>The lesson this came from</summary>

A/B testing is a controlled online experiment that randomly assigns users or requests to two or more variants, such as a control experience and a treatment that changes a model, ranking algorithm, or interface. Predefined metrics are compared across groups; the random assignment makes the groups comparable so an observed difference can be attributed to the variant rather than to preexisting differences. Results are usually evaluated with a frequentist hypothesis test and confidence interval, using a primary metric plus guardrail metrics to detect regressions.

## Why interviewers ask this

The interviewer is testing whether you can design an experiment that gives a causally valid answer: pick the right randomization unit and metrics, compute or justify the sample size, and interpret results without overclaiming. It also probes whether you know the common failure modes such as peeking, multiple comparisons, and network effects.

## The core idea

Random assignment is the core mechanism: it balances both observed and unobserved user characteristics in expectation, so the only systematic difference between control and treatment is the change being tested. Predefine a primary metric tied to the hypothesis, set the significance level, minimum detectable effect, and required sample size before the test starts. After the test, report the estimated effect with a confidence interval, not just a p-value, and distinguish statistical significance from practical importance. Guardrail metrics protect against shipping a change that improves one metric while degrading overall user experience.

## Key points

- Randomization is what makes A/B tests support causal claims; without it, differences may be driven by user population mismatch or seasonality.
- Pre-specifying a primary metric and required sample size before the test starts is necessary for the fixed-sample p-value to have its nominal false-positive rate.
- Peeking at results and stopping when a p-value crosses 0.05 inflates the type I error rate because repeated tests are not independent.
- Guardrail metrics such as latency, daily active users, or revenue per user detect cases where the treatment improves the primary metric but causes harmful side effects.
- A statistically significant result with a tiny estimated effect may not be worth shipping; the confidence interval must include the range that is practically meaningful.

## Your 60-second answer

An A/B test is a randomized controlled experiment that compares two or more versions of a product to estimate the causal effect of a change. You randomly assign users to control and treatment groups, collect the same predefined metric from each group, and test whether the observed difference is too large to be explained by chance. Randomization is what makes the comparison valid: it balances known and unknown user differences in expectation, so the only systematic difference between the groups is the variant itself. The main trade-off is that the test needs enough sample size and duration to detect a meaningful effect, and if you stop early once the p-value looks good, you will inflate false positives.

## If they dig deeper

**What metrics would you choose for an A/B test?**

Choose one primary success metric directly tied to the hypothesis, such as conversion rate or click-through rate. Add guardrail metrics that would catch harmful side effects, like page latency, error rate, or revenue per user, and pre-specify them before the test starts.

**How do you decide how many users the test needs?**

Set the significance level, typically 0.05, the desired power, typically 0.80 or 0.90, and the minimum detectable effect in the primary metric. Use baseline conversion or variance to compute the required sample size per group, then translate that into a duration that covers weekly seasonality. This prevents the test from being underpowered.

**Why is peeking at results a problem?**

If you compute a test at the 0.05 level repeatedly as data accumulates, the probability of seeing a false positive at least once rises above 5%, often substantially. A fixed-sample z-test or t-test assumes the sample size was chosen in advance. To peek safely, use sequential testing methods with adjusted boundaries.

**What happens if users in the treatment group affect users in the control group?**

The stable unit treatment value assumption is violated, so the control group is partly exposed to the treatment effect and the estimated lift is biased. Examples include social apps, marketplaces, and ad experiments where treatment users interact with control users. Mitigations include randomizing by cluster, ego-network, or using switchback designs for time-based interference.

**How would you handle an effect that changes over time, such as a novelty effect or user learning?**

You separate the early exposure period from the later plateau by pre-specifying time windows or using post-exposure cohorts. A novelty effect can make a short test look better than long-run performance, while learning effects can make a good treatment look weak at first. The correct approach is to define the evaluation window before looking at the data, run long enough to observe the steady state, and avoid post-hoc segmentation unless the analysis was planned.

## Worked example

A checkout flow test randomizes 5,000 users to each version. Control conversion is 20% and treatment conversion is 22%. For the two-proportion z-test, the pooled conversion rate is 21%, so the standard error is about 0.0081. The observed 2 percentage point lift gives z ≈ 2.46 and a two-sided p-value ≈ 0.014. You reject the null at α = 0.05, but the 95% confidence interval for the lift is roughly [0.4%, 3.6%]. If the team only cares about lifts above 2 percentage points, this result is statistically significant but not practically decisive, so the right move is to run longer or treat a launch decision with caution.

## Common traps

- Stopping the test as soon as the p-value drops below 0.05 and then interpreting that test as a standard fixed-sample result.
- Running many metrics and many treatment arms, then highlighting only the one comparison that happened to be significant.
- Concluding the change is safe because the primary metric improved while ignoring guardrail metrics that may be degrading.
- Treating a confidence interval that barely excludes zero as strong evidence without checking whether the lower bound is below the business-relevant effect.

</details>

---

## 3. Generative Model Evaluation · flash · Easy

*ai · gate confidence 0.5*

**Question**

What three aspects of a generated answer does the RAGAS RAG triad score?

**Reference answer**

Faithfulness, answer relevance, and context relevance.

**Graded on**

- Faithfulness
- Answer relevance
- Context relevance

<details><summary>The lesson this came from</summary>

Generative model evaluation is the set of methods for scoring open-ended model outputs—text, code, or tool calls—against explicit criteria such as faithfulness, relevance, correctness, and safety. Because generated outputs have no single correct answer, evaluation combines reference-based metrics, reference-free model judgments, and task-specific checks rather than one accuracy score. It includes static benchmarks, curated regression sets, and runtime scoring of a model's actual outputs on production prompts.

## Why interviewers ask this

Interviewers use this topic to test whether you can design an evaluation pipeline that detects real failure modes—hallucination, irrelevance, unsafe tool use—and aligns with product goals. They are looking for judgment about when to trust automated metrics, LLM judges, or human review, and how to separate broad benchmark capability from behavior on your own data.

## The core idea

For open-ended generation, no single metric captures quality; you need targeted metrics for groundedness, relevance, safety, and goal completion. Classic word-overlap metrics such as BLEU and ROUGE are weak proxies for semantic correctness because valid paraphrases can score low. Hallucination is evaluated as whether claims are supported by provided context or retrieved evidence, not by fluency. LLM-as-judge uses a rubric and a strong model to score outputs, and is cheaper than human review but must be calibrated against human labels. For RAG systems, retrieval metrics like recall@k, MRR, and nDCG are separated from generation metrics such as faithfulness, answer relevance, and context relevance. Agent evaluation adds tool-selection quality, step success, and trajectory adherence to final-answer accuracy.

## Key points

- Classic n-gram overlap metrics like BLEU and ROUGE are unreliable for open-ended LLM outputs because semantically correct variations can score low while fluent hallucinations may score high.
- The RAGAS RAG triad scores faithfulness, answer relevance, and context relevance, while retrieval is often measured with recall@k, MRR, and nDCG.
- LLM-as-judge uses a rubric and a strong model to grade outputs; pairwise win rates and Elo ratings aggregate relative quality in arenas like Chatbot Arena.
- Benchmarks like MMLU, GPQA, and SWE-bench measure broad capability, while safety and jailbreak robustness require red-teaming and adversarial prompt suites.
- Agent evaluation focuses on tool-selection quality, task/step success, and trajectory adherence, distinct from final-answer correctness.

## Your 60-second answer

Generative model evaluation is the practice of scoring an LLM's open-ended outputs against the specific qualities you care about—faithfulness to the provided context, relevance to the query, correctness, and safety. Unlike classification, there is usually no single right answer, so we combine several signals. We may use retrieval metrics like recall@k and nDCG to check that relevant context was fetched, then score the generated answer with reference-based checks or an LLM-as-judge against a rubric. Hallucination is typically measured by whether claims are grounded in the given context or retrieved sources. Benchmarks such as MMLU, GPQA, and SWE-bench give a broad capability signal, but they do not tell you whether your product behaves safely and usefully on your own data. The main trade-off is that LLM-as-judge is cheaper and faster than human review but can be biased and must be calibrated against human labels.

## If they dig deeper

**Why do classic metrics like BLEU and ROUGE fail for open-ended LLM evaluation?**

They measure exact n-gram overlap against a reference. LLM outputs can be semantically correct with very different wording, and fluent hallucinations can match reference words by chance. They do not assess groundedness, instruction following, or safety.

**What is the RAG triad and why should retrieval be evaluated separately from generation?**

The RAGAS triad scores faithfulness, answer relevance, and context relevance for the generated answer. Retrieval quality is measured separately with recall@k, MRR, and nDCG. Separation matters because a perfect retrieval can still produce an unfaithful answer, and a useful answer can come from noisy context; the fixes are different.

**How do you make an LLM-as-judge evaluation trustworthy?**

Use a clear rubric, calibrate against human labels, prefer pairwise comparisons or multiple judges, check for position and verbosity biases, and keep a held-out set of human-labeled examples for ongoing validation. It is a cheap proxy, not ground truth.

**What does trajectory-based agent evaluation catch that final-answer scoring misses?**

It catches wrong tool selection, repeated failed steps, unnecessary calls, and policy violations on the path to the answer. A model can reach a correct final answer with an unsafe or inefficient trajectory, and those intermediate failures matter in production.

**How do you measure hallucination in free-form generation without a reference answer?**

Break the output into atomic claims and verify each claim against provided context or retrieved sources using entailment/contradiction checks or an LLM judge. For closed-book generation, sample multiple responses and check consistency; unsupported or contradictory claims are flagged as likely hallucinations.

## Worked example

Consider a RAG system asked, 'When was the transformer architecture introduced?' Retrieval returns three passages; the top passage contains 'Vaswani et al. introduced the Transformer in 2017 in Attention Is All You Need,' and the other two are about electrical transformers. Recall@1 for this query is 1 because the relevant passage is ranked first. The model answers, 'The transformer was introduced in 2017 by Vaswani et al.' A faithfulness check decomposes the answer into two claims—the year and the authorship—and finds both supported by the retrieved context, so faithfulness is high. Answer relevance is also high because the answer directly addresses the question. Context relevance for the top three is lower because only one of the three retrieved passages is useful. A BLEU score against a reference like 'The Transformer architecture was presented in 2017' could still be low because the wording differs. This shows why retrieval and generation need separate metrics.

## Common traps

- Relying on BLEU or ROUGE as the main metric for open-ended generation—it rewards superficial overlap and punishes valid paraphrases.
- Treating a benchmark score such as MMLU or SWE-bench as proof of product quality, rather than a broad capability probe.
- Using LLM-as-judge raw scores without calibration against human labels and reporting them as ground truth.
- Evaluating only the final answer in an agent system, which misses wrong tool calls or unsafe intermediate steps.

</details>

---

## 4. Training and Optimization · output · Easy

*ai · gate confidence 0.5*

**Question**

What does this Python snippet print?

```python
x = [1.0, 2.0, 3.0]
y = [2.0, 3.0, 4.0]
theta = 0.0
grad = (2/3) * sum(xi * (theta * xi - yi) for xi, yi in zip(x, y))
print(round(grad, 2))
```

**Reference answer**

-13.33

**Graded on**

- The model is y = theta * x with MSE loss
- At theta = 0 the full-batch gradient is -13.33
- round(grad, 2) prints -13.33

<details><summary>The lesson this came from</summary>

Training a neural network means minimizing a scalar loss function over a dataset by repeatedly computing gradients and updating parameters. The loss is chosen to match the task: mean squared error for real-valued outputs, cross-entropy for discrete probabilities. Gradient descent variants differ in how many examples are used per update—full batch, one example (SGD), or a small random mini-batch—and update-rule variants such as momentum and Adam alter how the gradient is used. Learning rate schedules adjust the step size during training to improve convergence.

## Why interviewers ask this

Interviewers ask about training and optimization to see whether you can debug a model that is not learning or is unstable, rather than just call a framework API. They want you to connect batch size, loss selection, learning rate, and optimizer state, and justify choices for a given data size and hardware.

## The core idea

Every supervised deep learning model is trained by the same loop: forward pass to produce predictions, compute a scalar loss, backward pass to compute gradients of the loss with respect to parameters, and an optimizer step that subtracts a learning-rate-scaled gradient. Mini-batches are a compromise: full-batch gradients are accurate but expensive; single-example SGD is cheap but very noisy. The learning rate controls how far you move per step and is the most sensitive hyperparameter, so schedules reduce it from an initially high value or warm it up in very deep models. Loss functions encode the task: cross-entropy with logits gives better gradients for classification than MSE through a sigmoid.

## Key points

- The loss function measures error on a single example; the cost is the average over the training set or mini-batch, though most APIs call the batch-level quantity 'loss'.
- Batch gradient descent computes the gradient on the full dataset and is stable but slow; SGD uses one random example and is noisy but fast; mini-batch uses a small random subset and is the standard compromise.
- For regression the usual loss is mean squared error; for binary and multi-class classification the usual losses are binary cross-entropy and categorical cross-entropy, because they produce better gradients with sigmoid/softmax outputs.
- Learning rate schedules such as step decay, cosine annealing, or ReduceLROnPlateau reduce the step size during training; a high learning rate can diverge, a low one stalls learning.
- In PyTorch, gradients accumulate across backward calls, so call optimizer.zero_grad() before backward unless intentionally accumulating, and apply gradient clipping after backward but before optimizer.step().

## Your 60-second answer

Training a neural network is an optimization problem: we minimize a loss function that measures prediction error. For regression we typically use mean squared error; for classification, cross-entropy. The standard update is θ ← θ - η∇J(θ), but instead of the full dataset we usually use mini-batch gradient descent: sample a small random batch, compute its average loss gradient, and update. That balances the stability of the full-batch gradient with the speed and noise tolerance of SGD. The learning rate η is the most important knob; we often anneal it with a schedule like step decay or cosine, and sometimes warm it up at the start. Too high and you diverge; too low and training stalls. If loss plateaus, check data, initialization, capacity, and LR before reaching for exotic optimizers.

## If they dig deeper

**What is the difference between batch gradient descent, SGD, and mini-batch gradient descent?**

Batch gradient descent computes the gradient over the entire training set before updating, which gives a stable direction but is slow and memory-heavy. SGD updates on a single random training example, making it fast and able to escape some minima, but the gradient is very noisy. Mini-batch gradient descent computes the average gradient over a small random subset, balancing variance and compute and using hardware better.

**Why does SGD still converge if each gradient is noisy?**

Each noisy gradient is an unbiased estimate of the true gradient, so in expectation the step moves downhill. The noise can actually help escape sharp local minima and saddle points. Convergence to the exact minimum requires decreasing the learning rate over time because the noise never disappears; otherwise SGD oscillates around the optimum.

**When would you use a learning rate warmup, and how does it help?**

Warmup starts with a small learning rate and gradually increases it over an initial portion of training, which avoids large unstable updates when weights are near their random initialization. It is especially useful for very deep networks, large batch sizes, and transformers, where initial gradients can be large or noisy. After warmup, the main schedule decays the learning rate for convergence.

**Why sample batches without replacement within an epoch instead of sampling with replacement?**

Using an epoch means each training example is seen exactly once per pass, which reduces the variance of the gradient estimate across the epoch and guarantees coverage of the full dataset. With replacement, some examples can be skipped or repeated, increasing variance and making progress less predictable; without-replacement sampling is also often more efficient with shuffled data loaders.

**Your validation loss is lower than training loss. What might explain that?**

Training loss is averaged over the entire epoch, including early iterations when the model was worse, while validation is evaluated at the end of the epoch on the improved model. Regularization such as dropout is active during training but turned off during validation, making validation loss lower. Data augmentation and other train-time stochasticity also contribute.

## Worked example

Consider three points (x,y)=(1,2),(2,3),(3,4) and model y=θx with MSE loss L=(1/n)Σ(θx-y)^2. At θ=0, the full-batch gradient is dL/dθ=(2/3)[1(0-2)+2(0-3)+3(0-4)]=(2/3)(-2-6-12)=-13.33; with learning rate 0.05 the update is θ=0-0.05(-13.33)=0.667. A stochastic update on only the first point gives gradient 2×1(0-2)=-4 and θ=0.2. A mini-batch of the first two points gives gradient (2/2)[1(-2)+2(-3)]=-8 and θ=0.4. All three move θ in the positive direction toward the least-squares fit, but the smaller batches take noisier steps because they use partial data.

## Common traps

- Treating 'loss' and 'cost' as always identical in an interview; strictly, loss is per-example and cost is an average, though framework logs blur this.
- Saying SGD settles exactly at the minimum; with a fixed learning rate it continues to bounce around the optimum, and only a decaying schedule brings it close.
- Forgetting that PyTorch accumulates gradients by default; skipping zero_grad() combines gradients from multiple backward calls and corrupts the update.
- Choosing MSE for classification with sigmoid outputs can stall learning because the loss gradient includes a sigmoid-derivative term that saturates; cross-entropy is preferred.

</details>

---

## 5. Why this company · flash · Easy

*behavioral · gate confidence 0.5*

**Question**

What is the primary purpose of the 'Why this company?' question in a behavioral interview?

**Reference answer**

To check whether the candidate has researched the company and has a specific, credible reason tied to its products or engineering work, rather than a generic list of perks.

**Graded on**

- checks research effort
- checks motivation and retention risk
- requires specific company/team connection
- does not accept generic praise

<details><summary>The lesson this came from</summary>

The “Why this company?” question asks you to connect the company’s actual products, engineering domain, or team-level work to your own experience and what you want next. A strong answer is specific to that company and role, not a list of generic perks, and shows you have researched what the company builds and how its teams operate. It is a behavioral question: the interviewer is checking motivation, research effort, and whether you would accept the role if offered.

## Why interviewers ask this

Interviewers ask this to see whether you did real research and have a reason that survives follow-up questions. They also want to know what kind of work will keep you engaged, because a candidate who gives a generic answer is a retention risk. If you can only say “great culture” or “interesting work,” you have not shown enough signal.

## The core idea

A credible answer names one or two things this company actually does that you can speak about, then connects them to what you have built or want to build. For large companies, the useful move is to pick the product or infrastructure area you would join, not the whole company, because most big tech companies have teams across ads, cloud, payments, and internal tools. You do not need to prove you love every product; you need to show that the specific team or problem aligns with skills you already have. Use the product yourself only if it truly gives you product intuition, and treat that as one part of the answer, not the whole reason. The answer should sound like a working engineer choosing a problem, not a fan praising a brand.

## Key points

- Most large tech companies have teams across many domains, so a strong answer names the specific product, platform, or infrastructure area you would target rather than the company as a whole.
- Meta’s core products are social networks (Facebook, Instagram), messaging (WhatsApp, Messenger), and VR hardware (Oculus).
- Google’s signature areas include search, Chrome, Maps, Google Cloud, and Workspace.
- Amazon is best known for AWS and e-commerce; Microsoft for Windows and Office; Apple for hardware, operating systems, and services like iCloud and Apple Music.
- Using a product as an external user can improve product intuition, but interviewers expect engineering reasons as well.

## Your 60-second answer

I want to work here because the team I am applying to is solving a problem I have already worked on at a smaller scale. At my current job I built a system that hit the same kind of limits this team has written about, and I want to learn how it is done at your volume. I am not applying because the company is famous; I am applying because the specific product or infrastructure area has technical constraints that force the team to build things in-house, and that is the environment where I do my best work. I also use one of your products, which gives me a user’s sense of where failures matter. The trade-off is that this role will be harder than similar ones elsewhere, with more on-call and more ambiguity, but that is exactly the next step I want.

## If they dig deeper

**What do you know about our products?**

I know your company is best known for its core product area, but I also looked at the specific team I am applying to. For example, if this were Google, I would mention Search, Chrome, Maps, Google Cloud, and Workspace, then say I am most interested in the team because of a specific technical reason I found in their engineering posts, not just the marketing pages.

**Why this company and not another big tech firm?**

Because the problem I want to work on is central here in a way it is not elsewhere. If I wanted to work on social graph problems, Meta is the obvious place; if I wanted search or developer infrastructure at that scale, Google is where those problems are concentrated. It is not that other companies lack the problem, but the depth and ownership differ.

**Which team or area do you want to join, and why that one?**

I want to join the team that owns the specific system or problem I have been working on in a smaller form. I read that this team had to build certain tooling in-house because off-the-shelf systems could not handle the load, and that is the kind of constraint I want to work under. I can contribute from day one while learning the scale-specific techniques.

**What would you do in your first 90 days if we hired you?**

I would first learn the system by reading the design docs and tracing the critical paths in the code, then take on a small, well-scoped task to build trust. I would ask the team where the current pain points are and see if my past experience with a related problem can help. I would not try to redesign anything until I understand why the existing design is the way it is.

**If you joined and found the team’s work was less aligned with your interests than you expected, what would you do?**

I would give it at least a quarter, because early impressions of scope are often wrong and the real interesting problems may not be visible in the first month. If the mismatch persisted, I would look for an internal transfer to a team closer to my interests, since large companies generally support moving between teams. I would only leave quickly if there were a values or management problem, which is different from a domain mismatch.

## Worked example

A strong answer sounds like: “I applied to the payments team because I want to work on reconciliation at the scale your systems operate at. At my current job I built a smaller version of that system, and the hard part was exactly the idempotency and replay issue your team described in its engineering blog. I also use your customer-facing app, which gives me a user’s intuition for where failures are visible. I am not applying because the company is famous; I am applying because this team owns the harder version of the problem I have been working on.” The candidate names a team, a matching technical problem, a source of research, and a reason that can be checked.

## Common traps

- Reciting generic praise like “great culture and smart people” without naming a product, team, or technical problem.
- Naming a company but explaining only why the role is good for you, not what you would contribute to that specific team.
- Saying “I want to work on big scale” without showing you know what scale means at that company or what systems they built to handle it.
- Picking a product you do not actually use or understand just because it sounds impressive, then failing when asked a follow-up about it.

</details>

---

## 6. Delivering results · typed · Medium

*behavioral · gate confidence 0.5*

**Question**

When an interviewer asks, 'What was your specific role in that project?', what should your answer separate?

**Reference answer**

Separate what you personally decided or did from what teammates did, and claim only the lever you owned. For example, own the cache fix and load test while a teammate owned the deployment pipeline, with mutual review.

**Graded on**

- personal vs team actions
- claim only your lever
- use specific example

<details><summary>The lesson this came from</summary>

Delivering results is the behavioral competency of taking ownership of an outcome and driving it to completion with verifiable impact. In an interview, it is evaluated by asking for a specific past project and checking whether the candidate can state the goal, the actions they personally took, the obstacles they hit, and the outcome in numbers or concrete scope. It is distinct from effort: the interviewer wants evidence that the work changed a metric, met a hard deadline, or shipped under constraints rather than simply being busy.

## Why interviewers ask this

Interviewers ask about delivering results to test whether you can be trusted with ambiguous or important work once hired. They are checking for agency—did you push the work or wait for guidance—and for judgment—did you pick the right target and adjust when the plan failed. They expect one clear story with causal detail, not a list of tasks.

## The core idea

A credible answer starts with the result, then works backward to the actions that caused it. Name the outcome in units someone outside your team would understand: latency, error rate, revenue, completion rate, delivery date, number of users or regions. Show the input you controlled, because a result without an owned lever sounds like luck or team credit. Include a setback and the change you made in response; the setback is often the part the interviewer weighs most. End with what you would do again, because that shows learning under pressure. At senior levels, the result should be a team or cross-team outcome, not just an individual task.

## Key points

- A strong answer follows situation, task, action, and measurable result rather than a chronological list of duties.
- Quantified outcomes—time saved, error rate, latency, revenue, users, regions, release date—are stronger than adjectives like 'successful'.
- Interviewers score only the part you personally drove; a team result becomes credible when you name your specific lever.
- A delivered result that had no obstacle or adjustment sounds invented, because real delivery usually requires a trade-off.
- At senior levels, the expected scope widens from individual delivery to team, multi-team, or business-level output.

## Your 60-second answer

A result I personally drove was keeping the checkout API available during peak traffic. In my previous role I owned the API layer. The success measure was availability. I profiled the service, found a connection leak in the cache client, fixed it, and added a load test before the next event. When the load test exposed a database bottleneck, I moved read-only traffic to a replica and tuned the connection pool. The service stayed up through the peak at its normal latency. The reason I chose that story is the result was measurable and my lever was direct. The trade-off was that I delayed a feature release to finish the fix, because the outage risk mattered more.

## If they dig deeper

**What was your specific role in that project?**

I can separate what I personally did from what the team did. In my story, I owned the decision about the cache fix and the load test, while a teammate handled the deployment pipeline; I reviewed their part and they reviewed mine.

**How did you measure success before you started?**

I set a target that was observable: availability above a threshold during the peak, and error rate below the previous event. I chose that because it captured user impact rather than engineering activity.

**When did the plan fail or a deadline slip, and what did you change?**

The first load test failed because the database saturated at the expected peak. I moved read traffic to a replica, retested, and then re-estimated the date; I did not keep the original date and hope the problem disappeared.

**How did you decide whether to cut scope, add resources, or miss the date?**

I compared the value of each item against the release risk: features that were not user-facing were cut first, and the date moved only when cutting more would still not meet the availability target. I made the trade-off explicit to the product owner.

**If you had to coordinate delivery across three teams with conflicting priorities, how would you create a single source of truth?**

I would create one scorecard with the shared outcome, each team's input metric, and a weekly review. I would make blocked work visible before it slips, and escalate only when a team cannot resolve a dependency with its peer.

## Worked example

A strong answer sounds like: 'In my previous role I owned [project]. The success measure was [metric], with a baseline of [number] and a target of [number]. I drove [specific action you personally took], and I tracked progress through [input metric]. When [specific obstacle] happened, I changed [specific action] and negotiated [scope/date] with [stakeholder]. We shipped [date or scope], and [metric] moved from [baseline] to [result]. The part I would repeat is [action]; the part I would change is [mistake].' The interviewer can follow because situation, task, action, and result are explicit. Choose fill-ins you can defend with data: if you cannot name a metric, name concrete scope such as the number of teams, regions, or customers affected.

## Common traps

- Listing responsibilities or team activities instead of a result you personally caused.
- Calling a project successful without a metric or before-and-after comparison.
- Describing the effort and setbacks at length but omitting the decision that changed the outcome.
- Claiming a team outcome without separating your lever, which makes the interviewer unable to score your contribution.

</details>

---

## 7. STAR method · mcq · Hard

*behavioral · gate confidence 0.5*

**Question**

Which of the following is NOT a common STAR trap?

**Options**

- Spending most of the answer on Situation and Task
- Using 'we' throughout the Action section
- Ending with a vague result like 'the project was successful'
- Using 'I' and explaining rejected options in the Action section

**Reference answer**

Using 'I' and explaining rejected options in the Action section

**Graded on**

- common traps: overlong context, 'we' in Action, vague results
- using 'I' with options is a strength, not a trap

<details><summary>The lesson this came from</summary>

STAR is a four-part framework for answering behavioral interview questions that ask about a past experience. The candidate describes the Situation (context and constraints), the Task (the objective or problem, including scope and success criteria), the Action (what the candidate did, why, and what alternatives were considered), and the Result (the measurable outcome and what was learned). Some interview coaching variants replace Task with Target to emphasize a goal the candidate set for themselves rather than one assigned by others. STAR is a narrative structure, not a scoring rubric.

## Why interviewers ask this

Behavioral questions are designed to predict future behavior from specific past examples. Interviewers use STAR to see whether the candidate can select a relevant experience, articulate their own contribution rather than the team's, and explain the reasoning behind decisions. The format also exposes whether the candidate understands scope, severity, benchmarks, and learning.

## The core idea

A strong behavioral answer follows a causal chain: what was happening, what I needed to achieve, what I actually did, and what came of it. STAR forces that chain by separating context from objective from action from outcome. The Action component carries most of the evaluation weight because interviewers are testing decision-making and ownership, not just a happy ending. A weak STAR answer expands Situation and Result while leaving Action vague or plural ('we did') and fails to connect the result to the action. The Task part should state scope, severity, and a benchmark so the listener can judge how hard the problem was.

## Key points

- STAR stands for Situation, Task, Action, and Result, and it structures answers to behavioral questions about past experience.
- The Task should include the scope, severity, and specific benchmarks or outcomes required, so the difficulty of the situation is clear.
- The Action should describe what the candidate personally did, why they did it, and what alternatives they considered, not just a list of steps.
- The Result should state a measurable outcome and what the candidate learned or changed afterward.
- A common variant replaces Task with Target when the candidate wants to emphasize a self-imposed objective.

## Your 60-second answer

STAR is a four-part structure I use for behavioral questions: Situation, Task, Action, and Result. I first set the context with enough detail to make the constraints clear, then state the specific objective or problem I owned, including scope or deadlines. The core of my answer is the Action: what I did, why I chose it over alternatives, and how I made the decision. Finally I close with the Result, giving a measurable outcome and what I learned from it. Interviewers favor this because it converts a rambling story into a causal chain they can evaluate quickly. The trade-off is that STAR can sound formulaic if the Situation drags on or the Result is vague, so I keep the Action the largest part and make the Result concrete.

## If they dig deeper

**What do the letters in STAR stand for?**

Situation, Task, Action, and Result. Situation establishes the context; Task states the objective or problem with its scope; Action describes what the candidate personally did and why; Result gives the outcome and what was learned.

**Can you walk me through a STAR answer for a conflict you handled?**

Choose a specific, recent conflict where you had a clear role. For Situation, give one or two sentences on the project and the disagreement; Task, the outcome you were responsible for; Action, the concrete steps you took to listen, explain, and reach agreement; Result, a measurable change in the team or timeline and what you learned.

**What separates a strong STAR answer from a weak one?**

A strong answer makes the Action first-person, decision-based, and specific: it names the alternatives considered and why one was chosen. A weak answer spends most of the time on background and ends with a team result, without showing the candidate's individual contribution or reasoning.

**What do you do if you don't have a perfect example for the question?**

Use the closest relevant experience and be honest about the boundaries. Describe the parts of the STAR framework you do have, then bridge to how you would handle the missing parts or what you learned from a related situation. Avoid inventing a story or borrowing someone else's result.

**How does STAR change when the interview asks about a failure or a mistake?**

The Result should emphasize what actually went wrong rather than hiding it, and the learning becomes the strongest evidence. The Action should still show ownership and the specific changes made afterward. Interviewers value a candidate who can describe a real failure with a concrete correction more than a sanitized success.

## Worked example

A strong answer sounds like: 'Situation: In my previous role at [company/product], a critical batch job began missing its SLA after a schema change. Task: I owned the fix and needed to restore the job to under [X] minutes without rolling back the schema. Action: I profiled the slow query, found a missing composite index, and tested it on a staging copy before applying it; I also added a timeout and alert so regressions would be caught early. Result: The job returned to [Y] minutes, the alert fired once in the following month and caught a second query before it affected users, and I documented the indexing checklist for the team.' This shape works because Situation is concrete but brief, Task includes a measurable bar, Action is first-person and includes testing, and Result ties the outcome to the action and learning.

## Common traps

- Memorizing the acronym but answering with a vague or generic story; interviewers probe for one specific project with dates, system names, and constraints.
- Spending most of the time on Situation and Result while compressing Action into 'we collaborated'; the interviewer needs the candidate's individual decisions and trade-offs.
- Choosing a Result with no measurable or verifiable outcome and no stated learning; the Result loses all evidentiary value.
- Changing the order or omitting Task because the objective feels obvious; without a defined objective, the listener cannot judge whether the Action was appropriately difficult.

</details>

---

## 8. Synchronization Primitives · typed · Hard

*cs · gate confidence 0.5*

**Question**

How would you implement a counting semaphore using a mutex and a condition variable?

**Reference answer**

Protect an integer count with a mutex. In wait, lock the mutex, wait on the condition variable while count is zero, decrement count, and unlock. In signal, lock the mutex, increment count, signal the condition variable, and unlock. Incrementing the count preserves semaphore memory for future waiters.

**Graded on**

- Protect integer count with a mutex
- Wait while count is zero on the condition variable
- Decrement count after waking
- Signal increments count and notifies one waiter

<details><summary>The lesson this came from</summary>

Mutexes, semaphores, monitors, and condition variables are concurrency controls that coordinate threads by blocking and waking them instead of letting them spin. A mutex provides mutual exclusion with ownership; a semaphore maintains an integer count of permits and blocks waiters when the count is zero; a condition variable lets a thread atomically release a mutex and sleep until another thread signals a state change; a monitor packages a lock and condition state into a language-level construct, as in Java's synchronized methods.

## Why interviewers ask this

The interviewer is testing whether you can distinguish the roles of these primitives and choose the right one for a given synchronization problem. It also reveals whether you understand ownership, memory, and wakeup semantics, which matter for deadlock and race avoidance.

## The core idea

Each primitive solves a different blocking problem. A mutex is a single-owner lock: only the thread that acquired it may release it. A semaphore is a counter with memory: signals accumulate as permits even when no one is waiting. A condition variable is a queue of sleeping threads that wait for an arbitrary predicate under a mutex, and its signals are lost when no waiter exists. A monitor is a structured wrapper that combines a lock with condition state, reducing explicit lock/unlock errors but limiting flexibility. The key is to match the primitive to the required semantics: ownership, counting, state waiting, or language-level encapsulation.

## Key points

- A non-recursive mutex, the default in POSIX threads, deadlocks if the same thread locks it twice without unlocking it first.
- A semaphore's signal operation increments the count even if no thread is waiting, so a future waiter will proceed; a condition variable signal with no waiting thread is lost.
- A condition variable wait must be rechecked in a while loop because a thread can wake spuriously or another waiter can consume the condition before the woken thread reacquires the mutex.
- Java's synchronized methods implement monitors with one implicit condition per object, while Java 5's ReentrantLock supports multiple Condition objects, tryLock, timed acquisition, and interruptible locking.
- A binary semaphore can enforce mutual exclusion, but it has no owner, so a different thread can signal it and priority-inheritance mechanisms tied to mutex ownership do not apply.

## Your 60-second answer

These are four ways threads block and resume each other. A mutex is a single-owner lock: one thread locks it, others block, and only the owner can unlock it. A semaphore is a non-negative counter; wait decrements it and blocks at zero, signal increments it and wakes a waiter. A condition variable is a queue of threads waiting for a predicate: wait releases the mutex and sleeps, and signal or broadcast wakes one or all waiters so they recheck under the lock. A monitor combines a mutex and condition state behind language methods, like Java's synchronized block with wait and notify. The trade-off is that mutexes are simple but only express mutual exclusion; semaphores express counting and signaling; condition variables express arbitrary state waiting; monitors reduce explicit lock bugs but are less flexible than explicit locks.

## If they dig deeper

**What is the difference between a mutex and a binary semaphore?**

A mutex has ownership: only the thread that locked it may unlock it, which supports priority inheritance and ownership checks. A binary semaphore can be signaled by any thread, so it is useful for signaling between threads but does not provide mutex ownership semantics.

**Why must a condition variable wait always be inside a while loop?**

A thread can wake spuriously, or another waiter may be woken first and change the condition before the first thread reacquires the mutex. The while loop rechecks the predicate under the lock, preserving the invariant.

**What happens if a condition variable is signaled when no thread is waiting?**

The signal is lost. Condition variables do not remember past signals; only a currently waiting thread can receive it. This differs from a semaphore, whose signal increments the count and therefore affects future waiters.

**How do Java's synchronized monitors compare with explicit ReentrantLock and Condition objects?**

Java synchronized blocks provide an implicit monitor lock and one implicit condition per object, with automatic unlocking but no tryLock, timed lock, or interruptible lock acquisition. ReentrantLock since Java 5 offers multiple Condition objects, tryLock, lockInterruptibly, timed waits, and an optional fairness policy, but the lock must be released in a finally block.

**How would you implement a counting semaphore using a mutex and a condition variable?**

You keep an integer count protected by a mutex. In wait, lock the mutex, wait on a condition variable while count is zero, decrement count, and unlock. In signal, lock the mutex, increment count, signal the condition variable, and unlock. This reproduces semaphore memory because incrementing the count affects future waiters even if none are currently blocked.

## Worked example

A producer and consumer share a one-slot buffer guarded by a mutex with two condition variables, notFull and notEmpty. The producer locks the mutex, checks whether the buffer is full, and calls wait on notFull if it is. Wait atomically releases the mutex and puts the producer on notFull's waiter queue. The consumer later locks the mutex, removes the item, signals notFull, and unlocks the mutex. The producer wakes, reacquires the mutex, and its while loop rechecks the buffer before inserting. If the producer used if instead of while, a spurious wakeup or a newly empty slot consumed by another producer could let it write into a full buffer and lose an item. The signal only works if the producer was already waiting; a signal on notFull when no producer was waiting is simply lost.

## Common traps

- Using if instead of while around a condition variable wait lets spurious or stolen wakeups break the invariant.
- Treating a binary semaphore as a mutex introduces ownership bugs because any thread can release the lock, and priority inheritance is not guaranteed.
- Assuming condition variable signals are queued when no one is waiting leads to lost wakeups and deadlocks.
- Forgetting to unlock a mutex on an exception path, or double-locking a non-recursive mutex, deadlocks the thread or the whole program.

</details>

---

## 9. File Systems · flash · Easy

*cs · gate confidence 0.5*

**Question**

What is the trade-off of using a journaling filesystem compared to a non-journaled filesystem?

**Reference answer**

Journaling adds write traffic and ordering overhead to normal operations but provides fast, bounded crash recovery that replays only recent transactions instead of a full fsck scan.

**Graded on**

- extra write overhead
- fast bounded recovery
- replaces full fsck scan

<details><summary>The lesson this came from</summary>

File systems provide the persistent storage layer that maps file names to bytes on disk. On Unix-like systems, a directory is a table of name-to-inode-number mappings; an inode holds metadata such as size, owner, permissions, timestamps, and pointers to data blocks, and in some filesystems can store small file data inline. Hard links let several directory entries name the same inode, so deletion is governed by both link count and open file descriptors. Journaling uses a write-ahead log to make multi-block updates recoverable after a crash.

## Why interviewers ask this

Interviewers ask this to see whether candidates understand the indirection between file names, inodes, and data blocks, and how filesystems remain consistent after crashes. It tests knowledge of real storage system behavior, not just language-level file APIs. A strong answer can reason about hard links, open descriptors, and recovery tradeoffs.

## The core idea

Everything in a Unix-like file system resolves through the inode. Directories do not contain file data; they contain lookups from names to inode numbers, which is why hard links can point to the same inode. The inode's on-disk state and data blocks are freed only when the link count reaches zero and no open file references remain. Multi-block updates cannot be atomic on storage, so journaling records a transaction in a separate area, commits it, and then checkpoints it; recovery replays committed transactions and ignores partial ones. This makes crash recovery fast and bounded rather than scanning every object as fsck does.

## Key points

- An inode stores metadata like file type, size, permissions, owner, timestamps, link count, and block pointers; ext4, XFS, and NTFS can also store small file data or short symlink targets inline in the inode or its equivalent record.
- A directory is a mapping from filename to inode number, not a container for file contents.
- Hard links are multiple directory entries pointing to the same inode; the inode and its data blocks are freed only when the hard link count reaches zero and all open file descriptors referencing that inode are closed.
- Journaling is write-ahead logging: a transaction is written to the journal, committed with an end marker, and later checkpointed to its final location, allowing recovery to replay only committed transactions.
- fsck scans and repairs the entire filesystem's metadata, whereas journal replay is much faster but adds write overhead to normal operation.

## Your 60-second answer

Unix-like file systems separate the name from the data. A directory maps human-readable names to inode numbers; each inode stores metadata like size, owner, permissions, timestamps, and block pointers, and in some filesystems small file contents live inline. Directory entries can share an inode via hard links, so the link count determines when the on-disk inode and blocks can be reclaimed—but only after the last open file descriptor is closed. Crashes make multi-block updates hard, so journaled filesystems use write-ahead logging: they record a transaction in the journal, commit it, then checkpoint it to the final location. After a crash, recovery replays committed transactions and discards incomplete ones, which is far faster than an older fsck scanning the whole volume. The trade-off is extra write traffic to the journal.

## If they dig deeper

**What exactly does an inode contain?**

File type, permissions, owner/group IDs, size, link count, timestamps, and pointers to data blocks or extents. In classic Unix filesystems it does not store the file name—that lives in directory entries—but ext4, XFS, and NTFS can store small file data or short symlink targets inline in the inode or equivalent record.

**How are hard links different from symbolic links?**

A hard link is just another directory entry pointing to the same inode, so it increases the link count and cannot cross filesystems or point to a directory in most Unix filesystems. A symbolic link is a separate inode holding a path string; it can cross filesystems and may dangle if the target is removed.

**Why does deleting an open file not immediately free its space?**

unlink removes the directory entry and decrements the inode link count, but a process holding an open file descriptor still references the inode through the open-file table. The inode and data blocks remain allocated until that last descriptor is closed; if the link count is already zero at that point, the space is freed. This is why processes can fill a disk with deleted-but-open files.

**Walk through crash recovery in an ext4 ordered-mode journaled filesystem.**

For a metadata update, the filesystem writes data blocks to their final locations before committing the metadata transaction. It then writes the journal transaction begin, the new metadata, and a transaction end; only after the end record is on disk is the transaction considered committed. After a crash, recovery replays committed transactions and ignores incomplete ones, then writes them in a checkpoint pass. Ext3/ext4 also use revoke records to prevent replaying stale metadata that would resurrect a reused block.

**Compare fsck and journaling for crash recovery.**

fsck scans and repairs the entire filesystem's metadata structures, so recovery time scales with disk size and can be minutes to hours on large volumes. Journaling only replays the last incomplete transactions, so boot-time recovery is fast, but adds write and ordering overhead during normal operation. fsck is still used when the journal cannot be trusted or on filesystems without a journal.

## Worked example

Run `echo hello > /tmp/x`; the inode has link count 1 and one data block. A process opens /tmp/x and keeps the descriptor. Another process (or the same) runs `unlink("/tmp/x")`. The directory entry disappears, but the kernel does not free the inode or data block because the open file descriptor still references it: `fstat` on the descriptor can still show size 6 and link count 0, and the process can read/write normally. When the process closes the descriptor, the kernel sees link count 0 and no remaining references, and then frees the inode and returns the data block to the free list. If a second hard link had existed, the link count would have been 1 after unlink and the data would survive through that other name.

## Common traps

- Treating the filename as the file's identity; in Unix, the inode is the file, and hard links are alternate names for the same underlying inode.
- Claiming unlink deletes the file immediately; if any process still has it open, the inode and blocks stay allocated until the last descriptor closes.
- Assuming a journaling filesystem always logs file data; ext4/ext3 ordered mode journals metadata only, so user data durability comes from write ordering, not the journal.
- Using fsck as if it were a fast everyday recovery tool; it is a full-volume scan and repair mechanism that is slow on large disks and cannot recover arbitrary data loss.

</details>

---

## 10. TLS/SSL Handshake · mcq · Medium

*cs · gate confidence 0.5*

**Question**

Which statement about forward secrecy in TLS is correct?

**Options**

- RSA key exchange provides forward secrecy because the pre-master secret is encrypted with the server's public key
- Ephemeral Diffie-Hellman provides forward secrecy because per-session private keys are discarded
- Forward secrecy means a certificate cannot be spoofed by a man-in-the-middle
- Forward secrecy is only available in TLS 1.3

**Reference answer**

Ephemeral Diffie-Hellman provides forward secrecy because per-session private keys are discarded

**Graded on**

- Static RSA key exchange does not provide forward secrecy
- Ephemeral Diffie-Hellman uses fresh per-session secrets
- Forward secrecy protects past traffic if long-term keys are later compromised
- TLS 1.2 supports forward secrecy through ECDHE and DHE

<details><summary>The lesson this came from</summary>

The TLS handshake is the initial phase of a Transport Layer Security session where client and server negotiate protocol version and cipher suite, authenticate each other (usually only the server), and derive symmetric encryption keys without exposing them to a passive observer. TLS 1.2 uses a two-round-trip full handshake, while TLS 1.3 reduces this to one round trip after the TCP connection is established. SSL refers to the deprecated predecessors of TLS (SSL 2.0 and 3.0); modern secure communication uses TLS 1.2 or TLS 1.3.

## Why interviewers ask this

Interviewers ask this to test whether you understand how HTTPS confidentiality and integrity are bootstrapped, why key exchange and authentication are separate mechanisms, and how the protocol prevents man-in-the-middle, downgrade, and certificate-spoofing attacks. A strong answer shows you can trace the handshake messages and reason about failure modes rather than just naming steps.

## The core idea

The handshake solves three problems: negotiating a cipher suite both sides support, authenticating the server using its certificate chain, and establishing a shared secret. In TLS 1.2 the client sends a ClientHello with random nonce and supported cipher suites; the server responds with its chosen suite, certificate, and optionally an ephemeral key exchange parameter, then both sides derive a master secret and expand it into per-direction keys. TLS 1.3 changed the structure so the client includes its Diffie-Hellman key share in the first flight, cutting latency and encrypting most of the handshake after the ServerHello. The Finished messages authenticate the full handshake transcript under the derived keys, so tampering with negotiated parameters is detected. Session resumption reuses previously derived key material; TLS 1.3 0-RTT can send early data but without built-in replay protection.

## Key points

- TLS 1.3 removed static RSA key exchange and makes forward secrecy mandatory through ephemeral ECDHE or DHE key agreement.
- A TLS 1.2 full handshake needs two network round trips before application data flows, while a TLS 1.3 full handshake needs one.
- Certificate validation must check the chain to a trusted root, signatures, validity dates, key usage, and revocation via CRL or OCSP.
- Finished messages carry a MAC of all previous handshake messages using the derived keys, protecting the negotiation from tampering and downgrade.
- Server Name Indication (SNI) lets one IP address host multiple TLS certificates, and ALPN negotiates HTTP/1.1 versus h2 inside the handshake.

## Your 60-second answer

The TLS handshake is how a client and server agree on encryption parameters, authenticate the server, and derive session keys. In TLS 1.2, the client sends a ClientHello with supported cipher suites and a random nonce. The server responds with its chosen suite, certificate chain, and for ECDHE cipher suites a signed ephemeral public key. The client validates the certificate, then both sides perform the key exchange and derive a master secret. Since TLS 1.3, the client includes its key share in the first message, cutting the handshake to one round trip and encrypting more of the exchange. Static RSA key exchange is gone because it lacks forward secrecy. The trade-off with TLS 1.3 0-RTT resumption is that early data can be replayed, so non-idempotent requests must opt out.

## If they dig deeper

**What is the difference between SSL and TLS?**

SSL was the original protocol, with SSL 2.0 and 3.0 now deprecated because of security flaws like POODLE. TLS 1.0 was the standardised successor in 1999; TLS 1.2 and TLS 1.3 are the versions in modern use, with TLS 1.3 offering a simplified handshake and stronger cryptographic defaults.

**Why did TLS 1.3 remove RSA key exchange?**

RSA key exchange encrypts the pre-master secret with the server's static private key, so anyone who later obtains that private key can decrypt all past captured handshakes, meaning no forward secrecy. TLS 1.3 mandates ephemeral Diffie-Hellman so the key agreement uses fresh per-session secrets, and it also reduces handshake round trips.

**How does the client verify the server certificate?**

The client builds a chain from the server certificate through intermediate certificates to a trusted root, validates each signature, checks validity dates, verifies key usage and extended key usage, and checks that the hostname matches a Subject Alternative Name entry. It also consults CRLs or OCSP for revocation, bounded by the platform's policy.

**What does the Finished message protect against?**

The Finished message is computed with the derived session keys over a hash of all previous handshake messages. Both sides verify it, so any attacker modification of cipher suite negotiation, version numbers, or key exchange parameters causes the verification to fail, preventing downgrade and man-in-the-middle tampering.

**How does TLS 1.3 0-RTT resumption work and what is its main risk?**

The client caches a PSK or session ticket from a previous connection and derives an early traffic secret to send application data with its ClientHello. The server may accept early data, but it has no built-in protection against replay, so a captured early-data flight could be replayed. Servers must restrict 0-RTT to idempotent requests or use single-use tickets.

## Worked example

A client connects to https://example.com with TLS 1.3. Its ClientHello includes an x25519 key share and ALPN offering h2 and http/1.1. The server replies with ServerHello containing its own x25519 key share, selects h2, sends its certificate chain, and computes the handshake secret from the two key shares; it then sends a Finished message encrypted under the server handshake traffic secret. The client derives the same secrets after validating the certificate chain and checking the SAN for example.com, then sends its own encrypted Finished. Both sides now derive application traffic secrets and begin HTTP/2 frames under AES-GCM. If a middlebox replaces the server certificate with its own, the client's signature validation fails before the Finished is accepted and the connection is aborted.

## Common traps

- Saying SSL and TLS are interchangeable without stating that SSL versions are deprecated and modern deployments use TLS.
- Claiming RSA key exchange offers forward secrecy or implying all TLS 1.2 cipher suites are equally secure.
- Describing certificate validation as only verifying a signature chain and forgetting hostname/SAN matching and revocation checks.
- Assuming TLS 1.3 0-RTT early data is safe against replay by default without server-side mitigations.

</details>

---

## 11. Stack · mcq · Easy

*dsa · gate confidence 0.5*

**Question**

What time complexity does a monotonic stack algorithm achieve for Largest Rectangle in Histogram?

**Options**

- O(n)
- O(n log n)
- O(n^2)
- O(n * max_height)

**Reference answer**

O(n)

**Graded on**

- each bar pushed and popped at most once
- not quadratic or linearithmic

<details><summary>The lesson this came from</summary>

A stack is a linear collection where insertion and deletion are restricted to one end, called the top, enforcing Last-In, First-Out order. The most recently added element is removed first. Stacks are typically implemented with an array or linked list; push, pop, peek/top, and isEmpty run in O(1) time, with array push amortized O(1) when resizing. They are the mechanism behind function call stacks, undo/redo, and expression evaluation.

## Why interviewers ask this

Interviewers use stack problems to test recognition of LIFO ordering and whether you can adapt the basic structure to maintain extra state. The observed company list includes Bank of America and Intuit for Valid Parentheses, Meta and Tesla for Basic Calculator II, and Visa and Flipkart for Largest Rectangle in Histogram, so the topic spans easy validation through hard monotonic stack parsing.

## The core idea

A stack resolves problems where the most recent unmatched or temporary item must be processed first. You push items while the condition is open or unresolved and pop when a matching or finalizing input arrives; the pop order is the reverse of the push order. That is why it validates balanced parentheses, evaluates postfix expressions, and supports undo. For monotonic stack problems, you pop while the new element violates an increasing or decreasing invariant, and each pop identifies the nearest smaller or larger boundary for that element. The stack only exposes the top, and respecting that constraint is usually the key to the correct algorithm.

## Key points

- A stack is Last-In, First-Out; only the top element is directly accessible, not arbitrary positions.
- push, pop, peek/top, and isEmpty are O(1) in both array-based and linked-list implementations; array push is amortized O(1) when the array resizes.
- Monotonic stack algorithms pop elements that violate a non-increasing or non-decreasing order, giving O(n) solutions for next-greater and largest-rectangle problems.
- In Java, ArrayDeque is preferred over java.util.Stack because Stack extends Vector and synchronizes each operation.
- Common uses include balanced parentheses, postfix/prefix expression evaluation, undo/redo, and the function call stack.

## Your 60-second answer

A stack is a linear data structure where all insertions and removals happen at the same end, called the top, so the last item pushed is the first item popped—LIFO. The standard operations are push, pop, peek, and isEmpty, and each runs in O(1) time. You implement it with a dynamic array or a linked list and keep a pointer or reference to the top. The reason it matters is that many problems have a delayed decision structure: a closing bracket must match the most recent opening bracket, an operator must consume the most recent operands, and undo must revert the latest change. Interviewers also extend it to monotonic stacks for next-greater-element and largest-rectangle-in-histogram problems. The main trade-off is that you cannot access arbitrary elements directly; you only get the top, so random access requires another data structure or popping elements and losing the structure.

## If they dig deeper

**What operations does a stack support, and what are their time complexities?**

push, pop, peek/top, and isEmpty. Each runs in O(1) time for array-based and linked-list implementations; array-based push is amortized O(1) because occasional resizing copies the existing elements.

**How would you solve Valid Parentheses with a stack?**

Push each opening bracket. For each closing bracket, if the stack is empty or the top is not the matching opening bracket, reject; otherwise pop. Accept only if the stack is empty after the scan.

**How do you implement a Min Stack with O(1) getMin?**

Keep a second stack of minimums. On push, if the new value is less than or equal to the current minimum, push it onto the min stack. On pop, if the popped value equals the min stack top, pop the min stack too. getMin returns the min stack top.

**In postfix/RPN evaluation, what happens when the current token is an operator?**

Pop the right operand, then the left operand, apply the operator in that order, and push the result. The order matters for subtraction and division, so you must not reverse the operands.

**What is a monotonic stack, and how does it solve Daily Temperatures or Largest Rectangle in Histogram?**

A monotonic stack keeps its elements in non-increasing or non-decreasing order by popping items that violate the invariant as new items arrive. Each popped item can record the new item as its next greater/smaller boundary, and each element is pushed and popped at most once, giving O(n) time. For largest rectangle, the stack stores indices of increasing bar heights so popping a bar identifies the right boundary and the stack top becomes the left boundary.

## Worked example

To evaluate postfix expression 2 1 + 3 *, start with an empty stack. Push 2, then push 1. At '+', pop the right operand 1 and the left operand 2, compute 2 + 1 = 3, and push 3. Push the next token 3, so the stack is [3, 3]. At '*', pop the right operand 3 and the left operand 3, compute 3 * 3 = 9, and push 9. The final stack top is 9. The most recent operands were consumed first, exactly the LIFO behavior needed for postfix evaluation.

## Common traps

- Trying to access elements below the top without popping them, which breaks the stack's LIFO contract and often turns an O(n) algorithm into O(n^2).
- Forgetting to check for an empty stack before peek/pop, causing underflow on inputs like a closing bracket with no opener.
- Applying operands in the wrong order for subtraction/division in RPN, such as computing right - left instead of left - right.
- Claiming every array-based push is worst-case O(1); resizing makes it amortized O(1), with an occasional O(n) copy.

</details>

---

## 12. Prefix Sum · typed · Hard

*dsa · gate confidence 0.5*

**Question**

Using a prefix-sum map initialized with {0: -1}, find the length of the longest zero-sum subarray in [2, -1, -1, 3, -3].

**Reference answer**

The longest length is 5, the whole array. Prefix sums are 0 at -1, 2, 1, 0, 3, 0; the later prefix 0 at index 4 matches the initial empty prefix at index -1, giving length 4 - (-1) = 5.

**Graded on**

- initial map {0: -1}
- prefix 0 recurs at index 4
- length is 4 - (-1) = 5
- whole array sums to 0

<details><summary>The lesson this came from</summary>

With 0-based original indices, a prefix sum array stores P[i] = nums[0] + ... + nums[i], with P[-1] = 0. Any contiguous subarray sum nums[l..r] is P[r] - P[l-1], so it can be answered in O(1) after O(n) preprocessing. The same idea extends to XOR and parity because both operations are associative and invertible. Hash maps over prefix values turn many O(n^2) subarray checks into one O(n) pass.

## Why interviewers ask this

Interviewers use prefix-sum questions to test whether you can precompute state instead of re-scanning windows. They also probe edge cases, especially whether the needed base case like {0: -1} is present. Real interview data shows these problems at companies such as Citadel, Visa, Twilio, PhonePe, and Akamai, often in medium-to-hard subarray variants.

## The core idea

Build an array P where P[i] = sum(nums[0..i]) and define P[-1] = 0. Then sum(nums[l..r]) = P[r] - P[l-1]. For subarray problems, iterate once and keep a hash map from prefix value to the earliest index or count, depending on the goal. Initialize the map with the zero prefix at index -1, so arrays starting at the first element are handled. This removes one dimension of brute force: instead of O(n^2) over all subarrays, one pass over positions plus hash map operations is O(n) expected. The static prefix array does not handle updates; that requires a Fenwick tree or segment tree.

## Key points

- With P[i] = sum(nums[0..i]) and P[-1] = 0, sum(nums[l..r]) = P[r] - P[l-1], giving O(1) range queries after O(n) preprocessing.
- For counting subarrays with sum k, maintain a hash map of seen prefix sums to their frequencies; each new prefix P[r] contributes map[P[r] - k] arrays ending at r.
- For the longest subarray with sum 0, initialize the prefix-sum-to-index map with {0: -1}; otherwise arrays that start at index 0 are missed.
- For contiguous XOR queries, XOR prefix sums use the same difference pattern because XOR is its own inverse.
- A simple prefix array is for static data; point updates require a Fenwick tree or segment tree, which extends the cumulative idea to O(log n) updates and queries.

## Your 60-second answer

A prefix sum array stores the cumulative sum up to each position, with an implicit zero before the array. Once you build it, the sum of any subarray nums[l..r] is P[r] minus P[l minus one], so a query that would otherwise take O(n) becomes O(1). The reason interviewers like it is that many subarray conditions can be rephrased as equality or a constraint on two prefix sums. For example, a zero-sum subarray exists whenever the same prefix sum appears twice. I would precompute in O(n) and then run one pass, using a hash map from prefix sum to either the first index or a count. The trade-off is space: the prefix array or map is O(n), and it only helps on static data; for live updates I would switch to a Fenwick tree.

## If they dig deeper

**How do you answer a range sum query on a static array without recomputing the sum each time?**

Build P where P[i] = sum(nums[0..i]) with P[-1] = 0. For a query [l, r], return P[r] - P[l-1]. Preprocessing is O(n), and each query is O(1).

**How would you count all subarrays whose sum equals k?**

Scan left to right while maintaining a hash map of prefix sums seen so far. At index r, if current prefix is P[r], add count of P[r] - k from the map, then record P[r]. Initialize the map with {0: 1} so subarrays starting at index 0 are counted.

**What special base case do zero-sum and sum-k solutions need?**

The empty prefix sum 0 must be registered before scanning. For the longest zero-sum subarray, use {0: -1}; for counting subarrays, use {0: 1}. Without it, subarrays that begin at index 0 are either missed or measured with the wrong length.

**Does prefix sum still work when the array contains negative numbers?**

Yes for range sums and exact-sum counting because the formula is algebraic and does not depend on values being positive. However, shortest-subarray-with-sum-at-least-k fails with a plain sliding window because negative values break monotonicity, and the standard fix is a monotonic deque over prefix sums.

**Shortest Subarray with Sum at Least K cannot be solved by a simple hash map approach. Why, and what structure works?**

A hash map tracks equality, but here the target is an inequality: P[j] - P[i] >= k. Negative values mean the earliest or latest index for a prefix is not enough; use a deque of candidate prefix indices with strictly increasing prefix sums. At each j, pop from the front while P[j] - P[deque.front] >= k and update the minimum length; then pop from the back while P[j] <= P[deque.back] before pushing j, so dominated indices are removed and the whole pass is O(n).

## Worked example

Array: [1, -1, 3, 2, -5]. Prefix sums are P[-1]=0, P[0]=1, P[1]=0, P[2]=3, P[3]=5, P[4]=0. For the longest zero-sum subarray, the map starts as {0: -1}. At index 0, P=1 is new, so the map becomes {0: -1, 1: 0}. At index 1, P=0 is already mapped to -1, giving length 1 - (-1) = 2 for [0, 1], which is [1, -1]. At index 4, P=0 again maps to -1, giving length 4 - (-1) = 5 for the whole array. The answer is 5 because 1 - 1 + 3 + 2 - 5 = 0. If the map had not contained 0 initially, the final prefix would have no earlier index and the whole array would be missed.

## Common traps

- Forgetting to initialize the prefix map with the empty prefix, 0 at -1 for index or 0 as count 1 for counting, which silently mishandles subarrays starting at 0.
- Using a sliding window for shortest subarray sum at least k when negative numbers are present; window pointer logic only works when sums are monotonic.
- Building an O(n) prefix array and then still iterating over all O(n^2) subarray pairs instead of using a hash map or deque to exploit prefix relationships.
- Assuming prefix products are always as easy as prefix sums; product prefix breaks if any element is zero, so division by prefix product is unsafe without extra handling.

</details>

---

## 13. Intervals · flash · Easy

*dsa · gate confidence 0.5*

**Question**

What is the time complexity of Merge Intervals when sorting is used?

**Reference answer**

O(n log n) time and O(n) extra space for the output list.

**Graded on**

- Sorting dominates at O(n log n)
- Linear scan after sorting
- O(n) space for merged result

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

## 14. ArrayList vs LinkedList · flash · Easy

*java · gate confidence 0.5*

**Question**

What is the backing data structure of a LinkedList in Java?

**Reference answer**

A doubly linked list of nodes, where each node holds an item plus prev and next references.

**Graded on**

- doubly linked list
- nodes
- prev and next references

<details><summary>The lesson this came from</summary>

ArrayList is a List implementation backed by a dynamically resized array of references. LinkedList is a List and Deque implementation backed by a doubly linked list of nodes, each holding an item plus prev and next references. Both maintain insertion order, allow null elements, and are not thread-safe. ArrayList offers O(1) positional get/set; LinkedList offers O(1) add/remove at either end and constant-time insertion/removal when a positioned iterator has already found the spot.

## Why interviewers ask this

This question tests whether the candidate knows actual implementation and complexity classes rather than repeating the oversimplified 'ArrayList for read, LinkedList for write' rule. Interviewers want to see cost by operation, including lookup before insertion, resizing behavior, memory overhead, and choosing the right data structure for a workload.

## The core idea

ArrayList keeps references in one contiguous array, so get(i) is a single array load, but inserting or removing at index i shifts every later element, O(n). LinkedList keeps nodes and links; get(i) walks from the nearer end, O(n), while append, removeFirst, and removeLast are O(1) and a positioned iterator can splice a node in O(1). Appending to ArrayList is amortized O(1) because the backing array grows geometrically, not on every add. The important practical nuance is that LinkedList's O(1) insertion only applies once you have the node; add(index, e) still pays O(n) to reach it. The decision is therefore access pattern and where modifications happen, not a blanket read/write rule.

## Key points

- ArrayList is backed by a dynamically resized array, giving O(1) get/set by index.
- LinkedList is backed by a doubly linked list of nodes, so get/set by index is O(n) because it walks from the nearest end.
- ArrayList appends are amortized O(1); add/remove at an arbitrary index is O(n) due to element shifting.
- LinkedList add/remove at either end is O(1); add(index, e) and remove(index) are O(n) because the node must first be found.
- LinkedList implements both List and Deque (Deque since Java 6), while ArrayList implements List but not Deque; LinkedList also has prev/next reference overhead per node.

## Your 60-second answer

ArrayList is backed by a resizable array; LinkedList is a doubly linked list of nodes. That single difference determines the trade-off. ArrayList gives O(1) get and set by index because it is one array load. LinkedList gives O(n) get/set by index because it walks the list from whichever end is closer. The common 'LinkedList is faster for insert/delete' claim is too broad. Appending to ArrayList is amortized O(1); inserting or removing in the middle shifts later elements, O(n). LinkedList is O(1) to add or remove at either end, or through a list iterator that is already at the node, but add(index, e) still costs O(n) to find that index. In practice I choose ArrayList for random access and read-heavy lists; I choose LinkedList only for work at the ends, iterator-heavy mutations, or when I specifically need Deque operations.

## If they dig deeper

**What are the time complexities for get, add, and remove in each?**

ArrayList get/set is O(1); append is amortized O(1), while add/remove at an arbitrary index is O(n) because later elements shift. LinkedList get/set is O(n); add/remove at either end is O(1); add(index, e) and remove(index) are O(n) to find the node, after which the link change is O(1).

**Why is ArrayList's add-at-end amortized O(1) when it occasionally resizes?**

The backing array grows geometrically rather than by one slot. In current OpenJDK, it typically grows by about 50%. The copy happens exponentially less often, so n appends still do O(n) total copying, averaging O(1) per append.

**When would you actually choose LinkedList over ArrayList?**

When the workload is dominated by addFirst/removeFirst/pollFirst or other Deque operations at the ends, or when a list iterator is already positioned at the mutation point. If the mutations are random indexed inserts, the O(n) lookup in LinkedList often makes ArrayList's contiguous array copy faster in practice.

**Why can ArrayList beat LinkedList even for an insertion-heavy workload, despite the asymptotic O(n) shift?**

ArrayList's shift is a contiguous in-memory copy of references, which is cache-friendly and often vectorized. LinkedList must allocate a new node, chase scattered pointers, and update several references; cache misses and allocation overhead can outweigh the asymptotic advantage for realistic sizes. Benchmark the actual access pattern before accepting the textbook rule.

## Worked example

For a 1,000,000-element list, ArrayList.get(499_999) computes one index into the backing array. LinkedList.get(499_999) chooses the closer end and then follows roughly 500,000 next or prev links; if the node objects are scattered across the heap, those are cache misses. Removing index 0 from ArrayList copies the remaining 999,999 references one slot left via a contiguous array copy. Removing index 0 from LinkedList just updates head plus one node's prev, constant time. But removing index 500,000 from LinkedList first walks roughly 500,000 links to find the node, while ArrayList shifts about 499,999 references. The crossover is workload-dependent; the asymptotic label alone does not pick the winner.

## Common traps

- Saying 'LinkedList is faster for insertion and deletion' without qualifying that indexed insertion/removal still requires O(n) traversal.
- Forgetting that ArrayList's append is amortized O(1), not O(n), because the resize copies are amortized over many operations.
- Believing an ArrayList stores the objects themselves contiguously; it stores references contiguously, but the referenced objects can be scattered in memory.
- Automatically using LinkedList as a Deque when ArrayDeque is usually the better queue/deque implementation due to no per-node overhead and better locality; LinkedList is mostly for cases needing nulls or iterator-specific removals in a List.

</details>

---

## 15. Java Memory Model · typed · Medium

*java · gate confidence 0.5*

**Question**

How does a volatile field establish ordering between earlier and later operations?

**Reference answer**

A volatile write is a release: all earlier writes become visible to a later read of that same volatile that sees the write. A volatile read is an acquire: later operations in that thread cannot be reordered before it. The language-level contract is a happens-before edge, not a particular barrier instruction.

**Graded on**

- volatile write is a release
- volatile read is an acquire
- creates happens-before edge
- implementation may use barriers but contract is HB

<details><summary>The lesson this came from</summary>

The Java Memory Model is the part of the Java Language Specification (Chapter 17, revised by JSR 133 for Java 5) that defines legal multithreaded executions. It specifies when a write by one thread is guaranteed to be visible to another thread and what reorderings of reads and writes are permitted. It is a relaxed memory model: without synchronization, a thread is not required to see another thread's latest shared-heap writes. Synchronization actions such as locking, volatile access, and thread start/join create happens-before relationships that impose visibility and ordering.

## Why interviewers ask this

Interviewers use JMM questions to find out whether you understand concurrency beyond synchronized syntax: visibility, stale reads, reordering, and data races. They want to know you can design shared state with volatile, final fields, and safe publication instead of assuming multithreaded code behaves like single-threaded code. It also tests whether you can explain why a concurrent program may pass tests on one machine but fail on another.

## The core idea

Each thread in Java has its own stack for local variables, while objects and their fields live on the shared heap. A thread can keep heap values in CPU registers or caches, so another thread may not observe updates unless the JMM forces them. The model does this through happens-before edges: program order within a thread, an unlock and a later lock on the same monitor, a volatile write and a subsequent read of that variable, a thread start and the started thread's first action, and a thread's final action and a join returning. If two accesses to the same variable are not ordered by happens-before and at least one is a write, they form a data race, and the program's behavior is not sequentially consistent. Since Java 5, correctly initialized final fields are visible without synchronization; the freeze at constructor exit also makes reachable state created before the freeze visible, but not later mutations.

## Key points

- Local primitive variables and reference variables live on each thread's stack, while all objects and their instance fields live on the shared heap.
- Without happens-before, the JMM allows stale reads and reordered reads/writes, so unsynchronized shared mutable fields can break even simple flags.
- Since Java 5, volatile reads and writes create acquire/release ordering: a volatile write happens-before any subsequent read of that same volatile that sees that write.
- Monitor operations order visibility: an unlock on a monitor happens-before every subsequent lock on that same monitor, even on different code paths.
- The final-field freeze at constructor exit guarantees visibility of final fields and of reachable objects populated before construction ended, but not of state mutated after publication.

## Your 60-second answer

The Java Memory Model is the JLS chapter that defines how threads see shared memory. It says a write by one thread is not guaranteed visible to another until there is a happens-before edge between them. Those edges come from synchronization: an unlock happens-before a later lock on the same monitor, a volatile write happens-before a volatile read of that variable that sees it, and thread start and join create ordering. When one action happens-before another, the earlier writes are visible and ordered before the later one. The reason this exists is that without it each thread could keep values in registers or CPU caches, and the compiler could reorder operations, so code that works in test may break elsewhere. The trade-off is that the JVM only imposes those guarantees where you ask for them: volatile, locking, or safe publication. Data races make execution much harder to reason about.

## If they dig deeper

**What is the difference between visibility and atomicity in Java?**

Visibility means a completed write by one thread must be seen by another thread; atomicity means a compound action like count++ executes as an indivisible unit. volatile gives visibility and ordering for individual reads and writes but does not make read-modify-write sequences atomic. For count++ you need synchronized, AtomicInteger, or another atomic class.

**How does a volatile field actually guarantee ordering?**

In the JMM, a volatile write acts as a release: earlier writes become visible when the volatile is later read. A volatile read acts as an acquire: later operations in that thread cannot be reordered before it. The JIT typically implements these semantics with memory barriers and by not caching the value in a register across the access, but the language-level contract is the happens-before edge, not a specific barrier instruction.

**What does synchronized guarantee besides mutual exclusion?**

Entering a monitor after another thread exits establishes a happens-before edge: everything the releasing thread wrote before unlocking is visible to the next thread that locks the same monitor. It also makes the critical section atomic with respect to other threads using that same monitor. Two threads synchronizing on different monitor objects get no mutual exclusion or visibility relationship.

**Can a final reference field make an entire object graph safely visible?**

The final-field freeze at the end of a constructor guarantees visibility of the final field itself and, under JLS 17.5.1, state reachable through that final reference if it was populated before the freeze and is not modified concurrently. It does not make that reachable state immutable or protect it from later mutation. Post-construction writes to the shared graph require additional synchronization, and a this escape during construction can break the guarantee.

## Worked example

One thread writes data = 42 and then sets a volatile boolean ready = true. Another thread loops until ready is true, then reads data. The writer's program order makes data = 42 happen-before the volatile write to ready. That volatile write happens-before the later volatile read that sees true. The reader's program order makes that ready read happen-before the read of data. By transitivity, the reader is guaranteed to see 42, not 0. If ready were a plain non-volatile field, those edges would not exist: the writer's two writes could become visible in the opposite order or not at all, so the reader could print 0 forever. The same pattern underlies safe publication with a volatile reference.

## Common traps

- Confusing the runtime stack/heap layout with the JMM; the JMM is about visibility and ordering of shared data, not where local variables are allocated.
- Believing volatile makes compound operations like increment atomic.
- Assuming the JVM is sequentially consistent by default; compilers and CPUs reorder accesses unless synchronization prevents it.
- Saying a final reference makes all reachable mutable state thread-safe; post-freeze mutations are not covered.

</details>

---

## 16. Thread lifecycle · mcq · Easy

*java · gate confidence 0.5*

**Question**

What happens if you call start() on a Thread object that has already been started?

**Options**

- It starts a second thread and runs run() again
- It throws IllegalStateException
- It throws IllegalThreadStateException
- It does nothing

**Reference answer**

It throws IllegalThreadStateException

**Graded on**

- start() can only be called once
- second call throws IllegalThreadStateException
- thread must be NEW to start

<details><summary>The lesson this came from</summary>

A Java thread's lifecycle is represented by the java.lang.Thread.State enum, introduced in Java 5, with six values: NEW, RUNNABLE, BLOCKED, WAITING, TIMED_WAITING, and TERMINATED. The state changes when specific methods are called or monitor events occur; the JVM tracks this state, not the OS scheduler. BLOCKED is specifically for waiting to enter or re-enter a synchronized block/method whose monitor is held by another thread. WAITING and TIMED_WAITING cover indefinite and timed pauses from wait, join, park, sleep, and timed wait.

## Why interviewers ask this

Interviewers use thread lifecycle questions to check whether you understand Java's actual Thread.State values and the methods or conditions that move a thread between them. They want to see you distinguish scheduler states from blocking states and know what code actions produce each state, because that informs deadlock, liveness, and performance reasoning.

## The core idea

The Thread.State enum captures six JVM-visible states. NEW is before start; RUNNABLE means the thread is either executing in the JVM or ready to run, but not necessarily on CPU. BLOCKED only occurs when a thread waits for an intrinsic monitor lock held by another thread. WAITING is an indefinite pause caused by Object.wait(), Thread.join(), or LockSupport.park(); TIMED_WAITING adds a timeout from sleep, timed wait, timed join, or timed park. TERMINATED is reached when run() returns normally or an uncaught exception propagates out of run. You cannot move backward from TERMINATED to any runnable state.

## Key points

- A thread is NEW only after construction and before start(); calling start() twice throws IllegalThreadStateException.
- RUNNABLE includes both executing and ready-to-run; it does not mean the OS is currently running the thread.
- BLOCKED is entered when a thread attempts to enter or re-enter a synchronized block/method whose monitor is held by another thread.
- WAITING is caused by Object.wait(), Thread.join(), or LockSupport.park() without timeout; TIMED_WAITING is caused by sleep, timed wait, timed join, or timed park.
- TERMINATED is final; a terminated thread cannot be restarted, and run() returning or throwing an uncaught exception ends the thread.

## Your 60-second answer

A Java thread has six states defined by the Thread.State enum: NEW, RUNNABLE, BLOCKED, WAITING, TIMED_WAITING, and TERMINATED. NEW is before start() is called. Once start() executes, the thread becomes RUNNABLE, which means it is either executing in the JVM or ready to be scheduled; it does not mean the OS is currently running it. BLOCKED happens only when a thread is waiting to enter a synchronized block whose monitor is held by another thread. WAITING occurs with indefinite methods like wait(), join(), or park(), while TIMED_WAITING adds a timeout, like sleep or timed wait. After run() returns, the thread is TERMINATED. The main trade-off is that RUNNABLE hides scheduler details, so two RUNNABLE threads may be making progress at very different rates depending on the OS scheduler and available cores.

## If they dig deeper

**What is the difference between calling run() and start()?**

Calling run() directly executes the method in the current thread, so no new thread is created and the state stays whatever the current thread is. Calling start() creates a new thread, which enters RUNNABLE before executing run() in that new thread, and start() can only be called once or it throws IllegalThreadStateException.

**Which methods put a thread into WAITING versus TIMED_WAITING?**

Object.wait() without timeout, Thread.join() without timeout, and LockSupport.park() put a thread into WAITING. The timed variants—wait(long), join(long), sleep(long), LockSupport.parkNanos or parkUntil—put it into TIMED_WAITING. The key is whether a timeout is specified.

**What is the difference between BLOCKED and WAITING?**

BLOCKED is exclusively waiting to acquire or reacquire an intrinsic monitor lock on a synchronized block or method. WAITING is after the thread already owns the lock and calls wait(), or when it calls join()/park()—it is waiting for a notification or specific event, not a monitor acquisition. A thread can also be WAITING without ever being blocked on a monitor, for example in join().

**Why might a thread state show RUNNABLE even though the thread appears stuck?**

RUNNABLE includes sitting in the run queue waiting for a CPU core, so under heavy load a thread can be RUNNABLE but not scheduled. In the HotSpot JVM, many blocking native or I/O operations are also reported as RUNNABLE because the JVM does not distinguish OS-level blocking, so a thread stuck in a socket read can appear RUNNABLE in jstack.

## Worked example

Suppose main holds an object's monitor while starting a worker thread whose run() first enters a synchronized(lock) block and then calls lock.wait(). After t.start(), the thread becomes RUNNABLE and immediately tries to enter the synchronized block, but because main still holds the lock, t moves to BLOCKED. When main exits the synchronized block, t acquires the lock, enters the block, then calls lock.wait(), releasing the lock and moving to WAITING. Later, main synchronizes on lock and calls lock.notify(); t wakes but must reacquire the lock while main holds it, so t becomes BLOCKED until main exits the synchronized block, then acquires the lock and returns from wait(), moving to RUNNABLE. Finally t exits the block and finishes run(), moving to TERMINATED. The sequence shows NEW → RUNNABLE → BLOCKED → RUNNABLE → WAITING → BLOCKED → RUNNABLE → TERMINATED, with the repeated RUNNABLE states being the JVM running the thread between blocking conditions.

## Common traps

- Treating 'Running' as a separate Thread.State: in Java's enum it is part of RUNNABLE, not a distinct value.
- Calling run() directly instead of start(): the code executes in the current thread, no new thread is created, and the method can be called many times.
- Assuming BLOCKED is a generic 'not running' state; it only means waiting to acquire an intrinsic monitor lock.
- Trying to restart a TERMINATED thread by calling start() again; the second call throws IllegalThreadStateException.

</details>

---

## 17. Coupling and Cohesion · typed · Hard

*lld · gate confidence 0.5*

**Question**

An OrderService directly creates a StripeGateway, charges a payment, writes a row through a raw database connection, and formats an email body. How would you refactor this class to improve coupling and cohesion?

**Reference answer**

Extract three interfaces—PaymentGateway with charge, OrderRepository with save, and NotificationSender with send. OrderService accepts these in its constructor and only coordinates calls. Stripe-specific and database-specific code move behind the interfaces, so each class has one responsibility and depends on abstractions.

**Graded on**

- split responsibilities: payment, persistence, notification
- define interfaces for external collaborators
- inject interfaces through constructor
- concrete implementations live behind interfaces

<details><summary>The lesson this came from</summary>

Coupling measures the degree to which one module depends on another, including what it knows about the other's interfaces, data, and internal implementation. Cohesion measures how strongly the responsibilities inside a single module belong together. A system with low coupling and high cohesion isolates change: modifying one module rarely forces changes elsewhere, and each module is easier to understand and test.

## Why interviewers ask this

Interviewers use this to test whether you can evaluate design quality beyond syntax and spot code that will become hard to maintain. They want to see that you can identify tight coupling or low cohesion in a given design and propose a concrete refactor. The question often hides inside code review, architecture discussion, or a design prompt.

## The core idea

Coupling and cohesion are two independent axes of modularity. Coupling is about dependencies between modules; cohesion is about relationships within a module. You cannot eliminate coupling entirely, but you can move it toward stable interfaces and dependency inversion. High cohesion does not mean fewer classes; it means each class has one clear reason to change. The goal is not a metric to hit, but a design where a requirement change touches a small, predictable set of modules.

## Key points

- Coupling describes how much one module knows about or depends on another module's internals; lower coupling reduces ripple effects.
- Cohesion describes how focused a module's responsibilities are; functional cohesion is the strongest classic level.
- The classic coupling levels from loosest to tightest are data, stamp, control, common, and content coupling.
- The classic cohesion levels from weakest to strongest are coincidental, logical, temporal, procedural, communicational, sequential, and functional.
- High cohesion and low coupling are complementary: moving logic to the module that owns the relevant data usually improves both.

## Your 60-second answer

Coupling is how much one module depends on another; cohesion is how focused the responsibilities inside a module are. Good design wants low coupling and high cohesion. Low coupling means you can change or replace one module without a cascade of changes elsewhere. High cohesion means a module does one logical thing, so it is easier to name, test, and reason about. A classic sign of trouble is a class that knows a collaborator's private data or that mixes persistence, validation, and business rules; that class is both tightly coupled and low in cohesion. The trade-off is that pushing for zero coupling is impossible: modules must talk to each other, so the practical goal is to couple to stable abstractions, not concrete implementations.

## If they dig deeper

**What is an example of tight coupling you would spot in a code review?**

A service that directly instantiates a concrete StripeClient and calls its methods is tightly coupled to that client. If StripeClient changes its constructor or method signatures, the service must change, and you cannot swap in a fake for tests without changing production code.

**What are the classic levels of coupling from loosest to tightest?**

The levels are data, stamp, control, common, and content. Data coupling passes only simple data through parameters; stamp coupling passes a whole record; control coupling passes a flag that changes behavior; common coupling shares global state; content coupling reaches into another module's internals.

**What are the classic levels of cohesion from weakest to strongest?**

They run from coincidental, logical, temporal, procedural, communicational, sequential, to functional. A functionally cohesive module performs one well-defined task with all parts contributing to that task; a coincidentally cohesive module groups unrelated tasks just because they happen to be in the same file.

**How would you refactor a class that has both low cohesion and tight coupling?**

I would first split it along responsibility boundaries, such as validation, persistence, and business workflow. Then I would define interfaces for its external collaborators and inject them through the constructor, so the class depends on abstractions rather than concrete implementations.

**What is connascence, and how does it refine the idea of coupling?**

Connascence measures coupling by asking: if one module changes, must another module change to stay correct? It classifies coupling by strength and locality—connascence of name is weaker than connascence of meaning, and strong connascence across module boundaries is more harmful than within one module.

## Worked example

Consider an OrderService that inside placeOrder creates a StripeGateway, calls stripe.charge(...), writes a row through a raw database connection, and formats an email body. That module has low cohesion: it mixes payment processing, persistence, and notification. It is also tightly coupled to Stripe's concrete API and a specific database driver; any change to either breaks OrderService. Refactor by extracting a PaymentGateway interface with a charge method, an OrderRepository interface with a save method, and a NotificationSender interface with a send method. OrderService now accepts these three interfaces in its constructor and coordinates their calls. The Stripe-specific logic lives behind StripePaymentGateway, and the database-specific code lives in a repository. If Stripe's API changes, only one class changes, and tests can pass fakes for the interfaces.

## Common traps

- Treating 'low coupling' as 'no dependencies' and creating a tangle of indirection, event buses, or configurable plugins for what should be one direct call.
- Equating high cohesion with many tiny classes, so a simple feature gets fragmented across dozens of classes that hide the actual workflow.
- Calling a class cohesive because its methods all share the same noun, even when they change for unrelated reasons.
- Measuring only syntactic coupling, such as number of imports, while ignoring semantic coupling where two modules change together for the same business reason.

</details>

---

## 18. Interfaces · mcq · Medium

*lld · gate confidence 0.5*

**Question**

Which statement about static methods in Java interfaces is correct?

**Options**

- They are called on the interface name and are not inherited by implementing classes
- They are inherited by implementing classes and can be overridden
- They are called on an instance and can access instance fields
- They are identical to default methods except they cannot be called from implementing classes

**Reference answer**

They are called on the interface name and are not inherited by implementing classes

**Graded on**

- called on the interface name
- not inherited
- not overridden

<details><summary>The lesson this came from</summary>

An interface is a named set of method signatures—and, in modern Java and C#, possibly default, static, or private methods—that a class agrees to implement. It specifies what operations are available without dictating how an object stores its state. In Java a class uses `implements` to satisfy an interface; in C++, the same contract is expressed as an abstract class containing only pure virtual functions; in Python, abstract base classes with `@abstractmethod` serve the role. A class can implement many interfaces, giving multiple inheritance of type rather than state.

## Why interviewers ask this

Interviewers ask about interfaces to test whether you can define stable abstractions, decouple callers from concrete implementations, and explain the trade-offs with abstract classes and multiple inheritance. They may follow up on language-specific evolution such as Java 8 default methods or C# 8 default interface members. The signal is design judgement under change, not just syntax.

## The core idea

An interface is a contract: callers depend on the methods it declares, not on a particular class. Implementing many interfaces lets a type expose several roles while avoiding the diamond problem of stateful multiple inheritance, because Java and C# interfaces cannot declare instance fields. Since Java 8 and C# 8, interfaces can also provide default method bodies, so a new method can be added without breaking existing implementers. Historically interfaces had only public abstract members, but Java 9 and C# 8 allow non-public members such as private methods; non-public members are no longer unique to abstract classes. Still, an abstract class can hold instance state and constructors, which an interface cannot.

## Key points

- In Java, a class uses `implements` to satisfy an interface and may implement multiple interfaces while extending only one class.
- Java 8 added `default` and `static` methods to interfaces, and Java 9 added `private` and `private static` methods for sharing code inside the interface.
- C# 8 added default interface implementations and non-public access modifiers such as private, protected, and internal, but interfaces still cannot declare instance fields.
- C++ has no `interface` keyword; an interface is an abstract class with only pure virtual functions (`= 0`) and a virtual destructor.
- Interfaces enable polymorphic dispatch: client code depends on the interface type and can receive any implementation, improving testability and loose coupling.

## Your 60-second answer

An interface is a contract that defines a set of method signatures a class must implement. In Java, I would declare `interface Payment { void pay(double amount); }` and then have `class CreditCardPayment implements Payment`. Client code depends on `Payment`, not on a concrete card class, so I can swap in PayPal or a test double without changing callers. A class can implement many interfaces—say `Flyable` and `Drivable`—which gives multiple inheritance of type without multiple inheritance of state. The main trade-off is that an interface cannot hold instance fields or constructors, so shared state still belongs to an abstract class or composition. Modern Java and C# have blurred the line with default and private interface methods, but an interface still defines capability, not object state.

## If they dig deeper

**What is the difference between an interface and an abstract class?**

An interface defines a contract with method signatures and, in modern Java and C#, may include default, static, or private methods, but it cannot hold instance state or constructors. An abstract class can have state, constructors, and non-public members; however, since Java 9 and C# 8 interfaces also support non-public members, the remaining key differences are state and constructors.

**Why does Java allow multiple interface inheritance but not multiple class inheritance?**

Multiple class inheritance creates ambiguity and the diamond problem for state and method dispatch, because a class would inherit more than one copy of instance data. Java interfaces do not hold instance state, so implementing many interfaces only combines method contracts; default method conflicts are resolved by explicit override rules.

**What changed in Java 8 regarding interfaces, and why was that change made?**

Java 8 added default and static methods to interfaces so existing interfaces like `Collection` could gain new methods such as `stream()` without breaking every implementing class. Default methods provide a fallback implementation that classes can override.

**How are default method conflicts resolved when a class implements two interfaces with the same default method?**

If two unrelated interfaces provide the same default method signature, the implementing class must override the method and can explicitly delegate to one interface's default using `InterfaceA.super.method()`. If one interface inherits from the other, the more specific interface's default wins.

**When would you prefer composition over implementing many interfaces?**

Interfaces describe capabilities but do not share state or implementation. Composition lets you delegate behavior to collaborator objects, making the relationship changeable at runtime and avoiding inheriting unwanted methods; many design guidelines favor composition over inheritance while still using interfaces for polymorphism.

## Worked example

Suppose a checkout service depends on a `PaymentProcessor` interface with `ChargeResult charge(Money amount)`. It receives a `CreditCardProcessor` at runtime but the code only knows `PaymentProcessor`. Adding a `BankTransferProcessor` that implements the same interface requires no change to checkout logic—this is the open/closed principle. In Java, the interface declares the method signature and each concrete class uses `implements PaymentProcessor`; in C++, the same contract is an abstract class with `virtual ChargeResult charge(Money amount) = 0;` and classes inherit from it. The call site's static type is the interface, and virtual dispatch chooses the correct implementation.

## Common traps

- Saying interfaces cannot have any method bodies, when Java 8 and C# 8 allow default methods with implementation in the interface.
- Claiming non-public members are unique to abstract classes; Java 9 and C# 8 allow private interface methods.
- Confusing multiple interface inheritance with multiple inheritance of state—interfaces do not give a class multiple copies of instance fields.
- Forgetting that the implementing class must resolve conflicting default methods from two unrelated interfaces.

</details>

---

## 19. Adapter Pattern · flash · Easy

*lld · gate confidence 0.5*

**Question**

What is the key difference between an object adapter and a class adapter?

**Reference answer**

An object adapter uses composition (holding an adaptee instance), while a class adapter uses multiple inheritance from both target and adaptee, and therefore only works in languages that support multiple inheritance.

**Graded on**

- Object adapter uses composition
- Class adapter uses multiple inheritance
- Class adapter requires multiple inheritance support
- Object adapter can adapt subclasses

<details><summary>The lesson this came from</summary>

The Adapter pattern is a structural design pattern that lets two incompatible interfaces work together. It introduces an adapter class that implements the target interface a client depends on and holds a reference to the existing class, called the adaptee. Each target method delegates to one or more adaptee calls, rewriting method names, reordering parameters, converting types, and translating exceptions. The client continues to program against the target interface, unaware of the adaptee's different API.

## Why interviewers ask this

Interviewers use this to test whether you can integrate legacy or third-party code without rewriting it or coupling the client to its details. The pattern is a concrete application of the dependency inversion and open/closed principles: new code depends on abstractions, and existing working code stays closed for modification. It also reveals whether you can separate interface mismatch from behavioral change.

## The core idea

The heart of the Adapter pattern is delegation with translation. Define the interface the client already knows, the target. Put the incompatible existing class, the adaptee, behind a new class that inherits from the target and holds an adaptee instance. In each target method, call the appropriate adaptee method or methods, converting as needed. This preserves the client's code and the adaptee's code untouched. Object adapters rely on composition and are the usual choice in Java and Python; class adapters inherit from both target and adaptee and require a language that permits multiple inheritance, such as C++. The adaptee has no knowledge of the adapter.

## Key points

- An object adapter implements the target interface and holds a reference to the adaptee; it translates calls by delegation.
- Class adapters use multiple inheritance from target and adaptee and only work in languages that support it, such as C++.
- The client code is written against the target interface, so swapping adapters or replacing the adaptee later does not change client code.
- Adapter resolves interface mismatch: different method names, argument order or count, data formats, and exception types.
- Adapter should not be used to add behavior beyond adaptation or to hide a complex subsystem; those are Decorator and Facade, respectively.

## Your 60-second answer

The Adapter pattern converts the interface of an existing class into the interface a client expects. You create an adapter class that implements the target interface and holds a reference to the legacy or third-party class, the adaptee. Each target method delegates to one or more adaptee methods, reordering arguments, converting types, or renaming calls. You reach for it when two pieces of working code have incompatible interfaces and you don't want to change either, especially when the client is already coded against an abstraction. The benefit is that client and adaptee stay decoupled, and you can swap in another adapter later. The cost is an extra layer of indirection, and if every integration gets its own adapter the design can become harder to trace. In Java, use object composition; class adapters need multiple inheritance and are mainly a C++ option.

## If they dig deeper

**What are the four participants in the Adapter pattern?**

Target is the interface the client uses; adaptee is the existing class with the incompatible interface; adapter implements target and wraps adaptee; client depends only on target.

**What is the difference between object adapter and class adapter?**

An object adapter uses composition, holding an adaptee instance, so it can adapt the class and any subclasses. A class adapter uses multiple inheritance from target and adaptee, which can override adaptee behavior, but only works in languages with multiple inheritance, like C++.

**Can you sketch an Adapter for a legacy payment gateway?**

Define a PaymentProcessor target with process_payment(amount, currency). A LegacyGateway may have make_payment(currency, amount). The adapter stores a LegacyGateway and implements process_payment by calling legacy.make_payment(currency, amount), possibly converting amount to cents and catching legacy exceptions.

**When would you choose Adapter over Facade or Decorator?**

Use Adapter when interfaces differ and the client expects a specific contract. Facade provides a simplified interface over a complex subsystem, not for interface mismatch. Decorator adds behavior while preserving the interface, not converting it.

**How do you handle differences in error handling and unsupported operations when adapting?**

The adapter should translate adaptee-specific exceptions into ones the target client already knows, so the legacy details don't leak. For operations the adaptee cannot support, either throw a documented UnsupportedOperationException at the target level or implement a reasonable default, but don't silently swallow errors.

## Worked example

A checkout service is written against PaymentProcessor with process_payment(amount, currency). A legacy gateway only offers make_payment(currency, amount) with amounts in cents. The adapter implements PaymentProcessor, stores a LegacyGateway, and in process_payment calls legacy.make_payment(currency, int(amount * 100)). The client's call process_payment(25.50, 'USD') becomes make_payment('USD', 2550) inside the adapter. If the legacy gateway raises LegacyGatewayError, the adapter catches it and raises PaymentProcessorError, so the client sees a consistent exception type. The legacy class never changes, and the checkout service remains unaware of its method names or parameter order.

## Common traps

- Modifying the adaptee or client instead of inserting an adapter, which propagates brittle changes and violates the open/closed principle.
- Using Adapter to add new behavior or to simplify many calls into one when the interface is unchanged; that indicates Decorator or Facade.
- Letting adaptee-specific exceptions or data formats escape the adapter, so clients learn about the legacy API.
- Creating a single adapter that handles several unrelated adaptees, which concentrates integration logic and becomes hard to maintain.

</details>

---

## 20. Decorator Pattern · output · Easy

*lld · gate confidence 0.5*

**Question**

What is printed by this Java snippet?
```java
interface Beverage { int cost(); }
class DarkRoast implements Beverage { public int cost() { return 200; } }
class Mocha implements Beverage {
    private Beverage b;
    Mocha(Beverage b) { this.b = b; }
    public int cost() { return 30 + b.cost(); }
}
class Whip implements Beverage {
    private Beverage b;
    Whip(Beverage b) { this.b = b; }
    public int cost() { return 20 + b.cost(); }
}
System.out.println(new Whip(new Mocha(new DarkRoast())).cost());
```

**Reference answer**

250

**Graded on**

- DarkRoast cost is 200
- Mocha adds 30
- Whip adds 20
- outermost Whip adds its cost first, total 250

<details><summary>The lesson this came from</summary>

The Decorator pattern wraps an object in another object that implements the same interface, intercepting calls and adding behavior before or after delegating to the wrapped object. Clients interact with the wrapper exactly as they would with the original component, so behavior can be added dynamically without changing the wrapped class. Multiple wrappers can be nested to combine behaviors, and each wrapper is responsible for one added concern.

## Why interviewers ask this

Interviewers ask about Decorator to test whether you can extend object behavior without an explosion of subclasses and without modifying working code. The pattern demonstrates comfort with object composition, interface contracts, and open/closed design, which are core LLD signals. A follow-up often pushes on runtime composition, ordering, or how this differs from inheritance.

## The core idea

Decorator works because the wrapper has the same type as the object it wraps. When a client calls a method, the outer wrapper performs its added concern, delegates the same call to the inner object, and may post-process the result. Nesting several wrappers builds a delegation chain, so behavior is composed at runtime rather than fixed at compile time. The wrapped classes remain unchanged, satisfying the open/closed principle. The pattern is an example of favoring composition over inheritance for extending behavior. The cost is that wrapper order can matter and many small classes are produced.

## Key points

- The decorator and the component it wraps implement the same interface, so a decorated object can be used anywhere the original is expected.
- Each decorator holds a reference to another component and typically adds behavior before or after delegating the call.
- Decorators can be nested in arbitrary order at runtime; the resulting behavior is determined by that order.
- Adding a decorator does not require modifying the decorated class, preserving the open/closed principle.
- Java's I/O streams use decorators: BufferedInputStream wraps an InputStream to add buffering while remaining an InputStream to clients.

## Your 60-second answer

The Decorator pattern adds behavior to an object at runtime by wrapping it in another object that implements the same interface. The wrapper holds a reference to the original object, so it can do extra work before or after delegating the call. Because the wrapper has the same type, clients don't know whether they are using the plain object or a decorated chain. That lets you compose behaviors like buffering, logging, or encryption by nesting wrappers, instead of creating a subclass for every combination. The big payoff is that you keep classes open for extension but closed for modification, and you can choose features dynamically. The trade-off is that you get many small wrapper classes and the behavior can depend on wrapper order, which makes debugging and reasoning harder. In Java I/O, for example, a BufferedInputStream decorating an InputStream is exactly this idea.

## If they dig deeper

**What is the Decorator pattern and what problem does it solve?**

It attaches additional responsibilities to an object dynamically by wrapping it in another object that shares its interface. The wrapper delegates to the inner object while adding behavior before or after the call. This avoids the combinatorial explosion of subclasses when many independent features can be mixed.

**How is using a decorator different from simply subclassing a concrete class to add behavior?**

Subclassing creates a new type at compile time for each combination of features, which becomes unmanageable as options grow. A decorator uses object composition, so features are selected and ordered at runtime and the original class is not modified. You often still use an interface or abstract class, but each added behavior lives in its own wrapper.

**Why must a decorator both implement the same interface and hold a reference to the wrapped object?**

The shared interface preserves substitutability: client code that expects a Component can accept the wrappers without change. The reference is how the decorator forwards the core behavior to the wrapped object; without it, the original behavior would be lost. Both pieces together give behavior add-on with transparent delegation.

**Can you describe a situation where decorator order changes the result?**

Yes, compression and encryption are the classic case. If you need to compress before encrypting, an outer Encryptor wrapping an inner Compressor yields encrypt(compressed(plaintext)); swapping the order yields compressed(encrypted) data, which is not the same and may be unusable. In the call stack, the outermost wrapper runs first, so wrapper order is part of program semantics.

**What are the real-world downsides of relying heavily on decorators, and when should you avoid them?**

Heavy use creates many small wrapper classes, deep call stacks, and code that checks concrete types may break because the object is now a wrapper chain. Order-sensitive behavior and extra allocation/indirection are also costs. If the possible extensions are fixed and simple at compile time, plain inheritance or direct modification may be clearer.

## Worked example

A coffee order system has a Beverage interface with a cost() method. DarkRoast implements Beverage and returns 200 cents. A Mocha decorator also implements Beverage, holds a Beverage, and returns 30 plus the wrapped cost. A Whip decorator does the same with 20. Building new Whip(new Mocha(new DarkRoast())) creates a chain: calling cost() on Whip returns 20 plus Mocha.cost(), which returns 30 plus DarkRoast.cost(), which returns 200; the total is 250. The client only sees a Beverage, and adding another shot of Mocha requires wrapping again, not editing any class.

## Common traps

- Forgetting to delegate from the decorator to the wrapped component, which silently drops the original behavior.
- Writing code that uses instanceof or casts to the concrete class, which breaks once the object is wrapped and should rely on the interface instead.
- Assuming wrapper order does not matter; some features such as encryption and compression are order-dependent.
- Creating a decorator for every minor variant instead of composing a few meaningful wrappers, which produces excessive small classes and obscure behavior.

</details>

---

## 21. Execution plans · mcq · Medium

*sql · gate confidence 0.5*

**Question**

A query returns 95% of the rows from a large table and the optimizer uses a sequential scan. Why is this often the correct choice rather than an index scan?

**Options**

- An index scan would cause many random heap fetches, making it more expensive than reading sequentially
- The optimizer cannot use an index when the table is large
- Sequential scan is always faster for large tables
- Stale statistics force the optimizer to ignore indexes

**Reference answer**

An index scan would cause many random heap fetches, making it more expensive than reading sequentially

**Graded on**

- sequential scan can beat index scan when returning most rows
- index scan causes random heap fetches
- not automatically a problem

<details><summary>The lesson this came from</summary>

An execution plan is the set of physical operators the database optimizer chooses to run a query. It names the access method for each table (sequential scan, index scan, index seek), the join algorithm, sort or aggregate steps, and the order of operations. Plans also carry estimated row counts, actual row counts when executed, and relative costs. In PostgreSQL these appear via EXPLAIN and EXPLAIN ANALYZE, in MySQL via EXPLAIN, and in SQL Server as graphical or XML plans.

## Why interviewers ask this

The interviewer is testing whether you can diagnose a slow query from the plan instead of guessing. They want to see that you can trace data flow from leaves to root, compare estimated and actual row counts, and connect expensive operators to missing indexes, stale statistics, join choice, or an inherently large result.

## The core idea

A plan shows the optimizer's physical contract: which indexes are used, how tables are joined, and in what order. The fastest way to find a bottleneck is to locate the operator with the largest actual time or the largest gap between estimated and actual rows. That gap often compounds into the wrong join algorithm, excessive memory use, or extra I/O. Fixes follow from the cause: update statistics, add or change an index, rewrite a non-sargable predicate, or sometimes force a different plan.

## Key points

- In PostgreSQL, EXPLAIN shows estimated cost, rows, and width; EXPLAIN ANALYZE executes the statement and adds actual time and rows per operator.
- A sequential scan is not automatically bad: for small tables or when a query returns most of a table, it can beat an index scan that causes random heap fetches.
- A large gap between estimated and actual rows is a primary signal for stale statistics or correlated predicates, and it should be checked before other tuning work.
- The most expensive operator is not always the root cause; look for the earliest point where rows explode or a bad estimate forces a downstream operator to do far more work.
- Common plan-driven fixes are updating statistics, adding a covering index, rewriting predicates to be sargable, and changing join order or join algorithm.

## Your 60-second answer

An execution plan is the database's chosen physical recipe for a query: which tables are scanned or index-seeked, how they are joined, and how rows are filtered and sorted. I read it from the leaves upward, first finding the operator with the largest actual time or actual-vs-estimated row gap. For example, if PostgreSQL shows a nested loop with a million loops and an inner index scan, the planner may have expected only a few outer rows. A big gap usually means stale statistics or a predicate that hides correlation. The fix might be ANALYZE, a covering index, or rewriting the predicate so the optimizer can use it. The trade-off is that adding an index speeds reads but adds write overhead, and it will not help if the query still fetches most of the table.

## If they dig deeper

**What is the difference between an estimated and an actual execution plan?**

An estimated plan is generated without running the query, using statistics and cost models to predict rows and costs. An actual plan runs the query and records real row counts, execution counts, and timings. Actual plans are how you detect that the optimizer guessed wrong.

**How do you read a PostgreSQL EXPLAIN ANALYZE output?**

Start from the innermost indented nodes and move outward, because each outer node consumes what the inner nodes produce. Compare the estimated rows with actual rows and check the actual time and loops fields. The buffers field also tells you whether an operator is doing a lot of disk or shared-buffer I/O.

**If a plan shows a sequential scan and the query is slow, what do you check before adding an index?**

Check the table size and how selective the filter really is. If the query returns a large fraction of the table, the sequential scan may be cheaper than random heap fetches from an index. Also check whether the predicate is sargable: a function wrapped around the indexed column can prevent index use entirely.

**What are the main join algorithms, and when does each perform poorly?**

Nested loop is good for a small outer input and an index on the inner join key, but it degrades when the outer side is large and the inner lookup is expensive. Hash join handles large equality joins well but can spill to disk when memory is insufficient. Merge join can stream sorted inputs efficiently but requires both sides to be sorted, which may add sort costs.

**How can the same query get a good plan for one parameter value and a terrible plan for another?**

SQL Server calls this parameter sniffing: the optimizer compiles the plan using the first parameter value supplied, then reuses it for later values. If those values differ in selectivity, the plan can be wrong. PostgreSQL prepared statements may also use a generic plan after several executions, so a plan that suits average rows can be bad for an extremely selective or extremely broad value.

## Worked example

Suppose a PostgreSQL query joins 1,000,000 orders to 100,000 customers on customer_id and filters orders to the last 30 days. EXPLAIN ANALYZE shows a hash join with a sequential scan on orders returning 500,000 actual rows, where the planner estimated 5,000. Because the date statistics do not capture that recent orders are heavily overrepresented, the hash table is much larger than planned and spills to disk. The right first step is to run ANALYZE on orders; with better statistics the planner may choose an index scan on the order date, reducing both the build-side input and the join cost. The example illustrates that fixing the estimate error often fixes the expensive operator without adding a new index.

## Common traps

- Assuming a sequential scan is always a problem and adding an index will automatically make the query faster.
- Stopping at the most expensive operator without checking whether a bad row estimate upstream caused it.
- Reading only the estimated plan after the query runs, when an actual plan would show the real row-count error.
- Comparing cost numbers across different plans or servers as if they were milliseconds; costs are relative units within one plan.

</details>

---

## 22. Correlated vs nested subqueries · typed · Medium

*sql · gate confidence 0.5*

**Question**

Explain why a correlated subquery cannot be evaluated once and reused, unlike an independent nested subquery.

**Reference answer**

Because its predicate references a column from the outer query, so the inner result depends on the current outer row. It is logically evaluated once for each outer row, and each evaluation can produce a different result.

**Graded on**

- references outer column
- result depends on current outer row
- logically evaluated per outer row
- no single reusable result

<details><summary>The lesson this came from</summary>

A nested, non-correlated subquery is an inner SELECT with no reference to any outer query column, so the database can evaluate it once and use its result as a scalar, list, or derived table. A correlated subquery contains a reference to one or more columns from the outer query, so its result depends on the current outer row and it is logically evaluated once for each outer row. The distinction is about dependency, not the depth of nesting.

## Why interviewers ask this

Interviewers ask this to check whether you can reason about SQL execution order and cost. They want to see that you know an independent inner query runs once while a correlated query may be re-evaluated for each outer row, and that you can choose among a subquery, join, or window function.

## The core idea

The definition is dependency: if the inner query references an outer column, it is correlated; otherwise it is an independent nested subquery. An independent subquery can be evaluated once and its result reused; a correlated one cannot be precomputed because its predicate changes for each outer row. Many engines have optimizers that may decorrelate EXISTS and some scalar subqueries into semi-joins or outer joins, so 'once per row' is a logical model, not always physical reality. For row-dependent checks such as finding each employee's department maximum, a correlated subquery is clear, but a join or window function often avoids repeated aggregate scans.

## Key points

- A nested (non-correlated) subquery has no outer-column reference and is logically evaluated once.
- A correlated subquery references at least one outer column and is logically evaluated for each row of the outer query.
- Correlated subqueries are typical with EXISTS or NOT EXISTS, where the inner query tests related rows such as an employee's orders.
- Because correlated subqueries can cause repeated scans, joins or window functions are often used to compute the same result in fewer passes.
- Correlation is decided by column resolution, not by the keyword NESTED or by how deeply the subquery appears.

## Your 60-second answer

A correlated subquery references columns from the outer query, while a nested, non-correlated subquery is independent and references no outer columns. The independent subquery can be run once and its result used by the outer query; the correlated subquery logically runs once for every outer row because its predicate depends on that row. For example, WHERE salary > (SELECT AVG(salary) FROM employees) is non-correlated, but WHERE salary = (SELECT MAX(salary) FROM employees e2 WHERE e2.dept_id = e.dept_id) is correlated because the inner MAX is scoped to the outer row's department. Correlated subqueries are convenient for row-by-row existence checks like EXISTS, but they can be expensive on large tables, so engineers often rewrite them with a single join or a window function such as ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC).

## If they dig deeper

**Which part executes first when the subquery is non-correlated?**

The inner query executes first because the outer query depends on its result. In practice the optimizer may merge the two into a join or rewrite the plan, but logically the independent subquery is evaluated once before the outer predicate is applied.

**When would you use a correlated subquery instead of a join?**

Use a correlated subquery when the condition is a row-dependent existence or anti-existence test, such as EXISTS or NOT EXISTS, especially if you do not need to return columns from the related table. It often expresses the intent more directly than a self-join. For large tables, though, a join or window function may perform better.

**Why are correlated subqueries often slower, and how do you improve them?**

Logically, each outer row triggers an evaluation of the inner query, which can lead to repeated scans of the inner table and O(n*m) work. If the optimizer cannot decorrelate it, rewrite using a grouped subquery joined once or a window function that computes the needed aggregate in a single pass.

**Can a subquery reference a column from more than one level up?**

Yes. In nested query blocks, a correlated subquery can resolve column references against any enclosing query scope, not only the immediately outer one. That makes it dependent on each referenced level, and logical evaluation is per row of those outer levels.

**How does a query optimizer decorrelate a correlated subquery?**

The optimizer converts the correlated predicate into a join condition between outer and inner row sources. EXISTS becomes a semi-join, NOT EXISTS becomes an anti-join, and scalar subqueries may become left outer joins with handling for empty results; this lets inner rows be read once. Decorrelation is not guaranteed, especially with complex aggregates or nested subqueries, so some engines fall back to per-row evaluation.

## Worked example

Take employees(emp_id, dept_id, salary). A correlated query is: SELECT emp_id FROM employees e WHERE salary = (SELECT MAX(salary) FROM employees e2 WHERE e2.dept_id = e.dept_id); For each outer employee, the inner aggregate rescans the employee table filtered to that employee's department. If all 1,000 employees are in one department, the max is computed 1,000 times over 1,000 rows. A window rewrite is: SELECT emp_id FROM (SELECT emp_id, salary, MAX(salary) OVER (PARTITION BY dept_id) AS dept_max FROM employees) t WHERE salary = dept_max; This computes the department maximum once in the window function and then filters, avoiding repeated scans. The same result can also be produced by joining once to a grouped subquery on (dept_id, MAX(salary)).

## Common traps

- Equating 'nested' with 'correlated': a subquery can be deeply nested and still non-correlated; correlation is determined only by outer-column references.
- Claiming a correlated subquery always physically runs once per row; many database engines decorrelate EXISTS and some scalar subqueries into semi-joins or joins.
- Using a correlated aggregate subquery when a window function or grouped join returns the same result in fewer scans.
- Writing an inner reference without an alias so both columns resolve to the inner table, silently changing a correlated query into an independent one.

</details>

---

## 23. Aggregate functions · flash · Easy

*sql · gate confidence 0.5*

**Question**

What is an aggregate function in SQL?

**Reference answer**

It consumes a set of rows—the whole table or a group produced by GROUP BY—and returns one scalar value per group.

**Graded on**

- consumes set of rows
- returns one scalar per group
- without GROUP BY the whole table is one group

<details><summary>The lesson this came from</summary>

An aggregate function consumes a set of rows—either the whole table or a group produced by GROUP BY—and returns one scalar value for that set. The core ones are COUNT, SUM, AVG, MIN, and MAX. In standard SQL engines, SUM, AVG, MIN, and MAX ignore NULL input values; COUNT has multiple behaviours: COUNT(*) counts all rows, COUNT(column) counts only non-NULL values, and COUNT(DISTINCT column) counts distinct non-NULL values.

## Why interviewers ask this

Aggregate functions are the basic mechanism for reducing row sets, so the interviewer is testing whether you can reason in groups rather than rows. They probe NULL semantics, WHERE versus HAVING placement, and the rules for which columns may appear alongside GROUP BY.

## The core idea

Aggregation is a reduction that turns row sets into single values per group. With no GROUP BY, the whole table is one group. With GROUP BY, rows sharing the grouping keys form buckets, and each bucket emits one row; columns in SELECT must either be grouped, be inside an aggregate, or be functionally dependent on the grouped columns in SQL:1999-compliant engines. WHERE filters individual rows before aggregation, while HAVING filters whole groups after aggregation. Null handling matters every time: an aggregate over an empty or all-NULL set returns NULL, except COUNT returns 0.

## Key points

- Every aggregate returns one scalar per group; without GROUP BY the entire table is treated as a single group.
- COUNT(*) counts rows, COUNT(col) counts non-NULL values, and COUNT(DISTINCT col) counts distinct non-NULL values.
- SUM, AVG, MIN, and MAX ignore NULL inputs; AVG divides by the number of non-NULL values, not by COUNT(*).
- WHERE filters rows before aggregation, while HAVING filters groups after aggregation.
- Standard SQL since SQL:1999 allows a non-aggregated SELECT column to be omitted from GROUP BY only if it is functionally dependent on the grouped columns; PostgreSQL 9.1+ and MySQL with ONLY_FULL_GROUP_BY enforce this, while SQL Server does not allow the extension.

## Your 60-second answer

An aggregate function collapses a set of rows into one scalar. COUNT(*) returns the number of rows in the set. COUNT(column) counts only non-NULL values, and COUNT(DISTINCT column) counts distinct non-NULL values. SUM, AVG, MIN, and MAX ignore NULL inputs, and AVG divides the sum by the count of non-NULL values. Without GROUP BY, the whole table is one group; with GROUP BY, each group produces one output row, and every selected column must either appear in GROUP BY, be inside an aggregate, or be functionally dependent on the grouping columns in engines that implement the SQL standard rule. HAVING filters after aggregation, WHERE filters before it. The main trade-off is that aggregates discard row detail for summary, and null handling can create surprises—COUNT(*) counts rows with NULLs while COUNT(column) skips them.

## If they dig deeper

**What is the difference between COUNT(*) and COUNT(column)?**

COUNT(*) returns the total number of rows in the group, including rows where every field is NULL. COUNT(column) returns the number of rows where that column is not NULL, and COUNT(DISTINCT column) returns the number of distinct non-NULL values in that column.

**When do you filter with WHERE versus HAVING?**

WHERE filters individual rows before any grouping or aggregation, so it cannot reference aggregate function results. HAVING filters the groups after aggregation and can use conditions such as HAVING SUM(amount) > 1000. Both can appear in the same query.

**Why does SQL reject SELECT dept_id, name, COUNT(*) FROM employees GROUP BY dept_id, and are there exceptions?**

The name column is not a grouping column and not inside an aggregate, so it has no single value per group. Standard SQL since SQL:1999 allows such a column only if it is functionally dependent on the grouped columns—for example, if dept_id is a unique key of the table. PostgreSQL and MySQL with ONLY_FULL_GROUP_BY implement that relaxation; SQL Server still requires every selected column to be grouped or aggregated.

**What does AVG return when a column contains only NULLs or the input set is empty?**

AVG returns NULL when all input values are NULL, because the sum of non-NULL values divided by zero non-NULL rows is undefined in SQL. If a query has no groups and the table is empty, the aggregate also returns NULL, while COUNT returns 0. If the query is grouped, an empty group does not produce an output row.

**Can you nest aggregate functions, like MAX(SUM(salary))?**

No, SQL does not allow directly nesting aggregate functions in the same SELECT or HAVING list because the inner aggregate would need to be computed per group while the outer computes over groups. You can compute the inner aggregate in a subquery or CTE, then apply the outer aggregate to that result.

## Worked example

Consider a sales table with rows (region, amount): ('North', 100), ('North', NULL), ('South', 50), ('South', 150). The query SELECT region, COUNT(*), COUNT(amount), SUM(amount), AVG(amount), MIN(amount), MAX(amount) FROM sales GROUP BY region yields two rows. For North, COUNT(*) is 2 because there are two input rows, COUNT(amount) is 1 because the NULL is ignored, SUM and AVG are both 100, and MIN and MAX are both 100. For South, COUNT(*) is 2, COUNT(amount) is 2, SUM is 200, AVG is 100, MIN is 50, and MAX is 150. The NULL disappears from the numeric aggregates but still contributes to the row count.

## Common traps

- Using HAVING for a row-level condition, such as HAVING salary > 100000, when WHERE should filter rows before aggregation.
- Assuming AVG divides by COUNT(*) or treats NULLs as zeros; it ignores NULLs entirely.
- Forgetting that MIN and MAX also ignore NULLs, so MIN over a column with NULLs does not return NULL unless every value is NULL.
- Selecting a non-grouped column without checking for functional dependency, which fails in strict engines and can return some indeterminate row's value in MySQL without ONLY_FULL_GROUP_BY.

</details>

---

## 24. Design a web crawler · flash · Medium

*system_design · gate confidence 0.5*

**Question**

How does a crawler recover URLs that were in-flight when a worker crashed?

**Reference answer**

Workers hold a timed lease or timestamp for in-flight URLs; if the lease expires without completion, the URL is reassigned to the pending state for another worker.

**Graded on**

- in-flight state
- timed lease or timestamp
- timeout
- reassign to pending

<details><summary>The lesson this came from</summary>

A web crawler is a distributed system that starts from seed URLs, fetches pages over HTTP, parses them to extract links, and schedules newly discovered URLs for later fetching. It must maintain a frontier of pending URLs, store visited URLs to avoid cycles, respect per-domain robots.txt and rate limits, and support re-crawling content that changes over time. The core components are the URL frontier/scheduler, fetcher workers, parser, and a durable seen-URL store with a Bloom filter in front for fast negative acceptance.

## Why interviewers ask this

The interviewer is testing whether you can design a scalable graph traversal that runs across many machines, avoids fetching the same page repeatedly, and is polite to target sites. Real questions at Amazon, Google, Facebook, and Atlassian probe URL deduplication, per-domain delays, and prioritization because those are the parts where naive designs break under billions of pages. The follow-up sequence typically moves from basic scheduling to exact dedup and politeness.

## The core idea

A crawler is a distributed BFS with a priority queue instead of a simple FIFO. The URL frontier stores pending URLs, usually partitioned by domain so each worker can enforce a per-domain fetch delay without coordination. Before fetching, a worker checks a Bloom filter: a negative is definitive proof the URL has not been seen, so it can proceed; a positive requires a lookup in the durable seen-URL store to determine whether it is a true duplicate or a false positive. Once fetched, the page is parsed, links are canonicalized and run through the same dedup pipeline, and new URLs are enqueued with a priority score. Politeness is enforced by caching robots.txt rules and last-fetch timestamps per domain. Re-crawling is handled by storing last-crawl timestamps and scheduling a revisit based on how often the page changes or its site priority.

## Key points

- The URL frontier is a priority queue that can be partitioned by domain, letting workers enforce per-domain politeness without global coordination.
- A Bloom filter has no false negatives, so a negative result definitively means a URL is unseen and safe to fetch; a positive result must be checked against a durable exact store to rule out a false positive.
- robots.txt and crawl-delay rules should be cached and checked before each fetch, with per-domain last-access timestamps or token buckets to enforce delays and concurrency limits.
- Exact URL deduplication requires canonicalization (removing fragments, normalizing query order) and a durable store; content hashing can catch near-duplicate pages.
- Re-crawling is scheduled from last-crawl timestamps and priority; high-value or frequently changing pages get shorter revisit intervals, not a global fixed period.

## Your 60-second answer

A web crawler is a distributed graph traversal. A frontier holds pending URLs, workers fetch and parse pages, extract links, and enqueue new URLs while deduplicating against everything already seen. The dedup pipeline uses a Bloom filter in front of a durable URL store: because a Bloom filter has no false negatives, a negative answer is definitive and lets us fetch immediately; a positive answer means the URL is likely seen, so we query the store to check whether it is a true duplicate or a false positive. Politeness is enforced per domain: workers check cached robots.txt rules, crawl delay, and concurrency caps before each fetch. For re-crawling, I would store last-fetch timestamps and schedule faster for high-priority domains like news. The core tradeoff is freshness versus politeness and load: crawling aggressively gives fresher results but can overload target sites and your own infrastructure.

## If they dig deeper

**Should the crawler be real-time or periodic?**

For most search or archival crawlers, periodic or incremental crawling is enough; real-time crawling matters only for news or price monitoring where freshness is a hard requirement. I would expose a crawl scheduling policy with priority and per-domain revisit intervals, treating real-time as a special high-frequency tier rather than the default.

**How do you handle URL deduplication?**

I use canonicalization first, then a Bloom filter in front of an exact URL store. A negative Bloom result is safe because Bloom filters produce no false negatives; a positive requires a database lookup to distinguish a true duplicate from a false positive. For content-level dedup I also store a hash of the normalized page content.

**What system do you use to track visited vs unvisited URLs?**

The crawler state is a small state machine: pending, in-flight, done, and failed, stored in a durable database or distributed queue. The frontier holds pending URLs; workers mark URLs in-flight with a lease or timestamp so crashes can reassign them; after a successful fetch they move to done; after retryable errors they go back to pending with a backoff.

**How do you implement delay between requests to the same domain?**

Each worker checks a per-domain record in Redis or an equivalent store before fetching: the last request timestamp and current concurrency count. It also consults cached robots.txt for a crawl-delay directive; if the elapsed time since the last request is less than the required delay, the worker waits or re-queues. Concurrency caps and a token bucket prevent accidentally hammering a domain.

**How do you prioritize pages and support re-crawling?**

Priority is computed per URL from signals like site authority, PageRank, change frequency, or a user-provided seed quality. The frontier orders by score, with separate queues for high and low priority to avoid starvation. Re-crawling is scheduled by last-fetch timestamp and the same priority: news sites get revisits every few minutes, static pages every days or weeks; a scheduler re-enqueues URLs whose revisit interval has elapsed.

## Worked example

Suppose a seed URL https://news.example.com/politics enters the frontier. A worker first checks the Bloom filter; it returns negative, so the URL is certainly unseen, and the worker fetches the page. Parsing extracts 32 links; each link is canonicalized. One link is https://news.example.com/politics itself, so the Bloom filter returns positive and the durable store confirms it was already seen—this duplicate is discarded. Another link returns positive in the Bloom filter but the store has no record; that is a false positive, so the URL is inserted into the store and enqueued. Before fetching again from news.example.com, the worker checks the domain's robots.txt cache, which sets a crawl-delay of 3 seconds; if only 1 second has passed since the last request, the worker waits 2 more seconds before fetching.

## Common traps

- Treating the Bloom filter as an exact dedup store and skipping the backing database leads to dropping legitimate URLs because of false positives.
- Fetching all links in parallel without per-domain throttling violates robots.txt and can get the crawler banned; politeness is a per-domain control, not a global rate.
- Storing URLs without canonicalization means the same page with different fragments or query parameter order is fetched multiple times.
- Modeling crawler state as a simple boolean 'visited' loses in-flight and retry semantics; crashed workers leave URLs stuck or duplicated.

</details>

---

## 25. SQL vs NoSQL · typed · Medium

*system_design · gate confidence 0.5*

**Question**

How would you model recurring events in SQL for something like a calendar?

**Reference answer**

Store events once with a recurrence rule, expand recurring rules into concrete occurrences in application code or a materialized occurrences table, then join with one-off events and check overlap using e.start_time < :slot_end AND e.end_time > :slot_start.

**Graded on**

- Store recurrence rule, not each occurrence
- Expand into occurrences in app or materialized table
- Join one-off and expanded occurrences
- Overlap condition start < slot_end and end > slot_start

<details><summary>The lesson this came from</summary>

SQL databases, such as PostgreSQL, MySQL, and Oracle, store rows in tables with predefined columns and use primary/foreign keys and SQL joins to express relationships. NoSQL is an umbrella term for non-relational models: key-value stores like Redis and DynamoDB, document stores like MongoDB and Couchbase, wide-column stores like Cassandra and HBase, and graph databases like Neo4j and Neptune. SQL systems emphasize ACID transactions and ad hoc relational queries; NoSQL systems typically trade some of those guarantees for horizontal scaling, flexible schemas, or specialized access patterns.

## Why interviewers ask this

Interviewers use this to test whether you can map a service's data shape, query pattern, transaction boundaries, and scaling needs to a concrete store instead of defaulting to a buzzword. Real design prompts such as Google Calendar, Uber ETA, and stream/platform designs force the question: do you need joins and invariants, or keyed writes at high throughput? The signal is trade-off reasoning with named mechanisms, not memorized definitions.

## The core idea

Start with the workload, not the label. If entities have many-to-many relationships, ad hoc aggregation, or updates that must succeed or fail together, a relational database is usually the simplest correct choice. If access is almost always by a known key, attributes vary per item, or a single relational node cannot absorb the write/read volume, choose the NoSQL model that matches the access pattern: key-value for hot keys and caches, document for variable-shaped records, wide-column for time-series/event logs, graph for deep relationship traversal. The same system can be polyglot: orders in PostgreSQL, sessions in Redis, catalog in MongoDB, analytics in Cassandra. NoSQL does not automatically mean no transactions or no consistency; it means those guarantees are usually scoped and must be verified per database and operation.

## Key points

- SQL databases store rows in fixed-schema tables and enforce relationships through primary/foreign keys; SQL queries can join, aggregate, and filter across them.
- The four common NoSQL models are key-value (Redis, DynamoDB), document (MongoDB, Couchbase), wide-column/column-family (Cassandra, HBase), and graph (Neo4j, Neptune).
- SQL systems usually scale vertically first; horizontal scaling with read replicas and sharding is possible but adds operational complexity, while many NoSQL systems shard and replicate across nodes automatically.
- Many NoSQL systems trade full ACID cross-row guarantees for availability and throughput, exposing tunable consistency such as DynamoDB strongly consistent reads or Cassandra per-query consistency levels.
- Relational is usually right for transactions, joins, and evolving ad hoc queries; NoSQL is usually right for keyed access, variable schemas, or write-heavy horizontal scale.

## Your 60-second answer

Asked to choose, I start from the access pattern and invariants. If data is relational and I need multi-row transactions or arbitrary joins, I use PostgreSQL or MySQL: tables, foreign keys, and ACID give me strong correctness with much less application code. If the records are mostly fetched by ID, the schema varies by type, or a single relational node cannot handle the write throughput or data volume, I move that part to NoSQL. A document store like MongoDB fits variable product attributes; Redis or DynamoDB fits sessions and key-value caches; Cassandra fits time-series events; Neo4j fits relationship traversal. The trade-off is that NoSQL usually gives up cross-record ACID or rich query/join ability to get horizontal scale and low-latency key access, so consistency and denormalization become application problems. I therefore choose per service, not globally.

## If they dig deeper

**When would you choose NoSQL over SQL in a system design?**

Choose NoSQL when the access pattern is key-based with no need for joins, the schema varies per item and changes often, or the write volume and data size require horizontal partitioning from day one. For example, a session store is key-value, a product catalog with category-specific attributes is document, and event ingestion is wide-column. The choice is justified by a concrete pattern, not by vague 'scale'.

**Can NoSQL databases provide ACID guarantees?**

Yes, but often scoped. MongoDB 4.0+ supports multi-document ACID transactions on replica sets, and 4.2+ extends them to sharded clusters. DynamoDB supports transactions with constraints across items and tables. Cassandra gives atomicity within a partition and tunable consistency per query. None of these gives the arbitrary cross-node joins of PostgreSQL, so transaction support does not mean relational semantics.

**How would you model recurring events in SQL for something like a calendar?**

Store events once with a recurrence rule, not every occurrence. For querying a date range, expand recurring rules into concrete occurrences within that range in application code or a materialized occurrences table, then join against the one-off events table to find overlaps. The SQL overlap check is e.start_time < :slot_end AND e.end_time > :slot_start; this is simpler and indexable than trying to encode recurrence directly in a single WHERE clause.

**When would a graph database be better than a relational database for relationship queries?**

A graph database can beat a relational store when the query is deep relationship traversal: multi-hop connections, shortest paths, friend-of-friend, fraud rings. It stores edges as first-class adjacency and traverses pointers rather than joining large tables repeatedly. If relationships are only one or two hops and mixed with reporting, PostgreSQL with recursive CTEs is often enough.

**How does CAP or PACELC influence the SQL vs NoSQL choice?**

CAP is about distributed replicas: when a partition happens, a system must choose availability (respond from each side) or consistency (refuse writes/reads on minority side). Many NoSQL systems default to availability and expose tunable consistency; Cassandra lets each query choose a consistency level, while DynamoDB has optional strongly consistent reads. PACELC adds the normal-case trade-off: with no partition, you choose latency versus strong consistency; SQL databases usually choose consistent reads on the primary or replica, while NoSQL may serve stale reads faster.

## Worked example

Consider a checkout flow that writes an orders row, two order_items rows, and decrements inventory. With PostgreSQL, this runs as BEGIN; INSERT INTO orders ...; INSERT INTO order_items ...; UPDATE inventory SET quantity = quantity - 1 WHERE sku = :sku; COMMIT;. If the inventory update fails after the order inserts, the transaction rolls back and no partial order survives; that is exactly the kind of multi-row invariant that motivates SQL. The product catalog, by contrast, is read by SKU and has different fields per category: a phone document might be {sku: 'p1', type: 'phone', battery_mah: 4000} while a book is {sku: 'b1', type: 'book', page_count: 320}. Forcing those into one relational table means nullable columns for every category or a generic EAV table; a document store stores only the fields that exist. The service split remains polyglot: relational orders, document catalog, key-value sessions.

## Common traps

- Using 'NoSQL scales, SQL does not' as a rule: relational databases can scale with read replicas and sharding, and many NoSQL stores still have single-node or single-partition limits.
- Choosing a NoSQL store because the prompt mentions scale without describing the access pattern, indexes, or consistency required, which is the real decision.
- Assuming NoSQL means no transactions: DynamoDB, MongoDB, and others have transactional APIs, but their guarantees are narrower than a relational multi-row transaction with arbitrary joins.
- Conflating 'eventual consistency' with 'no consistency': it means replicas converge after writes, and many systems let you request a strong read or higher consistency level when needed.

</details>

---

## Cards the gate rejected

Judge whether it was right. Each was thrown away.

- **beh-failure-and-learning** (typed): What pattern can signal that you are about to repeat a past mistake?
  - Gate said: not answerable: The question is too vague and open-ended without a specific framework or context referenced.

- **beh-handling-feedback** (flash): When receiving feedback as a software engineer, what sequence of steps helps you handle it effectively?
  - Gate said: wrong_format: Describing a sequence of steps requires more than one crisp sentence.

- **java-equals-and-hashcode-contract** (typed): What rules must an equals implementation itself obey?
  - Gate said: wrong_format: The honest answer is an enumeration of the five equivalence relation properties (reflexive, symmetric, transitive, consistent, non-null).

- **lld-restaurant-management-system-design** (flash): In an object-oriented restaurant management system, a Branch object is composed of which two main domain components?
  - Gate said: not answerable: The question assumes a specific system design breakdown or class diagram that is not standard across all LLD designs.

- **sd-jwt** (typed): When a server verifies a JWT, what should it check?
  - Gate said: wrong_format: The question asks for an open-ended enumeration of verification checks without bounding the scope.

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
  - Gate said: wrong_format: SQL output formatting (headers, delimiters, row representation) has no single standardized plaintext representation.

## Cards the gate caught and the rewrite fixed

These are the questions as first written. The gate objected, a rewrite pass replaced each one, and the replacement passed - so these are not in the app. They are here because the gate is on trial too: if its objections below look wrong, it is throwing away good work, and if they look right, it is earning its cost.

- **ai-data-structures-and-algorithms** (flash): Why does a binary heap retrieve the minimum or maximum in O(1), while inserting or extracting that element takes O(log n)?
  - Gate said: wrong_format: Answering both parts fully requires more than a single crisp sentence.

- **ai-metrics-offline-and-online** (flash): Which offline metrics are more informative than accuracy for imbalanced classification?
  - Gate said: wrong_format: Asking to list multiple metrics is unconstrained and fits poorly into a one-sentence flash card.

- **ai-probability-and-statistics** (flash): State the three axioms that any probability measure must satisfy.
  - Gate said: wrong_format: Stating three distinct mathematical axioms cannot fit into a single crisp sentence.

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

- **beh-failure-and-learning** (flash): What four elements make a complete failure answer?
  - Gate said: not answerable: Asking to list four specific elements refers to a specific unseen framework and does not fit a one-sentence flash format.

- **beh-growth-mindset** (flash): When answering a behavioral interview question about growth mindset, what four elements should the story include to demonstrate that the change stuck?
  - Gate said: not answerable: Asking for an exact list of four specific elements from an unseen framework cannot be answered or graded reliably in a one-sentence flash format.

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

- **lld-parking-lot-design** (flash): What are the typical parking spot types modeled in a parking garage?
  - Gate said: wrong_format: Enumerating a list of spot types does not fit a single-sentence flash card.

- **lld-ride-sharing-service-design** (flash): Why should driver availability be a separate state rather than being derived only from trip status?
  - Gate said: a human reviewer objected: Why should driver availability be a separate state rather than being derived onl

- **lld-ride-sharing-service-design** (typed): What happens in the dispatch flow when a driver does not accept an offer before the timeout expires?
  - Gate said: a human reviewer objected: What happens in the dispatch flow when a driver does not accept an offer before 

- **lld-uml-sequence-diagram** (flash): What is a UML sequence diagram, and what do the vertical and horizontal axes represent?
  - Gate said: wrong_format: Asking for definition plus both axes typically requires multiple sentences or clauses beyond a single crisp sentence.

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

- **sd-design-case-studies** (typed): Two concurrent requests with the same Idempotency-Key and merchant_id arrive at the payment API. What ensures only one provider call is made?
  - Gate said: a human reviewer objected: Two concurrent requests with the same Idempotency-Key and merchant_id arrive at 

- **sd-design-case-studies** (typed): How do you mark a payment as completed and prevent a duplicate webhook from double-applying the update?
  - Gate said: a human reviewer objected: How do you mark a payment as completed and prevent a duplicate webhook from doub

- **sd-design-case-studies** (mcq): How should you shard an idempotency store so that uniqueness checks on idempotency keys are local?
  - Gate said: a competent answer disagrees with the marked option

- **sd-jwt** (mcq): Where should a JWT be stored to prevent JavaScript on the page from reading it?
  - Gate said: a human reviewer objected: Where should a JWT be stored to prevent JavaScript on the page from reading it?

- **sd-object-storage** (flash): Name the three major managed object storage services.
  - Gate said: wrong_format: Flash cards require a single crisp sentence, not a list of named entities which is open to varying company selections.

- **sd-service-discovery** (flash): Name common service registry implementations used for service discovery.
  - Gate said: not answerable: Asking to list multiple implementations is an open-ended enumeration poorly suited for a single-sentence flash card.

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

- **sql-constraints** (typed): What is the difference between a PRIMARY KEY and a FOREIGN KEY?
  - Gate said: a human reviewer objected: What is the difference between a PRIMARY KEY and a FOREIGN KEY?

- **sql-constraints** (typed): What happens when you delete or update a parent row referenced by a foreign key, and which referential actions can you declare?
  - Gate said: wrong_format: Asking to list which referential actions can be declared requires an open-ended enumeration.

- **sql-constraints** (mcq): Which of the following is a separate column requirement often grouped with SQL constraints, rather than one of the common declarative constraints?
  - Gate said: not answerable: NOT NULL is standardly defined as a declarative constraint in SQL, making the question ambiguous and poorly defined.

- **sql-ddl-dml-dcl-tcl** (mcq): In SQL Server, after ROLLBACK TRANSACTION savepoint_name, what is the state of the outer transaction?
  - Gate said: a human reviewer objected: In SQL Server, after ROLLBACK TRANSACTION savepoint_name, what is the state of t

- **sql-ddl-dml-dcl-tcl** (flash): In SQL, which command family includes CREATE, ALTER, DROP, and TRUNCATE?
  - Gate said: a human reviewer objected: In SQL, which command family includes CREATE, ALTER, DROP, and TRUNCATE?

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
