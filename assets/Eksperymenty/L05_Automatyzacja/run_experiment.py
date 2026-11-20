"""Skompiluj eksperyment C++, uruchom go i zachowaj dowody z obu etapów."""

import argparse
import datetime
import locale
import shutil
import subprocess
import time
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
SOURCE = Path("main.cpp")
BUILD_DIR = Path("_build")
PROGRAM = BUILD_DIR / "experiment.exe"
EVIDENCE_ROOT = PROJECT_DIR / "logs"


def decode_output(data):
    """Odczytaj wynik narzędzi, które mogą używać różnych kodowań znaków.

    Args:
        data: Bajty przechwycone ze standardowego wyjścia albo wyjścia błędów.

    Returns:
        Odczytany tekst. Niepoprawne bajty są zastępowane dopiero po
        sprawdzeniu kodowań typowych dla używanych narzędzi Windows.
    """
    if not data:
        return ""

    encodings = ("utf-8", locale.getpreferredencoding(False), "cp852")
    for encoding in dict.fromkeys(encodings):
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            pass

    return data.decode("utf-8", errors="replace")


def save_text(path, content):
    """Ujednolić końce wierszy i zastąpić plik tekstowy UTF-8.

    Args:
        path: Ścieżka pliku docelowego.
        content: Tekst, który ma zostać ujednolicony i zapisany.
    """
    normalized = content.replace("\r\n", "\n").replace("\r", "\n")
    path.write_text(normalized, encoding="utf-8")


def save_summary(path, values):
    """Zapisać dowody jako uporządkowane pary klucz-wartość.

    Args:
        path: Ścieżka pliku docelowego.
        values: Mapa, której kolejność dodawania ustala kolejność wierszy.
    """
    lines = [f"{key}={value}" for key, value in values.items()]
    save_text(path, "\n".join(lines) + "\n")


def run_process(command, timeout_seconds):
    """Uruchomić polecenie, przechwycić dowody i pilnować limitu czasu.

    Args:
        command: Lista argumentów przekazywana bezpośrednio procesowi potomnemu.
        timeout_seconds: Maksymalny czas działania w sekundach.

    Returns:
        Kod wyjścia, bajty stdout i stderr, czas w milisekundach oraz
        informacja o przekroczeniu czasu. Kod 124 oznacza timeout.
    """
    start = time.perf_counter()

    try:
        completed = subprocess.run(
            command,
            cwd=PROJECT_DIR,
            capture_output=True,
            shell=False,
            timeout=timeout_seconds,
            check=False,
        )
        elapsed_ms = (time.perf_counter() - start) * 1000
        return completed.returncode, completed.stdout, completed.stderr, elapsed_ms, False
    except subprocess.TimeoutExpired as error:
        elapsed_ms = (time.perf_counter() - start) * 1000
        return 124, error.stdout or b"", error.stderr or b"", elapsed_ms, True


def main():
    """Skompilować i uruchomić wybrany przypadek oraz zwrócić jego status."""
    parser = argparse.ArgumentParser(description="Compile, run and register evidence from a C++ experiment.")
    parser.add_argument(
        "--configuration",
        choices=("debug", "release"),
        default="release",
    )
    parser.add_argument(
        "--case",
        choices=("pass", "fail"),
        default="pass",
    )
    args = parser.parse_args()

    # Dodajemy mikrosekundy, aby dwa szybko wykonane uruchomienia nie zapisały
    # dowodów w tym samym katalogu i nie nadpisały swoich wyników.
    run_id = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    evidence_dir = EVIDENCE_ROOT / run_id
    evidence_dir.mkdir(parents=True)
    (PROJECT_DIR / BUILD_DIR).mkdir(exist_ok=True)

    summary = {
        "run_id": run_id,
        "configuration": args.configuration,
        "case": args.case,
        "compile_exit_code": "not_started",
        "execution_attempted": "false",
        "run_exit_code": "not_started",
        "final_status": "started",
    }

    if shutil.which("cl") is None:
        # Brak cl.exe oznacza źle przygotowane środowisko, a nie błąd badanego programu.
        # Rozróżnienie tych sytuacji zapobiega niesprawiedliwemu wynikowi testu.
        summary["final_status"] = "environment_error"
        save_summary(evidence_dir / "summary.txt", summary)
        print("ERROR: cl.exe not found.")
        print("Run this script from Developer PowerShell for VS 2022.")
        return 2

    program_path = PROJECT_DIR / PROGRAM
    # Usuwamy stary plik EXE, aby po nieudanej kompilacji nie uruchomić przypadkiem
    # programu pozostałego z poprzedniej, udanej próby.
    program_path.unlink(missing_ok=True)

    # Przekazujemy argumenty jako listę i nie uruchamiamy powłoki. Python nie musi
    # wtedy interpretować cudzysłowów ani znaków specjalnych polecenia.
    compile_command = [
        "cl",
        "/nologo",
        "/std:c++17",
        "/EHsc",
        "/W4",
        "/permissive-",
        "/utf-8",
        str(SOURCE),
        f"/Fe:{PROGRAM}",
        f"/Fo:{BUILD_DIR / 'main.obj'}",
    ]

    if args.configuration == "release":
        compile_command.extend(("/O2", "/MD"))
    else:
        compile_command.extend(("/Od", "/MDd"))

    summary["compile_command"] = subprocess.list2cmdline(compile_command)
    compile_code, compile_stdout, compile_stderr, compile_ms, compile_timeout = run_process(
        compile_command, timeout_seconds=60
    )
    save_text(evidence_dir / "compile_stdout.txt", decode_output(compile_stdout))
    save_text(evidence_dir / "compile_stderr.txt", decode_output(compile_stderr))
    summary["compile_exit_code"] = compile_code
    summary["compile_time_ms"] = f"{compile_ms:.3f}"
    summary["compile_timeout"] = str(compile_timeout).lower()

    # Sama wartość 0 nie wystarcza: sprawdzamy też, czy powstał plik EXE. Dzięki temu
    # uszkodzone narzędzie lub nietypowa konfiguracja nie zgłosi fałszywego sukcesu.
    if compile_code != 0 or not program_path.exists():
        summary["final_status"] = "compile_failed"
        save_summary(evidence_dir / "summary.txt", summary)
        print(f"COMPILE FAILED. Evidence: logs/{run_id}")
        return compile_code if compile_code != 0 else 1

    run_command = [str(PROGRAM)]
    if args.case == "fail":
        run_command.append("--simulate-failure")

    summary["execution_attempted"] = "true"
    summary["run_command"] = subprocess.list2cmdline(run_command)
    run_code, run_stdout, run_stderr, run_ms, run_timeout = run_process(
        run_command,
        timeout_seconds=10,
    )
    save_text(evidence_dir / "run_stdout.txt", decode_output(run_stdout))
    save_text(evidence_dir / "run_stderr.txt", decode_output(run_stderr))
    summary["run_exit_code"] = run_code
    summary["run_time_ms"] = f"{run_ms:.3f}"
    summary["run_timeout"] = str(run_timeout).lower()
    summary["final_status"] = "passed" if run_code == 0 else "run_failed"
    save_summary(evidence_dir / "summary.txt", summary)

    print(f"{summary['final_status'].upper()}. Evidence: logs/{run_id}")
    return run_code


if __name__ == "__main__":
    raise SystemExit(main())
