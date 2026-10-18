"""Kompilacja i sekwencyjne procesy według wcześniej utrwalonego planu C."""

import argparse
import json
import platform
import shlex
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from common import FLAGS, SOURCES, dump, now, sha


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("study", choices=["C1", "C2"])
    parser.add_argument("--fault", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    if Path.cwd() != root:
        parser.error("run from rozszerzenia/C")
    prepared = json.loads(Path("prepared.json").read_text())
    assert sha(Path("plan_C.md").read_bytes()) == prepared["plan_sha256"]
    assert sha((Path(args.study) / "schedule.json").read_bytes()) == prepared["schedules"][args.study]
    name = datetime.now(ZoneInfo("Europe/Warsaw")).strftime("%Y%m%d_%H%M%S_%f_") + ("fault" if args.fault else "good")
    run = Path(args.study) / "przebiegi" / name
    (run / "sources").mkdir(parents=True)
    (run / "data").mkdir()
    (run / "_build").mkdir()
    print(run, flush=True)
    for source in SOURCES:
        shutil.copyfile(source, run / "sources" / source)
    if args.fault:
        s = run / "sources/benchmark.py"
        s.write_text(s.read_text().replace("d = x - 500", "d = x - 0"))
        (run / "fault_description.txt").write_text(
            "Python calculation centre changed from 500 to 0; expected checksum remains unchanged.\n"
        )
    dump(run / "source_sha256.json", {n: sha((run / "sources" / n).read_bytes()) for n in SOURCES})
    for name in ["schedule.json", "data_manifest.json"]:
        shutil.copyfile(Path(args.study) / name, run / name)
    shutil.copyfile("prepared.json", run / "prepared.json")
    shutil.copyfile("../../dane/input.txt", run / "data/historical_A.txt")
    for data in (Path(args.study) / "dane").iterdir():
        shutil.copyfile(data, run / "data" / data.name)
    commands, execution, codes = [], [], {}

    def call(label, argv, timeout=60, include=True):
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
            out, err, code, status = b"", f"launch error errno={exc.errno}\n".encode(), 127, "launch_error"
        (run / f"{label}_stdout.txt").write_bytes(out)
        (run / f"{label}_stderr.txt").write_bytes(err)
        execution.append({"label": label, "started_at": started, "finished_at": now(), "code": code, "status": status})
        dump(run / "execution.json", execution)
        if include:
            codes[label] = code
            dump(run / "exit_codes.json", codes)
        (run / "exit_codes.txt").write_text(
            "\n".join(f"{x['label']}={x['code']} ({x['status']})" for x in execution) + "\n"
        )
        return out, code

    env = {
        "recorded_at": now(),
        "study": args.study,
        "system": platform.system(),
        "arch": platform.machine(),
        "python": platform.python_version(),
        "python_implementation": platform.python_implementation(),
        "debugger": False,
        "rounds": 100,
        "time_unit": "ns",
        "fault": args.fault,
        "flags": {k: FLAGS[k] for k in (["Debug", "Release"] if args.study == "C1" else ["Release"])},
        "compiler_version_scope": "first two lines; installation path deliberately not collected",
        "data_sha256_before": {p.name: sha(p.read_bytes()) for p in (run / "data").iterdir()},
    }
    version_script = "import subprocess,sys; p=subprocess.run(['clang++','--version'],capture_output=True); print('\\n'.join(p.stdout.decode().splitlines()[:2])); sys.exit(p.returncode)"
    out, code = call("compiler_version", ["python3", "-c", version_script])
    if code:
        raise RuntimeError("compiler version query failed")
    env["compiler"] = out.decode().splitlines()
    for key, argv in [
        ("macOS", ["sw_vers", "-productVersion"]),
        ("build", ["sw_vers", "-buildVersion"]),
        ("cpu", ["sysctl", "-n", "machdep.cpu.brand_string"]),
        ("memory_bytes", ["sysctl", "-n", "hw.memsize"]),
    ]:
        out, code = call("meta_" + key, argv)
        if code:
            dump(run / "environment.json", env)
            dump(
                run / "runner_result.json",
                {"exit_code": 2, "stage": "environment", "failed_query": key, "measurements_started": False},
            )
            print("Environment query rejected; preserved partial run; no measurements")
            return 2
        env[key] = out.decode().strip()
    dump(run / "environment.json", env)
    builds = {}
    for config, flags in env["flags"].items():
        binary = run / "_build" / f"benchmark_{config}"
        _, code = call(
            "compile_" + config, ["clang++", *flags, str(run / "sources/benchmark.cpp"), "-o", str(binary)], 120
        )
        builds[config] = code
        if not code:
            env.setdefault("binary_sha256", {})[config] = sha(binary.read_bytes())
    manifest = json.loads((run / "data_manifest.json").read_text())
    if all(code == 0 for code in builds.values()):
        for item in json.loads((run / "schedule.json").read_text()):
            exe = (
                [str(run / "_build" / f"benchmark_{item['configuration']}")]
                if item["language"] == "cpp"
                else ["python3", str(run / "sources/benchmark.py")]
            )
            data = manifest["data"][str(item["size"])]
            argv = exe + [
                str(run / "data" / f"input_{item['size']}.txt"),
                str(item["size"]),
                str(data["expected"]),
                str(item["first_trial"]),
                str(item["trials"]),
            ]
            call(item["label"], argv)
    env["data_sha256_after"] = {p.name: sha(p.read_bytes()) for p in (run / "data").iterdir()}
    dump(run / "environment.json", env)
    _, code = call("validate", ["python3", str(run / "sources/validate_C.py"), str(run)], include=False)
    dump(run / "runner_result.json", {"exit_code": code, "finished_at": now()})
    return code


if __name__ == "__main__":
    sys.exit(main())
