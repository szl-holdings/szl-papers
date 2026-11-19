"""Fail-closed validator for non-normative external research intake.

Never imports experiment code, contacts providers, requests credentials, or
authorizes training, publishing, PR merge or production admission.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
from urllib.parse import urlparse

SCHEMA = "szl.frontier-research-intake/v1"
MAX_BYTES = 131072
ID = re.compile(r"RQ-[A-Z0-9-]{2,24}\Z")
REPO = re.compile(r"[A-Za-z0-9_.-]{2,100}\Z")
DOMAIN_ALLOWLIST = {
    "arxiv.org", "proceedings.mlr.press", "proceedings.iclr.cc",
    "github.com", "discoveredmaterials.com", "www.vals.ai",
}
POLICY_FALSE = (
    "run_authorized", "training_authorized",
    "public_model_promotion_authorized", "dataset_ingestion_authorized",
    "provider_or_account_mutation_authorized", "imported_upstream_code",
    "immutable_upstream_shas_verified", "live_training_evaluations_verified",
    "source_and_hub_runtime_alignment_verified",
)
TOP_FIELDS = {"schema", "as_of_utc_date", "observed_repository_listing", "policy", "experiments"}
OBS_FIELDS = {
    "organization", "scope", "returned", "archived", "active",
    "private_visible", "all_repositories_semantically_audited", "all_ci_green_claim",
}
EXPERIMENT_FIELDS = {
    "id", "method", "paper", "code", "targets", "hypothesis", "control",
    "primary_metric", "negative_control", "required_gates",
}


class IntakeHold(ValueError):
    pass


def _distinct_pairs(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise IntakeHold("DUPLICATE_JSON_KEY")
        obj[key] = value
    return obj


def _deny_nonfinite(value):
    raise IntakeHold("NONFINITE_JSON")


def _text(item, minimum=4, maximum=1200):
    return type(item) is str and minimum <= len(item.strip()) <= maximum


def _url(item):
    if not _text(item, 16, 300):
        return False
    parsed = urlparse(item)
    return (
        parsed.scheme == "https"
        and parsed.hostname in DOMAIN_ALLOWLIST
        and parsed.username is None
        and parsed.password is None
        and not parsed.fragment
        and not parsed.query
    )


def validate(value):
    if type(value) is not dict or set(value) != TOP_FIELDS:
        raise IntakeHold("TOP_SCHEMA_INVALID")
    if value["schema"] != SCHEMA or value["as_of_utc_date"] != "2026-11-19":
        raise IntakeHold("SCHEMA_OR_OBSERVATION_DATE_INVALID")

    obs = value["observed_repository_listing"]
    if type(obs) is not dict or set(obs) != OBS_FIELDS:
        raise IntakeHold("OBSERVATION_FIELDS_INVALID")
    if obs["organization"] != "szl-holdings":
        raise IntakeHold("SOURCE_ORGANIZATION_INVALID")
    if obs["scope"] != "two-pages-of-authorized-github-repository-search-not-a-code-or-ci-audit":
        raise IntakeHold("INVENTORY_COVERAGE_OVERCLAIM")
    for field in ("returned", "archived", "active", "private_visible"):
        if type(obs[field]) is not int or obs[field] < 0:
            raise IntakeHold("CENSUS_COUNT_INVALID")
    if (obs["returned"] != obs["active"] + obs["archived"]
            or obs["private_visible"] > obs["returned"]):
        raise IntakeHold("CENSUS_ACCOUNTING_INVALID")
    if obs["all_repositories_semantically_audited"] is not False:
        raise IntakeHold("SEMANTIC_AUDIT_NOT_PROVED")
    if obs["all_ci_green_claim"] is not False:
        raise IntakeHold("CI_COVERAGE_NOT_PROVED")

    policy = value["policy"]
    if type(policy) is not dict or set(policy) != {"stage", *POLICY_FALSE}:
        raise IntakeHold("POLICY_SCHEMA_INVALID")
    if policy["stage"] != "SOURCE_RESEARCH_ONLY":
        raise IntakeHold("RESEARCH_NOT_ADMITTED")
    for flag in POLICY_FALSE:
        if policy[flag] is not False:
            raise IntakeHold("UNSUPPORTED_AUTHORIZATION_OR_MEASUREMENT")

    experiments = value["experiments"]
    if type(experiments) is not list or not 1 <= len(experiments) <= 32:
        raise IntakeHold("EXPERIMENT_COUNT_INVALID")
    seen = set()
    for experiment in experiments:
        if type(experiment) is not dict or set(experiment) != EXPERIMENT_FIELDS:
            raise IntakeHold("EXPERIMENT_SCHEMA_INVALID")
        ident = experiment["id"]
        if type(ident) is not str or not ID.fullmatch(ident) or ident in seen:
            raise IntakeHold("EXPERIMENT_ID_INVALID_OR_DUPLICATED")
        seen.add(ident)
        for field in ("method", "hypothesis", "control", "negative_control"):
            if not _text(experiment[field]):
                raise IntakeHold("EXPERIMENT_DESCRIPTION_MISSING")
        if not _url(experiment["paper"]):
            raise IntakeHold("PAPER_SOURCE_UNTRUSTED_OR_MISSING")
        code = experiment["code"]
        if code is not None and (not _url(code) or not code.startswith("https://github.com/")):
            raise IntakeHold("CODE_SOURCE_UNTRUSTED")
        targets = experiment["targets"]
        if (
            type(targets) is not list or not 1 <= len(targets) <= 12
            or len(set(str(x) for x in targets)) != len(targets)
            or any(type(x) is not str or not REPO.fullmatch(x) for x in targets)
        ):
            raise IntakeHold("SZL_REPOSITORY_TARGET_INVALID")
        metric = experiment["primary_metric"]
        if type(metric) is not dict or set(metric) != {"name", "unit", "denominator"}:
            raise IntakeHold("METRIC_SCHEMA_INVALID")
        if any(not _text(metric[x]) for x in ("name", "unit", "denominator")):
            raise IntakeHold("METRIC_OR_DENOMINATOR_MISSING")
        gates = experiment["required_gates"]
        if (
            type(gates) is not list or not 3 <= len(gates) <= 12
            or len(set(str(g) for g in gates)) != len(gates)
            or any(type(g) is not str or not REPO.fullmatch(g) for g in gates)
        ):
            raise IntakeHold("EVIDENCE_GATES_MISSING")
    return {
        "schema": SCHEMA,
        "state": "SOURCE_INTAKE_VALIDATED_NOT_ADMITTED",
        "scope": "STATIC_RESEARCH_MANIFEST_ONLY",
        "repository_listing_rows": obs["returned"],
        "experiment_intakes": len(experiments),
        "approved_runs": 0,
        "models_qualified": 0,
        "publications_authorized": False,
    }


def load(path):
    if path.is_symlink() or not path.is_file():
        raise IntakeHold("INPUT_FILE_MISSING_OR_SYMLINK")
    if path.stat().st_size > MAX_BYTES:
        raise IntakeHold("INPUT_BYTE_LIMIT")
    data = path.read_bytes()
    if not data or len(data) > MAX_BYTES:
        raise IntakeHold("INPUT_BYTE_LIMIT")
    try:
        value = json.loads(
            data.decode("utf-8"), object_pairs_hook=_distinct_pairs,
            parse_constant=_deny_nonfinite
        )
    except (ValueError, UnicodeError) as exc:
        raise IntakeHold("INPUT_JSON_INVALID") from exc
    return validate(value)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args()
    try:
        result = load(args.manifest)
    except (IntakeHold, OSError) as exc:
        reason = str(exc) if isinstance(exc, IntakeHold) else "INPUT_IO_UNAVAILABLE"
        print(json.dumps({"state": "HOLD", "reason": reason}))
        return 2
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
