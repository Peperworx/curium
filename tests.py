from curium import lex as clex
from curium import parse as cparse
from curium import compile as ccompile
from curium.error import *

def strip_whitespace(inlex):
    """
        Strips whitespace from a list of tokens
    """
    for i in inlex:
        if i.type not in ["SPACE","NEWLINE"]:
            yield i

def print_pretty(t,level=0,indent=4):
    """
        Pretty prints a parse tree
    """
    if not isinstance(t,tuple):
        print(f"{' '*indent*level}{t}")
        return
    print(f"{' '*indent*level}(")
    for i in t:
        print_pretty(i,level+1,indent)
    print(f"{' '*indent*level})")

if __name__ == '__main__':
    # Initialize a lexer class
    lexer = clex.CuriumLexer()

    # This is out test string to lex
    with open("tests/test1.cr") as f:
        tolex = f.read()

    # This basic function escapes a string of newlines
    def escape_str(s) -> str:
        return s.replace("\n","\\n")

    # Initialize a variable that contains the reconstructed data
    reconstructed = ""

    # Print newline
    print("\n")

    # Initialize linenumber and column tracking
    lineno = 1
    col = 1

    # Iterate over the lexed code
    for t in lexer.tokenize(tolex):
        # Add the value to reconstructed
        reconstructed += str(t.value)
        
        # Print the value, and relevant information
        print(f"{lineno}:{col}\t| {escape_str(t.value)}      \t\t: {t.type}")

        # Handle basic column tracking
        col += len(t.value)
        if t.value == "\n":
            lineno += 1
            col = 1
            
        
    # If it is perfectly reconstructed, then the lexer did not error
    assert tolex == reconstructed, "Reconstructed does not match original"

    # Parse
    error_handler = CuriumErrorHandler(tolex.split("\n"),lexer)
    parser = cparse.CuriumParser()

    print_pretty(parser.parse(strip_whitespace(lexer.tokenize(tolex))))
    print("\n\n")
    # Compile
    compiler = ccompile.CuriumCompiler()

    print(compiler.compile(parser.parse(strip_whitespace(lexer.tokenize(tolex)))))
