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
                        label_name
                    )
                ]
                # Continue
                continue
            
            # If it is not a label, assume instruction


            # Get the instruction name
            instruction_name = child.children[1].text

            # Resolve the argument list
            arglist = self._resolve_arglist(child.children[3],i)
            
            # Resolve the instruction
            instruction = (
                "instruction",
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

        # For every argument
        for argument in arglist.children:
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

class Assembler:
    opcodes: list[Opcode] = [
        Opcode(
            name = "mov",
            opcode = 0x00,
            function = 0x00,
            numargs = 2
        ),
        Opcode(
            name = "print",
            opcode = 0x01,
            function = 0x00,
            numargs = -1
        ),
    ]
    def __init__(self,opcodes=[]):
        self.opcodes += opcodes
    
    def _encode_instruction(self,instruction):
        output = bytearray()

        # First Lets find the opcode
        opname = instruction[1]

        fopcode = None

        for opcode in self.opcodes:
            if opcode.name == opname:
                fopcode = opcode
                break
        
        # If we found it, great!
        # If not, we need to throw an error
        if not fopcode:
            print(f"Opcode not found: f{opname}")
            sys.exit(2)
        
        print(fopcode)


        return bytes()

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