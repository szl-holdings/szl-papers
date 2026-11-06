# The Free-Energy Certification: PAC-Bayes Bounds as Governed AI Admission Criteria

**Stephen P. Lutar Jr.**
SZL Holdings, North Salem, NY · ORCID 0009-0001-0110-4173 · stephen@szlholdings.com

*Preprint. Not peer reviewed. Version 1.0.0. All Lean declarations cited at pinned
commits; all model measurements cite published receipts.*

---

## Abstract

We observe that the McAllester PAC-Bayes bound — already carried as a conditional
theorem in the SZL Lean surface — decomposes into exactly the two terms of Friston's
Free Energy Principle: an accuracy term (empirical risk) and a complexity term
(KL divergence to a prior). This identity is not metaphorical; the formulas are
the same. We exploit this to define a **free-energy certification** for AI models:
a certificate that computes a model's measured accuracy on a certified probe suite
and its complexity (KL to a declared prior), then bounds the model's true risk
using the McAllester inequality — with the bound itself carrying a Lean proof
status, a Hoeffding confidence interval, and a cryptographic receipt. The
certificate is then aggregated under the Λ-spine governance gate (advisory;
Conjecture 1 machine-checked false as stated), where a single failed measured
check vetoes admission regardless of the bound. We connect this to the deep
mathematical lineage of the estate: Liu Hui's polygon method (the first certified
computation with an error bound), Madhava's series (convergence with explicit
remainder), and the Schur-concavity of the Λ aggregator (proved in Lean as the
Robin Hood lemma). The result is a certification product that is simultaneously
statistical (PAC-Bayes), formal (Lean), governed (Λ-spine), and provenance-backed
(Khipu receipts) — a combination we believe to be novel.

**Keywords:** PAC-Bayes; free energy principle; model certification; Lean;
governed AI; statistical learning theory

---

## 1. Introduction

Two results from different fields state the same principle.

**Friston's Free Energy Principle** (neuroscience/philosophy): any adaptive
system that persists must minimize

  F = −⟨log p(model|data)⟩ = Accuracy + Complexity

where Accuracy measures how well the model predicts observations, and Complexity
measures how far the model's internal states diverge from prior expectations.

**McAllester's PAC-Bayes bound** (statistical learning theory): with probability
≥ 1−δ over samples S of size n:

  R(Q) ≤ R̂_S(Q) + √((KL(Q‖P) + ln(2√n/δ)) / (2n))

where R̂_S is the empirical risk (Accuracy), KL(Q‖P) is the KL divergence from
posterior to prior (Complexity), and the bound holds for any posterior Q.

The identity: **empirical risk IS the accuracy term; KL divergence IS the
complexity term; the PAC-Bayes bound IS the free-energy bound applied to model
selection.** The connection has been noted in passing (Friston himself cites
PAC-Bayes as a precursor), but never exploited as a *certification product*:
a bound on a model's true risk, computed from measured data, with formal proof
status, governed by an admission gate, and sealed with a receipt.

This paper does exactly that.

## 2. The Lean Surface

The estate's Lean surface (lutar-lean, pinned at commit `04f904ec`) contains:

- **TH13: PAC-Bayes bound for the Λ-gate governance head** — the McAllester bound
  as a conditional theorem, with two sorries discharged (BoundedIntegrability via
  Mathlib's `Integrable.mono'`, ChernoffOptimisation via explicit algebra).
  Status: **Theorem (conditional on Mathlib MomentSubGaussian)**.
- **Schur-concavity of Λ** (Lutar/Lambda/SchurConcave.lean): the Robin Hood
  lemma — equalizing transfers weakly increase Λ — **PROVED, 0 sorry**.
  This means the aggregator *prefers* balanced evidence over concentrated
  evidence, which is the resource-allocation principle the free-energy
  bound formalizes.
- **A2 (positive homogeneity) and A4 (boundedness) of Λ**: **PROVEN** in Lean.
- The full doctrine count: **749 declarations, 14 axioms, 163 sorries** —
  the honest inventory, carried verbatim.

The free-energy certification uses exactly these ingredients. No new
mathematics is claimed.

## 3. The Free-Energy Certificate

Given a model M, a certified probe suite of n probes, and a declared prior P:

1. **Measure accuracy**: run M on the probes; count errors → empirical risk R̂.
   Each probe's result is receipted (Khipu chain).
2. **Measure complexity**: compute KL(M‖P) — the divergence of the model's
   output distribution from the prior. In practice: the KL divergence of the
   model's response distribution on the probe set from the prior's.
3. **Compute the bound**: R(M) ≤ R̂ + √((KL + ln(2√n/δ))/(2n)).
   This is the free energy: accuracy + complexity.
4. **Attach the proof status**: the McAllester bound is a conditional theorem
   in Lean (TH13); the Hoeffding bound is proven; both are carried verbatim.
5. **Gate the certificate**: the free-energy bound is one axis of the Λ-spine
   gate. A model with a strong bound but a failed provenance check, a failed
   license check, or a measured confabulation is **still NO_GO** — zero-veto.
6. **Seal with a receipt**: the certificate is a Khipu receipt, DSSE-signed,
   independently verifiable.

## 4. The Ancient Lineage

The free-energy certification is the modern form of an ancient practice:

- **Liu Hui (3rd century CE)** computed π using polygon approximations with
  an explicit error bound: the difference between the inscribed and circumscribed
  polygons gives a certified interval. This is the first known *certified
  computation* — a result with its own error bound. The estate carries Liu Hui's
  formula in the 21-formula atlas.
- **Madhava of Sangamagrama (14th century)** derived series for π, sin, and cos
  with explicit remainder terms — convergence with certified truncation error.
  Again: a result with its own accuracy guarantee. The estate carries Madhava's
  series.
- **The Schur-concavity of Λ** (proved in Lean as the Robin Hood lemma):
  spreading evidence more equally across axes weakly increases the aggregate.
  This is the resource-allocation principle that the free-energy bound
  formalizes: a model that is accurate on everything but expert at nothing
  has higher Λ (more balanced) than one that is perfect on one axis and
  fails another.

The free-energy certificate continues this lineage: a computational result
with its own error bound, its own proof status, and its own receipt.

## 5. Connections to the Leaders

| Leader | Connection |
|---|---|
| **Tao (compressed sensing)** | The probe suite is a compressed measurement: few probes, provable bound. Tao's uncertainty principle work connects to the Bohr/Kochen-Specker formulas in the atlas. |
| **Susskind (holography)** | The certificate is a boundary encoding of the model's bulk behavior. The Bekenstein bound (in the atlas) is the entropy limit of the holographic encoding. |
| **Verlinde (entropic gravity)** | The Landauer formula (in the atlas) gives the energy cost of information. The free-energy certificate's complexity term IS an information cost. |
| **Deutsch (constructor theory)** | The Λ gate is an admission principle: what tasks are possible vs impossible, independent of the constructor (the model). |
| **Friston (free energy)** | The McAllester bound IS the free-energy bound. This paper makes the identity computational. |

## 6. Implementation

The certification is implemented in `formal-ai-underwriting/certification/bounds.py`
(merged to main): `pac_bayes_mcallester()` computes the bound from measured
inputs; `certify_risk()` produces the full certificate with both bounds and
the honesty contract. The Λ gate is implemented in `second_brain/hirag.py`
(merged to main) and `acoustic-validation/src/formula_governance.py` (merged).

## 7. Limitations

- The PAC-Bayes bound in Lean is **conditional** (TH13, on Mathlib
  MomentSubGaussian); the SORRY status is carried verbatim and never upgraded.
- The KL divergence measurement in practice requires declaring a prior; the
  choice of prior affects the bound. The certificate requires the prior to be
  declared and the KL to be measured, not assumed.
- The free-energy identity with Friston's principle is an observation about
  the structure of the formulas, not a claim that AI models are brains.
- The Λ aggregator is advisory; Conjecture 1 (uniqueness) is machine-checked
  false as stated. The gate does not depend on uniqueness.
- No claim that the certification predicts real-world performance; it bounds
  risk on the probe distribution, with the confidence level stated.

## 8. Conclusion

The McAllester PAC-Bayes bound and Friston's Free Energy Principle are the
same formula. The estate's Lean surface already carries the bound as a
conditional theorem; the Schur-concavity of the aggregator is proved; the
certification infrastructure exists. The free-energy certificate combines
statistical learning theory, formal verification, governed admission, and
cryptographic provenance into one product. Liu Hui would recognize it.

## Data Availability

- Lean surface: `szl-holdings/lutar-lean` at pinned commits
- Formula atlas: `szl-holdings/szl-formulas` (21 executable, 30 attributed)
- Certification bounds: `szl-holdings/formal-ai-underwriting` (merged)
- Λ gate: `szl-holdings/second-brain` (HIRAG, merged) and
  `szl-holdings/acoustic-validation` (formula_governance, merged)
- Governance validation certificates: `SZLHOLDINGS/model-eval-receipts`
- Reasoning corpus: `SZLHOLDINGS/reasoning-puzzles-sft-v1`

## References

1. McAllester, D. (1999). PAC-Bayesian model averaging. COLT.
2. McAllester, D. (2003). PAC-Bayesian stochastic model selection. Machine Learning 51(1).
3. Catoni, O. (2007). PAC-Bayesian supervised classification. IMS Lecture Notes 56.
4. Friston, K. (2010). The free-energy principle: a unified brain theory? Nat Rev Neurosci.
5. Maurer, A. (2004). A note on the PAC-Bayesian theorem. arXiv:cs/0411099.
6. Lutar, S.P. Jr. Ouroboros thesis line; Doctrine v11 (749/14/163). Zenodo concept DOI 10.5281/zenodo.19944926.
7. Lutar, S.P. Jr. TH13: PAC-Bayes bound for the Λ-gate. lutar-lean, pinned commit.

---

*Honesty note: the PAC-Bayes Lean obligation is SORRY (conditional); the Schur-concavity
is PROVED; Λ is advisory; Conjecture 1 is machine-checked false as stated. The
free-energy identity is an observation about formula structure, not a claim about
brains. No capability claim is made without a receipt.*
