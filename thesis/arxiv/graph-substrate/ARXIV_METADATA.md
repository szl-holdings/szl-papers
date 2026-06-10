# arXiv submission metadata — Paper 2 (graph substrate)

**Files in this package:** `main.tex`, `references.bib`
**Compile:** `pdflatex main && bibtex main && pdflatex main && pdflatex main` (standard `article` + amsmath/booktabs/listings/hyperref).

---

## Title
A Kernel-Verified Graph Substrate for Governed AI: Isomorphism-Invariant Trust Aggregation, a 1-WL Expressivity Ceiling, Spectral Contraction, and Bounded-Frontier DAG Termination

## Authors
Stephen P. Lutar Jr. (SZL Holdings, Inc.) — ORCID 0009-0001-0110-4173

## arXiv categories
- **Primary:** `cs.LG` (Machine Learning)
- **Cross-list:** `cs.LO` (Logic in Computer Science), `cs.DM` (Discrete Mathematics), `stat.ML` (Machine Learning, statistics)

## ACM classification
I.2.6 (Learning); F.4.1 (Mathematical Logic); G.2.2 (Graph Theory)

## MSC 2020
68V15 (Formal proofs / proof assistants); 68T07 (Artificial neural networks / deep learning); 05C60 (Isomorphism problems in graph theory); 68R10 (Graph theory in CS)

## License
CC-BY-4.0

## Comments field (suggested)
~15 pages. 11 Lean 4 theorems, sorry-free, no new axiom (Wave-6 graph substrate, branch prove-wave6/graph-substrate-fg1-fg6, head dc7ae26d). Relates to position-aware GNN and expressivity lineage (You et al.; Xu et al. GIN; graph2nn; Polymathic AI; McLeish et al.). Companion concept DOI: 10.5281/zenodo.19944926. Source repository: github.com/szl-holdings/lutar-lean.

## Abstract (ready to paste)
We present a machine-checked graph substrate for governed AI: eleven Lean 4 theorems, all sorry-free and introducing no axiom beyond the Lean core, that pin down four structural properties of a trust-aggregation graph used as a governance control plane. (F-G4) The Lutar trust aggregator is isomorphism-invariant: relabelling the graph leaves the aggregated verdict unchanged. (F-G2) A single message-passing layer over this substrate is no more expressive than the 1-dimensional Weisfeiler-Leman test (a 1-WL ceiling), proven axiom-free, making the substrate's discriminative power exactly characterizable rather than assumed. (F-G3) The aggregation update is a geometric contraction whose iterates are non-increasing, giving a spectral convergence guarantee. (F-G1) A coordinate-Lipschitz Frechet embedding gives an isometric structural map, and (F-G5, F-G6) a bounded-frontier iteration drains in finite steps with a relabelling-invariant adjacency count, yielding DAG termination. We position these results against the position-aware and expressivity-bounded GNN lineage and are explicit about the locked-versus-experimental boundary: the substrate theorems are kernel-verified, while the broader Lutar uniqueness result remains conditional (Theorem U) and the unconditional version is machine-checked false (Conjecture 1).

## Lineage cited as related work (NOT claimed as ours)
- Jiaxuan You et al. — Position-aware GNNs (P-GNN), GraphGym, design-space work (Stanford/SNAP).
- Keyulu Xu et al. — Graph Isomorphism Network (GIN) and the WL expressivity bound.
- graph2nn — network-as-graph / relational graph structure of neural nets.
- Polymathic AI / Jeff Shen — foundation models for science.
- McLeish et al. — recurrent-depth / abacus-style reasoning.

## Honesty notes for the founder
- The 11 theorems are locked/kernel-verified (sorry-free, no new axiom); the GNN-lineage works are cited strictly as prior/related art.
- The 1-WL ceiling is stated as a limiting ceiling (honest expressivity bound), not a capability claim.
- No fabricated benchmarks, citations, or arXiv IDs appear.
