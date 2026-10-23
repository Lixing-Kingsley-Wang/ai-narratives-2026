"""A4 · Score the prefilter-audit workbook (D1, X2). Pre-specified in
revision_r1/coding/PROTOCOL_r1_validation.md §6.2.

Usage:
  python a4_score_prefilter.py --completed <prefilter_audit_COMPLETED.xlsx>
      [--key ../coding/prefilter_key.csv] [--manifest ../coding/prefilter_sampling_manifest.csv]
      --outdir <dir> [--label SYNTHETIC]

KEEP = discourse or evaluative. Cell = stratum × year (EX-F, EX-S, RET;
2021–2025); weight = frame N / coded n per cell. PILOT rows are used only for
intra-rater agreement. Bootstrap: 1000 resamples within cells, seed 42.
Three variants: primary; borderline=Y → application; borderline=Y → KEEP.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from openpyxl import load_workbook
from scipy import stats

from r1_common import binary_metrics_cm, cohen_kappa_cm, confusion, md_table

YEARS = [2021, 2022, 2023, 2024, 2025]
LAB3 = ["discourse", "evaluative", "application"]
KEEP = {"discourse", "evaluative"}
N_BOOT, SEED = 1000, 42


def read_completed(path):
    ws = load_workbook(path, data_only=True)["Coding"]
    rows = list(ws.iter_rows(values_only=True))
    df = pd.DataFrame(rows[1:], columns=list(rows[0]))
    df["row_id"] = df["row_id"].astype(int)
    df["human_label"] = df["human_label"].fillna("").astype(str).str.strip().str.lower()
    df["borderline"] = df["borderline"].fillna("").astype(str).str.strip().str.upper().eq("Y")
    return df[["row_id", "human_label", "borderline", "notes"]]


def wlogit(X, y, w, iters=100):
    """Weighted logistic regression by IRLS; returns beta, model-based SE."""
    beta = np.zeros(X.shape[1])
    for _ in range(iters):
        p = 1 / (1 + np.exp(-(X @ beta)))
        W = w * p * (1 - p)
        H = X.T @ (X * W[:, None])
        step = np.linalg.solve(H, X.T @ (w * (y - p)))
        beta += step
        if np.abs(step).max() < 1e-10:
            break
    p = 1 / (1 + np.exp(-(X @ beta)))
    se = np.sqrt(np.diag(np.linalg.inv(X.T @ (X * (w * p * (1 - p))[:, None]))))
    return beta, se


def estimates(d, N):
    """d: coded audit rows (EX-F, EX-S, RET) with keep_h, keep_full; N: {(stratum, year): frame}."""
    out = {}
    p = d.groupby(["stratum", "year"])["keep_h"].mean()
    pf = d.groupby(["stratum", "year"])["keep_full"].mean()
    get = lambda s, y: p.get((s, y), np.nan)
    M_tot = Nex_tot = 0.0
    for y in YEARS:
        nf, ns = N.get(("EX-F", y), 0), N.get(("EX-S", y), 0)
        M = nf * np.nan_to_num(get("EX-F", y)) + ns * np.nan_to_num(get("EX-S", y))
        out[f"missed_{y}"] = M
        out[f"FNrate_{y}"] = M / (nf + ns) if nf + ns else np.nan
        out[f"PPV_RET_{y}"] = get("RET", y)
        out[f"fullabs_precision_{y}"] = get("EX-F", y)
        M_tot += M; Nex_tot += nf + ns
    out["missed_total"] = M_tot
    out["FNrate_pooled"] = M_tot / Nex_tot
    for band, ys in (("2021_2022", [2021, 2022]), ("2024_2025", [2024, 2025])):
        m = sum(out[f"missed_{y}"] for y in ys)
        n = sum(N.get(("EX-F", y), 0) + N.get(("EX-S", y), 0) for y in ys)
        out[f"FNrate_{band}"] = m / n
    out["FNrate_diff_2024_25_minus_2021_22"] = out["FNrate_2024_2025"] - out["FNrate_2021_2022"]
    nret = {y: N.get(("RET", y), 0) for y in YEARS}
    out["PPV_RET_pooled"] = sum(nret[y] * np.nan_to_num(get("RET", y)) for y in YEARS) / sum(nret.values())
    nexf = {y: N.get(("EX-F", y), 0) for y in YEARS}
    out["fullabs_precision_pooled"] = sum(nexf[y] * np.nan_to_num(get("EX-F", y)) for y in YEARS) / sum(nexf.values())
    # production 2x2 (weighted counts)
    TP = sum(nret[y] * np.nan_to_num(get("RET", y)) for y in YEARS)
    FP = sum(nret.values()) - TP
    FN = M_tot; TN = Nex_tot - M_tot
    for k, v in binary_metrics_cm(TP, FN, FP, TN).items():
        out[f"prod2x2_{k}"] = v
    out.update({"prod2x2_TP": TP, "prod2x2_FP": FP, "prod2x2_FN": FN, "prod2x2_TN": TN})
    # full-abstract classifier 2x2: weight each coded record by its cell weight
    w = d["w"].to_numpy(); h = d["keep_h"].to_numpy().astype(bool); f = d["keep_full"].to_numpy().astype(bool)
    tp, fn_, fp, tn = (w * (h & f)).sum(), (w * (h & ~f)).sum(), (w * (~h & f)).sum(), (w * (~h & ~f)).sum()
    for k, v in binary_metrics_cm(tp, fn_, fp, tn).items():
        out[f"full2x2_{k}"] = v
    return out


def boot(d, N):
    rng = np.random.default_rng(SEED)
    cells = [g.index.to_numpy() for _, g in d.groupby(["stratum", "year"])]
    draws = []
    for _ in range(N_BOOT):
        idx = np.concatenate([c[rng.integers(0, len(c), len(c))] for c in cells])
        draws.append(estimates(d.loc[idx].reset_index(drop=True), N))
    return pd.DataFrame(draws)


def logistic_tests(d):
    ex = d[d["stratum"].isin(["EX-F", "EX-S"])]
    yc = ex["year"] - ex["year"].mean()
    X = np.column_stack([np.ones(len(ex)), yc, (ex["stratum"] == "EX-F").astype(float)])
    y = ex["keep_h"].astype(float).to_numpy()
    res = {}
    if 0 < y.sum() < len(y):
        b, se = wlogit(X, y, np.ones(len(y)))
        z = b[1] / se[1]
        res.update({"OR_unweighted": np.exp(b[1]), "OR_unw_lo": np.exp(b[1] - 1.96 * se[1]),
                    "OR_unw_hi": np.exp(b[1] + 1.96 * se[1]), "P_unweighted_wald": 2 * stats.norm.sf(abs(z))})
        Xw = np.column_stack([np.ones(len(ex)), yc])
        bw, _ = wlogit(Xw, y, ex["w"].to_numpy())
        rng = np.random.default_rng(SEED)
        cells = [np.where((ex["stratum"] == s).to_numpy() & (ex["year"] == yy).to_numpy())[0]
                 for s in ("EX-F", "EX-S") for yy in YEARS]
        cells = [c for c in cells if len(c)]
        ors = []
        for _ in range(N_BOOT):
            idx = np.concatenate([c[rng.integers(0, len(c), len(c))] for c in cells])
            yy = y[idx]
            if 0 < yy.sum() < len(yy):
                try:
                    ors.append(np.exp(wlogit(Xw[idx], yy, ex["w"].to_numpy()[idx])[0][1]))
                except np.linalg.LinAlgError:
                    pass
        lo, hi = np.percentile(ors, [2.5, 97.5]) if ors else (np.nan, np.nan)
        res.update({"OR_weighted": np.exp(bw[1]), "OR_w_boot_lo": lo, "OR_w_boot_hi": hi})
    return res


def main():
    ap = argparse.ArgumentParser()
    here = Path(__file__).resolve().parent
    ap.add_argument("--completed", required=True)
    ap.add_argument("--key", default=str(here.parent / "coding/prefilter_key.csv"))
    ap.add_argument("--manifest", default=str(here.parent / "coding/prefilter_sampling_manifest.csv"))
    ap.add_argument("--outdir", required=True)
    ap.add_argument("--label", default="")
    a = ap.parse_args()
    out = Path(a.outdir); out.mkdir(parents=True, exist_ok=True)

    key = pd.read_csv(a.key, dtype={"pmid": str}, keep_default_na=False)
    man = pd.read_csv(a.manifest)
    N = {(r.stratum, int(r.year)): int(r.frame_n) for r in man.itertuples() if r.stratum != "PILOT"}
    df = key.merge(read_completed(a.completed), on="row_id", how="left", validate="one_to_one")
    unusable = df[~df["human_label"].isin(LAB3)]
    df = df[df["human_label"].isin(LAB3)].copy()

    L = [f"# Prefilter audit scores {a.label}\n",
         f"Coded rows usable: {len(df)}; unusable (blank/invalid label): {len(unusable)}; borderline=Y: {int(df.borderline.sum())}.\n"]
    all_rows = []
    for variant in ("primary", "borderline→application", "borderline→KEEP"):
        d = df[df["stratum"] != "PILOT"].copy()
        d["keep_h"] = d["human_label"].isin(KEEP)
        if variant == "borderline→application":
            d.loc[d.borderline, "keep_h"] = False
        elif variant == "borderline→KEEP":
            d.loc[d.borderline, "keep_h"] = True
        d["keep_full"] = d["label_fullabstract"].isin(KEEP)
        d["year"] = d["year"].astype(int)
        n_c = d.groupby(["stratum", "year"]).size()
        d["w"] = [N[(s, y)] / n_c[(s, y)] for s, y in zip(d.stratum, d.year)]
        d = d.reset_index(drop=True)
        point = estimates(d, N)
        B = boot(d, N)
        for k, v in point.items():
            lo, hi = np.nanpercentile(B[k], [2.5, 97.5]) if B[k].notna().any() else (np.nan, np.nan)
            all_rows.append({"variant": variant, "estimate_name": k, "estimate": v, "lo": lo, "hi": hi})
        for k, v in logistic_tests(d).items():
            all_rows.append({"variant": variant, "estimate_name": f"logit_year_{k}", "estimate": v, "lo": np.nan, "hi": np.nan})
        if variant == "primary":
            # 3-class confusion, coded sample (unweighted and weighted)
            for lab_col, name in (("label_production", "production"), ("label_fullabstract", "full-abstract")):
                cm = confusion(d["human_label"], d[lab_col], LAB3)
                cmw = pd.crosstab(d["human_label"], d[lab_col], values=d["w"], aggfunc="sum").reindex(index=LAB3, columns=LAB3).fillna(0)
                pd.DataFrame(cm, index=LAB3, columns=LAB3).to_csv(out / f"confusion3_human_vs_{name}_unweighted.csv")
                cmw.to_csv(out / f"confusion3_human_vs_{name}_weighted.csv")
                L.append(f"### 3-class: human (rows) × {name} label (columns), coded sample, unweighted\n")
                L.append(md_table(pd.DataFrame(cm, index=LAB3, columns=LAB3).reset_index().rename(columns={"index": ""}), "{:.0f}"))
                L.append("")
    R = pd.DataFrame(all_rows)
    R.to_csv(out / "prefilter_scores_long.csv", index=False)

    def f(variant, k, pct=True, d=1):
        x = R[(R.variant == variant) & (R.estimate_name == k)]
        if x.empty or pd.isna(x.estimate.iloc[0]):
            return "n/a"
        x = x.iloc[0]
        s = 100 if pct else 1
        sep = " to " if x.lo < 0 or x.hi < 0 else "–"
        ci = "" if pd.isna(x.lo) else f" ({x.lo*s:.{d}f}{sep}{x.hi*s:.{d}f})"
        return f"{x.estimate*s:.{d}f}{ci}"

    for variant in ("primary", "borderline→application", "borderline→KEEP"):
        L.append(f"## Variant: {variant}\n")
        L.append("| year | 1−NPV, % (excluded) | missed AI-engaged records | PPV retained, % | full-abstract precision (EX-F), % |")
        L.append("|---|---|---|---|---|")
        for y in YEARS:
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
        L.append("| population-weighted 2×2 | production prefilter | full-abstract re-run |\n|---|---|---|")
        for k in ("sensitivity", "specificity", "PPV", "NPV", "kappa", "AC1"):
            pct = k not in ("kappa", "AC1")
            L.append(f"| {k} | {f(variant, f'prod2x2_{k}', pct, 1 if pct else 3)} | {f(variant, f'full2x2_{k}', pct, 1 if pct else 3)} |")
        L.append("")

    pil = df[df["stratum"] == "PILOT"]
    if len(pil):
        cm3 = confusion(pil["pilot_my_label"], pil["human_label"], LAB3)
        hb = pil["pilot_my_label"].isin(KEEP).to_numpy(); nb = pil["human_label"].isin(KEEP).to_numpy()
        cm2 = np.array([[(hb & nb).sum(), (hb & ~nb).sum()], [(~hb & nb).sum(), (~hb & ~nb).sum()]])
        L += ["## Intra-rater agreement (PILOT rows: original my_label vs new code)\n",
              f"n = {len(pil)}; 3-class agreement {np.trace(cm3)}/{cm3.sum()} = {np.trace(cm3)/cm3.sum()*100:.1f}%, "
              f"κ = {cohen_kappa_cm(cm3):.3f}; KEEP/DROP agreement {np.trace(cm2)}/{cm2.sum()} = "
              f"{np.trace(cm2)/cm2.sum()*100:.1f}%, κ = {cohen_kappa_cm(cm2):.3f}.\n"]
    (out / "prefilter_scores.md").write_text("\n".join(L) + "\n")
    print("\n".join(L[:3]))
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
