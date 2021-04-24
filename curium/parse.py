from sly import Parser
from . import lex as clex
from .tokens import *

class CuriumParser(Parser):
    # Grab tokens from lexer
    tokens = clex.CuriumLexer.tokens

    # Parser out file
    debugfile = 'parser.out'

    # Operator precedences
    precedence = (
        ('left', 'COMMA'),
        ('right', ASSG,
        ADD_ASSG, SUB_ASSG,
        MUL_ASSG, DIV_ASSG, MOD_ASSG,
        BLS_ASSG, BRS_ASSG,
        BAND_ASSG, BXOR_ASSG, BOR_ASSG),
        ('left', LOR),
        ('left', LAND),
        ('left', BOR),
        ('left', BXOR),
        ('left', BAND),
        ('left', EQ, NEQ),
        ('left', LT, LTEQ, GT, GTEQ),
        ('left', BLS, BRS),
        ('left', ADD, SUB),
        ('left', MUL, DIV, MOD),
        ('right', LNOT, BNOT)
    )

    # A statement
    @_("expr","declaration")
    def statement(self, v):
        return ('statement', v[0])

    # Basic expressions
    @_("expr ADD expr",
        "expr SUB expr",
        "expr MUL expr",
        "expr DIV expr",
        "expr MOD expr",
        "expr LT expr",
        "expr GT expr",
        "expr LTEQ expr",
        "expr GTEQ expr",
        "expr EQ expr",
        "expr NEQ expr",
        "expr BAND expr",
        "expr BOR expr",
        "expr BXOR expr",
        "expr BLS expr",
        "expr BRS expr",
        "expr BNOT expr",
        "expr LAND expr",
        "expr LOR expr",
        "expr LNOT expr")
    def expr(self, v):
        return ('binop',v[1],v[0],v[2])
    
    @_("LPAREN expr RPAREN")
    def expr(self, v):
        return v[1]
    # Assignment
    @_("defined_type COLON type ASSG expr")
    def declaration(self, v):
        return ('decl-assg', v[3], v[0], v[2], v[4])

    @_("defined_type COLON type")
    def declaration(self, v):
        return ('decl', v[0], v[2])

    @_("defined_type assgop expr")
    def assignment(self, v):
        return ('assg', v[0], v[1], v[2])
    
    # Assignment is an expression
    @_("assignment")
    def expr(self ,v):
        return v[0]

    # Assignment operators
    @_("ASSG",
        "ADD_ASSG",
        "SUB_ASSG",
        "MUL_ASSG",
        "DIV_ASSG",
        "MOD_ASSG",
        "BLS_ASSG",
        "BRS_ASSG",
        "BAND_ASSG",
        "BOR_ASSG",
        "BXOR_ASSG")
    def assgop(self, v):
        return v[0]

    # Expressions should link to types
    @_("type")
    def expr(self, v):
        return v[0]

    # Integers
    @_("HEXIDECIMAL","OCTAL","BINARY","DECIMAL")
    def expr(self,v):
        
        # Convert the integer
        if v[0].startswith("0x"):
            v[0] = int(v[0][2:],16)
        elif v[0].startswith("0o"):
            v[0] = int(v[0][2:],8)
        elif v[0].startswith("0b"):
            v[0] = int(v[0][2:],2)
        else:
            v[0] = int(v[0])
        
        # Return the node in the AST.
        # This includes the webassembly type
        return (f'{"i32.const" if v[0] <= 0xFFFFFFFF else "i64.const"}', v[0])

    # Strings
    @_("STRING")
    def expr(self, v):
        return ('string', v[0])

    
    # Names
    @_("NAME")
    def defined_type(self, v):
        return ('defined-type', v[0])
    
    # Defined type should link to type
    @_("defined_type")
    def type(self, v):
        return v[0]

    # Signed integers
    @_("INT","LONG")
    def type(self, v):
        return ('standard-type', 'i32' if v[0] == 'int' else 'i64', v[0], 'signed')
    
    # Unsigned integers
    @_("UINT","ULONG")
    def type(self, v):
        # Grab the actual type
        t = 'i32' if v[0][1:] == 'int' else 'i64'

        # Return
        return ('standard-type', t, v[0], 'unsigned')
    
    # Floating point numbers
    @_("FLOAT","DOUBLE")
    def type(self,v):
        return ('standard-type', 'f32' if v[0] == 'float' else 'f64')
