from io import StringIO
from sly import Lexer
import toml
import os
class Lex(Lexer):
    # Some basic literals
    literals = {
        '=', 
        '+',
        "-",
        "*",
        "/",
        '(',
        ')',
        '[',
        ']',
        '{',
        '}',
        ',',
        ';',
        ':'
    }

    # Ignore tabs and spaces
    ignore = ' \t'

    # List of tokens
    tokens = {
        NAME,
        STRING,
        HEXIDECIMAL,
        OCTAL,
        BINARY,
        DECIMAL
    }

    # Add a token for a name
    NAME    = r'[a-zA-Z_][a-zA-Z0-9_]*'

    # Token for integers
    HEXIDECIMAL = r'0x[a-fA-F0-9]+'
    OCTAL       = r'0o[0-8]+'
    BINARY      = r'0b[0-1]+'
    DECIMAL = r'[0-9]+'
    

    # Token for string
    STRING  = r'\".*?\"'

    

    @_(r'\n+')
    def newline(self, t):
        self.lineno += t.value.count('\n')