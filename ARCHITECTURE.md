# Architecture — szl-papers

> Doctrine v11 LOCKED `749/14/163` · Kernel commit `c7c0ba17` · Λ = **Conjecture 1**
> (conditional Theorem U) · Khipu BFT = **Conjecture 2** (OPEN) · SLSA L1 honest.

`szl-papers` is the SZL Holdings **academic corpus** — preprints, thesis lineage,
bounty problems, and prior-art disclosures. It is a documents-and-sources repository,
not a runtime service.

## Repository layout

```
szl-papers/
├── preprints/              Preprints (e.g. PURIQ — Λ-aggregator formal spec).
├── thesis/                 Thesis lineage (Ouroboros receipt-DAG).
├── bounty/                 Open mathematical bounty problems (Λ-conjecture).
├── prior-art/              Prior-art disclosures for IP protection.
├── papers/                 Published / submitted papers.
├── branding/               Shared figures / brand assets.
├── PAPERS_INDEX.md         Index of all citable artifacts.
├── ARXIV_SUBMISSION_GUIDE.md
└── CITATION.cff            Citation metadata.
```

## Source-of-truth relationship

Every mathematical claim in this corpus is anchored to **lutar-lean**, the Lean 4 +
Mathlib formalization that holds the machine-checked proofs. The honesty contract:

- **Λ** is cited as **Conjecture 1**, conditional on Theorem U — never as a closed
  theorem.
- **Khipu BFT** is cited as **Conjecture 2 (OPEN)**.
- Canonical counts are **749 declarations · 14 axioms · 163 tracked sorries**, kernel
  commit `c7c0ba17`. Divergent counts are not permitted.
- SLSA is claimed at **L1 honest**, never higher.

## CI gates (required on `main`)

`overclaim / Governed surfaces are honest (Theorem U citation rule)` — the honesty
gate that enforces conditional citation of Λ / Khipu BFT and consistency with the
canonical counts. Pin-check and CodeQL also run.

## Licensing

Text and figures are CC-BY-4.0 unless otherwise noted (see `LICENSE`).

---

© 2026 Lutar, Stephen P. — SZL Holdings
