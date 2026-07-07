<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# drafts/ — publication-ready thesis drafts

Two draft papers, honesty-labelled per **Doctrine v11** (locked-8 {F1,F4,F7,F11,F12,F18,F19,F22}
@ `c7c0ba17`, 749/14/163; `locked_count_eight` by `decide`). **Λ = Conjecture 1** — unconditional
uniqueness is machine-checked FALSE; only conditional **Theorem U** is proven, axiom-free. Nothing in
these drafts upgrades a conjecture to a theorem, and neither claims a result that is not either
(a) locked in the kernel, (b) an experimental CI-green in-tree theorem, or (c) an explicitly-labelled
*proposal*.

| File | Title | Target venue | Status |
|------|-------|--------------|--------|
| [`lambda-uniqueness-counterexample-note.md`](lambda-uniqueness-counterexample-note.md) | A Machine-Checked Counterexample to Unconditional Uniqueness of the Λ Trust Aggregator, and an Axiom-Free Conditional Uniqueness Theorem | arXiv `cs.LO` (x-list `cs.AI`, `math.CA`) | Draft — not posted |
| [`doubly-verified-receipt.md`](doubly-verified-receipt.md) | Doubly-Verified Receipts: A Lean Theorem that Consumes an α,β-CROWN Robustness Certificate and Binds Model-Verification SOTA to a Governance Kernel | CAV / ITP (arXiv `cs.LO`, x-list `cs.CR`, `cs.LG`) | Draft — proposal / schema |

**Honesty scope of each draft.**

- *Counterexample note*: states Conjecture 1 (unconditional Λ-uniqueness) is **machine-checked FALSE**
  as literally stated (`maxAgg_ne_Lambda`; `min` second witness), gives the explicit `(4,1)` witness,
  and proves **Theorem U** (`lambda_unique_of_separable`) axiom-free under {A1,A2,A3,A5} +
  slice-multiplicativity. Discloses the open `CAUCHY_ND` residual and the refined open conjecture.
- *Doubly-verified receipt*: a **proposal** — a Lean theorem *schema* that *consumes* an α,β-CROWN
  certificate as a hypothesis (does not re-prove the verifier) and binds it to the governance kernel
  via in-toto/SLSA + Sigstore. Explicitly discloses verifier-soundness as an assumption (SoundnessBench),
  the fp/determinism caveat, and that the theorem is not part of the locked-8.

All external references were URL-checked. Author: Stephen P. Lutar Jr.
(ORCID [0009-0001-0110-4173](https://orcid.org/0009-0001-0110-4173)). Concept DOI
[10.5281/zenodo.19944926](https://doi.org/10.5281/zenodo.19944926).
