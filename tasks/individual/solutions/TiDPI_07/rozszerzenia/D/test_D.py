"""Marked synthetic validator fixtures copied from real evidence; no benchmark reruns."""

import json
import shutil
import subprocess
from pathlib import Path

from common import dump, now


def main():
    source = Path(json.loads(Path("latest.json").read_text())["series"][0])
    root = Path("kontrole") / ("validator_" + now().replace(":", ""))
    root.mkdir(parents=True)
    for n in ["validate_D.py", "common.py", "test_D.py"]:
        shutil.copy2(n, root / n)
    cases = [
        ("valid", True, None),
        ("checksum", False, "CHECKSUM_TIME"),
        ("missing", False, "HEADER_COUNT"),
        ("schedule", False, "SCHEDULE"),
        ("warmup", False, "WARMUP_VALUE"),
        ("overlap", False, "SEQUENTIAL"),
    ]
    results = []
    for name, expected, rule in cases:
        dest = root / name
        shutil.copytree(source, dest)
        dump(
            dest / "fixture.json",
            dict(synthetic=True, source=str(source), mutation=name, expected_accept=expected, expected_rule=rule),
        )
        schedule = json.loads((dest / "schedule.json").read_text())
        label = schedule[0]["label"]
        if name == "checksum":
            p = dest / f"{label}_stdout.txt"
            p.write_text(p.read_text().replace(";251042700;true", ";251042701;true"))
        if name == "missing":
            p = dest / f"{label}_stdout.txt"
            p.write_text(p.read_text().splitlines()[0] + "\n")
        if name == "schedule":
            schedule[0], schedule[1] = schedule[1], schedule[0]
            dump(dest / "schedule.json", schedule)
        if name == "warmup":
            p = dest / f"{label}_stderr.txt"
            p.write_text(p.read_text().replace("checksum=251042700", "checksum=0", 1))
        if name == "overlap":
            events = json.loads((dest / "execution.json").read_text())
            events[-1]["start_monotonic_ns"] = events[-2]["start_monotonic_ns"]
            dump(dest / "execution.json", events)
        with (dest / "validator_stdout.txt").open("wb") as out, (dest / "validator_stderr.txt").open("wb") as err:
            p = subprocess.run(["python3", "validate_D.py", str(dest)], stdout=out, stderr=err)
        (dest / "validator_exit_code.txt").write_text(str(p.returncode) + "\n")
        r = json.loads((dest / "validation.json").read_text())
        passed = (
            r["accepted"] == expected
            and p.returncode == (0 if expected else 1)
            and (dest / "results.csv").exists() == expected
            and (dest / "warmups.csv").exists() == expected
            and (rule is None or any(e.startswith(rule) for e in r["errors"]))
        )
        results.append(
            dict(name=name, expected_accept=expected, actual_accept=r["accepted"], passed=passed, errors=r["errors"])
        )
    dump(
        root / "summary.json",
        dict(
            synthetic=True,
            passed=sum(r["passed"] for r in results),
            failed=sum(not r["passed"] for r in results),
            cases=results,
        ),
    )
    dump("test_latest.json", dict(root=str(root)))
    assert all(r["passed"] for r in results)
    print("6/6 validator decisions match expectations, rejected copies have no results.csv")


if __name__ == "__main__":
    main()
