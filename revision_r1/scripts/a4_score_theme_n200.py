"""A1 theme scoring, PRIMARY ANALYSIS AFTER AMENDMENT 1 (2026-10-26): all 200
sampled records. A record where the coder ticked no theme ("can't tell" /
"no theme detected") is scored as an empty human set, so every model theme on
it counts as a false positive. Reason: the manuscript reports model themes for
every critical record, including these.

Amendment 1 was made after the coded sheet was returned and the originally
pre-specified analysis (frozen a4_score_theme.py, which excludes such
records) had been run; that analysis is kept as a secondary result. This
script reuses the frozen functions unchanged and writes the same report
format as the frozen scorer.

Usage: python a4_score_theme_n200.py --completed <COMPLETED.xlsx> --outdir <dir>
"""

import argparse
from pathlib import Path

import pandas as pd

import a4_score_theme as S
from r1_common import md_table


def main():
    ap = argparse.ArgumentParser()
    here = Path(__file__).resolve().parent
    ap.add_argument("--completed", required=True)
    ap.add_argument("--key", default=str(here.parent / "coding/theme_key.csv"))
    ap.add_argument("--manifest", default=str(here.parent / "coding/theme_sampling_manifest.csv"))
    ap.add_argument("--outdir", required=True)
    a = ap.parse_args()
    out = Path(a.outdir); out.mkdir(parents=True, exist_ok=True)

    key = pd.read_csv(a.key, dtype={"pmid": str})
    man = pd.read_csv(a.manifest)
    man = man[man["year"].astype(str) != "All"]
    frame_n = {int(r.year): int(r.frame_n) for r in man.itertuples()}
    df = key.merge(S.read_completed(a.completed), on="row_id", how="left", validate="one_to_one")
    for t in S.THEMES:
        df[f"h_{t}"] = df[t].fillna(0).astype(int)
        df[f"m_{t}"] = df["model_themes"].fillna("").str.split("|").apply(lambda l: int(t in l))
    nh = df[[f"h_{t}" for t in S.THEMES]].sum(axis=1)
    n_empty, over3 = int((nh == 0).sum()), int((nh > 3).sum())

    rows = []
    for band, ys in [("All 2021–2025", list(frame_n))] + list(S.BANDS.items()):
        sub = df[df["year"].isin(ys)].reset_index(drop=True)
        for (lab, k), (v, lo, hi) in S.score(sub, frame_n).items():
            rows.append({"band": band, "weighting": lab, "metric": k, "estimate": v, "lo": lo, "hi": hi, "n_records": len(sub)})
    res = pd.DataFrame(rows)
    res.to_csv(out / "theme_scores_long.csv", index=False)

    support_unw = {t: int(df[f"h_{t}"].sum()) for t in S.THEMES}
    nthemes = pd.crosstab(nh.rename("n_human"), df[[f"m_{t}" for t in S.THEMES]].sum(axis=1).rename("n_model"))
    nthemes.to_csv(out / "theme_n_themes_crosstab.csv")

    def fmt(band, lab, k):
        x = res[(res.band == band) & (res.weighting == lab) & (res.metric == k)]
        if x.empty or pd.isna(x.estimate.iloc[0]):
            return "n/a"
        x = x.iloc[0]
        return f"{x.estimate:.3f} ({x.lo:.3f}–{x.hi:.3f})"

    L = ["# Theme classifier validation scores — PRIMARY (amendment 1: all 200 records)\n",
         f"Records: {len(df)}; with no human theme (scored as empty sets): {n_empty}; more than 3 ticked: {over3}.\n",
         "## Per theme (all years)\n",
         "| theme | human-positive n | support flag | precision (unw.) | recall (unw.) | F1 (unw.) | precision (wt.) | recall (wt.) | F1 (wt.) |",
         "|---|---|---|---|---|---|---|---|---|"]
    for t in S.THEMES:
        flag = "insufficient support" if support_unw[t] < 10 else ""
        L.append(f"| {t} | {support_unw[t]} | {flag} | " + " | ".join(
            fmt("All 2021–2025", lab, f"{t}|{k}") for lab in ("unweighted", "weighted") for k in ("precision", "recall", "F1")) + " |")
    L += ["\n## Overall, by year band\n",
          "| band | weighting | micro-F1 | macro-F1 | exact match | Hamming loss | mean Jaccard | mean n themes human | mean n themes model |",
          "|---|---|---|---|---|---|---|---|---|"]
    for band in ["All 2021–2025"] + list(S.BANDS):
        for lab in ("unweighted", "weighted"):
            L.append(f"| {band} | {lab} | " + " | ".join(fmt(band, lab, k) for k in
                     ("micro_F1", "macro_F1", "exact_match", "hamming_loss", "mean_jaccard",
                      "mean_n_themes_human", "mean_n_themes_model")) + " |")
    L += ["\n## Number of themes per record (rows human, columns model; unweighted counts)\n",
          md_table(nthemes.reset_index(), "{:.0f}")]
    (out / "theme_scores.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
