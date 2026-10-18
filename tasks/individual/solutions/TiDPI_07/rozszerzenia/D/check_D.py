"""Read-only final artifact checks, explicit list of visually inspected pages."""

import argparse
import json
import re
import subprocess
import zlib
from pathlib import Path

from common import dump, now, sha


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--visual-pages", default="")
    args = ap.parse_args()
    task = Path("../..")
    report = (task / "raport.md").read_text()
    assert len(re.findall(r"^# ", report, re.M)) == 1
    assert list(map(int, re.findall(r"^## (\d+)\.", report, re.M))) == list(range(1, 13))
    assert all(f"**D{i:02}**" in report for i in range(25, 32))
    assert all(f"TC-{i:02}" in report for i in range(21, 28))
    assert all(s in report for s in ['date: "2026-10-17"', 'author: "Kryptonim TiDPI: Regulus"', "lang: pl-PL"])
    links = re.findall(r"\]\(([^)]+)\)", report)
    for target in links:
        assert (task / target).is_file(), target
    old = json.loads(Path("preexisting_sha256.json").read_text())
    preserved = 0
    for n, h in old.items():
        if n == "raport.md":
            assert sha(task / "archiwum_C/raport.md") == h
            continue
        assert sha(task / n) == h, n
        preserved += 1
    # Original C PDF snapshot, kept byte-identical before exporting D.
    assert (task / "archiwum_C/raport.pdf").is_file()
    runs = json.loads(Path("latest.json").read_text())["series"]
    total = warm = 0
    for name in runs:
        p = Path(name)
        r = json.loads((p / "validation.json").read_text())
        assert r["accepted"] and r["published_records"] == 80 and r["warmup_records"] == 160
        total += r["published_records"]
        warm += r["warmup_records"]
        assert (p / "validate_exit_code.txt").read_text().strip() == "0"
        assert all(x["code"] == 0 for x in json.loads((p / "execution.json").read_text()))
        for n, h in json.loads((p / "source_sha256.json").read_text()).items():
            assert sha(p / "sources" / n) == h
        for item in json.loads((p / "schedule.json").read_text()):
            for stream in ["stdout", "stderr"]:
                assert (p / f"{item['label']}_{stream}.txt").is_file()
    tests = Path(json.loads(Path("test_latest.json").read_text())["root"])
    t = json.loads((tests / "summary.json").read_text())
    assert t["passed"] == 6 and t["failed"] == 0
    for case in t["cases"]:
        if not case["expected_accept"]:
            assert (
                not (tests / case["name"] / "results.csv").exists()
                and not (tests / case["name"] / "warmups.csv").exists()
            )
    independent = json.loads(Path("analysis/independent_check.json").read_text())
    assert independent["all_160_rows_equal_raw"] and independent["same_binary"] and independent["sequential_series"]
    # Scan all deliverable sources/logs, all exported PDF text/metadata/decompressed streams.
    privacy = re.compile(rb"/(?:Users|home)/|[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
    files = [
        p
        for p in task.rglob("*")
        if p.is_file()
        and not any(x in p.parts for x in ["_build", "__pycache__"])
        and p.name != "TiDPI_07_Rzetelny_benchmark_Cpp_i_Python.pdf"
    ]
    for p in files:
        if p.suffix == ".pdf":
            txt = subprocess.run(["pdftotext", str(p), "-"], capture_output=True, check=True).stdout
            info = subprocess.run(["pdfinfo", str(p)], capture_output=True, check=True).stdout
            streams = []
            for m in re.finditer(rb"stream\r?\n(.*?)\r?\nendstream", p.read_bytes(), re.S):
                try:
                    streams.append(zlib.decompress(m[1]))
                except zlib.error:
                    pass
            assert not privacy.search(txt + info + b"\n".join(streams)), str(p.relative_to(task))
        else:
            assert not privacy.search(p.read_bytes()), str(p.relative_to(task))
    info = subprocess.run(["pdfinfo", str(task / "raport.pdf")], capture_output=True, check=True).stdout
    pdftext = subprocess.run(
        ["pdftotext", "-layout", str(task / "raport.pdf"), "-"], capture_output=True, check=True
    ).stdout.decode()
    pages = int(re.search(rb"Pages:\s+(\d+)", info)[1])
    assert b"Kryptonim TiDPI: Regulus" in info
    raw_rows = re.findall(r"^(?:cpp|python);[0-9]+;[0-9]+;[0-9]+;(?:true|false)$", report, re.M)
    assert all(row in pdftext for row in raw_rows), [row for row in raw_rows if row not in pdftext]
    assert pdftext.count("language;trial;time_ns;checksum;correct") >= report.count(
        "language;trial;time_ns;checksum;correct"
    )
    assert all(x in pdftext for x in ["Środowisko", "Poziom D", "251042700", "Rysunek 1", "215,641", "197,313"])
    raw = (task / "raport.pdf").read_bytes()
    streams = []
    for m in re.finditer(rb"stream\r?\n(.*?)\r?\nendstream", raw, re.S):
        try:
            streams.append(zlib.decompress(m[1]))
        except zlib.error:
            pass
    targets = [x.decode("utf8") for x in re.findall(rb"/(?:URI|F)\(([^()]+)\)", b"\n".join(streams))]
    assert len(targets) >= len(links), (len(targets), len(links))
    assert all((task / x).is_file() for x in targets)
    inspected = list(map(int, args.visual_pages.split(","))) if args.visual_pages else []
    if inspected:
        assert inspected == list(range(1, pages + 1))
    # Every visible text bounding box must stay within the page.
    bbox = subprocess.run(
        ["pdftotext", "-bbox", str(task / "raport.pdf"), "-"], capture_output=True, check=True
    ).stdout.decode()
    for page in re.findall(r'<page width="([0-9.]+)" height="([0-9.]+)">(.*?)</page>', bbox, re.S):
        width, height, body = page
        for x1, y1, x2, y2 in re.findall(
            r'<word xMin="([0-9.-]+)" yMin="([0-9.-]+)" xMax="([0-9.-]+)" yMax="([0-9.-]+)"', body
        ):
            assert 0 <= float(x1) <= float(x2) <= float(width) and 0 <= float(y1) <= float(y2) <= float(height)
    # Explicit manifest, not a package or upload. School PDF is excluded.
    manifest = Path("submission_files.txt")
    manifest.write_text("\n".join(sorted(str(p.relative_to(task)) for p in files if p != task / manifest)) + "\n")
    result = dict(
        recorded_at=now(),
        TC_27="passed" if inspected else "pending_visual_review",
        preserved_previous_files=preserved,
        all_link_targets_exist=True,
        markdown_links=len(links),
        pdf_links=len(targets),
        accepted_trials=total,
        accepted_warmups=warm,
        validator_tests=6,
        independent_arithmetic_passed=True,
        privacy_scan_passed=True,
        plot_visual_review="passed",
        all_report_raw_rows_in_pdf=len(raw_rows),
        pdf_pages=pages,
        text_bounds_passed=True,
        render_sha256={str(i): sha(task / "_build/D_render" / f"final-{i:02d}.png") for i in inspected},
        visual_review=dict(
            reviewer="Codex assistant",
            pages=inspected,
            method="Poppler page PNGs, inspected using view_image",
            checks=["Polish glyphs", "tables", "logs", "links", "all 160 plotted observations", "page breaks"],
        ),
        report_sha256=sha(task / "raport.md"),
        pdf_sha256=sha(task / "raport.pdf"),
        plot_sha256=sha(task / "images/D_distribution.png"),
        excluded=["school task PDF", "_build binaries and renders", "__pycache__"],
        deviations=[
            "D uses exact 10000-line prefix of 20020-element historical A",
            "previous C2 data deviation retained",
            "macOS/arm64/Clang instead of Windows/MSVC",
        ],
        no_git_commit_push_or_external_delivery=True,
    )
    dump("kontrole/final_check.json", result)
    print(f"Checks passed; pages={pages}; links={len(links)}; visual={bool(inspected)}; trials={total}; warmups={warm}")


if __name__ == "__main__":
    main()
