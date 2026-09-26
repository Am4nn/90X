from pipeline import staging
from pipeline.enrich import patterns


class FakeLLM:
    def __init__(self):
        self.prompts = []

    def complete_json(self, system, user, schema, tier="fast", purpose=""):
        self.prompts.append(user)
        return schema(pattern="Sliding Window", techniques=["sliding-window"])


def test_tags_only_untagged_problems_with_statements(tmp_path):
    con = staging.connect(tmp_path / "s.duckdb")
    con.execute("""insert into problems (slug, kind, title, difficulty, pattern_slug, pattern_source, statement_md, solutions, topic_slugs) values
        ('a', 'leetcode', 'A', 'Easy', 'arrays-hashing', 'neetcode', 'stmt', '{}', []),
        ('b', 'leetcode', 'B', 'Medium', null, null, 'longest window', '{"python": "def f(): pass"}', []),
        ('c', 'leetcode', 'C', 'Hard', null, null, null, '{}', [])""")
    fake = FakeLLM()
    assert patterns.run(con, fake) == 2
    rows = dict(con.execute("select slug, pattern_slug || '/' || coalesce(pattern_source, '') from problems").fetchall())
    assert rows == {"a": "arrays-hashing/neetcode", "b": "sliding-window/ai", "c": None}  # NeetCode pattern kept
    techniques = dict(con.execute("select slug, techniques from problems").fetchall())
    assert techniques["a"] == ["sliding-window"] and techniques["b"] == ["sliding-window"]
    assert any("longest window" in p and "def f(): pass" in p for p in fake.prompts)


def test_pattern_choice_rejects_unknown_names():
    import pytest
    from pydantic import ValidationError

    with pytest.raises(ValidationError):
        patterns.PatternTags(pattern="Quantum Sort", techniques=["greedy"])
