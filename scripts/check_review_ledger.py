#!/usr/bin/env python3
"""Read-only consistency checker for the non-normative review ledgers in ``reviews/``.

The v26 locked-eight claim ledger (``reviews/v26-locked-eight-claim-ledger.json``
plus its Markdown rendering) compares what the v26 manuscript says about the
locked eight with the Lean declarations that carry them at a pinned lutar-lean
commit. This script checks that the ledger stays well-formed and anchored:

  * exactly the locked ids {F1, F4, F7, F11, F12, F18, F19, F22}, one row each;
  * every ``manuscript_anchors[].quote`` appears verbatim on its cited line of
    ``thesis/ouroboros/papers/v26/unified-gpd-thesis-v26.md`` (drift detector);
  * required fields and types, 40-hex commit pins, verdict / severity /
    decision-status enums;
  * every theorem's ``kernel_axioms`` lies inside {propext, Classical.choice,
    Quot.sound}; the theorems cited are exactly the 24 carriers listed in
    lutar-lean ``tools/lean/LockedGuard.lean`` at the pin, each under its own
    locked id, and the recorded kernel summary matches the per-theorem data;
  * every quoted evidence item names a known repository (szl-papers,
    lutar-lean, szl-forge) and cites that repository's ledger pin;
  * szl-papers evidence quotes appear in the cited line ranges of this checkout;
  * with ``--lean-root``: lutar-lean quotes and statements appear in the cited
    line ranges of that tree, the two kernel input files match the recorded
    sha256, and the ``#geh_guard`` list in ``tools/lean/LockedGuard.lean`` is
    exactly the 24 carriers above (without ``--lean-root`` this is NOT_RUN);
  * the Markdown rendering agrees with the JSON: each row's own section carries
    its verdict and severity line, title, claim, gap or finding, quotes,
    evidence, proposed wording, owner decisions and, per declaration, the
    lean_ref, statement and kernel-axiom label; the summary tables, owner
    decision lines, pins and kernel evidence also match;
  * no line of the ledger files trips the org overclaim guard's rules A and B
    (unqualified Lambda uniqueness / Conjecture 1 called proven) or rule C
    (absolute security / correctness phrases). The regexes are copied from
    szl-holdings/.github reusable-overclaim-guard.yml @ 464069d.

It is stdlib-only, makes no network call and writes nothing. A passing default
run means the ledger is internally consistent, and that its manuscript anchors
and szl-papers quotes match the current checkout. lutar-lean quotes are
compared only with ``--lean-root``; szl-forge quotes are not checked. It does
not re-run the Lean kernel and says nothing about whether the manuscript or
the Lean code is right.

Usage:
    python3 scripts/check_review_ledger.py
    python3 scripts/check_review_ledger.py --json
    python3 scripts/check_review_ledger.py --lean-root /path/to/lutar-lean
    python3 scripts/check_review_ledger.py --self-test
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import re
import sys
import tempfile

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

LEDGER_REL = "reviews/v26-locked-eight-claim-ledger.json"
LEDGER_MD_REL = "reviews/v26-locked-eight-claim-ledger.md"
README_REL = "reviews/README.md"
MANUSCRIPT_REL = "thesis/ouroboros/papers/v26/unified-gpd-thesis-v26.md"

SCHEMA = "szl.papers.review-ledger/v1"
LOCKED_IDS = frozenset({"F1", "F4", "F7", "F11", "F12", "F18", "F19", "F22"})
TRUST_BASE = frozenset({"propext", "Classical.choice", "Quot.sound"})
VERDICTS = ("EXCEEDS", "PARTIAL", "MARGINAL", "MATCHES")
SEVERITIES = ("major", "moderate", "minor", "none")
DECL_KINDS = ("theorem", "def", "abbrev", "inductive")
DECISION_IDS = tuple(f"D{i}" for i in range(1, 10))
DECISION_STATUSES = ("OPEN", "TAKEN")
CROSS_CUTTING_IDS = ("P-X1", "P-X2", "P-X3", "P-X4", "P-X5")
KERNEL_STATUS_REQUIRED = "MEASURED"

SZL_PAPERS_REPO = "szl-holdings/szl-papers"
LUTAR_LEAN_REPO = "szl-holdings/lutar-lean"
SZL_FORGE_REPO = "szl-holdings/szl-forge"
# Repository -> key under ``pins``. A quoted evidence item must cite that pin.
PIN_KEY_BY_REPO = {
    SZL_PAPERS_REPO: "szl_papers",
    LUTAR_LEAN_REPO: "lutar_lean",
    SZL_FORGE_REPO: "szl_forge",
}

# Files the kernel axiom replica read; --lean-root compares their sha256.
PROVED_FORMULAS_REL = "Lutar/Puriq/Formulas/ProvedFormulas.lean"
LOCKED_GUARD_REL = "tools/lean/LockedGuard.lean"
KERNEL_INPUTS = (PROVED_FORMULAS_REL, LOCKED_GUARD_REL)

# The 24 carrier theorems guarded by lutar-lean tools/lean/LockedGuard.lean at
# 04f904ecd5683753a481ab2b1ded69ac01a7a661 (namespace Puriq.Formula.Proved).
CARRIER_NAMESPACE = "Puriq.Formula.Proved."
LOCKED_CARRIERS = frozenset({
    "f1_replay_hash_determinism", "f1_replay_trace_stable",
    "f11_ayni_reciprocity_conservation", "f12_kuramoto_additive",
    "f18_reed_solomon_parity_count", "f18_erasure_tolerance",
    "f19_bekenstein_additive", "f19_budget_monotone",
    "f4_khipu_no_self_loop", "f4_khipu_acyclic_irrefl",
    "f4_khipu_reach_strictly_smaller", "f4_khipu_reach_decreases",
    "f4_khipu_no_cycle", "f4_khipu_append_preserves_invariant",
    "f4_khipu_dag_acyclic_preserved",
    "f7_chaski_enqueueAll_nil", "f7_chaski_drain_eq",
    "f7_chaski_enqueue_preserves_prefix", "f7_chaski_head_is_oldest",
    "f7_chaski_fifo_order", "f7_chaski_fifo_positional",
    "f22_emit_appends_length", "f22_emit_strictly_greater",
    "f22_khipu_emit_monotone",
})

HEX40_RE = re.compile(r"^[0-9a-f]{40}$")
HEX64_RE = re.compile(r"^[0-9a-f]{64}$")
REF_RE = re.compile(r"^(?P<path>[^:\s]+):(?P<start>\d+)(?:-(?P<end>\d+))?$")
LEAN_REF_RE = re.compile(r"^[A-Za-z0-9_./-]+\.lean:\d+(?:-\d+)?$")
GUARD_LINE_RE = re.compile(r"^#geh_guard\s+(\S+)\s*$")

ENTRY_FIELDS = (
    "id", "row", "title", "lutar_lean_sha", "lean_decls", "lean_summary",
    "manuscript_anchors", "manuscript_claim", "verdict", "severity", "gap",
    "proposed_wording", "owner_decisions", "runtime_symbol",
)
DECL_FIELDS = ("decl", "kind", "primary", "lean_ref", "statement", "kernel_axioms")
CROSS_FIELDS = (
    "id", "title", "surface", "verdict", "severity", "finding",
    "manuscript_anchors", "evidence", "proposed_wording", "owner_decisions",
)

# --- org overclaim guard rules (reusable-overclaim-guard.yml @ 464069d) -----
# Rule A: unconditional "Lambda is unique" with no safe qualifier on the line.
RULE_A_RE = re.compile(
    r"(Λ|lambda)[^.|]{0,80}(is|are|was)[^.|]{0,40}uniqu|uniqu[a-z]*[^.|]{0,40}(of|for)"
    r"[^.|]{0,20}(Λ|lambda)[^.|]{0,40}(is |are )?(proven|proved|established|a theorem)",
    re.IGNORECASE,
)
RULE_A_SAFE_RE = re.compile(
    r"[Cc]onjecture|[Cc]onditional|modulo|≈Λ|≉Λ|Theorem U|TheoremU|U₁|U₂|under IA|"
    r"Identifiab|Anchored|Normalized|statement-only|machine-checked|FALSE|false|"
    r"not a theorem|NOT a theorem|never|stays|OPEN|open|bounty|lambda_unique_|"
    r"unique aggregator|min-gate|impostor",
    re.IGNORECASE,
)
# Rule B: Conjecture 1 declared proven / closed / resolved.
RULE_B_RE = re.compile(
    r"conjecture[ _-]?1\b[^.|]{0,25}(is |was |now |been |=|: )?"
    r"(proven|proved|closed|resolved|solved|a theorem|holds unconditionally)",
    re.IGNORECASE,
)
RULE_B_SAFE_RE = re.compile(
    r"statement-only|machine-checked|FALSE|false|OPEN|open|not |never|stays|bounty|"
    r"non-claim|unqualified|overclaim",
    re.IGNORECASE,
)
# Rule C: generic absolute security / correctness phrases (byte-identical to the guard).
RULE_C_TRIG_RE = re.compile(
    r"tamper[-\s]?proof|\bunbreakable\b|\bunhackable\b|\bun-?forgeable\b|bullet[-\s]?proof|"
    r"provably secure|provable security|(?:absolutely|completely|perfectly|fully|totally) "
    r"secure|impossible to (?:forge|break|hack|tamper|compromise|reverse)|cannot be "
    r"(?:forged|broken|hacked|compromised)|100\s*%\s*(?:secure|safe|accurate|reliable|"
    r"guaranteed|certain|correct|uptime|private|anonymous|unbreakable|foolproof)|"
    r"mathematically guaranteed|guaranteed (?:secure|safe|unhackable|unbreakable|correct|"
    r"accurate|private|tamper[-\s]?proof)|military[-\s]grade (?:encryption|security|crypto)|"
    r"\brisk[-\s]?free\b|\bzero[-\s]risk\b|\bfoolproof\b",
    re.IGNORECASE,
)
RULE_C_NEG_RE = re.compile(
    r"\bnot\b|\bnever\b|n't|\bwithout\b|\bnon-|tamper[-\s]?evident|less than 100|<\s?100|"
    r"sub-100|below 100",
    re.IGNORECASE,
)


# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------

def _dict(value) -> dict:
    """``value`` if it is a dict, else an empty dict (type errors are reported elsewhere)."""
    return value if isinstance(value, dict) else {}


def _list(value) -> list:
    """``value`` if it is a list, else an empty list (type errors are reported elsewhere)."""
    return value if isinstance(value, list) else []


def _key(value) -> str:
    """A hashable, printable stand-in for an arbitrary JSON value."""
    return value if isinstance(value, str) else repr(value)


def _all_str(values) -> bool:
    return isinstance(values, list) and all(isinstance(v, str) for v in values)


def _collapse(text: str) -> str:
    return " ".join(text.split())


def _read_lines(path: str) -> list[str]:
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read().splitlines()


def _safe_join(root: str, rel: str) -> str | None:
    """Join ``rel`` under ``root``; None if it is absolute or escapes ``root``."""
    if not isinstance(rel, str) or not rel or os.path.isabs(rel) or rel.startswith(("/", "\\")):
        return None
    parts = re.split(r"[\\/]", rel)
    if any(p in ("..", "") for p in parts):
        return None
    return os.path.join(root, *parts)


def _parse_ref(ref: object) -> tuple[str, int, int] | None:
    if not isinstance(ref, str):
        return None
    m = REF_RE.match(ref)
    if not m:
        return None
    start = int(m.group("start"))
    end = int(m.group("end") or start)
    if start < 1 or end < start:
        return None
    return m.group("path"), start, end


def _read_lf_bytes(path: str) -> bytes:
    with open(path, "rb") as fh:
        return fh.read().replace(b"\r\n", b"\n")


def git_blob_sha1(path: str) -> str:
    """Git blob id of ``path`` with CRLF normalised to LF (core.autocrlf checkouts)."""
    data = _read_lf_bytes(path)
    # Git object id, not a security use.
    return hashlib.sha1(b"blob %d\0" % len(data) + data, usedforsecurity=False).hexdigest()


def sha256_lf(path: str) -> str:
    """sha256 of ``path`` with CRLF normalised to LF (matches a ``git show`` export)."""
    return hashlib.sha256(_read_lf_bytes(path)).hexdigest()


def load_ledger(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data, dict):
        raise ValueError("ledger root must be a JSON object")
    return data


def _iter_strings(node, path="$"):
    if isinstance(node, str):
        yield path, node
    elif isinstance(node, dict):
        for k, v in node.items():
            yield from _iter_strings(v, f"{path}.{k}")
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from _iter_strings(v, f"{path}[{i}]")


def _rows(ledger: dict) -> list[dict]:
    return [r for r in _list(ledger.get("entries")) + _list(ledger.get("cross_cutting"))
            if isinstance(r, dict)]


def _row_id(row: dict) -> str:
    return _key(row.get("row") or row.get("id"))


# ---------------------------------------------------------------------------
# Checks (each returns a list of error strings; empty means no finding)
# ---------------------------------------------------------------------------

def check_top_level(ledger: dict) -> list[str]:
    errors = []
    if ledger.get("schema") != SCHEMA:
        errors.append(f"[field] schema must be {SCHEMA!r}")
    if ledger.get("normative") is not False:
        errors.append("[normative] a review ledger must declare \"normative\": false")
    for key in ("ledger_id", "title", "review_status", "date", "scope"):
        if not isinstance(ledger.get(key), str) or not ledger.get(key).strip():
            errors.append(f"[field] top-level {key!r} missing or empty")
    manuscript = ledger.get("manuscript")
    if not isinstance(manuscript, dict) or manuscript.get("path") != MANUSCRIPT_REL:
        errors.append(f"[field] manuscript.path must be {MANUSCRIPT_REL!r}")
    for key in ("entries", "cross_cutting", "owner_decisions"):
        if not isinstance(ledger.get(key), list):
            errors.append(f"[field] top-level {key!r} must be a list")
    if not isinstance(ledger.get("pins"), dict):
        errors.append("[field] top-level 'pins' must be an object")
    return errors


def check_pins(ledger: dict) -> list[str]:
    """Every commit-like value (keys ``sha``, ``*_sha``, ``*_change``) is 40-hex."""
    errors = []

    def walk(node, path):
        if isinstance(node, dict):
            for k, v in node.items():
                sub = f"{path}.{k}"
                if k == "sha" or k.endswith("_sha") or k.endswith("_change"):
                    if not (isinstance(v, str) and HEX40_RE.match(v)):
                        errors.append(f"[pin] {sub} must be a 40-hex commit id, got {v!r}")
                else:
                    walk(v, sub)
        elif isinstance(node, list):
            for i, v in enumerate(node):
                walk(v, f"{path}[{i}]")

    walk(ledger, "$")
    pins = _dict(ledger.get("pins"))
    for key, value in pins.items():
        if not isinstance(value, dict):
            errors.append(f"[pin] pins.{key} must be an object with repo and sha, got {value!r}")
    lean_pin = _dict(pins.get("lutar_lean")).get("sha")
    papers_pin = _dict(pins.get("szl_papers")).get("sha")
    if not lean_pin or not papers_pin:
        errors.append("[pin] pins.lutar_lean.sha and pins.szl_papers.sha are required")
    if papers_pin and _dict(ledger.get("manuscript")).get("sha") != papers_pin:
        errors.append("[pin] manuscript.sha must equal pins.szl_papers.sha")
    for entry in _list(ledger.get("entries")):
        if isinstance(entry, dict) and lean_pin and entry.get("lutar_lean_sha") != lean_pin:
            errors.append(f"[pin] {_key(entry.get('id'))}: lutar_lean_sha must equal pins.lutar_lean.sha")
    return errors


def check_locked_ids(ledger: dict) -> list[str]:
    errors = []
    ids = [_key(e.get("id")) for e in _list(ledger.get("entries")) if isinstance(e, dict)]
    dupes = sorted({i for i in ids if ids.count(i) > 1})
    if dupes:
        errors.append(f"[locked-ids] duplicate entry ids: {dupes}")
    missing = sorted(LOCKED_IDS - set(ids))
    extra = sorted(set(ids) - LOCKED_IDS)
    if missing:
        errors.append(f"[locked-ids] missing locked ids: {missing}")
    if extra:
        errors.append(f"[locked-ids] ids outside the locked eight: {extra}")
    declared = ledger.get("locked_ids")
    if not _all_str(declared) or set(declared) != LOCKED_IDS or len(declared) != 8:
        errors.append("[locked-ids] top-level locked_ids must be exactly the locked eight")
    return errors


def _carrier_prefix(entry_id: str) -> str:
    return entry_id.lower() + "_"


def check_fields(entry: dict) -> list[str]:
    """Required fields, types, enums, declarations and axiom sets for one locked-id row."""
    if not isinstance(entry, dict):
        return ["[field] entry must be an object"]
    eid = entry.get("id", "<no-id>")
    label = _key(eid)
    errors = []
    for key in ENTRY_FIELDS:
        if key not in entry:
            errors.append(f"[field] {label}: missing {key!r}")
    for key in ("title", "lean_summary", "manuscript_claim", "gap", "proposed_wording"):
        if key in entry and (not isinstance(entry[key], str) or not entry[key].strip()):
            errors.append(f"[field] {label}: {key!r} must be a non-empty string")
    if isinstance(eid, str) and entry.get("row") != f"P-{eid}":
        errors.append(f"[field] {label}: row must be 'P-{eid}'")
    if entry.get("verdict") not in VERDICTS:
        errors.append(f"[verdict] {label}: verdict {entry.get('verdict')!r} not in {VERDICTS}")
    if entry.get("severity") not in SEVERITIES:
        errors.append(f"[field] {label}: severity {entry.get('severity')!r} not in {SEVERITIES}")
    runtime = entry.get("runtime_symbol")
    if runtime is not None and (not isinstance(runtime, str) or not runtime.strip()):
        errors.append(f"[field] {label}: runtime_symbol must be null or a non-empty string")
    anchors = entry.get("manuscript_anchors")
    if not isinstance(anchors, list) or not anchors:
        errors.append(f"[field] {label}: manuscript_anchors must be a non-empty list")
    decls = entry.get("lean_decls")
    if not isinstance(decls, list) or not decls:
        errors.append(f"[field] {label}: lean_decls must be a non-empty list")
        return errors
    primaries = 0
    for d in decls:
        if not isinstance(d, dict):
            errors.append(f"[field] {label}: lean_decls items must be objects")
            continue
        name = d.get("decl", "<no-decl>")
        dlabel = f"{label}/{_key(name)}"
        for key in DECL_FIELDS:
            if key not in d:
                errors.append(f"[field] {dlabel}: missing {key!r}")
        if not isinstance(name, str) or not name.strip():
            errors.append(f"[field] {dlabel}: decl must be a non-empty string")
        if not isinstance(d.get("statement"), str) or not d["statement"].strip():
            errors.append(f"[field] {dlabel}: statement must be a non-empty quoted string")
        if not (isinstance(d.get("lean_ref"), str) and LEAN_REF_RE.match(d["lean_ref"])):
            errors.append(f"[field] {dlabel}: lean_ref must look like path.lean:LINE[-LINE]")
        if not isinstance(d.get("primary"), bool):
            errors.append(f"[field] {dlabel}: primary must be true or false")
        kind = d.get("kind")
        if kind not in DECL_KINDS:
            errors.append(f"[field] {dlabel}: kind {kind!r} not in {DECL_KINDS}")
        axioms = d.get("kernel_axioms")
        if kind == "theorem":
            if not _all_str(axioms):
                errors.append(f"[axioms] {dlabel}: theorem kernel_axioms must be a list of names")
            else:
                outside = sorted(set(axioms) - TRUST_BASE)
                if outside:
                    errors.append(
                        f"[axioms] {dlabel}: kernel_axioms {outside} outside "
                        f"{sorted(TRUST_BASE)}"
                    )
            short = name[len(CARRIER_NAMESPACE):] if isinstance(name, str) and \
                name.startswith(CARRIER_NAMESPACE) else None
            if short not in LOCKED_CARRIERS:
                errors.append(f"[carrier] {dlabel}: not one of the 24 LockedGuard carriers")
            elif isinstance(eid, str) and not short.startswith(_carrier_prefix(eid)):
                errors.append(f"[carrier] {dlabel}: carrier does not belong to {eid}")
        elif axioms is not None and not (_all_str(axioms) and set(axioms) <= TRUST_BASE):
            errors.append(f"[axioms] {dlabel}: non-theorem kernel_axioms must be null or in the trust base")
        if d.get("primary") is True:
            primaries += 1
            if kind != "theorem":
                errors.append(f"[field] {dlabel}: the primary declaration must be a theorem")
    if primaries != 1:
        errors.append(f"[field] {label}: exactly one primary lean_decl required, found {primaries}")
    return errors


def check_carrier_coverage(ledger: dict) -> list[str]:
    seen: list[str] = []
    for entry in _list(ledger.get("entries")):
        for d in _list(_dict(entry).get("lean_decls")):
            if isinstance(d, dict) and d.get("kind") == "theorem" and isinstance(d.get("decl"), str):
                seen.append(d["decl"][len(CARRIER_NAMESPACE):])
    errors = []
    dupes = sorted({s for s in seen if seen.count(s) > 1})
    if dupes:
        errors.append(f"[carrier] carriers cited more than once: {dupes}")
    missing = sorted(LOCKED_CARRIERS - set(seen))
    if missing:
        errors.append(f"[carrier] LockedGuard carriers without a row: {missing}")
    return errors


def check_kernel_summary(ledger: dict) -> list[str]:
    errors = []
    ev = ledger.get("kernel_axiom_evidence")
    if not isinstance(ev, dict):
        return ["[kernel-summary] kernel_axiom_evidence object missing"]
    if ev.get("status") != KERNEL_STATUS_REQUIRED:
        errors.append(
            f"[kernel-summary] status is {ev.get('status')!r}; the per-theorem axiom sets "
            f"need {KERNEL_STATUS_REQUIRED!r} evidence (UNKNOWN is never a pass)"
        )
    trust = ev.get("trust_base")
    if not _all_str(trust) or set(trust) != TRUST_BASE:
        errors.append("[kernel-summary] trust_base must be {propext, Classical.choice, Quot.sound}")
    for key in ("method", "environment", "date"):
        if not isinstance(ev.get(key), str) or not ev.get(key).strip():
            errors.append(f"[kernel-summary] {key!r} missing")
    hashes = ev.get("input_sha256")
    if not isinstance(hashes, dict) or set(hashes) != set(KERNEL_INPUTS) or not all(
            isinstance(v, str) and HEX64_RE.match(v) for v in hashes.values()):
        errors.append(
            f"[kernel-summary] input_sha256 must map exactly {list(KERNEL_INPUTS)} to 64-hex sha256 values"
        )
    sets = []
    for entry in _list(ledger.get("entries")):
        for d in _list(_dict(entry).get("lean_decls")):
            if isinstance(d, dict) and d.get("kind") == "theorem" and _all_str(d.get("kernel_axioms")):
                sets.append(frozenset(d["kernel_axioms"]))
    computed = {
        "carriers": len(sets),
        "allowed_true": sum(1 for s in sets if s <= TRUST_BASE),
        "allowed_false": sum(1 for s in sets if not s <= TRUST_BASE),
        "no_axiom": sum(1 for s in sets if not s),
        "propext_only": sum(1 for s in sets if s == {"propext"}),
        "propext_and_quot_sound": sum(1 for s in sets if s == {"propext", "Quot.sound"}),
        "uses_classical_choice": sum(1 for s in sets if "Classical.choice" in s),
    }
    recorded = _dict(ev.get("result"))
    for key, value in computed.items():
        if recorded.get(key) != value:
            errors.append(
                f"[kernel-summary] result.{key} records {recorded.get(key)!r} but the "
                f"per-theorem data gives {value}"
            )
    if computed["carriers"] != len(LOCKED_CARRIERS):
        errors.append(f"[kernel-summary] expected {len(LOCKED_CARRIERS)} carriers, found {computed['carriers']}")
    return errors


def check_owner_decisions(ledger: dict) -> list[str]:
    errors = []
    decisions = _list(ledger.get("owner_decisions"))
    ids = [_key(d.get("id")) for d in decisions if isinstance(d, dict)]
    if sorted(ids) != sorted(DECISION_IDS) or len(ids) != len(set(ids)):
        errors.append(f"[decision] owner_decisions must be exactly {list(DECISION_IDS)}, got {ids}")
    for d in decisions:
        if not isinstance(d, dict):
            errors.append("[decision] owner_decisions items must be objects")
            continue
        if d.get("status") not in DECISION_STATUSES:
            errors.append(f"[decision] {_key(d.get('id'))}: status {d.get('status')!r} not in {DECISION_STATUSES}")
        if not isinstance(d.get("question"), str) or not d["question"].strip():
            errors.append(f"[decision] {_key(d.get('id'))}: question missing")
    for row in _rows(ledger):
        refs = row.get("owner_decisions")
        if not isinstance(refs, list):
            errors.append(f"[decision] {_row_id(row)}: owner_decisions must be a list")
            continue
        unknown = sorted(set(map(_key, refs)) - set(DECISION_IDS))
        if unknown:
            errors.append(f"[decision] {_row_id(row)}: unknown owner decision ids {unknown}")
    return errors


def check_cross_cutting(row: dict) -> list[str]:
    if not isinstance(row, dict):
        return ["[field] cross_cutting rows must be objects"]
    rid = _key(row.get("id", "<no-id>"))
    errors = []
    for key in CROSS_FIELDS:
        if key not in row:
            errors.append(f"[field] {rid}: missing {key!r}")
    for key in ("title", "surface", "finding", "proposed_wording"):
        if key in row and (not isinstance(row[key], str) or not row[key].strip()):
            errors.append(f"[field] {rid}: {key!r} must be a non-empty string")
    verdict = row.get("verdict")
    if verdict is not None and verdict not in VERDICTS:
        errors.append(f"[verdict] {rid}: verdict {verdict!r} must be null or in {VERDICTS}")
    severity = row.get("severity")
    if verdict is None and severity is not None:
        errors.append(f"[field] {rid}: an inventory row (verdict null) takes severity null")
    if verdict is not None and severity not in SEVERITIES:
        errors.append(f"[field] {rid}: severity {severity!r} not in {SEVERITIES}")
    for key in ("manuscript_anchors", "evidence"):
        if not isinstance(row.get(key), list):
            errors.append(f"[field] {rid}: {key!r} must be a list")
    return errors


def check_cross_cutting_ids(ledger: dict) -> list[str]:
    ids = [r.get("id") for r in _list(ledger.get("cross_cutting")) if isinstance(r, dict)]
    if ids != list(CROSS_CUTTING_IDS):
        return [f"[field] cross_cutting ids must be {list(CROSS_CUTTING_IDS)} in order, got {ids}"]
    return []


def _pin_for(ledger: dict, repo: str) -> str | None:
    key = PIN_KEY_BY_REPO.get(repo)
    return _dict(_dict(ledger.get("pins")).get(key)).get("sha") if key else None


def _evidence_items(ledger: dict):
    """Yield (label, item) for every evidence / cross_refs item of every row."""
    for row in _rows(ledger):
        rid = _row_id(row)
        for key in ("evidence", "cross_refs"):
            for k, item in enumerate(_list(row.get(key))):
                yield f"{rid}.{key}[{k}]", item


def check_evidence(ledger: dict) -> list[str]:
    """Evidence and cross-reference items: known repo, 40-hex sha, ref + quote, pinned."""
    errors = []
    for row in _rows(ledger):
        if "cross_refs" in row and not isinstance(row["cross_refs"], list):
            errors.append(f"[evidence] {_row_id(row)}: cross_refs must be a list")
    for label, item in _evidence_items(ledger):
        if not isinstance(item, dict):
            errors.append(f"[evidence] {label}: item must be an object")
            continue
        repo = item.get("repo")
        if repo not in PIN_KEY_BY_REPO:
            errors.append(f"[evidence] {label}: repo {repo!r} is not one of {sorted(PIN_KEY_BY_REPO)}")
            continue
        sha = item.get("sha")
        if not (isinstance(sha, str) and HEX40_RE.match(sha)):
            errors.append(f"[evidence] {label}: needs a full 40-hex 'sha', got {sha!r}")
            continue
        if item.get("ref") is None:
            if not isinstance(item.get("note"), str) or not item["note"].strip():
                errors.append(f"[evidence] {label}: an item without a ref needs a note")
            continue
        if _parse_ref(item.get("ref")) is None or not isinstance(item.get("quote"), str) \
                or not item["quote"].strip():
            errors.append(f"[evidence] {label}: ref {item.get('ref')!r} needs PATH:LINE[-LINE] and a quote")
            continue
        pin = _pin_for(ledger, repo)
        if sha != pin:
            errors.append(
                f"[evidence] {label}: a quoted {repo} ref must cite pins.{PIN_KEY_BY_REPO[repo]}.sha "
                f"({str(pin)[:12]}), got {sha[:12]}"
            )
    return errors


def check_anchor(manuscript_lines: list[str], anchor: dict, label: str) -> list[str]:
    """The quote must appear verbatim on the cited manuscript line."""
    if not isinstance(anchor, dict):
        return [f"[anchor] {label}: anchor must be an object"]
    line, quote = anchor.get("line"), anchor.get("quote")
    if not isinstance(anchor.get("section"), str) or not anchor["section"].strip():
        return [f"[anchor] {label}: section missing"]
    if not isinstance(quote, str) or not quote.strip():
        return [f"[anchor] {label}: quote missing"]
    if not isinstance(line, int) or isinstance(line, bool) or not 1 <= line <= len(manuscript_lines):
        return [f"[anchor] {label}: line {line!r} outside the manuscript (1..{len(manuscript_lines)})"]
    if quote in manuscript_lines[line - 1]:
        return []
    elsewhere = [i + 1 for i, text in enumerate(manuscript_lines) if quote in text]
    hint = f"; found on line(s) {elsewhere[:5]}" if elsewhere else "; not found anywhere"
    return [f"[anchor] {label}: quote not on manuscript line {line}{hint}: {quote[:80]!r}"]


def check_ranged_quote(root: str, item: dict, label: str, code: str) -> list[str]:
    """Whitespace-collapsed ``quote`` must occur in the cited line range under ``root``."""
    parsed = _parse_ref(item.get("ref") if "ref" in item else item.get("lean_ref"))
    quote = item.get("quote") if "quote" in item else item.get("statement")
    if parsed is None or not isinstance(quote, str):
        return [f"[{code}] {label}: unusable ref or quote"]
    rel, start, end = parsed
    path = _safe_join(root, rel)
    if path is None:
        return [f"[{code}] {label}: ref path {rel!r} must be relative and stay inside the checkout"]
    if not os.path.isfile(path):
        return [f"[{code}] {label}: {rel} not found under {root}"]
    lines = _read_lines(path)
    if end > len(lines):
        return [f"[{code}] {label}: {rel}:{start}-{end} beyond end of file ({len(lines)} lines)"]
    window = _collapse(" ".join(lines[start - 1:end]))
    if _collapse(quote) in window:
        return []
    return [f"[{code}] {label}: quote not in {rel}:{start}-{end}: {quote[:80]!r}"]


def check_lean_root_pin(ledger: dict, lean_root: str) -> list[str]:
    """--lean-root must hold the pinned kernel inputs and the 24-carrier guard list."""
    errors = []
    hashes = _dict(_dict(ledger.get("kernel_axiom_evidence")).get("input_sha256"))
    for rel, expected in sorted(hashes.items()):
        path = _safe_join(lean_root, rel)
        if path is None or not os.path.isfile(path):
            errors.append(f"[lean-pin] {rel} not found under --lean-root {lean_root}")
            continue
        actual = sha256_lf(path)
        if actual != expected:
            errors.append(
                f"[lean-pin] {rel}: sha256 {actual[:12]} differs from kernel_axiom_evidence."
                f"input_sha256 {str(expected)[:12]}; --lean-root is not at the pinned files"
            )
    guard_path = _safe_join(lean_root, LOCKED_GUARD_REL)
    if guard_path is None or not os.path.isfile(guard_path):
        errors.append(f"[lean-guard] {LOCKED_GUARD_REL} not found under --lean-root {lean_root}")
        return errors
    guarded = []
    for line in _read_lines(guard_path):
        m = GUARD_LINE_RE.match(line.strip())
        if m:
            guarded.append(m.group(1))
    expected_names = {CARRIER_NAMESPACE + c for c in LOCKED_CARRIERS}
    if set(guarded) != expected_names or len(guarded) != len(expected_names):
        errors.append(
            f"[lean-guard] {LOCKED_GUARD_REL} guards {len(guarded)} theorems; missing "
            f"{sorted(expected_names - set(guarded))}, extra {sorted(set(guarded) - expected_names)}"
        )
    return errors


def scan_overclaims(label: str, lines: list[str]) -> list[str]:
    """Apply the org overclaim guard's rules A, B and C line by line."""
    errors = []
    for i, line in enumerate(lines):
        if RULE_A_RE.search(line) and not RULE_A_SAFE_RE.search(line):
            errors.append(f"[overclaim-A] {label}:{i + 1}: unqualified Lambda uniqueness: {line.strip()[:160]}")
        if RULE_B_RE.search(line) and not RULE_B_SAFE_RE.search(line):
            errors.append(f"[overclaim-B] {label}:{i + 1}: Conjecture 1 called proven/closed: {line.strip()[:160]}")
        if RULE_C_TRIG_RE.search(line):
            prev = lines[i - 1] if i > 0 else ""
            if not (RULE_C_NEG_RE.search(line) or RULE_C_NEG_RE.search(prev)):
                errors.append(f"[overclaim-C] {label}:{i + 1}: absolute security/correctness phrase: {line.strip()[:160]}")
    return errors


def check_no_lambda_overclaim(text: str, label: str) -> list[str]:
    return scan_overclaims(label, text.splitlines())


# --- Markdown rendering contract -------------------------------------------

def _md_sections(md_text: str) -> list[tuple[str, list[str]]]:
    """``### `` sections as (heading, body lines); a ``#``/``##`` heading closes a section."""
    sections: list[tuple[str, list[str]]] = []
    current = None
    for line in md_text.splitlines():
        if line.startswith("### "):
            current = (line, [])
            sections.append(current)
        elif line.startswith("# ") or line.startswith("## "):
            current = None
        elif current is not None:
            current[1].append(line)
    return sections


def axiom_label(decl: dict) -> str:
    """How a declaration's kernel axioms are rendered at the end of its Markdown bullet."""
    axioms = decl.get("kernel_axioms")
    if axioms is None:
        return "definition (no axiom check)"
    if not _all_str(axioms):
        return f"kernel axioms: {axioms!r}"
    return "kernel axioms: " + ("none" if not axioms else ", ".join(f"`{a}`" for a in axioms))


def summary_row(row: dict, entry: bool) -> str | None:
    """The summary-table line the Markdown must carry for ``row``."""
    if entry:
        primary = next((d for d in _list(row.get("lean_decls"))
                        if isinstance(d, dict) and d.get("primary") is True), None)
        if primary is None:
            return None
        axioms = primary.get("kernel_axioms")
        shown = "none" if not axioms else (", ".join(axioms) if _all_str(axioms) else repr(axioms))
        return (f"| {row.get('row')} | {row.get('id')} | `{primary.get('decl')}` | {shown} | "
                f"**{row.get('verdict')}** | {row.get('severity')} |")
    return (f"| {row.get('id')} | {row.get('title')} | **{row.get('verdict') or 'inventory'}** | "
            f"{row.get('severity') or '-'} |")


def verdict_line(row: dict) -> str:
    verdict = row.get("verdict")
    shown = verdict if verdict is not None else "inventory (no verdict)"
    severity = row.get("severity")
    return f"Verdict **{shown}** · severity {severity if severity is not None else '-'}"


def kernel_result_line(ev: dict) -> str:
    r = _dict(ev.get("result"))
    return (f"{r.get('allowed_true')}/{r.get('carriers')} carriers allowed, {r.get('allowed_false')} refused. "
            f"{r.get('no_axiom')} use no axiom, {r.get('propext_only')} use `propext` only, "
            f"{r.get('propext_and_quot_sound')} use `propext` + `Quot.sound`; "
            f"{r.get('uses_classical_choice')} use `Classical.choice`.")


def _section_texts(row: dict) -> list[tuple[str, str]]:
    """(what, text) pairs that must appear inside the row's own Markdown section."""
    texts = []
    for key in ("title", "lean_summary", "manuscript_claim", "gap", "finding", "proposed_wording"):
        if isinstance(row.get(key), str):
            texts.append((key, row[key]))
    for a in _list(row.get("manuscript_anchors")):
        if isinstance(a, dict) and isinstance(a.get("quote"), str):
            texts.append(("manuscript quote", a["quote"]))
    for key in ("evidence", "cross_refs"):
        for item in _list(row.get(key)):
            for field in ("ref", "quote", "note"):
                if isinstance(item, dict) and isinstance(item.get(field), str):
                    texts.append((f"{key} {field}", item[field]))
    if isinstance(row.get("runtime_symbol"), str):
        texts.append(("runtime_symbol", f"`{row['runtime_symbol']}`"))
    return texts


def check_markdown_sync(ledger: dict, md_text: str) -> list[str]:
    """The Markdown rendering must agree with the JSON, row by row and table by table."""
    errors = []
    lines = {ln.strip() for ln in md_text.splitlines()}
    sections = _md_sections(md_text)
    entries = [e for e in _list(ledger.get("entries")) if isinstance(e, dict)]
    cross = [x for x in _list(ledger.get("cross_cutting")) if isinstance(x, dict)]
    for is_entry, row in [(True, e) for e in entries] + [(False, x) for x in cross]:
        rid = _row_id(row)
        verdict = row.get("verdict")
        own = re.compile(r"^### " + re.escape(rid) + r"(?![\w-])")
        mine = [s for s in sections if own.match(s[0])]
        if len(mine) != 1:
            errors.append(f"[md-sync] {rid}: expected exactly one '### {rid}' section, found {len(mine)}")
            continue
        heading, body = mine[0]
        text = "\n".join([heading] + body)
        shown = verdict if verdict is not None else "inventory"
        if not re.search(r"(?<![\w-])" + re.escape(str(shown)) + r"(?![\w-])", heading):
            errors.append(f"[md-sync] {rid}: section heading does not carry verdict {shown}")
        want = verdict_line(row)
        if not any(ln.startswith(want) for ln in body):
            errors.append(f"[md-sync] {rid}: section lacks the line {want!r}")
        for what, value in _section_texts(row):
            if value not in text:
                errors.append(f"[md-sync] {rid}: {what} missing from its section: {value[:60]!r}")
        for d in _list(row.get("lean_decls")):
            if not isinstance(d, dict) or not isinstance(d.get("decl"), str):
                continue
            bullets = [ln for ln in body if ln.startswith(f"- `{d['decl']}`")]
            if len(bullets) != 1:
                errors.append(f"[md-sync] {rid}: declaration {d['decl']} needs exactly one bullet, found {len(bullets)}")
                continue
            bullet = bullets[0]
            if ("(primary)" in bullet) != (d.get("primary") is True):
                errors.append(f"[md-sync] {rid}: declaration {d['decl']} primary marker differs from the JSON")
            if isinstance(d.get("lean_ref"), str) and f"`{d['lean_ref']}`" not in bullet:
                errors.append(f"[md-sync] {rid}: declaration {d['decl']} lean_ref {d['lean_ref']} missing from its bullet")
            if not bullet.endswith(axiom_label(d)):
                errors.append(f"[md-sync] {rid}: declaration {d['decl']} kernel axioms differ from the JSON "
                              f"(want {axiom_label(d)!r})")
            if isinstance(d.get("statement"), str) and d["statement"] not in text:
                errors.append(f"[md-sync] {rid}: declaration {d['decl']} statement missing from its section")
        decisions = ", ".join(map(_key, _list(row.get("owner_decisions"))))
        owner_re = re.compile(r"^\*\*Owner decisions:\*\* " + re.escape(decisions) + r"(?: ·|$)")
        if not any(owner_re.match(ln) for ln in body):
            errors.append(f"[md-sync] {rid}: owner decisions line is not '{decisions}'")
        want_summary = summary_row(row, is_entry)
        if want_summary is not None and want_summary not in lines:
            errors.append(f"[md-sync] {rid}: summary table row does not match the JSON (want {want_summary!r})")
    for d in _list(ledger.get("owner_decisions")):
        if isinstance(d, dict):
            want = f"- **{d.get('id')}** ({d.get('status')}): {d.get('question')}"
            if want not in lines:
                errors.append(f"[md-sync] owner decision {_key(d.get('id'))} line does not match the JSON")
    ev = _dict(ledger.get("kernel_axiom_evidence"))
    for key in ("method", "environment", "agrees_with", "rerun_trigger"):
        if isinstance(ev.get(key), str) and ev[key] not in md_text:
            errors.append(f"[md-sync] kernel_axiom_evidence.{key} missing from Markdown")
    if ev and kernel_result_line(ev) not in md_text:
        errors.append(f"[md-sync] kernel result line missing (want {kernel_result_line(ev)!r})")
    for rel, digest in _dict(ev.get("input_sha256")).items():
        if f"`{digest}`" not in md_text:
            errors.append(f"[md-sync] input_sha256 of {rel} missing from Markdown")
    for key, pin in _dict(ledger.get("pins")).items():
        sha = _dict(pin).get("sha")
        if isinstance(sha, str) and f"`{sha}`" not in md_text:
            errors.append(f"[md-sync] pins.{key}.sha missing from Markdown")
    return errors


# ---------------------------------------------------------------------------
# Evaluate
# ---------------------------------------------------------------------------

def evaluate(repo_root: str, ledger_path: str | None = None,
             lean_root: str | None = None) -> dict:
    errors: list[str] = []
    notes: list[str] = []
    stats = {
        "anchors_checked": 0, "papers_quotes_checked": 0, "lean_quotes_checked": 0,
        "external_quotes_unchecked": 0, "overclaim_lines_scanned": 0,
    }
    ledger_path = ledger_path or os.path.join(repo_root, *LEDGER_REL.split("/"))
    result = {"ledger": ledger_path, "errors": errors, "notes": notes, "stats": stats,
              "verdicts": {}, "lean_check": "NOT_RUN", "ok": False}
    try:
        ledger = load_ledger(ledger_path)
    except (OSError, ValueError) as exc:
        errors.append(f"[load] cannot read ledger {ledger_path}: {exc}")
        return result

    errors += check_top_level(ledger)
    if errors:
        return result  # fail closed: the walks below need these top-level types
    errors += check_pins(ledger)
    errors += check_locked_ids(ledger)
    for entry in ledger["entries"]:
        errors += check_fields(entry)
    errors += check_carrier_coverage(ledger)
    errors += check_kernel_summary(ledger)
    errors += check_cross_cutting_ids(ledger)
    for row in ledger["cross_cutting"]:
        errors += check_cross_cutting(row)
    errors += check_evidence(ledger)
    errors += check_owner_decisions(ledger)

    for entry in ledger["entries"]:
        if isinstance(entry, dict):
            v = _key(entry.get("verdict"))
            result["verdicts"][v] = result["verdicts"].get(v, 0) + 1

    # Manuscript anchors (exact line match) + blob provenance note.
    rows = _rows(ledger)
    manuscript_path = os.path.join(repo_root, *MANUSCRIPT_REL.split("/"))
    try:
        manuscript_lines = _read_lines(manuscript_path)
    except OSError as exc:
        errors.append(f"[anchor] cannot read manuscript {MANUSCRIPT_REL}: {exc}")
        manuscript_lines = None
    if manuscript_lines is not None:
        for row in rows:
            rid = _row_id(row)
            for k, anchor in enumerate(_list(row.get("manuscript_anchors"))):
                errors += check_anchor(manuscript_lines, anchor, f"{rid}.manuscript_anchors[{k}]")
                stats["anchors_checked"] += 1
        pinned_blob = _dict(ledger.get("manuscript")).get("blob_sha")
        actual_blob = git_blob_sha1(manuscript_path)
        if actual_blob == pinned_blob:
            notes.append(f"manuscript blob matches the pinned blob {actual_blob[:12]}")
        else:
            notes.append(
                f"manuscript blob {actual_blob[:12]} differs from the pinned blob "
                f"{str(pinned_blob)[:12]}; anchors above are still checked line by line"
            )

    # Evidence and Lean quotes. Malformed items were reported by check_evidence.
    lean_items = []
    for row in rows:
        rid = _row_id(row)
        for d in _list(row.get("lean_decls")):
            if isinstance(d, dict):
                lean_items.append((f"{rid}/{_key(d.get('decl'))}", d))
    for label, item in _evidence_items(ledger):
        if not isinstance(item, dict) or item.get("ref") is None:
            continue
        repo = item.get("repo")
        if repo == SZL_PAPERS_REPO:
            errors += check_ranged_quote(repo_root, item, label, "papers-quote")
            stats["papers_quotes_checked"] += 1
        elif repo == LUTAR_LEAN_REPO:
            lean_items.append((label, item))
        elif repo == SZL_FORGE_REPO:
            stats["external_quotes_unchecked"] += 1
    if lean_root:
        if not os.path.isdir(lean_root):
            errors.append(f"[lean-quote] --lean-root {lean_root} is not a directory")
        else:
            for label, item in lean_items:
                errors += check_ranged_quote(lean_root, item, label, "lean-quote")
                stats["lean_quotes_checked"] += 1
            errors += check_lean_root_pin(ledger, lean_root)
            result["lean_check"] = "RUN"
    else:
        stats["lean_quotes_unchecked"] = len(lean_items)

    # Overclaim scan over the review files (raw lines; JSON also per decoded string).
    md_path = os.path.join(repo_root, *LEDGER_MD_REL.split("/"))
    readme_path = os.path.join(repo_root, *README_REL.split("/"))
    for rel, path in ((LEDGER_REL, ledger_path), (LEDGER_MD_REL, md_path), (README_REL, readme_path)):
        try:
            lines = _read_lines(path)
        except OSError as exc:
            errors.append(f"[load] cannot read {rel}: {exc}")
            continue
        errors += scan_overclaims(rel, lines)
        stats["overclaim_lines_scanned"] += len(lines)
    for spath, value in _iter_strings(ledger):
        errors += check_no_lambda_overclaim(value, f"{LEDGER_REL}#{spath}")

    # Markdown rendering and README index.
    try:
        with open(md_path, "r", encoding="utf-8") as fh:
            errors += check_markdown_sync(ledger, fh.read())
    except OSError:
        pass  # already reported by the overclaim scan
    try:
        with open(readme_path, "r", encoding="utf-8") as fh:
            readme = fh.read()
        for needle in ("non-normative", os.path.basename(LEDGER_REL), os.path.basename(LEDGER_MD_REL)):
            if needle not in readme:
                errors.append(f"[readme] {README_REL} must mention {needle!r}")
    except OSError:
        pass

    result["ok"] = not errors
    return result


# ---------------------------------------------------------------------------
# Self-test (positive + negative fixtures in a temporary directory)
# ---------------------------------------------------------------------------

_FIX_LEAN_PIN = "1" * 40
_FIX_PAPERS_PIN = "2" * 40
_FIX_FORGE_PIN = "4" * 40


def _expect(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _fixture_files() -> tuple[list[str], list[str], list[str]]:
    manuscript = ["# Fixture manuscript"] + [f"Locked {i} is described here." for i in sorted(LOCKED_IDS)]
    lean = [f"theorem {name} : True := trivial" for name in sorted(LOCKED_CARRIERS)]
    guard = ["-- fixture guard"] + [f"#geh_guard {CARRIER_NAMESPACE}{name}" for name in sorted(LOCKED_CARRIERS)]
    return manuscript, lean, guard


def _text_sha256(lines: list[str]) -> str:
    return hashlib.sha256(("\n".join(lines) + "\n").encode("utf-8")).hexdigest()


def _fixture_ledger(manuscript: list[str], lean: list[str], guard: list[str]) -> dict:
    entries = []
    for eid in sorted(LOCKED_IDS):
        decls = []
        for idx, text in enumerate(lean):
            short = text.split()[1]
            if short.startswith(_carrier_prefix(eid)):
                decls.append({
                    "decl": CARRIER_NAMESPACE + short, "kind": "theorem",
                    "primary": not decls, "lean_ref": f"{PROVED_FORMULAS_REL}:{idx + 1}",
                    "statement": text, "kernel_axioms": [],
                })
        line = manuscript.index(f"Locked {eid} is described here.") + 1
        entries.append({
            "id": eid, "row": f"P-{eid}", "title": f"{eid} fixture",
            "lutar_lean_sha": _FIX_LEAN_PIN, "lean_decls": decls,
            "lean_summary": f"{eid} states True.", "manuscript_claim": f"{eid} fixture claim.",
            "manuscript_anchors": [{"section": "§1", "line": line, "quote": f"Locked {eid} is described"}],
            "verdict": "MATCHES", "severity": "none", "gap": f"{eid}: none in the fixture.",
            "proposed_wording": f"{eid} [locked]: a fixture statement.",
            "owner_decisions": ["D1"], "runtime_symbol": None,
            "cross_refs": [{"repo": LUTAR_LEAN_REPO, "sha": _FIX_LEAN_PIN,
                            "ref": f"{PROVED_FORMULAS_REL}:1", "quote": lean[0]}],
        })
    cross = []
    for rid in CROSS_CUTTING_IDS:
        cross.append({
            "id": rid, "title": f"{rid} fixture", "surface": "manuscript",
            "verdict": None if rid == "P-X5" else "MATCHES",
            "severity": None if rid == "P-X5" else "none",
            "finding": f"{rid} fixture finding.", "manuscript_anchors": [],
            "evidence": [{"repo": SZL_PAPERS_REPO, "sha": _FIX_PAPERS_PIN,
                          "ref": "NOTES.md:2", "quote": "evidence line two"},
                         {"repo": SZL_FORGE_REPO, "sha": _FIX_FORGE_PIN,
                          "ref": "forge/index.json:3", "quote": "not checked by the script"},
                         {"repo": LUTAR_LEAN_REPO, "sha": "5" * 40, "ref": None,
                          "note": f"{rid}: a note about an older commit."}],
            "proposed_wording": f"{rid} fixture wording.", "owner_decisions": ["D2"],
        })
    return {
        "schema": SCHEMA, "ledger_id": "fixture", "title": "Fixture ledger",
        "normative": False, "review_status": "DRAFT_FOR_OWNER_REVIEW",
        "date": "2026-10-06", "scope": "Self-test fixture.",
        "manuscript": {"repo": SZL_PAPERS_REPO, "path": MANUSCRIPT_REL,
                       "sha": _FIX_PAPERS_PIN, "blob_sha": "3" * 40},
        "pins": {"szl_papers": {"repo": SZL_PAPERS_REPO, "sha": _FIX_PAPERS_PIN},
                 "lutar_lean": {"repo": LUTAR_LEAN_REPO, "sha": _FIX_LEAN_PIN},
                 "szl_forge": {"repo": SZL_FORGE_REPO, "sha": _FIX_FORGE_PIN}},
        "locked_ids": sorted(LOCKED_IDS),
        "kernel_axiom_evidence": {
            "status": "MEASURED", "trust_base": sorted(TRUST_BASE),
            "method": "fixture method", "environment": "fixture environment", "date": "2026-10-06",
            "input_sha256": {PROVED_FORMULAS_REL: _text_sha256(lean), LOCKED_GUARD_REL: _text_sha256(guard)},
            "result": {"carriers": 24, "allowed_true": 24, "allowed_false": 0,
                       "no_axiom": 24, "propext_only": 0, "propext_and_quot_sound": 0,
                       "uses_classical_choice": 0},
            "agrees_with": "fixture agreement", "rerun_trigger": "fixture trigger",
        },
        "entries": entries, "cross_cutting": cross,
        "owner_decisions": [{"id": d, "status": "TAKEN" if d == "D2" else "OPEN",
                             "question": f"Fixture question {d}?"} for d in DECISION_IDS],
    }


def _fixture_markdown(ledger: dict) -> str:
    """Render a fixture ledger the way the real Markdown is laid out."""
    out = ["# Fixture ledger", "", "## Pins", ""]
    out += [f"- {k}: `{_dict(v).get('sha')}`" for k, v in _dict(ledger.get("pins")).items()]
    ev = _dict(ledger.get("kernel_axiom_evidence"))
    out += ["", "## Kernel", "", f"- Method: {ev.get('method')}", f"- Environment: {ev.get('environment')}",
            f"- Result: {kernel_result_line(ev)}", f"- Agrees with: {ev.get('agrees_with')}",
            f"- Re-run when: {ev.get('rerun_trigger')}"]
    out += [f"- `{k}` `{v}`" for k, v in _dict(ev.get("input_sha256")).items()]
    entries = [e for e in _list(ledger.get("entries")) if isinstance(e, dict)]
    cross = [x for x in _list(ledger.get("cross_cutting")) if isinstance(x, dict)]
    out += ["", "## Summary", ""]
    out += [summary_row(e, True) or "" for e in entries]
    out += [summary_row(x, False) or "" for x in cross]
    out += ["", "## Rows", ""]
    for row in entries + cross:
        out += [f"### {_row_id(row)} · {row.get('verdict') or 'inventory'} · {row.get('title')}", "",
                verdict_line(row), ""]
        for d in _list(row.get("lean_decls")):
            tag = " (primary)" if d.get("primary") else ""
            out += [f"- `{d.get('decl')}`{tag} · {d.get('kind')} · `{d.get('lean_ref')}` · {axiom_label(d)}",
                    f"  {d.get('statement')}"]
        for key in ("lean_summary", "manuscript_claim", "gap", "finding"):
            if key in row:
                out.append(f"{key}: {row[key]}")
        out += [f"- L{a.get('line')}: `` {a.get('quote')} ``" for a in _list(row.get("manuscript_anchors"))]
        for item in _list(row.get("evidence")) + _list(row.get("cross_refs")):
            if item.get("ref"):
                out.append(f"- `{item.get('ref')}`: `` {item.get('quote')} ``")
            else:
                out.append(f"- {item.get('note')}")
        out.append(f"Proposed: {row.get('proposed_wording', '')}")
        rs = f" · runtime `{row['runtime_symbol']}`" if row.get("runtime_symbol") else ""
        out += [f"**Owner decisions:** {', '.join(map(_key, _list(row.get('owner_decisions'))))}{rs}", ""]
    out += ["## Owner decisions", ""]
    out += [f"- **{d['id']}** ({d['status']}): {d['question']}" for d in ledger["owner_decisions"]]
    return "\n".join(out) + "\n"


_FIX_README = (
    "# Reviews\n\nReviews here are non-normative.\n"
    "- v26-locked-eight-claim-ledger.md\n- v26-locked-eight-claim-ledger.json\n"
)


def _write(root: str, rel: str, text: str) -> None:
    path = os.path.join(root, *rel.split("/"))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


def _write_fixture(root: str, ledger: dict, md: str, readme: str = _FIX_README,
                   manuscript: list[str] | None = None, lean: list[str] | None = None,
                   guard: list[str] | None = None, ensure_ascii: bool = False) -> str:
    _write(root, LEDGER_REL, json.dumps(ledger, ensure_ascii=ensure_ascii, indent=2) + "\n")
    _write(root, LEDGER_MD_REL, md)
    _write(root, README_REL, readme)
    _write(root, "NOTES.md", "evidence line one\nevidence line two\n")
    if manuscript is not None:
        _write(root, MANUSCRIPT_REL, "\n".join(manuscript) + "\n")
    lean_root = os.path.join(root, "_lean")
    if lean is not None:
        _write(lean_root, PROVED_FORMULAS_REL, "\n".join(lean) + "\n")
    if guard is not None:
        _write(lean_root, LOCKED_GUARD_REL, "\n".join(guard) + "\n")
    return lean_root


def _self_test() -> int:
    manuscript, lean, guard = _fixture_files()
    base = _fixture_ledger(manuscript, lean, guard)
    base_md = _fixture_markdown(base)
    counts = {"negative": 0, "codes": set()}

    with tempfile.TemporaryDirectory() as root:
        lean_root = _write_fixture(root, base, base_md, manuscript=manuscript, lean=lean, guard=guard)

        # POSITIVE: the well-formed fixture passes, with and without --lean-root.
        res = evaluate(root, lean_root=lean_root)
        _expect(res["ok"], f"positive fixture should pass: {res['errors']}")
        _expect(res["stats"]["lean_quotes_checked"] == 24 + 8, res["stats"])
        _expect(res["stats"]["anchors_checked"] == 8, res["stats"])
        _expect(res["stats"]["papers_quotes_checked"] == 5, res["stats"])
        _expect(res["stats"]["external_quotes_unchecked"] == 5, res["stats"])
        res = evaluate(root)
        _expect(res["ok"] and res["lean_check"] == "NOT_RUN", res)

        def run_case(mutate, code: str, needle: str = "", md=None, readme: str = _FIX_README,
                     lean_text: list[str] | None = None, guard_text: list[str] | None = None,
                     ensure_ascii: bool = False) -> None:
            ledger = copy.deepcopy(base)
            mutate(ledger)
            text = md(_fixture_markdown(ledger)) if callable(md) else \
                (md if md is not None else _fixture_markdown(ledger))
            _write_fixture(root, ledger, text, readme=readme,
                           lean=lean_text if lean_text is not None else lean,
                           guard=guard_text if guard_text is not None else guard,
                           ensure_ascii=ensure_ascii)
            out = evaluate(root, lean_root=lean_root)
            _expect(not out["ok"], f"{code}/{needle}: negative fixture unexpectedly passed")
            _expect(any(e.startswith(f"[{code}]") and needle in e for e in out["errors"]),
                    f"expected a [{code}] error containing {needle!r}, got {out['errors'][:6]}")
            counts["negative"] += 1
            counts["codes"].add(code)

        def entry(ledger: dict, eid: str) -> dict:
            return next(e for e in ledger["entries"] if e["id"] == eid)

        def decl(ledger: dict, eid: str, i: int = 0) -> dict:
            return entry(ledger, eid)["lean_decls"][i]

        def move_f4_carrier_to_f7(L: dict) -> None:
            moved = entry(L, "F4")["lean_decls"].pop(1)
            entry(L, "F7")["lean_decls"].append(moved)

        def duplicate_carrier(L: dict) -> None:
            first, second = entry(L, "F4")["lean_decls"][:2]
            second.update(decl=first["decl"], statement=first["statement"], lean_ref=first["lean_ref"])

        # NEGATIVE fixtures: each one breaks one rule and expects that rule's message.
        # -- ids, pins, enums, fields
        run_case(lambda L: L["entries"].pop(), "locked-ids", "missing locked ids")
        run_case(lambda L: L["entries"].append(dict(copy.deepcopy(L["entries"][0]), id="F23", row="P-F23")),
                 "locked-ids", "outside the locked eight")
        run_case(lambda L: L["pins"]["lutar_lean"].update(sha="c7c0ba17"), "pin", "40-hex")
        run_case(lambda L: L["manuscript"].update(sha="9" * 40), "pin", "manuscript.sha")
        run_case(lambda L: entry(L, "F1").update(lutar_lean_sha="9" * 40), "pin", "lutar_lean_sha must equal")
        run_case(lambda L: L["pins"].update(lutar_lean="04f904e"), "pin", "must be an object")
        run_case(lambda L: entry(L, "F18").update(verdict="PROVEN"), "verdict", "PROVEN")
        run_case(lambda L: entry(L, "F18").update(severity="huge"), "field", "severity 'huge'")
        run_case(lambda L: entry(L, "F19").pop("proposed_wording"), "field", "missing 'proposed_wording'")
        run_case(lambda L: entry(L, "F1").update(manuscript_anchors=5), "field", "manuscript_anchors must be")
        run_case(lambda L: decl(L, "F4", 1).update(primary=True), "field", "exactly one primary")
        run_case(lambda L: decl(L, "F4", 1).update(primary="yes"), "field", "primary must be true or false")
        run_case(lambda L: decl(L, "F12").update(decl=5), "field", "decl must be a non-empty string")
        run_case(lambda L: entry(L, "F1").update(runtime_symbol=5), "field", "runtime_symbol must be null")
        run_case(lambda L: L["cross_cutting"].reverse(), "field", "in order")
        run_case(lambda L: L.update(normative=True), "normative", "normative")
        # -- carriers, axioms, kernel summary
        run_case(lambda L: decl(L, "F4").update(kernel_axioms=["funext"]), "axioms", "funext")
        run_case(lambda L: decl(L, "F4").update(kernel_axioms=["sorryAx"]), "axioms", "sorryAx")
        run_case(lambda L: decl(L, "F7").update(decl=CARRIER_NAMESPACE + "f7_fake"), "carrier",
                 "not one of the 24")
        run_case(move_f4_carrier_to_f7, "carrier", "does not belong to F7")
        run_case(duplicate_carrier, "carrier", "cited more than once")
        run_case(lambda L: L["kernel_axiom_evidence"]["result"].update(no_axiom=11), "kernel-summary",
                 "result.no_axiom")
        run_case(lambda L: L["kernel_axiom_evidence"].update(status="UNKNOWN"), "kernel-summary",
                 "UNKNOWN is never a pass")
        run_case(lambda L: L["kernel_axiom_evidence"].pop("input_sha256"), "kernel-summary", "input_sha256")
        # -- owner decisions
        run_case(lambda L: entry(L, "F11").update(owner_decisions=["D10"]), "decision", "D10")
        run_case(lambda L: L["owner_decisions"][2].update(status="MAYBE"), "decision", "status 'MAYBE'")
        # -- anchors and quotes
        run_case(lambda L: entry(L, "F1")["manuscript_anchors"][0].update(quote="Locked F1 is proven"),
                 "anchor", "not found anywhere")
        run_case(lambda L: entry(L, "F1")["manuscript_anchors"][0].update(line=3), "anchor", "found on line")
        run_case(lambda L: L["cross_cutting"][0]["evidence"][0].update(quote="evidence line nine"),
                 "papers-quote", "evidence line nine")
        run_case(lambda L: None, "lean-quote", "True := trivial",
                 lean_text=[ln.replace("True", "False") for ln in lean])
        run_case(lambda L: entry(L, "F12")["cross_refs"][0].update(quote="theorem made_up"), "lean-quote",
                 "made_up")
        # -- evidence routing and pins
        run_case(lambda L: L["cross_cutting"][2]["evidence"][0].update(repo="szl-holdings/szl_papers",
                                                                        quote="totally fabricated quote"),
                 "evidence", "not one of")
        run_case(lambda L: L["cross_cutting"][0]["evidence"][0].pop("sha"), "evidence", "40-hex 'sha'")
        run_case(lambda L: L["cross_cutting"][1]["evidence"][0].update(sha="9" * 40), "evidence",
                 "must cite pins.szl_papers.sha")
        run_case(lambda L: entry(L, "F7")["cross_refs"][0].update(sha="9" * 40), "evidence",
                 "must cite pins.lutar_lean.sha")
        run_case(lambda L: L["cross_cutting"][3]["evidence"][2].pop("note"), "evidence", "needs a note")
        run_case(lambda L: entry(L, "F22").update(cross_refs={"ref": "x"}), "evidence", "cross_refs must be a list")
        # -- --lean-root pin checks
        run_case(lambda L: None, "lean-pin", PROVED_FORMULAS_REL, lean_text=lean + ["-- drift"])
        run_case(lambda L: L["kernel_axiom_evidence"]["input_sha256"].update(
            {LOCKED_GUARD_REL: _text_sha256(guard[:-1])}), "lean-guard", "guards 23",
            guard_text=guard[:-1])
        # -- Markdown / JSON sync
        run_case(lambda L: None, "md-sync", "P-F12: expected exactly one",
                 md=lambda m: m.replace("### P-F12 ", "### P-F12x "))
        run_case(lambda L: None, "md-sync", "P-F1: manuscript quote",
                 md=lambda m: m.replace("`` Locked F1 is described ``", "`` Locked F1 ``"))
        run_case(lambda L: None, "md-sync", "P-F4: proposed_wording",
                 md=lambda m: m.replace("F4 [locked]: a fixture statement.", "F4 [locked]: reworded."))
        run_case(lambda L: None, "md-sync", "P-F7: gap",
                 md=lambda m: m.replace("gap: F7: none in the fixture.", "gap: No gap."))
        run_case(lambda L: None, "md-sync", "P-X2: evidence quote",
                 md=lambda m: _drop_in_section(m, "### P-X2 ", "`` evidence line two ``"))
        run_case(lambda L: None, "md-sync", "kernel axioms differ",
                 md=lambda m: m.replace("· kernel axioms: none", "· kernel axioms: `propext`", 1))
        run_case(lambda L: None, "md-sync", "P-F1: expected exactly one '### P-F1' section, found 2",
                 md=lambda m: m + "### P-F1 · MATCHES · F1 fixture\n")
        run_case(lambda L: None, "md-sync", "needs exactly one bullet, found 0",
                 md=lambda m: _drop_line(m, f"- `{CARRIER_NAMESPACE}f18_erasure_tolerance`"))
        run_case(lambda L: None, "md-sync", "needs exactly one bullet, found 2",
                 md=lambda m: _repeat_line(m, f"- `{CARRIER_NAMESPACE}f18_erasure_tolerance`"))
        run_case(lambda L: None, "md-sync", "primary marker",
                 md=lambda m: m.replace(" (primary)", "", 1))
        run_case(lambda L: None, "md-sync", "statement missing",
                 md=lambda m: m.replace("  theorem f12_kuramoto_additive : True", "  theorem f12_kuramoto_additive : False"))
        run_case(lambda L: None, "md-sync", "lean_ref",
                 md=lambda m: m.replace(f"`{PROVED_FORMULAS_REL}:1` ·", f"`{PROVED_FORMULAS_REL}:2` ·", 1))
        run_case(lambda L: None, "md-sync", "section lacks the line",
                 md=lambda m: m.replace("Verdict **MATCHES** · severity none", "Verdict **MATCHES** · severity major", 1))
        run_case(lambda L: None, "md-sync", "heading does not carry verdict",
                 md=lambda m: m.replace("### P-F18 · MATCHES", "### P-F18 · EXCEEDS"))
        run_case(lambda L: None, "md-sync", "summary table row",
                 md=lambda m: m.replace("| **MATCHES** | none |", "| **EXCEEDS** | major |", 1))
        run_case(lambda L: None, "md-sync", "owner decisions line",
                 md=lambda m: m.replace("**Owner decisions:** D1", "**Owner decisions:** D1, D7", 1))
        run_case(lambda L: None, "md-sync", "owner decision D3",
                 md=lambda m: m.replace("- **D3** (OPEN)", "- **D3** (TAKEN)"))
        run_case(lambda L: None, "md-sync", "kernel result line",
                 md=lambda m: m.replace("24 use no axiom", "11 use no axiom"))
        run_case(lambda L: None, "md-sync", "rerun_trigger", md=lambda m: m.replace("fixture trigger", "x"))
        run_case(lambda L: None, "md-sync", f"input_sha256 of {LOCKED_GUARD_REL}",
                 md=lambda m: m.replace(_text_sha256(guard), "0" * 64))
        run_case(lambda L: None, "md-sync", "pins.szl_forge.sha", md=lambda m: m.replace(_FIX_FORGE_PIN, "4" * 39))
        run_case(lambda L: entry(L, "F11").update(runtime_symbol="tools.fixture.symbol"), "md-sync",
                 "runtime_symbol", md=lambda m: m.replace(" · runtime `tools.fixture.symbol`", ""))
        run_case(lambda L: None, "readme", "must mention", readme="# Reviews\n")
        # -- overclaim rules (Markdown, raw JSON line and decoded JSON string)
        run_case(lambda L: None, "overclaim-B", LEDGER_MD_REL, md=base_md + "Conjecture 1 is now proven.\n")
        run_case(lambda L: None, "overclaim-A", LEDGER_MD_REL,
                 md=base_md + "Lambda is shown to be uniquely determined by A1-A5.\n")
        run_case(lambda L: None, "overclaim-C", LEDGER_MD_REL, md=base_md + "The receipt chain is tamper-proof.\n")
        run_case(lambda L: L.update(scope="Conjecture 1 is proven."), "overclaim-B", f"{LEDGER_REL}:")
        run_case(lambda L: L.update(scope="Λ is shown to be uniquely determined by A1-A5."), "overclaim-A",
                 f"{LEDGER_REL}#$.scope", ensure_ascii=True)

        # [load]: a missing ledger fails closed with a diagnostic, not a traceback.
        out = evaluate(root, ledger_path=os.path.join(root, "reviews", "missing.json"), lean_root=lean_root)
        _expect(not out["ok"] and any(e.startswith("[load]") for e in out["errors"]), out["errors"])
        counts["negative"] += 1
        counts["codes"].add("load")

    # Guard exemptions behave like the org guard (honest qualified lines pass).
    honest = [
        "Conjecture 1 is disproved as stated; the weaker-condition question remains open.",
        "Λ uniqueness is Conjecture 1; only conditional Theorem U is reported.",
        "The receipt chain is tamper-evident, not tamper-proof.",
        "Locked F18 is shard-count arithmetic, not a codec.",
    ]
    _expect(scan_overclaims("honest", honest) == [], scan_overclaims("honest", honest))
    _expect(scan_overclaims("soft-wrap", ["tamper-evident and", "tamper-proof is not claimed"]) == [],
            "rule C should consult the previous line")
    _expect(len(scan_overclaims("bad", ["Conjecture 1 is disproved as stated."])) == 1,
            "an unqualified 'disproved' line still trips rule B, exactly like the org guard")

    print(f"self-test OK ({counts['negative']} negative fixtures across {len(counts['codes'])} error codes)")
    return 0


def _drop_line(md: str, prefix: str) -> str:
    return "\n".join(ln for ln in md.split("\n") if not ln.startswith(prefix))


def _repeat_line(md: str, prefix: str) -> str:
    out = []
    for ln in md.split("\n"):
        out.append(ln)
        if ln.startswith(prefix):
            out.append(ln)
    return "\n".join(out)


def _drop_in_section(md: str, heading_prefix: str, needle: str) -> str:
    """Remove ``needle`` from the first section whose heading starts with ``heading_prefix``."""
    out, inside, done = [], False, False
    for ln in md.split("\n"):
        if ln.startswith("#"):
            inside = ln.startswith(heading_prefix)
        if inside and not done and needle in ln:
            ln = ln.replace(needle, "`` removed ``")
            done = True
        out.append(ln)
    return "\n".join(out)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo-path", default=None, help="szl-papers checkout (default: this script's repo)")
    ap.add_argument("--ledger", default=None, help="override the ledger JSON path")
    ap.add_argument("--lean-root", default=None, help="lutar-lean checkout at the pinned commit (optional)")
    ap.add_argument("--json", action="store_true", help="emit the machine-readable result")
    ap.add_argument("--self-test", action="store_true", help="run the fixtures only")
    args = ap.parse_args(argv)

    if args.self_test:
        return _self_test()

    repo_root = args.repo_path or os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    result = evaluate(repo_root, args.ledger, args.lean_root)

    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))
        return 0 if result["ok"] else 1

    s = result["stats"]
    v = result["verdicts"]
    print(f"review ledger: {os.path.relpath(result['ledger'], repo_root)}")
    print("  verdicts: " + " · ".join(f"{k} {v.get(k, 0)}" for k in VERDICTS))
    print(f"  manuscript anchors checked (exact line match): {s['anchors_checked']}")
    print(f"  szl-papers evidence quotes checked: {s['papers_quotes_checked']}")
    if result["lean_check"] == "RUN":
        print(f"  lutar-lean quotes checked against --lean-root: {s['lean_quotes_checked']} "
              "(plus kernel input sha256 and the LockedGuard carrier list)")
    else:
        print(f"  lutar-lean quotes: NOT_RUN ({s.get('lean_quotes_unchecked', 0)} quotes; "
              "pass --lean-root <lutar-lean checkout at the pin> to compare)")
    print(f"  szl-forge quotes not checked by this script: {s['external_quotes_unchecked']}")
    print(f"  overclaim scan (org guard rules A/B/C): {s['overclaim_lines_scanned']} lines")
    for note in result["notes"]:
        print(f"  note: {note}")
    for err in result["errors"]:
        print(f"  ERROR {err}")
    scope = "" if result["lean_check"] == "RUN" else " (lutar-lean quotes NOT_RUN)"
    print("VERDICT:", ("OK" + scope) if result["ok"] else "FAIL")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
