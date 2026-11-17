# SZL Holdings | Investor and developer evidence brief

*2026-11-17 · 19:59 UTC snapshot · Public source links with explicit release limits*

**Positioning:** SZL builds Python-first, proof-carrying AI infrastructure.
GitHub is the source authority; Hugging Face hosts models and demonstrations;
Cloudflare presents product and API interfaces; PyPI distributes reusable Python
components. None of these layers automatically certifies another.

## What the receipts establish

| Layer | Verified now | Independent evidence | Remaining production gate |
| --- | --- | --- | --- |
| Python + GitHub | The `szl-gov` source-controlled x402 POST witness passed focused tests, was merged and can build as an importable wheel. | [Merged #38](https://github.com/szl-holdings/szl-gov/pull/38), [source witness](https://github.com/szl-holdings/szl-gov/blob/main/tools/x402_post_method_watch.py), [developer method](https://github.com/szl-holdings/szl-gov/blob/main/docs/X402_POST_METHOD_WITNESS.md) | Tests/builds prove source behavior only; they do not establish payment settlement or deployed inference. |
| Five-organ runtime (isolated kind CI) | All 5/5 organ signatures, deployment readiness checks and /healthz endpoints passed on [run 44160741070](https://github.com/szl-holdings/szl-build-env/actions/runs/44160741070). | [Source and provenance repair #45](https://github.com/szl-holdings/szl-build-env/pull/45) | Exact fan-out returned HTTP 503 with `TRACING_NOT_CONFIGURED`; fresh Jaeger five-service trace unavailable; isolated fix [#46](https://github.com/szl-holdings/szl-build-env/pull/46) requires CI, not a production exemption. |
| Cloudflare public pricing | The operator's bounded GET witness observed both free product/proof surfaces HTTP 200 and paid chat/inference GET challenges HTTP 402. Two unsigned, deliberately invalid **POST** calls also returned x402 v2 HTTP 402 and matched dated public price terms. | [x402 POST witness](https://github.com/szl-holdings/szl-gov/blob/main/tools/x402_post_method_watch.py), [pricing catalog](https://github.com/szl-holdings/szl-gov/blob/main/pricing/README.md) | Provider rule readback, actual payment authorization, paid-model fulfillment, facilitator settlement, on-chain reconciliation and net revenue are **UNVERIFIED**. A 402 is not a sale. |
| Hugging Face / product UI | [A11oy Space](https://huggingface.co/spaces/SZLHOLDINGS/a11oy) was RUNNING during the owner's 2026-11-17 inspection; public `/api/build-info` identified deployed source `531dcb16f7c8f030bb86cba0f28aae7244c7ea02`. | [A11oy protected GitHub source](https://github.com/szl-holdings/a11oy), [HF synchronization run 44161642686](https://github.com/szl-holdings/a11oy/actions/runs/44161642686) | Later main revisions differed from live source. `SOURCE_AHEAD`; the workflow correctly blocked deployment because the maintenance window was closed. A running Space does not mean live source parity, signed-release readiness or HF source convergence. |
| Python packaging / PyPI | `szl-gov==0.1.0` built sdist + wheel; strict Twine, isolated installation, metadata and import checks passed. Source-owned OIDC-only release workflow merged. | [Trusted publisher #41](https://github.com/szl-holdings/szl-gov/pull/41), [release admission](https://github.com/szl-holdings/szl-gov/blob/main/docs/PYPI_RELEASE_ADMISSION.md) | Public `szl-gov` PyPI JSON returned HTTP 404; pending publisher and protected `pypi` GitHub environment must be configured. **NOT PUBLISHED.** |
| Research | Source papers, conjectures, Lean snapshots and evidence scope are separately documented, with preprint metadata and claims reviewed by domain-specific gates. | [Public SZL Papers index](https://github.com/szl-holdings/szl-papers/blob/main/PAPERS_INDEX.md), [claim contract](https://github.com/szl-holdings/szl-papers/blob/main/metadata/locked-claim-contract.json) | A preprint is not peer review, and a source math check is not automatic deployment, model validation or a clinical result. |

## Developer verification: reproducible public workflow

```bash
git clone https://github.com/szl-holdings/szl-gov.git
cd szl-gov
python -m pytest -q tests/test_x402_post_method_watch.py
python -m build --wheel
python -m twine check dist/*.whl

# Optional, opt-in, exactly two intentionally invalid public POSTs:
python tools/x402_post_method_watch.py --execute \
  --catalog pricing/generated/x402-pricing.json \
  --output /secure/local/x402-post-readback.json
```

The last command uses no wallet, cookies, signatures or settled transaction,
and its output reports `settlement: UNVERIFIED` and `revenue: NO_CLAIM`.
The source allows no user-selected URLs and does not follow redirects.

## Investor due-diligence checklist

Source checks, runtime checks, signed-image provenance, Cloudflare payment
challenge, paid fulfillment, settlement, PyPI Trusted Publishing and research
publication are **separate admission gates**. For a transaction-related claim
ask for the exact source SHA, current deployed digest, payload-free payment
challenge summary, authenticated settlement transaction, receiving-wallet
readback and reconciliation. For a model-evaluation claim require immutable
run inputs, independent held-out evaluation and the exact public/private
evidence boundary.

**No revenue, production release, full source parity or publication success is
asserted from the checks above.** This status brief records the known facts and
their limitations; historical investor collateral below must be interpreted
against its dated scope, not treated as a live estate-wide attestation.
