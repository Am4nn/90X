"""Stage-B commands. Each takes parsed args and a staging connection."""

from . import staging


def normalize(args, con) -> None:
    targets = args.targets or ["dsa"]
    for target in targets:
        if target == "dsa":
            from .normalize import dsa

            print(f"dsa: {dsa.run(con)} problems")
        elif target == "competitive":
            from . import llm
            from .normalize import competitive

            print(f"competitive: {competitive.run(con, llm.LLM(con), pool_size=args.pool)} problems, spend ${llm.spend_usd(con):.2f}")
        elif target == "docs":
            from .normalize import docs

            print(f"docs: {docs.run(con)} documents")
        else:
            raise SystemExit(f"Unknown normalize target: {target}")


def status(args, con) -> None:
    from .llm import spend_usd

    def count(sql: str) -> int:
        return con.execute(sql).fetchone()[0]

    print("problems")
    for kind, n in con.execute("select kind, count(*) from problems group by kind order by kind").fetchall():
        print(f"  {kind:12} {n}")
    print(f"  with statement   {count('select count(*) from problems where statement_md is not null')}")
    print(f"  with pattern     {count('select count(*) from problems where pattern_slug is not null')}")
    print(f"  NeetCode 150     {count('select count(*) from problems where nc150')}")
    print(f"  with companies   {count('select count(*) from problems where json_array_length(json_keys(companies)) > 0')}")
    print(f"documents          {count('select count(*) from documents')}")
    print(f"topics             {count('select count(*) from topics')}")
    print(f"chunks             {count('select count(*) from chunks')}")
    print(f"cards              {count('select count(*) from cards')}")
    print(f"LLM spend          ${spend_usd(con):.4f}")


def enrich(args, con) -> None:
    from .enrich import importance, topics

    step = getattr(args, "step", None)
    if step in (None, "basic"):
        print(f"importance: {importance.run(con)} problems scored")
        print(f"topics: {topics.apply_dsa(con)} DSA patterns + roadmap links")
    if step == "patterns":
        from . import llm
        from .enrich import patterns

        ai = llm.LLM(con)
        print(f"patterns: {patterns.run(con, ai, limit=args.limit, retag=args.retag)} problems tagged, spend ${llm.spend_usd(con):.2f}")
        print(f"sample for review: {patterns.write_sample(con)}")


def topics(args, con) -> None:
    from . import llm
    from .enrich import topic_lists

    ai = llm.LLM(con)
    domains = args.domains or list(topic_lists.PREFIX)
    for domain in domains:
        if args.action == "draft":
            print(f"{domain}: drafted {topic_lists.draft(con, ai, domain)}")
        else:
            print(f"{domain}: {len(topic_lists.load(domain))} topics, {topic_lists.apply(con, ai, domain)} documents assigned")
    print(f"spend ${llm.spend_usd(con):.2f}")


def tricks(args, con) -> None:
    from . import llm
    from .enrich import tricks as t

    print(f"tricks: {t.build(con, llm.LLM(con))} tricks, spend ${llm.spend_usd(con):.2f}")


def chunk(args, con) -> None:
    from . import chunk as c

    print(f"chunks: {c.run(con)}")


def embed(args, con) -> None:
    from . import vector

    up, deleted, left = vector.run(con)
    print(f"vector: {up} upserted, {deleted} deleted, {left} left for another day (10K/day free limit)")


def cards(args, con) -> None:
    from . import llm
    from .cards import run as card_run

    ai = llm.LLM(con)
    stats = card_run.run(con, ai, min_importance=args.min_importance, limit=args.limit)
    print(f"cards: {stats}, spend ${llm.spend_usd(con):.2f}")


def lessons(args, con) -> None:
    from . import llm
    from .lessons import run as lesson_run

    written, failed = lesson_run.run(
        con, only=args.topics or None, limit=args.limit, redo=args.redo, tier=args.tier
    )
    print(f"lessons: {written} written, {failed} failed, spend ${llm.spend_usd(con):.2f}")


def lesson_cards(args, con) -> None:
    from . import llm
    from .cards import run_lessons

    kept, rejected = run_lessons.run(
        con, only=args.topics or None, limit=args.limit, redo=args.redo, tier=args.tier
    )
    total = kept + rejected
    share = rejected / total if total else 0
    print(f"cards: {kept} kept, {rejected} rejected ({share:.0%}), spend ${llm.spend_usd(con):.2f}")


def lesson_review(args, con) -> None:
    from pathlib import Path

    from .config import REPO_DIR
    from .lessons import review_pack

    out = Path(REPO_DIR) / ".planning" / "lesson-review.md"
    out.write_text(review_pack.report(con), encoding="utf-8")
    print(f"written to {out}")


def gaps(args, con) -> None:
    from pathlib import Path

    from . import llm
    from .config import REPO_DIR
    from .lessons import gaps as g

    rows = g.run(con, llm.LLM(con), domains=args.domains or None, tier=args.tier)
    out = Path(REPO_DIR) / ".planning" / "taxonomy-gaps.md"
    out.write_text(g.report(rows), encoding="utf-8")
    kept = sum(1 for r in rows if r["verdict"] == "gap")
    print(f"gaps: {kept} of {len(rows)} candidates are real, written to {out}, spend ${llm.spend_usd(con):.2f}")


def roadmaps(args, con) -> None:
    from . import roadmaps as rm

    counts = rm.fetch()
    staged = rm.normalize(con)
    linked = con.execute("select count(*) from roadmap_nodes where topic_slug is not null").fetchone()[0]
    print(f"{len(counts)} roadmaps, {staged} nodes staged, {linked} linked to a topic")


def publish(args, con) -> None:
    import os

    from . import publish as p

    for table, (n, deleted) in p.run(con, os.environ["DATABASE_URL"], dry_run=args.dry_run).items():
        print(f"  {table:15} {n:6} upserted, {deleted} removed")
    print("dry run: rolled back" if args.dry_run else "published")


def rebatch(args, con) -> None:
    import os

    from .cards import rebatch as rb

    summary = rb.run(con, None if args.dry_run else os.environ["DATABASE_URL"], dry_run=args.dry_run)
    for label, n in sorted(summary.items()):
        print(f"  {label:40} {n:5} cards")
    print(f"{len(summary)} batches" + (" (dry run)" if args.dry_run else ", applied to staging and Supabase"))


COMMANDS = {"normalize": normalize, "enrich": enrich, "topics": topics, "tricks": tricks, "chunk": chunk,
            "embed": embed, "cards": cards, "lessons": lessons, "lesson-cards": lesson_cards, "roadmaps": roadmaps, "gaps": gaps, "lesson-review": lesson_review, "publish": publish, "rebatch": rebatch, "status": status}


def run(name: str, args) -> None:
    con = staging.connect()
    try:
        COMMANDS[name](args, con)
    finally:
        con.close()
