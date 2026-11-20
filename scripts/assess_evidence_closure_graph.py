#!/usr/bin/env python3
"""Fail-closed *source-only* Evidence Closure Graph (ECG) intake.

This tool parses untrusted declarations, not their underlying evidence.
Its strongest positive verdict is REVIEW_CANDIDATE_ONLY, NEVER production ready.
No network calls, signatures, commands, credentials or provider effects.
"""
from __future__ import annotations
import argparse
import json
import re
import sys
from typing import Any

SCHEMA = "szl.evidence-closure-graph/v1"
COMMIT = re.compile(r"^[0-9a-f]{40}$")
DIGEST = re.compile(r"^[0-9a-f]{64}$")
IDENT = re.compile(r"^[A-Za-z][A-Za-z0-9_.-]{0,59}$")
MAX_BYTES = 65536
MAX_NODES = 128
MAX_EDGES = 256
TOP_KEYS = {"schema", "source_repo", "source_commit", "claims"}
NODE_KEYS = {"id", "source_commit", "depends_on", "test_digest", "review_digest",
             "receipt_digest", "declared_dissent_resolved"}
FORBIDDEN_AUTHORITY = ("runtime_verified", "proof_verified", "signer_verified",
                       "reviewer_independence_verified", "merge_authorized",
                       "release_authorized", "production_ready")

def no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result = {}
    for k, value in pairs:
        if k in result:
            raise ValueError("DUPLICATE_JSON_KEY")
        result[k] = value
    return result

def no_constant(value: str) -> None:
    raise ValueError("NONFINITE_JSON_NUMBER")

def deny(reason: str, *, nodes: int = 0) -> dict[str, Any]:
    return {
        "state": "HOLD",
        "reason": reason,
        "nodes_checked": nodes,
        "structurally_well_formed": False,
        "independent_evidence_verified": False,
        "runtime_verified": False,
        "merge_authorized": False,
        "publication_authorized": False,
        "production_ready": False,
    }

def assess(raw: bytes) -> dict[str, Any]:
    if not isinstance(raw, bytes) or len(raw) > MAX_BYTES:
        return deny("PAYLOAD_UNAVAILABLE_OR_OVERSIZED")
    try:
        payload = json.loads(
            raw.decode("utf-8", errors="strict"),
            object_pairs_hook=no_duplicates,
            parse_constant=no_constant,
        )
    except (ValueError, UnicodeDecodeError, TypeError, RecursionError):
        return deny("MALFORMED_JSON")
    if not isinstance(payload, dict) or set(payload) != TOP_KEYS:
        return deny("TOP_LEVEL_SCHEMA_MISMATCH")
    if payload["schema"] != SCHEMA or payload["source_repo"] != "szl-holdings/szl-papers":
        return deny("UNAUTHORIZED_SCHEMA_OR_SOURCE")
    root = payload["source_commit"]
    if not isinstance(root, str) or not COMMIT.fullmatch(root):
        return deny("INVALID_SOURCE_COMMIT")
    claims = payload["claims"]
    if not isinstance(claims, list) or not claims or len(claims) > MAX_NODES:
        return deny("INVALID_NODE_COUNT")
    nodes = {}
    edge_count = 0
    for item in claims:
        if not isinstance(item, dict) or set(item) != NODE_KEYS:
            return deny("CLAIM_SCHEMA_MISMATCH", nodes=len(nodes))
        cid = item["id"]
        if not isinstance(cid, str) or not IDENT.fullmatch(cid) or cid in nodes:
            return deny("INVALID_OR_DUPLICATE_CLAIM_ID", nodes=len(nodes))
        sha = item["source_commit"]
        if not isinstance(sha, str) or sha != root:
            return deny("SOURCE_COMMIT_MISMATCH", nodes=len(nodes))
        deps = item["depends_on"]
        if (not isinstance(deps, list) or len(deps) > MAX_NODES
            or any(not isinstance(x, str) or not IDENT.fullmatch(x) for x in deps)
            or len(deps) != len(set(deps))):
            return deny("INVALID_PARENT_LIST", nodes=len(nodes))
        edge_count += len(deps)
        if edge_count > MAX_EDGES:
            return deny("EDGE_BUDGET_EXCEEDED", nodes=len(nodes))
        for name in ("test_digest", "review_digest", "receipt_digest"):
            value = item[name]
            if not isinstance(value, str) or not DIGEST.fullmatch(value):
                return deny("INVALID_DECLARED_DIGEST", nodes=len(nodes))
        if type(item["declared_dissent_resolved"]) is not bool:
            return deny("INVALID_DISSENT_DECLARATION", nodes=len(nodes))
        nodes[cid] = item
    for cid, item in nodes.items():
        if any(parent not in nodes for parent in item["depends_on"]):
            return deny("UNKNOWN_DEPENDENCY", nodes=len(nodes))
        if cid in item["depends_on"]:
            return deny("SELF_DEPENDENCY", nodes=len(nodes))
    states: dict[str, int] = {}
    def visit(cid: str) -> bool:
        if states.get(cid) == 1:
            return False
        if states.get(cid) == 2:
            return True
        states[cid] = 1
        for parent in nodes[cid]["depends_on"]:
            if not visit(parent):
                return False
        states[cid] = 2
        return True
    if not all(visit(cid) for cid in nodes):
        return deny("CYCLIC_CLAIM_GRAPH", nodes=len(nodes))
    unresolved = [cid for cid,item in nodes.items()
                  if not item["declared_dissent_resolved"]]
    if unresolved:
        return deny("DECLARED_DISSENT_UNRESOLVED", nodes=len(nodes))
    # Digest declarations can be fabricated coherently; these are NOT verified.
    return {
        "state": "REVIEW_CANDIDATE_ONLY",
        "reason": "STRUCTURAL_CHECKS_ONLY_ALL_EVIDENCE_UNTRUSTED",
        "nodes_checked": len(nodes),
        "edges_checked": edge_count,
        "structurally_well_formed": True,
        "independent_evidence_verified": False,
        "runtime_verified": False,
        "merge_authorized": False,
        "publication_authorized": False,
        "production_ready": False,
    }

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("request", help="public, untrusted JSON request file")
    args = parser.parse_args()
    from pathlib import Path
    try:
        raw = Path(args.request).read_bytes()
    except OSError:
        print(json.dumps(deny("INPUT_FILE_UNAVAILABLE"), sort_keys=True))
        return 2
    verdict = assess(raw)
    print(json.dumps(verdict, sort_keys=True))
    return 0 if verdict["state"] == "REVIEW_CANDIDATE_ONLY" else 2

if __name__ == "__main__":
    sys.exit(main())