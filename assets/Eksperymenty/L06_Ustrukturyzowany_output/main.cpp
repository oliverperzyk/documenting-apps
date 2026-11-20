#include <algorithm>
#include <chrono>
#include <cstdint>
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

enum class FaultMode { none, invalid_number, missing_field, duplicate_row, failed_test, wrong_version };

FaultMode parse_fault_mode(int argc, char *argv[]) {
    // Tryby awarii celowo wytwarzają konkretne błędy danych. Dzięki nim sprawdzamy
    // każdą ścieżkę odrzucenia parsera bez przypadkowego uszkadzania programu.
    if (argc == 1) {
        return FaultMode::none;
    }

    if (argc != 3 || std::string(argv[1]) != "--fault") {
        throw std::invalid_argument("usage: program [--fault MODE]");
    }

    const std::string mode = argv[2];

    if (mode == "invalid-number") {
        return FaultMode::invalid_number;
    }
    if (mode == "missing-field") {
        return FaultMode::missing_field;
    }
    if (mode == "duplicate-row") {
        return FaultMode::duplicate_row;
    }
    if (mode == "failed-test") {
        return FaultMode::failed_test;
    }
    if (mode == "wrong-version") {
        return FaultMode::wrong_version;
    }

    throw std::invalid_argument("unknown fault mode");
}

std::vector<int> make_data(const std::string &test_case, std::size_t size, int trial) {
    std::vector<int> values(size);

    for (std::size_t i = 0; i < size; ++i) {
        values[i] = static_cast<int>(i);
    }

    if (test_case == "reversed") {
        std::reverse(values.begin(), values.end());
    } else if (test_case == "random") {
        // Osobny generator z zapisanym ziarnem odtwarza dane danej próby niezależnie
        // od kolejności uruchomień, więc wynik można później powtórzyć.
        const std::uint32_t seed =
            20260600U + static_cast<std::uint32_t>(size * 10) + static_cast<std::uint32_t>(trial);
        std::mt19937 generator(seed);
        std::shuffle(values.begin(), values.end(), generator);
    }

    return values;
}

std::uint64_t bubble_sort(std::vector<int> &values) {
    std::uint64_t comparisons = 0;

    for (std::size_t pass = 0; pass + 1 < values.size(); ++pass) {
        bool swapped = false;

        for (std::size_t i = 0; i + 1 < values.size() - pass; ++i) {
            ++comparisons;

            if (values[i] > values[i + 1]) {
                std::swap(values[i], values[i + 1]);
                swapped = true;
            }
        }

        if (!swapped) {
            // Brak zamiany oznacza, że dane są już uporządkowane i dalsze przebiegi
            // nie zmienią wyniku.
            break;
        }
    }

    return comparisons;
}

SortResult run_trial(const std::string &test_case, std::size_t size, int trial) {
    std::vector<int> values = make_data(test_case, size, trial);
    std::vector<int> expected = values;
    std::sort(expected.begin(), expected.end());

    // Mierzymy wyłącznie sortowanie. Przygotowanie danych i wyniku wzorcowego
    // pozostaje poza przedziałem, aby nie zawyżać czasu badanej operacji.
    const auto start = std::chrono::steady_clock::now();
    const std::uint64_t comparisons = bubble_sort(values);
    const auto stop = std::chrono::steady_clock::now();

    const long long time_us = std::chrono::duration_cast<std::chrono::microseconds>(stop - start).count();

    return SortResult{ test_case, size, trial, time_us, comparisons, values == expected };
}

void emit_row(const SortResult &result, FaultMode fault_mode, bool first_row) {
    // Psujemy tylko pierwszy rekord, aby każda próba sprawdzała jedną regułę
    // walidacji i było wiadomo, która nieprawidłowość wywołała reakcję parsera.
    if (first_row && fault_mode == FaultMode::invalid_number) {
        std::cout << result.test_case << ";many;" << result.trial << ';' << result.time_us << ';' << result.comparisons
                  << ';' << std::boolalpha << result.correct << '\n';
        return;
    }

    std::cout << result.test_case << ';' << result.size << ';' << result.trial << ';' << result.time_us << ';'
              << result.comparisons;

    if (!(first_row && fault_mode == FaultMode::missing_field)) {
        std::cout << ';' << std::boolalpha << result.correct;
    }

    std::cout << '\n';
}

int main(int argc, char *argv[]) {
    FaultMode fault_mode = FaultMode::none;

    try {
        fault_mode = parse_fault_mode(argc, argv);
    } catch (const std::invalid_argument &error) {
        std::cerr << "ERROR: " << error.what() << '\n';
        return 2;
    }

    std::vector<SortResult> results;
    const std::vector<std::string> test_cases{ "sorted", "reversed", "random" };
    const std::vector<std::size_t> sizes{ 16, 32 };

    for (const std::string &test_case : test_cases) {
        for (const std::size_t size : sizes) {
            for (int trial = 1; trial <= 3; ++trial) {
                results.push_back(run_trial(test_case, size, trial));
            }
        }
    }

    if (fault_mode == FaultMode::failed_test) {
        // Rekord zachowuje poprawny format, ale opisuje nieudany test. Sprawdzamy w ten
        // sposób, czy parser odróżnia poprawność danych od wyniku samego testu.
        results.front().correct = false;
    }

    // Nazwa protokołu i wersja mówią parserowi, jak rozumieć pola. Bez nich nowy
    // format mógłby zostać cicho odczytany według starych, błędnych zasad.
    std::cout << "TIDPI_RESULTS;" << (fault_mode == FaultMode::wrong_version ? "99" : "1") << '\n'
              << "case;size;trial;time_us;comparisons;correct\n";

    for (std::size_t i = 0; i < results.size(); ++i) {
        emit_row(results[i], fault_mode, i == 0);
    }

    if (fault_mode == FaultMode::duplicate_row) {
        // Powtarzamy rekord o tym samym przypadku, rozmiarze i numerze próby. Te trzy
        // pola razem identyfikują pomiar, więc parser powinien wykryć duplikat.
        emit_row(results.back(), FaultMode::none, false);
    }

    // Poprawny format nie oznacza zaliczonego testu. Kod wyjścia 1 informuje
    // automatyzację, że dane są czytelne, ale co najmniej jeden test nie przeszedł.
    return fault_mode == FaultMode::failed_test ? 1 : 0;
}
