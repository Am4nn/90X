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


def _cards(rows):
    con = duckdb.connect(":memory:")
    con.execute("create table cards (id varchar, status varchar, kept boolean, reject_reason varchar, quality varchar)")
    for r in rows:
        con.execute("insert into cards values (?, ?, ?, ?, '{}')", r)
    return con


def test_a_retest_restores_only_cards_the_audit_rejected_and_rejects_only_live_ones(tmp_path, monkeypatch):
    """Two rules that keep this from undoing someone else's decision: a card rejected for any
    other reason (a duplicate, a premise that cannot hold) is not this script's to bring back
    just because two models liked its key, and a card already rejected is not newly rejected."""
    con = _cards([
        ("audit-rejected", "rejected", False, "answer key contradicts the explanation: x"),
        ("rejected-for-other-reason", "rejected", False, "near-duplicate of abc"),
        ("live-and-confirmed-bad", "draft", True, None),
        ("already-rejected-and-bad", "rejected", False, "answer key contradicts the explanation: y"),
    ])
    path = tmp_path / "retest.json"
    path.write_text(json.dumps({
        "restore": ["audit-rejected", "rejected-for-other-reason"],
        "keep_out": ["live-and-confirmed-bad", "already-rejected-and-bad"],
        "uncertain": [], "first": {}, "second": {},
    }), encoding="utf-8")
    monkeypatch.setattr(ks.duckdb, "connect", lambda *a, **k: con)
    monkeypatch.setattr(ks, "APPLIED", str(tmp_path / "applied.json"))

    ks.apply_retest(str(path))

    status = dict(con.execute("select id, status || '/' || kept::varchar from cards").fetchall())
    assert status["audit-rejected"] == "draft/true", "both models cleared it, so it comes back"
    assert status["rejected-for-other-reason"] == "rejected/false", "not the audit's to restore"
    assert status["live-and-confirmed-bad"] == "rejected/false", "a live card both models confirmed bad is taken out"
    assert status["already-rejected-and-bad"] == "rejected/false"
    applied = json.loads(Path(ks.APPLIED).read_text(encoding="utf-8"))
    assert applied == {"restored": ["audit-rejected"], "newly_rejected": ["live-and-confirmed-bad"]}
    note = con.execute("select quality from cards where id = 'audit-rejected'").fetchone()[0]
    assert "key_audit_restored" in note, "a restored card records why it was put back"


def test_a_retest_with_nothing_to_do_does_not_open_the_database(tmp_path, monkeypatch, capsys):
    path = tmp_path / "empty.json"
    path.write_text(json.dumps({"restore": [], "keep_out": [], "uncertain": ["a"], "first": {}, "second": {}}), encoding="utf-8")

    def forbidden(*a, **k):
        raise AssertionError("opened the database with nothing to apply")

    monkeypatch.setattr(ks.duckdb, "connect", forbidden)
    ks.apply_retest(str(path))
    assert "nothing to restore" in capsys.readouterr().out
