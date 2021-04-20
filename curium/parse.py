from sly import Parser
from . import lex as clex
from .tokens import *

class CuriumParser(Parser):
    # Grab tokens from lexer
    tokens = clex.CuriumLexer.tokens

    @_("DEF NAME LPAREN RPAREN ARROW name LBRACE statements RBRACE")
    def function_def(self,v):
        return v

    @_("statement", "statement statements")
    def statements(self,v):
        return v

    @_("RETURN expr SEMICOLON")
    def statement(self, v):
        return ("return", v[1])
    
    @_("expr SEMICOLON")
    def statement(self,v):
        return v[0]

    # Type
    @_("number","string","name")
    def expr(self,v):
        return v[0]

    # Numbers
    @_("HEXIDECIMAL","OCTAL","BINARY","DECIMAL")
    def number(self,v):
        
        if v[0].startswith("0x"):
            return int(v[0][2:],16)
        elif v[0].startswith("0o"):
            return int(v[0][2:],8)
        elif v[0].startswith("0b"):
            return int(v[0][2:],2)
        else:
            return int(v[0])

    # Strings
    @_("STRING")
    def string(self, v):
        return v[0]

    # Names
    @_(
        "NAME",
        "CHAR",
        "UCHAR",
        "SHORT",
        "USHORT",
        "INT",
        "UINT",
        "LONG",
        "ULONG",
        "FLOAT",
        "DOUBLE"
        )
    def name(self,v):
        return v[0]