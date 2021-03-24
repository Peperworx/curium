# Curium

Curium has gone through many, many stages. First it was intended to be a full programming language, next it was intended to be an intermediate language, then a full programming language, and now, finally, Curium is a virtual machine and assembly language designed for implementation in other languages.

This document describes the specification of this final form, the form of an assembly language.

## Instructions

Curium is based off of instructions. Instructions have two forms: stack operations and register/immediate/memory operations.

### Stack operations

Stack operations are the simplest, and the simplest of all stack operations is `pushi`.

Stack operations generally take a single argument. This argument can be many things, but in the case of `pushi` this argument is a 64 bit intermediate value.

`pushi` pushes an intermediate value to the current stack. 

Here is an example:
```
pushi 0b01010101
```
Notice how this example shows an 8 bit value and not a 64 bit value? The assembler automatically expands it to a 64 bit value with the same value. Values larger than 64 bits are split into two instructions.

Here is the structure of a stack operation:

- Operation type (1 bit)
    - This is equal to 0 for stack based operations
- Operation subtype (7 bits)
- Opcode (8 bits)
- Argument (64 bits)

A stack operation instruction is 10 bytes long. These are padded with zeroes and take up a final size of 28 bytes.

### Other operations

Other operations have the same header as stack based operations, but use a different format from other operations.

- Operation type (1 bit)
    - This is 1 for other operations
- Operation subtype (7 bits)
- Opcode (8 bits)
- Argument Type Specifiers (8 bits)
- Argument Size Specifiers (8 bits)
- Argument (64 bits)
- Argument (64 bits)
- Argument (64 bits)

Each instruction takes up 28 bytes.

Each type specifier specifies the type of the argument:
0 - register
1 - immediate
2 - memory address
3 - label

Each size specifier specifies the size of the argument. This is only needed for memory addresses:
0 - 1 byte
1 - 2 bytes
2 - 4 bytes
3 - 8 bytes

The second to last and last bits are modifiers for the first two arguments.
If either of the bits is set, here is the values for the sizes of the first two arguments, based off of their size specifiers
0 - 16 bytes
1 - 24 bytes
2 - 32 bytes
3 - 64 bytes





