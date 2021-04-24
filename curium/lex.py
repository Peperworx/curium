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
        STRING,
        LPAREN,
        RPAREN,
        LBRACE,
        RBRACE,
        LBRACK,
        RBRACK,
        ARROW,
        DEF,
        CHAR,
        UCHAR,
        SHORT,
        USHORT,
        INT,
        UINT,
        LONG,
        ULONG,
        FLOAT,
        DOUBLE,
        RETURN,
        SEMICOLON,
        COLON,
        HEXIDECIMAL,
        BINARY,
        OCTAL,
        DECIMAL,
        COMMA,
        ADD,
        SUB,
        DIV,
        MUL,
        MOD,
        LT,
        GT,
        LTEQ,
        GTEQ,
        EQ,
        NEQ,
        ASSG,
        ADD_ASSG,
        SUB_ASSG,
        MUL_ASSG,
        DIV_ASSG,
        MOD_ASSG,
        BLS_ASSG,
        BRS_ASSG,
        BAND_ASSG,
        BOR_ASSG,
        BXOR_ASSG,
        BAND,
        BOR,
        BXOR,
        BLS,
        BRS,
        BNOT,
        LAND,
        LOR,
        LNOT,

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


    # Built in names

    # There are a few built in names

    # There are generally called keywords
    # We will define then here



    NAME['def'] = DEF # For function definition

    # Integer and floating point datatype names
    NAME['char'] = CHAR # Signed and unsigned char (8bit)
    NAME['uchar'] = UCHAR

    NAME['short'] = SHORT # Signed and unsigned short (16 bits)
    NAME['ushort'] = USHORT

    NAME['int'] = INT # Signed and unsigned integer (32 bits)
    NAME['uint'] = UINT

    NAME['long'] = LONG # Signed and unsigned long (64 bits)
    NAME['ulong'] = ULONG

    NAME['float'] = FLOAT # Floating point number (32 bits)
    NAME['double'] = DOUBLE # Double precision floating point number (64 bits)

    NAME['return'] = RETURN # The return keyword

    # Numbers come in different forms

    # The four that will be implemented first 
    # are decimal, hexidecimal, binary and octal


    # This is the main number function
    # It converts all numbers to decimal

    
    HEXIDECIMAL = r'0x[0-9a-fA-F]+'
    BINARY = r'0b[0-1]+'
    OCTAL = r'0o[0-7]+'
    DECIMAL = r'[0-9]+'
    
    # Strings are another type. Strings CAN be multiline
    STRING = r'\"(?s).*?\"'

    # Brackets are essential to curium
    # They denote the start and end of sections of code, lists, etc.
    LPAREN = r"\("
    RPAREN = r"\)"
    LBRACE = r"{"
    RBRACE = r"}"
    LBRACK = r"\["
    RBRACK = r"\]"

    # The arrow denotes two things:
    # Function return types
    # And indirected member access
    ARROW = r"\->"

    # Semicolons are used to end instructions
    SEMICOLON = r';'

    # And colons are used in variable definitions
    COLON = r':'
    
    # Commas are used to delimit lists
    COMMA = r','
    
    

    # Compairison
    LT   = "<"
    GT   = ">"
    LTEQ = "<="
    GTEQ = ">="
    EQ   = "=="
    NEQ  = "!="

    # Assignment
    ASSG      = "="
    ADD_ASSG  = "\+="
    SUB_ASSG  = "\-="
    MUL_ASSG  = "\*="
    DIV_ASSG  = "/="
    MOD_ASSG  = "%="
    BLS_ASSG  = "<<="
    BRS_ASSG  = ">>="
    BAND_ASSG = "&="
    BOR_ASSG  = "\|="
    BXOR_ASSG = "^="

    # Basic arithmetic
    ADD  = "\+"
    SUB  = "\-"
    MUL  = "\*"
    DIV  = "/"
    MOD  = "%"

    # Bitwise Operators
    BAND = "&"
    BOR  = "\|"
    BXOR = '\^'
    BLS  = "<<"
    BRS  = ">>"
    BNOT = "~"

    # Logical
    LAND = "&&"
    LOR  = "\|\|"
    LNOT = "!"




    
