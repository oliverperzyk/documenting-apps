#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <iostream>
#include <memory>

constexpr std::size_t element_count = 50'000;
constexpr std::uint32_t rounds = 100;
constexpr int trial_count = 6;

using FixedArray = std::array<std::uint32_t, element_count>;

// Tablica globalna pozwala porównać ten sam typ danych przechowywany w innym
// obszarze pamięci i istniejący przez cały czas działania programu.
FixedArray global_values{};

template <typename Operation> long long measure_microseconds(Operation operation) {
    // Interesuje nas czas trwania operacji, nie godzina. steady_clock jest
    // monotoniczny, więc zmiana zegara systemowego nie zafałszuje pomiaru.
    const auto start = std::chrono::steady_clock::now();
    operation();
    const auto stop = std::chrono::steady_clock::now();
    return std::chrono::duration_cast<std::chrono::microseconds>(stop - start).count();
}

void prepare_data(std::uint32_t *data, std::size_t size) {
    // Każdy wariant pamięci dostaje ten sam prosty wzorzec. Dzięki temu różnice
    // wynikają ze sposobu przechowywania, a poprawność łatwo sprawdzić.
    for (std::size_t i = 0; i < size; ++i) {
        data[i] = static_cast<std::uint32_t>(i % 1000);
    }
}

void process_data(std::uint32_t *data, std::size_t size) {
    // Pojedyncze dodanie trwa zbyt krótko, aby je wiarygodnie zmierzyć.
    // Powtarzamy operację wiele razy, żeby jej koszt był widoczny ponad szum
    // pomiarowy.
    for (std::uint32_t round = 0; round < rounds; ++round) {
        for (std::size_t i = 0; i < size; ++i) {
            ++data[i];
        }
    }
}

bool verify_initial_data(const std::uint32_t *data, std::size_t size) {
    if (data == nullptr || size == 0) {
        return false;
    }
    for (std::size_t i = 0; i < size; ++i) {
        const std::uint32_t expected = static_cast<std::uint32_t>(i % 1000);
        if (data[i] != expected) {
            return false;
        }
    }
    return true;
}

bool verify_processed_data(const std::uint32_t *data, std::size_t size) {
    if (data == nullptr || size == 0) {
        return false;
    }
    for (std::size_t i = 0; i < size; ++i) {
        const std::uint32_t expected = static_cast<std::uint32_t>(i % 1000) + rounds;
        if (data[i] != expected) {
            return false;
        }
    }
    return true;
}

std::uint64_t checksum(const std::uint32_t *data, std::size_t size) {
    std::uint64_t result = 0;
    for (std::size_t i = 0; i < size; ++i) {
        result += data[i];
    }
    return result;
}

struct TrialResult {
    int trial;
    long long fixed_microseconds;
    long long global_microseconds;
    long long dynamic_microseconds;
    bool fixed_correct;
    bool global_correct;
    bool dynamic_correct;
    bool equal_results;
    std::uint64_t fixed_checksum;
    std::uint64_t global_checksum;
    std::uint64_t dynamic_checksum;
};

TrialResult run_trial(int trial) {
    // Tworzymy te obiekty razem, aby w jednej próbie porównać pamięć automatyczną
    // (lokalną) z pamięcią przydzielaną dynamicznie na stercie.
    FixedArray fixed_values{};
    auto dynamic_values = std::make_unique<std::uint32_t[]>(element_count);

    // Badamy przetwarzanie elementów, a nie koszt tworzenia tablic. Dlatego
    // przydział pamięci i przygotowanie danych wykonujemy przed pomiarem.
    prepare_data(fixed_values.data(), fixed_values.size());
    prepare_data(global_values.data(), global_values.size());
    prepare_data(dynamic_values.get(), element_count);

    if (!verify_initial_data(fixed_values.data(), fixed_values.size()) ||
        !verify_initial_data(global_values.data(), global_values.size()) ||
        !verify_initial_data(dynamic_values.get(), element_count)) {
        // Nie mierzymy błędnych danych: szybkie wykonanie operacji na złym wejściu
        // nie jest dowodem ani poprawności, ani dobrej wydajności.
        return TrialResult{ trial, 0, 0, 0, false, false, false, false, 0, 0, 0 };
    }

    long long fixed_time = 0;
    long long global_time = 0;
    long long dynamic_time = 0;

    // Nadajemy operacjom nazwy, aby zmieniać ich kolejność bez kopiowania kodu
    // pomiarowego i bez ryzyka, że warianty będą mierzone inaczej.
    const auto measure_fixed = [&fixed_values, &fixed_time]() {
        fixed_time =
            measure_microseconds([&fixed_values]() { process_data(fixed_values.data(), fixed_values.size()); });
    };
    const auto measure_global = [&global_time]() {
        global_time = measure_microseconds([]() { process_data(global_values.data(), global_values.size()); });
    };
    const auto measure_dynamic = [&dynamic_values, &dynamic_time]() {
        dynamic_time = measure_microseconds([&dynamic_values]() { process_data(dynamic_values.get(), element_count); });
    };

    if (trial % 3 == 1) {
        // Rotacja kolejności rozdziela między warianty wpływ rozgrzania procesora,
        // pamięci podręcznej i chwilowych zadań działających w tle.
        measure_fixed();
        measure_global();
        measure_dynamic();
    } else if (trial % 3 == 2) {
        measure_global();
        measure_dynamic();
        measure_fixed();
    } else {
        measure_dynamic();
        measure_fixed();
        measure_global();
    }

    const bool fixed_correct = verify_processed_data(fixed_values.data(), fixed_values.size());
    const bool global_correct = verify_processed_data(global_values.data(), global_values.size());
    const bool dynamic_correct = verify_processed_data(dynamic_values.get(), element_count);

    // Dwie różne tablice mogą przypadkiem mieć tę samą sumę kontrolną.
    // Dlatego poprawność potwierdzamy także przez porównanie każdego elementu.
    const bool equal_results = std::equal(fixed_values.begin(), fixed_values.end(), global_values.begin()) &&
                               std::equal(fixed_values.begin(), fixed_values.end(), dynamic_values.get());

    // Sumy kontrolne zapisujemy jako krótki ślad wyniku, ale nie zastępują one
    // dokładnej walidacji wykonanej element po elemencie.
    return TrialResult{ trial,
                        fixed_time,
                        global_time,
                        dynamic_time,
                        fixed_correct,
                        global_correct,
                        dynamic_correct,
                        equal_results,
                        checksum(fixed_values.data(), fixed_values.size()),
                        checksum(global_values.data(), global_values.size()),
                        checksum(dynamic_values.get(), element_count) };
}

int main() {
    const std::size_t bytes_per_array = element_count * sizeof(std::uint32_t);

    std::cout << "element_count=" << element_count << '\n'
              << "bytes_per_array=" << bytes_per_array << '\n'
              << "kibibytes_per_array=" << (bytes_per_array / 1024.0) << '\n'
              << "trial;fixed_us;global_us;dynamic_us;fixed_ok;global_ok;"
                 "dynamic_ok;equal;fixed_checksum;global_checksum;"
                 "dynamic_checksum\n";

    bool all_correct = true;
    for (int trial = 1; trial <= trial_count; ++trial) {
        const TrialResult result = run_trial(trial);
        all_correct = all_correct && result.fixed_correct && result.global_correct && result.dynamic_correct &&
                      result.equal_results;
        std::cout << result.trial << ';' << result.fixed_microseconds << ';' << result.global_microseconds << ';'
                  << result.dynamic_microseconds << ';' << std::boolalpha << result.fixed_correct << ';'
                  << result.global_correct << ';' << result.dynamic_correct << ';' << result.equal_results << ';'
                  << result.fixed_checksum << ';' << result.global_checksum << ';' << result.dynamic_checksum << '\n';
    }

    std::cout << "all_correct=" << std::boolalpha << all_correct << '\n';
    return all_correct ? 0 : 1;
}
