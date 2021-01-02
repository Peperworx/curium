## 0.0.1-dev WIP
This version is a work in progress.

This includes a full refractor of the lexer and parser. The first version of the lexer and parser is buggy, and uses tuples and lists in excess. This will be moving towards a more object oriented approach. Either way, the parser will require a second pass. (First to parse the program, next to parse the parse tree to a better, more readable format)

Note for this version: tuples are simply commas as binary operators with the highest precedence.


## 0.0.0
Basic parser and lexer finished. Basic bytecode assembler in progress.