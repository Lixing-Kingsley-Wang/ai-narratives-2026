"""C1 step 2 · Assemble the R1 numbers book (JMIR R1 Batch 2c; E12, E13, E4, E2/E8).

Reads Batch 1-2b outputs (revision_r1/outputs/) and the Batch 2c
recomputations (revision_r1/final/data/, from c1_compute.py) and writes every
number the revised manuscript will need, in JMIR format, with a stable ID and
its source file:
  revision_r1/final/NUMBERS_BOOK_R1.csv   (machine-readable)
  revision_r1/final/NUMBERS_BOOK_R1.md
No number is computed here except formatting, sums of existing counts,
CI half-widths, and the 1/OR inversion for "United States vs China".
"""

from __future__ import annotations

import json
import re

import numpy as np
import pandas as pd

from scipy.stats import beta

from c_common import (DATA, OUT, Y5, Book, ci, fn, jmirize, nN, or_ci, p_txt, pct, rc)

B = Book()
T4A = pd.read_csv(OUT / "T4_annual_all_domains.csv")
T4T = pd.read_csv(OUT / "T4_trend_tests.csv")
T5 = pd.read_csv(OUT / "T5_crosssectional_both_windows.csv")
W5 = "2021–2025"
SRC_T4 = "outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv"
BOOT = "percentile bootstrap, 1000 resamples, seed 42"


def ann(domain, outcome, year):
    r = T4A[(T4A.domain == domain) & (T4A.outcome == outcome) & (T4A.window == W5) & (T4A.year == year)]
    return r.iloc[0]


def trend(domain, outcome):
    return T4T[(T4T.domain == domain) & (T4T.outcome == outcome) & (T4T.window == W5)].iloc[0]


def share_val(p, lo, hi, k, n, d=1):
    """Share with n/N and its CI; when k=0 or k=n the bootstrap interval is degenerate,
    so the exact Clopper-Pearson interval is added."""
    k, n = int(k), int(n)
    s = f"{p:.{d}f}% ({nN(k, n)}; {ci(lo, hi, d)}"
    if n and (k == 0 or k == n):
        clo = 0.0 if k == 0 else beta.ppf(0.025, k, n - k + 1) * 100
        chi = 100.0 if k == n else beta.ppf(0.975, k + 1, n - k) * 100
        s += f" (bootstrap); exact Clopper-Pearson {ci(clo, chi, d)[7:]}"
    return s + ")"


def or_val(o, lo, hi, p, d=3):
    return f"OR {o:.{d}f} per year ({ci(lo, hi, d, unit='')}), {p_txt(p)}"


def parse_rho(s):
    """'+0.90 (P=.083)' / '-0.20 (P=1.000)' / '-1.00 (P<.001)' -> formatted 'ρ=+0.90 (P=.083)', rho."""
    m = re.match(r"\s*([+-]?[0-9.]+) \(P([=<])([0-9.]+)\)", s)
    rho, op, p = float(m[1]), m[2], float(m[3])
    return (f"ρ={rho:+.2f} (P<.001)" if op == "<" else f"ρ={rho:+.2f} ({p_txt(p)})"), rho


def parse_or(s):
    """'0.834 (0.798–0.871), P<.001' -> (or, lo, hi, P-text)."""
    m = re.match(r"\s*([0-9.]+) \(([0-9.]+)–([0-9.]+)\), P([=<])([0-9.]+)", s)
    o, lo, hi, op, p = float(m[1]), float(m[2]), float(m[3]), m[4], float(m[5])
    return o, lo, hi, ("P<.001" if op == "<" else p_txt(p))


def add_series(prefix, sec, sub, label, domain, outcome, src=SRC_T4, ann_override=None):
    """Annual values + Spearman rho (exact P) + record-level OR per year."""
    for y in Y5:
        r = ann(domain, outcome, y) if ann_override is None else ann_override[y]
        B.add(f"{prefix}-{y}", sec, sub, f"{label}, {y}", share_val(r["pct"], r["lo"], r["hi"], r["k"], r["N"]),
              r["pct"], r["lo"], r["hi"], int(r["k"]), int(r["N"]), ci_method=BOOT if ann_override is None else
              "percentile bootstrap, 1000 resamples, deterministic per-cell seed 42 + cell index", source=src)
    t = trend(domain, outcome)
    B.add(f"{prefix}-RHO", sec, sub, f"{label}: Spearman ρ across 5 annual values (exact permutation P)",
          f"ρ={t['rho']:+.2f} ({p_txt(t['P_exact_perm'])})", t["rho"], p=t["P_exact_perm"],
          ci_method="exact permutation over all 5! orderings; minimum attainable two-sided P=.017", source=src)
    if not pd.isna(t["OR_per_year"]):
        B.add(f"{prefix}-OR", sec, sub, f"{label}: unadjusted record-level logistic OR per year",
              or_val(t["OR_per_year"], t["OR_lo"], t["OR_hi"], t["P_wald"]), t["OR_per_year"], t["OR_lo"], t["OR_hi"],
              int(t["events"]), int(t["n_records"]), t["P_wald"], ci_method="Wald", source=src)
    B.add(f"{prefix}-DELTA", sec, sub, f"{label}: change 2021 to 2025, percentage points",
          f"{t['delta_pp']:+.1f} percentage points ({t['first_year_pct']:.1f}% to {t['last_year_pct']:.1f}%)",
          t["delta_pp"], source=src)


# =====================================================================
# 1. Corpus and flow
# =====================================================================
def corpus():
    S = "Corpus and flow"
    f = pd.read_csv(DATA / "flow_2021_2025.csv")
    for i, r in enumerate(f.itertuples(), 1):
        B.add(f"COR-{i:02d}", S, "Record flow (Figure 1)", r.label.strip(), fn(r.n), r.n, n=r.n,
              window="retrieval to 2021-2025 analytic set", source="final/data/flow_2021_2025.csv (from outputs/T6_*.csv and prefilter files)")
    k = dict(zip(f.key, f.n))
    B.add("COR-Q1Q2-PCT", S, "Record flow (Figure 1)", "Q1/Q2 share of records screened for SJR quartile",
          f"{k['q1q2']/k['sjr_screened']*100:.1f}% ({nN(k['q1q2'], k['sjr_screened'])})", k["q1q2"] / k["sjr_screened"] * 100,
          k=k["q1q2"], n=k["sjr_screened"], window="retrieval", source="outputs/T6_stage_table.csv; output/sjr.log")
    q3 = trend("Q3 comparison arm", "Critical (Alarm+Caution)")
    B.add("COR-Q3-N", S, "Record flow (Figure 1)", "Q3 comparison arm, valid stance, 2021-2025", fn(q3["n_records"]),
          q3["n_records"], n=q3["n_records"], source=SRC_T4)
    b1 = pd.read_csv(OUT / "B1/prefilter_exact_ci_long.csv")
    b1 = b1[b1.variant == "primary"].set_index("estimate_name")
    r = b1.loc["FNrate_pooled"]
    B.add("COR-AUDIT-FN", S, "Record flow (Figure 1)", "Estimated AI-engaged among prefilter-excluded records (1-NPV, pooled 2021-2025)",
          f"{r.estimate*100:.1f}% ({ci(r.jeffreys_lo*100, r.jeffreys_hi*100)})", r.estimate * 100, r.jeffreys_lo * 100,
          r.jeffreys_hi * 100, ci_method="Jeffreys Beta(k+1/2, n-k+1/2), 10,000 draws per cell, seed 42 (Amendment 3)",
          source="outputs/B1/prefilter_exact_ci_long.csv")
    r = b1.loc["missed_total"]
    B.add("COR-AUDIT-MISSED", S, "Record flow (Figure 1)", "Estimated AI-engaged records missed by the prefilter, 2021-2025",
          f"{fn(r.estimate)} ({ci(r.jeffreys_lo, r.jeffreys_hi, 0, unit='')})".replace("95% CI ", "95% CI "),
          r.estimate, r.jeffreys_lo, r.jeffreys_hi, ci_method="Jeffreys (Amendment 3)", source="outputs/B1/prefilter_exact_ci_long.csv")
    s = pd.read_csv(DATA / "subsets_2021_2025.csv")
    for i, r in enumerate(s.itertuples(), 1):
        B.add(f"COR-SUB-{i:02d}", S, "Downstream analytic subsets", r.label,
              f"{fn(r.n)} of {fn(r.denominator)} ({r.n/r.denominator*100:.1f}%)", r.n, k=r.n, n=r.denominator,
              source="final/data/subsets_2021_2025.csv")
    B.add("COR-2026-N", S, "Downstream analytic subsets", "January-April 2026 records with valid stance (descriptive table only)",
          "2689", 2689, n=2689, window="January-April 2026", source="outputs/T4_2026_descriptive.csv")


# =====================================================================
# 2. Missing data
# =====================================================================
def missing():
    S = "Missing data, 2021-2025 (E14)"
    m = pd.read_csv(DATA / "missing_2021_2025.csv")
    for i, r in enumerate(m.itertuples(), 1):
        B.add(f"MIS-{i:02d}", S, "Losses by stage, records dated 2021-2025", re.sub(r"^\d+[ab]?\. ", "", r.stage),
              f"{fn(r.total_2021_2025)} (2021: {r._2}; 2022: {r._3}; 2023: {r._4}; 2024: {r._5}; 2025: {r._6})",
              r.total_2021_2025, n=r.total_2021_2025, source="final/data/missing_2021_2025.csv (from outputs/T6_losses_by_year.csv)")
    t = pd.read_csv(DATA / "title_only_2021_2025.csv")
    for i, r in enumerate(t.itertuples(), 1):
        B.add(f"MIS-TO-{i:02d}", S, "Title-only (empty abstract) records by stage", r.stage,
              f"{r.pct:.1f}% ({nN(r.empty_abstract, r.N)})", r.pct, k=r.empty_abstract, n=r.N,
              source="final/data/title_only_2021_2025.csv (from outputs/T6_title_only_by_stage.csv)")
    B.add("MIS-NOTE-01", S, "Handling rules", "Handling of missing values",
          "Complete-case: records with a FAILED or missing label for a variable are excluded from analyses of that variable "
          "only; no imputation. Unknown region is kept as its own level in regression (B4).", source="outputs/T6_missing_data.md; outputs/B4/B4_regression.md")


# =====================================================================
# 3. Sample size and precision
# =====================================================================
def precision():
    S = "Sample size and precision (E2/E8)"
    B.add("PRE-00", S, "Design statement", "Sample size",
          "The analytic corpus is a census of all eligible Q1/Q2 records published 2021-2025 that the prefilter retained "
          "(n=14,058); no sample was drawn and no power calculation applies. Precision is reported as the 95% CI half-width.",
          source="final/data/flow_2021_2025.csv")
    o = T5[(T5.window == W5) & (T5.analysis == "Overall stance") & (T5.group == "Critical")].iloc[0]
    B.add("PRE-ALL", S, "Overall", "Critical share, all records: n and 95% CI half-width",
          f"n={fn(o.n)}; half-width {(o.hi-o.lo)/2:.1f} percentage points", (o.hi - o.lo) / 2, n=o.n,
          ci_method=BOOT, source="outputs/T5_crosssectional_both_windows.csv")
    for y in Y5:
        r = ann("Stance", "Critical (Alarm+Caution)", y)
        B.add(f"PRE-YR-{y}", S, "By year", f"Critical share {y}: n and half-width",
              f"n={fn(r.N)}; half-width {(r.hi-r.lo)/2:.1f} percentage points", (r.hi - r.lo) / 2, n=r.N, ci_method=BOOT, source=SRC_T4)
    sp = pd.read_csv(DATA / "specialty_2021_2025.csv")
    for r in sp.itertuples():
        B.add(f"PRE-SPC-{slug(r.specialty)}", S, "By specialty", f"{r.specialty}: n and half-width",
              f"n={fn(r.n)}; half-width {(r.hi-r.lo)/2:.1f} percentage points", (r.hi - r.lo) / 2, n=r.n, ci_method=BOOT,
              source="final/data/specialty_2021_2025.csv")
    rg = pd.read_csv(DATA / "region_2021_2025.csv")
    for r in rg.itertuples():
        B.add(f"PRE-REG-{slug(r.region)}", S, "By region", f"{r.region}: n and half-width",
              f"n={fn(r.n)}; half-width {(r.hi-r.lo)/2:.1f} percentage points", (r.hi - r.lo) / 2, n=r.n, ci_method=BOOT,
              source="final/data/region_2021_2025.csv")
    pt = pd.read_csv(DATA / "pubtype_stance.csv")
    for r in pt[pt.outcome == "Critical"].itertuples():
        B.add(f"PRE-PT-{slug(r.pubtype)}", S, "By publication type", f"{r.pubtype}: n and half-width",
              f"n={fn(r.n)}; half-width {(r.hi-r.lo)/2:.1f} percentage points", (r.hi - r.lo) / 2, n=r.n, ci_method=BOOT,
              source="final/data/pubtype_stance.csv")


def slug(s):
    s = re.sub(r"[^A-Za-z0-9]+", "", s.replace("&", "and").replace("/", " ").title())
    return s[:24].upper()


# =====================================================================
# 4. Validation
# =====================================================================
def validation():
    S = "Validation (Table 1)"
    vc = pd.read_csv(DATA / "validation_ci.csv")

    def vrow(id_, sub, item, step, set_, stat, d=3, src="final/data/validation_ci.csv"):
        r = vc[(vc.step == step) & (vc.set == set_) & (vc.statistic == stat)].iloc[0]
        if stat.endswith("%"):
            v = f"{r.point:.1f}% ({nN(r.k, r.n)}; {ci(r.lo, r.hi)})"
        elif pd.isna(r.lo):
            v = f"{r.point:.{d}f}"
        else:
            v = f"{r.point:.{d}f} ({ci(r.lo, r.hi, d, unit='')})"
        B.add(id_, S, sub, item, v, r.point, r.lo, r.hi, r.k if not pd.isna(r.k) else None, r.n, ci_method=r.ci,
              window="validation sample", source=src)

    # prefilter pilot (T1)
    t1 = pd.read_csv(OUT / "T1_binary_keep_drop_metrics.csv").set_index("metric")
    sub = "Prefilter, development pilot (T1)"
    B.add("VAL-PF-PILOT-DESIGN", S, sub, "Design", "200 records; sampling undocumented (year mix consistent with simple random "
          "sampling of eligible records, χ²=2.57, df=5, P=.77); one coder; no written codebook; 3 classes", n=200,
          window="validation sample", source="outputs/T1_prefilter_validation.md")
    B.add("VAL-PF-PILOT-RAW", S, sub, "3-class raw agreement", "85.5% (171/200)", 85.5, k=171, n=200,
          window="validation sample", source="outputs/T1_prefilter_validation.md")
    B.add("VAL-PF-PILOT-K3", S, sub, "3-class Cohen κ", "0.511 (95% CI 0.345-0.646)", 0.511, 0.345, 0.646, n=200,
          ci_method=BOOT + " (recomputed; original CI code not found)", window="validation sample",
          source="outputs/T1_prefilter_validation.md")
    for m, lab in (("sensitivity", "KEEP sensitivity"), ("specificity", "KEEP specificity"), ("PPV", "PPV"), ("NPV", "NPV"),
                   ("kappa", "KEEP/DROP Cohen κ"), ("AC1", "KEEP/DROP Gwet AC1")):
        r = t1.loc[m]
        if m in ("kappa", "AC1"):
            v = f"{r.point:.3f} ({ci(r.ci_lo, r.ci_hi, 3, unit='')})"
        else:
            v = f"{r.point*100:.1f}% ({r['n/N']}; {ci(r.ci_lo*100, r.ci_hi*100)})"
        B.add(f"VAL-PF-PILOT-{m.upper()}", S, sub, lab, v, r.point, r.ci_lo, r.ci_hi, ci_method=BOOT,
              window="validation sample", source="outputs/T1_binary_keep_drop_metrics.csv")

    # prefilter audit (A3; B1 Jeffreys primary)
    sub = "Prefilter, R1 audit (A3; Amendments 2-3)"
    man = pd.read_csv(rc.R1 / "coding/prefilter_sampling_manifest.csv")
    des = "; ".join(f"{s} {int(man[man.stratum == s].sample_n.sum())}" for s in ("EX-F", "EX-S", "RET", "PILOT"))
    B.add("VAL-PF-AUDIT-DESIGN", S, sub, "Design",
          f"370 records stratified by prefilter outcome x year 2021-2025 ({des}); design-weighted to frame sizes; "
          "codebook verbatim from the classifier prompt; one coder blinded to model labels and stratum; frozen protocol "
          "(commits 0d21f6c, 47cf6fe)", n=370, window="validation sample", source="coding/PROTOCOL_r1_validation.md")
    b1 = pd.read_csv(OUT / "B1/prefilter_exact_ci_long.csv")
    b1 = b1[b1.variant == "primary"].set_index("estimate_name")
    for key, lab, kind in (("prod2x2_sensitivity", "Production prefilter sensitivity (population-weighted)", "pct"),
                           ("prod2x2_specificity", "Production prefilter specificity", "pct"),
                           ("prod2x2_PPV", "Production prefilter PPV", "pct"),
                           ("prod2x2_NPV", "Production prefilter NPV", "pct"),
                           ("prod2x2_kappa", "Production prefilter Cohen κ", "k"),
                           ("prod2x2_AC1", "Production prefilter Gwet AC1", "k"),
                           ("FNrate_pooled", "False-negative rate among excluded records (1-NPV), pooled", "pct"),
                           ("FNrate_2021_2022", "1-NPV, 2021-2022", "pct"), ("FNrate_2024_2025", "1-NPV, 2024-2025", "pct"),
                           ("FNrate_diff_2024_25_minus_2021_22", "1-NPV difference, 2024-2025 minus 2021-2022 (percentage points)", "pp"),
                           ("missed_total", "Estimated missed AI-engaged records, 2021-2025", "n"),
                           ("PPV_RET_pooled", "PPV among retained records, pooled", "pct"),
                           ("fullabs_precision_pooled", "Full-abstract re-run precision (EX-F), pooled", "pct")) + tuple(
            (f"FNrate_{y}", f"1-NPV, {y}", "pct") for y in Y5) + tuple((f"missed_{y}", f"Estimated missed records, {y}", "n") for y in Y5):
        r = b1.loc[key]
        if kind == "pct":
            v = f"{r.estimate*100:.1f}% ({ci(r.jeffreys_lo*100, r.jeffreys_hi*100)})"
            pt, lo, hi = r.estimate * 100, r.jeffreys_lo * 100, r.jeffreys_hi * 100
        elif kind == "pp":
            v = f"{r.estimate*100:+.1f} percentage points ({ci(r.jeffreys_lo*100, r.jeffreys_hi*100, unit='')})"
            pt, lo, hi = r.estimate * 100, r.jeffreys_lo * 100, r.jeffreys_hi * 100
        elif kind == "n":
            v = f"{fn(r.estimate)} ({ci(r.jeffreys_lo, r.jeffreys_hi, 0, unit='')})"
            pt, lo, hi = r.estimate, r.jeffreys_lo, r.jeffreys_hi
        else:
            v = f"{r.estimate:.3f} ({ci(r.jeffreys_lo, r.jeffreys_hi, 3, unit='')})"
            pt, lo, hi = r.estimate, r.jeffreys_lo, r.jeffreys_hi
        B.add(f"VAL-PF-AUDIT-{slug(key)}", S, sub, lab, v, pt, lo, hi,
              ci_method="Jeffreys Beta(k+1/2, n-k+1/2), 10,000 draws per cell, seed 42", window="2021-2025 frame",
              source="outputs/B1/prefilter_exact_ci_long.csv")
    for key, lab in (("full2x2_sensitivity", "Full-abstract re-run sensitivity"), ("full2x2_specificity", "Full-abstract specificity"),
                     ("full2x2_PPV", "Full-abstract PPV"), ("full2x2_NPV", "Full-abstract NPV"), ("full2x2_kappa", "Full-abstract Cohen κ")):
        r = b1.loc[key]
        if key.endswith("kappa"):
            v = f"{r.estimate:.3f} ({ci(r.boot_lo, r.boot_hi, 3, unit='')})"
            pt, lo, hi = r.estimate, r.boot_lo, r.boot_hi
        else:
            v = f"{r.estimate*100:.1f}% ({ci(r.boot_lo*100, r.boot_hi*100)})"
            pt, lo, hi = r.estimate * 100, r.boot_lo * 100, r.boot_hi * 100
        B.add(f"VAL-PF-AUDIT-{slug(key)}", S, sub, lab, v, pt, lo, hi,
              ci_method="within-cell percentile bootstrap, 1000, seed 42 (Jeffreys not used for the full-abstract 2x2; Amendment 3)",
              window="2021-2025 frame", source="outputs/B1/prefilter_exact_ci_long.csv")
    vrow("VAL-PF-INTRA-AGREE", sub, "Intra-rater agreement, KEEP/DROP (20 pilot records recoded)", "prefilter intra-rater",
         "20 pilot records recoded", "KEEP/DROP agreement %")
    vrow("VAL-PF-INTRA-AGREE3", sub, "Intra-rater agreement, 3-class", "prefilter intra-rater", "20 pilot records recoded",
         "3-class agreement %")
    vrow("VAL-PF-INTRA-K", sub, "Intra-rater Cohen κ, KEEP/DROP", "prefilter intra-rater", "20 pilot records recoded",
         "KEEP/DROP Cohen κ")

    # stance
    sub = "Stance (Table S18; T2)"
    B.add("VAL-ST-DESIGN", S, sub, "Design", "300 records stratified by model-assigned stance (Alarm 40, Caution 60, Neutral 70, "
          "Cautious Optimism 100, Advocacy 30), abstract-present records only; one coder blinded to model labels; in-scope "
          "layer excludes 75 records the coder flagged as not codable or out of scope", n=300, window="validation sample",
          source="outputs/T2_stance_perclass.md")
    vrow("VAL-ST-QK-225", sub, "Quadratic-weighted Cohen κ, in-scope (n=225)", "stance", "in-scope (n=225)", "quadratic-weighted Cohen κ", 2)
    vrow("VAL-ST-QK-300", sub, "Quadratic-weighted Cohen κ, all records (n=300)", "stance", "all records (n=300)", "quadratic-weighted Cohen κ", 2)
    vrow("VAL-ST-UK-225", sub, "Unweighted Cohen κ, in-scope", "stance", "in-scope (n=225)", "unweighted Cohen κ", 2)
    vrow("VAL-ST-RAW-225", sub, "Exact agreement, in-scope", "stance", "in-scope (n=225)", "raw agreement %")
    vrow("VAL-ST-RAW-300", sub, "Exact agreement, all records", "stance", "all records (n=300)", "raw agreement %")
    for lay, f_ in (("225", "T2_perclass_inscope225.csv"), ("300", "T2_perclass_all300.csv")):
        pc = pd.read_csv(OUT / f_).set_index("class")
        r = pc.loc["macro-F1"]
        B.add(f"VAL-ST-MACROF1-{lay}", S, sub, f"Macro-F1 (5 classes), n={lay}", f"{r.F1:.2f} ({ci(r.F1_lo, r.F1_hi, 2, unit='')})",
              r.F1, r.F1_lo, r.F1_hi, n=int(lay), ci_method=BOOT, window="validation sample", source=f"outputs/{f_}")
        for c in rc.STANCES:
            q = pc.loc[c]
            B.add(f"VAL-ST-F1-{slug(c)}-{lay}", S, sub, f"{c}: precision / recall / F1, n={lay}",
                  f"precision {q.precision:.2f} ({ci(q.precision_lo, q.precision_hi, 2, unit='')}); recall {q.recall:.2f} "
                  f"({ci(q.recall_lo, q.recall_hi, 2, unit='')}); F1 {q.F1:.2f} ({ci(q.F1_lo, q.F1_hi, 2, unit='')}); "
                  f"support {int(q.support_human)}", q.F1, q.F1_lo, q.F1_hi, n=int(lay), ci_method=BOOT,
                  window="validation sample", source=f"outputs/{f_}")
    cv = pd.read_csv(OUT / "T2_collapsed_views.csv")
    cv = cv[cv["view"].notna()]
    for lay, laylab in (("in-scope (n=225)", "225"), ("all (n=300)", "300")):
        for m in ("sensitivity", "PPV"):
            r = cv[(cv.layer == lay) & (cv.view == "Advocacy vs not Advocacy") & (cv.metric == m)].iloc[0]
            B.add(f"VAL-ST-ADV-{m.upper()}-{laylab}", S, sub, f"Advocacy {m}, n={laylab}",
                  f"{r.point*100:.1f}% ({r['n/N']}; {ci(r.lo*100, r.hi*100)})", r.point * 100, r.lo * 100, r.hi * 100,
                  ci_method=BOOT, window="validation sample", source="outputs/T2_collapsed_views.csv")
    vrow("VAL-ST-RTR-QK", sub, "Run-to-run stability (two re-inferences at T=1.0): quadratic-weighted κ", "stance run-to-run",
         "300 validation records, two re-inferences", "quadratic-weighted Cohen κ")
    vrow("VAL-ST-RTR-RAW", sub, "Run-to-run stability: raw agreement", "stance run-to-run",
         "300 validation records, two re-inferences", "raw agreement %")

    # themes
    sub = "Themes (A1; Amendment 1)"
    B.add("VAL-TH-DESIGN", S, sub, "Design", "200 critical records 2021-2025, 40 per year by simple random sampling within year "
          "(frame 4283); one coder blinded to model labels; codebook verbatim from the classifier prompt; frozen protocol "
          "(commit 0d21f6c); primary analysis N=200 (Amendment 1), pre-specified analysis N=187", n=200,
          window="validation sample", source="coding/PROTOCOL_r1_validation.md")
    for tag, f_, N in (("200", "A4_theme_primary_n200/theme_scores_long.csv", 200), ("187", "A4_theme/theme_scores_long.csv", 187)):
        md = (OUT / f_.replace("theme_scores_long.csv", "theme_scores.md")).read_text()
        for wt in ("unweighted", "weighted"):
            m = re.search(rf"\| All 2021–2025 \| {wt} \| ([0-9.]+) \(([0-9.]+)–([0-9.]+)\) \| ([0-9.]+) \(([0-9.]+)–([0-9.]+)\)", md)
            mi, mlo, mhi, ma, alo, ahi = map(float, m.groups())
            B.add(f"VAL-TH-MICRO-{tag}-{wt[:2].upper()}", S, sub, f"Micro-F1, N={N}, {wt}", f"{mi:.3f} ({ci(mlo, mhi, 3, unit='')})",
                  mi, mlo, mhi, n=N, ci_method="within-year percentile bootstrap, 1000, seed 42", window="validation sample",
                  source=f"outputs/{f_.replace('theme_scores_long.csv', 'theme_scores.md')}")
            B.add(f"VAL-TH-MACRO-{tag}-{wt[:2].upper()}", S, sub, f"Macro-F1, N={N}, {wt}", f"{ma:.3f} ({ci(alo, ahi, 3, unit='')})",
                  ma, alo, ahi, n=N, ci_method="within-year percentile bootstrap, 1000, seed 42", window="validation sample",
                  source=f"outputs/{f_.replace('theme_scores_long.csv', 'theme_scores.md')}")
        f1s = {}
        for th, lab in (("hallucination", "Hallucination / errors"), ("safety_clinical", "Patient safety"),
                        ("ethics_bias", "Ethics & bias"), ("regulation", "Governance / regulation")):
            m = re.search(rf"\| {th} \| (\d+) \|[^|]*\| ([0-9.]+) \(([0-9.]+)–([0-9.]+)\) \| ([0-9.]+) \(([0-9.]+)–([0-9.]+)\) \| ([0-9.]+) \(([0-9.]+)–([0-9.]+)\)", md)
            g = m.groups()
            f1, flo, fhi = float(g[7]), float(g[8]), float(g[9])
            f1s[lab] = f1
            B.add(f"VAL-TH-F1-{slug(lab)}-{tag}", S, sub, f"{lab}: F1 (unweighted), N={N}",
                  f"F1 {f1:.3f} ({ci(flo, fhi, 3, unit='')}); precision {float(g[1]):.3f}; recall {float(g[4]):.3f}; "
                  f"human-positive n={g[0]}", f1, flo, fhi, n=N, ci_method="within-year percentile bootstrap, 1000, seed 42",
                  window="validation sample", source=f"outputs/{f_.replace('theme_scores_long.csv', 'theme_scores.md')}")
        lo_t, hi_t = min(f1s, key=f1s.get), max(f1s, key=f1s.get)
        B.add(f"VAL-TH-F1RANGE-{tag}", S, sub, f"F1 range, four headline themes, N={N}",
              f"{f1s[lo_t]:.3f} ({lo_t}) to {f1s[hi_t]:.3f} ({hi_t})", n=N, window="validation sample",
              source=f"outputs/{f_.replace('theme_scores_long.csv', 'theme_scores.md')}")

    # mechanism
    sub = "Mechanism (T3)"
    B.add("VAL-MX-DESIGN", S, sub, "Design", "120 critical records stratified by year and model-assigned failure mode; 12 title-only "
          "records excluded (n=108); one coder blinded to model labels", n=108, window="validation sample",
          source="outputs/T3_mechanism_confusion.md")
    for ax, tag in (("model type", "MT"), ("failure mode", "FM")):
        vrow(f"VAL-MX-{tag}-K", sub, f"{ax.capitalize()}: Cohen κ", f"mechanism, {ax}", "abstract-present (n=108)", "Cohen κ", 2)
        vrow(f"VAL-MX-{tag}-AC1", sub, f"{ax.capitalize()}: Gwet AC1", f"mechanism, {ax}", "abstract-present (n=108)", "Gwet AC1", 2)
        vrow(f"VAL-MX-{tag}-RAW", sub, f"{ax.capitalize()}: raw agreement", f"mechanism, {ax}", "abstract-present (n=108)", "raw agreement %")
        vrow(f"VAL-MX-{tag}-KMAX", sub, f"{ax.capitalize()}: κ_max", f"mechanism, {ax}", "abstract-present (n=108)", "κ_max", 3)
    fd = pd.read_csv(OUT / "T3_fabrication_direction.csv", index_col=0)
    B.add("VAL-MX-FABDIR", S, sub, "Fabrication disagreements: model fabrication-involved, human not vs human fabrication-involved, model not",
          f"{int(fd.loc['Human: not fabrication', 'Model: fabrication-involved'])} vs {int(fd.loc['Human: fabrication-involved', 'Model: not fabrication'])} "
          f"(model fabrication-involved {int(fd.loc['Column total', 'Model: fabrication-involved'])}/108; human {int(fd.loc['Human: fabrication-involved', 'Row total'])}/108)",
          window="validation sample", source="outputs/T3_fabrication_direction.csv")

    # specialty
    sub = "Specialty"
    B.add("VAL-SP-DESIGN", S, sub, "Design", "120 records stratified by model-assigned specialty, with an 'unclear from abstract' "
          "option for the coder; one coder blinded to model labels", n=120, window="validation sample",
          source="output/analyses/specialty_kappa_report.md")
    vrow("VAL-SP-K", sub, "Cohen κ (unweighted, 'Unclear' as its own category)", "specialty", "all coded (n=120)", "Cohen κ", 2)
    vrow("VAL-SP-AC1", sub, "Gwet AC1", "specialty", "all coded (n=120)", "Gwet AC1", 2)
    vrow("VAL-SP-RAW", sub, "Raw agreement", "specialty", "all coded (n=120)", "raw agreement %")
    vrow("VAL-SP-KMAX", sub, "κ_max", "specialty", "all coded (n=120)", "κ_max", 3)

    # symmetric endorsement (B3)
    sub = "Symmetric endorsement flag vs human Advocacy (B3)"
    ag = pd.read_csv(OUT / "B3/B3_agreement.csv")
    for (_, r), tag in zip(ag.iterrows(), ("ALL", "INSCOPE")):
        for col, lab in (("sensitivity", "sensitivity"), ("PPV", "PPV"), ("Cohen κ", "Cohen κ")):
            s = r[col]
            m = re.match(r"(?:(\d+)/(\d+) = )?([0-9.]+) \(([0-9.]+)–([0-9.]+)\)", s)
            k, n, p, lo, hi = m.groups()
            if k:
                v = f"{float(p)*100:.1f}% ({k}/{n}; {ci(float(lo)*100, float(hi)*100)})"
            else:
                v = f"{float(p):.2f} ({ci(float(lo), float(hi), 2, unit='')})"
            B.add(f"VAL-B3-{tag}-{slug(lab)}", S, sub, f"{r.set} (n={r.n}): {lab}", v, float(p), float(lo), float(hi),
                  ci_method=BOOT, window="validation sample", source="outputs/B3/B3_agreement.csv")


# =====================================================================
# 5. Results
# =====================================================================
def results():
    S = "Results, 2021-2025"
    # 5.1 overall
    sub = "1. Overall stance distribution"
    for s in rc.STANCES + ["Critical", "Favourable"]:
        r = T5[(T5.window == W5) & (T5.analysis == "Overall stance") & (T5.group == s)].iloc[0]
        B.add(f"RES-OVR-{slug(s)}", S, sub, s, share_val(r.value, r.lo, r.hi, int(r.k), int(r.n)), r.value, r.lo, r.hi,
              int(r.k), int(r.n), ci_method=BOOT, source="outputs/T5_crosssectional_both_windows.csv")

    # 5.2 temporal
    sub = "2. Temporal trends"
    for code, out in (("ALARM", "Alarm"), ("CAUT", "Caution"), ("NEUT", "Neutral"), ("CO", "Cautious Optimism"),
                      ("ADV", "Advocacy"), ("CRIT", "Critical (Alarm+Caution)"), ("FAV", "Favourable (CO+Advocacy)")):
        add_series(f"RES-TMP-{code}", S, sub, out, "Stance", out)
    b4 = pd.read_csv(OUT / "B4/B4_primary_critical_ORs.csv")
    r = b4[b4.variable == "year_c"].iloc[0] if (b4.variable == "year_c").any() else b4[b4.term == "year_c"].iloc[0]
    B.add("RES-TMP-CRIT-AOR", S, sub, "Critical: adjusted OR per year (B4 primary; genre, publication type, specialty, region; "
          "journal-clustered SEs)", or_val(r.OR_adj, r.lo_adj, r.hi_adj, r.P_adj), r.OR_adj, r.lo_adj, r.hi_adj, 4283, 14058, r.P_adj,
          ci_method="Wald, cluster-robust by journal (2278 clusters)", source="outputs/B4/B4_primary_critical_ORs.csv")
    sens = pd.read_csv(OUT / "B4/B4_sensitivity_ORs.csv")
    for rr in sens[(sens.model == "S1 year categorical") & (sens.variable == "year")].itertuples():
        B.add(f"RES-TMP-CRIT-CAT-{int(float(rr.level))}", S, sub, f"Critical: adjusted OR, {int(float(rr.level))} vs 2021 (B4 S1, categorical year)",
              or_ci(rr.OR, rr.lo, rr.hi, 2, rr.P), rr.OR, rr.lo, rr.hi, p=rr.P, ci_method="Wald, cluster-robust by journal",
              source="outputs/B4/B4_sensitivity_ORs.csv")
    adv = pd.read_csv(OUT / "B4/B4_advocacy_ORs.csv")
    r = adv[adv.term == "year_c"].iloc[0]
    B.add("RES-TMP-ADV-AOR", S, sub, "Advocacy: adjusted OR per year (B4 secondary 2)", or_val(r.OR, r.lo, r.hi, r.P),
          r.OR, r.lo, r.hi, 218, 14058, r.P, ci_method="Wald, cluster-robust by journal", source="outputs/B4/B4_advocacy_ORs.csv")
    B.add("RES-TMP-ADV-CAT", S, sub, "Advocacy: categorical-year adjusted ORs",
          "Not produced: B4 fitted the categorical-year model (S1) for the critical outcome only; the Advocacy model used "
          "continuous year. Fitting it would be a new analysis.", source="outputs/B4/B4_regression.md")
    amp = pd.read_csv(OUT / "B4/B4_primary_critical_AMP.csv")
    for rr in amp[amp.variable == "year"].itertuples():
        B.add(f"RES-TMP-CRIT-AMP-{int(rr.level)}", S, sub, f"Critical: adjusted average marginal probability, {int(rr.level)}",
              f"{rr._4:.1f}% ({ci(rr.lo, rr.hi)})", rr._4, rr.lo, rr.hi, ci_method="delta method on the logit scale, cluster-robust",
              source="outputs/B4/B4_primary_critical_AMP.csv")
    # strong endorsement (B3)
    b3 = pd.read_csv(OUT / "B3/B3_trend.csv").set_index("outcome")
    for row_lab, code in (("Strong endorsement (flag yes)", "SE"), ("Strong endorsement, upper bound (FAILED as yes)", "SEUB")):
        r = b3.loc[row_lab]
        for y in Y5:
            m = re.match(r"([0-9.]+) \(([0-9.]+)–([0-9.]+)\); (\d+)/(\d+)", r[str(y)])
            p, lo, hi, k, n = float(m[1]), float(m[2]), float(m[3]), int(m[4]), int(m[5])
            B.add(f"RES-TMP-{code}-{y}", S, sub, f"{row_lab}, {y}", share_val(p, lo, hi, k, n), p, lo, hi, k, n, ci_method=BOOT,
                  source="outputs/B3/B3_trend.csv")
        txt, rho = parse_rho(r["Spearman ρ (exact P)"])
        B.add(f"RES-TMP-{code}-RHO", S, sub, f"{row_lab}: Spearman ρ (exact P)", txt, rho,
              ci_method="exact permutation", source="outputs/B3/B3_trend.csv")
        o, lo, hi, pt_ = parse_or(r["OR/yr (95% CI), P"])
        B.add(f"RES-TMP-{code}-OR", S, sub, f"{row_lab}: unadjusted OR per year",
              f"OR {o:.3f} per year ({ci(lo, hi, 3, unit='')}), {pt_}", o, lo, hi, ci_method="Wald", source="outputs/B3/B3_trend.csv")
    # within genre (Table S3 values, deterministic seeds; trend tests from T4)
    s3 = pd.read_csv(OUT / "B7_tableS3_2021_2025.csv")
    for g in ("discourse", "evaluative"):
        ov = {}
        for r in s3[s3.genre == g].itertuples():
            ov[r.year] = {"pct": r._7, "lo": r.lo, "hi": r.hi, "k": r.k, "N": r.n}
        add_series(f"RES-TMP-GEN{g[:4].upper()}", S, sub, f"Critical share within {g} records", f"Within genre: {g}",
                   "Critical (Alarm+Caution)", src="outputs/B7_tableS3_2021_2025.csv; outputs/T4_trend_tests.csv", ann_override=ov)
    gr = pd.read_csv(OUT / "T4_genre_ratio.csv")
    for r in gr[gr.year <= 2025].itertuples():
        B.add(f"RES-TMP-GENRATIO-{r.year}", S, sub, f"Discourse:evaluative ratio, {r.year}", f"{r.ratio:.2f} ({r.n_discourse}/{r.n_evaluative})",
              r.ratio, source="outputs/T4_genre_ratio.csv")
    # themes
    for t in rc.THEMES:
        lab = rc.THEME_LABELS[t]
        add_series(f"RES-TMP-TH-{slug(lab)}", S, sub, f"Theme among critical records: {lab}", "Theme (among critical)", lab)
    # mechanism
    for code, dom, out in (("FM-CONF", "Mechanism, hallucination-gated (failure-mode composition)", "Confabulation (fabrication only)"),
                           ("FM-MIS", "Mechanism, hallucination-gated (failure-mode composition)", "Misclassification (factual error)"),
                           ("FM-BOTH", "Mechanism, hallucination-gated (failure-mode composition)", "Both"),
                           ("FM-NONE", "Mechanism, hallucination-gated (failure-mode composition)", "None or unclear"),
                           ("FAB-GATED", "Mechanism, hallucination-gated", "Fabrication-involved (confabulation or both)"),
                           ("GENSHARE", "Mechanism, all abstract-present critical", "Generative-model share (generative or both)"),
                           ("FAB-ALL", "Mechanism, all abstract-present critical", "Fabrication share (confabulation or both)"),
                           ("FAB-GEN", "Mechanism, generative-model papers", "Fabrication share among generative")):
        add_series(f"RES-TMP-{code}", S, sub, f"{dom}: {out}", dom, out)
    mf = json.loads((OUT / "T4_mechanism_facts.json").read_text())[W5]
    B.add("RES-TMP-MECH-GENNOFAB", S, sub, "Generative-model papers without a fabrication concern, abstract-present critical",
          f"{mf['gen_without_fab_pct']:.1f}% ({nN(mf['gen_without_fab'], mf['n_abstract_present_critical'])})",
          mf["gen_without_fab_pct"], k=mf["gen_without_fab"], n=mf["n_abstract_present_critical"], source="outputs/T4_mechanism_facts.json")
    B.add("RES-TMP-MECH-FABDISC", S, sub, "Fabrication raised in a discriminative-only system", str(mf["fab_in_discriminative_only"]),
          mf["fab_in_discriminative_only"], source="outputs/T4_mechanism_facts.json")
    k, n = map(int, mf["gate_recall_fab"].split("/"))
    B.add("RES-TMP-MECH-GATERECALL", S, sub, "Share of fabrication-involved records captured by the hallucination theme",
          f"{mf['gate_recall_fab_pct']:.1f}% ({nN(k, n)})", mf["gate_recall_fab_pct"], k=k, n=n, source="outputs/T4_mechanism_facts.json")
    k, n = map(int, mf["fab_among_gated"].split("/"))
    B.add("RES-TMP-MECH-FABGATED", S, sub, "Fabrication-involved share among hallucination-gated records, pooled",
          f"{mf['fab_among_gated_pct']:.1f}% ({nN(k, n)})", mf["fab_among_gated_pct"], k=k, n=n, source="outputs/T4_mechanism_facts.json")
    add_series("RES-TMP-KEEP", S, sub, "Prefilter keep rate", "Prefilter keep rate", "Kept (discourse or evaluative)")
    for code, out in (("CRIT", "Critical (Alarm+Caution)"), ("ALARM", "Alarm"), ("CAUT", "Caution"), ("NEUT", "Neutral"),
                      ("CO", "Cautious Optimism"), ("ADV", "Advocacy")):
        add_series(f"RES-TMP-Q3-{code}", S, sub, f"Q3 comparison arm: {out}", "Q3 comparison arm", out)

    # 5.3 themes, both measures
    sub = "3. Headline themes: LLM prevalence share and lexicon mention share"
    lex_name = {"Patient safety": "Patient safety", "Hallucination / errors": "Errors and hallucination",
                "Governance / regulation": "Regulation", "Ethics & bias": "Ethics and bias"}
    la = pd.read_csv(OUT / "B6/B6_lexicon_annual.csv"); lt = pd.read_csv(OUT / "B6/B6_lexicon_trends.csv").set_index("lexicon theme")
    for lab, lx in lex_name.items():
        for r in la[la["lexicon theme"] == lx].itertuples():
            B.add(f"RES-THM-LEX-{slug(lab)}-{r.year}", S, sub, f"{lab}: lexicon mention share among critical records, {r.year}",
                  share_val(r.pct, r.lo, r.hi, r.k, r.n), r.pct, r.lo, r.hi, r.k, r.n, ci_method=BOOT,
                  source="outputs/B6/B6_lexicon_annual.csv")
        q = lt.loc[lx]
        txt, rho = parse_rho(q["Spearman ρ (exact P)"])
        B.add(f"RES-THM-LEX-{slug(lab)}-RHO", S, sub, f"{lab}: lexicon Spearman ρ (exact P)", txt, rho,
              ci_method="exact permutation", source="outputs/B6/B6_lexicon_trends.csv")
        o, lo, hi, pt_ = parse_or(q["OR/yr (95% CI), P"])
        B.add(f"RES-THM-LEX-{slug(lab)}-OR", S, sub, f"{lab}: lexicon OR per year",
              f"OR {o:.3f} per year ({ci(lo, hi, 3, unit='')}), {pt_}", o, lo, hi, ci_method="Wald",
              source="outputs/B6/B6_lexicon_trends.csv")
        B.add(f"RES-THM-LEX-{slug(lab)}-DIR", S, sub, f"{lab}: lexicon and LLM trends in the same direction",
              q["same direction"], source="outputs/B6/B6_lexicon_trends.csv")
        B.add(f"RES-THM-LLM-{slug(lab)}", S, sub, f"{lab}: LLM prevalence share series", f"see RES-TMP-TH-{slug(lab)}-2021 to -OR",
              source=SRC_T4)
    tc = pd.read_csv(OUT / "T4_theme_counts.csv")
    for r in tc[(tc.theme == "Governance / regulation") & (tc.year <= 2025)].itertuples():
        B.add(f"RES-THM-REGCOUNT-{r.year}", S, sub, f"Regulation-themed critical records, annual count, {r.year}",
              f"{r.n_papers} of {r.n_critical} critical records", r.n_papers, k=r.n_papers, n=r.n_critical,
              source="outputs/T4_theme_counts.csv")

    # 5.4 specialty
    sub = "4. Specialty"
    sp = pd.read_csv(DATA / "specialty_2021_2025.csv")
    amp_sp = amp[amp.variable == "specialty"].set_index("level")
    for r in sp.sort_values("point", ascending=False).itertuples():
        B.add(f"RES-SPC-OBS-{slug(r.specialty)}", S, sub, f"{r.specialty}: observed critical rate",
              share_val(r.point, r.lo, r.hi, r.k, r.n), r.point, r.lo, r.hi, r.k, r.n, ci_method=BOOT + " (joint resample)",
              source="final/data/specialty_2021_2025.csv")
        a = amp_sp.loc[r.specialty]
        B.add(f"RES-SPC-AMP-{slug(r.specialty)}", S, sub, f"{r.specialty}: adjusted average marginal probability (B4)",
              f"{a['AMP_%']:.1f}% ({ci(a.lo, a.hi)})", a["AMP_%"], a.lo, a.hi, ci_method="delta method on the logit scale, cluster-robust",
              source="outputs/B4/B4_primary_critical_AMP.csv")
        B.add(f"RES-SPC-FDA-{slug(r.specialty)}", S, sub, f"{r.specialty}: FDA cleared AI/ML devices (mapped panels)",
              f"{r.fda_devices}" + (" (structural zero)" if r.structural_zero else ""), r.fda_devices,
              window="FDA list 1995-2025", source="final/data/specialty_2021_2025.csv (load_fda_device_counts)")
    hi_, lo_ = sp.sort_values("point").iloc[-1], sp.sort_values("point").iloc[0]
    B.add("RES-SPC-RANGE", S, sub, "Observed critical-rate range across the 18 categories",
          f"{hi_.specialty} {hi_.point:.1f}% ({nN(hi_.k, hi_.n)}) to {lo_.specialty} {lo_.point:.1f}% ({nN(lo_.k, lo_.n)})",
          source="final/data/specialty_2021_2025.csv")
    fr = pd.read_csv(DATA / "fda_robustness.csv")
    ids = ["RES-SPC-FDA-RHO18", "RES-SPC-GEN-RHO", "RES-SPC-FDAGEN-RHO", "RES-SPC-FDA-PARTIAL", "RES-SPC-FDA-RHO11", "RES-SPC-EVAL-RHO"]
    for id_, r in zip(ids, fr.itertuples()):
        extra = ""
        if not pd.isna(r.p_one):
            extra = f"; one-sided {p_txt(r.p_one)}; permutation one-sided {p_txt(r.p_perm_one)}"
        B.add(id_, S, sub, f"{r.relationship} (n={r.n})", f"ρ={r.rho:+.2f} (two-sided {p_txt(r.p_two)}{extra})", r.rho, p=r.p_two,
              n=r.n, ci_method="Spearman; permutation = 10,000 pairing permutations, seed 42", source="final/data/fda_robustness.csv")
    B.add("RES-SPC-FDA-LABEL", S, sub, "Status of the FDA association", "exploratory ecological association (18 category-level units)",
          source="Batch 2c brief, decision D4b")

    # 5.5 geography
    sub = "5. Geography"
    ct = pd.read_csv(DATA / "country_2021_2025.csv")
    B.add("RES-GEO-NCTY50", S, sub, "Countries with >= 50 first-author records", str(int((ct.set == ">=50").sum())),
          int((ct.set == ">=50").sum()), source="final/data/country_2021_2025.csv")
    B.add("RES-GEO-NCTY20", S, sub, "Countries with >= 20 first-author records", str(len(ct)), len(ct), source="final/data/country_2021_2025.csv")
    for r in ct.itertuples():
        B.add(f"RES-GEO-CTY-{slug(r.country)}", S, sub, f"{r.country}: critical rate (n {r.set})", share_val(r.point, r.lo, r.hi, r.k, r.n),
              r.point, r.lo, r.hi, r.k, r.n, ci_method=BOOT + " (within country)", source="final/data/country_2021_2025.csv")
    rg = pd.read_csv(DATA / "region_2021_2025.csv")
    amp_rg = amp[amp.variable == "region"].set_index("level")
    orr = b4[b4.variable == "region"].set_index("level")
    for r in rg.itertuples():
        B.add(f"RES-GEO-REG-{slug(r.region)}", S, sub, f"{r.region}: critical rate (corrected n)", share_val(r.point, r.lo, r.hi, r.k, r.n),
              r.point, r.lo, r.hi, r.k, r.n, ci_method=BOOT + " (joint resample)", source="final/data/region_2021_2025.csv")
        a = amp_rg.loc[r.region]
        B.add(f"RES-GEO-AMP-{slug(r.region)}", S, sub, f"{r.region}: adjusted average marginal probability (B4)",
              f"{a['AMP_%']:.1f}% ({ci(a.lo, a.hi)})", a["AMP_%"], a.lo, a.hi, ci_method="delta method, cluster-robust",
              source="outputs/B4/B4_primary_critical_AMP.csv")
        if r.region in orr.index:
            o = orr.loc[r.region]
            B.add(f"RES-GEO-AOR-{slug(r.region)}", S, sub, f"{r.region} vs North America: adjusted OR (B4)",
                  or_ci(o.OR_adj, o.lo_adj, o.hi_adj, 2, o.P_adj), o.OR_adj, o.lo_adj, o.hi_adj, p=o.P_adj,
                  ci_method="Wald, cluster-robust by journal", source="outputs/B4/B4_primary_critical_ORs.csv")
    cn = sens[(sens.model == "S4 country instead of region") & (sens.level == "China")].iloc[0]
    B.add("RES-GEO-USCN-AOR", S, sub, "United States vs China: adjusted OR (B4 S4, country levels with >= 100 records)",
          or_ci(1 / cn.OR, 1 / cn.hi, 1 / cn.lo, 2, cn.P), 1 / cn.OR, 1 / cn.hi, 1 / cn.lo, p=cn.P,
          ci_method="Wald, cluster-robust; inverse of the China vs United States OR", source="outputs/B4/B4_sensitivity_ORs.csv")
    ea = pd.read_csv(DATA / "ea_vs_nawe_within_specialty.csv")
    for r in ea.itertuples():
        B.add(f"RES-GEO-EAWS-{slug(r.specialty)}", S, sub, f"{r.specialty}: East Asia vs North America + Western Europe",
              f"East Asia {r.ea_pct:.1f}% ({nN(r.k_ea, r.n_ea)}; {ci(r.ea_lo, r.ea_hi)}) vs {r.nawe_pct:.1f}% "
              f"({nN(r.k_nawe, r.n_nawe)}; {ci(r.nawe_lo, r.nawe_hi)}); difference {r.delta_pp:+.1f} percentage points",
              r.delta_pp, ci_method=BOOT + " (within group)", source="final/data/ea_vs_nawe_within_specialty.csv")
    rw = json.loads((DATA / "ea_reweighting.json").read_text())
    B.add("RES-GEO-EARW", S, sub, "East Asia critical rate reweighted to the North America + Western Europe specialty mix",
          f"{rw['ea_raw']:.1f}% raw to {rw['ea_reweighted']:.1f}% reweighted, vs {rw['nawe_raw']:.1f}% (share of gap closed "
          f"{(rw['ea_reweighted']-rw['ea_raw'])/(rw['nawe_raw']-rw['ea_raw'])*100:.0f}%)", rw["ea_reweighted"],
          source="final/data/ea_reweighting.json (run_east_asia_diagnose.py logic)")

    # 5.6 publication format
    sub = "6. Publication format"
    pt = pd.read_csv(DATA / "pubtype_stance.csv")
    amp_pt = amp[amp.variable == "pubtype"].set_index("level"); or_pt = b4[b4.variable == "pubtype"].set_index("level")
    for p_ in ["Research Article", "Review", "Letter", "Editorial", "Commentary"]:
        for o in rc.STANCES + ["Critical", "Favourable"]:
            r = pt[(pt.pubtype == p_) & (pt.outcome == o)].iloc[0]
            B.add(f"RES-FMT-{slug(p_)}-{slug(o)}", S, sub, f"{p_}: {o}", share_val(r.point, r.lo, r.hi, r.k, r.n), r.point, r.lo, r.hi,
                  r.k, r.n, ci_method=BOOT + " (within type)", source="final/data/pubtype_stance.csv")
        a = amp_pt.loc[p_]
        B.add(f"RES-FMT-{slug(p_)}-AMP", S, sub, f"{p_}: adjusted average marginal probability of critical stance (B4)",
              f"{a['AMP_%']:.1f}% ({ci(a.lo, a.hi)})", a["AMP_%"], a.lo, a.hi, ci_method="delta method, cluster-robust",
              source="outputs/B4/B4_primary_critical_AMP.csv")
        if p_ in or_pt.index:
            o = or_pt.loc[p_]
            B.add(f"RES-FMT-{slug(p_)}-AOR", S, sub, f"{p_} vs Research Article: adjusted OR for critical stance (B4)",
                  or_ci(o.OR_adj, o.lo_adj, o.hi_adj, 2, o.P_adj), o.OR_adj, o.lo_adj, o.hi_adj, p=o.P_adj,
                  ci_method="Wald, cluster-robust", source="outputs/B4/B4_primary_critical_ORs.csv")
    op = T5[(T5.window == W5) & (T5.analysis == "Pub type: opinion pooled (Comm+Letter+Ed)")].iloc[0]
    B.add("RES-FMT-OPINION-CRIT", S, sub, "Opinion formats pooled (Commentary, Letter, Editorial): critical",
          share_val(op.value, op.lo, op.hi, int(op.k), int(op.n)), op.value, op.lo, op.hi, int(op.k), int(op.n), ci_method=BOOT,
          source="outputs/T5_crosssectional_both_windows.csv")
    x = T5[(T5.window == W5) & (T5.analysis == "Opinion vs Research Article stance")].set_index("metric")
    B.add("RES-FMT-CHISQ", S, sub, "Opinion formats vs Research Articles, five-category stance distribution",
          f"χ²={x.loc['chi2','value']:.1f}, df={int(x.loc['df','value'])}, {p_txt(x.loc['P','value'])}, Cramér V={x.loc['V','value']:.3f}; "
          f"N={fn(x.loc['chi2','n'])}", x.loc["chi2", "value"], n=x.loc["chi2", "n"], p=x.loc["P", "value"],
          ci_method="χ² test of independence", source="outputs/T5_crosssectional_both_windows.csv")
    rs = pd.read_csv(DATA / "review_subtypes.csv")
    for r in rs.itertuples():
        B.add(f"RES-FMT-RSUB-{slug(r.subtype)}-{slug(r.outcome)}", S, sub, f"{r.subtype}: {r.outcome}",
              share_val(r.point, r.lo, r.hi, r.k, r.n), r.point, r.lo, r.hi, r.k, r.n, ci_method=BOOT + " (within subtype)",
              source="final/data/review_subtypes.csv")
    B.add("RES-FMT-RSUB-RULE", S, sub, "Review subtype rule",
          "PubMed Publication Type substring precedence (analysis/robustness.py::simplify_pubtype_7): Editorial > Letter > "
          "Systematic Review > Review > Comment > News > Research Article. 'Systematic Review' tag = systematic subtype; any "
          "other 'Review' tag (including Scoping Review) = narrative subtype; Meta-Analysis has no rule of its own.",
          source="outputs/T8_review_subtype.md")
    tf = pd.read_csv(DATA / "theme_by_format.csv")
    for r in tf.itertuples():
        B.add(f"RES-FMT-THEME-{slug(r.theme)}", S, sub, f"{r.theme} among critical records: Reviews vs Research Articles",
              f"Reviews {r.rev_pct:.1f}% ({nN(r.rev_k, r.rev_n)}; {ci(r.rev_lo, r.rev_hi)}) vs Research Articles {r.res_pct:.1f}% "
              f"({nN(r.res_k, r.res_n)}; {ci(r.res_lo, r.res_hi)}); difference {r.delta_pp:+.1f} percentage points", r.delta_pp,
              ci_method=BOOT + " (within format)", source="final/data/theme_by_format.csv")

    # 5.7 Advocacy by specialty
    sub = "7. Advocacy by specialty, 2021 vs 2025"
    ad = pd.read_csv(DATA / "advocacy_by_specialty.csv")
    for y in (2021, 2025):
        tot = int(ad[ad.year == y].advocacy_total.iloc[0])
        B.add(f"RES-ADVSP-TOTAL-{y}", S, sub, f"Advocacy records, {y}", str(tot), tot, source="final/data/advocacy_by_specialty.csv")
    for s in ad.specialty.unique():
        a, b = ad[(ad.year == 2021) & (ad.specialty == s)].iloc[0], ad[(ad.year == 2025) & (ad.specialty == s)].iloc[0]
        B.add(f"RES-ADVSP-{slug(s)}", S, sub, f"{s}: Advocacy records (share of all Advocacy; rate within specialty)",
              f"2021: {a.advocacy_k} ({a.share_of_advocacy_pct:.1f}% of {a.advocacy_total}; {a.advocacy_rate_in_specialty_pct:.1f}% of "
              f"{a.records_in_specialty}); 2025: {b.advocacy_k} ({b.share_of_advocacy_pct:.1f}% of {b.advocacy_total}; "
              f"{b.advocacy_rate_in_specialty_pct:.1f}% of {b.records_in_specialty})", source="final/data/advocacy_by_specialty.csv")

    # 5.8 sensitivity analyses
    sub = "8. Sensitivity analyses"
    b2md = (OUT / "B2/B2_analysis.md").read_text()
    m = re.search(r"Recovered frame: ([0-9,]+) records.*?FAILED after one resubmission: (\d+)\. With a valid stance and dated "
                  r"2021–2025: ([0-9,]+)\. Corpus \(d\) drops ([0-9,]+)", b2md)
    fr, fl, rec, drop = (int(x.replace(",", "")) for x in m.groups())
    B.add("RES-SEN-B2-FRAME", S, sub, "B2 recovered frame: production application, full-abstract discourse or evaluative (all years)",
          fn(fr), fr, source="outputs/B2/B2_analysis.md", window="all years")
    B.add("RES-SEN-B2-FAILED", S, sub, "B2 recovered records with stance FAILED after one resubmission", str(fl), fl,
          source="outputs/B2/B2_analysis.md", window="all years")
    B.add("RES-SEN-B2-RECOVERED", S, sub, "B2 recovered records with a valid stance, dated 2021-2025 (added in corpus b)", fn(rec), rec,
          source="outputs/B2/B2_analysis.md")
    B.add("RES-SEN-B2-DROPPED", S, sub, "B2 corpus d: production records 2021-2025 dropped because the full-abstract label is application",
          fn(drop), drop, source="outputs/B2/B2_analysis.md")
    mv = pd.read_csv(OUT / "B2/B2_trend_movement.csv")
    for r in mv.itertuples():
        code = r.corpus[1]
        o, lo, hi, pt_ = parse_or(r._7)
        txt, rho = parse_rho(r._6)
        B.add(f"RES-SEN-B2{code.upper()}-{slug(r.outcome)}", S, sub, f"B2 corpus {r.corpus}: {r.outcome}",
              f"{r._3:.1f}% (2021) to {r._4:.1f}% (2025); {txt}; OR {o:.3f} per year ({ci(lo, hi, 3, unit='')}), {pt_}",
              o, lo, hi, ci_method="Wald (frequency-weighted GLM with HC0 SEs for corpus c)", source="outputs/B2/B2_trend_movement.csv")
    cons = pd.read_csv(OUT / "B3/B3_consistency.csv")
    for st in ("Advocacy", "Cautious Optimism"):
        r = cons[(cons["production stance"] == st) & (cons.period == "2021–2025")].iloc[0]
        k, n = map(int, r["flag yes"].split("/"))
        lo, hi = map(float, r["exact 95% CI"].split("–"))
        B.add(f"RES-SEN-B3-CONS-{slug(st)}", S, sub, f"B3: production {st} records flagged strong endorsement, 2021-2025",
              f"{float(r['%']):.1f}% ({nN(k, n)}; {ci(lo, hi)})", float(r["%"]), lo, hi, k, n, ci_method="Clopper-Pearson",
              source="outputs/B3/B3_consistency.csv")
    cp_ = pd.read_csv(OUT / "B3/B3_corrected_prevalence.csv")
    for r in cp_.itertuples():
        m = re.match(r"([0-9.]+) \(([0-9.]+)–([0-9.]+)\)", r._2)
        B.add(f"RES-SEN-B3-CORR-{r.year}", S, sub, f"B3: misclassification-corrected human-Advocacy prevalence, {r.year}",
              f"{float(m[1]):.2f}% ({ci(float(m[2]), float(m[3]), 2)})", float(m[1]), float(m[2]), float(m[3]),
              ci_method="stratified bootstrap (validation within strata x corpus), 1000, seed 42", source="outputs/B3/B3_corrected_prevalence.csv")
    b5 = pd.read_csv(OUT / "B5/B5_long.csv")
    for d, code in (("D1 Medicine area (primary)", "D1"), ("D2 D1 minus Medicine (misc.)", "D2"), ("D3 broad health sciences", "D3")):
        x = b5[b5.definition == d]
        for r in x[x.section.isin(["Trend 2021–2025", "Theme trend 2021–2025 (among critical)"])].itertuples():
            B.add(f"RES-SEN-B5{code}-{slug(r.item)}", S, sub, f"B5 {d}: {r.item} trend", jmirize(r.value),
                  source="outputs/B5/B5_long.csv")
        for r in x[x.section == "Specialty, 2021–2025"].itertuples():
            B.add(f"RES-SEN-B5{code}-SPC-{slug(r.item)}", S, sub, f"B5 {d}: specialty {r.item}", jmirize(r.value),
                  source="outputs/B5/B5_long.csv")
        for it in ("East Asia", "North America"):
            r = x[(x.section == "Region, 2021–2025") & (x.item == it)].iloc[0]
            B.add(f"RES-SEN-B5{code}-REG-{slug(it)}", S, sub, f"B5 {d}: {it} critical", jmirize(r.value), source="outputs/B5/B5_long.csv")
        for it in ("Review", "Research Article"):
            r = x[(x.section == "Publication type, 2021–2025") & (x.item == it)].iloc[0]
            B.add(f"RES-SEN-B5{code}-PT-{slug(it)}", S, sub, f"B5 {d}: {it} critical", jmirize(r.value), source="outputs/B5/B5_long.csv")
        rem = (OUT / "B5/B5_sjr_sensitivity.md").read_text()
        m = re.search(rf"\| {re.escape(d)} \| (\d+) \| (\d+) \| (\d+) \| (\d+) \| (\d+) \| (\d+) \| (\d+) \|", rem)
        removed = sum(int(g) for g in m.groups()[:5])
        B.add(f"RES-SEN-B5{code}-REMOVED", S, sub, f"B5 {d}: records removed, 2021-2025", f"{fn(removed)} of 14,058",
              removed, n=14058, source="outputs/B5/B5_sjr_sensitivity.md")
    for model, code in (("S3 journal fixed effects", "S3"), ("S4 country instead of region", "S4")):
        r = sens[(sens.model == model) & (sens.term == "year_c")].iloc[0]
        B.add(f"RES-SEN-B4{code}-YEAR", S, sub, f"B4 {model}: critical OR per year", or_val(r.OR, r.lo, r.hi, r.P), r.OR, r.lo, r.hi,
              p=r.P, ci_method="Wald, cluster-robust" if code == "S4" else "Wald, cluster-robust; journals with >= 10 records and outcome variation",
              source="outputs/B4/B4_sensitivity_ORs.csv")
    for rr in sens[(sens.model == "S2 with Jan–Apr 2026") & (sens.variable == "year")].itertuples():
        B.add(f"RES-SEN-B4S2-{int(float(rr.level))}", S, sub, f"B4 S2 (adds January-April 2026): critical OR, {int(float(rr.level))} vs 2021",
              or_ci(rr.OR, rr.lo, rr.hi, 2, rr.P), rr.OR, rr.lo, rr.hi, p=rr.P, window="2021-April 2026",
              source="outputs/B4/B4_sensitivity_ORs.csv")
    B.add("RES-SEN-B4S3-N", S, sub, "B4 S3 sample", "n=8529 records, 2728 events, 275 journals", 8529, source="outputs/B4/B4_regression.md")
    B.add("RES-SEN-B4-PO", S, sub, "B4 ordinal model: proportional-odds assumption",
          "fails for 27 of 32 terms (pre-specified rule), mainly at the Advocacy cut point", source="outputs/B4/B4_regression.md")

    # 5.9 forward validation
    sub = "9. Forward-validation (Multimedia Appendix 2; unchanged)"
    fv = json.loads((DATA / "fv_counts.json").read_text())
    tv = pd.read_csv(DATA / "fv_tier_verdict.csv", index_col=0)
    B.add("RES-FV-CAND", S, sub, "Advocacy records 2021-2023 with a predictive-claim flag", str(fv["candidates"]), fv["candidates"],
          window="2021-2023 claims; 2024-April 2026 evidence", source="output/analyses/prophecy/prophecy_panel_candidates_2021_2023.csv")
    B.add("RES-FV-FP", S, sub, "False positives removed by blind human review", str(fv["candidates"] - fv["frozen_papers"]),
          fv["candidates"] - fv["frozen_papers"], window="2021-2023 claims", source="output/analyses/prophecy/phase1_signature_claims_FROZEN.csv")
    B.add("RES-FV-PREC", S, sub, "Post-hoc flag precision", f"{fv['frozen_papers']/fv['candidates']:.2f} ({fv['frozen_papers']}/{fv['candidates']})",
          fv["frozen_papers"] / fv["candidates"], window="2021-2023 claims", source="output/analyses/prophecy/")
    B.add("RES-FV-SET", S, sub, "Frozen set", f"{fv['frozen_papers']} papers, {fv['claims']} claims (Tier 1 {fv['tier_counts']['1']}; "
          f"Tier 2 {fv['tier_counts']['2']}; Tier 3 {fv['tier_counts']['3']})", fv["claims"], window="2021-2023 claims",
          source="output/analyses/prophecy/phase2_prophecy_verdicts_worksheet.xlsx")
    for v_, lab in (("borne_out", "borne out"), ("partially", "partially borne out"), ("not_borne_out", "not borne out"),
                    ("too_early_unfalsifiable", "too early/unfalsifiable")):
        k = fv["verdicts"][v_]
        B.add(f"RES-FV-{slug(v_)}", S, sub, f"Claims {lab}", f"{k}/78 ({k/78*100:.1f}%)", k, k=k, n=78,
              window="evidence 2024-April 2026", source="output/analyses/prophecy/phase2_prophecy_verdicts_worksheet.xlsx")
    for t in ("1", "2", "3"):
        r = tv.loc[int(t)] if int(t) in tv.index else tv.loc[t]
        B.add(f"RES-FV-TIER{t}", S, sub, f"Tier {t} verdicts", f"borne out {r.borne_out}; partially {r.partially}; not borne out "
              f"{r.not_borne_out}; too early/unfalsifiable {r.too_early_unfalsifiable} (n={r.Total})", int(r.Total),
              window="evidence 2024-April 2026", source="final/data/fv_tier_verdict.csv")

    # 5.10 2026 descriptive
    sub = "10. January-April 2026 (descriptive only; no trend statistics)"
    d26 = pd.read_csv(OUT / "T4_2026_descriptive.csv")
    d26 = d26[d26.domain == "Stance"]
    for r in d26.itertuples():
        B.add(f"RES-2026-{slug(r.outcome)}", S, sub, f"{r.outcome}, January-April 2026", share_val(r.pct_2026, r.lo, r.hi, r.k, r.N),
              r.pct_2026, r.lo, r.hi, r.k, r.N, ci_method=BOOT + " (2026 records only)", window="January-April 2026",
              source="outputs/T4_2026_descriptive.csv")


# =====================================================================
# 5b. Multivariable regression in full (Table 2; MA3 regression_full)
# =====================================================================
def parse_term(t):
    if t == "year_c":
        return "year", "per 1 year"
    m = re.match(r"C\((\w+), Treatment\(reference=.*?\)\)\[T\.(.*)\]", t)
    return m[1], m[2]


REF = {"genre": "discourse", "pubtype": "Research Article", "specialty": "Medical Informatics / Digital Health",
       "region": "North America"}


def regression():
    S = "Results, 2021-2025"
    sub = "11. Multivariable logistic regression, critical stance (B4 primary; Table 2)"
    SRC = "outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv"
    B.add("RES-REG-HEADER", S, sub, "Model", "Logistic regression of critical stance (Alarm or Caution) on publication year "
          "(continuous, centred on 2023.856), genre, publication type, specialty and first-author region; n=14,058; "
          "events=4283; 2278 journal clusters; cluster-robust (journal) SEs", source="outputs/B4/B4_regression.md")
    b4 = pd.read_csv(OUT / "B4/B4_primary_critical_ORs.csv")
    amp = pd.read_csv(OUT / "B4/B4_primary_critical_AMP.csv")
    yr = b4[b4.term == "year_c"].iloc[0]
    B.add("RES-REG-YEAR-UOR", S, sub, "Year (per 1 year): unadjusted OR", or_ci(yr.OR_unadj, yr.lo_unadj, yr.hi_unadj, 3, yr.P_unadj),
          yr.OR_unadj, yr.lo_unadj, yr.hi_unadj, p=yr.P_unadj, ci_method="Wald, cluster-robust", source=SRC)
    for var in ("genre", "pubtype", "specialty", "region"):
        for r in amp[amp.variable == var].itertuples():
            lvl = r.level
            tag = f"RES-REG-{var.upper()}-{slug(lvl)}"
            B.add(f"{tag}-N", S, sub, f"{var}: {lvl}: records", fn(r.n_records_at_level), r.n_records_at_level, source=SRC)
            if lvl == REF[var]:
                B.add(f"{tag}-AOR", S, sub, f"{var}: {lvl}: adjusted OR", "1 (reference)", 1.0, source=SRC)
                B.add(f"{tag}-UOR", S, sub, f"{var}: {lvl}: unadjusted OR", "1 (reference)", 1.0, source=SRC)
            else:
                o = b4[(b4.variable == var) & (b4.level == lvl)].iloc[0]
                B.add(f"{tag}-AOR", S, sub, f"{var}: {lvl}: adjusted OR", or_ci(o.OR_adj, o.lo_adj, o.hi_adj, 2, o.P_adj),
                      o.OR_adj, o.lo_adj, o.hi_adj, p=o.P_adj, ci_method="Wald, cluster-robust", source=SRC)
                B.add(f"{tag}-UOR", S, sub, f"{var}: {lvl}: unadjusted OR", or_ci(o.OR_unadj, o.lo_unadj, o.hi_unadj, 2, o.P_unadj),
                      o.OR_unadj, o.lo_unadj, o.hi_unadj, p=o.P_unadj, ci_method="Wald, cluster-robust", source=SRC)
            B.add(f"{tag}-AMP", S, sub, f"{var}: {lvl}: adjusted average marginal probability",
                  f"{r._4:.1f}% ({ci(r.lo, r.hi)})", r._4, r.lo, r.hi, ci_method="delta method on the logit scale, cluster-robust",
                  source=SRC)

    sub = "12. Advocacy model (B4 secondary 2)"
    adv = pd.read_csv(OUT / "B4/B4_advocacy_ORs.csv")
    B.add("RES-REGADV-HEADER", S, sub, "Model", "Logistic regression of Advocacy vs not; n=14,058; events=218; 2278 journal clusters; "
          "levels with fewer than 5 Advocacy events collapsed into 'Other (<5 events)'", source="outputs/B4/B4_regression.md")
    for r in adv.itertuples():
        var, lvl = parse_term(r.term)
        B.add(f"RES-REGADV-{var.upper()}-{slug(lvl)}", S, sub, f"{var}: {lvl}: adjusted OR", or_ci(r.OR, r.lo, r.hi, 2, r.P),
              r.OR, r.lo, r.hi, p=r.P, ci_method="Wald, cluster-robust", source="outputs/B4/B4_advocacy_ORs.csv")

    sub = "13. Ordinal model (B4 secondary 1)"
    od = pd.read_csv(OUT / "B4/B4_ordinal_and_cutpoints.csv")
    B.add("RES-REGORD-HEADER", S, sub, "Model", "Proportional-odds logistic model (Alarm < Caution < Neutral < Cautious Optimism < "
          "Advocacy); OR > 1 = more favourable; n=14,058; cluster-robust SEs; cut-point ORs from separate binary models",
          source="outputs/B4/B4_regression.md")
    for r in od.itertuples():
        var, lvl = parse_term(r.term)
        cuts = "; ".join(f">{c} {np.exp(getattr(r, f'b_gt_{c.replace(' ', '_')}') if hasattr(r, f'b_gt_{c.replace(' ', '_')}') else np.nan):.2f}"
                         for c in ("Alarm", "Caution", "Neutral"))
        co = od.loc[r.Index, "b_gt_Cautious Optimism"]
        B.add(f"RES-REGORD-{var.upper()}-{slug(lvl)}", S, sub, f"{var}: {lvl}: ordinal OR; cut-point ORs; proportional-odds check",
              f"{or_ci(np.exp(r.beta), np.exp(r.lo), np.exp(r.hi), 2, r.P)}; cut-point ORs {cuts}; >Cautious Optimism "
              f"{np.exp(co):.2f}; check: {r.PO_check if isinstance(r.PO_check, str) and r.PO_check else 'holds'}",
              np.exp(r.beta), np.exp(r.lo), np.exp(r.hi), p=r.P, ci_method="Wald, cluster-robust", source="outputs/B4/B4_ordinal_and_cutpoints.csv")

    sub = "14. Sensitivity models S1-S4 (B4)"
    sens = pd.read_csv(OUT / "B4/B4_sensitivity_ORs.csv")
    code = {"S1 year categorical": "S1", "S2 with Jan–Apr 2026": "S2", "S3 journal fixed effects": "S3",
            "S4 country instead of region": "S4"}
    for r in sens.itertuples():
        var, lvl = parse_term(r.term)
        id_ = f"RES-REGSEN-{code[r.model]}-{var.upper()}-{slug(str(lvl))}"
        B.add(id_, S, sub, f"{r.model}: {var}: {lvl}: adjusted OR", or_ci(r.OR, r.lo, r.hi, 3 if var == 'year' else 2, r.P),
              r.OR, r.lo, r.hi, p=r.P, window="2021-April 2026" if code[r.model] == "S2" else "2021-2025",
              ci_method="Wald, cluster-robust", source="outputs/B4/B4_sensitivity_ORs.csv")


# =====================================================================
# 5c. Inputs for the Multimedia Appendix 3 units
# =====================================================================
def cell(id_, S, sub, item, k, n, pt, lo, hi, src, d=1, window="2021-2025", method=BOOT):
    B.add(id_, S, sub, item, share_val(pt, lo, hi, k, n, d), pt, lo, hi, int(k), int(n), ci_method=method, window=window, source=src)


def ma_extras():
    S = "Results, 2021-2025"
    sub = "15. Stance trend under the stricter v2 rubric (Table S1 v2 column)"
    for r in pd.read_csv(DATA / "v2_trend.csv").itertuples():
        B.add(f"RES-V2-{slug(r.stance)}", S, sub, f"{r.stance}: v2 rubric 2021 and 2025 shares; Spearman ρ (exact P)",
              f"{r.v2_2021:.1f}% to {r.v2_2025:.1f}%; ρ={r.rho:+.2f} ({p_txt(r.P_exact)})", r.rho, p=r.P_exact,
              ci_method="exact permutation over 5 annual values", source="final/data/v2_trend.csv (output/analyses/temporal_stance_v2.csv)")
    sub = "16. Pooled theme prevalence among critical records (Table S5)"
    for r in pd.read_csv(DATA / "theme_pooled.csv").itertuples():
        cell(f"RES-THM-POOLED-{slug(r.theme)}", S, sub, f"{r.theme}: pooled prevalence 2021-2025", r.k, r.n, r.point, r.lo, r.hi,
             "final/data/theme_pooled.csv")
    sub = "17. Q3 comparison arm, pooled 2021-2025 (Table S14)"
    for r in pd.read_csv(DATA / "q3_pooled.csv").itertuples():
        cell(f"RES-Q3-POOLED-{slug(r.stance)}", S, sub, f"Q3 arm: {r.stance}", r.k, r.n, r.point, r.lo, r.hi, "final/data/q3_pooled.csv")
    sub = "18. B5 annual series by corpus definition"
    for r in pd.read_csv(DATA / "b5_annual.csv").itertuples():
        code = r.definition.split(" ")[0] if r.definition.startswith("D") else "FULL"
        cell(f"RES-B5ANN-{code}-{slug(r.outcome)}-{r.year}", S, sub, f"{r.definition}: {r.outcome}, {r.year}", r.k, r.n, r.point,
             r.lo, r.hi, "final/data/b5_annual.csv")
    sub = "19. B5 detail, 2021-2025 (Table S sjr_sensitivity)"
    b5 = pd.read_csv(OUT / "B5/B5_long.csv")
    for r in b5[b5.section.str.contains("2021–2025")].itertuples():
        code = r.definition.split(" ")[0] if r.definition.startswith("D") else "FULL"
        B.add(f"RES-B5X-{code}-{slug(r.section)[:10]}-{slug(r.item)}", S, sub, f"{r.definition}: {r.section}: {r.item}",
              jmirize(r.value), source="outputs/B5/B5_long.csv")
    sub = "20. B2 recovered vs retained records, and annual series by corpus"
    for r in pd.read_csv(DATA / "b2_recovered_vs_retained.csv").itertuples():
        cell(f"RES-B2RR-{slug(r.set)[:8]}-{slug(r.stance)}", S, sub, f"{r.set}: {r.stance}", r.k, r.n, r.point, r.lo, r.hi,
             "final/data/b2_recovered_vs_retained.csv")
    ba = pd.read_csv(OUT / "B2/B2_annual_by_corpus.csv")
    for r in ba[ba.category.isin(["Critical", "Advocacy"])].itertuples():
        code = r.corpus[1].upper()
        if code == "C":
            B.add(f"RES-B2ANN-{code}-{slug(r.category)}-{r.year}", S, sub, f"B2 corpus {r.corpus}: {r.category}, {r.year}",
                  f"{r.pct:.1f}% (weighted {r.k_weighted:.1f}/{r.N_weighted:.1f}; {ci(r.lo, r.hi)})", r.pct, r.lo, r.hi,
                  ci_method=BOOT, source="outputs/B2/B2_annual_by_corpus.csv")
        else:
            cell(f"RES-B2ANN-{code}-{slug(r.category)}-{r.year}", S, sub, f"B2 corpus {r.corpus}: {r.category}, {r.year}",
                 r.k, r.N, r.pct, r.lo, r.hi, "outputs/B2/B2_annual_by_corpus.csv")
    sub = "21. B3 symmetric scale distribution, 2021-2025"
    sy = pd.read_csv(OUT / "B3/B3_symmetric_scale.csv").set_index("period").loc["2021–2025"]
    for col in [c for c in sy.index if c != "N"]:
        m = re.match(r"([0-9.]+)% \(([0-9,]+)\)", sy[col])
        k = int(m[2].replace(",", ""))
        B.add(f"RES-B3SYM-{slug(col)}", S, sub, f"Symmetric scale 2021-2025: {col}", f"{float(m[1]):.1f}% ({nN(k, int(sy['N']))})",
              float(m[1]), k=k, n=int(sy["N"]), source="outputs/B3/B3_symmetric_scale.csv")
    sub = "22. B6 MeSH and keyword re-fetch; term triangulation"
    comp = pd.read_csv(OUT / "B6/B6_completeness_by_year.csv")
    comp["year"] = pd.to_numeric(comp["year"], errors="coerce")
    for r in comp[comp.year.between(2021, 2025)].itertuples():
        B.add(f"RES-B6-COMP-{int(r.year)}", S, sub, f"Records with MeSH / with author keywords, {int(r.year)}",
              f"MeSH {r._5:.1f}% ({nN(r.with_mesh, r.records)}); keywords {r._6:.1f}% ({nN(r.with_keywords, r.records)})",
              r._5, k=int(r.with_mesh), n=int(r.records), source="outputs/B6/B6_completeness_by_year.csv")
    for f_, tag in (("B6_emerging_terms_top30.csv", "EMERG"), ("B6_stance_terms_top30.csv", "STANCE")):
        t = pd.read_csv(OUT / "B6" / f_)
        for i, r in enumerate(t.itertuples(), 1):
            B.add(f"RES-B6-{tag}-{i:02d}", S, sub, f"{'Emerging (2024-2025 vs 2021-2022)' if tag == 'EMERG' else 'Critical vs favourable'} term {i}: {r.term}",
                  f"z={r.z:.2f}; log-odds difference {r.delta:.2f}; records {int(r.df_group1)} vs {int(r.df_group2)}; {r.direction}",
                  r.z, source=f"outputs/B6/{f_}")

    S = "Results, 2021-2025"
    sub = "23. Theme counts, generative share by specialty, forward-validation corpus silence"
    tc = pd.read_csv(OUT / "T4_theme_counts.csv")
    for r in tc[tc.year <= 2025].itertuples():
        B.add(f"RES-THM-COUNT-{slug(r.theme)}-{r.year}", S, sub, f"{r.theme}: critical records with the theme, {r.year}",
              f"{r.n_papers} of {r.n_critical}", r.n_papers, k=r.n_papers, n=r.n_critical, source="outputs/T4_theme_counts.csv")
    sf = pd.read_csv(DATA / "specialty_fda.csv")
    for r in sf.itertuples():
        B.add(f"RES-SPC-GENSHARE-{slug(r.specialty)}", S, sub, f"{r.specialty}: generative-model share among abstract-present critical records",
              f"{r.generative_share_pct:.1f}% (n={r.n_critical_abstract})", r.generative_share_pct, n=r.n_critical_abstract,
              source="final/data/specialty_fda.csv")
    sil = pd.read_csv(DATA / "fv_tier_silent.csv", index_col=0)
    for t in sil.index:
        B.add(f"RES-FV-SILENT-T{t}", S, sub, f"Tier {t}: claims with corpus silence (classified too early/unfalsifiable)",
              str(int(sil.loc[t].get("true", 0))), int(sil.loc[t].get("true", 0)),
              window="evidence 2024-April 2026", source="final/data/fv_tier_silent.csv")

    S = "Validation (Table 1)"
    sub = "Theme validation per theme; audit sampling manifest"
    for tag, f_ in (("200", "A4_theme_primary_n200/theme_scores.md"), ("187", "A4_theme/theme_scores.md")):
        md = (OUT / f_).read_text()
        for th in rc.THEMES:
            m = re.search(rf"\| {th} \| (\d+) \|([^|]*)\| " + r"\| ".join([r"([0-9.]+) \(([0-9.]+)–([0-9.]+)\) "] * 6), md)
            g_ = m.groups()
            n_pos, flag = int(g_[0]), g_[1].strip()
            vals = [tuple(map(float, g_[2 + 3 * i: 5 + 3 * i])) for i in range(6)]
            names = ["precision (unweighted)", "recall (unweighted)", "F1 (unweighted)", "precision (weighted)", "recall (weighted)", "F1 (weighted)"]
            for (pt, lo, hi), nm in zip(vals, names):
                B.add(f"VAL-TH-PT-{tag}-{slug(th)}-{slug(nm)}", S, sub, f"Theme {th}, N={tag}: {nm}" + (f" [{flag}]" if flag else ""),
                      f"{pt:.3f} ({ci(lo, hi, 3, unit='')})", pt, lo, hi, n=int(tag), ci_method="within-year percentile bootstrap, 1000, seed 42",
                      window="validation sample", source=f"outputs/{f_}")
            B.add(f"VAL-TH-PT-{tag}-{slug(th)}-SUPPORT", S, sub, f"Theme {th}, N={tag}: human-positive records", str(n_pos), n_pos,
                  window="validation sample", source=f"outputs/{f_}")
    man = pd.read_csv(rc.R1 / "coding/prefilter_sampling_manifest.csv")
    for r in man.itertuples():
        B.add(f"VAL-PF-MAN-{r.stratum}-{r.year}", S, sub, f"Audit sampling: {r.stratum} {r.year}: frame and sample",
              f"frame {fn(r.frame_n)}; sampled {r.sample_n}; sampling fraction {r.sampling_fraction*100:.2f}%", r.sample_n,
              k=r.sample_n, n=r.frame_n, window="2021-2025 frame", source="coding/prefilter_sampling_manifest.csv")

    S = "Validation (Table 1)"
    sub = "Confusion matrices and cell-level audit estimates (Multimedia Appendix 3)"
    for tag, f_ in (("225", "stance_confusion_inscope225.csv"), ("300", "stance_confusion_all300.csv")):
        cm = pd.read_csv(DATA / f_, index_col=0)
        for h in cm.index:
            for m_ in cm.columns:
                B.add(f"VAL-ST-CM{tag}-{slug(h)}-{slug(m_)}", S, sub, f"Stance n={tag}: human {h}, model {m_}", str(int(cm.loc[h, m_])),
                      int(cm.loc[h, m_]), window="validation sample", source=f"final/data/{f_}")
        if tag == "225":
            labs = list(cm.index)
            for i, h in enumerate(labs):
                row = cm.loc[h]; n = int(row.sum()); ex = int(row.iloc[i])
                adj = int(sum(row.iloc[j] for j in (i - 1, i + 1) if 0 <= j < len(labs)))
                crit = {"Alarm", "Caution"}; fav = {"Cautious Optimism", "Advocacy"}
                cross = (int(sum(row[c] for c in fav)) if h in crit else int(sum(row[c] for c in crit)) if h in fav else None)
                B.add(f"VAL-ST-S18C-{slug(h)}", S, sub, f"Stance in scope: {h} exact / adjacent / boundary-crossing",
                      f"n={n}; exact {ex} ({ex/n*100:.1f}%); adjacent {adj} ({adj/n*100:.1f}%); boundary-crossing "
                      f"{cross if cross is not None else 'not applicable'}", ex / n * 100, k=ex, n=n, window="validation sample",
                      source="final/data/stance_confusion_inscope225.csv")
    for f_, tag in (("T1_confusion_3x3.csv", "PF3"), ("T3_confusion_failure_mode.csv", "FM"), ("T3_confusion_model_type.csv", "MT")):
        cm = pd.read_csv(OUT / f_, index_col=0)
        for h in cm.index:
            for m_ in cm.columns:
                B.add(f"VAL-CM-{tag}-{slug(str(h))[:10]}-{slug(str(m_))[:10]}", S, sub, f"{f_}: {h} x {m_}", str(int(cm.loc[h, m_])),
                      int(cm.loc[h, m_]), window="validation sample", source=f"outputs/{f_}")
    rr = pd.read_csv(rc.REPO_OUT / "revision_checks/rep1_stability_metrics.csv").iloc[0]
    B.add("VAL-ST-RTR-SHIFT", S, sub, "Run-to-run: labels shifted between the two re-inferences", f"{int(rr.n_labels_shifted)} of 300 "
          "(all adjacent; no shift across the critical-favourable boundary)", int(rr.n_labels_shifted), n=300,
          window="validation sample", source="output/revision_checks/rep1_stability_metrics.csv; Table S15")
    cells = pd.read_csv(OUT / "B1/prefilter_cell_exact_ci.csv")
    for r in cells.itertuples():
        B.add(f"VAL-PF-CELL-{slug(r.variant)}-{r.stratum}-{r.year}-{'FA' if 'full' in r.comparison else 'PR'}", S, sub,
              f"Audit cell ({r.variant}): {r.stratum} {r.year}, {r.comparison}: human KEEP",
              f"{r.proportion*100:.1f}% ({r.human_KEEP}/{r.n}; exact Clopper-Pearson {ci(r.CP_lo*100, r.CP_hi*100)[7:]})",
              r.proportion * 100, r.CP_lo * 100, r.CP_hi * 100, int(r.human_KEEP), int(r.n), ci_method="Clopper-Pearson",
              window="validation sample", source="outputs/B1/prefilter_cell_exact_ci.csv")
    b1 = pd.read_csv(OUT / "B1/prefilter_exact_ci_long.csv")
    for r in b1[b1.variant != "primary"].itertuples():
        if r.estimate_name.startswith(("prod2x2_", "FNrate_pooled", "missed_total", "PPV_RET_pooled", "fullabs_precision")) and \
                not r.estimate_name.endswith(("F1", "accuracy", "PABAK", "prevalence_human")):
            kappa = r.estimate_name.endswith(("kappa", "AC1"))
            mult = 1 if (kappa or r.estimate_name == "missed_total") else 100
            d = 3 if kappa else 0 if r.estimate_name == "missed_total" else 1
            unit = "" if mult == 1 else "%"
            B.add(f"VAL-PF-VAR-{slug(r.variant)}-{slug(r.estimate_name)}", S, sub, f"Audit ({r.variant}): {r.estimate_name}",
                  f"{r.estimate*mult:.{d}f}{unit} ({ci(r.jeffreys_lo*mult, r.jeffreys_hi*mult, d, unit)})", r.estimate * mult,
                  r.jeffreys_lo * mult, r.jeffreys_hi * mult, ci_method="Jeffreys (Amendment 3)", window="2021-2025 frame",
                  source="outputs/B1/prefilter_exact_ci_long.csv")


# =====================================================================
# 6. Superseded numbers
# =====================================================================
SUPERSEDED = [
    # (old as printed, where, new ID or text, reason)
    ("16,749 abstracts; 2021-2026 (title)", "Title", "COR-23 (14,058); 2021-2025", "Analytic corpus is 2021-2025 (decision 1)"),
    ("97,492 eligible Q1/Q2 records", "Abstract; Methods; Results", "COR-16 (86,700)", "Window step 2021-2025 replaces the April 2026 cutoff"),
    ("16,759 retained (8,899 discourse; 7,860 evaluative)", "Abstract; Methods; Results", "COR-19 to COR-21 (14,066; 7637; 6429)", "2021-2025 window"),
    ("16,749 valid labels; 10 unparseable", "Abstract; Methods; Results", "COR-22, COR-23 (8 FAILED; 14,058)", "2021-2025 window"),
    ("16,747 records dated 2021-2026; 2 dated 2020", "Methods; Results; Figure captions", "COR-23 (14,058)", "2021-2025 window; 2020 records fall outside the window"),
    ("5,161 critical records", "Methods; Results", "COR-SUB-01 (4283)", "2021-2025 window"),
    ("5,159 parsed; 4,747 abstract-present critical", "Methods; Results", "COR-SUB-04, COR-SUB-06 (4281; 3906)", "2021-2025 window"),
    ("2,226 hallucination-gated records", "Abstract; Results; Figure 2", "COR-SUB-07 (1775)", "2021-2025 window"),
    ("16,734 records with valid specialty; 13 FAILED", "Results; Figure 3; Table S16", "COR-SUB-08, COR-SUB-09 (14,048; 10)", "2021-2025 window"),
    ("90.3% of records resolved to a country", "Methods", "COR-SUB-10 (12,745/14,058)", "2021-2025 window"),
    ("Q1/Q2 = 88.0% of records", "Methods", "COR-Q1Q2-PCT (88.1%)", "Rounding error (98,626/112,011 = 88.05%; B7 item 5)"),
    ("7,922 unmatched", "Methods", "COR-07 to COR-10 (5092 not in SJR; 1494 no quartile; 1336 Q4)", "Unmatched includes Q4 and no-quartile titles (T7)"),
    ("Cautious Optimism 62.8% (n=10,514); Neutral 5.0% (n=837); Advocacy 1.4% (n=235); critical 30.8% (916 Alarm, 4,245 Caution)", "Abstract; Results", "RES-OVR-*", "2021-2025 window"),
    ("Advocacy 2.9% (2021) to 0.6% (2026), Spearman ρ=-1.00", "Abstract; Results; Discussion", "RES-TMP-ADV-2021, -2025, -RHO, -OR, -AOR", "2026 is no longer a trend point"),
    ("Critical 25.4% (22.9-28.1) to 32.6% (30.9-34.4); +7.25 percentage points", "Abstract; Results; Table S1", "RES-TMP-CRIT-*", "2021-2025 window"),
    ("Alarm 2.7% to 6.8% (2024), 6.2% in 2026; Caution 22.7% to 26.4%; Cautious Optimism 60.2%-65.3%", "Results", "RES-TMP-ALARM-*, -CAUT-*, -CO-*", "2021-2025 window"),
    ("17 Advocacy records in 2026; 5 about drug discovery (Table S2)", "Results; Table S2", "RES-2026-ADVOCACY; RES-ADVSP-*", "2026 is descriptive only; Table S2 replaced by the 2026 descriptive table"),
    ("Discourse 30.2% to 37.8% (ρ=+0.94); evaluative 14.6% to 28.1% (ρ=+0.77); ratio 2.24 to 0.88", "Results; Table S3", "RES-TMP-GENDISC-*, -GENEVAL-*, RES-TMP-GENRATIO-*", "2021-2025 window; deterministic per-cell seeds (B7 item 2)"),
    ("Keep rate ρ=+1.00 (Table S4)", "Results", "RES-TMP-KEEP-*", "2021-2025 window"),
    ("Patient safety +11.0; errors +30.9; regulation -22.0; ethics/bias -8.1 percentage points (36.7% to 28.6%)", "Abstract; Results; Table S5", "RES-TMP-TH-*", "2021-2025 window"),
    ("Factual error 56% to 90% of gated papers; fabrication-involved 0% (2021) to roughly 21-23% from 2023", "Abstract; Results", "RES-TMP-FM-MIS-*, RES-TMP-FAB-GATED-*", "2021-2025 window; values in B7 item 6"),
    ("Generative share 5.3% (2021) to 62.8% (2026), ρ=+0.94; fabrication share 13.8% in 2026; 21.8%, 22.9%, 19.7%, 22.0% among generative (2023-2026)", "Results", "RES-TMP-GENSHARE-*, RES-TMP-FAB-ALL-*, RES-TMP-FAB-GEN-*", "2021-2025 window"),
    ("1,858 records (39.1%) generative without fabrication", "Results", "RES-TMP-MECH-GENNOFAB", "2021-2025 window"),
    ("Specialty range: Mental Health 51.3% (46.8-55.5) to Cardiology 16.8% (14.1-19.8); Informatics 44.9%; Nursing 43.0%; Ophthalmology 18.4%; Oncology 19.7%", "Abstract; Results; Figure 3", "RES-SPC-OBS-*, RES-SPC-RANGE", "2021-2025 window"),
    ("FDA ρ=-0.65 (two-sided P=.004); structural zeros dropped ρ=-0.58 (P=.062, n=11); generative-share ρ=-0.01", "Abstract; Results; Table S6; Figure S5", "RES-SPC-FDA-RHO18, -RHO11, -PARTIAL, RES-SPC-GEN-RHO", "2021-2025 window; labelled exploratory (D4b)"),
    ("United States 34.5% (n=4,222) vs China 16.2% (n=1,904); Netherlands 44.4%; Denmark 42.6%; Australia 42.5%; Ireland 41.1%; United Kingdom 40.6%; Japan 18.3%; Iran 18.0%; South Korea 20.5%; India 20.6%", "Abstract; Results; Table S7", "RES-GEO-CTY-*; RES-GEO-USCN-AOR", "2021-2025 window"),
    ("36 countries with >= 50 records; 45 with >= 20", "Figure 4; Figure S6; Table S7", "RES-GEO-NCTY50, RES-GEO-NCTY20", "2021-2025 window"),
    ("Region n: North America 4,964; Western Europe 4,298; East Asia 3,262 (Table S9)", "Results; Table S9", "RES-GEO-REG-*", "n's printed on 16,759, rates on 16,747 (B7 item 3); now both on 14,058"),
    ("East Asia 18.5% reweighted to 19.9%, closing 8% of the gap; Hong Kong 31.6%; Singapore 26.7%", "Results", "RES-GEO-EARW; RES-GEO-CTY-*", "2021-2025 window"),
    ("Publication type n: Research Articles 10,315; Reviews 5,444; Letters 480; Editorials 404; Commentaries 104", "Results; Table S10", "RES-FMT-*", "2021-2025 window"),
    ("Commentary critical 53.9%", "Results; Table S10", "RES-FMT-COMMENTARY-CRITICAL", "Rounding (56/104 = 53.85%, B7 item 4) and 2021-2025 window"),
    ("Opinion 41.8% vs Research 32.9%; χ²4=430.5, P<.001, Cramér V=0.195 (N=11,303)", "Results; Table S10", "RES-FMT-OPINION-CRIT, RES-FMT-CHISQ", "2021-2025 window"),
    ("Reviews 24.9% critical, 73.1% favourable; systematic 29.3% (n=980) vs narrative 23.9% (n=4,464)", "Abstract; Results; Table S11", "RES-FMT-REVIEW-*, RES-FMT-RSUB-*", "2021-2025 window"),
    ("Table S12 theme-by-format values", "Table S12", "RES-FMT-THEME-*", "2021-2025 window"),
    ("Table S1 P values (.072, .072, .019, .329, .003, .072)", "Table S1", "RES-TMP-*-RHO", "Exact permutation P on 5 annual points (B7 item 1)"),
    ("Prefilter κ 0.51 (95% CI 0.35-0.68)", "Abstract; Methods", "VAL-PF-PILOT-K3 (0.511; 0.345-0.646)", "Original CI code not found; recomputed bootstrap (B7 item 8a)"),
    ("Failure mode κ_max 0.76; model type AC1 0.89", "Methods", "VAL-MX-FM-KMAX (0.755); VAL-MX-MT-AC1 (0.88)", "Double rounding (B7 items 7a-7b)"),
    ("Specialty κ 0.75 (no CI)", "Abstract; Methods", "VAL-SP-K", "CI added (E12)"),
    ("Model type κ 0.84; failure mode κ 0.57 (no CI)", "Abstract; Methods", "VAL-MX-MT-K, VAL-MX-FM-K", "CI added (E12)"),
    ("Supplementary Note 2 prints the v2 stance prompt; Methods Advocacy definition paraphrases v2", "Methods; Note 2", "C5 Note 2 (a) v1, (b) v2", "All reported labels come from v1 (decision 4; Batch 2b finding)"),
    ("Prefilter API: Batch API", "Methods", "Text correction", "First 2,500 records ran synchronously; 94,992 via one Message Batch (B7 item 8)"),
]


def superseded():
    S = "Superseded numbers"
    for i, (old, where, new, why) in enumerate(SUPERSEDED, 1):
        B.add(f"SUP-{i:02d}", S, "Old -> new -> reason", f"{old} [{where}]", f"-> {new}", window="submitted -> R1",
              source=why)
    b7 = (OUT / "B7_corrections.md").read_text()
    B.add("SUP-B7", S, "Old -> new -> reason", "All B7 numeric corrections (Table S1 P values, Table S3 seeds, Table S9 n's, "
          "Commentary 53.8%, Q1/Q2 88.1%, κ_max 0.755, AC1 0.885, prefilter κ CI, fabrication-involved series)",
          "-> see outputs/B7_corrections.md (included verbatim in the C1 markdown appendix)", window="submitted -> R1",
          source="outputs/B7_corrections.md")
    return b7


def main():
    corpus(); missing(); precision(); validation(); results(); regression(); ma_extras()
    b7 = superseded()
    intro = ("# R1 numbers book\n\nJMIR #109710, major revision R1, Batch 2c (C1). Every number the revised manuscript needs, "
             "recomputed on **2021-2025** unless the Window column says otherwise, in JMIR format, each with a stable ID and "
             "its source file. Machine-readable twin: `NUMBERS_BOOK_R1.csv` (columns: id, section, subsection, item, value, "
             "point, lo, hi, k, n, p, ci_method, window, source).\n\n"
             "**Conventions.** n/N with every percentage; 95% CI for every estimate (method in the csv `ci_method` column; "
             "default: percentile bootstrap, 1000 resamples, seed 42); exact P with no leading zero and P<.001 at the floor; "
             "commas only in numbers >= 10,000; record-level ORs per year to 3 decimals, other ORs to 2. Critical stance = Alarm "
             "or Caution; favourable = Cautious Optimism or Advocacy. Paths are relative to `revision_r1/` unless they start "
             "with `output/` (repository) or `analysis/`.\n\n"
             "**Scripts.** `final/scripts/c1_compute.py` (recomputations on 2021-2025 -> `final/data/`) and "
             "`final/scripts/c1_numbers_book.py` (this book).")
    B.write(intro)
    with open(rc.R1 / "final/NUMBERS_BOOK_R1.md", "a", encoding="utf-8") as f:
        f.write("\n\n## Appendix: B7 numeric corrections (verbatim)\n\n" + b7.replace("# B7", "### B7"))
    print(f"{len(B.rows)} numbers-book rows")


if __name__ == "__main__":
    main()
