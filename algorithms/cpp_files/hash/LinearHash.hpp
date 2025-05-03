#ifndef LINEARHASH_HPP
#define LINEARHASH_HPP

#include <string>
#include <cstdint>

class LinearHash {
public:
    // Constructor with an optional multiplier (default: 31)
    explicit LinearHash(uint64_t multiplier = 31) 
        : multiplier_(multiplier) {}

    // Hashing function
    size_t operator()(const std::string& s) const {
        uint64_t hash = 0;
        for (char c : s) {
            hash = hash * multiplier_ + static_cast<unsigned char>(c);
        }
        return static_cast<size_t>(hash);
    }

private:
    uint64_t multiplier_;
};

#endif // LINEARHASH_HPP