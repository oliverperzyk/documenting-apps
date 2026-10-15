#include "ownership_ops.hpp"

#include <chrono>
#include <cstdint>
#include <iostream>
#include <memory>
#include <vector>

// Poziom D: raw new[] vs unique_ptr vs vector.
// Faza 1 = tylko alokacja+zwolnienie; Faza 2 = tylko process_data.
constexpr std::size_t element_count = 50'000;
constexpr std::uint32_t rounds = 100;
constexpr int trial_count = 6;
constexpr int alloc_repetitions = 1000;
constexpr int alloc_series_count = 6;

template <typename Operation>
long long measure_microseconds(Operation operation) {
  const auto start = std::chrono::steady_clock::now();
  operation();
  const auto stop = std::chrono::steady_clock::now();
  return std::chrono::duration_cast<std::chrono::microseconds>(stop - start)
      .count();
}

void prepare_data(std::uint32_t *data, std::size_t size) {
  for (std::size_t i = 0; i < size; ++i) {
    data[i] = static_cast<std::uint32_t>(i % 1000);
  }
}

void process_data(std::uint32_t *data, std::size_t size) {
  for (std::uint32_t round = 0; round < rounds; ++round) {
    for (std::size_t i = 0; i < size; ++i) {
      ++data[i];
    }
  }
}

bool verify_processed_data(const std::uint32_t *data, std::size_t size) {
  if (data == nullptr || size == 0) {
    return false;
  }
  for (std::size_t i = 0; i < size; ++i) {
    const std::uint32_t expected =
        static_cast<std::uint32_t>(i % 1000) + rounds;
    if (data[i] != expected) {
      return false;
    }
  }
  return true;
}

bool smoke_check() {
  {
    std::uint32_t *raw = new std::uint32_t[element_count];
    raw[0] = 1;
    raw[element_count - 1] = 2;
    const bool ok = raw[0] == 1 && raw[element_count - 1] == 2;
    delete[] raw;
    if (!ok) {
      return false;
    }
  }
  {
    auto up = std::make_unique<std::uint32_t[]>(element_count);
    up[0] = 3;
    up[element_count - 1] = 4;
    if (up[0] != 3 || up[element_count - 1] != 4) {
      return false;
    }
  }
  {
    std::vector<std::uint32_t> v(element_count);
    v[0] = 5;
    v[element_count - 1] = 6;
    if (v[0] != 5 || v[element_count - 1] != 6) {
      return false;
    }
  }
  return true;
}

struct SeriesStats {
  long long min_total = 0;
  long long max_total = 0;
  long long sum_total = 0;
};

void update_stats(SeriesStats &stats, long long total, int series_index) {
  if (series_index == 1) {
    stats.min_total = stats.max_total = total;
  } else {
    if (total < stats.min_total) {
      stats.min_total = total;
    }
    if (total > stats.max_total) {
      stats.max_total = total;
    }
  }
  stats.sum_total += total;
}

void print_stats(const char *label, const SeriesStats &stats) {
  const double mean_total =
      static_cast<double>(stats.sum_total) / alloc_series_count;
  const double mean_one = mean_total / alloc_repetitions;
  std::cout << label << "_min_total_us=" << stats.min_total << '\n'
            << label << "_max_total_us=" << stats.max_total << '\n'
            << label << "_range_total_us="
            << (stats.max_total - stats.min_total) << '\n'
            << label << "_mean_total_us=" << mean_total << '\n'
            << label << "_mean_us_per_alloc_free=" << mean_one << '\n';
}

int main() {
  const std::size_t bytes = element_count * sizeof(std::uint32_t);

  std::cout << "experiment=ownership_raw_unique_vector\n"
            << "element_count=" << element_count << '\n'
            << "bytes_per_array=" << bytes << '\n'
            << "rounds=" << rounds << '\n'
            << "alloc_repetitions_per_series=" << alloc_repetitions << '\n'
            << "alloc_series_count=" << alloc_series_count << '\n'
            << "process_trial_count=" << trial_count << '\n'
            << "phase1_timer=alloc_and_free_only\n"
            << "phase2_timer=process_data_only_after_prepare\n"
            << "note=vector_n_value_initializes_uint32_t_to_zero\n"
            << "note=optnone_on_alloc_bodies_blocks_allocation_elision\n";

  if (!smoke_check()) {
    std::cout << "smoke_ok=false\nall_ok=false\n";
    return 1;
  }
  std::cout << "smoke_ok=true\n";

  // ----- Faza 1: tylko alokacja + zwolnienie -----
  std::cout << "phase=alloc_free\n"
            << "series;raw_total_us;unique_total_us;vector_total_us;"
               "raw_mean_us;unique_mean_us;vector_mean_us\n";

  SeriesStats raw_stats{};
  SeriesStats unique_stats{};
  SeriesStats vector_stats{};

  for (int series = 1; series <= alloc_series_count; ++series) {
    const long long raw_total = measure_microseconds([]() {
      for (int i = 0; i < alloc_repetitions; ++i) {
        alloc_free_raw(element_count, static_cast<std::uint32_t>(i));
      }
    });
    const long long unique_total = measure_microseconds([]() {
      for (int i = 0; i < alloc_repetitions; ++i) {
        alloc_free_unique(element_count, static_cast<std::uint32_t>(i));
      }
    });
    const long long vector_total = measure_microseconds([]() {
      for (int i = 0; i < alloc_repetitions; ++i) {
        alloc_free_vector(element_count, static_cast<std::uint32_t>(i));
      }
    });

    update_stats(raw_stats, raw_total, series);
    update_stats(unique_stats, unique_total, series);
    update_stats(vector_stats, vector_total, series);

    std::cout << series << ';' << raw_total << ';' << unique_total << ';'
              << vector_total << ';'
              << (static_cast<double>(raw_total) / alloc_repetitions) << ';'
              << (static_cast<double>(unique_total) / alloc_repetitions) << ';'
              << (static_cast<double>(vector_total) / alloc_repetitions)
              << '\n';
  }

  print_stats("raw", raw_stats);
  print_stats("unique", unique_stats);
  print_stats("vector", vector_stats);

  // ----- Faza 2: tylko process_data -----
  std::cout << "phase=process\n"
            << "trial;raw_us;unique_us;vector_us;raw_ok;unique_ok;vector_ok\n";

  bool all_ok = true;
  for (int trial = 1; trial <= trial_count; ++trial) {
    long long raw_us = 0;
    long long unique_us = 0;
    long long vector_us = 0;
    bool raw_ok = false;
    bool unique_ok = false;
    bool vector_ok = false;

    const auto run_raw = [&]() {
      std::uint32_t *raw = new std::uint32_t[element_count];
      prepare_data(raw, element_count);
      raw_us = measure_microseconds(
          [raw]() { process_data(raw, element_count); });
      raw_ok = verify_processed_data(raw, element_count);
      delete[] raw;
    };
    const auto run_unique = [&]() {
      auto up = std::make_unique<std::uint32_t[]>(element_count);
      prepare_data(up.get(), element_count);
      unique_us = measure_microseconds(
          [&up]() { process_data(up.get(), element_count); });
      unique_ok = verify_processed_data(up.get(), element_count);
    };
    const auto run_vector = [&]() {
      std::vector<std::uint32_t> v(element_count);
      prepare_data(v.data(), element_count);
      vector_us = measure_microseconds(
          [&v]() { process_data(v.data(), element_count); });
      vector_ok = verify_processed_data(v.data(), element_count);
    };

    if (trial % 3 == 1) {
      run_raw();
      run_unique();
      run_vector();
    } else if (trial % 3 == 2) {
      run_unique();
      run_vector();
      run_raw();
    } else {
      run_vector();
      run_raw();
      run_unique();
    }

    all_ok = all_ok && raw_ok && unique_ok && vector_ok;
    std::cout << trial << ';' << raw_us << ';' << unique_us << ';' << vector_us
              << ';' << std::boolalpha << raw_ok << ';' << unique_ok << ';'
              << vector_ok << '\n';
  }

  std::cout << "ownership_sink=" << ownership_sink << '\n'
            << "all_ok=" << std::boolalpha << all_ok << '\n';
  return all_ok ? 0 : 1;
}
