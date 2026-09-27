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
    """Roadmap nodes with no topic, most prominent first."""
    rows = con.execute(
        """select domain, label, kind, min(sort) as sort, count(*) as seen
           from roadmap_nodes
           where topic_slug is null and (? is null or domain = ?)
           group by domain, label, kind
           order by domain, kind desc, seen desc, sort""",
        [domain, domain],
    ).fetchall()
    return [dict(zip(["domain", "label", "kind", "sort", "seen"], r)) for r in rows]


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
    return out


def report(rows: list[dict]) -> str:
    """The list Aman cuts down, gaps first and most interview-relevant first."""
    gaps = sorted([r for r in rows if r["verdict"] == "gap"], key=lambda r: (r["domain"], -r["relevance"]))
    n_covered = sum(1 for r in rows if r["verdict"] == "covered")
    n_broad = sum(1 for r in rows if r["verdict"] == "too_broad")
    lines = [
        "# Topics roadmap.sh has that 90x does not",
        "",
        f"{len(gaps)} real {'gap' if len(gaps) == 1 else 'gaps'} out of {len(rows)} candidates. "
        f"{n_covered} {'was' if n_covered == 1 else 'were'} already covered under another name, and "
        f"{n_broad} {'was a heading' if n_broad == 1 else 'were headings'}, not topics.",
        "",
        "**Cut this list down.** Anything you keep gets a lesson written for it, "
        "at roughly $0.04 each. Deleting a line is the whole review.",
        "",
    ]
    domain = None
    for row in gaps:
        if row["domain"] != domain:
            domain = row["domain"]
            lines += ["", f"## {domain}", ""]
        lines.append(f"- **{row['label']}** ({row['relevance']:.1f}) - {row['why']}")
    covered = [r for r in rows if r["verdict"] == "covered"]
    if covered:
        lines += ["", "---", "", "## Already covered under another name", ""]
        lines += [f"- {r['label']} -> {r['covered_by']}" for r in covered]
    return "\n".join(lines)
