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

int main() {
    // size_t m = 5;  // registers per group
    // size_t L = 5;   // number of groups

    AMS fm(64);

    // for (int i = 0; i < 100000; ++i) {
    //     fm.add("user_" + std::to_string(i));
    // }
    // string txt_path = "/Users/lily/Documents/2024-2025_Spring/algorithm_lab/cadinality_estimation/COMP3022_Project/dataset/demo/output.txt";
    string txt_path = "/Users/lily/Documents/2024-2025_Spring/algorithm_lab/cadinality_estimation/COMP3022_Project/dataset/cleaned/NCVoters/ncvoter_all.txt";
    std::ifstream file(txt_path);
    std::vector<std::string> strings;
    std::string line;

    while (std::getline(file, line)) {
        strings.push_back(line);
    }

    // // Print all strings
    // for (const auto& str : strings) {
    //     fm.add(str);
    // }
    auto start = std::chrono::high_resolution_clock::now();
    fm.addBatch(strings);
    auto end = std::chrono::high_resolution_clock::now();

    std::chrono::duration<double> duration = end - start;
    std::cout << "FM addBatch time: " << std::fixed << std::setprecision(6)
              << duration.count() << " seconds\n";

    std::cout << "Estimated cardinality: " << fm.estimate() << "\n";

    // Approximate memory usage
    // size_t memory_bytes = m * (sizeof(uint64_t) /* bitmap */ + sizeof(uint64_t) /* seed */);
    // std::cout << "Approx. memory usage: " << memory_bytes / 1024.0 << " KB\n";

    size_t mem = getMemoryUsage();
    std::cout << "Memory usage: " << mem / (1024.0 * 1024.0) << " MB\n";
    return 0;
}
