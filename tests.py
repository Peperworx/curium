from curium import lex as clex

import unittest

class TestLexer(unittest.TestCase):
    def test_lex_1(self):
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
            print(f"{escape_str(t.value)}: {t.type} {lineno}:{col}")

            col += len(t.value)

            # Handle basic column tracking
            if t.value == "\n":
                lineno += 1
                col = 1

            
            
            

        # If it is perfectly reconstructed, then the lexer did not error
        self.assertEqual(tolex, reconstructed, "Reconstructed does not match original")

if __name__ == '__main__':
    unittest.main()