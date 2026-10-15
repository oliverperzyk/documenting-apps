#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <random>
#include <string_view>
#include <vector>

// Badanie D: porównania std::sort (własny komparator) vs instrumentowany Bubble
// Sort.
constexpr std::array<std::size_t, 4> sizes = { 500, 1000, 2000, 4000 };
constexpr std::uint32_t seed = 20260401;

enum class InputOrder { Sorted, Reversed, Pseudorandom };

constexpr std::array<InputOrder, 3> input_orders = { InputOrder::Sorted, InputOrder::Reversed,
                                                     InputOrder::Pseudorandom };

struct SortStats {
    std::uint64_t comparisons = 0;
    std::uint64_t swaps = 0;
    std::uint64_t passes = 0;
};

struct CountingLess {
    std::uint64_t *comparisons = nullptr;
    bool operator()(int a, int b) const {
        ++(*comparisons);
        return a < b;
    }
};

std::string_view order_name(InputOrder order) {
    switch (order) {
    case InputOrder::Sorted:
        return "sorted";
    case InputOrder::Reversed:
        return "reversed";
    case InputOrder::Pseudorandom:
        return "pseudorandom";
    }
    return "unknown";
}

std::vector<int> make_data(std::size_t size, InputOrder order, std::uint32_t data_seed) {
    std::vector<int> values(size);
    if (order == InputOrder::Sorted) {
        std::iota(values.begin(), values.end(), 0);
    } else if (order == InputOrder::Reversed) {
        std::iota(values.begin(), values.end(), 0);
        std::reverse(values.begin(), values.end());
    } else {
        std::mt19937 generator(data_seed);
        for (int &value : values) {
            value = static_cast<int>(generator() % 10'000U);
        }
    }
    return values;
}

std::uint64_t fingerprint(const std::vector<int> &values) {
    std::uint64_t result = 14695981039346656037ULL;
    for (const int value : values) {
        result ^= static_cast<std::uint32_t>(value);
        result *= 1099511628211ULL;
    }
    return result;
}

SortStats bubble_sort(std::vector<int> &values) {
    SortStats stats;
    if (values.size() < 2) {
        return stats;
    }
    for (std::size_t end = values.size() - 1; end > 0; --end) {
        bool swapped = false;
        ++stats.passes;
        for (std::size_t i = 0; i < end; ++i) {
            ++stats.comparisons;
            if (values[i] > values[i + 1]) {
                std::swap(values[i], values[i + 1]);
                ++stats.swaps;
                swapped = true;
            }
        }
        if (!swapped) {
            break;
        }
    }
    return stats;
}

void emit_row(std::size_t size, InputOrder order, std::string_view algo, std::uint64_t comparisons, std::uint64_t swaps,
              std::uint64_t passes, std::uint64_t source_fingerprint, bool correct) {
    std::cout << size << ';' << seed << ';' << order_name(order) << ';' << algo << ';' << comparisons << ';' << swaps
              << ';' << passes << ';' << source_fingerprint << ';' << std::boolalpha << correct << '\n';
}

int main() {
    std::cout << "study=std_sort_comparisons\n"
              << "engine=std::mt19937\n"
              << "value_mapping=engine_output_modulo_10000\n"
              << "seed=" << seed << '\n'
              << "algos=bubble,std_sort\n"
              << "size;seed;order;algo;comparisons;swaps;passes;fingerprint;"
                 "correct\n";

    bool all_correct = true;
    for (const std::size_t size : sizes) {
        for (const InputOrder order : input_orders) {
            const std::vector<int> source = make_data(size, order, seed);
            const std::uint64_t source_fingerprint = fingerprint(source);

            std::vector<int> expected = source;
            std::sort(expected.begin(), expected.end());

            std::vector<int> bubble_data = source;
            const SortStats bubble_stats = bubble_sort(bubble_data);
            const bool bubble_ok = bubble_data == expected;
            all_correct = all_correct && bubble_ok;
            emit_row(size, order, "bubble", bubble_stats.comparisons, bubble_stats.swaps, bubble_stats.passes,
                     source_fingerprint, bubble_ok);

            std::vector<int> std_data = source;
            std::uint64_t std_comparisons = 0;
            std::sort(std_data.begin(), std_data.end(), CountingLess{ &std_comparisons });
            const bool std_ok = std_data == expected;
            all_correct = all_correct && std_ok;
            emit_row(size, order, "std_sort", std_comparisons, 0, 0, source_fingerprint, std_ok);
        }
    }

    std::cout << "all_correct=" << std::boolalpha << all_correct << '\n';
    return all_correct ? 0 : 1;
}
