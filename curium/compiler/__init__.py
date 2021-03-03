class Compiler:

    def __init__(self):
        self.symbol_table = {
            "int32_t": [{
                "type":"typealias",
                "original":"s32"
            }]
        }
    
    def map_type(self, typename):
        """
            Converts a Curium type to it's LLVM equivilent, and returns
        """
        ...
    


    def preload_variable(self, variable_name):
        """
            Generates and returns the preload code of a variable
            This could be loading from memory, or it could be nothing.
            This also returns the variable that the value of the variable is stored in.
        """
        ...
    
    def add_symbol(self, name, value):
        """
            Adds a symbol with name and value to the symbol table
        """
        if name in self.symbol_table.keys():
            self.symbol_table[name].append(value)
        else:
            self.symbol_table[name] = [value]

    def handle_funcdef(self, in_tree: dict, **kwargs):
        """
            Generates LLVM code for a function definition.
        """

        # Preload out variable
        out_elem = kwargs.get("out")
        out = out_elem if out_elem else ""


        # Get the return type, defaulting to void if it does not exist
        return_type = in_tree.get("returns") if in_tree.get("returns") else "void"

        # Resolve the return type to LLVM standards
        resolved_type = self.map_type(return_type)


        # Register the function in the symbol table
        st_entry = {
            "type":"function",
            "symbol_table":[]
        }
        self.add_symbol(in_tree["name"],st_entry)
        
        


        # Return output code
        return out
        

    def compile(self, in_tree, **kwargs):
        """
            Recurses over the tree, generating LLVM code.
        """
        # Get the tree type
        in_type = in_tree["type"]

        # Get the out element from kwargs
        out_elem = kwargs.get("out")
        out = out_elem if out_elem else ""

        # If this is the code body, compile the contents
        if in_type == "body":
            for i in in_tree["contents"]:
                kwargs["out"] = out
                out = self.compile(i,**kwargs)
        elif in_type == "funcdef":
            # If it is a function definition, handle
            out = self.handle_funcdef(in_tree,**kwargs)
        else:
            print(in_type)
        return out