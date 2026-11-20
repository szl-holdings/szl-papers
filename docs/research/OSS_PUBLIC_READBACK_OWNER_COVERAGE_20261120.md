# SZL × Kimi × Mistral — public OSS pin readback and owner coverage

**Observation (UTC): 2026-11-20T05:26:15.8175049Z.** Source-only / **NOT ATTESTED / NOT DEPLOYED / NO RIGHTS ADMITTED**. This is an additive verification report to the [17-upstream research intake](oss-global-source-pins-20261120.json), not another research controller. The corresponding compact [public readback record](oss-source-readback-20261120.json) was captured using authorized BETTERWITHAGE GitHub CLI read-only requests and checked against the source manifest's Git **blob** identity. Its matching Git blob is `23cdd6764d58332395d61741b9c44b0c71f6b818`.

## The gap that both model reviewers identified

The existing intake validated declared `repo`, 40-hex SHA, linked URL and `license` **shape**, not whether that commit existed on the claimed upstream repo. Kimi recommended a source-owner evidence ledger with exact population coverage; Mistral independently proposed a two-record pin cross-check. This PR implements their overlapping design insight as a **non-authorizing GitHub API readback comparison**. It is not a signature and was not collected by an independently trusted custodian; both the manifest and readback can be changed by one authorized editor. It cannot establish SLSA source level or legal usage rights.

On the recorded GitHub readback, **17 of 17** pinned upstream commit identifiers resolved to the exact pinned source revision. Current GitHub repository metadata SPDX labels agreed with all 17 recorded labels. This is **current repository metadata**, **not proof of the license applicable to any file at the pinned commit, transitive dependency, model weight or training dataset**. The Qwen3 GitHub license metadata was `NOASSERTION`, so it is explicitly **UNRESOLVED**, not guessed Apache/MIT.

The target-org metadata API was read in **two full-pagination calls**: 100 and 82 repos. It returned **182 metadata entries = 153 active + 29 archived**, including five private. The survey is non-atomic and not a semantic code or security audit. Private repo names are **not included** in the public readback record; only aggregate counts are. All **16 named, public SZL source-owner targets** referenced by the manifest were listed active, not archived or private.

Among **148 active public repositories**, two returned no GitHub license metadata: `conformance-corpus` and `frontier-55-runs`. Existing **draft** source-owner PRs [conformance-corpus#9](https://github.com/szl-holdings/conformance-corpus/pull/9) and [frontier-55-runs#1](https://github.com/szl-holdings/frontier-55-runs/pull/1) already address those cases. **Do not open competing PRs or auto-publish license statements without rights review.** A separately governed private `szl-billing` license PR #11 also exists; this public report does not publish any private code or asset identity inventory.

## What the new offline contract actually checks

The additive, stdlib-only `scripts/validate_oss_source_readback.py` consumes the exact source manifest and a separate readback record. It checks:

1. Existing v1 research source/rights/admission policy remains valid; the **exact manifest Git blob SHA** binds both views to the same source bytes.
2. Every upstream repo has exactly one API-reported commit + **HEAD** license-metadata row, with exact SHA and SPDX-label agreement and reported HTTP 200 on both GitHub API routes. Missing, duplicated, inaccessible or mismatched entries **HOLD**.
3. Every distinct manifest target (`source.target` and `experiment.target_repositories`) has exactly one public, active metadata record. Missing, swapped, private or archived owners **HOLD**. We do not publish the five private identities.
4. Scope counts reconcile within the recorded non-atomic pagination; attempts to claim a whole-estate semantic audit, signed provider evidence, cleared rights, new training, provider mutation or commercial qualification **HOLD**.
5. The result is **`RECORDED_PUBLIC_READBACK_CONSISTENT_NOT_ATTESTED`**. SHA-1 Git blob identity and SHA-256 asset digests are identifiers, **not signatures, legal clearances, runtime attestations or independent evaluators**.

The API observation is external to the *original manifest's assertions*, but its recorded JSON is still editable. Genuine independent verification next requires origin-signed source provenance / verified issuer expectations or fresh provider readback by the authorized owner, followed by exact pinned file LICENSE/NOTICE and dependency rights review. See the [SLSA source-verification guidance](https://slsa.dev/spec/v1.2/verifying-source) and [OpenSSF Scorecard](https://scorecard.dev/). A Scorecard badge does not prove correctness or license rights.

## Highest-value next engineering experiments (all unmeasured)

**Receipt and billing (A11oy, Hatun, szl-crosscheck, szl-receipt, szl-billing):** Freeze a synthetic run population, independently verify all attempted tool actions and evidence, and require an unrelated verifier before a *billability review*. An agent-signed or self-graded success, replay, missing denominator or fake payment settlement must **not** become chargeable. No live settlements or customer billing changed.

**Grounded retrieval (szl-retrieval-bench, Second Brain):** Compare pinned ColBERT-style late interaction against an independent BM25 reference on identical rights-checked query/qrels population, reporting attempted, measured, skipped and unavailable cases. Wrong tenant/source revision or citation without a matched passage is **ABSTAIN**, not a "live hologram" success.

**Simulation-only embodied validation (Killinchu, existing szl-papers physical-AI owner):** Use pinned, licensed LeRobot/GR00T/OpenVLA-compatible scenarios with independent baselines, safety-critical negative episodes and complete dataset provenance. Do not equate simulated safety with robot control clearance; that separate owner already has [PR #92](https://github.com/szl-holdings/szl-papers/pull/92).

For consumer-facing model cards and 3D evidence interfaces, display independent state columns — `SOURCE_PINNED`, `RIGHTS_REVIEWED`, `ARTIFACT_VERIFIED`, `EVALUATED`, `DEPLOYED`, `QUALIFIED` — only when each corresponding evidence gate exists. Never silently transform a matching commit into measured model quality or revenue.

## Explicit follow-through

This task makes **no upstream code import**, no model-weight/dataset download, no new paid training or GPU job, no Cloudflare/PyPI/Snowflake mutation, no consumer release, no repository visibility change and no credentials grant. A PR and offline green test are a proof of source behavior on synthetic cases only; rights and production admission remain independent. The next actual work belongs to existing source owners and existing independent reviewers, **not** to a new Ouroboros scheduler.
