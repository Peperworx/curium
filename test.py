
from curium import parser
from curium import lexer
from curium import preprocessor
from rich.console import Console
from rich import print
import json


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
    
    # If there are no errors, lexing succeded
    # Lets dump these to some lexdump files
    lexdump = []
    
    for l in lex.tokenize(out):
        lexdump.append(
            {
                "type":l.type,
                "value":l.value,
                "lineno":l.lineno,
                "index":l.index,
                "column":lexer.find_column(out,l)-1 # Remove one so that it starts at 1
            }
        )
    
    # Save the lexdump
    with open(filename+".lexdump","w+") as f:
        f.write(json.dumps(lexdump,indent=4))

    # Now try to parse it
    lexed = lex.tokenize(out)
    parse = parser.Parse()
    parse.text = out
    parsed = parse.parse(lexed)
    
    # Now save the parsedump
    parsedump = json.dumps(parsed.resolve(), indent=4)

    with open(filename+".parsedump","w+") as f:
        f.write(parsedump)




if __name__ == "__main__":
    for i in range(1):
        print(f"Test {i}")
        test_file(f"tests/curium/test{i}.cm",f"tests/curium/test{i}.cm.res")
    
    