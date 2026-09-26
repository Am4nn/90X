"""Full card generation: pick important sources, generate with the fast model,
review each card with the independent reviewer, dedupe per topic, and store
in staging as one batch per area. Cards are saved as each source finishes and
sources that already have cards are skipped, so the run can be stopped and
resumed. A progress line reports spend per model and a projected total."""

import json
import time
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed

from . import check, generate

CARD_DOMAINS = ("system_design", "cs", "java", "sql")


def _sources(con, min_importance: float, limit: int | None) -> list[tuple[str, dict]]:
    done_problems = {r[0] for r in con.execute("select distinct problem_slug from cards where problem_slug is not null").fetchall()}
    done_docs = {r[0] for r in con.execute("select distinct document_id from cards where document_id is not null").fetchall()}
    out: list[tuple[str, dict]] = []
    for slug, title, diff, pattern, statement, solutions in con.execute(
        """select slug, title, difficulty, pattern_slug, statement_md, solutions from problems
           where kind = 'leetcode' and not premium and len(coalesce(topic_slugs, [])) = 0
             and statement_md is not null and pattern_slug is not null
             and (nc150 or blind75 or importance >= ?)
           order by importance desc""", [min_importance]
    ).fetchall():
        if slug in done_problems:
            continue
        sol = json.loads(solutions or "{}")
        out.append(("problem", {"slug": slug, "title": title, "difficulty": diff, "pattern_slug": pattern,
                                "pattern": pattern.replace("-", " "), "statement": statement,
                                "solution": sol.get("python") or sol.get("java") or ""}))
    for doc_id, domain, title, body, topic in con.execute(
        f"""select d.id, d.domain, d.title, d.body_md, d.topic_slug from documents d
            join topics t on t.slug = d.topic_slug
            where d.domain in ({', '.join('?' * len(CARD_DOMAINS))})
            order by t.importance desc, d.sort""", list(CARD_DOMAINS)
    ).fetchall():
        doc = {"id": doc_id, "domain": domain, "title": title, "body": body, "topic_slug": topic}
        if doc_id not in done_docs and generate.is_card_worthy(doc):
            out.append(("doc", doc))
    return out[:limit] if limit else out


def _one(llm, kind: str, src: dict) -> list[dict]:
    if kind == "problem":
        cards, text, domain = generate.for_problem(llm, src, tier="fast"), src["statement"] + "\n\n" + src["solution"], "dsa"
    else:
        cards, text, domain = generate.for_document(llm, src, tier="fast"), src["body"], src["domain"]
    tier = "review" if "review" in llm.models else "smart"
    for c in cards:
        verdict = check.review(llm, c, text, tier=tier)
        c.update({"domain": domain, "kept": verdict["keep"],
                  "quality": {k: verdict[k] for k in ("correct", "clear", "relevant", "issues")},
                  "source_refs": [{"kind": kind, "id": src.get("slug") or src.get("id"), "title": src["title"]}]})
    return cards


class _NoLock:
    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


def _save(con, batch_id: str, group: list[dict]) -> None:
    """Store one source's reviewed cards right away, so a crash or budget stop
    keeps everything finished so far. Duplicates are marked at the end."""
    for c in group:
        c["id"] = str(uuid.uuid4())
    con.executemany(
        """insert into cards (id, batch_id, topic_slug, problem_slug, document_id, format, difficulty, prompt_md,
               options, answer_md, key_points, source_refs, quality, status, kept)
           values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'draft', ?)""",
        [[c["id"], batch_id, c.get("topic_slug"), c.get("problem_slug"), c.get("document_id"), c["format"],
          c["difficulty"], c["prompt"], json.dumps(c["options"]) if c.get("options") else None, c["answer"],
          json.dumps(c["key_points"]), json.dumps(c["source_refs"]), json.dumps(c["quality"]), c["kept"]]
         for c in group],
    )


def _progress(i: int, total: int, cards: list[dict], llm, started: float, failed: int = 0) -> str:
    kept = sum(1 for c in cards if c["kept"])
    costs = getattr(llm, "run_costs", {})
    spend = sum(cost for _, cost in costs.values())
    per_model = ", ".join(f"{m} ${cost:.3f} ({n} calls)" for m, (n, cost) in sorted(costs.items()))
    elapsed = time.monotonic() - started
    eta_min = elapsed / i * (total - i) / 60 if i else 0
    projected = spend / i * total if i else 0
    return (f"  sources {i}/{total} ({failed} failed) | cards {len(cards)}, kept {kept / len(cards):.0%} | "
            f"run ${spend:.2f} -> projected ${projected:.2f} | {per_model} | eta {eta_min:.0f} min"
            if cards else f"  sources {i}/{total} | no cards yet | {per_model}")


def run(con, llm, min_importance: float = 0.5, limit: int | None = None, workers: int = 8,
        progress_every: int = 25) -> dict:
    sources = _sources(con, min_importance, limit)
    lock = getattr(llm, "lock", _NoLock())
    batches: dict[str, str] = {}
    cards: list[dict] = []
    failed = 0
    started = time.monotonic()
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = [pool.submit(_one, llm, kind, src) for kind, src in sources]
        for i, f in enumerate(as_completed(futures), 1):
            try:
                group = f.result()
            except Exception as e:  # budget stops, bad JSON: keep what we have
                failed += 1
                print(f"  skip: {e}", flush=True)
                group = []
            if group:
                domain = group[0]["domain"]
                with lock:
                    if domain not in batches:
                        batches[domain] = str(uuid.uuid4())
                        con.execute("insert into card_batches (id, domain, topic_slugs) values (?, ?, [])",
                                    [batches[domain], domain])
                    _save(con, batches[domain], group)
                cards.extend(group)
            if i % progress_every == 0 or i == len(sources):
                print(_progress(i, len(sources), cards, llm, started, failed), flush=True)

    for domain, batch_id in batches.items():
        group = [c for c in cards if c["domain"] == domain]
        kept = [c for c in group if c["kept"]]
        unique = {c["id"] for topic in {c.get("topic_slug") for c in kept}
                  for c in check.dedupe([k for k in kept if k.get("topic_slug") == topic])}
        dupes = [c["id"] for c in kept if c["id"] not in unique]
        if dupes:
            con.executemany("update cards set kept = false where id = ?", [[d] for d in dupes])
        con.execute("update card_batches set topic_slugs = ?, ai_pass_rate = ? where id = ?",
                    [sorted({c.get("topic_slug") for c in group if c.get("topic_slug")}),
                     round(len(kept) / len(group), 3), batch_id])
    return {"sources": len(sources), "cards": len(cards), "failed": failed,
            "kept": sum(1 for c in cards if c["kept"])}
