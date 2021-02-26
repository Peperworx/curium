from re import match
from sly import Parser as SLYParser
from ..lexer.tokens import *
from ..lexer import Lex
from . import tree
import sys

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
            SEMICOLON,
        ),("right",
            COMMA,
        ),("right",
            ASSG,
            ADDASSG,
            SUBASSG,
            MULASSG,
            DIVASSG,
            MODASSG,
            FLOORASSG
        ), ("left",
            LOR
        ), ('left',
            LAND
        ), ("left",
            BOR
        ), ("left",
            BXOR
        ), ("left",
            BAND
        ), ("left",
            EQU,
            NEQU,
            LTGT
        ), ("left",
            LT,
            LTEQ,
            GT,
            GTEQ
        ), ("left",
            BLS,
            BRS
        ), ("left",
            ADD,
            SUB
        ), ("left",
            MUL,
            DIV,
            MOD,
            FLOORDIV
        ), # Space for a bunch more here
        # (pointer-to-member, cast, indirection, addr, new, del, etc)
        ("right",
            #INCP,
            #DECP,
            #UPLUS,
            #UMIN,
            LNOT,
            BOC,
            #INDIRECTION,
            #ADDR
        ), ("left",
           INC,
           DEC,
           # Leave room for function call, subscript, member access
        ),
    )

    # An entire file is a list of statements

    @_("statement SEMICOLON statements")
    def statements(self, v):
        out = [v[0]]
        out.extend(v[2].statements)
        return tree.namespace(
            out
        )
    @_("statement SEMICOLON")
    def statements(self, v):
        out = [v[0]]
        return tree.namespace(
            out
        )
    
    @_("statement")
    def statements(self, v):
        out = [v[0]]
        return tree.namespace(
            out
        )
    
    @_("expr")
    def statement(self,v):
        return tree.expr_statement(
            v[0],v[0].lineno,v[0].index
        )
    
    
    # Expressions

    @_("integer_literal")
    def expr(self,v):
        return v[0]
    

    # Basic literals

    # Integers first
    @_("HEXIDECIMAL",
        "OCTAL",
        "BINARY",
        "DECIMAL")
    def integer_literal(self,v):
        return tree.integer_literal(v[0],v.lineno,v.index)
    
    
    
    
    

    def find_column(self, text, token):
        last_cr = text.rfind('\n', 0, token.index)
        if last_cr < 0:
            last_cr = 0
        column = (token.index - last_cr) + 1
        return column
    
    def error(self,t):
        if t:
            col = self.find_column(self.text,t)
            line = self.text.split("\n")[t.lineno-1]
            print("|"+"-"*max(len(line),50))
            print("|",line)
            print(
                f'|{" " * (col)}{"^" * len(t.value)}'
            )
            print(f"| Syntax error at line {t.lineno} col {col-1}:")
            print(f"| \tUnexpected token \"{t.value}\"")
            print("|\n")
        else:
            print("|"+"-"*50)
            print("| End of file error")
        sys.exit()
        

    