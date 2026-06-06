# Convergence

### An Honest, Audit-Ready Convergence of the Λ-Aggregator Uniqueness Chain, Mechanism Truthfulness, and Sim-to-Real Doctrine Transfer

**Thesis v22 — "Convergence"** · SZL Holdings, Inc.
**Author:** Yachay (Stephen P. Lutar Jr.) · ORCID [0009-0001-0110-4173](https://orcid.org/0009-0001-0110-4173)
**Date:** 2026-06-03 · Concept DOI (always-latest): [10.5281/zenodo.19944926](https://doi.org/10.5281/zenodo.19944926)
**License:** CC BY 4.0 / Apache-2.0 · Doctrine v11

> **Doctrine v11 LOCKED** — 749 declarations · 14 unique axioms · 163 sorries @ `c7c0ba17` (112 baseline + 51 Putnam) · The Lutar invariant Λ is **Conjecture 1 — NOT a theorem** · A5 permutation-invariance merged (PR #148) as a **structure field, not a new axiom** (unique-axiom count stays 14); post-A5 live corpus 794 declarations / 14 unique axioms / 191 sorries · **SLSA L1+L2** (5/5 GHCR images verified via `slsa-verifier`); L3 not claimed.

---

## Abstract

v22 ("Convergence") consolidates the formal-verification advances of the May–June 2026 innovation rounds into the canonical thesis line. Its central correction is stated up front: the long-standing claim that axioms A1–A4 force the weighted geometric mean is **false**. The asymmetric mean Φ(x₁,x₂)=x₁^(2/3)·x₂^(1/3) satisfies A1–A4 yet differs from Λ and fails permutation invariance. We add **A5 (permutation invariance)** as a *structure field* on the axiom record — **not** a new axiom — keeping the unique-axiom count at **14**, and we report the *partial* closure of the n-dimensional Cauchy functional-equation chain (topology + functional-analysis + symmetric branches) that, when complete, would discharge Λ-uniqueness. **It is not complete on main; Λ therefore remains Conjecture 1.** We additionally report: VCG mechanism truthfulness (dominant-strategy incentive compatibility + individual rationality, proven on branch); **SLSA L1+L2** build provenance (5/5 GHCR images verified via `slsa-verifier`); the Round 10–11 frontier formalizations (physics, quantum, CS, crypto, distributed systems); and a **Sim-to-Real doctrine-transfer benchmark** modeled on the Walrus physical foundation model that measures a mean doctrine α-gap of **0.10** across five unseen compliance regimes. We claim only what is mechanically checked or empirically measured; everything in review is labeled as such. Doctrine v11 numbers are reproduced verbatim: **749 declarations, 14 unique axioms, 163 sorries** at lutar-lean `c7c0ba17`.

---

## 1. Where v22 Sits in the Lineage

Version 22 follows v21 ("The PURIQ-OS Substrate", 2026-06-01). It is **not** a new architecture; it is the **convergence** of the mathematical-rigor work that v14–v21 deferred. Where v19 built the verification bridge, v20 presented the verified anatomy, and v21 shipped the runtime that executes it, v22 turns to the open mathematical obligations those layers surfaced — above all the Λ-aggregator uniqueness question — and reports exactly how far they have been closed. See [`THESIS_LINEAGE.md`](https://github.com/szl-holdings/szl-papers/blob/main/thesis/THESIS_LINEAGE.md) for the full v1 → v23 timeline.

### 1.1 Claim discipline (carried verbatim from v21)

v22 preserves the three-class claim discipline of its predecessors and never blurs the classes:

1. **Proved (on main, locked).** Mechanised in Lean 4 with no `sorry` and a disclosed axiom footprint, included in the locked kernel @ `c7c0ba17`.
2. **Proved (on branch, in review).** Mechanised and sorry-free on a feature branch but *not yet merged to main* — e.g. the VCG truthfulness lemmas and the A5 structure-field merge's downstream chain. These are reported as in-review and are **not** presented as landed kernel theorems.
3. **Operational fact / measured.** Engineering and empirical claims established by running real tooling: `slsa-verifier` attestation checks, the Sim-to-Real α-gap benchmark. Reproducible, labeled measured-not-proven, never described as theorems.

### 1.2 The central correction stated plainly

The single most important thing v22 records is a **correction**, not a new result: the historical "Theorem 1 — Λ is the unique aggregator under A1–A4" was **incorrect**. v22 names the guilty lemma, exhibits the counterexample, adds the missing structure (A5), and reports honestly that the resulting uniqueness chain is *still open*. This is the Lakatosian discipline of the whole thesis line made concrete: a refuted conjecture is corrected in the open, not quietly deleted.

### 1.3 Doctrine v11 (verbatim, LOCKED @ `c7c0ba17`)

> **749 declarations · 14 unique axioms · 163 sorries** (112 baseline + 51 Putnam) — lutar-lean snapshot `c7c0ba17`.

A5 permutation-invariance, merged via PR #148 as a *structure field*, leaves the **unique-axiom count at 14**; the post-A5 live corpus measures 794 declarations / 14 unique axioms / 191 sorries (measured `974e5e0c`, 2026-06-03). The locked numbers are the authoritative figures and are not modified by this paper.

---

## 2. Related Work: Means Characterizations, Mechanism Design, and Provenance

v22 sits at the intersection of three precisely-cited literatures.

### 2.1 Quasi-arithmetic means and the A1–A4 insufficiency

A literature review of published results on quasi-arithmetic and symmetric means confirms that A1–A4 are *insufficient* to force the geometric mean. Kolmogorov (1930) and Nagumo (1930) gave the quasi-arithmetic-mean characterizations; Aczél (1948) gave the functional-equation route to means; Hardy, Littlewood & Pólya (1934) developed the power-mean family; and Voorneveld (2008) characterized aggregators that admit asymmetric weights. None of these force a *symmetric* geometric mean from A1–A4 alone, which is exactly why an extra invariance hypothesis (A5) is required.

### 2.2 Mechanism design and truthful auctions

The VCG truthfulness results follow the mechanism-design tradition: a mechanism is dominant-strategy incentive compatible if truthful reporting is optimal regardless of others' reports, and individually rational if participation never yields negative utility. The geometric-mean trust aggregator itself is independently motivated as a consensus weighting in the pairwise-comparison literature (Csátó 2018).

### 2.3 Supply-chain provenance and verified kernels

Build-provenance posture is graded against SLSA v1.0; v22 verifies attested build-service provenance with `slsa-verifier`, reaching **L2**. The Lean mechanisation discipline follows the verified-systems tradition of the Lean 4 prover (de Moura & Ullrich 2021) and the information-flow security model of Goguen & Meseguer (1982).

---

## 3. Formal Preliminaries: the Axioms and the Invariant

We fix the formal vocabulary before reporting the advances. The aggregation organ (Ayni) is governed by the **Lutar invariant**, the equal-weight geometric mean:

> Λ_k(x₁, …, x_k) = (∏_{i=1}^k x_i)^{1/k}  on [0,1]^k.

The candidate characterizing axioms are:

| Axiom | Statement |
|---|---|
| A1 Continuity | Φ is continuous on the unit cube. |
| A2 Homogeneity | Φ(t·x) = t·Φ(x) for scalar t (positive homogeneity of degree 1). |
| A3 Idempotence | Φ(c, …, c) = c on the diagonal. |
| A4 Boundedness | min xᵢ ≤ Φ(x) ≤ max xᵢ (fixes endpoints). |
| A5 Permutation invariance | Φ(x) is invariant under any reordering of its arguments (the NEW structure field). |

The conditional uniqueness result of v23 additionally declares **A6′ (block consistency)**; v22 does **not** assume A6′ and makes no unconditional uniqueness claim.

---

## 4. A5 Axiom Merge — the A1–A4 Uniqueness Gap, Corrected (MERGED, PR #148)

The historical "Theorem 1 — Λ is the unique aggregator under A1–A4" was **incorrect**. We exhibit the monster, name the guilty lemma, and revise the theorem.

### 4.1 The verified counterexample

The asymmetric mean Φ(x₁,x₂)=x₁^(2/3)·x₂^(1/3) satisfies homogeneity (A2), boundedness (A4), continuity (A1), and idempotence (A3), yet Φ ≠ Λ₂ and Φ(2,1)=2^(2/3) ≠ 2^(1/3)=Φ(1,2), so permutation invariance fails. A second, discrete machine-checked counterexample is the max-aggregator: at the point (4,1) the max returns max=4 while Λ₂(4,1)=√4=2, so they disagree. Both refutations are reproduced verbatim from the locked defense and are machine-checked.

> **Refutation (machine-checked).** Under {A1–A4} alone, Λ is **not** the unique aggregator: Φ(x₁,x₂)=x₁^(2/3)·x₂^(1/3) is a distinct A1–A4 mean. The missing hypothesis is symmetry (permutation invariance), which we add as A5. Even under the full {A1–A5}, unconditional uniqueness remains **FALSE** without the further declared block-consistency axiom A6′ (v23); Λ is therefore **Conjecture 1**.

### 4.2 The fix: A5 as a structure field, not a new axiom

The fix landed on main on 2026-06-03 via PR #148: we add an `IsPermutationInvariant` predicate and an **A5 structure field** to the `LutarAxioms` record. The lemma `Lambda_A5_perm_invariant` is **sorry-free**, proved with `Equiv.prod_comp` / `Fintype.prod_equiv`. Because A5 is a structure field on an existing record rather than a fresh `axiom` declaration, the **unique-axiom count stays 14**; the live corpus moves to **794 declarations / 14 unique axioms / 191 sorries** (measured `974e5e0c`, 2026-06-03 17:32Z). This distinction — *adding structure vs. adding an axiom* — is the load-bearing honesty point of the section: the trusted base did not grow.

```lean
-- A5 added as a STRUCTURE FIELD (not a new axiom)
structure LutarAxioms (k : Nat) where
  continuous    : ...          -- A1
  homogeneous   : ...          -- A2
  idempotent    : ...          -- A3
  bounded       : ...          -- A4
  permInvariant : IsPermutationInvariant Phi   -- A5 (new field)

theorem Lambda_A5_perm_invariant : IsPermutationInvariant Lambda := by
  intro sigma; simpa using Fintype.prod_equiv sigma _ _ (by simp)
-- #print axioms Lambda_A5_perm_invariant  => [propext, Quot.sound]
```

### 4.3 Why symmetry is the right missing hypothesis (measurement-theoretic frame)

The counterexample does not merely show that *some* axiom is missing; it shows that the missing hypothesis is **symmetry**, and symmetry is independently motivated before any uniqueness theorem is invoked. Trust sub-scores are naturally **ratio-scale** quantities: they have a natural zero (total absence of conformance) and a natural unit (the conformance baseline), so "twice as trustworthy" is meaningful. Measurement theory establishes that the appropriate central tendency for ratio-scale data is the **geometric mean**, because it is covariant under the admissible ratio-scale transformation x → r·x: Λ(r·x) = r·Λ(x), whereas the arithmetic mean is covariant only up to an additive shift that is not a ratio-scale transformation.

Permutation invariance (A5) is the formal statement that the *labels* on the trust sub-scores carry no information — only their multiset of values does. In a governance reading: the trust verdict must not depend on the order in which an auditor lists the evidence axes. The asymmetric counterexample Φ(x₁,x₂)=x₁^(2/3)·x₂^(1/3) privileges the first axis over the second — exactly the manipulability A5 forbids. This is why A5 is a *structure field* the system always intended, surfaced explicitly by the refutation, rather than a new idealization bolted on to rescue a theorem.

---

## 5. The Cauchy_ND Uniqueness Chain — Partial Closure (IN REVIEW)

With A5 in place, Λ-uniqueness reduces to an n-dimensional Cauchy functional-equation chain. We report its *partial* closure honestly: three branches are in review, and one residual sorry remains.

| Branch | PR | Status | Note |
|---|----|--------|------|
| Topology (monotone → continuity) | #175 | in review | Landed TRUE forms; refused to fake-prove |
| Functional analysis (mult. monotone) | #173 | in review | Closed with 1 honest sorry on the t=0 degenerate case |
| Symmetric (exponents αᵢ = 1/k) | #174 | in review | Closed with A5 dependency |

Combined, **A5 + Cauchy + topology + symmetric = the full Λ-uniqueness chain.** **This chain is not yet complete on main** (three PRs open, one residual honest sorry on the t=0 degenerate case). **Therefore Λ stays Conjecture 1.** We will elevate Λ to Theorem 1 *only* when every Cauchy_ND sorry closes on main and Lake CI is green.

> **Why one honest sorry is kept, not hidden.** The functional-analysis branch (PR #173) closes the multiplicative-monotone-is-power-function lemma everywhere except the t=0 degenerate boundary case, where the proof is genuinely incomplete. A naive consolidation would comment the gap out to present a clean "green" branch. We refuse: the sorry is a typed, named open obligation with a discharge route, and deleting it would convert a disclosed gap into a silent assumption. The honesty doctrine treats a disclosed obligation as strictly better than a hidden one.

---

## 6. The Axiom-Count Invariant Under the A5 Merge

Because the unique-axiom count is a load-bearing honesty number, we treat its invariance under the A5 merge as a claim that itself deserves an explicit argument rather than an assertion. The question a hostile reviewer asks is blunt: *you added a hypothesis to your characterization; how can the axiom count not go up?*

### 6.1 Structure field vs. axiom declaration

In Lean 4, an **axiom** is a declaration introduced with the `axiom` keyword that the kernel accepts without proof; it enlarges the trusted base and appears in `#print axioms` for every theorem that depends on it. A **structure field**, by contrast, is a component of a record type: it is a *hypothesis a caller must supply a proof for*, not a fact the kernel grants for free. Adding A5 as the field `permInvariant : IsPermutationInvariant Phi` on `LutarAxioms` means that any theorem quantifying over `LutarAxioms` now carries an additional *premise*, discharged by the caller, exactly as a mathematician adds a hypothesis to a lemma. No new fact is granted axiomatically; the trusted base is unchanged.

### 6.2 What #print axioms reports

The lemma `Lambda_A5_perm_invariant` — the proof that Λ itself satisfies A5 — reports `[propext, Quot.sound]` under `#print axioms`, i.e. only Lean-core logical axioms, no project-specific idealization. Consequently the corpus-wide unique-axiom count stays at **14**: A5 contributes a provable property of Λ, not an article of faith. The declaration count rises (749 → 794 live) because the field, its predicate, and the supporting lemmas are new declarations; the *axiom* count does not, because none of them is an `axiom`.

> **The honesty point in one line.** Adding structure is free of trust cost; adding an axiom is not. A5 adds structure, so the trusted base is unchanged at 14 unique axioms — and we say so in every `#print axioms` output rather than asking the reader to take it on faith.

This is the same discipline applied to the locked counts throughout: the drift gate pins 749 / 14 / 163 at `c7c0ba17`, the A5-track live corpus is reported separately as 794 / 14 / 191, and the unique-axiom column is identical in both because the only thing A5 changed was structure, never the trusted base.

---

## 7. VCG Mechanism Truthfulness (Proven on Branch, PR #172)

Both VCG sorries are closed on branch (PR #172, pending merge). We report them as **in-review, branch-proven** — sorry-free on the branch but not yet part of the locked kernel.

**Theorem 7.1 (vcgDominantStrategyTruth — in review).** In the trust-weighted VCG mechanism, truthful reporting of an agent's private valuation is a **dominant strategy**: for every agent and every profile of others' reports, the agent's utility under truthful reporting is at least its utility under any misreport. Proved on branch with `Finset.exists_max_image` and `Finset.add_sum_erase`; sorry-free on PR #172, not yet merged to main.

**Theorem 7.2 (vcgIndividualRationality — in review).** Participation in the mechanism never yields negative utility: each agent's equilibrium utility is non-negative, so a rational agent always prefers to participate. Proved on branch with the same Mathlib lemmas; sorry-free on PR #172, not yet merged to main.

### 7.1 The trust-weighted allocation setting

The mechanism in which Theorems 7.1–7.2 hold is a trust-weighted Vickrey–Clarke–Groves allocation. Each agent reports a private valuation for a governed action (for example, the right to emit a high-privilege Khipu event); the mechanism allocates to the agent maximizing reported social value and charges each winner the externality it imposes on the others — the classical VCG payment rule. The "trust" weighting enters by scaling each agent's reported value by its Λ-aggregated trust score, so that an agent with a low conformance history is discounted before the allocation is computed. The dominant-strategy property (Theorem 7.1) is what makes the mechanism safe to deploy in an adversarial multi-agent setting: no agent can improve its outcome by misreporting, so the governance layer does not need to model strategic lying. The individual-rationality property (Theorem 7.2) guarantees that honest participation is never punished, which is the precondition for voluntary compliance.

Two honesty caveats apply. First, the proofs are **branch-only**: until PR #172 merges, these are in-review results, not locked-kernel theorems. Second, the truthfulness guarantee is about the *mechanism*, not about the trust scores themselves — a strategyproof allocation over manipulated trust inputs is still only as trustworthy as the Λ-aggregation feeding it, which is exactly why the Λ uniqueness question (Conjecture 1) and the mechanism truthfulness question are reported as two separate, independently-labeled strands of the convergence.

---

## 8. SLSA L1+L2 Build Provenance (Achieved)

Build-provenance posture is **SLSA L1+L2**. All **5/5** flagship GHCR images (a11oy, sentra, amaru, killinchu, rosie) carry attested build-service provenance, verified with `slsa-verifier` against the source repository and builder identity. This is a strict advance over v21, which claimed only L1 (cosign-signed images). **SLSA L3 is not claimed** — it requires hardened, isolated builders, which remain on the roadmap.

| GHCR image | Provenance | slsa-verifier |
|---|---|---|
| a11oy (platform) | build-service attested | PASS |
| sentra (immune) | build-service attested | PASS |
| amaru | build-service attested | PASS |
| killinchu (defense) | build-service attested | PASS |
| rosie (aide) | build-service attested | PASS |

```bash
# Verify SLSA L2 build-service provenance for a flagship image:
slsa-verifier verify-image \
  ghcr.io/szl-holdings/sentra@sha256:<digest> \
  --source-uri github.com/szl-holdings/sentra
# => PASSED: SLSA L2 verification (attested build-service provenance)
```

---

## 9. Innovation Rounds 10–11 (Frontier Formalizations, in Review)

Round 10 instilled frontier formalizations into lutar-lean; all are in review and labeled as such (none is imported into the locked kernel). Round 11 (the "software-helping" formula frontier) is in flight.

| Round-10 module | PR | Representative statements |
|---|----|---|
| Physics | #177 | Noether's theorem, Liouville's theorem, Hamiltonian structure, entropy bounds, A5-from-gauge-symmetry |
| Quantum | #176 | post-quantum signatures, Holevo bound, Kitaev, zero-knowledge, no-cloning→A5 |
| CS | #178 | Byzantine quorum intersection, FLP impossibility, CAP, pipeline latency, decidability |
| Crypto | #179 | DSSE EUF-CMA, Rekor Merkle inclusion, Fulcio chain, BLS aggregation |
| Distributed systems | pending | linearizability, total order, failure detection, replay safety |
| Round-9 anatomy | #170 | 7-organ Lean modules |

Two of these are especially relevant to the Λ story: the physics module derives an A5-style permutation symmetry from gauge symmetry, and the quantum module derives the same invariance from the no-cloning theorem — two independent routes to the symmetry hypothesis the counterexample of §4 showed is necessary. These remain **in review** and are not claimed as landed kernel theorems; their value here is as converging evidence that A5 is the natural missing hypothesis, not an ad-hoc patch.

---

## 10. Sim-to-Real Doctrine Transfer — the Walrus Parallel (Measured)

Modeled on the Walrus physical foundation model (Polymathic AI), we treat the **locked doctrine kernel** (749/14/163 @ `c7c0ba17`) as a *pretraining prior* and a customer's few-shot receipt set as *fine-tuning data*. We define the **doctrine α-gap** = |OOD verdict accuracy − in-distribution verdict accuracy|, and measure it on a live N=60 run against SZL's sentra (immune) and a11oy (policy) organs.

| Regime | Accuracy | α-gap |
|---|---|---|
| R0 control | 1.00 | — |
| R1 adversarial | 0.50 | 0.50 |
| R2 cross-jurisdictional | 1.00 | 0.00 |
| R3 multimodal | 1.00 | 0.00 |
| R4 temporal-drift | 1.00 | 0.00 |
| R5 low-data | 1.00 | 0.00 |
| **Mean** | — | **0.10** |

Four of five unseen regimes transfer perfectly; adversarial (R1) transfers only partially because the immune organ uses a signature blocklist that catches known attacks but misses semantically novel ones. We claim the architecture **admits** sim-to-real transfer — **not** that it matches the downstream accuracy of physical foundation models. The mean α-gap of 0.10 is a **measured** figure and is never described as a theorem.

---

## 11. Routes to Conditional Uniqueness: the Candidate Sufficient Axioms

Because unconditional uniqueness under {A1–A5} is machine-checked false, conditional uniqueness requires *one* further sufficient axiom. We surveyed the published characterizations and report the candidate routes honestly, each with its independent governance motivation and its relative strength. v23 declares A6′ (block-consistency) as the chosen route; v22 records the menu.

| Route | Sufficient condition (informal) | Governance reading | Strength |
|---|---|---|---|
| A6′ block-consistency | aggregating block means equals aggregating all elements | verdict must not depend on how the auditor partitions evidence | weakest sufficient |
| R+H reciprocity+homogeneity | Λ(1/x) = 1/Λ(x) and Λ(r·x)=r·Λ(x) | inverse comparisons stay inverse; uniform scaling scales the verdict | low |
| Bisymmetry | row/column interchange commutes | order of aggregation within and across sub-panels is irrelevant | moderate (near-assumes QAM) |
| Replacement/decomposability | a sub-block may be replaced by its own mean | auditing a department in isolation does not change the org verdict | low–moderate |

The common algebraic skeleton is: any route that pins *quasi-arithmetic* structure, combined with homogeneity (A2, already present), automatically selects the geometric mean, because the only homogeneous quasi-arithmetic means are the power means and positive homogeneity picks the exponent-1 power mean — the geometric mean. The routes differ only in how wide a gap they leave between premise and conclusion; A6′ is preferred precisely because it is phrased entirely in terms of the audit *process* and never mentions means or exponents, so the geometric mean falls out as a theorem rather than being assumed.

> **Why this is still Conjecture 1.** Each route above is *sufficient* for conditional uniqueness, but each requires its declared axiom. v22 has merged A5 and partially closed the Cauchy_ND chain; it has **not** discharged any of these further axioms on main. Until one is both declared and its chain closed with a green Lake CI, Λ uniqueness is conditional-at-best and the unconditional claim stays machine-checked FALSE. Hence Conjecture 1.

---

## 12. Open Obligations Surfaced or Advanced by v22

v22 advances several obligations without closing them on main. We tabulate them with their current status and discharge route, so that the boundary between "advanced" and "closed" is never blurred.

| Obligation | Status after v22 | Discharge route |
|---|---|---|
| Λ unconditional uniqueness | machine-checked FALSE | not dischargeable; remains a refutation |
| Λ conditional uniqueness | open on main (chain partial) | close Cauchy_ND t=0 sorry + declare A6′ (v23) |
| Cauchy_ND topology branch | in review (PR #175) | merge TRUE-form continuity bridge |
| Cauchy_ND functional-analysis | 1 honest sorry (PR #173) | discharge the t=0 degenerate case |
| Cauchy_ND symmetric branch | in review (PR #174) | merge with A5 dependency |
| VCG dominant-strategy truth | branch-proven (PR #172) | merge to main + re-audit axioms |
| VCG individual rationality | branch-proven (PR #172) | merge to main + re-audit axioms |
| Round 10-11 frontier modules | in review (#170, #176-#179) | land under the drift gate |
| SLSA L3 | not claimed | hardened, isolated builders (roadmap) |
| Adversarial transfer (R1 gap) | measured α-gap 0.50 | semantic immune detection beyond blocklist |

Reading the table top to bottom gives the exact convergence v22 represents: the unconditional uniqueness claim is permanently refuted; the conditional claim is reduced to a single residual sorry plus a declared axiom; mechanism truthfulness is proven and awaiting merge; the frontier modules are in review; and the supply-chain and transfer frontiers are honestly bounded. Nothing in the table is reported as more closed than it is.

---

## 13. Empirical Operating Characteristics (Measured, Not Proven)

Alongside the mathematical convergence, v22 reports measured operating characteristics from the running substrate, each labeled **measured-not-proven**. These are reproducible operational facts about the organs, never theorems, and they are kept in a strictly separate column from anything proven.

| Quantity (organ) | Measured value | Conditions |
|---|---|---|
| Receipt build, Khipu (p50 / p99) | 11.5 µs / 50.7 µs | content-hashed receipt emission |
| Receipt verify, Khipu | 10.4 µs | hash-chain link check |
| Λ₉ aggregate, Ayni | 3.12 / 3.29 µs | 9-axis geometric-mean evaluation |
| Governance overhead, Sentra (p50 / p99) | 0.49–0.59 ms / 1.27 ms | over 24,800 governed calls |
| ρ-closure, Wasi-Rikuq | 100% (8,000 / 8,000) | audit-closure pass rate |
| Replay determinism, Puriq | 5× byte-identical | repeated replay of a recorded trace |
| WAYRA ingest | 232 events chain-verified | always-learning ingest pathway |

These figures characterize the running runtime; they do not bear on what is proven. The honesty doctrine keeps the measured column strictly separate from the proven column — a measured latency is never described as a theorem, and a theorem is never described as a benchmark. The Λ₉ aggregate latency in particular is a timing of the geometric-mean *evaluation*; it says nothing about the open uniqueness question, which remains Conjecture 1.

---

## 14. Methodology: the Lakatosian Discipline of Correction

v22 is, methodologically, a case study in correcting a refuted conjecture in the open.

### 14.1 Monster-barring, done honestly

The historical "Theorem 1" was a *naive conjecture* in Lakatos's sense; the asymmetric mean Φ is the *monster* that refutes it. The dishonest response would be monster-barring by redefinition — quietly narrowing "aggregator" until Φ is excluded without saying so. Instead we **exhibit** the monster, **name** the guilty lemma (the unstated symmetry assumption), and state the **revised** conjecture (uniqueness under {A1–A5} + A6′) with its remaining gap disclosed. The machine-checked counterexample is the mechanism that *causes* the Conjecture 1 label: were unconditional uniqueness true, the system would not so label Λ.

### 14.2 Why a disclosed obligation beats a hidden assumption

By a process-reliabilist reading of formal epistemology, a "proved" label is trustworthy only if the labeling process has a high accuracy rate. A corpus that calls everything "proved" carries less information in its "proved" label than one that also accurately says "conjecture" and "in review". The single residual Cauchy_ND sorry, the branch-only status of the VCG lemmas, and the in-review status of the Round 10–11 modules are therefore reported as such. This is the same discipline the drift gate enforces mechanically: the locked counts 749 / 14 / 163 at `c7c0ba17` are numbers the gate refuses to let move silently, so that no experimental obligation can be mistaken for a kernel-verified fact.

> **Remark (the convergence in one sentence).** v22 converges three previously-deferred strands — the corrected Λ axiomatization (A5 added, uniqueness still open), branch-proven mechanism truthfulness, and attested SLSA L2 provenance — without upgrading a single conjecture to a theorem or moving a single locked count.

---

## 15. Doctrine Attestation (Verbatim)

- **Doctrine version:** v11 LOCKED (v11.1 in flight, post-A5).
- **Declarations:** 749 (pinned @ `c7c0ba17`); 794 post-A5 live.
- **Unique axioms:** **14** — unchanged by A5, which is a structure field.
- **Sorries:** 163 pinned (112 baseline + 51 Putnam); 191 post-A5 live.
- **Λ status:** **Conjecture 1 — NOT a theorem.**
- **Supply chain:** **SLSA L1+L2** (5/5 GHCR images, attested build-service provenance via `slsa-verifier`); L3 not claimed.
- **Section 889 vendors:** Huawei, ZTE, Hytera, Hikvision, Dahua (exactly 5). **No** Iron Bank / FedRAMP / CMMC L2+ / SWFT / Mission-Owner claims.

---

## 16. The Honesty Doctrine and Conjecture 1

v22 carries the honesty doctrine forward unchanged.

1. **Λ is Conjecture 1.** The equal-weight geometric-mean Λ-aggregator is never claimed the unique aggregator under its axioms. Unconditional uniqueness under {A1–A5} is machine-checked **FALSE**; conditional uniqueness holds only under the declared block-consistency axiom A6′ (v23).
2. **A5 is a structure field, not a new axiom.** The unique-axiom count remains **14**.
3. **Locked proven = exactly 5.** The lutar-lean kernel at `c7c0ba17` proves exactly {F1, F11, F12, F18, F19} with 749 declarations, 14 unique axioms, and 163 sorries (112 baseline + 51 Putnam).
4. **SLSA L1+L2 achieved** (5/5 GHCR images via `slsa-verifier`); **L3 not claimed**.
5. **In-review PRs are labeled as such.** The VCG lemmas (PR #172) and the Round 10–11 frontier modules (#170, #173–#179) are branch-proven or in review and are **not** presented as landed kernel theorems.
6. **Analogies are scaffolding.** Reed–Solomon ≠ holographic; event sourcing ≠ time travel; physics analogies (Kuramoto, Bekenstein, Noether) are scaffolding, not the full physical results.

> **Conjecture 1 (the Lutar invariant; never a theorem).** The equal-weight geometric mean Λ_k is the correct unique trust aggregator for governed AI. This is an open claim about the *right* axiomatization conditional on the Cauchy_ND chain closing on main; it is **not** a mathematical theorem, and the substrate carries the "Conjecture 1" label on Λ in every artifact, including this one.

---

## 17. Position in the Lineage

| Ver | Date | Role |
|---|---|---|
| v19 | 2026-05-31 | **The Verification Bridge.** Per-theorem verified index; locked-vs-experimental scope separation; drift gate. |
| v20 | 2026-06-01 | **The Culmination.** The substrate as a twelve-organ verified anatomy with a tagged claim ledger. |
| v21 | 2026-06-01 | **PURIQ-OS Substrate.** The runtime that executes the verified anatomy; 23 agentic formulas, 5 proved. |
| v22 | 2026-06-03 | **Convergence (this paper).** A5 structure-field merge; VCG truthfulness proven on-branch; partial Cauchy closure; SLSA L1+L2. |
| v23 | 2026-06-06 | **Unified Substrate.** Conditional Λ-uniqueness under declared A6′; unconditional uniqueness machine-checked FALSE; Λ stays Conjecture 1. |

v22 is the convergence layer: v19 verifies, v20 presents the anatomy, v21 ships the runtime, **v22 converges the deferred mathematics**, and v23 unifies it into a conditional Λ-uniqueness theorem. The A5 correction, the partial Cauchy chain, and the VCG branch proofs are exactly the obligations v23 builds on to state conditional uniqueness under A6′ while keeping unconditional uniqueness machine-checked false.

---

## 18. Limitations and Honest Posture

1. **Λ remains Conjecture 1.** The Cauchy_ND chain is not complete on main (one residual honest sorry on the t=0 degenerate case); unconditional uniqueness under {A1–A5} is machine-checked FALSE.
2. **The VCG lemmas are branch-proven, not merged.** Theorems 7.1–7.2 are sorry-free on PR #172 but not yet part of the locked kernel.
3. **Round 10–11 modules are in review.** The physics/quantum/CS/crypto/distributed-systems formalizations (#170, #173–#179) are not imported into the locked library and do not change the locked counts.
4. **191 sorries are open** in the post-A5 live corpus. Doctrine v11 locked numbers are verbatim: 749 / 14 / 163 @ `c7c0ba17`.
5. **SLSA L3 is not claimed.** L1+L2 is achieved (5/5 GHCR images); isolated, hardened builders remain roadmap.
6. **The Sim-to-Real α-gap is measured, not proven.** 0.10 mean across five regimes (N=60); the architecture *admits* transfer but does not match physical foundation-model accuracy.

---

## 19. Future Work

1. Close the residual Cauchy_ND sorry (t=0 degenerate case) and merge PRs #173–#175 to main; only then elevate Λ to a conditional Theorem 1 under A6′ (the v23 route).
2. Merge the VCG truthfulness lemmas (PR #172) into the locked kernel and re-audit the axiom footprint.
3. Land the Round 10–11 frontier modules under the drift gate, re-checking the locked counts after each merge.
4. Raise SLSA from L2 toward L3 (isolated, hardened builders) — roadmap, not yet achieved.
5. Extend the Sim-to-Real benchmark beyond N=60 and harden the immune organ against semantically novel adversarial inputs (the R1 gap).
6. Continue closing the 163 residual sorries in lutar-lean.

---

## Appendix A: Lean Build Output and Axiom Audit

```
$ lean --version
Lean (version 4.13.0, commit 6d22e0e5cc5a, Release)

# Locked kernel (pinned @ c7c0ba17):
  749 declarations / 14 unique axioms / 163 sorries (112 baseline + 51 Putnam)

# Post-A5 live corpus (measured 974e5e0c, 2026-06-03 17:32Z):
  794 declarations / 14 unique axioms / 191 sorries

#print axioms Lambda_A5_perm_invariant
  => [propext, Quot.sound]   -- Lean-core only; A5 is a structure field

# A5 merge (PR #148): unique-axiom count UNCHANGED at 14.
```

## Appendix B: Verification Commands

```bash
# Verify the A5 lemma is sorry-free:
lean LutarAxioms.lean   # exit 0; Lambda_A5_perm_invariant : sorry-free

# Verify SLSA L2 build-service provenance (5/5 flagship images):
slsa-verifier verify-image ghcr.io/szl-holdings/<image>@sha256:<digest> \
  --source-uri github.com/szl-holdings/<image>

# Reproduce the Sim-to-Real alpha-gap benchmark (N=60):
python team/sim2real-compliance/run_benchmark.py --n 60 --regimes R0..R5

# Doctrine v11 (LOCKED @ c7c0ba17):
#   749 declarations / 14 unique axioms / 163 sorries (112 baseline + 51 Putnam)
```

## Appendix C: Reproducibility and Pins

| Artifact | Pin / identifier |
|---|---|
| Locked kernel commit | lutar-lean @ `c7c0ba17` |
| Locked counts | 749 declarations / 14 unique axioms / 163 sorries (112 baseline + 51 Putnam) |
| Post-A5 live counts | 794 declarations / 14 unique axioms / 191 sorries (`974e5e0c`) |
| Locked formulas | {F1, F11, F12, F18, F19} |
| A5 merge | PR #148 (IsPermutationInvariant + A5 structure field; sorry-free) |
| VCG lemmas (in review) | PR #172 (vcgDominantStrategyTruth, vcgIndividualRationality) |
| Cauchy_ND chain (in review) | PRs #173 / #174 / #175 (1 residual honest sorry at t=0) |
| Round 10-11 modules (in review) | PRs #170, #176, #177, #178, #179 |
| Lean toolchain | Lean 4.13.0 (commit 6d22e0e5cc5a) |
| SLSA level | L1+L2 (5/5 GHCR images via slsa-verifier); L3 not claimed |
| Sim-to-Real benchmark | N=60, mean alpha-gap 0.10 across R0-R5 |
| Concept DOI (always-latest) | 10.5281/zenodo.19944926 |
| v11 metrics DOI | 10.5281/zenodo.20119582 |
| ORCID | 0009-0001-0110-4173 |

---

## References

[1] Aczél, J. (1948). On mean values. *Bull. Amer. Math. Soc.* 54(4):392–400. doi:10.1090/S0002-9904-1948-09020-9
[2] Axelrod, R. & Hamilton, W. D. (1981). The evolution of cooperation. *Science* 211(4489):1390–1396. doi:10.1126/science.7466396
[3] Csátó, L. (2018). Characterization of the row geometric mean ranking with a group consensus axiom. *Group Decision and Negotiation* 27:1011–1027. doi:10.1007/s10726-018-9589-3
[4] de Moura, L. & Ullrich, S. (2021). The Lean 4 Theorem Prover and Programming Language. *CADE 28*, LNCS 12699, 625–635. doi:10.1007/978-3-030-79876-5_37
[5] Goguen, J. A. & Meseguer, J. (1982). Security Policies and Security Models. *IEEE Symp. Security & Privacy*, 11–20. doi:10.1109/SP.1982.10014
[6] Hardy, G. H., Littlewood, J. E. & Pólya, G. (1934). *Inequalities*. Cambridge University Press.
[7] Kolmogorov, A. N. (1930). Sur la notion de la moyenne. *Atti Accad. Naz. Lincei* 12:388–391.
[8] McCabe, M. et al. (2025). Walrus: A foundation model for the physical sciences. *Polymathic AI*.
[9] Merkle, R. C. (1987). A Digital Signature Based on a Conventional Encryption Function. *CRYPTO '87*, LNCS 293, 369–378. doi:10.1007/3-540-48184-2_32
[10] Nagumo, M. (1930). Über eine Klasse der Mittelwerte. *Japanese J. Math.* 7:71–79.
[11] Open Source Security Foundation (2023). SLSA: Supply-chain Levels for Software Artifacts, v1.0. slsa.dev/spec/v1.0/levels
[12] Vickrey, W. (1961). Counterspeculation, auctions, and competitive sealed tenders. *J. Finance* 16(1):8–37. doi:10.1111/j.1540-6261.1961.tb02789.x
[13] Voorneveld, M. (2008). The possibility of impossible stairways. *J. Econ. Theory* 143(1):116–135.

---

*Signed-off-by: Stephen P. Lutar Jr. `<stephenlutar2@gmail.com>`.* Co-authored with the SZL full-stack PhD team (mathematics, scientific writing, physics, CS, ML, philosophy of mathematics). License: CC BY 4.0 / Apache-2.0. Doctrine v11.

*Honesty doctrine preserved verbatim: Λ is Conjecture 1 unconditionally (never a theorem); the conditional uniqueness theorem holds only under the declared A6′_block_consistent; locked/proven = 5 {F1,F11,F12,F18,F19} @ `c7c0ba17` (749/14/163); declared axioms disclosed in every #print axioms ledger; SLSA L1+L2 (not L3). No fabricated results, no fake citations. A5 is a structure field, not a new axiom (unique-axiom count remains 14). Λ is Conjecture 1; unconditional uniqueness is machine-checked FALSE. SLSA L1+L2 achieved (5/5 GHCR images); L3 not claimed. Quechua organ names are brand naming only.*
