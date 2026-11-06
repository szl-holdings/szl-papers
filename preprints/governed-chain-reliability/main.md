# Receipt-Attached Reliability: Whole-Chain Measurement for Governed MCP Tool Servers

**Stephen P. Lutar Jr.**
SZL Holdings, North Salem, NY · ORCID 0009-0001-0110-4173 · stephen@szlholdings.com

*Preprint. Not peer reviewed. Version 1.0.0, 2026-11-05. All measurements in this work are
published as verbatim receipt files; see Data Availability.*

**DOI:** [10.5281/zenodo.24005477](https://doi.org/10.5281/zenodo.24005477) — published on Zenodo, 2026-11-06.

---

## Abstract

Agent systems built on the Model Context Protocol (MCP) compose multiple networked
steps — session initialization, tool discovery, tool invocation, and response
handling — into a single logical task. Conventional quality reporting scores each
step in isolation, which overstates end-to-end reliability: five steps at 95%
per-step reliability yield roughly 77% whole-chain success. We propose and
demonstrate a measurement protocol that scores *whole chains* with a *cryptographic
receipt attached to every step*: each governed tool call must emit a hash-chained
receipt (Khipu) inside a DSSE-signed envelope, and receipt verification is itself a
scored chain step. We implement the protocol against a production governed MCP
server (hatun-mcp) enforcing per-call authentication, a 13-axis input gate, client
reputation, and receipt emission on both success and failure. Across 10 complete
five-step chains, we measure 100% whole-chain success (10/10), 100% per-step success
including receipt verification, and 0.84 s mean chain latency. Notably, the protocol
detected two real configuration defects — a host-pinning mismatch (HTTP 421) and a
tool-argument schema mismatch (HTTP 403) — on its first execution, both of which
single-call smoke testing had missed; after remediation the measured chain success
was 100%. We release all raw measurements as verbatim receipts. The central
methodological claim is modest and falsifiable: when reliability is scored at the
chain level and provenance is scored as a step, both the reliability estimate and
its evidence are stronger than per-call reporting alone can provide.

**Keywords:** agent reliability; Model Context Protocol; provenance; DSSE; receipts;
chain-level evaluation; governed AI

---

## 1. Introduction

Production agent systems fail at their seams. A tool server that responds correctly
to 95% of individual calls will still fail roughly one in five five-step chains
(0.95⁵ ≈ 0.774), and the failures concentrate in exactly the places single-call
testing does not look: session lifecycle, discovery/schema drift, and transport
configuration. At the same time, the emerging commercial model for agent
infrastructure — per-call metered access to governed tool servers — creates a second
requirement that conventional reliability reporting ignores: every billable action
should carry verifiable provenance, both for the customer's audit trail and for the
operator's own honesty about what the system did.

This paper contributes:

1. **A whole-chain measurement protocol for MCP tool servers** in which (i) the unit
   of scoring is the complete chain, not the call; (ii) receipt verification is a
   scored step, so provenance is measured, not assumed; and (iii) latency is
   reported per chain and per step.
2. **A reference implementation** against a production governed MCP server
   (hatun-mcp) that enforces per-call API-key authentication, a 13-axis conjunctive
   input gate (Yuyay-13), a per-client reputation factor, hash-chained Khipu receipts
   on success *and* failure, and DSSE-signed responses.
3. **Measured results with published receipts**, including the protocol's own
   failure-mode discovery: on first execution the protocol caught two configuration
   defects that single-call smoke testing had missed.
4. **A complementary burst-load latency study** of the co-located inference server,
   reported at the 99th percentile rather than the mean, in which p99 = 3.77 s with
   zero errors across 43 requests including 8-concurrent bursts and near-context-limit
   prompts.

We deliberately do not claim generality beyond the studied system. The contribution
is the protocol and its receipts, not a leaderboard.

## 2. Related Work

Chain-level evaluation of composed systems is well established in question-answering
pipelines and agentic benchmarks, which score end-task success rather than component
accuracy. The MCP specification standardizes tool-server transport (Streamable HTTP,
stdio) but does not prescribe reliability measurement or provenance. In-toto and the
DSSE (Dead Simple Signing Envelope) standard provide the provenance envelope used
here; SLSA provides the supply-chain integrity vocabulary. What prior art does not
combine — to our knowledge — is (a) chain-level reliability scoring, (b) provenance
verification *as a scored step inside the chain*, and (c) per-call economic
enforcement (x402 metered access) on the same surface being measured. The SZL
governance substrate (Doctrine v11; Λ aggregator with Conjecture 1 preserved as
disproved-as-stated; Khipu receipt chains) supplies the provenance layer.

## 3. System under Test

**hatun-mcp** is a doctrine-aware MCP server exposing a read-only Streamable HTTP
surface at `/mcp/` with metadata endpoints (`/healthz`, `/connect`, server card).
Every tool invocation:

1. authenticates the client (API key → PBKDF2-SHA256 fingerprint → operator scope
   binding; anonymous requests are declined by construction);
2. applies the Yuyay-13 conjunctive input gate (a zero on any axis vetoes the call);
3. computes a per-client reputation factor in [0,1];
4. requires a second approver for state-changing operations;
5. calls the backend within a latency budget;
6. emits a Khipu receipt — a SHA-256 hash-chained record — on success *and* failure;
7. returns a DSSE-signed response carrying the receipt hash.

Deployment: Massed Compute A6000 node, Ubuntu 24.04, Python 3.12, uvicorn,
fronted by a Cloudflare tunnel at `https://mcp.a-11-oy.com`, with per-call x402
monetization ($0.10 general, $0.50 verified bots). The measurement client was
admitted through the operator scope-binding mechanism with a `read` scope.

## 4. Measurement Protocol

A *chain* is the ordered five-step sequence:

| Step | Operation | Success criterion |
|---|---|---|
| 1 | `initialize` (MCP handshake) | JSON-RPC result present |
| 2 | `tools/list` (discovery) | tool catalog returned |
| 3 | `tools/call` (governed invocation of `szl_formula_evaluate`) | tool result present |
| 4 | **receipt verification** | response contains receipt/DSSE hash material |
| 5 | `ping` | JSON-RPC result present |

A chain succeeds iff all five steps succeed. We report per-step success counts,
whole-chain success rate, and per-chain wall-clock latency. The protocol was
executed 10 times consecutively against the production server (loopback transport
to isolate the server from edge effects; the edge is measured separately in §6).

## 5. Results

### 5.1 First execution: the protocol finds what smoke tests miss

On first execution, whole-chain success was 0/10. Two distinct defects were
isolated and attributed by the protocol's per-step telemetry:

- **Host-pinning mismatch (HTTP 421).** The server pins the `Host` authority,
  including port. The allowlist contained `localhost` but the requests carried
  `localhost:8080`; every handshake and discovery step failed with 421 until the
  allowlist was corrected to match the authority-with-port contract.
- **Tool-argument schema mismatch (HTTP 403, `formula_not_admitted_for_http`).**
  The invocation used a plausible but wrong argument shape; the server's
  allowlist correctly refused it. Reading the tool's published `inputSchema` and
  correcting the client fixed the step.

Both defects were invisible to the single-call smoke checks previously run against
the same deployment (which exercised only `/healthz` and the index route). This is
the paper's central practical observation: **chain-level protocols with per-step
telemetry locate seam failures that endpoint-level checks cannot.**

### 5.2 Remediated runs

| Metric | Value |
|---|---|
| Chains attempted | 10 |
| Chains succeeded | **10 (100%)** |
| `initialize` | 10/10 |
| `tools/list` | 10/10 |
| `tools/call` (governed) | 10/10 |
| **receipt verification** | **10/10** |
| `ping` | 10/10 |
| Mean chain latency | **0.84 s** |

Every governed tool call in every chain carried verifiable receipt material; the
receipt-verification step passed 10/10. For comparison, the naive independence
arithmetic for five steps at 95% per-step reliability predicts 77.4% chain success;
the measured system's per-step and chain rates coincide at this sample size, and
we emphasize that **n = 10 bounds the strength of this claim** (see §7).

### 5.3 Burst-load latency (complementary measurement)

The co-located production inference server (estate-tuned 4B model, vLLM, A6000,
bfloat16, 2048-token context) was measured under a replay-style load mix: 43
requests across steady trickle, 8-concurrent bursts, and a mixed storm, with
prompt classes short / medium / long (~500-token prompts near the context limit).

| Prompt class | n | p50 | p95 | p99 | max | errors |
|---|---|---|---|---|---|---|
| Short | 14 | 1.18 s | 2.36 s | 2.36 s | 2.36 s | 0 |
| Medium | 14 | 2.95 s | 2.95 s | 2.95 s | 2.95 s | 0 |
| Long | 15 | 3.45 s | 3.77 s | 3.77 s | 3.77 s | 0 |
| **Overall** | **43** | **2.80 s** | **3.77 s** | **3.77 s** | **3.77 s** | **0** |

p99 is 34% above p50; no tail collapse under burst load; ~213 completion tokens per
call. We report p99 rather than the mean because the mean (2.51 s) understates the
user-felt tail by 50%.

## 6. Discussion

Three observations generalize beyond this deployment:

1. **Score the chain, and score provenance inside it.** Treating receipt
   verification as a first-class step converts provenance from a marketing
   property into a measured property. A system that cannot produce its receipts
   under measurement does not have them.
2. **The first run is the most informative run.** A chain protocol executed
   against a freshly deployed server found two real defects in under a minute,
   both of which had survived endpoint-level smoke testing. We recommend chain
   protocols as a standing deployment gate rather than a one-time benchmark.
3. **Report the tail.** The inference server's mean latency was unremarkable;
   its p99 is what a paying caller experiences under burst load.

## 7. Limitations

- **Sample size.** n = 10 chains and n = 43 load-test requests bound all
  statistical claims; 10/10 is consistent with any true per-chain reliability
  above ~69% at 95% confidence (rule of three). We report 100% as a measured
  rate over this sample, not as a system property.
- **Single system.** One server implementation, one deployment, one admitted
  test client with `read` scope. State-changing operations (two-person gate)
  were not exercised.
- **Loopback transport.** Chain measurements bypass the edge; the edge's bot
  challenge behavior on datacenter clients is a real operational consideration
  reported qualitatively, not measured here.
- **No external baseline.** We compare against the analytic 0.95⁵ chain
  arithmetic as a framing device, not against a measured competing system.

## 8. Conclusions

Whole-chain measurement with receipt verification as a scored step is cheap
(0.84 s per chain), operationally informative (it found two defects smoke testing
missed), and produces reliability claims that carry their own evidence. We release
all measurements as verbatim receipts and invite replication against any MCP server
that emits verifiable per-call provenance.

## Data Availability

All measurements are published verbatim (no aggregation beyond percentile
computation) in `SZLHOLDINGS/model-eval-receipts`:

- Chain test: `chain-test-mcp-2026-11-05.json` (`MEASURED_PRODUCTION_CHAIN`)
- Load test: `loadtest-inference-2026-11-05.json` (`MEASURED_PRODUCTION_LOAD`)
- Fleet probe evaluation: `fleet-eval-2026-11-05.json`

Server source: `szl-holdings/hatun-mcp` (Apache-2.0). Governance substrate:
`szl-holdings/szl-papers` (Ouroboros line; Doctrine v11, 749/14/163, Λ = Conjecture 1
disproved as stated; Theorem U conditional).

## References

1. Model Context Protocol specification — transport and lifecycle semantics.
2. DSSE: Dead Simple Signing Envelope, IETF. In-toto project.
3. SLSA: Supply-chain Levels for Software Artifacts, OpenSSF.
4. Lutar, S. P. Jr. Ouroboros thesis line, versions v1–v26; Doctrine v11 (749 Lean
   declarations / 14 axioms / 163 obligations). Zenodo concept DOI 10.5281/zenodo.19944926.
5. PURIQ: A Master Formula for Agentic AI under Provable Provenance. SZL Holdings preprint.

---

*Honesty note: this preprint reports measured rates over small samples, publishes its
failure modes (§5.1), and makes no capability claim beyond the receipts cited. Λ is
advisory; Conjecture 1 is machine-checked false as stated; nothing here depends on it.*
