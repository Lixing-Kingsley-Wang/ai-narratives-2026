"""Assemble Multimedia Appendix 2 (supplementary tables) and 3 (supplementary figures), v3.

Numbering follows ma_order_v3.yaml (first citation, Methods -> Results -> Discussion). Tables are
cited first in the manuscript, so tables are Multimedia Appendix 2 and figures Multimedia Appendix 3
(the reverse of the submitted version). Reads units from revision_r1/final/v3/ma/units/.
Writes Multimedia_Appendix_2_R1_v3.{docx,md}, Multimedia_Appendix_3_R1_v3.{docx,md} and
ma_numbering_map_v3.csv in revision_r1/final/v3/ma/.
"""
from __future__ import annotations

import csv
import json
import re

import yaml
from docx.enum.section import WD_ORIENT, WD_SECTION
from docx.shared import Inches
from PIL import Image

from v3_common import V3, add_runs, md_table, md_text, new_doc, para, resolver, table

MA = V3 / "ma"
UT, UF = MA / "units" / "tables", MA / "units" / "figures"
O = yaml.safe_load((MA / "ma_order_v3.yaml").read_text())
NN = {u: i for i, u in enumerate(O["ma1_notes"], 1)}
TN = {u: i for i, u in enumerate(O["ma2_tables"], 1)}
FN = {u: i for i, u in enumerate(O["ma3_figures"], 1)}


def split_caption(md):
    m = re.match(r"\*\*(.+?)\*\*\s*(.*)", md.strip(), re.S)
    return (m[1], m[2]) if m else ("", md.strip())


def build_tables():
    res = resolver(FN, TN, NN, "MA2")
    d = new_doc("Multimedia Appendix 2. Supplementary Tables")
    L = ["# Multimedia Appendix 2. Supplementary Tables", ""]
    rows = []
    have = {p.stem for p in UT.glob("*.json")}
    assert set(O["ma2_tables"]) == have, (set(O["ma2_tables"]) ^ have)
    for uid in O["ma2_tables"]:
        n = TN[uid]
        s = json.loads((UT / f"{uid}.json").read_text(encoding="utf-8"))
        want = bool(s["landscape"])
        sec = d.add_section(WD_SECTION.NEW_PAGE)
        sec.orientation = WD_ORIENT.LANDSCAPE if want else WD_ORIENT.PORTRAIT
        w, h = sec.page_width, sec.page_height
        if (want and w < h) or (not want and w > h):
            sec.page_width, sec.page_height = h, w
        cap = res(s["caption"])
        p = d.add_paragraph(); r = p.add_run(f"Table S{n}. "); r.bold = True
        add_runs(p, cap, bold=True)
        hdr = [res(x) for x in s["header"]]
        body = [[res(str(c)) for c in row] for row in s["rows"]]
        g, sb = set(s["group_rows"]), set(s.get("sub_rows", []))
        assert all(len(r_) == len(hdr) for i, r_ in enumerate(body) if i not in g), uid
        table(d, hdr, body, size=7 if want else 8, group_rows=g, sub_rows=sb)
        notes = [res(x) for x in s["notes"]]
        for x in notes:
            para(d, x, 8, space_after=2)
        L += [f"**Table S{n}. {md_text(cap)}**", "", md_table(hdr, body, g, sb), ""] + [md_text(x) + "\n" for x in notes]
        rows.append({"unit_id": uid, "appendix": "Multimedia Appendix 2", "number": f"Table S{n}", "title": cap})
    d.save(MA / "Multimedia_Appendix_2_R1_v3.docx")
    (MA / "Multimedia_Appendix_2_R1_v3.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    return rows


def build_figures():
    res = resolver(FN, TN, NN, "MA3")
    d = new_doc("Multimedia Appendix 3. Supplementary Figures")
    L = ["# Multimedia Appendix 3. Supplementary Figures", ""]
    rows = []
    for uid in O["ma3_figures"]:
        n = FN[uid]
        title, body = split_caption((UF / f"{uid}_caption.md").read_text(encoding="utf-8"))
        title, body = res(title), res(body)
        img = UF / f"{uid}.png"
        with Image.open(img) as im:
            wpx, hpx = im.size
            dpi = (im.info.get("dpi") or (600, 600))[0] or 600
        width = min(6.6, wpx / dpi)
        if width * hpx / wpx > 8.0:          # keep tall figures on one page
            width = 8.0 * wpx / hpx
        d.add_page_break()
        d.add_picture(str(img), width=Inches(width))
        p = d.add_paragraph()
        r = p.add_run(f"Figure S{n}. "); r.bold = True
        add_runs(p, title + " ", bold=True)
        add_runs(p, body)
        L += [f"![Figure S{n}](units/figures/{uid}.png)", "", f"**Figure S{n}. {md_text(title)}** {md_text(body)}", ""]
        rows.append({"unit_id": uid, "appendix": "Multimedia Appendix 3", "number": f"Figure S{n}", "title": title})
    d.save(MA / "Multimedia_Appendix_3_R1_v3.docx")
    (MA / "Multimedia_Appendix_3_R1_v3.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    return rows


def main():
    rows = [{"unit_id": u, "appendix": "Multimedia Appendix 1", "number": f"Note {i}", "title": ""} for u, i in NN.items()]
    rows += build_tables() + build_figures()
    with open(MA / "ma_numbering_map_v3.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["unit_id", "appendix", "number", "title"])
        w.writeheader(); w.writerows(rows)
    for fn in ("Multimedia_Appendix_2_R1_v3.md", "Multimedia_Appendix_3_R1_v3.md"):
        assert "{{" not in (MA / fn).read_text(), fn
    print(f"MA2 {len(O['ma2_tables'])} tables; MA3 {len(O['ma3_figures'])} figures")


if __name__ == "__main__":
    main()
