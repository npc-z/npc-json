from dataclasses import dataclass
from enum import Enum
from typing import List

from internal.utils import log


class NPCJSONException(Exception):
    pass


class InvalidCharacter(NPCJSONException):
    ...


class TokenType(Enum):
    INT = "int"
    FLOAT = "float"
    STRING = "string"
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
