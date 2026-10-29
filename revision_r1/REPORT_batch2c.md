# Batch 2c report · final figures, tables, appendices and numbers book (JMIR #109710, R1)

Branch `jmir-r1-major-revision`. Everything new is under `revision_r1/final/` except this report. No LLM API calls, no data fetches, no manuscript edits, nothing deleted or overwritten outside `final/`, nothing pushed.

## 1. Files

| Path (under `revision_r1/`) | Contents |
|---|---|
| `final/NUMBERS_BOOK_R1.md`, `final/NUMBERS_BOOK_R1.csv` | C1 numbers book: 2,122 numbers with stable IDs, JMIR format, window and source file; ends with the superseded-numbers list and the B7 corrections verbatim |
| `final/data/*.csv`, `*.json` | 2021-2025 recomputations behind the book (flow, subsets, missing data, specialty, region, country, publication type, review subtypes, FDA robustness, East Asia within specialty, theme by format, Advocacy by specialty, validation CIs, v2 trend, pooled themes, Q3, B5 annual, B2 recovered vs retained, confusion matrices, forward-validation counts) |
| `final/figures/Fig1-Fig6.{png,pdf}`, `Fig*_caption.md` | C2 main figures (PNG 600 dpi + vector PDF) and factual captions; `figure_ids_used.csv` lists the book IDs each figure plots |
| `final/tables/Table1-3.{docx,md}` | C3 main tables as real Word tables with footnotes; `table_ids_used.csv` |
| `final/ma/units/` | C4 units: 29 table specs (`tables/*.json`) and 10 figures (`figures/*.png/.pdf/_caption.md`) with the book IDs used |
| `final/ma/ma_order.yaml`, `final/ma/assemble.py` | Default order and the assembler |
| `final/ma/Multimedia_Appendix_2_R1.{docx,md}`, `Multimedia_Appendix_3_R1.{docx,md}`, `ma_numbering_map.csv` | Assembled appendices and the unit -> number map |
| `final/ma/Multimedia_Appendix_1_R1.{docx,md}`, `ma1_prompt_hashes.txt` | C5 corrected Supplementary Notes 1-10 |
| `final/QA_batch2c.md`, `final/QA_unmatched_tokens.csv` | C6 QA |
| `final/scripts/c_common.py`, `c_docx.py`, `c1_compute.py`, `c1_numbers_book.py`, `c2_figures.py`, `c3_tables.py`, `c4_units.py`, `c5_ma1.py`, `c6_qa.py`, `c7_report.py` | Scripts (c1_compute, c2, c4: project venv; others: `revision_r1/.venv`) |
| `final/requirements_batch2c.txt` | python-docx, lxml, PyYAML added to `revision_r1/.venv` (pinned) |
| `final/checksums/*_post_batch2c.sha256` | `output/` manifests after Batch 2c |

Run order: `c1_compute.py` -> `c1_numbers_book.py` -> `c2_figures.py` -> `c3_tables.py` -> `c4_units.py` -> `ma/assemble.py` -> `c5_ma1.py` -> `c6_qa.py` -> `c7_report.py`.

## 2. Analytic N and headline numbers (2021-2025)

- **Analytic N:** 14,058 records with a valid stance (discourse 7633, evaluative 6425); from 86,700 eligible Q1/Q2 records, 14,066 retained by the prefilter, 8 stance FAILED. January-April 2026: 2689 records, descriptive table only.
- **Prefilter audit:** estimated AI-engaged among excluded records 5.2% (95% CI 4.1%-8.9%); about 3747 (95% CI 2946-6447) records.
- **Overall:** critical 30.5% (4283/14,058; 95% CI 29.7%-31.2%); Cautious Optimism 62.9% (8836/14,058; 95% CI 62.0%-63.7%); Advocacy 1.6% (218/14,058; 95% CI 1.4%-1.8%).
- **Critical trend:** 25.4% (270/1063; 95% CI 22.8%-28.0%) (2021) to 31.0% (1828/5898; 95% CI 29.8%-32.3%) (2025); ρ=+0.80 (P=.133); unadjusted OR 1.077 per year (95% CI 1.046-1.108), P<.001; adjusted OR 1.103 per year (95% CI 1.066-1.141), P<.001.
- **Advocacy trend:** 2.9% (31/1063; 95% CI 1.9%-4.0%) to 1.1% (66/5898; 95% CI 0.9%-1.4%); ρ=-1.00 (P=.017); unadjusted OR 0.793 per year (95% CI 0.721-0.872), P<.001; adjusted OR 0.841 per year (95% CI 0.754-0.939), P=.002. Strong endorsement (B3): 10.8% (115/1063; 95% CI 9.1%-12.7%) to 6.6% (390/5898; 95% CI 6.0%-7.3%); OR 0.834 per year (95% CI 0.798-0.871), P<.001.
- **Themes (among 4283 critical records), OR per year:** patient safety OR 1.055 per year (95% CI 1.002-1.111), P=.041; hallucination/errors OR 1.367 per year (95% CI 1.296-1.442), P<.001; regulation OR 0.765 per year (95% CI 0.727-0.805), P<.001; ethics & bias OR 0.915 per year (95% CI 0.869-0.963), P<.001. Lexicon direction agrees for safety and errors, not for regulation (OR 1.128 per year (95% CI 1.062-1.198), P<.001) or ethics (OR 1.008 per year (95% CI 0.959-1.060), P=.753).
- **Mechanism:** hallucination-gated n=1775; fabrication-involved 0.0% (0/56; 95% CI 0.0%-0.0% (bootstrap); exact Clopper-Pearson 0.0%-6.4%) (2021) to 20.6% (182/883; 95% CI 18.0%-23.4%) (2025); generative share 5.3% (13/245; 95% CI 2.8%-8.2%) to 57.8% (1015/1757; 95% CI 55.5%-60.0%).
- **Specialty:** Mental Health / Psychiatry 50.3% (196/390) to Cardiology 16.1% (87/542); FDA (exploratory ecological): all 18 ρ=-0.61 (two-sided P=.007; one-sided P=.004; permutation one-sided P=.005); 11 non-zero ρ=-0.58 (two-sided P=.062; one-sided P=.031; permutation one-sided P=.036).
- **Geography:** United States 34.2% (1226/3586; 95% CI 32.7%-35.7%) vs China 14.9% (230/1540; 95% CI 13.2%-16.6%); adjusted OR 2.81 (95% CI 2.26-3.48), P<.001. East Asia 17.7% (478/2702; 95% CI 16.3%-19.3%); adjusted vs North America OR 0.44 (95% CI 0.38-0.51), P<.001. Countries with >=50 records: 32.
- **Publication format:** Reviews critical 24.3% (1120/4611; 95% CI 23.1%-25.5%), favourable 73.6% (3395/4611; 95% CI 72.3%-75.0%); adjusted Review vs Research Article OR 0.47 (95% CI 0.41-0.54), P<.001; opinion vs research χ²=376.1, df=4, P<.001, Cramér V=0.200; N=9447.
- **Validation:** stance quadratic κ 0.79 (95% CI 0.72-0.84) (in scope); themes micro-F1 0.885 (95% CI 0.855-0.914) (N=200); prefilter audit sensitivity 78.5% (95% CI 66.8%-81.7%), κ 0.842 (95% CI 0.713-0.856); model type κ 0.84 (95% CI 0.74-0.93); failure mode κ 0.57 (95% CI 0.46-0.69); specialty κ 0.75 (95% CI 0.66-0.83).

## 3. Multimedia Appendix order

Default order (Methods, then Results):

| Number | Unit ID | Title |
|---|---|---|
| MA2 Figure S1 | `within_genre_fig` | Annual critical share within each prefilter genre, 2021-2025. |
| MA2 Figure S2 | `temporal_robustness_fig` | Critical and Advocacy trends under alternative corpus definitions and a symmetric endorsement scale, 2021-2025. |
| MA2 Figure S3 | `q3_fig` | Stance in the Q1/Q2 analytic corpus and the Q3 comparison arm, 2021-2025. |
| MA2 Figure S4 | `other_themes_fig` | The six lower-prevalence concern themes among critical records, 2021-2025. |
| MA2 Figure S5 | `theme_counts_fig` | Annual count and prevalence share of the ten concern themes, 2021-2025. |
| MA2 Figure S6 | `lexicon_vs_llm_fig` | LLM theme prevalence and lexicon mention share for the four headline themes among critical records, 2021-2025. |
| MA2 Figure S7 | `terms_fig` | MeSH and keyword terms most over-represented by period and by stance, 2021-2025. |
| MA2 Figure S8 | `generative_share_fig` | Critical rate against generative-model share across the 18 specialty and domain categories, 2021-2025. |
| MA2 Figure S9 | `country_map_20` | Critical rate by country of first authorship at the 20-record threshold, 2021-2025. |
| MA2 Figure S10 | `forward_validation_sankey` | Exploratory forward-validation of early Advocacy predictions (unchanged; exploratory and Advocacy-only). |
| MA3 Table S1 | `prefilter_validation` | Validation of the AI-engagement prefilter: development pilot and R1 audit. |
| MA3 Table S2 | `stance_confusion` | Human versus model stance labels in the validation sample, with per-class agreement. |
| MA3 Table S3 | `run_to_run` | Run-to-run stability of the stance classifier at the provider-default temperature (unchanged). |
| MA3 Table S4 | `theme_validation` | Validation of the concern-theme classifier, per theme. |
| MA3 Table S5 | `mechanism_confusion` | Human versus model labels for the two mechanism axes. |
| MA3 Table S6 | `specialty_definitions` | The 18 specialty and domain categories with the verbatim definitions used in the classification prompt. |
| MA3 Table S7 | `fda_mapping` | Mapping of FDA lead review panels to the 18 specialty and domain categories (unchanged). |
| MA3 Table S8 | `missing_data` | Missing-data accounting for the 2021-2025 analytic corpus. |
| MA3 Table S9 | `precision` | Sample size and precision of the critical-share estimates, 2021-2025. |
| MA3 Table S10 | `stance_trend` | Per-stance temporal trend under the canonical v1 rubric and the stricter v2 rubric, 2021-2025. |
| MA3 Table S11 | `within_genre` | Annual critical share within each prefilter genre, 2021-2025. |
| MA3 Table S12 | `keep_rate` | Annual prefilter keep rate, 2021-2025. |
| MA3 Table S13 | `symmetric_endorsement` | Symmetric endorsement scale: re-classification of favourable records for strong endorsement (B3), 2021-2025. |
| MA3 Table S14 | `corpus_sensitivity` | Sensitivity of stance trends to the prefilter: recovered records and alternative corpora (B2), 2021-2025. |
| MA3 Table S15 | `sjr_sensitivity` | Sensitivity of the main estimates to an SJR medical-category restriction (B5), 2021-2025. |
| MA3 Table S16 | `q3_arm` | Stance in the Q1/Q2 analytic corpus and the Q3 comparison arm, 2021-2025. |
| MA3 Table S17 | `themes` | Prevalence and temporal trend of the ten concern themes among critical records, 2021-2025. |
| MA3 Table S18 | `lexicon_and_terms` | MeSH and keyword triangulation of the theme trends (B6), 2021-2025. |
| MA3 Table S19 | `fda_robustness` | Robustness of the association between critical rate and FDA cleared-device count across specialty categories, 2021-2025. |
| MA3 Table S20 | `country` | Critical rate by country of first authorship, countries with at least 20 records, 2021-2025. |
| MA3 Table S21 | `region` | Critical rate by first-author region, 2021-2025. |
| MA3 Table S22 | `ea_vs_nawe_within_specialty` | Critical rate within specialty, East Asian vs North American or Western European first authors, 2021-2025. |
| MA3 Table S23 | `pubtype` | Stance distribution by publication type, 2021-2025. |
| MA3 Table S24 | `review_subtypes` | Stance distribution within the two review subtypes, 2021-2025. |
| MA3 Table S25 | `theme_by_format` | Concern-theme prevalence among critical records, Reviews compared with Research Articles, 2021-2025. |
| MA3 Table S26 | `advocacy_by_specialty` | Advocacy records by specialty or domain category, 2021 and 2025. |
| MA3 Table S27 | `regression_full` | Multivariable models in full: Advocacy model, ordinal model and sensitivity models S1 to S4, 2021-2025. |
| MA3 Table S28 | `fv_tier_verdict` | Forward-validation of early Advocacy predictions: adjudicated verdicts by falsifiability tier (unchanged). |
| MA3 Table S29 | `update_2026` | Stance distribution among records published January to April 2026 (descriptive only). |

**To change it:** reorder the unit IDs in `final/ma/ma_order.yaml` (each ID once; no renaming), then run `revision_r1/.venv/bin/python revision_r1/final/ma/assemble.py`. The assembler renumbers S1, S2, ..., resolves every `{{F:id}}` / `{{T:id}}` cross-reference in captions and footnotes, rewrites both appendices (.docx and .md) and `ma_numbering_map.csv`, and stops if an ID is missing, duplicated or unresolved.

## 4. QA results (details: `final/QA_batch2c.md`)

1. **Numbers:** every numeric token in Tables 1-3, the 29 MA3 units and all 16 figure captions was matched against the book rows its builder read (strict per-unit check), with derived differences verified arithmetically. Tokens left for review: 1 (the FDA device column total, 1430, a sum of 18 book values that equals the submitted total). Figure values are plotted from book IDs.
2. **Figure rules:** no simple bar graphs; exact values printed on every panel (in the B2/B5 robustness figure for the reference series and strong endorsement, the other series' values are in MA3 tables); no asterisks; no in-figure titles; PNG 600 dpi plus PDF; base font 7 pt at final width, no smaller font set; Okabe-Ito palette, fixed stance colours; maps use a diverging RdYlBu scale. Exception: the unchanged forward-validation Sankey (below).
3. **2026:** no figure plots 2026 data. Figure 1 prints the retrieval period and the window-step exclusion counts (January-April 2026 n=10,757; May 2026 or later n=1134); the Sankey keeps its 2024-April 2026 evidence window.
4. **Word tables:** Tables 1-3 one real table each; MA3 29 real tables; MA1 4 (Notes 1, 9 and 10); no table is an image.
5. **Note 2(a) hash:** `b3949917…` equals the production prompt hash (recomputed from `9c79cd5:classify_stance_batch.py`).
6. **Format scan:** no lowercase p, no leading zero in P, no 'Cohen's', no em dash in a caption, no comma in a 4-digit number, no en dash in a range.

## 5. Not produced, deviations, and items for Peter

- **Advocacy categorical-year ORs:** not produced. B4 fitted the categorical-year model (S1) for the critical outcome only; fitting it for Advocacy would be a new analysis. Book row `RES-TMP-ADV-CAT` says so.
- **Sankey resolution:** reproduced unchanged from the submitted manuscript (1484 x 1139 px; about 225 pixels per inch at 6.6 in), below the 300 dpi rule. The repository SVG is supplied, but it carries an in-figure title the submitted image cropped out, and no SVG renderer is installed here. A 300 dpi version needs a re-render without the title.
- **Table 3:** B2 corpora and B5 have stance/region/publication-type values only where those analyses exist; recovered B2 records carry no theme, specialty or region label, and B5 did not recompute country, so those cells are '—' (footnoted).
- **Old Table S16 (specialty definitions):** definitions verbatim; the n column is updated to 2021-2025 (the submitted column counted the retired set). Old Table S2 (17 records of 2026) is replaced by the January-April 2026 descriptive table.
- **v2 rubric on 2021-2025 (Table S1 v2 column):** Cautious Optimism 55.5% to 58.5%; ρ=+0.20 (P=.783) vs v1 ρ=-0.60 (P=.350) (opposite direction); Advocacy 1.6% to 0.9%; ρ=-0.50 (P=.450) (same direction). Reported only.
- **B5 removed count:** 2325 of 14,058 records in 2021-2025 for D1 (the Batch 2b report's 2781 includes January-April 2026).
- **Two CIs for the unadjusted year OR:** Table 2 prints B4's cluster-robust interval (1.038-1.116); the temporal results and Table 3 print the record-level Wald interval (1.046-1.108). Same point estimate (1.077).
- **Within-genre CIs** use the B7 deterministic per-cell seeds (the corrected Table S3), not the T4 joint bootstrap; point estimates are identical.
- **Intra-rater κ interval** spans 0 to 1 (1 disagreement in 20); footnoted in Table 1.
- **Working title:** the appendices' title block uses 'Infoveillance Study of 14,058 High-Quartile Journal Abstracts, 2021-2025' with a note that the revised manuscript title may differ.
- **Q3 count:** 5463 Q3 records before the cutoff; the Q3 arm analysed in 2021-2025 has 853 records with a valid stance.
- **Main Figure 1 mentions 2026** only as exclusion counts of the window step, which the brief requires; flagged here because decision 2 says no 2026 element in any figure.

## 6. Checks

- `output/` checksums: worktree (189 files) and main checkout (174 files) identical to the post-Batch 2b manifests; new manifests in `final/checksums/`.
- No tracked file outside `revision_r1/final/` and this report was changed; `revision_r1/inputs/` read only (the submitted Sankey image and the MA1 Notes 3-7 text were read from the submitted .docx files).
- No LLM API call; no network data fetch (python-docx and PyYAML were installed into `revision_r1/.venv` from PyPI).
- Nothing pushed.
