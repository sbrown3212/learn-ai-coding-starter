"""Exact stdout for programs in examples/.

Each entry maps an example's file stem to everything it prints. An example without an
entry here still runs cleanly under tests/test_examples.py; this file is where behavior
is pinned down.
"""

from pathlib import Path

import pytest

from sloperator.runner import run_source

EXAMPLES = Path(__file__).resolve().parent.parent / "examples"

EXPECTED_OUTPUTS = {
    "equality": "✅\n❌\n❌\n",
    "hello": "hello, slop\n",
    "short-circuit": "❌\n✅\n",
}


@pytest.mark.parametrize(("name", "expected_stdout"), sorted(EXPECTED_OUTPUTS.items()))
def test_example_output(name: str, expected_stdout: str):
    source = (EXAMPLES / f"{name}.slop").read_text(encoding="utf-8")
    result = run_source(source)
    assert result.stderr == ""
    assert result.exit_code == 0
    assert result.stdout == expected_stdout
