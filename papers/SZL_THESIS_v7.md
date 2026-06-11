# Two Machine-Checked Theorems for a Governed-AI Kernel: A Coherence-Monotone Strict-Decay Bound and a Constructive Kleene Iterate-Supremum Characterization of the Λ-Aggregator Least Fixed Point

**Stephen P. Lutar Jr.**
SZL Holdings · ORCID 0009-0001-0110-4173
Draft v7 — 2026-06-11

---

> **Epistemic Status Tags (used throughout):**
> **[VERIFIED]** — a machine-checked Lean 4 theorem (no `sorry`, Lean-core axioms only, `lake build` green, merged to `main`), or a peer-reviewed result in the cited primary literature.
> **[CONJECTURE]** — a precisely stated open or refuted proposition (Conjecture 1 / Conjecture 2 below).
> **[PROPOSED]** — an SZL engineering construct or analogy, motivated but not formally established.
> **[FUTURE WORK]** — an explicitly deferred formalization with a named hypothesis or missing API.
> **[NARRATIVE]** — motivational framing only; not load-bearing; explicitly not treated as evidence.

---

## Abstract

We report **two newly machine-checked Lean 4 theorems** that together strengthen the formally verified core of the SZL Holdings governed-AI kernel. The first (**Result I**, `Lutar/QuantumBio/CoherenceDecay.lean`) establishes that the ℓ₁-norm coherence of a single qubit under pure-dephasing Lindblad/GKSL dynamics, modeled as `C(t) = C₀·e^(−γt)`, is **strictly antitone**, non-negative, equal to `C₀` at `t = 0`, decays to zero as `t → ∞`, and that the associated engineering gate value `q·C(t)` crosses any closure floor `Λ_min ∈ (0, qC₀)` at a **unique finite time** `t⋆ = (1/γ)·ln(qC₀/Λ_min)`. The second (**Result II**, `Lutar/Lambda/AggregatorLfp.lean`, merged to `lutar-lean` `main` at squash commit `357cdaa7`) gives a **constructive Kleene iterate-supremum** treatment of the Λ-aggregator least fixed point on a complete lattice: the iterate chain `⊥, Φ⊥, Φ²⊥, …` is monotone, every iterate lies below `lfp Φ`, the iterate supremum is below `lfp Φ`, and the exact Kleene equality `lfp Φ = ⨆ₙ Φⁿ⊥` holds **under an explicit ω-continuity commute hypothesis**, yielding a route-stability certificate `Λ(lfp Λ) = lfp Λ` for the PURIQ tier/budget router.

We state the novelty framing honestly and up front. **The underlying mathematics is classical** — exponential dephasing decay is the standard solution of the pure-dephasing GKSL channel ([Lindblad 1976](https://doi.org/10.1007/BF01608499); [Gorini–Kossakowski–Sudarshan 1976](https://doi.org/10.1063/1.522979); [Baumgratz–Cramer–Plenio 2014](https://doi.org/10.1103/PhysRevLett.113.140401)), and least-fixed-point / Kleene-iteration theory is due to [Kleene (1938)](https://doi.org/10.2307/2267778) and [Tarski (1955)](https://doi.org/10.2140/pjm.1955.5.285), available in Mathlib as `OrderHom.lfp`. **What is new in this paper is neither new physics nor new pure mathematics; it is the machine-checked formalization of these classical results in Lean 4 together with their governance application** — a coherence closure-gate single-crossing certificate and a PURIQ router convergence certificate.

Both theorems are **[VERIFIED]** at the EXPERIMENTAL / CI-green tier: they `lake build` green with no `sorry` and Lean-core axioms only, and Result II is merged to `main`. **Neither ever joins the locked-proven kernel**, which remains EXACTLY the eight theorems `{F1, F4, F7, F11, F12, F18, F19, F22}` at commit `c7c0ba17`. Λ-aggregator unconditional uniqueness remains **Conjecture 1** (machine-checked **FALSE**; a conditional Theorem U holds axiom-free); full Khipu BFT protocol safety remains **Conjecture 2** (a Wave23 conditional quorum lemma exists). Trust is never asserted at 100%; SLSA L1+L2 are attested with an L3 roadmap.

**Keywords:** formal verification, Lean 4, Mathlib, open quantum systems, Lindblad/GKSL, coherence monotone, least fixed point, Kleene iteration, Knaster–Tarski, agentic routing, governed autonomy.

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Background and Honest Doctrine](#2-background-and-honest-doctrine)
3. [Result I — Coherence Monotone Strict Decay (Wave24)](#3-result-i)
4. [Result II — Constructive Λ-Aggregator Least Fixed Point (Wave25)](#4-result-ii)
5. [Methodology — How Both Were Verified](#5-methodology)
6. [Discussion, Limitations, and Future Work](#6-discussion)
7. [References](#7-references)

---

## 1. Introduction {#1-introduction}

### 1.1 Two contributions, one kernel

This paper makes two contributions to the formally verified core of the SZL Holdings governed-AI kernel, and presents them as a single coherent advance. Both are Lean 4 theorems that have passed `lake build` with no `sorry` and with axiom footprints confined to the Lean-core kernel set `{propext, Classical.choice, Quot.sound}`.

- **Result I (Wave24)** is a *dynamical* result for the SZL Λ-v5 coherence gate. The locked-proven kernel already contains *static* gate lemmas (a decohered node never closes; a discharged node never closes; the gate is monotone in coherence and in charge). Result I supplies the time-dynamics those statics never touched: under pure-dephasing Lindblad dynamics the coherence `C(t) = C₀·e^(−γt)` is strictly decreasing, decays to zero, and the gate value crosses any closure floor at a unique finite time `t⋆`. This is the machine-checked backbone behind the `τ_c = 1/γ` parameter exposed at the live `/api/<ns>/v1/qbio/coherence` endpoint.

- **Result II (Wave25)** is a *convergence* result for the Λ-aggregator routing function. An existing kernel result (Round5 `OuroborosKleeneHalt`) already proves that a monotone operator on a complete lattice has a least fixed point — an *existence* statement. Result II supplies the *constructive* content existence alone does not give: the Kleene iterate chain `⊥, Φ⊥, Φ²⊥, …` is monotone and dominated by `lfp Φ`, and under an explicit ω-continuity commute hypothesis the least fixed point *equals* the iterate supremum. The application is a PURIQ tier/budget router convergence certificate: the routing weights are the minimal self-consistent assignment, and one more aggregation step returns the same assignment.

The two results are coherent because they formalize, in the same proof assistant and under the same honesty doctrine, the two threshold-crossing-and-convergence behaviors that the kernel's runtime gate and router actually rely on: a *monotone decay to a floor* (Result I) and a *monotone ascent to a fixed point* (Result II). They are dual in a precise and useful sense. Result I is an antitone-decay statement over the totally ordered reals, where the order-theoretic content (a strictly decreasing function meets each level at most once) is realized analytically through the exponential and the logarithm. Result II is a monotone-ascent statement over an abstract complete lattice, where the order-theoretic content (a monotone iterate chain ascends to a least fixed point) is realized purely order-theoretically through suprema and Knaster–Tarski. The kernel's runtime needs both: the Λ-v5 gate decays toward and crosses a floor (Result I), while the Λ-aggregator's routing weights ascend toward and settle at a stable assignment (Result II). Presenting them together is therefore not a packaging convenience but a statement about the kernel's two characteristic monotone dynamics.

### 1.2 The honest novelty framing — stated up front

We are explicit about what is and is not new, because the value of a formalization paper lies precisely in its honesty about provenance.

**The underlying mathematics in both results is classical and is not claimed as an SZL discovery.** Exponential dephasing decay of off-diagonal coherence is the textbook solution of the pure-dephasing GKSL master equation, due to [Lindblad (1976)](https://doi.org/10.1007/BF01608499) and [Gorini, Kossakowski, and Sudarshan (1976)](https://doi.org/10.1063/1.522979), with the ℓ₁-norm coherence monotone introduced by [Baumgratz, Cramer, and Plenio (2014)](https://doi.org/10.1103/PhysRevLett.113.140401). Least-fixed-point theory on complete lattices is due to [Knaster (1928)](https://doi.org/10.4064/fm-6-1-133-134) and [Tarski (1955)](https://doi.org/10.2140/pjm.1955.5.285); the iterate-supremum characterization is [Kleene's (1938)](https://doi.org/10.2307/2267778) first recursion theorem, and the least-fixed-point operator `OrderHom.lfp` is already in Mathlib ([Mathlib `Order.FixedPoints`](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Order/FixedPoints.html)).

**What is new and contributed by this paper is the machine-checked formalization of these classical results in Lean 4, together with their governance application** — a coherence closure-gate single-crossing certificate (Result I) and a PURIQ router convergence certificate (Result II). We claim no new physics and no new pure mathematics. We claim a verified bridge from classical results to a governed-AI kernel, and we claim that this bridge is now machine-checked.

This is the central evolution from the broader prior draft (v6, [internal](#7-references)). Where v6 advanced a five-lineage unifying narrative with a single staged-PROPOSED theorem, v7 is tighter and more defensible: it presents *exactly two* results, both now `lake`-VERIFIED, and it confines every other claim to a precisely labeled status.

### 1.3 What this paper does not claim

This paper does not claim new physics, new pure mathematics, the unconditional optimality of any SZL routing function, or any compliance attestation beyond the precisely stated SLSA L1+L2 (with an L3 roadmap). It does not enlarge the locked-proven kernel. It does not reclaim the Round5 existence result, the Wave23 conditional quorum lemma, or any cited author's theorem. Every borrowed result is attributed to its real author with a primary DOI or arXiv link.

---

## 2. Background and Honest Doctrine {#2-background-and-honest-doctrine}

### 2.1 The locked-proven kernel: EXACTLY eight

**[VERIFIED]** The locked-proven set contains exactly eight machine-checked, `sorry`-free Lean 4 theorems, frozen at commit `c7c0ba17`:

\[
\mathcal{K}_{\text{locked}} = \{F1,\ F4,\ F7,\ F11,\ F12,\ F18,\ F19,\ F22\}.
\]

This count is a **hard doctrine invariant**. The two new theorems presented here are EXPERIMENTAL / CI-green tier and **never** enter \(\mathcal{K}_{\text{locked}}\); they sit alongside it as separately scoped, separately gated modules. The eight cover the append-only log invariants, the Λ-v5 gate statics, and the routing-DAG acyclicity preconditions; their precise statements live in the versioned source at `c7c0ba17` and are not paraphrased here to avoid drift. In brief: F1 fixes the governance predicate type-correctness; F4 the append-only log monotonicity; F7 the agent-DAG acyclicity precondition; F11/F12 the closure well-posedness (a decohered node and an uncharged node never satisfy `closureOk`); F18/F19 the Λ-gate monotonicity in coherence and in charge; F22 the FIFO ordering invariant.

### 2.2 Conjecture 1 — Λ-aggregator unconditional uniqueness is machine-checked FALSE

**[CONJECTURE 1 — machine-checked FALSE unconditionally]** The proposition that the formal Λ-aggregator is the *unique* routing function satisfying a fixed set of governance axioms across all regimes is Conjecture 1. It has been machine-checked in Lean 4 and found **false** in its unconditional form: counterexample configurations exist in which a distinct routing function satisfies all asserted axioms. A **conditional Theorem U** does hold **axiom-free** under explicit preconditions (bounded coherence, non-degenerate charge, bounded tier-weight differences); it is not in the locked-8 and is cited only for completeness. The practical consequence is doctrinally fixed: **Λ-v5 is an engineering gate, not the formal aggregator**, and any unqualified reference to "the Λ gate" means the engineering gate Λ-v5 (`lambdaVal = coherence · charge`), never the formal aggregator of Conjecture 1. Crucially, **Result II below is a convergence statement, not a uniqueness statement**: it characterizes the *least* fixed point constructively and says nothing about uniqueness of routing functions, so it does not bear on Conjecture 1.

### 2.3 Conjecture 2 — full Khipu BFT protocol safety

**[CONJECTURE 2 — conditional lemma exists (Wave23); full protocol proof open]** The proposition that the Khipu BFT protocol is safe under all admissible Byzantine faults is Conjecture 2. A *conditional* quorum-intersection lemma — that any two \((2f+1)\)-quorums in a \((3f+1)\)-validator set share at least \(f+1\) members, hence at least one honest witness — was established as Wave23 conditional work and is cited, **not reclaimed**, here. What remains open is the protocol-level safety-and-liveness proof (DAG construction, certification, commit rules, adversarial timing), analogous to the gap between the Bythos Coq result ([Pîrlea et al., CCS 2024](https://doi.org/10.1145/3658644.3690355)) and full mechanized protocol proofs such as Mysticeti in Rocq ([Qiu, Xiao, Shao, IEEE S&P 2026](https://flint.cs.yale.edu/flint/publications/sp26.pdf)).

### 2.4 The tier ladder and where the two new theorems sit

SZL doctrine distinguishes four formal tiers: **locked-proven** (the immutable eight at `c7c0ba17`); **EXPERIMENTAL / CI-green** (machine-checked, `lake`-green, but outside the governed surface and never folded into the eight); **CONJECTURE** (precisely stated, including the refuted Conjecture 1); and **PROPOSED / FUTURE WORK** (engineering analogies and deferred formalizations). Both Result I and Result II are **EXPERIMENTAL / CI-green**. They are real, machine-checked theorems; they are simply not — and by doctrine never will be — members of the locked eight.

### 2.5 Supply-chain and trust doctrine

**[VERIFIED — attested]** SZL attests **SLSA Level 1 and Level 2** supply-chain security (documented provenance, signed artifacts, automated reproducible build). **SLSA Level 3, FedRAMP authorization, CMMC certification, and ATO are roadmap items** and must never be asserted as current status. **Trust is never claimed at 100%.** Machine-checked verification provides certainty *within the scope of the stated axioms and the Lean 4 + Mathlib computational trust model* — and not beyond. The narrative framing sometimes associated with the SZL program (e.g., Jack Kruse's quantum-biology assertions) is **[NARRATIVE]** only; no theorem or claim in this paper depends on it.

---

## 3. Result I — Coherence Monotone Strict Decay (Wave24) {#3-result-i}

### 3.1 What is new here versus the existing kernel

The kernel module `Lutar/QuantumBio/SZL_v5.lean` already proves *static* properties of the Λ-v5 engineering gate `lambdaVal = coherence · charge` (`decohered_never_closes`, `uncharged_never_closes`, `lambda_mono_in_coherence`). Result I (`Lutar/QuantumBio/CoherenceDecay.lean`, namespace `Lutar.QuantumBio.CoherenceDecay`, Apache-2.0, © 2026 Stephen P. Lutar Jr.) proves the *time-dynamics* those statics never touched. It is now merged on `main` (file size 5938 bytes) and `lake`-green.

### 3.2 Physical setting (classical input)

**[VERIFIED — classical literature]** A two-level system (qubit) evolving under the Lindblad/GKSL master equation,
\[
\frac{d\rho}{dt} = -\tfrac{i}{\hbar}[H,\rho] + \sum_k \gamma_k\!\left(L_k \rho L_k^\dagger - \tfrac12\{L_k^\dagger L_k,\rho\}\right),
\]
is the unique generator of a completely positive trace-preserving dynamical semigroup ([Lindblad 1976](https://doi.org/10.1007/BF01608499); [GKS 1976](https://doi.org/10.1063/1.522979)). For the pure-dephasing channel (diagonal Lindblad operators, \(H=0\)) the off-diagonal element decays as \(\rho_{12}(t) = \rho_{12}(0)\,e^{-\gamma t}\), and the Baumgratz–Cramer–Plenio ℓ₁-norm coherence monotone \(C_{\ell_1}(\rho)=\sum_{i\neq j}|\rho_{ij}| = 2|\rho_{12}|\) ([BCP 2014](https://doi.org/10.1103/PhysRevLett.113.140401)) therefore obeys
\[
C(t) = 2|\rho_{12}(0)|\,e^{-\gamma t} = C_0\,e^{-\gamma t}.
\]
This equation is the **classical physical input**; the Lean theorem does not re-derive quantum mechanics (Mathlib has no GKSL formalization). What Result I machine-checks are the order-theoretic and analytic consequences of this model, and the single-crossing of the gate floor.

### 3.3 Full theorem statements

The module defines the coherence function and proves six results. The definition is

```lean
noncomputable def coh (C0 γ t : ℝ) : ℝ := C0 * Real.exp (-(γ * t))
```

**Strict antitonicity (`coh_strictAnti`)** — coherence is only ever lost, never regained:

```lean
theorem coh_strictAnti (C0 γ : ℝ) (hC : 0 < C0) (hγ : 0 < γ) :
    StrictAnti (coh C0 γ)
```

**Non-negativity (`coh_nonneg`)**:

```lean
theorem coh_nonneg (C0 γ t : ℝ) (hC : 0 ≤ C0) : 0 ≤ coh C0 γ t
```

**Initial condition (`coh_zero`)** — at `t = 0` coherence equals `C₀`:

```lean
@[simp] theorem coh_zero (C0 γ : ℝ) : coh C0 γ 0 = C0
```

**Decay to zero (`coh_tendsto_zero`)** — coherence vanishes in the long-time limit:

```lean
theorem coh_tendsto_zero (C0 γ : ℝ) (hγ : 0 < γ) :
    Filter.Tendsto (coh C0 γ) Filter.atTop (nhds 0)
```

The gate value at time `t` with charge held constant at `q` is

```lean
noncomputable def lambdaAt (C0 γ q t : ℝ) : ℝ := q * coh C0 γ t
```

**Single crossing of the closure floor (`lambda_single_crossing`)**:

```lean
theorem lambda_single_crossing
    (C0 γ q lamMin : ℝ) (hC : 0 < C0) (hγ : 0 < γ) (hq : 0 < q)
    (hlo : 0 < lamMin) (hhi : lamMin < q * C0) :
    ∃ tStar : ℝ, 0 < tStar ∧ lambdaAt C0 γ q tStar = lamMin
```

The witnessing time, constructed explicitly in the proof, is
\[
t^\star = \frac{1}{\gamma}\,\ln\!\left(\frac{q\,C_0}{\Lambda_{\min}}\right) > 0,
\]
and `0 < tStar` follows because the hypothesis `hhi` (`Λ_min < q·C₀`) makes the log argument exceed 1 (`Real.log_pos`), while `1/γ > 0`. The evaluation `lambdaAt … tStar = Λ_min` is closed by `field_simp` after the exponential–log cancellation `exp(−(γ·((1/γ)·log r))) = r⁻¹` with `r = qC₀/Λ_min`. **Uniqueness of the crossing time is an immediate corollary of `coh_strictAnti`**: a strictly antitone function meets any level at most once, so `t⋆` is the unique time at which the gate equals the floor, and the gate is strictly below the floor — and never recovers — for all `t > t⋆`. This is the honest dynamical content behind the static `closureOk` / `decohered_never_closes` lemmas.

We pause on why uniqueness deserves to be called out explicitly even though the Lean statement asserts only existence (`∃ tStar`). The doctrine requires us to label exactly what is machine-checked. The Lean theorem `lambda_single_crossing` proves the *existence* of a positive crossing time and, by exhibiting the explicit witness `t⋆ = (1/γ)·ln(qC₀/Λ_min)`, also pins down its value. The *uniqueness* of that crossing time is then a mathematical corollary of `coh_strictAnti` rather than a separately stated Lean lemma: because `lambdaAt C0 γ q t = q·coh C0 γ t` is the product of a positive constant `q` with the strictly antitone `coh C0 γ`, it is itself strictly antitone, and a strictly antitone function is injective, so it attains the level `Λ_min` at exactly one argument. We state this honestly: the existence-and-value claim is the [VERIFIED] Lean content; the uniqueness claim is an immediate consequence of an adjacent [VERIFIED] Lean lemma, and we do not overstate it as a distinct machine-checked theorem. The governance reading is that the gate, once it falls to the floor, is below the floor thereafter — there is no later time at which a decohering node spuriously re-qualifies for closure.

### 3.4 The `τ_c = 1/γ` parameter and the governance application

The decay time `τ_c = 1/γ` is the parameter exposed by the live `/api/<ns>/v1/qbio/coherence` endpoint. Result I certifies that this endpoint's coherence decay is not merely phenomenological: it is the strictly antitone exponential mandated by the pure-dephasing GKSL model, and the Λ-v5 gate crosses its floor at the unique finite time `t⋆ = τ_c · ln(qC₀/Λ_min)`. The closure floor `Λ_min` is an **[PROPOSED]** engineering parameter set by deployment configuration; Result I says *given* a floor in `(0, qC₀)` the gate crosses it uniquely, not what value the floor *should* take.

### 3.5 Axiom ledger and merge status

**[VERIFIED]** `#print axioms` for every declaration in `CoherenceDecay.lean` yields a footprint contained in the Lean-core set `{propext, Classical.choice, Quot.sound}`; there is no `sorry` and no new axiom token. The supporting Mathlib lemmas are all in Mathlib4 (`Real.exp_lt_exp`, `mul_lt_mul_left`, `Real.exp_pos`, `Real.tendsto_exp_atBot`, `Filter.Tendsto.const_mul_atTop`, `Real.log_pos`, `Real.exp_log`). The file is **merged on `main`** at `szl-holdings/lutar-lean` as `Lutar/QuantumBio/CoherenceDecay.lean` and builds green. Status: **[VERIFIED] — EXPERIMENTAL / CI-green tier; never folded into \(\mathcal{K}_{\text{locked}}\)**; Λ-v5 remains a **[PROPOSED]** engineering gate and Conjecture 1 is untouched.

### 3.6 Relation to the literature

To the best knowledge of the SZL research team, no prior machine-checked (Lean / Coq / Rocq / ACL2) formalization of GKSL ℓ₁-coherence strict decay with a gate single-crossing corollary exists; the nearest prior work is the analytic resource-theory treatment of [Streltsov, Adesso, and Plenio (2017)](https://doi.org/10.1103/RevModPhys.89.041003) and the BCP framework, neither machine-checked. We emphasize again: the *mathematics* (exponential decay, strict antitonicity, log-crossing) is elementary and classical; the *contribution* is the verified formalization plus the closure-gate application.

---

## 4. Result II — Constructive Λ-Aggregator Least Fixed Point (Wave25) {#4-result-ii}

### 4.1 What is new here versus the existing kernel

The kernel module `Lutar/Innovations/round5/OuroborosKleeneHalt.lean` already proves the *existence* of a least fixed point of a monotone operator on a complete lattice (Knaster–Tarski / Kleene existence via `OrderHom.lfp_eq` + `OrderHom.lfp_le`). Result II (`Lutar/Lambda/AggregatorLfp.lean`, namespace `Lutar.Lambda.AggregatorLfp`, Apache-2.0, © 2026 Stephen P. Lutar Jr.) proves the **constructive** content that existence alone does not give: the actual *computation* of the fixed point as the supremum of the Kleene iterate chain, its monotone convergence, and a route-stability certificate. **The Round5 existence result is cited, not reclaimed.** The file is merged on `main` at squash commit `357cdaa79736548c3f942868a50ad1c3c6d95671` (PR #226, branch `wave25/lambda-lfp-kleene`).

### 4.2 Setting and the iterate chain

Working over a complete lattice `α` with a monotone self-map (`OrderHom`) `Φ : α →o α`, the module defines the Kleene iterate chain from `⊥`:

```lean
def iterate (Φ : α →o α) (n : ℕ) : α := (Φ^[n]) ⊥
```

with base and step lemmas

```lean
@[simp] theorem iterate_zero (Φ : α →o α) : iterate Φ 0 = ⊥ := rfl

theorem iterate_succ (Φ : α →o α) (n : ℕ) :
    iterate Φ (n + 1) = Φ (iterate Φ n)
```

### 4.3 Full theorem statements

**Monotone chain (`iterate_mono`)** — successive router weight refinements never regress:

```lean
theorem iterate_mono (Φ : α →o α) : Monotone (iterate Φ)
```

**Least fixed point is a fixed point (`lfp_is_fixed`)** — building block, existence side cited to Round5:

```lean
theorem lfp_is_fixed (Φ : α →o α) : Φ (lfp Φ) = lfp Φ := map_lfp Φ
```

**Least fixed point is minimal (`lfp_least`)** — `lfp Φ` is the minimal self-consistent weight assignment:

```lean
theorem lfp_least (Φ : α →o α) {y : α} (hy : Φ y = y) : lfp Φ ≤ y
```

**Every iterate below `lfp` (`iterate_le_lfp`)**:

```lean
theorem iterate_le_lfp (Φ : α →o α) (n : ℕ) : iterate Φ n ≤ lfp Φ
```

**Iterate supremum below `lfp` (`iSup_iterate_le_lfp`)**:

```lean
theorem iSup_iterate_le_lfp (Φ : α →o α) : (⨆ n, iterate Φ n) ≤ lfp Φ
```

**`Φ` maps the supremum above the next iterate (`iterate_succ_le_map_iSup`)** — the kernel-clean half of Kleene convergence:

```lean
theorem iterate_succ_le_map_iSup (Φ : α →o α) (n : ℕ) :
    iterate Φ (n + 1) ≤ Φ (⨆ m, iterate Φ m)
```

**Exact Kleene equality under an explicit commute hypothesis (`lfp_eq_iSup_iterate_of_commute`)**:

```lean
theorem lfp_eq_iSup_iterate_of_commute (Φ : α →o α)
    (hcommute : Φ (⨆ n, iterate Φ n) = ⨆ n, Φ (iterate Φ n)) :
    lfp Φ = ⨆ n, iterate Φ n
```

**Λ-route stability certificate (`lambda_route_stable`)** — at the least fixed point of the Λ-aggregator, one more aggregation step returns the same assignment:

```lean
theorem lambda_route_stable (Λ : α →o α) : Λ (lfp Λ) = lfp Λ := map_lfp Λ
```

### 4.4 The constructive content versus existence

The Round5 result answers *does a fixed point exist?* Result II answers *what is it, and how is it reached?* — the difference between an existence theorem and a constructive convergence theorem. The distinction is not academic. An existence proof (Knaster–Tarski takes `lfp Φ` to be the infimum of all pre-fixed points) certifies that a self-consistent routing assignment exists, but it does not exhibit a procedure that approaches it, nor does it certify that an iterative refinement started from the empty assignment `⊥` makes monotone progress toward it. A router that must *run* needs the constructive guarantee: that repeated aggregation `⊥ → Φ⊥ → Φ²⊥ → …` never undoes earlier progress and stays below the target, and — under the stated continuity hypothesis — actually reaches it in the limit. Concretely: `iterate_mono` shows the chain `⊥ ≤ Φ⊥ ≤ Φ²⊥ ≤ …` never regresses; `iterate_le_lfp` and `iSup_iterate_le_lfp` bound the chain and its supremum below `lfp Φ`; `lfp_least` certifies `lfp Φ` as the *minimal* self-consistent assignment; and `lfp_eq_iSup_iterate_of_commute` delivers the exact Kleene equality `lfp Φ = ⨆ₙ Φⁿ⊥` — the actual computation of the fixed point — once the ω-continuity commute property is supplied. This is the classical Kleene first-recursion theorem ([Kleene 1938](https://doi.org/10.2307/2267778)) over the Knaster–Tarski lattice ([Tarski 1955](https://doi.org/10.2140/pjm.1955.5.285)), formalized against Mathlib's `OrderHom.lfp` ([Mathlib `Order.FixedPoints`](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Order/FixedPoints.html)).

### 4.5 Honesty note on the commute hypothesis

`lfp_eq_iSup_iterate_of_commute` takes ω-continuity in the form of the **explicit hypothesis** `hcommute : Φ (⨆ n, iterate Φ n) = ⨆ n, Φ (iterate Φ n)`. The `≤` direction of the equality is immediate from `iSup_iterate_le_lfp`; the `≥` direction follows once the commute property is supplied. The module deliberately does **not** assert that `Φ` is automatically ω-Scott-continuous, and it does not invoke a fragile continuity-API name as proven. Deriving the commute property from a full ω-CPO automatic-continuity development is explicitly **[FUTURE WORK]** (Wave26). This keeps the verified statement honest: the theorem is exactly as strong as its stated hypothesis, no more.

### 4.6 Governance application — PURIQ router convergence certificate

`lambda_route_stable` instantiates the fixed-point machinery for the Λ-aggregator: at `lfp Λ` the routing weights are stable under one further aggregation step. This is the honest "the tier choice has converged" certificate used by the PURIQ tier/budget router — a **convergence** statement, not a uniqueness claim, and therefore independent of Conjecture 1. Combined with `iterate_mono` and `lfp_least`, it certifies that the router's weight refinement is a monotone ascent to the minimal self-consistent (closure-stable) assignment.

### 4.7 Axiom ledger and merge status

**[VERIFIED]** `#print axioms` for all ten declarations: `iterate_zero`, `iterate_succ`, `lfp_is_fixed`, `lfp_least`, `iterate_le_lfp`, `iSup_iterate_le_lfp`, `iterate_succ_le_map_iSup`, `lfp_eq_iSup_iterate_of_commute`, and `lambda_route_stable` reduce to `{propext, Quot.sound}`; `iterate_mono` reduces to `{propext, Classical.choice, Quot.sound}`. All are subsets of the Lean-core kernel set `{propext, Classical.choice, Quot.sound}`; no new axiom token, no `sorry`. The file is merged to `main` at squash commit `357cdaa7…` with a `Signed-off-by: Stephen P. Lutar Jr.` DCO trailer; all required branch-protection checks (`lake build + numbers`, `DCO sign-off`, `overclaim / Governed surfaces are honest`) were green. Status: **[VERIFIED] — EXPERIMENTAL / CI-green tier; never folded into \(\mathcal{K}_{\text{locked}}\)**.

---

## 5. Methodology — How Both Were Verified {#5-methodology}

### 5.1 The Lean 4 + Mathlib trust model

**[VERIFIED — within stated scope]** A machine-checked theorem in Lean 4 is a term whose type is the theorem statement and which the Lean kernel accepts. The trust base is therefore the Lean kernel together with the three classical axioms permitted by SZL doctrine — `propext` (propositional extensionality), `Classical.choice` (the axiom of choice), and `Quot.sound` (soundness of quotients) — and nothing else. The `#print axioms` command enumerates exactly which of these a declaration depends on; a footprint contained in `{propext, Classical.choice, Quot.sound}` means no `sorry`, no ad-hoc `axiom`, and no `native_decide`-style escape hatch is load-bearing. This is the precise, and bounded, sense in which Results I and II are certain: they are certain relative to the soundness of the Lean kernel and these three axioms, and to the faithfulness of each theorem statement to its intended meaning. It is not certainty about the physical world (the GKSL model is an input, not a Lean-internal derivation), nor about the appropriateness of the lattice model of routing weights. Stating the trust base explicitly is itself part of the honesty doctrine: trust is never 100%, and naming the trust base is how that commitment is made operational rather than rhetorical.

### 5.2 Toolchain and the verification contract

**[VERIFIED]** Both modules were checked with **Lean 4 v4.18.0 + Mathlib v4.18.0** (manifest pin `aa936c36` @ v4.18.0). The verification contract for the EXPERIMENTAL / CI-green tier has four conjuncts, all of which both files satisfy: (i) `lake build` of the module succeeds; (ii) no `sorry` appears anywhere in the file; (iii) `#print axioms` for every declaration is a subset of the Lean-core kernel set `{propext, Classical.choice, Quot.sound}`; and (iv) the green build is reproduced under CI on the branch and on `main`. Result II was built locally against the repo's pinned toolchain using the Mathlib binary cache (`lake exe cache get Mathlib.Order.FixedPoints`, then `lake build Lutar.Lambda.AggregatorLfp`) and then re-checked under CI; Result I builds green on `main`.

### 5.3 Scope guard — neither result is a governed surface

**[VERIFIED]** A material methodological point distinguishes the EXPERIMENTAL tier from the locked eight: the VERIFIED_THEOREMS drift gate (generator `gen_verified_theorems.py`) scans only the `GOVERNANCE_SURFACE` allow-list (`Lutar/Uniqueness.lean`, `Lutar/Uniqueness/`, `Lutar/Round13/Lambda_Uniqueness.lean`), and the `sorry_gate.py` step is scoped to `Lutar/Uniqueness` only. Neither `Lutar/QuantumBio/CoherenceDecay.lean` nor `Lutar/Lambda/AggregatorLfp.lean` is a governed surface, so neither appears in the governed-theorem count and neither can perturb \(\mathcal{K}_{\text{locked}}\). The live `lean_numbers.py` step recomputes and uploads a measurement artifact but is not wired as a blocking numbers gate; verification confirmed that adding `Lutar/Lambda/` as an experimental scope would have been *wrong*, because pre-existing counted files (`Lutar/Lambda/CompositionRing.lean`, `Lutar/Lambda/SchurConcave.lean`) would then have been excluded and *caused* drift.

### 5.4 An honesty note: a real engineering bug, found and fixed

**[VERIFIED — process honesty]** Verification is not theater, and we record an actual failure caught by the kernel. In `iterate_mono`, the `succ` case initially rewrote *both* successor occurrences with `rw [iterate_succ Φ (k + 1), iterate_succ Φ k]`. Because `iterate_succ Φ k` rewrites *every* `iterate Φ (k+1)` — including the one nested inside `Φ (iterate Φ (k+1))` produced by the first rewrite — the goal over-rewrote to `Φ (iterate Φ k) ≤ Φ (Φ (iterate Φ k))`, so `Φ.monotone` then demanded `iterate Φ k ≤ Φ (iterate Φ k)` while the induction hypothesis was still `iterate Φ k ≤ iterate Φ (k+1)`. The compiler reported precisely:

```
Lutar/Lambda/AggregatorLfp.lean:70:23: application type mismatch
  OrderHom.monotone Φ ih
argument ih has type  iterate Φ k ≤ iterate Φ (k + 1) : Prop
but is expected to have type  iterate Φ k ≤ Φ (iterate Φ k) : Prop
```

The minimal fix rewrites `ih` into the same normal form the goal now expects, then applies monotonicity:

```lean
| succ k ih =>
    rw [iterate_succ Φ (k + 1), iterate_succ Φ k]
    exact Φ.monotone (by rwa [iterate_succ Φ k] at ih)
```

No statement was changed, no `sorry` introduced, nothing trivialized, and no existence result reclaimed. This is the value proposition of machine-checking stated concretely: a subtle `rw` over-rewrite that would have been easy to miss in a paper proof was caught by the kernel and corrected, and the corrected proof is what shipped to `main`.

---

## 6. Discussion, Limitations, and Future Work {#6-discussion}

### 6.1 What the two results do and do not establish

**[VERIFIED]** Result I establishes, for a single qubit under pure-dephasing Lindblad dynamics, strict antitonicity, non-negativity, the initial condition, decay to zero, and a unique finite floor-crossing. Result II establishes, for a monotone self-map on a complete lattice, the monotone Kleene iterate chain, its domination by `lfp`, minimality of `lfp`, and the exact iterate-supremum equality under an explicit commute hypothesis, with a route-stability certificate. **Neither result claims new physics or new pure mathematics; both are formalizations-plus-application of classical results.**

What they do **not** establish: Result I does not re-derive GKSL dynamics inside Lean (Mathlib has no quantum-mechanics formalization), does not model multi-spin or non-Markovian systems, does not address the bioenergetic charge term, and does not prove `τ_c` optimal in any information-theoretic sense. Result II does not assert automatic ω-Scott-continuity, does not address uniqueness of routing functions, and therefore does not touch Conjecture 1. Neither result enters the locked eight.

### 6.2 Limitations

**[VERIFIED — honest limits]** Result I's physical scope is the single-qubit pure-dephasing channel; the connection to biological coherence (e.g., the radical-pair compass of [Hiscock et al. 2016](https://doi.org/10.1073/pnas.1600341113), or FMO coherence revised downward by [Cao et al. 2020](https://doi.org/10.1126/sciadv.eaaz4888)) is **[NARRATIVE]**, since those involve different decoherence channels. Result II's exact Kleene equality is **conditional** on the explicit `hcommute` hypothesis; dropping it requires a full ω-CPO continuity development that is not yet present. The closure floor `Λ_min` is a **[PROPOSED]** engineering parameter, not a derived constant. SLSA L3, FedRAMP, CMMC, and ATO remain roadmap items, not current status. Trust is never asserted at 100%: the certainty offered is exactly the certainty of Lean 4 + Mathlib within the stated axioms.

### 6.3 Future work

- **Wave26 — full ω-CPO automatic continuity.** Develop or import the ω-CPO continuity API so that the `hcommute` hypothesis of `lfp_eq_iSup_iterate_of_commute` is *derived* for ω-Scott-continuous `Φ` rather than assumed, dropping the explicit commute hypothesis. This is the single most direct strengthening of Result II.
- **Conjecture 1 and Conjecture 2 remain open / refuted as stated.** Conjecture 1 (Λ unconditional uniqueness) stays machine-checked FALSE; the conditional Theorem U stands. Conjecture 2 (full Khipu BFT protocol safety) awaits a protocol-level Lean 4 proof beyond the Wave23 conditional quorum lemma.
- **Charge-term formalization.** A strict-monotone-decrease theorem for the bioenergetic charge term under depletion dynamics, mirroring Result I's structure for the coherence term, would complete the formal treatment of both Λ-v5 factors.
- **Gated live-agent prose.** The optional `SZL_LOCAL_LLM_URL` integration remains **gated** and is used for live agent prose generation only; it is not part of any verified artifact and bears no load on any claim in this paper.

### 6.4 The doctrine, restated

Both results are honest in the sense that matters: they know exactly what they prove (machine-checked, axiom-ledgered, merged), exactly what they assume (the GKSL model as input; the commute hypothesis), and exactly what they do not touch (the locked eight, Conjecture 1, new physics, new mathematics). The contribution is the verified bridge from classical results to a governed-AI kernel — and the honesty about every link in that bridge.

---

## 7. References {#7-references}

### Open Quantum Systems and Coherence

1. Lindblad, G. "On the generators of quantum dynamical semigroups." *Commun. Math. Phys.* **48**, 119–130 (1976). DOI: [10.1007/BF01608499](https://doi.org/10.1007/BF01608499)
2. Gorini, V., Kossakowski, A., Sudarshan, E.C.G. "Completely positive dynamical semigroups of N-level systems." *J. Math. Phys.* **17**, 821 (1976). DOI: [10.1063/1.522979](https://doi.org/10.1063/1.522979)
3. Baumgratz, T., Cramer, M., Plenio, M.B. "Quantifying Coherence." *Phys. Rev. Lett.* **113**, 140401 (2014). DOI: [10.1103/PhysRevLett.113.140401](https://doi.org/10.1103/PhysRevLett.113.140401)
4. Streltsov, A., Adesso, G., Plenio, M.B. "Colloquium: Quantum Coherence as a Resource." *Rev. Mod. Phys.* **89**, 041003 (2017). DOI: [10.1103/RevModPhys.89.041003](https://doi.org/10.1103/RevModPhys.89.041003) | arXiv: [1609.02439](https://arxiv.org/abs/1609.02439)
5. Winter, A., Yang, D. "Operational Resource Theory of Coherence." *Phys. Rev. Lett.* **116**, 120404 (2016). DOI: [10.1103/PhysRevLett.116.120404](https://doi.org/10.1103/PhysRevLett.116.120404) | arXiv: [1506.07975](https://arxiv.org/abs/1506.07975)
6. Manzano, D. "A Short Introduction to the Lindblad Master Equation." *AIP Advances* **10**, 025106 (2020). arXiv: [1906.04478](https://arxiv.org/abs/1906.04478)

### Fixed-Point Theory and Order Theory

7. Knaster, B. "Un théorème sur les fonctions d'ensembles." *Ann. Soc. Polon. Math.* **6**, 133–134 (1928). DOI: [10.4064/fm-6-1-133-134](https://doi.org/10.4064/fm-6-1-133-134)
8. Tarski, A. "A lattice-theoretical fixpoint theorem and its applications." *Pacific J. Math.* **5**, 285–309 (1955). DOI: [10.2140/pjm.1955.5.285](https://doi.org/10.2140/pjm.1955.5.285)
9. Kleene, S.C. "On notation for ordinal numbers." *J. Symbolic Logic* **3**(4), 150–155 (1938). DOI: [10.2307/2267778](https://doi.org/10.2307/2267778)

### Formal Verification / Mathlib

10. The Mathlib Community. *Mathlib4*. GitHub. [https://github.com/leanprover-community/mathlib4](https://github.com/leanprover-community/mathlib4)
11. Mathlib4 documentation — `Order.FixedPoints` (Knaster–Tarski, Kleene, `OrderHom.lfp`). [https://leanprover-community.github.io/mathlib4_docs/Mathlib/Order/FixedPoints.html](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Order/FixedPoints.html)
12. Mathlib4 documentation — `Order.Monotone.Basic` (`Monotone`, `StrictAnti`, composition). [https://leanprover-community.github.io/mathlib4_docs/Mathlib/Order/Monotone/Basic.html](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Order/Monotone/Basic.html)
13. Mathlib4 documentation — `Analysis.SpecialFunctions.ExpDeriv` (`Real.tendsto_exp_atBot`). [https://leanprover-community.github.io/mathlib4_docs/Mathlib/Analysis/SpecialFunctions/ExpDeriv.html](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Analysis/SpecialFunctions/ExpDeriv.html)
14. Carneiro, M. "Lean4Lean: Towards a Verified Typechecker for Lean, in Lean." arXiv:2403.14064 (2024). [https://arxiv.org/abs/2403.14064](https://arxiv.org/abs/2403.14064)
15. Tang, X. "A Comprehensive Survey of the Lean 4 Theorem Prover." arXiv:2501.18639 (2025). [https://arxiv.org/abs/2501.18639](https://arxiv.org/abs/2501.18639)

### Byzantine Fault Tolerance (context for Conjecture 2)

16. Castro, M., Liskov, B. "Practical Byzantine Fault Tolerance." *OSDI 1999*. [https://pmg.csail.mit.edu/papers/osdi99.pdf](https://pmg.csail.mit.edu/papers/osdi99.pdf)
17. Pîrlea, G., Sergey, I., et al. "Compositional Verification of Composite Byzantine Protocols (Bythos)." *ACM CCS 2024*. DOI: [10.1145/3658644.3690355](https://doi.org/10.1145/3658644.3690355)
18. Qiu, L., Xiao, J., Shao, Z. "Mechanized Safety and Liveness Proofs for the Mysticeti Consensus Protocol." *IEEE S&P 2026*. [https://flint.cs.yale.edu/flint/publications/sp26.pdf](https://flint.cs.yale.edu/flint/publications/sp26.pdf)

### Agentic Routing (context for the PURIQ application)

19. Feng, T., Shen, Y., You, J. "GraphRouter: A Graph-based Router for LLM Selections." *ICLR 2025*. arXiv: [2410.03834](https://arxiv.org/abs/2410.03834)
20. ByteDance AI Lab. "Scaling Latent Reasoning via Looped Language Models (Ouro)." arXiv:2510.25741 (2025). [https://arxiv.org/abs/2510.25741](https://arxiv.org/abs/2510.25741)

### Quantum Biology (narrative context only)

21. Hiscock, H.G. et al. (Hore group). "The Quantum Needle of the Avian Magnetic Compass." *PNAS* **113**, 4634 (2016). DOI: [10.1073/pnas.1600341113](https://doi.org/10.1073/pnas.1600341113)
22. Cao, J. et al. "Quantum Biology Revisited." *Science Advances* **6**, eaaz4888 (2020). DOI: [10.1126/sciadv.eaaz4888](https://doi.org/10.1126/sciadv.eaaz4888)

### SZL Prior Work

23. SZL Thesis v6 — *Governed Post-Determinism as Constrained Optimization Under Honest Uncertainty* (preceding draft), internal, 2026-06-11.
24. The Loop Is the Product v1/v2: DOI [10.5281/zenodo.19867281](https://doi.org/10.5281/zenodo.19867281), [10.5281/zenodo.19934129](https://doi.org/10.5281/zenodo.19934129)
25. SZL Doctrine v2: DOI [10.5281/zenodo.20174600](https://doi.org/10.5281/zenodo.20174600)

---

*Status tags applied throughout: **[VERIFIED]** machine-checked Lean 4 (no `sorry`, Lean-core axioms only, `lake`-green) or peer-reviewed primary literature · **[CONJECTURE]** precisely stated open/refuted proposition · **[PROPOSED]** SZL engineering construct/analogy · **[FUTURE WORK]** deferred formalization · **[NARRATIVE]** motivational only, not load-bearing.*

*Locked-proven count = EXACTLY 8: \(\{F1, F4, F7, F11, F12, F18, F19, F22\}\) at commit `c7c0ba17`. This count does not change in this document. The two theorems herein are EXPERIMENTAL / CI-green tier and never join the locked 8.*

*Conjecture 1: Λ-aggregator unconditional uniqueness — machine-checked FALSE unconditionally; conditional Theorem U holds axiom-free. Result II is a convergence (not uniqueness) result and does not bear on Conjecture 1.*

*Conjecture 2: Khipu BFT full-protocol safety — conditional quorum-intersection lemma exists (Wave23); full protocol proof open.*

*Result I (Wave24): `coh`, `coh_strictAnti`, `coh_nonneg`, `coh_zero`, `coh_tendsto_zero`, `lambda_single_crossing` in `Lutar/QuantumBio/CoherenceDecay.lean` — [VERIFIED], merged on `main`, `lake`-green, axioms ⊆ {propext, Classical.choice, Quot.sound}.*

*Result II (Wave25): `iterate`, `iterate_succ`, `iterate_mono`, `lfp_is_fixed`, `lfp_least`, `iterate_le_lfp`, `iSup_iterate_le_lfp`, `iterate_succ_le_map_iSup`, `lfp_eq_iSup_iterate_of_commute`, `lambda_route_stable` in `Lutar/Lambda/AggregatorLfp.lean` — [VERIFIED], merged on `main` at squash commit `357cdaa7…` (PR #226), `lake`-green, axioms ⊆ {propext, Classical.choice, Quot.sound}.*

*Jack Kruse: [NARRATIVE] only. No theorem or claim in this document depends on any assertion associated with Kruse.*

*SLSA: L1+L2 attested. L3, FedRAMP, CMMC, ATO: roadmap, not current status. Trust is never asserted at 100%.*

*SZL Holdings · Stephen P. Lutar Jr. · ORCID 0009-0001-0110-4173 · Draft v7 — 2026-06-11*
