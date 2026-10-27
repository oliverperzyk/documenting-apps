"""Validate a benchmark run and produce reproducible statistics and PNG plots."""

import argparse
import csv
import hashlib
import json
import os
from collections import Counter, defaultdict
from pathlib import Path
from statistics import median

ROOT = Path(__file__).resolve().parent
DEFAULT_RUN = ROOT / "results/20261026T184512Z_7d95f26993"
STAT_FIELDS = [
    "language",
    "data_id",
    "size_bytes",
    "variant",
    "count",
    "median_ns",
    "min_ns",
    "max_ns",
    "range_ns",
]
STATUSES = {"valid", "wrong_result", "invalid_output", "runtime_error", "timeout"}


def statistics(values):
    """Keep zeros and extremes; no rounding of half-integer medians."""
    if not values:
        return dict(count=0, median_ns="", min_ns="", max_ns="", range_ns="")
    return dict(
        count=len(values),
        median_ns=median(values),
        min_ns=min(values),
        max_ns=max(values),
        range_ns=max(values) - min(values),
    )


def analyze(run_dir):
    metadata = json.loads((run_dir / "metadata.json").read_text())
    summary = json.loads((run_dir / "summary.json").read_text())
    with (run_dir / "measurements.csv").open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        required = {
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
        }
        if not required <= set(reader.fieldnames or []):
            raise ValueError("Brak wymaganych kolumn CSV")
        rows = list(reader)
    repetitions = metadata["repetitions"]
    if type(repetitions) is not int or repetitions <= 0 or metadata["unit"] != "ns":
        raise ValueError("Niepoprawna liczba powtórzeń lub jednostka metadanych")
    datasets = {d["data_id"]: d for d in metadata["datasets"]}
    if len(datasets) != len(metadata["datasets"]):
        raise ValueError("Powielone identyfikatory danych w metadanych")
    expected = {(lang, data_id): d for data_id, d in datasets.items() for lang in ("cpp", "python")}
    grouped = defaultdict(list)
    issues = []

    def issue(message, language="", data_id="", row=""):
        issues.append(dict(row=row, language=language, data_id=data_id, issue=message))

    for number, row in enumerate(rows, 2):
        key = row["language"], row["data_id"]
        if key not in expected:
            issue("Nieoczekiwana kombinacja język–plik", *key, number)
        else:
            grouped[key].append((number, row))
    pairs = {}
    for pair in summary["pairs"]:
        key = pair["language"], pair["data_id"]
        if key in pairs:
            issue("Powielona para w summary.json", *key)
        pairs[key] = pair
    if set(pairs) != set(expected):
        issue("Zestaw par summary.json nie odpowiada metadanym")
    stats, completeness = [], []
    for key, dataset in sorted(
        expected.items(), key=lambda item: (item[1]["size_bytes"], item[1]["variant"], item[0][0])
    ):
        entries = grouped[key]
        start_issues = len(issues)
        trials = Counter()
        parsed = []
        for number, row in entries:
            errors = []
            try:
                trial = int(row["trial"])
                trials[trial] += 1
                if not 1 <= trial <= repetitions:
                    errors.append("Numer próby poza planem")
                position = 1 if (key[0] == "cpp") == (trial % 2 == 1) else 2
                if int(row["position"]) != position:
                    errors.append("Niepoprawna kolejność języków")
            except (ValueError, TypeError):
                trial = None
                errors.append("Niepoprawny numer próby lub pozycja")
            for field in ("sha256", "size_bytes", "variant", "expected_words"):
                if str(row[field]) != str(dataset[field]):
                    errors.append(f"Niezgodność pola {field} z metadanymi")
            if row["unit"] != "ns":
                errors.append("Jednostka różna od ns")
            if row["status"] not in STATUSES:
                errors.append("Nieznany status")
            elapsed = None
            try:
                if row["elapsed"] != "":
                    elapsed = int(row["elapsed"])
                    if elapsed < 0:
                        raise ValueError()
            except (ValueError, TypeError):
                errors.append("Niepoprawny czas")
            if row["status"] == "valid":
                if elapsed is None:
                    errors.append("Brak czasu poprawnej próby")
                if row["actual_words"] != row["expected_words"]:
                    errors.append("Błędny wynik oznaczony jako valid")
                if row["reason"]:
                    errors.append("Powód odrzucenia przy statusie valid")
            else:
                issue(f"Próba odrzucona: {row['status']}; {row['reason']}", *key, number)
            for error in errors:
                issue(error, *key, number)
            parsed.append((trial, elapsed, not errors and row["status"] == "valid"))
        missing = sorted(set(range(1, repetitions + 1)) - set(trials))
        duplicates = sorted(t for t, count in trials.items() if count > 1)
        if missing:
            issue("Brak numerów prób: " + ", ".join(map(str, missing)), *key)
        if duplicates:
            issue("Powielone numery prób: " + ", ".join(map(str, duplicates)), *key)
        values = [elapsed for trial, elapsed, valid in parsed if valid and trials[trial] == 1]
        valid_status = sum(r["status"] == "valid" for _, r in entries)
        rejected = len(entries) - valid_status
        actual = dict(planned=repetitions, executed=len(entries), valid=valid_status, rejected=rejected)
        if any(pairs.get(key, {}).get(k) != v for k, v in actual.items()):
            issue("Liczniki summary.json nie odpowiadają CSV i planowi", *key)
        if len(values) != repetitions:
            issue(f"Poprawnych jednoznacznych prób {len(values)} zamiast {repetitions}", *key)
        stats.append(
            dict(
                language=key[0],
                data_id=key[1],
                size_bytes=dataset["size_bytes"],
                variant=dataset["variant"],
                **statistics(values),
            )
        )
        completeness.append(
            dict(
                language=key[0],
                data_id=key[1],
                **actual,
                usable=len(values),
                missing_trials=";".join(map(str, missing)),
                duplicate_trials=";".join(map(str, duplicates)),
                issues=len(issues) - start_issues,
            )
        )
    actual_totals = dict(
        planned=len(expected) * repetitions,
        executed=len(rows),
        valid=sum(r["status"] == "valid" for r in rows),
        rejected=sum(r["status"] != "valid" for r in rows),
    )
    if any(summary.get(k) != v for k, v in actual_totals.items()):
        issue("Globalne liczniki summary.json nie odpowiadają CSV i planowi")
    wanted_status = (
        "complete"
        if actual_totals["executed"] == actual_totals["planned"] and not actual_totals["rejected"]
        else "completed_with_rejections"
    )
    if summary["status"] != wanted_status or metadata["status"] != summary["status"]:
        issue("Status przebiegu nie odpowiada licznikom lub metadanym")
    return stats, completeness, issues


def write_csv(path, rows, fields):
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def provenance(run_dir):
    meta = json.loads((run_dir / "metadata.json").read_text())
    sources = []
    for name, expected in meta["source_sha256"].items():
        path = ROOT / name
        actual = hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None
        sources.append(
            dict(
                file=name,
                recorded_sha256=expected,
                current_sha256=actual,
                matches=actual == expected,
            )
        )
    data = []
    for item in meta["datasets"]:
        path = ROOT / "data" / item["data_id"]
        actual = hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None
        data.append(dict(data_id=item["data_id"], matches=actual == item["sha256"]))
    return dict(
        measurements_sha256=hashlib.sha256((run_dir / "measurements.csv").read_bytes()).hexdigest(),
        sources=sources,
        datasets=data,
    )


def plots(stats, run_dir, output):
    # Avoid writes to a private user cache; works on headless systems too.
    os.environ.setdefault("MPLCONFIGDIR", "/tmp/word-counter-matplotlib")
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.ticker import ScalarFormatter

    plt.rcParams.update({"font.size": 10, "axes.grid": True, "grid.alpha": 0.22})
    image_dir = output / "images"
    image_dir.mkdir(exist_ok=True)
    source = Path(os.path.relpath(run_dir / "measurements.csv", ROOT)).as_posix()
    sizes = sorted({s["size_bytes"] for s in stats})
    common = sorted(set.intersection(*({s["variant"] for s in stats if s["size_bytes"] == size} for size in sizes)))
    colors = ["#1864ab", "#d9480f", "#2b8a3e", "#7048a5"]
    fig, axes = plt.subplots(1, 2, figsize=(13, 5.5))
    for ax, lang in zip(axes, ("cpp", "python")):
        for variant, color in zip(common, colors):
            series = sorted(
                (s for s in stats if s["language"] == lang and s["variant"] == variant and s["count"]),
                key=lambda s: s["size_bytes"],
            )
            ax.plot(
                [s["size_bytes"] for s in series],
                [s["median_ns"] / 1000 for s in series],
                marker="o",
                color=color,
                label=variant,
            )
        ax.set(
            title="C++" if lang == "cpp" else "Python",
            xlabel="Długość tekstu [B]",
            ylabel="Mediana czasu [µs]",
            ylim=(0, None),
        )
        ax.set_xticks(sizes, [f"{n:,}".replace(",", " ") for n in sizes])
        ax.tick_params(axis="x", labelsize=9)
        ax.legend(fontsize=8)
        ax.xaxis.set_major_formatter(ScalarFormatter(useOffset=False))
        ax.ticklabel_format(axis="x", style="plain")
    fig.suptitle("Mediany czasu a długość tekstu — cztery wspólne warianty (osie liniowe)")
    fig.text(
        0.02,
        0.02,
        f"Źródło: {source}\nPoprawne próby; ns / 1000 = µs. Osobne skale czasu dla języków.",
        fontsize=8,
    )
    fig.tight_layout(rect=(0, 0.10, 1, 0.94))
    fig.savefig(image_dir / "mediany_dlugosc.png", dpi=180)
    plt.close(fig)
    fig, axes = plt.subplots(len(sizes), 2, figsize=(13, 4 * len(sizes)), squeeze=False)
    for index, size in enumerate(sizes):
        for col, lang in enumerate(("cpp", "python")):
            ax = axes[index, col]
            series = [s for s in stats if s["language"] == lang and s["size_bytes"] == size and s["count"]]
            med = [s["median_ns"] / 1000 for s in series]
            ax.errorbar(
                med,
                range(len(series)),
                xerr=[
                    [(s["median_ns"] - s["min_ns"]) / 1000 for s in series],
                    [(s["max_ns"] - s["median_ns"]) / 1000 for s in series],
                ],
                fmt="o",
                capsize=4,
                color=colors[col],
                label="Mediana i zakres min–max",
            )
            ax.set_yticks(range(len(series)), [s["variant"] for s in series])
            ax.set(
                title=f"{'C++' if lang == 'cpp' else 'Python'} · {size:,} B".replace(",", " "),
                xlabel="Czas [µs]",
                ylabel="Wariant danych",
                xlim=(0, None),
            )
            ax.invert_yaxis()
            ax.legend(fontsize=8, loc="best")
    fig.suptitle("Mediany i rozrzut czasów wszystkich wariantów — bez usuwania skrajności")
    fig.text(
        0.02,
        0.01,
        f"Źródło: {source}\nOsie liniowe; każdy panel ma własną skalę czasu; zakres to minimum–maksimum, nie przedział ufności.",
        fontsize=8,
    )
    fig.tight_layout(rect=(0, 0.06, 1, 0.97))
    fig.savefig(image_dir / "rozrzut_warianty.png", dpi=180)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", type=Path, default=DEFAULT_RUN)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "analysis")
    args = parser.parse_args()
    # Never overwrite raw inputs, even with an accidental output path.
    if (
        args.output_dir.resolve().is_relative_to((ROOT / "results").resolve())
        or args.output_dir.resolve() == args.run_dir.resolve()
    ):
        parser.error("Katalog analizy musi znajdować się poza surowymi wynikami")
    try:
        stats, completeness, issues = analyze(args.run_dir)
        args.output_dir.mkdir(parents=True, exist_ok=True)
        write_csv(args.output_dir / "statistics.csv", stats, STAT_FIELDS)
        write_csv(args.output_dir / "completeness.csv", completeness, list(completeness[0]))
        write_csv(args.output_dir / "issues.csv", issues, ["row", "language", "data_id", "issue"])
        (args.output_dir / "provenance.json").write_text(
            json.dumps(provenance(args.run_dir), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        plots(stats, args.run_dir, args.output_dir)
    except (OSError, ValueError, KeyError, ImportError) as error:
        parser.exit(2, f"Analiza nie powiodła się: {error}\n")
    print(f"Przeanalizowano {len(stats)} grup; odstępstwa: {len(issues)}. Wyniki: {args.output_dir.name}/")
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
