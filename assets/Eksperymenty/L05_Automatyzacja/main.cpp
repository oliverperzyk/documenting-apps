#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

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

int main(int argc, char *argv[]) {
    bool simulate_failure = false;

    if (argc == 2 && std::string(argv[1]) == "--simulate-failure") {
        simulate_failure = true;
    } else if (argc != 1) {
        std::cerr << "ERROR: unknown argument\n";
        return 2;
    }

    const std::vector<int> source{ 8, 3, 7, 4, 9, 2, 6, 1 };
    std::vector<int> expected = source;
    std::vector<int> result = source;

    std::sort(expected.begin(), expected.end());
    bubble_sort(result);

    if (simulate_failure) {
        // Celowo psujemy wynik, aby sprawdzić nie algorytm, lecz reakcję automatyzacji:
        // czy wykryje niepowodzenie i zachowa właściwe dowody.
        result.front() = -1;
    }

    const bool correct = result == expected;

    std::cout << "Case: " << (simulate_failure ? "simulated failure" : "normal") << '\n'
              << "Input count: " << source.size() << '\n'
              << "Result correct: " << std::boolalpha << correct << '\n';

    if (!correct) {
        std::cerr << "ERROR: result differs from the reference\n";
    }

    // Kod wyjścia 0 oznacza sukces, a inna wartość błąd. Dzięki temu skrypt może
    // podjąć decyzję bez zgadywania znaczenia tekstu przeznaczonego dla człowieka.
    return correct ? 0 : 1;
}
