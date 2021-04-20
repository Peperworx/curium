from sly import Lexer

from .tokens import *


class CuriumLexer(Lexer):
    def __init__(self,*args,**kwargs):
        self.col = 1
        return Lexer.__init__(self,*args,**kwargs)
    tokens = {
        SPACE,
        TAB,
        NEWLINE,
        NAME,
        NUMBER,
        STRING
    }
    
    # We do not "ignore" whitespace. We simple make note of it, and move on

    @_(r'\n+')
    def NEWLINE(self, t):
        return t
    
    @_(r' +')
    def SPACE(self, t):
        return t
    


    # Names are used to identify objects in curium.
    # For example, your function could have the NAME "main"
    # Names must not start with a number. This allows us to 
    # have custom names that only the compiler can use, and also allows
    # notation for other numeric types (e.x. 0xF00D)
    NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'

    # Numbers come in different forms

    # The four that will be implemented first 
    # are decimal, hexidecimal, binary and octal


    # This is the main number function
    # It converts all numbers to decimal

    @_(
        r'0x[0-9a-fA-F]+',
        r'0b[0-1]+',
        r'0o[0-7]+',
        r'[0-9]+')
    def NUMBER(self, t):

        # Check and convert for each type
        if t.value.startswith("0x"):
            t.value = int(t.value[2:],16)
        elif t.value.startswith("0b"):
            t.value = int(t.value[2:],2)
        elif t.value.startswith("0o"):
            t.value =  int(t.value[2:],8)
        else:
            t.value = int(t.value[2:])

        # Return T
        return t
    

    # Brackets are essential to curium
    # They denote the start and end of sections of code, lists, etc.
    LPAREN = r"\("
    RPAREN = r"\)"
    LBRACE = r"{"
    RBRACE = r"}"
    LBRACK = r"["
    RBRACk = r"]"

    
    # Strings are another type. Strings CAN be multiline
    STRING = r'\"(?s).*?\"'
