from pipeline import staging
from pipeline.enrich import tricks


class FakeLLM:
    def __init__(self):
        self.calls = []

    def complete_json(self, system, user, schema, tier="fast", purpose=""):
        self.calls.append({"user": user, "tier": tier})
        return schema(tricks=[
            {"name": "XOR cancels duplicates", "idea": "a ^ a = 0, so XOR of all values leaves the odd one out.",
             "snippet": "x = 0\nfor v in nums: x ^= v", "problems": ["single-number", "made-up-problem"]},
            {"name": "Lowest set bit", "idea": "x & -x isolates the lowest set bit.", "snippet": "low = x & -x",
             "problems": ["single-number-iii"]},
        ])


def test_tricks_link_only_real_problems(tmp_path):
    con = staging.connect(tmp_path / "s.duckdb")
    con.execute("""insert into problems (slug, kind, title, difficulty, pattern_slug, statement_md, solutions, importance) values
        ('single-number', 'leetcode', 'Single Number', 'Easy', 'bit-manipulation', 's', '{"python": "xor"}', 0.9),
        ('single-number-iii', 'leetcode', 'Single Number III', 'Medium', 'bit-manipulation', 's', '{"python": "lowbit"}', 0.6)""")
    llm = FakeLLM()
    n = tricks.build(con, llm, patterns=[("bit-manipulation", "Bit Manipulation")])
    assert n == 2
    rows = con.execute("select name, problem_slugs from pattern_tricks order by sort").fetchall()
    assert rows[0] == ("XOR cancels duplicates", ["single-number"])  # invented slug dropped
    assert "Single Number" in llm.calls[0]["user"] and "xor" in llm.calls[0]["user"] and llm.calls[0]["tier"] == "smart"
