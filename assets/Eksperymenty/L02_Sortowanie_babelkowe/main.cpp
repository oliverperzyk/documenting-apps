#include <algorithm>
#include <chrono>
#include <cstdint>
#include <iomanip>
#include <iostream>
#include <random>
#include <string>
#include <vector>

const char *build_configuration() {
#ifdef _DEBUG
    return "Debug";
#else
    return "Release or another configuration without _DEBUG";
#endif
}

void bubble_sort_indexed(std::vector<int> &values) {
    // Dla pustego wektora nie ma czego sortować. Sprawdzamy rozmiar przed
    // obliczeniem size - 1, ponieważ std::size_t jest typem bez znaku i 0 - 1
    // dałoby bardzo dużą liczbę zamiast wartości ujemnej.
    if (values.size() < 2) {
        return;
    }

    for (std::size_t end = values.size() - 1; end > 0; --end) {
        bool swapped = false;

        for (std::size_t i = 0; i < end; ++i) {
            if (values[i] > values[i + 1]) {
                std::swap(values[i], values[i + 1]);
                swapped = true;
            }
        }

        if (!swapped) {
            // Jeżeli w całym przebiegu niczego nie zamieniliśmy, dane są już
            // uporządkowane i kolejne przebiegi nie zmienią wyniku.
            break;
        }
    }
}

void bubble_sort_pointers(int *data, std::size_t size) {
    // Surowy wskaźnik może mieć wartość nullptr i nie wskazywać żadnej tablicy.
    // Sprawdzamy go przed użyciem operatora *, bo odczyt przez nullptr prowadzi
    // do niezdefiniowanego zachowania.
    if (data == nullptr || size < 2) {
        return;
    }

    for (int *last = data + size - 1; last > data; --last) {
        bool swapped = false;

        for (int *current = data; current < last; ++current) {
            int *next = current + 1;

            if (*current > *next) {
                std::swap(*current, *next);
                swapped = true;
            }
        }

        if (!swapped) {
            break;
        }
    }
}

std::vector<int> make_random_data(std::size_t size, std::uint32_t seed) {
    // Zapisane ziarno inicjuje generator zawsze w tym samym stanie, dzięki czemu
    // odtwarzamy dane i uczciwie podajemy je obu implementacjom.
    std::mt19937 generator(seed);
    std::uniform_int_distribution<int> distribution(-1'000'000, 1'000'000);
    std::vector<int> values(size);

    for (int &value : values) {
        value = distribution(generator);
    }

    return values;
}

template <typename Operation> long long measure_microseconds(Operation operation) {
    // Mierzymy czas trwania, a nie godzinę. steady_clock jest monotoniczny,
    // więc korekta zegara systemowego nie cofnie wyniku pomiaru.
    const auto start = std::chrono::steady_clock::now();
    operation();
    const auto stop = std::chrono::steady_clock::now();

    return std::chrono::duration_cast<std::chrono::microseconds>(stop - start).count();
}

struct TrialResult {
    std::size_t size;
    int trial;
    long long indexed_microseconds;
    long long pointers_microseconds;
    bool indexed_correct;
    bool pointers_correct;
};

TrialResult run_trial(std::size_t size, int trial, std::uint32_t seed) {
    const std::vector<int> source = make_random_data(size, seed);
    // Obie wersje dostają identyczne, lecz osobne kopie. Sortowanie zmienia
    // wektor, więc druga wersja nie może dostać danych już posortowanych przez pierwszą.
    std::vector<int> indexed_result = source;
    std::vector<int> pointers_result = source;
    std::vector<int> expected = source;
    // Wynik wzorcowy tworzymy poza pomiarem, aby czasu std::sort nie doliczyć
    // do czasu badanych implementacji.
    std::sort(expected.begin(), expected.end());

    long long indexed_time = 0;
    long long pointers_time = 0;

    if (trial % 2 == 1) {
        // Zamieniamy kolejność, aby jedna wersja nie korzystała zawsze z efektu
        // rozgrzania procesora i pamięci podręcznej jako uruchamiana druga.
        indexed_time = measure_microseconds([&indexed_result]() { bubble_sort_indexed(indexed_result); });

        pointers_time = measure_microseconds(
            [&pointers_result]() { bubble_sort_pointers(pointers_result.data(), pointers_result.size()); });
    } else {
        pointers_time = measure_microseconds(
            [&pointers_result]() { bubble_sort_pointers(pointers_result.data(), pointers_result.size()); });

        indexed_time = measure_microseconds([&indexed_result]() { bubble_sort_indexed(indexed_result); });
    }

    return TrialResult{
        size, trial, indexed_time, pointers_time, indexed_result == expected, pointers_result == expected
    };
}

void print_sample_addresses(const std::vector<int> &values) {
    std::cout << "Sample addresses:\n";
    const std::size_t limit = std::min<std::size_t>(values.size(), 5);

    for (std::size_t i = 0; i < limit; ++i) {
        std::cout << "&values[" << i
                  << "] = "
                  // Wypisujemy adres, aby pokazać kolejne położenie elementów w pamięci.
                  // &values[i] ma typ const char*, który std::cout traktuje jak początek
                  // napisu w stylu C. Rzutowanie na const void* wymusza wypisanie adresu.
                  << static_cast<const void *>(&values[i]) << ", value = " << values[i] << '\n';
    }
}

int main() {
    const std::vector<std::size_t> sizes = { 1000, 2000, 4000 };
    constexpr int trials = 5;
    constexpr std::uint32_t base_seed = 20260201;

    std::cout << "Build: " << build_configuration() << "\n\n";

    const std::vector<int> address_sample = make_random_data(5, base_seed);
    print_sample_addresses(address_sample);

    std::cout << "\nsize;trial;indexed_us;pointers_us;indexed_ok;pointers_ok\n";

    bool all_results_correct = true;

    for (const std::size_t size : sizes) {
        for (int trial = 1; trial <= trials; ++trial) {
            const TrialResult result = run_trial(size, trial,
                                                 // Jedna próba ma jeden zestaw danych, bo porównanie czasów ma sens
                                                 // tylko wtedy, gdy obie implementacje rozwiązują to samo zadanie.
                                                 base_seed + static_cast<std::uint32_t>(trial));

            all_results_correct = all_results_correct && result.indexed_correct && result.pointers_correct;

            std::cout << result.size << ';' << result.trial << ';' << result.indexed_microseconds << ';'
                      << result.pointers_microseconds << ';' << std::boolalpha << result.indexed_correct << ';'
                      << std::boolalpha << result.pointers_correct << '\n';
        }
    }

    std::cout << "\nAll results correct: " << std::boolalpha << all_results_correct << '\n';

    if (!all_results_correct) {
        // Szybki, ale błędny algorytm nie daje wartościowego wyniku. Odrzucamy
        // pomiary, jeżeli choć jedna implementacja zwróciła zły rezultat.
        std::cerr << "At least one implementation returned an incorrect result.\n";
        return 1;
    }

    return 0;
}
