# Comparative Ancient Mathematics: Source Ledger and Falsifiable SZL Analogy

**Research status:** SOURCE-ONLY, DRAFT, NON-NORMATIVE; not a new paper version,
not a proof theorem, not historical decipherment or training permission.

This research register links `szl-papers` and `lutar-lean` to the **original
Python-only** review proposal in `szl-mesh/src/szl_mesh/heritage_math.py`.
The owner paper's v26/P3 release hold stays unchanged. The eight locked
identifiers and the 21 formula-kernel functions remain distinct.

## Sources assessed

| Tradition and original artifact | Publication / collection link | Mathematical pattern | SZL code analogy | Constraint |
|---|---|---|---|---|
| Inka-style khipu (knotted cords, **not codices**) | [Open Khipu Repository](https://github.com/khipulab/open-khipu-repository); [NIST](https://www.nist.gov/nist-museum/standardizing-empire) | Decimal place-value and documented hierarchy | Synthetic base-10 positional identity, potential ledger sum checks | No automatic knot decipherment, narrative decoding or archaeology-to-weight training |
| Egyptian Rhind Papyrus, British Museum EA10057–58 | [British Museum guide](https://www.britishmuseum.org/sites/default/files/2022-10/Hieroglyphs_unlocking_ancient_Egypt_large_print_guide_The_British_Museum_2.pdf), [Open University](https://www.open.edu/openlearn/science-maths-technology/mathematics-statistics/egyptian-mathematics/content-section-1.1.1) | Multiplication, unit fractions and proportional false position | Integer doubling and exact Fraction identities with bounded execution | Modern greedy unit-fraction algorithm is **not** attributed to a particular ancient Rhind solution |
| Euclid, *Elements* VII.2, Greek text tradition | [Clark University historical translation](https://mathcs.clarku.edu/~%20djoyce/elements/bookVII/propVII2.html) | Mutual subtraction / greatest common measure | Bounded modern quotient/remainder GCD | Mathematical equivalence, not verbatim ancient proof or an SZL Lean proof |
| YBC 7289 Babylonian tablet (Mesopotamia) | [MAA / Yale Babylonian Collection](https://old.maa.org/press/periodicals/convergence/the-best-known-old-babylonian-tablet) | Sexagesimal value of √2 | Exact `1;24,51,10 = 30547/21600`, squared residual `-791/466560000` | Does not establish scribe's derivation or rights to reproduce photographs |
| Dresden Maya Codex (**Maya, not Inka**) | [SLUB Dresden](https://www.slub-dresden.de/en/explore/manuscripts/the-dresden-maya-codex) | 260-day ritual and 365-day solar-calendar cycles | Modern `LCM(260,365)=18,980` | No reading of Dresden astronomy, provenance or ritual texts, and no facsimile copied |

## Why existing SZL evidence matters more than a mythology of "hidden codes"

- `a11oy/docs/ANCIENT_TEXTS_FORMULA_LINEAGE.md` already separates historical
  inspiration from deployed algorithms and correct formal status. It includes
  Liu Hui polygon convergence and Madhava/Kerala arctangent remainder methods;
  both remain valid separate research lanes and are not silently mapped to
  new formula proof identifiers here.
- `szl-khipu/research/okr_corpus/README.md` reports an exact **R2 top-cord**
  arithmetic excess in 619 pinned OKR records: 54 observed matching sums vs
  null mean 4.96 across 1,000 fixed-seed permutations. Sensitivity matters:
  removing records with missing provenance reduces the R2 observed count to
  29/398 provenance-identified records, with role/depth null mean 2.934.
  These are **reported, not re-run measurements**, and their distributions
  cannot establish cord meaning, independent records, or broader Inka cultural
  universality. Other relations (especially R3) did **not** pass the
  preregistered family-wise threshold; preserve that negative finding.
- `szl-formulas` contains the 21 computational formula functions. The locked
  Lean F1/F4/F7/F11/F12/F18/F19/F22 set is a separate carrier reference.
  `szl-papers/metadata/locked-claim-contract.json` keeps v26 claim-wording
  mismatches and owner review unresolved; do not rewrite thesis claims or cite
  these synthetic checks as new experimental/theorem progress.

## Original bounded proposed experiment

One integer is independently written as an **abstract** decimal sequence
and a sexagesimal sequence. Check both equal N with exact arithmetic, then
check (a) Egyptian binary doubling N×b, (b) Euclid's GCD remainder chain,
(c) fraction decomposition and proportional correction, and (d) calendar
period LCM as a **separate** historical example. A mismatch is `HOLD`.
No receipt authority, historical decipherment, model-accuracy improvement,
conjecture resolution or benchmarking superiority follows from these
elementary identities. The point of the composite is **multi-source provenance
hygiene** for agentic claims, not claiming to invent an ancient theorem.

The proof-carrying agent junction only accepts **synthetic** numbers and
**reviewable proposals**. All real archaeological data need verified licences,
site/cohort provenance, community stewardship review and independent scholarly
controls before any ingestion or research publication. Ancient public-domain
mathematical ideas may be implemented independently, but linked photographs,
modern translations and datasets retain their own rights.

## Reproduction and missing evidence

The original SZL Python implementation is in `szl-mesh`, with synthetic-only
unit and negative tests. Future empirical work must preregister competing
null models, independent source/site holdouts, false discovery correction,
recovery tests and expert review; preserve raw results and inconclusive cases.
The existing v26 and DOI lifecycle hold remains unchanged. A source PR
cannot qualify a new Zenodo or arXiv publication.
