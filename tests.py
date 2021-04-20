from curium import lex as clex
from curium import parse as cparse

def strip_whitespace(inlex):
    """
        Strips whitespace from a list of tokens
    """
    for i in inlex:
        if i.type not in ["SPACE","NEWLINE"]:
            yield i

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
    parser = cparse.CuriumParser()

    print(parser.parse(strip_whitespace(lexer.tokenize(tolex))))