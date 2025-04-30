// utils.h
#ifndef UTILS_H  // Header guard (prevents double inclusion)
#define UTILS_H

#include <stdint.h>
#include <iostream>

void print_uint8_t_hex(uint8_t *hash_result) {
    int len = (int) sizeof(hash_result); 
    for (int i = 0; i < 16; i++) printf("%02x", hash_result[i]);

}

void print_unit8_t_bin(uint8_t *hash_result) {
    int len = (int) sizeof(hash_result); 
    for (int i = 0; i < len; i++) {
        for (int j = 7; j >= 0; j--) {
            printf("%d", (hash_result[i] >> j) & 1);
        }
        printf(" "); // Optional: space between bytes
    }
}

#endif