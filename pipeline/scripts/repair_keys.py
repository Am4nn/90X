"""Repair the keys of cards the audit retired, then check the repair with two model families.

    uv run python scripts/repair_keys.py                # derive, validate, audit; writes nothing to cards
    uv run python scripts/repair_keys.py --apply        # also write the cards both models approve
    uv run python scripts/repair_keys.py --from FILE    # write a saved result without calling a model

For each card the audit retired for a key that contradicts its explanation:
  1. a model reads the explanation and says what key it describes (`key_repair.derive`);
  2. the code turns that into the stored columns, and `wellformed` must accept them;
  3. the REPAIRED card is audited by two models of different families, and it is written only
     if both say the key now agrees with the explanation.

Step 3 is not redundant. A repaired key agrees with the explanation by construction, so the
audit proves less than it did on the original card - but it still catches a derivation that
misread the numbering, and it is the check that the repaired card reads the way the author
meant. What it cannot catch is an explanation that is itself wrong; nothing here can.

Run on OpenCode Go (see RUNBOOK.md): FIRST is the `fast` tier, SECOND the `smart` tier, and
the two should be different families.
"""

import copy
import json
import os
import sys
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, "src")

import duckdb

from pipeline.cards import key_audit, key_repair, regate, wellformed
from pipeline.llm import LLM, BudgetExceeded, LLMError

ARGS = sys.argv[1:]
APPLY = "--apply" in ARGS
LIMIT = int(ARGS[ARGS.index("--limit") + 1]) if "--limit" in ARGS else 0
# Deriving the key is the step where a misreading does damage, so it defaults to the strong
# tier; the two audits that follow use fast then smart.
DERIVE = ARGS[ARGS.index("--derive-tier") + 1] if "--derive-tier" in ARGS else "smart"
WORKERS = 8
OUT = os.path.abspath("../.data/review/key-repair.json")


def with_key(card, updates: dict):
    """A copy of the card carrying the repaired key, so it can be validated and audited
    exactly as it would be stored, without touching the row."""
    fixed = copy.copy(card)
    for column, value in updates.items():
        setattr(fixed, column, value)
    return fixed


def derive_all(llm, cards: list, tier: str) -> dict[str, dict]:
    """card id -> the stored columns its explanation implies. Unsettled or invalid cards are absent."""
    out: dict[str, dict] = {}
    skipped = defaultdict(int)

    def one(card):
        return card, key_repair.new_key(card, key_repair.derive(llm, card, tier=tier))

    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futures = [pool.submit(one, c) for c in cards]
        done = 0
        for fut in as_completed(futures):
            try:
                card, updates = fut.result()
            except BudgetExceeded as e:
                print(f"  stopping: {e}", flush=True)
                break
            except (LLMError, Exception) as e:  # noqa: BLE001 - one card's failure costs that card
                print(f"  FAILED {type(e).__name__}: {str(e)[:100]}", flush=True)
                continue
            done += 1
            if updates is None:
                skipped[card.format] += 1
                continue
            problems = wellformed.problems(with_key(card, updates))
            if problems:
                skipped[card.format] += 1
                continue
            out[card.id] = updates
            if done % 25 == 0:
                print(f"  derived {done}/{len(cards)}", flush=True)
    print(f"derived a valid key for {len(out)} of {len(cards)}; not settled or invalid: {dict(skipped)}")
    return out


def audit_all(llm, repaired: list, topics: dict, tier: str) -> dict[str, str]:
    """card id -> verdict, auditing the REPAIRED copies by topic in chunks."""
    groups: dict[str, list] = defaultdict(list)
    for c in repaired:
        groups[c.topic_slug].append(c)
    work = [(slug, cards[i:i + 10]) for slug, cards in groups.items() for i in range(0, len(cards), 10)]
    verdicts: dict[str, str] = {}

    def job(slug, chunk):
        return chunk, key_audit.audit(llm, topics[slug], chunk, tier=tier)

    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        for fut in as_completed([pool.submit(job, s, ch) for s, ch in work]):
            try:
                chunk, result = fut.result()
            except BudgetExceeded as e:
                print(f"  stopping: {e}", flush=True)
                break
            except (LLMError, Exception) as e:  # noqa: BLE001
                print(f"  FAILED {type(e).__name__}: {str(e)[:100]}", flush=True)
                continue
            said = {v.index: v.verdict for v in result.verdicts}
            for i, c in enumerate(chunk):
                verdicts[c.id] = said.get(i, "missing")
    return verdicts


def write(con, accepted: dict[str, dict]) -> None:
    columns = {"picked": json.dumps, "pairs": json.dumps, "constraints": json.dumps, "value": float}
    for cid, updates in accepted.items():
        sets, params = [], []
        for column, value in updates.items():
            sets.append(f"{column} = ?")
            params.append(columns[column](value))
        con.execute(
            f"""update cards set {", ".join(sets)}, status = 'draft', kept = true, reject_reason = null,
                       quality = json_merge_patch(coalesce(quality, '{{}}'),
                                                 json_object('key_repaired',
                                                             'key re-derived from the explanation; two model families agree it now matches'))
                 where id = ? and status = 'rejected' and reject_reason like 'answer key contradicts%'""",
            [*params, cid],
        )
    con.commit()


def main() -> None:
    if "--from" in ARGS:
        saved = json.load(open(ARGS[ARGS.index("--from") + 1], encoding="utf-8"))
        accepted = saved["accepted"]
        if not accepted:
            print("nothing was accepted, so nothing to write")
            return
        con = duckdb.connect(os.path.abspath("../.data/staging.duckdb"))
        write(con, accepted)
        print(f"wrote {len(accepted)} repaired cards back to draft")
        return

    # Read-write even for a dry run: the client records each call's cost in this database.
    con = duckdb.connect(os.path.abspath("../.data/staging.duckdb"))
    topics = {t["slug"]: t for t in regate.topics_with_cards(con)}
    retired = {r[0] for r in con.execute(
        "select id from cards where status = 'rejected' and reject_reason like 'answer key contradicts%'").fetchall()}
    cards = [c for slug in topics for c in regate.cards_of(con, slug)
             if c.id in retired and key_repair.can_repair(c.format)]
    if LIMIT:
        cards = cards[:LIMIT]
    by_format = defaultdict(int)
    for c in cards:
        by_format[c.format] += 1
    print(f"{len(cards)} retired cards to repair {dict(by_format)}")

    llm = LLM(con)
    derived = derive_all(llm, cards, DERIVE)
    repaired = [with_key(c, derived[c.id]) for c in cards if c.id in derived]

    print(f"auditing {len(repaired)} repaired cards with two model families")
    first = audit_all(llm, repaired, topics, "fast")
    second = audit_all(llm, repaired, topics, "smart")
    accepted = {cid: derived[cid] for cid in derived if first.get(cid) == "agrees" and second.get(cid) == "agrees"}

    old = {c.id: c for c in cards}
    changed = sum(1 for cid, u in accepted.items()
                  if any(getattr(old[cid], col) != val for col, val in u.items()))
    fmt = {c.id: c.format for c in cards}
    tally = defaultdict(lambda: [0, 0])
    for cid in derived:
        tally[fmt[cid]][0] += 1
        tally[fmt[cid]][1] += cid in accepted
    print(f"\nrepaired and approved by both models: {len(accepted)} of {len(cards)}  (key actually changed in {changed})")
    print("by primitive: approved / derived")
    for f, (n, ok) in sorted(tally.items(), key=lambda kv: -kv[1][0]):
        print(f"  {f:13} {ok:>3} / {n}")
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump({"accepted": accepted, "first": first, "second": second}, fh, indent=1, ensure_ascii=False)
    print(f"saved to {OUT}")

    if APPLY and accepted:
        write(con, accepted)
        print(f"wrote {len(accepted)} repaired cards back to draft")
    elif accepted:
        print("nothing written; pass --apply, or --from the saved file")


if __name__ == "__main__":
    main()
