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
    if (argc != 3 || (std::string(argv[2]) != "1" && std::string(argv[2]) != "6")) {
        std::cerr << "usage: benchmark input.txt first_trial(1|6)\n";
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
    if (input.bad() || values.size() != 20020) {
        std::cerr << "invalid input/count\n";
        return 2;
    }
    using Clock = std::chrono::steady_clock;
    std::cerr << "clock=steady_clock;is_steady=" << Clock::is_steady << ";period_num=" << Clock::period::num
              << ";period_den=" << Clock::period::den << '\n';
    std::cout << "language;trial;time_ns;checksum;correct\n";
    const int first = std::stoi(argv[2]);
    for (int offset = -2; offset < 5; ++offset) {
        const auto start = Clock::now();
        const auto checksum = calculate(values);
        const auto stop = Clock::now();
        const auto ns = std::chrono::duration_cast<std::chrono::nanoseconds>(stop - start).count();
        const bool correct = checksum == 501000000;
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
