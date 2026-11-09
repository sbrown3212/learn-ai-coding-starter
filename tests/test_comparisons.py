from sloperator.runner import run_source


def test_equality_binds_looser_than_comparison():
    result = run_source("hallucinate(1 < 2 == ✅)✨")

    assert result.stdout == "✅\n"
    assert result.stderr == ""
    assert result.exit_code == 0
