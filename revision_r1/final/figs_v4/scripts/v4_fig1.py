"""v4 (2026-11-04): copy of v3b/scripts/v3_figures.py; redraws Figure 1 only, without the human validation
samples column (covered by Table 1); canvas width cropped to the remaining content. Output: final/figs_v4/Fig1_v3.{png,pdf}.
All plotted numbers come from the same book IDs as v3. MA figures are not touched.

v3 figures: Figure 1 relabelled, three MA figures redrawn or new, and cleaned captions for all MA figures.

Every plotted or printed number is read from the numbers book (NUMBERS_BOOK_R1_v2.csv) by ID.
* Fig1_v3: identical drawing code to c2_figures.fig1; only the three "R1" labels change.
* temporal_robustness_fig: identical data; panel titles and legend labels without internal codes.
* terms_fig: both directions of each comparison (top 15 each way), so the terms that fell are shown.
* advocacy_measures_fig (new): the three measures of unqualified promotion.
Other MA figures: image copied unchanged; caption cleaned.
Fonts: Arial if installed, else Liberation Sans (metric-compatible with Arial).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'v3b' / 'scripts'))  # v3_common, read-only

import re
import shutil

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402

from v3_common import SRC, V3, Y5, book  # noqa: E402

plt.rcParams.update({"font.family": ["Arial", "Liberation Sans", "DejaVu Sans"], "font.size": 7, "axes.titlesize": 7,
                     "axes.labelsize": 7, "xtick.labelsize": 7, "ytick.labelsize": 7, "legend.fontsize": 7,
                     "pdf.fonttype": 42, "ps.fonttype": 42, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.linewidth": 0.6, "xtick.major.width": 0.6, "ytick.major.width": 0.6})
B = book()
W_IN, DPI = 7.5, 600
UF_IN = SRC / "ma" / "units" / "figures"
UF = V3 / "ma" / "units" / "figures"
FIGS = V3.parent / "figs_v4"
FIGS.mkdir(parents=True, exist_ok=True)
USED = {}


def n(fig, id_):
    USED.setdefault(fig, []).append(id_)
    r = B[id_]
    f = lambda x: float(x) if x not in ("", None) else float("nan")
    return {"point": f(r["point"]), "lo": f(r["lo"]), "hi": f(r["hi"]), "k": f(r["k"]), "n": f(r["n"]), "value": r["value"],
            "item": r["item"]}


def fn(x):
    x = int(round(float(x)))
    return f"{x:,}" if abs(x) >= 10000 else str(x)


def ci(lo, hi, d=1):
    a, b = f"{lo:.{d}f}%", f"{hi:.{d}f}%"
    return f"95% CI {a} to {b}" if (lo < 0 or hi < 0) else f"95% CI {a}-{b}"


def save(fig, path_stem):
    fig.savefig(f"{path_stem}.png", dpi=DPI)
    fig.savefig(f"{path_stem}.pdf")
    plt.close(fig)


def series(ax, fig_id, prefix, colour, label, ymax, marker="o", offset=0.0, show=True, below=False, fmt="{:.1f}"):
    pts = [n(fig_id, f"{prefix}-{y}") for y in Y5]
    p = np.array([x["point"] for x in pts]); lo = np.array([x["lo"] for x in pts]); hi = np.array([x["hi"] for x in pts])
    xs = np.array(Y5) + offset
    ax.errorbar(xs, p, yerr=[p - lo, hi - p], fmt="-" + marker, color=colour, ms=3, lw=1.0, elinewidth=0.6, capsize=1.6, label=label)
    if show:
        for x, v, h, l_ in zip(xs, p, hi, lo):
            if below:
                ax.text(x, l_ - ymax * 0.02, fmt.format(v), ha="center", va="top", fontsize=7, color=colour)
            else:
                ax.text(x, h + ymax * 0.02, fmt.format(v), ha="center", va="bottom", fontsize=7, color=colour)
    return p


# ------------------------------------------------------------------ Figure 1 (main text)
def fig1():
    F = "Fig1"
    c = lambda i: fn(n(F, i)["point"])
    H = 10.2
    fig = plt.figure(figsize=(W_IN, H))
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W_IN); ax.set_ylim(H, 0); ax.axis("off")
    LH = 0.128

    def box(x, y, w, text, bold_first=False, dashed=False, fs=7, fill="white", align="center"):
        lines = text.split("\n")
        h = len(lines) * LH + 0.12
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="square,pad=0", lw=0.8 if not dashed else 0.9,
                                    edgecolor="black", facecolor=fill, linestyle=(0, (4, 2)) if dashed else "solid"))
        tx = x + w / 2 if align == "center" else x + 0.07
        for i, ln in enumerate(lines):
            ax.text(tx, y + 0.06 + LH * (i + 0.5), ln, ha=align, va="center", fontsize=fs,
                    fontweight="bold" if (bold_first and i == 0) else "normal")
        return (x, y, w, h)

    def down(b1, b2):
        x = b1[0] + b1[2] / 2
        ax.annotate("", xy=(x, b2[1]), xytext=(x, b1[1] + b1[3]),
                    arrowprops=dict(arrowstyle="-|>", lw=0.8, color="black", mutation_scale=7))

    MX, MW = 0.15, 2.55
    EX, EW = 2.95, 2.45
    ax.text(MX, 0.12, "Main flow", fontsize=7, fontweight="bold", va="top")
    ax.text(EX, 0.12, "Exclusions (reason, n)", fontsize=7, fontweight="bold", va="top")
    fnr = n(F, "COR-AUDIT-FN"); mis = n(F, "COR-AUDIT-MISSED")
    stages = [
        (f"Identified\nPubMed records, monthly searches,\nJanuary 2021-April 2026\nn={c('COR-01')}", True, "white",
         f"Duplicate PMIDs across monthly searches,\nn={c('COR-02')}", False),
        (f"Screened\nUnique records\nn={c('COR-03')}", True, "white",
         f"Conference proceedings or preprints,\nn={c('COR-04')}", False),
        (f"Journal quartile assessed\n(SCImago Journal Rank)\nn={c('COR-05')}", True, "white",
         f"Not Q1/Q2 in SJR, n={c('COR-06')}\n- title not in SJR, n={c('COR-07')}\n- listed with no quartile, n={c('COR-08')}\n"
         f"- best quartile Q4, n={c('COR-09')}\nQ3 journals, n={c('COR-10')}\n(separate comparison arm)", False),
        (f"Q1/Q2 records\nn={c('COR-11')} ({n(F, 'COR-Q1Q2-PCT')['value'].split(' ')[0]} of records assessed)", False, "white",
         f"Analysis window 2021-2025\nOutside the window, n={c('COR-12')}\n- cover date May 2026 or later, n={c('COR-13')}\n"
         f"- January-April 2026, n={c('COR-14')}\n  (descriptive table only)\n- dated before 2021, n={c('COR-15')}", True),
        (f"Assessed for eligibility\nQ1/Q2 records published 2021-2025,\nscreened by the AI-engagement prefilter\n"
         f"(title + first 300 characters of abstract)\nn={c('COR-16')}", True, "white",
         f"Application (AI used as a method),\nn={c('COR-17')}\n- prefilter failures defaulted to\n  application, n={c('COR-18')}\n"
         f"Estimated AI-engaged among excluded\n(prefilter audit): {fnr['point']:.1f}% ({ci(fnr['lo'], fnr['hi'])}),\n"
         f"about {fn(mis['point'])} records", False),
        (f"AI-engaged records retained\nn={c('COR-19')}\n(discourse {c('COR-20')}; evaluative {c('COR-21')})", False, "white",
         f"Stance classification unparseable,\nn={c('COR-22')}", False),
        (f"Included in analysis\nValid stance, 2021-2025\nn={c('COR-23')}\n(discourse {c('COR-24')}; evaluative {c('COR-25')})",
         True, "#EEEEEE", None, False),
    ]
    hgt = lambda t: len(t.split("\n")) * LH + 0.12
    y = 0.35
    prev = None
    for txt, bold, fill, excl, dashed in stages:
        b = box(MX, y, MW, txt, bold, fill=fill)
        if prev is not None:
            down(prev, b)
        prev = b
        if excl is None:
            break
        he = hgt(excl)
        gap = max(0.42, he + 0.22)
        ym = b[1] + b[3] + gap / 2
        box(EX, ym - he / 2, EW, excl, dashed, dashed=dashed, align="left")
        ax.annotate("", xy=(EX, ym), xytext=(MX + MW / 2, ym),
                    arrowprops=dict(arrowstyle="-|>", lw=0.8, color="black", mutation_scale=7))
        y = b[1] + b[3] + gap
    b7 = prev
    y = b7[1] + b7[3] + 0.5
    ax.text(EX + 0.72, b7[1] + b7[3] + 0.25, "Analytic subsets", fontsize=7, fontweight="bold", va="center")
    s1 = box(MX, y, 1.22, f"Critical\n(Alarm or Caution)\nn={c('COR-SUB-01')}\nTheme-labelled\nn={c('COR-SUB-02')}")
    s2 = box(MX + 1.33, y, 1.22, f"Specialty valid\nn={c('COR-SUB-08')}\n(FAILED n={c('COR-SUB-09')})")
    s3 = box(EX, y, 1.15, f"Country resolved\nn={c('COR-SUB-10')}\n(unresolved\nn={c('COR-SUB-11')})")
    s4 = box(EX + 1.3, y, 1.15, f"Region known\nn={c('COR-SUB-13')}\n(Unknown\nn={c('COR-SUB-14')})")
    for s in (s1, s2):
        ax.annotate("", xy=(s[0] + s[2] / 2, s[1]), xytext=(MX + MW / 2, b7[1] + b7[3]),
                    arrowprops=dict(arrowstyle="-|>", lw=0.6, color="black", mutation_scale=6))
    for s in (s3, s4):
        ax.annotate("", xy=(s[0] + s[2] / 2, s[1]), xytext=(MX + MW, b7[1] + b7[3] - 0.12),
                    arrowprops=dict(arrowstyle="-|>", lw=0.6, color="black", mutation_scale=6,
                                    connectionstyle="angle,angleA=0,angleB=90"))
    y2 = s1[1] + s1[3] + 0.25
    s5 = box(MX, y2, 2.55, f"Abstract-present critical, mechanism parsed\nn={c('COR-SUB-06')} (mechanism FAILED "
             f"n={c('COR-SUB-03')};\ntitle-only n={c('COR-SUB-05')})")
    down(s1, (MX, y2, 1.22, 0))
    y3 = s5[1] + s5[3] + 0.25
    box(MX, y3, 2.55, f"Hallucination-gated, abstract-present\ncritical records, n={c('COR-SUB-07')}")
    down((MX, s5[1], 2.55, s5[3]), (MX, y3, 2.55, 0))
    W_OUT = EX + EW + MX  # content width plus the same margin on both sides
    ax.set_xlim(0, W_OUT); ax.set_ylim(y3 + 0.7, 0)
    fig.set_size_inches(W_OUT, y3 + 0.7)
    save(fig, FIGS / "Fig1_v3")


# ------------------------------------------------------------------ MA figures
def temporal_robustness():
    F = "temporal_robustness_fig"
    fig, axes = plt.subplots(2, 2, figsize=(W_IN, 5.6))
    corp = [("A", "(a) Production", "#000000", "o"), ("B", "(b) Augmented", "#0072B2", "s"),
            ("C", "(c) Precision-weighted", "#56B4E9", "^"), ("D", "(d) Full abstract", "#E69F00", "D")]
    for ax, out, lab, ym in ((axes[0, 0], "CRITICAL", "critical", 40), (axes[0, 1], "ADVOCACY", "Advocacy", 5)):
        for j, (c, l_, col, mk) in enumerate(corp):
            series(ax, F, f"RES-B2ANN-{c}-{out}", col, l_, ym, marker=mk, offset=(j - 1.5) * 0.08, show=(c == "A"))
        ax.set_ylim(0, ym); ax.set_xticks(Y5); ax.grid(axis="y", lw=0.3, color="#DDDDDD")
        ax.legend(frameon=False, fontsize=7, loc="lower right" if out == "CRITICAL" else "upper right")
        ax.set_ylabel(f"{'Critical' if out == 'CRITICAL' else 'Advocacy'}, % of records")
        ax.text(0.02, 1.02, f"Prefilter-defined corpora: {lab}", transform=ax.transAxes, fontweight="bold")
    defs = [("FULL", "Full corpus", "#000000", "o"), ("D1", "Medicine area", "#0072B2", "s"),
            ("D2", "Medicine area without Medicine (misc.)", "#56B4E9", "^"), ("D3", "Broad health sciences", "#E69F00", "D")]
    for ax, out, lab, ym in ((axes[1, 0], "CRITICAL", "critical", 40), (axes[1, 1], "ADVOCACY", "Advocacy", 5)):
        for j, (c, l_, col, mk) in enumerate(defs):
            series(ax, F, f"RES-B5ANN-{c}-{out}", col, l_, ym, marker=mk, offset=(j - 1.5) * 0.08, show=(c == "FULL"))
        if out == "ADVOCACY":
            series(ax, F, "RES-TMP-SE", "#CC79A7", "Strong endorsement (symmetric scale), full corpus", ym, marker="v", show=False)
        ax.set_ylim(0, ym if out == "CRITICAL" else 27); ax.set_xticks(Y5); ax.grid(axis="y", lw=0.3, color="#DDDDDD")
        ax.legend(frameon=False, fontsize=7, loc="lower right" if out == "CRITICAL" else "upper right")
        ax.set_ylabel(f"{'Critical' if out == 'CRITICAL' else 'Advocacy or strong endorsement'}, % of records")
        ax.text(0.02, 1.02, f"SJR medical-category definitions: {lab}", transform=ax.transAxes, fontweight="bold")
    for x, r in zip(Y5, [n(F, f"RES-TMP-SE-{y}") for y in Y5]):
        axes[1, 1].text(x, r["hi"] + 0.3, f"{r['point']:.1f}", ha="center", va="bottom", fontsize=7, color="#CC79A7")
    fig.tight_layout(h_pad=2.2)
    save(fig, UF / F)
    return ("**Critical and Advocacy trends under alternative corpus definitions and a symmetric endorsement scale, 2021-2025.** "
            "Top: the four prefilter-defined corpora ((a) production; (b) augmented with records recovered by the full-abstract "
            "prefilter reclassification; (c) augmented with precision weights; (d) full-abstract corpus). Bottom: the full corpus and "
            "three SJR medical-category restrictions, with the strong-endorsement share from the symmetric stance scale (all records "
            "as denominator) beside Advocacy. Points show annual estimates and whiskers 95% percentile bootstrap CIs (1000 joint "
            "resamples, seed 42); values are printed for the reference series (production corpus or full corpus, black) and for "
            "strong endorsement; every value with n/N for the other series is in {{T:corpus_sensitivity}}, {{T:sjr_sensitivity}} and "
            "{{T:symmetric_endorsement}}. Points are offset horizontally within each year for legibility. Critical stance was Alarm "
            "or Caution.")


def corr_const(id_):
    v = B[id_]["value"]
    m = re.search(r"constant-rate \(T2, pre-specified\) ([\d.]+)% \(95% CI ([\d.]+)%-([\d.]+)%\)", v)
    assert m, v
    return float(m[1]), float(m[2]), float(m[3])


def advocacy_measures():
    F = "advocacy_measures_fig"
    fig, ax = plt.subplots(figsize=(W_IN * 0.72, 3.3))
    ym = 16
    series(ax, F, "RES-TMP-SE", "#CC79A7", "Strong endorsement (symmetric stance scale)", ym, marker="v", offset=0.0)
    cc = [corr_const(f"VAL-ST-PER-CORR-ADVOCACY-{y}") for y in Y5]
    USED.setdefault(F, []).extend(f"VAL-ST-PER-CORR-ADVOCACY-{y}" for y in Y5)
    p = np.array([x[0] for x in cc]); lo = np.array([x[1] for x in cc]); hi = np.array([x[2] for x in cc])
    xs = np.array(Y5) + 0.1
    ax.errorbar(xs, p, yerr=[p - lo, hi - p], fmt="-s", color="#E69F00", ms=3, lw=1.0, elinewidth=0.6, capsize=1.6,
                label="Misclassification-corrected Advocacy (constant rates)")
    for x, v in zip(xs, p):
        ax.text(x + 0.06, v + 0.35, f"{v:.2f}", ha="left", va="bottom", fontsize=7, color="#B07800")
    series(ax, F, "RES-TMP-ADV", "#0072B2", "Classifier Advocacy label", ym, marker="o", offset=-0.1, below=True)
    ax.set_ylim(0, ym); ax.set_xlim(2020.6, 2025.5); ax.set_xticks(Y5)
    ax.set_ylabel("% of records"); ax.grid(axis="y", lw=0.3, color="#DDDDDD")
    h, l_ = ax.get_legend_handles_labels()
    order = [l_.index(x) for x in ("Classifier Advocacy label", "Strong endorsement (symmetric stance scale)",
                                   "Misclassification-corrected Advocacy (constant rates)")]
    ax.legend([h[i] for i in order], [l_[i] for i in order], frameon=False, loc="upper right")
    fig.tight_layout()
    save(fig, UF / F)
    adv_or = n(F, "RES-TMP-ADV-OR")["value"]; se_or = n(F, "RES-TMP-SE-OR")["value"]
    d = B["VAL-ST-PER-CORR-ADVOCACY-DELTA"]["value"]
    m = re.search(r"constant-rate \(T2, pre-specified\) (-[\d.]+) percentage points \(95% CI (-[\d.]+) to (-[\d.]+)\)", d)
    assert m, d
    USED[F].append("VAL-ST-PER-CORR-ADVOCACY-DELTA")
    return ("**Three measures of unqualified promotion, 2021-2025.** Classifier Advocacy label: share of records the stance "
            "classifier labelled Advocacy (records per year: 2021 1063, 2022 1343, 2023 2054, 2024 3700, 2025 5898). Strong "
            "endorsement: share of all records flagged as strong endorsement on the symmetric stance scale, which does not require "
            "transformative language ({{T:symmetric_endorsement}}). Misclassification-corrected Advocacy: estimated share of records "
            "the human coder would label Advocacy, from the prespecified constant-rate correction ({{T:corrected_prevalence}}; "
            "{{N:note_correction_estimator}}). Points show annual estimates and whiskers 95% CIs (percentile bootstrap, 1000 "
            "resamples, seed 42; for the corrected series, validation records resampled within model label jointly with corpus "
            "records); printed values are point estimates (%). Points are offset horizontally within each year for legibility. "
            f"Record-level logistic regression on publication year (journal cluster-robust SEs): Advocacy {adv_or}; strong "
            f"endorsement {se_or}. Corrected Advocacy, change 2025 minus 2021: {m[1]} percentage points (95% CI {m[2]} to {m[3]}).")


def terms():
    F = "terms_fig"
    fig, axes = plt.subplots(1, 2, figsize=(W_IN, 6.2))
    spec = ((axes[0], "EMERG", "2024-2025 vs 2021-2022 records", "#0072B2", "#E69F00",
             "more in 2024-2025", "more in 2021-2022"),
            (axes[1], "STANCE", "Critical vs favourable records", "#D55E00", "#0072B2", "more in critical", "more in favourable"))
    for ax, tag, title, cpos, cneg, lpos, lneg in spec:
        pos = [n(F, f"RES-B6-{tag}-{i:02d}") for i in range(1, 16)]
        neg = [n(F, f"RES-B6-{tag}-{i:02d}") for i in range(31, 46)]
        assert all(x["point"] > 0 for x in pos) and all(x["point"] < 0 for x in neg)
        assert all(a["point"] >= b["point"] for a, b in zip(pos, pos[1:])) and all(a["point"] <= b["point"] for a, b in zip(neg, neg[1:]))
        rows = [(x["item"].split(": ", 1)[1], x["point"]) for x in pos] + [None] + \
               [(x["item"].split(": ", 1)[1], x["point"]) for x in neg[::-1]]
        ys = list(range(len(rows)))[::-1]
        labels = []
        for y, r in zip(ys, rows):
            if r is None:
                labels.append(""); continue
            t, z = r
            col = cpos if z > 0 else cneg
            ax.scatter([z], [y], color=col, s=12, zorder=3)
            right = z > 0 or z < -12
            ax.text(z + (0.5 if right else -0.5), y, f"{z:.1f}", va="center", ha="left" if right else "right", fontsize=7)
            labels.append(t)
        ax.set_yticks(ys); ax.set_yticklabels(labels)
        ax.tick_params(axis="y", length=0)
        ax.axvline(0, color="#444444", lw=0.6)
        ax.set_xlim(-22, 21); ax.set_ylim(-1.6, len(rows) + 0.6); ax.set_xticks([-20, -10, 0, 10, 20]); ax.grid(axis="x", lw=0.3, color="#DDDDDD")
        ax.set_xlabel("z score (weighted log-odds)")
        ax.text(0.0, 1.01, title, transform=ax.transAxes, fontweight="bold", va="bottom")
        ax.text(20.5, len(rows) - 0.1, lpos, ha="right", va="center", color=cpos)
        ax.text(-21.5, -1.1, lneg, ha="left", va="center", color=cneg)
    fig.tight_layout(w_pad=1.5)
    save(fig, UF / F)
    return ("**MeSH and keyword terms that differed most by period and by stance, 2021-2025.** Left: records published 2024-2025 "
            "vs 2021-2022; right: critical vs favourable records. For each comparison, the 15 terms most over-represented in each "
            "direction, ranked by the z score of the weighted log-odds ratio with an informative Dirichlet prior (Monroe et al. 2008; "
            "terms present in at least 20 records). Positive z: more frequent in 2024-2025 or in critical records; negative z: more "
            "frequent in 2021-2022 or in favourable records. Printed values are z scores. The top 30 terms in each direction, with "
            "record counts, are in {{T:lexicon_and_terms}}. Critical stance was Alarm or Caution; favourable stance was Cautious "
            "Optimism or Advocacy.")


V2_NOTE = (" Version 2 (Batch 2d): every OR per year here comes from record-level logistic regression on publication year with "
           "journal cluster-robust SEs (95% CI and P from the cluster-robust covariance); point estimates are unchanged.")
OR_NOTE = " OR per year: record-level logistic regression on publication year with journal cluster-robust SEs."


def cleaned_caption(uid):
    p = UF_IN / f"{uid}_caption_v2.md"
    cap = (p if p.exists() else UF_IN / f"{uid}_caption.md").read_text(encoding="utf-8").strip()
    edits = {
        "within_genre_fig": [(V2_NOTE, OR_NOTE)],
        "other_themes_fig": [(V2_NOTE, OR_NOTE)],
        "lexicon_vs_llm_fig": [(V2_NOTE, OR_NOTE), ("(Multimedia Appendix 1, Note 10)", "({{N:note_mesh_keywords}})")],
        "theme_counts_fig": [("CIs for the shares are in {{T:themes}} and the R1 numbers book.",
                              "Annual shares with 95% CIs are in Figure 2 (headline themes) and {{F:other_themes_fig}} (other "
                              "themes); pooled shares are in {{T:themes}}.")],
        "forward_validation_sankey": [("(unchanged; exploratory and Advocacy-only)", "(Advocacy only)"),
                                      ("The figure is reproduced unchanged from the submission (its evidence window extends to "
                                       "April 2026 by design). ", "The evidence window extends to April 2026 by design. "),
                                      ("The Tier x verdict matrix", "The tier by verdict matrix")],
        "generative_share_fig": [], "country_map_20": [], "q3_fig": [],
    }[uid]
    for old, new in edits:
        assert cap.count(old) == 1, (uid, old)
        cap = cap.replace(old, new)
    return cap


def main():
    fig1()
    with open(FIGS / "figure_ids_used_v4.csv", "w", encoding="utf-8") as f:
        f.write("figure,id\n")
        for k, v in USED.items():
            for i in v:
                f.write(f"{k},{i}\n")
    print("Fig1 v4 done")


if __name__ == "__main__":
    main()
