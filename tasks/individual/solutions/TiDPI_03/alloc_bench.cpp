#include "alloc_ops.hpp"

#include <chrono>
#include <cstdint>
#include <iostream>
#include <memory>

// Osobny pomiar kosztu alokacji i zwolnienia. Nie zawiera process_data.
constexpr std::size_t element_count = 50'000;
constexpr int repetitions = 1000;
constexpr int series_count = 6;

template <typename Operation> long long measure_microseconds(Operation operation) {
    const auto start = std::chrono::steady_clock::now();
    operation();
    const auto stop = std::chrono::steady_clock::now();
    return std::chrono::duration_cast<std::chrono::microseconds>(stop - start).count();
}

bool smoke_check() {
    auto p = std::make_unique<std::uint32_t[]>(element_count);
    if (p == nullptr) {
        return false;
    }
    p[0] = 42;
    p[element_count - 1] = 99;
    return p[0] == 42 && p[element_count - 1] == 99;
}

int main() {
    const std::size_t bytes = element_count * sizeof(std::uint32_t);

    std::cout << "experiment=alloc_free\n"
              << "element_count=" << element_count << '\n'
              << "bytes_per_array=" << bytes << '\n'
              << "repetitions_per_series=" << repetitions << '\n'
              << "series_count=" << series_count << '\n'
              << "timer_covers=alloc_and_free_once="
                 "make_unique_uint32_array_plus_unique_ptr_destructor\n"
              << "timer_excludes=prepare_data_and_process_data\n"
              << "note=clang_optnone_on_alloc_body_blocks_allocation_elision\n";

    if (!smoke_check()) {
        std::cout << "smoke_ok=false\nall_ok=false\n";
        return 1;
    }
    std::cout << "smoke_ok=true\n"
              << "series;total_us;mean_us_per_alloc_free\n";

    long long min_total = 0;
    long long max_total = 0;
    long long sum_total = 0;

    for (int series = 1; series <= series_count; ++series) {
        const long long total_us = measure_microseconds([]() {
            for (int i = 0; i < repetitions; ++i) {
                alloc_and_free_once(element_count, static_cast<std::uint32_t>(i));
            }
        });
        const double mean = static_cast<double>(total_us) / repetitions;
        std::cout << series << ';' << total_us << ';' << mean << '\n';

        if (series == 1) {
            min_total = max_total = total_us;
        } else {
            if (total_us < min_total) {
                min_total = total_us;
            }
            if (total_us > max_total) {
                max_total = total_us;
            }
        }
        sum_total += total_us;
    }

    std::cout << "min_total_us=" << min_total << '\n'
              << "max_total_us=" << max_total << '\n'
              << "range_total_us=" << (max_total - min_total) << '\n'
              << "mean_total_us=" << (static_cast<double>(sum_total) / series_count) << '\n'
              << "mean_us_per_alloc_free=" << (static_cast<double>(sum_total) / series_count / repetitions) << '\n'
              << "alloc_sink=" << alloc_sink << '\n'
              << "all_ok=true\n";
    return 0;
}
