"""scripts/key_audit.py: the parts that decide what gets rejected.

A script that rejects live cards on a model's say-so needs its own bookkeeping to be right,
because a checkpoint that loses the first pass, or a `--from` that crashes after committing,
is how a run's paid-for results go missing.
"""

import importlib.util
import json
import os
from pathlib import Path

import duckdb

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "key_audit.py"
os.chdir(Path(__file__).resolve().parents[1])
_spec = importlib.util.spec_from_file_location("key_audit_script", SCRIPT)
ks = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ks)


def v(verdict, reason=""):
    return {"verdict": verdict, "reason": reason, "topic": "t"}


def test_a_card_is_confirmed_only_when_both_passes_call_it_a_contradiction():
    state = {
        "first": {"both": v("contradicts"), "only_first": v("contradicts"), "only_second": v("agrees")},
        "second": {"both": v("contradicts"), "only_first": v("agrees"), "only_second": v("contradicts")},
    }
    assert ks.confirmed_from(state) == ["both"]


def test_every_checkpoint_is_the_full_schema_so_the_second_pass_cannot_erase_the_first(tmp_path, monkeypatch):
    monkeypatch.setattr(ks, "OUT", str(tmp_path / "audit.json"))
    state = {"first": {"a": v("contradicts")}, "second": {}, "confirmed": []}
    ks.save(state)  # a checkpoint written mid-first-pass
    state["second"]["a"] = v("contradicts")
    ks.save(state)  # then mid-second-pass
    saved = json.loads(Path(ks.OUT).read_text(encoding="utf-8"))
    assert set(saved) == {"first", "second", "confirmed"}
    assert saved["first"]["a"]["verdict"] == "contradicts", "the second pass erased the first"
    assert saved["confirmed"] == ["a"]


def test_from_survives_a_file_that_never_got_its_final_save(tmp_path, monkeypatch):
    """A run killed between passes leaves a file with no `confirmed`. It must derive it and
    reject that card, not crash on the missing key after the passes were already paid for."""
    path = tmp_path / "partial.json"
    path.write_text(json.dumps({"first": {"a": v("contradicts", "ticks X")}, "second": {"a": v("contradicts", "ticks X")}}),
                    encoding="utf-8")

    class FakeCon:
        def __init__(self):
            self.updates = []

        def execute(self, sql, params=None):
            if sql.lstrip().startswith("update"):
                self.updates.append(params)
            return self

        def fetchone(self):
            return (0,)

        def commit(self):
            pass

    con = FakeCon()
    monkeypatch.setattr(ks.duckdb, "connect", lambda *a, **k: con)
    ks.apply_saved(str(path))
    assert [u[1] for u in con.updates] == ["a"], con.updates


def test_from_with_nothing_confirmed_does_nothing_and_does_not_touch_the_database(tmp_path, monkeypatch, capsys):
    path = tmp_path / "none.json"
    path.write_text(json.dumps({"first": {"a": v("agrees")}, "second": {}, "confirmed": []}), encoding="utf-8")

    def forbidden(*a, **k):
        raise AssertionError("opened the database for an empty result")

    monkeypatch.setattr(ks.duckdb, "connect", forbidden)
    ks.apply_saved(str(path))
    assert "nothing" in capsys.readouterr().out


def test_stratifying_an_empty_selection_returns_nothing_instead_of_dividing_by_zero():
    con = duckdb.connect(":memory:")
    con.execute("create table cards (id varchar, format varchar)")
    con.execute("insert into cards values ('x', 'self_rate'), ('y', 'compose')")
    assert ks.stratified(con, ["x", "y"], 120) == []
    assert ks.stratified(con, [], 120) == []
