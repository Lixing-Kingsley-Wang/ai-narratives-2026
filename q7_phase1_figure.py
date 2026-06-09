"""Phase 1 temporal figure on q7_classified_alarm.csv.
Two stacked-bar panels (failure_mode and model_type, % within year) sharing the
year axis, plus an inline line panel for confabulation-share and generative-share."""

import csv, os
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np

BASE = os.path.dirname(os.path.abspath(__file__))
P    = os.path.join(BASE, "output", "analyses", "q7_classified_alarm.csv")
OUT  = os.path.join(BASE, "output", "figures", "q7_alarm_temporal.png")

YEARS = ["2021","2022","2023","2024","2025","2026"]
FM_ORDER  = ["confabulation","both","misclassification","none_or_unclear"]
MT_ORDER  = ["generative","both","discriminative","unclear"]
FM_COLORS = {"confabulation":"#d62728", "both":"#9467bd",
             "misclassification":"#1f77b4", "none_or_unclear":"#bcbd22"}
MT_COLORS = {"generative":"#e377c2", "both":"#9467bd",
             "discriminative":"#2ca02c", "unclear":"#7f7f7f"}

with open(P, encoding="utf-8") as f:
    rows = [r for r in csv.DictReader(f) if r["failure_mode"] != "FAILED"]

by_year = Counter(r["pub_year"] for r in rows)
fm_by   = Counter((r["pub_year"], r["failure_mode"]) for r in rows)
mt_by   = Counter((r["pub_year"], r["model_type"])  for r in rows)

# matrices: rows = category, cols = year, values = % within year
def mat(order, joint):
    m = np.zeros((len(order), len(YEARS)))
    for i, cat in enumerate(order):
        for j, y in enumerate(YEARS):
            tot = by_year[y]
            m[i, j] = joint.get((y, cat), 0) / tot * 100 if tot else 0
    return m

fm_m = mat(FM_ORDER, fm_by)
mt_m = mat(MT_ORDER, mt_by)
totals = [by_year[y] for y in YEARS]

# key share lines
conf_share = [(fm_by.get((y,"confabulation"),0) + fm_by.get((y,"both"),0))/by_year[y]*100 for y in YEARS]
gen_share  = [(mt_by.get((y,"generative"),0)    + mt_by.get((y,"both"),0))/by_year[y]*100 for y in YEARS]

fig = plt.figure(figsize=(12, 11))
gs  = fig.add_gridspec(3, 1, height_ratios=[1.2, 1.2, 1.0], hspace=0.35)
ax1 = fig.add_subplot(gs[0])
ax2 = fig.add_subplot(gs[1], sharex=ax1)
ax3 = fig.add_subplot(gs[2], sharex=ax1)

def stacked(ax, m, order, colors, title, totals):
    x = np.arange(len(YEARS))
    bottom = np.zeros(len(YEARS))
    for i, cat in enumerate(order):
        ax.bar(x, m[i], bottom=bottom, color=colors[cat], label=cat,
               edgecolor="white", linewidth=0.5, width=0.7)
        # annotate cells ≥4%
        for j in range(len(YEARS)):
            v = m[i, j]
            if v >= 4:
                ax.text(j, bottom[j] + v/2, f"{v:.0f}%", ha="center", va="center",
                        fontsize=8, color="white" if cat != "none_or_unclear" else "black",
                        fontweight="bold")
        bottom += m[i]
    ax.set_xticks(x)
    ax.set_xticklabels([f"{y}\n(n={totals[j]})" for j,y in enumerate(YEARS)], fontsize=9)
    ax.set_ylim(0, 105)
    ax.set_ylabel("% within year")
    ax.set_title(title, fontsize=11, fontweight="bold", loc="left")
    ax.legend(loc="center left", bbox_to_anchor=(1.005, 0.5), fontsize=9, frameon=False)
    ax.axvline(2 - 0.5, color="red", linestyle="--", linewidth=1.2, alpha=0.7)
    ax.text(2 - 0.5, 102, " 2023 inflection", color="red", fontsize=8,
            va="bottom", ha="left", style="italic")
    for s in ("top","right"): ax.spines[s].set_visible(False)

stacked(ax1, fm_m, FM_ORDER, FM_COLORS,
        "A. failure_mode composition by year (Alarm only, n=915)", totals)
stacked(ax2, mt_m, MT_ORDER, MT_COLORS,
        "B. model_type composition by year (Alarm only, n=915)", totals)

x = np.arange(len(YEARS))
ax3.plot(x, gen_share,  marker="o", color="#e377c2", linewidth=2.2,
         label="generative-share (model_type ∈ {generative, both})")
ax3.plot(x, conf_share, marker="s", color="#d62728", linewidth=2.2,
         label="confabulation-share (failure_mode ∈ {confabulation, both})")
for xi, v in zip(x, gen_share):
    ax3.annotate(f"{v:.0f}%", (xi, v), textcoords="offset points",
                 xytext=(0, 8), ha="center", fontsize=8, color="#e377c2")
for xi, v in zip(x, conf_share):
    ax3.annotate(f"{v:.0f}%", (xi, v), textcoords="offset points",
                 xytext=(0,-14), ha="center", fontsize=8, color="#d62728")
ax3.axvline(2 - 0.5, color="red", linestyle="--", linewidth=1.2, alpha=0.7)
ax3.set_xticks(x); ax3.set_xticklabels(YEARS, fontsize=9)
ax3.set_ylim(-5, 100)
ax3.set_ylabel("% of Alarm papers")
ax3.set_title("C. Key shares over time — note divergence between the two axes",
              fontsize=11, fontweight="bold", loc="left")
ax3.legend(loc="upper left", fontsize=9, frameon=False)
for s in ("top","right"): ax3.spines[s].set_visible(False)

fig.suptitle("Q7 Phase 1 — temporal pattern of failure_mode and model_type within Alarm papers",
             fontsize=12, y=0.995)
fig.text(0.5, 0.005,
         "Prompt: q7_failuremode_v1 · model: claude-sonnet-4-6 · stance: Alarm only (Caution pending)",
         ha="center", fontsize=8, style="italic", color="gray")

os.makedirs(os.path.dirname(OUT), exist_ok=True)
fig.savefig(OUT, dpi=300, bbox_inches="tight")
print(f"saved → {OUT}")

# print the underlying numbers
print("\nYear-by-year shares (Alarm):")
print(f"  {'year':<8s} {'n':>5s} {'conf%':>7s} {'misc%':>7s} {'both_fm%':>9s} {'unclear%':>9s}  ||  "
      f"{'gen%':>6s} {'discr%':>7s} {'both_mt%':>9s} {'unclear%':>9s}")
for j, y in enumerate(YEARS):
    n = totals[j]
    print(f"  {y:<8s} {n:>5d} "
          f"{fm_m[0,j]:>6.1f}% {fm_m[2,j]:>6.1f}% {fm_m[1,j]:>8.1f}% {fm_m[3,j]:>8.1f}%  ||  "
          f"{mt_m[0,j]:>5.1f}% {mt_m[2,j]:>6.1f}% {mt_m[1,j]:>8.1f}% {mt_m[3,j]:>8.1f}%")
print(f"\nConfabulation-share by year: {[f'{v:.1f}%' for v in conf_share]}")
print(f"Generative-share   by year: {[f'{v:.1f}%' for v in gen_share]}")
