from typing import Union

import pytest

from internal.scanner import (
    InvalidCharacter,
    InvalidFloat,
    InvalidString,
    Scanner,
    Token,
    TokenType,
    UnClosedQuote,
)


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


def make_int_token(value: Union[int, str]):
    return Token(value=str(value), type=TokenType.INT)


def make_float_token(value: Union[float, str]):
    return Token(value=str(value), type=TokenType.FLOAT)


def make_string_token(value: str):
    return Token(value=value, type=TokenType.STRING)


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


def test_scanner_with_int():
    content = "[12, 99]"
    tokens = Scanner(content).scan()

    assert tokens == [
        make_punctuation_token("["),
        Token(value="12", type=TokenType.INT),
        make_punctuation_token(","),
        Token(value="99", type=TokenType.INT),
        make_punctuation_token("]"),
        eof_token(),
    ]


def test_scanner_with_float():
    content = "[1.2, 33, 3.1415]"
    tokens = Scanner(content).scan()
    assert tokens == [
        make_punctuation_token("["),
        Token(value="1.2", type=TokenType.FLOAT),
        make_punctuation_token(","),
        Token(value="33", type=TokenType.INT),
        make_punctuation_token(","),
        Token(value="3.1415", type=TokenType.FLOAT),
        make_punctuation_token("]"),
        eof_token(),
    ]


def test_scanner_with_invalid_float():
    content = """
        [1, 2., 33]
    """
    with pytest.raises(InvalidFloat):
        tokens = Scanner(content).scan()


def test_scanner_with_null():
    content = """
        {1: null, [null]}
    """
    tokens = Scanner(content).scan()
    assert tokens == [
        make_punctuation_token("{"),
        make_int_token(1),
        make_punctuation_token(":"),
        Token(value="null", type=TokenType.NULL),
        make_punctuation_token(","),
        make_punctuation_token("["),
        Token(value="null", type=TokenType.NULL),
        make_punctuation_token("]"),
        make_punctuation_token("}"),
        eof_token(),
    ]


def test_scanner_with_string():
    content = """
        {"name": "bob", "age": 18, "balance": 23.3}
    """
    tokens = Scanner(content).scan()
    assert tokens == [
        make_punctuation_token("{"),
        make_string_token("name"),
        make_punctuation_token(":"),
        make_string_token("bob"),
        make_punctuation_token(","),
        make_string_token("age"),
        make_punctuation_token(":"),
        make_int_token(18),
        make_punctuation_token(","),
        make_string_token("balance"),
        make_punctuation_token(":"),
        make_float_token(23.3),
        make_punctuation_token("}"),
        eof_token(),
    ]


def test_scanner_with_unclosed_quote():
    content = """
        "abc
    """
    with pytest.raises(UnClosedQuote):
        Scanner(content).scan()


def test_scanner_with_invalid_string():
    content = """
        nulla
    """
    with pytest.raises(InvalidString):
        Scanner(content).scan()


def test_scanner_with_invalid_string():
    content = """
        "1agc
    """
    with pytest.raises(InvalidString):
        Scanner(content).scan()
