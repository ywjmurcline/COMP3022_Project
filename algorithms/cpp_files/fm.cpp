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

using namespace std;


class FlajoletMartin {
public:
    explicit FlajoletMartin(size_t m, string hash_type, int seed)
        : m_(m), seeds_(m), bitmaps_(m, 0) {
        assert(m > 0);
        initSeeds(seed);
        initHash(hash_type);
    }

    void add(const std::string& item) {
        addBatch({item});
    }

    void addBatch(const std::vector<std::string>& items) {
        for (const auto& it : items) {
            for (size_t i = 0; i < m_; ++i) {
                size_t h = hashWithSeed(it, seeds_[i]);
                uint32_t r = TrailingZeroes(h); // 1000, return 3
                
                if (r < 64) {  // Cap to bitmap size
                    bitmaps_[i] |= (1ULL << r);
                }
            }
        }
    }

    double estimate() const {
        double R_sum = 0;
        for (uint64_t bitmap : bitmaps_) {
            uint32_t R = TrailingOnes(bitmap);
            R_sum += R;
        }
        double R_avg = R_sum / static_cast<double>(m_);
        return std::pow(2.0, R_avg) / PHI;
    }

private:
    static constexpr double PHI = 0.77351;
    size_t m_;
    std::vector<uint64_t> seeds_;
    std::vector<uint64_t> bitmaps_;
    std::function<size_t(const std::string&, uint64_t)> hashWithSeed;

    void initSeeds(int seed) {
        std::mt19937_64 rng(seed);
        std::uniform_int_distribution<uint64_t> dist;
        for (auto& s : seeds_) {
            s = dist(rng);
        }
    }


    // Initialize based on choice parameter (0–3)
    void initHash(string hash_type) {
        if (hash_type == "murmurhash2") {
            hashWithSeed = &FlajoletMartin::murmurhash2;
            cout << "Using self-implemented MurmurHash2" << endl;
        } else if (hash_type == "fnv1a") {
            hashWithSeed = &FlajoletMartin::fnv1a;
            cout << "Using self-implemented fnv1a" << endl;
        } else if (hash_type == "linearhash") {
            hashWithSeed = &FlajoletMartin::linearhash;
            cout << "Using self-implemented linearhash" << endl;
        } else {
            hashWithSeed = &FlajoletMartin::murmurhash_cpp;
            cout << "Using C++ MurmurHash2" << endl;
        }
    }

    static size_t murmurhash2(const std::string& s, uint64_t seed) {
        MurmurHash2_64 hasher;
        return hasher(std::to_string(seed) + s);
    }
    static size_t fnv1a(const std::string& s, uint64_t seed) {
        FNV1aHash64 hasher;
        return hasher(std::to_string(seed) + s);
    }
    static size_t linearhash(const std::string& s, uint64_t seed) {
        LinearHash hasher;
        return hasher(std::to_string(seed) + s);
    }
    static size_t murmurhash_cpp(const std::string& s, uint64_t seed) {
        std::hash<std::string> hasher;
        return hasher(std::to_string(seed) + s);
    }


    // least significant 1, that is number of trailing zeros
    uint32_t TrailingZeroes(size_t x) {
        return x ? __builtin_ctzll(x): 64;
    }

    // least significant 0, that is number of trailing ones
    static uint32_t TrailingOnes(uint64_t bitmap) {
        for (uint32_t i = 0; i < 64; ++i) {    
            if ((bitmap & (1ULL << i)) == 0)
                return i;
        }
        return 64;
    }

};


size_t getMemoryUsage() {
    task_basic_info info;
    mach_msg_type_number_t size = TASK_BASIC_INFO_COUNT;
    kern_return_t result = task_info(mach_task_self(), TASK_BASIC_INFO,
                                     (task_info_t)&info, &size);
    if (result != KERN_SUCCESS) return 0;
    return info.resident_size; // in bytes
}

size_t calculateMemoryUsage(const std::vector<std::string>& vec) {
    size_t total = sizeof(vec); // Memory for the vector structure
    
    // Memory for each string object in the vector
    total += sizeof(std::string) * vec.capacity();
    
    // Memory for each string's content
    for (const auto& str : vec) {
        total += str.capacity(); // Memory for the string's characters
    }
    
    return total;
}

int main(int argc, char* argv[]) {

    if (argc != 5) {
        std::cerr << "Usage: " << argv[0] << " <num_registers> <hash_type> <seed> <data_path>\n";
        return 1;
    }

    size_t m = std::stoull(argv[1]);
    std::string hash_type = argv[2];
    int seed = std::stoi(argv[3]);
    std::string txt_path = argv[4];


    FlajoletMartin fm(m, hash_type, seed);

    // string txt_path = "/Users/lily/Documents/2024-2025_Spring/algorithm_lab/cadinality_estimation/COMP3022_Project/dataset/cleaned/NCVoters/ncvoter_all.txt";
    std::ifstream file(txt_path);
    std::vector<std::string> strings;
    std::string line;

    while (std::getline(file, line)) {
        strings.push_back(line);
    }

    auto start = std::chrono::high_resolution_clock::now();
    fm.addBatch(strings);
    auto end = std::chrono::high_resolution_clock::now();

    std::chrono::duration<double> duration = end - start;
    std::cout << "FM addBatch time: " << std::fixed << std::setprecision(6)
              << duration.count() << " seconds\n";

    std::cout << "Estimated cardinality: " << fm.estimate() << "\n";


    size_t mem = getMemoryUsage();
    size_t vec_mem = calculateMemoryUsage(strings);
    std::cout << "Memory usage: " << (mem - vec_mem) / (1024.0 * 1024.0) << " MB\n";
    return 0;
}
