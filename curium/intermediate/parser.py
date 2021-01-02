from dataclasses import dataclass
from enum import Enum



@dataclass
class Address:
    pass

@dataclass
class Operator:
    # The common name of the operator
    # Must be all lowercase
    # For example: add
    name: str

    # The symbol for the operator
    # Cannot contain letters or numbers
    # For example: +
    symbol: str

    # If this is true, the operator
    # Is a unary operator
    unary: bool


class Operators(Enum):
    # Lets add a few basic operators
    add = Operator("add","+",False) # Binary addition
    sub = Operator("sub","-",False) # Binary subtraction
    mul = Operator("mul","*",False) # Binary multiplication
    div = Operator("div","/",False) # Binary division

@dataclass
class Instruction:
    # The address of the result of the operation
    result: Address

    # The address of the first operand
    left: Address

    # The address of the second operand
    right: Address

    # The operator
    operator: Operator

    # An instruction resolves to the format
    # [result =] [left] operator right

    # Unary operators are right associative
    # For example:
    # a = - a

    # Operators can also be on their own, without a result
    # Examples:
    # -- a
    # call a
    # push a
    
    # These correspond to this assembly:
    # DEC a
    # CALL a
    # PUSH a

    # There are no real calling conventions, 
    # and it is up to the code generator to provide its own


