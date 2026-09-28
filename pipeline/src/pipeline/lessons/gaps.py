"""What roadmap.sh covers that 90x does not - separated from what only looks missing.

Exact-name matching leaves 306 topic-level nodes unmatched, but most are not
gaps. "Content Delivery Networks" is our CDN topic under another name, and
"Introduction", "Databases" and "Security" are section headers on a diagram
rather than anything you could write a lesson about. Handing over all 306
would be handing over the job of sorting them.

So a model sorts each node into covered / too_broad / gap and rates how
likely a real SDE interview is to go there. Aman approves the shortlist; the
ranking is a suggestion, never the decision, because this is exactly where a
curated 274 quietly becomes an unfocused 800.
"""

from datetime import datetime, timezone
from typing import Literal

from pydantic import BaseModel, Field

BATCH = 40

SYSTEM = """You are sorting topics for an interview-prep app used by engineers preparing for SDE interviews.

You are given the topics 90x already covers in one area, then a list of candidate topics taken from a public developer roadmap. For each candidate, decide:

- "covered": 90x already has this under a different name. Give the existing topic's exact name in `covered_by`. "Content Delivery Networks" is covered by "CDN"; "Load Balancers" is covered by "Load balancing".
- "too_broad": it is a heading rather than a topic, or so broad that a single lesson would be meaningless. "Introduction", "Databases", "Communication", "Security".
- "gap": a real, specific topic that an SDE interview could go into and 90x does not have.

For a "gap", rate `relevance` from 0 to 1: how likely is a real SDE interview loop at a product company to go into this? Operations and tooling that engineers use but are rarely asked to explain (Terraform, Helm charts, CI runners) score low. Things that get asked directly - idempotency, consistency models, indexing strategy - score high.

Be strict. Marking something a gap means someone writes and reviews a lesson for it."""


class Judgement(BaseModel):
    label: str = Field(description="the candidate, copied exactly")
    verdict: Literal["covered", "too_broad", "gap"]
    covered_by: str = Field(default="", description="covered only: the existing topic's name")
    relevance: float = Field(default=0.0, ge=0, le=1, description="gap only: 0 to 1")
    why: str = Field(default="", description="gap only: one short sentence")


class Judgements(BaseModel):
    judgements: list[Judgement]


def uncovered(con, domain: str | None = None) -> list[dict]:
    """Roadmap nodes with no topic, most prominent first.

    Grouping on the raw label treated " Logistic Regression " and "Logistic
    Regression" as two candidates, so both were sorted, both were paid for, and
    both reached the list Aman is meant to cut down. Trim and collapse the
    whitespace first, and group on that.
    """
    rows = con.execute(
        """select domain, trim(regexp_replace(label, '\\s+', ' ', 'g')) as label, kind,
                  min(sort) as sort, count(*) as seen
           from roadmap_nodes
           where topic_slug is null and (? is null or domain = ?)
           group by domain, 2, kind
           order by domain, kind desc, seen desc, sort""",
        [domain, domain],
    ).fetchall()
    return [dict(zip(["domain", "label", "kind", "sort", "seen"], r)) for r in rows]


def save(con, rows: list[dict]) -> None:
    """Keep the verdicts, so rewriting the report costs nothing."""
    now = datetime.now(timezone.utc)
    con.executemany(
        """insert or replace into taxonomy_gaps
           (domain, label, verdict, covered_by, relevance, why, judged_at)
           values (?, ?, ?, ?, ?, ?, ?)""",
        [[r["domain"], r["label"], r["verdict"], r["covered_by"], r["relevance"], r["why"], now] for r in rows],
    )


def stored(con) -> list[dict]:
    rows = con.execute(
        "select domain, label, verdict, covered_by, relevance, why from taxonomy_gaps"
    ).fetchall()
    return [dict(zip(["domain", "label", "verdict", "covered_by", "relevance", "why"], r)) for r in rows]


def judge(llm, domain: str, our_topics: list[str], candidates: list[str], tier: str = "smart") -> list[Judgement]:
    user = (
        f"Area: {domain}\n\n"
        f"Topics 90x already covers ({len(our_topics)}):\n"
        + "\n".join(f"- {t}" for t in our_topics)
        + "\n\nCandidates to sort:\n"
        + "\n".join(f"- {c}" for c in candidates)
    )
    return llm.complete_json(SYSTEM, user, Judgements, tier=tier, purpose="taxonomy-gaps").judgements


def run(con, llm, domains: list[str] | None = None, tier: str = "smart") -> list[dict]:
    """Returns every candidate with its verdict, ready to be written up."""
    rows = uncovered(con)
    wanted = set(domains or {r["domain"] for r in rows})
    out: list[dict] = []
    for domain in sorted(wanted):
        ours = [r[0] for r in con.execute("select name from topics where domain = ? order by sort", [domain]).fetchall()]
        candidates = [r["label"] for r in rows if r["domain"] == domain]
        for i in range(0, len(candidates), BATCH):
            chunk = candidates[i : i + BATCH]
            judged = {j.label: j for j in judge(llm, domain, ours, chunk, tier=tier)}
            for label in chunk:
                j = judged.get(label)
                # A candidate the model skipped stays visible as unsorted rather
                # than silently vanishing from the list Aman reviews.
                out.append({
                    "domain": domain,
                    "label": label,
                    "verdict": j.verdict if j else "unsorted",
                    "covered_by": j.covered_by if j else "",
                    "relevance": j.relevance if j else 0.0,
                    "why": j.why if j else "",
                })
            print(f"  {domain}: sorted {min(i + BATCH, len(candidates))}/{len(candidates)}", flush=True)
            # Saved per batch, not at the end. A 33-minute run over 1,959
            # candidates that dies on the last batch should not have to start
            # over, and the report is rewritten far more often than the sort.
            save(con, out[-len(chunk):])
    return out


LIKELY = 0.7  # "an interview will go here", in the sorter's own terms


def _dedupe(gaps: list[dict]) -> list[dict]:
    """One row per topic, keeping the highest relevance it was given.

    The same topic appears on several roadmaps under slightly different
    capitalisation, and each copy was sorted separately, so the list Aman reads
    had "Sampling Parameters" twice with different reasons."""
    best: dict[tuple[str, str], dict] = {}
    for row in gaps:
        key = (row["domain"], " ".join(row["label"].split()).casefold())
        if key not in best or row["relevance"] > best[key]["relevance"]:
            best[key] = row
    return list(best.values())


def _listing(rows: list[dict]) -> list[str]:
    lines: list[str] = []
    domain = None
    for row in sorted(rows, key=lambda r: (r["domain"], -r["relevance"], r["label"])):
        if row["domain"] != domain:
            domain = row["domain"]
            lines += ["", f"### {domain}", ""]
        lines.append(f"- **{' '.join(row['label'].split())}** ({row['relevance']:.1f}) - {row['why']}")
    return lines


def report(rows: list[dict], all_domains: list[str] | None = None) -> str:
    """The list Aman cuts down.

    The first version handed over all 1,100 gaps and asked him to cut them,
    which is the job rather than the review - and he had already said plainly
    he would not read 320 cards. The sorter scores each gap for how likely an
    interview is to go there, so the report leads with the ones it scored 0.7
    and up and counts the rest. The tail is still listed, because a suggestion
    is not a decision, but it is below the line.
    """
    gaps = _dedupe([r for r in rows if r["verdict"] == "gap"])
    likely = [r for r in gaps if r["relevance"] >= LIKELY]
    tail = [r for r in gaps if r["relevance"] < LIKELY]
    n_covered = sum(1 for r in rows if r["verdict"] == "covered")
    n_broad = sum(1 for r in rows if r["verdict"] == "too_broad")
    duplicates = sum(1 for r in rows if r["verdict"] == "gap") - len(gaps)

    lines = [
        "# Topics roadmap.sh has that 90x does not",
        "",
        f"**{len(likely)} worth reading.** Of {len(rows)} candidates, {len(gaps)} are gaps 90x "
        f"genuinely does not cover, and {len(likely)} of those scored {LIKELY} or higher for "
        "\"a real SDE loop will go here\". The other "
        f"{len(tail)} are gaps the sorter itself rated unlikely to come up; they are below the line.",
        "",
        f"{n_covered} candidates were already covered under another name and "
        f"{n_broad} were headings rather than topics"
        + (f"; {duplicates} {'was' if duplicates == 1 else 'were'} the same topic listed twice."
           if duplicates else "."),
        "",
        "**Deleting a line is the whole review.** Anything you keep gets a lesson written for "
        "it, at roughly $0.04 each - and 90x is 274 curated topics, which is the thing worth "
        "protecting. The score is a suggestion, not a decision.",
        "",
    ]
    # A partial sort must say which areas it never reached. Otherwise an empty
    # section reads as "no gaps here", which is the opposite of "not looked at".
    missing = sorted(set(all_domains or []) - {r["domain"] for r in rows})
    if missing:
        lines += [
            f"> **{', '.join(missing)} {'is' if len(missing) == 1 else 'are'} missing from this "
            f"report.** The sort stopped before reaching {'it' if len(missing) == 1 else 'them'}, "
            "so an absent area means nothing was looked at, not that nothing was found.",
            "",
        ]
    lines.append("## Worth writing")
    lines += _listing(likely)
    if tail:
        lines += [
            "",
            "---",
            "",
            f"## Below the line ({len(tail)})",
            "",
            "The sorter called each of these a real gap and then rated an interview unlikely "
            "to reach it - mostly tooling and operations engineers use without being asked to "
            "explain. Here in case it was wrong about one.",
        ]
        lines += _listing(tail)
    covered = _dedupe([r for r in rows if r["verdict"] == "covered"])
    if covered:
        lines += ["", "---", "", f"## Already covered under another name ({len(covered)})", ""]
        lines += [f"- {' '.join(r['label'].split())} -> {r['covered_by']}"
                  for r in sorted(covered, key=lambda r: (r["domain"], r["label"]))]
    return "\n".join(lines)
