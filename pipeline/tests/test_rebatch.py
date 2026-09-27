from pipeline.cards import rebatch


def test_dsa_patterns_fall_into_five_groups():
    assert rebatch.group_of("dsa", "sliding-window", None, 0, 0) == ("dsa-arrays", "DSA · Arrays, strings, windows")
    assert rebatch.group_of("dsa", "heap-priority-queue", None, 0, 0)[0] == "dsa-search"
    assert rebatch.group_of("dsa", "advanced-graphs", None, 0, 0)[0] == "dsa-graphs"
    assert rebatch.group_of("dsa", "2-d-dynamic-programming", None, 0, 0)[0] == "dsa-dp"
    assert rebatch.group_of("dsa", "segment-tree-fenwick", None, 0, 0)[0] == "dsa-math"
    assert rebatch.group_of("dsa", "some-new-pattern", None, 0, 0)[0] == "dsa-math"  # anything unknown lands in the catch-all


def test_design_splits_case_studies_and_core_halves():
    assert rebatch.group_of("system_design", "sd-design-a-url-shortener", "sd-design-case-studies", 50, 20)[0] == "sd-cases"
    assert rebatch.group_of("system_design", "sd-design-case-studies", None, 40, 20)[0] == "sd-cases"
    assert rebatch.group_of("system_design", "sd-caching", None, 5, 20)[0] == "sd-core-1"
    assert rebatch.group_of("system_design", "sd-consensus", None, 30, 20)[0] == "sd-core-2"


def test_cs_by_subject_and_single_batches_for_java_sql():
    assert rebatch.group_of("cs", "cs-deadlocks", None, 0, 0)[0] == "cs-os"
    assert rebatch.group_of("cs", "cs-dns", None, 0, 0)[0] == "cs-net"
    assert rebatch.group_of("cs", "cs-acid-properties", None, 0, 0)[0] == "cs-db"
    assert rebatch.group_of("cs", "cs-object-oriented-programming-principles", None, 0, 0)[0] == "cs-os"
    assert rebatch.group_of("java", "java-streams", None, 0, 0) == ("java", "Java")
    assert rebatch.group_of("sql", "sql-joins", None, 0, 0) == ("sql", "SQL")


def test_risk_is_the_lowest_reviewer_score_scaled():
    assert rebatch.risk_of('{"correct": 5, "clear": 4, "relevant": 5}') == 0.8
    assert rebatch.risk_of("{}") is None
    assert rebatch.risk_of(None) is None


def test_a_batch_pass_rate_counts_the_cards_the_gate_rejected(tmp_path):
    """Lesson cards the gate turned down are stored as `rejected`, not as a
    draft with kept = false. Grouping only drafts left nothing in the
    denominator that could fail, so every lesson batch reported a 100% pass
    rate on the admin screen no matter what the gate did."""
    from pipeline import staging

    con = staging.connect(tmp_path / "s.duckdb")
    con.execute("insert into topics (slug, domain, name, sort) values ('java-streams', 'java', 'Streams', 0)")
    for i, (kept, status) in enumerate([(True, "draft"), (True, "draft"), (True, "draft"), (False, "rejected")]):
        con.execute(
            """insert into cards (id, topic_slug, format, prompt_md, answer_md, kept, status, source)
               values (?, 'java-streams', 'typed', ?, 'a', ?, ?, 'lesson')""",
            [f"00000000-0000-4000-8000-00000000000{i}", f"q{i}", kept, status],
        )
    # A repaired row records the question as first written; its replacement is
    # already one of the drafts, so counting it too would punish the fix.
    con.execute(
        """insert into cards (id, topic_slug, format, prompt_md, answer_md, kept, status, source)
           values ('00000000-0000-4000-8000-0000000000ff', 'java-streams', 'typed', 'old wording', 'a', false, 'repaired', 'lesson')"""
    )
    group = rebatch.plan(con)["java"]
    assert group["generated"] == 4, group
    assert len(group["card_ids"]) == 3
    assert group["pass_rate"] == 0.75, group["pass_rate"]
