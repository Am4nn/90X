"""Re-deriving a key from its explanation: the model names things, the code computes indices.

A grid stores `row * columns + column`, and a model asked for that number got it wrong in
about half the grids it wrote - which is how the cards this repairs came to exist. So these
pin the two things that matter: the arithmetic happens in code, and a part the explanation
does not settle means no repair rather than a guess.
"""

from types import SimpleNamespace

from pipeline.cards import key_repair as kr


def card(**kw):
    base = dict(format="pick_one", prompt="Q?", answer="An explanation.", options=None,
                picked=None, constraints=None, pairs=None, value=None, tolerance=None, why_step=None)
    base.update(kw)
    return SimpleNamespace(**base)


GRID = {"rows": ["Class inheritance", "Interface inheritance", "Composition"],
        "columns": ["Is-a", "Inherits implementation", "Runtime replaceable"]}


def test_a_grid_key_is_computed_in_code_from_row_and_column_numbers():
    c = card(format="grid_toggle", options=GRID)
    derived = kr.Grid(ticks=[
        kr.RowTicks(row=0, columns=[0, 1]),
        kr.RowTicks(row=1, columns=[0]),
        kr.RowTicks(row=2, columns=[2]),
    ])
    # row * 3 + column: (0,0)=0 (0,1)=1 (1,0)=3 (2,2)=8
    assert kr.new_key(c, derived) == {"picked": [0, 1, 3, 8]}


def test_a_grid_that_skips_a_row_is_not_repaired_rather_than_guessed():
    c = card(format="grid_toggle", options=GRID)
    derived = kr.Grid(ticks=[kr.RowTicks(row=0, columns=[0]), kr.RowTicks(row=2, columns=[2])])
    assert kr.new_key(c, derived) is None


def test_a_grid_the_explanation_does_not_settle_is_not_repaired():
    assert kr.new_key(card(format="grid_toggle", options=GRID), kr.Grid(ticks=None)) is None
    # A grid with nothing ticked anywhere is not a key either.
    empty = kr.Grid(ticks=[kr.RowTicks(row=i, columns=[]) for i in range(3)])
    assert kr.new_key(card(format="grid_toggle", options=GRID), empty) is None


def test_a_column_outside_the_grid_is_refused():
    c = card(format="grid_toggle", options=GRID)
    assert kr.new_key(c, kr.Grid(ticks=[kr.RowTicks(row=i, columns=[5]) for i in range(3)])) is None


def test_claim_verdicts_are_matched_by_statement_and_every_statement_needs_one():
    c = card(format="claim_grid", options=["s0", "s1", "s2"])
    ok = kr.Claims(verdicts=[kr.Verdict(statement=2, true=False), kr.Verdict(statement=0, true=True), kr.Verdict(statement=1, true=True)])
    assert kr.new_key(c, ok) == {"pairs": [[0, 1], [1, 1], [2, 0]]}
    unsettled = kr.Claims(verdicts=[kr.Verdict(statement=0, true=True), kr.Verdict(statement=1, true=None), kr.Verdict(statement=2, true=False)])
    assert kr.new_key(c, unsettled) is None, "a statement the explanation does not rule on cannot be guessed"
    missing = kr.Claims(verdicts=[kr.Verdict(statement=0, true=True), kr.Verdict(statement=1, true=True)])
    assert kr.new_key(c, missing) is None


def test_a_chosen_option_must_exist():
    c = card(options=["a", "b", "c", "d"])
    assert kr.new_key(c, kr.Choice(choice=2)) == {"picked": [2]}
    assert kr.new_key(c, kr.Choice(choice=4)) is None
    assert kr.new_key(c, kr.Choice(choice=None)) is None
    tap = card(format="tap_in_place", options=["x", "y"])
    assert kr.new_key(tap, kr.Choice(choice=1)) == {"picked": [1]}


def test_an_assemble_order_becomes_a_chain_of_constraints_and_must_use_every_token():
    c = card(format="assemble", options={"tokens": ["a", "b", "c", "d"], "fixed": [None] * 4})
    assert kr.new_key(c, kr.Order(order=[2, 0, 3, 1])) == {"constraints": {"before": [[2, 0], [0, 3], [3, 1]]}}
    assert kr.new_key(c, kr.Order(order=[0, 1, 2])) is None, "a token is missing"
    assert kr.new_key(c, kr.Order(order=[0, 1, 1, 2])) is None, "a token is repeated"
    assert kr.new_key(c, kr.Order(order=None)) is None


def test_match_and_bucket_need_every_item_placed():
    m = card(format="match", options={"left": ["l0", "l1"], "right": ["r0", "r1"]})
    assert kr.new_key(m, kr.Pairs(pairs=[[0, 1], [1, 0]])) == {"pairs": [[0, 1], [1, 0]]}
    assert kr.new_key(m, kr.Pairs(pairs=[[0, 1]])) is None
    assert kr.new_key(m, kr.Pairs(pairs=[[0, 1], [1, 1]])) is None, "two terms cannot share a meaning"
    b = card(format="bucket", options={"items": ["i0", "i1", "i2"], "columns": ["c0", "c1"]})
    assert kr.new_key(b, kr.Placements(placements=[[0, 0], [1, 1], [2, 1]])) == {"pairs": [[0, 0], [1, 1], [2, 1]]}
    assert kr.new_key(b, kr.Placements(placements=[[0, 0], [1, 1]])) is None
    assert kr.new_key(b, kr.Placements(placements=[[0, 0], [1, 1], [2, 2]])) is None, "column 2 does not exist"


def test_a_number_the_explanation_does_not_give_is_not_invented():
    assert kr.new_key(card(format="numeric"), kr.Number(value=4.17)) == {"value": 4.17}
    assert kr.new_key(card(format="numeric"), kr.Number(value=None)) is None


def test_the_model_is_shown_numbered_things_and_the_explanation_and_told_to_take_it_at_its_word():
    c = card(format="grid_toggle", options=GRID, answer="Interface inheritance does not inherit implementation.")

    class Fake:
        def __init__(self):
            self.seen = None

        def complete_json(self, system, user, schema, tier="smart", purpose="", thinking=False):
            self.seen = {"system": system, "user": user, "schema": schema}
            return kr.Grid(ticks=None)

    llm = Fake()
    kr.derive(llm, c)
    assert "row 1: Interface inheritance" in llm.seen["user"]
    assert "column 2: Runtime replaceable" in llm.seen["user"]
    assert "Interface inheritance does not inherit implementation." in llm.seen["user"]
    assert llm.seen["schema"] is kr.Grid
    assert "Do not overrule it" in llm.seen["system"] and "give null" in llm.seen["system"]
    assert kr.derive(Fake(), card(format="order")) is None, "order cards are not repaired here"
