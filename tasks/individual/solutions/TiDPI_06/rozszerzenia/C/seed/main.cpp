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
    std::uint32_t seed;
};

constexpr const char *header = "case;size;trial;time_us;comparisons;correct;seed\n";

enum class FaultMode { none, invalid_number, missing_field, duplicate_row, wrong_version, failed_test, invalid_seed };

FaultMode parse_fault_mode(int argc, char *argv[]) {
    if (argc == 1) {
        return FaultMode::none;
    }
    if (argc == 3 && std::string(argv[1]) == "--fault") {
        const std::string mode = argv[2];
        if (mode == "invalid-seed")
            return FaultMode::invalid_seed;
        if (mode == "invalid-number")
            return FaultMode::invalid_number;
        if (mode == "missing-field")
            return FaultMode::missing_field;
        if (mode == "duplicate-row")
            return FaultMode::duplicate_row;
        if (mode == "wrong-version")
            return FaultMode::wrong_version;
        if (mode == "failed-test")
            return FaultMode::failed_test;
        throw std::invalid_argument("unknown fault mode: " + mode);
    }
    throw std::invalid_argument("usage: tidpi06 [--clock-info | --fault MODE]");
}

std::uint32_t seed_for(const std::string &test_case, std::size_t size, int trial) {
    // Zero oznacza brak generatora dla ukladow deterministycznych.
    return test_case == "random" ? 20260600U + static_cast<std::uint32_t>(size * 10) + static_cast<std::uint32_t>(trial)
                                 : 0U;
}

std::vector<int> make_data(const std::string &test_case, std::size_t size, std::uint32_t seed) {
    std::vector<int> values(size);
    for (std::size_t i = 0; i < size; ++i) {
        values[i] = static_cast<int>(i);
    }
    if (test_case == "reversed") {
        std::reverse(values.begin(), values.end());
    } else if (test_case == "random") {
        std::mt19937 generator(seed);
        std::shuffle(values.begin(), values.end(), generator);
    }
    return values;
}

std::uint64_t bubble_sort(std::vector<int> &values) {
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

SortResult run_trial(const std::string &test_case, std::size_t size, int trial) {
    const auto seed = seed_for(test_case, size, trial);
    auto values = make_data(test_case, size, seed);
    auto expected = values;
    std::sort(expected.begin(), expected.end());

    // Stoper obejmuje sortowanie i licznik; wzorzec i kontrola są poza nim.
    const auto start = std::chrono::steady_clock::now();
    const auto comparisons = bubble_sort(values);
    const auto stop = std::chrono::steady_clock::now();
    const auto elapsed = std::chrono::duration_cast<std::chrono::microseconds>(stop - start).count();
    return { test_case, size, trial, elapsed, comparisons, values == expected, seed };
}

void emit_row(std::ostream &output, const SortResult &row, FaultMode fault = FaultMode::none) {
    output << std::boolalpha << row.test_case << ';';
    if (fault == FaultMode::invalid_number) {
        output << "many";
    } else {
        output << row.size;
    }
    output << ';' << row.trial << ';' << row.time_us << ';' << row.comparisons;
    if (fault != FaultMode::missing_field) {
        output << ';' << (fault == FaultMode::failed_test ? false : row.correct);
    }
    output << ';' << (fault == FaultMode::invalid_seed ? std::string("-1") : std::to_string(row.seed));
    output << '\n';
}

void emit_rows(std::ostream &output, const std::vector<SortResult> &results, FaultMode fault = FaultMode::none) {
    output << header << std::boolalpha;
    // V2 zawiera tylko liczby i zamknięte słowniki bez separatorów/cudzysłowów.
    for (std::size_t i = 0; i < results.size(); ++i) {
        // Awaria dotyczy emisji pierwszego rekordu, nie badanego sortowania.
        emit_row(output, results[i], i == 0 ? fault : FaultMode::none);
    }
    if (fault == FaultMode::duplicate_row) {
        emit_row(output, results.back());
    }
}

void write_csv(const std::vector<SortResult> &results) {
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

int main(int argc, char *argv[]) {
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
    try {
        const auto fault = parse_fault_mode(argc, argv);
        std::vector<SortResult> results;
        const std::vector<std::string> cases = { "sorted", "reversed", "random" };
        // Rotacja porządku układów między próbami, stały rozmiar w danej grupie.
        for (const std::size_t size : { 16U, 32U }) {
            for (int trial = 1; trial <= 3; ++trial) {
                for (std::size_t position = 0; position < cases.size(); ++position) {
                    const auto index = (position + static_cast<std::size_t>(trial - 1)) % cases.size();
                    results.push_back(run_trial(cases[index], size, trial));
                }
            }
        }
        // W trybach awarii tylko parser może opublikować wynikowy CSV.
        if (fault == FaultMode::none) {
            write_csv(results);
        }
        std::cout << "TIDPI_RESULTS;" << (fault == FaultMode::wrong_version ? "99" : "2") << '\n';
        emit_rows(std::cout, results, fault);
        std::cout.flush();
        if (!std::cout) {
            throw std::runtime_error("cannot write raw output to stdout");
        }
        if (fault == FaultMode::failed_test) {
            return 1;
        }
        return std::all_of(results.begin(), results.end(), [](const SortResult &row) { return row.correct; }) ? 0 : 1;
    } catch (const std::exception &error) {
        std::cerr << "ERROR: " << error.what() << '\n';
        return 2;
    }
}
