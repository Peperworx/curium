
from curium.lexer.tokens import ELSE, IF
from sly import Parser as SlyParser
from sly import Lexer as SlyLexer
from rich import print
import os

# Pylance errors go byby
_ = lambda v: print(v)

class Lexer(SlyLexer):
    tokens = {
        NAME,
        LPAREN, RPAREN,
        LBRACE, RBRACE,
        LBRACK, RBRACK,
        PCT,
        COMMA,
        COLON,
        SEMICOLON,
        PERIOD,
        LT, GT,
        LTEQ, GTEQ,
        EQU, NEQU,
        DECIMAL,
        HEX,
        BIN,
        IF, ELSE
    }

    # Ignore spaces and tabs.
    ignore = ' \t'

    # Names
    NAME = r"[a-zA-Z_][a-zA-Z0-9_]*"
    NAME['if'] = IF
    NAME['else'] = ELSE

    # Parentheses and brackets
    LPAREN = r'\('
    RPAREN = r'\)'
    LBRACE = r'\{'
    RBRACE = r'\}'
    LBRACK = r'\['
    RBRACK = r'\]'

    # Percent symbol
    PCT = r"%"

    # Comma
    COMMA = r','

    # Colon and semicolon
    COLON = r':'
    SEMICOLON = r';'

    # Period for member access
    PERIOD = r'\.'

    # A bunch of compairison symbols.
    EQU = r'=='
    NEQU = r'!='
    GT = r'>'
    LT = r'<'
    GTEQ = r'>='
    LTEQ = r'<='


    # Decimal Integers
    @_(r"[0-9]+")
    def DECIMAL(self, v):
        v.value = int(v.value)
        return v
    
    # Hex integers
    @_(r"0x[a-fA-F0-9]*")
    def HEX(self, v):
        v.value = int(v.value[2:],16)
        return v
    
    # Bin integers
    @_(r"0b[0-1]*")
    def BIN(self, v):
        v.value = int(v.value[2:],2)
        return v

    # Newlines should increment lineno
    @_(r'\n+')
    def newline(self, v):
        self.lineno += len(v.value)

class Parser(SlyParser):
    tokens = Lexer.tokens



    # The entire file is just a list of instructions
    @_('insts')
    def file(self, v):
        return v[0]

    
    
    # A namespace is { insts }
    @_('LBRACE insts RBRACE')
    def namespace(self, v):
        return ['ns',v[1]]

    # For a list of instructions
    @_('semiinst insts')
    def insts(self, v):
        out = ['insts',v[0]]
        if v[1][0] == "inst":
            out.append(v[1][1])
        elif v[1][0] == "insts":
            out.extend(v[1][1:])
        return out

    @_('semiinst')
    def insts(self, v):
        return ["inst",v[0]]
    
    # Rule for a single instruction with semicolon
    @_('instruction SEMICOLON')
    def semiinst(self,v):
        return v[0]

    # A single instruction call
    @_('builtin instructioncall')
    def instruction(self, v):
        return ["icall",v[0],v[1]]

    

    # Rule for instructioncall
    @_('LPAREN args RPAREN')
    def instructioncall(self,v):
        return ['call'] + v[1][1:]
    
    @_('LPAREN RPAREN')
    def instructioncall(self,v):
        return ['call']


    # A list of instruction arguments
    @_("arg COMMA args")
    def args(self,v):
        out = ['args',v[0]]
        if v[2][0] == "arg":
            out.append(v[2][1])
        elif v[2][0] == "args":
            out.extend(v[2][1:])
        return out
    

    @_("arg")
    def args(self,v):
        return ['arg',v[0]]


    # For a instruction argument
    @_('number','builtin','udefname')
    def arg(self,v):
        return v[0]

    # Rule for builtins
    @_('names')
    def builtin(self,v):
        if v[0][1] == 'if':
            return ['IF']
        if v[0][1] == 'else':
            return ['ELSE']
        return ['builtin',v[0]]

    # Rule for user defined names
    @_('PCT names')
    def udefname(self,v):
        return ['udefname',v[1]]

    # To match names
    @_("NAME PERIOD names")
    def names(self,v):
        out = ['names',v[0]]
        if v[2][0] == "name":
            out.append(v[2][1])
        elif v[2][0] == "names":
            out.extend(v[2][1:])
        return out
    

    @_("NAME","IF","ELSE")
    def names(self,v):
        return ['name',v[0]]
    
    

    # To match numbers
    @_("HEX","DECIMAL","BIN")
    def number(self, v):
        return ['number',v[0]]