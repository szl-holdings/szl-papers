# arXiv Submission Guide — SZL Holdings Thesis Line

**Prepared:** 2026-06-10 · **Founder:** Stephen P. Lutar Jr., ORCID [0009-0001-0110-4173](https://orcid.org/0009-0001-0110-4173)

> **Important:** An agent cannot submit to arXiv. arXiv requires a logged-in human submitter (and, for first-time submitters in some categories, an endorsement). This guide gives you three complete, self-contained LaTeX packages and the exact field values to paste. **No paper here is posted to arXiv; do not represent any as posted until you complete the steps below.** A Zenodo concept DOI ([10.5281/zenodo.19944926](https://doi.org/10.5281/zenodo.19944926)) already exists for the program and can be cross-referenced.

---

## The three submission-ready packages

All packages live in `/home/user/workspace/team/theses/` and are mirrored in the `szl-papers` repo under `thesis/arxiv/`.

| Paper | Folder | Files | Primary / cross-list |
|-------|--------|-------|----------------------|
| **P1** Verifiable Append-Only Governance | `theses/append-only-governance/arxiv/` | `main.tex`, `references.bib`, `ARXIV_METADATA.md` | **cs.LO** / cs.CR, cs.DC, cs.LG |
| **P2** Kernel-Verified Graph Substrate | `theses/graph-substrate/arxiv/` | `main.tex`, `references.bib`, `ARXIV_METADATA.md` | **cs.LG** / cs.LO, cs.DM, stat.ML |
| **P3** Governed Post-Determinism (v26) | `theses/gpd-v26/arxiv/` | `main.tex`, `references.bib`, `ARXIV_METADATA.md` (+ source `unified-gpd-thesis-v26.md`) | **cs.LO** / cs.CR, cs.LG, math.OC |

Each `ARXIV_METADATA.md` contains the ready-to-paste **title, author, abstract, categories, ACM/MSC class, license, and comments** for that paper.

---

## Step 0 — Compile each package locally (sanity check)

No special document class is used; only standard `article` + `amsmath, amssymb, amsthm, booktabs, array, longtable, listings, xcolor, hyperref, geometry`.

```bash
cd theses/<paper>/arxiv
pdflatex main.tex
bibtex main          # references are also inlined; bibtex is optional
pdflatex main.tex
pdflatex main.tex    # resolve cross-refs / ToC
```

If a compiler isn't installed locally, upload the `.tex` + `.bib` directly to arXiv — arXiv compiles server-side with TeX Live. The packages passed a structural brace/environment balance check (`/tmp/texcheck.py`): P1 and P2 balance exactly; P3 balances once escaped `\%` is accounted for (validator artifact only — the LaTeX is correct).

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
- **Report-no / Journal-ref / DOI** — leave Journal-ref blank; you may put the Zenodo concept DOI `10.5281/zenodo.19944926` in the **DOI** field to cross-link the program deposit.

## Step 5 — Review and submit

1. Verify the compiled PDF renders the abstract, all theorem environments, the tables, and the `lstlisting` verification block.
2. Submit. arXiv assigns an identifier **only after moderation** (often the next business day). **Until you see a real `arXiv:YYMM.NNNNN`, do not cite or claim an arXiv ID anywhere** — the doctrine forbids fabricating one.

## Step 6 — After acceptance

- Add the assigned arXiv ID back into `szl-papers` (`PAPERS_INDEX.md`, `THESIS_LINEAGE.md`) and the paper's `ARXIV_METADATA.md`.
- Optionally mint/attach a versioned Zenodo DOI for the specific paper and add it to the `.tex` thanks footnote.

---

## Suggested submission order

1. **P1 (Append-Only Governance)** — the cleanest fully-locked result; strongest first impression and lowest moderation risk (all claims kernel-verified).
2. **P2 (Graph Substrate)** — broad `cs.LG` reach; ties to the GNN expressivity/position-aware lineage (You, Xu/GIN, graph2nn, Polymathic, McLeish) cited strictly as related work.
3. **P3 (GPD v26)** — the unification thesis; references P1/P2 results as pillars. Submit after P1/P2 so you can cross-cite their arXiv IDs once assigned.

## Honesty checklist (must hold before you submit each paper)

- [ ] Locked-proven count stated as **exactly 8** {F1,F4,F7,F11,F12,F18,F19,F22}, certified by `locked_count_eight`.
- [ ] Λ uniqueness = **Conjecture 1** (machine-checked FALSE); only **Theorem U** is the proven conditional.
- [ ] Khipu BFT safety = **Conjecture 2** (Wave-23 conditional agreement only).
- [ ] Experimental (~185, Waves 11–23) clearly labeled and never folded into the locked eight.
- [ ] No fabricated benchmarks, citations, or arXiv IDs; GPD grounded only in SZL Zenodo DOIs.
- [ ] Trust never reported as 100%.
