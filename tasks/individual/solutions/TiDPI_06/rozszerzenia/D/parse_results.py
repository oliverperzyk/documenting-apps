"""TiDPI v1: walidacja całości oraz wymagany, ustrukturyzowany raport JSON.

python3 parse_results.py input.txt results.csv --report-json validation.json
Kody: 0 = poprawne dane, 1 = poprawne dane z FAIL, 2 = odrzucenie/błąd I/O.
"""

import argparse
import csv
import json
import os
import sys
import tempfile
from pathlib import Path

HEADER = ["case", "size", "trial", "time_us", "comparisons", "correct"]
MINIMUMS = {"size": 2, "trial": 1, "time_us": 0, "comparisons": 0}
CASES = {"sorted", "reversed", "random"}


def issue(rule, line, message):
    return {"rule": rule, "line": line, "message": message}


def safe_io_error(error):
    """Diagnostyka bez prywatnych nazw plików, także dla tempfile."""
    if isinstance(error, OSError):
        return f"{error.strerror} (errno={error.errno})"
    return str(error)


def read_rows(path):
    rows = []
    try:
        with path.open(encoding="utf-8-sig", newline="") as source:
            reader = csv.reader(source, delimiter=";", strict=True)
            while True:
                line = reader.line_num + 1
                try:
                    row = next(reader)
                except StopIteration:
                    break
                except csv.Error as error:
                    return [], [issue("CSV_SYNTAX", line, str(error))]
                if reader.line_num != line:
                    return [], [issue("MULTILINE", line, "multiline records are not allowed")]
                rows.append((line, row))
    except (OSError, UnicodeError) as error:
        return [], [issue("READ", None, f"cannot read input: {safe_io_error(error)}")]
    return rows, []


def validate_rows(rows):
    records, errors = [], []
    identities = set()
    if len(rows) < 2:
        return [], [issue("FILE_STRUCTURE", 1, "protocol line and header are required")]
    if rows[0][1] != ["TIDPI_RESULTS", "1"]:
        errors.append(issue("PROTOCOL", 1, "expected protocol TIDPI_RESULTS;1"))
    if rows[1][1] != HEADER:
        errors.append(issue("HEADER", 2, "expected header " + ";".join(HEADER)))
    for line, row in rows[2:]:
        if not row:
            errors.append(issue("BLANK_ROW", line, "unexpected blank row"))
            continue
        if row == HEADER:
            errors.append(issue("REPEATED_HEADER", line, "unexpected repeated header"))
            continue
        if len(row) != len(HEADER):
            errors.append(issue("FIELD_COUNT", line, f"expected 6 fields, got {len(row)}"))
            continue
        before = len(errors)
        record = dict(zip(HEADER, row))
        if record["case"] not in CASES:
            errors.append(issue("CASE", line, f"unknown case {record['case']!r}"))
        for field, minimum in MINIMUMS.items():
            try:
                value = int(record[field])
            except ValueError:
                errors.append(issue("INTEGER", line, f"{field} must be an integer, got {record[field]!r}"))
                record[field] = None
                continue
            record[field] = value
            if value < minimum:
                errors.append(issue("RANGE", line, f"{field} must be >= {minimum}, got {value}"))
        if record["correct"] not in {"true", "false"}:
            errors.append(issue("BOOLEAN", line, "correct must be exactly 'true' or 'false'"))
        if record["size"] is not None and record["trial"] is not None:
            identity = (record["case"], record["size"], record["trial"])
            if identity in identities:
                errors.append(issue("DUPLICATE", line, f"duplicate record identity {identity!r}"))
            identities.add(identity)
        if len(errors) == before:
            records.append(record)
    if len(rows) == 2:
        errors.append(issue("EMPTY_DATA", 3, "file contains no result records"))
    return records, errors


def atomic_write(path, encoding, emit):
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding=encoding, newline="", dir=path.parent,
            prefix=".tidpi-d-", suffix=".tmp", delete=False,
        ) as target:
            temporary = Path(target.name)
            emit(target)
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def write_csv(path, records):
    def emit(target):
        writer = csv.DictWriter(target, fieldnames=HEADER, delimiter=";", lineterminator="\n")
        writer.writeheader()
        writer.writerows(records)
    atomic_write(path, "utf-8-sig", emit)


def write_json(path, report):
    atomic_write(path, "utf-8", lambda target: json.dump(report, target, ensure_ascii=False, indent=2))


def aliases(a, b):
    return a.resolve() == b.resolve() or (a.exists() and b.exists() and a.samefile(b))


def print_errors(errors):
    for error in errors:
        location = f"line {error['line']}: " if error["line"] is not None else ""
        print(f"VALIDATION ERROR [{error['rule']}]: {location}{error['message']}", file=sys.stderr)


def main(argv=None):
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("input", type=Path)
    cli.add_argument("output", type=Path)
    cli.add_argument("--report-json", required=True, type=Path)
    args = cli.parse_args(argv)
    paths = [args.input, args.output, args.report_json]
    try:
        if any(aliases(paths[i], paths[j]) for i in range(3) for j in range(i + 1, 3)):
            print_errors([issue("PATH", None, "input, CSV and JSON must be distinct files")])
            return 2
    except (OSError, RuntimeError) as error:
        print_errors([issue("PATH", None, f"cannot check paths: {safe_io_error(error)}")])
        return 2

    records, errors = [], []
    try:
        args.output.unlink(missing_ok=True)
        args.report_json.unlink(missing_ok=True)
    except OSError as error:
        errors.append(issue("OUTPUT", None, f"cannot prepare destinations: {safe_io_error(error)}"))
    if not errors:
        rows, errors = read_rows(args.input)
        if not errors:
            records, errors = validate_rows(rows)
    if not errors:
        try:
            write_csv(args.output, records)
        except (OSError, UnicodeError, csv.Error) as error:
            errors.append(issue("OUTPUT", None, f"cannot write CSV: {safe_io_error(error)}"))
    failed_tests = sum(r["correct"] == "false" for r in records) if not errors else 0
    code = 2 if errors else (1 if failed_tests else 0)
    report = {
        "schema_version": 1,
        "decision": "rejected" if errors else ("failed_tests" if failed_tests else "accepted"),
        "exit_code": code,
        "published_records": 0 if errors else len(records),
        "failed_tests": failed_tests,
        "csv_created": not errors,
        "errors": errors,
    }
    try:
        write_json(args.report_json, report)
    except (OSError, UnicodeError) as error:
        # Sukces CSV bez obowiązkowego raportu nie jest sukcesem całego przebiegu.
        try:
            args.output.unlink(missing_ok=True)
        except OSError as cleanup_error:
            print_errors([issue("OUTPUT", None, f"cannot remove CSV: {safe_io_error(cleanup_error)}")])
        print_errors(errors + [issue("REPORT", None, f"cannot write JSON: {safe_io_error(error)}")])
        return 2
    if errors:
        print_errors(errors)
        print(f"REJECTED: {len(errors)} validation error(s)", file=sys.stderr)
    else:
        print(f"ACCEPTED: {len(records)} record(s), failed tests: {failed_tests}")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
