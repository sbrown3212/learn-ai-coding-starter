# Sloperator

A tree-walking Python interpreter for [SlopLang](docs/spec.md).

## Quick Start

```bash
uv run sloperator.py examples/fib.slop           # run a program
uv run sloperator.py --check examples/fib.slop   # check syntax only
uv run playground/server.py                      # playground at localhost:8080
```

## Validation

```bash
uv run pytest              # tests
uv run ruff format --check # formatting
uv run ruff check          # linting
uv run ty check            # type checking
```

## Language Reference

The complete language — words, values, scopes, control flow, operators,
grammar, and errors — is specified in [docs/spec.md](docs/spec.md).

```slop
clanker describe(count) {
    vibe count > 1 { ship “big slop”✨ }
    ship “small slop”✨
}
hallucinate(describe(3))✨   — big slop
```

## Layout

`sloperator.py` is the CLI, `sloperator/runner.py` runs source through all
stages, and `sloperator/` holds the lexer, parser, and evaluator. Example
programs live in `examples/`, tests in `tests/`, and the web playground in
`playground/`.
