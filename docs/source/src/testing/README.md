# Steps for Testing


For each tutorial step, the step must pass these stages of processing and compilation in order.

1. Preprocessor
   - All Macros must successfully resolve
   - All comments must be striped
   - Verify by hand.
2. Parser
   - The syntax must parse without any errors.
   - The parser must generate a valid parse tree.
   - The parse tree must match the code.
   - Verify by hand
3. Compiler
   - Parse Tree must compile to valid custom assembly.
   - Assembly must result in desired action
   - Verify by hand
4. Assembler
   - Must produce valid bytecode.
   - Bytecode must match the assembly
   - Hand check by dissassembling, compareing, and reassembling
5. Interpreter
   - Must produce desired result.
   - Verify by hand
