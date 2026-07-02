#!/usr/bin/env python3
"""Served-claim ↔ real-Lean-corpus backing guard for the Ouroboros claim corpus.

This is the szl-papers mirror of lutar-lean's ``check_proven_formulas.py`` (the
SOURCE-side registry guard) and a11oy's served-formula guard. Where those verify
Lean *declarations*, this verifies the *published TeX claims* harvested into
``thesis/ouroboros/corpus-v18/claims_v18_extracted.json`` against the in-repo
honest index of what is genuinely backed.

The honest contract, per the szl-holdings doctrine (no-network, stdlib only):

  * A claim whose title/statement asserts a PROVED / kernel-verified / machine-
    checked status must be BACKED: it must reference a concrete Lean artifact
    (a ``.lean`` file or a named Lean declaration) OR be covered by the in-repo
    allowlist built from ``thesis/EXPERIMENTAL_LEAN_THEOREMS.md`` + the explicit
    locked-8 + the Theorem U manifest. A proved-status claim with nothing behind
    it is an *unbacked served claim* — caught here, reported, never served as
    proven.
  * Λ-aggregator uniqueness stays **Conjecture 1 (OPEN)** — machine-checked
    false as stated, never a proved theorem. The governance-safe form is
    **Theorem U** (conditional, axiom-free: unique modulo ``≈Λ`` under the
    Identifiability Assumptions). A claim that presents UNCONDITIONAL Λ / the
    aggregator as *uniquely proved* without that conditional qualifier is an
    overclaim and is caught here.
  * Claims honestly labelled conjecture / conditional / pending / experimental
    are reported as such and are never a hard failure.

Nothing here asserts "the model is correct" — a resolved reference is *evidence*
that the named Lean artifact is claimed to exist, not a re-run of the kernel.

Usage:
    # Human summary (exit 1 on any unbacked / overclaim).
    python3 scripts/check_claim_backing.py --repo-path .

    # Machine-readable verdict.
    python3 scripts/check_claim_backing.py --repo-path . --json

    # Self-test the checker against positive + negative fixtures (no repo scan).
    python3 scripts/check_claim_backing.py --self-test
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys

# ---------------------------------------------------------------------------
# In-repo backing manifest (source-of-truth allowlist seed)
# ---------------------------------------------------------------------------

# The locked-proven set is EXACTLY these eight formula IDs, pinned at lutar-lean
# c7c0ba17. This mirrors thesis/EXPERIMENTAL_LEAN_THEOREMS.md ("locked-8").
LOCKED_PROVEN_IDS = {"F1", "F4", "F7", "F11", "F12", "F18", "F19", "F22"}

# Named Lean declarations the honest in-repo index records as genuinely backed.
# Theorem U is the governance-safe CONDITIONAL uniqueness result (axiom-free);
# the unconditional aggregator-uniqueness statement stays Conjecture 1 (OPEN),
# never a proved theorem.
MANIFEST_LEAN_NAMES = {
    "lambda_unique_of_separable",   # Theorem U (conditional uniqueness)
    "locked_count_eight",
    "f4_khipu_dag_acyclic_preserved",
    "f7_chaski_fifo_order",
    "f22_khipu_emit_monotone",
    "khipu_quorum_safety_conditional",
}

# Tokens that assert a PROVED / verified status.
PROVED_TOKENS = (
    "kernel-verified", "kernel verified", "machine-checked", "machine checked",
    "machine-checke",  # tolerate the corpus's occasional truncation
    "0 sorry", "0\\,sorry", "sorry-free", "no sorry", "qed", "\\qed",
    "proven", "proved",
)

# PRECISE qualifiers that make a Λ-UNIQUENESS assertion honest (Theorem U
# conditional / Conjecture 1 OPEN / modulo ≈Λ …). Deliberately narrow: broad
# words like "normalisation" or "the open problem … is resolved" must NOT count
# as conditioning the uniqueness claim, or the guard would miss a real overclaim.
# (Text is tilde-normalised before matching, so "theorem~u" == "theorem u".)
UNIQ_SAFE = (
    "conjecture 1", "conjecture 2", "conjecture", "theorem u", "theoremu",
    "u\u2081", "u\u2082", "conditional", "modulo", "\u2248\u039b",
    "\\approx_\\lambda", "\\approx_{\\lambda}", "identifiab", "separable",
    "not a theorem", "not a proved theorem", "machine-checked false",
    "machine checked false", "stays open", "remains open", "open conjecture",
)

# Honest hedges that mark a claim as conditional / not-yet-proved (used to keep
# an honestly hedged claim from being mis-flagged as an unbacked served claim,
# and to label genuinely conditional / conjectural claims).
HEDGE_TOKENS = (
    "conjecture", "conditional", "theorem u", "theoremu", "modulo", "pending",
    "identifiab", "separable", "roadmap", "experimental", "\u2248\u039b",
)

# Lambda-uniqueness assertion patterns (the live overclaim risk).
_LAMBDA = r"(?:\\lambda|lambda|\u039b|\u03bb)"
UNIQUENESS_PATTERNS = (
    re.compile(r"unique\s+aggregator", re.IGNORECASE),
    re.compile(r"uniquely\s+determined", re.IGNORECASE),
    re.compile(r"uniqueness\s+theorem", re.IGNORECASE),
    re.compile(r"unique[^.]{0,80}aggregator", re.IGNORECASE),
    re.compile(r"aggregator[^.]{0,80}uniqu", re.IGNORECASE),
    re.compile(_LAMBDA + r"[^.]{0,60}uniqu", re.IGNORECASE),
    re.compile(r"uniqu[^.]{0,60}" + _LAMBDA, re.IGNORECASE),
)

# A concrete Lean-artifact reference: a .lean file OR a named declaration.
LEAN_FILE_RE = re.compile(r"[A-Za-z0-9_/]+\.lean", re.IGNORECASE)
LEAN_DECL_IN_TEXTT_RE = re.compile(
    r"\\texttt\{[^}]*?(?:theorem|lemma|def)\s+[^}]+\}", re.IGNORECASE
)
LEAN_IDENT_IN_TEXTT_RE = re.compile(r"\\texttt\{[^}]*\\_[^}]*\}")


# ---------------------------------------------------------------------------
# Tolerant corpus loader (the JSON is a documented PARTIAL harvest)
# ---------------------------------------------------------------------------

def load_claims(path: str) -> tuple[list[dict], bool]:
    """Load the claim list, tolerating a truncated (partial-harvest) tail.

    Returns ``(claims, truncated)``. If the file is valid JSON the whole array
    is returned with ``truncated=False``; if it is a documented partial harvest
    (unterminated tail) every COMPLETE leading object is returned with
    ``truncated=True``. We never fabricate the missing tail.
    """
    with open(path, "r", encoding="utf-8") as fh:
        raw = fh.read()
    try:
        data = json.loads(raw)
        if isinstance(data, list):
            return data, False
        return [data], False
    except json.JSONDecodeError:
        pass
    # Tolerant salvage: raw_decode one complete object at a time.
    dec = json.JSONDecoder()
    start = raw.find("[")
    if start < 0:
        return [], True
    i = start + 1
    n = len(raw)
    claims: list[dict] = []
    while i < n:
        while i < n and raw[i] in " \t\r\n,":
            i += 1
        if i >= n or raw[i] == "]":
            break
        try:
            obj, end = dec.raw_decode(raw, i)
        except json.JSONDecodeError:
            break
        if isinstance(obj, dict):
            claims.append(obj)
        i = end
    return claims, True


# ---------------------------------------------------------------------------
# Allowlist (built from the in-repo honesty index)
# ---------------------------------------------------------------------------

def build_allowlist(repo_root: str) -> dict:
    """Assemble the genuinely-backed identifier allowlist from in-repo sources.

    Seeds from the explicit locked-8 + Theorem U manifest, then augments with
    identifiers parsed out of ``thesis/EXPERIMENTAL_LEAN_THEOREMS.md`` and
    ``PAPERS_INDEX.md`` (Lean file basenames + named declarations). No network,
    no new deps.
    """
    lean_names: set[str] = set(MANIFEST_LEAN_NAMES)
    lean_files: set[str] = set()
    formula_ids: set[str] = set(LOCKED_PROVEN_IDS)

    for rel in ("thesis/EXPERIMENTAL_LEAN_THEOREMS.md", "PAPERS_INDEX.md"):
        p = os.path.join(repo_root, rel)
        if not os.path.isfile(p):
            continue
        with open(p, "r", encoding="utf-8") as fh:
            text = fh.read()
        for m in LEAN_FILE_RE.finditer(text):
            lean_files.add(os.path.basename(m.group(0)))
        # Named Lean declarations (snake_case idents with an underscore) in
        # backticks or inline code fences.
        for tok in re.findall(r"`([A-Za-z][A-Za-z0-9_']*_[A-Za-z0-9_']*)`", text):
            lean_names.add(tok)
        for tok in re.findall(r"\b(f\d+_[A-Za-z0-9_]+)\b", text):
            lean_names.add(tok)
        for tok in re.findall(r"\b(F\d{1,2})\b", text):
            if tok in LOCKED_PROVEN_IDS:
                formula_ids.add(tok)

    return {
        "lean_names": lean_names,
        "lean_files": lean_files,
        "formula_ids": formula_ids,
    }


def references_allowlist(text: str, allowlist: dict) -> bool:
    """True if the claim text names an allowlisted Lean file / decl / formula."""
    for fn in allowlist["lean_files"]:
        if fn and fn in text:
            return True
    for name in allowlist["lean_names"]:
        if name and re.search(r"(?<![A-Za-z0-9_])" + re.escape(name) + r"(?![A-Za-z0-9_])", text):
            return True
    return False


# ---------------------------------------------------------------------------
# Per-claim classification
# ---------------------------------------------------------------------------

def _has_any(text_low: str, tokens) -> bool:
    return any(t in text_low for t in tokens)


def has_lean_reference(text: str) -> bool:
    return bool(
        LEAN_FILE_RE.search(text)
        or LEAN_DECL_IN_TEXTT_RE.search(text)
        or LEAN_IDENT_IN_TEXTT_RE.search(text)
    )


def mentions_lambda_uniqueness(text: str) -> bool:
    return any(p.search(text) for p in UNIQUENESS_PATTERNS)


def _normalise(text: str) -> str:
    """Lower-case and treat LaTeX spacing (``~``) as a space for token matching."""
    low = text.lower().replace("~", " ")
    return re.sub(r"\s+", " ", low)


def classify(claim: dict, allowlist: dict) -> dict:
    """Return the honest verdict for one claim."""
    label = claim.get("label", "<no-label>")
    title = claim.get("title", "") or ""
    statement = claim.get("statement", "") or ""
    text = f"{title} {statement}"
    text_norm = _normalise(text)

    asserts_proved = _has_any(text_norm, PROVED_TOKENS)
    uniq_safe = _has_any(text_norm, UNIQ_SAFE)
    hedge = _has_any(text_norm, HEDGE_TOKENS)
    lean_ref = has_lean_reference(text)
    allow = references_allowlist(text, allowlist)
    uniq = mentions_lambda_uniqueness(text)

    # 1) UNCONDITIONAL Λ-aggregator uniqueness presented as proved → overclaim.
    #    The honest form is Theorem U (conditional); unconditional Λ-uniqueness
    #    stays Conjecture 1 (OPEN) and is never a proved theorem.
    if uniq and asserts_proved and not uniq_safe:
        status = "unconditional-overclaim"
    # 1b) A uniqueness claim carrying the Theorem U / Conjecture-1 qualifier is
    #     an honestly conditional result.
    elif uniq and uniq_safe:
        status = "conditional"
    # 2) A proved-status claim with a resolvable Lean/allowlist backing → verified.
    elif asserts_proved and (lean_ref or allow):
        status = "verified"
    # 3) A proved-status claim backed only by an honest hedge (e.g. "kernel-
    #    verified conditional on A15") → conditional, not unbacked.
    elif asserts_proved and hedge:
        status = "conditional"
    # 4) A proved-status claim with NOTHING behind it → unbacked served claim.
    elif asserts_proved:
        status = "unbacked"
    # 5) Not proved, but honestly hedged as a conjecture / pending result.
    elif hedge:
        status = "conditional"
    # 6) No strong proved-status assertion → descriptive (not a hard claim).
    else:
        status = "descriptive"

    return {
        "label": label,
        "env": claim.get("env", ""),
        "asserts_proved": asserts_proved,
        "lean_reference": lean_ref,
        "allowlisted": allow,
        "hedge_qualifier": hedge,
        "uniqueness_qualifier": uniq_safe,
        "lambda_uniqueness": uniq,
        "status": status,
    }


# ---------------------------------------------------------------------------
# Evaluate the whole corpus
# ---------------------------------------------------------------------------

def evaluate(repo_root: str, claims_path: str | None = None) -> dict:
    if claims_path is None:
        claims_path = os.path.join(
            repo_root, "thesis", "ouroboros", "corpus-v18",
            "claims_v18_extracted.json",
        )
    claims, truncated = load_claims(claims_path)
    allowlist = build_allowlist(repo_root)

    registry = [classify(c, allowlist) for c in claims]
    counts: dict[str, int] = {}
    for r in registry:
        counts[r["status"]] = counts.get(r["status"], 0) + 1

    unbacked = [r for r in registry if r["status"] == "unbacked"]
    overclaims = [r for r in registry if r["status"] == "unconditional-overclaim"]

    return {
        "claims_path": claims_path,
        "truncated_partial_harvest": truncated,
        "n_claims_scanned": len(claims),
        "allowlist": {
            "lean_names": sorted(allowlist["lean_names"]),
            "lean_files": sorted(allowlist["lean_files"]),
            "formula_ids": sorted(allowlist["formula_ids"]),
        },
        "registry": registry,
        "counts": counts,
        "unbacked": unbacked,
        "unconditional_overclaims": overclaims,
        "ok": not unbacked and not overclaims,
    }


# ---------------------------------------------------------------------------
# Self-test (positive + negative fixtures — trust the checker first)
# ---------------------------------------------------------------------------

def _self_test() -> int:
    allowlist = {
        "lean_names": {"lambda_unique_of_separable", "Lambda_le_max"},
        "lean_files": {"Bound.lean", "TheoremU.lean"},
        "formula_ids": set(LOCKED_PROVEN_IDS),
    }

    # POSITIVE (a): a legit CONDITIONAL uniqueness claim (Theorem U) passes.
    pos_conditional = {
        "env": "theorem", "label": "thm:pos-cond",
        "title": "Conditional aggregator uniqueness (Theorem U)",
        "statement": (
            "Theorem U (conditional, axiom-free): the aggregator is unique "
            "modulo the equivalence under the Identifiability Assumptions; "
            "\\texttt{Lutar/Uniqueness/TheoremU.lean} "
            "(\\texttt{lambda\\_unique\\_of\\_separable}). "
            "Unconditional uniqueness stays Conjecture 1 (OPEN, never a proved "
            "theorem). Status: kernel-verified conditional."
        ),
    }
    v = classify(pos_conditional, allowlist)
    assert v["status"] == "conditional", v

    # POSITIVE (b): a backed bound theorem (real .lean + named decl) verifies.
    pos_backed = {
        "env": "theorem", "label": "thm:pos-backed",
        "title": "Upper bound",
        "statement": (
            "Status: kernel-verified (0 sorry). Lean: "
            "\\texttt{Lutar/Bound.lean}, \\texttt{Lambda\\_le\\_max}."
        ),
    }
    v = classify(pos_backed, allowlist)
    assert v["status"] == "verified", v

    # NEGATIVE (c): a fabricated served-only kernel-verified claim is caught.
    neg_fabricated = {
        "env": "theorem", "label": "thm:neg-fab",
        "title": "Grand result",
        "statement": (
            "This result is kernel-verified and machine-checked (0 sorry)."
        ),
    }
    v = classify(neg_fabricated, allowlist)
    assert v["status"] == "unbacked", v

    # NEGATIVE (d): unconditional aggregator uniqueness as a proved theorem is
    #    caught (it stays Conjecture 1, never proved unconditionally).
    neg_uncond = {
        "env": "theorem", "label": "thm:neg-uncond",
        "title": "Unique aggregator",
        "statement": (
            "Under axioms A1--A4 the unique aggregator is the geometric mean; "
            "\\texttt{Lutar/Uniqueness.lean}. Status: kernel-verified. The first "
            "machine-checked proof that the governance scalar is uniquely "
            "determined by four axioms."
        ),
    }
    v = classify(neg_uncond, allowlist)
    assert v["status"] == "unconditional-overclaim", v

    # A claim with no proved-status assertion is merely descriptive (no failure).
    descriptive = {
        "env": "corollary", "label": "cor:desc",
        "title": "Interpretability sandwich",
        "statement": "min_i x_i <= Lambda_9(x) <= max_i x_i.",
    }
    v = classify(descriptive, allowlist)
    assert v["status"] == "descriptive", v

    # Tolerant loader recovers complete objects from a truncated array.
    import tempfile
    fd, tmp = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    try:
        with open(tmp, "w", encoding="utf-8") as fh:
            fh.write('[\n  {"label": "a", "title": "t"},\n'
                     '  {"label": "b", "statement": "kernel-verified')  # truncated
        claims, truncated = load_claims(tmp)
        assert truncated is True, (claims, truncated)
        assert [c.get("label") for c in claims] == ["a"], claims
    finally:
        os.remove(tmp)

    print("self-test OK")
    return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo-path", default=".", help="repository root")
    ap.add_argument("--claims-path", default=None, help="override claims JSON path")
    ap.add_argument("--json", action="store_true", help="emit JSON verdict")
    ap.add_argument("--self-test", action="store_true", help="run fixtures only")
    args = ap.parse_args(argv)

    if args.self_test:
        return _self_test()

    result = evaluate(args.repo_path, args.claims_path)

    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        c = result["counts"]
        print(
            "claim backing registry: "
            f"{c.get('verified', 0)} verified · "
            f"{c.get('conditional', 0)} conditional · "
            f"{c.get('descriptive', 0)} descriptive · "
            f"{c.get('unbacked', 0)} unbacked · "
            f"{c.get('unconditional-overclaim', 0)} unconditional-overclaim "
            f"({result['n_claims_scanned']} scanned)"
        )
        if result["truncated_partial_harvest"]:
            print(
                "  note: claims JSON is a documented PARTIAL harvest — only "
                "complete leading objects were scanned (no fabricated tail)."
            )
        mark = {
            "verified": "OK ", "conditional": "~~ ", "descriptive": ".. ",
            "unbacked": "!! ", "unconditional-overclaim": "XX ",
        }
        for r in result["registry"]:
            print(f"  {mark.get(r['status'], '?? ')}{r['label']:<28} {r['status']}")
        for r in result["unbacked"]:
            print(f"  UNBACKED SERVED CLAIM: {r['label']}")
        for r in result["unconditional_overclaims"]:
            print(
                "  OVERCLAIM (unconditional aggregator uniqueness must stay "
                f"Conjecture 1 / Theorem U conditional): {r['label']}"
            )
        print("VERDICT:", "OK" if result["ok"] else "FAIL")

    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
