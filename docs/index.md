# Curium

Curium is a programming language specification designed after Python, C++, and Rust, and is purely conceptual until the specification is complete.

Curium is different from most programming languages. Curium in and of itself will only contain a few parts:

- Language Structure
- Integer, Array, and Pointer Types
- Calling Convention
- Operators

Check out some of the core specification before moving on: [core](core)


## Language Structure

In Curium, the structure of a program is flexible. Curium does not force the programmer to use object oriented programming, or any other method. It is closer to C++ in that respect. Note that this page is something of a cheat sheet. This only contains some code snippets that explain the syntax a small amount, but do not explain why or how things work. Each element expressed here will have further documentation in the future. Variables take largely after Rust. Functions and classes take largely after Python (this will be explained in the individual documentation)

### Functions
Defining:
```cpp
def function_name() -> return_type{
    
}
```
Calling:
```cpp
function_name(args...);
```


### Variables

Defining non-mutable:
```rust
let v: i32 = 1234;
```
Defining mutable:
```rust
let mut v:i32 = 1234;
```

Shadowing:

```rust
let v:i32 = 1234;
let v:i32 = 5678;
```
Global variables can not be shadowed.

### Constants

Inline constants:
```rust
let v: i32 = 1234;
             ^^^^
```
The arrows point to the inline constant.

Global constants (outside of any scope):
```cpp
const v:i32 = 1234;
```

Constants can never be changed, and cannot be shadowed.

### Structures

Defining:
```c++
struct some_struct {
    let a: i32 = 1234;
    let b: i32 = 5678;
}
```

Using:
```c++
let v: some_struct;
let a: i32 = v.a;
```

### Pointers

Defining:
```cpp
let mut v:i16* = (i16*)0xb8000;
```

Accessing offset:
```cpp
v[0] = ('X'<<8)|0x0f;
```

Getting value:
```cpp
let v: i16 = *v;
```

Getting address:
```cpp
let v: i16 = &v;
```

Setting value:
```cpp
*v = ('Y'<<8)|0x0f;
```

Setting address:
```cpp
v = (i16*)0xb8000
```

**NOTE** The above code will not work on anything other than bare metal x86.

### Casts

Casting:
```cpp
let mut v:i32* = (i32*)0xb8000;
```

### Classes

Creating:
```cpp
class class_name {
    let private a:i32 = 20;
    def get_a(self:class_name*) -> i32 {
        return self->name;
    }
}
```
Using:
```cpp
let mut v:class_name;
let a:i32 = v.get_a();
```