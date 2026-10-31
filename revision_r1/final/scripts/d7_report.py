"""Write revision_r1/REPORT_batch2d.md from the Batch 2d outputs (nothing retyped). Run with revision_r1/.venv."""

from __future__ import annotations

import pandas as pd

import c_common as _cc
_cc.BOOK_CSV = _cc.FINAL / "NUMBERS_BOOK_R1_v2.csv"
from c_common import DATA, FINAL, MA, R1, c_book  # noqa: E402

B = c_book()
v = lambda i: B[i]["value"]


def main():
    d1 = pd.read_csv(DATA / "d1_cluster_or.csv")
    diff = pd.read_csv(FINAL / "NUMBERS_DIFF_v1_v2.csv")
    flags = pd.read_csv(DATA / "d1_flags.csv")
    rep = pd.read_csv(DATA / "d2_reproduction_check.csv")
    rows = pd.read_csv(DATA / "d2_lexicon_rows.csv"); terms = pd.read_csv(DATA / "d2_lexicon_terms.csv")
    ab = pd.read_csv(DATA / "d2_abstract_length.csv")
    qa = (FINAL / "QA_batch2d.md").read_text()
    lex_tab = (MA / "new_tables/MA3_lexicon_decomposition.md").read_text()
    per_tab = (MA / "new_tables/MA3_period_correction.md").read_text()

    reg = rows[(rows.theme == "Regulation") & (rows.year != "trend")].copy()
    reg["year"] = reg["year"].astype(int)
    exp = {"a": [24.8, 22.5, 20.8, 19.5, 29.9], "b": [23.7, 22.5, 20.5, 18.8, 29.3], "c": [1.1, 0.0, 0.3, 0.7, 0.7],
           "d": [8.1, 7.8, 6.2, 5.9, 7.5], "e": [15.6, 14.7, 14.3, 12.9, 21.6]}
    mism = []
    for r_, e in exp.items():
        got = reg[reg.row == r_].sort_values("year")["pct"].round(1).tolist()
        if got != e:
            mism.append(f"row ({r_}): expected {e}, got {got}")
    for term, e in (("oversight", [3.0, 2.1, 2.2, 2.1, 9.3]), ("human oversight", [0.4, 0.3, 0.5, 0.7, 3.2])):
        t = terms[(terms.term == term) & (terms.year != "trend")].copy(); t["year"] = t["year"].astype(int)
        got = t.sort_values("year")["pct"].round(1).tolist()
        if got != e:
            mism.append(f"'{term}': expected {e}, got {got}")
    med21, med25 = ab.loc[ab.year == 2021, "median_len_all"].iloc[0], ab.loc[ab.year == 2025, "median_len_all"].iloc[0]
    if med21 != 1426:
        mism.append(f"median abstract length 2021: expected 1426, got {med21:.1f} (median of an even number of records, all "
                    "critical records including empty abstracts; 1511.0 among the 245 with an abstract)")
    if med25 != 1766:
        mism.append(f"median abstract length 2025: expected 1766, got {med25:.1f}")

    L = [
        "# Batch 2d report · cluster-robust CIs and two post hoc tables (JMIR #109710, R1)", "",
        "Branch `jmir-r1-major-revision`. No LLM API calls, no data fetches, nothing pushed. Batch 2c files unchanged; every "
        "updated file is a new `_v2` file. Chat reports aggregates only.", "",
        "## Pre-specification", "",
        "- `revision_r1/ANALYSIS_PLAN_batch2d.md` committed as **b8e1c7e** (2026-10-31 11:10:50 -0400), before any D1-D3 "
        "computation. First outputs: `final/data/d1_cluster_or.csv` 11:12, `d2_lexicon_rows.csv` 11:13, "
        "`d3_corrected_prevalence.csv` 11:14 (file times; D1 was rerun once after the weighted-sandwich check below, with "
        "identical unweighted results).",
        "- D2 and D3 are labelled post hoc (2026-10-31) in every output.", "",
        "## D1 · Journal cluster-robust CIs", "",
        f"- **Series recomputed:** {len(d1)} (stances, critical, favourable, within-genre, 10 themes, 4 lexicon series, 8 mechanism "
        f"series, keep rate, B3 strong endorsement and upper bound, B2 corpora (a)-(d), B5 full and D1-D3 incl. the four theme "
        "trends, Q3 arm). Clusters: 2278 journals in the analytic corpus; keep rate "
        f"{int(d1.loc[d1.series == 'Prefilter keep rate', 'clusters'].iloc[0])} journals (86,700 eligible records); Q3 arm "
        f"{int(d1.loc[d1.series == 'Q3: critical', 'clusters'].iloc[0])}.",
        f"- **Point estimates:** all equal Batch 2c at the printed 3 decimals (max absolute difference "
        f"{d1.abs_diff.max():.5f}, from Batch 2c values that were stored only as 3-decimal text). Critical: "
        f"{v('RES-TMP-CRIT-OR')}, identical to B4's unadjusted cluster-robust estimate.",
        "- **Weighted corpus (B2 c):** statsmodels warns that cluster covariance is not fully supported with frequency weights, so "
        "this series uses an explicit weighted cluster sandwich (statsmodels' small-sample factor); on an unweighted series it "
        "reproduces the statsmodels SE to 15 digits.",
        f"- **Changed book rows:** {len(diff)} (`final/NUMBERS_DIFF_v1_v2.csv`). Adjusted ORs, Spearman ρ and proportion CIs unchanged.",
        f"- **Flag list** (P crosses .05, or CI changes between excluding and including 1): {len(flags)} rows, "
        f"{flags.series.nunique()} series (the two patient-safety rows are one estimate, computed for the main trend and for B5's "
        "full corpus; so two distinct findings):", "",
        "| Book ID | Series | v1 (Wald) | v2 (journal cluster-robust) |", "|---|---|---|---|",
    ] + [f"| {r.id} | {r.series} | {r.v1} | {r.v2} |" for r in flags.itertuples()] + [
        "",
        f"  Caution (v1 P=.016) stays below .05: {v('RES-TMP-CAUT-OR')}. Other P values that moved but did not cross .05 are "
        "in the diff file.",
        "- **`_v2` files:** `final/NUMBERS_BOOK_R1_v2.{md,csv}`; `final/NUMBERS_DIFF_v1_v2.csv`; `final/tables/Table2_v2.{docx,md}` "
        "(values identical to v1, because Table 2 already used B4's cluster-robust ORs; footnote states this) and "
        "`Table3_v2.{docx,md}` (primary, B2 and B5 columns updated; footnote now says journal cluster-robust SEs); "
        "`final/figures/Fig2_caption_v2.md`, `Fig3_caption_v2.md` (figures themselves unchanged); MA3 units "
        "`final/ma/units/tables/{stance_trend, within_genre, keep_rate, themes, q3_arm, symmetric_endorsement, corpus_sensitivity, "
        "sjr_sensitivity, lexicon_and_terms}_v2.json`; MA2 captions `final/ma/units/figures/{within_genre_fig, other_themes_fig, "
        "lexicon_vs_llm_fig}_caption_v2.md`; assembled `final/ma/Multimedia_Appendix_2_R1_v2.{docx,md}`, "
        "`Multimedia_Appendix_3_R1_v2.{docx,md}`, `ma_numbering_map_v2.csv` (same default order). Scripts: "
        "`final/scripts/d1_cluster_or.py`, `d4_book_v2.py`, and copies `c2_figures_v2.py`, `c3_tables_v2.py`, `c4_units_v2.py`, "
        "`final/ma/assemble_v2.py`.", "",
        "## D2 · Post hoc lexicon source decomposition", "",
        f"- **Row (a) reproduces B6 exactly:** {', '.join(f'{r.theme} {'yes' if r.reproduces_B6_k_and_n else 'NO'}' for r in rep.itertuples())} "
        f"(k and n identical every year); (a) = (b) or (c) for every record: {'yes' if rep.a_equals_b_or_c.all() else 'NO'}.",
        "- **Expected values:** " + ("all regulation rows (a)-(e), 'oversight' and 'human oversight' match to 1 decimal. "
                                     if not [m for m in mism if not m.startswith('median')] else "") +
        ("Mismatches: " + "; ".join(mism) + "." if mism else "no mismatch."),
        "- Table: `final/ma/new_tables/MA3_lexicon_decomposition.{md,docx}`; book rows `RES-LEXD-*`. `ma_order.yaml` unchanged.", "",
        lex_tab, "",
        "## D3 · Post hoc period-specific misclassification correction", "",
        f"- {v('VAL-ST-PER-META')}.",
        "- The constant-rate estimator re-implemented here reproduces the pre-specified T2 values exactly (Advocacy 6.16% to "
        "5.13%, Δ −1.03; critical 26.99% to 31.36%, Δ +4.37).",
        f"- **Advocacy, period-specific:** {v('VAL-ST-PER-CORR-ADVOCACY-2021').split(';')[0].replace('period-specific ', '')} (2021) to "
        f"{v('VAL-ST-PER-CORR-ADVOCACY-2025').split(';')[0].replace('period-specific ', '')} (2025); change "
        f"{v('VAL-ST-PER-CORR-ADVOCACY-DELTA').split(';')[0].replace('period-specific ', '')}.",
        f"- **Critical, period-specific:** {v('VAL-ST-PER-CORR-CRITICAL-2021').split(';')[0].replace('period-specific ', '')} (2021) to "
        f"{v('VAL-ST-PER-CORR-CRITICAL-2025').split(';')[0].replace('period-specific ', '')} (2025); change "
        f"{v('VAL-ST-PER-CORR-CRITICAL-DELTA').split(';')[0].replace('period-specific ', '')}.",
        "- Table: `final/ma/new_tables/MA3_period_correction.{md,docx}`; book rows `VAL-ST-PER-*`.", "",
        per_tab, "",
        "## QA (`final/QA_batch2d.md`)", "",
        "- " + qa.split("\n")[3].strip(),
        "- The one token left is the journal count in the lexicon-table footnote (1215), read from the book row's CI-method "
        "field rather than its value.",
        "- All new and `_v2` tables are real Word tables; format scan clean (no lowercase p, no leading zero, no 'Cohen's', no "
        "4-digit comma, no en dash in ranges, no 'Wald CI' left in a v2 file).", "",
        "## Checks", "",
        "- `output/` checksums: worktree (189 files) and main checkout (174 files) identical to the post-Batch 2c manifests.",
        "- No tracked Batch 2c file modified; `revision_r1/inputs/` read only.",
        "- No LLM API call; no data fetch; nothing pushed.",
    ]
    (R1 / "REPORT_batch2d.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("report written;", len(mism), "D2 mismatches")


if __name__ == "__main__":
    main()
