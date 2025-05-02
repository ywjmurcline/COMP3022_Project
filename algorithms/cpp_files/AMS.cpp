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

using namespace std;

class AMS {
public:
    explicit AMS(size_t m)
        : m_(m), seeds_(m), Z_(m, 0) {
        assert(m > 0);
        initSeeds();
    }

    void add(const std::string& item) {
        addBatch({item});
    }

    void addBatch(const std::vector<std::string>& items) {
        for (const auto& item : items) {
            for (size_t i = 0; i < m_; ++i) {
                uint64_t h = hashWithSeed(item, seeds_[i]);
                uint32_t r = rank(h);
    
                Z_[i] = std::max(r, Z_[i]);
            }
        }
    }

    double estimate() const {
        double average = 0;
        for (double z : Z_) {
            average += z;
        }
        average /= m_;
        return std::pow(2.0, average);
    }

private:
    size_t m_;
    std::vector<uint64_t> seeds_;
    std::vector<uint32_t> Z_;  // Accumulators per sketch

    void initSeeds() {
        std::mt19937_64 rng(424242);
        std::uniform_int_distribution<uint64_t> dist;
        for (auto& s : seeds_) {
            s = dist(rng);
        }
    }

    static uint32_t rank(size_t x) {
        return x ? __builtin_ctzll(x) : 64;
    }


    static size_t hashWithSeed(const std::string& s, uint64_t seed) {
        std::hash<std::string> hasher;
        return hasher(std::to_string(seed) + s);
    }

    static uint32_t msb(uint64_t x) {
        if (x == 0) return 0;
        return 63 - __builtin_clzll(x);
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
    if (argc != 3) {
        std::cerr << "Usage: " << argv[0] << " <num_registers> <data_string>\n";
        return 1;
    }

    size_t m = std::stoull(argv[1]);
    std::string txt_path = argv[2];

    AMS ams(m);

    
    std::ifstream file(txt_path);
    std::vector<std::string> strings;
    std::string line;

    while (std::getline(file, line)) {
        strings.push_back(line);
    }


    auto start = std::chrono::high_resolution_clock::now();
    ams.addBatch(strings);
    auto end = std::chrono::high_resolution_clock::now();

    std::chrono::duration<double> duration = end - start;
    std::cout << "FM addBatch time: " << std::fixed << std::setprecision(6)
              << duration.count() << " seconds\n";

    std::cout << "Estimated cardinality: " << ams.estimate() << "\n";

    // Approximate memory usage
    // size_t memory_bytes = m * (sizeof(uint64_t) /* bitmap */ + sizeof(uint64_t) /* seed */);
    // std::cout << "Approx. memory usage: " << memory_bytes / 1024.0 << " KB\n";
    size_t mem = getMemoryUsage();
    size_t vec_mem = calculateMemoryUsage(strings);
    std::cout << "Memory usage: " << (mem - vec_mem) / (1024.0 * 1024.0) << " MB\n";
    return 0;
}
