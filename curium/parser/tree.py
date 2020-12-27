class Expr:
    pass

class BinOp(Expr):
    def __init__(self, op, left, right, lineno, index):
        self.op = op
        self.left = left
        self.right = right
        self.lineno = lineno
        self.index = index
class Initialize(Expr):
    def __init__(self, new, type, value, lineno, index):
        self.new = new
        self.type = type
        self.value = value
        self.lineno = lineno
        self.index = index



class UnOp(Expr):
    def __init__(self, op, right, lineno, index):
        self.op = op
        self.right = right
        self.lineno = lineno
        self.index = index

class Group(Expr):
    def __init__(self, id, lineno, index, *args):
        self.all = args
        self.lineno = lineno
        self.index = index


class If(Expr):
    def __init__(self,op,expr,conts,nextSet = None):
        self.op = op
        self.expr = expr
        self.conts = conts
        self.nextSet = nextSet

class Elif(If):
    pass

class Else(Expr):
    def __init__(self,op,conts):
        self.op = op
        self.conts = conts

class EndNode(Expr):
    def __init__(self, value, lineno, index):
        self.value = value
        self.lineno = lineno
        self.index = index

class Number(EndNode):
    pass

class String(EndNode):
    pass

class Name:
    def __init__(self,value,template,lineno,index):
        self.value = value
        self.template = template
        self.lineno = lineno
        self.index = index

class Function:
    def __init__(self,contents,args):
        self.contents = contents
        self.args = args