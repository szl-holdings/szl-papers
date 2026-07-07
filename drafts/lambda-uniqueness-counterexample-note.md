<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- SZL Holdings — Draft research note · target arXiv cs.LO -->

# A Machine-Checked Counterexample to Unconditional Uniqueness of the Λ Trust Aggregator, and an Axiom-Free Conditional Uniqueness Theorem

**Draft research note — target: arXiv `cs.LO` (cross-list `cs.AI`, `math.CA`).**

**Author.** Stephen P. Lutar Jr. — SZL Holdings.
ORCID: [0009-0001-0110-4173](https://orcid.org/0009-0001-0110-4173).

**Concept DOI (always-latest):** [10.5281/zenodo.19944926](https://doi.org/10.5281/zenodo.19944926).

**Artifacts.** Lean 4 kernel: [`szl-holdings/lutar-lean`](https://github.com/szl-holdings/lutar-lean), locked at commit
`c7c0ba17` (749 declarations / 14 unique axioms / 163 sorries). Bounty / open-problem intake:
[`szl-holdings/lambda-bounty`](https://github.com/szl-holdings/lambda-bounty).

> **Honesty banner (binding, verbatim across SZL artifacts).** The Λ aggregator's *unconditional*
> uniqueness under the stated axioms is **Conjecture 1** — it is **not** a theorem, and as literally
> stated it is **machine-checked FALSE** (see §4). Only a **conditional** uniqueness result
> (**Theorem U**, §5) is proven, and it is proven **axiom-free** — its trusted base is exactly the
> Lean core `{propext, Classical.choice, Quot.sound}`. Λ is never rendered "green." This note claims
> nothing beyond those two facts.

---

## Abstract

The Λ ("Lutar") invariant is an equal-weight geometric-mean trust aggregator,
\( \Lambda_k(x) = \bigl(\prod_{i=1}^{k} x_i\bigr)^{1/k} \), used as the apex trust gate of a
governance kernel whose properties are machine-checked in Lean 4. A natural and attractive claim is
that a short list of order-theoretic axioms — monotonicity, positive homogeneity, idempotence, and
permutation-invariance (plus a max/min boundedness axiom) — pins \(\Lambda_k\) down *uniquely*. We
report, honestly, that this claim is **false as stated**: we exhibit an explicit, machine-checked
counterexample (the maximum aggregator \(\max_i x_i\), with the minimum aggregator as a second
witness) that satisfies every one of the stated axioms yet differs from \(\Lambda_k\). Accordingly we
retain the label **Conjecture 1** for *unconditional* uniqueness and never upgrade it to a theorem.
We then prove what *is* true: a **conditional** uniqueness theorem (**Theorem U**,
`Lutar.Round13.lambda_unique_of_separable`) showing that any aggregator satisfying the axioms *and* a
checkable structural property — *slice-multiplicativity* (separability) — must equal \(\Lambda_k\).
Theorem U is proven **axiom-free**: `#print axioms` reports only the Lean core. We give the exact
hypotheses, the explicit counterexample, the boundary between them (the "cancellative cone"), and a
precise statement of what remains open. The scientific point of this note is calibration: publishing
the refutation of our own headline conjecture is what makes the conditional theorem credible.

**Keywords.** trust aggregation, geometric mean, functional-equation uniqueness, quasi-arithmetic
means, Lean 4, Mathlib, machine-checked counterexample, `#print axioms`, AI governance.

---

## 1. Introduction

Governed deployment of agentic AI requires *checkable* trust verdicts, not dashboards. The SZL
governance kernel collapses a vector of per-axis trust scores into a single scalar via the Λ
aggregator, the equal-weight geometric mean
\[
  \Lambda_k(x) \;=\; \Bigl(\textstyle\prod_{i=1}^{k} x_i\Bigr)^{1/k}, \qquad x \in [0,1]^k,
\]
whose one defining behavior is *weakest-link / zero-absorption*: a single fully-failed axis
(\(x_i = 0\)) vetoes trust (\(\Lambda_k = 0\)). Geometric-mean aggregators are classical in
multi-criteria decision analysis; we do not claim the functional form is novel. What we do claim, and
formalize in Lean 4, is a specific *uniqueness characterization program* plus a strict honesty
discipline about which parts of it are proven.

The tempting headline is: "the four (or five) natural axioms pin Λ down uniquely." That headline is
**Conjecture 1** of the program. This note does three things, in order of importance:

1. **States, without softening, that Conjecture 1 is false as literally stated**, and gives the
   explicit machine-checked counterexample (§4).
2. **Proves the conditional replacement (Theorem U)** — uniqueness on the slice-multiplicative
   (cancellative) class — *axiom-free*, with the exact hypotheses (§5).
3. **Delimits precisely what remains open** (§6): the refined governance-relevant conjecture, and the
   status of a fully machine-checked *unconditional-under-added-structure* proof.

We regard publishing (1) as a credibility asset, not a defect. A weakness converted into a precise,
machine-checked negative result is stronger science than an unfalsifiable claim of uniqueness. This
posture aligns with the classical view of mathematics as a discipline of proofs *and* refutations
([Lakatos, 1976](https://doi.org/10.1017/CBO9781139171472)).

### 1.1 Honesty tiers used in this note

Every claim below is tagged with exactly one tier:

- **[locked / kernel-verified]** — proven in Lean 4, sorry-free, trusted base `{propext,
  Classical.choice, Quot.sound}`, pinned at `c7c0ba17`, part of the *locked* count.
- **[experimental · axiom-free · CI-green]** — proven sorry-free with only the Lean core, CI-green at
  the recorded commit, but **never folded into the locked count**.
- **[machine-checked FALSE]** — the statement is *refuted* by a machine-checked counterexample.
- **[Conjecture — NOT a theorem]** — a research hypothesis; explicitly not proven.

The locked kernel proves **exactly eight** governance formulas {F1, F4, F7, F11, F12, F18, F19, F22},
sorry-free, at `c7c0ba17` (749/14/163), and the fact that there are *exactly eight* is itself a Lean
theorem (`locked_count_eight`, discharged by `decide`). Λ-uniqueness is **not** among them.

---

## 2. The Λ aggregator and the candidate class

**Definition 2.1 (Λ).** For \(x \in [0,1]^k\), \(\Lambda_k(x) = \bigl(\prod_{i=1}^{k} x_i\bigr)^{1/k}\).
On the ratio scale (\(x \in \mathbb{R}_{\ge 0}^k\)) the same formula applies.

The candidate aggregators are functions \(\Phi : \mathbb{R}_{\ge 0}^k \to \mathbb{R}_{\ge 0}\)
constrained by the following axioms. We list five (the Lean development uses A1–A5); the bounty's
public statement uses the four essential ones {A1, A2, A3, A5} plus zero-absorption. Both are refuted
by the same witness.

| Axiom | Name | Statement |
|------:|------|-----------|
| **A1** | Monotonicity | \(x \le y\) pointwise \(\Rightarrow \Phi(x) \le \Phi(y)\). |
| **A2** | Positive homogeneity | \(\Phi(c\,x) = c\,\Phi(x)\) for \(c > 0\). |
| **A3** | Idempotence / diagonal | \(\Phi(c,\dots,c) = c\). |
| **A4** | Boundedness | \(\min_i x_i \le \Phi(x) \le \max_i x_i\). |
| **A5** | Permutation-invariance | \(\Phi\) is symmetric in its arguments. |

\(\Lambda_k\) satisfies all five (each proven in-tree; e.g. homogeneity by
`Finset.prod_mul_distrib` + `NNReal.mul_rpow`, idempotence by the normalization lemma). The question
is whether A1–A5 (or the four-axiom subset) *force* \(\Phi = \Lambda_k\).

---

## 3. Conjecture 1, stated precisely

**Conjecture 1 (Λ-Aggregator Uniqueness — unconditional).** Any two aggregators \(\Phi_1, \Phi_2\)
satisfying A1–A5 agree on every input; equivalently, \(\Lambda_k\) is the unique aggregator satisfying
A1–A5.

In Lean, the target statement (the bounty artifact) is:

```lean
theorem lambda_aggregator_unique
    (Λ₁ Λ₂ : Aggregator)
    (h₁ : SatisfiesAxioms Λ₁) (h₂ : SatisfiesAxioms Λ₂) :
    ∀ x, Λ₁ x = Λ₂ x := by
  sorry  -- OPEN as stated; refuted by the §4 witness under the literal axiom set
```

**[Conjecture — NOT a theorem]** We label this **Conjecture 1** and never claim it proven. As the next
section shows, the *literal* statement is in fact **false**; "Conjecture 1" therefore survives only as
a *refined* open hypothesis (§6), never as the literal A1–A5 statement.

---

## 4. The counterexample: unconditional uniqueness is FALSE (machine-checked)

**Theorem 4.1 (Refutation of unconditional uniqueness).** *[machine-checked FALSE] [experimental ·
CI-green]* There exists \(\Phi \neq \Lambda_k\) satisfying A1–A5. Concretely, the **maximum
aggregator** \(\mathrm{maxAgg}(x) = \max_i x_i\) satisfies A1–A5 yet differs from \(\Lambda_k\).

**The witness.** Take \(k = 2\) and \(\mathrm{maxAgg}(x_0, x_1) = \max(x_0, x_1)\). It passes every
axiom:

- **A2 (homogeneous):** \(\max(c x_0, c x_1) = c \max(x_0, x_1)\).  *(`maxAgg_A2`, via `mul_sup`)*
- **A3 (idempotence):** \(\max(c, c) = c\).  *(`maxAgg_A3`, via `sup_idem`)*
- **A5 (symmetric):** \(\max(x_0, x_1) = \max(x_1, x_0)\).  *(`maxAgg_A5`, via `sup_comm`)*
- **A1 (monotone)** and **A4 (\(\le \max\))** hold by `sup` monotonicity and reflexivity.

Yet at the single point \(x = (4, 1)\):
\[
  \mathrm{maxAgg}(4, 1) = 4, \qquad \Lambda_2(4, 1) = (4 \cdot 1)^{1/2} = 2, \qquad 4 \neq 2.
\]
Hence \(\mathrm{maxAgg} \neq \Lambda_2\). A **second witness** is the minimum aggregator
\(\min_i x_i\) (the lower idempotent aggregator), which is likewise A1–A5-compliant and differs from
\(\Lambda_k\).

**Lean reference.** The in-tree witness is `Round13.maxAgg_ne_Lambda`; the separating evaluation at
\((4,1)\) is discharged by `decide`, and `#print axioms maxAgg_ne_Lambda` reports Lean-core axioms
only. The `min` companion is an analogous `decide`-checked term. This is not a failure to prove
uniqueness — it is a proof of its *negation* under the literal axiom set.

### 4.1 Why max and min evade uniqueness (the structural reason)

\(\max\) and \(\min\) are **idempotent** and **non-separable**: they cannot be written as a product
\(\prod_i x_i^{\alpha_i}\) for any exponents, because a product is *multiplicative across axes* while
\(\max/\min\) are not. They live *outside* the image of the factorization predicate `Factors`. The
geometric mean is *strictly internal* — it moves whenever any coordinate moves — whereas
\(\max(t, 1)\) is frozen at \(1\) for all \(t \le 1\). This is exactly the property captured by the
predicate `IsCancellative` (each axis-slice strictly increasing on the positives), and it is exactly
the property \(\max/\min\) fail. On the interior *cancellative cone* the geometric mean is unique
(§5); on the *idempotent boundary*, \(\max\) and \(\min\) coexist with it.

### 4.2 What the "missing axiom" would be (and why we do not add it)

The classical theory of means says the property that forces the quasi-arithmetic / geometric form is
**bisymmetry / associativity**
([Aczél, 1966](https://doi.org/10.1017/CBO9781139086578);
Kolmogorov 1930; Nagumo 1930;
[Hardy–Littlewood–Pólya, 1934, §2.18](https://archive.org/details/inequalities0000hard)):
\[
  \Phi\bigl(\Phi(x_{11}, x_{12}),\, \Phi(x_{21}, x_{22})\bigr)
  = \Phi\bigl(\Phi(x_{11}, x_{21}),\, \Phi(x_{12}, x_{22})\bigr).
\]
This would be an "A6." But \(\max/\min\) are *themselves* bisymmetric, so bisymmetry **alone** is not
the whole story: it is bisymmetry *together with* strict internality (cancellativity) that excludes
the idempotent boundary and lands on the geometric mean once homogeneity (A2) fixes the generator (cf.
regularity-free characterizations of quasi-arithmetic means,
[Burai–Kiss–Szokol, 2021](https://doi.org/10.1007/s10474-021-01185-z)).

**We deliberately do NOT add A6 as a project axiom.** Adding it would push the unique-axiom count from
14 to 15 and change the locked doctrine. Instead we *condition* the theorem on a checkable *property*
of \(\Phi\) — not an axiom — and prove Theorem U (§5). The axiom count stays **14**, and the
\(\max/\min\) witnesses remain the honest, machine-checked answer to the *unconditional* question:
**no**.

---

## 5. Theorem U: axiom-free conditional uniqueness

We now state what *is* proven. The key move replaces an unprovable idealization with a *checkable
structural property* of the candidate aggregator: **slice-multiplicativity** (separability).

**Definition 5.1 (slice-multiplicativity / separability).** \(\Phi : [0,1]^k \to [0,1]\) is
*slice-multiplicative* if there exist slice functions \(f_i : \mathbb{R}_{\ge 0} \to \mathbb{R}_{\ge 0}\)
such that
- **(sep)** \(\Phi(x) = \prod_{i} f_i(x_i)\),
- **(mul)** \(f_i(s t) = f_i(s)\, f_i(t)\),
- **(one)** \(f_i(1) = 1\),
- **(mono)** each \(f_i\) is monotone.

**Theorem U (axiom-free conditional uniqueness of Λ).** *[experimental · axiom-free · CI-green]* Let
\(k > 0\) and let \(\Phi\) satisfy the Lutar axioms {A1, A2, A3, A5}. If \(\Phi\) is
slice-multiplicative (Definition 5.1), then \(\Phi = \Lambda_k\).

The Lean term is `Lutar.Round13.lambda_unique_of_separable`; its trusted base is exactly
```
#print axioms lambda_unique_of_separable = {propext, Classical.choice, Quot.sound}
```
— **no project axiom**. It is kernel-clean and CI-green. The exact Lean signature:

```lean
theorem lambda_unique_of_separable {k : ℕ} (hk : 0 < k)
    (Φ : Aggregator k) (hL : LutarAxioms Φ)
    (f : Fin k → (NNReal → NNReal))
    (hsep  : ∀ x, Φ x = ∏ i, f i (x i))
    (hmul  : ∀ i s t, f i (s * t) = f i s * f i t)
    (hone  : ∀ i, f i 1 = 1)
    (hmono : ∀ i, Monotone (f i)) :
    Φ = Λ k
```

**Proof sketch (in-tree lemma chain).**

1. **Per-axis power law.** Each slice \(f_i\) is multiplicative (mul), monotone (mono), and normalized
   (one). The lemma `multiplicative_monotone_isPow_pos` yields an exponent \(\alpha_i\) with
   \(f_i(t) = t^{\alpha_i}\) for \(t \neq 0\). This is the multiplicative Cauchy functional equation on
   \(\mathbb{R}_{\ge 0}\): a monotone (hence, on the positives, continuous) multiplicative solution is
   a power function ([Cauchy, 1821](https://doi.org/10.1017/CBO9780511693328);
   [Aczél, 1966](https://doi.org/10.1017/CBO9781139086578), Thm 5.1). The boundary value
   \(f_i(0) = 0^{\alpha_i} = 0\) follows from the idempotent dichotomy (`slice_zero_idem`,
   `slice_const_one_of_zero_one`).
2. **Exponent equality across axes.** Symmetry (A5) forces the exponents equal: applying a swap
   \(\texttt{Equiv.swap}\ i\ j\) to a two-hot test vector and using injectivity
   (`rpow_left_inj_one_lt`: \(c^a = c^b \Rightarrow a = b\) for \(c > 1\)) gives \(\alpha_i = \alpha_j\).
3. **Assemble factorization.** The per-axis power laws yield \(\Phi(x) = \prod_i x_i^{\alpha_i}\) (the
   `Factors` predicate).
4. **Discharge.** Apply `lambda_unique_of_factors`; idempotence (A3) forces
   \(\sum_i \alpha_i = 1\) and symmetry (A5) forces all \(\alpha_i\) equal, whence
   \(\alpha_i = 1/k\) and \(\Phi = \Lambda_k\).

**Why this is an epistemic upgrade.** A prior route (v23) obtained conditional uniqueness *gated on a
declared project axiom* (A6′ block-consistency; `#print axioms` listed that non-core axiom). Theorem U
removes that gate: the added hypothesis is now a *property one can, in principle, check by inspecting
the definition of a concrete \(\Phi\)*, and the trusted base is the Lean core alone. Replacing a
declared axiom with a checkable property is a strict strengthening.

### 5.1 Worked sanity checks

- **Λ is slice-multiplicative** (antecedent non-vacuous). Take \(f_i(t) = t^{1/k}\): multiplicative,
  normalized (\(1^{1/k} = 1\)), monotone, and \(\prod_i t_i^{1/k} = \Lambda_k\).
- **maxAgg is not slice-multiplicative.** No product of per-axis slices reproduces \(\max\), consistent
  with \(\mathrm{maxAgg}\) being an A1–A5 counterexample *outside* the slice-multiplicative class.
- **Separation at \((4,1)\).** \(\mathrm{maxAgg}(4,1) = 4 \neq 2 = \Lambda_2(4,1)\) — the
  `decide`-checked witness of §4.

---

## 6. What remains open

We state the open problems precisely.

1. **Refined Conjecture 1 (governance-relevant).** *[Conjecture — NOT a theorem]* The literal A1–A5
   statement is refuted (§4). What survives is the *refined* hypothesis that, for the
   *governance-relevant* class of aggregators actually deployed, the additional structural assumption
   (slice-multiplicativity, or an equivalent bisymmetry+cancellativity condition) always holds — so
   that Theorem U applies. Whether that structural assumption is *forced* by an independently
   motivated governance requirement (rather than assumed) is open. This is the standing target of the
   public bounty ([`szl-holdings/lambda-bounty`](https://github.com/szl-holdings/lambda-bounty)),
   whose CI is *intentionally red* until Conjecture 1 (under a tightened, disclosed axiom set) is
   discharged with only the allowlisted core axioms.

2. **Fully machine-checked \(n\)-dimensional Cauchy step.** *[open sorry, disclosed]* A separate,
   axiom-*structured* uniqueness track (`Lutar/Uniqueness.lean`, theorem `lutar_unique`) documents the
   general \(n\)-axis geometric-mean derivation but carries a tagged residual `sorry` (`CAUCHY_ND`) at
   the point where the \(n\)-dimensional Cauchy/Aczél step must be fully formalized in Mathlib
   (`Mathlib.Analysis.SpecialFunctions.Pow.NNReal`). We disclose this residual explicitly; that track
   is **not** claimed proven and is **not** in the locked count. Theorem U (§5) is the honestly-proven
   result and does *not* depend on this residual.

3. **Uniqueness modulo equivalence vs. strict equality.** *[refinement]* Under weaker "identifiability"
   assumptions one obtains uniqueness only *modulo* a trust-order-preserving equivalence \(\approx_\Lambda\);
   strict equality requires an anchoring/normalization condition. Characterizing the minimal anchoring
   hypothesis that upgrades \(\approx_\Lambda\)-uniqueness to \(=\) is open.

---

## 7. Honest limitations

- **Functional form is not novel.** Weighted/equal-weight geometric-mean aggregators are standard in
  multi-criteria decision analysis. The contribution here is the *axiomatic characterization program*,
  the *machine-checked refutation* of the naive uniqueness claim, and the *axiom-free conditional*
  theorem — not the mean itself.
- **Theorem U is conditional.** It requires slice-multiplicativity. It does **not** establish
  unconditional uniqueness, and we never present it as doing so.
- **`decide`-checked evaluation.** The counterexample's separating inequality is checked by `decide`
  at a concrete rational point on the ratio scale; this is a finite, kernel-trusted decision, not a
  claim about all points.
- **Axiom scope.** "Axiom-free" for Theorem U means the trusted base is the Lean core `{propext,
  Classical.choice, Quot.sound}` — the standard classical foundation of Mathlib — not that the proof
  is constructive.
- **Pin discipline.** The locked kernel facts (749/14/163; locked-8; `locked_count_eight`) are pinned
  at `c7c0ba17`; the experimental theorems `maxAgg_ne_Lambda` and `lambda_unique_of_separable` reside
  in the experimental CI-green tier at the recorded development commit and are never folded into the
  locked count.
- **This is a draft note**, not a posted preprint. arXiv posting requires manual submission by the
  author; the DOI-pinned program on Zenodo already covers the underlying artifacts.

---

## 8. Reproduction

```bash
git clone https://github.com/szl-holdings/lutar-lean && cd lutar-lean
lake exe cache get && lake build
# counterexample (Conjecture 1 is FALSE as stated):
echo 'import Lutar.Round13.Lambda_Uniqueness
open Lutar.Round13
#print axioms maxAgg_ne_Lambda' > _Chk.lean && lake env lean _Chk.lean
# conditional uniqueness (Theorem U), axiom-free:
echo 'import Lutar.Round13.Lambda_Uniqueness
open Lutar.Round13
#print axioms lambda_unique_of_separable' >> _Chk.lean && lake env lean _Chk.lean
# expect: {propext, Classical.choice, Quot.sound} for lambda_unique_of_separable
```

---

## References

1. J. Aczél. *Lectures on Functional Equations and Their Applications.* Academic Press, 1966.
   (Cambridge reissue: [doi:10.1017/CBO9781139086578](https://doi.org/10.1017/CBO9781139086578);
   Theorem 5.1, §6 — quasi-arithmetic mean characterization.)
2. A.-L. Cauchy. *Cours d'analyse de l'École Royale Polytechnique.* 1821. (Cambridge Library reissue:
   [doi:10.1017/CBO9780511693328](https://doi.org/10.1017/CBO9780511693328); Chap. V — the
   multiplicative/additive Cauchy functional equation.)
3. M. Burai, G. Kiss, P. Szokol. *Characterization of quasi-arithmetic means without regularity
   condition.* Acta Math. Hungar. **165** (2021), 309–326.
   [doi:10.1007/s10474-021-01185-z](https://doi.org/10.1007/s10474-021-01185-z).
4. G. H. Hardy, J. E. Littlewood, G. Pólya. *Inequalities.* Cambridge Univ. Press, 1934, §2.18.
   [archive.org/details/inequalities0000hard](https://archive.org/details/inequalities0000hard).
5. I. Lakatos. *Proofs and Refutations: The Logic of Mathematical Discovery.* Cambridge Univ. Press,
   1976. [doi:10.1017/CBO9781139171472](https://doi.org/10.1017/CBO9781139171472).
6. The mathlib Community. *The Lean mathematical library.* CPP 2020, 367–381.
   [doi:10.1145/3372885.3373824](https://doi.org/10.1145/3372885.3373824).
7. SZL Holdings. *lutar-lean — Lean 4 formal proofs for the Ouroboros Thesis* (locked `c7c0ba17`,
   749/14/163). [github.com/szl-holdings/lutar-lean](https://github.com/szl-holdings/lutar-lean).
   Concept DOI [10.5281/zenodo.19944926](https://doi.org/10.5281/zenodo.19944926).
8. SZL Holdings. *Λ-Conjecture Bounty (Conjecture 1 intake + CI arbiter).*
   [github.com/szl-holdings/lambda-bounty](https://github.com/szl-holdings/lambda-bounty).

---

*Signed-off-by: Stephen P. Lutar Jr. <stephenlutar2@gmail.com>*
*Co-Authored-By: Perplexity Computer Agent <agent@perplexity.ai>*
