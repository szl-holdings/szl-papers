# SZL Holdings

**Governed AI you can prove — every decision comes with a signed, verifiable receipt, built on public data, running on your own hardware.**

We'd rather you verify than take our word for it. Every claim below is something you can check yourself in a few minutes. Links and commands are at the end.

---

## The problem

AI systems make consequential decisions — who to contact, what to approve, what to flag — and when someone asks *"why, and can you prove it?"*, the honest answer today is usually no. The leading AI-governance and intent-data platforms output a score or a verdict with **no verifiable provenance**: you cannot independently confirm which policies ran, what the verdict was, which model produced it, or that nothing was fabricated.

For anyone operating under real accountability — regulated sales, finance, defense-adjacent, compliance — that gap is the difference between "interesting" and "usable."

## What we built

A governed-AI substrate where **every decision emits a cryptographically signed receipt** that anyone can verify independently — offline, on their own hardware, with standard open tools (`cosign`-compatible ECDSA-P256). If a single byte is altered, verification fails. If no signing key is present, the receipt is honestly marked *unsigned* — it never reports a false "verified."

We reviewed the field leaders (governance/guardrails, observability, attested compute, agent runtimes, sovereign serving) and confirmed: a signed, verifiable per-decision receipt is the one capability none of them ship. It is our wedge, and it is working today.

## The product you can run right now

**`szl-router`** — a sovereign, OpenAI-compatible LLM gateway. Point any OpenAI client at it; every answer returns a signed receipt header recording which model served it, on whose hardware, and at what tier. Build and run from the public source in two commands:

```
git clone https://github.com/szl-holdings/szl-router && cd szl-router
docker build -t szl-router . && docker run -p 8000:8000 -e GROQ_API_KEY=... szl-router
```

(A prebuilt image is also published to `ghcr.io/szl-holdings/szl-router`.)

Built on it: **a11oy** (the governed-AI Command Center), **David Leads** (compliant insurance lead intelligence), **killinchu** (edge sensor analytics), **anatomy** (a navigable 3D view of the system). All live, all public.

## Why it holds up

- **Public data only. Nothing private, nothing invented.** Honesty is enforced in the math, not promised in marketing — a non-compliant decision is *structurally* removed, it can't be averaged back in.
- **Open and checkable.** 33 public repositories, machine-checkable proofs, CI-enforced tests. The core scoring claim is published as an open conjecture (advisory), not overstated as a theorem.
- **Sovereign.** Runs on your own metal; nothing has to leave your environment.

## Traction signals (verifiable)

- **12,400+ downloads** of one of our public datasets (killinchu OSINT corpus) — adoption we did not market.
- **Multiple live, running applications** (a11oy, David Leads, killinchu, anatomy, IMMUNE demo) — not slideware.
- **33 public repositories** with passing CI and signed releases.

## Verify our claims in ~5 minutes

1. **Run the gateway and inspect a signed receipt:**
   `git clone https://github.com/szl-holdings/szl-router && cd szl-router && docker build -t szl-router . && docker run -p 8000:8000 -e GROQ_API_KEY=... szl-router`
   Point an OpenAI client at `http://localhost:8000/v1`; read the `x-szl-receipt` header; the server logs its public key on boot.
2. **Verify it independently:** `POST /v1/receipt/verify` (or `python -m szl_router.verify`). Tamper with one byte — verification fails.
3. **The 60-second proof:** `python szl-receipt/examples/governed_ai_you_can_prove.py` — mints a signed decision, verifies it, shows a tampered copy fail, and shows a keyless receipt stay honestly unsigned. Ends with `PROOF OK`.
4. **The live demos:** the IMMUNE investor demo and David Leads run in the browser today.

---

*Prepared by SZL Holdings · public-data only · honest by design · © 2026. Everything in this page is independently verifiable — that is the point.*
