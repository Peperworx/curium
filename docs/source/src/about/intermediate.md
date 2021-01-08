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

1. The name of the structure to add a member to
2. The name of the member
3. The type of the member
4. The default value of the member (Optional)


## Types

There are various types.

Pointer types can point any names. They look like `ptr:%name`

There are several integer types:

##### Unsigned
- U64, a 64 bit integer, unsigned
- U32, a 32 bit integer, unsigned
- U16, a 16 bit integer, unsigned
- U8, an 8 bit integer, unsigned

##### Signed
- S64, a 64 bit integer, signed
- S32, a 32 bit integer, signed
- S16, a 16 bit integer, signed
- S8, an 8 bit integer, signed

There can also be pointers to respective integer types

There are also several float types:

- Float, a 32 bit float
- Double, a 64 bit float
- long double, an 80 bit floar
  
### Void type
A void type is a raw pointer, with no type specified. It can be referenced by pointing to an integer address, or pointing to a label.
For example:

```cpp
// Define a label
label(%x);

// Reference a pointer to the label
ptr:%x

// Reference a pointer to an address
ptr:0xB8000

```

### Structures as types

Structures can be used as types. For example:
```cpp
// This uses struct a from the structures section

struct(%a);
member(%a, %b, u32);
member(%a, %c, ptr:%a);
member(%a, %d, u32, 0);



// Create instance of a
define(%inst_of_a, %a);

// Create e
define(%e, u32);

// Add b and d
add(%inst_of_a.b, %inst_of_a.d);

// Pop into e
pop(%e);

```

Structure instances are simply defined by using `define` with the name of the structure.

Structure members are accessed using `.`.



## Functions

Functions are very similar to assembly labels.

Here is an example function that adds two numbers and returns them:

```cpp
// Define the function
function(%add_two_numbers){

// add the two numbers at the top of the stack
add($0, $1);

// This already pushes the value to stack, so our job is over

// End the function definition
}

```
This function can be called like so:
```cpp
define(%out); // Define a variable for output
push(1); // Push the last argument
push(3); // Push the first argument

// Call the function
call(%add_two_numbers);

// Pop the result into argument
pop(%out);
```

This behaves similarly to assembly's labels and ret, except that function contents need to be explicitly called.

## Conditionals

Here is a basic if, elif, else conditional:

```cpp

// Compare the values 1 and 2.
cmp(1,2);

if(>){
    // Contents of if
} else if (<) {
    // Contents of else if
} else {
    // Contents of else
}

// Do something else

```

Now, even though the first if will always run, this is still an interesting example.

The first if is a jg, the second if is a glt, and the else is simply a jump.

This translates to this nasm code:

```nasm
_start:
    mov rax, 1
    cmp rax, 2
    jg if_seg_1234 ; This will be some random number
    jl elif_1_seg_1234 ; This will be the same number
    jmp else_seg_1234 ; So will this

if_seg_1234:
    ; Contents of if
    jmp finish_seg_1234

elif_f_seg_1234:
    ; Contents of else if
    jmp finish_seg_1234

else_seg_1234:
    ; Contents of else
    jmp finish_seg_1234

finish_seg_1234:
    jmp seg_1235

seg_1235:
    ; Do somemthing else


```

This is why C-like conditionals are so epic. So much less to do. Sooooo much less.

And and Or also exist for conditionals:

```cpp
cmp(1,2);

if(> | <){

}

if(== & !=){

}
```
Those are just some nonsensical examples, but they are good for demonstration.



## Classes

Classes are simply structures with a code segment.

The following example is how a class would be implemented.
```cpp
struct(%test_struct);
member(%test_struct, %a, u32);
member(%test_struct, %b, u32);

function(%test_struct.add_to_a_b){
    // Load the this reference.
    define(%this);
    pop(%this);

    // Add a and b to the argument.
    add($0,%this.a);
    add($0,%this.b);
    // Already on stack. no need to push
}

// The above function takes one argument, and
// Adds a and b to it.

// Lets create an instance of %test_struct

define(%test_inst,%test_struct);

// Create variable for output
define(%out, u32);

// Move 1 and 2 into test_inst.a and b
mov(%test_inst.a,1);
mov(%test_inst.b,2);

// Push the argument (3)
push(3);

// Call the function
call(%test_inst.add_t_a_b);

// Pop into output
pop(%out);


```

When you call a function that is a member of a structure, a pointer to the instance of the structure is pushed to the stack automatically. If you call off of the main type, instead of the instance, the pointer is not pushed automatically.


# Behind the scenes

This intermediate language mostly reads line by line.

Only in two circumstances does it actually "branch" off, and that is functions and conditionals. Functions are not real branches, and they can not be nested. Conditionals, however, are a 100% different story.


