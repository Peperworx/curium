# Curium

Curium has gone through many, many stages. First it was intended to be a full programming language, next it was intended to be an intermediate language, then a full programming language, and now, finally, Curium is a virtual machine and assembly language designed for implementation in other languages.

This document describes the specification of this final form, the form of an assembly language.

## Instructions

Curium is based off of instructions. Instructions have two forms: stack operations and register/immediate/memory operations.

Stack operations are the simplest, and the simplest of all stack operations is `pushi`.

Stack operations generally take a single argument. This argument can be many things, but in the case of `pushi` this argument is a 64 bit intermediate value.

`pushi` pushes and intermediate value to the stack. 