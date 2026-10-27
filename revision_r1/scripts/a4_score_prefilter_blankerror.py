"""A3 prefilter-audit scoring, PRIMARY ANALYSIS AFTER AMENDMENT 2 (2026-10-26):
every coded row is used. A row the coder left unlabelled ("can't tell") is
counted as an error of whichever classifier is being evaluated:
  * production-prefilter estimands (1−NPV, missed records, PPV among retained,
    production 2×2, year logistic test): human KEEP := NOT production KEEP;
  * full-abstract re-run estimands (EX-F precision, full-abstract 2×2):
    human KEEP := NOT full-abstract KEEP;
  * PILOT intra-rater agreement: counted as a disagreement;
  * 3-class tables: shown as a separate 'unlabelled' row.
The originally pre-specified rule (protocol §6: exclude unlabelled rows) is
kept as the secondary analysis (frozen a4_score_prefilter.py). This script
reuses the frozen functions (estimates, boot, logistic_tests, read_completed)
unchanged.

Usage: python a4_score_prefilter_blankerror.py --completed <COMPLETED.xlsx> --outdir <dir>
"""

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

import a4_score_prefilter as P
from r1_common import cohen_kappa_cm, confusion, md_table

PROD_KEYS = ("missed_", "FNrate_", "PPV_RET_", "prod2x2_")
FULL_KEYS = ("fullabs_precision_", "full2x2_")


def build(df, N, variant, against):
    d = df[df["stratum"] != "PILOT"].copy()
    d["blank"] = ~d["human_label"].isin(P.LAB3)
    d["keep_h"] = d["human_label"].isin(P.KEEP)
    if variant == "borderline→application":
        d.loc[d.borderline & ~d.blank, "keep_h"] = False
    elif variant == "borderline→KEEP":
        d.loc[d.borderline & ~d.blank, "keep_h"] = True
    d["keep_prod"] = d["label_production"].isin(P.KEEP)
    d["keep_full"] = d["label_fullabstract"].isin(P.KEEP)
    ref = d["keep_prod"] if against == "production" else d["keep_full"]
    d.loc[d.blank, "keep_h"] = ~ref[d.blank]          # blank = error of the classifier evaluated
    d["year"] = d["year"].astype(int)
    n_c = d.groupby(["stratum", "year"]).size()
    d["w"] = [N[(s, y)] / n_c[(s, y)] for s, y in zip(d.stratum, d.year)]
    return d.reset_index(drop=True)


def main():
    ap = argparse.ArgumentParser()
    here = Path(__file__).resolve().parent
    ap.add_argument("--completed", required=True)
    ap.add_argument("--key", default=str(here.parent / "coding/prefilter_key.csv"))
    ap.add_argument("--manifest", default=str(here.parent / "coding/prefilter_sampling_manifest.csv"))
    ap.add_argument("--outdir", required=True)
    a = ap.parse_args()
    out = Path(a.outdir); out.mkdir(parents=True, exist_ok=True)

    key = pd.read_csv(a.key, dtype={"pmid": str}, keep_default_na=False)
    man = pd.read_csv(a.manifest)
    N = {(r.stratum, int(r.year)): int(r.frame_n) for r in man.itertuples() if r.stratum != "PILOT"}
    df = key.merge(P.read_completed(a.completed), on="row_id", how="left", validate="one_to_one")
    n_blank = int((~df["human_label"].isin(P.LAB3)).sum())
    blank_by_stratum = df.loc[~df["human_label"].isin(P.LAB3), "stratum"].value_counts().to_dict()

    rows = []
    for variant in ("primary", "borderline→application", "borderline→KEEP"):
        dp = build(df, N, variant, "production")
        dfu = build(df, N, variant, "full-abstract")
        for d, prefixes in ((dp, PROD_KEYS), (dfu, FULL_KEYS)):
            point = P.estimates(d, N)
            B = P.boot(d, N)
            for k, v in point.items():
                if k.startswith(prefixes):
                    lo, hi = np.nanpercentile(B[k], [2.5, 97.5]) if B[k].notna().any() else (np.nan, np.nan)
                    rows.append({"variant": variant, "estimate_name": k, "estimate": v, "lo": lo, "hi": hi})
        for k, v in P.logistic_tests(dp).items():
            rows.append({"variant": variant, "estimate_name": f"logit_year_{k}", "estimate": v, "lo": np.nan, "hi": np.nan})
    R = pd.DataFrame(rows)
    R.to_csv(out / "prefilter_scores_long.csv", index=False)

    def f(variant, k, pct=True, dp_=1):
        x = R[(R.variant == variant) & (R.estimate_name == k)]
        if x.empty or pd.isna(x.estimate.iloc[0]):
            return "n/a"
        x = x.iloc[0]; s = 100 if pct else 1
        sep = " to " if (not pd.isna(x.lo)) and (x.lo < 0 or x.hi < 0) else "–"
        ci = "" if pd.isna(x.lo) else f" ({x.lo*s:.{dp_}f}{sep}{x.hi*s:.{dp_}f})"
        return f"{x.estimate*s:.{dp_}f}{ci}"

    L = ["# Prefilter audit scores — PRIMARY (amendment 2: unlabelled rows counted as errors)\n",
         f"Rows: {len(df)}; unlabelled: {n_blank} (by stratum: {blank_by_stratum}); borderline=Y: {int(df.borderline.sum())}.\n"]
    d3 = df[df["stratum"] != "PILOT"].copy()
    d3["human3"] = d3["human_label"].where(d3["human_label"].isin(P.LAB3), "unlabelled")
    rowsets = P.LAB3 + ["unlabelled"]
    for col, name in (("label_production", "production"), ("label_fullabstract", "full-abstract")):
        ct = pd.crosstab(d3["human3"], d3[col]).reindex(index=rowsets, columns=P.LAB3, fill_value=0)
        ct.to_csv(out / f"confusion3_human_vs_{name}_unweighted.csv")
        L += [f"### 3-class: human (rows) × {name} label (columns), coded sample, unweighted\n",
              md_table(ct.reset_index().rename(columns={"human3": ""}), "{:.0f}"), ""]
    for variant in ("primary", "borderline→application", "borderline→KEEP"):
        L += [f"## Variant: {variant}\n",
              "| year | 1−NPV, % (excluded) | missed AI-engaged records | PPV retained, % | full-abstract precision (EX-F), % |",
              "|---|---|---|---|---|"]
        for y in P.YEARS:
            L.append(f"| {y} | {f(variant, f'FNrate_{y}')} | {f(variant, f'missed_{y}', False, 0)} | "
                     f"{f(variant, f'PPV_RET_{y}')} | {f(variant, f'fullabs_precision_{y}')} |")
        L.append(f"| pooled | {f(variant, 'FNrate_pooled')} | {f(variant, 'missed_total', False, 0)} | "
                 f"{f(variant, 'PPV_RET_pooled')} | {f(variant, 'fullabs_precision_pooled')} |")
        L.append(f"\n1−NPV 2021–2022: {f(variant, 'FNrate_2021_2022')}%; 2024–2025: {f(variant, 'FNrate_2024_2025')}%; "
                 f"difference (2024–25 minus 2021–22): {f(variant, 'FNrate_diff_2024_25_minus_2021_22')} pp.")
        L.append(f"Logistic, year on human KEEP within excluded strata: unweighted OR/yr "
                 f"{f(variant, 'logit_year_OR_unweighted', False, 3)} (Wald {f(variant, 'logit_year_OR_unw_lo', False, 3)}–"
                 f"{f(variant, 'logit_year_OR_unw_hi', False, 3)}, P={f(variant, 'logit_year_P_unweighted_wald', False, 3)}; "
                 f"stratum adjusted); weighted OR/yr {f(variant, 'logit_year_OR_weighted', False, 3)} (bootstrap "
                 f"{f(variant, 'logit_year_OR_w_boot_lo', False, 3)}–{f(variant, 'logit_year_OR_w_boot_hi', False, 3)}).\n")
        L += ["| population-weighted 2×2 | production prefilter | full-abstract re-run |", "|---|---|---|"]
        for k in ("sensitivity", "specificity", "PPV", "NPV", "kappa", "AC1"):
            pct = k not in ("kappa", "AC1")
            L.append(f"| {k} | {f(variant, f'prod2x2_{k}', pct, 1 if pct else 3)} | {f(variant, f'full2x2_{k}', pct, 1 if pct else 3)} |")
        L.append("")

    pil = df[df["stratum"] == "PILOT"].copy()
    h = pil["human_label"].where(pil["human_label"].isin(P.LAB3), "unlabelled")
    agree3 = int((h == pil["pilot_my_label"]).sum())
    labelled = pil[pil["human_label"].isin(P.LAB3)]
    cm3 = confusion(labelled["pilot_my_label"], labelled["human_label"], P.LAB3)
    hb = pil["pilot_my_label"].isin(P.KEEP).to_numpy()
    nb = np.where(pil["human_label"].isin(P.LAB3), pil["human_label"].isin(P.KEEP), ~hb)  # blank = disagreement
    cm2 = np.array([[(hb & nb).sum(), (hb & ~nb).sum()], [(~hb & nb).sum(), (~hb & ~nb).sum()]])
    L += ["## Intra-rater agreement (PILOT rows: original my_label vs new code; unlabelled = disagreement)\n",
          f"n = {len(pil)} (unlabelled: {int((h == 'unlabelled').sum())}); 3-class agreement {agree3}/{len(pil)} = "
          f"{agree3/len(pil)*100:.1f}%; KEEP/DROP agreement {np.trace(cm2)}/{cm2.sum()} = {np.trace(cm2)/cm2.sum()*100:.1f}%, "
          f"κ = {cohen_kappa_cm(cm2):.3f}. 3-class κ on labelled rows only (κ is undefined for a missing category): "
          f"{cohen_kappa_cm(cm3):.3f} (n = {cm3.sum()}).\n"]
    (out / "prefilter_scores.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
