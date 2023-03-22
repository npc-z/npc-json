import pytest

from internal.scanner import InvalidCharacter, Scanner, Token, TokenType


def make_punctuation_token(punctuation: str):
    tokens = {
        "[": Token(value=punctuation, type=TokenType.LEFT_SQUARE),
        "]": Token(value=punctuation, type=TokenType.RIGHT_SQUARE),
        "{": Token(value=punctuation, type=TokenType.LEFT_CURLY),
        "}": Token(value=punctuation, type=TokenType.RIGHT_CURLY),
        ":": Token(value=punctuation, type=TokenType.COLON),
        ",": Token(value=punctuation, type=TokenType.COMMA),
        "/": Token(value=punctuation, type=TokenType.SLASH),
    }

    return tokens[punctuation]


def eof_token():
    return Token(value="", type=TokenType.EOF)


def test_scanner_with_empty_content():
    content = ""
    tokens = Scanner(content=content).scan()

    assert tokens == [eof_token()]


def test_scanner_with_some_whitespace():
    content = "     \n  \t"
    tokens = Scanner(content=content).scan()

    assert tokens == [eof_token()]


def test_scanner_with_comment():
    content = """
        // this is a comment
    """
    tokens = Scanner(content=content).scan()

    assert tokens == [eof_token()]


def test_scanner_with_punctuations():
    content = """
        []{}:,
    """
    tokens = Scanner(content=content).scan()

    assert tokens == [
        make_punctuation_token("["),
        make_punctuation_token("]"),
        make_punctuation_token("{"),
        make_punctuation_token("}"),
        make_punctuation_token(":"),
        make_punctuation_token(","),
        eof_token(),
    ]


def test_scanner_with_invalid_char():
    content = "?!@#"
    with pytest.raises(InvalidCharacter):
        Scanner(content).scan()
