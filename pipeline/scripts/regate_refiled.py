"""Re-gate only the cards `refile` moved, to confirm they fit where they landed.

`refile` prints "run card-regate to confirm they fit now", and `card-regate` works
per topic: the 523 moved cards are spread over 159 topics, so taking it at its word
means re-judging some 4,000 cards to check 523, and re-rolling verdicts on all of
them in the process.

This asks the same question of the moved cards alone. It is the answerability gate
only - no blind gate, no rewrite pass - because the question is narrow: does the
card ask what its new archetype says it asks? A card that fails goes back to
rejected, naming the archetype it failed in, so the move is undone in effect and
visible in the record.

Run from `pipeline/`. Dry run unless called with --apply.
"""

import os
import sys
from collections import defaultdict

sys.path.insert(0, "src")

import duckdb

from pipeline.cards import gate, regate
from pipeline.llm import LLM, BudgetExceeded, LLMError

APPLY = "--apply" in sys.argv
TIER = "smart" if "--smart" in sys.argv else "fast"

con = duckdb.connect(os.path.abspath("../.data/staging.duckdb"), read_only=not APPLY)

moved = con.execute("""
    select topic_slug, id from cards
     where quality like '%refiled_from%' and kept = true and status = 'draft'
       and archetype is not null
     order by topic_slug, id
""").fetchall()
by_topic: dict[str, set[str]] = defaultdict(set)
for slug, card_id in moved:
    by_topic[slug].add(card_id)

print(f"{len(moved)} refiled cards across {len(by_topic)} topics, tier={TIER}, apply={APPLY}")

topics = {t["slug"]: t for t in regate.topics_with_cards(con, list(by_topic))}
missing = set(by_topic) - set(topics)
assert not missing, f"topics not found: {sorted(missing)[:5]}"

llm = LLM(con)
checked = kept = failed = 0
failures: list[tuple[str, str, str]] = []

for slug, wanted in by_topic.items():
    # `cards_of` builds the Draft objects the gate expects, with the answer columns
    # `wellformed` needs. Filter to the moved ones: their neighbours were judged in
    # the full pass and asking again would only re-roll verdicts already paid for.
    cards = [c for c in regate.cards_of(con, slug) if c.id in wanted]
    if not cards:
        continue
    try:
        result = gate.review(llm, topics[slug], cards, tier=TIER)
    except BudgetExceeded as e:
        print(f"  stopping: {e}")
        break
    except (LLMError, Exception) as e:
        print(f"  {slug}: FAILED {type(e).__name__}: {e}")
        continue
    rejected = gate.judge(cards, result)
    checked += len(cards)
    kept += len(cards) - len(rejected)
    failed += len(rejected)
    for card, why in rejected:
        failures.append((slug, card.archetype, why))
    if rejected and APPLY:
        confidence = gate.confidence_by_card(cards, result)
        regate.apply(con, cards, rejected, confidence)
        con.commit()
    if rejected:
        print(f"  {slug}: {len(rejected)} of {len(cards)} did not fit")

print(f"\nchecked {checked}, fit {kept}, did not fit {failed}")
if failures:
    print("\nreasons (first 12):")
    for slug, archetype, why in failures[:12]:
        print(f"  [{archetype}] {slug}: {why[:95]}")
if not APPLY:
    print("\ndry run; pass --apply to write the rejections")
