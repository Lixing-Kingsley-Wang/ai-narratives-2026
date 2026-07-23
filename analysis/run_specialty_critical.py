"""
Step 2.5 (A.2) — Critical rate by specialty.

Joins specialty_classifications.csv onto v1/v2 stance frames by pmid.
Bootstrap 95% CI per specialty, v1/v2 robustness verdict, horizontal bar
chart sorted by critical rate.

Produces:
  output/analyses/specialty_critical_v1.csv
  output/analyses/specialty_critical_v2.csv
  output/analyses/specialty_critical_robustness.md
  output/figures/specialty_critical.png
"""

from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from analysis.robustness import dual_analysis, load_classifications

WORKTREE = Path(__file__).resolve().parents[1]
ANALYSES_DIR = WORKTREE / "output" / "analyses"
FIGURES_DIR = WORKTREE / "output" / "figures"
SPEC_PATH = WORKTREE / "output" / "specialty_classifications.csv"

# Plot order — set by descending count by default; sorted in plot.
ALL_SPECIALTIES = [
    "Radiology / Diagnostic Imaging",
    "Pathology / Laboratory Medicine",
    "Cardiology",
    "Oncology",
    "Surgery",
    "Ophthalmology",
    "Dermatology",
    "Neurology / Neuroscience",
    "Mental Health / Psychiatry",
    "Internal Medicine / Primary Care",
    "Emergency Medicine / Critical Care",
    "Pediatrics",
    "Obstetrics / Gynecology",
    "Dentistry",
    "Medical Informatics / Digital Health",
    "Nursing",
    "Medical Education",
    "Multidisciplinary / Other",
]


def attach_specialty(df: pd.DataFrame) -> pd.DataFrame:
    spec = pd.read_csv(SPEC_PATH, usecols=["pmid", "specialty"])
    df = df.copy()
    df["pmid"] = df["pmid"].astype(str)
    spec["pmid"] = spec["pmid"].astype(str)
    return df.merge(spec, on="pmid", how="left")


def critical_by_specialty(df: pd.DataFrame) -> pd.Series:
    mask = df["stance"].isin(["Alarm", "Caution"])
    out = mask.groupby(df["specialty"]).mean() * 100
    return out.reindex(ALL_SPECIALTIES).fillna(0.0)


def main() -> None:
    print("Step 2.5 (A.2) — Critical rate by specialty")
    print("=" * 60)

    v1 = attach_specialty(load_classifications("v1"))
    v2 = attach_specialty(load_classifications("v2"))
    print(f"v1: {len(v1):,} records; v2: {len(v2):,}")
    print(f"v1 specialty counts (top to bottom):")
    counts = v1["specialty"].value_counts().reindex(ALL_SPECIALTIES).fillna(0).astype(int)
    for s, n in counts.items():
        print(f"  {s:<40}  n={n:,}")
    n_unclassified = v1["specialty"].isna().sum() + (v1["specialty"] == "FAILED").sum()
    print(f"  (unclassified / FAILED: {n_unclassified:,})")

    result = dual_analysis(
        critical_by_specialty,
        agg_name="specialty_critical",
        output_dir=ANALYSES_DIR,
        v1_df=v1,
        v2_df=v2,
        tolerance_pp=3.0,
    )

    boot_v1 = result["v1_result"]
    boot_v2 = result["v2_result"]
    pts = boot_v1["point"]

    # Drop near-empty cells (n < 30) from the headline, but keep them in CSV.
    rare = [s for s in ALL_SPECIALTIES if counts[s] < 30]
    for s in rare:
        print(f"  excluding {s!r} from headline (n={counts[s]}<30)")
    keep = [s for s in ALL_SPECIALTIES if counts[s] >= 30]
    ranked = pts.reindex(keep).sort_values(ascending=False)

    print("\nCritical rate (Alarm + Caution) by specialty — v1 with 95% CI:")
    for s in ranked.index:
        lo = boot_v1["lower"][s]; hi = boot_v1["upper"][s]
        v2_pt = boot_v2["point"].get(s, np.nan)
        delta = v2_pt - pts[s] if not np.isnan(v2_pt) else np.nan
        print(f"  {s:<40} n={counts[s]:>5,}  {pts[s]:5.1f}% ({lo:5.1f}–{hi:5.1f})  "
              f"v2={v2_pt:5.1f}  Δ={delta:+.2f}pp")

    print(f"\nTOP 3 most critical: {', '.join(f'{s} ({v:.1f}%)' for s, v in ranked.head(3).items())}")
    print(f"TOP 3 least critical: {', '.join(f'{s} ({v:.1f}%)' for s, v in ranked.tail(3).items())}")

    # ── Figure: horizontal bar sorted by critical rate ────────────────────────
    plot_specs = ranked.sort_values().index.tolist()
    point = ranked.sort_values().values
    lo = np.array([boot_v1["lower"][s] for s in plot_specs])
    hi = np.array([boot_v1["upper"][s] for s in plot_specs])
    xerr = np.array([point - lo, hi - point])

    fig, ax = plt.subplots(figsize=(10, 6.5))
    ax.barh(plot_specs, point, xerr=xerr, color="#C0392B", alpha=0.85,
            edgecolor="white", error_kw={"lw": 1.0, "capsize": 3, "ecolor": "#333"})
    v2_pts = np.array([boot_v2["point"].get(s, 0) for s in plot_specs])
    ax.plot(v2_pts, plot_specs, "o", color="#222", ms=5, alpha=0.7, label="v2 (robustness)")
    for i, (s, p) in enumerate(zip(plot_specs, point)):
        ax.text(p + 1.5, i, f"{p:.1f}% (n={counts[s]:,})",
                va="center", fontsize=8, color="#333")
    ax.set_xlabel("% Critical (Alarm + Caution)", fontsize=10)
    ax.set_xlim(0, max(hi.max() + 12, 60))
    ax.legend(loc="lower right", fontsize=9, framealpha=0.9)
    ax.set_title(
        f"Critical stance by clinical specialty — v1 bars w/ bootstrap 95% CI\n"
        f"Q1/Q2 medical, 2021–2026, n={int(counts[keep].sum()):,}; rare specialties (n<30) excluded.",
        fontsize=10, fontweight="bold",
    )
    fig.tight_layout()
    out_fig = FIGURES_DIR / "specialty_critical.png"
    fig.savefig(out_fig, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"\nFigure: {out_fig}")
    print(f"Files: {[str(f.relative_to(WORKTREE)) for f in result['files']]}")


if __name__ == "__main__":
    main()
