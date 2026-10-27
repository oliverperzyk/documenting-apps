import sys
import time
from dataclasses import dataclass


@dataclass
class BenchmarkResult:
    count: int
    elapsed: int


class Solution:
    @staticmethod
    def countWords(text: str) -> int:
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
        start: int = time.perf_counter_ns()
        count: int = Solution.countWords(text)
        stop: int = time.perf_counter_ns()
        return BenchmarkResult(count, stop - start)

    @staticmethod
    def printResults(result: BenchmarkResult) -> None:
        print(f"Ilość znalezionych słów: {result.count}; (czas: {result.elapsed} ns)")

    @staticmethod
    def init() -> int:
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
