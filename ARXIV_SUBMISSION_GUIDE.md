# arXiv Submission Guide — SZL Holdings Thesis Line

**Prepared:** 2026-07-15 · **Founder:** Stephen P. Lutar Jr., ORCID [0009-0001-0110-4173](https://orcid.org/0009-0001-0110-4173)

> **Important:** An agent cannot submit to arXiv. arXiv requires a logged-in human submitter (and, for first-time submitters in some categories, an endorsement). This guide recommends two distinct, self-contained LaTeX packages and gives the exact field values to paste. **No paper here is posted to arXiv; do not represent either as posted until you complete the steps below.** A Zenodo concept DOI ([10.5281/zenodo.19944926](https://doi.org/10.5281/zenodo.19944926)) already exists for the broader program and can be cross-referenced as related work, not as either paper's DOI.

---

## The two recommended submission packages

All packages live in this repository under `thesis/arxiv/`.

| Paper | Folder | Files | Primary / cross-list |
|-------|--------|-------|----------------------|
| **P1** Verifiable Append-Only Governance | `thesis/arxiv/append-only-governance/` | `main.tex`, `references.bib`, `ARXIV_METADATA.md` | **cs.LO** / cs.CR, cs.DC, cs.LG |
| **P2** Graph-Shaped Governance Audit | `thesis/arxiv/graph-substrate/` | `main.tex`, `references.bib`, `ARXIV_METADATA.md` | **cs.LO** / cs.LG, cs.DM |

Each `ARXIV_METADATA.md` contains the ready-to-paste **title, author, abstract, categories, ACM/MSC class, license, and comments** for that paper. The older GPD v26 package remains repository source material but is deliberately **not** part of this two-paper submission wave: it overlaps the umbrella thesis line and should wait until P1/P2 have identifiers and an independent claim review.

---

## Step 0 — Compile each package locally (sanity check)

No special document class is used; the packages rely on standard `article` plus `amsmath, amssymb, amsthm, booktabs, array, longtable, tabularx, listings, xcolor, hyperref, geometry, placeins, multicol, microtype`.

```bash
cd thesis/arxiv/<paper>
tectonic main.tex     # or run pdflatex twice
```

The bibliographies are inlined, so BibTeX is not required. Both papers were compiled with Tectonic 0.16.9 and visually reviewed page by page on 2026-07-15. P1 is 20 pages with no overfull boxes or undefined references; P2 is 23 pages with no overfull or underfull boxes and no undefined citations or references. If a compiler is unavailable locally, upload the package sources to arXiv and inspect arXiv's generated PDF before submission.

---

## Step 1 — Log in / register at arXiv

1. Go to <https://arxiv.org/> and sign in (or create an account).
2. Link your **ORCID 0009-0001-0110-4173** under *Account → ORCID*.
3. First-time submitters to `cs.LO`/`cs.LG`/`cs.CR` may need an **endorsement**. If prompted, request one from a colleague already publishing in that category, or submit to a category where you are auto-endorsed. arXiv shows the endorsement code/instructions inline.

## Step 2 — Start a new submission

1. <https://arxiv.org/submit> → *Start a New Submission*.
2. **License:** select **CC BY 4.0** (matches the package headers).
3. **Submission type:** *New paper*.

## Step 3 — Upload files

1. Upload `main.tex` and `references.bib` from the paper's `arxiv/` folder (do **not** upload the `.md` or `ARXIV_METADATA.md` — they are not part of the build).
2. Let arXiv process/compile. Review the generated PDF.
3. If you have a precompiled `figures/` set, add it — these papers use no external figures.

## Step 4 — Fill metadata (copy from the paper's `ARXIV_METADATA.md`)

- **Title** — copy verbatim.
- **Authors** — `Stephen P. Lutar Jr.` ; affiliation `SZL Holdings, Inc.` ; ORCID `0009-0001-0110-4173`.
- **Abstract** — paste the "Abstract (ready to paste)" block.
- **Primary category** and **cross-list categories** — as in the table above.
- **ACM-class** and **MSC-class** — from the metadata file.
- **Comments** — paste the suggested comments line (page count, Lean/Mathlib note, `locked_count_eight`, concept DOI, repo).
- **Report-no / Journal-ref / DOI** — leave these blank for a new submission. The umbrella concept DOI `10.5281/zenodo.19944926` identifies the broader program, not either individual paper, and should not be entered as the paper DOI.

## Step 5 — Review and submit

1. Verify the compiled PDF renders the abstract, all theorem environments, the tables, and the `lstlisting` verification block.
2. Submit. arXiv assigns an identifier **only after moderation** (often the next business day). **Until you see a real `arXiv:YYMM.NNNNN`, do not cite or claim an arXiv ID anywhere** — the doctrine forbids fabricating one.

## Step 6 — After acceptance

- Add the assigned arXiv ID back into `szl-papers` (`PAPERS_INDEX.md`, `THESIS_LINEAGE.md`) and the paper's `ARXIV_METADATA.md`.
- If no paper-specific Zenodo record exists, create or reserve exactly one; otherwise update and relate that same record. Add only that paper-specific DOI to the `.tex` thanks footnote.

---

## Suggested submission order

1. **P1 (Append-Only Governance)** — the cleanest locked-registry result, now with an explicit distinction between the `c7c0ba17` canonical-count baseline and the `5cfaf9a3…` proof snapshot.
2. **P2 (Graph Substrate)** — broad `cs.LG` reach, provided the submission retains the artifact audit's experimental-tier and topology-blindness disclosures.

## Honesty checklist (must hold before you submit each paper)

- [ ] Locked-proven count stated as **exactly 8** {F1,F4,F7,F11,F12,F18,F19,F22}, certified by `locked_count_eight`.
- [ ] **Conjecture 1 is disproved as stated**; conditional **Theorem U** is proven and only the weaker-condition uniqueness question remains open.
- [ ] Khipu BFT safety = **Conjecture 2** (Wave-23 conditional agreement only).
- [ ] Experimental (~185, Waves 11–23) clearly labeled and never folded into the locked eight.
- [ ] No fabricated benchmarks, citations, or arXiv IDs; GPD grounded only in SZL Zenodo DOIs.
- [ ] Trust never reported as 100%.

## Zenodo strategy (avoid duplicate DOIs)

Do not mint another DOI for SZL Thesis v8: the published record is [10.5281/zenodo.21184984](https://doi.org/10.5281/zenodo.21184984), under concept DOI [10.5281/zenodo.20567256](https://doi.org/10.5281/zenodo.20567256). The public umbrella concept [10.5281/zenodo.19944926](https://doi.org/10.5281/zenodo.19944926) currently resolves to the v21 thesis record and is not a paper-specific identifier for P1 or P2.

For P1 and P2, first complete the final human/arXiv metadata review. Then create one Zenodo concept per paper (or reserve each paper DOI immediately before submission), upload the exact reviewed PDF/source bundle, and relate the record to its eventual arXiv identifier. If arXiv assigns an identifier first, add it to the existing Zenodo record/version rather than creating a second deposit for the same paper. Never reuse the program concept DOI in arXiv's paper DOI field.
