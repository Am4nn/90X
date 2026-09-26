from pipeline import staging
from pipeline.cards import run as card_run


class FakeLLM:
    models = {"fast": "deepseek-flash", "smart": "deepseek-v4-pro", "review": "gemini"}

    def __init__(self):
        self.calls = []

    def complete_json(self, system, user, schema, tier="fast", purpose=""):
        self.calls.append((purpose, tier))
        if purpose.startswith("cards-check"):
            bad = "drop me" in user
            return schema(correct=2 if bad else 5, clear=5, relevant=5, issues="wrong" if bad else "")
        return schema(cards=[
            {"format": "typed", "prompt": "Which pattern fits and why?", "answer": "Sliding window",
             "key_points": ["contiguous", "shrink"], "difficulty": "Medium"},
            {"format": "flash", "prompt": "drop me: what is the complexity?", "answer": "O(n)",
             "key_points": ["linear", "one pass"], "difficulty": "Easy"},
        ])


def seed(con):
    con.execute("""insert into topics (slug, domain, name, importance) values
        ('sd-caching', 'system_design', 'Caching', 0.9), ('lld-parking', 'lld', 'Parking lot', 0.5)""")
    con.execute("""insert into problems (slug, kind, title, difficulty, pattern_slug, statement_md, solutions, importance, nc150, topic_slugs, premium) values
        ('hot', 'leetcode', 'Hot', 'Medium', 'sliding-window', 's', '{"python": "x"}', 0.9, true, [], false),
        ('cold', 'leetcode', 'Cold', 'Hard', 'graphs', 's', '{"python": "x"}', 0.1, false, [], false),
        ('sqlp', 'leetcode', 'SQL', 'Easy', null, 's', '{}', 0.9, false, ['sql'], false)""")
    con.execute("""insert into documents (id, domain, title, body_md, topic_slug) values
        ('d1', 'system_design', 'Caching', ?, 'sd-caching'),
        ('d2', 'system_design', 'Lab Projects', ?, 'sd-caching'),
        ('d3', 'lld', 'Parking lot', ?, 'lld-parking'),
        ('d4', 'system_design', 'Unassigned', ?, null)""", ["x " * 400] * 4)


def test_generates_reviews_and_stores_cards_in_batches(tmp_path):
    con = staging.connect(tmp_path / "s.duckdb")
    seed(con)
    llm = FakeLLM()
    stats = card_run.run(con, llm, min_importance=0.5)
    # sources: 'hot' problem + 'd1' document (lab projects, unassigned, lld and low-importance skipped)
    assert stats["sources"] == 2
    assert con.execute("select count(*) from cards").fetchone()[0] == 4
    assert con.execute("select count(*) from cards where kept").fetchone()[0] == 2
    batches = dict(con.execute("select domain, ai_pass_rate from card_batches").fetchall())
    assert batches == {"dsa": 0.5, "system_design": 0.5}
    assert ("cards-problem", "fast") in llm.calls and ("cards-check", "review") in llm.calls
    # re-run skips sources that already have cards
    assert card_run.run(con, llm, min_importance=0.5)["sources"] == 0
