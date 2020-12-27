from sly import Parser as SLYParser
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
            NAME
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
            p[1],
            p.expr0,
            p.expr1
        )
    
    # Add a rule for assignment operators
    @_(
        "expr ASSG expr", # Asignment operators are to
        "expr ADDASSG expr",
        "expr SUBASSG expr",
        "expr MULASSG expr",
        "expr DIVASSG expr",
        "expr MODASSG expr",
        "expr FLOORASSG expr",
    )
    def assg(self,v):
        return (
            "assignment-operator",
            v[1],
            v[0],
            v[3]
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
    
    # A rule for parentheses
    @_("LPAREN expr RPAREN")
    def expr(self,v):
        return ("group-expr",v[1])
    

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
    
    # Time for name rules!

    # Names can be assigned templates
    # For this we need tuples

    # So here is a rule for tuples
    @_(
        "expr COMMA tuple",
        "COMMA"
    )   
    def tuple(self,v):
        return (
            "tuple-literal",
            v.text
        )
    # And here is the actual rule
    @_(
        "tuple"
    )
    def expr(self,v):
        return v[0]
    

    # Now for names

    # Basic name
    @_(
        "NAME LBRACK expr RBRACK"
    )
    def name(self,v):
        return (
            "name-literal",
            v.NAME,
            v.name
        )
    
    # And the actual expression
    @_("name")
    def expr(self,v):
        return v