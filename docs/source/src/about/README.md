# Introduction


Peperworx Lang is a conceptual programming language that will be implemented in Python once a "specification" is complete. This "specification" is in fact this documentation. The language will be designed to complete the documentation, one tutorial step at a time.

This language is a C-like language with static typing that can be compiled to multiple targets. The primary target will be a custom assembly language that will assemble into a custom bytecode. This bytecode could then be interpreted or, as I plan to implement in the far future, converted to an ELF executable.

This language will be version using [Semantic Versioning](https://semver.org/) with a twist. Every tutorial step will be a minor version, and every tutorial section will be a major version.

## Why Python??

Python is a very dynamic programming language. We can twist things around, and make things feel the way we want when designing an interface to this language and its subset assembly/bytecode. For example: We can dynamically add new attributes to classes, and list the attributes of classes. We are also not limited on integer and string sizes. 
This language will be using and abusing typehints. Visual Studio Code, or a similar editor, should be able to give you intellisense (or whatever you are using) information for every step of the way. I will also do my best to comment the code as much as humanly possible.

## Isn't Python Slow?

Some Python code can be optimized to the point of running almost C-like levels. However, even if we were to optimize our compiler to that point, the speed would still not matter. While the compiler, parser, and frontend will be written in Python, it is really the interpreter that matters. The interpreter will be written in one of two forms: either a C++ shared library that is accessed by the ctypes module, or a C library for Python. Possibly even both. However, the first one (the shared library) is most likely to be developed first, as you could then embed it in other programming languages that support .dll and .so libraries.

