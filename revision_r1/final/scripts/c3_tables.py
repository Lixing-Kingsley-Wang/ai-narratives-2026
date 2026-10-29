"""C3 · Main Tables 1-3 as real Word tables plus Markdown twins (JMIR R1 Batch 2c;
D1, D2a, D2b, X4a, E12, D4a, X3, D3, D6, X1).

Every cell is read from the numbers book by ID. Run with revision_r1/.venv.
Outputs: revision_r1/final/tables/Table{1,2,3}.{docx,md}, table_ids_used.csv
"""

from __future__ import annotations

import csv
import re

from c_common import TABLES, c_book, fn
from c_docx import md_table, md_text, new_doc, para, set_landscape, table

BOOK = c_book()
USED = []


def v(tab, id_):
    USED.append((tab, id_))
    return BOOK[id_]["value"]


def num(tab, id_):
    USED.append((tab, id_))
    r = BOOK[id_]
    f = lambda x: float(x) if x not in ("", None) else float("nan")
    return f(r["point"]), f(r["lo"]), f(r["hi"]), f(r["p"]), r


def slug(s):
    s = re.sub(r"[^A-Za-z0-9]+", "", s.replace("&", "and").replace("/", " ").title())
    return s[:24].upper()


def ci_cell(p, lo, hi, d=2, unit=""):
    sep = " to " if (lo < 0 or hi < 0) else "-"
    return f"{p:.{d}f}{unit} ({lo:.{d}f}{sep}{hi:.{d}f})"


def ptxt(p):
    if p != p:
        return ""
    if p < 0.001:
        return "P<.001"
    s = f"{p:.3f}"
    return "P=" + (s[1:] if s.startswith("0") else s)


def write(name, title, header, rows, notes, widths=None, landscape=False, group_rows=()):
    d = new_doc(landscape=landscape)
    para(d, title, 10, bold=True)
    table(d, header, rows, widths=widths, size=8 if not landscape else 7.5, group_rows=group_rows)
    for n_ in notes:
        para(d, n_, 8, space_after=2)
    d.save(TABLES / f"{name}.docx")
    (TABLES / f"{name}.md").write_text(f"**{md_text(title)}**\n\n{md_table(header, rows, group_rows)}\n\n" +
                                       "\n\n".join(md_text(n_) for n_ in notes) + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
def table1():
    T = "Table1"
    rows = [
        ["Prefilter, development pilot",
         "Claude Haiku 4.5 (claude-haiku-4-5-20251001), Batch API, provider-default temperature; title + first 300 abstract characters; 3 classes (discourse, evaluative, application)",
         "Records from the eligible corpus; sampling undocumented (year mix consistent with simple random sampling); unweighted; no written codebook; one coder",
         "200",
         f"3-class Cohen κ {v(T, 'VAL-PF-PILOT-K3')}",
         f"Raw agreement {v(T, 'VAL-PF-PILOT-RAW')}; KEEP sensitivity {v(T, 'VAL-PF-PILOT-SENSITIVITY')}; specificity "
         f"{v(T, 'VAL-PF-PILOT-SPECIFICITY')}; PPV {v(T, 'VAL-PF-PILOT-PPV')}; NPV {v(T, 'VAL-PF-PILOT-NPV')}"],
        ["Prefilter, R1 audit",
         "As above (production labels); full-abstract re-run with the same model and prompt as comparator",
         "Stratified by prefilter outcome x year 2021-2025 (excluded, full-abstract keep 75; excluded, full-abstract drop 225; retained 50) "
         "plus 20 pilot records recoded; design-weighted to frame sizes; codebook verbatim from the classifier prompt; one coder blinded to model labels and stratum; "
         "frozen protocol (Multimedia Appendix 1, Note 9)",
         "370",
         f"Sensitivity {v(T, 'VAL-PF-AUDIT-PROD2X2SENSITIVITY')}",
         f"Specificity {v(T, 'VAL-PF-AUDIT-PROD2X2SPECIFICITY')}; PPV {v(T, 'VAL-PF-AUDIT-PROD2X2PPV')}; NPV {v(T, 'VAL-PF-AUDIT-PROD2X2NPV')}; "
         f"Cohen κ {v(T, 'VAL-PF-AUDIT-PROD2X2KAPPA')}; Gwet AC1 {v(T, 'VAL-PF-AUDIT-PROD2X2AC1')}; false-negative rate among excluded records "
         f"(1-NPV) {v(T, 'VAL-PF-AUDIT-FNRATEPOOLED')}, about {v(T, 'VAL-PF-AUDIT-MISSEDTOTAL')} records; intra-rater KEEP/DROP agreement "
         f"{v(T, 'VAL-PF-INTRA-AGREE')}, Cohen κ {v(T, 'VAL-PF-INTRA-K')}"],
        ["Stance",
         "Claude Sonnet 4.6 (claude-sonnet-4-6), Batch API, provider-default temperature; title + full abstract; canonical v1 prompt; 5 ordered classes",
         "Stratified by model-assigned stance (Alarm 40, Caution 60, Neutral 70, Cautious Optimism 100, Advocacy 30), abstract-present records; "
         "one coder blinded to model labels; in-scope set excludes 75 records the coder judged not codable or out of scope",
         "300 (225 in scope)",
         f"Quadratic-weighted Cohen κ, in scope {v(T, 'VAL-ST-QK-225')}",
         f"Quadratic-weighted κ, all 300: {v(T, 'VAL-ST-QK-300')}; macro-F1, in scope {v(T, 'VAL-ST-MACROF1-225')}; Advocacy sensitivity "
         f"{v(T, 'VAL-ST-ADV-SENSITIVITY-225')}; Advocacy PPV {v(T, 'VAL-ST-ADV-PPV-225')}; run-to-run quadratic κ {v(T, 'VAL-ST-RTR-QK')}"],
        ["Themes",
         "Claude Sonnet 4.6, Batch API, provider-default temperature; title + first 400 abstract characters; 1-3 of 10 themes (multilabel); critical records only",
         "Critical records 2021-2025, 40 per year by simple random sampling within year (frame 4283); codebook verbatim from the classifier prompt; "
         "one coder blinded to model labels; frozen protocol; primary N=200 (Amendment 1), pre-specified N=187",
         "200",
         f"Micro-F1, N=200 {v(T, 'VAL-TH-MICRO-200-UN')}",
         f"Macro-F1, N=200 {v(T, 'VAL-TH-MACRO-200-UN')}; micro-F1, pre-specified N=187 {v(T, 'VAL-TH-MICRO-187-UN')}; F1 range, four headline "
         f"themes (N=200): {v(T, 'VAL-TH-F1RANGE-200')}"],
        ["Mechanism",
         "Claude Sonnet 4.6, synchronous API, temperature 0; title + full abstract; failure mode and model type (4 classes each); critical records only",
         "Critical records stratified by year and model-assigned failure mode; 12 title-only records excluded; one coder blinded to model labels",
         "108",
         f"Model type Cohen κ {v(T, 'VAL-MX-MT-K')}; failure mode Cohen κ {v(T, 'VAL-MX-FM-K')}",
         f"Model type: Gwet AC1 {v(T, 'VAL-MX-MT-AC1')}, raw agreement {v(T, 'VAL-MX-MT-RAW')}. Failure mode: Gwet AC1 {v(T, 'VAL-MX-FM-AC1')}, "
         f"raw agreement {v(T, 'VAL-MX-FM-RAW')}, κ_max {v(T, 'VAL-MX-FM-KMAX')}. Fabrication disagreements, model fabrication-involved and human not "
         f"vs the reverse: {v(T, 'VAL-MX-FABDIR').split(' (')[0]}"],
        ["Specialty",
         "Claude Haiku 4.5 (claude-haiku-4-5), Batch API, provider-default temperature; title + full abstract; 18 categories",
         "Stratified by model-assigned specialty; coder could choose 'unclear from abstract'; one coder blinded to model labels",
         "120",
         f"Cohen κ {v(T, 'VAL-SP-K')}",
         f"Gwet AC1 {v(T, 'VAL-SP-AC1')}; raw agreement {v(T, 'VAL-SP-RAW')}; κ_max {v(T, 'VAL-SP-KMAX')}"],
    ]
    notes = [
        "Agreement is between the model label and the human code. CIs: percentile bootstrap over records (1000 resamples, seed 42) unless stated; "
        "prefilter audit metrics are design-weighted with Jeffreys intervals (Beta(k+1/2, n-k+1/2) draws per sampling cell, 10,000 draws, seed 42; "
        "Amendment 3); raw agreement uses the exact Clopper-Pearson interval.",
        "Prefilter metrics treat discourse or evaluative as KEEP (positive) and application as DROP. In the audit, the one unlabelled record counts as "
        "an error of the classifier being evaluated (Amendment 2).",
        "Theme F1 values are unweighted; frame-weighted estimates and per-theme values are in Multimedia Appendix 3.",
        "κ_max: the largest κ attainable given the two sets of marginal totals.",
        "The intra-rater κ interval spans 0 to 1 because only 1 of the 20 recoded records disagreed, so many bootstrap resamples "
        "contain no disagreement or no DROP record; the exact interval for raw agreement is more informative.",
        "The development pilot preceded the production run and its CI could not be reproduced from the original code; the value shown is a "
        "recomputation with the study's bootstrap.",
    ]
    write(T, "Table 1. Human validation of every large language model classification step.",
          ["Step", "Model and input", "Validation design (sampling, blinding, coder)", "n", "Primary metric (95% CI)", "Other metrics (95% CI)"],
          rows, notes, widths=[0.9, 1.6, 1.9, 0.5, 1.4, 2.6], landscape=True)


# ---------------------------------------------------------------------------
def table2():
    T = "Table2"
    from analysis.run_specialty_aiadoption import ALL_SPECIALTIES  # noqa
    order = {
        "genre": ["discourse", "evaluative"],
        "pubtype": ["Research Article", "Review", "Editorial", "Letter", "Commentary"],
        "specialty": ["Medical Informatics / Digital Health"] + sorted(s for s in ALL_SPECIALTIES if s != "Medical Informatics / Digital Health") + ["Unassigned"],
        "region": ["North America", "Western Europe", "East Asia", "Eastern Europe", "Latin America / Oceania", "Middle East / North Africa",
                   "South/Southeast Asia", "Sub-Saharan Africa", "Unknown"],
    }
    label = {"genre": "Genre (prefilter)", "pubtype": "Publication type", "specialty": "Specialty or domain category",
             "region": "First-author region"}
    rows, groups = [], []
    groups.append(len(rows)); rows.append(["Publication year"])
    u = num(T, "RES-REG-YEAR-UOR"); a = num(T, "RES-TMP-CRIT-AOR")
    rows.append(["Per 1 year (continuous)", fn(14058), ci_cell(*u[:3], d=3), ci_cell(*a[:3], d=3), ptxt(a[3]), ""])
    for y in (2021, 2022, 2023, 2024, 2025):
        m = num(T, f"RES-TMP-CRIT-AMP-{y}")
        n = num(T, f"RES-TMP-CRIT-{y}")[4]["n"]
        rows.append([f"  {y}", fn(float(n)), "", "", "", ci_cell(*m[:3], d=1)])
    for var in ("genre", "pubtype", "specialty", "region"):
        groups.append(len(rows)); rows.append([label[var]])
        for lvl in order[var]:
            tag = f"RES-REG-{var.upper()}-{slug(lvl)}"
            n = num(T, f"{tag}-N")[0]
            if BOOK[f"{tag}-AOR"]["value"].startswith("1 (reference)"):
                USED.append((T, f"{tag}-AOR"))
                orr, uor, pp = "1 (reference)", "1 (reference)", ""
            else:
                ao = num(T, f"{tag}-AOR"); uo = num(T, f"{tag}-UOR")
                orr, uor, pp = ci_cell(*ao[:3]), ci_cell(*uo[:3]), ptxt(ao[3])
            am = num(T, f"{tag}-AMP")
            name = lvl if lvl != "Unassigned" else "Unassigned (specialty classification FAILED)"
            rows.append([f"  {name}", fn(n), uor, orr, pp, ci_cell(*am[:3], d=1)])
    notes = [
        f"{md_free(v(T, 'RES-REG-HEADER'))}.",
        "Critical stance was Alarm or Caution. Unadjusted OR: one-predictor logistic model with the same cluster-robust SEs. Adjusted OR: all "
        "covariates in the table entered together. P values are for the adjusted OR (Wald, cluster-robust). AMP: average marginal predicted "
        "probability of critical stance with all records set to that level and other covariates at their observed values; 95% CI by the delta "
        "method on the logit scale with the cluster-robust covariance.",
        "Reference levels: discourse (genre), Research Article (publication type), Medical Informatics / Digital Health (specialty), North America "
        "(region); chosen as the most frequent level. Region 'Unknown' (affiliation not resolvable) and specialty 'Unassigned' (classification "
        "FAILED) are kept as levels so that no record is dropped.",
        "Standard errors are cluster-robust by journal (normalised SJR-matching title; 2278 clusters).",
        "Not included: model type (failure-mechanism axis), because it is defined only for critical records and therefore cannot predict "
        "critical stance; and FDA cleared-device count, because it is an 18-unit category-level (ecological) variable that is fully determined "
        "by specialty and would be collinear with the specialty terms.",
        "Sensitivity models (categorical year, adding January-April 2026, journal fixed effects, first-author country instead of region), the "
        "ordinal model with its proportional-odds check and the Advocacy model are in Multimedia Appendix 3.",
    ]
    write(T, "Table 2. Multivariable logistic regression of critical stance, 2021-2025 (n=14,058; 4283 events; 2278 journal clusters).",
          ["Variable and level", "Records, n", "Unadjusted OR (95% CI)", "Adjusted OR (95% CI)", "P (adjusted)", "AMP, % (95% CI)"],
          rows, notes, widths=[2.9, 0.8, 1.4, 1.4, 0.8, 1.3], landscape=True, group_rows=groups)


def md_free(s):
    return s


# ---------------------------------------------------------------------------
def or_from_text(s):
    m = re.search(r"OR ([0-9.]+) per year \(95% CI ([0-9.]+)-([0-9.]+)\)", s)
    return f"OR {m[1]} ({m[2]}-{m[3]})" if m else s


def table3():
    T = "Table3"
    D = "—"

    def orc(id_, d=3):
        p, lo, hi, P, _ = num(T, id_)
        return f"OR {p:.{d}f} ({lo:.{d}f}-{hi:.{d}f})"

    def pc(id_):
        return f"{num(T, id_)[0]:.1f}%"

    def b5(id_):
        return or_from_text(v(T, id_))

    def b5pct(id_):
        return v(T, id_).split(" (")[0]

    rows = []
    rows.append(["Critical trend (OR per year)", orc("RES-TMP-CRIT-OR"), orc("RES-TMP-CRIT-AOR"), orc("RES-SEN-B4S3-YEAR"),
                 orc("RES-SEN-B2B-CRITICAL"), orc("RES-SEN-B2D-CRITICAL"), b5("RES-SEN-B5D1-CRITICAL"), D])
    rows.append(["Advocacy trend (OR per year)", orc("RES-TMP-ADV-OR"), orc("RES-TMP-ADV-AOR"), D,
                 orc("RES-SEN-B2B-ADVOCACY"), orc("RES-SEN-B2D-ADVOCACY"), b5("RES-SEN-B5D1-ADVOCACY"),
                 "Strong endorsement " + orc("RES-TMP-SE-OR")])
    rows.append(["Strong endorsement trend (OR per year)", orc("RES-TMP-SE-OR"), D, D, D, D, D, D])
    for t in ("Patient safety", "Hallucination / errors", "Governance / regulation", "Ethics & bias"):
        b5id = {"Patient safety": "PATIENTSAFETY", "Hallucination / errors": "HALLUCINATIONERRORS",
                "Governance / regulation": "GOVERNANCEREGULATION", "Ethics & bias": "ETHICSANDBIAS"}[t]
        rows.append([f"Theme trend among critical records: {t} (OR per year)", orc(f"RES-TMP-TH-{slug(t)}-OR"), D, D, D, D,
                     b5(f"RES-SEN-B5D1-{b5id}"), D])
    mh, ca = num(T, "RES-SPC-AMP-MENTALHEALTHPSYCHIATRY"), num(T, "RES-SPC-AMP-CARDIOLOGY")
    rng = v(T, "RES-SPC-RANGE")
    m = re.match(r"(.+?) ([0-9.]+)% \(.*?\) to (.+?) ([0-9.]+)%", rng)
    rows.append(["Specialty range of critical rate (highest to lowest)", f"{m[1]} {m[2]}% to {m[3]} {m[4]}%",
                 f"AMP: Mental Health / Psychiatry {mh[0]:.1f}% to Cardiology {ca[0]:.1f}%", D, D, D,
                 re.sub(r" \(\d+/\d+\)", "", v(T, "RES-SEN-B5D1-SPC-RANGEN30CATEGORIES")), D])
    rows.append(["East Asia vs North America (critical)", f"{pc('RES-GEO-REG-EASTASIA')} vs {pc('RES-GEO-REG-NORTHAMERICA')}",
                 orc("RES-GEO-AOR-EASTASIA", 2), orc("RES-REGSEN-S3-REGION-EASTASIA", 2), D, D,
                 f"{b5pct('RES-SEN-B5D1-REG-EASTASIA')} vs {b5pct('RES-SEN-B5D1-REG-NORTHAMERICA')}", D])
    rows.append(["United States vs China (critical)", f"{pc('RES-GEO-CTY-UNITEDSTATES')} vs {pc('RES-GEO-CTY-CHINA')}",
                 orc("RES-GEO-USCN-AOR", 2), D, D, D, D, D])
    rows.append(["Reviews vs Research Articles (critical)", f"{pc('RES-FMT-REVIEW-CRITICAL')} vs {pc('RES-FMT-RESEARCHARTICLE-CRITICAL')}",
                 orc("RES-FMT-REVIEW-AOR", 2), orc("RES-REGSEN-S3-PUBTYPE-REVIEW", 2), D, D,
                 f"{b5pct('RES-SEN-B5D1-PT-REVIEW')} vs {b5pct('RES-SEN-B5D1-PT-RESEARCHARTICLE')}", D])
    f18 = num(T, "RES-SPC-FDA-RHO18")
    fdab5 = v(T, "RES-SEN-B5D1-SPC-FDASPEARMAN")
    rows.append(["FDA cleared-device count vs critical rate, 18 categories (Spearman ρ)", f"ρ={f18[0]:.2f} ({ptxt(f18[3])})", D, D, D, D,
                 "ρ=" + fdab5.replace(" (two-sided ", " (").replace(", n=18)", ")"), D])
    s3n = v(T, "RES-SEN-B4S3-N").split(" records")[0].replace("n=", "")
    rec = v(T, "RES-SEN-B2-RECOVERED"); drop = v(T, "RES-SEN-B2-DROPPED"); rem = v(T, "RES-SEN-B5D1-REMOVED").split(" of")[0]
    notes = [
        "Primary: 2021-2025 analytic corpus, unadjusted; OR per year from record-level logistic regression on publication year (Wald 95% CI). "
        "Adjusted: B4 multivariable model (Table 2; journal-clustered SEs); for the specialty row, adjusted average marginal probabilities. "
        f"Within journal: B4 sensitivity model with journal fixed effects (journals with at least 10 records and outcome variation; n={s3n}). "
        f"Augmented: production corpus plus {rec} records dated 2021-2025 that the production prefilter excluded but the full-abstract re-run "
        f"kept, stance-classified with the same v1 prompt (B2 corpus b). Full abstract: corpus defined by the full-abstract prefilter labels, "
        f"which adds the same {rec} records and drops {drop} production records (B2 corpus d). SJR medical: records in journals that are Q1/Q2 "
        f"in at least one SCImago Medicine-area category (B5 definition D1; {rem} records removed from 2021-2025). Symmetric scale: "
        "'strong endorsement' flag from a re-classification that drops the transformative-language requirement (B3).",
        "Values are OR (95% CI) unless shown as percentages or ρ. Critical stance was Alarm or Caution.",
        "— not applicable or not estimated: B4 modelled the critical and Advocacy outcomes only (no theme models), and the FDA count is an "
        "ecological variable that was not modelled; the journal fixed-effects model was fitted for the critical outcome only; recovered B2 "
        "records carry a stance label but no theme, specialty or region label, so B2 was used for the stance trends only; B5 did not "
        "recompute first-author country; the symmetric scale applies to the favourable end only.",
        "Full values with exact P and n/N for every cell are in the R1 numbers book and Multimedia Appendix 3.",
    ]
    write(T, "Table 3. Robustness of the headline findings to adjustment, corpus definition and stance scale.",
          ["Headline", "Primary (2021-2025, unadjusted)", "Adjusted (B4)", "Within journal (B4 S3)", "Augmented corpus (B2 b)",
           "Full-abstract corpus (B2 d)", "SJR medical corpus (B5 D1)", "Symmetric scale (B3)"],
          rows, notes, widths=[1.6, 1.35, 1.35, 1.1, 1.05, 1.05, 1.3, 1.1], landscape=True)


def main():
    table1(); table2(); table3()
    with open(TABLES / "table_ids_used.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["table", "id"]); w.writerows(sorted(set(USED)))
    print("tables done;", len(set(USED)), "book IDs used")


if __name__ == "__main__":
    main()
