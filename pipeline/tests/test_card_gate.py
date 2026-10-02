"""The card gate. Every case is a draft the first card pass actually shipped."""

from dataclasses import dataclass, field

from pipeline.cards.gate import GateResult, Verdict, judge, prompt_only


@dataclass
class FakeCard:
    prompt: str
    answer: str = "an answer"
    format: str = "typed"
    options: list[str] = field(default_factory=list)


def ruled(**kw):
    """A Verdict with the three nullable fields stated.

    `fits_archetype`, `premise_holds` and `one_answer` are required and have no
    default, so that a model reply which leaves one out is a schema violation and
    gets retried rather than being read as a rejection. Tests that predate those
    fields mean "the model ruled, and said fine"; this says it once.
    """
    return Verdict(**{"fits_archetype": True, "premise_holds": True, "one_answer": True, **kw})


def gate(cards, verdicts):
    return judge(cards, GateResult(verdicts=verdicts))


def test_rejects_a_card_that_needs_the_source():
    """The card Aman found: it quotes a solution the reader never sees."""
    card = FakeCard("In the reference solution, after removing the run starting at x up to y-1, "
                    "it sets d[x] = d[y] + y - x. What invariant makes this correct?")
    rejected = gate([card], [ruled(index=0)])
    assert len(rejected) == 1
    assert "unseen material" in rejected[0][1], rejected
    assert "reference solution" in rejected[0][1]


def test_rejects_what_the_reviewer_calls_unanswerable():
    card = FakeCard("What does the diagram show?")
    rejected = gate([card], [ruled(index=0, answerable=False, reason="no diagram is present")])
    assert rejected[0][1].startswith("not answerable")


def test_rejects_a_typed_card_that_should_be_multiple_choice():
    """Aman's second example: the honest answer is a list to enumerate."""
    card = FakeCard("Along which dimensions can content negotiation vary the representation of a resource?")
    rejected = gate([card], [ruled(index=0, fits_format=False, reason="the answer is a list")])
    assert rejected[0][1].startswith("wrong_format")


def test_keeps_a_fair_card():
    card = FakeCard("Why does a sliding window run in O(n) even with a nested loop?")
    assert gate([card], [ruled(index=0)]) == []


def test_mcq_where_a_competent_answer_disagrees_is_rejected():
    card = FakeCard("Which is true of TCP?", answer="It is connection-oriented", format="mcq",
                    options=["It is connectionless", "It is connection-oriented",
                             "It never retransmits", "It has no ordering guarantee"])
    rejected = gate([card], [ruled(index=0, picked="It is connectionless")])
    assert "disagrees with the marked option" in rejected[0][1]


def test_mcq_agreement_is_kept():
    card = FakeCard("Which is true of TCP?", answer="It is connection-oriented", format="mcq",
                    options=["It is connectionless", "It is connection-oriented",
                             "It never retransmits", "It has no ordering guarantee"])
    assert gate([card], [ruled(index=0, picked=" It is connection-oriented ")]) == []


def test_a_card_the_reviewer_never_ruled_on_is_rejected():
    """Keeping it meant a truncated reply silently passed questions nobody
    checked. Rejected is not deleted: it goes through the repair pass and is
    gated again, so an omission costs a retry rather than a card."""
    cards = [FakeCard("Why is TCP reliable?"), FakeCard("Why is UDP fast?")]
    rejected = gate(cards, [ruled(index=0)])
    assert len(rejected) == 1
    assert rejected[0][0].prompt == "Why is UDP fast?"
    assert "did not rule" in rejected[0][1]


def test_the_gate_never_sees_the_answer():
    card = FakeCard("Why is a hash map O(1) on average?", answer="SECRET-REFERENCE-ANSWER")
    shown = prompt_only(card)
    assert "SECRET-REFERENCE-ANSWER" not in shown
    assert "Why is a hash map O(1) on average?" in shown


def test_mcq_options_are_shown_but_not_which_is_right():
    card = FakeCard("Which is true?", answer="B", format="mcq", options=["A", "B"])
    shown = prompt_only(card)
    assert "A" in shown and "B" in shown
    assert "answer" not in shown.lower()


def test_card_budget_follows_importance():
    from pipeline.cards import archetypes

    assert archetypes.count_for(0.5) == 10
    assert archetypes.count_for(0.8) == 16
    assert archetypes.count_for(1.0) == 20


def test_risk_column_holds_confidence_not_risk():
    """pickReviewSample sorts ascending and reviews the first half, so a LOW
    value is what gets looked at. Inverting the gate's confidence would put
    the cards it liked most in front of the reviewer."""
    from pipeline.cards.rebatch import risk_of

    doubtful = risk_of('{"gate_confidence": 0.3}')
    confident = risk_of('{"gate_confidence": 0.95}')
    assert doubtful < confident, "the doubtful card must sort first"
    assert confident == 0.95

    # Chunk-generated cards keep the old scale: lowest of three 0-5 scores.
    assert risk_of('{"correct": 2, "clear": 5, "relevant": 5}') == 0.4
    assert risk_of(None) is None


def test_lesson_card_ids_are_stable_uuids():
    """public.cards.id is a uuid, so a readable "slug:l0" id never publishes.
    uuid5 keeps regeneration idempotent instead of duplicating every card."""
    import uuid

    from pipeline.cards.run_lessons import CARD_NAMESPACE

    first = uuid.uuid5(CARD_NAMESPACE, "sliding-window:0")
    assert first == uuid.uuid5(CARD_NAMESPACE, "sliding-window:0")
    assert first != uuid.uuid5(CARD_NAMESPACE, "sliding-window:1")
    assert first != uuid.uuid5(CARD_NAMESPACE, "two-pointers:0")
    uuid.UUID(str(first))  # parses as a uuid, which Postgres requires


def test_one_malformed_card_does_not_cost_the_whole_topic():
    """A multiple-choice card with three options used to fail the whole set,
    losing eleven good cards and the topic with it."""
    from pipeline.cards.from_lessons import CardSet

    good = {
        "format": "typed",
        "prompt": "Why does a hash map give O(1) average lookup?",
        "answer": "Keys spread across buckets, so each holds a constant number.",
        "key_points": ["hashing spreads keys", "buckets stay short"],
        "difficulty": "Easy",
    }
    malformed = {**good, "format": "mcq", "answer": "not one of the options", "options": ["x", "y", "z"]}
    kept = CardSet.model_validate({"cards": [good, malformed, good, good]}).cards
    assert len(kept) == 3
    assert all(c.format == "typed" for c in kept)


def test_a_set_of_only_malformed_cards_still_fails():
    import pytest
    from pydantic import ValidationError

    from pipeline.cards.from_lessons import CardSet

    junk = {"format": "mcq", "prompt": "Which?", "answer": "nope", "key_points": ["a", "b"],
            "difficulty": "Easy", "options": ["x"]}
    with pytest.raises(ValidationError):
        CardSet.model_validate({"cards": [junk, junk, junk]})


def test_a_card_id_follows_its_question_not_its_position():
    """Keying on position meant the gate changing its mind about one card
    moved every later card's id, so published study history could attach to a
    different question."""
    from pipeline.cards.run_lessons import card_id

    first = card_id("sliding-window", "Why is it O(n) despite the nested loop?")
    assert first == card_id("sliding-window", "Why is it O(n) despite the nested loop?")
    # Reflowed whitespace is the same question.
    assert first == card_id("sliding-window", "  Why is it O(n)   despite the nested loop?\n")
    assert first != card_id("sliding-window", "When does the technique stop working?")
    assert first != card_id("two-pointers", "Why is it O(n) despite the nested loop?")


def test_the_gate_cannot_reject_a_card_for_having_a_valid_format():
    """The real rejection, from the published review pack:

        wrong_format: Format 'output' is not one of the allowed card formats
        (flash, typed, mcq).

    69 output cards were live at the time. The prompt documents `output` and
    the Card enum allows it - the reviewing model invented the restriction. A
    format from our own enum is legal by construction, so an objection that
    only says otherwise is not an objection.
    """
    card = FakeCard("What is the exact output?\n```python\nprint(sorted({3,1,2}))\n```",
                    answer="[1, 2, 3]", format="output")
    verdict = ruled(index=0, fits_format=False,
                      reason="Format 'output' is not one of the allowed card formats (flash, typed, mcq).")
    assert gate([card], [verdict]) == []


def test_a_real_format_objection_still_rejects():
    """The guard must not swallow the objection it was built to allow."""
    card = FakeCard("What is the exact output?\n```python\nprint(time.time())\n```",
                    answer="1759000000.0", format="output")
    rejected = gate([card], [ruled(index=0, fits_format=False,
                                     reason="the snippet prints a timestamp, so the output changes")])
    assert "wrong_format" in rejected[0][1]


def test_an_answerable_card_in_the_wrong_format_reports_the_format():
    """The stages are separate so both can be true at once. Collapsing them
    into one enum meant the reviewer had to choose, and the repair pass was
    told whichever it happened to pick."""
    card = FakeCard("Name the four transaction isolation levels.")
    rejected = gate([card], [ruled(index=0, answerable=True, fits_format=False,
                                     reason="the honest answer is a list to enumerate")])
    assert rejected[0][1].startswith("wrong_format")


def test_the_earliest_failure_is_the_one_reported():
    """A card that needs unseen material is a worse card than one in the wrong
    format, and the repair pass should be told the more fundamental thing."""
    card = FakeCard("In the reference solution, name the four isolation levels.")
    rejected = gate([card], [ruled(index=0, answerable=False, fits_format=False,
                                     reason="the answer is a list")])
    assert "unseen material" in rejected[0][1]


def test_a_structurally_broken_card_is_caught_without_the_model():
    card = FakeCard("Which isolation level?", answer="Serializable", format="mcq",
                    options=["Read committed", "Serializable"])
    rejected = gate([card], [ruled(index=0)])
    assert "malformed" in rejected[0][1] and "4 options" in rejected[0][1]


def test_an_output_card_must_show_its_snippet():
    card = FakeCard("What does the loop print?", answer="3", format="output")
    rejected = gate([card], [ruled(index=0)])
    assert "must show the snippet" in rejected[0][1]


def test_confidence_is_keyed_by_card_not_by_position():
    """The gate returns verdicts keyed by position; a caller holding cards has
    to join the two. Leaving that to callers cost every one of 2,804 cards its
    score: the re-gate looked up `id(card)` in a position-keyed map, missed
    every time, and stored the 0.5 fallback into the column the review screen
    sorts on."""
    from pipeline.cards.gate import confidence_by_card

    cards = [FakeCard("a"), FakeCard("b"), FakeCard("c")]
    result = GateResult(verdicts=[ruled(index=0, confidence=0.2), ruled(index=2, confidence=0.9)])
    scores = confidence_by_card(cards, result)
    assert scores[id(cards[0])] == 0.2
    assert scores[id(cards[2])] == 0.9
    # Never ruled on: the fallback, but only for that card.
    assert scores[id(cards[1])] == 0.5


def test_a_gradability_objection_is_never_suppressed():
    """The format-denial guard used to cover the gradable verdict too, so an
    ungradable card stayed publishable whenever the reason mentioned formats."""
    card = FakeCard("What is the exact output?\n```sql\nselect 1;\n```", answer="1", format="output")
    rejected = gate([card], [ruled(index=0, gradable=False,
                                     reason="no standard plaintext format is valid for a SQL result set")])
    assert "not gradable" in rejected[0][1]


def test_a_real_format_objection_that_mentions_validity_still_rejects():
    """"this format is not valid for exact-match grading" is a genuine
    objection. A looser denial pattern swallowed it."""
    card = FakeCard("What is printed?\n```python\nprint(hash('a'))\n```", answer="x", format="output")
    rejected = gate([card], [ruled(index=0, fits_format=False,
                                     reason="this format is not valid for exact-match grading here")])
    assert "wrong_format" in rejected[0][1]


def test_an_objection_names_one_card_or_none():
    """Taking the topic's first card is what broke the first review round: a
    topic has around ten cards and the sample shows one, so twelve of thirteen
    objections rewrote a card nobody had complained about and left the offending
    one publishable. Refusing is better than guessing."""
    from pipeline.cards.fix import pick

    class Row:
        def __init__(self, prompt):
            self.prompt = prompt

    cards = [Row("What is the core idea behind reducing ambiguity?"),
             Row("At the senior level, what scope of people should the story involve?"),
             Row("How does handling ambiguity change at staff level?")]
    assert pick(cards, "At the senior level").prompt.startswith("At the senior")
    # Whitespace and case are not part of the identity.
    assert pick(cards, "  at the SENIOR   level ").prompt.startswith("At the senior")
    # Ambiguous or absent: refuse rather than pick the first.
    assert pick(cards, "ambiguity") is None
    assert pick(cards, "not in any card") is None
    assert pick(cards, "") is None
    # A topic with exactly one card needs no match line.
    assert pick(cards[:1], "") is cards[0]


def test_an_objection_block_parses_its_match_line(tmp_path):
    from pipeline.cards.fix import objections

    path = tmp_path / "obj.md"
    path.write_text(
        "# Card objections\n\n"
        "## beh-dealing-with-ambiguity\n\n"
        "match: At the senior level\n\n"
        "The levelling ladder is not a universal truth.\n",
        encoding="utf-8",
    )
    found = objections(path)
    item = found["beh-dealing-with-ambiguity|At the senior level"]
    assert item.slug == "beh-dealing-with-ambiguity"
    assert item.match == "At the senior level"
    assert "levelling ladder" in item.text
    assert "match:" not in item.text, "the directive must not reach the rewrite prompt"


def test_a_failed_fix_is_not_reported_as_applied(tmp_path):
    """A replacement that fails re-gating is stored as `rejected` and can still
    carry the objection's fragment. Counting rejected rows as evidence reported
    a failed fix as applied, and a later run would skip it for good."""
    from pipeline import staging
    from pipeline.cards.fix import superseded

    con = staging.connect(tmp_path / "s.duckdb")
    con.execute("""insert into cards (id, topic_slug, format, prompt_md, answer_md, kept, status, source)
        values ('00000000-0000-4000-8000-00000000000a', 'sd-jwt', 'typed',
                'When a server verifies a JWT, what should it check?', 'a', false, 'rejected', 'lesson')""")
    assert superseded(con, "sd-jwt", "When a server verifies a JWT") is False
    con.execute("""insert into cards (id, topic_slug, format, prompt_md, answer_md, kept, status, source)
        values ('00000000-0000-4000-8000-00000000000b', 'sd-jwt', 'typed',
                'When a server verifies a JWT, what should it check?', 'a', false, 'repaired', 'lesson')""")
    assert superseded(con, "sd-jwt", "When a server verifies a JWT") is True


def test_the_printed_selector_matches_the_way_pick_matches(tmp_path):
    """The report printed a fragment tested with a case-sensitive prefix match
    while `pick` looks for it anywhere, ignoring case - so a selector the report
    called unique could still be ambiguous to the code that uses it."""
    from pipeline import staging
    from pipeline.cards.fix import pick
    from pipeline.cards.review_pack import selector

    con = staging.connect(tmp_path / "s.duckdb")
    shared = "Which statement about transaction isolation is correct"
    rows = [
        ("00000000-0000-4000-8000-00000000000c", f"{shared} for read committed?"),
        # Same words, but later in the question and differently cased.
        ("00000000-0000-4000-8000-00000000000d", f"In MySQL: {shared.lower()} for repeatable read?"),
    ]
    for cid, prompt in rows:
        con.execute("""insert into cards (id, topic_slug, format, prompt_md, answer_md, kept, status, source)
            values (?, 'sql-iso', 'mcq', ?, 'a', true, 'draft', 'lesson')""", [cid, prompt])

    class Row:
        def __init__(self, prompt):
            self.prompt = prompt

    picked = selector(con, "sql-iso", rows[0][1])
    cards = [Row(p) for _, p in rows]
    assert pick(cards, picked) is not None, f"{picked!r} is still ambiguous to pick"


def test_a_question_that_does_not_match_its_archetype_is_rejected():
    """The hole the first corpus shipped through.

    A card filed under `output-prediction` asked which SOLID principle a design
    violates, and every gate passed it: wellformed checks the answer's shape, the
    blind gate checks guessability, and fits_format asks whether the answer fits
    the screen. None of them asked whether the question was the one the archetype
    promised.
    """
    from types import SimpleNamespace

    from pipeline.cards import gate

    card = SimpleNamespace(
        # Medium, so `wellformed` has no quarrel with it: a Hard card without a
        # why-step is rejected earlier and would not reach the archetype verdict.
        id="x", archetype="output-prediction", format="pick_one", difficulty="Medium",
        prompt="Which SOLID principle is most clearly violated by this design?",
        options=["SRP", "OCP", "LSP", "DIP"], answer="OCP", key_points=[],
        picked=[1], constraints=None, pairs=None, value=None, tolerance=None, why_step=None,
    )
    result = gate.GateResult(verdicts=[
        gate.Verdict(index=0, answerable=True, premise_holds=True, one_answer=True,
                     fits_archetype=False, fits_format=True, gradable=True, confidence=0.9,
                     reason="asks about design principles, not output"),
    ])
    rejected = gate.judge([card], result)
    assert len(rejected) == 1, rejected
    assert "wrong archetype" in rejected[0][1], rejected[0][1]


def test_the_gate_is_told_which_archetype_it_is_judging():
    from types import SimpleNamespace

    from pipeline.cards import gate

    shown = gate.prompt_only(SimpleNamespace(
        archetype="tap-the-bug", format="tap_in_place", prompt="Which line is wrong?", options=None))
    assert "tap-the-bug" in shown, shown
    # A legacy card has no archetype and must not grow a blank line for one.
    legacy = gate.prompt_only(SimpleNamespace(archetype=None, format="typed", prompt="Why?", options=None))
    assert "archetype" not in legacy, legacy


def test_a_refusal_to_rule_on_archetype_verdict_rejects_rather_than_passes():
    """The check must fail closed.

    `fits_archetype` used to default to True, so a model that simply did not
    answer the question passed every mismatch silently - a safety check that is
    disabled by the thing it is checking not replying.
    """
    from types import SimpleNamespace

    from pipeline.cards import gate

    card = SimpleNamespace(
        id="x", archetype="output-prediction", format="pick_one", difficulty="Medium",
        prompt="What does this print?", options=["1", "2", "3", "4"], answer="2",
        key_points=[], picked=[1], constraints=None, pairs=None, value=None,
        tolerance=None, why_step=None,
    )
    # A verdict with every other field answered and this one absent.
    silent = gate.GateResult(verdicts=[
        # Every verdict before the archetype one answered: isolates that branch.
        gate.Verdict(index=0, fits_archetype=None, answerable=True, premise_holds=True, one_answer=True,
                     fits_format=True, gradable=True, confidence=0.9, reason="fine"),
    ])
    rejected = gate.judge([card], silent)
    assert len(rejected) == 1 and "wrong archetype" in rejected[0][1], rejected

    # A legacy card has no archetype, so the question does not apply to it.
    legacy = SimpleNamespace(
        id="y", archetype=None, format="typed", difficulty="Medium", prompt="Why?",
        options=[], answer="because", key_points=[], picked=None, constraints=None,
        pairs=None, value=None, tolerance=None, why_step=None,
    )
    assert gate.judge([legacy], silent) == []


def test_a_self_contradictory_premise_is_rejected():
    """Card #4 of the review pack: "16 initial bins", "no resizing", "all keys hash to
    distinct bins", then 100,000 insertions. 100,000 distinct bins cannot exist among
    16, and the reference answer accepted the contradiction. Nothing checked that a
    question's own assumptions can hold at once."""
    from types import SimpleNamespace

    from pipeline.cards import gate

    card = SimpleNamespace(
        id="x", archetype="complexity", format="numeric", difficulty="Medium",
        prompt="A map has 16 bins. 100 threads insert 1000 distinct keys each. "
               "Assume no resizing and all keys hash to distinct bins. How many CAS operations?",
        options=None, answer="100000", key_points=[], picked=None, constraints=None,
        pairs=None, value=100000.0, tolerance=0.0, why_step=None,
    )
    result = gate.GateResult(verdicts=[
        gate.Verdict(index=0, answerable=True, premise_holds=False, one_answer=True,
                     fits_archetype=True,
                     fits_format=True, gradable=True, confidence=0.8,
                     reason="100,000 distinct bins cannot exist among 16"),
    ])
    rejected = gate.judge([card], result)
    assert len(rejected) == 1 and "impossible premise" in rejected[0][1], rejected


def test_a_refusal_to_rule_on_premise_verdict_also_rejects():
    """Fails closed, like the archetype verdict: silence must not read as "fine"."""
    from types import SimpleNamespace

    from pipeline.cards import gate

    card = SimpleNamespace(
        id="x", archetype="concept", format="pick_one", difficulty="Medium",
        prompt="Which is correct?", options=["a", "b", "c", "d"], answer="a",
        key_points=[], picked=[0], constraints=None, pairs=None, value=None,
        tolerance=None, why_step=None,
    )
    silent = gate.GateResult(verdicts=[
        gate.Verdict(index=0, one_answer=True, premise_holds=None, answerable=True, fits_archetype=True, fits_format=True,
                     gradable=True, confidence=0.9, reason="fine"),
    ])
    rejected = gate.judge([card], silent)
    assert len(rejected) == 1 and "impossible premise" in rejected[0][1], rejected


def test_a_question_with_two_defensible_answers_is_rejected():
    """The class a third reviewer named that nobody else did: the question does not
    constrain the answer. "A stable sort, optimal comparisons" does not fix an
    algorithm, so a comparison count is not determined by the question as asked."""
    from types import SimpleNamespace

    from pipeline.cards import gate

    card = SimpleNamespace(
        id="x", archetype="complexity", format="pick_one", difficulty="Hard",
        prompt="Using a stable sort with optimal comparisons, how many comparisons are needed?",
        options=["7", "8", "9", "10"], answer="7", key_points=[], picked=[0],
        constraints=None, pairs=None, value=None, tolerance=None,
        why_step={"options": ["because the bound is tight", "because it is TimSort"], "correct": 0},
    )
    result = gate.GateResult(verdicts=[
        gate.Verdict(index=0, answerable=True, premise_holds=True, one_answer=False,
                     fits_archetype=True, fits_format=True, gradable=True, confidence=0.8,
                     reason="no algorithm is fixed, so the count is not determined"),
    ])
    rejected = gate.judge([card], result)
    assert len(rejected) == 1 and "more than one answer" in rejected[0][1], rejected


def test_a_refusal_to_rule_on_one_answer_verdict_also_rejects():
    from types import SimpleNamespace

    from pipeline.cards import gate

    card = SimpleNamespace(
        id="x", archetype="concept", format="pick_one", difficulty="Medium",
        prompt="Which is correct?", options=["a", "b", "c", "d"], answer="a",
        key_points=[], picked=[0], constraints=None, pairs=None, value=None,
        tolerance=None, why_step=None,
    )
    silent = gate.GateResult(verdicts=[
        gate.Verdict(index=0, one_answer=None, answerable=True, premise_holds=True, fits_archetype=True,
                     fits_format=True, gradable=True, confidence=0.9, reason="fine"),
    ])
    rejected = gate.judge([card], silent)
    assert len(rejected) == 1 and "more than one answer" in rejected[0][1], rejected


def test_a_reply_that_leaves_a_verdict_out_is_invalid_rather_than_a_rejection():
    """The `trees` batch: a model returned verdicts with the premise field missing and
    18 fair cards were rejected as "the gate did not rule", with nothing asking it
    again. An absent field must not reach judge() at all - it is a schema violation,
    which the LLM client retries - while an explicit null still means "I will not
    rule" and still rejects.
    """
    import pytest
    from pydantic import ValidationError

    from pipeline.cards import gate

    stated = '{"index": 0, "answerable": true, "fits_format": true, "gradable": true, '
    for missing in ("fits_archetype", "premise_holds", "one_answer"):
        fields = {"fits_archetype": "true", "premise_holds": "true", "one_answer": "true"}
        del fields[missing]
        body = stated + ", ".join(f'"{k}": {v}' for k, v in fields.items()) + "}"
        with pytest.raises(ValidationError) as caught:
            gate.Verdict.model_validate_json(body)
        assert missing in str(caught.value), missing

    # The null is accepted, carried, and judged as a refusal.
    null_ruling = gate.Verdict.model_validate_json(
        stated + '"fits_archetype": true, "premise_holds": null, "one_answer": true}'
    )
    assert null_ruling.premise_holds is None

    # And the schema the model is shown says all three are required, which is what
    # makes it answer them in the first place.
    required = gate.Verdict.model_json_schema()["required"]
    assert {"fits_archetype", "premise_holds", "one_answer"} <= set(required), required
