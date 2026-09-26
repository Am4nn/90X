"""Full card generation: pick important sources, generate with the fast model,
review each card with the independent reviewer, dedupe per topic, and store
in staging as one batch per area. Sources that already have cards are skipped,
so the run can be stopped and resumed."""

import json
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


def run(con, llm, min_importance: float = 0.5, limit: int | None = None, workers: int = 8) -> dict:
    sources = _sources(con, min_importance, limit)
    cards: list[dict] = []
    failed = 0
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = [pool.submit(_one, llm, kind, src) for kind, src in sources]
        for i, f in enumerate(as_completed(futures), 1):
            try:
                cards.extend(f.result())
            except Exception as e:  # budget stops, bad JSON: keep what we have
                failed += 1
                print(f"  skip: {e}", flush=True)
            if i % 100 == 0:
                print(f"  sources {i}/{len(sources)}, cards {len(cards)}", flush=True)

    by_domain: dict[str, list[dict]] = {}
    for c in cards:
        by_domain.setdefault(c["domain"], []).append(c)
    for domain, group in by_domain.items():
        kept = [c for c in group if c["kept"]]
        unique_ids = {id(c) for topic in {c.get("topic_slug") for c in kept}
                      for c in check.dedupe([k for k in kept if k.get("topic_slug") == topic])}
        batch_id = str(uuid.uuid4())
        con.execute("insert into card_batches (id, domain, topic_slugs, ai_pass_rate) values (?, ?, ?, ?)",
                    [batch_id, domain, sorted({c.get("topic_slug") for c in group if c.get("topic_slug")}),
                     round(len(kept) / len(group), 3) if group else None])
        con.executemany(
            """insert into cards (id, batch_id, topic_slug, problem_slug, document_id, format, difficulty, prompt_md,
                   options, answer_md, key_points, source_refs, quality, status, kept)
               values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'draft', ?)""",
            [[str(uuid.uuid4()), batch_id, c.get("topic_slug"), c.get("problem_slug"), c.get("document_id"), c["format"],
              c["difficulty"], c["prompt"], json.dumps(c["options"]) if c.get("options") else None, c["answer"],
              json.dumps(c["key_points"]), json.dumps(c["source_refs"]), json.dumps(c["quality"]),
              c["kept"] and id(c) in unique_ids] for c in group],
        )
    return {"sources": len(sources), "cards": len(cards), "failed": failed,
            "kept": sum(1 for c in cards if c["kept"])}
