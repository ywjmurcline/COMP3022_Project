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

class PCSA {
public:
    explicit PCSA(size_t m, std::string hash_type1, std::string hash_type2, int seed)
        : m_(m), log2m_(std::log2(m_)), bitmaps_(m, 0), bucket_count_(m, 0){
        assert(m > 0); // m must be power of 2
        initSeeds(seed);
        initHash(hash_type1, hash_type2);
    }

    void add(const std::string& item) {
        addBatch({item});
    }

    void addBatch(const std::vector<std::string>& items) {
        for (const auto& item : items) {
            // use first hash function to get the index
            size_t h1 = hash1(item, seed_);
            size_t idx = h1 >> (64 - log2m_); // use top bits to choose bitmap

            // use second hash function to get the remaining bits
            size_t h2 = hash2(item, seed_);
            size_t remaining = h2 & ((1ULL << (64 - log2m_)) - 1);

            uint32_t r = TrailingZeroes(remaining);
            if (r < 64) {
                bitmaps_[idx] |= (1ULL << r);
                bucket_count_[idx] += 1; // Increment the count for this bucket
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
        return (m_ / PHI) * std::pow(2.0, R_avg);
    }

    std::vector<int> get_bucket_count() {
        return bucket_count_;
    }


private:
    static constexpr double PHI = 0.77351;
    size_t m_;
    uint32_t log2m_;
    uint64_t seed_;
    std::vector<uint64_t> bitmaps_;
    std::function<size_t(const std::string&, uint64_t)> hash1;
    std::function<size_t(const std::string&, uint64_t)> hash2;
    std::vector<int> bucket_count_;
    

    void initSeeds(int seed) {
       seed_ = seed;
    }


    // Initialize based on choice parameter (0–3)
    void initHash(string hash_type1, string hash_type2) {
        if (hash_type1 == "murmurhash2") {
            hash1 = &PCSA::murmurhash2;
            cout << "Using self-implemented MurmurHash2" << endl;
        } else if (hash_type1 == "fnv1a") {
            hash1 = &PCSA::fnv1a;
            cout << "Using self-implemented fnv1a" << endl;
        } else if (hash_type1 == "linearhash") {
            hash1 = &PCSA::linearhash;
            cout << "Using self-implemented linearhash" << endl;
        } else {
            hash1 = &PCSA::murmurhash_cpp;
            cout << "Using C++ MurmurHash2" << endl;
        }

        if (hash_type2 == "murmurhash2") {
            hash2 = &PCSA::murmurhash2;
            cout << "Using self-implemented MurmurHash2" << endl;
        } else if (hash_type2 == "fnv1a") {
            hash2 = &PCSA::fnv1a;
            cout << "Using self-implemented fnv1a" << endl;
        } else if (hash_type2 == "linearhash") {
            hash2 = &PCSA::linearhash;
            cout << "Using self-implemented linearhash" << endl;
        } else {
            hash2 = &PCSA::murmurhash_cpp;
            cout << "Using C++ MurmurHash2" << endl;
        }
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

    static size_t murmurhash2(const std::string& s, uint64_t seed_) {
        MurmurHash2_64 hasher;
        return hasher(std::to_string(seed_) + s);
    }
    static size_t fnv1a(const std::string& s, uint64_t seed_) {
        FNV1aHash64 hasher;
        return hasher(std::to_string(seed_) + s);
    }
    static size_t linearhash(const std::string& s, uint64_t seed_) {
        LinearHash hasher;
        return hasher(std::to_string(seed_) + s);
    }
    static size_t murmurhash_cpp(const std::string& s, uint64_t seed_) {
        std::hash<std::string> hasher;
        return hasher(std::to_string(seed_) + s);
    }
};


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

size_t getMemoryUsage() {
    task_basic_info info;
    mach_msg_type_number_t size = TASK_BASIC_INFO_COUNT;
    kern_return_t result = task_info(mach_task_self(), TASK_BASIC_INFO,
                                     (task_info_t)&info, &size);
    if (result != KERN_SUCCESS) return 0;
    return info.resident_size; // in bytes
}


int main(int argc, char* argv[]) {
    if (argc != 6) {
        std::cerr << "Usage: " << argv[0] << " <num_registers> <hash_type> <seed> <data_path>\n";
        return 1;
    }

    size_t m = std::stoull(argv[1]);
    std::string hash_type1 = argv[2];
    std::string hash_type2 = argv[3];
    int seed = std::stoi(argv[4]);
    std::string txt_path = argv[5];
    

    PCSA pcsa(m, hash_type1, hash_type2, seed);

    std::ifstream file(txt_path);
    std::vector<std::string> strings;
    std::string line;

    while (std::getline(file, line)) {
        strings.push_back(line);
    }

    auto start = std::chrono::high_resolution_clock::now();
    pcsa.addBatch(strings);
    auto end = std::chrono::high_resolution_clock::now();

    std::chrono::duration<double> duration = end - start;
    std::cout << "FM addBatch time: " << std::fixed << std::setprecision(6)
              << duration.count() << " seconds\n";

    std::cout << "Estimated cardinality: " << pcsa.estimate() << "\n";

    size_t mem = getMemoryUsage();
    size_t vec_mem = calculateMemoryUsage(strings);
    std::cout << "Memory usage: " << (mem - vec_mem) / (1024.0 * 1024.0) << " MB\n";

    std::vector<int> bucket_count = pcsa.get_bucket_count();
    std::cout << "Bucket counts: ";
    for (size_t i = 0; i < bucket_count.size(); ++i) {
        std::cout << bucket_count[i] << " ";
    }
    std::cout << std::endl;
    return 0;
}
