"""Wykonać ten sam benchmark co program C++ i wypisać zgodne rekordy CSV."""

import argparse
import time
from pathlib import Path


def load_data(path):
    """Odczytać wspólne dane całkowite z pliku tekstowego.

    Args:
        path: Ścieżka pliku z jedną liczbą w każdym wierszu.

    Returns:
        Lista odczytanych liczb całkowitych.

    Raises:
        ValueError: Gdy plik jest pusty albo zawiera tekst inny niż liczba.
        OSError: Gdy pliku nie można odczytać.
    """
    values = [int(line) for line in path.read_text(encoding="utf-8").splitlines()]
    if not values:
        raise ValueError("input file is empty")
    return values


def calculate_checksum(values, rounds):
    """Obliczyć kontrolny wynik pracy wykonywanej przez oba programy."""
    checksum = 0
    for _ in range(rounds):
        for value in values:
            checksum += value * value
    return checksum


def main():
    """Uruchomić rozgrzewkę i serię pomiarów, zwracając status dla automatyzacji."""
    parser = argparse.ArgumentParser(description="Run the TiDPI Python benchmark.")
    parser.add_argument("data_file", type=Path)
    parser.add_argument("rounds", type=int)
    parser.add_argument("warmup", type=int)
    parser.add_argument("repeat", type=int)
    args = parser.parse_args()
    if args.rounds < 1 or args.warmup < 0 or args.repeat < 1:
        parser.error("ROUNDS and REPEAT must be positive; WARMUP cannot be negative")

    try:
        values = load_data(args.data_file)
    except (OSError, ValueError) as error:
        print(f"ERROR: {error}")
        return 2

    expected = calculate_checksum(values, 1) * args.rounds

    # Rozgrzewki nie raportujemy jako pomiaru. Ma ona przygotować interpreter
    # i dane, aby pierwsza zapisana próba nie była wyjątkowym „zimnym startem”.
    for _ in range(args.warmup):
        if calculate_checksum(values, args.rounds) != expected:
            print("ERROR: warmup returned an incorrect checksum")
            return 1

    print("language;trial;time_ns;checksum;correct")
    for trial in range(1, args.repeat + 1):
        # perf_counter_ns mierzy upływ czasu zegarem monotonicznym. Wczytanie pliku
        # pozostaje poza pomiarem, ponieważ badamy pętlę obliczeniową, nie dysk.
        start = time.perf_counter_ns()
        checksum = calculate_checksum(values, args.rounds)
        stop = time.perf_counter_ns()
        correct = checksum == expected
        print(f"python;{trial};{stop - start};{checksum};{str(correct).lower()}")
        if not correct:
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
