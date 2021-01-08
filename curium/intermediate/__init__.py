from sly import Lexer as SlyLexer
from rich import print
import os

# Pylance errors go byby
_ = lambda v: print(v)

class Lexer(SlyLexer):
    tokens = {
        NAME,
        LPAREN, RPAREN,
        LBRACE, RBRACE,
        LBRACK, RBRACK,
        PCT,
        COMMA,
        COLON,
        SEMICOLON
    }

    # Ignore spaces and tabs.
    ignore = ' \t'

    # Names
    NAME = r"[a-zA-Z_][a-zA-Z0-9_]*"

    # Parentheses and brackets
    LPAREN = r'\('
    RPAREN = r'\)'
    LBRACE = r'\{'
    RBRACE = r'\}'
    LBRACK = r'\['
    RBRACK = r'\]'

    # Percent symbol
    PCT = r"%"

    # Comma
    COMMA = r','

    # Colon and semicolon
    COLON = r':'
    SEMICOLON = r';'


    # Decimal Integers
    @_(r"[0-9]+")
    def decimal(self, v):
        v.value = int(v.value)
        return v

    # Newlines should increment lineno
    @_('\n')
    def newline(self, v):
        self.lineno += len(v.value)