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

using namespace std;


#include <iostream>
#include <vector>
#include <cmath>
#include <string>
#include <functional>
#include <bitset>
#include <cassert>
#include <limits>

class HyperLogLog {
public:
    explicit HyperLogLog(uint32_t b) : b_(b), m_(1 << b), registers_(m_, 0) {
        assert(b_ >= 4 && b_ <= 16);
        alphaMM_ = getAlphaMM(m_);
    }

    void add(const std::string& item) {
        uint32_t hash = hash32(item);
        uint32_t index = hash >> (32 - b_);                      // First b bits
        uint32_t w = hash << b_;                                 // Remaining bits
        uint8_t rank = countLeadingZeros(w) + 1;
        registers_[index] = std::max(registers_[index], rank);
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


int main() {
    HyperLogLog hll(12); // m = 2^12 = 4096 registers

    // string txt_path = "/Users/lily/Documents/2024-2025_Spring/algorithm_lab/cadinality_estimation/COMP3022_Project/dataset/demo/output.txt";
    string txt_path = "/Users/lily/Documents/2024-2025_Spring/algorithm_lab/cadinality_estimation/COMP3022_Project/dataset/cleaned/NCVoters/ncvoter_all.txt";
    std::ifstream file(txt_path);
    std::vector<std::string> strings;
    std::string line;

    while (std::getline(file, line)) {
        strings.push_back(line);
    }

    for (const auto& str : strings) {
        hll.add(str);
    }


    std::cout << "Estimated cardinality: " << hll.estimate() << std::endl;
    return 0;
}
