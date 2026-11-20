"""Offline, non-authorizing structural audit for a curated public OSS method index.

Never fetches code/assets, imports a model, accesses provider authentication, trains
a model, publishes a release or proves a software/data license is legally cleared.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
from urllib.parse import urlparse

SCHEMA = "szl.oss-global-method-index/v1"
MAX_BYTES = 131072
SHA40 = re.compile(r"[0-9a-f]{40}\Z")
REPO = re.compile(r"[A-Za-z0-9_.-]{2,100}/[A-Za-z0-9_.-]{1,100}\Z")
ID = re.compile(r"[A-Z0-9-]{2,40}\Z")
TARGET = re.compile(r"[A-Za-z0-9_.-]{2,100}\Z")
LICENSES = {"MIT", "Apache-2.0", "BSD-3-Clause", "NOASSERTION"}
REFERENCE_HOSTS = {
    "arxiv.org", "github.com", "opentelemetry.io",
    "docs.sigstore.dev", "developers.cloudflare.com",
    "www.openpolicyagent.org",
}
SCOPE = {
    "kind", "source_count", "whole_world_scraped",
    "complete_source_audit", "license_cleared",
}
AUTHORITY = {
    "copied_external_code", "trained_or_deployed_models", "published_assets",
    "paid_jobs_authorized", "commercial_release_authorized",
}
SOURCE = {
    "id", "repository", "revision", "license", "license_evidence",
    "source_url", "reference", "method", "target",
    "asset_rights", "code_imported",
}
EXPERIMENT = {
    "id", "source_ids", "target_repositories", "metric", "unit",
    "planned_denominator", "negative_control", "stage",
    "source_code_copied", "release_authorized",
}


class IntakeHold(ValueError):
    """Invalid format, not verified external evidence."""


def _strict_fields(item, expected, error):
    if type(item) is not dict or set(item) != expected:
        raise IntakeHold(error)


def _distinct_json(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise IntakeHold("DUPLICATE_JSON_KEY")
        result[key] = value
    return result


def _nonfinite(value):
    raise IntakeHold("NONFINITE_JSON")


def _safe_reference(raw):
    if type(raw) is not str or not 15 <= len(raw) <= 350:
        return False
    try:
        parsed = urlparse(raw)
    except ValueError:
        return False
    return (
        parsed.scheme == "https" and parsed.hostname in REFERENCE_HOSTS
        and parsed.username is None and parsed.password is None
        and not parsed.fragment and not parsed.query
        and ".." not in parsed.path and "\\" not in parsed.path
    )


def _unique_names(rows, pattern, maximum, error):
    if (
        type(rows) is not list or not 1 <= len(rows) <= maximum
        or any(type(x) is not str or pattern.fullmatch(x) is None for x in rows)
        or len(rows) != len(set(rows))
    ):
        raise IntakeHold(error)


def validate(value):
    _strict_fields(
        value, {"schema", "observed_on_utc_date", "scope", "authority", "sources", "experiments"},
        "ROOT_SCHEMA_INVALID",
    )
    if value["schema"] != SCHEMA or value["observed_on_utc_date"] != "2026-11-20":
        raise IntakeHold("SCHEMA_OR_DATE_INVALID")
    scope = value["scope"]
    _strict_fields(scope, SCOPE, "SCOPE_SCHEMA_INVALID")
    if scope["kind"] != "CURATED_PUBLIC_SAMPLE":
        raise IntakeHold("EXHAUSTIVE_SCOPE_OVERCLAIM")
    if type(scope["source_count"]) is not int or scope["source_count"] < 1:
        raise IntakeHold("COVERAGE_COUNT_INVALID")
    if any(scope[key] is not False for key in ("whole_world_scraped", "complete_source_audit", "license_cleared")):
        raise IntakeHold("COVERAGE_CLAIM_UNSUPPORTED")
    authority = value["authority"]
    _strict_fields(authority, AUTHORITY, "AUTHORITY_SCHEMA_INVALID")
    if any(authority[key] is not False for key in AUTHORITY):
        raise IntakeHold("UNSUPPORTED_AUTHORIZATION")

    sources = value["sources"]
    if type(sources) is not list or not 1 <= len(sources) <= 64:
        raise IntakeHold("SOURCE_COUNT_INVALID")
    if len(sources) != scope["source_count"]:
        raise IntakeHold("SOURCE_COVERAGE_MISMATCH")
    seen, seen_repos = set(), set()
    unknown_license_count = 0
    for source in sources:
        _strict_fields(source, SOURCE, "SOURCE_SCHEMA_INVALID")
        sid, repo, sha = source["id"], source["repository"], source["revision"]
        if type(sid) is not str or not ID.fullmatch(sid) or sid in seen:
            raise IntakeHold("SOURCE_ID_INVALID_OR_DUPLICATE")
        if type(repo) is not str or not REPO.fullmatch(repo) or repo.lower() in seen_repos:
            raise IntakeHold("SOURCE_REPO_INVALID_OR_DUPLICATE")
        if type(sha) is not str or not SHA40.fullmatch(sha):
            raise IntakeHold("SOURCE_NOT_IMMUTABLY_PINNED")
        if source["source_url"] != f"https://github.com/{repo}/commit/{sha}":
            raise IntakeHold("REVISION_URL_DRIFT")
        if type(source["license"]) is not str or source["license"] not in LICENSES:
            raise IntakeHold("LICENSE_METADATA_INVALID")
        if source["license_evidence"] != "GITHUB_REPO_METADATA_ONLY":
            raise IntakeHold("FALSE_LICENSE_AUTHORITY")
        if source["asset_rights"] != "UNASSESSED" or source["code_imported"] is not False:
            raise IntakeHold("UNAUTHORIZED_ASSET_IMPORT_OR_RIGHTS")
        if not _safe_reference(source["reference"]):
            raise IntakeHold("INVALID_PRIMARY_REFERENCE")
        if type(source["method"]) is not str or not 7 <= len(source["method"]) <= 220:
            raise IntakeHold("UNSPECIFIED_METHOD")
        if type(source["target"]) is not str or not TARGET.fullmatch(source["target"]):
            raise IntakeHold("INVALID_SOURCE_OWNER")
        seen.add(sid)
        seen_repos.add(repo.lower())
        unknown_license_count += source["license"] == "NOASSERTION"

    experiments = value["experiments"]
    if type(experiments) is not list or not 1 <= len(experiments) <= 20:
        raise IntakeHold("EXPERIMENT_COUNT_INVALID")
    exp_ids = set()
    for exp in experiments:
        _strict_fields(exp, EXPERIMENT, "EXPERIMENT_SCHEMA_INVALID")
        if type(exp["id"]) is not str or not ID.fullmatch(exp["id"]) or exp["id"] in exp_ids:
            raise IntakeHold("EXPERIMENT_ID_INVALID_OR_DUPLICATE")
        exp_ids.add(exp["id"])
        _unique_names(exp["source_ids"], ID, 64, "EXPERIMENT_SOURCE_IDS_INVALID")
        if not set(exp["source_ids"]).issubset(seen):
            raise IntakeHold("UNKNOWN_EXPERIMENT_SOURCE")
        _unique_names(exp["target_repositories"], TARGET, 12, "EXPERIMENT_OWNERS_INVALID")
        if exp["stage"] != "UNMEASURED" or exp["source_code_copied"] is not False or exp["release_authorized"] is not False:
            raise IntakeHold("PREMATURE_EXPERIMENT_OR_RELEASE_CLAIM")
        for key in ("metric", "unit", "planned_denominator", "negative_control"):
            if type(exp[key]) is not str or not (3 if key == "unit" else 6) <= len(exp[key].strip()) <= 350:
                raise IntakeHold("METRIC_OR_DENOMINATOR_MISSING")
    return {
        "state": "SOURCE_RESEARCH_VALIDATED_NOT_ADMITTED",
        "sampled_public_sources": len(sources),
        "unmeasured_experiments": len(experiments),
        "unresolved_github_license_metadata": unknown_license_count,
        "code_imported": False,
        "training_or_deployment_authorized": False,
    }


def load(path):
    path = Path(path)
    if path.is_symlink() or not path.is_file():
        raise IntakeHold("INPUT_FILE_UNAVAILABLE_OR_SYMLINK")
    if not 1 <= path.stat().st_size <= MAX_BYTES:
        raise IntakeHold("INPUT_SIZE_INVALID")
    try:
        value = json.loads(
            path.read_bytes().decode("utf-8"),
            object_pairs_hook=_distinct_json,
            parse_constant=_nonfinite,
        )
    except (ValueError, UnicodeError) as exc:
        raise IntakeHold("INPUT_JSON_INVALID") from exc
    return validate(value)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest")
    args = parser.parse_args()
    try:
        result = load(args.manifest)
    except (IntakeHold, OSError) as exc:
        print(json.dumps({"state": "HOLD", "reason": str(exc) if isinstance(exc, IntakeHold) else "INPUT_IO_UNAVAILABLE"}))
        return 2
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
