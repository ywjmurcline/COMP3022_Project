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
    explicit PCSA(size_t m)
        : m_(m), log2m_(std::log2(m_)), bitmaps_(m, 0) {
        assert(m > 0); // m must be power of 2
    }

    void add(const std::string& item) {
        addBatch({item});
    }

    void addBatch(const std::vector<std::string>& items) {
        for (const auto& item : items) {
            size_t h = hash(item);
            size_t idx = h >> (64 - log2m_); // use top bits to choose bitmap
            // cout << "idx:  " << idx << endl;
            // cout << "h:  " << size_t_to_binary(h) << endl;

            // size_t remaining = (h << log2m_); // discard used top bits
            size_t remaining = h & ((1ULL << (64 - log2m_)) - 1);
            // cout << "remaining:  " << size_t_to_binary(remaining) << endl;

            uint32_t r = rank(remaining);
            // cout << "r:  " << r << endl;
            if (r < 64) {
                bitmaps_[idx] |= (1ULL << r);
            }
            // cout << "remaining:  " << size_t_to_binary(bitmaps_[idx]) << endl;

            // cout << bitmaps_[idx] << endl;
            // for (uint32_t i = 0; i < 64; ++i) {
            //     if ((bitmaps_[idx] & (1ULL << i)) == 0)
            //         cout << "immediate i: " << i << endl;
            // }
        }

    }

    double estimate() const {
        double sum_R = 0.0;
        for (uint64_t bitmap : bitmaps_) {
            // cout << "bitmap: " << bitmap << endl;
            uint32_t R = firstZeroBit(bitmap);
            // cout << "R:  " << R << endl;
            sum_R += R;
            // cout << "sum_R:  " << sum_R << endl;
        }

        double R_avg = sum_R / static_cast<double>(m_);
        return (m_ / PHI) * std::pow(2.0, R_avg);
    }

private:
    static constexpr double PHI = 0.77351;
    size_t m_;
    uint32_t log2m_;
    std::vector<uint64_t> bitmaps_;

    static size_t hash(const std::string& s) {
        std::hash<std::string> hasher;
        return hasher(s);
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

    // static size_t nextPowerOfTwo(size_t n) {
    //     size_t p = 1;
    //     while (p < n) p <<= 1;
    //     return p;
    // }
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
    if (argc != 3) {
        std::cerr << "Usage: " << argv[0] << " <num_registers> <data_string>\n";
        return 1;
    }

    size_t m = std::stoull(argv[1]);
    std::string txt_path = argv[2];

    PCSA pcsa(m);

    // string txt_path = "/Users/lily/Documents/2024-2025_Spring/algorithm_lab/cadinality_estimation/COMP3022_Project/dataset/demo/output.txt";
    // string txt_path = "/Users/lily/Documents/2024-2025_Spring/algorithm_lab/cadinality_estimation/COMP3022_Project/dataset/cleaned/NCVoters/ncvoter_all.txt";
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

    // Approximate memory usage
    // size_t memory_bytes = m * (sizeof(uint64_t) /* bitmap */ + sizeof(uint64_t) /* seed */);
    // std::cout << "Approx. memory usage: " << memory_bytes / 1024.0 << " KB\n";

    size_t mem = getMemoryUsage();
    size_t vec_mem = calculateMemoryUsage(strings);
    std::cout << "Memory usage: " << (mem - vec_mem) / (1024.0 * 1024.0) << " MB\n";
    return 0;
}
