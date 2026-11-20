#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

std::vector<std::int64_t> load_data(const std::string &path) {
    std::ifstream input(path);
    if (!input) {
        throw std::runtime_error("cannot open input file: " + path);
    }

    std::vector<std::int64_t> values;
    std::int64_t value = 0;
    while (input >> value) {
        values.push_back(value);
    }

    if (!input.eof()) {
        throw std::runtime_error("input contains a value that is not an integer");
    }
    if (values.empty()) {
        throw std::runtime_error("input file is empty");
    }
    return values;
}

std::int64_t calculate_checksum(const std::vector<std::int64_t> &values, int rounds) {
    std::int64_t checksum = 0;
    for (int round = 0; round < rounds; ++round) {
        for (const std::int64_t value : values) {
            checksum += value * value;
        }
    }
    return checksum;
}

int main(int argc, char *argv[]) {
    if (argc != 5) {
        std::cerr << "usage: benchmark.exe DATA_FILE ROUNDS WARMUP REPEAT\n";
        return 2;
    }

    try {
        const std::vector<std::int64_t> values = load_data(argv[1]);
        const int rounds = std::stoi(argv[2]);
        const int warmup = std::stoi(argv[3]);
        const int repeat = std::stoi(argv[4]);
        if (rounds < 1 || warmup < 0 || repeat < 1) {
            throw std::invalid_argument("ROUNDS and REPEAT must be positive; WARMUP cannot be negative");
        }

        const std::int64_t expected = calculate_checksum(values, 1) * rounds;

        // Rozgrzewka nie trafia do wyników. Jej celem jest ograniczenie przewagi
        // pierwszej próby, która może płacić za zimne dane i inicjalizację programu.
        for (int trial = 0; trial < warmup; ++trial) {
            if (calculate_checksum(values, rounds) != expected) {
                throw std::runtime_error("warmup returned an incorrect checksum");
            }
        }

        std::cout << "language;trial;time_ns;checksum;correct\n";
        for (int trial = 1; trial <= repeat; ++trial) {
            // Mierzymy wyłącznie badaną pętlę. Wczytanie pliku wykonaliśmy wcześniej,
            // bo szybkość dysku nie jest przedmiotem tego benchmarku.
            const auto start = std::chrono::steady_clock::now();
            const std::int64_t checksum = calculate_checksum(values, rounds);
            const auto stop = std::chrono::steady_clock::now();
            const auto time_ns = std::chrono::duration_cast<std::chrono::nanoseconds>(stop - start).count();
            const bool correct = checksum == expected;

            // Wypisany checksum sprawia, że wynik obliczenia jest obserwowalny.
            // Kompilator nie może więc bezpiecznie usunąć całej badanej pracy jako zbędnej.
            std::cout << "cpp;" << trial << ';' << time_ns << ';' << checksum << ';' << std::boolalpha << correct
                      << '\n';
            if (!correct) {
                return 1;
            }
        }
    } catch (const std::exception &error) {
        std::cerr << "ERROR: " << error.what() << '\n';
        return 2;
    }
    return 0;
}
