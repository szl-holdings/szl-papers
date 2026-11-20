# Curated global open-source methods → SZL transferable frontier (2026-11-20)

**Status: public-research proposal / not admitted / no code copied / no training or release.** This is a finite sample of **17** public upstream repositories across software agents, evaluation, retrieval, robotics, GPU training, supply-chain provenance and payments. It is *not* a scrape of the entire world, a full upstream security scan, a benchmark reproduction or an audit of every SZL repository. The exact machine-readable GitHub commit/license observations and six unmeasured hypotheses are in [oss-global-source-pins-20261120.json](oss-global-source-pins-20261120.json).

**Source ownership and non-duplication.** [Existing frontier intake #90](https://github.com/szl-holdings/szl-papers/pull/90) already mapped seven outside methods to SZL. [Embodied Passport #92](https://github.com/szl-holdings/szl-papers/pull/92) owns the actual robotics study. This addendum focuses on **immutable open-source code references, explicit rights separation, source-owner routing and negative-controlled commercial hypotheses**; it starts no other controller, GPU job or pipeline writer.

## First-party public source / license metadata observations

Each repository was checked with configured GitHub CLI metadata and an exact default-branch commit readback from BETTERWITHAGE on **2026-11-20 UTC**. SPDX strings are **GitHub's repository metadata**, not a checked license for each file, dependency or asset. Some projects release source code under permissive terms but their model weights and datasets have different licenses. All asset rights remain **UNASSESSED** and no upstream bytes were imported.

| Repository / study link | Immutable source | GitHub SPDX metadata | Transferable hypothesis → SZL owner |
| --- | --- | --- | --- |
| [OpenHands/OpenHands](https://arxiv.org/abs/2407.16741) | [`428b3dc2a0e8`](https://github.com/OpenHands/OpenHands/commit/428b3dc2a0e8d3d0f689a909e2607e33d973da76) | `MIT` | agent sandbox isolation → `szl-mesh` |
| [SWE-agent/SWE-agent](https://arxiv.org/abs/2405.15793) | [`3ea751c087f3`](https://github.com/SWE-agent/SWE-agent/commit/3ea751c087f32b16e039a2233dd6eefecef325d5) | `MIT` | agent-computer interface → `szl-ci-witness` |
| [huggingface/lerobot](https://github.com/huggingface/lerobot) | [`83883ae60a8e`](https://github.com/huggingface/lerobot/commit/83883ae60a8e1682552b6853e4170c74d83a4525) | `Apache-2.0` | robotics dataset and sim eval → `szl-papers` |
| [NVIDIA/Isaac-GR00T](https://arxiv.org/abs/2503.14734) | [`708617f5716c`](https://github.com/NVIDIA/Isaac-GR00T/commit/708617f5716c63fc0a327391492ea2b91977ae90) | `Apache-2.0` | VLA policy validation; weights separately licensed → `szl-papers` |
| [openvla/openvla](https://github.com/openvla/openvla) | [`c8f03f48af69`](https://github.com/openvla/openvla/commit/c8f03f48af692657d3060c19588038c7220e9af9) | `MIT` | open VLA method baseline → `killinchu` |
| [EleutherAI/lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness) | [`d6de81643928`](https://github.com/EleutherAI/lm-evaluation-harness/commit/d6de81643928d653435c431bae19945d41d32520) | `MIT` | model evaluation task provenance → `szl-crosscheck` |
| [pytorch/torchtitan](https://github.com/pytorch/torchtitan) | [`c387dd46e5df`](https://github.com/pytorch/torchtitan/commit/c387dd46e5df93401d08e725d83ad8f2d87622a8) | `BSD-3-Clause` | training resume state accounting → `szl-gpu-bridge` |
| [stanford-futuredata/ColBERT](https://arxiv.org/abs/2112.01488) | [`cc4f3dc91c0b`](https://github.com/stanford-futuredata/ColBERT/commit/cc4f3dc91c0b45d2d08c251d9d95178285c65f1c) | `MIT` | late interaction retrieval → `szl-retrieval-bench` |
| [open-telemetry/opentelemetry-python](https://opentelemetry.io/docs/specs/semconv/gen-ai/) | [`70c6f2a9d5bc`](https://github.com/open-telemetry/opentelemetry-python/commit/70c6f2a9d5bcee0062a383e18f5d7c02334bff9d) | `Apache-2.0` | privacy-safe GenAI tracing → `vsp-otel` |
| [sigstore/cosign](https://docs.sigstore.dev/cosign/) | [`339a3ca85413`](https://github.com/sigstore/cosign/commit/339a3ca85413b4d89a49daf1eb554591c93ee365) | `Apache-2.0` | artifact signature verification → `szl-receipt` |
| [coinbase/x402](https://developers.cloudflare.com/agents/tools/payments/x402/) | [`0e6e8c55d86b`](https://github.com/coinbase/x402/commit/0e6e8c55d86b4f14234fb6e49a4052074fb93e57) | `Apache-2.0` | verified payment settlement → `a11oy` |
| [open-policy-agent/opa](https://www.openpolicyagent.org/docs) | [`a4d2f0c0f149`](https://github.com/open-policy-agent/opa/commit/a4d2f0c0f14977ec8b527da7d248d0ad27e1906c) | `Apache-2.0` | policy deny before tool effect → `hatun-mcp` |
| [deepseek-ai/DeepGEMM](https://github.com/deepseek-ai/DeepGEMM) | [`5081f8513af5`](https://github.com/deepseek-ai/DeepGEMM/commit/5081f8513af57e61696de4f4f04b0e707ffb503e) | `MIT` | SM90/SM100 kernel incompatibility warning for SM86 → `szl-kernels` |
| [QwenLM/Qwen3](https://github.com/QwenLM/Qwen3) | [`7a2f61ffc7a2`](https://github.com/QwenLM/Qwen3/commit/7a2f61ffc7a20d47efcd2bf97f6f2bf52729042e) | `NOASSERTION` | hybrid reasoning; repo license metadata absent → `szl-serve` |
| [NAVER-Cloud-HyperCLOVA-X/OmniServe](https://github.com/NAVER-Cloud-HyperCLOVA-X/OmniServe) | [`ae0d33fe6177`](https://github.com/NAVER-Cloud-HyperCLOVA-X/OmniServe/commit/ae0d33fe61773e099b5c221afed4bc23949181ed) | `Apache-2.0` | multimodal encoder/decoder separation → `killinchu` |
| [mistralai/mistral-vibe](https://github.com/mistralai/mistral-vibe) | [`63dab302305c`](https://github.com/mistralai/mistral-vibe/commit/63dab302305c80131ea1e5b1c3cb18c2a4fd96d3) | `Apache-2.0` | bounded tool approvals → `szl-mesh` |
| [MoonshotAI/kimi-code](https://github.com/MoonshotAI/kimi-code) | [`094771711c4d`](https://github.com/MoonshotAI/kimi-code/commit/094771711c4d82b42c579936bc2daa7b1ae1040c) | `MIT` | context-isolated coding subagents → `szl-mesh` |

**Important rights/hardware distinctions.** NVIDIA GR00T labels its **code Apache-2.0** but **model weights under NVIDIA Open Model License**: do not treat those as the same asset. LeRobot datasets and OpenVLA model weights each require asset-specific provenance, consent/use-rights and dataset notices. The GitHub API returned **no repository-level SPDX value** for Qwen3 (`NOASSERTION` in this survey); its model-family license statements do not cure that specific source/data gap. MIT, Apache-2.0 and BSD-3-Clause code can often be used commercially with obligations, but legal review must consider the actual files, NOTICE/copyright, patents, trademarks, model cards and transitive dependencies. A Git SHA or source hash proves identity only, never permission.

DeepGEMM's documented kernels require **SM90/SM100**. The historical SZL RTX A6000 is **SM86**; transferring reported DeepGEMM throughput or trying unsupported kernels on that node would be misleading. Keep hardware and budget admission separate.

## Six falsifiable, commercially relevant but unmeasured studies

Every row below requires a rights review, the real implementation repository owner, independent evaluation and an exact source/metric/denominator plan. A negative control is not evidence that an experiment actually ran. Existing runtime, training and release authorities retain control.

| Experiment | Existing SZL owners | Primary declared metric and denominator | Required falsifying control |
| --- | --- | --- | --- |
| `AGENT-RECEIPT` | `szl-mesh`, `szl-crosscheck`, `szl-receipt`, `a11oy` | false billable accepts (cases); denominator: all preregistered synthetic agent-run fixtures including failed, missing and replayed | self-signed agent success with independent evaluator refusal must stay non-billable |
| `RETRIEVAL` | `szl-retrieval-bench`, `szl-second-brain` | ndcg at 10 (fraction); denominator: all preregistered qrels-covered queries including failures | stale or cross-tenant citation forces abstention |
| `SIM-ROBOTICS` | `szl-papers`, `killinchu` | critical simulated violations (episodes); denominator: all preregistered simulation episodes and invalid outcomes | zero simulated failures is not approval for robot actuation |
| `CHECKPOINT` | `szl-gpu-bridge`, `szl-quant-witness` | resumes with complete evidence (runs); denominator: all preregistered interruption and attempted recovery runs | weights-only without optimizer or RNG cannot qualify resumed training |
| `MULTIMODAL` | `a11oy`, `killinchu`, `szl-serve` | capabilities with exact runtime binding (claims); denominator: all preregistered user-visible capability claims including unavailable | HTTP 200 without expected tokenizer or model revision is not live inference |
| `HARDWARE` | `szl-kernels`, `szl-engine-bench` | compatible kernel candidates (cases); denominator: all preregistered kernel and actual compute-capability pairs | SM90-only kernel on the RTX A6000 SM86 remains INCOMPATIBLE |

**Priority order:** (1) offline receipt/billability false-positive audit; (2) retrieval evidence/citation and tenant isolation; (3) GPU compatibility rejection without paid compute; (4) checkpoint resume-integrity proof; (5) model/encoder/decoder source coherence; (6) simulation-only embodied evidence in [its existing owner PR #92](https://github.com/szl-holdings/szl-papers/pull/92). These priorities are engineering hypotheses, not measured market demand.

## Which leaders and ideas deserve independent reproduction?

**Agent coding and peer review.** [John Yang et al., SWE-agent](https://arxiv.org/abs/2405.15793) makes the agent-computer interface an explicit experimental variable. [Xingyao Wang et al., OpenHands](https://arxiv.org/abs/2407.16741) investigates executable and isolated agent environments. [Moonshot Kimi Code CLI](https://github.com/MoonshotAI/kimi-code) uses context-isolated coding subagents; [Mistral Vibe](https://github.com/mistralai/mistral-vibe) documents concise tool/approval interfaces. SZL's original experiment must separate the proposer from evaluator, count **all** tried candidates (including failures) and reject self-grading despite two models agreeing. Model output and green source CI are advisory, not release signatures.

**Retrieval and independent quality.** [ColBERTv2](https://aclanthology.org/2022.naacl-main.272/) and [PLAID](https://arxiv.org/abs/2205.09707) propose token-level late interaction and efficient filtering. Author-reported latency/quality must be remeasured against matched SZL BM25/hybrid baselines, identical qrels/corpus version, hardware and p95 latency. An unavailable or tenant-leaking citation remains a HOLD rather than an embellished model card.

**Training integrity.** [TorchTitan](https://github.com/pytorch/torchtitan) provides reusable methodological lessons about training-state and elasticity, while [EleutherAI lm-eval](https://github.com/EleutherAI/lm-evaluation-harness) provides benchmark task/version accounting. Nothing here authorizes a trainer restart, a new GRPO lane, checkpoint deserialization or claims that a final filename proves completion.

**Multimodal and physical AI.** [NAVER OmniServe](https://github.com/NAVER-Cloud-HyperCLOVA-X/OmniServe), [NVIDIA GR00T](https://github.com/NVIDIA/Isaac-GR00T), [LeRobot](https://github.com/huggingface/lerobot) and [OpenVLA](https://github.com/openvla/openvla) motivate split capability receipts and simulation-only comparisons. Simulation success does *not* establish physical robot safety, dataset rights or commercial hardware readiness.

**Receipts, observability and payment.** [Sigstore Cosign](https://github.com/sigstore/cosign) motivates independent signature verification; [OPA](https://github.com/open-policy-agent/opa) motivates deny-before-action; [OTel GenAI](https://opentelemetry.io/docs/specs/semconv/gen-ai/) motivates bounded tool-call spans with **no private prompts/secrets**; and [Cloudflare's x402 description](https://developers.cloudflare.com/agents/tools/payments/x402/) distinguishes a payment challenge from verified settlement. Source integrity, semantic correctness, runtime readback and actual revenue remain separate gates.

## Actual Kimi × Mistral peer-study outcomes

Kimi's **2026-11-20** cloud Ollama review of a sanitized public-source summary proposed an original **independently verified agent-run evidence and billability seam**: compare signed/unsigned, forged and replayed receipts against predeclared offline fixtures, using *all* attempts as the denominator and separating payment settlement from the agent's own success claims. **This was a proposal only**; no harness/receipt/billing experiment has been run or admitted. The attempted Mistral-large cloud reply to that proposal was **empty**, so it is **not counted as an independent review of this final proposal**. Earlier Mistral advice warned against circular signer validation, which remains a concrete negative control—not a signature or approval.

## High-reliability consumer launch contract

Use the established source-owning paths and a [Google SRE launch checklist](https://sre.google/sre-book/launch-checklist/) approach: maintain exact source and rights; freeze hidden negatives and denominators before candidates; require independent evaluator and security tests; verify deployment provenance, canary/rollback/health, backups and served revision independently; then test customer checkout, entitlement and actual x402 settlement. A beautiful 3D visual must show **UNAVAILABLE** when the actual model binding, live metric or permission is missing. A GitHub PR or static card alone is not product readiness.

**Prohibited by this source study:** cloning unknown-license weights or datasets; rebranding upstream work as solely ours; weakening CI/protections; using credentials or training data in model prompts; installing unsupported kernels; spending GPUs; using synthetic test success as a revenue, accuracy, formal theorem or safety claim. Commercial transfer only occurs following rights and independent release admission.
