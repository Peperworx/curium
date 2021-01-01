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