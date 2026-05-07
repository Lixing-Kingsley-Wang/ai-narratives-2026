"""
Figure Generator — AI Narratives Study
Reads all analysis CSVs and regenerates all figures at 300 DPI.
Run after all classification and analysis scripts are complete.

Figures produced (output/figures/):
  fig01_stance_stream.png        — stacked area, stance × quarter
  fig02_alarm_arc.png            — critical stance trend with ChatGPT marker
  fig03_thematic_evolution.png   — theme × year heatmap (Alarm+Caution papers)
  fig04_specialty_ranking.png    — specialty ranked by critical stance
  fig05_q3_comparison.png        — Q1Q2 vs Q3 pre-filtered comparison
  fig06_geography.png            — regional critical stance
  fig07_pubtype.png              — stance by publication type
  fig08_volume_growth.png        — publication volume by year
"""

import csv, os, re, collections
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
import numpy as np

BASE_DIR     = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR   = os.path.join(BASE_DIR, "output")
ANALYSIS_DIR = os.path.join(OUTPUT_DIR, "analysis")
FIGURES_DIR  = os.path.join(OUTPUT_DIR, "figures")
os.makedirs(FIGURES_DIR, exist_ok=True)

STANCES = ["Alarm", "Caution", "Neutral", "Cautious Optimism", "Advocacy"]
COLOURS = {
    "Alarm":             "#C0392B",
    "Caution":           "#E67E22",
    "Neutral":           "#95A5A6",
    "Cautious Optimism": "#27AE60",
    "Advocacy":          "#2980B9",
}
CRITICAL_COLOUR = "#8E1A0E"
CHATGPT_COLOUR  = "#2C3E50"

PLT_STYLE = {
    "font.family":   "Arial",
    "font.size":     11,
    "axes.spines.top":   False,
    "axes.spines.right": False,
    "axes.labelsize":    12,
    "axes.titlesize":    13,
    "axes.titleweight":  "bold",
    "figure.dpi":        150,
}
plt.rcParams.update(PLT_STYLE)


def load_csv(fname):
    path = os.path.join(ANALYSIS_DIR, fname)
    if not os.path.exists(path):
        print(f"  WARNING: {fname} not found — skipping")
        return []
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def save(fig, name):
    path = os.path.join(FIGURES_DIR, name)
    fig.savefig(path, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  Saved: {name}")


# ── Fig 01: Stance stream by quarter ──────────────────────────────────────────
def fig01_stance_stream():
    rows = load_csv("01_stance_by_quarter.csv")
    if not rows:
        return

    # Filter 2021-2025 (exclude partial 2026)
    rows = [r for r in rows if "2021" <= r["quarter"][:4] <= "2025"]
    quarters = [r["quarter"] for r in rows]
    x = np.arange(len(quarters))

    fig, ax = plt.subplots(figsize=(14, 6))
    bottoms = np.zeros(len(quarters))

    for stance in STANCES:
        vals = np.array([float(r.get(f"{stance}_pct", 0)) for r in rows])
        ax.fill_between(x, bottoms, bottoms + vals,
                        color=COLOURS[stance], alpha=0.88, label=stance)
        bottoms += vals

    # ChatGPT launch marker
    cg_idx = next((i for i, q in enumerate(quarters) if q == "2022-Q4"), None)
    if cg_idx:
        ax.axvline(cg_idx, color=CHATGPT_COLOUR, lw=1.2, ls="--", alpha=0.6)
        ax.text(cg_idx + 0.2, 97, "ChatGPT\nlaunched", fontsize=8.5,
                va="top", color=CHATGPT_COLOUR)

    # x-axis: year labels at Q1
    yticks = [i for i, q in enumerate(quarters) if q.endswith("Q1")]
    ylabels = [q[:4] for q in quarters if q.endswith("Q1")]
    ax.set_xticks(yticks)
    ax.set_xticklabels(ylabels, fontsize=11)
    ax.set_xlim(0, len(quarters) - 1)
    ax.set_ylim(0, 100)
    ax.set_ylabel("Proportion of papers (%)", fontsize=12)
    ax.set_xlabel("Publication year", fontsize=12)
    ax.set_title("Stance toward AI in medicine — Q1/Q2 journals, 2021–2025\n(discourse and evaluative papers only; n = 13,374)",
                 fontsize=12, fontweight="bold")

    handles = [mpatches.Patch(color=COLOURS[s], label=s) for s in STANCES]
    ax.legend(handles=handles[::-1], loc="lower left", fontsize=9,
              framealpha=0.9, ncol=1)

    fig.tight_layout()
    save(fig, "fig01_stance_stream.png")


# ── Fig 02: Critical stance arc ────────────────────────────────────────────────
def fig02_alarm_arc():
    rows = load_csv("01_stance_by_quarter.csv")
    if not rows:
        return

    rows = [r for r in rows if "2021" <= r["quarter"][:4] <= "2025"]
    quarters = [r["quarter"] for r in rows]
    x = np.arange(len(quarters))

    fig, ax = plt.subplots(figsize=(13, 5))

    for stance, lw, alpha in [("Alarm", 2.0, 0.75), ("Caution", 1.5, 0.65)]:
        vals = np.array([float(r.get(f"{stance}_pct", 0)) for r in rows])
        ax.plot(x, vals, color=COLOURS[stance], lw=lw, label=stance, alpha=alpha)

    # Combined critical
    crit = np.array([
        float(r.get("Alarm_pct", 0)) + float(r.get("Caution_pct", 0))
        for r in rows
    ])
    ax.plot(x, crit, color=CRITICAL_COLOUR, lw=2.8,
            label="Alarm + Caution (combined)", zorder=5)

    # Smoothed trend
    from numpy.polynomial.polynomial import polyfit
    coeffs = polyfit(x, crit, 3)
    smooth = np.polyval(coeffs[::-1], x)
    ax.plot(x, smooth, color=CRITICAL_COLOUR, lw=1.2, ls=":", alpha=0.5)

    # ChatGPT marker
    cg_idx = next((i for i, q in enumerate(quarters) if q == "2022-Q4"), None)
    if cg_idx:
        ax.axvline(cg_idx, color=CHATGPT_COLOUR, lw=1.2, ls="--", alpha=0.5)
        ax.text(cg_idx + 0.15, ax.get_ylim()[1] * 0.92,
                "ChatGPT\nlaunched", fontsize=8.5, color=CHATGPT_COLOUR, va="top")

    yticks = [i for i, q in enumerate(quarters) if q.endswith("Q1")]
    ax.set_xticks(yticks)
    ax.set_xticklabels([q[:4] for q in quarters if q.endswith("Q1")], fontsize=11)
    ax.set_ylabel("% of papers per quarter", fontsize=12)
    ax.set_xlabel("Publication year", fontsize=12)
    ax.set_title("Critical stance (Alarm + Caution) toward AI in medicine, 2021–2025",
                 fontsize=12, fontweight="bold")
    ax.set_ylim(bottom=0)
    ax.legend(fontsize=10, loc="upper left")
    fig.tight_layout()
    save(fig, "fig02_alarm_arc.png")


# ── Fig 03: Thematic evolution heatmap ────────────────────────────────────────
def fig03_thematic_evolution():
    path = os.path.join(OUTPUT_DIR, "analysis", "thematic_alarm.csv")
    if not os.path.exists(path):
        print("  WARNING: thematic_alarm.csv not found — skipping fig03")
        return

    theme_by_year = collections.defaultdict(lambda: collections.Counter())
    total_by_year = collections.Counter()

    with open(path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            year = row.get("pub_year","") or ""
            if not year:
                m = re.search(r'\b(20\d{2})\b', row.get("pub_date","") or "")
                year = m.group() if m else ""
            themes = [t for t in row.get("themes","").split("|") if t]
            if year and "2021" <= year <= "2025":
                total_by_year[year] += 1
                for t in themes:
                    theme_by_year[year][t] += 1

    years = sorted(total_by_year.keys())
    theme_order = [
        "safety_clinical", "regulation", "ethics_bias", "hallucination",
        "data_privacy", "education", "cognitive", "existential", "replacement", "other"
    ]
    theme_labels = {
        "safety_clinical": "Patient safety",
        "regulation":      "Governance/regulation",
        "ethics_bias":     "Ethics & bias",
        "hallucination":   "Hallucination/errors",
        "data_privacy":    "Data privacy",
        "education":       "Medical education",
        "cognitive":       "Cognitive offloading",
        "existential":     "Existential threat",
        "replacement":     "Replacement fears",
        "other":           "Other"
    }

    matrix = np.array([
        [theme_by_year[y].get(t, 0) / total_by_year[y] * 100 if total_by_year[y] else 0
         for y in years]
        for t in theme_order
    ])

    fig, ax = plt.subplots(figsize=(10, 7))
    im = ax.imshow(matrix, aspect="auto", cmap="YlOrRd", vmin=0, vmax=70)

    ax.set_xticks(range(len(years)))
    ax.set_xticklabels(years, fontsize=11)
    ax.set_yticks(range(len(theme_order)))
    ax.set_yticklabels([theme_labels[t] for t in theme_order], fontsize=10)

    for i in range(len(theme_order)):
        for j in range(len(years)):
            val = matrix[i, j]
            ax.text(j, i, f"{val:.0f}%", ha="center", va="center",
                    fontsize=9, color="black" if val < 40 else "white",
                    fontweight="bold" if val > 50 else "normal")

    cbar = plt.colorbar(im, ax=ax, shrink=0.8)
    cbar.set_label("% of critical papers that year", fontsize=10)
    ax.set_title("Concern themes in critical AI discourse by year\n(% of Alarm + Caution papers; multiple themes per paper)",
                 fontsize=12, fontweight="bold")
    ax.set_xlabel("Publication year", fontsize=12)
    fig.tight_layout()
    save(fig, "fig03_thematic_evolution.png")


# ── Fig 04: Specialty ranking ─────────────────────────────────────────────────
def fig04_specialty():
    rows = load_csv("03_specialty_stance.csv")
    if not rows:
        return

    # Filter meaningful specialties
    rows = [r for r in rows if int(r.get("total","0")) >= 50]
    rows.sort(key=lambda x: float(x.get("critical_pct","0")), reverse=True)

    specialties = [r["specialty"] for r in rows]
    alarm_pcts  = [float(r.get("Alarm_pct","0")) for r in rows]
    caut_pcts   = [float(r.get("Caution_pct","0")) for r in rows]
    opt_pcts    = [float(r.get("Cautious Optimism_pct","0")) for r in rows]
    ns          = [int(r.get("total","0")) for r in rows]

    y = np.arange(len(specialties))
    fig, ax = plt.subplots(figsize=(11, 7))

    bars_alarm = ax.barh(y, alarm_pcts, color=COLOURS["Alarm"], label="Alarm", alpha=0.9)
    bars_caut  = ax.barh(y, caut_pcts, left=alarm_pcts,
                         color=COLOURS["Caution"], label="Caution", alpha=0.9)
    # Cautious Optimism as separate markers
    ax.scatter(opt_pcts, y, color=COLOURS["Cautious Optimism"],
               marker="D", s=50, zorder=5, label="Cautious Optimism %")

    # n labels
    for i, (n, ap, cp) in enumerate(zip(ns, alarm_pcts, caut_pcts)):
        ax.text(ap + cp + 0.5, i, f"n={n:,}", va="center", fontsize=8.5, color="#555")

    ax.set_yticks(y)
    ax.set_yticklabels(specialties, fontsize=10)
    ax.set_xlabel("% of papers", fontsize=12)
    ax.set_title("Stance toward AI by medical specialty\n(ranked by critical stance; Q1/Q2 journals, 2021–2025)",
                 fontsize=12, fontweight="bold")
    ax.axvline(25, color="#aaa", lw=0.8, ls="--", alpha=0.6)
    ax.legend(loc="lower right", fontsize=9)
    ax.set_xlim(0, max(alarm_pcts[i] + caut_pcts[i] for i in range(len(rows))) + 12)
    fig.tight_layout()
    save(fig, "fig04_specialty_ranking.png")


# ── Fig 05: Q1Q2 vs Q3 comparison ─────────────────────────────────────────────
def fig05_q3_comparison():
    rows = load_csv("05_q1q2_vs_q3_stance.csv")
    if not rows:
        return

    years   = sorted(set(r["year"] for r in rows if "2021" <= r["year"] <= "2025"))
    q1q2    = {r["year"]: float(r["critical_pct"]) for r in rows if r["corpus"] in ("Q1/Q2","Q1Q2")}
    q3      = {r["year"]: float(r["critical_pct"]) for r in rows if "Q3" in r["corpus"]}

    x = np.arange(len(years))
    w = 0.35

    fig, ax = plt.subplots(figsize=(10, 5))
    bars1 = ax.bar(x - w/2, [q1q2.get(y, 0) for y in years], w,
                   color=CRITICAL_COLOUR, alpha=0.85, label="Q1/Q2 journals")
    bars2 = ax.bar(x + w/2, [q3.get(y, 0) for y in years], w,
                   color="#7F8C8D", alpha=0.75, label="Q3 journals")

    for bar in bars1:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 0.3,
                f"{h:.0f}%", ha="center", va="bottom", fontsize=9, fontweight="bold",
                color=CRITICAL_COLOUR)
    for bar in bars2:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 0.3,
                f"{h:.0f}%", ha="center", va="bottom", fontsize=9, color="#555")

    ax.set_xticks(x)
    ax.set_xticklabels(years, fontsize=11)
    ax.set_ylabel("Critical stance (Alarm + Caution, %)", fontsize=12)
    ax.set_title("Critical stance by journal quality tier\n(pre-filtered discourse+evaluative papers; comparable corpora)",
                 fontsize=12, fontweight="bold")
    ax.legend(fontsize=10)
    ax.set_ylim(0, max(list(q1q2.values()) + list(q3.values())) + 8)
    fig.tight_layout()
    save(fig, "fig05_q3_comparison.png")


# ── Fig 06: Geographic critical stance ────────────────────────────────────────
def fig06_geography():
    rows = load_csv("geographic_stance.csv")
    if not rows:
        return

    # Filter meaningful regions
    rows = [r for r in rows if int(r.get("total","0")) >= 100
            and r["region"] != "Unknown"]
    rows.sort(key=lambda x: float(x.get("critical_pct","0")), reverse=True)

    regions    = [r["region"] for r in rows]
    crit_pcts  = [float(r.get("critical_pct","0")) for r in rows]
    alarm_pcts = [float(r.get("alarm_pct","0")) for r in rows]
    ns         = [int(r.get("total","0")) for r in rows]

    y = np.arange(len(regions))
    fig, ax = plt.subplots(figsize=(10, 5))

    colours = [CRITICAL_COLOUR if c > 25 else "#5D6D7E" for c in crit_pcts]
    bars = ax.barh(y, crit_pcts, color=colours, alpha=0.85)

    for i, (n, c, a) in enumerate(zip(ns, crit_pcts, alarm_pcts)):
        ax.text(c + 0.3, i, f"{c:.1f}%  (Alarm: {a:.1f}%)  n={n:,}",
                va="center", fontsize=9, color="#333")

    ax.set_yticks(y)
    ax.set_yticklabels(regions, fontsize=10)
    ax.set_xlabel("Critical stance (Alarm + Caution, %)", fontsize=12)
    ax.set_title("Critical stance toward AI by geographic region\n(Q1/Q2 discourse+evaluative papers, 2021–2025)",
                 fontsize=12, fontweight="bold")
    ax.axvline(22.6, color="#aaa", lw=1, ls="--", alpha=0.7)
    ax.text(22.8, -0.5, "Overall\nmean", fontsize=8, color="#888")
    ax.set_xlim(0, max(crit_pcts) + 18)
    fig.tight_layout()
    save(fig, "fig06_geography.png")


# ── Fig 07: Stance by publication type ────────────────────────────────────────
def fig07_pubtype():
    rows = load_csv("pubtype_stance.csv")
    if not rows:
        return

    # Order by critical pct descending
    rows.sort(key=lambda x: float(x.get("critical_pct","0")), reverse=True)
    types     = [r["sector"] for r in rows]
    alarm_p   = [float(r.get("Alarm","0")) / max(int(r.get("total","1")),1) * 100 for r in rows]
    caut_p    = [float(r.get("Caution","0")) / max(int(r.get("total","1")),1) * 100 for r in rows]
    opt_p     = [float(r.get("Cautious Optimism","0")) / max(int(r.get("total","1")),1) * 100 for r in rows]
    ns        = [int(r.get("total","0")) for r in rows]

    x = np.arange(len(types))
    w = 0.25
    fig, ax = plt.subplots(figsize=(12, 5))

    ax.bar(x - w, alarm_p, w, color=COLOURS["Alarm"],
           label="Alarm", alpha=0.88)
    ax.bar(x, caut_p, w, color=COLOURS["Caution"],
           label="Caution", alpha=0.88)
    ax.bar(x + w, opt_p, w, color=COLOURS["Cautious Optimism"],
           label="Cautious Optimism", alpha=0.88)

    for i, n in enumerate(ns):
        ax.text(i, max(alarm_p[i], caut_p[i], opt_p[i]) + 0.5,
                f"n={n:,}", ha="center", fontsize=8, color="#555")

    ax.set_xticks(x)
    ax.set_xticklabels(types, fontsize=10)
    ax.set_ylabel("% of papers", fontsize=12)
    ax.set_title("Stance toward AI by publication type\n(Q1/Q2 discourse+evaluative papers, 2021–2025)",
                 fontsize=12, fontweight="bold")
    ax.legend(fontsize=10)
    fig.tight_layout()
    save(fig, "fig07_pubtype.png")


# ── Fig 08: Volume growth ─────────────────────────────────────────────────────
def fig08_volume():
    rows = load_csv("02_stance_by_year.csv")
    if not rows:
        return

    rows = [r for r in rows if "2021" <= r["year"] <= "2025"]
    years  = [r["year"] for r in rows]
    totals = [int(r["total"]) for r in rows]
    alarm  = [float(r.get("Alarm_pct","0")) for r in rows]
    crit   = [float(r.get("critical_pct","0")) for r in rows]

    x = np.arange(len(years))
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True,
                                    gridspec_kw={"height_ratios": [2, 1]})

    # Top: volume bars coloured by critical pct
    bar_colours = plt.cm.RdYlGn_r(
        [(c - min(crit)) / (max(crit) - min(crit) + 0.001) for c in crit]
    )
    bars = ax1.bar(x, totals, color=bar_colours, alpha=0.85, edgecolor="white")
    for bar, t, y in zip(bars, totals, years):
        label = f"{t:,}*" if y == "2024" else f"{t:,}"
        ax1.text(bar.get_x() + bar.get_width()/2, t + 30, label,
                 ha="center", fontsize=10, fontweight="bold")
    # Add asterisk note
    ax1.text(0.02, 0.02, "* 2024 undercount due to publication lag",
             transform=ax1.transAxes, fontsize=8, color="#888", va="bottom", style="italic")

    ax1.set_ylabel("Discourse+evaluative papers\n(Q1/Q2 journals)", fontsize=11)
    ax1.set_title("Growth of AI discourse in Q1/Q2 medical journals, 2021–2025",
                  fontsize=12, fontweight="bold")

    # Bottom: critical stance line
    ax2.plot(x, crit, color=CRITICAL_COLOUR, lw=2.5, marker="o", ms=7, zorder=5)
    ax2.fill_between(x, 0, crit, color=CRITICAL_COLOUR, alpha=0.12)
    for xi, c in zip(x, crit):
        ax2.text(xi, c + 0.3, f"{c:.1f}%", ha="center", fontsize=9,
                 color=CRITICAL_COLOUR, fontweight="bold")
    ax2.set_ylabel("Critical stance %", fontsize=11)
    ax2.set_ylim(0, max(crit) + 5)
    # Flag 2024 if present
    if "2024" in years:
        idx_24 = years.index("2024")
        ax2.annotate("*", (idx_24, crit[idx_24] + 0.3), fontsize=12,
                     ha="center", color="#888")
    ax2.set_xticks(x)
    ax2.set_xticklabels(years, fontsize=11)
    ax2.set_xlabel("Publication year", fontsize=12)

    # ChatGPT marker on both panels
    cg_x = years.index("2022") + 0.5 if "2022" in years else None
    if cg_x:
        for axx in (ax1, ax2):
            axx.axvline(cg_x, color=CHATGPT_COLOUR, lw=1.2, ls="--", alpha=0.5)
        ax1.text(cg_x + 0.05, max(totals) * 0.92, "ChatGPT",
                 fontsize=8.5, color=CHATGPT_COLOUR)

    fig.tight_layout()
    save(fig, "fig08_volume_growth.png")


# ── main ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Figure Generator — AI Narratives Study")
    print(f"Reading from: {ANALYSIS_DIR}")
    print(f"Writing to:   {FIGURES_DIR}")
    print("="*55)
    print("NOTE: 2024 records are underrepresented due to PubMed indexing lag.")
    print("      Late-2024 papers appear as 2025 in PubMed metadata.")
    print("      Figures exclude 2026 (partial year: Jan-Apr only).")
    print("      2024 flagged with asterisk in annual figures.")

    fig01_stance_stream()
    fig02_alarm_arc()
    fig03_thematic_evolution()
    fig04_specialty()
    fig05_q3_comparison()
    fig06_geography()
    fig07_pubtype()
    fig08_volume()

    print("\nAll figures complete.")
    print(f"Open output/figures/ to review.")
