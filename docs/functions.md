# Functions

This section fully describes functions.

## Definition

Here is the basic example of a main function:

```cpp
def main() -> i32{
    return 0;
}
```

This maps down to the following LLVM:

```LLVM
define i32 @_ZNE_main_F_i32() {
    ret i32 0
}
```

