#!/usr/bin/env python3
"""Check that preprint and investor pages state each preprint DOI once and consistently.

The check is offline and stdlib-only. It never contacts Zenodo, DataCite or
doi.org, so it cannot show that a DOI resolves or which record it names. It
checks something narrower: the repository gives each preprint one DOI, the same
one everywhere, and an investor page never lists a theory preprint under a
"measured" heading.

Rules, each reported with a stable code:

  DOI_STATEMENT_COUNT     A preprint README.md or main.md has more than one
                          line that starts with ``**DOI:**``, for example a DOI
                          plus a stale "not assigned" or "tag a release to
                          mint" line.
  DOI_LINK_MISMATCH       A DOI link whose text and doi.org target differ.
  DOI_FILE_MISMATCH       A paper's README.md and main.md both make a DOI
                          statement, and the statements give different DOIs.
  DOI_SHARED              Two papers give the same DOI.
  INVESTOR_UNKNOWN_PAPER  An investor page labels a DOI "P<n>", and no
                          preprint README calls itself "Preprint P<n>".
  INVESTOR_DOI_MISMATCH   An investor page labels a DOI "P<n>", and P<n>'s
                          README gives a different DOI or none.
  MEASURED_SECTION_THEORY_PAPER
                          An investor section with "measured" in its heading
                          cites the DOI of a preprint whose README declares no
                          receipted measured claims. A README declares them
                          with a line that starts with ``**Measured claims``
                          and a line that starts with ``**Receipts:**``.

    python3 scripts/check_preprint_doi_consistency.py [--repo-path .]
    python3 scripts/check_preprint_doi_consistency.py --self-test
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys
import tempfile
from dataclasses import dataclass, field

DOI = r"10\.5281/zenodo\.\d+"
DOI_RE = re.compile(DOI)
DOI_LINK_RE = re.compile(r"\[(" + DOI + r")\]\(https://doi\.org/(" + DOI + r")\)")
STATEMENT_RE = re.compile(r"^\*\*DOI:\*\*.*$", re.MULTILINE)
PAPER_LABEL_RE = re.compile(r"\bPreprint P(\d+)\b")
MEASURED_CLAIMS_RE = re.compile(r"^\*\*Measured claims\b", re.MULTILINE)
RECEIPTS_RE = re.compile(r"^\*\*Receipts:\*\*", re.MULTILINE)
HEADING_RE = re.compile(r"^#{1,6}\s+(.*)$")
MEASURED_HEADING_RE = re.compile(r"\bmeasured\b", re.IGNORECASE)
NOT_MEASURED_RE = re.compile(r"\b(?:not|never)\s+measured\b", re.IGNORECASE)
LABEL_RE = re.compile(r"\bP(\d+)\b")
PAPER_FILES = ("README.md", "main.md")


@dataclass(frozen=True)
class Finding:
    code: str
    path: str
    message: str

    def __str__(self) -> str:
        return f"{self.code} {self.path}: {self.message}"


@dataclass
class Paper:
    directory: str
    label: int | None = None
    measured: bool = False
    # file name -> DOIs named by that file's **DOI:** statements; a file with no
    # statement is absent, a statement that names no DOI maps to an empty set.
    statements: dict[str, frozenset[str]] = field(default_factory=dict)

    @property
    def dois(self) -> frozenset[str]:
        """The paper's DOIs as its landing page (README.md, else main.md) states them."""
        for name in PAPER_FILES:
            if name in self.statements:
                return self.statements[name]
        return frozenset()


def _read(path: pathlib.Path) -> str:
    return path.read_text(encoding="utf-8")


def _rel(root: pathlib.Path, path: pathlib.Path) -> str:
    return path.relative_to(root).as_posix()


def _link_findings(rel: str, line_no: int, line: str) -> list[Finding]:
    return [
        Finding(
            "DOI_LINK_MISMATCH",
            f"{rel}:{line_no}",
            f"link text {text} points at https://doi.org/{target}",
        )
        for text, target in DOI_LINK_RE.findall(line)
        if text != target
    ]


def load_papers(root: pathlib.Path) -> tuple[list[Paper], list[Finding]]:
    papers: list[Paper] = []
    findings: list[Finding] = []
    preprints = root / "preprints"
    if not preprints.is_dir():
        return papers, findings
    for directory in sorted(p for p in preprints.iterdir() if p.is_dir()):
        paper = Paper(directory=_rel(root, directory))
        for name in PAPER_FILES:
            path = directory / name
            if not path.is_file():
                continue
            text = _read(path)
            rel = _rel(root, path)
            if name == "README.md":
                label = PAPER_LABEL_RE.search(text)
                paper.label = int(label.group(1)) if label else None
                paper.measured = bool(MEASURED_CLAIMS_RE.search(text) and RECEIPTS_RE.search(text))
            statements = STATEMENT_RE.findall(text)
            if len(statements) > 1:
                shown = " | ".join(s.strip()[:70] for s in statements)
                findings.append(
                    Finding(
                        "DOI_STATEMENT_COUNT",
                        rel,
                        f"{len(statements)} '**DOI:**' statements, keep exactly one: {shown}",
                    )
                )
            if statements:
                paper.statements[name] = frozenset(
                    doi for statement in statements for doi in DOI_RE.findall(statement)
                )
            for line_no, line in enumerate(text.splitlines(), start=1):
                if line.startswith("**DOI:**"):
                    findings.extend(_link_findings(rel, line_no, line))
        if paper.statements or paper.label is not None:
            papers.append(paper)
    return papers, findings


def check_papers(papers: list[Paper]) -> list[Finding]:
    findings: list[Finding] = []
    owners: dict[str, list[str]] = {}
    for paper in papers:
        readme = paper.statements.get("README.md")
        main = paper.statements.get("main.md")
        if readme is not None and main is not None and readme != main:
            findings.append(
                Finding(
                    "DOI_FILE_MISMATCH",
                    paper.directory,
                    f"README.md gives {sorted(readme) or 'no DOI'}, main.md gives {sorted(main) or 'no DOI'}",
                )
            )
        for doi in sorted(set().union(*paper.statements.values()) if paper.statements else ()):
            owners.setdefault(doi, []).append(paper.directory)
    for doi, directories in sorted(owners.items()):
        if len(directories) > 1:
            findings.append(Finding("DOI_SHARED", doi, f"given by {', '.join(directories)}"))
    return findings


def check_investor_pages(root: pathlib.Path, papers: list[Paper]) -> list[Finding]:
    findings: list[Finding] = []
    investor = root / "investor"
    if not investor.is_dir():
        return findings
    by_label = {paper.label: paper for paper in papers if paper.label is not None}
    by_doi = {doi: paper for paper in papers for doi in paper.dois}
    for path in sorted(investor.glob("*.md")):
        rel = _rel(root, path)
        measured_heading: str | None = None
        in_fence = False
        for line_no, line in enumerate(_read(path).splitlines(), start=1):
            if line.lstrip().startswith("```"):
                in_fence = not in_fence
                continue
            heading = None if in_fence else HEADING_RE.match(line)
            if heading:
                title = heading.group(1)
                is_measured = MEASURED_HEADING_RE.search(title) and not NOT_MEASURED_RE.search(title)
                measured_heading = title if is_measured else None
                continue
            where = f"{rel}:{line_no}"
            findings.extend(_link_findings(rel, line_no, line))
            for match in DOI_LINK_RE.finditer(line):
                doi = match.group(1)
                # The label that names a DOI is the last "P<n>" before it in the
                # same ';'-separated item, so "P3 data feeds P5 *X* — [doi]" is P5.
                item_start = line.rfind(";", 0, match.start()) + 1
                labels = LABEL_RE.findall(line, item_start, match.start())
                if not labels:
                    continue
                label = int(labels[-1])
                paper = by_label.get(label)
                if paper is None:
                    findings.append(
                        Finding("INVESTOR_UNKNOWN_PAPER", where, f"P{label} cites {doi}, but no README says 'Preprint P{label}'")
                    )
                elif doi not in paper.dois:
                    stated = sorted(paper.dois) or "no DOI"
                    findings.append(
                        Finding(
                            "INVESTOR_DOI_MISMATCH",
                            where,
                            f"P{label} cites {doi}, but {paper.directory}/README.md gives {stated}",
                        )
                    )
            if measured_heading is None:
                continue
            for doi in sorted(set(DOI_RE.findall(line))):
                paper = by_doi.get(doi)
                if paper is not None and not paper.measured:
                    findings.append(
                        Finding(
                            "MEASURED_SECTION_THEORY_PAPER",
                            where,
                            f"{doi} ({paper.directory}) sits under the heading '{measured_heading}', "
                            "but that README declares no receipted measured claims",
                        )
                    )
    return findings


def check_loaded(root: pathlib.Path) -> tuple[list[Paper], list[Finding]]:
    papers, findings = load_papers(root)
    return papers, findings + check_papers(papers) + check_investor_pages(root, papers)


def check(root: pathlib.Path) -> list[Finding]:
    return check_loaded(root)[1]


# --- self-test -------------------------------------------------------------

def _doi_line(recid: int) -> str:
    doi = f"10.5281/zenodo.{recid}"
    return f"**DOI:** [{doi}](https://doi.org/{doi}) — published on Zenodo."


MEASURED_README = (
    "# Measured paper\n\n{doi}\n\nPreprint P3 — **not peer reviewed**.\n\n"
    "**Measured claims (all receipted):**\n- 10/10 chains\n\n**Receipts:** `chain-test.json`\n"
)
THEORY_README = "# Theory paper\n\n{doi}\n\nPreprint P5 — **not peer reviewed**.\n\nA formula identity.\n"
MAIN = "# Paper\n\n*Preprint. Not peer reviewed.*\n\n{doi}\n\n## Abstract\n"
ONE_PAGER = (
    "# Company\n\n### Production, measured (every number below has a published receipt)\n\n"
    "- **One preprint derived from these measurements:** P3 *Measured paper* — "
    "[10.5281/zenodo.100](https://doi.org/10.5281/zenodo.100).\n\n"
    "### Theory preprints (formal arguments, not production measurements)\n\n"
    "- P5 *Theory paper* — [10.5281/zenodo.200](https://doi.org/10.5281/zenodo.200).\n"
)


def baseline_files() -> dict[str, str]:
    return {
        "preprints/measured/README.md": MEASURED_README.format(doi=_doi_line(100)),
        "preprints/measured/main.md": MAIN.format(doi=_doi_line(100)),
        "preprints/theory/README.md": THEORY_README.format(doi=_doi_line(200)),
        "preprints/theory/main.md": MAIN.format(doi=_doi_line(200)),
        "investor/ONE_PAGER.md": ONE_PAGER,
    }


def _append(name: str, text: str):
    def mutate(files: dict[str, str]) -> None:
        files[name] += text
    return mutate


def _replace(name: str, old: str, new: str):
    def mutate(files: dict[str, str]) -> None:
        if old not in files[name]:
            raise ValueError(f"self-test fixture {name} has no {old!r}")
        files[name] = files[name].replace(old, new)
    return mutate


def _chain(*mutations):
    def mutate(files: dict[str, str]) -> None:
        for mutation in mutations:
            mutation(files)
    return mutate


def _unchanged(files: dict[str, str]) -> None:
    return None


# (name, mutation, expected codes); an empty set means the tree must pass.
SELF_TEST_CASES = [
    ("baseline passes", _unchanged, set()),
    (
        "stale 'not assigned' line under a recorded DOI",
        _append("preprints/measured/README.md", "\n**DOI:** not assigned. Local metadata only.\n"),
        {"DOI_STATEMENT_COUNT"},
    ),
    (
        "stale 'tag a release to mint' line under a recorded DOI",
        _append("preprints/theory/README.md", "\n**DOI:** tag release `p5-v1.0.0` to mint.\n"),
        {"DOI_STATEMENT_COUNT"},
    ),
    (
        "link text and target disagree",
        _replace(
            "preprints/measured/README.md",
            "(https://doi.org/10.5281/zenodo.100)",
            "(https://doi.org/10.5281/zenodo.101)",
        ),
        {"DOI_LINK_MISMATCH"},
    ),
    (
        "README and main.md disagree",
        _replace("preprints/measured/main.md", "zenodo.100", "zenodo.999"),
        {"DOI_FILE_MISMATCH"},
    ),
    (
        "README says not assigned, main.md gives a DOI",
        _replace("preprints/theory/README.md", _doi_line(200), "**DOI:** not assigned."),
        {"DOI_FILE_MISMATCH", "INVESTOR_DOI_MISMATCH"},
    ),
    (
        "two papers share a DOI",
        _chain(*(
            _replace(name, "zenodo.200", "zenodo.100")
            for name in ("preprints/theory/README.md", "preprints/theory/main.md", "investor/ONE_PAGER.md")
        )),
        {"DOI_SHARED"},
    ),
    (
        "investor label points at another paper's DOI",
        _replace(
            "investor/ONE_PAGER.md",
            "P5 *Theory paper* — [10.5281/zenodo.200](https://doi.org/10.5281/zenodo.200)",
            "P5 *Theory paper* — [10.5281/zenodo.100](https://doi.org/10.5281/zenodo.100)",
        ),
        {"INVESTOR_DOI_MISMATCH"},
    ),
    (
        "investor label names no preprint",
        _append("investor/ONE_PAGER.md", "- P9 *Missing* — [10.5281/zenodo.900](https://doi.org/10.5281/zenodo.900).\n"),
        {"INVESTOR_UNKNOWN_PAPER"},
    ),
    (
        "theory preprint listed under the measured heading",
        _replace(
            "investor/ONE_PAGER.md",
            "[10.5281/zenodo.100](https://doi.org/10.5281/zenodo.100).\n",
            "[10.5281/zenodo.100](https://doi.org/10.5281/zenodo.100);\n"
            "  P5 *Theory paper* — [10.5281/zenodo.200](https://doi.org/10.5281/zenodo.200).\n",
        ),
        {"MEASURED_SECTION_THEORY_PAPER"},
    ),
    (
        "unlabelled theory DOI under the measured heading",
        _replace(
            "investor/ONE_PAGER.md",
            "### Theory preprints",
            "- See [10.5281/zenodo.200](https://doi.org/10.5281/zenodo.200).\n\n### Theory preprints",
        ),
        {"MEASURED_SECTION_THEORY_PAPER"},
    ),
    (
        "a 'not measured' heading is not a measured section",
        _replace("investor/ONE_PAGER.md", "(formal arguments, not production measurements)", "(not measured)"),
        set(),
    ),
    (
        "the label nearest the DOI names it",
        _replace("investor/ONE_PAGER.md", "- P5 *Theory paper*", "- Built on P3's receipts, P5 *Theory paper*"),
        set(),
    ),
]


def write_tree(root: pathlib.Path, files: dict[str, str]) -> None:
    for name, text in files.items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")


def run_case(mutation) -> set[str]:
    files = baseline_files()
    mutation(files)
    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        write_tree(root, files)
        return {finding.code for finding in check(root)}


def self_test() -> int:
    failures = 0
    for name, mutation, expected in SELF_TEST_CASES:
        found = run_case(mutation)
        ok = expected <= found if expected else not found
        if not ok:
            failures += 1
            print(f"  SELF-TEST FAIL: {name}: expected {sorted(expected) or 'no findings'}, got {sorted(found) or 'no findings'}")
    if failures:
        print(f"preprint DOI consistency self-test FAILED ({failures} of {len(SELF_TEST_CASES)} cases)")
        return 1
    negatives = sum(1 for _, _, expected in SELF_TEST_CASES if expected)
    positives = len(SELF_TEST_CASES) - negatives
    print(f"preprint DOI consistency self-test OK: {positives} positive + {negatives} negative cases")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--repo-path", default=".")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return self_test()

    root = pathlib.Path(args.repo_path).resolve()
    papers, findings = check_loaded(root)
    pages = len(list((root / "investor").glob("*.md"))) if (root / "investor").is_dir() else 0
    print(f"preprint DOI consistency: {len(papers)} papers · {pages} investor pages · {len(findings)} errors")
    for finding in findings:
        print(f"  ERROR: {finding}")
    print("VERDICT:", "OK" if not findings else "FAIL")
    return 0 if not findings else 1


if __name__ == "__main__":
    sys.exit(main())
