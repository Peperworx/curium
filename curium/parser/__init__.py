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


    # The most basic of statements is an expression
    # followed by a semicolon
    
    @_("expr SEMICOLON")
    def statement(self, v):
        return tree.expr_statement(
            v[0],
            v.lineno,
            v.index
        )

    # Second most basic is a assignment

    # First variable initialization
    @_("name COLON name SEMICOLON")
    def statement(self, v):
        return tree.var_initialize(
            v[0],
            v[2]
        )
    
    # Variable assignment is an expression
    @_(
        "name ASSG expr",
        "name ADDASSG expr",
        "name SUBASSG expr",
        "name MULASSG expr",
        "name DIVASSG expr",
        "name MODASSG expr",
        "name FLOORASSG expr"
    )
    def expr(self, v):
        return tree.var_assign(
            v[0],
            v[2],
            v[1],
            v.lineno,
            v.index
        )

    # Assignment and initialization at the same time
    @_(
        "name COLON name ASSG expr SEMICOLON",
        "name COLON name ADDASSG expr SEMICOLON",
        "name COLON name SUBASSG expr SEMICOLON",
        "name COLON name MULASSG expr SEMICOLON",
        "name COLON name DIVASSG expr SEMICOLON",
        "name COLON name MODASSG expr SEMICOLON",
        "name COLON name FLOORASSG expr SEMICOLON"
    )
    def statement(self, v):
        return tree.var_init_assg(
            v[0],
            v[2],
            v[4],
            v[3],
            v.lineno,
            v.index
        )
    

    
    

    # Binary operators
    @_(
        "expr COMMA expr",      # Tuple
        "expr LAND expr",       # Logical operators
        "expr LOR expr",
        "expr BAND expr",       # Bitwise operators
        "expr BOR expr",
        "expr BXOR expr",
        "expr BOC expr",
        "expr BLS expr",
        "expr BRS expr",
        "expr EQU expr",        # Compairson operators
        "expr NEQU expr",
        "expr LTGT expr",
        "expr GT expr",
        "expr LT expr",
        "expr GTEQ expr",
        "expr LTEQ expr",
        "expr ADD expr",        # Arithmetic
        "expr SUB expr",
        "expr MUL expr",
        "expr DIV expr",
        "expr MOD expr",
        "expr FLOORDIV expr"
    )
    def expr(self, v):
        return tree.binary_op(
            v[1],
            v[0],
            v[2],
            v.lineno,
            v.index
        )

    # Unary prefix operators
    @_(
        "INC expr %prec INCP",
        "DEC expr %prec DECP",
        "ADD expr %prec UPLUS",
        "SUB expr %prec UMIN",
        "LNOT expr"
    )
    def expr(self,v):
        return tree.unary_op(
            v[0],
            v[1],
            v.lineno,
            v.index
        )

    # Unary postfix operators
    @_(
        "expr INC",
        "expr DEC"
    )
    def expr(self,v):
        return tree.unary_op(
            v[0],
            v[1],
            v.lineno,
            v.index
        )

    
    # Integer literals
    @_(
        "HEXIDECIMAL",
        "OCTAL",
        "BINARY",
        "DECIMAL"
    )
    def expr(self,v):
        return tree.integer_literal(v[0],
            v.lineno,
            v.index)

    # String literals
    @_("STRING")
    def expr(self,v):
        return tree.string_literal(
            v[0],
            v.lineno,
            v.index
        )


    ## Here comes the fun part! Names.

    @_("name")
    def expr(self, v):
        return v[0]

    @_("NAME")
    def name(self,v):
        return tree.name_literal(
            v[0],
            tree.empty_expr(),
            v.lineno,
            v.index
        )

    @_("NAME LBRACK NAME RBRACK")
    def name(self,v):
        return tree.name_literal(
            v[0],
            v[2],
            v.lineno,
            v.index
        )
    

    # Function types
    @_("LPAREN expr RPAREN namespace")
    def expr(self,v):
        return tree.function_literal(
            v[1],
            v[3],
            v.lineno,
            v.index
        )

    @_("LPAREN RPAREN namespace")
    def expr(self,v):
        return tree.function_literal(
            tree.empty_statement(),
            v[2],
            v.lineno,
            v.index
        )



    # Now for namespaces
    @_("LBRACE RBRACE")
    def namespace(self,v):
        return tree.namespace(
            [],
            v.lineno,
            v.index
        )
    
    @_("LBRACE statement RBRACE")
    def namespace(self,v):
        return tree.namespace(
            [],
            v.lineno,
            v.index
        )

    
    
    # Function calls
    @_("name LPAREN expr RPAREN")
    def expr(self, v):
        return tree.function_call(
            v[0],
            v[2],
            v.lineno,
            v.index
        )

    @_("name LPAREN RPAREN")
    def expr(self, v):
        return tree.function_call(
            v[0],
            tree.empty_expr(),
            v.lineno,
            v.index
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
            f'|{" " * (col)}{"^" * len(t.value)}'
        )
        print(f"| Syntax error at line {t.lineno} col {col-1}:")
        print(f"| \tUnexpected token \"{t.value}\"")
        print("|\n")
        

    