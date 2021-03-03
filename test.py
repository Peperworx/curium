from curium import compiler

code = {
    "type": "body",
    "statements": [
        {
            "type": "funcdef",
            "returns": "i32",
            "name": "main",
            "contents": [
                {
                    "type": "statement",
                    "name": "return",
                    "arguments": [
                        "0"
                    ]
                }
            ]
        }
    ]
}

compiled = compiler.compile(code)

print(compiled)