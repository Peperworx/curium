from . import lexer
from rich import print
import os




class Parser:
    def parse(self, input):
        lex = lexer.Lexer()
        tok = [t for t in lex.tokenize(input)]



