def main() -> int {
    let a: int = 3 + 1;
    a += 1;
    a &= somefunc(a);
    
}
def somefunc(a: int) -> int {
    return a * 2;
}