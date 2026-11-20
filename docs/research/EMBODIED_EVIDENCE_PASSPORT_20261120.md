# Embodied Evidence Passport — original SZL physical-AI research intake
**Date:** 20 November 2026 (UTC). **Authority:** source-only hypothesis, not a normative doctrine amendment, publication, hardware authorization, trained policy, verified deployment, qualified model, customer sale, or released package. The machine-readable experiment and ten HOLD gates are in [embodied-evidence-pilot-20261120.json](embodied-evidence-pilot-20261120.json).

## Executive decision
**Build the verification layer beside robotics foundation models, not a competing untrained humanoid foundation model.** The product hypothesis is a provenance-carrying *action passport* for each simulated robot episode: exact source/model/dataset/configuration, rights, calibration and safety state, observed action digest, independent verification, replay and a graph of what remains UNKNOWN. A beautiful 3D graph with invented "LIVE" nodes is a failed product, not a feature.

This is a proposed SZL synthesis of established practices. It is **not** a priority or novelty claim over prior art, and no outside code, model weights or datasets were copied. The first lane is **offline simulation-only** with synthetic, rights-clear fixtures. There is no unattended real-world robot control, GPU training, new cluster, cloud spend, or automatic rollout.

## Primary-source landscape and adaptation

| Leader | Primary paper/code/engineering reference | What is transferable | What we do *not* inherit |
|---|---|---|---|
| NVIDIA Isaac GR00T N1.7 | [official GitHub](https://github.com/NVIDIA/Isaac-GR00T), [July 2026 end-to-end development](https://developer.nvidia.com/blog/develop-humanoid-robot-policies-end-to-end-with-nvidia-isaac-gr00t/), [GR00T N1 paper](https://arxiv.org/abs/2503.14734) | Demonstration-to-model lineage, embodiment tags, simulation/real evaluation separation, reproducible training inputs | Checkpoints, licensing, benchmark numbers, commercial authorization or robotics qualification. Source code and model weights carry separately stated licenses; verify both |
| Hugging Face LeRobot / SmolVLA | [LeRobot GitHub](https://github.com/huggingface/lerobot), [SmolVLA documentation](https://huggingface.co/docs/lerobot/main/smolvla) | Standard episode schema, sensor/video/state/action synchronization, dataset revision and evaluation conventions | Private demonstrations, automatic rights to third-party datasets, measured robot success or a deployed policy |
| Google DeepMind Gemini Robotics 2.5 | [10 Nov 2026 research update](https://deepmind.google/blog/gemini-robotics-2-5-accelerates-real-world-physical-intelligence/) | Physical reasoning, task generalization and safety evaluation categories | Access to proprietary models, software/weights, licensed commercial rights, or comparable performance |
| Google SRE | [launch checklist](https://sre.google/sre-book/launch-checklist/), [canary evaluation](https://sre.google/workbook/canarying-releases/) | Independent production readiness, failure drills, capacity, monitoring, staged rollout, measured rollback | A passed launch merely because CI is green |
| Software provenance | [SLSA security levels](https://slsa.dev/spec/v1.2/), [RFC 9162](https://www.rfc-editor.org/rfc/rfc9162.html), [W3C PROV-O](https://www.w3.org/TR/prov-o/) | Build provenance, inclusion/consistency proofs, entity/activity/agent lineage | The false assumption that SHA-256 alone is an authorized signature or external attestation |

**Research boundary:** these sources were studied as public material; this is not an exhaustive review of every leader, publication, robot embodiment, benchmark, license, or GitHub organization. Every newly introduced upstream dependency requires its own exact revision, rights review and independent reproduction before adoption.

## System-of-systems design (hypothesis)

1. **Sensor/episode adapter** (future owner: retrieval-bench, LeRobot-compatible connector): reads synthetic, time-synchronized episode and calibration metadata; hashes public fixture bytes. No private videos are copied to a graph.
2. **Artifact identity** (future owner: GitHub source + HF immutable revisions): binds a specific source commit, model/config digest, dataset revision and rights. A model card or download does not establish training or quality.
3. **Safety gate** (future owner: a11oy/Hatun): verifies tenant, intended action scope, policy version, calibration, freshness and independent review. The initial mode cannot dispatch to actuators; missing or contradictory evidence always refuses.
4. **External verifier** (future owner: governed-receipt-spec / szl-receipt): verifies a trusted issuer/signature, anti-replay and immutable linkage. Declared hashes and self-recomputed certificates remain UNVERIFIED.
5. **Append-only evidence** (future owner: existing receipts/ledger owner): stores bounded provenance and a negative verdict even for failed episodes. Never serialize or execute untrusted training pickle files.
6. **Holographic graph** (future owner: holographic-unify / a11oy): displays per-node source revision, UTC observed time, age, denominators, evidence link and statuses such as DENY, STALE, UNVERIFIED and SIMULATED_ADMISSIBLE_FOR_REPLAY. Decorative animation is never telemetry.
7. **Customer evidence export** (future owner: product/billing): offers a replayable test report only after source, privacy and rights clearance. Payment receipts and actual settlements must be independently reconciled; an HTTP 402 or payment challenge is not revenue.

No implementation step above grants automatic training, source merge, account configuration or real-robot execution.

## Reproducible experimental protocol

**H1 — false admissions.** Preregister at least 1,000 simulated negative episodes across 12 adversarial classes: wrong source/model revision, missing dataset rights, future/stale clock, replayed episode ID, tampered action/sensor hash, stale calibration, unsafe interlock, forged "signature verified", tenant mismatch, edge disconnect and simulated-as-real claims. Baseline: status-only, unsigned metadata display. Primary metric: false admission count / total adversarial episodes. Target: **0 among a preregistered population**, while reporting the statistical upper confidence bound; 0/1000 observations does **not** prove a zero underlying risk.

**H2 — comprehension.** With fixed scenarios, identities, source revisions and participant order randomization, compare the evidence-bound 3D lens against the existing 2D log/receipt table. Report ground-truth fault-localization accuracy, p50/p95 seconds, user task failures and confidence intervals. A pretty renderer is not a measured reduction in investigation time.

**H3 — overhead.** Against a signed JSON log with equivalent rights and source-binding checks, report verified events/sec, bytes/episode, p50/p95 verification latency, cold and warm startup, bounded memory and storage, and cost per verified million simulated episodes. Report failed or unverified receipts separately. Do not extrapolate these numbers to GPU training, revenue, robot reliability or deployed real-time control.

**Gate mathematics:** for proposal x, an initial conservative admission candidate is A(x) = I(source) × I(rights) × I(calibration) × I(freshness) × I(policy) × I(replay) × I(independent_verifier). Each I is a separately measured binary test, not an AI model's assertion. If any factor is absent, zero or unobserved, **refuse**. This conjunctive policy is a routine safety rule, not a new theorem or a replacement for locked SZL mathematics. Report **coverage** as independently verified eligible events divided by all eligible attempts, with an empty denominator = UNAVAILABLE; do not treat declared hashes as verified.

**Dataset governance:** require explicit rights and consent, separate source-group-held-out tasks from training and tuning, bind every result to immutable weights and benchmark version, retain private imagery off public cards, and forbid shortcut learning on held-out tasks.

## Consumer readiness borrowed from operating organizations

1. **Working backwards / PRFAQ:** define the buyer, incident, current manual cost, why this product wins, measurable outcome, acquisition and willingness to pay *before* an attractive demo. See the [Amazon Working Backwards framework](https://workingbackwards.com/concepts/working-backwards-pr-faq-process/).
2. **Engineering acceptance:** reproducible CI with exact SHAs, deterministic negative tests, dependency/license inventory, SBOM, threat model, identity/auth/tenant tests, resource limits, backup/restore drills, accessibility including 2D fallback and reduced-motion support, browser/device smoke, load/soak tests, SLO/error budget and user support.
3. **Release admission:** independent reviewer approval, signed provenance and published artifact readback, sampled canary with a control group, measured error/latency thresholds, rollback rehearsal and observed deployed revision. SLO failure or inconsistent identity stops promotion.
4. **Commercial admission:** test-mode receipts, webhook idempotency/replay controls, reconciliation to actual settlement, refund and customer-support paths, accurate pricing copy, legal/privacy review and customer-facing SLAs. No advertised settlement or revenue without records.

For physical hardware, separately add hazard analysis, human emergency-stop ownership, interlock validation, functional safety assessment, offline sandbox escape testing, equipment insurance and qualified hardware supervision. None of those has been completed by this proposal.

## First paying-customer hypothesis

**Buyer:** robotics integration shops, labs and fleet QA teams. **Job-to-be-done:** demonstrate reproducibly why a simulated policy/robot run was admitted, rejected or withheld. **Free entry:** Python/TypeScript offline receipt verifier, sample synthetic datasets and a falsifiable example report. **Paid hypothesis:** managed report storage, third-party-verifiable audit bundles, private deployment, source-to-runtime lineage and fleet audit exports. Pricing and buyer conversion are **UNKNOWN**, not launch-approved. Commercial moat must be tested against open alternatives, not proclaimed.

**What not to sell yet:** unverified robot safety certification, autonomy, SOTA model superiority, production uptime, zero false-positive risk, actual x402 revenue or guaranteed regulatory compliance.

## Cross-plane ownership and current holds

| Plane | First desired source-owned deliverable | Separate admission needed |
|---|---|---|
| GitHub (szl-papers / szl-org-health) | this typed protocol, schema validation and owner mapping | review, protected-main CI, exact-head merge and evidence chain |
| Hugging Face SZLHOLDINGS | approved, revision-pinned dataset/model cards and synthetic demo | write scope, rights, Hub SHA, rendered public readback; no current complete org inventory |
| A11oy / Hatun / Killinchu | bounded action-refusal and simulation-only verification adapters | authenticated runtime, interlocks, privacy, held-out tests and negative controls |
| 3D / Holo | independent evidence lens and accessible 2D fallback | actual live telemetry/identity/collector readback, not catalog labels |
| Cloudflare / x402 | optional verification API with test-mode payment | DNS/Worker/WAF owner authority, signing, webhook settlement, rollback and billing |
| PyPI | versioned offline verification SDK | signed wheel, Trusted Publisher, test import, source-to-wheel parity and metadata |
| Snowflake | privacy-restricted evidence analytics tables | authorized warehouse connection, role, retention, row access and query audit |

**Release disposition: HOLD.** The companion JSON starts every gate at HOLD and every measurement at null. Existing Flagship54 and Ouroboros controllers retain their owners. Ten independent whole-estate passes, full public/private inventory, source-to-HF parity, live robot evaluation, paid execution and production qualification are NOT claimed. Future passes should link to existing queues, not create a second writer or scheduler.
