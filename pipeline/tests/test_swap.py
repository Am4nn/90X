"""`pipeline swap` must not resurrect a card the newest publish left out.

Runs against a LOCAL Postgres only (`TEST_DATABASE_URL`, e.g. the Supabase stack on
127.0.0.1), never `DATABASE_URL`: the swap updates every card in the covered areas, and
the other integration tests' habit of running against the real database inside a
rolled-back transaction is fine for an insert and not for this. Every test ends in a
rollback.

    TEST_DATABASE_URL=postgresql://postgres:postgres@127.0.0.1:64322/postgres uv run pytest tests/test_swap.py
"""

import os
import uuid
from datetime import datetime, timedelta, timezone

import pytest

URL = os.environ.get("TEST_DATABASE_URL")
pytestmark = pytest.mark.skipif(not URL, reason="needs TEST_DATABASE_URL (a local database, never production)")

psycopg = pytest.importorskip("psycopg")

T1 = datetime(2026, 10, 1, 12, 0, tzinfo=timezone.utc)
T2 = T1 + timedelta(days=2)


@pytest.fixture
def pg():
    assert URL and "supabase.co" not in URL and "pooler" not in URL, "refusing to run against a hosted database"
    conn = psycopg.connect(URL, prepare_threshold=None)
    try:
        yield conn
    finally:
        conn.rollback()
        conn.close()


def seed(pg, cards: dict[str, dict]) -> dict[str, str]:
    """Insert cards under one batch and one topic; returns name -> id."""
    topic, batch = f"zz-swap-{uuid.uuid4().hex[:6]}", str(uuid.uuid4())
    pg.execute("insert into public.topics (slug, domain, name, sort) values (%s, 'dsa', 'Swap test', 0)", (topic,))
    pg.execute("insert into public.card_batches (id, domain, topic_slugs, status) values (%s, 'dsa', %s, 'published')",
               (batch, [topic]))
    ids = {}
    for name, c in cards.items():
        ids[name] = str(uuid.uuid4())
        pg.execute(
            """insert into public.cards (id, batch_id, topic_slug, format, difficulty, prompt_md, answer_md,
                      archetype, status, published_at)
               values (%s, %s, %s, 'pick_one', 'Easy', %s, 'a', %s, %s, %s)""",
            (ids[name], batch, topic, f"question {name}", c.get("archetype", "concept"), c["status"], c.get("stamp")),
        )
    return ids


def statuses(pg, ids: dict[str, str]) -> dict[str, str]:
    rows = pg.execute("select id::text, status from public.cards where id = any(%s::uuid[])", (list(ids.values()),)).fetchall()
    by_id = dict(rows)
    return {name: by_id[i] for name, i in ids.items()}


def test_a_card_retired_on_purpose_stays_retired_when_the_newest_publish_omits_it():
    """The bug: swap activated `status in (draft, live, retired)` for every archetyped
    card, so a card retired because the refile check found it did not fit, or because the
    key audit found it contradicting its explanation, went straight back in front of
    readers. Found by a dry run offering 3,812 activations when production held 40 drafts.
    """
    from pipeline.cards import swap

    conn = psycopg.connect(URL, prepare_threshold=None)
    try:
        ids = seed(conn, {
            "sent_again":      {"status": "draft",   "stamp": T2},   # in the newest publish
            "regenerated":     {"status": "retired", "stamp": T2},   # same id, sent again: must come back
            "retired_earlier": {"status": "retired", "stamp": T1},   # an older publish: leave it
            "never_stamped":   {"status": "retired", "stamp": None},  # predates the column: leave it
            "went_stale":      {"status": "live",    "stamp": T1},   # live but no longer sent: retire it
            "legacy":          {"status": "draft",   "stamp": T2, "archetype": None},  # no archetype: never
        })
        # Nothing else in this database may be newer than T2.
        conn.execute("update public.cards set published_at = null where published_at > %s", (T2,))

        swap.flip(conn, dry_run=False)

        assert statuses(conn, ids) == {
            "sent_again": "live",
            "regenerated": "live",
            "retired_earlier": "retired",
            "never_stamped": "retired",
            "went_stale": "retired",
            "legacy": "draft",
        }
    finally:
        conn.rollback()
        conn.close()


def test_the_dry_run_reports_what_the_stamp_is_keeping_out(pg):
    from pipeline.cards import swap

    ids = seed(pg, {
        "sent_again": {"status": "draft", "stamp": T2},
        "retired_earlier": {"status": "retired", "stamp": T1},
    })
    pg.execute("update public.cards set published_at = null where published_at > %s", (T2,))
    before = swap.flip(pg, dry_run=True)
    assert before["newest_publish"] == T2.isoformat()
    assert before["left_retired_not_in_newest_publish"] >= 1
    assert statuses(pg, ids) == {"sent_again": "draft", "retired_earlier": "retired"}, "a dry run must change nothing"


def test_swap_refuses_when_nothing_has_been_published_with_a_stamp(pg):
    """With no stamp there is no 'current corpus', and the old behaviour would have
    activated everything archetyped. Refuse instead."""
    from pipeline.cards import swap

    seed(pg, {"a": {"status": "draft", "stamp": None}})
    pg.execute("update public.cards set published_at = null")
    with pytest.raises(swap.SwapRefused):
        swap.flip(pg, dry_run=False)
    # The dry run still reports, so you can see why.
    assert swap.flip(pg, dry_run=True)["newest_publish"] is None
