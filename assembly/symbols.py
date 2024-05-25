from enum import Enum, auto


class Symbol(Enum):
    EOF = auto()
    EMPTY = auto()

    # Parser Types
    nonterminal = auto()
    optional = auto()
    token = auto()

    # Parser Symbols
    REPEAT = auto()
    LPAREN = auto()
    RPAREN = auto()
    NOT = auto()
    OR = auto()
    OPT = auto()
