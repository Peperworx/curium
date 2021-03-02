# Functions

This section fully describes functions.

## Definition

Here is the basic example of a main function:

```cpp
def main() -> i32 {
    return 0;
}
```

This maps down to the following LLVM:

```LLVM
define i32 @_ZNE_main_F_i32() {
    ret i32 0
}
```

Easy. What about a function with arguments?

```cpp
def main(i32 a) -> i32 {
    return a;
}
```

Again, this maps to the following LLVM:

```LLVM
define i32 @_ZNE_main_F_i32_i32_a(i32 %a){
    ret i32 %a
}
```

The reason why functions are introduced first in the documentation is because every other example will use a main function, similar to C.

## Variable Arguments

Having a variable number of arguments is designed to be ease, like in languages such as python.

A variable number of arguments may be expressed by adding a `...` to the end of an argument. For example:

```rust
def sum(i32 a...){
    let mut s:i32 = 0;
    for(i32 i = 0; i < a.count; i++){
        s += a.values[i];
    }
    return s;
}
```

What is happening here? The variable `a` has become a structure containing the number of values provided, as well as an array of the values. The number of passed values is generated at compile time. For run time argument passing, if you have an array, and you have the length of items, you can create a variable argument as follows:

```cpp
sum($some_count:some_array);
```

This creates and passes the structure automatically. You can also manually create the structure.