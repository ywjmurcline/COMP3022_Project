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
#include <thread>

using namespace std;


// class FlajoletMartin {
// public:
//     explicit FlajoletMartin(size_t m)
//         : m_(m), seeds_(m), registers_(m, 0) {
//         assert(m > 0);
//         initSeeds();
//     }

//     void add(const std::string& item) {
//         for (size_t i = 0; i < m_; ++i) {
//             size_t h = hashWithSeed(item, seeds_[i]);
//             uint32_t r = rank(h);
//             registers_[i] = std::max(registers_[i], r);
//         }
//     }

//     double estimate() const {
//         double Z = 0.0;
//         for (uint32_t r : registers_) {
//             Z += std::pow(2.0, static_cast<int>(r));
//         }
//         return Z / m_;
//     }

// private:
//     size_t m_;
//     std::vector<uint64_t> seeds_;
//     std::vector<uint32_t> registers_;

//     void initSeeds() {
//         std::mt19937_64 rng(42);
//         std::uniform_int_distribution<uint64_t> dist;
//         for (auto& s : seeds_) {
//             s = dist(rng);
//         }
//         std::cout << "seed_: ";
//         for (const auto& seed : seeds_) {
//             std::cout << seed << " ";
//         }
//         std::cout << std::endl;
//     }

//     static uint32_t rank(size_t x) {
//         // cout << "rank: " << (x ? __builtin_ctzll(x) + 1 : 0) << endl;
//         return x ? __builtin_ctzll(x) + 1 : 0;
//     }

//     static size_t hashWithSeed(const std::string& s, uint64_t seed) {
//         std::hash<std::string> hasher;
//         return hasher(std::to_string(seed) + s);
//     }
// };


// class FlajoletMartin {
// public:
//     explicit FlajoletMartin(size_t m)
//         : m_(m), seeds_(m), bitmaps_(m, 0) {
//         assert(m > 0);
//         initSeeds();
//     }

//     void add(const std::string& item) {
//         for (size_t i = 0; i < m_; ++i) {
//             size_t h = hashWithSeed(item, seeds_[i]);
//             uint32_t r = rank(h);
            
//             if (r < 64) {  // Cap to bitmap size
//                 bitmaps_[i] |= (1ULL << r);
//             }
//             cout << "r: " << r << endl;
//             std::cout << "bitmap: " <<  (1ULL << r) << std::endl;

//         }
//     }

//     double estimate() const {
//         double Z = 0.0;
//         for (uint64_t bitmap : bitmaps_) {
//             uint32_t R = firstZeroBit(bitmap);
//             Z += std::pow(2.0, R);
//         }
//         return Z / m_;
//     }

// private:
//     size_t m_;
//     std::vector<uint64_t> seeds_;
//     std::vector<uint64_t> bitmaps_;  // Each is a 64-bit bitmap

//     void initSeeds() {
//         std::mt19937_64 rng(1337);
//         std::uniform_int_distribution<uint64_t> dist;
//         for (auto& s : seeds_) {
//             s = dist(rng);
//         }
//     }

//     static uint32_t rank(size_t x) {
//         return x ? __builtin_ctzll(x) : 64;  // 64 is "off the map"
//     }

//     static uint32_t firstZeroBit(uint64_t bitmap) {
//         for (uint32_t i = 0; i < 64; ++i) {
//             if ((bitmap & (1ULL << i)) == 0)
//                 return i;
//         }
//         return 64;  // Fully saturated
//     }

//     static size_t hashWithSeed(const std::string& s, uint64_t seed) {
//         std::hash<std::string> hasher;
//         return hasher(std::to_string(seed) + s);
//     }
// };



class FlajoletMartin {
public:
    explicit FlajoletMartin(size_t m)
        : m_(m), seeds_(m), bitmaps_(m, 0) {
        assert(m > 0);
        initSeeds();
    }

    void add(const std::string& item) {
        addBatch({item});
    }

    void addBatch(const std::vector<std::string>& items) {
        const size_t num_threads = std::min((int)m_, (int)std::thread::hardware_concurrency());
        std::vector<std::thread> threads;

        auto worker = [&](size_t start, size_t end) {
            for (size_t i = start; i < end; ++i) {
                for (const auto& item : items) {
                    size_t h = hashWithSeed(item, seeds_[i]);
                    uint32_t r = rank(h);
                    if (r < 64) {
                        uint64_t mask = 1ULL << r;
                        bitmaps_[i] |= mask;  // No race: i is thread-private
                    }
                }
            }
        };

        size_t chunk_size = (m_ + num_threads - 1) / num_threads;
        for (size_t t = 0; t < num_threads; ++t) {
            size_t start = t * chunk_size;
            size_t end = std::min(start + chunk_size, m_);
            if (start < end) {
                threads.emplace_back(worker, start, end);
            }
        }

        for (auto& th : threads) {
            th.join();
        }
    }

    double estimate() const {
        double Z = 0.0;
        for (uint64_t bitmap : bitmaps_) {
            uint32_t R = firstZeroBit(bitmap);
            Z += std::pow(2.0, R);
        }
        return Z / m_;
    }

private:
    size_t m_;
    std::vector<uint64_t> seeds_;
    std::vector<uint64_t> bitmaps_;

    void initSeeds() {
        std::mt19937_64 rng(1337);
        std::uniform_int_distribution<uint64_t> dist;
        for (auto& s : seeds_) {
            s = dist(rng);
        }
    }

    static uint32_t rank(size_t x) {
        return x ? __builtin_ctzll(x) : 64;
    }

    static uint32_t firstZeroBit(uint64_t bitmap) {
        for (uint32_t i = 0; i < 64; ++i) {
            if ((bitmap & (1ULL << i)) == 0)
                return i;
        }
        return 64;
    }

    static size_t hashWithSeed(const std::string& s, uint64_t seed) {
        std::hash<std::string> hasher;
        return hasher(std::to_string(seed) + s);
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

    FlajoletMartin fm(64);

    // for (int i = 0; i < 100000; ++i) {
    //     fm.add("user_" + std::to_string(i));
    // }

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
