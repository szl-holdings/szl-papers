# Global Frontier: Research-to-Experiment Contract (2026-11-19)

**Status:** SOURCE-ONLY / PROPOSED / NON-NORMATIVE. This is a reviewed-source research plan, **not** a benchmark result, a training run, an independent mathematical proof, an accepted deployment, a model-card qualification, a new v26 thesis version, or authorization to spend money. It is deliberately separate from the protected training observer, the Flagship54 shutdown guard, and the source-owned publication gates.

**Research question.** Can SZL combine verifiable-reward post-training, fully reproducible multilingual/synthetic-data practices, and software-engineering assurance with SZL's existing proof/receipt substrate to improve *measured, calibrated problem solving* while reducing false claims and unrecoverable runs? The null hypothesis for every intervention is **no improvement over the matched baseline**.

## Primary research targets (a selective review, not a world census)

| Research lineage | First-party code/paper anchor | Technique worth testing | SZL-specific limitation |
| --- | --- | --- | --- |
| **China — DeepSeek / verl** | [DeepSeek-V3](https://github.com/deepseek-ai/DeepSeek-V3), [DeepSeek-R1](https://github.com/deepseek-ai/DeepSeek-R1), [verl / HybridFlow](https://github.com/verl-project/verl) | Multi-head latent attention/MoE efficiency, verifiable-reward RL and GRPO-style group comparisons, DAPO recipes | Published large-scale training results do not transfer to SZL's hardware, data or adapters; first validate reward correctness and resumability on a *separately approved* small run |
| **China — Moonshot AI** | [Kimi-K2 and technical report](https://github.com/MoonshotAI/Kimi-K2) | MuonClip stability hypotheses and synthetic tool-use trajectories with verifiable tasks | Must isolate optimizer effects from dataset, inference, hardware, token count and evaluator differences; never copy unavailable private trajectories |
| **South Korea — KAIST / KORMo** | [KORMo research and open assets](https://kaist-mlplab.github.io/kormo/), [paper](https://arxiv.org/abs/2510.09426) | Fully documented synthetic-data curation, checkpoints, tokenizer, training logs and multilingual controls | Reported model quality is not a SZL benchmark. Language/source leakage and cultural/community data rights require separate audits |
| **South Korea — LG AI Research** | [EXAONE Deep](https://github.com/LG-AI-EXAONE/EXAONE-Deep), [K-EXAONE](https://github.com/LG-AI-EXAONE/K-EXAONE) | Evaluate small/medium reasoning models with explicitly separated training and inference baselines | A released weight or benchmark table does not authorize use of its training data or prove a comparable local result |
| **Ireland — Lero / AIware Lab, University of Limerick** | [AIware Lab](https://aiware-lero.github.io/), [Lero research](https://lero.ie/research/) | Fault localization, property-based testing, runtime monitoring and evaluation of AI-generated software | This is a software-assurance research lineage, not evidence that Lero developed an SZL-compatible GRPO trainer |
| **Ireland — BDS / Conor Ryan** | [BDS group](https://bds.ul.ie/about.html), [BDS GitHub](https://github.com/bdsul), [GRAPE](https://github.com/bdsul/grape) | Grammatical evolution for constrained candidate programs and adversarial test generation | Generated programs are **untrusted inputs**; never execute them against privileged services or claim that search gives a Lean proof |
| **International reference implementations** | [PrimeIntellect prime-rl training/recovery](https://github.com/PrimeIntellect-ai/prime-rl/blob/main/docs/training.md), [OpenRLHF checkpointing](https://openrlhf.readthedocs.io/en/latest/checkpoint.html) | Distinct trainer/orchestrator resume state, optimizer/sampler continuity, and reproducible evaluation entrypoints | Copy *design lessons* after license, threat-model and integration review; preserve SZL's existing one-writer architecture |

Each experimental intake must pin exact upstream repository SHA, paper version, license, dataset rights and locally changed diff. A moving webpage or upstream model card is a *lead*, not immutable experiment provenance.

## Existing SZL substrate: reuse, do not fork its authority

1. [Ancient mathematics source ledger](ANCIENT_MATH_SOURCE_LEDGER_20261118.md) and [math-to-runtime execution matrix](../../MATH_RUNTIME_EXECUTION_MATRIX.md): distinguish mathematical identities from provenance, historical claims and the **eight** locked proof identifiers F1/F4/F7/F11/F12/F18/F19/F22.
2. [lutar-lean](https://github.com/szl-holdings/lutar-lean) / Mathlib / Lake: exact proof revision and `#print axioms` evidence. The unconditional uniqueness version of Λ is **disproved as stated**; only its separately established conditional theorem may be cited. Khipu BFT safety is not an unconditional established theorem.
3. [szl-formulas](https://github.com/szl-holdings/szl-formulas), [szl-invariants](https://github.com/szl-holdings/szl-invariants), [szl-mesh](https://github.com/szl-holdings/szl-mesh) and [szl-forge](https://github.com/szl-holdings/szl-forge): explicit parameterized formula implementations, synthetic-only heritage-math fixtures, graph/control-plane wiring and adversarial testing. Do not infer deployed behavior from a source module.
4. [szl-gpu-bridge](https://github.com/szl-holdings/szl-gpu-bridge): the existing trainer, one-shot snapshots, artifact qualification, evaluation binding and receipt transport. Treat it as the owner of its own schemas; **do not** add a second scheduler, observer or Flagship54 shutdown guard.
5. [szl-receipt](https://github.com/szl-holdings/szl-receipt), [szl-quant-witness](https://github.com/szl-holdings/szl-quant-witness), [hatun-mcp](https://github.com/szl-holdings/hatun-mcp): content identity, witness replay and governed tool boundary. A hash is not a signer or independent scientific validation.

## Original testable proposal: evidence-gated curriculum, not a new theorem

Model outputs are assessed using a **three-valued** evidence state (\{\mathrm{PASS},\mathrm{FAIL},\mathrm{UNKNOWN}\}) at each mandatory rail. `UNKNOWN` propagates as `REVIEW/ABSTAIN`, never as zero failures or implied success. The proposed mandatory rails are:

- (G_1) input/source rights and immutable dataset identity;
- (G_2) correct answer under a known independent oracle (where an oracle exists);
- (G_3) proof-term/kernel replay if a formal claim is made; no proof is required where the task only requests ordinary factual answers;
- (G_4) checkpoint/restart and producer-to-adapter binding;
- (G_5) held-out evaluation binding, denominator and contamination checks;
- (G_6) signed publication/owner authorization for consequential release.

For a requested claim set (J(x)), **admission is conjunctive**:
(\mathrm{ADMIT}(x)=\bigwedge_{j\in J(x)}[G_j(x)=\mathrm{PASS}]).
A single `UNKNOWN` yields `HOLD`. This is a **proposed engineering policy**, not a newly proved Lean theorem or a claim that all six rails are implemented.

For eligible GRPO-style experiments, compare group-centered reward estimates
(A_i=(r_i-\bar r)/(s_r+\epsilon)), with a separately pinned upstream algorithm specification. A **hypothesized**, not deployed, reward is
(r_i=w_c C_i+w_p P_i-w_f F_i-w_u U_i),
where (C_i) is independently checked correctness, (P_i) a verified proof *when requested*, (F_i) an incorrect-confident-answer indicator, and (U_i) a policy violation. Weights and normalization **must be preregistered on calibration data**; no reward or evaluation signal can be constructed from hidden held-out answers. `ABSTAIN` is scored in a separate coverage/utility analysis and cannot automatically count as correctness.

Use the existing experimental **Λ geometric-mean advisory** only on strictly positive, independently measured, dimensionless normalized factors and with the documented conditional semantics. Missing factors invalidate the aggregate; Λ must never override mandatory `HOLD`/signed authority or be represented as an unconditional theorem.

### Bounded experiment ladder — no compute launch authorized by this document

| Arm | Intervention | Matched control | Required falsifier |
| --- | --- | --- | --- |
| E0: integrity baseline | Pure read-only provider/source/checkpoint/recovery census with explicit pagination and omitted scope | Same authorized immutable sources at previous observation | Incomplete project discovery, unverified trainer bytes, mismatched command target, or missing backups => `UNOBSERVED/HOLD` |
| E1: resiliency | After an approved owner-controlled training allocation, compare exact resume state, optimizer/scheduler/sampler/RNG **opaque** byte preservation and step continuity | Baseline existing trainer on same base/data/steps/compute | A preemption returns to step 0, loses sampler position, or produces no pinned recovery record |
| E2: proof curriculum | Synthetic decimal khipu-style position, Egyptian doubling/fraction identities, Euclidean GCD, and independent algebra/oracle cases; learn from **derived** exercises | Same synthetic data budget without proof feedback | No held-out gain or any new incorrect-confident answer, leakage, source-rights failure or unproven archaeological claim |
| E3: verified RL and abstention | Verifiable rewards and a calibrated abstain option using approved GRPO/reference implementation | Matched SFT / GRPO-only / abstention-only ablations | Improvement disappears on genuinely new templates, false-accept rate worsens, or proof replay fails |
| E4: generalization and assurance | Multilingual/synthetic controls plus grammar-evolved adversarial tasks, isolated from privileges | Same model/token budget and untouched independent heldouts | Leakage, executable generated payloads, unreproducible seeds, incompatible license or lack of statistically supported benefit |
| E5: agentic proof path | Governed tool interactions through Hatun → SZL Forge → receipt replay, with failure injection and bounded rollback | Same task distribution with existing governance, *not* an unguarded production agent | Any action without owner permission, any unlogged tool effect, a broken hash chain or unverified rollback |

**Measurement contract.** Report dataset IDs and rights, exact base/adapter/revision, prompt templates, seeds, GPU type and GPU-hours, steps, wall-time, checkpoint integrity, evaluation harness commit, contamination controls, sample counts, accuracy conditional on answered cases, abstention/coverage, false-accept count, confidence intervals (e.g. Wilson interval for binomial endpoints), latency and cost. Use matched paired examples and preregister the primary metric plus multiplicity correction. An empty or unavailable denominator must display **UNAVAILABLE**, not 0% or 100%. Include negative and inconclusive results, and do not transfer a benchmark from older weights to a new adapter.

## Implementation routing and acceptance sequence

1. **Recover observation first.** Respect the authorized protected one-shot release and its SHA-256 trust gate. If absent, report coverage `UNOBSERVED` and prepare a separately reviewed owner-controlled restoration; never substitute an unpinned local probe or silently fall back after 401/403/429.
2. **Fix evidence-channel load at source.** Rate-limit and batch *non-proof* log/heartbeat messages; maintain per-receipt immutable readback for boot, completion and public claims. A `429` means preservation admission is held pending a successful later immutable readback. Existing concurrent writer ownership remains intact.
3. **Qualify artifact-only evidence.** Trainer JSON at exact revision + actual final adapter bytes, tokenizer/config, complete restartable state and independently read-back backup. This is `ARTIFACT_VERIFIED` at best, not quality or training authorization.
4. **Run only approved small paired canaries.** Use source-owned container/image/dependency pins; no arbitrary upgrades inside an image, no budget or replica expansion, and no restart based only on filenames or HTTP 200.
5. **Promote through distinct gates.** `TRAINING`, `ARTIFACT_VERIFIED`, `EVALUATED`, `DEPLOYED`, `QUALIFIED` must never collapse to one badge. Source PR, CI green, immutable Hub publication, public rendered card and serving behavior require independent readbacks.

## Non-goals and owner decisions

No live cloud change, no new data scraping or training-data ingestion, no model/prompt code execution from upstream repositories, no alteration of the existing guard, no credentials in receipts, no checkpoint deletion, no paper DOI/v26/P3 promotion, no unsigned public qualification, and no unapproved adoption of partner or heritage data. Before production work, the owner must resolve transport/observer restoration, receipt throughput ownership, exact training worker/image pins, and a budgeted cloud test window. A merge of this note **cannot** satisfy those runtime obligations.
