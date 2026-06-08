# Thesis v24 — Axiom-Free Conditional Uniqueness of the Lutar Invariant

**A Machine-Verified Trust Foundation for Governed Agentic AI**

[![Λ Conjecture 1](https://img.shields.io/badge/Λ-Conjecture_1_(NOT_theorem)-blue.svg)](https://github.com/szl-holdings/lutar-lean)
[![CUT-2 axiom-free](https://img.shields.io/badge/CUT--2-axiom--free_conditional_uniqueness-success.svg)](https://github.com/szl-holdings/lutar-lean)
[![Doctrine v11 LOCKED](https://img.shields.io/badge/Doctrine-v11_LOCKED-d4a444.svg)](https://github.com/szl-holdings/lutar-lean)
[![SLSA L1 honest · L2 roadmap](https://img.shields.io/badge/SLSA-L1_honest_·_L2_roadmap-green.svg)](https://slsa.dev)
[![Concept DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.19944926-blue.svg)](https://doi.org/10.5281/zenodo.19944926)

**Author:** Stephen P. Lutar Jr. · ORCID [0009-0001-0110-4173](https://orcid.org/0009-0001-0110-4173)
*Co-authored with the SZL full-stack PhD research collective.*

---

## What this is

v24 is the next version of the SZL Ouroboros thesis program (v1–v23): a single, arXiv-style paper
(20 pages) on a **machine-verified trust substrate** for governed agentic AI — the **Ouroboros
loop**, the **Lutar invariant Λ**, and a **proof-trail / receipt architecture** formalized in Lean 4.

## The v24 advance (the headline)

> In v23, the conditional uniqueness of Λ was gated on a **declared** project axiom (A6′
> block-consistency). v24 reports `Lutar.Round13.lambda_unique_of_separable`: under
> {A1, A2, A3, A5} together with **slice-multiplicativity (separability)**, Λ is the unique
> aggregator — with `#print axioms = {propext, Classical.choice, Quot.sound}`, i.e. **no project
> axiom**, kernel-clean, CI-green, merged to `main` at `b910c276`. The extra hypothesis is now a
> **checkable property of Φ** (weaker than the old `Factors` premise), discharged through Mathlib +
> already-proved in-tree lemmas. Replacing a *declared axiom* with a *checkable property* is an
> **epistemic upgrade**.

**Crucially:** the **unconditional** uniqueness of Λ under {A1–A5} remains **machine-checked FALSE**
(`maxAgg_ne_Lambda`; `maxAgg` and `min` are A1–A5 counterexamples). **Λ stays Conjecture 1 —
never a theorem.**

## Files

| File | Description |
|------|-------------|
| `main.tex` | Authoritative arXiv-style LaTeX source. |
| `main.pdf` | Compiled 20-page PDF (tectonic; 0 overfull boxes, 0 undefined refs). |
| `main.md`  | Faithful markdown rendering. |
| `refs.bib` | References with DOIs / arXiv IDs. |
| `README.md`| This file. |

## Verification status (honest tiers)

| Tier | Items | Pin |
|------|-------|-----|
| **Locked / kernel-verified** | **5** — {F1, F11, F12, F18, F19} (749 decl / 14 axioms / 163 sorries) | `c7c0ba17` |
| **Headline — axiom-free, CI-green** | `lambda_unique_of_separable` (CUT-2): conditional Λ-uniqueness, `#print axioms` = core only | `b910c276` |
| **Machine-checked FALSE** | `maxAgg_ne_Lambda` — unconditional uniqueness refuted (Λ = Conjecture 1) | — |
| **Experimental · CI-green tier** (NEVER folded into locked-5) | 1323 decl / 23 axioms (22 unique) / 307 sorries; CF-13, CF-17, Wave-13, Wave-14 (CF-18/19/20/21) — all `#print axioms`-clean | `b910c276` |
| **Conjecture / open** | Λ unconditional (Conjecture 1); Byzantine BFT (Khipu Conjecture 2); DPO KL/Pinsker (false-as-stated) | — |

## Honesty doctrine (binding)

- Locked-proven = **exactly five** {F1, F11, F12, F18, F19}. Nothing else is "locked."
- Λ is **Conjecture 1** unconditionally; only **conditional** uniqueness is proven (now axiom-free).
- Supply-chain posture: **SLSA L1 honest, L2 roadmap** — *not* L2-verified, L3, FedRAMP, Iron Bank, or CMMC. (Corrects a v23 README badge overstatement.)
- Declared axioms disclosed; 0 runtime CDN; nothing fabricated; no fake citations.

## Verify it yourself

```bash
git clone https://github.com/szl-holdings/lutar-lean && cd lutar-lean
lake exe cache get && lake build                       # whole library, CI-green
lake env lean -e '#print axioms Lutar.Round13.lambda_unique_of_separable'
# => {propext, Classical.choice, Quot.sound}  (no project axiom)
```

## Cite

DOI (this version): minted on GitHub Release `thesis-v24.0.0` via the Zenodo integration.
Concept DOI (always-latest): [10.5281/zenodo.19944926](https://doi.org/10.5281/zenodo.19944926).
