import parser

test = """

; This defines a label called a
label:a = 0

; We can assign b a value
b = 2

; and then perform an operation on that value
c = b * 2

; Conditional jump
_ = #=b

; #=  : Jump equal
; #!  : Jump not equal
; #<  : Jump less than
; #>  : Jump greater than
; #<= : Jump less than equal to
; #>= : Jump greater than equal to

; Registers can be directly read using %

d = %rax

; Functions can be called using $
_ = $somefunc

; The hashtag (#) is a unary operator for jump
; underscore (_) is a null variable. All input to this variable
; is discarded. Jumps return nothing, so using "_" is appropriate
_ = #a


# Infinite loops can be created like this:
e = #e


"""

def parseString(input):
    print(input)


parseString(test)