section .data

section .bss
temp_42318_0 resq 1
temp_42318_1 resq 1
section .text
_start:
push 1
pop temp_42318_1
mov rax, [temp_42318_1]
mul rax, 2
push rax
pop temp_42318_1
mov rax, [temp_42318_1]
add rax, 1
push rax
push 3
pop temp_42318_1
mov rax, [temp_42318_1]
mul rax, 2
push rax
pop temp_42318_1
mov rax, [temp_42318_1]
add rax, 1
push rax
pop temp_42318_1
pop temp_42318_2
mov rax, [temp_42318_1]
add rax, [temp_42318_2]
push rax
pop %c
