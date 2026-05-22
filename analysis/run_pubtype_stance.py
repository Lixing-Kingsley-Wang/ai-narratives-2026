"""
Task 3.2 — Publication-type stratification.

Computes stance distribution by pub_type (5-bucket: Research Article,
Editorial, Review, Commentary, Letter) with bootstrap 95% CIs. Tests
whether editorial/commentary differ from research articles in stance
(chi-square). Reports v1/v2 robustness.

Produces:
  output/analyses/pubtype_stance_v1.csv
  output/analyses/pubtype_stance_v2.csv
  output/analyses/pubtype_stance_robustness.md
  output/analyses/pubtype_chi_square.md
  output/figures/pubtype_stance.png            (grouped bar, 300 dpi)
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency

from analysis.robustness import (
    PUBTYPE_BUCKETS_5,
    STANCES,
    dual_analysis,
    load_classifications,
)

WORKTREE = Path(__file__).resolve().parents[1]
ANALYSES_DIR = WORKTREE / "output" / "analyses"
FIGURES_DIR = WORKTREE / "output" / "figures"

STANCE_COLOURS = {
    "Alarm": "#C0392B",
    "Caution": "#E67E22",
    "Neutral": "#95A5A6",
    "Cautious Optimism": "#27AE60",
    "Advocacy": "#2980B9",
}


def stance_pct_by_pubtype(df: pd.DataFrame) -> pd.DataFrame:
    """Return pubtype (rows) x stance (cols) of percentages, 5-bucket."""
    ct = pd.crosstab(df["pub_type_simple_5"], df["stance"], normalize="index") * 100
    return ct.reindex(index=PUBTYPE_BUCKETS_5, columns=STANCES).fillna(0.0)


def main() -> None:
    print("Task 3.2 — Publication-type stratification")
    print("=" * 60)

    v1 = load_classifications("v1")
    v2 = load_classifications("v2")

    # Counts per pubtype
    print("\nCounts by pub_type (5-bucket):")
    counts_v1 = v1["pub_type_simple_5"].value_counts().reindex(PUBTYPE_BUCKETS_5).fillna(0).astype(int)
    counts_v2 = v2["pub_type_simple_5"].value_counts().reindex(PUBTYPE_BUCKETS_5).fillna(0).astype(int)
    for pt in PUBTYPE_BUCKETS_5:
        print(f"  {pt:<18} v1: {counts_v1[pt]:>6,}   v2: {counts_v2[pt]:>6,}")

    # ── Dual analysis with bootstrap CIs ───────────────────────────────────
    result = dual_analysis(
        stance_pct_by_pubtype,
        agg_name="pubtype_stance",
        output_dir=ANALYSES_DIR,
        v1_df=v1,
        v2_df=v2,
        tolerance_pp=3.0,
    )
    pt_v1 = result["v1_result"]["point"]
    pt_v2 = result["v2_result"]["point"]

    print("\nv1 % stance by pub_type:")
    print(pt_v1.round(2).to_string())
    print("\nv1 critical (Alarm+Caution) by pub_type:")
    crit_v1 = (pt_v1["Alarm"] + pt_v1["Caution"]).round(2)
    print(crit_v1.to_string())

    # ── Chi-square: editorial+commentary vs research article ──────────────
    chi_md = ["# Chi-square test — opinion (Editorial+Commentary+Letter) vs Research Article",
              "",
              "v1 (canonical):",
              ""]
    # Group opinion
    v1_op = v1[v1["pub_type_simple_5"].isin(["Editorial", "Commentary", "Letter"])]
    v1_re = v1[v1["pub_type_simple_5"] == "Research Article"]
    contingency = pd.DataFrame(
        {
            "Opinion (Ed+Com+Let)": v1_op["stance"].value_counts().reindex(STANCES).fillna(0).astype(int),
            "Research Article": v1_re["stance"].value_counts().reindex(STANCES).fillna(0).astype(int),
        }
    )
    chi2, p, dof, expected = chi2_contingency(contingency.values)
    def _df_to_md(df: pd.DataFrame) -> str:
        cols = list(df.columns)
        lines = ["| | " + " | ".join(str(c) for c in cols) + " |"]
        lines.append("|" + "---|" * (len(cols) + 1))
        for idx, row in df.iterrows():
            lines.append(
                "| " + str(idx) + " | " + " | ".join(str(v) for v in row.values) + " |"
            )
        return "\n".join(lines)

    chi_md.append("Contingency table (counts):\n")
    chi_md.append(_df_to_md(contingency))
    chi_md.append("")
    chi_md.append(f"- chi² = {chi2:.2f}, dof = {dof}, p = {p:.3e}")
    chi_md.append(
        f"- n_opinion = {int(v1_op.shape[0]):,}  vs  n_research = {int(v1_re.shape[0]):,}"
    )
    crit_opinion = (
        v1_op["stance"].isin(["Alarm", "Caution"]).mean() * 100
    )
    crit_research = (
        v1_re["stance"].isin(["Alarm", "Caution"]).mean() * 100
    )
    chi_md.append(
        f"- Critical (Alarm+Caution): opinion **{crit_opinion:.1f}%** vs "
        f"research **{crit_research:.1f}%** (Δ {crit_opinion - crit_research:+.1f} pp)"
    )

    # Same on v2
    v2_op = v2[v2["pub_type_simple_5"].isin(["Editorial", "Commentary", "Letter"])]
    v2_re = v2[v2["pub_type_simple_5"] == "Research Article"]
    cont2 = pd.DataFrame(
        {
            "Opinion (Ed+Com+Let)": v2_op["stance"].value_counts().reindex(STANCES).fillna(0).astype(int),
            "Research Article": v2_re["stance"].value_counts().reindex(STANCES).fillna(0).astype(int),
        }
    )
    chi2_v2, p_v2, dof_v2, _ = chi2_contingency(cont2.values)
    crit_op_v2 = v2_op["stance"].isin(["Alarm", "Caution"]).mean() * 100
    crit_re_v2 = v2_re["stance"].isin(["Alarm", "Caution"]).mean() * 100
    chi_md += [
        "",
        "## v2 (robustness)",
        "",
        _df_to_md(cont2),
        "",
        f"- chi² = {chi2_v2:.2f}, dof = {dof_v2}, p = {p_v2:.3e}",
        f"- Critical (Alarm+Caution): opinion **{crit_op_v2:.1f}%** vs "
        f"research **{crit_re_v2:.1f}%** (Δ {crit_op_v2 - crit_re_v2:+.1f} pp)",
    ]
    (ANALYSES_DIR / "pubtype_chi_square.md").write_text("\n".join(chi_md) + "\n")
    print(f"\nChi-square (v1): chi²={chi2:.2f}, dof={dof}, p={p:.3e}")
    print(f"  opinion critical%: {crit_opinion:.1f}  vs research: {crit_research:.1f}")
    print(f"Chi-square (v2): chi²={chi2_v2:.2f}, dof={dof_v2}, p={p_v2:.3e}")
    print(f"  opinion critical%: {crit_op_v2:.1f}  vs research: {crit_re_v2:.1f}")

    # ── Figure: grouped bar, pubtype × stance with CIs ─────────────────────
    fig, ax = plt.subplots(figsize=(12, 6))
    x = np.arange(len(PUBTYPE_BUCKETS_5))
    width = 0.16
    for i, stance in enumerate(STANCES):
        pts = pt_v1[stance].reindex(PUBTYPE_BUCKETS_5).values
        lo = result["v1_result"]["lower"][stance].reindex(PUBTYPE_BUCKETS_5).values
        hi = result["v1_result"]["upper"][stance].reindex(PUBTYPE_BUCKETS_5).values
        yerr = np.array([pts - lo, hi - pts])
        ax.bar(
            x + (i - 2) * width,
            pts,
            width,
            color=STANCE_COLOURS[stance],
            label=stance,
            yerr=yerr,
            error_kw={"lw": 0.8, "capsize": 2, "ecolor": "#333"},
            alpha=0.9,
        )
    # n labels
    for j, pt in enumerate(PUBTYPE_BUCKETS_5):
        ax.text(
            x[j], -3.5, f"n={counts_v1[pt]:,}", ha="center", fontsize=9, color="#555",
        )
    ax.set_xticks(x)
    ax.set_xticklabels(PUBTYPE_BUCKETS_5, fontsize=10)
    ax.set_ylabel("% of records", fontsize=11)
    ax.set_title(
        "Stance by publication type — Q1/Q2 medical journals, 2021–2026 (v1)\n"
        "Bars: bootstrap 95% CI (n_boot=1000). See pubtype_stance_v2.csv for v2 robustness.",
        fontsize=11, fontweight="bold",
    )
    ax.legend(loc="upper left", fontsize=9, framealpha=0.9, ncol=2)
    ax.set_ylim(bottom=-7)
    ax.axhline(0, color="#888", lw=0.5)
    fig.tight_layout()
    out_fig = FIGURES_DIR / "pubtype_stance.png"
    fig.savefig(out_fig, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"\nFigure: {out_fig}")

    print(f"\nVerdict summary: {result['verdict']['summary']}")
    print("Files:", [str(f.relative_to(WORKTREE)) for f in result["files"]])


if __name__ == "__main__":
    main()
