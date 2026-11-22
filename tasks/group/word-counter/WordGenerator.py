import argparse
import hashlib
import json
import random
from collections.abc import Sequence
from pathlib import Path


class WordGenerator:
    """Tworzy wspolne dane dla implementacji C++ i Python oraz oczekiwane wyniki."""

    # Lokalna kopia 250 slow pobranych z first20hours/google-10000-english.
    # Pochodzenie, sposob wyboru i hash pobranej listy sa zapisane obok slow.
    VOCABULARY = json.loads((Path(__file__).resolve().parent / "assets/english_words.json").read_text(encoding="ascii"))
    SHORT_WORDS = tuple(VOCABULARY["short"])  # 125 slow, 1-5 liter.
    LONG_WORDS = tuple(VOCABULARY["long"])  # 125 slow, 7-8 liter.
    # Nazwa, slownik, dlugosc grupy separatorow, cykl separatorow.
    VARIANTS = (
        ("short_sparse_mixed", SHORT_WORDS, 1, b" \t\n"),
        ("short_dense_mixed", SHORT_WORDS, 8, b" \t\n"),
        ("long_sparse_mixed", LONG_WORDS, 1, b" \t\n"),
        ("long_dense_mixed", LONG_WORDS, 8, b" \t\n"),
        ("short_spaces", SHORT_WORDS, 1, b" "),
        ("short_tabs", SHORT_WORDS, 1, b"\t"),
        ("short_lf", SHORT_WORDS, 1, b"\n"),
    )
    # Oczekiwania zapisane recznie, niezaleznie od implementacji licznika slow.
    FIXTURES = (
        ("empty", b"", 0),
        ("only_separators", b" \t\n  \n\t", 0),
        ("one_word_no_trailing_separator", b"word", 1),
        ("repeated_spaces", b"Ala  ma", 2),
        ("mixed_separators", b"Ala\tma\nkota", 3),
        ("leading_trailing_separators", b" \t\ncat  dog\n\t ", 2),
        ("punctuation", b"kot,pies", 1),
        ("cr_is_not_separator", b"Ala\rma", 1),
    )

    @staticmethod
    def positive_size(value: str) -> int:
        """
        Odrzuca niepoprawny rozmiar przed utworzeniem plików.

        Args:
            value - tekstowa wartość argumentu określającego rozmiar pliku w bajtach.

        Returns:
            Dodatnia liczba całkowita określająca rozmiar pliku w bajtach.

        Raises:
            argparse.ArgumentTypeError - jeśli wartość nie jest liczbą całkowitą większą od zera.
        """
        try:
            size = int(value)
        except ValueError as error:
            raise argparse.ArgumentTypeError("Rozmiar musi byc dodatnia liczba calkowita bajtow.") from error
        if size <= 0:
            raise argparse.ArgumentTypeError("Rozmiar musi byc wiekszy od zera.")
        return size

    @staticmethod
    def build_text(
        size: int, words: Sequence[str], gap: int, separators: bytes, rng: random.Random
    ) -> tuple[bytes, int]:
        """
        Buduje tekst z pełnych słów i zlicza je podczas dodawania.

        Args:
            size - docelowa długość tekstu w bajtach; liczba nieujemna.
            words - niepusta lista lub inna sekwencja niepustych słów ASCII bez separatorów.
            gap - dodatnia liczba separatorów dodawanych po każdym słowie, o ile wystarczy miejsca.
            separators - niepusty cykl bajtów separatorów: spacji, tabulatorów lub LF.
            rng - generator liczb pseudolosowych używany do wyboru słów.

        Returns:
            Para zawierająca tekst jako bytes o długości size oraz oczekiwaną liczbę słów.
            Miejsce, w którym nie mieści się pełne słowo, zostaje wypełnione separatorami.
        """
        vocabulary = tuple(word.encode("ascii") for word in words)
        shortest = min(map(len, vocabulary))
        longest = max(map(len, vocabulary))
        result = bytearray()
        expected_words = 0
        separator_position = 0

        def append_separators(count: int) -> None:
            """
            Dopisuje separatory do budowanego tekstu, kontynuując ich cykl.

            Args:
                count - liczba bajtów separatorów do dopisania.
            """
            nonlocal separator_position
            for _ in range(count):
                result.append(separators[separator_position % len(separators)])
                separator_position += 1

        while len(result) < size:
            remaining = size - len(result)
            if remaining < shortest:
                append_separators(remaining)
                break
            available = (
                vocabulary if remaining >= longest else tuple(word for word in vocabulary if len(word) <= remaining)
            )
            result.extend(rng.choice(available))
            expected_words += 1
            append_separators(min(gap, size - len(result)))
        return bytes(result), expected_words

    @classmethod
    def generate(cls, output_dir: Path, sizes: Sequence[int], seed: int) -> dict:
        """
        Zapisuje pliki benchmarkowe, przypadki kontrolne i manifest bieżącego zestawu.

        Args:
            output_dir - katalog docelowy; zostanie utworzony, jeśli nie istnieje.
            sizes - niepusta sekwencja dodatnich rozmiarów plików benchmarkowych w bajtach.
                Powtórzenia są usuwane, a rozmiary sortowane rosnąco.
            seed - ziarno losowania zapewniające powtarzalność danych dla tych samych parametrów.

        Returns:
            Słownik manifestu zawierający konfigurację, słowniki, warianty i listę plików
            z rozmiarami, oczekiwanymi liczbami słów oraz sumami SHA-256.
            Ten sam manifest zostaje zapisany w pliku manifest.json.

        Raises:
            ValueError - jeśli lista rozmiarów jest pusta lub zawiera rozmiar niedodatni.
            OSError - jeśli nie można utworzyć katalogu lub zapisać plików.
        """
        if not sizes or any(size <= 0 for size in sizes):
            raise ValueError("Podaj co najmniej jeden dodatni rozmiar.")
        sizes = sorted(set(sizes))
        output_dir.mkdir(parents=True, exist_ok=True)
        records = []

        def save(name: str, data: bytes, expected: int, **metadata: object) -> None:
            """
            Zapisuje pojedynczy plik i dodaje jego opis do listy rekordów manifestu.

            Args:
                name - nazwa pliku w katalogu output_dir.
                data - bajty przeznaczone do zapisania w pliku.
                expected - oczekiwana liczba słów w danych.
                **metadata - dodatkowe pola rekordu, np. rodzaj danych i nazwa wariantu.
            """
            (output_dir / name).write_bytes(data)
            records.append(
                {
                    "file": name,
                    "size_bytes": len(data),
                    "expected_words": expected,
                    "sha256": hashlib.sha256(data).hexdigest(),
                    **metadata,
                }
            )

        for name, words, gap, separators in cls.VARIANTS:
            for size in sizes:
                # Oddzielne ziarno dla kazdego pliku: wybor innych rozmiarow nie zmienia tego pliku.
                rng = random.Random(f"{seed}:{name}:{size}")
                data, expected = cls.build_text(size, words, gap, separators, rng)
                save(f"{name}_{size}.txt", data, expected, kind="benchmark", variant=name)
        for name, data, expected in cls.FIXTURES:
            save(f"test_{name}.txt", data, expected, kind="test", variant=name)

        manifest = {
            "generator_version": 2,
            "encoding": "ascii",
            "seed": seed,
            "sizes_bytes": sizes,
            "word_separators": [" ", "\t", "\n"],
            "padding": "Full words only; remaining bytes are filled with variant separators.",
            "vocabulary": {"short": cls.SHORT_WORDS, "long": cls.LONG_WORDS},
            "vocabulary_source": cls.VOCABULARY["source"],
            "variants": [
                {
                    "name": name,
                    "word_length_min": min(map(len, words)),
                    "word_length_max": max(map(len, words)),
                    "separator_group_length": gap,
                    "separator_cycle": separators.decode("ascii"),
                }
                for name, words, gap, separators in cls.VARIANTS
            ],
            "files": records,
        }
        (output_dir / "manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=True, indent=4) + "\n", encoding="ascii"
        )
        return manifest

    @classmethod
    def init(cls, argv: Sequence[str] | None = None) -> None:
        """
        Odczytuje argumenty, uruchamia generator i wypisuje podsumowanie.

        Args:
            argv - argumenty wiersza poleceń bez nazwy skryptu; None oznacza użycie
                argumentów procesu. Obsługuje --output-dir, --sizes oraz --seed.

        Raises:
            SystemExit - po wyświetleniu pomocy (kod 0), przy błędzie argumentów (kod 2)
                lub błędzie zapisu danych (kod 1).
        """
        parser = argparse.ArgumentParser(description="Generator plikow ASCII do benchmarku licznika slow.")
        parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parent / "data")
        parser.add_argument("--sizes", type=cls.positive_size, nargs="+", default=[1000, 100000, 1000000])
        parser.add_argument("--seed", type=int, default=14)
        args = parser.parse_args(argv)
        try:
            manifest = cls.generate(args.output_dir, args.sizes, args.seed)
        except OSError as error:
            parser.exit(1, f"Nie udalo sie zapisac danych: {error}\n")
        print(f"Zapisano {len(manifest['files'])} plikow oraz manifest.json w {args.output_dir}")


if __name__ == "__main__":
    WordGenerator.init()
