"""Assemble Multimedia Appendices 2 (figures) and 3 (tables) from numbered units
(JMIR R1 Batch 2c, C4).

Reads ma_order.yaml, numbers the units (Figure S1.. in MA2, Table S1.. in MA3),
resolves {{F:id}} / {{T:id}} placeholders in every caption and footnote, and
writes:
  Multimedia_Appendix_2_R1.docx / .md   figures with captions
  Multimedia_Appendix_3_R1.docx / .md   real Word tables with captions and footnotes
  ma_numbering_map.csv                   unit id -> appendix and number
Run from anywhere with revision_r1/.venv:  python assemble.py
"""

from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

import yaml
from docx.enum.section import WD_ORIENT, WD_SECTION
from docx.shared import Inches

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "scripts"))
from c_common import jmir_text  # noqa: E402
from c_docx import add_runs, md_table, md_text, new_doc, para, table  # noqa: E402

UT, UF = HERE / "units" / "tables", HERE / "units" / "figures"
PH = re.compile(r"\{\{([FT]):([a-z0-9_]+)\}\}")


def load_order():
    o = yaml.safe_load((HERE / "ma_order.yaml").read_text())
    figs, tabs = o["ma2_figures"], o["ma3_tables"]
    have_f = {p.stem for p in UF.glob("*.json")}; have_t = {p.stem for p in UT.glob("*.json")}
    for name, lst, have in (("ma2_figures", figs, have_f), ("ma3_tables", tabs, have_t)):
        if len(set(lst)) != len(lst):
            sys.exit(f"{name}: duplicate unit id")
        if set(lst) != have:
            sys.exit(f"{name}: order lists {sorted(set(lst) - have)} without a unit and omits {sorted(have - set(lst))}")
    return figs, tabs


def resolver(fnum, tnum, here):
    def sub(m):
        kind, uid = m.group(1), m.group(2)
        if kind == "F":
            if uid not in fnum:
                sys.exit(f"unresolved figure placeholder {uid}")
            return f"Figure S{fnum[uid]}" if here == "MA2" else f"Multimedia Appendix 2, Figure S{fnum[uid]}"
        if uid not in tnum:
            sys.exit(f"unresolved table placeholder {uid}")
        return f"Table S{tnum[uid]}" if here == "MA3" else f"Multimedia Appendix 3, Table S{tnum[uid]}"
    return lambda s: jmir_text(PH.sub(sub, s))


def split_caption(md):
    m = re.match(r"\*\*(.+?)\*\*\s*(.*)", md.strip(), re.S)
    return (m[1], m[2]) if m else ("", md.strip())


def build_ma2(figs, fnum, tnum):
    res = resolver(fnum, tnum, "MA2")
    d = new_doc("Multimedia Appendix 2. Supplementary Figures")
    L = ["# Multimedia Appendix 2. Supplementary Figures", ""]
    rows = []
    for uid in figs:
        n = fnum[uid]
        title, body = split_caption((UF / f"{uid}_caption.md").read_text(encoding="utf-8"))
        title, body = res(title), res(body)
        d.add_page_break()
        d.add_picture(str(UF / f"{uid}.png"), width=Inches(6.6))
        p = d.add_paragraph()
        r = p.add_run(f"Figure S{n}. "); r.bold = True
        add_runs(p, title + " ", bold=True)
        add_runs(p, body)
        L += [f"![Figure S{n}](units/figures/{uid}.png)", "", f"**Figure S{n}. {md_text(title)}** {md_text(body)}", ""]
        rows.append({"unit_id": uid, "appendix": "Multimedia Appendix 2", "number": f"Figure S{n}", "title": title,
                     "files": f"units/figures/{uid}.png; units/figures/{uid}.pdf" + ("; units/figures/forward_validation_sankey.svg"
                                                                                  if uid == "forward_validation_sankey" else "")})
    d.save(HERE / "Multimedia_Appendix_2_R1.docx")
    (HERE / "Multimedia_Appendix_2_R1.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    return rows


def build_ma3(tabs, fnum, tnum):
    res = resolver(fnum, tnum, "MA3")
    d = new_doc("Multimedia Appendix 3. Supplementary Tables")
    L = ["# Multimedia Appendix 3. Supplementary Tables", ""]
    rows = []
    for uid in tabs:
        n = tnum[uid]
        spec = json.loads((UT / f"{uid}.json").read_text(encoding="utf-8"))
        want = bool(spec["landscape"])
        sec = d.add_section(WD_SECTION.NEW_PAGE)
        sec.orientation = WD_ORIENT.LANDSCAPE if want else WD_ORIENT.PORTRAIT
        w, h = sec.page_width, sec.page_height
        if (want and w < h) or (not want and w > h):
            sec.page_width, sec.page_height = h, w
        cap = res(spec["caption"])
        p = d.add_paragraph(); r = p.add_run(f"Table S{n}. "); r.bold = True
        add_runs(p, cap, bold=True)
        hdr = [res(h) for h in spec["header"]]
        body = [[res(str(c)) for c in row] for row in spec["rows"]]
        table(d, hdr, body, size=7 if want else 8, group_rows=set(spec["group_rows"]))
        notes = [res(x) for x in spec["notes"]]
        for x in notes:
            para(d, x, 8, space_after=2)
        L += [f"**Table S{n}. {md_text(cap)}**", "", md_table(hdr, body, set(spec["group_rows"])), ""] + [md_text(x) + "\n" for x in notes]
        rows.append({"unit_id": uid, "appendix": "Multimedia Appendix 3", "number": f"Table S{n}", "title": cap,
                     "files": f"units/tables/{uid}.json"})
    d.save(HERE / "Multimedia_Appendix_3_R1.docx")
    (HERE / "Multimedia_Appendix_3_R1.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    return rows


def main():
    figs, tabs = load_order()
    fnum = {u: i for i, u in enumerate(figs, 1)}
    tnum = {u: i for i, u in enumerate(tabs, 1)}
    rows = build_ma2(figs, fnum, tnum) + build_ma3(tabs, fnum, tnum)
    with open(HERE / "ma_numbering_map.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["unit_id", "appendix", "number", "title", "files"])
        w.writeheader(); w.writerows(rows)
    left = [p for p in ("Multimedia_Appendix_2_R1.md", "Multimedia_Appendix_3_R1.md") if "{{" in (HERE / p).read_text()]
    if left:
        sys.exit(f"unresolved placeholders in {left}")
    print(f"assembled: {len(figs)} figures (MA2), {len(tabs)} tables (MA3)")


if __name__ == "__main__":
    main()
