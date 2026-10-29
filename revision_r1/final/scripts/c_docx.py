"""Word (.docx) and Markdown helpers for Batch 2c tables and appendices.

Tables are real Word tables (python-docx, style 'Table Grid'), never images.
'P' in 'P=', 'P<' or 'P>' is set in italics (JMIR). Revision venv only.
"""

from __future__ import annotations

import re

from docx import Document
from docx.enum.section import WD_ORIENT
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt

from c_common import AUTHORS, TITLE_NOTE, TITLE_R1

P_RE = re.compile(r"(?<![A-Za-z])(P)(?=[=<>])")


def new_doc(appendix_name=None, landscape=False):
    d = Document()
    st = d.styles["Normal"]
    st.font.name = "Arial"; st.font.size = Pt(10)
    st.element.rPr.rFonts.set(qn("w:eastAsia"), "Arial")
    sec = d.sections[0]
    if landscape:
        set_landscape(sec)
    for m in ("left_margin", "right_margin", "top_margin", "bottom_margin"):
        setattr(sec, m, Inches(0.8))
    if appendix_name:
        p = d.add_paragraph(); r = p.add_run(appendix_name); r.bold = True; r.font.size = Pt(12)
        p = d.add_paragraph(); p.add_run(TITLE_R1)
        p = d.add_paragraph(); p.add_run(AUTHORS)
        p = d.add_paragraph(); r = p.add_run(TITLE_NOTE); r.italic = True; r.font.size = Pt(8)
    return d


def set_landscape(sec):
    sec.orientation = WD_ORIENT.LANDSCAPE
    w, h = sec.page_width, sec.page_height
    if w < h:
        sec.page_width, sec.page_height = h, w


def add_runs(par, text, size=None, bold=False, italic=False):
    """Add text with italic P before =, < or >."""
    parts = P_RE.split(text)
    for i, part in enumerate(parts):
        if not part:
            continue
        r = par.add_run(part)
        r.bold = bold
        r.italic = italic or (part == "P" and i % 2 == 1)
        if size:
            r.font.size = Pt(size)
    return par


def para(d, text, size=10, bold=False, italic=False, space_after=4):
    p = d.add_paragraph()
    add_runs(p, text, size, bold, italic)
    p.paragraph_format.space_after = Pt(space_after)
    return p


def _shade(cell, hexcol):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd"); shd.set(qn("w:val"), "clear"); shd.set(qn("w:color"), "auto"); shd.set(qn("w:fill"), hexcol)
    tcPr.append(shd)


def table(d, header, rows, widths=None, size=8, group_rows=()):
    """Real Word table. group_rows: indices of rows rendered as bold, shaded group headings."""
    t = d.add_table(rows=1, cols=len(header))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for j, h in enumerate(header):
        c = t.rows[0].cells[j]; c.text = ""
        add_runs(c.paragraphs[0], str(h), size, bold=True)
        _shade(c, "E7E6E6")
    hdr = t.rows[0]._tr.get_or_add_trPr()
    th = OxmlElement("w:tblHeader"); th.set(qn("w:val"), "true"); hdr.append(th)
    for i, row in enumerate(rows):
        cells = t.add_row().cells
        if i in group_rows:
            m = cells[0].merge(cells[-1]); m.text = ""
            add_runs(m.paragraphs[0], str(row[0]), size, bold=True)
            _shade(m, "F2F2F2")
            continue
        for j, v in enumerate(row):
            cells[j].text = ""
            add_runs(cells[j].paragraphs[0], "" if v is None else str(v), size)
    if widths:
        t.autofit = False
        for row in t.rows:
            for j, w in enumerate(widths):
                row.cells[j].width = Inches(w)
    return t


def md_table(header, rows, group_rows=()):
    esc = lambda s: str(s).replace("|", "\\|").replace("\n", " ")
    ital = lambda s: P_RE.sub(r"*\1*", esc(s))
    L = ["| " + " | ".join(ital(h) for h in header) + " |", "|" + "---|" * len(header)]
    for i, r in enumerate(rows):
        if i in group_rows:
            L.append("| **" + esc(r[0]) + "** |" + " |" * (len(header) - 1))
        else:
            L.append("| " + " | ".join(ital(x) for x in r) + " |")
    return "\n".join(L)


def md_text(s):
    return P_RE.sub(r"*\1*", s)
