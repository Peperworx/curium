# Curium

Curium is a programming language specification designed after Python, C++, and Rust, and is purely conceptual until the specification is complete.

Curium is different from most programming languages. Curium in and of itself will only contain a few parts:

- Language Structure
- Integer, Array, and Pointer Types
- Calling Convention
- Operators




## Language Structure

In Curium, the structure of a program is flexible. Curium does not force the programmer to use object oriented programming, or any other method. It is closer to C++ in that respect.

The one of the most basic constructs in curium is a function. The calling convention is simple. First push a number of arguments to the stack, then push the arguments one by one, in the order they are defined in the function header. Lets take a look at a Curium function:
```cpp
def main() -> i32{
    return 0;
}
```
This is the most basic of functions, and it does absolutely nothing. Here is what this function definition looks like in LLVM:
```LLVM
define i32 main(){
    ret i32 0;
}
```