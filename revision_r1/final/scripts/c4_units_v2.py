"""Batch 2d copy of c4_units.py: v2 book; writes <id>_v2.json for every MA3 unit and
<id>_caption_v2.md for every MA2 caption that quotes a changed OR; figures are not redrawn.

C4 · Multimedia Appendix 2 (figures) and 3 (tables) as numbered units
(JMIR R1 Batch 2c).

Each unit has a stable ID and is written to revision_r1/final/ma/units/:
  tables/<id>.json   caption (with {{F:id}} / {{T:id}} placeholders), header, rows,
                     group rows, footnotes, layout, and the numbers-book IDs used
  figures/<id>.png, <id>.pdf, <id>_caption.md (+ <id>.json with the IDs used)
Numbering, placeholder resolution and the .docx/.md appendices are done by
revision_r1/final/ma/assemble.py from ma_order.yaml.

All numbers come from the numbers book by ID. Figures: 2021-2025 only (the
forward-validation Sankey keeps its own design), JMIR figure rules as in
c2_figures.py. Run with the project venv (geopandas for the 20-record map).
"""

from __future__ import annotations

import json
import re
import shutil

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

import c_common as _cc  # Batch 2d: read the v2 numbers book (journal cluster-robust ORs)
_cc.BOOK_CSV = _cc.FINAL / "NUMBERS_BOOK_R1_v2.csv"
from c_common import (HEADLINE_THEMES, MA, R1, REPO, STANCE_COLOURS, THEME_COLOURS, Y5, c_book, fn, rc)  # noqa: E402

UT = MA / "units" / "tables"; UF = MA / "units" / "figures"
for d in (UT, UF):
    d.mkdir(parents=True, exist_ok=True)
BOOK = c_book()
plt.rcParams.update({"font.family": ["Arial", "DejaVu Sans"], "font.size": 7, "axes.titlesize": 7, "axes.labelsize": 7,
                     "xtick.labelsize": 7, "ytick.labelsize": 7, "legend.fontsize": 7, "pdf.fonttype": 42,
                     "axes.spines.top": False, "axes.spines.right": False, "axes.linewidth": 0.6})
W_IN, DPI = 7.5, 600
D = "—"


class U:
    """Collects the book IDs a unit uses."""

    def __init__(self, uid):
        self.uid, self.ids = uid, []

    def v(self, id_):
        self.ids.append(id_)
        return BOOK[id_]["value"]

    def n(self, id_):
        self.ids.append(id_)
        r = BOOK[id_]
        f = lambda x: float(x) if x not in ("", None) else float("nan")
        return {"point": f(r["point"]), "lo": f(r["lo"]), "hi": f(r["hi"]), "k": f(r["k"]), "n": f(r["n"]), "p": f(r["p"]),
                "value": r["value"], "item": r["item"]}

    def has(self, id_):
        return id_ in BOOK


def slug(s):
    s = re.sub(r"[^A-Za-z0-9]+", "", s.replace("&", "and").replace("/", " ").title())
    return s[:24].upper()


def ptxt(p):
    if p != p:
        return ""
    if p < 0.001:
        return "P<.001"
    if p > 0.999:
        return "P>.99"
    s = f"{p:.3f}"
    return "P=" + (s[1:] if s.startswith("0") else s)


def cic(p, lo, hi, d=1):
    sep = " to " if (lo < 0 or hi < 0) else "-"
    return f"{p:.{d}f} ({lo:.{d}f}{sep}{hi:.{d}f})"


def share(u, id_, d=1):
    """'31.0 (29.8-32.3); 1828/5898' from a book share row."""
    x = u.n(id_)
    return f"{cic(x['point'], x['lo'], x['hi'], d)}; {fn(x['k'])}/{fn(x['n'])}"


V2_NOTE = ("Version 2 (Batch 2d): every OR per year here comes from record-level logistic regression on publication year with "
           "journal cluster-robust SEs (95% CI and P from the cluster-robust covariance); point estimates are unchanged.")


def table_unit(u, caption, header, rows, notes, landscape=False, group_rows=()):
    notes = list(notes) + [V2_NOTE]
    spec = {"id": u.uid, "kind": "table", "caption": caption, "header": header, "rows": rows, "group_rows": list(group_rows),
            "notes": notes, "landscape": landscape, "book_ids": sorted(set(u.ids))}
    if u.uid in AFFECTED:
        (UT / f"{u.uid}_v2.json").write_text(json.dumps(spec, indent=1, ensure_ascii=False), encoding="utf-8")


def fig_save(u, fig, caption):
    plt.close(fig)   # Batch 2d: figure unchanged, caption only
    if u.uid in AFFECTED:
        (UF / f"{u.uid}_caption_v2.md").write_text(caption + " " + V2_NOTE + "\n", encoding="utf-8")


CRIT = "Critical stance was Alarm or Caution."
FAV = "Favourable stance was Cautious Optimism or Advocacy."
BOOTN = "95% percentile bootstrap CIs (1000 resamples, seed 42)"


# =====================================================================
# MA3 table units
# =====================================================================
def t_stance_trend():
    u = U("stance_trend")
    rows = []
    for code, s, v2 in (("ALARM", "Alarm", "ALARM"), ("CAUT", "Caution", "CAUTION"), ("NEUT", "Neutral", "NEUTRAL"),
                        ("CO", "Cautious Optimism", "CAUTIOUSOPTIMISM"), ("ADV", "Advocacy", "ADVOCACY"),
                        ("CRIT", "Critical (Alarm or Caution)", "CRITICAL"), ("FAV", "Favourable (Cautious Optimism or Advocacy)", None)):
        a, b = u.n(f"RES-TMP-{code}-2021"), u.n(f"RES-TMP-{code}-2025")
        r = u.n(f"RES-TMP-{code}-RHO"); o = u.n(f"RES-TMP-{code}-OR")
        if v2:
            vv = u.v(f"RES-V2-{v2}")
            v2rho = float(re.search(r"ρ=([+-][0-9.]+)", vv)[1])
            same = "same" if np.sign(v2rho) == np.sign(r["point"]) else "opposite"
            v2c = f"{vv.split(';')[0]}; {vv.split('; ')[1]} ({same} direction)"
        else:
            v2c = D
        rows.append([s, share(u, f"RES-TMP-{code}-2021"), share(u, f"RES-TMP-{code}-2025"), f"{u.n(f'RES-TMP-{code}-DELTA')['point']:+.1f}",
                     f"{r['point']:+.2f} ({ptxt(r['p'])})", cic(o["point"], o["lo"], o["hi"], 3), ptxt(o["p"]), v2c])
    table_unit(u, "Per-stance temporal trend under the canonical v1 rubric and the stricter v2 rubric, 2021-2025.",
               ["Stance", "2021, % (95% CI); n/N", "2025, % (95% CI); n/N", "Change, percentage points", "Spearman ρ (exact P)",
                "OR per year (95% CI)", "P (OR)", "v2 rubric: 2021 to 2025; ρ (exact P)"], rows,
               [f"Annual shares among records with a valid v1 stance (2021 n={fn(u.n('RES-TMP-CRIT-2021')['n'])}; 2025 "
                f"n={fn(u.n('RES-TMP-CRIT-2025')['n'])}); {BOOTN}, joint resampling of records. Spearman ρ over the five annual values "
                "with the exact two-sided permutation P (all 120 orderings; the smallest attainable P is .017). OR per year: record-level "
                "logistic regression of the outcome on publication year (journal cluster-robust SEs). v2: a stricter conclusion-anchored prompt used only "
                "for this sensitivity analysis (Multimedia Appendix 1, Note 2b); its favourable share was not tabulated separately. "
                f"{CRIT} {FAV}"], landscape=True)


def t_update_2026():
    u = U("update_2026")
    rows = []
    for code, s in (("ALARM", "Alarm"), ("CAUTION", "Caution"), ("NEUTRAL", "Neutral"), ("CAUTIOUSOPTIMISM", "Cautious Optimism"),
                    ("ADVOCACY", "Advocacy"), ("CRITICALALARMCAUTION", "Critical (Alarm or Caution)"),
                    ("FAVOURABLECOADVOCACY", "Favourable (Cautious Optimism or Advocacy)")):
        x = u.n(f"RES-2026-{code}")
        rows.append([s, f"{fn(x['k'])}/{fn(x['n'])}", cic(x["point"], x["lo"], x["hi"])])
    table_unit(u, "Stance distribution among records published January to April 2026 (descriptive only).",
               ["Stance", "n/N", "% (95% CI)"], rows,
               [f"January-April 2026 records with a valid stance (n={fn(u.n('COR-2026-N')['point'])}), classified with the same v1 prompt. "
                "These records are outside the 2021-2025 analytic window; they are reported descriptively and enter no trend statistic, "
                f"figure or model. {BOOTN}, resampling 2026 records only. {CRIT} {FAV}"])


def t_within_genre():
    u = U("within_genre")
    rows = []
    for y in Y5:
        r = u.n(f"RES-TMP-GENRATIO-{y}")
        rows.append([str(y), share(u, f"RES-TMP-GENDISC-{y}"), share(u, f"RES-TMP-GENEVAL-{y}"), u.v(f"RES-TMP-GENRATIO-{y}")])
    rd, re_ = u.n("RES-TMP-GENDISC-RHO"), u.n("RES-TMP-GENEVAL-RHO")
    od, oe = u.n("RES-TMP-GENDISC-OR"), u.n("RES-TMP-GENEVAL-OR")
    table_unit(u, "Annual critical share within each prefilter genre, 2021-2025.",
               ["Year", "Discourse: critical % (95% CI); n/N", "Evaluative: critical % (95% CI); n/N", "Discourse:evaluative ratio (n/n)"],
               rows,
               [f"Critical share computed separately within discourse and evaluative records. {BOOTN.replace('seed 42', 'deterministic seed 42 + cell index per genre-year cell, cells ordered by genre then year')}; "
                "point estimates are unchanged from the submitted Table S3. "
                f"Discourse: Spearman ρ {rd['value']}; {od['value']}. Evaluative: Spearman ρ {re_['value']}; {oe['value']}. "
                f"Annual series are plotted in {{{{F:within_genre_fig}}}}. {CRIT}"])


def t_keep_rate():
    u = U("keep_rate")
    rows = [[str(y), share(u, f"RES-TMP-KEEP-{y}")] for y in Y5]
    table_unit(u, "Annual prefilter keep rate, 2021-2025.", ["Year", "Kept, % (95% CI); kept/eligible"], rows,
               [f"Proportion of eligible Q1/Q2 records retained by the AI-engagement prefilter as discourse or evaluative. Year is the first "
                f"four-digit year in the PubMed date field. {BOOTN}. Spearman ρ {u.v('RES-TMP-KEEP-RHO')}; {u.v('RES-TMP-KEEP-OR')}. "
                "The R1 prefilter audit estimates the false-negative rate among excluded records by year in "
                "{{T:prefilter_validation}}."])


def t_themes():
    u = U("themes")
    rows = []
    for t in rc.THEMES:
        lab = rc.THEME_LABELS[t]; s_ = slug(lab)
        a, b = u.n(f"RES-TMP-TH-{s_}-2021"), u.n(f"RES-TMP-TH-{s_}-2025")
        r, o = u.n(f"RES-TMP-TH-{s_}-RHO"), u.n(f"RES-TMP-TH-{s_}-OR")
        rows.append([lab, share(u, f"RES-THM-POOLED-{s_}"), f"{a['point']:.1f}", f"{b['point']:.1f}", f"{u.n(f'RES-TMP-TH-{s_}-DELTA')['point']:+.1f}",
                     f"{r['point']:+.2f} ({ptxt(r['p'])})", cic(o["point"], o["lo"], o["hi"], 3), ptxt(o["p"])])
    table_unit(u, "Prevalence and temporal trend of the ten concern themes among critical records, 2021-2025.",
               ["Theme", "Pooled 2021-2025, % (95% CI); n/N", "2021, %", "2025, %", "Change, percentage points", "Spearman ρ (exact P)",
                "OR per year (95% CI)", "P (OR)"], rows,
               [f"Denominator: {fn(u.n('COR-SUB-01')['point'])} critical records 2021-2025 (per-year n in Figure 2). Themes were multilabel "
                f"(one to three per record), so prevalences do not sum to 100%. {BOOTN}. Annual values with CIs for every year are in the R1 "
                "numbers book; the six lower-prevalence themes are plotted in {{F:other_themes_fig}} and annual counts in "
                f"{{{{F:theme_counts_fig}}}}. {CRIT}"], landscape=True)


def t_fda_robustness():
    u = U("fda_robustness")
    rows = []
    for id_ in ("RES-SPC-FDA-RHO18", "RES-SPC-GEN-RHO", "RES-SPC-FDAGEN-RHO", "RES-SPC-FDA-PARTIAL", "RES-SPC-FDA-RHO11", "RES-SPC-EVAL-RHO"):
        x = u.n(id_)
        rows.append([x["item"].rsplit(" (n=", 1)[0], str(int(x["n"])), f"{x['point']:+.2f}", x["value"].split("(", 1)[1].rstrip(")")])
    table_unit(u, "Robustness of the association between critical rate and FDA cleared-device count across specialty categories, 2021-2025.",
               ["Relationship", "Categories, n", "Spearman ρ", "P"], rows,
               ["Spearman correlations across specialty or domain categories (category-level, ecological units). Critical rate per category "
                "from 2021-2025 records; FDA counts from the list of AI/ML-enabled devices cleared 1995-2025 mapped to review panels "
                "({{T:fda_mapping}}). The two-sided P is primary; one-sided P (alternative ρ<0) and a one-sided pairing-permutation P "
                "(10,000 permutations, seed 42) are sensitivity variants. Generative-model share is computed among abstract-present critical "
                "records and is endogenous to criticality, so the partial correlation is a sensitivity analysis, not a confounder adjustment. "
                "Structural zeros: the 7 categories with no mapped FDA panel. This is an exploratory ecological association."])


def t_country():
    u = U("country")
    rows = []
    for k in [k for k in BOOK if k.startswith("RES-GEO-CTY-")]:
        x = u.n(k)
        name = x["item"].split(":")[0] + ("†" if "20-49" in x["item"] else "")
        rows.append((x["n"], [name, fn(x["n"]), f"{fn(x['k'])}", cic(x["point"], x["lo"], x["hi"])]))
    rows = [r for _, r in sorted(rows, key=lambda t: -t[0])]
    table_unit(u, "Critical rate by country of first authorship, countries with at least 20 records, 2021-2025.",
               ["Country", "Records, n", "Critical, n", "Critical, % (95% CI)"], rows,
               [f"Country resolved from the first-author affiliation ({fn(u.n('COR-SUB-10')['point'])} of 14,058 records resolved); "
                f"{u.v('RES-GEO-NCTY20')} countries have at least 20 records and {u.v('RES-GEO-NCTY50')} at least 50. {BOOTN}, resampling "
                "within country. † 20 to 49 records: low-confidence estimate, shown only on the 20-record map ({{F:country_map_20}}); "
                "Figure 5 shows countries with at least 50 records. Country indexes publication discourse, not national attitudes, "
                f"research quality or AI capability. {CRIT}"])


def t_ea_vs_nawe():
    u = U("ea_vs_nawe_within_specialty")
    rows = []
    for k in [k for k in BOOK if k.startswith("RES-GEO-EAWS-")]:
        x = u.n(k)
        m = re.match(r"East Asia ([0-9.]+)% \((\d+)/(\d+); 95% CI ([0-9.]+)%-([0-9.]+)%\) vs ([0-9.]+)% \((\d+)/(\d+); 95% CI ([0-9.]+)%-([0-9.]+)%\); "
                     r"difference ([+-][0-9.]+)", x["value"])
        rows.append([x["item"].split(":")[0], m[3], f"{m[1]} ({m[4]}-{m[5]}); {m[2]}/{m[3]}", m[8], f"{m[6]} ({m[9]}-{m[10]}); {m[7]}/{m[8]}", m[11]])
    table_unit(u, "Critical rate within specialty, East Asian vs North American or Western European first authors, 2021-2025.",
               ["Specialty", "East Asia, n", "East Asia, % (95% CI); n/N", "North America + Western Europe, n",
                "North America + Western Europe, % (95% CI); n/N", "Difference, percentage points"], rows,
               ["The ten specialty categories most frequent among East Asian first authors with at least 30 records in both groups "
                f"(run_east_asia_diagnose.py rule). {BOOTN}, resampling within group. Reweighting East Asia to the North America + "
                f"Western Europe specialty mix: {u.v('RES-GEO-EARW')}. Region from the first-author affiliation. {CRIT}"], landscape=True)


def t_region():
    u = U("region")
    rows = []
    for reg in ["North America", "Western Europe", "East Asia", "Middle East / North Africa", "South/Southeast Asia", "Latin America / Oceania",
                "Eastern Europe", "Sub-Saharan Africa", "Unknown"]:
        s_ = slug(reg)
        aor = u.v(f"RES-GEO-AOR-{s_}") if u.has(f"RES-GEO-AOR-{s_}") else "1 (reference)"
        am = u.n(f"RES-GEO-AMP-{s_}")
        rows.append([reg + ("†" if reg == "Unknown" else ""), fn(u.n(f"RES-GEO-REG-{s_}")["n"]), share(u, f"RES-GEO-REG-{s_}"),
                     cic(am["point"], am["lo"], am["hi"]), aor])
    table_unit(u, "Critical rate by first-author region, 2021-2025.",
               ["Region", "Records, n", "Critical, % (95% CI); n/N", "Adjusted AMP, % (95% CI)", "Adjusted OR vs North America (95% CI), P"],
               rows,
               [f"Regions from the first-author country (geography_classifications.csv); n's are on the 14,058-record analytic corpus. {BOOTN}, "
                "joint resampling of records. Adjusted values from the multivariable model in Table 2 (AMP: average marginal predicted "
                "probability). † Affiliation not resolvable to a country; kept for denominator completeness. Sub-Saharan Africa has few "
                f"records and a correspondingly wide interval. {CRIT}"], landscape=True)


def t_pubtype():
    u = U("pubtype")
    types = ["Research Article", "Review", "Editorial", "Letter", "Commentary"]
    outs = rc.STANCES + ["Critical", "Favourable"]
    rows = []
    for t in types:
        n = u.n(f"RES-FMT-{slug(t)}-CRITICAL")["n"]
        row = [t, fn(n)]
        for o in outs:
            x = u.n(f"RES-FMT-{slug(t)}-{slug(o)}")
            row.append(f"{cic(x['point'], x['lo'], x['hi'])}; {fn(x['k'])}")
        rows.append(row)
    table_unit(u, "Stance distribution by publication type, 2021-2025.",
               ["Publication type", "Records, n"] + [f"{o}, % (95% CI); n" for o in outs], rows,
               [f"Row percentages; {BOOTN}, resampling within type. Opinion formats (Commentary, Letter and Editorial pooled), critical "
                f"{u.v('RES-FMT-OPINION-CRIT')}. Opinion formats vs Research Articles, five-category stance distribution: "
                f"{u.v('RES-FMT-CHISQ')} (χ² test of independence). Adjusted ORs are in Table 2. {CRIT} {FAV}"], landscape=True)


def t_review_subtypes():
    u = U("review_subtypes")
    outs = ["Critical", "Alarm", "Caution", "Neutral", "Cautious Optimism", "Advocacy", "Favourable"]
    rows = []
    for st in ("Systematic Review", "Review (narrative)"):
        n = u.n(f"RES-FMT-RSUB-{slug(st)}-CRITICAL")["n"]
        rows.append([st, fn(n)] + [f"{cic(x['point'], x['lo'], x['hi'])}; {fn(x['k'])}" for x in
                                   (u.n(f"RES-FMT-RSUB-{slug(st)}-{slug(o)}") for o in outs)])
    table_unit(u, "Stance distribution within the two review subtypes, 2021-2025.",
               ["Subtype", "Records, n"] + [f"{o}, % (95% CI); n" for o in outs], rows,
               [f"{BOOTN}, resampling within subtype. Subtype rule: {u.v('RES-FMT-RSUB-RULE')} {CRIT} {FAV}"], landscape=True)


def t_theme_by_format():
    u = U("theme_by_format")
    rows = []
    for k in [k for k in BOOK if k.startswith("RES-FMT-THEME-")]:
        x = u.n(k)
        m = re.match(r"Reviews ([0-9.]+)% \((\d+)/(\d+); 95% CI ([0-9.]+)%-([0-9.]+)%\) vs Research Articles ([0-9.]+)% \((\d+)/(\d+); "
                     r"95% CI ([0-9.]+)%-([0-9.]+)%\); difference ([+-][0-9.]+)", x["value"])
        rows.append([x["item"].split(" among")[0], f"{m[1]} ({m[4]}-{m[5]}); {m[2]}/{m[3]}", f"{m[6]} ({m[9]}-{m[10]}); {m[7]}/{m[8]}", m[11]])
    table_unit(u, "Concern-theme prevalence among critical records, Reviews compared with Research Articles, 2021-2025.",
               ["Theme", "Reviews, % (95% CI); n/N", "Research Articles, % (95% CI); n/N", "Difference, percentage points"], rows,
               [f"Prevalence of each theme among critical records within each format; themes were multilabel, so columns do not sum to 100%. "
                f"Difference = Reviews minus Research Articles. {BOOTN}, resampling within format. {CRIT}"])


def t_fv():
    u = U("fv_tier_verdict")
    rows = []
    labs = {"1": "Tier 1, specific superiority or replacement", "2": "Tier 2, capability deployment", "3": "Tier 3, diffuse transformation"}
    for t in ("1", "2", "3"):
        x = u.v(f"RES-FV-TIER{t}")
        m = re.match(r"borne out (\d+); partially (\d+); not borne out (\d+); too early/unfalsifiable (\d+) \(n=(\d+)\)", x)
        rows.append([f"{labs[t]} (n={m[5]})", m[1], m[2], m[3], m[4], u.v(f"RES-FV-SILENT-T{t}")])
    tot = [u.n(f"RES-FV-{s}")["point"] for s in ("BORNEOUT", "PARTIALLY", "NOTBORNEOUT", "TOOEARLYUNFALSIFIABLE")]
    rows.append(["Total (n=78)"] + [str(int(x)) for x in tot] + [str(sum(int(u.v(f'RES-FV-SILENT-T{t}')) for t in '123'))])
    table_unit(u, "Forward-validation of early Advocacy predictions: adjudicated verdicts by falsifiability tier (unchanged).",
               ["Tier", "Borne out", "Partially borne out", "Not borne out", "Too early or unfalsifiable", "of which corpus silent"], rows,
               [f"All {u.v('RES-FV-SET')} from Advocacy records published 2021-2023 with a confirmed predictive claim "
                f"({u.v('RES-FV-CAND')} flagged; {u.v('RES-FV-FP')} false positives removed by blind human review). Claims were adjudicated by a "
                "single rater against evidence published 2024 to April 2026 (the evidence window predates the 2021-2025 analytic decision "
                "and is unchanged). 'Not borne out' required positive contrary evidence; corpus silence was classified as too early or "
                "unfalsifiable. Exploratory, Advocacy-only and retrieval-dependent; the flow diagram is {{F:forward_validation_sankey}}."])


def t_q3():
    u = U("q3_arm")
    rows, groups = [], [0]
    rows.append(["Pooled 2021-2025"])
    for s in rc.STANCES + ["Critical", "Favourable"]:
        a, b = u.n(f"RES-OVR-{slug(s)}"), u.n(f"RES-Q3-POOLED-{slug(s)}")
        rows.append([s, share(u, f"RES-OVR-{slug(s)}"), share(u, f"RES-Q3-POOLED-{slug(s)}"), f"{b['point'] - a['point']:+.1f}"])
    groups.append(len(rows)); rows.append(["Critical share by year"])
    for y in Y5:
        a, b = u.n(f"RES-TMP-CRIT-{y}"), u.n(f"RES-TMP-Q3-CRIT-{y}")
        rows.append([str(y), share(u, f"RES-TMP-CRIT-{y}"), share(u, f"RES-TMP-Q3-CRIT-{y}"), f"{b['point'] - a['point']:+.1f}"])
    table_unit(u, "Stance in the Q1/Q2 analytic corpus and the Q3 comparison arm, 2021-2025.",
               ["Stance or year", "Q1/Q2, % (95% CI); n/N", "Q3, % (95% CI); n/N", "Difference (Q3 minus Q1/Q2), percentage points"], rows,
               [f"Both arms were prefiltered and classified with the identical v1 prompt; Q3 arm n={u.v('COR-Q3-N')} records with a valid "
                f"stance. {BOOTN}. Q3 trend: Spearman ρ {u.v('RES-TMP-Q3-CRIT-RHO')}; {u.v('RES-TMP-Q3-CRIT-OR')}. Small Q3 annual counts "
                f"give wide intervals. Plotted in {{{{F:q3_fig}}}}. {CRIT} {FAV}"], group_rows=groups)


def t_run_to_run():
    u = U("run_to_run")
    rows = [["Records (both runs valid)", "300/300 (0 FAILED)"], ["Raw agreement", u.v("VAL-ST-RTR-RAW")],
            ["Quadratic-weighted Cohen κ", u.v("VAL-ST-RTR-QK")], ["Labels shifted", u.v("VAL-ST-RTR-SHIFT")]]
    table_unit(u, "Run-to-run stability of the stance classifier at the provider-default temperature (unchanged).",
               ["Metric", "Value"], rows,
               ["The 300 stance-validation records were classified twice more with the production v1 configuration. Agreement is between the "
                "two re-inference runs, not against human coding; canonical labels and human codes were not altered. CIs: bootstrap over "
                "records (1000, seed 42) for κ; Clopper-Pearson for raw agreement (CIs added in R1)."])


def _parse_old_table(tag, next_tag):
    txt = (R1 / "inputs" / "Multimedia Appendix 3. Supplementary Tables S1 to S18..txt").read_text(encoding="utf-8")
    heads = {"S16": "Table S16. The 18", "S17": "Table S17. Mapping", "S18": "Table S18. Human"}
    blk = txt[txt.index(heads[tag]):txt.index(heads[next_tag])]
    return [l.strip() for l in blk.split("\n")]


def t_specialty_definitions():
    u = U("specialty_definitions")
    L = _parse_old_table("S16", "S17")
    i = L.index("n") + 1
    rows = []
    from analysis.run_specialty_aiadoption import ALL_SPECIALTIES
    while L[i] != "Total":
        if L[i] == "":
            i += 1
            continue
        num_, cat, defn, _old_n = L[i:i + 4]
        full = ALL_SPECIALTIES[int(num_) - 1]
        rows.append([num_, cat, defn, fn(u.n(f"RES-SPC-OBS-{slug(full)}")["n"])])
        i += 4
    rows.append(["", "Total", "", fn(u.n("COR-SUB-08")["point"])])
    table_unit(u, "The 18 specialty and domain categories with the verbatim definitions used in the classification prompt.",
               ["#", "Category (as in figures)", "Verbatim definition text from SPECIALTY_PROMPT", "Records, 2021-2025, n"], rows,
               ["Definitions are reproduced exactly as in the submitted Table S16 (from analysis/classify_specialty.py), including the "
                "disambiguation rules. The final column is updated to the 2021-2025 analytic corpus (records with a valid specialty label); "
                "the submitted column counted the retired 2021-April 2026 set."], landscape=True)


def t_fda_mapping():
    u = U("fda_mapping")
    L = _parse_old_table("S17", "S18")
    i = L.index("Structural zero?") + 1
    rows = []
    from analysis.run_specialty_aiadoption import ALL_SPECIALTIES
    while L[i].strip() != "Total":
        cat, panels, cnt, flag = L[i:i + 4]
        assert int(cnt.replace(",", "")) == int(u.n(f"RES-SPC-FDA-{slug(cat)}")["point"]), cat
        rows.append([cat, panels, fn(int(cnt.replace(",", ""))), flag.strip()])
        i += 4
    rows.append(["Total", "", fn(sum(int(r[2].replace(",", "")) for r in rows)), ""])
    table_unit(u, "Mapping of FDA lead review panels to the 18 specialty and domain categories (unchanged).",
               ["Specialty category", "Mapped FDA lead review panel(s)", "Cleared-device count", "Structural zero?"], rows,
               ["Cleared-device counts from the FDA list of AI/ML-enabled medical devices cleared 1995-2025 (accessed 2 June 2026). A "
                "structural zero means that no FDA review panel maps to the category; it does not indicate an absence of clinically "
                "available AI in that field. Counts are not corpus-dependent and are unchanged from the submission."])


def t_stance_confusion():
    u = U("stance_confusion")
    S = rc.STANCES
    rows, groups = [], []
    for tag, lab in (("225", "(a) In-scope records (n=225)"), ("300", "(b) All 300 validation records")):
        groups.append(len(rows)); rows.append([lab])
        for h in S:
            cells = [int(u.n(f"VAL-ST-CM{tag}-{slug(h)}-{slug(m)}")["point"]) for m in S]
            rows.append([f"Human: {h}"] + [str(c) for c in cells] + [str(sum(cells))])
    groups.append(len(rows)); rows.append(["(c) Per-class agreement, in-scope records (n=225)"])
    for h in S:
        rows.append([h, u.v(f"VAL-ST-S18C-{slug(h)}"), "", "", "", "", ""])
    groups.append(len(rows)); rows.append(["(d) Per-class precision, recall and F1 (95% CI), in-scope records (n=225)"])
    for h in S:
        rows.append([h, u.v(f"VAL-ST-F1-{slug(h)}-225"), "", "", "", "", ""])
    rows.append(["Macro-F1", u.v("VAL-ST-MACROF1-225"), "", "", "", "", ""])
    table_unit(u, "Human versus model stance labels in the validation sample, with per-class agreement.",
               ["Human code \\ model label", "Alarm", "Caution", "Neutral", "Cautious Optimism", "Advocacy", "Row total"], rows,
               ["Rows give the human code and columns the model label. In (b), records the coder judged not codable or out of scope are "
                "recorded as Neutral. In (c), adjacent means one step away on the ordered scale; boundary-crossing means the disagreement "
                "crossed the critical-favourable boundary (not defined for Neutral). (d): bootstrap CIs over records (1000, seed 42). "
                f"Overall: quadratic-weighted κ {u.v('VAL-ST-QK-225')} (in scope) and {u.v('VAL-ST-QK-300')} (all 300). The validation "
                "sample spans all publication years and was drawn from abstract-present records."], landscape=True, group_rows=groups)


def t_mechanism_confusion():
    u = U("mechanism_confusion")
    rows, groups = [], []
    for tag, lab, labs in (("FM", "(a) Failure mode (n=108)", ["confabulation", "misclassification", "both", "none_or_unclear"]),
                           ("MT", "(b) Model type (n=108)", ["generative", "discriminative", "both", "unclear"])):
        groups.append(len(rows)); rows.append([lab])
        for h in labs:
            cells = [int(u.n(f"VAL-CM-{tag}-{slug(h)[:10]}-{slug(m)[:10]}")["point"]) for m in labs]
            rows.append([f"Human: {h.replace('_', ' ')}"] + [str(c) for c in cells] + [str(sum(cells))])
    table_unit(u, "Human versus model labels for the two mechanism axes.",
               ["Human code \\ model label", "Column 1", "Column 2", "Column 3", "Column 4", "Row total"], rows,
               ["Columns follow the row order within each panel: (a) confabulation (reported as fabrication), misclassification (factual "
                "error), both, none or unclear; (b) generative, discriminative, both, unclear. 120 stratified critical records; 12 title-only "
                f"records excluded. Failure mode: Cohen κ {u.v('VAL-MX-FM-K')}, Gwet AC1 {u.v('VAL-MX-FM-AC1')}, raw agreement "
                f"{u.v('VAL-MX-FM-RAW')}, κ_max {u.v('VAL-MX-FM-KMAX')}. Model type: Cohen κ {u.v('VAL-MX-MT-K')}, Gwet AC1 "
                f"{u.v('VAL-MX-MT-AC1')}, raw agreement {u.v('VAL-MX-MT-RAW')}. Fabrication-involved disagreements (model yes, human no vs "
                f"the reverse): {u.v('VAL-MX-FABDIR')}."], group_rows=groups)


def t_prefilter_validation():
    u = U("prefilter_validation")
    rows, groups = [], []
    groups.append(len(rows)); rows.append(["(a) Development pilot (n=200): human (rows) vs model (columns)"])
    labs = ["human:discourse", "human:evaluative", "human:application"]
    cols = ["model:discourse", "model:evaluative", "model:application"]
    for h in labs:
        c = [int(u.n(f"VAL-CM-PF3-{slug(h)[:10]}-{slug(m)[:10]}")["point"]) for m in cols]
        rows.append([h.replace("human:", "Human: "), str(c[0]), str(c[1]), str(c[2]), str(sum(c))])
    for id_, lab in (("VAL-PF-PILOT-RAW", "3-class raw agreement"), ("VAL-PF-PILOT-K3", "3-class Cohen κ"),
                     ("VAL-PF-PILOT-SENSITIVITY", "KEEP sensitivity"), ("VAL-PF-PILOT-SPECIFICITY", "KEEP specificity"),
                     ("VAL-PF-PILOT-PPV", "PPV"), ("VAL-PF-PILOT-NPV", "NPV"), ("VAL-PF-PILOT-KAPPA", "KEEP/DROP Cohen κ"),
                     ("VAL-PF-PILOT-AC1", "KEEP/DROP Gwet AC1")):
        rows.append([lab, u.v(id_), "", "", ""])
    groups.append(len(rows)); rows.append(["(b) R1 audit design: frame and sample per stratum and year"])
    for st, lab in (("EX-F", "Excluded by production, kept by full-abstract re-run"), ("EX-S", "Excluded by both"),
                    ("RET", "Retained by production")):
        for y in Y5:
            rows.append([f"{lab}, {y}", u.v(f"VAL-PF-MAN-{st}-{y}"), "", "", ""])
    rows.append(["Pilot records recoded (intra-rater)", u.v("VAL-PF-MAN-PILOT-any"), "", "", ""])
    groups.append(len(rows)); rows.append(["(c) R1 audit estimates by year (primary analysis; Jeffreys 95% CI)"])
    for y in Y5:
        rows.append([str(y), "1-NPV " + u.v(f"VAL-PF-AUDIT-FNRATE{y}"), "missed " + u.v(f"VAL-PF-AUDIT-MISSED{y}"),
                     "PPV among retained " + u.v(f"VAL-PF-CELL-PRIMARY-RET-{y}-PR"),
                     "full-abstract precision " + u.v(f"VAL-PF-CELL-PRIMARY-EX-F-{y}-FA")])
    groups.append(len(rows)); rows.append(["(d) Population-weighted 2x2, production prefilter vs full-abstract re-run"])
    for m, lab in (("SENSITIVITY", "Sensitivity"), ("SPECIFICITY", "Specificity"), ("PPV", "PPV"), ("NPV", "NPV"), ("KAPPA", "Cohen κ")):
        rows.append([lab, "production " + u.v(f"VAL-PF-AUDIT-PROD2X2{m}"), "full abstract " + u.v(f"VAL-PF-AUDIT-FULL2X2{m}"), "", ""])
    rows.append(["Gwet AC1", "production " + u.v("VAL-PF-AUDIT-PROD2X2AC1"), "", "", ""])
    groups.append(len(rows)); rows.append(["(e) Borderline sensitivity variants (Jeffreys 95% CI)"])
    for var, lab in (("BORDERLINEAPPLICATION", "Borderline coded as application"), ("BORDERLINEKEEP", "Borderline coded as KEEP")):
        rows.append([lab, "1-NPV " + u.v(f"VAL-PF-VAR-{var}-FNRATEPOOLED"), "missed " + u.v(f"VAL-PF-VAR-{var}-MISSEDTOTAL"),
                     "sensitivity " + u.v(f"VAL-PF-VAR-{var}-PROD2X2SENSITIVITY"), "κ " + u.v(f"VAL-PF-VAR-{var}-PROD2X2KAPPA")])
    groups.append(len(rows)); rows.append(["(f) Intra-rater agreement (20 pilot records recoded)"])
    rows.append(["KEEP/DROP", u.v("VAL-PF-INTRA-AGREE"), "κ " + u.v("VAL-PF-INTRA-K"), "", ""])
    rows.append(["3 classes", u.v("VAL-PF-INTRA-AGREE3"), "", "", ""])
    table_unit(u, "Validation of the AI-engagement prefilter: development pilot and R1 audit.",
               ["Item", "Value 1", "Value 2", "Value 3", "Value 4"], rows,
               ["(a) Pilot: sampling undocumented, unweighted, no written codebook; bootstrap CIs over records (1000, seed 42). (b-f) R1 audit "
                "(frozen protocol, Multimedia Appendix 1, Note 9): KEEP = discourse or evaluative. Estimates are weighted by frame size / "
                "sample size per stratum-year cell; Jeffreys intervals from 10,000 draws of each cell's Beta(k+1/2, n-k+1/2) posterior (seed "
                "42; Amendment 3); single cells use the exact Clopper-Pearson interval. The full-abstract 2x2 uses the within-cell bootstrap "
                "because its sub-cells are too small for the Jeffreys prior (Amendment 3). The one unlabelled record counts as an error of the "
                "classifier being evaluated (Amendment 2). The intra-rater κ interval is wide because only 1 of 20 records disagreed."],
               landscape=True, group_rows=groups)


def t_theme_validation():
    u = U("theme_validation")
    rows, groups = [], []
    for tag, lab in (("200", "Primary analysis, all 200 sampled records (Amendment 1)"), ("187", "Pre-specified analysis, 187 records with at least one human theme")):
        groups.append(len(rows)); rows.append([lab])
        for th in rc.THEMES:
            p_ = lambda nm: u.n(f"VAL-TH-PT-{tag}-{slug(th)}-{slug(nm)}")
            pr, rc_, f1 = p_("precision (unweighted)"), p_("recall (unweighted)"), p_("F1 (unweighted)")
            f1w = p_("F1 (weighted)")
            flag = " (insufficient support)" if "insufficient" in f1["item"] else ""
            rows.append([th + flag, u.v(f"VAL-TH-PT-{tag}-{slug(th)}-SUPPORT"), cic(pr["point"], pr["lo"], pr["hi"], 3),
                         cic(rc_["point"], rc_["lo"], rc_["hi"], 3), cic(f1["point"], f1["lo"], f1["hi"], 3),
                         cic(f1w["point"], f1w["lo"], f1w["hi"], 3)])
        rows.append(["Micro-F1 (unweighted / weighted)", "", "", "", u.v(f"VAL-TH-MICRO-{tag}-UN"), u.v(f"VAL-TH-MICRO-{tag}-WE")])
        rows.append(["Macro-F1 (unweighted / weighted)", "", "", "", u.v(f"VAL-TH-MACRO-{tag}-UN"), u.v(f"VAL-TH-MACRO-{tag}-WE")])
    table_unit(u, "Validation of the concern-theme classifier, per theme.",
               ["Theme", "Human-positive records, n", "Precision (95% CI)", "Recall (95% CI)", "F1, unweighted (95% CI)",
                "F1, frame-weighted (95% CI)"], rows,
               ["200 critical records 2021-2025, 40 per year by simple random sampling within year; codebook verbatim from the classifier "
                "prompt; one coder blinded to model labels (frozen protocol, Multimedia Appendix 1, Note 9). Set-based comparison per record. "
                "Weighted: each record weighted by frame size / sample size of its year. CIs: percentile bootstrap within year (1000, seed "
                "42). Insufficient support: fewer than 10 human-positive records. In the primary analysis the 13 records with no human "
                "theme count as empty sets, so every model theme on them is a false positive (Amendment 1, made after the pre-specified "
                "analysis had been run)."], landscape=True, group_rows=groups)


def t_regression_full():
    u = U("regression_full")
    rows, groups = [], []
    groups.append(len(rows)); rows.append(["(a) Primary model, critical stance: see Table 2 for every level; year effect"])
    rows.append(["Year, per 1 year", u.v("RES-REG-YEAR-UOR"), u.v("RES-TMP-CRIT-AOR"), ""])
    groups.append(len(rows)); rows.append(["(b) Advocacy model (secondary 2): adjusted OR (95% CI), P"])
    for k in [k for k in BOOK if k.startswith("RES-REGADV-") and k != "RES-REGADV-HEADER"]:
        x = u.n(k)
        rows.append([x["item"].replace(": adjusted OR", ""), x["value"], "", ""])
    groups.append(len(rows)); rows.append(["(c) Ordinal model (secondary 1): ordinal OR (95% CI), P; cut-point ORs; proportional-odds check"])
    for k in [k for k in BOOK if k.startswith("RES-REGORD-") and k != "RES-REGORD-HEADER"]:
        x = u.n(k)
        a, b = x["value"].split("; cut-point ORs ")
        cp, chk = b.split("; check: ")
        rows.append([x["item"].split(": ordinal")[0], a, cp, chk])
    groups.append(len(rows)); rows.append(["(d) Sensitivity models S1-S4, critical stance: adjusted OR (95% CI), P"])
    for k in [k for k in BOOK if k.startswith("RES-REGSEN-")]:
        x = u.n(k)
        rows.append([x["item"].replace(": adjusted OR", ""), x["value"], "", ""])
    table_unit(u, "Multivariable models in full: Advocacy model, ordinal model and sensitivity models S1 to S4, 2021-2025.",
               ["Model: variable: level", "Estimate", "Cut-point ORs (ordinal model)", "Proportional-odds check"], rows,
               [f"{u.v('RES-REG-HEADER')}. {u.v('RES-REGADV-HEADER')}. {u.v('RES-REGORD-HEADER')}. Proportional odds was judged violated when a "
                f"cut-point coefficient fell outside the ordinal coefficient's CI or changed sign; {u.v('RES-SEN-B4-PO')}. S1: year as "
                "categories (reference 2021). S2: adds January-April 2026 as a year level (n=16,747; the only model that uses 2026 records). "
                f"S3: journal fixed effects ({u.v('RES-SEN-B4S3-N')}). S4: first-author country levels with at least 100 records (reference "
                "United States) instead of region. Reference levels and covariates as in Table 2. All SEs cluster-robust by journal."],
               landscape=True, group_rows=groups)


def t_corpus_sensitivity():
    u = U("corpus_sensitivity")
    rows, groups = [], []
    groups.append(len(rows)); rows.append(["(a) Stance of recovered vs retained records, 2021-2025: % (95% CI); n/N"])
    for s in rc.STANCES + ["Critical"]:
        rows.append([s, share(u, f"RES-B2RR-{slug('Retained (production corpus)')[:8]}-{slug(s)}"),
                     share(u, f"RES-B2RR-{slug('Recovered (B2)')[:8]}-{slug(s)}"), "", ""])
    groups.append(len(rows)); rows.append(["(b) Annual critical share by corpus: % (95% CI); n/N"])
    for y in Y5:
        rows.append([str(y)] + [share(u, f"RES-B2ANN-{c}-CRITICAL-{y}") if c != "C" else u.v(f"RES-B2ANN-C-CRITICAL-{y}")
                                for c in "ABCD"])
    groups.append(len(rows)); rows.append(["(c) Annual Advocacy share by corpus: % (95% CI); n/N"])
    for y in Y5:
        rows.append([str(y)] + [share(u, f"RES-B2ANN-{c}-ADVOCACY-{y}") if c != "C" else u.v(f"RES-B2ANN-C-ADVOCACY-{y}")
                                for c in "ABCD"])
    groups.append(len(rows)); rows.append(["(d) Trend by corpus"])
    for o in ("CRITICAL", "ADVOCACY"):
        rows.append([o.capitalize()] + [u.v(f"RES-SEN-B2{c}-{o}").split("; ", 1)[1] for c in "ABCD"])
    table_unit(u, "Sensitivity of stance trends to the prefilter: recovered records and alternative corpora (B2), 2021-2025.",
               ["Item", "(a) Production corpus", "(b) Augmented corpus", "(c) Precision-weighted augmented", "(d) Full-abstract corpus"],
               rows,
               [f"Recovered records: {u.v('RES-SEN-B2-FRAME')} records (all years) that the production prefilter labelled application but the "
                f"full-abstract re-run labelled discourse or evaluative, stance-classified with the production v1 configuration; "
                f"{u.v('RES-SEN-B2-FAILED')} stayed FAILED after one resubmission and {u.v('RES-SEN-B2-RECOVERED')} with a valid stance are "
                "dated 2021-2025. In (a), columns 2 and 3 are retained and recovered records. Corpora: (a) production; (b) production plus "
                "recovered; (c) as (b) with recovered records weighted by the audit's full-abstract precision for their year; (d) the "
                f"full-abstract prefilter's corpus (adds recovered records, drops {u.v('RES-SEN-B2-DROPPED')} production records whose "
                f"full-abstract label is application). {BOOTN}, joint resampling; (c) uses a frequency-weighted logistic model with HC0 SEs. "
                f"Plotted in {{{{F:temporal_robustness_fig}}}}. {CRIT}"], landscape=True, group_rows=groups)


def t_symmetric():
    u = U("symmetric_endorsement")
    rows, groups = [], []
    groups.append(len(rows)); rows.append(["(a) Symmetric scale, 2021-2025"])
    for k in [k for k in BOOK if k.startswith("RES-B3SYM-")]:
        x = u.n(k)
        rows.append([x["item"].split(": ", 1)[1], x["value"], "", ""])
    groups.append(len(rows)); rows.append(["(b) Annual share among all records: % (95% CI); n/N"])
    for y in Y5:
        rows.append([str(y), share(u, f"RES-TMP-SE-{y}"), share(u, f"RES-TMP-SEUB-{y}"), share(u, f"RES-TMP-ADV-{y}")])
    rows.append(["Spearman ρ (exact P)", u.v("RES-TMP-SE-RHO"), u.v("RES-TMP-SEUB-RHO"), u.v("RES-TMP-ADV-RHO")])
    rows.append(["OR per year (95% CI), P", u.v("RES-TMP-SE-OR"), u.v("RES-TMP-SEUB-OR"), u.v("RES-TMP-ADV-OR")])
    groups.append(len(rows)); rows.append(["(c) Consistency with production labels, 2021-2025"])
    rows.append(["Production Advocacy flagged strong endorsement", u.v("RES-SEN-B3-CONS-ADVOCACY"), "", ""])
    rows.append(["Production Cautious Optimism flagged strong endorsement", u.v("RES-SEN-B3-CONS-CAUTIOUSOPTIMISM"), "", ""])
    groups.append(len(rows)); rows.append(["(d) Agreement of the flag with human Advocacy (model-favourable validation records)"])
    for tag, lab in (("ALL", "All model-favourable records (n=130)"), ("INSCOPE", "In-scope records (n=112)")):
        rows.append([lab, "sensitivity " + u.v(f"VAL-B3-{tag}-SENSITIVITY"), "PPV " + u.v(f"VAL-B3-{tag}-PPV"),
                     "Cohen κ " + u.v(f"VAL-B3-{tag}-COHEN")])
    groups.append(len(rows)); rows.append(["(e) Misclassification-corrected human-Advocacy prevalence (secondary)"])
    for y in Y5:
        rows.append([str(y), u.v(f"RES-SEN-B3-CORR-{y}"), "", ""])
    table_unit(u, "Symmetric endorsement scale: re-classification of favourable records for strong endorsement (B3), 2021-2025.",
               ["Item", "Strong endorsement (flag yes)", "Upper bound (FAILED counted as yes)", "Production Advocacy"], rows,
               ["Every favourable record (production Cautious Optimism or Advocacy) was re-classified for 'strong endorsement' with a prompt "
                "that keeps the Advocacy endorsement criterion but drops the transformative-language requirement (verbatim in Multimedia "
                "Appendix 1, Note 8); Claude Sonnet 4.6, temperature 0. FAILED records (model prose before the JSON) stay in the denominators. "
                f"{BOOTN}. (c) exact Clopper-Pearson CIs. (e) stratified estimator with strata = model stance x flag and P(human Advocacy | "
                "stratum) from the 300 validation records. Favourable stance was Cautious Optimism or Advocacy."],
               landscape=True, group_rows=groups)


def t_sjr():
    u = U("sjr_sensitivity")
    defs = [("FULL", "Full corpus"), ("D1", "D1"), ("D2", "D2"), ("D3", "D3")]
    items = {}
    for k in [k for k in BOOK if k.startswith("RES-B5X-")]:
        code = k.split("-")[2]
        x = BOOK[k]
        sec, it = x["item"].split(": ", 2)[1:3]
        items.setdefault((sec, it), {})[code] = k
    rows, groups = [], []
    cur = None
    for (sec, it), m in items.items():
        if sec != cur:
            cur = sec; groups.append(len(rows)); rows.append([sec])
        rows.append([it] + [u.v(m[c]) if c in m else D for c, _ in defs])
    groups.append(len(rows)); rows.append(["Records removed from 2021-2025"])
    rows.append(["Removed (of 14,058)", D] + [u.v(f"RES-SEN-B5{c}-REMOVED") for c in ("D1", "D2", "D3")])
    table_unit(u, "Sensitivity of the main estimates to an SJR medical-category restriction (B5), 2021-2025.",
               ["Item", "Full corpus", "D1 Medicine area (primary)", "D2 D1 minus Medicine (miscellaneous)", "D3 broad health sciences"],
               rows,
               ["A record is kept only if its journal-year is Q1/Q2 in at least one SCImago category of the definition. D1 (primary): any "
                "Medicine-area (ASJC 27xx) category. D2: D1 without 'Medicine (miscellaneous)'. D3: broad health sciences (Medicine, Nursing, "
                f"Dentistry, Health Professions, Neuroscience, Pharmacology, Immunology and Microbiology, Psychology). {BOOTN}. Trend: Spearman "
                f"ρ (exact P) over 5 annual values and OR per year. Annual series are plotted in {{{{F:temporal_robustness_fig}}}}. {CRIT}"],
               landscape=True, group_rows=groups)


def t_lexicon():
    u = U("lexicon_and_terms")
    rows, groups = [], []
    groups.append(len(rows)); rows.append(["(a) MeSH and author-keyword completeness by year"])
    for y in Y5:
        rows.append([str(y), u.v(f"RES-B6-COMP-{y}"), "", ""])
    groups.append(len(rows)); rows.append(["(b) Lexicon mention share vs LLM theme prevalence among critical records"])
    lex = {"Patient safety": "PATIENTSAFETY", "Hallucination / errors": "HALLUCINATIONERRORS",
           "Governance / regulation": "GOVERNANCEREGULATION", "Ethics & bias": "ETHICSANDBIAS"}
    for t in HEADLINE_THEMES:
        s_ = slug(t)
        rows.append([t, f"lexicon {u.v(f'RES-THM-LEX-{s_}-RHO')}; {u.v(f'RES-THM-LEX-{s_}-OR')}",
                     f"LLM {u.v(f'RES-TMP-TH-{s_}-RHO')}; {u.v(f'RES-TMP-TH-{s_}-OR')}", "same direction: " + u.v(f"RES-THM-LEX-{s_}-DIR")])
    for tag, lab in (("EMERG", "(c) Terms most over-represented in 2024-2025 vs 2021-2022 (top 30)"),
                     ("STANCE", "(d) Terms most over-represented in critical vs favourable records (top 30)")):
        groups.append(len(rows)); rows.append([lab])
        for i in range(1, 31):
            id_ = f"RES-B6-{tag}-{i:02d}"
            if id_ in BOOK:
                x = u.n(id_)
                rows.append([x["item"].split(": ", 1)[1], *x["value"].split("; ")[:3]])
    table_unit(u, "MeSH and keyword triangulation of the theme trends (B6), 2021-2025.",
               ["Item", "Value 1", "Value 2", "Value 3"], rows,
               ["MeSH terms and author keywords were re-fetched from PubMed for the analytic records (Multimedia Appendix 1, Note 10). (b) "
                "Lexicon: pre-specified term lists matched to MeSH, keywords, title and abstract (verbatim in Note 10); LLM: concern-theme "
                "classifier. Both measured among critical records; trends are Spearman ρ (exact P) over 5 annual values and OR per year. "
                "(c-d) Weighted log-odds ratio with an informative Dirichlet prior (Monroe et al. 2008; prior from all retained records, "
                "α0=1000; terms in at least 20 records); z is the log-odds difference divided by its SE; records = documents containing the "
                f"term in each group. Plotted in {{{{F:lexicon_vs_llm_fig}}}} and {{{{F:terms_fig}}}}. {CRIT}"], landscape=True, group_rows=groups)


def t_missing():
    u = U("missing_data")
    rows, groups = [], []
    groups.append(len(rows)); rows.append(["(a) Records lost at each stage, records dated 2021-2025"])
    for k in [k for k in BOOK if re.match(r"MIS-\d\d$", k)]:
        x = u.n(k)
        rows.append([x["item"], x["value"]])
    groups.append(len(rows)); rows.append(["(b) Title-only (empty abstract) records at each stage, 2021-2025"])
    for k in [k for k in BOOK if k.startswith("MIS-TO-")]:
        x = u.n(k)
        rows.append([x["item"], x["value"]])
    groups.append(len(rows)); rows.append(["(c) Missing values in the analytic corpus (n=14,058)"])
    for k in ("COR-SUB-03", "COR-SUB-05", "COR-SUB-09", "COR-SUB-11", "COR-SUB-12", "COR-SUB-14", "COR-SUB-15"):
        x = u.n(k)
        rows.append([x["item"], x["value"]])
    rows.append(["Handling", u.v("MIS-NOTE-01")])
    table_unit(u, "Missing-data accounting for the 2021-2025 analytic corpus.", ["Stage or variable", "Records, n (by year)"], rows,
               ["Counts are restricted to records dated 2021-2025 (year as the first four-digit year in the PubMed date). Stage losses "
                "that are exclusions by design (for example, application records at the prefilter) are listed with the reasons in "
                "Figure 1. Title-only records were classified from the title alone except in the mechanism analyses, which used "
                "abstract-present records only."], group_rows=groups)


def t_precision():
    u = U("precision")
    rows, groups = [], []
    rows.append(["Design", u.v("PRE-00")])
    rows.append(["All records", u.v("PRE-ALL")])
    for pre, lab in (("PRE-YR-", "By year"), ("PRE-SPC-", "By specialty or domain category"), ("PRE-REG-", "By first-author region"),
                     ("PRE-PT-", "By publication type")):
        groups.append(len(rows)); rows.append([lab])
        for k in [k for k in BOOK if k.startswith(pre)]:
            x = u.n(k)
            rows.append([x["item"].replace(": n and half-width", ""), x["value"]])
    table_unit(u, "Sample size and precision of the critical-share estimates, 2021-2025.", ["Group", "n; 95% CI half-width"], rows,
               [f"Half-width = half the width of the 95% percentile bootstrap CI (1000 resamples, seed 42), in percentage points. {CRIT}"],
               group_rows=groups)


def t_advocacy_by_specialty():
    u = U("advocacy_by_specialty")
    rows = []
    for k in [k for k in BOOK if k.startswith("RES-ADVSP-") and not k.startswith("RES-ADVSP-TOTAL")]:
        x = u.n(k)
        a, b = x["value"].split("; 2025: ")
        rows.append([x["item"].split(":")[0].replace("FAILED", "Specialty FAILED"), a.replace("2021: ", ""), b])
    table_unit(u, "Advocacy records by specialty or domain category, 2021 and 2025.",
               ["Specialty", "2021: n (% of all Advocacy; % of records in the category)", "2025: n (% of all Advocacy; % of records in the category)"],
               rows,
               [f"Advocacy records: 2021 n={u.v('RES-ADVSP-TOTAL-2021')}; 2025 n={u.v('RES-ADVSP-TOTAL-2025')}. Counts and shares only; with "
                "few Advocacy records per category, category-level shares are imprecise."])


# =====================================================================
# MA2 figure units
# =====================================================================
def _series(ax, u, prefix, colour, label, ymax=None, marker="o", offset=0.0, show=True, below=False):
    pts = [u.n(f"{prefix}-{y}") for y in Y5]
    p = np.array([x["point"] for x in pts]); lo = np.array([x["lo"] for x in pts]); hi = np.array([x["hi"] for x in pts])
    xs = np.array(Y5) + offset
    ax.errorbar(xs, p, yerr=[p - lo, hi - p], fmt="-" + marker, color=colour, ms=3, lw=1.0, elinewidth=0.6, capsize=1.6, label=label)
    if show:
        top = ymax or max(hi) * 1.3
        for x, v_, h, l_ in zip(xs, p, hi, lo):
            if below:
                ax.text(x, l_ - top * 0.02, f"{v_:.1f}", ha="center", va="top", fontsize=7, color=colour)
            else:
                ax.text(x, h + top * 0.02, f"{v_:.1f}", ha="center", va="bottom", fontsize=7, color=colour)
    return p


def f_within_genre():
    u = U("within_genre_fig")
    fig, ax = plt.subplots(figsize=(W_IN * 0.62, 3.0))
    _series(ax, u, "RES-TMP-GENDISC", "#0072B2", "Discourse records", ymax=50, offset=-0.06)
    _series(ax, u, "RES-TMP-GENEVAL", "#D55E00", "Evaluative records", ymax=50, marker="s", offset=0.06)
    ax.set_ylim(0, 50); ax.set_xticks(Y5); ax.set_ylabel("Critical stance, % of records in the genre"); ax.legend(frameon=False, loc="lower right")
    ax.grid(axis="y", lw=0.3, color="#DDDDDD")
    fig.tight_layout()
    fig_save(u, fig, "**Annual critical share within each prefilter genre, 2021-2025.** Points show the critical share within discourse "
             "and within evaluative records; whiskers show 95% percentile bootstrap CIs (1000 resamples, deterministic seed 42 + cell index); "
             f"printed values are the point estimates (%). Discourse: {u.v('RES-TMP-GENDISC-RHO')}, {u.v('RES-TMP-GENDISC-OR')}; evaluative: "
             f"{u.v('RES-TMP-GENEVAL-RHO')}, {u.v('RES-TMP-GENEVAL-OR')} (Spearman ρ with exact P; record-level logistic OR per year). "
             "Annual n's and the discourse:evaluative ratio are in {{T:within_genre}}. Critical stance was Alarm or Caution.")


def f_other_themes():
    u = U("other_themes_fig")
    others = [t for t in rc.THEMES if rc.THEME_LABELS[t] not in HEADLINE_THEMES]
    cols = ["#CC79A7", "#56B4E9", "#E69F00", "#009E73", "#0072B2", "#999999"]
    fig, axes = plt.subplots(2, 3, figsize=(W_IN, 4.4))
    for ax, t, c in zip(axes.flat, others, cols):
        lab = rc.THEME_LABELS[t]
        _series(ax, u, f"RES-TMP-TH-{slug(lab)}", c, lab, ymax=18)
        ax.set_ylim(0, 18); ax.set_xticks(Y5); ax.set_xticklabels([str(y) for y in Y5], rotation=45)
        ax.text(0.03, 0.97, lab, transform=ax.transAxes, va="top", fontweight="bold")
        ax.grid(axis="y", lw=0.3, color="#DDDDDD")
    for ax in axes[:, 0]:
        ax.set_ylabel("% of critical records")
    fig.tight_layout()
    stats = "; ".join(f"{rc.THEME_LABELS[t]} {u.v(f'RES-TMP-TH-{slug(rc.THEME_LABELS[t])}-RHO')}, {u.v(f'RES-TMP-TH-{slug(rc.THEME_LABELS[t])}-OR')}"
                      for t in others)
    fig_save(u, fig, "**The six lower-prevalence concern themes among critical records, 2021-2025.** Annual prevalence among critical "
             f"records ({fn(u.n('COR-SUB-01')['point'])} in total; per-year n in Figure 2); points with 95% percentile bootstrap CIs (1000 "
             f"resamples, seed 42) and printed point estimates (%). Themes were multilabel. Trend statistics: {stats}. Pooled prevalences are "
             "in {{T:themes}}. Critical stance was Alarm or Caution.")


def f_theme_counts():
    u = U("theme_counts_fig")
    fig, axes = plt.subplots(2, 5, figsize=(W_IN, 5.4))
    for ax, t in zip(axes.flat, rc.THEMES):
        lab = rc.THEME_LABELS[t]
        cnt = [u.n(f"RES-THM-COUNT-{slug(lab)}-{y}")["point"] for y in Y5]
        shr = [u.n(f"RES-TMP-TH-{slug(lab)}-{y}")["point"] for y in Y5]
        ax.bar(Y5, cnt, color="#BBBBBB", width=0.6)
        for x, c in zip(Y5, cnt):
            ax.text(x, c + max(cnt) * 0.03, f"{int(c)}", ha="center", va="bottom", fontsize=7, rotation=90)
        ax.set_ylim(0, max(cnt) * 2.3); ax.set_xticks(Y5); ax.set_xticklabels([str(y)[2:] for y in Y5])
        a2 = ax.twinx(); a2.plot(Y5, shr, "-o", color="#0072B2", ms=2.5, lw=0.9)
        lo_, hi_ = min(shr), max(shr); span = max(hi_ - lo_, 2.0)
        a2.set_ylim(lo_ - span * 1.9, hi_ + span * 0.75)
        for x, s_ in zip(Y5, shr):
            a2.text(x, s_ + span * 0.12, f"{s_:.1f}", ha="center", va="bottom", fontsize=7, color="#0072B2", rotation=90)
        a2.spines["right"].set_visible(True); a2.spines["top"].set_visible(False)
        tk = [t_ for t_ in a2.get_yticks() if max(0.0, lo_ - span * 0.6) <= t_ <= hi_ + span * 0.75]
        a2.set_yticks(tk); a2.spines["right"].set_bounds(min(tk), max(tk))
        a2.tick_params(axis="y", colors="#0072B2")
        ax.text(0.02, 1.02, lab, transform=ax.transAxes, fontweight="bold", va="bottom")
        if ax in axes[:, 0]:
            ax.set_ylabel("Records with the theme, n")
        if ax in axes[:, -1]:
            a2.set_ylabel("% of critical records", color="#0072B2")
    fig.tight_layout(h_pad=1.5)
    fig_save(u, fig, "**Annual count and prevalence share of the ten concern themes, 2021-2025.** Grey bars (left axis): number of critical "
             "records assigned the theme each year (printed above each bar). Blue line (right axis): prevalence among critical records "
             "(printed, %), drawn in the upper part of each panel on its own scale. Two measures are shown per panel. Denominator per year: the critical records of that year (Figure 2). Themes "
             "were multilabel. CIs for the shares are in {{T:themes}} and the R1 numbers book. Critical stance was Alarm or Caution. Years "
             "are shown as two digits (21 = 2021).")


def f_generative_share():
    u = U("generative_share_fig")
    from analysis.run_specialty_aiadoption import ALL_SPECIALTIES
    fig, ax = plt.subplots(figsize=(W_IN, 3.8))
    SH = {"Radiology / Diagnostic Imaging": "Radiology", "Pathology / Laboratory Medicine": "Pathology", "Mental Health / Psychiatry": "Mental health",
          "Internal Medicine / Primary Care": "Internal medicine", "Emergency Medicine / Critical Care": "Emergency medicine",
          "Obstetrics / Gynecology": "Obstetrics/gynecology", "Medical Informatics / Digital Health": "Medical informatics",
          "Multidisciplinary / Other": "Multidisciplinary", "Neurology / Neuroscience": "Neurology", "Medical Education": "Medical education"}
    for s in ALL_SPECIALTIES:
        g_ = u.n(f"RES-SPC-GENSHARE-{slug(s)}"); c = u.n(f"RES-SPC-OBS-{slug(s)}")
        ax.scatter(g_["point"], c["point"], s=g_["n"] * 0.25 + 6, facecolor="#56B4E9", edgecolor="#333333", lw=0.5, alpha=0.9)
        # crowded cluster: labels in the empty right-hand area with leader lines (data coordinates)
        ABS = {"Dentistry": (80, 26.0), "Pediatrics": (80, 24.0), "Neurology / Neuroscience": (80, 22.0),
               "Internal Medicine / Primary Care": (80, 20.0), "Ophthalmology": (80, 18.0), "Oncology": (80, 16.0)}
        OFF = {"Radiology / Diagnostic Imaging": (-7, 0, "right"), "Pathology / Laboratory Medicine": (0, 9, "center"),
               "Obstetrics / Gynecology": (-5, 0, "right")}
        txt = f"{SH.get(s, s)} ({g_['point']:.1f}, {c['point']:.1f})"
        if s in ABS:
            ax.annotate(txt, (g_["point"], c["point"]), xytext=ABS[s], textcoords="data", fontsize=7, ha="left", va="center",
                        arrowprops=dict(arrowstyle="-", lw=0.4, color="#888888", shrinkA=0, shrinkB=4))
        else:
            dx, dy, ha = OFF.get(s, (5, 2, "left"))
            ax.annotate(txt, (g_["point"], c["point"]), xytext=(dx, dy), textcoords="offset points", fontsize=7, ha=ha, va="center")
    ax.set_xlabel("Generative-model share among abstract-present critical records, %"); ax.set_ylabel("Critical stance, % of records")
    ax.set_xlim(0, 105); ax.set_ylim(13, 53); ax.grid(lw=0.3, color="#EEEEEE")
    fig.tight_layout()
    fig_save(u, fig, "**Critical rate against generative-model share across the 18 specialty and domain categories, 2021-2025.** Each point is "
             "one category; point area is proportional to the number of abstract-present critical records in the category; labels give "
             "(generative-model share, critical rate) in %. Generative-model share is the proportion of a category's abstract-present "
             "critical records classified as generative or both, so it is computed among critical records only. Labels for a crowded "
             "cluster are set to the right with leader lines. No fitted line is shown. "
             f"Spearman correlation: {u.v('RES-SPC-GEN-RHO')}. Correlations involving the FDA count, including the partial correlation, are "
             "in {{T:fda_robustness}}. Critical stance was Alarm or Caution.")


def f_country_map_20():
    u = U("country_map_20")
    import geopandas  # noqa: F401
    from matplotlib.colors import TwoSlopeNorm
    from matplotlib.lines import Line2D
    from matplotlib.patches import Rectangle
    from analysis.run_country_critical_map import centroid_lookup, load_world_robinson
    world = load_world_robinson(); cen = centroid_lookup(world)
    sel = []
    for k in [k for k in BOOK if k.startswith("RES-GEO-CTY-")]:
        x = u.n(k)
        sel.append((x["item"].split(":")[0], x["point"], int(x["n"]), "20-49" in x["item"]))
    norm = TwoSlopeNorm(vmin=10, vcenter=u.n("RES-OVR-CRITICAL")["point"], vmax=55); cmap = plt.get_cmap("RdYlBu_r")
    SCALE = 0.32
    fig = plt.figure(figsize=(W_IN, 4.6))
    ax = fig.add_axes([0.0, 0.0, 0.9, 1.0])
    world.plot(ax=ax, color="#E6E6E6", edgecolor="white", linewidth=0.3)
    EU = (-1.05e6, 2.45e6, 3.85e6, 6.95e6)
    in_eu = lambda x, y: EU[0] <= x <= EU[1] and EU[2] <= y <= EU[3]
    ins = fig.add_axes([0.335, 0.02, 0.29, 0.5])
    world.plot(ax=ins, color="#E6E6E6", edgecolor="white", linewidth=0.3)
    ins.set_facecolor("white")
    for s_ in ins.spines.values():
        s_.set_visible(True); s_.set_linewidth(0.6); s_.set_color("#555555")
    POS_MAIN = {"Japan": "r", "South Korea": "a", "Taiwan": "r", "Hong Kong": "bl", "Saudi Arabia": "bl", "United Arab Emirates": "r",
                "Iran": "a", "Israel": "l", "Turkey": "a", "Canada": "a", "Singapore": "bl", "Brazil": "l", "Egypt": "bl", "Qatar": "a",
                "Malaysia": "r", "Thailand": "l", "Colombia": "l", "Chile": "r", "Norway": "a"}
    POS_IN = {"Netherlands": "a", "Belgium": "b", "Germany": "r", "United Kingdom": "b", "Ireland": "l", "Denmark": "a", "Sweden": "r",
              "Poland": "r", "Austria": "r", "Switzerland": "bl", "France": "l", "Italy": "r", "Romania": "r", "Greece": "b",
              "Spain": "b", "Portugal": "l", "Hungary": "b", "Finland": "r"}
    for name, p, n, low in sel:
        x, y = cen[name]
        for a in ([ax] + ([ins] if in_eu(x, y) else [])):
            a.scatter(x, y, s=SCALE * n, c=[p], cmap=cmap, norm=norm, edgecolor="black" if low else "#333333",
                      lw=1.0 if low else 0.4, linestyle=(0, (2, 1)) if low else "solid", zorder=3)
        tgt = ins if in_eu(x, y) else ax
        pos = (POS_IN if tgt is ins else POS_MAIN).get(name, "b")
        r_ = np.sqrt(SCALE * n) / 2 + 1.5
        dx = -r_ if "l" in pos else r_ if "r" in pos else 0
        dy = 0 if pos in ("l", "r") else (r_ if "a" in pos else -r_)
        tgt.annotate(f"{p:.1f}", (x, y), xytext=(dx, dy), textcoords="offset points", fontsize=7, zorder=6,
                     ha="right" if "l" in pos else "left" if "r" in pos else "center",
                     va="center" if pos in ("l", "r") else "bottom" if "a" in pos else "top")
    ax.set_axis_off(); ax.set_xlim(world.total_bounds[0], world.total_bounds[2]); ax.set_ylim(-6.3e6, 8.6e6)
    ax.add_patch(Rectangle((EU[0], EU[2]), EU[1] - EU[0], EU[3] - EU[2], fill=False, lw=0.6, ec="#555555"))
    ins.set_xlim(EU[0], EU[1]); ins.set_ylim(EU[2], EU[3]); ins.set_xticks([]); ins.set_yticks([])
    cax = fig.add_axes([0.915, 0.22, 0.018, 0.6])
    cb = fig.colorbar(plt.cm.ScalarMappable(cmap=cmap, norm=norm), cax=cax, extend="both"); cb.set_label("Critical stance, % of records")
    hs = [Line2D([0], [0], marker="o", color="none", markerfacecolor="#BBBBBB", markeredgecolor="#333333", markersize=np.sqrt(SCALE * n),
                 label=fn(n)) for n in (20, 500, 2000)]
    hs.append(Line2D([0], [0], marker="o", color="none", markerfacecolor="white", markeredgecolor="black", markersize=5, ls="none",
                     label="20-49 records (dashed outline)"))
    ax.legend(handles=hs, title="Records", loc="lower left", frameon=False, labelspacing=1.6, handletextpad=1.4, bbox_to_anchor=(0, 0.04))
    n_low = sum(1 for s in sel if s[3])
    fig_save(u, fig, f"**Critical rate by country of first authorship at the 20-record threshold, 2021-2025.** As Figure 5, but including all "
             f"{len(sel)} countries with at least 20 first-author records; the {n_low} countries with 20 to 49 records have a dashed outline "
             "and are low-confidence estimates. Bubble area is proportional to the number of records; fill colour and the printed value give "
             "the critical rate (%). Europe is enlarged in the inset, where its values are printed; some low-count countries overlap at "
             "map scale and their values are in {{T:country}}. Country indexes publication discourse, not national attitudes, research "
             "quality or AI capability. Critical stance was Alarm or Caution. Robinson projection.")


def f_q3():
    u = U("q3_fig")
    fig, (a, b) = plt.subplots(1, 2, figsize=(W_IN, 3.2), gridspec_kw={"width_ratios": [1.2, 1]})
    cats = rc.STANCES + ["Critical", "Favourable"]
    for i, s in enumerate(cats):
        for off, pre, col, mk in ((-0.15, "RES-OVR", "#0072B2", "o"), (0.15, "RES-Q3-POOLED", "#D55E00", "s")):
            x = u.n(f"{pre}-{slug(s)}")
            a.errorbar(i + off, x["point"], yerr=[[x["point"] - x["lo"]], [x["hi"] - x["point"]]], fmt=mk, color=col, ms=3, elinewidth=0.6,
                       capsize=1.5)
            a.text(i + off, x["hi"] + 1.5, f"{x['point']:.1f}", ha="center", va="bottom", fontsize=7, color=col, rotation=90)
    a.set_xticks(range(len(cats))); a.set_xticklabels(["Alarm", "Caution", "Neutral", "Cautious\nOptimism", "Advocacy", "Critical", "Favourable"])
    a.set_ylim(0, 95); a.set_ylabel("% of records"); a.grid(axis="y", lw=0.3, color="#DDDDDD")
    a.plot([], [], "o", color="#0072B2", label="Q1/Q2"); a.plot([], [], "s", color="#D55E00", label="Q3"); a.legend(frameon=False, loc="upper left")
    _series(b, u, "RES-TMP-CRIT", "#0072B2", "Q1/Q2", ymax=50, offset=-0.07, below=True)
    _series(b, u, "RES-TMP-Q3-CRIT", "#D55E00", "Q3", ymax=50, marker="s", offset=0.07)
    b.set_ylim(0, 55); b.set_xticks(Y5); b.set_ylabel("Critical stance, % of records"); b.legend(frameon=False, loc="lower right")
    b.grid(axis="y", lw=0.3, color="#DDDDDD")
    a.text(-0.12, 1.02, "a", transform=a.transAxes, fontweight="bold", fontsize=9); b.text(-0.14, 1.02, "b", transform=b.transAxes, fontweight="bold", fontsize=9)
    fig.tight_layout()
    fig_save(u, fig, "**Stance in the Q1/Q2 analytic corpus and the Q3 comparison arm, 2021-2025.** (a) Pooled 2021-2025 stance distribution "
             f"for the Q1/Q2 corpus (n=14,058) and the Q3 arm (n={u.v('COR-Q3-N')}), both classified with the identical v1 prompt. (b) Annual "
             "critical share by quartile tier. Points show estimates and whiskers 95% percentile bootstrap CIs (1000 resamples, seed 42); "
             "printed values are point estimates (%). Small Q3 annual counts give wide intervals; values and n/N are in {{T:q3_arm}}. "
             "Critical stance was Alarm or Caution; favourable stance was Cautious Optimism or Advocacy.")


def f_sankey():
    u = U("forward_validation_sankey")
    src = rc.REPO_OUT / "analyses/prophecy/prophecy_sankey.svg"
    s = "/private/tmp/claude-501/-Users-kingslywang-Documents----ai-narratives-2026--claude-worktrees-jmir-r1-batch-1-fc3398/aa1ae4a7-1433-4f64-82ee-5af427f6ee43/scratchpad/ms/word/media/image6.png"
    import zipfile
    with zipfile.ZipFile(R1 / "inputs" / "Final Manuscript Submission LW jmir.docx") as z:
        (UF / "forward_validation_sankey.png").write_bytes(z.read("word/media/image6.png"))
    shutil.copyfile(src, UF / "forward_validation_sankey.svg")
    for id_ in ("RES-FV-SET", "RES-FV-CAND", "RES-FV-FP"):
        u.v(id_)
    (UF / "forward_validation_sankey_caption.md").write_text(
        "**Exploratory forward-validation of early Advocacy predictions (unchanged; exploratory and Advocacy-only).** The flow diagram "
        f"shows {u.v('RES-FV-SET').split(' (')[0]} from Advocacy records published in 2021-2023, grouped by falsifiability tier and adjudicated "
        "against evidence published from 2024 to April 2026. Node height and ribbon width represent claim counts. A single rater assigned "
        "each claim as borne out, partially borne out, not borne out, or too early/unfalsifiable; 'not borne out' required positive "
        "contrary evidence and corpus silence was classified as too early/unfalsifiable. The figure is reproduced unchanged from the "
        "submission (its evidence window extends to April 2026 by design). The Tier x verdict matrix is in {{T:fv_tier_verdict}}. The "
        "analysis was exploratory, Advocacy-only, single-rater and retrieval-dependent; it does not adjudicate AI capability or whether "
        "critical stances were correct. Critical stance was Alarm or Caution; favourable stance was Cautious Optimism or Advocacy; "
        "this figure concerns Advocacy records only.\n", encoding="utf-8")
    (UF / "forward_validation_sankey.json").write_text(json.dumps({"id": u.uid, "kind": "figure", "book_ids": sorted(set(u.ids)),
                                                                   "note": "image reproduced from the submitted manuscript (word/media/image6.png)"}, indent=1))


def f_temporal_robustness():
    u = U("temporal_robustness_fig")
    fig, axes = plt.subplots(2, 2, figsize=(W_IN, 5.6))
    corp = [("A", "(a) Production", "#000000", "o"), ("B", "(b) Augmented", "#0072B2", "s"), ("C", "(c) Precision-weighted", "#56B4E9", "^"),
            ("D", "(d) Full abstract", "#E69F00", "D")]
    for ax, out, ym in ((axes[0, 0], "CRITICAL", 40), (axes[0, 1], "ADVOCACY", 5)):
        for j, (c, lab, col, mk) in enumerate(corp):
            _series(ax, u, f"RES-B2ANN-{c}-{out}", col, lab, ymax=ym, marker=mk, offset=(j - 1.5) * 0.08, show=(c == "A"))
        ax.set_ylim(0, ym); ax.set_xticks(Y5); ax.grid(axis="y", lw=0.3, color="#DDDDDD"); ax.legend(frameon=False, fontsize=7, loc="lower right" if out == "CRITICAL" else "upper right")
        ax.set_ylabel(f"{'Critical' if out == 'CRITICAL' else 'Advocacy'}, % of records")
        ax.text(0.02, 1.02, f"B2 corpora: {out.lower()}", transform=ax.transAxes, fontweight="bold")
    defs = [("FULL", "Full corpus", "#000000", "o"), ("D1", "D1 Medicine area", "#0072B2", "s"), ("D2", "D2 without Medicine (misc.)", "#56B4E9", "^"),
            ("D3", "D3 broad health sciences", "#E69F00", "D")]
    for ax, out, ym in ((axes[1, 0], "CRITICAL", 40), (axes[1, 1], "ADVOCACY", 5)):
        for j, (c, lab, col, mk) in enumerate(defs):
            _series(ax, u, f"RES-B5ANN-{c}-{out}", col, lab, ymax=ym, marker=mk, offset=(j - 1.5) * 0.08, show=(c == "FULL"))
        if out == "ADVOCACY":
            _series(ax, u, "RES-TMP-SE", "#CC79A7", "Strong endorsement (B3), full corpus", ymax=ym, marker="v", show=False)
        ax.set_ylim(0, ym if out == "CRITICAL" else 22); ax.set_xticks(Y5); ax.grid(axis="y", lw=0.3, color="#DDDDDD")
        ax.legend(frameon=False, fontsize=7, loc="lower right" if out == "CRITICAL" else "upper right")
        ax.set_ylabel(f"{'Critical' if out == 'CRITICAL' else 'Advocacy or strong endorsement'}, % of records")
        ax.text(0.02, 1.02, f"B5 SJR definitions: {out.lower()}", transform=ax.transAxes, fontweight="bold")
    se = [u.n(f"RES-TMP-SE-{y}")["point"] for y in Y5]
    for x, s_ in zip(Y5, se):
        axes[1, 1].text(x, s_ + 0.4, f"{s_:.1f}", ha="center", va="bottom", fontsize=7, color="#CC79A7")
    fig.tight_layout(h_pad=2.2)
    fig_save(u, fig, "**Critical and Advocacy trends under alternative corpus definitions and a symmetric endorsement scale, 2021-2025.** "
             "Top: the four B2 corpora (production; augmented with records recovered by the full-abstract prefilter re-run; augmented with "
             "precision weights; full-abstract corpus). Bottom: the full corpus and three SJR medical-category restrictions (B5), with the "
             "B3 strong-endorsement share (all records as denominator) beside Advocacy. Points show annual estimates and whiskers 95% "
             "percentile bootstrap CIs (1000 joint resamples, seed 42); values are printed for the reference series (production corpus "
             "or full corpus, black) and for strong endorsement; every value with n/N for the other series is in {{T:corpus_sensitivity}}, {{T:sjr_sensitivity}} and "
             "{{T:symmetric_endorsement}}. Points are offset horizontally within each year for legibility. Critical stance was Alarm or "
             "Caution.")


def f_lexicon_vs_llm():
    u = U("lexicon_vs_llm_fig")
    fig, axes = plt.subplots(1, 4, figsize=(W_IN, 3.3), sharey=True)
    for ax, t in zip(axes, HEADLINE_THEMES):
        s_ = slug(t)
        _series(ax, u, f"RES-TMP-TH-{s_}", THEME_COLOURS[t], "LLM theme", ymax=80, offset=-0.09, show=False)
        _series(ax, u, f"RES-THM-LEX-{s_}", "#555555", "Lexicon", ymax=80, marker="s", offset=0.09, show=False)
        for y in Y5:   # per year: the higher series labelled above its CI, the lower one below
            a_, b_ = u.n(f"RES-TMP-TH-{s_}-{y}"), u.n(f"RES-THM-LEX-{s_}-{y}")
            for x_, c_, col, up in ((a_, b_, THEME_COLOURS[t], a_["point"] >= b_["point"]), (b_, a_, "#555555", b_["point"] > a_["point"])):
                ax.text(y + (-0.09 if col != "#555555" else 0.09), (x_["hi"] + 1.6) if up else (x_["lo"] - 1.6), f"{x_['point']:.1f}",
                        ha="center", va="bottom" if up else "top", fontsize=7, color=col)
        ax.set_ylim(0, 82); ax.set_xticks(Y5); ax.set_xticklabels([str(y) for y in Y5], rotation=45)
        ax.text(0.02, 1.02, t, transform=ax.transAxes, fontweight="bold"); ax.grid(axis="y", lw=0.3, color="#DDDDDD")
    axes[0].set_ylabel("% of critical records")
    from matplotlib.lines import Line2D
    fig.legend(handles=[Line2D([0], [0], marker="o", color="#333333", lw=1, ms=3, label="LLM theme (colour per theme)"),
                        Line2D([0], [0], marker="s", color="#555555", lw=1, ms=3, label="Lexicon (grey)")],
               loc="lower center", ncol=2, frameon=False)
    fig.tight_layout(rect=(0, 0.07, 1, 1))
    st = "; ".join(f"{t}: LLM {u.v(f'RES-TMP-TH-{slug(t)}-OR')}, lexicon {u.v(f'RES-THM-LEX-{slug(t)}-OR')}" for t in HEADLINE_THEMES)
    fig_save(u, fig, "**LLM theme prevalence and lexicon mention share for the four headline themes among critical records, 2021-2025.** "
             "Coloured points: share of critical records assigned the theme by the LLM classifier; grey squares: share whose MeSH terms, "
             "author keywords, title or abstract match the theme's pre-specified lexicon (Multimedia Appendix 1, Note 10). Whiskers: 95% "
             f"percentile bootstrap CIs (1000 resamples, seed 42); printed values are point estimates (%). OR per year: {st}. "
             "Values are in {{T:lexicon_and_terms}}. Critical stance was Alarm or Caution.")


def f_terms():
    u = U("terms_fig")
    fig, axes = plt.subplots(1, 2, figsize=(W_IN, 5.4))
    for ax, tag, lab, col in ((axes[0], "EMERG", "More frequent in 2024-2025 than 2021-2022", "#0072B2"),
                              (axes[1], "STANCE", "More frequent in critical than favourable records", "#D55E00")):
        rows = []
        for i in range(1, 21):
            x = u.n(f"RES-B6-{tag}-{i:02d}")
            rows.append((x["item"].split(": ", 1)[1], x["point"]))
        rows = rows[::-1]
        ax.scatter([r[1] for r in rows], range(len(rows)), color=col, s=12, zorder=3)
        for j, (t, z) in enumerate(rows):
            ax.text(z + 0.3, j, f"{z:.1f}", va="center", fontsize=7)
        ax.set_yticks(range(len(rows))); ax.set_yticklabels([r[0] for r in rows]); ax.set_xlabel("z score (weighted log-odds)")
        ax.set_xlim(0, max(r[1] for r in rows) * 1.18); ax.grid(axis="x", lw=0.3, color="#DDDDDD")
        ax.text(0.0, 1.01, lab, transform=ax.transAxes, fontweight="bold", va="bottom")
    fig.tight_layout(w_pad=2)
    fig_save(u, fig, "**MeSH and keyword terms most over-represented by period and by stance, 2021-2025.** Left: terms more frequent in "
             "2024-2025 than in 2021-2022 records; right: terms more frequent in critical than in favourable records. Top 20 terms per "
             "comparison by z score of the weighted log-odds ratio with an informative Dirichlet prior (Monroe et al. 2008; terms present in "
             "at least 20 records); printed values are z scores. The top 30 terms with their record counts are in {{T:lexicon_and_terms}}. "
             "Critical stance was Alarm or Caution; favourable stance was Cautious Optimism or Advocacy.")


TABLES = [t_stance_trend, t_update_2026, t_within_genre, t_keep_rate, t_themes, t_fda_robustness, t_country, t_ea_vs_nawe, t_region,
          t_pubtype, t_review_subtypes, t_theme_by_format, t_fv, t_q3, t_run_to_run, t_specialty_definitions, t_fda_mapping,
          t_stance_confusion, t_mechanism_confusion, t_prefilter_validation, t_theme_validation, t_regression_full, t_corpus_sensitivity,
          t_symmetric, t_sjr, t_lexicon, t_missing, t_precision, t_advocacy_by_specialty]
FIGURES = [f_within_genre, f_other_themes, f_theme_counts, f_generative_share, f_country_map_20, f_q3, f_sankey,
           f_temporal_robustness, f_lexicon_vs_llm, f_terms]


CHANGED = {r["id"] for r in __import__("csv").DictReader(open(_cc.FINAL / "NUMBERS_DIFF_v1_v2.csv", encoding="utf-8"))}
AFFECTED = {p.stem for p in UT.glob("*.json") if not p.stem.endswith("_v2") and set(json.loads(p.read_text())["book_ids"]) & CHANGED} | \
           {p.stem for p in UF.glob("*.json") if set(json.loads(p.read_text())["book_ids"]) & CHANGED}
FIG_UNIT = {"f_within_genre": "within_genre_fig", "f_other_themes": "other_themes_fig", "f_lexicon_vs_llm": "lexicon_vs_llm_fig",
            "f_theme_counts": "theme_counts_fig", "f_generative_share": "generative_share_fig", "f_country_map_20": "country_map_20",
            "f_q3": "q3_fig", "f_sankey": "forward_validation_sankey", "f_temporal_robustness": "temporal_robustness_fig", "f_terms": "terms_fig"}


def main():
    for f in TABLES:
        f()
    for f in FIGURES:
        if FIG_UNIT[f.__name__] in AFFECTED:
            f()
    print("v2 units written:", sorted(AFFECTED))


if __name__ == "__main__":
    main()
