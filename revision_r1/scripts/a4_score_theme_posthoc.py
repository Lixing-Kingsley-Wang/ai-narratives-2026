"""POST-HOC sensitivity analysis (not pre-specified; added 2026-10-26 after the
coded sheet was returned): keep the records where the coder ticked no theme
("can't tell" / "no theme detected") as human = empty set, instead of excluding
them as protocol §6 specifies. Every model theme on such a record then counts
as a false positive. Uses the frozen a4_score_theme.py functions unchanged.

Usage: python a4_score_theme_posthoc.py --completed <COMPLETED.xlsx> --outdir <dir>
"""

import argparse
from pathlib import Path

import pandas as pd

import a4_score_theme as S


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
    n_empty = int((df[[f"h_{t}" for t in S.THEMES]].sum(axis=1) == 0).sum())

    rows = []
    for band, ys in [("All 2021–2025", list(frame_n))] + list(S.BANDS.items()):
        sub = df[df["year"].isin(ys)].reset_index(drop=True)
        for (lab, k), (v, lo, hi) in S.score(sub, frame_n).items():
            rows.append({"band": band, "weighting": lab, "metric": k, "estimate": v, "lo": lo, "hi": hi, "n_records": len(sub)})
    res = pd.DataFrame(rows)
    res.to_csv(out / "theme_scores_posthoc_long.csv", index=False)

    def fmt(band, lab, k):
        x = res[(res.band == band) & (res.weighting == lab) & (res.metric == k)].iloc[0]
        return "n/a" if pd.isna(x.estimate) else f"{x.estimate:.3f} ({x.lo:.3f}–{x.hi:.3f})"

    L = ["# POST-HOC sensitivity: 'no theme' records kept as empty human sets\n",
         f"Not pre-specified. Records: {len(df)} (of which {n_empty} with no human theme; the primary analysis excludes them).\n",
         "| band | weighting | micro-F1 | macro-F1 | exact match | Hamming loss | mean Jaccard |",
         "|---|---|---|---|---|---|---|"]
    for band in ["All 2021–2025"] + list(S.BANDS):
        for lab in ("unweighted", "weighted"):
            L.append(f"| {band} | {lab} | " + " | ".join(fmt(band, lab, k) for k in
                     ("micro_F1", "macro_F1", "exact_match", "hamming_loss", "mean_jaccard")) + " |")
    L += ["\nPer-theme precision (all years; recall is unchanged because empty records add no human positives):\n",
          "| theme | precision (unw.) | precision (wt.) |", "|---|---|---|"]
    for t in S.THEMES:
        L.append(f"| {t} | {fmt('All 2021–2025', 'unweighted', f'{t}|precision')} | {fmt('All 2021–2025', 'weighted', f'{t}|precision')} |")
    (out / "theme_scores_posthoc.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
