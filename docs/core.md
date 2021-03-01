# Core specification

This page defines some of the core Curium specification, such as the built in calling convention, name mangling, etc.

## Name Mangling

Names are mangled for a variety of reasons:
- Keeping namespaces
- Keeping scope (classes)
- Function overloading
- Debugging

The format in which names are to be mangled is described in this section. By unmangling the name, a function prototype, as well as the tree leading up to the name can be regnerated.
