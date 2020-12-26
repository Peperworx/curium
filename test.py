from curium import preprocessor
from io import StringIO
import unittest
import hashlib

class TestPreprocessor(unittest.TestCase):
    def test_basic_define(self):
        pre = preprocessor.PreProcessor()
        inp = []
        inp += ["%define a bc"]
        inp += ['print(a,"a");']
        
        output = pre.process(
            "\n".join(inp)
        )
        self.assertEqual(output,'print(bc,"a");')
        print()
    def test_multiline(self):
        # Test multiline preprocessor with no preprocessor statements
        pre = preprocessor.PreProcessor()
        pre.knownNames = {}
        inp = []
        inp += ["a(b,c);"]
        inp += ["d(e,f);"]
        output = pre.process(
            "\n".join(inp)
        )
        
        self.assertEqual(output,"\n".join(inp))
    
    def test_comments(self):
        # Test multiline preprocessor with no preprocessor statements
        pre = preprocessor.PreProcessor()
        pre.knownNames = {}
        inp = []
        inp += ["a('//Test',c); // test"]
        inp += ["d(\"// test //\",f); // test //"]
        out = pre.process(
            "\n".join(inp)
        )
        print("No comments:")
        print(out)

def preprocessor_test_file(filename,result):
    pre = preprocessor.PreProcessor()
    with open(filename) as f:
        out = pre.process(f.read())
    
    with open(result) as f:
        # Now compare and return
        # We strip whitespace for consistancy.
        return "".join(f.read().split()) == "".join(out.split())


if __name__ == "__main__":
    for i in range(0):
        preprocessor_test_file(f"tests/test{i}.cm","tests/test{i}.cm.res")
    unittest.main()
    