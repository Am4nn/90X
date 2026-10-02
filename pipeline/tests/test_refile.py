"""Re-filing a card the gate rejected for the wrong archetype.

The question is usually fine and only the label is wrong, so moving it recovers a
card the repair pass would have rewritten or lost. The move has to be bounded, and
these are the bounds.
"""

from dataclasses import dataclass

from pipeline.cards import archetypes, refile


@dataclass
class Card:
    prompt: str = "Which SOLID principle is violated?"
    archetype: str = "output-prediction"
    format: str = "pick_one"
    difficulty: str = "Medium"


def test_candidates_keep_the_cards_own_primitive():
    """The answer columns are shaped for the primitive: `picked` for chosen, `pairs`
    for mapping. Moving a card to an archetype with a different primitive would
    leave an answer definition nothing can grade."""
    card = Card(format="pick_one")
    for a in refile.candidates(card, "lld"):
        assert "pick_one" in a.primitives, f"{a.id} does not take pick_one"

    mapping = Card(format="match", archetype="term-meaning")
    for a in refile.candidates(mapping, "lld"):
        assert "match" in a.primitives, f"{a.id} does not take match"


def test_candidates_respect_area_and_difficulty():
    card = Card(format="pick_one", difficulty="Hard")
    for a in refile.candidates(card, "sql"):
        assert "sql" in a.areas, f"{a.id} is not eligible for sql"
        assert "Hard" in a.difficulties, f"{a.id} does not allow Hard"


def test_the_cards_current_archetype_is_never_a_candidate():
    card = Card(archetype="concept", format="pick_one")
    assert "concept" not in {a.id for a in refile.candidates(card, "java")}


def test_the_real_mismatch_can_reach_a_sensible_home():
    """The card that prompted all of this: a SOLID question filed under
    output-prediction. `which-principle-violated` is pick_one and eligible for lld,
    so the move is available without touching the answer columns."""
    ids = {a.id for a in refile.candidates(Card(), "lld")}
    assert "which-principle-violated" in ids


def test_an_invented_archetype_is_refused_rather_than_written():
    """The model picks from a list; an id outside it must not reach the database."""

    class FakeLLM:
        def complete_json(self, system, user, schema, tier="fast", purpose=""):
            return refile.Choice(archetype="not-a-real-archetype", reason="made up")

    options = refile.candidates(Card(), "lld")
    assert options, "the test needs candidates to choose from"
    assert refile.choose(FakeLLM(), Card(), options) is None


def test_a_refusal_is_honoured():
    class FakeLLM:
        def complete_json(self, system, user, schema, tier="fast", purpose=""):
            return refile.Choice(archetype=None, reason="nothing fits")

    assert refile.choose(FakeLLM(), Card(), refile.candidates(Card(), "lld")) is None


def test_no_candidates_means_no_model_call():
    class Exploding:
        def complete_json(self, *a, **k):
            raise AssertionError("should not be asked when there is nothing to choose from")

    assert refile.choose(Exploding(), Card(), []) is None


def test_every_candidate_offers_an_intent_to_choose_by():
    """The prompt is a list of ids and intents; a blank intent gives the model
    nothing to match the question against."""
    for a in refile.candidates(Card(), "lld"):
        assert a.intent, f"{a.id} has no intent"


def test_one_cards_provider_failure_does_not_discard_the_rest(tmp_path):
    """A model-client exception used to escape the loop before the write, so every
    move already chosen was lost and no later card was tried."""
    from pipeline import staging
    from pipeline.cards import refile as rf

    class Flaky:
        def __init__(self):
            self.calls = 0

        def complete_json(self, system, user, schema, tier="fast", purpose=""):
            self.calls += 1
            if self.calls == 1:
                raise RuntimeError("provider exploded")
            return rf.Choice(archetype=None, reason="nothing fits")

    con = staging.connect(tmp_path / "s.duckdb")
    con.execute("""insert into topics (slug, domain, name, sort)
                   values ('zz-t', 'lld', 'T', 0)""")
    for n in (1, 2):
        con.execute(
            """insert into cards (id, topic_slug, format, archetype, difficulty, prompt_md,
                   answer_md, status, kept, reject_reason, source)
               values (?, 'zz-t', 'pick_one', 'output-prediction', 'Medium', ?, 'a',
                   'rejected', false, 'wrong archetype: no', 'lesson')""",
            [f"id-{n}", f"Question {n}?"],
        )

    result = rf.run(con, llm=Flaky(), dry_run=True)
    assert result["failed"] == 1, result
    assert result["considered"] == 2, "the second card must still be tried"
    assert result["stopped_early"] is False, result


def test_a_budget_stop_is_reported_and_not_counted_as_considered(tmp_path):
    from pipeline import staging
    from pipeline.llm import BudgetExceeded
    from pipeline.cards import refile as rf

    class Broke:
        def complete_json(self, *a, **k):
            raise BudgetExceeded("cap reached")

    con = staging.connect(tmp_path / "s.duckdb")
    con.execute("""insert into topics (slug, domain, name, sort) values ('zz-t', 'lld', 'T', 0)""")
    con.execute(
        """insert into cards (id, topic_slug, format, archetype, difficulty, prompt_md,
               answer_md, status, kept, reject_reason, source)
           values ('id-1', 'zz-t', 'pick_one', 'output-prediction', 'Medium', 'Q?', 'a',
               'rejected', false, 'wrong archetype: no', 'lesson')"""
    )
    result = rf.run(con, llm=Broke(), dry_run=True)
    assert result["stopped_early"] is True, result
    assert result["considered"] == 0, "a card stopped on cannot count as considered"
    assert result["pending"] == 1, result


def test_a_move_records_where_the_card_came_from(tmp_path):
    """Setting reject_reason to null erased the only trace that a card had moved, so
    a follow-up gate could not be aimed at the cards that needed one and the whole
    corpus had to be re-judged - $6 rather than under $1, every run."""
    from pipeline import staging
    from pipeline.cards import refile as rf

    class Picks:
        def complete_json(self, system, user, schema, tier="fast", purpose=""):
            return rf.Choice(archetype="which-principle-violated", reason="it names a principle")

    con = staging.connect(tmp_path / "s.duckdb")
    con.execute("insert into topics (slug, domain, name, sort) values ('zz-t', 'lld', 'T', 0)")
    con.execute(
        """insert into cards (id, topic_slug, format, archetype, difficulty, prompt_md,
               answer_md, status, kept, reject_reason, source)
           values ('id-1', 'zz-t', 'pick_one', 'output-prediction', 'Medium',
               'Which SOLID principle is violated?', 'OCP', 'rejected', false,
               'wrong archetype: asks about principles', 'lesson')"""
    )

    result = rf.run(con, llm=Picks(), dry_run=False)
    assert result["moved"] == 1, result

    status, archetype, quality = con.execute(
        "select status, archetype, quality from cards where id = 'id-1'"
    ).fetchone()
    assert status == "draft", status
    assert archetype == "which-principle-violated", archetype
    assert "output-prediction" in (quality or ""), f"the old archetype was not recorded: {quality}"

    # And the topic is findable, which is the point of recording it.
    assert rf.refiled(con) == ["zz-t"]
