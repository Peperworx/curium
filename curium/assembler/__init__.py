import parsimonious
import os

class Parser:
    def __init__(self):
        with open(
            os.path.join(
                os.path.dirname(__file__),
                "./asm.peg"
            )
        ) as f:
            self.grammar = parsimonious.Grammar(f.read())
    def parse(self,input):
        return self.grammar.parse(input)