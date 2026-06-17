# Contributing — SZL Papers

Thank you for your interest in the SZL Holdings academic corpus.

## Doctrine Constraints (READ FIRST)

All contributions must comply with **Doctrine v11 LOCKED** (749/14/163), kernel
commit `c7c0ba17`:

- Λ = **Conjecture 1** (conditional Theorem U) — NOT a closed theorem. Every
  paper, abstract, and preprint must cite it honestly.
- Khipu BFT = **Conjecture 2** (OPEN).
- SLSA L1 honest (NOT an L3 claim).
- Counts are canonical: **749 declarations · 14 axioms · 163 tracked sorries.**
  Do not introduce divergent counts; the overclaim guard will fail the build.

## What Belongs Here

| Directory | Contents |
|-----------|----------|
| `preprints/` | Preprints (PURIQ Λ-aggregator spec, etc.) |
| `thesis/` | Thesis lineage (Ouroboros receipt-DAG) |
| `bounty/` | Open mathematical bounty problems |
| `prior-art/` | Prior-art disclosures for IP protection |
| `papers/` | Published / submitted papers |

## How to Contribute

1. Fork the repository.
2. Create a branch (`git checkout -b paper/your-topic`).
3. Add or edit sources under the correct directory; keep LaTeX build artifacts
   out of git (they are `.gitignore`d).
4. Update `PAPERS_INDEX.md` / `CITATION.cff` if you add a citable artifact.
5. Commit with a DCO sign-off and open a Pull Request.

## DCO Sign-off

All commits require a DCO sign-off trailer:

```bash
git commit --signoff -m "your message"
```

This certifies the [Developer Certificate of Origin](https://developercertificate.org).

## Honesty Review

The `overclaim / Governed surfaces are honest (Theorem U citation rule)` check is
a required gate. Any claim about Λ, Khipu BFT, or SLSA level must be cited
conditionally and consistently with the canonical counts above.

---

© 2026 Lutar, Stephen P. — SZL Holdings · Text/figures CC-BY-4.0 unless noted.
