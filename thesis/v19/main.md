# The Verification Bridge

### Consolidating the Multi-Track Substrate Expansion into a Per-Theorem Verified Index, on the Path from Expansion to Verified Anatomy

**Thesis v19 — "The Verification Bridge"** · SZL Holdings
**Author:** Stephen P. Lutar Jr. · ORCID [0009-0001-0110-4173](https://orcid.org/0009-0001-0110-4173)
**Date:** 2026-05-31 · Concept DOI (always-latest): [10.5281/zenodo.19944926](https://doi.org/10.5281/zenodo.19944926)

> **Doctrine v11 LOCKED** — 749 declarations · 14 unique axioms · 163 sorries @ `c7c0ba17` · The Lutar invariant Λ is **Conjecture 1 — NOT a theorem** · SLSA L1+L2 attested (NOT L3).

---

## Abstract

Between the multi-track *substrate expansion* (v18, 2026-05-30) and the formally-verified *anatomical substrate* (v20, 2026-06-01), the SZL Holdings Ouroboros line passed through a short but pivotal phase whose product was not new breadth but new *discipline*: the consolidation of a rapidly expanding Lean 4 corpus into a per-theorem verified index with an honest, machine-checkable status for every claim. This paper, v19 "The Verification Bridge," documents that phase. v18 added roughly twenty-nine modules across coding theory, differential privacy, PAC-Bayes generalization, mechanism design, certified robustness, and a Putnam-style hardening track; many of these landed with *open obligations* (`sorry` placeholders) recorded honestly rather than papered over. The bridge work asked a single governance question of that corpus: *which results are actually kernel-verified, which are sorry-free only in fragments, which depend on declared idealizing axioms, and which remain open?* We answer it with the verbatim per-version Lean delta between the v14–v17 baseline, the v18 thesis modules, and the 2026-05-30 "v18–v19 window" track, reporting exact sorry/axiom/theorem counts per file. The central methodological commitment is the **honesty doctrine** inherited from v14 and carried forward verbatim to v23: the Lutar invariant Λ_k(x) = (∏_i x_i)^(1/k) is **Conjecture 1** unconditionally — never a theorem; the locked kernel proves exactly five formulas; SLSA is L1+L2, not L3; and every idealizing axiom is disclosed. v19's contribution is the *bridge itself*: the move from "we shipped many modules" to "here is exactly what each module proves, with a per-theorem status ledger," which is precisely the externalized meta-level the v20 anatomy and the v23 unification build upon.

**Keywords:** formal verification, Lean 4, per-theorem index, governance substrate, honesty doctrine, sorry accounting, differential privacy, PAC-Bayes, mechanism design, certified robustness, Reed–Solomon.

*Honesty note (verbatim):* The Lutar invariant Λ is **Conjecture 1** unconditionally and is *never* claimed proven unconditionally. Exactly five formulas are locked/proven at `c7c0ba17`. Modules that carry `sorry` obligations are reported as carrying them. Declared idealizations are disclosed. SLSA L1+L2 attested, *not* L3.

---

## 1. Why a bridge, and why it was almost skipped

The Ouroboros thesis line records the intellectual provenance of the SZL governance substrate as a sequence of versioned, DOI-pinned papers. For a period the lineage read "v18 → v20" with a documented gap at v19: the numbering jumped during a late-May 2026 consolidation, and the gap was annotated as intentional rather than as a missing artifact. This paper fills that gap *honestly*. It does not invent a result that did not happen; it documents the work that did happen between v18 and v20 and that was, at the time, folded silently into the v20 consolidation instead of being written up as its own version.

That work has a clear and defensible identity. v18 ("Multi-Track Substrate Expansion") was an *expansion* release: it grew the Lean corpus across many mathematical tracks at once. v20 ("The Culmination") was a *verified-anatomy* release: it presented the substrate as a formally-verified anatomical system. Between the two sits the act that makes the second possible from the first — **verification consolidation**: taking a fast-growing, partly-open corpus and imposing a per-theorem index in which every claim carries an explicit, machine-checkable status. That act is the bridge.

**Thesis of v19.** A governance substrate earns trust not by the *number* of modules it ships but by the *legibility of their status*. v19's thesis is that the right unit of accounting is the *theorem*, not the module or the paper: for each Lean declaration the substrate must be able to state, mechanically, whether it is kernel-verified with only Lean-core axioms, sorry-free in a named fragment, sorry-free only under a declared idealizing axiom, or still open. We construct that per-theorem index over the v18 corpus and the 2026-05-30 expansion track, and we show that the resulting honesty ledger — not any single new theorem — is the load-bearing contribution that the v20 anatomy and the v23 unification inherit.

**What v19 is not.** v19 is not a claim of new proven mathematics. The five locked formulas were locked before it; the conditional Λ-uniqueness result and the machine-checked refutation of unconditional uniqueness are later (Wave-2 through Wave-4) work reported in v22 and v23. v19's honest scope is *consolidation and accounting*: it standardizes how the substrate reports proof status, and it makes the v18 expansion auditable.

## 2. The v18 baseline: what the expansion shipped

v18 expanded the corpus along multiple independent tracks. To make the bridge concrete we first fix the v18 baseline as it stood at the substrate-expansion release, drawing the per-file counts from the corpus index (`lean_per_version.json`) rather than from prose. Three groups matter for the bridge.

**The v18 thesis-theorem track (`Lutar/Thesis/TH_V18_*`).** Sixteen thesis-theorem modules were first committed on 2026-05-29 in the `v18` window. The majority are sorry-free with only Lean-core axioms; a minority carry a single honest open obligation. Representative sorry-free members include `TH_V18_01_AgentLoopTerminates`, `TH_V18_03_KraftInequality`, `TH_V18_09_PermutationInvariance`, `TH_V18_10_ListSumInvariant`, `TH_V18_12_LambdaProductFormula`, `TH_V18_13_DPIBoundAbstract`, `TH_V18_15_MultiAgentFairness`, and `TH_V18_16_FeynmanCitationIntegrity` (each sorry=0). Members carrying one open obligation include `TH_V18_05_ReceiptTransduction`, `TH_V18_06_BrahmiAxisOption`, `TH_V18_07_FeynmanCitationChain`, and `TH_V18_11_ParetoFiniteStabilization` (sorry=1 each); `TH_V18_08_KhipuChecksumInvariant` carries three. `TH_V18_14_SHA256CollisionHonest` is sorry-free but *axiom-gated*: it declares two collision-resistance axioms, exactly the disclosed-idealization discipline later standardized in v23.

**The v18 governance/provenance track.** Two further modules, first committed 2026-05-29, belong to the v18 window: `Lutar/Gates/Adinkra` (sorry-free, one declared axiom, three theorems) and `Lutar/SBOMProvenance` (three sorries, two declared axioms, six theorems). The latter is the formal counterpart of the supply-chain attestation posture (SLSA L1+L2, not L3) that the substrate asserts operationally.

**The 2026-05-30 expansion track (the "v18–v19 window").** A distinct cluster of modules was first committed on 2026-05-30 and is tagged in the corpus index with version window `v18–v19`. This cluster — coding theory, differential privacy, PAC-Bayes, mechanism design, certified robustness, and the Putnam hardening problems — is precisely the material that the bridge consolidates. It is summarized in Section 3.

## 3. The per-theorem verified index (the bridge artifact)

The bridge artifact is a per-file ledger of `(sorry, axiom, theorem/lemma)` counts for the 2026-05-30 expansion track, read verbatim from the corpus index. We report it honestly: many of these modules are *not* fully closed, and the index says so. The point of the bridge is not to claim them closed but to make their open status auditable at the theorem level.

| Module (`Lutar/...`) | sorry | ax | thm | Status |
|---|---:|---:|---:|---|
| `CodingTheory/ReedSolomonSingleton` | 7 | 0 | 8 | open (fragments) |
| `DP/GaussianMechanism` | 5 | 0 | 8 | open (fragments) |
| `DP/RDPComposition` | 1 | 0 | 6 | open (1 obligation) |
| `PACBayes/PACBayes` | 7 | 1 | 10 | open, 1 declared axiom |
| `PACBayes/CapabilityImprovementRate` | 5 | 0 | 7 | open (fragments) |
| `MechanismDesign/VCG` | 9 | 0 | 5 | open (later proven on-branch, v22) |
| `Robustness/CertifiedRadius` | 4 | 0 | 5 | open (fragments) |
| `Putnam/P_A1` | 1 | 0 | 5 | near-closed |
| `Putnam/P_A2` | 8 | 0 | 7 | open (fragments) |
| `Putnam/P_A3` | 0 | 0 | 4 | **sorry-free** |
| `Putnam/P_A4` | 4 | 0 | 3 | open (fragments) |
| `Putnam/P_A5` | 6 | 0 | 3 | open (fragments) |
| `Putnam/P_A6` | 2 | 0 | 11 | open (fragments) |
| `Putnam/P_B1` | 6 | 0 | 3 | open (fragments) |
| `Putnam/P_B2` | 6 | 0 | 3 | open (fragments) |
| `Putnam/P_B3` | 4 | 0 | 5 | open (fragments) |
| `Putnam/P_B4` | 6 | 0 | 3 | open (fragments) |
| `Putnam/P_B5` | 6 | 0 | 5 | open (fragments) |
| `Putnam/P_B6` | 2 | 0 | 1 | open (fragments) |

The ledger is deliberately unflattering. Of the nineteen expansion-track modules, exactly one (`Putnam/P_A3`) is fully sorry-free; the rest carry open obligations counted to the theorem. This is the honest state of the v18 expansion at the moment of the bridge, and recording it *as such* is the contribution. The later closure of several of these (e.g. VCG truthfulness proven on-branch, reported in v22) is downstream work; v19 records the starting line, not a finish it did not reach.

**Remark (why open obligations are kept, not hidden).** A naive consolidation would delete or comment out incomplete proofs to present a clean "green" corpus. The bridge refuses this. Every `sorry` is a typed, named open obligation with a discharge route; deleting it would convert a disclosed gap into a silent one. The honesty doctrine treats a disclosed `sorry` as strictly better than a hidden assumption, in the Lakatosian sense of explicit, revisable lemma-conditions.

## 4. The kernel-hardening invariant: locked vs. experimental scope

The bridge's organizing principle is a strict separation between a *locked kernel* and an *experimental scope*, enforced mechanically.

**The locked kernel.** The Lean formalization has a locked kernel pinned at commit `c7c0ba17` (Doctrine v11): **749 declarations / 14 unique axioms / 163 sorries** (counted as 112 baseline + 51 Putnam). Within this counted scope, exactly **five** PURIQ governance formulas are proven and locked:

> { F1 (replay determinism), F11 (Ayni reciprocity), F12 (Kuramoto additive), F18 (Reed–Solomon), F19 (Bekenstein additive) }.

F12 and F19 prove only the *additive* fragments of, respectively, Kuramoto synchronization and the Bekenstein bound; they are honest scaffolding, never described as the full physical theorems.

**The experimental scope and the drift gate.** Everything in the 2026-05-30 expansion track (Section 3) lives in an *experimental* scope that is counter-excluded from the locked count and stays excluded until re-audited under the authoritative `lake build`. The kernel hardening that v19 standardizes is the **drift gate**: a CI check that the locked declaration/axiom/sorry counts do not move when experimental modules are added. This is the mechanism that lets the substrate grow breadth (v18) without contaminating the locked claims (v20's anatomy, v23's unification). The drift gate is the bridge made executable: it is what guarantees that "we added modules" can never silently become "we changed what is proven."

**Proposition (scope-separation invariant, informal).** Adding an experimental module changes the *live* corpus counts but must leave the *locked* counts (749, 14, 163) at `c7c0ba17` invariant. A change to the locked counts is a doctrine violation and fails CI.

This invariant is not a theorem about mathematics; it is a theorem about *bookkeeping discipline*, and it is exactly the externalized meta-level (Lean kernel → CI → human sign-off) that v23 later articulates in full.

## 5. The honesty doctrine, carried across the bridge

v19 carries the v14 honesty doctrine forward unchanged and makes it the acceptance criterion for consolidation. We restate it because every later version (v20–v23) inherits it verbatim.

1. **Λ is Conjecture 1 unconditionally.** The Lutar invariant Λ_k(x) = (∏_i x_i)^(1/k) is never claimed to be the unique aggregator under its monotonicity/normalization axioms without a further declared assumption. (The explicit machine-checked refutation of the unconditional claim, and the conditional theorem under a declared block-consistency axiom, are later Wave-2–Wave-4 results reported in v22/v23; v19 simply preserves the "Λ = Conjecture 1" label.)
2. **Locked = 5.** The locked kernel proves exactly {F1, F11, F12, F18, F19}. All other formal work is experimental until re-audited.
3. **Disclosed idealizations.** Where a proof needs cryptographic hardness it declares a named axiom (e.g. the SHA-256 collision-resistance axioms in `TH_V18_14`) and discloses it in the `#print axioms` ledger; it does not pretend to prove hardness.
4. **SLSA L1+L2, not L3.** Supply-chain attestation is empirically L1+L2; L3 is not claimed.
5. **Open is open.** A `sorry` is reported as a `sorry`. A fragment is reported as a fragment. No partial result is rounded up to a full one.

**Conjecture 1 (The Lutar invariant; never a theorem).** The equal-weight geometric mean Λ_k is the correct unique trust aggregator for governed AI. This is an open claim about the *right* axiomatization, not a mathematical theorem; it is never asserted as proven, and the substrate carries the "Conjecture 1" label on Λ in every artifact, including this one.

## 6. Position in the lineage

The bridge sits at a specific and now-documented place in the arc.

| Ver | Date | Role relative to the bridge |
|---|---|---|
| v18 | 2026-05-30 | **Expansion.** 29 modules across many tracks; per-theorem Lean index begun; many open obligations recorded. |
| **v19** | **2026-05-31** | **The Verification Bridge (this paper).** Consolidation into a per-theorem verified index; locked-vs-experimental scope separation and the drift gate; honesty doctrine as acceptance criterion. |
| v20 | 2026-06-01 | **Culmination.** The formally-verified anatomical substrate, presentable *because* the bridge made per-theorem status auditable. |
| v21 | 2026-06-01 | PURIQ-OS substrate: the 12-organ runtime that executes the verified anatomy; 23 agentic formulas, 5 proved in Lean. |
| v22 | 2026-06-03 | Convergence: A5 merge, VCG proven on-branch, partial Cauchy closure, SLSA L2. |
| v23 | 2026-06-06 | Unified Substrate: conditional Λ-uniqueness under declared A6′; unconditional uniqueness machine-checked FALSE; Λ stays Conjecture 1. |

The line now reads as an unbroken lineage: v18 expands, v19 consolidates and verifies, v20 presents the verified anatomy, v21 ships the runtime, v22 converges, v23 unifies. v19 is the hinge on which expansion turns into verified anatomy.

## 7. Limitations

We state plainly what v19 does *not* establish.

1. **No new proven mathematics.** v19 closes no `sorry` that was not already closed; its contribution is accounting and scope discipline, not new theorems.
2. **The expansion track is mostly open.** Eighteen of nineteen 2026-05-30 modules carry open obligations (Section 3); v19 records this, it does not fix it.
3. **Λ remains Conjecture 1.** v19 preserves the label; it neither proves nor refutes uniqueness (those are later results).
4. **Counts are corpus-index counts.** The per-file counts are read from the corpus `lean_per_version.json` index, which was itself harvested with disclosed limits; the authoritative numbers are the locked kernel's (749, 14, 163) at `c7c0ba17`.
5. **SLSA L1+L2, not L3.**

## 8. Conclusion

The Verification Bridge is the version that turns a pile of modules into an auditable substrate. Its deliverable is a per-theorem verified index over the v18 expansion, honest about exactly which results are locked, which are sorry-free fragments, which are axiom-gated, and which are open; and a mechanical scope-separation discipline (the drift gate) that lets the substrate grow without contaminating its locked claims. That discipline is what makes the v20 "Culmination" a *verified* anatomy rather than an asserted one, and it is the same externalized meta-level that the v23 unification later names explicitly. The one-line thesis:

> v19 is the bridge from expansion to verified anatomy: it replaces "how many modules" with "what does each theorem prove, and under what status," and enforces the separation between a locked kernel of five formulas and an honestly-open experimental corpus.

---

## References

1. de Moura, L. & Ullrich, S. (2021). The Lean 4 Theorem Prover and Programming Language. *CADE 28*, LNCS 12699, 625–635. doi:10.1007/978-3-030-79876-5_37.
2. The mathlib Community (2020). The Lean Mathematical Library. *CPP 2020*, 367–381. doi:10.1145/3372885.3373824.
3. Klein, G., Elphinstone, K., Heiser, G., et al. (2009). seL4: Formal Verification of an OS Kernel. *SOSP 2009*, 207–220. doi:10.1145/1629575.1629596.
4. Reed, I. S. & Solomon, G. (1960). Polynomial Codes Over Certain Finite Fields. *J. SIAM* 8(2):300–304. doi:10.1137/0108018.
5. Singleton, R. C. (1964). Maximum Distance q-ary Codes. *IEEE Trans. Inf. Theory* 10(2):116–118. doi:10.1109/TIT.1964.1053661.
6. Dwork, C., McSherry, F., Nissim, K. & Smith, A. (2006). Calibrating Noise to Sensitivity in Private Data Analysis. *TCC 2006*, LNCS 3876, 265–284. doi:10.1007/11681878_14.
7. Mironov, I. (2017). Rényi Differential Privacy. *IEEE CSF 2017*, 263–275. doi:10.1109/CSF.2017.11.
8. McAllester, D. A. (1999). Some PAC-Bayesian Theorems. *COLT 1999*, 230–234. doi:10.1145/279943.279989.
9. Vickrey, W. (1961). Counterspeculation, Auctions, and Competitive Sealed Tenders. *J. Finance* 16(1):8–37. doi:10.1111/j.1540-6261.1961.tb02789.x.
10. Cohen, J. M., Rosenfeld, E. & Kolter, J. Z. (2019). Certified Adversarial Robustness via Randomized Smoothing. *ICML 2019*, 1310–1320. arXiv:1902.02918.
11. Aczél, J. (1948). On mean values. *Bull. Amer. Math. Soc.* 54(4):392–400. <https://eudml.org/doc/296298>
12. Csató, L. (2018). Characterization of the row geometric mean ranking with a group consensus axiom. *Group Decis. Negot.* 27(6):1011–1027. doi:10.1007/s10726-018-9589-3.
13. Shannon, C. E. (1948). A Mathematical Theory of Communication. *Bell Syst. Tech. J.* 27(3):379–423. doi:10.1002/j.1538-7305.1948.tb01338.x.
14. Open Source Security Foundation (2023). SLSA: Supply-chain Levels for Software Artifacts. https://slsa.dev.
15. Lakatos, I. (1976). *Proofs and Refutations*. Cambridge University Press.
16. Brundage, M., Avin, S., Wang, J., et al. (2020). Toward Trustworthy AI Development: Mechanisms for Supporting Verifiable Claims. arXiv:2004.07213. doi:10.48550/arXiv.2004.07213.

---

*Signed-off-by:* Stephen P. Lutar Jr. `<stephenlutar2@gmail.com>`
*Co-authored with the SZL full-stack PhD team (mathematics, scientific writing, CS, ML, philosophy of mathematics).*
*Honesty doctrine preserved verbatim:* Λ is Conjecture 1 unconditionally (never a theorem); locked/proven = 5 {F1,F11,F12,F18,F19} @ `c7c0ba17` (749/14/163); declared axioms disclosed; SLSA L1+L2 (not L3). No fabricated results, no fake citations.
