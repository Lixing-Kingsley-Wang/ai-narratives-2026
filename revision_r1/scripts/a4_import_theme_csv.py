"""Import the coder's completed theme sheet (exported from Numbers as CSV) into
the workbook format the frozen scorer reads.

The source CSV is copied unchanged into revision_r1/coding/completed/ (its
SHA-256 is logged); the ticks and notes are written into a copy of the
template's Coding sheet, matched by row_id, after checking that every title and
abstract is identical to the template (whitespace-normalised).

Usage: python a4_import_theme_csv.py "<Coding-Table 1.csv>" ["<Read me first-Table 1.csv>"]
"""

import hashlib
import shutil
import sys

import pandas as pd
from openpyxl import load_workbook

from r1_coding import CODING

THEMES = ["replacement", "hallucination", "safety_clinical", "ethics_bias", "cognitive",
          "education", "regulation", "existential", "data_privacy", "other"]


def main():
    src = sys.argv[1]
    dst_dir = CODING / "completed"
    dst_dir.mkdir(exist_ok=True)
    log = []
    for p in sys.argv[1:]:
        h = hashlib.sha256(open(p, "rb").read()).hexdigest()
        tgt = dst_dir / ("theme_" + p.rsplit("/", 1)[-1].replace(" ", "_"))
        shutil.copyfile(p, tgt)
        log.append(f"{tgt.name}\tsha256 {h}\tsource {p}")

    d = pd.read_csv(src, dtype=str, keep_default_na=False, encoding="utf-8-sig")
    d["row_id"] = d["row_id"].astype(int)
    assert sorted(d["row_id"]) == list(range(1, 201)), "row_ids are not 1..200"
    bad = {t: sorted(set(d[t]) - {"", "1"}) for t in THEMES if set(d[t]) - {"", "1"}}
    assert not bad, f"unexpected tick values: {bad}"

    wb = load_workbook(CODING / "theme_validation_TEMPLATE.xlsx")
    ws = wb["Coding"]
    hdr = [c.value for c in ws[1]]
    norm = lambda s: " ".join(str(s).split())
    by_id = d.set_index("row_id")
    for r in range(2, ws.max_row + 1):
        rid = int(ws.cell(row=r, column=1).value)
        rec = by_id.loc[rid]
        assert norm(ws.cell(row=r, column=hdr.index("title") + 1).value) == norm(rec["title"]), f"title mismatch row_id {rid}"
        assert norm(ws.cell(row=r, column=hdr.index("abstract") + 1).value) == norm(rec["abstract"]), f"abstract mismatch row_id {rid}"
        for t in THEMES:
            ws.cell(row=r, column=hdr.index(t) + 1, value=1 if rec[t] == "1" else None)
        ws.cell(row=r, column=hdr.index("notes") + 1, value=rec["notes"] or None)
    out = dst_dir / "theme_validation_COMPLETED.xlsx"
    wb.save(out)
    log.append(f"{out.name}\tbuilt from template + CSV ticks/notes; 200/200 titles and abstracts identical to template")
    (dst_dir / "theme_import_log.txt").write_text("\n".join(log) + "\n")
    print("\n".join(log))


if __name__ == "__main__":
    main()
