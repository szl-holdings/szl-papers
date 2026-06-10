# arXiv submission metadata — Paper 3 (GPD unification thesis, v26)

**Files in this package:** `main.tex`, `references.bib`
**Source prose:** `../unified-gpd-thesis-v26.md` (Markdown master)
**Compile:** `pdflatex main && bibtex main && pdflatex main && pdflatex main` (standard `article` + amsmath/booktabs/longtable/listings/hyperref).

---

## Title
Governed Post-Determinism: A Unified Theory of Verifiable Autonomy — The Lutar Invariant, Khipu Consensus, and the Provenance Substrate (The Ouroboros Thesis v26, Locked-Eight Edition)

## Authors
Stephen P. Lutar Jr. (SZL Holdings, Inc.) — ORCID 0009-0001-0110-4173

## arXiv categories
- **Primary:** `cs.LO` (Logic in Computer Science)
- **Cross-list:** `cs.CR` (Cryptography and Security), `cs.LG` (Machine Learning), `math.OC` (Optimization and Control)

## ACM classification
F.3.1 (Specifying, Verifying, Reasoning about Programs); D.4.6 (Security and Protection); I.2.0 (AI — general)

## MSC 2020
68V15 (Formal proofs / proof assistants); 68W15 (Distributed algorithms); 39B22 (Functional equations); 68T01 (AI foundations)

## License
CC-BY-4.0

## Comments field (suggested)
~16 pages. Unification thesis over the SZL DOI-pinned lineage (v1–v25). Locked-proven = exactly eight formulas {F1,F4,F7,F11,F12,F18,F19,F22} (locked_count_eight, by decide); locked-kernel baseline c7c0ba17 (749/14/163). Lambda uniqueness is Conjecture 1 (machine-checked FALSE) with axiom-free conditional Theorem U; Khipu BFT safety is Conjecture 2 (Wave-23 conditional only). Concept DOI: 10.5281/zenodo.19944926. Repository: github.com/szl-holdings/lutar-lean.

## Abstract (ready to paste)
Autonomous and agentic artificial intelligence is post-deterministic: the same prompt, model, and tools can produce different action sequences, and the controlling logic is statistical rather than fixed. Deployed into regulated and defense settings, such systems break the classical assumption that auditing means re-deriving a deterministic trace. We unify the SZL Holdings research program (v1–v25, DOI-pinned) into a single framework, Governed Post-Determinism (GPD): a discipline for bounding, attesting, and replicating the behavior of post-deterministic agents so that every governed action carries a checkable, tamper-evident warrant. GPD rests on five pillars, each mapped to an exact, honestly-tiered result: Protocol-Bounded Execution (F1, locked); Verifiable Intent-to-Execution (a locked triad F4/F7/F22 plus F18 and attested SLSA L1+L2 provenance); a Bounded-Recursion Control Plane whose aggregator is the Lutar invariant (the equal-weight geometric mean), whose unconditional uniqueness is machine-checked FALSE (Conjecture 1) but whose conditional uniqueness under slice-multiplicativity is proven axiom-free (Theorem U); Semantic Quorum Assurance via Khipu BFT, whose unconditional Byzantine safety is open (Conjecture 2) but whose conditional agreement under n>=3f+1 and honest non-equivocation is proven axiom-clean; and Epistemic State Replication. The unifying observation is a single structural pattern: in each pillar the honest result is a conditional theorem whose antecedent is the weakest checkable hypothesis, and the unconditional statement sits at a machine-checked sharp boundary. We hold an honesty doctrine binding: locked-proven = exactly eight (a decidable theorem), with roughly 185 experimental CI-green theorems kept in a strictly separate tier.

## Honesty notes for the founder
- Single substantive change from v25: locked count five -> eight (genuine F4/F7/F22 proofs of 2026-06-10); kernel baseline unchanged.
- GPD is grounded only in the SZL Zenodo DOI chain; no external "post-deterministic" framework is claimed as a source.
- Lambda = Conjecture 1, Khipu = Conjecture 2, experimental tier labeled, trust never 100%. No fabricated results, citations, or arXiv IDs.
- A Zenodo concept DOI (10.5281/zenodo.19944926) already exists for the program; this is the first arXiv submission of the thesis line. Cross-reference the DOI in the arXiv "Journal-ref / DOI" or comments field; do NOT claim arXiv posting until the founder completes submission.
