#include <chrono>
#include <cstddef>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <string>

struct BenchmarkResult {
    std::size_t count;
    std::chrono::nanoseconds elapsed;
};

class Solution {
  public:
    static std::size_t countWords(const std::string &text) {
        std::size_t count = 0;
        bool inWord = false;

        for (char character : text) {
            if (character == ' ' || character == '\t' || character == '\n') {
                inWord = false;
            } else if (!inWord) {
                ++count;
                inWord = true;
            }
        }

        return count;
    }

    static BenchmarkResult benchmark(const std::string &text) {
        const auto start = std::chrono::steady_clock::now();
        const std::size_t count = countWords(text);
        const auto stop = std::chrono::steady_clock::now();

        return { count, std::chrono::duration_cast<std::chrono::nanoseconds>(stop - start) };
    }

    static void printResults(const BenchmarkResult &result) {
        std::cout << "Ilość znalezionych słów: " << result.count << "; (czas: " << result.elapsed.count() << " ns)\n";
    }

    static int init(int argc, char *argv[]) {
        if (argc == 2 && std::string(argv[1]) == "--clock-info") {
            using Clock = std::chrono::steady_clock;
            std::cout << "{\"name\":\"std::chrono::steady_clock\",\"monotonic\":"
                      << (Clock::is_steady ? "true" : "false") << ",\"period_num\":" << Clock::period::num
                      << ",\"period_den\":" << Clock::period::den << "}\n";
            return 0;
        }
        if (argc != 2) {
            std::cerr << "Uzycie: " << argv[0] << " <sciezka-do-pliku>\n";
            return 1;
        }

        std::error_code pathError;
        const bool isDirectory = std::filesystem::is_directory(argv[1], pathError);
        std::ifstream file(argv[1], std::ios::binary);
        if (isDirectory || !file.is_open()) {
            std::cerr << "Nie mozna otworzyc pliku: " << argv[1] << '\n';
            return 1;
        }

        std::string text;
        char buffer[8192];
        while (file.read(buffer, sizeof(buffer))) {
            text.append(buffer, static_cast<std::size_t>(file.gcount()));
        }
        text.append(buffer, static_cast<std::size_t>(file.gcount()));

        if (file.bad() || !file.eof()) {
            std::cerr << "Blad odczytu pliku: " << argv[1] << '\n';
            return 1;
        }

        const BenchmarkResult result = benchmark(text);
        printResults(result);
        return 0;
    }
};

int main(int argc, char *argv[]) { return Solution::init(argc, argv); }
