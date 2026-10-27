# Agent instructions

## Shell commands

Shell commands require approval except `bootdev run *` (see `opencode.jsonc`). The
shell scanner checks each command in a compound command separately, so an extra
command in a pipeline or `&&` chain triggers an approval prompt even when the
first command is allowed.

- Run `bootdev run <lesson-uuid>` as a bare command. Do not pipe it through
  `tail`, `head`, `grep`, or chain it with `|`, `&&`, or `;`.
- Tool output is already truncated automatically and the full result is saved to
  a file, so piping to shorten output is unnecessary.
- The same applies to other allowed commands: keep them as a single command when
  an approval prompt should be avoided.
