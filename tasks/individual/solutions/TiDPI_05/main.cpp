#include <algorithm>
#include <cstdlib>
#include <iostream>
#include <string>
#include <vector>

namespace {
constexpr int kSizeMin = 1;
constexpr int kSizeMax = 10000;
} // namespace

void bubble_sort(std::vector<int> &values) {
    for (std::size_t pass = 0; pass + 1 < values.size(); ++pass) {
        bool swapped = false;
        for (std::size_t i = 0; i + 1 < values.size() - pass; ++i) {
            if (values[i] > values[i + 1]) {
                std::swap(values[i], values[i + 1]);
                swapped = true;
            }
        }
        if (!swapped) {
            // Brak zamiany w całym przebiegu oznacza, że dane są już uporządkowane,
            // więc następne przebiegi nie zmienią wyniku.
            break;
        }
    }
}

std::vector<int> make_default_source() { return { 8, 3, 7, 4, 9, 2, 6, 1 }; }

std::vector<int> make_sized_source(int size) {
    std::vector<int> values(static_cast<std::size_t>(size));
    for (int i = 0; i < size; ++i) {
        values[static_cast<std::size_t>(i)] = size - 1 - i;
    }
    return values;
}

int main(int argc, char *argv[]) {
    bool simulate_failure = false;
    bool size_given = false;
    int size_argument = 0;

    for (int i = 1; i < argc; ++i) {
        const std::string arg = argv[i];
        if (arg == "--simulate-failure") {
            simulate_failure = true;
        } else if (arg == "--size") {
            if (i + 1 >= argc) {
                std::cerr << "ERROR: --size requires an integer argument\n";
                return 2;
            }
            ++i;
            char *end = nullptr;
            const long parsed = std::strtol(argv[i], &end, 10);
            if (end == argv[i] || *end != '\0') {
                std::cerr << "ERROR: --size value is not an integer\n";
                return 2;
            }
            if (parsed < kSizeMin || parsed > kSizeMax) {
                std::cerr << "ERROR: --size out of range [" << kSizeMin << ", " << kSizeMax << "]\n";
                return 2;
            }
            size_given = true;
            size_argument = static_cast<int>(parsed);
        } else {
            std::cerr << "ERROR: unknown argument\n";
            return 2;
        }
    }

    const std::vector<int> source = size_given ? make_sized_source(size_argument) : make_default_source();
    std::vector<int> expected = source;
    std::vector<int> result = source;
    std::sort(expected.begin(), expected.end());
    bubble_sort(result);

    if (simulate_failure) {
        // Celowo psujemy wynik, aby sprawdzić nie algorytm, lecz reakcję
        // automatyzacji: czy wykryje niepowodzenie i zachowa właściwe dowody.
        result.front() = -1;
    }

    const bool correct = result == expected;
    std::cout << "Case: " << (simulate_failure ? "simulated failure" : "normal") << '\n';
    if (size_given) {
        std::cout << "Size argument: " << size_argument << '\n';
    }
    std::cout << "Input count: " << source.size() << '\n' << "Result correct: " << std::boolalpha << correct << '\n';
    if (!correct) {
        std::cerr << "ERROR: result differs from the reference\n";
    }
    // Kod wyjścia 0 oznacza sukces, a inna wartość błąd. Dzięki temu skrypt może
    // podjąć decyzję bez zgadywania znaczenia tekstu przeznaczonego dla
    // człowieka.
    return correct ? 0 : 1;
}
