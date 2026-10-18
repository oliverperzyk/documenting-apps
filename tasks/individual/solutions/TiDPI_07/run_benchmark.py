"""Sekwencyjny automat B: świeży build, pełne strumienie, walidacja całości."""

import argparse
import hashlib
import platform
import shlex
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from validate_results import SCHEDULE, dump, expectation

FLAGS = ["-std=c++17", "-O2", "-DNDEBUG", "-Wall", "-Wextra", "-pedantic"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--python-source", type=Path, default=Path("benchmark.py"))
    parser.add_argument("--label", choices=["good1", "fault", "good2"], required=True)
    args = parser.parse_args()
    if Path.cwd() != Path(__file__).resolve().parent:
        parser.error("run from TiDPI_07")

    def now():
        return datetime.now(ZoneInfo("Europe/Warsaw")).isoformat()

    run = Path("przebiegi") / (datetime.now(ZoneInfo("Europe/Warsaw")).strftime("%Y%m%d_%H%M%S_%f_") + args.label)
    run.mkdir(parents=True)
    print(run.as_posix(), flush=True)
    codes, commands, execution = {}, [], []

    def call(label, argv, timeout=60, record_code=True):
        commands.append({"label": label, "argv": argv, "timeout_seconds": timeout})
        dump(run / "commands.json", commands)
        (run / "commands.txt").write_text("\n".join(shlex.join(x["argv"]) for x in commands) + "\n")
        started = now()
        status = "completed"
        try:
            proc = subprocess.run(argv, capture_output=True, timeout=timeout, check=False)
            out, err, code = proc.stdout, proc.stderr, proc.returncode
        except subprocess.TimeoutExpired as exc:
            out, err, code, status = exc.stdout or b"", exc.stderr or b"", 124, "timeout"
        except OSError as exc:
            out, err, code, status = b"", f"launch error: errno={exc.errno}\n".encode(), 127, "launch_error"
        (run / f"{label}_stdout.txt").write_bytes(out)
        (run / f"{label}_stderr.txt").write_bytes(err)
        execution.append({"label": label, "started_at": started, "finished_at": now(), "code": code, "status": status})
        dump(run / "execution.json", execution)
        if record_code:
            codes[label] = code
            dump(run / "exit_codes.json", codes)
        (run / "exit_codes.txt").write_text(
            "\n".join(f"{x['label']}={x['code']} ({x['status']})" for x in execution) + "\n"
        )
        return code

    try:
        data = Path("dane/input.txt").read_bytes()
        expectation(data)
        (run / "input.txt").write_bytes(data)
        dump(run / "schedule.json", SCHEDULE)
        sources = run / "sources"
        sources.mkdir()
        for name in ["benchmark.cpp", "generate_data.py", "run_benchmark.py", "validate_results.py", "plan_B.md"]:
            shutil.copyfile(name, sources / name)
        shutil.copyfile(args.python_source, sources / "benchmark.py")
        dump(
            run / "source_sha256.json",
            {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(sources.iterdir())},
        )
        # Nie zbieramy prywatnej ścieżki instalacji kompilatora.
        compiler = subprocess.run(["clang++", "--version"], capture_output=True, text=True, check=True, timeout=10)
        env = {
            "recorded_at": now(),
            "system": platform.system(),
            "arch": platform.machine(),
            "python": platform.python_version(),
            "python_implementation": platform.python_implementation(),
            "compiler": compiler.stdout.splitlines()[:2],
            "flags": FLAGS,
            "compiler_version_scope": "first two version lines; installation path not collected",
            "compiler_version_exit_code": compiler.returncode,
            "debugger": False,
            "rounds": 100,
            "time_unit": "ns",
            "count": 20020,
            "seed": 20261017,
            "data_sha256_before": hashlib.sha256(data).hexdigest(),
        }
        for key, argv in [
            ("macOS", ["sw_vers", "-productVersion"]),
            ("build", ["sw_vers", "-buildVersion"]),
            ("cpu", ["sysctl", "-n", "machdep.cpu.brand_string"]),
            ("memory_bytes", ["sysctl", "-n", "hw.memsize"]),
        ]:
            meta = subprocess.run(argv, capture_output=True, text=True, check=True, timeout=10)
            env[key] = meta.stdout.strip()
        dump(run / "environment.json", env)
        build = run / "_build"
        build.mkdir()
        binary = build / "benchmark"
        rc = call("compile", ["clang++", *FLAGS, str(sources / "benchmark.cpp"), "-o", str(binary)], 120)
        if rc == 0 and binary.is_file():
            env["binary_sha256"] = hashlib.sha256(binary.read_bytes()).hexdigest()
            for item in SCHEDULE:
                b, lang = item["block"], item["language"]
                exe = [str(binary)] if lang == "cpp" else ["python3", str(sources / "benchmark.py")]
                call(f"block{b}_{lang}", exe + ["dane/input.txt", str(item["first_trial"])])
        env["data_sha256_after"] = hashlib.sha256(Path("dane/input.txt").read_bytes()).hexdigest()
        dump(run / "environment.json", env)
        code = call("validate", ["python3", str(sources / "validate_results.py"), str(run)], record_code=False)
        dump(
            run / "runner_result.json",
            {"exit_code": code, "validation_exit_code": code, "run": run.name, "finished_at": now()},
        )
        return code
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        dump(run / "runner_result.json", {"exit_code": 2, "error_type": type(exc).__name__, "finished_at": now()})
        print("Runner configuration/environment error; see runner_result.json")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
