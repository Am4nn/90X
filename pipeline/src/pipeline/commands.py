"""Stage-B commands. Each takes parsed args and a staging connection."""

import types

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

    written, refused = run_lessons.run(
        con, only=args.topics or None, limit=args.limit, redo=args.redo, tier=args.tier
    )
    print(f"cards: {written} written, {refused} slots refused, spend ${llm.spend_usd(con):.2f}")


def trial(args, con) -> None:
    from .cards import trial as t

    t.run(con, tier=args.tier, thinking=args.writer_thinking)


def gate2(args, con) -> None:
    from . import llm
    from .cards import gate2 as g2

    result = g2.run(con, llm.LLM(con), n=args.n, tier=args.tier)
    print(f"gate2: {result['rejected']}/{result['cards']} rejected ({result['rate']:.0%}), "
          f"spend ${result['spend']:.4f}")


def consistency(args, con) -> None:
    import json
    from pathlib import Path

    from . import llm
    from .config import REPO_DIR
    from .lessons import consistency as c
    from .lessons import run as lesson_run

    ai = llm.LLM(con)
    # Findings on disk are reused, because re-running the check to apply a fix it
    # already found costs the whole $2.40 again. Filtered to the asked-for areas
    # BEFORE deciding whether to run: stored findings from another area used to
    # count as "already checked", so `consistency sql` with only cs findings on
    # disk wrote "None found" for sql without ever looking at it.
    wanted = set(args.domains or [])
    kept = [] if args.redo else [x for x in c.stored(con) if not wanted or x["domain"] in wanted]
    found = kept or c.run(con, ai, domains=args.domains or None, tier=args.tier)
    if wanted:
        found = [x for x in found if x["domain"] in wanted]

    out = Path(REPO_DIR) / ".planning" / "lesson-contradictions.md"
    # The report always covers everything known, even when this run looked at one
    # area: writing only the filtered subset deleted every other area's findings
    # from the file.
    everything = c.stored(con) or found
    lines = ["# Claims that disagree across lessons", "",
             f"{len(everything)} found." if everything else "None found.", ""]
    for x in sorted(everything, key=lambda x: (x["domain"], x["disagreement"])):
        lines += [f"## {x['domain']}: {', '.join(x['topics'])}", "",
                  f"- **They disagree:** {x['disagreement']}",
                  f"- **Correct:** {x['correct']}",
                  f"- **Rewriting:** `{x['fix']}`", ""]
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"{len(found)} contradictions in scope, {len(everything)} known, written to {out}")

    if args.fix and found:
        # Each named lesson is rewritten once, carrying the correction.
        for slug in sorted({x["fix"] for x in found}):
            notes = "\n".join(
                f"- [contradicts {', '.join(t for t in x['topics'] if t != slug)}] {x['correct']}"
                for x in found
                if x["fix"] == slug
            )
            con.execute("update lessons set status = 'draft', problems = ? where topic_slug = ?", [notes, slug])
        # Retired once applied. Keeping them meant the next --fix marked the same
        # corrected lessons for rewrite again, with the notes they had already
        # taken - scheduling work that was done and paying to redo it.
        c.retire(con, found)
        print(f"marked {len({x['fix'] for x in found})} lessons for rewrite; run `pipeline lessons` to redo them."
              " These findings are now retired, so the next `consistency` run checks afresh rather than"
              " re-applying them; the report file keeps the record.")
    print(f"spend ${llm.spend_usd(con):.2f}")


def card_review(args, con) -> None:
    from pathlib import Path

    from .cards import review_pack
    from .config import REPO_DIR

    out = Path(REPO_DIR) / ".planning" / "card-review.md"
    out.write_text(review_pack.report(con), encoding="utf-8")
    print(f"written to {out}")


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

    # --report-only rewrites the write-up from the verdicts already stored. The
    # sort costs a model run over ~2,000 candidates; the wording does not.
    rows = g.stored(con) if args.report_only else g.run(
        con, llm.LLM(con), domains=args.domains or None, tier=args.tier, redo=args.redo)
    if args.report_only and not rows:
        raise SystemExit("no stored verdicts: run `pipeline gaps` without --report-only first")
    out = Path(REPO_DIR) / ".planning" / "taxonomy-gaps.md"
    areas = [r[0] for r in con.execute("select distinct domain from topics order by 1").fetchall()]
    out.write_text(g.report(rows, areas), encoding="utf-8")
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

    for table, (n, deleted) in p.run(con, os.environ["DATABASE_URL"], dry_run=args.dry_run, force=args.force).items():
        print(f"  {table:15} {n:6} upserted, {deleted} removed")
    print("dry run: rolled back" if args.dry_run else "published")


def card_fix(args, con) -> None:
    from . import llm
    from .cards import fix

    fixed, failed = fix.run(con, llm.LLM(con), tier=args.tier, only=args.topics or None)
    print(f"card-fix: {fixed} fixed, {failed} still failing, spend ${llm.spend_usd(con):.2f}")


def card_regate(args, con) -> None:
    from . import llm
    from .cards import regate

    t = regate.run(con, only=args.topics or None, tier=args.tier)
    print(f"card-regate: {t['judged']} cards re-judged across {t['topics']} topics, "
          f"{t['recovered']} recovered, {t['reformatted']} rewritten and passed, "
          f"{t['rejected']} still rejected, spend ${llm.spend_usd(con):.2f}")


def card_validate(args, con) -> None:
    from .cards import validate

    print(validate.report(con))


def rebatch(args, con) -> None:
    from .cards import rebatch as rb

    summary = rb.run(con, dry_run=args.dry_run)
    for label, n in sorted(summary.items()):
        print(f"  {label:40} {n:5} cards")
    print(f"{len(summary)} batches" + (" (dry run)" if args.dry_run else ", in staging; run publish to send them"))


def swap(args, con) -> None:
    import os

    from .cards import swap as s

    result = s.run(os.environ["DATABASE_URL"], dry_run=not args.apply)
    if args.apply:
        print(f"swap applied: {result['retired']} retired, {result['activated']} activated, "
              f"{result['kept_live_uncovered_area']} kept live (area not in the catalogue)")
    else:
        print(f"dry run: would retire {result['retire_live']} live cards and "
              f"activate {result['activate_draft_archetyped']} draft archetyped cards")
        print(f"  keeping {result['kept_live_uncovered_area']} live cards whose area no archetype covers")
        print(f"  covered areas: {', '.join(result['covered_areas'])}")


def reconcile(args, con) -> None:
    """Trim each topic's surplus archetypes and write its shortfall."""
    from .cards import reconcile as rc
    from .llm import LLM

    llm = LLM(con, run_id=args.run_id) if args.run_id else None
    written, dropped, refused = rc.run(con, only=args.topics or None, tier=args.tier,
                                      llm=llm, dry_run=not args.apply)
    if args.apply:
        print(f"wrote {written}, trimmed {dropped}, refused {refused}")


def wellformed(args, con) -> None:
    """Audit the archetyped corpus against the registry's answer contract, and
    optionally reject what fails so the repair pass rewrites it.

    Free: no model call. This is the check that did not exist for nine of the ten
    primitives during the first full run, which is how 241 unanswerable cards
    reached the review pack.
    """
    import collections
    import json

    from .cards import wellformed as wf

    rows = con.execute(
        """select id, archetype, format, difficulty, options, picked, constraints, pairs,
                  value, tolerance, why_step
           from cards where archetype is not null and status = 'draft' order by id"""
    ).fetchall()

    loads = lambda v: json.loads(v) if v else None
    reasons: collections.Counter[str] = collections.Counter()
    by_primitive: collections.Counter[str] = collections.Counter()
    failed: list[tuple[str, str]] = []
    for row in rows:
        card = types.SimpleNamespace(
            id=row[0], archetype=row[1], format=row[2], difficulty=row[3],
            options=loads(row[4]), picked=loads(row[5]), constraints=loads(row[6]),
            pairs=loads(row[7]), value=row[8], tolerance=row[9], why_step=loads(row[10]))
        if found := wf.problems(card):
            failed.append((row[0], found[0]))
            by_primitive[row[2]] += 1
            for message in found:
                reasons[message.split(",")[0][:70]] += 1

    print(f"{len(rows)} archetyped draft cards, {len(failed)} not well formed "
          f"({100 * len(failed) / max(len(rows), 1):.1f}%), {len(rows) - len(failed)} clean")
    print("\nby primitive:")
    for primitive, n in by_primitive.most_common():
        print(f"  {primitive:14} {n:5}")
    print("\nby reason:")
    for reason, n in reasons.most_common(25):
        print(f"  {n:5}  {reason}")

    if not args.apply:
        print(f"\ndry run: {len(failed)} cards would be marked rejected. Re-run with --apply.")
        return
    con.executemany(
        "update cards set status = 'rejected', kept = false, reject_reason = ? where id = ?",
        [[f"not well formed: {reason}", card_id] for card_id, reason in failed],
    )
    print(f"\nmarked {len(failed)} cards rejected; run card-fix to rewrite them.")


COMMANDS = {"normalize": normalize, "enrich": enrich, "topics": topics, "tricks": tricks, "chunk": chunk,
            "embed": embed, "cards": cards, "lessons": lessons, "lesson-cards": lesson_cards, "roadmaps": roadmaps, "gaps": gaps, "lesson-review": lesson_review, "card-review": card_review, "card-fix": card_fix, "card-regate": card_regate, "card-validate": card_validate, "consistency": consistency, "publish": publish, "rebatch": rebatch, "swap": swap, "reconcile": reconcile, "wellformed": wellformed, "status": status, "trial": trial, "gate2": gate2}


def run(name: str, args) -> None:
    con = staging.connect()
    try:
        COMMANDS[name](args, con)
    finally:
        con.close()
