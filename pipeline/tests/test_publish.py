"""Integration test: publishes a tiny staging DB to the real Supabase inside a
transaction that is always rolled back (dry run). Skipped without DATABASE_URL."""

import os

import pytest

from pipeline import publish, staging

pytestmark = pytest.mark.skipif(not os.environ.get("DATABASE_URL"), reason="needs DATABASE_URL")


def tiny(tmp_path):
    con = staging.connect(tmp_path / "s.duckdb")
    con.execute("insert into topics (slug, domain, name, sort) values ('zz-test-topic', 'dsa', 'Test topic', 0)")
    con.execute("""insert into problems (slug, kind, title, difficulty, pattern_slug, topic_slugs, tags, techniques,
                   importance, premium, companies, statement_md, solutions, url, source_id)
                   values ('zz-test-problem', 'leetcode', 'Test', 'Easy', 'zz-test-topic', [], ['Array'], ['hash-map'],
                   0.5, false, '{"Amazon": 50}', 'statement', '{"python": "pass"}', 'https://x', 'leetcode-detailed')""")
    con.execute("""insert into documents (id, domain, title, body_md, source_id, sort)
                   values ('zz-doc', 'system_design', 'Doc', 'body', 'system-design-primer', 0)""")
    con.execute("""insert into card_batches (id, domain, topic_slugs, ai_pass_rate) values ('00000000-0000-4000-8000-0000000000aa', 'dsa', ['zz-test-topic'], 0.9)""")
    con.execute("""insert into cards (id, batch_id, topic_slug, problem_slug, format, difficulty, prompt_md, answer_md, key_points, kept)
                   values ('00000000-0000-4000-8000-0000000000bb', '00000000-0000-4000-8000-0000000000aa', 'zz-test-topic',
                   'zz-test-problem', 'typed', 'Easy', 'Which pattern?', 'Hashing', '["a", "b"]', true)""")
    return con


def test_dry_run_publishes_everything_then_rolls_back(tmp_path):
    from pipeline import config  # noqa: F401  loads pipeline/.env

    con = tiny(tmp_path)
    counts = publish.run(con, os.environ["DATABASE_URL"], dry_run=True)
    assert counts["problems"][0] == 1 and counts["documents"][0] == 1 and counts["cards"] == (1, 0)
    assert counts["sources"][0] >= 40
    # dry run: staging not marked published, Supabase unchanged
    assert con.execute("select published from card_batches").fetchone()[0] is False
    import psycopg
    with psycopg.connect(os.environ["DATABASE_URL"]) as pg:
        assert pg.execute("select count(*) from public.problems where slug = 'zz-test-problem'").fetchone()[0] == 0
