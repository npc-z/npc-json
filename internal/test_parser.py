from typing import Union

from internal.parser import Ast, AstList, AstType, AstValue, Parser
from internal.scanner import Scanner, Token, TokenType


def make_value_ast(val: Union[int, float, str]):
    token_type = TokenType.UNKNOWN
    if isinstance(val, int):
        token_type = TokenType.INT
    elif isinstance(val, float):
        token_type = TokenType.FLOAT
    elif isinstance(val, str):
        token_type = TokenType.STRING

    return AstValue(type=AstType.VALUE, token=Token(str(val), type=token_type))


def test_parser_empty_list():
    content = "[]"
    tokens = Scanner(content).scan()
    ast = Parser(tokens).parse()

    assert ast.type == AstType.LIST
    assert ast.items == []


def test_parser_with_list_with_basic_values():
    content = """
        [1, "bob", 3.14]
    """
    tokens = Scanner(content).scan()
    ast = Parser(tokens).parse()

    assert ast.type == AstType.LIST
    assert len(ast.items) == 3
    assert ast.items == [
        make_value_ast(1),
        make_value_ast("bob"),
        make_value_ast(3.14),
    ]


def test_parser_with_list_with_additional_comma():
    content = """
        [1, "bob", 3.14,]
    """
    tokens = Scanner(content).scan()
    ast = Parser(tokens).parse()

    assert ast.type == AstType.LIST
    assert len(ast.items) == 3
    assert ast.items == [
        make_value_ast(1),
        make_value_ast("bob"),
        make_value_ast(3.14),
    ]


def test_parser_with_nested_list():
    content = """
        [
            null,
            "bob",
            [1, 3],
        ]
    """
    tokens = Scanner(content).scan()
    ast = Parser(tokens).parse()

    assert ast.type == AstType.LIST
    assert len(ast.items) == 3

    inner_list: AstList = ast.items[2]
    assert inner_list.type == AstType.LIST
    assert len(inner_list.items) == 2
