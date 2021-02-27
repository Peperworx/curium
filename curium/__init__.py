## Curium library entry
from parsimonious.grammar import Grammar



def parse(input):
    with open("parse.lex") as f:
        grammar = Grammar(f.read())
    