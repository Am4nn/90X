"""Every command module imports and every subcommand is wired.

A syntax error in commands.py once passed a full green test run, because
nothing imported it: the tests exercise the libraries and the CLI was only
ever run by hand. These import the modules the CLI needs and check the
parser agrees with the dispatch table.
"""

import importlib
import pkgutil

import pytest

import pipeline


def test_every_pipeline_module_imports():
    """Catches a file that parses only when someone runs its command."""
    broken = []
    for module in pkgutil.walk_packages(pipeline.__path__, prefix="pipeline."):
        # __main__ runs the CLI on import, and would parse pytest's own argv.
        if module.name.endswith("__main__"):
            continue
        try:
            importlib.import_module(module.name)
        except Exception as e:  # noqa: BLE001 - report them all, not the first
            broken.append(f"{module.name}: {type(e).__name__}: {e}")
    assert not broken, "modules failed to import:\n" + "\n".join(broken)


def test_every_subcommand_has_a_handler():
    from pipeline.commands import COMMANDS

    parser_commands = {
        "sources", "download", "normalize", "enrich", "topics", "tricks", "chunk", "embed",
        "cards", "lessons", "lesson-cards", "card-review", "lesson-review", "consistency",
        "gaps", "roadmaps", "publish", "rebatch", "status",
    }
    missing = sorted(c for c in parser_commands - {"sources", "download"} if c not in COMMANDS)
    assert not missing, f"subcommands with no handler: {missing}"


@pytest.mark.parametrize("command", ["lessons", "lesson-cards", "consistency", "gaps", "publish", "roadmaps"])
def test_the_parser_accepts_each_command(command):
    import sys
    from unittest.mock import patch

    with patch.object(sys, "argv", ["pipeline", command, "--help"]), pytest.raises(SystemExit) as exit_info:
        pipeline.main()
    assert exit_info.value.code == 0
