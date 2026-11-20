"""Walidować wynik eksperymentu i publikować CSV tylko dla wiarygodnych danych."""

import argparse
import csv
import sys
from pathlib import Path

PROTOCOL_NAME = "TIDPI_RESULTS"
SUPPORTED_VERSION = "1"
EXPECTED_HEADER = [
    "case",
    "size",
    "trial",
    "time_us",
    "comparisons",
    "correct",
]
ALLOWED_CASES = {"sorted", "reversed", "random"}


def parse_integer(text, field_name, line_number, minimum, errors):
    """Sprawdzić jedno pole całkowite i zapisać opis wykrytego błędu.

    Args:
        text: Tekst odczytany z pola źródłowego.
        field_name: Nazwa pola używana w komunikacie diagnostycznym.
        line_number: Numer wiersza źródła liczony od jednego.
        minimum: Najmniejsza dopuszczalna wartość.
        errors: Modyfikowana lista, do której dopisywane są błędy walidacji.

    Returns:
        Odczytana liczba albo None, gdy pole nie przejdzie walidacji.
    """
    try:
        value = int(text)
    except ValueError:
        errors.append(f"line {line_number}: {field_name} must be an integer, got {text!r}")
        return None

    if value < minimum:
        errors.append(f"line {line_number}: {field_name} must be >= {minimum}, got {value}")
        return None

    return value


def parse_boolean(text, line_number, errors):
    """Sprawdzić wymagany przez protokół zapis wartości logicznej małymi literami.

    Args:
        text: Tekst odczytany z pola źródłowego.
        line_number: Numer wiersza źródła liczony od jednego.
        errors: Modyfikowana lista, do której dopisywane są błędy walidacji.

    Returns:
        True, False albo None, gdy pole nie przejdzie walidacji.
    """
    if text == "true":
        return True
    if text == "false":
        return False

    errors.append(f"line {line_number}: correct must be 'true' or 'false', got {text!r}")
    return None


def validate_rows(rows):
    """Sprawdzić cały protokół bez publikowania częściowych wyników.

    Args:
        rows: Wiersze podzielone już na pola przez czytnik CSV.

    Returns:
        Para zawierająca poprawne, ujednolicone rekordy i wszystkie komunikaty.
    """
    errors = []
    records = []
    identities = set()

    if len(rows) < 2:
        return [], ["file must contain a protocol line and a header"]

    # Sprawdzamy dokładnie wersję i nagłówek, aby przesunięte lub zmienione kolumny
    # nie zostały cicho zinterpretowane według nieaktualnych zasad.
    if rows[0] != [PROTOCOL_NAME, SUPPORTED_VERSION]:
        errors.append(f"line 1: expected {PROTOCOL_NAME};{SUPPORTED_VERSION}, got {';'.join(rows[0])!r}")

    if rows[1] != EXPECTED_HEADER:
        errors.append(f"line 2: expected header {';'.join(EXPECTED_HEADER)!r}, got {';'.join(rows[1])!r}")

    for line_number, row in enumerate(rows[2:], start=3):
        if len(row) != len(EXPECTED_HEADER):
            errors.append(f"line {line_number}: expected {len(EXPECTED_HEADER)} fields, got {len(row)}")
            continue

        error_count_before = len(errors)
        test_case, size_text, trial_text, time_text, comparisons_text, correct_text = row

        if test_case not in ALLOWED_CASES:
            errors.append(
                f"line {line_number}: unknown case {test_case!r}; allowed: {', '.join(sorted(ALLOWED_CASES))}"
            )

        size = parse_integer(size_text, "size", line_number, 2, errors)
        trial = parse_integer(trial_text, "trial", line_number, 1, errors)
        time_us = parse_integer(time_text, "time_us", line_number, 0, errors)
        comparisons = parse_integer(
            comparisons_text,
            "comparisons",
            line_number,
            0,
            errors,
        )
        correct = parse_boolean(correct_text, line_number, errors)

        if size is not None and trial is not None:
            # Sama nazwa przypadku nie jest unikatowa. Dopiero przypadek, rozmiar i numer
            # próby razem wskazują jeden pomiar, więc ten zestaw wykrywa duplikaty.
            identity = (test_case, size, trial)
            if identity in identities:
                errors.append(f"line {line_number}: duplicate record identity {identity!r}")
            else:
                identities.add(identity)

        if len(errors) == error_count_before:
            records.append(
                {
                    "case": test_case,
                    "size": size,
                    "trial": trial,
                    "time_us": time_us,
                    "comparisons": comparisons,
                    "correct": "true" if correct else "false",
                }
            )

    if len(rows) == 2:
        errors.append("file contains no result records")

    return records, errors


def read_rows(input_path):
    """Odczytać z pliku UTF-8 wiersze rozdzielone średnikami.

    Args:
        input_path: Ścieżka surowego wyniku eksperymentu.

    Returns:
        Lista wierszy, z których każdy jest listą pól.

    Raises:
        OSError: Gdy pliku nie można otworzyć albo odczytać.
        UnicodeError: Gdy wejście nie jest poprawnym tekstem UTF-8.
        csv.Error: Gdy parser CSV nie potrafi odczytać struktury.
    """
    with input_path.open("r", encoding="utf-8-sig", newline="") as source:
        return list(csv.reader(source, delimiter=";"))


def write_csv(output_path, records):
    """Zastąpić plik docelowy ujednoliconymi rekordami rozdzielonymi średnikami.

    Args:
        output_path: Ścieżka docelowego pliku CSV.
        records: Zweryfikowane rekordy zgodne z EXPECTED_HEADER.

    Raises:
        OSError: Gdy nie można zapisać pliku docelowego.
    """
    with output_path.open("w", encoding="utf-8-sig", newline="") as target:
        writer = csv.DictWriter(
            target,
            fieldnames=EXPECTED_HEADER,
            delimiter=";",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(records)


def main():
    """Zweryfikować plik wejściowy i zwrócić status zrozumiały dla automatyzacji."""
    parser = argparse.ArgumentParser(description="Validate TiDPI result output and create a clean CSV file.")
    parser.add_argument("input", type=Path, help="raw output from the C++ program")
    parser.add_argument("output", type=Path, help="validated CSV destination")
    args = parser.parse_args()

    # Usuwamy stary CSV przed walidacją, aby po odrzuceniu nowych danych nie pozostał
    # plik z poprzedniej próby, który wyglądałby jak aktualny wynik.
    args.output.unlink(missing_ok=True)

    # Zapisujemy CSV dopiero po sprawdzeniu wszystkich wierszy. Jeden błędny rekord
    # odrzuca cały zestaw, więc nie publikujemy mylących wyników częściowych.
    try:
        rows = read_rows(args.input)
    except (OSError, UnicodeError, csv.Error) as error:
        print(f"VALIDATION ERROR: cannot read input: {error}", file=sys.stderr)
        return 2

    records, errors = validate_rows(rows)

    if errors:
        for error in errors:
            print(f"VALIDATION ERROR: {error}", file=sys.stderr)
        print(f"REJECTED: {len(errors)} validation error(s)", file=sys.stderr)
        return 2

    try:
        write_csv(args.output, records)
    except OSError as error:
        print(f"OUTPUT ERROR: cannot write CSV: {error}", file=sys.stderr)
        return 2

    failed_tests = sum(record["correct"] == "false" for record in records)
    print(f"ACCEPTED: {len(records)} record(s), failed tests: {failed_tests}")

    return 1 if failed_tests else 0


if __name__ == "__main__":
    raise SystemExit(main())
