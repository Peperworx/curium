from os import stat


class expr:
    pass

class empty_expr(expr):
    def __init__(self, lineno: int, index: int):
        self.lineno = lineno
        self.index = index
    def resolve(self):
        return ('empty-expr', (self.lineno,self.index))

class statement:
    pass

class empty_statement(statement):
    def __init__(self, lineno: int, index: int):
        self.lineno = lineno
        self.index = index
    def resolve(self):
        return ('empty-statement',(self.lineno,self.index))

class expr_statement(statement):
    def __init__(self, value: expr, lineno: int, index: int):
        # Set the expression value
        self.value = value

        # Lineno and index
        self.lineno = lineno
        self.index = index
    def resolve(self):
        return ('expr-statement',self.value.resolve(),(self.lineno,self.index))
class namespace(expr):
    def __init__(self,
            statements: list[statement]):
        # The actual list of statements
        self.statements = statements
        
    def resolve(self):
        return ('namespace', [s.resolve() for s in self.statements])
        


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
        return ('binary-op',self.op, self.left.resolve(), self.right.resolve(), (self.lineno,self.index))

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
        return ('unary-op',self.op, self.operand.resolve(), (self.lineno,self.index))

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
        return ('function-call',self.name.resolve(), self.arguments.resolve(), (self.lineno,self.index))

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
        return ('function-literal', self.arguments.resolve(), self.contents.resolve(), (self.lineno,self.index))


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
        return ('integer-literal',self.value, (self.lineno,self.index))


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
        return ('string-literal', self.value, (self.lineno,self.index))

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
        return ('name-literal', self.value, self.annotation.resolve(), (self.lineno,self.index))

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
        return ('var-init',
            self.var_type.resolve(),
            self.name.resolve(),
            (self.lineno,self.index))

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
        return ('var-assign',
            self.name.resolve(),
            self.value.resolve(),
            self.op 
            (self.lineno,self.index))

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
        return ('var-init-assg',
            self.var_type.resolve(), 
            self.name.resolve(),
            self.value.resolve(),
            self.op,
            (self.lineno,self.index))


class return_statement(statement):
    def __init__(self, value: expr, lineno:int, index: int):
        # The value
        self.value = value

        # The linenumber and index
        self.lineno = lineno
        self.index = index
    def resolve(self):
        return ('return-statement',self.value.resolve(), (self.lineno,self.index))