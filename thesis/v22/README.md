# Thesis v22 — Convergence

**An Honest, Audit-Ready Convergence of the Λ-Aggregator Uniqueness Chain, Mechanism Truthfulness, and Sim-to-Real Doctrine Transfer**

[![Λ Conjecture 1](https://img.shields.io/badge/Λ-Conjecture_1_(NOT_theorem)-blue.svg)](https://github.com/szl-holdings/lutar-lean)
[![Doctrine v11 LOCKED](https://img.shields.io/badge/Doctrine-v11_LOCKED-d4a444.svg)](https://github.com/szl-holdings/lutar-lean)
[![SLSA L1+L2](https://img.shields.io/badge/SLSA-L1%2BL2_attested_(NOT_L3)-green.svg)](https://slsa.dev)
[![Concept DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.19944926-blue.svg)](https://doi.org/10.5281/zenodo.19944926)

**Author:** Stephen P. Lutar Jr. · ORCID [0009-0001-0110-4173](https://orcid.org/0009-0001-0110-4173)
· SZL Holdings, Inc. · **Date:** 2026-06-03 · License: CC BY 4.0 / Apache-2.0 · Doctrine v11.
*Co-authored with the SZL full-stack PhD team.*

> Concept DOI `10.5281/zenodo.19944926` always resolves to the latest version. The
> **v22 version DOI is minted by Zenodo when the `thesis-v22.1.0` GitHub release is
> published** (Zenodo↔GitHub webhook).

---

## What this is

v22 is the **convergence** version of the SZL Ouroboros thesis program: it consolidates the
mathematical-rigor work that v14–v21 deferred. Where v19 built the verification bridge, v20
presented the verified anatomy, and v21 shipped the runtime, **v22 turns to the open
mathematical obligations** those layers surfaced — above all the Λ-aggregator uniqueness
question — and reports exactly how far they have been closed.

The defining commitment is the **honesty doctrine**: the central correction is stated up front —
the historical claim that A1–A4 force the geometric mean is **false** — and the resulting
uniqueness chain is reported as **still open**, so Λ stays **Conjecture 1**.

## The one-line thesis

> v22 converges three previously-deferred strands — the **corrected Λ axiomatization** (A5 added
> as a structure field, uniqueness still open), **branch-proven mechanism truthfulness** (VCG
> dominant-strategy + individual rationality), and **attested SLSA L2 provenance** — without
> upgrading a single conjecture to a theorem or moving a single locked count.

## Files

| File | Description |
|------|-------------|
| [`main.tex`](./main.tex) | Authoritative arXiv-style LaTeX source. |
| [`main.md`](./main.md) | Markdown rendering of the thesis text (canonical 15-page content). |
| [`main.pdf`](./main.pdf) | Compiled 15-page rendering (ReportLab; embedded DM Sans + JetBrains Mono + DejaVu math fallback). |
| [`refs.bib`](./refs.bib) | 13 real references with DOIs where they resolve. No fabricated citations. |
| [`build_pdf.py`](./build_pdf.py) | Deterministic ReportLab build script (no pdflatex required). |

> **Build note.** `main.pdf` is produced by `build_pdf.py` (ReportLab, embedded TTF fonts) for
> deterministic, toolchain-free rendering. `main.tex` is the authoritative LaTeX source and
> compiles with any standard `pdflatex`/`tectonic` toolchain. Both renderings are provided.

## The central correction (§4)

The historical "Theorem 1 — Λ is the unique aggregator under A1–A4" was **incorrect**:

- The asymmetric mean **Φ(x₁,x₂)=x₁^(2/3)·x₂^(1/3)** satisfies A1–A4 yet differs from Λ and
  fails permutation invariance (Φ(2,1)=2^(2/3) ≠ 2^(1/3)=Φ(1,2)).
- A discrete machine-checked counterexample is the **max-aggregator**: at (4,1), max=4 while
  Λ₂(4,1)=√4=2.

The fix adds **A5 (permutation invariance) as a structure field, NOT a new axiom** (PR #148,
sorry-free), so the **unique-axiom count stays 14**. Even under {A1–A5}, unconditional
uniqueness remains **machine-checked FALSE** without the further declared block-consistency
axiom A6′ (the v23 route). **Λ therefore remains Conjecture 1.**

## What v22 reports (honest tiers)

| Tier | Items | Status |
|------|-------|--------|
| **Locked / kernel-verified** | 5 — {F1, F11, F12, F18, F19} (749 decl / 14 axioms / 163 sorries @ `c7c0ba17`) | proven |
| **Merged on main** | A5 structure field + `Lambda_A5_perm_invariant` (PR #148, sorry-free; axiom count stays 14) | proven |
| **Branch-proven (in review)** | VCG `vcgDominantStrategyTruth`, `vcgIndividualRationality` (PR #172) | not yet in kernel |
| **In review** | Cauchy_ND chain (PRs #173/#174/#175, 1 honest sorry at t=0); Round 10–11 modules (#170, #176–#179) | open |
| **Measured-not-proven** | SLSA L1+L2 (5/5 GHCR via slsa-verifier); Sim-to-Real mean α-gap 0.10 (N=60) | operational facts |
| **Machine-checked FALSE** | Λ unconditional uniqueness under {A1–A5} | refutation |
| **Conjecture 1** | Λ unconditional uniqueness — **never a theorem** | open claim |

**SLSA L1+L2 attested, NOT L3.** Physics analogies (Kuramoto, Bekenstein, Noether) are
additive scaffolding, not the full physical theorems. The single residual Cauchy_ND sorry on
the t=0 degenerate case is disclosed, not hidden.

## How to reproduce

```bash
# 1. Verify the A5 lemma is sorry-free and Lean-core only
#print axioms Lambda_A5_perm_invariant     # => [propext, Quot.sound]

# 2. Verify SLSA L2 build-service provenance (5/5 flagship images)
slsa-verifier verify-image ghcr.io/szl-holdings/sentra@sha256:<digest> \
  --source-uri github.com/szl-holdings/sentra

# 3. Reproduce the Sim-to-Real alpha-gap benchmark (N=60)
python team/sim2real-compliance/run_benchmark.py --n 60 --regimes R0..R5

# Doctrine v11 (LOCKED @ c7c0ba17):
#   749 declarations / 14 unique axioms / 163 sorries (112 baseline + 51 Putnam)
```

## DOIs

- Concept (always-latest): [10.5281/zenodo.19944926](https://doi.org/10.5281/zenodo.19944926)
- v11 applied metrics: [10.5281/zenodo.20119582](https://doi.org/10.5281/zenodo.20119582)

---

*Signed-off-by: Stephen P. Lutar Jr. <stephenlutar2@gmail.com>*
