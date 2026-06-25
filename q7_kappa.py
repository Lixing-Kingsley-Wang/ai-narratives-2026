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
BLIND = os.path.join(BASE, "output", "analyses", "q7_validation_blind.csv")
AC    = os.path.join(BASE, "output", "analyses", "q7_classified_ac.csv")

FM_LABELS = ["confabulation","misclassification","both","none_or_unclear"]
MT_LABELS = ["generative","discriminative","both","unclear"]

def main():
    if not os.path.exists(BLIND):
        sys.exit(f"Blind file not found: {BLIND}")
    blind = pd.read_csv(BLIND, dtype={"pmid": str})
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
        print(f"  Cohen's kappa : {kappa:+.3f}")
        print(f"  raw agreement : {agree*100:.1f}%")
        cm = confusion_matrix(h, m, labels=labels)
        cmdf = pd.DataFrame(cm, index=[f"H:{l}" for l in labels],
                            columns=[f"M:{l}" for l in labels])
        print("  confusion matrix (rows=human, cols=model):")
        print(cmdf.to_string())

    report("failure_mode", "human_failure_mode", "failure_mode", FM_LABELS)
    report("model_type",   "human_model_type",   "model_type",   MT_LABELS)

if __name__ == "__main__":
    main()
