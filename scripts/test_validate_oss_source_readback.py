"""Synthetic negative controls for source-owner/OSS GitHub readback alignment."""
from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest

from validate_oss_source_readback import (
    IntakeHold, _git_blob_sha, load_pair, validate_readback,
)

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "docs/research/oss-global-source-pins-20261120.json"
WITNESS = ROOT / "docs/research/oss-source-readback-20261120.json"


def fixture():
    raw = MANIFEST.read_bytes()
    return json.loads(raw), raw, json.loads(WITNESS.read_text(encoding="utf-8"))


class ReadbackContractTest(unittest.TestCase):
    def hold(self, manifest, raw, witness, expected):
        with self.assertRaises(IntakeHold) as e:
            validate_readback(manifest, raw, witness)
        self.assertEqual(str(e.exception), expected)

    def test_actual_source_records_agree_but_are_not_attestations(self):
        r = load_pair(MANIFEST, WITNESS)
        self.assertEqual(r["state"], "RECORDED_PUBLIC_READBACK_CONSISTENT_NOT_ATTESTED")
        self.assertEqual(r["public_upstream_commit_matches"], 17)
        self.assertEqual(r["public_owner_targets_listed_active"], 16)
        self.assertEqual(r["org_metadata_rows"], 182)
        self.assertEqual(r["license_metadata_unresolved"], 1)
        for field in ("provider_response_authenticated", "license_or_asset_rights_proven",
                      "independent_source_attestation_verified",
                      "all_repositories_semantically_audited",
                      "training_or_deployment_authorized", "commercial_release_authorized"):
            self.assertIs(r[field], False)

    def test_manifest_git_blob_bytes_bound_to_readback(self):
        manifest, raw, witness = fixture()
        self.assertEqual(_git_blob_sha(raw), witness["source_manifest_blob_sha"])
        witness["source_manifest_blob_sha"] = "f" * 40
        self.hold(manifest, raw, witness, "SOURCE_MANIFEST_BYTES_NOT_BOUND")

    def test_source_bytes_changing_even_if_claims_correspond_is_hold(self):
        manifest, raw, witness = fixture()
        changed = raw.replace(b"OpenHands/OpenHands", b"OpenHands/OtherHand")
        self.assertNotEqual(raw, changed)
        altered = json.loads(changed)
        self.hold(altered, changed, witness, "SOURCE_MANIFEST_BYTES_NOT_BOUND")

    def test_same_count_wrong_upstream_sha_is_not_provider_readback(self):
        manifest, raw, witness = fixture()
        witness["upstreams"][0]["commit_sha_observed"] = witness["upstreams"][1]["commit_sha_observed"]
        self.hold(manifest, raw, witness, "UPSTREAM_COMMIT_OR_HEAD_LICENSE_METADATA_MISMATCH")

    def test_same_count_wrong_source_or_duplicate_fails(self):
        manifest, raw, witness = fixture()
        witness["upstreams"][0]["repository"] = "outside/unknown"
        self.hold(manifest, raw, witness, "UPSTREAM_IDENTITY_UNKNOWN_OR_DUPLICATED")
        manifest, raw, witness = fixture()
        witness["upstreams"][0]["repository"] = witness["upstreams"][1]["repository"]
        self.hold(manifest, raw, witness, "UPSTREAM_IDENTITY_UNKNOWN_OR_DUPLICATED")

    def test_omitted_record_is_not_completed_coverage(self):
        manifest, raw, witness = fixture()
        witness["upstreams"].pop()
        self.hold(manifest, raw, witness, "UPSTREAM_COVERAGE_INCOMPLETE")

    def test_wrong_license_or_unconfirmed_provider_status_holds(self):
        manifest, raw, witness = fixture()
        witness["upstreams"][0]["repository_metadata_license_head"] = "GPL-3.0"
        self.hold(manifest, raw, witness, "UPSTREAM_COMMIT_OR_HEAD_LICENSE_METADATA_MISMATCH")
        for bad in (401, 403, 429, 503, 200.0, True):
            manifest, raw, witness = fixture()
            witness["upstreams"][0]["commit_api_http"] = bad
            self.hold(manifest, raw, witness, "UPSTREAM_READBACK_NOT_CONFIRMED")

    def test_qwen_noassertion_is_never_cleared_by_matching_spdx(self):
        manifest, raw, witness = fixture()
        matches = [r for r in witness["upstreams"] if r["repository"] == "QwenLM/Qwen3"]
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0]["repository_metadata_license_head"], "NOASSERTION")
        self.assertFalse(witness["authority"]["exact_commit_license_rights_verified"])
        self.assertEqual(validate_readback(manifest, raw, witness)["license_metadata_unresolved"], 1)

    def test_source_owner_omission_or_substitution_fails(self):
        manifest, raw, witness = fixture()
        witness["owner_targets"].pop()
        self.hold(manifest, raw, witness, "OWNER_TARGET_COVERAGE_INCOMPLETE")
        manifest, raw, witness = fixture()
        witness["owner_targets"][0]["name"] = "not-a-real-target"
        self.hold(manifest, raw, witness, "OWNER_TARGET_UNKNOWN_OR_DUPLICATED")
        manifest, raw, witness = fixture()
        witness["owner_targets"][0]["name"] = witness["owner_targets"][1]["name"]
        self.hold(manifest, raw, witness, "OWNER_TARGET_UNKNOWN_OR_DUPLICATED")

    def test_archived_private_or_wrong_origin_owner_rejected(self):
        for key, value, reason in [
            ("archived", True, "OWNER_NOT_ACTIVE_PUBLIC"),
            ("private", True, "OWNER_NOT_ACTIVE_PUBLIC"),
            ("source", "USER_SUPPLIED_NOT_GITHUB", "OWNER_SOURCE_UNSUPPORTED"),
        ]:
            manifest, raw, witness = fixture()
            witness["owner_targets"][0][key] = value
            self.hold(manifest, raw, witness, reason)

    def test_private_names_and_claimed_semantic_audit_cannot_be_published(self):
        for key, value in [
            ("private_repository_names_included", True),
            ("entire_org_semantically_audited", True),
            ("non_atomic", False),
        ]:
            manifest, raw, witness = fixture()
            witness["snapshot"][key] = value
            self.hold(manifest, raw, witness, "ORG_SCOPE_OVERCLAIM")

    def test_counts_and_false_permissions_fail_closed(self):
        manifest, raw, witness = fixture()
        witness["snapshot"]["active"] = 154
        self.hold(manifest, raw, witness, "ORG_SCOPE_ACCOUNTING_INVALID")
        for key in fixture()[2]["authority"]:
            manifest, raw, witness = fixture()
            witness["authority"][key] = True
            self.hold(manifest, raw, witness, "UNVERIFIED_AUTHORITY_CLAIM")

    def test_timestamp_and_reporter_claims_cannot_hide(self):
        manifest, raw, witness = fixture()
        witness["captured_at_utc"] = "2026-11-20T05:26:15"
        self.hold(manifest, raw, witness, "CAPTURE_TIME_INVALID")
        manifest, raw, witness = fixture()
        witness["capture_protection"] = "INDEPENDENTLY_SIGNED"
        self.hold(manifest, raw, witness, "FALSE_READBACK_ATTESTATION")

    def test_input_unchanged_after_verification(self):
        manifest, raw, witness = fixture()
        before = deepcopy((manifest, witness))
        validate_readback(manifest, raw, witness)
        self.assertEqual((manifest, witness), before)

    def test_invalid_disk_bytes_and_duplicate_keys_are_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            file = Path(tmp) / "bad.json"
            file.write_text('{"x":1,"x":2}', encoding="utf-8")
            with self.assertRaises(IntakeHold):
                load_pair(MANIFEST, file)
            file.write_text('{"x":NaN}', encoding="utf-8")
            with self.assertRaises(IntakeHold):
                load_pair(MANIFEST, file)
            file.write_text("z" * 131073, encoding="utf-8")
            with self.assertRaisesRegex(IntakeHold, "INPUT_TOO_LARGE_OR_EMPTY"):
                load_pair(MANIFEST, file)
            alias = Path(tmp) / "alias.json"
            try:
                alias.symlink_to(WITNESS)
            except OSError:
                return
            with self.assertRaisesRegex(IntakeHold, "INPUT_UNAVAILABLE_OR_SYMLINK"):
                load_pair(MANIFEST, alias)


if __name__ == "__main__":
    unittest.main()
