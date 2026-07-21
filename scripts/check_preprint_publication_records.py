#!/usr/bin/env python3
"""Validate the aggregate index for the two archived July 2026 preprints.

The check is deliberately offline and stdlib-only. It verifies the identities
already read back from Zenodo and GitHub, and prevents repository-level
``CITATION.cff`` or ``.zenodo.json`` metadata from being rewritten as though
the aggregate ``szl-papers`` repository were either standalone preprint.
"""

from __future__ import annotations

import argparse
import json
import os
import re
from copy import deepcopy


SCHEMA = "szl.preprint-publication-records/v1"
AGGREGATE_REPOSITORY = "https://github.com/szl-holdings/szl-papers"
DOI_RE = re.compile(r"^10\.5281/zenodo\.(\d+)$")

EXPECTED = {
    "10.5281/zenodo.21332317": {
        "paper_id": "evidence-typed-formula-governance",
        "concept_doi": "10.5281/zenodo.21332316",
        "title": "From Build Success to Admissible Proof: Evidence-Typed Governance for a Mixed Lean and Executable Formula Corpus",
        "repository_url": "https://github.com/szl-holdings/evidence-typed-formula-governance",
        "github_release_published_at": "2026-07-13T06:18:18Z",
    },
    "10.5281/zenodo.21332338": {
        "paper_id": "fail-closed-governed-ai-services",
        "concept_doi": "10.5281/zenodo.21332337",
        "title": "Readiness Is Not Evidence: Fail-Closed Epistemic Boundaries for Governed AI Services",
        "repository_url": "https://github.com/szl-holdings/fail-closed-governed-ai-services",
        "github_release_published_at": "2026-07-13T06:19:02Z",
    },
}

REQUIRED_FIELDS = {
    "paper_id",
    "title",
    "version",
    "publication_date",
    "publication_type",
    "peer_reviewed",
    "lifecycle",
    "version_doi",
    "version_doi_url",
    "concept_doi",
    "concept_doi_url",
    "zenodo_record_url",
    "zenodo_status",
    "license",
    "pages",
    "repository_url",
    "repository_archived",
    "github_release_tag",
    "github_release_url",
    "github_release_published_at",
    "immutable_archive",
    "embedded_pdf_metadata_caveat",
}


def _load_json(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def validate(data: dict, citation_text: str, zenodo_data: dict) -> list[str]:
    errors: list[str] = []

    if data.get("schema") != SCHEMA:
        errors.append(f"schema must be {SCHEMA!r}")
    if data.get("repository_scope") != "aggregate_index":
        errors.append("repository_scope must be 'aggregate_index'")
    if data.get("repository_url") != AGGREGATE_REPOSITORY:
        errors.append("repository_url must identify the aggregate szl-papers repository")

    records = data.get("records")
    if not isinstance(records, list):
        return errors + ["records must be an array"]

    seen_ids: set[str] = set()
    seen_version_dois: set[str] = set()
    seen_concept_dois: set[str] = set()

    for index, record in enumerate(records):
        label = f"records[{index}]"
        if not isinstance(record, dict):
            errors.append(f"{label} must be an object")
            continue

        missing = sorted(REQUIRED_FIELDS - set(record))
        if missing:
            errors.append(f"{label} missing fields: {', '.join(missing)}")
            continue

        paper_id = record["paper_id"]
        version_doi = record["version_doi"]
        concept_doi = record["concept_doi"]

        if not isinstance(paper_id, str) or not paper_id:
            errors.append(f"{label}.paper_id must be a non-empty string")
        elif paper_id in seen_ids:
            errors.append(f"duplicate paper_id: {paper_id}")
        seen_ids.add(paper_id)

        version_match = DOI_RE.fullmatch(str(version_doi))
        concept_match = DOI_RE.fullmatch(str(concept_doi))
        if not version_match:
            errors.append(f"{label}.version_doi is not a Zenodo DOI")
        if not concept_match:
            errors.append(f"{label}.concept_doi is not a Zenodo DOI")
        if version_doi in seen_version_dois:
            errors.append(f"duplicate version DOI: {version_doi}")
        if concept_doi in seen_concept_dois:
            errors.append(f"duplicate concept DOI: {concept_doi}")
        seen_version_dois.add(version_doi)
        seen_concept_dois.add(concept_doi)

        expected = EXPECTED.get(version_doi)
        if expected is None:
            errors.append(f"unrecognized July 2026 preprint DOI: {version_doi}")
        else:
            for field, expected_value in expected.items():
                if record.get(field) != expected_value:
                    errors.append(
                        f"{label}.{field} must be {expected_value!r} for {version_doi}"
                    )

        if version_match:
            recid = version_match.group(1)
            exact_values = {
                "version_doi_url": f"https://doi.org/{version_doi}",
                "zenodo_record_url": f"https://zenodo.org/records/{recid}",
            }
            for field, expected_value in exact_values.items():
                if record.get(field) != expected_value:
                    errors.append(f"{label}.{field} must be {expected_value!r}")
        if concept_match and record.get("concept_doi_url") != f"https://doi.org/{concept_doi}":
            errors.append(f"{label}.concept_doi_url does not match concept_doi")

        repository_url = record.get("repository_url")
        release_tag = record.get("github_release_tag")
        if record.get("github_release_url") != f"{repository_url}/releases/tag/{release_tag}":
            errors.append(f"{label}.github_release_url does not match repository and tag")

        exact_contract = {
            "version": "0.1.0",
            "publication_date": "2026-07-13",
            "publication_type": "preprint",
            "peer_reviewed": False,
            "lifecycle": "PUBLISHED_PREPRINT_NOT_PEER_REVIEWED",
            "zenodo_status": "published",
            "license": "CC-BY-4.0",
            "pages": 24,
            "repository_archived": True,
            "github_release_tag": "v0.1.0",
            "immutable_archive": True,
        }
        for field, expected_value in exact_contract.items():
            if record.get(field) != expected_value:
                errors.append(f"{label}.{field} must be {expected_value!r}")

        caveat = record.get("embedded_pdf_metadata_caveat")
        if not isinstance(caveat, str) or "new immutable Zenodo version" not in caveat:
            errors.append(f"{label} must preserve the embedded-PDF metadata caveat")

    if seen_version_dois != set(EXPECTED):
        missing = sorted(set(EXPECTED) - seen_version_dois)
        extra = sorted(seen_version_dois - set(EXPECTED))
        if missing:
            errors.append(f"missing required version DOIs: {', '.join(missing)}")
        if extra:
            errors.append(f"unexpected version DOIs: {', '.join(extra)}")

    citation_lower = citation_text.lower()
    if "type: software" not in citation_lower:
        errors.append("root CITATION.cff must retain aggregate software identity")
    if f'repository-code: "{AGGREGATE_REPOSITORY}"' not in citation_text:
        errors.append("root CITATION.cff must retain the aggregate repository URL")
    for record in records:
        if isinstance(record, dict) and record.get("title") in citation_text:
            errors.append("root CITATION.cff must not take a standalone preprint title")
        if isinstance(record, dict) and record.get("version_doi") in citation_text:
            errors.append("root CITATION.cff must not take a standalone preprint DOI")

    if not isinstance(zenodo_data.get("title"), str):
        errors.append("root .zenodo.json must retain a valid title")
    if "REFERENCE ONLY" not in str(zenodo_data.get("notes", "")):
        errors.append("root .zenodo.json must remain explicitly reference-only")
    related = zenodo_data.get("related_identifiers")
    if not isinstance(related, list) or not any(
        isinstance(item, dict)
        and item.get("identifier") == AGGREGATE_REPOSITORY
        and item.get("relation") == "isSupplementTo"
        for item in related
    ):
        errors.append("root .zenodo.json must retain the aggregate repository relation")
    for record in records:
        if not isinstance(record, dict):
            continue
        if zenodo_data.get("title") == record.get("title"):
            errors.append("root .zenodo.json must not take a standalone preprint title")
        if zenodo_data.get("doi") == record.get("version_doi"):
            errors.append("root .zenodo.json must not take a standalone preprint DOI")

    return errors


def check_repository(repo_root: str) -> dict:
    records_path = os.path.join(repo_root, "PREPRINT_PUBLICATION_RECORDS.json")
    citation_path = os.path.join(repo_root, "CITATION.cff")
    zenodo_path = os.path.join(repo_root, ".zenodo.json")
    try:
        data = _load_json(records_path)
        with open(citation_path, "r", encoding="utf-8") as handle:
            citation_text = handle.read()
        zenodo_data = _load_json(zenodo_path)
        errors = validate(data, citation_text, zenodo_data)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        errors = [str(exc)]
        data = {}
    return {
        "path": records_path,
        "records": len(data.get("records", [])) if isinstance(data.get("records"), list) else 0,
        "errors": errors,
        "ok": not errors,
    }


def self_test(repo_root: str) -> None:
    records_path = os.path.join(repo_root, "PREPRINT_PUBLICATION_RECORDS.json")
    data = _load_json(records_path)
    with open(os.path.join(repo_root, "CITATION.cff"), "r", encoding="utf-8") as handle:
        citation_text = handle.read()
    zenodo_data = _load_json(os.path.join(repo_root, ".zenodo.json"))

    assert validate(data, citation_text, zenodo_data) == []

    wrong_scope = deepcopy(data)
    wrong_scope["repository_scope"] = "standalone_paper"
    assert any("repository_scope" in error for error in validate(wrong_scope, citation_text, zenodo_data))

    collapsed_citation = citation_text + f'\ndoi: "{data["records"][0]["version_doi"]}"\n'
    assert any("standalone preprint DOI" in error for error in validate(data, collapsed_citation, zenodo_data))

    swapped_ids = deepcopy(data)
    swapped_ids["records"][0]["paper_id"], swapped_ids["records"][1]["paper_id"] = (
        swapped_ids["records"][1]["paper_id"],
        swapped_ids["records"][0]["paper_id"],
    )
    assert any(".paper_id must be" in error for error in validate(swapped_ids, citation_text, zenodo_data))

    wrong_release = deepcopy(data)
    wrong_release["records"][0]["github_release_url"] = "https://example.invalid/release"
    assert any("github_release_url" in error for error in validate(wrong_release, citation_text, zenodo_data))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-path", default=".")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        self_test(args.repo_path)
        print("preprint publication records self-test OK")
        return 0

    result = check_repository(args.repo_path)
    print(
        "preprint publication records: "
        f"{result['records']} records · "
        f"{len(result['errors'])} errors"
    )
    for error in result["errors"]:
        print(f"  ERROR: {error}")
    print("VERDICT:", "OK" if result["ok"] else "FAIL")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
