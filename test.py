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
                    "type": "vardef",
                    "mutable": True,
                    "name": "test",
                    "var_type": "i32",
                    "value": {
                        "type":"integer_literal",
                        "value":"1234"
                    }
                },
                {
                    "type": "statement",
                    "name": "return",
                    "arguments": [
                        "0"
                    ]
                }
            ]
        },
        {
            "type": "vardef",
            "mutable": False,
            "name": "test",
            "var_type": "i32",
            "value": {
                "type":"integer_literal",
                "value":"1234"
            }
        }
    ]
}

c = compiler.Compiler()

compiled = c.compile(code)

print(compiled)