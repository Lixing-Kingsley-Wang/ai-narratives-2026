#!/usr/bin/env python3
"""
Build the Phase 2 human ADJUDICATION workbook (.xlsx) from phase2_prophecy_verdicts_worksheet.csv.

Layout (repo house style): GREY/locked = machine evidence + context (read-only); YELLOW = your verdict
columns, with dropdowns on verdict / external_evidence_used / ambiguous_flag. Claim, neutral summary,
and key evidence sit immediately left of the verdict cells so you read then adjudicate in place.
corpus_silent rows are tinted so the "silence => too_early" default is obvious. The model assigned NO
verdict; you fill them. Iron rule: not_borne_out REQUIRES positive contrary evidence; silence => too_early.
"""
import os, csv, sys
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils import get_column_letter

csv.field_size_limit(sys.maxsize)
OUT_DIR = "/Users/kingslywang/repos/ai-narratives-2026/output/analyses/prophecy"
CSV_IN  = os.path.join(OUT_DIR, "phase2_prophecy_verdicts_worksheet.csv")
XLSX    = os.path.join(OUT_DIR, "phase2_prophecy_verdicts_worksheet.xlsx")

HDR = PatternFill("solid", fgColor="305496")
GRY = PatternFill("solid", fgColor="E7E6E6")
YEL = PatternFill("solid", fgColor="FFF2CC")
ORG = PatternFill("solid", fgColor="FCE4D6")   # corpus_silent tint
HF  = Font(color="FFFFFF", bold=True, size=10)
LK  = Font(size=10)
WRAP = Alignment(wrap_text=True, vertical="top")
TOP  = Alignment(vertical="top")
THIN = Side(style="thin", color="BFBFBF")
BORD = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)

# (csv_key or None, header, width, kind)  kind: ref | silent | claim | wrapref | verdict | evpmid | ext | amb | note
COLS = [
    ("claim_id",              "claim_id",              11, "ref"),
    ("pmid",                  "pmid",                  11, "ref"),
    ("tier",                  "tier",                   6, "ref"),
    ("corpus_silent",         "corpus_silent",         12, "silent"),
    ("signature_claim",       "signature_claim",       52, "claim"),
    ("evidence_status_summary","evidence_status_summary",68, "wrapref"),
    ("key_evidence",          "key_evidence",          58, "wrapref"),
    (None,                    "verdict",               22, "verdict"),
    (None,                    "verdict_evidence_pmid", 16, "evpmid"),
    (None,                    "external_evidence_used",16, "ext"),
    (None,                    "ambiguous_flag",        12, "amb"),
    (None,                    "adjudicator_note",      34, "note"),
    ("claim_role",            "claim_role",            10, "ref"),
    ("pub_year",              "pub_year",               9, "ref"),
    ("topic",                 "topic",                 22, "ref"),
    ("horizon",               "horizon",               13, "ref"),
    ("top_score",             "top_score",              9, "ref"),
    ("low_similarity",        "low_similarity",        12, "ref"),
    ("retrieved_pmids_top20", "retrieved_pmids_top20", 40, "wrapref"),
]
YELLOW = {"verdict", "evpmid", "ext", "amb", "note"}


def main():
    rows = list(csv.DictReader(open(CSV_IN, encoding="utf-8")))
    wb = Workbook(); s = wb.active; s.title = "adjudicate"

    for j, (_, hdr, w, _) in enumerate(COLS, start=1):
        c = s.cell(1, j, hdr); c.fill = HDR; c.font = HF; c.border = BORD
        c.alignment = Alignment(wrap_text=True, vertical="center")
        s.column_dimensions[get_column_letter(j)].width = w
    s.row_dimensions[1].height = 28

    for i, r in enumerate(rows, start=2):
        silent = r.get("corpus_silent", "") == "TRUE"
        for j, (key, hdr, w, kind) in enumerate(COLS, start=1):
            val = "" if key is None else r.get(key, "")
            c = s.cell(i, j, val); c.border = BORD
            if kind in YELLOW:
                c.fill = YEL; c.font = LK
                c.alignment = WRAP if kind == "note" else TOP
            elif kind == "silent":
                c.fill = ORG if silent else GRY; c.font = LK; c.alignment = TOP
            else:
                c.fill = GRY; c.font = LK
                c.alignment = WRAP if kind in ("claim", "wrapref") else TOP
        s.row_dimensions[i].height = 118

    n = len(rows) + 1
    L = {hdr: get_column_letter(j) for j, (_, hdr, _, _) in enumerate(COLS, start=1)}

    def dv(items, col):
        d = DataValidation(type="list", formula1='"%s"' % ",".join(items), allow_blank=True)
        s.add_data_validation(d); d.add(f"{col}2:{col}{n}")

    dv(["borne_out", "partially", "not_borne_out", "too_early_unfalsifiable"], L["verdict"])
    dv(["none", "source"], L["external_evidence_used"])
    dv(["Y", "N"], L["ambiguous_flag"])

    s.freeze_panes = "C2"
    s.auto_filter.ref = f"A1:{get_column_letter(len(COLS))}{n}"

    rd = wb.create_sheet("README")
    rd.column_dimensions["A"].width = 112
    notes = [
        "PHASE 2 ADJUDICATION — Prophecy Panel. The model assigned NO verdict; you fill the YELLOW columns.",
        "",
        "Read (grey): signature_claim -> evidence_status_summary (neutral, from retrieved 2024-2026 abstracts only)",
        "-> key_evidence (up to 5 'PMID - finding [outcome|restatement]'). Continued advocacy = restatement, not outcome.",
        "corpus_silent=TRUE rows are tinted orange.",
        "",
        "Fill (yellow), per rubric A4:",
        "  verdict {borne_out | partially | not_borne_out | too_early_unfalsifiable}",
        "     borne_out      = positive evidence the predicted outcome materialized substantially as claimed",
        "     partially      = right direction but narrower/weaker/slower (e.g. piloted, not routine)",
        "     not_borne_out  = POSITIVE CONTRARY evidence the outcome did not materialize  (REQUIRED — see iron rule)",
        "     too_early_unfalsifiable = horizon not reached, OR too vague to test, OR corpus silent (no evidence either way)",
        "  verdict_evidence_pmid  = the specific PMID backing your verdict (>=1 per A7)",
        "  external_evidence_used {none | source} = 'source' only if you used one cited external datum (A5 hard-fact claims)",
        "  ambiguous_flag {Y | N} = mark Y on partially & too_early calls for Dan's blind spot-check (A7)",
        "  adjudicator_note = free-text rationale",
        "",
        "IRON RULE (A4): corpus silence maps to too_early_unfalsifiable, NEVER to not_borne_out.",
        "Only POSITIVE CONTRARY evidence yields not_borne_out. Absence of evidence is not failure.",
        "Default for corpus_silent / open-ended no-deadline claims: too_early_unfalsifiable unless positive evidence exists.",
        "",
        "Stance-blind: adjudicate on the evidence, not on the fact that these were Advocacy papers.",
        "When done, save the file and tell Claude — it will read verdicts back for the tier->verdict Sankey (A8).",
    ]
    for i, t in enumerate(notes, start=1):
        c = rd.cell(i, 1, t); c.alignment = Alignment(wrap_text=True, vertical="top")
        if i == 1:
            c.font = Font(bold=True, size=12)

    wb.save(XLSX)
    silent = sum(1 for r in rows if r.get("corpus_silent") == "TRUE")
    print(f"Wrote {XLSX}")
    print(f"  claims={len(rows)}  corpus_silent(tinted)={silent}  verdict cells blank for human")


if __name__ == "__main__":
    main()
