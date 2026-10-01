"""The final validation pass: answer-definition consistency + cross-topic dedupe."""

from pathlib import Path

from pipeline import staging
from pipeline.cards.validate import answer_problems, consistency, cross_topic_dupes


def _card(format, options, **over):
    base = {"format": format, "options": options, "picked": None, "constraints": None,
            "pairs": None, "value": None, "tolerance": None, "why_step": None}
    base.update(over)
    return base


def test_a_picked_index_out_of_range_is_flagged():
    card = _card("pick_one", ["A", "B", "C", "D"], picked=[5])
    assert any("picked index 5 out of range" in p for p in answer_problems(card))


def test_a_valid_pick_one_card_is_clean():
    card = _card("pick_one", ["A", "B", "C", "D"], picked=[0])
    assert answer_problems(card) == []


def test_a_why_step_correct_out_of_range_is_flagged():
    card = _card("pick_one", ["A", "B", "C", "D"], picked=[0],
                 why_step={"options": ["r1", "r2"], "correct": 2})
    assert any("why-step correct index 2 out of range" in p for p in answer_problems(card))


def test_a_numeric_card_missing_tolerance_is_flagged():
    card = _card("numeric", None, value=5, tolerance=None)
    assert any("missing value or tolerance" in p for p in answer_problems(card))


def _insert(con, topic, card_id, prompt):
    con.execute("insert into topics (slug, domain, name, importance) values (?, 'dsa', ?, ?)",
                [topic, topic, 1.0])
    con.execute("insert into cards (id, topic_slug, format, prompt_md, answer_md, status, source) "
                "values (?, ?, 'pick_one', ?, 'a', 'draft', 'lesson')", [card_id, topic, prompt])


def test_cross_topic_dupes_flags_the_same_question_in_two_topics(tmp_path):
    con = staging.connect(Path(tmp_path) / "s.duckdb")
    _insert(con, "topic-a", "a1", "What is the time complexity of a hash table lookup?")
    _insert(con, "topic-b", "b1", "What is the time complexity of hash table lookup?")
    dupes = cross_topic_dupes(con)
    assert len(dupes) == 1
    assert dupes[0][0] == "a1" and dupes[0][1] == "b1"


def test_cross_topic_dupes_ignores_distinct_questions(tmp_path):
    con = staging.connect(Path(tmp_path) / "s.duckdb")
    _insert(con, "topic-a", "a1", "What is the time complexity of a hash table lookup?")
    _insert(con, "topic-b", "b1", "Which traversal visits the left subtree first?")
    assert cross_topic_dupes(con) == []


def test_consistency_returns_only_inconsistent_cards(tmp_path):
    con = staging.connect(Path(tmp_path) / "s.duckdb")
    _insert(con, "topic-a", "a1", "Which structure gives O(1) lookup?")
    con.execute("update cards set picked = '[5]' where id = 'a1'")
    bad = consistency(con)
    assert "a1" in bad
    assert any("picked index 5" in p for p in bad["a1"])
