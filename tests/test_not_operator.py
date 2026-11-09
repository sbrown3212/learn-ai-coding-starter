import pytest

from sloperator.runner import run_source


def run(source: str) -> str:
    result = run_source(source)
    assert result.stderr == "", result.stderr
    return result.stdout


def fails(source: str) -> str:
    result = run_source(source)
    assert result.exit_code == 1
    return result.stderr.rstrip("\n")


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("!✅", "❌"),
        ("!❌", "✅"),
        ("!!✅", "✅"),
        ("!!❌", "❌"),
        ("!!!✅", "❌"),
        ("!(1 == 1)", "❌"),
        ("!✅ == ❌", "✅"),
    ],
)
def test_bang_flips_booleans(expression: str, expected: str):
    assert run(f"hallucinate({expression})✨") == f"{expected}\n"


def test_bang_works_on_variables():
    source = """slop ready = ❌✨
hallucinate(!ready)✨
hallucinate(!!ready)✨"""
    assert run(source) == "✅\n❌\n"


@pytest.mark.parametrize(
    ("expression", "type_name"),
    [
        ("1", "number"),
        ("“slop”", "string"),
    ],
)
def test_bang_rejects_non_booleans(expression: str, type_name: str):
    assert fails(f"hallucinate(!{expression})✨") == (
        f"SlopLang runtime error at line 1: operand of unary '!' must be a boolean, got {type_name}"
    )
