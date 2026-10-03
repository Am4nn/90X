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


def test_publish_retires_drafts_but_never_a_live_card(tmp_path):
    """The fix that made production step 3 possible at all.

    `_retire_superseded_cards` used to delete every published card staging no
    longer had. Regeneration removes a topic's old cards from staging, so
    publishing a regenerated corpus raised StudyHistoryAtRisk over the whole old
    corpus and rolled the entire transaction back.

    A live card is retired by the flip, not deleted here, and not even retired
    here: between publish and the flip the old corpus is the only thing live.

    Runs in a transaction that is rolled back. Does not cover the guard itself -
    that needs a card_reviews row, which needs a real user.
    """
    import psycopg

    from pipeline import config  # noqa: F401  loads pipeline/.env

    con = staging.connect(tmp_path / "s.duckdb")
    batch = "00000000-0000-4000-8000-0000000000ac"
    live_id = "00000000-0000-4000-8000-0000000000bd"
    draft_id = "00000000-0000-4000-8000-0000000000be"

    with psycopg.connect(os.environ["DATABASE_URL"], prepare_threshold=None) as pg:
        cur = pg.cursor()
        try:
            cur.execute(
                """insert into public.card_batches (id, domain, topic_slugs, ai_pass_rate, status)
                   values (%s, 'dsa', '{}', 0.9, 'draft')""",
                (batch,),
            )
            for card_id, status in ((live_id, "live"), (draft_id, "draft")):
                cur.execute(
                    """insert into public.cards
                       (id, batch_id, format, difficulty, prompt_md, answer_md, key_points, status)
                       values (%s, %s, 'typed', 'Easy', 'Which pattern?', 'Hashing', '[]', %s)""",
                    (card_id, batch, status),
                )

            # Staging is given every draft the target already holds except our own,
            # so the delete can only ever remove the one row this test created.
            # An empty staging would make it delete every unstaged draft in the
            # database, and this suite points at production by default.
            cur.execute("select id from public.cards where status = 'draft' and id <> %s", (draft_id,))
            for (keep,) in cur.fetchall():
                con.execute(
                    "insert into cards (id, format, prompt_md, answer_md, kept) values (?, 'typed', 'x', 'y', true)",
                    [str(keep)],
                )

            deleted = publish._retire_superseded_cards(con, cur, force=False)

            cur.execute("select status from public.cards where id = %s", (live_id,))
            row = cur.fetchone()
            assert row is not None, "publish deleted a live card"
            assert row[0] == "live", f"publish changed a live card's status to {row[0]!r}"

            cur.execute("select count(*) from public.cards where id = %s", (draft_id,))
            assert cur.fetchone()[0] == 0, "publish kept a draft card staging had dropped"
            assert deleted == 1, f"expected to delete only this test's draft, deleted {deleted}"
        finally:
            pg.rollback()


def test_republishing_a_card_updates_its_format_and_options_too(tmp_path):
    """A regenerated card that keeps its question keeps its id, so the upsert has
    to replace its whole content, not only its answer columns.

    The conflict clause used to write the new `picked`/`pairs`/`value` and keep
    the old `format` and `options`. A live card then rendered one primitive's
    interaction over another's answer definition - four stale options against a
    mapping answer - which no reader could answer. Rolled back.
    """
    import json

    import psycopg

    from pipeline import config  # noqa: F401  loads pipeline/.env

    con = tiny(tmp_path)
    # Same id (same topic, same prompt), different primitive and options.
    con.execute(
        """update cards set format = 'claim_grid', options = ?, answer_md = 'New answer',
                             pairs = ?, picked = null
           where id = '00000000-0000-4000-8000-0000000000bb'""",
        [json.dumps(["claim one", "claim two"]), json.dumps([[0, 1], [1, 0]])],
    )
    # `_publish_cards` publishes cards alone, so the FK targets have to be there.
    con.execute("update cards set problem_slug = null where problem_slug is not null")

    url = os.environ["DATABASE_URL"]
    with psycopg.connect(url, prepare_threshold=None) as pg:
        cur = pg.cursor()
        try:
            cur.execute(
                """insert into public.topics (slug, domain, name, sort)
                   values ('zz-test-topic', 'dsa', 'Test topic', 0)
                   on conflict (slug) do nothing"""
            )
            publish._publish_cards(con, cur)  # first publish: the row is created
            cur.execute(
                """update public.cards set format = 'pick_one', options = %s::jsonb, answer_md = 'Stale'
                   where id = '00000000-0000-4000-8000-0000000000bb'""",
                (json.dumps(["stale a", "stale b", "stale c", "stale d"]),),
            )
            publish._publish_cards(con, cur)  # second publish must converge it

            cur.execute(
                """select format, options, answer_md, pairs from public.cards
                   where id = '00000000-0000-4000-8000-0000000000bb'"""
            )
            fmt, options, answer, pairs = cur.fetchone()
            assert fmt == "claim_grid", f"format kept the stale value {fmt!r}"
            assert options == ["claim one", "claim two"], f"options kept the stale value {options!r}"
            assert answer == "New answer", f"answer_md kept the stale value {answer!r}"
            assert pairs == [[0, 1], [1, 0]], pairs
        finally:
            pg.rollback()


def test_publish_stamps_every_card_it_sends_with_one_timestamp(tmp_path):
    """`swap` activates only the newest `published_at`, so a publish has to stamp every
    card it sends with the *same* value: one card carrying a slightly older stamp than its
    neighbours would be left out of the activation. `now()` is the transaction's start,
    which is what makes one publish one stamp. Rolled back."""
    import psycopg

    from pipeline import config  # noqa: F401  loads pipeline/.env

    con = tiny(tmp_path)
    con.execute(
        """insert into cards (id, batch_id, topic_slug, problem_slug, format, difficulty, prompt_md, answer_md, key_points, kept)
           values ('00000000-0000-4000-8000-0000000000bc', '00000000-0000-4000-8000-0000000000aa', 'zz-test-topic',
                   'zz-test-problem', 'typed', 'Easy', 'A second question?', 'Another', '["a", "b"]', true)"""
    )
    con.execute("update cards set problem_slug = null where problem_slug is not null")

    with psycopg.connect(os.environ["DATABASE_URL"], prepare_threshold=None) as pg:
        cur = pg.cursor()
        try:
            cur.execute("""insert into public.topics (slug, domain, name, sort)
                           values ('zz-test-topic', 'dsa', 'Test topic', 0) on conflict (slug) do nothing""")
            publish._publish_cards(con, cur)
            cur.execute(
                """select count(*), count(distinct published_at), count(*) filter (where published_at = now())
                   from public.cards where id in ('00000000-0000-4000-8000-0000000000bb',
                                                  '00000000-0000-4000-8000-0000000000bc')"""
            )
            total, distinct, at_now = cur.fetchone()
            assert total == 2, total
            assert distinct == 1, f"one publish produced {distinct} different stamps"
            assert at_now == 2, "the stamp must be the transaction's now(), not NULL or a stale value"
        finally:
            pg.rollback()
