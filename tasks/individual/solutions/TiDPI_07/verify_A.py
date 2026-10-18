"""Weryfikacja całej serii A przed statystykami."""

import collections
import csv
import hashlib
import io
import json
import statistics
import sys
from pathlib import Path

HEADER = ["language", "trial", "time_ns", "checksum", "correct"]


def verify(run):
    data = Path("dane/input.txt").read_bytes()
    values = [int(x) for x in data.split()]
    assert len(values) == 20020
    assert collections.Counter(values) == {x: 20 for x in range(1001)}
    meta = json.loads((run / "generator_stdout.txt").read_text())
    assert meta["sha256"] == hashlib.sha256(data).hexdigest()
    assert meta["count"] == 20020 and meta["seed"] == 20261017
    # Wzorzec z sum dwóch partycji, inny algorytm niż badana pętla.
    low = [x for x in values if x < 500]
    high = [x for x in values if x > 500]
    one_round = 500 * len(low) - sum(low) + sum(high) - 500 * len(high)
    assert one_round == 20 * 2 * (500 * 501 // 2) == 5010000
    expected = one_round * 200
    assert expected == 1002000000
    codes = json.loads((run / "exit_codes.json").read_text())
    assert set(codes) == {"generator", "compile", "block1_cpp", "block1_python", "block2_python", "block2_cpp"}
    assert all(x == 0 for x in codes.values())
    manifest = json.loads((run / "source_sha256.json").read_text())
    for name, digest in manifest.items():
        assert hashlib.sha256(Path(name).read_bytes()).hexdigest() == digest
        assert hashlib.sha256((run / "sources" / name).read_bytes()).hexdigest() == digest
    all_rows = {}
    for lang in ["cpp", "python"]:
        rows = []
        for block in [1, 2]:
            content = (run / f"block{block}_{lang}_stdout.txt").read_text()
            reader = csv.reader(io.StringIO(content), delimiter=";")
            assert next(reader) == HEADER
            blockrows = list(reader)
            assert len(blockrows) == 5
            for number, row in enumerate(blockrows, 1 + (block - 1) * 5):
                assert len(row) == 5 and row[0] == lang
                assert row[1].isdigit() and int(row[1]) == number
                assert row[2].isdigit() and int(row[2]) > 0
                assert row[3].isdigit() and int(row[3]) == expected
                assert row[4] == "true"
            stderr = (run / f"block{block}_{lang}_stderr.txt").read_text().splitlines()
            warmups = [x for x in stderr if x.startswith("warmup=")]
            assert len(warmups) == 2
            for number, line in enumerate(warmups, 1):
                fields = dict(x.split("=") for x in line.split(";"))
                assert int(fields["warmup"]) == number and int(fields["time_ns"]) > 0
                assert int(fields["checksum"]) == expected and fields["correct"] == "true"
            rows.extend(blockrows)
        all_rows[lang] = rows
    # Dopiero po akceptacji CAŁOŚCI powstają pliki pochodne.
    stats = {}
    for lang, rows in all_rows.items():
        times = [int(row[2]) for row in rows]
        ordered = sorted(times)
        median = (ordered[4] + ordered[5]) / 2
        assert median == statistics.median(times)
        stats[lang] = {
            "min_ns": min(times),
            "max_ns": max(times),
            "range_ns": max(times) - min(times),
            "median_ns": median,
            "sorted_ns": ordered,
            "middle_pair_ns": ordered[4:6],
        }
        with (run / f"A_{lang}_raw.txt").open("w", newline="") as f:
            writer = csv.writer(f, delimiter=";", lineterminator="\n")
            writer.writerow(HEADER)
            writer.writerows(rows)
    result = {
        "TC-01": "passed",
        "TC-02": "passed",
        "TC-03": "passed",
        "TC-04": "passed",
        "expected": expected,
        "one_round": one_round,
        "data_sha256": meta["sha256"],
        "trials_per_language": 10,
        "warmups_per_language": 4,
        "stats": stats,
        "raw_aggregation": "Two original block stdout files, one header retained in derived A_*_raw.txt",
    }
    (run / "verification.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    verify(Path(sys.argv[1]))
