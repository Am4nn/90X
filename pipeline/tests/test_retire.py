"""Which cards publish stands behind, and which it lets go.

Retirement deletes a published card that staging no longer has, and every
answer and review schedule cascades with it - so what counts as "has" is the
whole safety of the thing.
"""

from pipeline import publish, staging

A = "00000000-0000-4000-8000-00000000000a"
B = "00000000-0000-4000-8000-00000000000b"
C = "00000000-0000-4000-8000-00000000000c"
D = "00000000-0000-4000-8000-00000000000d"


def card(con, cid: str, kept, status: str) -> None:
    con.execute(
        """insert into cards (id, topic_slug, format, prompt_md, answer_md, kept, status, source)
           values (?, 'zz', 'typed', ?, 'a', ?, ?, 'lesson')""",
        [cid, f"question {cid[-1]}", kept, status],
    )


def test_a_rejected_card_is_not_something_staging_stands_behind(tmp_path):
    """A card that was published and is now rejected must be retirable.

    Its id is still in staging, carrying the gate's reason, so matching on
    presence left it live in the Feed - the gate's verdict reached the report
    and never reached the reader.
    """
    con = staging.connect(tmp_path / "s.duckdb")
    card(con, A, True, "draft")
    card(con, B, False, "rejected")
    card(con, C, False, "repaired")
    ids = publish.staged_card_ids(con)
    assert ids == [A], ids


def test_a_card_with_kept_unset_is_kept(tmp_path):
    """Older rows predate the column. Retiring one would delete a live card and
    its answers on the strength of a null, which is not a rejection."""
    con = staging.connect(tmp_path / "s.duckdb")
    card(con, D, None, "draft")
    assert publish.staged_card_ids(con) == [D]
