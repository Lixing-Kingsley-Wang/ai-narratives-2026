"""
Step 2.6 (A.3) — Temporal stance by specialty.

For the top 8 specialties by count, compute year x critical-rate with
bootstrap CIs (v1), Spearman rho on year vs critical rate per specialty.
Eight-panel small-multiples figure (2x4 grid).

Produces:
  output/analyses/temporal_stance_by_specialty.csv
  output/analyses/temporal_stance_by_specialty_trends.csv
  output/figures/temporal_stance_by_specialty.png
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
SPEC_PATH = WORKTREE / "output" / "specialty_classifications.csv"

YEARS = list(range(2021, 2027))
TOP_N = 8


def attach_specialty(df: pd.DataFrame) -> pd.DataFrame:
    spec = pd.read_csv(SPEC_PATH, usecols=["pmid", "specialty"])
    df = df.copy()
    df["pmid"] = df["pmid"].astype(str)
    spec["pmid"] = spec["pmid"].astype(str)
    return df.merge(spec, on="pmid", how="left")


def critical_pct_by_year(df: pd.DataFrame) -> pd.Series:
    mask = df["stance"].isin(["Alarm", "Caution"])
    return (mask.groupby(df["pub_year"]).mean() * 100).reindex(YEARS).fillna(0.0)


def main() -> None:
    print("Step 2.6 (A.3) — Temporal stance by specialty")
    print("=" * 60)

    v1 = attach_specialty(load_classifications("v1"))
    v1 = v1[v1["specialty"].notna() & (v1["specialty"] != "FAILED")].copy()

    specialty_counts = v1["specialty"].value_counts()
    top = specialty_counts.head(TOP_N).index.tolist()
    print(f"Top {TOP_N} specialties:")
    for s in top:
        print(f"  {s:<40}  n={specialty_counts[s]:>5,}")

    per_spec, trend_rows, long_rows = {}, [], []
    for s in top:
        sub = v1[v1["specialty"] == s].copy()
        boot = bootstrap_ci(sub, critical_pct_by_year)
        per_spec[s] = boot
        pts = boot["point"].values
        rho, p = spearmanr(YEARS, pts)
        trend_rows.append({
            "specialty": s, "n": len(sub),
            "spearman_rho": round(float(rho), 4),
            "p_value": round(float(p), 5),
            "y_2021": round(float(pts[0]), 2),
            "y_2026": round(float(pts[-1]), 2),
            "delta_pp_2021_to_2026": round(float(pts[-1] - pts[0]), 2),
        })
        for year in YEARS:
            long_rows.append({
                "specialty": s, "year": year,
                "critical_pct": round(float(boot["point"][year]), 4),
                "ci_lower": round(float(boot["lower"][year]), 4),
                "ci_upper": round(float(boot["upper"][year]), 4),
            })

    pd.DataFrame(long_rows).to_csv(ANALYSES_DIR / "temporal_stance_by_specialty.csv", index=False)
    pd.DataFrame(trend_rows).to_csv(ANALYSES_DIR / "temporal_stance_by_specialty_trends.csv", index=False)

    print("\nSpearman trend tests (v1, year vs critical %):")
    for r in trend_rows:
        sig = "**" if r["p_value"] < 0.01 else "*" if r["p_value"] < 0.05 else ""
        print(f"  {r['specialty']:<40}  rho={r['spearman_rho']:+.3f}{sig}  "
              f"p={r['p_value']:.4f}  Δ={r['delta_pp_2021_to_2026']:+.2f}pp "
              f"({r['y_2021']:.1f}→{r['y_2026']:.1f}%)")

    n_rising = sum(1 for r in trend_rows if r["spearman_rho"] > 0)
    n_sig_rising = sum(1 for r in trend_rows if r["spearman_rho"] > 0 and r["p_value"] < 0.05)
    print(f"\nKEY QUESTION — is the post-ChatGPT critical shift field-wide?")
    print(f"  Rising trends: {n_rising}/{TOP_N} specialties")
    print(f"  Significant rising (p<0.05): {n_sig_rising}/{TOP_N} specialties")

    # ── 2x4 figure ────────────────────────────────────────────────────────────
    fig, axes = plt.subplots(2, 4, figsize=(18, 8), sharey=True)
    axes = axes.flatten()
    for ax, s in zip(axes, top):
        boot = per_spec[s]
        pts = boot["point"].values
        lo = boot["lower"].values
        hi = boot["upper"].values
        ax.fill_between(YEARS, lo, hi, alpha=0.18, color="#C0392B", linewidth=0)
        ax.plot(YEARS, pts, "o-", color="#C0392B", lw=1.7, ms=5)
        ax.set_title(s, fontsize=9.5, fontweight="bold")
        ax.set_xticks(YEARS)
        ax.set_xticklabels([str(y) if y != 2026 else "26*" for y in YEARS],
                            rotation=45, fontsize=8)
        ax.tick_params(axis="y", labelsize=8)
        ax.set_ylim(0, max(60, hi.max() + 5))
        rho, p = spearmanr(YEARS, pts)
        sig = "**" if p < 0.01 else "*" if p < 0.05 else ""
        ax.text(0.97, 0.95, f"ρ={rho:+.2f}{sig}", transform=ax.transAxes,
                ha="right", va="top", fontsize=9, color="#333")
        ax.text(0.03, 0.95, f"n={specialty_counts[s]:,}", transform=ax.transAxes,
                ha="left", va="top", fontsize=8, color="#666")
    axes[0].set_ylabel("% Critical", fontsize=10)
    axes[4].set_ylabel("% Critical", fontsize=10)
    fig.suptitle(
        "Critical stance by year across top 8 specialties — Q1/Q2 medical, 2021–2026\n"
        f"v1 with bootstrap 95% CI, n_boot=1000. * 2026 partial year (Jan–Apr).",
        fontsize=11, fontweight="bold", y=1.02,
    )
    fig.tight_layout()
    out_fig = FIGURES_DIR / "temporal_stance_by_specialty.png"
    fig.savefig(out_fig, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"\nFigure: {out_fig}")


if __name__ == "__main__":
    main()
