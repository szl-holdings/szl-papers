#!/usr/bin/env python3
"""build_pdf.py -- Render "Convergence (v22)" as an arXiv-style PDF.
Compiled rendering of main.tex/main.md (no LaTeX engine in sandbox). Shares
typography with the v23 exemplar via _thesisbuild."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _thesisbuild import *
from reportlab.lib.units import inch

HERE = os.path.dirname(os.path.abspath(__file__))
register_fonts(os.path.join(HERE, "fonts"))
reset_story()

# ======================================================================= TITLE
title_block(
    "Convergence",
    "An Honest, Audit-Ready Convergence of the &Lambda;-Aggregator Uniqueness Chain, "
    "Mechanism Truthfulness, and Sim-to-Real Doctrine Transfer",
    "Yachay (Stephen P. Lutar Jr.)",
    ['SZL Holdings, Inc. &nbsp;·&nbsp; ORCID <a href="https://orcid.org/0009-0001-0110-4173" color="#01696F">0009-0001-0110-4173</a>',
     'Thesis v22 &ldquo;Convergence&rdquo; &nbsp;·&nbsp; 2026-06-03 &nbsp;·&nbsp; Concept DOI (always-latest): '
     '<a href="https://doi.org/10.5281/zenodo.19944926" color="#01696F">10.5281/zenodo.19944926</a> &nbsp;·&nbsp; License: CC&nbsp;BY&nbsp;4.0 / Apache-2.0',
     '<font color="#0C4E54"><b>Doctrine v11 LOCKED</b></font> &mdash; 749 declarations &middot; 14 unique axioms &middot; '
     '163 sorries @ c7c0ba17 &nbsp;·&nbsp; &Lambda; is <font color="#A12C7B"><b>Conjecture 1</b></font> &nbsp;·&nbsp; SLSA L1+L2 (5/5 GHCR images)'],
)

abstract_block(
    "v22 (&ldquo;Convergence&rdquo;) consolidates the formal-verification advances of the May&ndash;June 2026 "
    "innovation rounds into the canonical thesis line. Its central correction is stated up front: the long-standing "
    "claim that axioms A1&ndash;A4 force the weighted geometric mean is <b>false</b>. The asymmetric mean "
    "&Phi;(x&#8321;,x&#8322;)=x&#8321;<sup>2/3</sup>&middot;x&#8322;<sup>1/3</sup> satisfies A1&ndash;A4 yet differs "
    "from &Lambda; and fails permutation invariance. We add <b>A5 (permutation invariance)</b> as a <i>structure "
    "field</i> on the axiom record &mdash; <b>not</b> a new axiom &mdash; keeping the unique-axiom count at <b>14</b>, "
    "and we report the <i>partial</i> closure of the n-dimensional Cauchy functional-equation chain (topology + "
    "functional-analysis + symmetric branches) that, when complete, would discharge &Lambda;-uniqueness. <b>It is not "
    "complete on main; &Lambda; therefore remains Conjecture&nbsp;1.</b> We additionally report: VCG mechanism "
    "truthfulness (dominant-strategy incentive compatibility + individual rationality, proven on branch); "
    f"<b>SLSA L1+L2</b> build provenance (5/5 GHCR images verified via {M('slsa-verifier')}); the Round&nbsp;10&ndash;11 "
    "frontier formalizations (physics, quantum, CS, crypto, distributed systems); and a <b>Sim-to-Real "
    "doctrine-transfer benchmark</b> modeled on the Walrus physical foundation model that measures a mean doctrine "
    "&alpha;-gap of <b>0.10</b> across five unseen compliance regimes. We claim only what is mechanically checked or "
    "empirically measured; everything in review is labeled as such. Doctrine v11 numbers are reproduced verbatim: "
    "<b>749 declarations, 14 unique axioms, 163 sorries</b> at lutar-lean c7c0ba17.",
    "Convergence, &Lambda;-aggregator, Conjecture&nbsp;1, permutation invariance, A5 structure field, Cauchy "
    "functional equation, VCG truthfulness, mechanism design, SLSA L2, sim-to-real transfer, Lean&nbsp;4, honesty "
    "doctrine.",
    "<i>Honesty note (verbatim):</i> The &Lambda;-aggregator is <b>Conjecture&nbsp;1</b> &mdash; explicitly not a "
    "theorem; unconditional uniqueness under {A1&ndash;A5} is machine-checked <b>FALSE</b>. A5 is a <b>structure "
    "field</b>, not a new axiom; the unique-axiom count stays <b>14</b>. The Cauchy_ND chain is <b>not</b> complete on "
    f"main (one residual honest sorry at t=0). SLSA <b>L1+L2</b> is achieved (5/5 GHCR images via {M('slsa-verifier')}); "
    "<b>L3 not claimed</b>. Reed&ndash;Solomon is coding, not a hologram; event sourcing is fold-replay, not time "
    "travel; physics analogies are scaffolding. Quechua organ names are brand naming, not prior-art or cultural claims.",
)

# ======================================================================= 1
section("Where v22 sits in the lineage")
para("Version&nbsp;22 follows v21 (&ldquo;The PURIQ-OS Substrate&rdquo;, 2026-06-01). It is <b>not</b> a new "
"architecture; it is the <b>convergence</b> of the mathematical-rigor work that v14&ndash;v21 deferred. Where v19 "
"built the verification bridge, v20 presented the verified anatomy, and v21 shipped the runtime that executes it, v22 "
"turns to the open mathematical obligations those layers surfaced &mdash; above all the &Lambda;-aggregator "
"uniqueness question &mdash; and reports exactly how far they have been closed. See "
'<a href="https://github.com/szl-holdings/szl-papers/blob/main/thesis/THESIS_LINEAGE.md" color="#01696F">'
"THESIS_LINEAGE.md</a> for the full v1&nbsp;&rarr;&nbsp;v23 timeline.")
subsection("Claim discipline (carried verbatim from v21)")
para("v22 preserves the three-class claim discipline of its predecessors and never blurs the classes:")
numbered([
"<b>Proved (on main, locked).</b> Mechanised in Lean&nbsp;4 with no &lsquo;sorry&rsquo; and a disclosed axiom "
"footprint, included in the locked kernel @ c7c0ba17.",
"<b>Proved (on branch, in review).</b> Mechanised and sorry-free on a feature branch but <i>not yet merged to "
"main</i> &mdash; e.g. the VCG truthfulness lemmas and the A5 structure-field merge&rsquo;s downstream chain. These "
"are reported as in-review and are <b>not</b> presented as landed kernel theorems.",
"<b>Operational fact / measured.</b> Engineering and empirical claims established by running real tooling: "
f"{M('slsa-verifier')} attestation checks, the Sim-to-Real &alpha;-gap benchmark. Reproducible, labeled "
"measured-not-proven, never described as theorems.",
])
subsection("The central correction stated plainly")
para("The single most important thing v22 records is a <b>correction</b>, not a new result: the historical "
"&ldquo;Theorem&nbsp;1 &mdash; &Lambda; is the unique aggregator under A1&ndash;A4&rdquo; was <b>incorrect</b>. v22 "
"names the guilty lemma, exhibits the counterexample, adds the missing structure (A5), and reports honestly that the "
"resulting uniqueness chain is <i>still open</i>. This is the Lakatosian discipline of the whole thesis line made "
"concrete: a refuted conjecture is corrected in the open, not quietly deleted.")
subsection("Doctrine v11 (verbatim, LOCKED @ c7c0ba17)")
para("<b>749 declarations &middot; 14 unique axioms &middot; 163 sorries</b> (112 baseline + 51 Putnam) &mdash; "
"lutar-lean snapshot c7c0ba17. A5 permutation-invariance, merged via PR&nbsp;#148 as a <i>structure field</i>, leaves "
"the <b>unique-axiom count at 14</b>; the post-A5 live corpus measures 794 declarations / 14 unique axioms / 191 "
"sorries (measured 974e5e0c, 2026-06-03). The locked numbers are the authoritative figures and are not modified by "
"this paper.")

# ======================================================================= 2
section("Related work: means characterizations, mechanism design, and provenance")
para("v22 sits at the intersection of three precisely-cited literatures.")
subsection("Quasi-arithmetic means and the A1&ndash;A4 insufficiency")
para("A literature review of published results on quasi-arithmetic and symmetric means confirms that A1&ndash;A4 are "
"<i>insufficient</i> to force the geometric mean. Kolmogorov (1930) and Nagumo (1930) gave the quasi-arithmetic-mean "
"characterizations; Acz&eacute;l "
'<a href="https://doi.org/10.1090/S0002-9904-1948-09020-9" color="#01696F">[Acz&eacute;l 1948]</a> gave the '
"functional-equation route to means; Hardy, Littlewood &amp; P&oacute;lya (1934) developed the power-mean family; and "
"Voorneveld (2008) characterized aggregators that admit asymmetric weights. None of these force a <i>symmetric</i> "
"geometric mean from A1&ndash;A4 alone, which is exactly why an extra invariance hypothesis (A5) is required.")
subsection("Mechanism design and truthful auctions")
para("The VCG truthfulness results follow the mechanism-design tradition: a mechanism is dominant-strategy incentive "
"compatible if truthful reporting is optimal regardless of others&rsquo; reports, and individually rational if "
"participation never yields negative utility. The geometric-mean trust aggregator itself is independently motivated as "
"a consensus weighting in the pairwise-comparison literature "
'<a href="https://doi.org/10.1007/s10726-018-9589-3" color="#01696F">[Cs&aacute;t&oacute; 2018]</a>.')
subsection("Supply-chain provenance and verified kernels")
para("Build-provenance posture is graded against "
'<a href="https://slsa.dev/spec/v1.0/levels" color="#01696F">[SLSA v1.0]</a>; v22 verifies attested '
f"build-service provenance with {M('slsa-verifier')}, reaching <b>L2</b>. The Lean mechanisation discipline follows "
"the verified-systems tradition of the Lean&nbsp;4 prover "
'<a href="https://doi.org/10.1007/978-3-030-79876-5_37" color="#01696F">[de Moura &amp; Ullrich 2021]</a> and the '
"information-flow security model of "
'<a href="https://doi.org/10.1109/SP.1982.10014" color="#01696F">[Goguen &amp; Meseguer 1982]</a>.')

# ======================================================================= 3
section("Formal preliminaries: the axioms and the invariant")
para("We fix the formal vocabulary before reporting the advances. The aggregation organ (Ayni) is governed by the "
"<b>Lutar invariant</b>, the equal-weight geometric mean:")
boxed([P('&Lambda;<sub>k</sub>(x<sub>1</sub>, &hellip;, x<sub>k</sub>) = '
         '(&prod;<sub>i=1</sub><sup>k</sup> x<sub>i</sub>)<sup>1/k</sup> &nbsp; on [0,1]<sup>k</sup>.', thm)])
para("The candidate characterizing axioms are:")
table(["Axiom","Statement"],
[["**A1 Continuity","&Phi; is continuous on the unit cube."],
 ["**A2 Homogeneity","&Phi;(t&middot;x) = t&middot;&Phi;(x) for scalar t (positive homogeneity of degree 1)."],
 ["**A3 Idempotence","&Phi;(c, &hellip;, c) = c on the diagonal."],
 ["**A4 Boundedness","min&nbsp;x<sub>i</sub> &le; &Phi;(x) &le; max&nbsp;x<sub>i</sub> (fixes endpoints)."],
 ["**A5 Permutation inv.","&Phi;(x) is invariant under any reordering of its arguments (the NEW structure field)."]],
[1.5*inch,4.8*inch])
para("The conditional uniqueness result of v23 additionally declares <b>A6&prime; (block consistency)</b>; v22 does "
"<b>not</b> assume A6&prime; and makes no unconditional uniqueness claim.")

# ======================================================================= 4
section("A5 axiom merge &mdash; the A1&ndash;A4 uniqueness gap, corrected (MERGED, PR #148)")
para("The historical &ldquo;Theorem&nbsp;1 &mdash; &Lambda; is the unique aggregator under A1&ndash;A4&rdquo; was "
"<b>incorrect</b>. We exhibit the monster, name the guilty lemma, and revise the theorem.")
subsection("The verified counterexample")
para("The asymmetric mean &Phi;(x&#8321;,x&#8322;)=x&#8321;<sup>2/3</sup>&middot;x&#8322;<sup>1/3</sup> satisfies "
"homogeneity (A2), boundedness (A4), continuity (A1), and idempotence (A3), yet &Phi;&nbsp;&ne;&nbsp;&Lambda;<sub>2</sub> "
"and &Phi;(2,1)=2<sup>2/3</sup>&nbsp;&ne;&nbsp;2<sup>1/3</sup>=&Phi;(1,2), so permutation invariance fails. A second, "
"discrete machine-checked counterexample is the max-aggregator: at the point (4,1) the max returns max=4 while "
"&Lambda;<sub>2</sub>(4,1)=&radic;4=2, so they disagree. Both refutations are reproduced verbatim from the locked "
"defense and are machine-checked.")
boxed([P("<b>Refutation (machine-checked).</b> Under {A1&ndash;A4} alone, &Lambda; is <b>not</b> the unique "
"aggregator: &Phi;(x&#8321;,x&#8322;)=x&#8321;<sup>2/3</sup>&middot;x&#8322;<sup>1/3</sup> is a distinct A1&ndash;A4 "
"mean. The missing hypothesis is symmetry (permutation invariance), which we add as A5. Even under the full "
"{A1&ndash;A5}, unconditional uniqueness remains <b>FALSE</b> without the further declared block-consistency axiom "
"A6&prime; (v23); &Lambda; is therefore <b>Conjecture&nbsp;1</b>.", thm)], bg=CONJBG)
subsection("The fix: A5 as a structure field, not a new axiom")
para("The fix landed on main on 2026-06-03 via PR&nbsp;#148: we add an "
f"{M('IsPermutationInvariant')} predicate and an <b>A5 structure field</b> to the "
f"{M('LutarAxioms')} record. The lemma {M('Lambda_A5_perm_invariant')} is <b>sorry-free</b>, proved with "
f"{M('Equiv.prod_comp')} / {M('Fintype.prod_equiv')}. Because A5 is a structure field on an existing record rather "
f"than a fresh {M('axiom')} declaration, the <b>unique-axiom count stays 14</b>; the live corpus moves to "
"<b>794 declarations / 14 unique axioms / 191 sorries</b> (measured 974e5e0c, 2026-06-03 17:32Z). This distinction "
"&mdash; <i>adding structure vs. adding an axiom</i> &mdash; is the load-bearing honesty point of the section: the "
"trusted base did not grow.")
codeblock([
"-- A5 added as a STRUCTURE FIELD (not a new axiom)",
"structure LutarAxioms (k : Nat) where",
"  continuous   : ...          -- A1",
"  homogeneous  : ...          -- A2",
"  idempotent   : ...          -- A3",
"  bounded      : ...          -- A4",
"  permInvariant : IsPermutationInvariant Phi   -- A5 (new field)",
"",
"theorem Lambda_A5_perm_invariant : IsPermutationInvariant Lambda := by",
"  intro sigma; simpa using Fintype.prod_equiv sigma _ _ (by simp)",
"-- #print axioms Lambda_A5_perm_invariant  => [propext, Quot.sound]",
])
para("<i>Listing&nbsp;4.1: A5 added as a structure field; the proof is sorry-free and the axiom count is unchanged.</i>")

# ======================================================================= 5
section("The Cauchy_ND uniqueness chain &mdash; partial closure (IN REVIEW)")
para("With A5 in place, &Lambda;-uniqueness reduces to an n-dimensional Cauchy functional-equation chain. We report "
"its <i>partial</i> closure honestly: three branches are in review, and one residual sorry remains.")
table(["Branch","PR","Status","Note"],
[["Topology (monotone &rarr; continuity)","#175","in review","Landed TRUE forms; refused to fake-prove"],
 ["Functional analysis (mult. monotone)","#173","in review","Closed with 1 honest sorry on the t=0 degenerate case"],
 ["Symmetric (exponents &alpha;<sub>i</sub>=1/k)","#174","in review","Closed with A5 dependency"]],
[2.4*inch,0.6*inch,0.8*inch,2.5*inch])
para("Combined, <b>A5 + Cauchy + topology + symmetric = the full &Lambda;-uniqueness chain.</b> <b>This chain is not "
"yet complete on main</b> (three PRs open, one residual honest sorry on the t=0 degenerate case). <b>Therefore "
"&Lambda; stays Conjecture&nbsp;1.</b> We will elevate &Lambda; to Theorem&nbsp;1 <i>only</i> when every Cauchy_ND "
"sorry closes on main and Lake CI is green.")
boxed([P("<b>Why one honest sorry is kept, not hidden.</b> The functional-analysis branch (PR&nbsp;#173) closes the "
"multiplicative-monotone-is-power-function lemma everywhere except the t=0 degenerate boundary case, where the proof "
"is genuinely incomplete. A naive consolidation would comment the gap out to present a clean &lsquo;green&rsquo; "
"branch. We refuse: the sorry is a typed, named open obligation with a discharge route, and deleting it would convert "
"a disclosed gap into a silent assumption. The honesty doctrine treats a disclosed obligation as strictly better than "
"a hidden one.", thm)])


# ---- new section: the axiom-count invariant under A5 (defensive detail) ----
section("The axiom-count invariant under the A5 merge")
para("Because the unique-axiom count is a load-bearing honesty number, we treat its invariance under the A5 merge as "
"a claim that itself deserves an explicit argument rather than an assertion. The question a hostile reviewer asks is "
"blunt: <i>you added a hypothesis to your characterization; how can the axiom count not go up?</i>")
subsection("Structure field vs. axiom declaration")
para(f"In Lean&nbsp;4, an <b>axiom</b> is a declaration introduced with the {M('axiom')} keyword that the kernel "
f"accepts without proof; it enlarges the trusted base and appears in {M('#print axioms')} for every theorem that "
"depends on it. A <b>structure field</b>, by contrast, is a component of a record type: it is a <i>hypothesis a "
"caller must supply a proof for</i>, not a fact the kernel grants for free. Adding A5 as the field "
f"{M('permInvariant : IsPermutationInvariant Phi')} on {M('LutarAxioms')} means that any theorem quantifying over "
f"{M('LutarAxioms')} now carries an additional <i>premise</i>, discharged by the caller, exactly as a mathematician "
"adds a hypothesis to a lemma. No new fact is granted axiomatically; the trusted base is unchanged.")
subsection("What #print axioms reports")
para(f"The lemma {M('Lambda_A5_perm_invariant')} &mdash; the proof that &Lambda; itself satisfies A5 &mdash; reports "
f"{M('[propext, Quot.sound]')} under {M('#print axioms')}, i.e. only Lean-core logical axioms, no project-specific "
"idealization. Consequently the corpus-wide unique-axiom count stays at <b>14</b>: A5 contributes a provable "
"property of &Lambda;, not an article of faith. The declaration count rises (749&nbsp;&rarr;&nbsp;794 live) because "
"the field, its predicate, and the supporting lemmas are new declarations; the <i>axiom</i> count does not, because "
f"none of them is an {M('axiom')}.")
boxed([P("<b>The honesty point in one line.</b> Adding structure is free of trust cost; adding an axiom is not. A5 "
"adds structure, so the trusted base is unchanged at 14 unique axioms &mdash; and we say so in every "
f"{M('#print axioms')} output rather than asking the reader to take it on faith.", thm)])
para("This is the same discipline applied to the locked counts throughout: the drift gate pins 749 / 14 / 163 at "
"c7c0ba17, the A5-track live corpus is reported separately as 794 / 14 / 191, and the unique-axiom column is "
"identical in both because the only thing A5 changed was structure, never the trusted base.")

# ======================================================================= 6
section("VCG mechanism truthfulness (proven on branch, PR #172)")
para("Both VCG sorries are closed on branch (PR&nbsp;#172, pending merge). We report them as <b>in-review, "
"branch-proven</b> &mdash; sorry-free on the branch but not yet part of the locked kernel.")
theorem_box("Theorem 6.1 (vcgDominantStrategyTruth &mdash; in review)", CIG,
"In the trust-weighted VCG mechanism, truthful reporting of an agent&rsquo;s private valuation is a "
"<b>dominant strategy</b>: for every agent and every profile of others&rsquo; reports, the agent&rsquo;s utility under "
"truthful reporting is at least its utility under any misreport.",
f"Proved on branch with {M('Finset.exists_max_image')} and {M('Finset.add_sum_erase')}; sorry-free on PR&nbsp;#172, "
"not yet merged to main.")
theorem_box("Theorem 6.2 (vcgIndividualRationality &mdash; in review)", CIG,
"Participation in the mechanism never yields negative utility: each agent&rsquo;s equilibrium utility is "
"non-negative, so a rational agent always prefers to participate.",
f"Proved on branch with the same Mathlib lemmas; sorry-free on PR&nbsp;#172, not yet merged to main.")

subsection("The trust-weighted allocation setting")
para("The mechanism in which Theorems&nbsp;6.1&ndash;6.2 hold is a trust-weighted Vickrey&ndash;Clarke&ndash;Groves "
"allocation. Each agent reports a private valuation for a governed action (for example, the right to emit a "
"high-privilege Khipu event); the mechanism allocates to the agent maximizing reported social value and charges each "
"winner the externality it imposes on the others &mdash; the classical VCG payment rule. The &lsquo;trust&rsquo; "
"weighting enters by scaling each agent&rsquo;s reported value by its &Lambda;-aggregated trust score, so that an "
"agent with a low conformance history is discounted before the allocation is computed. The dominant-strategy "
"property (Theorem&nbsp;6.1) is what makes the mechanism safe to deploy in an adversarial multi-agent setting: no "
"agent can improve its outcome by misreporting, so the governance layer does not need to model strategic lying. The "
"individual-rationality property (Theorem&nbsp;6.2) guarantees that honest participation is never punished, which is "
"the precondition for voluntary compliance.")
para("Two honesty caveats apply. First, the proofs are <b>branch-only</b>: until PR&nbsp;#172 merges, these are "
"in-review results, not locked-kernel theorems. Second, the truthfulness guarantee is about the <i>mechanism</i>, "
"not about the trust scores themselves &mdash; a strategyproof allocation over manipulated trust inputs is still "
"only as trustworthy as the &Lambda;-aggregation feeding it, which is exactly why the &Lambda; uniqueness question "
"(Conjecture&nbsp;1) and the mechanism truthfulness question are reported as two separate, independently-labeled "
"strands of the convergence.")
para("These two lemmas together establish that the trust-weighted allocation mechanism is strategyproof and "
"voluntary-participation-safe on the branch. They are <b>not</b> presented as landed kernel theorems: until PR&nbsp;#172 "
"merges and Lake CI is green on main, they sit in the in-review class of the claim discipline of &sect;1.2.")

# ======================================================================= 7
section("SLSA L1+L2 build provenance (achieved)")
para("Build-provenance posture is <b>SLSA L1+L2</b>. All <b>5/5</b> flagship GHCR images (a11oy, sentra, amaru, "
"killinchu, rosie) carry attested build-service provenance, verified with "
f"{M('slsa-verifier')} against the source repository and builder identity. This is a strict advance over v21, which "
"claimed only L1 (cosign-signed images). <b>SLSA L3 is not claimed</b> &mdash; it requires hardened, isolated "
"builders, which remain on the roadmap.")
table(["GHCR image","Provenance","slsa-verifier"],
[["**a11oy (platform)","build-service attested","PASS"],
 ["**sentra (immune)","build-service attested","PASS"],
 ["**amaru","build-service attested","PASS"],
 ["**killinchu (defense)","build-service attested","PASS"],
 ["**rosie (aide)","build-service attested","PASS"]],
[2.0*inch,2.5*inch,1.8*inch])
para("<i>Table&nbsp;7.1: All five flagship images reach SLSA L2 (attested build-service provenance), verified via "
f"{M('slsa-verifier')}.</i>")
codeblock([
"# Verify SLSA L2 build-service provenance for a flagship image:",
"slsa-verifier verify-image \\",
"  ghcr.io/szl-holdings/sentra@sha256:<digest> \\",
"  --source-uri github.com/szl-holdings/sentra \\",
"  --builder-id https://github.com/slsa-framework/...",
"# => PASSED: SLSA L2 verification (attested build-service provenance)",
])
para("<i>Listing&nbsp;7.1: SLSA L2 verification command. The attested provenance binds each image to its source "
"commit and the build service that produced it.</i>")

# ======================================================================= 8
section("Innovation Rounds 10&ndash;11 (frontier formalizations, in review)")
para("Round&nbsp;10 instilled frontier formalizations into lutar-lean; all are in review and labeled as such (none is "
"imported into the locked kernel). Round&nbsp;11 (the &lsquo;software-helping&rsquo; formula frontier) is in flight.")
table(["Round-10 module","PR","Representative statements"],
[["Physics","#177","Noether&rsquo;s theorem, Liouville&rsquo;s theorem, Hamiltonian structure, entropy bounds, A5-from-gauge-symmetry"],
 ["Quantum","#176","post-quantum signatures, Holevo bound, Kitaev, zero-knowledge, no-cloning&rarr;A5"],
 ["CS","#178","Byzantine quorum intersection, FLP impossibility, CAP, pipeline latency, decidability"],
 ["Crypto","#179","DSSE EUF-CMA, Rekor Merkle inclusion, Fulcio chain, BLS aggregation"],
 ["Distributed systems","pending","linearizability, total order, failure detection, replay safety"],
 ["Round-9 anatomy","#170","7-organ Lean modules"]],
[1.5*inch,0.7*inch,4.1*inch])
para("Two of these are especially relevant to the &Lambda; story: the physics module derives an A5-style permutation "
"symmetry from gauge symmetry, and the quantum module derives the same invariance from the no-cloning theorem &mdash; "
"two independent routes to the symmetry hypothesis the counterexample of &sect;4 showed is necessary. These remain "
"<b>in review</b> and are not claimed as landed kernel theorems; their value here is as converging evidence that A5 "
"is the natural missing hypothesis, not an ad-hoc patch.")

# ======================================================================= 9
section("Sim-to-Real doctrine transfer &mdash; the Walrus parallel (measured)")
para("Modeled on the Walrus physical foundation model (Polymathic AI), we treat the <b>locked doctrine kernel</b> "
"(749/14/163 @ c7c0ba17) as a <i>pretraining prior</i> and a customer&rsquo;s few-shot receipt set as "
"<i>fine-tuning data</i>. We define the <b>doctrine &alpha;-gap</b> = |OOD verdict accuracy &minus; in-distribution "
"verdict accuracy|, and measure it on a live N=60 run against SZL&rsquo;s sentra (immune) and a11oy (policy) organs.")
table(["Regime","Accuracy","&alpha;-gap"],
[["R0 control","1.00","&mdash;"],
 ["R1 adversarial","0.50","0.50"],
 ["R2 cross-jurisdictional","1.00","0.00"],
 ["R3 multimodal","1.00","0.00"],
 ["R4 temporal-drift","1.00","0.00"],
 ["R5 low-data","1.00","0.00"],
 ["**Mean","**&mdash;","**0.10"]],
[2.6*inch,1.8*inch,1.9*inch])
para("<i>Table&nbsp;9.1: Doctrine &alpha;-gap across five unseen compliance regimes (N=60, measured-not-proven).</i>")
para("Four of five unseen regimes transfer perfectly; adversarial (R1) transfers only partially because the immune "
"organ uses a signature blocklist that catches known attacks but misses semantically novel ones. We claim the "
"architecture <b>admits</b> sim-to-real transfer &mdash; <b>not</b> that it matches the downstream accuracy of "
"physical foundation models. The mean &alpha;-gap of 0.10 is a <b>measured</b> figure and is never described as a "
"theorem.")


# ---- measurement-theory subsection appended into A5 section ----
subsection("Why symmetry is the right missing hypothesis (measurement-theoretic frame)")
para("The counterexample does not merely show that <i>some</i> axiom is missing; it shows that the missing "
"hypothesis is <b>symmetry</b>, and symmetry is independently motivated before any uniqueness theorem is invoked. "
"Trust sub-scores are naturally <b>ratio-scale</b> quantities: they have a natural zero (total absence of "
"conformance) and a natural unit (the conformance baseline), so &lsquo;twice as trustworthy&rsquo; is meaningful. "
"Measurement theory establishes that the appropriate central tendency for ratio-scale data is the <b>geometric "
"mean</b>, because it is covariant under the admissible ratio-scale transformation x &rarr; r&middot;x: "
"&Lambda;(r&middot;x) = r&middot;&Lambda;(x), whereas the arithmetic mean is covariant only up to an additive shift "
"that is not a ratio-scale transformation.")
para("Permutation invariance (A5) is the formal statement that the <i>labels</i> on the trust sub-scores carry no "
"information &mdash; only their multiset of values does. In a governance reading: the trust verdict must not depend "
"on the order in which an auditor lists the evidence axes. The asymmetric counterexample "
"&Phi;(x&#8321;,x&#8322;)=x&#8321;<sup>2/3</sup>&middot;x&#8322;<sup>1/3</sup> privileges the first axis over the "
"second &mdash; exactly the manipulability A5 forbids. This is why A5 is a <i>structure field</i> the system always "
"intended, surfaced explicitly by the refutation, rather than a new idealization bolted on to rescue a theorem.")

# ---- new section: empirical operating characteristics ----
section("Empirical operating characteristics (measured, not proven)")
para("Alongside the mathematical convergence, v22 reports measured operating characteristics from the running "
"substrate, each labeled <b>measured-not-proven</b>. These are reproducible operational facts about the organs, "
"never theorems, and they are kept in a strictly separate column from anything proven.")
table(["Quantity (organ)","Measured value","Conditions"],
[["Receipt build, Khipu (p50 / p99)","11.5&nbsp;&micro;s / 50.7&nbsp;&micro;s","content-hashed receipt emission"],
 ["Receipt verify, Khipu","10.4&nbsp;&micro;s","hash-chain link check"],
 ["&Lambda;<sub>9</sub> aggregate, Ayni","3.12 / 3.29&nbsp;&micro;s","9-axis geometric-mean evaluation"],
 ["Governance overhead, Sentra (p50 / p99)","0.49&ndash;0.59&nbsp;ms / 1.27&nbsp;ms","over 24,800 governed calls"],
 ["&rho;-closure, Wasi-Rikuq","100% (8,000 / 8,000)","audit-closure pass rate"],
 ["Replay determinism, Puriq","5&times; byte-identical","repeated replay of a recorded trace"],
 ["WAYRA ingest","232 events chain-verified","always-learning ingest pathway"]],
[2.0*inch,1.8*inch,2.5*inch])
para("These figures characterize the running runtime; they do not bear on what is proven. The honesty doctrine keeps "
"the measured column strictly separate from the proven column &mdash; a measured latency is never described as a "
"theorem, and a theorem is never described as a benchmark. The &Lambda;<sub>9</sub> aggregate latency in particular "
"is a timing of the geometric-mean <i>evaluation</i>; it says nothing about the open uniqueness question, which "
"remains Conjecture&nbsp;1.")

# ---- new section: methodology / why honest labeling is a virtue ----
section("Methodology: the Lakatosian discipline of correction")
para("v22 is, methodologically, a case study in correcting a refuted conjecture in the open. We make the method "
"explicit because it is the through-line of the whole thesis lineage.")
subsection("Monster-barring, done honestly")
para("The historical &ldquo;Theorem&nbsp;1&rdquo; was a <i>naive conjecture</i> in Lakatos&rsquo;s sense; the "
"asymmetric mean &Phi; is the <i>monster</i> that refutes it. The dishonest response would be monster-barring by "
"redefinition &mdash; quietly narrowing &lsquo;aggregator&rsquo; until &Phi; is excluded without saying so. Instead "
"we <b>exhibit</b> the monster, <b>name</b> the guilty lemma (the unstated symmetry assumption), and state the "
"<b>revised</b> conjecture (uniqueness under {A1&ndash;A5} + A6&prime;) with its remaining gap disclosed. The "
"machine-checked counterexample is the mechanism that <i>causes</i> the Conjecture&nbsp;1 label: were unconditional "
"uniqueness true, the system would not so label &Lambda;.")
subsection("Why a disclosed obligation beats a hidden assumption")
para("By a process-reliabilist reading of formal epistemology, a &lsquo;proved&rsquo; label is trustworthy only if "
"the labeling process has a high accuracy rate. A corpus that calls everything &lsquo;proved&rsquo; carries less "
"information in its &lsquo;proved&rsquo; label than one that also accurately says &lsquo;conjecture&rsquo; and "
"&lsquo;in review&rsquo;. The single residual Cauchy_ND sorry, the branch-only status of the VCG lemmas, and the "
"in-review status of the Round&nbsp;10&ndash;11 modules are therefore reported as such. This is the same discipline "
"the drift gate enforces mechanically: the locked counts 749 / 14 / 163 at c7c0ba17 are numbers the gate refuses to "
"let move silently, so that no experimental obligation can be mistaken for a kernel-verified fact.")
boxed([P("<b>Remark (the convergence in one sentence).</b> v22 converges three previously-deferred strands &mdash; "
"the corrected &Lambda; axiomatization (A5 added, uniqueness still open), branch-proven mechanism truthfulness, and "
"attested SLSA&nbsp;L2 provenance &mdash; without upgrading a single conjecture to a theorem or moving a single "
"locked count.", thm)])

# ======================================================================= 10
section("Doctrine attestation (verbatim)")
para("We restate the load-bearing doctrine clauses verbatim, because every later version inherits them.")
bullets([
"<b>Doctrine version:</b> v11 LOCKED (v11.1 in flight, post-A5).",
"<b>Declarations:</b> 749 (pinned @ c7c0ba17); 794 post-A5 live.",
"<b>Unique axioms:</b> <b>14</b> &mdash; unchanged by A5, which is a structure field.",
"<b>Sorries:</b> 163 pinned (112 baseline + 51 Putnam); 191 post-A5 live.",
"<b>&Lambda; status:</b> <b>Conjecture&nbsp;1 &mdash; NOT a theorem.</b>",
f"<b>Supply chain:</b> <b>SLSA L1+L2</b> (5/5 GHCR images, attested build-service provenance via {M('slsa-verifier')}); "
"L3 not claimed.",
"<b>Section&nbsp;889 vendors:</b> Huawei, ZTE, Hytera, Hikvision, Dahua (exactly 5). <b>No</b> Iron&nbsp;Bank / "
"FedRAMP / CMMC&nbsp;L2+ / SWFT / Mission-Owner claims.",
])

# ======================================================================= 11
section("The honesty doctrine and Conjecture&nbsp;1")
para("v22 carries the honesty doctrine forward unchanged. We restate the clauses that every version inherits verbatim.")
numbered([
"<b>&Lambda; is Conjecture&nbsp;1.</b> The equal-weight geometric-mean &Lambda;-aggregator is never claimed the "
"unique aggregator under its axioms. Unconditional uniqueness under {A1&ndash;A5} is machine-checked <b>FALSE</b>; "
"conditional uniqueness holds only under the declared block-consistency axiom A6&prime; (v23).",
"<b>A5 is a structure field, not a new axiom.</b> The unique-axiom count remains <b>14</b>.",
"<b>Locked proven = exactly 5.</b> The lutar-lean kernel at c7c0ba17 proves exactly {F1, F11, F12, F18, F19} with "
"749 declarations, 14 unique axioms, and 163 sorries (112 baseline + 51 Putnam).",
f"<b>SLSA L1+L2 achieved</b> (5/5 GHCR images via {M('slsa-verifier')}); <b>L3 not claimed</b>.",
"<b>In-review PRs are labeled as such.</b> The VCG lemmas (PR&nbsp;#172) and the Round&nbsp;10&ndash;11 frontier "
"modules (#170, #173&ndash;#179) are branch-proven or in review and are <b>not</b> presented as landed kernel "
"theorems.",
"<b>Analogies are scaffolding.</b> Reed&ndash;Solomon &ne; holographic; event sourcing &ne; time travel; physics "
"analogies (Kuramoto, Bekenstein, Noether) are scaffolding, not the full physical results.",
])
boxed([P("<b>Conjecture&nbsp;1 (the Lutar invariant; never a theorem).</b> The equal-weight geometric mean "
"&Lambda;<sub>k</sub> is the correct unique trust aggregator for governed AI. This is an open claim about the "
"<i>right</i> axiomatization conditional on the Cauchy_ND chain closing on main; it is <b>not</b> a mathematical "
"theorem, and the substrate carries the &lsquo;Conjecture&nbsp;1&rsquo; label on &Lambda; in every artifact, "
"including this one.", thm)], bg=CONJBG)


# ---- new section: the alternative sufficient axioms (routes to uniqueness) ----
section("Routes to conditional uniqueness: the candidate sufficient axioms")
para("Because unconditional uniqueness under {A1&ndash;A5} is machine-checked false, conditional uniqueness requires "
"<i>one</i> further sufficient axiom. We surveyed the published characterizations and report the candidate routes "
"honestly, each with its independent governance motivation and its relative strength. v23 declares A6&prime; "
"(block-consistency) as the chosen route; v22 records the menu.")
table(["Route","Sufficient condition (informal)","Governance reading","Strength"],
[["**A6&prime; block-consistency","aggregating block means equals aggregating all elements","verdict must not depend on how the auditor partitions evidence","weakest sufficient"],
 ["**R+H reciprocity+homogeneity","&Lambda;(1/x) = 1/&Lambda;(x) and &Lambda;(r&middot;x)=r&middot;&Lambda;(x)","inverse comparisons stay inverse; uniform scaling scales the verdict","low"],
 ["**Bisymmetry","row/column interchange commutes","order of aggregation within and across sub-panels is irrelevant","moderate (near-assumes QAM)"],
 ["**Replacement/decomposability","a sub-block may be replaced by its own mean","auditing a department in isolation does not change the org verdict","low&ndash;moderate"]],
[1.55*inch,2.05*inch,1.95*inch,0.75*inch])
para("The common algebraic skeleton is: any route that pins <i>quasi-arithmetic</i> structure, combined with "
"homogeneity (A2, already present), automatically selects the geometric mean, because the only homogeneous "
"quasi-arithmetic means are the power means and positive homogeneity picks the exponent-1 power mean &mdash; the "
"geometric mean. The routes differ only in how wide a gap they leave between premise and conclusion; A6&prime; is "
"preferred precisely because it is phrased entirely in terms of the audit <i>process</i> and never mentions means or "
"exponents, so the geometric mean falls out as a theorem rather than being assumed.")
boxed([P("<b>Why this is still Conjecture&nbsp;1.</b> Each route above is <i>sufficient</i> for conditional "
"uniqueness, but each requires its declared axiom. v22 has merged A5 and partially closed the Cauchy_ND chain; it "
"has <b>not</b> discharged any of these further axioms on main. Until one is both declared and its chain closed with "
"a green Lake CI, &Lambda; uniqueness is conditional-at-best and the unconditional claim stays machine-checked "
"FALSE. Hence Conjecture&nbsp;1.", thm)], bg=CONJBG)

# ---- new section: open obligations and discharge routes ----
section("Open obligations surfaced or advanced by v22")
para("v22 advances several obligations without closing them on main. We tabulate them with their current status and "
"discharge route, so that the boundary between &lsquo;advanced&rsquo; and &lsquo;closed&rsquo; is never blurred.")
table(["Obligation","Status after v22","Discharge route"],
[["&Lambda; unconditional uniqueness","machine-checked FALSE","not dischargeable; remains a refutation"],
 ["&Lambda; conditional uniqueness","open on main (chain partial)","close Cauchy_ND t=0 sorry + declare A6&prime; (v23)"],
 ["Cauchy_ND topology branch","in review (PR #175)","merge TRUE-form continuity bridge"],
 ["Cauchy_ND functional-analysis","1 honest sorry (PR #173)","discharge the t=0 degenerate case"],
 ["Cauchy_ND symmetric branch","in review (PR #174)","merge with A5 dependency"],
 ["VCG dominant-strategy truth","branch-proven (PR #172)","merge to main + re-audit axioms"],
 ["VCG individual rationality","branch-proven (PR #172)","merge to main + re-audit axioms"],
 ["Round 10-11 frontier modules","in review (#170, #176-#179)","land under the drift gate"],
 ["SLSA L3","not claimed","hardened, isolated builders (roadmap)"],
 ["Adversarial transfer (R1 gap)","measured &alpha;-gap 0.50","semantic immune detection beyond blocklist"]],
[2.1*inch,1.85*inch,2.35*inch])
para("Reading the table top to bottom gives the exact convergence v22 represents: the unconditional uniqueness claim "
"is permanently refuted; the conditional claim is reduced to a single residual sorry plus a declared axiom; "
"mechanism truthfulness is proven and awaiting merge; the frontier modules are in review; and the supply-chain and "
"transfer frontiers are honestly bounded. Nothing in the table is reported as more closed than it is.")

# ======================================================================= 12
section("Position in the lineage")
table(["Ver","Date","Role"],
[["v19","2026-05-31","<b>The Verification Bridge.</b> Per-theorem verified index; locked-vs-experimental scope separation; drift gate."],
 ["v20","2026-06-01","<b>The Culmination.</b> The substrate as a twelve-organ verified anatomy with a tagged claim ledger."],
 ["v21","2026-06-01","<b>PURIQ-OS Substrate.</b> The runtime that executes the verified anatomy; 23 agentic formulas, 5 proved."],
 ["**v22","**2026-06-03","<b>Convergence (this paper).</b> A5 structure-field merge; VCG truthfulness proven on-branch; partial Cauchy closure; SLSA L1+L2."],
 ["v23","2026-06-06","<b>Unified Substrate.</b> Conditional &Lambda;-uniqueness under declared A6&prime;; unconditional uniqueness machine-checked FALSE; &Lambda; stays Conjecture 1."]],
[0.5*inch,0.9*inch,5.4*inch])
para("v22 is the convergence layer: v19 verifies, v20 presents the anatomy, v21 ships the runtime, <b>v22 converges "
"the deferred mathematics</b>, and v23 unifies it into a conditional &Lambda;-uniqueness theorem. The A5 correction, "
"the partial Cauchy chain, and the VCG branch proofs are exactly the obligations v23 builds on to state conditional "
"uniqueness under A6&prime; while keeping unconditional uniqueness machine-checked false.")

# ======================================================================= 13
section("Limitations and honest posture")
para("We state plainly what v22 does <i>not</i> establish.")
numbered([
"<b>&Lambda; remains Conjecture&nbsp;1.</b> The Cauchy_ND chain is not complete on main (one residual honest sorry "
"on the t=0 degenerate case); unconditional uniqueness under {A1&ndash;A5} is machine-checked FALSE.",
"<b>The VCG lemmas are branch-proven, not merged.</b> Theorems&nbsp;6.1&ndash;6.2 are sorry-free on PR&nbsp;#172 but "
"not yet part of the locked kernel.",
"<b>Round&nbsp;10&ndash;11 modules are in review.</b> The physics/quantum/CS/crypto/distributed-systems "
"formalizations (#170, #173&ndash;#179) are not imported into the locked library and do not change the locked counts.",
"<b>191 sorries are open</b> in the post-A5 live corpus (163 pinned + the A5-track delta). Doctrine v11 locked "
"numbers are verbatim: 749 / 14 / 163 @ c7c0ba17.",
"<b>SLSA L3 is not claimed.</b> L1+L2 is achieved (5/5 GHCR images); isolated, hardened builders remain roadmap.",
"<b>The Sim-to-Real &alpha;-gap is measured, not proven.</b> 0.10 mean across five regimes (N=60); the architecture "
"<i>admits</i> transfer but does not match physical foundation-model accuracy.",
])

# ======================================================================= 14
section("Future work")
numbered([
"Close the residual Cauchy_ND sorry (t=0 degenerate case) and merge PRs&nbsp;#173&ndash;#175 to main; only then "
"elevate &Lambda; to a conditional Theorem&nbsp;1 under A6&prime; (the v23 route).",
"Merge the VCG truthfulness lemmas (PR&nbsp;#172) into the locked kernel and re-audit the axiom footprint.",
"Land the Round&nbsp;10&ndash;11 frontier modules under the drift gate, re-checking the locked counts after each "
"merge.",
"Raise SLSA from L2 toward L3 (isolated, hardened builders) &mdash; roadmap, not yet achieved.",
"Extend the Sim-to-Real benchmark beyond N=60 and harden the immune organ against semantically novel adversarial "
"inputs (the R1 gap).",
"Continue closing the 163 residual sorries in lutar-lean.",
])

# ======================================================================= APPENDICES
pagebreak()
section("Appendix A: Lean build output and axiom audit")
para("The post-A5 corpus compiles under Lean&nbsp;4.13.0 (matching the lutar-lean toolchain). The locked kernel @ "
"c7c0ba17 is unchanged; the A5 structure field adds declarations but no new unique axiom.")
codeblock([
"$ lean --version",
"Lean (version 4.13.0, commit 6d22e0e5cc5a, Release)",
"",
"# Locked kernel (pinned @ c7c0ba17):",
"  749 declarations / 14 unique axioms / 163 sorries (112 baseline + 51 Putnam)",
"",
"# Post-A5 live corpus (measured 974e5e0c, 2026-06-03 17:32Z):",
"  794 declarations / 14 unique axioms / 191 sorries",
"",
"#print axioms Lambda_A5_perm_invariant",
"  => [propext, Quot.sound]   -- Lean-core only; A5 is a structure field",
"",
"# A5 merge (PR #148): unique-axiom count UNCHANGED at 14.",
])

section("Appendix B: Verification commands")
codeblock([
"# Verify the A5 lemma is sorry-free:",
"lean LutarAxioms.lean   # exit 0; Lambda_A5_perm_invariant : sorry-free",
"",
"# Verify SLSA L2 build-service provenance (5/5 flagship images):",
"slsa-verifier verify-image ghcr.io/szl-holdings/<image>@sha256:<digest> \\",
"  --source-uri github.com/szl-holdings/<image>",
"",
"# Reproduce the Sim-to-Real alpha-gap benchmark (N=60):",
"python team/sim2real-compliance/run_benchmark.py --n 60 --regimes R0..R5",
"",
"# Doctrine v11 (LOCKED @ c7c0ba17):",
"#   749 declarations / 14 unique axioms / 163 sorries (112 baseline + 51 Putnam)",
])

section("Appendix C: Reproducibility and pins")
para("The artifacts behind every claim, pinned for reproduction.")
table(["Artifact","Pin / identifier"],
[["Locked kernel commit","lutar-lean @ c7c0ba17"],
 ["Locked counts","749 declarations / 14 unique axioms / 163 sorries (112 baseline + 51 Putnam)"],
 ["Post-A5 live counts","794 declarations / 14 unique axioms / 191 sorries (974e5e0c)"],
 ["Locked formulas","{F1, F11, F12, F18, F19}"],
 ["A5 merge","PR #148 (IsPermutationInvariant + A5 structure field; sorry-free)"],
 ["VCG lemmas (in review)","PR #172 (vcgDominantStrategyTruth, vcgIndividualRationality)"],
 ["Cauchy_ND chain (in review)","PRs #173 / #174 / #175 (1 residual honest sorry at t=0)"],
 ["Round 10-11 modules (in review)","PRs #170, #176, #177, #178, #179"],
 ["Lean toolchain","Lean 4.13.0 (commit 6d22e0e5cc5a)"],
 ["SLSA level","L1+L2 (5/5 GHCR images via slsa-verifier); L3 not claimed"],
 ["Sim-to-Real benchmark","N=60, mean alpha-gap 0.10 across R0-R5"],
 ["Concept DOI (always-latest)","10.5281/zenodo.19944926"],
 ["v11 metrics DOI","10.5281/zenodo.20119582"],
 ["ORCID","0009-0001-0110-4173"]],
[1.9*inch,4.4*inch])

# ======================================================================= REFERENCES
references_block([
'Acz&eacute;l, J. (1948). On mean values. <i>Bull. Amer. Math. Soc.</i> 54(4):392&ndash;400. <a href="https://doi.org/10.1090/S0002-9904-1948-09020-9" color="#01696F">doi:10.1090/S0002-9904-1948-09020-9</a>',
'Axelrod, R. &amp; Hamilton, W. D. (1981). The evolution of cooperation. <i>Science</i> 211(4489):1390&ndash;1396. <a href="https://doi.org/10.1126/science.7466396" color="#01696F">doi:10.1126/science.7466396</a>',
'Cs&aacute;t&oacute;, L. (2018). Characterization of the row geometric mean ranking with a group consensus axiom. <i>Group Decision and Negotiation</i> 27:1011&ndash;1027. <a href="https://doi.org/10.1007/s10726-018-9589-3" color="#01696F">doi:10.1007/s10726-018-9589-3</a>',
'de Moura, L. &amp; Ullrich, S. (2021). The Lean 4 Theorem Prover and Programming Language. <i>CADE 28</i>, LNCS 12699, 625&ndash;635. <a href="https://doi.org/10.1007/978-3-030-79876-5_37" color="#01696F">doi:10.1007/978-3-030-79876-5_37</a>',
'Goguen, J. A. &amp; Meseguer, J. (1982). Security Policies and Security Models. <i>IEEE Symp. Security &amp; Privacy</i>, 11&ndash;20. <a href="https://doi.org/10.1109/SP.1982.10014" color="#01696F">doi:10.1109/SP.1982.10014</a>',
'Hardy, G. H., Littlewood, J. E. &amp; P&oacute;lya, G. (1934). <i>Inequalities</i>. Cambridge University Press.',
'Kolmogorov, A. N. (1930). Sur la notion de la moyenne. <i>Atti Accad. Naz. Lincei</i> 12:388&ndash;391.',
'McCabe, M. et&nbsp;al. (2025). Walrus: A foundation model for the physical sciences. <i>Polymathic AI</i>. <a href="https://polymathic-ai.org" color="#01696F">polymathic-ai.org</a>',
'Merkle, R. C. (1987). A Digital Signature Based on a Conventional Encryption Function. <i>CRYPTO &rsquo;87</i>, LNCS 293, 369&ndash;378. <a href="https://doi.org/10.1007/3-540-48184-2_32" color="#01696F">doi:10.1007/3-540-48184-2_32</a>',
'Nagumo, M. (1930). &Uuml;ber eine Klasse der Mittelwerte. <i>Japanese J. Math.</i> 7:71&ndash;79.',
'Open Source Security Foundation (2023). SLSA: Supply-chain Levels for Software Artifacts, v1.0. <a href="https://slsa.dev/spec/v1.0/levels" color="#01696F">slsa.dev/spec/v1.0/levels</a>',
'Vickrey, W. (1961). Counterspeculation, auctions, and competitive sealed tenders. <i>J. Finance</i> 16(1):8&ndash;37. <a href="https://doi.org/10.1111/j.1540-6261.1961.tb02789.x" color="#01696F">doi:10.1111/j.1540-6261.1961.tb02789.x</a>',
'Voorneveld, M. (2008). The possibility of impossible stairways. <i>J. Econ. Theory</i> 143(1):116&ndash;135.',
])

signoff_block("A5 is a structure field, not a new axiom (unique-axiom count remains 14). "
"&Lambda; is Conjecture&nbsp;1; unconditional uniqueness is machine-checked FALSE. "
"SLSA L1+L2 achieved (5/5 GHCR images); L3 not claimed. Quechua organ names are brand naming only.")
build(os.path.join(HERE, "main.pdf"),
      "Convergence (v22): The Lambda-Uniqueness Chain, Mechanism Truthfulness, and Sim-to-Real Doctrine Transfer",
      "Convergence (v22)")
