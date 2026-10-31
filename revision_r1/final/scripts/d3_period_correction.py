"""D3 · POST HOC (2026-10-31) period-specific misclassification correction
(JMIR R1 Batch 2d; D2b, X1). Plan: revision_r1/ANALYSIS_PLAN_batch2d.md (b8e1c7e).

Validation data from t2_stance_perclass.load_validation() (imported); strata = model
stance (T2). Periods 2021-2023 and 2024-2025; records dated 2026 (and 2020) excluded
from period estimates. Corrected prevalence = sum_c share_y(model=c) x P_g(target | c).
Bootstrap: 1000 draws, default_rng(42); validation resampled within stratum x period,
Jeffreys draw Beta(k+1/2, n-k+1/2) for cells with 0 or all events; corpus rows jointly.
Run with revision_r1/.venv.
Outputs: revision_r1/final/data/d3_*.csv
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.stats import beta, fisher_exact

from c_common import DATA, OUT, Y5, rc
from t2_stance_perclass import load_validation

S = rc.STANCES
PERIODS = {"2021-2023": [2021, 2022, 2023], "2024-2025": [2024, 2025]}
TARGETS = {"Advocacy": {"Advocacy"}, "Critical": {"Alarm", "Caution"}}


def cp(k, n):
    if n == 0:
        return np.nan, np.nan
    return (0.0 if k == 0 else beta.ppf(0.025, k, n - k + 1)) * 100, (1.0 if k == n else beta.ppf(0.975, k + 1, n - k)) * 100


def main():
    val = load_validation()
    n_all = len(val)
    val["period"] = val["year"].map({y: g for g, ys in PERIODS.items() for y in ys})
    excl = val[val["period"].isna()]["year"].value_counts().to_dict()
    vp = val[val["period"].notna()].reset_index(drop=True)

    # (1) conversion rates by stratum x period
    conv = []
    for c in S:
        for tname, tset in TARGETS.items():
            cnt = {}
            for g in PERIODS:
                d = vp[(vp.model == c) & (vp.period == g)]
                k, n = int(d["human"].isin(tset).sum()), len(d)
                lo, hi = cp(k, n)
                cnt[g] = (k, n)
                conv.append({"stratum": c, "target": tname, "period": g, "k": k, "n": n,
                             "pct": k / n * 100 if n else np.nan, "lo": lo, "hi": hi, "under10": n < 10})
            (k1, n1), (k2, n2) = cnt["2021-2023"], cnt["2024-2025"]
            p = fisher_exact([[k1, n1 - k1], [k2, n2 - k2]])[1] if n1 and n2 else np.nan
            conv.append({"stratum": c, "target": tname, "period": "Fisher exact P (period difference)", "P": p})
    pd.DataFrame(conv).to_csv(DATA / "d3_conversion_rates.csv", index=False)

    # (2) Advocacy accuracy by period
    acc = []
    for lay, d0 in (("all 300", vp), ("in-scope 225", vp[~vp["out_of_layerA"]])):
        for g in PERIODS:
            d = d0[d0.period == g]
            for m, num, den in (("precision (human Advocacy | model Advocacy)", (d.model == "Advocacy") & (d.human == "Advocacy"), d.model == "Advocacy"),
                                ("recall (model Advocacy | human Advocacy)", (d.model == "Advocacy") & (d.human == "Advocacy"), d.human == "Advocacy")):
                k, n = int(num.sum()), int(den.sum())
                lo, hi = cp(k, n)
                acc.append({"set": lay, "period": g, "metric": m, "k": k, "n": n, "pct": k / n * 100 if n else np.nan,
                            "lo": lo, "hi": hi})
    pd.DataFrame(acc).to_csv(DATA / "d3_advocacy_accuracy.csv", index=False)

    # (3) period-specific corrected prevalence (and the constant-rate estimator as a code check)
    corpus = rc.load_v1(year_range=(2021, 2025))
    cy = corpus["pub_year"].astype(int).to_numpy(); cs = corpus["stance"].to_numpy()
    ycode = np.array([Y5.index(y) for y in cy]); scode = np.array([S.index(s) for s in cs])
    gidx = {g: [Y5.index(y) for y in ys] for g, ys in PERIODS.items()}

    def shares(rows):
        M = np.zeros((5, 5)); np.add.at(M, (ycode[rows], scode[rows]), 1)
        return M / M.sum(1, keepdims=True)

    cells = {(c, g): np.where((vp.model == c).to_numpy() & (vp.period == g).to_numpy())[0] for c in S for g in PERIODS}
    hv = vp["human"].to_numpy()
    ind = {t: np.isin(hv, list(ts)).astype(float) for t, ts in TARGETS.items()}

    def rates(t, draw=None, rng=None):
        R = np.zeros((len(PERIODS), 5))
        for gi, g in enumerate(PERIODS):
            for ci, c in enumerate(S):
                ix = cells[(c, g)]; k, n = ind[t][ix].sum(), len(ix)
                if draw is None:
                    R[gi, ci] = k / n
                elif k == 0 or k == n:
                    R[gi, ci] = rng.beta(k + 0.5, n - k + 0.5)
                else:
                    R[gi, ci] = ind[t][ix[rng.integers(0, n, n)]].mean()
        return R

    def corr(Sh, R):
        out = np.zeros(5)
        for gi, g in enumerate(PERIODS):
            for yi in gidx[g]:
                out[yi] = Sh[yi] @ R[gi]
        return out * 100

    Sh0 = shares(np.arange(len(cy)))
    point = {t: corr(Sh0, rates(t)) for t in TARGETS}
    rng = np.random.default_rng(42)
    draws = {t: [] for t in TARGETS}
    for _ in range(1000):
        Rb = {t: rates(t, True, rng) for t in TARGETS}
        Shb = shares(rng.integers(0, len(cy), len(cy)))
        for t in TARGETS:
            draws[t].append(corr(Shb, Rb[t]))
    # constant-rate check (all 300 records, all years, as T2)
    hv_all, vm_all = val["human"].to_numpy(), val["model"].to_numpy()
    const = {t: (Sh0 @ np.array([np.isin(hv_all[vm_all == c], list(ts)).mean() for c in S])) * 100 for t, ts in TARGETS.items()}
    t2 = pd.read_csv(OUT / "T2_corrected_prevalence.csv")
    t2 = t2[(t2["validation set"] == "primary: all 300") & (t2["corpus"] == "all records")]
    res = []
    for t in TARGETS:
        D = np.array(draws[t])
        for yi, y in enumerate(Y5):
            lo, hi = np.percentile(D[:, yi], [2.5, 97.5])
            r2 = t2[(t2.outcome == t) & (t2.year.astype(str) == str(y))].iloc[0]
            res.append({"target": t, "year": y, "period_rates": "2021-2023" if y <= 2023 else "2024-2025",
                        "period_specific": point[t][yi], "ps_lo": lo, "ps_hi": hi,
                        "constant_rate_T2": r2["corrected %"], "cr_lo": r2["corr_lo"], "cr_hi": r2["corr_hi"],
                        "constant_rate_recomputed": const[t][yi], "observed": Sh0[yi, [S.index(s) for s in TARGETS[t]]].sum() * 100})
        dd = D[:, 4] - D[:, 0]; lo, hi = np.percentile(dd, [2.5, 97.5])
        r2 = t2[(t2.outcome == t) & (t2.year.astype(str).str.startswith("Δ"))].iloc[0]
        res.append({"target": t, "year": "change 2025 minus 2021", "period_specific": point[t][4] - point[t][0], "ps_lo": lo, "ps_hi": hi,
                    "constant_rate_T2": r2["corrected %"], "cr_lo": r2["corr_lo"], "cr_hi": r2["corr_hi"],
                    "constant_rate_recomputed": const[t][4] - const[t][0]})
    out = pd.DataFrame(res)
    out.to_csv(DATA / "d3_corrected_prevalence.csv", index=False)
    meta = pd.DataFrame([{"validation_records": n_all, "in_periods": len(vp), "excluded_by_year": str(excl),
                          "cells_under10": int(pd.DataFrame([c for c in conv if "n" in c and c["target"] == "Advocacy"])["under10"].sum()),
                          "jeffreys_cells_advocacy": sum(1 for (c, g), ix in cells.items() if ind["Advocacy"][ix].sum() in (0, len(ix))),
                          "jeffreys_cells_critical": sum(1 for (c, g), ix in cells.items() if ind["Critical"][ix].sum() in (0, len(ix)))}])
    meta.to_csv(DATA / "d3_meta.csv", index=False)
    print(meta.to_string())
    cv = pd.DataFrame(conv)
    print(cv[cv["n"].notna()][["stratum", "target", "period", "k", "n", "pct"]].to_string())
    print(cv[cv["P"].notna()][["stratum", "target", "P"]].to_string())
    print(pd.DataFrame(acc).to_string())
    print(out.round(2).to_string())


if __name__ == "__main__":
    main()
