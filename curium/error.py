def strip_whitespace(inlex):
    """
        Strips whitespace from a list of tokens
    """
    for i in inlex:
        if i.type not in ["SPACE","NEWLINE"]:
            yield i

class CuriumErrorHandler():
    def __init__(self, file, lexer):
        self.file = file
        self.lexer = lexer
    def show(self, err):
        err.show(self.file,self.lexer)

class CuriumError():
    def __init__(self, msg):
        self.msg = msg
    def show(self):
        print(msg)

class NameAlreadyDefined():
    def __init__(self, name, index):
        self.name = name
        self.index = index
    def show(self, file, lexer):
        

        offset = 0
        line = 0
        lexed = lexer.tokenize('\n'.join(file))
        i = None
        for i in lexed:
            if i.index == self.index:
                break
            
            offset += len(i.value)
            if i.type == "NEWLINE":
                offset = 0
                line+=1
        
        print(f"Error on line {line+1}: Name '{self.name}' already defined")
        print(file[line])

        print(f"{' '*(file[line][offset:].find(self.name))}{'^'*len(self.name)}")

