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
    norm.add_argument("targets", nargs="*", help="dsa (default), docs")
    sub.add_parser("enrich", help="importance scores and DSA topics")
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
