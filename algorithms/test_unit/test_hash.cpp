#include <stdint.h>  // For uint32_t
#include "hash/murmurhash3.h"
#include <iostream>
#include "utils.hpp"



int main(){
    // Your data
    const char *data = "help";
    int length = (int) strlen(data); 
    uint32_t seed = 0;
    uint8_t hash_result[16]; // 128-bit = 16 bytes

    // Compute hash

    MurmurHash3_x64_128(data, length, seed, hash_result);

    print_uint8_t_hex(hash_result);

    // for (int i = 0; i < 16; i++) printf("%02x", hash_result[i]);

    
    // size_t _length = sizeof(hash_result);  // Returns 16 (bytes)

    // std::cout << std::endl << (int) _length << std::endl;
    // Prints each byte as 2-digit hex, concatenated
}


// hash_result now contains the 128-bit hash