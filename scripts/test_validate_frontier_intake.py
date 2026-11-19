"""Offline falsification tests for the static, non-admitting research intake."""
from __future__ import annotations

from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "docs" / "research" / "frontier-research-intake-20261119.json"
SOURCE = Path(__file__).with_name("validate_frontier_intake.py")
spec = importlib.util.spec_from_file_location("frontier_intake", SOURCE)
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class FrontierIntakeTests(unittest.TestCase):
    def setUp(self):
        self.known = json.loads(PATH.read_text(encoding="utf-8"))

    def test_observed_manifest_is_research_only(self):
        result = checker.validate(self.known)
        self.assertEqual(result["state"], "SOURCE_INTAKE_VALIDATED_NOT_ADMITTED")
        self.assertEqual(result["repository_listing_rows"], 178)
        self.assertEqual(result["experiment_intakes"], 7)
        self.assertEqual(result["approved_runs"], 0)
        self.assertFalse(result["publications_authorized"])

    def test_discovered_2026_papers_have_explicit_falsifiers(self):
        for experiment in self.known["experiments"]:
            self.assertTrue(experiment["control"])
            self.assertTrue(experiment["negative_control"])
            self.assertTrue(experiment["primary_metric"]["denominator"])
            self.assertGreaterEqual(len(experiment["required_gates"]), 3)

    def test_policy_refuses_all_runtime_approvals(self):
        for flag in checker.POLICY_FALSE:
            with self.subTest(flag=flag):
                candidate = deepcopy(self.known)
                candidate["policy"][flag] = True
                with self.assertRaises(checker.IntakeHold):
                    checker.validate(candidate)

    def test_false_global_green_is_refused(self):
        candidate = deepcopy(self.known)
        candidate["observed_repository_listing"]["all_ci_green_claim"] = True
        with self.assertRaises(checker.IntakeHold):
            checker.validate(candidate)

    def test_false_exhaustive_code_audit_is_refused(self):
        candidate = deepcopy(self.known)
        candidate["observed_repository_listing"][
            "all_repositories_semantically_audited"
        ] = True
        with self.assertRaises(checker.IntakeHold):
            checker.validate(candidate)

    def test_census_accounting_and_booleans_are_strict(self):
        for bad in (179, True, -1, None):
            with self.subTest(bad=bad):
                candidate = deepcopy(self.known)
                candidate["observed_repository_listing"]["active"] = bad
                with self.assertRaises(checker.IntakeHold):
                    checker.validate(candidate)

    def test_duplicate_experiment_is_refused(self):
        candidate = deepcopy(self.known)
        candidate["experiments"][1]["id"] = candidate["experiments"][0]["id"]
        with self.assertRaises(checker.IntakeHold):
            checker.validate(candidate)

    def test_extra_claim_field_is_refused(self):
        candidate = deepcopy(self.known)
        candidate["experiments"][0]["measured_accuracy"] = "100%"
        with self.assertRaises(checker.IntakeHold):
            checker.validate(candidate)

    def test_missing_control_or_denominator_is_refused(self):
        for path in ("control", "denominator"):
            with self.subTest(path=path):
                candidate = deepcopy(self.known)
                experiment = candidate["experiments"][0]
                if path == "control":
                    experiment["control"] = ""
                else:
                    experiment["primary_metric"]["denominator"] = ""
                with self.assertRaises(checker.IntakeHold):
                    checker.validate(candidate)

    def test_unsafe_upstream_url_is_refused(self):
        for url in ("http://example.com/paper", "https://evil.example/paper"):
            with self.subTest(url=url):
                candidate = deepcopy(self.known)
                candidate["experiments"][0]["paper"] = url
                with self.assertRaises(checker.IntakeHold):
                    checker.validate(candidate)

    def test_source_code_is_never_loaded_or_executed(self):
        self.assertIsNone(self.known["experiments"][2]["code"])
        self.assertFalse(self.known["policy"]["imported_upstream_code"])

    def test_exact_record_set_and_ci_state(self):
        self.assertEqual(
            {x["id"] for x in self.known["experiments"]},
            {"RQ-NQ", "RQ-DT", "RQ-SH", "RQ-CRAM", "RQ-ATLAS", "RQ-MAT", "RQ-BENCH"},
        )
        self.assertFalse(self.known["policy"]["source_and_hub_runtime_alignment_verified"])

    def test_file_loader_rejects_duplicate_json_keys(self):
        with tempfile.TemporaryDirectory() as root:
            path = Path(root) / "intake.json"
            path.write_text('{"schema":"x","schema":"y"}', encoding="utf-8")
            with self.assertRaises(checker.IntakeHold):
                checker.load(path)

    def test_file_loader_rejects_symlinks(self):
        with tempfile.TemporaryDirectory() as root:
            path = Path(root) / "intake.json"
            try:
                path.symlink_to(PATH)
            except (OSError, NotImplementedError):
                self.skipTest("symlink unavailable")
            with self.assertRaises(checker.IntakeHold):
                checker.load(path)

    def test_file_loader_rejects_oversize(self):
        with tempfile.TemporaryDirectory() as root:
            path = Path(root) / "intake.json"
            path.write_bytes(b"x" * (checker.MAX_BYTES + 1))
            with self.assertRaises(checker.IntakeHold):
                checker.load(path)


if __name__ == "__main__":
    unittest.main()
