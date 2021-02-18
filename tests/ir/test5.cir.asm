section .data

section .bss

section .text
_start:
cmp 1,2
ja if_1332
jb %elif_0_1332
je %elif_1_1332
jmp %else_1332
jmp %sect_end_1332
if_1332_3699478835:
mov rax, 1
add rax, 2
push rax
jmp %sect_end_1332
elif_0_1332_2584194070:
mov rax, 2
add rax, 3
push rax
jmp %sect_end_1332
elif_1_1332_2787035544:
mov rax, 3
add rax, 4
push rax
jmp %sect_end_1332
else_1332_1289558268:
mov rax, 4
add rax, 5
push rax
jmp %sect_end_1332
sect_end_1332_716623312:
mov rax, 5
add rax, 6
push rax
