#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <iostream>
#include <random>
#include <vector>

// Badanie C1: wiele seedów — tylko układ pseudorandom.
// Trzy nowe seedy względem bazy: 20260403, 20260404, 20260405.
constexpr std::array<std::size_t, 4> sizes = {500, 1000, 2000, 4000};
constexpr std::array<std::uint32_t, 5> seeds = {20260401, 20260402, 20260403,
                                                20260404, 20260405};
constexpr int trial_count = 1;

struct SortStats {
  std::uint64_t comparisons = 0;
  std::uint64_t swaps = 0;
  std::uint64_t passes = 0;
};

std::vector<int> make_pseudorandom(std::size_t size, std::uint32_t seed) {
  std::vector<int> values(size);
  std::mt19937 generator(seed);
  for (int &value : values) {
    value = static_cast<int>(generator() % 10'000U);
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

int main() {
  std::cout << "study=wiele_seedow\n"
            << "engine=std::mt19937\n"
            << "value_mapping=engine_output_modulo_10000\n"
            << "order=pseudorandom\n"
            << "new_seeds=20260403,20260404,20260405\n"
            << "size;seed;order;trial;time_us;comparisons;swaps;passes;"
               "fingerprint;correct\n";
  bool all_correct = true;
  for (const std::uint32_t seed : seeds) {
    for (const std::size_t size : sizes) {
      for (int trial = 1; trial <= trial_count; ++trial) {
        const std::vector<int> source = make_pseudorandom(size, seed);
        const std::uint64_t source_fingerprint = fingerprint(source);
        std::vector<int> expected = source;
        std::vector<int> result = source;
        std::sort(expected.begin(), expected.end());
        const auto start = std::chrono::steady_clock::now();
        const SortStats stats = bubble_sort(result);
        const auto stop = std::chrono::steady_clock::now();
        const long long elapsed =
            std::chrono::duration_cast<std::chrono::microseconds>(stop - start)
                .count();
        const bool correct = result == expected;
        all_correct = all_correct && correct;
        std::cout << size << ';' << seed << ";pseudorandom;" << trial << ';'
                  << elapsed << ';' << stats.comparisons << ';' << stats.swaps
                  << ';' << stats.passes << ';' << source_fingerprint << ';'
                  << std::boolalpha << correct << '\n';
      }
    }
  }
  std::cout << "all_correct=" << std::boolalpha << all_correct << '\n';
  return all_correct ? 0 : 1;
}
