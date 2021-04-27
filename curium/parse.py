from sly import Parser
from . import lex as clex
from .tokens import *
from .error import *
import sys

# Shortcut variable for assignment operators
assg_op = ["ASSG", "ADD_ASSG", "SUB_ASSG",
    "MUL_ASSG", "DIV_ASSG", "MOD_ASSG",
    "BRS_ASSG", "BLS_ASSG", "BAND_ASSG",
    "BOR_ASSG", "BXOR_ASSG"]

class CuriumParser(Parser):
    def __init__(self, *args, **kwargs):
        return Parser.__init__(self, *args, **kwargs)

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
        ('left', BNOT, LNOT)
    )

    def func_in_type_tree(self, name):
        for i in self.type_tree["functions"]:
            if i["name"] == name:
                return i
        return None

    # File
    @_("file_component file")
    def file(self, v):
        return (v[0], *v[1])

    @_("file_component")
    def file(self, v):
        return (v[0],)
    
    # Function definitions
    @_("DEF defined_type LPAREN arglist RPAREN ARROW type LBRACE function_body RBRACE")
    def file_component(self, v):
        return ('func-def', v[1], v[6], v[3], v[8])

    @_("statements", "empty_statements")
    def function_body(self, v):
        return v[0]

    # Argument list
    @_("defined COMMA arglist")
    def arglist(self, v):
        return ('arglist', v[0], v[2][1:])
    
    @_("defined")
    def arglist(self, v):
        return ('arglist', v[0])
    
    @_("")
    def arglist(self, v):
        return ('arglist',)
    
    # An empty statement list
    @_('')
    def empty_statements(self, v):
        return ('statements',)
    

    # Statements
    @_("statement statements")
    def statements(self, v):
        return ('statements', v[0], *v[1][1:])

    @_("statement")
    def statements(self, v):
        return ('statements', v[0])

    # Return statement
    @_("RETURN expr SEMICOLON")
    def statement(self, v):
        return ('return', v[1])

    @_("expr SEMICOLON", "declare SEMICOLON")
    def statement(self, v):
        return v[0]
    
    
    # Function call
    @_("defined_type LPAREN funcall_list RPAREN")
    def expr(self, v):
        return ('func-call', v[0], v[2])

    # Funcall list
    @_("expr")
    def funcall_list(self, v):
        return ('funcall-list', v[0][1:] if v[0][0] == "tuple" else v[0])
    
    @_('')
    def funcall_list(self, v):
        return ('funcall-list',)
    

    # Basic binary operators
    @_("expr ADD expr",
        "expr SUB expr",
        "expr MUL expr",
        "expr DIV expr",
        "expr MOD expr",
        "expr BLS expr",
        "expr BRS expr",
        "expr LT expr",
        "expr LTEQ expr",
        "expr GT expr",
        "expr GTEQ expr",
        "expr EQ expr",
        "expr NEQ expr",
        "expr BAND expr",
        "expr BOR expr",
        "expr BXOR expr",
        "expr BNOT expr",
        "expr LOR expr",
        "expr LAND expr",
        "expr LNOT expr"
        )
    def expr(self, v):
        return ('binop', v[1], v[0], v[2])

    @_("expr COMMA expr")
    def expr(self, v):
        return ('tuple', v[0], *(v[2][1:] if v[2][0] == 'tuple' else [v[2]]))

    # Defining values
    @_("defined_type COLON type")
    def defined(self, v):
        return (v[0], v[2])

    # Declaring variables
    @_("LET defined")
    def declare(self, v):
        return ('declare', *v[1])
    
    # Declaring and assigning variables
    @_(*[f"LET defined {i} expr" for i in assg_op])
    def declare(self, v):
        return ('decl-assg', v[2], *v[1], v[3])
    
    # Raw assignment
    @_(*[f"defined_type {i} expr" for i in assg_op])
    def expr(self, v):
        return ('assign', v[1], v[0], v[2])
    
    
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
        # This includes the type
        return (f'{"i32.const" if v[0] <= 0xFFFFFFFF else "i64.const"}', v[0])

    # Strings
    @_("STRING")
    def expr(self, v):
        return ('string', v[0])

    
    # Names
    @_("NAME")
    def defined_type(self, v):
        return ('defined-type', v[0])
    
    # Defined types are also types
    @_("defined_type")
    def type(self, v):
        return v[0]

    # Signed integers
    @_("INT","LONG","SHORT","CHAR")
    def type(self, v):
        t = ""
        if v[0] == "int":
            t = "i32"
        elif v[0] == "long":
            t = "i64"
        elif v[0] == "short":
            t = "i16"
        elif v[0] == "char":
            t = "i8"

        return ('standard-type', t, 'signed')
    
    
    
    # Unsigned integers
    @_("UINT","ULONG","USHORT","UCHAR")
    def type(self, v):
        # Remove the U
        v[0] = v[0][1:]

        # Grab the actual type
        t = ""
        if v[0] == "int":
            t = "i32"
        elif v[0] == "long":
            t = "i64"
        elif v[0] == "short":
            t = "i16"
        elif v[0] == "char":
            t = "i8"

        # Return
        return ('standard-type', t, 'unsigned')
    
    # Floating point numbers
    @_("FLOAT","DOUBLE")
    def type(self,v):
        return ('standard-type', 'f32' if v[0] == 'float' else 'f64')

    