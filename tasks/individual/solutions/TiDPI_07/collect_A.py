"""Zachowuje jedną serię A (dwa bloki), bez eksperymentów poziomu B."""

import hashlib
import json
import platform
import shlex
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


def main():
    if Path.cwd() != Path(__file__).resolve().parent:
        raise SystemExit("run from TiDPI_07")
    run = Path("wyniki") / datetime.now(ZoneInfo("Europe/Warsaw")).strftime("%Y%m%d_%H%M%S_%f_A")
    run.mkdir()
    codes, commands = {}, []

    def call(label, args):
        commands.append(shlex.join(args))
        result = subprocess.run(args, capture_output=True)
        (run / f"{label}_stdout.txt").write_bytes(result.stdout)
        (run / f"{label}_stderr.txt").write_bytes(result.stderr)
        codes[label] = result.returncode
        (run / "commands.txt").write_text("\n".join(commands) + "\n")
        (run / "exit_codes.json").write_text(json.dumps(codes, indent=2) + "\n")
        if result.returncode:
            raise SystemExit(f"failed: {label}")

    compiler = subprocess.run(["clang++", "--version"], capture_output=True, text=True, check=True)
    env = {
        "recorded_at": datetime.now(ZoneInfo("Europe/Warsaw")).isoformat(),
        "system": platform.system(),
        "arch": platform.machine(),
        "python": platform.python_version(),
        "python_implementation": platform.python_implementation(),
        "compiler": compiler.stdout.splitlines()[:2],
        "compiler_version_command": "clang++ --version (first two lines only; installation path not collected)",
        "debugger": False,
    }
    for key, args in [
        ("macOS", ["sw_vers", "-productVersion"]),
        ("build", ["sw_vers", "-buildVersion"]),
        ("cpu", ["sysctl", "-n", "machdep.cpu.brand_string"]),
        ("memory_bytes", ["sysctl", "-n", "hw.memsize"]),
    ]:
        env[key] = subprocess.run(args, capture_output=True, text=True, check=True).stdout.strip()
    (run / "environment.json").write_text(json.dumps(env, indent=2) + "\n")
    sources = run / "sources"
    sources.mkdir()
    for name in ["benchmark.cpp", "benchmark.py", "generate_data.py", "collect_A.py", "verify_A.py", "plan_A.md"]:
        shutil.copyfile(name, sources / name)
    manifest = {f.name: hashlib.sha256(f.read_bytes()).hexdigest() for f in sources.iterdir()}
    (run / "source_sha256.json").write_text(json.dumps(manifest, indent=2) + "\n")
    call("generator", ["python3", "generate_data.py"])
    Path("_build").mkdir(exist_ok=True)
    call(
        "compile",
        [
            "clang++",
            "-std=c++17",
            "-O2",
            "-DNDEBUG",
            "-Wall",
            "-Wextra",
            "-pedantic",
            "benchmark.cpp",
            "-o",
            "_build/benchmark",
        ],
    )
    for block, languages in [(1, ["cpp", "python"]), (2, ["python", "cpp"])]:
        for lang in languages:
            exe = ["_build/benchmark"] if lang == "cpp" else ["python3", "benchmark.py"]
            call(f"block{block}_{lang}", exe + ["dane/input.txt", str(1 + (block - 1) * 5)])
    print(run.as_posix())


if __name__ == "__main__":
    main()
