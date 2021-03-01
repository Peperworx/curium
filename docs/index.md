# Curium

Curium is a programming language specification designed after Python, C++, and Rust, and is purely conceptual until the specification is complete.

Curium is different from most programming languages. Curium in and of itself will only contain a few parts:

- Language Structure
- Integer, Array, and Pointer Types
- Calling Convention
- Operators




## Language Structure

In Curium, the structure of a program is flexible. Curium does not force the programmer to use object oriented programming, or any other method. It is closer to C++ in that respect.

### Functions

The one of the most basic constructs in curium is a function. The calling convention is simple. First push a number of arguments to the stack, then push the arguments one by one, in the order they are defined in the function header. Lets take a look at a Curium function:
```cpp
def main() -> i32{
    return 0;
}
```
This is the most basic of functions, and it does absolutely nothing. Here is what this function definition looks like in LLVM:
```LLVM
define i32 @main(){
    ret i32 0;
}
```

We can also call functions like so:
```cpp
def function2() -> i32 {
    return 0;
}

def main() -> i32 {
    return function2();
}
```

Unoptimized, this turns into this LLVM code:

```LLVM

define i32 @function2() {
    ret i32 0
}

define i32 @main() {
    %0 = call i32 @function2()
    ret i32 %0
}
```


### Variables

Variables are also some of the most simple constructs available.

In Curium, variables are defined like so:
```rust
let v: i32 = 1234;
```
This is where Curium is similar to Rust. Variables are immutable unless defined as mutable. This is simply a construct of Curium, and variables are implemented the same in LLVM.

Global variables and local variables are defined in the same way, just like C.

This translates to the following LLVM.

Global:
```LLVM
@v = global i32 1234
```
Local:
```LLVM
%v = alloca i32
store i32 1234, i32* %v
```

In Curium, mutable variables can be defined almost like rust:
```rust
let mut v:i32 = 1234;
```

Just like rust, variables can also be shadowed:

```rust
let v:i32 = 1234;
let v:i32 = 5678;
```

And this translates to LLVM like so:
```LLVM
%v.0 = alloca i32
store i32 1234, i32* v
%v.1 = alloca i32
store i32 5678, i32* v
```
The most recent revision of the variable will be used. Global variables may not be shadowed as they can also be defined as external.

### Constants

Constant values come in two variants: inline and global.

Constants are always private, and can not be made external.

Inline constants are simple, when assigning a value to a variable, you use an inline constant:
```rust
let v: i32 = 1234;
             ^^^^
```
The arrows point to the inline constant.

Global constants are slightly different. Here is an example:
```cpp
const v:i32 = 1234;
```

This maps to the following in LLVM:
```LLVM
@v = internal constant i32 1234
```

Constants can never be changed, and cannot be shadowed.

### Structures

Structures are simple, and almost exactly like C (excepting the variable declarations)
```c++
struct some_struct {
    let a: i32 = 1234;
    let b: i32 = 5678;
}

def main() -> i32 {
    let v: some_struct;
    return v.a;
}
```

This maps to the following LLVM:
```LLVM
%some_struct = type {i32, i32}

define i32 @main() {
    ; Create the structure
    %v = alloca some_struct
    
    ; Load members
    %v.a = getelementptr %some_struct, %some_struct* %v, i32 0, i32 0
    %v.b = getelementptr %some_struct, %some_struct* %v, i32 1, i32 0
    
    ; Store default values
    store i32 1234, i32* %v.a
    store i32 5678, i32* %v.b
    
    ; Return the value
    %0 = load load i32, i32* %v.a
    ret i32 %0
}
```