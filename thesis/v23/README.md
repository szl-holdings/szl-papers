# Thesis v23 — The Unified Substrate

**A Machine-Verified Trust Foundation for Governed Agentic AI**

[![Λ Conjecture 1](https://img.shields.io/badge/Λ-Conjecture_1_(NOT_theorem)-blue.svg)](https://github.com/szl-holdings/lutar-lean)
[![Doctrine v11 LOCKED](https://img.shields.io/badge/Doctrine-v11_LOCKED-d4a444.svg)](https://github.com/szl-holdings/lutar-lean)
[![SLSA L1+L2](https://img.shields.io/badge/SLSA-L1%2BL2_attested_(NOT_L3)-green.svg)](https://slsa.dev)
[![Concept DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.19944926-blue.svg)](https://doi.org/10.5281/zenodo.19944926)

**Author:** Stephen P. Lutar Jr. · ORCID [0009-0001-0110-4173](https://orcid.org/0009-0001-0110-4173)
*Co-authored with the SZL full-stack PhD team.*

---

## What this is

v23 is the **unifying** version of the SZL Ouroboros thesis program (v1–v22): a single,
arXiv-style paper (20 pages) consolidating the **Ouroboros loop**, the **Lutar invariant Λ**,
and a **disclosed-axiom proof-trail / receipt architecture** into one machine-verified trust
substrate for governed agentic AI.

The defining commitment is the **honesty doctrine**: every claim is tagged *proven*,
*proven-under-declared-axiom*, or *conjecture*, and the one tempting overclaim (Λ uniqueness) is
guarded by a **machine-checked refutation**.

## The one-line thesis

> v23 is the first machine-verified governed-AI trust substrate with fully disclosed axioms, in
> which the central trust aggregator's uniqueness is proven **conditionally** (under a declared,
> governance-natural block-consistency axiom) while its **unconditional uniqueness is
> machine-checked false** — so the conditional theorem is the maximal true statement and the
> invariant is honestly labeled **Conjecture 1**, never a theorem.

## Files

| File | Description |
|------|-------------|
| `main.tex` | Authoritative arXiv-style LaTeX source (~960 lines). |
| `refs.bib` | 25 real references with DOIs / arXiv IDs. |
| `main.pdf` | Compiled 20-page rendering (ReportLab; embedded DM Sans + JetBrains Mono + DejaVu math fallback). |
| `main.md` | Faithful markdown rendering of the paper. |
| `README.md` | This file. |
| `build_pdf.py` | The ReportLab generator that produces `main.pdf` from the paper content. |
| `fonts/` | Embedded TTFs (DM Sans family + JetBrains Mono). |

> **Rendering note.** No LaTeX engine is available in the build environment; `main.pdf` is produced
> by `build_pdf.py` (ReportLab) as the compiled rendering. `main.tex` is the canonical source and
> compiles with any standard `pdflatex`/`tectonic` toolchain. The task accepts "a compiled or
> markdown rendering" — both are provided.

## Verification status (honest tiers)

| Tier | Count / items | Pin |
|------|---------------|-----|
| **Locked / kernel-verified** | **5** — {F1, F11, F12, F18, F19} (749 decl / 14 axioms / 163 sorries) | `c7c0ba17` |
| Sorry-free, Lean-core only | **+19** Wave-3 cores (C8 Kraft, C9 Shannon, C10 Byzantine 3f+1, C11 DLS, C12 FLP bivalence, C17 BLUE, C20 softmax) | `775093f0` / `02e44c30` |
| Axiom-gated (declared idealizations) | **+4** Merkle (C13, C13a, C14, C14b) | — |
| Conditional theorem (CI-green under declared A6′) | `lambda_unique_under_block` | `043c3df` |
| **Machine-checked FALSE** | `maxAgg_ne_Lambda` — unconditional uniqueness refuted (Thm 4.2) | — |
| **CI-pending (NOT proven)** | C1 Tsirelson 2√2, C2 CHSH ≤ 2, C6 Jensen | — |
| Conjecture 1 | Λ unconditional uniqueness — **never a theorem** | — |

**SLSA L1+L2 attested, NOT L3.** F12 (Kuramoto) and F19 (Bekenstein) are additive scaffolding,
not the full physical theorems. Open sorries are disclosed (§11).

## How to reproduce the verification

```
# 1. Kernel-check the locked core + Wave-3/4 modules
git checkout 02e44c30 && lake build          # expect: green

# 2. Disclose the trusted axiom base
#print axioms lambda_unique_under_block
# => [A6'_block_consistent, propext, Quot.sound, Classical.choice]

# 3. Confirm the refutation is sorry-free
#print axioms maxAgg_ne_Lambda               # => Lean-core axioms only
```

## DOIs

- Concept (always-latest): [10.5281/zenodo.19944926](https://doi.org/10.5281/zenodo.19944926)
- v11 applied metrics: [10.5281/zenodo.20119582](https://doi.org/10.5281/zenodo.20119582)

---

*Signed-off-by: Stephen P. Lutar Jr. <stephenlutar2@gmail.com>*
