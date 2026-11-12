---
name: create-test-program
description: Add a runnable SlopLang example program to examples/ and pin its exact stdout in tests/test_example_outputs.py. Use this whenever the user asks for an example, sample, demo, or test program for a SlopLang feature; whenever a feature from docs/spec.md needs an end-to-end test; or whenever someone wants examples/ to cover something with exact output. Also use it when the request mentions "example", "exact output", "sample program", or exercising a language feature end to end, even if the skill isn't named.
---

# Create a Test Program

Given a SlopLang feature, produce two artifacts that stay in sync: a small program in
`examples/` that exercises the feature, and an entry in `tests/test_example_outputs.py`
that pins everything the program prints.

The split matters. `tests/test_examples.py` already checks that every `examples/*.slop`
file exits cleanly with non-empty stdout, so it catches crashes but not wrong output.
The exact-output test is what catches a change in behavior.

## 1. Read the spec for the feature

Read the relevant part of `docs/spec.md` before writing anything. It is the source of
truth for syntax, values, operators, scoping, and error formats, and it is where the
Unicode punctuation rules live. If the feature is not described there, stop and say so
rather than inventing syntax.

While reading, note the exact characters involved: strings use `“` and `”`, statements
end with `✨`, booleans are `✅` and `❌`, and comments start with `—`. Straight quotes,
`;`, and `//` are deliberately not part of the language.

## 2. Write the example

Create `examples/<feature>.slop`, where `<feature>` is a short lowercase name such as
`unary_not` or `string_escapes`. Match the existing files:

- Open with a one-line `—` comment naming what the program demonstrates.
- Focus on the single feature. A few lines that make the behavior obvious beat a long
  program; readers use these files to learn, and the tests use them as evidence.
- Prefer output that shows the result directly, for example printing each value rather
  than computing one final answer.
- Print deterministic output only. There is no input, so anything environment-dependent
  is out of bounds.

Run it before going further:

```bash
uv run sloperator.py examples/<feature>.slop
```

It must exit 0 with nothing on stderr. If it fails, either the example is wrong or the
feature is missing; find out which instead of working around it.

## 3. Capture the exact output

Do not type the expected output from memory. Trailing newlines, tabs, and blank lines
all matter, and `hallucinate()` with no arguments prints a blank line. Capture the real
bytes with Python's `repr`, which keeps the escapes readable and unambiguous:

```bash
uv run sloperator.py examples/<feature>.slop | uv run python -c 'import sys; print(repr(sys.stdin.read()))'
```

Paste that literal into the test.

## 4. Add the exact-output test

If `tests/test_example_outputs.py` does not exist, create it with this harness, which
seeds one known case so the file is obviously a table to extend:

```python
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
    "hello": "hello, slop\n",
}


@pytest.mark.parametrize(("name", "expected_stdout"), sorted(EXPECTED_OUTPUTS.items()))
def test_example_output(name: str, expected_stdout: str):
    source = (EXAMPLES / f"{name}.slop").read_text(encoding="utf-8")
    result = run_source(source)
    assert result.stderr == ""
    assert result.exit_code == 0
    assert result.stdout == expected_stdout
```

If the file already exists, add an entry to `EXPECTED_OUTPUTS` keyed by the example's
stem and leave the rest alone. If it exists in a different shape, follow that shape
instead of rewriting it; someone may have customized it on purpose.

The harness intentionally parametrizes over the table rather than over every file in
`examples/`. That keeps the suite green as new examples land, without demanding a
backfill of exact output for programs nobody has pinned yet.

## 5. Format

Apply the formatter once, after the example and test are final:

```bash
uv run ruff format
```

`AGENTS.md` asks for exactly one formatting pass per task, as the last step after code
changes. Doing it here means the files are ready for whatever checks run next, and
nobody has to reformat after a check points it out.

## 6. Run the focused tests

```bash
uv run pytest tests/test_example_outputs.py tests/test_examples.py
```

These two files are the whole scope here: they prove the example runs and that its
output matches what was captured. The rest of the project checks belong to a separate
validation step, so this skill stays a fast file-producing step on its own and drops
cleanly into a larger workflow without running anything twice.

Report what the program prints and whether the focused tests passed. If an assertion
fails, the mismatch is the interesting part: say what was expected, what came out, and
whether the example or the interpreter is wrong. Do not adjust the expectation just to
make it pass.

## When the feature is missing

If the spec documents the feature but the interpreter rejects it, that is a bug report,
not a skill failure. Say so plainly and leave the example and test out until the
interpreter is fixed; a test that documents intended behavior while failing is worse
than no test, because it hides real regressions in noise.

If fixing the interpreter is in scope, update `docs/spec.md` when behavior changes and
add regression coverage next to the affected area in `tests/`, per `AGENTS.md`.
