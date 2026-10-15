"""Testy parsera na sztucznych fixture; liczby nie są wynikami eksperymentu."""

import csv
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("main.py")
HEADER = "TIDPI_RESULTS;1\ncase;size;trial;time_us;comparisons;correct\n"
ROW = "sorted;16;1;0;15;true\n"


class ParserTests(unittest.TestCase):
    def setUp(self):
        self.workspace = tempfile.TemporaryDirectory(prefix="tidpi06-test-")
        self.addCleanup(self.workspace.cleanup)
        self.folder = Path(self.workspace.name)
        self.source = self.folder / "raw.txt"
        self.output = self.folder / "results.csv"

    def run_parser(self, payload, output=None):
        self.source.write_bytes(payload if isinstance(payload, bytes) else payload.encode("utf-8"))
        return subprocess.run(
            [sys.executable, str(SCRIPT), str(self.source), str(output or self.output)],
            capture_output=True, text=True, check=False, timeout=10,
        )

    def test_full_dataset_and_bom_round_trip(self):
        rows = [
            f"{case};{size};{trial};0;0;true\n"
            for case in ("sorted", "reversed", "random")
            for size in (16, 32)
            for trial in (1, 2, 3)
        ]
        for bom in ("", "\ufeff"):
            with self.subTest(bom=bool(bom)):
                result = self.run_parser(bom + HEADER + "".join(rows))
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(result.stderr, "")
                self.assertIn("ACCEPTED: 18 record(s), failed tests: 0", result.stdout)
                self.assertTrue(self.output.read_bytes().startswith(b"\xef\xbb\xbf"))
                with self.output.open(encoding="utf-8-sig", newline="") as source:
                    reader = csv.DictReader(source, delimiter=";")
                    actual = list(reader)
                self.assertEqual(reader.fieldnames, HEADER.splitlines()[1].split(";"))
                expected = [dict(zip(reader.fieldnames, row.strip().split(";"))) for row in rows]
                self.assertEqual(actual, expected)

    def test_failed_test_is_published(self):
        result = self.run_parser(HEADER + ROW.replace("true", "false"))
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("failed tests: 1", result.stdout)
        self.assertIn(";false\n", self.output.read_text(encoding="utf-8-sig"))

    def test_rejections_remove_previous_csv(self):
        fixtures = {
            "invalid-number": (HEADER + ROW.replace("16", "many"), "line 3: size must be an integer"),
            "missing-field": (HEADER + "sorted;16;1;0;15\n", "line 3: expected 6 fields"),
            "duplicate-row": (HEADER + ROW + ROW, "line 4: duplicate record"),
            "wrong-version": ((HEADER + ROW).replace("RESULTS;1", "RESULTS;99"), "line 1:"),
            "wrong-header": (HEADER.replace("case;size", "size;case") + ROW, "line 2:"),
            "size-boundary": (HEADER + ROW.replace("16", "1"), "size must be >= 2"),
            "trial-boundary": (HEADER + "sorted;16;0;0;15;true\n", "trial must be >= 1"),
            "negative-time": (HEADER + "sorted;16;1;-1;15;true\n", "time_us must be >= 0"),
            "negative-count": (HEADER + "sorted;16;1;0;-1;true\n", "comparisons must be >= 0"),
            "unknown-case": (HEADER + ROW.replace("sorted", "other"), "unknown case"),
            "boolean-case": (HEADER + ROW.replace("true", "True"), "correct must be exactly"),
            "empty-data": (HEADER, "no result records"),
            "empty-file": ("", "protocol line and a header"),
            "blank-record": (HEADER + ROW + "\n", "line 4: expected 6 fields"),
            "extra-field": (HEADER + ROW.strip() + ";extra\n", "expected 6 fields, got 7"),
            "decimal": (HEADER + ROW.replace("16", "16.0"), "size must be an integer"),
            "broken-csv": (HEADER + '"sorted;16;1;0;15;true\n', "line 3:"),
            "invalid-utf8": (b"\xff", "cannot read input"),
            "combined-errors": (HEADER + "other;1;0;-1;-1;TRUE\n", "REJECTED: 6 validation error(s)"),
        }
        for name, (payload, diagnostic) in fixtures.items():
            with self.subTest(fixture=name):
                # Poprzedni wynik jest prawidłowym CSV z osobnego uruchomienia.
                self.assertEqual(self.run_parser(HEADER + ROW).returncode, 0)
                result = self.run_parser(payload)
                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertIn(diagnostic, result.stderr)
                self.assertEqual(result.stdout, "")
                self.assertFalse(self.output.exists())

    def test_input_aliases_are_never_deleted(self):
        self.source.write_text(HEADER + ROW, encoding="utf-8")
        aliases = [self.source, self.folder / "symlink.txt", self.folder / "hardlink.txt"]
        aliases[1].symlink_to(self.source)
        aliases[2].hardlink_to(self.source)
        for alias in aliases:
            with self.subTest(alias=alias.name):
                result = self.run_parser(HEADER + ROW, output=alias)
                self.assertEqual(result.returncode, 2)
                self.assertIn("must be distinct files", result.stderr)
                self.assertEqual(self.source.read_text(encoding="utf-8"), HEADER + ROW)
                self.assertTrue(alias.exists())

    def test_missing_input_removes_stale_output(self):
        self.assertEqual(self.run_parser(HEADER + ROW).returncode, 0)
        self.source.unlink()
        result = subprocess.run(
            [sys.executable, str(SCRIPT), str(self.source), str(self.output)],
            capture_output=True, text=True, check=False, timeout=10,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("cannot read input", result.stderr)
        self.assertFalse(self.output.exists())

    def test_output_failure_returns_two(self):
        result = self.run_parser(HEADER + ROW, output=self.folder / "missing" / "results.csv")
        self.assertEqual(result.returncode, 2)
        self.assertIn("OUTPUT ERROR", result.stderr)
        self.assertEqual(result.stdout, "")
        self.assertFalse(list(self.folder.glob(".tidpi-results-*")))


if __name__ == "__main__":
    unittest.main()
