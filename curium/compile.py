starting_table = {
    "functions": [],
    "globals": []
}

class CuriumCompiler:
    def _retrieve_function_locals(self, func_tree):
        """
            Using the parse tree of a function, find all local variable definitions
        """
        # Not implemented
        return []
    
    def _verify_function_signature(self, funcsig):
        """
            Verifies the parsed function signature.
        """
        
        # Confirm that name is of type name
        assert funcsig[1][1] == 'name', 'function_is_not_name'

        

    def _build_symbol_table(self, tree, typeinfo=starting_table):
        """
            Builds type information from a parse tree
        """

        # Iterate over each member of tree
        for i in tree:
            # If it is a function, add to function typeinfo
            if i[0] == 'function':
                
                # Run verification
                self._verify_function_signature(i)

                # Create table entry
                entry = {
                    "name": i[1][2],
                    "args": i[2][1:] or [],
                    "return": i[3] or "void",
                    "locals": self._retrieve_function_locals(i),
                }

                # Add the table entry
                typeinfo["functions"].append(entry)
        return typeinfo

    def _resolve_type(sel, typ):
        r = "none"
        if typ == "int":
            r = "i32"
        return r

    def _funcgen(self, func, type_info):
        """
            Generates wasm code for a funcion
        """

        # Grab func into
        finfo = None
        for f in type_info["functions"]:
            if f["name"] == func[1][2]:
                finfo = f
                break
        if not finfo:
            raise RuntimeError(f"Function {func[1][2]} not found in symbol table")

        ret = f"(result {self._resolve_type(finfo['return'][2])})" if finfo["return"] != "none" else None

        return f"(func ${finfo['name']} {ret if ret else ''} \n)"

    def _codegen(self, in_tree, type_info):
        """
            Generates wasm code
        """
        code = ["(module"]

        for i in in_tree:
            
            if i[0] == 'function':
                
                # Generate function
                code += [self._funcgen(i, type_info)]
        
        code += ")"

        return code
    def compile(self, in_tree):
        """
            Converts a parsed tree into web assembly
        """

        # Build type information
        symbol_table = self._build_symbol_table(in_tree)
        
        # Generate code
        gen = self._codegen(in_tree, symbol_table)
        print(in_tree)
        

        return '\n'.join(gen)