"""Batch 2d · numbers book v2 (JMIR R1). Plan: revision_r1/ANALYSIS_PLAN_batch2d.md (b8e1c7e).

Starts from NUMBERS_BOOK_R1.csv (Batch 2c, unchanged) and writes:
  NUMBERS_BOOK_R1_v2.{csv,md}  same IDs; OR rows carry the D1 journal cluster-robust CI and P;
                               composite rows that quote an OR are rewritten; new rows RES-LEXD-* (D2)
                               and VAL-ST-PER-* (D3), labelled post hoc (2026-10-31)
  NUMBERS_DIFF_v1_v2.csv       ID, v1 value, v2 value for every changed row
  data/d1_flags.csv            ORs whose P crosses .05 or whose CI changes between excluding and including 1
Run with revision_r1/.venv after d1_cluster_or.py, d2_lexicon_decomposition.py, d3_period_correction.py.
"""

from __future__ import annotations

import csv
import re

import numpy as np
import pandas as pd

import c_common
from c_common import DATA, FINAL, Y5, Book, ci, fn, nN, p_txt

V1 = list(csv.DictReader(open(c_common.BOOK_CSV, encoding="utf-8")))
OR_RE = re.compile(r"OR ([0-9.]+) per year \(95% CI ([0-9.]+)-([0-9.]+)\)(, P[=<>][0-9.]+)?")
POSTHOC = "post hoc, 2026-10-31"


def share_txt(pct, lo, hi, k, n):
    """As c1_numbers_book.share_val: exact Clopper-Pearson added when k = 0 or k = n (bootstrap degenerate)."""
    from scipy.stats import beta
    s = f"{pct:.1f}% ({nN(int(k), int(n))}; {ci(lo, hi)}"
    if k == 0 or k == n:
        clo = 0.0 if k == 0 else beta.ppf(0.025, k, n - k + 1) * 100
        chi = 100.0 if k == n else beta.ppf(0.975, k + 1, n - k) * 100
        s += f" (bootstrap); exact Clopper-Pearson {ci(clo, chi)[7:]}"
    return s + ")"


def or_text(r):
    return f"OR {r.OR:.3f} per year ({ci(r.OR_lo, r.OR_hi, 3, unit='')}), {p_txt(r.P)}"


def main():
    d1 = pd.read_csv(DATA / "d1_cluster_or.csv")
    by_id = {}
    for r in d1.itertuples():
        for i in r.book_ids.split(";"):
            by_id[i] = r
    B = Book()
    diff, flags = [], []
    for row in V1:
        new = dict(row)
        if row["id"] in by_id:
            r = by_id[row["id"]]
            m = OR_RE.search(row["value"])
            assert m, row["id"]
            v1_or, v1_lo, v1_hi = float(m[1]), float(m[2]), float(m[3])
            v1_p = float(row["p"]) if (row["id"].endswith("-OR") and row["p"] not in ("", None)) else None
            if v1_p is None and m[4]:
                ptxt = m[4][3:]
                v1_p = 0.0005 if ptxt.startswith("<") else float(ptxt[1:])
            new["value"] = OR_RE.sub(or_text(r), row["value"], count=1)
            num_is_or = row["point"] not in ("", None) and abs(float(row["point"]) - v1_or) < 6e-4
            if row["id"].endswith("-OR") or num_is_or:   # composite rows (B2) also store the OR in their numeric fields
                new.update({"point": r.OR, "lo": r.OR_lo, "hi": r.OR_hi, "p": r.P})
            new["ci_method"] = f"Wald, journal cluster-robust ({r.clusters} clusters)"
            inc1_v1, inc1_v2 = v1_lo <= 1 <= v1_hi, r.OR_lo <= 1 <= r.OR_hi
            sig_v1 = (v1_p < 0.05) if v1_p is not None else not inc1_v1
            sig_v2 = r.P < 0.05
            if sig_v1 != sig_v2 or inc1_v1 != inc1_v2:
                flags.append({"id": row["id"], "series": r.series, "v1": m[0], "v2": or_text(r),
                              "v1_P": "" if v1_p is None else (f"{v1_p:.3f}" if v1_p >= 0.001 else "<.001"),
                              "v2_P": p_txt(r.P), "crosses_.05": sig_v1 != sig_v2,
                              "CI_now_includes_1": (not inc1_v1) and inc1_v2, "CI_now_excludes_1": inc1_v1 and not inc1_v2})
            if new["value"] != row["value"]:
                diff.append({"id": row["id"], "v1_value": row["value"], "v2_value": c_common.jmir_text(new["value"])})
        B.add(new["id"], new["section"], new["subsection"], new["item"], new["value"], new["point"] or None, new["lo"] or None,
              new["hi"] or None, new["k"] or None, new["n"] or None, new["p"] or None, new["ci_method"], new["window"], new["source"])

    # ---------------- D2 rows ----------------
    S, sub0 = "Post hoc analyses (2026-10-31)", "D2 lexicon source decomposition"
    rows = pd.read_csv(DATA / "d2_lexicon_rows.csv"); terms = pd.read_csv(DATA / "d2_lexicon_terms.csv")
    lex = {"Errors and hallucination": "ERR", "Patient safety": "SAF", "Regulation": "REG", "Ethics and bias": "ETH"}
    for r in rows.itertuples():
        base = f"RES-LEXD-{lex[r.theme]}-{r.row.upper()}"
        if str(r.year) == "trend":
            B.add(f"{base}-OR", S, sub0, f"{r.theme}, {r.label}: OR per year ({POSTHOC})",
                  f"OR {r.OR:.3f} per year ({ci(r.OR_lo, r.OR_hi, 3, unit='')}), {p_txt(r.P)}; Spearman ρ={r.rho:+.2f} ({p_txt(r.P_rho)})",
                  r.OR, r.OR_lo, r.OR_hi, int(r.k), int(r.n), r.P, f"Wald, journal cluster-robust ({int(r.clusters)} clusters)",
                  source="final/data/d2_lexicon_rows.csv")
        else:
            B.add(f"{base}-{r.year}", S, sub0, f"{r.theme}, {r.label}, {r.year} ({POSTHOC})",
                  share_txt(r.pct, r.lo, r.hi, int(r.k), int(r.n)), r.pct, r.lo, r.hi, int(r.k), int(r.n),
                  ci_method="percentile bootstrap, 1000 joint resamples, seed 42", source="final/data/d2_lexicon_rows.csv")
    sub = "D2 single lexicon terms in title + abstract"
    for r in terms.itertuples():
        base = f"RES-LEXD-{lex[r.theme]}-TERM-{re.sub(r'[^A-Za-z]', '', r.term).upper()}"
        if str(r.year) == "trend":
            B.add(f"{base}-OR", S, sub, f"{r.theme}: term '{r.term}' in title + abstract: OR per year ({POSTHOC})",
                  f"OR {r.OR:.3f} per year ({ci(r.OR_lo, r.OR_hi, 3, unit='')}), {p_txt(r.P)}; Spearman ρ={r.rho:+.2f} ({p_txt(r.P_rho)})",
                  r.OR, r.OR_lo, r.OR_hi, int(r.k), int(r.n), r.P, "Wald, journal cluster-robust", source="final/data/d2_lexicon_terms.csv")
        else:
            B.add(f"{base}-{r.year}", S, sub, f"{r.theme}: term '{r.term}' in title + abstract, {r.year} ({POSTHOC})",
                  share_txt(r.pct, r.lo, r.hi, int(r.k), int(r.n)), r.pct, r.lo, r.hi, int(r.k), int(r.n),
                  ci_method="percentile bootstrap, 1000 joint resamples, seed 42", source="final/data/d2_lexicon_terms.csv")
    for r in pd.read_csv(DATA / "d2_abstract_length.csv").itertuples():
        B.add(f"RES-LEXD-ABSLEN-{r.year}", S, "D2 abstract length, critical records", f"Median abstract length, {r.year} ({POSTHOC})",
              f"{r.median_len_all:.1f} characters (all {fn(r.n_all)} critical records); {r.median_len_abstract_present:.1f} characters "
              f"({fn(r.n_abstract_present)} with an abstract)", r.median_len_all, n=r.n_all, source="final/data/d2_abstract_length.csv")
    for r in pd.read_csv(DATA / "d2_reproduction_check.csv").itertuples():
        B.add(f"RES-LEXD-{lex[r.theme]}-REPRO", S, "D2 reproduction check", f"{r.theme}: row (a) reproduces B6_lexicon_annual.csv",
              f"{'yes' if r.reproduces_B6_k_and_n else 'NO'} (k and n identical every year); (a) = (b) or (c) for every record: "
              f"{'yes' if r.a_equals_b_or_c else 'NO'}", source="final/data/d2_reproduction_check.csv")

    # ---------------- D3 rows ----------------
    sub = "D3 period-specific misclassification correction"
    conv = pd.read_csv(DATA / "d3_conversion_rates.csv")
    per = {"2021-2023": "P1", "2024-2025": "P2"}
    for r in conv.itertuples():
        st = re.sub(r"[^A-Za-z]", "", r.stratum).upper()
        if r.period in per:
            B.add(f"VAL-ST-PER-CONV-{st}-{r.target.upper()}-{per[r.period]}", S, sub,
                  f"Model {r.stratum}, {r.period}: P(human {r.target.lower()} | model stratum) ({POSTHOC})",
                  (f"{r.pct:.1f}% ({int(r.k)}/{int(r.n)}; exact Clopper-Pearson {ci(r.lo, r.hi)[7:]})" if r.n else "no records")
                  + (" [fewer than 10 validation records]" if r.under10 else ""),
                  r.pct, r.lo, r.hi, int(r.k), int(r.n), ci_method="Clopper-Pearson", window="validation sample, by period",
                  source="final/data/d3_conversion_rates.csv")
        else:
            B.add(f"VAL-ST-PER-FISHER-{st}-{r.target.upper()}", S, sub, f"Model {r.stratum}: period difference in P(human {r.target.lower()}) ({POSTHOC})",
                  f"Fisher exact two-sided {p_txt(r.P)}", p=r.P, window="validation sample", source="final/data/d3_conversion_rates.csv")
    for r in pd.read_csv(DATA / "d3_advocacy_accuracy.csv").itertuples():
        m = "PREC" if r.metric.startswith("precision") else "REC"
        B.add(f"VAL-ST-PER-ADV-{m}-{'ALL' if r.set.startswith('all') else 'INSCOPE'}-{per[r.period]}", S, sub,
              f"{r.set}, {r.period}: Advocacy {r.metric} ({POSTHOC})",
              f"{r.pct:.1f}% ({int(r.k)}/{int(r.n)}; exact Clopper-Pearson {ci(r.lo, r.hi)[7:]})", r.pct, r.lo, r.hi, int(r.k),
              int(r.n), ci_method="Clopper-Pearson", window="validation sample, by period", source="final/data/d3_advocacy_accuracy.csv")
    cp_ = pd.read_csv(DATA / "d3_corrected_prevalence.csv")
    for r in cp_.itertuples():
        tag = str(r.year) if str(r.year).isdigit() else "DELTA"
        unit = "%" if tag != "DELTA" else ""
        sfx = "" if tag != "DELTA" else " percentage points"
        B.add(f"VAL-ST-PER-CORR-{r.target.upper()}-{tag}", S, sub,
              f"Corrected {r.target.lower()} prevalence, {r.year}: period-specific vs constant-rate ({POSTHOC})",
              f"period-specific {r.period_specific:.2f}{unit}{sfx} ({ci(r.ps_lo, r.ps_hi, 2, unit)}); constant-rate (T2, pre-specified) "
              f"{r.constant_rate_T2:.2f}{unit}{sfx} ({ci(r.cr_lo, r.cr_hi, 2, unit)})",
              r.period_specific, r.ps_lo, r.ps_hi,
              ci_method="bootstrap: validation within stratum x period (Jeffreys draws for 0 or all events) and corpus jointly; 1000, seed 42",
              source="final/data/d3_corrected_prevalence.csv")
    mt = pd.read_csv(DATA / "d3_meta.csv").iloc[0]
    B.add("VAL-ST-PER-META", S, sub, f"Validation records in the period analysis ({POSTHOC})",
          f"{mt.in_periods} of {mt.validation_records}; excluded by publication year: 46 dated 2026 and 1 dated 2020; stratum x period "
          f"cells with fewer than 10 records: {mt.cells_under10} of 10; Jeffreys-drawn cells: Advocacy {mt.jeffreys_cells_advocacy}, "
          f"critical {mt.jeffreys_cells_critical}", int(mt.in_periods), n=int(mt.validation_records), window="validation sample",
          source="final/data/d3_meta.csv")

    c_common.BOOK_CSV = FINAL / "NUMBERS_BOOK_R1_v2.csv"
    c_common.BOOK_MD = FINAL / "NUMBERS_BOOK_R1_v2.md"
    intro = ("# R1 numbers book, v2 (Batch 2d)\n\nSame IDs as `NUMBERS_BOOK_R1.md` (Batch 2c, unchanged). Changes: every unadjusted "
             "record-level OR per year now carries a journal cluster-robust 95% CI and P (point estimates unchanged; "
             "`NUMBERS_DIFF_v1_v2.csv` lists every changed row); new post hoc rows (2026-10-31) `RES-LEXD-*` (D2 lexicon source "
             "decomposition) and `VAL-ST-PER-*` (D3 period-specific misclassification correction). Plan: "
             "`revision_r1/ANALYSIS_PLAN_batch2d.md`, commit b8e1c7e.")
    B.write(intro)
    pd.DataFrame(diff).to_csv(FINAL / "NUMBERS_DIFF_v1_v2.csv", index=False)
    pd.DataFrame(flags).to_csv(DATA / "d1_flags.csv", index=False)
    print(f"v2 book: {len(B.rows)} rows; changed: {len(diff)}; flags: {len(flags)}")
    print(pd.DataFrame(flags)[["id", "v1", "v2"]].to_string())


if __name__ == "__main__":
    main()
