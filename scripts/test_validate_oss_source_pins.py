"""Synthetic, no-provider negative controls for global OSS method discovery."""
from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest

from validate_oss_source_pins import IntakeHold, load, validate

BASE = Path(__file__).resolve().parents[1] / "docs/research/oss-global-source-pins-20261120.json"


def sample():
    return json.loads(BASE.read_text(encoding="utf-8"))


class OSSSourcePinsTest(unittest.TestCase):
    def assert_hold(self, payload, reason):
        with self.assertRaises(IntakeHold) as error:
            validate(payload)
        self.assertEqual(str(error.exception), reason)

    def test_real_sample_is_intake_not_authority(self):
        out = load(BASE)
        self.assertEqual(out["sampled_public_sources"], 17)
        self.assertEqual(out["unmeasured_experiments"], 6)
        self.assertEqual(out["unresolved_github_license_metadata"], 1)
        self.assertFalse(out["code_imported"])
        self.assertFalse(out["training_or_deployment_authorized"])

    def test_input_immutable(self):
        data = sample()
        before = deepcopy(data)
        validate(data)
        self.assertEqual(data, before)

    def test_worldwide_claim_denied(self):
        for key in ("whole_world_scraped", "complete_source_audit", "license_cleared"):
            data = sample()
            data["scope"][key] = True
            self.assert_hold(data, "COVERAGE_CLAIM_UNSUPPORTED")

    def test_source_pop_count_and_bool_confusion(self):
        data = sample()
        data["sources"].pop()
        self.assert_hold(data, "SOURCE_COVERAGE_MISMATCH")
        data = sample()
        data["scope"]["source_count"] = True
        self.assert_hold(data, "COVERAGE_COUNT_INVALID")

    def test_source_sha_pinning_and_commit_url(self):
        data = sample()
        data["sources"][0]["revision"] = "main"
        self.assert_hold(data, "SOURCE_NOT_IMMUTABLY_PINNED")
        data = sample()
        data["sources"][0]["revision"] = "f" * 40
        self.assert_hold(data, "REVISION_URL_DRIFT")

    def test_code_license_is_metadata_not_rights(self):
        data = sample()
        data["sources"][0]["license_evidence"] = "LEGALLY_CLEARED"
        self.assert_hold(data, "FALSE_LICENSE_AUTHORITY")
        data = sample()
        data["sources"][0]["asset_rights"] = "FULL_RIGHTS"
        self.assert_hold(data, "UNAUTHORIZED_ASSET_IMPORT_OR_RIGHTS")
        data = sample()
        data["sources"][0]["code_imported"] = True
        self.assert_hold(data, "UNAUTHORIZED_ASSET_IMPORT_OR_RIGHTS")

    def test_qwen_repo_license_unknown_is_not_approval(self):
        qwen = [r for r in sample()["sources"] if r["id"] == "QWEN3"]
        self.assertEqual(len(qwen), 1)
        self.assertEqual(qwen[0]["license"], "NOASSERTION")
        self.assertEqual(qwen[0]["asset_rights"], "UNASSESSED")

    def test_no_future_billability_from_nominal_pass(self):
        for key in sample()["authority"]:
            data = sample()
            data["authority"][key] = True
            self.assert_hold(data, "UNSUPPORTED_AUTHORIZATION")

    def test_paper_link_cannot_embed_credentials(self):
        data = sample()
        data["sources"][0]["reference"] = "https://a:b@arxiv.org/abs/2407.16741"
        self.assert_hold(data, "INVALID_PRIMARY_REFERENCE")
        data = sample()
        data["sources"][0]["reference"] = "https://arxiv.org/abs/2407.16741?token=abc"
        self.assert_hold(data, "INVALID_PRIMARY_REFERENCE")

    def test_duplicate_records_and_disguised_owners(self):
        data = sample()
        data["sources"][1]["id"] = data["sources"][0]["id"]
        self.assert_hold(data, "SOURCE_ID_INVALID_OR_DUPLICATE")
        data = sample()
        data["experiments"][0]["target_repositories"] = ["../../admin"]
        self.assert_hold(data, "EXPERIMENT_OWNERS_INVALID")

    def test_missing_qrels_denominator_is_hold(self):
        data = sample()
        data["experiments"][1]["planned_denominator"] = ""
        self.assert_hold(data, "METRIC_OR_DENOMINATOR_MISSING")
        data = sample()
        data["experiments"][1]["stage"] = "PUBLISHED"
        self.assert_hold(data, "PREMATURE_EXPERIMENT_OR_RELEASE_CLAIM")

    def test_unknown_source_does_not_create_admitted_experiment(self):
        data = sample()
        data["experiments"][0]["source_ids"] = ["GHOST"]
        self.assert_hold(data, "UNKNOWN_EXPERIMENT_SOURCE")

    def test_symlink_and_duplicate_key_and_nonfinite_hold(self):
        with tempfile.TemporaryDirectory() as tmp:
            file = Path(tmp) / "bad.json"
            file.write_text('{"a":1,"a":2}', encoding="utf-8")
            with self.assertRaises(IntakeHold):
                load(file)
            file.write_text('{"v":NaN}', encoding="utf-8")
            with self.assertRaises(IntakeHold):
                load(file)
            big = Path(tmp) / "big.json"
            big.write_text("z" * 131073, encoding="utf-8")
            with self.assertRaisesRegex(IntakeHold, "INPUT_SIZE_INVALID"):
                load(big)
            alias = Path(tmp) / "link.json"
            try:
                alias.symlink_to(BASE)
            except OSError:
                return
            with self.assertRaisesRegex(IntakeHold, "INPUT_FILE_UNAVAILABLE_OR_SYMLINK"):
                load(alias)


if __name__ == "__main__":
    unittest.main()
