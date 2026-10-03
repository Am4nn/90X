"""Write cards for thin archetypes, gate every one, and release only what clears everything.

    uv run python scripts/fill_archetypes.py --plan                       # candidate topics, no model
    uv run python scripts/fill_archetypes.py --per 3 --attempts 6         # a small pilot
    uv run python scripts/fill_archetypes.py threshold interleaving --per 15

Why this exists. Six archetypes ended with one to five live cards each because the writer was
never told what an archetype asks (only its label), so for a topic with no natural fit it wrote a
plausible card of another kind and the gate rejected it. The writer now sees the archetype's
`intent` and a `requires` precondition on the lesson and is free to refuse. This asks it, topic by
topic, for the archetypes that are short, and measures how many actually clear the gate.

The new cards are written as HELD drafts (`kept = false`) and stay held through every stage:

  1. write           the writer may refuse; a refusal costs a lesson read and refills nothing
  2. gate            `refile.verify`: the full answerability gate, options visible, only these ids
  3. key audit       the key must agree with the explanation, on two tiers; a contradiction from
                     EITHER rejects a new card, because losing one costs almost nothing
  4. duplicates      a new card that repeats a card in a more important topic is dropped
  5. release         only now `kept = true`

A crash at any point leaves held cards that `publish` ignores, never an ungated card ready to ship.
Writes nothing to production; publishing and taking cards live are separate, deliberate steps.
"""

import json
import os
import re
import sys
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone

sys.path.insert(0, "src")

import duckdb

from pipeline.cards import archetypes, key_audit, reconcile, refile, regate, validate, write
from pipeline.cards.archetypes import CardSlot
from pipeline.cards.run_lessons import hard_sources, hard_text
from pipeline.llm import LLM, BudgetExceeded, LLMError

ARGS = [a for a in sys.argv[1:]]
THIN = ["threshold", "impossible-bound", "class-relationship", "data-leak-spotter", "tap-the-insertion-point", "interleaving"]


def _opt(name: str, default: int) -> int:
    return int(ARGS[ARGS.index(name) + 1]) if name in ARGS else default


PER = _opt("--per", 12)
ATTEMPTS = _opt("--attempts", 40)
WORKERS = 6
PLAN = "--plan" in ARGS
WANTED = [a for a in ARGS if a in {x.id for x in archetypes.registry().archetypes}] or THIN
OUT = os.path.abspath("../.data/review/fill-archetypes.json")

# A cheap, deterministic filter on the lesson text, so the writer is not asked to read a lesson
# that plainly cannot support the archetype. The writer's own refusal is still the real check;
# this only saves reading lessons that have no chance. Ranked by how many distinct cues match.
CUES = {
    "threshold": r"threshold|break-?even|cross-?over|trade-?off|per second|qps|rps|latency|throughput|cut-?off|scales? (to|with)",
    "impossible-bound": r"lower bound|upper bound|impossib|cannot be|at most|at least|optimal|np-|omega|\bΩ|no algorithm",
    "interleaving": r"thread|concurren|race condition|lock|synchroniz|atomic|deadlock|interleav|mutex|volatile",
    # Lessons are prose with no code fences at all, so this cannot look for a snippet; the writer
    # invents one. The cue is a topic that describes how code behaves.
    "tap-the-insertion-point": r"\b(method|function|constructor|loop|query|statement|return|implement|variable|pointer|iterat)\w*",
    "class-relationship": r"inherit|composition|aggregat|association|dependency|is-a|has-a|extends|implements|uml",
    "data-leak-spotter": r"leak|training set|test set|validation|train/test|split|preprocess|normaliz|cross-valid|feature",
}


def cue_score(archetype_id: str, lesson: str) -> int:
    pattern = re.compile(CUES.get(archetype_id, "."), re.I)
    return len(set(m.group(0).lower() for m in pattern.finditer(lesson or "")))


def held(con, ids: list[str], keep: bool) -> None:
    for i in ids:
        con.execute("update cards set kept = ? where id = ? and status = 'draft'", [keep, i])
    con.commit()


def plan(con, topics: dict[str, dict]) -> dict[str, list[dict]]:
    """Per archetype: eligible topics that have a lesson, none of that archetype already, best cues first."""
    importance = dict(con.execute("select slug, importance from topics").fetchall())
    have = defaultdict(set)
    for slug, arch in con.execute(
        "select topic_slug, archetype from cards where kept = true and archetype is not null and status = 'draft'"
    ).fetchall():
        have[arch].add(slug)
    out: dict[str, list[dict]] = {}
    for aid in WANTED:
        a = archetypes.by_id(aid)
        rows = []
        for slug, t in topics.items():
            if t["domain"] not in a.areas or slug in have[aid]:
                continue
            score = cue_score(aid, t["lesson"])
            if score:
                rows.append({"topic": t, "score": score, "importance": importance.get(slug) or 0})
        rows.sort(key=lambda r: (-r["score"], -r["importance"], r["topic"]["slug"]))
        out[aid] = rows
    return out


def attempt(llm, con_lock, task: dict):
    """One writer call. Pure model work: no database access from a worker thread."""
    slot = CardSlot(task["archetype"], task["primitive"], task["difficulty"])
    try:
        result = write.write_one(llm, task["topic"], task["topic"]["lesson"], slot, task["hard"], "smart")
    except BudgetExceeded:
        raise
    return task, result


def main() -> None:
    # Read-write even to plan: the client records each call's cost in this database.
    con = duckdb.connect(os.path.abspath("../.data/staging.duckdb"))
    topics = {t["slug"]: t for t in regate.topics_with_cards(con)}
    candidates = plan(con, topics)
    print("candidate topics per archetype (lesson cues present, none of that archetype yet):")
    for aid in WANTED:
        print(f"  {aid:26} {len(candidates[aid]):>3} topics  areas={','.join(archetypes.by_id(aid).areas)}")
    if PLAN:
        return

    started = datetime.now(timezone.utc)
    llm = LLM(con)
    stats: dict[str, dict] = {aid: {"attempts": 0, "refused": 0, "written": 0} for aid in WANTED}
    refusals: dict[str, list[str]] = defaultdict(list)
    written_by_topic: dict[str, list] = defaultdict(list)
    difficulties = ["Medium", "Easy", "Hard"]

    for aid in WANTED:
        a = archetypes.by_id(aid)
        queue = list(candidates[aid])
        n = 0
        while stats[aid]["written"] < PER and queue and stats[aid]["attempts"] < ATTEMPTS:
            need = PER - stats[aid]["written"]
            wave = [queue.pop(0) for _ in range(min(len(queue), max(4, need * 2), ATTEMPTS - stats[aid]["attempts"]))]
            tasks = []
            for row in wave:
                diff = difficulties[n % len(difficulties)]
                diff = diff if diff in a.difficulties else a.difficulties[0]
                t = row["topic"]
                hard = hard_sources(con, t["slug"], t["domain"])
                tasks.append({"archetype": aid, "primitive": archetypes.pick_primitive(a, n), "difficulty": diff,
                              "topic": t, "hard": hard_text(hard) if diff == "Hard" else "", "hard_raw": hard})
                n += 1
            with ThreadPoolExecutor(max_workers=WORKERS) as pool:
                for fut in as_completed([pool.submit(attempt, llm, None, tk) for tk in tasks]):
                    try:
                        task, result = fut.result()
                    except BudgetExceeded as e:
                        print(f"  stopping: {e}", flush=True)
                        raise SystemExit(1) from None
                    except (LLMError, Exception) as e:  # noqa: BLE001 - one attempt's failure costs that attempt
                        print(f"  FAILED {type(e).__name__}: {str(e)[:90]}", flush=True)
                        continue
                    stats[aid]["attempts"] += 1
                    if isinstance(result, write.Card):
                        stats[aid]["written"] += 1
                        written_by_topic[task["topic"]["slug"]].append((result, task["hard_raw"]))
                    else:
                        stats[aid]["refused"] += 1
                        refusals[aid].append(result.reason)
        s = stats[aid]
        print(f"  {aid:26} attempts={s['attempts']:>3}  written={s['written']:>3}  refused={s['refused']:>3}", flush=True)

    # 1. Save as HELD drafts.
    for slug, items in written_by_topic.items():
        reconcile.save_additional(con, topics[slug], [c for c, _ in items], items[0][1])
    con.commit()
    new_ids = [r[0] for r in con.execute(
        "select id from cards where source = 'lesson' and status = 'draft' and list_contains(?, archetype) and created_at >= ?",
        [WANTED, started]).fetchall()]
    held(con, new_ids, False)
    print(f"\nwrote {len(new_ids)} held drafts")
    if not new_ids:
        return

    # 2. The full answerability gate, options visible, only these cards.
    out = refile.verify(con, llm, new_ids, tier="smart")
    survivors = [i for (i,) in con.execute(
        f"select id from cards where id in ({','.join('?' * len(new_ids))}) and status = 'draft'", new_ids).fetchall()]
    held(con, survivors, False)
    print(f"gate: {out['fit']} fit, {out['unfit']} rejected; {len(survivors)} continue")

    # 3. Key audit on two tiers; a contradiction from either rejects a NEW card.
    audited_out: set[str] = set()
    by_topic: dict[str, list] = defaultdict(list)
    for slug in {r[0] for r in con.execute(
            f"select topic_slug from cards where id in ({','.join('?' * len(survivors))})", survivors).fetchall()} if survivors else []:
        by_topic[slug] = [c for c in regate.cards_of(con, slug) if c.id in set(survivors) and key_audit.has_key(c)]
    for tier in ("fast", "smart"):
        for slug, cards in by_topic.items():
            for i in range(0, len(cards), 10):
                chunk = cards[i:i + 10]
                try:
                    res = key_audit.audit(llm, topics[slug], chunk, tier=tier)
                except (LLMError, Exception) as e:  # noqa: BLE001
                    print(f"  audit FAILED {type(e).__name__}: {str(e)[:80]}")
                    continue
                for idx, why in key_audit.contradictions(chunk, res).items():
                    audited_out.add(chunk[idx].id)
                    con.execute("update cards set status = 'rejected', kept = false, reject_reason = ? where id = ?",
                                [f"answer key contradicts the explanation: {why[:160]}", chunk[idx].id])
    con.commit()
    survivors = [i for i in survivors if i not in audited_out]
    print(f"key audit: {len(audited_out)} rejected; {len(survivors)} continue")

    # 4. A new card that repeats a card in a more important topic is dropped.
    mine = set(survivors)
    dupes = [(keep, dupe) for keep, dupe in validate.cross_topic_dupes(con) if dupe in mine]
    for keep, dupe in dupes:
        con.execute("update cards set status = 'rejected', kept = false, reject_reason = ? where id = ?",
                    [f"near-duplicate of {keep}", dupe])
    con.commit()
    survivors = [i for i in survivors if i not in {d for _, d in dupes}]
    print(f"duplicates: {len(dupes)} dropped; {len(survivors)} continue")

    # 5. Release.
    held(con, survivors, True)
    by_arch = defaultdict(int)
    for (arch,) in con.execute(
            f"select archetype from cards where id in ({','.join('?' * len(survivors))})", survivors).fetchall() if survivors else []:
        by_arch[arch] += 1
    print(f"\nreleased {len(survivors)} cards: {dict(by_arch)}")
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump({"released": survivors, "stats": stats, "refusals": {k: v[:8] for k, v in refusals.items()}}, fh, indent=1, ensure_ascii=False)
    print(f"saved to {OUT}. Publish and take them live as separate steps.")


if __name__ == "__main__":
    main()
