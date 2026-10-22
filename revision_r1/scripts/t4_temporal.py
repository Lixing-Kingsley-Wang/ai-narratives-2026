"""T4 · Temporal re-analysis, primary window 2021–2025 (D3, X3).

Primary window: complete calendar years 2021–2025. January–April 2026 appears
only in T4_2026_descriptive.csv (no trend statistics). The two 2020 records
stay excluded. "Old" values recompute the submitted 2021–2026 analysis with
the same code so the endpoint table compares like with like.

Bootstrap: joint row-level resampling of the analysis set (1000 draws,
seed 42), per-year shares from each draw — the scheme of
analysis/robustness.py::bootstrap_ci used for Figure 1a / Table S1.

Outputs: revision_r1/outputs/T4_*.csv, T4_temporal_2021_2025.md
"""

from __future__ import annotations

import json
import re

import numpy as np
import pandas as pd

from r1_common import (DATA_ROOT, OUT, REPO_OUT, STANCES, THEMES, THEME_LABELS, boot_group_share,
                       fmt_p, load_v1, logit_trend, md_table, read_str, spearman_exact)

Y5 = [2021, 2022, 2023, 2024, 2025]
Y6 = [2021, 2022, 2023, 2024, 2025, 2026]
WINDOWS = {"2021–2025": Y5, "2021–2026 (submitted)": Y6}

trend_rows = []      # one row per (domain, outcome, window)
annual_rows = []     # one row per (domain, outcome, window, year)


def annual(domain, outcome, years_arr, success, window_years, window_name, n_boot_set=None):
    """Bootstrap per-year share for one binary outcome over a record set."""
    mask = np.isin(years_arr, window_years)
    yrs = np.asarray(years_arr)[mask]
    suc = np.asarray(success, dtype=float)[mask]
    tab = boot_group_share(yrs, suc, list(window_years))
    for _, r in tab.iterrows():
        annual_rows.append({"domain": domain, "outcome": outcome, "window": window_name,
                            "year": int(r["level"]), "k": int(r["k"]), "N": int(r["n"]),
                            "pct": r["point"], "lo": r["lo"], "hi": r["hi"]})
    rho, p_exact, p_asym = spearman_exact(window_years, tab["point"].to_numpy())
    lt = logit_trend(yrs, suc) if 0 < suc.sum() < len(suc) else {}
    trend_rows.append({"domain": domain, "outcome": outcome, "window": window_name,
                       "n_years": len(window_years), "first_year_pct": tab["point"].iloc[0],
                       "last_year_pct": tab["point"].iloc[-1],
                       "delta_pp": tab["point"].iloc[-1] - tab["point"].iloc[0],
                       "rho": rho, "P_exact_perm": p_exact, "P_scipy_asymptotic": p_asym,
                       "OR_per_year": lt.get("OR"), "OR_lo": lt.get("OR_lo"), "OR_hi": lt.get("OR_hi"),
                       "P_wald": lt.get("P_wald"), "P_LR": lt.get("P_LR"),
                       "year_centre": lt.get("centre"), "n_records": int(len(suc)),
                       "events": int(suc.sum())})
    return tab


def run_all(domain, outcome, years_arr, success, logit=True):
    out = {}
    for wname, wy in WINDOWS.items():
        out[wname] = annual(domain, outcome, years_arr, success, wy, wname)
    return out


def main():
    # ---------------- 1. stance --------------------------------------------
    v1 = load_v1(year_range=(2021, 2026))
    yrs = v1["pub_year"].astype(int).to_numpy()
    for s in STANCES:
        run_all("Stance", s, yrs, v1["stance"] == s)
    run_all("Stance", "Critical (Alarm+Caution)", yrs, v1["critical"])
    run_all("Stance", "Favourable (CO+Advocacy)", yrs, v1["favourable"])

    # ---------------- 2. within genre --------------------------------------
    ratio_rows = []
    for g in ["discourse", "evaluative"]:
        sub = v1[v1["paper_type"] == g]
        run_all(f"Within genre: {g}", "Critical (Alarm+Caution)", sub["pub_year"].astype(int).to_numpy(),
                sub["critical"])
    for y in Y6:
        nd = int(((v1.pub_year == y) & (v1.paper_type == "discourse")).sum())
        ne = int(((v1.pub_year == y) & (v1.paper_type == "evaluative")).sum())
        ratio_rows.append({"year": y, "n_discourse": nd, "n_evaluative": ne, "ratio": nd / ne})
    ratio = pd.DataFrame(ratio_rows)
    ratio.to_csv(OUT / "T4_genre_ratio.csv", index=False)
    r5 = spearman_exact(Y5, ratio[ratio.year <= 2025]["ratio"])

    # ---------------- 3. themes --------------------------------------------
    th = pd.read_csv(REPO_OUT / "analysis/thematic_alarm.csv", dtype={"pmid": str}, low_memory=False)
    th["pub_year"] = pd.to_numeric(th["pub_year"], errors="coerce")
    th = th[th["pub_year"].between(2021, 2026)].copy()
    th_years = th["pub_year"].astype(int).to_numpy()
    tl = th["themes"].fillna("").str.split("|")
    theme_counts = []
    for t in THEMES:
        has = tl.apply(lambda lst: t in lst).to_numpy()
        run_all("Theme (among critical)", THEME_LABELS[t], th_years, has)
        for y in Y6:
            theme_counts.append({"theme": THEME_LABELS[t], "year": y,
                                 "n_papers": int(has[th_years == y].sum()),
                                 "n_critical": int((th_years == y).sum())})
    pd.DataFrame(theme_counts).to_csv(OUT / "T4_theme_counts.csv", index=False)

    # ---------------- 4. mechanism -----------------------------------------
    ac = pd.read_csv(REPO_OUT / "analyses/q7_classified_ac.csv", dtype={"pmid": str})
    n_ac = len(ac)
    ac = ac[(ac["failure_mode"] != "FAILED") & (ac["model_type"] != "FAILED")].copy()
    n_parsed = len(ac)
    ab = load_v1(year_range=None)[["pmid", "has_abstract"]]
    ac = ac.merge(ab, on="pmid", how="left")
    ac = ac[ac["has_abstract"] == True].copy()  # noqa: E712
    gate = th.assign(g=th["themes"].fillna("").str.lower().str.contains("hallucination"))[["pmid", "g"]]
    ac = ac.merge(gate, on="pmid", how="left")
    ac["g"] = ac["g"].fillna(False).astype(bool)
    ac["pub_year"] = ac["pub_year"].astype(int)
    ac["fab"] = ac["failure_mode"].isin(["confabulation", "both"])
    ac["gen"] = ac["model_type"].isin(["generative", "both"])
    gated = ac[ac["g"]]
    for fm, lab in [("confabulation", "Confabulation (fabrication only)"),
                    ("misclassification", "Misclassification (factual error)"),
                    ("both", "Both"), ("none_or_unclear", "None or unclear")]:
        run_all("Mechanism, hallucination-gated (failure-mode composition)", lab,
                gated["pub_year"].to_numpy(), gated["failure_mode"] == fm)
    run_all("Mechanism, hallucination-gated", "Fabrication-involved (confabulation or both)",
            gated["pub_year"].to_numpy(), gated["fab"])
    run_all("Mechanism, all abstract-present critical", "Generative-model share (generative or both)",
            ac["pub_year"].to_numpy(), ac["gen"])
    run_all("Mechanism, all abstract-present critical", "Fabrication share (confabulation or both)",
            ac["pub_year"].to_numpy(), ac["fab"])
    gen = ac[ac["gen"]]
    run_all("Mechanism, generative-model papers", "Fabrication share among generative",
            gen["pub_year"].to_numpy(), gen["fab"])
    mech_facts = {}
    for wname, wy in WINDOWS.items():
        a = ac[ac.pub_year.isin(wy)]; g_ = a[a.g]
        mech_facts[wname] = {
            "n_abstract_present_critical": len(a), "n_gated": len(g_),
            "gen_without_fab": int((a.gen & ~a.fab).sum()),
            "gen_without_fab_pct": (a.gen & ~a.fab).mean() * 100,
            "fab_in_discriminative_only": int((a.fab & (a.model_type == "discriminative")).sum()),
            "gate_recall_fab": f"{int((a.fab & a.g).sum())}/{int(a.fab.sum())}",
            "gate_recall_fab_pct": (a.fab & a.g).sum() / a.fab.sum() * 100,
            "fab_among_gated": f"{int(g_.fab.sum())}/{len(g_)}",
            "fab_among_gated_pct": g_.fab.mean() * 100,
        }
    mech_facts["counts"] = {"q7_records": n_ac, "parsed": n_parsed}

    # ---------------- 5. keep rate -----------------------------------------
    de = read_str(DATA_ROOT / "prefiltered_discourse_eval.csv")
    ap = read_str(DATA_ROOT / "prefiltered_application.csv")
    elig = pd.concat([de[["pmid", "pub_date", "pub_year"]].assign(kept=True),
                      ap[["pmid", "pub_date", "pub_year"]].assign(kept=False)], ignore_index=True)
    # denominator year as in cv2_keep_rate.py (first 20xx in pub_date)
    elig["y"] = elig["pub_date"].str.extract(r"\b(20\d{2})\b")[0].astype(float)
    elig = elig[elig["y"].between(2021, 2026)]
    run_all("Prefilter keep rate", "Kept (discourse or evaluative)", elig["y"].astype(int).to_numpy(),
            elig["kept"].to_numpy())

    # ---------------- 6. Q3 --------------------------------------------------
    q3 = pd.read_csv(DATA_ROOT / "classified_medical_Q3.csv", low_memory=False, dtype={"pmid": str})
    q3["pub_year"] = pd.to_numeric(q3["pub_year"], errors="coerce")
    q3 = q3[(q3["stance"] != "FAILED") & q3["pub_year"].between(2021, 2026)].copy()
    run_all("Q3 comparison arm", "Critical (Alarm+Caution)", q3["pub_year"].astype(int).to_numpy(),
            q3["stance"].isin(["Alarm", "Caution"]))
    for s in STANCES:
        run_all("Q3 comparison arm", s, q3["pub_year"].astype(int).to_numpy(), q3["stance"] == s)

    ann = pd.DataFrame(annual_rows)
    tr = pd.DataFrame(trend_rows)
    ann.to_csv(OUT / "T4_annual_all_domains.csv", index=False)
    tr.to_csv(OUT / "T4_trend_tests.csv", index=False)
    (OUT / "T4_mechanism_facts.json").write_text(json.dumps(mech_facts, indent=2, default=float))

    # ---------------- 7. 2026 descriptive -----------------------------------
    d26 = ann[(ann.window == "2021–2026 (submitted)") & (ann.year == 2026)].copy()
    # within-2026 CIs from a 2026-only bootstrap (seed 42), not the joint draw
    d26 = d26.drop(columns=["window"])
    d26 = d26.rename(columns={"pct": "pct_2026", "lo": "lo_jointboot", "hi": "hi_jointboot"})
    # recompute CI using 2026 records only
    from r1_common import boot_indices
    def ci_2026(k, n):
        x = np.r_[np.ones(k), np.zeros(n - k)]
        draws = [x[i].mean() * 100 for i in boot_indices(n)]
        return np.percentile(draws, [2.5, 97.5])
    los, his = [], []
    for _, r in d26.iterrows():
        lo, hi = ci_2026(int(r["k"]), int(r["N"])) if r["N"] > 0 else (np.nan, np.nan)
        los.append(lo); his.append(hi)
    d26["lo"] = los; d26["hi"] = his
    d26 = d26.drop(columns=["lo_jointboot", "hi_jointboot", "year"])
    d26.to_csv(OUT / "T4_2026_descriptive.csv", index=False)

    write_md(ann, tr, ratio, r5, mech_facts, d26)


def g(ann, domain, outcome, window, year):
    r = ann[(ann.domain == domain) & (ann.outcome == outcome) & (ann.window == window) & (ann.year == year)]
    return r.iloc[0]


def t(tr, domain, outcome, window):
    return tr[(tr.domain == domain) & (tr.outcome == outcome) & (tr.window == window)].iloc[0]


def write_md(ann, tr, ratio, r5, mech, d26):
    W5, W6 = "2021–2025", "2021–2026 (submitted)"
    L = ["# T4 · Temporal re-analysis, primary window 2021–2025 (D3, X3)\n",
         "Script: `revision_r1/scripts/t4_temporal.py` (figures: `t4_figures.py`). All shares are "
         "percentages with n/N and 95% percentile bootstrap CIs (1000 joint row-level resamples of the "
         "analysis set, seed 42). Trend statistics: Spearman ρ of the annual shares on year with **exact** "
         "two-sided permutation P (all 5! = 120 orderings; with 5 points the smallest attainable two-sided "
         "P is 2/120 ≈ .017), and record-level unadjusted logistic regression of the outcome on publication "
         "year (continuous, centred on the record-level mean year of the window), OR per year with Wald "
         "95% CI and Wald P (likelihood-ratio P in the csv). No covariates.\n",
         f"Analysis set sizes (2021–2025) are the `records` column below; e.g. stance "
         f"{int(t(tr, 'Stance', 'Alarm', W5).n_records):,} of {int(t(tr, 'Stance', 'Alarm', W6).n_records):,} "
         f"records dated 2021–2026.\n"]

    def block(domain, outcomes, title, note=""):
        L.append(f"## {title}\n")
        if note:
            L.append(note + "\n")
        rows = []
        for o in outcomes:
            row = {"outcome": o}
            for y in Y5:
                r = g(ann, domain, o, W5, y)
                row[str(y)] = f"{r.pct:.1f} ({r.lo:.1f}–{r.hi:.1f}); {r.k}/{r.N}"
            rows.append(row)
        L.append(md_table(pd.DataFrame(rows)))
        L.append("")
        rows = []
        for o in outcomes:
            x = t(tr, domain, o, W5)
            rows.append({"outcome": o, "Δ 2021→2025 (pp)": f"{x.delta_pp:+.2f}",
                         "Spearman ρ": f"{x.rho:+.2f}", "exact P": fmt_p(x.P_exact_perm),
                         "OR per year (95% CI)": "" if pd.isna(x.OR_per_year) else
                         f"{x.OR_per_year:.3f} ({x.OR_lo:.3f}–{x.OR_hi:.3f})",
                         "P (Wald)": fmt_p(x.P_wald), "events/records": f"{x.events:,}/{x.n_records:,}"})
        L.append(md_table(pd.DataFrame(rows)))
        L.append("")

    block("Stance", STANCES + ["Critical (Alarm+Caution)", "Favourable (CO+Advocacy)"],
          "1–3. Annual stance distribution, 2021–2025")
    block("Within genre: discourse", ["Critical (Alarm+Caution)"], "4a. Within-genre critical share: discourse (Table S3, Figure S2)")
    block("Within genre: evaluative", ["Critical (Alarm+Caution)"], "4a. Within-genre critical share: evaluative")
    rr = ratio[ratio.year <= 2025]
    L.append("Discourse:evaluative ratio, 2021–2025: " + ", ".join(
        f"{int(r.year)} {r.ratio:.2f} ({r.n_discourse:,}/{r.n_evaluative:,})" for r in rr.itertuples()) +
        f". Spearman ρ = {r5[0]:+.2f}, exact P = {fmt_p(r5[1])}.\n")
    block("Theme (among critical)", [THEME_LABELS[x] for x in THEMES],
          "4b. Concern themes among critical records (Table S5, Figure 1b, Figures S3–S4)",
          "Denominator: critical records published that year. Multilabel.")
    block("Mechanism, hallucination-gated (failure-mode composition)",
          ["Confabulation (fabrication only)", "Misclassification (factual error)", "Both", "None or unclear"],
          "4c. Failure-mode composition, hallucination-gated abstract-present critical records (Figure 2a)")
    block("Mechanism, hallucination-gated", ["Fabrication-involved (confabulation or both)"],
          "4c. Fabrication-involved share within the gated subset")
    block("Mechanism, all abstract-present critical",
          ["Generative-model share (generative or both)", "Fabrication share (confabulation or both)"],
          "4c. Generative-model and fabrication share, all abstract-present critical records (Figure 2b)")
    block("Mechanism, generative-model papers", ["Fabrication share among generative"],
          "4c. Fabrication share among generative-model papers")
    m5 = mech[W5]
    L.append(f"Mechanism facts, 2021–2025: abstract-present critical records {m5['n_abstract_present_critical']:,}; "
             f"gated {m5['n_gated']:,}; generative without fabrication {m5['gen_without_fab']:,} "
             f"({m5['gen_without_fab_pct']:.1f}%); fabrication in discriminative-only papers "
             f"{m5['fab_in_discriminative_only']}; gate recall of fabrication {m5['gate_recall_fab']} "
             f"({m5['gate_recall_fab_pct']:.1f}%); fabrication among gated {m5['fab_among_gated']} "
             f"({m5['fab_among_gated_pct']:.1f}%).\n")
    block("Prefilter keep rate", ["Kept (discourse or evaluative)"], "4d. Prefilter keep rate (Table S4)",
          "Denominator: eligible Q1/Q2 records (pre-prefilter), year from `pub_date` as in cv2_keep_rate.py.")
    block("Q3 comparison arm", ["Critical (Alarm+Caution)"] + STANCES, "4e. Q3 comparison arm (Table S14, Figure S7)")

    # ---- endpoint comparison ------------------------------------------------
    L.append("## 5. Endpoint comparison: submitted (2021→2026) vs primary (2021→2025)\n")
    L.append("Full table with every domain/outcome: [T4_endpoint_comparison.csv](T4_endpoint_comparison.csv). "
             "'Old' values are recomputed here with the submitted window; the reproduction status against the "
             "manuscript text is in T5.\n")
    ep = []
    for (dom, out), grp in tr.groupby(["domain", "outcome"], sort=False):
        o = grp[grp.window == W6].iloc[0]; n = grp[grp.window == W5].iloc[0]
        ep.append({"domain": dom, "outcome": out,
                   "old: 2021 %": round(o.first_year_pct, 2), "old: 2026 %": round(o.last_year_pct, 2),
                   "old: Δ pp": round(o.delta_pp, 2), "old: ρ (6 pts)": round(o.rho, 3),
                   "old: exact P": round(o.P_exact_perm, 4), "old: scipy P": round(o.P_scipy_asymptotic, 4),
                   "new: 2021 %": round(n.first_year_pct, 2), "new: 2025 %": round(n.last_year_pct, 2),
                   "new: Δ pp": round(n.delta_pp, 2), "new: ρ (5 pts)": round(n.rho, 3),
                   "new: exact P": round(n.P_exact_perm, 4),
                   "new: OR/yr": None if pd.isna(n.OR_per_year) else round(n.OR_per_year, 3),
                   "new: OR 95% CI": "" if pd.isna(n.OR_per_year) else f"{n.OR_lo:.3f}–{n.OR_hi:.3f}",
                   "new: P (Wald)": fmt_p(n.P_wald),
                   "old: OR/yr (2021–2026)": None if pd.isna(o.OR_per_year) else round(o.OR_per_year, 3)})
    ep = pd.DataFrame(ep)
    ep.to_csv(OUT / "T4_endpoint_comparison.csv", index=False)
    show = ep[["domain", "outcome", "old: 2021 %", "old: 2026 %", "old: Δ pp", "old: ρ (6 pts)", "old: exact P",
               "new: 2025 %", "new: Δ pp", "new: ρ (5 pts)", "new: exact P", "new: OR/yr", "new: OR 95% CI"]]
    show = show.copy()
    for c in ["old: exact P", "new: exact P"]:
        show[c] = show[c].map(fmt_p)
    L.append(md_table(show, "{:.2f}"))
    L.append("")
    L.append("Other temporal numbers in the manuscript (old → new):\n")
    co5 = [g(ann, "Stance", "Cautious Optimism", W5, y).pct for y in Y5]
    co6 = [g(ann, "Stance", "Cautious Optimism", W6, y).pct for y in Y6]
    al5 = [g(ann, "Stance", "Alarm", W5, y).pct for y in Y5]
    L.append(f"- Cautious Optimism annual range: {min(co6):.1f}–{max(co6):.1f}% (2021–2026) → "
             f"{min(co5):.1f}–{max(co5):.1f}% (2021–2025).")
    L.append(f"- Alarm peak: {max(al5):.1f}% in {Y5[int(np.argmax(al5))]} (unchanged; 2026 value no longer an endpoint).")
    r6 = ratio
    L.append(f"- Discourse:evaluative ratio: 2.24 → 0.88 (2021→2026) becomes "
             f"{r6.ratio.iloc[0]:.2f} → {r6[r6.year == 2025].ratio.iloc[0]:.2f} (2021→2025).")
    fig1b = []
    for lab in ["Patient safety", "Hallucination / errors", "Governance / regulation", "Ethics & bias"]:
        m6 = np.mean([g(ann, "Theme (among critical)", lab, W6, y).pct for y in Y6])
        m5_ = np.mean([g(ann, "Theme (among critical)", lab, W5, y).pct for y in Y5])
        fig1b.append(f"{lab} {m6:.0f}% → {m5_:.0f}%")
    L.append("- Figure 1b legend (mean of annual prevalences): " + "; ".join(fig1b) + ".")
    m6 = mech[W6]
    L.append(f"- Generative without fabrication: {m6['gen_without_fab']:,} ({m6['gen_without_fab_pct']:.1f}%) "
             f"of {m6['n_abstract_present_critical']:,} → {m5['gen_without_fab']:,} ({m5['gen_without_fab_pct']:.1f}%) "
             f"of {m5['n_abstract_present_critical']:,}.")
    L.append(f"- Gated subset size: {m6['n_gated']:,} → {m5['n_gated']:,}. Gate recall of fabrication: "
             f"{m6['gate_recall_fab']} ({m6['gate_recall_fab_pct']:.1f}%) → {m5['gate_recall_fab']} "
             f"({m5['gate_recall_fab_pct']:.1f}%). Fabrication among gated: {m6['fab_among_gated']} "
             f"({m6['fab_among_gated_pct']:.1f}%) → {m5['fab_among_gated']} ({m5['fab_among_gated_pct']:.1f}%).")
    L.append("")

    # ---- 2026 descriptive ---------------------------------------------------
    L.append("## 6. January–April 2026 (partial year) — descriptive only, no trend statistics\n")
    L.append("CIs: percentile bootstrap of the 2026 records alone (1000 resamples, seed 42).\n")
    d = d26.copy()
    d["2026 % (95% CI); n/N"] = [f"{r.pct_2026:.1f} ({r.lo:.1f}–{r.hi:.1f}); {int(r.k)}/{int(r.N)}" for r in d.itertuples()]
    L.append(md_table(d[["domain", "outcome", "2026 % (95% CI); n/N"]]))
    L.append("\n## Output files\n")
    for fn in ["T4_annual_all_domains.csv", "T4_trend_tests.csv", "T4_endpoint_comparison.csv",
               "T4_genre_ratio.csv", "T4_theme_counts.csv", "T4_mechanism_facts.json",
               "T4_2026_descriptive.csv", "T4_figure_captions.md"]:
        L.append(f"- [{fn}]({fn})")
    L.append("- Figures: `revision_r1/figures/*_r1_draft.png|pdf`")
    (OUT / "T4_temporal_2021_2025.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
