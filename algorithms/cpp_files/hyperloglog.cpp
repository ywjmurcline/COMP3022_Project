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


using namespace std;


class HyperLogLog {
public:
    explicit HyperLogLog(uint32_t m) : m_(m), b_(std::log2(m)), registers_(m_, 0) {
        // assert(b_ >= 4 && b_ <= 16);
        assert(m_ >= 16 && m_ <= 239755970);
        alphaMM_ = getAlphaMM(m_);
    }


    void add(const std::string& item) {
        addBatch({item});
    }

    // void add(const std::string& item) {
    //     uint32_t hash = hash32(item);
    //     uint32_t index = hash >> (32 - b_);                      // First b bits
    //     uint32_t w = hash << b_;                                 // Remaining bits
    //     uint8_t rank = countLeadingZeros(w) + 1;
    //     registers_[index] = std::max(registers_[index], rank);
    // }

    void addBatch(const std::vector<std::string>& items) {
        for (const auto& item : items) {
            uint32_t hash = hash32(item);
            uint32_t index = hash >> (32 - b_);                      // First b bits
            uint32_t w = hash << b_;                                 // Remaining bits
            uint8_t rank = countLeadingZeros(w) + 1;
            registers_[index] = std::max(registers_[index], rank);
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

private:
    uint32_t b_;
    uint32_t m_;
    double alphaMM_;
    std::vector<uint8_t> registers_;

    static double getAlphaMM(uint32_t m) {
        switch (m) {
            case 16:  return 0.673 * m * m;
            case 32:  return 0.697 * m * m;
            case 64:  return 0.709 * m * m;
            default:  return (0.7213 / (1.0 + 1.079 / m)) * m * m;
        }
    }

    static uint8_t countLeadingZeros(uint32_t x) {
        if (x == 0) return 32;
        return __builtin_clz(x);
    }

    static uint32_t hash32(const std::string& s) {
        std::hash<std::string> hasher;
        return static_cast<uint32_t>(hasher(s));  // Truncate to 32-bit
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


    HyperLogLog hll(m); // m = 2^12 = 4096 registers

    // string txt_path = "/Users/lily/Documents/2024-2025_Spring/algorithm_lab/cadinality_estimation/COMP3022_Project/dataset/demo/output.txt";
    // string txt_path = "/Users/lily/Documents/2024-2025_Spring/algorithm_lab/cadinality_estimation/COMP3022_Project/dataset/cleaned/NCVoters/ncvoter_all.txt";
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
    return 0;
}
