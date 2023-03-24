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


class UnknownJSONType(NPCJSONException):
    ...


class EatUnexpectedTokenType(NPCJSONException):
    ...
