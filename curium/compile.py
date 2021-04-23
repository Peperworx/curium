starting_table = {
    "functions": [],
    "variables": []
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
                    "return": self._resolve_type(i[3][2] or "void"),
                    "variables": self._retrieve_function_locals(i),
                }

                # Add the table entry
                typeinfo["functions"].append(entry)
        return typeinfo

    def _resolve_type(self, typ):
        
        r = "none"
        if typ == "int":
            r = "i32"
        return r

    def _funcgen(self, func):
        """
            Generates wasm code for a funcion
        """

        # Grab func into
        finfo = None
        for f in self.type_info["functions"]:
            if f["name"] == func[1][2]:
                finfo = f
                break
        if not finfo:
            raise RuntimeError(f"Function {func[1][2]} not found in symbol table")

        ret = f"(result {self._resolve_type(finfo['return'][2])})" if finfo["return"] != "none" else None

        return f"(func ${finfo['name']} {ret if ret else ''} \n{self._statementsgen(func)})"

    def _get_expr_result_type(self, expr, func=None):
        """
            Gets the resulting type of an expression
            These types are determined by precedence 
            (so if an operation has a and b as operands, the operand with the highest precedence is chosen)
            Floats have a higher precedence than integers, and 64 bit values have a higher 
            precedence than 32 bit numbers.
            
            So i32 + i64 will be i64
            f32 + f64 will be f64
            f64 + i32 will be f64
            f32 + i64 will be f64
        """
        
        if expr[0] == "literal":
            # Handle code for literals

            # If it is a name literal, return the type
            if expr[1] == "name":
                
                
                # Search in locals for the name
                if func:
                    f=None
                    for f in self.type_info["functions"]:
                        if f["name"] == function[1][2]:
                            break
                    for v in f["variables"]:
                        if v["name"] == expr[1]:
                            return v["type"]
                # If We can not find in locals, search globals
                for v in self.type_info["variables"]:
                    if v["name"] == expr[1]:
                        return v["type"]
                # If this failed, return none
                return None
            elif expr[1] == "integer":

                # If it is above 0xFFFFFFFF then it is 64 bit, if not, 32 bit
                if expr[2] > 0xFFFFFFFF:
                    return "i64"
                else:
                    return "i32"

    def _generate_expression(self, expr, out:list[str] = []):
        """
            Generates WASM code for an expression
        """
        
        if expr[0] == "literal":
            # If it is a literal, just add to stack
            if expr[1] == "integer":
                out += [f"{self._get_expr_result_type(expr)}.constant {expr[2]}"]
        
        return out

    def _statementsgen(self, function):
        """
            Generates WASM code by compiling a list of statements in a function
        """

        out = []

        for s in function[4][1:]:
            # Switch on each statement, generating code for each one
            if s[0] == "function_call": # If a function call
                # Call the function
                out += [f"call ${s[1][2]}"]
            elif s[0] == "return": # If it is a return statement
                # Return statements simply resolve the expression,
                # And make sure the value is on the stack
                
                # Grab the type of the result
                restype = self._get_expr_result_type(s[1])
                
                # Grab from typeinfo
                f=None
                for f in self.type_info["functions"]:
                    if f["name"] == function[1][2]:
                        break
                if not f:
                    raise Exception(f"Function {function[1][2]} Not found in type info")
                # Get the size of the result type
                ressize = int(restype[1:])
                # get size of return type
                retsize = int(f["return"][1:])
                
                # If the retsize is >= the ressize we are good to go
                if retsize < ressize:
                    raise Exception(f"Invalid return type for function {f['name']}")
                
                # If all good, lets generate the expression
                out.extend(self._generate_expression(s[1],[]))
                
        
        return '\n'.join(out+[""])

    def _codegen(self, in_tree):
        """
            Generates wasm code
        """
        code = ["(module"]

        for i in in_tree:
            
            if i[0] == 'function':
                
                # Generate function
                code += [self._funcgen(i)]
        
        code += ")"

        return code
    def compile(self, in_tree):
        """
            Converts a parsed tree into web assembly
        """

        # Build type information
        self.type_info = self._build_symbol_table(in_tree)
        
        # Generate code
        gen = self._codegen(in_tree)
        

        return '\n'.join(gen)