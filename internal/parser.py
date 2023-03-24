from dataclasses import dataclass
from typing import List, Optional

from internal.exception import EatUnexpectedTokenType, UnknownJSONType
from internal.scanner import Token, TokenType


class AstType:
    EMPTY = "empty"
    LIST = "list"
    OBJECT = "object"
    VALUE = "value"


@dataclass
class Ast:
    type: AstType


@dataclass
class AstValue(Ast):
    token: Token


@dataclass
class AstList(Ast):
    items: List[Ast]


class Parser:
    def __init__(self, tokens: List[Token]) -> None:
        self._tokens = tokens
        self._next_pos = 0
        self.next_token = self._tokens[self._next_pos]

    def peek(self):
        token = self.next_token
        if not self.at_end():
            return self._tokens[self._next_pos + 1]

        return token

    def at_end(self):
        return self.next_token.type == TokenType.EOF

    def advance(self):
        if not self.at_end():
            self._next_pos += 1
            self.next_token = self._tokens[self._next_pos]

    def eat(self, expected_token_type: TokenType):
        if self.next_token.type == expected_token_type:
            self.advance()
            return

        raise EatUnexpectedTokenType(
            f"Expected {expected_token_type}, but got {self.next_token.type}"
        )

    def parse(self):
        token = self.next_token

        if token.type in [
            TokenType.INT,
            TokenType.FLOAT,
            TokenType.STRING,
            TokenType.NULL,
        ]:
            return self.parse_value()

        if token.type == TokenType.LEFT_SQUARE:
            return self.parse_list()

        if token.type == TokenType.EOF:
            return Ast(type=AstType.EMPTY)

    def parse_list(self) -> AstList:
        self.eat(TokenType.LEFT_SQUARE)
        items: List[Ast] = self.parse_list_items()
        ast = AstList(type=AstType.LIST, items=items)

        return ast

    def parse_list_items(self):
        items = []

        # empty list
        if self.next_token.type == TokenType.RIGHT_SQUARE:
            self.eat(TokenType.RIGHT_SQUARE)
            return items

        # has at least one item
        items.append(self.parse())

        while (
            self.next_token.type == TokenType.COMMA
            and self.peek().type != TokenType.RIGHT_SQUARE
        ):
            self.eat(TokenType.COMMA)
            item = self.parse()
            items.append(item)

        # have one "," and only one
        if self.next_token.type == TokenType.COMMA:
            self.eat(TokenType.COMMA)

        self.eat(TokenType.RIGHT_SQUARE)

        return items

    def parse_value(self):
        token = self.next_token

        if token.type == TokenType.INT:
            self.eat(TokenType.INT)
            return AstValue(type=AstType.VALUE, token=token)

        if token.type == TokenType.FLOAT:
            self.eat(TokenType.FLOAT)
            return AstValue(type=AstType.VALUE, token=token)

        if token.type == TokenType.STRING:
            self.eat(TokenType.STRING)
            return AstValue(type=AstType.VALUE, token=token)

        if token.type == TokenType.NULL:
            self.eat(TokenType.NULL)
            return AstValue(type=AstType.VALUE, token=token)


"""
npc-json ->
    list | object | empty

list ->
    empty-list
    | "[" npc-json ( "," npc-json )* ","+ "]"

empty-list -> "[" "]"

AST-VALUE ->
    int | float | string | null
"""
