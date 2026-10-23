"""A4 · Score the theme-validation workbook (D2a). Pre-specified in
revision_r1/coding/PROTOCOL_r1_validation.md §6.1.

Usage:
  python a4_score_theme.py --completed <theme_validation_COMPLETED.xlsx>
      [--key ../coding/theme_key.csv] [--manifest ../coding/theme_sampling_manifest.csv]
      --outdir <dir> [--label SYNTHETIC]

Comparisons are set-based per record (model themes from the key; human
themes = ticked columns). Weights w = frame_n(year) / coded_n(year).
Bootstrap: 1000 resamples of coded records within year, seed 42, percentile.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from openpyxl import load_workbook

from r1_common import md_table

THEMES = ["replacement", "hallucination", "safety_clinical", "ethics_bias", "cognitive",
          "education", "regulation", "existential", "data_privacy", "other"]
BANDS = {"2021–2022": [2021, 2022], "2023": [2023], "2024–2025": [2024, 2025]}
N_BOOT, SEED = 1000, 42


def read_completed(path):
    ws = load_workbook(path, data_only=True)["Coding"]
    rows = list(ws.iter_rows(values_only=True))
    hdr = list(rows[0])
    df = pd.DataFrame(rows[1:], columns=hdr)
    for t in THEMES:
        df[t] = df[t].apply(lambda v: 1 if str(v).strip() in ("1", "1.0") else 0)
    df["row_id"] = df["row_id"].astype(int)
    return df[["row_id"] + THEMES + ["notes"]]


def metrics(H, M, w):
    """H, M: (n, 10) 0/1 arrays; w: (n,) weights. Returns dict."""
    w = w[:, None]
    tp = (w * (H & M)).sum(0); fp = (w * (~H & M)).sum(0); fn = (w * (H & ~M)).sum(0)
    with np.errstate(invalid="ignore", divide="ignore"):
        prec = tp / (tp + fp); rec = tp / (tp + fn); f1 = 2 * tp / (2 * tp + fp + fn)
    ww = w[:, 0]
    inter = (H & M).sum(1); union = (H | M).sum(1)
    out = {f"{t}|{k}": v[i] for i, t in enumerate(THEMES)
           for k, v in (("precision", prec), ("recall", rec), ("F1", f1), ("support", (w * H).sum(0)))}
    out.update({
        "micro_F1": 2 * tp.sum() / (2 * tp.sum() + fp.sum() + fn.sum()),
        "macro_F1": np.nanmean(f1) if np.isfinite(f1).any() else np.nan,
        "exact_match": np.average((H == M).all(1), weights=ww),
        "hamming_loss": np.average((H ^ M).sum(1) / len(THEMES), weights=ww),
        "mean_jaccard": np.average(np.where(union > 0, inter / np.maximum(union, 1), 1.0), weights=ww),
        "mean_n_themes_human": np.average(H.sum(1), weights=ww),
        "mean_n_themes_model": np.average(M.sum(1), weights=ww),
    })
    return out


def score(df, frame_n):
    """Point estimates + bootstrap CIs, unweighted and weighted."""
    H = df[[f"h_{t}" for t in THEMES]].to_numpy().astype(bool)
    M = df[[f"m_{t}" for t in THEMES]].to_numpy().astype(bool)
    yrs = df["year"].to_numpy()
    n_y = pd.Series(yrs).value_counts()
    w = np.array([frame_n[y] / n_y[y] for y in yrs])
    res = {}
    for lab, ww in (("unweighted", np.ones(len(df))), ("weighted", w)):
        point = metrics(H, M, ww)
        rng = np.random.default_rng(SEED)
        cells = {y: np.where(yrs == y)[0] for y in np.unique(yrs)}
        draws = []
        for _ in range(N_BOOT):
            idx = np.concatenate([c[rng.integers(0, len(c), len(c))] for c in cells.values()])
            draws.append(metrics(H[idx], M[idx], ww[idx]))
        D = pd.DataFrame(draws)
        for k, v in point.items():
            lo, hi = np.nanpercentile(D[k], [2.5, 97.5]) if D[k].notna().any() else (np.nan, np.nan)
            res[(lab, k)] = (v, lo, hi)
    return res


def main():
    ap = argparse.ArgumentParser()
    here = Path(__file__).resolve().parent
    ap.add_argument("--completed", required=True)
    ap.add_argument("--key", default=str(here.parent / "coding/theme_key.csv"))
    ap.add_argument("--manifest", default=str(here.parent / "coding/theme_sampling_manifest.csv"))
    ap.add_argument("--outdir", required=True)
    ap.add_argument("--label", default="")
    a = ap.parse_args()
    out = Path(a.outdir); out.mkdir(parents=True, exist_ok=True)

    key = pd.read_csv(a.key, dtype={"pmid": str})
    man = pd.read_csv(a.manifest)
    man = man[man["year"].astype(str) != "All"]
    frame_n = {int(r.year): int(r.frame_n) for r in man.itertuples()}
    hum = read_completed(a.completed)
    df = key.merge(hum, on="row_id", how="left", validate="one_to_one")
    for t in THEMES:
        df[f"h_{t}"] = df[t].fillna(0).astype(int)
        df[f"m_{t}"] = df["model_themes"].fillna("").str.split("|").apply(lambda l: int(t in l))
    nh = df[[f"h_{t}" for t in THEMES]].sum(1)
    excluded = df[nh == 0]
    over3 = int((nh > 3).sum())
    df = df[nh > 0].reset_index(drop=True)

    rows = []
    for band, ys in [("All 2021–2025", list(frame_n))] + list(BANDS.items()):
        sub = df[df["year"].isin(ys)].reset_index(drop=True)
        if sub.empty:
            continue
        r = score(sub, frame_n)
        for (lab, k), (v, lo, hi) in r.items():
            rows.append({"band": band, "weighting": lab, "metric": k, "estimate": v, "lo": lo, "hi": hi, "n_records": len(sub)})
    res = pd.DataFrame(rows)
    res.to_csv(out / "theme_scores_long.csv", index=False)

    support_unw = {t: int(df[f"h_{t}"].sum()) for t in THEMES}
    nthemes = pd.crosstab(df[[f"h_{t}" for t in THEMES]].sum(1).rename("n_human"),
                          df[[f"m_{t}" for t in THEMES]].sum(1).rename("n_model"))
    nthemes.to_csv(out / "theme_n_themes_crosstab.csv")

    def fmt(band, lab, k):
        x = res[(res.band == band) & (res.weighting == lab) & (res.metric == k)]
        if x.empty or pd.isna(x.estimate.iloc[0]):
            return "n/a"
        x = x.iloc[0]
        return f"{x.estimate:.3f} ({x.lo:.3f}–{x.hi:.3f})"

    L = [f"# Theme classifier validation scores {a.label}\n",
         f"Coded records used: {len(df)} (excluded, no theme ticked: {len(excluded)}; more than 3 ticked, kept: {over3}).\n",
         "## Per theme (all years)\n",
         "| theme | human-positive n | support flag | precision (unw.) | recall (unw.) | F1 (unw.) | precision (wt.) | recall (wt.) | F1 (wt.) |",
         "|---|---|---|---|---|---|---|---|---|"]
    for t in THEMES:
        flag = "insufficient support" if support_unw[t] < 10 else ""
        L.append(f"| {t} | {support_unw[t]} | {flag} | " + " | ".join(
            fmt("All 2021–2025", lab, f"{t}|{k}") for lab in ("unweighted", "weighted") for k in ("precision", "recall", "F1")) + " |")
    L += ["\n## Overall, by year band\n", "| band | weighting | micro-F1 | macro-F1 | exact match | Hamming loss | mean Jaccard | mean n themes human | mean n themes model |",
          "|---|---|---|---|---|---|---|---|---|"]
    for band in ["All 2021–2025"] + list(BANDS):
        for lab in ("unweighted", "weighted"):
            L.append(f"| {band} | {lab} | " + " | ".join(fmt(band, lab, k) for k in
                     ("micro_F1", "macro_F1", "exact_match", "hamming_loss", "mean_jaccard",
                      "mean_n_themes_human", "mean_n_themes_model")) + " |")
    L += ["\n## Number of themes per record (rows human, columns model; unweighted counts)\n",
          md_table(nthemes.reset_index(), "{:.0f}")]
    (out / "theme_scores.md").write_text("\n".join(L) + "\n")
    print("\n".join(L[:6]))
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
