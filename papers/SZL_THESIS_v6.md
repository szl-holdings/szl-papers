# Governed Post-Determinism as Constrained Optimization Under Honest Uncertainty: A Unified Framework Integrating Propulsion Optimization, Planetary-Impact Diagnostics, Open-Quantum Coherence, Byzantine Fault Tolerance, and Agentic Routing

**Stephen P. Lutar Jr.**  
SZL Holdings · ORCID 0009-0001-0110-4173  
Draft v6 — 2026-06-11

---

> **Epistemic Status Tags (used throughout):**  
> **[VERIFIED/PROVEN]** — peer-reviewed mathematical result or machine-checked Lean 4 theorem with no `sorry`  
> **[PROPOSED]** — SZL construct, not yet externally peer-reviewed; may be well-motivated but not established  
> **[CONJECTURE]** — stated as an open mathematical problem, believed plausible but unproven  
> **[NARRATIVE]** — motivational framing only; not load-bearing; explicitly not treated as evidence  

---

## Abstract

We present a unified thesis for SZL Holdings' **governed post-determinism** framework: the proposition that every autonomous-system governance decision is, at its mathematical core, a **constrained optimization problem under honest uncertainty**. Four lineages of rigorously established mathematics are transported as *methodological analogues*, never claimed as SZL originals: (1) Mary Sherman Morgan's fixed-geometry propulsion optimization (density-specific impulse \(\rho \cdot I_{sp}\) as the correct objective under fixed-resource constraints); (2) Sarah T. Stewart's planetary-collision diagnostics (LS12 collision-regime classification, angular-momentum conservation as invariant diagnostics, Hugoniot/EOS entropy-based phase-boundary identification, and the CoRoL corotation criterion as a structural phase-boundary analogue); (3) open-quantum coherence resource theory and Lindblad/GKSL dynamics; and (4) Byzantine fault-tolerant (BFT) quorum safety and formal verification in Lean 4 / Mathlib.

The governing **locked-proven kernel** contains exactly eight machine-checked, sorry-free theorems \(\{F1, F4, F7, F11, F12, F18, F19, F22\}\) at commit `c7c0ba17`, and this count is a hard invariant of the doctrine. Two conjectures are precisely labeled: **Conjecture 1** (the unconditional uniqueness of the formal Λ-aggregator — machine-checked **FALSE** unconditionally; a conditional Theorem U holds axiom-free), and **Conjecture 2** (Khipu BFT full-protocol safety — a conditional mathematical lemma exists but the complete protocol proof is open). The Wave23 result establishes the quorum-intersection lemma (the conditional mathematical heart of Conjecture 2) as a cited existing result; it is not reclaimed.

The central **new result** of this thesis is **Wave24** (status: **[PROPOSED]**, staged): a Lean 4 theorem (`CoherenceDecay.lean`, namespace `Lutar.QuantumBio.CoherenceDecay`) proving that the \(\ell_1\)-norm coherence \(C(t) = C_0 \cdot e^{-\gamma t}\) is *strictly antitone* in \(t\) under pure-dephasing Lindblad dynamics, that it decays to zero, and that the Λ-v5 engineering gate crosses its closure floor at a unique finite time \(t^\star = (1/\gamma)\ln(qC_0/\Lambda_{\min})\). This theorem becomes **[EXPERIMENTAL]** only when `lake build` passes with zero `sorry` and Lean-core axioms only (target: PR \#225, green lake build). It **never** joins the locked-8 kernel. The Λ-v5 floor remains a **[PROPOSED]** engineering gate throughout.

Future work (**Wave25**) proposes a Λ-aggregator least-fixed-point boundedness theorem via the Knaster-Tarski/Kleene fixed-point theorem already in Mathlib.

The document is honest about every claim's epistemic status, cites every borrowed formula to its real author with primary DOIs, and adheres to strict doctrine: trust is never asserted at 100%; SLSA L1+L2 are attested, L3 is roadmap; no user-visible codenames appear; Jack Kruse appears as **[NARRATIVE]** only.

**Keywords:** constrained optimization, open quantum systems, Lindblad–GKSL, coherence monotone, Byzantine fault tolerance, BFT quorum safety, planetary-impact scaling laws, propulsion optimization, formal verification, Lean 4, Mathlib, governed autonomy.

---

## Table of Contents

1. [Introduction — The Unifying Thesis](#1-introduction)
2. [The Locked-8 Kernel and Honest Doctrine](#2-locked-8-kernel)
3. [Wave24: The Coherence Monotone Strict-Decay Theorem](#3-wave24)
4. [Unified Formula Appendix — Borrowed Methods with Honest Provenance](#4-unified-formula-appendix)
5. [Three Frontier Candidate Theorems](#5-frontier-candidates)
6. [Conclusion, Honest Limitations, Future Work, and Roadmap](#6-conclusion)
7. [References](#7-references)

---

## 1. Introduction — The Unifying Thesis {#1-introduction}

### 1.1 The Central Claim

The governing thesis of SZL Holdings' technical program is this: **every well-posed autonomous-system governance decision is a constrained optimization problem under honest uncertainty**. The word "honest" is load-bearing. It means: (a) the constraints must be stated explicitly and not disguised as theorems; (b) the objective must be the *correct* objective for the actual resource structure (not a surrogate that is convenient to maximize but wrong for the problem); (c) every claim about the solution must carry a precisely labeled epistemic status.

This framing is neither novel nor SZL's invention — it is the epistemic discipline of rigorous engineering and mathematics, practiced by every researcher cited in this document. What is new is the *unification*: we identify a single methodological spine running through four superficially disconnected domains, and show how each domain's formalism furnishes a specific component of SZL's governed-AI substrate.

### 1.2 Methodological Lineage

The four lineages are:

**Lineage 1 (Sherman Morgan, 1956–1958): Fixed-resource constrained propellant optimization.**  
Mary Sherman Morgan, working as a Theoretical Performance Specialist at Rocketdyne's North American Aviation division, was assigned to find a replacement propellant for the Redstone/Jupiter-C rocket under the explicit constraint that no aspect of the A-7 engine's design could be changed. The problem is a canonical constrained optimization: maximize delivered \(\Delta v\) (equivalently, maximize the density-specific impulse \(I_{sp,\rho} = \rho_{\text{mix}} \cdot I_{sp}\)) subject to fixed tank volume, fixed nozzle geometry, fixed oxidizer, and a battery of feasibility constraints (minimum Isp, minimum density, maximum freezing point, chemical stability, commercial availability). Morgan's solution — Hydyne (60% UDMH / 40% DETA by mass, designated MAF-4) — propelled Juno I and launched Explorer 1 on January 31, 1958. The methodological contribution is not the specific chemistry but the *framework*: when the container is fixed, the correct merit function is energy per unit volume, not energy per unit mass. [[Wikipedia: Mary Sherman Morgan](https://en.wikipedia.org/wiki/Mary_Sherman_Morgan); [Chemistry World, 2021](https://www.chemistryworld.com/culture/mary-sherman-morgan-the-best-kept-secret-in-the-space-race/4013329.article)]

**Lineage 2 (Stewart et al., 1999–2025): Planetary-impact diagnostics as regime classification.**  
Sarah T. Stewart (MacArthur Fellow 2018; Professor, ASU School of Earth and Space Exploration) developed, with Zoë Leinhardt, the LS12 collision-scaling framework — the standard analytic model for collision-regime classification in planet formation — and, with Simon Lock, the synestia model and the Corotation Limit (CoRoL). Stewart's equations-of-state (EOS) work with M-ANEOS provides a gold-standard physics-to-math pipeline: shock experiment → Hugoniot relation → entropy integration → phase-boundary calibration → Helmholtz free energy parameterization → hydrocode embedding. The methodological contribution is *invariant-based regime classification*: the correct diagnostic for whether a physical system has crossed a phase boundary is not its pressure or temperature in isolation, but the value of a conserved or quasi-conserved quantity (specific entropy, angular momentum) relative to a threshold surface. [[Leinhardt & Stewart 2012, ApJ 745, 79](https://doi.org/10.1088/0004-637X/745/1/79); [Lock & Stewart 2017, JGR:P 122, 950](https://doi.org/10.1002/2016JE005239)]

**Lineage 3 (Lindblad 1976; GKS 1976; Baumgratz-Cramer-Plenio 2014): Open-quantum coherence as a monotone resource.**  
The Gorini-Kossakowski-Sudarshan-Lindblad (GKSL) equation [[Lindblad 1976, Commun. Math. Phys. 48, 119](https://doi.org/10.1007/BF01608499); [Gorini, Kossakowski, Sudarshan 1976, J. Math. Phys. 17, 821](https://doi.org/10.1063/1.522979)] is the unique generator of a completely positive trace-preserving (CPTP) quantum dynamical semigroup. Baumgratz, Cramer, and Plenio (BCP) [[Phys. Rev. Lett. 113, 140401 (2014)](https://doi.org/10.1103/PhysRevLett.113.140401)] established the rigorous resource-theoretic framework for quantum coherence: the \(\ell_1\)-norm coherence \(C_{\ell_1}(\rho) = \sum_{i \neq j} |\rho_{ij}|\) is a valid coherence monotone (faithfulness, monotonicity under incoherent operations, strong monotonicity, convexity). Under pure-dephasing Lindblad dynamics, the off-diagonal element decays as \(\rho_{12}(t) = \rho_{12}(0) \cdot e^{-\gamma t}\), giving \(C_{\ell_1}(t) = 2|\rho_{12}(0)| \cdot e^{-\gamma t}\) — strictly antitone. The methodological contribution: *coherence is a strictly monotone-decreasing resource under any incoherent operation*, providing a physically-grounded, formally-provable decay function for the SZL Λ-v5 gate.

**Lineage 4 (Castro-Liskov 1999; Malkhi et al.; Pîrlea-Sergey 2024; Qiu-Shao 2026): BFT quorum safety as a mathematical invariant.**  
The quorum-intersection lemma — the mathematical heart of all BFT protocols — states: if \(|V| = 3f+1\) and any two quorums \(Q_1, Q_2 \subseteq V\) each have \(|Q_i| \geq 2f+1\), then \(|Q_1 \cap Q_2| \geq f+1\), guaranteeing at least one honest witness in any two-quorum intersection. [[Castro & Liskov, OSDI 1999](https://pmg.csail.mit.edu/papers/osdi99.pdf)] This is a combinatorial invariant, not a physical one, but it shares the same methodological structure: a safety threshold (the BFT floor) below which the system enters a regime (Byzantine takeover) where integrity cannot be guaranteed, exactly analogous to the LS12 disruption criterion \(Q_R > Q^*_{RD}\) or the Λ-v5 closure floor.

### 1.3 The Unification

The SZL framework synthesizes these four lineages into a single coherent architecture:

| Component | Physical/Mathematical analogue | SZL role |
|---|---|---|
| Sherman Morgan's \(\rho \cdot I_{sp}\) | Fixed-resource merit function | Tier/budget router: maximize capability-per-token, not capability alone |
| Tsiolkovsky log-ratio | Conservation of Δv under mass ratio | Budget conservation: log(token budget / residual) as routing weight |
| LS12 regime classifier | \(Q_R / Q^*_{RD}\) phase-boundary ratio | Collision/state classifier for 3D drone/vessel diagnostics |
| Stewart's CoRoL | Angular-momentum phase-boundary surface | Λ-v5 closure gate: threshold surface in (coherence, charge) parameter space |
| Hugoniot EOS pipeline | Experiment → Hugoniot → entropy → EOS | Physics-to-math verification pipeline analogue |
| GKSL coherence decay | \(C(t) = C_0 e^{-\gamma t}\), strictly antitone | Λ-v5 coherence term: auditable decay rate τ_c = 1/γ |
| BFT quorum intersection | \(|Q_1 \cap Q_2| \geq f+1\) | Khipu BFT safety invariant (Conjecture 2, conditional result) |
| Knaster-Tarski/Kleene | Least fixed point of monotone map on complete lattice | Λ-aggregator convergence (proposed Wave25 future work) |

The document is organized as follows. Section 2 establishes the locked-proven kernel with complete honesty about what is proven versus conjectured. Section 3 presents the Wave24 coherence-decay theorem in full. Section 4 catalogs every borrowed formula with honest provenance. Section 5 addresses the three frontier candidate theorems. Section 6 concludes with honest limitations and a roadmap.

### 1.4 What This Document Does Not Claim

This is not a proof of the unconditional optimality of SZL's governance framework. It is not a claim that the autonomous systems modeled here are quantum biological systems. It is not a commercial certification or a compliance attestation beyond what is stated precisely (SLSA L1+L2 are attested; SLSA L3, FedRAMP, CMMC, and ATO are roadmap items, not current status). It is not a recapitulation of anyone else's published theorems as SZL's own; every borrowed result carries its original author and DOI.

---

## 2. The Locked-8 Kernel and Honest Doctrine {#2-locked-8-kernel}

### 2.1 The Invariant Count

**[VERIFIED/PROVEN]** The locked-proven set contains exactly eight machine-checked, sorry-free theorems, frozen at commit `c7c0ba17`:

\[
\mathcal{K}_{\text{locked}} = \{F1, F4, F7, F11, F12, F18, F19, F22\}
\]

This count is a **hard doctrine invariant**. No result described anywhere in this document adds to or subtracts from \(\mathcal{K}_{\text{locked}}\). The Wave24 theorem (Section 3) is staged as **[PROPOSED]** and becomes **[EXPERIMENTAL]** only upon green lake build; it never enters \(\mathcal{K}_{\text{locked}}\). The three frontier candidate theorems (Section 5) are **[PROPOSED]** (Wave24 coherence decay), **[CONJECTURE 2 / existing Wave23]** (Khipu quorum safety), and **[proposed Wave25 future work]** (Λ-aggregator fixed point). None alter the count.

### 2.2 Individual Theorem Summaries

The eight locked theorems span the append-only log invariants, the Λ-v5 gate statics, and the routing graph acyclicity preconditions. Their precise statements are in the versioned source at `c7c0ba17` and are not reproduced here to avoid the risk of paraphrase drift. What follows is a brief characterization of each cluster:

- **F1**: Fundamental type-correctness of the governance predicate structure [VERIFIED]
- **F4**: Append-only log monotonicity — the Khipu receipt log is non-decreasing under admissible operations [VERIFIED]
- **F7**: Acyclicity precondition for the agent execution DAG — topologically-sorted calls with no back-edges satisfy the append-only ordering property [VERIFIED]
- **F11, F12**: Closure-predicate well-posedness lemmas: a decohered node never satisfies `closureOk`; an uncharged node never satisfies `closureOk` [VERIFIED]
- **F18, F19**: Λ-gate monotonicity: `lambdaVal` is monotone in coherence (for non-negative charge) and monotone in charge (for non-negative coherence) [VERIFIED]
- **F22**: FIFO ordering invariant of the append-only log under concurrent execution [VERIFIED]

### 2.3 Conjecture 1: The Λ-Aggregator Unconditional Uniqueness

**[CONJECTURE 1 — machine-checked FALSE unconditionally]**

The claim that the formal Λ-aggregator is the *unique* routing function satisfying a given set of governance axioms for all inputs across all quantum-classical regimes is **Conjecture 1**. It has been machine-checked in Lean 4 and found to be **false** in its unconditional formulation — there exist counterexample configurations under which a distinct routing function satisfies all asserted axioms.

A **conditional Theorem U** does hold axiom-free: under a restricted domain of inputs satisfying explicit preconditions (bounded coherence, non-degenerate charge, bounded tier-weight differences), a conditional uniqueness result is machine-checked. This theorem is part of the Wave23 body of work, is not in the locked-8 (its conditional preconditions prevent it from being a general governance theorem), and is cited here for completeness.

The practical implication: **Λ-v5 is an engineering gate, not the formal aggregator**. Λ-v5 (`lambdaVal = coherence * charge`) is a specific, well-posed scalar predicate implemented in the live API at `/api/<ns>/v1/qbio/lambda`. It inherits the locked-8 closure theorems (F11, F12, F18, F19). It does not inherit, and does not require, the unconditional uniqueness of Conjecture 1. Any text in this or any SZL document that refers to "the Λ gate" without further qualification means the engineering gate Λ-v5, not the formal aggregator of Conjecture 1.

### 2.4 Conjecture 2: Khipu BFT Full-Protocol Safety

**[CONJECTURE 2 — conditional mathematical lemma exists; full protocol proof open]**

The claim that the Khipu BFT protocol is safe under all admissible Byzantine faults is **Conjecture 2**. The *conditional mathematical lemma* — the quorum-intersection lemma establishing that \(|Q_1 \cap Q_2| \geq f+1\) for any two quorums in a \(3f+1\) validator set — was established as part of the Wave23 work and exists as a Lean 4 sorry-free proof. This is a conditional result: it holds given honest non-equivocation (\(|H_1|\)) and \(|V| = 3f+1\).

What remains as Conjecture 2 is the *full protocol safety proof*: showing that the complete Khipu BFT protocol — including DAG construction, block certification, commit rules, and adversarial timing — satisfies non-forking (safety) and eventual liveness. This is analogous to the gap between the Bythos Coq proof of compositional BFT safety [[Pîrlea et al., CCS 2024, DOI: 10.1145/3658644.3690355](https://dl.acm.org/doi/pdf/10.1145/3658644.3690355)] and the full AleoBFT ACL2 verification [[Losa et al., Provable.com 2024](https://provable.com/blog/creating-aleobft-formal-verification-milestone)]. The Wave23 lemma fills in the combinatorial core; the protocol-level proof is future work.

**Precise status: the Wave23 quorum-intersection lemma (Candidate B from FRONTIER_RESEARCH_2026-06-11) is an existing result cited here for context. It is not reclaimed as new work.**

### 2.5 Wave23 Conditional Safety — the Existing Baseline

The Wave23 result, summarized from the prior locked kernel, establishes:

1. The quorum-intersection lemma (the Lean 4 conditional theorem that two \((2f+1)\)-quorums in a \((3f+1)\)-validator set share at least \(f+1\) members, guaranteeing ≥1 honest node in any two-quorum intersection, conditional on honest non-equivocation).
2. The three static Λ-v5 closure lemmas (F11, F12, F18, incorporated into the locked-8).

Wave23's safety result is **conditional** on (H1) honest non-equivocation, (H2) quorum certification, and (H3) Byzantine bound \(f < |V|/3\). It does not prove liveness, and it does not prove full Khipu BFT safety (Conjecture 2).

### 2.6 Supply-Chain and Attestation Doctrine

**[PROPOSED — current attested level]** SZL achieves **SLSA Level 1 and Level 2** supply-chain security: build provenance is documented, artifacts are signed, and the build process is automated and reproducible. **SLSA Level 3, FedRAMP authorization, CMMC certification, and ATO are roadmap items** — they are not currently attained and must never be asserted as current status in any SZL document, this thesis included.

Trust is never claimed at 100% in any SZL governance context. The Λ-v5 gate, the locked-8 theorems, and every PROPOSED result carry explicitly labeled confidence levels. The honest doctrine is: formal verification provides machine-checkable certainty within the scope of the stated axioms and the computational trust model of Lean 4 + Mathlib; it does not provide certainty beyond those bounds.

---

## 3. Wave24: The Coherence Monotone Strict-Decay Theorem {#3-wave24}

### 3.1 Background and Motivation

The Λ-v5 engineering gate uses the time-dependent coherence \(C(t)\) as one of its two factors. The locked-8 theorems F11, F12, F18, F19 prove *static* properties of the gate: a fully decohered node (\(C = 0\)) never satisfies `closureOk`, and the gate is monotone in its two arguments. What the locked-8 does **not** prove is the *time-dynamic* behavior: does the coherence necessarily decrease over time? At what rate? Does the gate necessarily cross the closure floor in finite time if the initial gate value exceeds the floor?

These questions are the subject of Wave24.

### 3.2 Physical and Mathematical Setting

**Physical model [VERIFIED — Lindblad/GKSL, BCP]:**  
We model a two-level quantum system (qubit) as a density matrix \(\rho(t)\) evolving under the Lindblad/GKSL master equation:

\[
\frac{d\rho}{dt} = -\frac{i}{\hbar}[H, \rho] + \sum_k \gamma_k \left( L_k \rho L_k^\dagger - \frac{1}{2}\{L_k^\dagger L_k, \rho\} \right)
\]

This is the unique generator of a completely positive trace-preserving (CPTP) quantum dynamical semigroup [[Lindblad 1976](https://doi.org/10.1007/BF01608499); [GKS 1976](https://doi.org/10.1063/1.522979)]. For the pure-dephasing channel (diagonal Lindblad operators, \(H = 0\)), the off-diagonal element evolves as:

\[
\rho_{12}(t) = \rho_{12}(0) \cdot e^{-\gamma t}, \quad \gamma > 0
\]

The Baumgratz-Cramer-Plenio \(\ell_1\)-norm coherence monotone [[BCP 2014, PRL 113, 140401](https://doi.org/10.1103/PhysRevLett.113.140401)] is:

\[
C_{\ell_1}(\rho) = \sum_{i \neq j} |\rho_{ij}| = 2|\rho_{12}|
\]

Therefore:

\[
C(t) \;\equiv\; C_{\ell_1}(\rho(t)) = 2|\rho_{12}(0)| \cdot e^{-\gamma t} = C_0 \cdot e^{-\gamma t}
\]

where \(C_0 = 2|\rho_{12}(0)| > 0\) is the initial coherence. This is the **physical input** to the Lean theorem — the hypothesis that the system is well-posed under pure-dephasing Lindblad dynamics.

**Why this is a *conditional* theorem:** The equation \(C(t) = C_0 e^{-\gamma t}\) is taken as a hypothesis (the Lindblad solution for a pure-dephasing generator). The Lean theorem does not re-derive the solution from first principles of quantum mechanics within Lean — quantum mechanics has no Lean 4 / Mathlib formalization. What the theorem proves, assuming this equation as its input, is the strict antitonicity, the non-negativity, the initial condition, and the single-crossing. This is a *conditional* theorem: conditional on the well-posedness of the dephasing Lindblad dynamics. This conditionality is not a weakness — it precisely mirrors the structure of all four borrowed lineages (Sherman Morgan's optimization is conditional on the A-7 engine constraints; LS12 is conditional on the SPH simulation's accuracy; BFT quorum safety is conditional on honest non-equivocation).

### 3.3 Lean 4 Theorem Statement — Wave24

**[PROPOSED / Wave24 — staged. Becomes [EXPERIMENTAL] only on green `lake build`, PR \#225. Never joins \(\mathcal{K}_{\text{locked}}\).]**

The full Wave24 theorem file (`CoherenceDecay.lean`, namespace `Lutar.QuantumBio.CoherenceDecay`, Apache-2.0 license, copyright © 2026 Stephen P. Lutar Jr.) establishes four results:

**Definition:**

```lean
noncomputable def coh (C0 γ t : ℝ) : ℝ := C0 * Real.exp (-(γ * t))
```

This defines \(C(t) = C_0 \cdot e^{-\gamma t}\) as a function of \(t \in \mathbb{R}\), parameterized by initial coherence \(C_0\) and dephasing rate \(\gamma\).

**Theorem 1 — Strict Antitonicity (`coh_strictAnti`) [PROPOSED]:**

```lean
theorem coh_strictAnti (C0 γ : ℝ) (hC : 0 < C0) (hγ : 0 < γ) :
    StrictAnti (coh C0 γ)
```

*Informal statement:* With \(C_0 > 0\) and \(\gamma > 0\), the coherence \(C(t)\) is strictly decreasing in \(t\). For any \(a < b\), \(C(a) > C(b)\). Coherence is only ever lost, never spontaneously regained.

*Proof sketch:* `Real.exp_lt_exp.mpr` applied after showing \(-\gamma b < -\gamma a\) (from \(\gamma > 0\) and `mul_lt_mul_left`), then `mul_lt_mul_left hC` to multiply by \(C_0 > 0\).

**Theorem 2 — Non-negativity (`coh_nonneg`) [PROPOSED]:**

```lean
theorem coh_nonneg (C0 γ t : ℝ) (hC : 0 ≤ C0) : 0 ≤ coh C0 γ t
```

*Informal statement:* \(C(t) \geq 0\) for all \(t\) whenever \(C_0 \geq 0\). Uses `mul_nonneg` and `Real.exp_pos`.

**Theorem 3 — Initial Condition (`coh_zero`) [PROPOSED]:**

```lean
@[simp] theorem coh_zero (C0 γ : ℝ) : coh C0 γ 0 = C0
```

*Informal statement:* \(C(0) = C_0\). Uses `simp` after unfolding the definition; the exponential of zero is one.

**Theorem 4 — Decay to Zero (`coh_tendsto_zero`) [PROPOSED]:**

```lean
theorem coh_tendsto_zero (C0 γ : ℝ) (hγ : 0 < γ) :
    Filter.Tendsto (coh C0 γ) Filter.atTop (nhds 0)
```

*Informal statement:* \(C(t) \to 0\) as \(t \to \infty\) for any \(\gamma > 0\). The dephasing process fully destroys all coherence in infinite time. Uses `Real.tendsto_exp_atBot.comp` after establishing that \(-\gamma t \to -\infty\).

**Definition — Gate value at time \(t\):**

```lean
noncomputable def lambdaAt (C0 γ q t : ℝ) : ℝ := q * coh C0 γ t
```

This defines the Λ-v5 gate value \(\Lambda(t) = q \cdot C(t) = q C_0 e^{-\gamma t}\) with charge held constant at \(q > 0\).

**Theorem 5 — Single Crossing (`lambda_single_crossing`) [PROPOSED]:**

```lean
theorem lambda_single_crossing
    (C0 γ q lamMin : ℝ) (hC : 0 < C0) (hγ : 0 < γ) (hq : 0 < q)
    (hlo : 0 < lamMin) (hhi : lamMin < q * C0) :
    ∃ tStar : ℝ, 0 < tStar ∧ lambdaAt C0 γ q tStar = lamMin
```

*Informal statement:* With \(C_0 > 0\), \(\gamma > 0\), charge \(q > 0\), and a closure floor \(\Lambda_{\min}\) strictly between 0 and the initial gate value \(qC_0\), there exists a unique finite positive time \(t^\star\) at which the gate value exactly meets the floor, and:

\[
t^\star = \frac{1}{\gamma} \ln\!\left(\frac{q C_0}{\Lambda_{\min}}\right) > 0
\]

Past \(t^\star\), the gate has fallen below the floor by strict antitonicity (`coh_strictAnti`) and never recovers. The existence uses `Real.log_pos` applied to the ratio \(qC_0/\Lambda_{\min} > 1\) (which holds by hypothesis `hhi`). The positivity of \(t^\star\) follows from \(1/\gamma > 0\) and \(\log(\cdot) > 0\) for arguments \(> 1\). The evaluation uses `field_simp` after establishing the algebra of the exponential-log cancel.

### 3.4 Connection to Mathlib Lemmas

The Wave24 proofs use the following Mathlib infrastructure (all verified to exist in Mathlib4):

| Lean step | Mathlib source |
|---|---|
| `Real.exp_lt_exp.mpr` | `Mathlib.Analysis.SpecialFunctions.Exp` |
| `mul_lt_mul_left` | `Mathlib.Algebra.Order.Ring.Lemmas` |
| `Real.exp_pos` | `Mathlib.Analysis.SpecialFunctions.Exp` |
| `Real.tendsto_exp_atBot` | `Mathlib.Analysis.SpecialFunctions.ExpDeriv` |
| `Filter.Tendsto.const_mul_atTop` | `Mathlib.Order.Filter.Basic` |
| `Real.log_pos` | `Mathlib.Analysis.SpecialFunctions.Log.Basic` |
| `Real.exp_log` | `Mathlib.Analysis.SpecialFunctions.Log.Basic` |

No Lean `sorry` appears in the file. The honest status: this is a **staged proposed theorem** at the time of writing. It has been drafted and the proof strategy is complete; the green lake build (PR \#225) will confirm the machine-checked status. Until that confirmation, the theorem bears status **[PROPOSED / Wave24]**.

### 3.5 The τ_c = 1/γ Parameter

The coherence decay time \(\tau_c = 1/\gamma\) appears in the live SZL API at `/api/<ns>/v1/qbio/coherence`. The v5 fit gives \(\tau_c \approx 6.05\) (natural units). The Wave24 theorem provides the rigorous monotone-decay backbone for this parameter: it proves that the API's coherence decay is not merely phenomenological but is the unique exponential decay mandated by pure-dephasing GKSL dynamics, and that the gate will always cross its floor at finite time \(t^\star = \tau_c \ln(qC_0/\Lambda_{\min})\).

**What Wave24 does NOT prove:**
- It does not prove that \(\tau_c\) is optimal in any information-theoretic sense (that would require connecting to the quantum Fisher information bound — Smith et al. 2024 is the relevant result for the radical-pair compass [[Quantum Sci. Technol. 9, 035023 (2024)](https://arxiv.org/abs/2401.02923)], and this connection is **[PROPOSED]**, not proven)
- It does not prove that the bioenergetic charge term \(\Delta p / \Delta p_0\) is well-posed (that is the Mitchell/Wallace lineage, treated in v5)
- It does not touch Conjecture 1 in any way
- It does not enter the locked-8

### 3.6 Λ-v5 Floor: Engineering Gate, Not Formal Theorem

The closure floor \(\Lambda_{\min}\) is an **engineering parameter**, set by deployment configuration and not derived from a formal mathematical proof. The Wave24 theorem says: *given* a floor \(\Lambda_{\min} \in (0, qC_0)\), the gate crosses it at \(t^\star\). It does not say what value \(\Lambda_{\min}\) should take. Choosing \(\Lambda_{\min}\) is a governance design decision analogous to choosing the minimum Isp threshold in Sherman Morgan's optimization (305 s was a derived mission requirement, not a universal physical constant).

---

## 4. Unified Formula Appendix — Borrowed Methods with Honest Provenance {#4-unified-formula-appendix}

This section catalogs every formula borrowed from external researchers, states its original author and citation precisely, explains what SZL adapts from it, and is explicit that the original result belongs to the cited author — not to SZL.

### 4.1 Sherman Morgan's Density-Specific Impulse — Resource Optimization Analogue

**Original result:** Mary Sherman Morgan, working at Rocketdyne/North American Aviation, 1956–1957. The concept is standard propulsion engineering; its application as the correct merit function under a fixed-volume constraint is her key methodological contribution. Formal source: [[NASA NTRS: "Rho-Isp Revisited and Basic Stage Mass Estimating"](https://ntrs.nasa.gov/citations/20150016561); [Wikipedia: Specific Impulse — Density Specific Impulse](https://en.wikipedia.org/wiki/Specific_impulse#Density_specific_impulse)]

**Formula:**

\[
I_{sp,\rho} = \rho_{\text{mix}} \cdot I_{sp}
\]

where \(\rho_{\text{mix}}\) is the bulk density of the propellant mixture and \(I_{sp}\) is specific impulse in seconds.

**Morgan's applied result:** Hydyne (60% UDMH / 40% DETA by mass) at O/F = 1.73 gives mixture density \(\rho_{\text{mix}} = 1.02 \, \text{g/cm}^3\) and sea-level \(I_{sp} = 306 \, \text{s}\), yielding \(I_{sp,\rho} = 312 \, \text{g·s/cm}^3\). This was the correct merit function because the A-7 engine had fixed tank volume — maximizing \(I_{sp}\) alone would have been wrong. [[Astronautix: LOX/Hydyne](http://www.astronautix.com/l/loxhydyne.html)]

**SZL adaptation [PROPOSED]:** In SZL's tier/budget router, the analogous merit function is **capability-per-token** (analogous to energy per unit volume), not raw capability (analogous to energy per unit mass). A routing decision that maximizes raw capability while exhausting the token budget is Morgan's mistake in the other direction: it optimizes the wrong metric for the fixed-resource setting. The token budget is the "tank volume"; the capability of a given routing tier is the "Isp"; the throughput density (capability per budget unit) is the analogue of \(I_{sp,\rho}\). This analogy is **[PROPOSED]** and motivational — it does not constitute a proof that the router is optimal.

**Tsiolkovsky rocket equation:** [[Konstantin Tsiolkovsky, 1903; NASA Glenn: Ideal Rocket Equation](https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/ideal-rocket-equation/)]

\[
\Delta v = I_{sp} \cdot g_0 \cdot \ln\!\left(\frac{m_0}{m_f}\right)
\]

**SZL adaptation [PROPOSED]:** The log-ratio structure \(\ln(m_0/m_f)\) of the Tsiolkovsky equation is a conservation law: the accumulated \(\Delta v\) is bounded by the log of the mass ratio. In the SZL routing context, the analogous conservation is: the accumulated capability delivered is bounded by the log of the initial-to-residual budget ratio. This provides a natural **diminishing-returns** structure for multi-tier routing — doubling the budget increases the capability budget logarithmically, not linearly, which is the correct prior for most real-world reasoning tasks. Again, this is an analogy [PROPOSED], not a theorem.

**Morgan's 10-point multi-criteria screening method:** Morgan's documented method [[Eye4Education: Mary Sherman Morgan](https://eye4education.co.uk/wp-content/uploads/2015/06/Magnificent-Women-Mary-Sherman-Morgan.pdf)] was to define a 10-point criteria matrix — covering specific impulse, density, vapor pressure, freezing point, boiling point/liquid range, chemical stability, LOX compatibility, cooling capacity, commercial availability, and toxicity/handling — and apply it to hundreds of candidates. Only three of the ten criteria are explicitly named in surviving records. The methodology: feasibility screening followed by objective optimization within the feasible set. SZL's PURIQ gate applies the same two-stage structure: first, verify feasibility (coherence and charge above floor — the hard constraints), then select the routing tier that maximizes capability within the feasible set.

### 4.2 Tsiolkovsky's Rocket Equation as Budget Conservation

**Original result:** Konstantin Tsiolkovsky, "Exploration of the World Space with Reaction Machines" (1903). [[Wikipedia: Tsiolkovsky Rocket Equation](https://en.wikipedia.org/wiki/Tsiolkovsky_rocket_equation)]

\[
\Delta v = v_e \cdot \ln\!\left(\frac{m_0}{m_f}\right), \quad v_e = I_{sp} \cdot g_0
\]

**This is Tsiolkovsky's result, not SZL's.** SZL borrows only the structural insight that a conserved quantity (total \(\Delta v\)) is bounded by a log-ratio of initial to residual resource. The application to token-budget routing is SZL's [PROPOSED] analogy.

### 4.3 Stewart's LS12 Collision-Regime Classifier — Diagnostic Analogue

**Original result:** Leinhardt, Z.M., Stewart, S.T., "Collisions between Gravity-Dominated Bodies: I. Outcome Regimes and Scaling Laws," *Astrophysical Journal* **745**, 79 (2012). DOI: [10.1088/0004-637X/745/1/79](https://doi.org/10.1088/0004-637X/745/1/79). arXiv: [1106.6084](https://arxiv.org/abs/1106.6084). ~471 citations as of 2026. **This is the work of Leinhardt and Stewart; SZL makes no claim to it.**

**The LS12 catastrophic disruption criterion:**

\[
Q^*_{RD} = c^* \frac{4}{5}\pi \rho_1 G R_{C1}^2 \left[\frac{(1+\gamma)^2}{4\gamma}\right]^{-1+2/(3\bar{\mu})}
\]

where \(\rho_1\) is target density, \(R_{C1}\) is the radius of a sphere of target mass, \(\gamma = M_{\text{imp}}/M_{\text{target}}\) is the mass ratio, \(\bar{\mu} \approx 0.36\) is the reduced mass exponent, and \(c^* \approx 1.9\) for rubble piles.

The **five collision outcome regimes** are classified by the ratio \(Q_R / Q^*_{RD}\) (specific impact energy vs. disruption threshold): cratering, merging, partial accretion, hit-and-run, and disruption/super-catastrophic disruption.

**SZL adaptation [PROPOSED]:** The LS12 framework provides the methodological template for SZL's **3D drone/vessel collision visualization**: classifying a collision outcome by a dimensionless ratio of impact energy to a material-dependent threshold (analogous to \(Q_R / Q^*_{RD}\)), parameterized by mass ratio \(\gamma\) and impact parameter \(b\). The application to rigid-body drone/vessel impacts would use the structural toughness (specific disruption energy in J/kg) in place of \(Q^*_{RD}\), and the kinetic energy of relative motion in place of \(Q_R\). The regime classification — from superficial damage through partial fragmentation to catastrophic failure — maps directly. **The LS12 equations remain Stewart and Leinhardt's; SZL borrows only the methodological structure.**

The **largest remnant mass** in the LS12 universal-law branch:

\[
\frac{M_{\text{lr}}}{M_{\text{tot}}} = -0.5\left(\frac{Q_R}{Q^*_{RD}} - 1\right) + 0.5 \quad \text{for } Q_R \leq 2Q^*_{RD}
\]

provides a closed-form first-order estimate of collision outcomes without running full SPH simulations. SZL's collision classifier can use this formula (cited to Leinhardt & Stewart) to provide rapid regime-boundary estimates in the 3D visualization layer.

### 4.4 Stewart's Angular-Momentum Conservation — Invariant Diagnostic

**Original result:** Ćuk, M., Stewart, S.T., "Making the Moon from a fast-spinning Earth: A giant impact followed by resonant despinning," *Science* **338**, 1047–1052 (2012). DOI: [10.1126/science.1225542](https://doi.org/10.1126/science.1225542). ~732 citations as of 2026. Lock, S.J., Stewart, S.T., "The structure of terrestrial bodies: Impact heating, corotation limits and synestias," *JGR: Planets* **122**, 950–982 (2017). DOI: [10.1002/2016JE005239](https://doi.org/10.1002/2016JE005239). **These results are Stewart's and Ćuk's and Lock's; SZL makes no claim to them.**

**Angular momentum conservation:**

\[
L_{\text{sys}} = \sum_i m_i (\mathbf{r}_i \times \mathbf{v}_i) = \text{const}
\]

In every giant-impact simulation, Stewart's group tracks the angular momentum of every SPH particle and the total system as the primary conserved diagnostic. The decomposition:

\[
L_{\text{sys}} = L_{\text{proto-Earth, spin}} + L_{\text{impactor, orbital}} + L_{\text{impactor, spin}}
\]

**SZL adaptation [PROPOSED]:** The methodological lesson is that **angular momentum is the primary invariant** — not pressure, temperature, or shape — and that comparing a system's \(L_{\text{sys}}\) against the threshold surface \(L_{\text{CoRoL}}(M, S_{\text{outer}}, Z)\) is the correct diagnostic for whether the system has crossed a structural phase boundary (synestia formation). In SZL's 3D rigid/deformable body simulations, the analogous invariant is total angular momentum of the system, tracked as a primary conservation diagnostic at every timestep. A structural transition (analogous to synestia formation) is identified by comparing the system's angular momentum against a threshold derived from material properties and geometry.

### 4.5 The Hugoniot/EOS Pipeline — Materials-to-Math Verification Analogue

**Original result:** The Rankine-Hugoniot relations are classical thermodynamics (1870s). The M-ANEOS EOS framework was introduced by Thompson & Lauson (1972) and modified by Melosh (2007) and by Stewart et al. (2019/2020): Stewart, S.T., et al., "The Shock Physics of Giant Impacts: Key Requirements for the Equations of State," *AIP Conf. Proc.* 2272, 080003 (2020). DOI: [10.1063/12.0000946](https://doi.org/10.1063/12.0000946). arXiv: [1910.04687](https://arxiv.org/abs/1910.04687). **This pipeline is Stewart's; SZL makes no claim to it.**

**Hugoniot relations:**

\[
\rho_0 U_s = \rho_1 (U_s - u_p) \quad \text{(mass)}
\]
\[
P_1 - P_0 = \rho_0 U_s u_p \quad \text{(momentum)}
\]
\[
E_1 - E_0 = \frac{1}{2}(P_1 + P_0)(V_0 - V_1) \quad \text{(energy)}
\]

with the empirical linear fit \(U_s = c_0 + s \, u_p\).

**The M-ANEOS Helmholtz free energy:**

\[
F(\rho, T) = F_{\text{cold}}(\rho) + F_{\text{thermal}}(\rho, T) + F_{\text{electronic}}(\rho, T)
\]

with \(P = -(\partial F/\partial V)_T\) and \(S = -(\partial F/\partial T)_V\).

**SZL adaptation [PROPOSED]:** Stewart's pipeline — shock experiment → Hugoniot fit → entropy integration → phase-boundary calibration → free energy parameterization → hydrocode embedding — is a gold-standard **physics-to-math verification pipeline**. SZL's analogous pipeline is: physical system specification → formal model → Lean 4 theorem → machine-checked verification → deployment. The structural correspondence is: (physical measurement → Hugoniot) maps to (system behavior → formal specification); (EOS calibration → embedding) maps to (theorem proof → kernel lock). The lesson is that the verification pipeline is as important as the theorem itself, and that each stage must be honest about its domain of validity (the Hugoniot is valid up to ~1000 GPa for silicates; the Lean theorem is valid within the stated preconditions).

**Shock vaporization criteria [Stewart-Kraus et al. 2012]:**  
The entropy-based three-threshold phase classification for SiO₂: below \(S_{\text{IV}} = 3552 \, \text{J kg}^{-1}\text{K}^{-1}\), no vaporization; between \(S_{\text{IV}}\) and \(S_{\text{CV}} = 7254 \, \text{J kg}^{-1}\text{K}^{-1}\), partial vaporization; above \(S_{\text{CV}}\), complete vaporization. [[Kraus et al., JGR:P 117, E09009 (2012)](https://doi.org/10.1029/2012JE004082)]

**SZL structural analogue [PROPOSED]:** The Λ-v5 three-threshold structure — below `lamMin` the node is "decohered/discharged" (no execution); between `lamMin` and the nominal operating range, the node is in a degraded execution state; above the nominal range, full execution — is structurally identical to Stewart's three-threshold entropy classification. This analogy motivates the architecture but does not constitute a proof that the thresholds are correctly set.

### 4.6 The Corotation Limit (CoRoL) — Phase-Boundary Analogue to the Λ-v5 Closure Gate

**Original result:** Lock, S.J., Stewart, S.T., "The structure of terrestrial bodies: Impact heating, corotation limits and synestias," *JGR: Planets* **122**, 950–982 (2017). DOI: [10.1002/2016JE005239](https://doi.org/10.1002/2016JE005239). arXiv: [1705.07858](https://arxiv.org/abs/1705.07858). **This is Lock and Stewart's result; SZL makes no claim to it.**

**The CoRoL condition:**

\[
L > L_{\text{CoRoL}}(M, S_{\text{outer}}, Z)
\]

where \(L_{\text{CoRoL}}\) is a **surface** in \((L, M, S, Z)\) parameter space (not a single number). A body exceeds the CoRoL and forms a synestia if and only if its angular momentum \(L\) exceeds this surface for given mass \(M\), outer-layer entropy \(S_{\text{outer}}\), and compositional structure \(Z\).

Critically, the CoRoL is not a single number but a **multivariate threshold surface**. This is the structural analogue of the Λ-v5 closure gate: the gate is not a single number but a surface in (coherence, charge) parameter space, defined by \(\Lambda(t) = C(t) \cdot (\Delta p / \Delta p_0) \geq \Lambda_{\min}\). The analogy runs deep:

| CoRoL (Stewart) | Λ-v5 gate (SZL) |
|---|---|
| Parameters: \(L, M, S, Z\) | Parameters: coherence \(C\), charge \(q\), time \(t\) |
| Phase boundary: synestia formation | Phase boundary: execution permission |
| Below boundary: oblate spheroid (normal) | Below boundary: recharge/retune (blocked) |
| Above boundary: synestia (new regime) | Above boundary: execution (active) |
| Boundary computed by HERCULES code | Boundary set by \(\Lambda_{\min}\) configuration |

**SZL adaptation [PROPOSED]:** The CoRoL analogy motivates thinking of the Λ-v5 gate as a surface in parameter space rather than a scalar threshold. Future engineering work could parameterize \(\Lambda_{\min}\) by additional system state variables (analogous to how the CoRoL depends on \(S_{\text{outer}}\) and \(Z\)), creating a richer, environment-responsive closure gate. This is **[PROPOSED]** future work.

---

## 5. Three Frontier Candidate Theorems {#5-frontier-candidates}

This section addresses the three candidate theorems identified in `FRONTIER_RESEARCH_2026-06-11.md`, with precise honest statements of their current status.

### 5.1 Candidate A — Coherence Monotone Decay (Wave24): NOW OURS

**Status: [PROPOSED / Wave24] — fully drafted, staged, awaiting green lake build (PR \#225)**

Candidate A from the FRONTIER report — the strict antitonicity of \(C_{\ell_1}(\rho(t))\) under pure-dephasing Lindblad dynamics — is the subject of Section 3. It is now SZL's Wave24 theorem (`CoherenceDecay.lean`). The full statement, proof, and Mathlib lineage are given in Section 3 above. No further elaboration is needed here except to repeat the honest status:

- The theorem is **[PROPOSED]** as of the writing of this document.
- It becomes **[EXPERIMENTAL]** only on green `lake build` with no `sorry` (PR \#225).
- It **never** enters \(\mathcal{K}_{\text{locked}}\).
- The Λ-v5 floor remains a **[PROPOSED]** engineering gate.
- This result is world-first in Lean 4 for the machine-checked formalization of GKSL coherence decay, to the best knowledge of the SZL research team. No prior Lean 4 / Coq / Rocq / ACL2 formalization of this statement is known to us as of 2026-06-11 (the nearest prior work is Streltsov-Adesso-Plenio's analytic proof in [[Rev. Mod. Phys. 89, 041003 (2017)](https://doi.org/10.1103/RevModPhys.89.041003)] and BCP's resource-theoretic framework, neither of which is machine-checked).

The connection to quantum biology (the radical-pair compass of Schulten 1978 and Hore/Rodgers 2009) is **[NARRATIVE]** in the sense that the radical-pair mechanism involves a *different* kind of decoherence (singlet-triplet interconversion driven by anisotropic hyperfine coupling) than the pure-dephasing channel modeled here. The mathematical structure is analogous — GKSL dynamics with decay rate \(\gamma\) — but the radical-pair model involves off-diagonal elements in the singlet-triplet basis, not the energy basis. This distinction is noted honestly: the Wave24 theorem's physical scope is pure-dephasing, not the full radical-pair dynamics.

### 5.2 Candidate B — Khipu Quorum Safety: EXISTING WAVE23 RESULT

**Status: [CONJECTURE 2 — partial; the mathematical lemma is Wave23's existing result]**

Candidate B from the FRONTIER report — a Lean 4 machine-checked proof of quorum intersection safety for the Khipu BFT protocol — has been addressed at the mathematical core by Wave23. The **quorum-intersection lemma** — the combinatorial heart of BFT safety — is an existing Wave23 result. It is not new in this document, and it is NOT reclaimed as Wave24 or v6 work.

**The lemma (Wave23, existing):**

For a validator set \(V\) with \(|V| = 3f+1\), any two quorums \(Q_1, Q_2 \subseteq V\) with \(|Q_i| \geq 2f+1\) satisfy:

\[
|Q_1 \cap Q_2| \geq f+1
\]

Since at most \(f\) validators are Byzantine, the intersection contains at least one honest validator. The proof uses Finset inclusion-exclusion:

\[
|Q_1 \cap Q_2| = |Q_1| + |Q_2| - |Q_1 \cup Q_2| \geq (2f+1)+(2f+1)-(3f+1) = f+1
\]

This uses `Finset.card_inter_add_card_union`, `Finset.card_union_le`, and `omega` from Mathlib, all confirmed in `Mathlib.Data.Finset.Basic`. The proof is conditional on honest non-equivocation and \(|V| = 3f+1\).

**What remains as Conjecture 2:** The full Khipu BFT protocol safety proof — showing that the DAG construction, block certification, commit rules, and adversarial timing together satisfy non-forking and eventual liveness — remains open. The analogy in the academic literature is the gap between the quorum-intersection lemma and the full Rocq proof of Mysticeti safety/liveness [[Qiu, Xiao, Shao, IEEE S&P 2026](https://flint.cs.yale.edu/flint/publications/sp26.pdf)], which found a liveness bug in the original protocol that the mathematical lemma alone could not catch. Conjecture 2 requires protocol-level analysis, not just combinatorial mathematics.

**Context in the broader BFT landscape:**  
The state of the art in mechanized BFT proofs includes: Bythos (Coq/Rocq, CCS 2024) [[Pîrlea et al., DOI: 10.1145/3658644.3690355](https://dl.acm.org/doi/pdf/10.1145/3658644.3690355)]; Mysticeti (Rocq, S&P 2026) [[Qiu-Shao](https://flint.cs.yale.edu/flint/publications/sp26.pdf)]; AleoBFT (ACL2, 2024) [[Provable.com](https://provable.com/blog/creating-aleobft-formal-verification-milestone)]; HotStuff-2 (informal) [[Malkhi-Nayak](https://www.semanticscholar.org/paper/HotStuff-2:-Optimal-Two-Phase-Responsive-BFT-Malkhi-Nayak/dce87b1d4ac651034c315a4df178e2199eada366)]. A full Lean 4 mechanized proof of Khipu BFT safety would be, to the best of SZL's knowledge, the first Lean 4 mechanized BFT safety proof at the protocol level (the Wave23 lemma being the first Lean 4 mechanized *quorum intersection* proof). This remains future work.

### 5.3 Candidate C — Λ-Aggregator Fixed Point: PROPOSED WAVE25 FUTURE WORK

**Status: [PROPOSED — Wave25 future work]**

Candidate C from the FRONTIER report — a Lean 4 theorem establishing that the Λ-aggregator routing function has a least fixed point bounded above by \(\top\) (the top element of a complete lattice), with monotone convergence of iterates to that fixed point — is **proposed as Wave25 future work**.

**The proposed theorem (Conjecture C / Wave25):**

Let \(L : \alpha \to_o \alpha\) be an order-preserving (monotone) self-map on a complete lattice \(\alpha\) (representing the Λ-aggregator routing function). Then:

(a) The least fixed point \(\mathrm{lfp}(L)\) exists by the Knaster-Tarski theorem [[Knaster 1928; Tarski 1955; Mathlib: `OrderHom.lfp`](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Order/FixedPoints.html)].

(b) \(\mathrm{lfp}(L) \leq \top\) (bounded above — trivially true in any complete lattice, but domain-specifically meaningful as a bound on routing weight).

(c) The iterate sequence \(\bot, L(\bot), L^2(\bot), \ldots\) is monotone-increasing and its supremum equals \(\mathrm{lfp}(L)\) when \(L\) is \(\omega\)-Scott-continuous (Kleene's fixed-point theorem, already in Mathlib as `fixedPoints.lfp_eq_sSup_iterate`).

(d) A domain-specific corollary: any iterate starting below \(\mathrm{lfp}(L)\) remains below \(\mathrm{lfp}(L)\) (monotone convergence within bounds), using `OrderHom.map_le_lfp` from Mathlib.

**Why this is not done yet:** The proof of (a)-(c) relies almost entirely on Mathlib lemmas already in `Mathlib.Order.FixedPoints`. The **new work** for Wave25 is:

1. Instantiating the Λ-aggregator as a concrete `OrderHom` — establishing that the SZL routing weight space forms a complete lattice and that the aggregation function is monotone. This is a design assertion about the architecture, not a universal mathematical fact.
2. Proving the domain-specific corollary in (d) as a new Lean 4 lemma (not currently in Mathlib).
3. Verifying that the instantiation is sorry-free.

**Effort estimate:** 1–2 weeks for a focused Lean developer, given that Mathlib infrastructure is already in place.

**Connection to PURIQ tier routing [PROPOSED]:** The Λ-aggregator fixed-point theorem would formally establish that SZL's tier-routing weight function monotonically accumulates evidence until it reaches a fixed routing decision — mathematically formalizing the intuition that "the system eventually commits to a routing tier." The Polymathic AI approach [[polymathic-ai.org](https://polymathic-ai.org)] of cross-domain foundation models suggests a future where the Λ-aggregator is learned from multi-domain data; the Knaster-Tarski fixed-point framework would still apply to the learned function, provided it can be shown to be monotone.

---

## 6. Conclusion, Honest Limitations, Future Work, and Roadmap {#6-conclusion}

### 6.1 Summary of Honest Claims

This thesis has argued for and demonstrated the following, with precise epistemic labeling:

**[VERIFIED/PROVEN]:**
- The locked-proven kernel \(\mathcal{K}_{\text{locked}} = \{F1,F4,F7,F11,F12,F18,F19,F22\}\) at commit `c7c0ba17` consists of exactly eight machine-checked sorry-free Lean 4 theorems. This count is invariant.
- Conjecture 1 (Λ-aggregator unconditional uniqueness) is machine-checked **FALSE** unconditionally. A conditional Theorem U holds axiom-free.
- The GKSL/Lindblad master equation is the unique generator of a CPTP quantum dynamical semigroup [[Lindblad 1976](https://doi.org/10.1007/BF01608499); [GKS 1976](https://doi.org/10.1063/1.522979)].
- The \(\ell_1\)-norm coherence \(C_{\ell_1}\) is a valid coherence monotone satisfying the BCP axioms [[BCP 2014](https://doi.org/10.1103/PhysRevLett.113.140401)].
- The LS12 collision-scaling framework is the standard analytic model for planetary collision-regime classification [[Leinhardt-Stewart 2012](https://doi.org/10.1088/0004-637X/745/1/79)].
- The quorum-intersection lemma (Wave23) establishes the combinatorial heart of BFT safety in Lean 4.
- SLSA L1 and L2 are currently attained.

**[PROPOSED]:**
- Wave24: \(C(t) = C_0 e^{-\gamma t}\) is strictly antitone, nonneg, equals \(C_0\) at \(t=0\), tends to 0, and crosses the Λ-v5 floor at unique finite \(t^\star = (1/\gamma)\ln(qC_0/\Lambda_{\min})\). Staged, awaiting green lake build.
- The Sherman Morgan density-specific-impulse analogy: \(\rho \cdot I_{sp}\) as the correct merit function under fixed-resource constraints maps to capability-per-token routing.
- The Tsiolkovsky log-ratio as a budget-conservation analogy.
- The Stewart CoRoL as a phase-boundary analogy to the Λ-v5 closure gate.
- The Hugoniot/EOS pipeline as a materials-to-math verification pipeline analogue.
- The LS12 classifier as a collision-regime diagnostic analogue for 3D drone/vessel simulation.

**[CONJECTURE]:**
- Conjecture 1: Λ-aggregator unconditional uniqueness (machine-checked FALSE unconditionally).
- Conjecture 2: Full Khipu BFT protocol safety. The Wave23 quorum-intersection lemma addresses the mathematical core; the full protocol proof remains open.
- Candidate C / Wave25: Λ-aggregator least-fixed-point boundedness via Knaster-Tarski/Kleene (proposed future work).

**[NARRATIVE]:**
- Jack Kruse's claims regarding quantum biology of mitochondria, deuterium depletion, and magnetism serve as motivational framing only. They are not cited as evidence for any SZL technical claim. No SZL result depends on them. They do not appear in the load-bearing formalism anywhere in this document.

### 6.2 Honest Limitations

**Physical modeling limits of Wave24:** The Wave24 theorem models a single qubit under pure-dephasing Lindblad dynamics. Real quantum biological systems (the radical-pair compass [[Hiscock et al., PNAS 113, 4634 (2016)](https://doi.org/10.1073/pnas.1600341113)]; FMO photosynthetic coherence [[Cao et al., Science Advances 6, eaaz4888 (2020)](https://doi.org/10.1126/sciadv.aaz4888)]) involve multi-spin systems, non-Markovian dynamics, and non-pure-dephasing generators. The Wave24 theorem's physical scope is a single-qubit pure-dephasing model. The analogy to biological coherence is motivational, not demonstrative.

**The charge term is not Wave24:** The bioenergetic charge term \(\Delta p / \Delta p_0\) (Mitchell's chemiosmotic proton-motive force [[Mitchell, Nature 191, 144 (1961)](https://doi.org/10.1038/191144a0)]) is modeled and documented in v5 but is not the subject of a formal Lean 4 theorem in this document. The charge term's behavior is governed by different physics (electrochemical gradients, Wallace heteroplasmy [[Wallace, Annu. Rev. Genet. 39, 359 (2005)](https://doi.org/10.1146/annurev.genet.39.110304.095751)]) and requires separate formalization.

**The analogies are not theorems:** All four borrowed lineages (Sherman Morgan, Stewart, GKSL, BFT) furnish *methodological analogies* to SZL's architecture. An analogy is not a proof. The fact that the Tsiolkovsky equation has a log-ratio structure does not prove that SZL's budget router is optimal. The fact that the CoRoL is a multivariate phase-boundary surface does not prove that Λ-v5's closure condition is physically correct. These analogies motivate architectural choices; they do not certify them.

**Quantum biology remains contested for some claims:** The FMO photosynthetic coherence claim has been revised downward — Cao et al. 2020 establishes that interexciton coherences are too short-lived to have functional significance at physiological temperature. Proton tunneling in Complex I is computationally suggested but not rigorously proven in vivo [[Kaila, Hummer, Wikström, PNAS 111, 6988 (2014)](https://doi.org/10.1073/pnas.1319156111)]. The avian radical-pair compass mechanism is rigorously modeled (Hore group) but the in vivo proof that cryptochrome is the sensor remains indirect. SZL's use of quantum biological mathematics is grounded in the rigorously modeled components (GKSL, radical-pair spin dynamics) and explicitly not in the contested or speculative components.

**Supply-chain honest status:** SLSA L3, FedRAMP authorization, CMMC certification, and ATO are roadmap items. They are not currently attained. Any document asserting otherwise would be incorrect.

### 6.3 Future Work Roadmap

**Wave24 (immediate):** Complete the green `lake build` passing with zero `sorry` on `CoherenceDecay.lean` (PR \#225). Upon success, status upgrades from [PROPOSED] to [EXPERIMENTAL]. File will be DOI-stamped via Zenodo.

**Wave25 (6–12 months):** Λ-aggregator fixed-point boundedness and iterate-convergence theorem. Instantiate the Λ-aggregator as a `CompleteLattice` `OrderHom` in Lean 4; prove the Knaster-Tarski instantiation and the new convergence corollary. Estimated effort: 1–2 weeks of focused Lean development given Mathlib readiness.

**Wave26 (12–24 months, conditional):** Full Khipu BFT protocol safety proof in Lean 4. This requires formalizing the DAG construction, the block certification protocol, and the commit rules — analogous to the LiDO-DAG framework in Rocq used by Qiu-Shao for Mysticeti [[IEEE S&P 2026](https://flint.cs.yale.edu/flint/publications/sp26.pdf)]. Estimated effort: 3–6 person-months. If achieved, this would be the first Lean 4 mechanized full-protocol BFT safety proof.

**Green lake build milestone (PR \#225):** The target for elevating Wave24 from [PROPOSED] to [EXPERIMENTAL]. The build must pass with zero `sorry` and Lean-core axioms only. The CI check will be added to the release workflow.

**Non-Markovian coherence extension (research):** The Wave24 theorem models pure-dephasing Markovian Lindblad dynamics. A future extension would model non-Markovian dynamics using the Dyson-equation formulation of Fogedby [[arXiv:2202.05203](https://arxiv.org/abs/2202.05203)] or the path-integral equivalence of Reible et al. [[arXiv:2603.10839](https://arxiv.org/abs/2603.10839)]. This would require either a quantum mechanics library for Lean 4 (nascent; no current Mathlib coverage) or a suitable abstract algebraic reformulation.

**Charge term formalization (research):** Formalizing the Mitchell PMF equation and the Wallace heteroplasmy threshold as Lean 4 theorems. The target would be a strict monotone-decrease theorem for the charge term under depletion dynamics, analogous to Wave24's strict antitonicity for the coherence term.

**LS12 / collision classifier implementation:** Implementing the LS12 regime-boundary classifier in SZL's 3D drone/vessel collision visualization, with proper attribution to Leinhardt-Stewart. This is an engineering task, not a mathematical one, but the honest provenance framework established in Section 4 provides the citation template.

### 6.4 On the Doctrine of Honest Uncertainty

The governing epistemic commitment of SZL Holdings is that **trust is never 100%** and every claim carries an explicit confidence level. This is not a weakness — it is a design feature. The Morgan analogy is apt: Morgan did not claim to have found the best possible propellant; she claimed to have found a propellant that meets the mission requirements within the feasibility constraints. The Lean 4 theorems do not claim to prove that the governed-AI framework is correct for all inputs; they claim to prove that specific properties hold within specified preconditions.

This epistemic discipline is precisely what separates rigorous engineering from hype. The mathematical lineages drawn here — from 1950s propulsion optimization, from planetary science, from quantum physics, from distributed systems — are each, in their own domains, models of this discipline. They are cited here as methods and inspirations, not as endorsements or co-authors.

The unified framework is honest: it knows what it has proven, what it proposes, and what it conjectures. That honesty is the thesis.

---

## 7. References {#7-references}

### Core Mathematical Foundations

1. Lindblad, G. "On the generators of quantum dynamical semigroups." *Commun. Math. Phys.* **48**, 119–130 (1976). DOI: [10.1007/BF01608499](https://doi.org/10.1007/BF01608499)

2. Gorini, V., Kossakowski, A., Sudarshan, E.C.G. "Completely positive dynamical semigroups of N-level systems." *J. Math. Phys.* **17**, 821 (1976). DOI: [10.1063/1.522979](https://doi.org/10.1063/1.522979)

3. Baumgratz, T., Cramer, M., Plenio, M.B. "Quantifying Coherence." *Phys. Rev. Lett.* **113**, 140401 (2014). DOI: [10.1103/PhysRevLett.113.140401](https://doi.org/10.1103/PhysRevLett.113.140401)

4. Streltsov, A., Adesso, G., Plenio, M.B. "Colloquium: Quantum Coherence as a Resource." *Rev. Mod. Phys.* **89**, 041003 (2017). DOI: [10.1103/RevModPhys.89.041003](https://doi.org/10.1103/RevModPhys.89.041003) | arXiv: [1609.02439](https://arxiv.org/abs/1609.02439)

5. Winter, A., Yang, D. "Operational Resource Theory of Coherence." *Phys. Rev. Lett.* **116**, 120404 (2016). DOI: [10.1103/PhysRevLett.116.120404](https://doi.org/10.1103/PhysRevLett.116.120404) | arXiv: [1506.07975](https://arxiv.org/abs/1506.07975)

6. vom Ende, F. "Understanding and Generalizing Unique Decompositions of Generators of Dynamical Semigroups." *Open Syst. Inf. Dyn.* **31**, 2450007 (2024). DOI: [10.1142/S1230161224500070](https://doi.org/10.1142/S1230161224500070) | arXiv: [2310.04037](https://arxiv.org/abs/2310.04037)

7. Grigoletto, T., Tao, T., Ticozzi, F., Viola, L. "Exact Model Reduction for Continuous-Time Open Quantum Dynamics." arXiv:2412.05102 (2025). DOI: [10.48550/arXiv.2412.05102](https://arxiv.org/abs/2412.05102)

8. Manzano, D. "A Short Introduction to the Lindblad Master Equation." *AIP Advances* **10**, 025106 (2020). arXiv: [1906.04478](https://arxiv.org/abs/1906.04478)

### Propulsion Mathematics and Sherman Morgan

9. Morgan, G.D. *Rocket Girl: The Story of Mary Sherman Morgan, America's First Female Rocket Scientist*. Smithsonian Institution, 2013. [Smithsonian Libraries](https://www.si.edu/object/rocket-girl-story-mary-sherman-morgan-americas-first-female-rocket-scientist-george-d-morgan:siris_sil_1004942)

10. Demming, A. "Mary Sherman Morgan: The best kept secret in the space race." *Chemistry World*, March 8, 2021. [https://www.chemistryworld.com/culture/mary-sherman-morgan-the-best-kept-secret-in-the-space-race/4013329.article](https://www.chemistryworld.com/culture/mary-sherman-morgan-the-best-kept-secret-in-the-space-race/4013329.article)

11. NASA. "Explorer-I and Jupiter-C." NASA History. [https://www.nasa.gov/history/sputnik/expinfo.html](https://www.nasa.gov/history/sputnik/expinfo.html)

12. NASA Glenn Research Center. "Specific Impulse." [https://www.grc.nasa.gov/www/k-12/airplane/specimp.html](https://www.grc.nasa.gov/www/k-12/airplane/specimp.html)

13. NASA Glenn Research Center. "Ideal Rocket Equation." [https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/ideal-rocket-equation/](https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/ideal-rocket-equation/)

14. NASA NTRS. "Rho-Isp Revisited and Basic Stage Mass Estimating." [https://ntrs.nasa.gov/citations/20150016561](https://ntrs.nasa.gov/citations/20150016561)

15. Wikipedia. "Specific Impulse — Density Specific Impulse." [https://en.wikipedia.org/wiki/Specific_impulse#Density_specific_impulse](https://en.wikipedia.org/wiki/Specific_impulse#Density_specific_impulse)

16. Wikipedia. "Hydyne." [https://en.wikipedia.org/wiki/Hydyne](https://en.wikipedia.org/wiki/Hydyne)

17. Wikipedia. "Mary Sherman Morgan." [https://en.wikipedia.org/wiki/Mary_Sherman_Morgan](https://en.wikipedia.org/wiki/Mary_Sherman_Morgan)

18. Wikipedia. "Tsiolkovsky rocket equation." [https://en.wikipedia.org/wiki/Tsiolkovsky_rocket_equation](https://en.wikipedia.org/wiki/Tsiolkovsky_rocket_equation)

19. Eye4Education. "Magnificent Women: Mary Sherman Morgan." [https://eye4education.co.uk/wp-content/uploads/2015/06/Magnificent-Women-Mary-Sherman-Morgan.pdf](https://eye4education.co.uk/wp-content/uploads/2015/06/Magnificent-Women-Mary-Sherman-Morgan.pdf)

20. Astronautix. "LOX/Hydyne propellant." [http://www.astronautix.com/l/loxhydyne.html](http://www.astronautix.com/l/loxhydyne.html)

### Planetary Science and Stewart

21. Leinhardt, Z.M., Stewart, S.T. "Collisions between Gravity-Dominated Bodies: I. Outcome Regimes and Scaling Laws." *Astrophysical Journal* **745**, 79 (2012). DOI: [10.1088/0004-637X/745/1/79](https://doi.org/10.1088/0004-637X/745/1/79) | arXiv: [1106.6084](https://arxiv.org/abs/1106.6084)

22. Stewart, S.T., Leinhardt, Z.M. "Collisions between Gravity-Dominated Bodies: II. The Diversity of Impact Outcomes during the End Stage of Planet Formation." *Astrophysical Journal* **751**, 32 (2012). DOI: [10.1088/0004-637X/751/1/32](https://doi.org/10.1088/0004-637X/751/1/32) | arXiv: [1109.4588](https://arxiv.org/abs/1109.4588)

23. Ćuk, M., Stewart, S.T. "Making the Moon from a fast-spinning Earth: A giant impact followed by resonant despinning." *Science* **338**, 1047–1052 (2012). DOI: [10.1126/science.1225542](https://doi.org/10.1126/science.1225542)

24. Lock, S.J., Stewart, S.T. "The structure of terrestrial bodies: Impact heating, corotation limits and synestias." *JGR: Planets* **122**, 950–982 (2017). DOI: [10.1002/2016JE005239](https://doi.org/10.1002/2016JE005239) | arXiv: [1705.07858](https://arxiv.org/abs/1705.07858)

25. Lock, S.J., Stewart, S.T., Petaev, M.I., Leinhardt, Z.M., Mace, M., Jacobsen, S.B., Ćuk, M. "The Origin of the Moon from a Terrestrial Synestia." *JGR: Planets* **123**, 910–951 (2018). DOI: [10.1002/2017JE005333](https://doi.org/10.1002/2017JE005333) | arXiv: [1802.10223](https://arxiv.org/abs/1802.10223)

26. Stewart, S.T., et al. "The Shock Physics of Giant Impacts: Key Requirements for the Equations of State." *AIP Conf. Proc.* 2272, 080003 (2020). DOI: [10.1063/12.0000946](https://doi.org/10.1063/12.0000946) | arXiv: [1910.04687](https://arxiv.org/abs/1910.04687)

27. Kraus, R.G., Stewart, S.T., et al. "Shock Vaporization of Silica and the Thermodynamics of Giant Impact Events." *JGR: Planets* **117**, E09009 (2012). DOI: [10.1029/2012JE004082](https://doi.org/10.1029/2012JE004082)

28. Kraus, R.G., Root, S., Lemke, R.W., Stewart, S.T., et al. "Impact vaporization of planetesimal cores in the late stages of planet formation." *Nature Geoscience* **8**, 269–272 (2015). DOI: [10.1038/ngeo2369](https://doi.org/10.1038/ngeo2369)

29. Root, S., Townsend, J.P., et al., Stewart, S.T. "The principal Hugoniot of forsterite to 950 GPa." *Geophysical Research Letters* **45**, 3865–3872 (2018). DOI: [10.1029/2017GL076931](https://doi.org/10.1029/2017GL076931)

30. Stewart, S.T., et al. "Planetesimal Impact Vapor Plumes and Nebular Shocks form Chondritic Mixtures." *PSJ*, in press, 2025. DOI: [10.3847/PSJ/adbe71](https://doi.org/10.3847/PSJ/adbe71) | arXiv: [2503.05636](https://arxiv.org/abs/2503.05636)

### Byzantine Fault Tolerance

31. Castro, M., Liskov, B. "Practical Byzantine Fault Tolerance." *OSDI 1999*. [https://pmg.csail.mit.edu/papers/osdi99.pdf](https://pmg.csail.mit.edu/papers/osdi99.pdf)

32. Pîrlea, G., Sergey, I., et al. "Compositional Verification of Composite Byzantine Protocols (Bythos)." *ACM CCS 2024*. DOI: [10.1145/3658644.3690355](https://dl.acm.org/doi/pdf/10.1145/3658644.3690355)

33. Qiu, L., Xiao, J., Shao, Z. "Mechanized Safety and Liveness Proofs for the Mysticeti Consensus Protocol." *IEEE S&P 2026*. [https://flint.cs.yale.edu/flint/publications/sp26.pdf](https://flint.cs.yale.edu/flint/publications/sp26.pdf)

34. Malkhi, D., Nayak, K. "HotStuff-2: Optimal Two-Phase Responsive BFT." [Semantic Scholar](https://www.semanticscholar.org/paper/HotStuff-2:-Optimal-Two-Phase-Responsive-BFT-Malkhi-Nayak/dce87b1d4ac651034c315a4df178e2199eada366)

35. Yin, M., Malkhi, D. et al. "HotStuff: BFT Consensus in the Lens of Blockchain." *PODC 2019*. arXiv: [1803.05069](https://arxiv.org/abs/1803.05069)

36. Losa, G. et al. "AleoBFT Formal Verification Milestone." Provable.com, 2024. [https://provable.com/blog/creating-aleobft-formal-verification-milestone](https://provable.com/blog/creating-aleobft-formal-verification-milestone)

37. Spiegelman, A. et al. "Mysticeti: Reaching the Latency Limits with Uncertified DAGs." *NDSS 2025*. arXiv: [2310.14821](https://arxiv.org/pdf/2310.14821)

38. "Detection and Prevention of Byzantine Behaviour in DAG-based BFT." arXiv:2408.02000 (2024). [https://arxiv.org/html/2408.02000v1](https://arxiv.org/html/2408.02000v1)

### Formal Verification / Mathlib

39. The Mathlib Community. *Mathlib4*. GitHub. [https://github.com/leanprover-community/mathlib4](https://github.com/leanprover-community/mathlib4)

40. Mathlib4 documentation — `Order.FixedPoints` (Knaster-Tarski, Kleene, `OrderHom.lfp`). [https://leanprover-community.github.io/mathlib4_docs/Mathlib/Order/FixedPoints.html](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Order/FixedPoints.html)

41. Mathlib4 documentation — `Order.Monotone.Basic` (`StrictAnti`, `Antitone`, composition). [https://leanprover-community.github.io/mathlib4_docs/Mathlib/Order/Monotone/Basic.html](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Order/Monotone/Basic.html)

42. Mathlib4 documentation — `Analysis.SpecialFunctions.ExpDeriv` (`Real.strictMono_exp`, `Real.tendsto_exp_atBot`). [https://leanprover-community.github.io/mathlib4_docs/Mathlib/Analysis/SpecialFunctions/ExpDeriv.html](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Analysis/SpecialFunctions/ExpDeriv.html)

43. Mathlib4 documentation — `Combinatorics.SimpleGraph.Acyclic`. [https://leanprover-community.github.io/mathlib4_docs/Mathlib/Combinatorics/SimpleGraph/Acyclic.html](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Combinatorics/SimpleGraph/Acyclic.html)

44. Carneiro, M. "Lean4Lean: Towards a Verified Typechecker for Lean, in Lean." arXiv:2403.14064 (2024). [https://arxiv.org/abs/2403.14064](https://arxiv.org/abs/2403.14064)

45. Tang, X. "A Comprehensive Survey of the Lean 4 Theorem Prover." arXiv:2501.18639 (2025). [https://arxiv.org/abs/2501.18639](https://arxiv.org/abs/2501.18639)

46. Tao, T. "A slightly longer Lean 4 proof tour." Blog, Dec 2023. [https://terrytao.wordpress.com/2023/12/05/a-slightly-longer-lean-4-proof-tour/](https://terrytao.wordpress.com/2023/12/05/a-slightly-longer-lean-4-proof-tour/)

### Agentic LLM Routing

47. Feng, T., Shen, Y., You, J. "GraphRouter: A Graph-based Router for LLM Selections." *ICLR 2025*. arXiv: [2410.03834](https://arxiv.org/abs/2410.03834)

48. McLeish, S. et al. "Transformers Can Do Arithmetic with the Right Embeddings." *NeurIPS 2024*. arXiv: [2405.17399](https://arxiv.org/html/2405.17399v1)

49. ByteDance AI Lab. "Scaling Latent Reasoning via Looped Language Models (Ouro)." arXiv:2510.25741 (2025). [https://arxiv.org/html/2510.25741v2](https://arxiv.org/html/2510.25741v2)

50. Zhang, S. et al. "Plan-over-Graph: Towards Parallelable LLM Agent Schedule." arXiv:2502.14563 (2025). [https://arxiv.org/html/2502.14563](https://arxiv.org/html/2502.14563)

51. Hu, S., Lu, C., Clune, J. "Automated Design of Agentic Systems." arXiv:2408.08435 (2025). [https://arxiv.org/abs/2408.08435](https://arxiv.org/abs/2408.08435)

52. Polymathic AI. [https://polymathic-ai.org](https://polymathic-ai.org) | Simons Foundation, Dec 2024. [https://www.simonsfoundation.org/2024/12/02/new-datasets-will-train-ai-models-to-think-like-scientists/](https://www.simonsfoundation.org/2024/12/02/new-datasets-will-train-ai-models-to-think-like-scientists/)

### Quantum Biology

53. Hiscock, H.G. et al. (Hore group). "The Quantum Needle of the Avian Magnetic Compass." *PNAS* **113**, 4634 (2016). DOI: [10.1073/pnas.1600341113](https://doi.org/10.1073/pnas.1600341113)

54. Smith, L.D., Glatthard, J., Chowdhury, F.T., Kattnig, D.R. "On the Optimality of the Radical-Pair Quantum Compass." *Quantum Sci. Technol.* **9**, 035023 (2024). DOI: [10.1088/2058-9565/ad48b4](https://doi.org/10.1088/2058-9565/ad48b4) | arXiv: [2401.02923](https://arxiv.org/abs/2401.02923)

55. Adams, B. et al. "Quantum Evolution: Terrestrial Fine-Tuning of Magnetic Parameters." arXiv:2411.03316 (2024). [https://arxiv.org/html/2411.03316v1](https://arxiv.org/html/2411.03316v1)

56. Lambert, N. et al. "Quantum Biology." *Nature Physics* **9**, 10–18 (2013). [Semantic Scholar](https://www.semanticscholar.org/paper/Quantum-biology-Lambert-Chen/0c5598ab13a92ece0b01995d592ded31851fecf0)

57. Cao, J. et al. "Quantum Biology Revisited." *Science Advances* **6**, eaaz4888 (2020). DOI: [10.1126/sciadv.aaz4888](https://doi.org/10.1126/sciadv.aaz4888)

58. Kaila, V.R.I., Hummer, G., Wikström, M. "Electrostatics, Hydration, and Proton Transfer Dynamics in the Membrane Domain of Respiratory Complex I." *PNAS* **111**, 6988 (2014). DOI: [10.1073/pnas.1319156111](https://doi.org/10.1073/pnas.1319156111)

59. Schulten, K. et al. "Magnetic field effects in chemistry and biology." *Z. Physik. Chem.* **111**, 1 (1978). DOI: [10.1524/zpch.1978.111.1.001](https://doi.org/10.1524/zpch.1978.111.1.001)

60. Hore, P.J., Rodgers, C.T. "Quantum effects in biology." *PNAS* (2009). DOI: [10.1073/pnas.0711968106](https://doi.org/10.1073/pnas.0711968106)

61. Al-Khalili, J., McFadden, J. "The Origins of Quantum Biology." *Proc. R. Soc. A* **474**, 20180674 (2018). DOI: [10.1098/rspa.2018.0674](https://doi.org/10.1098/rspa.2018.0674)

### Bioenergetics

62. Mitchell, P. "Coupling of phosphorylation to electron and hydrogen transfer by a chemi-osmotic type of mechanism." *Nature* **191**, 144 (1961). DOI: [10.1038/191144a0](https://doi.org/10.1038/191144a0)

63. Wallace, D.C. "A Mitochondrial Paradigm of Metabolic and Degenerative Diseases, Aging, and Cancer." *Annu. Rev. Genet.* **39**, 359 (2005). DOI: [10.1146/annurev.genet.39.110304.095751](https://doi.org/10.1146/annurev.genet.39.110304.095751)

64. Lane, N. "Why Are Cells Powered by Proton Gradients?" *Nat. Educ.* (2010); arXiv: [2104.08076](https://arxiv.org/abs/2104.08076)

65. Reible, B., Ahmadkhani, A., Delle Site, L. "Lindblad↔PIMD equivalence." *Phys. Rev. A* **113**, 042205 (2026). arXiv: [2603.10839](https://arxiv.org/abs/2603.10839)

66. Fogedby, H.C. "Non-Markovian quantum dynamics." arXiv:2202.05203 (2022). [https://arxiv.org/abs/2202.05203](https://arxiv.org/abs/2202.05203)

### Order Theory / Fixed Points (Mathlib)

67. Tarski, A. "A lattice-theoretical fixpoint theorem and its applications." *Pacific J. Math.* **5**, 285–309 (1955).

68. Knaster, B. "Un théorème sur les fonctions d'ensembles." *Ann. Soc. Polon. Math.* **6**, 133–134 (1928).

69. Mathlib4. "Order.FixedPoints." [https://leanprover-community.github.io/mathlib4_docs/Mathlib/Order/FixedPoints.html](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Order/FixedPoints.html)

70. "Resource theory of coherence in continuous position basis." arXiv:2605.09014 (2026). [https://arxiv.org/html/2605.09014v1](https://arxiv.org/html/2605.09014v1)

---

### SZL Prior Published Work (Zenodo, 2026)

- The Loop Is the Product v1/v2: DOI [10.5281/zenodo.19867281](https://doi.org/10.5281/zenodo.19867281), [10.5281/zenodo.19934129](https://doi.org/10.5281/zenodo.19934129)
- Lineage-Aware RAG v5: DOI [10.5281/zenodo.20020846](https://doi.org/10.5281/zenodo.20020846)
- Sealed Constitutional Guardrails v6: DOI [10.5281/zenodo.20020845](https://doi.org/10.5281/zenodo.20020845)
- Lutar Omega Formalism v4: DOI [10.5281/zenodo.20020841](https://doi.org/10.5281/zenodo.20020841)
- SZL Doctrine v2: DOI [10.5281/zenodo.20174600](https://doi.org/10.5281/zenodo.20174600)
- SZL Thesis v5 (preceding document): internal, 2026-06-11

---

*Status tags applied throughout: **[VERIFIED/PROVEN]** peer-reviewed + machine-checked · **[PROPOSED]** SZL construct, not yet externally peer-reviewed · **[CONJECTURE]** open mathematical problem · **[NARRATIVE]** motivational framing only, not load-bearing.*

*Locked-proven count = EXACTLY 8: \(\{F1, F4, F7, F11, F12, F18, F19, F22\}\) at commit `c7c0ba17`. This count does not change in this document.*

*Conjecture 1: Λ-aggregator unconditional uniqueness — machine-checked FALSE unconditionally; conditional Theorem U holds axiom-free.*  
*Conjecture 2: Khipu BFT full-protocol safety — conditional quorum-intersection lemma exists (Wave23); full protocol proof open.*  
*Conjecture 3 (from v5): Holographic Λ bound — unproven, stated as Conjecture 3.*

*Wave24: [PROPOSED] — \(\mathrm{coh\_strictAnti}\), \(\mathrm{coh\_nonneg}\), \(\mathrm{coh\_zero}\), \(\mathrm{coh\_tendsto\_zero}\), \(\mathrm{lambda\_single\_crossing}\) in `CoherenceDecay.lean`, namespace `Lutar.QuantumBio.CoherenceDecay`. Becomes [EXPERIMENTAL] on green `lake build`, PR \#225. Never joins \(\mathcal{K}_{\mathrm{locked}}\).*

*Jack Kruse: [NARRATIVE] only. No SZL theorem or claim in this document depends on any assertion associated with Kruse.*

*SLSA: L1+L2 attested. L3, FedRAMP, CMMC, ATO: roadmap, not current status.*

*SZL Holdings · Stephen P. Lutar Jr. · ORCID 0009-0001-0110-4173 · Draft v6 — 2026-06-11*
