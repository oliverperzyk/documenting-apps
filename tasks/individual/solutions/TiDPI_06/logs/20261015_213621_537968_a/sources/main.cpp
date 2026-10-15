#include <algorithm>
#include <chrono>
#include <cstdint>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <random>
#include <stdexcept>
#include <string>
#include <vector>

struct SortResult {
    std::string test_case;
    std::size_t size;
    int trial;
    long long time_us;
    std::uint64_t comparisons;
    bool correct;
};

constexpr const char* header = "case;size;trial;time_us;comparisons;correct\n";

std::vector<int> make_data(const std::string& test_case, std::size_t size, int trial) {
    std::vector<int> values(size);
    for (std::size_t i = 0; i < size; ++i) {
        values[i] = static_cast<int>(i);
    }
    if (test_case == "reversed") {
        std::reverse(values.begin(), values.end());
    } else if (test_case == "random") {
        const auto seed = 20260600U + static_cast<std::uint32_t>(size * 10) +
                          static_cast<std::uint32_t>(trial);
        std::mt19937 generator(seed);
        std::shuffle(values.begin(), values.end(), generator);
    }
    return values;
}

std::uint64_t bubble_sort(std::vector<int>& values) {
    std::uint64_t comparisons = 0;
    for (std::size_t end = values.size(); end > 1; --end) {
        bool swapped = false;
        for (std::size_t i = 1; i < end; ++i) {
            ++comparisons;
            if (values[i - 1] > values[i]) {
                std::swap(values[i - 1], values[i]);
                swapped = true;
            }
        }
        if (!swapped) {
            break;
        }
    }
    return comparisons;
}

SortResult run_trial(const std::string& test_case, std::size_t size, int trial) {
    auto values = make_data(test_case, size, trial);
    auto expected = values;
    std::sort(expected.begin(), expected.end());

    // Stoper obejmuje sortowanie i licznik; wzorzec i kontrola są poza nim.
    const auto start = std::chrono::steady_clock::now();
    const auto comparisons = bubble_sort(values);
    const auto stop = std::chrono::steady_clock::now();
    const auto elapsed =
        std::chrono::duration_cast<std::chrono::microseconds>(stop - start).count();
    return {test_case, size, trial, elapsed, comparisons, values == expected};
}

void emit_rows(std::ostream& output, const std::vector<SortResult>& results) {
    output << header << std::boolalpha;
    // V1 zawiera tylko liczby i zamknięte słowniki bez separatorów/cudzysłowów.
    for (const auto& row : results) {
        output << row.test_case << ';' << row.size << ';' << row.trial << ';'
               << row.time_us << ';' << row.comparisons << ';' << row.correct << '\n';
    }
}

void write_csv(const std::vector<SortResult>& results) {
    const std::filesystem::path output = "results.csv";
    const std::filesystem::path temporary = "results.csv.tmp";
    // Nie zastępuj wcześniejszego przebiegu ani nie przejmuj obcego pliku tymczasowego.
    if (std::filesystem::exists(output) || std::filesystem::exists(temporary)) {
        throw std::runtime_error("results.csv or results.csv.tmp already exists; use a fresh run directory");
    }
    bool temporary_created = false;
    try {
        std::ofstream target;
        target.exceptions(std::ios::failbit | std::ios::badbit);
        target.open(temporary, std::ios::binary);
        temporary_created = true;
        target << "\xEF\xBB\xBF";
        emit_rows(target, results);
        target.close();
        std::filesystem::rename(temporary, output);
    } catch (...) {
        if (temporary_created) {
            std::error_code ignored;
            std::filesystem::remove(temporary, ignored);
        }
        throw;
    }
}

int main(int argc, char* argv[]) {
    if (argc == 2 && std::string(argv[1]) == "--clock-info") {
        using Clock = std::chrono::steady_clock;
        std::cout << "clock=std::chrono::steady_clock\n"
                  << "is_steady=" << std::boolalpha << Clock::is_steady << '\n'
                  << "period_num=" << Clock::period::num << '\n'
                  << "period_den=" << Clock::period::den << '\n'
                  << "output_unit=microseconds (integer, truncated)\n"
                  << "effective_resolution=not_measured\n";
        return 0;
    }
    if (argc != 1) {
        std::cerr << "ERROR: usage: tidpi06 [--clock-info]\n";
        return 2;
    }
    try {
        std::vector<SortResult> results;
        const std::vector<std::string> cases = {"sorted", "reversed", "random"};
        // Rotacja porządku układów między próbami, stały rozmiar w danej grupie.
        for (const std::size_t size : {16U, 32U}) {
            for (int trial = 1; trial <= 3; ++trial) {
                for (std::size_t position = 0; position < cases.size(); ++position) {
                    const auto index = (position + static_cast<std::size_t>(trial - 1)) % cases.size();
                    results.push_back(run_trial(cases[index], size, trial));
                }
            }
        }
        write_csv(results);
        std::cout << "TIDPI_RESULTS;1\n";
        emit_rows(std::cout, results);
        std::cout.flush();
        if (!std::cout) {
            throw std::runtime_error("cannot write raw output to stdout");
        }
        return std::all_of(results.begin(), results.end(),
                           [](const SortResult& row) { return row.correct; }) ? 0 : 1;
    } catch (const std::exception& error) {
        std::cerr << "ERROR: " << error.what() << '\n';
        return 2;
    }
}
