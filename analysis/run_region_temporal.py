"""
Step 3.6 (B.3) — Temporal stance by region.

For the top 5 regions by record count, compute year x critical-rate with
bootstrap CIs (v1), Spearman rho on year vs critical rate per region.
Five-panel small-multiples figure.

Produces:
  output/analyses/temporal_stance_by_region.csv   (long: region, year, point, lo, hi, v1)
  output/figures/temporal_stance_by_region.png
"""

from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import spearmanr

from analysis.robustness import bootstrap_ci, load_classifications

WORKTREE = Path(__file__).resolve().parents[1]
ANALYSES_DIR = WORKTREE / "output" / "analyses"
FIGURES_DIR = WORKTREE / "output" / "figures"
GEO_PATH = WORKTREE / "output" / "geography_classifications.csv"

YEARS = list(range(2021, 2027))
TOP_N = 5


def attach_region(df: pd.DataFrame) -> pd.DataFrame:
    geo = pd.read_csv(GEO_PATH, usecols=["pmid", "region"])
    df = df.copy()
    df["pmid"] = df["pmid"].astype(str)
    geo["pmid"] = geo["pmid"].astype(str)
    return df.merge(geo, on="pmid", how="left")


def critical_pct_by_year(df: pd.DataFrame) -> pd.Series:
    mask = df["stance"].isin(["Alarm", "Caution"])
    out = mask.groupby(df["pub_year"]).mean() * 100
    return out.reindex(YEARS).fillna(0.0)


def main() -> None:
    print("Step 3.6 (B.3) — Temporal stance by region")
    print("=" * 60)

    v1 = attach_region(load_classifications("v1"))
    v1 = v1[v1["region"] != "Unknown"].copy()

    region_counts = v1["region"].value_counts()
    top_regions = region_counts.head(TOP_N).index.tolist()
    print(f"Top {TOP_N} regions by count:")
    for r in top_regions:
        print(f"  {r:<32} n={region_counts[r]:>5,}")

    # Bootstrap CIs per region
    per_region: dict[str, dict] = {}
    trend_rows = []
    for region in top_regions:
        sub = v1[v1["region"] == region].copy()
        boot = bootstrap_ci(sub, critical_pct_by_year)
        per_region[region] = boot
        pts = boot["point"].values
        rho, p = spearmanr(YEARS, pts)
        d_21_26 = float(pts[-1] - pts[0])
        trend_rows.append({
            "region": region, "n": len(sub),
            "spearman_rho": round(float(rho), 4),
            "p_value": round(float(p), 5),
            "y_2021": round(float(pts[0]), 2),
            "y_2026": round(float(pts[-1]), 2),
            "delta_pp_2021_to_2026": round(d_21_26, 2),
        })

    # Long-format CSV
    long_rows = []
    for region in top_regions:
        boot = per_region[region]
        for year in YEARS:
            long_rows.append({
                "region": region, "year": year,
                "critical_pct": round(float(boot["point"][year]), 4),
                "ci_lower": round(float(boot["lower"][year]), 4),
                "ci_upper": round(float(boot["upper"][year]), 4),
            })
    pd.DataFrame(long_rows).to_csv(ANALYSES_DIR / "temporal_stance_by_region.csv", index=False)
    pd.DataFrame(trend_rows).to_csv(ANALYSES_DIR / "temporal_stance_by_region_trends.csv", index=False)

    # ── Headline: is the post-ChatGPT critical shift global or regional? ──────
    print("\nSpearman trend tests (v1, year vs critical %):")
    for r in trend_rows:
        sig = "**" if r["p_value"] < 0.01 else "*" if r["p_value"] < 0.05 else ""
        print(f"  {r['region']:<32}  rho={r['spearman_rho']:+.3f}{sig}  "
              f"p={r['p_value']:.4f}  Δ={r['delta_pp_2021_to_2026']:+.2f}pp "
              f"({r['y_2021']:.1f}→{r['y_2026']:.1f}%)")

    n_rising = sum(1 for r in trend_rows if r["spearman_rho"] > 0)
    n_significant_rising = sum(1 for r in trend_rows
                                if r["spearman_rho"] > 0 and r["p_value"] < 0.05)
    print(f"\nKEY QUESTION — global vs regional post-ChatGPT critical shift?")
    print(f"  Rising trends: {n_rising}/{TOP_N} regions")
    print(f"  Significant rising (p<0.05): {n_significant_rising}/{TOP_N} regions")

    # ── Figure: 5-panel small-multiples ───────────────────────────────────────
    fig, axes = plt.subplots(1, TOP_N, figsize=(18, 4), sharey=True)
    for ax, region in zip(axes, top_regions):
        boot = per_region[region]
        pts = boot["point"].values
        lo = boot["lower"].values
        hi = boot["upper"].values
        ax.fill_between(YEARS, lo, hi, alpha=0.18, color="#C0392B", linewidth=0)
        ax.plot(YEARS, pts, "o-", color="#C0392B", lw=1.7, ms=5)
        ax.set_title(region, fontsize=10, fontweight="bold")
        ax.set_xticks(YEARS)
        ax.set_xticklabels([str(y) if y != 2026 else "26*" for y in YEARS],
                            rotation=45, fontsize=8)
        ax.tick_params(axis="y", labelsize=8)
        ax.set_ylim(0, max(60, hi.max() + 5))
        rho, p = spearmanr(YEARS, pts)
        sig = "**" if p < 0.01 else "*" if p < 0.05 else ""
        ax.text(0.97, 0.95, f"ρ={rho:+.2f}{sig}", transform=ax.transAxes,
                ha="right", va="top", fontsize=9, color="#333")
        n = sum(1 for _ in range(1))  # placeholder; show n in title via inset
        n_region = int((v1["region"] == region).sum())
        ax.text(0.03, 0.95, f"n={n_region:,}", transform=ax.transAxes,
                ha="left", va="top", fontsize=8, color="#666")
    axes[0].set_ylabel("% Critical (Alarm + Caution)", fontsize=10)
    fig.suptitle(
        "Critical stance by year across top 5 regions — Q1/Q2 medical, 2021–2026\n"
        f"(v1, bootstrap 95% CI, n_boot=1000). * 2026 partial year (Jan–Apr).",
        fontsize=11, fontweight="bold", y=1.05,
    )
    fig.tight_layout()
    out_fig = FIGURES_DIR / "temporal_stance_by_region.png"
    fig.savefig(out_fig, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"\nFigure: {out_fig}")


if __name__ == "__main__":
    main()
