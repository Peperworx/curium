from typing import Any
from sly import Lexer
# Get rid of them pylint errors
_ = lambda v: print
NAME = ''
BUILTIN = ''
FLOAT = ''
INTEGER = ''

class Lex(Lexer):
    



    # Ignore tabs and spaces
    ignore = ' \t'

    
    # List of tokens
    tokens: set = {
        NAME,
        BUILTIN,
        FLOAT,
        INTEGER
    }

    # A name is a user defined symbol that points to a memory address or value
    NAME            = r'[%@][-a-zA-Z$._][-a-zA-Z$._0-9]*'

    # A builtin is a name that has special meaning and is reserved for compiler use
    BUILTIN         = r'[a-zA-Z_][a-zA-Z0-9_]*'

    # All numbers are represented in decimal format
    FLOAT           = r'[0-9]*\.[0-9]+'
    INTEGER         = r'[0-9]+'

    

    @_(r'\n+')
    def newline(self, t):
        self.lineno += t.value.count('\n')