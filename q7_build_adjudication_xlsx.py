"""Build the adjudication workbook for the 46 validation disagreements.

For each row where your blind code differs from the classifier on at least one
axis, show title + abstract + the model's rationale, your label, and the model's
label side by side, with a drop-down for your FINAL call. Only the contested
cells are left blank (yellow); agreed axes are pre-filled and greyed so you only
decide what's actually in dispute.

After you fill it, q7_kappa.py --adjudicated re-scores κ with the final labels.
"""
import os
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils import get_column_letter

BASE = os.path.dirname(os.path.abspath(__file__))
DIS  = os.path.join(BASE, "output", "analyses", "q7_validation_disagreements.csv")
AC   = os.path.join(BASE, "output", "analyses", "q7_classified_ac.csv")
SRC  = os.path.join(BASE, "output", "classified_medical_Q1Q2.csv")
OUT  = os.path.join(BASE, "output", "analyses", "q7_adjudication.xlsx")

FM = ["confabulation", "misclassification", "both", "none_or_unclear"]
MT = ["generative", "discriminative", "both", "unclear"]
FONT = "Arial"
HDR  = PatternFill("solid", fgColor="305496")
YEL  = PatternFill("solid", fgColor="FFF2CC")   # fill me
GRY  = PatternFill("solid", fgColor="E7E6E6")    # agreed → locked
DIFF = PatternFill("solid", fgColor="FCE4D6")    # contested context
THIN = Side(style="thin", color="BFBFBF")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)

dis = pd.read_csv(DIS, dtype={"pmid": str})
rat = pd.read_csv(AC, dtype={"pmid": str})[["pmid", "rationale"]]
src = pd.read_csv(SRC, dtype={"pmid": str})[["pmid", "title", "abstract"]]
df = dis.merge(rat, on="pmid", how="left").merge(src, on="pmid", how="left")
df = df.sort_values(["pub_year", "pmid"]).reset_index(drop=True)

wb = Workbook()
s = wb.active
s.title = "Adjudicate"
s.sheet_view.showGridLines = False

headers = ["row", "pmid", "pub_year", "title", "abstract",
           "your_failure_mode", "model_failure_mode", "model_rationale",
           "FINAL_failure_mode",
           "your_model_type", "model_model_type", "FINAL_model_type", "notes"]
widths  = [5, 10, 8, 38, 80, 18, 18, 46, 18, 16, 16, 16, 24]
for j, (h, w) in enumerate(zip(headers, widths), start=1):
    c = s.cell(row=1, column=j, value=h)
    c.font = Font(name=FONT, bold=True, color="FFFFFF", size=10)
    c.fill = HDR
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    c.border = BORDER
    s.column_dimensions[get_column_letter(j)].width = w

dv_fm = DataValidation(type="list", formula1='"%s"' % ",".join(FM), allow_blank=True)
dv_fm.error = "Pick one: " + ", ".join(FM); dv_fm.errorTitle = "Invalid"
dv_mt = DataValidation(type="list", formula1='"%s"' % ",".join(MT), allow_blank=True)
dv_mt.error = "Pick one: " + ", ".join(MT); dv_mt.errorTitle = "Invalid"
s.add_data_validation(dv_fm); s.add_data_validation(dv_mt)

n_fm_contested = n_mt_contested = 0
for i, rec in enumerate(df.itertuples(index=False), start=2):
    fm_diff = rec.human_failure_mode != rec.failure_mode
    mt_diff = rec.human_model_type   != rec.model_type
    n_fm_contested += int(fm_diff); n_mt_contested += int(mt_diff)
    vals = [i - 1, rec.pmid, rec.pub_year, rec.title, rec.abstract,
            rec.human_failure_mode, rec.failure_mode, rec.rationale,
            "" if fm_diff else rec.human_failure_mode,
            rec.human_model_type, rec.model_type,
            "" if mt_diff else rec.human_model_type, ""]
    for j, v in enumerate(vals, start=1):
        c = s.cell(row=i, column=j, value=v)
        c.font = Font(name=FONT, size=10)
        c.alignment = Alignment(vertical="top",
                                wrap_text=(j in (4, 5, 8, 13)),
                                horizontal="center" if j in (1, 3, 6, 7, 9, 10, 11, 12) else "left")
        c.border = BORDER
    # colour the contested axis context + final cells
    if fm_diff:
        s.cell(i, 6).fill = DIFF; s.cell(i, 7).fill = DIFF; s.cell(i, 9).fill = YEL
    else:
        s.cell(i, 9).fill = GRY
    if mt_diff:
        s.cell(i, 10).fill = DIFF; s.cell(i, 11).fill = DIFF; s.cell(i, 12).fill = YEL
    else:
        s.cell(i, 12).fill = GRY
    dv_fm.add(f"I{i}"); dv_mt.add(f"L{i}")
    s.row_dimensions[i].height = 150

s.freeze_panes = "A2"
s.auto_filter.ref = f"A1:M{len(df)+1}"

# instructions sheet
g = wb.create_sheet("Read me first", 0)
g.sheet_view.showGridLines = False
g.column_dimensions["A"].width = 100
notes = [
    ("Adjudication — resolve the validation disagreements", True, 14, "305496"),
    ("", False, 11, "000000"),
    ("These are the %d papers (of 120) where your blind code differed from the classifier on at "
     "least one axis. Fill ONLY the yellow cells:" % len(df), False, 11, "000000"),
    ("  • FINAL_failure_mode (col I) — yellow where failure_mode is contested (%d rows)" % n_fm_contested, False, 11, "000000"),
    ("  • FINAL_model_type (col L) — yellow where model_type is contested (%d rows)" % n_mt_contested, False, 11, "000000"),
    ("Greyed cells are axes you and the model already agreed on — leave them.", False, 11, "000000"),
    ("", False, 11, "000000"),
    ("For each contested cell: read the abstract and the model's rationale (col H), then choose your "
     "FINAL judgment from the drop-down. You may keep your original call or switch to the model's — "
     "the rationale is there to help you decide, not to push you. This is a considered second pass, "
     "so resolve genuinely (don't just rubber-stamp either side).", False, 11, "000000"),
    ("", False, 11, "000000"),
    ("failure_mode: confabulation = AI made something up · misclassification = AI got a label/score "
     "wrong · both · none_or_unclear = no mechanism described.", False, 11, "000000"),
    ("model_type: generative (LLM/chatbot/generator) · discriminative (classifier/detector/risk) · "
     "both · unclear.", False, 11, "000000"),
    ("", False, 11, "000000"),
    ("When done, save (keep .xlsx, same name) and tell me — I re-run κ with your FINAL labels.", True, 11, "C00000"),
]
for r, (txt, bold, size, color) in enumerate(notes, start=1):
    c = g.cell(row=r, column=1, value=txt)
    c.font = Font(name=FONT, bold=bold, size=size, color=color)
    c.alignment = Alignment(vertical="top", wrap_text=True)
    g.row_dimensions[r].height = 34

wb.save(OUT)
print(f"Saved → {OUT}")
print(f"  rows: {len(df)} disagreements")
print(f"  contested failure_mode cells (yellow, col I): {n_fm_contested}")
print(f"  contested model_type   cells (yellow, col L): {n_mt_contested}")
print(f"  total cells to adjudicate: {n_fm_contested + n_mt_contested}")
