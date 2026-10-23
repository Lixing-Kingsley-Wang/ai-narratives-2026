"""A1 · Theme-validation sample, key, manifest and blinded workbook (D2a).

Frame: critical (Alarm or Caution) records dated 2021–2025 that carry a theme
label in output/analysis/thematic_alarm.csv (title-only records included).
Sample: 40 per year, simple random within year, numpy default_rng(42):
  for year in 2021..2025 (ascending): frame sorted by integer PMID,
  idx = rng.choice(n_year, 40, replace=False); then row order =
  rng.permutation(200) → row_id 1..200.
Outputs (revision_r1/coding/):
  theme_sampling_manifest.csv, theme_key.csv, theme_validation_TEMPLATE.xlsx
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from openpyxl import Workbook
from openpyxl.formatting.rule import FormulaRule
from openpyxl.styles import Alignment, PatternFill
from openpyxl.worksheet.datavalidation import DataValidation

from r1_coding import (CODING, YELLOW, block_between, last_commit, read_system_prompt, sha256,
                       show_text, style_header, write_readme)
from r1_common import REPO_OUT, SEED

SRC = "classify_themes_batch.py"
YEARS = [2021, 2022, 2023, 2024, 2025]
PER_YEAR = 40
# Column order = order in which the classifier prompt lists the themes.
THEME_ORDER = ["replacement", "hallucination", "safety_clinical", "ethics_bias", "cognitive",
               "education", "regulation", "existential", "data_privacy", "other"]


def main():
    prompt = read_system_prompt(SRC)
    theme_block = block_between(prompt, "Identify concern themes", "\n\nReturn ONLY valid JSON")
    listed = [ln.split(":", 1)[0].lstrip("- ").strip() for ln in theme_block.split("THEMES (return 1-3 most prominent):\n", 1)[1].split("\n")]
    assert listed == THEME_ORDER, f"theme order in prompt changed: {listed}"
    commit = last_commit(SRC)

    th = pd.read_csv(REPO_OUT / "analysis/thematic_alarm.csv", dtype=str, keep_default_na=False)
    th["year"] = pd.to_numeric(th["pub_year"], errors="coerce")
    frame = th[th["year"].isin(YEARS) & th["stance"].isin(["Alarm", "Caution"]) & (th["themes"].str.strip() != "")].copy()
    frame["pmid_i"] = frame["pmid"].astype(int)

    rng = np.random.default_rng(SEED)
    picks, man = [], []
    for y in YEARS:
        fy = frame[frame["year"] == y].sort_values("pmid_i").reset_index(drop=True)
        n = len(fy)
        k = min(PER_YEAR, n)
        idx = rng.choice(n, k, replace=False)
        picks.append(fy.iloc[np.sort(idx)])
        man.append({"year": y, "frame_n": n, "sample_n": k, "sampling_fraction": k / n,
                    "frame_title_only": int((fy["abstract"].str.strip() == "").sum())})
    sample = pd.concat(picks, ignore_index=True)
    order = rng.permutation(len(sample))
    sample = sample.iloc[order].reset_index(drop=True)
    sample["row_id"] = np.arange(1, len(sample) + 1)

    man = pd.DataFrame(man)
    man.loc[len(man)] = {"year": "All", "frame_n": int(man.frame_n.sum()), "sample_n": int(man.sample_n.sum()),
                         "sampling_fraction": man.sample_n.sum() / man.frame_n.sum(),
                         "frame_title_only": int(man.frame_title_only.sum())}
    man.to_csv(CODING / "theme_sampling_manifest.csv", index=False)

    key = pd.DataFrame({"row_id": sample["row_id"], "pmid": sample["pmid"], "year": sample["year"].astype(int),
                        "journal": sample["journal"], "stance": sample["stance"],
                        "model_themes": sample["themes"],
                        "abstract_present": (sample["abstract"].str.strip() != "").astype(int)})
    key.to_csv(CODING / "theme_key.csv", index=False)

    # ---- workbook ---------------------------------------------------------
    wb = Workbook()
    rd = wb.active
    rd.title = "Read me first"
    write_readme(rd, "Theme validation — coding instructions", [
        ("1. Task",
         "Every paper on the Coding tab was classified as critical toward AI (Alarm or Caution). "
         "Read the title and the full abstract. Tick the 1 to 3 most prominent concern themes."),
        ("2. Theme list (verbatim from the classifier's SYSTEM_PROMPT)",
         f"Source: {SRC}, commit {commit}; SHA-256 of the full SYSTEM_PROMPT: {sha256(prompt)}\n\n" + theme_block),
        ("3. How to fill the sheet",
         "• Tick a theme by typing 1 in its column; leave other theme cells blank.\n"
         "• Tick at least 1 and at most 3 themes. The n_themes cell turns red unless the count is 1, 2 or 3.\n"
         "• Use 'other' only when no listed theme fits.\n"
         "• Code each paper independently, and do not look papers up.\n"
         "• Write any ambiguity in 'notes' rather than inventing a rule.\n"
         "• Save the finished file as theme_validation_COMPLETED.xlsx (do not overwrite the template)."),
        ("4. Note",
         "The classifier saw only the title and the first 400 characters of the abstract; you read the full "
         "abstract. This is intended."),
    ])
    ws = wb.create_sheet("Coding")
    cols = ["row_id", "title", "abstract"] + THEME_ORDER + ["n_themes", "notes"]
    ws.append(cols)
    for r in sample.itertuples():
        ws.append([int(r.row_id), r.title, show_text(r.abstract)] + [None] * len(THEME_ORDER) + [None, None])
    n = len(sample)
    first_t, last_t = "D", chr(ord("D") + len(THEME_ORDER) - 1)  # D..M
    ncol = chr(ord(last_t) + 1)                                   # N
    notes_col = chr(ord(ncol) + 1)                                # O
    for i in range(2, n + 2):
        ws[f"{ncol}{i}"] = f"=COUNTA({first_t}{i}:{last_t}{i})"
        for c in range(4, 4 + len(THEME_ORDER)):
            ws.cell(row=i, column=c).fill = YELLOW
        ws[f"{notes_col}{i}"].fill = YELLOW
        for c in ("B", "C"):
            ws[f"{c}{i}"].alignment = Alignment(wrap_text=True, vertical="top")
    dv = DataValidation(type="list", formula1='"1"', allow_blank=True,
                        error="Type 1 to tick a theme, or leave the cell blank.", errorTitle="1 or blank")
    ws.add_data_validation(dv)
    dv.add(f"{first_t}2:{last_t}{n + 1}")
    ws.conditional_formatting.add(f"{ncol}2:{ncol}{n + 1}", FormulaRule(
        formula=[f"OR({ncol}2<1,{ncol}2>3)"], fill=PatternFill("solid", fgColor="FF9999")))
    style_header(ws, len(cols))
    for col, w in {"A": 7, "B": 45, "C": 100, ncol: 9, notes_col: 35}.items():
        ws.column_dimensions[col].width = w
    for c in range(4, 4 + len(THEME_ORDER)):
        ws.column_dimensions[ws.cell(row=1, column=c).column_letter].width = 11
    out = CODING / "theme_validation_TEMPLATE.xlsx"
    wb.save(out)

    # blinding self-check: workbook holds only row_id/title/abstract + empty inputs
    from openpyxl import load_workbook
    chk = load_workbook(out)
    assert chk.sheetnames == ["Read me first", "Coding"]
    assert all(s.sheet_state == "visible" for s in chk.worksheets)
    blob = " ".join(str(c.value) for s in chk.worksheets for row in s.iter_rows() for c in row if c.value is not None)
    leaks = [p for p in sample["pmid"] if p in blob]
    assert not leaks, "PMID found in workbook"
    print(man.to_string(index=False))
    print(f"commit {commit}; prompt sha256 {sha256(prompt)[:12]}…; title-only in sample: "
          f"{int(key.abstract_present.eq(0).sum())}")


if __name__ == "__main__":
    main()
