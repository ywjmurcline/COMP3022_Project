#include <iostream>
#include <vector>
#include <cmath>
#include <bitset>
#include <string>
#include <unordered_set>
#include <functional>
#include <limits>
#include <cassert>
#include <fstream>
#include <mach/mach.h>
#include <iomanip>
#include "hash/LinearHash.hpp"
#include "hash/MurmurHash2.hpp"
#include "hash/FNV.hpp"
#include <functional>

using namespace std;


class HyperLogLog {
public:
    explicit HyperLogLog(uint32_t m, std::string hash_type1, std::string hash_type2, int seed) 
    : m_(m), log2m_(std::log2(m)), registers_(m_, 0), bucket_count_(m, 0){
        alphaMM_ = getAlphaMM(m);
        initSeeds(seed);
        initHash(hash_type1, hash_type2);
    }

    void add(const std::string& item) {
        addBatch({item});
    }
    void addBatch(const std::vector<std::string>& items) {
        for (const auto& item : items) {
            uint32_t h1 = hash1(item, seed_);
            uint32_t index = h1 >> (64 - log2m_);   
                               // First b bits
            // use second hash function to get the remaining bits
            size_t h2 = hash2(item, seed_);
            size_t remaining = h2 & ((1ULL << (64 - log2m_)) - 1);   
                                         // Remaining bits
            uint8_t rank = TrailingZeroes(remaining);

            registers_[index] = std::max(registers_[index], rank);
            bucket_count_[index] += 1; // Increment the count for this bucket
        }
    }

    double estimate() const {
        // Harmonic mean of 2^-Ri
        double sum = 0.0;
        for (uint8_t r : registers_) {
            sum += 1.0 / (1ULL << r);
        }

        double rawEstimate = alphaMM_ / sum;

        // Small range correction (Linear Counting)
        if (rawEstimate <= 2.5 * m_) {
            uint32_t V = std::count(registers_.begin(), registers_.end(), 0);
            if (V != 0) {
                return m_ * std::log(static_cast<double>(m_) / V);
            }
        }

        // Large range correction
        if (rawEstimate > (1ULL << 32) / 30.0) {
            return -static_cast<double>(1ULL << 32) *
                   std::log(1.0 - (rawEstimate / (1ULL << 32)));
        }

        return rawEstimate;
    }

    std::vector<int> get_bucket_count() {
        return bucket_count_;
    }

private:
    uint32_t log2m_;
    uint32_t m_;
    double alphaMM_;
    uint64_t seed_;
    std::vector<uint8_t> registers_;
    std::function<size_t(const std::string&, uint64_t)> hash1;
    std::function<size_t(const std::string&, uint64_t)> hash2;
    std::vector<int> bucket_count_;

    static double getAlphaMM(uint32_t m) {
        switch (m) {
            case 16:  return 0.673 * m * m;
            case 32:  return 0.697 * m * m;
            case 64:  return 0.709 * m * m;
            default:  return (0.7213 / (1.0 + 1.079 / m)) * m * m;
        }
    }

    void initSeeds(int seed) {
        seed_ = seed;
     }

    // Initialize based on choice parameter (0–3)
    void initHash(string hash_type1, string hash_type2) {
        if (hash_type1 == "murmurhash2") {
            hash1 = &HyperLogLog::murmurhash2;
            cout << "Using self-implemented MurmurHash2" << endl;
        } else if (hash_type1 == "fnv1a") {
            hash1 = &HyperLogLog::fnv1a;
            cout << "Using self-implemented fnv1a" << endl;
        } else if (hash_type1 == "linearhash") {
            hash1 = &HyperLogLog::linearhash;
            cout << "Using self-implemented linearhash" << endl;
        } else {
            hash1 = &HyperLogLog::murmurhash_cpp;
            cout << "Using C++ MurmurHash2" << endl;
        }

        if (hash_type2 == "murmurhash2") {
            hash2 = &HyperLogLog::murmurhash2;
            cout << "Using self-implemented MurmurHash2" << endl;
        } else if (hash_type2 == "fnv1a") {
            hash2 = &HyperLogLog::fnv1a;
            cout << "Using self-implemented fnv1a" << endl;
        } else if (hash_type2 == "linearhash") {
            hash2 = &HyperLogLog::linearhash;
            cout << "Using self-implemented linearhash" << endl;
        } else {
            hash2 = &HyperLogLog::murmurhash_cpp;
            cout << "Using C++ MurmurHash2" << endl;
        }
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

    // least significant 1, that is number of trailing zeros
    uint32_t TrailingZeroes(size_t x) {
        return (x ? __builtin_ctzll(x): 64) + 1;
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
    if (argc != 6) {
        std::cerr << "Usage: " << argv[0] << " <num_registers> <hash_type> <seed> <data_path>\n";
        return 1;
    }

    size_t m = std::stoull(argv[1]);
    std::string hash_type1 = argv[2];
    std::string hash_type2 = argv[3];
    int seed = std::stoi(argv[4]);
    std::string txt_path = argv[5];


    HyperLogLog hll(m, hash_type1, hash_type2, seed); // m = 2^12 = 4096 registers

    std::ifstream file(txt_path);
    std::vector<std::string> strings;
    std::string line;

    while (std::getline(file, line)) {
        strings.push_back(line);
    }

    // for (const auto& str : strings) {
    //     hll.add(str);
    // }
    auto start = std::chrono::high_resolution_clock::now();
    hll.addBatch(strings);
    auto end = std::chrono::high_resolution_clock::now();

    std::chrono::duration<double> duration = end - start;
    std::cout << "FM addBatch time: " << std::fixed << std::setprecision(6)
              << duration.count() << " seconds\n";

    std::cout << "Estimated cardinality: " << hll.estimate() << std::endl;
    
    size_t mem = getMemoryUsage();
    size_t vec_mem = calculateMemoryUsage(strings);
    std::cout << "Memory usage: " << (mem - vec_mem) / (1024.0 * 1024.0) << " MB\n";
    std::vector<int> bucket_count = hll.get_bucket_count();
    std::cout << "Bucket counts: ";
    for (size_t i = 0; i < bucket_count.size(); ++i) {
        std::cout << bucket_count[i] << " ";
    }
    std::cout << std::endl;
    return 0;
}
