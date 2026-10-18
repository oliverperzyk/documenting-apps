#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

std::int64_t calculate(const std::vector<std::int64_t> &values) {
    std::int64_t result = 0;
    for (int round = 0; round < 100; ++round) {
        for (const auto x : values) {
            auto d = x - 500;
            if (d < 0)
                d = -d;
            result += d;
        }
    }
    return result;
}

int main(int argc, char **argv) {
    if (argc != 6) {
        std::cerr << "usage: benchmark input count expected first_trial trials\n";
        return 2;
    }
    long long count, expected, first, trials;
    try {
        long long *targets[] = { &count, &expected, &first, &trials };
        for (int i = 2; i < 6; ++i) {
            std::size_t end = 0;
            *targets[i - 2] = std::stoll(argv[i], &end);
            if (end != std::string(argv[i]).size())
                throw std::invalid_argument("parameter");
        }
        if (count < 1 || count > 50000 || expected < 0 || expected > count * 500 * 100 || first < 1 || first > 10 ||
            trials < 1 || trials > 10 || first + trials > 11)
            throw std::invalid_argument("range");
    } catch (...) {
        std::cerr << "invalid parameters\n";
        return 2;
    }
    std::ifstream input(argv[1]);
    if (!input) {
        std::cerr << "input read error\n";
        return 2;
    }
    std::vector<std::int64_t> values;
    std::string token;
    while (input >> token) {
        try {
            std::size_t end = 0;
            auto x = std::stoll(token, &end);
            if (end != token.size() || x < 0 || x > 1000)
                throw std::invalid_argument("range");
            values.push_back(x);
        } catch (...) {
            std::cerr << "input parse/range error\n";
            return 2;
        }
    }
    if (input.bad() || values.size() != static_cast<std::size_t>(count)) {
        std::cerr << "invalid input/count\n";
        return 2;
    }
    using Clock = std::chrono::steady_clock;
    std::cerr << "clock=steady_clock;is_steady=" << Clock::is_steady << ";period_num=" << Clock::period::num
              << ";period_den=" << Clock::period::den << '\n';
    std::cout << "language;trial;time_ns;checksum;correct\n";
    for (int offset = -2; offset < trials; ++offset) {
        const auto start = Clock::now();
        const auto checksum = calculate(values);
        const auto stop = Clock::now();
        const auto ns = std::chrono::duration_cast<std::chrono::nanoseconds>(stop - start).count();
        const bool correct = checksum == expected;
        if (offset < 0) {
            std::cerr << "warmup=" << offset + 3 << ";time_ns=" << ns << ";checksum=" << checksum
                      << ";correct=" << (correct ? "true" : "false") << '\n';
        } else {
            std::cout << "cpp;" << first + offset << ';' << ns << ';' << checksum << ';' << (correct ? "true" : "false")
                      << '\n';
        }
        if (!correct)
            return 1;
    }
}
