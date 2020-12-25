import unittest
from curium import preprocessor


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
        inp += ["d(\"/* test /*\",f); /* test /*"]
        out = pre.process(
            "\n".join(inp)
        )
        print("No comments:")
        print(out)
if __name__ == "__main__":
    unittest.main()