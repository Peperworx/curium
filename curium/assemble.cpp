#include "assemble.h"


/*
    Preprocesses a line of assembly code.
*/
string assembler::process(string in){
    // Remove all comments
    return "";
}


/*
    Assembles file given in argument 3
*/
int assembler::assemble(int argc, char** argv){
    if(argc < 3){
        cout << "Error: Missing file to assemble\n";
        return 0;
    }

    string file = argv[2];

    return 0;
}