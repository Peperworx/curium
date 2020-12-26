import re

class PreProcessor:
    knownNames: dict[str,str]
    regexString: re.Pattern = re.compile(
        r"(\'.*?\'|\".*?\")"
    )
    def __init__(self,knownNames: dict[str,str] = {}) -> None:
        self.knownNames = knownNames
    def directive(self,directive):
        # Split the percent symbol
        directive = directive.split("%")[1]
        dFiltered = []
        # Now split by whitespace and filter
        for d in directive.split():
            if d.strip():
                dFiltered.append(d)
        directive = dFiltered

        # If it is a define
        if directive[0] == "define":
            # Define the name, joining the next arguments by spaces
            self.knownNames[directive[1]] = " ".join(directive[2:])
        
    def splitNotInStr(self,value: str,delimeter: str) -> list[str]:
        # Every string starts with a \" or a \'
        # And ends with the same

        # When defining macros, we do not want to replace values specified in strings.
        # (Unless surrounded with % symbols)
        

        # Lets regex split by string
        split = re.split(self.regexString,value)
        
        output = [""]

        # And iterate over each string
        for s in split:
            # If it is a string literal, ignore
            if re.match(self.regexString,s):
                output[-1] += s
                continue
            s = s.split(delimeter)
            output[-1] += s[0]
            output.extend(s[1:])
            

        return [o for o in output if not o.strip().isspace()]


    def filter(self,to_filt: str) -> str:
        out = to_filt
        for k,v in self.knownNames.items():
            r = self.splitNotInStr(out,k)
            out = str(v).join(r)
        

        return out
    
    def stripComments(self,in_str:str):
        # Strip every character between a // and a newline that is not in a string
        splitByStrings = re.split(self.regexString,in_str)
        for i,v in enumerate(splitByStrings):
            # If it is a string, ignore
            if i % 2 != 0:
                continue
            
            # If it is not, then every character between a // and a newline needs to be removed
            r = re.split(r"//.*(?=\n)*",v)
            splitByStrings[i] = "".join(r)
        
        splitByStrings = re.split(self.regexString,"".join(splitByStrings))
        # Now we have removed all single line comments
        
        # Multi line comments will be implemented at a later time

        in_str = "".join(filter(None,splitByStrings))

        return in_str
    def process(self,in_str:str):
        # First strip comments
        in_str = self.stripComments(in_str)

        # First get each line
        lines = in_str.split("\n")

        filtered_lines = []
        # Then iterate over each line
        for line in lines:
            # Strip the comments
            #line = line.split("//")[0]
            # If it is a preprocessor directive
            if line.startswith("%"):
                # Process it
                self.directive(line)
            else:
                # If it is not
                # Then filter it for macros
                # And append to filtered_lines
                filtered_lines.append(
                    self.filter(line)
                )
        
        # Rejoin it with newlines
        in_str = "\n".join(filtered_lines)

        return in_str