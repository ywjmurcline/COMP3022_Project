#include <iostream>
#include <vector>
#include <cmath>
#include <random>
#include <bitset>
#include <functional>
#include <string>
#include <limits>
#include <cassert>
#include <fstream>
#include <vector>
#include <chrono>
#include <mach/mach.h>
#include <iomanip>
#include "hash/LinearHash.hpp"
#include "hash/MurmurHash2.hpp"
#include "hash/FNV.hpp"
#include <functional>

std::string size_t_to_binary(size_t n) {
    std::string binary_string;
    if (n == 0) {
        binary_string = "0";
    } else {
        while (n > 0) {
            binary_string += (n % 2 == 0 ? '0' : '1');
            n /= 2;
        }
        std::reverse(binary_string.begin(), binary_string.end());
    }
    return binary_string;
}