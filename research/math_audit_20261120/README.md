# Mathematical audit evolution: model-error and coverage falsification

**SOURCE-ONLY RESEARCH. NOT an arXiv submission, Lean certificate, signed attestation, trained-model result, or authorization to deploy, merge or trade.**

This folder contains a standalone arithmetic appendix for the evolved 30-page SZL mathematical working preprint (20 November 2026). It checks the exact inequalities and conditional sampling formulas without needing cloud APIs or model inference.

## A real model-review error

On 20 November, the authorized BETTERWITHAGE Ollama local model
ministral-3:3b returned a mathematically reversed equivalence:

- INCORRECT: epsilon^(1/n) >= t  iff  epsilon <= t^n
- CORRECT: epsilon^(1/n) >= t  iff  epsilon >= t^n

For epsilon = 1/100, threshold t = 7/10, n = 13:
t^13 = 96889010407 / 10000000000000 = 0.0096889010407,
which is less than epsilon = 0.01; thus G_13 = 0.701703828670... > 0.70.
At n = 12 the gate does not reach 0.70. For fixed 0<epsilon<t<1,
the strict condition holds at every integer n > log(epsilon)/log(t).
The source does NOT infer that any source AI reviewer is independently verified.
Kimi K3.1 Pro Cloud returned only an acknowledgement or noncompleted analysis
on this question. We therefore do not claim AI consensus or model approval.

The signed-or-hashed appearance of a generated answer cannot replace an
independent arithmetic counterexample. A thresholded mean cannot replace a
mandatory action-authority veto.

## Audit population coverage is a mathematical claim

An authenticated GitHub organization metadata census at
2026-11-20T05:24:33Z counted 182 accessible repositories, 153 active and
29 archived, with 5 private. A GitHub Search query at 05:29:58Z returned
66 open PRs. These are metadata observations, NOT 182 code/security audits.

Given B hypothetical bad repositories in a universe of N, a uniformly
random size-n sample without replacement misses every bad repo with
probability C(N-B,n)/C(N,n), or zero if n > N-B.
At N=182, B=15, n=30 the probability is approximately 0.059434905875.
Thus 0 defects in 30 samples would not rule out B=15 at the 5% level
under those conditional assumptions. B=15 is hypothetical, not a finding.

If each of ten independent passes samples 20 of the 182 repos uniformly,
the expected distinct coverage is N*[1-(1-20/N)^10] = 125.1791595, not
182. Repeating the exact same 20 covers just 20. A complete audit requires
an explicit 182/182 manifest with source SHA and measured per-repo state.

## Proof claims remain scoped

The current Lutar A1-A5 axioms admit geometric, arithmetic and maximum
aggregators. At x=(1/4,1), their values are 1/2, 5/8 and 1.
Unconditional uniqueness is false; conditional uniqueness requires more
assumptions. Source PR lutar-lean#386 removes false uniqueness prose,
with all 20 GitHub workflows green at reviewed head but still independent
review-gated. A second draft PR #387 overlaps the inventory-note edit.
Coordinate rather than merge duplicate notes blindly.

The historical locked v11 proof counts 749/14/163 and a later source
lexical inventory 1410 declarations / 25 unique axiom names / 251
non-comment sorry occurrences are not the same scope. The repaired
n-axis Pinsker theorem retains probability-simplex hypotheses; it
cannot silently authorize an older unrestricted DPO axiom.
Eight formula identifiers do not mean eight end-to-end runtime
implementation proofs. The Lean-to-Python mapping is still unverified.

## Reproduce locally (standard library only)

    python -B -m unittest discover -s research/math_audit_20261120 -p test_arithmetic.py -v
    python -B research/math_audit_20261120/arithmetic.py

The output is a non-authorizing SOURCE_ONLY report. A passing test is
not a proof term, signed artifact, provider settlement or training admission.

## Conceptual research inputs; no copied implementations

Lean official proof validation: https://lean-lang.org/doc/reference/latest/ValidatingProofs/
Math Commons formalization assurance: https://github.com/math-commons/formalization-assurance
Google DeepMind AlphaProof Code on Signal (2026-11-10): https://deepmind.google/documents/36/Formal_Verification_of_Signal_4.pdf
ICML 2026 SWE-ABS adversarial tests: https://proceedings.mlr.press/v306/yu26b.html
Google SRE Canarying Releases: https://sre.google/workbook/canarying-releases/

Next steps require independent theorem/axiom checks, an immutable 182/182
repo manifest, heldout evaluations and tests, required GitHub reviews,
GitHub/HF runtime parity, true x402 settlement, per-wheel PyPI attestation
verification and authenticated Snowflake/database readback.
