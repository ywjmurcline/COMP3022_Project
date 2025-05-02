#include <iostream>
#include <vector>
#include <cmath>
#include <string>
#include <random>
#include <cassert>
#include <functional>
#include <fstream>

using namespace std;

class LogLog {
public:
    explicit LogLog(size_t m)
        : m_(m), seeds_(m), maxRho_(m, 0) {
        assert((m & (m - 1)) == 0);  // m must be power of 2
        initSeeds();
    }

    void add(const std::string& item) {
        addBatch({item});
    }

    void addBatch(const std::vector<std::string>& items) {
        for (const auto& it : items) {
            cout << it << endl;
            for (size_t i = 0; i < m_; ++i) {
                uint64_t h = hashWithSeed(it, seeds_[i]);
                uint32_t rho = leadingZeros(h) + 1;
                cout << rho << endl;
                if (rho > maxRho_[i]) {
                    maxRho_[i] = rho;
                }
            }
        }
    }

    double estimate() const {
        double sum = 0.0;
        for (auto r : maxRho_) {
            sum += r;
        }
        // cout << "avg: " << avg << endl;
        double avg = sum / static_cast<double>(m_);
        cout << "avg: " << avg << endl;
        // Use correction constant as per the LogLog paper
        double alpha = 0.39701; // for large m, this stabilizes
        return alpha * m_ * std::pow(2.0, avg);
    }

private:
    size_t m_;
    std::vector<uint64_t> seeds_;
    std::vector<uint32_t> maxRho_;

    void initSeeds() {
        std::mt19937_64 rng(1337);
        std::uniform_int_distribution<uint64_t> dist;
        for (auto& s : seeds_) {
            s = dist(rng);
        }
    }

    static uint32_t leadingZeros(uint64_t x) {
        if (x == 0) return 64;
        return __builtin_clzll(x);
    }

    static uint64_t hashWithSeed(const std::string& s, uint64_t seed) {
        std::hash<std::string> hasher;
        return hasher(std::to_string(seed) + s);
    }
};

int main() {
    LogLog loglog(4); // m = 64 registers

    // std::vector<std::string> data = {
    //     "apple", "banana", "orange", "apple", "banana",
    //     "grape", "kiwi", "melon", "peach", "plum",
    //     "orange", "grapefruit", "blueberry", "strawberry"
    // };

    string txt_path = "/Users/lily/Documents/2024-2025_Spring/algorithm_lab/cadinality_estimation/COMP3022_Project/dataset/demo/output.txt";
    std::ifstream file(txt_path);
    std::vector<std::string> strings;
    std::string line;

    while (std::getline(file, line)) {
        strings.push_back(line);
    }

    loglog.addBatch(strings);

    std::cout << "Estimated number of distinct elements: " << loglog.estimate() << std::endl;
    return 0;
}
