import copy
import csv
import json
import tempfile
import unittest
from pathlib import Path

import Analyze


class AnalysisTests(unittest.TestCase):
    def test_statistics(self):
        self.assertEqual(
            Analyze.statistics([10, 0, 4, 2]), dict(count=4, median_ns=3, min_ns=0, max_ns=10, range_ns=10)
        )
        self.assertEqual(Analyze.statistics([0, 1, 1000000])["median_ns"], 1)
        self.assertEqual(Analyze.statistics([0, 1])["median_ns"], 0.5)
        self.assertEqual(Analyze.statistics([])["median_ns"], "")

    def fixture(self):
        dataset = dict(data_id="a.txt", sha256="abc", size_bytes=100, variant="short", expected_words=2)
        meta = dict(datasets=[dataset], repetitions=2, unit="ns", status="complete")
        rows = []
        for trial in (1, 2):
            for lang in ("cpp", "python"):
                rows.append(
                    dict(
                        dataset,
                        language=lang,
                        trial=str(trial),
                        position=str(1 if (lang == "cpp") == (trial % 2 == 1) else 2),
                        elapsed=str(0 if trial == 1 else 1000000),
                        unit="ns",
                        actual_words=2,
                        status="valid",
                        reason="",
                    )
                )
        pairs = [
            dict(language=lang, data_id="a.txt", planned=2, executed=2, valid=2, rejected=0)
            for lang in ("cpp", "python")
        ]
        summary = dict(status="complete", planned=4, executed=4, valid=4, rejected=0, pairs=pairs)
        return meta, rows, summary

    def execute(self, mutate=lambda m, r, s: None):
        meta, rows, summary = copy.deepcopy(self.fixture())
        mutate(meta, rows, summary)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "metadata.json").write_text(json.dumps(meta))
            (root / "summary.json").write_text(json.dumps(summary))
            with (root / "measurements.csv").open("w", newline="") as stream:
                writer = csv.DictWriter(stream, fieldnames=rows[0].keys())
                writer.writeheader()
                writer.writerows(rows)
            return Analyze.analyze(root)

    def test_complete_preserves_zero_and_extreme(self):
        stats, complete, issues = self.execute()
        self.assertEqual(issues, [])
        self.assertTrue(all(s["median_ns"] == 500000 and s["min_ns"] == 0 and s["max_ns"] == 1000000 for s in stats))
        self.assertTrue(all(s["usable"] == 2 for s in complete))

    def test_missing(self):
        _, complete, issues = self.execute(lambda m, r, s: r.pop())
        self.assertTrue(any(s["missing_trials"] == "2" for s in complete))
        self.assertTrue(any("Brak numerów" in i["issue"] for i in issues))

    def test_duplicate_excludes_ambiguous_trial(self):
        stats, complete, issues = self.execute(lambda m, r, s: r.append(dict(r[0])))
        self.assertEqual(next(s for s in stats if s["language"] == "cpp")["count"], 1)
        self.assertTrue(any(s["duplicate_trials"] == "1" for s in complete))
        self.assertTrue(any("Powielone" in i["issue"] for i in issues))

    def test_rejected_excluded(self):
        def mutate(m, r, s):
            r[0].update(status="wrong_result", actual_words=3, reason="wrong")

        stats, _, issues = self.execute(mutate)
        self.assertEqual(next(s for s in stats if s["language"] == "cpp")["count"], 1)
        self.assertTrue(any("odrzucona" in i["issue"] for i in issues))

    def test_corrupt_valid_row_is_excluded(self):
        for field, value in [
            ("unit", "ms"),
            ("sha256", "bad"),
            ("actual_words", 3),
            ("elapsed", ""),
            ("elapsed", "-1"),
            ("position", "2"),
            ("status", "unknown"),
        ]:
            with self.subTest(field=field, value=value):
                stats, _, issues = self.execute(lambda m, r, s: r[0].update({field: value}))
                self.assertTrue(issues)
                self.assertEqual(next(s for s in stats if s["language"] == "cpp")["count"], 1)

    def test_unknown_pair_and_summary_mismatch(self):
        _, _, issues = self.execute(lambda m, r, s: r[0].update(language="other"))
        self.assertTrue(any("Nieoczekiwana" in i["issue"] for i in issues))
        _, _, issues = self.execute(lambda m, r, s: s.update(valid=0))
        self.assertTrue(any("Globalne" in i["issue"] for i in issues))


if __name__ == "__main__":
    unittest.main()
