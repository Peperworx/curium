section .data

section .bss
temp_30933_0 resq 1
temp_30933_1 resq 1
section .text
_start:
jmp %end_%add_two_numbers
add_two_numbers_16258310:
pop temp_30933_1
pop temp_30933_2
mov rax, [temp_30933_1]
add rax, [temp_30933_2]
push rax
ret 
end_add_two_numbers_1512716905:
push 1
push 3
call %add_two_numbers
pop %out
