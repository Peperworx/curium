from curium import preprocessor
from curium import lexer



def test_file(filename: str,result: str):
    pre = preprocessor.PreProcessor()
    with open(filename) as f:
        out = pre.process(f.read())
    with open(result) as f:
        # Now compare and assert
        # We strip whitespace for consistancy.
        assert "".join(f.read().split()) == "".join(out.split())
    
    # Now lex it
    lex = lexer.Lex()
    for l in lex.tokenize(out):
        print(l)


if __name__ == "__main__":
    for i in range(4):
        test_file(f"tests/test{i}.cm",f"tests/test{i}.cm.res")
    