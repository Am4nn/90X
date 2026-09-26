"""Card quality trial: the same sources through Flash and Pro, every card
reviewed, written side by side to .data/review/card_trial.md for a human
to judge before any large generation run."""

import json

from ..config import DATA_DIR
from . import check, generate

DOC_SOURCES = ["system-design-primer", "system-design-karan", "ostep", "java-basics", "sql-basics", "last-minute-notes"]


def pick_sources(con, n_problems: int = 4) -> tuple[list[dict], list[dict]]:
    problems = [
        dict(zip(["slug", "title", "difficulty", "pattern_slug", "statement", "solutions"], r))
        for r in con.execute(
            """select slug, title, difficulty, pattern_slug, statement_md, solutions from problems
               where nc150 and statement_md is not null order by hash(slug) limit ?""", [n_problems]
        ).fetchall()
    ]
    for p in problems:
        sol = json.loads(p.pop("solutions") or "{}")
        p["solution"] = sol.get("python") or sol.get("java") or ""
        p["pattern"] = (p["pattern_slug"] or "").replace("-", " ")
    docs = []
    for source in DOC_SOURCES:
        row = con.execute(
            """select id, domain, title, body_md, topic_slug from documents
               where source_id = ? and length(body_md) between 1500 and 6000 order by hash(id) limit 1""", [source]
        ).fetchone()
        if row:
            docs.append(dict(zip(["id", "domain", "title", "body", "topic_slug"], row)))
    return problems, docs


def run(con, llm, tiers=("fast", "smart")) -> str:
    from ..llm import spend_usd

    problems, docs = pick_sources(con)
    lines = ["# Card quality trial", "",
             "Same sources, two generator models. Every card is reviewed twice: by DeepSeek Pro (same family as the",
             "generator) and by an independent model (REVIEW_MODEL). Scores are correct / clear / relevant, 1-5;",
             "a card is kept when all three are >= 4. The independent reviewer decides.", ""]
    summary = {t: {"cards": 0, "kept": 0, "cost": 0.0, "disagree": 0} for t in tiers}
    reviewer = "review" if "review" in llm.models else "smart"

    sources = [("problem", p, p["statement"] + "\n\n" + p["solution"]) for p in problems] + \
              [("doc", d, d["body"]) for d in docs]
    for kind, src, text in sources:
        title = src["title"]
        lines += [f"## {'Problem' if kind == 'problem' else src['domain'] + ' note'}: {title}", ""]
        for tier in tiers:
            before = spend_usd(con)
            try:
                cards = generate.for_problem(llm, src, tier) if kind == "problem" else generate.for_document(llm, src, tier)
            except Exception as e:
                lines += [f"### {tier}: generation failed ({e})", ""]
                continue
            self_checks = [check.review(llm, c, text, tier="smart") for c in cards]
            verdicts = [check.review(llm, c, text, tier=reviewer) for c in cards] if reviewer != "smart" else self_checks
            summary[tier]["cost"] += spend_usd(con) - before
            summary[tier]["cards"] += len(cards)
            summary[tier]["kept"] += sum(v["keep"] for v in verdicts)
            summary[tier]["disagree"] += sum(a["keep"] != b["keep"] for a, b in zip(self_checks, verdicts))
            lines += [f"### {llm.models[tier]}", ""]
            for c, v, sc in zip(cards, verdicts, self_checks):
                mark = "KEEP" if v["keep"] else "DROP"
                other = "" if reviewer == "smart" else f" (DeepSeek Pro: {'keep' if sc['keep'] else 'drop'} {sc['correct']}/{sc['clear']}/{sc['relevant']})"
                lines += [f"- **[{mark} {v['correct']}/{v['clear']}/{v['relevant']}]{other} {c['format']}, {c['difficulty']}**",
                          f"  - **Q:** {c['prompt']}"]
                if c.get("options"):
                    lines.append(f"  - **Options:** {' | '.join(c['options'])}")
                lines += [f"  - **A:** {c['answer']}", f"  - **Key points:** {'; '.join(c['key_points'])}"]
                if v["issues"]:
                    lines.append(f"  - *Reviewer:* {v['issues']}")
                if reviewer != "smart" and sc["issues"] and sc["keep"] != v["keep"]:
                    lines.append(f"  - *DeepSeek Pro:* {sc['issues']}")
            lines.append("")
    head = [f"Reviewer: {llm.models[reviewer]}", "",
            "| Generator | Cards | Kept by reviewer | Reviewers disagree | Cost (incl. both reviews) |", "|---|---|---|---|---|"]
    for tier in tiers:
        s = summary[tier]
        head.append(f"| {llm.models[tier]} | {s['cards']} | {s['kept']} | {s['disagree']} | ${s['cost']:.3f} |")
    lines[4:4] = head + [""]
    path = DATA_DIR / "review" / "card_trial.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")
    return str(path)
