"""Audit the corpus for answer keys that contradict their own explanation.

    uv run python scripts/key_audit.py --pilot 120      # a stratified sample, to measure the rate
    uv run python scripts/key_audit.py                  # every kept card
    uv run python scripts/key_audit.py --formats grid_toggle,assemble   # only these primitives
    uv run python scripts/key_audit.py --apply          # reject what both passes call a contradiction

Two passes, on purpose. The first runs on the cheap tier and is allowed to be noisy; the
second re-reads only what the first flagged, on the smart tier, and a card is rejected
only when both say "contradicts". A single cheap model rejecting live cards on its own
say-so is how good cards get thrown away.

Results are written to `.data/review/key-audit*.json` after every chunk, so a crash or a
spend cap loses nothing already paid for.

Run from `pipeline/`. Nothing is written to the cards without --apply.
"""

import json
import os
import random
import sys
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, "src")

import duckdb

from pipeline.cards import key_audit, regate
from pipeline.llm import LLM, BudgetExceeded, LLMError

ARGS = sys.argv[1:]
APPLY = "--apply" in ARGS
PILOT = int(ARGS[ARGS.index("--pilot") + 1]) if "--pilot" in ARGS else 0
FIRST = ARGS[ARGS.index("--first") + 1] if "--first" in ARGS else "fast"
SECOND = ARGS[ARGS.index("--second") + 1] if "--second" in ARGS else "smart"
ONLY = ARGS[ARGS.index("--formats") + 1].split(",") if "--formats" in ARGS else []
CHUNK = 10
WORKERS = 8
OUT = os.path.abspath("../.data/review/key-audit" + ("-pilot" if PILOT else "") + ("-" + "-".join(ONLY) if ONLY else "") + ".json")


def candidates(con) -> list[str]:
    """Every kept card with a key to audit: the corpus that is, or is about to be, live."""
    rows = con.execute("""
        select id, format from cards
         where source = 'lesson' and kept = true and status = 'draft' and archetype is not null
    """).fetchall()
    return [r[0] for r in rows if not ONLY or r[1] in ONLY]


def stratified(con, ids: list[str], n: int) -> list[str]:
    """About n cards, spread over the primitives so no shape is left unmeasured."""
    fmt = dict(con.execute("select id, format from cards").fetchall())
    by = defaultdict(list)
    for i in ids:
        by[fmt[i]].append(i)
    rng = random.Random(7)
    keyed = [f for f in by if f not in ("self_rate", "compose")]
    if not keyed:  # --formats named only primitives with no key, or nothing matched
        return []
    per = max(6, n // len(keyed))
    picked: list[str] = []
    for f in keyed:
        pool = by[f][:]
        rng.shuffle(pool)
        picked += pool[:per]
    return picked


# The one shape every checkpoint and the final file share. Each chunk used to replace the
# file with only the current pass, so a second-pass checkpoint overwrote the first pass, and
# a run that died between the two left a file `--from` could not read.
STATE: dict = {"first": {}, "second": {}, "confirmed": []}


def confirmed_from(state: dict) -> list[str]:
    """Cards both passes call a contradiction. Derived, so it is right at every checkpoint."""
    first, second = state.get("first", {}), state.get("second", {})
    return sorted(cid for cid, r in second.items()
                  if r["verdict"] == "contradicts" and first.get(cid, {}).get("verdict") == "contradicts")


def save(state: dict) -> None:
    state["confirmed"] = confirmed_from(state)
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(state, fh, indent=1, ensure_ascii=False)


def run(llm, groups: dict[str, list], topics: dict[str, dict], tier: str, label: str) -> dict[str, dict]:
    """Audit each topic's cards in chunks. Returns card id -> {verdict, reason}."""
    work = [(slug, cards[i:i + CHUNK]) for slug, cards in groups.items() for i in range(0, len(cards), CHUNK)]
    results: dict[str, dict] = STATE[label]
    done = 0

    def job(slug, chunk):
        return slug, chunk, key_audit.audit(llm, topics[slug], chunk, tier=tier)

    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futures = [pool.submit(job, slug, chunk) for slug, chunk in work]
        for fut in as_completed(futures):
            try:
                slug, chunk, result = fut.result()
            except BudgetExceeded as e:
                print(f"  stopping: {e}", flush=True)
                break
            except (LLMError, Exception) as e:  # noqa: BLE001 - one chunk's failure costs that chunk
                print(f"  FAILED {type(e).__name__}: {str(e)[:100]}", flush=True)
                continue
            said = {v.index: v for v in result.verdicts}
            for i, c in enumerate(chunk):
                v = said.get(i)
                results[c.id] = {"verdict": v.verdict if v else "missing", "reason": (v.reason if v else ""), "topic": slug}
            done += 1
            save(STATE)
            if done % 20 == 0:
                print(f"  [{label}] {done}/{len(work)} chunks", flush=True)
    return results


def apply_saved(path: str) -> None:
    """Reject what a previous run confirmed, without paying for the model calls again."""
    saved = json.load(open(path, encoding="utf-8"))
    first, second = saved.get("first", {}), saved.get("second", {})
    confirmed = saved.get("confirmed") or confirmed_from(saved)
    if not confirmed:
        print("nothing was confirmed, so nothing to reject")
        return
    con = duckdb.connect(os.path.abspath("../.data/staging.duckdb"))
    for cid in confirmed:
        why = (second[cid]["reason"] or first[cid]["reason"])[:200]
        con.execute(
            """update cards set status = 'rejected', kept = false, reject_reason = ?
                where id = ? and status = 'draft'""",
            [f"answer key contradicts the explanation: {why}", cid],
        )
    con.commit()
    left = con.execute(
        "select count(*) from cards where id in (" + ",".join("?" * len(confirmed)) + ") and status = 'draft'", confirmed
    ).fetchone()[0]
    print(f"rejected {len(confirmed)} cards in staging; {left} still draft (want 0)")


def main() -> None:
    if "--from" in ARGS:
        return apply_saved(ARGS[ARGS.index("--from") + 1])
    # Read-write even for a dry run: the LLM client records every call's cost in this
    # database, so a read-only connection makes each call fail AFTER the API has
    # answered and been paid for. Only the rejection below is gated on --apply.
    con = duckdb.connect(os.path.abspath("../.data/staging.duckdb"))
    ids = candidates(con)
    if PILOT:
        ids = stratified(con, ids, PILOT)
    wanted = set(ids)

    topics = {t["slug"]: t for t in regate.topics_with_cards(con)}
    groups: dict[str, list] = {}
    skipped = 0
    for slug in topics:
        cards = [c for c in regate.cards_of(con, slug) if c.id in wanted]
        keep = [c for c in cards if key_audit.has_key(c)]
        skipped += len(cards) - len(keep)
        if keep:
            groups[slug] = keep
    total = sum(len(v) for v in groups.values())
    print(f"{total} cards across {len(groups)} topics ({skipped} have no stored key to audit); first pass: {FIRST}")

    llm = LLM(con)
    first = run(llm, groups, topics, FIRST, "first")
    flagged = {cid for cid, r in first.items() if r["verdict"] == "contradicts"}
    unclear = sum(1 for r in first.values() if r["verdict"] in ("unclear", "missing"))
    print(f"\nfirst pass: {len(first)} judged, {len(flagged)} contradict, {unclear} unclear")

    by_id = {c.id: c for cards in groups.values() for c in cards}
    again: dict[str, list] = defaultdict(list)
    for cid in flagged:
        again[first[cid]["topic"]].append(by_id[cid])
    second = run(llm, again, topics, SECOND, "second") if again else {}
    save(STATE)
    confirmed = set(STATE["confirmed"])  # both passes, not the second alone
    print(f"second pass ({SECOND}): {len(second)} re-read, {len(confirmed)} confirmed")

    fmt = dict(con.execute("select id, format from cards").fetchall())
    by_format = defaultdict(lambda: [0, 0])
    for cid in first:
        by_format[fmt[cid]][0] += 1
        by_format[fmt[cid]][1] += cid in confirmed
    print("\nconfirmed contradictions by primitive (confirmed / audited):")
    for f, (n, bad) in sorted(by_format.items(), key=lambda kv: -kv[1][1]):
        print(f"  {f:13} {bad:>3} / {n}")

    if not APPLY:
        print(f"\nsaved to {OUT}; nothing changed. Pass --apply to reject the {len(confirmed)} confirmed.")
        return
    for cid in sorted(confirmed):
        why = (second[cid]["reason"] or first[cid]["reason"])[:200]
        con.execute(
            """update cards set status = 'rejected', kept = false, reject_reason = ?
                where id = ? and status = 'draft'""",
            [f"answer key contradicts the explanation: {why}", cid],
        )
    con.commit()
    print(f"\nrejected {len(confirmed)} cards in staging. Production is unchanged until they are retired there.")


if __name__ == "__main__":
    main()
