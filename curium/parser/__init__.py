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
            BOC,
            INDIRECTION,
            ADDR
        ), ("left",
           INC,
           DEC,
           # Leave room for function call, subscript, member access
        ),
    )

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
    def statements(self,v):
        out = [v[0]]
        return tree.namespace(
            out
        )
    
    

    # The most basic of statements is an expression
    
    @_("expr")
    def statement(self, v):
        return tree.expr_statement(
            v[0],
            v[0].lineno,
            v[0].index
        )

    # Second most basic is a assignment

    # First variable initialization
    @_("name COLON name")
    def statement(self, v):
        return tree.var_initialize(
            v[0],
            v[2],
            v.lineno,
            v.index
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
        "name COLON name ASSG expr",
        "name COLON name ADDASSG expr",
        "name COLON name SUBASSG expr",
        "name COLON name MULASSG expr",
        "name COLON name DIVASSG expr",
        "name COLON name MODASSG expr",
        "name COLON name FLOORASSG expr"
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
    

    # Builtin statements

    # First return
    @_(
        "RETURN expr"
    )
    def statement(self, v):
        return tree.return_statement(
            v[1],
            v.lineno,
            v.index
        )

    # For loop
    @_(
        "FOR LPAREN statement SEMICOLON expr SEMICOLON statement RPAREN namespace"
    )
    def statement(self,v):
        return tree.for_loop(
            v[2],
            v[4],
            v[6],
            v[8],
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

    # Function calls
    @_("expr LPAREN expr RPAREN")
    def expr(self, v):
        return tree.function_call(
            v[0],
            v[2],
            v.lineno,
            v.index
        )

    @_("expr LPAREN RPAREN")
    def expr(self, v):
        return tree.function_call(
            v[0],
            tree.empty_expr(v.lineno,v.index),
            v.lineno,
            v.index
        )


    ## Here comes the fun part! Names.

    @_("name")
    def expr(self, v):
        return v[0]

    @_(
        "MUL name %prec INDIRECTION",
        "BAND name %prec ADDR"
    )
    def name(self, v):
        nm = v[1]
        if v[0] == "*":
            nm.indirection = True
        if v[0] == "&":
            nm.addr = True
        return nm

    @_("NAME")
    def name(self,v):
        return tree.name_literal(
            v[0],
            tree.empty_expr(v.lineno,v.index),
            False,
            False,
            v.lineno,
            v.index
        )

    @_("NAME LBRACK name RBRACK")
    def name(self,v):
        return tree.name_literal(
            v[0],
            v[2],
            False,
            False,
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
            tree.empty_statement(v.lineno,v.index),
            v[2],
            v.lineno,
            v.index
        )


    @_("namespace")
    def expr(self, v):
        return v[0]

    # Now for namespaces
    @_("LBRACE RBRACE")
    def namespace(self,v):
        return tree.namespace(
            []
        )
    
    @_("LBRACE statements RBRACE")
    def namespace(self,v):
        return v[1]

    
    
    
    

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
        

    