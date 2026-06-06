#!/usr/bin/env python3
"""
_thesisbuild.py -- Shared ReportLab Platypus rendering library for the SZL
Holdings Ouroboros thesis line (v19-v22). Factored out of the v23 build_pdf.py
exemplar so every version shares the same proven, glyph-safe typography.

No LaTeX engine is used in the sandbox; this is the compiled rendering of each
version's main.tex / main.md. Embeds DM Sans + JetBrains Mono; uses DejaVu Sans
as a Greek/math fallback ("Math") so glyphs like Lambda Phi sum prod radic le ge
ne render correctly with no tofu boxes.

Each version's build_pdf.py does:
    from _thesisbuild import *
    new_doc(fonts_dir)            # registers fonts (idempotent)
    ... build story via section()/para()/table()/theorem_box() ...
    build(out_path, title=..., running_title=...)
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
    HRFlowable, KeepTogether, ListFlowable, ListItem, PageBreak
)
import re as _re

# ---------------------------------------------------------------- fonts
_FONTS_REGISTERED = False
def register_fonts(fonts_dir):
    global _FONTS_REGISTERED
    if _FONTS_REGISTERED:
        return
    pdfmetrics.registerFont(TTFont("DMSans", os.path.join(fonts_dir, "DMSans-Regular.ttf")))
    pdfmetrics.registerFont(TTFont("DMSans-Bold", os.path.join(fonts_dir, "DMSans-Bold.ttf")))
    pdfmetrics.registerFont(TTFont("DMSans-Italic", os.path.join(fonts_dir, "DMSans-Italic.ttf")))
    pdfmetrics.registerFont(TTFont("DMSans-Med", os.path.join(fonts_dir, "DMSans-Medium.ttf")))
    pdfmetrics.registerFont(TTFont("Mono", os.path.join(fonts_dir, "JetBrainsMono-Regular.ttf")))
    pdfmetrics.registerFontFamily("DMSans", normal="DMSans", bold="DMSans-Bold",
                                  italic="DMSans-Italic", boldItalic="DMSans-Bold")
    dj = "/usr/share/fonts/truetype/dejavu"
    pdfmetrics.registerFont(TTFont("Math", os.path.join(dj, "DejaVuSans.ttf")))
    pdfmetrics.registerFont(TTFont("Math-Bold", os.path.join(dj, "DejaVuSans-Bold.ttf")))
    pdfmetrics.registerFont(TTFont("Math-Italic", os.path.join(dj, "DejaVuSans-Oblique.ttf")))
    pdfmetrics.registerFontFamily("Math", normal="Math", bold="Math-Bold",
                                  italic="Math-Italic", boldItalic="Math-Bold")
    _FONTS_REGISTERED = True

# ---------------------------------------------------------------- glyph fixer
# HTML entities for Greek letters / math operators DM Sans cannot render.
_MATH_ENTS = [
    "Lambda", "Phi", "Omega", "Sigma", "Pi", "Delta",
    "alpha", "beta", "mu", "rho", "pi", "phi", "lambda", "sigma", "tau", "epsilon", "delta", "theta",
    "prod", "sum", "radic", "le", "ge", "asymp", "equiv", "cong", "sim", "prop",
    "ne", "isin", "notin", "ell", "rArr", "rArr", "rarr", "larr", "harr", "forall", "exist",
    "prime", "not", "minus", "times", "middot", "plusmn", "infin", "part", "nabla", "int",
    "cap", "cup", "sub", "sube", "sup", "supe", "empty", "and", "or",
    "langle", "rangle", "lang", "rang", "otimes", "oplus", "perp", "sdot", "lowast",
]
_MATH_RE = _re.compile("&(" + "|".join(_MATH_ENTS) + ");")
# Numeric entities outside DM Sans coverage:
#  hbar 8463, blackboard N 8469, R 8477, Z 8484, Q 8474, parallel 8741,
#  script-l 8467, intersection 8745, union 8746, subset 8834, element 8712,
#  ceil/floor 8968-8971, angle 8736, leq/geq 8804/8805, approx 8776, neq 8800,
#  arrows 8594/8592/8596/8658, sqrt 8730, prod 8719, sum 8721, infinity 8734,
#  bullet 8226, perp 8869, top 8868, dagger 8224, times 215, div 247, degree 176,
#  superscripts handled by <super>; otimes 8855, oplus 8853.
_MATH_NUM = {8463, 8469, 8477, 8484, 8474, 8741, 8467, 8745, 8746, 8834, 8712,
             8968, 8969, 8970, 8971, 8736, 8804, 8805, 8776, 8800, 8594, 8592,
             8596, 8658, 8730, 8719, 8721, 8734, 8226, 8869, 8868, 8855, 8853,
             8801, 8744, 8743, 8709, 8704, 8707, 8595, 8593, 8729, 215, 247, 8722,
             8320, 8321, 8322, 8323, 8324, 8325, 8326, 8327, 8328, 8329}
_MATH_NUM_RE = _re.compile("&#(" + "|".join(str(n) for n in _MATH_NUM) + ");")
def fixglyphs(text):
    if not text:
        return text
    text = _MATH_RE.sub(lambda m: f'<font name="Math">&{m.group(1)};</font>', text)
    text = _MATH_NUM_RE.sub(lambda m: f'<font name="Math">&#{m.group(1)};</font>', text)
    return text

# ---------------------------------------------------------------- palette
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

def S(name, **kw):
    return ParagraphStyle(name, **kw)

# ---------------------------------------------------------------- styles
body = S("body", fontName="DMSans", fontSize=9.5, leading=14, textColor=INK,
         alignment=TA_JUSTIFY, spaceAfter=6)
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
abh = S("abh", fontName="DMSans-Bold", fontSize=11, alignment=TA_CENTER, textColor=INK, spaceAfter=4)
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
codest = S("code", fontName="Mono", fontSize=7.6, leading=10.5, textColor=INK,
           leftIndent=8, rightIndent=8, spaceAfter=3, spaceBefore=2)
cell = S("cell", fontName="DMSans", fontSize=7.8, leading=10.5, textColor=INK)
cellb = S("cellb", fontName="DMSans-Bold", fontSize=7.8, leading=10.5, textColor=INK)
cellh = S("cellh", fontName="DMSans-Bold", fontSize=8, leading=10.5, textColor=colors.white)

def M(s):  # monospace inline shorthand
    return f'<font name="Mono" size="8">{s}</font>'

# status tags
LOCKED = '<font name="DMSans-Bold" color="#01696F" size="8">[LOCKED / kernel-verified]</font>'
SFREE  = '<font name="DMSans-Bold" color="#01696F" size="8">[sorry-free, Lean-core only]</font>'
AXIOM  = '<font name="DMSans-Bold" color="#964219" size="8">[axiom-gated]</font>'
CIG    = '<font name="DMSans-Bold" color="#01696F" size="8">[CI-green]</font>'
PEND   = '<font name="DMSans-Bold" color="#5A5957" size="8">[CI-pending]</font>'
OPEN   = '<font name="DMSans-Bold" color="#5A5957" size="8">[open obligation]</font>'
CONJ   = '<font name="DMSans-Bold" color="#A12C7B" size="8">[Conjecture 1 - NOT a theorem]</font>'
OPFACT = '<font name="DMSans-Bold" color="#964219" size="8">[operational fact - not proven]</font>'

# ---------------------------------------------------------------- story + helpers
story = []
def reset_story():
    global story
    story = []
    Sec.n = 0; Sec.sub = 0

def para(text, st=body): story.append(Paragraph(fixglyphs(text), st))
def P(text, st): return Paragraph(fixglyphs(text), st)
def sp(h=6): story.append(Spacer(1, h))
def rule(c=RULE, w=0.8): story.append(HRFlowable(width="100%", thickness=w, color=c, spaceBefore=4, spaceAfter=4))
def pagebreak(): story.append(PageBreak())

class Sec:
    n = 0; sub = 0
def section(t):
    Sec.n += 1; Sec.sub = 0
    story.append(Paragraph(fixglyphs(f'{Sec.n}.&nbsp;&nbsp;{t}'), h1))
def subsection(t):
    Sec.sub += 1
    story.append(Paragraph(fixglyphs(f'{Sec.n}.{Sec.sub}&nbsp;&nbsp;{t}'), h2))
def subsub(t):
    story.append(Paragraph(fixglyphs(t), h3))

def boxed(flow_list, bg=BOXBG, border=RULE):
    t = Table([[flow_list]], colWidths=[6.5*inch])
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1),bg),
        ("BOX",(0,0),(-1,-1),0.6,border),
        ("LEFTPADDING",(0,0),(-1,-1),8),("RIGHTPADDING",(0,0),(-1,-1),8),
        ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
    ]))
    story.append(KeepTogether(t)); sp(4)

def theorem_box(label, statustags, statement, proof_text=None, bg=BOXBG):
    flows = [Paragraph(fixglyphs(f'{label} &nbsp; {statustags}'), thmhead),
             Paragraph(fixglyphs(statement), thm)]
    if proof_text:
        flows.append(Paragraph(fixglyphs(f'<b>Proof / Lean reference.</b> {proof_text}'), proof))
    boxed(flows, bg=bg)

def codeblock(lines, bg=colors.HexColor("#F2F1ED")):
    flows = [Paragraph(fixglyphs(ln if ln.strip() else "&nbsp;"), codest) for ln in lines]
    boxed(flows, bg=bg)

def bullets(items, st=li):
    items2 = [ListItem(Paragraph(fixglyphs(x), st), leftIndent=14, value=None) for x in items]
    story.append(ListFlowable(items2, bulletType="bullet", start="•",
                              bulletColor=TEAL, bulletFontSize=7, leftIndent=16))
    sp(3)

def numbered(items, st=li):
    items2 = [ListItem(Paragraph(fixglyphs(x), st), leftIndent=14) for x in items]
    story.append(ListFlowable(items2, bulletType="1", leftIndent=18,
                              bulletFontName="DMSans-Bold", bulletColor=TEAL))
    sp(3)

def table(headers, rows, colw, fontsize=7.8):
    data = [[Paragraph(fixglyphs(h), cellh) for h in headers]]
    for r in rows:
        data.append([Paragraph(fixglyphs(c.replace("**","")), cellb)
                     if (isinstance(c, str) and c.startswith("**")) else Paragraph(fixglyphs(c), cell)
                     for c in r])
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

def title_block(title_text, subtitle_text, author_text, meta_lines):
    para(title_text, title)
    para(subtitle_text, subtitle)
    para(author_text, author)
    for ml in meta_lines:
        para(ml, meta)
    sp(8); rule(TEAL, 1.0)

def abstract_block(abstract_text, keywords, honesty_note):
    para("Abstract", abh)
    para(abstract_text, abst)
    sp(2)
    para(f'<b>Keywords:</b> {keywords}', small)
    rule(RULE)
    para(honesty_note, note)
    pagebreak()

def references_block(refs):
    section("References")
    for i, r in enumerate(refs, 1):
        story.append(P(f"[{i}]&nbsp; {r}", refsty))

def signoff_block(extra=""):
    sp(8); rule(TEAL, 1.0)
    para('<i>Signed-off-by:</i> Stephen P. Lutar Jr. &lt;stephenlutar2@gmail.com&gt;<br/>'
         '<i>Co-authored with the SZL full-stack PhD team (mathematics, scientific writing, '
         'physics, CS, ML, philosophy of mathematics).</i><br/>'
         '<i>Honesty doctrine preserved verbatim:</i> &Lambda; is Conjecture 1 unconditionally '
         '(never a theorem); the conditional uniqueness theorem holds only under the declared '
         f'{M("A6&#39;_block_consistent")}; locked/proven = 5 {{F1,F11,F12,F18,F19}} @ '
         f'{M("c7c0ba17")} (749/14/163); declared axioms disclosed in every #print&nbsp;axioms '
         'ledger; SLSA L1+L2 (not L3). No fabricated results, no fake citations. ' + extra, small)

# ---------------------------------------------------------------- doc build
def build(out_path, title, running_title):
    def header_footer(canvas, doc):
        canvas.saveState()
        canvas.setFont("DMSans", 7.5)
        canvas.setFillColor(MUTED)
        canvas.drawString(1*inch, 10.55*inch, "SZL Holdings")
        canvas.drawRightString(7.5*inch, 10.55*inch, running_title)
        canvas.setStrokeColor(RULE); canvas.setLineWidth(0.4)
        canvas.line(1*inch, 10.45*inch, 7.5*inch, 10.45*inch)
        canvas.line(1*inch, 0.72*inch, 7.5*inch, 0.72*inch)
        canvas.drawCentredString(4.25*inch, 0.55*inch, f"{doc.page}")
        canvas.restoreState()
    doc = BaseDocTemplate(out_path, pagesize=LETTER,
                          leftMargin=1*inch, rightMargin=1*inch,
                          topMargin=1*inch, bottomMargin=0.9*inch,
                          title=title, author="Perplexity Computer")
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="main")
    doc.addPageTemplates([PageTemplate(id="all", frames=[frame], onPage=header_footer)])
    doc.build(story)
    print("WROTE", out_path, os.path.getsize(out_path), "bytes")
