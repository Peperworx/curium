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

    @_('expr SEMICOLON')
    def statement(self,v):
        return v[0]

    # Function calls
    @_('name LPAREN RPAREN')
    def statement(self,v):
        return (
            'function-call',
            v[0],
            ""
        )
    # Function calls
    @_('name LPAREN expr RPAREN')
    def statement(self,v):
        return (
            'function-call',
            v[0],
            v[2]
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
    
    


    # A rule for integer and string
    @_(
        "HEXIDECIMAL",
        "DECIMAL",
        "BINARY",
        "OCTAL"
    )
    def expr(self,v):
        return (
            "integer-literal",
            v[0]
        )
    
    @_('STRING')
    def expr(self,v):
        return (
            'string-literal',
            v[0]
        )
    
    
    # Rules for names
    @_("NAME LBRACK expr RBRACK")
    def name(self,v):
        return (
            'name-literal-template',
            v[0],
            v[2]
        )
    
    @_("NAME")
    def name(self,v):
        return (
            'name-literal',
            v[0]
        )
    
    @_("name")
    def expr(self,v):
        return v
    
    # Function definitions
    @_('LPAREN RPAREN LBRACE expr RBRACE')
    def expr(self,v):
        return (
            'function-def',
            "",
            v[3]
        )
    @_('LPAREN expr RPAREN LBRACE expr RBRACE')
    def expr(self,v):
        return (
            'function-def',
            v[1],
            v[4]
        )
    
    
    
    # Assignment expressions

    @_(
        "name COLON name ASSG expr", # Asignment operators are to
        "name COLON name ADDASSG expr",
        "name COLON name SUBASSG expr",
        "name COLON name MULASSG expr",
        "name COLON name DIVASSG expr",
        "name COLON name MODASSG expr",
        "name COLON name FLOORASSG expr"
    )
    def expr(self,v):
        return (
            'assign',
            v[0],
            v[1],
            v[2]
        )

    @_(
        "name ASSG expr", # Asignment operators are to
        "name ADDASSG expr",
        "name SUBASSG expr",
        "name MULASSG expr",
        "name DIVASSG expr",
        "name MODASSG expr",
        "name FLOORASSG expr"
    )
    def expr(self,v):
        return (
            'assign',
            v[0],
            v[1],
            v[2]
        )
    


    
    
    
    
    
    # A rule for parentheses
    @_("LPAREN expr RPAREN")
    def expr(self,v):
        return ("group-expr",v[1])
    

    
    
    
    
    
