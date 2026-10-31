import pytest

from sloperator.errors import LexicalError
from sloperator.lexer import tokenize


def test_unexpected_character_is_a_lexical_error():
    with pytest.raises(LexicalError) as info:
        tokenize("$")
    assert info.value.line == 1
    assert info.value.message == "unexpected character '$'"
    assert str(info.value) == "SlopLang lexical error at line 1: unexpected character '$'"
