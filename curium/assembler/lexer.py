from typing import Any
from ..lexer.tokens import *
from sly import Lexer

# Get rid of them pylint errors
_ = lambda v: print
def find_column(text, token):
        last_cr = text.rfind('\n', 0, token.index)
        if last_cr < 0:
            last_cr = 0
        column = (token.index - last_cr) + 1
        return column


class Lex(Lexer):
    # Ignore tabs and spaces
    ignore = ' \t'

    # List of tokens
    tokens: set[Any] = {
        NAME,
        STRING,
        HEXIDECIMAL,
        OCTAL,
        BINARY,
        DECIMAL,
        IF,
        ELSE,
        ELIF,
        WHILE,
        FOR,
        RETURN,
        LPAREN,
        RPAREN,
        LBRACK,
        RBRACK,
        LBRACE,
        RBRACE,
        COMMA,
        SEMICOLON,
        COLON,
        NEWLINE
    }
    # Literals, because the builtin function cant have precedence
    LPAREN          = r"\("
    RPAREN          = r"\)"
    LBRACK          = r"\["
    RBRACK          = r"\]"
    LBRACE          = r"{"
    RBRACE          = r"}"
    COMMA           = r","
    SEMICOLON       = r";"
    COLON           = r":"

    # Add a token for a name
    NAME            = r'[a-zA-Z_][a-zA-Z0-9_]*'

    # Token for builtin names
    NAME['if']      = IF
    NAME['else']    = ELSE
    NAME['elif']    = ELIF
    NAME['while']   = WHILE
    NAME['for']     = FOR
    NAME['return']  = RETURN
    

    # Token for integers
    HEXIDECIMAL     = r'0x[a-fA-F0-9]+'
    OCTAL           = r'0o[0-8]+'
    BINARY          = r'0b[0-1]+'
    DECIMAL         = r'[0-9]+'
    
    # Newline
    NEWLINE         = r'\n'

    # Token for string
    STRING          = r'\".*?\"'

    @_(r'\n+')
    def newline(self, t):
        self.lineno += t.value.count('\n')
    
    