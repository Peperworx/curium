

## 0.0.2-dev WIP
This development version is a work in progress.

This version removes the work in progress assembly language, and introduces an intermediate intermediate language (Yes, the two intermediates were intentional.) This language is super basic, supports strict typing, and a super basic system for implementing structures and classes.

This language compiles to llvm IR using the llvmlite library

Note: This ir uses peg parsing, as opposed to Lex/Yacc. This is acomplished using [parsimonious](https://github.com/erikrose/parsimonious).

## 0.0.1-dev
This development version includes a rewrite of the initial compiler, with a new parse tree and name system.

Much of the code, however, is the same. The AST can be dumped to a dictionary, and from there into a JSON string.

## 0.0.0
Basic parser and lexer finished. Basic bytecode assembler in progress.