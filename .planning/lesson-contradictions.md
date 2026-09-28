# Claims that disagree across lessons

6 found.

## ai: ai-ml-system-design, ai-metrics-offline-and-online

- **They disagree:** The ML system design lesson says offline metrics measure label prediction quality on held-out data, while the metrics lesson says offline metrics include latency and compute-cost measures, which are system-performance metrics rather than label-quality metrics.
- **Correct:** Offline metrics should be model-quality metrics such as AUC, precision, recall, and ranking metrics computed offline; latency and compute cost are system performance metrics that can be benchmarked offline but are not label-based offline metrics.
- **Rewriting:** `ai-metrics-offline-and-online`

## ai: ai-supervised-learning, ai-evaluation-metrics

- **They disagree:** The supervised learning lesson says ROC/AUC better captures performance on the minority class for imbalanced data, while the evaluation metrics lesson says ROC-AUC can remain high because of the large true-negative denominator and that precision-recall AUC is often more informative.
- **Correct:** For highly imbalanced classification, ROC-AUC can be optimistic because it summarizes ranking and is less sensitive to the positive class; precision-recall AUC focuses on the minority class and is generally the more informative metric, so ROC/AUC should not be described as reliably capturing minority-class performance.
- **Rewriting:** `ai-supervised-learning`

## behavioral: beh-choosing-and-organizing-stories, beh-story-bank

- **They disagree:** One lesson says a reusable story bank should be a set of 3–5 past projects, while the other says a story bank contains 6–10 distinct stories.
- **Correct:** A story bank typically contains 6–10 distinct stories to cover enough competencies and allow selecting a subset before an interview loop; 3–5 projects is too few if each is reduced to a single narrative.
- **Rewriting:** `beh-choosing-and-organizing-stories`

## lld: lld-abstraction, lld-interfaces

- **They disagree:** Abstraction states that Java and C# interfaces can have default method bodies since Java 8 and C# 8, while Interfaces states that implementing multiple interfaces provides multiple inheritance of type but not of implementation.
- **Correct:** Since Java 8 and C# 8, interfaces can include default method implementations, so they do provide limited implementation inheritance; they still cannot hold instance state.
- **Rewriting:** `lld-interfaces`

## system_design: sd-acid-vs-base, sd-replication

- **They disagree:** sd-acid-vs-base states that an ACID database can serve stale reads across replicas unless synchronous replication is configured, while sd-replication states that some synchronous replication modes such as PostgreSQL remote_write and MySQL semi-sync may acknowledge before applying changes, so reads from that follower can still be stale.
- **Correct:** Synchronous replication can reduce but not eliminate stale reads; only modes that wait for a follower to apply the change before acknowledging (such as PostgreSQL remote_apply or MySQL synchronous replication that waits for apply) prevent reads from that acknowledged follower from being stale. remote_write and semi-sync are durable but not queryable.
- **Rewriting:** `sd-acid-vs-base`

## system_design: sd-caching, sd-distributed-cache

- **They disagree:** sd-caching states that distributed caches shard keys with consistent hashing, but sd-distributed-cache states that Redis Cluster, a common distributed cache, divides keys into 16,384 hash slots rather than using consistent hashing.
- **Correct:** Not all distributed caches use consistent hashing: Memcached clusters typically use client-side consistent hashing, while Redis Cluster uses 16,384 hash slots assigned to primary nodes.
- **Rewriting:** `sd-caching`
