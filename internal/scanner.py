from dataclasses import dataclass
from enum import Enum
from typing import List

from internal.utils import log


class NPCJSONException(Exception):
    pass


class InvalidCharacter(NPCJSONException):
    ...


class InvalidFloat(NPCJSONException):
    ...


class InvalidString(NPCJSONException):
    ...


class UnClosedQuote(NPCJSONException):
    ...


class TokenType(Enum):
    INT = "int"
    FLOAT = "float"
    STRING = "string"
    NULL = "null"
    LEFT_CURLY = "{"
    RIGHT_CURLY = "}"
    LEFT_SQUARE = "["
    RIGHT_SQUARE = "]"
    COMMA = ","
    COLON = ":"
    SLASH = "/"
    EOF = "eof"


@dataclass(frozen=True, unsafe_hash=True)
class Token:
    value: str
    type: TokenType


class Scanner:
    small_alphas = "abcdefghijklmnopqrstuvwxyz"
    capital_alphas = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    alphas = small_alphas + capital_alphas
    numbers = "0123456789"
    valid_string_starter = alphas + "_"
    valid_string = alphas + numbers + "_"

    def __init__(self, content: str) -> None:
        self.content = content
        self.pos = 0
        self.length = len(content)
        self.tokens: List[Token] = []
        self.char = self.content[self.pos] if self.length > 0 else ""

    def next_token(self) -> Token:
        if self.pos >= self.length:
            return Token(value="", type=TokenType.EOF)

        if self.is_whitespace(self.char):
            self.skip_whitespace()
            return self.next_token()

        if self.char == "/" and self.peek() == "/":
            self.skip_comment()
            return self.next_token()

        if self.is_digit(self.char):
            return self.parse_number()

        if self.char == "n":
            return self.parse_null()

        if self.char == '"':
            return self.parse_string()

        if self.char == "[":
            self.advance()
            return Token(value="[", type=TokenType.LEFT_SQUARE)
        if self.char == "]":
            self.advance()
            return Token(value="]", type=TokenType.RIGHT_SQUARE)
        if self.char == "{":
            self.advance()
            return Token(value="{", type=TokenType.LEFT_CURLY)
        if self.char == "}":
            self.advance()
            return Token(value="}", type=TokenType.RIGHT_CURLY)
        if self.char == ":":
            self.advance()
            return Token(value=":", type=TokenType.COLON)
        if self.char == ",":
            self.advance()
            return Token(value=",", type=TokenType.COMMA)

        raise InvalidCharacter(f"Invalid char ({self.char})")

    def scan(self) -> List[Token]:
        token = self.next_token()
        self.tokens.append(token)
        while token.type != TokenType.EOF:
            token = self.next_token()
            self.tokens.append(token)

        return self.tokens

    def advance(self):
        self.pos += 1
        self.char = self.content[self.pos] if self.pos < self.length else ""

    def peek(self):
        if self.pos + 1 < self.length:
            return self.content[self.pos + 1]

        return ""

    def skip_whitespace(self):
        while self.pos < self.length and self.is_whitespace(self.char):
            self.advance()

    @staticmethod
    def is_whitespace(char: str):
        return char == " " or char == "\n" or char == "\t"

    def skip_comment(self):
        # eat the "//"
        self.advance()
        self.advance()
        while self.pos < self.length and self.char != "\n":
            self.advance()

    def is_digit(self, char: str):
        return char in self.numbers

    def is_alpha(self, char: str):
        return char in self.alphas

    def is_alpha_digit(self, char: str):
        return self.is_digit(char) or self.is_alpha(char)

    def parse_number(self):
        n = self.char
        self.advance()
        while self.pos < self.length and self.is_digit(self.char):
            n += self.char
            self.advance()

        if self.char == ".":
            if not self.is_digit(self.peek()):
                raise InvalidFloat()

            n += self.char
            self.advance()
            while self.pos < self.length and self.is_digit(self.char):
                n += self.char
                self.advance()
            return Token(value=n, type=TokenType.FLOAT)
        else:
            return Token(value=n, type=TokenType.INT)

    def parse_null(self):
        s = self.char
        self.advance()
        while self.pos < self.length and self.is_alpha_digit(self.char):
            s += self.char
            self.advance()

        if s == TokenType.NULL.value:
            return Token(value=s, type=TokenType.NULL)

        raise InvalidString(s)

    def parse_string(self):
        self.advance()
        s = ""
        if self.char in self.valid_string_starter:
            s += self.char
            self.advance()
        else:
            raise InvalidString()

        while (
            self.pos < self.length
            and self.char in self.valid_string
            and self.char != '"'
        ):
            s += self.char
            self.advance()

        if self.char != '"':
            raise UnClosedQuote()

        self.advance()
        return Token(value=s, type=TokenType.STRING)
