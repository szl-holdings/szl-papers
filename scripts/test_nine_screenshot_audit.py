"""Offline source-level tests for the user-supplied nine-image research audit."""

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs" / "research" / "NINE_SCREENSHOT_PRIMARY_SOURCE_AUDIT_20261119.md"
UPSTREAM = {
    "SamsungLabs/NanoQuant": "a9e0a430881ff80d83b622c3129e330dc33c04f5",
    "agentic-learning-ai-lab/deleting-weights":
        "94f0340ebb574f95bb41d844165253a6785e215e",
    "Prefrontal-AI/CRAM": "62bbe830c7d6f87f2ba18f30a28039258b986454",
    "HKUST-KnowComp/AtlasKV": "61e3abc1fb09fbfb426cfc847c4c26c5e94bcaeb",
}


class PrimarySourceAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = AUDIT.read_text(encoding="utf-8")

    def test_all_nine_uploaded_images_are_addressed(self):
        for section in (
            "## 1 / NanoQuant",
            "## 2 / Self-improving agent harness",
            "## 3 / Deletion Tuning",
            "## 4 / CRAM",
            "## 5 / Open-source contribution example",
            "## 6 / AtlasKV",
            "## 7 / GPT-6.2 Astra",
            "## 8–9 / Discovered Materials",
        ):
            with self.subTest(section=section):
                self.assertIn(section, self.text)

    def test_four_upstream_commit_sources_are_immutable_ids(self):
        for repository, revision in UPSTREAM.items():
            with self.subTest(repository=repository):
                self.assertRegex(revision, re.compile(r"^[0-9a-f]{40}$"))
                self.assertIn("https://github.com/" + repository, self.text)
                self.assertEqual(self.text.count(revision), 1)

    def test_required_negative_reproduction_boundaries(self):
        for phrase in (
            "not a successful reproduction",
            "offline knowledge-encoding GPU cost",
            "LoRA/MTH baselines",
            "not a trained deletion-mask optimizer",
            "pre-SM80",
            "not independently identified",
            "full-model-memory guarantee",
            "independently calibrated SZL trial",
            "No submission",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase.casefold(), self.text.casefold())

    def test_szl_cram_negative_reproduction_is_preserved(self):
        for marker in (
            "szl-cram",
            "1/150 (0.67%)",
            "13/150 (8.67%)",
            "99.996%",
            "not a directly paired failure ratio",
            "source claims",
            "GPU Triton page kernel",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker.casefold(), self.text.casefold())

    def test_no_unapproved_training_claim(self):
        for phrase in ("NO deployment", "No upstream code was executed"):
            self.assertIn(phrase, self.text)

    def test_first_party_benchmark_links(self):
        for url in (
            "https://proceedings.mlr.press/v306/chong26a.html",
            "https://arxiv.org/abs/2611.10866",
            "https://arxiv.org/abs/2611.17309",
            "https://arxiv.org/abs/2611.22299",
            "https://arxiv.org/abs/2510.17934",
            "https://grandchallenges.discoveredmaterials.com/official-rules",
        ):
            self.assertIn(url, self.text)


if __name__ == "__main__":
    unittest.main()
