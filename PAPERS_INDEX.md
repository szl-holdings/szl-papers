# SZL Holdings — Papers Index (Zenodo DOIs)

Author: **Stephen P. Lutar Jr.** · ORCID: [0009-0001-0110-4173](https://orcid.org/0009-0001-0110-4173)
License: CC-BY-4.0 · Migrated to org namespace 2026-06-02 · Papers Space: `betterwithage/szl-papers-live`

**Umbrella concept DOI:** [10.5281/zenodo.19944926](https://doi.org/10.5281/zenodo.19944926)
**Umbrella v21:** [10.5281/zenodo.20490218](https://doi.org/10.5281/zenodo.20490218)

## Papers

| # | Title | DOI |
|---|---|---|
| 1 | Lutar Omega Formalism | [10.5281/zenodo.20499315](https://doi.org/10.5281/zenodo.20499315) |
| 2 | Prisca-GraphRAG | [10.5281/zenodo.20499317](https://doi.org/10.5281/zenodo.20499317) |
| 3 | Hermetic Constitutional Guardrails | [10.5281/zenodo.20499319](https://doi.org/10.5281/zenodo.20499319) |
| 4 | Sefirot Continual Learning | [10.5281/zenodo.20499322](https://doi.org/10.5281/zenodo.20499322) |
| 5 | Free-Energy-Lutar Active Inference | [10.5281/zenodo.20499324](https://doi.org/10.5281/zenodo.20499324) |
| 6 | Tawa Sparse Autoencoder | [10.5281/zenodo.20499328](https://doi.org/10.5281/zenodo.20499328) |
| 7 | EPR-Bell Entanglement Validation | [10.5281/zenodo.20499330](https://doi.org/10.5281/zenodo.20499330) |
| 8 | Chinchilla-Lutar Scaling Laws | [10.5281/zenodo.20499334](https://doi.org/10.5281/zenodo.20499334) |

> Honesty (Doctrine v11): Λ-uniqueness taxonomy — *governance-safe* uniqueness is **Theorem U** (proven, conditional, axiom-free: unique *modulo* `≈Λ` under the Identifiability Assumptions, strict `=` only under `Anchored`/`Normalized`; [`Lutar/Uniqueness/TheoremU.lean`](https://github.com/szl-holdings/lutar-lean/blob/main/Lutar/Uniqueness/TheoremU.lean)), while *unconditional* uniqueness stays **Conjecture 1 — OPEN** (machine-checked false as stated, not a proved theorem). Supply-chain posture is **SLSA L1+L2 attested** (killinchu, a11oy), L3 roadmap. Harvested from HF model card `SZLHOLDINGS/szl-papers` during the HF Collections harvest.

---

## arXiv submission line (preprint packages, not yet posted)

Three finished papers are prepared as complete arXiv LaTeX packages under [`thesis/arxiv/`](thesis/arxiv/) (each has `main.tex`, `references.bib`, `ARXIV_METADATA.md`). **None is posted to arXiv yet** — arXiv requires the founder to submit manually; see [`ARXIV_SUBMISSION_GUIDE.md`](ARXIV_SUBMISSION_GUIDE.md). The Zenodo concept DOI ([10.5281/zenodo.19944926](https://doi.org/10.5281/zenodo.19944926)) already covers the program.

| Paper | Title | Primary arXiv | Lean grounding | Status |
|-------|-------|---------------|----------------|--------|
| **P1** | Verifiable Append-Only Governance: Kernel-Proven Acyclicity, FIFO Reception, and Emit Monotonicity for AI Decision Receipts | `cs.LO` (x-list cs.CR/cs.DC/cs.LG) | F4 `f4_khipu_dag_acyclic_preserved`, F7 `f7_chaski_fifo_order`, F22 `f22_khipu_emit_monotone`, `locked_count_eight` | **Submission-ready** |
| **P2** | A Kernel-Verified Graph Substrate for Governed AI: Iso-Invariant Trust Aggregation, a 1-WL Ceiling, Spectral Contraction, and Bounded-Frontier DAG Termination | `cs.LG` (x-list cs.LO/cs.DM/stat.ML) | 11 Wave-6 theorems (`Λ_graph_iso_invariant`, `gnn_le_wl`, `geometric_contraction`, `frechet_isometric_embedding`, …), no new axiom | **Submission-ready** |
| **P3** | Governed Post-Determinism: A Unified Theory of Verifiable Autonomy (Ouroboros Thesis v26, Locked-Eight Edition) | `cs.LO` (x-list cs.CR/cs.LG/math.OC) | locked-8 + Theorem U + Wave-23 `khipu_quorum_safety_conditional` | **Submission-ready** |

---

## Ouroboros Thesis lineage (v1 → v26)

The DOI-pinned thesis lineage lives under [`thesis/`](thesis/) and [`thesis/ouroboros/papers/`](thesis/ouroboros/papers/). Full timeline: [`thesis/THESIS_LINEAGE.md`](thesis/THESIS_LINEAGE.md).

| Ver | Title | Location | Headline |
|----|-------|----------|----------|
| v22 | "Convergence" | `thesis/ouroboros/papers/v22/` | A5 merge; VCG; Cauchy_ND partial; SLSA posture advanced |
| v23 | "Conditional Uniqueness / Unified Substrate" | `thesis/ouroboros/papers/v23/`, `thesis/v23/` | conditional Λ gated on declared A6′; unconditional FALSE; Λ = Conjecture 1 |
| v24 | "Axiom-Free Conditional Uniqueness" | `thesis/ouroboros/papers/v24/`, `thesis/v24/` | A6′ gate removed — Theorem U `lambda_unique_of_separable` axiom-free; CUT-1 closed (Waves 18–22) |
| v25 | "Governed Post-Determinism (GPD)" | `thesis/ouroboros/papers/v25/` | unification of v1–v24 into the five-pillar GPD framework; incorporates Wave-23 `khipu_quorum_safety_conditional`; checkable-antecedent pattern; locked = 5 at that pin |
| **v26** | **"Governed Post-Determinism (GPD), Locked-Eight Edition"** | [`thesis/ouroboros/papers/v26/`](thesis/ouroboros/papers/v26/), [`thesis/arxiv/gpd-v26/`](thesis/arxiv/gpd-v26/) | **locked-proven count moves 5 → exactly 8 {F1,F4,F7,F11,F12,F18,F19,F22}; genuine non-vacuous F4/F7/F22 proofs (2026-06-10); `locked_count_eight` by `decide`; kernel baseline unchanged** |

> **v26 doctrine (binding):** GPD is SZL's OWN framework, grounded only in the SZL Zenodo DOIs (no external "post-deterministic" cite). Locked-proven = **exactly 8** {F1,F4,F7,F11,F12,F18,F19,F22} @ `c7c0ba17` (749/14/163), certified by `locked_count_eight` (by `decide`); F4 (Khipu DAG acyclicity), F7 (Chaski FIFO ordering), F22 (Khipu emit append-only monotonicity) newly proven 2026-06-10 — F4/F7 were previously vacuous, now genuine; ~185 experimental CI-green (Waves 11–23) are a separate tier, never folded into the locked eight. Λ unconditional uniqueness = **Conjecture 1** (machine-checked FALSE); conditional = **Theorem U**, axiom-free. Khipu BFT safety = **Conjecture 2**; Wave-23 proves only **conditional** agreement (`n≥3f+1` + honest non-equivocation, axiom-clean); liveness = Conjecture 3. **SLSA L1+L2 attested** where `attest-build-provenance` runs (killinchu, a11oy), else L1 honest / L2 roadmap; **L3 roadmap**; FedRAMP/Iron Bank/CMMC only with "roadmap." Trust never 100%; 0 runtime CDN. Unbroken DOI chain v1→…→v25→v26; v26 continues — does NOT overwrite — the immutable v20–v25 sources.

---

*Signed-off-by: Yachay <yachay@szlholdings.ai>*
*Co-Authored-By: SZL Unified Thesis Collective · Perplexity Computer Agent <agent@perplexity.ai>*
