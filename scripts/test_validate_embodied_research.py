# SPDX-License-Identifier: Apache-2.0
"""Negative controls for the research-intake validator; hermetic and source-only."""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import json
import unittest

import validate_embodied_research as gate

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "docs" / "research" / "embodied-evidence-pilot-20261120.json"


class EmbodiedResearchIntakeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reference = gate.load(INPUT)

    def specimen(self):
        return deepcopy(self.reference)

    def must_hold(self, specimen, code):
        self.assertIn(code, gate.validate(specimen))

    def test_actual_fixture_is_structural_only(self):
        self.assertEqual(gate.validate(self.specimen()), [])
        self.assertEqual(self.reference["status"], "SOURCE_ONLY_NOT_ADMITTED")
        self.assertFalse(self.reference["scope"]["real_robot_control_authorized"])

    def test_top_level_unknown_field_is_refused(self):
        s = self.specimen()
        s["surprise"] = "READY"
        self.must_hold(s, "TOP_SHAPE")

    def test_model_training_and_hardware_authority_never_infer(self):
        for field in ("training_authorized", "real_robot_control_authorized",
                      "production_qualified", "model_promotion_authorized",
                      "dataset_ingestion_authorized", "provider_or_account_mutation_authorized"):
            s = self.specimen()
            s["scope"][field] = True
            self.must_hold(s, "SCOPE_AUTHORITY_HOLD")

    def test_wrong_environment_and_signer_authority(self):
        s = self.specimen()
        s["scope"]["environment"] = "ROBOT_LIVE"
        self.must_hold(s, "SCOPE_AUTHORITY_HOLD")
        s = self.specimen()
        s["protocol"]["signer_authority"] = "MODEL_SELF_ASSERTED"
        self.must_hold(s, "PROTOCOL_BOUNDARY")

    def test_no_accidental_actuator_egress(self):
        s = self.specimen()
        s["protocol"]["hardware_egress"] = "ENABLED"
        self.must_hold(s, "PROTOCOL_BOUNDARY")
        s = self.specimen()
        s["protocol"]["output_states"] = ["READY", "DEPLOYED", "EXECUTED"]
        self.must_hold(s, "PROTOCOL_BOUNDARY")

    def test_upstream_source_links_must_be_https_and_allowlisted(self):
        for url in ("http://github.com/NVIDIA/Isaac-GR00T",
                    "https://evil.example/source", "https://user:pass@github.com/x/y",
                    "https://github.com/x/y#fragment"):
            s = self.specimen()
            s["leaders"][0]["url"] = url
            self.must_hold(s, "LEADER_SOURCE_RIGHTS")

    def test_duplicate_or_missing_leader_rights_hold(self):
        s = self.specimen()
        s["leaders"][1]["name"] = s["leaders"][0]["name"]
        self.must_hold(s, "LEADER_SOURCE_RIGHTS")
        s = self.specimen()
        s["leaders"][0]["license_rights"] = ""
        self.must_hold(s, "LEADER_SOURCE_RIGHTS")

    def test_result_cannot_be_invented(self):
        for key in ("measured_value", "baseline_measured_value"):
            s = self.specimen()
            s["hypotheses"][0][key] = 0.95
            self.must_hold(s, "UNMEASURED_HYPOTHESIS_H1")

    def test_missing_denominator_is_refused(self):
        s = self.specimen()
        s["hypotheses"][1]["denominator"] = ""
        self.must_hold(s, "UNMEASURED_HYPOTHESIS_H2")

    def test_missing_or_duplicate_hypothesis_population(self):
        s = self.specimen()
        s["hypotheses"].pop()
        self.must_hold(s, "HYPOTHESIS_POPULATION")
        s = self.specimen()
        s["hypotheses"][2]["id"] = "H1"
        self.must_hold(s, "HYPOTHESIS_POPULATION")

    def test_negative_controls_required_and_independent(self):
        s = self.specimen()
        s["negative_controls"].pop()
        self.must_hold(s, "NEGATIVE_CONTROL_HOLD")
        s = self.specimen()
        s["negative_controls"][1]["id"] = "N01"
        self.must_hold(s, "NEGATIVE_CONTROL_HOLD")
        s = self.specimen()
        s["negative_controls"][2]["expected"] = "ADMIT"
        self.must_hold(s, "NEGATIVE_CONTROL_HOLD")

    def test_all_release_gates_hold(self):
        s = self.specimen()
        s["release_gates"][0]["state"] = "PASS"
        self.must_hold(s, "RELEASE_GATE_HOLD")
        s = self.specimen()
        s["release_gates"].pop()
        self.must_hold(s, "RELEASE_GATE_HOLD")

    def test_commercial_receipts_not_invented(self):
        for field, value in (("actual_customer_count", 10),
                             ("revenue_usd", 100.0),
                             ("pricing_approved", True),
                             ("x402_settlements_verified", True)):
            s = self.specimen()
            s["commercialization"][field] = value
            self.must_hold(s, "COMMERCIAL_OVERCLAIM")

    def test_no_signed_receipts_or_real_robot_trials_claimed(self):
        for field, value in (("verified_signature_count", 1),
                             ("real_robot_trials", 1),
                             ("simulated_trials", 1),
                             ("real_robot_training_runs", 1),
                             ("completed_experiment", True),
                             ("software_deployed", True),
                             ("current_model_weights_revision", "fake")):
            s = self.specimen()
            s["evidence"][field] = value
            self.must_hold(s, "EVIDENCE_OVERCLAIM")

    def test_no_cross_plane_readiness_promotion(self):
        for field in self.reference["claims"]:
            s = self.specimen()
            s["claims"][field] = True
            self.must_hold(s, "ESTATE_READINESS_OVERCLAIM")

    def test_duplicate_json_keys_refused_even_if_values_look_safe(self):
        with self.assertRaisesRegex(ValueError, "DUPLICATE_JSON_KEY"):
            json.loads('{"status":"HOLD","status":"READY"}',
                       object_pairs_hook=gate._no_duplicate_keys)


if __name__ == "__main__":
    unittest.main()
