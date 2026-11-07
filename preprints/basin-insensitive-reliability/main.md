# Basin-Insensitive Reliability: When Riddled Geometry Makes Reproducibility Unattainable, Certification Is the Correct Instrument

**Stephen P. Lutar Jr.**
SZL Holdings
ORCID 0009-0001-0110-4173

**Version:** v1.0.0 | **Status:** Preprint (not peer reviewed) | **Date:** 2026-11-07
**DOI:** [10.5281/zenodo.24043620 (concept)](https://doi.org/10.5281/zenodo.24043620) · [v1: 10.5281/zenodo.24043621](https://doi.org/10.5281/zenodo.24043621)

---

## Abstract

Recent work has established that the difficulty of reproducing deep-learning training outcomes is not merely an artifact of extrinsic randomness: Ly and Gong (2026) show that the basins of attraction governing training outcomes are *riddled* — every initialization leading to one solution lies arbitrarily close to initializations leading to different solutions — with an uncertainty exponent near zero, so that increases in initialization precision yield no material gain in reproducibility. We accept this result as given and ask the engineering question it forces: **if seed-level reproducibility is unattainable in principle, what is the correct reliability instrument for a trained model?** We answer with a synthesis of two independently developed lines of work: (i) a *governed distillation* pipeline in which a teacher model's outputs must pass a deterministic, fail-closed grounding gate before entering a student's training corpus, and (ii) *certified risk bounds* of the PAC-Bayes family, which bound the risk of whatever solution training finds, independently of which basin it landed in. We report a three-round measured arc on estate-scale models (0.8B–4B): free generation passes the grounding gate at 0.3% (0.8B teachers) and 2.7% (4B teacher); *gate-assisted* generation — the rule and the allowed identifiers placed in the prompt — passes at 1.3%, i.e. prompt-side assistance made acceptance *worse*, establishing that the confabulation floor at this scale is structural rather than instructional. We further report a null result in measuring the uncertainty exponent on a minimal deterministic setup (flip fraction 0.000 at perturbation scales $10^{-2}$ through $10^{-5}$), and name the design flaw: a task defined by the perturbed initialization admits no competing attractors. On the strength of these measurements we argue: (1) riddled geometry makes *predict-then-reproduce* a dead end as a reliability strategy; (2) the correct instrument when $\phi \approx 0$ is a bound that holds for the trained model itself — basin-independent by construction; and (3) the honest publication of failures (a 1.3% acceptance rate, a null $\phi$ measurement) is not an embarrassment to the certification program but its *demonstration*. All numbers in this paper are verbatim from published measurement receipts; none are simulated.

---

## 1. Introduction

A reliable AI system is one whose claims you can check. The industry's default answer to this has been reproducibility: fix the seed, pin the environment, and expect the same model twice. The dynamical-systems result of Ly and Gong (2026) removes that answer's foundation. Training outcomes are governed by riddled basin geometry — a fat fractal in which basins of different outcomes interleave at arbitrarily fine scales — with a measured uncertainty exponent near zero. In one image-recognition network, a single-bit change in initialization flipped the training outcome in roughly 48% of cases, and a ten-billion-fold increase in initialization precision produced no measurable reproducibility gain [1]. The implication is stark and was stated plainly by its authors: reproducibility of deep-learning training is limited by the mathematics of the learning process itself, not by engineering carelessness.

This paper is the engineering response. It does not dispute the result; it accepts it and asks what a builder should do. Our claim is that the correct reliability instrument, when training outcomes are effectively unpredictable at the seed level, is **certification of the trained artifact**: a statistical bound that holds for the model you actually have, whatever basin it landed in. This is precisely the property of PAC-Bayes generalization bounds [2, 3]: the bound is evaluated on the trained model's own parameters and a held-out sample; it does not ask which run produced them. Where Ly and Gong prove that *predicting the outcome* is hopeless, the certification program proves that *predicting the outcome was never necessary*.

To make this synthesis concrete rather than rhetorical, we contribute measured evidence from a production estate of small models (0.8B–4B parameters) trained and evaluated under a deterministic, fail-closed governance gate:

1. **The governed distillation gate (Section 3).** A teacher model's outputs enter a student's training corpus only if they pass a deterministic grounding gate: every identifier the response relies on must appear in the source context; responses must answer or abstain explicitly; degenerate outputs are rejected. The gate is the estate's admission mathematics applied to training data.

2. **A three-round measured arc (Section 4).** Free generation by 0.8B teachers passed the gate at 0.3%; the 4B teacher at 2.7%. A *gate-assisted* round — the grounding rule stated in the prompt together with the allowed identifiers — passed at **1.3%**: worse than unassisted. Prompt-side assistance does not break the confabulation floor; the floor is structural.

3. **A null uncertainty-exponent measurement, honestly recorded (Section 5).** Following Ly and Gong's method on a minimal deterministic setup, we measured flip fractions of 0.000 at all perturbation scales. We name the design flaw — our synthetic task was defined *by* the perturbed initialization, admitting no competing attractors — and publish the null result verbatim.

4. **The synthesis (Section 6).** Certification succeeds exactly where reproducibility fails: the PAC-Bayes bound is basin-insensitive by construction, and the governed gate's receipts — including its failures — are the demonstration that the certification program measures rather than markets.

The paper's stance on honesty is itself a contribution. Every acceptance rate, including the 1.3% that makes the gate-assisted round look bad, is published verbatim in a public receipt dataset with per-response evidence. The null $\phi$ measurement is published with its design flaw named. We hold that for a certification program, the willingness to publish unfavorable numbers is not a virtue signaling exercise; it is the *only* way the favorable numbers can mean anything.

### 1.1 Why this matters beyond one estate

The question "can I trust this model?" is being asked today under two inadequate answers. The first is *benchmark scores* — which measure a particular artifact and say nothing about whether you could have gotten a different one. The second is *reproducibility checklists* — which Ly and Gong's result renders unattainable at the level that matters, the identity of the trained solution. The third answer, developed here, is *certification*: a bound on the artifact you have, with the measurement that produced it attached as a receipt. The three-round arc and the null measurement are small-scale; the synthesis is not. If $\phi \approx 0$ holds at frontier scale — and Ly and Gong present evidence across architectures and scales — then every reliability program built on outcome prediction needs the basin-insensitive instrument this paper describes.

---

## 2. Related Work

**Riddled basins and the limits of reproducibility.** Riddled basin geometry originates in the dynamical-systems study of coupled chaotic systems [4, 5]: when an invariant subspace of a dynamical system loses stability transversally, the basins of the remaining attractors can become interwoven at every scale, so that no finite precision of initial conditions determines the outcome. Ly and Gong (2026) establish this geometry as a unifying mechanism for deep-learning irreproducibility: a minimal network model exhibits the classical route to riddling analytically; ~500,000 trained networks across architectures, datasets, and training methods exhibit uncertainty exponents near zero [1]. Their result rationalizes a decade of empirical observations that independently trained models differ [6, 7], and the seed-variance literature's finding that run-to-run differences can dominate reported benchmark gaps [8].

**PAC-Bayes certification.** The PAC-Bayes program [2, 3] bounds the expected risk of a learned predictor in terms of its empirical risk on a sample and a complexity term measuring the divergence of the learned predictor from a data-independent prior, holding with high probability over the draw of the sample. The bound is evaluated on the trained predictor; nothing in its statement references the training trajectory or its initialization. This is the property we lean on: the bound is *basin-independent by construction*. It does not matter which attractor training found; the bound prices the one it did.

**Governed admission for training data.** The gate studied here descends from a lineage of fail-closed admission contracts in the estate's production systems: receipt-attached decision chains [9], honest abstention evaluation [10], and free-energy certification connecting PAC-Bayes bounds to the free-energy principle [11]. The gate's semantics — fabrication, evasion, and degeneracy are the three failure classes — were hardened through five waves of adversarial review on the pipeline's own pull requests, including the discovery that a teacher shown its own answers (a missing generation prompt) cannot produce an honest acceptance rate, and that chat-model termination must be judged against the generation configuration's EOS list rather than the tokenizer's.

**The distinction we maintain.** Nothing in this paper claims that a bound *settles* a scientific question, nor that passing synthetic fixtures establishes biological validity. The reciprocal honesty clause under which the estate collaborates with measurement scientists states these limits explicitly, and we restate them here: agreement with a second rater is agreement; synthetic tests evaluate the method, not the world.

---

## 3. The Governed Distillation Gate

### 3.1 Definitions

Let a *prompt* be a source context $c$ (the user-side content of a conversation) and let $I(\cdot)$ extract the *identifiers* of a text: the maximal runs of word characters, separators, and version slashes that name artifacts — formula IDs, contract names, model names, DOIs. Let $A$ be a small whitelist of abstention and function tokens. A response $r$ to context $c$ is judged by:

$$
\mathcal{G}(c, r) \in \{\textsc{Accept}, \textsc{Reject}\}
$$

defined as the conjunction:

1. **Non-emptiness and termination.** $r$ is non-empty and the generation terminated on a configured end-of-sequence token (a generation stopped by the token cap is *truncated*, hence rejected).
2. **Non-degeneracy.** The repetition ratio of $r$ does not exceed a fixed threshold.
3. **Grounding.** Every identifier in $r$ outside $A$ appears in $c$: $\; I(r) \setminus A \subseteq I(c)$.
4. **Answer or abstain.** $r$ either carries substantive content or contains an explicit abstention marker.

Failures are named: a violation of (3) reports the fabricated identifiers; of (4), the evasion. The gate is deterministic, fail-closed, and testable; its implementation and test matrix (including contamination-before-assignment analogues for the related protocol work) are public.

### 3.2 The gate as measurement instrument

The gate's acceptance rate is not a quality score for the teacher. It is a **measurement of the teacher's confabulation floor**: the fraction of freely generated doctrine-targeted responses that are grounded in their own prompt. A low acceptance rate is a finding about the model, published verbatim; a high one would be a finding too. This stance — the gate measures rather than judges — is what makes the three-round arc interpretable.

### 3.3 Hardening history (measured)

Five review waves on the gate's implementation each caught a defect that would have corrupted the measurement: unused imports (cosmetic); a missing generation prompt and unstripped assistant turns, which would have shown teachers their own answers; an identifier regex that could not capture dotted names, making the fabrication filter partly unreachable; truncated generations passing for want of a termination check, and source-side code-fence identifiers wrongly stripped from the allowed set; and a termination check against the wrong end-of-sequence id — chat models stop on the generation configuration's EOS *list* (template turn closers), not the tokenizer's single EOS. The last defect would have undercounted every teacher. The lesson generalizes: **a measurement instrument needs its own adversarial review at the same standard as the thing it measures.**

---

## 4. The Three-Round Measured Arc

### 4.1 Setup

Teachers: estate-trained 0.8B models (Reasoning-v1, FreeEnergy-v1) and a 4B estate model (Nemotron-Mini-4B-Estate-v1). Prompts: a doctrine corpus of 150 conversation prompts targeting estate-specific facts (contract names, formula IDs, paper attributions, DOIs). Decoding: temperature 0.7, sampled, with per-round maximum generation lengths of 384–512 tokens. Every response — accepted or rejected — is receipted with its verdict, reasons, and response length; receipts are published to a public dataset at the moment of the run.

### 4.2 Round 1 — Free generation, 0.8B teachers

Acceptance: **0.3%**. Of ~300 generated responses across two 0.8B teachers, one passed. The rejection reasons were dominated by fabricated identifiers: invented formula IDs, invented paper attributions, invented DOIs — the model *knows the shape* of an estate fact and fills the shape with a guess. This is confabulation in the strict sense: fluent, confident, false.

### 4.3 Round 2 — Free generation, 4B teacher

Acceptance: **2.7%** (4/150). The 4B teacher confabulates less fluently wrong than the 0.8B teachers — an order of magnitude better at the gate — but 96.3% of its outputs still fail grounding. The corpus of four accepted examples is below the pre-registered floor for student training (≥32 examples), so the student wave correctly did not run. The preflight rule holding is the system working, not the experiment failing.

### 4.4 Round 3 — Gate-assisted generation, 4B teacher

The experiment this section exists for. If the confabulation floor were *instructional* — the teacher fabricating because it does not know the rule — then stating the rule and providing the allowed identifiers in the prompt should raise acceptance. We injected a system message stating the grounding rule verbatim ("use ONLY identifiers that appear verbatim in the prompt... If the prompt does not contain the information needed, reply ABSTAIN") and left the gate unchanged.

Acceptance: **1.3%** (2/150). *Worse than unassisted.* The gate-assisted teacher did not ground itself; it fabricated at a slightly higher rate while, anecdotally, producing more evasive non-answers. We report this without a settled explanation, offering the two candidate mechanisms the data permits: (a) instruction-following pressure competes with the generation prior and produces evasion-class failures; (b) the added rule text supplies more surface for near-miss fabrication. What the data does not permit is the comfortable reading — that with better prompting the floor would lift. **The confabulation floor at 0.8B–4B scale is structural, not promptable.**

### 4.5 What remains, honestly

Two approaches remain untried and one is a decision. *Constrained decoding* — masking the teacher's logits to the source context's token set during generation — grounds the output by construction, but changes the teacher's nature from generator to re-combiner; the receipts for such a round must state that the gate then measures coherence, not honesty. A *frontier-API teacher* may clear the gate at usable rates; that is a cost decision, and the measured 2.7% at 4B gives no principled extrapolation to frontier scale — it is an empirical question with a price tag. The third approach is the one this paper takes: accept the floor as a measured property of the model class and certify around it.

---

## 5. Measuring the Uncertainty Exponent: A Null Result

### 5.1 Method

Following Ly and Gong's method [1]: fix a base initialization; for perturbation scales $\varepsilon \in \{10^{-2}, 10^{-3}, 10^{-4}, 10^{-5}\}$, perturb the initialization by uniform noise of scale $\varepsilon$; retrain the same configuration; measure the flip fraction $f(\varepsilon)$ — the fraction of perturbed runs landing in a different outcome bucket. If $f(\varepsilon) \sim \varepsilon^{\phi}$, then $\phi$ near zero indicates riddled geometry (precision does not help) and $\phi$ near one indicates smooth basins. We ran 40 perturbed runs per scale on a minimal deterministic setup: a two-layer MLP (512→64→1), 60 SGD steps, fully deterministic seeding.

### 5.2 Result

$$f(\varepsilon) = 0.000 \text{ at every scale.}$$

No flips. The uncertainty exponent is not computable (the log-linear fit has no signal). **This is a null result and we publish it verbatim** [12].

### 5.3 The design flaw, named

The null was not bad luck; it was bad design, and the flaw is instructive. Our synthetic task was *defined by the perturbed initialization*: the training target was a function of the perturbed weights, so every perturbation moved the target and the training tracked it into the same outcome bucket. There were no competing attractors because the construction admitted none. A meaningful $\phi$ measurement requires the paper's minimal model — symmetry-induced invariant subspaces whose transversal instability creates genuinely competing basins. The null result is retained as the recorded first iteration: the design flaw is named, not hidden, and the correction is specified rather than improvised.

The deeper point survives the null: **measuring $\phi$ on one's own training runs is cheap at small scale, and the receipt trail the estate maintains is exactly the substrate such measurements need.** The corrected design — the symmetry-based minimal model, then seed-sweeps on the estate's recorded waves — is the natural continuation, and its cost is hours, not grants.

---

## 6. The Synthesis: Certification Succeeds Where Reproducibility Fails

### 6.1 The two instruments

| Property | Reproducibility (predict-then-reproduce) | Certification (bound-then-receipt) |
|---|---|---|
| Asks | "Will training land in the same basin?" | "What is the risk of the basin it landed in?" |
| Defeated by riddled geometry | **Yes** — $\phi \approx 0$ means precision does not help [1] | No — the bound is evaluated on the trained parameters |
| Instrument | Seeds, pinned environments, checklists | PAC-Bayes/McAllester bound + held-out sample + receipt |
| Failure mode | Silent: a reproduced run that is wrong *the same way* twice | Named: the bound is loose, and the receipt says how loose |

The PAC-Bayes bound $R(h) \leq \hat{R}(h) + \text{complexity}(h, \text{sample})$ holds with high probability over the data draw for the learned predictor $h$ *as trained*. Nothing in its derivation references the initialization, the trajectory, or the basin identity. This is not an accident to be exploited; it is the program's semantic center. A bound that held only for *reproducible* models would be useless precisely where Ly and Gong prove reproducibility unattainable.

### 6.2 What the estate's receipts add to the argument

The certification program's credibility rests on the same property the riddled-basins result makes unavoidable: **outcomes are not the unit of trust; measured artifacts are.** The estate's three-round arc demonstrates the practice end to end:

- The 0.3%, 2.7%, and 1.3% acceptance rates are published verbatim, with per-response evidence, at the moment of measurement [12].
- The null $\phi$ result is published with its design flaw named.
- The student-training floor (≥32 gate-accepted examples) held: no student was trained on a corpus that did not clear it, and the *reason* is recorded, not implied.

A skeptic reading these receipts learns more than from any favorable number: the program's failures are measured, named, and retained. That is the substance of the claim that certification is the correct instrument — its receipts are *willing to record disagreement with the program's own hopes*.

### 6.3 The engineering consequence

For a builder holding a trained model, the practical sequence under riddled geometry is:

1. **Do not spend on seed-level reproducibility** beyond what debugging requires; the geometry says the spend buys nothing at the outcome level [1].
2. **Certify the artifact**: evaluate a PAC-Bayes-family bound on the trained model against a held-out sample; publish the bound with its sample size, confidence parameter, and complexity term [11].
3. **Attach the receipt**: the bound, the measurement conditions, and — where relevant — the measured sensitivity (the $\phi$ program of Section 5, correctly designed) travel with the model as its reliability statement.
4. **Where the bound is loose, say so.** A loose bound with a receipt beats a tight claim without one; the receipt is the difference between measurement and marketing.

---

## 7. Limitations

**Scale.** All measured results are at 0.8B–4B parameters on single-node hardware. The riddled-basins mechanism is scale-insensitive in Ly and Gong's evidence, but our *gate* results are not known to extrapolate: a frontier teacher may clear the gate at rates that make the whole floor question moot, and we flag that as the cheapest decisive experiment we have not run (it is a cost decision, not an engineering one).

**Single-teacher-family confounds.** Rounds 2–3 used one 4B teacher; the gate-assisted result (1.3%) rests on 150 prompts and could shift under repetition. The direction of the finding (assisted ≤ unassisted) is what we claim; the specific gap is a single measurement.

**The null $\phi$ setup.** Section 5's null result reflects a flawed minimal design, not evidence against riddling; the corrected design is specified but not yet run. We are explicit that this paper's $\phi$ program is a design plus a null, not a measurement.

**Bounds are not correctness.** A PAC-Bayes bound bounds risk on a distribution; it does not certify a specific prediction, does not establish domain validity, and — as the estate's reciprocal honesty clause with its scientific collaborators states — agreement with a second rater is agreement, never independent proof.

**The gate measures grounding, not truth.** A response can pass the gate by correctly citing its prompt and still be scientifically wrong; the gate's claim is the absence of *fabrication*, which is a necessary, not sufficient, condition for trust.

---

## 8. Conclusion

Ly and Gong proved that the reproducibility program in deep learning rests on geometry that defeats it. This paper takes the result seriously in the only way an engineer can: by changing instruments. The measured arc reported here — three rounds of a governed distillation gate, a gate-assisted round that made acceptance *worse*, a null uncertainty-exponent measurement with its design flaw named — is offered as the working demonstration of the alternative: **certify the artifact you have, attach the measurement, publish the failures verbatim.** The confabulation floor at small scale is structural; the certification instrument is basin-independent; and the receipts that make the argument checkable are public. Where reproducibility fails by theorem, reliability must be built on what survives: measured artifacts, named limits, and the willingness to let the receipts disagree with the hopes.

---

## References

[1] Ly, A., & Gong, P. (2026). Fractal basin geometry and the limits to predictability and reproducibility in deep learning. *Nature Machine Intelligence*. Preprint: arXiv:2510.05606.

[2] McAllester, D. A. (2003). Simplified PAC-Bayesian margin bounds. *Neural Information Processing Systems*.

[3] Maurer, A. (2004). A note on the PAC-Bayesian theorem. arXiv:cs/0411099.

[4] Ott, E., Sommerer, J. C., & Yorke, J. A. (1994). On the riddled structure of basin boundaries in chaotic systems. As cited in [1] and the dynamical-systems literature on riddled basins and blowout bifurcations.

[5] Sommerer, J. C., & Ott, E. (1993). A physical system with qualitatively uncertain dynamics. *Nature*, 365, 136. (Basin-uncertainty antecedents as contextualized by [1].)

[6] Bouthillier, X., et al. (2021). Accounting for variance in machine learning benchmarks. *MLSys*.

[7] Picard, D. (2021). torch.manual_seed(3407) is all you need: The curious case of neural networks. arXiv:2109.12678. (Seed-variance evidence; the estate's training pipeline historically used seed 3407, an unremarked instance of the practice this literature examines.)

[8] Irreducible model variability as rationalized by [1]; measured instances in the estate's three-condition ablation (confabulation rates 4/6, 3/6, 5/6 across training conditions on the same probe family), receipts published [12].

[9] Lutar, S. P. Jr. (2026). Receipt-Attached Reliability: Whole-Chain Measurement for Governed MCP Tool Serving. Zenodo, concept DOI 10.5281/zenodo.24025910.

[10] Lutar, S. P. Jr. (2026). Honest Abstention Transfer in Small-Corpus Supervised Fine-Tuning: Measured Refusals, Not Invented Scores. Zenodo, concept DOI 10.5281/zenodo.24025916.

[11] Lutar, S. P. Jr. (2026). The Free-Energy Certification: PAC-Bayes Bounds as Governed AI Admission Criteria. Zenodo, concept DOI 10.5281/zenodo.24025918.

[12] SZL Holdings (2026). Model evaluation receipts, published verbatim at measurement time. Hugging Face dataset: SZLHOLDINGS/model-eval-receipts. Includes the three-round distillation gate receipts (0.3%, 2.7%, 1.3%), the khipu-r3 exact-bytes evaluation (FAIL, 1/6 abstained), and the null uncertainty-exponent measurement (f = 0.000 at all scales, design flaw named).

---

## Appendix A. Gate pseudocode

```
function GATE(context c, response r, terminated t):
    if r is empty:               REJECT [EMPTY_RESPONSE]
    if not t:                    REJECT [TRUNCATED_GENERATION]
    if repetition_ratio(r) > θ:  REJECT [REPETITION_LOOP]
    fabricated = identifiers(r) − whitelist − identifiers(c)
    if fabricated ≠ ∅:           REJECT [FABRICATED_IDENTIFIERS: fabricated]
    if not (answers(r) or abstains(r)):
                                 REJECT [NEITHER_ANSWERS_NOR_ABSTAINS]
    ACCEPT
```

Identifiers are maximal runs of `[A-Za-z][A-Za-z0-9_\-./]{3,40}` with trailing separators stripped; the source context's code-fenced identifiers count toward the allowed set; the response's code fences are stripped before extraction. Termination is judged against the generation configuration's complete EOS list.

## Appendix B. Receipt index

All receipts are public and were published at measurement time, win or lose:

| Receipt | Result | Verdict |
|---|---|---|
| Distillation round 1 (0.8B teachers, free) | 0.3% acceptance | Floor measured |
| Distillation round 2 (4B teacher, free) | 2.7% acceptance (4/150) | Floor measured; student floor (≥32) correctly held |
| Distillation round 3 (4B teacher, gate-assisted) | 1.3% acceptance (2/150) | **Assistance made it worse** |
| khipu-r3 exact-bytes confabulation probes | 1/6 abstained, 4 fabrications | FAIL, published |
| Uncertainty exponent (minimal setup) | f = 0.000 at all scales | NULL, design flaw named |

## Appendix C. Reproducibility statement

In keeping with the paper's own thesis, we do not claim the training outcomes described here are seed-reproducible; riddled geometry suggests they are not [1]. What is reproducible: the gate (deterministic, public, with its test matrix), the receipts (published verbatim), the analysis (all numbers in this paper are traceable to a receipt), and the null $\phi$ protocol (specified to the seed). The certified statements are the bounds and the receipts, not the basins.
