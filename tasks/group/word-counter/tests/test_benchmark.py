import argparse
import contextlib
import csv
import hashlib
import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import Benchmark as benchmark


class BenchmarkTests(unittest.TestCase):
    def execute(self, code, expected=1, **kwargs):
        return benchmark.measure([sys.executable, "-c", code], expected, **kwargs)

    def test_valid_and_zero_time(self):
        row, _ = self.execute("print('Ilość znalezionych słów: 1; (czas: 0 ns)')")
        self.assertEqual((row["status"], row["elapsed"]), ("valid", 0))

    def test_wrong_result_keeps_time(self):
        row, _ = self.execute("print('Ilość znalezionych słów: 2; (czas: 42 ns)')")
        self.assertEqual((row["status"], row["actual_words"], row["elapsed"]), ("wrong_result", 2, 42))

    def test_invalid_output(self):
        for output in (
            "hello",
            "Ilość znalezionych słów: 1; (czas: -1 ns)",
            "Ilość znalezionych słów: 1; (czas: 1 ns) extra",
        ):
            with self.subTest(output=output):
                row, _ = self.execute(f"print({output!r})")
                self.assertEqual(row["status"], "invalid_output")
                self.assertEqual(row["elapsed"], "")

    def test_runtime_error(self):
        row, diagnostic = self.execute("import sys; print('failure', file=sys.stderr); sys.exit(2)")
        self.assertEqual(row["status"], "runtime_error")
        self.assertIn("failure", diagnostic["stderr"])

    def test_missing_executable(self):
        row, _ = benchmark.measure(["/nonexistent-word-counter-executable"], 1)
        self.assertEqual(row["status"], "runtime_error")

    def test_timeout(self):
        row, _ = self.execute("import time; time.sleep(2)", timeout=0.05)
        self.assertEqual(row["status"], "timeout")

    def test_failed_compilation_removes_old_binary(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            binary = root / "word-counter"
            binary.write_text("old executable")
            with patch.object(
                benchmark.subprocess, "run", return_value=subprocess.CompletedProcess([], 1, b"", b"compile failed")
            ):
                with self.assertRaises(RuntimeError):
                    benchmark.compile_cpp("c++", binary, root, root / "compilation.log")
            self.assertFalse(binary.exists())
            self.assertIn("compile failed", (root / "compilation.log").read_text())

    def make_data(self, root, expected=1):
        data_dir = root / "data"
        data_dir.mkdir()
        (data_dir / "sample.txt").write_bytes(b"Ala\rma")
        manifest = {
            "files": [
                {
                    "file": "sample.txt",
                    "size_bytes": 6,
                    "sha256": hashlib.sha256(b"Ala\rma").hexdigest(),
                    "variant": "cr",
                    "expected_words": expected,
                }
            ]
        }
        (data_dir / "manifest.json").write_text(json.dumps(manifest))
        return data_dir

    def test_integrity_check(self):
        with tempfile.TemporaryDirectory() as directory:
            data_dir = self.make_data(Path(directory))
            self.assertEqual(len(benchmark.load_datasets(data_dir)), 1)
            (data_dir / "sample.txt").write_bytes(b"changed")
            with self.assertRaises(ValueError):
                benchmark.load_datasets(data_dir)

    def test_rejected_trials_are_saved_and_excluded(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            # Deliberately wrong expected value: both real programs must return 1.
            args = argparse.Namespace(
                data_dir=self.make_data(root, expected=2), output_dir=root / "results", repetitions=2, compiler="c++"
            )
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                code = benchmark.run(args)
            self.assertEqual(code, 1)
            (run_dir,) = args.output_dir.iterdir()
            summary = json.loads((run_dir / "summary.json").read_text())
            self.assertEqual((summary["executed"], summary["valid"], summary["rejected"]), (4, 0, 4))
            self.assertEqual(summary["status"], "completed_with_rejections")
            with (run_dir / "measurements.csv").open(newline="") as stream:
                rows = list(csv.DictReader(stream))
            self.assertEqual([row["language"] for row in rows], ["cpp", "python", "python", "cpp"])
            self.assertTrue(all(row["status"] == "wrong_result" and row["elapsed"] for row in rows))
            self.assertEqual(len((run_dir / "errors.jsonl").read_text().splitlines()), 4)

    def test_build_failure_never_starts_measurements(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            args = argparse.Namespace(
                data_dir=self.make_data(root), output_dir=root / "results", repetitions=1, compiler="c++"
            )
            with (
                patch.object(benchmark, "compile_cpp", side_effect=RuntimeError("build failed")),
                patch.object(benchmark, "measure") as measure,
                contextlib.redirect_stdout(io.StringIO()),
                contextlib.redirect_stderr(io.StringIO()),
            ):
                self.assertEqual(benchmark.run(args), 1)
            measure.assert_not_called()
            (run_dir,) = args.output_dir.iterdir()
            self.assertEqual(json.loads((run_dir / "summary.json").read_text())["executed"], 0)

    def test_interrupt_preserves_incomplete_summary(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            args = argparse.Namespace(
                data_dir=self.make_data(root), output_dir=root / "results", repetitions=1, compiler="c++"
            )
            with (
                patch.object(benchmark, "measure", side_effect=KeyboardInterrupt),
                contextlib.redirect_stdout(io.StringIO()),
                contextlib.redirect_stderr(io.StringIO()),
            ):
                self.assertEqual(benchmark.run(args), 130)
            (run_dir,) = args.output_dir.iterdir()
            summary = json.loads((run_dir / "summary.json").read_text())
            self.assertEqual((summary["status"], summary["executed"], summary["planned"]), ("interrupted", 0, 2))


if __name__ == "__main__":
    unittest.main()
