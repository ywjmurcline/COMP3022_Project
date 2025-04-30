#include <iostream>
#include <fstream>
#include <vector>

using namespace std;

int main() {
    string txt_path = "/Users/lily/Documents/2024-2025_Spring/algorithm_lab/cadinality_estimation/COMP3022_Project/dataset/demo/output.txt";
    std::ifstream file(txt_path);
    std::vector<std::string> strings;
    std::string line;

    while (std::getline(file, line)) {
        strings.push_back(line);
    }

    // Print all strings
    for (const auto& str : strings) {
        std::cout << str << std::endl;
    }
}