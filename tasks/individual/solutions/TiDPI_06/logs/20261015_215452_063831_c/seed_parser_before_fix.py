"""Parser kontraktu TiDPI_RESULTS;2 i eksport zweryfikowanych danych do CSV.

Uruchomienie: python3 main.py raw_output.txt results.csv
Kody: 0 — poprawne dane; 1 — poprawne dane z nieudanym testem;
2 — błąd wejścia, kontraktu lub zapisu. Nie wymaga dodatkowych bibliotek.
"""

import argparse
import csv
import os
import sys
import tempfile
from pathlib import Path

PROTOCOL = ["TIDPI_RESULTS", "2"]
EXPECTED_HEADER = ["case", "size", "trial", "time_us", "comparisons", "correct", "seed"]
ALLOWED_CASES = {"sorted", "reversed", "random"}
INTEGER_MINIMUMS = {"size": 2, "trial": 1, "time_us": 0, "comparisons": 0, "seed": 0}


def read_rows(input_path):
    """Odczytaj CSV wraz z rzeczywistymi numerami wierszy (UTF-8 z/bez BOM)."""
    rows = []
    with input_path.open(encoding="utf-8-sig", newline="") as source:
        reader = csv.reader(source, delimiter=";", strict=True)
        while True:
            line_number = reader.line_num + 1
            try:
                row = next(reader)
            except StopIteration:
                break
            except csv.Error as error:
                raise csv.Error(f"line {line_number}: {error}") from error
            # Kontrakt v2 przewiduje jeden rekord na wiersz, bez pól wielowierszowych.
            if reader.line_num != line_number:
                raise csv.Error(f"line {line_number}: multiline records are not allowed")
            rows.append((line_number, row))
    return rows


def validate_rows(rows):
    """Zbierz niezależne błędy; żaden rekord nie jest jeszcze publikowany."""
    records, errors = [], []
    identities = set()
    if len(rows) < 2:
        return [], ["line 1: file must contain a protocol line and a header"]

    if rows[0][1] != PROTOCOL:
        errors.append("line 1: expected protocol TIDPI_RESULTS;1")
    if rows[1][1] != EXPECTED_HEADER:
        errors.append(f"line 2: expected header {';'.join(EXPECTED_HEADER)}")

    for line_number, row in rows[2:]:
        prefix = f"line {line_number}: "
        if len(row) != len(EXPECTED_HEADER):
            errors.append(prefix + f"expected {len(EXPECTED_HEADER)} fields, got {len(row)}")
            continue
        error_count = len(errors)
        record = dict(zip(EXPECTED_HEADER, row))
        if record["case"] not in ALLOWED_CASES:
            errors.append(prefix + f"unknown case {record['case']!r}")

        for field, minimum in INTEGER_MINIMUMS.items():
            try:
                value = int(record[field])
            except ValueError:
                errors.append(prefix + f"{field} must be an integer, got {record[field]!r}")
                record[field] = None
                continue
            record[field] = value
            if value < minimum:
                errors.append(prefix + f"{field} must be >= {minimum}, got {value}")

        if record["seed"] is not None and record["seed"] > 4294967295:
            errors.append(prefix + f"seed must be <= 4294967295, got {record['seed']}")

        if record["correct"] not in {"true", "false"}:
            errors.append(prefix + "correct must be exactly 'true' or 'false'")

        if record["size"] is not None and record["trial"] is not None:
            identity = (record["case"], record["size"], record["trial"])
            if identity in identities:
                errors.append(prefix + f"duplicate record identity {identity!r}")
            identities.add(identity)

        if len(errors) == error_count:
            records.append(record)

    if len(rows) == 2:
        errors.append("line 3: file contains no result records")
    return records, errors


def write_csv(output_path, records):
    """Publikuj kompletny CSV atomowo, po udanym zamknięciu pliku tymczasowego."""
    temporary_path = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8-sig", newline="", dir=output_path.parent,
            prefix=".tidpi-results-", suffix=".tmp", delete=False,
        ) as target:
            temporary_path = Path(target.name)
            writer = csv.DictWriter(
                target, fieldnames=EXPECTED_HEADER, delimiter=";", lineterminator="\n",
            )
            writer.writeheader()
            writer.writerows(records)
        os.replace(temporary_path, output_path)
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Walidacja TiDPI_RESULTS;2 i eksport CSV (UTF-8 BOM, separator ;).",
        epilog="Kody zakończenia: 0 = PASS, 1 = poprawne dane z FAIL, 2 = błąd.",
    )
    parser.add_argument("input", type=Path, help="surowy plik wyjściowy producenta C++")
    parser.add_argument("output", type=Path, help="docelowy CSV; stary plik zostanie usunięty")
    args = parser.parse_args(argv)

    # Sprawdzenie musi poprzedzać unlink, również dla aliasów i dowiązań twardych.
    try:
        same_path = args.input.resolve() == args.output.resolve()
        if args.input.exists() and args.output.exists():
            same_path = same_path or args.input.samefile(args.output)
        if same_path:
            print("OUTPUT ERROR: input and output must be distinct files", file=sys.stderr)
            return 2
        args.output.unlink(missing_ok=True)
    except (OSError, RuntimeError) as error:
        print(f"OUTPUT ERROR: cannot prepare destination: {error}", file=sys.stderr)
        return 2

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
    except (OSError, UnicodeError, csv.Error) as error:
        print(f"OUTPUT ERROR: cannot write CSV: {error}", file=sys.stderr)
        return 2

    failed_tests = sum(record["correct"] == "false" for record in records)
    print(f"ACCEPTED: {len(records)} record(s), failed tests: {failed_tests}")
    return 1 if failed_tests else 0


if __name__ == "__main__":
    raise SystemExit(main())
