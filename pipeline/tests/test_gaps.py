"""The write-up Aman actually reads.

The sort is a model call over ~2,000 candidates; the report is a rendering of
its verdicts. Handing over all 1,100 gaps and asking him to cut them is the
job, not the review - he had already said he would not read 320 cards.
"""

from pipeline.lessons import gaps


def row(domain, label, verdict="gap", relevance=0.0, why="", covered_by=""):
    return {"domain": domain, "label": label, "verdict": verdict,
            "relevance": relevance, "why": why, "covered_by": covered_by}


def test_the_shortlist_leads_and_the_unlikely_tail_is_below_the_line():
    out = gaps.report([
        row("ai", "Linear Regression", relevance=0.8, why="always asked"),
        row("ai", "Helm Charts", relevance=0.1, why="tooling, rarely asked"),
        row("cs", "Idempotency", relevance=0.9, why="asked directly"),
        row("cs", "Databases", verdict="too_broad"),
        row("cs", "Content Delivery Networks", verdict="covered", covered_by="CDN"),
    ])
    assert "**2 worth reading.**" in out
    shortlist, tail = out.split("## Below the line")
    assert "Idempotency" in shortlist and "Linear Regression" in shortlist
    assert "Helm Charts" not in shortlist, "an unlikely gap must not sit in the shortlist"
    assert "Helm Charts" in tail, "and must still be listed, because the score is a suggestion"
    assert "Content Delivery Networks -> CDN" in out


def test_the_same_topic_twice_is_one_line_at_its_best_score():
    """Each roadmap lists it with its own capitalisation, and each copy was
    sorted separately, so the list showed "Sampling Parameters" twice with
    different reasons."""
    out = gaps.report([
        row("ai", "Sampling Parameters", relevance=0.7, why="decoding parameters"),
        row("ai", " sampling parameters ", relevance=0.5, why="less certain"),
    ])
    assert out.count("Sampling Parameters") == 1
    assert "(0.7)" in out and "(0.5)" not in out
    assert "1 were the same topic listed twice" in out
