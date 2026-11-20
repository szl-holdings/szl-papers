"""Independent offline negative tests for the untrusted ECG source intake."""
import json
import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from assess_evidence_closure_graph import assess, SCHEMA

SHA = "a" * 40
def node(name="alpha", parent=None):
    return {
        "id": name, "source_commit": SHA,
        "depends_on": parent or [],
        "test_digest": "b" * 64,
        "review_digest": "c" * 64,
        "receipt_digest": "d" * 64,
        "declared_dissent_resolved": True,
    }
def fixture():
    return {
        "schema": SCHEMA,
        "source_repo": "szl-holdings/szl-papers",
        "source_commit": SHA,
        "claims": [node()],
    }
def evaluate(obj):
    return assess(json.dumps(obj).encode("utf-8"))

class EvidenceClosureGraphTests(unittest.TestCase):
    def assert_hold(self, obj, reason=None):
        response = evaluate(obj)
        self.assertEqual(response["state"], "HOLD")
        self.assertFalse(response["production_ready"])
        self.assertFalse(response["merge_authorized"])
        if reason:
            self.assertEqual(response["reason"], reason)

    def test_well_formed_is_never_admitted(self):
        out = evaluate(fixture())
        self.assertEqual(out["state"], "REVIEW_CANDIDATE_ONLY")
        for f in ("independent_evidence_verified","runtime_verified",
                  "merge_authorized","publication_authorized","production_ready"):
            self.assertFalse(out[f])

    def test_forged_self_consistent_digests_remain_unverified(self):
        f = fixture()
        for k in ("test_digest","review_digest","receipt_digest"):
            f["claims"][0][k] = "e" * 64
        self.assertFalse(evaluate(f)["independent_evidence_verified"])

    def test_missing_source_sha(self):
        f = fixture()
        f["source_commit"] = "f" * 40
        self.assert_hold(f, "SOURCE_COMMIT_MISMATCH")

    def test_cycles(self):
        f = fixture()
        f["claims"] = [node("one", ["two"]), node("two", ["one"])]
        self.assert_hold(f, "CYCLIC_CLAIM_GRAPH")

    def test_self_edge(self):
        f = fixture()
        f["claims"] = [node("one", ["one"])]
        self.assert_hold(f, "SELF_DEPENDENCY")

    def test_unknown_dependency(self):
        f = fixture()
        f["claims"] = [node("one", ["missing"])]
        self.assert_hold(f, "UNKNOWN_DEPENDENCY")

    def test_duplicate_id(self):
        f = fixture()
        f["claims"].append(node())
        self.assert_hold(f, "INVALID_OR_DUPLICATE_CLAIM_ID")

    def test_duplicate_parent(self):
        f = fixture()
        f["claims"] = [node("a", ["b","b"]), node("b")]
        self.assert_hold(f, "INVALID_PARENT_LIST")

    def test_unresolved_dissent(self):
        f = fixture()
        f["claims"][0]["declared_dissent_resolved"] = False
        self.assert_hold(f, "DECLARED_DISSENT_UNRESOLVED")

    def test_unauthorized_authority_injection(self):
        f = fixture()
        f["claims"][0]["production_ready"] = True
        self.assert_hold(f, "CLAIM_SCHEMA_MISMATCH")

    def test_extra_release_authority_injection(self):
        f = fixture()
        f["release_authorized"] = True
        self.assert_hold(f, "TOP_LEVEL_SCHEMA_MISMATCH")

    def test_invalid_sha(self):
        f = fixture()
        f["source_commit"] = "../secrets"
        self.assert_hold(f, "INVALID_SOURCE_COMMIT")

    def test_invalid_digest(self):
        f = fixture()
        f["claims"][0]["receipt_digest"] = "signed-trust-me"
        self.assert_hold(f, "INVALID_DECLARED_DIGEST")

    def test_payload_size_limit(self):
        self.assertEqual(assess(b"x"*65537)["reason"],"PAYLOAD_UNAVAILABLE_OR_OVERSIZED")

    def test_duplicate_json_keys(self):
        body = b'{"schema":"szl.evidence-closure-graph/v1","schema":"bad"}'
        self.assertEqual(assess(body)["reason"],"MALFORMED_JSON")

    def test_non_finite_value(self):
        self.assertEqual(assess(b'{"x":NaN}')["reason"],"MALFORMED_JSON")

    def test_empty_claims(self):
        f = fixture()
        f["claims"] = []
        self.assert_hold(f, "INVALID_NODE_COUNT")

    def test_graph_order_agnostic(self):
        f = fixture()
        f["claims"] = [node("c", ["b"]), node("a"), node("b",["a"])]
        out = evaluate(f)
        self.assertEqual(out["state"],"REVIEW_CANDIDATE_ONLY")
        self.assertEqual(out["edges_checked"],2)

    def test_cyclic_negative_fuzz_cases(self):
        for i in range(40):
            f = fixture()
            name1, name2 = f"node{i}", f"edge{i}"
            f["claims"] = [node(name1, [name2]), node(name2, [name1])]
            with self.subTest(i=i):
                self.assert_hold(f,"CYCLIC_CLAIM_GRAPH")

    def test_trust_fields_always_false_under_valid_graph(self):
        for n in range(1,16):
            f=fixture()
            f["claims"]=[node(f"c{i}",[f"c{i-1}"] if i else []) for i in range(n)]
            with self.subTest(n=n):
                out=evaluate(f)
                self.assertFalse(out["production_ready"])
                self.assertFalse(out["merge_authorized"])
                self.assertFalse(out["independent_evidence_verified"])

if __name__ == "__main__":
    unittest.main(verbosity=2)