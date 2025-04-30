#include <iostream>
#include <mach/mach.h>

size_t getMemoryUsage() {
    task_basic_info info;
    mach_msg_type_number_t size = TASK_BASIC_INFO_COUNT;
    kern_return_t result = task_info(mach_task_self(), TASK_BASIC_INFO,
                                     (task_info_t)&info, &size);
    if (result != KERN_SUCCESS) return 0;
    return info.resident_size; // in bytes
}

int main() {
    std::cout << "Program started.\n";

    // Your code here
    // Simulate allocation
    int* big_array = new int[10000000];

    // Log memory usage
    size_t mem = getMemoryUsage();
    std::cout << "Memory usage: " << mem / (1024.0 * 1024.0) << " MB\n";

    // Clean up
    delete[] big_array;

    std::cout << "Program finished.\n";
    return 0;
}
