# ARXIV_SUBMIT_RUNBOOK.md — Founder Step-by-Step (v22 "Convergence")

**FOUNDER-ONLY ACTION.** arXiv requires the submitter's verified identity and (for a first
submission to a category) an endorsement. An agent cannot and must not submit on the founder's
behalf. This runbook makes the founder's action mechanical: copy/paste each field below.

**Author:** Stephen P. Lutar Jr. · ORCID 0009-0001-0110-4173
**Doctrine:** v11 LOCKED 749/14/163 @ `c7c0ba17` · Λ = Conjecture 1 · SLSA L1+L2 (not L3)
**Submission URL:** https://arxiv.org/submit

---

## 0. Prerequisites (founder)

1. **arXiv account** with a verified institutional or affiliated email. (https://arxiv.org/user/)
2. **ORCID linked** to the arXiv account: 0009-0001-0110-4173.
3. **Endorsement** for the primary category if this is the founder's first submission there.
   - Primary target **cs.LO** typically requires endorsement unless the founder has prior cs.*
     submissions. Request via the arXiv endorsement system; cite the SZL/lutar-lean Zenodo DOIs as
     prior work. (math.LO is an acceptable alternative stream — see §4.)
4. **Source files ready** (the agent pods produced these — collect into one upload folder):
   - `thesis_v22.tex`  — from `team/phd-thesis-arxiv/arxiv_bundle/thesis_v22.tex`
   - `references.bib`  — from `team/phd-thesis-writing/references.bib` (44 verified entries)
   - (No figure files — v22 has only native LaTeX tables.)
5. Compile locally once with `pdflatex thesis_v22 && bibtex thesis_v22 && pdflatex x2` to confirm a
   clean build before upload. arXiv re-compiles from source; PDF-only is rejected for TeX papers.

---

## 1. Start the submission

- Go to **https://arxiv.org/submit** → "Start New Submission."
- **License:** select **Creative Commons Attribution 4.0 International (CC BY 4.0)** — matches the
  thesis declaration. (Do NOT pick arXiv's non-exclusive-only license; CC BY 4.0 is intended.)

## 2. Upload source

- Upload `thesis_v22.tex` and `references.bib` together (a single `.zip` or `.tar.gz` is fine).
- Let arXiv auto-detect TeX. Resolve any "missing font / Type-3" warnings — the bundle uses stock
  `article` + `amsmath`/`amssymb`/`booktabs`/`hyperref`; no nonstandard fonts are required.
- Confirm the auto-generated PDF preview renders the two tables (Sim2Real regimes; lineage) and the
  Greek/math (Λ, Φ) correctly.

## 3. Metadata — paste exactly

**Title:**
```
The Ouroboros Thesis v22 — Convergence: Lambda-Uniqueness Chain, Mechanism Truthfulness, and Sim-to-Real Doctrine Transfer
```

**Authors:**
```
Stephen P. Lutar Jr.
```
(Link ORCID 0009-0001-0110-4173 in the author field.)

**Abstract:** paste the entire contents of `team/phd-thesis-writing/v22_abstract.txt`
(plain text, 1851 characters, well under the 1920 limit; no markdown).

**Comments field:**
```
22nd version of the Ouroboros Thesis line. Lambda-aggregator uniqueness is Conjecture 1 (NOT a theorem): the n-dimensional Cauchy functional-equation chain is only partially closed. A5 permutation invariance added as a structure field (axiom count unchanged at 14). SLSA L1+L2 attested (NOT L3). VCG truthfulness and Round 10-11 formalizations proved on branch / in review. Code (Lean 4): https://github.com/szl-holdings/lutar-lean . Concept DOI: 10.5281/zenodo.19944926 . v22 version DOI minted on Zenodo release paper-v22-1.0.0.
```

**MSC class (paste):**
```
39B22 (Primary) 26E60 68V20 91B26 94A60 (Secondary)
```

**ACM class (paste):**
```
F.4.1; F.2.0; K.6.5
```

**Report number:** leave blank (or `SZL-OUROBOROS-v22`).

## 4. Category selection

- **Primary:** `cs.LO` (Logic in Computer Science) — matches the formal-verification core and the
  math pod's checklist.
- **Cross-list:** `math.OC` (Optimization & Control — VCG/mechanism design), `cs.CR`
  (Cryptography & Security — BLS/DSSE/SLSA), `cs.LG` (Machine Learning — PAC-Bayes / Sim-to-Real).
- **If moderators redirect:** `math.LO` is an acceptable primary if they prefer the math stream;
  in that case keep the same cross-lists and the same MSC string.

## 5. Verify & submit

- Re-read the rendered abstract and PDF preview one final time. Confirm **no over-claim**: the word
  "theorem" must not appear asserting Λ-uniqueness; the abstract and comments both say Conjecture 1.
- Click **Submit**. arXiv assigns a temporary identifier immediately.

## 6. After submission — timeline & follow-ups

- **Moderation:** arXiv holds new submissions for moderator review. Typical window **~24–72 hours**
  (longer over weekends/holidays). The paper announces on the next mailing after acceptance.
- **DOI mint (founder):** create the GitHub release **`paper-v22-1.0.0`** in `szl-holdings/szl-papers`;
  the Zenodo↔GitHub webhook mints the **v22 version DOI**. Then, if desired, add the arXiv ID to the
  Zenodo record and the v22 DOI to the arXiv "Comments"/journal-ref via a metadata update.
- **Endorsement delay:** if endorsement is pending, the submission sits until granted — request it
  before or immediately after starting the submission.
- **Replacement (if needed):** the t=0 Cauchy sorry and the in-review PRs may close on `main`
  shortly. Do NOT delay v1 of the preprint for them — post the honest conjecture-status version now,
  and submit a **replacement** (`arxiv.org/abs/<id>` → "Replace") once the chain closes, updating
  only the relevant sections. Never elevate Λ to a theorem in the text until every Cauchy_ND sorry
  closes on `main` under green CI.

---

## Field cheat-sheet (one block to keep open while submitting)

| arXiv field | Source |
|---|---|
| License | CC BY 4.0 |
| Source upload | `arxiv_bundle/thesis_v22.tex` + `references.bib` |
| Title | see §3 |
| Abstract | `v22_abstract.txt` (1851 chars) |
| MSC | `39B22 (Primary) 26E60 68V20 91B26 94A60 (Secondary)` |
| ACM | `F.4.1; F.2.0; K.6.5` |
| Primary cat | `cs.LO` |
| Cross-list | `math.OC`, `cs.CR`, `cs.LG` |
| Comments | see §3 |

---

*Signed-off-by: Yachay <yachay@szlholdings.ai>*
*Co-Authored-By: Perplexity Computer Agent <agent@perplexity.ai>*
