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

import re
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


def canonical(label: str) -> str:
    """One key per topic, however a roadmap happens to spell it.

    The candidate list carried "Big O", "Big-O Notation" and "Asymptotic
    Notation" as three separate topics, and "Queue" beside "Queues". Each was
    sorted separately, paid for separately, and reached the list Aman is meant
    to cut down. Punctuation, case and a trailing plural are not a new topic.
    """
    # Some punctuation IS the name. Stripping it made canonical("C"),
    # canonical("C++") and canonical("C#") all "c", so one would have been
    # marked covered by another, or merged away in the report.
    text = label.casefold().replace("++", " cpp").replace("#", " csharp")
    text = re.sub(r"[^a-z0-9 ]+", " ", text)
    words = [w[:-1] if len(w) > 3 and w.endswith("s") else w for w in text.split()]
    # Words that never distinguish one topic from another.
    return " ".join(w for w in words if w not in {"notation", "the", "a", "an", "and", "of", "to"})


def already_ours(con) -> dict[str, str]:
    """Every topic we have, keyed canonically - across all areas.

    This is the fix for the worst defect in the first sort: candidates were
    compared against their own area's topic names only. "Linked List" came off
    the CS roadmap, our Linked List topic is in DSA, and so it was structurally
    invisible - the model could not have got it right. Twenty gaps were exact
    name matches for topics we already had, four of them scored 0.9.
    """
    return {canonical(name): name
            for (name,) in con.execute("select name from topics order by sort").fetchall()}


# Words naming the shape of a topic rather than the topic. "Prompt Injection
# Attacks" is the subject "prompt injection", and searching a body for the whole
# phrase found nothing while the bare phrase was sitting in two lessons.
SUBJECT_NOISE = {"attack", "attacks", "basic", "basics", "overview", "introduction",
                 "fundamental", "fundamentals", "concept", "concepts", "notation",
                 "practice", "practices", "best", "technique", "techniques",
                 "strategy", "strategies", "type", "types"}
COMPARISON = re.compile(r"\s+(?:vs\.?|versus)\s+", re.IGNORECASE)


def subjects_of(label: str) -> list[str] | None:
    """The phrases a lesson must contain to be teaching this, or None.

    A comparison is two subjects, not one: "RAG vs Fine-tuning" never appears
    verbatim in prose, so the whole-phrase search found nothing even though both
    sides are taught. Each side is searched separately and every side must be
    present - otherwise half a comparison being mentioned would count as
    covering it, which is worse than not checking at all.

    None means the label is too short to search on, and the caller must not
    treat that as "not covered".
    """
    parts = COMPARISON.split(label) if COMPARISON.search(label) else [label]
    out = []
    for part in parts:
        words = re.sub(r"[^a-z0-9 ]+", " ", part.casefold()).split()
        kept = [w for w in words if w not in SUBJECT_NOISE] or words
        phrase = " ".join(kept).strip()
        if len(phrase) < 3:
            return None
        out.append(phrase)
    return out or None


def taught_in(con, label: str) -> list[str]:
    """Lessons whose body already teaches this, by name.

    The sorter only ever saw topic titles, so a subject covered inside another
    lesson looked like a gap: "Prompt Injection" is taught in two lessons and
    was still scored 0.7. Titles are what a taxonomy knows; bodies are what a
    reader actually gets.

    Bounded at both ends, with only the inflections a topic name actually takes.
    An opening boundary alone let "RAG" match "ragged arrays", which would mark
    a real gap covered on the strength of a coincidence; the suffix group keeps
    "index" finding "indexes" and "indexing".
    """
    subjects = subjects_of(label)
    if not subjects:
        return []
    clause = " and ".join("regexp_matches(lower(body_md), ?)" for _ in subjects)
    return [r[0] for r in con.execute(
        f"select topic_slug from lessons where status = 'ok' and {clause} order by topic_slug",
        [rf"\b{re.escape(subject)}(?:s|es|ing|ed)?\b" for subject in subjects],
    ).fetchall()]


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


def run(con, llm, domains: list[str] | None = None, tier: str = "smart", redo: bool = False) -> list[dict]:
    """Returns every candidate with its verdict, ready to be written up.

    Resumes by default: a candidate already sorted is not sorted again. The
    first run died on a provider balance error with two areas left, and
    starting over would have paid a second time for the 1,357 verdicts already
    stored. `redo` sorts everything again, for when the prompt changes.
    """
    rows = uncovered(con)
    wanted = set(domains or {r["domain"] for r in rows})
    done = set() if redo else {(r["domain"], r["label"]) for r in stored(con)}
    out: list[dict] = [r for r in stored(con) if r["domain"] in wanted] if not redo else []
    ours_everywhere = already_ours(con)
    # Everything a query can settle is settled before the model is asked. It got
    # these wrong - "Linked List", "Stack", "Binary Search" and "CAP Theorem"
    # came back as gaps at 0.8 and above - and it was never going to get them
    # right, because it only ever saw one area's topic names and one area's
    # titles. Cheaper and correct beats a second opinion on a fact.
    settled: list[dict] = []
    for row in rows:
        # Not skipped when already stored: correcting a stored verdict is the
        # point. A query proving we own the topic outranks the model's guess
        # that we do not, and the stored guesses are what put "Linked List" in
        # front of Aman at 0.9.
        if match := ours_everywhere.get(canonical(row["label"])):
            settled.append({**row, "verdict": "covered", "covered_by": match,
                            "relevance": 0.0, "why": ""})
    if settled:
        print(f"{len(settled)} candidates settled without asking the model", flush=True)
        save(con, settled)
        # Replace, never append: `out` already holds the stored verdict for
        # these, and two rows for one candidate would put it in the report twice
        # with opposite answers.
        corrected = {(s["domain"], s["label"]): s for s in settled}
        out = [corrected.pop((r["domain"], r["label"]), r) for r in out]
        out += [s for k, s in corrected.items() if s["domain"] in wanted]
        done |= {(s["domain"], s["label"]) for s in settled}

    for domain in sorted(wanted):
        ours = [r[0] for r in con.execute("select name from topics where domain = ? order by sort", [domain]).fetchall()]
        candidates = [r["label"] for r in rows
                      if r["domain"] == domain and (domain, r["label"]) not in done]
        if not candidates:
            print(f"  {domain}: already sorted", flush=True)
            continue
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

    # A phrase found in a lesson body is a hint, not a verdict, so it annotates
    # the candidate rather than settling it. Treating it as coverage marked
    # "Linear Search" covered because some lesson happened to name it, and a
    # covered candidate drops out of the list Aman reads - so a passing mention
    # could hide a lesson still worth writing. He can tell a mention from a
    # treatment; a LIKE query cannot.
    annotated = []
    for row in out:
        if row["verdict"] != "gap":
            continue
        lessons = taught_in(con, row["label"])
        if not lessons:
            continue
        where = ", ".join(lessons[:2]) + (f" and {len(lessons) - 2} more" if len(lessons) > 2 else "")
        note = f"already named in {len(lessons)} {'lesson' if len(lessons) == 1 else 'lessons'} ({where})"
        if note not in (row["why"] or ""):
            row["why"] = f"{row['why']} - {note}".strip(" -")
            annotated.append(row)
    if annotated:
        save(con, annotated)
        print(f"{len(annotated)} gaps are already named in a lesson; noted, not removed", flush=True)
    return out


LIKELY = 0.7  # "an interview will go here", in the sorter's own terms


def _dedupe(gaps: list[dict]) -> list[dict]:
    """One row per topic, keeping the highest relevance it was given.

    The same topic appears on several roadmaps spelled differently, and each
    copy was sorted separately, so the list Aman reads had "Sampling
    Parameters" twice with different reasons, and "Big O" beside "Big-O
    Notation". `canonical` collapses punctuation, case, plurals and filler
    words; it will not collapse genuine synonyms like "Asymptotic Notation",
    which needs a model to see."""
    best: dict[tuple[str, str], dict] = {}
    for row in gaps:
        key = (row["domain"], canonical(row["label"]))
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
