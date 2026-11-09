# Parser package instructions

`sloperator/parser/` is a recursive-descent parser that turns `list[Token]` into a
`Program`. The grammar in `docs/spec.md` is the source of truth.

## Conventions

- **One method per grammar rule.** Name methods after the rule (`logic_or`,
  `logic_and`, `comparison`, `term`, `factor`, `unary`, `call`, `primary`, etc.).
  Do not fold adjacent precedence levels or multiple productions into one method.
  Keep the repetition inside the rule method (for example, `factor` handles its own
  `*`/`/` loop) rather than splitting the rule into a `_tail` helper.
- **Syntax errors must say what token was found.** For unexpected tokens, raise
  through `self.error(token, message)`, which appends `, found '<lexeme>'`; at EOF it
  appends `, but reached end of file` instead. Contextual errors (duplicate
  parameter, `ship` outside a function, nested `clanker`) may raise
  `SlopSyntaxError` directly, but still include the relevant lexeme and line.

## Invariants

- `parse(tokens)` is the only entrypoint and returns `list[Stmt]`.
- AST nodes are frozen dataclasses in `ast.py`; use tuples for fixed sequences
  (parameters and arguments).
- `ship` is valid only inside a `clanker`; nested `clanker` declarations are syntax
  errors. Track this with `function_depth`.
- Error text is part of the contract. `tests/test_parser.py` asserts the exact line
  and message, and CLI tests assert the formatted diagnostic.
- Keep precedence order matching `docs/spec.md`: `logic_and` delegates to `equality`,
  which delegates to `comparison`, which delegates to `term`.

## Validation

- Parser tests: `uv run pytest tests/test_parser.py`
- Comparison tests: `uv run pytest tests/test_comparisons.py`
- Error-message tests: `uv run pytest tests/test_errors.py`
- Full check: `uv run pytest`
