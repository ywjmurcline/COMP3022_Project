#ifndef LINEARHASH_HPP
#define LINEARHASH_HPP

#include <string>
#include <cstdint>
#include <random>

// class LinearHash {
// public:
//     // Constructor with an optional multiplier (default: 31)
//     explicit LinearHash(uint64_t multiplier = 31) 
//         : multiplier_(multiplier) {}

//     // Hashing function
//     size_t operator()(const std::string& s) const {
//         uint64_t hash = 0;
//         for (char c : s) {
//             hash = hash * multiplier_ + static_cast<unsigned char>(c);
//         }
//         return static_cast<size_t>(hash);
//     }

// private:
//     uint64_t multiplier_;
// };

class LinearHash {
    public:
        explicit LinearHash(uint64_t m =601498281960143, uint64_t p = 2305843009213693951ULL)  // p = 2^61 - 1
            : m_(m), p_(p) {
            a_ = 792302817513587;
            b_ = 470109996110717;
        }

        size_t operator()(const std::string& s) const {
            uint64_t hash_val = stringToUint64(s);
            return ((a_ * hash_val+ b_) % p_) % m_;
        }
        

        private:
            uint64_t a_, b_, p_, m_;

            uint64_t stringToUint64(const std::string& s) const {
                const uint64_t base = 127;
                uint64_t hash = 0;
                for (char c : s) {
                    hash = (hash * base + static_cast<unsigned char>(c)) % p_;
                }
                return hash;
            }
};

#endif // LINEARHASH_HPP