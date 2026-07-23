#!/usr/bin/env python3
"""
Build the Phase 1 human-review WORKBOOK (.xlsx) from phase1_signature_claims_for_review.csv.

CSV can't carry data-validation dropdowns, so the reviewer works in this xlsx. Layout
(matching the repo's q7 review-sheet house style):
  - GREY, locked  = machine pre-pass + context (read-only reference; preserves flag-precision audit)
  - YELLOW, edit  = reviewer columns; dropdowns on keep / flag_confirmed / tier
Pre-filled with the machine values so review = confirm-or-correct, not type-from-scratch.
False positives are pre-marked keep=delete; override any cell freely.

When the reviewer is done, prophecy_phase1_freeze_from_xlsx.py converts this back to
phase1_signature_claims_FROZEN.csv (kept rows only) for Phase 2.
"""
import os, csv
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils import get_column_letter

OUT_DIR = "/Users/kingslywang/repos/ai-narratives-2026/output/analyses/prophecy"
CSV_IN  = os.path.join(OUT_DIR, "phase1_signature_claims_for_review.csv")
CAND_IN = os.path.join(OUT_DIR, "prophecy_panel_candidates_2021_2023.csv")  # source title+abstract
XLSX    = os.path.join(OUT_DIR, "phase1_signature_claims_for_review.xlsx")

HDR  = PatternFill("solid", fgColor="305496")   # dark blue header
GRY  = PatternFill("solid", fgColor="E7E6E6")   # locked reference
YEL  = PatternFill("solid", fgColor="FFF2CC")   # reviewer: fill / confirm me
HDRF = Font(color="FFFFFF", bold=True, size=10)
WRAP = Alignment(wrap_text=True, vertical="top")
TOP  = Alignment(vertical="top")
THIN = Side(style="thin", color="BFBFBF")
BORD = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
LOCK = Font(size=10)

# (key_in_csv_or_None, header, width, kind)  kind: ref | keep | flag | claim | tier | text
COLS = [
    ("pmid",              "pmid",              11, "ref"),
    ("pub_year",          "pub_year",           9, "ref"),
    ("journal",           "journal",           22, "ref"),
    ("specialty",         "specialty",         16, "ref"),
    ("has_abstract",      "has_abstract",       9, "ref"),
    ("title",             "title",             46, "ref"),
    ("__abstract__",      "abstract",          80, "abstract"),
    ("flag_confirmed",    "machine_flag",       9, "ref"),
    ("tier",              "machine_tier",       7, "ref"),
    ("flag_reason",       "flag_reason",       50, "ref"),
    (None,                "keep?",              9, "keep"),
    ("flag_confirmed",    "flag_confirmed",    11, "flag"),
    ("signature_claim",   "signature_claim",   62, "claim"),
    ("signature_claim_2", "signature_claim_2", 34, "claim"),
    ("tier",              "tier",               7, "tier"),
    ("topic",             "topic",             22, "text"),
    ("horizon",           "horizon",           14, "text"),
    (None,                "reviewer_note",     30, "text"),
]

def main():
    rows = list(csv.DictReader(open(CSV_IN, encoding="utf-8")))
    abstr = {r["pmid"]: (r.get("abstract") or "").strip()
             for r in csv.DictReader(open(CAND_IN, encoding="utf-8"))}
    wb = Workbook()
    s = wb.active
    s.title = "review"

    # header
    for j, (_, hdr, w, _) in enumerate(COLS, start=1):
        c = s.cell(row=1, column=j, value=hdr)
        c.fill = HDR; c.font = HDRF; c.alignment = Alignment(wrap_text=True, vertical="center")
        c.border = BORD
        s.column_dimensions[get_column_letter(j)].width = w
    s.row_dimensions[1].height = 28

    # data
    for i, r in enumerate(rows, start=2):
        mflag = r.get("flag_confirmed", "")
        for j, (key, hdr, w, kind) in enumerate(COLS, start=1):
            if kind == "keep":
                val = "keep" if mflag == "yes" else "delete"
            elif kind == "abstract":
                val = abstr.get(r.get("pmid", ""), "") or "(title-only — no abstract)"
            elif key is None:
                val = ""
            else:
                val = r.get(key, "")
            c = s.cell(row=i, column=j, value=val)
            c.border = BORD
            if kind in ("ref", "abstract"):
                c.fill = GRY; c.font = LOCK
                c.alignment = WRAP if hdr in ("title", "flag_reason", "abstract") else TOP
            else:
                c.fill = YEL; c.font = LOCK
                c.alignment = WRAP if kind == "claim" else TOP

    n = len(rows) + 1  # last data row

    # dropdowns
    def add_dv(items, col_letter):
        dv = DataValidation(type="list", formula1='"%s"' % ",".join(items),
                            allow_blank=True, showDropDown=False)
        s.add_data_validation(dv)
        dv.add(f"{col_letter}2:{col_letter}{n}")

    letters = {hdr: get_column_letter(j) for j, (_, hdr, _, _) in enumerate(COLS, start=1)}
    add_dv(["keep", "delete"], letters["keep?"])
    add_dv(["yes", "no"],      letters["flag_confirmed"])
    add_dv(["1", "2", "3"],    letters["tier"])

    for i in range(2, n + 1):       # taller rows so wrapped abstract/claim are readable
        s.row_dimensions[i].height = 90
    s.freeze_panes = "C2"           # keep pmid + pub_year visible while scrolling right
    s.auto_filter.ref = f"A1:{get_column_letter(len(COLS))}{n}"

    # README sheet
    rd = wb.create_sheet("README")
    rd.column_dimensions["A"].width = 110
    notes = [
        "PHASE 1 REVIEW — Prophecy Panel (human review gate)",
        "",
        "GREY columns = machine pre-pass + context. Read-only reference. 'machine_flag'/'machine_tier'",
        "are kept so flag precision (machine vs your truth) stays auditable — do not edit them.",
        "",
        "YELLOW columns = your decision. Pre-filled with the machine values; confirm or correct:",
        "  • keep?            dropdown {keep, delete}.  False positives are pre-marked 'delete'.",
        "  • flag_confirmed   dropdown {yes, no}.  Does the paper make a specific forward-looking AI claim?",
        "  • signature_claim  edit freely — the single most specific/falsifiable prediction (1 sentence).",
        "  • signature_claim_2 only if the paper makes a 2nd genuinely independent major bet (usually blank).",
        "  • tier             dropdown {1,2,3}. 1=superiority/replacement vs humans, 2=capability deployment,",
        "                     3=diffuse 'revolutionize' (no mechanism/horizon). Any concrete testable element => not 3.",
        "  • topic / horizon  edit freely. horizon = explicit timeframe in the claim, else 'open-ended'.",
        "  • reviewer_note    free text (why you changed something, ambiguity, etc.).",
        "",
        "Tier is by CLAIM STRUCTURE, blind to whether it later came true. Do not consult 2024-2026 evidence here.",
        "",
        "WHEN DONE: just save this .xlsx (keep the filename). Tell Claude 'proceed' and it will generate",
        "phase1_signature_claims_FROZEN.csv from your kept rows (keep?=keep) for Phase 2. No manual row deletion needed.",
    ]
    for i, t in enumerate(notes, start=1):
        c = rd.cell(row=i, column=1, value=t)
        c.alignment = Alignment(wrap_text=True, vertical="top")
        if i == 1:
            c.font = Font(bold=True, size=12)

    wb.save(XLSX)
    print(f"Wrote {XLSX}")
    print(f"  rows={len(rows)}  pre-marked delete={sum(1 for r in rows if r.get('flag_confirmed')!='yes')}")

if __name__ == "__main__":
    main()
