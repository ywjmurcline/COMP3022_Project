#ifndef FNV_HPP
#define FNV_HPP

#include <string>
#include <cstdint>

class FNV1aHash64 {
public:
    // 64-bit FNV-1a constants
    static constexpr uint64_t OFFSET_BASIS = 14695981039346656037ULL;
    static constexpr uint64_t FNV_PRIME     = 1099511628211ULL;

    FNV1aHash64() = default;

    // Hash a string
    size_t operator()(const std::string& s) const {
        return hash(s.data(), s.size());
    }

    // Hash arbitrary binary data
    static size_t hash(const void* data, size_t len) {
        const uint8_t* bytes = static_cast<const uint8_t*>(data);
        uint64_t hash = OFFSET_BASIS;

        for (size_t i = 0; i < len; ++i) {
            hash ^= static_cast<uint64_t>(bytes[i]);
            hash *= FNV_PRIME;
        }

        return static_cast<size_t>(hash);
    }
};

#endif // FNV_HPP
