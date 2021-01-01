

class expr:
    pass

class empty_expr(expr):
    def __init__(self, lineno: int, index: int):
        self.lineno = lineno
        self.index = index
    def resolve(self):
        return {
            "tokname": "empty-expression",
            "type": "expression",
            "lineno": self.lineno,
            "index": self.index
        }

class statement:
    pass

class empty_statement(statement):
    def __init__(self, lineno: int, index: int):
        self.lineno = lineno
        self.index = index
    def resolve(self):
        return {
            "tokname": "empty-statement",
            "type": "statement",
            "lineno": self.lineno,
            "index": self.index
        }

class expr_statement(statement):
    def __init__(self, value: expr, lineno: int, index: int):
        # Set the expression value
        self.value = value

        # Lineno and index
        self.lineno = lineno
        self.index = index
    def resolve(self):
        return {
            "tokname": "expression-statement",
            "type": "statement",
            "value": self.value.resolve(),
            "lineno": self.lineno,
            "index": self.index
        }



class namespace(expr):
    def __init__(self,
            statements: list[statement]):
        # The actual list of statements
        self.statements = statements
        
    def resolve(self):
        return {
            "tokname": "namespace",
            "type": "expression",
            "statements": [s.resolve() for s in self.statements]
        }

        


class binary_op(expr):
    def __init__(self, 
            op: str, 
            left: expr, 
            right: expr, 
            lineno: int,
            index: int):
        # The operator
        self.op = op

        # The left operand
        self.left = left

        # The right operand
        self.right = right

        # The linenumber and index
        self.lineno = lineno
        self.index = index
    def resolve(self):
        return {
            "tokname": "binary-op",
            "type": "expression",
            "left": self.left.resolve(),
            "right": self.right.resolve(),
            "op": self.op,
            "lineno": self.lineno,
            "index": self.index
        }


class unary_op(expr):
    def __init__(self, 
            op: str, 
            operand: expr, 
            lineno: int, 
            index: int):
        # The operator
        self.op = op

        # The operand
        # This does not have a side because there are both
        # Prefix and postfix unary operators
        self.operand = operand

        # The linenumber and index
        self.lineno = lineno
        self.index = index
    def resolve(self):
        return {
            "tokname": "unary-op",
            "type": "expression",
            "op": self.op,
            "operand": self.operand.resolve(),
            "lineno": self.lineno,
            "index": self.index
        }


class function_call(expr):
    def __init__(self, 
            name: expr, 
            arguments: expr, 
            lineno: int, 
            index: int ):
        # The name of the function
        self.name = name

        # The arguments of the function.
        # This is an expression
        self.arguments = arguments

        # The linenumber and index
        self.lineno = lineno
        self.index = index
    def resolve(self):
        return {
            "tokname": "function-call",
            "type": "expression",
            "name": self.name.resolve(),
            "arguments": self.arguments.resolve(),
            "lineno": self.lineno,
            "index": self.index
        }


class function_literal(expr):
    def __init__(self,
            arguments: expr,
            contents: namespace,
            lineno: int,
            index: int):
        
        # List of arguments taken
        self.arguments = arguments

        # Contents of the function
        self.contents = contents

        # The linenumber and index
        self.lineno = lineno
        self.index = index
    def resolve(self):
        return {
            "tokname": "function-literal",
            "type": "literal-expression",
            "arguments": self.arguments.resolve(),
            "contents": self.contents.resolve(),
            "lineno": self.lineno,
            "index": self.index
        }


class integer_literal(expr):
    def __init__(self, 
            value: str,
            lineno: int,
            index: int):

        # Set the value
        self.value = value

        # The linenumber and index
        self.lineno = lineno
        self.index = index
    def resolve(self):
        return {
            "tokname": "integer-literal",
            "type": "literal-expression",
            "value": self.value,
            "lineno": self.lineno,
            "index": self.index
        }


class string_literal(expr):
    def __init__(self, 
            value: str,
            lineno: int,
            index: int):

        # Set the value
        self.value = value

        # The linenumber and index
        self.lineno = lineno
        self.index = index
    def resolve(self):
        return {
            "tokname": "string-literal",
            "type": "literal-expression",
            "value": self.value,
            "lineno": self.lineno,
            "index": self.index
        }

class name_literal(expr):
    def __init__(self,
            value: str,
            annotation: expr,
            lineno: int,
            index: int):

        # The name of the name
        self.value = value

        # The annotation of the name
        self.annotation = annotation

        # The linenumber and index
        self.lineno = lineno
        self.index = index
    def resolve(self):
        return {
            "tokname": "name-literal",
            "type": "literal-expression",
            "value": self.value,
            "annotation": self.annotation.resolve(),
            "lineno": self.lineno,
            "index": self.index
        }

class var_initialize(statement):
    def __init__(self, 
            var_type: name_literal,
            name: name_literal,
            lineno: int,
            index: int):

        # The type of the variable
        self.var_type = var_type

        # The name of the variable
        self.name = name

        # The linenumber and index
        self.lineno = lineno
        self.index = index
    def resolve(self):
        return {
            "tokname": "var-init",
            "type": "statement",
            "var-type": self.var_type.resolve(),
            "name": self.name.resolve(),
            "lineno": self.lineno,
            "index": self.index
        }
        

class var_assign(statement):
    def __init__(self,
            name: name_literal,
            value: expr,
            op: str,
            lineno: int,
            index: int):
        
        # The variable name
        self.name = name

        # The new value
        self.value = value

        # The assignment op
        self.op = op

        # The linenumber and index
        self.lineno = lineno
        self.index = index
    def resolve(self):
        return {
            "tokname": "var-assg",
            "type": "statement",
            "name": self.name.resolve(),
            "value": self.value.resolve(),
            "op": self.op,
            "lineno": self.lineno,
            "index": self.index
        }
        

class var_init_assg(statement):
    def __init__(self,
            var_type: name_literal,
            name: name_literal,
            value: expr,
            op: str,
            lineno: int,
            index: int):
        
        # The variable type
        self.var_type = var_type

        # The variable name
        self.name = name

        # The variable value
        self.value = value

        # The assignment op
        self.op = op

        # The linenumber and index
        self.lineno = lineno
        self.index = index
    def resolve(self):
        return {
            "tokname": "var-init-assg",
            "type": "statement",
            "var-type": self.var_type.resolve(),
            "name": self.name.resolve(),
            "value": self.value.resolve(),
            "op": self.op,
            "lineno": self.lineno,
            "index": self.index
        }
        


class return_statement(statement):
    def __init__(self, value: expr, lineno:int, index: int):
        # The value
        self.value = value

        # The linenumber and index
        self.lineno = lineno
        self.index = index
    def resolve(self):
        return {
            "tokname": "return",
            "type": "statement",
            "value": self.value.resolve(),
            "lineno": self.lineno,
            "index": self.index
        }
        
