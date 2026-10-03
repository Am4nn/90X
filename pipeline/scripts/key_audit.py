"""Audit the corpus for answer keys that contradict their own explanation.

    uv run python scripts/key_audit.py --pilot 120      # a stratified sample, to measure the rate
    uv run python scripts/key_audit.py                  # every kept card
    uv run python scripts/key_audit.py --formats grid_toggle,assemble   # only these primitives
    uv run python scripts/key_audit.py --apply          # reject what both passes call a contradiction
    uv run python scripts/key_audit.py --recheck 300    # how much did the cheap first pass miss?

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
APPLIED = os.path.abspath("../.data/review/key-audit-retest-applied.json")
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


def recheck(n: int) -> None:
    """Re-read a random sample of the first pass's `agrees` with the strong model.

    The first pass is cheap and only what it flags is re-read, so a card it called
    `agrees` was never double-checked and its miss rate was unknown. This measures it:
    the share of that sample the strong model calls a contradiction is the cheap pass's
    miss rate, and it says whether the clean corpus is as clean as it looks.

    Writes nothing to the cards. Hits are saved for reading and for `--from`.
    """
    import glob

    con = duckdb.connect(os.path.abspath("../.data/staging.duckdb"))
    pool: list[str] = []
    for path in glob.glob(os.path.abspath("../.data/review/key-audit-*.json")):
        if "pilot" in path or "recheck" in path:
            continue
        pool += [cid for cid, r in json.load(open(path, encoding="utf-8")).get("first", {}).items() if r["verdict"] == "agrees"]
    live = {r[0] for r in con.execute(
        "select id from cards where kept = true and status = 'draft' and archetype is not null").fetchall()}
    pool = sorted(set(pool) & live)
    sample = set(random.Random(11).sample(pool, min(n, len(pool))))
    topics = {t["slug"]: t for t in regate.topics_with_cards(con)}
    groups: dict[str, list] = {}
    for slug in topics:
        keep = [c for c in regate.cards_of(con, slug) if c.id in sample and key_audit.has_key(c)]
        if keep:
            groups[slug] = keep
    print(f"{len(pool)} cards the first pass called clean and are still live; re-reading {sum(len(v) for v in groups.values())} with {SECOND}")
    out = run(LLM(con), groups, topics, SECOND, "second")
    hits = sorted(cid for cid, r in out.items() if r["verdict"] == "contradicts")
    fmt = dict(con.execute("select id, format from cards").fetchall())
    print(f"\nstrong model on the cheap pass's clean cards: {len(hits)} contradict of {len(out)} re-read "
          f"({100 * len(hits) / max(len(out), 1):.1f}%)")
    by = defaultdict(lambda: [0, 0])
    for cid in out:
        by[fmt[cid]][0] += 1
        by[fmt[cid]][1] += cid in hits
    for f, (total, bad) in sorted(by.items(), key=lambda kv: -kv[1][1]):
        print(f"  {f:13} {bad:>3} / {total}")
    save_path = os.path.abspath("../.data/review/key-audit-recheck.json")
    with open(save_path, "w", encoding="utf-8") as fh:
        json.dump({"first": {c: {**out[c], "verdict": "contradicts"} for c in hits}, "second": {c: out[c] for c in hits},
                   "confirmed": hits, "all": out}, fh, indent=1, ensure_ascii=False)
    print(f"saved to {save_path}; nothing changed. Apply with --from.")


def retest() -> None:
    """Re-judge every card the audit has flagged, with two independent models.

    The first audit's two passes were a cheap model and a stronger one from the same family,
    reading a key worded the same way. Re-reading nine of the flagged cards by hand showed
    a share of them were misreadings the wording caused - a tap-the-bug card's key *is* the
    bug line, a rebuilt line was spaced differently from its explanation, a numeric key was
    the exponent the explanation wrote as O(n^2) - and both passes made the same mistake,
    so agreement between them proved less than it looked.

    So: every flagged card goes through FIRST and then SECOND, each over every card (not only
    what the first flagged), and the two should be different model families. Then
      - both say agrees       -> restore: the original flag was a misreading
      - both say contradicts  -> keep_out: a genuine disagreement, confirmed independently
      - anything else         -> uncertain: left where it is, for a person
    Writes nothing to the cards.
    """
    import glob

    global OUT
    OUT = os.path.abspath("../.data/review/key-audit-retest.json")
    con = duckdb.connect(os.path.abspath("../.data/staging.duckdb"))
    ids: set[str] = set()
    for path in glob.glob(os.path.abspath("../.data/review/key-audit-*.json")):
        if "pilot" in path or "retest" in path:
            continue
        ids |= set(json.load(open(path, encoding="utf-8")).get("confirmed", []))
    topics = {t["slug"]: t for t in regate.topics_with_cards(con)}
    groups: dict[str, list] = {}
    for slug in topics:
        keep = [c for c in regate.cards_of(con, slug) if c.id in ids and key_audit.has_key(c)]
        if keep:
            groups[slug] = keep
    total = sum(len(v) for v in groups.values())
    print(f"{total} flagged cards to re-judge; first={FIRST} second={SECOND}")
    llm = LLM(con)
    first = run(llm, groups, topics, FIRST, "first")
    second = run(llm, groups, topics, SECOND, "second")

    fmt = dict(con.execute("select id, format from cards").fetchall())
    result: dict[str, list[str]] = {"restore": [], "keep_out": [], "uncertain": []}
    for cid in sorted(set(first) | set(second)):
        a, b = first.get(cid, {}).get("verdict"), second.get(cid, {}).get("verdict")
        if a == "agrees" and b == "agrees":
            result["restore"].append(cid)
        elif a == "contradicts" and b == "contradicts":
            result["keep_out"].append(cid)
        else:
            result["uncertain"].append(cid)
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump({**result, "first": first, "second": second}, fh, indent=1, ensure_ascii=False)
    print(f"\nrestore (both agree): {len(result['restore'])}   keep out (both contradict): {len(result['keep_out'])}   "
          f"uncertain: {len(result['uncertain'])}")
    by = defaultdict(lambda: [0, 0, 0])
    for i, name in enumerate(("restore", "keep_out", "uncertain")):
        for cid in result[name]:
            by[fmt[cid]][i] += 1
    print("\nby primitive:   restore / keep out / uncertain")
    for f, (r, k, u) in sorted(by.items(), key=lambda kv: -sum(kv[1])):
        print(f"  {f:13} {r:>4} / {k:>4} / {u:>4}")
    print(f"\nsaved to {OUT}; nothing changed.")


def apply_retest(path: str) -> None:
    """Act on a retest: put back what both models cleared, take out what both confirmed.

    Staging only. Production follows from the lists this prints: `publish` stamps the restored
    cards (it leaves `status` alone), then they are taken live by id.
    """
    saved = json.load(open(path, encoding="utf-8"))
    restore, keep_out = saved.get("restore", []), saved.get("keep_out", [])
    if not restore and not keep_out:
        print("nothing to restore and nothing to take out")
        return
    con = duckdb.connect(os.path.abspath("../.data/staging.duckdb"))
    restored, rejected = [], []
    for cid in restore:
        # Only a card the audit itself rejected. A card rejected for any other reason is
        # not this script's to bring back.
        row = con.execute(
            "select 1 from cards where id = ? and status = 'rejected' and reject_reason like 'answer key contradicts%'",
            [cid],
        ).fetchone()
        if row:
            con.execute(
                """update cards set status = 'draft', kept = true, reject_reason = null,
                          quality = json_merge_patch(coalesce(quality, '{}'),
                                                    json_object('key_audit_restored',
                                                                'retest: two independent models agree the key matches'))
                    where id = ?""",
                [cid],
            )
            restored.append(cid)
    for cid in keep_out:
        why = (saved["second"].get(cid, {}).get("reason") or saved["first"].get(cid, {}).get("reason") or "")[:200]
        row = con.execute("select 1 from cards where id = ? and status = 'draft' and kept = true", [cid]).fetchone()
        if row:  # a live card the strong recheck flagged and a second family confirmed
            con.execute(
                "update cards set status = 'rejected', kept = false, reject_reason = ? where id = ?",
                [f"answer key contradicts the explanation: {why}", cid],
            )
            rejected.append(cid)
    con.commit()
    out = APPLIED
    with open(out, "w", encoding="utf-8") as fh:
        json.dump({"restored": restored, "newly_rejected": rejected}, fh, indent=1)
    print(f"restored {len(restored)} to draft; newly rejected {len(rejected)} that were live")
    print(f"ids for the production step saved to {out}")


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
    if "--apply-retest" in ARGS:
        return apply_retest(ARGS[ARGS.index("--apply-retest") + 1])
    if "--retest" in ARGS:
        return retest()
    if "--recheck" in ARGS:
        return recheck(int(ARGS[ARGS.index("--recheck") + 1]))
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
