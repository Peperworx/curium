# Curium

Curium is the specification for a webassembly based programming language for frontend development.


# Functions

Curium functions are defined like so:

```
def function_name(argname: typename, ...) -> return_type {
    
}
```

The entry point to a curium program is the main function:

```
def main() -> int {
    return 0;
}
```

## Exporting functions

Curium can export functions for use from javascript and other WASM modules like so:

```
export def function_name(args...) -> return_type {

}
```







