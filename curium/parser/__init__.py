from sly import Parser as SLYParser
from ..lexer.tokens import *
from ..lexer import Lex

from . import tree

_ = ""

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
        return tree.BinOp(v[1],v[0],v[2],v.lineno,v.index)
    
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
        return tree.BinOp(v[1],v[0],v[2],v.lineno,v.index)
    # Prefix operators
    @_(
        "INC expr %prec INCP",
        "DEC expr %prec DECP",
        "ADD expr %prec UPLUS",
        "SUB expr %prec UMIN"
    )
    def expr(self,v):
        return tree.UnOp(v[0],v[1],v.lineno,v.index)

    @_('LPAREN expr RPAREN')
    def expr(self, v):
        return v.expr
    
    # Rule for variable initialization
    @_("NAME COLON NAME SEMICOLON")
    def expr(self,v):
        return tree.Initialize(
            v[2],
            v[0],
            None,
            v.lineno,
            v.index
        )
    
    # Rule for variable declaration
    @_("NAME COLON NAME SEMICOLON assg expr")
    def expr(self,v):
        return tree.Initialize(
            v[2],
            v[0],
            v[5],
            v.lineno,
            v.index
        )

    # Rule for name templates
    

    @_("NAME LBRACK nametemp RBRACK")
    def nametemp(self,v):
        return tree.Name(
            v[0],
            v[2],
            v.lineno,
            v.index
        )

    # Rule for variable assignent
    @_("NAME assg expr")
    def expr(selv,v):
        return tree.BinOp(v[1],v[0],v[2])

    # All Numbers
    @_(
        "DECIMAL",
        "HEXIDECIMAL",
        "OCTAL",
        "BINARY"
    )
    def expr(self,v):
        # Return a number object
        return tree.Number(v[0],v.lineno,v.index)
    
    # All Strings
    @_("STRING")
    def expr(self,v):
        return tree.String(v[0],v.lineno,v.index)
    
    # All Names (Except conditionals)
    @_("NAME")
    def expr(self,v):
        return tree.Name(v[0],v.lineno,v.index)
    
    # Subscript
    @_("expr LBRACK expr RBRACK")
    def expr(self,v):
        return tree.BinOp("[]",v[0],v[2])
    

    

    # Conditional
    @_("conditional")
    def expr(self,v):
        return v
    
    @_("IF LPAREN expr RPAREN LBRACE expr RBRACE elseorif")
    def conditional(self,v):
        return tree.Conditional(
            v[0],
            v[2],
            v[5],
            v[7]
        )

    @_("ELSE LBRACE expr RBRACE")
    def elseorif(self,v):
        return tree.Else(
            v[0],
            v[5]
        )
    @_("ELIF LPAREN expr RPAREN LBRACE expr RBRACE elseorif")
    def elseorif(self,v):
        return tree.Conditional(
            v[0],
            v[2],
            v[5],
            v[7]
        )