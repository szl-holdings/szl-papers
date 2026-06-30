<!--
  szl-papers README — investor-readable rewrite · 2026-06-30
  Honesty doctrine LOCKED. Sign-off: Stephen Lutar <stephenlutar2@gmail.com>
  DCO + Conventional Commits.
-->

# SZL Papers

**The published research behind SZL's governance math** — preprints, thesis lineage, open bounty problems, and prior-art disclosures.

[![Doctrine v11 LOCKED](https://img.shields.io/badge/Doctrine-v11_LOCKED-d4a444.svg)](https://github.com/szl-holdings/lutar-lean)
[![Concept DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.19944926-01696F.svg)](https://doi.org/10.5281/zenodo.19944926)
[![Λ Conjecture 1](https://img.shields.io/badge/%CE%9B-Conjecture_1_%C2%B7_Theorem_U_conditional-B79BD6.svg)](https://github.com/szl-holdings/lutar-lean/blob/main/BOUNTY.md)
[![SLSA L1](https://img.shields.io/badge/SLSA-L1_honest-green.svg)](https://slsa.dev)
[![DCO](https://img.shields.io/badge/DCO-required-orange.svg)](https://developercertificate.org)

---

## What this is

Every claim SZL makes about AI governance traces to a versioned, machine-checked source. This repository is that paper trail: the preprints, thesis versions, and open problems that underpin the proof backbone.

The core thesis has 26 versions (v1 through v26), each DOI-pinned to Zenodo. The always-current concept DOI is **[10.5281/zenodo.19944926](https://doi.org/10.5281/zenodo.19944926)**.

---

## Contents

| Directory | What it is |
|---|---|
| [`preprints/puriq/`](preprints/puriq/) | PURIQ preprint — formal specification of the Λ trust aggregator |
| [`thesis/ouroboros/`](thesis/ouroboros/) | Ouroboros thesis — the full governance substrate, 26 versions |
| [`bounty/`](bounty/) | Open mathematical challenges — prove (or disprove) Conjecture 1 |
| [`prior-art/`](prior-art/) | Prior-art disclosures for IP protection |

---

## The thesis in brief

SZL's core thesis: AI governance should produce **cryptographic receipts** — not dashboards — and the trust math behind those receipts should be **machine-checked in a proof kernel**, not claimed in marketing copy.

**Latest version:** v26 — *Governed Post-Determinism (GPD), Locked-Eight Edition*

Key milestones:
- **8 formulas locked-proven** (kernel `c7c0ba17`): receipt replay, DAG acyclicity, FIFO ordering, ledger conservation, bounded coupling, Reed–Solomon recovery, entropy budget, append-only monotonicity.
- **~185 theorems** machine-checked across Waves 11–23 (CI-green, not in the locked 8).
- **Λ uniqueness:** Conditional uniqueness proven axiom-free (Theorem U). Unconditional uniqueness is **Conjecture 1** — machine-checked false. We found the counterexample and publish it.
- **Open bounty:** Prove or constructively disprove Theorem U under weaker conditions. See [`bounty/`](bounty/).

Full proof library and commit history: **[szl-holdings/lutar-lean](https://github.com/szl-holdings/lutar-lean)**

---

## Honest proof status

| Tier | Count | What it means |
|---|---|---|
| **LOCKED-proven** | **8** — F1, F4, F7, F11, F12, F18, F19, F22 | Kernel-verified, no proof gaps, Lean-core axioms only. Never inflated. |
| **Machine-checked (experimental)** | ~185 | CI-green across Waves 11–23. Real work, honest stage. Not in the locked count. |
| **Conjectures** | 2 | Λ uniqueness (Conjecture 1) and Khipu BFT safety (Conjecture 2). Stated honestly; not claimed as proven. |

---

## Cite this work

```bibtex
@misc{szl2026governed,
  title  = {Governed Post-Determinism: A Proof-Backed Substrate for Consequential AI},
  author = {Lutar, Stephen P.},
  year   = {2026},
  doi    = {10.5281/zenodo.19944926},
  url    = {https://doi.org/10.5281/zenodo.19944926}
}
```

---

**[SZL Holdings](https://a-11-oy.com)** · Apache-2.0 code · CC BY 4.0 papers · Concept DOI [10.5281/zenodo.19944926](https://doi.org/10.5281/zenodo.19944926)

<sub>No production ATO claimed · SLSA L1 honest · Λ = Conjecture 1 · Not affiliated with Defense Unicorns</sub>
