# Batch 2d report · cluster-robust CIs and two post hoc tables (JMIR #109710, R1)

Branch `jmir-r1-major-revision`. No LLM API calls, no data fetches, nothing pushed. Batch 2c files unchanged; every updated file is a new `_v2` file. Chat reports aggregates only.

## Pre-specification

- `revision_r1/ANALYSIS_PLAN_batch2d.md` committed as **b8e1c7e** (2026-10-31 11:10:50 -0400), before any D1-D3 computation. First outputs: `final/data/d1_cluster_or.csv` 11:12, `d2_lexicon_rows.csv` 11:13, `d3_corrected_prevalence.csv` 11:14 (file times; D1 was rerun once after the weighted-sandwich check below, with identical unweighted results).
- D2 and D3 are labelled post hoc (2026-10-31) in every output.

## D1 · Journal cluster-robust CIs

- **Series recomputed:** 72 (stances, critical, favourable, within-genre, 10 themes, 4 lexicon series, 8 mechanism series, keep rate, B3 strong endorsement and upper bound, B2 corpora (a)-(d), B5 full and D1-D3 incl. the four theme trends, Q3 arm). Clusters: 2278 journals in the analytic corpus; keep rate 3903 journals (86,700 eligible records); Q3 arm 380.
- **Point estimates:** all equal Batch 2c at the printed 3 decimals (max absolute difference 0.00045, from Batch 2c values that were stored only as 3-decimal text). Critical: OR 1.077 per year (95% CI 1.038-1.116), P<.001, identical to B4's unadjusted cluster-robust estimate.
- **Weighted corpus (B2 c):** statsmodels warns that cluster covariance is not fully supported with frequency weights, so this series uses an explicit weighted cluster sandwich (statsmodels' small-sample factor); on an unweighted series it reproduces the statsmodels SE to 15 digits.
- **Changed book rows:** 88 (`final/NUMBERS_DIFF_v1_v2.csv`). Adjusted ORs, Spearman ρ and proportion CIs unchanged.
- **Flag list** (P crosses .05, or CI changes between excluding and including 1): 4 rows, 3 series (the two patient-safety rows are one estimate, computed for the main trend and for B5's full corpus; so two distinct findings):

| Book ID | Series | v1 (Wald) | v2 (journal cluster-robust) |
|---|---|---|---|
| RES-TMP-TH-PATIENTSAFETY-OR | Theme: Patient safety | OR 1.055 per year (95% CI 1.002-1.111), P=.041 | OR 1.055 per year (95% CI 0.995-1.118), P=.071 |
| RES-SEN-B5D2-ETHICSANDBIAS | B5 D2: theme Ethics & bias | OR 0.938 per year (95% CI 0.883-0.996) | OR 0.938 per year (95% CI 0.871-1.009), P=.087 |
| RES-B5X-FULL-THEMETREND-PATIENTSAFETY | B5 FULL: theme Patient safety | OR 1.055 per year (95% CI 1.002-1.111) | OR 1.055 per year (95% CI 0.995-1.118), P=.071 |
| RES-B5X-D2-THEMETREND-ETHICSANDBIAS | B5 D2: theme Ethics & bias | OR 0.938 per year (95% CI 0.883-0.996) | OR 0.938 per year (95% CI 0.871-1.009), P=.087 |

  Caution (v1 P=.016) stays below .05: OR 1.038 per year (95% CI 1.001-1.077), P=.047. Other P values that moved but did not cross .05 are in the diff file.
- **`_v2` files:** `final/NUMBERS_BOOK_R1_v2.{md,csv}`; `final/NUMBERS_DIFF_v1_v2.csv`; `final/tables/Table2_v2.{docx,md}` (values identical to v1, because Table 2 already used B4's cluster-robust ORs; footnote states this) and `Table3_v2.{docx,md}` (primary, B2 and B5 columns updated; footnote now says journal cluster-robust SEs); `final/figures/Fig2_caption_v2.md`, `Fig3_caption_v2.md` (figures themselves unchanged); MA3 units `final/ma/units/tables/{stance_trend, within_genre, keep_rate, themes, q3_arm, symmetric_endorsement, corpus_sensitivity, sjr_sensitivity, lexicon_and_terms}_v2.json`; MA2 captions `final/ma/units/figures/{within_genre_fig, other_themes_fig, lexicon_vs_llm_fig}_caption_v2.md`; assembled `final/ma/Multimedia_Appendix_2_R1_v2.{docx,md}`, `Multimedia_Appendix_3_R1_v2.{docx,md}`, `ma_numbering_map_v2.csv` (same default order). Scripts: `final/scripts/d1_cluster_or.py`, `d4_book_v2.py`, and copies `c2_figures_v2.py`, `c3_tables_v2.py`, `c4_units_v2.py`, `final/ma/assemble_v2.py`.

## D2 · Post hoc lexicon source decomposition

- **Row (a) reproduces B6 exactly:** Errors and hallucination yes, Patient safety yes, Regulation yes, Ethics and bias yes (k and n identical every year); (a) = (b) or (c) for every record: yes.
- **Expected values:** all regulation rows (a)-(e), 'oversight' and 'human oversight' match to 1 decimal. Mismatches: median abstract length 2021: expected 1426, got 1426.5 (median of an even number of records, all critical records including empty abstracts; 1511.0 among the 245 with an abstract).
- Table: `final/ma/new_tables/MA3_lexicon_decomposition.{md,docx}`; book rows `RES-LEXD-*`. `ma_order.yaml` unchanged.

**Post hoc source decomposition of the lexicon mention shares among critical records, 2021-2025.**

| Source or term | 2021 | 2022 | 2023 | 2024 | 2025 | OR per year (95% CI); P |
|---|---|---|---|---|---|---|
| **Regulation lexicon** | | | | | | |
| (a) All sources (title, abstract, author keywords or MeSH) | 24.8 (19.9-29.7); 67/270 | 22.5 (18.1-27.5); 75/333 | 20.8 (17.6-23.9); 130/624 | 19.5 (17.5-21.9); 240/1228 | 29.9 (27.7-32.1); 547/1828 | 1.128 (1.050-1.212); *P*<.001 |
| (b) Title + abstract | 23.7 (19.0-28.5); 64/270 | 22.5 (18.1-27.5); 75/333 | 20.5 (17.3-23.7); 128/624 | 18.8 (16.7-21.2); 231/1228 | 29.3 (27.0-31.4); 535/1828 | 1.128 (1.048-1.213); *P*=.001 |
| (c) Keywords or MeSH only (no title + abstract match) | 1.1 (0.0-2.5); 3/270 | 0.0 (0.0-1.1, exact); 0/333 | 0.3 (0.0-0.8); 2/624 | 0.7 (0.3-1.2); 9/1228 | 0.7 (0.3-1.1); 12/1828 | 1.077 (0.730-1.589); *P*=.708 |
| (d) Classifier input (title + first 400 abstract characters) | 8.1 (5.0-11.4); 22/270 | 7.8 (5.1-10.8); 26/333 | 6.2 (4.3-8.1); 39/624 | 5.9 (4.6-7.2); 72/1228 | 7.5 (6.4-8.8); 138/1828 | 1.000 (0.903-1.107); *P*=.995 |
| (e) Later abstract only (characters 401 onward; no match in title + first 400) | 15.6 (11.7-19.8); 42/270 | 14.7 (11.0-18.7); 49/333 | 14.3 (11.6-17.0); 89/624 | 12.9 (11.2-14.9); 159/1228 | 21.6 (19.7-23.5); 395/1828 | 1.170 (1.076-1.271); *P*<.001 |
|   term 'accountab*' (title + abstract) | 2.6 (0.8-4.7); 7/270 | 3.6 (1.8-5.7); 12/333 | 3.5 (2.2-5.1); 22/624 | 3.5 (2.5-4.5); 43/1228 | 6.1 (5.0-7.1); 111/1828 | 1.273 (1.099-1.476); *P*=.001 |
|   term 'governance' (title + abstract) | 2.2 (0.7-4.1); 6/270 | 5.4 (3.1-7.9); 18/333 | 2.6 (1.4-3.8); 16/624 | 2.7 (1.9-3.7); 33/1228 | 5.9 (4.9-7.0); 108/1828 | 1.253 (1.064-1.476); *P*=.007 |
|   term 'human oversight' (title + abstract) | 0.4 (0.0-1.4); 1/270 | 0.3 (0.0-0.9); 1/333 | 0.5 (0.0-1.1); 3/624 | 0.7 (0.3-1.1); 8/1228 | 3.2 (2.4-4.0); 58/1828 | 2.706 (1.714-4.271); *P*<.001 |
|   term 'legislat*' (title + abstract) | 1.9 (0.4-3.6); 5/270 | 0.9 (0.0-2.1); 3/333 | 0.5 (0.0-1.1); 3/624 | 0.5 (0.2-0.9); 6/1228 | 0.5 (0.3-0.9); 10/1828 | 0.761 (0.530-1.093); *P*=.139 |
|   term 'liability' (title + abstract) | 3.0 (1.1-5.0); 8/270 | 3.6 (1.7-5.8); 12/333 | 2.1 (1.0-3.3); 13/624 | 2.1 (1.4-2.9); 26/1228 | 2.1 (1.5-2.8); 38/1828 | 0.891 (0.762-1.042); *P*=.149 |
|   term 'oversight' (title + abstract) | 3.0 (1.2-5.1); 8/270 | 2.1 (0.6-3.8); 7/333 | 2.2 (1.1-3.6); 14/624 | 2.1 (1.4-2.9); 26/1228 | 9.3 (8.0-10.7); 170/1828 | 1.869 (1.449-2.412); *P*<.001 |
|   term 'policies' (title + abstract) | 2.2 (0.7-4.1); 6/270 | 1.2 (0.2-2.4); 4/333 | 2.1 (1.1-3.2); 13/624 | 1.3 (0.7-2.0); 16/1228 | 3.0 (2.2-3.7); 54/1828 | 1.194 (0.914-1.559); *P*=.194 |
|   term 'policy' (title + abstract) | 4.4 (2.2-7.1); 12/270 | 2.7 (1.2-4.6); 9/333 | 1.9 (0.9-3.0); 12/624 | 2.9 (2.0-4.0); 36/1228 | 4.8 (3.7-5.7); 87/1828 | 1.169 (0.969-1.409); *P*=.102 |
|   term 'regulat*' (title + abstract) | 13.7 (9.8-18.0); 37/270 | 13.2 (9.7-17.1); 44/333 | 11.1 (8.5-13.4); 69/624 | 10.4 (8.7-12.2); 128/1228 | 13.6 (11.9-15.2); 248/1828 | 1.020 (0.942-1.106); *P*=.621 |
| **Ethics and bias lexicon** | | | | | | |
| (a) All sources (title, abstract, author keywords or MeSH) | 44.1 (38.2-49.6); 119/270 | 45.9 (40.2-51.4); 153/333 | 41.5 (37.6-45.4); 259/624 | 37.9 (35.0-40.6); 465/1228 | 44.8 (42.4-47.1); 819/1828 | 1.008 (0.955-1.064); *P*=.767 |
| (b) Title + abstract | 41.5 (35.7-47.2); 112/270 | 45.0 (39.5-50.6); 150/333 | 39.3 (35.3-43.1); 245/624 | 36.4 (33.4-39.2); 447/1228 | 43.4 (41.2-45.8); 794/1828 | 1.016 (0.963-1.072); *P*=.554 |
| (c) Keywords or MeSH only (no title + abstract match) | 2.6 (0.8-4.6); 7/270 | 0.9 (0.0-2.0); 3/333 | 2.2 (1.1-3.6); 14/624 | 1.5 (0.9-2.1); 18/1228 | 1.4 (0.9-1.9); 25/1828 | 0.891 (0.732-1.085); *P*=.252 |
| (d) Classifier input (title + first 400 abstract characters) | 23.0 (17.9-28.2); 62/270 | 27.9 (23.0-32.7); 93/333 | 21.8 (18.7-24.9); 136/624 | 18.6 (16.4-20.8); 228/1228 | 20.9 (19.1-22.7); 382/1828 | 0.937 (0.875-1.003); *P*=.059 |
| (e) Later abstract only (characters 401 onward; no match in title + first 400) | 18.5 (14.1-23.2); 50/270 | 17.1 (13.1-21.4); 57/333 | 17.5 (14.5-20.6); 109/624 | 17.8 (15.7-20.0); 218/1228 | 22.5 (20.7-24.5); 412/1828 | 1.103 (1.036-1.175); *P*=.002 |
|   term 'bias*' (title + abstract) | 21.9 (17.3-26.6); 59/270 | 21.9 (17.2-26.6); 73/333 | 21.2 (18.0-24.3); 132/624 | 17.6 (15.4-19.6); 216/1228 | 22.6 (20.8-24.7); 414/1828 | 1.016 (0.955-1.080); *P*=.620 |
|   term 'discriminat*' (title + abstract) | 2.6 (1.0-4.6); 7/270 | 1.5 (0.3-2.8); 5/333 | 3.0 (1.6-4.5); 19/624 | 1.8 (1.1-2.6); 22/1228 | 1.6 (1.1-2.2); 30/1828 | 0.889 (0.761-1.040); *P*=.141 |
|   term 'equit*' (title + abstract) | 5.2 (2.8-7.9); 14/270 | 6.9 (4.3-9.7); 23/333 | 6.7 (4.7-8.6); 42/624 | 5.9 (4.5-7.3); 72/1228 | 10.9 (9.5-12.3); 199/1828 | 1.248 (1.115-1.398); *P*<.001 |
|   term 'ethic*' (title + abstract) | 21.5 (16.9-26.5); 58/270 | 24.3 (19.7-29.0); 81/333 | 20.8 (17.7-24.0); 130/624 | 22.1 (19.6-24.7); 272/1228 | 28.0 (26.0-30.2); 512/1828 | 1.107 (1.032-1.188); *P*=.005 |
|   term 'fairness' (title + abstract) | 3.0 (1.1-5.1); 8/270 | 5.4 (2.9-8.1); 18/333 | 4.2 (2.7-5.8); 26/624 | 3.7 (2.7-4.8); 45/1228 | 4.8 (3.8-5.7); 87/1828 | 1.053 (0.917-1.208); *P*=.466 |
|   term 'justice' (title + abstract) | 2.6 (1.0-4.6); 7/270 | 1.8 (0.6-3.3); 6/333 | 1.6 (0.8-2.7); 10/624 | 1.7 (1.0-2.5); 21/1228 | 1.5 (0.9-2.0); 27/1828 | 0.898 (0.747-1.081); *P*=.257 |
| **Errors and hallucination lexicon** | | | | | | |
| (a) All sources (title, abstract, author keywords or MeSH) | 8.1 (5.1-11.5); 22/270 | 7.2 (4.5-10.1); 24/333 | 13.9 (11.3-16.7); 87/624 | 20.7 (18.5-23.0); 254/1228 | 22.6 (20.9-24.7); 414/1828 | 1.384 (1.283-1.493); *P*<.001 |
| (b) Title + abstract | 8.1 (5.1-11.5); 22/270 | 7.2 (4.5-10.1); 24/333 | 13.8 (11.1-16.5); 86/624 | 20.6 (18.4-23.0); 253/1228 | 22.4 (20.6-24.4); 410/1828 | 1.380 (1.279-1.490); *P*<.001 |
| (c) Keywords or MeSH only (no title + abstract match) | 0.0 (0.0-1.4, exact); 0/270 | 0.0 (0.0-1.1, exact); 0/333 | 0.2 (0.0-0.5); 1/624 | 0.1 (0.0-0.3); 1/1228 | 0.2 (0.1-0.4); 4/1828 | 1.750 (0.641-4.778); *P*=.275 |
| (d) Classifier input (title + first 400 abstract characters) | 3.0 (1.1-5.2); 8/270 | 2.4 (0.8-4.2); 8/333 | 2.6 (1.4-4.0); 16/624 | 3.2 (2.3-4.2); 39/1228 | 4.5 (3.5-5.5); 83/1828 | 1.212 (1.025-1.432); *P*=.024 |
| (e) Later abstract only (characters 401 onward; no match in title + first 400) | 5.2 (2.6-7.9); 14/270 | 4.8 (2.7-7.3); 16/333 | 11.2 (8.8-13.8); 70/624 | 17.4 (15.3-19.6); 214/1228 | 17.8 (16.3-19.7); 326/1828 | 1.396 (1.291-1.510); *P*<.001 |
|   term 'confabulat*' (title + abstract) | 0.0 (0.0-1.4, exact); 0/270 | 0.0 (0.0-1.1, exact); 0/333 | 0.2 (0.0-0.5); 1/624 | 0.3 (0.1-0.7); 4/1228 | 0.2 (0.0-0.4); 3/1828 | 1.291 (0.827-2.017); *P*=.261 |
|   term 'error*' (title + abstract) | 5.9 (3.2-8.8); 16/270 | 6.3 (3.9-9.1); 21/333 | 5.8 (4.1-7.8); 36/624 | 6.9 (5.6-8.4); 85/1228 | 8.0 (6.7-9.2); 146/1828 | 1.107 (0.997-1.230); *P*=.058 |
|   term 'fabricat*' (title + abstract) | 0.0 (0.0-1.4, exact); 0/270 | 0.0 (0.0-1.1, exact); 0/333 | 0.6 (0.2-1.4); 4/624 | 1.1 (0.6-1.8); 14/1228 | 1.1 (0.7-1.6); 20/1828 | 1.569 (1.176-2.095); *P*=.002 |
|   term 'factual*' (title + abstract) | 0.0 (0.0-1.4, exact); 0/270 | 0.0 (0.0-1.1, exact); 0/333 | 0.5 (0.0-1.1); 3/624 | 1.4 (0.7-2.0); 17/1228 | 1.8 (1.2-2.4); 32/1828 | 1.937 (1.463-2.564); *P*<.001 |
|   term 'hallucinat*' (title + abstract) | 0.0 (0.0-1.4, exact); 0/270 | 0.0 (0.0-1.1, exact); 0/333 | 1.0 (0.3-1.8); 6/624 | 2.9 (1.9-3.8); 35/1228 | 5.1 (4.1-6.1); 93/1828 | 2.370 (1.888-2.976); *P*<.001 |
|   term 'inaccura*' (title + abstract) | 0.7 (0.0-2.0); 2/270 | 0.3 (0.0-1.2); 1/333 | 3.8 (2.4-5.6); 24/624 | 5.6 (4.4-7.1); 69/1228 | 5.2 (4.2-6.2); 95/1828 | 1.421 (1.246-1.622); *P*<.001 |
|   term 'incorrect' (title + abstract) | 1.9 (0.4-3.7); 5/270 | 0.6 (0.0-1.6); 2/333 | 3.2 (1.9-4.7); 20/624 | 5.9 (4.4-7.2); 72/1228 | 4.4 (3.5-5.4); 80/1828 | 1.276 (1.111-1.466); *P*<.001 |
|   term 'misinformation' (title + abstract) | 0.0 (0.0-1.4, exact); 0/270 | 0.0 (0.0-1.1, exact); 0/333 | 1.6 (0.7-2.7); 10/624 | 2.1 (1.3-3.0); 26/1228 | 3.0 (2.2-3.8); 54/1828 | 1.736 (1.367-2.205); *P*<.001 |
| **Patient safety lexicon** | | | | | | |
| (a) All sources (title, abstract, author keywords or MeSH) | 13.7 (9.5-18.0); 37/270 | 14.1 (10.4-17.9); 47/333 | 14.3 (11.2-17.3); 89/624 | 16.5 (14.5-18.6); 203/1228 | 19.2 (17.5-20.9); 351/1828 | 1.133 (1.055-1.217); *P*<.001 |
| (b) Title + abstract | 13.7 (9.5-18.0); 37/270 | 13.5 (9.9-17.1); 45/333 | 13.3 (10.6-16.1); 83/624 | 16.2 (14.2-18.3); 199/1228 | 18.8 (17.2-20.5); 344/1828 | 1.139 (1.058-1.226); *P*<.001 |
| (c) Keywords or MeSH only (no title + abstract match) | 0.0 (0.0-1.4, exact); 0/270 | 0.6 (0.0-1.5); 2/333 | 1.0 (0.3-1.8); 6/624 | 0.3 (0.1-0.7); 4/1228 | 0.4 (0.1-0.7); 7/1828 | 0.939 (0.714-1.234); *P*=.651 |
| (d) Classifier input (title + first 400 abstract characters) | 4.8 (2.3-7.3); 13/270 | 6.0 (3.8-8.7); 20/333 | 5.6 (3.9-7.5); 35/624 | 4.6 (3.5-5.8); 57/1228 | 6.1 (5.1-7.2); 112/1828 | 1.042 (0.931-1.167); *P*=.474 |
| (e) Later abstract only (characters 401 onward; no match in title + first 400) | 8.9 (5.6-12.5); 24/270 | 7.5 (4.8-10.2); 25/333 | 7.5 (5.5-9.7); 47/624 | 11.6 (9.8-13.4); 142/1228 | 12.7 (11.3-14.2); 232/1828 | 1.182 (1.080-1.293); *P*<.001 |
|   term 'adverse' (title + abstract) | 0.7 (0.0-1.9); 2/270 | 1.2 (0.3-2.5); 4/333 | 1.3 (0.5-2.2); 8/624 | 1.3 (0.7-1.9); 16/1228 | 1.4 (0.9-1.9); 25/1828 | 1.091 (0.866-1.375); *P*=.460 |
|   term 'harm*' (title + abstract) | 4.1 (1.9-6.5); 11/270 | 6.6 (4.0-9.4); 22/333 | 7.1 (5.1-9.2); 44/624 | 7.0 (5.6-8.5); 86/1228 | 6.2 (5.2-7.3); 114/1828 | 1.029 (0.929-1.140); *P*=.584 |
|   term 'patient safety' (title + abstract) | 3.7 (1.5-6.1); 10/270 | 0.6 (0.0-1.6); 2/333 | 1.9 (1.0-3.1); 12/624 | 2.4 (1.5-3.2); 29/1228 | 4.3 (3.4-5.1); 78/1828 | 1.292 (1.061-1.574); *P*=.011 |
|   term 'safety' (title + abstract) | 11.1 (7.2-15.2); 30/270 | 6.3 (3.9-9.0); 21/333 | 6.7 (4.7-8.7); 42/624 | 9.8 (8.3-11.4); 120/1228 | 13.9 (12.4-15.5); 255/1828 | 1.226 (1.117-1.347); *P*<.001 |
| **Median abstract length, critical records (characters)** | | | | | | |
| All critical records (empty abstract = 0) | 1426.5 | 1423.0 | 1495.5 | 1625.5 | 1766.0 |  |
| Records with an abstract | 1511.0 | 1612.0 | 1611.0 | 1720.0 | 1786.0 |  |

Post hoc analysis, 2026-10-31 (plan: revision_r1/ANALYSIS_PLAN_batch2d.md, committed before the analysis). Critical records (Alarm or Caution) 2021-2025, n=4283. Lexicons, word-boundary matching and MeSH matching are those of the pre-specified B6 analysis (Multimedia Appendix 1, Note 10). Row (a) reproduces the B6 lexicon series exactly, and (a) is the union of (b) and (c) for every record. Rows (d) and (e) split the title + abstract text at the 400th abstract character, the input limit of the concern-theme classifier; a term that straddles character 400 is counted in neither.

Cells: % (95% CI); n/N, with N = critical records of that year (2021 270; 2022 333; 2023 624; 2024 1228; 2025 1828). CIs: 95% percentile bootstrap, 1000 joint resamples of records, seed 42. OR per year: record-level logistic regression on publication year with journal cluster-robust SEs (1215 journals).

Cells with no or all events show the exact Clopper-Pearson interval ('exact'). Single-term rows use the title + abstract text of row (b); 'human oversight' is an added phrase, not a lexicon term. Critical stance was Alarm or Caution.


## D3 · Post hoc period-specific misclassification correction

- 253 of 300; excluded by publication year: 46 dated 2026 and 1 dated 2020; stratum x period cells with fewer than 10 records: 1 of 10; Jeffreys-drawn cells: Advocacy 6, critical 4.
- The constant-rate estimator re-implemented here reproduces the pre-specified T2 values exactly (Advocacy 6.16% to 5.13%, Δ −1.03; critical 26.99% to 31.36%, Δ +4.37).
- **Advocacy, period-specific:** 3.07% (95% CI 0.98%-10.04%) (2021) to 6.99% (95% CI 2.26%-13.06%) (2025); change 3.92 percentage points (95% CI -3.79 to 9.45).
- **Critical, period-specific:** 30.45% (95% CI 19.55%-41.09%) (2021) to 27.70% (95% CI 22.03%-33.84%) (2025); change -2.75 percentage points (95% CI -14.52 to 9.57).
- Table: `final/ma/new_tables/MA3_period_correction.{md,docx}`; book rows `VAL-ST-PER-*`.

**Post hoc period-specific misclassification correction for Advocacy and critical prevalence, 2021-2025.**

| Item | 2021-2023 / period-specific | 2024-2025 / constant-rate | Fisher P / rates applied |
|---|---|---|---|
| **(a) Conversion rates by model stratum and period: % (exact 95% CI; k/n)** | | | |
| Model Alarm: P(human Advocacy) | 0.0% (0/7; exact Clopper-Pearson 0.0%-41.0%) [fewer than 10 validation records] | 0.0% (0/24; exact Clopper-Pearson 0.0%-14.2%) | *P*>.99 |
| Model Alarm: P(human critical) | 100.0% (7/7; exact Clopper-Pearson 59.0%-100.0%) [fewer than 10 validation records] | 95.8% (23/24; exact Clopper-Pearson 78.9%-99.9%) | *P*>.99 |
| Model Caution: P(human Advocacy) | 0.0% (0/12; exact Clopper-Pearson 0.0%-26.5%) | 0.0% (0/38; exact Clopper-Pearson 0.0%-9.3%) | *P*>.99 |
| Model Caution: P(human critical) | 58.3% (7/12; exact Clopper-Pearson 27.7%-84.8%) | 68.4% (26/38; exact Clopper-Pearson 51.3%-82.5%) | *P*=.728 |
| Model Neutral: P(human Advocacy) | 0.0% (0/26; exact Clopper-Pearson 0.0%-13.2%) | 0.0% (0/33; exact Clopper-Pearson 0.0%-10.6%) | *P*>.99 |
| Model Neutral: P(human critical) | 11.5% (3/26; exact Clopper-Pearson 2.4%-30.2%) | 0.0% (0/33; exact Clopper-Pearson 0.0%-10.6%) | *P*=.080 |
| Model Cautious Optimism: P(human Advocacy) | 3.0% (1/33; exact Clopper-Pearson 0.1%-15.8%) | 9.6% (5/52; exact Clopper-Pearson 3.2%-21.0%) | *P*=.397 |
| Model Cautious Optimism: P(human critical) | 21.2% (7/33; exact Clopper-Pearson 9.0%-38.9%) | 7.7% (4/52; exact Clopper-Pearson 2.1%-18.5%) | *P*=.099 |
| Model Advocacy: P(human Advocacy) | 38.5% (5/13; exact Clopper-Pearson 13.9%-68.4%) | 73.3% (11/15; exact Clopper-Pearson 44.9%-92.2%) | *P*=.125 |
| Model Advocacy: P(human critical) | 0.0% (0/13; exact Clopper-Pearson 0.0%-24.7%) | 0.0% (0/15; exact Clopper-Pearson 0.0%-21.8%) | *P*>.99 |
| **(b) Advocacy accuracy by period: % (exact 95% CI; k/n)** | | | |
| precision, P(human Advocacy \| model Advocacy), all 300 | 38.5% (5/13; exact Clopper-Pearson 13.9%-68.4%) | 73.3% (11/15; exact Clopper-Pearson 44.9%-92.2%) |  |
| recall, P(model Advocacy \| human Advocacy), all 300 | 83.3% (5/6; exact Clopper-Pearson 35.9%-99.6%) | 68.8% (11/16; exact Clopper-Pearson 41.3%-89.0%) |  |
| precision, P(human Advocacy \| model Advocacy), in-scope 225 | 50.0% (5/10; exact Clopper-Pearson 18.7%-81.3%) | 78.6% (11/14; exact Clopper-Pearson 49.2%-95.3%) |  |
| recall, P(model Advocacy \| human Advocacy), in-scope 225 | 83.3% (5/6; exact Clopper-Pearson 35.9%-99.6%) | 68.8% (11/16; exact Clopper-Pearson 41.3%-89.0%) |  |
| **(c) Corrected advocacy prevalence, % (95% CI): period-specific vs constant-rate** | | | |
| 2021 | 3.07% (95% CI 0.98%-10.04%) | 6.16% (95% CI 3.13%-9.65%) | 2021-2023 rates |
| 2022 | 2.75% (95% CI 0.78%-9.67%) | 5.71% (95% CI 2.75%-8.99%) | 2021-2023 rates |
| 2023 | 2.61% (95% CI 0.77%-9.73%) | 5.40% (95% CI 2.67%-8.50%) | 2021-2023 rates |
| 2024 | 6.86% (95% CI 2.58%-12.63%) | 5.04% (95% CI 2.40%-8.10%) | 2024-2025 rates |
| 2025 | 6.99% (95% CI 2.26%-13.06%) | 5.13% (95% CI 2.33%-8.41%) | 2024-2025 rates |
| Change 2025 minus 2021, percentage points | 3.92 (95% CI -3.79 to 9.45) | -1.03 (95% CI -1.79 to -0.42) |  |
| **(c) Corrected critical prevalence, % (95% CI): period-specific vs constant-rate** | | | |
| 2021 | 30.45% (95% CI 19.55%-41.09%) | 26.99% (95% CI 21.82%-32.64%) | 2021-2023 rates |
| 2022 | 30.31% (95% CI 18.87%-41.42%) | 26.73% (95% CI 21.70%-32.49%) | 2021-2023 rates |
| 2023 | 33.43% (95% CI 22.11%-43.73%) | 30.33% (95% CI 25.13%-35.53%) | 2021-2023 rates |
| 2024 | 29.22% (95% CI 24.03%-35.43%) | 32.61% (95% CI 27.71%-37.96%) | 2024-2025 rates |
| 2025 | 27.70% (95% CI 22.03%-33.84%) | 31.36% (95% CI 26.25%-36.75%) | 2024-2025 rates |
| Change 2025 minus 2021, percentage points | -2.75 (95% CI -14.52 to 9.57) | 4.37 (95% CI 2.61-5.99) |  |

Post hoc analysis, 2026-10-31 (plan: revision_r1/ANALYSIS_PLAN_batch2d.md, committed before the analysis). It relaxes the assumption of the pre-specified correction (Multimedia Appendix 3, stance validation) that P(human label | model label) is the same every year. 253 of 300; excluded by publication year: 46 dated 2026 and 1 dated 2020; stratum x period cells with fewer than 10 records: 1 of 10; Jeffreys-drawn cells: Advocacy 6, critical 4.

(a) and (b): exact Clopper-Pearson 95% CIs; Fisher exact two-sided test of the period difference within each stratum. In (a) the first value column is 2021-2023 and the second 2024-2025; in (b) the same; in (c) the first value column is the period-specific estimate, the second the pre-specified constant-rate estimate, and the third the rates applied. The validation sample was stratified by model stance, not by year, so period cells are small.

(c): corrected prevalence for year y = sum over model strata of (share of year-y records with that model label) x P(human target | model label) for the period containing y; corpus = 14,058 records 2021-2025. Period-specific CIs: 1000 bootstrap draws (seed 42) resampling validation records within stratum x period, with a Jeffreys Beta(k+1/2, n-k+1/2) draw for cells with no or all events, and corpus records jointly. Constant-rate values are the pre-specified estimates (all 300 validation records); re-implemented here, they reproduce exactly. Critical stance was Alarm or Caution.


## QA (`final/QA_batch2d.md`)

- 
- The one token left is the journal count in the lexicon-table footnote (1215), read from the book row's CI-method field rather than its value.
- All new and `_v2` tables are real Word tables; format scan clean (no lowercase p, no leading zero, no 'Cohen's', no 4-digit comma, no en dash in ranges, no 'Wald CI' left in a v2 file).

## Checks

- `output/` checksums: worktree (189 files) and main checkout (174 files) identical to the post-Batch 2c manifests.
- No tracked Batch 2c file modified; `revision_r1/inputs/` read only.
- No LLM API call; no data fetch; nothing pushed.
