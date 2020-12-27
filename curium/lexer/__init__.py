from typing import Any, Collection, get_type_hints

from sly.yacc import _collect_grammar_rules
from .tokens import *
from sly import Lexer

# Get rid of them pylint errors
_ = lambda v: 0 == 0
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
        LAND,
        LOR,
        LNOT,
        BAND,
        BOR,
        BXOR,
        BOC,
        BLS,
        BRS,
        EQU,
        NEQU,
        LTGT,
        GT,
        LT,
        GTEQ,
        LTEQ,
        ASSG,
        ADDASSG,
        SUBASSG,
        MULASSG,
        DIVASSG,
        MODASSG,
        FLOORASSG,
        ADD,
        SUB,
        MUL,
        DIV,
        MOD,
        FLOORDIV,
        INC,
        DEC,
        LPAREN,
        RPAREN,
        LBRACK,
        RBRACK,
        LBRACE,
        RBRACE,
        COMMA,
        SEMICOLON,
        COLON
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
    

    # Token for integers
    HEXIDECIMAL     = r'0x[a-fA-F0-9]+'
    OCTAL           = r'0o[0-8]+'
    BINARY          = r'0b[0-1]+'
    DECIMAL         = r'[0-9]+'
    

    # Token for string
    STRING          = r'\".*?\"'

    # INC and DEC
    INC             = r"\+\+"
    DEC             = r"--"

    # Logical operators
    LAND            = r'&&'
    LOR             = r'\|\|'
    LNOT            = r"!"

    # Bitwise operators
    BAND            = r'&'
    BOR             = r'\|'
    BXOR            = r'\^'
    BOC             = r'~'
    BLS             = r'<<'
    BRS             = r'>>'



    # Compairson operators
    EQU             = r'=='
    NEQU            = r'!='
    LTGT            = r'<>'

    GT              = r'>'
    LT              = r'<'

    GTEQ            = r'>='
    LTEQ            = r'<='

    # Assignment operators
    ASSG            = r'='

    ADDASSG         = r'\+='

    SUBASSG         = r'-='

    MULASSG         = r'\*='

    DIVASSG         = r'/='

    MODASSG         = r'%='

    FLOORASSG       = r'//='



    # Mathematical operators
    ADD             = r'\+'
    SUB             = r'\-'
    MUL             = r'\*'
    DIV             = r'/'
    MOD             = r'%'
    FLOORDIV        = r'//'    

    

    @_(r'\n+')
    def newline(self, t):
        self.lineno += t.value.count('\n')
    
    