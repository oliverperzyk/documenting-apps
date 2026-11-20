"""Zlicza słowa w pliku ASCII i mierzy czas samego zliczania."""

import sys
import time
from dataclasses import dataclass


@dataclass
class BenchmarkResult:
    """Wynik pojedynczego pomiaru licznika.

    Attributes:
        count: Liczba znalezionych słów.
        elapsed: Czas zliczania w nanosekundach.
    """

    count: int
    elapsed: int


class Solution:
    """Zlicza słowa, mierzy czas i obsługuje wiersz poleceń."""

    @staticmethod
    def countWords(text: str) -> int:
        """Zlicza ciągi znaków oddzielone spacją, tabulatorem lub LF.

        CR, interpunkcja i pozostałe znaki mogą należeć do słowa.

        Args:
            text: Tekst do przeszukania.

        Returns:
            Liczba niepustych ciągów rozdzielonych separatorami.
        """
        count: int = 0
        inWord: bool = False

        for character in text:
            if character == " " or character == "\t" or character == "\n":
                inWord = False
            elif not inWord:
                count += 1
                inWord = True

        return count

    @staticmethod
    def benchmark(text: str) -> BenchmarkResult:
        """Mierzy czas zliczania za pomocą time.perf_counter_ns.

        Args:
            text: Tekst wczytany przed pomiarem.

        Returns:
            Liczba słów i czas samego zliczania w nanosekundach.
        """
        start: int = time.perf_counter_ns()
        count: int = Solution.countWords(text)
        stop: int = time.perf_counter_ns()
        return BenchmarkResult(count, stop - start)

    @staticmethod
    def printResults(result: BenchmarkResult) -> None:
        """Wypisuje liczbę słów i czas zliczania na stdout.

        Wiersz ma postać „Ilość znalezionych słów: N; (czas: T ns)”.

        Args:
            result: Wynik zawierający liczbę słów i czas w nanosekundach.
        """
        print(f"Ilość znalezionych słów: {result.count}; (czas: {result.elapsed} ns)")

    @staticmethod
    def init() -> int:
        """Wczytuje plik wskazany w sys.argv, mierzy czas i wypisuje wynik.

        Oczekuje jednej ścieżki. Czyta plik w trybie binarnym i dekoduje
        bajty jako ASCII przed rozpoczęciem pomiaru.

        Returns:
            Kod 0 po wypisaniu wyniku lub 1 przy błędnej liczbie argumentów,
            błędzie otwarcia lub odczytu pliku albo danych spoza ASCII.
            Komunikaty o tych błędach trafiają na stderr.
        """
        if len(sys.argv) != 2:
            print(f"Uzycie: {sys.argv[0]} <sciezka-do-pliku>", file=sys.stderr)
            return 1

        try:
            with open(sys.argv[1], "rb") as file:
                text: str = file.read().decode("ascii")
        except OSError as error:
            print(f"Blad otwarcia lub odczytu pliku: {sys.argv[1]}: {error}", file=sys.stderr)
            return 1
        except UnicodeDecodeError:
            print(f"Plik zawiera znaki spoza ASCII: {sys.argv[1]}", file=sys.stderr)
            return 1

        result = Solution.benchmark(text)
        Solution.printResults(result)
        return 0


if __name__ == "__main__":
    sys.exit(Solution.init())
