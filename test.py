
from curium import preprocessor
from rich.console import Console
from rich import print
import curium
import json


def test_file(filename: str,result: str):
    pre = preprocessor.PreProcessor()
    with open(filename) as f:
        out = pre.process(f.read())
    with open(result) as f:
        # Now compare and assert
        # We strip whitespace for consistancy.
        assert "".join(f.read().split()) == "".join(out.split())
    

    parsed = curium.parse(out)


if __name__ == "__main__":
    for i in range(1):
        print(f"Test {i}")
        test_file(f"tests/curium/test{i}.cm",f"tests/curium/test{i}.cm.res")
    
    