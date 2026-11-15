"""Regression tests for scripts/check_preprint_doi_consistency.py.

The real-tree test is the one that matters: it fails on the tree that commit
bc985cc left behind (each preprint README stated a DOI and, lower down, "DOI:
not assigned" or "tag a release to mint"; the investor one-pager listed three
theory preprints as "derived from measured production data") and passes once
those statements agree.

    python3 -m unittest discover -s scripts -p 'test_check_preprint_doi_consistency.py' -v
"""
import os
import pathlib
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_preprint_doi_consistency as guard

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]


def codes_for(files: dict[str, str]) -> list[str]:
    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        guard.write_tree(root, files)
        return sorted(finding.code for finding in guard.check(root))


class RealTreeTest(unittest.TestCase):
    def test_repository_statements_are_consistent(self):
        findings = guard.check(REPO_ROOT)
        self.assertEqual([], [str(finding) for finding in findings])

    def test_every_preprint_doi_statement_is_found(self):
        papers, _ = guard.load_papers(REPO_ROOT)
        stated = [paper for paper in papers if paper.dois]
        # P3-P7 each carry a DOI; a parser that silently found none would pass
        # the consistency test above for the wrong reason.
        self.assertGreaterEqual(len(stated), 5)
        for paper in stated:
            self.assertEqual(1, len(paper.dois), paper.directory)


class FixtureCasesTest(unittest.TestCase):
    def test_self_test_cases(self):
        for name, mutation, expected in guard.SELF_TEST_CASES:
            with self.subTest(name):
                found = guard.run_case(mutation)
                if expected:
                    self.assertLessEqual(expected, found)
                else:
                    self.assertEqual(set(), found)

    def test_self_test_entry_point_passes(self):
        self.assertEqual(0, guard.self_test())


class Bc985ccShapeTest(unittest.TestCase):
    """The exact defect shapes commit bc985cc introduced, reduced to fixtures."""

    def setUp(self):
        self.files = guard.baseline_files()

    def test_doi_added_above_a_stale_not_assigned_line(self):
        self.files["preprints/measured/README.md"] += (
            "\n**DOI:** not assigned. The per-paper `.zenodo.json` is local metadata only.\n"
        )
        self.assertIn("DOI_STATEMENT_COUNT", codes_for(self.files))

    def test_doi_added_above_a_stale_tag_to_mint_line(self):
        self.files["preprints/theory/README.md"] += "\n**DOI:** tag release `p6-v1.0.0` to mint.\n"
        self.assertIn("DOI_STATEMENT_COUNT", codes_for(self.files))

    def test_theory_preprints_listed_as_measured_production_data(self):
        self.files["investor/ONE_PAGER.md"] = (
            "# Company\n\n### Production, measured (every number below has a published receipt)\n\n"
            "- **Two DOI-minted preprints** on Zenodo, all derived from measured production data:\n"
            "  P3 *Measured paper* — [10.5281/zenodo.100](https://doi.org/10.5281/zenodo.100);\n"
            "  P5 *Theory paper* — [10.5281/zenodo.200](https://doi.org/10.5281/zenodo.200).\n"
        )
        self.assertEqual(["MEASURED_SECTION_THEORY_PAPER"], codes_for(self.files))

    def test_reworded_measured_heading_keeps_the_rule(self):
        # A reworded heading (as proposed in PR #70) still names a measured section.
        one_pager = self.files["investor/ONE_PAGER.md"].replace(
            "(every number below has a published receipt)",
            "(November 2026 — each line names its source and says when that source is not yet public)",
        )
        self.files["investor/ONE_PAGER.md"] = one_pager.replace(
            "\n### Theory preprints",
            "- P5 *Theory paper* — [10.5281/zenodo.200](https://doi.org/10.5281/zenodo.200).\n\n### Theory preprints",
        )
        self.assertEqual(["MEASURED_SECTION_THEORY_PAPER"], codes_for(self.files))

    def test_fenced_code_is_not_a_heading(self):
        self.files["investor/ONE_PAGER.md"] = self.files["investor/ONE_PAGER.md"].replace(
            "### Theory preprints (formal arguments, not production measurements)\n",
            "### Theory preprints (formal arguments, not production measurements)\n\n"
            "```\n# measured setup comment, not a heading\n```\n",
        )
        self.assertEqual([], codes_for(self.files))


if __name__ == "__main__":
    unittest.main()
