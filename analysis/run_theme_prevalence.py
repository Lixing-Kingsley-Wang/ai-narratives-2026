"""
Task 3.3 — Theme prevalence over time, restricted to v1 Alarm+Caution.

Themes can co-occur per paper, so per-year % is computed as
(papers flagged with theme T in year Y) / (Alarm+Caution papers in Y) × 100.

v2 has no theme classifications — robustness not assessed (per brief).

Produces:
  output/analyses/theme_prevalence_v1.csv
  output/analyses/theme_prevalence_trends.csv  (Spearman year vs prevalence)
  output/analyses/theme_prevalence_summary.md
  output/figures/theme_prevalence.png            (line chart, 300 dpi)
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
    SEED,
    THEMES_PATH,
    bootstrap_ci,
    load_classifications,
)

WORKTREE = Path(__file__).resolve().parents[1]
ANALYSES_DIR = WORKTREE / "output" / "analyses"
FIGURES_DIR = WORKTREE / "output" / "figures"

YEARS = list(range(2021, 2027))

THEME_ORDER = [
    "safety_clinical",
    "hallucination",
    "regulation",
    "ethics_bias",
    "education",
    "data_privacy",
    "cognitive",
    "existential",
    "replacement",
    "other",
]
THEME_LABELS = {
    "safety_clinical": "Patient safety",
    "hallucination": "Hallucination / errors",
    "regulation": "Governance / regulation",
    "ethics_bias": "Ethics & bias",
    "education": "Medical education",
    "data_privacy": "Data privacy",
    "cognitive": "Cognitive offloading",
    "existential": "Existential threat",
    "replacement": "Replacement fears",
    "other": "Other",
}
# Distinct colour per theme
THEME_COLOURS = dict(
    zip(THEME_ORDER, plt.cm.tab10(np.linspace(0, 1, len(THEME_ORDER))))
)


def load_themes_v1_alarm_caution() -> pd.DataFrame:
    """Join themes file with v1 (already pre-filtered to A+C); explode themes."""
    th = pd.read_csv(THEMES_PATH, low_memory=False)
    # Restrict to year window for consistency with other analyses
    th = th[(th["pub_year"] >= YEARS[0]) & (th["pub_year"] <= YEARS[-1])].copy()
    # One row per (pmid, theme) with all theme columns broken out as boolean
    for t in THEME_ORDER:
        th[f"has_{t}"] = th["themes"].fillna("").str.split("|").apply(
            lambda lst: t in lst
        )
    return th


def theme_prevalence_by_year(df: pd.DataFrame) -> pd.DataFrame:
    """% of A+C papers per year flagged with each theme. Year x theme."""
    rows = []
    for yr in YEARS:
        sub = df[df["pub_year"] == yr]
        n = len(sub)
        if n == 0:
            rows.append({t: 0.0 for t in THEME_ORDER})
        else:
            rows.append({t: sub[f"has_{t}"].mean() * 100 for t in THEME_ORDER})
    out = pd.DataFrame(rows, index=YEARS)[THEME_ORDER]
    out.index.name = "pub_year"
    return out


def main() -> None:
    print("Task 3.3 — Theme prevalence over time (v1 Alarm+Caution only)")
    print("=" * 60)

    df = load_themes_v1_alarm_caution()
    print(f"v1 Alarm+Caution records (2021-2026): {len(df):,}")
    print(f"  by year: {df['pub_year'].value_counts().sort_index().to_dict()}")

    # Point estimates
    pt = theme_prevalence_by_year(df)
    print("\nTheme prevalence (%) by year:")
    print(pt.round(1).to_string())

    # Bootstrap CIs (frame agg)
    print(f"\nBootstrapping (n=1000, seed={SEED})...")
    boot = bootstrap_ci(df, theme_prevalence_by_year, n_boot=1000)
    print("Done.")

    # Save v1 result (long form)
    pt_long = boot["point"].stack(future_stack=True).rename("point")
    lo_long = boot["lower"].stack(future_stack=True).rename("ci_lower")
    hi_long = boot["upper"].stack(future_stack=True).rename("ci_upper")
    long_df = pd.concat([pt_long, lo_long, hi_long], axis=1).reset_index()
    long_df.columns = ["pub_year", "theme", "point", "ci_lower", "ci_upper"]
    long_df.to_csv(ANALYSES_DIR / "theme_prevalence_v1.csv", index=False)

    # Overall prevalence (whole period) — rank
    overall = (
        df[[f"has_{t}" for t in THEME_ORDER]].mean() * 100
    ).round(2).rename(lambda c: c.replace("has_", ""))
    overall = overall.sort_values(ascending=False)
    print("\nOverall prevalence (whole 2021-2026 A+C corpus):")
    print(overall.to_string())

    # Spearman trends per theme
    trends = []
    for t in THEME_ORDER:
        vals = boot["point"][t].values
        rho, p = spearmanr(YEARS, vals)
        trends.append(
            {
                "theme": t,
                "label": THEME_LABELS[t],
                "spearman_rho": round(float(rho), 4),
                "p_value": round(float(p), 5),
                "direction": "rising" if rho > 0 else "falling" if rho < 0 else "flat",
                "y_2021": round(float(boot["point"][t].loc[2021]), 2),
                "y_2026": round(float(boot["point"][t].loc[2026]), 2),
                "delta_pp_2021_to_2026": round(
                    float(boot["point"][t].loc[2026] - boot["point"][t].loc[2021]),
                    2,
                ),
                "overall_pct": round(float(overall[t]), 2),
            }
        )
    trends_df = pd.DataFrame(trends).sort_values("overall_pct", ascending=False)
    trends_df.to_csv(ANALYSES_DIR / "theme_prevalence_trends.csv", index=False)

    print("\nPer-theme Spearman trend tests:")
    for r in trends_df.to_dict(orient="records"):
        print(
            f"  {r['label']:<26} overall {r['overall_pct']:>5.1f}%   "
            f"rho={r['spearman_rho']:+.3f}  p={r['p_value']:.4f}  "
            f"Δ={r['delta_pp_2021_to_2026']:+.2f}pp  ({r['y_2021']:.1f}→{r['y_2026']:.1f}%)"
        )

    # Markdown summary
    md = [
        "# Theme prevalence over time (v1 Alarm+Caution subset)",
        "",
        f"- v1 A+C records, 2021–2026: **{len(df):,}**",
        f"- Bootstrap n=1000, seed={SEED}, 95% CI on year×theme cells.",
        "- v2 has no thematic classification — **robustness not assessed**.",
        "",
        "## Top 3 themes by overall prevalence",
        "",
    ]
    for i, t in enumerate(overall.head(3).index):
        md.append(f"{i+1}. **{THEME_LABELS[t]}** — {overall[t]:.1f}% of A+C papers")
    md.append("")
    md.append("## Per-theme temporal trend (Spearman year vs prevalence)")
    md.append("")
    md.append(
        "| Theme | Overall % | 2021 % | 2026 % | Δ (pp) | Spearman ρ | p |"
    )
    md.append("|---|---:|---:|---:|---:|---:|---:|")
    for r in trends_df.to_dict(orient="records"):
        md.append(
            f"| {r['label']} | {r['overall_pct']:.1f} | {r['y_2021']:.1f} | "
            f"{r['y_2026']:.1f} | {r['delta_pp_2021_to_2026']:+.2f} | "
            f"{r['spearman_rho']:+.3f} | {r['p_value']:.4f} |"
        )
    (ANALYSES_DIR / "theme_prevalence_summary.md").write_text("\n".join(md) + "\n")

    # Figure
    fig, ax = plt.subplots(figsize=(12, 7))
    # Sort themes for legend by overall prevalence descending
    legend_order = list(overall.index)
    for t in legend_order:
        pts = boot["point"][t].values
        lo = boot["lower"][t].values
        hi = boot["upper"][t].values
        ax.plot(YEARS, pts, marker="o", lw=2, color=THEME_COLOURS[t],
                label=f"{THEME_LABELS[t]} ({overall[t]:.0f}%)")
        ax.fill_between(YEARS, lo, hi, color=THEME_COLOURS[t], alpha=0.10)
    ax.set_xticks(YEARS)
    ax.set_xticklabels([str(y) if y != 2026 else "2026*" for y in YEARS], fontsize=10)
    ax.set_xlabel("Publication year", fontsize=11)
    ax.set_ylabel("% of Alarm+Caution papers flagged with theme", fontsize=11)
    ax.set_title(
        f"Theme prevalence in critical AI discourse, 2021–2026 (v1; n={len(df):,})\n"
        "Lines: point estimate, shaded: bootstrap 95% CI. Themes can co-occur per paper.\n"
        "* 2026 partial year (Jan–Apr).",
        fontsize=11, fontweight="bold",
    )
    ax.legend(loc="center left", bbox_to_anchor=(1.01, 0.5), fontsize=9,
              title="Theme (overall %)", title_fontsize=9)
    ax.grid(axis="y", alpha=0.25, ls="--", lw=0.5)
    fig.tight_layout()
    out_fig = FIGURES_DIR / "theme_prevalence.png"
    fig.savefig(out_fig, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"\nFigure: {out_fig}")

    print(f"\nFiles:")
    for p in [
        ANALYSES_DIR / "theme_prevalence_v1.csv",
        ANALYSES_DIR / "theme_prevalence_trends.csv",
        ANALYSES_DIR / "theme_prevalence_summary.md",
        out_fig,
    ]:
        print(f"  {p.relative_to(WORKTREE)}")


if __name__ == "__main__":
    main()
