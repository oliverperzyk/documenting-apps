"""Independent raw reader, Decimal statistics, preservation audit and PGFPlots source."""

import collections
import csv
import json
from decimal import Decimal
from pathlib import Path

from common import dump, sha


def stat(values):
    a = sorted(map(Decimal, values))
    n = len(a)
    return dict(
        n=n,
        min_ns=str(a[0]),
        max_ns=str(a[-1]),
        range_ns=str(a[-1] - a[0]),
        median_ns=str((a[(n - 1) // 2] + a[n // 2]) / 2),
        middle_pair_ns=list(map(str, a[n // 2 - 1 : n // 2 + 1])),
        sorted_ns=list(map(str, a)),
    )


def main():
    task = Path("../..")
    old = json.loads(Path("preexisting_sha256.json").read_text())
    preserved = {n: sha(task / n) == h for n, h in old.items() if n != "raport.md"}
    assert all(preserved.values())
    # New read-only audit of previous evidence, not new benchmark runs.
    history = {}
    for name, expected, blocks in [
        ("wyniki/20261017_102226_905860_A", 1002000000, 2),
        ("przebiegi/20261017_104449_232316_good1", 501000000, 2),
        ("przebiegi/20261017_104916_993218_good2", 501000000, 2),
    ]:
        p = task / name
        counts = {}
        for n, h in json.loads((p / "source_sha256.json").read_text()).items():
            assert sha(p / "sources" / n) == h
        for lang in ["cpp", "python"]:
            rows = []
            for b in range(1, blocks + 1):
                rows += list(
                    csv.DictReader((p / f"block{b}_{lang}_stdout.txt").read_text().splitlines(), delimiter=";")
                )
                warm = [
                    x for x in (p / f"block{b}_{lang}_stderr.txt").read_text().splitlines() if x.startswith("warmup=")
                ]
                assert len(warm) == 2 and all(f"checksum={expected};correct=true" in x for x in warm)
            assert [int(r["trial"]) for r in rows] == list(range(1, 11))
            assert all(int(r["checksum"]) == expected and r["correct"] == "true" for r in rows)
            counts[lang] = len(rows)
        history[name] = counts
    for study, runname in [("C1", "20261017_110944_353315_good"), ("C2", "20261017_111039_385982_good")]:
        p = task / "rozszerzenia/C" / study / "przebiegi" / runname
        val = json.loads((p / "validation.json").read_text())
        assert val["accepted"]
        for n, h in json.loads((p / "source_sha256.json").read_text()).items():
            assert sha(p / "sources" / n) == h
        rows = list(csv.DictReader((p / "results.csv").read_text().splitlines(), delimiter=";"))
        for r in rows:
            raw = list(csv.DictReader((p / f"{r['source_label']}_stdout.txt").read_text().splitlines(), delimiter=";"))[
                int(r["source_line"]) - 2
            ]
            assert all(r[k] == v for k, v in raw.items())
        for label in {r["source_label"] for r in rows}:
            warm = [x for x in (p / f"{label}_stderr.txt").read_text().splitlines() if x.startswith("warmup=")]
            expect = next(r["checksum"] for r in rows if r["source_label"] == label)
            assert len(warm) == 2 and all(f"checksum={expect};correct=true" in x for x in warm)
        history[study] = dict(records=len(rows), raw_matches=True, warmups_valid=True)
    for p in [
        task / "przebiegi/20261017_104540_940321_fault",
        task / "rozszerzenia/C/C2/przebiegi/20261017_111029_701722_fault",
    ]:
        assert not json.loads((p / "validation.json").read_text())["accepted"] and not (p / "results.csv").exists()
    data = Path("data/input_10000.txt")
    hist = collections.Counter(map(int, data.read_bytes().split()))
    expected = sum(f * abs(x - 500) for x, f in hist.items()) * 100
    assert expected == 251042700
    runs = json.loads(Path("latest.json").read_text())["series"]
    allrows = []
    selected = []
    stats = {}
    positions = {}
    ratios = {}
    ends = []
    binary = []
    for name in runs:
        run = Path(name)
        validation = json.loads((run / "validation.json").read_text())
        assert validation["accepted"]
        rows = list(csv.DictReader((run / "results.csv").read_text().splitlines(), delimiter=";"))
        assert len(rows) == 80
        events = json.loads((run / "execution.json").read_text())
        ends.append((events[0]["start_monotonic_ns"], events[-1]["end_monotonic_ns"]))
        binary.append(json.loads((run / "environment.json").read_text())["binary_sha256_after"])
        for r in rows:
            fields = (run / r["source_stdout"]).read_text().splitlines()
            assert fields[0] == "language;trial;time_ns;checksum;correct"
            raw = fields[int(r["source_line"]) - 1].split(";")
            assert raw == [r[k] for k in ["language", "trial", "time_ns", "checksum", "correct"]]
            assert int(r["checksum"]) == expected
            if r["pair"] in ["1", "20"]:
                selected.append(
                    dict(
                        series=r["series"],
                        schedule=r["schedule"],
                        pair=r["pair"],
                        language=r["language"],
                        raw=raw,
                        time_ms=str(Decimal(r["time_ns"]) / 1000000),
                        source=str(run / r["source_stdout"]),
                    )
                )
            allrows.append(dict(r, source_run=str(run)))
        for s in ["naprzemienny", "losowany"]:
            for lang in ["cpp", "python"]:
                group = [r for r in rows if r["schedule"] == s and r["language"] == lang]
                key = f"{group[0]['series']}/{s}/{lang}"
                assert len(group) == 20
                stats[key] = stat(r["time_ns"] for r in group)
                for pos in ["1", "2"]:
                    g = [r for r in group if r["position"] == pos]
                    assert len(g) == 10
                    positions[key + "/" + pos] = stat(r["time_ns"] for r in g)
                ratios[key + "/position_2_over_1"] = str(
                    Decimal(positions[key + "/2"]["median_ns"]) / Decimal(positions[key + "/1"]["median_ns"])
                )
            key = f"{rows[0]['series']}/{s}"
            ratios[key + "/python_over_cpp"] = str(
                Decimal(stats[key + "/python"]["median_ns"]) / Decimal(stats[key + "/cpp"]["median_ns"])
            )
    assert ends[0][1] <= ends[1][0] and binary[0] == binary[1]
    out = Path("analysis")
    out.mkdir(exist_ok=True)
    dump(
        out / "independent_check.json",
        dict(
            reviewer="Codex assistant, not a manual student verification",
            previous_files_unchanged=len(preserved),
            previous_evidence=history,
            expected_histogram=expected,
            histogram=dict(sorted(hist.items())),
            all_160_rows_equal_raw=True,
            sequential_series=True,
            same_binary=True,
            selected_raw_rows_pairs_1_20=selected,
            statistics_method="Decimal; sorted middle pair average",
            stats=stats,
            positions=positions,
            ratios=ratios,
        ),
    )
    dump(out / "stats.json", dict(groups=stats, positions=positions, ratios=ratios))
    with (out / "plot_data.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(allrows[0]), delimiter=";", lineterminator="\n")
        w.writeheader()
        w.writerows(allrows)
    # Standard scientific plotting tool PGFPlots; every observation has a separate x coordinate.
    tex = [
        r"\documentclass[border=5pt]{standalone}",
        r"\usepackage{fontspec}",
        r"\setmainfont{Arial}",
        r"\usepackage{pgfplots}",
        r"\pgfplotsset{compat=1.18}",
        r"\begin{document}",
        r"\begin{tikzpicture}",
    ]
    for index, lang in enumerate(["cpp", "python"]):
        tex.append(
            r"\begin{axis}[at={(0,"
            + str(-index * 6.3)
            + r"cm)},anchor=north west,width=16cm,height=6cm,ylabel={"
            + ("C++ Release" if lang == "cpp" else "CPython 3.14.4")
            + r": czas [ms]},xmin=0.5,xmax=4.5,xtick={1,2,3,4},xticklabels={S1 N,S1 L,S2 L,S2 N},scaled y ticks=false,/pgf/number format/use comma,ymajorgrids=true,legend style={at={(0.5,1.02)},anchor=south,legend columns=3,font=\small}]"
        )
        keys = [("1", "naprzemienny"), ("1", "losowany"), ("2", "losowany"), ("2", "naprzemienny")]
        for pos, color, mark in [("1", "blue", "*"), ("2", "orange!85!black", "triangle*")]:
            coords = []
            for x, (series, s) in enumerate(keys, 1):
                for r in allrows:
                    if (r["series"], r["schedule"], r["language"], r["position"]) == (series, s, lang, pos):
                        jitter = (int(r["pair"]) - 10.5) * 0.025
                        coords.append(f"({x + jitter:.4f},{Decimal(r['time_ns']) / 1000000})")
            tex.append(
                r"\addplot[only marks,mark="
                + mark
                + ",color="
                + color
                + r",mark size=1.7pt] coordinates {"
                + " ".join(coords)
                + "};"
            )
            tex.append(r"\addlegendentry{Pozycja " + pos + "}")
        for x, (series, s) in enumerate(keys, 1):
            y = Decimal(stats[f"{series}/{s}/{lang}"]["median_ns"]) / 1000000
            tex.append(
                r"\addplot[black,thick,forget plot] coordinates {("
                + str(x - 0.25)
                + ","
                + str(y)
                + ") ("
                + str(x + 0.25)
                + ","
                + str(y)
                + ")};"
            )
        tex.append(r"\end{axis}")
    tex += [r"\end{tikzpicture}", r"\end{document}"]
    (out / "distribution.tex").write_text("\n".join(tex) + "\n")
    print("A-C preserved; 160 raw rows, checksum histogram, all group/position statistics checked")


if __name__ == "__main__":
    main()
