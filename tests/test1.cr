def main (i: int) -> int {
    let a: int = i + 1;
    a += 1;
    a &= somefunc();
    
}
def somefunc (a: int) -> int {
    return a;
}