"""Sequential, validated benchmark of the C++ and Python word counters."""

import argparse
import csv
import hashlib
import json
import os
import platform
import re
import subprocess
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FLAGS = ["-std=c++17", "-O2", "-Wall", "-Wextra", "-Wpedantic"]
TIMEOUT = 30
OUTPUT = re.compile(r"Ilość znalezionych słów: ([0-9]+); \(czas: ([0-9]+) ns\)\n")
FIELDS = [
    "language",
    "data_id",
    "sha256",
    "size_bytes",
    "variant",
    "trial",
    "position",
    "elapsed",
    "unit",
    "expected_words",
    "actual_words",
    "status",
    "reason",
]


def timestamp():
    return datetime.now(timezone.utc).isoformat()


def write_json(path, value):
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def load_datasets(data_dir):
    datasets = []
    seen = set()
    manifests = sorted(data_dir.rglob("manifest.json"))
    if not manifests:
        raise ValueError("Nie znaleziono manifestow danych.")
    for manifest_path in manifests:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        for entry in manifest["files"]:
            path = (manifest_path.parent / entry["file"]).resolve()
            data_id = path.relative_to(data_dir.resolve()).as_posix()
            if data_id in seen:
                raise ValueError(f"Powtorzony identyfikator danych: {data_id}")
            seen.add(data_id)
            data = path.read_bytes()
            data.decode("ascii")
            if len(data) != entry["size_bytes"] or sha256(data) != entry["sha256"]:
                raise ValueError(f"Niezgodny rozmiar lub SHA-256: {data_id}")
            if type(entry["expected_words"]) is not int or entry["expected_words"] < 0:
                raise ValueError(f"Niepoprawna oczekiwana liczba slow: {data_id}")
            datasets.append(
                {
                    "path": path,
                    "data_id": data_id,
                    "sha256": entry["sha256"],
                    "size_bytes": len(data),
                    "variant": entry["variant"],
                    "expected_words": entry["expected_words"],
                }
            )
    if not datasets:
        raise ValueError("Manifesty nie zawieraja plikow.")
    return sorted(datasets, key=lambda item: (item["size_bytes"], item["data_id"]))


def as_text(value):
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return value or ""


def measure(command, expected, timeout=TIMEOUT):
    row = {"elapsed": "", "actual_words": "", "status": "runtime_error", "reason": ""}
    diagnostic = {"stdout": "", "stderr": ""}
    try:
        process = subprocess.run(command, capture_output=True, timeout=timeout)
        diagnostic = {
            "stdout": as_text(process.stdout),
            "stderr": as_text(process.stderr),
            "returncode": process.returncode,
        }
        match = OUTPUT.fullmatch(diagnostic["stdout"])
        if match:
            row.update(actual_words=int(match[1]), elapsed=int(match[2]))
        if process.returncode != 0:
            row["reason"] = f"Kod zakonczenia: {process.returncode}"
        elif not match or diagnostic["stderr"]:
            row.update(status="invalid_output", reason="Niepoprawny format stdout lub niepusty stderr")
        elif row["actual_words"] != expected:
            row.update(status="wrong_result", reason=f"Oczekiwano {expected}, otrzymano {row['actual_words']}")
        else:
            row.update(status="valid")
    except subprocess.TimeoutExpired as error:
        row.update(status="timeout", reason=f"Przekroczono limit {timeout} s")
        diagnostic = {"stdout": as_text(error.stdout), "stderr": as_text(error.stderr)}
    except OSError as error:
        row["reason"] = str(error)
    return row, diagnostic


def compile_cpp(compiler, binary, root, log):
    command = [compiler, *FLAGS, "source/cpp/main.cpp", "-o", os.path.relpath(binary, root)]
    # Never reuse an output, even if this helper is called outside a fresh run.
    binary.unlink(missing_ok=True)
    try:
        result = subprocess.run(command, cwd=root, capture_output=True, timeout=120)
        log.write_bytes(result.stdout + result.stderr)
        if result.returncode != 0 or not binary.is_file():
            raise RuntimeError("Kompilacja nie powiodla sie; zobacz compilation.log")
    except (OSError, subprocess.TimeoutExpired) as error:
        log.write_text(str(error) + "\n", encoding="utf-8")
        raise RuntimeError("Nie udalo sie uruchomic lub zakonczyc kompilacji") from error
    return command


def version(command):
    result = subprocess.run(command, capture_output=True, text=True, timeout=TIMEOUT, check=True)
    return result.stdout.strip()


def cpu_info():
    if sys.platform == "darwin":
        try:
            return version(["sysctl", "-n", "machdep.cpu.brand_string"])
        except (OSError, subprocess.SubprocessError):
            pass
    if Path("/proc/cpuinfo").is_file():
        for line in Path("/proc/cpuinfo").read_text().splitlines():
            if line.startswith("model name"):
                return line.partition(":")[2].strip()
    return platform.processor() or "unavailable"


def summarize(datasets, repetitions, counts, status, error=""):
    pairs = []
    for data in datasets:
        for language in ("cpp", "python"):
            totals = counts[(data["data_id"], language)]
            pairs.append({"data_id": data["data_id"], "language": language, "planned": repetitions, **totals})
    return {
        "status": status,
        "error": error,
        "finished_at_utc": timestamp(),
        "planned": len(pairs) * repetitions,
        "executed": sum(pair["executed"] for pair in pairs),
        "valid": sum(pair["valid"] for pair in pairs),
        "rejected": sum(pair["rejected"] for pair in pairs),
        "pairs": pairs,
    }


def run(args, root=ROOT):
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "_" + uuid.uuid4().hex[:10]
    run_dir = output_dir / run_id
    run_dir.mkdir(exist_ok=False)
    print(f"Katalog przebiegu: {run_dir}", flush=True)
    metadata = {
        "started_at_utc": timestamp(),
        "status": "running",
        "repetitions": args.repetitions,
        "warmups": 0,
        "timeout_seconds": TIMEOUT,
        "unit": "ns",
        "order": "per file: odd trial cpp/python, even trial python/cpp; sequential fresh processes",
        "measurement": "algorithm and word-count result only; excludes process startup and IO",
        "system": platform.platform(),
        "architecture": platform.machine(),
        "cpu": cpu_info(),
        "logical_cpus": os.cpu_count(),
        "python_version": sys.version,
        "python_executable": sys.executable,
        "compiler": args.compiler,
        "compiler_flags": FLAGS,
    }
    datasets, counts = [], {}
    status, error = "failed", ""
    exit_code = 1
    try:
        write_json(run_dir / "metadata.json", metadata)
        datasets = load_datasets(args.data_dir)
        counts = {
            (data["data_id"], language): {"executed": 0, "valid": 0, "rejected": 0}
            for data in datasets
            for language in ("cpp", "python")
        }
        metadata["datasets"] = [{k: v for k, v in data.items() if k != "path"} for data in datasets]
        sources = ["source/cpp/main.cpp", "source/python/main.py", Path(__file__).name]
        metadata["source_sha256"] = {name: sha256((root / name).read_bytes()) for name in sources}
        binary = run_dir / "word-counter"
        metadata["compile_command"] = [
            args.compiler,
            *FLAGS,
            "source/cpp/main.cpp",
            "-o",
            os.path.relpath(binary, root),
        ]
        write_json(run_dir / "metadata.json", metadata)
        compile_cpp(args.compiler, binary, root, run_dir / "compilation.log")
        metadata["compiler_version"] = version([args.compiler, "--version"])
        cpp_clock = json.loads(version([str(binary), "--clock-info"]))
        python_clock = vars(time.get_clock_info("perf_counter"))
        if not cpp_clock["monotonic"] or not python_clock["monotonic"]:
            raise ValueError("Zegar nie jest monotoniczny")
        metadata["clocks"] = {"cpp": cpp_clock, "python": python_clock}
        metadata["clock_note"] = (
            "ns is output unit; C++ period is nominal, Python resolution is declared; neither guarantees accuracy"
        )
        write_json(run_dir / "metadata.json", metadata)
        commands = {"cpp": [str(binary)], "python": [sys.executable, "-B", str(root / "source/python/main.py")]}
        with (run_dir / "measurements.csv").open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=FIELDS)
            writer.writeheader()
            stream.flush()
            for data in datasets:
                for trial in range(1, args.repetitions + 1):
                    order = ("cpp", "python") if trial % 2 else ("python", "cpp")
                    for position, language in enumerate(order, 1):
                        result, diagnostic = measure([*commands[language], str(data["path"])], data["expected_words"])
                        row = {
                            key: data[key] for key in ("data_id", "sha256", "size_bytes", "variant", "expected_words")
                        }
                        row.update(language=language, trial=trial, position=position, unit="ns", **result)
                        writer.writerow(row)
                        stream.flush()
                        totals = counts[(data["data_id"], language)]
                        totals["executed"] += 1
                        totals["valid" if result["status"] == "valid" else "rejected"] += 1
                        if result["status"] != "valid":
                            with (run_dir / "errors.jsonl").open("a", encoding="utf-8") as errors:
                                errors.write(json.dumps({**row, **diagnostic}, ensure_ascii=False) + "\n")
                print(f"Zakonczono: {data['data_id']}", flush=True)
        if all(item["valid"] == args.repetitions for item in counts.values()):
            status, exit_code = "complete", 0
        else:
            status = "completed_with_rejections"
            error = "Nie wszystkie zaplanowane proby sa poprawne."
    except KeyboardInterrupt:
        status, error, exit_code = "interrupted", "Przerwano przebieg.", 130
    except (OSError, ValueError, KeyError, TypeError, RuntimeError, subprocess.SubprocessError) as exception:
        error = str(exception)
    finally:
        metadata.update(status=status, error=error, finished_at_utc=timestamp())
        write_json(run_dir / "metadata.json", metadata)
        summary = summarize(datasets, args.repetitions, counts, status, error)
        write_json(run_dir / "summary.json", summary)
    if error:
        print(error, file=sys.stderr)
    print(f"Status: {status}; poprawne: {summary['valid']}/{summary['planned']}", flush=True)
    return exit_code


def positive_int(value):
    number = int(value)
    if number <= 0:
        raise argparse.ArgumentTypeError("Liczba prob musi byc dodatnia.")
    return number


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repetitions", type=positive_int, default=30)
    parser.add_argument("--data-dir", type=Path, default=ROOT / "data")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "results")
    parser.add_argument("--compiler", default="c++", help="Executable name or path, without flags")
    return run(parser.parse_args())


if __name__ == "__main__":
    sys.exit(main())
