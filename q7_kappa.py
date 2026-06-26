"""Part 5 — per-axis Cohen's κ for the Q7 validation set.

Reads the filled blind file (output/analyses/q7_validation_blind.csv) and joins
back to q7_classified_ac.csv on pmid to recover the model labels, then reports
for each axis (failure_mode, model_type): Cohen's κ, raw agreement, and the
confusion matrix. Runs only on rows the human has filled.
"""
import os, sys
import numpy as np
import pandas as pd
from sklearn.metrics import cohen_kappa_score, confusion_matrix

BASE  = os.path.dirname(os.path.abspath(__file__))
XLSX  = os.path.join(BASE, "output", "analyses", "q7_validation_coding.xlsx")
BLIND = os.path.join(BASE, "output", "analyses", "q7_validation_blind.csv")
AC    = os.path.join(BASE, "output", "analyses", "q7_classified_ac.csv")

FM_LABELS = ["confabulation","misclassification","both","none_or_unclear"]
MT_LABELS = ["generative","discriminative","both","unclear"]

def load_coding():
    """Prefer the filled coding workbook (sheet 'Coding'); else the blind CSV."""
    if os.path.exists(XLSX):
        b = pd.read_excel(XLSX, sheet_name="Coding", dtype={"pmid": str})
        print(f"Source: {os.path.basename(XLSX)} (sheet 'Coding')")
        return b
    if os.path.exists(BLIND):
        print(f"Source: {os.path.basename(BLIND)}")
        return pd.read_csv(BLIND, dtype={"pmid": str})
    sys.exit(f"No coding file found: {XLSX} or {BLIND}")

def main():
    blind = load_coding()
    for c in ("human_failure_mode","human_model_type"):
        if c not in blind.columns:
            sys.exit(f"Missing column '{c}' in coding file.")
    model = pd.read_csv(AC, dtype={"pmid": str})[["pmid","failure_mode","model_type"]]
    df = blind.merge(model, on="pmid", how="left",
                     suffixes=("", "_model"))

    # normalize human columns; a row counts as "coded" only if it carries a
    # valid label on at least one axis (empty cells read back as NaN→"nan")
    for c in ("human_failure_mode","human_model_type"):
        df[c] = df[c].astype(str).str.strip().str.lower()
    coded = df[df["human_failure_mode"].isin(FM_LABELS) |
               df["human_model_type"].isin(MT_LABELS)].copy()
    n_total, n_coded = len(df), len(coded)
    print(f"Validation rows: {n_total} | coded so far: {n_coded}")
    if n_coded == 0:
        print("No rows coded yet — fill human_failure_mode / human_model_type and re-run.")
        return

    def landis_koch(k):
        return ("poor" if k < 0 else "slight" if k < 0.20 else "fair" if k < 0.40
                else "moderate" if k < 0.60 else "substantial" if k < 0.80
                else "almost perfect")

    md = ["# Q7 validation — inter-rater agreement (human vs classifier)\n",
          f"Coded rows: **{n_coded}/{n_total}**. Cohen's κ (unweighted, nominal). "
          "Strength labels per Landis & Koch (1977).\n"]

    def report(axis, human_col, model_col, labels):
        h = coded[human_col]
        m = coded[model_col].astype(str).str.strip().str.lower()
        valid = h.isin(labels) & m.isin(labels)
        bad = (~valid).sum()
        h, m = h[valid], m[valid]
        if len(h) == 0:
            print(f"\n[{axis}] no valid coded rows."); return
        kappa = cohen_kappa_score(h, m, labels=labels)
        agree = (h.values == m.values).mean()
        print(f"\n{'='*70}\n[{axis}]  n={len(h)}"
              + (f"  ({bad} rows with out-of-vocab labels skipped)" if bad else ""))
        print(f"  Cohen's kappa : {kappa:+.3f}  ({landis_koch(kappa)})")
        print(f"  raw agreement : {agree*100:.1f}%")
        cm = confusion_matrix(h, m, labels=labels)
        cmdf = pd.DataFrame(cm, index=[f"H:{l}" for l in labels],
                            columns=[f"M:{l}" for l in labels])
        print("  confusion matrix (rows=human, cols=model):")
        print(cmdf.to_string())
        md.append(f"\n## {axis}\n")
        md.append(f"- n = {len(h)}{f' ({bad} out-of-vocab skipped)' if bad else ''}")
        md.append(f"- **Cohen's κ = {kappa:+.3f}** ({landis_koch(kappa)})")
        md.append(f"- raw agreement = {agree*100:.1f}%\n")
        md.append("Confusion matrix (rows = human, cols = model):\n")
        md.append("| | " + " | ".join(cmdf.columns) + " |")
        md.append("|" + "---|" * (len(cmdf.columns) + 1))
        for idx, row in cmdf.iterrows():
            md.append(f"| **{idx}** | " + " | ".join(str(v) for v in row.values) + " |")
        md.append("")

    report("failure_mode", "human_failure_mode", "failure_mode", FM_LABELS)
    report("model_type",   "human_model_type",   "model_type",   MT_LABELS)

    # disagreement rows for adjudication
    dis = coded[(coded["human_failure_mode"] != coded["failure_mode"].str.lower()) |
                (coded["human_model_type"]   != coded["model_type"].str.lower())]
    keep = ["pmid","pub_year","human_failure_mode","failure_mode",
            "human_model_type","model_type"]
    keep = [c for c in keep if c in dis.columns]
    out_dis = os.path.join(BASE, "output", "analyses", "q7_validation_disagreements.csv")
    dis[keep].to_csv(out_dis, index=False)
    out_md = os.path.join(BASE, "output", "analyses", "q7_kappa_report.md")
    with open(out_md, "w") as f:
        f.write("\n".join(md))
    print(f"\nDisagreements ({len(dis)} rows) → {out_dis}")
    print(f"Report → {out_md}")

if __name__ == "__main__":
    main()
