from pipeline import staging
from pipeline.enrich import patterns
from tests.test_patterns import FakeLLM


def test_evaluate_scores_against_neetcode_and_writes_nothing(tmp_path):
    con = staging.connect(tmp_path / "s.duckdb")
    con.execute("""insert into problems (slug, kind, title, difficulty, pattern_slug, pattern_source, statement_md, solutions) values
        ('a', 'leetcode', 'A', 'Easy', 'sliding-window', 'neetcode', 's', '{}'),
        ('b', 'leetcode', 'B', 'Easy', 'trees', 'neetcode', 's', '{}')""")
    accuracy, results = patterns.evaluate(con, FakeLLM(), n=10)
    assert accuracy == 0.5 and len(results) == 2
    assert con.execute("select count(*) from problems where pattern_source = 'ai'").fetchone()[0] == 0
