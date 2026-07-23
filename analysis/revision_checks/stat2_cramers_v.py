"""
TASK STAT-2 — Confirm chi-square N and compute Cramer's V.

For the opinion-vs-research publication-type chi-square (reported chi2_4 =
430.5). Rebuild the 2x5 contingency from v1 canonical labels (this only
TABULATES existing stance labels; it does NOT rerun classification), confirm
the exact N used, and compute Cramer's V:

    V = sqrt(chi2 / (N * min(r-1, c-1)))    ;  for 2x5, min(r-1,c-1)=1

Grouping matches the manuscript source (analysis/run_pubtype_stance.py /
pubtype_stance_v1.csv):
  Opinion  = Editorial + Commentary + Letter   (pub_type_simple_5)
  Research = Research Article
  Review is excluded (neither opinion nor research); FAILED already dropped.

Outputs:
  output/revision_checks/stat2_pubtype_chisq_effect_size.csv
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency

WT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(WT))
from analysis.robustness import STANCES, load_classifications  # noqa: E402

OUT = WT / "output" / "revision_checks"
OUT.mkdir(parents=True, exist_ok=True)


def main() -> None:
    v1 = load_classifications("v1")  # drops FAILED, 2021-2026, adds pub_type_simple_5
    op = v1[v1["pub_type_simple_5"].isin(["Editorial", "Commentary", "Letter"])]
    re_ = v1[v1["pub_type_simple_5"] == "Research Article"]

    contingency = pd.DataFrame({
        "Opinion (Ed+Com+Let)": op["stance"].value_counts().reindex(STANCES).fillna(0).astype(int),
        "Research Article": re_["stance"].value_counts().reindex(STANCES).fillna(0).astype(int),
    })
    print("Contingency (counts), rows=stance, cols=pubtype group:")
    print(contingency.to_string())

    chi2, p, dof, expected = chi2_contingency(contingency.values)
    N = int(contingency.values.sum())
    n_opinion = int(op.shape[0])
    n_research = int(re_.shape[0])
    r, c = contingency.shape  # 5 x 2
    min_dim = min(r - 1, c - 1)
    cramers_v = float(np.sqrt(chi2 / (N * min_dim)))
    # Using the reported chi2 = 430.5 exactly, for cross-check:
    cramers_v_reported = float(np.sqrt(430.5 / (N * min_dim)))

    print(f"\nN (opinion + research) = {N}  (= {n_opinion} + {n_research})")
    print(f"chi2 = {chi2:.4f}, dof = {dof}, p = {p:.3e}")
    print(f"table shape r x c = {r} x {c}; min(r-1,c-1) = {min_dim}")
    print(f"Cramer's V (recomputed chi2) = {cramers_v:.4f}")
    print(f"Cramer's V (reported chi2=430.5) = {cramers_v_reported:.4f}")

    res = pd.DataFrame([{
        "test": "opinion(Ed+Com+Let) vs Research Article x 5 stances (v1)",
        "N": N,
        "n_opinion": n_opinion,
        "n_research": n_research,
        "table_rows": r,
        "table_cols": c,
        "min_r1_c1": min_dim,
        "chi2_recomputed": chi2,
        "chi2_reported": 430.5,
        "dof": dof,
        "p_value": p,
        "cramers_v_recomputed": cramers_v,
        "cramers_v_from_reported_chi2": cramers_v_reported,
    }])
    res.to_csv(OUT / "stat2_pubtype_chisq_effect_size.csv", index=False)
    # also persist the contingency for auditability
    contingency.to_csv(OUT / "stat2_pubtype_contingency.csv")
    print(f"\nSaved: {OUT / 'stat2_pubtype_chisq_effect_size.csv'}")
    print(f"Saved: {OUT / 'stat2_pubtype_contingency.csv'}")


if __name__ == "__main__":
    main()
