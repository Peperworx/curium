starting_table = {
    "functions": [],
    "variables": []
}

class CuriumCompiler:
    def __init__(self):
        self.type_info = {
            "functions": [],
            "variables": []
        }

    def _find_function_locals(self, func):
        """
            Gets a list of all local variables in a function
        """

        # Not implemented yet
        return []
    
    def _resolve_variable_scope(self, name, scope=None):
        """
            Returns the information of a variable found in a scope.
            A scope can be the global scope (self.type_info)
            or a local scope of a function.

            Scope defaults to self.type_info
        """

        if not scope:
            scope = self.type_info

        for v in scope["variables"]:
            if v["name"] == name:
                return v
        
        return None
    
    def _determine_type_precedence(self, t1, t2):
        """
            Takes two types, t1 and t2.
            Returns a type that is created by the combination of the two types in a binop.
        """

        # If they are not default types, return the first one
        if (t1 not in ["f32","f64","i32","i64"] or
             t2 not in ["f32","f64","i32","i64"]):
            return t1

        # Grab the size of each
        t1size = int(t1[1:])
        t2size = int(t2[1:])

        # Grab the type of each
        t1type = t1[0] == "f"
        t2type = t2[0] == "f"

        # Select type
        t3type = max(t1type,t2type)
        
        # Select size
        t3size = max(t1size, t2size)

        return f"{['i','f'][t3type]}{str(t3size)}"

    def _resolve_types(self, in_tree):
        """
            Stores type information in self.type_info
        """

        # Iterate over
        for i in in_tree:
            
            if i[0] == 'function':
                self.type_info["functions"] += [
                    {
                        "name":i[1][2],
                        "args": i[2][1:],
                        "return": i[3][2],
                        "locals": self._find_function_locals(i)
                    }
                ]
            else:
                print(i)
    
    def _resolve_static_type(self, t):
        """
            Returns the WASM equivilent of a type
        """
        if t == "int":
            return "i32"

    


    def _codegen_expression(self, in_tree, scope, out: list = []):
        """
            Recursive function to generate WAT code for an expression tree
            Requires a scope. Can be global
        """

        if in_tree[0] == "literal": # if a literal
            if in_tree[1] == "integer":
                # Determine the type of the integer:
                
                itype = "i32"
                if in_tree[2] > 0xFFFFFFFF:
                    itype = "i64"
                
                # generate constant expression
                out += [f"{itype}.const {str(in_tree[2])}"]
        elif in_tree[0] == "function_call":
            # Very primitive function call
            # TODO Replace this
            out += [f"call ${in_tree[1][2]}"]
        


        return out
    def _codegen_statement(self, in_tree, scope):
        """
            Generates WAT code for a statement.
            Requires a scope, can be global.
        """
        out = []

        # If it is a return
        if in_tree[0] == 'return':
            # Generate the expression
            out += self._codegen_expression(in_tree[1][2],scope,[])
        elif in_tree[0] == 'expr':
            out += self._codegen_expression(in_tree[2],scope,[])

            # If it is a statement expression, drop the output
            if in_tree[1] == "statement":
                out += ["drop"]
        
        return out

    def _codegen_function(self, in_tree):
        """
            Generates WAT code for a function
        """
        
        # Generate function prototype
        proto = f"(func ${in_tree[1][2]} (result {self._resolve_static_type(in_tree[3][2])})"

        # Default out
        out = [proto]

        # For each statement, generate code for that statement.
        for s in in_tree[4][1:]:
            out += self._codegen_statement(s, in_tree)

        # Add ending paren of function
        out += [")"]

        return out
    def _codegen(self, in_tree):
        """
            Uses input tree to generate WASM text
        """

        out = ["(module"]

        # Now iterate over every part of the file, 
        # generating code for each

        for i in in_tree:
            # If a function, generate function code
            if i[0] == 'function':
                out += self._codegen_function(i)

        out += [")"]

        return '\n'.join(out)

    def compile(self, in_tree):
        """
            Converts a parsed tree into web assembly
        """
        
        # Resolve the types
        self._resolve_types(in_tree)
        
        

        # Begin codegen
        gen = self._codegen(in_tree)

        return gen