"""Niezależna kontrola raw i rachunków C, bez użycia walidatora lub calculate."""

import collections
import csv
import hashlib
import json
from decimal import Decimal
from pathlib import Path


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def output(p, v):
    p.write_text(json.dumps(v, ensure_ascii=False, indent=2) + "\n")


def main():
    root = Path(".")
    task = Path("../..")
    old = json.loads((root / "preexisting_sha256.json").read_text())
    preservation = {
        name: digest(task / name) == sha for name, sha in old.items() if name not in ["raport.md", "raport.pdf"]
    }
    assert all(preservation.values())
    history = {}
    for run, expected in [
        ("wyniki/20261017_102226_905860_A", 1002000000),
        ("przebiegi/20261017_104449_232316_good1", 501000000),
        ("przebiegi/20261017_104916_993218_good2", 501000000),
    ]:
        path = task / run
        for name, sha in json.loads((path / "source_sha256.json").read_text()).items():
            assert digest(path / "sources" / name) == sha
        groups = {}
        for lang in ["cpp", "python"]:
            rows = []
            for b in [1, 2]:
                rows.extend(
                    csv.DictReader((path / f"block{b}_{lang}_stdout.txt").read_text().splitlines(), delimiter=";")
                )
                warm = [
                    x
                    for x in (path / f"block{b}_{lang}_stderr.txt").read_text().splitlines()
                    if x.startswith("warmup=")
                ]
                assert len(warm) == 2 and all(f"checksum={expected};correct=true" in x for x in warm)
            assert len(rows) == 10 and [int(r["trial"]) for r in rows] == list(range(1, 11))
            assert all(int(r["checksum"]) == expected and r["correct"] == "true" for r in rows)
            times = sorted(Decimal(r["time_ns"]) for r in rows)
            groups[lang] = {"records": 10, "median_ns": str((times[4] + times[5]) / 2), "checksum": expected}
        history[run] = groups
    f = task / "przebiegi/20261017_104540_940321_fault"
    assert not json.loads((f / "validation.json").read_text())["accepted"] and not (f / "results.csv").exists()
    output(
        root / "kontrole/audit_AB.json",
        {
            "reviewer": "Codex assistant",
            "history": history,
            "preserved_file_count": len(preservation),
            "preservation": preservation,
            "B_fault_rejected_without_csv": True,
            "note": "New read-only audit of historical evidence; not a historical execution.",
        },
    )
    runs = {}
    for study in ["C1", "C2"]:
        candidates = [
            p
            for p in (root / study / "przebiegi").iterdir()
            if (p / "validation.json").exists() and json.loads((p / "validation.json").read_text())["accepted"]
        ]
        assert len(candidates) == 1
        run = candidates[0]
        validation = json.loads((run / "validation.json").read_text())
        manifest = json.loads((run / "data_manifest.json").read_text())
        expected = {}
        for n, m in manifest["data"].items():
            hist = collections.Counter(map(int, (run / "data" / f"input_{n}.txt").read_bytes().split()))
            total = sum(freq * abs(value - 500) for value, freq in hist.items()) * 100
            assert total == m["expected"]
            expected[int(n)] = total
        merged = list(csv.DictReader((run / "results.csv").read_text().splitlines(), delimiter=";"))
        groups = {}
        for key, stat in validation["stats"].items():
            config, n, lang = key.split("/")
            n = int(n)
            raw = []
            variant = config if study == "C1" else lang
            for b in range(1, 6):
                label = f"b{b}_{n}_{variant}"
                source = run / f"{label}_stdout.txt"
                for line, row in enumerate(csv.DictReader(source.read_text().splitlines(), delimiter=";"), 2):
                    matching = [r for r in merged if r["source_label"] == label and int(r["source_line"]) == line]
                    assert len(matching) == 1
                    assert all(matching[0][k] == row[k] for k in row)
                    raw.append(row)
            assert len(raw) == 10 and [int(r["trial"]) for r in raw] == list(range(1, 11))
            assert all(int(r["checksum"]) == expected[n] and r["correct"] == "true" for r in raw)
            times = sorted(Decimal(r["time_ns"]) for r in raw)
            median = (times[4] + times[5]) / 2
            assert median == Decimal(stat["median_ns"])
            assert (
                times[0] == stat["min_ns"] and times[-1] == stat["max_ns"] and times[-1] - times[0] == stat["range_ns"]
            )
            selected = [
                {
                    "trial": int(r["trial"]),
                    "time_ns": r["time_ns"],
                    "time_ms": str(Decimal(r["time_ns"]) / 1000000),
                    "checksum": r["checksum"],
                }
                for r in raw
                if r["trial"] in ["1", "10"]
            ]
            groups[key] = {
                "median_ns": str(median),
                "middle_pair_ns": list(map(str, times[4:6])),
                "range_ns": str(times[-1] - times[0]),
                "selected_rows": selected,
            }
        runs[study] = {"run": str(run), "groups": groups, "expected_histogram": expected}
    fault = [p for p in Path("C2/przebiegi").iterdir() if p.name.endswith("_fault")][0]
    assert not json.loads((fault / "validation.json").read_text())["accepted"] and not (fault / "results.csv").exists()
    good = Path(runs["C2"]["run"])
    assert (good / "sources/benchmark.py").read_bytes() == Path("benchmark.py").read_bytes()
    assert (fault / "sources/benchmark.py").read_text().replace("d = x - 0", "d = x - 500") == Path(
        "benchmark.py"
    ).read_text()
    events = json.loads((fault / "execution.json").read_text())
    correct_events = json.loads((good / "execution.json").read_text())
    assert events[-1]["finished_at"] <= correct_events[0]["started_at"]
    output(
        root / "kontrole/independent_check.json",
        {
            "reviewer": "Codex assistant; not a manual student check",
            "runs": runs,
            "fault_rejected_no_csv": True,
            "correct_python_restored": True,
            "all_accepted_csv_rows_match_raw": True,
            "all_stats_independently_recomputed": True,
        },
    )
    print("A-B preserved; C histogram checks, every CSV row, statistics and trials 1/10 checked independently")


if __name__ == "__main__":
    main()
