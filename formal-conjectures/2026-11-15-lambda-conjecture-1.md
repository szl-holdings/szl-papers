# Formal Conjectures statement record — Λ (Conjecture 1)

**Benchmark format:** google-deepmind/formal-conjectures
([arXiv:2605.13171](https://arxiv.org/abs/2605.13171)) — statement-record style
adopted here for the estate's flagship conjecture. This file is the
benchmark-format PUBLICATION of Λ as stated in thesis v23 §4
(thesis/v23/main.md); the machine-checked formalizations live in-tree in
szl-holdings/lutar-lean and are cited below with their honest status.

## Statement

**Conjecture 1 (Λ, unconditional form).** Let Φ : [0,1]^k → [0,1] be a trust
aggregator satisfying the governance axioms

- **A1 (Monotonicity)** — increasing any sub-score does not decrease the verdict;
- **A2 (Positive homogeneity)** — Φ(λx) = λΦ(x) for λ > 0;
- **A3 (Idempotence)** — Φ(c,…,c) = c;
- **A4 (Boundedness)** — Φ(x) ≤ max_i x_i;
- **A5 (Permutation-invariance)** — the verdict is anonymous in the sub-scores.

Then Φ = Λ, where Λ_k(x) = (∏_{i=1}^k x_i)^{1/k} is the equal-weight
geometric mean (the Lutar invariant).

## Status (honest, machine-checked where claimed)

**REFUTED (unconditionally).** The max aggregator maxAgg(x) = max_i x_i
satisfies A1–A5 but ≠ Λ; witness x = (0.8, 0.2): Λ = 0.4, maxAgg = 0.8
(rescaled Nat-permille witness (4,1): Λ = 2, maxAgg = 4). Machine-checked,
sorry-free, decide-checked: lutar-lean `Lutar/Round13/Lambda_Uniqueness.lean`
(theorems `maxAgg_ne_Lambda`, `unconditional_lambda_is_false`). Λ therefore
remains **Conjecture 1** unconditionally — never a theorem.

**PROVEN (conditionally, under a single declared axiom).** Adding

- **A6′ (Block-consistency)** — the verdict is invariant to how the auditor
  partitions evidence into review blocks (aggregation-invariance,
  [Csátó 2018]; Kolmogorov 1930 decomposability)

pins Λ uniquely: lutar-lean `Lutar/Wave4/LambdaBlockConsistency.lean`,
theorem `lambda_unique_under_block`, CI-green, `#print axioms` ⇒
[A6'_block_consistent, propext, Quot.sound, Classical.choice]. Non-vacuity:
`lambda_factors` (axiom-free). A weaker published characterization on the
quasi-arithmetic class — reciprocity + positive homogeneity
([Aczél–Saaty 1983], doi:10.1016/0022-2496(83)90028-7) — is recorded as
`A6''_reciprocity_homogeneity` in the same file.

**OPEN (the frontier this record submits to the benchmark).** On the full
aggregator class (not restricted to quasi-arithmetic means), what is the
WEAKEST natural axiom that, added to {A1–A5}, pins Λ? The in-tree axiom
ladder runs A6_bisymmetric (strongest; packages the conclusion) →
A6′_block_consistent (governance-natural) → A6″_reciprocity+homogeneity
(quasi-arithmetic class only). Whether a single axiom strictly weaker than
A6′ suffices on the unrestricted class is open. A second open residual:
independence of A6′ from {A1–A5} on the unrestricted class in the precise
sense needed for minimality.

## Metadata

- **Author:** Stephen P. Lutar (SZL Holdings), ORCID 0009-0001-0110-4173
- **Source paper:** thesis v23 (in-tree, thesis/v23/main.md), §4
- **Formalization repo:** szl-holdings/lutar-lean (locked kernel c7c0ba17;
  Wave-4 experimental scope, NOT folded into the locked v11 baseline)
- **Axiom disclosure:** every conditional theorem's `#print axioms` is in-tree
- **Upstream submission note:** contributing this statement upstream to
  google-deepmind/formal-conjectures requires their Mathlib-based build and
  review; owner-gated before any external submission in the estate's name.

## References

- Formal Conjectures benchmark: https://github.com/google-deepmind/formal-conjectures
- L. Csató, "Characterization of the row geometric mean ranking with a
  single parameter" (2018) — aggregation-invariance / block-consistency.
- J. Aczél, T. L. Saaty, "Procedures for synthesizing ratio judgements,"
  J. Math. Psychology 27 (1983) 93–102.
- A. N. Kolmogorov, "Sur la notion de la moyenne" (1930) — decomposability.
- Grabisch, Marichal, Mesiar, Pap, "Aggregation Functions" (CUP 2009) —
  conjunctive aggregator axiomatics (the deny-by-default dual result,
  Lutar/Wave8/MinGate.lean, proves the pointwise MIN is the unique
  deny-by-default aggregator — the complementary positive uniqueness).
