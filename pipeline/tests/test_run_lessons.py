"""The generation driver: budget, per-archetype writes, refills, and save."""

import json
from pathlib import Path

from pipeline import staging
from pipeline.cards import archetypes, run_lessons, write
from pipeline.cards.generate import Card


class _Writer:
    """Refuses ordering, writes a pick-one card for everything else."""

    def __init__(self):
        self.calls = []

    def complete_json(self, system, user, schema, tier="smart", purpose=""):
        self.calls.append(user)
        if "Primitive: order" in user:
            return write.WriteResult(refused="no natural sequence for this topic")
        return write.WriteResult(draft=write.CardDraft(
            prompt=f"Which structure gives O(1) lookup? ({len(self.calls)})",
            answer="A hash map.", key_points=["hashing spreads keys", "buckets stay short"],
            options=["A", "B", "C", "D"], picked=[0],
        ))


def _topic():
    return {"slug": "arrays-hashing", "name": "Arrays & Hashing", "domain": "dsa", "importance": 1.0}


def test_save_writes_the_archetype_and_answer_columns(tmp_path):
    con = staging.connect(Path(tmp_path) / "s.duckdb")
    topic = _topic()
    cards = [
        Card(format="pick_one", archetype="concept", difficulty="Easy",
             prompt="Which structure?", answer="A hash map.", key_points=["a", "b"],
             options=["A", "B", "C", "D"], picked=[0]),
        Card(format="numeric", archetype="complexity", difficulty="Easy",
             prompt="Time complexity?", answer="O(n).", key_points=["a", "b"],
             value=1, tolerance=0),
    ]
    run_lessons.save(con, topic, cards, {"problems": [], "tricks": []})
    rows = con.execute(
        "select format, archetype, difficulty, picked, value, tolerance, status, kept "
        "from cards where topic_slug = ? order by format", [topic["slug"]]
    ).fetchall()
    assert len(rows) == 2
    assert rows[0][0] == "numeric" and rows[0][1] == "complexity" and rows[0][4] == 1
    assert rows[1][0] == "pick_one" and rows[1][1] == "concept" and rows[1][3] == "[0]"
    assert all(r[6] == "draft" and r[7] for r in rows)


def test_constraints_are_saved_as_before_object(tmp_path):
    """Part B's grader reads constraints as {"before": [[a, b], ...]}; the flat
    list the writer returns must be wrapped before it hits the column."""
    con = staging.connect(Path(tmp_path) / "s.duckdb")
    topic = _topic()
    run_lessons.save(con, topic, [
        Card(format="order", archetype="sequence", difficulty="Medium",
             prompt="Put these in order.", answer="1, 2, 3.", key_points=["a", "b"],
             options=["A", "B", "C", "D", "E", "F"],
             constraints=[[1, 5], [5, 2]]),
    ], {"problems": [], "tricks": []})
    raw = con.execute("select constraints from cards where topic_slug = ?", [topic["slug"]]).fetchone()[0]
    assert json.loads(raw) == {"before": [[1, 5], [5, 2]]}


def test_a_refused_slot_refills_instead_of_aborting(tmp_path):
    con = staging.connect(Path(tmp_path) / "s.duckdb")
    topic = _topic()
    slots = archetypes.budget(topic)
    llm = _Writer()
    cards, refused = run_lessons.write_topic(llm, topic, "lesson", slots, "", "smart")
    # Every slot lands either a card or a recorded refusal; an ordering slot that
    # refuses gets refilled with another archetype rather than dropping the topic.
    assert len(cards) + len(refused) == len(slots)
    assert any("Primitive: order" in u for u in llm.calls), "the ordering slot was attempted"
    assert len(cards) == len(slots), "refill fills every slot the fake can answer"
