"""Shared helpers for the v3 (final-numbering) build of the JMIR R1 tables and appendices.

New file (2026-11-02). Reads, never writes, revision_r1/final/ (Batch 2c/2d outputs).
Everything it builds goes to revision_r1/final/v3/. Formatting and Word helpers are
copies of c_common.py / c_docx.py (not imported, so nothing upstream is touched).
"""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt

HERE = Path(__file__).resolve().parent
V3 = HERE.parent                               # revision_r1/final/v3b/
SRC = HERE.parent.parent                       # revision_r1/final/ (read only)
BOOK_CSV = SRC / "NUMBERS_BOOK_R1_v2.csv"
Y5 = [2021, 2022, 2023, 2024, 2025]

TITLE_FINAL = ("Evaluative Stance Toward Artificial Intelligence in High-Quartile Medical Journal Abstracts, "
               "2021-2025: Infoveillance Study")
AUTHORS = "Lixing Wang, Dan Poenaru"


def book() -> dict:
    with open(BOOK_CSV, encoding="utf-8") as f:
        return {r["id"]: r for r in csv.DictReader(f)}


def num(r, k):
    v = r[k]
    return float(v) if v not in ("", None) else float("nan")


def jmir_text(v: str) -> str:
    """Hyphen for ranges; no comma in 4-digit numbers (copy of c_common.jmir_text)."""
    v = v.replace("\u2013", "-")
    return re.sub(r"(?<![\d,.])(\d),(\d{3})(?![\d,])", r"\1\2", v)


# ------------------------------------------------------------------ placeholders
PH = re.compile(r"\{\{([FTN]):([a-z0-9_]+)\}\}")


def resolver(fnum: dict, tnum: dict, nnum: dict, here: str, jmir: bool = True):
    """here: 'MA1' (notes), 'MA2' (tables), 'MA3' (figures) or 'MAIN'."""
    def sub(m):
        kind, uid = m.group(1), m.group(2)
        if kind == "F":
            if uid not in fnum:
                raise SystemExit(f"unresolved figure placeholder {uid}")
            return f"Figure S{fnum[uid]}" if here == "MA3" else f"Multimedia Appendix 3, Figure S{fnum[uid]}"
        if kind == "T":
            if uid not in tnum:
                raise SystemExit(f"unresolved table placeholder {uid}")
            return f"Table S{tnum[uid]}" if here == "MA2" else f"Multimedia Appendix 2, Table S{tnum[uid]}"
        if uid not in nnum:
            raise SystemExit(f"unresolved note placeholder {uid}")
        return f"Note {nnum[uid]}" if here == "MA1" else f"Multimedia Appendix 1, Note {nnum[uid]}"
    return (lambda s: compact(jmir_text(PH.sub(sub, s)))) if jmir else (lambda s: compact(PH.sub(sub, s)))


_MA_RUN = re.compile(r"Multimedia Appendix (\d), (Table|Figure) S(\d+)(?:(?:, | and )Multimedia Appendix \1, \2 S\d+)+")
_LOCAL_RUN = re.compile(r"(?<!Appendix \d, )\b(Table|Figure) S(\d+)(?:(?:, | and )\1 S\d+)+")


def _listing(nums):
    nums = [f"S{x}" for x in sorted(set(int(v) for v in nums))]
    return nums[0] if len(nums) == 1 else ", ".join(nums[:-1]) + " and " + nums[-1]


def compact(s: str) -> str:
    """'Multimedia Appendix 2, Table S20, Multimedia Appendix 2, Table S1 and ...' -> 'Multimedia Appendix 2, Tables S1, S20 and ...'."""
    s = _MA_RUN.sub(lambda m: f"Multimedia Appendix {m[1]}, {m[2]}s " + _listing(re.findall(r"S(\d+)", m[0])), s)
    s = _LOCAL_RUN.sub(lambda m: f"{m[1]}s " + _listing(re.findall(r"S(\d+)", m[0])), s)
    return s


# ------------------------------------------------------------------ Word helpers (copied from c_docx.py)
P_RE = re.compile(r"(?<![A-Za-z])(P)(?=[=<>])")


def new_doc(appendix_name=None):
    d = Document()
    st = d.styles["Normal"]
    st.font.name = "Arial"; st.font.size = Pt(10)
    st.element.rPr.rFonts.set(qn("w:eastAsia"), "Arial")
    sec = d.sections[0]
    for m in ("left_margin", "right_margin", "top_margin", "bottom_margin"):
        setattr(sec, m, Inches(0.8))
    if appendix_name:
        p = d.add_paragraph(); r = p.add_run(appendix_name); r.bold = True; r.font.size = Pt(12)
        p = d.add_paragraph(); p.add_run(TITLE_FINAL)
        p = d.add_paragraph(); p.add_run(AUTHORS)
    return d


def add_runs(par, text, size=None, bold=False, italic=False):
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


def table(d, header, rows, size=8, group_rows=(), sub_rows=()):
    """Real Word table. group_rows: merged bold shaded headings; sub_rows: bold shaded
    per-cell rows used as an internal column header for a panel."""
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
            add_runs(cells[j].paragraphs[0], "" if v is None else str(v), size, bold=(i in sub_rows))
            if i in sub_rows:
                _shade(cells[j], "F2F2F2")
    return t


def md_table(header, rows, group_rows=(), sub_rows=()):
    esc = lambda s: str(s).replace("|", "\\|").replace("\n", " ")
    ital = lambda s: P_RE.sub(r"*\1*", esc(s))
    L = ["| " + " | ".join(ital(h) for h in header) + " |", "|" + "---|" * len(header)]
    for i, r in enumerate(rows):
        if i in group_rows:
            L.append("| **" + esc(r[0]) + "** |" + " |" * (len(header) - 1))
        elif i in sub_rows:
            L.append("| " + " | ".join(f"**{esc(x)}**" if str(x).strip() else "" for x in r) + " |")
        else:
            L.append("| " + " | ".join(ital(x) for x in r) + " |")
    return "\n".join(L)


def md_text(s):
    return P_RE.sub(r"*\1*", s)


def write_json(path: Path, obj):
    path.write_text(json.dumps(obj, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
