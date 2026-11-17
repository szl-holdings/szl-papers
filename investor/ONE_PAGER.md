# SZL Holdings

**Governed AI built for independent verification — signed receipts where signing is admitted, explicit holds and honest unsigned states elsewhere.**

We'd rather you verify than take our word for it. The [current investor and developer evidence brief](RELEASE_EVIDENCE_BRIEF_2026-11-17.md) separates source checks, runtime readbacks, Cloudflare payment challenges, PyPI releases and publications. Claims in this historical one-pager that cite private or dated sources are not independently current.

---

## The problem

AI systems make consequential decisions — who to contact, what to approve, what to flag — and when someone asks *"why, and can you prove it?"*, the honest answer today is usually no. The leading AI-governance and intent-data platforms output a score or a verdict with **no verifiable provenance**: you cannot independently confirm which policies ran, what the verdict was, which model produced it, or that nothing was fabricated.

For anyone operating under real accountability — regulated sales, finance, defense-adjacent, compliance — that gap is the difference between "interesting" and "usable."

## What we built

A governed-AI substrate designed to attach independently verifiable cryptographic receipts to admitted operations. Supported receipts can be checked offline with ECDSA-P256 verification; if a signing key is absent or a runtime gate blocks an action, the system must report **unsigned, blocked or unavailable**, not fabricate a verified receipt.

Our differentiation is a source-owned, receipt-first assurance chain that treats observation, policy enforcement, cryptographic verification and production admission as distinct claims. Individual capabilities are supported by the linked receipts and tests, not by blanket comparisons to competitors.

## The product you can run right now

**`szl-router`** — source for a sovereign, OpenAI-compatible LLM gateway. Receipt headers must be independently verified for each admitted response; missing signing authority or an unavailable runtime cannot be described as a successfully signed answer. The example below is a developer build recipe, not a verified live-production deployment:

```
git clone https://github.com/szl-holdings/szl-router && cd szl-router
docker build -t szl-router . && docker run -p 8000:8000 -e GROQ_API_KEY=... szl-router
```

(A prebuilt image is also published to `ghcr.io/szl-holdings/szl-router`.)

Product surfaces include **a11oy** (governed-AI Command Center), **David Leads**, **killinchu**, and the **anatomy** visual workspace. Their source availability, hosting state, fresh runtime revision and public-access state must each be verified independently; a GitHub passing build is not evidence that all are live or public.

## Why it holds up

- **Explicit data boundaries.** Public research examples and source code are distinguishable from authorized private datasets, model weights and protected clinical or partner information. Blocked evidence never becomes verified through averaging.
- **Open and checkable where published.** Source repositories, machine-checkable proof fragments and CI receipts can be inspected independently; the estate is not claimed universally green. The core scoring conjecture is not overstated as an unconditional theorem.
- **Sovereign.** Runs on your own metal; nothing has to leave your environment.

## Historical traction reports (not current independently verified adoption)

Earlier reports described public dataset downloads, live application demos and repository growth. They are retained as historical program context, **not** a current verified customer, revenue, availability or all-green-CI metric. Use dated provider analytics and runtime readbacks before treating them as traction.

### Production, measured (November 2026 — each line names its source and says when that source is not yet public)

- **x402 pay-per-call rules are enabled on 7 machine-API path prefixes:** 4 Cloudflare Monetization Gateway rules on a-11-oy.com, $0.02–$0.05 per call, and none on a11oy.net; on 4 of the 7 prefixes the rules charge only Cloudflare-verified bots (source: the gateway's rule configuration as of 2026-11-06 16:27 UTC, which is not public). The exported rules name no HTTP method and the gateway's documented default charges only `GET` requests, so the dated **rule export alone** cannot certify `POST`. A separate [source-owned unsigned POST challenge witness](https://github.com/szl-holdings/szl-gov/blob/main/docs/X402_POST_METHOD_WITNESS.md) observed x402 v2 HTTP 402 on chat and completions POST endpoints on November 17, 2026; that establishes challenge delivery only, not successful charging or settlement. **Settled revenue to date: not yet reconciled.** Nothing reconciles gateway settlements yet, so we state no revenue figure. An HTTP 402 is a payment request, not a sale, so we do not count 402 responses as traction. We publish no request-volume figure until we can attach the analytics export behind it.
- **Production inference measured under burst load:** p99 = 3.77 s, 0 errors in 43 requests including 8-concurrent bursts and near-context-limit prompts (receipt for the latency and error figures: `SZLHOLDINGS/model-eval-receipts/loadtest-inference-2026-11-05.json`; that dataset is still private, so this receipt is not yet public. The burst and prompt-length mix is described in §5.3 of P3, listed below, and is not recorded in the receipt).
- **Governed MCP tool server measured at the chain level:** 10/10 five-step chains succeeded with cryptographic receipt verification as a scored step (0.84 s mean chain latency) — the first execution caught two real configuration defects that single-call smoke testing missed (receipt: `chain-test-mcp-2026-11-05.json`, in the same private dataset; not yet public).
- **Two DOI-minted preprints** on Zenodo, derived from measured production data: 
  P3 *Receipt-Attached Reliability* — [10.5281/zenodo.24025910](https://doi.org/10.5281/zenodo.24025910); 
  P4 *Honest Abstention Transfer* — [10.5281/zenodo.24025916](https://doi.org/10.5281/zenodo.24025916).
- **Academic collaboration:** co-authorship on a certified-unique-puzzle benchmark paper (Behnamian, Lund/KU), contributing the small-open-weights size point and a certified-reasoning training corpus (`SZLHOLDINGS/reasoning-puzzles-sft-v1`).
- **A model trained on certified reasoning data:** the first estate fine-tune whose chain-of-thought ground truth is solver-extracted (formally verified minimal clue sets), not model-invented rationale (source: the `SZLHOLDINGS/SZL-Reasoning-0.8B-v1` model card).

### Theory preprints (formal arguments, not production measurements)

- **Three DOI-minted theory preprints** (not peer reviewed). They report no production measurements:
  P5 *Free-Energy Certification* (the PAC-Bayes bound read as a free-energy decomposition, with a conditional Lean bound) — [10.5281/zenodo.24025918](https://doi.org/10.5281/zenodo.24025918);
  P6 *Information-Thermodynamic Certification* (Landauer, Bekenstein and PAC-Bayes stated as one principle) — [10.5281/zenodo.24025920](https://doi.org/10.5281/zenodo.24025920);
  P7 *Schur-Concavity as a Falsifiable Physics Prediction* (a Lean-proved lemma and an untested physics hypothesis) — [10.5281/zenodo.24025922](https://doi.org/10.5281/zenodo.24025922).

### The honest-failure differentiator

We publish our models' failures verbatim, next to the wins: the eval receipts include the exact sentences where our estate model fabricated citations, and the papers analyze the failure mode. Our honesty doctrine is machine-checked where possible and receipts-first everywhere — a technical due-diligence team can verify the claims on this page from public artifacts, including the ones that make us look unfinished; a line whose source is not yet public says so.

## Verify our claims in ~5 minutes

1. **Run the gateway and inspect a signed receipt:**
   `git clone https://github.com/szl-holdings/szl-router && cd szl-router && docker build -t szl-router . && docker run -p 8000:8000 -e GROQ_API_KEY=... szl-router`
   Point an OpenAI client at `http://localhost:8000/v1`; read the `x-szl-receipt` header; the server logs its public key on boot.
2. **Verify it independently:** `POST /v1/receipt/verify` (or `python -m szl_router.verify`). Tamper with one byte — verification fails.
3. **The 60-second proof:** `python szl-receipt/examples/governed_ai_you_can_prove.py` — mints a signed decision, verifies it, shows a tampered copy fail, and shows a keyless receipt stay honestly unsigned. Ends with `PROOF OK`.
4. **Product demos:** verify the current version, runtime stage and access directly before describing the IMMUNE or David Leads demos as live; a source page or historical screenshot is not current availability.

---

*Prepared by SZL Holdings · public-data only · honest by design · © 2026. Independent verification is the point: where a source on this page is not yet public, its line says so.*
