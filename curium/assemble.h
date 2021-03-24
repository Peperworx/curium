#pragma once

#include <iostream>
#include <fstream>
#include <vector>
#include <map>

using namespace std;


class Assembler {
private:
    size_t position = 0;
public:
    map<string,size_t> labels;
    string process(string in);
    int assemble(int argc, char** argv);

};  