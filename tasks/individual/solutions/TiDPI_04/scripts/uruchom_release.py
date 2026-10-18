"""Skompiluj i uruchom A/C/D w Release bez debuggera.
Zastępuje główne outputy; zachowuje istniejące archiwum Debug.
Po uruchomieniu odśwież raport skryptem opracuj_wyniki.py.
"""

import argparse
import hashlib
import platform
import subprocess
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
FLAGS = ["-std=c++17", "-O2", "-DNDEBUG", "-Wall", "-Wextra", "-pedantic"]


def capture(command):
    return subprocess.run(command, check=True, capture_output=True, text=True).stdout


def metadata(date, jobs):
    lines = [
        f"date={date}",
        "timezone=Europe/Warsaw",
        "configuration=Release",
        "flags=" + " ".join(FLAGS),
        "execution=terminal_without_debugger",
        "host=" + capture(["sw_vers", "-productVersion"]).strip(),
        "build=" + capture(["sw_vers", "-buildVersion"]).strip(),
        "arch=" + platform.machine(),
    ]
    # Pierwsze dwie linie nie ujawniają lokalnej ścieżki instalacji.
    lines.extend(capture(["clang++", "--version"]).splitlines()[:2])
    lines.append("name;source_sha256;compile_exit;run_exit;output")
    for name, src, out in jobs:
        lines.append(
            ";".join([name, hashlib.sha256(src.read_bytes()).hexdigest(), "0", "0", str(out.relative_to(ROOT))])
        )
    lines.append("A_powtorzony;same_binary_as_A_bazowy;not_recompiled;0;wyniki/A_powtorzony.txt")
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--date",
        default=datetime.now(ZoneInfo("Europe/Warsaw")).date().isoformat(),
        help="Data serii YYYY-MM-DD, do metryczki.",
    )
    args = parser.parse_args()
    datetime.strptime(args.date, "%Y-%m-%d")
    build = ROOT / ".build/release"
    build.mkdir(parents=True, exist_ok=True)
    source = (ROOT / "main.cpp").read_text()
    assert source.count("{20260401, 20260402}") == 1
    assert source.count("generator() % 10'000U") == 1
    (build / "seed.cpp").write_text(source.replace("{20260401, 20260402}", "{20260499, 20260402}"))
    (build / "generator.cpp").write_text(
        source.replace("generator() % 10'000U", "generator() % 9'999U").replace(
            "engine_output_modulo_10000", "engine_output_modulo_9999"
        )
    )
    jobs = [
        ("A_bazowy", ROOT / "main.cpp", ROOT / "wyniki/A_bazowy.txt"),
        ("A_zmieniony_seed", build / "seed.cpp", ROOT / "wyniki/A_zmieniony_seed.txt"),
        ("A_zmieniony_generator", build / "generator.cpp", ROOT / "wyniki/A_zmieniony_generator.txt"),
        (
            "C_wiele_seedow",
            ROOT / "rozszerzenia/C/wiele_seedow/main.cpp",
            ROOT / "rozszerzenia/C/wiele_seedow/output.txt",
        ),
        (
            "C_bez_early_exit",
            ROOT / "rozszerzenia/C/bez_early_exit/main.cpp",
            ROOT / "rozszerzenia/C/bez_early_exit/output.txt",
        ),
        ("D_std_sort", ROOT / "rozszerzenia/D/main.cpp", ROOT / "rozszerzenia/D/output.txt"),
    ]
    for name, src, out in jobs:
        subprocess.run(["clang++", *FLAGS, str(src), "-o", str(build / name)], check=True)
        stdout = capture([str(build / name)])
        assert stdout.rstrip().endswith("all_correct=true"), name
        out.write_text(stdout)
        print(name + ": compile_exit=0, run_exit=0")
    (ROOT / "wyniki/A_powtorzony.txt").write_text(capture([str(build / "A_bazowy")]))
    assert (ROOT / "main.cpp").read_text() == source
    (ROOT / "wyniki/Release_metadane.txt").write_text(metadata(args.date, jobs))


if __name__ == "__main__":
    main()
