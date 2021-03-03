class Compiler:

    def __init__(self):
        self.symbol_table = {}

    def map_type(self, typ):
        return typ


    def resolve_body(self, in_tree, out = "", parent=None, nesting = 0):
        for s in in_tree["statements"]:
            out = self.compile(s, out=out, parent=parent, nesting=nesting)
        return out

    def resolve_funcdef(self, in_tree, out = "", parent=None, nesting = 0):
        out += "\n"
        out += f"define {self.map_type(in_tree['returns'])} {in_tree['name']} ()"+"{"
        nesting += 1
        for s in in_tree["contents"]:
            out = self.compile(s, out, parent = in_tree, nesting=nesting)
            out += "\n"
        out += "}\n"
        return out

    def resolve_return(self, in_tree, out = "", parent=None, nesting = 0):
        nst = '    '*nesting
        out += f"{nst}ret {parent['returns']} {in_tree['arguments'][0]}"
        return out
    
    def resolve_value(self, value):
        return value["value"]

    def create_global_variable(self, in_tree, nesting = 0):
        """
            Constructs an LLVM global variable
        """

        val = {
            "type":"variable",
            "second_type": in_tree["var_type"],
            "mutable": in_tree["mutable"],
            "name": in_tree["name"],
            "global":True
        }

        # If it is in the symbol table, add
        if in_tree["name"] in self.symbol_table.keys():
            self.symbol_table[in_tree["name"]].append(val)
        else:
            self.symbol_table[in_tree["name"]] = [val]

        # Now create the variable
        var = f'@{val["name"]}.{len(self.symbol_table[val["name"]])-1} = global {self.map_type(val["second_type"])} {self.resolve_value(in_tree["value"])}'

        # And return
        return var
    
    def create_local_variable(self, in_tree, nesting = 0):
        """
            Constructs an LLVM global variable
        """

        val = {
            "type":"variable",
            "second_type": in_tree["var_type"],
            "mutable": in_tree["mutable"],
            "name": in_tree["name"],
            "global":False
        }

        # If it is in the symbol table, add
        if in_tree["name"] in self.symbol_table.keys():
            self.symbol_table[in_tree["name"]].append(val)
        else:
            self.symbol_table[in_tree["name"]] = [val]

        # Now create the variable
        ident = '    '*nesting
        if in_tree["mutable"]:
            var =  f'{ident}%{val["name"]}.{len(self.symbol_table[val["name"]])-1} = alloca {self.map_type(val["second_type"])}\n'
            var += f'{ident}store {self.map_type(val["second_type"])} {self.resolve_value(in_tree["value"])}, {self.map_type(val["second_type"])}* {val["name"]}.{len(self.symbol_table[val["name"]])-1}'
        else:
            var = f'{ident}%{val["name"]}.{len(self.symbol_table[val["name"]])-1} = {self.map_type(val["second_type"])} {self.resolve_value(in_tree["value"])}'

        # And return
        return var

    def resolve_vardef(self, in_tree, out = "", parent=None, nesting = 0):
        print(in_tree)
        if nesting == 0:
            out += self.create_global_variable(in_tree, nesting)
        else:
            out += self.create_local_variable(in_tree, nesting)
        return out

    def compile(self, in_tree, out = "", parent=None, nesting = 0):
        """
            Recurses over the tree, generating LLVM code.
        """

        t_type = in_tree["type"]

        if t_type == "body":
            # Resolve a body
            out = self.resolve_body(in_tree, out=out, parent=parent, nesting=nesting)
        elif t_type == "funcdef":
            out = self.resolve_funcdef(in_tree, out=out, parent=parent, nesting=nesting)
        elif t_type == "statement":
            if in_tree["name"] == "return":
                out = self.resolve_return(in_tree, out=out, parent=parent, nesting=nesting)
        elif t_type == "vardef":
            out += "\n"
            out = self.resolve_vardef(in_tree, out=out, parent=parent, nesting=nesting)
        else:
            print(in_tree)
        return out