#!/usr/bin/env python3
"""Read-only consistency checker for the non-normative review ledgers in ``reviews/``.

The v26 locked-eight claim ledger (``reviews/v26-locked-eight-claim-ledger.json``
plus its Markdown rendering) compares what the v26 manuscript says about the
locked eight with the Lean declarations that carry them at a pinned lutar-lean
commit. This script checks that the ledger stays well-formed and anchored:

  * exactly the locked ids {F1, F4, F7, F11, F12, F18, F19, F22}, one row each;
  * every ``manuscript_anchors[].quote`` appears verbatim on its cited line of
    ``thesis/ouroboros/papers/v26/unified-gpd-thesis-v26.md`` (drift detector);
  * required fields, 40-hex commit pins, verdict / severity enums;
  * every theorem's ``kernel_axioms`` lies inside {propext, Classical.choice,
    Quot.sound}; the theorems cited are exactly the 24 carriers listed in
    lutar-lean ``tools/lean/LockedGuard.lean`` at the pin, and the recorded
    kernel summary matches the per-theorem data;
  * szl-papers evidence quotes appear in the cited line ranges of this checkout;
  * with ``--lean-root``, lutar-lean quotes and statements appear in the cited
    line ranges of a lutar-lean checkout at the pin (otherwise NOT_RUN);
  * the Markdown rendering carries every row id, verdict, primary declaration,
    manuscript quote, proposed wording and owner-decision id from the JSON;
  * no line of the ledger files trips the org overclaim guard's rules A and B
    (unqualified Lambda uniqueness / Conjecture 1 called proven) or rule C
    (absolute security / correctness phrases). The regexes are copied from
    szl-holdings/.github reusable-overclaim-guard.yml @ 464069d.

It is stdlib-only, makes no network call and writes nothing. A passing run means
the ledger is internally consistent and its quotes still match the pinned
sources; it does not re-run the Lean kernel and says nothing about whether the
manuscript or the Lean code is right.

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
REF_RE = re.compile(r"^(?P<path>[^:\s]+):(?P<start>\d+)(?:-(?P<end>\d+))?$")
LEAN_REF_RE = re.compile(r"^[A-Za-z0-9_./-]+\.lean:\d+(?:-\d+)?$")

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

def _collapse(text: str) -> str:
    return " ".join(text.split())


def _read_lines(path: str) -> list[str]:
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read().splitlines()


def _safe_join(root: str, rel: str) -> str | None:
    """Join ``rel`` under ``root``; None if it is absolute or escapes ``root``."""
    if not rel or os.path.isabs(rel) or rel.startswith(("/", "\\")):
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


def git_blob_sha1(path: str) -> str:
    """Git blob id of ``path`` with CRLF normalised to LF (core.autocrlf checkouts)."""
    with open(path, "rb") as fh:
        data = fh.read().replace(b"\r\n", b"\n")
    # Git object id, not a security use.
    return hashlib.sha1(b"blob %d\0" % len(data) + data, usedforsecurity=False).hexdigest()


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
    pins = ledger.get("pins") if isinstance(ledger.get("pins"), dict) else {}
    lean_pin = (pins.get("lutar_lean") or {}).get("sha")
    papers_pin = (pins.get("szl_papers") or {}).get("sha")
    if not lean_pin or not papers_pin:
        errors.append("[pin] pins.lutar_lean.sha and pins.szl_papers.sha are required")
    manuscript = ledger.get("manuscript") if isinstance(ledger.get("manuscript"), dict) else {}
    if papers_pin and manuscript.get("sha") != papers_pin:
        errors.append("[pin] manuscript.sha must equal pins.szl_papers.sha")
    for entry in ledger.get("entries") or []:
        if isinstance(entry, dict) and lean_pin and entry.get("lutar_lean_sha") != lean_pin:
            errors.append(f"[pin] {entry.get('id')}: lutar_lean_sha must equal pins.lutar_lean.sha")
    return errors


def check_locked_ids(ledger: dict) -> list[str]:
    errors = []
    ids = [e.get("id") for e in ledger.get("entries") or [] if isinstance(e, dict)]
    dupes = sorted({i for i in ids if ids.count(i) > 1}, key=str)
    if dupes:
        errors.append(f"[locked-ids] duplicate entry ids: {dupes}")
    missing = sorted(LOCKED_IDS - set(ids))
    extra = sorted({str(i) for i in ids} - LOCKED_IDS)
    if missing:
        errors.append(f"[locked-ids] missing locked ids: {missing}")
    if extra:
        errors.append(f"[locked-ids] ids outside the locked eight: {extra}")
    declared = ledger.get("locked_ids")
    if not isinstance(declared, list) or set(declared) != LOCKED_IDS or len(declared) != 8:
        errors.append("[locked-ids] top-level locked_ids must be exactly the locked eight")
    return errors


def _carrier_prefix(entry_id: str) -> str:
    return entry_id.lower() + "_"


def check_fields(entry: dict) -> list[str]:
    """Required fields, enums, declarations and axiom sets for one locked-id row."""
    if not isinstance(entry, dict):
        return ["[field] entry must be an object"]
    eid = entry.get("id", "<no-id>")
    errors = []
    for key in ENTRY_FIELDS:
        if key not in entry:
            errors.append(f"[field] {eid}: missing {key!r}")
    for key in ("title", "lean_summary", "manuscript_claim", "gap", "proposed_wording"):
        if key in entry and (not isinstance(entry[key], str) or not entry[key].strip()):
            errors.append(f"[field] {eid}: {key!r} must be a non-empty string")
    if isinstance(eid, str) and entry.get("row") != f"P-{eid}":
        errors.append(f"[field] {eid}: row must be 'P-{eid}'")
    if entry.get("verdict") not in VERDICTS:
        errors.append(f"[verdict] {eid}: verdict {entry.get('verdict')!r} not in {VERDICTS}")
    if entry.get("severity") not in SEVERITIES:
        errors.append(f"[field] {eid}: severity {entry.get('severity')!r} not in {SEVERITIES}")
    anchors = entry.get("manuscript_anchors")
    if not isinstance(anchors, list) or not anchors:
        errors.append(f"[field] {eid}: manuscript_anchors must be a non-empty list")
    decls = entry.get("lean_decls")
    if not isinstance(decls, list) or not decls:
        errors.append(f"[field] {eid}: lean_decls must be a non-empty list")
        return errors
    primaries = 0
    for d in decls:
        if not isinstance(d, dict):
            errors.append(f"[field] {eid}: lean_decls items must be objects")
            continue
        name = d.get("decl", "<no-decl>")
        for key in DECL_FIELDS:
            if key not in d:
                errors.append(f"[field] {eid}/{name}: missing {key!r}")
        if not isinstance(d.get("statement"), str) or not d.get("statement", "").strip():
            errors.append(f"[field] {eid}/{name}: statement must be a non-empty quoted string")
        if not (isinstance(d.get("lean_ref"), str) and LEAN_REF_RE.match(d["lean_ref"])):
            errors.append(f"[field] {eid}/{name}: lean_ref must look like path.lean:LINE[-LINE]")
        kind = d.get("kind")
        if kind not in DECL_KINDS:
            errors.append(f"[field] {eid}/{name}: kind {kind!r} not in {DECL_KINDS}")
        axioms = d.get("kernel_axioms")
        if kind == "theorem":
            if not isinstance(axioms, list) or not all(isinstance(a, str) for a in axioms):
                errors.append(f"[axioms] {eid}/{name}: theorem kernel_axioms must be a list of names")
            else:
                outside = sorted(set(axioms) - TRUST_BASE)
                if outside:
                    errors.append(
                        f"[axioms] {eid}/{name}: kernel_axioms {outside} outside "
                        f"{sorted(TRUST_BASE)}"
                    )
            short = name[len(CARRIER_NAMESPACE):] if isinstance(name, str) and \
                name.startswith(CARRIER_NAMESPACE) else None
            if short not in LOCKED_CARRIERS:
                errors.append(f"[carrier] {eid}/{name}: not one of the 24 LockedGuard carriers")
            elif isinstance(eid, str) and not short.startswith(_carrier_prefix(eid)):
                errors.append(f"[carrier] {eid}/{name}: carrier does not belong to {eid}")
        elif axioms is not None and not (
            isinstance(axioms, list) and set(axioms) <= TRUST_BASE
        ):
            errors.append(f"[axioms] {eid}/{name}: non-theorem kernel_axioms must be null or in the trust base")
        if d.get("primary") is True:
            primaries += 1
            if kind != "theorem":
                errors.append(f"[field] {eid}/{name}: the primary declaration must be a theorem")
    if primaries != 1:
        errors.append(f"[field] {eid}: exactly one primary lean_decl required, found {primaries}")
    return errors


def check_carrier_coverage(ledger: dict) -> list[str]:
    seen: list[str] = []
    for entry in ledger.get("entries") or []:
        for d in (entry.get("lean_decls") or []) if isinstance(entry, dict) else []:
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
    if set(ev.get("trust_base") or []) != TRUST_BASE:
        errors.append("[kernel-summary] trust_base must be {propext, Classical.choice, Quot.sound}")
    for key in ("method", "environment", "date"):
        if not isinstance(ev.get(key), str) or not ev.get(key).strip():
            errors.append(f"[kernel-summary] {key!r} missing")
    sets = []
    for entry in ledger.get("entries") or []:
        for d in (entry.get("lean_decls") or []) if isinstance(entry, dict) else []:
            if isinstance(d, dict) and d.get("kind") == "theorem" and isinstance(d.get("kernel_axioms"), list):
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
    recorded = ev.get("result") if isinstance(ev.get("result"), dict) else {}
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
    decisions = ledger.get("owner_decisions") or []
    ids = [d.get("id") for d in decisions if isinstance(d, dict)]
    if sorted(ids, key=str) != sorted(DECISION_IDS) or len(ids) != len(set(ids)):
        errors.append(f"[decision] owner_decisions must be exactly {list(DECISION_IDS)}, got {ids}")
    for d in decisions:
        if not isinstance(d, dict):
            continue
        if d.get("status") not in DECISION_STATUSES:
            errors.append(f"[decision] {d.get('id')}: status {d.get('status')!r} not in {DECISION_STATUSES}")
        if not isinstance(d.get("question"), str) or not d["question"].strip():
            errors.append(f"[decision] {d.get('id')}: question missing")
    rows = list(ledger.get("entries") or []) + list(ledger.get("cross_cutting") or [])
    for row in rows:
        if not isinstance(row, dict):
            continue
        refs = row.get("owner_decisions")
        if not isinstance(refs, list):
            errors.append(f"[decision] {row.get('id')}: owner_decisions must be a list")
            continue
        unknown = sorted(set(map(str, refs)) - set(DECISION_IDS))
        if unknown:
            errors.append(f"[decision] {row.get('id')}: unknown owner decision ids {unknown}")
    return errors


def check_cross_cutting(row: dict) -> list[str]:
    if not isinstance(row, dict):
        return ["[field] cross_cutting rows must be objects"]
    rid = row.get("id", "<no-id>")
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
    for item in row.get("evidence") or []:
        if not isinstance(item, dict) or not isinstance(item.get("repo"), str):
            errors.append(f"[field] {rid}: evidence items need a repo")
            continue
        if item.get("ref") is None:
            if not isinstance(item.get("note"), str) or not item["note"].strip():
                errors.append(f"[field] {rid}: evidence without a ref needs a note")
        elif _parse_ref(item.get("ref")) is None or not isinstance(item.get("quote"), str) \
                or not item["quote"].strip():
            errors.append(f"[field] {rid}: evidence ref {item.get('ref')!r} needs PATH:LINE[-LINE] and a quote")
    return errors


def check_cross_cutting_ids(ledger: dict) -> list[str]:
    ids = [r.get("id") for r in ledger.get("cross_cutting") or [] if isinstance(r, dict)]
    if ids != list(CROSS_CUTTING_IDS):
        return [f"[field] cross_cutting ids must be {list(CROSS_CUTTING_IDS)} in order, got {ids}"]
    return []


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


def check_markdown_sync(ledger: dict, md_text: str) -> list[str]:
    """The Markdown rendering must carry the JSON's ids, verdicts, quotes and wording."""
    errors = []
    headings = [ln for ln in md_text.splitlines() if ln.startswith("### ")]
    rows = list(ledger.get("entries") or []) + list(ledger.get("cross_cutting") or [])
    for row in rows:
        if not isinstance(row, dict):
            continue
        rid = row.get("row") or row.get("id")
        verdict = row.get("verdict")
        own = re.compile(r"^### " + re.escape(str(rid)) + r"(?![\w-])")
        if not any(own.match(h) and (verdict is None or verdict in h) for h in headings):
            errors.append(f"[md-sync] no '### ' heading carries {rid} with verdict {verdict}")
        for anchor in row.get("manuscript_anchors") or []:
            quote = anchor.get("quote") if isinstance(anchor, dict) else None
            if isinstance(quote, str) and quote not in md_text:
                errors.append(f"[md-sync] {rid}: manuscript quote missing from Markdown: {quote[:60]!r}")
        wording = row.get("proposed_wording")
        if isinstance(wording, str) and wording not in md_text:
            errors.append(f"[md-sync] {rid}: proposed_wording missing from Markdown")
        for d in row.get("lean_decls") or []:
            if isinstance(d, dict) and d.get("primary") and isinstance(d.get("decl"), str) \
                    and d["decl"] not in md_text:
                errors.append(f"[md-sync] {rid}: primary declaration {d['decl']} missing from Markdown")
    for d in ledger.get("owner_decisions") or []:
        if isinstance(d, dict) and f"**{d.get('id')}**" not in md_text:
            errors.append(f"[md-sync] owner decision {d.get('id')} missing from Markdown")
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
        return result  # fail closed before walking a malformed structure
    errors += check_pins(ledger)
    errors += check_locked_ids(ledger)
    for entry in ledger.get("entries") or []:
        errors += check_fields(entry)
    errors += check_carrier_coverage(ledger)
    errors += check_kernel_summary(ledger)
    errors += check_cross_cutting_ids(ledger)
    for row in ledger.get("cross_cutting") or []:
        errors += check_cross_cutting(row)
    errors += check_owner_decisions(ledger)

    for entry in ledger.get("entries") or []:
        if isinstance(entry, dict):
            v = entry.get("verdict")
            result["verdicts"][v] = result["verdicts"].get(v, 0) + 1

    # Manuscript anchors (exact line match) + blob provenance note.
    manuscript_path = os.path.join(repo_root, *MANUSCRIPT_REL.split("/"))
    try:
        manuscript_lines = _read_lines(manuscript_path)
    except OSError as exc:
        errors.append(f"[anchor] cannot read manuscript {MANUSCRIPT_REL}: {exc}")
        manuscript_lines = None
    rows = [r for r in list(ledger.get("entries") or []) + list(ledger.get("cross_cutting") or [])
            if isinstance(r, dict)]
    if manuscript_lines is not None:
        for row in rows:
            rid = row.get("row") or row.get("id")
            for k, anchor in enumerate(row.get("manuscript_anchors") or []):
                errors += check_anchor(manuscript_lines, anchor, f"{rid}.manuscript_anchors[{k}]")
                stats["anchors_checked"] += 1
        pinned_blob = (ledger.get("manuscript") or {}).get("blob_sha")
        actual_blob = git_blob_sha1(manuscript_path)
        if actual_blob == pinned_blob:
            notes.append(f"manuscript blob matches the pinned blob {actual_blob[:12]}")
        else:
            notes.append(
                f"manuscript blob {actual_blob[:12]} differs from the pinned blob "
                f"{str(pinned_blob)[:12]}; anchors above are still checked line by line"
            )

    # Evidence and Lean quotes.
    lean_pin = ((ledger.get("pins") or {}).get("lutar_lean") or {}).get("sha")
    lean_items = []
    for row in rows:
        rid = row.get("row") or row.get("id")
        for d in row.get("lean_decls") or []:
            if isinstance(d, dict):
                lean_items.append((f"{rid}/{d.get('decl')}", d))
        for key in ("evidence", "cross_refs"):
            for k, item in enumerate(row.get(key) or []):
                if not isinstance(item, dict) or item.get("ref") is None:
                    continue
                label = f"{rid}.{key}[{k}]"
                if item.get("repo") == SZL_PAPERS_REPO:
                    errors += check_ranged_quote(repo_root, item, label, "papers-quote")
                    stats["papers_quotes_checked"] += 1
                elif item.get("repo") == LUTAR_LEAN_REPO and item.get("sha") == lean_pin:
                    lean_items.append((label, item))
                else:
                    stats["external_quotes_unchecked"] += 1
    if lean_root:
        if not os.path.isdir(lean_root):
            errors.append(f"[lean-quote] --lean-root {lean_root} is not a directory")
        else:
            for label, item in lean_items:
                errors += check_ranged_quote(lean_root, item, label, "lean-quote")
                stats["lean_quotes_checked"] += 1
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
_FIX_LEAN_FILE = "Lutar/Puriq/Formulas/ProvedFormulas.lean"


def _expect(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _fixture_files() -> tuple[list[str], list[str]]:
    manuscript = ["# Fixture manuscript"] + [f"Locked {i} is described here." for i in sorted(LOCKED_IDS)]
    lean = [f"theorem {name} : True := trivial" for name in sorted(LOCKED_CARRIERS)]
    return manuscript, lean


def _fixture_ledger(manuscript: list[str], lean: list[str]) -> dict:
    entries = []
    for eid in sorted(LOCKED_IDS):
        decls = []
        for idx, text in enumerate(lean):
            short = text.split()[1]
            if short.startswith(_carrier_prefix(eid)):
                decls.append({
                    "decl": CARRIER_NAMESPACE + short, "kind": "theorem",
                    "primary": not decls, "lean_ref": f"{_FIX_LEAN_FILE}:{idx + 1}",
                    "statement": text, "kernel_axioms": [],
                })
        line = manuscript.index(f"Locked {eid} is described here.") + 1
        entries.append({
            "id": eid, "row": f"P-{eid}", "title": f"{eid} fixture",
            "lutar_lean_sha": _FIX_LEAN_PIN, "lean_decls": decls,
            "lean_summary": "True.", "manuscript_claim": "A fixture claim.",
            "manuscript_anchors": [{"section": "§1", "line": line, "quote": f"Locked {eid} is described"}],
            "verdict": "MATCHES", "severity": "none", "gap": "None in the fixture.",
            "proposed_wording": f"{eid} [locked]: a fixture statement.",
            "owner_decisions": ["D1"], "runtime_symbol": None,
        })
    cross = []
    for rid in CROSS_CUTTING_IDS:
        cross.append({
            "id": rid, "title": f"{rid} fixture", "surface": "manuscript",
            "verdict": None if rid == "P-X5" else "MATCHES",
            "severity": None if rid == "P-X5" else "none",
            "finding": "A fixture finding.", "manuscript_anchors": [],
            "evidence": [{"repo": SZL_PAPERS_REPO, "sha": _FIX_PAPERS_PIN,
                          "ref": "NOTES.md:2", "quote": "evidence line two"}],
            "proposed_wording": f"{rid} fixture wording.", "owner_decisions": ["D2"],
        })
    return {
        "schema": SCHEMA, "ledger_id": "fixture", "title": "Fixture ledger",
        "normative": False, "review_status": "DRAFT_FOR_OWNER_REVIEW",
        "date": "2026-10-06", "scope": "Self-test fixture.",
        "manuscript": {"repo": SZL_PAPERS_REPO, "path": MANUSCRIPT_REL,
                       "sha": _FIX_PAPERS_PIN, "blob_sha": "3" * 40},
        "pins": {"szl_papers": {"repo": SZL_PAPERS_REPO, "sha": _FIX_PAPERS_PIN},
                 "lutar_lean": {"repo": LUTAR_LEAN_REPO, "sha": _FIX_LEAN_PIN}},
        "locked_ids": sorted(LOCKED_IDS),
        "kernel_axiom_evidence": {
            "status": "MEASURED", "trust_base": sorted(TRUST_BASE),
            "method": "fixture", "environment": "fixture", "date": "2026-10-06",
            "result": {"carriers": 24, "allowed_true": 24, "allowed_false": 0,
                       "no_axiom": 24, "propext_only": 0, "propext_and_quot_sound": 0,
                       "uses_classical_choice": 0},
        },
        "entries": entries, "cross_cutting": cross,
        "owner_decisions": [{"id": d, "status": "TAKEN" if d == "D2" else "OPEN",
                             "question": f"Fixture question {d}?"} for d in DECISION_IDS],
    }


def _fixture_markdown(ledger: dict) -> str:
    out = ["# Fixture ledger", ""]
    for row in ledger["entries"] + ledger["cross_cutting"]:
        rid = row.get("row") or row["id"]
        out.append(f"### {rid} · {row.get('verdict') or 'INVENTORY'}")
        for a in row["manuscript_anchors"]:
            out.append(f"- `` {a['quote']} ``")
        for d in row.get("lean_decls") or []:
            if d.get("primary"):
                out.append(f"- `{d['decl']}`")
        out.append(f"Proposed: {row.get('proposed_wording', '')}")
        out.append("")
    out += [f"- **{d['id']}** {d['question']}" for d in ledger["owner_decisions"]]
    return "\n".join(out) + "\n"


_FIX_README = (
    "# Reviews\n\nReviews here are non-normative.\n"
    "- v26-locked-eight-claim-ledger.md\n- v26-locked-eight-claim-ledger.json\n"
)


def _write_fixture(root: str, ledger: dict, md: str, readme: str = _FIX_README,
                   manuscript: list[str] | None = None, lean: list[str] | None = None) -> str:
    def write(rel: str, text: str) -> None:
        path = os.path.join(root, *rel.split("/"))
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text)

    write(LEDGER_REL, json.dumps(ledger, ensure_ascii=False, indent=2) + "\n")
    write(LEDGER_MD_REL, md)
    write(README_REL, readme)
    write("NOTES.md", "evidence line one\nevidence line two\n")
    if manuscript is not None:
        write(MANUSCRIPT_REL, "\n".join(manuscript) + "\n")
    lean_root = os.path.join(root, "_lean")
    if lean is not None:
        path = os.path.join(lean_root, *_FIX_LEAN_FILE.split("/"))
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("\n".join(lean) + "\n")
    return lean_root


def _self_test() -> int:
    manuscript, lean = _fixture_files()
    base = _fixture_ledger(manuscript, lean)
    base_md = _fixture_markdown(base)

    with tempfile.TemporaryDirectory() as root:
        lean_root = _write_fixture(root, base, base_md, manuscript=manuscript, lean=lean)

        # POSITIVE: the well-formed fixture passes, with and without --lean-root.
        res = evaluate(root, lean_root=lean_root)
        _expect(res["ok"], f"positive fixture should pass: {res['errors']}")
        _expect(res["stats"]["lean_quotes_checked"] == 24, res["stats"])
        _expect(res["stats"]["anchors_checked"] == 8, res["stats"])
        res = evaluate(root)
        _expect(res["ok"] and res["lean_check"] == "NOT_RUN", res)

        def run_case(mutate, code: str, md: str | None = None, readme: str = _FIX_README,
                     lean_text: list[str] | None = None) -> None:
            ledger = copy.deepcopy(base)
            mutate(ledger)
            _write_fixture(root, ledger, md if md is not None else _fixture_markdown(ledger),
                           readme=readme, lean=lean_text if lean_text is not None else lean)
            out = evaluate(root, lean_root=lean_root)
            _expect(not out["ok"], f"{code}: negative fixture unexpectedly passed")
            _expect(any(e.startswith(f"[{code}]") for e in out["errors"]),
                    f"expected a [{code}] error, got {out['errors'][:5]}")

        def entry(ledger: dict, eid: str) -> dict:
            return next(e for e in ledger["entries"] if e["id"] == eid)

        # NEGATIVE fixtures, one failure mode each.
        run_case(lambda L: L["entries"].pop(), "locked-ids")                       # F7 dropped
        run_case(lambda L: L["entries"].append(dict(copy.deepcopy(L["entries"][0]), id="F23", row="P-F23")),
                 "locked-ids")
        run_case(lambda L: entry(L, "F1")["manuscript_anchors"][0].update(quote="Locked F1 is proven"),
                 "anchor")                                                          # quote drift
        run_case(lambda L: entry(L, "F1")["manuscript_anchors"][0].update(line=3), "anchor")
        run_case(lambda L: L["pins"]["lutar_lean"].update(sha="c7c0ba17"), "pin")   # short sha
        run_case(lambda L: entry(L, "F4")["lean_decls"][0].update(kernel_axioms=["funext"]), "axioms")
        run_case(lambda L: entry(L, "F4")["lean_decls"][0].update(kernel_axioms=["sorryAx"]), "axioms")
        run_case(lambda L: entry(L, "F18").update(verdict="PROVEN"), "verdict")
        run_case(lambda L: entry(L, "F19").pop("proposed_wording"), "field")
        run_case(lambda L: L.update(normative=True), "normative")
        run_case(lambda L: entry(L, "F7")["lean_decls"][0].update(decl=CARRIER_NAMESPACE + "f7_fake"),
                 "carrier")
        run_case(lambda L: L["kernel_axiom_evidence"]["result"].update(no_axiom=11), "kernel-summary")
        run_case(lambda L: L["kernel_axiom_evidence"].update(status="UNKNOWN"), "kernel-summary")
        run_case(lambda L: entry(L, "F11").update(owner_decisions=["D10"]), "decision")
        run_case(lambda L: L["cross_cutting"][0]["evidence"][0].update(quote="evidence line nine"),
                 "papers-quote")
        run_case(lambda L: None, "lean-quote",
                 lean_text=[ln.replace("True", "False") for ln in lean])
        run_case(lambda L: None, "md-sync", md=base_md.replace("P-F12", "P-F12x"))
        run_case(lambda L: None, "readme", readme="# Reviews\n")
        run_case(lambda L: None, "overclaim-B", md=base_md + "Conjecture 1 is now proven.\n")
        run_case(lambda L: None, "overclaim-A",
                 md=base_md + "Lambda is shown to be uniquely determined by A1-A5.\n")
        run_case(lambda L: None, "overclaim-C", md=base_md + "The receipt chain is tamper-proof.\n")
        run_case(lambda L: entry(L, "F12").update(gap="Conjecture 1 is proven."), "overclaim-B")

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

    print("self-test OK")
    return 0


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
        print(f"  lutar-lean quotes checked against --lean-root: {s['lean_quotes_checked']}")
    else:
        print(f"  lutar-lean quotes: NOT_RUN ({s.get('lean_quotes_unchecked', 0)} quotes; "
              "pass --lean-root <lutar-lean checkout at the pin> to compare)")
    print(f"  quotes from other repositories not checked by this script: {s['external_quotes_unchecked']}")
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
