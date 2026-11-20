<!-- SPDX-License-Identifier: CC-BY-4.0 -->
# Evidence Closure Graph (ECG): falsifiable research intake for agentic review, retrieval and formal obligations

**Status:** proposed source-only integration research. **Owner:** `szl-holdings/szl-papers`.
**Base source:** `bbddb249a847082f01de0271aa5596e236dcec17`.
**Execution:** BETTERWITHAGE, 2026-11-19 ET / 2026-11-20 UTC.
**No new theorem, benchmark, DOI, publisher authority or production admission.**

## Question / intended contribution

Can an evidence-typed directed acyclic claim graph make it easier to reject *false
readiness* in multi-agent engineering than ordinary untyped dashboards or retrieved
source snippets, without requiring agents to share administrator privileges?

This is **an experimental integration hypothesis**, not an established unique
contribution. Graph-based retrieval, provenance graphs, reproducible build records,
signed attestations and review workflows are established prior work.

## Source ownership and status

- The prior Ouroboros v1-v26 thesis, `lutar-lean` conditional Theorem U and
  Khipu's conditional quorum claims are **not** rewritten or upgraded here.
- Existing locked eight: F1/F4/F7/F11/F12/F18/F19/F22 at the paper's
  historical snapshot `5cfaf9a3b55fd75e8a2a1197502a93dd8ca68be3`.
  The current claim-wording ledger has EXCEEDS/PARTIAL/MARGINAL findings;
  a locked registry count alone does not certify broad prose interpretations.
- Unconditional uniqueness of the equal-weight geometric-mean Lutar
  aggregator under the original axioms is **machine-checked false**;
  Theorem U is conditional, and requires the exact proved hypotheses.
  Numeric Lambda values here are at most advisory and never release gates.
- The umbrella concept DOI `10.5281/zenodo.19944926` identifies prior program
  lineage, **not** this paper. No new DOI, Zenodo version or arXiv ID exists.

## Proposed evidence model

Each claim in `G=(V,E)` is a node whose parent edges identify prerequisites
(e.g. source snapshot -> test -> review -> signer -> runtime admission). The graph
is required to be acyclic. Each node declares its exact source SHA, hashes for
test/review/receipt *documents*, and a declared disposition of dissent.
Hierarchical retrieval (GraphRAG/HiRAG-like) may propose nodes and context;
**retrieval ranking must never become proof of source, reviewer or signature**.

The present code in `scripts/assess_evidence_closure_graph.py` deliberately
checks only bounded JSON shape, revision equality, references, duplicate/cyclic
edges, digest syntax, and unresolved dissent. It never downloads sources,
replays tests, verifies signatures, authenticates Kimi/Mistral identities,
proves source refinements, or authorizes a merge. A positive result is
`REVIEW_CANDIDATE_ONLY`, not READY.

A future *separate* privileged verifier would have to fetch immutable source
bytes, replay exact test artifacts, authenticate a non-colluding reviewer,
verify a signature chain and resolve a deployment window. This PR does
**not** implement that verifier.

## Peer-coding transcript boundary

A bounded sanitized public-fact packet was supplied over Ollama to Kimi
`kimi-k3.1-pro:cloud` and local Ministral `ministral-3:3b`. Both produced
textual critiques; neither fully satisfied the strict JSON response schema.
Kimi challenged circular self-certification, receipt self-rehash, reviewer
collusion and novelty against provenance practice. Mistral challenged weak
falsifiability and prior-art overlap, but made unsupported assumptions about
the SZL implementation; those are research questions rather than evidence.
**No model's answer was executed, admitted as an independent review,
or supplied with a secret, production token or unrestricted tool.**

## Fixed falsification protocol (proposed)

Freeze a corpus of claims from a public repo and label every test case before
running experimental graph retrieval. For every candidate, demand:

1. exact immutable source revision and no speculative source-to-runtime parity;
2. deterministically replayed negative test with count and independent result;
3. a distinct reviewer identity evidenced outside the source document;
4. cryptographically verified signer and receipt (none exist in this prototype);
5. explicit unresolved dissent and dependencies, including graph-cycle checks;
6. a *positive* control so that a validator rejecting all input is not rewarded;
7. denominator: every injected false-ready case, not only the cases retrieved.

**Primary outcome:** false production admissions among injected false-ready
claims; target zero, **unmeasured**. Secondary outcomes: missing-evidence recall,
precision of unique-source retrieval, p95 latency, CPU/energy and human review
time, each with exact denominators and baseline harness. Compare against
plain-text retrieval, an ordinary graph index, and a graph with typed evidence
but no dissent gate. Report abstentions and unclassified cases separately.
Nothing here claims that target has been achieved.

## Concrete source-only regression coverage

`python scripts/test_assess_evidence_closure_graph.py` -> 20/20 local
unit tests passed, including 40 separately generated cycle controls and
15 structurally valid chains that remain unauthorised for production.
The suite rejects duplicate JSON keys, arbitrary trust/authority fields,
self/unknown edges, duplicate nodes, inconsistent SHA pins, forged
self-consistent hash declarations and missing dissent resolution.
**Not** a complete security audit, CI run, Lean proof or production test.

## Product alignment: design only, not deployed

- **Second Brain / Prisca-GraphRAG / HiRAG:** retrieve source *candidates* and
  ancestor obligations; abstain when model identity is missing, regardless of
  an HTTP 200 health endpoint.
- **Khipu:** treat verified model identity, licensed weights, dataset lineage,
  training and signed inference receipts as separate preconditions.
- **Agentic Anatomy / Holo:** render verified evidence state separately from
  curated 3D objects; an attractive scene is not live data rendering.
- **A11oy / Killinchu / Hatun:** source tests, authenticated runtime behavior,
  side-effect safety and release receipts are four distinct evidence classes.
- **Cloudflare / PyPI / Snowflake:** settlement, wheel provenance, and DB
  query/readback are separate actual transactions; x402 challenges, packages
  and database connection screens are not substitutions.
- **Robotics:** simulator traces and bounded actuator policies are required
  before any real-world command. Historical Egyptian/Greek mathematics and
  Andean khipu are *comparative intellectual motifs*, not a validated direct
  source of these modern algorithms.

## Public peers and reproducibility references

- Microsoft GraphRAG, Edge et al., arXiv:2404.16130:
  https://arxiv.org/abs/2404.16130
- Huang et al., Hierarchical Knowledge RAG, EMNLP 2025:
  https://aclanthology.org/2025.findings-emnlp.321/
- SWE-rebench, NeurIPS 2025, contamination-aware coding-agent evaluation:
  https://proceedings.neurips.cc/paper_files/paper/2025/hash/21bec6ace947b1b58967b945c8ac0f10-Abstract-Datasets_and_Benchmarks_Track.html
- Google SRE reliable product launches:
  https://sre.google/sre-book/reliable-product-launches/
- W3C PROV-O: https://www.w3.org/TR/prov-o/
- RFC 9162: https://www.rfc-editor.org/rfc/rfc9162.html
- Existing SZL deposit policy: ../../ZENODO_DEPOSIT_POLICY.md

**Attribution:** these sources inform experiment design only; no upstream code,
text sections or datasets copied into this implementation.

## Release and editorial holds

1. Exact-head GitHub CI and independent source-owner review, no self-approval.
2. Source-byte/Lean proof readback and per-formula claim-wording reconciliation.
3. Reproducible empirical study with pre-registered denominators and baseline.
4. Paper-specific novelty and DOI collision review under `ZENODO_DEPOSIT_POLICY.md`.
5. Independent signing, authenticated runtime and external release evidence
   before any consumer-facing or production admission.

A structurally well-formed evidence claim is not scientific validity.