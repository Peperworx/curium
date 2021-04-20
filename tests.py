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

        # Iterate over the lexed code
        for t in lexer.tokenize(tolex):

            # Add the value to reconstructed
            reconstructed += t.value
            
            # Print the value, and relevant information
            print(f"{escape_str(t.value)}: {t.type} {t.lineno}:{lexer.col}")

            # Handle basic column tracking
            if t.value == '\n' or not lexer.col:
                lexer.col = 1
            else:
                lexer.col += len(t.value)

        # If it is perfectly reconstructed, then the lexer did not error
        self.assertEqual(tolex, reconstructed, "Reconstructed does not match original")

if __name__ == '__main__':
    unittest.main()