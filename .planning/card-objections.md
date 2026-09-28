# Card objections from review

What a human reviewer said was wrong with a specific card, in their words plus
ours. `pipeline card-fix` reads this file, pushes each objection through the
same rewrite-and-re-gate path the gate's own rejections use, and replaces the
card if the rewrite passes.

One block per card. The heading is the topic slug, which identifies the card
because the review sample carries at most one card per topic. Everything under
it is the objection handed to the rewrite.

Round 1, 2026-09-28. An outside reviewer read the 25-card sample and approved
13, asked for 11 revisions and rejected 1. Each objection was checked against
the card before being recorded here, and the ones that turned out to be a
factual error in the card rather than a matter of taste are marked.

They flagged twelve cards in all - eleven to revise and one to reject - and
eleven are recorded below. The twelfth was the reviewer's #18,
which they labelled "Knowledge distillation" and asked to have scoped to "the
same model". The card is `ai-prediction-service` and already asks "which
technique does NOT reduce inference compute **for an existing model**", which
is that scoping. Nothing to fix, so nothing is recorded for it - a rewrite
prompted by an objection the card already answers is how a good card gets
made worse.

## beh-leadership

The reference answer treats "concrete artifacts such as internal design docs,
blog posts, talks or open-source contributions" as the measure of thought
leadership. That is one reasonable view, not a fact an interviewer would mark
against. Ask about something checkable instead: what distinguishes an answer
that shows influence without authority from one that only lists actions.

## beh-dealing-with-ambiguity

WRONG AS WRITTEN. It presents "senior means aligning multiple people, staff
means aligning multiple teams" as a universal scope ladder. Levelling
definitions differ at every company and no interviewer grades against this.
Rewrite so the answer is about the behaviour the interviewer is looking for
under ambiguity, not about a title-to-scope mapping.

## lld-ride-sharing-service-design

The question is too broad to have one gradable answer, so any competent
response could miss the key points by writing about something else equally
valid. Narrow it to one decision in the design with a defensible answer -
matching riders to drivers, or how location updates are stored.

## sql-ddl-dml-dcl-tcl

Privileges differ by engine: who may run DDL, and whether DDL is
transactional, is not the same in PostgreSQL, MySQL and Oracle. Either name
the engine in the question or ask for the general principle - least privilege,
and which statement classes change data versus structure - rather than
presenting one engine's rules as generic SQL.

## sql-constraints

WRONG AS WRITTEN, and the reviewer is right to reject it outright. The question
asks which item is "a separate column requirement rather than one of the common
declarative constraints" and marks NOT NULL as the answer. NOT NULL is a SQL
constraint: it is a column constraint in the SQL standard and in every major
engine. Replace the card completely with one that tests something true about
constraints - for example what CHECK can and cannot reference, or what happens
to a FOREIGN KEY on delete.

## sd-design-a-notification-system

"How would you handle failure in a notification system?" is too broad for a
card answered in one to three sentences, and the key points cannot fairly grade
it because a good answer might cover retries, idempotency, dead-letter queues
or fan-out isolation and still miss them. Give it one concrete failure: a push
provider returning 503 for ten minutes, say, and ask what the system does.

## sd-consistent-hashing

WRONG TO TEST. The marked answer rests on how DynamoDB implements virtual
nodes internally, which is vendor-specific, undocumented in detail, and liable
to change. Test the concept: why virtual nodes are added at all, or what
happens to keys when one node leaves the ring.

## sd-design-case-studies

The marked answer is "use a cache", which is one possible design rather than
the only correct one - a reader who answers with an approximate counter or a
probabilistic structure is not wrong. Ask about a specific mechanism instead:
how a sliding window of active viewers is maintained, and what it costs.

## java-hashmap-internals

WRONG AS WRITTEN. It marks "O(1) average and O(log n) worst case" as correct
for HashMap.get in Java 8. A bucket only becomes a tree at TREEIFY_THRESHOLD
of 8 collisions *and* a table capacity of at least MIN_TREEIFY_CAPACITY, 64;
below that the map resizes instead, so a small table's worst case really is
O(n). Ask about a treeified bucket explicitly, or about the two conditions
treeifying requires.

## sql-char-vs-varchar

The answer explains what VARCHAR(n) stores and says it "does not pad shorter
values", but the question asks what it stores *compared with* CHAR(n) and never
says that CHAR pads to n. Complete the comparison so the contrast is gradable.

## cs-locking-mechanisms

The options mix MySQL storage engines with entire database systems - InnoDB and
MyISAM beside PostgreSQL and SQL Server - so only two options are even
candidates and the card is trivially easy. Every wrong option should be a real
mistake: use four MySQL storage engines, or ask the question about database
systems and choose four of those.

## java-equals-and-hashcode-contract

The reviewer named this card as one the gate was wrong to throw away: the
equals() contract is a real interview question. It was rejected as a typed card
because the honest answer enumerates five properties - reflexive, symmetric,
transitive, consistent, and non-null handling - and a candidate cannot guess how
many are wanted. Make it multiple choice, with four options where the wrong ones
are mistakes people actually make: leaving out symmetry, requiring equal
hashCodes as part of the equals contract rather than as a consequence, or
allowing equals(null) to throw.

## sd-jwt

Rejected as a typed card for asking an open-ended list of verification checks,
and it is a question worth keeping - "what does a server check on a JWT" is
asked constantly. Bound it: make it multiple choice over four checks where the
wrong options are real errors (trusting the `alg` header, checking the signature
but not `exp`, validating `iss` but not the audience), or ask about one check
and why skipping it is exploitable.
