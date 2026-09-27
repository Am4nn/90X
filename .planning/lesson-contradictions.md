# Claims that disagree across lessons

6 found.

## behavioral: beh-story-bank, beh-choosing-and-organizing-stories

- **They disagree:** One lesson says a story bank should contain 8–12 distinct professional stories, while the other says to collect only 3–5 high-impact experiences as a reusable set.
- **Correct:** A behavioral story bank should contain enough distinct stories to cover the common competencies, typically 8–12; 3–5 is too few to reliably cover categories like failure, conflict, leadership, and ownership.
- **Rewriting:** `beh-choosing-and-organizing-stories`

## cs: cs-tcp-vs-udp, cs-tcp-3-way-handshake

- **They disagree:** cs-tcp-vs-udp says TCP Fast Open allows data in the initial SYN, while cs-tcp-3-way-handshake says an ACK after a SYN is always the received ISN plus one.
- **Correct:** A SYN without data consumes exactly one sequence number, so its acknowledgment is ISN+1; if the SYN carries data under TCP Fast Open, the data also consumes sequence numbers and the ACK must be ISN+1 plus the data length.
- **Rewriting:** `cs-tcp-3-way-handshake`

## cs: cs-tcp-3-way-handshake, cs-tcp-vs-udp

- **They disagree:** cs-tcp-vs-udp says TCP Fast Open allows application data in the initial SYN, while cs-tcp-3-way-handshake says an ACK after a SYN is always the received ISN plus one; if the SYN carries data, the ACK must also acknowledge that data.
- **Correct:** A SYN consumes one sequence number, so a data-free SYN is acknowledged as ISN+1; when TCP Fast Open puts data in the initial SYN, the SYN-ACK acknowledges the data and has acknowledgment number ISN+1+data length.
- **Rewriting:** `cs-tcp-3-way-handshake`

## java: java-hashset-vs-treeset, java-comparable-vs-comparator

- **They disagree:** One lesson says TreeSet/TreeMap use a supplied Comparator, while the other says TreeSet keeps elements in natural order or a supplied Comparator.
- **Correct:** TreeSet and TreeMap use natural ordering (Comparable) when no Comparator is supplied, and use the supplied Comparator when one is provided.
- **Rewriting:** `java-comparable-vs-comparator`

## java: java-comparable-vs-comparator, java-hashset-vs-treeset

- **They disagree:** java-comparable-vs-comparator states that ordered collections such as TreeSet and TreeMap use a supplied Comparator, while java-hashset-vs-treeset states that TreeSet keeps elements in ascending natural order or a supplied Comparator.
- **Correct:** TreeSet and TreeMap use natural ordering via Comparable when constructed without a Comparator, and use a supplied Comparator only when one is provided at construction.
- **Rewriting:** `java-comparable-vs-comparator`

## system_design: sd-distributed-transactions, sd-sagas

- **They disagree:** The distributed transactions lesson says saga-based approaches are distributed transactions that make all changes either become durable or all roll back, while the sagas lesson says each local transaction commits independently and is reversed by compensating transactions, not distributed rollback.
- **Correct:** A saga does not provide atomic all-or-nothing rollback; its local transactions commit, and failures are handled by later compensating actions, so intermediate states remain visible. Atomic all-or-nothing durability/rollback applies to protocols such as two-phase commit.
- **Rewriting:** `sd-distributed-transactions`
