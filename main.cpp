#include <iostream>
#include <string>
#include "curium/opcodes.h"
#include "curium/assemble.h"

using namespace std;

/*
    Shows help for the program
*/
void help() {
    // Print version
    cout << "Curium v" << VERSION_MAJOR;
    cout << "." << VERSION_MINOR;
    cout << "." << VERSION_PATCH << " - help" << "\n";
    cout << "\n";

    // Print command format
    cout << "Command Format:\n";
    cout << "\tcurium [command] [file]\n";
    cout << "\n";

    // Print commands
    cout << "Commands:\n";
    cout << "\tassemble - assembles provided file\n";
}




int main(int argc, char** argv) {
    // Make sure we have the arguments
    if(argc < 2){
        help();
        return 0;
    }

    try {
        // Check argument
        if (string(argv[1]) == "assemble"){
            Assembler *a = new(Assembler);
            return a->assemble(argc,argv);
        } else {
            help();
        }
    } catch (int e) {
        return e;
    }

}

