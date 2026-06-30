# PAPER_NOTES.md
## Governed Post-Determinism: A Machine-Checked, Cryptographically-Receipted
## Substrate for Verifiable AI Inference

**Author:** Stephen P. Lutar, Jr. · ORCID 0009-0001-0110-4173 · SZL Holdings, Inc.
**License:** CC-BY-4.0
**Concept DOI:** 10.5281/zenodo.19944926
**Files:** `main.tex` (1299 lines), `references.bib` (371 lines)
**Compiled PDF:** `main.pdf` — **23 pages**, 360,707 bytes (clean compile, no errors)
**Compile command:** `pdflatex main && bibtex main && pdflatex main && pdflatex main`

---

## Page count and structure

| Section | Pages (approx.) | Content |
|---|---|---|
| Title / Abstract / ToC | 1–2 | Abstract, keywords, ACM CCS, MSC 2020, TOC |
| §1 Introduction | 2–4 | Post-deterministic governance gap; thesis; C1–C4 contributions |
| §2 Related Work | 4–6 | Arize/Credo/Fiddler; Sigstore/in-toto/SLSA; seL4; quasi-arith means; BFT |
| §3 Lutar Invariant Λ | 6–8 | Definition, A1–A5, Conjecture 1 (FALSE), Theorem U (proven axiom-free), CUT-1 |
| §4 Eight Locked Formulas | 8–12 | Table of 8; F4 DAG acyclicity detail; F7 FIFO detail; non-vacuity audit; Merkle Functor (EXPERIMENTAL); E8 geometry |
| §5 Governed-Inference Pipeline | 12–14 | Λ-gate → DSSE → in-toto → Merkle; offline verifiability; LIVE/ROADMAP table; SLSA L1+L2 |
| §6 Energy Attestation | 14–15 | GSF SCI signed field; MEASURED; not audited |
| §7 Khipu BFT | 15–17 | Conjecture 2 (OPEN); Theorem (conditional, Wave 23); Conjecture 3; checkable-antecedent pattern |
| §8 Counter-UAS (killinchu) | 17–18 | Interdiction loop; auditability; honest status |
| §9 Honesty Methodology | 18–20 | Doctrine; half-state principle; checkable-antecedent pattern; attributed classical results |
| §10 Limitations & Roadmap | 20–21 | All honest limitations; roadmap table |
| §11 Conclusion | 21–22 | Summary; negative results as positive contributions |
| References | 22 | ~35 real citations; no fabricated entries |
| Appendix A: Lean Theorem Index | 22–23 | Locked-8 table; count theorem; key experimental theorems; axiom ledger |
| Appendix B: Reproducibility | 23 | Pinned commits; verification instructions |
| Appendix C: DOI Lineage | 23 | v1–v26 DOI table; concept DOI |

**Total: 23 pages** (exceeds the 20-page minimum).

---

## Claims vs. honest limitations

### What IS claimed (all honest, doctrine-compliant)

| Claim | Evidence | Tier |
|---|---|---|
| 8 locked-proven Lean formulas {F1,F4,F7,F11,F12,F18,F19,F22} | Lean kernel c7c0ba17 (749/14/163); count = `locked_count_eight` by `decide` | LOCKED |
| Count = exactly 8 | `locked_count_eight : lockedDisclosed.length = 8 := by decide` | LOCKED |
| F4/F7/F22 genuine proofs (non-vacuous) | 2026-06-10 proofs in `ProvedFormulas.lean`; F4/F7 formerly vacuous | LOCKED |
| Theorem U: conditional Λ uniqueness | `lambda_unique_of_separable`; `#print axioms = {propext, Classical.choice, Quot.sound}` (no project axiom) | EXPERIMENTAL, axiom-free |
| Conjecture 1 refutation: unconditional FALSE | `maxAgg_ne_Lambda` witness | EXPERIMENTAL (machine-checked FALSE) |
| Khipu conditional agreement | `khipu_quorum_safety_conditional`; Wave 23; axiom-clean | EXPERIMENTAL |
| DSSE/ECDSA-P256 receipts | LIVE | MEASURED |
| in-toto Statement v1 receipts | LIVE | MEASURED |
| Self-hosted Merkle transparency log | LIVE | MEASURED |
| SLSA L1+L2 attestation | killinchu run 26896047715; a11oy | MEASURED |
| GSF SCI energy field (signed) | LIVE | MEASURED |

### What is HONESTLY labeled as NOT claimed

| Non-claim | Label |
|---|---|
| Λ unconditional uniqueness | Conjecture 1 — machine-checked FALSE |
| Khipu unconditional Byzantine safety | Conjecture 2 — OPEN |
| Khipu liveness | Conjecture 3 — OPEN |
| Per-receipt Sigstore Rekor public log | ROADMAP |
| TEE hardware attestation | ROADMAP |
| SLSA L3 | ROADMAP |
| ATO / IL5 / FedRAMP authorization | ROADMAP |
| New physics or pure mathematics | Not claimed; all attributed to original authors |
| Merkle Functor as locked theorem | EXPERIMENTAL (not in locked 8) |
| Reed–Solomon upper-distance Singleton | OPEN (only lower half proven) |
| BKS n-adic full Λ closure | ROADMAP (Mathlib v4.18.0 blocker) |
| Trust = 100% | Never; zero-absorption design |

---

## arXiv submission metadata

- **Primary category:** `cs.LO` (Logic in Computer Science)
- **Cross-list:** `cs.AI`, `cs.CR` (Cryptography and Security), `cs.DC` (Distributed Computing)
- **Title:** Governed Post-Determinism: A Machine-Checked, Cryptographically-Receipted Substrate for Verifiable AI Inference
- **ACM CCS:** Theory of computation → Logic and verification; Security and privacy → Formal methods; Computing methodologies → Autonomous agents
- **MSC 2020:** 68V15 (formal proofs); 68W15 (distributed algorithms); 39B22 (functional equations); 68T01 (AI foundations)
- **License:** CC-BY-4.0
- **Comments field suggestion:** 23 pages. Lean 4 / Mathlib machine-checked; locked-proven = exactly 8 formulas {F1,F4,F7,F11,F12,F18,F19,F22} (locked_count_eight, by decide) @ kernel c7c0ba17 (749/14/163). Lambda uniqueness is Conjecture 1 (machine-checked FALSE) with axiom-free conditional Theorem U; Khipu BFT safety is Conjecture 2. DSSE/ECDSA-P256 governed-inference receipts LIVE; public Sigstore Rekor per-receipt is ROADMAP. SLSA L1+L2 attested (not L3). Concept DOI: 10.5281/zenodo.19944926. Lean source: github.com/szl-holdings/lutar-lean.

---

## Submit-readiness assessment

| Check | Status |
|---|---|
| Compiles cleanly (pdflatex) | ✓ Zero errors; only hyperref PDF-string warnings (cosmetic) |
| ≥20 pages | ✓ 23 pages |
| Proper arXiv LaTeX (article class, standard packages only) | ✓ |
| All \cite{} resolved | ✓ (after bibtex pass) |
| No fabricated citations or arXiv IDs | ✓ |
| Doctrine-honest: Λ = Conjecture 1 | ✓ |
| Doctrine-honest: Khipu = Conjecture 2 | ✓ |
| Locked count = exactly 8, count theorem cited | ✓ |
| Kernel baseline 749/14/163 @ c7c0ba17 | ✓ |
| SLSA L1+L2 (not L3) | ✓ |
| E8 = error-detection geometry only (not BFT) | ✓ |
| F19/Bekenstein applied, not reclaimed | ✓ |
| Classical results attributed (Lindblad, BCP, Kleene, Tarski, Aczél, Viazovska, McAllester) | ✓ |
| No ATO/IL5/FedRAMP claimed | ✓ |
| Public Rekor labeled ROADMAP | ✓ |
| Trust never 100% | ✓ |
| Concept DOI 10.5281/zenodo.19944926 cited | ✓ |
| Author: Stephen P. Lutar, Jr. ORCID 0009-0001-0110-4173 | ✓ |
| READY TO SUBMIT (founder action required) | **YES** |

**Note:** Do NOT submit to arXiv directly — the founder submits. The paper is format-ready and doctrine-complete.

---

## Distinction from existing szl-papers arXiv packages

The three existing arXiv packages in szl-papers are:
1. `thesis/arxiv/append-only-governance/` — focuses on F4/F7/F22 specifically (~15pp)
2. `thesis/arxiv/graph-substrate/` — focuses on the graph substrate
3. `thesis/arxiv/gpd-v26/` — the GPD unification thesis (~16pp)

This new paper (in `thesis/arxiv/gpd-unified-v26/`) is **distinct** from all three:
- It is explicitly positioned around the cryptographic receipt pipeline (DSSE → in-toto → Merkle)
- It includes the GSF SCI energy attestation section
- It includes the killinchu counter-UAS case study
- It includes a dedicated §9 Honesty Methodology
- It includes full Related Work positioning against Arize/Credo/Fiddler
- It is 23 pages (the "20+ page" arXiv submission)
- It carries the full 11-section structure requested by the task brief

---

*Generated: 2026-06-30 by Perplexity Computer Agent*
*Signed-off-by: Stephen Lutar <stephenlutar2@gmail.com>*
*Co-Authored-By: Perplexity Computer Agent <agent@perplexity.ai>*
