"""The review sample: two cards per archetype, grouped, not shuffled."""

import json

from pipeline import staging
from pipeline.cards import review_pack


def _seed(con):
    con.execute("insert into topics (slug, domain, name) values ('t', 'dsa', 'Topic')")
    con.execute("insert into lessons (topic_slug, title, body_md) values ('t', 'L', 'body')")


def _card(con, cid, archetype, confidence, format="pick_one"):
    con.execute(
        """insert into cards (id, topic_slug, format, prompt_md, answer_md, kept, status, source,
                              archetype, quality, picked)
           values (?, 't', ?, ?, 'a', true, 'draft', 'lesson', ?, ?, ?)""",
        [cid, format, f"prompt {cid}", archetype, json.dumps({"gate_confidence": confidence}), json.dumps([0])],
    )


def test_sample_takes_two_least_confident_per_archetype_grouped(tmp_path):
    con = staging.connect(tmp_path / "s.duckdb")
    _seed(con)
    _card(con, "00000000-0000-4000-8000-000000000001", "concept", 0.9)
    _card(con, "00000000-0000-4000-8000-000000000002", "concept", 0.3)
    _card(con, "00000000-0000-4000-8000-000000000003", "concept", 0.6)
    _card(con, "00000000-0000-4000-8000-000000000004", "flash", 0.5)

    picked = review_pack.sample(con)

    # Grouped by archetype in registry order (concept before flash), and within
    # an archetype the two least-confident cards come first.
    assert [c["archetype"] for c in picked] == ["concept", "concept", "flash"]
    assert [c["id"] for c in picked] == [
        "00000000-0000-4000-8000-000000000002",
        "00000000-0000-4000-8000-000000000003",
        "00000000-0000-4000-8000-000000000004",
    ]
    assert picked[0]["archetype_label"] == "Concept"


def test_sample_caps_at_two_even_with_many_cards(tmp_path):
    con = staging.connect(tmp_path / "s.duckdb")
    _seed(con)
    for n in range(5):
        _card(con, f"00000000-0000-4000-8000-{n:012d}", "concept", 0.1 * n)

    picked = review_pack.sample(con)
    assert [c["archetype"] for c in picked] == ["concept", "concept"]


def test_report_groups_by_archetype_and_shows_answer(tmp_path):
    con = staging.connect(tmp_path / "s.duckdb")
    _seed(con)
    _card(con, "00000000-0000-4000-8000-000000000001", "concept", 0.5)
    _card(con, "00000000-0000-4000-8000-000000000002", "flash", 0.5, format="self_rate")

    out = review_pack.report(con)

    # One archetype heading per group, and the answer definition is shown.
    assert "## Concept (`concept` · pick_one)" in out
    assert "## Flash (`flash` · self_rate)" in out
    assert "**Answer (the reader is graded on)**" in out
