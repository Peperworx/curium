from re import match
from sly import Parser as SLYParser
from typing_extensions import IntVar
from ..lexer.tokens import *
from .lexer import Lex

_ = lambda *v: v

class Parse(SLYParser):
    tokens = Lex.tokens

    # Precedences
    precedence = (
        # Literals
        ("nonassoc", 
            DECIMAL,
            HEXIDECIMAL,
            OCTAL,
            BINARY,
            STRING,
            NAME,
            RETURN,
            LPAREN,
            RPAREN,
            
        ),(
            "left", 
            COMMA,
            COLON
        )
    )

    @_("label NEWLINE","instruction NEWLINE")
    def line(self,v):
        return (
            'line', 
            v[0]
        )
    
    @_("instruction NEWLINE instruction")
    def line(self,v):
        return (
            'line-list',
            v[0],
            v[2]
        )

    @_("NAME COLON")
    def label(self,v):
        return (
            'label',
            v[0],
            v.lineno,
            v.index
        )
    
    @_("NAME expr")
    def instruction(self,v):
        return (
            'instruction',
            v[0],
            v[1],
            v.lineno,
            v.index
        )
    
    @_(
        "HEXIDECIMAL",
        "DECIMAL",
        "BINARY",
        "OCTAL"
    )
    def integer(self,v):
        return v[0]

    @_("LBRACK integer RBRACK")
    def expr(self,v):
        return (
            "pointer",
            v[1]
        )
    
    @_("integer")
    def expr(self,v):
        # Resolve this integer into a decimal
        dec = None
        if v[0].startswith("0x"):
            dec = int(v[0][2:],16)
        print(dec)
        return (
            "integer_type",
            v[0]
        )
    
    def find_column(self, text, token):
        last_cr = text.rfind('\n', 0, token.index)
        if last_cr < 0:
            last_cr = 0
        column = (token.index - last_cr) + 1
        return column
    
    def error(self,t):
        if not t:
            print("EOF Error!")
        else:
            col = self.find_column(self.text,t)
            line = self.text.split("\n")[t.lineno-1]
            print("|"+"-"*max(len(line),50))
            print("|",line)
            print(
                f'|{" " * (col - 1)}{"^" * len(t.value)}'
            )
            print(f"| Syntax error at line {t.lineno} col {col-1}:")
            print(f"| \tUnexpected token \"{t.value}\"")
            print("|\n")

    