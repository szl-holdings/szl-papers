---
license: apache-2.0
tags:
- mathematics
- formal-verification
- thesis
- ouroboros-invariant
- szl-holdings
- doi:10.5281/zenodo.19944926
- doi:10.5281/zenodo.20434276
task_categories:
- text-generation
- other
pretty_name: SZL Holdings Thesis Corpus v18
size_categories:
- n<1K
language:
- en
configs:
- config_name: formal-blocks
  data_files:
  - split: train
    path: formal_blocks_179.csv
- config_name: version-ledger
  data_files:
  - split: train
    path: per_version_delta_ledger.csv
---

<!-- szl:card-presentation:v1 -->
<p><a href="https://huggingface.co/SZLHOLDINGS"><img src="https://raw.githubusercontent.com/szl-holdings/szl-brand/fd62fe5856ed8e5f660eaae5a9c52957cd71b0a7/kit/logos/orbit-v2/suite/szl-icon-32.svg" width="40" height="40" alt="SZL Holdings" /></a></p>

[Dataset files](https://huggingface.co/datasets/SZLHOLDINGS/thesis-corpus-v18/tree/main) · [SZL catalog](https://huggingface.co/SZLHOLDINGS) · [Proof and documentation](https://a11oy.net/)

Orbit artwork: Stephen P. Lutar / SZL Holdings · [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) · [Native source](https://github.com/szl-holdings/szl-brand/tree/fd62fe5856ed8e5f660eaae5a9c52957cd71b0a7/kit/logos/orbit-v2) · [Trademark notice](https://github.com/szl-holdings/szl-brand/blob/fd62fe5856ed8e5f660eaae5a9c52957cd71b0a7/NOTICE). Dataset rights remain as declared in its original metadata and documentation.
<!-- /szl:card-presentation:v1 -->

<div align="center">
<p>

[![dataset](https://img.shields.io/badge/dataset-thesis%20corpus%20v18-3af4c8?style=flat-square)](https://huggingface.co/datasets/SZLHOLDINGS/thesis-corpus-v18/tree/main)
[![license](https://img.shields.io/badge/license-apache--2.0-7e8aa3?style=flat-square)](https://huggingface.co/datasets/SZLHOLDINGS/thesis-corpus-v18)

</p>
</div>

# SZLHOLDINGS/thesis-corpus-v18

The **v18 Ouroboros Invariant thesis** — LaTeX chapters, the **179 formal blocks**
(theorem / lemma / definition / axiom environments) as a flat CSV, and the per-version
delta ledger that tracks how every formal block evolved v1 → v18.

## Contents

| File | What |
|------|------|
| `chapters/*.tex` | 9 v18 LaTeX chapters (00_abstract … 08_conclusion) |
| `main.tex` | thesis driver |
| `formal_blocks_179.csv` | **179 formal blocks** flattened (env, label, statement, file, lines, status) |
| `per_version_delta_ledger.csv` | per-version theorem table v1→v18 (label · type · statement · lean_file · reference_vector · status) |
| `claims_v18_extracted.json` | raw extracted theorem/lemma/def/axiom environments from the v18 tex |

## Honesty (Doctrine v11)

Each formal block has a **status** column (proven / sorry / axiom / conjecture / informal / pre-formal). **HONEST NOTE: 167 of 179 rows have a blank status field** — these are v14–v18 LaTeX-extracted blocks whose Lean mapping was not completed at snapshot time. Only 12 rows carry a filled status (v1–v9 blocks and the A1–A4 axiom entries). This is the correct, honest state of this historical snapshot; do not treat blank-status rows as PROVEN. For proof status on individual theorems, use `SZLHOLDINGS/lean-proofs-v1`. Λ uniqueness is a **CONJECTURE**. Canonical Lean numbers: **749 declarations / 14 unique axioms / 163 tracked sorries**.

## Sibling datasets

- `SZLHOLDINGS/lean-proofs-v1` · `SZLHOLDINGS/canonical-formulas-v1` · `SZLHOLDINGS/doctrine-v10-v11`

## Citation


**Cite this.** Part of the SZL Holdings *Ouroboros Thesis* (Governed Post-Determinism).  
Concept DOI (always-latest): [10.5281/zenodo.19944926](https://doi.org/10.5281/zenodo.19944926) · This artifact’s version DOI: [10.5281/zenodo.20434276](https://doi.org/10.5281/zenodo.20434276).  
Author: Stephen P. Lutar Jr. · [ORCID 0009-0001-0110-4173](https://orcid.org/0009-0001-0110-4173) · Dataset license: Apache-2.0; the cited program publication is CC-BY-4.0.  
Full DOI-pinned lineage (v1→v26) + the 8 papers: [szl-papers PAPERS_INDEX](https://github.com/szl-holdings/szl-papers/blob/main/PAPERS_INDEX.md).

Honesty (Doctrine v11): Λ unconditional uniqueness is **Conjecture 1** (machine-checked FALSE as stated) — never a theorem; conditional uniqueness is **Theorem U** (axiom-free). Locked-proven formulas = **exactly 8** {F1,F4,F7,F11,F12,F18,F19,F22}; ~185 experimental theorems are a separate CI-green tier; Khipu BFT safety = Conjecture 2. Trust never 100%.

```bibtex
@misc{lutar_szl_ouroboros,
  author    = {Lutar, Stephen P., Jr.},
  title     = {SZL Holdings --- The Ouroboros Thesis (Governed Post-Determinism)},
  year      = {2026},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.19944926},
  url       = {https://doi.org/10.5281/zenodo.19944926},
  note      = {Concept DOI --- always resolves to the latest version. ORCID 0009-0001-0110-4173. CC-BY-4.0.}
}

@misc{lutar_ouroboros_v18,
  author    = {Lutar, Stephen P., Jr.},
  title     = {The Ouroboros Thesis v18 --- Multi-track Substrate Expansion},
  year      = {2026},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.20434276},
  url       = {https://doi.org/10.5281/zenodo.20434276}
}
```

Concept DOI: [10.5281/zenodo.19944926](https://doi.org/10.5281/zenodo.19944926) · ORCID `0009-0001-0110-4173`

---

### ◇ Explore the SZL Holdings estate
[▶ a11oy console (a-11-oy.com)](https://a-11-oy.com) · [a11oy Space](https://huggingface.co/spaces/SZLHOLDINGS/a11oy) · [killinchu](https://huggingface.co/spaces/SZLHOLDINGS/killinchu) · [holographic (3D)](https://huggingface.co/spaces/SZLHOLDINGS/holographic) · [all datasets & models → SZLHOLDINGS](https://huggingface.co/SZLHOLDINGS) · [GitHub org](https://github.com/szl-holdings)

---

<div align="center">

**[🛡️ SZLHOLDINGS on Hugging Face →](https://huggingface.co/SZLHOLDINGS)**   ·   **[a-11-oy.com →](https://a-11-oy.com)**   ·   **[SZL Atlas — estate map →](https://huggingface.co/spaces/SZLHOLDINGS/szl-command-lab)**

### Governed AI you can prove.

<sub>SLSA: L1 honest · L2 attested · L3 roadmap. Λ = Conjecture 1 (advisory, never a theorem). Trust ceiling 0.97 — never 100%. Labels honest by default: MEASURED / REPORTED / MODELED / HEURISTIC / UNKNOWN / UNAVAILABLE. locked-proven = exactly 8 {F1,F4,F7,F11,F12,F18,F19,F22}.</sub>

</div>

## Dataset-server loading boundary

The `formal-blocks` and `version-ledger` configs expose the two tabular CSV artifacts independently. LaTeX chapters, extracted JSON, provenance, and citation files remain source artifacts and are excluded from automatic schema unification. Blank theorem-status fields remain blank; loading the rows does not promote them to proved results.
