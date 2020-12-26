---
sidebar: auto
---

# Tutorial
## Hello, World!

::: tip INFO
This will be fully implemented in 0.1.x
Required for full implementation:
- datatypes
- functions
- returns
- templating
- variables

Lexing Complete
:::

The tutorial is divided into several steps. This is the first step.


Every good language documentation starts off with a hello world sample:

```cpp
function[int]: main(){
    print("Hello,World!\n");

    return 0;
}
```

For Curium, you can just use C++ language highlighting.

Lets examine the code snippet above:

First thing to notice is the function declaration. Functions are declared like this:
```cpp
function[return_type]: function_name(type arg1, type arg2,...){
    // Code body
    return return_value;
}
```

The function type is a builtin specifier that tells the program that a function is defined there.
Inside of the brackets, next to function, we can specify the return type. After that, the function declaration looks the same as any other C-like language. the function name, the arguments, and the return. If the function never returns, then the compiler automatically returns the default constructor of the return value.

Functions are called the same as in most other C-like languages:
```cpp
function_name(arg1,arg2,arg3,...);
```

Second major thing to notice is the print function. C has the printf, C++ has cout, and Curium has print. This print function behaves like the python print function, except it does not automatically append a newline.

This concludes the first step of the tutorial. Curium should be able to execute this code at version 0.1.x

## Variables

::: tip INFO
This is the second step of our tutorial. Version 0.2.x of Curium will be able to execute this flawlessly, and 0.1.x may be able to execute this, depending on development progress.

Required for full implementation:
- data types
- mathematical parsing
- variables
- templating


Lexing Complete
:::



Every true programming language has variables. Variables can store dynamic values such as numbers.
Lets try defining some variables:

```cpp
function[int]: main(){
    // Here we define the variable a as 7
    int: a = 7;

    // And here we define the variable b as 6
    int: b = 6;

    // And here we do some basic math,
    // Assigning the value a * b to the variable c
    int: c = a + b;

    return 0;
}
```

Easy. A variable definition looks like this:

```cpp
type_name: variable_name = value;
```

We also implement a system similar to C++ templates.
These work by appending brackets with arguments between them:

```cpp
list[int]: list_of_ints = [0,1,2,3];
```

Even though these function similar to C++ templates, they are not realy templates.
They are calculated at both compile time and at runtime. Compile time for making sure that typing rules are being filed, ant at runtime for actually performing operations with the target.

If python were statically typed, this would be similar to this python code:

```python
class TemplateTaker:
    def __init__(self,arg_type, arg):
        self.arg: arg_type = arg

```

## Structures

::: tip INFO
This section will be implemented in 0.3.x
Required for full implementation:
- structs
- pointers



Lexing Complete
:::

Most languages have an implementation of data structures. In this section, we will be overviewing a form of static data structures simply called structs.

These function like in the C language, except the final semicolon is optional.
Here is an example of a struct for a linked list:

```cpp
struct listItem {
    int: contents;
    listItem*: next;
}
```

Here you can also see what is called a pointer type. These function like in C and we will overview them later.