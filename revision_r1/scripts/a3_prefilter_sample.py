"""A3 · Prefilter-audit sample, key, manifest and blinded workbook (D1, X2).

Written and frozen before A2 results exist; run after A2 `finalize`.

Strata (years 2021–2025 only; year = first 20xx in pub_date, as the production
prefilter's pub_year):
  EX-F  production = application, full-abstract = discourse|evaluative  15/year
  EX-S  production = application, full-abstract = application          45/year
  RET   production = discourse|evaluative (retained)                    10/year
  PILOT records from the 200-record prefilter pilot (any year)            20
Rules: pilot PMIDs are excluded from EX-F/EX-S/RET; records whose
full-abstract label is FAILED enter no frame; a stratum-year below target is
taken in full. Sampling: numpy default_rng(42); for stratum in (EX-F, EX-S,
RET), for year 2021..2025: frame sorted by integer PMID,
rng.choice(n, min(target, n), replace=False); then PILOT: pilot sorted by
integer PMID, rng.choice(200, 20, replace=False); then row order =
rng.permutation(370) → row_id.
Outputs (revision_r1/coding/):
  prefilter_sampling_manifest.csv, prefilter_key.csv, prefilter_audit_TEMPLATE.xlsx
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment
from openpyxl.worksheet.datavalidation import DataValidation

from r1_coding import (CODING, YELLOW, block_between, last_commit, read_system_prompt, sha256,
                       show_text, style_header, write_readme)
from r1_common import DATA_ROOT, OUT, SEED, read_str

SRC = "prefilter_batch.py"
YEARS = [2021, 2022, 2023, 2024, 2025]
TARGETS = {"EX-F": 15, "EX-S": 45, "RET": 10}
N_PILOT = 20
KEEP = {"discourse", "evaluative"}


def main():
    prompt = read_system_prompt(SRC)
    rules = block_between(prompt, "You are classifying", "\n\nReturn ONLY valid JSON")
    assert "When in doubt, classify as application." in rules
    commit = last_commit(SRC)

    lab = read_str(OUT / "A2" / "a2_fullabstract_labels.csv")
    corpus = read_str(DATA_ROOT / "filtered_medical_all_Q1Q2.csv").set_index("pmid")
    pilot = read_str(DATA_ROOT / "pilot_200_full_haiku.csv")
    pilot_ids = set(pilot["pmid"])
    assert len(lab) == len(corpus) == 97492
    lab["year_i"] = pd.to_numeric(lab["year"], errors="coerce")
    n_failed = int((lab["label_fullabstract"] == "FAILED").sum())
    n_failed_window = int(((lab["label_fullabstract"] == "FAILED") & lab["year_i"].isin(YEARS)).sum())
    ok = lab[(lab["label_fullabstract"] != "FAILED") & lab["year_i"].isin(YEARS) & ~lab["pmid"].isin(pilot_ids)].copy()
    ok["stratum"] = np.select(
        [(ok.label_production == "application") & ok.label_fullabstract.isin(KEEP),
         (ok.label_production == "application") & (ok.label_fullabstract == "application"),
         ok.label_production.isin(KEEP)],
        ["EX-F", "EX-S", "RET"], default="")
    assert (ok["stratum"] != "").all()
    ok["pmid_i"] = ok["pmid"].astype(int)

    rng = np.random.default_rng(SEED)
    picks, man = [], []
    for st, target in TARGETS.items():
        for y in YEARS:
            f = ok[(ok.stratum == st) & (ok.year_i == y)].sort_values("pmid_i").reset_index(drop=True)
            k = min(target, len(f))
            idx = rng.choice(len(f), k, replace=False) if k else np.array([], int)
            picks.append(f.iloc[np.sort(idx)])
            man.append({"stratum": st, "year": y, "frame_n": len(f), "target": target, "sample_n": k,
                        "sampling_fraction": k / len(f) if len(f) else np.nan, "below_target": k < target})
    pl = pilot.assign(pmid_i=pilot["pmid"].astype(int)).sort_values("pmid_i").reset_index(drop=True)
    pidx = rng.choice(len(pl), N_PILOT, replace=False)
    pls = pl.iloc[np.sort(pidx)]
    lab_idx = lab.set_index("pmid")
    pls = pd.DataFrame({"pmid": pls["pmid"], "year_i": pd.to_numeric(pls["year"]), "stratum": "PILOT",
                        "label_production": pls["pmid"].map(lab_idx["label_production"]),
                        "label_fullabstract": pls["pmid"].map(lab_idx["label_fullabstract"]),
                        "pilot_my_label": pls["my_label"].str.strip().str.lower()})
    man.append({"stratum": "PILOT", "year": "any", "frame_n": len(pl), "target": N_PILOT, "sample_n": N_PILOT,
                "sampling_fraction": N_PILOT / len(pl), "below_target": False})
    sample = pd.concat(picks + [pls], ignore_index=True)
    order = rng.permutation(len(sample))
    sample = sample.iloc[order].reset_index(drop=True)
    sample["row_id"] = np.arange(1, len(sample) + 1)

    man = pd.DataFrame(man)
    man.to_csv(CODING / "prefilter_sampling_manifest.csv", index=False)
    (CODING / "prefilter_sampling_notes.txt").write_text(
        f"FAILED full-abstract labels (all years): {n_failed}; within 2021-2025: {n_failed_window}. "
        f"These enter no frame.\nPilot PMIDs excluded from EX-F/EX-S/RET frames: {len(pilot_ids)}.\n")
    key = pd.DataFrame({"row_id": sample["row_id"], "pmid": sample["pmid"],
                        "year": sample["year_i"].astype(int),
                        "journal": sample["pmid"].map(corpus["journal"]), "stratum": sample["stratum"],
                        "label_production": sample["label_production"],
                        "label_fullabstract": sample["label_fullabstract"],
                        "pilot_my_label": sample.get("pilot_my_label", pd.Series(index=sample.index)).fillna("")})
    key.to_csv(CODING / "prefilter_key.csv", index=False)

    wb = Workbook()
    rd = wb.active
    rd.title = "Read me first"
    write_readme(rd, "Prefilter audit — coding instructions", [
        ("1. Categories and rules (verbatim from the production prefilter's SYSTEM_PROMPT)",
         f"Source: {SRC}, commit {commit}; SHA-256 of the full SYSTEM_PROMPT: {sha256(prompt)}\n\n" + rules),
        ("2. How to fill the sheet",
         "• Read the title and the full abstract.\n"
         "• Choose human_label from the drop-down: discourse, evaluative, or application.\n"
         "• Code each paper independently, and do not look papers up.\n"
         "• Use 'borderline' (Y) and 'notes' for uncertainty: mark Y when you were torn, or when you applied "
         "the \"when in doubt\" rule.\n"
         "• Save the finished file as prefilter_audit_COMPLETED.xlsx (do not overwrite the template)."),
        ("3. Note",
         "The production classifier saw only the title and the first 300 characters of the abstract; you read "
         "the full abstract. This is intended."),
    ])
    ws = wb.create_sheet("Coding")
    cols = ["row_id", "title", "abstract", "human_label", "borderline", "notes"]
    ws.append(cols)
    for r in sample.itertuples():
        ws.append([int(r.row_id), corpus.at[r.pmid, "title"], show_text(corpus.at[r.pmid, "abstract"]), None, None, None])
    n = len(sample)
    for i in range(2, n + 2):
        for c in ("D", "E", "F"):
            ws[f"{c}{i}"].fill = YELLOW
        for c in ("B", "C"):
            ws[f"{c}{i}"].alignment = Alignment(wrap_text=True, vertical="top")
    dv1 = DataValidation(type="list", formula1='"discourse,evaluative,application"', allow_blank=True,
                         error="Choose discourse, evaluative, or application.", errorTitle="Invalid label")
    dv2 = DataValidation(type="list", formula1='"Y"', allow_blank=True, error="Y or blank.", errorTitle="Y or blank")
    ws.add_data_validation(dv1); ws.add_data_validation(dv2)
    dv1.add(f"D2:D{n + 1}"); dv2.add(f"E2:E{n + 1}")
    style_header(ws, len(cols))
    for col, w in {"A": 7, "B": 50, "C": 110, "D": 14, "E": 11, "F": 35}.items():
        ws.column_dimensions[col].width = w
    out = CODING / "prefilter_audit_TEMPLATE.xlsx"
    wb.save(out)

    chk = load_workbook(out)
    assert chk.sheetnames == ["Read me first", "Coding"]
    assert all(s.sheet_state == "visible" for s in chk.worksheets)
    blob = " ".join(str(c.value) for s in chk.worksheets for row in s.iter_rows() for c in row if c.value is not None)
    assert not [p for p in sample["pmid"] if p in blob], "PMID found in workbook"
    print(man.to_string(index=False))
    print(f"FAILED (all years) {n_failed}; within 2021-2025 {n_failed_window}; rows {n}")


if __name__ == "__main__":
    main()
