---
sidebar: auto
---
# Introduction


Curium Lang is a conceptual programming language that will be implemented in Python once a "specification" is complete. This "specification" is in fact this documentation. The language will be designed to complete the documentation, one tutorial step at a time.

Curium is a C-like language with static typing that can be compiled to multiple targets. The primary target will be a custom assembly language that will assemble into a custom bytecode. This bytecode could then be interpreted or, as I plan to implement in the far future, converted to an ELF executable.

Versioning will be using [Semantic Versioning](https://semver.org/) with a twist. Every tutorial step will be a minor version, and every tutorial section will be a major version.

## Why Python??

Python is great for prototyping software fast. Using Python features like decorators, kerword arguments, dictionaries, the large standard library, and various tools that are available, we can create an easy to use interface that allows users to expand upon Curium (For Example: Providing custom standard library modules and builtin functions.)

### Isn't Python Slow?

Not really. Using many language features of python (list comprehensions, C libraries, threading, etc) we can optimize code alot. However, python will be used only for the compiler and assembler. The interpreter will be written in C++ and compiled as a dynamic library. This will then be loaded and called from python using ctypes.


## Language Details

### How will this language be typed?

Curium will be statically typed. Every variable will have a type, but unlike other statically typed languages, variables types can be reassigned. This is possible because every type is at it's core just an array of bytes. Different parts of the array mean different things. Due to the nature of computers, however, this will only be available for the interpreted version. For the compiled version, this will be less efficient, simply creating a new variable and casting the original value to that new variable, as opposed to realocating the original variable. 

### Everything is an object/type

Function? Object. Number? Object. String? Object. Class? Object. Struct? Object. This means that we can pass functions, structs, numbers, etc around effortlessly. On the top, it will seem a lot like python. Define a function, and it is the same as a callable class.  


## Step 1 Compiler Details

The step 1 compiler is an integral part of this language concept. It converts a parse tree to a custom assembly code which is then assembled into a custom bytecode. This bytecode can then be intepreted or compiled.

## Assembler Details

The assembler will convert the custom assembly code into bytecode. More details on this once I get this 100% working. (I actually have a working demo right now, but it sucks.)

## Interpreter Details

### Memory Management

The interpreter will manage memory with a 100% custom memory allocator. The interpreter will store the program's memory in a custom list/vector of chars. This allows us to be super efficient with our memory use, and reduce overhead from possible "extra features" that build in memory managers provide. All we need is malloc and free. We will go into more details once an interpreter is in progress.

## Step 2 Compiler Details

The step 2 compiler will be super similar to the interpreter. It will interpret the bytecode, but instead of performing actions based on what it sees, it will generate NASM assembly from the program.

## The Tutorial

As I said, Curium will use Documentation Driven Devlopment, as (in my opinion) the best way to plan is to have a thorough understanding of how it the end result will work. This will be accomplished by means of a tutorial. As I said above, each step of a tutorial will be a minor version, and each section a major version. Patch versions are for security and bug fixes only.
You can start the tutorial by going [here](/tutorial/).

## More about this language
You can find out details [here](/about/more) And about the intermediate language [here](/about/intermediate)
