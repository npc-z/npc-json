from typing import List
from enum import Enum


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


class Token:
    def __init__(self, value: str, token_type: TokenType) -> None:
        self.value: str = value
        self.token_type: TokenType = token_type


def scanner(content: str) -> List[Token]:
    ...
