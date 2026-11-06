# Receipt-Attached Reliability: Whole-Chain Measurement for Governed MCP Tool Servers

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](LICENSE)

**DOI:** [10.5281/zenodo.24005477](https://doi.org/10.5281/zenodo.24005477) — published on Zenodo, 2026-11-06.

Preprint P3 — **not peer reviewed**. The paper is [`main.md`](main.md).

**One-line summary:** scoring whole five-step MCP chains with receipt verification as
a scored step measured 100% chain success (10/10, 0.84 s mean) against the production
hatun-mcp server — and caught two configuration defects on its first run that
single-call smoke testing had missed.

**Measured claims (all receipted):**
- 10/10 chains, every step 10/10 including Khipu/DSSE receipt verification
- 0.84 s mean chain latency
- First-execution defect discovery: host-pinning (421) + tool-schema (403) failures
- Complementary burst-load study: p99 = 3.77 s, 0/43 errors

**Receipts:** `SZLHOLDINGS/model-eval-receipts` → `chain-test-mcp-2026-11-05.json`,
`loadtest-inference-2026-11-05.json`. Server: `szl-holdings/hatun-mcp` (Apache-2.0).

**Deposit route:** the per-paper `.zenodo.json` is local metadata only.
GitHub–Zenodo reads the repository-root `.zenodo.json`, which stays
reference-only and must not be minted as this paper (see root
`ZENODO_DEPOSIT_POLICY.md`). Do not cut a release to auto-mint `p3-v1.0.0`
onto the shared concept. DOI sync searches for this preprint's own title and
does not record any other deposit as its DOI.
