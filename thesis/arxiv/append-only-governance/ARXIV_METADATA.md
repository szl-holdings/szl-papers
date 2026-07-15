# arXiv submission metadata — Paper 1 (flagship)

**Files in this package:** `main.tex`, `references.bib`
**Compile:** `pdflatex main && pdflatex main` (bibliography is inline; no BibTeX database; standard `article` plus bundled TeX packages).

---

## Title
Verifiable Append-Only Governance: Kernel-Proven Acyclicity, FIFO Reception, and Emit Monotonicity for AI Decision Receipts

## Authors
Stephen P. Lutar Jr. (SZL Holdings, Inc.) — ORCID 0009-0001-0110-4173

## arXiv categories
- **Primary:** `cs.LO` (Logic in Computer Science)
- **Cross-list:** `cs.CR` (Cryptography and Security), `cs.DC` (Distributed, Parallel, and Cluster Computing), `cs.LG` (Machine Learning)

## ACM classification
F.3.1 (Specifying and Verifying and Reasoning about Programs); D.4.5 (Reliability — verification); K.6.5 (Security and Protection)

## MSC 2020
68V15 (Formal proofs / proof assistants); 68W15 (Distributed algorithms); 68M14 (Distributed systems)

## License
CC-BY-4.0

## Comments field (suggested)
20 pages including appendices. Lean 4 / Mathlib machine-checked; focal declarations are sorry-free and use only disclosed Lean core axioms. Proof snapshot: 5cfaf9a3b55fd75e8a2a1197502a93dd8ca68be3; the distinct frozen Doctrine-v11 count baseline is c7c0ba17c2eaec60ad38ea9172b4a0d9ca0b582f. The locked-proven formula registry contains exactly eight entries (locked_count_eight, by decide). Related umbrella record (not this paper's DOI): 10.5281/zenodo.19944926. Source: github.com/szl-holdings/lutar-lean.

## Abstract (ready to paste)
Agentic AI is post-deterministic: the same prompt and tools may yield different action sequences, so accountability cannot rest on re-deriving a deterministic trace. It must instead rest on a record whose structural invariants are themselves verifiable. We give a machine-checked foundation for three such invariants over a modeled AI decision-receipt substrate: (F4) a backward-reference receipt graph is acyclic and remains acyclic under append; (F7) the modeled Chaski batch drain preserves first-in-first-out order, with a positional equality witness; and (F22) the constructed range log extends by the next sequence number and is strictly monotone by position. The three proof terms are checked and non-vacuous at snapshot 5cfaf9a3b55fd75e8a2a1197502a93dd8ca68be3. They move the separate disclosure registry from five to exactly eight entries, a count certified by locked_count_eight, while the canonical 749/14/163 declaration baseline remains frozen at the earlier Doctrine commit c7c0ba17. We define the adversary and refinement boundary, give countermodels and negative controls, distinguish the string-valued disclosure registry from required per-declaration #print axioms output, and provide a commit-addressed reproducibility and deployment-audit protocol. The work claims structural safety under explicit constructors, not cryptographic immutability, exactly-once delivery, durable broker semantics, storage overwrite prevention, Byzantine agreement, or a verified database implementation.

## Honesty notes for the founder
- F4/F7/F22 are kernel-checked at the named proof snapshot and registered in the locked-proven formula set; the canonical 749/14/163 baseline is a distinct earlier commit and the paper now says so explicitly.
- F4 and F7 were previously vacuous; the paper states this openly as the non-vacuity audit narrative — a strength, not a liability.
- Paper-and-pencil consequences and pseudocode are labeled as such and are not added to the locked theorem count.
- No fabricated benchmarks, citations, or arXiv IDs appear.
