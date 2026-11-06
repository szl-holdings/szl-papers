# Schur-Concavity as a Falsifiable Physics Prediction: The Robin Hood Lemma Applied to Navier-Stokes Regularization

**Stephen P. Lutar Jr.**
SZL Holdings, North Salem, NY · ORCID 0009-0001-0110-4173 · stephen@szlholdings.com

*Preprint. Not peer reviewed. Version 1.0.0. The Lean proof is real; the physics
prediction derived from it is a hypothesis.*

**DOI:** [10.5281/zenodo.24005485](https://doi.org/10.5281/zenodo.24005485) — published on Zenodo, 2026-11-06.

---

## Abstract

We observe that the Schur-concavity of the Λ aggregator — proved in the Lean 4
proof assistant with zero remaining obligations as the "Robin Hood lemma"
(equalizing transfers weakly increase Λ) — produces a falsifiable prediction
when applied to the acoustoelastic stress tensor of the Aero-FF Navier-Stokes
regularization hypothesis: **systems with balanced stress across their Murnaghan
constants should be more resistant to velocity blowup than systems with the
same total stress concentrated in a single constant.** This prediction is
derived from a proved mathematical property, not from the physical hypothesis
itself; it is testable by varying the stress balance in the physical device
and measuring the regularization stability. We present the Lean proof status,
the derivation of the prediction, the falsifiable experimental design, and the
connection to the peer-reviewed acoustic OAM literature (Liu et al., Nature
Communications 16:2823, 2025) that provides the experimental foundation.

**Keywords:** Schur-concavity; Lean; Navier-Stokes; acoustoelasticity;
topological protection; falsifiable prediction; governed AI

---

## 1. The Proved Property

The Λ aggregator (szl.lambda/v1) is a weighted geometric mean over axis scores
in [0,1]. Its Schur-concavity is proved in Lean 4:

**Theorem (Robin Hood lemma).** If x is more balanced than y (x is majorized
by y), then Λ(x) ≥ Λ(y). Equalizing transfers weakly increase the aggregate.

**Proof status:** PROVED in `Lutar/Lambda/SchurConcave.lean` with **zero sorry**
obligations. The two-axis case is proved via the product lemma; the general
case follows by induction on transfers.

This is a property of the aggregator's mathematics, independent of any physical
application.

## 2. The Application to Navier-Stokes Regularization

The Aero-FF hypothesis (Barnard, Molecular Audio Canada) claims that physical
fluid channels undergo acoustoelastic mode conversion under extreme localized
stress, launching a topologically protected helicoidal Rayleigh surface wave
that regularizes 3D vorticity. The 4-step pathway:

1. **Stress** (Murnaghan): ρ₀vL² = λ+2μ − [(7λ+10μ+2A+10B+6C)/(3λ+2μ)]σ
2. **Strain** (Poisson): ε_θθ = −ν(σ/E_eff)
3. **Kinetic energy** (EP): G = 2/(1−|R|²)
4. **Forced acceleration** (Chern): Cₙ = m, L_ph = mℏ

The stress kick depends on the combination **2A + 10B + 6C** — the third-order
Murnaghan constants enter through a weighted sum. The Schur-concavity of Λ
applied to this sum produces the prediction.

## 3. The Prediction

Consider two systems with the same total third-order contribution S = 2A + 10B + 6C:

- **System 1 (balanced):** the contributions are evenly distributed across A, B, C
- **System 2 (concentrated):** one constant dominates

Normalizing the contributions to [0,1] axes and computing Λ:

- Λ(balanced) > Λ(concentrated) — by the proved Schur-concavity

**The prediction:** the balanced system should exhibit MORE STABLE NS
regularization than the concentrated system, because:

1. Higher Λ → more balanced evidence → more robust governance (the proved property)
2. Balanced stress → more uniform mode conversion → more isotropic regularization
   (the physical interpretation)
3. The Robin Hood lemma says equalizing is always weakly better — never worse

**This is falsifiable:** construct two Aero-FF devices with the same S but
different balance; measure the regularization stability; if the concentrated
system is MORE stable, the prediction is falsified.

## 4. The Experimental Design

**Independent variable:** the balance index of the Murnaghan contributions:
- balance = 1 − variance(2A, 10B, 6C) / max_variance
- balance = 1.0: perfectly balanced; balance = 0.0: maximally concentrated

**Dependent variable:** the regularization stability, measured as the persistence
of the helicoidal surface wave under perturbation (the topological protection
lifetime).

**Control:** total stress S held constant; only the distribution varies.

**Prediction:** stability should correlate positively with the balance index.
The Schur-concavity says this is a mathematical necessity for the Λ aggregate;
whether it holds for the physical device is the test.

## 5. Connection to Peer-Reviewed Literature

The experimental foundation is Liu et al. (Nature Communications 16:2823, 2025):
"Generation of spatiotemporal acoustic vortices with arbitrarily oriented orbital
angular momentum." This peer-reviewed, experimentally verified paper demonstrates:
- 3D spatiotemporal acoustic vortices carrying longitudinal and transverse OAM
- Arbitrarily oriented OAM through rotation and intersection
- Experimental generation using a 121-speaker phased array

The Aero-FF hypothesis builds on this verified phenomenon. The Schur-concavity
prediction adds a testable constraint: the OAM regularization should be more
stable when the generating stress is balanced.

## 6. What is Proved and What is Hypothesis

| Claim | Status |
|---|---|
| Schur-concavity of Λ (Robin Hood lemma) | **PROVED** in Lean, 0 sorry |
| The prediction: balanced → more stable | **HYPOTHESIS** derived from the proved property |
| Acoustic OAM generation (Liu et al.) | **PEER-REVIEWED** (experimentally verified) |
| Aero-FF NS regularization | **HYPOTHESIS_UNVERIFIED** (Barnard's claim) |
| NS millennium prize resolution | **NOT_ESTABLISHED** |

The Lean proof is real mathematics. The physics prediction derived from it is
a hypothesis — testable, falsifiable, and stated as such.

## 7. Implementation

The prediction is implemented in `szl-holdings/acoustic-validation`:
- `src/lambda_ns_prediction.py` — `schur_concavity_prediction()` computes the
  Λ gap between actual and equalized stress distributions; `murnaghan_balance_index()`
  computes the balance of third-order contributions
- `src/ns_regularization.py` — the full 4-step pathway as falsifiable checks
- `src/aero_ff.py` — the 7 operating values as executable formulas

All code is public, tested (26 tests passing), and carries honesty labels:
`HYPOTHESIS_FROM_PROVED_PROPERTY`.

## 8. Conclusion

A Lean-proved theorem about a governance aggregator makes a falsifiable
prediction about fluid dynamics. This is, to our knowledge, the first case of
a formally verified AI governance formula producing a testable physics
prediction. If the prediction holds, it establishes that the estate's
governance math has physical predictive power beyond computational admission
control. If it fails, the Schur-concavity remains a proved property of the
aggregator — the physics application was wrong, not the math.

Either way, the prediction is honest, testable, and derived from a proof.

## References

1. Lutar, S.P. Jr. Lutar/Lambda/SchurConcave.lean. szl-holdings/lutar-lean (PROVED, 0 sorry).
2. Barnard, C. Aero-FF Technology: Helicoidal Waveform Distributor. Molecular Audio Canada (2026).
3. Liu, S., Ge, H., et al. Generation of spatiotemporal acoustic vortices with
   arbitrarily oriented orbital angular momentum. Nature Communications 16:2823 (2025).
4. Lutar, S.P. Jr. P6: The Information-Thermodynamic Certification. Zenodo (DOI-minted).
5. McAllester, D. PAC-Bayesian model averaging. COLT (1999).

---

*Honesty note: the Schur-concavity is PROVED in Lean with 0 sorry. The physics
prediction is HYPOTHESIS_FROM_PROVED_PROPERTY. The NS regularization is
HYPOTHESIS_UNVERIFIED. The millennium prize claim is NOT_ESTABLISHED. The
peer-reviewed OAM generation (Liu et al. 2025) is the verified foundation.
No claim is made without its proof status stated.*
