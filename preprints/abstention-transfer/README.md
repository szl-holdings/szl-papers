# Honest Abstention Transfer in Small-Corpus SFT: Measured Refusals and Confabulations in a 4B Estate-Tuned Model

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](LICENSE)

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

**DOI:** reserved via GitHub release Zenodo auto-mint (`.zenodo.json` included).
Tag a release `p4-v1.0.0` to mint the concept DOI; never reuse the Ouroboros
umbrella concept (see root `ZENODO_DEPOSIT_POLICY.md`).
