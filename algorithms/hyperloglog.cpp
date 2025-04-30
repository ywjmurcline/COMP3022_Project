#include <iostream>
#include <vector>
#include <cmath>
#include <bitset>
#include <string>
#include <unordered_set>
#include <functional>
#include <limits>
#include <cassert>

using namespace std;

// Constants for bias correction
double getAlphaM(int m) {
    if (m == 16) return 0.673;
    else if (m == 32) return 0.697;
    else if (m == 64) return 0.709;
    else return 0.7213 / (1 + 1.079 / m);
}

// Function to get the position of the leftmost 1-bit in a binary string
int rho(const string& w) {
    for (size_t i = 0; i < w.size(); ++i) {
        if (w[i] == '1') return i + 1;
    }
    return w.size() + 1;
}

// Main HyperLogLog function
double hyperloglog(const vector<string>& data, int b) {
    assert(b > 0);
    int m = 1 << b; // m = 2^b
    cout << "m: " << m << endl;

    vector<int> M(m, numeric_limits<int>::min());

    cout << "M: " << endl;
    for (const auto& str : M) {
        std::cout << str << std::endl;
    }

    hash<string> hasher;

    for (const auto& v : data) {
        // Hash the input item to a 64-bit value

        cout << "v: " << v << endl;
        size_t x = hasher(v);

        cout << "x: " << x << endl;

        // Convert to binary string
        bitset<64> bits(x);
        string bin = bits.to_string();

        cout << "bin: " << bin << endl;

        // First b bits determine the register index j
        string j_str = bin.substr(0, b);
        cout << "j_str: " << j_str << endl;
        int j = 1 + stoi(j_str, nullptr, 2);
        cout << "j: " << j << endl;

        // Remaining bits are used to compute ρ(w)
        string w = bin.substr(b);
        cout << "w: " << w << endl;
        int r = rho(w);
        cout << "r: " << r << endl;

        // Update register
        M[j] = max(M[j], r);
    }

    // Compute indicator function Z
    double Z = 0.0;
    for (int j = 0; j < m; ++j) {
        Z += pow(2.0, -M[j]);
    }
    Z = 1.0 / Z;

    // Apply the HyperLogLog estimator
    double alpha_m = getAlphaM(m);
    double E = alpha_m * m * m * Z;
    return E;
}

int main() {
    // Sample dataset (simulate multiset input)
    vector<string> dataset = {"apple", "banana", "orange", "apple", "grape", "banana", "kiwi", "pineapple", "strawberry", "pear", "durian"};

    int b = 1; // log2(m), where m is the number of registers (e.g., m = 16)
    double estimate = hyperloglog(dataset, b);

    cout << "Estimated cardinality: " << estimate << endl;

    return 0;
}
