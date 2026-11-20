# SPDX-License-Identifier: Apache-2.0
"""Offline, stdlib-only source-honesty gate for the non-normative SZL robotics intake.

Never imports or executes model code, robot controllers, private datasets or providers.
It checks source claims and PR preregistration structure, not real-robot safety.
"""
from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlsplit
import sys

SCHEMA = "szl.embodied-evidence-research/v1"
TOP = frozenset({
    "schema", "as_of_utc_date", "title", "status", "owner", "source_authority",
    "scope", "leaders", "protocol", "hypotheses", "negative_controls",
    "release_gates", "commercialization", "evidence", "claims"
})
HOSTS = frozenset({
    "github.com", "developer.nvidia.com", "arxiv.org", "huggingface.co",
    "deepmind.google", "sre.google", "slsa.dev", "www.rfc-editor.org", "www.w3.org"
})
SCOPE_FALSE = frozenset({
    "real_robot_control_authorized", "training_authorized", "dataset_ingestion_authorized",
    "model_promotion_authorized", "production_qualified",
    "provider_or_account_mutation_authorized", "pricing_approved",
    "payment_settlement_verified"
})
EVIDENCE_NONE = frozenset({
    "current_source_commit", "current_dataset_revision", "current_model_weights_revision"
})
EVIDENCE_FALSE = frozenset({
    "completed_experiment", "benchmark_quality_qualified", "software_deployed"
})
EVIDENCE_ZERO = frozenset({
    "real_robot_trials", "real_robot_training_runs", "simulated_trials",
    "verified_signature_count"
})


def _mapping(value: object) -> dict:
    return value if type(value) is dict else {}


def _nonempty(value: object) -> bool:
    return type(value) is str and bool(value.strip()) and len(value) <= 1000


def _unique(records: object, key: str) -> bool:
    return (type(records) is list and
            all(type(item) is dict and _nonempty(item.get(key)) for item in records)
            and len(set(item[key] for item in records)) == len(records))


def _safe_source(url: object) -> bool:
    if not _nonempty(url):
        return False
    parsed = urlsplit(url)
    return (parsed.scheme == "https" and parsed.hostname in HOSTS
            and not parsed.username and not parsed.password and not parsed.fragment
            and not parsed.port)


def validate(document: object) -> list[str]:
    """Return fixed refusal codes. An empty list is STRUCTURAL_SOURCE_ONLY, not approval."""
    failures: list[str] = []
    if type(document) is not dict or set(document) != TOP:
        return ["TOP_SHAPE"]
    if document["schema"] != SCHEMA or document["status"] != "SOURCE_ONLY_NOT_ADMITTED":
        failures.append("SOURCE_STAGE")
    if document["source_authority"] != "szl-holdings/szl-papers":
        failures.append("SOURCE_OWNER")
    if not all(_nonempty(document[k]) for k in ("title", "owner", "as_of_utc_date")):
        failures.append("METADATA")

    scope = _mapping(document["scope"])
    if scope.get("environment") != "SIMULATED_ONLY" or any(
        scope.get(key) is not False for key in SCOPE_FALSE
    ):
        failures.append("SCOPE_AUTHORITY_HOLD")

    leaders = document["leaders"]
    if (not _unique(leaders, "name") or len(leaders) < 5 or
            any(not _safe_source(item.get("url")) or
                not _nonempty(item.get("license_rights")) or
                not _nonempty(item.get("adoption"))
                for item in leaders)):
        failures.append("LEADER_SOURCE_RIGHTS")

    protocol = _mapping(document["protocol"])
    if (protocol.get("hardware_egress") != "FORBIDDEN_IN_INITIAL_PILOT" or
            protocol.get("signer_authority") != "EXTERNAL_VERIFIER_REQUIRED" or
            not all(type(protocol.get(k)) is list and len(protocol[k]) >= 3
                    for k in ("input_fields", "output_states", "force_denial_if_missing")) or
            "DENY" not in protocol.get("output_states", [])):
        failures.append("PROTOCOL_BOUNDARY")

    hypotheses = document["hypotheses"]
    if (not _unique(hypotheses, "id") or
            set(h["id"] for h in hypotheses) != {"H1", "H2", "H3"}):
        failures.append("HYPOTHESIS_POPULATION")
    else:
        for h in hypotheses:
            if (not all(_nonempty(h.get(k)) for k in (
                    "claim", "primary_metric", "unit", "denominator", "baseline", "target")) or
                    h.get("measured_value", "MISSING") is not None or
                    h.get("baseline_measured_value", "MISSING") is not None):
                failures.append("UNMEASURED_HYPOTHESIS_" + h["id"])

    negative = document["negative_controls"]
    if (not _unique(negative, "id") or len(negative) < 12 or
            any(n.get("expected") != "DENY" or not _nonempty(n.get("case"))
                for n in negative)):
        failures.append("NEGATIVE_CONTROL_HOLD")

    gates = document["release_gates"]
    if (not _unique(gates, "id") or len(gates) != 10 or
            {g["id"] for g in gates} != {"G%02d" % i for i in range(1, 11)} or
            any(g.get("state") != "HOLD" or not _nonempty(g.get("name")) for g in gates)):
        failures.append("RELEASE_GATE_HOLD")

    business = _mapping(document["commercialization"])
    if (not all(_nonempty(business.get(k)) for k in (
            "first_customer_hypothesis", "product", "free_offer", "paid_offer_hypothesis"))
            or business.get("actual_customer_count", "MISSING") is not None
            or business.get("revenue_usd", "MISSING") is not None
            or business.get("pricing_approved") is not False
            or business.get("x402_settlements_verified") is not False):
        failures.append("COMMERCIAL_OVERCLAIM")

    evidence = _mapping(document["evidence"])
    if (any(evidence.get(k, "MISSING") is not None for k in EVIDENCE_NONE)
            or any(evidence.get(k) is not False for k in EVIDENCE_FALSE)
            or any(type(evidence.get(k)) is not int or evidence[k] != 0
                   for k in EVIDENCE_ZERO)):
        failures.append("EVIDENCE_OVERCLAIM")

    claims = _mapping(document["claims"])
    if not claims or any(value is not False for value in claims.values()):
        failures.append("ESTATE_READINESS_OVERCLAIM")
    return failures


def _no_duplicate_keys(pairs: list[tuple[str, object]]) -> dict:
    result: dict = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("DUPLICATE_JSON_KEY")
        result[key] = value
    return result


def load(path: Path) -> object:
    raw = path.read_bytes()
    if len(raw) > 100_000:
        raise ValueError("OVERSIZED_INPUT")
    return json.loads(raw.decode("utf-8"), object_pairs_hook=_no_duplicate_keys)


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: validate_embodied_research.py path", file=sys.stderr)
        return 2
    try:
        errors = validate(load(Path(argv[1])))
    except (OSError, UnicodeError, ValueError) as exc:
        print("HOLD_PARSE_" + type(exc).__name__)
        return 1
    if errors:
        print("HOLD_SOURCE_CONTRACT " + ",".join(sorted(set(errors))))
        return 1
    print("PASS_STRUCTURAL_SOURCE_ONLY_NOT_AUTHORIZED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
