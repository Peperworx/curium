#pragma once

#include <iostream>
#include <fstream>

using namespace std;


class Assembler {
public:
    string process(string in);
    int assemble(int argc, char** argv);

};  