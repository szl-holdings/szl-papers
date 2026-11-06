# The Information-Thermodynamic Certification: Landauer, Bekenstein, and PAC-Bayes as One Principle

**Stephen P. Lutar Jr.**
SZL Holdings, North Salem, NY · ORCID 0009-0001-0110-4173 · stephen@szlholdings.com

*Preprint. Not peer reviewed. Version 1.0.0. All formula references trace to
the estate's 21-formula atlas; all Lean declarations at pinned commits.*

---

## Abstract

We observe that the physical bounds on information (Landauer's erasure cost,
Bekenstein's spatial entropy limit) and the statistical bounds on inference
(McAllester's PAC-Bayes risk bound, Hoeffding's concentration inequality) are
instances of a single principle: **information has a cost, and the cost must be
paid before the information is trusted.** The estate's 21-formula atlas carries
all of these bounds simultaneously, and its governed admission gate (the Λ-spine
with zero-veto) enforces them at the decision level. We present the unification,
map each bound to its atlas formula and Lean status, and demonstrate the
certification product that computes them all from measured data. The result is
an information-thermodynamic certification: every claim about a model's
capability, provenance, and risk is bounded by physical law, statistical law,
and governance law — simultaneously.

**Keywords:** Landauer principle; Bekenstein bound; PAC-Bayes; information
theory; thermodynamics of computation; model certification; governed AI

---

## 1. The Single Principle

Every bound in the estate's formula atlas answers the same question: **what is
the minimum cost of knowing something?**

| Bound | Cost measured | Minimum | Atlas formula | Proof status |
|---|---|---|---|---|
| **Landauer (1961)** | Energy to erase one bit | kBT ln 2 | `landauer` | Physical law |
| **Bekenstein (1972)** | Entropy in a spatial region | 2πRE/(ℏc) | `bekenstein_cascade` | PROVEN(TH6 DPI) |
| **Bremermann (1962)** | Computation rate | mc²/h | implicit | Physical law |
| **PAC-Bayes (McAllester 1999)** | Samples to bound true risk | R̂ + √((KL + ln(2√n/δ))/(2n)) | `pac_bayes_mcallester` | SORRY(PACBayes), Lean TH13 conditional |
| **Hoeffding (1963)** | Measurements for confidence | exp(-2nt²) | `hoeffding_tail` | PROVEN(Hoeffding) |
| **Kraft (1949)** | Code space allocation | Σ D^(-ℓᵢ) ≤ 1 | `reed_solomon_singleton` | PROVEN(TH_V18_03) |
| **Λ gate (Lutar 2026)** | Evidence for admission | Λ_w(x) = Π x_k^w_k | `lambda_aggregate` | Axioms A2/A4 PROVEN; Conjecture 1 FALSE as stated |

**The unification:** at every scale — physical, statistical, combinatorial,
governance — you cannot get information (or trust, or accuracy, or code space,
or admission) from nothing. The cost must be measured, stated, and paid.

## 2. The Physical Layer

### Landauer: information is physical

Rolf Landauer (IBM, 1961) proved that erasing one bit of information requires
a minimum energy of kBT ln 2. At room temperature, this is ~0.018 eV. His deeper
insight: **computation is a physical process and must obey thermodynamics.**

The estate's connection: the Khipu receipt chain is Landauer's principle made
computational. A hash-chained, append-only receipt cannot be erased without
visible evidence — the computational analog of the thermodynamic constraint.
Every receipt in the chain is physical information with a measurable cost.

### Bekenstein: information occupies space

Jacob Bekenstein (1972) bounded the maximum information (entropy) in a spatial
region: S_max = 2πRE/(ℏc). This is the holographic bound — the maximum
information that can fit in a region of radius R with energy E.

The estate's connection: the Living Anatomy is a holographic projection of the
estate — a lower-dimensional boundary encoding of a higher-dimensional system.
The Bekenstein bound is the entropy limit of that encoding. The certificate
IS a boundary encoding of the model's bulk behavior.

### Feynman: simulating physics requires quantum mechanics

Richard Feynman (1981) observed that simulating quantum systems on classical
computers is exponentially hard — you need quantum computers. The estate's
atlas carries the quantum foundations: Shor codeword distance, Kochen-Specker
witnesses, Bohr complementarity, Gleason's theorem, Kitaev surface codes.

## 3. The Statistical Layer

### PAC-Bayes: samples bound risk

The McAllester bound (already in Lean as TH13) bounds a model's true risk
from its measured performance plus its complexity. This IS Friston's Free
Energy Principle (P5, DOI-minted): accuracy + complexity.

### Hoeffding: measurements bound confidence

The Hoeffding bound gives the confidence interval for a bounded random variable
from n independent measurements. The estate's certification product computes
this from the measured probe sample.

## 4. The Governance Layer

### The Λ gate: evidence bounds admission

The Λ-spine aggregator (szl.lambda/v1) computes a weighted geometric mean over
measured axis scores. Its Schur-concavity (proved in Lean as the Robin Hood
lemma) means that more balanced evidence scores higher than concentrated
evidence. Its zero-veto property means a single failed measured check refuses
admission regardless of other scores.

### Kraft and Singleton: code space and error correction

The Kraft inequality bounds the allocation of code space; the Singleton bound
bounds the error-correction distance. Both are resource-allocation constraints
that the governance layer enforces alongside the Λ gate.

## 5. The Certification Product

The Formal AI Underwriting product (merged to main) computes all three layers
simultaneously:

1. **Physical**: the receipt chain's integrity (Landauer: information cannot
   be silently erased) + the certificate as a holographic encoding (Bekenstein)
2. **Statistical**: the PAC-Bayes risk bound + the Hoeffding confidence
   interval, both computed from the measured probe sample
3. **Governance**: the Λ-spine admission gate with zero-veto, plus the Kraft
   and Singleton resource-allocation bounds

The certificate carries:
- The computed risk bound with its confidence level
- The Lean proof status of every formula used
- The Khipu receipt chain position (tamper-evident provenance)
- The honesty contract: what the bound does and does not certify

## 6. The Ancient Continuity

This principle is not new. Liu Hui (3rd century CE) computed π with an explicit
error bound. Madhava (14th century) derived series with known truncation errors.
The Babylonian scribes verified quadratic solutions by substitution. The
Andean khipukamayuq maintained tamper-evident records for 5000 years.

**Every civilization that developed mathematics independently discovered that
results need bounds.** The estate's formula atlas is the modern continuation:
all the bounds, in one place, serving one admission gate, with Lean proof
status where available and honesty labels where not.

## 7. Limitations

- The Landauer bound is a physical law; the estate's receipts are a
  computational analog, not a physical implementation
- The Bekenstein bound is a dimensional helper; the certificate is not a
  physical hologram
- The PAC-Bayes Lean obligation is SORRY (conditional on Mathlib
  MomentSubGaussian); the Hoeffding bound is PROVEN
- The Λ aggregator is advisory; Conjecture 1 (uniqueness) is machine-checked
  false as stated; the gate does not depend on uniqueness
- No claim that the certification predicts real-world performance beyond the
  probe distribution with the stated confidence

## 8. Conclusion

Landauer proved information is physical. Bekenstein proved information
occupies space. McAllester proved information about risk requires samples.
Hoeffding proved confidence requires measurements. Kraft proved code space
is bounded. The Λ gate proves admission requires evidence, and a single
failure vetoes.

**They are all the same principle: you cannot get something from nothing.**
The estate carries every bound in one formula atlas, enforces them at one
admission gate, and certifies the result with receipts. Liu Hui would recognize
it. Landauer would approve. Feynman would ask what took us so long.

## Data Availability

- Formula atlas: `szl-holdings/szl-formulas` (21 executable, 30 attributed)
- Lean surface: `szl-holdings/lutar-lean` at pinned commits
- Certification bounds: `szl-holdings/formal-ai-underwriting` (merged)
- Λ gate: `szl-holdings/second-brain` (HIRAG) and `szl-holdings/acoustic-validation`
- Governed validation: `SZLHOLDINGS/model-eval-receipts`
- Reasoning corpora: `SZLHOLDINGS/reasoning-puzzles-sft-v1`,
  `SZLHOLDINGS/free-energy-reasoning-sft-v1`, `SZLHOLDINGS/ancient-math-reasoning-sft-v1`

## References

1. Landauer, R. (1961). Irreversibility and heat generation in the computing process. IBM J. Res. Dev. 5(3).
2. Bekenstein, J.D. (1972). Black holes and the second law. Lett. Nuovo Cimento 4.
3. Feynman, R.P. (1982). Simulating physics with computers. Int. J. Theor. Phys. 21.
4. McAllester, D. (1999). PAC-Bayesian model averaging. COLT.
5. Hoeffding, W. (1963). Probability inequalities for sums of bounded random variables. JASA 58.
6. Kraft, L.G. (1949). A device for quantizing, grouping, and coding amplitude-modulated pulses. MIT MS thesis.
7. Singleton, R.C. (1964). Maximum distance q-nary codes. IEEE Trans. Inf. Theory 10.
8. Friston, K. (2010). The free-energy principle. Nat. Rev. Neurosci. 11.
9. Lutar, S.P. Jr. Ouroboros thesis; Doctrine v11 (749/14/163). Zenodo 10.5281/zenodo.19944926.
10. Lutar, S.P. Jr. P5: The Free-Energy Certification. Zenodo (DOI-minted).

---

*Honesty note: Landauer and Bekenstein are physical laws, not Lean theorems.
PAC-Bayes is SORRY (conditional). Hoeffding is PROVEN. Λ is advisory; Conjecture 1
is machine-checked false as stated. Every bound carries its proof status verbatim.
No capability claim is made without a receipt. The ancients knew; the estate
makes it computational.*
