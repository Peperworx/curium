from sly import Parser
from . import lex as clex
from .tokens import *

class CuriumParser(Parser):
    # Grab tokens from lexer
    tokens = clex.CuriumLexer.tokens
    
    

    # Integers
    @_("HEXIDECIMAL","OCTAL","BINARY","DECIMAL")
    def type(self,v):
        
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
    def type(self, v):
        return ('string', v[0])

    
    # Names
    @_("NAME")
    def type(self, v):
        return ('defined-type', v[0])
    
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
