# Agent instructions

Sloperator is a Python 3.13 tree-walking interpreter for SlopLang, a small language
with Unicode syntax.

## Project layout

- `sloperator.py` — CLI for running or syntax-checking a `.slop` file.
- `sloperator/` — lexer, parser, and evaluator; `runner.py` wires the stages together.
- `examples/` — sample `.slop` programs, all exercised by the test suite.
- `tests/` — pytest suite covering the CLI, lexer, parser, evaluator, and examples.
- `playground/` — local web playground in `playground/server.py`.
- `docs/spec.md` — the language specification.

## Validation

Run these four commands from the project root:

1. `uv run pytest`
2. `uv run ruff format --check`
3. `uv run ruff check`
4. `uv run ty check`

Apply formatting with `uv run ruff format` exactly once per task, as the last step
after all code changes are complete. Do not run the formatter after each edit, so it
is not executed repeatedly throughout a single change. Then run the validation
commands above to confirm nothing would change.

## Regression tests

Add a regression test whenever you fix a bug or change observable behavior. Put it
next to the affected area (`tests/test_lexer*`, `tests/test_parser.py`,
`tests/test_evaluator.py`, or `tests/test_cli.py`) and assert exact output, line
numbers, and error messages. New `examples/*.slop` files are picked up automatically
by `tests/test_examples.py`, which requires a clean exit and non-empty stdout.

For comparison or equality precedence changes, run the focused suite with
`uv run pytest tests/test_comparisons.py`.

## Language behavior

See [docs/spec.md](docs/spec.md) for syntax, values, operators, scoping, control flow,
and error formats. It is the source of truth; update it when language behavior changes.
