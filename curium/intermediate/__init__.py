
from curium.lexer.tokens import ELSE, IF
from sly import Parser as SlyParser
from sly import Lexer as SlyLexer
from rich import print
import random
import os

# Pylance errors go byby
_ = lambda v: print(v)

class Lexer(SlyLexer):
    tokens = {
        NAME,
        BUILTIN,
        LPAREN, RPAREN,
        LBRACE, RBRACE,
        LBRACK, RBRACK,
        PCT,
        COMMA,
        COLON,
        SEMICOLON,
        PERIOD,
        LT, GT,
        LTEQ, GTEQ,
        EQU, NEQU,
        DECIMAL,
        HEX,
        BIN,
        IF, ELSE, ELIF,
        PTR,
        DS,
        FUNCTION
    }

    # Ignore spaces and tabs.
    ignore = ' \t'

    # Names
    NAME = r"%[a-zA-Z_][a-zA-Z0-9_\.]*"
    BUILTIN = r"[a-zA-Z_][a-zA-Z0-9_\.]*"
    BUILTIN["if"] = IF
    BUILTIN["else"] = ELSE
    BUILTIN["elif"] = ELIF
    BUILTIN['ptr'] = PTR
    BUILTIN['function'] = FUNCTION

    # Parentheses and brackets
    LPAREN = r'\('
    RPAREN = r'\)'
    LBRACE = r'\{'
    RBRACE = r'\}'
    LBRACK = r'\['
    RBRACK = r'\]'

    # Percent symbol
    PCT = r"%"

    # Comma
    COMMA = r','

    # Colon and semicolon
    COLON = r':'
    SEMICOLON = r';'

    # Period for member access
    PERIOD = r'\.'

    # Dollar sign
    DS = r'\$'

    # A bunch of compairison symbols.
    EQU = r'=='
    NEQU = r'!='
    GT = r'>'
    LT = r'<'
    GTEQ = r'>='
    LTEQ = r'<='


    # Decimal Integers
    @_(r"[0-9]+")
    def DECIMAL(self, v):
        v.value = int(v.value)
        return v
    
    # Hex integers
    @_(r"0x[a-fA-F0-9]*")
    def HEX(self, v):
        v.value = int(v.value[2:],16)
        return v
    
    # Bin integers
    @_(r"0b[0-1]*")
    def BIN(self, v):
        v.value = int(v.value[2:],2)
        return v

    # Newlines should increment lineno
    @_(r'\n+')
    def newline(self, v):
        self.lineno += len(v.value)

class Parser(SlyParser):
    tokens = Lexer.tokens



    # The entire file is just a list of instructions
    @_('insts')
    def file(self, v):
        return v[0]

    # A namespace is { insts }
    @_('LBRACE insts RBRACE')
    def namespace(self, v):
        return ['ns',v[1]]
    
    @_('LBRACE RBRACE')
    def namespace(self, v):
        return ['ns',None]
    

    # For a list of instructions
    @_('semiinst insts')
    def insts(self, v):
        out = ['insts',v[0]]
        if v[1][0] == "inst":
            out.append(v[1][1])
        elif v[1][0] == "insts":
            out.extend(v[1][1:])
        return out
    @_('semiinst')
    def insts(self, v):
        return ["inst",v[0]]

    @_('statement')
    def semiinst(self,v):
        return v[0]

    # Function definition
    @_("FUNCTION LPAREN udefname RPAREN namespace")
    def statement(self,v):
        return ["function",v[0],v[2],v[4]]


    # Conditional
    @_("if_statement")
    def statement(self,v):
        return ["conditional",v[0],None,None]
    
    @_('if_statement else_statement')
    def statement(self,v):
        return ["conditional",v[0],None,v[1]]
    
    
    @_('if_statement elif_chain')
    def statement(self,v):
        return ["conditional",v[0],v[1],None]
    
    
    
    @_('if_statement elif_chain else_statement')
    def statement(self,v):
        return ["conditional",v[0],v[1],v[2]]

    # Elif chain
    @_("elif_statement")
    def elif_chain(self,v):
        return ['elif-chain',v[0]]
    
    @_("elif_statement elif_chain")
    def elif_chain(self,v):
        return ['elif-chain',v[0],*v[1][1:]]


    # If statement
    @_("IF LPAREN compair RPAREN namespace")
    def if_statement(self,v):
        return ['if',v[2],v[4]]
    
    
    @_("ELIF LPAREN compair RPAREN namespace")
    def elif_statement(self,v):
        return ['elif',v[2],v[4]]

    @_("ELSE namespace")
    def else_statement(self,v):
        return ['else',v[1]]
    
    # Compairison
    @_(
        "EQU",
        "NEQU",
        "GT",
        "LT",
        "GTEQ",
        "LTEQ"
    )
    def compair(self,v):
        return v[0]

    

    
    
    # Rule for a single instruction with semicolon
    @_('instruction SEMICOLON')
    def semiinst(self,v):
        return v[0]

    # A single instruction call
    @_('builtin instructioncall')
    def instruction(self, v):
        return ["icall",v[0],v[1]]

    

    # Rule for instructioncall
    @_('LPAREN args RPAREN')
    def instructioncall(self,v):
        return ['call'] + v[1][1:]
    
    @_('LPAREN RPAREN')
    def instructioncall(self,v):
        return ['call']


    # A list of instruction arguments
    @_("arg COMMA args")
    def args(self,v):
        out = ['args',v[0]]
        if v[2][0] == "arg":
            out.append(v[2][1])
        elif v[2][0] == "args":
            out.extend(v[2][1:])
        return out
    

    @_("arg")
    def args(self,v):
        return ['arg',v[0]]


    # For a instruction argument
    @_('number','builtin','udefname','ptr','stackmember')
    def arg(self,v):
        return v[0]
    
    @_('DS DECIMAL')
    def stackmember(self,v):
        return ['stack',v[1]]
    
    @_('PTR COLON arg')
    def ptr(self, v):
        return ['pointer',v[2]]

    # Rule for builtins
    @_('BUILTIN')
    def builtin(self,v):
        return ['builtin',v[0]]

    # Rule for user defined names
    @_('names')
    def udefname(self,v):
        return ['udefname',v[0][1]]

    # To match names
    @_("NAME PERIOD names")
    def names(self,v):
        out = ['names',v[0]]
        if v[2][0] == "name":
            out.append(v[2][1])
        elif v[2][0] == "names":
            out.extend(v[2][1:])
        return out
    

    @_("NAME")
    def names(self,v):
        return ['name',v[0]]
    
    

    # To match numbers
    @_("HEX","DECIMAL","BIN")
    def number(self, v):
        return ['number',v[0]]

class CodeGen:
    def create_section(self,name,conts):
        print(name)
        print(conts)

    def __init__(self):
        self.ids = []


    def gen(self,input,sectid=""):
        return self.parse(input,isfirst=True)
    
    def inst_handle(self, conts):
        return ["instruction",conts[0][1],conts[1][1:]]
    def jump_from_condition(self,v,section):
        jump_table = {
            "==":"je",
            "!=":"jne",
            ">":"ja",
            ">=":"jae",
            "<":"jb",
            "<=":"jbe"
        }
        
        return [
            [
                "instruction", 
                jump_table[v],
                [["udefname",section]]
            ]
        ]



    def conditional_handle(self,cond,sectid=""):
        """
            This function handles conditionals, and in theory, nested conditionals.
        """
        # These are the "sections" of
        # the conditional handlers that hold specific parts
        ifsect = cond[0][1:]
        elifsect = cond[1][1:]
        elsesect = cond[2][1] if cond[2] else None
        
        
        #################
        # ID Generation
        #################
        # Now we need to generate the id
        id = random.randint(0,0xFFFF)

        # And if it already exists, regenerate
        while id in self.ids:
            id = random.randint(0,0xFFFF)
        
        # Append it, So that we know if it exists
        self.ids.append(id)
        

        #################
        # Segment names
        #################

        # Generate the segment names

        # The description that describes every segment.
        # We only add sectid if it exists
        desc = f"{id}{f'_{sectid}' if sectid != '' else ''}"

        # if segment name
        ifseg = f"if_{desc}"

        # else segment name
        elseseg = f"else_{desc}"

        # and one for each elif
        elifsegs = [f"elif_{i}_{desc}" for i in range(len(elifsect))]

        # as well as one for the end of the conditional
        endlabel = f"sect_end_{desc}"

        
        # Now we need to start on output
        output = []

        ####################
        # Conditional Jumps
        ####################

        # These are the actual "conditional" part of the code
        # the statements are executed in the order
        # if, elif(s), else, the rest of the code.

        # If the conditional jump succeeds, then the rest won't be executed

        # Jump for if
        output.extend(self.jump_from_condition(ifsect[0],ifseg))

        # If the above jump succeeds, it will skip the rest
        # This happens for every jump

        # Do this for every elif
        for e,n in zip(elifsect,elifsegs):
            output.extend(self.jump_from_condition(e[1],f"%{n}"))

        # And for else, but only if else exists
        if elsesect:
            output.append(["instruction","jmp", [["udefname",f"%{elseseg}"]]])
        


        # Now we need a backup jump.
        # Each created segment will jump to the end,
        # But if for some reason none of the above jumps
        # succeed, we still need to skip the conditional.
        # This also happens if no else statement is provided.
        output.append(["instruction","jmp",[["udefname", f"%{endlabel}"]]])
        
        ####################
        # Label Generation
        ####################

        # Now we need to generate labels for each section
        # These are what the above jump commands jump to

        # If Label
        # Add the name of the label
        output.append(["label",f"%{ifseg}"])
        
        # Convert the contents to a form useable by the parse function
        ifsegdesc = ["insts",*ifsect[1][1][1:]]

        # Add the parsed contents, using the section id of the if segment
        output.extend(self.parse(ifsegdesc,sectid=ifseg))

        # Jump Ahead to the end of the conditional.
        # This will be skipped if if is never called
        output.append(["instruction","jmp",[["udefname",f"%{endlabel}"]]])
        

        # Do the same for elif
        for e,n in zip(elifsect,elifsegs):
            # Create label n
            output.append(["label",f"%{n}"])
            
            # Contents
            elifsegdesc = ["insts",*e[2][1][1:]]
            output.extend(self.parse(elifsegdesc,sectid=n))

            # Jump Ahead
            output.append(["instruction","jmp",[["udefname",f"%{endlabel}"]]])

        # And for else
        if elsesect:
            output.append(["label",f"%{elseseg}"])
            elsesegdesc = ["insts",*elsesect[1][1:]]
            output.extend(self.parse(elsesegdesc,sectid=elseseg))
            # Jump Ahead
            output.append(["instruction","jmp",[["udefname",f"%{endlabel}"]]])

        # And add a label that marks the end of the conditional
        output.append(["label", f"%{endlabel}"])

        # Return the output
        return output
    
    def function_handle(self, conts, sectid=""):
        out = []

        # Generate function name
        name = f"{f'{sectid}_' if sectid != '' else ''}{conts[1][1]}"

        # Add the skip jump
        out.append(["instruction","jmp",["udefname",f"%end_{name}"]])

        # Create a label of function name
        out.append(["label",f"%{name}"])
        
        # Add the functions contents
        out.extend(self.parse(["insts",*conts[2][1][1:]],name))
        
        # Add the function return
        out.append(["instruction","ret",[]])

        # Add the end label
        out.append(["label",f"%end_{name}"])

        return out

    def parse(self,input,sectid="",isfirst=False):
        # Get the tag
        tag = input[0]

        # Get the contents
        conts = input[1:]

        output = []

        # If it is an instruction list
        if tag == "insts":
            # If it is the first, then add the start tag
            if isfirst:
                output.append(["label", "_start"])
            
            # Now parse per instruction
            for i in conts:
                output.extend(self.parse(i))
        elif tag == "icall":
            # Append the instruction call
            output.append(self.inst_handle(conts))

        elif tag == "conditional":
            # Append the conditional definition
            output.extend(self.conditional_handle(conts,sectid))
        
        elif tag == "function":
            # append the function definition
            output.extend(self.function_handle(conts,sectid))
        
        return output