"""Mierzy czas liczenia słów w Pythonie po rozgrzewce w tym samym procesie."""

from pathlib import Path
from statistics import median

from source.python.main import Solution


def main() -> None:
    input_path = Path(__file__).resolve().parent / "data/100000B_seed42/long_dense_mixed_100000.txt"
    text = input_path.read_bytes().decode("ascii")
    expected_words = 6498

    for _ in range(5):
        Solution.countWords(text)

    times_ns = []
    for _ in range(30):
        result = Solution.benchmark(text)
        if result.count != expected_words:
            raise SystemExit(f"Oczekiwano {expected_words} słów, otrzymano {result.count}.")
        times_ns.append(result.elapsed)

    print(f"{expected_words} słów, mediana z {len(times_ns)} prób wynosi {median(times_ns)} ns.")


if __name__ == "__main__":
    main()
