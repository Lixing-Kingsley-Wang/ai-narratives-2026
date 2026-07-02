"""
Revised theme_prevalence figure (v2 layout):
  - Main figure: 4 focal themes as coloured lines + gray min-max ribbon for 6 minor themes
  - Supplementary figure: 6 minor themes as individual coloured lines

Reads pre-computed bootstrap CSV so no re-sampling needed.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import numpy as np
import pandas as pd

WORKTREE = Path(__file__).resolve().parents[1]
ANALYSES_DIR = WORKTREE / "output" / "analyses"
FIGURES_DIR  = WORKTREE / "output" / "figures"

YEARS = list(range(2021, 2027))

FOCAL_THEMES = ["safety_clinical", "hallucination", "regulation", "ethics_bias"]
FOCAL_LABELS = {
    "safety_clinical": "Patient safety",
    "hallucination":   "Hallucination / errors",
    "regulation":      "Governance / regulation",
    "ethics_bias":     "Ethics & bias",
}
# Distinct, colourblind-friendly colours for the 4 focal themes
FOCAL_COLOURS = {
    "safety_clinical": "#1f77b4",   # blue
    "hallucination":   "#ff7f0e",   # orange
    "regulation":      "#2ca02c",   # green
    "ethics_bias":     "#d62728",   # red
}

MINOR_THEMES = ["education", "data_privacy", "cognitive", "existential", "replacement", "other"]
MINOR_LABELS = {
    "education":    "Medical education",
    "data_privacy": "Data privacy",
    "cognitive":    "Cognitive offloading",
    "existential":  "Existential threat",
    "replacement":  "Replacement fears",
    "other":        "Other / uncategorised",
}
# Tab10 colours (positions 4–9) for the supplementary figure
_tab10 = plt.cm.tab10(np.linspace(0, 1, 10))
MINOR_COLOURS = {t: _tab10[4 + i] for i, t in enumerate(MINOR_THEMES)}

GRAY_RIBBON   = "#999999"
GRAY_LINE     = "#666666"


def load_data() -> pd.DataFrame:
    df = pd.read_csv(ANALYSES_DIR / "theme_prevalence_v1.csv")
    df = df[df["pub_year"].isin(YEARS)]
    return df


def pivot(df: pd.DataFrame, col: str) -> pd.DataFrame:
    return df.pivot(index="pub_year", columns="theme", values=col)


# ── Main figure ────────────────────────────────────────────────────────────────

def plot_main(df: pd.DataFrame) -> None:
    pt  = pivot(df, "point")
    lo  = pivot(df, "ci_lower")
    hi  = pivot(df, "ci_upper")

    # Overall % for legend labels (mean across years)
    overall = pt.mean()

    fig, ax = plt.subplots(figsize=(9, 5.5))

    # ── Gray ribbon: min–max across minor themes per year ──────────────────
    minor_lo  = lo[MINOR_THEMES].min(axis=1)
    minor_hi  = hi[MINOR_THEMES].max(axis=1)
    minor_mid = pt[MINOR_THEMES].mean(axis=1)   # centre line (dashed)

    ax.fill_between(YEARS, minor_lo, minor_hi,
                    color=GRAY_RIBBON, alpha=0.35, zorder=1, label="_nolegend_")
    ax.plot(YEARS, minor_mid, color=GRAY_LINE, lw=1.2, ls="--",
            zorder=2, label="_nolegend_")

    # ── 4 focal coloured lines ─────────────────────────────────────────────
    for t in FOCAL_THEMES:
        c = FOCAL_COLOURS[t]
        pct = overall[t]
        ax.plot(YEARS, pt[t], marker="o", lw=2, color=c, zorder=3,
                label=f"{FOCAL_LABELS[t]} ({pct:.0f}%)")
        ax.fill_between(YEARS, lo[t], hi[t], color=c, alpha=0.12, zorder=2)

    # ── Legend ─────────────────────────────────────────────────────────────
    # Build custom handles: 4 coloured lines + 1 gray composite patch
    line_handles = [
        mlines.Line2D([], [], color=FOCAL_COLOURS[t], marker="o", lw=2,
                      label=f"{FOCAL_LABELS[t]} ({overall[t]:.0f}%)")
        for t in FOCAL_THEMES
    ]

    # Compute overall range of minor themes for the legend note
    minor_overall_lo = pt[MINOR_THEMES].mean().min()
    minor_overall_hi = pt[MINOR_THEMES].mean().max()
    other_patch = mpatches.Patch(
        facecolor=GRAY_RIBBON, alpha=0.55, edgecolor=GRAY_LINE, lw=1,
        label=f"Other themes  (n=6, avg {minor_overall_lo:.0f}–{minor_overall_hi:.0f}%)"
    )

    # ── Axes ──────────────────────────────────────────────────────────────
    ax.set_xticks(YEARS)
    ax.set_xticklabels([str(y) if y != 2026 else "2026*" for y in YEARS], fontsize=10)
    ax.set_xlabel("Publication year", fontsize=11)
    ax.set_ylabel("% of Alarm+Caution papers", fontsize=11)
    ax.set_ylim(bottom=0)
    ax.set_title(
        "Theme Prevalence in the Critical AI Corpus, 2021–2026 (n=5,161)",
        fontsize=11, fontweight="bold",
    )
    ax.grid(axis="y", alpha=0.25, ls="--", lw=0.5)

    leg = ax.legend(
        handles=line_handles + [other_patch],
        loc="center left",
        bbox_to_anchor=(1.01, 0.5),
        fontsize=9,
        framealpha=0.9,
        edgecolor="#cccccc",
    )

    fig.tight_layout()
    fig.subplots_adjust(right=0.72)

    out = FIGURES_DIR / "theme_prevalence.png"
    fig.savefig(out, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Main figure → {out.relative_to(WORKTREE)}")


# ── Supplementary figure ──────────────────────────────────────────────────────

def plot_supplementary(df: pd.DataFrame) -> None:
    pt  = pivot(df, "point")
    lo  = pivot(df, "ci_lower")
    hi  = pivot(df, "ci_upper")
    overall = pt.mean()

    fig, ax = plt.subplots(figsize=(9, 5.5))

    for t in MINOR_THEMES:
        c = MINOR_COLOURS[t]
        yerr_lo = pt[t].values - lo[t].values
        yerr_hi = hi[t].values - pt[t].values
        ax.plot(YEARS, pt[t], marker="o", lw=2, color=c,
                label=f"{MINOR_LABELS[t]} ({overall[t]:.0f}%)", zorder=3)
        ax.errorbar(YEARS, pt[t], yerr=[yerr_lo, yerr_hi],
                    fmt="none", color=c, capsize=3, lw=1, alpha=0.7, zorder=2)

    ax.set_xticks(YEARS)
    ax.set_xticklabels([str(y) if y != 2026 else "2026*" for y in YEARS], fontsize=10)
    ax.set_xlabel("Publication year", fontsize=11)
    ax.set_ylabel("% of Alarm+Caution papers", fontsize=11)
    ax.set_ylim(bottom=0)
    ax.set_title(
        "Supplementary Figure — Minor Theme Prevalence in the Critical AI Corpus,\n"
        "2021–2026 (n=5,161)",
        fontsize=11, fontweight="bold",
    )
    ax.legend(
        loc="center left",
        bbox_to_anchor=(1.01, 0.5),
        fontsize=9,
        framealpha=0.9,
        edgecolor="#cccccc",
    )
    ax.grid(axis="y", alpha=0.25, ls="--", lw=0.5)

    fig.tight_layout()
    fig.subplots_adjust(right=0.72)

    out = FIGURES_DIR / "theme_prevalence_sup.png"
    fig.savefig(out, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Supplementary figure → {out.relative_to(WORKTREE)}")


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    df = load_data()
    plot_main(df)
    plot_supplementary(df)
    print("Done.")
