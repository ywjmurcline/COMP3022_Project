#ifndef MURMURHASH2_HPP
#define MURMURHASH2_HPP

#include <cstdint>
#include <cstddef>
#include <string>

class MurmurHash2_64 {
public:
    explicit MurmurHash2_64(uint64_t seed = 0) : seed_(seed) {}

    size_t operator()(const std::string& s) const {
        return hash(s.data(), s.length(), seed_);
    }

    static uint64_t hash(const void* key, size_t len, uint64_t seed) {
        const uint64_t m = 0xc6a4a7935bd1e995ULL;
        const int r = 47;

        uint64_t h = seed ^ (len * m);
        const uint64_t* data = static_cast<const uint64_t*>(key);
        const uint64_t* end = data + (len / 8);

        while (data != end) {
            uint64_t k = *data++;
            k *= m;
            k ^= k >> r;
            k *= m;

            h ^= k;
            h *= m;
        }

        const uint8_t* data2 = reinterpret_cast<const uint8_t*>(data);
        switch (len & 7) {
            case 7: h ^= uint64_t(data2[6]) << 48;
            case 6: h ^= uint64_t(data2[5]) << 40;
            case 5: h ^= uint64_t(data2[4]) << 32;
            case 4: h ^= uint64_t(data2[3]) << 24;
            case 3: h ^= uint64_t(data2[2]) << 16;
            case 2: h ^= uint64_t(data2[1]) << 8;
            case 1: h ^= uint64_t(data2[0]);
                    h *= m;
        }

        h ^= h >> r;
        h *= m;
        h ^= h >> r;

        return h;
    }

private:
    uint64_t seed_;
};

#endif // MURMURHASH2_HPP
