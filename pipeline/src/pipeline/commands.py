"""Stage-B commands. Each takes parsed args and a staging connection."""

from . import staging


def normalize(args, con) -> None:
    targets = args.targets or ["dsa"]
    for target in targets:
        if target == "dsa":
            from .normalize import dsa

            print(f"dsa: {dsa.run(con)} problems")
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
        print(f"patterns: {patterns.run(con, ai, limit=args.limit)} problems tagged, spend ${llm.spend_usd(con):.2f}")
        print(f"sample for review: {patterns.write_sample(con)}")


COMMANDS = {"normalize": normalize, "enrich": enrich, "status": status}


def run(name: str, args) -> None:
    con = staging.connect()
    try:
        COMMANDS[name](args, con)
    finally:
        con.close()
