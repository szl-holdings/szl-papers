# Three Machine-Checked Theorems for a Governed-AI Kernel, Framed Within a Cross-Disciplinary Methodology: Coherence-Monotone Strict Decay, a Constructive Kleene Least-Fixed-Point Characterization, and Its Unconditional ω-Continuous Strengthening

**Stephen P. Lutar Jr.**
SZL Holdings · ORCID [0009-0001-0110-4173](https://orcid.org/0009-0001-0110-4173)
Version v8 (canonical) — 2026-06-11

*This document is the single canonical consolidated thesis. It supersedes drafts v6 and v7 and is the version designated to receive a DOI. It is one cohesive paper — one abstract, one numbered section scheme, one status-tag system, one deduplicated reference list — not a concatenation of prior drafts.*

---

> **Epistemic Status Legend (used consistently throughout):**
> **[VERIFIED]** — a machine-checked Lean 4 theorem (no `sorry`, Lean-core axioms only, `lake build` green, merged to `main`), or a peer-reviewed result in the cited primary literature.
> **[CONJECTURE]** — a precisely stated open or refuted proposition (Conjecture 1 / Conjecture 2 below).
> **[PROPOSED]** — an SZL engineering construct or analogy, motivated but not formally established.
> **[FUTURE WORK]** — an explicitly deferred formalization with a named hypothesis or missing API.
> **[NARRATIVE]** — motivational framing only; not load-bearing; explicitly not treated as evidence.

---

## Abstract

We report **three machine-checked Lean 4 theorems** that together constitute the formally verified core of the SZL Holdings governed-AI kernel, and we frame them within a cross-disciplinary methodology adapted — never reclaimed — from five established research lineages. The verified core has three components. **Result I** (Wave24, `Lutar/QuantumBio/CoherenceDecay.lean`) establishes that the $\ell_1$-norm coherence of a single qubit under pure-dephasing Lindblad/GKSL dynamics, modeled as $C(t) = C_0\,e^{-\gamma t}$, is strictly antitone, non-negative, equal to $C_0$ at $t = 0$, decays to zero as $t \to \infty$, and that the engineering gate value $q\,C(t)$ crosses any closure floor $\Lambda_{\min} \in (0, qC_0)$ at a unique finite time $t^\star = (1/\gamma)\ln(qC_0/\Lambda_{\min})$. **Result II** (Wave25, `Lutar/Lambda/AggregatorLfp.lean`) gives a **constructive** Kleene iterate-supremum treatment of the Λ-aggregator least fixed point on a complete lattice: the iterate chain $\bot, \Phi\bot, \Phi^2\bot, \dots$ is monotone, bounded above by $\operatorname{lfp}\Phi$, and the exact Kleene equality $\operatorname{lfp}\Phi = \bigsqcup_n \Phi^n\bot$ holds **under an explicit ω-continuity commute hypothesis** (`lfp_eq_iSup_iterate_of_commute`). **Result III** (Wave26, same file, additive) is the **unconditional** strengthening: `lfp_eq_iSup_iterate` **drops** Wave25's explicit hypothesis by *deriving* the commute property from ω-Scott-continuity, using the Mathlib v4.18.0 ωCPO continuity API.

We state the novelty honestly and up front. **The underlying mathematics is classical** — exponential dephasing decay is the standard solution of the pure-dephasing GKSL channel ([Lindblad 1976](https://doi.org/10.1007/BF01608499); [Gorini–Kossakowski–Sudarshan 1976](https://doi.org/10.1063/1.522979); [Baumgratz–Cramer–Plenio 2014](https://doi.org/10.1103/PhysRevLett.113.140401)), and least-fixed-point / Kleene-iteration theory is due to [Knaster (1928)](https://doi.org/10.4064/fm-6-1-133-134), [Kleene (1938)](https://doi.org/10.2307/2267778), and [Tarski (1955)](https://doi.org/10.2140/pjm.1955.5.285), available in Mathlib as `OrderHom.lfp`. **What is new in this paper is neither new physics nor new pure mathematics; it is the machine-checked formalization of these classical results in Lean 4 together with their governance application** — a coherence closure-gate single-crossing certificate and a PURIQ router convergence certificate.

All three theorems are **[VERIFIED]** at the EXPERIMENTAL / CI-green tier and merged to `main`. **None ever joins the locked-proven kernel**, which remains EXACTLY the eight theorems $\{F1, F4, F7, F11, F12, F18, F19, F22\}$ at commit `c7c0ba17`. Λ-aggregator unconditional uniqueness remains **Conjecture 1** (machine-checked **FALSE**; a conditional Theorem U holds axiom-free); full Khipu BFT protocol safety remains **Conjecture 2** (a Wave23 conditional quorum-intersection lemma exists). The Results II/III convergence statements are **not** uniqueness statements and do not bear on Conjecture 1. Trust is never asserted at 100%; SLSA L1+L2 are attested with an L3 roadmap.

**Keywords:** formal verification, Lean 4, Mathlib, open quantum systems, Lindblad/GKSL, coherence monotone, least fixed point, Kleene iteration, Knaster–Tarski, ω-Scott-continuity, Byzantine fault tolerance, constrained optimization, agentic routing, governed autonomy.

---

## Contents

1. [Introduction](#1-introduction)
2. [Background and Honest Doctrine](#2-background-and-honest-doctrine)
3. [The Verified Core — Three Machine-Checked Theorems](#3-the-verified-core)
4. [Cross-Disciplinary Methodological Lineage](#4-cross-disciplinary-methodological-lineage)
5. [Applications — Live Governance Surfaces](#5-applications)
6. [Discussion, Limitations, and Future Work](#6-discussion)
7. [References](#7-references)

---

## 1. Introduction {#1-introduction}

### 1.1 The thesis: a governed-AI kernel with a verified core

This paper presents the formally verified core of the SZL Holdings governed-AI kernel and situates it within a cross-disciplinary methodology. The kernel is the substrate by which an autonomous-system governance decision is treated, at its mathematical center, as a *constrained optimization under honest uncertainty*: constraints are stated explicitly and never disguised as theorems, the objective is the correct objective for the resource structure, and every claim carries a precisely labeled epistemic status. The verified core of that kernel is now **three machine-checked Lean 4 theorems**, each of which has passed `lake build` with no `sorry` and with an axiom footprint confined to the Lean-core kernel set $\{\texttt{propext}, \texttt{Classical.choice}, \texttt{Quot.sound}\}$, and each of which is merged to `main` on `szl-holdings/lutar-lean`.

The three theorems formalize, in the same proof assistant and under the same honesty doctrine, the two characteristic monotone dynamics the kernel's runtime gate and router actually rely on, plus the strengthening that removes a hypothesis from the second:

- **Result I (Wave24)** is a *dynamical* result for the SZL Λ-v5 coherence gate. The locked-proven kernel already contains *static* gate lemmas (a decohered node never closes; a discharged node never closes; the gate is monotone in coherence and in charge). Result I supplies the time-dynamics those statics never touched: under pure-dephasing Lindblad dynamics the coherence $C(t) = C_0\,e^{-\gamma t}$ is strictly decreasing, decays to zero, and the gate value crosses any closure floor at a unique finite time $t^\star$. This is the machine-checked backbone behind the $\tau_c = 1/\gamma$ parameter exposed at the live `/api/<ns>/v1/qbio/coherence` endpoint.

- **Result II (Wave25)** is a *constructive convergence* result for the Λ-aggregator routing function. An existing kernel result (Round5 `OuroborosKleeneHalt`) already proves that a monotone operator on a complete lattice has a least fixed point — an *existence* statement. Result II supplies the constructive content that existence alone does not give: the Kleene iterate chain $\bot, \Phi\bot, \Phi^2\bot, \dots$ is monotone and dominated by $\operatorname{lfp}\Phi$, and under an explicit ω-continuity commute hypothesis the least fixed point *equals* the iterate supremum.

- **Result III (Wave26)** is the *unconditional strengthening* of Result II. It drops the explicit commute hypothesis Wave25 carried, by *deriving* the commute property automatically from ω-Scott-continuity via the Mathlib ωCPO continuity API. This is the standard Kleene fixpoint theorem, now machine-checked in the form that requires only the natural continuity hypothesis rather than an assumed commutation.

These results are coherent as one advance because they capture two dual monotone behaviors and the convergence guarantee that ties them to a running system. Result I is an antitone-decay statement over the totally ordered reals, where the order-theoretic content — a strictly decreasing function meets each level at most once — is realized analytically through the exponential and the logarithm. Results II and III are monotone-ascent statements over an abstract complete lattice, where the order-theoretic content — a monotone iterate chain ascends to a least fixed point — is realized purely order-theoretically through suprema and Knaster–Tarski–Kleene theory. The kernel's runtime needs both: the Λ-v5 gate decays toward and crosses a floor (Result I), while the Λ-aggregator's routing weights ascend toward and settle at a stable assignment (Results II/III). Presenting them together is therefore a statement about the kernel's two characteristic monotone dynamics, not a packaging convenience.

### 1.2 The honest novelty framing — stated up front

We are explicit about what is and is not new, because the value of a formalization paper lies precisely in its honesty about provenance.

**The underlying mathematics in all three results is classical and is not claimed as an SZL discovery.** Exponential dephasing decay of off-diagonal coherence is the textbook solution of the pure-dephasing GKSL master equation, due to [Lindblad (1976)](https://doi.org/10.1007/BF01608499) and [Gorini, Kossakowski, and Sudarshan (1976)](https://doi.org/10.1063/1.522979), with the $\ell_1$-norm coherence monotone introduced by [Baumgratz, Cramer, and Plenio (2014)](https://doi.org/10.1103/PhysRevLett.113.140401). Least-fixed-point theory on complete lattices is due to [Knaster (1928)](https://doi.org/10.4064/fm-6-1-133-134) and [Tarski (1955)](https://doi.org/10.2140/pjm.1955.5.285); the iterate-supremum characterization is [Kleene's (1938)](https://doi.org/10.2307/2267778) first recursion theorem, and the least-fixed-point operator `OrderHom.lfp` is already in Mathlib ([`Order.FixedPoints`](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Order/FixedPoints.html)).

We therefore state the contribution in one sentence, reused verbatim as the doctrine of this paper:

> **What is new in this paper is neither new physics nor new pure mathematics; it is the machine-checked formalization of these classical results in Lean 4 together with their governance application.**

Concretely, the contributions are a coherence closure-gate single-crossing certificate (Result I) and a PURIQ router convergence certificate (Results II/III), both machine-checked. We claim no new physics and no new pure mathematics. We claim a verified bridge from classical results to a governed-AI kernel, and we claim that this bridge is now machine-checked.

This is the evolution across the SZL draft history. The broad prior draft (v6) advanced a five-lineage unifying narrative with a single staged-PROPOSED theorem; the focused draft (v7) tightened to *exactly two* `lake`-VERIFIED results. This canonical version (v8) presents *three* VERIFIED theorems — adding the Wave26 unconditional strengthening — and reframes the broad five-lineage material as a clearly labeled cross-disciplinary *context* chapter (§4) rather than as results.

### 1.3 What this paper does not claim

This paper does not claim new physics, new pure mathematics, the unconditional optimality of any SZL routing function, or any compliance attestation beyond the precisely stated SLSA L1+L2 (with an L3 roadmap). It does not enlarge the locked-proven kernel. It does not reclaim the Round5 existence result, the Wave23 conditional quorum lemma, or any cited author's theorem. Every borrowed result is attributed to its real author with a primary DOI or arXiv link, and every borrowed formula in §4 is explicitly labeled as a [PROPOSED] or [NARRATIVE] analogy. No assertion in this paper depends on any [NARRATIVE] framing.

---

## 2. Background and Honest Doctrine {#2-background-and-honest-doctrine}

### 2.1 The locked-proven kernel: EXACTLY eight

**[VERIFIED]** The locked-proven set contains exactly eight machine-checked, `sorry`-free Lean 4 theorems, frozen at commit `c7c0ba17`:

$$
\mathcal{K}_{\text{locked}} = \{F1,\ F4,\ F7,\ F11,\ F12,\ F18,\ F19,\ F22\}.
$$

This count is a **hard doctrine invariant**. The three theorems presented in §3 are EXPERIMENTAL / CI-green tier and **never** enter $\mathcal{K}_{\text{locked}}$; they sit alongside it as separately scoped, separately gated modules. The eight cover the append-only log invariants, the Λ-v5 gate statics, and the routing-DAG acyclicity preconditions; their precise statements live in the versioned source at `c7c0ba17` and are not paraphrased here to avoid drift. In brief: F1 fixes the governance-predicate type-correctness; F4 the append-only log monotonicity (the Khipu receipt log is non-decreasing under admissible operations); F7 the agent-execution-DAG acyclicity precondition; F11/F12 the closure well-posedness (a decohered node and an uncharged node never satisfy `closureOk`); F18/F19 the Λ-gate monotonicity in coherence and in charge; F22 the FIFO ordering invariant of the append-only log under concurrent execution.

### 2.2 Conjecture 1 — Λ-aggregator unconditional uniqueness is machine-checked FALSE

**[CONJECTURE 1 — machine-checked FALSE unconditionally]** The proposition that the formal Λ-aggregator is the *unique* routing function satisfying a fixed set of governance axioms across all regimes is Conjecture 1. It has been machine-checked in Lean 4 and found **false** in its unconditional form: counterexample configurations exist in which a distinct routing function satisfies all asserted axioms. A **conditional Theorem U** does hold **axiom-free** under explicit preconditions (bounded coherence, non-degenerate charge, bounded tier-weight differences); it is not in the locked-8 and is cited only for completeness, because its preconditions prevent it from being a general governance theorem.

The practical consequence is doctrinally fixed: **Λ-v5 is an engineering gate, not the formal aggregator**, and any unqualified reference to "the Λ gate" means the engineering gate Λ-v5 (`lambdaVal = coherence · charge`), never the formal aggregator of Conjecture 1. Crucially, **Results II and III below are convergence statements, not uniqueness statements**: they characterize the *least* fixed point constructively and say nothing about uniqueness of routing functions, so they do not bear on Conjecture 1 and must never be conflated with it.

### 2.3 Conjecture 2 — full Khipu BFT protocol safety

**[CONJECTURE 2 — conditional lemma exists (Wave23); full protocol proof open]** The proposition that the Khipu BFT protocol is safe under all admissible Byzantine faults is Conjecture 2. A *conditional* quorum-intersection lemma — that any two $(2f+1)$-quorums in a $(3f+1)$-validator set share at least $f+1$ members, hence at least one honest witness — was established as Wave23 conditional work (via `Finset` inclusion–exclusion: $|Q_1 \cap Q_2| = |Q_1| + |Q_2| - |Q_1 \cup Q_2| \geq (2f{+}1)+(2f{+}1)-(3f{+}1) = f{+}1$) and is **cited, not reclaimed**, here. It is conditional on honest non-equivocation and $|V| = 3f+1$. What remains open is the protocol-level safety-and-liveness proof (DAG construction, certification, commit rules, adversarial timing), analogous to the gap between the Bythos Coq result ([Pîrlea et al., CCS 2024](https://doi.org/10.1145/3658644.3690355)) and full mechanized protocol proofs such as Mysticeti in Rocq ([Qiu, Xiao, Shao, IEEE S&P 2026](https://flint.cs.yale.edu/flint/publications/sp26.pdf)), the latter of which surfaced a liveness bug the combinatorial lemma alone could not catch.

### 2.4 The four-tier ladder and where the three theorems sit

SZL doctrine distinguishes four formal tiers:

1. **locked-proven** — the immutable eight at `c7c0ba17`;
2. **EXPERIMENTAL / CI-green** — machine-checked, `lake`-green, merged, but outside the governed surface and never folded into the eight;
3. **CONJECTURE** — precisely stated, including the refuted Conjecture 1 and the open Conjecture 2;
4. **PROPOSED / FUTURE WORK** — engineering analogies and deferred formalizations.

All three of Results I, II, and III are **EXPERIMENTAL / CI-green**. They are real, machine-checked theorems; they are simply not — and by doctrine never will be — members of the locked eight.

### 2.5 Supply-chain and trust doctrine

**[VERIFIED — attested]** SZL attests **SLSA Level 1 and Level 2** supply-chain security (documented provenance, signed artifacts, automated reproducible build). **SLSA Level 3, FedRAMP authorization, CMMC certification, and ATO are roadmap items** and must never be asserted as current status. **Trust is never claimed at 100%.** Machine-checked verification provides certainty *within the scope of the stated axioms and the Lean 4 + Mathlib computational trust model* — and not beyond. Any narrative framing sometimes associated with the SZL program — including Jack Kruse's quantum-biology assertions — is **[NARRATIVE]** only; no theorem or claim in this paper depends on it.

---

## 3. The Verified Core — Three Machine-Checked Theorems {#3-the-verified-core}

This section is the heart of the paper. It presents the three machine-checked theorems with their real Lean 4 statements, their axiom ledgers, and a unified methodology subsection covering verification, the bug found and fixed, and the scope guard that keeps the locked eight untouched.

### 3.1 Result I — Coherence Monotone Strict Decay (Wave24)

#### 3.1.1 What is new here versus the existing kernel

The kernel module `Lutar/QuantumBio/SZL_v5.lean` already proves *static* properties of the Λ-v5 engineering gate `lambdaVal = coherence · charge` (`decohered_never_closes`, `uncharged_never_closes`, `lambda_mono_in_coherence`). Result I (`Lutar/QuantumBio/CoherenceDecay.lean`, namespace `Lutar.QuantumBio.CoherenceDecay`, Apache-2.0, © 2026 Stephen P. Lutar Jr.) proves the *time-dynamics* those statics never touched. It is merged on `main` and `lake`-green.

#### 3.1.2 Physical setting (classical input)

**[VERIFIED — classical literature]** A two-level system (qubit) evolving under the Lindblad/GKSL master equation,

$$
\frac{d\rho}{dt} = -\tfrac{i}{\hbar}[H,\rho] + \sum_k \gamma_k\!\left(L_k \rho L_k^\dagger - \tfrac12\{L_k^\dagger L_k,\rho\}\right),
$$

is the unique generator of a completely positive trace-preserving dynamical semigroup ([Lindblad 1976](https://doi.org/10.1007/BF01608499); [GKS 1976](https://doi.org/10.1063/1.522979)). For the pure-dephasing channel (diagonal Lindblad operators, $H=0$) the off-diagonal element decays as $\rho_{12}(t) = \rho_{12}(0)\,e^{-\gamma t}$, and the Baumgratz–Cramer–Plenio $\ell_1$-norm coherence monotone $C_{\ell_1}(\rho)=\sum_{i\neq j}|\rho_{ij}| = 2|\rho_{12}|$ ([BCP 2014](https://doi.org/10.1103/PhysRevLett.113.140401)) therefore obeys

$$
C(t) = 2|\rho_{12}(0)|\,e^{-\gamma t} = C_0\,e^{-\gamma t}.
$$

This equation is the **classical physical input**; the Lean theorem does not re-derive quantum mechanics (Mathlib has no GKSL formalization). What Result I machine-checks are the order-theoretic and analytic consequences of this model, and the single-crossing of the gate floor. This conditionality mirrors the structure of every borrowed lineage in §4 — each result is conditional on a clearly stated domain of validity.

#### 3.1.3 Full theorem statements

The module defines the coherence function

```lean
noncomputable def coh (C0 γ t : ℝ) : ℝ := C0 * Real.exp (-(γ * t))
```

and proves the following, quoted from the merged `main`:

**Strict antitonicity (`coh_strictAnti`)** — coherence is only ever lost, never regained:

```lean
theorem coh_strictAnti (C0 γ : ℝ) (hC : 0 < C0) (hγ : 0 < γ) :
    StrictAnti (coh C0 γ)
```

**Non-negativity (`coh_nonneg`)**:

```lean
theorem coh_nonneg (C0 γ t : ℝ) (hC : 0 ≤ C0) : 0 ≤ coh C0 γ t
```

**Initial condition (`coh_zero`)** — at $t = 0$ coherence equals $C_0$:

```lean
@[simp] theorem coh_zero (C0 γ : ℝ) : coh C0 γ 0 = C0
```

**Decay to zero (`coh_tendsto_zero`)** — coherence vanishes in the long-time limit:

```lean
theorem coh_tendsto_zero (C0 γ : ℝ) (hγ : 0 < γ) :
    Filter.Tendsto (coh C0 γ) Filter.atTop (nhds 0)
```

The gate value at time $t$ with charge held constant at $q$ is

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

$$
t^\star = \frac{1}{\gamma}\,\ln\!\left(\frac{q\,C_0}{\Lambda_{\min}}\right) > 0,
$$

and $0 < t^\star$ follows because the hypothesis `hhi` ($\Lambda_{\min} < qC_0$) makes the log argument exceed $1$ (`Real.log_pos`), while $1/\gamma > 0$ (closed by `positivity`). The evaluation `lambdaAt … tStar = lamMin` is closed by `field_simp`/`ring` after the exponential–log cancellation `Real.exp_log` with argument $qC_0/\Lambda_{\min}$.

**Uniqueness of the crossing time is an immediate corollary of `coh_strictAnti`**: because `lambdaAt C0 γ q t = q · coh C0 γ t` is the product of a positive constant $q$ with the strictly antitone `coh C0 γ`, it is itself strictly antitone, hence injective, so it attains the level $\Lambda_{\min}$ at exactly one argument. We label this honestly: the existence-and-value claim is the **[VERIFIED]** Lean content of `lambda_single_crossing`; the uniqueness claim is an immediate consequence of the adjacent **[VERIFIED]** lemma `coh_strictAnti`, and we do not overstate it as a distinct machine-checked theorem. The governance reading is that the gate, once it falls to the floor, is below the floor thereafter — there is no later time at which a decohering node spuriously re-qualifies for closure.

#### 3.1.4 Axiom ledger and merge status

**[VERIFIED]** `#print axioms` for every declaration in `CoherenceDecay.lean` yields a footprint contained in the Lean-core set $\{\texttt{propext}, \texttt{Classical.choice}, \texttt{Quot.sound}\}$; there is no `sorry` and no new axiom token. Supporting Mathlib lemmas are all in Mathlib4 (`Real.exp_lt_exp`, `mul_lt_mul_left`, `Real.exp_pos`, `Real.tendsto_exp_atBot`, `Filter.Tendsto.const_mul_atTop`, `Real.log_pos`, `Real.exp_log`). The file is **merged on `main`** at `szl-holdings/lutar-lean` as `Lutar/QuantumBio/CoherenceDecay.lean` and builds green. Status: **[VERIFIED] — EXPERIMENTAL / CI-green tier; never folded into $\mathcal{K}_{\text{locked}}$**; Λ-v5 remains a **[PROPOSED]** engineering gate and Conjecture 1 is untouched. To the best knowledge of the SZL research team, no prior machine-checked (Lean / Coq / Rocq / ACL2) formalization of GKSL $\ell_1$-coherence strict decay with a gate single-crossing corollary exists; the nearest prior work is the analytic resource-theory treatment of [Streltsov, Adesso, and Plenio (2017)](https://doi.org/10.1103/RevModPhys.89.041003) and the BCP framework, neither machine-checked.

### 3.2 Result II — Constructive Kleene Least Fixed Point with Commute Hypothesis (Wave25)

#### 3.2.1 What is new here versus the existing kernel

The kernel module `Lutar/Innovations/round5/OuroborosKleeneHalt.lean` already proves the *existence* of a least fixed point of a monotone operator on a complete lattice (Knaster–Tarski / Kleene existence via `OrderHom.lfp_eq` + `OrderHom.lfp_le`). Result II (`Lutar/Lambda/AggregatorLfp.lean`, namespace `Lutar.Lambda.AggregatorLfp`, Apache-2.0, © 2026 Stephen P. Lutar Jr.) proves the **constructive** content that existence alone does not give: the actual *computation* of the fixed point as the supremum of the Kleene iterate chain, its monotone convergence, and a route-stability certificate. **The Round5 existence result is cited, not reclaimed.** The file is merged on `main` at squash commit `357cdaa7…` (PR #226, branch `wave25/lambda-lfp-kleene`).

#### 3.2.2 Setting and the iterate chain

Working over a complete lattice `α` with a monotone self-map (`OrderHom`) `Φ : α →o α`, the module defines the Kleene iterate chain from `⊥`:

```lean
def iterate (Φ : α →o α) (n : ℕ) : α := (Φ^[n]) ⊥

@[simp] theorem iterate_zero (Φ : α →o α) : iterate Φ 0 = ⊥ := rfl

theorem iterate_succ (Φ : α →o α) (n : ℕ) :
    iterate Φ (n + 1) = Φ (iterate Φ n)
```

#### 3.2.3 Full theorem statements

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

#### 3.2.4 Constructive content versus existence; and the honest commute hypothesis

The Round5 result answers *does a fixed point exist?* Result II answers *what is it, and how is it reached?* An existence proof (Knaster–Tarski takes $\operatorname{lfp}\Phi$ to be the infimum of all pre-fixed points) certifies that a self-consistent routing assignment exists, but it does not exhibit a procedure that approaches it, nor does it certify that iterative refinement from the empty assignment $\bot$ makes monotone progress. A router that must *run* needs the constructive guarantee: that repeated aggregation $\bot \to \Phi\bot \to \Phi^2\bot \to \dots$ never undoes earlier progress, stays below the target, and — under the stated continuity hypothesis — reaches it in the limit. Concretely, `iterate_mono` shows the chain $\bot \leq \Phi\bot \leq \Phi^2\bot \leq \dots$ never regresses; `iterate_le_lfp` and `iSup_iterate_le_lfp` bound the chain and its supremum below $\operatorname{lfp}\Phi$; `lfp_least` certifies $\operatorname{lfp}\Phi$ as the *minimal* self-consistent assignment; and `lfp_eq_iSup_iterate_of_commute` delivers the exact Kleene equality $\operatorname{lfp}\Phi = \bigsqcup_n \Phi^n\bot$ once the ω-continuity commute property is supplied.

The honesty discipline here is exact. `lfp_eq_iSup_iterate_of_commute` takes ω-continuity in the form of the **explicit hypothesis** `hcommute : Φ (⨆ n, iterate Φ n) = ⨆ n, Φ (iterate Φ n)`. The $\leq$ direction of the equality is immediate from `iSup_iterate_le_lfp`; the $\geq$ direction follows once the commute property is supplied. Wave25 deliberately does **not** assert that `Φ` is automatically ω-Scott-continuous, and it does not invoke a fragile continuity-API name as proven. The theorem is exactly as strong as its stated hypothesis, no more — and deriving that hypothesis from ω-Scott-continuity is precisely the strengthening delivered by Result III (§3.3).

#### 3.2.5 Axiom ledger and merge status

**[VERIFIED]** `#print axioms` for the Wave25 declarations: `iterate_zero`, `iterate_succ`, `lfp_is_fixed`, `lfp_least`, `iterate_le_lfp`, `iSup_iterate_le_lfp`, `iterate_succ_le_map_iSup`, `lfp_eq_iSup_iterate_of_commute`, and `lambda_route_stable` reduce to $\{\texttt{propext}, \texttt{Quot.sound}\}$; `iterate_mono` reduces to $\{\texttt{propext}, \texttt{Classical.choice}, \texttt{Quot.sound}\}$. All are subsets of the Lean-core kernel set; no new axiom token, no `sorry`. The file is merged to `main` at squash commit `357cdaa7…` with a `Signed-off-by: Stephen P. Lutar Jr.` DCO trailer; all required branch-protection checks (`lake build + numbers`, `DCO sign-off`, `overclaim / Governed surfaces are honest`) were green. Status: **[VERIFIED] — EXPERIMENTAL / CI-green tier; never folded into $\mathcal{K}_{\text{locked}}$**.

### 3.3 Result III — Unconditional Kleene Least Fixed Point from ω-Scott-Continuity (Wave26)

#### 3.3.1 The strengthening: dropping Wave25's hypothesis

Result III (`lfp_eq_iSup_iterate`, same file `Lutar/Lambda/AggregatorLfp.lean`, purely additive — the first 128 lines of the Wave25 file are byte-identical) is the unconditional Kleene fixpoint theorem for the Λ-aggregator. Where Wave25's `lfp_eq_iSup_iterate_of_commute` carries the explicit commute hypothesis as an assumption, Wave26 *derives* that commute property automatically from ω-Scott-continuity, leaving only the natural continuity hypothesis:

```lean
theorem lfp_eq_iSup_iterate (Φ : α →o α)
    (hΦ : OmegaCompletePartialOrder.ωScottContinuous (Φ : α → α)) :
    lfp Φ = ⨆ n, iterate Φ n := by
  let c : OmegaCompletePartialOrder.Chain α := ⟨iterate Φ, iterate_mono Φ⟩
  have hmap := hΦ.map_ωSup c
  have hcommute : Φ (⨆ n, iterate Φ n) = ⨆ n, Φ (iterate Φ n) := by
    have hL : (⨆ n, iterate Φ n) = OmegaCompletePartialOrder.ωSup c := rfl
    have hR : (⨆ n, Φ (iterate Φ n))
        = OmegaCompletePartialOrder.ωSup (c.map ⟨Φ, hΦ.monotone⟩) := rfl
    rw [hL, hR, hmap]
  exact lfp_eq_iSup_iterate_of_commute Φ hcommute
```

This is the standard Kleene fixpoint theorem in its natural form. It remains a **convergence** result — the constructive computation of the lfp — and is explicitly **not** a uniqueness claim, so it does not bear on Conjecture 1.

#### 3.3.2 The Mathlib v4.18.0 ω-continuity API used

The mechanism, verified by building against Mathlib v4.18.0, rests on the following ωCPO API from `Mathlib/Order/OmegaCompletePartialOrder.lean` (as documented in the Wave26 result record):

- **`OmegaCompletePartialOrder.ωScottContinuous (f : α → β) : Prop`** — the ω-Scott-continuity predicate, requiring `[OmegaCompletePartialOrder α] [OmegaCompletePartialOrder β]`. This is the correct, minimal predicate for an ℕ-chain; `ScottContinuous` (over all directed sets) is strictly stronger, and `ScottContinuous.ωScottContinuous` exists but is not needed.
- **`OmegaCompletePartialOrder.Chain α := ℕ →o α`** — a chain is a monotone ℕ-indexed sequence; the Wave25 `iterate_mono` shows the Kleene iterate sequence is exactly such a chain.
- **`ωScottContinuous.map_ωSup (hf) (c : Chain α) : f (ωSup c) = ωSup (c.map ⟨f, hf.monotone⟩)`** — the distribution-over-ωSup lemma.
- **`ωScottContinuous.monotone`** — extracts the underlying monotonicity used to build `c.map ⟨Φ, hΦ.monotone⟩`.
- **The `CompleteLattice → OmegaCompletePartialOrder` instance** (priority 100): for `[CompleteLattice α]`, the ωCPO `ωSup c` is *definitionally* `⨆ i, c i`. This is the load-bearing fact: the two `rfl`s in `hL` and `hR` witness that, on a complete lattice, the ωCPO `ωSup` and the lattice `⨆` coincide, and that `Chain.map` coerces to function composition. Consequently `map_ωSup` literally *is* the `iSup`-phrased commute property up to `rfl`, after which the proof discharges through the preserved Wave25 antisymmetry argument unchanged.

#### 3.3.3 Axiom ledger and merge status

**[VERIFIED]** Per the Wave26 result record (PR [#227](https://github.com/szl-holdings/lutar-lean/pull/227), branch `wave26/lambda-kleene-unconditional` off `main` @ `1e3cd90b…`, commit `6feeee59…`, DCO-signed):

```
Lutar.Lambda.AggregatorLfp.lfp_eq_iSup_iterate            : {propext, Classical.choice, Quot.sound}
Lutar.Lambda.AggregatorLfp.lfp_eq_iSup_iterate_of_commute : {propext, Quot.sound}   (Wave25, preserved)
```

Both footprints are subsets of the Lean-core set $\{\texttt{propext}, \texttt{Classical.choice}, \texttt{Quot.sound}\}$; there is no `sorryAx`, no `sorry`/`admit`, and no new declared `axiom` token. Local verification under the real compiler (Lean v4.18.0 + Mathlib v4.18.0) reported `lake env lean … → exit 0`, `lake build Lutar.Lambda.AggregatorLfp → ✔ [545/545] Built … Build completed successfully`, and `#print axioms lfp_eq_iSup_iterate → [propext, Classical.choice, Quot.sound]`; the full-library `lake build` was completed under CI, which holds the complete prebuilt Mathlib cache. The change is purely additive: Wave25's `lfp_eq_iSup_iterate_of_commute` and all other Wave25 theorems are untouched (first 128 lines byte-identical), and the Round5 existence result is not reclaimed. Status: **[VERIFIED] — EXPERIMENTAL / CI-green tier; never folded into $\mathcal{K}_{\text{locked}}$**.

### 3.4 Methodology — How the Three Were Verified

#### 3.4.1 The Lean 4 + Mathlib trust model

**[VERIFIED — within stated scope]** A machine-checked theorem in Lean 4 is a term whose type is the theorem statement and which the Lean kernel accepts. The trust base is therefore the Lean kernel together with the three classical axioms permitted by SZL doctrine — `propext` (propositional extensionality), `Classical.choice` (the axiom of choice), and `Quot.sound` (soundness of quotients) — and nothing else. The `#print axioms` command enumerates exactly which of these a declaration depends on; a footprint contained in $\{\texttt{propext}, \texttt{Classical.choice}, \texttt{Quot.sound}\}$ means no `sorry`, no ad-hoc `axiom`, and no `native_decide`-style escape hatch is load-bearing. This is the precise, bounded sense in which the three results are certain: certain relative to the soundness of the Lean kernel and these three axioms, and to the faithfulness of each statement to its intended meaning. It is not certainty about the physical world (the GKSL model is an input, not a Lean-internal derivation), nor about the appropriateness of the lattice model of routing weights. Naming the trust base explicitly is how the "trust is never 100%" doctrine is made operational rather than rhetorical.

#### 3.4.2 Toolchain and the verification contract

**[VERIFIED]** All three theorems were checked with **Lean 4 v4.18.0 + Mathlib v4.18.0** (manifest pin `aa936c36` @ v4.18.0). The verification contract for the EXPERIMENTAL / CI-green tier has four conjuncts, all of which each file satisfies: (i) `lake build` of the module succeeds; (ii) no `sorry` appears anywhere in the file; (iii) `#print axioms` for every declaration is a subset of the Lean-core kernel set; and (iv) the green build is reproduced under CI on the branch and on `main`. The `AggregatorLfp` module (Results II and III) was built locally against the repo's pinned toolchain using the Mathlib binary cache, then re-checked under CI; `CoherenceDecay` (Result I) builds green on `main`.

#### 3.4.3 An honesty note: a real engineering bug, found and fixed

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

No statement was changed, no `sorry` introduced, nothing trivialized, and no existence result reclaimed. This is the value proposition of machine-checking stated concretely: a subtle `rw` over-rewrite that would have been easy to miss in a paper proof was caught by the kernel and corrected, and the corrected proof is what shipped to `main` — and what Result III later reuses unchanged as the chain-monotonicity input.

#### 3.4.4 Scope guard — none of the three is a governed surface

**[VERIFIED]** A material methodological point distinguishes the EXPERIMENTAL tier from the locked eight: the VERIFIED_THEOREMS drift gate (generator `gen_verified_theorems.py`) scans only the `GOVERNANCE_SURFACE` allow-list (`Lutar/Uniqueness.lean`, `Lutar/Uniqueness/`, `Lutar/Round13/Lambda_Uniqueness.lean`), and the `sorry_gate.py` step is scoped to `Lutar/Uniqueness` only. Neither `Lutar/QuantumBio/CoherenceDecay.lean` nor `Lutar/Lambda/AggregatorLfp.lean` is a governed surface, so neither appears in the governed-theorem count and neither can perturb $\mathcal{K}_{\text{locked}}$. The live `lean_numbers.py` step recomputes and uploads a measurement artifact but is not wired as a blocking numbers gate; verification confirmed that adding `Lutar/Lambda/` as an experimental scope would have been *wrong*, because pre-existing counted files (`Lutar/Lambda/CompositionRing.lean`, `Lutar/Lambda/SchurConcave.lean`) would then have been excluded and *caused* drift. The locked-8 count is thereby provably undisturbed by all three results.

---

## 4. Cross-Disciplinary Methodological Lineage {#4-cross-disciplinary-methodological-lineage}

This chapter provides the cross-disciplinary *context* for the kernel. It is **adapted methodological structure, not new results.** It catalogs five research lineages whose formalisms motivate SZL's architecture, attributes every borrowed formula to its real author with a real DOI or URL, and labels every borrowing explicitly as **[PROPOSED]** analogy or **[NARRATIVE]** framing. **SZL claims only the methodological structure — the discipline of treating governance as constrained optimization under honest uncertainty — never the original results, which belong to their cited authors.** The unifying thesis is that every well-posed autonomous-system governance decision is a constrained optimization under honest uncertainty; this framing is the epistemic discipline of rigorous engineering, not an SZL invention.

### 4.1 Sherman Morgan — fixed-resource constrained optimization

**Original result (not SZL's).** Mary Sherman Morgan, a Theoretical Performance Specialist at Rocketdyne / North American Aviation (1956–1958), solved a canonical constrained-optimization problem: replace the Redstone/Jupiter-C propellant under the constraint that no aspect of the A-7 engine could change, maximizing the density-specific impulse

$$
I_{sp,\rho} = \rho_{\text{mix}} \cdot I_{sp}
$$

subject to fixed tank volume, fixed nozzle geometry, fixed oxidizer, and feasibility constraints. Her solution — Hydyne (60% UDMH / 40% DETA) — launched Explorer 1 on 1958-01-31 ([Chemistry World, 2021](https://www.chemistryworld.com/culture/mary-sherman-morgan-the-best-kept-secret-in-the-space-race/4013329.article); [NASA NTRS: Rho-Isp](https://ntrs.nasa.gov/citations/20150016561)). The methodological lesson: when the container is fixed, the correct merit function is energy per unit *volume*, not per unit *mass*. The related Tsiolkovsky rocket equation $\Delta v = I_{sp}\,g_0\,\ln(m_0/m_f)$ ([NASA Glenn](https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/ideal-rocket-equation/)) expresses a conserved quantity bounded by a log-ratio of resources.

**SZL adaptation [PROPOSED].** In the SZL tier/budget router, the analogous merit function is *capability-per-token*, not raw capability — the token budget is the "tank volume," routing-tier capability is the "$I_{sp}$." The Tsiolkovsky log-ratio motivates a diminishing-returns prior for multi-tier routing. These are **[PROPOSED]** analogies that motivate architecture; they do not prove the router optimal. The original propulsion results remain Morgan's and Tsiolkovsky's.

### 4.2 Stewart — planetary-impact diagnostics, EOS, and angular momentum

**Original results (not SZL's).** Sarah T. Stewart and collaborators developed the LS12 collision-scaling framework, the catastrophic-disruption criterion $Q^*_{RD}$, and the five collision-outcome regimes classified by the ratio $Q_R/Q^*_{RD}$ ([Leinhardt & Stewart 2012, *ApJ* 745, 79](https://doi.org/10.1088/0004-637X/745/1/79)); the angular-momentum-conserving giant-impact model ([Ćuk & Stewart 2012, *Science* 338, 1047](https://doi.org/10.1126/science.1225542)); the Corotation Limit (CoRoL) and synestia model, in which a body forms a synestia iff its angular momentum exceeds a **multivariate threshold surface** $L > L_{\text{CoRoL}}(M, S_{\text{outer}}, Z)$ ([Lock & Stewart 2017, *JGR:P* 122, 950](https://doi.org/10.1002/2016JE005239)); and the Hugoniot/M-ANEOS physics-to-math EOS pipeline ([Stewart et al. 2020, *AIP Conf. Proc.* 2272, 080003](https://doi.org/10.1063/12.0000946); shock-vaporization entropy thresholds, [Kraus et al. 2012, *JGR:P* 117, E09009](https://doi.org/10.1029/2012JE004082)). **These results are Stewart's, Leinhardt's, Ćuk's, and Lock's; SZL makes no claim to them.**

**SZL adaptation [PROPOSED].** Three methodological analogies follow. First, *invariant-based regime classification*: the LS12 $Q_R/Q^*_{RD}$ ratio is the template for SZL's [PROPOSED] 3D drone/vessel collision visualization, classifying outcomes by a dimensionless energy ratio. Second, the CoRoL as a *phase-boundary surface*: the Λ-v5 closure gate is, by analogy, a surface in (coherence, charge, time) space rather than a scalar threshold — motivating future environment-responsive gating. Third, the *Hugoniot/EOS pipeline as a verification-pipeline analogue*: experiment → Hugoniot fit → entropy integration → phase-boundary calibration → embedding maps to specification → formal model → Lean theorem → machine-checked verification → deployment, with each stage honest about its domain of validity. All three are **[PROPOSED]** analogies; the borrowed formulas and the conserved-quantity unifying view (entropy and angular momentum as the right diagnostics relative to a threshold surface) remain Stewart's group's, cited above.

### 4.3 Open-quantum coherence — the conservation-law unifying view

**Original results (not SZL's).** The GKSL equation is the unique generator of a CPTP semigroup ([Lindblad 1976](https://doi.org/10.1007/BF01608499); [GKS 1976](https://doi.org/10.1063/1.522979)); the $\ell_1$-norm coherence $C_{\ell_1}(\rho)=\sum_{i\neq j}|\rho_{ij}|$ is a valid monotone, strictly decreasing under incoherent operations ([BCP 2014](https://doi.org/10.1103/PhysRevLett.113.140401); resource-theory review, [Streltsov, Adesso, Plenio 2017](https://doi.org/10.1103/RevModPhys.89.041003)). This is the same physics that §3.1 formalizes. The unifying methodological view across §4.1–4.3 is that each domain identifies a *conserved or monotone quantity* (Δv, angular momentum, entropy, coherence) and a *threshold surface* across which a regime changes — the same structure as the Λ-v5 closure floor and the BFT safety floor below.

**SZL role [PROPOSED → VERIFIED in §3.1].** As a methodological lineage this is **[PROPOSED]**: coherence as a monotone-decreasing resource furnishes the physically grounded decay function for the Λ-v5 gate. The *formalization* of that decay (Result I) is the [VERIFIED] machine-checked contribution of §3.1; the methodological framing here is context for it.

### 4.4 Byzantine fault tolerance — a combinatorial safety threshold

**Original results (not SZL's).** The quorum-intersection lemma — for $|V| = 3f+1$, any two $(2f+1)$-quorums share $\geq f+1$ members, hence an honest witness — is the combinatorial heart of all BFT protocols ([Castro & Liskov, OSDI 1999](https://pmg.csail.mit.edu/papers/osdi99.pdf)). The state of the art in mechanized BFT proofs includes Bythos in Coq ([Pîrlea et al., CCS 2024](https://doi.org/10.1145/3658644.3690355)), Mysticeti in Rocq ([Qiu, Xiao, Shao, IEEE S&P 2026](https://flint.cs.yale.edu/flint/publications/sp26.pdf)), and AleoBFT in ACL2 ([Losa et al., Provable.com 2024](https://provable.com/blog/creating-aleobft-formal-verification-milestone)).

**SZL role [PROPOSED / CONJECTURE 2].** The quorum-intersection lemma shares the same methodological structure — a safety threshold below which a regime (Byzantine takeover) cannot be guaranteed safe — as the LS12 disruption criterion and the Λ-v5 floor. As established in §2.3, the Wave23 conditional lemma is *cited, not reclaimed*, and full Khipu BFT protocol safety is the open **Conjecture 2**.

### 4.5 Agentic routing — the application domain

**Original results (not SZL's).** Graph-based and learned routers for LLM selection are an active research area: [Feng, Shen, You (GraphRouter, ICLR 2025)](https://arxiv.org/abs/2410.03834); looped/latent-reasoning language models ([Ouro, arXiv:2510.25741](https://arxiv.org/abs/2510.25741)); automated agentic-system design ([Hu, Lu, Clune, arXiv:2408.08435](https://arxiv.org/abs/2408.08435)); cross-domain foundation models ([Polymathic AI](https://polymathic-ai.org)). **These are the cited authors' results; SZL makes no claim to them.**

**SZL role [PROPOSED → VERIFIED in §3.2–3.3].** Agentic routing is the application domain for the Λ-aggregator convergence certificate. The methodological framing — that a router should monotonically accumulate evidence until it commits to a tier — is **[PROPOSED]**; the *formalization* of that convergence (Results II and III) is the [VERIFIED] contribution of §3.2–3.3. Were the Λ-aggregator to be learned from multi-domain data, the Knaster–Tarski–Kleene framework would still apply provided the learned function is monotone (and, for the exact iterate-supremum equality, ω-Scott-continuous).

### 4.6 A note on [NARRATIVE]-only material

The quantum-biology assertions sometimes associated with the SZL program — including those of **Jack Kruse**, which are **[NARRATIVE]** only — are motivational framing and are explicitly not load-bearing. The connection between Result I's single-qubit pure-dephasing model and biological coherence phenomena (the radical-pair compass of [Hiscock et al. 2016](https://doi.org/10.1073/pnas.1600341113); FMO coherence revised downward by [Cao et al. 2020](https://doi.org/10.1126/sciadv.eaaz4888)) is likewise **[NARRATIVE]**, since those involve different decoherence channels. No theorem or claim in this paper depends on any such framing.

---

## 5. Applications — Live Governance Surfaces {#5-applications}

The three verified theorems are not abstract exercises; each underwrites a live governance surface.

### 5.1 Closure-gate single-crossing certificate (Result I) — `/api/<ns>/v1/qbio/coherence`

The decay time $\tau_c = 1/\gamma$ is the parameter exposed by the live `/api/<ns>/v1/qbio/coherence` endpoint. Result I certifies that this endpoint's coherence decay is not merely phenomenological: it is the strictly antitone exponential mandated by the pure-dephasing GKSL model, and the Λ-v5 gate crosses its floor at the unique finite time $t^\star = \tau_c \ln(qC_0/\Lambda_{\min})$. The closure floor $\Lambda_{\min}$ is a **[PROPOSED]** engineering parameter set by deployment configuration; Result I says *given* a floor in $(0, qC_0)$ the gate crosses it uniquely, not what value the floor *should* take. The single-crossing-and-no-recovery property is the honest dynamical content behind the static `closureOk` / `decohered_never_closes` locked lemmas.

### 5.2 Router convergence certificate (Results II/III) — PURIQ tier/budget router

`lambda_route_stable` instantiates the fixed-point machinery for the Λ-aggregator: at $\operatorname{lfp}\Lambda$ the routing weights are stable under one further aggregation step. This is the honest "the tier choice has converged" certificate used by the PURIQ tier/budget router — a **convergence** statement, not a uniqueness claim, and therefore independent of Conjecture 1. Combined with `iterate_mono` and `lfp_least`, it certifies that the router's weight refinement is a monotone ascent to the minimal self-consistent (closure-stable) assignment. Result II certifies this under an explicit ω-continuity commute hypothesis; Result III certifies it under the natural and more usable hypothesis that the aggregator is ω-Scott-continuous, which is the form the runtime router relies on.

### 5.3 Unified-formulas endpoints — `/v1/unified/*`

The cross-disciplinary structure of §4 is surfaced through the `/v1/unified/*` family of endpoints, which expose the **[PROPOSED]** methodological analogues — the capability-per-token merit function (§4.1), the collision-regime classifier and CoRoL-style phase-boundary view (§4.2), and the conserved-quantity diagnostics (§4.3) — each labeled as a [PROPOSED] analogy in the API surface itself, never as a verified result. These endpoints are engineering conveniences that carry no load on any [VERIFIED] claim in §3.

---

## 6. Discussion, Limitations, and Future Work {#6-discussion}

### 6.1 What the three results do and do not establish

**[VERIFIED]** Result I establishes, for a single qubit under pure-dephasing Lindblad dynamics, strict antitonicity, non-negativity, the initial condition, decay to zero, and a unique finite floor-crossing. Result II establishes, for a monotone self-map on a complete lattice, the monotone Kleene iterate chain, its domination by `lfp`, minimality of `lfp`, and the exact iterate-supremum equality under an explicit commute hypothesis, with a route-stability certificate. Result III strengthens Result II by deriving that commute hypothesis from ω-Scott-continuity, yielding the unconditional Kleene fixpoint theorem. **None of the three claims new physics or new pure mathematics; all are formalizations-plus-application of classical results.**

What they do **not** establish: Result I does not re-derive GKSL dynamics inside Lean (Mathlib has no quantum-mechanics formalization), does not model multi-spin or non-Markovian systems, does not address the bioenergetic charge term, and does not prove $\tau_c$ optimal in any information-theoretic sense. Results II and III do not address uniqueness of routing functions and therefore do not touch Conjecture 1. None of the three enters the locked eight.

### 6.2 Limitations

**[VERIFIED — honest limits]** Result I's physical scope is the single-qubit pure-dephasing channel; the connection to biological coherence is **[NARRATIVE]**, since those phenomena involve different decoherence channels. Result II's exact Kleene equality is **conditional** on the explicit `hcommute` hypothesis; Result III removes that conditionality but introduces the (natural, and in the router's case satisfied) hypothesis of ω-Scott-continuity — there is no free lunch, only a more usable hypothesis. The closure floor $\Lambda_{\min}$ is a **[PROPOSED]** engineering parameter, not a derived constant. The §4 analogies are analogies, not theorems: the log-ratio structure of the Tsiolkovsky equation does not prove the budget router optimal, and the multivariate CoRoL surface does not prove the Λ-v5 condition physically correct. SLSA L3, FedRAMP, CMMC, and ATO remain roadmap items, not current status. Trust is never asserted at 100%: the certainty offered is exactly that of Lean 4 + Mathlib within the stated axioms.

### 6.3 Future work

- **Wave27 directions.** With the unconditional Kleene theorem (Result III) in hand, the natural next step is to *instantiate* the Λ-aggregator as a concrete ω-Scott-continuous `OrderHom` on the routing-weight lattice, discharging the ω-continuity hypothesis for the actual PURIQ aggregator rather than assuming it abstractly — converting the convergence certificate from a schema into a fully instantiated runtime guarantee. A parallel Wave27 direction is a charge-term formalization: a strict-monotone-decrease theorem for the bioenergetic charge term under depletion dynamics, mirroring Result I's structure, which would complete the formal treatment of both Λ-v5 factors.
- **Conjecture 1 and Conjecture 2 remain open / refuted as stated.** Conjecture 1 (Λ unconditional uniqueness) stays machine-checked FALSE; the conditional Theorem U stands. Conjecture 2 (full Khipu BFT protocol safety) awaits a protocol-level Lean 4 proof beyond the Wave23 conditional quorum lemma, analogous to the Rocq Mysticeti development.
- **Gated live-agent prose.** The optional `SZL_LOCAL_LLM_URL` integration remains **gated** and is used for live agent prose generation only; it is not part of any verified artifact and bears no load on any claim in this paper.
- **Non-Markovian coherence extension.** Extending Result I beyond pure-dephasing Markovian dynamics would require either a quantum-mechanics library for Lean 4 (none currently in Mathlib) or a suitable abstract algebraic reformulation.

### 6.4 The doctrine, restated

The three results are honest in the sense that matters: they know exactly what they prove (machine-checked, axiom-ledgered, merged), exactly what they assume (the GKSL model as input; the commute hypothesis in Result II; ω-Scott-continuity in Result III), and exactly what they do not touch (the locked eight, Conjecture 1, new physics, new mathematics). The cross-disciplinary lineage of §4 is honest in the same way: it borrows methodological structure, attributes every formula to its author, and labels every analogy. The contribution is the verified bridge from classical results to a governed-AI kernel — and the honesty about every link in that bridge. That honesty is the thesis.

---

## 7. References {#7-references}

*Single deduplicated reference list. Status of each entry follows the legend: peer-reviewed primary literature and Mathlib documentation are [VERIFIED] sources; popular and encyclopedic links are context for [PROPOSED]/[NARRATIVE] material.*

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

10. The Mathlib Community. *Mathlib4*. GitHub. [github.com/leanprover-community/mathlib4](https://github.com/leanprover-community/mathlib4)
11. Mathlib4 documentation — `Order.FixedPoints` (Knaster–Tarski, Kleene, `OrderHom.lfp`). [leanprover-community.github.io/mathlib4_docs/Mathlib/Order/FixedPoints.html](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Order/FixedPoints.html)
12. Mathlib4 documentation — `Order.OmegaCompletePartialOrder` (`ωScottContinuous`, `Chain`, `map_ωSup`, ωCPO–`CompleteLattice` instance). [leanprover-community.github.io/mathlib4_docs/Mathlib/Order/OmegaCompletePartialOrder.html](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Order/OmegaCompletePartialOrder.html)
13. Mathlib4 documentation — `Order.Monotone.Basic` (`Monotone`, `StrictAnti`, composition). [leanprover-community.github.io/mathlib4_docs/Mathlib/Order/Monotone/Basic.html](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Order/Monotone/Basic.html)
14. Mathlib4 documentation — `Analysis.SpecialFunctions.ExpDeriv` (`Real.tendsto_exp_atBot`). [leanprover-community.github.io/mathlib4_docs/Mathlib/Analysis/SpecialFunctions/ExpDeriv.html](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Analysis/SpecialFunctions/ExpDeriv.html)
15. Carneiro, M. "Lean4Lean: Towards a Verified Typechecker for Lean, in Lean." arXiv:2403.14064 (2024). [arxiv.org/abs/2403.14064](https://arxiv.org/abs/2403.14064)
16. Tang, X. "A Comprehensive Survey of the Lean 4 Theorem Prover." arXiv:2501.18639 (2025). [arxiv.org/abs/2501.18639](https://arxiv.org/abs/2501.18639)

### Byzantine Fault Tolerance (context for Conjecture 2)

17. Castro, M., Liskov, B. "Practical Byzantine Fault Tolerance." *OSDI 1999*. [pmg.csail.mit.edu/papers/osdi99.pdf](https://pmg.csail.mit.edu/papers/osdi99.pdf)
18. Pîrlea, G., Sergey, I., et al. "Compositional Verification of Composite Byzantine Protocols (Bythos)." *ACM CCS 2024*. DOI: [10.1145/3658644.3690355](https://doi.org/10.1145/3658644.3690355)
19. Qiu, L., Xiao, J., Shao, Z. "Mechanized Safety and Liveness Proofs for the Mysticeti Consensus Protocol." *IEEE S&P 2026*. [flint.cs.yale.edu/flint/publications/sp26.pdf](https://flint.cs.yale.edu/flint/publications/sp26.pdf)
20. Losa, G., et al. "AleoBFT Formal Verification Milestone." Provable.com, 2024. [provable.com/blog/creating-aleobft-formal-verification-milestone](https://provable.com/blog/creating-aleobft-formal-verification-milestone)
21. Yin, M., Malkhi, D., et al. "HotStuff: BFT Consensus in the Lens of Blockchain." *PODC 2019*. arXiv: [1803.05069](https://arxiv.org/abs/1803.05069)
22. Spiegelman, A., et al. "Mysticeti: Reaching the Latency Limits with Uncertified DAGs." *NDSS 2025*. arXiv: [2310.14821](https://arxiv.org/abs/2310.14821)

### Agentic Routing (context for the PURIQ application)

23. Feng, T., Shen, Y., You, J. "GraphRouter: A Graph-based Router for LLM Selections." *ICLR 2025*. arXiv: [2410.03834](https://arxiv.org/abs/2410.03834)
24. ByteDance AI Lab. "Scaling Latent Reasoning via Looped Language Models (Ouro)." arXiv:2510.25741 (2025). [arxiv.org/abs/2510.25741](https://arxiv.org/abs/2510.25741)
25. Hu, S., Lu, C., Clune, J. "Automated Design of Agentic Systems." arXiv:2408.08435 (2025). [arxiv.org/abs/2408.08435](https://arxiv.org/abs/2408.08435)
26. Polymathic AI. [polymathic-ai.org](https://polymathic-ai.org)

### Propulsion Optimization (Lineage 1, §4.1 — [PROPOSED] analogy)

27. Demming, A. "Mary Sherman Morgan: The best kept secret in the space race." *Chemistry World*, 2021. [chemistryworld.com](https://www.chemistryworld.com/culture/mary-sherman-morgan-the-best-kept-secret-in-the-space-race/4013329.article)
28. NASA NTRS. "Rho-Isp Revisited and Basic Stage Mass Estimating." [ntrs.nasa.gov/citations/20150016561](https://ntrs.nasa.gov/citations/20150016561)
29. NASA Glenn Research Center. "Ideal Rocket Equation." [grc.nasa.gov — ideal-rocket-equation](https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/ideal-rocket-equation/)
30. Wikipedia. "Mary Sherman Morgan." [en.wikipedia.org/wiki/Mary_Sherman_Morgan](https://en.wikipedia.org/wiki/Mary_Sherman_Morgan)
31. Wikipedia. "Tsiolkovsky rocket equation." [en.wikipedia.org/wiki/Tsiolkovsky_rocket_equation](https://en.wikipedia.org/wiki/Tsiolkovsky_rocket_equation)

### Planetary Science (Lineage 2, §4.2 — [PROPOSED] analogy)

32. Leinhardt, Z.M., Stewart, S.T. "Collisions between Gravity-Dominated Bodies: I. Outcome Regimes and Scaling Laws." *ApJ* **745**, 79 (2012). DOI: [10.1088/0004-637X/745/1/79](https://doi.org/10.1088/0004-637X/745/1/79) | arXiv: [1106.6084](https://arxiv.org/abs/1106.6084)
33. Ćuk, M., Stewart, S.T. "Making the Moon from a fast-spinning Earth." *Science* **338**, 1047–1052 (2012). DOI: [10.1126/science.1225542](https://doi.org/10.1126/science.1225542)
34. Lock, S.J., Stewart, S.T. "The structure of terrestrial bodies: Impact heating, corotation limits and synestias." *JGR: Planets* **122**, 950–982 (2017). DOI: [10.1002/2016JE005239](https://doi.org/10.1002/2016JE005239) | arXiv: [1705.07858](https://arxiv.org/abs/1705.07858)
35. Stewart, S.T., et al. "The Shock Physics of Giant Impacts: Key Requirements for the Equations of State." *AIP Conf. Proc.* **2272**, 080003 (2020). DOI: [10.1063/12.0000946](https://doi.org/10.1063/12.0000946) | arXiv: [1910.04687](https://arxiv.org/abs/1910.04687)
36. Kraus, R.G., Stewart, S.T., et al. "Shock Vaporization of Silica and the Thermodynamics of Giant Impact Events." *JGR: Planets* **117**, E09009 (2012). DOI: [10.1029/2012JE004082](https://doi.org/10.1029/2012JE004082)

### Quantum Biology ([NARRATIVE] context only)

37. Hiscock, H.G., et al. (Hore group). "The Quantum Needle of the Avian Magnetic Compass." *PNAS* **113**, 4634 (2016). DOI: [10.1073/pnas.1600341113](https://doi.org/10.1073/pnas.1600341113)
38. Cao, J., et al. "Quantum Biology Revisited." *Science Advances* **6**, eaaz4888 (2020). DOI: [10.1126/sciadv.eaaz4888](https://doi.org/10.1126/sciadv.eaaz4888)
39. Smith, L.D., Glatthard, J., Chowdhury, F.T., Kattnig, D.R. "On the Optimality of the Radical-Pair Quantum Compass." *Quantum Sci. Technol.* **9**, 035023 (2024). DOI: [10.1088/2058-9565/ad48b4](https://doi.org/10.1088/2058-9565/ad48b4) | arXiv: [2401.02923](https://arxiv.org/abs/2401.02923)

### SZL Prior Work

40. SZL Thesis v6 — *Governed Post-Determinism as Constrained Optimization Under Honest Uncertainty* (broad five-lineage draft; superseded by this v8). Internal, 2026-06-11.
41. SZL Thesis v7 — *Two Machine-Checked Theorems for a Governed-AI Kernel* (focused verified-core draft; superseded by this v8). Internal, 2026-06-11.
42. The Loop Is the Product v1/v2. DOI: [10.5281/zenodo.19867281](https://doi.org/10.5281/zenodo.19867281), [10.5281/zenodo.19934129](https://doi.org/10.5281/zenodo.19934129)
43. SZL Doctrine v2. DOI: [10.5281/zenodo.20174600](https://doi.org/10.5281/zenodo.20174600)

---

*Status tags applied throughout: **[VERIFIED]** machine-checked Lean 4 (no `sorry`, Lean-core axioms only, `lake`-green, merged) or peer-reviewed primary literature · **[CONJECTURE]** precisely stated open/refuted proposition · **[PROPOSED]** SZL engineering construct/analogy · **[FUTURE WORK]** deferred formalization · **[NARRATIVE]** motivational only, not load-bearing.*

*Locked-proven count = EXACTLY 8: $\{F1, F4, F7, F11, F12, F18, F19, F22\}$ at commit `c7c0ba17`. This count does not change in this document. The three theorems herein are EXPERIMENTAL / CI-green tier and never join the locked 8.*

*Conjecture 1: Λ-aggregator unconditional uniqueness — machine-checked FALSE unconditionally; conditional Theorem U holds axiom-free. Results II and III are convergence (not uniqueness) results and do not bear on Conjecture 1.*

*Conjecture 2: Khipu BFT full-protocol safety — conditional quorum-intersection lemma exists (Wave23); full protocol proof open.*

*Result I (Wave24): `coh`, `coh_strictAnti`, `coh_nonneg`, `coh_zero`, `coh_tendsto_zero`, `lambda_single_crossing` in `Lutar/QuantumBio/CoherenceDecay.lean` — [VERIFIED], merged on `main`, `lake`-green, axioms ⊆ {propext, Classical.choice, Quot.sound}.*

*Result II (Wave25): `iterate`, `iterate_succ`, `iterate_mono`, `lfp_is_fixed`, `lfp_least`, `iterate_le_lfp`, `iSup_iterate_le_lfp`, `iterate_succ_le_map_iSup`, `lfp_eq_iSup_iterate_of_commute`, `lambda_route_stable` in `Lutar/Lambda/AggregatorLfp.lean` — [VERIFIED], merged on `main` at squash commit `357cdaa7…` (PR #226), `lake`-green, axioms ⊆ {propext, Classical.choice, Quot.sound}.*

*Result III (Wave26): `lfp_eq_iSup_iterate` (unconditional, derives commute from ω-Scott-continuity) in `Lutar/Lambda/AggregatorLfp.lean` — [VERIFIED], PR #227, commit `6feeee59…`, additive over Wave25, `lake`-green, axioms ⊆ {propext, Classical.choice, Quot.sound}.*

*Jack Kruse: [NARRATIVE] only. No theorem or claim in this document depends on any assertion associated with Kruse.*

*SLSA: L1+L2 attested. L3, FedRAMP, CMMC, ATO: roadmap, not current status. Trust is never asserted at 100%.*

*SZL Holdings · Stephen P. Lutar Jr. · ORCID 0009-0001-0110-4173 · Version v8 (canonical) — 2026-06-11*
