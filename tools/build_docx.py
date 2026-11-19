#!/usr/bin/env python3
"""Writes the after resume as an editable Word file, from the same content as the page."""
import pathlib, sys
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_TAB_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from build import AFTER, NAME, DOCS

GREEN = RGBColor(0x1E, 0x4D, 0x45)
doc = Document()
sec = doc.sections[0]
sec.page_width, sec.page_height = Inches(8.5), Inches(11)
sec.left_margin = sec.right_margin = Inches(0.6)
sec.top_margin, sec.bottom_margin = Inches(0.5), Inches(0.45)
RIGHT = sec.page_width - sec.left_margin - sec.right_margin
st = doc.styles["Normal"]; st.font.name = "Calibri"; st.font.size = Pt(10.5)
st.paragraph_format.space_after = Pt(0); st.paragraph_format.line_spacing = 1.1
doc.core_properties.title = f"{NAME} resume (concept demo)"
doc.core_properties.author = "Alex Mercer (concept demo)"

def para(text="", bold=False, size=None, color=None, after=0, before=0):
    p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(after); p.paragraph_format.space_before = Pt(before)
    if text:
        r = p.add_run(text); r.bold = bold
        if size: r.font.size = Pt(size)
        if color: r.font.color.rgb = color
    return p

def rule(p, sz=6):
    pPr = p._p.get_or_add_pPr(); b = OxmlElement("w:pBdr"); bt = OxmlElement("w:bottom")
    for k, v in (("w:val", "single"), ("w:sz", str(sz)), ("w:space", "2"), ("w:color", "BFC3C9")): bt.set(qn(k), v)
    b.append(bt); pPr.append(b)

def heading(t):
    p = para(t.upper(), bold=True, size=10, color=GREEN, before=10, after=4); rule(p)

def left_right(left_runs, right):
    p = para(); p.paragraph_format.tab_stops.add_tab_stop(RIGHT, WD_TAB_ALIGNMENT.RIGHT)
    for t, b in left_runs: r = p.add_run(t); r.bold = b
    p.add_run("\t" + right); return p

para(NAME, bold=True, size=22)
para(AFTER["title"], size=12, color=GREEN, before=2)
p = para(" · ".join(AFTER["contact"]), size=9.5, before=2, after=4); rule(p, 12)
heading("Summary"); para(AFTER["summary"])
heading("Experience")
for i, j in enumerate(AFTER["jobs"]):
    p = left_right([(j["role"], True), (f", {j['org']} · {j['place']}", False)], j["dates"])
    if i: p.paragraph_format.space_before = Pt(7)
    for b in j["bullets"]:
        bp = doc.add_paragraph(b, style="List Bullet"); bp.paragraph_format.space_before = Pt(2)
heading("Skills")
for k, v in AFTER["skills"]:
    p = para(); p.add_run(k + ": ").bold = True; p.add_run(v); p.paragraph_format.space_after = Pt(2)
heading("Education and certifications")
for a, b, c in AFTER["education"]:
    left_right([(a, True), ((", " + b) if b else "", False)], c)
p = para("Concept demo by Alex Mercer. The person, employers and school are fictional; all figures are example data.", size=7.5, color=RGBColor(0x7A, 0x7F, 0x88), before=14)
doc.save(DOCS / "Noa-Brightwater-resume-DEMO.docx")
print("wrote docx")
