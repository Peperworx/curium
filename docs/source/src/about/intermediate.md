# Curium intermediate language

This intermediate language is simply a way to linearize complex, branching programs.

A Very basic example follows:
```cpp
uint32_t c = 1 + 2;

// Turns into

// Define C
define(%c, u32);

// Execute add function
add(1,2);

// Result is on top of stack
pop(%c);
```

Something more complex:

```cpp
uint32_t c = (1*2+-1)+(3*2+-1);

// Turns into


// Define c
define(%c, u32);

// (1*2+-1):
push(1);
mul($0, 2);
add($0, -1);

// (3*2+-1):
push(3)
mul($0 ,2);
add($0, -1);

// The center addition
// This pops both and pushes the result.
add($1, $0);

// Pop value into c
pop(%c)

```
Lets take a real quick look at that.

### User defined names
Every user defined name starts with a `%`.
This makes it so that conflicts between user defined and builtin names do not occur. `define` is used to define names. It takes a name reference and a type. (In this case u32)

### Stack access

A Dollar Sign, followed by a number dictates and item on the stack. This number is similar to an array index, as it starts at zero. For example: `$0` is the first item, `$1` is the second item, and so on. These pop the item from the stack.

The push command takes a single argument, and pushes it to the stack.

The pop command pops and item from the stack, and inserts it at the given address or variable.

### Arithmetic 

Arithmetic can be performed using various operators such as add, mul, sub, div, bls (bitwise left shift), etc. A Complete list is to come once the IR is finished. Arithmetic operators always push the result to the stack.




## Structures
Any good language supports data structures. This IR language provides support for just that:

```cpp

struct a {
    uint32_t b;
    a* c;
    uint16_t d = 0;
};

// Converts to this:

struct(%a);
member(%a, %b, u32);
member(%a, %c, ptr:%a);
member(%a, %d, u32, 0);


```

Here `struct` defines a data structure. It has one input, the name.
`member` adds a new member to the structure.
The arguments are as follows:


