(window.webpackJsonp=window.webpackJsonp||[]).push([[10],{386:function(e,t,a){"use strict";a.r(t);var i=a(42),r=Object(i.a)({},(function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("ContentSlotsDistributor",{attrs:{"slot-key":e.$parent.slotKey}},[a("h1",{attrs:{id:"introduction"}},[a("a",{staticClass:"header-anchor",attrs:{href:"#introduction"}},[e._v("#")]),e._v(" Introduction")]),e._v(" "),a("p",[e._v('Curium Lang is a conceptual programming language that will be implemented in Python once a "specification" is complete. This "specification" is in fact this documentation. The language will be designed to complete the documentation, one tutorial step at a time.')]),e._v(" "),a("p",[e._v("Curium is a C-like language with static typing that can be compiled to multiple targets. The primary target will be a custom assembly language that will assemble into a custom bytecode. This bytecode could then be interpreted or, as I plan to implement in the far future, converted to an ELF executable.")]),e._v(" "),a("p",[e._v("Versioning will be using "),a("a",{attrs:{href:"https://semver.org/",target:"_blank",rel:"noopener noreferrer"}},[e._v("Semantic Versioning"),a("OutboundLink")],1),e._v(" with a twist. Every tutorial step will be a minor version, and every tutorial section will be a major version.")]),e._v(" "),a("h2",{attrs:{id:"why-python"}},[a("a",{staticClass:"header-anchor",attrs:{href:"#why-python"}},[e._v("#")]),e._v(" Why Python??")]),e._v(" "),a("p",[e._v("Python is great for prototyping software fast. Using Python features like decorators, kerword arguments, dictionaries, the large standard library, and various tools that are available, we can create an easy to use interface that allows users to expand upon Curium (For Example: Providing custom standard library modules and builtin functions.)")]),e._v(" "),a("h3",{attrs:{id:"isn-t-python-slow"}},[a("a",{staticClass:"header-anchor",attrs:{href:"#isn-t-python-slow"}},[e._v("#")]),e._v(" Isn't Python Slow?")]),e._v(" "),a("p",[e._v("Not really. Using many language features of python (list comprehensions, C libraries, threading, etc) we can optimize code alot. However, python will be used only for the compiler and assembler. The interpreter will be written in C++ and compiled as a dynamic library. This will then be loaded and called from python using ctypes.")]),e._v(" "),a("h2",{attrs:{id:"language-details"}},[a("a",{staticClass:"header-anchor",attrs:{href:"#language-details"}},[e._v("#")]),e._v(" Language Details")]),e._v(" "),a("h3",{attrs:{id:"how-will-this-language-be-typed"}},[a("a",{staticClass:"header-anchor",attrs:{href:"#how-will-this-language-be-typed"}},[e._v("#")]),e._v(" How will this language be typed?")]),e._v(" "),a("p",[e._v("Curium will be statically typed. Every variable will have a type, but unlike other statically typed languages, variables types can be reassigned. This is possible because every type is at it's core just an array of bytes. Different parts of the array mean different things. Due to the nature of computers, however, this will only be available for the interpreted version. For the compiled version, this will be less efficient, simply creating a new variable and casting the original value to that new variable, as opposed to realocating the original variable.")]),e._v(" "),a("h3",{attrs:{id:"everything-is-an-object-type"}},[a("a",{staticClass:"header-anchor",attrs:{href:"#everything-is-an-object-type"}},[e._v("#")]),e._v(" Everything is an object/type")]),e._v(" "),a("p",[e._v("Function? Object. Number? Object. String? Object. Class? Object. Struct? Object. This means that we can pass functions, structs, numbers, etc around effortlessly. On the top, it will seem a lot like python. Define a function, and it is the same as a callable class.")]),e._v(" "),a("h2",{attrs:{id:"step-1-compiler-details"}},[a("a",{staticClass:"header-anchor",attrs:{href:"#step-1-compiler-details"}},[e._v("#")]),e._v(" Step 1 Compiler Details")]),e._v(" "),a("p",[e._v("The step 1 compiler is an integral part of this language concept. It converts a parse tree to a custom assembly code which is then assembled into a custom bytecode. This bytecode can then be intepreted or compiled.")]),e._v(" "),a("h2",{attrs:{id:"assembler-details"}},[a("a",{staticClass:"header-anchor",attrs:{href:"#assembler-details"}},[e._v("#")]),e._v(" Assembler Details")]),e._v(" "),a("p",[e._v("The assembler will convert the custom assembly code into bytecode. More details on this once I get this 100% working. (I actually have a working demo right now, but it sucks.)")]),e._v(" "),a("h2",{attrs:{id:"interpreter-details"}},[a("a",{staticClass:"header-anchor",attrs:{href:"#interpreter-details"}},[e._v("#")]),e._v(" Interpreter Details")]),e._v(" "),a("h3",{attrs:{id:"memory-management"}},[a("a",{staticClass:"header-anchor",attrs:{href:"#memory-management"}},[e._v("#")]),e._v(" Memory Management")]),e._v(" "),a("p",[e._v('The interpreter will manage memory with a 100% custom memory allocator. The interpreter will store the program\'s memory in a custom list/vector of chars. This allows us to be super efficient with our memory use, and reduce overhead from possible "extra features" that build in memory managers provide. All we need is malloc and free. We will go into more details once an interpreter is in progress.')]),e._v(" "),a("h2",{attrs:{id:"step-2-compiler-details"}},[a("a",{staticClass:"header-anchor",attrs:{href:"#step-2-compiler-details"}},[e._v("#")]),e._v(" Step 2 Compiler Details")]),e._v(" "),a("p",[e._v("The step 2 compiler will be super similar to the interpreter. It will interpret the bytecode, but instead of performing actions based on what it sees, it will generate NASM assembly from the program.")]),e._v(" "),a("h2",{attrs:{id:"the-tutorial"}},[a("a",{staticClass:"header-anchor",attrs:{href:"#the-tutorial"}},[e._v("#")]),e._v(" The Tutorial")]),e._v(" "),a("p",[e._v("As I said, Curium will use Documentation Driven Devlopment, as (in my opinion) the best way to plan is to have a thorough understanding of how it the end result will work. This will be accomplished by means of a tutorial. As I said above, each step of a tutorial will be a minor version, and each section a major version. Patch versions are for security and bug fixes only.\nYou can start the tutorial by going "),a("RouterLink",{attrs:{to:"/tutorial/"}},[e._v("here")]),e._v(".")],1)])}),[],!1,null,null,null);t.default=r.exports}}]);