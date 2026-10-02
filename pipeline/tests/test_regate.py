"""The combined gate pass: answerability + guessability reject on either."""

from dataclasses import dataclass

from pipeline.cards.regate import merge_rejects


@dataclass
class Card:
    prompt: str


def test_a_card_only_the_blind_gate_rejected_is_still_rejected():
    card = Card("which structure?")
    out = merge_rejects([], [(card, "guessable by elimination: 2/3 samples flagged it")])
    assert out == [(card, "guessable by elimination: 2/3 samples flagged it")]


def test_the_answerability_reason_wins_when_both_gates_reject():
    card = Card("which structure?")
    out = merge_rejects([(card, "the marked answer is wrong")], [(card, "guessable")])
    assert len(out) == 1
    assert out[0][1] == "the marked answer is wrong"


def test_value_equal_but_distinct_cards_are_not_deduped():
    # The two gates share the same card objects from `cards_of`, so deduping is
    # by identity, not by value. Two cards that merely read alike are distinct.
    a, b = Card("same prompt"), Card("same prompt")
    out = merge_rejects([(a, "wrong")], [(b, "guessable")])
    assert len(out) == 2
    assert out[0][0] is a and out[1][0] is b


def test_no_blind_holds_a_rewrite_to_the_same_bar_as_the_card_it_replaces(monkeypatch):
    """`--no-blind` skipped the guessability gate for the stored cards but ran it on
    every replacement, so a rewrite had to clear a gate the original was never tested
    against. Eight topics in a row reported "0 rewritten" and the rewrite pass - the
    most expensive call in the run, because it sends the whole lesson - bought
    nothing. With blind=False the blind gate must not be consulted at all.
    """
    from pipeline.cards import blind_gate, regate

    topic = {"slug": "trees", "lesson": "a lesson", "importance": 1}
    bad, good = Card("refers to the lesson"), Card("a self-contained question")

    monkeypatch.setattr(regate, "topics_with_cards", lambda con, only=None: [topic])
    monkeypatch.setattr(regate, "cards_of", lambda con, slug: [bad])
    monkeypatch.setattr(regate, "rewrite", lambda llm, t, lesson, rejected, tier="smart": [good])
    monkeypatch.setattr(regate, "spend_usd", lambda con, run_id=None: 0.0)
    monkeypatch.setattr(regate, "apply", lambda con, cards, rejected, confidence: (0, len(rejected)))
    monkeypatch.setattr(regate.gate, "review", lambda llm, t, cards, tier="smart": object())
    monkeypatch.setattr(regate.gate, "confidence_by_card", lambda cards, result: {})
    # The replacement passes answerability; the original does not.
    monkeypatch.setattr(regate.gate, "judge",
                        lambda cards, result: [(c, "refers to unseen material") for c in cards if c is bad])

    def forbidden(*a, **kw):
        raise AssertionError("the blind gate ran under --no-blind")

    monkeypatch.setattr(blind_gate, "review", forbidden)

    stored: list = []
    monkeypatch.setattr(regate, "store_fix",
                        lambda con, t, old, card, confidence: stored.append((old, card)) or True)

    totals = regate.run(object(), tier="smart", llm=object(), blind=False)

    assert stored == [(bad, good)], stored
    assert totals["reformatted"] == 1 and totals["rejected"] == 0, totals


def test_a_second_repair_of_the_same_card_does_not_collide(tmp_path):
    """The crash that killed the corrected pass at topic 100 of 274, with every topic
    before it already paid for. `card_id` hashes the question, so it is stable by
    design - and the re-key is an UPDATE, so the second repair of a card computes the
    `repaired:` id the first repair already took and violates the primary key.
    """
    import duckdb

    from pipeline.cards.regate import _free_id
    from pipeline.cards.run_lessons import card_id

    con = duckdb.connect(str(tmp_path / "t.duckdb"))
    con.execute("create table cards (id varchar primary key, note varchar)")

    taken = card_id("trees", "what does it print?", "repaired:abc")
    con.execute("insert into cards values (?, 'the first repair')", [taken])

    # A second repair of the same question must land somewhere else.
    second = _free_id(con, "trees", "what does it print?", "repaired:abc")
    assert second != taken
    con.execute("insert into cards values (?, 'the second repair')", [second])
    assert con.execute("select count(*) from cards").fetchone()[0] == 2

    # And the row being re-keyed may hold the id itself: that is not a collision.
    con.execute("insert into cards values ('live-row', 'being re-keyed')")
    mine = card_id("trees", "a question of its own", "repaired:live-row")
    con.execute("update cards set id = ? where id = 'live-row'", [mine])
    assert _free_id(con, "trees", "a question of its own", "repaired:live-row", keep=mine) == mine
