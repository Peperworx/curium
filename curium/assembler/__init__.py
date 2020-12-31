from rich.console import Console
from pydantic import BaseModel
from rich import print
from .. import errors
import parsimonious
import rich
import sys
import os
import re

class Parser:
    def __init__(self):
        with open(
            os.path.join(
                os.path.dirname(__file__),
                "./asm.peg"
            )
        ) as f:
            self.grammar = parsimonious.Grammar(f.read())
    def parse(self,input):

        lines = input.split("\n")

        # Filter whitespace
        lines = [l for l in lines if l.strip()]
        # The output variable
        output = []

        # For every line
        for i,line in enumerate(lines):
            # Parse the line
            parsed_line = self.grammar.parse(line)
            
            # Get the instruction
            child = parsed_line.children[0]

            # If it is a label
            if child.expr.name == "label":
                # Get the label name
                label_name = child.children[1].text
                
                # Add the label to output
                output += [
                    (
                        "label",
                        (
                            i,
                            child.full_text,
                            child.start,
                            child.end
                        ),
                        label_name
                    )
                ]
                # Continue
                continue
            
            # If it is not a label, assume instruction


            # Get the instruction name
            instruction_name = child.children[1].text
            
            # Resolve the argument list
            arglist = self._resolve_arglist(child.children[2],i)
            
            # Resolve the instruction
            instruction = (
                "instruction",
                (
                    i,
                    child.full_text,
                    child.start,
                    child.end,
                    child.children[1].start,
                    child.children[1].end
                ),
                instruction_name,
                arglist
            )
            output.append(instruction)

        return tuple(output)

    def _resolve_integer(self,input,full,lineno):
        # Get error handler ready
        parserError = errors.CuriumParseError("Integer resolution error")
        # Initialize output to one
        output = None

        if input.startswith('0x'):
            output = int(input[2:],16)
        elif input.startswith('0o'):
            output = int(input[2:],8)
        elif input.startswith('0b'):
            output = int(input[2:],2)
        else:
            try:
                output = int(input.text,10)
            except:
                parserError.raiseExec(
                    f"Integer {input} does not match one of the build in integer types. Unable to resolve",
                    full.full_text,
                    lineno,
                    full.start,
                    full.end
                )
                sys.exit(1)
        
        return output

    def _resolve_arglist(self,arglist,lineno):
        
        # Output list
        output = []
        # Get error handler ready
        parserError = errors.CuriumParseError("Internal parser error")
        if not arglist.text.strip():
            return tuple([])
        # Lets get up a few levels
        arglist = arglist.children[0].children[1]
        
        # For every argument
        for argument in arglist.children[0]:
            # Get the value
            value = argument.children[0].children[0]
            
            # If it is an integer literal, resolve
            if value.expr.name == "integerliteral":
                value = self._resolve_integer(value.text,value,lineno)
                value = (
                    'integer-type',
                    value
                )
            
            # If it is a string literal, resolve
            elif value.expr.name == "string":
                # Remove the "
                stripped = str(value.text).lstrip("\"").rstrip("\"")
                
                # Set value
                value = (
                    'string-type',
                    stripped
                )
            
            # If it is a pointer, resolve
            elif value.expr.name == "pointer":
                if value.children[1].children[0].expr.name == "integerliteral":
                    value = self._resolve_integer(value.children[1].text,value,lineno)

                    value = (
                        'pointer-type',
                        value
                    )
                else:
                    value = (
                        'pointer-type-label',
                        value.children[1].text
                    )
            # Else, we are going to throw an error.
            else:
                # This error should never happen.
                
                parserError.raiseExec(
                    f"Argument type of [i]{value.expr.name}[/i] is not a valid argument type",
                    value.full_text,
                    lineno,
                    value.start,
                    value.end
                )
                sys.exit(1)

            output.append(value)
        
        return tuple(output)






class Opcode(BaseModel):
    name: str
    opcode: int
    function: int
    numargs: int
    argnames: list[str]

class Assembler:
    opcodes: list[Opcode] = [
        Opcode(
            name = "mov",
            opcode = 0x00,
            function = 0x00,
            numargs = 2,
            argnames = ["dest","src"]
        ),
        Opcode(
            name = "print",
            opcode = 0x01,
            function = 0x00,
            numargs = -1,
            argnames = ["input"]
        ),
    ]
    def __init__(self,opcodes=[]):
        self.opcodes += opcodes
    
    def _encode_instruction(self,instruction,labels={},defaultLabel=0x000):
        output = bytearray()

        # First Lets find the opcode
        opname = instruction[2]

        fopcode = None

        for opcode in self.opcodes:
            if opcode.name == opname:
                fopcode = opcode
                break
        
        # If we found it, great!
        # If not, we need to throw an error
        if not fopcode:
            opcodeNotFound = errors.CuriumParseError("Invalid opcode")
            opcodeNotFound.raiseExec(
                f"Opcode [i]{opname}[/i] is not a valid opcode",
                instruction[1][1],
                instruction[1][0],
                instruction[1][4],
                instruction[1][5]
            )
            sys.exit(2)
        
        # Verify the number of arguments
        if fopcode.numargs < len(instruction[3]) and fopcode.numargs >= 0:
            tooManyArguments = errors.CuriumParseError("Too many arguments")
            tooManyArguments.raiseExec(
                f"Opcode {fopcode.name} is unable to take more than {fopcode.numargs} arguments",
                instruction[1][1],
                instruction[1][0],
                instruction[1][5]+1,
                len(instruction[1][1].rstrip())-1
            )
            sys.exit(2)
        if fopcode.numargs > len(instruction[3]) and fopcode.numargs >= 0:
            notEnoughArguments = errors.CuriumParseError("Not enough arguments")
            notEnoughArguments.raiseExec(
                f"Opcode {fopcode.name} is missing argument{'s' if len(instruction[3]) - fopcode.numargs > 1 else ''} [i]{','.join(fopcode.argnames[len(instruction[3]):])}[/i]",
                instruction[1][1],
                instruction[1][0],
                instruction[1][4],
                instruction[1][3]
            )
            sys.exit(2)

        # At this point, the instruction matches
        # So lets generate it

        print(instruction)

        # The opcode
        opcode = fopcode.opcode

        # The arguments
        arguments = instruction[3]

        # Dump the opcode
        output += int.to_bytes(opcode,1,"little")

        # Dump the function/numargs
        output += int.to_bytes((fopcode.function<<4)|len(arguments),1,"little")

        

        print(output)
        return bytes(output)

    def assemble(self,input):

        # We need to make two passes.
        # One to extract the lables, and one to compile the bytecode

        # The first pass will also encode all instructions
        # This is so we can get the offset of the label

        # All labels will be replaced with a 16 bit integer (0xFFFF) until
        # The labels are resolved

        # Set the offset of the first pass
        fpoffset = 0

        # Create a dictionary to keep track of labels
        labeldict = {}

        # Now iterate over the input
        for inst in input:
            if inst[0] == "label":
                # If it is a label
                # Append the offset to the label table
                labeldict[inst[1]] = fpoffset
            if inst[0] == "instruction":
                # If it is an instruction, append its calculated size to fpoffset
                fpoffset += len(self._encode_instruction(inst))