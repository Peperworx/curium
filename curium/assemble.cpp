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
        if (cln != in.size()-1) {
            cout << "Syntax Error: Unexpected character" << (in.size() - 1 - cln > 1 ? "s " : " ") << "in label\n";
            cln += 1;
            string out = "";
            for(int i = 0; i < cln; i++) {
                out.append(" ");
            }
            for(int i = 0; i < in.size()-cln; i++) {
                out.append("^");
            }
            cout << in << "\n";
            cout << out << "\n";
            throw 2;
        } else {
            // Else, add a label at position
            this->labels[in.substr(0,cln)] = this->position;
            return "";
        }
    }

    // Check if there is a # at the beginning
    size_t hsh = in.find("#");
    if(hsh != string::npos && hsh == 0){
        // If there is, then remove it and interpret the preprocessor directive
        in = in.substr(1,in.size());

        // Now parse the directive
        vector<string> args;
        string ic = in; // Copy in
        size_t c;
        while((c = ic.find(" ")) != string::npos) {
            args.push_back(ic.substr(0,c));
            ic = ic.substr(c,ic.size());
        }
        for(int i = 0; i < args.size(); i++) {
            cout << args[i] << ",";
        }
        cout << "\n";

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

    // Lets show all labels
    for(auto it = this->labels.cbegin(); it != this->labels.cend(); it++){
        cout << it->first << " : " << it->second << "\n";
    }

    // Close the file
    infile.close();

    return 0;
}