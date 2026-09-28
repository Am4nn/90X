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
    assert "1 was the same topic listed twice" in out


def test_an_area_the_sort_never_reached_says_so():
    """The sort died on a provider balance error two areas from the end. An
    empty section reads as "no gaps here", which is the opposite of the
    truth, and nobody rereads a report to notice a heading is absent."""
    out = gaps.report(
        [row("ai", "Linear Regression", relevance=0.8, why="always asked")],
        all_domains=["ai", "sql", "system_design"],
    )
    assert "sql, system_design are missing from this report" in out
    assert "nothing was looked at, not that nothing was found" in out


def test_a_complete_sort_carries_no_missing_note():
    out = gaps.report(
        [row("ai", "Linear Regression", relevance=0.8, why="always asked")],
        all_domains=["ai"],
    )
    assert "missing from this report" not in out


def test_a_topic_we_already_have_is_never_asked_about(tmp_path):
    """The worst defect in the first sort: candidates were compared against
    their own area's topic names only. "Linked List" came off the CS roadmap,
    our Linked List topic is in DSA, so it was structurally invisible - and it
    came back a gap at 0.9. Twenty gaps were exact matches for topics we had."""
    from pipeline import staging

    con = staging.connect(tmp_path / "s.duckdb")
    con.execute("""insert into topics (slug, domain, name, sort) values
        ('linked-list', 'dsa', 'Linked List', 1), ('sd-cap-theorem', 'system_design', 'CAP theorem', 2)""")
    ours = gaps.already_ours(con)
    assert ours[gaps.canonical("Linked Lists")] == "Linked List"
    assert ours[gaps.canonical("CAP Theorem")] == "CAP theorem"


def test_a_subject_taught_inside_another_lesson_is_covered(tmp_path):
    """The sorter only ever saw topic titles. "Prompt Injection" is taught in
    two lesson bodies and was still scored 0.7 as a gap."""
    from pipeline import staging

    con = staging.connect(tmp_path / "s.duckdb")
    con.execute("""insert into lessons (topic_slug, title, body_md, status) values
        ('ai-generative-ai-llms', 'Generative AI', 'A prompt injection attack rewrites the instruction.', 'ok')""")
    assert gaps.taught_in(con, "Prompt Injection") == ["ai-generative-ai-llms"]
    assert gaps.taught_in(con, "Kubernetes Operators") == []


def test_spelling_variants_are_one_topic():
    assert gaps.canonical("Big-O Notation") == gaps.canonical("Big O")
    assert gaps.canonical("Queues") == gaps.canonical("Queue")
    assert gaps.canonical("Load Balancers") == gaps.canonical("load balancer")
    # Not a synonym engine: this one needs a model to see, and pretending
    # otherwise would quietly drop a real candidate.
    assert gaps.canonical("Asymptotic Notation") != gaps.canonical("Big O")


def test_a_stored_gap_is_corrected_when_a_query_proves_we_cover_it(tmp_path):
    """The settling pass must overrule what is already stored, or the 20 wrong
    verdicts already on disk stay in front of Aman. It must also not leave the
    candidate in the report twice with opposite answers."""
    from pipeline import staging
    from pipeline import llm as llm_mod

    con = staging.connect(tmp_path / "s.duckdb")
    con.execute("insert into topics (slug, domain, name, sort) values ('linked-list', 'dsa', 'Linked List', 1)")
    con.execute("""insert into roadmap_nodes (id, roadmap, domain, label, kind, sort) values
        ('n1', 'cs', 'cs', 'Linked List', 'topic', 1)""")
    con.execute("""insert into taxonomy_gaps (domain, label, verdict, covered_by, relevance, why)
        values ('cs', 'Linked List', 'gap', '', 0.9, 'core data structure')""")

    class NoLLM:
        models = {"smart": "x"}

        def complete_json(self, *a, **k):
            raise AssertionError("the model must not be asked about a topic we own")

    out = gaps.run(con, NoLLM())
    rows = [r for r in out if r["label"] == "Linked List"]
    assert len(rows) == 1, rows
    assert rows[0]["verdict"] == "covered" and rows[0]["covered_by"] == "Linked List"
    assert gaps.stored(con)[0]["verdict"] == "covered"
