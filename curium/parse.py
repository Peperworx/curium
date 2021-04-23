from sly import Parser
from . import lex as clex
from .tokens import *

class CuriumParser(Parser):
    # Grab tokens from lexer
    tokens = clex.CuriumLexer.tokens
    debugfile = 'parser.out'
    
    @_("file_component", "file_component file")
    def file(self, v):
        return (v[0],) if len(v) == 1 else (v[0], *v[1])

    @_("function_def","statements")
    def file_component(self,v):
        return v[0]

    @_("DEF name LPAREN tuple RPAREN ARROW name LBRACE statements RBRACE")
    def function_def(self,v):
        return ('function',v[1],v[3],v[6],v[8])

    @_("DEF name LPAREN RPAREN ARROW name LBRACE statements RBRACE")
    def function_def(self,v):
        return ('function',v[1],('tuple',),v[5],v[7])

    @_("statement", "statements statements")
    def statements(self,v):
        return ('statements', v[0]) if len(v) == 1 else ('statements', *v[0][1:], *v[1][1:])

    

    @_("RETURN expr SEMICOLON")
    def statement(self, v):
        return ("return", ('expr','inline',v[1]))
    
    @_("expr SEMICOLON")
    def statement(self,v):
        return ('expr','statement',v[0])

    # Tuple
    @_("expr COMMA expr")
    def tuple(self,v):
        return ('tuple',v[0],v[1]) if v[2][0] != "tuple" else ('tuple',v[0],*v[2][1:])

    # OOP Stuff
    @_("LPAREN expr RPAREN")
    def expr(self, v):
        return v[1]

    

    # Function calls
    @_("name LPAREN tuple RPAREN")
    def expr(self, v):
        return ('function_call', v[0], v[2])
    
    @_("name LPAREN RPAREN")
    def expr(self,v):
        return ('function_call', v[0], ('tuple',))

    # Type
    @_("number","string","name","tuple")
    def expr(self,v):
        return v[0]

    # Numbers
    @_("HEXIDECIMAL","OCTAL","BINARY","DECIMAL")
    def number(self,v):
        
        if v[0].startswith("0x"):
            v[0] = int(v[0][2:],16)
        elif v[0].startswith("0o"):
            v[0] = int(v[0][2:],8)
        elif v[0].startswith("0b"):
            v[0] = int(v[0][2:],2)
        else:
            v[0] = int(v[0])
        
        return ('literal', 'integer', v[0], ["i32","i64"][v[0] > 0xFFFFFFFF])

    # Strings
    @_("STRING")
    def string(self, v):
        return ('literal', 'string', v[0])

    # Names
    @_(
        "NAME",
        "CHAR",
        "UCHAR",
        "SHORT",
        "USHORT",
        "INT",
        "UINT",
        "LONG",
        "ULONG",
        "FLOAT",
        "DOUBLE"
        )
    def name(self,v):
        if v[0] in ["int","uint","short","ushort","char","uchar"]:
            v[0] = "i32"
        elif v[0] in ["long","ulong"]:
            v[0] = "i32"
        elif v[0] == "float":
            v[0] = "f32"
        elif v[0] == "double":
            v[0] = "f64"
        
        return ('literal', 'name', v[0])