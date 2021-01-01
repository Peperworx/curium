from re import match
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
            NAME,
            RETURN,
            LPAREN,
            RPAREN,
            
        ),(
            "left", 
            COMMA,
            SEMICOLON
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


    

    @_("expr SEMICOLON expr")
    def expr(self,v):
        return (
            'expression-list', 
            v[0],
            v[2]
        )
    
    @_("expr SEMICOLON")
    def expr(self,v):
        return (
            'statement',
            v[0]
        )
    # Return statement
    @_("RETURN expr")
    def expr(self,v):
        return (
            'return',
            v[1]
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
    def expr(self,v):
        return (
            'var-assign-init',
            v[3],
            v[0],
            v[2],
            v[4]
        )
    
    # Variable assignment
    @_(
        "expr ASSG expr",
        "expr ADDASSG expr",
        "expr SUBASSG expr",
        "expr MULASSG expr",
        "expr FLOORASSG expr",
        "expr DIVASSG expr",
        "expr MODASSG expr"
    )
    def expr(self,v):
        return (
            'var-assign',
            v[1],
            v[0],
            v[2]
        )

    # Variable initialization
    @_(
        "expr COLON NAME"
    )
    def expr(self,v):
        return (
            'var-init',
            v[0],
            v[2],
        )

    
    @_("NAME LPAREN RPAREN")
    def expr(self,v):
        return (
            'function-call',
            v[0],
            (
                'empty-expr'
            )
        )
    
    @_("NAME LPAREN expr RPAREN")
    def expr(self,v):
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
    @_(
        "LPAREN expr RPAREN"
    )
    def expr(self,v):
        return v[1]
    
    # Types


    @_("ltype","typedName")
    def expr(self,v):
        return (
            'literal',
            v[0]
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
    
    # Function type
    @_('LPAREN expr RPAREN LBRACE expr RBRACE')
    def ltype(self,v):
        return (
            'function-type',
            v[1],
            v[4]
        )
    # Function type
    @_('LPAREN RPAREN LBRACE expr RBRACE')
    def ltype(self,v):
        return (
            'function-type',
            ('empty-type',),
            v[3]
        )
    
    @_('STRING')
    def ltype(self,v):
        return (
            'string-literal',
            v[0]
        )
    
    @_("NAME LBRACK typedName RBRACK")
    def typedName(self,v):
        return (
            'typed-name',
            v[0],
            v[2]
        )
    
    @_("NAME")
    def typedName(self,v):
        return (
            'untyped-name',
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
        print("|"+"-"*max(len(line),50))
        print("|",line)
        print(
            f'|{" " * (col - 1)}{"^" * len(t.value)}'
        )
        print(f"| Syntax error at line {t.lineno} col {col-1}:")
        print(f"| \tUnexpected token \"{t.value}\"")
        print("|\n")
        

    