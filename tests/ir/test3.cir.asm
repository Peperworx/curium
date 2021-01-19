section .data

section .bss

section .text
_start:
mov rax, %inst_of_a.b
add rax, %inst_of_a.d
push rax
pop %e
