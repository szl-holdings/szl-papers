# Certified Benchmarks as Honest Evaluation Instruments: Measured Failures of Small Models on Unique-Solution Puzzles

**Stephen P. Lutar Jr.**¹ and **Sara Behnamian**²\*

¹ SZL Holdings. ORCID 0009-0001-0110-4173
² Lund University / University of Copenhagen

\* Authorship offered per the collaboration's standing pattern: the benchmark, its certificates, and the generation→encode→certify loop are Behnamian's; the measured model evaluations, the confabulation analysis, the contamination control, and the continuous-certification contribution are the estate's. Final author order to be agreed against the work, as is the collaboration's rule.

**Version:** v1.0.0 | **Status:** Preprint (not peer reviewed) | **Date:** 2026-11-07

**DOI:** [10.5281/zenodo.24043622 (concept; resolves to all versions)](https://doi.org/10.5281/zenodo.24043622)

---

## Abstract

Evaluation benchmarks earn trust by being hard to game and easy to verify. The certified unique-solution puzzle benchmark of Behnamian (zebra puzzles, Sudoku, Killer Sudoku, Futoshiki; dual-solver uniqueness certificates; a five-level deduction ladder) is among the few that carries machine-checkable proof that every released item has exactly one solution. This paper reports what happens when a fleet of small, estate-trained language models (0.8B–4B parameters) is evaluated against that benchmark under exact-answer scoring — and what the failures teach about evaluation itself. Our findings are uniformly uncomfortable and uniformly measured: freely-generating models fabricate puzzle *identifiers* and *solution structures* (a confabulation floor measured at 0.3%–2.7% gate acceptance across scales); fine-tuning on a certified corpus derived from the benchmark transfers format compliance but not solution ability; a three-condition ablation finds confabulation rates of 4/6, 3/6, and 5/6 across training conditions on the same probe family — irreducible model variability in the sense of the riddled-basin literature; and an audit of our own training corpus found 8 of 16 validation rows contaminated by group overlap, which we corrected with a group-disjoint split and now report as a methodological finding. As a contribution back to the benchmark, we make it *continuously certified*: a release-integrity contract that re-proves a stratified sample of the released certificates on every commit and the full 242-certificate bank weekly, so the benchmark's central claim is re-verified by machinery rather than frozen at release time. The throughline is the paper's thesis: **a certified benchmark is the only kind against which honest failure is measurable — and honest failure, published verbatim, is the most informative evaluation result there is.**

---

## 1. Introduction

Most model evaluations are scored against answers that are themselves unverified. A benchmark's answer key is trusted because a careful person made it; a model's score is trusted because the key was. The certified benchmark of Behnamian [1] breaks that chain of trust-by-attention in a way that matters for evaluation science: every released puzzle carries a solver certificate — uniqueness proved by MiniSat via PySAT and independently cross-checked with OR-tools CP-SAT, with clue-minimality, per-level deduction-ladder metrics, and minimal-unsatisfiable-core explanations for every derivable fact. When a model fails against such a benchmark, the failure cannot be attributed to the key.

This paper is the account of a small-model fleet meeting that benchmark, told the way the benchmark itself is built: with the failures as visible as the rest. It contributes:

1. **Measured confabulation on certified items (Section 4).** Freely-generating 0.8B–4B models fail not by being wrong about puzzles but by fabricating the *apparatus* of answers — puzzle identifiers, solution schemas, attributions — at measured rates (grounding-gate acceptance 0.3% for 0.8B teachers, 2.7% for a 4B teacher, and, decisively, **1.3% when the grounding rule and allowed identifiers were placed in the prompt**: assistance made it worse [2]).

2. **A three-condition ablation with irreducible variability (Section 5).** Three training conditions on certified-corpus derivatives — reasoning-annotated, free-energy-annotated, and ancient-math corpora — produce confabulation rates of 4/6, 3/6, and 5/6 on the same six-probe family. The spread is a single-family instance of the run-to-run and condition-to-condition variability that the riddled-basin geometry of Ly and Gong rationalizes as fundamental [3].

3. **A contamination audit of our own corpus (Section 6).** An audit of the estate's training mix found 8 of 16 validation rows sharing group provenance with training rows — a quiet leakage of the kind evaluation papers rarely admit. We report it, correct it with a group-disjoint, lineage-verified split, and publish the corrected corpus (v3) with the fix measured.

4. **Continuous certification for the benchmark itself (Section 7).** A release-integrity contract, contributed upstream: a deterministic stratified sample of the released bank is re-proved with the repository's own certifier on every commit, and all 242 certificates are re-proved weekly by scheduled machinery. The benchmark's datasheet can now claim not "certified at release" but "continuously re-certified, last full proof <date>" — a strictly stronger guarantee than any static release can make.

The paper's stance: certified benchmarks convert evaluation from trust-by-attention into measurement-by-proof, and the first thing a measured evaluation of small models produces is honest, receipted failure. That is a feature.

### 1.1 What this paper does not claim

Passing synthetic fixtures establishes method behavior, not world-validity; failing them establishes measured limits, not model worthlessness. The models evaluated here are small; their failures are reported as properties of a scale class under a specific instrument, with every number traceable to a published receipt [2]. Nothing here claims the benchmark's puzzles measure general reasoning; they measure certified-solution recovery, and the paper treats that distinction as load-bearing.

---

## 2. The Benchmark and Its Certificates

The benchmark [1] generates logic puzzles through a generate→encode→certify loop: language models write or encode puzzles (zebra puzzles in English, 9×9 Sudoku, 6×6 Killer Sudoku, 5×5 Futoshiki); two independent model encodings of the same text are proved equivalent with z3 (dual encoding); a SAT solver proves exactly one solution; a five-level nested deduction ladder (unit propagation → single-constraint GAC → failed-literal probing → two-level lookahead → search) grades difficulty alongside solver statistics and group-MUS explanations. The release carries 242 puzzles with certificates, metrics, explanations, and machine-readable specs, documented in a datasheet following Gebru et al.

Two properties matter for this paper. First, **uniqueness is checkable by anyone**: the certificate is not a claim but a proof artifact, re-runnable with public tools. Second, **fresh generation is reproducible**: anyone can regenerate never-published items with the same code and a new seed, avoiding training-data contamination — a property we test adversarially in Section 6.

Our engagement with the benchmark began with verification, not use: we re-certified a stratified sample of the released bank with the repository's own certifier (13/13 across all four families; MiniSat uniqueness + CP-SAT cross-check + intended-solution match; zero mismatches), then contributed the continuous-certification machinery of Section 7 upstream.

---

## 3. Evaluation Instruments

### 3.1 Exact-answer scoring

Models were evaluated under exact JSON parsing against the certified solution schema: a response counts as solved only if its answer parses to the unique certified solution. Crude substring scoring was used in an initial 12-puzzle pass and discarded as uninformative; the 48-puzzle evaluation used exact parsing throughout. The distinction matters: under crude scoring, a model that mentions the right shape of answer can appear to succeed; under exact scoring, it cannot.

### 3.2 The confabulation probes

Six probes target estate-specific apparatus rather than puzzle content: exact formula IDs, exact repository names, exact paper attributions, exact DOIs — each with a correct answer that is checkable, and an explicit abstention marker ("ABSTAIN") permitted. The scoring is binary per probe: abstain-or-correct passes; a fluent, confident, false answer is a confabulation. This instrument descends from the estate's honest-abstention program [4]: a model that will not abstain when it cannot know is a model whose successes cannot be trusted either.

### 3.3 The grounding gate

For corpus generation, a deterministic fail-closed gate [2] requires that every identifier in a generated response appear in its own source context, that the response answer or abstain explicitly, and that it terminate and not degenerate. The gate's acceptance rate is a *measurement* of the confabulation floor, not a quality score; its three-round arc is summarized in Section 4 and analyzed in full in the companion paper [5].

---

## 4. Measured Confabulation on Certified Items

### 4.1 The floor across scale

| Round | Teacher | Condition | Acceptance |
|---|---|---|---|
| 1 | 0.8B × 2 (Reasoning-v1, FreeEnergy-v1) | free generation | **0.3%** |
| 2 | 4B (Nemotron-Mini-4B-Estate-v1) | free generation | **2.7%** (4/150) |
| 3 | 4B (same) | gate-assisted (rule + allowed identifiers in prompt) | **1.3%** (2/150) |

The direction of round 3 is the finding: **stating the rule and providing the allowed identifiers made acceptance worse.** The confabulation floor at this scale is structural, not instructional [5]. For evaluation practice, the implication is direct: a small model's failure on a certified benchmark is not reliably a failure to *know* — it is substantially a failure to *ground*, and prompting cannot fix it.

### 4.2 What confabulation looks like on certified items

The failure mode is specific and instructive. Models do not decline to answer; they produce fluent, correctly-shaped apparatus: a plausible formula ID that does not exist, a plausible repository name that does not exist, a plausible paper author with a plausible journal and year. Under crude scoring these near-misses can pass; under exact scoring against a *certified* key they cannot — which is the benchmark's gift to evaluation science. Against an uncertified key, a near-miss is an argument; against a certificate, it is a measurement.

### 4.3 The exact-bytes replay discipline

An earlier evaluation artifact (a LoRA adapter, "khipu-r3") claimed abstention performance its report attributed to it. An exact-bytes re-evaluation against the six probes returned 1/6 abstained with four outright fabrications (invented benchmark certifier, invented contract license, fabricated paper author, fabricated title) — a FAIL, published verbatim with the artifact's identity [2]. The replay discipline is the point: **any claimed performance must survive re-evaluation of the exact artifact**, and the estate's receipts publish the failures at the same prominence as the successes.

---

## 5. The Three-Condition Ablation

Three 0.8B models were fine-tuned on certified-corpus derivatives: a reasoning-annotated corpus (242 examples), a free-energy-annotated corpus (242), and an ancient-mathematics corpus (24 examples, seven traditions — Liu Hui, Madhava, Egyptian, Babylonian, Greek, Andean khipu). All three were probed with the same six-probe family.

| Condition | Confabulations | Abstentions |
|---|---|---|
| Reasoning | 4/6 | 2/6 |
| FreeEnergy | **3/6** | 3/6 |
| AncientMath | 5/6 | 1/6 |

Three observations, held carefully:

1. **The free-energy annotation helps** (3/6 vs 4/6 and 5/6) — consistent with the hypothesis that training a model to recognize when it lacks sufficient information (the free-energy framing's core move) transfers to abstention [6]. The effect is one probe-family wide and we do not inflate it.
2. **The spread itself is the finding.** Three training conditions on the same corpus family, evaluated on the same probes, produce three different confabulation profiles. This is irreducible model variability in exactly the sense the riddled-basin literature predicts [3]: the conditions select different basins, and the basins disagree. The evaluation consequence is that **single-run model comparisons at this scale are noise dressed as ranking** — a conclusion the certified benchmark makes measurable because its key cannot be blamed for the variance.
3. **DPO did not push below the floor.** Two remediation attempts (a 4B DPO round and a 0.8B free-energy DPO round) returned 4/6 and 3/6 confabulations respectively — no improvement beyond the SFT floor [2]. The floor is not a preference-alignment gap.

---

## 6. The Contamination Audit

Evaluation honesty includes auditing one's own training data. The estate's frontier SFT mix (v2) was audited for group provenance: **8 of 16 validation rows shared group lineage with training rows** — a leakage that would have inflated validation performance by letting the model recognize, rather than solve, held-out items.

The correction is a **group-disjoint, lineage-verified split** (v3): validation rows are drawn from groups with zero overlap with training groups at every level of the provenance hierarchy, verified by lineage check rather than by row identity alone. The corrected corpus is published with the fix measured — the contaminated v2 validation performance and the clean v3 are both on the receipt, so the size of the leakage's effect is visible, not estimated.

This finding generalizes to the benchmark context directly: the certified benchmark's regenerability ("anyone can regenerate never-published items with a new seed") is the strong form of the same protection, and our audit is the weak-form demonstration of what goes wrong without it. The two mechanisms are complementary: regeneration protects the benchmark from pre-training contamination; lineage verification protects fine-tuning from post-training contamination.

---

## 7. Continuous Certification: A Contribution Back

A certified benchmark's guarantee is only as good as its maintenance. Certificates are proofs of the released files; any drift — a corrupted file, a mistaken edit, a toolchain change that alters the certifier — silently invalidates the claim while the badge still says certified. We contributed to the benchmark repository a **release-integrity contract**:

- **On every commit**: a deterministic stratified sample (every 20th puzzle, all four families) is re-proved with the repository's own certifier — MiniSat uniqueness, CP-SAT cross-check, intended-solution match. Fourteen tests, ~1 second.
- **Weekly, scheduled**: the **full 242-certificate bank** is re-proved with both solvers, with per-25-puzzle progress and a fail-closed list of any certificate that no longer holds.
- **Fail-closed everywhere**: a certificate that does not re-prove fails the build; there is no warning tier.

The datasheet upgrade this enables: *"continuously re-certified (last full proof: <date>)"* — a strictly stronger claim than any static release can make, and one that converts the benchmark's central property from an event (a release-time proof) into a standing invariant (a machine-checked schedule). The same discipline transfers to the models: the estate's evaluation receipts are published at measurement time, win or lose, which is the model-side analogue of a benchmark that re-proves itself.

---

## 8. What the Failures Teach About Evaluation

Four lessons, each measured:

1. **Certified keys change the epistemics of failure.** Against an uncertified key, a model's near-miss is disputable; against a certificate, it is data. Every confabulation rate in this paper is a measurement precisely because the benchmark's answers are proofs.
2. **Grounding, not knowledge, is the small-model bottleneck.** The gate-assisted round is the controlled evidence: the models fabricate *with the allowed identifiers in front of them*. Evaluation instruments for small models must therefore measure grounding explicitly — the abstention probe is as important as the accuracy score.
3. **Condition-level variance is real and must be reported.** The 3/6–4/6–5/6 spread across training conditions is a single-family instance of a fundamental geometry [3]. Single-run rankings at this scale are not evidence; multi-condition spreads with receipts are.
4. **Evaluation pipelines need their own certification.** Our contamination audit found our own validation split leaking; the continuous-certification contribution is the same discipline pointed at the benchmark. The instruments measure, and the instruments are measured.

---

## 9. Limitations

**Scale.** All model results are 0.8B–4B on single-node hardware. The confabulation floor is measured for this scale class; frontier behavior is an open empirical question the estate has not paid to answer.

**Probe breadth.** The six-probe family is narrow and estate-specific; the abstention findings are about grounding apparatus, not about the puzzles themselves. Exact-answer puzzle-solving rates for the fleet are low and reported in the receipts; we do not generalize from them to reasoning ability in either direction.

**Ablation width.** One probe family, three conditions, single runs. The spread is reported as an observation consistent with [3], not as a powered estimate of condition effects.

**The contamination audit is one corpus.** The v2→v3 fix is measured for this corpus; the method (group-disjoint lineage verification) is the contribution, not a universal contamination rate.

**The continuous-certification contribution is pending full adoption upstream.** The machinery is contributed and tested; the benchmark's owner retains review, as is right.

---

## 10. Conclusion

A certified benchmark is an instrument that cannot be argued with, only measured against. Pointed at a fleet of small models, it produced this paper's every finding: a structural confabulation floor that prompting worsens rather than repairs; condition-level variability consistent with riddled basin geometry; a contamination leak in our own pipeline, found and fixed with the fix measured; and a standing contribution that makes the benchmark re-prove itself forever. None of these results flatters the models. All of them, we submit, is what evaluation is for — and the certified benchmark is what makes the telling honest.

---

## References

[1] Behnamian, S. (2026). Puzzle generation with guaranteed uniqueness: certified unique-solution puzzles generated by language models. https://github.com/sarabehnamian/Puzzle-generation-with-guaranteed-uniqueness

[2] SZL Holdings (2026). Model evaluation receipts, published verbatim at measurement time. Hugging Face dataset: SZLHOLDINGS/model-eval-receipts. Includes the three-round grounding-gate arc, the khipu-r3 exact-bytes FAIL, and the three-condition ablation.

[3] Ly, A., & Gong, P. (2026). Fractal basin geometry and the limits to predictability and reproducibility in deep learning. *Nature Machine Intelligence*. arXiv:2510.05606.

[4] Lutar, S. P. Jr. (2026). Honest Abstention Transfer in Small-Corpus Supervised Fine-Tuning: Measured Refusals, Not Invented Scores. Zenodo, concept DOI 10.5281/zenodo.24025916.

[5] Lutar, S. P. Jr. (2026). Basin-Insensitive Reliability: When Riddled Geometry Makes Reproducibility Unattainable, Certification Is the Correct Instrument. Companion preprint.

[6] Lutar, S. P. Jr. (2026). The Free-Energy Certification: PAC-Bayes Bounds as Governed AI Admission Criteria. Zenodo, concept DOI 10.5281/zenodo.24025918.

---

## Appendix A. The continuously-certified contract

```
on: push, pull_request, schedule (weekly)
jobs:
  tests:        # every commit
    pytest -q   # 17 unit tests + 14 release-certificate re-proofs
                # (stratified sample: every 20th puzzle, all families)
  full-recertification:  # weekly, scheduled
    re-prove ALL 242 certificates with the repository's own certifier
    (MiniSat uniqueness + CP-SAT cross-check + intended-solution match)
    fail-closed: any certificate that does not re-prove fails the build
```

## Appendix B. Receipt index

| Measurement | Result | Verdict |
|---|---|---|
| Released-bank sample re-certification | 13/13 across all four families | Certificates hold |
| Grounding gate, 0.8B teachers (free) | 0.3% acceptance | Floor measured |
| Grounding gate, 4B teacher (free) | 2.7% (4/150) | Floor measured |
| Grounding gate, 4B (gate-assisted) | **1.3% (2/150)** | Assistance made it worse |
| khipu-r3 exact-bytes probes | 1/6 abstained, 4 fabrications | FAIL, published |
| Three-condition ablation | 4/6, 3/6, 5/6 confabulations | Spread is the finding |
| DPO remediation ×2 | 4/6, 3/6 | No improvement over SFT floor |
| Contamination audit (v2 validation) | 8/16 group-overlapping rows | Found; fixed with group-disjoint v3 |
