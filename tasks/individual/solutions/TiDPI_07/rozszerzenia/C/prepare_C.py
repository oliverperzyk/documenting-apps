"""Przygotowanie planu i danych przed pomiarami; bez uruchomień benchmarków."""

import random
from pathlib import Path

from common import A_SHA, SEED, dump, expectation, now, schedule, sha


def main():
    root = Path(__file__).resolve().parent
    task = root.parent.parent
    if (root / "prepared.json").exists():
        raise SystemExit("Preparation already exists; do not overwrite evidence")
    archive = task / "archiwum_B"
    archive.mkdir(exist_ok=False)
    # Zachowujemy wersję raportu B i jego kontroli przed aktualizacją raportu.
    for name, source in [
        ("raport.md", task / "raport.md"),
        ("raport.pdf", task / "raport.pdf"),
        ("check_artifacts.py", task / "check_artifacts.py"),
        ("final_check.json", task / "kontrole_B/final_check.json"),
    ]:
        (archive / name).write_bytes(source.read_bytes())
    dump(archive / "integrity.json", {p.name: sha(p.read_bytes()) for p in archive.iterdir() if p.is_file()})
    baseline = {}
    for p in task.rglob("*"):
        if p.is_file() and not any(x in p.parts for x in ["_build", "__pycache__", "rozszerzenia"]):
            baseline[p.relative_to(task).as_posix()] = sha(p.read_bytes())
    dump(root / "preexisting_sha256.json", baseline)
    a = (task / "dane/input.txt").read_bytes()
    assert sha(a) == A_SHA and len(a.split()) == 20020
    values = [i % 1001 for i in range(50000)]
    random.Random(SEED).shuffle(values)
    master = "".join(f"{x}\n" for x in values).encode("ascii")
    datasets = {
        "C1": {10000: b"".join(a.splitlines(keepends=True)[:10000])},
        "C2": {n: b"".join(master.splitlines(keepends=True)[:n]) for n in [10000, 30000, 50000]},
    }
    for study, files in datasets.items():
        dest = root / study
        (dest / "dane").mkdir(parents=True)
        manifest = {
            "prepared_at": now(),
            "study": study,
            "seed": SEED,
            "historical_A_sha256": A_SHA,
            "historical_A_count": 20020,
            "generator": (
                "Historical A: values=[i % 1001 for i in range(20020)]; random.Random(20261017).shuffle(values); then take first 10000 lines"
                if study == "C1"
                else "values=[i % 1001 for i in range(50000)]; random.Random(20261017).shuffle(values)"
            ),
            "provenance": "historical A first 10000 lines" if study == "C1" else "new 50000 master and its prefixes",
            "format": "ASCII, one integer per line, LF",
            "data": {str(n): expectation(data) for n, data in files.items()},
        }
        for n, data in files.items():
            (dest / "dane" / f"input_{n}.txt").write_bytes(data)
        dump(dest / "data_manifest.json", manifest)
        dump(dest / "schedule.json", schedule(study))
    prefix = datasets["C2"][10000]
    dump(
        root / "prefix_check.json",
        {
            "checked_at": now(),
            "historical_A_count": 20020,
            "A_full_equals_C2_10000": a == prefix,
            "A_first10000_equals_C2_10000": datasets["C1"][10000] == prefix,
            "A_first10000_sha256": sha(datasets["C1"][10000]),
            "C2_first10000_sha256": sha(prefix),
            "C2_10000_is_master_prefix": master.startswith(prefix),
            "C2_30000_is_master_prefix": master.startswith(datasets["C2"][30000]),
            "resolution": "User approved retaining the A generator, using A prefix for C1, and disclosing mismatch for C2.",
        },
    )
    dump(
        root / "prepared.json",
        {
            "prepared_at": now(),
            "measurements_started": False,
            "plan_sha256": sha((root / "plan_C.md").read_bytes()),
            "schedules": {s: sha((root / s / "schedule.json").read_bytes()) for s in datasets},
        },
    )
    print("Prepared C1/C2; no benchmark executed; prefix mismatch preserved")


if __name__ == "__main__":
    main()
