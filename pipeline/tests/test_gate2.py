"""Gate 2 reports a rejection rate over n cards and writes nothing."""

from pathlib import Path

from pipeline import staging
from pipeline.cards import gate2
from pipeline.cards.blind_gate import Guess


class _FakeLLM:
    def __init__(self):
        self.calls = 0

    def complete_json(self, system, user, schema, tier="smart", purpose="", thinking=False):
        self.calls += 1
        return Guess(picked=[0])


def _insert(con, i: int, picked: str) -> None:
    con.execute(
        """insert into cards (id, topic_slug, format, archetype, difficulty, prompt_md, options,
                              answer_md, key_points, picked, status, source, kept)
           values (?, ?, 'pick_one', 'concept', 'Easy', ?, ?, 'a hash map', '["a","b"]', ?, 'draft', 'lesson', true)""",
        [f"00000000-0000-4000-8000-00000000000{i}", f"topic-{i}", f"Which structure? ({i})",
         '["w","x","y","z"]', picked],
    )


def test_gate2_reports_the_rejection_rate_and_writes_nothing(tmp_path):
    con = staging.connect(Path(tmp_path) / "s.duckdb")
    for i in range(3):
        _insert(con, i, "[0]")
    llm = _FakeLLM()

    result = gate2.run(con, llm=llm, n=3)

    assert result["cards"] == 3
    # Every sample picks [0], which matches `picked`, so every card is guessable.
    assert result["rejected"] == 3
    assert result["rate"] == 1.0
    assert llm.calls == 9  # 3 samples x 3 cards
    # Gate 2 is report-only: nothing is written, no status changes.
    assert con.execute("select count(*) from cards where status = 'draft'").fetchone()[0] == 3
    assert con.execute("select count(*) from cards where status != 'draft'").fetchone()[0] == 0


def test_gate2_counts_nothing_when_no_drafts(tmp_path):
    con = staging.connect(Path(tmp_path) / "s.duckdb")
    result = gate2.run(con, llm=_FakeLLM(), n=3)
    assert result == {"cards": 0, "rejected": 0, "rate": 0.0, "spend": 0.0}
