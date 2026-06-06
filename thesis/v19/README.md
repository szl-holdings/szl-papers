# Thesis v19 — The Verification Bridge

**Ouroboros Thesis v19.0** — the honest consolidation of the multi-track substrate
expansion (v18) into a **per-theorem verified index**, on the path from substrate
expansion to the formally-verified anatomy (v20).

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19944926.svg)](https://doi.org/10.5281/zenodo.19944926)

> Concept DOI `10.5281/zenodo.19944926` always resolves to the latest version. The
> **v19 version DOI is minted by Zenodo when the `thesis-v19.0.0` GitHub release is
> published** (Zenodo↔GitHub webhook). **FOUNDER ACTION.**

**Author:** Stephen P. Lutar Jr. · ORCID [0009-0001-0110-4173](https://orcid.org/0009-0001-0110-4173)
· SZL Holdings · **Date:** 2026-05-31 · License: CC BY 4.0 (paper), Apache-2.0 (code).

| File | Description |
|---|---|
| [`main.tex`](./main.tex) | Canonical arXiv-style LaTeX source (v19.0) |
| [`main.md`](./main.md) | Markdown rendering of the thesis text |
| [`main.pdf`](./main.pdf) | Typeset PDF (embedded fonts, honest-posture banner) |
| [`refs.bib`](./refs.bib) | BibTeX bibliography (real citations with DOIs) |

## What this version is

v19 fills the previously-documented **v18 → v20 gap** *honestly*. For a period the
lineage jumped from v18 ("Multi-Track Substrate Expansion") straight to v20 ("The
Culmination"), with the v19 slot annotated as an intentional gap. This paper records
the work that actually happened in that window and that was, at the time, folded
silently into the v20 consolidation: **verification consolidation**.

- **The per-theorem verified index** — a per-file `(sorry, axiom, theorem)` ledger over
  the v18 corpus and the 2026-05-30 expansion track, read verbatim from the corpus
  index (`lean_per_version.json`). Every claim carries an explicit, machine-checkable
  status: kernel-verified, sorry-free fragment, axiom-gated, or open.
- **Locked-vs-experimental scope separation** — a strict boundary between the locked
  kernel (749/14/163 @ `c7c0ba17`) and the experimental expansion corpus.
- **The drift gate** — a CI invariant that the locked declaration/axiom/sorry counts do
  not move when experimental modules are added. This is the bridge made executable.
- **The honesty doctrine as acceptance criterion** — inherited verbatim from v14 and
  carried forward to v23.

## What this version is NOT

v19 claims **no new proven mathematics**. It closes no `sorry` that was not already
closed; its contribution is **accounting and scope discipline**, not new theorems. Of
the nineteen 2026-05-30 expansion-track modules indexed here, exactly **one**
(`Putnam/P_A3`) is fully sorry-free; the rest carry honestly-recorded open obligations.

## Honest posture (load-bearing)

- The **Lutar invariant Λ is Conjecture 1 — unconditionally, NEVER a theorem.** v19
  preserves the label only; the machine-checked refutation of *unconditional* uniqueness
  and the *conditional* theorem under a declared block-consistency axiom are later
  (Wave-2–Wave-4) results reported in v22/v23.
- **Locked / proven = 5:** `{F1 replay determinism, F11 Ayni reciprocity, F12 Kuramoto
  additive, F18 Reed–Solomon RS(10,6), F19 Bekenstein additive}`. F12 and F19 prove only
  the **additive scaffolding** fragments, never the full physical theorems.
- **Disclosed idealizations:** where a proof needs cryptographic hardness it declares a
  named axiom (e.g. the SHA-256 collision-resistance axioms in `TH_V18_14`) and discloses
  it in the `#print axioms` ledger; it does not pretend to prove hardness.
- **SLSA L1 + L2 attested; NOT L3.**
- **Open is open.** A `sorry` is reported as a `sorry`; a fragment as a fragment.

## Doctrine v11 (LOCKED @ `c7c0ba17`)

**749 declarations · 14 unique axioms · 163 sorries (112 baseline + 51 Putnam).**

## Lineage

v18 (expand) → **v19 (consolidate & verify — this paper)** → v20 (verified anatomy) →
v21 (PURIQ-OS runtime) → v22 (convergence) → v23 (unified substrate). v19 is the hinge
on which expansion turns into verified anatomy.

---

*Signed-off-by:* Stephen P. Lutar Jr. `<stephenlutar2@gmail.com>`
Co-authored with the SZL full-stack PhD team (mathematics, scientific writing, CS, ML,
philosophy of mathematics).
