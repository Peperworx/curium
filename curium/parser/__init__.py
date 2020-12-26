from lark import Lark
from os import path

class Parser:
    grammar: Lark
    def __init__(self):
        with open(path.join(path.dirname(__file__),"lang.lark")) as f:
            self.grammar = Lark(
                f.read()
            )
    def parse(self,s: str):
        parsed = self.grammar.parse(s)
        return parsed