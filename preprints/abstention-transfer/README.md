# Honest Abstention Transfer in Small-Corpus SFT: Measured Refusals and Confabulations in a 4B Estate-Tuned Model

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](LICENSE)

**DOI:** [10.5281/zenodo.24025916](https://doi.org/10.5281/zenodo.24025916) — published on Zenodo, 2026-11-06.

Preprint P4 — **not peer reviewed**. The paper is [`main.md`](main.md).

**One-line summary:** small-corpus SFT on a 4B model transfers refusal for unmeasured
*values* but not for unmeasured *citations* — both behaviors are published verbatim,
and the measured failures become the DPO counterweight's preference pairs.

**Measured claims (all receipted, verbatim):**
- Correct abstention: refuses to fabricate AUM/customer counts with anti-fabrication doctrine
- Measured failure: confabulated citations ("Per the canonical thesis (v8), section 'GPU
  utilization on node 2'") for sections that do not exist
- The refusal/confabulation asymmetry appears across the 4-model trained family
- Eval-driven counterweight protocol defined from the failures themselves

**Receipts:** `SZLHOLDINGS/model-eval-receipts` → `fleet-eval-2026-11-05.json` and the
doctrine-abstention evaluations. Model: `SZLHOLDINGS/SZL-Nemotron-Mini-4B-Estate-v1`.

**Deposit route:** the per-paper `.zenodo.json` is local metadata only.
GitHub–Zenodo reads the repository-root `.zenodo.json`, which stays
reference-only and must not be minted as this paper (see root
`ZENODO_DEPOSIT_POLICY.md`). Do not cut a release to auto-mint `p4-v1.0.0`
onto the shared concept. DOI sync searches for this preprint's own title and
does not record any other deposit as its DOI.
