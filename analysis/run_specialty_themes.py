"""
Step 2.7 (A.4) — Theme inversion by specialty.

Within the A+C subset (5,161 records), for each of the top 8 specialty
buckets, compute year-by-year prevalence of hallucination, regulation, and
safety_clinical themes.

Key question: is the hallucination rise uniform across specialties, or
concentrated in patient-facing LLM-use specialties (Mental Health, Internal
Medicine, Pediatrics)? Same for regulation decline.

Produces:
  output/analyses/themes_by_specialty.csv
  output/figures/themes_by_specialty.png
"""

from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import spearmanr

WORKTREE = Path(__file__).resolve().parents[1]
ANALYSES_DIR = WORKTREE / "output" / "analyses"
FIGURES_DIR = WORKTREE / "output" / "figures"
SPEC_PATH = WORKTREE / "output" / "specialty_classifications.csv"
THEMES_PATH = Path("/Users/kingslywang/repos/ai-narratives-2026/output/analysis/thematic_alarm.csv")

YEARS = list(range(2021, 2027))
THEMES_TO_TRACK = ["hallucination", "regulation", "safety_clinical"]
TOP_N = 8


def has_theme(themes_str: str, theme: str) -> int:
    if not isinstance(themes_str, str):
        return 0
    return int(theme in {t.strip() for t in themes_str.split("|")})


def main() -> None:
    print("Step 2.7 (A.4) — Theme inversion by specialty")
    print("=" * 60)

    themes_df = pd.read_csv(THEMES_PATH, low_memory=False)
    themes_df["pub_year"] = pd.to_numeric(themes_df["pub_year"], errors="coerce").astype("Int64")
    themes_df = themes_df[(themes_df["pub_year"] >= 2021) & (themes_df["pub_year"] <= 2026)].copy()

    spec = pd.read_csv(SPEC_PATH, usecols=["pmid", "specialty"])
    themes_df["pmid"] = themes_df["pmid"].astype(str)
    spec["pmid"] = spec["pmid"].astype(str)
    df = themes_df.merge(spec, on="pmid", how="left")
    df = df[df["specialty"].notna() & (df["specialty"] != "FAILED")].copy()

    for theme in THEMES_TO_TRACK:
        df[theme] = df["themes"].apply(lambda s: has_theme(s, theme))

    print(f"A+C subset with specialty: {len(df):,}")
    spec_counts = df["specialty"].value_counts()
    top = spec_counts.head(TOP_N).index.tolist()
    print(f"\nTop {TOP_N} specialties (within A+C):")
    for s in top:
        print(f"  {s:<40}  n={spec_counts[s]:>4,}")

    long_rows = []
    for s in top:
        sub = df[df["specialty"] == s]
        for year in YEARS:
            year_sub = sub[sub["pub_year"] == year]
            n_year = len(year_sub)
            row = {"specialty": s, "year": year, "n": n_year}
            for theme in THEMES_TO_TRACK:
                row[f"{theme}_pct"] = (year_sub[theme].mean() * 100) if n_year else 0.0
                row[f"{theme}_n"] = int(year_sub[theme].sum())
            long_rows.append(row)
    long_df = pd.DataFrame(long_rows)
    long_df.to_csv(ANALYSES_DIR / "themes_by_specialty.csv", index=False)

    # ── Spearman per (specialty, theme) ───────────────────────────────────────
    print("\nSpearman rho on year vs theme prevalence (per specialty):")
    print(f"  {'specialty':<40} {'hallu_rho':>9} {'reg_rho':>9} {'safety_rho':>11}")
    trend_rows = []
    for s in top:
        sub = long_df[long_df["specialty"] == s].sort_values("year")
        row = {"specialty": s, "n_total": int(sub["n"].sum())}
        for theme in THEMES_TO_TRACK:
            pts = sub[f"{theme}_pct"].values
            rho, p = spearmanr(YEARS, pts)
            row[f"{theme}_rho"] = round(float(rho), 3)
            row[f"{theme}_p"] = round(float(p), 4)
            row[f"{theme}_21"] = round(float(pts[0]), 1)
            row[f"{theme}_26"] = round(float(pts[-1]), 1)
            row[f"{theme}_delta"] = round(float(pts[-1] - pts[0]), 1)
        trend_rows.append(row)
        print(f"  {s:<40} {row['hallucination_rho']:>+8.2f}  {row['regulation_rho']:>+8.2f}  "
              f"{row['safety_clinical_rho']:>+10.2f}")
    pd.DataFrame(trend_rows).to_csv(ANALYSES_DIR / "themes_by_specialty_trends.csv", index=False)

    # ── Headline: is hallucination rise uniform? ──────────────────────────────
    n_rising_hallu = sum(1 for r in trend_rows if r["hallucination_rho"] > 0)
    n_falling_reg = sum(1 for r in trend_rows if r["regulation_rho"] < 0)
    print(f"\nKEY QUESTION — is the theme inversion field-wide?")
    print(f"  Hallucination rising: {n_rising_hallu}/{TOP_N} specialties")
    print(f"  Regulation falling:   {n_falling_reg}/{TOP_N} specialties")

    # ── 3-row figure: rows are themes, cols are specialties ───────────────────
    fig, axes = plt.subplots(3, TOP_N, figsize=(2.2 * TOP_N, 7), sharey="row")
    theme_colors = {
        "hallucination": "#C0392B",
        "regulation": "#2980B9",
        "safety_clinical": "#E67E22",
    }
    theme_labels = {
        "hallucination": "Hallucination",
        "regulation": "Regulation",
        "safety_clinical": "Safety / Clinical",
    }
    for col, s in enumerate(top):
        sub = long_df[long_df["specialty"] == s].sort_values("year")
        for row, theme in enumerate(THEMES_TO_TRACK):
            ax = axes[row, col]
            pts = sub[f"{theme}_pct"].values
            ax.plot(YEARS, pts, "o-", color=theme_colors[theme], lw=1.5, ms=4)
            ax.set_xticks(YEARS)
            ax.set_xticklabels([str(y)[-2:] for y in YEARS], rotation=0, fontsize=7)
            ax.tick_params(axis="y", labelsize=7)
            if row == 0:
                ax.set_title(s, fontsize=8.5, fontweight="bold")
            if col == 0:
                ax.set_ylabel(theme_labels[theme] + " %", fontsize=9)
            rho, p = spearmanr(YEARS, pts)
            sig = "*" if p < 0.05 else ""
            ax.text(0.97, 0.95, f"ρ={rho:+.2f}{sig}", transform=ax.transAxes,
                    ha="right", va="top", fontsize=8, color="#333")
    fig.suptitle(
        "Theme prevalence by year × specialty — A+C subset of v1, 2021–2026\n"
        f"Rows: themes (hallucination, regulation, safety_clinical). Columns: top {TOP_N} specialties.",
        fontsize=11, fontweight="bold", y=1.02,
    )
    fig.tight_layout()
    out_fig = FIGURES_DIR / "themes_by_specialty.png"
    fig.savefig(out_fig, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"\nFigure: {out_fig}")


if __name__ == "__main__":
    main()
