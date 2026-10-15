#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <random>
#include <string_view>
#include <vector>

constexpr std::array<std::size_t, 4> sizes = { 500, 1000, 2000, 4000 };
constexpr std::array<std::uint32_t, 2> seeds = { 20260401, 20260402 };
constexpr int trial_count = 5;

enum class InputOrder { Sorted, Reversed, Pseudorandom };

constexpr std::array<InputOrder, 3> input_orders = { InputOrder::Sorted, InputOrder::Reversed,
                                                     InputOrder::Pseudorandom };

struct SortStats {
    std::uint64_t comparisons = 0;
    std::uint64_t swaps = 0;
    std::uint64_t passes = 0;
};

struct TrialResult {
    std::size_t size;
    std::uint32_t seed;
    InputOrder order;
    int trial;
    long long microseconds;
    SortStats stats;
    std::uint64_t fingerprint;
    bool correct;
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

std::vector<int> make_data(std::size_t size, InputOrder order, std::uint32_t seed) {
    std::vector<int> values(size);
    if (order == InputOrder::Sorted) {
        std::iota(values.begin(), values.end(), 0);
    } else if (order == InputOrder::Reversed) {
        std::iota(values.begin(), values.end(), 0);
        std::reverse(values.begin(), values.end());
    } else {
        // Nowy generator uruchomiony z tym samym ziarnem odtwarza ten sam ciąg.
        // Dzięki temu eksperyment można powtórzyć i sprawdzić na tych samych
        // danych.
        std::mt19937 generator(seed);
        for (int &value : values) {
            // Operator modulo upraszcza wartości do potrzeb eksperymentu. Nie badamy
            // tutaj jakości rozkładu losowego, więc świadomie pomijamy jego
            // niewielkie odchylenia.
            value = static_cast<int>(generator() % 10'000U);
        }
    }
    return values;
}

std::uint64_t fingerprint(const std::vector<int> &values) {
    // Odcisk pozwala szybko zauważyć przypadkową zmianę danych wejściowych.
    // Nie służy do bezpieczeństwa i nie jest kryptograficzną funkcją skrótu.
    std::uint64_t result = 14695981039346656037ULL;
    for (const int value : values) {
        // Dla liczby bez znaku przepełnienie jest zdefiniowane modulo 2^64:
        // nadmiarowe bity są odrzucane. Dzięki temu obliczenie pozostaje
        // powtarzalne.
        result ^= static_cast<std::uint32_t>(value);
        result *= 1099511628211ULL;
    }
    return result;
}

SortStats bubble_sort(std::vector<int> &values) {
    SortStats stats;
    // Pustego wektora nie sortujemy. Sprawdzamy rozmiar przed size - 1, ponieważ
    // std::size_t nie ma wartości ujemnych, a 0 - 1 dałoby ogromną liczbę.
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
            // Brak zamiany oznacza, że dane są już uporządkowane. Wczesne wyjście
            // pokazuje najlepszy przypadek sortowania bąbelkowego zamiast wykonywać
            // zbędne przebiegi.
            break;
        }
    }
    return stats;
}

TrialResult run_trial(std::size_t size, std::uint32_t seed, InputOrder order, int trial) {
    const std::vector<int> source = make_data(size, order, seed);
    // Odcisk i wynik wzorcowy służą walidacji, a nie są częścią badanego
    // algorytmu. Wykonujemy je poza pomiarem, aby nie zawyżały czasu sortowania
    // bąbelkowego.
    const std::uint64_t source_fingerprint = fingerprint(source);
    std::vector<int> expected = source;
    std::vector<int> result = source;
    std::sort(expected.begin(), expected.end());
    const auto start = std::chrono::steady_clock::now();
    const SortStats stats = bubble_sort(result);
    const auto stop = std::chrono::steady_clock::now();
    const long long elapsed = std::chrono::duration_cast<std::chrono::microseconds>(stop - start).count();
    return TrialResult{ size, seed, order, trial, elapsed, stats, source_fingerprint, result == expected };
}

int main() {
    // Metadane zapisują rodzaj danych, rozmiar i ziarno, czyli przepis potrzebny
    // do odtworzenia dokładnie tego samego wejścia pseudolosowego.
    std::cout << "engine=std::mt19937\n"
              << "value_mapping=engine_output_modulo_10000\n"
              << "size;seed;order;trial;time_us;comparisons;swaps;passes;"
                 "fingerprint;correct\n";
    bool all_correct = true;
    for (const std::uint32_t seed : seeds) {
        for (const std::size_t size : sizes) {
            for (int trial = 1; trial <= trial_count; ++trial) {
                for (std::size_t position = 0; position < input_orders.size(); ++position) {
                    // Rotujemy kolejność, aby jeden rodzaj danych nie był zawsze mierzony
                    // na nierozgrzanym programie albo po wszystkich pozostałych próbach.
                    const InputOrder order =
                        input_orders[(position + static_cast<std::size_t>(trial - 1)) % input_orders.size()];
                    const TrialResult result = run_trial(size, seed, order, trial);
                    all_correct = all_correct && result.correct;
                    std::cout << result.size << ';' << result.seed << ';' << order_name(result.order) << ';'
                              << result.trial << ';' << result.microseconds << ';' << result.stats.comparisons << ';'
                              << result.stats.swaps << ';' << result.stats.passes << ';' << result.fingerprint << ';'
                              << std::boolalpha << result.correct << '\n';
                }
            }
        }
    }
    std::cout << "all_correct=" << std::boolalpha << all_correct << '\n';
    return all_correct ? 0 : 1;
}
