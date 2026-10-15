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
SIZE_MIN = 1
SIZE_MAX = 10000
ALLOWED_CONFIGURATIONS = frozenset({"debug", "release"})
ALLOWED_CASES = frozenset({"pass", "fail"})


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
        return (
            completed.returncode,
            completed.stdout,
            completed.stderr,
            elapsed_ms,
            False,
        )
    except subprocess.TimeoutExpired as error:
        elapsed_ms = (time.perf_counter() - start) * 1000
        return 124, error.stdout or b"", error.stderr or b"", elapsed_ms, True


def format_command(command):
    """Czytelna postać listy argumentów (Windows list2cmdline lub join)."""
    if hasattr(subprocess, "list2cmdline"):
        return subprocess.list2cmdline(command)
    return " ".join(command)


def build_compile_command(configuration):
    """Zbudować listę argumentów kompilacji: MSVC cl albo clang++.

    Returns:
        Para (backend, command) albo (None, None), gdy brak kompilatora.
    """
    if shutil.which("cl") is not None:
        command = [
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
        if configuration == "release":
            command.extend(("/O2", "/MD"))
        else:
            command.extend(("/Od", "/MDd"))
        return "cl", command

    if shutil.which("clang++") is not None:
        command = [
            "clang++",
            "-std=c++17",
            "-Wall",
            "-Wextra",
            "-pedantic",
            "-o",
            str(PROGRAM),
            str(SOURCE),
        ]
        if configuration == "release":
            command[1:1] = ["-O2", "-DNDEBUG"]
        else:
            command[1:1] = ["-O0", "-g", "-D_DEBUG"]
        return "clang++", command

    return None, None


def resolve_config_path(raw_path):
    """Rozwiązać ścieżkę config i odrzucić wyjście poza PROJECT_DIR.

    Args:
        raw_path: Ścieżka względna lub bezwzględna podana przez użytkownika.

    Returns:
        Para (Path albo None, komunikat błędu albo None).
    """
    candidate = Path(raw_path)
    if not candidate.is_absolute():
        candidate = PROJECT_DIR / candidate
    resolved = candidate.resolve()
    try:
        resolved.relative_to(PROJECT_DIR)
    except ValueError:
        return None, "config path escapes project directory"
    if not resolved.is_file():
        return None, "config file does not exist"
    return resolved, None


def load_and_validate_config(config_path):
    """Wczytać YAML przez safe_load i zweryfikować wymagane pola.

    Args:
        config_path: Ścieżka do pliku już zweryfikowana względem PROJECT_DIR.

    Returns:
        Para (dict parametrów albo None, komunikat błędu albo None).
        Dict zawiera: configuration, case, repeat, size (size może być None).
    """
    try:
        import yaml
    except ImportError:
        return None, "PyYAML is not installed (pip install -r requirements.txt)"

    try:
        text = config_path.read_text(encoding="utf-8")
    except OSError as error:
        return None, f"cannot read config: {error}"

    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as error:
        return None, f"YAML parse error: {error}"

    if not isinstance(data, dict):
        return None, "config root must be a mapping"

    if "configuration" not in data:
        return None, "missing required field: configuration"
    if "case" not in data:
        return None, "missing required field: case"

    configuration = data["configuration"]
    case = data["case"]
    if not isinstance(configuration, str) or configuration not in ALLOWED_CONFIGURATIONS:
        return None, "configuration must be 'debug' or 'release'"
    if not isinstance(case, str) or case not in ALLOWED_CASES:
        return None, "case must be 'pass' or 'fail'"

    repeat = data.get("repeat", 1)
    if not isinstance(repeat, int) or isinstance(repeat, bool):
        return None, "repeat must be an integer from 1 to 10"
    if repeat < 1 or repeat > 10:
        return None, "repeat must be an integer from 1 to 10"

    size = data.get("size", None)
    if size is not None:
        if not isinstance(size, int) or isinstance(size, bool):
            return None, f"size must be null or an integer from {SIZE_MIN} to {SIZE_MAX}"
        if size < SIZE_MIN or size > SIZE_MAX:
            return None, f"size must be null or an integer from {SIZE_MIN} to {SIZE_MAX}"

    unknown = set(data) - {"configuration", "case", "repeat", "size"}
    if unknown:
        return None, f"unknown config fields: {sorted(unknown)}"

    return {
        "configuration": configuration,
        "case": case,
        "repeat": repeat,
        "size": size,
    }, None


def relative_config_display(config_path):
    """Ścieżka względna do projektu (bez nazwy konta użytkownika)."""
    try:
        return config_path.relative_to(PROJECT_DIR).as_posix()
    except ValueError:
        return config_path.name


def main():
    """Skompilować i uruchomić wybrany przypadek oraz zwrócić jego status."""
    parser = argparse.ArgumentParser(
        description="Compile, run and register evidence from a C++ experiment."
    )
    parser.add_argument(
        "--config",
        default=None,
        help="YAML config under project dir (when set, run params come from file).",
    )
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
    parser.add_argument(
        "--repeat",
        type=int,
        default=1,
        help="Number of program runs to record (1..10).",
    )
    parser.add_argument(
        "--size",
        type=int,
        default=None,
        help=f"Pass --size to the program ({SIZE_MIN}..{SIZE_MAX}).",
    )
    args = parser.parse_args()

    # Dodajemy mikrosekundy, aby dwa szybko wykonane uruchomienia nie zapisały
    # dowodów w tym samym katalogu i nie nadpisały swoich wyników.
    run_id = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    evidence_dir = EVIDENCE_ROOT / run_id
    evidence_dir.mkdir(parents=True)
    (PROJECT_DIR / BUILD_DIR).mkdir(exist_ok=True)

    configuration = args.configuration
    case = args.case
    repeat = args.repeat
    size = args.size
    config_loaded = False
    config_display = ""

    if args.config is not None:
        # Przy --config parametry biegu pochodzą wyłącznie z YAML (bez mieszania CLI).
        resolved, path_error = resolve_config_path(args.config)
        config_display = args.config
        if path_error is not None:
            summary = {
                "run_id": run_id,
                "config_path": config_display,
                "config_loaded": "false",
                "compile_exit_code": "not_started",
                "execution_attempted": "false",
                "run_exit_code": "not_started",
                "final_status": "config_error",
                "config_error": path_error,
            }
            save_summary(evidence_dir / "summary.txt", summary)
            print(f"ERROR: {path_error}")
            print(f"CONFIG ERROR. Evidence: logs/{run_id}")
            return 2

        config_display = relative_config_display(resolved)
        params, config_error = load_and_validate_config(resolved)
        if config_error is not None:
            summary = {
                "run_id": run_id,
                "config_path": config_display,
                "config_loaded": "false",
                "compile_exit_code": "not_started",
                "execution_attempted": "false",
                "run_exit_code": "not_started",
                "final_status": "config_error",
                "config_error": config_error,
            }
            save_summary(evidence_dir / "summary.txt", summary)
            print(f"ERROR: {config_error}")
            print(f"CONFIG ERROR. Evidence: logs/{run_id}")
            return 2

        configuration = params["configuration"]
        case = params["case"]
        repeat = params["repeat"]
        size = params["size"]
        config_loaded = True

    summary = {
        "run_id": run_id,
        "configuration": configuration,
        "case": case,
        "repeat": repeat,
        "size": "default" if size is None else size,
        "compile_exit_code": "not_started",
        "execution_attempted": "false",
        "run_exit_code": "not_started",
        "final_status": "started",
    }
    if args.config is not None:
        summary["config_path"] = config_display
        summary["config_loaded"] = "true" if config_loaded else "false"

    if repeat < 1 or repeat > 10:
        summary["final_status"] = "validation_failed"
        summary["validation_error"] = "repeat out of range [1, 10]"
        save_summary(evidence_dir / "summary.txt", summary)
        print("ERROR: --repeat must be an integer from 1 to 10.")
        print(f"VALIDATION FAILED. Evidence: logs/{run_id}")
        return 2

    backend, compile_command = build_compile_command(configuration)
    if backend is None:
        # Brak kompilatora oznacza źle przygotowane środowisko, a nie błąd
        # badanego programu.
        summary["final_status"] = "environment_error"
        summary["compiler_backend"] = "none"
        save_summary(evidence_dir / "summary.txt", summary)
        print("ERROR: neither cl.exe nor clang++ found.")
        print("On Windows: run from Developer PowerShell for VS 2022.")
        print("On macOS/Linux: install a C++17 compiler (clang++ / g++).")
        return 2

    summary["compiler_backend"] = backend
    program_path = PROJECT_DIR / PROGRAM
    # Usuwamy stary plik EXE, aby po nieudanej kompilacji nie uruchomić
    # przypadkiem programu pozostałego z poprzedniej, udanej próby.
    program_path.unlink(missing_ok=True)

    summary["compile_command"] = format_command(compile_command)
    compile_code, compile_stdout, compile_stderr, compile_ms, compile_timeout = (
        run_process(compile_command, timeout_seconds=60)
    )
    save_text(evidence_dir / "compile_stdout.txt", decode_output(compile_stdout))
    save_text(evidence_dir / "compile_stderr.txt", decode_output(compile_stderr))
    summary["compile_exit_code"] = compile_code
    summary["compile_time_ms"] = f"{compile_ms:.3f}"
    summary["compile_timeout"] = str(compile_timeout).lower()

    # Sama wartość 0 nie wystarcza: sprawdzamy też, czy powstał plik EXE.
    if compile_code != 0 or not program_path.exists():
        summary["final_status"] = "compile_failed"
        save_summary(evidence_dir / "summary.txt", summary)
        print(f"COMPILE FAILED. Evidence: logs/{run_id}")
        return compile_code if compile_code != 0 else 1

    # Walidacja --size po kompilacji, przed uruchomieniem programu.
    if size is not None and (size < SIZE_MIN or size > SIZE_MAX):
        summary["final_status"] = "validation_failed"
        summary["validation_error"] = (
            f"size out of range [{SIZE_MIN}, {SIZE_MAX}]"
        )
        summary["execution_attempted"] = "false"
        save_summary(evidence_dir / "summary.txt", summary)
        print(
            f"ERROR: --size must be an integer from {SIZE_MIN} to {SIZE_MAX}."
        )
        print(f"VALIDATION FAILED. Evidence: logs/{run_id}")
        return 2

    run_command = [str(PROGRAM)]
    if size is not None:
        run_command.extend(["--size", str(size)])
    if case == "fail":
        run_command.append("--simulate-failure")

    summary["execution_attempted"] = "true"
    summary["run_command"] = format_command(run_command)

    all_passed = True
    last_code = 0
    total_run_ms = 0.0
    any_timeout = False

    # Nie przerywamy po pierwszej awarii — każda próba dostaje własne pliki.
    for index in range(1, repeat + 1):
        label = f"{index:02d}"
        run_code, run_stdout, run_stderr, run_ms, run_timeout = run_process(
            run_command,
            timeout_seconds=10,
        )
        save_text(
            evidence_dir / f"run_{label}_stdout.txt",
            decode_output(run_stdout),
        )
        save_text(
            evidence_dir / f"run_{label}_stderr.txt",
            decode_output(run_stderr),
        )
        summary[f"run_{label}_exit_code"] = run_code
        summary[f"run_{label}_time_ms"] = f"{run_ms:.3f}"
        summary[f"run_{label}_timeout"] = str(run_timeout).lower()
        last_code = run_code
        total_run_ms += run_ms
        any_timeout = any_timeout or run_timeout
        if run_code != 0:
            all_passed = False

    summary["run_exit_code"] = last_code
    summary["run_time_ms"] = f"{total_run_ms:.3f}"
    summary["run_timeout"] = str(any_timeout).lower()
    summary["final_status"] = "passed" if all_passed else "run_failed"
    save_summary(evidence_dir / "summary.txt", summary)
    print(f"{summary['final_status'].upper()}. Evidence: logs/{run_id}")
    return 0 if all_passed else last_code if last_code != 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
