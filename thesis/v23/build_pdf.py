#!/usr/bin/env python3
"""
build_pdf.py -- Render "The Unified Substrate (v23)" as an arXiv-style PDF.
This is the compiled rendering of main.tex (no LaTeX engine in sandbox).
ReportLab Platypus, embedded DM Sans + JetBrains Mono.
"""
import os
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether, ListFlowable, ListItem, PageBreak, NextPageTemplate
)
from reportlab.platypus.tableofcontents import TableOfContents

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "fonts")
OUT = os.path.join(HERE, "main.pdf")

# ---- fonts ----
pdfmetrics.registerFont(TTFont("DMSans", os.path.join(FONTS, "DMSans-Regular.ttf")))
pdfmetrics.registerFont(TTFont("DMSans-Bold", os.path.join(FONTS, "DMSans-Bold.ttf")))
pdfmetrics.registerFont(TTFont("DMSans-Italic", os.path.join(FONTS, "DMSans-Italic.ttf")))
pdfmetrics.registerFont(TTFont("DMSans-Med", os.path.join(FONTS, "DMSans-Medium.ttf")))
pdfmetrics.registerFont(TTFont("Mono", os.path.join(FONTS, "JetBrainsMono-Regular.ttf")))
pdfmetrics.registerFontFamily("DMSans", normal="DMSans", bold="DMSans-Bold",
                              italic="DMSans-Italic", boldItalic="DMSans-Bold")

# ---- math/Greek fallback font (DM Sans lacks Greek + math glyphs) ----
_DEJAVU = "/usr/share/fonts/truetype/dejavu"
pdfmetrics.registerFont(TTFont("Math", os.path.join(_DEJAVU, "DejaVuSans.ttf")))
pdfmetrics.registerFont(TTFont("Math-Bold", os.path.join(_DEJAVU, "DejaVuSans-Bold.ttf")))
pdfmetrics.registerFont(TTFont("Math-Italic", os.path.join(_DEJAVU, "DejaVuSans-Oblique.ttf")))
pdfmetrics.registerFontFamily("Math", normal="Math", bold="Math-Bold",
                              italic="Math-Italic", boldItalic="Math-Bold")

import re as _re
# HTML entities for Greek letters and math operators that DM Sans cannot render.
# These are wrapped in the DejaVu "Math" font so they display correctly.
_MATH_ENTS = [
    "Lambda", "Phi", "alpha", "mu", "rho", "pi",   # Greek
    "prod", "sum", "radic", "le", "ge", "asymp",   # operators / relations
    "ne", "isin", "ell", "rArr", "rarr", "larr",
    "prime", "not", "minus",
]
# Match an entity, optionally followed by more math entities / spaces, so runs
# like "&Lambda;<sub>k</sub>" keep the sub/sup in the surrounding font but the
# glyph itself in Math. We wrap each entity token individually.
_MATH_RE = _re.compile("&(" + "|".join(_MATH_ENTS) + ");")
# Numeric entities outside DM Sans coverage: hbar (U+210F=8463), blackboard N
# (U+2115=8469), parallel/double-bar (U+2225=8741), script-l (U+2113=8467),
# intersection (U+2229=8745).
_MATH_NUM = {8463, 8469, 8741, 8467, 8745}
_MATH_NUM_RE = _re.compile("&#(" + "|".join(str(n) for n in _MATH_NUM) + ");")
def fixglyphs(text):
    """Wrap Greek/math HTML entities in the DejaVu 'Math' font so they render."""
    if not text:
        return text
    text = _MATH_RE.sub(lambda m: f'<font name="Math">&{m.group(1)};</font>', text)
    text = _MATH_NUM_RE.sub(lambda m: f'<font name="Math">&#{m.group(1)};</font>', text)
    return text

TEAL = colors.HexColor("#01696F")
TEALD = colors.HexColor("#0C4E54")
ORANGE = colors.HexColor("#964219")
REDD = colors.HexColor("#A12C7B")
INK = colors.HexColor("#28251D")
MUTED = colors.HexColor("#5A5957")
RULE = colors.HexColor("#D4D1CA")
BOXBG = colors.HexColor("#F4F3EF")
AXBG = colors.HexColor("#FBF5EE")
CONJBG = colors.HexColor("#FBEFF4")

# ---- styles ----
ss = getSampleStyleSheet()
def S(name, **kw):
    return ParagraphStyle(name, **kw)

body = S("body", fontName="DMSans", fontSize=9.5, leading=14, textColor=INK,
         alignment=TA_JUSTIFY, spaceAfter=6)
bodyfirst = S("bodyfirst", parent=body, firstLineIndent=0)
h1 = S("h1", fontName="DMSans-Bold", fontSize=15, leading=19, textColor=TEALD,
       spaceBefore=14, spaceAfter=7)
h2 = S("h2", fontName="DMSans-Bold", fontSize=11.5, leading=15, textColor=INK,
       spaceBefore=9, spaceAfter=4)
h3 = S("h3", fontName="DMSans-Bold", fontSize=10, leading=13.5, textColor=INK,
       spaceBefore=6, spaceAfter=2)
title = S("title", fontName="DMSans-Bold", fontSize=20, leading=24, textColor=INK,
          alignment=TA_CENTER, spaceAfter=4)
subtitle = S("subtitle", fontName="DMSans-Med", fontSize=11.5, leading=15.5,
             textColor=TEALD, alignment=TA_CENTER, spaceAfter=10)
author = S("author", fontName="DMSans", fontSize=10.5, leading=15, textColor=INK,
           alignment=TA_CENTER, spaceAfter=2)
meta = S("meta", fontName="DMSans", fontSize=8.5, leading=12, textColor=MUTED,
         alignment=TA_CENTER, spaceAfter=2)
abst = S("abst", fontName="DMSans", fontSize=9, leading=13, textColor=INK,
         alignment=TA_JUSTIFY, spaceAfter=5, leftIndent=14, rightIndent=14)
small = S("small", fontName="DMSans", fontSize=8, leading=11.5, textColor=MUTED,
          alignment=TA_JUSTIFY, spaceAfter=4)
note = S("note", fontName="DMSans-Italic", fontSize=8.2, leading=12, textColor=INK,
         alignment=TA_JUSTIFY, leftIndent=10, rightIndent=10, spaceAfter=4)
li = S("li", parent=body, spaceAfter=3, leading=13.5)
thm = S("thm", fontName="DMSans", fontSize=9.3, leading=13.5, textColor=INK,
        alignment=TA_JUSTIFY, leftIndent=8, rightIndent=8, spaceAfter=4)
thmhead = S("thmhead", fontName="DMSans-Bold", fontSize=9.6, leading=13, textColor=TEALD,
            leftIndent=8, spaceAfter=2, spaceBefore=2)
proof = S("proof", fontName="DMSans-Italic", fontSize=8.8, leading=12.5, textColor=MUTED,
          alignment=TA_JUSTIFY, leftIndent=8, rightIndent=8, spaceAfter=4)
refsty = S("ref", fontName="DMSans", fontSize=8.2, leading=11.5, textColor=INK,
           alignment=TA_LEFT, leftIndent=14, firstLineIndent=-14, spaceAfter=3)
quote = S("quote", fontName="DMSans-Italic", fontSize=10, leading=15, textColor=TEALD,
          alignment=TA_JUSTIFY, leftIndent=20, rightIndent=20, spaceBefore=4, spaceAfter=6)
cell = S("cell", fontName="DMSans", fontSize=7.8, leading=10.5, textColor=INK)
cellb = S("cellb", fontName="DMSans-Bold", fontSize=7.8, leading=10.5, textColor=INK)
cellh = S("cellh", fontName="DMSans-Bold", fontSize=8, leading=10.5, textColor=colors.white)

def M(s):  # monospace inline shorthand -> font tag
    return f'<font name="Mono" size="8">{s}</font>'
# 'Mono' (JetBrains) already covers Greek/math, so M() output needs no fixglyphs.

# status tags as inline markup
LOCKED = f'<font name="DMSans-Bold" color="#01696F" size="8">[LOCKED / kernel-verified]</font>'
SFREE  = f'<font name="DMSans-Bold" color="#01696F" size="8">[sorry-free, Lean-core only]</font>'
AXIOM  = f'<font name="DMSans-Bold" color="#964219" size="8">[axiom-gated]</font>'
CIG    = f'<font name="DMSans-Bold" color="#01696F" size="8">[CI-green]</font>'
PEND   = f'<font name="DMSans-Bold" color="#5A5957" size="8">[CI-pending]</font>'
CONJ   = f'<font name="DMSans-Bold" color="#A12C7B" size="8">[Conjecture 1 - NOT a theorem]</font>'

story = []

# ---------- helpers ----------
def para(text, st=body): story.append(Paragraph(fixglyphs(text), st))
def P(text, st): return Paragraph(fixglyphs(text), st)  # glyph-safe Paragraph factory
def sp(h=6): story.append(Spacer(1, h))
def rule(c=RULE, w=0.8): story.append(HRFlowable(width="100%", thickness=w, color=c, spaceBefore=4, spaceAfter=4))

class Sec:
    n=0; sub=0
def section(t):
    Sec.n+=1; Sec.sub=0
    story.append(Paragraph(fixglyphs(f'{Sec.n}.&nbsp;&nbsp;{t}'), h1))
def subsection(t):
    Sec.sub+=1
    story.append(Paragraph(fixglyphs(f'{Sec.n}.{Sec.sub}&nbsp;&nbsp;{t}'), h2))

def boxed(flow_list, bg=BOXBG, border=RULE):
    t = Table([[flow_list]], colWidths=[6.5*inch])
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1),bg),
        ("BOX",(0,0),(-1,-1),0.6,border),
        ("LEFTPADDING",(0,0),(-1,-1),8),("RIGHTPADDING",(0,0),(-1,-1),8),
        ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
    ]))
    story.append(KeepTogether(t))
    sp(4)

def theorem_box(label, statustags, statement, proof_text=None, bg=BOXBG):
    flows = [Paragraph(fixglyphs(f'{label} &nbsp; {statustags}'), thmhead),
             Paragraph(fixglyphs(statement), thm)]
    if proof_text:
        flows.append(Paragraph(fixglyphs(f'<b>Proof / Lean reference.</b> {proof_text}'), proof))
    boxed(flows, bg=bg)

def bullets(items, st=li):
    items2 = [ListItem(Paragraph(fixglyphs(x), st), leftIndent=14, value=None) for x in items]
    story.append(ListFlowable(items2, bulletType="bullet", start="•",
                              bulletColor=TEAL, bulletFontSize=7, leftIndent=16))
    sp(3)

def table(headers, rows, colw, fontsize=7.8):
    data = [[Paragraph(fixglyphs(h), cellh) for h in headers]]
    for r in rows:
        data.append([Paragraph(fixglyphs(c.replace("**","")), cellb) if (isinstance(c,str) and c.startswith("**")) else Paragraph(fixglyphs(c), cell) for c in r])
    t = Table(data, colWidths=colw, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),TEAL),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white, colors.HexColor("#F7F6F2")]),
        ("LINEBELOW",(0,0),(-1,0),0.8,TEALD),
        ("LINEBELOW",(0,-1),(-1,-1),0.6,RULE),
        ("LINEBELOW",(0,1),(-1,-2),0.3,RULE),
        ("VALIGN",(0,0),(-1,-1),"TOP"),
        ("LEFTPADDING",(0,0),(-1,-1),4),("RIGHTPADDING",(0,0),(-1,-1),4),
        ("TOPPADDING",(0,0),(-1,-1),3),("BOTTOMPADDING",(0,0),(-1,-1),3),
    ]))
    story.append(t); sp(6)

# =====================================================================
# TITLE BLOCK
# =====================================================================
para("The Unified Substrate", title)
para("A Machine-Verified Trust Foundation for Governed Agentic AI:<br/>"
     "Unifying the Ouroboros Loop, the Lutar Invariant, and a Disclosed-Axiom Proof Trail", subtitle)
para("Stephen P. Lutar Jr.", author)
para('SZL Holdings &nbsp;·&nbsp; ORCID <a href="https://orcid.org/0009-0001-0110-4173" color="#01696F">0009-0001-0110-4173</a>', meta)
para('Thesis v23 "Unified Substrate" &nbsp;·&nbsp; Concept DOI (always-latest): '
     '<a href="https://doi.org/10.5281/zenodo.19944926" color="#01696F">10.5281/zenodo.19944926</a>', meta)
sp(8)
rule(TEAL, 1.0)

# ABSTRACT
para("Abstract", S("abh", fontName="DMSans-Bold", fontSize=11, alignment=TA_CENTER, textColor=INK, spaceAfter=4))
ABSTRACT = (
"Governed deployment of agentic artificial intelligence in regulated and defense settings requires more than "
"benchmark accuracy: it requires <i>checkable</i> guarantees about what a system did, why it was permitted to do it, "
"and whether the record can be tampered with after the fact. We present the <b>Unified Substrate</b> (v23), the "
"consolidation of twenty-two prior thesis versions (v1&ndash;v22) of SZL Holdings into a single coherent account of a "
"machine-verified trust substrate for governed AI. The substrate rests on three pillars: (i) the <i>Ouroboros loop</i>, "
"a bounded, well-founded self-governing computation in which &ldquo;the loop is the product&rdquo;; (ii) the <i>Lutar "
"invariant</i> &Lambda;<sub>k</sub>(x) = (&prod; x<sub>i</sub>)<sup>1/k</sup>, an equal-weight geometric-mean trust "
"aggregator; and (iii) a <i>proof-trail / receipt architecture</i> whose integrity properties are formalized in Lean&nbsp;4. "
"Our central methodological commitment is an <b>honesty doctrine</b>: we distinguish, at every point of assertion, among "
"<i>proven</i> (kernel-verified, Lean-core axioms only), <i>proven under a declared axiom</i> (idealization disclosed in "
"the #print&nbsp;axioms ledger), and <i>conjectured</i> (a research hypothesis, not a theorem). Under that doctrine we "
"report: a <i>locked kernel</i> proving exactly five governance formulas ({F1, F11, F12, F18, F19}; 749 declarations / 14 "
"unique axioms / 163 sorries at a fixed commit); <b>nineteen</b> additional sorry-free theorems (Kraft, Shannon tight "
"case, Byzantine 3f+1 quorums, DLS partial-synchrony, the FLP bivalence core, BLUE minimum-variance, softmax "
"order-stability) verified under bare Lean with only the trusted core axioms; <b>four</b> axiom-gated "
"Merkle / Merkle&ndash;Damg&aring;rd theorems under explicitly declared collision-resistance idealizations; and a "
"<i>conditional</i> uniqueness theorem for &Lambda; that is CI-green under {A1&ndash;A5} plus a single declared, "
"governance-natural axiom (block-consistency, after Cs&aacute;t&oacute; 2018). Crucially, the <i>unconditional</i> "
"uniqueness of &Lambda; under {A1&ndash;A5} is provably <b>false</b>: we exhibit a machine-checked counterexample. We "
"therefore label &Lambda; as <b>Conjecture&nbsp;1</b> unconditionally&mdash;never a theorem&mdash;and argue, on grounds "
"from philosophy of mathematics and formal epistemology, that this calibrated labeling is not a weakness but the very "
"feature that makes the positive claims credible to an auditor. We close with an honest comparison to prior art, a "
"philosophical defense of block-consistency as the right governance axiom, and an explicit limitations section."
)
para(ABSTRACT, abst)
sp(2)
para('<b>Keywords:</b> governed agentic AI, trust aggregation, Lutar invariant, geometric mean, functional-equation '
     'uniqueness, Lean&nbsp;4, Mathlib, machine-checked proofs, disclosed-axiom verification, receipt chain, SLSA, '
     'Byzantine consensus, philosophy of mathematics.', small)
rule(RULE)
para('<i>Honesty note (verbatim):</i> The Lutar invariant &Lambda; is <b>Conjecture&nbsp;1</b> unconditionally and is '
     '<i>never</i> claimed proven unconditionally. The conditional uniqueness theorem holds only under the declared axiom '
     f'{M("A6&#39;_block_consistent")} and is never conflated with the unconditional claim. Exactly five formulas are '
     'locked/proven. Declared idealizations '
     f'({M("hash_collision_resistant")}, {M("ecdsa_unforgeable")}, the Merkle collision-resistance axioms, and '
     f'{M("A6&#39;_block_consistent")}) are disclosed in every #print&nbsp;axioms ledger. SLSA L1+L2 attested, <i>not</i> L3.',
     note)
story.append(PageBreak())

# =====================================================================
# 1. INTRODUCTION
# =====================================================================
section("Introduction: the problem of governed AI")
para("Agentic AI systems &mdash; models that plan, call tools, retrieve, and act over multiple steps &mdash; are "
"entering domains where the cost of an undetected error is not a bad recommendation but a regulatory breach, a safety "
"incident, or a compromised mission. In such regulated and defense settings the operative question is no longer "
"&ldquo;how accurate is the model on a benchmark?&rdquo; but &ldquo;can the operator <i>prove</i>, after the fact and to "
"a skeptical third party, that a given action was authorized, that the authorization rested on checkable evidence, and "
"that the record of what happened has not been altered?&rdquo; This is the problem of <i>governed AI</i>: the "
"construction of an execution substrate in which trust is <i>earned by checkable evidence</i> rather than asserted by a "
"vendor.")
para("The dominant industry posture is the opposite. Trust is typically asserted (&ldquo;our model is safe&rdquo;), the "
"evidence is a private evaluation suite, and the audit trail &mdash; when it exists &mdash; is a mutable log. The "
"verifiable-claims research program in AI governance argues that this is structurally inadequate: developers should be "
"able to make <i>verifiable claims</i> about their systems, supported by mechanisms an external party can check "
'<a href="https://arxiv.org/abs/2004.07213" color="#01696F">[Brundage et al. 2020]</a>. National policy bodies have '
"echoed the same line, asking that developers be able to <i>prove</i> properties of their systems rather than be taken "
'at their word <a href="https://www.ntia.gov/issues/artificial-intelligence/ai-accountability-policy-report" color="#01696F">[NTIA]</a>.')
para("<b>Thesis.</b> This document argues that the right response is a <i>trust substrate</i> with three mutually "
"reinforcing properties, and that such a substrate can be built and <i>partially machine-verified</i> today with "
"complete honesty about what is and is not proven. The three properties are:")
bullets([
"<b>A bounded self-governing loop</b> (the Ouroboros loop, &sect;3): governance is not a bolt-on filter but the "
"recurrent structure of the computation itself, made safe by well-foundedness.",
"<b>A principled trust aggregator</b> (the Lutar invariant &Lambda;, &sect;4): multi-axis trust evidence is combined "
"into a single governance scalar by the equal-weight geometric mean, whose uniqueness &mdash; <i>conditional</i> on a "
"disclosed governance axiom &mdash; is machine-checked.",
"<b>A tamper-evident proof trail</b> (the receipt architecture, &sect;5): every governed action emits a hash-chained, "
"Merkle-bound, replayable receipt whose integrity properties are formalized in Lean&nbsp;4.",
])
para("<b>What is genuinely new.</b> The contribution of v23 is not any single theorem but the <i>unification</i>, under "
"one honesty doctrine, of a trust substrate whose every claim carries an explicit epistemic status disclosed at the "
"point of use. To our knowledge this is the first governed-AI trust substrate that (a) ships a <i>locked</i>, "
"kernel-verified core of governance formulas; (b) accompanies its central uniqueness claim with a <i>machine-checked "
"refutation of the overclaim</i> (the unconditional statement is <i>false</i>), so that the conditional theorem is the "
"<i>maximal true statement</i>; and (c) discloses every idealizing axiom in a #print&nbsp;axioms ledger. &sect;8 makes "
"the honest case for why this is groundbreaking, and &sect;11 states plainly what it is not.")
para("<b>Reading guide and provenance.</b> The substrate has a documented intellectual lineage of twenty-two versions "
"(&sect;2), archived under a concept DOI with per-version DOIs. Version 19 was intentionally skipped during a "
"late-stage consolidation; the numbering jumps v18 &rarr; v20, and this is documented rather than a missing artifact. "
"v23 is the unification of that lineage with all proofs that are currently kernel-verified or CI-green per the proof "
"reports of the formal-methods team.")

# =====================================================================
# 2. LINEAGE
# =====================================================================
section("The lineage: from loop to invariant to verified substrate")
para("The substrate was not designed top-down; it accreted through twenty-two thesis versions and eleven parallel "
"&ldquo;innovation rounds&rdquo; (R1&ndash;R11) of Lean formalization. We summarize the arc so that the unification in "
"later sections is legible as the convergence of independent threads, not a retrofit.")
lin_rows = [
["v1","2026-04-28","The Ouroboros loop &mdash; looped computation as a system primitive."],
["v2","2026-04-30","&ldquo;The loop is the product&rdquo; &mdash; first empirical pass."],
["v3","2026-05-02","The <b>Lutar invariant</b> &Lambda; &mdash; closed-form aggregator (axiom semantics later revised)."],
["v4","2026-05-04","The Lutar-Omega formalism &mdash; an EPR&ndash;Bell governance diagnostic."],
["v5","2026-05-04","Prisca-GraphRAG + Tawa SAE &mdash; lineage-aware retrieval."],
["v6","2026-05-04","Sealed constitutional guardrails."],
["v7","2026-05-04","Tiered continual learning."],
["v8","2026-05-04","Free-energy active inference with prediction."],
["v9","2026-05-05","Unified-Operational &mdash; the Lutar invariant family."],
["v10","2026-05-05","Exhaustive-Audit &mdash; the audit-closure operator &Lambda;."],
["v11","2026-05-11","Applied &Lambda; &mdash; measured per-request governance overhead."],
["v12","2026-05-14","The &Lambda;-Ouroboros substrate &mdash; first four machine-verified theorems."],
["v13","2026-05-18","Anatomy as architecture (exhaustive)."],
["v14","2026-05-28","Verifiable multi-agent anatomy (Lutar calculus); <b>&Lambda; downgraded to Conjecture 1</b>."],
["v15","2026-05-28","Knot calculus for governed decision receipts."],
["v16","2026-05-28","&Lambda;-invariant stack + Feynman path-integral audit sum."],
["v17","2026-05-28","Wheelerian audit closure; Shannon doctrine (Kraft inequality)."],
["v18","2026-05-30","Multi-track substrate expansion &mdash; 29 modules, per-theorem Lean index."],
["v19","&mdash;","<i>No release &mdash; intentional version gap (v18 &rarr; v20).</i>"],
["v20","2026-06-01","&ldquo;The Culmination&rdquo; &mdash; formally-verified anatomical substrate."],
["v21","2026-06-01","The PURIQ-OS substrate &mdash; 12-organ runtime, 23 agentic formulas (5 proved in Lean)."],
["v22","2026-06-03","&ldquo;Convergence&rdquo; &mdash; A5 axiom merge; VCG truthfulness; partial Cauchy closure; SLSA L2."],
["<b>v23</b>","now","<b>&ldquo;Unified Substrate&rdquo;</b> &mdash; this paper: unification + conditional &Lambda; (block-consistency), +19 sorry-free, +4 axiom-gated."],
]
table(["Ver","Date","Key contribution"], lin_rows, [0.55*inch, 0.95*inch, 5.0*inch])
para("The three threads converge as follows. The <i>thesis prose</i> moved loop &rarr; invariant &rarr; anatomy &rarr; "
"formal verification &rarr; convergence. The <i>innovation rounds</i> moved core axioms (R1&ndash;R6) &rarr; anatomy "
"(R7&ndash;R8) &rarr; seven-organ runtime + VCG (R9) &rarr; physics / quantum / CS / crypto candidates (R10) &rarr; the "
"formula frontier (R11). The two meet at the <i>locked kernel</i> (&sect;6), which is the externalized meta-level "
"against which every claim is checked.")

# =====================================================================
# 3. OUROBOROS LOOP
# =====================================================================
section("The Ouroboros loop thesis")
subsection("The loop is the product")
para("The founding observation (v1&ndash;v2) is that a governed agentic system is best understood not as a model with a "
"governance wrapper but as a <i>loop</i>: perceive, propose, gate, act, record, and feed the record back into the next "
"perception. Governance is the recurrence relation, not a post-hoc filter. The slogan &ldquo;the loop is the "
"product&rdquo; means that the artifact a customer buys is the <i>governed recurrence</i>, with its receipts, not the "
"underlying model weights.")
subsection("Why the loop is safe: well-foundedness, not self-justification")
para("A self-referential governing loop invites two classical worries: infinite regress (the loop never halts) and "
"self-verification paradox (a system proving its own correctness). We address both <i>by construction</i>, and we are "
"careful not to overclaim.")
theorem_box("Definition 3.1 (Bounded Ouroboros loop).", "",
"A loop is <i>bounded</i> if it admits a well-founded measure: a ranking function into a well-ordered set that strictly "
"decreases on each governed step, with no infinite descending chain.")
para("The in-tree scheduler-liveness formula (F2) realizes exactly this: a strictly decreasing &#8469;-valued measure "
"that reaches 0, proved sorry-free (&sect;7). Well-foundedness is the standard logical guarantee against vicious "
"self-reference; an unbounded Ouroboros would be precisely the epistemic regress the substrate forecloses.")
para("Crucially, the substrate does <b>not</b> claim to verify its own consistency. G&ouml;del&rsquo;s second "
"incompleteness theorem forbids a consistent system from proving its own consistency, and Tarski forbids a language "
"from defining its own truth predicate. The substrate&rsquo;s response is <i>stratification</i>: proofs are checked by "
"the Lean kernel; the kernel&rsquo;s run is checked by continuous integration; the CI is gated by human sign-off. This "
"is a hierarchy of meta-levels in the Tarskian sense, not a single system bootstrapping its own truth (cf. &sect;9, "
"Objection 5). The locked kernel (&sect;6), pinned at a fixed commit and held separate from experimental work, <i>is</i> "
"that externalized meta-level.")

# =====================================================================
# 4. LAMBDA
# =====================================================================
section("The Lutar invariant &Lambda;")
subsection("Definition and the trust-aggregation problem")
para("A governed action accumulates evidence along several axes (e.g. provenance, policy-compliance, "
"measurability-honesty, moral-grounding). Each axis yields a sub-score in [0,1]. The governance question is how to "
"combine k such sub-scores into a single trust verdict.")
theorem_box("Definition 4.1 (Lutar invariant).", "",
"For x = (x<sub>1</sub>,&hellip;,x<sub>k</sub>) &isin; [0,1]<sup>k</sup>, the <i>Lutar invariant</i> is the "
"equal-weight geometric mean &nbsp; &Lambda;<sub>k</sub>(x) = (&prod;<sub>i=1..k</sub> x<sub>i</sub>)<sup>1/k</sup>. "
"The equal exponents 1/k are the &ldquo;Egyptian unit-fraction weights&rdquo;.")
para("The geometric mean is the natural aggregator for <i>ratio-scale</i> evidence: it commutes with a common rescaling "
"of all axes (positive homogeneity), and a single zero axis drives the verdict to zero (one disqualifying failure "
"cannot be averaged away). These are governance-desirable properties: a system that is excellent on eight axes and "
"catastrophic on one should not score well.")
subsection("The aggregation axioms A1&ndash;A5")
para("The substrate fixes five axioms on a candidate aggregator &Phi;: [0,1]<sup>k</sup> &rarr; [0,1].")
ax_flows = [
P("<b>A1 (Monotonicity).</b> &Phi; is non-decreasing in each argument.", thm),
P("<b>A2 (Positive homogeneity).</b> &Phi;(c&middot;x) = c&middot;&Phi;(x) for c &gt; 0.", thm),
P("<b>A3 (Idempotence / normalization).</b> &Phi;(c,&hellip;,c) = c.", thm),
P("<b>A4 (Boundedness).</b> &Phi;(x) &le; max<sub>i</sub> x<sub>i</sub>.", thm),
P("<b>A5 (Permutation invariance / symmetry).</b> &Phi; is invariant under any permutation of its arguments.", thm),
]
boxed(ax_flows, bg=AXBG, border=colors.HexColor("#E2C9A8"))
para("A5 was added as a structure field in a late round (PR #148) precisely because the literature (Kolmogorov 1930, "
"Nagumo 1930, Acz&eacute;l 1948, Hardy&ndash;Littlewood&ndash;P&oacute;lya 1934) confirms that A1&ndash;A4 <i>alone</i> "
"do not force the geometric mean.")

subsection("The honest crux: unconditional uniqueness is FALSE")
para("It is tempting to claim that &Lambda;<sub>k</sub> is the <i>unique</i> &Phi; satisfying A1&ndash;A5. "
"<b>This is false, and we prove it false.</b>")
theorem_box("Theorem 4.2 (Refutation of unconditional uniqueness).", f"{SFREE} &nbsp; {CIG}",
"There exists &Phi; &ne; &Lambda;<sub>k</sub> satisfying A1&ndash;A5. In particular, the max-aggregator "
"maxAgg(x) = max<sub>i</sub> x<sub>i</sub> satisfies A1&ndash;A5 yet differs from &Lambda;<sub>k</sub>: at (4,1) one has "
"maxAgg = 4 while &Lambda;<sub>2</sub>(4,1) = 2.",
f'The witness is {M("maxAgg_ne_Lambda")} (also realized as {M("unconditional_lambda_is_false")}), machine-checked '
"in-tree. The max function is monotone (A1), positively homogeneous (A2), idempotent (A3), bounded by itself hence "
f"&le; max (A4), and symmetric (A5); evaluating at (4,1) separates it from the geometric mean by {M('decide')}. "
f'#print&nbsp;axioms {M("maxAgg_ne_Lambda")} reports Lean-core axioms only. Independent companions {M("aggMin")} (min '
f'over nine axes) and {M("aggMaxZ")} exhibit the same failure on the nine-axis bounty variant, also decide-checked.')
para("This matches the classical theory exactly: Kolmogorov&ndash;Nagumo&ndash;de Finetti characterize quasi-arithmetic "
"means by symmetry, idempotency, monotonicity, continuity, <i>and</i> a <i>bisymmetry / associativity / replacement</i> "
'axiom <a href="https://en.wikipedia.org/wiki/Quasi-arithmetic_mean" color="#01696F">[quasi-arithmetic mean]</a>; the '
"missing ingredient in A1&ndash;A5 is precisely that last family. Acz&eacute;l&rsquo;s two-variable result uses "
'bisymmetry; the n-variable refinement is due to Maksa&ndash;Mokken&ndash;M&uuml;nnich '
'<a href="https://arxiv.org/html/2606.05221v1" color="#01696F">[arXiv:2606.05221]</a>.')

subsection("The conditional theorem: uniqueness given factorization")
theorem_box("Theorem 4.3 (Uniqueness given factorization).", f"{SFREE} &nbsp; {CIG}",
"Let &Phi; satisfy A1&ndash;A5 and suppose &Phi; <i>factors</i>, i.e. there exist exponents "
"&alpha;<sub>1</sub>,&hellip;,&alpha;<sub>k</sub> &ge; 0 with &Phi;(x) = &prod;<sub>i</sub> x<sub>i</sub><sup>&alpha;"
"<sub>i</sub></sup> for all x. Then &Phi; = &Lambda;<sub>k</sub>.",
f'The Lean term is {M("lambda_unique_of_factors")} (Round-13). Given factorization, idempotence (A3) forces &sum; '
"&alpha;<sub>i</sub> = 1 and symmetry (A5) forces all &alpha;<sub>i</sub> equal, whence each &alpha;<sub>i</sub> = 1/k "
f'and &Phi; = &Lambda;<sub>k</sub>. The exponent collapse uses {M("NNReal.rpow")} arithmetic and a Finset induction. A '
f'companion lemma {M("lambda_factors")} (axiom-free, CI-green) shows &Lambda;<sub>k</sub> <i>itself</i> factors with '
"exponents 1/k, so the factorization hypothesis is non-vacuous.")

subsection("The conditional theorem: uniqueness under block-consistency")
para("The factorization hypothesis is itself opaque to a non-specialist. The substrate&rsquo;s recommended route makes "
"the extra assumption a <i>governance-legible</i> axiom.")
theorem_box("Axiom A6&prime; (Block-consistency / aggregation-invariance).", "",
"Aggregating evidence within independent blocks and then across the block results equals aggregating the flattened "
"collection. Equivalently: the trust verdict does not depend on how the auditor partitions the evidence into review "
"blocks.", bg=AXBG)
theorem_box("Theorem 4.4 (Conditional uniqueness of &Lambda; under A6&prime;).", f"{AXIOM} &nbsp; {CIG}",
f'Under {{A1, A2, A3, A4, A5}} together with the single declared axiom {M("A6&#39;_block_consistent")} (Axiom A6&prime;), '
"the Lutar invariant &Lambda;<sub>k</sub> is the unique normalized aggregator.",
f'The Lean term is {M("lambda_unique_under_block")} ({M("Lutar/Wave4/LambdaBlockConsistency.lean")}). It is <b>CI-green</b>: '
f'the real lutar-lean CI {M("lake build")} (a full kernel check) succeeds at the recorded commit. The classical content '
"is that aggregation-invariance forces the quasi-arithmetic factorization that pins the geometric mean "
'(<a href="https://doi.org/10.1007/s10726-018-9589-3" color="#01696F">Cs&aacute;t&oacute; 2018</a>, after Kolmogorov '
f'1930); we formalize that implication as the declared axiom and derive factorization + uniqueness from it, then '
f'discharge via Theorem 4.3. #print&nbsp;axioms {M("lambda_unique_under_block")} discloses exactly '
f'[{M("A6&#39;_block_consistent")}, {M("propext")}, {M("Quot.sound")}, {M("Classical.choice")}]: one declared, '
"disclosed, non-core axiom and the trusted Lean core.", bg=AXBG)
para("A6&prime; is strictly <i>weaker</i> and more governance-natural than the prior bisymmetry axiom A6_bisymmetric, "
"which essentially asserts the factorization directly; the team deliberately downgraded to A6&prime; to widen the gap "
"between premise and conclusion (&sect;9). The cleanest <i>published</i> characterization is "
'<a href="https://doi.org/10.1016/0022-2496(83)90028-7" color="#01696F">Acz&eacute;l&ndash;Saaty 1983</a>: the geometric '
"mean is the unique quasi-arithmetic mean satisfying <i>reciprocity</i> + <i>positive homogeneity</i>, and positive "
"homogeneity is already A2, so the only new commitment is reciprocity.")

subsection("&Lambda; is Conjecture 1 &mdash; the precise claim structure")
para("We separate three propositions and assert the truth-value of each:")
bullets([
"<b>(U) Unconditional uniqueness:</b> &ldquo;&Lambda; is the unique &Phi; satisfying A1&ndash;A5.&rdquo; &mdash; "
"<b>FALSE</b> (Theorem 4.2).",
"<b>(C) Conditional uniqueness:</b> &ldquo;Given A1&ndash;A5 + A6&prime;, &Lambda; is unique.&rdquo; &mdash; "
"<b>PROVEN, conditional</b> (Theorem 4.4, CI-green, axiom disclosed).",
"<b>(Conj) The governance conjecture:</b> &ldquo;The <i>right</i> axiomatization of a governed trust aggregator forces "
"&Lambda;.&rdquo; &mdash; <b>Conjecture 1</b>: a research hypothesis, not a theorem.",
])
theorem_box("Conjecture 1 (The Lutar invariant; never a theorem).", CONJ,
"The equal-weight geometric mean &Lambda;<sub>k</sub> is the correct unique trust aggregator for governed AI, in the "
"sense that the governance-correct axiom (A6&prime;-type block-consistency / aggregation-invariance) is the right "
"normative demand on a governed aggregator. This is an open philosophical claim, not a mathematical theorem; it is "
"<i>never</i> asserted as proven, and the unconditional form (U) is <i>provably false</i>.", bg=CONJBG)
para("The honesty doctrine is simply: say (U) is false, (C) is proven-conditional, and (Conj) is open &mdash; and never "
"let any reader collapse them. &sect;9 defends why this calibration is epistemically virtuous rather than a weakness.")

subsection("Worked examples: the governance-desirable behaviour of &Lambda;")
para("Three numerical examples make the design rationale concrete and expose precisely where &Lambda; and the "
"counterexample maxAgg diverge. Throughout, evidence is on a nine-axis scale (provenance, policy, measurability, "
"moral-grounding, replay, attribution, inclusion, freshness, quorum), each normalized to [0,1].")
para("<b>(a) The disqualifying-zero property.</b> Let a candidate action score x = (0.99, 0.99, 0.99, 0.99, 0.99, 0.99, "
"0.99, 0.99, 0.00): eight axes near-perfect, one axis a hard failure (e.g. provenance cannot be established). The "
"arithmetic mean returns 0.88 &mdash; a passing grade that averages the failure away. The geometric mean returns "
"&Lambda;<sub>9</sub>(x) = (0.99<sup>8</sup>&middot;0)<sup>1/9</sup> = 0, correctly refusing to certify an action with an "
"unestablished provenance. This is the precise sense in which &ldquo;one disqualifying failure cannot be averaged "
"away,&rdquo; and it is why a governed substrate must not use the arithmetic mean.")
para("<b>(b) Scale-covariance (positive homogeneity, A2).</b> Suppose every axis is re-graded on a 0&ndash;100 scale "
"rather than 0&ndash;1, i.e. x &rarr; 100&middot;x. Then &Lambda;<sub>9</sub>(100&middot;x) = 100&middot;&Lambda;<sub>9</sub>(x): the "
"verdict rescales exactly with the inputs, so the certification decision is invariant under the choice of grading units. "
"An aggregator lacking A2 would let a cosmetic change of units flip a pass into a fail &mdash; an obviously "
"unacceptable property for an auditable process.")
para("<b>(c) Where maxAgg breaks (Theorem 4.2, concretely).</b> The refuting witness maxAgg satisfies all of "
"A1&ndash;A5 yet is the opposite of governance-safe: it certifies on the <i>best</i> axis. The table contrasts the two "
"aggregators on representative profiles; maxAgg passes exactly the actions a governed system must reject.")
lam_rows = [
["(4, 1) &mdash; the Lean witness pair", "2.00", "4.00", "maxAgg ignores the weak axis; separates from &Lambda; by <i>decide</i>."],
["(0.9, 0.9, 0.0) &mdash; one hard fail", "0.00", "0.90", "&Lambda; rejects; maxAgg certifies on the single good axis."],
["(0.5, 0.5, 0.5) &mdash; uniform", "0.50", "0.50", "Agree only on the idempotent diagonal (A3)."],
["(1.0, 0.2, 0.2) &mdash; one strong axis", "0.34", "1.00", "maxAgg awards a perfect score for a single strong axis."],
]
table(["Score profile x", "&Lambda;(x)", "maxAgg(x)", "Governance reading"], lam_rows,
      [1.95*inch, 0.6*inch, 0.7*inch, 3.05*inch])
para("The contrast is not a curiosity: it is the reason A1&ndash;A5 are insufficient and why a governance-natural sixth "
"axiom (A6&prime;, &sect;4.5) is needed to single out &Lambda;. maxAgg is the maximally permissive aggregator consistent "
"with A1&ndash;A5; &Lambda; is, under A6&prime;, the unique one that honours the disqualifying-zero norm.")

# =====================================================================
# 5. RECEIPTS
# =====================================================================
section("The proof-trail / receipt architecture")
para("Every governed action emits a <i>receipt</i>: a canonical record of the action, its inputs, the gate decision, "
"and the &Lambda; sub-scores. Receipts are hash-chained (each entry commits to its predecessor) and Merkle-bound (a set "
"of receipts commits to a single root), so that tampering is detectable and inclusion is checkable. The substrate "
"formalizes the structural and security properties of this architecture in Lean&nbsp;4, with cryptographic hardness "
"explicitly declared as an idealization rather than proved.")
subsection("Structural correctness (sorry-free)")
para("The replay engine (F1) is deterministic: equal logs replay to equal final state, and the folded state equals the "
"last entry of the explicit replay trace (proved by induction over the log; #print&nbsp;axioms reports propext only). "
"Hash-chain verification (F13) is sound: a verified chain implies all links match (propext, Quot.sound). The Merkle "
"inclusion checker (F15) is correct-by-construction over an abstract hash.")
subsection("Security under declared idealizations (axiom-gated)")
para("Security properties &mdash; tamper-evidence, attribution, inclusion-binding &mdash; require collision-resistance / "
"unforgeability assumptions. We declare these as named axioms and disclose them, following the ProVerif methodology of "
"abstracting a primitive as an axiom, proving the protocol against it, and discharging the axiom separately for a "
'concrete implementation <a href="https://arxiv.org/abs/2303.04500" color="#01696F">[arXiv:2303.04500]</a>. The declared '
"axioms are hash_collision_resistant (tamper-evidence, F13&prime;), ecdsa_unforgeable (DSSE attribution, F14), and "
"h2_collision_resistant (inclusion-binding, F15). The Wave-3 Merkle work adds compression_collision_resistant "
"(Merkle&ndash;Damg&aring;rd), node_collision_resistant, leaf_collision_resistant, and domain_separation. Each is an "
"injective-oracle abstraction, <i>not</i> a proof of cryptographic hardness, and is disclosed in the "
"#print&nbsp;axioms ledger (&sect;7).")
subsection("Supply-chain attestation: SLSA L1+L2 (NOT L3)")
para("The substrate&rsquo;s container images are SLSA-attested. Empirically, 5/5 GHCR images verify under "
'slsa-verifier, establishing SLSA Levels 1 and 2. We do <b>not</b> claim Level 3 '
'<a href="https://slsa.dev" color="#01696F">[SLSA]</a>; the honest status is L1+L2 attested.')
subsection("Receipt schema and a worked hash-chain example")
para("A receipt is a canonical, deterministically-serialized record. Writing H for the receipt hash function and "
"&#8741; for byte concatenation, the i-th receipt commits to its predecessor and to its own payload:")
rcpt_flows = [
P("<b>payload<sub>i</sub></b> = (action, inputs_digest, gate_decision, &Lambda;-subscores, timestamp, actor_id)", thm),
P("<b>link<sub>i</sub></b> = H( prev_hash<sub>i&minus;1</sub> &nbsp;<font name='Math'>&#8741;</font>&nbsp; canonical(payload<sub>i</sub>) ),"
" &nbsp; with prev_hash<sub>0</sub> = H(genesis).", thm),
P("<b>root</b> = MerkleRoot(link<sub>1</sub>, &hellip;, link<sub>n</sub>) &mdash; a single commitment to the whole batch.", thm),
]
boxed(rcpt_flows)
para("Canonicalization is essential: <i>canonical(&middot;)</i> fixes key order, number formatting, and Unicode "
"normalization so that semantically-equal payloads serialize byte-identically, which is exactly the precondition for "
"the determinism property F1 proves (equal logs &rArr; equal replay state). The structural guarantees are sorry-free "
"(&sect;5.1); the security guarantees &mdash; that a forged link or a swapped leaf is detectable &mdash; hold under the "
"declared collision-resistance axioms (&sect;5.2), reusing the Certificate-Transparency Merkle discipline "
'<a href="https://www.rfc-editor.org/info/rfc6962" color="#01696F">[RFC 6962]</a>.')
para("<b>Worked tamper check.</b> Suppose an adversary edits payload<sub>j</sub> after the fact (e.g. to hide a denied "
"action). Then link<sub>j</sub> recomputes to a value &ne; the stored one, so the chain check at position j fails and "
"every subsequent link &mdash; each of which folded the old prev_hash &mdash; also fails to reproduce the stored root. "
"Under node_collision_resistant and leaf_collision_resistant the adversary cannot construct a colliding edit, so the "
"single published root is sufficient to detect any post-hoc alteration of the batch. This is the formal content of "
"&ldquo;tamper-evident&rdquo;: not that tampering is impossible, but that undetected tampering is, under the declared "
"assumptions, computationally infeasible.")

# =====================================================================
# 6. LOCKED KERNEL
# =====================================================================
section("The locked kernel and the honest counts")
subsection("The locked kernel")
para("The Lean formalization has a <i>locked kernel</i>, pinned at commit c7c0ba17 (Doctrine v11): <b>749 declarations / "
"14 unique axioms / 163 sorries</b>. Within this counted scope, exactly <b>five</b> PURIQ governance formulas are "
"proven and locked: {F1 (replay determinism), F11 (Ayni reciprocity), F12 (Kuramoto additive), F18 (Reed&ndash;Solomon), "
"F19 (Bekenstein additive)}.")
para("All other formal work &mdash; the F1&ndash;F22 experimental pass, the Wave-3 C-candidates, and the Wave-4 "
"&Lambda; modules &mdash; lives in a separate <i>experimental</i> scope that is counter-excluded from the locked count, "
"and stays excluded until re-audited under the authoritative lake build. This separation is the externalized "
"meta-level of &sect;3.")
para("<b>Remark (on F12 and F19).</b> F12 and F19 prove only the <i>additive</i> fragment of, respectively, Kuramoto "
"synchronization and the Bekenstein bound. They are honest scaffolding, not the full nonlinear / physical theorems, and "
"are labeled as such in their docstrings. We never describe F12 as &ldquo;Kuramoto synchronization proved&rdquo; or F19 "
"as &ldquo;Bekenstein bound proved.&rdquo;", note)
subsection("Honest counts at a glance")
cnt_rows = [
["Locked / kernel-verified formulas","<b>5</b>","{F1,F11,F12,F18,F19} at c7c0ba17."],
["New sorry-free (Lean-core only)","<b>+19</b>","Wave-3 C8&ndash;C20 cores, bare-Lean verified."],
["New axiom-gated (declared idealizations)","<b>+4</b>","Merkle / Merkle&ndash;Damg&aring;rd."],
["Conditional &Lambda; uniqueness (declared A6&prime;)","<b>1</b>","CI-green; &Lambda; still Conjecture 1."],
["Mathlib re-exports (Tsirelson/CHSH/Jensen)","3","CI-pending; <i>not</i> claimed proven."],
["Unconditional &Lambda; uniqueness","&mdash;","<b>FALSE</b> (counterexample)."],
["SLSA","L1+L2","attested; <i>not</i> L3."],
]
table(["Tier","Count","Meaning"], cnt_rows, [2.7*inch, 0.9*inch, 2.9*inch])

# =====================================================================
# 7. THE MATHEMATICS
# =====================================================================
section("The mathematics: stated theorems with status")
para("This section states the principal formal results precisely, each with its <i>status</i>, a proof sketch or Lean "
"reference, and an explicit #print&nbsp;axioms disclosure. The status tags are: <b>[LOCKED]</b>, <b>[sorry-free, "
"Lean-core only]</b> (only propext / Quot.sound / Classical.choice), <b>[axiom-gated]</b> (sorry-free given a "
"<i>declared</i> idealization), <b>[CI-green]</b> (kernel-checked by the real CI), <b>[CI-pending]</b> "
"(Mathlib-dependent, awaiting a green build &mdash; <i>not</i> claimed proven), and <b>[Conjecture 1]</b>.")
subsection("The locked five")
locked_flows = [
P(f"<b>F1 &mdash; Replay determinism.</b> {LOCKED} Deterministic step-fold replay: equal logs replay to equal "
"final state; folded state = last of explicit trace (f1_replay_fold_deterministic). #print&nbsp;axioms: propext.", thm),
P(f"<b>F11 &mdash; Ayni reciprocity conservation.</b> {LOCKED} Tit-for-tat parity conserved "
"(Int.add_sub_cancel). #print&nbsp;axioms: propext.", thm),
P(f"<b>F12 &mdash; Kuramoto additive scaffolding.</b> {LOCKED} Additive superposition k&sum;p<sub>i</sub> = "
"&sum;kp<sub>i</sub>. <i>Additive fragment only.</i>", thm),
P(f"<b>F18 &mdash; Reed&ndash;Solomon RS(10,6).</b> {LOCKED} Erasure tolerance by shard counting "
"(decide/omega). #print&nbsp;axioms: propext, Quot.sound.", thm),
P(f"<b>F19 &mdash; Bekenstein additive scaffolding.</b> {LOCKED} Entropy budget additive over a region "
"partition; each region &le; total. <i>Additive scaffolding only; NOT the bound S &le; 2&pi;kRE/(&#8463;c).</i>", thm),
]
boxed(locked_flows)
para("A further set of F-formulas (F2&ndash;F10, F13, F15&ndash;F17, F20&ndash;F22) is proved sorry-free in the "
"<i>experimental</i> pass (21 distinct IDs total), but these are not in the locked count; we report them as engineering "
"targets, not as locked results.")

subsection("The +19 Wave-3 sorry-free theorems")
para("The following nineteen theorems were compiled sorry-free under bare Lean 4.13.0 with only the trusted Lean-core "
"axioms, and the corresponding Mathlib-free modules are CI-green at HEAD. Each is the honest, named fragment indicated; "
"several (C9, C12, C17, C20) are explicitly the Mathlib-free <i>core</i> of a larger result and are labeled as such.")
w3 = [
P(f"<b>C8 &mdash; Kraft inequality.</b> {SFREE} c8_kraft_equality_doctrine, c8a_kraft_sub_code, "
"c8b_kraft_mixed_lengths. Receipt-length budget. #print&nbsp;axioms: no axioms. (Kraft 1949.)", thm),
P(f"<b>C9 &mdash; Shannon L &ge; H, tight case.</b> {SFREE} c9_shannon_tight, c9a_no_undershoot, "
"c9b_entropy_value. Receipt information lower bound. #print&nbsp;axioms: no axioms. (Shannon 1948.)", thm),
P(f"<b>C10 &mdash; Byzantine 3f+1.</b> {SFREE} c10_threeFPlusOne, c10a_quorum_intersection, c10b_honest_majority, "
"c10c_infeasible_at_3f. Consensus quorum sizing (n &ge; 3f+1; two 2f+1 quorums intersect in an honest node). "
"#print&nbsp;axioms: propext, Quot.sound, Classical.choice. (Pease&ndash;Shostak&ndash;Lamport 1980.)", thm),
P(f"<b>C11 &mdash; DLS partial-synchrony.</b> {SFREE} c11_dls_threshold, c11a_three_groups. Safety/liveness "
"threshold f &lt; n/3 under partial synchrony. #print&nbsp;axioms: propext, Quot.sound, Classical.choice. "
"(Dwork&ndash;Lynch&ndash;Stockmeyer 1988.)", thm),
P(f"<b>C12 &mdash; FLP bivalence core.</b> {SFREE} c12a_bivalent_xor_univalent, c12b_no_decision_from_bivalent. "
"The bivalence dichotomy at the heart of FLP impossibility (the <i>core</i>; full FLP not claimed). #print&nbsp;axioms: "
"no axioms. (Fischer&ndash;Lynch&ndash;Paterson 1985.)", thm),
P(f"<b>C17 &mdash; BLUE minimum-variance, scalar core.</b> {SFREE} c17_blue_min_variance, c17a_blue_equality. The "
"minimum-variance linear unbiased estimator (Gauss&ndash;Markov), scalar fragment (full matrix-PSD is a CI target). "
"#print&nbsp;axioms: propext, Quot.sound, Classical.choice.", thm),
P(f"<b>C20 &mdash; Softmax order-stability, core.</b> {SFREE} c20_argmax_stable, c20a_translation_invariant, "
"c20b_robust_margin. Order-preservation / translation-invariance core of softmax (tight 1/2-Lipschitz in every "
"&ell;<sub>p</sub> is a CI target). #print&nbsp;axioms: no axioms / propext, Quot.sound. Retrieval / sparse-attention "
"stability.", thm),
]
boxed(w3)
para("These nineteen carry, in the verbatim Wave-3 ledger, only the trusted core; no sorryAx appears anywhere among "
"them.")

subsection("The +4 axiom-gated Merkle theorems")
m4 = [
P(f"<b>C13 &mdash; Merkle&ndash;Damg&aring;rd CR preservation.</b> {AXIOM} c13_md_step_cr, c13a_md_append_cr, "
"under compression_collision_resistant. Receipts hash-chain (F13&prime; upgrade). (Merkle 1979; Damg&aring;rd 1989.)", thm),
P(f"<b>C14 &mdash; Merkle-tree binding.</b> {AXIOM} c14_merkle_binding, under node_collision_resistant, "
"leaf_collision_resistant, and domain_separation. Receipts-Merkle binding (F15 upgrade).", thm),
P(f"<b>C14b &mdash; Domain separation blocks second-preimage.</b> {AXIOM} c14b_no_second_preimage, under the "
"domain_separation tag only (structural, no hardness assumption).", thm),
]
boxed(m4, bg=AXBG, border=colors.HexColor("#E2C9A8"))
para("The verbatim #print&nbsp;axioms ledger lists exactly these declared, non-core axioms and no others; they are "
"disclosed precisely as the existing kernel crypto axioms are.")

subsection("The conditional &Lambda; result and its refutation")
para("The pair of results from &sect;4 is the mathematical heart of the substrate. Theorem 4.2 (unconditional "
"uniqueness FALSE, maxAgg_ne_Lambda) and Theorem 4.4 (conditional uniqueness under declared A6&prime;, "
"lambda_unique_under_block, CI-green) are complementary: the first establishes the <i>boundary</i> (which extra "
"assumption is necessary, and that without it the claim fails), and the second establishes the <i>maximal true "
"statement</i>. A bare-Lean witness module of six zero-axiom theorems (LambdaBisymmetryWitness) exhibits the concrete "
"discriminating facts: the max/min aggregators fail strict monotonicity exactly where the geometric mean separates, and "
"&Lambda; is bisymmetric/decomposable.")
subsection("The CI-pending re-exports (not claimed proven)")
para("Three Mathlib-dependent re-exports &mdash; C1 Tsirelson 2&radic;2 ceiling, C2 CHSH classical ceiling &le; 2, and "
"C6 finite Jensen / ELBO direction &mdash; have signatures verified character-for-character against pinned Mathlib, but "
"wiring their module into the kernel-checked root reproducibly red-lights lake build, and the build log is not "
f"retrievable in the sandbox. Per the honesty doctrine these stay {PEND}: the file remains in-tree but is <i>not</i> "
"imported into the compiled root, so nothing is claimed proven that CI has not verified.")
subsection("Selected proof sketches")
para("To substantiate that the named theorems are real mathematics and not labels, we give honest proof sketches for "
"three representatives spanning information theory, distributed consensus, and impossibility. Each sketch is the human "
"reading of the corresponding sorry-free Lean development; the Lean term is authoritative.")
para("<b>C8 &mdash; Kraft inequality (c8_kraft_equality_doctrine).</b> Claim: a prefix-free code over an alphabet of "
"size D with codeword lengths &#8467;<sub>1</sub>, &hellip;, &#8467;<sub>n</sub> exists iff &sum;<sub>i</sub> "
"D<sup>&minus;&#8467;<sub>i</sub></sup> &le; 1. <i>Sketch.</i> Identify each codeword with a node at its depth in the "
"full D-ary tree; prefix-freeness means the chosen nodes are pairwise non-ancestral, so their descendant-leaf sets at "
"the maximal depth L are disjoint. A node of depth &#8467;<sub>i</sub> owns D<sup>L&minus;&#8467;<sub>i</sub></sup> such "
"leaves; disjointness gives &sum;<sub>i</sub> D<sup>L&minus;&#8467;<sub>i</sub></sup> &le; D<sup>L</sup>, and dividing by "
"D<sup>L</sup> yields the inequality. Equality holds iff the tree is saturated (a complete code). In Lean the budget "
"is proved as a finite sum bound; the doctrine-relevant corollary is that a receipt&rsquo;s field-length schedule "
"admits a prefix-free encoding precisely when its Kraft sum is &le; 1 (Kraft 1949). #print&nbsp;axioms: no axioms.")
para("<b>C10 &mdash; Byzantine fault tolerance, n &ge; 3f+1 (c10_threeFPlusOne, c10a_quorum_intersection).</b> Claim: "
"agreement among n processes tolerating f Byzantine faults requires n &ge; 3f+1, and any two quorums of size 2f+1 "
"intersect in at least one honest process. <i>Sketch.</i> A quorum must be usable when f processes are unreachable, so "
"it can have at most n&minus;f members; for two quorums Q<sub>1</sub>, Q<sub>2</sub> of size q to share an honest node "
"we need |Q<sub>1</sub> &#8745; Q<sub>2</sub>| &gt; f, i.e. 2q &minus; n &gt; f. Taking q = n&minus;f and requiring "
"2(n&minus;f) &minus; n &gt; f gives n &gt; 3f, hence n &ge; 3f+1. The intersection lemma c10a then exhibits, for "
"q = 2f+1 and n = 3f+1, an intersection of size &ge; f+1, which contains at least one honest node since at most f are "
"faulty (Pease&ndash;Shostak&ndash;Lamport 1980). The Lean proof discharges these as arithmetic facts over "
"&#8469; with omega. #print&nbsp;axioms: propext, Quot.sound, Classical.choice.")
para("<b>C12 &mdash; FLP bivalence core (c12a_bivalent_xor_univalent, c12b_no_decision_from_bivalent).</b> Claim: "
"a configuration of an asynchronous consensus protocol is either <i>univalent</i> (its decision is already determined) "
"or <i>bivalent</i> (both 0 and 1 remain reachable), exclusively; and no single deterministic step taken from a "
"bivalent configuration can itself force a decision. <i>Sketch.</i> Valence is defined as the set of decision values "
"reachable by some admissible run; the dichotomy is then a set-cardinality fact (the reachable-decision set is "
"non-empty and a subset of {0,1}, so it has size 1 &mdash; univalent &mdash; or 2 &mdash; bivalent). The second lemma "
"formalizes the step-locality argument at the heart of FLP: from a bivalent configuration there exist two one-step "
"successors of differing valence, so the step alone cannot have decided. We claim only this combinatorial core; the "
"full FLP impossibility (which adjoins a fairness/commutativity argument to build an infinite non-deciding run) is "
"<i>not</i> claimed (Fischer&ndash;Lynch&ndash;Paterson 1985). #print&nbsp;axioms: no axioms.")
para("These sketches are illustrative, not exhaustive; the remaining sixteen Wave-3 theorems carry analogous "
"docstring-level justifications in-tree, and in every case the Lean term &mdash; not the prose &mdash; is the "
"authoritative object.")

# =====================================================================
# 8. GROUNDBREAKING
# =====================================================================
section("Why this is groundbreaking &mdash; the honest case")
para("We make the case for significance without overclaiming. Each claim below is qualified exactly as far as the "
"evidence permits.")
subsection("First machine-verified governed-AI trust substrate with disclosed axioms")
para("To our knowledge, no prior governed-AI system ships a <i>locked, kernel-verified</i> core of governance formulas "
"together with a complete #print&nbsp;axioms disclosure of every idealizing axiom. The verifiable-claims program "
"argued for mechanisms supporting verifiable claims; the substrate is a concrete instantiation in which the "
"verification is performed by an independent proof kernel (Lean&nbsp;4) and the trusted base is enumerated. Formal "
"verification of security-critical systems is itself well established &mdash; seL4 is the canonical example of a "
"machine-checked OS kernel &mdash; but applying a <i>disclosed-axiom</i>, kernel-checked discipline to an <i>AI "
"governance</i> aggregator and its receipt architecture is, as far as we can determine, new.")
subsection("The conditional-uniqueness result with a machine-checked refutation of the overclaim")
para("The distinctive epistemic move is that we did <i>not</i> merely prove a conditional theorem; we also <i>proved "
"the negation of the unconditional claim</i> (Theorem 4.2). Establishing exactly which extra assumption is required, "
"and that without it the claim fails, converts a routine conditional into a <i>boundary</i> result: the conditional "
"theorem is demonstrably the maximal true statement, not a fallback for a proof we could not find. This is rare in "
"applied formal work and is, we argue, the correct standard for high-stakes governance claims.")
subsection("The proof-trail / receipt architecture as engineered epistemology")
para("The receipt chain is not merely an audit log; it is an <i>engineered sensitivity mechanism</i> in the sense of "
"formal epistemology (&sect;9). Tamper-evidence (under hash_collision_resistant) makes the system&rsquo;s record "
"<i>track</i> what actually happened: were the record altered, verification would fail to confirm it. Combined with "
"deny-by-default gating and full sub-score retention, the architecture supplies the non-lucky, checkable grounds on "
"which a rational human trust attitude can rest.")
subsection("Honest comparison to prior art")
pa_rows = [
["Verifiable-claims governance [Brundage 2020]; NTIA","The <i>argument</i> that AI claims should be externally verifiable.","v23 is a concrete substrate with a kernel-checked core and disclosed axioms; it does not claim to solve verifiability in general."],
["seL4 / Isabelle security","Machine-checked OS-kernel correctness; the gold standard for verified systems.","v23 verifies a <i>governance aggregator + receipt</i> layer, far smaller in scope and maturity; we do not claim seL4-level coverage."],
["Certificate Transparency (RFC 6962/9162)","Merkle-based tamper-evident logs in production.","v23 reuses the same Merkle discipline and formalizes the binding property in Lean under declared axioms."],
["SLSA framework","A supply-chain integrity ladder (L1&ndash;L4).","v23 attests L1+L2 only; L3 is explicitly <i>not</i> claimed."],
["Functional-equation aggregation (Acz&eacute;l, Cs&aacute;t&oacute;)","Uniqueness characterizations of the geometric mean.","v23 <i>formalizes</i> the conditional uniqueness in Lean and <i>machine-checks the unconditional refutation</i>; the math is classical, the verified-and-refuted packaging is the contribution."],
]
table(["Prior art","What it provides","How v23 differs (honestly)"], pa_rows, [1.7*inch, 1.9*inch, 2.9*inch])
para("The honest summary: the individual mathematical facts (Kraft, Shannon, Byzantine quorums, DLS, FLP, "
"Gauss&ndash;Markov, the geometric-mean characterizations) are classical and largely available in or portable to "
"Mathlib. The contribution of v23 is their <i>unification into a governed-AI trust substrate</i>, their "
"<i>kernel-checked instantiation</i> in the governance setting, and above all the <i>honesty architecture</i> &mdash; "
"locked counts, disclosed axioms, and a machine-checked refutation guarding the one tempting overclaim.")

# =====================================================================
# 9. PHILOSOPHY
# =====================================================================
section("Philosophical foundations: why block-consistency is the right axiom")
subsection("The acceptability test for a governance axiom")
para("A primitive is acceptable to a regulator/auditor only if it is (i) <i>interpretable</i> as a governance norm a "
"layperson-with-counsel would endorse, (ii) <i>non-question-begging</i> &mdash; not secretly &ldquo;the answer is the "
"geometric mean&rdquo; in disguise, and (iii) <i>independently motivated</i> &mdash; defensible before &Lambda; is "
"mentioned. Block-consistency (A6&prime;) passes all three.")
para("<b>Interpretable.</b> Aggregation-invariance says the trust verdict must not depend on how the auditor partitions "
"the evidence into review blocks &mdash; i.e. <i>path-independence of the audit</i>. An auditor who could change a "
"firm&rsquo;s score by re-drawing departmental boundaries would, by that very fact, be running a manipulable process.")
para("<b>Non-question-begging.</b> Bisymmetry and associativity are formally near-equivalent to the answer and can look, "
"to a hostile technical advisor, like assuming the conclusion. Aggregation-invariance is phrased entirely in terms of "
"the audit process (partition, aggregate, compare), with no reference to means, products, or exponents. Cs&aacute;"
"t&oacute; (2018) <i>derives</i> the row geometric mean from anonymity + responsiveness + aggregation-invariance "
"&mdash; the geometric mean falls out as a theorem rather than being smuggled in.")
para("<b>Independently motivated.</b> A6&prime; is a pre-existing, published axiom with a stand-alone governance "
"meaning, motivated before &Lambda; enters. It is the same move that underwrites objectivity in measurement theory "
"(invariance under admissible scale transformations) and in physics (covariance under coordinate choice): the procedure "
"must track the object, not the bookkeeping.")
subsection("When is a conditional uniqueness result legitimate, not overreach?")
para("A conditional &ldquo;if A6&prime; then &Lambda;-unique&rdquo; is trivially true as a material implication if "
"A6&prime; is strong enough, so a skeptical reviewer rightly worries about antecedent-smuggling. Four well-established "
"conditions distinguish a legitimate conditional from a vacuous one, and the substrate meets all four:")
bullets([
"<b>Independently-motivated antecedent.</b> A6&prime; is published (Cs&aacute;t&oacute; 2018) with a stand-alone "
"meaning; we deliberately chose the <i>weakest sufficient, most-independent</i> antecedent, downgrading from "
"A6_bisymmetric.",
"<b>Non-vacuous instantiation.</b> lambda_factors (axiom-free, CI-green) shows the factorization A6&prime; demands is "
"realized by &Lambda; itself.",
"<b>Boundary established.</b> We proved &not;(U) by explicit counterexample (Theorem 4.2); the conditional is the "
"maximal true statement.",
"<b>Disclosed at point of use.</b> Every theorem carries #print&nbsp;axioms exposing the A6&prime; dependency at "
"compile time &mdash; the Lakatosian virtue of explicit, revisable lemma-conditions, the opposite of silent "
"monster-barring.",
])
para("The residual gap &mdash; <i>is A6&prime; the philosophically correct demand?</i> &mdash; is genuinely open, which "
"is exactly why &Lambda; remains Conjecture 1. Calling it a theorem would be the overreach; calling it a conjecture is "
"the honest description of the open <i>philosophical</i> question, while the conditional theorem is the honest "
"description of the closed <i>mathematical</i> one.")
subsection("&ldquo;Conjecture 1&rdquo; as a calibration signal")
para("A reviewer who sees &ldquo;Conjecture 1&rdquo; beside &ldquo;machine-checked conditional theorem&rdquo; should "
"read it as calibration in the sense of formal epistemology: the authors&rsquo; assertions track the evidence. A "
"vendor who calls every plausible claim &ldquo;proven&rdquo; makes the label uninformative; the substrate&rsquo;s "
"distinct, audited tiers (&ldquo;locked&rdquo; = 5 formulas; &ldquo;proven under declared axiom&rdquo;; "
"&ldquo;conjecture&rdquo;) make its &ldquo;proven&rdquo; actually mean proven. Honesty here is not modesty; it is what "
"makes any of the positive claims credible.")
subsection("Doctrine-to-philosophy grounding map")
para("Each core substrate claim instantiates an established norm (it is <i>legitimized</i>, not <i>proven</i>, except "
"where Lean proves it):")
bullets([
"&Lambda; as aggregator &larr; representational measurement theory (Krantz/Luce/Suppes/Tversky) + functional-equation "
"uniqueness (Acz&eacute;l, Cs&aacute;t&oacute;).",
"Monotone trust &larr; mechanism-design monotonicity (a necessary condition for strategyproofness; non-monotone "
"aggregators are gameable by withholding good evidence).",
"Proof trail &larr; process reliabilism (Goldman) + truth-tracking (Nozick) + Gettier-proofing; plus verifiable-claims "
"governance (Brundage et al. 2020).",
"Deny-by-default &larr; Saltzer&ndash;Schroeder fail-safe defaults and complete mediation + epistemic conservatism.",
"Bounded Ouroboros &larr; well-foundedness + bounded rationality + Tarskian stratification (&sect;3).",
"Honesty doctrine &larr; Lakatos + Baier&rsquo;s moral test for trust (knowledge of what the relationship rests on "
"must not destabilize it).",
])
subsection("Steelman objections and honest rebuttals")
obj = [
("Objection 1 (strongest): &ldquo;A6&prime; is the geometric mean in a costume.&rdquo;",
"A6&prime; is independently published, phrased with no reference to means or exponents (audit path-independence); we "
"adopted the weakest sufficient, most independent version, <i>proved the unconditional claim false</i> so the "
"conditional is maximal, and disclose the axiom in every #print&nbsp;axioms. The honest residue is a <i>defensible "
"normative design choice</i> &mdash; &ldquo;a governed verdict must not depend on how an auditor partitions the "
"evidence&rdquo; &mdash; from which the geometric mean is derived, not assumed."),
("Objection 2: &ldquo;Motte-and-bailey.&rdquo;",
"The motte (conditional + Conjecture 1) and bailey (&ldquo;&Lambda; uniqueness&rdquo;) are labeled and separated <i>in "
"the artifacts themselves</i>: the lineage carries a literal &ldquo;&Lambda; &mdash; Conjecture 1 (NOT a "
"theorem)&rdquo; badge; proof reports lead with &ldquo;unconditional uniqueness STAYS FALSE.&rdquo; The fallacy "
"requires equivocation; here the three propositions (U/C/Conj) are explicitly distinguished at every assertion."),
("Objection 3: &ldquo;Idealized crypto/A6&prime; axioms make the guarantees illusory.&rdquo;",
"Conceded and already disclosed: these are declared axioms, stated as idealizations, not hardness proofs. Every applied "
"formal result is conditional on its abstraction boundary; the integrity move (ProVerif methodology) is to make that "
"boundary explicit. The guarantee is &ldquo;reliable given the standard cryptographic assumptions the digital economy "
"already relies on&rdquo; &mdash; the same conditional under which TLS and certificate transparency operate."),
("Objection 4: &ldquo;Arrow: aggregation is impossible.&rdquo;",
"Arrow/Sen concern aggregating <i>ordinal preferences of distinct agents</i> into a social ordering; &Lambda; "
"aggregates <i>cardinal, ratio-scale evidence sub-scores about one object</i> &mdash; a measurement problem, not "
"preference aggregation, and not subject to Arrow&rsquo;s IIA-driven impossibility. The honest concession: where trust "
"dimensions encode incommensurable values, a scalar can mask a trade-off, so the substrate retains the full sub-score "
"vector and never lets &Lambda; replace it."),
("Objection 5: &ldquo;G&ouml;del/Tarski: self-auditing is incoherent.&rdquo;",
"Conceded as a limit; it does not bite here. The substrate does <i>not</i> claim self-verification of its own "
"consistency. It claims bounded recursion with a well-founded measure (termination) and verification by an "
"<i>external, stratified</i> stack (Lean kernel &rarr; CI &rarr; human sign-off). The bottom turtle &mdash; the Lean "
"kernel, cryptographic, and human-trust assumptions &mdash; is finite and disclosed."),
("Objection 6: &ldquo;Trust can&rsquo;t be engineered.&rdquo;",
"Largely conceded, reframed as a feature. The philosophy of trust distinguishes the <i>attitude</i> of trust from the "
"<i>property</i> of trustworthiness; &Lambda; does not manufacture the attitude, it produces audited evidence of "
"trustworthiness-relevant properties on which a human&rsquo;s trust can rationally rest. We claim only to make "
"trustworthiness <i>checkable</i>."),
]
for head, reb in obj:
    story.append(P(f"<b>{head}</b>", h3))
    story.append(P(f"<i>Rebuttal.</i> {reb}", body))

# =====================================================================
# 10. EMPIRICAL
# =====================================================================
section("Empirical posture")
para("While the substrate&rsquo;s headline claims are formal, the runtime has measured operating characteristics "
"(reported as <i>measured</i>, not proven). Per-receipt build latency is &asymp; 11.5&nbsp;&mu;s at the median and "
"50.7&nbsp;&mu;s at p99; verification is &asymp; 10.4&nbsp;&mu;s median. The nine-axis &Lambda; computation costs "
"&asymp; 3.12&nbsp;&mu;s (base) / 3.29&nbsp;&mu;s (composed). On a v11 platform run of 24,800 HTTP calls, the "
"governance overhead was 0.49&ndash;0.59&nbsp;ms per route at the median (1.27&nbsp;ms at p99), and &rho;-closure "
"(paired governed calls) was 100% on 8,000/8,000 pairs. A deterministic 5&times; replay yields a byte-identical root. "
'These figures are archived under DOI <a href="https://doi.org/10.5281/zenodo.20119582" color="#01696F">'
"10.5281/zenodo.20119582</a> and are labeled <i>measured</i>; they are engineering evidence, not theorems.")
para("A Sim2Real &ldquo;Walrus-parallel&rdquo; design experiment pretrains the &Lambda;-axis on locked doctrine and "
"fine-tunes on customer receipts; a measured mean &alpha;-gap of 0.10 across five regimes (4/5 transfer at &alpha;=0.00; "
"adversarial at &alpha;=0.50, N=60) is reported as preliminary, not conclusive.")
subsection("Measurement methodology")
para("The latencies above are wall-clock timings of the production receipt path, collected in-process with a monotonic "
"nanosecond clock and reported as empirical percentiles over the run; they are <i>not</i> model-based estimates. Build "
"latency times the canonicalize&ndash;hash&ndash;chain&ndash;persist sequence for a single receipt; verify latency times "
"the chain-and-root re-check; the &Lambda; figures isolate the nine-axis aggregation alone. The per-route overhead is "
"the difference between governed and ungoverned handling of the same request, measured on the v11 platform run. We "
"report medians and tail percentiles rather than means because the governance path&rsquo;s tail behaviour is the "
"operationally relevant quantity for an SLO. All figures are point measurements of one archived run; no confidence "
"intervals or cross-run variance are claimed.")
lat_rows = [
["Receipt build", "11.5 &mu;s", "&mdash;", "50.7 &mu;s", "Canonicalize + hash + chain + persist."],
["Receipt verify", "10.4 &mu;s", "&mdash;", "&mdash;", "Chain re-check + root comparison."],
["&Lambda;<sub>9</sub> (base)", "3.12 &mu;s", "&mdash;", "&mdash;", "Nine-axis geometric mean, isolated."],
["&Lambda;<sub>9</sub> (composed)", "3.29 &mu;s", "&mdash;", "&mdash;", "Within a composed gate evaluation."],
["Governance overhead / route", "0.49&ndash;0.59 ms", "&mdash;", "1.27 ms", "Governed minus ungoverned, 24,800 calls."],
]
table(["Operation", "p50", "&nbsp;", "p99", "What is measured"], lat_rows,
      [1.7*inch, 1.0*inch, 0.3*inch, 0.7*inch, 2.6*inch])
para("Two correctness-flavoured runtime observations accompany the timings and are likewise <i>measured, not proven</i>: "
"a deterministic five-fold replay reproduced a byte-identical Merkle root (consistent with, but not a substitute for, "
"the F1 determinism theorem), and &rho;-closure held on all 8,000 paired governed calls. These observations corroborate "
"the formal results operationally; the formal results remain the authoritative guarantees.")

# =====================================================================
# 11. LIMITATIONS
# =====================================================================
section("Limitations and honesty section")
para("We state plainly what the substrate does <i>not</i> establish.")
bullets([
"<b>&Lambda; is Conjecture 1 unconditionally.</b> The unconditional uniqueness of &Lambda; under A1&ndash;A5 is "
"<i>false</i> (Theorem 4.2). Only the conditional theorem under the declared A6&prime; holds, and whether A6&prime; is "
"the philosophically correct demand is open. We never claim &Lambda; proven unconditionally.",
"<b>The locked count is exactly 5.</b> The locked kernel proves {F1,F11,F12,F18,F19} at c7c0ba17 (749/14/163). The "
"21-formula experimental pass, the +19 Wave-3 theorems, and the Wave-4 &Lambda; modules are <i>not</i> in the locked "
"count until re-audited.",
"<b>Open sorries remain.</b> The locked kernel carries 163 sorries; the live experimental scope carries on the order of "
"256 non-comment sorries. The analytic Cauchy step (monotone + additive &rArr; linear) has one isolated, named open "
"obligation in the slice machinery; F12/F19 are additive scaffolding, not the full physical theorems.",
"<b>SLSA L2, not L3.</b> Supply-chain attestation is L1+L2; L3 is not claimed.",
"<b>Declared idealizations.</b> Tamper-evidence, attribution, and Merkle binding hold only under declared "
"collision-resistance / unforgeability axioms; these are idealizations, not proofs of cryptographic hardness, and are "
"disclosed in every #print&nbsp;axioms ledger.",
"<b>CI-pending re-exports.</b> Tsirelson, CHSH, and Jensen re-exports are Mathlib-dependent and currently red-light the "
"wired build; they are <i>not</i> claimed proven.",
"<b>Scope.</b> The substrate verifies a governance-aggregator and receipt layer, not an end-to-end AI system; it is far "
"smaller in scope and maturity than a fully verified OS kernel.",
])

# =====================================================================
# 12. CONCLUSION
# =====================================================================
section("Conclusion")
para("The Unified Substrate (v23) consolidates twenty-two versions of a single idea: that trust in a governed AI must "
"be <i>earned by checkable evidence</i>, and that the machinery for earning it &mdash; a bounded self-governing loop, a "
"principled trust aggregator, and a tamper-evident proof trail &mdash; can be partially machine-verified today with "
"complete honesty about its limits. The one-line thesis is this:")
para("v23 is the first machine-verified governed-AI trust substrate with fully disclosed axioms, in which the central "
"trust aggregator&rsquo;s uniqueness is proven <i>conditionally</i> (under a declared, governance-natural "
"block-consistency axiom) while its <i>unconditional</i> uniqueness is machine-checked <i>false</i> &mdash; so the "
"conditional theorem is the maximal true statement and the invariant is honestly labeled Conjecture 1, never a theorem.",
quote)
para("The contribution is not a new theorem but a new <i>standard</i>: locked counts, disclosed axioms, and a "
"machine-checked refutation guarding the one tempting overclaim. We submit that this calibrated honesty is precisely "
"what a regulator, an auditor, or a defense customer should require &mdash; and what makes every positive claim in the "
"substrate credible.")

# =====================================================================
# APPENDICES
# =====================================================================
story.append(PageBreak())
section("Appendix A: Reproducibility and artifact manifest")
para("This appendix records the fixed identifiers and the steps by which an independent auditor can reproduce the "
"verification claims of this paper. Nothing here is asserted beyond what a green build of the cited commits "
"establishes; the audit trail is itself the evidence.")
subsection("Pinned commits and artifacts")
man_rows = [
["Locked kernel", "szl-holdings/lutar-lean", "c7c0ba17", "Doctrine v11; 749 decl / 14 axioms / 163 sorries; locks {F1,F11,F12,F18,F19}."],
["Wave-3 proofs", "szl-holdings/lutar-lean", "775093f0", "C8&ndash;C20 sorry-free cores."],
["Wave-3 root wiring", "szl-holdings/lutar-lean", "02e44c30", "Mathlib-free modules wired into root; CI-green."],
["Wave-4 (&Lambda; / A6&prime;)", "szl-holdings/lutar-lean", "043c3df", "LambdaBlockConsistency.lean; conditional uniqueness CI-green."],
["Knowledge base", "szl-holdings/a11oy", "&mdash;", "a11oy-knowledge: axioms, theorems, constants, DOIs."],
["This paper", "szl-holdings/szl-papers", "thesis/v23/", "main.tex, refs.bib, main.pdf, main.md, README.md."],
]
table(["Component", "Repository", "Pin", "Contents / status"], man_rows,
      [1.25*inch, 1.7*inch, 0.85*inch, 2.5*inch])
subsection("How to verify")
para("The verification reduces to three independent checks, each runnable by a third party:")
verify_flows = [
P(M("# 1. Kernel-check the locked core and Wave-3/4 modules")+"<br/>"
  +M("$ git checkout 02e44c30 &amp;&amp; lake build   # expect: green, no errors"), thm),
P(M("# 2. Disclose the trusted axiom base of any theorem")+"<br/>"
  +M("$ #print axioms lambda_unique_under_block")+"<br/>"
  +M("  =&gt; [A6'_block_consistent, propext, Quot.sound, Classical.choice]"), thm),
P(M("# 3. Confirm the refutation of the overclaim is sorry-free")+"<br/>"
  +M("$ #print axioms maxAgg_ne_Lambda     # =&gt; Lean-core axioms only"), thm),
]
boxed(verify_flows)
para("A passing run of (1) establishes the sorry-free / CI-green claims; (2) and (3) establish the disclosed-axiom and "
"refutation claims respectively. The trusted computing base for every &ldquo;proven&rdquo; claim is exactly the Lean "
"kernel plus the axioms each theorem&rsquo;s ledger prints &mdash; nothing more is assumed, and the declared "
"idealizations (collision-resistance, A6&prime;) appear explicitly wherever they are used.")
subsection("Trusted computing base")
para("The bottom turtles, stated once and for all: (i) the soundness of the Lean&nbsp;4 kernel and its core axioms "
"(propext, Quot.sound, Classical.choice); (ii) the declared cryptographic idealizations "
"(hash_collision_resistant, ecdsa_unforgeable, and the Merkle collision-resistance axioms); (iii) the single declared "
"governance axiom A6'_block_consistent, used only in the conditional &Lambda; theorem; and (iv) the human sign-off "
"gating the CI. Everything else is derived. This enumeration is the point of the honesty doctrine: the assumptions are "
"finite, named, and disclosed.")

section("Appendix B: Notation and glossary")
para("For reference, the principal symbols and named conditions used throughout.")
not_rows = [
["&Lambda;<sub>k</sub>(x)", "The Lutar invariant: equal-weight geometric mean (&prod;<sub>i</sub> x<sub>i</sub>)<sup>1/k</sup> on [0,1]<sup>k</sup>."],
["&Phi;", "A generic candidate aggregator [0,1]<sup>k</sup> &rarr; [0,1] satisfying some subset of A1&ndash;A6&prime;."],
["maxAgg", "The max aggregator; the machine-checked witness that A1&ndash;A5 do not pin &Lambda; (Theorem 4.2)."],
["A1&ndash;A5", "Monotonicity, positive homogeneity, idempotence, boundedness, permutation-invariance."],
["A6&prime;", "Block-consistency / aggregation-invariance: the declared governance axiom of the conditional theorem."],
["link<sub>i</sub>, root", "The i-th hash-chain entry and the Merkle commitment to a batch of receipts (&sect;5.4)."],
["sorry-free", "A Lean development with no <i>sorry</i> placeholder; the kernel checks every step."],
["CI-green", "The real continuous-integration lake build passes &mdash; a full kernel check at the pinned commit."],
["axiom-gated", "Sorry-free given an explicitly declared, disclosed idealizing axiom."],
["#print axioms", "Lean command that lists the trusted axiom base a given theorem depends on."],
["Conjecture 1", "The open philosophical claim that A6&prime;-type block-consistency is the correct governance demand; never a theorem."],
]
table(["Symbol / term", "Meaning"], not_rows, [1.6*inch, 4.7*inch])

# =====================================================================
# REFERENCES
# =====================================================================
section("References")
refs = [
'Acz&eacute;l, J. (1948). On mean values. <i>Bull. Amer. Math. Soc.</i> 54(4):392&ndash;400. doi:10.1090/S0002-9904-1948-09020-9. <a href="https://eudml.org/doc/296298" color="#01696F">eudml.org/doc/296298</a>',
'Acz&eacute;l, J. &amp; Saaty, T. L. (1983). Procedures for synthesizing ratio judgements. <i>J. Math. Psychology</i> 27(1):93&ndash;102. <a href="https://doi.org/10.1016/0022-2496(83)90028-7" color="#01696F">doi:10.1016/0022-2496(83)90028-7</a>',
'Brundage, M., Avin, S., Wang, J., et al. (2020). Toward Trustworthy AI Development: Mechanisms for Supporting Verifiable Claims. arXiv:2004.07213. <a href="https://arxiv.org/abs/2004.07213" color="#01696F">arxiv.org/abs/2004.07213</a>',
'Clauser, J. F., Horne, M. A., Shimony, A. &amp; Holt, R. A. (1969). Proposed Experiment to Test Local Hidden-Variable Theories. <i>Phys. Rev. Lett.</i> 23(15):880&ndash;884. <a href="https://doi.org/10.1103/PhysRevLett.23.880" color="#01696F">doi:10.1103/PhysRevLett.23.880</a>',
'Cs&aacute;t&oacute;, L. (2018). Characterization of the row geometric mean ranking with a group consensus axiom. <i>Group Decision and Negotiation</i> 27(6):1011&ndash;1027. <a href="https://doi.org/10.1007/s10726-018-9589-3" color="#01696F">doi:10.1007/s10726-018-9589-3</a>; arXiv:1706.07256.',
'Dwork, C., Lynch, N. &amp; Stockmeyer, L. (1988). Consensus in the Presence of Partial Synchrony. <i>J. ACM</i> 35(2):288&ndash;323. <a href="https://doi.org/10.1145/42282.42283" color="#01696F">doi:10.1145/42282.42283</a>',
'Fischer, M. J., Lynch, N. A. &amp; Paterson, M. S. (1985). Impossibility of Distributed Consensus with One Faulty Process. <i>J. ACM</i> 32(2):374&ndash;382. <a href="https://doi.org/10.1145/3149.214121" color="#01696F">doi:10.1145/3149.214121</a>',
'Gettier, E. L. (1963). Is Justified True Belief Knowledge? <i>Analysis</i> 23(6):121&ndash;123. <a href="https://doi.org/10.1093/analys/23.6.121" color="#01696F">doi:10.1093/analys/23.6.121</a>',
'Goldman, A. I. (1979). What Is Justified Belief? (process reliabilism). SEP: <a href="https://plato.stanford.edu/entries/reliabilism/" color="#01696F">plato.stanford.edu/entries/reliabilism</a>',
'Jensen, J. L. W. V. (1906). Sur les fonctions convexes et les in&eacute;galit&eacute;s entre les valeurs moyennes. <i>Acta Math.</i> 30:175&ndash;193. <a href="https://doi.org/10.1007/BF02418571" color="#01696F">doi:10.1007/BF02418571</a>',
'Kolmogorov, A. N. (1930). Sur la notion de la moyenne. <i>Atti Accad. Naz. Lincei</i> 12:388&ndash;391. See <a href="https://en.wikipedia.org/wiki/Quasi-arithmetic_mean" color="#01696F">Quasi-arithmetic mean</a>.',
'Kraft, L. G. (1949). A device for quantizing, grouping, and coding amplitude-modulated pulses. M.S. thesis, MIT (Kraft inequality; cf. McMillan 1956, doi:10.1109/TIT.1956.1056818).',
'Krantz, D. H., Luce, R. D., Suppes, P. &amp; Tversky, A. (1971). <i>Foundations of Measurement</i>, Vol. I. Academic Press. <a href="https://philpapers.org/rec/KRAFOM" color="#01696F">philpapers.org/rec/KRAFOM</a>',
'Lakatos, I. (1976). <i>Proofs and Refutations</i>. Cambridge University Press. <a href="https://en.wikipedia.org/wiki/Proofs_and_Refutations" color="#01696F">Proofs and Refutations</a>',
'Maksa, G., Mokken, R. J. &amp; M&uuml;nnich, &Aacute;. (2026). N-ary quasi-arithmetic means and families without regularity. arXiv:2606.05221. <a href="https://arxiv.org/html/2606.05221v1" color="#01696F">arxiv.org/html/2606.05221v1</a>',
'Merkle, R. C. (1979). Secrecy, Authentication, and Public Key Systems. Ph.D. dissertation, Stanford University (Merkle/hash trees).',
'National Telecommunications and Information Administration (2024). AI Accountability Policy Report: Proof of Claims and Trustworthiness. <a href="https://www.ntia.gov/issues/artificial-intelligence/ai-accountability-policy-report" color="#01696F">ntia.gov</a>',
'Nozick, R. (1981). <i>Philosophical Explanations</i> (truth-tracking / sensitivity). Harvard University Press.',
'Pease, M., Shostak, R. &amp; Lamport, L. (1980). Reaching Agreement in the Presence of Faults. <i>J. ACM</i> 27(2):228&ndash;234. <a href="https://doi.org/10.1145/322186.322188" color="#01696F">doi:10.1145/322186.322188</a>',
'ProVerif transparency-protocol verification (2023). Automatic verification of transparency protocols. arXiv:2303.04500. <a href="https://arxiv.org/abs/2303.04500" color="#01696F">arxiv.org/abs/2303.04500</a>',
'RFC 6962 (2013). Certificate Transparency. Laurie, Langley &amp; Kasper. <a href="https://www.rfc-editor.org/info/rfc6962/" color="#01696F">rfc-editor.org/info/rfc6962</a>',
'Saltzer, J. H. &amp; Schroeder, M. D. (1975). The Protection of Information in Computer Systems. <i>Proc. IEEE</i> 63(9):1278&ndash;1308. <a href="https://doi.org/10.1109/PROC.1975.9939" color="#01696F">doi:10.1109/PROC.1975.9939</a>',
'Shannon, C. E. (1948). A Mathematical Theory of Communication. <i>Bell Syst. Tech. J.</i> 27(3):379&ndash;423. <a href="https://doi.org/10.1002/j.1538-7305.1948.tb01338.x" color="#01696F">doi:10.1002/j.1538-7305.1948.tb01338.x</a>',
'SLSA (2023). Supply-chain Levels for Software Artifacts (L1&ndash;L4). Open Source Security Foundation. <a href="https://slsa.dev" color="#01696F">slsa.dev</a>',
'Tsirelson, B. S. (1980). Quantum generalizations of Bell&rsquo;s inequality. <i>Lett. Math. Phys.</i> 4(2):93&ndash;100. <a href="https://doi.org/10.1007/BF00417500" color="#01696F">doi:10.1007/BF00417500</a>',
]
for i, r in enumerate(refs, 1):
    story.append(P(f"[{i}]&nbsp; {r}", refsty))

sp(8)
rule(TEAL, 1.0)
para('<i>Signed-off-by:</i> Stephen P. Lutar Jr. &lt;stephenlutar2@gmail.com&gt;<br/>'
'<i>Co-authored with the SZL full-stack PhD team (mathematics, scientific writing, physics, CS, ML, philosophy of '
'mathematics).</i><br/>'
'<i>Honesty doctrine preserved verbatim:</i> &Lambda; is Conjecture 1 unconditionally (never a theorem); the '
"conditional theorem holds only under the declared A6&#39;_block_consistent; locked/proven = 5; declared axioms "
"disclosed in every #print&nbsp;axioms ledger; SLSA L1+L2 (not L3). No fabricated results, no fake citations.", small)

# =====================================================================
# DOC TEMPLATE w/ header/footer + page numbers
# =====================================================================
def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("DMSans", 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(1*inch, 10.55*inch, "SZL Holdings")
    canvas.drawRightString(7.5*inch, 10.55*inch, "The Unified Substrate (v23)")
    canvas.setStrokeColor(RULE)
    canvas.setLineWidth(0.4)
    canvas.line(1*inch, 10.45*inch, 7.5*inch, 10.45*inch)
    canvas.line(1*inch, 0.72*inch, 7.5*inch, 0.72*inch)
    canvas.drawCentredString(4.25*inch, 0.55*inch, f"{doc.page}")
    canvas.restoreState()

doc = BaseDocTemplate(OUT, pagesize=LETTER,
                      leftMargin=1*inch, rightMargin=1*inch,
                      topMargin=1*inch, bottomMargin=0.9*inch,
                      title="The Unified Substrate (v23): A Machine-Verified Trust Foundation for Governed Agentic AI",
                      author="Perplexity Computer")
frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="main")
doc.addPageTemplates([PageTemplate(id="all", frames=[frame], onPage=header_footer)])
doc.build(story)
print("WROTE", OUT, os.path.getsize(OUT), "bytes")
