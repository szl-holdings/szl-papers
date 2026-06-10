# arXiv submission metadata — Paper 1 (flagship)

**Files in this package:** `main.tex`, `references.bib`
**Compile:** `pdflatex main && bibtex main && pdflatex main && pdflatex main` (no external classes; standard `article` + amsmath/booktabs/listings/hyperref).

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
~15 pages. Lean 4 / Mathlib machine-checked; sorry-free; axioms limited to the Lean core {propext, funext, Classical.choice, Quot.sound}. Locked-proven formula count raised from five to exactly eight (locked_count_eight, by decide). Companion concept DOI: 10.5281/zenodo.19944926. Source repository: github.com/szl-holdings/lutar-lean.

## Abstract (ready to paste)
Agentic AI is post-deterministic: the same prompt and tools may yield different action sequences, so accountability cannot rest on re-deriving a deterministic trace. It must instead rest on a record whose structural invariants are themselves verifiable. We give a machine-checked foundation for three such invariants over an AI decision-receipt substrate, all proven in Lean 4 with no sorry and no axiom beyond the Lean core {propext, funext, Classical.choice, Quot.sound}: (F4) the receipt directed acyclic graph (DAG) is acyclic and remains acyclic under append; (F7) the inter-organ messaging channel (Chaski) delivers in first-in-first-out (FIFO) order, with a positional witness that the i-th received message equals the i-th sent message; and (F22) the emit log is append-only and strictly monotone in sequence number. These three results, kernel-verified and non-vacuous as of 2026-06-10, raise SZL Holdings' locked-proven formula count from five to exactly eight, a fact itself certified by a decidable theorem (locked_count_eight). We position the work against the verifiable-claims literature and machine-checked-systems tradition, are explicit about what is locked versus experimental, and document a non-vacuity audit that retired two previously-vacuous statements (a repackaged hypothesis and a reflexive identity) in favor of genuine theorems over concrete models.

## Honesty notes for the founder
- Every claim is locked/kernel-verified; no conjecture is dressed as a theorem.
- F4 and F7 were previously vacuous; the paper states this openly as the non-vacuity audit narrative — a strength, not a liability.
- No fabricated benchmarks, citations, or arXiv IDs appear.
