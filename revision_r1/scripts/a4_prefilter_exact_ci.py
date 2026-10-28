"""A3 prefilter audit · AMENDMENT 3 (2026-10-28): intervals that remain valid
when a sampling cell has no variation (e.g. 0/45 or 10/10), where the
within-cell percentile bootstrap collapses to a single point.

  * Single-cell proportions (by-year 1−NPV components, PPV among retained,
    EX-F precision): exact Clopper–Pearson 95% CI, with the Wilson interval
    alongside.
  * Weighted combinations of cells (per-year and pooled 1−NPV, missed
    records, pooled PPV / precision, population-weighted 2×2 metrics):
    there is no exact interval; each cell's human-KEEP proportion is drawn
    from its Jeffreys posterior Beta(k+½, n−k+½) (10,000 draws, seed 42) and
    the estimate recomputed; 2.5th–97.5th percentiles are reported.
Point estimates and label assignment are those of the primary analysis
(a4_score_prefilter_blankerror.build: unlabelled row = error of the
classifier evaluated). The bootstrap intervals are reported alongside.

Usage: python a4_prefilter_exact_ci.py --completed <COMPLETED.xlsx> --outdir <dir>
"""

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

import a4_score_prefilter as P
from a4_score_prefilter_blankerror import build
from r1_common import binary_metrics_cm, md_table

N_DRAW, SEED = 10000, 42
YEARS = P.YEARS


def cp(k, n, a=0.05):
    lo = 0.0 if k == 0 else stats.beta.ppf(a / 2, k, n - k + 1)
    hi = 1.0 if k == n else stats.beta.ppf(1 - a / 2, k + 1, n - k)
    return lo, hi


def wilson(k, n, z=1.959963984540054):
    p = k / n
    c = (p + z * z / (2 * n)) / (1 + z * z / n)
    h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return c - h, c + h


def prod_from_cells(p, N):
    """p: {(stratum, year): human-KEEP proportion}. Production-prefilter estimands."""
    out = {}
    M_tot = Nex = 0.0
    for y in YEARS:
        nf, ns = N[("EX-F", y)], N[("EX-S", y)]
        M = nf * p[("EX-F", y)] + ns * p[("EX-S", y)]
        out[f"missed_{y}"] = M; out[f"FNrate_{y}"] = M / (nf + ns)
        M_tot += M; Nex += nf + ns
    out["missed_total"] = M_tot; out["FNrate_pooled"] = M_tot / Nex
    for band, ys in (("2021_2022", [2021, 2022]), ("2024_2025", [2024, 2025])):
        out[f"FNrate_{band}"] = sum(out[f"missed_{y}"] for y in ys) / sum(N[("EX-F", y)] + N[("EX-S", y)] for y in ys)
    out["FNrate_diff_2024_25_minus_2021_22"] = out["FNrate_2024_2025"] - out["FNrate_2021_2022"]
    nret = sum(N[("RET", y)] for y in YEARS)
    TP = sum(N[("RET", y)] * p[("RET", y)] for y in YEARS)
    out["PPV_RET_pooled"] = TP / nret
    for k, v in binary_metrics_cm(TP, M_tot, nret - TP, Nex - M_tot).items():
        out[f"prod2x2_{k}"] = v
    return out


def full_from_subcells(q, W, N):
    """q: {(stratum, year, keep_full): human-KEEP proportion};
    W: {(stratum, year, keep_full): weighted record count}. Full-abstract estimands."""
    out = {}
    tp = fn = fp = tn = 0.0
    for key, w in W.items():
        h = q[key]; f = key[2]
        if f:
            tp += w * h; fp += w * (1 - h)
        else:
            fn += w * h; tn += w * (1 - h)
    for k, v in binary_metrics_cm(tp, fn, fp, tn).items():
        out[f"full2x2_{k}"] = v
    nexf = sum(N[("EX-F", y)] for y in YEARS)
    out["fullabs_precision_pooled"] = sum(N[("EX-F", y)] * q[("EX-F", y, True)] for y in YEARS) / nexf
    return out


def main():
    ap = argparse.ArgumentParser()
    here = Path(__file__).resolve().parent
    ap.add_argument("--completed", required=True)
    ap.add_argument("--key", default=str(here.parent / "coding/prefilter_key.csv"))
    ap.add_argument("--manifest", default=str(here.parent / "coding/prefilter_sampling_manifest.csv"))
    ap.add_argument("--boot", default=str(here.parent / "outputs/A4_prefilter_primary/prefilter_scores_long.csv"))
    ap.add_argument("--outdir", required=True)
    a = ap.parse_args()
    out = Path(a.outdir); out.mkdir(parents=True, exist_ok=True)

    key = pd.read_csv(a.key, dtype={"pmid": str}, keep_default_na=False)
    man = pd.read_csv(a.manifest)
    N = {(r.stratum, int(r.year)): int(r.frame_n) for r in man.itertuples() if r.stratum != "PILOT"}
    df = key.merge(P.read_completed(a.completed), on="row_id", how="left", validate="one_to_one")
    boot = pd.read_csv(a.boot)

    all_rows, cell_rows = [], []
    for variant in ("primary", "borderline→application", "borderline→KEEP"):
        dp = build(df, N, variant, "production")
        dfu = build(df, N, variant, "full-abstract")
        # cells for production estimands
        kc = dp.groupby(["stratum", "year"])["keep_h"].agg(["sum", "size"])
        p0 = {c: r["sum"] / r["size"] for c, r in kc.iterrows()}
        # sub-cells (stratum, year, keep_full) for full-abstract estimands
        g = dfu.groupby(["stratum", "year", "keep_full"])
        ks = g["keep_h"].agg(["sum", "size"])
        n_cell = dfu.groupby(["stratum", "year"]).size()
        W = {c: N[(c[0], c[1])] / n_cell[(c[0], c[1])] * r["size"] for c, r in ks.iterrows()}
        q0 = {c: r["sum"] / r["size"] for c, r in ks.iterrows()}
        point = {**prod_from_cells(p0, N), **full_from_subcells(q0, W, N)}
        # check against the frozen record-level estimator
        ref = {**{k: v for k, v in P.estimates(dp, N).items() if k.startswith(("missed", "FNrate", "PPV_RET_pooled", "prod2x2"))},
               **{k: v for k, v in P.estimates(dfu, N).items() if k.startswith(("full2x2", "fullabs_precision_pooled"))}}
        for k in point:
            if k in ref and not (np.isnan(point[k]) and np.isnan(ref[k])):
                assert abs(point[k] - ref[k]) < 1e-9, f"point mismatch {k}: {point[k]} vs {ref[k]}"

        rng = np.random.default_rng(SEED)
        draws = []
        for _ in range(N_DRAW):
            p = {c: rng.beta(r["sum"] + 0.5, r["size"] - r["sum"] + 0.5) for c, r in kc.iterrows()}
            q = {c: rng.beta(r["sum"] + 0.5, r["size"] - r["sum"] + 0.5) for c, r in ks.iterrows()}
            draws.append({**prod_from_cells(p, N), **full_from_subcells(q, W, N)})
        D = pd.DataFrame(draws)
        for k, v in point.items():
            lo, hi = np.nanpercentile(D[k], [2.5, 97.5])
            b = boot[(boot.variant == variant) & (boot.estimate_name == k)]
            all_rows.append({"variant": variant, "estimate_name": k, "estimate": v,
                             "jeffreys_lo": lo, "jeffreys_hi": hi,
                             "boot_lo": b.lo.iloc[0] if len(b) else np.nan, "boot_hi": b.hi.iloc[0] if len(b) else np.nan})
        # single-cell exact intervals
        for (s, y), r in kc.iterrows():
            k_, n_ = int(r["sum"]), int(r["size"])
            if s == "EX-F":
                kf = int(ks.loc[(s, y, True), "sum"]) if (s, y, True) in ks.index else 0  # vs full-abstract
                nf = int(ks.loc[(s, y, True), "size"]) if (s, y, True) in ks.index else 0
            lo, hi = cp(k_, n_); wl, wh = wilson(k_, n_)
            cell_rows.append({"variant": variant, "stratum": s, "year": y, "comparison": "vs production",
                              "human_KEEP": k_, "n": n_, "proportion": k_ / n_, "CP_lo": lo, "CP_hi": hi,
                              "Wilson_lo": wl, "Wilson_hi": wh})
            if s == "EX-F":
                lo, hi = cp(kf, nf); wl, wh = wilson(kf, nf)
                cell_rows.append({"variant": variant, "stratum": s, "year": y, "comparison": "vs full-abstract (precision)",
                                  "human_KEEP": kf, "n": nf, "proportion": kf / nf, "CP_lo": lo, "CP_hi": hi,
                                  "Wilson_lo": wl, "Wilson_hi": wh})
    R = pd.DataFrame(all_rows); C = pd.DataFrame(cell_rows)
    R.to_csv(out / "prefilter_exact_ci_long.csv", index=False)
    C.to_csv(out / "prefilter_cell_exact_ci.csv", index=False)

    def fmt(variant, k, s=100, d=1):
        x = R[(R.variant == variant) & (R.estimate_name == k)].iloc[0]
        sep = lambda lo, hi: " to " if lo < 0 or hi < 0 else "–"
        j = f"{x.jeffreys_lo*s:.{d}f}{sep(x.jeffreys_lo, x.jeffreys_hi)}{x.jeffreys_hi*s:.{d}f}"
        bb = "n/a" if np.isnan(x.boot_lo) else f"{x.boot_lo*s:.{d}f}{sep(x.boot_lo, x.boot_hi)}{x.boot_hi*s:.{d}f}"
        return f"{x.estimate*s:.{d}f}", j, bb

    L = ["# Prefilter audit — intervals robust to zero-event cells (Amendment 3)\n",
         "Point estimates = primary analysis (unlabelled row counted as an error). 'Jeffreys' = percentile interval "
         f"from {N_DRAW:,} draws of each cell's Beta(k+½, n−k+½) posterior (seed 42); 'bootstrap' = the within-cell "
         "percentile bootstrap reported earlier.\n"]
    for variant in ("primary", "borderline→application", "borderline→KEEP"):
        L += [f"## {variant}\n", "| estimand | estimate | 95% interval (Jeffreys) | 95% interval (bootstrap) |", "|---|---|---|---|"]
        items = ([(f"1−NPV {y}, %", f"FNrate_{y}", 100, 1) for y in YEARS] +
                 [("1−NPV pooled 2021–2025, %", "FNrate_pooled", 100, 1),
                  ("1−NPV 2021–2022, %", "FNrate_2021_2022", 100, 1), ("1−NPV 2024–2025, %", "FNrate_2024_2025", 100, 1),
                  ("difference 2024–25 minus 2021–22, pp", "FNrate_diff_2024_25_minus_2021_22", 100, 1)] +
                 [(f"missed records {y}", f"missed_{y}", 1, 0) for y in YEARS] +
                 [("missed records total", "missed_total", 1, 0), ("PPV among retained, pooled, %", "PPV_RET_pooled", 100, 1),
                  ("full-abstract precision (EX-F), pooled, %", "fullabs_precision_pooled", 100, 1)] +
                 [(f"production 2×2 {m}", f"prod2x2_{m}", 100 if m not in ("kappa", "AC1") else 1, 1 if m not in ("kappa", "AC1") else 3)
                  for m in ("sensitivity", "specificity", "PPV", "NPV", "kappa", "AC1")] +
                 [(f"full-abstract 2×2 {m}", f"full2x2_{m}", 100 if m not in ("kappa", "AC1") else 1, 1 if m not in ("kappa", "AC1") else 3)
                  for m in ("sensitivity", "specificity", "PPV", "NPV", "kappa", "AC1")])
        for lab, k, s, d in items:
            e, j, b = fmt(variant, k, s, d)
            L.append(f"| {lab} | {e} | {j} | {b} |")
        L.append("")
    L += ["**Do not use the Jeffreys intervals for the full-abstract 2×2.** That table splits RET cells by full-abstract "
          "label into sub-cells of n = 1–3, where the Jeffreys prior pulls proportions strongly toward ½. The resulting "
          "intervals for full-abstract specificity and PPV exclude the point estimate. Report the bootstrap interval for "
          "the full-abstract 2×2 instead (protocol Amendment 3).\n"]
    Cp = C[C.variant == "primary"].copy()
    Cp["proportion (exact CP 95% CI)"] = [f"{r.human_KEEP}/{r.n} = {r.proportion*100:.1f}% ({r.CP_lo*100:.1f}–{r.CP_hi*100:.1f})" for r in Cp.itertuples()]
    Cp["Wilson 95% CI"] = [f"{r.Wilson_lo*100:.1f}–{r.Wilson_hi*100:.1f}" for r in Cp.itertuples()]
    L += ["## Single-cell proportions, primary (exact Clopper–Pearson)\n",
          "EX-F/EX-S 'vs production' = human KEEP rate among records the production prefilter excluded; RET = PPV among "
          "retained; EX-F 'vs full-abstract' = precision of the full-abstract re-run.\n",
          md_table(Cp[["stratum", "year", "comparison", "proportion (exact CP 95% CI)", "Wilson 95% CI"]])]
    (out / "prefilter_exact_ci.md").write_text("\n".join(L) + "\n")
    print("\n".join(L[:40]))


if __name__ == "__main__":
    main()
