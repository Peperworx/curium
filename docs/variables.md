# Variables


This is where Curium becomes similar to languages like Rust. In Curium, variables are by default immutable. Here is an example:

```rust
let v: i32 = 0;
```

An immutable variable can only have it's value set once. Here is what the above code sample looks like in LLVM:

```LLVM
%v.0 = i32 0
```

As you can see, the name follows standard name mangling rules and can only be assigned once.

## Shadowing

Immutable variables, like in Rust, can also be shadowed. An example:

```rust
let v: i32 = 1234;
let v: i16 = 5670;
```

This is the equivilence of creating a new variable with a different name. Translated to LLVM:

```LLVM
%v.0 = i32 1234
%v.1 = i16 5678
```

## Mutable variables

Sometimes it is useful to be able to change variables. This can be done using mutable variables and it works like Rust:

```rust
let mut v: i32 = 1234;
v = 5678;
```

Mutable variables that are declared in a function are allocated on the stack, and global mutable variables are defined as global values in LLVM.

Here is the previous example, translated to LLVM like it is in a function:

```LLVM
%v = alloca i32
load i32 1234, i32* %v
load i32 5678, i32* %v
```