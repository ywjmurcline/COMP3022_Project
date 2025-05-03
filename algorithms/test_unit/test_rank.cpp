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
#include <functional>

using namespace std;


size_t m = 64;
size_t log2m_ = log2(m);

string item = "hash";

uint64_t seed_ = 1337;




size_t hash_(const std::string& s) {
    std::hash<std::string> hasher;
    return hasher(std::to_string(seed_) + s);
}

// least significant 1, that is number of trailing zeros
uint32_t TrailingZeroes(size_t x) {
    return x ? __builtin_ctzll(x): 64;
}

static uint32_t TrailingOnes(uint64_t bitmap) {
    for (uint32_t i = 0; i < 64; ++i) {

        cout << (bitmap & (1ULL << i)) << endl;

        if ((bitmap & (1ULL << i)) == 0)
            return i;
    }
    return 64;
}



int main() {

    uint64_t bitmap(0);
    cout << "bitmap: " << std::bitset<64>(bitmap) << endl;

    size_t h = hash_(item);
    cout << "hash: " << std::bitset<64>(h) << " " << h << endl;
    size_t idx = h >> (64 - log2m_); // use top bits to choose bitmap
    cout << "idx: " << idx << endl;

    cout << 64 - log2m_ << endl;
    size_t msk = ((1ULL << (64 - log2m_)) - 1);
    cout << "msk: " << std::bitset<64>(msk) << endl;

    size_t remaining = h & ((1ULL << (64 - log2m_)) - 1);
    // std::string binStr = std::bitset<64>(remaining).to_string();
    cout << "remaining: " << std::bitset<64>(remaining) << endl;
    
    uint32_t r = TrailingZeroes(remaining);
    if (r < 64) {
        bitmap |= (1ULL << r);
    }

    cout << "bitmap: " << std::bitset<64>(bitmap) << endl;

    uint32_t t = TrailingOnes(bitmap);

    cout << "firstOneBit: " <<  t << endl;

    return 1;
}

