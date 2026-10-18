"""Walidacja kompletnego badania C; żadnych statystyk ani CSV po odrzuceniu."""

import argparse
import csv
import json
import random
import re
from datetime import datetime
from decimal import Decimal
from pathlib import Path

from common import A_SHA, FLAGS, HEADER, SEED, SOURCES, dump, expectation, schedule, sha


def validate(run):
    run = Path(run)
    output = run / "results.csv"
    if output.is_symlink():
        raise ValueError("OUTPUT_SYMLINK")
    output.unlink(missing_ok=True)
    errors = []
    rows = []
    stats = {}

    def check(ok, rule, location):
        if not ok:
            errors.append({"rule": rule, "location": str(location)})
        return ok

    try:
        meta = json.loads((run / "environment.json").read_text())
        study = meta["study"]
        assert study in ["C1", "C2"]
        planned = schedule(study)
        check(json.loads((run / "schedule.json").read_text()) == planned, "SCHEDULE", "schedule.json")
        prepared = json.loads((run / "prepared.json").read_text())
        check(
            sha((run / "schedule.json").read_bytes()) == prepared["schedules"][study],
            "SCHEDULE_PREPARED",
            "schedule.json",
        )
        check(sha((run / "sources/plan_C.md").read_bytes()) == prepared["plan_sha256"], "PLAN_HASH", "plan_C.md")
        sources = json.loads((run / "source_sha256.json").read_text())
        check(set(sources) == set(SOURCES), "SOURCE_SET", "sources")
        for name, h in sources.items():
            check(sha((run / "sources" / name).read_bytes()) == h, "SOURCE_HASH", name)
        a = (run / "data/historical_A.txt").read_bytes()
        check(sha(a) == A_SHA, "HISTORICAL_A_HASH", "historical_A.txt")
        vals = [i % 1001 for i in range(50000)]
        random.Random(SEED).shuffle(vals)
        master = "".join(f"{x}\n" for x in vals).encode("ascii")
        expected_data = (
            {10000: b"".join(a.splitlines(keepends=True)[:10000])}
            if study == "C1"
            else {n: b"".join(master.splitlines(keepends=True)[:n]) for n in [10000, 30000, 50000]}
        )
        manifest = json.loads((run / "data_manifest.json").read_text())
        check(set(manifest["data"]) == set(map(str, expected_data)), "SIZE_SET", "data_manifest.json")
        check(
            manifest["seed"] == SEED and manifest["historical_A_sha256"] == A_SHA,
            "DATA_PARAMETERS",
            "data_manifest.json",
        )
        expectations = {}
        for n, data in expected_data.items():
            actual = (run / "data" / f"input_{n}.txt").read_bytes()
            check(actual == data, "DATA_CONTENT", n)
            expectations[n] = expectation(actual)
            check(expectations[n] == manifest["data"][str(n)], "DATA_MANIFEST", n)
        hashes = {p.name: sha(p.read_bytes()) for p in (run / "data").iterdir()}
        check(meta["data_sha256_before"] == hashes == meta["data_sha256_after"], "DATA_CHANGED", "environment.json")
        flags = {k: FLAGS[k] for k in (["Debug", "Release"] if study == "C1" else ["Release"])}
        check(
            meta["flags"] == flags
            and meta["rounds"] == 100
            and meta["time_unit"] == "ns"
            and meta["debugger"] is False,
            "CONFIGURATION",
            "environment.json",
        )
        codes = json.loads((run / "exit_codes.json").read_text())
        meta_labels = ["compiler_version", "meta_macOS", "meta_build", "meta_cpu", "meta_memory_bytes"]
        labels = meta_labels + ["compile_" + k for k in flags] + [i["label"] for i in planned]
        check(set(codes) == set(labels), "EXIT_CODE_SET", "exit_codes.json")
        for label, code in codes.items():
            check(type(code) is int and code == 0, "PROCESS_EXIT", label)
        execution = json.loads((run / "execution.json").read_text())
        execution = [x for x in execution if x["label"] != "validate"]
        check([x["label"] for x in execution] == labels, "EXECUTION_ORDER", "execution.json")
        for index, event in enumerate(execution):
            start = datetime.fromisoformat(event["started_at"])
            end = datetime.fromisoformat(event["finished_at"])
            check(
                start <= end and event["status"] == "completed" and event["code"] == codes[event["label"]],
                "EXECUTION_STATUS",
                event["label"],
            )
            check(start >= datetime.fromisoformat(prepared["prepared_at"]), "PLAN_BEFORE_RUN", event["label"])
            if index:
                check(
                    datetime.fromisoformat(execution[index - 1]["finished_at"]) <= start, "SEQUENTIAL", event["label"]
                )
        commands = json.loads((run / "commands.json").read_text())
        check([x["label"] for x in commands if x["label"] != "validate"] == labels, "COMMAND_ORDER", "commands.json")
        bylabel = {x["label"]: x["argv"] for x in commands}
        for config, f in flags.items():
            check(
                bylabel["compile_" + config]
                == [
                    "clang++",
                    *f,
                    str(run / "sources/benchmark.cpp"),
                    "-o",
                    str(run / "_build" / f"benchmark_{config}"),
                ],
                "COMPILE_COMMAND",
                config,
            )
        for item in planned:
            label = item["label"]
            n = item["size"]
            lang = item["language"]
            config = item["configuration"]
            expected = expectations[n]["expected"]
            exe = (
                [str(run / "_build" / f"benchmark_{config}")]
                if lang == "cpp"
                else ["python3", str(run / "sources/benchmark.py")]
            )
            check(
                bylabel[label]
                == exe + [str(run / "data" / f"input_{n}.txt"), str(n), str(expected), str(item["first_trial"]), "2"],
                "BENCHMARK_COMMAND",
                label,
            )
            content = (run / f"{label}_stdout.txt").read_text().splitlines()
            check(bool(content) and content[0] == HEADER, "HEADER", label)
            raw = list(csv.reader(content[1:], delimiter=";", strict=True))
            check(len(raw) == 2, "BLOCK_COUNT", label)
            ids = []
            for line, row in enumerate(raw, 2):
                loc = f"{label}:{line}"
                if not check(len(row) == 5, "FIELD_COUNT", loc):
                    continue
                check(row[0] == lang, "LANGUAGE", loc)
                check(row[4] == "true", "CORRECT", loc)
                if not check(all(re.fullmatch(r"-?[0-9]+", v) for v in row[1:4]), "INTEGER", loc):
                    continue
                trial, ns, checksum = map(int, row[1:4])
                ids.append(trial)
                check(ns >= 0, "TIME_NS", loc)
                check(checksum == expected, "CHECKSUM", loc)
                rows.append([study, config, n, 100, item["block"], lang, trial, ns, checksum, row[4], label, line])
            check(ids == list(range(item["first_trial"], item["first_trial"] + 2)), "TRIAL_SEQUENCE", label)
            diagnostics = (run / f"{label}_stderr.txt").read_text().splitlines()
            warm = [x for x in diagnostics if x.startswith("warmup=")]
            check(len(warm) == 2, "WARMUP_COUNT", label)
            for i, w in enumerate(warm, 1):
                match = re.fullmatch(r"warmup=([0-9]+);time_ns=(-?[0-9]+);checksum=(-?[0-9]+);correct=(true|false)", w)
                if check(match is not None, "WARMUP_FORMAT", label):
                    num, ns, checksum, correct = match.groups()
                    check(
                        int(num) == i and int(ns) >= 0 and int(checksum) == expected and correct == "true",
                        "WARMUP_VALUE",
                        label,
                    )
            clocks = [x for x in diagnostics if not x.startswith("warmup=")]
            if check(len(clocks) == 1, "CLOCK_COUNT", label):
                if lang == "cpp":
                    check(
                        re.fullmatch(
                            r"clock=steady_clock;is_steady=1;period_num=[1-9][0-9]*;period_den=[1-9][0-9]*", clocks[0]
                        )
                        is not None,
                        "CPP_CLOCK",
                        label,
                    )
                else:
                    clock = json.loads(clocks[0])
                    check(clock["resolution_seconds"] > 0 and clock["monotonic"] is True, "PYTHON_CLOCK", label)
        groups = (
            {("Debug", 10000, "cpp"), ("Release", 10000, "cpp")}
            if study == "C1"
            else {
                (c, n, language)
                for n in [10000, 30000, 50000]
                for c, language in [("Release", "cpp"), ("CPython", "python")]
            }
        )
        for config, n, lang in groups:
            times = [r for r in rows if r[1] == config and r[2] == n and r[5] == lang]
            check([r[6] for r in times] == list(range(1, 11)), "GROUP_COMPLETENESS", f"{config}/{n}/{lang}")
        if not errors:
            for config, n, lang in sorted(groups):
                times = sorted(r[7] for r in rows if r[1] == config and r[2] == n and r[5] == lang)
                stats[f"{config}/{n}/{lang}"] = {
                    "configuration": config,
                    "count": n,
                    "language": lang,
                    "trials": 10,
                    "min_ns": times[0],
                    "max_ns": times[-1],
                    "range_ns": times[-1] - times[0],
                    "median_ns": str(Decimal(times[4] + times[5]) / 2),
                    "middle_pair_ns": times[4:6],
                    "sorted_ns": times,
                }
    except (OSError, ValueError, KeyError, TypeError, AssertionError, IndexError, csv.Error) as exc:
        errors.append({"rule": "READ_OR_STRUCTURE", "location": type(exc).__name__})
    result = {"accepted": not errors, "errors": errors, "published_records": 0, "csv_created": False}
    if not errors:
        with (run / "results.csv.tmp").open("w", newline="") as f:
            writer = csv.writer(f, delimiter=";", lineterminator="\n")
            writer.writerow(
                [
                    "study",
                    "configuration",
                    "size",
                    "rounds",
                    "block",
                    "language",
                    "trial",
                    "time_ns",
                    "checksum",
                    "correct",
                    "source_label",
                    "source_line",
                ]
            )
            writer.writerows(rows)
        (run / "results.csv.tmp").replace(output)
        result.update(stats=stats, published_records=len(rows), csv_created=True)
    dump(run / "validation.json", result)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("run", type=Path)
    args = parser.parse_args()
    result = validate(args.run)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["accepted"] else 1)
