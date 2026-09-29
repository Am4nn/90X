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
    con.execute("""insert into lessons (topic_slug, title, body_md, practice, source_refs, words, status)
                   values ('zz-test-topic', 'Test topic', 'A lesson body. It stands alone.',
                   '{"problems": [], "questions": []}', '[]', 42, 'ok')""")
    con.execute("""insert into roadmap_nodes (id, roadmap, domain, label, kind, sort, topic_slug)
                   values ('zz-rm:node1', 'zz-rm', 'dsa', 'Test node', 'topic', 0, 'zz-test-topic')""")
    con.execute("""insert into card_batches (id, domain, topic_slugs, ai_pass_rate) values ('00000000-0000-4000-8000-0000000000aa', 'dsa', ['zz-test-topic'], 0.9)""")
    con.execute("""insert into cards (id, batch_id, topic_slug, problem_slug, format, difficulty, prompt_md, answer_md, key_points, kept)
                   values ('00000000-0000-4000-8000-0000000000bb', '00000000-0000-4000-8000-0000000000aa', 'zz-test-topic',
                   'zz-test-problem', 'typed', 'Easy', 'Which pattern?', 'Hashing', '["a", "b"]', true)""")
    return con


def test_dry_run_publishes_everything_then_rolls_back(tmp_path):
    from pipeline import config  # noqa: F401  loads pipeline/.env

    con = tiny(tmp_path)
    counts = publish.run(con, os.environ["DATABASE_URL"], dry_run=True)
    assert counts["problems"][0] == 1 and counts["cards"] == (1, 0)
    # The lesson layer and the roadmap checklist publish alongside everything else.
    assert counts["lessons"][0] == 1 and counts["roadmap_nodes"][0] == 1
    assert counts["sources"][0] >= 40
    # dry run: Supabase unchanged
    import psycopg
    with psycopg.connect(os.environ["DATABASE_URL"]) as pg:
        assert pg.execute("select count(*) from public.problems where slug = 'zz-test-problem'").fetchone()[0] == 0


def test_a_coach_written_lesson_survives_publish(tmp_path):
    """Publishing converges: whatever staging no longer has is deleted. A lesson
    the Coach wrote on demand was never in staging, so to that delete it looks
    like an orphan - and without the written_by guard the next publish would
    quietly remove a lesson the user is reading.

    The coach lesson is planted on a *second* staging topic that has no staging
    lesson of its own. It has to be a topic staging knows about, because publish
    converges `topics` too and `lessons.topic_slug` cascades on delete - the
    first version of this test failed for that reason rather than the guard.

    Runs inside a transaction that is always rolled back.
    """
    from pipeline import config  # noqa: F401  loads pipeline/.env

    import psycopg

    con = tiny(tmp_path)
    # A topic staging has and has no lesson for: exactly where a coach lesson lives.
    con.execute("insert into topics (slug, domain, name, sort) values ('zz-coach-topic', 'dsa', 'Coach topic', 1)")
    url = os.environ["DATABASE_URL"]
    with psycopg.connect(url) as probe:
        owner = probe.execute("select id from auth.users limit 1").fetchone()
    if not owner:
        pytest.skip("no auth.users row to own a coach-written lesson")

    with psycopg.connect(url) as pg:
        with pg.transaction(force_rollback=True):
            cur = pg.cursor()
            # The topic has to exist before its lesson; publish's own upsert
            # would create it, but the lesson is planted first on purpose.
            cur.execute("insert into public.topics (slug, domain, name, sort) values "
                        "('zz-coach-topic', 'dsa', 'Coach topic', 1) on conflict (slug) do nothing")
            cur.execute("insert into public.lessons (topic_slug, title, body_md, written_by) "
                        "values ('zz-coach-topic', 'Coach wrote this', 'Body.', %s)", (owner[0],))
            publish.publish(con, pg, dry_run=False)
            coach_lesson = cur.execute(
                "select count(*) from public.lessons where topic_slug = 'zz-coach-topic' and written_by is not null"
            ).fetchone()[0]
            pipeline_lesson = cur.execute(
                "select count(*) from public.lessons where topic_slug = 'zz-test-topic' and written_by is null"
            ).fetchone()[0]

    assert coach_lesson == 1, "publish deleted a lesson the Coach wrote"
    # And the pipeline's own lesson still publishes in the same run.
    assert pipeline_lesson == 1


def test_publishing_over_a_coach_lesson_takes_ownership_back(tmp_path):
    """The Coach can write a lesson for a topic whose staging lesson exists but
    has not been published yet - nothing in public.lessons, so it does not
    refuse. The next publish then replaces the text, and without reclaiming
    written_by the pipeline's own words would be credited to a user and exempt
    from every future delete."""
    from pipeline import config  # noqa: F401  loads pipeline/.env

    import psycopg

    con = tiny(tmp_path)
    url = os.environ["DATABASE_URL"]
    with psycopg.connect(url) as probe:
        owner = probe.execute("select id from auth.users limit 1").fetchone()
    if not owner:
        pytest.skip("no auth.users row to own a coach-written lesson")

    with psycopg.connect(url) as pg:
        with pg.transaction(force_rollback=True):
            cur = pg.cursor()
            # Same topic staging has an 'ok' lesson for.
            cur.execute("insert into public.topics (slug, domain, name, sort) values "
                        "('zz-test-topic', 'dsa', 'Test topic', 0) on conflict (slug) do nothing")
            cur.execute("insert into public.lessons (topic_slug, title, body_md, written_by) "
                        "values ('zz-test-topic', 'Coach got here first', 'Coach body.', %s) "
                        "on conflict (topic_slug) do update set written_by = excluded.written_by, "
                        "title = excluded.title, body_md = excluded.body_md", (owner[0],))
            publish.publish(con, pg, dry_run=False)
            title, written_by = cur.execute(
                "select title, written_by from public.lessons where topic_slug = 'zz-test-topic'"
            ).fetchone()

    assert title == "Test topic", "publish did not overwrite the coach's text"
    assert written_by is None, "publish kept written_by, so its own lesson is credited to a user"


def test_dropping_a_topic_does_not_cascade_away_a_coach_lesson(tmp_path):
    """lessons.topic_slug is `on delete cascade`, so a taxonomy refresh that
    drops a topic would take its Coach-written lesson with it and the lessons
    exemption would never get a say. Keeping a stale taxonomy row is visible and
    recoverable; deleting somebody's lesson silently is not."""
    from pipeline import config  # noqa: F401  loads pipeline/.env

    import psycopg

    con = tiny(tmp_path)  # staging does NOT contain zz-orphan-topic
    url = os.environ["DATABASE_URL"]
    with psycopg.connect(url) as probe:
        owner = probe.execute("select id from auth.users limit 1").fetchone()
    if not owner:
        pytest.skip("no auth.users row to own a coach-written lesson")

    with psycopg.connect(url) as pg:
        with pg.transaction(force_rollback=True):
            cur = pg.cursor()
            cur.execute("insert into public.topics (slug, domain, name, sort) values "
                        "('zz-orphan-topic', 'dsa', 'Dropped topic', 99)")
            cur.execute("insert into public.lessons (topic_slug, title, body_md, written_by) "
                        "values ('zz-orphan-topic', 'Coach wrote this', 'Body.', %s)", (owner[0],))
            publish.publish(con, pg, dry_run=False)
            topic = cur.execute("select count(*) from public.topics where slug = 'zz-orphan-topic'").fetchone()[0]
            lesson = cur.execute("select count(*) from public.lessons where topic_slug = 'zz-orphan-topic'").fetchone()[0]

    assert lesson == 1, "the topic delete cascaded away a coach-written lesson"
    assert topic == 1, "the topic has to survive for its lesson to be reachable"
