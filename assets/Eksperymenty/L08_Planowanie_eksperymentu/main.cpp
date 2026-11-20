#include <chrono>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

std::vector<std::int64_t> make_data(std::size_t size) {
    std::vector<std::int64_t> values(size);
    for (std::size_t index = 0; index < size; ++index) {
        values[index] = static_cast<std::int64_t>(index % 101);
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

void run_trial(const std::string &plan, const std::string &variant, int trial, std::size_t size, int rounds) {
    // Rozmiar zapisujemy w każdym rekordzie, aby dało się wykryć, czy wraz
    // z wariantem nie zmieniła się także ilość wykonywanej pracy.
    const std::vector<std::int64_t> values = make_data(size);
    const auto start = std::chrono::steady_clock::now();
    const std::int64_t checksum = calculate_checksum(values, rounds);
    const auto stop = std::chrono::steady_clock::now();
    const auto time_ns = std::chrono::duration_cast<std::chrono::nanoseconds>(stop - start).count();

    std::cout << plan << ';' << variant << ';' << trial << ';' << size << ';' << rounds << ';' << time_ns << ';'
              << checksum << '\n';
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        std::cerr << "usage: L08_Planowanie_eksperymentu.exe fair|confounded\n";
        return 2;
    }

    const std::string plan = argv[1];
    if (plan != "fair" && plan != "confounded") {
        std::cerr << "ERROR: plan must be fair or confounded\n";
        return 2;
    }

    constexpr std::size_t base_size = 100'000;
    constexpr int rounds = 100;
    constexpr int trials = 6;
    std::cout << "plan;variant;trial;data_size;rounds;time_ns;checksum\n";

    for (int trial = 1; trial <= trials; ++trial) {
        // W planie confounded celowo dajemy B mniej danych. To nie jest
        // optymalizacja, lecz zmienna zakłócająca przygotowana do wykrycia na lekcji.
        const std::size_t size_b = plan == "fair" ? base_size : base_size / 4;

        // Zmieniamy kolejność A/B, aby żaden wariant nie był zawsze pierwszy.
        if (trial % 2 == 1) {
            run_trial(plan, "A", trial, base_size, rounds);
            run_trial(plan, "B", trial, size_b, rounds);
        } else {
            run_trial(plan, "B", trial, size_b, rounds);
            run_trial(plan, "A", trial, base_size, rounds);
        }
    }
    return 0;
}
