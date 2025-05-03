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



class PCSA {
public:
    explicit PCSA(size_t m, std::string hash_type)
        : m_(m), log2m_(std::log2(m_)), bitmaps_(m, 0) {
        assert(m > 0); // m must be power of 2
        initHash(hash_type);
    }

    void add(const std::string& item) {
        addBatch({item});
    }

    void addBatch(const std::vector<std::string>& items) {
        for (const auto& item : items) {
            size_t h = hash(item);
            size_t idx = h >> (64 - log2m_); // use top bits to choose bitmap

            size_t remaining = h & ((1ULL << (64 - log2m_)) - 1);

            uint32_t r = rank(remaining);
            if (r < 64) {
                bitmaps_[idx] |= (1ULL << r);
            }
        }

    }

    double estimate() const {
        double sum_R = 0.0;
        for (uint64_t bitmap : bitmaps_) {
            uint32_t R = firstZeroBit(bitmap);
            sum_R += R;
        }

        double R_avg = sum_R / static_cast<double>(m_);
        return (m_ / PHI) * std::pow(2.0, R_avg);
    }

private:
    static constexpr double PHI = 0.77351;
    size_t m_;
    uint32_t log2m_;
    std::vector<uint64_t> bitmaps_;
    std::function<size_t(const std::string&)> hash;

    // static size_t hash(const std::string& s, string hash_type_) {
    //     if (hash_type_ == "murmur") {
    //         std::hash<std::string> hasher;
    //         return hasher(s);
    //     } else if (hash_type_ == "linear") {
    //         LinearHash hasher;
    //         return hasher(s);
    //     }
        
    // }

    // Initialize based on choice parameter (0–3)
    void initHash(string hash_type) {
        if (hash_type == "murmurhash2") {
            hash = &PCSA::murmurhash2;
            cout << "Using self-implemented MurmurHash2" << endl;
        } else if (hash_type == "fnv1a") {
            hash = &PCSA::fnv1a;
            cout << "Using self-implemented fnv1a" << endl;
        } else if (hash_type == "linearhash") {
            hash = &PCSA::linearhash;
            cout << "Using self-implemented linearhash" << endl;
        } else {
            hash = &PCSA::murmurhash_cpp;
            cout << "Using C++ MurmurHash2" << endl;
        }
    }

    static uint32_t rank(size_t x) {
        return x ? __builtin_ctzll(x): 64;
    }

    static uint32_t firstZeroBit(uint64_t bitmap) {
        for (uint32_t i = 0; i < 64; ++i) {
            if ((bitmap & (1ULL << i)) == 0)
                return i;
        }
        return 64;
    }

    static size_t murmurhash2(const std::string& s) {
        MurmurHash2_64 hasher;
        return hasher(s);
    }
    static size_t fnv1a(const std::string& s) {
        FNV1aHash64 hasher;
        return hasher(s);
    }
    static size_t linearhash(const std::string& s) {
        LinearHash hasher;
        return hasher(s);
    }
    static size_t murmurhash_cpp(const std::string& s) {
        std::hash<std::string> hasher;
        return hasher(s);
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
    if (argc != 4) {
        std::cerr << "Usage: " << argv[0] << " <num_registers> <data_string>\n";
        return 1;
    }

    size_t m = std::stoull(argv[1]);
    std::string hash_type = argv[2];
    std::string txt_path = argv[3];
    

    PCSA pcsa(m, hash_type);

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
    return 0;
}
