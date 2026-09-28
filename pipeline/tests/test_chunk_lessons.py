"""Lessons in the coach's index.

The coach used to retrieve only raw scraped chunks. Now that those are hidden
from readers, a coach quoting them would be quoting material we deliberately
stopped showing - and its citation would point at someone else's book rather
than the lesson we wrote.
"""

from pipeline import staging
from pipeline.chunk import run


def seeded(tmp_path):
    con = staging.connect(tmp_path / "s.duckdb")
    con.execute("insert into topics (slug, domain, name, sort) values ('sd-caching', 'system_design', 'Caching', 0)")
    con.execute(
        """insert into lessons (topic_slug, title, body_md, status)
           values ('sd-caching', 'Caching', ?, 'ok')""",
        ["A cache keeps hot data close to the reader. " * 30],
    )
    con.execute(
        """insert into lessons (topic_slug, title, body_md, status)
           values ('sd-held-back', 'Held back', 'Body that failed the fact check.', 'failed')"""
    )
    return con


def test_a_lesson_is_indexed_and_cites_its_own_page(tmp_path):
    con = seeded(tmp_path)
    run(con)
    rows = con.execute("select id, url, topic_slug, source_id from chunks where owner_kind = 'lesson'").fetchall()
    assert rows, "the lesson should be indexed"
    assert all(url.startswith("https://") and url.endswith("/library/topic/sd-caching") for _, url, _, _ in rows)
    assert all(source == "90x" for *_, source in rows)


def test_a_lesson_held_back_by_the_fact_checker_is_not_indexed(tmp_path):
    """It is unpublished for a reason; the coach must not quote it either."""
    con = seeded(tmp_path)
    run(con)
    held = con.execute("select count(*) from chunks where owner_id = 'sd-held-back'").fetchone()[0]
    assert held == 0
