/// \file
/// \brief Licznik słów z pomiarem czasu zliczania i informacją o zegarze.

#include <chrono>
#include <cstddef>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <string>

/// \brief Wynik pojedynczego pomiaru licznika.
struct BenchmarkResult {
    /// \brief Liczba znalezionych słów.
    std::size_t count;
    /// \brief Czas zliczania w nanosekundach.
    std::chrono::nanoseconds elapsed;
};

/// \brief Zlicza słowa, mierzy czas i obsługuje wiersz poleceń.
class Solution {
  public:
    /// \brief Zlicza ciągi bajtów oddzielone spacją, tabulatorem lub LF.
    ///
    /// CR, interpunkcja i pozostałe bajty mogą należeć do słowa.
    ///
    /// \param text Bajty wejściowe do przeszukania.
    /// \return Liczba niepustych ciągów rozdzielonych separatorami.
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

    /// \brief Mierzy czas zliczania za pomocą std::chrono::steady_clock.
    ///
    /// \param text Bajty wczytane przed pomiarem.
    /// \return Liczba słów i czas samego zliczania w nanosekundach.
    static BenchmarkResult benchmark(const std::string &text) {
        const auto start = std::chrono::steady_clock::now();
        const std::size_t count = countWords(text);
        const auto stop = std::chrono::steady_clock::now();

        return { count, std::chrono::duration_cast<std::chrono::nanoseconds>(stop - start) };
    }

    /// \brief Wypisuje liczbę słów i czas zliczania na stdout.
    ///
    /// Wiersz ma postać „Ilość znalezionych słów: N; (czas: T ns)”.
    ///
    /// \param result Wynik zawierający liczbę słów i czas w nanosekundach.
    static void printResults(const BenchmarkResult &result) {
        std::cout << "Ilość znalezionych słów: " << result.count << "; (czas: " << result.elapsed.count() << " ns)\n";
    }

    /// \brief Obsługuje pomiar dla wskazanego pliku lub tryb --clock-info.
    ///
    /// Odczytuje plik binarnie przed pomiarem i wypisuje wynik na stdout.
    /// Tryb --clock-info wypisuje JSON z nazwą zegara, informacją o jego
    /// monotoniczności oraz licznikiem i mianownikiem nominalnego okresu.
    ///
    /// \param argc Liczba argumentów łącznie z nazwą programu.
    /// \param argv Nazwa programu i jeden argument ze ścieżką lub --clock-info.
    /// \retval 0 Wypisano wynik pomiaru lub informację o zegarze.
    /// \retval 1 Wypisano błąd argumentów, otwarcia lub odczytu na stderr.
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

/// \brief Przekazuje argumenty wiersza poleceń do Solution::init.
///
/// \param argc Liczba argumentów łącznie z nazwą programu.
/// \param argv Tablica argumentów wiersza poleceń.
/// \return Kod zakończenia zwrócony przez Solution::init.
int main(int argc, char *argv[]) { return Solution::init(argc, argv); }
