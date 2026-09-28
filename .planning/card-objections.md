# Card objections from review

What a human reviewer said was wrong with a specific card. `pipeline card-fix`
reads this file and pushes each objection through the same rewrite-and-re-gate
path the gate's own rejections use, replacing the card if the rewrite passes.

One block per card. The heading is the topic slug and the `match:` line is a
fragment of the question, which together identify one card. Both are needed: a
topic holds around ten cards and the review sample shows one, so a heading alone
picks an arbitrary card. `pipeline card-review` prints the exact two lines to
copy beneath every card in the sample.

## Round 1, 2026-09-28

An outside reviewer read the 25-card sample and approved 13, asked for 11
revisions and rejected 1. Every objection was checked against the card before
being recorded.

The first run of this file had no `match:` lines, so twelve of the thirteen
objections rewrote the wrong card: it rewrote whichever card of the topic came
first and left the one complained about publishable. The replacements all passed
the gate, so nothing bad shipped, but three objections never reached their
target. Those three are below. The rest were either applied to the right card by
luck, or the offending card was separately caught and rewritten by the re-gate.

## beh-dealing-with-ambiguity

match: At the senior level

WRONG AS WRITTEN. It presents "senior means leading multiple people, staff means
multiple teams" as a universal scope ladder. Levelling definitions differ at
every company and no interviewer grades against this, so a candidate with a
sound answer could be marked wrong for using their own company's definition.
Rewrite so the answer is about the behaviour an interviewer is looking for under
ambiguity - naming the unknowns, stating assumptions, driving alignment - not
about a title-to-scope mapping.

## cs-locking-mechanisms

match: Which storage engine uses table-level locking

The options mix MySQL storage engines with entire database systems - InnoDB and
MyISAM beside PostgreSQL and SQL Server - so only two options are even
candidates and the card is trivially easy. Every wrong option should be a
mistake someone actually makes: use four MySQL storage engines, or ask the
question about database systems and choose four of those.

## sd-jwt

match: When a server verifies a JWT

Asks for an open-ended list of verification checks, so a good answer can miss the
key points by naming different real checks. It is a question worth keeping -
"what does a server check on a JWT" is asked constantly - so bound it: make it
multiple choice over four checks where the wrong options are real errors
(trusting the `alg` header, checking the signature but not `exp`, validating
`iss` but not the audience), or ask about one check and why skipping it is
exploitable.
