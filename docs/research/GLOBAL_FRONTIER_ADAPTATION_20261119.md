# Global frontier methods -> SZL falsifiable integration matrix (2026-11-19)

**Status: research proposal / source-only / non-normative.** No weights, services,
datasets, checkpoints, model inference, agent actions, training, deployment,
publication, legal conclusion, or proof promotion are authorized by this file.
The v26/P3 hold, Flagship54, sole-dispatcher constraint, and locked Lean registry
remain unchanged. This is not a reproduction of any outside paper.

## Purpose and original question

Can the SZL proof-carrying organ fabric improve **quality at fixed resources**
without converting a passing software test or a purported model answer into
unearned training, mathematical, licensing, or production authority?

Use the existing owners, rather than creating a parallel control plane:

- [szl-mesh](https://github.com/szl-holdings/szl-mesh) for bounded
  proposal-only organ packets;
- [szl-formulas](https://github.com/szl-holdings/szl-formulas) and
  [szl-invariants](https://github.com/szl-holdings/szl-invariants) for
  independently testable Python math/runtime checks;
- [lutar-lean](https://github.com/szl-holdings/lutar-lean) for pinned Lean
  declarations and kernel-replayed proof evidence;
- [szl-gpu-bridge](https://github.com/szl-holdings/szl-gpu-bridge) for the
  existing signed-dispatch/trainer/evidence gates, **only after owner admission**;
- [szl-forge](https://github.com/szl-holdings/szl-forge),
  [szl-receipt](https://github.com/szl-holdings/szl-receipt) and
  [vsp-otel](https://github.com/szl-holdings/vsp-otel) for controls, receipt
  verification and trace links;
- A11oy / Hugging Face / Cloudflare for **separately verified** served bytes,
  functionality and publication, never inferred from source CI.

## Primary technical prior art (study without silently copying)

| Jurisdiction | Primary paper / source | Transferable question | Compatibility and evidence constraint |
| --- | --- | --- | --- |
| China: DeepSeek | [DeepSeek-V3](https://github.com/deepseek-ai/DeepSeek-V3) (MoE/MLA, FP8 co-design, load balancing) | Can pinned local routing/batching improve tokens/sec and quality per unit energy? | Training claims belong to the original researchers. Reproduce only on a compatible, authorized pool with an independent energy meter and held-out tests. |
| China: DeepSeek | [DeepGEMM](https://github.com/deepseek-ai/DeepGEMM) (FP8/FP4/BF16 GPU kernels) | Which shapes and kernels outperform the SZL baseline? | Current upstream lists **SM90/SM100**. The RTX A6000 is **Ampere SM86**; do not install or report DeepGEMM acceleration on that node. Hardware capability check must precede any benchmark. |
| China: Alibaba Qwen | [Qwen3-Next technical article](https://qwen.ai/blog?id=qwen3-next) (sparse MoE, hybrid attention, multi-token prediction) | Does sparse routing or a compact reference improve held-out throughput/accuracy? | Published performance and training cost are authors' results, **not** SZL measurements; inspect model/code license and actual supported inference backend. |
| Ireland: Lero/AIware, University of Limerick | [SWE-ABS paper, ICML 2026](https://proceedings.mlr.press/v306/yu26b.html), [code](https://github.com/OpenAgentEval/SWE-ABS) | Can coverage- and mutation-strengthened hidden tests falsify apparently passing A11oy/agent PRs? | On original benchmark, authors rejected **19.78%** of previously passing patches. This is a research result, **not** an SZL measured rejection rate. Isolate test data and pinned mutants. |
| Ireland: Trinity/ADAPT | [W3C Data Privacy Vocabulary v2.3](https://w3c.github.io/dpv/2.3/dpv/), [repository](https://github.com/w3c/dpv) | Can source/data-purpose/rights/retention context travel with Khipu evidence handles? | DPV vocabularies assist semantic documentation; they do not prove legal compliance, consent, or data rights. |
| South Korea: NAVER Cloud | [OmniServe](https://github.com/NAVER-Cloud-HyperCLOVA-X/OmniServe), [HyperCLOVAX-SEED-Think-32B card](https://huggingface.co/naver-hyperclovax/HyperCLOVAX-SEED-Think-32B) | Can the Anatomy multimodal path separate encoder, reasoning, and decoder evidence with API-compatible traces? | OmniServe code says Apache-2.0. Model weights/license/quality/VRAM requirements are separately gated; do not assume 32B fits laptop VRAM. |
| South Korea: LG AI Research | [EXAONE 4.0 research code/card](https://github.com/LG-AI-EXAONE/EXAONE-4.0), [paper arXiv:2507.11407](https://arxiv.org/abs/2507.11407) | Evaluate hybrid local/global attention and reasoning-mode switching as **methods**. | The published EXAONE 4.0 model license is **NC and restricts competing-model development**. Commercial weights use and derivative-training rights are **not admitted** without a separate rights decision. |

The list is selected by actionable code/paper evidence, not a comprehensive
ranking of countries or researchers. The separate
[ancient mathematics source ledger](ANCIENT_MATH_SOURCE_LEDGER_20261118.md)
already bounds khipu arithmetic, Rhind proportional methods, Euclidean GCD,
Babylonian sexagesimal and the Maya Dresden codex; none automatically
translates into historical decipherment, training rights or new physics.

## Proposed proof-carrying comparative experiment

**Registration before experiments:** freeze a baseline source revision; one
unmodified external method; one independently implemented SZL adaptation; exact
hardware SKU/compute capability; model+dataset IDs and immutable revisions;
access/licensing approval; eval harness revision; intended metrics and thresholds;
held-out partition; seed list; compute cost ceiling; abort/rollback; authorized
owner. No test run may be silently added after reading outcomes.

**Three isolation lanes:**

1. **Inference efficiency (China):** identical public-rights model, prompt set,
   seeds, output budget, hardware, batch shapes and precision. Log actual
   TTFT, tokens/sec, peak allocated VRAM, power/energy if metered, OOM/failure
   denominator, and response equivalence. Compare compatible kernels against
   the baseline. Ampere gets an independent BF16/TF32-compatible candidate,
   **not a DeepGEMM SM90 binary**.
2. **Adversarial reliability (Ireland):** run known-good behavior,
   systematic coverage-guided negatives, and seeded mutants of the code/receipt
   evaluator. Log `valid_mutants`, `killed_mutants`, unchanged tests, skipped
   cases, contamination checks and failure examples. A weak green test suite
   cannot qualify code. Mutants are data, not source changes on protected main.
3. **Multimodal + rights (Korea/Ireland):** split text/vision/audio capability
   claims from what was actually tested. Require licensed fixtures, held-out
   answer checks, tool-call policy behavior, source revision, endpoint served
   revision, and rights/purpose/provenance metadata. No unlicensed model use.

**Required exact denominators:** define per-lane `N_attempted`,
`N_valid`, `N_failed`, `N_skipped`, `N_unavailable`, and a SHA-256 fixture
digest. A zero valid denominator or missing baseline result is **UNAVAILABLE**.
Do not hide skipped cases from either result accounting or front-end display.

**Falsifiable measurements**, without inventing empirical outcomes:

```text
mutation_survival = valid_mutants_not_killed / valid_mutants
mutation_kill_rate = killed_valid_mutants / valid_mutants
energy_per_valid_answer = measured_energy_j / independently_valid_answers
quality_delta = heldout_accuracy(candidate) - heldout_accuracy(baseline)
rate_ratio = observed_tokens_per_sec(candidate) / observed_tokens_per_sec(baseline)
```

Each fraction is **UNAVAILABLE** if its denominator is zero, unobserved or
identity-mismatched. An energy figure without a same-run meter is unavailable,
not zero. The real current runtime is not assumed to have this data.

**No scalar can launder a failed mandatory gate.** Let the independent necessary
evidence predicates be `G_source`, `G_rights`, `G_owner`,
`G_eval`, `G_signer`, `G_served`, `G_budget`, `G_rollback`.
If any is FAIL, the proposal is HOLD; if any is UNOBSERVED and none fail, it
is UNOBSERVED. Even all observational predicates passing is only a
**review candidate**, never self-authorized dispatch.

For diagnostics only, the SZL aggregate
`Lambda_k(x) = (product_i x_i) ** (1/k)` may summarize fully observed,
appropriately normalized positive measurements in a fixed test scope. It is
**not** a proof of causal improvement, a substitute for distinct hard gates,
or unconditional uniqueness. The unconditional Λ uniqueness statement was
refuted; only the separately pinned **conditional** Lean theorem can be
described as proved. Keep the locked-eight and 21 formula API identities distinct:
[MATH_RUNTIME_EXECUTION_MATRIX](../../MATH_RUNTIME_EXECUTION_MATRIX.md).

## Proposed receipt shape (new proposal only)

```text
schema=szl.frontier-comparison.proposal/v0
source_sha, baseline_sha, external_source_url, external_revision
model_revision, dataset_revision, fixture_sha256, rights_verdict
hardware_sku, compute_capability, training_owner_status
eval_code_revision, test_type, sample_counts, seeds
measured_results_or_UNAVAILABLE, errors, skipped_denominator
proof_status_tier, lean_revision, formula_id, invariant_ids
khipu_ledger_digest, trace_id, signer_status, served_byte_readback
cost_budget_verdict, decision=HOLD|UNOBSERVED|REVIEW
```

A local hash establishes packet-byte integrity **only**. The schema is a
discussion artifact, not a deployed authority, signature, finalized receipt
type, promoted proof, or signed queue schema.

## Entry / exit controls and source owners

- [ ] **Prerequisite HOLD:** resolve the existing
  [GPU bridge owner issue #260](https://github.com/szl-holdings/szl-gpu-bridge/issues/260),
  prove a sole authenticated dispatcher and re-run source-matched storage
  preflight. A workstation may have >50 GiB free yet have zero authorized
  dispatch owners. No new watcher, lease, task or trainer may be installed
  based on a green CI badge.
- [ ] Confirm hardware/toolchain compatibility, compute budget, dataset rights
  and EXAONE-style model restrictions **before** any download or experiment.
- [ ] Implement **source-only, CPU, offline synthetic controls** in the
  appropriate owner repo with failing mutation cases and no production writes.
  Require CI tests that demonstrate each mandatory gate can actually reject.
- [ ] Run separately authorized measured A/B trials; provide immutable
  paired results with uncertainty and both successful and failed denominators.
- [ ] Obtain independent Lean/readback, signature, source and served-byte
  verification where claims require them; run negative tests that mutate each
  field and confirm `HOLD`.
- [ ] Leave the pre-existing v26/P3 publication, GitHub protections,
  Flagship54 completion, Salad paid scale, and cloud monetization boundaries
  unchanged until their separate owner approvals.

**Current status:** source citations and a test protocol only; **0** new model
training trials, **0** GPU benchmark comparisons, **0** empirically validated
SZL improvement claims, **0** authority promotions. Future PRs belong to the
actual owner repositories and need independent proof and runtime verification.
