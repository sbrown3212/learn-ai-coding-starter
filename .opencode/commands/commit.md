---
description: Review changes, commit them, then rebase onto origin/main
---

Commit the current project changes using `$ARGUMENTS` as the commit message.

If `$ARGUMENTS` is empty, stop and ask for a message rather than inventing one.

1. Review before staging anything. Run `git status --short`, `git diff`, and
   `git diff --staged`, and read what actually changed. The point is to catch files that
   should not be in the commit — editor state, caches, `.env` files, unrelated edits —
   before they land in history.

2. Stage the reviewed changes with `git add <paths>`. Reach for `git add -A` only when
   everything in the worktree genuinely belongs in this one commit; otherwise name the
   paths so unrelated work stays out.

3. Commit with the exact message: `git commit -m "$ARGUMENTS"`. Do not append a body,
   trailers, or co-author lines that were not asked for.

4. Rebase onto the remote: `git pull --rebase origin main`.

5. Report the new commit hash and the outcome of the pull. If the rebase stops on
   conflicts, name the conflicting files and stop there; do not resolve them silently.

Do not push. This command ends after the rebase.
