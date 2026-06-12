# Experimental machine-checked Lean theorems (NOT locked-8)

**Status: EXPERIMENTAL.** Honest index of recently merged, lake-verified Lean
backbones that are **not** part of the locked set and are **not** injected into
the auto-generated `VERIFIED_THEOREMS.md` (that artifact stays auto-generated so
the honesty gate is never weakened).

## What "locked-8" means (unchanged)
The locked set is **exactly 8** kernel-gated formula theorems —
{F1, F4, F7, F11, F12, F18, F19, F22} — pinned at lutar-lean `c7c0ba17`.
Nothing on this page changes that count. The Λ-aggregator uniqueness result
remains **Conjecture 1 (OPEN)**; the backbones below are PROPOSED engineering
gates, not a discharge of it.

## Experimental backbones merged to lutar-lean `main`
Each is machine-checked by the Lean kernel via `lake` on lutar-lean `main`
(CI green). Per the merge records they carry **no `sorry`** and add **no new
axioms** beyond the core allowlist; each is tagged in `EXPERIMENTAL_SCOPES`, so
the locked count stays exactly 8.

| Domain | Lean file | PR | Merge commit | Tier |
|---|---|---|---|---|
| Allodial AI — order-theoretic backbone (𝒜-score / DCI / lattice / non-interference) | `Lutar/Allodial.lean` | [#229](https://github.com/szl-holdings/lutar-lean/pull/229) | `783a38d0` | EXPERIMENTAL |
| Entanglement — coherence→entanglement capacity bound | `Lutar/Entanglement.lean` | [#230](https://github.com/szl-holdings/lutar-lean/pull/230) | `7b344e11` | EXPERIMENTAL |
| Neuroplasticity — critical-period + BCM plasticity properties | `Lutar/Neuroplasticity.lean` | [#231](https://github.com/szl-holdings/lutar-lean/pull/231) | `9a0dcc77` | EXPERIMENTAL |

## Honesty boundary
- These are **machine-checked** (kernel-verified) but **experimental-tier**: they
  are PROPOSED backbones for their domains, not locked formula theorems and not
  formal Λ results.
- They are deliberately **excluded** from the auto-generated locked-theorem list.
- Verify independently: `lake build` the files above on lutar-lean `main`.
