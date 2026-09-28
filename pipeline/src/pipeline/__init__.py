import argparse
import sys


def main() -> None:
    parser = argparse.ArgumentParser(prog="pipeline", description="90X data pipeline")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("sources", help="list all sources")

    dl = sub.add_parser("download", help="download sources into .data/")
    dl.add_argument("names", nargs="*", help="only these sources (default: all)")
    dl.add_argument("--domain", help="only sources in this domain")
    dl.add_argument("--role", help="only sources with this role")
    dl.add_argument("--skip-large", action="store_true", help="skip sources over 1 GB")

    norm = sub.add_parser("normalize", help="normalize raw sources into staging")
    norm.add_argument("targets", nargs="*", help="dsa (default), docs, competitive")
    norm.add_argument("--pool", type=int, default=2000, help="competitive: candidates to triage")
    en = sub.add_parser("enrich", help="importance + DSA topics (default), or AI pattern tagging")
    en.add_argument("step", nargs="?", choices=["basic", "patterns"], help="basic (default) or patterns")
    en.add_argument("--limit", type=int, help="only the N most important untagged problems")
    en.add_argument("--retag", action="store_true", help="re-tag problems that already have tags")
    tp = sub.add_parser("topics", help="draft topic lists for review, or apply approved ones")
    tp.add_argument("action", choices=["draft", "apply"])
    tp.add_argument("domains", nargs="*", help="system_design cs java sql lld ai behavioral (default: all)")
    sub.add_parser("tricks", help="build the pattern trick catalog (AI)")
    sub.add_parser("chunk", help="split documents and problems into chunks")
    sub.add_parser("embed", help="upload changed chunks to Upstash Vector")
    cd = sub.add_parser("cards", help="generate and review cards (AI)")
    cd.add_argument("--limit", type=int, help="at most N sources (for a trial)")
    cd.add_argument("--min-importance", type=float, default=0.5)
    ls = sub.add_parser("lessons", help="author one lesson per topic (AI)")
    ls.add_argument("topics", nargs="*", help="only these topic slugs (default: all unwritten)")
    ls.add_argument("--limit", type=int, help="at most N topics")
    ls.add_argument("--redo", action="store_true", help="rewrite topics that already have a lesson")
    ls.add_argument("--tier", default="smart", help="model tier: fast or smart")
    lc = sub.add_parser("lesson-cards", help="generate cards from lessons, gated (AI)")
    lc.add_argument("topics", nargs="*", help="only these topic slugs")
    lc.add_argument("--limit", type=int, help="at most N topics")
    lc.add_argument("--redo", action="store_true", help="regenerate topics that already have lesson cards")
    lc.add_argument("--tier", default="smart")
    cn = sub.add_parser("consistency", help="find claims that contradict across lessons in an area (AI)")
    cn.add_argument("domains", nargs="*", help="only these areas")
    cn.add_argument("--fix", action="store_true", help="rewrite the lesson each contradiction names")
    cn.add_argument("--redo", action="store_true",
                    help="run the check again instead of using the findings already stored")
    cn.add_argument("--tier", default="smart")
    sub.add_parser("card-review", help="write the card sample to review before a bulk run")
    sub.add_parser("lesson-review", help="write the short list of lessons worth reading")
    gp = sub.add_parser("gaps", help="sort roadmap nodes 90x lacks into real gaps (AI)")
    gp.add_argument("domains", nargs="*", help="only these areas")
    gp.add_argument("--tier", default="smart")
    gp.add_argument("--redo", action="store_true", help="sort every candidate again, not just the unsorted")
    gp.add_argument("--report-only", action="store_true",
                    help="rewrite the report from stored verdicts, without paying to sort again")
    cf = sub.add_parser("card-fix", help="apply .planning/card-objections.md to the cards named there (AI)")
    cf.add_argument("--tier", default="smart")
    cr = sub.add_parser("card-regate", help="judge the cards we already have again, after a gate change (AI)")
    cr.add_argument("topics", nargs="*", help="only these topic slugs")
    cr.add_argument("--tier", default="review")
    sub.add_parser("roadmaps", help="fetch roadmap.sh structures and stage their nodes")
    pb = sub.add_parser("publish", help="publish staging to Supabase")
    pb.add_argument("--dry-run", action="store_true", help="run everything, then roll back")
    pb.add_argument("--force", action="store_true",
                    help="delete published cards even when they hold study history")
    rb = sub.add_parser("rebatch", help="regroup draft cards into review batches (area x part)")
    rb.add_argument("--dry-run", action="store_true", help="show the batches without changing anything")
    sub.add_parser("status", help="counts and LLM spend in staging")

    args = parser.parse_args()

    from .commands import COMMANDS, run

    if args.command in COMMANDS:
        run(args.command, args)
        return

    # Imported here so `pipeline --help` stays fast.
    from .sources import SOURCES

    if args.command == "sources":
        for s in SOURCES:
            print(f"{s.domain:14} {s.role:12} {s.size_gb:6.2f} GB  {s.name:38} {s.target}")
        print(f"\n{len(SOURCES)} sources, ~{sum(s.size_gb for s in SOURCES):.1f} GB")
        return

    from .download import download

    selected = [
        s for s in SOURCES
        if (not args.names or s.name in args.names)
        and (not args.domain or s.domain == args.domain)
        and (not args.role or s.role == args.role)
        and (not args.skip_large or s.size_gb < 1)
    ]
    unknown = set(args.names) - {s.name for s in SOURCES}
    if unknown:
        sys.exit(f"Unknown sources: {', '.join(sorted(unknown))}")

    failed = download(selected)
    if failed:
        sys.exit(f"\nFailed: {', '.join(failed)}")
    print(f"\nDone: {len(selected)} sources")
