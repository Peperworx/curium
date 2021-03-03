
def map_type(typ):
    return typ

def compile(in_tree, out = "", parent=None, nesting = 0):
    """
        Recurses over the tree, generating LLVM code.
    """
    
    t_type = in_tree["type"]

    if t_type == "body":
        for s in in_tree["statements"]:
            out = compile(s,out, parent=parent, nesting=nesting)
            return out
    elif t_type == "funcdef":
        out += "\n"
        out += f"define {map_type(in_tree['returns'])} {in_tree['name']} ()"+"{\n"
        nesting += 1
        for s in in_tree["contents"]:
            out = compile(s, out, parent = in_tree, nesting=nesting)
            out += "\n"
        out += "}"
        return out
    elif t_type == "statement":
        if in_tree["name"] == "return":
            nst = '    '*nesting
            out += f"{nst}ret {parent['returns']} {in_tree['arguments'][0]}"
            return out
    else:
        print(t_type)
        return out