"""Import the coder's completed prefilter-audit sheet into the workbook format
the frozen scorer reads.

The coder returned a Numbers file. A copy of it (never the original) was
exported to CSV with Numbers via AppleScript; this script copies the .numbers
file and the exported CSVs unchanged into revision_r1/coding/completed/
(SHA-256 logged), checks that every title and abstract matches the template
row by row, and writes human_label / borderline / notes into a copy of the
template.

Usage: python a4_import_prefilter_csv.py <original.numbers> <Coding-Table 1.csv> [<Read me first-Table 1.csv>]
"""

import hashlib
import shutil
import sys

import pandas as pd
from openpyxl import load_workbook

from r1_coding import CODING

LABELS = {"", "discourse", "evaluative", "application"}


def main():
    numbers_src, csv_src = sys.argv[1], sys.argv[2]
    dst = CODING / "completed"
    dst.mkdir(exist_ok=True)
    log = []
    for p in sys.argv[1:]:
        h = hashlib.sha256(open(p, "rb").read()).hexdigest()
        tgt = dst / ("prefilter_" + p.rsplit("/", 1)[-1].replace(" ", "_"))
        shutil.copyfile(p, tgt)
        log.append(f"{tgt.name}\tsha256 {h}\tsource {p}")

    d = pd.read_csv(csv_src, dtype=str, keep_default_na=False, encoding="utf-8-sig")
    d["row_id"] = d["row_id"].astype(int)
    assert sorted(d["row_id"]) == list(range(1, 371)), "row_ids are not 1..370"
    d["human_label"] = d["human_label"].str.strip().str.lower()
    d["borderline"] = d["borderline"].str.strip().str.upper()
    assert set(d["human_label"]) <= LABELS, f"unexpected labels: {set(d['human_label']) - LABELS}"
    assert set(d["borderline"]) <= {"", "Y"}, "unexpected borderline values"

    wb = load_workbook(CODING / "prefilter_audit_TEMPLATE.xlsx")
    ws = wb["Coding"]
    hdr = [c.value for c in ws[1]]
    norm = lambda s: " ".join(str(s).split())
    by_id = d.set_index("row_id")
    for r in range(2, ws.max_row + 1):
        rid = int(ws.cell(row=r, column=1).value)
        rec = by_id.loc[rid]
        assert norm(ws.cell(row=r, column=hdr.index("title") + 1).value) == norm(rec["title"]), f"title mismatch {rid}"
        assert norm(ws.cell(row=r, column=hdr.index("abstract") + 1).value) == norm(rec["abstract"]), f"abstract mismatch {rid}"
        ws.cell(row=r, column=hdr.index("human_label") + 1, value=rec["human_label"] or None)
        ws.cell(row=r, column=hdr.index("borderline") + 1, value=rec["borderline"] or None)
        ws.cell(row=r, column=hdr.index("notes") + 1, value=rec["notes"] or None)
    out = dst / "prefilter_audit_COMPLETED.xlsx"
    wb.save(out)
    log.append(f"{out.name}\tbuilt from template + CSV labels; 370/370 titles and abstracts identical to template; "
               f"blank human_label: {int((d.human_label == '').sum())}; borderline=Y: {int((d.borderline == 'Y').sum())}")
    (dst / "prefilter_import_log.txt").write_text("\n".join(log) + "\n")
    print("\n".join(log))


if __name__ == "__main__":
    main()
