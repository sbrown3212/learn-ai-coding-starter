# Agent instructions

Sloperator is a Python 3.13 tree-walking interpreter for SlopLang, a joke language
whose syntax uses Unicode punctuation. `docs/spec.md` is the language source of
truth; update it when changing language behavior.

## Commands

Use `uv run` for Python entrypoints; the project requires Python 3.13.

- Run a program: `uv run sloperator.py path/to/program.slop`
- Check syntax only: `uv run sloperator.py --check path/to/program.slop`
- Playground: `uv run playground/server.py` (defaults to `127.0.0.1:8080`; optional port arg)
- Validate (repo `validate` skill): `uv run pytest`, then `uv run ruff format --check`,
  then `uv run ruff check`
- `README.md` also lists `uv run ty check`; the validate skill does not run it.
- One test: `uv run pytest tests/test_parser.py::test_function_declaration`

## Architecture and invariants

- `sloperator.py` is the CLI. `sloperator/runner.py` wires
  `tokenize -> parse -> Interpreter` and exposes `run_source`, which returns
  `RunResult(stdout, stderr, exit_code)` for tests.
- Stages live in `sloperator/lexer/`, `parser/`, and `evaluator/`. All diagnostics
  are `SlopError` subclasses carrying a 1-based line; the runner catches them, and
  the CLI prints them to stderr and exits 1 (2 for usage/unreadable files). Do not
  let Python tracebacks escape.
- `docs/spec.md` defines values, scoping, operators, and grammar. Tests assert exact
  error lines and messages, so change code, tests, and spec together.
- `hallucinate` is an identifier bound to a builtin, not a keyword. Conditions
  require actual booleans, and Python `bool` must not be treated as a number.
- Only top-level `clanker` declarations are allowed, and `ship` is valid only inside
  one. Call depth is capped at 500 with a `stack overflow` runtime error.
- Known spec/code divergence: the parser nests `equality` inside `comparison`, so
  `==` binds tighter than `<`; `docs/spec.md` says the opposite. Confirm intent
  before changing precedence.

## SlopLang gotchas

- Statements end with `✨`; strings use `“ ”`; comments use `—`; booleans are
  `✅`/`❌`.
- The lexer deliberately rejects ASCII substitutes (`"`, `;`, `//`, `–`) with
  helpful messages. Preserve those messages.
- Numbers are arbitrary-precision ints (no floats); division truncates toward zero;
  `+` concatenates only string + string; there are no implicit conversions.

## Testing

- `tests/test_examples.py` auto-discovers `examples/*.slop`. Every example must run
  with no stderr, exit 0, and print non-empty stdout; make new examples print
  something.
- Tests call `run_source(...)` and assert exact stdout, stderr, and exit codes. CLI
  tests spawn `sys.executable sloperator.py` in a subprocess.
- Add error cases to `tests/test_errors.py` or `tests/test_parser.py` with the exact
  message and line the interpreter should produce.

## OpenCode setup

- Prefer the `run_slop` tool over shell for `.slop` files; it wraps
  `uv run --no-active sloperator.py` (`.opencode/plugins/run-slop.ts`).
- `.env` and `.env.*` reads are denied by `opencode.jsonc`; do not attempt them.
- Shell commands require approval except `bootdev run *`. The shell scanner checks
  each command in a compound command separately, so an extra command in a pipeline
  or `&&` chain triggers an approval prompt even when the first command is allowed.
  - Run `bootdev run <lesson-uuid>` as a bare command. Do not pipe it through
    `tail`, `head`, `grep`, or chain it with `|`, `&&`, or `;`.
  - Tool output is already truncated automatically and the full result is saved to
    a file, so piping to shorten output is unnecessary.
  - Keep other allowed commands as a single command when an approval prompt should
    be avoided.
