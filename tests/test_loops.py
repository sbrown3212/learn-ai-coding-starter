from sloperator.runner import run_source


def test_ralph_skips_body_when_condition_is_false():
    result = run_source("""ralph ❌ {
    hallucinate(“never”)✨
}""")

    assert result.stdout == ""
