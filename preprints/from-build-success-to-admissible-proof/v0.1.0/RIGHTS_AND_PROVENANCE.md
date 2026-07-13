# Rights and provenance

Package version: `0.1.0`  
Author: Stephen P. Lutar Jr.  
Affiliation: SZL Holdings LLC  
ORCID: https://orcid.org/0009-0001-0110-4173  
Status: `UNRELEASED_PREPRINT_PACKAGE`

| Source family | Included paths | Provenance / transformation | Governing terms | Redistribution status |
|---|---|---|---|---|
| Manuscript, PDF, package documentation, and metadata | `manuscript.md`, `manuscript.pdf`, `README.md`, `CITATION.cff`, manifests | Original SZL-authored content | CC BY 4.0 | `INCLUDED_REDISTRIBUTABLE_WITH_ATTRIBUTION` |
| Lutar-Lean selected source and exact path-safe receipts | `sources/lutar-lean/`, `evidence/paper1/` | Selected module and eligible receipts copied from the Apache-2.0 project; path-bearing audit copy is sanitized with both digests recorded | Apache-2.0 | `INCLUDED_REDISTRIBUTABLE_LICENSE_PRESERVED` |
| Proof-obligation queue, readiness ledger, and crosswalk | `data/`, `schemas/` | Queue is exact; ledger path strings are sanitized; crosswalk is derived deterministically | CC BY 4.0 | `INCLUDED_REDISTRIBUTABLE_WITH_ATTRIBUTION` |
| Lean, Mathlib, Python, ReportLab, and other third-party tools | Not bundled, except names/version pins | Referenced for reproduction only | Upstream terms apply | `NOT_BUNDLED_NO_RELICENSE` |
| MATLAB, GNU Octave, QPU/provider software, telemetry collectors, model weights, and external datasets | Not bundled | No execution substrate or third-party payload is represented as included | Upstream/proprietary terms would apply | `NOT_BUNDLED_NO_REDISTRIBUTION_CLAIM` |
| Scholarly references | Bibliographic citations only | No third-party paper, figure, or publisher PDF is bundled | Citation only | `CITATIONS_ONLY` |

Dataset and receipt paths are archive-relative when bundled and `${WORKSPACE_ROOT}/...` when referring to a nonbundled workspace source. Developer-specific absolute paths are excluded. See `SOURCE_TRANSFORMATIONS.json` for original and packaged digests.

No DOI, deposit identifier, release URL, peer-review status, or third-party endorsement is asserted.
