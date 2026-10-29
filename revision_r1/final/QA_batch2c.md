# QA · Batch 2c deliverables

Script: `revision_r1/final/scripts/c6_qa.py`. Book: `NUMBERS_BOOK_R1.csv` (2122 rows). Each table or caption is matched only against the book rows its builder read (strict check).

## 1. Numbers in tables and captions vs the numbers book

Numeric tokens checked: 7,312 in 48 tables/captions. Tokens matched to a book value or raw book field (at 0-3 decimals), or structural (years, CI level, seed, resample counts, small integers): 7,311. Tokens left for review: 1.

Every figure value is plotted from a book ID (lists: `figures/figure_ids_used.csv` and `ma/units/figures/*.json`), so figure-printed values match the book by construction; figure captions are checked as text below.

| Table or caption | Tokens | Not matched (token: context) |
|---|---|---|
| Main Table1 | 237 | none |
| Main Table2 | 417 | none |
| Main Table3 | 118 | none |
| Main Fig1_caption | 11 | none |
| Main Fig2_caption | 69 | none |
| Main Fig3_caption | 31 | none |
| Main Fig4_caption | 23 | none |
| Main Fig5_caption | 13 | none |
| Main Fig6_caption | 14 | none |
| MA3 unit advocacy_by_specialty | 197 | none |
| MA3 unit corpus_sensitivity | 354 | none |
| MA3 unit country | 229 | none |
| MA3 unit ea_vs_nawe_within_specialty | 142 | none |
| MA3 unit fda_mapping | 24 | `1430`: …; Physical Medicine / 4 /  / Total /  / 1430 /  / Cleared-device coun… |
| MA3 unit fda_robustness | 34 | none |
| MA3 unit fv_tier_verdict | 43 | none |
| MA3 unit keep_rate | 43 | none |
| MA3 unit lexicon_and_terms | 350 | none |
| MA3 unit mechanism_confusion | 83 | none |
| MA3 unit missing_data | 198 | none |
| MA3 unit precision | 91 | none |
| MA3 unit prefilter_validation | 336 | none |
| MA3 unit pubtype | 169 | none |
| MA3 unit q3_arm | 154 | none |
| MA3 unit region | 132 | none |
| MA3 unit regression_full | 1246 | none |
| MA3 unit review_subtypes | 70 | none |
| MA3 unit run_to_run | 18 | none |
| MA3 unit sjr_sensitivity | 987 | none |
| MA3 unit specialty_definitions | 51 | none |
| MA3 unit stance_confusion | 174 | none |
| MA3 unit stance_trend | 163 | none |
| MA3 unit symmetric_endorsement | 206 | none |
| MA3 unit theme_by_format | 118 | none |
| MA3 unit theme_validation | 310 | none |
| MA3 unit themes | 156 | none |
| MA3 unit update_2026 | 45 | none |
| MA3 unit within_genre | 91 | none |
| MA2 unit country_map_20_caption | 9 | none |
| MA2 unit forward_validation_sankey_caption | 7 | none |
| MA2 unit generative_share_fig_caption | 5 | none |
| MA2 unit lexicon_vs_llm_fig_caption | 47 | none |
| MA2 unit other_themes_fig_caption | 49 | none |
| MA2 unit q3_fig_caption | 9 | none |
| MA2 unit temporal_robustness_fig_caption | 5 | none |
| MA2 unit terms_fig_caption | 10 | none |
| MA2 unit theme_counts_fig_caption | 5 | none |
| MA2 unit within_genre_fig_caption | 19 | none |

Full list: `QA_unmatched_tokens.csv`.

## 2. JMIR figure compliance (Section 1, rule 7)

Fonts: base size 7 pt in both figure scripts; explicit font sizes below 7 pt in the code: none. Figures are drawn at final printed width (7.5 in), so 7 pt is the printed size.

| Figure | Simple bar graph? | Exact values printed | Asterisks | Title inside figure | PNG dpi / PDF | Palette | Stance colours | 2026 data |
|---|---|---|---|---|---|---|---|---|
| Fig1 | no (flowchart) | yes (all n) | none | none (panel letters and panel names only) | 600 / yes | Okabe-Ito | n/a | none |
| Fig2 | no (points + CIs) | yes | none | none (panel letters and panel names only) | 600 / yes | Okabe-Ito | fixed (Okabe-Ito) | none |
| Fig3 | no (100% composition + lines) | yes (table under bars) | none | none (panel letters and panel names only) | 600 / yes | Okabe-Ito | n/a | none |
| Fig4 | no (dot plot, two estimates) | yes | none | none (panel letters and panel names only) | 600 / yes | Okabe-Ito | n/a | none |
| Fig5 | no (map) | yes (bubble labels) | none | none (panel letters and panel names only) | 600 / yes | RdYlBu diverging (colour-blind safe) | n/a | none |
| Fig6 | no (3 outcomes per type) | yes | none | none (panel letters and panel names only) | 600 / yes | Okabe-Ito | fixed (Okabe-Ito) | none |
| country_map_20 | no (map) | yes (low-count overlaps in Table) | none | none (panel letters and panel names only) | 600 / yes | RdYlBu diverging (colour-blind safe) | n/a | none |
| forward_validation_sankey | no (Sankey, unchanged) | yes (submitted design) | none | none (panel letters and panel names only) | 144 / yes | submitted design (unchanged) | n/a | evidence window by design |
| generative_share_fig | no (scatter) | yes | none | none (panel letters and panel names only) | 600 / yes | Okabe-Ito | n/a | none |
| lexicon_vs_llm_fig | no (lines) | yes | none | none (panel letters and panel names only) | 600 / yes | Okabe-Ito | n/a | none |
| other_themes_fig | no (lines) | yes | none | none (panel letters and panel names only) | 600 / yes | Okabe-Ito | n/a | none |
| q3_fig | no (dot plot + lines) | yes | none | none (panel letters and panel names only) | 600 / yes | Okabe-Ito | fixed (Okabe-Ito) | none |
| temporal_robustness_fig | no (lines) | reference series and strong endorsement; others in MA3 tables | none | none (panel letters and panel names only) | 600 / yes | Okabe-Ito | n/a | none |
| terms_fig | no (dot plot) | yes | none | none (panel letters and panel names only) | 600 / yes | Okabe-Ito | n/a | none |
| theme_counts_fig | no (count bars + share line) | yes | none | none (panel letters and panel names only) | 600 / yes | Okabe-Ito | n/a | none |
| within_genre_fig | no (lines) | yes | none | none (panel letters and panel names only) | 600 / yes | Okabe-Ito | n/a | none |

The forward-validation Sankey is reproduced unchanged from the submission (PNG as submitted, 1484 x 1139 px, plus the repository SVG). At 6.6 in printed width it is about 225 pixels per inch, below the 300 dpi rule; a 300 dpi version needs the figure re-rendered from its source (the repository SVG carries an in-figure title that the submitted image cropped out), which was not done here because the figure is to stay unchanged.

## 3. 2026 content in figures

Book IDs with a 2026 window used by any figure: forward_validation_sankey: ['RES-FV-CAND'].

Mentions of 2026 in figure captions (none is plotted data):

- Fig1: …he R1 analysis window (2021-2025), which replaces the April 2026 cover-date cutoff; January-Ap…
- Fig1: …ch replaces the April 2026 cover-date cutoff; January-April 2026 records (n=10,757) appear onl…
- forward_validation_sankey: …d adjudicated against evidence published from 2024 to April 2026. Node height and ribbon width…
- forward_validation_sankey: …d from the submission (its evidence window extends to April 2026 by design). The Tier x verdic…

Figure 1 (flowchart) prints the retrieval period (January 2021-April 2026) and the exclusion counts of the window step (records published January-April 2026 or later); no 2026 data are analysed or plotted. The Sankey keeps its 2024-April 2026 evidence window by design. No other figure contains 2026.

## 4. Tables are real Word tables

| Document | Word tables | Inline images | Expected tables |
|---|---|---|---|
| tables/Table1.docx | 1 | 0 | 1 |
| tables/Table2.docx | 1 | 0 | 1 |
| tables/Table3.docx | 1 | 0 | 1 |
| ma/Multimedia_Appendix_3_R1.docx | 29 | 0 | 29 |
| ma/Multimedia_Appendix_1_R1.docx | 4 | 0 | Note 1, Note 9, Note 10 tables |
| ma/Multimedia_Appendix_2_R1.docx | 0 | 10 | 0 |

## 5. Note 2(a) prompt hash

- Note 2(a) (classify_stance.py): `b3949917159ea546ce7eb4c21224659be98c646aa937287d376f68c67992a39f`
- Production batch prompt (9c79cd5:classify_stance_batch.py), recomputed here: `b3949917159ea546ce7eb4c21224659be98c646aa937287d376f68c67992a39f`
- Equal: **True**
- Note 2(b) v2: `63761ee886a2de26f274b3148ca1886a69dd3ae52c26e7668467efd23315d254`; Note 8 B3: `27d28077cd7485fddcdfe4f0da3f4a3c13ad36a310bcd23f1544a5a89db50cf6`

## 6. Formatting scan (rule 6) over tables, captions and appendices

- lowercase p value (p=, p<): none
- leading zero in P (P=0.): none
- "Cohen's": none
- em dash in a caption: none
- comma in a 4-digit number: none
- en dash in a CI or range: none

Captions containing 'Critical stance was Alarm or Caution': Fig5_caption: yes, Fig2_caption: yes, Fig1_caption: yes, Fig4_caption: yes, Fig3_caption: yes, Fig6_caption: yes, within_genre_fig_caption: yes, other_themes_fig_caption: yes, temporal_robustness_fig_caption: yes, terms_fig_caption: yes, lexicon_vs_llm_fig_caption: yes, country_map_20_caption: yes, forward_validation_sankey_caption: yes, theme_counts_fig_caption: yes, q3_fig_caption: yes, generative_share_fig_caption: yes.

