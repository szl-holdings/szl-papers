# Thesis v24.1 — Axiom-Free Conditional Uniqueness of the Lutar Invariant

**A Machine-Verified Trust Foundation for Governed Agentic AI**

[![Λ Conjecture 1](https://img.shields.io/badge/Λ-Conjecture_1_(NOT_theorem)-blue.svg)](https://github.com/szl-holdings/lutar-lean)
[![CUT-2 axiom-free](https://img.shields.io/badge/CUT--2-axiom--free_conditional_uniqueness-success.svg)](https://github.com/szl-holdings/lutar-lean)
[![CUT-1 closed on hypotheses](https://img.shields.io/badge/CUT--1-representation_closed_on_stated_hypotheses-success.svg)](https://github.com/szl-holdings/lutar-lean)
[![Doctrine v11 LOCKED](https://img.shields.io/badge/Doctrine-v11_LOCKED-d4a444.svg)](https://github.com/szl-holdings/lutar-lean)
[![SLSA L1 honest · L2 attestation](https://img.shields.io/badge/SLSA-L1_honest_·_L2_build--attestation-green.svg)](https://slsa.dev)
[![Concept DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.19944926-blue.svg)](https://doi.org/10.5281/zenodo.19944926)

**Author:** Stephen P. Lutar Jr. · ORCID [0009-0001-0110-4173](https://orcid.org/0009-0001-0110-4173)
*Co-authored with the SZL full-stack PhD research collective.*

---

## What this is

v24.1 refreshes v24 of the SZL Ouroboros thesis program (v1–v24) to the **current** proof state: a
single, arXiv-style paper on a **machine-verified trust substrate** for governed agentic AI — the
**Ouroboros loop**, the **Lutar invariant Λ**, and a **proof-trail / receipt architecture**
formalized in Lean 4. Current `main` is pinned at `ba1050b7` (CI-green, Waves 11–22 merged).

## The v24 advance (the headline)

> In v23, the conditional uniqueness of Λ was gated on a **declared** project axiom (A6′
> block-consistency). v24 reports `Lutar.Round13.lambda_unique_of_separable`: under
> {A1, A2, A3, A5} together with **slice-multiplicativity (separability)**, Λ is the unique
> aggregator — with `#print axioms = {propext, Classical.choice, Quot.sound}`, i.e. **no project
> axiom**, kernel-clean, CI-green, present at `main` `ba1050b7` (originally merged at `b910c276`).
> The extra hypothesis is now a **checkable property of Φ** (weaker than the old `Factors`
> premise), discharged through Mathlib + already-proved in-tree lemmas. Replacing a *declared
> axiom* with a *checkable property* is an **epistemic upgrade**.

## The v24.1 advance: CUT-1 closed on its stated hypotheses

> **CUT-1 — the Aczél quasi-arithmetic *representation* theorem — is now fully closed on its
> stated, checkable hypotheses** across Waves 18–22:
> - **Wave 18** built the forward representation fragment (`generator_unique_up_to_affine`,
>   `expMidpoint`, `gen_continuous_of_denseRange`).
> - **Wave 19** supplied the Burai–Kiss–Szokol (BKS) density engine
>   (`false_of_uncountable_pairwiseDisjoint_Ioo`, `dyadic_image_dense`).
> - **Wave 20** added the supporting primitives.
> - **Wave 21** closed residual (B) — the perfect-set/uncountability step — via a monotone-extension
>   light route (`range_not_countable_of_strictMono`, `dyadic_image_dense_complete`).
> - **Wave 22** *derived* the (C-order) gap-shift ordering (BKS Fourth-step, arXiv:2208.07083
>   eqs 8–9) so it is **constructed, not assumed** (`gapShift_ordering`, `corder_gapshift`), and
>   produced `cut1_sharp_conditional_lambda`, which drops bisymmetry as redundant and drops
>   unit-normalization.
>
> The **conditional** Λ-uniqueness chain is now **axiom-clean end to end** on its stated checkable
> hypotheses: {A1–A5} + separability + slice-multiplicativity + slice-monotonicity. All Wave 18–22
> modules are `#print axioms`-clean (⊆ {propext, Classical.choice, Quot.sound}), no `sorry`, no new
> axiom; the numbers-drift baseline is **unchanged**.

**Crucially:** the **unconditional** uniqueness of Λ under {A1–A5} remains **machine-checked FALSE**
(`maxAgg_ne_Lambda`; `maxAgg` and `min` are A1–A5 counterexamples). **Λ stays Conjecture 1 —
never a theorem.** CUT-1 strengthens the *conditional* result; it does **not** make Λ
unconditional and never claims to.

## Files

| File | Description |
|------|-------------|
| `main.tex` | Authoritative arXiv-style LaTeX source. |
| `main.pdf` | Compiled 24-page PDF (tectonic 0.15.0). |
| `main.md`  | Faithful markdown rendering. |
| `refs.bib` | References with DOIs / arXiv IDs. |
| `.zenodo.json` | Zenodo deposition metadata (version 24.1.0). |
| `README.md`| This file. |

## Verification status (honest tiers)

| Tier | Items | Pin |
|------|-------|-----|
| **Locked / kernel-verified** | **5** — {F1, F11, F12, F18, F19} (749 decl / 14 axioms / 163 sorries) | `c7c0ba17` |
| **Headline — axiom-free, CI-green** | `lambda_unique_of_separable` (CUT-2): conditional Λ-uniqueness, `#print axioms` = core only | `ba1050b7` |
| **CUT-1 representation — closed on stated hypotheses, CI-green** | Aczél quasi-arithmetic representation (Waves 18–22); `cut1_sharp_conditional_lambda`; all `#print axioms`-clean | `ba1050b7` |
| **Machine-checked FALSE** | `maxAgg_ne_Lambda` — unconditional uniqueness refuted (Λ = Conjecture 1) | — |
| **Experimental · CI-green tier** (NEVER folded into locked-5) | ~185 kernel-clean theorems across Waves 11–22; drift baseline 1323 decl / 23 axioms (22 unique) / 307 sorries — unchanged; CF-13/17/22/23/24/25/26/27/28, Wave 13/14, CUT-1 (Waves 18–22) — all `#print axioms`-clean | `ba1050b7` |
| **Conjecture / open** | Λ unconditional (Conjecture 1); Byzantine BFT (Khipu Conjecture 2); DPO KL/Pinsker (false-as-stated; CF-22 gives conditional simplex-only repair) | — |

## Honesty doctrine (binding)

- Locked-proven = **exactly five** {F1, F11, F12, F18, F19} at `c7c0ba17`. Nothing else is "locked."
- Λ is **Conjecture 1** unconditionally; only **conditional** uniqueness is proven (now axiom-free).
- "CUT-1 fully closed on its stated hypotheses" means the quasi-arithmetic **representation**
  theorem is complete and it **strengthens the conditional** Λ-uniqueness result. It does **not**
  make Λ unconditional; the unconditional conjecture stays open/false.
- The experimental CI-green tier (~185 thms) is **separate** and is never folded into the locked-5.
- Supply-chain posture: **SLSA L1 honest, L2 build-attestation present** — L2-verified, L3,
  FedRAMP, Iron Bank, and CMMC remain **roadmap**.
- Declared axioms disclosed; 0 runtime CDN; nothing fabricated; no fake citations.

## Verify it yourself

```bash
git clone https://github.com/szl-holdings/lutar-lean && cd lutar-lean
git checkout ba1050b7
lake exe cache get && lake build                       # whole library, CI-green
lake env lean -e '#print axioms Lutar.Round13.lambda_unique_of_separable'
# => {propext, Classical.choice, Quot.sound}  (no project axiom)
lake env lean -e '#print axioms maxAgg_ne_Lambda'      # unconditional claim refuted
```

## Cite

DOI (this version): minted on GitHub Release `thesis-v24.1.0` via the Zenodo integration.
Concept DOI (always-latest): [10.5281/zenodo.19944926](https://doi.org/10.5281/zenodo.19944926).
