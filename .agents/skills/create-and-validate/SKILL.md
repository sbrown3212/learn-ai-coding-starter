---
name: create-and-validate
description: Add a SlopLang example program with an exact-output test, then run the project's full validation suite. Use this when the user wants a feature covered end to end — "add an example and validate", "write a test program and make sure everything passes", or any request that combines documenting a language feature with running the checks. Also use it when someone asks for one command that creates the example and proves the repo is still green.
---

# Create and Validate

This skill is a pipeline over two existing skills. It owns the handoff between them,
not their instructions: producing the example and its exact-output test lives in
`create-test-program`, and the project-wide checks live in `validate`. If either skill
changes, this one keeps working without edits.

## 1. Load `create-test-program`

Load the `create-test-program` skill and follow it to produce `examples/<feature>.slop`
and its entry in `tests/test_example_outputs.py`.

Loading it may prompt for approval, because `opencode.jsonc` marks that skill as
`ask`. That is expected; the permission exists so a human confirms before the skill
runs.

`create-test-program` ends by applying the formatter and running its focused two-file
pytest run. It does not run the project-wide checks — those belong to `validate`, which
you load next.

If `create-test-program` says the feature is missing from the interpreter, stop here
and report that. Validating a knowingly failing example just buries the real problem
in noise.

## 2. Load `validate`

Load the `validate` skill and follow it to run the project checks and report which
passed and which failed.

Do this only after the example and test are in place, so the formatting check and the
full pytest run see the final files. If something fails, report the failure first, as
`validate` instructs, and do not edit the expected output just to make the test pass.

## What to report

Name the example and the output it pins, then give the pass/fail result of each
validation check. Keep it short: the user wants to know what was added and whether the
repo is green.
