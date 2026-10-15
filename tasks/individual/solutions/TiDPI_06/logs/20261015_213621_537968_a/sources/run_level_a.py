"""Odtwórz lokalny poziom A; każdy przebieg ma własne źródła, dane i logi.

Uruchomienie z dowolnego katalogu: python3 run_level_a.py
Kopie wyników w katalogu zadania powstają tylko, jeśli jeszcze nie istnieją.
"""

import csv
import hashlib
import io
import json
import platform
import shutil
import statistics
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent
HEADER = ["case", "size", "trial", "time_us", "comparisons", "correct"]
CRITERIA = """Kryteria zapisane przed kompilacją i pomiarami:
TC-A01: Release C++17 -O2 -DNDEBUG, kompilator i producent kończą się kodem 0.
TC-A02: surowy protokół TIDPI_RESULTS;1 i dokładny nagłówek v1.
TC-A03: 18 unikalnych rekordów: sorted/reversed/random x 16/32 x próby 1/2/3.
TC-A04: pełne porównanie z std::sort w C++; wszystkie correct=true.
TC-A05: parser kończy się kodem 0 i zachowuje wszystkie wartości.
TC-A06: oba CSV mają UTF-8 BOM, separator ;, 6 pól i identyczną treść.
TC-A07: liczby bez jednostek; sorted comparisons=n-1; reversed=n*(n-1)/2.
TC-A08: kontrola tekstowa CSV i ponowny niezależny odczyt modułem csv.
TC-A09: istniejące testy parsera przechodzą; fixture to dane sztuczne.
Excel: niewykonane, ograniczona dostępność aplikacji w używanym środowisku.
Czasy nie są konkursem wydajności; rotacja układów między próbami.
"""


def save(path, text):
    path.write_text(text, encoding="utf-8")


def invoke(command, cwd, evidence, name, timeout=60):
    save(evidence / f"{name}_command.json", json.dumps(command, ensure_ascii=False) + "\n")
    try:
        result = subprocess.run(
            command, cwd=cwd, shell=False, capture_output=True, check=False, timeout=timeout,
        )
        stdout, stderr, code = result.stdout, result.stderr, result.returncode
    except subprocess.TimeoutExpired as error:
        stdout, stderr, code = error.stdout or b"", (error.stderr or b"") + b"\nTIMEOUT\n", 124
    except OSError as error:
        stdout, stderr, code = b"", str(error).encode("utf-8"), 2
    (evidence / f"{name}_stdout.txt").write_bytes(stdout)
    (evidence / f"{name}_stderr.txt").write_bytes(stderr)
    save(evidence / f"{name}_exit_code.txt", f"{code}\n")
    if code:
        raise RuntimeError(f"{name}: exit code {code}; see preserved logs")
    return stdout


def verify(evidence):
    """Oddzielna kontrola zbioru; nie importuje funkcji badanego parsera."""
    raw = (evidence / "raw_output.txt").read_text(encoding="utf-8")
    raw_rows = list(csv.reader(io.StringIO(raw), delimiter=";", strict=True))
    assert raw_rows[0] == ["TIDPI_RESULTS", "1"]
    assert raw_rows[1] == HEADER
    datasets = []
    for name in ("results.csv", "results_verified.csv"):
        data = (evidence / name).read_bytes()
        assert data.startswith(b"\xef\xbb\xbf"), name
        with (evidence / name).open(encoding="utf-8-sig", newline="") as source:
            rows = list(csv.reader(source, delimiter=";", strict=True))
        assert rows[0] == HEADER
        assert rows[1:] == raw_rows[2:]
        datasets.append(rows)
    assert datasets[0] == datasets[1]
    rows = datasets[0][1:]
    assert len(rows) == 18 and all(len(row) == 6 for row in rows)
    expected = {(case, size, trial) for case in ("sorted", "reversed", "random")
                for size in (16, 32) for trial in (1, 2, 3)}
    identities = []
    groups = {}
    for case, size, trial, time_us, comparisons, correct in rows:
        assert all(value.isascii() and value.isdecimal()
                   for value in (size, trial, time_us, comparisons))
        size, trial, time_us, comparisons = map(int, (size, trial, time_us, comparisons))
        assert correct == "true" and size >= 2 and trial >= 1
        assert time_us >= 0 and 0 <= comparisons <= size * (size - 1) // 2
        if case == "sorted":
            assert comparisons == size - 1
        if case == "reversed":
            assert comparisons == size * (size - 1) // 2
        identities.append((case, size, trial))
        groups.setdefault((case, size), []).append(time_us)
    assert len(set(identities)) == 18 and set(identities) == expected
    summary = []
    for (case, size), times in groups.items():
        summary.append(dict(case=case, size=size, trials=times, minimum=min(times),
                            maximum=max(times), range=max(times)-min(times),
                            median=statistics.median(times)))
    save(evidence / "summary.json", json.dumps(summary, indent=2) + "\n")
    save(evidence / "verification.txt", """TC-A02=PASS protocol and header
TC-A03=PASS records=18 unique=18 expected_identities=18
TC-A04=PASS correct_true=18 correct_false=0
TC-A05=PASS parser output matches all raw fields
TC-A06=PASS BOM=true delimiter=; fields=6 datasets_equal=true
TC-A07=PASS numeric_fields_without_units=true expected_comparisons=true
TC-A08=PASS independent csv reread; text editor review recorded separately
summary_groups=6 trials_per_group=3
excel_import=not_performed
""")


def main():
    started = datetime.now(ZoneInfo("Europe/Warsaw"))
    run_id = started.strftime("%Y%m%d_%H%M%S_%f") + "_a"
    evidence = ROOT / "logs" / run_id
    evidence.mkdir(parents=True, exist_ok=False)
    build = ROOT / "_build" / run_id
    build.mkdir(parents=True, exist_ok=False)
    save(evidence / "criteria.txt", CRITERIA)
    save(evidence / "started_at.txt", started.isoformat() + "\n")
    sources = evidence / "sources"
    sources.mkdir()
    for name in ("main.cpp", "main.py", "test_main.py", "run_level_a.py"):
        shutil.copyfile(ROOT / name, sources / name)
    hashes = {path.name: hashlib.sha256(path.read_bytes()).hexdigest()
              for path in sources.iterdir()}
    save(evidence / "source_sha256.json", json.dumps(hashes, indent=2) + "\n")
    try:
        compiler = invoke(["clang++", "--version"], ROOT, evidence, "compiler_version")
        os_version = invoke(["sw_vers", "-productVersion"], ROOT, evidence, "os_version")
        os_build = invoke(["sw_vers", "-buildVersion"], ROOT, evidence, "os_build")
        # Pełny stdout clang --version zawiera prywatną ścieżkę instalacji.
        # Zatrzymujemy go lokalnie poza załącznikami; do metryczki bierzemy dwie linie.
        shutil.move(evidence / "compiler_version_stdout.txt", build / "compiler_version_private.txt")
        save(evidence / "compiler_version_stdout_note.txt",
             "Full compiler version stdout kept privately in ignored _build/; "
             "environment.txt contains only compiler identity and target.\n")
        save(evidence / "environment.txt", "\n".join([
            f"recorded_at={started.isoformat()}", "timezone=Europe/Warsaw",
            f"host=macOS {os_version.decode().strip()}", f"build={os_build.decode().strip()}",
            f"arch={platform.machine()}", f"python={platform.python_version()}",
            *compiler.decode().splitlines()[:2],
            "configuration=Release; C++17; -O2 -DNDEBUG -Wall -Wextra -pedantic",
            "debugger=not_attached", "excel_import=not_performed",
        ]) + "\n")
        executable = f"_build/{run_id}/tidpi06"
        invoke(["clang++", "-std=c++17", "-O2", "-DNDEBUG", "-Wall", "-Wextra", "-pedantic",
                f"logs/{run_id}/sources/main.cpp", "-o", executable], ROOT, evidence, "compile")
        invoke([f"../../{executable}", "--clock-info"], evidence, evidence, "clock")
        raw = invoke([f"../../{executable}"], evidence, evidence, "producer")
        (evidence / "raw_output.txt").write_bytes(raw)
        invoke(["python3", "-B", f"logs/{run_id}/sources/main.py", f"logs/{run_id}/raw_output.txt",
                f"logs/{run_id}/results_verified.csv"], ROOT, evidence, "parser")
        verify(evidence)
        invoke(["python3", "-B", "-m", "unittest", "discover", "-s",
                f"logs/{run_id}/sources", "-p", "test_main.py", "-v"], ROOT, evidence, "tests")
        for name in ("raw_output.txt", "results.csv", "results_verified.csv"):
            destination = ROOT / name
            if not destination.exists():
                with destination.open("xb") as target:
                    target.write((evidence / name).read_bytes())
        save(evidence / "status.txt", "local_checks=passed\nexcel_import=not_performed\n")
        print(f"PASS: logs/{run_id}; 18 records; Excel import not performed")
        return 0
    except (RuntimeError, AssertionError, OSError, UnicodeError, csv.Error) as error:
        save(evidence / "status.txt", f"local_checks=failed\nreason={error}\n")
        print(f"FAIL: logs/{run_id}: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
