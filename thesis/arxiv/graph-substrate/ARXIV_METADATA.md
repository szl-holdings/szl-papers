# arXiv submission metadata - Paper 2 (graph-substrate audit)

**Primary source:** `main.tex`
**Reference mirror:** `references.bib` (the submitted `main.tex` is self-contained)
**Verified build:** Tectonic 0.16.9
**Verified length:** 23 pages
**License:** CC-BY-4.0

---

## Title

A Lean 4 Audit of Graph-Shaped Governance: Permutation-Safe Score Aggregation, 1-WL Factoring, Geometric Contraction, and Finite-Frontier Bounds

## Author

Stephen P. Lutar Jr. (SZL Holdings, Inc.) - ORCID 0009-0001-0110-4173

## arXiv categories

- **Primary:** `cs.LO` (Logic in Computer Science)
- **Cross-list:** `cs.LG` (Machine Learning), `cs.DM` (Discrete Mathematics)

The primary category is `cs.LO` because the paper's contribution is a formal
artifact and semantic non-vacuity audit, not a new trained model or graph-learning
benchmark.

## ACM classification

- Theory of computation -> Logic and verification
- Computing methodologies -> Machine learning -> Learning in probabilistic graphical models
- Security and privacy -> Formal methods and theory of security

## MSC 2020

- 68V15 (Mathematical software)
- 68T07 (Artificial neural networks and deep learning)
- 03B35 (Mechanization of proofs and logical operations)
- 05C60 (Isomorphism problems)

## Suggested comments field

23 pages, 7 tables, selected Lean excerpts, reviewer checklist, and
claim-to-artifact crosswalk. Audits the merged pull-request snapshot
`8de25baf1d5adcc11238d13e17a9a7eaaf05af6d` (PR #189) using public CI run
27066757406. Inventories 25 printed Lean declarations and corrects prior
overstatements about topology sensitivity, 1-WL factorization, frontier
termination, spectral scope, theorem count, and information-target status.
All audited results remain experimental-tier; frozen baseline `c7c0ba17` is
unchanged. Companion program DOI: 10.5281/zenodo.19944926.

## Abstract (ready to paste)

Formal verification proves that a conclusion follows from its premises, but it
does not by itself show that a formal model captures the operational claim
attached to it. We audit a Lean 4 graph-governance artifact merged as pull
request #189 at commit
`8de25baf1d5adcc11238d13e17a9a7eaaf05af6d`. A public CI run built the same Git
tree and printed the axiom dependencies for 25 declarations: none depends on
`sorryAx`; seven are axiom-free, four use only `propext`, one uses `propext` and
`Quot.sound`, and thirteen use the standard Mathlib trio. The semantic findings
are narrower. `vertexLambda` reads a vertex's score vector but never adjacency,
so the graph-level value is invariant under score-preserving reindexing yet
topology-blind; the isomorphism proofs do not consume their `edge_pres` field.
`gnn_le_wl` is a correct factoring implication but assumes, rather than
constructs, the factorization through an arbitrary coloring. The
finite-frontier declarations prove a natural-number countdown, not a graph
traversal, and the metric iteration theorem propagates a supplied contraction
without deriving a spectral gap. We provide countermodels, an exact declaration
ledger, a non-vacuity protocol, deployment guidance, and a reproducibility
checklist. The result separates kernel-checked proof validity from
graph-semantic and implementation-refinement evidence.

## Immutable audit identifiers

- Merged commit: `8de25baf1d5adcc11238d13e17a9a7eaaf05af6d`
- PR head checked by CI: `be376b40766a29d59549f7f22a113758e5c475e5`
- Identical Git tree: `d9db68448b337949aeaebe37409b453abad908b6`
- Public CI: <https://github.com/szl-holdings/lutar-lean/actions/runs/27066757406>
- Lean: `v4.18.0`
- Mathlib: `aa936c36e8484abd300577139faf8e945850831a` (`v4.18.0`)

## Verified declaration summary

- Focal graph/metric scope: 17 printed declarations.
- Context correction: 5 `InfoSubstrate` declarations and 3
  `SubGaussianKL` declarations.
- Total ledger: 25 printed declarations.
- Axiom output distribution: 7 none; 4 `[propext]`; 1
  `[propext, Quot.sound]`; 13
  `[propext, Classical.choice, Quot.sound]`.
- `mpRun_det` is reflexive and is not counted as a substantive determinism
  guarantee.
- All results remain experimental-tier; no declaration is promoted into the
  frozen baseline by this paper.

## Scope and originality notes

- The paper's central contribution is an exact source/semantic audit of a
  graph-shaped Lean artifact. It is not another general readiness or
  evidence-typing paper.
- The present `vertexLambda` is score-only. Do not describe it as a
  closed-neighborhood aggregate or as topology-sensitive.
- The 1-WL declaration assumes `hfac`; it does not define WL refinement or prove
  that `MPSystem` factors through it.
- The frontier model is a natural-number countdown. A concrete receipt-DAG
  refinement theorem remains future work.
- The metric theorem contains no spectral object and requires a supplied
  one-step distance bound.
- Information-theory targets were no longer deferred at the audited snapshot;
  `SubGaussianKL.lean` contains three Mathlib re-exports.
- No arXiv identifier has been assigned. Do not invent one.
- Do not mint a new Zenodo DOI for a draft revision until the final publication
  relationship and versioning plan are chosen; retain the program concept DOI
  in the manuscript meanwhile.

## Build and page verification

From the `szl-papers` repository root:

```text
tectonic --outdir tmp/pdfs/graph-substrate \
  thesis/arxiv/graph-substrate/main.tex
```

The verified PDF is 23 pages. The successful build emitted no TeX layout
warnings. Tectonic printed a host-level Fontconfig configuration notice on
Windows; it did not prevent font embedding or PDF generation.

## Submission checklist

- [x] Exact merged snapshot and public CI run identified
- [x] False neighborhood-aggregation claim removed
- [x] Unused `edge_pres` and topology blindness disclosed
- [x] 1-WL factorization premise disclosed
- [x] `mpRun_det` classified as reflexive
- [x] Frontier scope corrected to a natural-number countdown
- [x] Metric/spectral scope corrected
- [x] Information-target status corrected
- [x] Experimental vs. frozen baseline boundary explicit
- [x] Compiled page count verified (23)
- [x] TeX overflow/underflow warnings eliminated
- [ ] Founder review of title, categories, and submission account
- [ ] arXiv submission and identifier assignment
