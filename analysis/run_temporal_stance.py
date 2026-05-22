"""
Task 3.1 — Year x stance temporal trend.

Produces:
  output/analyses/temporal_stance_v1.csv
  output/analyses/temporal_stance_v2.csv
  output/analyses/temporal_stance_robustness.md
  output/analyses/temporal_stance_trends.csv   (Spearman per stance, v1)
  output/figures/temporal_stance.png            (5-panel, 300 dpi)
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import spearmanr

from analysis.robustness import (
    STANCES,
    bootstrap_ci,
    dual_analysis,
    load_classifications,
)

WORKTREE = Path(__file__).resolve().parents[1]
ANALYSES_DIR = WORKTREE / "output" / "analyses"
FIGURES_DIR = WORKTREE / "output" / "figures"
ANALYSES_DIR.mkdir(parents=True, exist_ok=True)
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

STANCE_COLOURS = {
    "Alarm": "#C0392B",
    "Caution": "#E67E22",
    "Neutral": "#95A5A6",
    "Cautious Optimism": "#27AE60",
    "Advocacy": "#2980B9",
}

YEARS = list(range(2021, 2027))  # 2021–2026 inclusive


def stance_pct_by_year(df: pd.DataFrame) -> pd.DataFrame:
    """Return year (rows) x stance (cols) DataFrame of percentages."""
    ct = pd.crosstab(df["pub_year"], df["stance"], normalize="index") * 100
    return ct.reindex(index=YEARS, columns=STANCES).fillna(0.0)


def main() -> None:
    print("Task 3.1 — Year x stance temporal trend")
    print("=" * 60)

    v1 = load_classifications("v1")
    v2 = load_classifications("v2")
    print(f"v1: {len(v1):,} records; v2: {len(v2):,}")

    # ── Dual analysis: bootstrap CIs on year x stance percentages ──────────
    result = dual_analysis(
        stance_pct_by_year,
        agg_name="temporal_stance",
        output_dir=ANALYSES_DIR,
        v1_df=v1,
        v2_df=v2,
        tolerance_pp=3.0,
    )

    boot_v1 = result["v1_result"]
    boot_v2 = result["v2_result"]
    verdict = result["verdict"]

    # ── Spearman trend tests (v1), per stance + combined critical ──────────
    trend_rows = []
    for stance in STANCES:
        pts = boot_v1["point"][stance].values
        rho, p = spearmanr(YEARS, pts)
        trend_rows.append(
            {
                "label": stance,
                "spearman_rho": round(float(rho), 4),
                "p_value": round(float(p), 5),
                "direction": "rising" if rho > 0 else "falling" if rho < 0 else "flat",
                "y_2021": round(float(boot_v1["point"][stance].loc[2021]), 2),
                "y_2026": round(float(boot_v1["point"][stance].loc[2026]), 2),
                "delta_pp_2021_to_2026": round(
                    float(boot_v1["point"][stance].loc[2026] - boot_v1["point"][stance].loc[2021]),
                    2,
                ),
            }
        )
    # Critical = Alarm + Caution combined
    crit = boot_v1["point"]["Alarm"] + boot_v1["point"]["Caution"]
    rho, p = spearmanr(YEARS, crit.values)
    trend_rows.append(
        {
            "label": "Critical (Alarm+Caution)",
            "spearman_rho": round(float(rho), 4),
            "p_value": round(float(p), 5),
            "direction": "rising" if rho > 0 else "falling" if rho < 0 else "flat",
            "y_2021": round(float(crit.loc[2021]), 2),
            "y_2026": round(float(crit.loc[2026]), 2),
            "delta_pp_2021_to_2026": round(float(crit.loc[2026] - crit.loc[2021]), 2),
        }
    )
    trends = pd.DataFrame(trend_rows)
    trends.to_csv(ANALYSES_DIR / "temporal_stance_trends.csv", index=False)

    print("\nSpearman trend tests (v1, year vs %):")
    for r in trend_rows:
        print(
            f"  {r['label']:<26} rho={r['spearman_rho']:+.3f}  "
            f"p={r['p_value']:.4f}  Δ={r['delta_pp_2021_to_2026']:+.2f}pp  "
            f"({r['y_2021']:.1f}→{r['y_2026']:.1f}%)"
        )

    # ── Same Spearman on v2 for comparison (printed only) ──────────────────
    print("\nSame test on v2 (for direction comparison):")
    v2_trends = []
    for stance in STANCES:
        pts = boot_v2["point"][stance].values
        rho, p = spearmanr(YEARS, pts)
        v2_trends.append((stance, rho, p))
        print(f"  {stance:<26} rho={rho:+.3f}  p={p:.4f}")
    crit_v2 = boot_v2["point"]["Alarm"] + boot_v2["point"]["Caution"]
    rho_c2, p_c2 = spearmanr(YEARS, crit_v2.values)
    v2_trends.append(("Critical (Alarm+Caution)", rho_c2, p_c2))
    print(f"  {'Critical (Alarm+Caution)':<26} rho={rho_c2:+.3f}  p={p_c2:.4f}  "
          f"({crit_v2.loc[2021]:.1f}→{crit_v2.loc[2026]:.1f}%)")

    # ── Figure: 5-panel, one per stance ────────────────────────────────────
    fig, axes = plt.subplots(1, 5, figsize=(18, 4), sharey=False)
    for ax, stance in zip(axes, STANCES):
        pts = boot_v1["point"][stance].values
        lo = boot_v1["lower"][stance].values
        hi = boot_v1["upper"][stance].values
        yerr = np.array([pts - lo, hi - pts])
        ax.bar(
            YEARS,
            pts,
            color=STANCE_COLOURS[stance],
            alpha=0.85,
            edgecolor="white",
            yerr=yerr,
            error_kw={"lw": 1.0, "capsize": 3, "ecolor": "#333"},
        )
        # v2 overlay
        v2_pts = boot_v2["point"][stance].values
        ax.plot(YEARS, v2_pts, "o-", color="#444", lw=1.0, ms=3.5, alpha=0.65,
                label="v2 (robustness)")
        ax.set_title(stance, fontsize=11, fontweight="bold")
        ax.set_xticks(YEARS)
        ax.set_xticklabels([str(y) if y != 2026 else "2026*" for y in YEARS],
                            rotation=45, fontsize=9)
        ax.tick_params(axis="y", labelsize=9)
        rho, p = spearmanr(YEARS, pts)
        sig = "**" if p < 0.01 else "*" if p < 0.05 else ""
        ax.text(
            0.98, 0.95, f"ρ={rho:+.2f}{sig}", transform=ax.transAxes,
            ha="right", va="top", fontsize=9, color="#333",
        )
    axes[0].set_ylabel("% of records", fontsize=10)
    axes[-1].legend(loc="upper right", fontsize=8, framealpha=0.9)
    fig.suptitle(
        "Stance distribution by year — Q1/Q2 medical journals, 2021–2026\n"
        "(v1 bars with bootstrap 95% CI, n_boot=1000; v2 overlay as line). "
        "* 2026 partial year (Jan–Apr).",
        fontsize=11, fontweight="bold", y=1.05,
    )
    fig.tight_layout()
    out_fig = FIGURES_DIR / "temporal_stance.png"
    fig.savefig(out_fig, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"\nFigure: {out_fig}")

    # ── Headline summary ───────────────────────────────────────────────────
    # Substantive headline = largest |delta in pp| with p<0.1, excluding the
    # combined critical (printed separately to avoid double-counting Alarm+Caution).
    candidates = [r for r in trend_rows if r["label"] != "Critical (Alarm+Caution)"
                  and r["p_value"] < 0.1]
    candidates.sort(key=lambda r: abs(r["delta_pp_2021_to_2026"]), reverse=True)
    head = candidates[0] if candidates else trend_rows[0]
    v2_match = next(r for r in v2_trends if r[0] == head["label"])
    v2_dir = "same" if v2_match[1] * head["spearman_rho"] > 0 else "opposite"
    print(
        f"\nHEADLINE (per-stance): {head['label']} {head['direction']}, "
        f"rho={head['spearman_rho']:+.3f}, p={head['p_value']:.4f}, "
        f"Δ={head['delta_pp_2021_to_2026']:+.2f}pp ({head['y_2021']:.1f}→{head['y_2026']:.1f}%); "
        f"v2 direction {v2_dir} (rho={v2_match[1]:+.3f})"
    )
    crit_row = next(r for r in trend_rows if r["label"] == "Critical (Alarm+Caution)")
    crit_v2_match = next(r for r in v2_trends if r[0] == "Critical (Alarm+Caution)")
    crit_v2_dir = ("same" if crit_v2_match[1] * crit_row["spearman_rho"] > 0
                    else "opposite")
    print(
        f"HEADLINE (combined critical): rho={crit_row['spearman_rho']:+.3f}, "
        f"p={crit_row['p_value']:.4f}, Δ={crit_row['delta_pp_2021_to_2026']:+.2f}pp "
        f"({crit_row['y_2021']:.1f}→{crit_row['y_2026']:.1f}%); "
        f"v2 direction {crit_v2_dir} (rho={crit_v2_match[1]:+.3f})"
    )

    print(f"\nVerdict summary: {verdict['summary']}")
    print("Files:", [str(f.relative_to(WORKTREE)) for f in result["files"]])


if __name__ == "__main__":
    main()
