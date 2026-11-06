#!/usr/bin/env python3
"""Investor-collateral claim guard (regression test for monetization audit G-04).

Offline and stdlib-only. It reads every Markdown file under ``investor/`` and
fails when the collateral breaks one of four wording rules:

R1 RETRACTED  Wording that presented HTTP 402 payment requests as traction, or
              that said every number has a published receipt, must not return.
R2 SOURCED    Every top-level bullet under a "Production, measured" heading
              names its source: a backticked artifact, a link, or "source:".
R3 PRIVATE    A bullet or line that cites a source known to be private says so
              ("not public" or "not yet public").
R4 VOLUME     A request-volume figure ("N requests per day/week/month") cites an
              attached artifact (a backticked path or a link) in the same bullet.

What this proves: the committed wording obeys the four rules.
What it does NOT prove: that a cited artifact exists, that a figure is correct,
or that a source is still private. Those need a credentialed or network check.
When the owner publishes a source, remove it from PRIVATE_SOURCES in the same
change that drops its "not yet public" label.
"""

from __future__ import annotations

import argparse
import os
import re
from typing import Iterable, List, Tuple

INVESTOR_DIR = "investor"

# R1: the G-04 failure mode. 402 responses are payment requests, not sales.
RETRACTED = (
    ("402 payment demands", re.compile(r"\b402\b[^\n]{0,60}?\bpayment\s+demands?\b", re.I)),
    ("payment demands served", re.compile(r"\bpayment\s+demands?\s+served\b", re.I)),
    (
        "402 responses counted per period",
        re.compile(
            r"\b402\s+(?:responses?|refusals?|prompts?|requests?)\b[^\n.]{0,40}?"
            r"(?:/|\bper\b)\s*(?:day|week|month)\b",
            re.I,
        ),
    ),
    (
        "every number has a published receipt",
        re.compile(r"\bevery\s+number\b[^\n]{0,40}?\bpublished\s+receipts?\b", re.I),
    ),
)

# R3: sources that are private as of 2026-11-06 (coordinator HF index: dataset
# SZLHOLDINGS/model-eval-receipts has private=true; the Cloudflare rule export
# lives only in the operator workspace).
PRIVATE_SOURCES = (
    (
        re.compile(
            r"model-eval-receipts|loadtest-inference-2026-11-05\.json|chain-test-mcp-2026-11-05\.json"
        ),
        "HF dataset SZLHOLDINGS/model-eval-receipts is private",
    ),
    (
        re.compile(r"\bgateway(?:['’]s)?\s+rule\s+(?:configuration|export)\b", re.I),
        "the Cloudflare Monetization Gateway rule export is not public",
    ),
)
NOT_PUBLIC = re.compile(r"\bnot\s+(?:yet\s+)?public\b", re.I)

ARTIFACT = re.compile(r"`[^`\n]+`|\]\([^)\s]+\)|https?://\S+")
SOURCE = re.compile(ARTIFACT.pattern + r"|\bsource:", re.I)
VOLUME = re.compile(
    r"\d[\d,.]*\s*[kKmM]?\+?\s+(?:HTTP\s+)?requests?\s*(?:/|\bper\b|\ba\b|\beach\b)\s*(?:day|week|month)\b",
    re.I,
)
HEADING = re.compile(r"^(#{1,6})\s+(.*)$")
BULLET = re.compile(r"^[-*+]\s+")
MEASURED = re.compile(r"\bproduction,?\s+measured\b", re.I)

Block = Tuple[int, str, bool, bool]  # (first line, text, is_bullet, in_measured_section)


def blocks(text: str) -> List[Block]:
    """Split Markdown into blocks: a bullet with its indented continuation
    lines, or any other single non-blank line (headings included)."""
    out: List[Block] = []
    section_level = 0  # level of the open "Production, measured" heading, 0 = none
    current = None  # [first line, [lines], in_section]
    in_fence = False
    for number, line in enumerate(text.splitlines(), start=1):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
        heading = None if in_fence else HEADING.match(line)
        if heading:
            level = len(heading.group(1))
            if section_level and level <= section_level:
                section_level = 0
            if MEASURED.search(heading.group(2)):
                section_level = level
        if current and line.strip() and line[:1].isspace() and not heading:
            current[1].append(line.strip())
            continue
        if current:
            out.append((current[0], " ".join(current[1]), True, current[2]))
            current = None
        if not line.strip():
            continue
        if BULLET.match(line) and not in_fence:
            current = [number, [line.strip()], bool(section_level)]
        else:
            out.append((number, line.strip(), False, bool(section_level) and not heading))
    if current:
        out.append((current[0], " ".join(current[1]), True, current[2]))
    return out


def check_text(text: str, label: str) -> List[str]:
    findings: List[str] = []
    for number, body, is_bullet, in_section in blocks(text):
        where = f"{label}:{number}"
        for name, pattern in RETRACTED:
            if pattern.search(body):
                findings.append(f"{where}: R1 RETRACTED: {name!r} presents 402s or receipts as traction")
        if is_bullet and in_section and not SOURCE.search(body):
            findings.append(
                f'{where}: R2 SOURCED: bullet under "Production, measured" names no source '
                '(add a backticked artifact, a link, or "source: ...")'
            )
        for pattern, why in PRIVATE_SOURCES:
            if pattern.search(body) and not NOT_PUBLIC.search(body):
                findings.append(f'{where}: R3 PRIVATE: {why}, but the line does not say "not yet public"')
        if VOLUME.search(body) and not ARTIFACT.search(body):
            findings.append(f"{where}: R4 VOLUME: request-volume figure cites no attached artifact")
    return findings


def markdown_files(repo_root: str) -> List[str]:
    root = os.path.join(repo_root, INVESTOR_DIR)
    if not os.path.isdir(root):
        raise FileNotFoundError(f"{root} does not exist (guard fails closed)")
    paths = sorted(
        os.path.join(dirpath, name)
        for dirpath, _dirs, names in os.walk(root)
        for name in names
        if name.lower().endswith(".md")
    )
    if not paths:
        raise FileNotFoundError(f"no Markdown files under {root} (guard fails closed)")
    return paths


def check_repository(repo_root: str) -> Tuple[int, List[str]]:
    findings: List[str] = []
    paths = markdown_files(repo_root)
    for path in paths:
        with open(path, "r", encoding="utf-8") as handle:
            findings.extend(check_text(handle.read(), os.path.relpath(path, repo_root)))
    return len(paths), findings


GOOD_PAGE = """# Example
### Production, measured (each line names its source)

- **x402 rules are enabled on 7 prefixes** (source: the gateway's rule configuration, which is not public).
- **p99 = 3.77 s** (receipt: `SZLHOLDINGS/model-eval-receipts/loadtest-inference-2026-11-05.json`; not yet public).
- **Five preprints**:
  P3 [10.5281/zenodo.24005477](https://doi.org/10.5281/zenodo.24005477).
- **A model** (source: the `SZLHOLDINGS/SZL-Reasoning-0.8B-v1` model card).
- **1.2M requests/week** (source: `analytics-export-2026-11.json`).

We do not count 402 responses as traction.

### The honest-failure differentiator

- An unsourced bullet outside the measured section is allowed.
"""

BAD_CASES = (
    (
        "the retracted G-04 line",
        "### Production, measured\n\n- **~330,000 requests/week** across the estate (Cloudflare zone analytics); "
        "**8,710 HTTP 402 payment demands served per day** on the x402-monetized surfaces.\n",
        ("R1 RETRACTED", "R2 SOURCED", "R4 VOLUME"),
    ),
    (
        "the retracted heading",
        "### Production, measured (November 2026 — every number below has a published receipt)\n",
        ("R1 RETRACTED",),
    ),
    ("402 counts per period", "- We served 9,000 402 responses per day.\n", ("R1 RETRACTED",)),
    (
        "a measured bullet with no source",
        "### Production, measured\n\n- **A model trained on certified reasoning data.**\n",
        ("R2 SOURCED",),
    ),
    (
        "a private receipt not labelled",
        "- p99 = 3.77 s (receipt: `SZLHOLDINGS/model-eval-receipts/loadtest-inference-2026-11-05.json`).\n",
        ("R3 PRIVATE",),
    ),
    (
        "the gateway export not labelled",
        "- 4 rules (source: the gateway’s rule configuration on 2026-11-06).\n",
        ("R3 PRIVATE",),
    ),
    (
        "a volume figure sourced only in prose",
        "- **1.2M requests per week** (source: Cloudflare zone analytics).\n",
        ("R4 VOLUME",),
    ),
)


def self_test() -> List[str]:
    failures: List[str] = []
    good = check_text(GOOD_PAGE, "good")
    if good:
        failures.append(f"positive fixture produced findings: {good}")
    for name, text, expected in BAD_CASES:
        found = check_text(text, "bad")
        for rule in expected:
            if not any(rule in finding for finding in found):
                failures.append(f"negative fixture {name!r} did not raise {rule}: {found}")
        unexpected = [f for f in found if not any(rule in f for rule in expected)]
        if unexpected:
            failures.append(f"negative fixture {name!r} raised unexpected findings: {unexpected}")
    return failures


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--repo-path", default=".")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(list(argv) if argv is not None else None)

    if args.self_test:
        failures = self_test()
        for failure in failures:
            print(f"  SELF-TEST FAIL: {failure}")
        if failures:
            return 1
        print(f"investor claims self-test OK: 1 positive + {len(BAD_CASES)} negative fixtures")
        return 0

    try:
        count, findings = check_repository(args.repo_path)
    except (OSError, UnicodeDecodeError) as exc:
        print(f"::error::investor claim guard could not run: {exc}")
        return 2
    print(f"investor claims: {count} files · {len(findings)} findings")
    for finding in findings:
        print(f"  ERROR: {finding}")
    print("VERDICT:", "FAIL" if findings else "OK")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
