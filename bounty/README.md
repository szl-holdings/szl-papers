<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- SZL Holdings — Λ-Conjecture Bounty · Sign: Yachay <yachay@szlholdings.dev> -->

# Λ Uniqueness Boundary — Original Bounty Suspended

**The original A1–A4 uniqueness statement is disproved as stated. No sound proof can discharge it, so the original bounty is suspended. The open research target is to identify the weakest independently justified additional condition and prove the resulting theorem in Lean 4.**

> **Doctrine v11** — 749 declarations · 14 unique axioms · 163 sorries · `locked_at c7c0ba17`
> **Conjecture 1 is disproved as stated.** Conditional Theorem U is proven on its declared hypotheses; the weaker-condition uniqueness question remains open. The historical target below is retained as a negative control, not as a winnable theorem.

> **Where to submit.** The working **intake + CI arbiter** lives in
> [`szl-holdings/lambda-bounty`](https://github.com/szl-holdings/lambda-bounty)
> (formal statement, `verify-proof` CI, submission template, live webhook). The
> founder-set **bounty declaration** lives in
> [`lutar-lean/BOUNTY.md`](https://github.com/szl-holdings/lutar-lean/blob/main/BOUNTY.md).
> Do not submit a purported proof of the refuted A1–A4 statement. A replacement bounty requires a founder-published strengthened statement, acceptance criteria, and award terms before submissions reopen.

---

## What is Λ?

Λ is the **9-axis geometric-mean trust aggregator** at the apex of the SZL mesh anatomy (the *crown* unifier, formula **F23**). It takes a 9-axis trust vector and collapses it to a single trust scalar with one defining behaviour: **a single fully-failed axis vetoes trust** (weakest-link / zero-absorption). Across the mesh kernels — brain, heart, spine, immune, aide — Λ is the function that decides whether composed agentic trust holds.

The original program **conjectured** that four natural axioms pin Λ down *uniquely*:

| Axiom | Name | Meaning |
|------:|------|---------|
| **A1** | Idempotence | Aggregating a constant vector returns that constant. |
| **A2** | Monotonicity | Pointwise ≤ on inputs ⇒ ≤ on the aggregate. |
| **A3** | Symmetry | The aggregate is invariant under permutation of the 9 axes. |
| **A4** | Zero-absorption | If any axis is `0`, the aggregate is `0` (weakest-link). |

**Refuted Conjecture 1 (Λ-Aggregator Uniqueness).** Any two aggregators satisfying A1–A4 agree on every input.

```lean
theorem lambda_aggregator_unique
    (Λ₁ Λ₂ : Aggregator)
    (h₁ : SatisfiesAxioms Λ₁) (h₂ : SatisfiesAxioms Λ₂) :
    ∀ x : Axis → Nat, Λ₁ x = Λ₂ x := by
  sorry  -- historical impossible target; retained only as a negative control
```

The formal statement lives in [`Lambda/Lambda.lean`](Lambda/Lambda.lean). The axiom allowlist lives in [`Lambda/Allowed_Axioms.lean`](Lambda/Allowed_Axioms.lean).

> **Provenance honesty.** Quechua/heritage names elsewhere in the SZL platform are *brand naming* and analogy only — no prior-art or mystical claims. The geometric-mean / weakest-link framing is classic aggregation theory; this conjecture is our concrete Lean formalization of the mesh's apex aggregator.

> **Soundness boundary.** A1–A4 *alone* do **not** single out the geometric mean: `min` satisfies all four (idempotent, monotone, symmetric, zero-absorbing) yet `min ≠ geometric mean` (Aczél 1966; Kolmogorov–Nagumo–de Finetti 1930–31). The literal statement is refuted by this counterexample. Candidate strengthened theorems require independently justified structure such as continuity, bisymmetry/associativity, and homogeneity or multiplicativity. Choosing the replacement statement is a founder decision; until then the bounty stays suspended and red CI records the refuted target rather than an unfinished proof.

---

## Historical validation contract

There is currently **no valid winning submission** for the refuted statement. The former CI contract is preserved below so the negative result remains reproducible; it must not be bypassed or weakened to manufacture a green check.

1. **`lake build` is green** on Lean `v4.13.0` + Mathlib `v4.13.0` (pinned by [`lean-toolchain`](lean-toolchain) and [`lakefile.lean`](lakefile.lean)).
2. **No `sorry` / `sorryAx` anywhere** under `Lambda/`. The historical target intentionally fails because the statement is false, not because a proof is merely undiscovered.
3. **No axiom beyond the allowlist.** CI runs `#print axioms lambda_aggregator_unique` and rejects any dependency outside:
   - `propext` — propositional extensionality (Lean core)
   - `Quot.sound` — quotient soundness (Lean core)
   - `Classical.choice` — classical choice (Mathlib/Std foundation)
4. **No new `axiom` declarations**, and no `native_decide`-style compiler-trust escape hatches. `decide`, `omega`, `simp`, `ring`, etc. are all fine — they elaborate to the allowlisted foundations.

There is **no bypass**: branch protection requires the `verify-proof` check to pass before merge.

---

## How to propose a replacement

1. Open a research proposal in [`szl-holdings/lambda-bounty`](https://github.com/szl-holdings/lambda-bounty) that states the added condition, its independent governance justification, and a counterexample showing why a weaker candidate fails.
2. Do not alter the refuted theorem or its failing negative-control CI until the founder publishes a replacement target.
3. For an accepted replacement target, run the eventual proof locally:
   ```bash
   lake exe cache get        # fetch prebuilt Mathlib
   lake build                # must be green
   echo 'import Lambda.Lambda
   open Lambda
   #print axioms lambda_aggregator_unique' > _AxiomCheck.lean
   lake env lean _AxiomCheck.lean   # must show only propext / Quot.sound / Classical.choice
   ```
4. Submit proof code only after the repository publishes revised terms and a revised theorem statement.

---

## Award status

No cash award, authorship promise, or submission window is active for the refuted target. Any replacement bounty must publish an exact theorem, eligibility rules, attribution terms, and a funded award before opening.

---

## Hall of Fame

| # | Solver | PR | Accepted (Khipu receipt) | Axioms used |
|--:|--------|----|--------------------------|-------------|
| — | *open* | —  | —                        | —           |

*Original target closed as refuted; replacement target not yet opened.*

---

## Repository layout

```
lambda-bounty/
├── Lambda.lean                  # library root (imports the conjecture + allowlist)
├── Lambda/
│   ├── Lambda.lean              # refuted historical target / negative control
│   ├── Allowed_Axioms.lean      # the axiom allowlist + its size lemma
│   └── Submissions/             # (optional) your helper lemmas go here
├── submissions/
│   └── SUBMISSION_TEMPLATE.md   # PR template — copy into your PR description
├── lakefile.lean                # Lean 4 + Mathlib v4.13.0
├── lean-toolchain               # leanprover/lean4:v4.13.0
├── .github/workflows/verify-proof.yml  # no-bypass CI arbiter
└── LICENSE                      # Apache-2.0
```

---

## License

Apache-2.0. See [LICENSE](LICENSE). By submitting, you license your contribution under Apache-2.0 and consent to thesis/DOI co-authorship attribution.

Signed — **Yachay** `<yachay@szlholdings.dev>` · SZL Holdings · Doctrine v11 (749 / 14 / 163 · `c7c0ba17`).
