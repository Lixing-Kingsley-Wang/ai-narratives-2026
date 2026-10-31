"""Batch 2d copy of c2_figures.py: v2 book; rewrites only the captions of Figures 2 and 3
(Fig2_caption_v2.md, Fig3_caption_v2.md); figures are not redrawn.

C2 · Main figures 1-6, final (JMIR R1 Batch 2c; E9, E10, D3, D4a, D4b, X3).

Every plotted value and every printed number is read from the numbers book
(NUMBERS_BOOK_R1.csv) by ID, so figures, captions and the book cannot drift.
2021-2025 only; nothing from 2026 is drawn. Figures are drawn at final printed
size (7.5 in wide), text >= 7 pt, PNG at 600 dpi plus vector PDF, colour-blind
safe palette (Okabe-Ito) with fixed stance colours, no in-figure titles, no
significance marks, no simple bar graphs, no fitted line on the FDA panel.

Run with the project venv (geopandas for Figure 5).
Outputs: revision_r1/final/figures/Fig{1..6}.{png,pdf}, Fig{1..6}_caption.md,
         figure_ids_used.csv (book IDs per figure, for C6 QA).
"""

from __future__ import annotations

import csv
import re

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.patches import FancyBboxPatch, Rectangle  # noqa: E402

import c_common as _cc  # Batch 2d: read the v2 numbers book (journal cluster-robust ORs)
_cc.BOOK_CSV = _cc.FINAL / "NUMBERS_BOOK_R1_v2.csv"
from c_common import (FIGS, HEADLINE_THEMES, REPO, STANCE_COLOURS, Y5, c_book, ci, fn, rc)  # noqa: E402

plt.rcParams.update({"font.family": ["Arial", "DejaVu Sans"], "font.size": 7, "axes.titlesize": 7,
                     "axes.labelsize": 7, "xtick.labelsize": 7, "ytick.labelsize": 7, "legend.fontsize": 7,
                     "pdf.fonttype": 42, "ps.fonttype": 42, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.linewidth": 0.6, "xtick.major.width": 0.6, "ytick.major.width": 0.6})
BOOK = c_book()
USED = []          # (figure, id)
W_IN = 7.5
DPI = 600
FM_COL = {"Confabulation (fabrication only)": "#D55E00", "Both": "#CC79A7",
          "Misclassification (factual error)": "#0072B2", "None or unclear": "#BBBBBB"}


def g(fig, id_):
    USED.append((fig, id_))
    r = BOOK[id_]
    f = lambda x: float(x) if x not in ("", None) else np.nan
    return {"point": f(r["point"]), "lo": f(r["lo"]), "hi": f(r["hi"]), "k": f(r["k"]), "n": f(r["n"]),
            "p": f(r["p"]), "value": r["value"]}


def save(fig, name):
    plt.close(fig)   # Batch 2d: figure unchanged


def caption(name, title, text):
    (FIGS / f"{name}_caption_v2.md").write_text(f"**{title}** {text}\n", encoding="utf-8")


def slug(s):
    s = re.sub(r"[^A-Za-z0-9]+", "", s.replace("&", "and").replace("/", " ").title())
    return s[:24].upper()


def panel_letter(ax, letter, x=-0.02, y=1.02):
    ax.text(x, y, letter, transform=ax.transAxes, fontsize=9, fontweight="bold", va="bottom", ha="right")


def series_plot(ax, fig, prefix, colour, label, ymax=None, fmt="{:.1f}"):
    pts = [g(fig, f"{prefix}-{y}") for y in Y5]
    p = np.array([x["point"] for x in pts]); lo = np.array([x["lo"] for x in pts]); hi = np.array([x["hi"] for x in pts])
    ax.errorbar(Y5, p, yerr=[p - lo, hi - p], fmt="-o", color=colour, ms=3.2, lw=1.0, elinewidth=0.7, capsize=1.8,
                ecolor="#333333")
    top = ymax or max(hi) * 1.28
    for x, v, h in zip(Y5, p, hi):
        ax.text(x, h + top * 0.025, fmt.format(v), ha="center", va="bottom", fontsize=7)
    ax.set_ylim(0, top)
    ax.set_xlim(2020.5, 2025.5)
    ax.set_xticks(Y5)
    ax.set_xticklabels([str(y) for y in Y5], rotation=45)
    ax.text(0.03, 0.98, label, transform=ax.transAxes, ha="left", va="top", fontsize=7, fontweight="bold")
    ax.grid(axis="y", lw=0.3, color="#DDDDDD")
    return pts


def or_text(fig, id_):
    v = g(fig, id_)["value"]
    return v


# ---------------------------------------------------------------------------
# Figure 1 · JARS flowchart
# ---------------------------------------------------------------------------
def fig1():
    F = "Fig1"
    c = lambda i: fn(g(F, i)["point"])
    sub = lambda i: fn(g(F, i)["point"])
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

    def right(b1, b2, y=None):
        y = y if y is not None else b2[1] + b2[3] / 2
        ax.annotate("", xy=(b2[0], y), xytext=(b1[0] + b1[2], y),
                    arrowprops=dict(arrowstyle="-|>", lw=0.8, color="black", mutation_scale=7))

    MX, MW = 0.15, 2.55          # main column
    EX, EW = 2.95, 2.45          # exclusion column
    VX, VW = 5.6, 1.78           # validation column
    ax.text(MX, 0.12, "Main flow", fontsize=7, fontweight="bold", va="top")
    ax.text(EX, 0.12, "Exclusions (reason, n)", fontsize=7, fontweight="bold", va="top")
    ax.text(VX, 0.12, "Human validation samples", fontsize=7, fontweight="bold", va="top")

    fnr = g(F, "COR-AUDIT-FN"); mis = g(F, "COR-AUDIT-MISSED")
    stages = [
        (f"Identified\nPubMed records, monthly searches,\nJanuary 2021-April 2026\nn={c('COR-01')}", True, "white",
         f"Duplicate PMIDs across monthly searches,\nn={c('COR-02')}", False),
        (f"Screened\nUnique records\nn={c('COR-03')}", True, "white",
         f"Conference proceedings or preprints,\nn={c('COR-04')}", False),
        (f"Journal quartile assessed\n(SCImago Journal Rank)\nn={c('COR-05')}", True, "white",
         f"Not Q1/Q2 in SJR, n={c('COR-06')}\n- title not in SJR, n={c('COR-07')}\n- listed with no quartile, n={c('COR-08')}\n"
         f"- best quartile Q4, n={c('COR-09')}\nQ3 journals, n={c('COR-10')}\n(separate comparison arm)", False),
        (f"Q1/Q2 records\nn={c('COR-11')} ({g(F, 'COR-Q1Q2-PCT')['value'].split(' ')[0]} of records assessed)", False, "white",
         f"R1 analysis window 2021-2025\nOutside the window, n={c('COR-12')}\n- cover date May 2026 or later, n={c('COR-13')}\n"
         f"- January-April 2026, n={c('COR-14')}\n  (descriptive table only)\n- dated before 2021, n={c('COR-15')}", True),
        (f"Assessed for eligibility\nQ1/Q2 records published 2021-2025,\nscreened by the AI-engagement prefilter\n"
         f"(title + first 300 characters of abstract)\nn={c('COR-16')}", True, "white",
         f"Application (AI used as a method),\nn={c('COR-17')}\n- prefilter failures defaulted to\n  application, n={c('COR-18')}\n"
         f"Estimated AI-engaged among excluded\n(R1 audit): {fnr['point']:.1f}% ({ci(fnr['lo'], fnr['hi'])}),\n"
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

    # downstream subsets
    y = b7[1] + b7[3] + 0.5
    ax.text(EX + 0.72, b7[1] + b7[3] + 0.25, "Analytic subsets", fontsize=7, fontweight="bold", va="center")
    s1 = box(MX, y, 1.22, f"Critical\n(Alarm or Caution)\nn={sub('COR-SUB-01')}\nTheme-labelled\nn={sub('COR-SUB-02')}")
    s2 = box(MX + 1.33, y, 1.22, f"Specialty valid\nn={sub('COR-SUB-08')}\n(FAILED n={sub('COR-SUB-09')})")
    s3 = box(EX, y, 1.15, f"Country resolved\nn={sub('COR-SUB-10')}\n(unresolved\nn={sub('COR-SUB-11')})")
    s4 = box(EX + 1.3, y, 1.15, f"Region known\nn={sub('COR-SUB-13')}\n(Unknown\nn={sub('COR-SUB-14')})")
    for s in (s1, s2):
        ax.annotate("", xy=(s[0] + s[2] / 2, s[1]), xytext=(MX + MW / 2, b7[1] + b7[3]),
                    arrowprops=dict(arrowstyle="-|>", lw=0.6, color="black", mutation_scale=6))
    for s in (s3, s4):
        ax.annotate("", xy=(s[0] + s[2] / 2, s[1]), xytext=(MX + MW, b7[1] + b7[3] - 0.12),
                    arrowprops=dict(arrowstyle="-|>", lw=0.6, color="black", mutation_scale=6,
                                    connectionstyle="angle,angleA=0,angleB=90"))
    y2 = s1[1] + s1[3] + 0.25
    s5 = box(MX, y2, 2.55, f"Abstract-present critical, mechanism parsed\nn={sub('COR-SUB-06')} (mechanism FAILED "
             f"n={sub('COR-SUB-03')};\ntitle-only n={sub('COR-SUB-05')})")
    down(s1, (MX, y2, 1.22, 0))
    y3 = s5[1] + s5[3] + 0.25
    s6 = box(MX, y3, 2.55, f"Hallucination-gated, abstract-present\ncritical records, n={sub('COR-SUB-07')}")
    down((MX, s5[1], 2.55, s5[3]), (MX, y3, 2.55, 0))

    # validation column
    def val_text(design_id, title):
        return title
    vy = 0.35
    vals = [
        ("Prefilter, development pilot", "n=200; unweighted; sampling\nundocumented; no written codebook"),
        ("Prefilter, R1 audit", "n=370; stratified by prefilter outcome\nx year, design-weighted (75 excluded,\n"
                                "full-abstract keep; 225 excluded,\nfull-abstract drop; 50 retained;\n20 pilot records recoded)"),
        ("Stance", "n=300; stratified by model stance;\n225 in scope"),
        ("Themes", "n=200 critical records; 40 per\nyear, simple random sampling"),
        ("Mechanism", "n=120 critical records; stratified\nby year and failure mode;\n108 with an abstract"),
        ("Specialty", "n=120; stratified by model\nspecialty; 'unclear' option"),
    ]
    for t, d in vals:
        b = box(VX, vy, VW, f"{t}\n{d}", True, fs=7, align="left")
        vy = b[1] + b[3] + 0.14
    ax.text(VX, vy + 0.02, "One coder, blinded to model\nlabels, for every sample.", fontsize=7, va="top")
    ax.set_ylim(max(y3 + 0.7, vy + 0.4), 0)
    fig.set_size_inches(W_IN, max(y3 + 0.7, vy + 0.4))
    save(fig, F)
    caption(F, "Figure 1. Flow of records from retrieval to the 2021-2025 analytic corpus, with exclusions and human validation samples.",
            f"Boxes on the left follow the JARS stages (identified, screened, assessed for eligibility, included in analysis) "
            f"applied to bibliographic records; boxes in the middle give each exclusion with its reason and n. The dashed box marks "
            f"the R1 analysis window (2021-2025), which replaces the April 2026 cover-date cutoff; January-April 2026 records "
            f"(n={c('COR-14')}) appear only in a descriptive supplementary table. The estimate of AI-engaged records among those "
            f"excluded by the prefilter comes from the R1 prefilter audit (design-weighted 1-NPV, Jeffreys interval; Multimedia "
            f"Appendix 3). The analytic subsets show the denominators for the theme, mechanism, specialty and geography analyses. "
            f"Critical stance was Alarm or Caution. The right-hand column lists every human validation sample with its n and design; "
            f"agreement statistics are in Table 1. Q: SCImago Journal Rank quartile; PMID: PubMed identifier.")


# ---------------------------------------------------------------------------
# Figure 2 · temporal trends
# ---------------------------------------------------------------------------
def fig2():
    F = "Fig2"
    fig, axes = plt.subplots(2, 5, figsize=(W_IN, 4.6))
    stance = [("ALARM", "Alarm"), ("CAUT", "Caution"), ("NEUT", "Neutral"), ("CO", "Cautious Optimism"), ("ADV", "Advocacy")]
    for ax, (code, s) in zip(axes[0], stance):
        pts = series_plot(ax, F, f"RES-TMP-{code}", STANCE_COLOURS[s], s,
                          ymax=88 if code == "CO" else max(x["hi"] for x in [g(F, f"RES-TMP-{code}-{y}") for y in Y5]) * 1.42)
    axes[0][0].set_ylabel("% of records (n=14,058)")
    themes = [(slug(t), t) for t in HEADLINE_THEMES]
    from c_common import THEME_COLOURS
    for ax, (code, t) in zip(axes[1], themes):
        series_plot(ax, F, f"RES-TMP-TH-{code}", THEME_COLOURS[t], t, ymax=90)
    axes[1][0].set_ylabel("% of critical records (n=4283)")
    axes[1][4].axis("off")
    ns = [fn(g(F, f"RES-TMP-CRIT-{y}")["n"]) for y in Y5]
    nc = [fn(g(F, f"RES-TMP-CRIT-{y}")["k"]) for y in Y5]
    axes[1][4].text(0.0, 0.95, "Records per year:\nall (critical)\n" + "\n".join(f"{y}: {a} ({b})" for y, a, b in zip(Y5, ns, nc)),
                    va="top", ha="left", fontsize=7, transform=axes[1][4].transAxes)
    panel_letter(axes[0][0], "a", -0.35); panel_letter(axes[1][0], "b", -0.35)
    fig.subplots_adjust(left=0.07, right=0.99, top=0.97, bottom=0.09, wspace=0.42, hspace=0.5)
    save(fig, F)
    ors = "; ".join(f"{lab} {g(F, f'RES-TMP-{code}-OR')['value']}" for code, lab in
                    (("CRIT", "critical"), ("ADV", "Advocacy")))
    ths = "; ".join(f"{t} {g(F, f'RES-TMP-TH-{slug(t)}-OR')['value']}" for t in HEADLINE_THEMES)
    rho = "; ".join(f"{s} {g(F, f'RES-TMP-{code}-RHO')['value']}" for code, s in stance)
    caption(F, "Figure 2. Annual evaluative stance and headline concern themes, 2021-2025.",
            f"(a) Annual share of each stance category among {fn(14058)} records with a valid stance (per-year n: "
            f"{', '.join(f'{y} {a}' for y, a in zip(Y5, ns))}). (b) Annual prevalence of the four headline concern themes among "
            f"{4283} critical records (per-year n: {', '.join(f'{y} {b}' for y, b in zip(Y5, nc))}); themes were multilabel (one to "
            f"three per record), so prevalences do not sum to 100%. Critical stance was Alarm or Caution; favourable stance was "
            f"Cautious Optimism or Advocacy. Points show annual estimates and whiskers 95% percentile bootstrap CIs (1000 joint "
            f"resamples of records, seed 42); printed values are the point estimates (%). Record-level logistic regression of the "
            f"outcome on publication year (unadjusted; journal cluster-robust SEs): {ors}; {ths}. Spearman correlation of the five annual values with year "
            f"(exact permutation P): {rho}.")


# ---------------------------------------------------------------------------
# Figure 3 · failure mechanism
# ---------------------------------------------------------------------------
def fig3():
    F = "Fig3"
    fig, (a, b) = plt.subplots(1, 2, figsize=(W_IN, 3.7), gridspec_kw={"width_ratios": [1.15, 1]})
    comp = [("FM-CONF", "Confabulation (fabrication only)"), ("FM-BOTH", "Both"),
            ("FM-MIS", "Misclassification (factual error)"), ("FM-NONE", "None or unclear")]
    tab = {code: [] for code, _ in comp}
    for i, y in enumerate(Y5):
        bottom = 0
        n = None
        for code, lab in comp:
            r = g(F, f"RES-TMP-{code}-{y}")
            n = r["n"]
            v = r["point"]
            a.bar(i, v, bottom=bottom, color=FM_COL[lab], width=0.62, edgecolor="white", lw=0.4,
                  label=lab if i == 0 else None)
            if v >= 6:
                a.text(i, bottom + v / 2, f"{v:.1f}", ha="center", va="center", fontsize=7,
                       color="white" if lab in ("Misclassification (factual error)", "Confabulation (fabrication only)") else "black")
            tab[code].append(v)
            bottom += v
        a.text(i, 101.5, f"n={fn(n)}", ha="center", va="bottom", fontsize=7)
    a.set_xticks(range(5)); a.set_xticklabels([str(y) for y in Y5]); a.set_xlim(-0.5, 4.95); a.set_ylim(0, 108)
    a.set_ylabel("% of hallucination-gated records")
    short = {"FM-CONF": "Fabrication only", "FM-BOTH": "Both", "FM-MIS": "Factual error", "FM-NONE": "None or unclear"}
    from matplotlib.transforms import blended_transform_factory
    tr = blended_transform_factory(a.transData, a.transAxes)
    for r_, (code, lab) in enumerate(reversed(comp)):
        yy = -0.15 - r_ * 0.075
        a.add_patch(Rectangle((-0.62, yy - 0.022), 0.12, 0.044, transform=tr, color=FM_COL[lab], clip_on=False))
        a.text(-0.68, yy, short[code], transform=tr, fontsize=7, va="center", ha="right")
        for i, v in enumerate(tab[code]):
            a.text(i, yy, f"{v:.1f}", transform=tr, fontsize=7, va="center", ha="center")
    for code, lab, col, mk in (("GENSHARE", "Generative-model share", "#0072B2", "o"),
                               ("FAB-ALL", "Fabrication share", "#D55E00", "s")):
        pts = [g(F, f"RES-TMP-{code}-{y}") for y in Y5]
        p = np.array([x["point"] for x in pts]); lo = np.array([x["lo"] for x in pts]); hi = np.array([x["hi"] for x in pts])
        b.errorbar(Y5, p, yerr=[p - lo, hi - p], fmt="-" + mk, color=col, ms=3.2, lw=1.0, elinewidth=0.7, capsize=1.8,
                   label=lab)
        for x, v, h, l_ in zip(Y5, p, hi, lo):
            if code == "GENSHARE":
                b.text(x - 0.12, h + 1.5, f"{v:.1f}", ha="right" if x > 2021 else "center", va="bottom", fontsize=7, color=col)
            else:
                b.text(x + 0.12, l_ - 1.5, f"{v:.1f}", ha="left", va="top", fontsize=7, color=col)
    b.set_xticks(Y5); b.set_xlim(2020.6, 2025.6); b.set_ylim(-5, 75)
    b.set_ylabel("% of abstract-present critical records")
    b.legend(loc="upper left", frameon=False)
    b.grid(axis="y", lw=0.3, color="#DDDDDD")
    panel_letter(a, "a", -0.1); panel_letter(b, "b", -0.12)
    fig.subplots_adjust(left=0.17, right=0.99, top=0.93, bottom=0.33, wspace=0.3)
    save(fig, F)
    ng = int(g(F, "COR-SUB-07")["point"]); na = int(g(F, "COR-SUB-06")["point"])
    caption(F, "Figure 3. Failure mechanism among critical records, 2021-2025.",
            f"(a) Annual failure-mode composition among {ng} hallucination-gated, abstract-present critical records (critical "
            f"records assigned the hallucination/errors theme). Each bar sums to 100%; the table under the bars gives every "
            f"within-year percentage (segments of 6% or more are also labelled in the bar), and n above each bar gives the annual count. Confabulation is reported as fabrication and misclassification as "
            f"factual error. (b) Annual generative-model share (generative or both) and fabrication share (confabulation or both) "
            f"among all {na} abstract-present critical records; points show annual estimates and whiskers 95% percentile bootstrap "
            f"CIs (1000 joint resamples, seed 42). Critical stance was Alarm or Caution. Record-level logistic regression on "
            f"publication year (unadjusted; journal cluster-robust SEs): generative-model share {g(F, 'RES-TMP-GENSHARE-OR')['value']}; fabrication share "
            f"{g(F, 'RES-TMP-FAB-ALL-OR')['value']}; fabrication-involved share among hallucination-gated records "
            f"{g(F, 'RES-TMP-FAB-GATED-OR')['value']}. Failure-mode agreement with human coding was moderate (Cohen κ "
            f"{g(F, 'VAL-MX-FM-K')['value']}) and the classifier assigned fabrication more often than the human coder "
            f"({g(F, 'VAL-MX-FABDIR')['value'].split(' (')[0]} disagreements), so fabrication shares are an upper bound.")


# ---------------------------------------------------------------------------
# Figure 4 · specialty
# ---------------------------------------------------------------------------
SHORT = {"Radiology / Diagnostic Imaging": "Radiology", "Pathology / Laboratory Medicine": "Pathology",
         "Mental Health / Psychiatry": "Mental health", "Internal Medicine / Primary Care": "Internal medicine",
         "Emergency Medicine / Critical Care": "Emergency medicine", "Obstetrics / Gynecology": "Obstetrics/gynecology",
         "Medical Informatics / Digital Health": "Medical informatics", "Multidisciplinary / Other": "Multidisciplinary",
         "Neurology / Neuroscience": "Neurology", "Medical Education": "Medical education"}


def fig4():
    F = "Fig4"
    specs = []
    from analysis.run_specialty_aiadoption import ALL_SPECIALTIES
    for sp in ALL_SPECIALTIES:
        o = g(F, f"RES-SPC-OBS-{slug(sp)}"); a = g(F, f"RES-SPC-AMP-{slug(sp)}"); d = g(F, f"RES-SPC-FDA-{slug(sp)}")
        specs.append((sp, o, a, d))
    specs.sort(key=lambda t: t[1]["point"])
    fig = plt.figure(figsize=(W_IN, 9.8))
    a = fig.add_axes([0.2, 0.42, 0.47, 0.54])
    tx = fig.add_axes([0.68, 0.42, 0.31, 0.54]); tx.axis("off")
    for i, (sp, o, am, _) in enumerate(specs):
        a.errorbar(o["point"], i + 0.17, xerr=[[o["point"] - o["lo"]], [o["hi"] - o["point"]]], fmt="o", color="black",
                   ms=3.2, elinewidth=0.7, capsize=1.6)
        a.errorbar(am["point"], i - 0.17, xerr=[[am["point"] - am["lo"]], [am["hi"] - am["point"]]], fmt="D", mfc="white",
                   mec="#555555", color="#777777", ms=3.0, elinewidth=0.7, capsize=1.6)
        tx.text(0.0, i + 0.2, f"{o['point']:.1f} ({o['lo']:.1f}-{o['hi']:.1f}); {fn(o['k'])}/{fn(o['n'])}", va="center", fontsize=7,
                transform=tx.transData)
        tx.text(0.0, i - 0.2, f"{am['point']:.1f} ({am['lo']:.1f}-{am['hi']:.1f})", va="center", fontsize=7, color="#555555",
                transform=tx.transData)
    tx.set_ylim(-0.6, len(specs) - 0.4); tx.set_xlim(0, 1)
    tx.text(0.0, len(specs) - 0.45, "Observed % (95% CI); k/n\nAdjusted % (95% CI)", fontsize=7, va="bottom", fontweight="bold",
            clip_on=False)
    a.set_yticks(range(len(specs))); a.set_yticklabels([SHORT.get(s[0], s[0]) for s in specs])
    a.set_ylim(-0.6, len(specs) - 0.4); a.set_xlim(0, 60)
    a.set_xlabel("Critical stance, % of records")
    a.grid(axis="x", lw=0.3, color="#DDDDDD")
    a.plot([], [], "o", color="black", ms=3.2, label="Observed")
    a.plot([], [], "D", mfc="white", mec="#555555", ms=3.0, label="Adjusted (average marginal probability)")
    a.legend(loc="lower right", frameon=True, framealpha=1, edgecolor="#CCCCCC")
    panel_letter(a, "a", -0.32, 1.0)

    b = fig.add_axes([0.1, 0.055, 0.86, 0.3])
    pts = []
    for sp, o, _, d in specs:
        x = d["point"] if d["point"] > 0 else 0.5
        zero = d["point"] == 0
        b.scatter(x, o["point"], s=22, facecolor="white" if zero else "black", edgecolor="black", lw=0.8, zorder=3)
        pts.append((x, o["point"], f"{SHORT.get(sp, sp)} {o['point']:.1f}" + (" (0 devices)" if zero else f" ({int(d['point'])})"), zero))
    # label positions (x factor, absolute y, ha) chosen for legibility; a leader line joins moved labels
    POS = {"Multidisciplinary": (1.18, 32.1, "left"), "Surgery": (1 / 1.2, 29.9, "right"),
           "Emergency medicine": (1.18, 27.9, "left"), "Dentistry": (1.18, 26.4, "left"),
           "Obstetrics/gynecology": (1.18, 23.4, "left"), "Internal medicine": (1 / 1.25, 20.9, "right"),
           "Neurology": (1.18, 25.6, "left"), "Pathology": (1.18, 19.6, "left"),
           "Ophthalmology": (1.18, 17.3, "left"), "Cardiology": (1.18, 15.4, "left"), "Radiology": (1 / 1.2, 22.6, "right")}
    for x, y, lab, zero in pts:
        key = lab.rsplit(" ", 2)[0]
        fx, ly, ha = POS.get(key, (1.18, y, "left"))
        b.annotate(lab, xy=(x, y), xytext=(x * fx, ly), fontsize=7, va="center", ha=ha,
                   arrowprops=dict(arrowstyle="-", lw=0.4, color="#888888", shrinkA=0, shrinkB=3) if abs(ly - y) > 0.6 else None)
    b.set_xscale("log"); b.set_xlim(0.35, 5000); b.set_ylim(10, 62)
    b.set_xticks([0.5, 1, 10, 100, 1000]); b.set_xticklabels(["0 (structural\nzero)", "1", "10", "100", "1000"])
    b.set_xlabel("FDA-cleared AI/ML devices in mapped review panels, 1995-2025 (log scale)")
    b.set_ylabel("Critical stance, %")
    b.scatter([], [], s=22, facecolor="black", edgecolor="black", label="Mapped FDA panel")
    b.scatter([], [], s=22, facecolor="white", edgecolor="black", label="Structural zero (no mapped panel), plotted at 0.5")
    b.legend(loc="upper right", frameon=True, framealpha=1, edgecolor="#CCCCCC")
    b.grid(lw=0.3, color="#EEEEEE")
    panel_letter(b, "b", -0.06, 1.0)
    save(fig, F)
    r18, r11 = g(F, "RES-SPC-FDA-RHO18"), g(F, "RES-SPC-FDA-RHO11")
    caption(F, "Figure 4. Critical stance by specialty or domain category and FDA cleared-device count, 2021-2025.",
            f"(a) Observed critical rate (filled circles) and adjusted average marginal probability of critical stance (open "
            f"diamonds) for the 18 categories among {fn(g(F, 'COR-SUB-08')['point'])} records with a valid specialty label, sorted by "
            f"the observed rate. Observed CIs are 95% percentile bootstrap intervals (1000 joint resamples, seed 42); adjusted "
            f"values come from the multivariable logistic model in Table 2 (year, genre, publication type, specialty and region; "
            f"journal-clustered SEs; delta-method 95% CI on the logit scale). (b) Observed critical rate against the number of "
            f"FDA-cleared AI/ML-enabled devices in the review panels mapped to each category (log scale). The 7 structural-zero "
            f"categories (no mapped FDA panel; not an absence of clinical AI) are drawn as hollow markers at 0.5. No fitted line "
            f"is shown. Labels give the critical rate (%) and device count. Spearman correlation, all 18 categories: "
            f"{r18['value']}; 11 categories with a mapped panel: {r11['value']}. This is an exploratory ecological association "
            f"across 18 category-level units. Critical stance was Alarm or Caution.")


# ---------------------------------------------------------------------------
# Figure 5 · country map
# ---------------------------------------------------------------------------
def fig5():
    F = "Fig5"
    import geopandas as gpd  # noqa: F401
    from matplotlib.colors import TwoSlopeNorm
    from matplotlib.lines import Line2D
    from analysis.run_country_critical_map import centroid_lookup, load_world_robinson
    world = load_world_robinson(); cen = centroid_lookup(world)
    rows = [(k[len("RES-GEO-CTY-"):], BOOK[k]) for k in BOOK if k.startswith("RES-GEO-CTY-")]
    sel = []
    for _, r in rows:
        name = r["item"].split(":")[0]
        if "(n >=50)" in r["item"]:
            USED.append((F, r["id"]))
            sel.append((name, float(r["point"]), int(float(r["n"]))))
    assert len(sel) == int(float(BOOK["RES-GEO-NCTY50"]["point"]))
    USED.append((F, "RES-GEO-NCTY50"))
    norm = TwoSlopeNorm(vmin=10, vcenter=float(BOOK["RES-OVR-CRITICAL"]["point"]), vmax=55)
    USED.append((F, "RES-OVR-CRITICAL"))
    cmap = plt.get_cmap("RdYlBu_r")
    SCALE = 0.32
    # label placement (direction from the bubble): "b" below (default), "a" above, "l" left, "r" right,
    # optionally combined (e.g. "al" = above-left)
    MAIN_POS = {"Japan": "r", "South Korea": "a", "Taiwan": "r", "Hong Kong": "bl", "Saudi Arabia": "bl",
                "United Arab Emirates": "r", "Iran": "a", "Israel": "l", "Turkey": "a", "Canada": "a", "Singapore": "r", "Brazil": "l"}
    INSET_POS = {"Netherlands": "a", "Belgium": "b", "Germany": "r", "United Kingdom": "b", "Ireland": "l",
                 "Denmark": "a", "Sweden": "r", "Poland": "r", "Austria": "r", "Switzerland": "bl", "France": "l",
                 "Italy": "r", "Romania": "r", "Greece": "b", "Spain": "b", "Portugal": "l"}

    def label(axx, x, y, n, txt, pos):
        r = np.sqrt(SCALE * n) / 2 + 1.5
        dx = (-r if "l" in pos else r if "r" in pos else 0)
        dy = (r if "a" in pos else -r if "b" in pos else 0)
        if pos in ("l", "r"):
            dy = 0
        ha = "right" if "l" in pos else "left" if "r" in pos else "center"
        va = "bottom" if "a" in pos else "top" if "b" in pos else "center"
        axx.annotate(txt, xy=(x, y), xytext=(dx, dy), textcoords="offset points", ha=ha, va=va, fontsize=7, zorder=6)

    fig = plt.figure(figsize=(W_IN, 4.6))
    ax = fig.add_axes([0.0, 0.0, 0.9, 1.0])
    world.plot(ax=ax, color="#E6E6E6", edgecolor="white", linewidth=0.3, zorder=1)
    EU = (-1.05e6, 2.45e6, 3.85e6, 6.95e6)   # Robinson x0, x1, y0, y1 (western, central and northern Europe)
    in_eu = lambda x, y: EU[0] <= x <= EU[1] and EU[2] <= y <= EU[3]
    for name, p, n in sel:
        x, y = cen[name]
        ax.scatter(x, y, s=SCALE * n, c=[p], cmap=cmap, norm=norm, edgecolor="#333333", lw=0.4, zorder=3)
        if not in_eu(x, y):
            label(ax, x, y, n, f"{p:.1f}", MAIN_POS.get(name, "b"))
    ax.set_axis_off()
    ax.set_xlim(world.total_bounds[0], world.total_bounds[2])
    ax.set_ylim(-6.3e6, 8.6e6)
    ax.add_patch(Rectangle((EU[0], EU[2]), EU[1] - EU[0], EU[3] - EU[2], fill=False, lw=0.6, ec="#555555", zorder=4))
    ins = fig.add_axes([0.335, 0.02, 0.29, 0.5])
    world.plot(ax=ins, color="#E6E6E6", edgecolor="white", linewidth=0.3)
    for name, p, n in sel:
        x, y = cen[name]
        if in_eu(x, y):
            ins.scatter(x, y, s=SCALE * n, c=[p], cmap=cmap, norm=norm, edgecolor="#333333", lw=0.4, zorder=3)
            label(ins, x, y, n, f"{p:.1f}", INSET_POS.get(name, "b"))
    ins.set_xlim(EU[0], EU[1]); ins.set_ylim(EU[2], EU[3]); ins.set_xticks([]); ins.set_yticks([])
    ins.set_facecolor("white")
    for s_ in ins.spines.values():
        s_.set_visible(True); s_.set_linewidth(0.6); s_.set_color("#555555")
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    cax = fig.add_axes([0.915, 0.22, 0.018, 0.6])
    cb = fig.colorbar(sm, cax=cax, extend="both"); cb.set_label("Critical stance, % of records")
    hs = [Line2D([0], [0], marker="o", color="none", markerfacecolor="#BBBBBB", markeredgecolor="#333333",
                 markersize=np.sqrt(SCALE * n), label=fn(n)) for n in (50, 500, 2000)]
    ax.legend(handles=hs, title="Records", loc="lower left", frameon=False, labelspacing=1.8, borderpad=0.8,
              handletextpad=1.6, bbox_to_anchor=(0.0, 0.04))
    save(fig, F)
    n_res = g(F, "COR-SUB-10")["point"]
    caption(F, "Figure 5. Critical stance by country of first authorship, 2021-2025.",
            f"The map shows the {len(sel)} countries with at least 50 first-author records among {fn(n_res)} records whose "
            f"first-author affiliation resolved to a country. Bubble area is proportional to the number of records; fill colour "
            f"shows the critical rate (centred on the corpus rate of {float(BOOK['RES-OVR-CRITICAL']['point']):.1f}%), and the "
            f"printed value is the critical rate (%). The boxed area of Europe is enlarged in the inset, where its values are "
            f"printed. Country was assigned from the first-author affiliation and indexes publication discourse, not national "
            f"attitudes, research quality or AI capability. Counts, 95% percentile bootstrap CIs (1000 resamples within country, "
            f"seed 42) and the 20-record map are in Multimedia Appendices 2 and 3. Critical stance was Alarm or Caution. Robinson "
            f"projection.")


# ---------------------------------------------------------------------------
# Figure 6 · publication format
# ---------------------------------------------------------------------------
def fig6():
    F = "Fig6"
    types = ["Review", "Research Article", "Editorial", "Letter", "Commentary"]
    outs = [("CRITICAL", "Critical (Alarm or Caution)", STANCE_COLOURS["Critical"]),
            ("NEUTRAL", "Neutral", STANCE_COLOURS["Neutral"]),
            ("FAVOURABLE", "Favourable (Cautious Optimism or Advocacy)", STANCE_COLOURS["Favourable"])]
    fig, ax = plt.subplots(figsize=(W_IN, 3.4))
    w = 0.26
    for j, (code, lab, col) in enumerate(outs):
        for i, t in enumerate(types):
            r = g(F, f"RES-FMT-{slug(t)}-{code}")
            x = i + (j - 1) * (w + 0.02)
            ax.bar(x, r["point"], width=w, color=col, label=lab if i == 0 else None, edgecolor="none")
            ax.errorbar(x, r["point"], yerr=[[r["point"] - r["lo"]], [r["hi"] - r["point"]]], fmt="none", ecolor="#222222",
                        elinewidth=0.6, capsize=1.6)
            ax.text(x, r["hi"] + 1.2, f"{r['point']:.1f}", ha="center", va="bottom", fontsize=7)
    labels = [f"{t}\n(n={fn(g(F, f'RES-FMT-{slug(t)}-CRITICAL')['n'])})" for t in types]
    ax.set_xticks(range(5)); ax.set_xticklabels(labels); ax.set_ylim(0, 92)
    ax.set_ylabel("% of records of that publication type")
    ax.legend(loc="upper right", frameon=False, ncol=1)
    ax.grid(axis="y", lw=0.3, color="#DDDDDD"); ax.set_axisbelow(True)
    fig.subplots_adjust(left=0.08, right=0.99, top=0.97, bottom=0.17)
    save(fig, F)
    chi = g(F, "RES-FMT-CHISQ")["value"]
    caption(F, "Figure 6. Stance by publication type, 2021-2025.",
            f"Share of records classified as critical, neutral or favourable within each publication type among {fn(14058)} "
            f"records; printed values are the point estimates (%) and n is the number of records of each type. Whiskers show "
            f"95% percentile bootstrap CIs (1000 resamples within type, seed 42). Critical stance was Alarm or Caution; favourable "
            f"stance was Cautious Optimism or Advocacy. Opinion formats (Commentary, Letter and Editorial pooled) compared with "
            f"Research Articles on the five-category stance distribution: {chi}. Adjusted odds ratios are in Table 2, and the "
            f"full five-category distribution, review subtypes and themes by format are in Multimedia Appendix 3.")


def main():
    fig2(); fig3()
    with open(FIGS / "figure_ids_used_v2.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["figure", "id"]); w.writerows(sorted(set(USED)))
    print("figures done;", len(set(USED)), "book IDs used")


if __name__ == "__main__":
    main()
