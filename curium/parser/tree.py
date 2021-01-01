class expr:
    pass


class statement:
    pass

class namespace(expr):
    def __init__(self,
            statements: list[statement]):
        # The actual list of statements
        self.statements = statements



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

class function_call(expr):
    def __init__(self, 
            name: str, 
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





class var_initialize(statement):
    def __init__(self, 
            var_type: expr,
            name: str):

        # The type of the variable
        self.var_type = var_type

        # The name of the variable
        self.name = name

class var_assign(statement):
    def __init__(self,
            name: str,
            value: expr):
        
        # The variable name
        self.name = name

        # The new value
        self.value = value

class var_init_assg(statement):
    def __init__(self,
            var_type: expr,
            name: str,
            value: expr):
        
        # The variable type
        self.var_type = var_type

        # The variable name
        self.name = name

        # The variable value
        self.value = value


