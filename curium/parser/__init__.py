from sly import Parser as SLYParser
from typing_extensions import IntVar
from ..lexer.tokens import *
from ..lexer import Lex

from . import tree

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
            RPAREN
        ),(
            "left", 
            COMMA
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
            INCP,
            DECP,
            UPLUS,
            UMIN,
            LNOT,
            BOC
        ), ("left",
           INC,
           DEC,
           # Leave room for function call, subscript, member access
        )
    )

    
    # Assignment initialization
    @_(
        "expr COLON NAME ASSG expr",
        "expr COLON NAME ADDASSG expr",
        "expr COLON NAME SUBASSG expr",
        "expr COLON NAME MULASSG expr",
        "expr COLON NAME FLOORASSG expr",
        "expr COLON NAME DIVASSG expr",
        "expr COLON NAME MODASSG expr"
    )
    def varassginit(self,v):
        return (
            'var-assign-init',
            v[3],
            v[0],
            v[2],
            v[4]
        )




    # Add a rule for every binary operator
    @_(
        "expr LAND expr", # Logical ops
        "expr LOR expr",
        "expr LNOT expr",
        "expr BAND expr", # Bitwise ops
        "expr BOR expr",
        "expr BXOR expr",
        "expr BOC expr",
        "expr BLS expr",
        "expr BRS expr",
        "expr EQU expr", # Comparison operators are binary too
        "expr NEQU expr",
        "expr LTGT expr",
        "expr GT expr",
        "expr LT expr",
        "expr GTEQ expr",
        "expr LTEQ expr",
        
        "expr ADD expr", # Finaly mathematical operators
        "expr SUB expr",
        "expr MUL expr",
        "expr DIV expr",
        "expr MOD expr",
        "expr FLOORDIV expr" # Thats all for now
    )
    def expr(self, v):
        return (
            "binary-expression",
            v[1],
            v.expr0,
            v.expr1
        )
    
    
    
    
    
    # Unary operators
    @_(
        "INC expr %prec INCP",
        "DEC expr %prec DECP",
        "ADD expr %prec UPLUS",
        "SUB expr %prec UMIN"
    )
    def expr(self,v):
        return (
            "unary-expr",
            v[0],
            v[1]
        )
    
    
    # Types


    @_("ltype","func")
    def expr(self,v):
        return (
            'literal',
            v[0]
        )

    # Function type
    @_('LPAREN expr RPAREN LBRACE expr RBRACE')
    def func(self,v):
        return (
            'function-type',
            v[1],
            v[4]
        )
    # Function type
    @_('LPAREN RPAREN LBRACE expr RBRACE')
    def func(self,v):
        return (
            'function-type',
            ('empty-type'),
            v[4]
        )

    @_(
        "HEXIDECIMAL",
        "DECIMAL",
        "BINARY",
        "OCTAL"
    )
    def ltype(self,v):
        return (
            "integer-literal",
            v[0]
        )
    
    @_('STRING')
    def ltype(self,v):
        return (
            'string-literal',
            v[0]
        )
    
    
    @_('NAME LBRACK ltype RBRACK')
    def ltype(self,v):
        return (
            'name-literal-tagged',
            v[0],
            v[1]
        )

    
    # Regular, non tagged names
    @_('NAME')
    def ltype(self,v):
        return (
            'name-literal',
            v[0]
        )
    
    def find_column(self, text, token):
        last_cr = text.rfind('\n', 0, token.index)
        if last_cr < 0:
            last_cr = 0
        column = (token.index - last_cr) + 1
        return column
    
    def error(self,t):
        col = self.find_column(self.text,t)
        line = self.text.split("\n")[t.lineno-1]
        print(line)
        print(f'{" "*(col-1)}^')
        print(f"Syntax error at line {t.lineno} col {col}:")
        print(f"\tUnexpected token \"{t.value}\"")
        

    