#include "assemble.h"


/*
    Preprocesses a line of assembly code.
*/
string Assembler::process(string in){
    // Remove all comments
    in = in.substr(0, in.find(";"));

    // Remove whitespace at the beginning of the line
    while(in.find(" ") == 0 || in.find("\t") == 0) {
        in = in.substr(1,in.size());
    }

    // Remove whitespace at the end of the line
    while(in.find(" ") == in.size() || in.find("\t") == in.size()) {
        in = in.substr(1,in.size());
    }

    // Check if there is a colon at the end
    size_t cln = in.find(":");
    if (cln != string::npos) {
        // If it is not at the end, error
        if (cln != in.size()) {
            
        }
    }

    return in;
}


/*
    Assembles file given in argument 3
*/
int Assembler::assemble(int argc, char** argv){
    if(argc < 3){
        cout << "Error: Missing file to assemble\n";
        return 1;
    }

    string file = argv[2];

    // Open the file
    ifstream infile;
    infile.open(file, ios::in);
    
    // If it was not found, error
    if (!infile.is_open()){
        cout << "Error: File " << file << " not found.\n";
        return 1;
    }

    // Iterate over each line
    for (string line; getline(infile,line);){
        // Preprocess the line
        line = this->process(line);
        cout << line << "\n";

        // Parse the line

    }

    // Close the file
    infile.close();

    return 0;
}