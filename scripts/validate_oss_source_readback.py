"""Offline comparison of declared OSS pins with a separate public-API readback.

A correct match is evidence of *two recorded data sets agreeing*, not a signed
attestation, rights approval, GitHub authentication or an independent code audit.
This module does no network, execution, model loading or provider mutation.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re

from validate_oss_source_pins import IntakeHold, validate as validate_v1

SCHEMA = "szl.oss-public-source-readback/v1"
MAX_BYTES = 131072
HEX40 = re.compile(r"[0-9a-f]{40}\Z")
SOURCE = {
    "repository", "commit_sha_observed", "repository_metadata_license_head",
    "commit_api_http", "repo_api_http", "archived", "private",
}
OWNER = {"name", "source", "archived", "private"}
TOP = {
    "schema", "captured_at_utc", "source_manifest_blob_sha", "acquisition",
    "capture_protection", "snapshot", "authority", "upstreams", "owner_targets",
}
SNAPSHOT = {
    "organization", "returned_repository_metadata_rows", "active", "archived",
    "private_visible", "pages_returned", "page_size", "non_atomic",
    "entire_org_semantically_audited", "private_repository_names_included",
}
AUTHORITY = {
    "provider_response_authenticated_by_capture",
    "source_supply_chain_provenance_verified",
    "exact_commit_license_rights_verified", "model_or_dataset_rights_verified",
    "all_repos_audited", "source_copy_authorized", "training_authorized",
    "deployment_authorized", "commercial_release_authorized",
}


def _deny(reason: str) -> None:
    raise IntakeHold(reason)


def _keys(obj: object, keys: set[str], reason: str) -> None:
    if type(obj) is not dict or set(obj) != keys:
        _deny(reason)


def _positive(value: object) -> bool:
    return type(value) is int and value > 0


def _rows(rows: object, expected: int, reason: str) -> None:
    if type(rows) is not list or len(rows) != expected:
        _deny(reason)


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            _deny("DUPLICATE_JSON_KEY")
        result[key] = value
    return result


def _reject_nonfinite(_value):
    _deny("NONFINITE_JSON")


def _load(path: Path) -> tuple[dict, bytes]:
    if path.is_symlink() or not path.is_file():
        _deny("INPUT_UNAVAILABLE_OR_SYMLINK")
    if not 1 <= path.stat().st_size <= MAX_BYTES:
        _deny("INPUT_TOO_LARGE_OR_EMPTY")
    raw = path.read_bytes()
    if not 1 <= len(raw) <= MAX_BYTES:
        _deny("INPUT_TOO_LARGE_OR_EMPTY")
    try:
        value = json.loads(
            raw.decode("utf-8"), object_pairs_hook=_pairs, parse_constant=_reject_nonfinite
        )
    except (ValueError, UnicodeError) as exc:
        raise IntakeHold("INPUT_JSON_INVALID") from exc
    return value, raw


def _git_blob_sha(raw: bytes) -> str:
    # GitHub's ordinary Git-blob object ID, NOT an independent signature.
    return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\x00" + raw).hexdigest()


def validate_readback(manifest: object, manifest_raw: bytes, witness: object) -> dict:
    """Cross-compare recorded metadata only; no provider API is called."""
    # The reusable in-memory API must not let a caller supply an altered
    # parsed object while reusing an unchanged source blob as its "proof".
    if type(manifest_raw) is not bytes or not 1 <= len(manifest_raw) <= MAX_BYTES:
        _deny("SOURCE_MANIFEST_RAW_INVALID")
    try:
        parsed = json.loads(
            manifest_raw.decode("utf-8"),
            object_pairs_hook=_pairs,
            parse_constant=_reject_nonfinite,
        )
    except (UnicodeError, ValueError) as exc:
        raise IntakeHold("SOURCE_MANIFEST_RAW_INVALID") from exc
    if parsed != manifest:
        _deny("MANIFEST_OBJECT_NOT_BOUND_TO_RAW")
    validate_v1(manifest)
    _keys(witness, TOP, "READBACK_SCHEMA_INVALID")
    if witness["schema"] != SCHEMA:
        _deny("READBACK_VERSION_INVALID")
    observed = witness["captured_at_utc"]
    if type(observed) is not str or not observed.endswith("Z"):
        _deny("CAPTURE_TIME_INVALID")
    try:
        stamp = datetime.fromisoformat(observed[:-1] + "+00:00")
    except ValueError:
        _deny("CAPTURE_TIME_INVALID")
    if stamp.tzinfo is None or stamp.utcoffset() != timezone.utc.utcoffset(stamp):
        _deny("CAPTURE_TIME_INVALID")
    if stamp.date().isoformat() != manifest["observed_on_utc_date"]:
        _deny("CAPTURE_DATE_MISMATCH")
    if (
        type(witness["source_manifest_blob_sha"]) is not str
        or not HEX40.fullmatch(witness["source_manifest_blob_sha"])
        or witness["source_manifest_blob_sha"] != _git_blob_sha(manifest_raw)
    ):
        _deny("SOURCE_MANIFEST_BYTES_NOT_BOUND")
    if witness["acquisition"] != "GH_CLI_GITHUB_REST_COMMIT_AND_CURRENT_REPO_METADATA":
        _deny("READBACK_ACQUISITION_UNSUPPORTED")
    if witness["capture_protection"] != "UNSIGNED_SINGLE_OPERATOR_REPORT_NOT_INDEPENDENT_ATTESTATION":
        _deny("FALSE_READBACK_ATTESTATION")

    scope = witness["snapshot"]
    _keys(scope, SNAPSHOT, "ORG_SCOPE_FIELDS_INVALID")
    if scope["organization"] != "szl-holdings" or scope["page_size"] != 100:
        _deny("ORG_SCOPE_IDENTITY_INVALID")
    for field in ("returned_repository_metadata_rows", "active", "archived", "private_visible", "pages_returned", "page_size"):
        if type(scope[field]) is not int or scope[field] < 0:
            _deny("ORG_SCOPE_COUNTS_INVALID")
    if scope["returned_repository_metadata_rows"] == 0 or scope["pages_returned"] == 0:
        _deny("ORG_SCOPE_COUNTS_INVALID")
    if (
        scope["active"] + scope["archived"] != scope["returned_repository_metadata_rows"]
        or scope["private_visible"] > scope["returned_repository_metadata_rows"]
        or scope["pages_returned"] !=
        (scope["returned_repository_metadata_rows"] + scope["page_size"] - 1) // scope["page_size"]
    ):
        _deny("ORG_SCOPE_ACCOUNTING_INVALID")
    if (
        scope["non_atomic"] is not True
        or scope["entire_org_semantically_audited"] is not False
        or scope["private_repository_names_included"] is not False
    ):
        _deny("ORG_SCOPE_OVERCLAIM")
    authority = witness["authority"]
    _keys(authority, AUTHORITY, "AUTHORITY_FIELDS_INVALID")
    if any(authority[key] is not False for key in AUTHORITY):
        _deny("UNVERIFIED_AUTHORITY_CLAIM")

    expected_sources = {src["repository"]: src for src in manifest["sources"]}
    upstreams = witness["upstreams"]
    _rows(upstreams, len(expected_sources), "UPSTREAM_COVERAGE_INCOMPLETE")
    # Check the full identity population *before* evaluating individual
    # content matches, so duplicate identities cannot be hidden by a faster
    # SHA mismatch classification in a same-count substitution.
    seen_sources: set[str] = set()
    for row in upstreams:
        _keys(row, SOURCE, "UPSTREAM_RECORD_FIELDS_INVALID")
        repo = row["repository"]
        if type(repo) is not str or repo not in expected_sources or repo.lower() in seen_sources:
            _deny("UPSTREAM_IDENTITY_UNKNOWN_OR_DUPLICATED")
        seen_sources.add(repo.lower())
    for row in upstreams:
        repo = row["repository"]
        source = expected_sources[repo]
        if (
            row["commit_sha_observed"] != source["revision"]
            or row["repository_metadata_license_head"] != source["license"]
        ):
            _deny("UPSTREAM_COMMIT_OR_HEAD_LICENSE_METADATA_MISMATCH")
        if (
            type(row["commit_api_http"]) is not int or row["commit_api_http"] != 200
            or type(row["repo_api_http"]) is not int or row["repo_api_http"] != 200
        ):
            _deny("UPSTREAM_READBACK_NOT_CONFIRMED")
        if row["archived"] is not False or row["private"] is not False:
            _deny("UPSTREAM_SCOPE_NOT_PUBLIC_ACTIVE")

    expected_owners = {
        *(src["target"] for src in manifest["sources"]),
        *(name for exp in manifest["experiments"] for name in exp["target_repositories"]),
    }
    targets = witness["owner_targets"]
    _rows(targets, len(expected_owners), "OWNER_TARGET_COVERAGE_INCOMPLETE")
    seen_owners: set[str] = set()
    for row in targets:
        _keys(row, OWNER, "OWNER_RECORD_FIELDS_INVALID")
        name = row["name"]
        if type(name) is not str or name not in expected_owners or name.lower() in seen_owners:
            _deny("OWNER_TARGET_UNKNOWN_OR_DUPLICATED")
        seen_owners.add(name.lower())
        if row["source"] != "GITHUB_ORG_REPO_METADATA_NONATOMIC":
            _deny("OWNER_SOURCE_UNSUPPORTED")
        if row["private"] is not False or row["archived"] is not False:
            _deny("OWNER_NOT_ACTIVE_PUBLIC")

    return {
        "state": "RECORDED_PUBLIC_READBACK_CONSISTENT_NOT_ATTESTED",
        "as_of_utc": observed,
        "org_metadata_rows": scope["returned_repository_metadata_rows"],
        "active_metadata_repos": scope["active"],
        "archived_metadata_repos": scope["archived"],
        "private_visible_metadata_repos": scope["private_visible"],
        "public_upstream_commit_matches": len(upstreams),
        "current_repo_head_license_metadata_matches": len(upstreams),
        "public_owner_targets_listed_active": len(targets),
        "license_metadata_unresolved": sum(
            src["license"] == "NOASSERTION" for src in manifest["sources"]
        ),
        "provider_response_authenticated": False,
        "license_or_asset_rights_proven": False,
        "independent_source_attestation_verified": False,
        "all_repositories_semantically_audited": False,
        "training_or_deployment_authorized": False,
        "commercial_release_authorized": False,
    }


def load_pair(manifest_path: Path, witness_path: Path) -> dict:
    manifest, raw = _load(Path(manifest_path))
    witness, _ = _load(Path(witness_path))
    return validate_readback(manifest, raw, witness)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("witness", type=Path)
    args = parser.parse_args()
    try:
        result = load_pair(args.manifest, args.witness)
    except (IntakeHold, OSError) as exc:
        reason = str(exc) if isinstance(exc, IntakeHold) else "FILE_IO_UNAVAILABLE"
        print(json.dumps({"state": "HOLD", "reason": reason}))
        return 2
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
