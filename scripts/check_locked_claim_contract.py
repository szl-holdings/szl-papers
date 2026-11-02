#!/usr/bin/env python3
"""Validate the v26 locked-claim contract against exact kernel evidence.

This offline, standard-library check joins four records without promoting any
of them:

* the byte-pinned v26 repository-source manuscript;
* the non-normative manuscript review ledger;
* the exact ``lutar-lean`` locked-formula evidence artifact member; and
* the GitHub Actions artifact receipt that identifies those member bytes.

The check fails closed if a formula ID, declaration, axiom set, review verdict,
source revision, artifact digest, publication version, or authority boundary
drifts.  A pass means only that the records agree at their named revisions.  It
does not establish manuscript semantics, runtime refinement, empirical
validity, publication, deployment, or authorization.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


CONTRACT_REL = Path("metadata/locked-claim-contract.json")
EXPECTED_CONTRACT_SCHEMA = "szl.papers.locked-claim-contract/v1"
EXPECTED_EVIDENCE_SCHEMA = "szl.lutar.locked-formula-evidence/v1"
EXPECTED_RECEIPT_SCHEMA = "szl.papers.external-evidence-receipt/v1"
EXPECTED_LEDGER_SCHEMA = "szl.papers.review-ledger/v1"
EXPECTED_IDS = ["F1", "F4", "F7", "F11", "F12", "F18", "F19", "F22"]
EXPECTED_TRUST_BASE = ["propext", "Classical.choice", "Quot.sound"]
EXPECTED_LIMITATION_TERMS = (
    "runtime refinement",
    "empirical validity",
    "deployment",
    "publication",
    "authorization",
)
SHA40 = re.compile(r"^[0-9a-f]{40}$")
SHA256 = re.compile(r"^sha256:[0-9a-f]{64}$")


class ContractError(ValueError):
    """The contract cannot be loaded safely."""


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise ContractError(f"duplicate JSON key {key!r}")
        value[key] = item
    return value


def _load_json_bytes(payload: bytes, label: str) -> dict[str, Any]:
    try:
        value = json.loads(
            payload.decode("utf-8"), object_pairs_hook=_unique_object
        )
    except (UnicodeDecodeError, json.JSONDecodeError, ContractError) as exc:
        raise ContractError(f"cannot parse {label}: {exc}") from exc
    if not isinstance(value, dict):
        raise ContractError(f"{label} root must be an object")
    return value


def _safe_path(root: Path, relative: object, label: str) -> Path:
    if not isinstance(relative, str) or not relative:
        raise ContractError(f"{label} must be a non-empty relative path")
    candidate = Path(relative)
    if candidate.is_absolute() or ".." in candidate.parts:
        raise ContractError(f"{label} must stay within the repository")
    resolved_root = root.resolve()
    resolved = (resolved_root / candidate).resolve()
    if resolved != resolved_root and resolved_root not in resolved.parents:
        raise ContractError(f"{label} escapes the repository")
    return resolved


def _read(path: Path, label: str) -> bytes:
    try:
        return path.read_bytes()
    except OSError as exc:
        raise ContractError(f"cannot read {label} at {path}: {exc}") from exc


def _sha256(payload: bytes) -> str:
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def _lf_bytes(payload: bytes) -> bytes:
    """Use Git's text-normalized line endings for cross-platform source pins."""
    return payload.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def _git_blob_sha1(payload: bytes) -> str:
    header = f"blob {len(payload)}\0".encode("ascii")
    return hashlib.sha1(header + payload).hexdigest()  # noqa: S324 - Git object ID


def _canonical_digest(value: dict[str, Any], omit: str) -> str:
    body = {key: item for key, item in value.items() if key != omit}
    encoded = json.dumps(
        body, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    return _sha256(encoded)


def _objects_by(rows: object, key: str, code: str, errors: list[str]) -> dict[str, dict[str, Any]]:
    if not isinstance(rows, list):
        errors.append(f"[{code}] expected a list")
        return {}
    result: dict[str, dict[str, Any]] = {}
    for index, row in enumerate(rows):
        if not isinstance(row, dict) or not isinstance(row.get(key), str):
            errors.append(f"[{code}] row {index} must be an object with string {key}")
            continue
        identity = row[key]
        if identity in result:
            errors.append(f"[{code}] duplicate {key} {identity}")
        result[identity] = row
    return result


def _false_authority(value: object, label: str, errors: list[str]) -> None:
    required = ("paper_claim_promotion", "publication", "deployment", "runtime")
    if not isinstance(value, dict):
        errors.append(f"[authority] {label} must be an object")
        return
    for key in required:
        if value.get(key) is not False:
            errors.append(f"[authority] {label}.{key} must be false")


def validate_records(
    contract: dict[str, Any],
    evidence: dict[str, Any],
    receipt: dict[str, Any],
    ledger: dict[str, Any],
    *,
    evidence_bytes: bytes,
    publication_bytes: bytes,
) -> list[str]:
    errors: list[str] = []

    if contract.get("schema") != EXPECTED_CONTRACT_SCHEMA:
        errors.append(f"[contract] schema must be {EXPECTED_CONTRACT_SCHEMA}")
    if contract.get("normative") is not False:
        errors.append("[contract] normative must be false")

    publication = contract.get("publication")
    if not isinstance(publication, dict):
        errors.append("[publication] publication must be an object")
        publication = {}
    if publication.get("version") != "v26":
        errors.append("[publication] version must be v26")
    if publication.get("lifecycle") != "REPOSITORY_SOURCE_NOT_SEPARATELY_DOI_PUBLISHED":
        errors.append("[publication] lifecycle must preserve the repository-source boundary")
    if publication.get("published_version") != "v21":
        errors.append("[publication] published_version must remain v21")
    if publication.get("concept_doi") != "10.5281/zenodo.19944926":
        errors.append("[publication] concept DOI drift")
    if publication.get("published_version_doi") != "10.5281/zenodo.20490218":
        errors.append("[publication] published v21 DOI drift")
    if not SHA40.fullmatch(str(publication.get("source_commit", ""))):
        errors.append("[publication] source_commit must be lowercase 40-hex")
    publication_lf = _lf_bytes(publication_bytes)
    if publication.get("git_blob_sha1") != _git_blob_sha1(publication_lf):
        errors.append("[publication] manuscript Git blob does not match the contract")
    if publication.get("sha256") != _sha256(publication_lf):
        errors.append("[publication] manuscript SHA-256 does not match the contract")

    if evidence.get("schema") != EXPECTED_EVIDENCE_SCHEMA:
        errors.append(f"[evidence-source] schema must be {EXPECTED_EVIDENCE_SCHEMA}")
    kernel = contract.get("kernel_evidence")
    if not isinstance(kernel, dict):
        errors.append("[evidence-source] kernel_evidence must be an object")
        kernel = {}
    for key in ("schema", "repository", "source_commit", "source_tree", "evidence_digest"):
        if kernel.get(key) != evidence.get(key):
            errors.append(f"[evidence-source] contract/evidence {key} mismatch")
    if evidence.get("repository") != "szl-holdings/lutar-lean":
        errors.append("[evidence-source] unexpected evidence repository")
    for key in ("source_commit", "source_tree"):
        if not SHA40.fullmatch(str(evidence.get(key, ""))):
            errors.append(f"[evidence-source] {key} must be lowercase 40-hex")
    if evidence.get("input_files_match_head") is not True:
        errors.append("[evidence-source] input_files_match_head must be true")
    if kernel.get("file_sha256") != _sha256(evidence_bytes):
        errors.append("[evidence-source] vendored evidence SHA-256 mismatch")
    if not SHA256.fullmatch(str(evidence.get("evidence_digest", ""))):
        errors.append("[evidence-digest] evidence_digest must be lowercase SHA-256")
    elif evidence.get("evidence_digest") != _canonical_digest(evidence, "evidence_digest"):
        errors.append("[evidence-digest] canonical evidence digest mismatch")
    if evidence.get("lean_toolchain") != "leanprover/lean4:v4.34.1":
        errors.append("[evidence-source] unexpected Lean toolchain")
    if evidence.get("kernel_query_tool") != "Lean.collectAxioms":
        errors.append("[evidence-source] unexpected kernel query tool")
    if evidence.get("trust_base") != EXPECTED_TRUST_BASE:
        errors.append("[axiom] evidence trust base drift")
    if evidence.get("carrier_theorem_count") != 24:
        errors.append("[carrier] carrier_theorem_count must be 24")
    if evidence.get("locked_ids") != EXPECTED_IDS:
        errors.append(f"[claims] evidence locked_ids must be {EXPECTED_IDS}")
    expected_inputs = {
        ".github/scripts/build_locked_formula_evidence.py",
        "Lutar/Puriq/Formulas/ProvedFormulas.lean",
        "claims/locked-formulas.v1.json",
        "lean-toolchain",
        "tools/lean/LockedGuard.lean",
    }
    inputs = evidence.get("inputs")
    if not isinstance(inputs, dict) or set(inputs) != expected_inputs:
        errors.append("[evidence-source] exact evidence input set drift")
    elif not all(SHA256.fullmatch(str(value)) for value in inputs.values()):
        errors.append("[evidence-source] every evidence input must have a lowercase SHA-256")

    evidence_claims = _objects_by(evidence.get("claims"), "claim_id", "claims", errors)
    if list(evidence_claims) != EXPECTED_IDS:
        errors.append(f"[claims] evidence claim order must be {EXPECTED_IDS}")
    carrier_by_name: dict[str, tuple[str, dict[str, Any]]] = {}
    for claim_id, row in evidence_claims.items():
        carriers = row.get("carriers")
        if not isinstance(carriers, list) or not carriers:
            errors.append(f"[carrier] {claim_id} must have carriers")
            continue
        for carrier in carriers:
            if not isinstance(carrier, dict) or not isinstance(carrier.get("theorem"), str):
                errors.append(f"[carrier] {claim_id} has a malformed carrier")
                continue
            theorem = carrier["theorem"]
            if theorem in carrier_by_name:
                errors.append(f"[carrier] duplicate theorem {theorem}")
            carrier_by_name[theorem] = (claim_id, carrier)
            axioms = carrier.get("axioms")
            if carrier.get("allowed") is not True:
                errors.append(f"[carrier] {theorem} must be allowed")
            if not isinstance(axioms, list) or not all(isinstance(item, str) for item in axioms):
                errors.append(f"[axiom] {theorem} axioms must be a string list")
            elif len(axioms) != len(set(axioms)) or not set(axioms).issubset(EXPECTED_TRUST_BASE):
                errors.append(f"[axiom] {theorem} axioms are duplicated or outside the trust base")
    if len(carrier_by_name) != 24:
        errors.append(f"[carrier] expected 24 unique carriers, found {len(carrier_by_name)}")

    if ledger.get("schema") != EXPECTED_LEDGER_SCHEMA:
        errors.append(f"[ledger] schema must be {EXPECTED_LEDGER_SCHEMA}")
    review = contract.get("review_ledger")
    if not isinstance(review, dict):
        errors.append("[ledger] review_ledger must be an object")
        review = {}
    for key in ("schema", "ledger_id", "review_status", "normative"):
        if review.get(key) != ledger.get(key):
            errors.append(f"[ledger] contract/ledger {key} mismatch")
    if ledger.get("normative") is not False or ledger.get("review_status") != "DRAFT_FOR_OWNER_REVIEW":
        errors.append("[ledger] review must remain non-normative and draft for owner review")
    if ledger.get("locked_ids") != EXPECTED_IDS:
        errors.append(f"[claims] ledger locked_ids must be {EXPECTED_IDS}")
    ledger_rows = _objects_by(ledger.get("entries"), "id", "ledger", errors)
    contract_claims = _objects_by(contract.get("claims"), "claim_id", "claims", errors)
    if list(contract_claims) != EXPECTED_IDS:
        errors.append(f"[claims] contract claim order must be {EXPECTED_IDS}")

    ledger_theorems: set[str] = set()
    for claim_id in EXPECTED_IDS:
        contract_row = contract_claims.get(claim_id, {})
        ledger_row = ledger_rows.get(claim_id, {})
        evidence_row = evidence_claims.get(claim_id, {})
        if contract_row.get("kernel_evidence_state") != "OBSERVED_AT_PIN":
            errors.append(f"[claim] {claim_id} kernel_evidence_state must be OBSERVED_AT_PIN")
        if contract_row.get("review_row") != ledger_row.get("row"):
            errors.append(f"[claim] {claim_id} review row mismatch")
        if contract_row.get("paper_claim_review_verdict") != ledger_row.get("verdict"):
            errors.append(f"[claim] {claim_id} review verdict mismatch")
        if contract_row.get("severity") != ledger_row.get("severity"):
            errors.append(f"[claim] {claim_id} severity mismatch")
        declarations = ledger_row.get("lean_decls")
        if not isinstance(declarations, list):
            errors.append(f"[claim] {claim_id} ledger declarations missing")
            continue
        primary = [item for item in declarations if isinstance(item, dict) and item.get("primary") is True]
        if len(primary) != 1:
            errors.append(f"[claim] {claim_id} must have exactly one primary declaration")
            continue
        declaration = primary[0]
        if contract_row.get("primary_declaration") != declaration.get("decl"):
            errors.append(f"[claim] {claim_id} primary declaration mismatch")
        if contract_row.get("kernel_axioms") != declaration.get("kernel_axioms"):
            errors.append(f"[claim] {claim_id} primary axiom mismatch")
        evidence_names = {
            carrier.get("theorem")
            for carrier in evidence_row.get("carriers", [])
            if isinstance(carrier, dict)
        }
        for declaration in declarations:
            if not isinstance(declaration, dict) or declaration.get("kind") != "theorem":
                continue
            name = declaration.get("decl")
            ledger_theorems.add(str(name))
            if name not in evidence_names:
                errors.append(f"[claim] {claim_id} ledger theorem {name} is absent from exact evidence")
                continue
            evidence_carrier = carrier_by_name.get(str(name), (None, {}))[1]
            if evidence_carrier.get("axioms") != declaration.get("kernel_axioms"):
                errors.append(f"[axiom] {name} ledger/evidence axiom mismatch")
    if ledger_theorems != set(carrier_by_name):
        errors.append("[carrier] ledger theorem set does not equal the exact evidence theorem set")

    if receipt.get("schema") != EXPECTED_RECEIPT_SCHEMA:
        errors.append(f"[receipt] schema must be {EXPECTED_RECEIPT_SCHEMA}")
    for key in ("source_repository", "source_commit", "source_tree"):
        evidence_key = "repository" if key == "source_repository" else key
        if receipt.get(key) != evidence.get(evidence_key):
            errors.append(f"[receipt] {key} does not match the evidence")
    workflow = receipt.get("workflow")
    artifact = receipt.get("artifact")
    if not isinstance(workflow, dict) or workflow.get("conclusion") != "success":
        errors.append("[receipt] workflow must be a successful recorded run")
        workflow = {}
    if workflow.get("run_id") != kernel.get("workflow_run_id"):
        errors.append("[receipt] workflow run ID mismatch")
    expected_run_url = f"https://github.com/szl-holdings/lutar-lean/actions/runs/{kernel.get('workflow_run_id')}"
    if workflow.get("name") != "Lake build (gate + numbers)" or workflow.get("event") != "push":
        errors.append("[receipt] workflow identity drift")
    if workflow.get("url") != expected_run_url:
        errors.append("[receipt] workflow URL mismatch")
    if not isinstance(artifact, dict):
        errors.append("[receipt] artifact must be an object")
        artifact = {}
    if artifact.get("id") != kernel.get("artifact_id"):
        errors.append("[receipt] artifact ID mismatch")
    if artifact.get("name") != kernel.get("artifact_name"):
        errors.append("[receipt] artifact name mismatch")
    if artifact.get("archive_digest") != kernel.get("artifact_archive_digest"):
        errors.append("[receipt] artifact archive digest mismatch")
    if artifact.get("vendored_path") != kernel.get("path"):
        errors.append("[receipt] vendored path mismatch")
    if artifact.get("member_path") != "locked-formulas.evidence.json":
        errors.append("[receipt] artifact member path drift")
    if artifact.get("member_sha256") != _sha256(evidence_bytes):
        errors.append("[receipt] artifact member SHA-256 mismatch")
    for digest_key in ("archive_digest", "member_sha256"):
        if not SHA256.fullmatch(str(artifact.get(digest_key, ""))):
            errors.append(f"[receipt] {digest_key} must be lowercase SHA-256")
    _false_authority(contract.get("authority"), "contract.authority", errors)
    _false_authority(receipt.get("authority"), "receipt.authority", errors)

    limitations = contract.get("limitations")
    if not isinstance(limitations, list) or not all(isinstance(item, str) for item in limitations):
        errors.append("[limitations] contract limitations must be a string list")
    else:
        joined = " ".join(limitations).lower()
        for term in EXPECTED_LIMITATION_TERMS:
            if term not in joined:
                errors.append(f"[limitations] contract must preserve {term!r}")
    return errors


def load_records(repo_root: Path) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any], bytes, bytes]:
    contract_bytes = _read(repo_root / CONTRACT_REL, "contract")
    contract = _load_json_bytes(contract_bytes, str(CONTRACT_REL))
    kernel = contract.get("kernel_evidence")
    publication = contract.get("publication")
    review = contract.get("review_ledger")
    if not isinstance(kernel, dict) or not isinstance(publication, dict) or not isinstance(review, dict):
        raise ContractError("contract must contain kernel_evidence, publication, and review_ledger objects")
    evidence_path = _safe_path(repo_root, kernel.get("path"), "kernel_evidence.path")
    receipt_path = _safe_path(repo_root, kernel.get("receipt_path"), "kernel_evidence.receipt_path")
    ledger_path = _safe_path(repo_root, review.get("path"), "review_ledger.path")
    publication_path = _safe_path(repo_root, publication.get("path"), "publication.path")
    evidence_bytes = _read(evidence_path, "kernel evidence")
    publication_bytes = _read(publication_path, "publication source")
    return (
        contract,
        _load_json_bytes(evidence_bytes, str(evidence_path)),
        _load_json_bytes(_read(receipt_path, "artifact receipt"), str(receipt_path)),
        _load_json_bytes(_read(ledger_path, "review ledger"), str(ledger_path)),
        evidence_bytes,
        publication_bytes,
    )


def evaluate(repo_root: Path) -> dict[str, Any]:
    try:
        contract, evidence, receipt, ledger, evidence_bytes, publication_bytes = load_records(repo_root)
        errors = validate_records(
            contract,
            evidence,
            receipt,
            ledger,
            evidence_bytes=evidence_bytes,
            publication_bytes=publication_bytes,
        )
    except ContractError as exc:
        errors = [f"[load] {exc}"]
        contract = evidence = ledger = {}
    return {
        "schema": "szl.papers.locked-claim-contract-check/v1",
        "ok": not errors,
        "errors": errors,
        "publication_version": contract.get("publication", {}).get("version") if isinstance(contract.get("publication"), dict) else None,
        "kernel_source_commit": evidence.get("source_commit"),
        "evidence_digest": evidence.get("evidence_digest"),
        "locked_claim_count": len(contract.get("claims", [])) if isinstance(contract.get("claims"), list) else 0,
        "carrier_theorem_count": evidence.get("carrier_theorem_count"),
        "review_status": ledger.get("review_status"),
        "authority": contract.get("authority"),
    }


def _self_test(repo_root: Path) -> int:
    contract, evidence, receipt, ledger, evidence_bytes, publication_bytes = load_records(repo_root)
    baseline = validate_records(
        contract, evidence, receipt, ledger,
        evidence_bytes=evidence_bytes, publication_bytes=publication_bytes,
    )
    if baseline:
        raise AssertionError(f"real contract must pass before fixtures run: {baseline}")

    cases: list[tuple[str, str, Any]] = []

    def case(name: str, code: str, mutate) -> None:
        values = [copy.deepcopy(contract), copy.deepcopy(evidence), copy.deepcopy(receipt), copy.deepcopy(ledger)]
        ebytes, pbytes = evidence_bytes, publication_bytes
        changed = mutate(values, ebytes, pbytes)
        if isinstance(changed, tuple) and len(changed) == 2:
            ebytes, pbytes = changed
        errors = validate_records(
            *values, evidence_bytes=ebytes, publication_bytes=pbytes
        )
        if not any(error.startswith(f"[{code}]") for error in errors):
            raise AssertionError(f"{name}: expected [{code}], got {errors}")
        cases.append((name, code, errors))

    case("wrong source commit", "evidence-source", lambda v, e, p: v[1].update(source_commit="0" * 40))
    case("tampered evidence digest", "evidence-digest", lambda v, e, p: v[1].update(evidence_digest="sha256:" + "0" * 64))
    case("disallowed carrier", "carrier", lambda v, e, p: v[1]["claims"][0]["carriers"][0].update(allowed=False))
    case("axiom outside trust base", "axiom", lambda v, e, p: v[1]["claims"][0]["carriers"][0].update(axioms=["sorryAx"]))
    case("fake primary declaration", "claim", lambda v, e, p: v[0]["claims"][0].update(primary_declaration="Puriq.Formula.Proved.fake"))
    case("missing claim", "claims", lambda v, e, p: v[0]["claims"].pop())
    case("verdict drift", "claim", lambda v, e, p: v[0]["claims"][0].update(paper_claim_review_verdict="MATCHES"))
    case("artifact member digest drift", "receipt", lambda v, e, p: v[2]["artifact"].update(member_sha256="sha256:" + "0" * 64))
    case("authority escalation", "authority", lambda v, e, p: v[0]["authority"].update(publication=True))
    case("manuscript byte drift", "publication", lambda v, e, p: (e, p + b"\nchanged\n"))

    print(f"self-test OK: 1 positive + {len(cases)} negative cases")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-path", type=Path, default=Path("."))
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)
    repo_root = args.repo_path.resolve()
    try:
        if args.self_test:
            return _self_test(repo_root)
        result = evaluate(repo_root)
    except (ContractError, AssertionError) as exc:
        print(f"locked-claim contract: FAIL: {exc}", file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    elif result["ok"]:
        print(
            "locked-claim contract: OK: "
            f"{result['locked_claim_count']} claims / "
            f"{result['carrier_theorem_count']} carriers / "
            f"{result['kernel_source_commit']}"
        )
        print("authority: publication=false deployment=false runtime=false paper_claim_promotion=false")
    else:
        for error in result["errors"]:
            print(f"ERROR {error}", file=sys.stderr)
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
