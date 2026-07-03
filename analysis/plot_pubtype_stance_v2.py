"""
Redesigned pubtype_stance figure.

For each pub-type shows 3 grouped bars:
  % Critical (Alarm + Caution) | % Neutral | % Favourable (CO + Advocacy)
with bootstrap 95% CI, sorted by critical rate descending.

Reads: output/analyses/pubtype_stance_v1.csv
Writes: output/figures/pubtype_stance.png
"""

from __future__ import annotations
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd
from pathlib import Path

WORKTREE    = Path(__file__).resolve().parents[1]
IN_CSV      = WORKTREE / "output" / "analyses" / "pubtype_stance_v1.csv"
OUT_FIG     = WORKTREE / "output" / "figures" / "pubtype_stance.png"

# ── blended colours ───────────────────────────────────────────────────────────
# Critical:    blend(Alarm #C0392B, Caution #E67E22)
# Favourable:  blend(CO #2980B9, Advocacy #27AE60)
C_CRIT  = "#D35B26"   # orange-red blend
C_NEUT  = "#95A5A6"   # grey  — Neutral (unchanged)
C_FAV   = "#28978C"   # teal blend

# ── load & aggregate ──────────────────────────────────────────────────────────
df = pd.read_csv(IN_CSV)
df.columns = ["pub_type", "stance", "point", "lo", "hi"]

def agg(pt: str, stances: list[str]) -> pd.DataFrame:
    sub = df[df["stance"].isin(stances)]
    g = sub.groupby("pub_type").agg(
        point=("point", "sum"),
        lo=("lo", "sum"),      # conservative: sum of lower bounds
        hi=("hi", "sum"),      # conservative: sum of upper bounds
    ).reset_index()
    g["label"] = pt
    return g

crit = agg("Critical\n(Alarm+Caution)", ["Alarm", "Caution"])
neut = agg("Neutral",                   ["Neutral"])
fav  = agg("Favourable\n(CO+Advocacy)", ["Cautious Optimism", "Advocacy"])

# Sort pub_types by critical rate ascending left→right (Review first)
order = crit.sort_values("point", ascending=True)["pub_type"].tolist()

# ── figure ────────────────────────────────────────────────────────────────────
n_types  = len(order)
group_w  = 0.72          # total width per pub-type group
bar_w    = group_w / 3   # individual bar width
gap      = 0.04

fig, ax = plt.subplots(figsize=(9, 5.5))

for gi, pt in enumerate(order):
    x_centre = gi
    offsets  = [-(bar_w + gap), 0, (bar_w + gap)]
    datasets = [crit, neut, fav]
    colours  = [C_CRIT, C_NEUT, C_FAV]

    for offset, ds, col in zip(offsets, datasets, colours):
        row = ds[ds["pub_type"] == pt].iloc[0]
        x   = x_centre + offset
        ax.bar(x, row["point"], width=bar_w, color=col, alpha=0.88,
               edgecolor="white", linewidth=0.5)
        yerr_lo = row["point"] - row["lo"]
        yerr_hi = row["hi"]    - row["point"]
        ax.errorbar(x, row["point"],
                    yerr=[[yerr_lo], [yerr_hi]],
                    fmt="none", color="#333", lw=1, capsize=2.5)

# ── axes ──────────────────────────────────────────────────────────────────────
N_BY_TYPE = {
    "Research Article": 10315,
    "Review":            5444,
    "Letter":             480,
    "Editorial":          404,
    "Commentary":         104,
}

ax.set_xticks(range(n_types))
ax.set_xticklabels(
    [f"{pt}\n(n={N_BY_TYPE[pt]:,})" for pt in order],
    fontsize=10,
)
ax.set_ylabel("% of pub-type papers", fontsize=11)
ax.set_ylim(0, 100)
ax.set_xlim(-0.65, n_types - 0.35)
ax.grid(axis="y", alpha=0.25, ls="--", lw=0.5)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)

ax.set_title(
    "Stance Distribution by Publication Type (n=16,747)",
    fontsize=11, fontweight="bold",
)

# ── legend ────────────────────────────────────────────────────────────────────
handles = [
    mpatches.Patch(facecolor=C_CRIT, alpha=0.88, label="Critical (Alarm + Caution)"),
    mpatches.Patch(facecolor=C_NEUT, alpha=0.88, label="Neutral"),
    mpatches.Patch(facecolor=C_FAV,  alpha=0.88, label="Favourable (CO + Advocacy)"),
]
ax.legend(handles=handles, loc="upper left", fontsize=9,
          framealpha=0.9, edgecolor="#cccccc")

fig.tight_layout(rect=[0, 0.07, 1, 1])
fig.text(
    0.5, 0.01,
    "Bars: v1 point estimate with bootstrap 95% CI. "
    "CI for combined stances = sum of individual CIs (conservative).",
    ha="center", va="bottom", fontsize=7.5, color="#444444",
)

fig.savefig(OUT_FIG, dpi=300, bbox_inches="tight", facecolor="white")
plt.close(fig)
print(f"Saved → {OUT_FIG.relative_to(WORKTREE)}")
