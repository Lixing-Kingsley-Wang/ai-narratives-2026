"""
Step 3.5 (B.2) — Critical rate by region.

Joins geography_classifications.csv onto v1/v2 stance frames by pmid, then
runs the same dual_analysis pattern as Session 1: bootstrap 95% CI per
region, v1/v2 robustness verdict, horizontal bar chart sorted by critical
rate.

Produces:
  output/analyses/region_critical_v1.csv
  output/analyses/region_critical_v2.csv
  output/analyses/region_critical_robustness.md
  output/figures/region_critical.png
"""

from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from analysis.robustness import (
    bootstrap_ci,
    dual_analysis,
    load_classifications,
)

WORKTREE = Path(__file__).resolve().parents[1]
ANALYSES_DIR = WORKTREE / "output" / "analyses"
FIGURES_DIR = WORKTREE / "output" / "figures"
GEO_PATH = WORKTREE / "output" / "geography_classifications.csv"
ANALYSES_DIR.mkdir(parents=True, exist_ok=True)
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

REGIONS_ORDER = [
    "North America",
    "Western Europe",
    "East Asia",
    "Middle East / North Africa",
    "South/Southeast Asia",
    "Latin America / Oceania",
    "Eastern Europe",
    "Sub-Saharan Africa",
    "Unknown",
]


def attach_region(df: pd.DataFrame) -> pd.DataFrame:
    geo = pd.read_csv(GEO_PATH, usecols=["pmid", "region"])
    # pmids are stringified in geo but may be int-cast in df — normalize
    df = df.copy()
    df["pmid"] = df["pmid"].astype(str)
    geo["pmid"] = geo["pmid"].astype(str)
    return df.merge(geo, on="pmid", how="left")


def critical_by_region(df: pd.DataFrame) -> pd.Series:
    """Series: region → % of records with stance in {Alarm, Caution}."""
    mask = df["stance"].isin(["Alarm", "Caution"])
    out = mask.groupby(df["region"]).mean() * 100
    return out.reindex(REGIONS_ORDER).fillna(0.0)


def main() -> None:
    print("Step 3.5 (B.2) — Critical rate by region")
    print("=" * 60)

    v1 = attach_region(load_classifications("v1"))
    v2 = attach_region(load_classifications("v2"))
    print(f"v1: {len(v1):,} records; v2: {len(v2):,}")
    print(f"v1 region counts:\n{v1['region'].value_counts().reindex(REGIONS_ORDER).fillna(0).astype(int)}\n")

    result = dual_analysis(
        critical_by_region,
        agg_name="region_critical",
        output_dir=ANALYSES_DIR,
        v1_df=v1,
        v2_df=v2,
        tolerance_pp=3.0,
    )

    boot_v1 = result["v1_result"]
    boot_v2 = result["v2_result"]

    # ── Headline: most/least critical regions ─────────────────────────────────
    pts = boot_v1["point"].copy()
    pts_for_rank = pts.drop("Unknown", errors="ignore").sort_values(ascending=False)
    print("\nCritical rate (Alarm + Caution) by region — v1 with 95% CI:")
    for region in pts_for_rank.index:
        lo = boot_v1["lower"][region]; hi = boot_v1["upper"][region]
        n_region = int((v1["region"] == region).sum())
        v2_pt = boot_v2["point"].get(region, np.nan)
        delta = v2_pt - pts[region] if not np.isnan(v2_pt) else np.nan
        print(f"  {region:<32} n={n_region:>5,}  {pts[region]:5.1f}% ({lo:5.1f}–{hi:5.1f})  "
              f"v2={v2_pt:5.1f}  Δ={delta:+.2f}pp")
    n_unk = int((v1["region"] == "Unknown").sum())
    if n_unk:
        print(f"  Unknown                          n={n_unk:>5,}  "
              f"{pts['Unknown']:5.1f}% (excluded from headline)")

    top3 = pts_for_rank.head(3)
    bot3 = pts_for_rank.tail(3)
    print(f"\nTOP 3 most critical: {', '.join(f'{r} ({v:.1f}%)' for r, v in top3.items())}")
    print(f"TOP 3 least critical: {', '.join(f'{r} ({v:.1f}%)' for r, v in bot3.items())}")

    # ── Figure: horizontal bar chart sorted by critical rate ──────────────────
    plot_data = pts.drop("Unknown", errors="ignore").sort_values()
    regions = plot_data.index.tolist()
    point = plot_data.values
    lo = np.array([boot_v1["lower"][r] for r in regions])
    hi = np.array([boot_v1["upper"][r] for r in regions])
    xerr = np.array([point - lo, hi - point])

    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.barh(regions, point, xerr=xerr, color="#C0392B", alpha=0.85,
                    edgecolor="white",
                    error_kw={"lw": 1.0, "capsize": 3, "ecolor": "#333"})
    # v2 overlay as black dots
    v2_pts = np.array([boot_v2["point"].get(r, 0) for r in regions])
    ax.plot(v2_pts, regions, "o", color="#222", ms=5, alpha=0.7, label="v2 (robustness)")

    for bar, p in zip(bars, point):
        ax.text(p + 1.5, bar.get_y() + bar.get_height()/2, f"{p:.1f}%",
                va="center", fontsize=9, color="#333")

    ax.set_xlabel("% Critical (Alarm + Caution)", fontsize=10)
    ax.set_xlim(0, max(hi.max() + 8, 50))
    ax.legend(loc="lower right", fontsize=9, framealpha=0.9)
    ax.set_title(
        "Critical stance by region (first-author affiliation) — v1 bars w/ bootstrap 95% CI\n"
        f"Q1/Q2 medical, 2021–2026, n={len(v1):,}; v2 overlay as black dots; Unknown excluded.",
        fontsize=10, fontweight="bold",
    )
    fig.tight_layout()
    out_fig = FIGURES_DIR / "region_critical.png"
    fig.savefig(out_fig, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"\nFigure: {out_fig}")
    print(f"Files: {[str(f.relative_to(WORKTREE)) for f in result['files']]}")


if __name__ == "__main__":
    main()
