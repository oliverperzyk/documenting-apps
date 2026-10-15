#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <random>
#include <string_view>
#include <vector>

// Badanie C2: Bubble Sort z early-exit vs bez early-exit.
// Identyczne wejście (ten sam fingerprint) dla obu wariantów.
constexpr std::array<std::size_t, 4> sizes = { 500, 1000, 2000, 4000 };
constexpr std::uint32_t seed = 20260401;
constexpr int trial_count = 1;

enum class InputOrder { Sorted, Reversed, Pseudorandom };

constexpr std::array<InputOrder, 3> input_orders = { InputOrder::Sorted, InputOrder::Reversed,
                                                     InputOrder::Pseudorandom };

struct SortStats {
    std::uint64_t comparisons = 0;
    std::uint64_t swaps = 0;
    std::uint64_t passes = 0;
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

SortStats bubble_sort_early(std::vector<int> &values) {
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

SortStats bubble_sort_full(std::vector<int> &values) {
    SortStats stats;
    if (values.size() < 2) {
        return stats;
    }
    // Wariant bez early-exit: zawsze pełna seria przebiegów.
    for (std::size_t end = values.size() - 1; end > 0; --end) {
        ++stats.passes;
        for (std::size_t i = 0; i < end; ++i) {
            ++stats.comparisons;
            if (values[i] > values[i + 1]) {
                std::swap(values[i], values[i + 1]);
                ++stats.swaps;
            }
        }
    }
    return stats;
}

int main() {
    std::cout << "study=bez_early_exit\n"
              << "engine=std::mt19937\n"
              << "value_mapping=engine_output_modulo_10000\n"
              << "seed=" << seed << '\n'
              << "variants=early,full\n"
              << "size;seed;order;variant;trial;time_us;comparisons;swaps;passes;"
                 "fingerprint;correct\n";
    bool all_correct = true;
    for (const std::size_t size : sizes) {
        for (const InputOrder order : input_orders) {
            for (int trial = 1; trial <= trial_count; ++trial) {
                const std::vector<int> source = make_data(size, order, seed);
                const std::uint64_t source_fingerprint = fingerprint(source);
                std::vector<int> expected = source;
                std::sort(expected.begin(), expected.end());

                for (const char *variant : { "early", "full" }) {
                    std::vector<int> result = source;
                    const auto start = std::chrono::steady_clock::now();
                    const SortStats stats = (variant[0] == 'e') ? bubble_sort_early(result) : bubble_sort_full(result);
                    const auto stop = std::chrono::steady_clock::now();
                    const long long elapsed =
                        std::chrono::duration_cast<std::chrono::microseconds>(stop - start).count();
                    const bool correct = result == expected;
                    all_correct = all_correct && correct;
                    std::cout << size << ';' << seed << ';' << order_name(order) << ';' << variant << ';' << trial
                              << ';' << elapsed << ';' << stats.comparisons << ';' << stats.swaps << ';' << stats.passes
                              << ';' << source_fingerprint << ';' << std::boolalpha << correct << '\n';
                }
            }
        }
    }
    std::cout << "all_correct=" << std::boolalpha << all_correct << '\n';
    return all_correct ? 0 : 1;
}
