"""T4 draft figures, 2021–2025 only (rule 11): Figure 1 (a, b), Figure 2 (a, b),
Figures S2, S3, S4, S7b. Reads the T4 csv outputs; writes
revision_r1/figures/*_r1_draft.{png,pdf} and outputs/T4_figure_captions.md.

JMIR compliance (rule 13): no simple one-variable bar graphs (Figure 1a uses
point estimates with CI whiskers instead of bars), exact values printed on
every panel, no significance asterisks (exact P values go in the captions).
Nothing from 2026 is drawn.
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from r1_common import FIG, OUT, STANCES, THEMES, THEME_LABELS, fmt_p

Y = [2021, 2022, 2023, 2024, 2025]
W = "2021–2025"
ANN = pd.read_csv(OUT / "T4_annual_all_domains.csv")
ANN = ANN[ANN.window == W]
TR = pd.read_csv(OUT / "T4_trend_tests.csv")
TR = TR[TR.window == W]
assert ANN.year.max() == 2025

STANCE_COL = {"Alarm": "#C0504D", "Caution": "#E58B44", "Neutral": "#9AA5A4",
              "Cautious Optimism": "#4285B9", "Advocacy": "#4BAF6F"}
THEME_COL = {"Patient safety": "#1F6FB2", "Hallucination / errors": "#F57F20",
             "Governance / regulation": "#1A9C7F", "Ethics & bias": "#D62A2A"}
MINOR_COL = {"Medical education": "#9467BD", "Data privacy": "#8C564B", "Cognitive offloading": "#E377C2",
             "Existential threat": "#7F7F7F", "Replacement fears": "#BCBD22", "Other": "#17BECF"}
FM_COL = {"Confabulation (fabrication only)": "#D62728", "Both": "#8C5DB3",
          "Misclassification (factual error)": "#2369A8", "None or unclear": "#B5B53A"}
captions = []


def series(domain, outcome):
    d = ANN[(ANN.domain == domain) & (ANN.outcome == outcome)].sort_values("year")
    return d


def trend(domain, outcome):
    return TR[(TR.domain == domain) & (TR.outcome == outcome)].iloc[0]


def tstr(domain, outcome, label=None):
    x = trend(domain, outcome)
    pe = fmt_p(x.P_exact_perm)
    s = f"{label or outcome}: ρ={x.rho:+.2f}, exact P{pe if pe.startswith('<') else '=' + pe}"
    if not pd.isna(x.OR_per_year):
        pw = fmt_p(x.P_wald)
        s += f"; OR per year {x.OR_per_year:.2f} (95% CI {x.OR_lo:.2f}–{x.OR_hi:.2f}), P{pw if pw.startswith('<') else '=' + pw}"
    return s


def save(fig, name):
    for ext in ("png", "pdf"):
        fig.savefig(FIG / f"{name}_r1_draft.{ext}", dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def label_points(ax, xs, ys, fmt="{:.1f}", dy=0.0, color="#333", size=7, va="bottom", ha="center"):
    for x, y in zip(xs, ys):
        ax.annotate(fmt.format(y), (x, y), xytext=(0, 4 if va == "bottom" else -4) if dy == 0 else (0, dy),
                    textcoords="offset points", ha=ha, va=va, fontsize=size, color=color)


# ---------------------------------------------------------------- Figure 1
def figure1():
    fig = plt.figure(figsize=(20, 11.5))
    gs = fig.add_gridspec(2, 5, height_ratios=[1, 1.55], hspace=0.32, wspace=0.28)
    for i, s in enumerate(STANCES):
        ax = fig.add_subplot(gs[0, i])
        d = series("Stance", s)
        x = np.arange(len(Y))
        ax.errorbar(x, d.pct, yerr=[d.pct - d.lo, d.hi - d.pct], fmt="o-", color=STANCE_COL[s],
                    ecolor="#333", elinewidth=1, capsize=3, ms=6, lw=1.5)
        for xi, (p, hi) in enumerate(zip(d.pct, d.hi)):
            ax.annotate(f"{p:.1f}", (xi, hi), xytext=(0, 3), textcoords="offset points",
                        ha="center", va="bottom", fontsize=8)
        x_ = trend("Stance", s)
        ax.set_title(f"{s}  (ρ={x_.rho:+.2f})", fontsize=11, fontweight="bold")
        ax.set_xticks(x); ax.set_xticklabels([str(y) for y in Y], rotation=45, fontsize=9)
        ax.set_ylim(0, (d.hi.max()) * 1.18)
        ax.set_xlim(-0.5, len(Y) - 0.5)
        if i == 0:
            ax.set_ylabel("% of records", fontsize=10)
    fig.text(0.09, 0.9, "a)", fontsize=22, fontweight="bold")

    ax = fig.add_subplot(gs[1, 1:4])
    major = ["Patient safety", "Hallucination / errors", "Governance / regulation", "Ethics & bias"]
    offsets = {"Patient safety": 16, "Hallucination / errors": -22, "Governance / regulation": 18, "Ethics & bias": -22}
    for lab in major:
        d = series("Theme (among critical)", lab)
        mean = d.pct.mean()
        ax.plot(d.year, d.pct, "o-", color=THEME_COL[lab], lw=2.2, ms=7, label=f"{lab} ({mean:.0f}%)")
        ax.fill_between(d.year, d.lo, d.hi, color=THEME_COL[lab], alpha=0.15)
        for yv, p in zip(d.year, d.pct):
            ax.annotate(f"{p:.1f}", (yv, p), xytext=(8, offsets[lab] / 2), textcoords="offset points",
                        fontsize=8, color=THEME_COL[lab], ha="left", va="center")
    minors = [THEME_LABELS[t] for t in THEMES if THEME_LABELS[t] not in major]
    M = np.array([series("Theme (among critical)", m).pct.to_numpy() for m in minors])
    ax.fill_between(Y, M.min(0), M.max(0), color="#999", alpha=0.35,
                    label=f"Other themes (n=6; range of annual prevalences)")
    ax.plot(Y, M.mean(0), "--", color="#444", lw=1.4, label=f"Other themes, mean ({M.mean():.0f}%)")
    for yv, mv, lo, hi in zip(Y, M.mean(0), M.min(0), M.max(0)):
        ax.annotate(f"{mv:.1f} [{lo:.1f}–{hi:.1f}]", (yv, hi), xytext=(0, 4), textcoords="offset points",
                    fontsize=7, color="#444", ha="center")
    ax.set_xticks(Y); ax.set_xticklabels([str(y) for y in Y], fontsize=12)
    ax.set_xlim(2020.7, 2025.5)
    ax.set_ylim(0, 78)
    ax.set_xlabel("Publication year", fontsize=13); ax.set_ylabel("% of Alarm+Caution papers", fontsize=13)
    ax.grid(axis="y", ls="--", alpha=0.3)
    ax.legend(loc="center left", bbox_to_anchor=(1.02, 0.5), fontsize=11, frameon=True)
    fig.text(0.09, 0.56, "b)", fontsize=22, fontweight="bold")
    save(fig, "fig1_stance_themes")

    n5 = int(trend("Stance", "Alarm").n_records)
    ncrit = int(trend("Theme (among critical)", "Patient safety").n_records)
    lines = [tstr("Stance", s) for s in STANCES] + [tstr("Stance", "Critical (Alarm+Caution)", "Critical"),
                                                    tstr("Stance", "Favourable (CO+Advocacy)", "Favourable")]
    tl = [tstr("Theme (among critical)", lab) for lab in major]
    captions.append(
        "**Figure 1 (draft).** Temporal distribution of AI stance and concern themes in high-quartile medical "
        f"journals, 2021–2025. a) Annual share of Alarm, Caution, Neutral, Cautious Optimism, and Advocacy among "
        f"{n5:,} records published 2021–2025. Points show annual estimates (value printed above each point) and "
        "whiskers show 95% percentile bootstrap CIs (1000 resamples, seed 42). Critical stance was Alarm or "
        "Caution; favourable stance was Cautious Optimism or Advocacy. ρ is the Spearman correlation of the five "
        "annual shares with publication year; P values are exact two-sided permutation P values (smallest "
        "attainable with five points: .017); ORs are from record-level logistic regression on year (centred). "
        + "; ".join(lines) + ". b) Annual prevalence of the four leading themes among critical records "
        f"(n={ncrit:,}). Themes were multilabel (one to three per paper), so prevalences do not sum to 100%. "
        "Lines show annual estimates; shaded bands show 95% percentile bootstrap CIs. The six lower-prevalence "
        "themes are summarised as their annual mean (dashed line, value printed with the range across the six) "
        "and range (grey band). Legend percentages are means of the five annual prevalences. "
        + "; ".join(tl) + ".")


# ---------------------------------------------------------------- Figure 2
def figure2():
    fig = plt.figure(figsize=(20, 7))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.15, 1], wspace=0.18)
    ax = fig.add_subplot(gs[0, 0])
    order = ["Confabulation (fabrication only)", "Both", "Misclassification (factual error)", "None or unclear"]
    dom = "Mechanism, hallucination-gated (failure-mode composition)"
    data = {o: series(dom, o) for o in order}
    N = data[order[0]].N.to_numpy()
    x = np.arange(len(Y))

    def stacked(axx, idx, label_min_h):
        bottom = np.zeros(len(idx))
        for o in order:
            d = data[o].iloc[idx]
            h = d.k.to_numpy()
            axx.bar(x[idx] if axx is ax else np.arange(len(idx)), h, bottom=bottom, color=FM_COL[o],
                    width=0.7, edgecolor="white", lw=0.5, label=o if axx is ax else None)
            for j, (hh, b, p) in enumerate(zip(h, bottom, d.pct)):
                xx = (x[idx] if axx is ax else np.arange(len(idx)))[j]
                if hh >= label_min_h and hh >= 0.06 * (N[idx].max() if axx is not ax else 1):
                    axx.text(xx, b + hh / 2, f"{p:.1f}%", ha="center", va="center", fontsize=8,
                             color="white" if o != "None or unclear" else "black", fontweight="bold")
                elif hh > 0 and axx is not ax:
                    axx.annotate(f"{p:.1f}% ({o.split(' ')[0].lower()})", (xx + 0.36, b + hh / 2),
                                 xytext=(4, 0), textcoords="offset points", fontsize=6.5, va="center",
                                 color=FM_COL[o], fontweight="bold")
            bottom = bottom + h
        for j, tot in enumerate(bottom):
            xx = (x[idx] if axx is ax else np.arange(len(idx)))[j]
            axx.text(xx, tot, f"n={int(tot)}", ha="center", va="bottom", fontsize=9, fontweight="bold")

    stacked(ax, np.arange(len(Y)), label_min_h=N.max() * 0.035)
    ax.set_xticks(x); ax.set_xticklabels([str(y) for y in Y], fontsize=11)
    ax.set_ylabel("# hallucination-gated papers", fontsize=12)
    ax.set_ylim(0, N.max() * 1.12)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.08), ncol=4, frameon=False, fontsize=10)
    ins = ax.inset_axes([0.05, 0.42, 0.45, 0.52])
    stacked(ins, np.arange(3), label_min_h=0.5)
    ins.set_xticks(range(3)); ins.set_xticklabels([str(y) for y in Y[:3]], fontsize=8)
    ins.set_title("Inset: 2021–2023 enlarged", fontsize=9, fontweight="bold")
    ins.set_ylim(0, N[:3].max() * 1.15); ins.tick_params(labelsize=7)
    fig.text(0.08, 0.93, "a)", fontsize=22, fontweight="bold")

    ax = fig.add_subplot(gs[0, 1])
    g = series("Mechanism, all abstract-present critical", "Generative-model share (generative or both)")
    f = series("Mechanism, all abstract-present critical", "Fabrication share (confabulation or both)")
    ax.plot(Y, g.pct, "o-", color="#1F6FB2", lw=2, label="Generative-model exposure")
    ax.plot(Y, f.pct, "s-", color="#C0392B", lw=2, label="Confabulation (fabrication) rate")
    for yv, p in zip(Y, g.pct):
        ax.annotate(f"{p:.1f}%", (yv, p), xytext=(0, 7), textcoords="offset points", ha="center",
                    fontsize=9, color="#1F6FB2", fontweight="bold")
    for yv, p in zip(Y, f.pct):
        ax.annotate(f"{p:.1f}%", (yv, p), xytext=(0, -13), textcoords="offset points", ha="center",
                    fontsize=9, color="#C0392B", fontweight="bold")
    ax.set_xticks(Y); ax.set_xticklabels([str(y) for y in Y], fontsize=11)
    ax.set_ylim(-3, 75); ax.set_ylabel("% of Alarm+Caution papers", fontsize=12)
    ax.grid(axis="y", ls="--", alpha=0.3); ax.spines[["top", "right"]].set_visible(False)
    ax.legend(loc="upper left", fontsize=10)
    fig.text(0.53, 0.93, "b)", fontsize=22, fontweight="bold")
    save(fig, "fig2_mechanism")

    ngate = int(N.sum())
    nall = int(g.N.sum())
    captions.append(
        "**Figure 2 (draft).** Failure-mode and model-type composition of critical records, 2021–2025. "
        f"a) Annual failure-mode composition among hallucination-gated, abstract-present critical records "
        f"(n={ngate:,}). Critical stance was Alarm or Caution. Bar height shows the yearly record count (printed "
        "above each bar); segments show within-year proportions (printed in each segment) classified as "
        "confabulation, misclassification, both, or none/unclear. Confabulation is reported as fabrication and "
        "misclassification as factual error. The inset enlarges 2021–2023, whose counts remain small relative to "
        "2024–2025. Each bar sums to 100%. "
        + "; ".join(tstr(dom, o) for o in order) + "; "
        + tstr("Mechanism, hallucination-gated", "Fabrication-involved (confabulation or both)") + ". "
        f"b) Annual generative-model exposure and confabulation rate in the full abstract-present critical corpus "
        f"(n={nall:,}). Generative-model exposure is the proportion classified as generative or both; "
        "confabulation rate is the proportion classified as confabulation or both. Exact values are printed at "
        "each point. "
        + tstr("Mechanism, all abstract-present critical", "Generative-model share (generative or both)",
               "Generative-model exposure") + "; "
        + tstr("Mechanism, all abstract-present critical", "Fabrication share (confabulation or both)",
               "Confabulation rate") + ".")


# ---------------------------------------------------------------- Figure S2
def figure_s2():
    fig, ax = plt.subplots(figsize=(10, 6.5))
    cols = {"discourse": "#8E44AD", "evaluative": "#16A085"}
    for gname, off in [("discourse", 8), ("evaluative", -14)]:
        d = series(f"Within genre: {gname}", "Critical (Alarm+Caution)")
        ax.plot(d.year, d.pct, "o-", color=cols[gname], lw=2, label=gname)
        ax.fill_between(d.year, d.lo, d.hi, color=cols[gname], alpha=0.18)
        for yv, p, lo, hi in zip(d.year, d.pct, d.lo, d.hi):
            ax.annotate(f"{p:.1f} ({lo:.1f}–{hi:.1f})", (yv, p), xytext=(0, off), textcoords="offset points",
                        ha="center", fontsize=8, color=cols[gname])
    ax.set_xticks(Y); ax.set_xticklabels([str(y) for y in Y])
    ax.set_xlabel("Publication year"); ax.set_ylabel("Critical share (Alarm + Caution), %")
    ax.grid(ls=":", alpha=0.5); ax.legend(title="Prefilter genre", loc="lower right")
    save(fig, "figS2_within_genre")
    captions.append(
        "**Figure S2 (draft).** Annual critical share within each prefilter genre, 2021–2025. Critical share, "
        "defined as Alarm or Caution, computed separately within discourse and evaluative records, with 95% "
        "percentile bootstrap confidence bands (1000 resamples, seed 42); point estimates and CIs are printed at "
        "each point. "
        + tstr("Within genre: discourse", "Critical (Alarm+Caution)", "Discourse") + "; "
        + tstr("Within genre: evaluative", "Critical (Alarm+Caution)", "Evaluative") + ".")


# ---------------------------------------------------------------- Figure S3
def figure_s3():
    fig, ax = plt.subplots(figsize=(11, 6.5))
    minors = list(MINOR_COL)
    for lab in minors:
        d = series("Theme (among critical)", lab)
        ax.plot(d.year, d.pct, "o-", color=MINOR_COL[lab], lw=2, label=f"{lab} ({d.pct.mean():.1f}%)")
        for yv, p in zip(d.year, d.pct):
            ax.annotate(f"{p:.1f}", (yv, p), xytext=(6, 0), textcoords="offset points", fontsize=7,
                        color=MINOR_COL[lab], va="center")
    ax.set_xticks(Y); ax.set_xticklabels([str(y) for y in Y]); ax.set_xlim(2020.7, 2025.4)
    ax.set_ylim(0, None); ax.grid(axis="y", ls="--", alpha=0.3)
    ax.set_xlabel("Publication year"); ax.set_ylabel("% of Alarm+Caution papers")
    ax.legend(loc="center left", bbox_to_anchor=(1.01, 0.5))
    save(fig, "figS3_minor_themes")
    captions.append(
        "**Figure S3 (draft).** Prevalence of the six lower-prevalence concern themes among critical abstracts, "
        "2021–2025. Themes were multilabel (one to three per record). The denominator in each year is the number "
        "of critical (Alarm or Caution) records published that year. Lines show annual point estimates (values "
        "printed beside each point); legend percentages are the mean of the five annual prevalences. "
        + "; ".join(tstr("Theme (among critical)", lab) for lab in minors) + ".")


# ---------------------------------------------------------------- Figure S4
def figure_s4():
    counts = pd.read_csv(OUT / "T4_theme_counts.csv")
    counts = counts[counts.year.isin(Y)]
    order = ["Replacement fears", "Medical education", "Other", "Hallucination / errors", "Patient safety",
             "Ethics & bias", "Governance / regulation", "Data privacy", "Cognitive offloading", "Existential threat"]
    fig, axes = plt.subplots(2, 5, figsize=(24, 9.5))
    for ax, lab in zip(axes.flat, order):
        c = counts[counts.theme == lab].sort_values("year")
        d = series("Theme (among critical)", lab)
        bars = ax.bar(c.year, c.n_papers, color="#8FBBDA", alpha=0.85)
        for b, v in zip(bars, c.n_papers):
            ax.text(b.get_x() + b.get_width() / 2, v, f"{v}", ha="center", va="bottom", fontsize=7, color="#1F6FB2")
        ax.set_ylabel("Paper count", color="#1F6FB2", fontsize=9)
        ax.tick_params(axis="y", colors="#1F6FB2", labelsize=8)
        ax2 = ax.twinx()
        ax2.plot(d.year, d.pct, "o-", color="#C0392B", lw=2, ms=4)
        for yv, p in zip(d.year, d.pct):
            ax2.annotate(f"{p:.1f}%", (yv, p), xytext=(0, 5), textcoords="offset points", ha="center",
                         fontsize=7, color="#C0392B",
                         bbox=dict(boxstyle="round,pad=0.1", fc="white", ec="none", alpha=0.8))
        lo, hi = d.pct.min(), d.pct.max()
        pad = (hi - lo) * 0.25 + 0.5
        ax2.set_ylim(lo - pad, hi + pad * 1.6)
        ax2.set_ylabel("Prevalence share (%)", color="#C0392B", fontsize=9)
        ax2.tick_params(axis="y", colors="#C0392B", labelsize=8)
        ax.set_ylim(0, c.n_papers.max() * 1.15)
        ax.set_xticks(Y); ax.set_xticklabels([str(y) for y in Y], fontsize=8)
        ax.set_title(lab, fontsize=11, fontweight="bold")
    fig.tight_layout()
    save(fig, "figS4_theme_count_vs_share")
    captions.append(
        "**Figure S4 (draft).** Annual paper count and prevalence share for all ten concern themes, 2021–2025. "
        "For each theme, bars show the annual number of critical (Alarm or Caution) records assigned that theme "
        "(left axis; count printed above each bar), and the line shows the annual prevalence share within the "
        "critical corpus (right axis; value printed at each point). The denominator is the number of critical "
        f"records published that year (2021–2025 total: {int(counts[counts.theme == order[0]].n_critical.sum()):,}). "
        "Themes were multilabel.")


# ---------------------------------------------------------------- Figure S7b
def figure_s7b():
    fig, ax = plt.subplots(figsize=(10, 6))
    a = series("Stance", "Critical (Alarm+Caution)")
    q = series("Q3 comparison arm", "Critical (Alarm+Caution)")
    ax.plot(a.year, a.pct, "o-", color="#1F77B4", lw=2, label="Q1/Q2")
    ax.fill_between(a.year, a.lo, a.hi, color="#1F77B4", alpha=0.2)
    ax.plot(q.year, q.pct, "s-", color="#E67E22", lw=2, label="Q3")
    ax.fill_between(q.year, q.lo, q.hi, color="#E67E22", alpha=0.15)
    for yv, p, pq, n in zip(a.year, a.pct, q.pct, q.N):
        up = pq > p  # put the higher series' label above, the lower one's below
        ax.annotate(f"{p:.1f}", (yv, p), xytext=(0, -14 if up else 8), textcoords="offset points",
                    ha="center", fontsize=8, color="#1F77B4")
        ax.annotate(f"{pq:.1f} (n={n})", (yv, pq), xytext=(0, 8 if up else -14), textcoords="offset points",
                    ha="center", fontsize=8, color="#E67E22")
    ax.set_xticks(Y); ax.set_xticklabels([str(y) for y in Y])
    ax.set_ylabel("% Critical (Alarm + Caution)"); ax.legend(loc="lower right")
    ax.grid(axis="y", ls=":", alpha=0.5)
    save(fig, "figS7b_q1q2_vs_q3_temporal")
    captions.append(
        "**Figure S7b (draft).** Annual critical share, defined as Alarm or Caution, by quality tier, 2021–2025, "
        "with 95% percentile bootstrap bands (1000 resamples, seed 42); Q1/Q2 values and Q3 values with annual n "
        f"are printed at each point. The Q3 2024 stratum contains {int(q[q.year == 2024].N.iloc[0])} records. "
        + tstr("Stance", "Critical (Alarm+Caution)", "Q1/Q2") + "; "
        + tstr("Q3 comparison arm", "Critical (Alarm+Caution)", "Q3") + ".")


if __name__ == "__main__":
    figure1(); figure2(); figure_s2(); figure_s3(); figure_s4(); figure_s7b()
    (OUT / "T4_figure_captions.md").write_text(
        "# T4 draft figure captions (2021–2025)\n\nExact P values replace significance asterisks. "
        "P values: exact two-sided permutation for Spearman ρ over 5 annual points; Wald P for the "
        "record-level logistic OR per year.\n\n" + "\n\n".join(captions) + "\n")
    print("\n\n".join(captions))
