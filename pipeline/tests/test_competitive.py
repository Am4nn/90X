from pipeline.normalize import competitive


def cand(i, pattern="Greedy", score=5):
    return {"id": f"x{i}", "statement": "s", "solution": "code", "url": f"https://codeforces.com/problemset/problem/{i}/A",
            "source": "apps", "triage": competitive.Triage(interview_like=score, title=f"Problem {i}", difficulty="Medium",
                                                          pattern=pattern, techniques=["greedy"])}


def test_select_keeps_best_and_balances_patterns():
    pool = [cand(i, "Greedy", 5) for i in range(40)] + [cand(100 + i, "Graphs", 4) for i in range(10)] + \
           [cand(200 + i, "Trees", 2) for i in range(10)]
    chosen = competitive.select(pool, keep=30, per_pattern=20)
    patterns = [c["triage"].pattern for c in chosen]
    assert len(chosen) == 30
    assert patterns.count("Greedy") == 20 and patterns.count("Graphs") == 10
    assert "Trees" not in patterns  # score 2 is below the bar


def test_clean_statement_drops_language_preamble():
    raw = "Solve the following coding problem using the programming language python:\n\nPolycarp has n words.\n\nThe input will be stdin"
    assert competitive.clean_statement(raw).startswith("Polycarp has n words.")


def test_slug_is_stable_and_prefixed():
    assert competitive.slug_for("apps", "x1", "Binary Words!") == competitive.slug_for("apps", "x1", "Binary Words!")
    assert competitive.slug_for("apps", "x1", "Binary Words!").startswith("cp-binary-words-")
