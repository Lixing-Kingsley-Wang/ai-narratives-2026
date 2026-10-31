"""Batch 2d · the two post hoc Multimedia Appendix 3 tables (JMIR R1; D5, D2b, X1).
Every cell is read from NUMBERS_BOOK_R1_v2.csv by ID. Placement in the appendix is left to
Peter (ma_order.yaml is not changed). Run with revision_r1/.venv.
Outputs: revision_r1/final/ma/new_tables/MA3_lexicon_decomposition.{md,docx},
         MA3_period_correction.{md,docx}, new_tables_ids_used.csv
"""

from __future__ import annotations

import csv
import re

import c_common as _cc
_cc.BOOK_CSV = _cc.FINAL / "NUMBERS_BOOK_R1_v2.csv"
from c_common import MA, Y5, c_book  # noqa: E402
from c_docx import md_table, md_text, new_doc, para, table  # noqa: E402

BOOK = c_book()
OUTD = MA / "new_tables"; OUTD.mkdir(parents=True, exist_ok=True)
USED = []


def v(tab, id_):
    USED.append((tab, id_)); return BOOK[id_]["value"]


def num(tab, id_):
    USED.append((tab, id_)); r = BOOK[id_]
    f = lambda x: float(x) if x not in ("", None) else float("nan")
    return {k: f(r[k]) for k in ("point", "lo", "hi", "k", "n", "p")}


def cell(tab, id_):
    x = num(tab, id_)
    k, n = int(x["k"]), int(x["n"])
    if k == 0 or k == n:   # bootstrap interval degenerate: exact Clopper-Pearson, as in the book row
        m = re.search(r"exact Clopper-Pearson ([0-9.]+)%-([0-9.]+)%", BOOK[id_]["value"])
        return f"{x['point']:.1f} ({m[1]}-{m[2]}, exact); {k}/{n}"
    return f"{x['point']:.1f} ({x['lo']:.1f}-{x['hi']:.1f}); {k}/{n}"


def ptxt(p):
    return "P<.001" if p < 0.001 else "P=" + f"{p:.3f}".lstrip("0")


def orcell(tab, id_):
    x = num(tab, id_)
    return f"{x['point']:.3f} ({x['lo']:.3f}-{x['hi']:.3f}); {ptxt(x['p'])}"


def write(name, title, header, rows, notes, group_rows=()):
    d = new_doc(landscape=True)
    para(d, title, 10, bold=True)
    table(d, header, rows, size=7, group_rows=set(group_rows))
    for n in notes:
        para(d, n, 8, space_after=2)
    d.save(OUTD / f"{name}.docx")
    (OUTD / f"{name}.md").write_text(f"**{md_text(title)}**\n\n{md_table(header, rows, set(group_rows))}\n\n"
                                     + "\n\n".join(md_text(n) for n in notes) + "\n", encoding="utf-8")


def lexicon():
    T = "MA3_lexicon_decomposition"
    themes = [("REG", "Regulation"), ("ETH", "Ethics and bias"), ("ERR", "Errors and hallucination"), ("SAF", "Patient safety")]
    labels = {"A": "(a) All sources (title, abstract, author keywords or MeSH)", "B": "(b) Title + abstract",
              "C": "(c) Keywords or MeSH only (no title + abstract match)",
              "D": "(d) Classifier input (title + first 400 abstract characters)",
              "E": "(e) Later abstract only (characters 401 onward; no match in title + first 400)"}
    rows, groups = [], []
    for code, name in themes:
        groups.append(len(rows)); rows.append([f"{name} lexicon"])
        for r in "ABCDE":
            rows.append([labels[r]] + [cell(T, f"RES-LEXD-{code}-{r}-{y}") for y in Y5] + [orcell(T, f"RES-LEXD-{code}-{r}-OR")])
        for k in sorted(k for k in BOOK if k.startswith(f"RES-LEXD-{code}-TERM-") and k.endswith("-OR")):
            base = k[:-3]
            term = re.search(r"term '(.+?)'", BOOK[k]["item"])[1]
            rows.append([f"  term '{term}' (title + abstract)"] + [cell(T, f"{base}-{y}") for y in Y5] + [orcell(T, k)])
    groups.append(len(rows)); rows.append(["Median abstract length, critical records (characters)"])
    rows.append(["All critical records (empty abstract = 0)"] + [f"{num(T, f'RES-LEXD-ABSLEN-{y}')['point']:.1f}" for y in Y5] + [""])
    rows.append(["Records with an abstract"] + [v(T, f"RES-LEXD-ABSLEN-{y}").split("; ")[1].split(" characters")[0] for y in Y5] + [""])
    notes = [
        "Post hoc analysis, 2026-10-31 (plan: revision_r1/ANALYSIS_PLAN_batch2d.md, committed before the analysis). Critical "
        "records (Alarm or Caution) 2021-2025, n=4283. Lexicons, word-boundary matching and MeSH matching are those of the "
        "pre-specified B6 analysis (Multimedia Appendix 1, Note 10). Row (a) reproduces the B6 lexicon series exactly, and (a) is "
        "the union of (b) and (c) for every record. Rows (d) and (e) split the title + abstract text at the 400th abstract "
        "character, the input limit of the concern-theme classifier; a term that straddles character 400 is counted in neither.",
        "Cells: % (95% CI); n/N, with N = critical records of that year ("
        + "; ".join(f"{y} {int(num(T, f'RES-LEXD-REG-A-{y}')['n'])}" for y in Y5) + "). CIs: 95% percentile bootstrap, 1000 joint "
        "resamples of records, seed 42. OR per year: record-level logistic regression on publication year with journal cluster-robust "
        f"SEs ({re.search(r'[(](\d+) clusters', BOOK['RES-LEXD-REG-A-OR']['ci_method'])[1]} journals).",
        "Cells with no or all events show the exact Clopper-Pearson interval ('exact'). Single-term rows use the title + abstract text of row (b); 'human oversight' is an added phrase, not a lexicon term. "
        "Critical stance was Alarm or Caution.",
    ]
    write(T, "Post hoc source decomposition of the lexicon mention shares among critical records, 2021-2025.",
          ["Source or term", "2021", "2022", "2023", "2024", "2025", "OR per year (95% CI); P"], rows, notes, groups)


def period():
    T = "MA3_period_correction"
    S = [("ALARM", "Alarm"), ("CAUTION", "Caution"), ("NEUTRAL", "Neutral"), ("CAUTIOUSOPTIMISM", "Cautious Optimism"), ("ADVOCACY", "Advocacy")]
    rows, groups = [], []
    groups.append(len(rows)); rows.append(["(a) Conversion rates by model stratum and period: % (exact 95% CI; k/n)"])
    for code, lab in S:
        for t in ("ADVOCACY", "CRITICAL"):
            a, b = v(T, f"VAL-ST-PER-CONV-{code}-{t}-P1"), v(T, f"VAL-ST-PER-CONV-{code}-{t}-P2")
            rows.append([f"Model {lab}: P(human {'Advocacy' if t == 'ADVOCACY' else 'critical'})", a, b,
                         v(T, f"VAL-ST-PER-FISHER-{code}-{t}").replace("Fisher exact two-sided ", "")])
    groups.append(len(rows)); rows.append(["(b) Advocacy accuracy by period: % (exact 95% CI; k/n)"])
    for st, lab in (("ALL", "all 300"), ("INSCOPE", "in-scope 225")):
        for m, ml in (("PREC", "precision, P(human Advocacy | model Advocacy)"), ("REC", "recall, P(model Advocacy | human Advocacy)")):
            rows.append([f"{ml}, {lab}", v(T, f"VAL-ST-PER-ADV-{m}-{st}-P1"), v(T, f"VAL-ST-PER-ADV-{m}-{st}-P2"), ""])
    for tgt, lab in (("ADVOCACY", "Advocacy"), ("CRITICAL", "Critical")):
        groups.append(len(rows)); rows.append([f"(c) Corrected {lab.lower()} prevalence, % (95% CI): period-specific vs constant-rate"])
        for y in Y5 + ["DELTA"]:
            x = v(T, f"VAL-ST-PER-CORR-{tgt}-{y}")
            ps, cr = x.split("; constant-rate (T2, pre-specified) ")
            rows.append([str(y) if y != "DELTA" else "Change 2025 minus 2021, percentage points",
                         ps.replace("period-specific ", "").replace(" percentage points", ""),
                         cr.replace(" percentage points", ""),
                         ("2021-2023 rates" if y in (2021, 2022, 2023) else "2024-2025 rates" if y != "DELTA" else "")])
    notes = [
        "Post hoc analysis, 2026-10-31 (plan: revision_r1/ANALYSIS_PLAN_batch2d.md, committed before the analysis). It relaxes the "
        "assumption of the pre-specified correction (Multimedia Appendix 3, stance validation) that P(human label | model label) is "
        "the same every year. " + v(T, "VAL-ST-PER-META") + ".",
        "(a) and (b): exact Clopper-Pearson 95% CIs; Fisher exact two-sided test of the period difference within each stratum. "
        "In (a) the first value column is 2021-2023 and the second 2024-2025; in (b) the same; in (c) the first value column is the "
        "period-specific estimate, the second the pre-specified constant-rate estimate, and the third the rates applied. "
        "The validation sample was stratified by model stance, not by year, so period cells are small.",
        "(c): corrected prevalence for year y = sum over model strata of (share of year-y records with that model label) x "
        "P(human target | model label) for the period containing y; corpus = 14,058 records 2021-2025. Period-specific CIs: 1000 "
        "bootstrap draws (seed 42) resampling validation records within stratum x period, with a Jeffreys Beta(k+1/2, n-k+1/2) draw "
        "for cells with no or all events, and corpus records jointly. Constant-rate values are the pre-specified estimates (all 300 "
        "validation records); re-implemented here, they reproduce exactly. Critical stance was Alarm or Caution.",
    ]
    write(T, "Post hoc period-specific misclassification correction for Advocacy and critical prevalence, 2021-2025.",
          ["Item", "2021-2023 / period-specific", "2024-2025 / constant-rate", "Fisher P / rates applied"], rows, notes, groups)


def main():
    lexicon(); period()
    with open(OUTD / "new_tables_ids_used.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["table", "id"]); w.writerows(sorted(set(USED)))
    print("new tables written")


if __name__ == "__main__":
    main()
