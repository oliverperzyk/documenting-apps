"""Uruchom niezależne oczekiwania fixture: python3 -B run_fixtures.py.

Każdy przebieg zachowuje osobne wyniki; 0 = wszystkie kontrole zgodne,
1 = co najmniej jedna niezgodność/awaria. Nie aktualizuje oczekiwań.
"""

import csv
import hashlib
import io
import json
import os
import platform
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent
TASK = ROOT.parent.parent
REPORT_KEYS = {"schema_version", "decision", "exit_code", "published_records",
               "failed_tests", "csv_created", "errors"}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save_json(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def frozen_previous():
    return {str(p.relative_to(TASK)): sha(p) for p in TASK.rglob("*")
            if p.is_file() and ROOT not in p.parents and "_build" not in p.parts
            and p.suffix != ".pdf" and p.name != "RAPORT.md"}


def execute(folder, source, output="results.csv", report="validation.json"):
    command = ["python3", "-B", os.path.relpath(ROOT / "parse_results.py", folder),
               os.path.relpath(source, folder), output, "--report-json", report]
    save_json(folder / "command.json", command)
    try:
        result = subprocess.run(command, cwd=folder, shell=False, capture_output=True,
                                check=False, timeout=10)
        code, stdout, stderr = result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired as error:
        code, stdout, stderr = 124, error.stdout or b"", error.stderr or b""
    except OSError as error:
        code, stdout, stderr = 127, b"", str(error).encode("utf-8")
    (folder / "parser_stdout.txt").write_bytes(stdout)
    (folder / "parser_stderr.txt").write_bytes(stderr)
    (folder / "parser_exit_code.txt").write_text(f"{code}\n", encoding="utf-8")
    return code, stdout.decode("utf-8", errors="replace"), stderr.decode("utf-8", errors="replace")


def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as source:
        return list(csv.reader(source, delimiter=";", strict=True))


def inspect(folder, expected, header, execution):
    code, stdout, stderr = execution
    problems = []

    def check(condition, message):
        if not condition:
            problems.append(message)

    check(code == expected["expected_exit_code"], "unexpected exit code")
    report = None
    try:
        report = json.loads((folder / "validation.json").read_text(encoding="utf-8"))
        check(type(report) is dict and set(report) == REPORT_KEYS, "unexpected JSON schema")
        check(report.get("schema_version") == 1, "unexpected JSON schema version")
        check(report.get("exit_code") == code, "JSON/process code mismatch")
        records = expected["expected_records"]
        failures = sum(row[-1] == "false" for row in records)
        decision = "rejected" if expected["expected_exit_code"] == 2 else (
            "failed_tests" if failures else "accepted")
        check(report.get("decision") == decision, "unexpected decision")
        check(report.get("published_records") == len(records), "unexpected published record count")
        check(report.get("failed_tests") == failures, "unexpected failed test count")
        check(report.get("csv_created") is expected["csv_expected"], "unexpected CSV flag")
        errors = report.get("errors", [])
        check(len(errors) == len(expected["expected_errors"]), "unexpected error count")
        for actual, wanted in zip(errors, expected["expected_errors"]):
            check(set(actual) == {"rule", "line", "message"}, "unexpected issue schema")
            check(actual.get("rule") == wanted["rule"], "unexpected error rule")
            check(actual.get("line") == wanted["line"], "unexpected error line")
            check(wanted["contains"] in actual.get("message", ""), "unexpected error message")
            check(f"[{wanted['rule']}]" in stderr, "missing stderr rule")
            if wanted["line"] is not None:
                check(f"line {wanted['line']}:" in stderr, "missing stderr line")
    except (OSError, ValueError, TypeError, AttributeError) as error:
        problems.append(f"invalid/missing JSON: {error}")
    output = folder / "results.csv"
    check(output.exists() == expected["csv_expected"], "unexpected CSV presence")
    if expected["csv_expected"]:
        try:
            check(output.read_bytes().startswith(b"\xef\xbb\xbf"), "missing CSV BOM")
            check(read_csv(output) == [header] + expected["expected_records"], "CSV values differ")
            check(not stderr, "unexpected stderr for accepted data")
            failures = sum(row[-1] == "false" for row in expected["expected_records"])
            check(stdout == f"ACCEPTED: {len(expected['expected_records'])} record(s), failed tests: {failures}\n",
                  "unexpected acceptance stdout")
        except (OSError, UnicodeError, csv.Error) as error:
            problems.append(f"cannot verify CSV: {error}")
    else:
        check(not stdout, "rejection printed success/stdout")
    check(not list(folder.glob(".tidpi-d-*.tmp")), "temporary output remains")
    return problems, report


def main():
    started = datetime.now(ZoneInfo("Europe/Warsaw"))
    run_id = started.strftime("%Y%m%d_%H%M%S_%f")
    run = ROOT / "wyniki" / run_id
    run.mkdir(parents=True, exist_ok=False)
    previous = frozen_previous()
    manifest = json.loads((ROOT / "fixtures/manifest.json").read_text(encoding="utf-8"))
    save_json(run / "criteria.json", manifest)
    save_json(run / "environment.json", {
        "recorded_at": started.isoformat(), "timezone": "Europe/Warsaw",
        "system": platform.system(), "macos": platform.mac_ver()[0],
        "machine": platform.machine(), "python": platform.python_version(),
        "int_max_str_digits": sys.get_int_max_str_digits(), "timeout_seconds": 10,
        "measurements": "none; synthetic contract fixtures",
    })
    version = subprocess.run(["python3", "--version"], capture_output=True, check=False, timeout=10)
    save_json(run / "python_check.json", {"command": ["python3", "--version"],
              "exit_code": version.returncode, "stdout": version.stdout.decode(),
              "stderr": version.stderr.decode()})
    tracked = [ROOT / "parse_results.py", ROOT / "run_fixtures.py", ROOT / "fixtures/manifest.json"]
    tracked += [ROOT / "fixtures" / fixture["file"] for fixture in manifest["fixtures"]]
    save_json(run / "source_fixture_sha256.json", {str(p.relative_to(ROOT)): sha(p) for p in tracked})
    outcomes = []
    clean_csv = None
    for expected in manifest["fixtures"]:
        folder = run / expected["id"]
        folder.mkdir()
        source = ROOT / "fixtures" / expected["file"]
        before = {"input_sha256": sha(source), "stale_csv_present": False}
        setup_problems = []
        if expected["expected_exit_code"] == 2:
            if clean_csv is None:
                setup_problems.append("first fixture did not provide verified CSV for stale-output test")
            else:
                (folder / "results.csv").write_bytes(clean_csv)
                before.update(stale_csv_present=True, stale_csv_sha256=sha(folder / "results.csv"))
        save_json(folder / "before.json", before)
        try:
            execution = execute(folder, source)
            problems, report = inspect(folder, expected, manifest["expected_header"], execution)
            problems = setup_problems + problems
            if sha(source) != before["input_sha256"]:
                problems.append("fixture input changed")
            if expected["id"] == "F01" and not problems:
                clean_csv = (folder / "results.csv").read_bytes()
            after = {"csv_present": (folder / "results.csv").exists(),
                     "input_unchanged": sha(source) == before["input_sha256"]}
            save_json(folder / "after.json", after)
        except Exception as error:
            # Błąd kontroli jednego przypadku nie zatrzymuje kolejnych prób.
            problems, report = setup_problems + [f"runner error: {type(error).__name__}: {error}"], None
        outcome = {"id": expected["id"], "fixture": expected["file"],
                   "expected_code": expected["expected_exit_code"],
                   "actual_code": int((folder / "parser_exit_code.txt").read_text())
                   if (folder / "parser_exit_code.txt").exists() else None,
                   "passed": not problems, "problems": problems}
        save_json(folder / "comparison.json", outcome)
        outcomes.append(outcome)

    # Dodatkowe scenariusze uruchomienia i I/O nie zastępują 18 plików fixture.
    extras = ["missing_input", "input_as_csv", "input_as_json", "symlink_as_csv",
              "hardlink_as_json", "csv_equals_json", "csv_write_error", "json_write_error"]
    for name in extras:
        folder = run / name
        folder.mkdir()
        problems = []
        input_path = folder / "input.txt"
        shutil.copyfile(ROOT / "fixtures" / manifest["fixtures"][0]["file"], input_path)
        input_hash = sha(input_path)
        output, report = "results.csv", "validation.json"
        if name == "missing_input":
            input_path.unlink()
            if clean_csv is not None:
                (folder / output).write_bytes(clean_csv)
        elif name == "input_as_csv":
            output = "input.txt"
        elif name == "input_as_json":
            report = "input.txt"
        elif name == "symlink_as_csv":
            (folder / "alias.txt").symlink_to("input.txt")
            output = "alias.txt"
        elif name == "hardlink_as_json":
            (folder / "alias.txt").hardlink_to(input_path)
            report = "alias.txt"
        elif name == "csv_equals_json":
            report = output
        elif name == "csv_write_error":
            output = "missing/results.csv"
        elif name == "json_write_error":
            report = "missing/validation.json"
        save_json(folder / "before.json", {"input_sha256": input_hash,
                  "input_exists": input_path.exists(), "output_argument": output,
                  "report_argument": report, "stale_csv_present": name == "missing_input" and clean_csv is not None})
        try:
            code, stdout, stderr = execute(folder, input_path, output, report)
            if code != 2 or stdout:
                problems.append("expected code 2 without success stdout")
            protected = name in {"input_as_csv", "input_as_json", "symlink_as_csv",
                                  "hardlink_as_json", "csv_equals_json"}
            if protected:
                if "[PATH]" not in stderr:
                    problems.append("missing PATH diagnostic")
                if sha(input_path) != input_hash:
                    problems.append("protected input changed")
                if (folder / "results.csv").exists() or (folder / "validation.json").exists():
                    problems.append("unsafe invocation created output")
            elif name == "json_write_error":
                if "[REPORT]" not in stderr or (folder / "results.csv").exists():
                    problems.append("JSON write failure did not roll back CSV")
            else:
                validation = json.loads((folder / "validation.json").read_text())
                rule = "READ" if name == "missing_input" else "OUTPUT"
                if validation["exit_code"] != 2 or validation["csv_created"] or validation["published_records"]:
                    problems.append("incorrect failure JSON")
                if validation["errors"][0]["rule"] != rule:
                    problems.append("incorrect I/O error rule")
                if (folder / output).exists():
                    problems.append("I/O rejection left CSV")
            if name != "missing_input" and sha(input_path) != input_hash:
                problems.append("input changed")
            if list(folder.rglob(".tidpi-d-*.tmp")):
                problems.append("temporary output remains")
        except Exception as error:
            problems.append(f"runner error: {type(error).__name__}: {error}")
        save_json(folder / "after.json", {"input_exists": input_path.exists(),
                  "input_unchanged": sha(input_path) == input_hash if input_path.exists() else None,
                  "csv_present": (folder / "results.csv").exists()})
        # Dowiązanie było fixture konfiguracji ścieżek, nie załącznikiem wynikowym.
        (folder / "alias.txt").unlink(missing_ok=True)
        outcome = {"id": name, "expected_code": 2,
                   "actual_code": int((folder / "parser_exit_code.txt").read_text())
                   if (folder / "parser_exit_code.txt").exists() else None,
                   "passed": not problems, "problems": problems}
        save_json(folder / "comparison.json", outcome)
        outcomes.append(outcome)
    current = frozen_previous()
    unchanged = current == previous
    save_json(run / "previous_integrity.json", {"all_unchanged": unchanged, "files": previous})
    save_json(run / "outcomes.json", outcomes)
    passed = sum(item["passed"] for item in outcomes)
    private_matches = []
    for path in run.rglob("*"):
        if path.is_file():
            text = path.read_text(encoding="utf-8")
            if "/Users/" in text or "/private/" in text:
                private_matches.append(str(path.relative_to(run)))
    save_json(run / "anonymization.json", {"checked": True, "private_path_matches": private_matches})
    code = 0 if passed == len(outcomes) and unchanged and version.returncode == 0 and not private_matches else 1
    save_json(run / "summary.json", {"fixture_count": len(manifest["fixtures"]),
              "extra_scenarios": len(extras), "total": len(outcomes), "passed": passed,
              "failed": len(outcomes) - passed, "previous_unchanged": unchanged, "anonymization_passed": not private_matches, "exit_code": code})
    (run / "runner_exit_code.txt").write_text(f"{code}\n", encoding="utf-8")
    print(f"{'PASS' if code == 0 else 'FAIL'}: wyniki/{run_id}; {passed}/{len(outcomes)} checks")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
