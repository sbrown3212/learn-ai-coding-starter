from sloperator.runner import run_source


def run(source: str) -> str:
    result = run_source(source)
    assert result.stderr == "", result.stderr
    assert result.exit_code == 0
    return result.stdout


def test_call_used_directly_as_an_argument_to_another_call():
    source = """clanker double(n) {
    ship n * 2✨
}
clanker add(left, right) {
    ship left + right✨
}
hallucinate(add(double(3), double(4)))✨"""
    assert run(source) == "14\n"
