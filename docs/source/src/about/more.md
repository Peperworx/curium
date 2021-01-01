---
tags: []
created: 2021-01-01T04:06:48.982Z
modified: 2021-01-01T04:07:13.115Z
---
# Details on Curium.

Curium borrows all of the best parts from several languages.

Curium is not designed to be fast. Curium at this point is simply a plan and a prototype.
Once the curium specification is complete, and a basic implementation is finished, a total refractor of the backend will take place.

I have noticed that there are a ton of languages that depend on whitespace.

For example, C requires whitespace between a type and the variable name:

```c
char* char_pointer;
```
I also noticed that, oddly, python, even though it is based off of using whitespace, does not require whitespace for variable type hints:

```python
byte_array:bytearray = bytearray(b"Hello,World!")
```

I liked how C/C++ put the type name before the variable, and I like how python type hints work, and this led me to this syntax:

```cpp
char*: char_pointer;
```

This simply replaces the C/C++ space with a colon.
It also allows "templates" (although in curium, templates are computed at runtime, and are not actually templates in the full sense of the word):

```cpp
vector[char]: vector_of_chars;
```

Functions also happen to be types. This takes after Python and Javascript (even though I dislike the second)

```cpp
function[int]: main = (char arg1, int arg2, string arg3)
{
    return 0x1BADB002;
}
```

If you do not provide the "function" type and you do not provide any function arguments it is assumed that you are writing a function. This is the same as previous:

```cpp
int: main = (char arg1, int arg2, string arg3)
{
    return 0x1BADB002;
}
```

We can also create computed values:

```cpp
computed[int]: main = (){
    return 0x1BADB002;
}
```

Getting the value from a computed value is the same as calling the function.

```cpp
print(main) // Prints the value of 0x1BADB002
```

This is all performed on the compiler step.

Lets now take a loop at the parsing step.

## Parsing

When parsing a file, newlines are ignored between brackets.

This includes function definitions, lists, argument lists, etc.

Every program consists of a list of statements.

The most basic statement is a expression with a semicolon terminating it:

```cpp
    0+0;
```

Function calls are also considered expressions:

```cpp
    function[int]: main = (){
        return 0;
    }
```

This allows functions to be assigned to variables, and even passed to other functions.

```cpp
funca((){
    print("This function is passed to funca!");
}, arg2, arg3, 4, 5, 6, 7);
```

Function definitions consist of two parts, a tuple of arguments with their type, and a namespace. A tuple looks like this: 
```cpp
(val1, val2, valx, ...)
```

A tuple of arguments looks like this:
```cpp
(type: arg1, type: arg2, ...)
```

Namespaces look like this:

```cpp
{
    statement1;
    statement2;
    expr();
}
```

A namespace is basically a list of statements delimited by semicolons. A namespace in itself is a type, and can be assigned like this:

```cpp
namespace: namespace_test = {
    int a;
    int b;
    float c;
    char d;
}
```

The scope of a namespace can be accessed using the "::" operator:

```cpp
print(namespace_test::a);
```

Sometimes, you want to have instanced namespaces. An example of an instanced namespace is a struct:

```cpp
struct: struct_test = {
    int a;
    int b;
    float c;
    char d;
}
```

An instanced namespace can have new "versions" of itself created. This can be done by using a instanced namespace as a type:

```cpp
struct_test: a;
a.a = 0;
a.b = 1;
a.c = 3.14;
a.d = 'D';
```

This creates a new version of the namespace in memory, and allows updating of the values for the namespace in that specific location.

Another example of an instanced namespace is a class:

```cpp
class: class_a = {
private:
    int: a;
public:
    function[int]: get_a;
}

class_a::get_a = (){
    print(a)
    return a;
}
```

Here we notice access modifiers. Every member declared after that, until the next access modifier has that access level. In the previous example we notice that get_a is accessible to the public, but the value of a is private.

We also notice that we can define the value of get_a outside of the class scope. When a program is executing, everything in the global scope is executed, and then the main function is executed. Only variable and function definitions may go in the global scope. Functions may not be called in the global scope.

We use the concept of namespaces, instead of separating class, struct and namespace because it is easier to implement. Classes, structs, and namespaces all have member access. In a function, everything defaults to private access unless otherwise specified. 

## Data types

The lowest datatype is *`object`*. Every other object is based off the *`object`* type.

There are several functions that objects can implement. These are similar to pythons dunder methods or C++'s operator overloads:


These each override the operator specified in their name. Example of overriding ==:

```cpp
function[bool]: operator(==) = (typename B){
    return B == this;
} 
```

Notice the function name is operator followed by the operator in parentheses.

You may be wondering how default types like integers are implemented.

They simply use inline assembly. For example (on uint64):

```cpp
function[void]: operator(=) = (uint64 B){
    __asm__("mov rax, [%1]; mov [%0], qword [rax]", *this.value, *B.value);
}
```