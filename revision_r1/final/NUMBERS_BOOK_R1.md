# R1 numbers book

JMIR #109710, major revision R1, Batch 2c (C1). Every number the revised manuscript needs, recomputed on **2021-2025** unless the Window column says otherwise, in JMIR format, each with a stable ID and its source file. Machine-readable twin: `NUMBERS_BOOK_R1.csv` (columns: id, section, subsection, item, value, point, lo, hi, k, n, p, ci_method, window, source).

**Conventions.** n/N with every percentage; 95% CI for every estimate (method in the csv `ci_method` column; default: percentile bootstrap, 1000 resamples, seed 42); exact P with no leading zero and P<.001 at the floor; commas only in numbers >= 10,000; record-level ORs per year to 3 decimals, other ORs to 2. Critical stance = Alarm or Caution; favourable = Cautious Optimism or Advocacy. Paths are relative to `revision_r1/` unless they start with `output/` (repository) or `analysis/`.

**Scripts.** `final/scripts/c1_compute.py` (recomputations on 2021-2025 -> `final/data/`) and `final/scripts/c1_numbers_book.py` (this book).

## Corpus and flow


### Record flow (Figure 1)

| ID | Item | Value | Window | Source |
|---|---|---|---|---|
| COR-01 | Records identified in PubMed (monthly windows, January 2021-April 2026) | 129,557 | retrieval to 2021-2025 analytic set | final/data/flow_2021_2025.csv (from outputs/T6_*.csv and prefilter files) |
| COR-02 | Excluded: duplicate PMIDs across monthly windows | 13,440 | retrieval to 2021-2025 analytic set | final/data/flow_2021_2025.csv (from outputs/T6_*.csv and prefilter files) |
| COR-03 | Unique records | 116,117 | retrieval to 2021-2025 analytic set | final/data/flow_2021_2025.csv (from outputs/T6_*.csv and prefilter files) |
| COR-04 | Excluded: conference proceedings or preprints | 4106 | retrieval to 2021-2025 analytic set | final/data/flow_2021_2025.csv (from outputs/T6_*.csv and prefilter files) |
| COR-05 | Records screened for SJR quartile | 112,011 | retrieval to 2021-2025 analytic set | final/data/flow_2021_2025.csv (from outputs/T6_*.csv and prefilter files) |
| COR-06 | Excluded: not Q1/Q2 in SJR (unmatched) | 7922 | retrieval to 2021-2025 analytic set | final/data/flow_2021_2025.csv (from outputs/T6_*.csv and prefilter files) |
| COR-07 | of which journal title not in SJR file | 5092 | retrieval to 2021-2025 analytic set | final/data/flow_2021_2025.csv (from outputs/T6_*.csv and prefilter files) |
| COR-08 | of which listed with no quartile | 1494 | retrieval to 2021-2025 analytic set | final/data/flow_2021_2025.csv (from outputs/T6_*.csv and prefilter files) |
| COR-09 | of which best quartile Q4 | 1336 | retrieval to 2021-2025 analytic set | final/data/flow_2021_2025.csv (from outputs/T6_*.csv and prefilter files) |
| COR-10 | Set aside: best quartile Q3 (comparison arm) | 5463 | retrieval to 2021-2025 analytic set | final/data/flow_2021_2025.csv (from outputs/T6_*.csv and prefilter files) |
| COR-11 | Q1/Q2 records | 98,626 | retrieval to 2021-2025 analytic set | final/data/flow_2021_2025.csv (from outputs/T6_*.csv and prefilter files) |
| COR-12 | Excluded: outside the 2021-2025 window | 11,926 | retrieval to 2021-2025 analytic set | final/data/flow_2021_2025.csv (from outputs/T6_*.csv and prefilter files) |
| COR-13 | of which cover date May 2026 or later (not retained on disk) | 1134 | retrieval to 2021-2025 analytic set | final/data/flow_2021_2025.csv (from outputs/T6_*.csv and prefilter files) |
| COR-14 | of which published January-April 2026 | 10,757 | retrieval to 2021-2025 analytic set | final/data/flow_2021_2025.csv (from outputs/T6_*.csv and prefilter files) |
| COR-15 | of which dated before 2021 | 35 | retrieval to 2021-2025 analytic set | final/data/flow_2021_2025.csv (from outputs/T6_*.csv and prefilter files) |
| COR-16 | Q1/Q2 records eligible, 2021-2025 (screened by the AI-engagement prefilter) | 86,700 | retrieval to 2021-2025 analytic set | final/data/flow_2021_2025.csv (from outputs/T6_*.csv and prefilter files) |
| COR-17 | Excluded: application (AI used as a method) | 72,634 | retrieval to 2021-2025 analytic set | final/data/flow_2021_2025.csv (from outputs/T6_*.csv and prefilter files) |
| COR-18 | of which prefilter failures defaulted to application | 95 | retrieval to 2021-2025 analytic set | final/data/flow_2021_2025.csv (from outputs/T6_*.csv and prefilter files) |
| COR-19 | AI-engaged records retained | 14,066 | retrieval to 2021-2025 analytic set | final/data/flow_2021_2025.csv (from outputs/T6_*.csv and prefilter files) |
| COR-20 | discourse | 7637 | retrieval to 2021-2025 analytic set | final/data/flow_2021_2025.csv (from outputs/T6_*.csv and prefilter files) |
| COR-21 | evaluative | 6429 | retrieval to 2021-2025 analytic set | final/data/flow_2021_2025.csv (from outputs/T6_*.csv and prefilter files) |
| COR-22 | Excluded: stance unparseable (FAILED) | 8 | retrieval to 2021-2025 analytic set | final/data/flow_2021_2025.csv (from outputs/T6_*.csv and prefilter files) |
| COR-23 | Included in analysis (valid stance, 2021-2025) | 14,058 | retrieval to 2021-2025 analytic set | final/data/flow_2021_2025.csv (from outputs/T6_*.csv and prefilter files) |
| COR-24 | discourse | 7633 | retrieval to 2021-2025 analytic set | final/data/flow_2021_2025.csv (from outputs/T6_*.csv and prefilter files) |
| COR-25 | evaluative | 6425 | retrieval to 2021-2025 analytic set | final/data/flow_2021_2025.csv (from outputs/T6_*.csv and prefilter files) |
| COR-Q1Q2-PCT | Q1/Q2 share of records screened for SJR quartile | 88.1% (98,626/112,011) | retrieval | outputs/T6_stage_table.csv; output/sjr.log |
| COR-Q3-N | Q3 comparison arm, valid stance, 2021-2025 | 853 | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| COR-AUDIT-FN | Estimated AI-engaged among prefilter-excluded records (1-NPV, pooled 2021-2025) | 5.2% (95% CI 4.1%-8.9%) | 2021-2025 | outputs/B1/prefilter_exact_ci_long.csv |
| COR-AUDIT-MISSED | Estimated AI-engaged records missed by the prefilter, 2021-2025 | 3747 (95% CI 2946-6447) | 2021-2025 | outputs/B1/prefilter_exact_ci_long.csv |

### Downstream analytic subsets

| ID | Item | Value | Window | Source |
|---|---|---|---|---|
| COR-SUB-01 | Critical records (Alarm or Caution) | 4283 of 14,058 (30.5%) | 2021-2025 | final/data/subsets_2021_2025.csv |
| COR-SUB-02 | Critical records with a theme label | 4283 of 4283 (100.0%) | 2021-2025 | final/data/subsets_2021_2025.csv |
| COR-SUB-03 | Mechanism classification FAILED | 2 of 4283 (0.0%) | 2021-2025 | final/data/subsets_2021_2025.csv |
| COR-SUB-04 | Critical records with a parsed mechanism label | 4281 of 4283 (100.0%) | 2021-2025 | final/data/subsets_2021_2025.csv |
| COR-SUB-05 | Title-only records among parsed critical records | 375 of 4281 (8.8%) | 2021-2025 | final/data/subsets_2021_2025.csv |
| COR-SUB-06 | Abstract-present critical records (mechanism analyses) | 3906 of 4283 (91.2%) | 2021-2025 | final/data/subsets_2021_2025.csv |
| COR-SUB-07 | Hallucination-gated, abstract-present critical records | 1775 of 3906 (45.4%) | 2021-2025 | final/data/subsets_2021_2025.csv |
| COR-SUB-08 | Records with a valid specialty label | 14,048 of 14,058 (99.9%) | 2021-2025 | final/data/subsets_2021_2025.csv |
| COR-SUB-09 | Specialty classification FAILED | 10 of 14,058 (0.1%) | 2021-2025 | final/data/subsets_2021_2025.csv |
| COR-SUB-10 | Records with a resolved first-author country | 12,745 of 14,058 (90.7%) | 2021-2025 | final/data/subsets_2021_2025.csv |
| COR-SUB-11 | First-author country unresolved | 1313 of 14,058 (9.3%) | 2021-2025 | final/data/subsets_2021_2025.csv |
| COR-SUB-12 |   of which first-author affiliation empty | 239 of 14,058 (1.7%) | 2021-2025 | final/data/subsets_2021_2025.csv |
| COR-SUB-13 | Records with a known first-author region | 13,554 of 14,058 (96.4%) | 2021-2025 | final/data/subsets_2021_2025.csv |
| COR-SUB-14 | First-author region Unknown | 504 of 14,058 (3.6%) | 2021-2025 | final/data/subsets_2021_2025.csv |
| COR-SUB-15 | Title-only records in the analytic set | 892 of 14,058 (6.3%) | 2021-2025 | final/data/subsets_2021_2025.csv |
| COR-2026-N | January-April 2026 records with valid stance (descriptive table only) | 2689 | January-April 2026 | outputs/T4_2026_descriptive.csv |

## Missing data, 2021-2025 (E14)


### Losses by stage, records dated 2021-2025

| ID | Item | Value | Window | Source |
|---|---|---|---|---|
| MIS-01 | Conference proceedings / preprints | 3897 (2021: 409; 2022: 438; 2023: 615; 2024: 1006; 2025: 1429) | 2021-2025 | final/data/missing_2021_2025.csv (from outputs/T6_losses_by_year.csv) |
| MIS-02 | SJR title matching | 7021 (2021: 822; 2022: 1190; 2023: 1156; 2024: 1598; 2025: 2255) | 2021-2025 | final/data/missing_2021_2025.csv (from outputs/T6_losses_by_year.csv) |
| MIS-03 | April 2026 cover-date cutoff (Q1/Q2) | 0 (2021: 0; 2022: 0; 2023: 0; 2024: 0; 2025: 0) | 2021-2025 | final/data/missing_2021_2025.csv (from outputs/T6_losses_by_year.csv) |
| MIS-04 | AI-engagement prefilter | 72,634 (2021: 10127; 2022: 11792; 2023: 12073; 2024: 15668; 2025: 22974) | 2021-2025 | final/data/missing_2021_2025.csv (from outputs/T6_losses_by_year.csv) |
| MIS-05 | of which: prefilter failures defaulted to application (T1) | 95 (2021: 87; 2022: 0; 2023: 0; 2024: 2; 2025: 6) | 2021-2025 | final/data/missing_2021_2025.csv (from outputs/T6_losses_by_year.csv) |
| MIS-06 | Stance classification | 8 (2021: 1; 2022: 1; 2023: 1; 2024: 4; 2025: 1) | 2021-2025 | final/data/missing_2021_2025.csv (from outputs/T6_losses_by_year.csv) |
| MIS-07 | Year window 2021–2026 | 0 (2021: 0; 2022: 0; 2023: 0; 2024: 0; 2025: 0) | 2021-2025 | final/data/missing_2021_2025.csv (from outputs/T6_losses_by_year.csv) |
| MIS-08 | Mechanism classification | 2 (2021: 0; 2022: 0; 2023: 1; 2024: 1; 2025: 0) | 2021-2025 | final/data/missing_2021_2025.csv (from outputs/T6_losses_by_year.csv) |
| MIS-09 | Title-only records within the parsed critical set | 375 (2021: 25; 2022: 48; 2023: 80; 2024: 151; 2025: 71) | 2021-2025 | final/data/missing_2021_2025.csv (from outputs/T6_losses_by_year.csv) |
| MIS-10 | Specialty classification (analytic set) | 10 (2021: 0; 2022: 2; 2023: 1; 2024: 2; 2025: 5) | 2021-2025 | final/data/missing_2021_2025.csv (from outputs/T6_losses_by_year.csv) |
| MIS-11 | First-author country (Figure 4 / Table S7 resolver) | 1313 (2021: 80; 2022: 99; 2023: 207; 2024: 396; 2025: 531) | 2021-2025 | final/data/missing_2021_2025.csv (from outputs/T6_losses_by_year.csv) |
| MIS-12 | First-author region (Table S9; geography_classifications.csv) | 504 (2021: 46; 2022: 48; 2023: 94; 2024: 163; 2025: 153) | 2021-2025 | final/data/missing_2021_2025.csv (from outputs/T6_losses_by_year.csv) |

### Title-only (empty abstract) records by stage

| ID | Item | Value | Window | Source |
|---|---|---|---|---|
| MIS-TO-01 | raw (116,117) | 1.5% (1491/102,480) | 2021-2025 | final/data/title_only_2021_2025.csv (from outputs/T6_title_only_by_stage.csv) |
| MIS-TO-02 | excluded conf/preprint | 0.1% (2/3897) | 2021-2025 | final/data/title_only_2021_2025.csv (from outputs/T6_title_only_by_stage.csv) |
| MIS-TO-03 | SJR unmatched | 1.7% (118/7021) | 2021-2025 | final/data/title_only_2021_2025.csv (from outputs/T6_title_only_by_stage.csv) |
| MIS-TO-04 | Q1/Q2 eligible (97,492) | 1.5% (1291/86,700) | 2021-2025 | final/data/title_only_2021_2025.csv (from outputs/T6_title_only_by_stage.csv) |
| MIS-TO-05 | prefilter: application | 0.5% (399/72,634) | 2021-2025 | final/data/title_only_2021_2025.csv (from outputs/T6_title_only_by_stage.csv) |
| MIS-TO-06 | prefilter: retained (16,759) | 6.3% (892/14,066) | 2021-2025 | final/data/title_only_2021_2025.csv (from outputs/T6_title_only_by_stage.csv) |
| MIS-TO-07 | stance valid, 2021–2026 (16,747) | 6.3% (892/14,058) | 2021-2025 | final/data/title_only_2021_2025.csv (from outputs/T6_title_only_by_stage.csv) |
| MIS-TO-08 | critical (5,161) | 8.8% (375/4283) | 2021-2025 | final/data/title_only_2021_2025.csv (from outputs/T6_title_only_by_stage.csv) |

### Handling rules

| ID | Item | Value | Window | Source |
|---|---|---|---|---|
| MIS-NOTE-01 | Handling of missing values | Complete-case: records with a FAILED or missing label for a variable are excluded from analyses of that variable only; no imputation. Unknown region is kept as its own level in regression (B4). | 2021-2025 | outputs/T6_missing_data.md; outputs/B4/B4_regression.md |

## Sample size and precision (E2/E8)


### Design statement

| ID | Item | Value | Window | Source |
|---|---|---|---|---|
| PRE-00 | Sample size | The analytic corpus is a census of all eligible Q1/Q2 records published 2021-2025 that the prefilter retained (n=14,058); no sample was drawn and no power calculation applies. Precision is reported as the 95% CI half-width. | 2021-2025 | final/data/flow_2021_2025.csv |

### Overall

| ID | Item | Value | Window | Source |
|---|---|---|---|---|
| PRE-ALL | Critical share, all records: n and 95% CI half-width | n=14,058; half-width 0.8 percentage points | 2021-2025 | outputs/T5_crosssectional_both_windows.csv |

### By year

| ID | Item | Value | Window | Source |
|---|---|---|---|---|
| PRE-YR-2021 | Critical share 2021: n and half-width | n=1063; half-width 2.6 percentage points | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| PRE-YR-2022 | Critical share 2022: n and half-width | n=1343; half-width 2.2 percentage points | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| PRE-YR-2023 | Critical share 2023: n and half-width | n=2054; half-width 2.1 percentage points | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| PRE-YR-2024 | Critical share 2024: n and half-width | n=3700; half-width 1.5 percentage points | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| PRE-YR-2025 | Critical share 2025: n and half-width | n=5898; half-width 1.2 percentage points | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |

### By specialty

| ID | Item | Value | Window | Source |
|---|---|---|---|---|
| PRE-SPC-RADIOLOGYDIAGNOSTICIMAGI | Radiology / Diagnostic Imaging: n and half-width | n=1769; half-width 1.9 percentage points | 2021-2025 | final/data/specialty_2021_2025.csv |
| PRE-SPC-PATHOLOGYLABORATORYMEDIC | Pathology / Laboratory Medicine: n and half-width | n=398; half-width 4.1 percentage points | 2021-2025 | final/data/specialty_2021_2025.csv |
| PRE-SPC-CARDIOLOGY | Cardiology: n and half-width | n=542; half-width 3.2 percentage points | 2021-2025 | final/data/specialty_2021_2025.csv |
| PRE-SPC-ONCOLOGY | Oncology: n and half-width | n=1211; half-width 2.2 percentage points | 2021-2025 | final/data/specialty_2021_2025.csv |
| PRE-SPC-SURGERY | Surgery: n and half-width | n=1191; half-width 2.7 percentage points | 2021-2025 | final/data/specialty_2021_2025.csv |
| PRE-SPC-OPHTHALMOLOGY | Ophthalmology: n and half-width | n=669; half-width 3.0 percentage points | 2021-2025 | final/data/specialty_2021_2025.csv |
| PRE-SPC-DERMATOLOGY | Dermatology: n and half-width | n=265; half-width 5.7 percentage points | 2021-2025 | final/data/specialty_2021_2025.csv |
| PRE-SPC-NEUROLOGYNEUROSCIENCE | Neurology / Neuroscience: n and half-width | n=290; half-width 4.9 percentage points | 2021-2025 | final/data/specialty_2021_2025.csv |
| PRE-SPC-MENTALHEALTHPSYCHIATRY | Mental Health / Psychiatry: n and half-width | n=390; half-width 4.8 percentage points | 2021-2025 | final/data/specialty_2021_2025.csv |
| PRE-SPC-INTERNALMEDICINEPRIMARYC | Internal Medicine / Primary Care: n and half-width | n=936; half-width 2.6 percentage points | 2021-2025 | final/data/specialty_2021_2025.csv |
| PRE-SPC-EMERGENCYMEDICINECRITICA | Emergency Medicine / Critical Care: n and half-width | n=308; half-width 5.0 percentage points | 2021-2025 | final/data/specialty_2021_2025.csv |
| PRE-SPC-PEDIATRICS | Pediatrics: n and half-width | n=303; half-width 4.7 percentage points | 2021-2025 | final/data/specialty_2021_2025.csv |
| PRE-SPC-OBSTETRICSGYNECOLOGY | Obstetrics / Gynecology: n and half-width | n=195; half-width 6.2 percentage points | 2021-2025 | final/data/specialty_2021_2025.csv |
| PRE-SPC-DENTISTRY | Dentistry: n and half-width | n=581; half-width 3.6 percentage points | 2021-2025 | final/data/specialty_2021_2025.csv |
| PRE-SPC-MEDICALINFORMATICSDIGITA | Medical Informatics / Digital Health: n and half-width | n=3701; half-width 1.6 percentage points | 2021-2025 | final/data/specialty_2021_2025.csv |
| PRE-SPC-NURSING | Nursing: n and half-width | n=227; half-width 6.5 percentage points | 2021-2025 | final/data/specialty_2021_2025.csv |
| PRE-SPC-MEDICALEDUCATION | Medical Education: n and half-width | n=876; half-width 3.2 percentage points | 2021-2025 | final/data/specialty_2021_2025.csv |
| PRE-SPC-MULTIDISCIPLINARYOTHER | Multidisciplinary / Other: n and half-width | n=196; half-width 6.9 percentage points | 2021-2025 | final/data/specialty_2021_2025.csv |

### By region

| ID | Item | Value | Window | Source |
|---|---|---|---|---|
| PRE-REG-EASTASIA | East Asia: n and half-width | n=2702; half-width 1.5 percentage points | 2021-2025 | final/data/region_2021_2025.csv |
| PRE-REG-EASTERNEUROPE | Eastern Europe: n and half-width | n=272; half-width 5.5 percentage points | 2021-2025 | final/data/region_2021_2025.csv |
| PRE-REG-LATINAMERICAOCEANIA | Latin America / Oceania: n and half-width | n=639; half-width 3.8 percentage points | 2021-2025 | final/data/region_2021_2025.csv |
| PRE-REG-MIDDLEEASTNORTHAFRICA | Middle East / North Africa: n and half-width | n=1322; half-width 2.6 percentage points | 2021-2025 | final/data/region_2021_2025.csv |
| PRE-REG-NORTHAMERICA | North America: n and half-width | n=4221; half-width 1.4 percentage points | 2021-2025 | final/data/region_2021_2025.csv |
| PRE-REG-SOUTHSOUTHEASTASIA | South/Southeast Asia: n and half-width | n=656; half-width 3.2 percentage points | 2021-2025 | final/data/region_2021_2025.csv |
| PRE-REG-SUBSAHARANAFRICA | Sub-Saharan Africa: n and half-width | n=49; half-width 14.0 percentage points | 2021-2025 | final/data/region_2021_2025.csv |
| PRE-REG-UNKNOWN | Unknown: n and half-width | n=504; half-width 3.9 percentage points | 2021-2025 | final/data/region_2021_2025.csv |
| PRE-REG-WESTERNEUROPE | Western Europe: n and half-width | n=3693; half-width 1.5 percentage points | 2021-2025 | final/data/region_2021_2025.csv |

### By publication type

| ID | Item | Value | Window | Source |
|---|---|---|---|---|
| PRE-PT-RESEARCHARTICLE | Research Article: n and half-width | n=8556; half-width 1.0 percentage points | 2021-2025 | final/data/pubtype_stance.csv |
| PRE-PT-REVIEW | Review: n and half-width | n=4611; half-width 1.2 percentage points | 2021-2025 | final/data/pubtype_stance.csv |
| PRE-PT-LETTER | Letter: n and half-width | n=429; half-width 4.7 percentage points | 2021-2025 | final/data/pubtype_stance.csv |
| PRE-PT-EDITORIAL | Editorial: n and half-width | n=364; half-width 4.9 percentage points | 2021-2025 | final/data/pubtype_stance.csv |
| PRE-PT-COMMENTARY | Commentary: n and half-width | n=98; half-width 10.2 percentage points | 2021-2025 | final/data/pubtype_stance.csv |

## Validation (Table 1)


### Prefilter, development pilot (T1)

| ID | Item | Value | Window | Source |
|---|---|---|---|---|
| VAL-PF-PILOT-DESIGN | Design | 200 records; sampling undocumented (year mix consistent with simple random sampling of eligible records, χ²=2.57, df=5, P=.77); one coder; no written codebook; 3 classes | validation sample | outputs/T1_prefilter_validation.md |
| VAL-PF-PILOT-RAW | 3-class raw agreement | 85.5% (171/200) | validation sample | outputs/T1_prefilter_validation.md |
| VAL-PF-PILOT-K3 | 3-class Cohen κ | 0.511 (95% CI 0.345-0.646) | validation sample | outputs/T1_prefilter_validation.md |
| VAL-PF-PILOT-SENSITIVITY | KEEP sensitivity | 52.6% (20/38; 95% CI 37.0%-67.6%) | validation sample | outputs/T1_binary_keep_drop_metrics.csv |
| VAL-PF-PILOT-SPECIFICITY | KEEP specificity | 93.8% (152/162; 95% CI 89.8%-97.0%) | validation sample | outputs/T1_binary_keep_drop_metrics.csv |
| VAL-PF-PILOT-PPV | PPV | 66.7% (20/30; 95% CI 48.0%-82.4%) | validation sample | outputs/T1_binary_keep_drop_metrics.csv |
| VAL-PF-PILOT-NPV | NPV | 89.4% (152/170; 95% CI 84.8%-93.7%) | validation sample | outputs/T1_binary_keep_drop_metrics.csv |
| VAL-PF-PILOT-KAPPA | KEEP/DROP Cohen κ | 0.505 (95% CI 0.331-0.646) | validation sample | outputs/T1_binary_keep_drop_metrics.csv |
| VAL-PF-PILOT-AC1 | KEEP/DROP Gwet AC1 | 0.805 (95% CI 0.728-0.871) | validation sample | outputs/T1_binary_keep_drop_metrics.csv |

### Prefilter, R1 audit (A3; Amendments 2-3)

| ID | Item | Value | Window | Source |
|---|---|---|---|---|
| VAL-PF-AUDIT-DESIGN | Design | 370 records stratified by prefilter outcome x year 2021-2025 (EX-F 75; EX-S 225; RET 50; PILOT 20); design-weighted to frame sizes; codebook verbatim from the classifier prompt; one coder blinded to model labels and stratum; frozen protocol (commits 0d21f6c, 47cf6fe) | validation sample | coding/PROTOCOL_r1_validation.md |
| VAL-PF-AUDIT-PROD2X2SENSITIVITY | Production prefilter sensitivity (population-weighted) | 78.5% (95% CI 66.8%-81.7%) | 2021-2025 frame | outputs/B1/prefilter_exact_ci_long.csv |
| VAL-PF-AUDIT-PROD2X2SPECIFICITY | Production prefilter specificity | 99.5% (95% CI 97.0%-99.6%) | 2021-2025 frame | outputs/B1/prefilter_exact_ci_long.csv |
| VAL-PF-AUDIT-PROD2X2PPV | Production prefilter PPV | 97.6% (95% CI 84.8%-98.1%) | 2021-2025 frame | outputs/B1/prefilter_exact_ci_long.csv |
| VAL-PF-AUDIT-PROD2X2NPV | Production prefilter NPV | 94.8% (95% CI 91.1%-95.9%) | 2021-2025 frame | outputs/B1/prefilter_exact_ci_long.csv |
| VAL-PF-AUDIT-PROD2X2KAPPA | Production prefilter Cohen κ | 0.842 (95% CI 0.713-0.856) | 2021-2025 frame | outputs/B1/prefilter_exact_ci_long.csv |
| VAL-PF-AUDIT-PROD2X2AC1 | Production prefilter Gwet AC1 | 0.933 (95% CI 0.873-0.941) | 2021-2025 frame | outputs/B1/prefilter_exact_ci_long.csv |
| VAL-PF-AUDIT-FNRATEPOOLED | False-negative rate among excluded records (1-NPV), pooled | 5.2% (95% CI 4.1%-8.9%) | 2021-2025 frame | outputs/B1/prefilter_exact_ci_long.csv |
| VAL-PF-AUDIT-FNRATE20212022 | 1-NPV, 2021-2022 | 3.3% (95% CI 2.3%-8.2%) | 2021-2025 frame | outputs/B1/prefilter_exact_ci_long.csv |
| VAL-PF-AUDIT-FNRATE20242025 | 1-NPV, 2024-2025 | 5.7% (95% CI 3.8%-11.4%) | 2021-2025 frame | outputs/B1/prefilter_exact_ci_long.csv |
| VAL-PF-AUDIT-FNRATEDIFF202425MINUS202 | 1-NPV difference, 2024-2025 minus 2021-2022 (percentage points) | +2.5 percentage points (95% CI -2.5 to 7.6) | 2021-2025 frame | outputs/B1/prefilter_exact_ci_long.csv |
| VAL-PF-AUDIT-MISSEDTOTAL | Estimated missed AI-engaged records, 2021-2025 | 3747 (95% CI 2946-6447) | 2021-2025 frame | outputs/B1/prefilter_exact_ci_long.csv |
| VAL-PF-AUDIT-PPVRETPOOLED | PPV among retained records, pooled | 97.6% (95% CI 84.8%-98.1%) | 2021-2025 frame | outputs/B1/prefilter_exact_ci_long.csv |
| VAL-PF-AUDIT-FULLABSPRECISIONPOOLED | Full-abstract re-run precision (EX-F), pooled | 80.4% (95% CI 69.0%-86.2%) | 2021-2025 frame | outputs/B1/prefilter_exact_ci_long.csv |
| VAL-PF-AUDIT-FNRATE2021 | 1-NPV, 2021 | 2.0% (95% CI 1.6%-7.3%) | 2021-2025 frame | outputs/B1/prefilter_exact_ci_long.csv |
| VAL-PF-AUDIT-FNRATE2022 | 1-NPV, 2022 | 4.4% (95% CI 2.3%-11.9%) | 2021-2025 frame | outputs/B1/prefilter_exact_ci_long.csv |
| VAL-PF-AUDIT-FNRATE2023 | 1-NPV, 2023 | 6.7% (95% CI 3.2%-15.2%) | 2021-2025 frame | outputs/B1/prefilter_exact_ci_long.csv |
| VAL-PF-AUDIT-FNRATE2024 | 1-NPV, 2024 | 2.6% (95% CI 2.0%-7.6%) | 2021-2025 frame | outputs/B1/prefilter_exact_ci_long.csv |
| VAL-PF-AUDIT-FNRATE2025 | 1-NPV, 2025 | 7.9% (95% CI 4.4%-16.5%) | 2021-2025 frame | outputs/B1/prefilter_exact_ci_long.csv |
| VAL-PF-AUDIT-MISSED2021 | Estimated missed records, 2021 | 202 (95% CI 158-736) | 2021-2025 frame | outputs/B1/prefilter_exact_ci_long.csv |
| VAL-PF-AUDIT-MISSED2022 | Estimated missed records, 2022 | 518 (95% CI 272-1404) | 2021-2025 frame | outputs/B1/prefilter_exact_ci_long.csv |
| VAL-PF-AUDIT-MISSED2023 | Estimated missed records, 2023 | 812 (95% CI 391-1826) | 2021-2025 frame | outputs/B1/prefilter_exact_ci_long.csv |
| VAL-PF-AUDIT-MISSED2024 | Estimated missed records, 2024 | 404 (95% CI 306-1182) | 2021-2025 frame | outputs/B1/prefilter_exact_ci_long.csv |
| VAL-PF-AUDIT-MISSED2025 | Estimated missed records, 2025 | 1812 (95% CI 1003-3779) | 2021-2025 frame | outputs/B1/prefilter_exact_ci_long.csv |
| VAL-PF-AUDIT-FULL2X2SENSITIVITY | Full-abstract re-run sensitivity | 82.0% (95% CI 72.1%-91.9%) | 2021-2025 frame | outputs/B1/prefilter_exact_ci_long.csv |
| VAL-PF-AUDIT-FULL2X2SPECIFICITY | Full-abstract specificity | 99.3% (95% CI 99.0%-99.6%) | 2021-2025 frame | outputs/B1/prefilter_exact_ci_long.csv |
| VAL-PF-AUDIT-FULL2X2PPV | Full-abstract PPV | 96.8% (95% CI 95.2%-98.2%) | 2021-2025 frame | outputs/B1/prefilter_exact_ci_long.csv |
| VAL-PF-AUDIT-FULL2X2NPV | Full-abstract NPV | 95.6% (95% CI 92.9%-98.1%) | 2021-2025 frame | outputs/B1/prefilter_exact_ci_long.csv |
| VAL-PF-AUDIT-FULL2X2KAPPA | Full-abstract Cohen κ | 0.862 (95% CI 0.785-0.931) | 2021-2025 frame | outputs/B1/prefilter_exact_ci_long.csv |
| VAL-PF-INTRA-AGREE | Intra-rater agreement, KEEP/DROP (20 pilot records recoded) | 95.0% (19/20; 95% CI 75.1%-99.9%) | validation sample | final/data/validation_ci.csv |
| VAL-PF-INTRA-AGREE3 | Intra-rater agreement, 3-class | 95.0% (19/20; 95% CI 75.1%-99.9%) | validation sample | final/data/validation_ci.csv |
| VAL-PF-INTRA-K | Intra-rater Cohen κ, KEEP/DROP | 0.773 (95% CI 0.000-1.000) | validation sample | final/data/validation_ci.csv |

### Stance (Table S18; T2)

| ID | Item | Value | Window | Source |
|---|---|---|---|---|
| VAL-ST-DESIGN | Design | 300 records stratified by model-assigned stance (Alarm 40, Caution 60, Neutral 70, Cautious Optimism 100, Advocacy 30), abstract-present records only; one coder blinded to model labels; in-scope layer excludes 75 records the coder flagged as not codable or out of scope | validation sample | outputs/T2_stance_perclass.md |
| VAL-ST-QK-225 | Quadratic-weighted Cohen κ, in-scope (n=225) | 0.79 (95% CI 0.72-0.84) | validation sample | final/data/validation_ci.csv |
| VAL-ST-QK-300 | Quadratic-weighted Cohen κ, all records (n=300) | 0.75 (95% CI 0.68-0.81) | validation sample | final/data/validation_ci.csv |
| VAL-ST-UK-225 | Unweighted Cohen κ, in-scope | 0.56 (95% CI 0.47-0.64) | validation sample | final/data/validation_ci.csv |
| VAL-ST-RAW-225 | Exact agreement, in-scope | 67.6% (152/225; 95% CI 61.0%-73.6%) | validation sample | final/data/validation_ci.csv |
| VAL-ST-RAW-300 | Exact agreement, all records | 66.7% (200/300; 95% CI 61.0%-72.0%) | validation sample | final/data/validation_ci.csv |
| VAL-ST-MACROF1-225 | Macro-F1 (5 classes), n=225 | 0.67 (95% CI 0.59-0.73) | validation sample | outputs/T2_perclass_inscope225.csv |
| VAL-ST-F1-ALARM-225 | Alarm: precision / recall / F1, n=225 | precision 0.78 (95% CI 0.62-0.89); recall 0.86 (95% CI 0.73-0.97); F1 0.82 (95% CI 0.70-0.90); support 36 | validation sample | outputs/T2_perclass_inscope225.csv |
| VAL-ST-F1-CAUTION-225 | Caution: precision / recall / F1, n=225 | precision 0.66 (95% CI 0.53-0.79); recall 0.57 (95% CI 0.44-0.68); F1 0.61 (95% CI 0.49-0.71); support 58 | validation sample | outputs/T2_perclass_inscope225.csv |
| VAL-ST-F1-NEUTRAL-225 | Neutral: precision / recall / F1, n=225 | precision 0.43 (95% CI 0.23-0.65); recall 0.71 (95% CI 0.44-0.93); F1 0.54 (95% CI 0.32-0.71); support 14 | validation sample | outputs/T2_perclass_inscope225.csv |
| VAL-ST-F1-CAUTIOUSOPTIMISM-225 | Cautious Optimism: precision / recall / F1, n=225 | precision 0.71 (95% CI 0.61-0.80); recall 0.66 (95% CI 0.55-0.75); F1 0.68 (95% CI 0.59-0.76); support 93 | validation sample | outputs/T2_perclass_inscope225.csv |
| VAL-ST-F1-ADVOCACY-225 | Advocacy: precision / recall / F1, n=225 | precision 0.65 (95% CI 0.46-0.83); recall 0.71 (95% CI 0.50-0.89); F1 0.68 (95% CI 0.51-0.81); support 24 | validation sample | outputs/T2_perclass_inscope225.csv |
| VAL-ST-MACROF1-300 | Macro-F1 (5 classes), n=300 | 0.67 (95% CI 0.62-0.73) | validation sample | outputs/T2_perclass_all300.csv |
| VAL-ST-F1-ALARM-300 | Alarm: precision / recall / F1, n=300 | precision 0.78 (95% CI 0.64-0.90); recall 0.86 (95% CI 0.74-0.97); F1 0.82 (95% CI 0.71-0.90); support 36 | validation sample | outputs/T2_perclass_all300.csv |
| VAL-ST-F1-CAUTION-300 | Caution: precision / recall / F1, n=300 | precision 0.57 (95% CI 0.44-0.69); recall 0.58 (95% CI 0.45-0.69); F1 0.57 (95% CI 0.46-0.67); support 59 | validation sample | outputs/T2_perclass_all300.csv |
| VAL-ST-F1-NEUTRAL-300 | Neutral: precision / recall / F1, n=300 | precision 0.81 (95% CI 0.72-0.90); recall 0.65 (95% CI 0.55-0.74); F1 0.72 (95% CI 0.64-0.79); support 88 | validation sample | outputs/T2_perclass_all300.csv |
| VAL-ST-F1-CAUTIOUSOPTIMISM-300 | Cautious Optimism: precision / recall / F1, n=300 | precision 0.61 (95% CI 0.51-0.70); recall 0.66 (95% CI 0.56-0.74); F1 0.63 (95% CI 0.55-0.71); support 93 | validation sample | outputs/T2_perclass_all300.csv |
| VAL-ST-F1-ADVOCACY-300 | Advocacy: precision / recall / F1, n=300 | precision 0.57 (95% CI 0.38-0.75); recall 0.71 (95% CI 0.53-0.88); F1 0.63 (95% CI 0.45-0.77); support 24 | validation sample | outputs/T2_perclass_all300.csv |
| VAL-ST-ADV-SENSITIVITY-225 | Advocacy sensitivity, n=225 | 70.8% (17/24; 95% CI 50.0%-88.9%) | validation sample | outputs/T2_collapsed_views.csv |
| VAL-ST-ADV-PPV-225 | Advocacy PPV, n=225 | 65.4% (17/26; 95% CI 46.4%-83.3%) | validation sample | outputs/T2_collapsed_views.csv |
| VAL-ST-ADV-SENSITIVITY-300 | Advocacy sensitivity, n=300 | 70.8% (17/24; 95% CI 52.6%-88.0%) | validation sample | outputs/T2_collapsed_views.csv |
| VAL-ST-ADV-PPV-300 | Advocacy PPV, n=300 | 56.7% (17/30; 95% CI 37.5%-75.0%) | validation sample | outputs/T2_collapsed_views.csv |
| VAL-ST-RTR-QK | Run-to-run stability (two re-inferences at T=1.0): quadratic-weighted κ | 0.974 (95% CI 0.956-0.989) | validation sample | final/data/validation_ci.csv |
| VAL-ST-RTR-RAW | Run-to-run stability: raw agreement | 95.3% (286/300; 95% CI 92.3%-97.4%) | validation sample | final/data/validation_ci.csv |

### Themes (A1; Amendment 1)

| ID | Item | Value | Window | Source |
|---|---|---|---|---|
| VAL-TH-DESIGN | Design | 200 critical records 2021-2025, 40 per year by simple random sampling within year (frame 4283); one coder blinded to model labels; codebook verbatim from the classifier prompt; frozen protocol (commit 0d21f6c); primary analysis N=200 (Amendment 1), pre-specified analysis N=187 | validation sample | coding/PROTOCOL_r1_validation.md |
| VAL-TH-MICRO-200-UN | Micro-F1, N=200, unweighted | 0.885 (95% CI 0.855-0.914) | validation sample | outputs/A4_theme_primary_n200/theme_scores.md |
| VAL-TH-MACRO-200-UN | Macro-F1, N=200, unweighted | 0.824 (95% CI 0.747-0.881) | validation sample | outputs/A4_theme_primary_n200/theme_scores.md |
| VAL-TH-MICRO-200-WE | Micro-F1, N=200, weighted | 0.888 (95% CI 0.853-0.919) | validation sample | outputs/A4_theme_primary_n200/theme_scores.md |
| VAL-TH-MACRO-200-WE | Macro-F1, N=200, weighted | 0.813 (95% CI 0.727-0.881) | validation sample | outputs/A4_theme_primary_n200/theme_scores.md |
| VAL-TH-F1-HALLUCINATIONERRORS-200 | Hallucination / errors: F1 (unweighted), N=200 | F1 0.897 (95% CI 0.839-0.942); precision 0.844; recall 0.956; human-positive n=68 | validation sample | outputs/A4_theme_primary_n200/theme_scores.md |
| VAL-TH-F1-PATIENTSAFETY-200 | Patient safety: F1 (unweighted), N=200 | F1 0.882 (95% CI 0.834-0.921); precision 0.820; recall 0.955; human-positive n=110 | validation sample | outputs/A4_theme_primary_n200/theme_scores.md |
| VAL-TH-F1-ETHICSANDBIAS-200 | Ethics & bias: F1 (unweighted), N=200 | F1 0.908 (95% CI 0.855-0.954); precision 0.901; recall 0.914; human-positive n=70 | validation sample | outputs/A4_theme_primary_n200/theme_scores.md |
| VAL-TH-F1-GOVERNANCEREGULATION-200 | Governance / regulation: F1 (unweighted), N=200 | F1 0.916 (95% CI 0.872-0.956); precision 0.872; recall 0.965; human-positive n=85 | validation sample | outputs/A4_theme_primary_n200/theme_scores.md |
| VAL-TH-F1RANGE-200 | F1 range, four headline themes, N=200 | 0.882 (Patient safety) to 0.916 (Governance / regulation) | validation sample | outputs/A4_theme_primary_n200/theme_scores.md |
| VAL-TH-MICRO-187-UN | Micro-F1, N=187, unweighted | 0.919 (95% CI 0.897-0.940) | validation sample | outputs/A4_theme/theme_scores.md |
| VAL-TH-MACRO-187-UN | Macro-F1, N=187, unweighted | 0.840 (95% CI 0.760-0.899) | validation sample | outputs/A4_theme/theme_scores.md |
| VAL-TH-MICRO-187-WE | Micro-F1, N=187, weighted | 0.926 (95% CI 0.901-0.948) | validation sample | outputs/A4_theme/theme_scores.md |
| VAL-TH-MACRO-187-WE | Macro-F1, N=187, weighted | 0.829 (95% CI 0.742-0.895) | validation sample | outputs/A4_theme/theme_scores.md |
| VAL-TH-F1-HALLUCINATIONERRORS-187 | Hallucination / errors: F1 (unweighted), N=187 | F1 0.963 (95% CI 0.924-0.993); precision 0.970; recall 0.956; human-positive n=68 | validation sample | outputs/A4_theme/theme_scores.md |
| VAL-TH-F1-PATIENTSAFETY-187 | Patient safety: F1 (unweighted), N=187 | F1 0.933 (95% CI 0.899-0.962); precision 0.913; recall 0.955; human-positive n=110 | validation sample | outputs/A4_theme/theme_scores.md |
| VAL-TH-F1-ETHICSANDBIAS-187 | Ethics & bias: F1 (unweighted), N=187 | F1 0.914 (95% CI 0.860-0.960); precision 0.914; recall 0.914; human-positive n=70 | validation sample | outputs/A4_theme/theme_scores.md |
| VAL-TH-F1-GOVERNANCEREGULATION-187 | Governance / regulation: F1 (unweighted), N=187 | F1 0.953 (95% CI 0.917-0.982); precision 0.943; recall 0.965; human-positive n=85 | validation sample | outputs/A4_theme/theme_scores.md |
| VAL-TH-F1RANGE-187 | F1 range, four headline themes, N=187 | 0.914 (Ethics & bias) to 0.963 (Hallucination / errors) | validation sample | outputs/A4_theme/theme_scores.md |

### Mechanism (T3)

| ID | Item | Value | Window | Source |
|---|---|---|---|---|
| VAL-MX-DESIGN | Design | 120 critical records stratified by year and model-assigned failure mode; 12 title-only records excluded (n=108); one coder blinded to model labels | validation sample | outputs/T3_mechanism_confusion.md |
| VAL-MX-MT-K | Model type: Cohen κ | 0.84 (95% CI 0.74-0.93) | validation sample | final/data/validation_ci.csv |
| VAL-MX-MT-AC1 | Model type: Gwet AC1 | 0.88 (95% CI 0.81-0.94) | validation sample | final/data/validation_ci.csv |
| VAL-MX-MT-RAW | Model type: raw agreement | 90.7% (98/108; 95% CI 83.6%-95.5%) | validation sample | final/data/validation_ci.csv |
| VAL-MX-MT-KMAX | Model type: κ_max | 0.984 | validation sample | final/data/validation_ci.csv |
| VAL-MX-FM-K | Failure mode: Cohen κ | 0.57 (95% CI 0.46-0.69) | validation sample | final/data/validation_ci.csv |
| VAL-MX-FM-AC1 | Failure mode: Gwet AC1 | 0.60 (95% CI 0.49-0.71) | validation sample | final/data/validation_ci.csv |
| VAL-MX-FM-RAW | Failure mode: raw agreement | 69.4% (75/108; 95% CI 59.8%-77.9%) | validation sample | final/data/validation_ci.csv |
| VAL-MX-FM-KMAX | Failure mode: κ_max | 0.755 | validation sample | final/data/validation_ci.csv |
| VAL-MX-FABDIR | Fabrication disagreements: model fabrication-involved, human not vs human fabrication-involved, model not | 20 vs 1 (model fabrication-involved 42/108; human 23/108) | validation sample | outputs/T3_fabrication_direction.csv |

### Specialty

| ID | Item | Value | Window | Source |
|---|---|---|---|---|
| VAL-SP-DESIGN | Design | 120 records stratified by model-assigned specialty, with an 'unclear from abstract' option for the coder; one coder blinded to model labels | validation sample | output/analyses/specialty_kappa_report.md |
| VAL-SP-K | Cohen κ (unweighted, 'Unclear' as its own category) | 0.75 (95% CI 0.66-0.83) | validation sample | final/data/validation_ci.csv |
| VAL-SP-AC1 | Gwet AC1 | 0.75 (95% CI 0.67-0.83) | validation sample | final/data/validation_ci.csv |
| VAL-SP-RAW | Raw agreement | 76.7% (92/120; 95% CI 68.1%-83.9%) | validation sample | final/data/validation_ci.csv |
| VAL-SP-KMAX | κ_max | 0.850 | validation sample | final/data/validation_ci.csv |

### Symmetric endorsement flag vs human Advocacy (B3)

| ID | Item | Value | Window | Source |
|---|---|---|---|---|
| VAL-B3-ALL-SENSITIVITY | all model-favourable (n=130): sensitivity | 41.7% (10/24; 95% CI 21.1%-63.3%) | validation sample | outputs/B3/B3_agreement.csv |
| VAL-B3-ALL-PPV | all model-favourable (n=130): PPV | 55.6% (10/18; 95% CI 31.6%-80.0%) | validation sample | outputs/B3/B3_agreement.csv |
| VAL-B3-ALL-COHEN | all model-favourable (n=130): Cohen κ | 0.38 (95% CI 0.15-0.60) | validation sample | outputs/B3/B3_agreement.csv |
| VAL-B3-INSCOPE-SENSITIVITY | in-scope (T2 layer A) (n=112): sensitivity | 41.7% (10/24; 95% CI 23.8%-63.3%) | validation sample | outputs/B3/B3_agreement.csv |
| VAL-B3-INSCOPE-PPV | in-scope (T2 layer A) (n=112): PPV | 55.6% (10/18; 95% CI 33.3%-78.9%) | validation sample | outputs/B3/B3_agreement.csv |
| VAL-B3-INSCOPE-COHEN | in-scope (T2 layer A) (n=112): Cohen κ | 0.36 (95% CI 0.14-0.57) | validation sample | outputs/B3/B3_agreement.csv |

## Results, 2021-2025


### 1. Overall stance distribution

| ID | Item | Value | Window | Source |
|---|---|---|---|---|
| RES-OVR-ALARM | Alarm | 5.3% (749/14,058; 95% CI 5.0%-5.7%) | 2021-2025 | outputs/T5_crosssectional_both_windows.csv |
| RES-OVR-CAUTION | Caution | 25.1% (3534/14,058; 95% CI 24.4%-25.9%) | 2021-2025 | outputs/T5_crosssectional_both_windows.csv |
| RES-OVR-NEUTRAL | Neutral | 5.1% (721/14,058; 95% CI 4.8%-5.5%) | 2021-2025 | outputs/T5_crosssectional_both_windows.csv |
| RES-OVR-CAUTIOUSOPTIMISM | Cautious Optimism | 62.9% (8836/14,058; 95% CI 62.0%-63.7%) | 2021-2025 | outputs/T5_crosssectional_both_windows.csv |
| RES-OVR-ADVOCACY | Advocacy | 1.6% (218/14,058; 95% CI 1.4%-1.8%) | 2021-2025 | outputs/T5_crosssectional_both_windows.csv |
| RES-OVR-CRITICAL | Critical | 30.5% (4283/14,058; 95% CI 29.7%-31.2%) | 2021-2025 | outputs/T5_crosssectional_both_windows.csv |
| RES-OVR-FAVOURABLE | Favourable | 64.4% (9054/14,058; 95% CI 63.6%-65.2%) | 2021-2025 | outputs/T5_crosssectional_both_windows.csv |

### 2. Temporal trends

| ID | Item | Value | Window | Source |
|---|---|---|---|---|
| RES-TMP-ALARM-2021 | Alarm, 2021 | 2.7% (29/1063; 95% CI 1.8%-3.8%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-ALARM-2022 | Alarm, 2022 | 2.6% (35/1343; 95% CI 1.8%-3.5%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-ALARM-2023 | Alarm, 2023 | 4.7% (97/2054; 95% CI 3.8%-5.6%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-ALARM-2024 | Alarm, 2024 | 6.8% (253/3700; 95% CI 6.1%-7.8%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-ALARM-2025 | Alarm, 2025 | 5.7% (335/5898; 95% CI 5.1%-6.2%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-ALARM-RHO | Alarm: Spearman ρ across 5 annual values (exact permutation P) | ρ=+0.80 (P=.133) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-ALARM-OR | Alarm: unadjusted record-level logistic OR per year | OR 1.202 per year (95% CI 1.126-1.282), P<.001 | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-ALARM-DELTA | Alarm: change 2021 to 2025, percentage points | +3.0 percentage points (2.7% to 5.7%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-CAUT-2021 | Caution, 2021 | 22.7% (241/1063; 95% CI 20.3%-25.2%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-CAUT-2022 | Caution, 2022 | 22.2% (298/1343; 95% CI 20.0%-24.4%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-CAUT-2023 | Caution, 2023 | 25.7% (527/2054; 95% CI 23.7%-27.7%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-CAUT-2024 | Caution, 2024 | 26.4% (975/3700; 95% CI 25.0%-27.8%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-CAUT-2025 | Caution, 2025 | 25.3% (1493/5898; 95% CI 24.2%-26.5%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-CAUT-RHO | Caution: Spearman ρ across 5 annual values (exact permutation P) | ρ=+0.60 (P=.350) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-CAUT-OR | Caution: unadjusted record-level logistic OR per year | OR 1.038 per year (95% CI 1.007-1.070), P=.016 | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-CAUT-DELTA | Caution: change 2021 to 2025, percentage points | +2.6 percentage points (22.7% to 25.3%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-NEUT-2021 | Neutral, 2021 | 7.3% (78/1063; 95% CI 5.7%-9.0%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-NEUT-2022 | Neutral, 2022 | 7.9% (106/1343; 95% CI 6.4%-9.4%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-NEUT-2023 | Neutral, 2023 | 6.3% (130/2054; 95% CI 5.2%-7.4%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-NEUT-2024 | Neutral, 2024 | 5.1% (189/3700; 95% CI 4.4%-5.8%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-NEUT-2025 | Neutral, 2025 | 3.7% (218/5898; 95% CI 3.3%-4.2%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-NEUT-RHO | Neutral: Spearman ρ across 5 annual values (exact permutation P) | ρ=-0.90 (P=.083) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-NEUT-OR | Neutral: unadjusted record-level logistic OR per year | OR 0.810 per year (95% CI 0.768-0.856), P<.001 | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-NEUT-DELTA | Neutral: change 2021 to 2025, percentage points | -3.6 percentage points (7.3% to 3.7%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-CO-2021 | Cautious Optimism, 2021 | 64.3% (684/1063; 95% CI 61.4%-67.0%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-CO-2022 | Cautious Optimism, 2022 | 65.3% (877/1343; 95% CI 62.8%-67.8%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-CO-2023 | Cautious Optimism, 2023 | 61.3% (1260/2054; 95% CI 59.2%-63.4%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-CO-2024 | Cautious Optimism, 2024 | 60.2% (2229/3700; 95% CI 58.5%-61.8%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-CO-2025 | Cautious Optimism, 2025 | 64.2% (3786/5898; 95% CI 62.9%-65.4%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-CO-RHO | Cautious Optimism: Spearman ρ across 5 annual values (exact permutation P) | ρ=-0.60 (P=.350) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-CO-OR | Cautious Optimism: unadjusted record-level logistic OR per year | OR 0.999 per year (95% CI 0.973-1.027), P=.962 | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-CO-DELTA | Cautious Optimism: change 2021 to 2025, percentage points | -0.2 percentage points (64.3% to 64.2%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-ADV-2021 | Advocacy, 2021 | 2.9% (31/1063; 95% CI 1.9%-4.0%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-ADV-2022 | Advocacy, 2022 | 2.0% (27/1343; 95% CI 1.3%-2.8%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-ADV-2023 | Advocacy, 2023 | 1.9% (40/2054; 95% CI 1.4%-2.6%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-ADV-2024 | Advocacy, 2024 | 1.5% (54/3700; 95% CI 1.1%-1.8%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-ADV-2025 | Advocacy, 2025 | 1.1% (66/5898; 95% CI 0.9%-1.4%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-ADV-RHO | Advocacy: Spearman ρ across 5 annual values (exact permutation P) | ρ=-1.00 (P=.017) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-ADV-OR | Advocacy: unadjusted record-level logistic OR per year | OR 0.793 per year (95% CI 0.721-0.872), P<.001 | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-ADV-DELTA | Advocacy: change 2021 to 2025, percentage points | -1.8 percentage points (2.9% to 1.1%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-CRIT-2021 | Critical (Alarm+Caution), 2021 | 25.4% (270/1063; 95% CI 22.8%-28.0%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-CRIT-2022 | Critical (Alarm+Caution), 2022 | 24.8% (333/1343; 95% CI 22.6%-27.1%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-CRIT-2023 | Critical (Alarm+Caution), 2023 | 30.4% (624/2054; 95% CI 28.3%-32.5%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-CRIT-2024 | Critical (Alarm+Caution), 2024 | 33.2% (1228/3700; 95% CI 31.8%-34.8%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-CRIT-2025 | Critical (Alarm+Caution), 2025 | 31.0% (1828/5898; 95% CI 29.8%-32.3%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-CRIT-RHO | Critical (Alarm+Caution): Spearman ρ across 5 annual values (exact permutation P) | ρ=+0.80 (P=.133) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-CRIT-OR | Critical (Alarm+Caution): unadjusted record-level logistic OR per year | OR 1.077 per year (95% CI 1.046-1.108), P<.001 | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-CRIT-DELTA | Critical (Alarm+Caution): change 2021 to 2025, percentage points | +5.6 percentage points (25.4% to 31.0%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-FAV-2021 | Favourable (CO+Advocacy), 2021 | 67.3% (715/1063; 95% CI 64.6%-69.9%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-FAV-2022 | Favourable (CO+Advocacy), 2022 | 67.3% (904/1343; 95% CI 64.9%-69.9%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-FAV-2023 | Favourable (CO+Advocacy), 2023 | 63.3% (1300/2054; 95% CI 61.2%-65.4%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-FAV-2024 | Favourable (CO+Advocacy), 2024 | 61.7% (2283/3700; 95% CI 60.0%-63.2%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-FAV-2025 | Favourable (CO+Advocacy), 2025 | 65.3% (3852/5898; 95% CI 64.0%-66.5%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-FAV-RHO | Favourable (CO+Advocacy): Spearman ρ across 5 annual values (exact permutation P) | ρ=-0.60 (P=.350) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-FAV-OR | Favourable (CO+Advocacy): unadjusted record-level logistic OR per year | OR 0.982 per year (95% CI 0.956-1.009), P=.197 | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-FAV-DELTA | Favourable (CO+Advocacy): change 2021 to 2025, percentage points | -2.0 percentage points (67.3% to 65.3%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-CRIT-AOR | Critical: adjusted OR per year (B4 primary; genre, publication type, specialty, region; journal-clustered SEs) | OR 1.103 per year (95% CI 1.066-1.141), P<.001 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv |
| RES-TMP-CRIT-CAT-2022 | Critical: adjusted OR, 2022 vs 2021 (B4 S1, categorical year) | OR 1.00 (95% CI 0.83-1.21), P=.993 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-TMP-CRIT-CAT-2023 | Critical: adjusted OR, 2023 vs 2021 (B4 S1, categorical year) | OR 1.31 (95% CI 1.09-1.56), P=.003 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-TMP-CRIT-CAT-2024 | Critical: adjusted OR, 2024 vs 2021 (B4 S1, categorical year) | OR 1.53 (95% CI 1.30-1.80), P<.001 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-TMP-CRIT-CAT-2025 | Critical: adjusted OR, 2025 vs 2021 (B4 S1, categorical year) | OR 1.45 (95% CI 1.23-1.70), P<.001 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-TMP-ADV-AOR | Advocacy: adjusted OR per year (B4 secondary 2) | OR 0.841 per year (95% CI 0.754-0.939), P=.002 | 2021-2025 | outputs/B4/B4_advocacy_ORs.csv |
| RES-TMP-ADV-CAT | Advocacy: categorical-year adjusted ORs | Not produced: B4 fitted the categorical-year model (S1) for the critical outcome only; the Advocacy model used continuous year. Fitting it would be a new analysis. | 2021-2025 | outputs/B4/B4_regression.md |
| RES-TMP-CRIT-AMP-2021 | Critical: adjusted average marginal probability, 2021 | 25.3% (95% CI 23.3%-27.5%) | 2021-2025 | outputs/B4/B4_primary_critical_AMP.csv |
| RES-TMP-CRIT-AMP-2022 | Critical: adjusted average marginal probability, 2022 | 27.1% (95% CI 25.4%-28.8%) | 2021-2025 | outputs/B4/B4_primary_critical_AMP.csv |
| RES-TMP-CRIT-AMP-2023 | Critical: adjusted average marginal probability, 2023 | 28.8% (95% CI 27.5%-30.2%) | 2021-2025 | outputs/B4/B4_primary_critical_AMP.csv |
| RES-TMP-CRIT-AMP-2024 | Critical: adjusted average marginal probability, 2024 | 30.7% (95% CI 29.5%-31.8%) | 2021-2025 | outputs/B4/B4_primary_critical_AMP.csv |
| RES-TMP-CRIT-AMP-2025 | Critical: adjusted average marginal probability, 2025 | 32.6% (95% CI 31.3%-33.9%) | 2021-2025 | outputs/B4/B4_primary_critical_AMP.csv |
| RES-TMP-SE-2021 | Strong endorsement (flag yes), 2021 | 10.8% (115/1063; 95% CI 9.1%-12.7%) | 2021-2025 | outputs/B3/B3_trend.csv |
| RES-TMP-SE-2022 | Strong endorsement (flag yes), 2022 | 13.2% (177/1343; 95% CI 11.3%-14.9%) | 2021-2025 | outputs/B3/B3_trend.csv |
| RES-TMP-SE-2023 | Strong endorsement (flag yes), 2023 | 9.8% (202/2054; 95% CI 8.6%-11.0%) | 2021-2025 | outputs/B3/B3_trend.csv |
| RES-TMP-SE-2024 | Strong endorsement (flag yes), 2024 | 8.0% (295/3700; 95% CI 7.1%-8.8%) | 2021-2025 | outputs/B3/B3_trend.csv |
| RES-TMP-SE-2025 | Strong endorsement (flag yes), 2025 | 6.6% (390/5898; 95% CI 6.0%-7.3%) | 2021-2025 | outputs/B3/B3_trend.csv |
| RES-TMP-SE-RHO | Strong endorsement (flag yes): Spearman ρ (exact P) | ρ=-0.90 (P=.083) | 2021-2025 | outputs/B3/B3_trend.csv |
| RES-TMP-SE-OR | Strong endorsement (flag yes): unadjusted OR per year | OR 0.834 per year (95% CI 0.798-0.871), P<.001 | 2021-2025 | outputs/B3/B3_trend.csv |
| RES-TMP-SEUB-2021 | Strong endorsement, upper bound (FAILED as yes), 2021 | 10.9% (116/1063; 95% CI 9.2%-12.8%) | 2021-2025 | outputs/B3/B3_trend.csv |
| RES-TMP-SEUB-2022 | Strong endorsement, upper bound (FAILED as yes), 2022 | 13.2% (177/1343; 95% CI 11.3%-14.9%) | 2021-2025 | outputs/B3/B3_trend.csv |
| RES-TMP-SEUB-2023 | Strong endorsement, upper bound (FAILED as yes), 2023 | 9.8% (202/2054; 95% CI 8.6%-11.0%) | 2021-2025 | outputs/B3/B3_trend.csv |
| RES-TMP-SEUB-2024 | Strong endorsement, upper bound (FAILED as yes), 2024 | 8.0% (296/3700; 95% CI 7.1%-8.8%) | 2021-2025 | outputs/B3/B3_trend.csv |
| RES-TMP-SEUB-2025 | Strong endorsement, upper bound (FAILED as yes), 2025 | 6.7% (392/5898; 95% CI 6.0%-7.3%) | 2021-2025 | outputs/B3/B3_trend.csv |
| RES-TMP-SEUB-RHO | Strong endorsement, upper bound (FAILED as yes): Spearman ρ (exact P) | ρ=-0.90 (P=.083) | 2021-2025 | outputs/B3/B3_trend.csv |
| RES-TMP-SEUB-OR | Strong endorsement, upper bound (FAILED as yes): unadjusted OR per year | OR 0.834 per year (95% CI 0.798-0.871), P<.001 | 2021-2025 | outputs/B3/B3_trend.csv |
| RES-TMP-GENDISC-2021 | Critical share within discourse records, 2021 | 30.2% (222/735; 95% CI 26.8%-33.6%) | 2021-2025 | outputs/B7_tableS3_2021_2025.csv; outputs/T4_trend_tests.csv |
| RES-TMP-GENDISC-2022 | Critical share within discourse records, 2022 | 31.2% (269/863; 95% CI 28.0%-34.4%) | 2021-2025 | outputs/B7_tableS3_2021_2025.csv; outputs/T4_trend_tests.csv |
| RES-TMP-GENDISC-2023 | Critical share within discourse records, 2023 | 35.3% (447/1267; 95% CI 32.7%-38.0%) | 2021-2025 | outputs/B7_tableS3_2021_2025.csv; outputs/T4_trend_tests.csv |
| RES-TMP-GENDISC-2024 | Critical share within discourse records, 2024 | 37.5% (713/1901; 95% CI 35.2%-39.6%) | 2021-2025 | outputs/B7_tableS3_2021_2025.csv; outputs/T4_trend_tests.csv |
| RES-TMP-GENDISC-2025 | Critical share within discourse records, 2025 | 35.4% (1016/2867; 95% CI 33.7%-37.3%) | 2021-2025 | outputs/B7_tableS3_2021_2025.csv; outputs/T4_trend_tests.csv |
| RES-TMP-GENDISC-RHO | Critical share within discourse records: Spearman ρ across 5 annual values (exact permutation P) | ρ=+0.90 (P=.083) | 2021-2025 | outputs/B7_tableS3_2021_2025.csv; outputs/T4_trend_tests.csv |
| RES-TMP-GENDISC-OR | Critical share within discourse records: unadjusted record-level logistic OR per year | OR 1.061 per year (95% CI 1.024-1.099), P=.001 | 2021-2025 | outputs/B7_tableS3_2021_2025.csv; outputs/T4_trend_tests.csv |
| RES-TMP-GENDISC-DELTA | Critical share within discourse records: change 2021 to 2025, percentage points | +5.2 percentage points (30.2% to 35.4%) | 2021-2025 | outputs/B7_tableS3_2021_2025.csv; outputs/T4_trend_tests.csv |
| RES-TMP-GENEVAL-2021 | Critical share within evaluative records, 2021 | 14.6% (48/328; 95% CI 10.7%-18.6%) | 2021-2025 | outputs/B7_tableS3_2021_2025.csv; outputs/T4_trend_tests.csv |
| RES-TMP-GENEVAL-2022 | Critical share within evaluative records, 2022 | 13.3% (64/480; 95% CI 10.6%-16.5%) | 2021-2025 | outputs/B7_tableS3_2021_2025.csv; outputs/T4_trend_tests.csv |
| RES-TMP-GENEVAL-2023 | Critical share within evaluative records, 2023 | 22.5% (177/787; 95% CI 19.6%-25.5%) | 2021-2025 | outputs/B7_tableS3_2021_2025.csv; outputs/T4_trend_tests.csv |
| RES-TMP-GENEVAL-2024 | Critical share within evaluative records, 2024 | 28.6% (515/1799; 95% CI 26.5%-30.7%) | 2021-2025 | outputs/B7_tableS3_2021_2025.csv; outputs/T4_trend_tests.csv |
| RES-TMP-GENEVAL-2025 | Critical share within evaluative records, 2025 | 26.8% (812/3031; 95% CI 25.2%-28.4%) | 2021-2025 | outputs/B7_tableS3_2021_2025.csv; outputs/T4_trend_tests.csv |
| RES-TMP-GENEVAL-RHO | Critical share within evaluative records: Spearman ρ across 5 annual values (exact permutation P) | ρ=+0.80 (P=.133) | 2021-2025 | outputs/B7_tableS3_2021_2025.csv; outputs/T4_trend_tests.csv |
| RES-TMP-GENEVAL-OR | Critical share within evaluative records: unadjusted record-level logistic OR per year | OR 1.209 per year (95% CI 1.147-1.274), P<.001 | 2021-2025 | outputs/B7_tableS3_2021_2025.csv; outputs/T4_trend_tests.csv |
| RES-TMP-GENEVAL-DELTA | Critical share within evaluative records: change 2021 to 2025, percentage points | +12.2 percentage points (14.6% to 26.8%) | 2021-2025 | outputs/B7_tableS3_2021_2025.csv; outputs/T4_trend_tests.csv |
| RES-TMP-GENRATIO-2021 | Discourse:evaluative ratio, 2021 | 2.24 (735/328) | 2021-2025 | outputs/T4_genre_ratio.csv |
| RES-TMP-GENRATIO-2022 | Discourse:evaluative ratio, 2022 | 1.80 (863/480) | 2021-2025 | outputs/T4_genre_ratio.csv |
| RES-TMP-GENRATIO-2023 | Discourse:evaluative ratio, 2023 | 1.61 (1267/787) | 2021-2025 | outputs/T4_genre_ratio.csv |
| RES-TMP-GENRATIO-2024 | Discourse:evaluative ratio, 2024 | 1.06 (1901/1799) | 2021-2025 | outputs/T4_genre_ratio.csv |
| RES-TMP-GENRATIO-2025 | Discourse:evaluative ratio, 2025 | 0.95 (2867/3031) | 2021-2025 | outputs/T4_genre_ratio.csv |
| RES-TMP-TH-PATIENTSAFETY-2021 | Theme among critical records: Patient safety, 2021 | 59.3% (160/270; 95% CI 53.5%-64.8%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-TH-PATIENTSAFETY-2022 | Theme among critical records: Patient safety, 2022 | 63.1% (210/333; 95% CI 57.8%-67.9%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-TH-PATIENTSAFETY-2023 | Theme among critical records: Patient safety, 2023 | 61.7% (385/624; 95% CI 58.1%-65.6%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-TH-PATIENTSAFETY-2024 | Theme among critical records: Patient safety, 2024 | 66.2% (813/1228; 95% CI 63.5%-68.7%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-TH-PATIENTSAFETY-2025 | Theme among critical records: Patient safety, 2025 | 64.9% (1187/1828; 95% CI 62.7%-67.2%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-TH-PATIENTSAFETY-RHO | Theme among critical records: Patient safety: Spearman ρ across 5 annual values (exact permutation P) | ρ=+0.80 (P=.133) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-TH-PATIENTSAFETY-OR | Theme among critical records: Patient safety: unadjusted record-level logistic OR per year | OR 1.055 per year (95% CI 1.002-1.111), P=.041 | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-TH-PATIENTSAFETY-DELTA | Theme among critical records: Patient safety: change 2021 to 2025, percentage points | +5.7 percentage points (59.3% to 64.9%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-TH-HALLUCINATIONERRORS-2021 | Theme among critical records: Hallucination / errors, 2021 | 23.7% (64/270; 95% CI 18.6%-28.5%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-TH-HALLUCINATIONERRORS-2022 | Theme among critical records: Hallucination / errors, 2022 | 21.9% (73/333; 95% CI 17.8%-26.7%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-TH-HALLUCINATIONERRORS-2023 | Theme among critical records: Hallucination / errors, 2023 | 42.1% (263/624; 95% CI 38.5%-46.1%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-TH-HALLUCINATIONERRORS-2024 | Theme among critical records: Hallucination / errors, 2024 | 51.9% (637/1228; 95% CI 49.2%-54.7%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-TH-HALLUCINATIONERRORS-2025 | Theme among critical records: Hallucination / errors, 2025 | 51.1% (934/1828; 95% CI 48.7%-53.3%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-TH-HALLUCINATIONERRORS-RHO | Theme among critical records: Hallucination / errors: Spearman ρ across 5 annual values (exact permutation P) | ρ=+0.80 (P=.133) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-TH-HALLUCINATIONERRORS-OR | Theme among critical records: Hallucination / errors: unadjusted record-level logistic OR per year | OR 1.367 per year (95% CI 1.296-1.442), P<.001 | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-TH-HALLUCINATIONERRORS-DELTA | Theme among critical records: Hallucination / errors: change 2021 to 2025, percentage points | +27.4 percentage points (23.7% to 51.1%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-TH-GOVERNANCEREGULATION-2021 | Theme among critical records: Governance / regulation, 2021 | 54.8% (148/270; 95% CI 49.1%-60.7%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-TH-GOVERNANCEREGULATION-2022 | Theme among critical records: Governance / regulation, 2022 | 55.9% (186/333; 95% CI 50.4%-60.9%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-TH-GOVERNANCEREGULATION-2023 | Theme among critical records: Governance / regulation, 2023 | 41.5% (259/624; 95% CI 37.6%-45.4%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-TH-GOVERNANCEREGULATION-2024 | Theme among critical records: Governance / regulation, 2024 | 34.2% (420/1228; 95% CI 31.5%-36.9%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-TH-GOVERNANCEREGULATION-2025 | Theme among critical records: Governance / regulation, 2025 | 31.7% (580/1828; 95% CI 29.6%-34.0%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-TH-GOVERNANCEREGULATION-RHO | Theme among critical records: Governance / regulation: Spearman ρ across 5 annual values (exact permutation P) | ρ=-0.90 (P=.083) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-TH-GOVERNANCEREGULATION-OR | Theme among critical records: Governance / regulation: unadjusted record-level logistic OR per year | OR 0.765 per year (95% CI 0.727-0.805), P<.001 | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-TH-GOVERNANCEREGULATION-DELTA | Theme among critical records: Governance / regulation: change 2021 to 2025, percentage points | -23.1 percentage points (54.8% to 31.7%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-TH-ETHICSANDBIAS-2021 | Theme among critical records: Ethics & bias, 2021 | 36.7% (99/270; 95% CI 30.9%-42.8%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-TH-ETHICSANDBIAS-2022 | Theme among critical records: Ethics & bias, 2022 | 45.3% (151/333; 95% CI 39.5%-50.7%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-TH-ETHICSANDBIAS-2023 | Theme among critical records: Ethics & bias, 2023 | 36.2% (226/624; 95% CI 32.4%-40.0%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-TH-ETHICSANDBIAS-2024 | Theme among critical records: Ethics & bias, 2024 | 32.8% (403/1228; 95% CI 30.3%-35.5%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-TH-ETHICSANDBIAS-2025 | Theme among critical records: Ethics & bias, 2025 | 33.0% (604/1828; 95% CI 30.8%-35.2%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-TH-ETHICSANDBIAS-RHO | Theme among critical records: Ethics & bias: Spearman ρ across 5 annual values (exact permutation P) | ρ=-0.80 (P=.133) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-TH-ETHICSANDBIAS-OR | Theme among critical records: Ethics & bias: unadjusted record-level logistic OR per year | OR 0.915 per year (95% CI 0.869-0.963), P<.001 | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-TH-ETHICSANDBIAS-DELTA | Theme among critical records: Ethics & bias: change 2021 to 2025, percentage points | -3.6 percentage points (36.7% to 33.0%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-TH-MEDICALEDUCATION-2021 | Theme among critical records: Medical education, 2021 | 3.7% (10/270; 95% CI 1.8%-6.1%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-TH-MEDICALEDUCATION-2022 | Theme among critical records: Medical education, 2022 | 1.8% (6/333; 95% CI 0.6%-3.4%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-TH-MEDICALEDUCATION-2023 | Theme among critical records: Medical education, 2023 | 9.3% (58/624; 95% CI 7.1%-11.7%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-TH-MEDICALEDUCATION-2024 | Theme among critical records: Medical education, 2024 | 8.4% (103/1228; 95% CI 6.7%-10.0%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-TH-MEDICALEDUCATION-2025 | Theme among critical records: Medical education, 2025 | 10.4% (190/1828; 95% CI 9.0%-11.8%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-TH-MEDICALEDUCATION-RHO | Theme among critical records: Medical education: Spearman ρ across 5 annual values (exact permutation P) | ρ=+0.80 (P=.133) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-TH-MEDICALEDUCATION-OR | Theme among critical records: Medical education: unadjusted record-level logistic OR per year | OR 1.312 per year (95% CI 1.181-1.456), P<.001 | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-TH-MEDICALEDUCATION-DELTA | Theme among critical records: Medical education: change 2021 to 2025, percentage points | +6.7 percentage points (3.7% to 10.4%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-TH-DATAPRIVACY-2021 | Theme among critical records: Data privacy, 2021 | 8.9% (24/270; 95% CI 5.8%-12.8%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-TH-DATAPRIVACY-2022 | Theme among critical records: Data privacy, 2022 | 8.4% (28/333; 95% CI 5.6%-11.5%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-TH-DATAPRIVACY-2023 | Theme among critical records: Data privacy, 2023 | 6.6% (41/624; 95% CI 4.8%-8.6%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-TH-DATAPRIVACY-2024 | Theme among critical records: Data privacy, 2024 | 6.8% (84/1228; 95% CI 5.4%-8.2%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-TH-DATAPRIVACY-2025 | Theme among critical records: Data privacy, 2025 | 8.1% (148/1828; 95% CI 6.9%-9.4%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-TH-DATAPRIVACY-RHO | Theme among critical records: Data privacy: Spearman ρ across 5 annual values (exact permutation P) | ρ=-0.60 (P=.350) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-TH-DATAPRIVACY-OR | Theme among critical records: Data privacy: unadjusted record-level logistic OR per year | OR 0.999 per year (95% CI 0.910-1.098), P=.986 | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-TH-DATAPRIVACY-DELTA | Theme among critical records: Data privacy: change 2021 to 2025, percentage points | -0.8 percentage points (8.9% to 8.1%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-TH-COGNITIVEOFFLOADING-2021 | Theme among critical records: Cognitive offloading, 2021 | 7.8% (21/270; 95% CI 4.9%-11.0%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-TH-COGNITIVEOFFLOADING-2022 | Theme among critical records: Cognitive offloading, 2022 | 5.7% (19/333; 95% CI 3.1%-8.3%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-TH-COGNITIVEOFFLOADING-2023 | Theme among critical records: Cognitive offloading, 2023 | 5.6% (35/624; 95% CI 4.0%-7.5%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-TH-COGNITIVEOFFLOADING-2024 | Theme among critical records: Cognitive offloading, 2024 | 4.8% (59/1228; 95% CI 3.7%-6.0%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-TH-COGNITIVEOFFLOADING-2025 | Theme among critical records: Cognitive offloading, 2025 | 6.6% (120/1828; 95% CI 5.5%-7.8%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-TH-COGNITIVEOFFLOADING-RHO | Theme among critical records: Cognitive offloading: Spearman ρ across 5 annual values (exact permutation P) | ρ=-0.40 (P=.517) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-TH-COGNITIVEOFFLOADING-OR | Theme among critical records: Cognitive offloading: unadjusted record-level logistic OR per year | OR 1.000 per year (95% CI 0.900-1.112), P=.994 | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-TH-COGNITIVEOFFLOADING-DELTA | Theme among critical records: Cognitive offloading: change 2021 to 2025, percentage points | -1.2 percentage points (7.8% to 6.6%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-TH-EXISTENTIALTHREAT-2021 | Theme among critical records: Existential threat, 2021 | 6.7% (18/270; 95% CI 3.7%-9.7%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-TH-EXISTENTIALTHREAT-2022 | Theme among critical records: Existential threat, 2022 | 4.2% (14/333; 95% CI 2.2%-6.4%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-TH-EXISTENTIALTHREAT-2023 | Theme among critical records: Existential threat, 2023 | 5.9% (37/624; 95% CI 4.2%-7.8%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-TH-EXISTENTIALTHREAT-2024 | Theme among critical records: Existential threat, 2024 | 3.2% (39/1228; 95% CI 2.2%-4.2%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-TH-EXISTENTIALTHREAT-2025 | Theme among critical records: Existential threat, 2025 | 5.6% (102/1828; 95% CI 4.6%-6.7%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-TH-EXISTENTIALTHREAT-RHO | Theme among critical records: Existential threat: Spearman ρ across 5 annual values (exact permutation P) | ρ=-0.50 (P=.450) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-TH-EXISTENTIALTHREAT-OR | Theme among critical records: Existential threat: unadjusted record-level logistic OR per year | OR 0.987 per year (95% CI 0.881-1.107), P=.829 | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-TH-EXISTENTIALTHREAT-DELTA | Theme among critical records: Existential threat: change 2021 to 2025, percentage points | -1.1 percentage points (6.7% to 5.6%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-TH-REPLACEMENTFEARS-2021 | Theme among critical records: Replacement fears, 2021 | 6.3% (17/270; 95% CI 3.7%-9.3%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-TH-REPLACEMENTFEARS-2022 | Theme among critical records: Replacement fears, 2022 | 5.1% (17/333; 95% CI 2.8%-7.6%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-TH-REPLACEMENTFEARS-2023 | Theme among critical records: Replacement fears, 2023 | 4.3% (27/624; 95% CI 2.8%-6.0%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-TH-REPLACEMENTFEARS-2024 | Theme among critical records: Replacement fears, 2024 | 4.1% (50/1228; 95% CI 3.0%-5.2%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-TH-REPLACEMENTFEARS-2025 | Theme among critical records: Replacement fears, 2025 | 3.3% (60/1828; 95% CI 2.5%-4.2%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-TH-REPLACEMENTFEARS-RHO | Theme among critical records: Replacement fears: Spearman ρ across 5 annual values (exact permutation P) | ρ=-1.00 (P=.017) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-TH-REPLACEMENTFEARS-OR | Theme among critical records: Replacement fears: unadjusted record-level logistic OR per year | OR 0.853 per year (95% CI 0.758-0.959), P=.008 | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-TH-REPLACEMENTFEARS-DELTA | Theme among critical records: Replacement fears: change 2021 to 2025, percentage points | -3.0 percentage points (6.3% to 3.3%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-TH-OTHER-2021 | Theme among critical records: Other, 2021 | 4.8% (13/270; 95% CI 2.3%-7.4%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-TH-OTHER-2022 | Theme among critical records: Other, 2022 | 4.5% (15/333; 95% CI 2.6%-6.9%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-TH-OTHER-2023 | Theme among critical records: Other, 2023 | 2.2% (14/624; 95% CI 1.2%-3.6%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-TH-OTHER-2024 | Theme among critical records: Other, 2024 | 1.7% (21/1228; 95% CI 1.0%-2.5%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-TH-OTHER-2025 | Theme among critical records: Other, 2025 | 1.7% (31/1828; 95% CI 1.1%-2.3%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-TH-OTHER-RHO | Theme among critical records: Other: Spearman ρ across 5 annual values (exact permutation P) | ρ=-1.00 (P=.017) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-TH-OTHER-OR | Theme among critical records: Other: unadjusted record-level logistic OR per year | OR 0.743 per year (95% CI 0.640-0.862), P<.001 | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-TH-OTHER-DELTA | Theme among critical records: Other: change 2021 to 2025, percentage points | -3.1 percentage points (4.8% to 1.7%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-FM-CONF-2021 | Mechanism, hallucination-gated (failure-mode composition): Confabulation (fabrication only), 2021 | 0.0% (0/56; 95% CI 0.0%-0.0% (bootstrap); exact Clopper-Pearson 0.0%-6.4%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-FM-CONF-2022 | Mechanism, hallucination-gated (failure-mode composition): Confabulation (fabrication only), 2022 | 1.6% (1/61; 95% CI 0.0%-6.0%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-FM-CONF-2023 | Mechanism, hallucination-gated (failure-mode composition): Confabulation (fabrication only), 2023 | 10.7% (23/215; 95% CI 6.6%-15.2%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-FM-CONF-2024 | Mechanism, hallucination-gated (failure-mode composition): Confabulation (fabrication only), 2024 | 11.8% (66/560; 95% CI 9.2%-14.6%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-FM-CONF-2025 | Mechanism, hallucination-gated (failure-mode composition): Confabulation (fabrication only), 2025 | 9.1% (80/883; 95% CI 7.2%-11.0%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-FM-CONF-RHO | Mechanism, hallucination-gated (failure-mode composition): Confabulation (fabrication only): Spearman ρ across 5 annual values (exact permutation P) | ρ=+0.70 (P=.233) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-FM-CONF-OR | Mechanism, hallucination-gated (failure-mode composition): Confabulation (fabrication only): unadjusted record-level logistic OR per year | OR 1.142 per year (95% CI 0.962-1.356), P=.129 | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-FM-CONF-DELTA | Mechanism, hallucination-gated (failure-mode composition): Confabulation (fabrication only): change 2021 to 2025, percentage points | +9.1 percentage points (0.0% to 9.1%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-FM-MIS-2021 | Mechanism, hallucination-gated (failure-mode composition): Misclassification (factual error), 2021 | 69.6% (39/56; 95% CI 58.3%-82.0%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-FM-MIS-2022 | Mechanism, hallucination-gated (failure-mode composition): Misclassification (factual error), 2022 | 90.2% (55/61; 95% CI 81.5%-96.8%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-FM-MIS-2023 | Mechanism, hallucination-gated (failure-mode composition): Misclassification (factual error), 2023 | 56.3% (121/215; 95% CI 49.2%-62.7%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-FM-MIS-2024 | Mechanism, hallucination-gated (failure-mode composition): Misclassification (factual error), 2024 | 61.4% (344/560; 95% CI 57.1%-65.3%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-FM-MIS-2025 | Mechanism, hallucination-gated (failure-mode composition): Misclassification (factual error), 2025 | 65.6% (579/883; 95% CI 62.5%-68.6%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-FM-MIS-RHO | Mechanism, hallucination-gated (failure-mode composition): Misclassification (factual error): Spearman ρ across 5 annual values (exact permutation P) | ρ=-0.50 (P=.450) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-FM-MIS-OR | Mechanism, hallucination-gated (failure-mode composition): Misclassification (factual error): unadjusted record-level logistic OR per year | OR 0.972 per year (95% CI 0.882-1.072), P=.574 | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-FM-MIS-DELTA | Mechanism, hallucination-gated (failure-mode composition): Misclassification (factual error): change 2021 to 2025, percentage points | -4.1 percentage points (69.6% to 65.6%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-FM-BOTH-2021 | Mechanism, hallucination-gated (failure-mode composition): Both, 2021 | 0.0% (0/56; 95% CI 0.0%-0.0% (bootstrap); exact Clopper-Pearson 0.0%-6.4%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-FM-BOTH-2022 | Mechanism, hallucination-gated (failure-mode composition): Both, 2022 | 0.0% (0/61; 95% CI 0.0%-0.0% (bootstrap); exact Clopper-Pearson 0.0%-5.9%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-FM-BOTH-2023 | Mechanism, hallucination-gated (failure-mode composition): Both, 2023 | 5.1% (11/215; 95% CI 2.4%-8.3%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-FM-BOTH-2024 | Mechanism, hallucination-gated (failure-mode composition): Both, 2024 | 11.6% (65/560; 95% CI 8.9%-14.4%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-FM-BOTH-2025 | Mechanism, hallucination-gated (failure-mode composition): Both, 2025 | 11.6% (102/883; 95% CI 9.5%-13.6%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-FM-BOTH-RHO | Mechanism, hallucination-gated (failure-mode composition): Both: Spearman ρ across 5 annual values (exact permutation P) | ρ=+0.87 (P=.100) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-FM-BOTH-OR | Mechanism, hallucination-gated (failure-mode composition): Both: unadjusted record-level logistic OR per year | OR 1.532 per year (95% CI 1.252-1.876), P<.001 | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-FM-BOTH-DELTA | Mechanism, hallucination-gated (failure-mode composition): Both: change 2021 to 2025, percentage points | +11.6 percentage points (0.0% to 11.6%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-FM-NONE-2021 | Mechanism, hallucination-gated (failure-mode composition): None or unclear, 2021 | 30.4% (17/56; 95% CI 18.0%-41.7%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-FM-NONE-2022 | Mechanism, hallucination-gated (failure-mode composition): None or unclear, 2022 | 8.2% (5/61; 95% CI 1.8%-16.0%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-FM-NONE-2023 | Mechanism, hallucination-gated (failure-mode composition): None or unclear, 2023 | 27.9% (60/215; 95% CI 22.1%-34.4%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-FM-NONE-2024 | Mechanism, hallucination-gated (failure-mode composition): None or unclear, 2024 | 15.2% (85/560; 95% CI 12.3%-18.1%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-FM-NONE-2025 | Mechanism, hallucination-gated (failure-mode composition): None or unclear, 2025 | 13.8% (122/883; 95% CI 11.6%-16.1%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-FM-NONE-RHO | Mechanism, hallucination-gated (failure-mode composition): None or unclear: Spearman ρ across 5 annual values (exact permutation P) | ρ=-0.40 (P=.517) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-FM-NONE-OR | Mechanism, hallucination-gated (failure-mode composition): None or unclear: unadjusted record-level logistic OR per year | OR 0.796 per year (95% CI 0.708-0.893), P<.001 | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-FM-NONE-DELTA | Mechanism, hallucination-gated (failure-mode composition): None or unclear: change 2021 to 2025, percentage points | -16.5 percentage points (30.4% to 13.8%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-FAB-GATED-2021 | Mechanism, hallucination-gated: Fabrication-involved (confabulation or both), 2021 | 0.0% (0/56; 95% CI 0.0%-0.0% (bootstrap); exact Clopper-Pearson 0.0%-6.4%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-FAB-GATED-2022 | Mechanism, hallucination-gated: Fabrication-involved (confabulation or both), 2022 | 1.6% (1/61; 95% CI 0.0%-6.0%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-FAB-GATED-2023 | Mechanism, hallucination-gated: Fabrication-involved (confabulation or both), 2023 | 15.8% (34/215; 95% CI 11.2%-20.9%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-FAB-GATED-2024 | Mechanism, hallucination-gated: Fabrication-involved (confabulation or both), 2024 | 23.4% (131/560; 95% CI 20.0%-27.0%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-FAB-GATED-2025 | Mechanism, hallucination-gated: Fabrication-involved (confabulation or both), 2025 | 20.6% (182/883; 95% CI 18.0%-23.4%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-FAB-GATED-RHO | Mechanism, hallucination-gated: Fabrication-involved (confabulation or both): Spearman ρ across 5 annual values (exact permutation P) | ρ=+0.90 (P=.083) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-FAB-GATED-OR | Mechanism, hallucination-gated: Fabrication-involved (confabulation or both): unadjusted record-level logistic OR per year | OR 1.347 per year (95% CI 1.174-1.544), P<.001 | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-FAB-GATED-DELTA | Mechanism, hallucination-gated: Fabrication-involved (confabulation or both): change 2021 to 2025, percentage points | +20.6 percentage points (0.0% to 20.6%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-GENSHARE-2021 | Mechanism, all abstract-present critical: Generative-model share (generative or both), 2021 | 5.3% (13/245; 95% CI 2.8%-8.2%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-GENSHARE-2022 | Mechanism, all abstract-present critical: Generative-model share (generative or both), 2022 | 2.5% (7/285; 95% CI 0.7%-4.2%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-GENSHARE-2023 | Mechanism, all abstract-present critical: Generative-model share (generative or both), 2023 | 33.0% (179/543; 95% CI 29.1%-37.0%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-GENSHARE-2024 | Mechanism, all abstract-present critical: Generative-model share (generative or both), 2024 | 56.9% (612/1076; 95% CI 53.8%-59.8%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-GENSHARE-2025 | Mechanism, all abstract-present critical: Generative-model share (generative or both), 2025 | 57.8% (1015/1757; 95% CI 55.5%-60.0%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-GENSHARE-RHO | Mechanism, all abstract-present critical: Generative-model share (generative or both): Spearman ρ across 5 annual values (exact permutation P) | ρ=+0.90 (P=.083) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-GENSHARE-OR | Mechanism, all abstract-present critical: Generative-model share (generative or both): unadjusted record-level logistic OR per year | OR 2.026 per year (95% CI 1.893-2.168), P<.001 | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-GENSHARE-DELTA | Mechanism, all abstract-present critical: Generative-model share (generative or both): change 2021 to 2025, percentage points | +52.5 percentage points (5.3% to 57.8%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-FAB-ALL-2021 | Mechanism, all abstract-present critical: Fabrication share (confabulation or both), 2021 | 0.0% (0/245; 95% CI 0.0%-0.0% (bootstrap); exact Clopper-Pearson 0.0%-1.5%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-FAB-ALL-2022 | Mechanism, all abstract-present critical: Fabrication share (confabulation or both), 2022 | 0.4% (1/285; 95% CI 0.0%-1.1%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-FAB-ALL-2023 | Mechanism, all abstract-present critical: Fabrication share (confabulation or both), 2023 | 7.2% (39/543; 95% CI 5.2%-9.5%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-FAB-ALL-2024 | Mechanism, all abstract-present critical: Fabrication share (confabulation or both), 2024 | 13.0% (140/1076; 95% CI 11.1%-15.0%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-FAB-ALL-2025 | Mechanism, all abstract-present critical: Fabrication share (confabulation or both), 2025 | 11.4% (201/1757; 95% CI 10.0%-13.0%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-FAB-ALL-RHO | Mechanism, all abstract-present critical: Fabrication share (confabulation or both): Spearman ρ across 5 annual values (exact permutation P) | ρ=+0.90 (P=.083) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-FAB-ALL-OR | Mechanism, all abstract-present critical: Fabrication share (confabulation or both): unadjusted record-level logistic OR per year | OR 1.552 per year (95% CI 1.381-1.745), P<.001 | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-FAB-ALL-DELTA | Mechanism, all abstract-present critical: Fabrication share (confabulation or both): change 2021 to 2025, percentage points | +11.4 percentage points (0.0% to 11.4%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-FAB-GEN-2021 | Mechanism, generative-model papers: Fabrication share among generative, 2021 | 0.0% (0/13; 95% CI 0.0%-0.0% (bootstrap); exact Clopper-Pearson 0.0%-24.7%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-FAB-GEN-2022 | Mechanism, generative-model papers: Fabrication share among generative, 2022 | 14.3% (1/7; 95% CI 0.0%-50.0%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-FAB-GEN-2023 | Mechanism, generative-model papers: Fabrication share among generative, 2023 | 21.8% (39/179; 95% CI 15.9%-27.6%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-FAB-GEN-2024 | Mechanism, generative-model papers: Fabrication share among generative, 2024 | 22.9% (140/612; 95% CI 19.5%-26.2%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-FAB-GEN-2025 | Mechanism, generative-model papers: Fabrication share among generative, 2025 | 19.7% (200/1015; 95% CI 17.3%-22.0%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-FAB-GEN-RHO | Mechanism, generative-model papers: Fabrication share among generative: Spearman ρ across 5 annual values (exact permutation P) | ρ=+0.70 (P=.233) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-FAB-GEN-OR | Mechanism, generative-model papers: Fabrication share among generative: unadjusted record-level logistic OR per year | OR 0.977 per year (95% CI 0.839-1.136), P=.759 | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-FAB-GEN-DELTA | Mechanism, generative-model papers: Fabrication share among generative: change 2021 to 2025, percentage points | +19.7 percentage points (0.0% to 19.7%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-MECH-GENNOFAB | Generative-model papers without a fabrication concern, abstract-present critical | 37.0% (1446/3906) | 2021-2025 | outputs/T4_mechanism_facts.json |
| RES-TMP-MECH-FABDISC | Fabrication raised in a discriminative-only system | 1 | 2021-2025 | outputs/T4_mechanism_facts.json |
| RES-TMP-MECH-GATERECALL | Share of fabrication-involved records captured by the hallucination theme | 91.3% (348/381) | 2021-2025 | outputs/T4_mechanism_facts.json |
| RES-TMP-MECH-FABGATED | Fabrication-involved share among hallucination-gated records, pooled | 19.6% (348/1775) | 2021-2025 | outputs/T4_mechanism_facts.json |
| RES-TMP-KEEP-2021 | Prefilter keep rate, 2021 | 9.5% (1064/11,191; 95% CI 8.9%-10.0%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-KEEP-2022 | Prefilter keep rate, 2022 | 10.2% (1344/13,136; 95% CI 9.7%-10.8%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-KEEP-2023 | Prefilter keep rate, 2023 | 14.5% (2055/14,128; 95% CI 14.0%-15.1%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-KEEP-2024 | Prefilter keep rate, 2024 | 19.1% (3704/19,372; 95% CI 18.6%-19.7%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-KEEP-2025 | Prefilter keep rate, 2025 | 20.4% (5899/28,873; 95% CI 20.0%-20.9%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-KEEP-RHO | Prefilter keep rate: Spearman ρ across 5 annual values (exact permutation P) | ρ=+1.00 (P=.017) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-KEEP-OR | Prefilter keep rate: unadjusted record-level logistic OR per year | OR 1.273 per year (95% CI 1.256-1.291), P<.001 | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-KEEP-DELTA | Prefilter keep rate: change 2021 to 2025, percentage points | +10.9 percentage points (9.5% to 20.4%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-Q3-CRIT-2021 | Q3 comparison arm: Critical (Alarm+Caution), 2021 | 23.0% (26/113; 95% CI 15.4%-30.9%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-Q3-CRIT-2022 | Q3 comparison arm: Critical (Alarm+Caution), 2022 | 19.0% (20/105; 95% CI 11.4%-26.9%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-Q3-CRIT-2023 | Q3 comparison arm: Critical (Alarm+Caution), 2023 | 27.2% (49/180; 95% CI 20.6%-34.0%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-Q3-CRIT-2024 | Q3 comparison arm: Critical (Alarm+Caution), 2024 | 34.4% (11/32; 95% CI 18.5%-51.3%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-Q3-CRIT-2025 | Q3 comparison arm: Critical (Alarm+Caution), 2025 | 28.1% (119/423; 95% CI 24.0%-32.3%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-Q3-CRIT-RHO | Q3 comparison arm: Critical (Alarm+Caution): Spearman ρ across 5 annual values (exact permutation P) | ρ=+0.80 (P=.133) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-Q3-CRIT-OR | Q3 comparison arm: Critical (Alarm+Caution): unadjusted record-level logistic OR per year | OR 1.093 per year (95% CI 0.986-1.212), P=.092 | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-Q3-CRIT-DELTA | Q3 comparison arm: Critical (Alarm+Caution): change 2021 to 2025, percentage points | +5.1 percentage points (23.0% to 28.1%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-Q3-ALARM-2021 | Q3 comparison arm: Alarm, 2021 | 2.7% (3/113; 95% CI 0.0%-6.1%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-Q3-ALARM-2022 | Q3 comparison arm: Alarm, 2022 | 1.0% (1/105; 95% CI 0.0%-3.3%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-Q3-ALARM-2023 | Q3 comparison arm: Alarm, 2023 | 3.9% (7/180; 95% CI 1.3%-7.0%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-Q3-ALARM-2024 | Q3 comparison arm: Alarm, 2024 | 15.6% (5/32; 95% CI 3.7%-30.0%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-Q3-ALARM-2025 | Q3 comparison arm: Alarm, 2025 | 5.2% (22/423; 95% CI 3.2%-7.3%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-Q3-ALARM-RHO | Q3 comparison arm: Alarm: Spearman ρ across 5 annual values (exact permutation P) | ρ=+0.80 (P=.133) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-Q3-ALARM-OR | Q3 comparison arm: Alarm: unadjusted record-level logistic OR per year | OR 1.272 per year (95% CI 0.994-1.626), P=.056 | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-Q3-ALARM-DELTA | Q3 comparison arm: Alarm: change 2021 to 2025, percentage points | +2.5 percentage points (2.7% to 5.2%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-Q3-CAUT-2021 | Q3 comparison arm: Caution, 2021 | 20.4% (23/113; 95% CI 13.0%-28.0%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-Q3-CAUT-2022 | Q3 comparison arm: Caution, 2022 | 18.1% (19/105; 95% CI 10.5%-25.4%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-Q3-CAUT-2023 | Q3 comparison arm: Caution, 2023 | 23.3% (42/180; 95% CI 17.1%-30.1%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-Q3-CAUT-2024 | Q3 comparison arm: Caution, 2024 | 18.8% (6/32; 95% CI 6.0%-32.3%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-Q3-CAUT-2025 | Q3 comparison arm: Caution, 2025 | 22.9% (97/423; 95% CI 19.0%-26.8%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-Q3-CAUT-RHO | Q3 comparison arm: Caution: Spearman ρ across 5 annual values (exact permutation P) | ρ=+0.30 (P=.683) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-Q3-CAUT-OR | Q3 comparison arm: Caution: unadjusted record-level logistic OR per year | OR 1.047 per year (95% CI 0.939-1.168), P=.407 | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-Q3-CAUT-DELTA | Q3 comparison arm: Caution: change 2021 to 2025, percentage points | +2.6 percentage points (20.4% to 22.9%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-Q3-NEUT-2021 | Q3 comparison arm: Neutral, 2021 | 3.5% (4/113; 95% CI 0.8%-7.4%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-Q3-NEUT-2022 | Q3 comparison arm: Neutral, 2022 | 4.8% (5/105; 95% CI 1.0%-9.1%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-Q3-NEUT-2023 | Q3 comparison arm: Neutral, 2023 | 5.6% (10/180; 95% CI 2.3%-9.2%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-Q3-NEUT-2024 | Q3 comparison arm: Neutral, 2024 | 6.2% (2/32; 95% CI 0.0%-16.7%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-Q3-NEUT-2025 | Q3 comparison arm: Neutral, 2025 | 2.6% (11/423; 95% CI 1.2%-4.3%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-Q3-NEUT-RHO | Q3 comparison arm: Neutral: Spearman ρ across 5 annual values (exact permutation P) | ρ=+0.00 (P>.99) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-Q3-NEUT-OR | Q3 comparison arm: Neutral: unadjusted record-level logistic OR per year | OR 0.877 per year (95% CI 0.699-1.100), P=.256 | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-Q3-NEUT-DELTA | Q3 comparison arm: Neutral: change 2021 to 2025, percentage points | -0.9 percentage points (3.5% to 2.6%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-Q3-CO-2021 | Q3 comparison arm: Cautious Optimism, 2021 | 69.9% (79/113; 95% CI 60.7%-78.0%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-Q3-CO-2022 | Q3 comparison arm: Cautious Optimism, 2022 | 67.6% (71/105; 95% CI 58.1%-76.5%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-Q3-CO-2023 | Q3 comparison arm: Cautious Optimism, 2023 | 63.9% (115/180; 95% CI 57.1%-71.1%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-Q3-CO-2024 | Q3 comparison arm: Cautious Optimism, 2024 | 59.4% (19/32; 95% CI 42.4%-77.4%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-Q3-CO-2025 | Q3 comparison arm: Cautious Optimism, 2025 | 66.9% (283/423; 95% CI 62.5%-71.3%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-Q3-CO-RHO | Q3 comparison arm: Cautious Optimism: Spearman ρ across 5 annual values (exact permutation P) | ρ=-0.70 (P=.233) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-Q3-CO-OR | Q3 comparison arm: Cautious Optimism: unadjusted record-level logistic OR per year | OR 0.982 per year (95% CI 0.894-1.080), P=.714 | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-Q3-CO-DELTA | Q3 comparison arm: Cautious Optimism: change 2021 to 2025, percentage points | -3.0 percentage points (69.9% to 66.9%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-Q3-ADV-2021 | Q3 comparison arm: Advocacy, 2021 | 3.5% (4/113; 95% CI 0.8%-7.1%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-Q3-ADV-2022 | Q3 comparison arm: Advocacy, 2022 | 8.6% (9/105; 95% CI 3.8%-14.2%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-Q3-ADV-2023 | Q3 comparison arm: Advocacy, 2023 | 3.3% (6/180; 95% CI 1.1%-5.9%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-Q3-ADV-2024 | Q3 comparison arm: Advocacy, 2024 | 0.0% (0/32; 95% CI 0.0%-0.0% (bootstrap); exact Clopper-Pearson 0.0%-10.9%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-Q3-ADV-2025 | Q3 comparison arm: Advocacy, 2025 | 2.4% (10/423; 95% CI 1.0%-3.9%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-Q3-ADV-RHO | Q3 comparison arm: Advocacy: Spearman ρ across 5 annual values (exact permutation P) | ρ=-0.80 (P=.133) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-Q3-ADV-OR | Q3 comparison arm: Advocacy: unadjusted record-level logistic OR per year | OR 0.792 per year (95% CI 0.626-1.004), P=.054 | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-TMP-Q3-ADV-DELTA | Q3 comparison arm: Advocacy: change 2021 to 2025, percentage points | -1.2 percentage points (3.5% to 2.4%) | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |

### 3. Headline themes: LLM prevalence share and lexicon mention share

| ID | Item | Value | Window | Source |
|---|---|---|---|---|
| RES-THM-LEX-PATIENTSAFETY-2021 | Patient safety: lexicon mention share among critical records, 2021 | 13.7% (37/270; 95% CI 9.5%-18.0%) | 2021-2025 | outputs/B6/B6_lexicon_annual.csv |
| RES-THM-LEX-PATIENTSAFETY-2022 | Patient safety: lexicon mention share among critical records, 2022 | 14.1% (47/333; 95% CI 10.4%-17.9%) | 2021-2025 | outputs/B6/B6_lexicon_annual.csv |
| RES-THM-LEX-PATIENTSAFETY-2023 | Patient safety: lexicon mention share among critical records, 2023 | 14.3% (89/624; 95% CI 11.2%-17.3%) | 2021-2025 | outputs/B6/B6_lexicon_annual.csv |
| RES-THM-LEX-PATIENTSAFETY-2024 | Patient safety: lexicon mention share among critical records, 2024 | 16.5% (203/1228; 95% CI 14.5%-18.6%) | 2021-2025 | outputs/B6/B6_lexicon_annual.csv |
| RES-THM-LEX-PATIENTSAFETY-2025 | Patient safety: lexicon mention share among critical records, 2025 | 19.2% (351/1828; 95% CI 17.5%-20.9%) | 2021-2025 | outputs/B6/B6_lexicon_annual.csv |
| RES-THM-LEX-PATIENTSAFETY-RHO | Patient safety: lexicon Spearman ρ (exact P) | ρ=+1.00 (P=.017) | 2021-2025 | outputs/B6/B6_lexicon_trends.csv |
| RES-THM-LEX-PATIENTSAFETY-OR | Patient safety: lexicon OR per year | OR 1.133 per year (95% CI 1.056-1.215), P<.001 | 2021-2025 | outputs/B6/B6_lexicon_trends.csv |
| RES-THM-LEX-PATIENTSAFETY-DIR | Patient safety: lexicon and LLM trends in the same direction | yes | 2021-2025 | outputs/B6/B6_lexicon_trends.csv |
| RES-THM-LLM-PATIENTSAFETY | Patient safety: LLM prevalence share series | see RES-TMP-TH-PATIENTSAFETY-2021 to -OR | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-THM-LEX-HALLUCINATIONERRORS-2021 | Hallucination / errors: lexicon mention share among critical records, 2021 | 8.1% (22/270; 95% CI 5.1%-11.5%) | 2021-2025 | outputs/B6/B6_lexicon_annual.csv |
| RES-THM-LEX-HALLUCINATIONERRORS-2022 | Hallucination / errors: lexicon mention share among critical records, 2022 | 7.2% (24/333; 95% CI 4.5%-10.1%) | 2021-2025 | outputs/B6/B6_lexicon_annual.csv |
| RES-THM-LEX-HALLUCINATIONERRORS-2023 | Hallucination / errors: lexicon mention share among critical records, 2023 | 13.9% (87/624; 95% CI 11.3%-16.7%) | 2021-2025 | outputs/B6/B6_lexicon_annual.csv |
| RES-THM-LEX-HALLUCINATIONERRORS-2024 | Hallucination / errors: lexicon mention share among critical records, 2024 | 20.7% (254/1228; 95% CI 18.5%-23.0%) | 2021-2025 | outputs/B6/B6_lexicon_annual.csv |
| RES-THM-LEX-HALLUCINATIONERRORS-2025 | Hallucination / errors: lexicon mention share among critical records, 2025 | 22.6% (414/1828; 95% CI 20.9%-24.7%) | 2021-2025 | outputs/B6/B6_lexicon_annual.csv |
| RES-THM-LEX-HALLUCINATIONERRORS-RHO | Hallucination / errors: lexicon Spearman ρ (exact P) | ρ=+0.90 (P=.083) | 2021-2025 | outputs/B6/B6_lexicon_trends.csv |
| RES-THM-LEX-HALLUCINATIONERRORS-OR | Hallucination / errors: lexicon OR per year | OR 1.384 per year (95% CI 1.284-1.492), P<.001 | 2021-2025 | outputs/B6/B6_lexicon_trends.csv |
| RES-THM-LEX-HALLUCINATIONERRORS-DIR | Hallucination / errors: lexicon and LLM trends in the same direction | yes | 2021-2025 | outputs/B6/B6_lexicon_trends.csv |
| RES-THM-LLM-HALLUCINATIONERRORS | Hallucination / errors: LLM prevalence share series | see RES-TMP-TH-HALLUCINATIONERRORS-2021 to -OR | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-THM-LEX-GOVERNANCEREGULATION-2021 | Governance / regulation: lexicon mention share among critical records, 2021 | 24.8% (67/270; 95% CI 19.9%-29.7%) | 2021-2025 | outputs/B6/B6_lexicon_annual.csv |
| RES-THM-LEX-GOVERNANCEREGULATION-2022 | Governance / regulation: lexicon mention share among critical records, 2022 | 22.5% (75/333; 95% CI 18.1%-27.5%) | 2021-2025 | outputs/B6/B6_lexicon_annual.csv |
| RES-THM-LEX-GOVERNANCEREGULATION-2023 | Governance / regulation: lexicon mention share among critical records, 2023 | 20.8% (130/624; 95% CI 17.6%-23.9%) | 2021-2025 | outputs/B6/B6_lexicon_annual.csv |
| RES-THM-LEX-GOVERNANCEREGULATION-2024 | Governance / regulation: lexicon mention share among critical records, 2024 | 19.5% (240/1228; 95% CI 17.5%-21.9%) | 2021-2025 | outputs/B6/B6_lexicon_annual.csv |
| RES-THM-LEX-GOVERNANCEREGULATION-2025 | Governance / regulation: lexicon mention share among critical records, 2025 | 29.9% (547/1828; 95% CI 27.7%-32.1%) | 2021-2025 | outputs/B6/B6_lexicon_annual.csv |
| RES-THM-LEX-GOVERNANCEREGULATION-RHO | Governance / regulation: lexicon Spearman ρ (exact P) | ρ=+0.00 (P>.99) | 2021-2025 | outputs/B6/B6_lexicon_trends.csv |
| RES-THM-LEX-GOVERNANCEREGULATION-OR | Governance / regulation: lexicon OR per year | OR 1.128 per year (95% CI 1.062-1.198), P<.001 | 2021-2025 | outputs/B6/B6_lexicon_trends.csv |
| RES-THM-LEX-GOVERNANCEREGULATION-DIR | Governance / regulation: lexicon and LLM trends in the same direction | no | 2021-2025 | outputs/B6/B6_lexicon_trends.csv |
| RES-THM-LLM-GOVERNANCEREGULATION | Governance / regulation: LLM prevalence share series | see RES-TMP-TH-GOVERNANCEREGULATION-2021 to -OR | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-THM-LEX-ETHICSANDBIAS-2021 | Ethics & bias: lexicon mention share among critical records, 2021 | 44.1% (119/270; 95% CI 38.2%-49.6%) | 2021-2025 | outputs/B6/B6_lexicon_annual.csv |
| RES-THM-LEX-ETHICSANDBIAS-2022 | Ethics & bias: lexicon mention share among critical records, 2022 | 45.9% (153/333; 95% CI 40.2%-51.4%) | 2021-2025 | outputs/B6/B6_lexicon_annual.csv |
| RES-THM-LEX-ETHICSANDBIAS-2023 | Ethics & bias: lexicon mention share among critical records, 2023 | 41.5% (259/624; 95% CI 37.6%-45.4%) | 2021-2025 | outputs/B6/B6_lexicon_annual.csv |
| RES-THM-LEX-ETHICSANDBIAS-2024 | Ethics & bias: lexicon mention share among critical records, 2024 | 37.9% (465/1228; 95% CI 35.0%-40.6%) | 2021-2025 | outputs/B6/B6_lexicon_annual.csv |
| RES-THM-LEX-ETHICSANDBIAS-2025 | Ethics & bias: lexicon mention share among critical records, 2025 | 44.8% (819/1828; 95% CI 42.4%-47.1%) | 2021-2025 | outputs/B6/B6_lexicon_annual.csv |
| RES-THM-LEX-ETHICSANDBIAS-RHO | Ethics & bias: lexicon Spearman ρ (exact P) | ρ=-0.20 (P=.783) | 2021-2025 | outputs/B6/B6_lexicon_trends.csv |
| RES-THM-LEX-ETHICSANDBIAS-OR | Ethics & bias: lexicon OR per year | OR 1.008 per year (95% CI 0.959-1.060), P=.753 | 2021-2025 | outputs/B6/B6_lexicon_trends.csv |
| RES-THM-LEX-ETHICSANDBIAS-DIR | Ethics & bias: lexicon and LLM trends in the same direction | no | 2021-2025 | outputs/B6/B6_lexicon_trends.csv |
| RES-THM-LLM-ETHICSANDBIAS | Ethics & bias: LLM prevalence share series | see RES-TMP-TH-ETHICSANDBIAS-2021 to -OR | 2021-2025 | outputs/T4_annual_all_domains.csv; outputs/T4_trend_tests.csv |
| RES-THM-REGCOUNT-2021 | Regulation-themed critical records, annual count, 2021 | 148 of 270 critical records | 2021-2025 | outputs/T4_theme_counts.csv |
| RES-THM-REGCOUNT-2022 | Regulation-themed critical records, annual count, 2022 | 186 of 333 critical records | 2021-2025 | outputs/T4_theme_counts.csv |
| RES-THM-REGCOUNT-2023 | Regulation-themed critical records, annual count, 2023 | 259 of 624 critical records | 2021-2025 | outputs/T4_theme_counts.csv |
| RES-THM-REGCOUNT-2024 | Regulation-themed critical records, annual count, 2024 | 420 of 1228 critical records | 2021-2025 | outputs/T4_theme_counts.csv |
| RES-THM-REGCOUNT-2025 | Regulation-themed critical records, annual count, 2025 | 580 of 1828 critical records | 2021-2025 | outputs/T4_theme_counts.csv |

### 4. Specialty

| ID | Item | Value | Window | Source |
|---|---|---|---|---|
| RES-SPC-OBS-MENTALHEALTHPSYCHIATRY | Mental Health / Psychiatry: observed critical rate | 50.3% (196/390; 95% CI 45.7%-55.2%) | 2021-2025 | final/data/specialty_2021_2025.csv |
| RES-SPC-AMP-MENTALHEALTHPSYCHIATRY | Mental Health / Psychiatry: adjusted average marginal probability (B4) | 46.7% (95% CI 40.6%-52.9%) | 2021-2025 | outputs/B4/B4_primary_critical_AMP.csv |
| RES-SPC-FDA-MENTALHEALTHPSYCHIATRY | Mental Health / Psychiatry: FDA cleared AI/ML devices (mapped panels) | 0 (structural zero) | FDA list 1995-2025 | final/data/specialty_2021_2025.csv (load_fda_device_counts) |
| RES-SPC-OBS-MEDICALINFORMATICSDIGITA | Medical Informatics / Digital Health: observed critical rate | 45.2% (1674/3701; 95% CI 43.6%-46.9%) | 2021-2025 | final/data/specialty_2021_2025.csv |
| RES-SPC-AMP-MEDICALINFORMATICSDIGITA | Medical Informatics / Digital Health: adjusted average marginal probability (B4) | 42.0% (95% CI 39.6%-44.4%) | 2021-2025 | outputs/B4/B4_primary_critical_AMP.csv |
| RES-SPC-FDA-MEDICALINFORMATICSDIGITA | Medical Informatics / Digital Health: FDA cleared AI/ML devices (mapped panels) | 0 (structural zero) | FDA list 1995-2025 | final/data/specialty_2021_2025.csv (load_fda_device_counts) |
| RES-SPC-OBS-NURSING | Nursing: observed critical rate | 41.4% (94/227; 95% CI 34.5%-47.5%) | 2021-2025 | final/data/specialty_2021_2025.csv |
| RES-SPC-AMP-NURSING | Nursing: adjusted average marginal probability (B4) | 38.2% (95% CI 30.9%-45.9%) | 2021-2025 | outputs/B4/B4_primary_critical_AMP.csv |
| RES-SPC-FDA-NURSING | Nursing: FDA cleared AI/ML devices (mapped panels) | 0 (structural zero) | FDA list 1995-2025 | final/data/specialty_2021_2025.csv (load_fda_device_counts) |
| RES-SPC-OBS-DERMATOLOGY | Dermatology: observed critical rate | 37.4% (99/265; 95% CI 31.7%-43.1%) | 2021-2025 | final/data/specialty_2021_2025.csv |
| RES-SPC-AMP-DERMATOLOGY | Dermatology: adjusted average marginal probability (B4) | 35.9% (95% CI 30.7%-41.6%) | 2021-2025 | outputs/B4/B4_primary_critical_AMP.csv |
| RES-SPC-FDA-DERMATOLOGY | Dermatology: FDA cleared AI/ML devices (mapped panels) | 0 (structural zero) | FDA list 1995-2025 | final/data/specialty_2021_2025.csv (load_fda_device_counts) |
| RES-SPC-OBS-MEDICALEDUCATION | Medical Education: observed critical rate | 34.9% (306/876; 95% CI 31.9%-38.3%) | 2021-2025 | final/data/specialty_2021_2025.csv |
| RES-SPC-AMP-MEDICALEDUCATION | Medical Education: adjusted average marginal probability (B4) | 30.1% (95% CI 26.5%-33.9%) | 2021-2025 | outputs/B4/B4_primary_critical_AMP.csv |
| RES-SPC-FDA-MEDICALEDUCATION | Medical Education: FDA cleared AI/ML devices (mapped panels) | 0 (structural zero) | FDA list 1995-2025 | final/data/specialty_2021_2025.csv (load_fda_device_counts) |
| RES-SPC-OBS-MULTIDISCIPLINARYOTHER | Multidisciplinary / Other: observed critical rate | 32.1% (63/196; 95% CI 25.3%-39.0%) | 2021-2025 | final/data/specialty_2021_2025.csv |
| RES-SPC-AMP-MULTIDISCIPLINARYOTHER | Multidisciplinary / Other: adjusted average marginal probability (B4) | 30.6% (95% CI 24.2%-37.7%) | 2021-2025 | outputs/B4/B4_primary_critical_AMP.csv |
| RES-SPC-FDA-MULTIDISCIPLINARYOTHER | Multidisciplinary / Other: FDA cleared AI/ML devices (mapped panels) | 4 | FDA list 1995-2025 | final/data/specialty_2021_2025.csv (load_fda_device_counts) |
| RES-SPC-OBS-SURGERY | Surgery: observed critical rate | 29.1% (347/1191; 95% CI 26.4%-31.8%) | 2021-2025 | final/data/specialty_2021_2025.csv |
| RES-SPC-AMP-SURGERY | Surgery: adjusted average marginal probability (B4) | 28.7% (95% CI 26.3%-31.3%) | 2021-2025 | outputs/B4/B4_primary_critical_AMP.csv |
| RES-SPC-FDA-SURGERY | Surgery: FDA cleared AI/ML devices (mapped panels) | 12 | FDA list 1995-2025 | final/data/specialty_2021_2025.csv (load_fda_device_counts) |
| RES-SPC-OBS-EMERGENCYMEDICINECRITICA | Emergency Medicine / Critical Care: observed critical rate | 27.9% (86/308; 95% CI 23.2%-33.2%) | 2021-2025 | final/data/specialty_2021_2025.csv |
| RES-SPC-AMP-EMERGENCYMEDICINECRITICA | Emergency Medicine / Critical Care: adjusted average marginal probability (B4) | 28.2% (95% CI 23.7%-33.2%) | 2021-2025 | outputs/B4/B4_primary_critical_AMP.csv |
| RES-SPC-FDA-EMERGENCYMEDICINECRITICA | Emergency Medicine / Critical Care: FDA cleared AI/ML devices (mapped panels) | 26 | FDA list 1995-2025 | final/data/specialty_2021_2025.csv (load_fda_device_counts) |
| RES-SPC-OBS-OBSTETRICSGYNECOLOGY | Obstetrics / Gynecology: observed critical rate | 25.1% (49/195; 95% CI 19.2%-31.5%) | 2021-2025 | final/data/specialty_2021_2025.csv |
| RES-SPC-AMP-OBSTETRICSGYNECOLOGY | Obstetrics / Gynecology: adjusted average marginal probability (B4) | 25.7% (95% CI 20.1%-32.3%) | 2021-2025 | outputs/B4/B4_primary_critical_AMP.csv |
| RES-SPC-FDA-OBSTETRICSGYNECOLOGY | Obstetrics / Gynecology: FDA cleared AI/ML devices (mapped panels) | 4 | FDA list 1995-2025 | final/data/specialty_2021_2025.csv (load_fda_device_counts) |
| RES-SPC-OBS-DENTISTRY | Dentistry: observed critical rate | 25.0% (145/581; 95% CI 21.4%-28.6%) | 2021-2025 | final/data/specialty_2021_2025.csv |
| RES-SPC-AMP-DENTISTRY | Dentistry: adjusted average marginal probability (B4) | 28.1% (95% CI 24.4%-32.1%) | 2021-2025 | outputs/B4/B4_primary_critical_AMP.csv |
| RES-SPC-FDA-DENTISTRY | Dentistry: FDA cleared AI/ML devices (mapped panels) | 5 | FDA list 1995-2025 | final/data/specialty_2021_2025.csv (load_fda_device_counts) |
| RES-SPC-OBS-NEUROLOGYNEUROSCIENCE | Neurology / Neuroscience: observed critical rate | 23.8% (69/290; 95% CI 18.7%-28.6%) | 2021-2025 | final/data/specialty_2021_2025.csv |
| RES-SPC-AMP-NEUROLOGYNEUROSCIENCE | Neurology / Neuroscience: adjusted average marginal probability (B4) | 25.0% (95% CI 20.0%-30.7%) | 2021-2025 | outputs/B4/B4_primary_critical_AMP.csv |
| RES-SPC-FDA-NEUROLOGYNEUROSCIENCE | Neurology / Neuroscience: FDA cleared AI/ML devices (mapped panels) | 65 | FDA list 1995-2025 | final/data/specialty_2021_2025.csv (load_fda_device_counts) |
| RES-SPC-OBS-PEDIATRICS | Pediatrics: observed critical rate | 23.8% (72/303; 95% CI 19.0%-28.4%) | 2021-2025 | final/data/specialty_2021_2025.csv |
| RES-SPC-AMP-PEDIATRICS | Pediatrics: adjusted average marginal probability (B4) | 24.0% (95% CI 19.8%-28.8%) | 2021-2025 | outputs/B4/B4_primary_critical_AMP.csv |
| RES-SPC-FDA-PEDIATRICS | Pediatrics: FDA cleared AI/ML devices (mapped panels) | 0 (structural zero) | FDA list 1995-2025 | final/data/specialty_2021_2025.csv (load_fda_device_counts) |
| RES-SPC-OBS-INTERNALMEDICINEPRIMARYC | Internal Medicine / Primary Care: observed critical rate | 21.6% (202/936; 95% CI 19.0%-24.3%) | 2021-2025 | final/data/specialty_2021_2025.csv |
| RES-SPC-AMP-INTERNALMEDICINEPRIMARYC | Internal Medicine / Primary Care: adjusted average marginal probability (B4) | 23.4% (95% CI 20.6%-26.5%) | 2021-2025 | outputs/B4/B4_primary_critical_AMP.csv |
| RES-SPC-FDA-INTERNALMEDICINEPRIMARYC | Internal Medicine / Primary Care: FDA cleared AI/ML devices (mapped panels) | 24 | FDA list 1995-2025 | final/data/specialty_2021_2025.csv (load_fda_device_counts) |
| RES-SPC-OBS-RADIOLOGYDIAGNOSTICIMAGI | Radiology / Diagnostic Imaging: observed critical rate | 20.4% (361/1769; 95% CI 18.6%-22.4%) | 2021-2025 | final/data/specialty_2021_2025.csv |
| RES-SPC-AMP-RADIOLOGYDIAGNOSTICIMAGI | Radiology / Diagnostic Imaging: adjusted average marginal probability (B4) | 23.0% (95% CI 20.9%-25.3%) | 2021-2025 | outputs/B4/B4_primary_critical_AMP.csv |
| RES-SPC-FDA-RADIOLOGYDIAGNOSTICIMAGI | Radiology / Diagnostic Imaging: FDA cleared AI/ML devices (mapped panels) | 1094 | FDA list 1995-2025 | final/data/specialty_2021_2025.csv (load_fda_device_counts) |
| RES-SPC-OBS-PATHOLOGYLABORATORYMEDIC | Pathology / Laboratory Medicine: observed critical rate | 20.4% (81/398; 95% CI 16.2%-24.4%) | 2021-2025 | final/data/specialty_2021_2025.csv |
| RES-SPC-AMP-PATHOLOGYLABORATORYMEDIC | Pathology / Laboratory Medicine: adjusted average marginal probability (B4) | 21.8% (95% CI 18.2%-25.9%) | 2021-2025 | outputs/B4/B4_primary_critical_AMP.csv |
| RES-SPC-FDA-PATHOLOGYLABORATORYMEDIC | Pathology / Laboratory Medicine: FDA cleared AI/ML devices (mapped panels) | 50 | FDA list 1995-2025 | final/data/specialty_2021_2025.csv (load_fda_device_counts) |
| RES-SPC-OBS-ONCOLOGY | Oncology: observed critical rate | 18.7% (227/1211; 95% CI 16.5%-21.0%) | 2021-2025 | final/data/specialty_2021_2025.csv |
| RES-SPC-AMP-ONCOLOGY | Oncology: adjusted average marginal probability (B4) | 21.1% (95% CI 18.8%-23.7%) | 2021-2025 | outputs/B4/B4_primary_critical_AMP.csv |
| RES-SPC-FDA-ONCOLOGY | Oncology: FDA cleared AI/ML devices (mapped panels) | 0 (structural zero) | FDA list 1995-2025 | final/data/specialty_2021_2025.csv (load_fda_device_counts) |
| RES-SPC-OBS-OPHTHALMOLOGY | Ophthalmology: observed critical rate | 18.5% (124/669; 95% CI 15.7%-21.6%) | 2021-2025 | final/data/specialty_2021_2025.csv |
| RES-SPC-AMP-OPHTHALMOLOGY | Ophthalmology: adjusted average marginal probability (B4) | 21.6% (95% CI 18.7%-24.8%) | 2021-2025 | outputs/B4/B4_primary_critical_AMP.csv |
| RES-SPC-FDA-OPHTHALMOLOGY | Ophthalmology: FDA cleared AI/ML devices (mapped panels) | 10 | FDA list 1995-2025 | final/data/specialty_2021_2025.csv (load_fda_device_counts) |
| RES-SPC-OBS-CARDIOLOGY | Cardiology: observed critical rate | 16.1% (87/542; 95% CI 12.8%-19.2%) | 2021-2025 | final/data/specialty_2021_2025.csv |
| RES-SPC-AMP-CARDIOLOGY | Cardiology: adjusted average marginal probability (B4) | 17.6% (95% CI 14.3%-21.4%) | 2021-2025 | outputs/B4/B4_primary_critical_AMP.csv |
| RES-SPC-FDA-CARDIOLOGY | Cardiology: FDA cleared AI/ML devices (mapped panels) | 136 | FDA list 1995-2025 | final/data/specialty_2021_2025.csv (load_fda_device_counts) |
| RES-SPC-RANGE | Observed critical-rate range across the 18 categories | Mental Health / Psychiatry 50.3% (196/390) to Cardiology 16.1% (87/542) | 2021-2025 | final/data/specialty_2021_2025.csv |
| RES-SPC-FDA-RHO18 | Critical rate vs FDA cleared-device count (zero-order) (n=18) | ρ=-0.61 (two-sided P=.007; one-sided P=.004; permutation one-sided P=.005) | 2021-2025 | final/data/fda_robustness.csv |
| RES-SPC-GEN-RHO | Critical rate vs generative-model share (n=18) | ρ=+0.01 (two-sided P=.971) | 2021-2025 | final/data/fda_robustness.csv |
| RES-SPC-FDAGEN-RHO | FDA cleared-device count vs generative-model share (n=18) | ρ=-0.03 (two-sided P=.913) | 2021-2025 | final/data/fda_robustness.csv |
| RES-SPC-FDA-PARTIAL | Partial: critical rate vs FDA count, controlling generative-model share (n=18) | ρ=-0.61 (two-sided P=.010) | 2021-2025 | final/data/fda_robustness.csv |
| RES-SPC-FDA-RHO11 | Critical rate vs FDA count, structural zeros dropped (n=11) | ρ=-0.58 (two-sided P=.062; one-sided P=.031; permutation one-sided P=.036) | 2021-2025 | final/data/fda_robustness.csv |
| RES-SPC-EVAL-RHO | (sensitivity) Critical rate vs in-corpus evaluation-share proxy (n=18) | ρ=-0.48 (two-sided P=.045; one-sided P=.022; permutation one-sided P=.023) | 2021-2025 | final/data/fda_robustness.csv |
| RES-SPC-FDA-LABEL | Status of the FDA association | exploratory ecological association (18 category-level units) | 2021-2025 | Batch 2c brief, decision D4b |

### 5. Geography

| ID | Item | Value | Window | Source |
|---|---|---|---|---|
| RES-GEO-NCTY50 | Countries with >= 50 first-author records | 32 | 2021-2025 | final/data/country_2021_2025.csv |
| RES-GEO-NCTY20 | Countries with >= 20 first-author records | 42 | 2021-2025 | final/data/country_2021_2025.csv |
| RES-GEO-CTY-UNITEDSTATES | United States: critical rate (n >=50) | 34.2% (1226/3586; 95% CI 32.7%-35.7%) | 2021-2025 | final/data/country_2021_2025.csv |
| RES-GEO-CTY-CHINA | China: critical rate (n >=50) | 14.9% (230/1540; 95% CI 13.2%-16.6%) | 2021-2025 | final/data/country_2021_2025.csv |
| RES-GEO-CTY-UNITEDKINGDOM | United Kingdom: critical rate (n >=50) | 40.0% (420/1049; 95% CI 37.1%-42.9%) | 2021-2025 | final/data/country_2021_2025.csv |
| RES-GEO-CTY-GERMANY | Germany: critical rate (n >=50) | 35.9% (232/647; 95% CI 32.3%-39.6%) | 2021-2025 | final/data/country_2021_2025.csv |
| RES-GEO-CTY-ITALY | Italy: critical rate (n >=50) | 25.0% (148/593; 95% CI 21.6%-28.7%) | 2021-2025 | final/data/country_2021_2025.csv |
| RES-GEO-CTY-CANADA | Canada: critical rate (n >=50) | 38.3% (183/478; 95% CI 34.1%-42.5%) | 2021-2025 | final/data/country_2021_2025.csv |
| RES-GEO-CTY-INDIA | India: critical rate (n >=50) | 19.7% (77/390; 95% CI 15.9%-23.9%) | 2021-2025 | final/data/country_2021_2025.csv |
| RES-GEO-CTY-SOUTHKOREA | South Korea: critical rate (n >=50) | 19.5% (75/384; 95% CI 15.6%-23.7%) | 2021-2025 | final/data/country_2021_2025.csv |
| RES-GEO-CTY-AUSTRALIA | Australia: critical rate (n >=50) | 43.8% (155/354; 95% CI 38.1%-49.2%) | 2021-2025 | final/data/country_2021_2025.csv |
| RES-GEO-CTY-TURKEY | Turkey: critical rate (n >=50) | 36.2% (122/337; 95% CI 30.9%-41.2%) | 2021-2025 | final/data/country_2021_2025.csv |
| RES-GEO-CTY-JAPAN | Japan: critical rate (n >=50) | 18.3% (60/327; 95% CI 14.7%-22.6%) | 2021-2025 | final/data/country_2021_2025.csv |
| RES-GEO-CTY-NETHERLANDS | Netherlands: critical rate (n >=50) | 44.2% (130/294; 95% CI 38.4%-50.0%) | 2021-2025 | final/data/country_2021_2025.csv |
| RES-GEO-CTY-FRANCE | France: critical rate (n >=50) | 26.3% (66/251; 95% CI 21.1%-32.3%) | 2021-2025 | final/data/country_2021_2025.csv |
| RES-GEO-CTY-SPAIN | Spain: critical rate (n >=50) | 25.4% (49/193; 95% CI 18.7%-31.6%) | 2021-2025 | final/data/country_2021_2025.csv |
| RES-GEO-CTY-SAUDIARABIA | Saudi Arabia: critical rate (n >=50) | 23.0% (41/178; 95% CI 17.4%-29.2%) | 2021-2025 | final/data/country_2021_2025.csv |
| RES-GEO-CTY-IRAN | Iran: critical rate (n >=50) | 17.6% (30/170; 95% CI 12.4%-22.9%) | 2021-2025 | final/data/country_2021_2025.csv |
| RES-GEO-CTY-SWITZERLAND | Switzerland: critical rate (n >=50) | 41.7% (70/168; 95% CI 34.5%-48.8%) | 2021-2025 | final/data/country_2021_2025.csv |
| RES-GEO-CTY-ISRAEL | Israel: critical rate (n >=50) | 34.2% (52/152; 95% CI 27.0%-41.5%) | 2021-2025 | final/data/country_2021_2025.csv |
| RES-GEO-CTY-SINGAPORE | Singapore: critical rate (n >=50) | 27.0% (38/141; 95% CI 19.9%-34.0%) | 2021-2025 | final/data/country_2021_2025.csv |
| RES-GEO-CTY-TAIWAN | Taiwan: critical rate (n >=50) | 20.9% (28/134; 95% CI 13.4%-27.6%) | 2021-2025 | final/data/country_2021_2025.csv |
| RES-GEO-CTY-BRAZIL | Brazil: critical rate (n >=50) | 22.0% (24/109; 95% CI 14.7%-30.3%) | 2021-2025 | final/data/country_2021_2025.csv |
| RES-GEO-CTY-SWEDEN | Sweden: critical rate (n >=50) | 35.8% (38/106; 95% CI 26.4%-45.3%) | 2021-2025 | final/data/country_2021_2025.csv |
| RES-GEO-CTY-DENMARK | Denmark: critical rate (n >=50) | 41.8% (41/98; 95% CI 32.7%-51.0%) | 2021-2025 | final/data/country_2021_2025.csv |
| RES-GEO-CTY-POLAND | Poland: critical rate (n >=50) | 23.3% (20/86; 95% CI 14.0%-32.6%) | 2021-2025 | final/data/country_2021_2025.csv |
| RES-GEO-CTY-HONGKONG | Hong Kong: critical rate (n >=50) | 30.1% (25/83; 95% CI 20.5%-41.0%) | 2021-2025 | final/data/country_2021_2025.csv |
| RES-GEO-CTY-BELGIUM | Belgium: critical rate (n >=50) | 35.4% (28/79; 95% CI 25.3%-45.6%) | 2021-2025 | final/data/country_2021_2025.csv |
| RES-GEO-CTY-PORTUGAL | Portugal: critical rate (n >=50) | 24.0% (18/75; 95% CI 14.7%-33.3%) | 2021-2025 | final/data/country_2021_2025.csv |
| RES-GEO-CTY-GREECE | Greece: critical rate (n >=50) | 25.0% (18/72; 95% CI 15.3%-34.8%) | 2021-2025 | final/data/country_2021_2025.csv |
| RES-GEO-CTY-AUSTRIA | Austria: critical rate (n >=50) | 31.4% (22/70; 95% CI 21.4%-41.4%) | 2021-2025 | final/data/country_2021_2025.csv |
| RES-GEO-CTY-IRELAND | Ireland: critical rate (n >=50) | 41.4% (29/70; 95% CI 30.0%-52.9%) | 2021-2025 | final/data/country_2021_2025.csv |
| RES-GEO-CTY-UNITEDARABEMIRATES | United Arab Emirates: critical rate (n >=50) | 23.7% (14/59; 95% CI 13.6%-35.6%) | 2021-2025 | final/data/country_2021_2025.csv |
| RES-GEO-CTY-ROMANIA | Romania: critical rate (n >=50) | 14.0% (7/50; 95% CI 6.0%-24.0%) | 2021-2025 | final/data/country_2021_2025.csv |
| RES-GEO-CTY-NORWAY | Norway: critical rate (n 20-49) | 22.4% (11/49; 95% CI 10.2%-34.7%) | 2021-2025 | final/data/country_2021_2025.csv |
| RES-GEO-CTY-THAILAND | Thailand: critical rate (n 20-49) | 22.4% (11/49; 95% CI 10.2%-34.7%) | 2021-2025 | final/data/country_2021_2025.csv |
| RES-GEO-CTY-QATAR | Qatar: critical rate (n 20-49) | 29.5% (13/44; 95% CI 18.1%-43.2%) | 2021-2025 | final/data/country_2021_2025.csv |
| RES-GEO-CTY-EGYPT | Egypt: critical rate (n 20-49) | 26.2% (11/42; 95% CI 14.3%-40.5%) | 2021-2025 | final/data/country_2021_2025.csv |
| RES-GEO-CTY-FINLAND | Finland: critical rate (n 20-49) | 32.5% (13/40; 95% CI 17.5%-47.5%) | 2021-2025 | final/data/country_2021_2025.csv |
| RES-GEO-CTY-MALAYSIA | Malaysia: critical rate (n 20-49) | 38.2% (13/34; 95% CI 23.5%-55.9%) | 2021-2025 | final/data/country_2021_2025.csv |
| RES-GEO-CTY-HUNGARY | Hungary: critical rate (n 20-49) | 33.3% (8/24; 95% CI 16.7%-50.0%) | 2021-2025 | final/data/country_2021_2025.csv |
| RES-GEO-CTY-CHILE | Chile: critical rate (n 20-49) | 42.9% (9/21; 95% CI 23.8%-62.0%) | 2021-2025 | final/data/country_2021_2025.csv |
| RES-GEO-CTY-COLOMBIA | Colombia: critical rate (n 20-49) | 15.0% (3/20; 95% CI 0.0%-35.0%) | 2021-2025 | final/data/country_2021_2025.csv |
| RES-GEO-CTY-SOUTHAFRICA | South Africa: critical rate (n 20-49) | 40.0% (8/20; 95% CI 20.0%-60.0%) | 2021-2025 | final/data/country_2021_2025.csv |
| RES-GEO-REG-EASTASIA | East Asia: critical rate (corrected n) | 17.7% (478/2702; 95% CI 16.3%-19.3%) | 2021-2025 | final/data/region_2021_2025.csv |
| RES-GEO-AMP-EASTASIA | East Asia: adjusted average marginal probability (B4) | 19.3% (95% CI 17.3%-21.6%) | 2021-2025 | outputs/B4/B4_primary_critical_AMP.csv |
| RES-GEO-AOR-EASTASIA | East Asia vs North America: adjusted OR (B4) | OR 0.44 (95% CI 0.38-0.51), P<.001 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv |
| RES-GEO-REG-EASTERNEUROPE | Eastern Europe: critical rate (corrected n) | 27.9% (76/272; 95% CI 22.6%-33.6%) | 2021-2025 | final/data/region_2021_2025.csv |
| RES-GEO-AMP-EASTERNEUROPE | Eastern Europe: adjusted average marginal probability (B4) | 29.4% (95% CI 24.7%-34.7%) | 2021-2025 | outputs/B4/B4_primary_critical_AMP.csv |
| RES-GEO-AOR-EASTERNEUROPE | Eastern Europe vs North America: adjusted OR (B4) | OR 0.80 (95% CI 0.61-1.04), P=.098 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv |
| RES-GEO-REG-LATINAMERICAOCEANIA | Latin America / Oceania: critical rate (corrected n) | 38.3% (245/639; 95% CI 34.6%-42.2%) | 2021-2025 | final/data/region_2021_2025.csv |
| RES-GEO-AMP-LATINAMERICAOCEANIA | Latin America / Oceania: adjusted average marginal probability (B4) | 36.2% (95% CI 32.7%-39.8%) | 2021-2025 | outputs/B4/B4_primary_critical_AMP.csv |
| RES-GEO-AOR-LATINAMERICAOCEANIA | Latin America / Oceania vs North America: adjusted OR (B4) | OR 1.11 (95% CI 0.93-1.33), P=.237 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv |
| RES-GEO-REG-MIDDLEEASTNORTHAFRICA | Middle East / North Africa: critical rate (corrected n) | 29.8% (394/1322; 95% CI 27.1%-32.3%) | 2021-2025 | final/data/region_2021_2025.csv |
| RES-GEO-AMP-MIDDLEEASTNORTHAFRICA | Middle East / North Africa: adjusted average marginal probability (B4) | 29.3% (95% CI 26.9%-31.8%) | 2021-2025 | outputs/B4/B4_primary_critical_AMP.csv |
| RES-GEO-AOR-MIDDLEEASTNORTHAFRICA | Middle East / North Africa vs North America: adjusted OR (B4) | OR 0.79 (95% CI 0.68-0.91), P=.001 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv |
| RES-GEO-REG-NORTHAMERICA | North America: critical rate (corrected n) | 34.9% (1472/4221; 95% CI 33.5%-36.3%) | 2021-2025 | final/data/region_2021_2025.csv |
| RES-GEO-AMP-NORTHAMERICA | North America: adjusted average marginal probability (B4) | 33.9% (95% CI 32.4%-35.5%) | 2021-2025 | outputs/B4/B4_primary_critical_AMP.csv |
| RES-GEO-REG-SOUTHSOUTHEASTASIA | South/Southeast Asia: critical rate (corrected n) | 24.4% (160/656; 95% CI 21.4%-27.8%) | 2021-2025 | final/data/region_2021_2025.csv |
| RES-GEO-AMP-SOUTHSOUTHEASTASIA | South/Southeast Asia: adjusted average marginal probability (B4) | 23.5% (95% CI 20.4%-27.0%) | 2021-2025 | outputs/B4/B4_primary_critical_AMP.csv |
| RES-GEO-AOR-SOUTHSOUTHEASTASIA | South/Southeast Asia vs North America: adjusted OR (B4) | OR 0.57 (95% CI 0.46-0.71), P<.001 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv |
| RES-GEO-REG-SUBSAHARANAFRICA | Sub-Saharan Africa: critical rate (corrected n) | 42.9% (21/49; 95% CI 29.2%-57.1%) | 2021-2025 | final/data/region_2021_2025.csv |
| RES-GEO-AMP-SUBSAHARANAFRICA | Sub-Saharan Africa: adjusted average marginal probability (B4) | 36.2% (95% CI 24.4%-49.9%) | 2021-2025 | outputs/B4/B4_primary_critical_AMP.csv |
| RES-GEO-AOR-SUBSAHARANAFRICA | Sub-Saharan Africa vs North America: adjusted OR (B4) | OR 1.11 (95% CI 0.60-2.06), P=.731 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv |
| RES-GEO-REG-UNKNOWN | Unknown: critical rate (corrected n) | 32.3% (163/504; 95% CI 28.5%-36.2%) | 2021-2025 | final/data/region_2021_2025.csv |
| RES-GEO-AMP-UNKNOWN | Unknown: adjusted average marginal probability (B4) | 28.2% (95% CI 23.5%-33.3%) | 2021-2025 | outputs/B4/B4_primary_critical_AMP.csv |
| RES-GEO-AOR-UNKNOWN | Unknown vs North America: adjusted OR (B4) | OR 0.74 (95% CI 0.57-0.98), P=.034 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv |
| RES-GEO-REG-WESTERNEUROPE | Western Europe: critical rate (corrected n) | 34.5% (1274/3693; 95% CI 33.0%-36.1%) | 2021-2025 | final/data/region_2021_2025.csv |
| RES-GEO-AMP-WESTERNEUROPE | Western Europe: adjusted average marginal probability (B4) | 35.2% (95% CI 33.1%-37.5%) | 2021-2025 | outputs/B4/B4_primary_critical_AMP.csv |
| RES-GEO-AOR-WESTERNEUROPE | Western Europe vs North America: adjusted OR (B4) | OR 1.06 (95% CI 0.95-1.19), P=.296 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv |
| RES-GEO-USCN-AOR | United States vs China: adjusted OR (B4 S4, country levels with >= 100 records) | OR 2.81 (95% CI 2.26-3.48), P<.001 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-GEO-EAWS-MEDICALEDUCATION | Medical Education: East Asia vs North America + Western Europe | East Asia 18.2% (26/143; 95% CI 11.9%-24.5%) vs 39.1% (164/419; 95% CI 34.6%-44.2%); difference -21.0 percentage points | 2021-2025 | final/data/ea_vs_nawe_within_specialty.csv |
| RES-GEO-EAWS-MEDICALINFORMATICSDIGITA | Medical Informatics / Digital Health: East Asia vs North America + Western Europe | East Asia 30.3% (185/611; 95% CI 26.5%-34.0%) vs 50.8% (1116/2197; 95% CI 48.7%-53.0%); difference -20.5 percentage points | 2021-2025 | final/data/ea_vs_nawe_within_specialty.csv |
| RES-GEO-EAWS-SURGERY | Surgery: East Asia vs North America + Western Europe | East Asia 17.4% (24/138; 95% CI 10.9%-23.9%) vs 31.3% (247/788; 95% CI 28.2%-34.6%); difference -14.0 percentage points | 2021-2025 | final/data/ea_vs_nawe_within_specialty.csv |
| RES-GEO-EAWS-RADIOLOGYDIAGNOSTICIMAGI | Radiology / Diagnostic Imaging: East Asia vs North America + Western Europe | East Asia 11.9% (57/479; 95% CI 9.2%-14.8%) vs 23.8% (245/1028; 95% CI 21.3%-26.5%); difference -11.9 percentage points | 2021-2025 | final/data/ea_vs_nawe_within_specialty.csv |
| RES-GEO-EAWS-OPHTHALMOLOGY | Ophthalmology: East Asia vs North America + Western Europe | East Asia 11.7% (21/179; 95% CI 7.3%-16.2%) vs 23.2% (73/314; 95% CI 19.1%-27.7%); difference -11.5 percentage points | 2021-2025 | final/data/ea_vs_nawe_within_specialty.csv |
| RES-GEO-EAWS-ONCOLOGY | Oncology: East Asia vs North America + Western Europe | East Asia 11.3% (35/309; 95% CI 7.8%-14.9%) vs 22.5% (145/644; 95% CI 19.3%-25.5%); difference -11.2 percentage points | 2021-2025 | final/data/ea_vs_nawe_within_specialty.csv |
| RES-GEO-EAWS-INTERNALMEDICINEPRIMARYC | Internal Medicine / Primary Care: East Asia vs North America + Western Europe | East Asia 13.0% (30/231; 95% CI 8.7%-17.3%) vs 24.0% (119/495; 95% CI 20.2%-28.3%); difference -11.1 percentage points | 2021-2025 | final/data/ea_vs_nawe_within_specialty.csv |
| RES-GEO-EAWS-DENTISTRY | Dentistry: East Asia vs North America + Western Europe | East Asia 17.0% (17/100; 95% CI 10.0%-24.0%) vs 27.9% (46/165; 95% CI 21.2%-34.5%); difference -10.9 percentage points | 2021-2025 | final/data/ea_vs_nawe_within_specialty.csv |
| RES-GEO-EAWS-PATHOLOGYLABORATORYMEDIC | Pathology / Laboratory Medicine: East Asia vs North America + Western Europe | East Asia 12.8% (10/78; 95% CI 6.4%-20.5%) vs 22.7% (59/260; 95% CI 17.3%-28.1%); difference -9.9 percentage points | 2021-2025 | final/data/ea_vs_nawe_within_specialty.csv |
| RES-GEO-EAWS-CARDIOLOGY | Cardiology: East Asia vs North America + Western Europe | East Asia 13.7% (13/95; 95% CI 7.4%-21.1%) vs 17.4% (61/351; 95% CI 13.4%-21.4%); difference -3.7 percentage points | 2021-2025 | final/data/ea_vs_nawe_within_specialty.csv |
| RES-GEO-EARW | East Asia critical rate reweighted to the North America + Western Europe specialty mix | 17.7% raw to 19.1% reweighted, vs 34.7% (share of gap closed 8%) | 2021-2025 | final/data/ea_reweighting.json (run_east_asia_diagnose.py logic) |

### 6. Publication format

| ID | Item | Value | Window | Source |
|---|---|---|---|---|
| RES-FMT-RESEARCHARTICLE-ALARM | Research Article: Alarm | 7.6% (647/8556; 95% CI 7.0%-8.1%) | 2021-2025 | final/data/pubtype_stance.csv |
| RES-FMT-RESEARCHARTICLE-CAUTION | Research Article: Caution | 25.2% (2152/8556; 95% CI 24.3%-26.1%) | 2021-2025 | final/data/pubtype_stance.csv |
| RES-FMT-RESEARCHARTICLE-NEUTRAL | Research Article: Neutral | 5.7% (491/8556; 95% CI 5.3%-6.2%) | 2021-2025 | final/data/pubtype_stance.csv |
| RES-FMT-RESEARCHARTICLE-CAUTIOUSOPTIMISM | Research Article: Cautious Optimism | 60.7% (5190/8556; 95% CI 59.5%-61.7%) | 2021-2025 | final/data/pubtype_stance.csv |
| RES-FMT-RESEARCHARTICLE-ADVOCACY | Research Article: Advocacy | 0.9% (76/8556; 95% CI 0.7%-1.1%) | 2021-2025 | final/data/pubtype_stance.csv |
| RES-FMT-RESEARCHARTICLE-CRITICAL | Research Article: Critical | 32.7% (2799/8556; 95% CI 31.6%-33.7%) | 2021-2025 | final/data/pubtype_stance.csv |
| RES-FMT-RESEARCHARTICLE-FAVOURABLE | Research Article: Favourable | 61.5% (5266/8556; 95% CI 60.5%-62.6%) | 2021-2025 | final/data/pubtype_stance.csv |
| RES-FMT-RESEARCHARTICLE-AMP | Research Article: adjusted average marginal probability of critical stance (B4) | 35.4% (95% CI 33.9%-36.9%) | 2021-2025 | outputs/B4/B4_primary_critical_AMP.csv |
| RES-FMT-REVIEW-ALARM | Review: Alarm | 1.1% (53/4611; 95% CI 0.8%-1.5%) | 2021-2025 | final/data/pubtype_stance.csv |
| RES-FMT-REVIEW-CAUTION | Review: Caution | 23.1% (1067/4611; 95% CI 21.9%-24.4%) | 2021-2025 | final/data/pubtype_stance.csv |
| RES-FMT-REVIEW-NEUTRAL | Review: Neutral | 2.1% (96/4611; 95% CI 1.7%-2.5%) | 2021-2025 | final/data/pubtype_stance.csv |
| RES-FMT-REVIEW-CAUTIOUSOPTIMISM | Review: Cautious Optimism | 71.7% (3308/4611; 95% CI 70.3%-73.1%) | 2021-2025 | final/data/pubtype_stance.csv |
| RES-FMT-REVIEW-ADVOCACY | Review: Advocacy | 1.9% (87/4611; 95% CI 1.5%-2.3%) | 2021-2025 | final/data/pubtype_stance.csv |
| RES-FMT-REVIEW-CRITICAL | Review: Critical | 24.3% (1120/4611; 95% CI 23.1%-25.5%) | 2021-2025 | final/data/pubtype_stance.csv |
| RES-FMT-REVIEW-FAVOURABLE | Review: Favourable | 73.6% (3395/4611; 95% CI 72.3%-75.0%) | 2021-2025 | final/data/pubtype_stance.csv |
| RES-FMT-REVIEW-AMP | Review: adjusted average marginal probability of critical stance (B4) | 21.5% (95% CI 19.6%-23.6%) | 2021-2025 | outputs/B4/B4_primary_critical_AMP.csv |
| RES-FMT-REVIEW-AOR | Review vs Research Article: adjusted OR for critical stance (B4) | OR 0.47 (95% CI 0.41-0.54), P<.001 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv |
| RES-FMT-LETTER-ALARM | Letter: Alarm | 7.0% (30/429; 95% CI 4.7%-9.3%) | 2021-2025 | final/data/pubtype_stance.csv |
| RES-FMT-LETTER-CAUTION | Letter: Caution | 33.6% (144/429; 95% CI 29.1%-38.7%) | 2021-2025 | final/data/pubtype_stance.csv |
| RES-FMT-LETTER-NEUTRAL | Letter: Neutral | 21.7% (93/429; 95% CI 17.7%-25.4%) | 2021-2025 | final/data/pubtype_stance.csv |
| RES-FMT-LETTER-CAUTIOUSOPTIMISM | Letter: Cautious Optimism | 31.2% (134/429; 95% CI 26.6%-35.9%) | 2021-2025 | final/data/pubtype_stance.csv |
| RES-FMT-LETTER-ADVOCACY | Letter: Advocacy | 6.5% (28/429; 95% CI 4.4%-8.9%) | 2021-2025 | final/data/pubtype_stance.csv |
| RES-FMT-LETTER-CRITICAL | Letter: Critical | 40.6% (174/429; 95% CI 36.1%-45.5%) | 2021-2025 | final/data/pubtype_stance.csv |
| RES-FMT-LETTER-FAVOURABLE | Letter: Favourable | 37.8% (162/429; 95% CI 33.1%-42.4%) | 2021-2025 | final/data/pubtype_stance.csv |
| RES-FMT-LETTER-AMP | Letter: adjusted average marginal probability of critical stance (B4) | 38.6% (95% CI 33.5%-43.8%) | 2021-2025 | outputs/B4/B4_primary_critical_AMP.csv |
| RES-FMT-LETTER-AOR | Letter vs Research Article: adjusted OR for critical stance (B4) | OR 1.16 (95% CI 0.90-1.51), P=.249 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv |
| RES-FMT-EDITORIAL-ALARM | Editorial: Alarm | 2.7% (10/364; 95% CI 1.1%-4.4%) | 2021-2025 | final/data/pubtype_stance.csv |
| RES-FMT-EDITORIAL-CAUTION | Editorial: Caution | 34.3% (125/364; 95% CI 29.7%-39.3%) | 2021-2025 | final/data/pubtype_stance.csv |
| RES-FMT-EDITORIAL-NEUTRAL | Editorial: Neutral | 9.6% (35/364; 95% CI 6.6%-12.6%) | 2021-2025 | final/data/pubtype_stance.csv |
| RES-FMT-EDITORIAL-CAUTIOUSOPTIMISM | Editorial: Cautious Optimism | 46.4% (169/364; 95% CI 41.2%-51.6%) | 2021-2025 | final/data/pubtype_stance.csv |
| RES-FMT-EDITORIAL-ADVOCACY | Editorial: Advocacy | 6.9% (25/364; 95% CI 4.4%-9.6%) | 2021-2025 | final/data/pubtype_stance.csv |
| RES-FMT-EDITORIAL-CRITICAL | Editorial: Critical | 37.1% (135/364; 95% CI 32.1%-42.0%) | 2021-2025 | final/data/pubtype_stance.csv |
| RES-FMT-EDITORIAL-FAVOURABLE | Editorial: Favourable | 53.3% (194/364; 95% CI 48.4%-58.5%) | 2021-2025 | final/data/pubtype_stance.csv |
| RES-FMT-EDITORIAL-AMP | Editorial: adjusted average marginal probability of critical stance (B4) | 29.2% (95% CI 24.8%-34.0%) | 2021-2025 | outputs/B4/B4_primary_critical_AMP.csv |
| RES-FMT-EDITORIAL-AOR | Editorial vs Research Article: adjusted OR for critical stance (B4) | OR 0.73 (95% CI 0.56-0.95), P=.018 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv |
| RES-FMT-COMMENTARY-ALARM | Commentary: Alarm | 9.2% (9/98; 95% CI 4.1%-15.3%) | 2021-2025 | final/data/pubtype_stance.csv |
| RES-FMT-COMMENTARY-CAUTION | Commentary: Caution | 46.9% (46/98; 95% CI 37.8%-57.1%) | 2021-2025 | final/data/pubtype_stance.csv |
| RES-FMT-COMMENTARY-NEUTRAL | Commentary: Neutral | 6.1% (6/98; 95% CI 2.0%-11.2%) | 2021-2025 | final/data/pubtype_stance.csv |
| RES-FMT-COMMENTARY-CAUTIOUSOPTIMISM | Commentary: Cautious Optimism | 35.7% (35/98; 95% CI 26.5%-45.9%) | 2021-2025 | final/data/pubtype_stance.csv |
| RES-FMT-COMMENTARY-ADVOCACY | Commentary: Advocacy | 2.0% (2/98; 95% CI 0.0%-5.1%) | 2021-2025 | final/data/pubtype_stance.csv |
| RES-FMT-COMMENTARY-CRITICAL | Commentary: Critical | 56.1% (55/98; 95% CI 45.9%-66.3%) | 2021-2025 | final/data/pubtype_stance.csv |
| RES-FMT-COMMENTARY-FAVOURABLE | Commentary: Favourable | 37.8% (37/98; 95% CI 28.6%-48.0%) | 2021-2025 | final/data/pubtype_stance.csv |
| RES-FMT-COMMENTARY-AMP | Commentary: adjusted average marginal probability of critical stance (B4) | 48.0% (95% CI 35.2%-61.2%) | 2021-2025 | outputs/B4/B4_primary_critical_AMP.csv |
| RES-FMT-COMMENTARY-AOR | Commentary vs Research Article: adjusted OR for critical stance (B4) | OR 1.79 (95% CI 0.98-3.26), P=.056 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv |
| RES-FMT-OPINION-CRIT | Opinion formats pooled (Commentary, Letter, Editorial): critical | 40.9% (364/891; 95% CI 37.7%-44.1%) | 2021-2025 | outputs/T5_crosssectional_both_windows.csv |
| RES-FMT-CHISQ | Opinion formats vs Research Articles, five-category stance distribution | χ²=376.1, df=4, P<.001, Cramér V=0.200; N=9447 | 2021-2025 | outputs/T5_crosssectional_both_windows.csv |
| RES-FMT-RSUB-SYSTEMATICREVIEW-CRITICAL | Systematic Review: Critical | 29.5% (245/831; 95% CI 26.2%-32.7%) | 2021-2025 | final/data/review_subtypes.csv |
| RES-FMT-RSUB-SYSTEMATICREVIEW-ALARM | Systematic Review: Alarm | 3.4% (28/831; 95% CI 2.2%-4.7%) | 2021-2025 | final/data/review_subtypes.csv |
| RES-FMT-RSUB-SYSTEMATICREVIEW-CAUTION | Systematic Review: Caution | 26.1% (217/831; 95% CI 23.0%-29.2%) | 2021-2025 | final/data/review_subtypes.csv |
| RES-FMT-RSUB-SYSTEMATICREVIEW-NEUTRAL | Systematic Review: Neutral | 2.4% (20/831; 95% CI 1.6%-3.6%) | 2021-2025 | final/data/review_subtypes.csv |
| RES-FMT-RSUB-SYSTEMATICREVIEW-CAUTIOUSOPTIMISM | Systematic Review: Cautious Optimism | 67.7% (563/831; 95% CI 64.3%-71.0%) | 2021-2025 | final/data/review_subtypes.csv |
| RES-FMT-RSUB-SYSTEMATICREVIEW-ADVOCACY | Systematic Review: Advocacy | 0.4% (3/831; 95% CI 0.0%-0.8%) | 2021-2025 | final/data/review_subtypes.csv |
| RES-FMT-RSUB-SYSTEMATICREVIEW-FAVOURABLE | Systematic Review: Favourable | 68.1% (566/831; 95% CI 64.7%-71.4%) | 2021-2025 | final/data/review_subtypes.csv |
| RES-FMT-RSUB-REVIEWNARRATIVE-CRITICAL | Review (narrative): Critical | 23.1% (875/3780; 95% CI 21.7%-24.5%) | 2021-2025 | final/data/review_subtypes.csv |
| RES-FMT-RSUB-REVIEWNARRATIVE-ALARM | Review (narrative): Alarm | 0.7% (25/3780; 95% CI 0.4%-0.9%) | 2021-2025 | final/data/review_subtypes.csv |
| RES-FMT-RSUB-REVIEWNARRATIVE-CAUTION | Review (narrative): Caution | 22.5% (850/3780; 95% CI 21.1%-23.8%) | 2021-2025 | final/data/review_subtypes.csv |
| RES-FMT-RSUB-REVIEWNARRATIVE-NEUTRAL | Review (narrative): Neutral | 2.0% (76/3780; 95% CI 1.6%-2.5%) | 2021-2025 | final/data/review_subtypes.csv |
| RES-FMT-RSUB-REVIEWNARRATIVE-CAUTIOUSOPTIMISM | Review (narrative): Cautious Optimism | 72.6% (2745/3780; 95% CI 71.3%-74.0%) | 2021-2025 | final/data/review_subtypes.csv |
| RES-FMT-RSUB-REVIEWNARRATIVE-ADVOCACY | Review (narrative): Advocacy | 2.2% (84/3780; 95% CI 1.7%-2.7%) | 2021-2025 | final/data/review_subtypes.csv |
| RES-FMT-RSUB-REVIEWNARRATIVE-FAVOURABLE | Review (narrative): Favourable | 74.8% (2829/3780; 95% CI 73.5%-76.3%) | 2021-2025 | final/data/review_subtypes.csv |
| RES-FMT-RSUB-RULE | Review subtype rule | PubMed Publication Type substring precedence (analysis/robustness.py::simplify_pubtype_7): Editorial > Letter > Systematic Review > Review > Comment > News > Research Article. 'Systematic Review' tag = systematic subtype; any other 'Review' tag (including Scoping Review) = narrative subtype; Meta-Analysis has no rule of its own. | 2021-2025 | outputs/T8_review_subtype.md |
| RES-FMT-THEME-GOVERNANCEREGULATION | Governance / regulation among critical records: Reviews vs Research Articles | Reviews 56.9% (637/1120; 95% CI 54.0%-59.7%) vs Research Articles 28.3% (792/2799; 95% CI 26.6%-29.8%); difference +28.6 percentage points | 2021-2025 | final/data/theme_by_format.csv |
| RES-FMT-THEME-ETHICSANDBIAS | Ethics & bias among critical records: Reviews vs Research Articles | Reviews 44.6% (500/1120; 95% CI 41.7%-47.7%) vs Research Articles 30.5% (854/2799; 95% CI 28.9%-32.3%); difference +14.1 percentage points | 2021-2025 | final/data/theme_by_format.csv |
| RES-FMT-THEME-DATAPRIVACY | Data privacy among critical records: Reviews vs Research Articles | Reviews 11.4% (128/1120; 95% CI 9.6%-13.2%) vs Research Articles 6.3% (176/2799; 95% CI 5.4%-7.2%); difference +5.1 percentage points | 2021-2025 | final/data/theme_by_format.csv |
| RES-FMT-THEME-OTHER | Other among critical records: Reviews vs Research Articles | Reviews 3.0% (34/1120; 95% CI 2.1%-4.1%) vs Research Articles 1.9% (54/2799; 95% CI 1.4%-2.5%); difference +1.1 percentage points | 2021-2025 | final/data/theme_by_format.csv |
| RES-FMT-THEME-PATIENTSAFETY | Patient safety among critical records: Reviews vs Research Articles | Reviews 64.6% (723/1120; 95% CI 61.7%-67.4%) vs Research Articles 63.6% (1781/2799; 95% CI 61.8%-65.5%); difference +0.9 percentage points | 2021-2025 | final/data/theme_by_format.csv |
| RES-FMT-THEME-REPLACEMENTFEARS | Replacement fears among critical records: Reviews vs Research Articles | Reviews 2.9% (32/1120; 95% CI 1.9%-3.8%) vs Research Articles 3.9% (109/2799; 95% CI 3.2%-4.6%); difference -1.0 percentage points | 2021-2025 | final/data/theme_by_format.csv |
| RES-FMT-THEME-EXISTENTIALTHREAT | Existential threat among critical records: Reviews vs Research Articles | Reviews 3.8% (43/1120; 95% CI 2.8%-5.0%) vs Research Articles 5.0% (140/2799; 95% CI 4.2%-5.8%); difference -1.2 percentage points | 2021-2025 | final/data/theme_by_format.csv |
| RES-FMT-THEME-COGNITIVEOFFLOADING | Cognitive offloading among critical records: Reviews vs Research Articles | Reviews 4.3% (48/1120; 95% CI 3.0%-5.4%) vs Research Articles 6.4% (179/2799; 95% CI 5.5%-7.3%); difference -2.1 percentage points | 2021-2025 | final/data/theme_by_format.csv |
| RES-FMT-THEME-MEDICALEDUCATION | Medical education among critical records: Reviews vs Research Articles | Reviews 5.4% (61/1120; 95% CI 4.1%-6.9%) vs Research Articles 10.1% (284/2799; 95% CI 9.0%-11.2%); difference -4.7 percentage points | 2021-2025 | final/data/theme_by_format.csv |
| RES-FMT-THEME-HALLUCINATIONERRORS | Hallucination / errors among critical records: Reviews vs Research Articles | Reviews 29.2% (327/1120; 95% CI 26.6%-32.1%) vs Research Articles 52.6% (1473/2799; 95% CI 50.7%-54.7%); difference -23.4 percentage points | 2021-2025 | final/data/theme_by_format.csv |

### 7. Advocacy by specialty, 2021 vs 2025

| ID | Item | Value | Window | Source |
|---|---|---|---|---|
| RES-ADVSP-TOTAL-2021 | Advocacy records, 2021 | 31 | 2021-2025 | final/data/advocacy_by_specialty.csv |
| RES-ADVSP-TOTAL-2025 | Advocacy records, 2025 | 66 | 2021-2025 | final/data/advocacy_by_specialty.csv |
| RES-ADVSP-RADIOLOGYDIAGNOSTICIMAGI | Radiology / Diagnostic Imaging: Advocacy records (share of all Advocacy; rate within specialty) | 2021: 2 (6.5% of 31; 1.1% of 181); 2025: 2 (3.0% of 66; 0.3% of 596) | 2021-2025 | final/data/advocacy_by_specialty.csv |
| RES-ADVSP-PATHOLOGYLABORATORYMEDIC | Pathology / Laboratory Medicine: Advocacy records (share of all Advocacy; rate within specialty) | 2021: 1 (3.2% of 31; 2.3% of 44); 2025: 0 (0.0% of 66; 0.0% of 137) | 2021-2025 | final/data/advocacy_by_specialty.csv |
| RES-ADVSP-CARDIOLOGY | Cardiology: Advocacy records (share of all Advocacy; rate within specialty) | 2021: 1 (3.2% of 31; 2.0% of 49); 2025: 3 (4.5% of 66; 1.5% of 200) | 2021-2025 | final/data/advocacy_by_specialty.csv |
| RES-ADVSP-ONCOLOGY | Oncology: Advocacy records (share of all Advocacy; rate within specialty) | 2021: 5 (16.1% of 31; 4.7% of 106); 2025: 6 (9.1% of 66; 1.2% of 489) | 2021-2025 | final/data/advocacy_by_specialty.csv |
| RES-ADVSP-SURGERY | Surgery: Advocacy records (share of all Advocacy; rate within specialty) | 2021: 1 (3.2% of 31; 1.8% of 56); 2025: 9 (13.6% of 66; 1.8% of 512) | 2021-2025 | final/data/advocacy_by_specialty.csv |
| RES-ADVSP-OPHTHALMOLOGY | Ophthalmology: Advocacy records (share of all Advocacy; rate within specialty) | 2021: 1 (3.2% of 31; 1.5% of 65); 2025: 0 (0.0% of 66; 0.0% of 229) | 2021-2025 | final/data/advocacy_by_specialty.csv |
| RES-ADVSP-DERMATOLOGY | Dermatology: Advocacy records (share of all Advocacy; rate within specialty) | 2021: 2 (6.5% of 31; 6.9% of 29); 2025: 1 (1.5% of 66; 1.1% of 94) | 2021-2025 | final/data/advocacy_by_specialty.csv |
| RES-ADVSP-NEUROLOGYNEUROSCIENCE | Neurology / Neuroscience: Advocacy records (share of all Advocacy; rate within specialty) | 2021: 2 (6.5% of 31; 10.5% of 19); 2025: 3 (4.5% of 66; 2.6% of 117) | 2021-2025 | final/data/advocacy_by_specialty.csv |
| RES-ADVSP-MENTALHEALTHPSYCHIATRY | Mental Health / Psychiatry: Advocacy records (share of all Advocacy; rate within specialty) | 2021: 0 (0.0% of 31; 0.0% of 25); 2025: 0 (0.0% of 66; 0.0% of 198) | 2021-2025 | final/data/advocacy_by_specialty.csv |
| RES-ADVSP-INTERNALMEDICINEPRIMARYC | Internal Medicine / Primary Care: Advocacy records (share of all Advocacy; rate within specialty) | 2021: 0 (0.0% of 31; 0.0% of 86); 2025: 6 (9.1% of 66; 1.6% of 384) | 2021-2025 | final/data/advocacy_by_specialty.csv |
| RES-ADVSP-EMERGENCYMEDICINECRITICA | Emergency Medicine / Critical Care: Advocacy records (share of all Advocacy; rate within specialty) | 2021: 0 (0.0% of 31; 0.0% of 16); 2025: 1 (1.5% of 66; 0.7% of 140) | 2021-2025 | final/data/advocacy_by_specialty.csv |
| RES-ADVSP-PEDIATRICS | Pediatrics: Advocacy records (share of all Advocacy; rate within specialty) | 2021: 0 (0.0% of 31; 0.0% of 11); 2025: 1 (1.5% of 66; 0.6% of 154) | 2021-2025 | final/data/advocacy_by_specialty.csv |
| RES-ADVSP-OBSTETRICSGYNECOLOGY | Obstetrics / Gynecology: Advocacy records (share of all Advocacy; rate within specialty) | 2021: 1 (3.2% of 31; 9.1% of 11); 2025: 0 (0.0% of 66; 0.0% of 94) | 2021-2025 | final/data/advocacy_by_specialty.csv |
| RES-ADVSP-DENTISTRY | Dentistry: Advocacy records (share of all Advocacy; rate within specialty) | 2021: 0 (0.0% of 31; 0.0% of 27); 2025: 1 (1.5% of 66; 0.3% of 330) | 2021-2025 | final/data/advocacy_by_specialty.csv |
| RES-ADVSP-MEDICALINFORMATICSDIGITA | Medical Informatics / Digital Health: Advocacy records (share of all Advocacy; rate within specialty) | 2021: 12 (38.7% of 31; 4.1% of 293); 2025: 28 (42.4% of 66; 1.8% of 1517) | 2021-2025 | final/data/advocacy_by_specialty.csv |
| RES-ADVSP-NURSING | Nursing: Advocacy records (share of all Advocacy; rate within specialty) | 2021: 1 (3.2% of 31; 20.0% of 5); 2025: 0 (0.0% of 66; 0.0% of 145) | 2021-2025 | final/data/advocacy_by_specialty.csv |
| RES-ADVSP-MEDICALEDUCATION | Medical Education: Advocacy records (share of all Advocacy; rate within specialty) | 2021: 2 (6.5% of 31; 7.4% of 27); 2025: 5 (7.6% of 66; 1.1% of 472) | 2021-2025 | final/data/advocacy_by_specialty.csv |
| RES-ADVSP-MULTIDISCIPLINARYOTHER | Multidisciplinary / Other: Advocacy records (share of all Advocacy; rate within specialty) | 2021: 0 (0.0% of 31; 0.0% of 13); 2025: 0 (0.0% of 66; 0.0% of 85) | 2021-2025 | final/data/advocacy_by_specialty.csv |
| RES-ADVSP-FAILED | FAILED: Advocacy records (share of all Advocacy; rate within specialty) | 2021: 0 (0.0% of 31; nan% of 0); 2025: 0 (0.0% of 66; 0.0% of 5) | 2021-2025 | final/data/advocacy_by_specialty.csv |

### 8. Sensitivity analyses

| ID | Item | Value | Window | Source |
|---|---|---|---|---|
| RES-SEN-B2-FRAME | B2 recovered frame: production application, full-abstract discourse or evaluative (all years) | 2850 | all years | outputs/B2/B2_analysis.md |
| RES-SEN-B2-FAILED | B2 recovered records with stance FAILED after one resubmission | 3 | all years | outputs/B2/B2_analysis.md |
| RES-SEN-B2-RECOVERED | B2 recovered records with a valid stance, dated 2021-2025 (added in corpus b) | 2453 | 2021-2025 | outputs/B2/B2_analysis.md |
| RES-SEN-B2-DROPPED | B2 corpus d: production records 2021-2025 dropped because the full-abstract label is application | 1587 | 2021-2025 | outputs/B2/B2_analysis.md |
| RES-SEN-B2A-ADVOCACY | B2 corpus (a) Production: Advocacy | 2.9% (2021) to 1.1% (2025); ρ=-1.00 (P=.017); OR 0.793 per year (95% CI 0.721-0.872), P<.001 | 2021-2025 | outputs/B2/B2_trend_movement.csv |
| RES-SEN-B2B-ADVOCACY | B2 corpus (b) Augmented: Advocacy | 2.5% (2021) to 1.2% (2025); ρ=-0.90 (P=.083); OR 0.840 per year (95% CI 0.767-0.920), P<.001 | 2021-2025 | outputs/B2/B2_trend_movement.csv |
| RES-SEN-B2C-ADVOCACY | B2 corpus (c) Precision-weighted augmented: Advocacy | 2.6% (2021) to 1.2% (2025); ρ=-0.90 (P=.083); OR 0.832 per year (95% CI 0.759-0.911), P<.001 | 2021-2025 | outputs/B2/B2_trend_movement.csv |
| RES-SEN-B2D-ADVOCACY | B2 corpus (d) Full-abstract corpus: Advocacy | 2.6% (2021) to 1.0% (2025); ρ=-0.90 (P=.083); OR 0.799 per year (95% CI 0.725-0.880), P<.001 | 2021-2025 | outputs/B2/B2_trend_movement.csv |
| RES-SEN-B2A-CRITICAL | B2 corpus (a) Production: Critical | 25.4% (2021) to 31.0% (2025); ρ=+0.80 (P=.133); OR 1.077 per year (95% CI 1.046-1.108), P<.001 | 2021-2025 | outputs/B2/B2_trend_movement.csv |
| RES-SEN-B2B-CRITICAL | B2 corpus (b) Augmented: Critical | 22.0% (2021) to 28.6% (2025); ρ=+0.90 (P=.083); OR 1.092 per year (95% CI 1.063-1.122), P<.001 | 2021-2025 | outputs/B2/B2_trend_movement.csv |
| RES-SEN-B2C-CRITICAL | B2 corpus (c) Precision-weighted augmented: Critical | 22.7% (2021) to 28.7% (2025); ρ=+0.80 (P=.133); OR 1.082 per year (95% CI 1.053-1.111), P<.001 | 2021-2025 | outputs/B2/B2_trend_movement.csv |
| RES-SEN-B2D-CRITICAL | B2 corpus (d) Full-abstract corpus: Critical | 24.0% (2021) to 30.7% (2025); ρ=+0.90 (P=.083); OR 1.089 per year (95% CI 1.059-1.120), P<.001 | 2021-2025 | outputs/B2/B2_trend_movement.csv |
| RES-SEN-B3-CONS-ADVOCACY | B3: production Advocacy records flagged strong endorsement, 2021-2025 | 38.1% (83/218; 95% CI 31.6%-44.9%) | 2021-2025 | outputs/B3/B3_consistency.csv |
| RES-SEN-B3-CONS-CAUTIOUSOPTIMISM | B3: production Cautious Optimism records flagged strong endorsement, 2021-2025 | 12.4% (1096/8836; 95% CI 11.7%-13.1%) | 2021-2025 | outputs/B3/B3_consistency.csv |
| RES-SEN-B3-CORR-2021 | B3: misclassification-corrected human-Advocacy prevalence, 2021 | 6.99% (95% CI 3.02%-11.79%) | 2021-2025 | outputs/B3/B3_corrected_prevalence.csv |
| RES-SEN-B3-CORR-2022 | B3: misclassification-corrected human-Advocacy prevalence, 2022 | 6.95% (95% CI 2.71%-12.70%) | 2021-2025 | outputs/B3/B3_corrected_prevalence.csv |
| RES-SEN-B3-CORR-2023 | B3: misclassification-corrected human-Advocacy prevalence, 2023 | 6.20% (95% CI 2.63%-10.54%) | 2021-2025 | outputs/B3/B3_corrected_prevalence.csv |
| RES-SEN-B3-CORR-2024 | B3: misclassification-corrected human-Advocacy prevalence, 2024 | 5.62% (95% CI 2.39%-9.60%) | 2021-2025 | outputs/B3/B3_corrected_prevalence.csv |
| RES-SEN-B3-CORR-2025 | B3: misclassification-corrected human-Advocacy prevalence, 2025 | 5.52% (95% CI 2.36%-9.26%) | 2021-2025 | outputs/B3/B3_corrected_prevalence.csv |
| RES-SEN-B5D1-CRITICAL | B5 D1 Medicine area (primary): Critical trend | ρ=+0.70 (P=.233); OR 1.066 per year (95% CI 1.034-1.100), P<.001 | 2021-2025 | outputs/B5/B5_long.csv |
| RES-SEN-B5D1-ADVOCACY | B5 D1 Medicine area (primary): Advocacy trend | ρ=-0.90 (P=.083); OR 0.771 per year (95% CI 0.690-0.862), P<.001 | 2021-2025 | outputs/B5/B5_long.csv |
| RES-SEN-B5D1-PATIENTSAFETY | B5 D1 Medicine area (primary): Patient safety trend | 59.1% to 66.7% (change +7.6 percentage points); ρ=+0.90 (P=.083); OR 1.080 per year (95% CI 1.021-1.143) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-SEN-B5D1-HALLUCINATIONERRORS | B5 D1 Medicine area (primary): Hallucination / errors trend | 23.0% to 50.7% (change +27.7 percentage points); ρ=+0.80 (P=.133); OR 1.386 per year (95% CI 1.308-1.470) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-SEN-B5D1-GOVERNANCEREGULATION | B5 D1 Medicine area (primary): Governance / regulation trend | 55.2% to 33.3% (change -21.9 percentage points); ρ=-0.90 (P=.083); OR 0.772 per year (95% CI 0.731-0.817) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-SEN-B5D1-ETHICSANDBIAS | B5 D1 Medicine area (primary): Ethics & bias trend | 37.0% to 33.1% (change -3.8 percentage points); ρ=-0.80 (P=.133); OR 0.912 per year (95% CI 0.863-0.965) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-SEN-B5D1-SPC-RANGEN30CATEGORIES | B5 D1 Medicine area (primary): specialty range (n≥30 categories) | Mental Health / Psychiatry 49.6% (167/337) to Cardiology 16.4% (82/500) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-SEN-B5D1-SPC-FDASPEARMAN | B5 D1 Medicine area (primary): specialty FDA Spearman ρ | -0.61 (two-sided P=.007, n=18) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-SEN-B5D1-REG-EASTASIA | B5 D1 Medicine area (primary): East Asia critical | 17.6% (389/2207; 95% CI 16.0%-19.2%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-SEN-B5D1-REG-NORTHAMERICA | B5 D1 Medicine area (primary): North America critical | 34.9% (1302/3727; 95% CI 33.4%-36.4%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-SEN-B5D1-PT-REVIEW | B5 D1 Medicine area (primary): Review critical | 25.0% (969/3873; 95% CI 23.6%-26.3%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-SEN-B5D1-PT-RESEARCHARTICLE | B5 D1 Medicine area (primary): Research Article critical | 32.9% (2321/7065; 95% CI 31.7%-33.9%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-SEN-B5D1-REMOVED | B5 D1 Medicine area (primary): records removed, 2021-2025 | 2325 of 14,058 | 2021-2025 | outputs/B5/B5_sjr_sensitivity.md |
| RES-SEN-B5D2-CRITICAL | B5 D2 D1 minus Medicine (misc.): Critical trend | ρ=+0.90 (P=.083); OR 1.085 per year (95% CI 1.049-1.122), P<.001 | 2021-2025 | outputs/B5/B5_long.csv |
| RES-SEN-B5D2-ADVOCACY | B5 D2 D1 minus Medicine (misc.): Advocacy trend | ρ=-0.90 (P=.083); OR 0.802 per year (95% CI 0.707-0.909), P<.001 | 2021-2025 | outputs/B5/B5_long.csv |
| RES-SEN-B5D2-PATIENTSAFETY | B5 D2 D1 minus Medicine (misc.): Patient safety trend | 60.4% to 69.1% (change +8.7 percentage points); ρ=+0.90 (P=.083); OR 1.107 per year (95% CI 1.042-1.177) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-SEN-B5D2-HALLUCINATIONERRORS | B5 D2 D1 minus Medicine (misc.): Hallucination / errors trend | 25.4% to 51.2% (change +25.8 percentage points); ρ=+0.80 (P=.133); OR 1.358 per year (95% CI 1.276-1.444) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-SEN-B5D2-GOVERNANCEREGULATION | B5 D2 D1 minus Medicine (misc.): Governance / regulation trend | 55.3% to 34.0% (change -21.3 percentage points); ρ=-0.90 (P=.083); OR 0.779 per year (95% CI 0.734-0.827) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-SEN-B5D2-ETHICSANDBIAS | B5 D2 D1 minus Medicine (misc.): Ethics & bias trend | 35.5% to 34.0% (change -1.5 percentage points); ρ=-0.60 (P=.350); OR 0.938 per year (95% CI 0.883-0.996) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-SEN-B5D2-SPC-RANGEN30CATEGORIES | B5 D2 D1 minus Medicine (misc.): specialty range (n≥30 categories) | Mental Health / Psychiatry 49.5% (153/309) to Cardiology 16.4% (73/445) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-SEN-B5D2-SPC-FDASPEARMAN | B5 D2 D1 minus Medicine (misc.): specialty FDA Spearman ρ | -0.60 (two-sided P=.008, n=18) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-SEN-B5D2-REG-EASTASIA | B5 D2 D1 minus Medicine (misc.): East Asia critical | 18.4% (348/1896; 95% CI 16.7%-20.1%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-SEN-B5D2-REG-NORTHAMERICA | B5 D2 D1 minus Medicine (misc.): North America critical | 34.9% (1170/3348; 95% CI 33.3%-36.5%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-SEN-B5D2-PT-REVIEW | B5 D2 D1 minus Medicine (misc.): Review critical | 26.0% (872/3352; 95% CI 24.6%-27.4%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-SEN-B5D2-PT-RESEARCHARTICLE | B5 D2 D1 minus Medicine (misc.): Research Article critical | 32.5% (1995/6133; 95% CI 31.4%-33.7%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-SEN-B5D2-REMOVED | B5 D2 D1 minus Medicine (misc.): records removed, 2021-2025 | 3878 of 14,058 | 2021-2025 | outputs/B5/B5_sjr_sensitivity.md |
| RES-SEN-B5D3-CRITICAL | B5 D3 broad health sciences: Critical trend | ρ=+0.90 (P=.083); OR 1.071 per year (95% CI 1.039-1.104), P<.001 | 2021-2025 | outputs/B5/B5_long.csv |
| RES-SEN-B5D3-ADVOCACY | B5 D3 broad health sciences: Advocacy trend | ρ=-0.90 (P=.083); OR 0.782 per year (95% CI 0.706-0.867), P<.001 | 2021-2025 | outputs/B5/B5_long.csv |
| RES-SEN-B5D3-PATIENTSAFETY | B5 D3 broad health sciences: Patient safety trend | 59.0% to 65.5% (change +6.5 percentage points); ρ=+0.90 (P=.083); OR 1.066 per year (95% CI 1.010-1.126) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-SEN-B5D3-HALLUCINATIONERRORS | B5 D3 broad health sciences: Hallucination / errors trend | 23.4% to 51.4% (change +28.1 percentage points); ρ=+0.80 (P=.133); OR 1.391 per year (95% CI 1.315-1.472) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-SEN-B5D3-GOVERNANCEREGULATION | B5 D3 broad health sciences: Governance / regulation trend | 54.5% to 31.7% (change -22.8 percentage points); ρ=-0.90 (P=.083); OR 0.762 per year (95% CI 0.722-0.805) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-SEN-B5D3-ETHICSANDBIAS | B5 D3 broad health sciences: Ethics & bias trend | 37.7% to 33.1% (change -4.6 percentage points); ρ=-0.80 (P=.133); OR 0.905 per year (95% CI 0.858-0.956) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-SEN-B5D3-SPC-RANGEN30CATEGORIES | B5 D3 broad health sciences: specialty range (n≥30 categories) | Mental Health / Psychiatry 50.0% (184/368) to Cardiology 16.3% (82/504) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-SEN-B5D3-SPC-FDASPEARMAN | B5 D3 broad health sciences: specialty FDA Spearman ρ | -0.63 (two-sided P=.005, n=18) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-SEN-B5D3-REG-EASTASIA | B5 D3 broad health sciences: East Asia critical | 18.0% (428/2372; 95% CI 16.5%-19.7%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-SEN-B5D3-REG-NORTHAMERICA | B5 D3 broad health sciences: North America critical | 35.0% (1375/3926; 95% CI 33.6%-36.5%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-SEN-B5D3-PT-REVIEW | B5 D3 broad health sciences: Review critical | 24.7% (1048/4239; 95% CI 23.4%-26.1%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-SEN-B5D3-PT-RESEARCHARTICLE | B5 D3 broad health sciences: Research Article critical | 33.2% (2541/7649; 95% CI 32.2%-34.3%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-SEN-B5D3-REMOVED | B5 D3 broad health sciences: records removed, 2021-2025 | 1347 of 14,058 | 2021-2025 | outputs/B5/B5_sjr_sensitivity.md |
| RES-SEN-B4S3-YEAR | B4 S3 journal fixed effects: critical OR per year | OR 1.082 per year (95% CI 1.030-1.137), P=.002 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-SEN-B4S4-YEAR | B4 S4 country instead of region: critical OR per year | OR 1.110 per year (95% CI 1.073-1.149), P<.001 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-SEN-B4S2-2022 | B4 S2 (adds January-April 2026): critical OR, 2022 vs 2021 | OR 1.00 (95% CI 0.82-1.21), P=.978 | 2021-April 2026 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-SEN-B4S2-2023 | B4 S2 (adds January-April 2026): critical OR, 2023 vs 2021 | OR 1.30 (95% CI 1.09-1.55), P=.004 | 2021-April 2026 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-SEN-B4S2-2024 | B4 S2 (adds January-April 2026): critical OR, 2024 vs 2021 | OR 1.53 (95% CI 1.30-1.80), P<.001 | 2021-April 2026 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-SEN-B4S2-2025 | B4 S2 (adds January-April 2026): critical OR, 2025 vs 2021 | OR 1.44 (95% CI 1.23-1.69), P<.001 | 2021-April 2026 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-SEN-B4S2-2026 | B4 S2 (adds January-April 2026): critical OR, 2026 vs 2021 | OR 1.61 (95% CI 1.35-1.92), P<.001 | 2021-April 2026 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-SEN-B4S3-N | B4 S3 sample | n=8529 records, 2728 events, 275 journals | 2021-2025 | outputs/B4/B4_regression.md |
| RES-SEN-B4-PO | B4 ordinal model: proportional-odds assumption | fails for 27 of 32 terms (pre-specified rule), mainly at the Advocacy cut point | 2021-2025 | outputs/B4/B4_regression.md |

### 9. Forward-validation (Multimedia Appendix 2; unchanged)

| ID | Item | Value | Window | Source |
|---|---|---|---|---|
| RES-FV-CAND | Advocacy records 2021-2023 with a predictive-claim flag | 92 | 2021-2023 claims; 2024-April 2026 evidence | output/analyses/prophecy/prophecy_panel_candidates_2021_2023.csv |
| RES-FV-FP | False positives removed by blind human review | 18 | 2021-2023 claims | output/analyses/prophecy/phase1_signature_claims_FROZEN.csv |
| RES-FV-PREC | Post-hoc flag precision | 0.80 (74/92) | 2021-2023 claims | output/analyses/prophecy/ |
| RES-FV-SET | Frozen set | 74 papers, 78 claims (Tier 1 7; Tier 2 36; Tier 3 35) | 2021-2023 claims | output/analyses/prophecy/phase2_prophecy_verdicts_worksheet.xlsx |
| RES-FV-BORNEOUT | Claims borne out | 2/78 (2.6%) | evidence 2024-April 2026 | output/analyses/prophecy/phase2_prophecy_verdicts_worksheet.xlsx |
| RES-FV-PARTIALLY | Claims partially borne out | 54/78 (69.2%) | evidence 2024-April 2026 | output/analyses/prophecy/phase2_prophecy_verdicts_worksheet.xlsx |
| RES-FV-NOTBORNEOUT | Claims not borne out | 8/78 (10.3%) | evidence 2024-April 2026 | output/analyses/prophecy/phase2_prophecy_verdicts_worksheet.xlsx |
| RES-FV-TOOEARLYUNFALSIFIABLE | Claims too early/unfalsifiable | 14/78 (17.9%) | evidence 2024-April 2026 | output/analyses/prophecy/phase2_prophecy_verdicts_worksheet.xlsx |
| RES-FV-TIER1 | Tier 1 verdicts | borne out 0; partially 1; not borne out 5; too early/unfalsifiable 1 (n=7) | evidence 2024-April 2026 | final/data/fv_tier_verdict.csv |
| RES-FV-TIER2 | Tier 2 verdicts | borne out 2; partially 23; not borne out 1; too early/unfalsifiable 10 (n=36) | evidence 2024-April 2026 | final/data/fv_tier_verdict.csv |
| RES-FV-TIER3 | Tier 3 verdicts | borne out 0; partially 30; not borne out 2; too early/unfalsifiable 3 (n=35) | evidence 2024-April 2026 | final/data/fv_tier_verdict.csv |

### 10. January-April 2026 (descriptive only; no trend statistics)

| ID | Item | Value | Window | Source |
|---|---|---|---|---|
| RES-2026-ALARM | Alarm, January-April 2026 | 6.2% (167/2689; 95% CI 5.2%-7.1%) | January-April 2026 | outputs/T4_2026_descriptive.csv |
| RES-2026-CAUTION | Caution, January-April 2026 | 26.4% (711/2689; 95% CI 24.8%-28.1%) | January-April 2026 | outputs/T4_2026_descriptive.csv |
| RES-2026-NEUTRAL | Neutral, January-April 2026 | 4.3% (116/2689; 95% CI 3.6%-5.1%) | January-April 2026 | outputs/T4_2026_descriptive.csv |
| RES-2026-CAUTIOUSOPTIMISM | Cautious Optimism, January-April 2026 | 62.4% (1678/2689; 95% CI 60.7%-64.3%) | January-April 2026 | outputs/T4_2026_descriptive.csv |
| RES-2026-ADVOCACY | Advocacy, January-April 2026 | 0.6% (17/2689; 95% CI 0.4%-0.9%) | January-April 2026 | outputs/T4_2026_descriptive.csv |
| RES-2026-CRITICALALARMCAUTION | Critical (Alarm+Caution), January-April 2026 | 32.7% (878/2689; 95% CI 30.9%-34.3%) | January-April 2026 | outputs/T4_2026_descriptive.csv |
| RES-2026-FAVOURABLECOADVOCACY | Favourable (CO+Advocacy), January-April 2026 | 63.0% (1695/2689; 95% CI 61.2%-64.9%) | January-April 2026 | outputs/T4_2026_descriptive.csv |

### 11. Multivariable logistic regression, critical stance (B4 primary; Table 2)

| ID | Item | Value | Window | Source |
|---|---|---|---|---|
| RES-REG-HEADER | Model | Logistic regression of critical stance (Alarm or Caution) on publication year (continuous, centred on 2023.856), genre, publication type, specialty and first-author region; n=14,058; events=4283; 2278 journal clusters; cluster-robust (journal) SEs | 2021-2025 | outputs/B4/B4_regression.md |
| RES-REG-YEAR-UOR | Year (per 1 year): unadjusted OR | OR 1.077 (95% CI 1.038-1.116), P<.001 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-GENRE-DISCOURSE-N | genre: discourse: records | 7633 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-GENRE-DISCOURSE-AOR | genre: discourse: adjusted OR | 1 (reference) | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-GENRE-DISCOURSE-UOR | genre: discourse: unadjusted OR | 1 (reference) | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-GENRE-DISCOURSE-AMP | genre: discourse: adjusted average marginal probability | 36.0% (95% CI 34.1%-37.9%) | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-GENRE-EVALUATIVE-N | genre: evaluative: records | 6425 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-GENRE-EVALUATIVE-AOR | genre: evaluative: adjusted OR | OR 0.54 (95% CI 0.48-0.61), P<.001 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-GENRE-EVALUATIVE-UOR | genre: evaluative: unadjusted OR | OR 0.63 (95% CI 0.55-0.71), P<.001 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-GENRE-EVALUATIVE-AMP | genre: evaluative: adjusted average marginal probability | 24.3% (95% CI 23.1%-25.7%) | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-PUBTYPE-COMMENTARY-N | pubtype: Commentary: records | 98 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-PUBTYPE-COMMENTARY-AOR | pubtype: Commentary: adjusted OR | OR 1.79 (95% CI 0.98-3.26), P=.056 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-PUBTYPE-COMMENTARY-UOR | pubtype: Commentary: unadjusted OR | OR 2.63 (95% CI 1.34-5.15), P=.005 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-PUBTYPE-COMMENTARY-AMP | pubtype: Commentary: adjusted average marginal probability | 48.0% (95% CI 35.2%-61.2%) | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-PUBTYPE-EDITORIAL-N | pubtype: Editorial: records | 364 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-PUBTYPE-EDITORIAL-AOR | pubtype: Editorial: adjusted OR | OR 0.73 (95% CI 0.56-0.95), P=.018 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-PUBTYPE-EDITORIAL-UOR | pubtype: Editorial: unadjusted OR | OR 1.21 (95% CI 0.94-1.57), P=.140 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-PUBTYPE-EDITORIAL-AMP | pubtype: Editorial: adjusted average marginal probability | 29.2% (95% CI 24.8%-34.0%) | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-PUBTYPE-LETTER-N | pubtype: Letter: records | 429 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-PUBTYPE-LETTER-AOR | pubtype: Letter: adjusted OR | OR 1.16 (95% CI 0.90-1.51), P=.249 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-PUBTYPE-LETTER-UOR | pubtype: Letter: unadjusted OR | OR 1.40 (95% CI 1.11-1.78), P=.005 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-PUBTYPE-LETTER-AMP | pubtype: Letter: adjusted average marginal probability | 38.6% (95% CI 33.5%-43.8%) | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-PUBTYPE-RESEARCHARTICLE-N | pubtype: Research Article: records | 8556 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-PUBTYPE-RESEARCHARTICLE-AOR | pubtype: Research Article: adjusted OR | 1 (reference) | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-PUBTYPE-RESEARCHARTICLE-UOR | pubtype: Research Article: unadjusted OR | 1 (reference) | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-PUBTYPE-RESEARCHARTICLE-AMP | pubtype: Research Article: adjusted average marginal probability | 35.4% (95% CI 33.9%-36.9%) | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-PUBTYPE-REVIEW-N | pubtype: Review: records | 4611 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-PUBTYPE-REVIEW-AOR | pubtype: Review: adjusted OR | OR 0.47 (95% CI 0.41-0.54), P<.001 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-PUBTYPE-REVIEW-UOR | pubtype: Review: unadjusted OR | OR 0.66 (95% CI 0.58-0.75), P<.001 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-PUBTYPE-REVIEW-AMP | pubtype: Review: adjusted average marginal probability | 21.5% (95% CI 19.6%-23.6%) | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-SPECIALTY-CARDIOLOGY-N | specialty: Cardiology: records | 542 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-SPECIALTY-CARDIOLOGY-AOR | specialty: Cardiology: adjusted OR | OR 0.28 (95% CI 0.21-0.36), P<.001 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-SPECIALTY-CARDIOLOGY-UOR | specialty: Cardiology: unadjusted OR | OR 0.23 (95% CI 0.18-0.30), P<.001 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-SPECIALTY-CARDIOLOGY-AMP | specialty: Cardiology: adjusted average marginal probability | 17.6% (95% CI 14.3%-21.4%) | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-SPECIALTY-DENTISTRY-N | specialty: Dentistry: records | 581 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-SPECIALTY-DENTISTRY-AOR | specialty: Dentistry: adjusted OR | OR 0.52 (95% CI 0.42-0.64), P<.001 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-SPECIALTY-DENTISTRY-UOR | specialty: Dentistry: unadjusted OR | OR 0.40 (95% CI 0.33-0.50), P<.001 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-SPECIALTY-DENTISTRY-AMP | specialty: Dentistry: adjusted average marginal probability | 28.1% (95% CI 24.4%-32.1%) | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-SPECIALTY-DERMATOLOGY-N | specialty: Dermatology: records | 265 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-SPECIALTY-DERMATOLOGY-AOR | specialty: Dermatology: adjusted OR | OR 0.76 (95% CI 0.59-0.98), P=.037 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-SPECIALTY-DERMATOLOGY-UOR | specialty: Dermatology: unadjusted OR | OR 0.72 (95% CI 0.56-0.94), P=.015 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-SPECIALTY-DERMATOLOGY-AMP | specialty: Dermatology: adjusted average marginal probability | 35.9% (95% CI 30.7%-41.6%) | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-SPECIALTY-EMERGENCYMEDICINECRITICA-N | specialty: Emergency Medicine / Critical Care: records | 308 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-SPECIALTY-EMERGENCYMEDICINECRITICA-AOR | specialty: Emergency Medicine / Critical Care: adjusted OR | OR 0.53 (95% CI 0.40-0.69), P<.001 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-SPECIALTY-EMERGENCYMEDICINECRITICA-UOR | specialty: Emergency Medicine / Critical Care: unadjusted OR | OR 0.47 (95% CI 0.36-0.61), P<.001 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-SPECIALTY-EMERGENCYMEDICINECRITICA-AMP | specialty: Emergency Medicine / Critical Care: adjusted average marginal probability | 28.2% (95% CI 23.7%-33.2%) | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-SPECIALTY-INTERNALMEDICINEPRIMARYC-N | specialty: Internal Medicine / Primary Care: records | 936 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-SPECIALTY-INTERNALMEDICINEPRIMARYC-AOR | specialty: Internal Medicine / Primary Care: adjusted OR | OR 0.41 (95% CI 0.34-0.49), P<.001 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-SPECIALTY-INTERNALMEDICINEPRIMARYC-UOR | specialty: Internal Medicine / Primary Care: unadjusted OR | OR 0.33 (95% CI 0.27-0.41), P<.001 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-SPECIALTY-INTERNALMEDICINEPRIMARYC-AMP | specialty: Internal Medicine / Primary Care: adjusted average marginal probability | 23.4% (95% CI 20.6%-26.5%) | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-SPECIALTY-MEDICALEDUCATION-N | specialty: Medical Education: records | 876 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-SPECIALTY-MEDICALEDUCATION-AOR | specialty: Medical Education: adjusted OR | OR 0.58 (95% CI 0.47-0.71), P<.001 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-SPECIALTY-MEDICALEDUCATION-UOR | specialty: Medical Education: unadjusted OR | OR 0.65 (95% CI 0.52-0.81), P<.001 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-SPECIALTY-MEDICALEDUCATION-AMP | specialty: Medical Education: adjusted average marginal probability | 30.1% (95% CI 26.5%-33.9%) | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-SPECIALTY-MEDICALINFORMATICSDIGITA-N | specialty: Medical Informatics / Digital Health: records | 3701 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-SPECIALTY-MEDICALINFORMATICSDIGITA-AOR | specialty: Medical Informatics / Digital Health: adjusted OR | 1 (reference) | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-SPECIALTY-MEDICALINFORMATICSDIGITA-UOR | specialty: Medical Informatics / Digital Health: unadjusted OR | 1 (reference) | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-SPECIALTY-MEDICALINFORMATICSDIGITA-AMP | specialty: Medical Informatics / Digital Health: adjusted average marginal probability | 42.0% (95% CI 39.6%-44.4%) | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-SPECIALTY-MENTALHEALTHPSYCHIATRY-N | specialty: Mental Health / Psychiatry: records | 390 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-SPECIALTY-MENTALHEALTHPSYCHIATRY-AOR | specialty: Mental Health / Psychiatry: adjusted OR | OR 1.22 (95% CI 0.94-1.60), P=.140 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-SPECIALTY-MENTALHEALTHPSYCHIATRY-UOR | specialty: Mental Health / Psychiatry: unadjusted OR | OR 1.22 (95% CI 0.93-1.62), P=.155 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-SPECIALTY-MENTALHEALTHPSYCHIATRY-AMP | specialty: Mental Health / Psychiatry: adjusted average marginal probability | 46.7% (95% CI 40.6%-52.9%) | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-SPECIALTY-MULTIDISCIPLINARYOTHER-N | specialty: Multidisciplinary / Other: records | 196 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-SPECIALTY-MULTIDISCIPLINARYOTHER-AOR | specialty: Multidisciplinary / Other: adjusted OR | OR 0.59 (95% CI 0.42-0.83), P=.002 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-SPECIALTY-MULTIDISCIPLINARYOTHER-UOR | specialty: Multidisciplinary / Other: unadjusted OR | OR 0.57 (95% CI 0.41-0.80), P<.001 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-SPECIALTY-MULTIDISCIPLINARYOTHER-AMP | specialty: Multidisciplinary / Other: adjusted average marginal probability | 30.6% (95% CI 24.2%-37.7%) | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-SPECIALTY-NEUROLOGYNEUROSCIENCE-N | specialty: Neurology / Neuroscience: records | 290 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-SPECIALTY-NEUROLOGYNEUROSCIENCE-AOR | specialty: Neurology / Neuroscience: adjusted OR | OR 0.44 (95% CI 0.32-0.61), P<.001 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-SPECIALTY-NEUROLOGYNEUROSCIENCE-UOR | specialty: Neurology / Neuroscience: unadjusted OR | OR 0.38 (95% CI 0.27-0.52), P<.001 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-SPECIALTY-NEUROLOGYNEUROSCIENCE-AMP | specialty: Neurology / Neuroscience: adjusted average marginal probability | 25.0% (95% CI 20.0%-30.7%) | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-SPECIALTY-NURSING-N | specialty: Nursing: records | 227 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-SPECIALTY-NURSING-AOR | specialty: Nursing: adjusted OR | OR 0.85 (95% CI 0.60-1.20), P=.349 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-SPECIALTY-NURSING-UOR | specialty: Nursing: unadjusted OR | OR 0.86 (95% CI 0.61-1.20), P=.368 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-SPECIALTY-NURSING-AMP | specialty: Nursing: adjusted average marginal probability | 38.2% (95% CI 30.9%-45.9%) | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-SPECIALTY-OBSTETRICSGYNECOLOGY-N | specialty: Obstetrics / Gynecology: records | 195 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-SPECIALTY-OBSTETRICSGYNECOLOGY-AOR | specialty: Obstetrics / Gynecology: adjusted OR | OR 0.46 (95% CI 0.33-0.65), P<.001 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-SPECIALTY-OBSTETRICSGYNECOLOGY-UOR | specialty: Obstetrics / Gynecology: unadjusted OR | OR 0.41 (95% CI 0.29-0.57), P<.001 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-SPECIALTY-OBSTETRICSGYNECOLOGY-AMP | specialty: Obstetrics / Gynecology: adjusted average marginal probability | 25.7% (95% CI 20.1%-32.3%) | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-SPECIALTY-ONCOLOGY-N | specialty: Oncology: records | 1211 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-SPECIALTY-ONCOLOGY-AOR | specialty: Oncology: adjusted OR | OR 0.35 (95% CI 0.30-0.42), P<.001 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-SPECIALTY-ONCOLOGY-UOR | specialty: Oncology: unadjusted OR | OR 0.28 (95% CI 0.23-0.34), P<.001 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-SPECIALTY-ONCOLOGY-AMP | specialty: Oncology: adjusted average marginal probability | 21.1% (95% CI 18.8%-23.7%) | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-SPECIALTY-OPHTHALMOLOGY-N | specialty: Ophthalmology: records | 669 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-SPECIALTY-OPHTHALMOLOGY-AOR | specialty: Ophthalmology: adjusted OR | OR 0.36 (95% CI 0.30-0.44), P<.001 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-SPECIALTY-OPHTHALMOLOGY-UOR | specialty: Ophthalmology: unadjusted OR | OR 0.28 (95% CI 0.22-0.34), P<.001 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-SPECIALTY-OPHTHALMOLOGY-AMP | specialty: Ophthalmology: adjusted average marginal probability | 21.6% (95% CI 18.7%-24.8%) | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-SPECIALTY-PATHOLOGYLABORATORYMEDIC-N | specialty: Pathology / Laboratory Medicine: records | 398 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-SPECIALTY-PATHOLOGYLABORATORYMEDIC-AOR | specialty: Pathology / Laboratory Medicine: adjusted OR | OR 0.37 (95% CI 0.29-0.47), P<.001 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-SPECIALTY-PATHOLOGYLABORATORYMEDIC-UOR | specialty: Pathology / Laboratory Medicine: unadjusted OR | OR 0.31 (95% CI 0.24-0.40), P<.001 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-SPECIALTY-PATHOLOGYLABORATORYMEDIC-AMP | specialty: Pathology / Laboratory Medicine: adjusted average marginal probability | 21.8% (95% CI 18.2%-25.9%) | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-SPECIALTY-PEDIATRICS-N | specialty: Pediatrics: records | 303 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-SPECIALTY-PEDIATRICS-AOR | specialty: Pediatrics: adjusted OR | OR 0.42 (95% CI 0.32-0.55), P<.001 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-SPECIALTY-PEDIATRICS-UOR | specialty: Pediatrics: unadjusted OR | OR 0.38 (95% CI 0.29-0.50), P<.001 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-SPECIALTY-PEDIATRICS-AMP | specialty: Pediatrics: adjusted average marginal probability | 24.0% (95% CI 19.8%-28.8%) | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-SPECIALTY-RADIOLOGYDIAGNOSTICIMAGI-N | specialty: Radiology / Diagnostic Imaging: records | 1769 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-SPECIALTY-RADIOLOGYDIAGNOSTICIMAGI-AOR | specialty: Radiology / Diagnostic Imaging: adjusted OR | OR 0.40 (95% CI 0.34-0.46), P<.001 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-SPECIALTY-RADIOLOGYDIAGNOSTICIMAGI-UOR | specialty: Radiology / Diagnostic Imaging: unadjusted OR | OR 0.31 (95% CI 0.26-0.37), P<.001 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-SPECIALTY-RADIOLOGYDIAGNOSTICIMAGI-AMP | specialty: Radiology / Diagnostic Imaging: adjusted average marginal probability | 23.0% (95% CI 20.9%-25.3%) | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-SPECIALTY-SURGERY-N | specialty: Surgery: records | 1191 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-SPECIALTY-SURGERY-AOR | specialty: Surgery: adjusted OR | OR 0.54 (95% CI 0.46-0.64), P<.001 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-SPECIALTY-SURGERY-UOR | specialty: Surgery: unadjusted OR | OR 0.50 (95% CI 0.42-0.59), P<.001 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-SPECIALTY-SURGERY-AMP | specialty: Surgery: adjusted average marginal probability | 28.7% (95% CI 26.3%-31.3%) | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-SPECIALTY-UNASSIGNED-N | specialty: Unassigned: records | 10 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-SPECIALTY-UNASSIGNED-AOR | specialty: Unassigned: adjusted OR | OR 0.16 (95% CI 0.02-1.45), P=.104 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-SPECIALTY-UNASSIGNED-UOR | specialty: Unassigned: unadjusted OR | OR 0.13 (95% CI 0.02-1.07), P=.058 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-SPECIALTY-UNASSIGNED-AMP | specialty: Unassigned: adjusted average marginal probability | 11.1% (95% CI 1.4%-51.7%) | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-REGION-EASTASIA-N | region: East Asia: records | 2702 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-REGION-EASTASIA-AOR | region: East Asia: adjusted OR | OR 0.44 (95% CI 0.38-0.51), P<.001 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-REGION-EASTASIA-UOR | region: East Asia: unadjusted OR | OR 0.40 (95% CI 0.34-0.47), P<.001 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-REGION-EASTASIA-AMP | region: East Asia: adjusted average marginal probability | 19.3% (95% CI 17.3%-21.6%) | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-REGION-EASTERNEUROPE-N | region: Eastern Europe: records | 272 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-REGION-EASTERNEUROPE-AOR | region: Eastern Europe: adjusted OR | OR 0.80 (95% CI 0.61-1.04), P=.098 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-REGION-EASTERNEUROPE-UOR | region: Eastern Europe: unadjusted OR | OR 0.72 (95% CI 0.55-0.96), P=.025 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-REGION-EASTERNEUROPE-AMP | region: Eastern Europe: adjusted average marginal probability | 29.4% (95% CI 24.7%-34.7%) | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-REGION-LATINAMERICAOCEANIA-N | region: Latin America / Oceania: records | 639 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-REGION-LATINAMERICAOCEANIA-AOR | region: Latin America / Oceania: adjusted OR | OR 1.11 (95% CI 0.93-1.33), P=.237 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-REGION-LATINAMERICAOCEANIA-UOR | region: Latin America / Oceania: unadjusted OR | OR 1.16 (95% CI 0.97-1.39), P=.109 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-REGION-LATINAMERICAOCEANIA-AMP | region: Latin America / Oceania: adjusted average marginal probability | 36.2% (95% CI 32.7%-39.8%) | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-REGION-MIDDLEEASTNORTHAFRICA-N | region: Middle East / North Africa: records | 1322 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-REGION-MIDDLEEASTNORTHAFRICA-AOR | region: Middle East / North Africa: adjusted OR | OR 0.79 (95% CI 0.68-0.91), P=.001 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-REGION-MIDDLEEASTNORTHAFRICA-UOR | region: Middle East / North Africa: unadjusted OR | OR 0.79 (95% CI 0.68-0.92), P=.002 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-REGION-MIDDLEEASTNORTHAFRICA-AMP | region: Middle East / North Africa: adjusted average marginal probability | 29.3% (95% CI 26.9%-31.8%) | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-REGION-NORTHAMERICA-N | region: North America: records | 4221 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-REGION-NORTHAMERICA-AOR | region: North America: adjusted OR | 1 (reference) | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-REGION-NORTHAMERICA-UOR | region: North America: unadjusted OR | 1 (reference) | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-REGION-NORTHAMERICA-AMP | region: North America: adjusted average marginal probability | 33.9% (95% CI 32.4%-35.5%) | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-REGION-SOUTHSOUTHEASTASIA-N | region: South/Southeast Asia: records | 656 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-REGION-SOUTHSOUTHEASTASIA-AOR | region: South/Southeast Asia: adjusted OR | OR 0.57 (95% CI 0.46-0.71), P<.001 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-REGION-SOUTHSOUTHEASTASIA-UOR | region: South/Southeast Asia: unadjusted OR | OR 0.60 (95% CI 0.49-0.74), P<.001 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-REGION-SOUTHSOUTHEASTASIA-AMP | region: South/Southeast Asia: adjusted average marginal probability | 23.5% (95% CI 20.4%-27.0%) | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-REGION-SUBSAHARANAFRICA-N | region: Sub-Saharan Africa: records | 49 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-REGION-SUBSAHARANAFRICA-AOR | region: Sub-Saharan Africa: adjusted OR | OR 1.11 (95% CI 0.60-2.06), P=.731 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-REGION-SUBSAHARANAFRICA-UOR | region: Sub-Saharan Africa: unadjusted OR | OR 1.40 (95% CI 0.75-2.63), P=.295 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-REGION-SUBSAHARANAFRICA-AMP | region: Sub-Saharan Africa: adjusted average marginal probability | 36.2% (95% CI 24.4%-49.9%) | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-REGION-UNKNOWN-N | region: Unknown: records | 504 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-REGION-UNKNOWN-AOR | region: Unknown: adjusted OR | OR 0.74 (95% CI 0.57-0.98), P=.034 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-REGION-UNKNOWN-UOR | region: Unknown: unadjusted OR | OR 0.89 (95% CI 0.62-1.28), P=.538 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-REGION-UNKNOWN-AMP | region: Unknown: adjusted average marginal probability | 28.2% (95% CI 23.5%-33.3%) | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-REGION-WESTERNEUROPE-N | region: Western Europe: records | 3693 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-REGION-WESTERNEUROPE-AOR | region: Western Europe: adjusted OR | OR 1.06 (95% CI 0.95-1.19), P=.296 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-REGION-WESTERNEUROPE-UOR | region: Western Europe: unadjusted OR | OR 0.98 (95% CI 0.87-1.12), P=.796 | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |
| RES-REG-REGION-WESTERNEUROPE-AMP | region: Western Europe: adjusted average marginal probability | 35.2% (95% CI 33.1%-37.5%) | 2021-2025 | outputs/B4/B4_primary_critical_ORs.csv; outputs/B4/B4_primary_critical_AMP.csv |

### 12. Advocacy model (B4 secondary 2)

| ID | Item | Value | Window | Source |
|---|---|---|---|---|
| RES-REGADV-HEADER | Model | Logistic regression of Advocacy vs not; n=14,058; events=218; 2278 journal clusters; levels with fewer than 5 Advocacy events collapsed into 'Other (<5 events)' | 2021-2025 | outputs/B4/B4_regression.md |
| RES-REGADV-GENRE-EVALUATIVE | genre: evaluative: adjusted OR | OR 0.17 (95% CI 0.10-0.27), P<.001 | 2021-2025 | outputs/B4/B4_advocacy_ORs.csv |
| RES-REGADV-PUBTYPE-EDITORIAL | pubtype: Editorial: adjusted OR | OR 3.31 (95% CI 1.96-5.61), P<.001 | 2021-2025 | outputs/B4/B4_advocacy_ORs.csv |
| RES-REGADV-PUBTYPE-LETTER | pubtype: Letter: adjusted OR | OR 3.48 (95% CI 2.18-5.54), P<.001 | 2021-2025 | outputs/B4/B4_advocacy_ORs.csv |
| RES-REGADV-PUBTYPE-OTHER5EVENTS | pubtype: Other (<5 events): adjusted OR | OR 0.81 (95% CI 0.17-3.89), P=.788 | 2021-2025 | outputs/B4/B4_advocacy_ORs.csv |
| RES-REGADV-PUBTYPE-REVIEW | pubtype: Review: adjusted OR | OR 0.90 (95% CI 0.62-1.31), P=.571 | 2021-2025 | outputs/B4/B4_advocacy_ORs.csv |
| RES-REGADV-SPECIALTY-CARDIOLOGY | specialty: Cardiology: adjusted OR | OR 1.47 (95% CI 0.79-2.72), P=.220 | 2021-2025 | outputs/B4/B4_advocacy_ORs.csv |
| RES-REGADV-SPECIALTY-DERMATOLOGY | specialty: Dermatology: adjusted OR | OR 1.02 (95% CI 0.40-2.60), P=.972 | 2021-2025 | outputs/B4/B4_advocacy_ORs.csv |
| RES-REGADV-SPECIALTY-INTERNALMEDICINEPRIMARYC | specialty: Internal Medicine / Primary Care: adjusted OR | OR 0.95 (95% CI 0.52-1.71), P=.855 | 2021-2025 | outputs/B4/B4_advocacy_ORs.csv |
| RES-REGADV-SPECIALTY-MEDICALEDUCATION | specialty: Medical Education: adjusted OR | OR 0.57 (95% CI 0.31-1.06), P=.077 | 2021-2025 | outputs/B4/B4_advocacy_ORs.csv |
| RES-REGADV-SPECIALTY-MULTIDISCIPLINARYOTHER | specialty: Multidisciplinary / Other: adjusted OR | OR 1.02 (95% CI 0.41-2.52), P=.966 | 2021-2025 | outputs/B4/B4_advocacy_ORs.csv |
| RES-REGADV-SPECIALTY-NEUROLOGYNEUROSCIENCE | specialty: Neurology / Neuroscience: adjusted OR | OR 1.34 (95% CI 0.58-3.09), P=.493 | 2021-2025 | outputs/B4/B4_advocacy_ORs.csv |
| RES-REGADV-SPECIALTY-ONCOLOGY | specialty: Oncology: adjusted OR | OR 1.03 (95% CI 0.60-1.79), P=.902 | 2021-2025 | outputs/B4/B4_advocacy_ORs.csv |
| RES-REGADV-SPECIALTY-OTHER5EVENTS | specialty: Other (<5 events): adjusted OR | OR 0.36 (95% CI 0.21-0.63), P<.001 | 2021-2025 | outputs/B4/B4_advocacy_ORs.csv |
| RES-REGADV-SPECIALTY-RADIOLOGYDIAGNOSTICIMAGI | specialty: Radiology / Diagnostic Imaging: adjusted OR | OR 0.51 (95% CI 0.29-0.92), P=.026 | 2021-2025 | outputs/B4/B4_advocacy_ORs.csv |
| RES-REGADV-SPECIALTY-SURGERY | specialty: Surgery: adjusted OR | OR 1.16 (95% CI 0.70-1.93), P=.565 | 2021-2025 | outputs/B4/B4_advocacy_ORs.csv |
| RES-REGADV-REGION-EASTASIA | region: East Asia: adjusted OR | OR 0.78 (95% CI 0.49-1.23), P=.283 | 2021-2025 | outputs/B4/B4_advocacy_ORs.csv |
| RES-REGADV-REGION-LATINAMERICAOCEANIA | region: Latin America / Oceania: adjusted OR | OR 0.67 (95% CI 0.32-1.40), P=.284 | 2021-2025 | outputs/B4/B4_advocacy_ORs.csv |
| RES-REGADV-REGION-MIDDLEEASTNORTHAFRICA | region: Middle East / North Africa: adjusted OR | OR 1.66 (95% CI 1.00-2.74), P=.049 | 2021-2025 | outputs/B4/B4_advocacy_ORs.csv |
| RES-REGADV-REGION-OTHER5EVENTS | region: Other (<5 events): adjusted OR | OR 1.06 (95% CI 0.47-2.37), P=.895 | 2021-2025 | outputs/B4/B4_advocacy_ORs.csv |
| RES-REGADV-REGION-SOUTHSOUTHEASTASIA | region: South/Southeast Asia: adjusted OR | OR 2.25 (95% CI 1.32-3.84), P=.003 | 2021-2025 | outputs/B4/B4_advocacy_ORs.csv |
| RES-REGADV-REGION-UNKNOWN | region: Unknown: adjusted OR | OR 1.35 (95% CI 0.71-2.57), P=.360 | 2021-2025 | outputs/B4/B4_advocacy_ORs.csv |
| RES-REGADV-REGION-WESTERNEUROPE | region: Western Europe: adjusted OR | OR 0.45 (95% CI 0.30-0.70), P<.001 | 2021-2025 | outputs/B4/B4_advocacy_ORs.csv |
| RES-REGADV-YEAR-PER1YEAR | year: per 1 year: adjusted OR | OR 0.84 (95% CI 0.75-0.94), P=.002 | 2021-2025 | outputs/B4/B4_advocacy_ORs.csv |

### 13. Ordinal model (B4 secondary 1)

| ID | Item | Value | Window | Source |
|---|---|---|---|---|
| RES-REGORD-HEADER | Model | Proportional-odds logistic model (Alarm < Caution < Neutral < Cautious Optimism < Advocacy); OR > 1 = more favourable; n=14,058; cluster-robust SEs; cut-point ORs from separate binary models | 2021-2025 | outputs/B4/B4_regression.md |
| RES-REGORD-GENRE-EVALUATIVE | genre: evaluative: ordinal OR; cut-point ORs; proportional-odds check | OR 1.36 (95% CI 1.22-1.51), P<.001; cut-point ORs >Alarm 0.19; >Caution 1.84; >Neutral 1.70; >Cautious Optimism 0.16; check: outside CI at >Alarm,Caution,Neutral,Cautious Optimism; sign change | 2021-2025 | outputs/B4/B4_ordinal_and_cutpoints.csv |
| RES-REGORD-PUBTYPE-COMMENTARY | pubtype: Commentary: ordinal OR; cut-point ORs; proportional-odds check | OR 0.59 (95% CI 0.39-0.87), P=.009; cut-point ORs >Alarm 0.38; >Caution 0.56; >Neutral 0.60; >Cautious Optimism 0.82; check: holds | 2021-2025 | outputs/B4/B4_ordinal_and_cutpoints.csv |
| RES-REGORD-PUBTYPE-EDITORIAL | pubtype: Editorial: ordinal OR; cut-point ORs; proportional-odds check | OR 1.33 (95% CI 1.04-1.68), P=.021; cut-point ORs >Alarm 1.07; >Caution 1.37; >Neutral 1.19; >Cautious Optimism 3.33; check: outside CI at >Cautious Optimism | 2021-2025 | outputs/B4/B4_ordinal_and_cutpoints.csv |
| RES-REGORD-PUBTYPE-LETTER | pubtype: Letter: ordinal OR; cut-point ORs; proportional-odds check | OR 0.65 (95% CI 0.51-0.83), P<.001; cut-point ORs >Alarm 0.66; >Caution 0.86; >Neutral 0.42; >Cautious Optimism 3.49; check: outside CI at >Caution,Neutral,Cautious Optimism; sign change | 2021-2025 | outputs/B4/B4_ordinal_and_cutpoints.csv |
| RES-REGORD-PUBTYPE-REVIEW | pubtype: Review: ordinal OR; cut-point ORs; proportional-odds check | OR 2.10 (95% CI 1.85-2.37), P<.001; cut-point ORs >Alarm 2.61; >Caution 2.13; >Neutral 2.42; >Cautious Optimism 0.89; check: outside CI at >Neutral,Cautious Optimism; sign change | 2021-2025 | outputs/B4/B4_ordinal_and_cutpoints.csv |
| RES-REGORD-SPECIALTY-CARDIOLOGY | specialty: Cardiology: ordinal OR; cut-point ORs; proportional-odds check | OR 3.47 (95% CI 2.80-4.32), P<.001; cut-point ORs >Alarm 2.16; >Caution 3.59; >Neutral 3.97; >Cautious Optimism 1.49; check: outside CI at >Cautious Optimism | 2021-2025 | outputs/B4/B4_ordinal_and_cutpoints.csv |
| RES-REGORD-SPECIALTY-DENTISTRY | specialty: Dentistry: ordinal OR; cut-point ORs; proportional-odds check | OR 1.85 (95% CI 1.51-2.27), P<.001; cut-point ORs >Alarm 1.44; >Caution 1.91; >Neutral 2.08; >Cautious Optimism 0.38; check: outside CI at >Cautious Optimism; sign change | 2021-2025 | outputs/B4/B4_ordinal_and_cutpoints.csv |
| RES-REGORD-SPECIALTY-DERMATOLOGY | specialty: Dermatology: ordinal OR; cut-point ORs; proportional-odds check | OR 1.32 (95% CI 1.00-1.74), P=.048; cut-point ORs >Alarm 0.95; >Caution 1.31; >Neutral 1.49; >Cautious Optimism 1.02; check: sign change | 2021-2025 | outputs/B4/B4_ordinal_and_cutpoints.csv |
| RES-REGORD-SPECIALTY-EMERGENCYMEDICINECRITICA | specialty: Emergency Medicine / Critical Care: ordinal OR; cut-point ORs; proportional-odds check | OR 1.84 (95% CI 1.43-2.37), P<.001; cut-point ORs >Alarm 1.12; >Caution 1.90; >Neutral 2.18; >Cautious Optimism 0.23; check: outside CI at >Cautious Optimism; sign change | 2021-2025 | outputs/B4/B4_ordinal_and_cutpoints.csv |
| RES-REGORD-SPECIALTY-INTERNALMEDICINEPRIMARYC | specialty: Internal Medicine / Primary Care: ordinal OR; cut-point ORs; proportional-odds check | OR 2.52 (95% CI 2.12-2.99), P<.001; cut-point ORs >Alarm 1.85; >Caution 2.47; >Neutral 2.93; >Cautious Optimism 0.95; check: outside CI at >Cautious Optimism; sign change | 2021-2025 | outputs/B4/B4_ordinal_and_cutpoints.csv |
| RES-REGORD-SPECIALTY-MEDICALEDUCATION | specialty: Medical Education: ordinal OR; cut-point ORs; proportional-odds check | OR 1.77 (95% CI 1.48-2.11), P<.001; cut-point ORs >Alarm 2.51; >Caution 1.73; >Neutral 1.99; >Cautious Optimism 0.57; check: outside CI at >Cautious Optimism; sign change | 2021-2025 | outputs/B4/B4_ordinal_and_cutpoints.csv |
| RES-REGORD-SPECIALTY-MENTALHEALTHPSYCHIATRY | specialty: Mental Health / Psychiatry: ordinal OR; cut-point ORs; proportional-odds check | OR 0.91 (95% CI 0.72-1.14), P=.399; cut-point ORs >Alarm 1.08; >Caution 0.82; >Neutral 1.02; >Cautious Optimism 0.12; check: outside CI at >Cautious Optimism; sign change | 2021-2025 | outputs/B4/B4_ordinal_and_cutpoints.csv |
| RES-REGORD-SPECIALTY-MULTIDISCIPLINARYOTHER | specialty: Multidisciplinary / Other: ordinal OR; cut-point ORs; proportional-odds check | OR 1.72 (95% CI 1.26-2.35), P<.001; cut-point ORs >Alarm 1.13; >Caution 1.69; >Neutral 2.00; >Cautious Optimism 1.01; check: holds | 2021-2025 | outputs/B4/B4_ordinal_and_cutpoints.csv |
| RES-REGORD-SPECIALTY-NEUROLOGYNEUROSCIENCE | specialty: Neurology / Neuroscience: ordinal OR; cut-point ORs; proportional-odds check | OR 2.24 (95% CI 1.69-2.98), P<.001; cut-point ORs >Alarm 1.17; >Caution 2.26; >Neutral 2.52; >Cautious Optimism 1.35; check: outside CI at >Alarm | 2021-2025 | outputs/B4/B4_ordinal_and_cutpoints.csv |
| RES-REGORD-SPECIALTY-NURSING | specialty: Nursing: ordinal OR; cut-point ORs; proportional-odds check | OR 1.22 (95% CI 0.90-1.66), P=.194; cut-point ORs >Alarm 1.29; >Caution 1.18; >Neutral 1.40; >Cautious Optimism 0.33; check: sign change | 2021-2025 | outputs/B4/B4_ordinal_and_cutpoints.csv |
| RES-REGORD-SPECIALTY-OBSTETRICSGYNECOLOGY | specialty: Obstetrics / Gynecology: ordinal OR; cut-point ORs; proportional-odds check | OR 2.31 (95% CI 1.67-3.20), P<.001; cut-point ORs >Alarm 1.79; >Caution 2.17; >Neutral 2.64; >Cautious Optimism 1.09; check: holds | 2021-2025 | outputs/B4/B4_ordinal_and_cutpoints.csv |
| RES-REGORD-SPECIALTY-ONCOLOGY | specialty: Oncology: ordinal OR; cut-point ORs; proportional-odds check | OR 2.69 (95% CI 2.31-3.14), P<.001; cut-point ORs >Alarm 2.17; >Caution 2.83; >Neutral 3.01; >Cautious Optimism 1.04; check: outside CI at >Cautious Optimism | 2021-2025 | outputs/B4/B4_ordinal_and_cutpoints.csv |
| RES-REGORD-SPECIALTY-OPHTHALMOLOGY | specialty: Ophthalmology: ordinal OR; cut-point ORs; proportional-odds check | OR 2.50 (95% CI 2.10-2.98), P<.001; cut-point ORs >Alarm 2.12; >Caution 2.75; >Neutral 2.93; >Cautious Optimism 0.22; check: outside CI at >Cautious Optimism; sign change | 2021-2025 | outputs/B4/B4_ordinal_and_cutpoints.csv |
| RES-REGORD-SPECIALTY-PATHOLOGYLABORATORYMEDIC | specialty: Pathology / Laboratory Medicine: ordinal OR; cut-point ORs; proportional-odds check | OR 2.37 (95% CI 1.93-2.91), P<.001; cut-point ORs >Alarm 1.63; >Caution 2.72; >Neutral 2.68; >Cautious Optimism 0.62; check: outside CI at >Cautious Optimism; sign change | 2021-2025 | outputs/B4/B4_ordinal_and_cutpoints.csv |
| RES-REGORD-SPECIALTY-PEDIATRICS | specialty: Pediatrics: ordinal OR; cut-point ORs; proportional-odds check | OR 2.37 (95% CI 1.86-3.03), P<.001; cut-point ORs >Alarm 1.71; >Caution 2.39; >Neutral 2.78; >Cautious Optimism 0.44; check: outside CI at >Cautious Optimism; sign change | 2021-2025 | outputs/B4/B4_ordinal_and_cutpoints.csv |
| RES-REGORD-SPECIALTY-RADIOLOGYDIAGNOSTICIMAGI | specialty: Radiology / Diagnostic Imaging: ordinal OR; cut-point ORs; proportional-odds check | OR 2.30 (95% CI 2.03-2.62), P<.001; cut-point ORs >Alarm 2.13; >Caution 2.53; >Neutral 2.53; >Cautious Optimism 0.52; check: outside CI at >Cautious Optimism; sign change | 2021-2025 | outputs/B4/B4_ordinal_and_cutpoints.csv |
| RES-REGORD-SPECIALTY-SURGERY | specialty: Surgery: ordinal OR; cut-point ORs; proportional-odds check | OR 1.95 (95% CI 1.65-2.30), P<.001; cut-point ORs >Alarm 1.20; >Caution 1.85; >Neutral 2.25; >Cautious Optimism 1.17; check: outside CI at >Alarm,Cautious Optimism | 2021-2025 | outputs/B4/B4_ordinal_and_cutpoints.csv |
| RES-REGORD-SPECIALTY-UNASSIGNED | specialty: Unassigned: ordinal OR; cut-point ORs; proportional-odds check | OR 3.44 (95% CI 0.94-12.62), P=.062; cut-point ORs >Alarm 1.19; >Caution 6.21; >Neutral 3.82; >Cautious Optimism 0.00; check: outside CI at >Cautious Optimism; sign change | 2021-2025 | outputs/B4/B4_ordinal_and_cutpoints.csv |
| RES-REGORD-REGION-EASTASIA | region: East Asia: ordinal OR; cut-point ORs; proportional-odds check | OR 1.90 (95% CI 1.70-2.14), P<.001; cut-point ORs >Alarm 1.98; >Caution 2.28; >Neutral 1.97; >Cautious Optimism 0.78; check: outside CI at >Caution,Cautious Optimism; sign change | 2021-2025 | outputs/B4/B4_ordinal_and_cutpoints.csv |
| RES-REGORD-REGION-EASTERNEUROPE | region: Eastern Europe: ordinal OR; cut-point ORs; proportional-odds check | OR 1.17 (95% CI 0.93-1.48), P=.177; cut-point ORs >Alarm 0.79; >Caution 1.25; >Neutral 1.20; >Cautious Optimism 0.85; check: sign change | 2021-2025 | outputs/B4/B4_ordinal_and_cutpoints.csv |
| RES-REGORD-REGION-LATINAMERICAOCEANIA | region: Latin America / Oceania: ordinal OR; cut-point ORs; proportional-odds check | OR 0.89 (95% CI 0.75-1.05), P=.154; cut-point ORs >Alarm 1.06; >Caution 0.90; >Neutral 0.87; >Cautious Optimism 0.68; check: sign change | 2021-2025 | outputs/B4/B4_ordinal_and_cutpoints.csv |
| RES-REGORD-REGION-MIDDLEEASTNORTHAFRICA | region: Middle East / North Africa: ordinal OR; cut-point ORs; proportional-odds check | OR 1.30 (95% CI 1.13-1.49), P<.001; cut-point ORs >Alarm 1.02; >Caution 1.27; >Neutral 1.32; >Cautious Optimism 1.67; check: holds | 2021-2025 | outputs/B4/B4_ordinal_and_cutpoints.csv |
| RES-REGORD-REGION-SOUTHSOUTHEASTASIA | region: South/Southeast Asia: ordinal OR; cut-point ORs; proportional-odds check | OR 1.81 (95% CI 1.48-2.22), P<.001; cut-point ORs >Alarm 1.59; >Caution 1.74; >Neutral 1.77; >Cautious Optimism 2.28; check: holds | 2021-2025 | outputs/B4/B4_ordinal_and_cutpoints.csv |
| RES-REGORD-REGION-SUBSAHARANAFRICA | region: Sub-Saharan Africa: ordinal OR; cut-point ORs; proportional-odds check | OR 0.98 (95% CI 0.55-1.75), P=.947; cut-point ORs >Alarm 0.77; >Caution 0.90; >Neutral 0.96; >Cautious Optimism 2.06; check: sign change | 2021-2025 | outputs/B4/B4_ordinal_and_cutpoints.csv |
| RES-REGORD-REGION-UNKNOWN | region: Unknown: ordinal OR; cut-point ORs; proportional-odds check | OR 1.21 (95% CI 0.97-1.51), P=.088; cut-point ORs >Alarm 0.95; >Caution 1.34; >Neutral 1.15; >Cautious Optimism 1.36; check: sign change | 2021-2025 | outputs/B4/B4_ordinal_and_cutpoints.csv |
| RES-REGORD-REGION-WESTERNEUROPE | region: Western Europe: ordinal OR; cut-point ORs; proportional-odds check | OR 0.95 (95% CI 0.86-1.05), P=.300; cut-point ORs >Alarm 1.12; >Caution 0.94; >Neutral 0.95; >Cautious Optimism 0.45; check: outside CI at >Cautious Optimism; sign change | 2021-2025 | outputs/B4/B4_ordinal_and_cutpoints.csv |
| RES-REGORD-YEAR-PER1YEAR | year: per 1 year: ordinal OR; cut-point ORs; proportional-odds check | OR 0.94 (95% CI 0.92-0.97), P<.001; cut-point ORs >Alarm 0.94; >Caution 0.91; >Neutral 0.97; >Cautious Optimism 0.84; check: outside CI at >Caution,Cautious Optimism | 2021-2025 | outputs/B4/B4_ordinal_and_cutpoints.csv |

### 14. Sensitivity models S1-S4 (B4)

| ID | Item | Value | Window | Source |
|---|---|---|---|---|
| RES-REGSEN-S1-YEAR-2022 | S1 year categorical: year: 2022: adjusted OR | OR 1.001 (95% CI 0.827-1.211), P=.993 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S1-YEAR-2023 | S1 year categorical: year: 2023: adjusted OR | OR 1.305 (95% CI 1.093-1.558), P=.003 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S1-YEAR-2024 | S1 year categorical: year: 2024: adjusted OR | OR 1.532 (95% CI 1.302-1.803), P<.001 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S1-YEAR-2025 | S1 year categorical: year: 2025: adjusted OR | OR 1.446 (95% CI 1.232-1.698), P<.001 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S1-GENRE-EVALUATIVE | S1 year categorical: genre: evaluative: adjusted OR | OR 0.54 (95% CI 0.48-0.61), P<.001 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S1-PUBTYPE-COMMENTARY | S1 year categorical: pubtype: Commentary: adjusted OR | OR 1.79 (95% CI 0.98-3.28), P=.059 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S1-PUBTYPE-EDITORIAL | S1 year categorical: pubtype: Editorial: adjusted OR | OR 0.72 (95% CI 0.55-0.93), P=.013 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S1-PUBTYPE-LETTER | S1 year categorical: pubtype: Letter: adjusted OR | OR 1.13 (95% CI 0.87-1.47), P=.354 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S1-PUBTYPE-REVIEW | S1 year categorical: pubtype: Review: adjusted OR | OR 0.47 (95% CI 0.41-0.54), P<.001 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S1-SPECIALTY-CARDIOLOGY | S1 year categorical: specialty: Cardiology: adjusted OR | OR 0.28 (95% CI 0.22-0.36), P<.001 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S1-SPECIALTY-DENTISTRY | S1 year categorical: specialty: Dentistry: adjusted OR | OR 0.52 (95% CI 0.42-0.65), P<.001 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S1-SPECIALTY-DERMATOLOGY | S1 year categorical: specialty: Dermatology: adjusted OR | OR 0.76 (95% CI 0.59-0.98), P=.033 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S1-SPECIALTY-EMERGENCYMEDICINECRITICA | S1 year categorical: specialty: Emergency Medicine / Critical Care: adjusted OR | OR 0.52 (95% CI 0.40-0.68), P<.001 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S1-SPECIALTY-INTERNALMEDICINEPRIMARYC | S1 year categorical: specialty: Internal Medicine / Primary Care: adjusted OR | OR 0.40 (95% CI 0.34-0.49), P<.001 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S1-SPECIALTY-MEDICALEDUCATION | S1 year categorical: specialty: Medical Education: adjusted OR | OR 0.58 (95% CI 0.47-0.71), P<.001 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S1-SPECIALTY-MENTALHEALTHPSYCHIATRY | S1 year categorical: specialty: Mental Health / Psychiatry: adjusted OR | OR 1.23 (95% CI 0.94-1.60), P=.134 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S1-SPECIALTY-MULTIDISCIPLINARYOTHER | S1 year categorical: specialty: Multidisciplinary / Other: adjusted OR | OR 0.59 (95% CI 0.42-0.83), P=.002 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S1-SPECIALTY-NEUROLOGYNEUROSCIENCE | S1 year categorical: specialty: Neurology / Neuroscience: adjusted OR | OR 0.44 (95% CI 0.32-0.60), P<.001 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S1-SPECIALTY-NURSING | S1 year categorical: specialty: Nursing: adjusted OR | OR 0.86 (95% CI 0.60-1.22), P=.390 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S1-SPECIALTY-OBSTETRICSGYNECOLOGY | S1 year categorical: specialty: Obstetrics / Gynecology: adjusted OR | OR 0.46 (95% CI 0.33-0.65), P<.001 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S1-SPECIALTY-ONCOLOGY | S1 year categorical: specialty: Oncology: adjusted OR | OR 0.35 (95% CI 0.29-0.42), P<.001 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S1-SPECIALTY-OPHTHALMOLOGY | S1 year categorical: specialty: Ophthalmology: adjusted OR | OR 0.36 (95% CI 0.30-0.44), P<.001 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S1-SPECIALTY-PATHOLOGYLABORATORYMEDIC | S1 year categorical: specialty: Pathology / Laboratory Medicine: adjusted OR | OR 0.37 (95% CI 0.29-0.47), P<.001 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S1-SPECIALTY-PEDIATRICS | S1 year categorical: specialty: Pediatrics: adjusted OR | OR 0.42 (95% CI 0.32-0.55), P<.001 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S1-SPECIALTY-RADIOLOGYDIAGNOSTICIMAGI | S1 year categorical: specialty: Radiology / Diagnostic Imaging: adjusted OR | OR 0.40 (95% CI 0.34-0.46), P<.001 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S1-SPECIALTY-SURGERY | S1 year categorical: specialty: Surgery: adjusted OR | OR 0.53 (95% CI 0.45-0.63), P<.001 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S1-SPECIALTY-UNASSIGNED | S1 year categorical: specialty: Unassigned: adjusted OR | OR 0.16 (95% CI 0.02-1.48), P=.108 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S1-REGION-EASTASIA | S1 year categorical: region: East Asia: adjusted OR | OR 0.44 (95% CI 0.38-0.52), P<.001 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S1-REGION-EASTERNEUROPE | S1 year categorical: region: Eastern Europe: adjusted OR | OR 0.80 (95% CI 0.61-1.05), P=.108 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S1-REGION-LATINAMERICAOCEANIA | S1 year categorical: region: Latin America / Oceania: adjusted OR | OR 1.12 (95% CI 0.94-1.34), P=.218 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S1-REGION-MIDDLEEASTNORTHAFRICA | S1 year categorical: region: Middle East / North Africa: adjusted OR | OR 0.80 (95% CI 0.69-0.92), P=.002 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S1-REGION-SOUTHSOUTHEASTASIA | S1 year categorical: region: South/Southeast Asia: adjusted OR | OR 0.57 (95% CI 0.46-0.71), P<.001 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S1-REGION-SUBSAHARANAFRICA | S1 year categorical: region: Sub-Saharan Africa: adjusted OR | OR 1.12 (95% CI 0.61-2.05), P=.721 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S1-REGION-UNKNOWN | S1 year categorical: region: Unknown: adjusted OR | OR 0.74 (95% CI 0.56-0.97), P=.029 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S1-REGION-WESTERNEUROPE | S1 year categorical: region: Western Europe: adjusted OR | OR 1.07 (95% CI 0.95-1.20), P=.256 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S2-YEAR-2022 | S2 with Jan–Apr 2026: year: 2022: adjusted OR | OR 0.997 (95% CI 0.825-1.206), P=.978 | 2021-April 2026 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S2-YEAR-2023 | S2 with Jan–Apr 2026: year: 2023: adjusted OR | OR 1.298 (95% CI 1.088-1.548), P=.004 | 2021-April 2026 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S2-YEAR-2024 | S2 with Jan–Apr 2026: year: 2024: adjusted OR | OR 1.529 (95% CI 1.300-1.798), P<.001 | 2021-April 2026 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S2-YEAR-2025 | S2 with Jan–Apr 2026: year: 2025: adjusted OR | OR 1.441 (95% CI 1.229-1.690), P<.001 | 2021-April 2026 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S2-YEAR-2026 | S2 with Jan–Apr 2026: year: 2026: adjusted OR | OR 1.610 (95% CI 1.349-1.921), P<.001 | 2021-April 2026 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S2-GENRE-EVALUATIVE | S2 with Jan–Apr 2026: genre: evaluative: adjusted OR | OR 0.54 (95% CI 0.48-0.60), P<.001 | 2021-April 2026 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S2-PUBTYPE-COMMENTARY | S2 with Jan–Apr 2026: pubtype: Commentary: adjusted OR | OR 1.62 (95% CI 0.88-2.99), P=.122 | 2021-April 2026 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S2-PUBTYPE-EDITORIAL | S2 with Jan–Apr 2026: pubtype: Editorial: adjusted OR | OR 0.76 (95% CI 0.59-0.98), P=.035 | 2021-April 2026 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S2-PUBTYPE-LETTER | S2 with Jan–Apr 2026: pubtype: Letter: adjusted OR | OR 1.20 (95% CI 0.94-1.54), P=.140 | 2021-April 2026 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S2-PUBTYPE-REVIEW | S2 with Jan–Apr 2026: pubtype: Review: adjusted OR | OR 0.48 (95% CI 0.42-0.54), P<.001 | 2021-April 2026 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S2-SPECIALTY-CARDIOLOGY | S2 with Jan–Apr 2026: specialty: Cardiology: adjusted OR | OR 0.30 (95% CI 0.23-0.38), P<.001 | 2021-April 2026 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S2-SPECIALTY-DENTISTRY | S2 with Jan–Apr 2026: specialty: Dentistry: adjusted OR | OR 0.52 (95% CI 0.43-0.62), P<.001 | 2021-April 2026 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S2-SPECIALTY-DERMATOLOGY | S2 with Jan–Apr 2026: specialty: Dermatology: adjusted OR | OR 0.76 (95% CI 0.60-0.96), P=.020 | 2021-April 2026 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S2-SPECIALTY-EMERGENCYMEDICINECRITICA | S2 with Jan–Apr 2026: specialty: Emergency Medicine / Critical Care: adjusted OR | OR 0.54 (95% CI 0.42-0.70), P<.001 | 2021-April 2026 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S2-SPECIALTY-INTERNALMEDICINEPRIMARYC | S2 with Jan–Apr 2026: specialty: Internal Medicine / Primary Care: adjusted OR | OR 0.42 (95% CI 0.35-0.50), P<.001 | 2021-April 2026 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S2-SPECIALTY-MEDICALEDUCATION | S2 with Jan–Apr 2026: specialty: Medical Education: adjusted OR | OR 0.58 (95% CI 0.48-0.71), P<.001 | 2021-April 2026 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S2-SPECIALTY-MENTALHEALTHPSYCHIATRY | S2 with Jan–Apr 2026: specialty: Mental Health / Psychiatry: adjusted OR | OR 1.30 (95% CI 1.02-1.65), P=.034 | 2021-April 2026 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S2-SPECIALTY-MULTIDISCIPLINARYOTHER | S2 with Jan–Apr 2026: specialty: Multidisciplinary / Other: adjusted OR | OR 0.60 (95% CI 0.45-0.82), P=.001 | 2021-April 2026 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S2-SPECIALTY-NEUROLOGYNEUROSCIENCE | S2 with Jan–Apr 2026: specialty: Neurology / Neuroscience: adjusted OR | OR 0.46 (95% CI 0.34-0.62), P<.001 | 2021-April 2026 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S2-SPECIALTY-NURSING | S2 with Jan–Apr 2026: specialty: Nursing: adjusted OR | OR 0.89 (95% CI 0.66-1.19), P=.419 | 2021-April 2026 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S2-SPECIALTY-OBSTETRICSGYNECOLOGY | S2 with Jan–Apr 2026: specialty: Obstetrics / Gynecology: adjusted OR | OR 0.52 (95% CI 0.37-0.73), P<.001 | 2021-April 2026 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S2-SPECIALTY-ONCOLOGY | S2 with Jan–Apr 2026: specialty: Oncology: adjusted OR | OR 0.37 (95% CI 0.32-0.44), P<.001 | 2021-April 2026 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S2-SPECIALTY-OPHTHALMOLOGY | S2 with Jan–Apr 2026: specialty: Ophthalmology: adjusted OR | OR 0.36 (95% CI 0.30-0.45), P<.001 | 2021-April 2026 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S2-SPECIALTY-PATHOLOGYLABORATORYMEDIC | S2 with Jan–Apr 2026: specialty: Pathology / Laboratory Medicine: adjusted OR | OR 0.38 (95% CI 0.30-0.48), P<.001 | 2021-April 2026 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S2-SPECIALTY-PEDIATRICS | S2 with Jan–Apr 2026: specialty: Pediatrics: adjusted OR | OR 0.47 (95% CI 0.37-0.60), P<.001 | 2021-April 2026 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S2-SPECIALTY-RADIOLOGYDIAGNOSTICIMAGI | S2 with Jan–Apr 2026: specialty: Radiology / Diagnostic Imaging: adjusted OR | OR 0.42 (95% CI 0.37-0.48), P<.001 | 2021-April 2026 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S2-SPECIALTY-SURGERY | S2 with Jan–Apr 2026: specialty: Surgery: adjusted OR | OR 0.54 (95% CI 0.46-0.62), P<.001 | 2021-April 2026 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S2-SPECIALTY-UNASSIGNED | S2 with Jan–Apr 2026: specialty: Unassigned: adjusted OR | OR 0.29 (95% CI 0.06-1.50), P=.139 | 2021-April 2026 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S2-REGION-EASTASIA | S2 with Jan–Apr 2026: region: East Asia: adjusted OR | OR 0.46 (95% CI 0.40-0.52), P<.001 | 2021-April 2026 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S2-REGION-EASTERNEUROPE | S2 with Jan–Apr 2026: region: Eastern Europe: adjusted OR | OR 0.83 (95% CI 0.65-1.06), P=.146 | 2021-April 2026 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S2-REGION-LATINAMERICAOCEANIA | S2 with Jan–Apr 2026: region: Latin America / Oceania: adjusted OR | OR 1.04 (95% CI 0.88-1.23), P=.625 | 2021-April 2026 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S2-REGION-MIDDLEEASTNORTHAFRICA | S2 with Jan–Apr 2026: region: Middle East / North Africa: adjusted OR | OR 0.83 (95% CI 0.73-0.95), P=.006 | 2021-April 2026 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S2-REGION-SOUTHSOUTHEASTASIA | S2 with Jan–Apr 2026: region: South/Southeast Asia: adjusted OR | OR 0.57 (95% CI 0.47-0.70), P<.001 | 2021-April 2026 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S2-REGION-SUBSAHARANAFRICA | S2 with Jan–Apr 2026: region: Sub-Saharan Africa: adjusted OR | OR 1.34 (95% CI 0.84-2.15), P=.222 | 2021-April 2026 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S2-REGION-UNKNOWN | S2 with Jan–Apr 2026: region: Unknown: adjusted OR | OR 0.75 (95% CI 0.58-0.96), P=.025 | 2021-April 2026 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S2-REGION-WESTERNEUROPE | S2 with Jan–Apr 2026: region: Western Europe: adjusted OR | OR 1.08 (95% CI 0.98-1.19), P=.138 | 2021-April 2026 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S3-GENRE-EVALUATIVE | S3 journal fixed effects: genre: evaluative: adjusted OR | OR 0.51 (95% CI 0.43-0.60), P<.001 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S3-PUBTYPE-COMMENTARY | S3 journal fixed effects: pubtype: Commentary: adjusted OR | OR 1.13 (95% CI 0.55-2.34), P=.734 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S3-PUBTYPE-EDITORIAL | S3 journal fixed effects: pubtype: Editorial: adjusted OR | OR 0.64 (95% CI 0.44-0.93), P=.019 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S3-PUBTYPE-LETTER | S3 journal fixed effects: pubtype: Letter: adjusted OR | OR 1.11 (95% CI 0.76-1.62), P=.585 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S3-PUBTYPE-REVIEW | S3 journal fixed effects: pubtype: Review: adjusted OR | OR 0.62 (95% CI 0.50-0.76), P<.001 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S3-SPECIALTY-CARDIOLOGY | S3 journal fixed effects: specialty: Cardiology: adjusted OR | OR 0.56 (95% CI 0.40-0.79), P<.001 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S3-SPECIALTY-DENTISTRY | S3 journal fixed effects: specialty: Dentistry: adjusted OR | OR 0.48 (95% CI 0.34-0.70), P<.001 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S3-SPECIALTY-DERMATOLOGY | S3 journal fixed effects: specialty: Dermatology: adjusted OR | OR 1.15 (95% CI 0.70-1.90), P=.576 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S3-SPECIALTY-EMERGENCYMEDICINECRITICA | S3 journal fixed effects: specialty: Emergency Medicine / Critical Care: adjusted OR | OR 0.46 (95% CI 0.31-0.67), P<.001 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S3-SPECIALTY-INTERNALMEDICINEPRIMARYC | S3 journal fixed effects: specialty: Internal Medicine / Primary Care: adjusted OR | OR 0.54 (95% CI 0.39-0.74), P<.001 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S3-SPECIALTY-MEDICALEDUCATION | S3 journal fixed effects: specialty: Medical Education: adjusted OR | OR 0.54 (95% CI 0.40-0.72), P<.001 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S3-SPECIALTY-MENTALHEALTHPSYCHIATRY | S3 journal fixed effects: specialty: Mental Health / Psychiatry: adjusted OR | OR 0.92 (95% CI 0.61-1.39), P=.693 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S3-SPECIALTY-MULTIDISCIPLINARYOTHER | S3 journal fixed effects: specialty: Multidisciplinary / Other: adjusted OR | OR 1.23 (95% CI 0.66-2.27), P=.516 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S3-SPECIALTY-NEUROLOGYNEUROSCIENCE | S3 journal fixed effects: specialty: Neurology / Neuroscience: adjusted OR | OR 0.47 (95% CI 0.28-0.79), P=.005 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S3-SPECIALTY-NURSING | S3 journal fixed effects: specialty: Nursing: adjusted OR | OR 0.74 (95% CI 0.40-1.36), P=.330 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S3-SPECIALTY-OBSTETRICSGYNECOLOGY | S3 journal fixed effects: specialty: Obstetrics / Gynecology: adjusted OR | OR 0.27 (95% CI 0.15-0.47), P<.001 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S3-SPECIALTY-ONCOLOGY | S3 journal fixed effects: specialty: Oncology: adjusted OR | OR 0.42 (95% CI 0.33-0.55), P<.001 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S3-SPECIALTY-OPHTHALMOLOGY | S3 journal fixed effects: specialty: Ophthalmology: adjusted OR | OR 0.49 (95% CI 0.35-0.68), P<.001 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S3-SPECIALTY-PATHOLOGYLABORATORYMEDIC | S3 journal fixed effects: specialty: Pathology / Laboratory Medicine: adjusted OR | OR 0.49 (95% CI 0.32-0.74), P<.001 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S3-SPECIALTY-PEDIATRICS | S3 journal fixed effects: specialty: Pediatrics: adjusted OR | OR 0.50 (95% CI 0.31-0.80), P=.004 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S3-SPECIALTY-RADIOLOGYDIAGNOSTICIMAGI | S3 journal fixed effects: specialty: Radiology / Diagnostic Imaging: adjusted OR | OR 0.49 (95% CI 0.40-0.62), P<.001 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S3-SPECIALTY-SURGERY | S3 journal fixed effects: specialty: Surgery: adjusted OR | OR 0.71 (95% CI 0.54-0.93), P=.014 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S3-SPECIALTY-UNASSIGNED | S3 journal fixed effects: specialty: Unassigned: adjusted OR | OR 0.41 (95% CI 0.05-3.54), P=.415 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S3-REGION-EASTASIA | S3 journal fixed effects: region: East Asia: adjusted OR | OR 0.48 (95% CI 0.40-0.57), P<.001 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S3-REGION-EASTERNEUROPE | S3 journal fixed effects: region: Eastern Europe: adjusted OR | OR 0.82 (95% CI 0.57-1.17), P=.279 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S3-REGION-LATINAMERICAOCEANIA | S3 journal fixed effects: region: Latin America / Oceania: adjusted OR | OR 0.93 (95% CI 0.73-1.19), P=.585 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S3-REGION-MIDDLEEASTNORTHAFRICA | S3 journal fixed effects: region: Middle East / North Africa: adjusted OR | OR 0.89 (95% CI 0.72-1.10), P=.271 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S3-REGION-SOUTHSOUTHEASTASIA | S3 journal fixed effects: region: South/Southeast Asia: adjusted OR | OR 0.72 (95% CI 0.51-1.02), P=.066 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S3-REGION-SUBSAHARANAFRICA | S3 journal fixed effects: region: Sub-Saharan Africa: adjusted OR | OR 1.36 (95% CI 0.45-4.05), P=.585 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S3-REGION-UNKNOWN | S3 journal fixed effects: region: Unknown: adjusted OR | OR 0.59 (95% CI 0.34-1.04), P=.069 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S3-REGION-WESTERNEUROPE | S3 journal fixed effects: region: Western Europe: adjusted OR | OR 1.03 (95% CI 0.86-1.22), P=.766 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S3-YEAR-PER1YEAR | S3 journal fixed effects: year: per 1 year: adjusted OR | OR 1.082 (95% CI 1.030-1.137), P=.002 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S4-GENRE-EVALUATIVE | S4 country instead of region: genre: evaluative: adjusted OR | OR 0.54 (95% CI 0.47-0.61), P<.001 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S4-PUBTYPE-COMMENTARY | S4 country instead of region: pubtype: Commentary: adjusted OR | OR 1.83 (95% CI 1.03-3.25), P=.041 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S4-PUBTYPE-EDITORIAL | S4 country instead of region: pubtype: Editorial: adjusted OR | OR 0.74 (95% CI 0.57-0.97), P=.026 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S4-PUBTYPE-LETTER | S4 country instead of region: pubtype: Letter: adjusted OR | OR 1.19 (95% CI 0.92-1.55), P=.190 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S4-PUBTYPE-REVIEW | S4 country instead of region: pubtype: Review: adjusted OR | OR 0.49 (95% CI 0.42-0.56), P<.001 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S4-SPECIALTY-CARDIOLOGY | S4 country instead of region: specialty: Cardiology: adjusted OR | OR 0.27 (95% CI 0.21-0.35), P<.001 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S4-SPECIALTY-DENTISTRY | S4 country instead of region: specialty: Dentistry: adjusted OR | OR 0.51 (95% CI 0.42-0.63), P<.001 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S4-SPECIALTY-DERMATOLOGY | S4 country instead of region: specialty: Dermatology: adjusted OR | OR 0.77 (95% CI 0.60-0.99), P=.043 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S4-SPECIALTY-EMERGENCYMEDICINECRITICA | S4 country instead of region: specialty: Emergency Medicine / Critical Care: adjusted OR | OR 0.52 (95% CI 0.40-0.67), P<.001 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S4-SPECIALTY-INTERNALMEDICINEPRIMARYC | S4 country instead of region: specialty: Internal Medicine / Primary Care: adjusted OR | OR 0.42 (95% CI 0.35-0.50), P<.001 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S4-SPECIALTY-MEDICALEDUCATION | S4 country instead of region: specialty: Medical Education: adjusted OR | OR 0.58 (95% CI 0.47-0.71), P<.001 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S4-SPECIALTY-MENTALHEALTHPSYCHIATRY | S4 country instead of region: specialty: Mental Health / Psychiatry: adjusted OR | OR 1.21 (95% CI 0.93-1.57), P=.164 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S4-SPECIALTY-MULTIDISCIPLINARYOTHER | S4 country instead of region: specialty: Multidisciplinary / Other: adjusted OR | OR 0.61 (95% CI 0.44-0.86), P=.004 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S4-SPECIALTY-NEUROLOGYNEUROSCIENCE | S4 country instead of region: specialty: Neurology / Neuroscience: adjusted OR | OR 0.45 (95% CI 0.33-0.62), P<.001 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S4-SPECIALTY-NURSING | S4 country instead of region: specialty: Nursing: adjusted OR | OR 0.81 (95% CI 0.57-1.13), P=.217 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S4-SPECIALTY-OBSTETRICSGYNECOLOGY | S4 country instead of region: specialty: Obstetrics / Gynecology: adjusted OR | OR 0.45 (95% CI 0.32-0.63), P<.001 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S4-SPECIALTY-ONCOLOGY | S4 country instead of region: specialty: Oncology: adjusted OR | OR 0.36 (95% CI 0.30-0.43), P<.001 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S4-SPECIALTY-OPHTHALMOLOGY | S4 country instead of region: specialty: Ophthalmology: adjusted OR | OR 0.36 (95% CI 0.29-0.44), P<.001 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S4-SPECIALTY-PATHOLOGYLABORATORYMEDIC | S4 country instead of region: specialty: Pathology / Laboratory Medicine: adjusted OR | OR 0.37 (95% CI 0.29-0.47), P<.001 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S4-SPECIALTY-PEDIATRICS | S4 country instead of region: specialty: Pediatrics: adjusted OR | OR 0.41 (95% CI 0.31-0.53), P<.001 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S4-SPECIALTY-RADIOLOGYDIAGNOSTICIMAGI | S4 country instead of region: specialty: Radiology / Diagnostic Imaging: adjusted OR | OR 0.39 (95% CI 0.33-0.45), P<.001 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S4-SPECIALTY-SURGERY | S4 country instead of region: specialty: Surgery: adjusted OR | OR 0.54 (95% CI 0.46-0.64), P<.001 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S4-SPECIALTY-UNASSIGNED | S4 country instead of region: specialty: Unassigned: adjusted OR | OR 0.17 (95% CI 0.02-1.57), P=.118 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S4-COUNTRY_G-AUSTRALIA | S4 country instead of region: country_g: Australia: adjusted OR | OR 1.45 (95% CI 1.15-1.82), P=.002 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S4-COUNTRY_G-BRAZIL | S4 country instead of region: country_g: Brazil: adjusted OR | OR 0.51 (95% CI 0.32-0.81), P=.005 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S4-COUNTRY_G-CANADA | S4 country instead of region: country_g: Canada: adjusted OR | OR 1.21 (95% CI 0.97-1.52), P=.090 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S4-COUNTRY_G-CHINA | S4 country instead of region: country_g: China: adjusted OR | OR 0.36 (95% CI 0.29-0.44), P<.001 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S4-COUNTRY_G-FRANCE | S4 country instead of region: country_g: France: adjusted OR | OR 0.87 (95% CI 0.63-1.19), P=.390 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S4-COUNTRY_G-GERMANY | S4 country instead of region: country_g: Germany: adjusted OR | OR 1.10 (95% CI 0.90-1.34), P=.363 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S4-COUNTRY_G-INDIA | S4 country instead of region: country_g: India: adjusted OR | OR 0.46 (95% CI 0.35-0.60), P<.001 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S4-COUNTRY_G-IRAN | S4 country instead of region: country_g: Iran: adjusted OR | OR 0.48 (95% CI 0.31-0.74), P<.001 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S4-COUNTRY_G-ISRAEL | S4 country instead of region: country_g: Israel: adjusted OR | OR 1.02 (95% CI 0.73-1.41), P=.929 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S4-COUNTRY_G-ITALY | S4 country instead of region: country_g: Italy: adjusted OR | OR 0.75 (95% CI 0.60-0.92), P=.007 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S4-COUNTRY_G-JAPAN | S4 country instead of region: country_g: Japan: adjusted OR | OR 0.53 (95% CI 0.39-0.71), P<.001 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S4-COUNTRY_G-NETHERLANDS | S4 country instead of region: country_g: Netherlands: adjusted OR | OR 1.64 (95% CI 1.29-2.08), P<.001 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S4-COUNTRY_G-OTHER | S4 country instead of region: country_g: Other: adjusted OR | OR 0.88 (95% CI 0.75-1.02), P=.095 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S4-COUNTRY_G-SAUDIARABIA | S4 country instead of region: country_g: Saudi Arabia: adjusted OR | OR 0.50 (95% CI 0.34-0.74), P<.001 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S4-COUNTRY_G-SINGAPORE | S4 country instead of region: country_g: Singapore: adjusted OR | OR 0.79 (95% CI 0.53-1.18), P=.244 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S4-COUNTRY_G-SOUTHKOREA | S4 country instead of region: country_g: South Korea: adjusted OR | OR 0.58 (95% CI 0.43-0.78), P<.001 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S4-COUNTRY_G-SPAIN | S4 country instead of region: country_g: Spain: adjusted OR | OR 0.75 (95% CI 0.51-1.10), P=.136 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S4-COUNTRY_G-SWEDEN | S4 country instead of region: country_g: Sweden: adjusted OR | OR 1.07 (95% CI 0.64-1.77), P=.805 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S4-COUNTRY_G-SWITZERLAND | S4 country instead of region: country_g: Switzerland: adjusted OR | OR 1.45 (95% CI 1.07-1.97), P=.016 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S4-COUNTRY_G-TAIWAN | S4 country instead of region: country_g: Taiwan: adjusted OR | OR 0.52 (95% CI 0.33-0.83), P=.006 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S4-COUNTRY_G-TURKEY | S4 country instead of region: country_g: Turkey: adjusted OR | OR 1.24 (95% CI 0.95-1.60), P=.107 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S4-COUNTRY_G-UNITEDKINGDOM | S4 country instead of region: country_g: United Kingdom: adjusted OR | OR 1.37 (95% CI 1.17-1.60), P<.001 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S4-COUNTRY_G-UNRESOLVED | S4 country instead of region: country_g: Unresolved: adjusted OR | OR 0.87 (95% CI 0.75-1.02), P=.086 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |
| RES-REGSEN-S4-YEAR-PER1YEAR | S4 country instead of region: year: per 1 year: adjusted OR | OR 1.110 (95% CI 1.073-1.149), P<.001 | 2021-2025 | outputs/B4/B4_sensitivity_ORs.csv |

### 15. Stance trend under the stricter v2 rubric (Table S1 v2 column)

| ID | Item | Value | Window | Source |
|---|---|---|---|---|
| RES-V2-ALARM | Alarm: v2 rubric 2021 and 2025 shares; Spearman ρ (exact P) | 2.2% to 3.6%; ρ=+0.80 (P=.133) | 2021-2025 | final/data/v2_trend.csv (output/analyses/temporal_stance_v2.csv) |
| RES-V2-CAUTION | Caution: v2 rubric 2021 and 2025 shares; Spearman ρ (exact P) | 16.9% to 21.6%; ρ=+0.70 (P=.233) | 2021-2025 | final/data/v2_trend.csv (output/analyses/temporal_stance_v2.csv) |
| RES-V2-NEUTRAL | Neutral: v2 rubric 2021 and 2025 shares; Spearman ρ (exact P) | 23.8% to 15.3%; ρ=-1.00 (P=.017) | 2021-2025 | final/data/v2_trend.csv (output/analyses/temporal_stance_v2.csv) |
| RES-V2-CAUTIOUSOPTIMISM | Cautious Optimism: v2 rubric 2021 and 2025 shares; Spearman ρ (exact P) | 55.5% to 58.5%; ρ=+0.20 (P=.783) | 2021-2025 | final/data/v2_trend.csv (output/analyses/temporal_stance_v2.csv) |
| RES-V2-ADVOCACY | Advocacy: v2 rubric 2021 and 2025 shares; Spearman ρ (exact P) | 1.6% to 0.9%; ρ=-0.50 (P=.450) | 2021-2025 | final/data/v2_trend.csv (output/analyses/temporal_stance_v2.csv) |
| RES-V2-CRITICAL | Critical: v2 rubric 2021 and 2025 shares; Spearman ρ (exact P) | 19.1% to 25.3%; ρ=+0.70 (P=.233) | 2021-2025 | final/data/v2_trend.csv (output/analyses/temporal_stance_v2.csv) |

### 16. Pooled theme prevalence among critical records (Table S5)

| ID | Item | Value | Window | Source |
|---|---|---|---|---|
| RES-THM-POOLED-PATIENTSAFETY | Patient safety: pooled prevalence 2021-2025 | 64.3% (2755/4283; 95% CI 62.9%-65.8%) | 2021-2025 | final/data/theme_pooled.csv |
| RES-THM-POOLED-HALLUCINATIONERRORS | Hallucination / errors: pooled prevalence 2021-2025 | 46.0% (1971/4283; 95% CI 44.5%-47.5%) | 2021-2025 | final/data/theme_pooled.csv |
| RES-THM-POOLED-GOVERNANCEREGULATION | Governance / regulation: pooled prevalence 2021-2025 | 37.2% (1593/4283; 95% CI 35.7%-38.6%) | 2021-2025 | final/data/theme_pooled.csv |
| RES-THM-POOLED-ETHICSANDBIAS | Ethics & bias: pooled prevalence 2021-2025 | 34.6% (1483/4283; 95% CI 33.2%-36.1%) | 2021-2025 | final/data/theme_pooled.csv |
| RES-THM-POOLED-MEDICALEDUCATION | Medical education: pooled prevalence 2021-2025 | 8.6% (367/4283; 95% CI 7.7%-9.4%) | 2021-2025 | final/data/theme_pooled.csv |
| RES-THM-POOLED-DATAPRIVACY | Data privacy: pooled prevalence 2021-2025 | 7.6% (325/4283; 95% CI 6.9%-8.4%) | 2021-2025 | final/data/theme_pooled.csv |
| RES-THM-POOLED-COGNITIVEOFFLOADING | Cognitive offloading: pooled prevalence 2021-2025 | 5.9% (254/4283; 95% CI 5.3%-6.6%) | 2021-2025 | final/data/theme_pooled.csv |
| RES-THM-POOLED-EXISTENTIALTHREAT | Existential threat: pooled prevalence 2021-2025 | 4.9% (210/4283; 95% CI 4.3%-5.5%) | 2021-2025 | final/data/theme_pooled.csv |
| RES-THM-POOLED-REPLACEMENTFEARS | Replacement fears: pooled prevalence 2021-2025 | 4.0% (171/4283; 95% CI 3.4%-4.6%) | 2021-2025 | final/data/theme_pooled.csv |
| RES-THM-POOLED-OTHER | Other: pooled prevalence 2021-2025 | 2.2% (94/4283; 95% CI 1.8%-2.7%) | 2021-2025 | final/data/theme_pooled.csv |

### 17. Q3 comparison arm, pooled 2021-2025 (Table S14)

| ID | Item | Value | Window | Source |
|---|---|---|---|---|
| RES-Q3-POOLED-ALARM | Q3 arm: Alarm | 4.5% (38/853; 95% CI 3.2%-5.7%) | 2021-2025 | final/data/q3_pooled.csv |
| RES-Q3-POOLED-CAUTION | Q3 arm: Caution | 21.9% (187/853; 95% CI 19.0%-24.6%) | 2021-2025 | final/data/q3_pooled.csv |
| RES-Q3-POOLED-NEUTRAL | Q3 arm: Neutral | 3.8% (32/853; 95% CI 2.6%-5.2%) | 2021-2025 | final/data/q3_pooled.csv |
| RES-Q3-POOLED-CAUTIOUSOPTIMISM | Q3 arm: Cautious Optimism | 66.5% (567/853; 95% CI 63.4%-69.6%) | 2021-2025 | final/data/q3_pooled.csv |
| RES-Q3-POOLED-ADVOCACY | Q3 arm: Advocacy | 3.4% (29/853; 95% CI 2.2%-4.8%) | 2021-2025 | final/data/q3_pooled.csv |
| RES-Q3-POOLED-CRITICAL | Q3 arm: Critical | 26.4% (225/853; 95% CI 23.3%-29.2%) | 2021-2025 | final/data/q3_pooled.csv |
| RES-Q3-POOLED-FAVOURABLE | Q3 arm: Favourable | 69.9% (596/853; 95% CI 66.8%-73.2%) | 2021-2025 | final/data/q3_pooled.csv |

### 18. B5 annual series by corpus definition

| ID | Item | Value | Window | Source |
|---|---|---|---|---|
| RES-B5ANN-FULL-CRITICAL-2021 | Full corpus: Critical, 2021 | 25.4% (270/1063; 95% CI 22.8%-28.0%) | 2021-2025 | final/data/b5_annual.csv |
| RES-B5ANN-FULL-CRITICAL-2022 | Full corpus: Critical, 2022 | 24.8% (333/1343; 95% CI 22.6%-27.1%) | 2021-2025 | final/data/b5_annual.csv |
| RES-B5ANN-FULL-CRITICAL-2023 | Full corpus: Critical, 2023 | 30.4% (624/2054; 95% CI 28.3%-32.5%) | 2021-2025 | final/data/b5_annual.csv |
| RES-B5ANN-FULL-CRITICAL-2024 | Full corpus: Critical, 2024 | 33.2% (1228/3700; 95% CI 31.8%-34.8%) | 2021-2025 | final/data/b5_annual.csv |
| RES-B5ANN-FULL-CRITICAL-2025 | Full corpus: Critical, 2025 | 31.0% (1828/5898; 95% CI 29.8%-32.3%) | 2021-2025 | final/data/b5_annual.csv |
| RES-B5ANN-FULL-ADVOCACY-2021 | Full corpus: Advocacy, 2021 | 2.9% (31/1063; 95% CI 1.9%-4.0%) | 2021-2025 | final/data/b5_annual.csv |
| RES-B5ANN-FULL-ADVOCACY-2022 | Full corpus: Advocacy, 2022 | 2.0% (27/1343; 95% CI 1.3%-2.8%) | 2021-2025 | final/data/b5_annual.csv |
| RES-B5ANN-FULL-ADVOCACY-2023 | Full corpus: Advocacy, 2023 | 1.9% (40/2054; 95% CI 1.4%-2.6%) | 2021-2025 | final/data/b5_annual.csv |
| RES-B5ANN-FULL-ADVOCACY-2024 | Full corpus: Advocacy, 2024 | 1.5% (54/3700; 95% CI 1.1%-1.8%) | 2021-2025 | final/data/b5_annual.csv |
| RES-B5ANN-FULL-ADVOCACY-2025 | Full corpus: Advocacy, 2025 | 1.1% (66/5898; 95% CI 0.9%-1.4%) | 2021-2025 | final/data/b5_annual.csv |
| RES-B5ANN-D1-CRITICAL-2021 | D1 Medicine area (primary): Critical, 2021 | 25.2% (230/912; 95% CI 22.5%-28.0%) | 2021-2025 | final/data/b5_annual.csv |
| RES-B5ANN-D1-CRITICAL-2022 | D1 Medicine area (primary): Critical, 2022 | 26.1% (296/1134; 95% CI 23.7%-28.7%) | 2021-2025 | final/data/b5_annual.csv |
| RES-B5ANN-D1-CRITICAL-2023 | D1 Medicine area (primary): Critical, 2023 | 31.4% (538/1712; 95% CI 29.3%-33.8%) | 2021-2025 | final/data/b5_annual.csv |
| RES-B5ANN-D1-CRITICAL-2024 | D1 Medicine area (primary): Critical, 2024 | 33.9% (1073/3163; 95% CI 32.4%-35.5%) | 2021-2025 | final/data/b5_annual.csv |
| RES-B5ANN-D1-CRITICAL-2025 | D1 Medicine area (primary): Critical, 2025 | 30.9% (1488/4812; 95% CI 29.6%-32.2%) | 2021-2025 | final/data/b5_annual.csv |
| RES-B5ANN-D1-ADVOCACY-2021 | D1 Medicine area (primary): Advocacy, 2021 | 2.4% (22/912; 95% CI 1.5%-3.5%) | 2021-2025 | final/data/b5_annual.csv |
| RES-B5ANN-D1-ADVOCACY-2022 | D1 Medicine area (primary): Advocacy, 2022 | 1.9% (21/1134; 95% CI 1.1%-2.7%) | 2021-2025 | final/data/b5_annual.csv |
| RES-B5ANN-D1-ADVOCACY-2023 | D1 Medicine area (primary): Advocacy, 2023 | 1.9% (33/1712; 95% CI 1.3%-2.6%) | 2021-2025 | final/data/b5_annual.csv |
| RES-B5ANN-D1-ADVOCACY-2024 | D1 Medicine area (primary): Advocacy, 2024 | 1.2% (39/3163; 95% CI 0.9%-1.6%) | 2021-2025 | final/data/b5_annual.csv |
| RES-B5ANN-D1-ADVOCACY-2025 | D1 Medicine area (primary): Advocacy, 2025 | 0.9% (42/4812; 95% CI 0.6%-1.1%) | 2021-2025 | final/data/b5_annual.csv |
| RES-B5ANN-D2-CRITICAL-2021 | D2 D1 minus Medicine (misc.): Critical, 2021 | 24.3% (197/811; 95% CI 21.4%-27.3%) | 2021-2025 | final/data/b5_annual.csv |
| RES-B5ANN-D2-CRITICAL-2022 | D2 D1 minus Medicine (misc.): Critical, 2022 | 26.1% (261/1001; 95% CI 23.5%-28.7%) | 2021-2025 | final/data/b5_annual.csv |
| RES-B5ANN-D2-CRITICAL-2023 | D2 D1 minus Medicine (misc.): Critical, 2023 | 31.2% (454/1454; 95% CI 29.0%-33.6%) | 2021-2025 | final/data/b5_annual.csv |
| RES-B5ANN-D2-CRITICAL-2024 | D2 D1 minus Medicine (misc.): Critical, 2024 | 33.9% (943/2781; 95% CI 32.3%-35.7%) | 2021-2025 | final/data/b5_annual.csv |
| RES-B5ANN-D2-CRITICAL-2025 | D2 D1 minus Medicine (misc.): Critical, 2025 | 31.6% (1306/4133; 95% CI 30.2%-33.1%) | 2021-2025 | final/data/b5_annual.csv |
| RES-B5ANN-D2-ADVOCACY-2021 | D2 D1 minus Medicine (misc.): Advocacy, 2021 | 2.0% (16/811; 95% CI 1.1%-2.9%) | 2021-2025 | final/data/b5_annual.csv |
| RES-B5ANN-D2-ADVOCACY-2022 | D2 D1 minus Medicine (misc.): Advocacy, 2022 | 1.7% (17/1001; 95% CI 1.0%-2.5%) | 2021-2025 | final/data/b5_annual.csv |
| RES-B5ANN-D2-ADVOCACY-2023 | D2 D1 minus Medicine (misc.): Advocacy, 2023 | 1.7% (25/1454; 95% CI 1.1%-2.5%) | 2021-2025 | final/data/b5_annual.csv |
| RES-B5ANN-D2-ADVOCACY-2024 | D2 D1 minus Medicine (misc.): Advocacy, 2024 | 1.1% (31/2781; 95% CI 0.7%-1.5%) | 2021-2025 | final/data/b5_annual.csv |
| RES-B5ANN-D2-ADVOCACY-2025 | D2 D1 minus Medicine (misc.): Advocacy, 2025 | 0.9% (36/4133; 95% CI 0.6%-1.2%) | 2021-2025 | final/data/b5_annual.csv |
| RES-B5ANN-D3-CRITICAL-2021 | D3 broad health sciences: Critical, 2021 | 25.4% (244/961; 95% CI 22.8%-28.3%) | 2021-2025 | final/data/b5_annual.csv |
| RES-B5ANN-D3-CRITICAL-2022 | D3 broad health sciences: Critical, 2022 | 25.9% (310/1197; 95% CI 23.6%-28.4%) | 2021-2025 | final/data/b5_annual.csv |
| RES-B5ANN-D3-CRITICAL-2023 | D3 broad health sciences: Critical, 2023 | 31.1% (560/1802; 95% CI 29.2%-33.1%) | 2021-2025 | final/data/b5_annual.csv |
| RES-B5ANN-D3-CRITICAL-2024 | D3 broad health sciences: Critical, 2024 | 33.8% (1148/3396; 95% CI 32.1%-35.4%) | 2021-2025 | final/data/b5_annual.csv |
| RES-B5ANN-D3-CRITICAL-2025 | D3 broad health sciences: Critical, 2025 | 31.2% (1672/5355; 95% CI 30.0%-32.4%) | 2021-2025 | final/data/b5_annual.csv |
| RES-B5ANN-D3-ADVOCACY-2021 | D3 broad health sciences: Advocacy, 2021 | 2.7% (26/961; 95% CI 1.7%-3.8%) | 2021-2025 | final/data/b5_annual.csv |
| RES-B5ANN-D3-ADVOCACY-2022 | D3 broad health sciences: Advocacy, 2022 | 1.9% (23/1197; 95% CI 1.1%-2.7%) | 2021-2025 | final/data/b5_annual.csv |
| RES-B5ANN-D3-ADVOCACY-2023 | D3 broad health sciences: Advocacy, 2023 | 2.1% (37/1802; 95% CI 1.4%-2.7%) | 2021-2025 | final/data/b5_annual.csv |
| RES-B5ANN-D3-ADVOCACY-2024 | D3 broad health sciences: Advocacy, 2024 | 1.4% (47/3396; 95% CI 1.0%-1.8%) | 2021-2025 | final/data/b5_annual.csv |
| RES-B5ANN-D3-ADVOCACY-2025 | D3 broad health sciences: Advocacy, 2025 | 1.0% (54/5355; 95% CI 0.8%-1.3%) | 2021-2025 | final/data/b5_annual.csv |

### 19. B5 detail, 2021-2025 (Table S sjr_sensitivity)

| ID | Item | Value | Window | Source |
|---|---|---|---|---|
| RES-B5X-FULL-STANCEDIST-ALARM | Full corpus: Stance distribution, 2021–2025: Alarm | 5.3% (749/14,058; 95% CI 5.0%-5.7%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-FULL-STANCEDIST-CAUTION | Full corpus: Stance distribution, 2021–2025: Caution | 25.1% (3534/14,058; 95% CI 24.4%-25.9%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-FULL-STANCEDIST-NEUTRAL | Full corpus: Stance distribution, 2021–2025: Neutral | 5.1% (721/14,058; 95% CI 4.8%-5.5%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-FULL-STANCEDIST-CAUTIOUSOPTIMISM | Full corpus: Stance distribution, 2021–2025: Cautious Optimism | 62.9% (8836/14,058; 95% CI 62.0%-63.7%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-FULL-STANCEDIST-ADVOCACY | Full corpus: Stance distribution, 2021–2025: Advocacy | 1.6% (218/14,058; 95% CI 1.4%-1.8%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-FULL-STANCEDIST-CRITICAL | Full corpus: Stance distribution, 2021–2025: Critical | 30.5% (4283/14,058; 95% CI 29.7%-31.2%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-FULL-STANCEDIST-FAVOURABLE | Full corpus: Stance distribution, 2021–2025: Favourable | 64.4% (9054/14,058; 95% CI 63.6%-65.2%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-FULL-TREND20212-CRITICAL | Full corpus: Trend 2021–2025: Critical | ρ=+0.80 (P=.133); OR 1.077 per year (95% CI 1.046-1.108), P<.001 | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-FULL-TREND20212-ADVOCACY | Full corpus: Trend 2021–2025: Advocacy | ρ=-1.00 (P=.017); OR 0.793 per year (95% CI 0.721-0.872), P<.001 | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-FULL-THEMETREND-PATIENTSAFETY | Full corpus: Theme trend 2021–2025 (among critical): Patient safety | 59.3% to 64.9% (change +5.7 percentage points); ρ=+0.80 (P=.133); OR 1.055 per year (95% CI 1.002-1.111) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-FULL-THEMETREND-HALLUCINATIONERRORS | Full corpus: Theme trend 2021–2025 (among critical): Hallucination / errors | 23.7% to 51.1% (change +27.4 percentage points); ρ=+0.80 (P=.133); OR 1.367 per year (95% CI 1.296-1.442) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-FULL-THEMETREND-GOVERNANCEREGULATION | Full corpus: Theme trend 2021–2025 (among critical): Governance / regulation | 54.8% to 31.7% (change -23.1 percentage points); ρ=-0.90 (P=.083); OR 0.765 per year (95% CI 0.727-0.805) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-FULL-THEMETREND-ETHICSANDBIAS | Full corpus: Theme trend 2021–2025 (among critical): Ethics & bias | 36.7% to 33.0% (change -3.6 percentage points); ρ=-0.80 (P=.133); OR 0.915 per year (95% CI 0.869-0.963) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-FULL-SPECIALTY2-RANGEN30CATEGORIES | Full corpus: Specialty, 2021–2025: range (n≥30 categories) | Mental Health / Psychiatry 50.3% (196/390) to Cardiology 16.1% (87/542) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-FULL-SPECIALTY2-FDASPEARMAN | Full corpus: Specialty, 2021–2025: FDA Spearman ρ | -0.61 (two-sided P=.007, n=18) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-FULL-SPECIALTYD-RADIOLOGYDIAGNOSTICIMAGI | Full corpus: Specialty detail, 2021–2025: Radiology / Diagnostic Imaging | 20.4% (18.6-22.4) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-FULL-SPECIALTYD-PATHOLOGYLABORATORYMEDIC | Full corpus: Specialty detail, 2021–2025: Pathology / Laboratory Medicine | 20.4% (16.2-24.4) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-FULL-SPECIALTYD-CARDIOLOGY | Full corpus: Specialty detail, 2021–2025: Cardiology | 16.1% (12.8-19.2) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-FULL-SPECIALTYD-ONCOLOGY | Full corpus: Specialty detail, 2021–2025: Oncology | 18.7% (16.5-21.0) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-FULL-SPECIALTYD-SURGERY | Full corpus: Specialty detail, 2021–2025: Surgery | 29.1% (26.4-31.8) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-FULL-SPECIALTYD-OPHTHALMOLOGY | Full corpus: Specialty detail, 2021–2025: Ophthalmology | 18.5% (15.7-21.6) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-FULL-SPECIALTYD-DERMATOLOGY | Full corpus: Specialty detail, 2021–2025: Dermatology | 37.4% (31.7-43.1) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-FULL-SPECIALTYD-NEUROLOGYNEUROSCIENCE | Full corpus: Specialty detail, 2021–2025: Neurology / Neuroscience | 23.8% (18.7-28.6) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-FULL-SPECIALTYD-MENTALHEALTHPSYCHIATRY | Full corpus: Specialty detail, 2021–2025: Mental Health / Psychiatry | 50.3% (45.7-55.2) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-FULL-SPECIALTYD-INTERNALMEDICINEPRIMARYC | Full corpus: Specialty detail, 2021–2025: Internal Medicine / Primary Care | 21.6% (19.0-24.3) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-FULL-SPECIALTYD-EMERGENCYMEDICINECRITICA | Full corpus: Specialty detail, 2021–2025: Emergency Medicine / Critical Care | 27.9% (23.2-33.2) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-FULL-SPECIALTYD-PEDIATRICS | Full corpus: Specialty detail, 2021–2025: Pediatrics | 23.8% (19.0-28.4) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-FULL-SPECIALTYD-OBSTETRICSGYNECOLOGY | Full corpus: Specialty detail, 2021–2025: Obstetrics / Gynecology | 25.1% (19.2-31.5) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-FULL-SPECIALTYD-DENTISTRY | Full corpus: Specialty detail, 2021–2025: Dentistry | 25.0% (21.4-28.6) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-FULL-SPECIALTYD-MEDICALINFORMATICSDIGITA | Full corpus: Specialty detail, 2021–2025: Medical Informatics / Digital Health | 45.2% (43.6-46.9) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-FULL-SPECIALTYD-NURSING | Full corpus: Specialty detail, 2021–2025: Nursing | 41.4% (34.5-47.5) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-FULL-SPECIALTYD-MEDICALEDUCATION | Full corpus: Specialty detail, 2021–2025: Medical Education | 34.9% (31.9-38.3) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-FULL-SPECIALTYD-MULTIDISCIPLINARYOTHER | Full corpus: Specialty detail, 2021–2025: Multidisciplinary / Other | 32.1% (25.3-39.0) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-FULL-REGION2021-EASTASIA | Full corpus: Region, 2021–2025: East Asia | 17.7% (478/2702; 95% CI 16.3%-19.3%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-FULL-REGION2021-EASTERNEUROPE | Full corpus: Region, 2021–2025: Eastern Europe | 27.9% (76/272; 95% CI 22.6%-33.6%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-FULL-REGION2021-LATINAMERICAOCEANIA | Full corpus: Region, 2021–2025: Latin America / Oceania | 38.3% (245/639; 95% CI 34.6%-42.2%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-FULL-REGION2021-MIDDLEEASTNORTHAFRICA | Full corpus: Region, 2021–2025: Middle East / North Africa | 29.8% (394/1322; 95% CI 27.1%-32.3%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-FULL-REGION2021-NORTHAMERICA | Full corpus: Region, 2021–2025: North America | 34.9% (1472/4221; 95% CI 33.5%-36.3%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-FULL-REGION2021-SOUTHSOUTHEASTASIA | Full corpus: Region, 2021–2025: South/Southeast Asia | 24.4% (160/656; 95% CI 21.4%-27.8%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-FULL-REGION2021-SUBSAHARANAFRICA | Full corpus: Region, 2021–2025: Sub-Saharan Africa | 42.9% (21/49; 95% CI 29.2%-57.1%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-FULL-REGION2021-UNKNOWN | Full corpus: Region, 2021–2025: Unknown | 32.3% (163/504; 95% CI 28.5%-36.2%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-FULL-REGION2021-WESTERNEUROPE | Full corpus: Region, 2021–2025: Western Europe | 34.5% (1274/3693; 95% CI 33.0%-36.1%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-FULL-PUBLICATIO-RESEARCHARTICLE | Full corpus: Publication type, 2021–2025: Research Article | 32.7% (2799/8556; 95% CI 31.6%-33.7%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-FULL-PUBLICATIO-REVIEW | Full corpus: Publication type, 2021–2025: Review | 24.3% (1120/4611; 95% CI 23.1%-25.5%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-FULL-PUBLICATIO-LETTER | Full corpus: Publication type, 2021–2025: Letter | 40.6% (174/429; 95% CI 36.1%-45.5%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-FULL-PUBLICATIO-EDITORIAL | Full corpus: Publication type, 2021–2025: Editorial | 37.1% (135/364; 95% CI 32.1%-42.0%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-FULL-PUBLICATIO-COMMENTARY | Full corpus: Publication type, 2021–2025: Commentary | 56.1% (55/98; 95% CI 45.9%-66.3%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D1-STANCEDIST-ALARM | D1 Medicine area (primary): Stance distribution, 2021–2025: Alarm | 5.3% (625/11,733; 95% CI 5.0%-5.8%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D1-STANCEDIST-CAUTION | D1 Medicine area (primary): Stance distribution, 2021–2025: Caution | 25.6% (3000/11,733; 95% CI 24.8%-26.4%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D1-STANCEDIST-NEUTRAL | D1 Medicine area (primary): Stance distribution, 2021–2025: Neutral | 5.0% (587/11,733; 95% CI 4.6%-5.4%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D1-STANCEDIST-CAUTIOUSOPTIMISM | D1 Medicine area (primary): Stance distribution, 2021–2025: Cautious Optimism | 62.8% (7364/11,733; 95% CI 61.9%-63.6%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D1-STANCEDIST-ADVOCACY | D1 Medicine area (primary): Stance distribution, 2021–2025: Advocacy | 1.3% (157/11,733; 95% CI 1.1%-1.6%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D1-STANCEDIST-CRITICAL | D1 Medicine area (primary): Stance distribution, 2021–2025: Critical | 30.9% (3625/11,733; 95% CI 30.1%-31.7%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D1-STANCEDIST-FAVOURABLE | D1 Medicine area (primary): Stance distribution, 2021–2025: Favourable | 64.1% (7521/11,733; 95% CI 63.2%-65.0%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D1-TREND20212-CRITICAL | D1 Medicine area (primary): Trend 2021–2025: Critical | ρ=+0.70 (P=.233); OR 1.066 per year (95% CI 1.034-1.100), P<.001 | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D1-TREND20212-ADVOCACY | D1 Medicine area (primary): Trend 2021–2025: Advocacy | ρ=-0.90 (P=.083); OR 0.771 per year (95% CI 0.690-0.862), P<.001 | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D1-THEMETREND-PATIENTSAFETY | D1 Medicine area (primary): Theme trend 2021–2025 (among critical): Patient safety | 59.1% to 66.7% (change +7.6 percentage points); ρ=+0.90 (P=.083); OR 1.080 per year (95% CI 1.021-1.143) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D1-THEMETREND-HALLUCINATIONERRORS | D1 Medicine area (primary): Theme trend 2021–2025 (among critical): Hallucination / errors | 23.0% to 50.7% (change +27.7 percentage points); ρ=+0.80 (P=.133); OR 1.386 per year (95% CI 1.308-1.470) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D1-THEMETREND-GOVERNANCEREGULATION | D1 Medicine area (primary): Theme trend 2021–2025 (among critical): Governance / regulation | 55.2% to 33.3% (change -21.9 percentage points); ρ=-0.90 (P=.083); OR 0.772 per year (95% CI 0.731-0.817) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D1-THEMETREND-ETHICSANDBIAS | D1 Medicine area (primary): Theme trend 2021–2025 (among critical): Ethics & bias | 37.0% to 33.1% (change -3.8 percentage points); ρ=-0.80 (P=.133); OR 0.912 per year (95% CI 0.863-0.965) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D1-SPECIALTY2-RANGEN30CATEGORIES | D1 Medicine area (primary): Specialty, 2021–2025: range (n≥30 categories) | Mental Health / Psychiatry 49.6% (167/337) to Cardiology 16.4% (82/500) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D1-SPECIALTY2-FDASPEARMAN | D1 Medicine area (primary): Specialty, 2021–2025: FDA Spearman ρ | -0.61 (two-sided P=.007, n=18) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D1-SPECIALTYD-RADIOLOGYDIAGNOSTICIMAGI | D1 Medicine area (primary): Specialty detail, 2021–2025: Radiology / Diagnostic Imaging | 21.0% (19.0-23.2) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D1-SPECIALTYD-PATHOLOGYLABORATORYMEDIC | D1 Medicine area (primary): Specialty detail, 2021–2025: Pathology / Laboratory Medicine | 20.2% (15.9-24.5) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D1-SPECIALTYD-CARDIOLOGY | D1 Medicine area (primary): Specialty detail, 2021–2025: Cardiology | 16.4% (13.5-19.7) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D1-SPECIALTYD-ONCOLOGY | D1 Medicine area (primary): Specialty detail, 2021–2025: Oncology | 19.3% (16.9-21.7) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D1-SPECIALTYD-SURGERY | D1 Medicine area (primary): Specialty detail, 2021–2025: Surgery | 29.1% (26.5-31.8) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D1-SPECIALTYD-OPHTHALMOLOGY | D1 Medicine area (primary): Specialty detail, 2021–2025: Ophthalmology | 18.9% (15.5-22.0) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D1-SPECIALTYD-DERMATOLOGY | D1 Medicine area (primary): Specialty detail, 2021–2025: Dermatology | 38.4% (32.1-45.0) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D1-SPECIALTYD-NEUROLOGYNEUROSCIENCE | D1 Medicine area (primary): Specialty detail, 2021–2025: Neurology / Neuroscience | 24.5% (19.2-30.0) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D1-SPECIALTYD-MENTALHEALTHPSYCHIATRY | D1 Medicine area (primary): Specialty detail, 2021–2025: Mental Health / Psychiatry | 49.6% (44.4-55.0) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D1-SPECIALTYD-INTERNALMEDICINEPRIMARYC | D1 Medicine area (primary): Specialty detail, 2021–2025: Internal Medicine / Primary Care | 21.6% (18.8-24.4) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D1-SPECIALTYD-EMERGENCYMEDICINECRITICA | D1 Medicine area (primary): Specialty detail, 2021–2025: Emergency Medicine / Critical Care | 27.5% (22.4-32.6) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D1-SPECIALTYD-PEDIATRICS | D1 Medicine area (primary): Specialty detail, 2021–2025: Pediatrics | 24.1% (19.4-29.2) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D1-SPECIALTYD-OBSTETRICSGYNECOLOGY | D1 Medicine area (primary): Specialty detail, 2021–2025: Obstetrics / Gynecology | 25.9% (19.1-32.2) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D1-SPECIALTYD-DENTISTRY | D1 Medicine area (primary): Specialty detail, 2021–2025: Dentistry | 21.9% (16.7-27.6) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D1-SPECIALTYD-MEDICALINFORMATICSDIGITA | D1 Medicine area (primary): Specialty detail, 2021–2025: Medical Informatics / Digital Health | 47.8% (46.1-49.4) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D1-SPECIALTYD-NURSING | D1 Medicine area (primary): Specialty detail, 2021–2025: Nursing | 37.3% (26.9-47.8) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D1-SPECIALTYD-MEDICALEDUCATION | D1 Medicine area (primary): Specialty detail, 2021–2025: Medical Education | 36.8% (33.3-40.4) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D1-SPECIALTYD-MULTIDISCIPLINARYOTHER | D1 Medicine area (primary): Specialty detail, 2021–2025: Multidisciplinary / Other | 36.5% (27.8-45.5) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D1-REGION2021-EASTASIA | D1 Medicine area (primary): Region, 2021–2025: East Asia | 17.6% (389/2207; 95% CI 16.0%-19.2%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D1-REGION2021-EASTERNEUROPE | D1 Medicine area (primary): Region, 2021–2025: Eastern Europe | 29.3% (63/215; 95% CI 23.4%-35.7%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D1-REGION2021-LATINAMERICAOCEANIA | D1 Medicine area (primary): Region, 2021–2025: Latin America / Oceania | 39.3% (212/539; 95% CI 35.3%-43.5%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D1-REGION2021-MIDDLEEASTNORTHAFRICA | D1 Medicine area (primary): Region, 2021–2025: Middle East / North Africa | 30.4% (294/967; 95% CI 27.3%-33.3%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D1-REGION2021-NORTHAMERICA | D1 Medicine area (primary): Region, 2021–2025: North America | 34.9% (1302/3727; 95% CI 33.4%-36.4%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D1-REGION2021-SOUTHSOUTHEASTASIA | D1 Medicine area (primary): Region, 2021–2025: South/Southeast Asia | 26.5% (122/460; 95% CI 22.4%-30.5%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D1-REGION2021-SUBSAHARANAFRICA | D1 Medicine area (primary): Region, 2021–2025: Sub-Saharan Africa | 44.2% (19/43; 95% CI 29.5%-60.0%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D1-REGION2021-UNKNOWN | D1 Medicine area (primary): Region, 2021–2025: Unknown | 30.7% (127/414; 95% CI 26.1%-35.0%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D1-REGION2021-WESTERNEUROPE | D1 Medicine area (primary): Region, 2021–2025: Western Europe | 34.7% (1097/3161; 95% CI 33.1%-36.3%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D1-PUBLICATIO-RESEARCHARTICLE | D1 Medicine area (primary): Publication type, 2021–2025: Research Article | 32.9% (2321/7065; 95% CI 31.7%-33.9%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D1-PUBLICATIO-REVIEW | D1 Medicine area (primary): Publication type, 2021–2025: Review | 25.0% (969/3873; 95% CI 23.6%-26.3%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D1-PUBLICATIO-LETTER | D1 Medicine area (primary): Publication type, 2021–2025: Letter | 42.5% (156/367; 95% CI 37.6%-48.0%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D1-PUBLICATIO-EDITORIAL | D1 Medicine area (primary): Publication type, 2021–2025: Editorial | 37.8% (125/331; 95% CI 32.3%-42.9%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D1-PUBLICATIO-COMMENTARY | D1 Medicine area (primary): Publication type, 2021–2025: Commentary | 55.7% (54/97; 95% CI 46.4%-66.0%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D2-STANCEDIST-ALARM | D2 D1 minus Medicine (misc.): Stance distribution, 2021–2025: Alarm | 5.4% (549/10,180; 95% CI 5.0%-5.8%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D2-STANCEDIST-CAUTION | D2 D1 minus Medicine (misc.): Stance distribution, 2021–2025: Caution | 25.7% (2612/10,180; 95% CI 24.8%-26.5%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D2-STANCEDIST-NEUTRAL | D2 D1 minus Medicine (misc.): Stance distribution, 2021–2025: Neutral | 4.8% (492/10,180; 95% CI 4.4%-5.3%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D2-STANCEDIST-CAUTIOUSOPTIMISM | D2 D1 minus Medicine (misc.): Stance distribution, 2021–2025: Cautious Optimism | 62.9% (6402/10,180; 95% CI 61.9%-63.8%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D2-STANCEDIST-ADVOCACY | D2 D1 minus Medicine (misc.): Stance distribution, 2021–2025: Advocacy | 1.2% (125/10,180; 95% CI 1.0%-1.4%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D2-STANCEDIST-CRITICAL | D2 D1 minus Medicine (misc.): Stance distribution, 2021–2025: Critical | 31.1% (3161/10,180; 95% CI 30.1%-32.0%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D2-STANCEDIST-FAVOURABLE | D2 D1 minus Medicine (misc.): Stance distribution, 2021–2025: Favourable | 64.1% (6527/10,180; 95% CI 63.2%-65.0%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D2-TREND20212-CRITICAL | D2 D1 minus Medicine (misc.): Trend 2021–2025: Critical | ρ=+0.90 (P=.083); OR 1.085 per year (95% CI 1.049-1.122), P<.001 | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D2-TREND20212-ADVOCACY | D2 D1 minus Medicine (misc.): Trend 2021–2025: Advocacy | ρ=-0.90 (P=.083); OR 0.802 per year (95% CI 0.707-0.909), P<.001 | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D2-THEMETREND-PATIENTSAFETY | D2 D1 minus Medicine (misc.): Theme trend 2021–2025 (among critical): Patient safety | 60.4% to 69.1% (change +8.7 percentage points); ρ=+0.90 (P=.083); OR 1.107 per year (95% CI 1.042-1.177) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D2-THEMETREND-HALLUCINATIONERRORS | D2 D1 minus Medicine (misc.): Theme trend 2021–2025 (among critical): Hallucination / errors | 25.4% to 51.2% (change +25.8 percentage points); ρ=+0.80 (P=.133); OR 1.358 per year (95% CI 1.276-1.444) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D2-THEMETREND-GOVERNANCEREGULATION | D2 D1 minus Medicine (misc.): Theme trend 2021–2025 (among critical): Governance / regulation | 55.3% to 34.0% (change -21.3 percentage points); ρ=-0.90 (P=.083); OR 0.779 per year (95% CI 0.734-0.827) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D2-THEMETREND-ETHICSANDBIAS | D2 D1 minus Medicine (misc.): Theme trend 2021–2025 (among critical): Ethics & bias | 35.5% to 34.0% (change -1.5 percentage points); ρ=-0.60 (P=.350); OR 0.938 per year (95% CI 0.883-0.996) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D2-SPECIALTY2-RANGEN30CATEGORIES | D2 D1 minus Medicine (misc.): Specialty, 2021–2025: range (n≥30 categories) | Mental Health / Psychiatry 49.5% (153/309) to Cardiology 16.4% (73/445) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D2-SPECIALTY2-FDASPEARMAN | D2 D1 minus Medicine (misc.): Specialty, 2021–2025: FDA Spearman ρ | -0.60 (two-sided P=.008, n=18) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D2-SPECIALTYD-RADIOLOGYDIAGNOSTICIMAGI | D2 D1 minus Medicine (misc.): Specialty detail, 2021–2025: Radiology / Diagnostic Imaging | 21.2% (19.2-23.2) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D2-SPECIALTYD-PATHOLOGYLABORATORYMEDIC | D2 D1 minus Medicine (misc.): Specialty detail, 2021–2025: Pathology / Laboratory Medicine | 20.7% (16.2-25.2) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D2-SPECIALTYD-CARDIOLOGY | D2 D1 minus Medicine (misc.): Specialty detail, 2021–2025: Cardiology | 16.4% (13.1-19.7) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D2-SPECIALTYD-ONCOLOGY | D2 D1 minus Medicine (misc.): Specialty detail, 2021–2025: Oncology | 19.4% (16.9-21.7) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D2-SPECIALTYD-SURGERY | D2 D1 minus Medicine (misc.): Specialty detail, 2021–2025: Surgery | 29.4% (26.8-32.3) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D2-SPECIALTYD-OPHTHALMOLOGY | D2 D1 minus Medicine (misc.): Specialty detail, 2021–2025: Ophthalmology | 19.0% (15.6-22.0) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D2-SPECIALTYD-DERMATOLOGY | D2 D1 minus Medicine (misc.): Specialty detail, 2021–2025: Dermatology | 38.6% (32.5-45.1) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D2-SPECIALTYD-NEUROLOGYNEUROSCIENCE | D2 D1 minus Medicine (misc.): Specialty detail, 2021–2025: Neurology / Neuroscience | 24.6% (18.8-30.3) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D2-SPECIALTYD-MENTALHEALTHPSYCHIATRY | D2 D1 minus Medicine (misc.): Specialty detail, 2021–2025: Mental Health / Psychiatry | 49.5% (44.3-54.8) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D2-SPECIALTYD-INTERNALMEDICINEPRIMARYC | D2 D1 minus Medicine (misc.): Specialty detail, 2021–2025: Internal Medicine / Primary Care | 21.8% (18.8-24.7) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D2-SPECIALTYD-EMERGENCYMEDICINECRITICA | D2 D1 minus Medicine (misc.): Specialty detail, 2021–2025: Emergency Medicine / Critical Care | 27.5% (21.6-32.6) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D2-SPECIALTYD-PEDIATRICS | D2 D1 minus Medicine (misc.): Specialty detail, 2021–2025: Pediatrics | 24.7% (19.4-29.7) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D2-SPECIALTYD-OBSTETRICSGYNECOLOGY | D2 D1 minus Medicine (misc.): Specialty detail, 2021–2025: Obstetrics / Gynecology | 26.6% (19.6-33.3) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D2-SPECIALTYD-DENTISTRY | D2 D1 minus Medicine (misc.): Specialty detail, 2021–2025: Dentistry | 20.9% (14.4-28.5) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D2-SPECIALTYD-MEDICALINFORMATICSDIGITA | D2 D1 minus Medicine (misc.): Specialty detail, 2021–2025: Medical Informatics / Digital Health | 49.5% (47.6-51.5) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D2-SPECIALTYD-NURSING | D2 D1 minus Medicine (misc.): Specialty detail, 2021–2025: Nursing | 33.3% (19.2-47.4) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D2-SPECIALTYD-MEDICALEDUCATION | D2 D1 minus Medicine (misc.): Specialty detail, 2021–2025: Medical Education | 40.3% (35.5-45.6) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D2-SPECIALTYD-MULTIDISCIPLINARYOTHER | D2 D1 minus Medicine (misc.): Specialty detail, 2021–2025: Multidisciplinary / Other | 36.8% (27.1-46.4) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D2-REGION2021-EASTASIA | D2 D1 minus Medicine (misc.): Region, 2021–2025: East Asia | 18.4% (348/1896; 95% CI 16.7%-20.1%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D2-REGION2021-EASTERNEUROPE | D2 D1 minus Medicine (misc.): Region, 2021–2025: Eastern Europe | 32.5% (50/154; 95% CI 25.2%-39.9%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D2-REGION2021-LATINAMERICAOCEANIA | D2 D1 minus Medicine (misc.): Region, 2021–2025: Latin America / Oceania | 39.3% (184/468; 95% CI 35.2%-43.8%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D2-REGION2021-MIDDLEEASTNORTHAFRICA | D2 D1 minus Medicine (misc.): Region, 2021–2025: Middle East / North Africa | 30.0% (232/773; 95% CI 26.7%-33.2%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D2-REGION2021-NORTHAMERICA | D2 D1 minus Medicine (misc.): Region, 2021–2025: North America | 34.9% (1170/3348; 95% CI 33.3%-36.5%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D2-REGION2021-SOUTHSOUTHEASTASIA | D2 D1 minus Medicine (misc.): Region, 2021–2025: South/Southeast Asia | 27.7% (106/382; 95% CI 23.1%-32.0%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D2-REGION2021-SUBSAHARANAFRICA | D2 D1 minus Medicine (misc.): Region, 2021–2025: Sub-Saharan Africa | 46.3% (19/41; 95% CI 29.7%-60.6%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D2-REGION2021-UNKNOWN | D2 D1 minus Medicine (misc.): Region, 2021–2025: Unknown | 28.4% (97/341; 95% CI 24.1%-33.2%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D2-REGION2021-WESTERNEUROPE | D2 D1 minus Medicine (misc.): Region, 2021–2025: Western Europe | 34.4% (955/2777; 95% CI 32.6%-36.1%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D2-PUBLICATIO-RESEARCHARTICLE | D2 D1 minus Medicine (misc.): Publication type, 2021–2025: Research Article | 32.5% (1995/6133; 95% CI 31.4%-33.7%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D2-PUBLICATIO-REVIEW | D2 D1 minus Medicine (misc.): Publication type, 2021–2025: Review | 26.0% (872/3352; 95% CI 24.6%-27.4%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D2-PUBLICATIO-LETTER | D2 D1 minus Medicine (misc.): Publication type, 2021–2025: Letter | 43.3% (142/328; 95% CI 38.1%-48.2%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D2-PUBLICATIO-EDITORIAL | D2 D1 minus Medicine (misc.): Publication type, 2021–2025: Editorial | 37.5% (106/283; 95% CI 31.8%-42.8%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D2-PUBLICATIO-COMMENTARY | D2 D1 minus Medicine (misc.): Publication type, 2021–2025: Commentary | 54.8% (46/84; 95% CI 44.0%-65.5%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D3-STANCEDIST-ALARM | D3 broad health sciences: Stance distribution, 2021–2025: Alarm | 5.4% (684/12,711; 95% CI 5.0%-5.8%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D3-STANCEDIST-CAUTION | D3 broad health sciences: Stance distribution, 2021–2025: Caution | 25.6% (3250/12,711; 95% CI 24.9%-26.4%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D3-STANCEDIST-NEUTRAL | D3 broad health sciences: Stance distribution, 2021–2025: Neutral | 4.9% (627/12,711; 95% CI 4.5%-5.3%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D3-STANCEDIST-CAUTIOUSOPTIMISM | D3 broad health sciences: Stance distribution, 2021–2025: Cautious Optimism | 62.6% (7963/12,711; 95% CI 61.8%-63.4%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D3-STANCEDIST-ADVOCACY | D3 broad health sciences: Stance distribution, 2021–2025: Advocacy | 1.5% (187/12,711; 95% CI 1.3%-1.7%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D3-STANCEDIST-CRITICAL | D3 broad health sciences: Stance distribution, 2021–2025: Critical | 30.9% (3934/12,711; 95% CI 30.2%-31.7%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D3-STANCEDIST-FAVOURABLE | D3 broad health sciences: Stance distribution, 2021–2025: Favourable | 64.1% (8150/12,711; 95% CI 63.3%-64.9%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D3-TREND20212-CRITICAL | D3 broad health sciences: Trend 2021–2025: Critical | ρ=+0.90 (P=.083); OR 1.071 per year (95% CI 1.039-1.104), P<.001 | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D3-TREND20212-ADVOCACY | D3 broad health sciences: Trend 2021–2025: Advocacy | ρ=-0.90 (P=.083); OR 0.782 per year (95% CI 0.706-0.867), P<.001 | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D3-THEMETREND-PATIENTSAFETY | D3 broad health sciences: Theme trend 2021–2025 (among critical): Patient safety | 59.0% to 65.5% (change +6.5 percentage points); ρ=+0.90 (P=.083); OR 1.066 per year (95% CI 1.010-1.126) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D3-THEMETREND-HALLUCINATIONERRORS | D3 broad health sciences: Theme trend 2021–2025 (among critical): Hallucination / errors | 23.4% to 51.4% (change +28.1 percentage points); ρ=+0.80 (P=.133); OR 1.391 per year (95% CI 1.315-1.472) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D3-THEMETREND-GOVERNANCEREGULATION | D3 broad health sciences: Theme trend 2021–2025 (among critical): Governance / regulation | 54.5% to 31.7% (change -22.8 percentage points); ρ=-0.90 (P=.083); OR 0.762 per year (95% CI 0.722-0.805) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D3-THEMETREND-ETHICSANDBIAS | D3 broad health sciences: Theme trend 2021–2025 (among critical): Ethics & bias | 37.7% to 33.1% (change -4.6 percentage points); ρ=-0.80 (P=.133); OR 0.905 per year (95% CI 0.858-0.956) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D3-SPECIALTY2-RANGEN30CATEGORIES | D3 broad health sciences: Specialty, 2021–2025: range (n≥30 categories) | Mental Health / Psychiatry 50.0% (184/368) to Cardiology 16.3% (82/504) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D3-SPECIALTY2-FDASPEARMAN | D3 broad health sciences: Specialty, 2021–2025: FDA Spearman ρ | -0.63 (two-sided P=.005, n=18) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D3-SPECIALTYD-RADIOLOGYDIAGNOSTICIMAGI | D3 broad health sciences: Specialty detail, 2021–2025: Radiology / Diagnostic Imaging | 21.1% (19.1-23.0) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D3-SPECIALTYD-PATHOLOGYLABORATORYMEDIC | D3 broad health sciences: Specialty detail, 2021–2025: Pathology / Laboratory Medicine | 20.2% (16.2-24.9) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D3-SPECIALTYD-CARDIOLOGY | D3 broad health sciences: Specialty detail, 2021–2025: Cardiology | 16.3% (13.3-19.4) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D3-SPECIALTYD-ONCOLOGY | D3 broad health sciences: Specialty detail, 2021–2025: Oncology | 19.1% (16.8-21.5) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D3-SPECIALTYD-SURGERY | D3 broad health sciences: Specialty detail, 2021–2025: Surgery | 29.2% (26.5-31.9) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D3-SPECIALTYD-OPHTHALMOLOGY | D3 broad health sciences: Specialty detail, 2021–2025: Ophthalmology | 18.8% (15.5-21.9) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D3-SPECIALTYD-DERMATOLOGY | D3 broad health sciences: Specialty detail, 2021–2025: Dermatology | 38.1% (32.1-44.3) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D3-SPECIALTYD-NEUROLOGYNEUROSCIENCE | D3 broad health sciences: Specialty detail, 2021–2025: Neurology / Neuroscience | 23.2% (18.2-28.6) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D3-SPECIALTYD-MENTALHEALTHPSYCHIATRY | D3 broad health sciences: Specialty detail, 2021–2025: Mental Health / Psychiatry | 50.0% (44.7-55.2) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D3-SPECIALTYD-INTERNALMEDICINEPRIMARYC | D3 broad health sciences: Specialty detail, 2021–2025: Internal Medicine / Primary Care | 21.9% (19.4-24.9) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D3-SPECIALTYD-EMERGENCYMEDICINECRITICA | D3 broad health sciences: Specialty detail, 2021–2025: Emergency Medicine / Critical Care | 27.2% (22.8-32.2) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D3-SPECIALTYD-PEDIATRICS | D3 broad health sciences: Specialty detail, 2021–2025: Pediatrics | 24.2% (19.3-29.2) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D3-SPECIALTYD-OBSTETRICSGYNECOLOGY | D3 broad health sciences: Specialty detail, 2021–2025: Obstetrics / Gynecology | 25.8% (19.9-31.6) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D3-SPECIALTYD-DENTISTRY | D3 broad health sciences: Specialty detail, 2021–2025: Dentistry | 25.9% (22.5-29.7) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D3-SPECIALTYD-MEDICALINFORMATICSDIGITA | D3 broad health sciences: Specialty detail, 2021–2025: Medical Informatics / Digital Health | 46.8% (45.1-48.5) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D3-SPECIALTYD-NURSING | D3 broad health sciences: Specialty detail, 2021–2025: Nursing | 42.5% (36.0-48.9) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D3-SPECIALTYD-MEDICALEDUCATION | D3 broad health sciences: Specialty detail, 2021–2025: Medical Education | 36.2% (32.9-39.6) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D3-SPECIALTYD-MULTIDISCIPLINARYOTHER | D3 broad health sciences: Specialty detail, 2021–2025: Multidisciplinary / Other | 34.1% (25.7-42.1) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D3-REGION2021-EASTASIA | D3 broad health sciences: Region, 2021–2025: East Asia | 18.0% (428/2372; 95% CI 16.5%-19.7%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D3-REGION2021-EASTERNEUROPE | D3 broad health sciences: Region, 2021–2025: Eastern Europe | 29.4% (70/238; 95% CI 23.8%-35.3%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D3-REGION2021-LATINAMERICAOCEANIA | D3 broad health sciences: Region, 2021–2025: Latin America / Oceania | 38.9% (225/579; 95% CI 34.8%-43.0%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D3-REGION2021-MIDDLEEASTNORTHAFRICA | D3 broad health sciences: Region, 2021–2025: Middle East / North Africa | 30.8% (364/1181; 95% CI 28.2%-33.3%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D3-REGION2021-NORTHAMERICA | D3 broad health sciences: Region, 2021–2025: North America | 35.0% (1375/3926; 95% CI 33.6%-36.5%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D3-REGION2021-SOUTHSOUTHEASTASIA | D3 broad health sciences: Region, 2021–2025: South/Southeast Asia | 25.2% (140/555; 95% CI 21.9%-29.0%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D3-REGION2021-SUBSAHARANAFRICA | D3 broad health sciences: Region, 2021–2025: Sub-Saharan Africa | 44.7% (21/47; 95% CI 31.1%-59.6%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D3-REGION2021-UNKNOWN | D3 broad health sciences: Region, 2021–2025: Unknown | 31.9% (145/454; 95% CI 27.7%-36.2%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D3-REGION2021-WESTERNEUROPE | D3 broad health sciences: Region, 2021–2025: Western Europe | 34.7% (1166/3359; 95% CI 33.1%-36.3%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D3-PUBLICATIO-RESEARCHARTICLE | D3 broad health sciences: Publication type, 2021–2025: Research Article | 33.2% (2541/7649; 95% CI 32.2%-34.3%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D3-PUBLICATIO-REVIEW | D3 broad health sciences: Publication type, 2021–2025: Review | 24.7% (1048/4239; 95% CI 23.4%-26.1%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D3-PUBLICATIO-LETTER | D3 broad health sciences: Publication type, 2021–2025: Letter | 42.3% (159/376; 95% CI 37.2%-47.3%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D3-PUBLICATIO-EDITORIAL | D3 broad health sciences: Publication type, 2021–2025: Editorial | 37.5% (131/349; 95% CI 32.4%-42.4%) | 2021-2025 | outputs/B5/B5_long.csv |
| RES-B5X-D3-PUBLICATIO-COMMENTARY | D3 broad health sciences: Publication type, 2021–2025: Commentary | 56.1% (55/98; 95% CI 45.9%-66.3%) | 2021-2025 | outputs/B5/B5_long.csv |

### 20. B2 recovered vs retained records, and annual series by corpus

| ID | Item | Value | Window | Source |
|---|---|---|---|---|
| RES-B2RR-RETAINED-ALARM | Retained (production corpus): Alarm | 5.3% (749/14,058; 95% CI 5.0%-5.7%) | 2021-2025 | final/data/b2_recovered_vs_retained.csv |
| RES-B2RR-RETAINED-CAUTION | Retained (production corpus): Caution | 25.1% (3534/14,058; 95% CI 24.4%-25.9%) | 2021-2025 | final/data/b2_recovered_vs_retained.csv |
| RES-B2RR-RETAINED-NEUTRAL | Retained (production corpus): Neutral | 5.1% (721/14,058; 95% CI 4.8%-5.5%) | 2021-2025 | final/data/b2_recovered_vs_retained.csv |
| RES-B2RR-RETAINED-CAUTIOUSOPTIMISM | Retained (production corpus): Cautious Optimism | 62.9% (8836/14,058; 95% CI 62.0%-63.7%) | 2021-2025 | final/data/b2_recovered_vs_retained.csv |
| RES-B2RR-RETAINED-ADVOCACY | Retained (production corpus): Advocacy | 1.6% (218/14,058; 95% CI 1.4%-1.8%) | 2021-2025 | final/data/b2_recovered_vs_retained.csv |
| RES-B2RR-RETAINED-CRITICAL | Retained (production corpus): Critical | 30.5% (4283/14,058; 95% CI 29.7%-31.2%) | 2021-2025 | final/data/b2_recovered_vs_retained.csv |
| RES-B2RR-RECOVERE-ALARM | Recovered (B2): Alarm | 2.5% (62/2453; 95% CI 2.0%-3.1%) | 2021-2025 | final/data/b2_recovered_vs_retained.csv |
| RES-B2RR-RECOVERE-CAUTION | Recovered (B2): Caution | 10.1% (248/2453; 95% CI 8.9%-11.3%) | 2021-2025 | final/data/b2_recovered_vs_retained.csv |
| RES-B2RR-RECOVERE-NEUTRAL | Recovered (B2): Neutral | 5.1% (126/2453; 95% CI 4.2%-6.0%) | 2021-2025 | final/data/b2_recovered_vs_retained.csv |
| RES-B2RR-RECOVERE-CAUTIOUSOPTIMISM | Recovered (B2): Cautious Optimism | 81.1% (1990/2453; 95% CI 79.6%-82.6%) | 2021-2025 | final/data/b2_recovered_vs_retained.csv |
| RES-B2RR-RECOVERE-ADVOCACY | Recovered (B2): Advocacy | 1.1% (27/2453; 95% CI 0.7%-1.5%) | 2021-2025 | final/data/b2_recovered_vs_retained.csv |
| RES-B2RR-RECOVERE-CRITICAL | Recovered (B2): Critical | 12.6% (310/2453; 95% CI 11.3%-13.9%) | 2021-2025 | final/data/b2_recovered_vs_retained.csv |
| RES-B2ANN-A-ADVOCACY-2021 | B2 corpus (a) Production: Advocacy, 2021 | 2.9% (31/1063; 95% CI 1.9%-4.0%) | 2021-2025 | outputs/B2/B2_annual_by_corpus.csv |
| RES-B2ANN-A-ADVOCACY-2022 | B2 corpus (a) Production: Advocacy, 2022 | 2.0% (27/1343; 95% CI 1.3%-2.8%) | 2021-2025 | outputs/B2/B2_annual_by_corpus.csv |
| RES-B2ANN-A-ADVOCACY-2023 | B2 corpus (a) Production: Advocacy, 2023 | 1.9% (40/2054; 95% CI 1.4%-2.6%) | 2021-2025 | outputs/B2/B2_annual_by_corpus.csv |
| RES-B2ANN-A-ADVOCACY-2024 | B2 corpus (a) Production: Advocacy, 2024 | 1.5% (54/3700; 95% CI 1.1%-1.8%) | 2021-2025 | outputs/B2/B2_annual_by_corpus.csv |
| RES-B2ANN-A-ADVOCACY-2025 | B2 corpus (a) Production: Advocacy, 2025 | 1.1% (66/5898; 95% CI 0.9%-1.4%) | 2021-2025 | outputs/B2/B2_annual_by_corpus.csv |
| RES-B2ANN-A-CRITICAL-2021 | B2 corpus (a) Production: Critical, 2021 | 25.4% (270/1063; 95% CI 22.8%-28.0%) | 2021-2025 | outputs/B2/B2_annual_by_corpus.csv |
| RES-B2ANN-A-CRITICAL-2022 | B2 corpus (a) Production: Critical, 2022 | 24.8% (333/1343; 95% CI 22.6%-27.1%) | 2021-2025 | outputs/B2/B2_annual_by_corpus.csv |
| RES-B2ANN-A-CRITICAL-2023 | B2 corpus (a) Production: Critical, 2023 | 30.4% (624/2054; 95% CI 28.3%-32.5%) | 2021-2025 | outputs/B2/B2_annual_by_corpus.csv |
| RES-B2ANN-A-CRITICAL-2024 | B2 corpus (a) Production: Critical, 2024 | 33.2% (1228/3700; 95% CI 31.8%-34.8%) | 2021-2025 | outputs/B2/B2_annual_by_corpus.csv |
| RES-B2ANN-A-CRITICAL-2025 | B2 corpus (a) Production: Critical, 2025 | 31.0% (1828/5898; 95% CI 29.8%-32.3%) | 2021-2025 | outputs/B2/B2_annual_by_corpus.csv |
| RES-B2ANN-B-ADVOCACY-2021 | B2 corpus (b) Augmented: Advocacy, 2021 | 2.5% (33/1339; 95% CI 1.8%-3.4%) | 2021-2025 | outputs/B2/B2_annual_by_corpus.csv |
| RES-B2ANN-B-ADVOCACY-2022 | B2 corpus (b) Augmented: Advocacy, 2022 | 1.7% (29/1674; 95% CI 1.1%-2.4%) | 2021-2025 | outputs/B2/B2_annual_by_corpus.csv |
| RES-B2ANN-B-ADVOCACY-2023 | B2 corpus (b) Augmented: Advocacy, 2023 | 1.8% (45/2455; 95% CI 1.3%-2.4%) | 2021-2025 | outputs/B2/B2_annual_by_corpus.csv |
| RES-B2ANN-B-ADVOCACY-2024 | B2 corpus (b) Augmented: Advocacy, 2024 | 1.3% (57/4251; 95% CI 1.0%-1.7%) | 2021-2025 | outputs/B2/B2_annual_by_corpus.csv |
| RES-B2ANN-B-ADVOCACY-2025 | B2 corpus (b) Augmented: Advocacy, 2025 | 1.2% (81/6792; 95% CI 1.0%-1.5%) | 2021-2025 | outputs/B2/B2_annual_by_corpus.csv |
| RES-B2ANN-B-CRITICAL-2021 | B2 corpus (b) Augmented: Critical, 2021 | 22.0% (294/1339; 95% CI 19.7%-24.2%) | 2021-2025 | outputs/B2/B2_annual_by_corpus.csv |
| RES-B2ANN-B-CRITICAL-2022 | B2 corpus (b) Augmented: Critical, 2022 | 22.3% (373/1674; 95% CI 20.4%-24.3%) | 2021-2025 | outputs/B2/B2_annual_by_corpus.csv |
| RES-B2ANN-B-CRITICAL-2023 | B2 corpus (b) Augmented: Critical, 2023 | 27.7% (681/2455; 95% CI 25.9%-29.6%) | 2021-2025 | outputs/B2/B2_annual_by_corpus.csv |
| RES-B2ANN-B-CRITICAL-2024 | B2 corpus (b) Augmented: Critical, 2024 | 30.7% (1305/4251; 95% CI 29.4%-32.2%) | 2021-2025 | outputs/B2/B2_annual_by_corpus.csv |
| RES-B2ANN-B-CRITICAL-2025 | B2 corpus (b) Augmented: Critical, 2025 | 28.6% (1940/6792; 95% CI 27.5%-29.6%) | 2021-2025 | outputs/B2/B2_annual_by_corpus.csv |
| RES-B2ANN-C-ADVOCACY-2021 | B2 corpus (c) Precision-weighted augmented: Advocacy, 2021 | 2.6% (weighted 32.5/1265.4; 95% CI 1.8%-3.5%) | 2021-2025 | outputs/B2/B2_annual_by_corpus.csv |
| RES-B2ANN-C-ADVOCACY-2022 | B2 corpus (c) Precision-weighted augmented: Advocacy, 2022 | 1.8% (weighted 28.6/1607.8; 95% CI 1.1%-2.4%) | 2021-2025 | outputs/B2/B2_annual_by_corpus.csv |
| RES-B2ANN-C-ADVOCACY-2023 | B2 corpus (c) Precision-weighted augmented: Advocacy, 2023 | 1.9% (weighted 43.3/2321.3; 95% CI 1.4%-2.4%) | 2021-2025 | outputs/B2/B2_annual_by_corpus.csv |
| RES-B2ANN-C-ADVOCACY-2024 | B2 corpus (c) Precision-weighted augmented: Advocacy, 2024 | 1.4% (weighted 56.2/4104.1; 95% CI 1.0%-1.7%) | 2021-2025 | outputs/B2/B2_annual_by_corpus.csv |
| RES-B2ANN-C-ADVOCACY-2025 | B2 corpus (c) Precision-weighted augmented: Advocacy, 2025 | 1.2% (weighted 80.0/6732.4; 95% CI 1.0%-1.5%) | 2021-2025 | outputs/B2/B2_annual_by_corpus.csv |
| RES-B2ANN-C-CRITICAL-2021 | B2 corpus (c) Precision-weighted augmented: Critical, 2021 | 22.7% (weighted 287.6/1265.4; 95% CI 20.5%-25.1%) | 2021-2025 | outputs/B2/B2_annual_by_corpus.csv |
| RES-B2ANN-C-CRITICAL-2022 | B2 corpus (c) Precision-weighted augmented: Critical, 2022 | 22.7% (weighted 365.0/1607.8; 95% CI 20.8%-24.7%) | 2021-2025 | outputs/B2/B2_annual_by_corpus.csv |
| RES-B2ANN-C-CRITICAL-2023 | B2 corpus (c) Precision-weighted augmented: Critical, 2023 | 28.5% (weighted 662.0/2321.3; 95% CI 26.6%-30.4%) | 2021-2025 | outputs/B2/B2_annual_by_corpus.csv |
| RES-B2ANN-C-CRITICAL-2024 | B2 corpus (c) Precision-weighted augmented: Critical, 2024 | 31.3% (weighted 1284.5/4104.1; 95% CI 30.0%-32.8%) | 2021-2025 | outputs/B2/B2_annual_by_corpus.csv |
| RES-B2ANN-C-CRITICAL-2025 | B2 corpus (c) Precision-weighted augmented: Critical, 2025 | 28.7% (weighted 1932.5/6732.4; 95% CI 27.6%-29.8%) | 2021-2025 | outputs/B2/B2_annual_by_corpus.csv |
| RES-B2ANN-D-ADVOCACY-2021 | B2 corpus (d) Full-abstract corpus: Advocacy, 2021 | 2.7% (31/1169; 95% CI 1.8%-3.7%) | 2021-2025 | outputs/B2/B2_annual_by_corpus.csv |
| RES-B2ANN-D-ADVOCACY-2022 | B2 corpus (d) Full-abstract corpus: Advocacy, 2022 | 1.8% (26/1473; 95% CI 1.2%-2.5%) | 2021-2025 | outputs/B2/B2_annual_by_corpus.csv |
| RES-B2ANN-D-ADVOCACY-2023 | B2 corpus (d) Full-abstract corpus: Advocacy, 2023 | 1.8% (39/2188; 95% CI 1.3%-2.4%) | 2021-2025 | outputs/B2/B2_annual_by_corpus.csv |
| RES-B2ANN-D-ADVOCACY-2024 | B2 corpus (d) Full-abstract corpus: Advocacy, 2024 | 1.3% (52/3897; 95% CI 1.0%-1.7%) | 2021-2025 | outputs/B2/B2_annual_by_corpus.csv |
| RES-B2ANN-D-ADVOCACY-2025 | B2 corpus (d) Full-abstract corpus: Advocacy, 2025 | 1.0% (64/6197; 95% CI 0.8%-1.3%) | 2021-2025 | outputs/B2/B2_annual_by_corpus.csv |
| RES-B2ANN-D-CRITICAL-2021 | B2 corpus (d) Full-abstract corpus: Critical, 2021 | 24.0% (281/1169; 95% CI 21.6%-26.6%) | 2021-2025 | outputs/B2/B2_annual_by_corpus.csv |
| RES-B2ANN-D-CRITICAL-2022 | B2 corpus (d) Full-abstract corpus: Critical, 2022 | 24.2% (356/1473; 95% CI 21.9%-26.3%) | 2021-2025 | outputs/B2/B2_annual_by_corpus.csv |
| RES-B2ANN-D-CRITICAL-2023 | B2 corpus (d) Full-abstract corpus: Critical, 2023 | 29.9% (654/2188; 95% CI 27.9%-31.8%) | 2021-2025 | outputs/B2/B2_annual_by_corpus.csv |
| RES-B2ANN-D-CRITICAL-2024 | B2 corpus (d) Full-abstract corpus: Critical, 2024 | 32.9% (1283/3897; 95% CI 31.5%-34.4%) | 2021-2025 | outputs/B2/B2_annual_by_corpus.csv |
| RES-B2ANN-D-CRITICAL-2025 | B2 corpus (d) Full-abstract corpus: Critical, 2025 | 30.7% (1903/6197; 95% CI 29.6%-31.9%) | 2021-2025 | outputs/B2/B2_annual_by_corpus.csv |

### 21. B3 symmetric scale distribution, 2021-2025

| ID | Item | Value | Window | Source |
|---|---|---|---|---|
| RES-B3SYM-ALARM | Symmetric scale 2021-2025: Alarm | 5.3% (749/14,058) | 2021-2025 | outputs/B3/B3_symmetric_scale.csv |
| RES-B3SYM-CAUTION | Symmetric scale 2021-2025: Caution | 25.1% (3534/14,058) | 2021-2025 | outputs/B3/B3_symmetric_scale.csv |
| RES-B3SYM-NEUTRAL | Symmetric scale 2021-2025: Neutral | 5.1% (721/14,058) | 2021-2025 | outputs/B3/B3_symmetric_scale.csv |
| RES-B3SYM-CAUTIOUSOPTIMISMFLAGNO | Symmetric scale 2021-2025: Cautious Optimism (flag no) | 56.0% (7871/14,058) | 2021-2025 | outputs/B3/B3_symmetric_scale.csv |
| RES-B3SYM-STRONGENDORSEMENTFLAGYES | Symmetric scale 2021-2025: Strong endorsement (flag yes) | 8.4% (1179/14,058) | 2021-2025 | outputs/B3/B3_symmetric_scale.csv |
| RES-B3SYM-FAVOURABLEFLAGFAILED | Symmetric scale 2021-2025: Favourable, flag FAILED | 0.0% (4/14,058) | 2021-2025 | outputs/B3/B3_symmetric_scale.csv |

### 22. B6 MeSH and keyword re-fetch; term triangulation

| ID | Item | Value | Window | Source |
|---|---|---|---|---|
| RES-B6-COMP-2021 | Records with MeSH / with author keywords, 2021 | MeSH 88.5% (942/1064); keywords 68.4% (728/1064) | 2021-2025 | outputs/B6/B6_completeness_by_year.csv |
| RES-B6-COMP-2022 | Records with MeSH / with author keywords, 2022 | MeSH 85.3% (1147/1344); keywords 71.4% (959/1344) | 2021-2025 | outputs/B6/B6_completeness_by_year.csv |
| RES-B6-COMP-2023 | Records with MeSH / with author keywords, 2023 | MeSH 80.5% (1655/2055); keywords 71.0% (1460/2055) | 2021-2025 | outputs/B6/B6_completeness_by_year.csv |
| RES-B6-COMP-2024 | Records with MeSH / with author keywords, 2024 | MeSH 79.0% (2928/3704); keywords 73.4% (2720/3704) | 2021-2025 | outputs/B6/B6_completeness_by_year.csv |
| RES-B6-COMP-2025 | Records with MeSH / with author keywords, 2025 | MeSH 74.0% (4367/5899); keywords 81.6% (4815/5899) | 2021-2025 | outputs/B6/B6_completeness_by_year.csv |
| RES-B6-EMERG-01 | Emerging (2024-2025 vs 2021-2022) term 1: large language models | z=12.06; log-odds difference 3.23; records 1416 vs 0; more in 2024-2025 | 2021-2025 | outputs/B6/B6_emerging_terms_top30.csv |
| RES-B6-EMERG-02 | Emerging (2024-2025 vs 2021-2022) term 2: chatgpt | z=11.26; log-odds difference 3.41; records 1326 vs 0; more in 2024-2025 | 2021-2025 | outputs/B6/B6_emerging_terms_top30.csv |
| RES-B6-EMERG-03 | Emerging (2024-2025 vs 2021-2022) term 3: male | z=11.18; log-odds difference 0.78; records 2003 vs 212; more in 2024-2025 | 2021-2025 | outputs/B6/B6_emerging_terms_top30.csv |
| RES-B6-EMERG-04 | Emerging (2024-2025 vs 2021-2022) term 4: female | z=10.90; log-odds difference 0.69; records 2242 vs 261; more in 2024-2025 | 2021-2025 | outputs/B6/B6_emerging_terms_top30.csv |
| RES-B6-EMERG-05 | Emerging (2024-2025 vs 2021-2022) term 5: generative artificial intelligence | z=9.58; log-odds difference 3.26; records 910 vs 0; more in 2024-2025 | 2021-2025 | outputs/B6/B6_emerging_terms_top30.csv |
| RES-B6-EMERG-06 | Emerging (2024-2025 vs 2021-2022) term 6: adult | z=9.56; log-odds difference 0.87; records 1278 vs 122; more in 2024-2025 | 2021-2025 | outputs/B6/B6_emerging_terms_top30.csv |
| RES-B6-EMERG-07 | Emerging (2024-2025 vs 2021-2022) term 7: middle aged | z=9.34; log-odds difference 0.84; records 1282 vs 127; more in 2024-2025 | 2021-2025 | outputs/B6/B6_emerging_terms_top30.csv |
| RES-B6-EMERG-08 | Emerging (2024-2025 vs 2021-2022) term 8: surveys and questionnaires | z=8.30; log-odds difference 1.17; records 702 vs 48; more in 2024-2025 | 2021-2025 | outputs/B6/B6_emerging_terms_top30.csv |
| RES-B6-EMERG-09 | Emerging (2024-2025 vs 2021-2022) term 9: language | z=8.27; log-odds difference 2.36; records 536 vs 8; more in 2024-2025 | 2021-2025 | outputs/B6/B6_emerging_terms_top30.csv |
| RES-B6-EMERG-10 | Emerging (2024-2025 vs 2021-2022) term 10: large language model | z=7.08; log-odds difference 3.39; records 526 vs 0; more in 2024-2025 | 2021-2025 | outputs/B6/B6_emerging_terms_top30.csv |
| RES-B6-EMERG-11 | Emerging (2024-2025 vs 2021-2022) term 11: aged | z=5.53; log-odds difference 0.53; records 866 vs 119; more in 2024-2025 | 2021-2025 | outputs/B6/B6_emerging_terms_top30.csv |
| RES-B6-EMERG-12 | Emerging (2024-2025 vs 2021-2022) term 12: medical education | z=5.51; log-odds difference 1.55; records 253 vs 11; more in 2024-2025 | 2021-2025 | outputs/B6/B6_emerging_terms_top30.csv |
| RES-B6-EMERG-13 | Emerging (2024-2025 vs 2021-2022) term 13: ai | z=5.44; log-odds difference 0.76; records 490 vs 52; more in 2024-2025 | 2021-2025 | outputs/B6/B6_emerging_terms_top30.csv |
| RES-B6-EMERG-14 | Emerging (2024-2025 vs 2021-2022) term 14: attitude of health personnel | z=5.38; log-odds difference 1.53; records 243 vs 11; more in 2024-2025 | 2021-2025 | outputs/B6/B6_emerging_terms_top30.csv |
| RES-B6-EMERG-15 | Emerging (2024-2025 vs 2021-2022) term 15: comprehension | z=5.22; log-odds difference 2.94; records 244 vs 1; more in 2024-2025 | 2021-2025 | outputs/B6/B6_emerging_terms_top30.csv |
| RES-B6-EMERG-16 | Emerging (2024-2025 vs 2021-2022) term 16: chatbot | z=5.09; log-odds difference 1.74; records 205 vs 7; more in 2024-2025 | 2021-2025 | outputs/B6/B6_emerging_terms_top30.csv |
| RES-B6-EMERG-17 | Emerging (2024-2025 vs 2021-2022) term 17: cross-sectional studies | z=5.08; log-odds difference 0.78; records 415 vs 43; more in 2024-2025 | 2021-2025 | outputs/B6/B6_emerging_terms_top30.csv |
| RES-B6-EMERG-18 | Emerging (2024-2025 vs 2021-2022) term 18: patient education as topic | z=5.07; log-odds difference 3.35; records 266 vs 0; more in 2024-2025 | 2021-2025 | outputs/B6/B6_emerging_terms_top30.csv |
| RES-B6-EMERG-19 | Emerging (2024-2025 vs 2021-2022) term 19: natural language processing | z=4.99; log-odds difference 0.60; records 576 vs 73; more in 2024-2025 | 2021-2025 | outputs/B6/B6_emerging_terms_top30.csv |
| RES-B6-EMERG-20 | Emerging (2024-2025 vs 2021-2022) term 20: educational measurement | z=4.97; log-odds difference 3.00; records 226 vs 1; more in 2024-2025 | 2021-2025 | outputs/B6/B6_emerging_terms_top30.csv |
| RES-B6-EMERG-21 | Emerging (2024-2025 vs 2021-2022) term 21: clinical competence | z=4.85; log-odds difference 1.05; records 268 vs 21; more in 2024-2025 | 2021-2025 | outputs/B6/B6_emerging_terms_top30.csv |
| RES-B6-EMERG-22 | Emerging (2024-2025 vs 2021-2022) term 22: internet | z=4.68; log-odds difference 1.90; records 170 vs 5; more in 2024-2025 | 2021-2025 | outputs/B6/B6_emerging_terms_top30.csv |
| RES-B6-EMERG-23 | Emerging (2024-2025 vs 2021-2022) term 23: patient education | z=4.63; log-odds difference 3.33; records 220 vs 0; more in 2024-2025 | 2021-2025 | outputs/B6/B6_emerging_terms_top30.csv |
| RES-B6-EMERG-24 | Emerging (2024-2025 vs 2021-2022) term 24: young adult | z=4.34; log-odds difference 0.79; records 299 vs 31; more in 2024-2025 | 2021-2025 | outputs/B6/B6_emerging_terms_top30.csv |
| RES-B6-EMERG-25 | Emerging (2024-2025 vs 2021-2022) term 25: generative ai | z=4.26; log-odds difference 3.36; records 189 vs 0; more in 2024-2025 | 2021-2025 | outputs/B6/B6_emerging_terms_top30.csv |
| RES-B6-EMERG-26 | Emerging (2024-2025 vs 2021-2022) term 26: llm | z=3.85; log-odds difference 3.42; records 158 vs 0; more in 2024-2025 | 2021-2025 | outputs/B6/B6_emerging_terms_top30.csv |
| RES-B6-EMERG-27 | Emerging (2024-2025 vs 2021-2022) term 27: chatbots | z=3.69; log-odds difference 2.58; records 111 vs 1; more in 2024-2025 | 2021-2025 | outputs/B6/B6_emerging_terms_top30.csv |
| RES-B6-EMERG-28 | Emerging (2024-2025 vs 2021-2022) term 28: qualitative research | z=3.68; log-odds difference 0.92; records 179 vs 16; more in 2024-2025 | 2021-2025 | outputs/B6/B6_emerging_terms_top30.csv |
| RES-B6-EMERG-29 | Emerging (2024-2025 vs 2021-2022) term 29: health literacy | z=3.66; log-odds difference 2.68; records 112 vs 1; more in 2024-2025 | 2021-2025 | outputs/B6/B6_emerging_terms_top30.csv |
| RES-B6-EMERG-30 | Emerging (2024-2025 vs 2021-2022) term 30: practice guidelines as topic | z=3.49; log-odds difference 1.27; records 116 vs 7; more in 2024-2025 | 2021-2025 | outputs/B6/B6_emerging_terms_top30.csv |
| RES-B6-EMERG-31 | Emerging (2024-2025 vs 2021-2022) term 31: machine learning | z=-17.75; log-odds difference -0.73; records 1757 vs 864; more in 2021-2022 | 2021-2025 | outputs/B6/B6_emerging_terms_top30.csv |
| RES-B6-EMERG-32 | Emerging (2024-2025 vs 2021-2022) term 32: deep learning | z=-16.51; log-odds difference -0.76; records 1385 vs 702; more in 2021-2022 | 2021-2025 | outputs/B6/B6_emerging_terms_top30.csv |
| RES-B6-EMERG-33 | Emerging (2024-2025 vs 2021-2022) term 33: covid-19 | z=-15.04; log-odds difference -1.94; records 94 vs 160; more in 2021-2022 | 2021-2025 | outputs/B6/B6_emerging_terms_top30.csv |
| RES-B6-EMERG-34 | Emerging (2024-2025 vs 2021-2022) term 34: algorithms | z=-14.01; log-odds difference -0.89; records 658 vs 385; more in 2021-2022 | 2021-2025 | outputs/B6/B6_emerging_terms_top30.csv |
| RES-B6-EMERG-35 | Emerging (2024-2025 vs 2021-2022) term 35: neural networks, computer | z=-12.58; log-odds difference -1.23; records 226 vs 188; more in 2021-2022 | 2021-2025 | outputs/B6/B6_emerging_terms_top30.csv |
| RES-B6-EMERG-36 | Emerging (2024-2025 vs 2021-2022) term 36: delivery of health care | z=-12.46; log-odds difference -0.97; records 414 vs 264; more in 2021-2022 | 2021-2025 | outputs/B6/B6_emerging_terms_top30.csv |
| RES-B6-EMERG-37 | Emerging (2024-2025 vs 2021-2022) term 37: sars-cov-2 | z=-8.82; log-odds difference -1.59; records 56 vs 67; more in 2021-2022 | 2021-2025 | outputs/B6/B6_emerging_terms_top30.csv |
| RES-B6-EMERG-38 | Emerging (2024-2025 vs 2021-2022) term 38: radiography | z=-8.76; log-odds difference -1.33; records 89 vs 82; more in 2021-2022 | 2021-2025 | outputs/B6/B6_emerging_terms_top30.csv |
| RES-B6-EMERG-39 | Emerging (2024-2025 vs 2021-2022) term 39: retrospective studies | z=-8.49; log-odds difference -0.64; records 559 vs 253; more in 2021-2022 | 2021-2025 | outputs/B6/B6_emerging_terms_top30.csv |
| RES-B6-EMERG-40 | Emerging (2024-2025 vs 2021-2022) term 40: forecasting | z=-8.44; log-odds difference -1.49; records 61 vs 66; more in 2021-2022 | 2021-2025 | outputs/B6/B6_emerging_terms_top30.csv |
| RES-B6-EMERG-41 | Emerging (2024-2025 vs 2021-2022) term 41: pandemics | z=-8.30; log-odds difference -1.64; records 45 vs 57; more in 2021-2022 | 2021-2025 | outputs/B6/B6_emerging_terms_top30.csv |
| RES-B6-EMERG-42 | Emerging (2024-2025 vs 2021-2022) term 42: health facilities | z=-8.12; log-odds difference -1.83; records 32 vs 49; more in 2021-2022 | 2021-2025 | outputs/B6/B6_emerging_terms_top30.csv |
| RES-B6-EMERG-43 | Emerging (2024-2025 vs 2021-2022) term 43: radiologists | z=-8.04; log-odds difference -1.18; records 104 vs 82; more in 2021-2022 | 2021-2025 | outputs/B6/B6_emerging_terms_top30.csv |
| RES-B6-EMERG-44 | Emerging (2024-2025 vs 2021-2022) term 44: big data | z=-7.76; log-odds difference -1.46; records 54 vs 57; more in 2021-2022 | 2021-2025 | outputs/B6/B6_emerging_terms_top30.csv |
| RES-B6-EMERG-45 | Emerging (2024-2025 vs 2021-2022) term 45: convolutional neural network | z=-7.62; log-odds difference -1.51; records 48 vs 53; more in 2021-2022 | 2021-2025 | outputs/B6/B6_emerging_terms_top30.csv |
| RES-B6-EMERG-46 | Emerging (2024-2025 vs 2021-2022) term 46: computers | z=-6.66; log-odds difference -2.19; records 13 vs 29; more in 2021-2022 | 2021-2025 | outputs/B6/B6_emerging_terms_top30.csv |
| RES-B6-EMERG-47 | Emerging (2024-2025 vs 2021-2022) term 47: endoscopy | z=-6.57; log-odds difference -1.48; records 37 vs 40; more in 2021-2022 | 2021-2025 | outputs/B6/B6_emerging_terms_top30.csv |
| RES-B6-EMERG-48 | Emerging (2024-2025 vs 2021-2022) term 48: image processing, computer-assisted | z=-6.54; log-odds difference -0.80; records 185 vs 100; more in 2021-2022 | 2021-2025 | outputs/B6/B6_emerging_terms_top30.csv |
| RES-B6-EMERG-49 | Emerging (2024-2025 vs 2021-2022) term 49: humans | z=-6.46; log-odds difference -0.16; records 7195 vs 1985; more in 2021-2022 | 2021-2025 | outputs/B6/B6_emerging_terms_top30.csv |
| RES-B6-EMERG-50 | Emerging (2024-2025 vs 2021-2022) term 50: lung | z=-6.17; log-odds difference -1.53; records 30 vs 34; more in 2021-2022 | 2021-2025 | outputs/B6/B6_emerging_terms_top30.csv |
| RES-B6-EMERG-51 | Emerging (2024-2025 vs 2021-2022) term 51: diabetic retinopathy | z=-6.13; log-odds difference -1.13; records 68 vs 51; more in 2021-2022 | 2021-2025 | outputs/B6/B6_emerging_terms_top30.csv |
| RES-B6-EMERG-52 | Emerging (2024-2025 vs 2021-2022) term 52: diagnosis, computer-assisted | z=-6.09; log-odds difference -1.10; records 71 vs 52; more in 2021-2022 | 2021-2025 | outputs/B6/B6_emerging_terms_top30.csv |
| RES-B6-EMERG-53 | Emerging (2024-2025 vs 2021-2022) term 53: technology | z=-5.99; log-odds difference -1.02; records 85 vs 57; more in 2021-2022 | 2021-2025 | outputs/B6/B6_emerging_terms_top30.csv |
| RES-B6-EMERG-54 | Emerging (2024-2025 vs 2021-2022) term 54: prognosis | z=-5.83; log-odds difference -0.81; records 146 vs 79; more in 2021-2022 | 2021-2025 | outputs/B6/B6_emerging_terms_top30.csv |
| RES-B6-EMERG-55 | Emerging (2024-2025 vs 2021-2022) term 55: diagnostic imaging | z=-5.71; log-odds difference -0.81; records 138 vs 75; more in 2021-2022 | 2021-2025 | outputs/B6/B6_emerging_terms_top30.csv |
| RES-B6-EMERG-56 | Emerging (2024-2025 vs 2021-2022) term 56: tomography, x-ray computed | z=-5.63; log-odds difference -0.63; records 250 vs 113; more in 2021-2022 | 2021-2025 | outputs/B6/B6_emerging_terms_top30.csv |
| RES-B6-EMERG-57 | Emerging (2024-2025 vs 2021-2022) term 57: colonic polyps | z=-5.60; log-odds difference -1.38; records 33 vs 32; more in 2021-2022 | 2021-2025 | outputs/B6/B6_emerging_terms_top30.csv |
| RES-B6-EMERG-58 | Emerging (2024-2025 vs 2021-2022) term 58: diabetes mellitus | z=-5.53; log-odds difference -1.35; records 34 vs 32; more in 2021-2022 | 2021-2025 | outputs/B6/B6_emerging_terms_top30.csv |
| RES-B6-EMERG-59 | Emerging (2024-2025 vs 2021-2022) term 59: neural network | z=-5.47; log-odds difference -1.63; records 20 vs 25; more in 2021-2022 | 2021-2025 | outputs/B6/B6_emerging_terms_top30.csv |
| RES-B6-EMERG-60 | Emerging (2024-2025 vs 2021-2022) term 60: morals | z=-5.46; log-odds difference -1.77; records 16 vs 23; more in 2021-2022 | 2021-2025 | outputs/B6/B6_emerging_terms_top30.csv |
| RES-B6-STANCE-01 | Critical vs favourable term 1: delivery of health care | z=16.15; log-odds difference 1.15; records 477 vs 327; more in critical | 2021-2025 | outputs/B6/B6_stance_terms_top30.csv |
| RES-B6-STANCE-02 | Critical vs favourable term 2: ethics | z=14.06; log-odds difference 2.11; records 211 vs 54; more in critical | 2021-2025 | outputs/B6/B6_stance_terms_top30.csv |
| RES-B6-STANCE-03 | Critical vs favourable term 3: bias | z=12.81; log-odds difference 2.63; records 174 vs 26; more in critical | 2021-2025 | outputs/B6/B6_stance_terms_top30.csv |
| RES-B6-STANCE-04 | Critical vs favourable term 4: qualitative research | z=9.25; log-odds difference 1.30; records 134 vs 78; more in critical | 2021-2025 | outputs/B6/B6_stance_terms_top30.csv |
| RES-B6-STANCE-05 | Critical vs favourable term 5: health facilities | z=8.66; log-odds difference 1.86; records 85 vs 28; more in critical | 2021-2025 | outputs/B6/B6_stance_terms_top30.csv |
| RES-B6-STANCE-06 | Critical vs favourable term 6: trust | z=8.41; log-odds difference 1.38; records 104 vs 56; more in critical | 2021-2025 | outputs/B6/B6_stance_terms_top30.csv |
| RES-B6-STANCE-07 | Critical vs favourable term 7: mental health | z=8.10; log-odds difference 1.26; records 107 vs 65; more in critical | 2021-2025 | outputs/B6/B6_stance_terms_top30.csv |
| RES-B6-STANCE-08 | Critical vs favourable term 8: informed consent | z=7.99; log-odds difference 2.30; records 67 vs 14; more in critical | 2021-2025 | outputs/B6/B6_stance_terms_top30.csv |
| RES-B6-STANCE-09 | Critical vs favourable term 9: chatgpt | z=7.61; log-odds difference 0.40; records 599 vs 877; more in critical | 2021-2025 | outputs/B6/B6_stance_terms_top30.csv |
| RES-B6-STANCE-10 | Critical vs favourable term 10: privacy | z=7.43; log-odds difference 1.61; records 70 vs 30; more in critical | 2021-2025 | outputs/B6/B6_stance_terms_top30.csv |
| RES-B6-STANCE-11 | Critical vs favourable term 11: health equity | z=6.93; log-odds difference 1.63; records 60 vs 25; more in critical | 2021-2025 | outputs/B6/B6_stance_terms_top30.csv |
| RES-B6-STANCE-12 | Critical vs favourable term 12: health personnel | z=6.57; log-odds difference 0.97; records 101 vs 83; more in critical | 2021-2025 | outputs/B6/B6_stance_terms_top30.csv |
| RES-B6-STANCE-13 | Critical vs favourable term 13: decision making | z=6.57; log-odds difference 1.14; records 80 vs 55; more in critical | 2021-2025 | outputs/B6/B6_stance_terms_top30.csv |
| RES-B6-STANCE-14 | Critical vs favourable term 14: mental disorders | z=6.53; log-odds difference 1.30; records 67 vs 39; more in critical | 2021-2025 | outputs/B6/B6_stance_terms_top30.csv |
| RES-B6-STANCE-15 | Critical vs favourable term 15: confidentiality | z=6.41; log-odds difference 2.71; records 44 vs 6; more in critical | 2021-2025 | outputs/B6/B6_stance_terms_top30.csv |
| RES-B6-STANCE-16 | Critical vs favourable term 16: healthcare | z=6.03; log-odds difference 0.76; records 122 vs 123; more in critical | 2021-2025 | outputs/B6/B6_stance_terms_top30.csv |
| RES-B6-STANCE-17 | Critical vs favourable term 17: chatbot | z=6.02; log-odds difference 0.75; records 126 vs 129; more in critical | 2021-2025 | outputs/B6/B6_stance_terms_top30.csv |
| RES-B6-STANCE-18 | Critical vs favourable term 18: united states | z=5.91; log-odds difference 0.71; records 133 vs 142; more in critical | 2021-2025 | outputs/B6/B6_stance_terms_top30.csv |
| RES-B6-STANCE-19 | Critical vs favourable term 19: checklist | z=5.86; log-odds difference 2.37; records 36 vs 7; more in critical | 2021-2025 | outputs/B6/B6_stance_terms_top30.csv |
| RES-B6-STANCE-20 | Critical vs favourable term 20: bioethics | z=5.86; log-odds difference 2.37; records 36 vs 7; more in critical | 2021-2025 | outputs/B6/B6_stance_terms_top30.csv |
| RES-B6-STANCE-21 | Critical vs favourable term 21: regulation | z=5.65; log-odds difference 2.64; records 34 vs 5; more in critical | 2021-2025 | outputs/B6/B6_stance_terms_top30.csv |
| RES-B6-STANCE-22 | Critical vs favourable term 22: healthcare disparities | z=5.62; log-odds difference 2.07; records 34 vs 9; more in critical | 2021-2025 | outputs/B6/B6_stance_terms_top30.csv |
| RES-B6-STANCE-23 | Critical vs favourable term 23: morals | z=5.56; log-odds difference 3.20; records 37 vs 3; more in critical | 2021-2025 | outputs/B6/B6_stance_terms_top30.csv |
| RES-B6-STANCE-24 | Critical vs favourable term 24: medical ethics | z=5.56; log-odds difference 1.97; records 34 vs 10; more in critical | 2021-2025 | outputs/B6/B6_stance_terms_top30.csv |
| RES-B6-STANCE-25 | Critical vs favourable term 25: chatbots | z=5.53; log-odds difference 0.97; records 71 vs 58; more in critical | 2021-2025 | outputs/B6/B6_stance_terms_top30.csv |
| RES-B6-STANCE-26 | Critical vs favourable term 26: computer security | z=5.52; log-odds difference 2.05; records 33 vs 9; more in critical | 2021-2025 | outputs/B6/B6_stance_terms_top30.csv |
| RES-B6-STANCE-27 | Critical vs favourable term 27: health care | z=5.45; log-odds difference 0.98; records 68 vs 55; more in critical | 2021-2025 | outputs/B6/B6_stance_terms_top30.csv |
| RES-B6-STANCE-28 | Critical vs favourable term 28: implementation | z=5.37; log-odds difference 1.63; records 36 vs 15; more in critical | 2021-2025 | outputs/B6/B6_stance_terms_top30.csv |
| RES-B6-STANCE-29 | Critical vs favourable term 29: patient safety | z=5.30; log-odds difference 1.12; records 53 vs 37; more in critical | 2021-2025 | outputs/B6/B6_stance_terms_top30.csv |
| RES-B6-STANCE-30 | Critical vs favourable term 30: ai | z=5.26; log-odds difference 0.43; records 253 vs 359; more in critical | 2021-2025 | outputs/B6/B6_stance_terms_top30.csv |
| RES-B6-STANCE-31 | Critical vs favourable term 31: deep learning | z=-16.95; log-odds difference -0.95; records 358 vs 2054; more in favourable | 2021-2025 | outputs/B6/B6_stance_terms_top30.csv |
| RES-B6-STANCE-32 | Critical vs favourable term 32: retrospective studies | z=-7.88; log-odds difference -0.65; records 177 vs 751; more in favourable | 2021-2025 | outputs/B6/B6_stance_terms_top30.csv |
| RES-B6-STANCE-33 | Critical vs favourable term 33: sensitivity and specificity | z=-7.59; log-odds difference -0.90; records 80 vs 443; more in favourable | 2021-2025 | outputs/B6/B6_stance_terms_top30.csv |
| RES-B6-STANCE-34 | Critical vs favourable term 34: precision medicine | z=-6.66; log-odds difference -0.95; records 55 vs 320; more in favourable | 2021-2025 | outputs/B6/B6_stance_terms_top30.csv |
| RES-B6-STANCE-35 | Critical vs favourable term 35: tomography, x-ray computed | z=-6.32; log-odds difference -0.83; records 66 vs 340; more in favourable | 2021-2025 | outputs/B6/B6_stance_terms_top30.csv |
| RES-B6-STANCE-36 | Critical vs favourable term 36: predictive value of tests | z=-5.53; log-odds difference -1.27; records 20 vs 163; more in favourable | 2021-2025 | outputs/B6/B6_stance_terms_top30.csv |
| RES-B6-STANCE-37 | Critical vs favourable term 37: neural networks, computer | z=-5.26; log-odds difference -0.61; records 90 vs 367; more in favourable | 2021-2025 | outputs/B6/B6_stance_terms_top30.csv |
| RES-B6-STANCE-38 | Critical vs favourable term 38: convolutional neural network | z=-5.25; log-odds difference -1.83; records 8 vs 118; more in favourable | 2021-2025 | outputs/B6/B6_stance_terms_top30.csv |
| RES-B6-STANCE-39 | Critical vs favourable term 39: aged | z=-5.09; log-odds difference -0.37; records 238 vs 762; more in favourable | 2021-2025 | outputs/B6/B6_stance_terms_top30.csv |
| RES-B6-STANCE-40 | Critical vs favourable term 40: radiomics | z=-5.09; log-odds difference -1.48; records 12 vs 123; more in favourable | 2021-2025 | outputs/B6/B6_stance_terms_top30.csv |
| RES-B6-STANCE-41 | Critical vs favourable term 41: machine learning | z=-5.07; log-odds difference -0.21; records 812 vs 2182; more in favourable | 2021-2025 | outputs/B6/B6_stance_terms_top30.csv |
| RES-B6-STANCE-42 | Critical vs favourable term 42: forecasting | z=-4.91; log-odds difference -1.30; records 15 vs 126; more in favourable | 2021-2025 | outputs/B6/B6_stance_terms_top30.csv |
| RES-B6-STANCE-43 | Critical vs favourable term 43: radiographic image interpretation, computer-assisted | z=-4.82; log-odds difference -0.92; records 31 vs 175; more in favourable | 2021-2025 | outputs/B6/B6_stance_terms_top30.csv |
| RES-B6-STANCE-44 | Critical vs favourable term 44: drug discovery | z=-4.67; log-odds difference -2.47; records 3 vs 94; more in favourable | 2021-2025 | outputs/B6/B6_stance_terms_top30.csv |
| RES-B6-STANCE-45 | Critical vs favourable term 45: biomarkers | z=-4.43; log-odds difference -1.93; records 5 vs 83; more in favourable | 2021-2025 | outputs/B6/B6_stance_terms_top30.csv |
| RES-B6-STANCE-46 | Critical vs favourable term 46: prospective studies | z=-4.42; log-odds difference -0.58; records 71 vs 281; more in favourable | 2021-2025 | outputs/B6/B6_stance_terms_top30.csv |
| RES-B6-STANCE-47 | Critical vs favourable term 47: endoscopy | z=-4.27; log-odds difference -1.44; records 9 vs 88; more in favourable | 2021-2025 | outputs/B6/B6_stance_terms_top30.csv |
| RES-B6-STANCE-48 | Critical vs favourable term 48: magnetic resonance imaging | z=-4.26; log-odds difference -0.55; records 74 vs 284; more in favourable | 2021-2025 | outputs/B6/B6_stance_terms_top30.csv |
| RES-B6-STANCE-49 | Critical vs favourable term 49: prostatic neoplasms | z=-4.23; log-odds difference -0.93; records 23 vs 132; more in favourable | 2021-2025 | outputs/B6/B6_stance_terms_top30.csv |
| RES-B6-STANCE-50 | Critical vs favourable term 50: convolutional neural networks | z=-4.16; log-odds difference -1.23; records 12 vs 95; more in favourable | 2021-2025 | outputs/B6/B6_stance_terms_top30.csv |
| RES-B6-STANCE-51 | Critical vs favourable term 51: meta-analysis | z=-4.00; log-odds difference -1.29; records 10 vs 84; more in favourable | 2021-2025 | outputs/B6/B6_stance_terms_top30.csv |
| RES-B6-STANCE-52 | Critical vs favourable term 52: prognosis | z=-3.99; log-odds difference -0.61; records 52 vs 212; more in favourable | 2021-2025 | outputs/B6/B6_stance_terms_top30.csv |
| RES-B6-STANCE-53 | Critical vs favourable term 53: screening | z=-3.89; log-odds difference -1.33; records 9 vs 78; more in favourable | 2021-2025 | outputs/B6/B6_stance_terms_top30.csv |
| RES-B6-STANCE-54 | Critical vs favourable term 54: computed tomography angiography | z=-3.82; log-odds difference -1.11; records 13 vs 89; more in favourable | 2021-2025 | outputs/B6/B6_stance_terms_top30.csv |
| RES-B6-STANCE-55 | Critical vs favourable term 55: coronary angiography | z=-3.81; log-odds difference -1.87; records 4 vs 62; more in favourable | 2021-2025 | outputs/B6/B6_stance_terms_top30.csv |
| RES-B6-STANCE-56 | Critical vs favourable term 56: feasibility studies | z=-3.81; log-odds difference -1.37; records 8 vs 73; more in favourable | 2021-2025 | outputs/B6/B6_stance_terms_top30.csv |
| RES-B6-STANCE-57 | Critical vs favourable term 57: mass screening | z=-3.75; log-odds difference -0.96; records 17 vs 100; more in favourable | 2021-2025 | outputs/B6/B6_stance_terms_top30.csv |
| RES-B6-STANCE-58 | Critical vs favourable term 58: electrocardiography | z=-3.67; log-odds difference -1.15; records 11 vs 79; more in favourable | 2021-2025 | outputs/B6/B6_stance_terms_top30.csv |
| RES-B6-STANCE-59 | Critical vs favourable term 59: coronary artery disease | z=-3.62; log-odds difference -1.09; records 12 vs 81; more in favourable | 2021-2025 | outputs/B6/B6_stance_terms_top30.csv |
| RES-B6-STANCE-60 | Critical vs favourable term 60: diabetic retinopathy | z=-3.59; log-odds difference -0.82; records 22 vs 112; more in favourable | 2021-2025 | outputs/B6/B6_stance_terms_top30.csv |

### 23. Theme counts, generative share by specialty, forward-validation corpus silence

| ID | Item | Value | Window | Source |
|---|---|---|---|---|
| RES-THM-COUNT-PATIENTSAFETY-2021 | Patient safety: critical records with the theme, 2021 | 160 of 270 | 2021-2025 | outputs/T4_theme_counts.csv |
| RES-THM-COUNT-PATIENTSAFETY-2022 | Patient safety: critical records with the theme, 2022 | 210 of 333 | 2021-2025 | outputs/T4_theme_counts.csv |
| RES-THM-COUNT-PATIENTSAFETY-2023 | Patient safety: critical records with the theme, 2023 | 385 of 624 | 2021-2025 | outputs/T4_theme_counts.csv |
| RES-THM-COUNT-PATIENTSAFETY-2024 | Patient safety: critical records with the theme, 2024 | 813 of 1228 | 2021-2025 | outputs/T4_theme_counts.csv |
| RES-THM-COUNT-PATIENTSAFETY-2025 | Patient safety: critical records with the theme, 2025 | 1187 of 1828 | 2021-2025 | outputs/T4_theme_counts.csv |
| RES-THM-COUNT-HALLUCINATIONERRORS-2021 | Hallucination / errors: critical records with the theme, 2021 | 64 of 270 | 2021-2025 | outputs/T4_theme_counts.csv |
| RES-THM-COUNT-HALLUCINATIONERRORS-2022 | Hallucination / errors: critical records with the theme, 2022 | 73 of 333 | 2021-2025 | outputs/T4_theme_counts.csv |
| RES-THM-COUNT-HALLUCINATIONERRORS-2023 | Hallucination / errors: critical records with the theme, 2023 | 263 of 624 | 2021-2025 | outputs/T4_theme_counts.csv |
| RES-THM-COUNT-HALLUCINATIONERRORS-2024 | Hallucination / errors: critical records with the theme, 2024 | 637 of 1228 | 2021-2025 | outputs/T4_theme_counts.csv |
| RES-THM-COUNT-HALLUCINATIONERRORS-2025 | Hallucination / errors: critical records with the theme, 2025 | 934 of 1828 | 2021-2025 | outputs/T4_theme_counts.csv |
| RES-THM-COUNT-GOVERNANCEREGULATION-2021 | Governance / regulation: critical records with the theme, 2021 | 148 of 270 | 2021-2025 | outputs/T4_theme_counts.csv |
| RES-THM-COUNT-GOVERNANCEREGULATION-2022 | Governance / regulation: critical records with the theme, 2022 | 186 of 333 | 2021-2025 | outputs/T4_theme_counts.csv |
| RES-THM-COUNT-GOVERNANCEREGULATION-2023 | Governance / regulation: critical records with the theme, 2023 | 259 of 624 | 2021-2025 | outputs/T4_theme_counts.csv |
| RES-THM-COUNT-GOVERNANCEREGULATION-2024 | Governance / regulation: critical records with the theme, 2024 | 420 of 1228 | 2021-2025 | outputs/T4_theme_counts.csv |
| RES-THM-COUNT-GOVERNANCEREGULATION-2025 | Governance / regulation: critical records with the theme, 2025 | 580 of 1828 | 2021-2025 | outputs/T4_theme_counts.csv |
| RES-THM-COUNT-ETHICSANDBIAS-2021 | Ethics & bias: critical records with the theme, 2021 | 99 of 270 | 2021-2025 | outputs/T4_theme_counts.csv |
| RES-THM-COUNT-ETHICSANDBIAS-2022 | Ethics & bias: critical records with the theme, 2022 | 151 of 333 | 2021-2025 | outputs/T4_theme_counts.csv |
| RES-THM-COUNT-ETHICSANDBIAS-2023 | Ethics & bias: critical records with the theme, 2023 | 226 of 624 | 2021-2025 | outputs/T4_theme_counts.csv |
| RES-THM-COUNT-ETHICSANDBIAS-2024 | Ethics & bias: critical records with the theme, 2024 | 403 of 1228 | 2021-2025 | outputs/T4_theme_counts.csv |
| RES-THM-COUNT-ETHICSANDBIAS-2025 | Ethics & bias: critical records with the theme, 2025 | 604 of 1828 | 2021-2025 | outputs/T4_theme_counts.csv |
| RES-THM-COUNT-MEDICALEDUCATION-2021 | Medical education: critical records with the theme, 2021 | 10 of 270 | 2021-2025 | outputs/T4_theme_counts.csv |
| RES-THM-COUNT-MEDICALEDUCATION-2022 | Medical education: critical records with the theme, 2022 | 6 of 333 | 2021-2025 | outputs/T4_theme_counts.csv |
| RES-THM-COUNT-MEDICALEDUCATION-2023 | Medical education: critical records with the theme, 2023 | 58 of 624 | 2021-2025 | outputs/T4_theme_counts.csv |
| RES-THM-COUNT-MEDICALEDUCATION-2024 | Medical education: critical records with the theme, 2024 | 103 of 1228 | 2021-2025 | outputs/T4_theme_counts.csv |
| RES-THM-COUNT-MEDICALEDUCATION-2025 | Medical education: critical records with the theme, 2025 | 190 of 1828 | 2021-2025 | outputs/T4_theme_counts.csv |
| RES-THM-COUNT-DATAPRIVACY-2021 | Data privacy: critical records with the theme, 2021 | 24 of 270 | 2021-2025 | outputs/T4_theme_counts.csv |
| RES-THM-COUNT-DATAPRIVACY-2022 | Data privacy: critical records with the theme, 2022 | 28 of 333 | 2021-2025 | outputs/T4_theme_counts.csv |
| RES-THM-COUNT-DATAPRIVACY-2023 | Data privacy: critical records with the theme, 2023 | 41 of 624 | 2021-2025 | outputs/T4_theme_counts.csv |
| RES-THM-COUNT-DATAPRIVACY-2024 | Data privacy: critical records with the theme, 2024 | 84 of 1228 | 2021-2025 | outputs/T4_theme_counts.csv |
| RES-THM-COUNT-DATAPRIVACY-2025 | Data privacy: critical records with the theme, 2025 | 148 of 1828 | 2021-2025 | outputs/T4_theme_counts.csv |
| RES-THM-COUNT-COGNITIVEOFFLOADING-2021 | Cognitive offloading: critical records with the theme, 2021 | 21 of 270 | 2021-2025 | outputs/T4_theme_counts.csv |
| RES-THM-COUNT-COGNITIVEOFFLOADING-2022 | Cognitive offloading: critical records with the theme, 2022 | 19 of 333 | 2021-2025 | outputs/T4_theme_counts.csv |
| RES-THM-COUNT-COGNITIVEOFFLOADING-2023 | Cognitive offloading: critical records with the theme, 2023 | 35 of 624 | 2021-2025 | outputs/T4_theme_counts.csv |
| RES-THM-COUNT-COGNITIVEOFFLOADING-2024 | Cognitive offloading: critical records with the theme, 2024 | 59 of 1228 | 2021-2025 | outputs/T4_theme_counts.csv |
| RES-THM-COUNT-COGNITIVEOFFLOADING-2025 | Cognitive offloading: critical records with the theme, 2025 | 120 of 1828 | 2021-2025 | outputs/T4_theme_counts.csv |
| RES-THM-COUNT-EXISTENTIALTHREAT-2021 | Existential threat: critical records with the theme, 2021 | 18 of 270 | 2021-2025 | outputs/T4_theme_counts.csv |
| RES-THM-COUNT-EXISTENTIALTHREAT-2022 | Existential threat: critical records with the theme, 2022 | 14 of 333 | 2021-2025 | outputs/T4_theme_counts.csv |
| RES-THM-COUNT-EXISTENTIALTHREAT-2023 | Existential threat: critical records with the theme, 2023 | 37 of 624 | 2021-2025 | outputs/T4_theme_counts.csv |
| RES-THM-COUNT-EXISTENTIALTHREAT-2024 | Existential threat: critical records with the theme, 2024 | 39 of 1228 | 2021-2025 | outputs/T4_theme_counts.csv |
| RES-THM-COUNT-EXISTENTIALTHREAT-2025 | Existential threat: critical records with the theme, 2025 | 102 of 1828 | 2021-2025 | outputs/T4_theme_counts.csv |
| RES-THM-COUNT-REPLACEMENTFEARS-2021 | Replacement fears: critical records with the theme, 2021 | 17 of 270 | 2021-2025 | outputs/T4_theme_counts.csv |
| RES-THM-COUNT-REPLACEMENTFEARS-2022 | Replacement fears: critical records with the theme, 2022 | 17 of 333 | 2021-2025 | outputs/T4_theme_counts.csv |
| RES-THM-COUNT-REPLACEMENTFEARS-2023 | Replacement fears: critical records with the theme, 2023 | 27 of 624 | 2021-2025 | outputs/T4_theme_counts.csv |
| RES-THM-COUNT-REPLACEMENTFEARS-2024 | Replacement fears: critical records with the theme, 2024 | 50 of 1228 | 2021-2025 | outputs/T4_theme_counts.csv |
| RES-THM-COUNT-REPLACEMENTFEARS-2025 | Replacement fears: critical records with the theme, 2025 | 60 of 1828 | 2021-2025 | outputs/T4_theme_counts.csv |
| RES-THM-COUNT-OTHER-2021 | Other: critical records with the theme, 2021 | 13 of 270 | 2021-2025 | outputs/T4_theme_counts.csv |
| RES-THM-COUNT-OTHER-2022 | Other: critical records with the theme, 2022 | 15 of 333 | 2021-2025 | outputs/T4_theme_counts.csv |
| RES-THM-COUNT-OTHER-2023 | Other: critical records with the theme, 2023 | 14 of 624 | 2021-2025 | outputs/T4_theme_counts.csv |
| RES-THM-COUNT-OTHER-2024 | Other: critical records with the theme, 2024 | 21 of 1228 | 2021-2025 | outputs/T4_theme_counts.csv |
| RES-THM-COUNT-OTHER-2025 | Other: critical records with the theme, 2025 | 31 of 1828 | 2021-2025 | outputs/T4_theme_counts.csv |
| RES-SPC-GENSHARE-RADIOLOGYDIAGNOSTICIMAGI | Radiology / Diagnostic Imaging: generative-model share among abstract-present critical records | 32.2% (n=345) | 2021-2025 | final/data/specialty_fda.csv |
| RES-SPC-GENSHARE-PATHOLOGYLABORATORYMEDIC | Pathology / Laboratory Medicine: generative-model share among abstract-present critical records | 35.1% (n=77) | 2021-2025 | final/data/specialty_fda.csv |
| RES-SPC-GENSHARE-CARDIOLOGY | Cardiology: generative-model share among abstract-present critical records | 35.4% (n=79) | 2021-2025 | final/data/specialty_fda.csv |
| RES-SPC-GENSHARE-ONCOLOGY | Oncology: generative-model share among abstract-present critical records | 50.2% (n=219) | 2021-2025 | final/data/specialty_fda.csv |
| RES-SPC-GENSHARE-SURGERY | Surgery: generative-model share among abstract-present critical records | 77.5% (n=302) | 2021-2025 | final/data/specialty_fda.csv |
| RES-SPC-GENSHARE-OPHTHALMOLOGY | Ophthalmology: generative-model share among abstract-present critical records | 53.0% (n=117) | 2021-2025 | final/data/specialty_fda.csv |
| RES-SPC-GENSHARE-DERMATOLOGY | Dermatology: generative-model share among abstract-present critical records | 36.2% (n=80) | 2021-2025 | final/data/specialty_fda.csv |
| RES-SPC-GENSHARE-NEUROLOGYNEUROSCIENCE | Neurology / Neuroscience: generative-model share among abstract-present critical records | 60.3% (n=68) | 2021-2025 | final/data/specialty_fda.csv |
| RES-SPC-GENSHARE-MENTALHEALTHPSYCHIATRY | Mental Health / Psychiatry: generative-model share among abstract-present critical records | 55.1% (n=185) | 2021-2025 | final/data/specialty_fda.csv |
| RES-SPC-GENSHARE-INTERNALMEDICINEPRIMARYC | Internal Medicine / Primary Care: generative-model share among abstract-present critical records | 63.2% (n=185) | 2021-2025 | final/data/specialty_fda.csv |
| RES-SPC-GENSHARE-EMERGENCYMEDICINECRITICA | Emergency Medicine / Critical Care: generative-model share among abstract-present critical records | 52.9% (n=85) | 2021-2025 | final/data/specialty_fda.csv |
| RES-SPC-GENSHARE-PEDIATRICS | Pediatrics: generative-model share among abstract-present critical records | 58.8% (n=68) | 2021-2025 | final/data/specialty_fda.csv |
| RES-SPC-GENSHARE-OBSTETRICSGYNECOLOGY | Obstetrics / Gynecology: generative-model share among abstract-present critical records | 40.8% (n=49) | 2021-2025 | final/data/specialty_fda.csv |
| RES-SPC-GENSHARE-DENTISTRY | Dentistry: generative-model share among abstract-present critical records | 58.9% (n=141) | 2021-2025 | final/data/specialty_fda.csv |
| RES-SPC-GENSHARE-MEDICALINFORMATICSDIGITA | Medical Informatics / Digital Health: generative-model share among abstract-present critical records | 38.5% (n=1471) | 2021-2025 | final/data/specialty_fda.csv |
| RES-SPC-GENSHARE-NURSING | Nursing: generative-model share among abstract-present critical records | 34.1% (n=91) | 2021-2025 | final/data/specialty_fda.csv |
| RES-SPC-GENSHARE-MEDICALEDUCATION | Medical Education: generative-model share among abstract-present critical records | 59.0% (n=290) | 2021-2025 | final/data/specialty_fda.csv |
| RES-SPC-GENSHARE-MULTIDISCIPLINARYOTHER | Multidisciplinary / Other: generative-model share among abstract-present critical records | 14.5% (n=55) | 2021-2025 | final/data/specialty_fda.csv |
| RES-FV-SILENT-T1 | Tier 1: claims with corpus silence (classified too early/unfalsifiable) | 0 | evidence 2024-April 2026 | final/data/fv_tier_silent.csv |
| RES-FV-SILENT-T2 | Tier 2: claims with corpus silence (classified too early/unfalsifiable) | 8 | evidence 2024-April 2026 | final/data/fv_tier_silent.csv |
| RES-FV-SILENT-T3 | Tier 3: claims with corpus silence (classified too early/unfalsifiable) | 1 | evidence 2024-April 2026 | final/data/fv_tier_silent.csv |

## Validation (Table 1)


### Theme validation per theme; audit sampling manifest

| ID | Item | Value | Window | Source |
|---|---|---|---|---|
| VAL-TH-PT-200-SAFETYCLINICAL-PRECISIONUNWEIGHTED | Theme safety_clinical, N=200: precision (unweighted) | 0.820 (95% CI 0.752-0.882) | validation sample | outputs/A4_theme_primary_n200/theme_scores.md |
| VAL-TH-PT-200-SAFETYCLINICAL-RECALLUNWEIGHTED | Theme safety_clinical, N=200: recall (unweighted) | 0.955 (95% CI 0.913-0.991) | validation sample | outputs/A4_theme_primary_n200/theme_scores.md |
| VAL-TH-PT-200-SAFETYCLINICAL-F1UNWEIGHTED | Theme safety_clinical, N=200: F1 (unweighted) | 0.882 (95% CI 0.834-0.921) | validation sample | outputs/A4_theme_primary_n200/theme_scores.md |
| VAL-TH-PT-200-SAFETYCLINICAL-PRECISIONWEIGHTED | Theme safety_clinical, N=200: precision (weighted) | 0.812 (95% CI 0.730-0.888) | validation sample | outputs/A4_theme_primary_n200/theme_scores.md |
| VAL-TH-PT-200-SAFETYCLINICAL-RECALLWEIGHTED | Theme safety_clinical, N=200: recall (weighted) | 0.962 (95% CI 0.918-0.995) | validation sample | outputs/A4_theme_primary_n200/theme_scores.md |
| VAL-TH-PT-200-SAFETYCLINICAL-F1WEIGHTED | Theme safety_clinical, N=200: F1 (weighted) | 0.881 (95% CI 0.826-0.927) | validation sample | outputs/A4_theme_primary_n200/theme_scores.md |
| VAL-TH-PT-200-SAFETYCLINICAL-SUPPORT | Theme safety_clinical, N=200: human-positive records | 110 | validation sample | outputs/A4_theme_primary_n200/theme_scores.md |
| VAL-TH-PT-200-HALLUCINATION-PRECISIONUNWEIGHTED | Theme hallucination, N=200: precision (unweighted) | 0.844 (95% CI 0.757-0.919) | validation sample | outputs/A4_theme_primary_n200/theme_scores.md |
| VAL-TH-PT-200-HALLUCINATION-RECALLUNWEIGHTED | Theme hallucination, N=200: recall (unweighted) | 0.956 (95% CI 0.901-1.000) | validation sample | outputs/A4_theme_primary_n200/theme_scores.md |
| VAL-TH-PT-200-HALLUCINATION-F1UNWEIGHTED | Theme hallucination, N=200: F1 (unweighted) | 0.897 (95% CI 0.839-0.942) | validation sample | outputs/A4_theme_primary_n200/theme_scores.md |
| VAL-TH-PT-200-HALLUCINATION-PRECISIONWEIGHTED | Theme hallucination, N=200: precision (weighted) | 0.863 (95% CI 0.775-0.939) | validation sample | outputs/A4_theme_primary_n200/theme_scores.md |
| VAL-TH-PT-200-HALLUCINATION-RECALLWEIGHTED | Theme hallucination, N=200: recall (weighted) | 0.961 (95% CI 0.896-1.000) | validation sample | outputs/A4_theme_primary_n200/theme_scores.md |
| VAL-TH-PT-200-HALLUCINATION-F1WEIGHTED | Theme hallucination, N=200: F1 (weighted) | 0.909 (95% CI 0.851-0.954) | validation sample | outputs/A4_theme_primary_n200/theme_scores.md |
| VAL-TH-PT-200-HALLUCINATION-SUPPORT | Theme hallucination, N=200: human-positive records | 68 | validation sample | outputs/A4_theme_primary_n200/theme_scores.md |
| VAL-TH-PT-200-REGULATION-PRECISIONUNWEIGHTED | Theme regulation, N=200: precision (unweighted) | 0.872 (95% CI 0.802-0.939) | validation sample | outputs/A4_theme_primary_n200/theme_scores.md |
| VAL-TH-PT-200-REGULATION-RECALLUNWEIGHTED | Theme regulation, N=200: recall (unweighted) | 0.965 (95% CI 0.922-1.000) | validation sample | outputs/A4_theme_primary_n200/theme_scores.md |
| VAL-TH-PT-200-REGULATION-F1UNWEIGHTED | Theme regulation, N=200: F1 (unweighted) | 0.916 (95% CI 0.872-0.956) | validation sample | outputs/A4_theme_primary_n200/theme_scores.md |
| VAL-TH-PT-200-REGULATION-PRECISIONWEIGHTED | Theme regulation, N=200: precision (weighted) | 0.873 (95% CI 0.784-0.947) | validation sample | outputs/A4_theme_primary_n200/theme_scores.md |
| VAL-TH-PT-200-REGULATION-RECALLWEIGHTED | Theme regulation, N=200: recall (weighted) | 0.923 (95% CI 0.830-1.000) | validation sample | outputs/A4_theme_primary_n200/theme_scores.md |
| VAL-TH-PT-200-REGULATION-F1WEIGHTED | Theme regulation, N=200: F1 (weighted) | 0.897 (95% CI 0.829-0.952) | validation sample | outputs/A4_theme_primary_n200/theme_scores.md |
| VAL-TH-PT-200-REGULATION-SUPPORT | Theme regulation, N=200: human-positive records | 85 | validation sample | outputs/A4_theme_primary_n200/theme_scores.md |
| VAL-TH-PT-200-ETHICSBIAS-PRECISIONUNWEIGHTED | Theme ethics_bias, N=200: precision (unweighted) | 0.901 (95% CI 0.827-0.966) | validation sample | outputs/A4_theme_primary_n200/theme_scores.md |
| VAL-TH-PT-200-ETHICSBIAS-RECALLUNWEIGHTED | Theme ethics_bias, N=200: recall (unweighted) | 0.914 (95% CI 0.851-0.972) | validation sample | outputs/A4_theme_primary_n200/theme_scores.md |
| VAL-TH-PT-200-ETHICSBIAS-F1UNWEIGHTED | Theme ethics_bias, N=200: F1 (unweighted) | 0.908 (95% CI 0.855-0.954) | validation sample | outputs/A4_theme_primary_n200/theme_scores.md |
| VAL-TH-PT-200-ETHICSBIAS-PRECISIONWEIGHTED | Theme ethics_bias, N=200: precision (weighted) | 0.905 (95% CI 0.821-0.970) | validation sample | outputs/A4_theme_primary_n200/theme_scores.md |
| VAL-TH-PT-200-ETHICSBIAS-RECALLWEIGHTED | Theme ethics_bias, N=200: recall (weighted) | 0.941 (95% CI 0.869-0.990) | validation sample | outputs/A4_theme_primary_n200/theme_scores.md |
| VAL-TH-PT-200-ETHICSBIAS-F1WEIGHTED | Theme ethics_bias, N=200: F1 (weighted) | 0.922 (95% CI 0.867-0.968) | validation sample | outputs/A4_theme_primary_n200/theme_scores.md |
| VAL-TH-PT-200-ETHICSBIAS-SUPPORT | Theme ethics_bias, N=200: human-positive records | 70 | validation sample | outputs/A4_theme_primary_n200/theme_scores.md |
| VAL-TH-PT-200-EDUCATION-PRECISIONUNWEIGHTED | Theme education, N=200: precision (unweighted) [insufficient support] | 0.875 (95% CI 0.599-1.000) | validation sample | outputs/A4_theme_primary_n200/theme_scores.md |
| VAL-TH-PT-200-EDUCATION-RECALLUNWEIGHTED | Theme education, N=200: recall (unweighted) [insufficient support] | 0.875 (95% CI 0.571-1.000) | validation sample | outputs/A4_theme_primary_n200/theme_scores.md |
| VAL-TH-PT-200-EDUCATION-F1UNWEIGHTED | Theme education, N=200: F1 (unweighted) [insufficient support] | 0.875 (95% CI 0.615-1.000) | validation sample | outputs/A4_theme_primary_n200/theme_scores.md |
| VAL-TH-PT-200-EDUCATION-PRECISIONWEIGHTED | Theme education, N=200: precision (weighted) [insufficient support] | 0.875 (95% CI 0.558-1.000) | validation sample | outputs/A4_theme_primary_n200/theme_scores.md |
| VAL-TH-PT-200-EDUCATION-RECALLWEIGHTED | Theme education, N=200: recall (weighted) [insufficient support] | 0.932 (95% CI 0.724-1.000) | validation sample | outputs/A4_theme_primary_n200/theme_scores.md |
| VAL-TH-PT-200-EDUCATION-F1WEIGHTED | Theme education, N=200: F1 (weighted) [insufficient support] | 0.903 (95% CI 0.666-1.000) | validation sample | outputs/A4_theme_primary_n200/theme_scores.md |
| VAL-TH-PT-200-EDUCATION-SUPPORT | Theme education, N=200: human-positive records | 8 | validation sample | outputs/A4_theme_primary_n200/theme_scores.md |
| VAL-TH-PT-200-DATAPRIVACY-PRECISIONUNWEIGHTED | Theme data_privacy, N=200: precision (unweighted) | 0.737 (95% CI 0.524-0.941) | validation sample | outputs/A4_theme_primary_n200/theme_scores.md |
| VAL-TH-PT-200-DATAPRIVACY-RECALLUNWEIGHTED | Theme data_privacy, N=200: recall (unweighted) | 0.778 (95% CI 0.550-0.947) | validation sample | outputs/A4_theme_primary_n200/theme_scores.md |
| VAL-TH-PT-200-DATAPRIVACY-F1UNWEIGHTED | Theme data_privacy, N=200: F1 (unweighted) | 0.757 (95% CI 0.571-0.897) | validation sample | outputs/A4_theme_primary_n200/theme_scores.md |
| VAL-TH-PT-200-DATAPRIVACY-PRECISIONWEIGHTED | Theme data_privacy, N=200: precision (weighted) | 0.792 (95% CI 0.550-0.960) | validation sample | outputs/A4_theme_primary_n200/theme_scores.md |
| VAL-TH-PT-200-DATAPRIVACY-RECALLWEIGHTED | Theme data_privacy, N=200: recall (weighted) | 0.715 (95% CI 0.436-0.976) | validation sample | outputs/A4_theme_primary_n200/theme_scores.md |
| VAL-TH-PT-200-DATAPRIVACY-F1WEIGHTED | Theme data_privacy, N=200: F1 (weighted) | 0.752 (95% CI 0.505-0.912) | validation sample | outputs/A4_theme_primary_n200/theme_scores.md |
| VAL-TH-PT-200-DATAPRIVACY-SUPPORT | Theme data_privacy, N=200: human-positive records | 18 | validation sample | outputs/A4_theme_primary_n200/theme_scores.md |
| VAL-TH-PT-200-COGNITIVE-PRECISIONUNWEIGHTED | Theme cognitive, N=200: precision (unweighted) | 0.857 (95% CI 0.643-1.000) | validation sample | outputs/A4_theme_primary_n200/theme_scores.md |
| VAL-TH-PT-200-COGNITIVE-RECALLUNWEIGHTED | Theme cognitive, N=200: recall (unweighted) | 1.000 (95% CI 1.000-1.000) | validation sample | outputs/A4_theme_primary_n200/theme_scores.md |
| VAL-TH-PT-200-COGNITIVE-F1UNWEIGHTED | Theme cognitive, N=200: F1 (unweighted) | 0.923 (95% CI 0.783-1.000) | validation sample | outputs/A4_theme_primary_n200/theme_scores.md |
| VAL-TH-PT-200-COGNITIVE-PRECISIONWEIGHTED | Theme cognitive, N=200: precision (weighted) | 0.910 (95% CI 0.715-1.000) | validation sample | outputs/A4_theme_primary_n200/theme_scores.md |
| VAL-TH-PT-200-COGNITIVE-RECALLWEIGHTED | Theme cognitive, N=200: recall (weighted) | 1.000 (95% CI 1.000-1.000) | validation sample | outputs/A4_theme_primary_n200/theme_scores.md |
| VAL-TH-PT-200-COGNITIVE-F1WEIGHTED | Theme cognitive, N=200: F1 (weighted) | 0.953 (95% CI 0.834-1.000) | validation sample | outputs/A4_theme_primary_n200/theme_scores.md |
| VAL-TH-PT-200-COGNITIVE-SUPPORT | Theme cognitive, N=200: human-positive records | 12 | validation sample | outputs/A4_theme_primary_n200/theme_scores.md |
| VAL-TH-PT-200-EXISTENTIAL-PRECISIONUNWEIGHTED | Theme existential, N=200: precision (unweighted) [insufficient support] | 0.778 (95% CI 0.444-1.000) | validation sample | outputs/A4_theme_primary_n200/theme_scores.md |
| VAL-TH-PT-200-EXISTENTIAL-RECALLUNWEIGHTED | Theme existential, N=200: recall (unweighted) [insufficient support] | 0.778 (95% CI 0.500-1.000) | validation sample | outputs/A4_theme_primary_n200/theme_scores.md |
| VAL-TH-PT-200-EXISTENTIAL-F1UNWEIGHTED | Theme existential, N=200: F1 (unweighted) [insufficient support] | 0.778 (95% CI 0.499-1.000) | validation sample | outputs/A4_theme_primary_n200/theme_scores.md |
| VAL-TH-PT-200-EXISTENTIAL-PRECISIONWEIGHTED | Theme existential, N=200: precision (weighted) [insufficient support] | 0.844 (95% CI 0.477-1.000) | validation sample | outputs/A4_theme_primary_n200/theme_scores.md |
| VAL-TH-PT-200-EXISTENTIAL-RECALLWEIGHTED | Theme existential, N=200: recall (weighted) [insufficient support] | 0.763 (95% CI 0.354-1.000) | validation sample | outputs/A4_theme_primary_n200/theme_scores.md |
| VAL-TH-PT-200-EXISTENTIAL-F1WEIGHTED | Theme existential, N=200: F1 (weighted) [insufficient support] | 0.801 (95% CI 0.412-1.000) | validation sample | outputs/A4_theme_primary_n200/theme_scores.md |
| VAL-TH-PT-200-EXISTENTIAL-SUPPORT | Theme existential, N=200: human-positive records | 9 | validation sample | outputs/A4_theme_primary_n200/theme_scores.md |
| VAL-TH-PT-200-REPLACEMENT-PRECISIONUNWEIGHTED | Theme replacement, N=200: precision (unweighted) [insufficient support] | 0.667 (95% CI 0.333-1.000) | validation sample | outputs/A4_theme_primary_n200/theme_scores.md |
| VAL-TH-PT-200-REPLACEMENT-RECALLUNWEIGHTED | Theme replacement, N=200: recall (unweighted) [insufficient support] | 1.000 (95% CI 1.000-1.000) | validation sample | outputs/A4_theme_primary_n200/theme_scores.md |
| VAL-TH-PT-200-REPLACEMENT-F1UNWEIGHTED | Theme replacement, N=200: F1 (unweighted) [insufficient support] | 0.800 (95% CI 0.500-1.000) | validation sample | outputs/A4_theme_primary_n200/theme_scores.md |
| VAL-TH-PT-200-REPLACEMENT-PRECISIONWEIGHTED | Theme replacement, N=200: precision (weighted) [insufficient support] | 0.513 (95% CI 0.138-1.000) | validation sample | outputs/A4_theme_primary_n200/theme_scores.md |
| VAL-TH-PT-200-REPLACEMENT-RECALLWEIGHTED | Theme replacement, N=200: recall (weighted) [insufficient support] | 1.000 (95% CI 1.000-1.000) | validation sample | outputs/A4_theme_primary_n200/theme_scores.md |
| VAL-TH-PT-200-REPLACEMENT-F1WEIGHTED | Theme replacement, N=200: F1 (weighted) [insufficient support] | 0.678 (95% CI 0.243-1.000) | validation sample | outputs/A4_theme_primary_n200/theme_scores.md |
| VAL-TH-PT-200-REPLACEMENT-SUPPORT | Theme replacement, N=200: human-positive records | 6 | validation sample | outputs/A4_theme_primary_n200/theme_scores.md |
| VAL-TH-PT-200-OTHER-PRECISIONUNWEIGHTED | Theme other, N=200: precision (unweighted) [insufficient support] | 0.400 (95% CI 0.000-1.000) | validation sample | outputs/A4_theme_primary_n200/theme_scores.md |
| VAL-TH-PT-200-OTHER-RECALLUNWEIGHTED | Theme other, N=200: recall (unweighted) [insufficient support] | 0.667 (95% CI 0.000-1.000) | validation sample | outputs/A4_theme_primary_n200/theme_scores.md |
| VAL-TH-PT-200-OTHER-F1UNWEIGHTED | Theme other, N=200: F1 (unweighted) [insufficient support] | 0.500 (95% CI 0.000-0.909) | validation sample | outputs/A4_theme_primary_n200/theme_scores.md |
| VAL-TH-PT-200-OTHER-PRECISIONWEIGHTED | Theme other, N=200: precision (weighted) [insufficient support] | 0.330 (95% CI 0.000-1.000) | validation sample | outputs/A4_theme_primary_n200/theme_scores.md |
| VAL-TH-PT-200-OTHER-RECALLWEIGHTED | Theme other, N=200: recall (weighted) [insufficient support] | 0.644 (95% CI 0.000-1.000) | validation sample | outputs/A4_theme_primary_n200/theme_scores.md |
| VAL-TH-PT-200-OTHER-F1WEIGHTED | Theme other, N=200: F1 (weighted) [insufficient support] | 0.436 (95% CI 0.000-0.892) | validation sample | outputs/A4_theme_primary_n200/theme_scores.md |
| VAL-TH-PT-200-OTHER-SUPPORT | Theme other, N=200: human-positive records | 3 | validation sample | outputs/A4_theme_primary_n200/theme_scores.md |
| VAL-TH-PT-187-SAFETYCLINICAL-PRECISIONUNWEIGHTED | Theme safety_clinical, N=187: precision (unweighted) | 0.913 (95% CI 0.865-0.959) | validation sample | outputs/A4_theme/theme_scores.md |
| VAL-TH-PT-187-SAFETYCLINICAL-RECALLUNWEIGHTED | Theme safety_clinical, N=187: recall (unweighted) | 0.955 (95% CI 0.911-0.991) | validation sample | outputs/A4_theme/theme_scores.md |
| VAL-TH-PT-187-SAFETYCLINICAL-F1UNWEIGHTED | Theme safety_clinical, N=187: F1 (unweighted) | 0.933 (95% CI 0.899-0.962) | validation sample | outputs/A4_theme/theme_scores.md |
| VAL-TH-PT-187-SAFETYCLINICAL-PRECISIONWEIGHTED | Theme safety_clinical, N=187: precision (weighted) | 0.908 (95% CI 0.840-0.964) | validation sample | outputs/A4_theme/theme_scores.md |
| VAL-TH-PT-187-SAFETYCLINICAL-RECALLWEIGHTED | Theme safety_clinical, N=187: recall (weighted) | 0.961 (95% CI 0.917-0.995) | validation sample | outputs/A4_theme/theme_scores.md |
| VAL-TH-PT-187-SAFETYCLINICAL-F1WEIGHTED | Theme safety_clinical, N=187: F1 (weighted) | 0.933 (95% CI 0.892-0.967) | validation sample | outputs/A4_theme/theme_scores.md |
| VAL-TH-PT-187-SAFETYCLINICAL-SUPPORT | Theme safety_clinical, N=187: human-positive records | 110 | validation sample | outputs/A4_theme/theme_scores.md |
| VAL-TH-PT-187-HALLUCINATION-PRECISIONUNWEIGHTED | Theme hallucination, N=187: precision (unweighted) | 0.970 (95% CI 0.922-1.000) | validation sample | outputs/A4_theme/theme_scores.md |
| VAL-TH-PT-187-HALLUCINATION-RECALLUNWEIGHTED | Theme hallucination, N=187: recall (unweighted) | 0.956 (95% CI 0.895-1.000) | validation sample | outputs/A4_theme/theme_scores.md |
| VAL-TH-PT-187-HALLUCINATION-F1UNWEIGHTED | Theme hallucination, N=187: F1 (unweighted) | 0.963 (95% CI 0.924-0.993) | validation sample | outputs/A4_theme/theme_scores.md |
| VAL-TH-PT-187-HALLUCINATION-PRECISIONWEIGHTED | Theme hallucination, N=187: precision (weighted) | 0.987 (95% CI 0.964-1.000) | validation sample | outputs/A4_theme/theme_scores.md |
| VAL-TH-PT-187-HALLUCINATION-RECALLWEIGHTED | Theme hallucination, N=187: recall (weighted) | 0.962 (95% CI 0.891-1.000) | validation sample | outputs/A4_theme/theme_scores.md |
| VAL-TH-PT-187-HALLUCINATION-F1WEIGHTED | Theme hallucination, N=187: F1 (weighted) | 0.974 (95% CI 0.935-0.996) | validation sample | outputs/A4_theme/theme_scores.md |
| VAL-TH-PT-187-HALLUCINATION-SUPPORT | Theme hallucination, N=187: human-positive records | 68 | validation sample | outputs/A4_theme/theme_scores.md |
| VAL-TH-PT-187-REGULATION-PRECISIONUNWEIGHTED | Theme regulation, N=187: precision (unweighted) | 0.943 (95% CI 0.886-0.988) | validation sample | outputs/A4_theme/theme_scores.md |
| VAL-TH-PT-187-REGULATION-RECALLUNWEIGHTED | Theme regulation, N=187: recall (unweighted) | 0.965 (95% CI 0.920-1.000) | validation sample | outputs/A4_theme/theme_scores.md |
| VAL-TH-PT-187-REGULATION-F1UNWEIGHTED | Theme regulation, N=187: F1 (unweighted) | 0.953 (95% CI 0.917-0.982) | validation sample | outputs/A4_theme/theme_scores.md |
| VAL-TH-PT-187-REGULATION-PRECISIONWEIGHTED | Theme regulation, N=187: precision (weighted) | 0.961 (95% CI 0.910-0.995) | validation sample | outputs/A4_theme/theme_scores.md |
| VAL-TH-PT-187-REGULATION-RECALLWEIGHTED | Theme regulation, N=187: recall (weighted) | 0.924 (95% CI 0.831-1.000) | validation sample | outputs/A4_theme/theme_scores.md |
| VAL-TH-PT-187-REGULATION-F1WEIGHTED | Theme regulation, N=187: F1 (weighted) | 0.942 (95% CI 0.886-0.983) | validation sample | outputs/A4_theme/theme_scores.md |
| VAL-TH-PT-187-REGULATION-SUPPORT | Theme regulation, N=187: human-positive records | 85 | validation sample | outputs/A4_theme/theme_scores.md |
| VAL-TH-PT-187-ETHICSBIAS-PRECISIONUNWEIGHTED | Theme ethics_bias, N=187: precision (unweighted) | 0.914 (95% CI 0.847-0.975) | validation sample | outputs/A4_theme/theme_scores.md |
| VAL-TH-PT-187-ETHICSBIAS-RECALLUNWEIGHTED | Theme ethics_bias, N=187: recall (unweighted) | 0.914 (95% CI 0.844-0.972) | validation sample | outputs/A4_theme/theme_scores.md |
| VAL-TH-PT-187-ETHICSBIAS-F1UNWEIGHTED | Theme ethics_bias, N=187: F1 (unweighted) | 0.914 (95% CI 0.860-0.960) | validation sample | outputs/A4_theme/theme_scores.md |
| VAL-TH-PT-187-ETHICSBIAS-PRECISIONWEIGHTED | Theme ethics_bias, N=187: precision (weighted) | 0.921 (95% CI 0.846-0.985) | validation sample | outputs/A4_theme/theme_scores.md |
| VAL-TH-PT-187-ETHICSBIAS-RECALLWEIGHTED | Theme ethics_bias, N=187: recall (weighted) | 0.941 (95% CI 0.876-0.989) | validation sample | outputs/A4_theme/theme_scores.md |
| VAL-TH-PT-187-ETHICSBIAS-F1WEIGHTED | Theme ethics_bias, N=187: F1 (weighted) | 0.931 (95% CI 0.879-0.974) | validation sample | outputs/A4_theme/theme_scores.md |
| VAL-TH-PT-187-ETHICSBIAS-SUPPORT | Theme ethics_bias, N=187: human-positive records | 70 | validation sample | outputs/A4_theme/theme_scores.md |
| VAL-TH-PT-187-EDUCATION-PRECISIONUNWEIGHTED | Theme education, N=187: precision (unweighted) [insufficient support] | 0.875 (95% CI 0.583-1.000) | validation sample | outputs/A4_theme/theme_scores.md |
| VAL-TH-PT-187-EDUCATION-RECALLUNWEIGHTED | Theme education, N=187: recall (unweighted) [insufficient support] | 0.875 (95% CI 0.600-1.000) | validation sample | outputs/A4_theme/theme_scores.md |
| VAL-TH-PT-187-EDUCATION-F1UNWEIGHTED | Theme education, N=187: F1 (unweighted) [insufficient support] | 0.875 (95% CI 0.631-1.000) | validation sample | outputs/A4_theme/theme_scores.md |
| VAL-TH-PT-187-EDUCATION-PRECISIONWEIGHTED | Theme education, N=187: precision (weighted) [insufficient support] | 0.872 (95% CI 0.554-1.000) | validation sample | outputs/A4_theme/theme_scores.md |
| VAL-TH-PT-187-EDUCATION-RECALLWEIGHTED | Theme education, N=187: recall (weighted) [insufficient support] | 0.932 (95% CI 0.724-1.000) | validation sample | outputs/A4_theme/theme_scores.md |
| VAL-TH-PT-187-EDUCATION-F1WEIGHTED | Theme education, N=187: F1 (weighted) [insufficient support] | 0.901 (95% CI 0.662-1.000) | validation sample | outputs/A4_theme/theme_scores.md |
| VAL-TH-PT-187-EDUCATION-SUPPORT | Theme education, N=187: human-positive records | 8 | validation sample | outputs/A4_theme/theme_scores.md |
| VAL-TH-PT-187-DATAPRIVACY-PRECISIONUNWEIGHTED | Theme data_privacy, N=187: precision (unweighted) | 0.737 (95% CI 0.533-0.917) | validation sample | outputs/A4_theme/theme_scores.md |
| VAL-TH-PT-187-DATAPRIVACY-RECALLUNWEIGHTED | Theme data_privacy, N=187: recall (unweighted) | 0.778 (95% CI 0.571-1.000) | validation sample | outputs/A4_theme/theme_scores.md |
| VAL-TH-PT-187-DATAPRIVACY-F1UNWEIGHTED | Theme data_privacy, N=187: F1 (unweighted) | 0.757 (95% CI 0.585-0.889) | validation sample | outputs/A4_theme/theme_scores.md |
| VAL-TH-PT-187-DATAPRIVACY-PRECISIONWEIGHTED | Theme data_privacy, N=187: precision (weighted) | 0.788 (95% CI 0.552-0.956) | validation sample | outputs/A4_theme/theme_scores.md |
| VAL-TH-PT-187-DATAPRIVACY-RECALLWEIGHTED | Theme data_privacy, N=187: recall (weighted) | 0.711 (95% CI 0.419-1.000) | validation sample | outputs/A4_theme/theme_scores.md |
| VAL-TH-PT-187-DATAPRIVACY-F1WEIGHTED | Theme data_privacy, N=187: F1 (weighted) | 0.747 (95% CI 0.505-0.911) | validation sample | outputs/A4_theme/theme_scores.md |
| VAL-TH-PT-187-DATAPRIVACY-SUPPORT | Theme data_privacy, N=187: human-positive records | 18 | validation sample | outputs/A4_theme/theme_scores.md |
| VAL-TH-PT-187-COGNITIVE-PRECISIONUNWEIGHTED | Theme cognitive, N=187: precision (unweighted) | 0.857 (95% CI 0.647-1.000) | validation sample | outputs/A4_theme/theme_scores.md |
| VAL-TH-PT-187-COGNITIVE-RECALLUNWEIGHTED | Theme cognitive, N=187: recall (unweighted) | 1.000 (95% CI 1.000-1.000) | validation sample | outputs/A4_theme/theme_scores.md |
| VAL-TH-PT-187-COGNITIVE-F1UNWEIGHTED | Theme cognitive, N=187: F1 (unweighted) | 0.923 (95% CI 0.786-1.000) | validation sample | outputs/A4_theme/theme_scores.md |
| VAL-TH-PT-187-COGNITIVE-PRECISIONWEIGHTED | Theme cognitive, N=187: precision (weighted) | 0.908 (95% CI 0.723-1.000) | validation sample | outputs/A4_theme/theme_scores.md |
| VAL-TH-PT-187-COGNITIVE-RECALLWEIGHTED | Theme cognitive, N=187: recall (weighted) | 1.000 (95% CI 1.000-1.000) | validation sample | outputs/A4_theme/theme_scores.md |
| VAL-TH-PT-187-COGNITIVE-F1WEIGHTED | Theme cognitive, N=187: F1 (weighted) | 0.952 (95% CI 0.839-1.000) | validation sample | outputs/A4_theme/theme_scores.md |
| VAL-TH-PT-187-COGNITIVE-SUPPORT | Theme cognitive, N=187: human-positive records | 12 | validation sample | outputs/A4_theme/theme_scores.md |
| VAL-TH-PT-187-EXISTENTIAL-PRECISIONUNWEIGHTED | Theme existential, N=187: precision (unweighted) [insufficient support] | 0.778 (95% CI 0.444-1.000) | validation sample | outputs/A4_theme/theme_scores.md |
| VAL-TH-PT-187-EXISTENTIAL-RECALLUNWEIGHTED | Theme existential, N=187: recall (unweighted) [insufficient support] | 0.778 (95% CI 0.499-1.000) | validation sample | outputs/A4_theme/theme_scores.md |
| VAL-TH-PT-187-EXISTENTIAL-F1UNWEIGHTED | Theme existential, N=187: F1 (unweighted) [insufficient support] | 0.778 (95% CI 0.500-0.952) | validation sample | outputs/A4_theme/theme_scores.md |
| VAL-TH-PT-187-EXISTENTIAL-PRECISIONWEIGHTED | Theme existential, N=187: precision (weighted) [insufficient support] | 0.844 (95% CI 0.451-1.000) | validation sample | outputs/A4_theme/theme_scores.md |
| VAL-TH-PT-187-EXISTENTIAL-RECALLWEIGHTED | Theme existential, N=187: recall (weighted) [insufficient support] | 0.758 (95% CI 0.301-1.000) | validation sample | outputs/A4_theme/theme_scores.md |
| VAL-TH-PT-187-EXISTENTIAL-F1WEIGHTED | Theme existential, N=187: F1 (weighted) [insufficient support] | 0.799 (95% CI 0.394-0.983) | validation sample | outputs/A4_theme/theme_scores.md |
| VAL-TH-PT-187-EXISTENTIAL-SUPPORT | Theme existential, N=187: human-positive records | 9 | validation sample | outputs/A4_theme/theme_scores.md |
| VAL-TH-PT-187-REPLACEMENT-PRECISIONUNWEIGHTED | Theme replacement, N=187: precision (unweighted) [insufficient support] | 0.667 (95% CI 0.333-1.000) | validation sample | outputs/A4_theme/theme_scores.md |
| VAL-TH-PT-187-REPLACEMENT-RECALLUNWEIGHTED | Theme replacement, N=187: recall (unweighted) [insufficient support] | 1.000 (95% CI 1.000-1.000) | validation sample | outputs/A4_theme/theme_scores.md |
| VAL-TH-PT-187-REPLACEMENT-F1UNWEIGHTED | Theme replacement, N=187: F1 (unweighted) [insufficient support] | 0.800 (95% CI 0.500-1.000) | validation sample | outputs/A4_theme/theme_scores.md |
| VAL-TH-PT-187-REPLACEMENT-PRECISIONWEIGHTED | Theme replacement, N=187: precision (weighted) [insufficient support] | 0.509 (95% CI 0.122-1.000) | validation sample | outputs/A4_theme/theme_scores.md |
| VAL-TH-PT-187-REPLACEMENT-RECALLWEIGHTED | Theme replacement, N=187: recall (weighted) [insufficient support] | 1.000 (95% CI 1.000-1.000) | validation sample | outputs/A4_theme/theme_scores.md |
| VAL-TH-PT-187-REPLACEMENT-F1WEIGHTED | Theme replacement, N=187: F1 (weighted) [insufficient support] | 0.675 (95% CI 0.218-1.000) | validation sample | outputs/A4_theme/theme_scores.md |
| VAL-TH-PT-187-REPLACEMENT-SUPPORT | Theme replacement, N=187: human-positive records | 6 | validation sample | outputs/A4_theme/theme_scores.md |
| VAL-TH-PT-187-OTHER-PRECISIONUNWEIGHTED | Theme other, N=187: precision (unweighted) [insufficient support] | 0.400 (95% CI 0.000-1.000) | validation sample | outputs/A4_theme/theme_scores.md |
| VAL-TH-PT-187-OTHER-RECALLUNWEIGHTED | Theme other, N=187: recall (unweighted) [insufficient support] | 0.667 (95% CI 0.000-1.000) | validation sample | outputs/A4_theme/theme_scores.md |
| VAL-TH-PT-187-OTHER-F1UNWEIGHTED | Theme other, N=187: F1 (unweighted) [insufficient support] | 0.500 (95% CI 0.000-0.858) | validation sample | outputs/A4_theme/theme_scores.md |
| VAL-TH-PT-187-OTHER-PRECISIONWEIGHTED | Theme other, N=187: precision (weighted) [insufficient support] | 0.327 (95% CI 0.000-1.000) | validation sample | outputs/A4_theme/theme_scores.md |
| VAL-TH-PT-187-OTHER-RECALLWEIGHTED | Theme other, N=187: recall (weighted) [insufficient support] | 0.639 (95% CI 0.000-1.000) | validation sample | outputs/A4_theme/theme_scores.md |
| VAL-TH-PT-187-OTHER-F1WEIGHTED | Theme other, N=187: F1 (weighted) [insufficient support] | 0.432 (95% CI 0.000-0.883) | validation sample | outputs/A4_theme/theme_scores.md |
| VAL-TH-PT-187-OTHER-SUPPORT | Theme other, N=187: human-positive records | 3 | validation sample | outputs/A4_theme/theme_scores.md |
| VAL-PF-MAN-EX-F-2021 | Audit sampling: EX-F 2021: frame and sample | frame 275; sampled 15; sampling fraction 5.45% | 2021-2025 frame | coding/prefilter_sampling_manifest.csv |
| VAL-PF-MAN-EX-F-2022 | Audit sampling: EX-F 2022: frame and sample | frame 330; sampled 15; sampling fraction 4.55% | 2021-2025 frame | coding/prefilter_sampling_manifest.csv |
| VAL-PF-MAN-EX-F-2023 | Audit sampling: EX-F 2023: frame and sample | frame 401; sampled 15; sampling fraction 3.74% | 2021-2025 frame | coding/prefilter_sampling_manifest.csv |
| VAL-PF-MAN-EX-F-2024 | Audit sampling: EX-F 2024: frame and sample | frame 551; sampled 15; sampling fraction 2.72% | 2021-2025 frame | coding/prefilter_sampling_manifest.csv |
| VAL-PF-MAN-EX-F-2025 | Audit sampling: EX-F 2025: frame and sample | frame 892; sampled 15; sampling fraction 1.68% | 2021-2025 frame | coding/prefilter_sampling_manifest.csv |
| VAL-PF-MAN-EX-S-2021 | Audit sampling: EX-S 2021: frame and sample | frame 9839; sampled 45; sampling fraction 0.46% | 2021-2025 frame | coding/prefilter_sampling_manifest.csv |
| VAL-PF-MAN-EX-S-2022 | Audit sampling: EX-S 2022: frame and sample | frame 11,435; sampled 45; sampling fraction 0.39% | 2021-2025 frame | coding/prefilter_sampling_manifest.csv |
| VAL-PF-MAN-EX-S-2023 | Audit sampling: EX-S 2023: frame and sample | frame 11,647; sampled 45; sampling fraction 0.39% | 2021-2025 frame | coding/prefilter_sampling_manifest.csv |
| VAL-PF-MAN-EX-S-2024 | Audit sampling: EX-S 2024: frame and sample | frame 15,081; sampled 45; sampling fraction 0.30% | 2021-2025 frame | coding/prefilter_sampling_manifest.csv |
| VAL-PF-MAN-EX-S-2025 | Audit sampling: EX-S 2025: frame and sample | frame 22,036; sampled 45; sampling fraction 0.20% | 2021-2025 frame | coding/prefilter_sampling_manifest.csv |
| VAL-PF-MAN-RET-2021 | Audit sampling: RET 2021: frame and sample | frame 1061; sampled 10; sampling fraction 0.94% | 2021-2025 frame | coding/prefilter_sampling_manifest.csv |
| VAL-PF-MAN-RET-2022 | Audit sampling: RET 2022: frame and sample | frame 1342; sampled 10; sampling fraction 0.75% | 2021-2025 frame | coding/prefilter_sampling_manifest.csv |
| VAL-PF-MAN-RET-2023 | Audit sampling: RET 2023: frame and sample | frame 2051; sampled 10; sampling fraction 0.49% | 2021-2025 frame | coding/prefilter_sampling_manifest.csv |
| VAL-PF-MAN-RET-2024 | Audit sampling: RET 2024: frame and sample | frame 3698; sampled 10; sampling fraction 0.27% | 2021-2025 frame | coding/prefilter_sampling_manifest.csv |
| VAL-PF-MAN-RET-2025 | Audit sampling: RET 2025: frame and sample | frame 5885; sampled 10; sampling fraction 0.17% | 2021-2025 frame | coding/prefilter_sampling_manifest.csv |
| VAL-PF-MAN-PILOT-any | Audit sampling: PILOT any: frame and sample | frame 200; sampled 20; sampling fraction 10.00% | 2021-2025 frame | coding/prefilter_sampling_manifest.csv |

### Confusion matrices and cell-level audit estimates (Multimedia Appendix 3)

| ID | Item | Value | Window | Source |
|---|---|---|---|---|
| VAL-ST-CM225-ALARM-ALARM | Stance n=225: human Alarm, model Alarm | 31 | validation sample | final/data/stance_confusion_inscope225.csv |
| VAL-ST-CM225-ALARM-CAUTION | Stance n=225: human Alarm, model Caution | 4 | validation sample | final/data/stance_confusion_inscope225.csv |
| VAL-ST-CM225-ALARM-NEUTRAL | Stance n=225: human Alarm, model Neutral | 0 | validation sample | final/data/stance_confusion_inscope225.csv |
| VAL-ST-CM225-ALARM-CAUTIOUSOPTIMISM | Stance n=225: human Alarm, model Cautious Optimism | 1 | validation sample | final/data/stance_confusion_inscope225.csv |
| VAL-ST-CM225-ALARM-ADVOCACY | Stance n=225: human Alarm, model Advocacy | 0 | validation sample | final/data/stance_confusion_inscope225.csv |
| VAL-ST-CM225-CAUTION-ALARM | Stance n=225: human Caution, model Alarm | 8 | validation sample | final/data/stance_confusion_inscope225.csv |
| VAL-ST-CM225-CAUTION-CAUTION | Stance n=225: human Caution, model Caution | 33 | validation sample | final/data/stance_confusion_inscope225.csv |
| VAL-ST-CM225-CAUTION-NEUTRAL | Stance n=225: human Caution, model Neutral | 3 | validation sample | final/data/stance_confusion_inscope225.csv |
| VAL-ST-CM225-CAUTION-CAUTIOUSOPTIMISM | Stance n=225: human Caution, model Cautious Optimism | 14 | validation sample | final/data/stance_confusion_inscope225.csv |
| VAL-ST-CM225-CAUTION-ADVOCACY | Stance n=225: human Caution, model Advocacy | 0 | validation sample | final/data/stance_confusion_inscope225.csv |
| VAL-ST-CM225-NEUTRAL-ALARM | Stance n=225: human Neutral, model Alarm | 0 | validation sample | final/data/stance_confusion_inscope225.csv |
| VAL-ST-CM225-NEUTRAL-CAUTION | Stance n=225: human Neutral, model Caution | 1 | validation sample | final/data/stance_confusion_inscope225.csv |
| VAL-ST-CM225-NEUTRAL-NEUTRAL | Stance n=225: human Neutral, model Neutral | 10 | validation sample | final/data/stance_confusion_inscope225.csv |
| VAL-ST-CM225-NEUTRAL-CAUTIOUSOPTIMISM | Stance n=225: human Neutral, model Cautious Optimism | 3 | validation sample | final/data/stance_confusion_inscope225.csv |
| VAL-ST-CM225-NEUTRAL-ADVOCACY | Stance n=225: human Neutral, model Advocacy | 0 | validation sample | final/data/stance_confusion_inscope225.csv |
| VAL-ST-CM225-CAUTIOUSOPTIMISM-ALARM | Stance n=225: human Cautious Optimism, model Alarm | 1 | validation sample | final/data/stance_confusion_inscope225.csv |
| VAL-ST-CM225-CAUTIOUSOPTIMISM-CAUTION | Stance n=225: human Cautious Optimism, model Caution | 12 | validation sample | final/data/stance_confusion_inscope225.csv |
| VAL-ST-CM225-CAUTIOUSOPTIMISM-NEUTRAL | Stance n=225: human Cautious Optimism, model Neutral | 10 | validation sample | final/data/stance_confusion_inscope225.csv |
| VAL-ST-CM225-CAUTIOUSOPTIMISM-CAUTIOUSOPTIMISM | Stance n=225: human Cautious Optimism, model Cautious Optimism | 61 | validation sample | final/data/stance_confusion_inscope225.csv |
| VAL-ST-CM225-CAUTIOUSOPTIMISM-ADVOCACY | Stance n=225: human Cautious Optimism, model Advocacy | 9 | validation sample | final/data/stance_confusion_inscope225.csv |
| VAL-ST-CM225-ADVOCACY-ALARM | Stance n=225: human Advocacy, model Alarm | 0 | validation sample | final/data/stance_confusion_inscope225.csv |
| VAL-ST-CM225-ADVOCACY-CAUTION | Stance n=225: human Advocacy, model Caution | 0 | validation sample | final/data/stance_confusion_inscope225.csv |
| VAL-ST-CM225-ADVOCACY-NEUTRAL | Stance n=225: human Advocacy, model Neutral | 0 | validation sample | final/data/stance_confusion_inscope225.csv |
| VAL-ST-CM225-ADVOCACY-CAUTIOUSOPTIMISM | Stance n=225: human Advocacy, model Cautious Optimism | 7 | validation sample | final/data/stance_confusion_inscope225.csv |
| VAL-ST-CM225-ADVOCACY-ADVOCACY | Stance n=225: human Advocacy, model Advocacy | 17 | validation sample | final/data/stance_confusion_inscope225.csv |
| VAL-ST-S18C-ALARM | Stance in scope: Alarm exact / adjacent / boundary-crossing | n=36; exact 31 (86.1%); adjacent 4 (11.1%); boundary-crossing 1 | validation sample | final/data/stance_confusion_inscope225.csv |
| VAL-ST-S18C-CAUTION | Stance in scope: Caution exact / adjacent / boundary-crossing | n=58; exact 33 (56.9%); adjacent 11 (19.0%); boundary-crossing 14 | validation sample | final/data/stance_confusion_inscope225.csv |
| VAL-ST-S18C-NEUTRAL | Stance in scope: Neutral exact / adjacent / boundary-crossing | n=14; exact 10 (71.4%); adjacent 4 (28.6%); boundary-crossing not applicable | validation sample | final/data/stance_confusion_inscope225.csv |
| VAL-ST-S18C-CAUTIOUSOPTIMISM | Stance in scope: Cautious Optimism exact / adjacent / boundary-crossing | n=93; exact 61 (65.6%); adjacent 19 (20.4%); boundary-crossing 13 | validation sample | final/data/stance_confusion_inscope225.csv |
| VAL-ST-S18C-ADVOCACY | Stance in scope: Advocacy exact / adjacent / boundary-crossing | n=24; exact 17 (70.8%); adjacent 7 (29.2%); boundary-crossing 0 | validation sample | final/data/stance_confusion_inscope225.csv |
| VAL-ST-CM300-ALARM-ALARM | Stance n=300: human Alarm, model Alarm | 31 | validation sample | final/data/stance_confusion_all300.csv |
| VAL-ST-CM300-ALARM-CAUTION | Stance n=300: human Alarm, model Caution | 4 | validation sample | final/data/stance_confusion_all300.csv |
| VAL-ST-CM300-ALARM-NEUTRAL | Stance n=300: human Alarm, model Neutral | 0 | validation sample | final/data/stance_confusion_all300.csv |
| VAL-ST-CM300-ALARM-CAUTIOUSOPTIMISM | Stance n=300: human Alarm, model Cautious Optimism | 1 | validation sample | final/data/stance_confusion_all300.csv |
| VAL-ST-CM300-ALARM-ADVOCACY | Stance n=300: human Alarm, model Advocacy | 0 | validation sample | final/data/stance_confusion_all300.csv |
| VAL-ST-CM300-CAUTION-ALARM | Stance n=300: human Caution, model Alarm | 8 | validation sample | final/data/stance_confusion_all300.csv |
| VAL-ST-CM300-CAUTION-CAUTION | Stance n=300: human Caution, model Caution | 34 | validation sample | final/data/stance_confusion_all300.csv |
| VAL-ST-CM300-CAUTION-NEUTRAL | Stance n=300: human Caution, model Neutral | 3 | validation sample | final/data/stance_confusion_all300.csv |
| VAL-ST-CM300-CAUTION-CAUTIOUSOPTIMISM | Stance n=300: human Caution, model Cautious Optimism | 14 | validation sample | final/data/stance_confusion_all300.csv |
| VAL-ST-CM300-CAUTION-ADVOCACY | Stance n=300: human Caution, model Advocacy | 0 | validation sample | final/data/stance_confusion_all300.csv |
| VAL-ST-CM300-NEUTRAL-ALARM | Stance n=300: human Neutral, model Alarm | 0 | validation sample | final/data/stance_confusion_all300.csv |
| VAL-ST-CM300-NEUTRAL-CAUTION | Stance n=300: human Neutral, model Caution | 10 | validation sample | final/data/stance_confusion_all300.csv |
| VAL-ST-CM300-NEUTRAL-NEUTRAL | Stance n=300: human Neutral, model Neutral | 57 | validation sample | final/data/stance_confusion_all300.csv |
| VAL-ST-CM300-NEUTRAL-CAUTIOUSOPTIMISM | Stance n=300: human Neutral, model Cautious Optimism | 17 | validation sample | final/data/stance_confusion_all300.csv |
| VAL-ST-CM300-NEUTRAL-ADVOCACY | Stance n=300: human Neutral, model Advocacy | 4 | validation sample | final/data/stance_confusion_all300.csv |
| VAL-ST-CM300-CAUTIOUSOPTIMISM-ALARM | Stance n=300: human Cautious Optimism, model Alarm | 1 | validation sample | final/data/stance_confusion_all300.csv |
| VAL-ST-CM300-CAUTIOUSOPTIMISM-CAUTION | Stance n=300: human Cautious Optimism, model Caution | 12 | validation sample | final/data/stance_confusion_all300.csv |
| VAL-ST-CM300-CAUTIOUSOPTIMISM-NEUTRAL | Stance n=300: human Cautious Optimism, model Neutral | 10 | validation sample | final/data/stance_confusion_all300.csv |
| VAL-ST-CM300-CAUTIOUSOPTIMISM-CAUTIOUSOPTIMISM | Stance n=300: human Cautious Optimism, model Cautious Optimism | 61 | validation sample | final/data/stance_confusion_all300.csv |
| VAL-ST-CM300-CAUTIOUSOPTIMISM-ADVOCACY | Stance n=300: human Cautious Optimism, model Advocacy | 9 | validation sample | final/data/stance_confusion_all300.csv |
| VAL-ST-CM300-ADVOCACY-ALARM | Stance n=300: human Advocacy, model Alarm | 0 | validation sample | final/data/stance_confusion_all300.csv |
| VAL-ST-CM300-ADVOCACY-CAUTION | Stance n=300: human Advocacy, model Caution | 0 | validation sample | final/data/stance_confusion_all300.csv |
| VAL-ST-CM300-ADVOCACY-NEUTRAL | Stance n=300: human Advocacy, model Neutral | 0 | validation sample | final/data/stance_confusion_all300.csv |
| VAL-ST-CM300-ADVOCACY-CAUTIOUSOPTIMISM | Stance n=300: human Advocacy, model Cautious Optimism | 7 | validation sample | final/data/stance_confusion_all300.csv |
| VAL-ST-CM300-ADVOCACY-ADVOCACY | Stance n=300: human Advocacy, model Advocacy | 17 | validation sample | final/data/stance_confusion_all300.csv |
| VAL-CM-PF3-HUMANDISCO-MODELDISCO | T1_confusion_3x3.csv: human:discourse x model:discourse | 14 | validation sample | outputs/T1_confusion_3x3.csv |
| VAL-CM-PF3-HUMANDISCO-MODELEVALU | T1_confusion_3x3.csv: human:discourse x model:evaluative | 1 | validation sample | outputs/T1_confusion_3x3.csv |
| VAL-CM-PF3-HUMANDISCO-MODELAPPLI | T1_confusion_3x3.csv: human:discourse x model:application | 7 | validation sample | outputs/T1_confusion_3x3.csv |
| VAL-CM-PF3-HUMANDISCO-ROWTOTAL | T1_confusion_3x3.csv: human:discourse x row_total | 22 | validation sample | outputs/T1_confusion_3x3.csv |
| VAL-CM-PF3-HUMANEVALU-MODELDISCO | T1_confusion_3x3.csv: human:evaluative x model:discourse | 0 | validation sample | outputs/T1_confusion_3x3.csv |
| VAL-CM-PF3-HUMANEVALU-MODELEVALU | T1_confusion_3x3.csv: human:evaluative x model:evaluative | 5 | validation sample | outputs/T1_confusion_3x3.csv |
| VAL-CM-PF3-HUMANEVALU-MODELAPPLI | T1_confusion_3x3.csv: human:evaluative x model:application | 11 | validation sample | outputs/T1_confusion_3x3.csv |
| VAL-CM-PF3-HUMANEVALU-ROWTOTAL | T1_confusion_3x3.csv: human:evaluative x row_total | 16 | validation sample | outputs/T1_confusion_3x3.csv |
| VAL-CM-PF3-HUMANAPPLI-MODELDISCO | T1_confusion_3x3.csv: human:application x model:discourse | 5 | validation sample | outputs/T1_confusion_3x3.csv |
| VAL-CM-PF3-HUMANAPPLI-MODELEVALU | T1_confusion_3x3.csv: human:application x model:evaluative | 5 | validation sample | outputs/T1_confusion_3x3.csv |
| VAL-CM-PF3-HUMANAPPLI-MODELAPPLI | T1_confusion_3x3.csv: human:application x model:application | 152 | validation sample | outputs/T1_confusion_3x3.csv |
| VAL-CM-PF3-HUMANAPPLI-ROWTOTAL | T1_confusion_3x3.csv: human:application x row_total | 162 | validation sample | outputs/T1_confusion_3x3.csv |
| VAL-CM-PF3-COLTOTAL-MODELDISCO | T1_confusion_3x3.csv: col_total x model:discourse | 19 | validation sample | outputs/T1_confusion_3x3.csv |
| VAL-CM-PF3-COLTOTAL-MODELEVALU | T1_confusion_3x3.csv: col_total x model:evaluative | 11 | validation sample | outputs/T1_confusion_3x3.csv |
| VAL-CM-PF3-COLTOTAL-MODELAPPLI | T1_confusion_3x3.csv: col_total x model:application | 170 | validation sample | outputs/T1_confusion_3x3.csv |
| VAL-CM-PF3-COLTOTAL-ROWTOTAL | T1_confusion_3x3.csv: col_total x row_total | 200 | validation sample | outputs/T1_confusion_3x3.csv |
| VAL-CM-FM-CONFABULAT-CONFABULAT | T3_confusion_failure_mode.csv: confabulation x confabulation | 7 | validation sample | outputs/T3_confusion_failure_mode.csv |
| VAL-CM-FM-CONFABULAT-MISCLASSIF | T3_confusion_failure_mode.csv: confabulation x misclassification | 1 | validation sample | outputs/T3_confusion_failure_mode.csv |
| VAL-CM-FM-CONFABULAT-BOTH | T3_confusion_failure_mode.csv: confabulation x both | 2 | validation sample | outputs/T3_confusion_failure_mode.csv |
| VAL-CM-FM-CONFABULAT-NONEORUNCL | T3_confusion_failure_mode.csv: confabulation x none_or_unclear | 0 | validation sample | outputs/T3_confusion_failure_mode.csv |
| VAL-CM-FM-MISCLASSIF-CONFABULAT | T3_confusion_failure_mode.csv: misclassification x confabulation | 5 | validation sample | outputs/T3_confusion_failure_mode.csv |
| VAL-CM-FM-MISCLASSIF-MISCLASSIF | T3_confusion_failure_mode.csv: misclassification x misclassification | 26 | validation sample | outputs/T3_confusion_failure_mode.csv |
| VAL-CM-FM-MISCLASSIF-BOTH | T3_confusion_failure_mode.csv: misclassification x both | 9 | validation sample | outputs/T3_confusion_failure_mode.csv |
| VAL-CM-FM-MISCLASSIF-NONEORUNCL | T3_confusion_failure_mode.csv: misclassification x none_or_unclear | 2 | validation sample | outputs/T3_confusion_failure_mode.csv |
| VAL-CM-FM-BOTH-CONFABULAT | T3_confusion_failure_mode.csv: both x confabulation | 2 | validation sample | outputs/T3_confusion_failure_mode.csv |
| VAL-CM-FM-BOTH-MISCLASSIF | T3_confusion_failure_mode.csv: both x misclassification | 0 | validation sample | outputs/T3_confusion_failure_mode.csv |
| VAL-CM-FM-BOTH-BOTH | T3_confusion_failure_mode.csv: both x both | 11 | validation sample | outputs/T3_confusion_failure_mode.csv |
| VAL-CM-FM-BOTH-NONEORUNCL | T3_confusion_failure_mode.csv: both x none_or_unclear | 0 | validation sample | outputs/T3_confusion_failure_mode.csv |
| VAL-CM-FM-NONEORUNCL-CONFABULAT | T3_confusion_failure_mode.csv: none_or_unclear x confabulation | 6 | validation sample | outputs/T3_confusion_failure_mode.csv |
| VAL-CM-FM-NONEORUNCL-MISCLASSIF | T3_confusion_failure_mode.csv: none_or_unclear x misclassification | 6 | validation sample | outputs/T3_confusion_failure_mode.csv |
| VAL-CM-FM-NONEORUNCL-BOTH | T3_confusion_failure_mode.csv: none_or_unclear x both | 0 | validation sample | outputs/T3_confusion_failure_mode.csv |
| VAL-CM-FM-NONEORUNCL-NONEORUNCL | T3_confusion_failure_mode.csv: none_or_unclear x none_or_unclear | 31 | validation sample | outputs/T3_confusion_failure_mode.csv |
| VAL-CM-MT-GENERATIVE-GENERATIVE | T3_confusion_model_type.csv: generative x generative | 60 | validation sample | outputs/T3_confusion_model_type.csv |
| VAL-CM-MT-GENERATIVE-DISCRIMINA | T3_confusion_model_type.csv: generative x discriminative | 1 | validation sample | outputs/T3_confusion_model_type.csv |
| VAL-CM-MT-GENERATIVE-BOTH | T3_confusion_model_type.csv: generative x both | 1 | validation sample | outputs/T3_confusion_model_type.csv |
| VAL-CM-MT-GENERATIVE-UNCLEAR | T3_confusion_model_type.csv: generative x unclear | 0 | validation sample | outputs/T3_confusion_model_type.csv |
| VAL-CM-MT-DISCRIMINA-GENERATIVE | T3_confusion_model_type.csv: discriminative x generative | 0 | validation sample | outputs/T3_confusion_model_type.csv |
| VAL-CM-MT-DISCRIMINA-DISCRIMINA | T3_confusion_model_type.csv: discriminative x discriminative | 23 | validation sample | outputs/T3_confusion_model_type.csv |
| VAL-CM-MT-DISCRIMINA-BOTH | T3_confusion_model_type.csv: discriminative x both | 0 | validation sample | outputs/T3_confusion_model_type.csv |
| VAL-CM-MT-DISCRIMINA-UNCLEAR | T3_confusion_model_type.csv: discriminative x unclear | 4 | validation sample | outputs/T3_confusion_model_type.csv |
| VAL-CM-MT-BOTH-GENERATIVE | T3_confusion_model_type.csv: both x generative | 0 | validation sample | outputs/T3_confusion_model_type.csv |
| VAL-CM-MT-BOTH-DISCRIMINA | T3_confusion_model_type.csv: both x discriminative | 1 | validation sample | outputs/T3_confusion_model_type.csv |
| VAL-CM-MT-BOTH-BOTH | T3_confusion_model_type.csv: both x both | 3 | validation sample | outputs/T3_confusion_model_type.csv |
| VAL-CM-MT-BOTH-UNCLEAR | T3_confusion_model_type.csv: both x unclear | 0 | validation sample | outputs/T3_confusion_model_type.csv |
| VAL-CM-MT-UNCLEAR-GENERATIVE | T3_confusion_model_type.csv: unclear x generative | 1 | validation sample | outputs/T3_confusion_model_type.csv |
| VAL-CM-MT-UNCLEAR-DISCRIMINA | T3_confusion_model_type.csv: unclear x discriminative | 2 | validation sample | outputs/T3_confusion_model_type.csv |
| VAL-CM-MT-UNCLEAR-BOTH | T3_confusion_model_type.csv: unclear x both | 0 | validation sample | outputs/T3_confusion_model_type.csv |
| VAL-CM-MT-UNCLEAR-UNCLEAR | T3_confusion_model_type.csv: unclear x unclear | 12 | validation sample | outputs/T3_confusion_model_type.csv |
| VAL-ST-RTR-SHIFT | Run-to-run: labels shifted between the two re-inferences | 14 of 300 (all adjacent; no shift across the critical-favourable boundary) | validation sample | output/revision_checks/rep1_stability_metrics.csv; Table S15 |
| VAL-PF-CELL-PRIMARY-EX-F-2021-PR | Audit cell (primary): EX-F 2021, vs production: human KEEP | 73.3% (11/15; exact Clopper-Pearson 44.9%-92.2%) | validation sample | outputs/B1/prefilter_cell_exact_ci.csv |
| VAL-PF-CELL-PRIMARY-EX-F-2021-FA | Audit cell (primary): EX-F 2021, vs full-abstract (precision): human KEEP | 73.3% (11/15; exact Clopper-Pearson 44.9%-92.2%) | validation sample | outputs/B1/prefilter_cell_exact_ci.csv |
| VAL-PF-CELL-PRIMARY-EX-F-2022-PR | Audit cell (primary): EX-F 2022, vs production: human KEEP | 80.0% (12/15; exact Clopper-Pearson 51.9%-95.7%) | validation sample | outputs/B1/prefilter_cell_exact_ci.csv |
| VAL-PF-CELL-PRIMARY-EX-F-2022-FA | Audit cell (primary): EX-F 2022, vs full-abstract (precision): human KEEP | 80.0% (12/15; exact Clopper-Pearson 51.9%-95.7%) | validation sample | outputs/B1/prefilter_cell_exact_ci.csv |
| VAL-PF-CELL-PRIMARY-EX-F-2023-PR | Audit cell (primary): EX-F 2023, vs production: human KEEP | 73.3% (11/15; exact Clopper-Pearson 44.9%-92.2%) | validation sample | outputs/B1/prefilter_cell_exact_ci.csv |
| VAL-PF-CELL-PRIMARY-EX-F-2023-FA | Audit cell (primary): EX-F 2023, vs full-abstract (precision): human KEEP | 66.7% (10/15; exact Clopper-Pearson 38.4%-88.2%) | validation sample | outputs/B1/prefilter_cell_exact_ci.csv |
| VAL-PF-CELL-PRIMARY-EX-F-2024-PR | Audit cell (primary): EX-F 2024, vs production: human KEEP | 73.3% (11/15; exact Clopper-Pearson 44.9%-92.2%) | validation sample | outputs/B1/prefilter_cell_exact_ci.csv |
| VAL-PF-CELL-PRIMARY-EX-F-2024-FA | Audit cell (primary): EX-F 2024, vs full-abstract (precision): human KEEP | 73.3% (11/15; exact Clopper-Pearson 44.9%-92.2%) | validation sample | outputs/B1/prefilter_cell_exact_ci.csv |
| VAL-PF-CELL-PRIMARY-EX-F-2025-PR | Audit cell (primary): EX-F 2025, vs production: human KEEP | 93.3% (14/15; exact Clopper-Pearson 68.1%-99.8%) | validation sample | outputs/B1/prefilter_cell_exact_ci.csv |
| VAL-PF-CELL-PRIMARY-EX-F-2025-FA | Audit cell (primary): EX-F 2025, vs full-abstract (precision): human KEEP | 93.3% (14/15; exact Clopper-Pearson 68.1%-99.8%) | validation sample | outputs/B1/prefilter_cell_exact_ci.csv |
| VAL-PF-CELL-PRIMARY-EX-S-2021-PR | Audit cell (primary): EX-S 2021, vs production: human KEEP | 0.0% (0/45; exact Clopper-Pearson 0.0%-7.9%) | validation sample | outputs/B1/prefilter_cell_exact_ci.csv |
| VAL-PF-CELL-PRIMARY-EX-S-2022-PR | Audit cell (primary): EX-S 2022, vs production: human KEEP | 2.2% (1/45; exact Clopper-Pearson 0.1%-11.8%) | validation sample | outputs/B1/prefilter_cell_exact_ci.csv |
| VAL-PF-CELL-PRIMARY-EX-S-2023-PR | Audit cell (primary): EX-S 2023, vs production: human KEEP | 4.4% (2/45; exact Clopper-Pearson 0.5%-15.1%) | validation sample | outputs/B1/prefilter_cell_exact_ci.csv |
| VAL-PF-CELL-PRIMARY-EX-S-2024-PR | Audit cell (primary): EX-S 2024, vs production: human KEEP | 0.0% (0/45; exact Clopper-Pearson 0.0%-7.9%) | validation sample | outputs/B1/prefilter_cell_exact_ci.csv |
| VAL-PF-CELL-PRIMARY-EX-S-2025-PR | Audit cell (primary): EX-S 2025, vs production: human KEEP | 4.4% (2/45; exact Clopper-Pearson 0.5%-15.1%) | validation sample | outputs/B1/prefilter_cell_exact_ci.csv |
| VAL-PF-CELL-PRIMARY-RET-2021-PR | Audit cell (primary): RET 2021, vs production: human KEEP | 100.0% (10/10; exact Clopper-Pearson 69.2%-100.0%) | validation sample | outputs/B1/prefilter_cell_exact_ci.csv |
| VAL-PF-CELL-PRIMARY-RET-2022-PR | Audit cell (primary): RET 2022, vs production: human KEEP | 90.0% (9/10; exact Clopper-Pearson 55.5%-99.7%) | validation sample | outputs/B1/prefilter_cell_exact_ci.csv |
| VAL-PF-CELL-PRIMARY-RET-2023-PR | Audit cell (primary): RET 2023, vs production: human KEEP | 90.0% (9/10; exact Clopper-Pearson 55.5%-99.7%) | validation sample | outputs/B1/prefilter_cell_exact_ci.csv |
| VAL-PF-CELL-PRIMARY-RET-2024-PR | Audit cell (primary): RET 2024, vs production: human KEEP | 100.0% (10/10; exact Clopper-Pearson 69.2%-100.0%) | validation sample | outputs/B1/prefilter_cell_exact_ci.csv |
| VAL-PF-CELL-PRIMARY-RET-2025-PR | Audit cell (primary): RET 2025, vs production: human KEEP | 100.0% (10/10; exact Clopper-Pearson 69.2%-100.0%) | validation sample | outputs/B1/prefilter_cell_exact_ci.csv |
| VAL-PF-CELL-BORDERLINEAPPLICATION-EX-F-2021-PR | Audit cell (borderline→application): EX-F 2021, vs production: human KEEP | 66.7% (10/15; exact Clopper-Pearson 38.4%-88.2%) | validation sample | outputs/B1/prefilter_cell_exact_ci.csv |
| VAL-PF-CELL-BORDERLINEAPPLICATION-EX-F-2021-FA | Audit cell (borderline→application): EX-F 2021, vs full-abstract (precision): human KEEP | 66.7% (10/15; exact Clopper-Pearson 38.4%-88.2%) | validation sample | outputs/B1/prefilter_cell_exact_ci.csv |
| VAL-PF-CELL-BORDERLINEAPPLICATION-EX-F-2022-PR | Audit cell (borderline→application): EX-F 2022, vs production: human KEEP | 73.3% (11/15; exact Clopper-Pearson 44.9%-92.2%) | validation sample | outputs/B1/prefilter_cell_exact_ci.csv |
| VAL-PF-CELL-BORDERLINEAPPLICATION-EX-F-2022-FA | Audit cell (borderline→application): EX-F 2022, vs full-abstract (precision): human KEEP | 73.3% (11/15; exact Clopper-Pearson 44.9%-92.2%) | validation sample | outputs/B1/prefilter_cell_exact_ci.csv |
| VAL-PF-CELL-BORDERLINEAPPLICATION-EX-F-2023-PR | Audit cell (borderline→application): EX-F 2023, vs production: human KEEP | 73.3% (11/15; exact Clopper-Pearson 44.9%-92.2%) | validation sample | outputs/B1/prefilter_cell_exact_ci.csv |
| VAL-PF-CELL-BORDERLINEAPPLICATION-EX-F-2023-FA | Audit cell (borderline→application): EX-F 2023, vs full-abstract (precision): human KEEP | 66.7% (10/15; exact Clopper-Pearson 38.4%-88.2%) | validation sample | outputs/B1/prefilter_cell_exact_ci.csv |
| VAL-PF-CELL-BORDERLINEAPPLICATION-EX-F-2024-PR | Audit cell (borderline→application): EX-F 2024, vs production: human KEEP | 73.3% (11/15; exact Clopper-Pearson 44.9%-92.2%) | validation sample | outputs/B1/prefilter_cell_exact_ci.csv |
| VAL-PF-CELL-BORDERLINEAPPLICATION-EX-F-2024-FA | Audit cell (borderline→application): EX-F 2024, vs full-abstract (precision): human KEEP | 73.3% (11/15; exact Clopper-Pearson 44.9%-92.2%) | validation sample | outputs/B1/prefilter_cell_exact_ci.csv |
| VAL-PF-CELL-BORDERLINEAPPLICATION-EX-F-2025-PR | Audit cell (borderline→application): EX-F 2025, vs production: human KEEP | 93.3% (14/15; exact Clopper-Pearson 68.1%-99.8%) | validation sample | outputs/B1/prefilter_cell_exact_ci.csv |
| VAL-PF-CELL-BORDERLINEAPPLICATION-EX-F-2025-FA | Audit cell (borderline→application): EX-F 2025, vs full-abstract (precision): human KEEP | 93.3% (14/15; exact Clopper-Pearson 68.1%-99.8%) | validation sample | outputs/B1/prefilter_cell_exact_ci.csv |
| VAL-PF-CELL-BORDERLINEAPPLICATION-EX-S-2021-PR | Audit cell (borderline→application): EX-S 2021, vs production: human KEEP | 0.0% (0/45; exact Clopper-Pearson 0.0%-7.9%) | validation sample | outputs/B1/prefilter_cell_exact_ci.csv |
| VAL-PF-CELL-BORDERLINEAPPLICATION-EX-S-2022-PR | Audit cell (borderline→application): EX-S 2022, vs production: human KEEP | 2.2% (1/45; exact Clopper-Pearson 0.1%-11.8%) | validation sample | outputs/B1/prefilter_cell_exact_ci.csv |
| VAL-PF-CELL-BORDERLINEAPPLICATION-EX-S-2023-PR | Audit cell (borderline→application): EX-S 2023, vs production: human KEEP | 4.4% (2/45; exact Clopper-Pearson 0.5%-15.1%) | validation sample | outputs/B1/prefilter_cell_exact_ci.csv |
| VAL-PF-CELL-BORDERLINEAPPLICATION-EX-S-2024-PR | Audit cell (borderline→application): EX-S 2024, vs production: human KEEP | 0.0% (0/45; exact Clopper-Pearson 0.0%-7.9%) | validation sample | outputs/B1/prefilter_cell_exact_ci.csv |
| VAL-PF-CELL-BORDERLINEAPPLICATION-EX-S-2025-PR | Audit cell (borderline→application): EX-S 2025, vs production: human KEEP | 2.2% (1/45; exact Clopper-Pearson 0.1%-11.8%) | validation sample | outputs/B1/prefilter_cell_exact_ci.csv |
| VAL-PF-CELL-BORDERLINEAPPLICATION-RET-2021-PR | Audit cell (borderline→application): RET 2021, vs production: human KEEP | 100.0% (10/10; exact Clopper-Pearson 69.2%-100.0%) | validation sample | outputs/B1/prefilter_cell_exact_ci.csv |
| VAL-PF-CELL-BORDERLINEAPPLICATION-RET-2022-PR | Audit cell (borderline→application): RET 2022, vs production: human KEEP | 90.0% (9/10; exact Clopper-Pearson 55.5%-99.7%) | validation sample | outputs/B1/prefilter_cell_exact_ci.csv |
| VAL-PF-CELL-BORDERLINEAPPLICATION-RET-2023-PR | Audit cell (borderline→application): RET 2023, vs production: human KEEP | 90.0% (9/10; exact Clopper-Pearson 55.5%-99.7%) | validation sample | outputs/B1/prefilter_cell_exact_ci.csv |
| VAL-PF-CELL-BORDERLINEAPPLICATION-RET-2024-PR | Audit cell (borderline→application): RET 2024, vs production: human KEEP | 100.0% (10/10; exact Clopper-Pearson 69.2%-100.0%) | validation sample | outputs/B1/prefilter_cell_exact_ci.csv |
| VAL-PF-CELL-BORDERLINEAPPLICATION-RET-2025-PR | Audit cell (borderline→application): RET 2025, vs production: human KEEP | 100.0% (10/10; exact Clopper-Pearson 69.2%-100.0%) | validation sample | outputs/B1/prefilter_cell_exact_ci.csv |
| VAL-PF-CELL-BORDERLINEKEEP-EX-F-2021-PR | Audit cell (borderline→KEEP): EX-F 2021, vs production: human KEEP | 86.7% (13/15; exact Clopper-Pearson 59.5%-98.3%) | validation sample | outputs/B1/prefilter_cell_exact_ci.csv |
| VAL-PF-CELL-BORDERLINEKEEP-EX-F-2021-FA | Audit cell (borderline→KEEP): EX-F 2021, vs full-abstract (precision): human KEEP | 86.7% (13/15; exact Clopper-Pearson 59.5%-98.3%) | validation sample | outputs/B1/prefilter_cell_exact_ci.csv |
| VAL-PF-CELL-BORDERLINEKEEP-EX-F-2022-PR | Audit cell (borderline→KEEP): EX-F 2022, vs production: human KEEP | 80.0% (12/15; exact Clopper-Pearson 51.9%-95.7%) | validation sample | outputs/B1/prefilter_cell_exact_ci.csv |
| VAL-PF-CELL-BORDERLINEKEEP-EX-F-2022-FA | Audit cell (borderline→KEEP): EX-F 2022, vs full-abstract (precision): human KEEP | 80.0% (12/15; exact Clopper-Pearson 51.9%-95.7%) | validation sample | outputs/B1/prefilter_cell_exact_ci.csv |
| VAL-PF-CELL-BORDERLINEKEEP-EX-F-2023-PR | Audit cell (borderline→KEEP): EX-F 2023, vs production: human KEEP | 86.7% (13/15; exact Clopper-Pearson 59.5%-98.3%) | validation sample | outputs/B1/prefilter_cell_exact_ci.csv |
| VAL-PF-CELL-BORDERLINEKEEP-EX-F-2023-FA | Audit cell (borderline→KEEP): EX-F 2023, vs full-abstract (precision): human KEEP | 80.0% (12/15; exact Clopper-Pearson 51.9%-95.7%) | validation sample | outputs/B1/prefilter_cell_exact_ci.csv |
| VAL-PF-CELL-BORDERLINEKEEP-EX-F-2024-PR | Audit cell (borderline→KEEP): EX-F 2024, vs production: human KEEP | 73.3% (11/15; exact Clopper-Pearson 44.9%-92.2%) | validation sample | outputs/B1/prefilter_cell_exact_ci.csv |
| VAL-PF-CELL-BORDERLINEKEEP-EX-F-2024-FA | Audit cell (borderline→KEEP): EX-F 2024, vs full-abstract (precision): human KEEP | 73.3% (11/15; exact Clopper-Pearson 44.9%-92.2%) | validation sample | outputs/B1/prefilter_cell_exact_ci.csv |
| VAL-PF-CELL-BORDERLINEKEEP-EX-F-2025-PR | Audit cell (borderline→KEEP): EX-F 2025, vs production: human KEEP | 100.0% (15/15; exact Clopper-Pearson 78.2%-100.0%) | validation sample | outputs/B1/prefilter_cell_exact_ci.csv |
| VAL-PF-CELL-BORDERLINEKEEP-EX-F-2025-FA | Audit cell (borderline→KEEP): EX-F 2025, vs full-abstract (precision): human KEEP | 100.0% (15/15; exact Clopper-Pearson 78.2%-100.0%) | validation sample | outputs/B1/prefilter_cell_exact_ci.csv |
| VAL-PF-CELL-BORDERLINEKEEP-EX-S-2021-PR | Audit cell (borderline→KEEP): EX-S 2021, vs production: human KEEP | 0.0% (0/45; exact Clopper-Pearson 0.0%-7.9%) | validation sample | outputs/B1/prefilter_cell_exact_ci.csv |
| VAL-PF-CELL-BORDERLINEKEEP-EX-S-2022-PR | Audit cell (borderline→KEEP): EX-S 2022, vs production: human KEEP | 2.2% (1/45; exact Clopper-Pearson 0.1%-11.8%) | validation sample | outputs/B1/prefilter_cell_exact_ci.csv |
| VAL-PF-CELL-BORDERLINEKEEP-EX-S-2023-PR | Audit cell (borderline→KEEP): EX-S 2023, vs production: human KEEP | 4.4% (2/45; exact Clopper-Pearson 0.5%-15.1%) | validation sample | outputs/B1/prefilter_cell_exact_ci.csv |
| VAL-PF-CELL-BORDERLINEKEEP-EX-S-2024-PR | Audit cell (borderline→KEEP): EX-S 2024, vs production: human KEEP | 0.0% (0/45; exact Clopper-Pearson 0.0%-7.9%) | validation sample | outputs/B1/prefilter_cell_exact_ci.csv |
| VAL-PF-CELL-BORDERLINEKEEP-EX-S-2025-PR | Audit cell (borderline→KEEP): EX-S 2025, vs production: human KEEP | 4.4% (2/45; exact Clopper-Pearson 0.5%-15.1%) | validation sample | outputs/B1/prefilter_cell_exact_ci.csv |
| VAL-PF-CELL-BORDERLINEKEEP-RET-2021-PR | Audit cell (borderline→KEEP): RET 2021, vs production: human KEEP | 100.0% (10/10; exact Clopper-Pearson 69.2%-100.0%) | validation sample | outputs/B1/prefilter_cell_exact_ci.csv |
| VAL-PF-CELL-BORDERLINEKEEP-RET-2022-PR | Audit cell (borderline→KEEP): RET 2022, vs production: human KEEP | 90.0% (9/10; exact Clopper-Pearson 55.5%-99.7%) | validation sample | outputs/B1/prefilter_cell_exact_ci.csv |
| VAL-PF-CELL-BORDERLINEKEEP-RET-2023-PR | Audit cell (borderline→KEEP): RET 2023, vs production: human KEEP | 90.0% (9/10; exact Clopper-Pearson 55.5%-99.7%) | validation sample | outputs/B1/prefilter_cell_exact_ci.csv |
| VAL-PF-CELL-BORDERLINEKEEP-RET-2024-PR | Audit cell (borderline→KEEP): RET 2024, vs production: human KEEP | 100.0% (10/10; exact Clopper-Pearson 69.2%-100.0%) | validation sample | outputs/B1/prefilter_cell_exact_ci.csv |
| VAL-PF-CELL-BORDERLINEKEEP-RET-2025-PR | Audit cell (borderline→KEEP): RET 2025, vs production: human KEEP | 100.0% (10/10; exact Clopper-Pearson 69.2%-100.0%) | validation sample | outputs/B1/prefilter_cell_exact_ci.csv |
| VAL-PF-VAR-BORDERLINEAPPLICATION-MISSEDTOTAL | Audit (borderline→application): missed_total | 3217 (95% CI 2640-5729) | 2021-2025 frame | outputs/B1/prefilter_exact_ci_long.csv |
| VAL-PF-VAR-BORDERLINEAPPLICATION-FNRATEPOOLED | Audit (borderline→application): FNrate_pooled | 4.4% (95% CI 3.6%-7.9%) | 2021-2025 frame | outputs/B1/prefilter_exact_ci_long.csv |
| VAL-PF-VAR-BORDERLINEAPPLICATION-PPVRETPOOLED | Audit (borderline→application): PPV_RET_pooled | 97.6% (95% CI 84.7%-98.1%) | 2021-2025 frame | outputs/B1/prefilter_exact_ci_long.csv |
| VAL-PF-VAR-BORDERLINEAPPLICATION-PROD2X2SENSITIVITY | Audit (borderline→application): prod2x2_sensitivity | 81.0% (95% CI 69.4%-83.3%) | 2021-2025 frame | outputs/B1/prefilter_exact_ci_long.csv |
| VAL-PF-VAR-BORDERLINEAPPLICATION-PROD2X2SPECIFICITY | Audit (borderline→application): prod2x2_specificity | 99.5% (95% CI 97.0%-99.6%) | 2021-2025 frame | outputs/B1/prefilter_exact_ci_long.csv |
| VAL-PF-VAR-BORDERLINEAPPLICATION-PROD2X2PPV | Audit (borderline→application): prod2x2_PPV | 97.6% (95% CI 84.7%-98.1%) | 2021-2025 frame | outputs/B1/prefilter_exact_ci_long.csv |
| VAL-PF-VAR-BORDERLINEAPPLICATION-PROD2X2NPV | Audit (borderline→application): prod2x2_NPV | 95.6% (95% CI 92.1%-96.4%) | 2021-2025 frame | outputs/B1/prefilter_exact_ci_long.csv |
| VAL-PF-VAR-BORDERLINEAPPLICATION-PROD2X2KAPPA | Audit (borderline→application): prod2x2_kappa | 0.860 (95% CI 0.733-0.867) | 2021-2025 frame | outputs/B1/prefilter_exact_ci_long.csv |
| VAL-PF-VAR-BORDERLINEAPPLICATION-PROD2X2AC1 | Audit (borderline→application): prod2x2_AC1 | 0.942 (95% CI 0.885-0.946) | 2021-2025 frame | outputs/B1/prefilter_exact_ci_long.csv |
| VAL-PF-VAR-BORDERLINEAPPLICATION-FULLABSPRECISIONPOOLED | Audit (borderline→application): fullabs_precision_pooled | 78.8% (95% CI 67.4%-84.9%) | 2021-2025 frame | outputs/B1/prefilter_exact_ci_long.csv |
| VAL-PF-VAR-BORDERLINEKEEP-MISSEDTOTAL | Audit (borderline→KEEP): missed_total | 3897 (95% CI 3104-6674) | 2021-2025 frame | outputs/B1/prefilter_exact_ci_long.csv |
| VAL-PF-VAR-BORDERLINEKEEP-FNRATEPOOLED | Audit (borderline→KEEP): FNrate_pooled | 5.4% (95% CI 4.3%-9.2%) | 2021-2025 frame | outputs/B1/prefilter_exact_ci_long.csv |
| VAL-PF-VAR-BORDERLINEKEEP-PPVRETPOOLED | Audit (borderline→KEEP): PPV_RET_pooled | 97.6% (95% CI 84.7%-98.1%) | 2021-2025 frame | outputs/B1/prefilter_exact_ci_long.csv |
| VAL-PF-VAR-BORDERLINEKEEP-PROD2X2SENSITIVITY | Audit (borderline→KEEP): prod2x2_sensitivity | 77.9% (95% CI 66.1%-81.0%) | 2021-2025 frame | outputs/B1/prefilter_exact_ci_long.csv |
| VAL-PF-VAR-BORDERLINEKEEP-PROD2X2SPECIFICITY | Audit (borderline→KEEP): prod2x2_specificity | 99.5% (95% CI 96.9%-99.6%) | 2021-2025 frame | outputs/B1/prefilter_exact_ci_long.csv |
| VAL-PF-VAR-BORDERLINEKEEP-PROD2X2PPV | Audit (borderline→KEEP): prod2x2_PPV | 97.6% (95% CI 84.7%-98.1%) | 2021-2025 frame | outputs/B1/prefilter_exact_ci_long.csv |
| VAL-PF-VAR-BORDERLINEKEEP-PROD2X2NPV | Audit (borderline→KEEP): prod2x2_NPV | 94.6% (95% CI 90.8%-95.7%) | 2021-2025 frame | outputs/B1/prefilter_exact_ci_long.csv |
| VAL-PF-VAR-BORDERLINEKEEP-PROD2X2KAPPA | Audit (borderline→KEEP): prod2x2_kappa | 0.837 (95% CI 0.706-0.850) | 2021-2025 frame | outputs/B1/prefilter_exact_ci_long.csv |
| VAL-PF-VAR-BORDERLINEKEEP-PROD2X2AC1 | Audit (borderline→KEEP): prod2x2_AC1 | 0.930 (95% CI 0.869-0.938) | 2021-2025 frame | outputs/B1/prefilter_exact_ci_long.csv |
| VAL-PF-VAR-BORDERLINEKEEP-FULLABSPRECISIONPOOLED | Audit (borderline→KEEP): fullabs_precision_pooled | 86.5% (95% CI 76.4%-90.8%) | 2021-2025 frame | outputs/B1/prefilter_exact_ci_long.csv |

## Superseded numbers


### Old -> new -> reason

| ID | Item | Value | Window | Source |
|---|---|---|---|---|
| SUP-01 | 16,749 abstracts; 2021-2026 (title) [Title] | -> COR-23 (14,058); 2021-2025 | submitted -> R1 | Analytic corpus is 2021-2025 (decision 1) |
| SUP-02 | 97,492 eligible Q1/Q2 records [Abstract; Methods; Results] | -> COR-16 (86,700) | submitted -> R1 | Window step 2021-2025 replaces the April 2026 cutoff |
| SUP-03 | 16,759 retained (8,899 discourse; 7,860 evaluative) [Abstract; Methods; Results] | -> COR-19 to COR-21 (14,066; 7637; 6429) | submitted -> R1 | 2021-2025 window |
| SUP-04 | 16,749 valid labels; 10 unparseable [Abstract; Methods; Results] | -> COR-22, COR-23 (8 FAILED; 14,058) | submitted -> R1 | 2021-2025 window |
| SUP-05 | 16,747 records dated 2021-2026; 2 dated 2020 [Methods; Results; Figure captions] | -> COR-23 (14,058) | submitted -> R1 | 2021-2025 window; 2020 records fall outside the window |
| SUP-06 | 5,161 critical records [Methods; Results] | -> COR-SUB-01 (4283) | submitted -> R1 | 2021-2025 window |
| SUP-07 | 5,159 parsed; 4,747 abstract-present critical [Methods; Results] | -> COR-SUB-04, COR-SUB-06 (4281; 3906) | submitted -> R1 | 2021-2025 window |
| SUP-08 | 2,226 hallucination-gated records [Abstract; Results; Figure 2] | -> COR-SUB-07 (1775) | submitted -> R1 | 2021-2025 window |
| SUP-09 | 16,734 records with valid specialty; 13 FAILED [Results; Figure 3; Table S16] | -> COR-SUB-08, COR-SUB-09 (14,048; 10) | submitted -> R1 | 2021-2025 window |
| SUP-10 | 90.3% of records resolved to a country [Methods] | -> COR-SUB-10 (12,745/14,058) | submitted -> R1 | 2021-2025 window |
| SUP-11 | Q1/Q2 = 88.0% of records [Methods] | -> COR-Q1Q2-PCT (88.1%) | submitted -> R1 | Rounding error (98,626/112,011 = 88.05%; B7 item 5) |
| SUP-12 | 7,922 unmatched [Methods] | -> COR-07 to COR-10 (5092 not in SJR; 1494 no quartile; 1336 Q4) | submitted -> R1 | Unmatched includes Q4 and no-quartile titles (T7) |
| SUP-13 | Cautious Optimism 62.8% (n=10,514); Neutral 5.0% (n=837); Advocacy 1.4% (n=235); critical 30.8% (916 Alarm, 4,245 Caution) [Abstract; Results] | -> RES-OVR-* | submitted -> R1 | 2021-2025 window |
| SUP-14 | Advocacy 2.9% (2021) to 0.6% (2026), Spearman ρ=-1.00 [Abstract; Results; Discussion] | -> RES-TMP-ADV-2021, -2025, -RHO, -OR, -AOR | submitted -> R1 | 2026 is no longer a trend point |
| SUP-15 | Critical 25.4% (22.9-28.1) to 32.6% (30.9-34.4); +7.25 percentage points [Abstract; Results; Table S1] | -> RES-TMP-CRIT-* | submitted -> R1 | 2021-2025 window |
| SUP-16 | Alarm 2.7% to 6.8% (2024), 6.2% in 2026; Caution 22.7% to 26.4%; Cautious Optimism 60.2%-65.3% [Results] | -> RES-TMP-ALARM-*, -CAUT-*, -CO-* | submitted -> R1 | 2021-2025 window |
| SUP-17 | 17 Advocacy records in 2026; 5 about drug discovery (Table S2) [Results; Table S2] | -> RES-2026-ADVOCACY; RES-ADVSP-* | submitted -> R1 | 2026 is descriptive only; Table S2 replaced by the 2026 descriptive table |
| SUP-18 | Discourse 30.2% to 37.8% (ρ=+0.94); evaluative 14.6% to 28.1% (ρ=+0.77); ratio 2.24 to 0.88 [Results; Table S3] | -> RES-TMP-GENDISC-*, -GENEVAL-*, RES-TMP-GENRATIO-* | submitted -> R1 | 2021-2025 window; deterministic per-cell seeds (B7 item 2) |
| SUP-19 | Keep rate ρ=+1.00 (Table S4) [Results] | -> RES-TMP-KEEP-* | submitted -> R1 | 2021-2025 window |
| SUP-20 | Patient safety +11.0; errors +30.9; regulation -22.0; ethics/bias -8.1 percentage points (36.7% to 28.6%) [Abstract; Results; Table S5] | -> RES-TMP-TH-* | submitted -> R1 | 2021-2025 window |
| SUP-21 | Factual error 56% to 90% of gated papers; fabrication-involved 0% (2021) to roughly 21-23% from 2023 [Abstract; Results] | -> RES-TMP-FM-MIS-*, RES-TMP-FAB-GATED-* | submitted -> R1 | 2021-2025 window; values in B7 item 6 |
| SUP-22 | Generative share 5.3% (2021) to 62.8% (2026), ρ=+0.94; fabrication share 13.8% in 2026; 21.8%, 22.9%, 19.7%, 22.0% among generative (2023-2026) [Results] | -> RES-TMP-GENSHARE-*, RES-TMP-FAB-ALL-*, RES-TMP-FAB-GEN-* | submitted -> R1 | 2021-2025 window |
| SUP-23 | 1,858 records (39.1%) generative without fabrication [Results] | -> RES-TMP-MECH-GENNOFAB | submitted -> R1 | 2021-2025 window |
| SUP-24 | Specialty range: Mental Health 51.3% (46.8-55.5) to Cardiology 16.8% (14.1-19.8); Informatics 44.9%; Nursing 43.0%; Ophthalmology 18.4%; Oncology 19.7% [Abstract; Results; Figure 3] | -> RES-SPC-OBS-*, RES-SPC-RANGE | submitted -> R1 | 2021-2025 window |
| SUP-25 | FDA ρ=-0.65 (two-sided P=.004); structural zeros dropped ρ=-0.58 (P=.062, n=11); generative-share ρ=-0.01 [Abstract; Results; Table S6; Figure S5] | -> RES-SPC-FDA-RHO18, -RHO11, -PARTIAL, RES-SPC-GEN-RHO | submitted -> R1 | 2021-2025 window; labelled exploratory (D4b) |
| SUP-26 | United States 34.5% (n=4,222) vs China 16.2% (n=1,904); Netherlands 44.4%; Denmark 42.6%; Australia 42.5%; Ireland 41.1%; United Kingdom 40.6%; Japan 18.3%; Iran 18.0%; South Korea 20.5%; India 20.6% [Abstract; Results; Table S7] | -> RES-GEO-CTY-*; RES-GEO-USCN-AOR | submitted -> R1 | 2021-2025 window |
| SUP-27 | 36 countries with >= 50 records; 45 with >= 20 [Figure 4; Figure S6; Table S7] | -> RES-GEO-NCTY50, RES-GEO-NCTY20 | submitted -> R1 | 2021-2025 window |
| SUP-28 | Region n: North America 4,964; Western Europe 4,298; East Asia 3,262 (Table S9) [Results; Table S9] | -> RES-GEO-REG-* | submitted -> R1 | n's printed on 16,759, rates on 16,747 (B7 item 3); now both on 14,058 |
| SUP-29 | East Asia 18.5% reweighted to 19.9%, closing 8% of the gap; Hong Kong 31.6%; Singapore 26.7% [Results] | -> RES-GEO-EARW; RES-GEO-CTY-* | submitted -> R1 | 2021-2025 window |
| SUP-30 | Publication type n: Research Articles 10,315; Reviews 5,444; Letters 480; Editorials 404; Commentaries 104 [Results; Table S10] | -> RES-FMT-* | submitted -> R1 | 2021-2025 window |
| SUP-31 | Commentary critical 53.9% [Results; Table S10] | -> RES-FMT-COMMENTARY-CRITICAL | submitted -> R1 | Rounding (56/104 = 53.85%, B7 item 4) and 2021-2025 window |
| SUP-32 | Opinion 41.8% vs Research 32.9%; χ²4=430.5, P<.001, Cramér V=0.195 (N=11,303) [Results; Table S10] | -> RES-FMT-OPINION-CRIT, RES-FMT-CHISQ | submitted -> R1 | 2021-2025 window |
| SUP-33 | Reviews 24.9% critical, 73.1% favourable; systematic 29.3% (n=980) vs narrative 23.9% (n=4,464) [Abstract; Results; Table S11] | -> RES-FMT-REVIEW-*, RES-FMT-RSUB-* | submitted -> R1 | 2021-2025 window |
| SUP-34 | Table S12 theme-by-format values [Table S12] | -> RES-FMT-THEME-* | submitted -> R1 | 2021-2025 window |
| SUP-35 | Table S1 P values (.072, .072, .019, .329, .003, .072) [Table S1] | -> RES-TMP-*-RHO | submitted -> R1 | Exact permutation P on 5 annual points (B7 item 1) |
| SUP-36 | Prefilter κ 0.51 (95% CI 0.35-0.68) [Abstract; Methods] | -> VAL-PF-PILOT-K3 (0.511; 0.345-0.646) | submitted -> R1 | Original CI code not found; recomputed bootstrap (B7 item 8a) |
| SUP-37 | Failure mode κ_max 0.76; model type AC1 0.89 [Methods] | -> VAL-MX-FM-KMAX (0.755); VAL-MX-MT-AC1 (0.88) | submitted -> R1 | Double rounding (B7 items 7a-7b) |
| SUP-38 | Specialty κ 0.75 (no CI) [Abstract; Methods] | -> VAL-SP-K | submitted -> R1 | CI added (E12) |
| SUP-39 | Model type κ 0.84; failure mode κ 0.57 (no CI) [Abstract; Methods] | -> VAL-MX-MT-K, VAL-MX-FM-K | submitted -> R1 | CI added (E12) |
| SUP-40 | Supplementary Note 2 prints the v2 stance prompt; Methods Advocacy definition paraphrases v2 [Methods; Note 2] | -> C5 Note 2 (a) v1, (b) v2 | submitted -> R1 | All reported labels come from v1 (decision 4; Batch 2b finding) |
| SUP-41 | Prefilter API: Batch API [Methods] | -> Text correction | submitted -> R1 | First 2,500 records ran synchronously; 94,992 via one Message Batch (B7 item 8) |
| SUP-B7 | All B7 numeric corrections (Table S1 P values, Table S3 seeds, Table S9 n's, Commentary 53.8%, Q1/Q2 88.1%, κ_max 0.755, AC1 0.885, prefilter κ CI, fabrication-involved series) | -> see outputs/B7_corrections.md (included verbatim in the C1 markdown appendix) | submitted -> R1 | outputs/B7_corrections.md |


## Appendix: B7 numeric corrections (verbatim)

### B7 · Numeric corrections (E13, D8)

Old value (as printed in the submitted manuscript/supplement) → corrected value → source. Numbers only; the manuscript is not edited here.

## 1. Table S1 P values → exact permutation P (all rows)

Source: `outputs/T4_trend_tests.csv` (t4_temporal.py; all 6! or 5! orderings). The printed values except Advocacy are scipy's asymptotic t-approximation. Minimum attainable two-sided P: 2/720 = .003 (6 points), 2/120 = .017 (5 points).

| Table S1 row | printed P (2021–2026) | ρ 2021–2026 | exact permutation P 2021–2026 | ρ 2021–2025 | exact permutation P 2021–2025 |
|---|---|---|---|---|---|
| Alarm | .072 | +0.771 | .103 | +0.800 | .133 |
| Caution | .072 | +0.771 | .103 | +0.600 | .350 |
| Neutral | .019 | -0.886 | .033 | -0.900 | .083 |
| Cautious Optimism | .329 | -0.486 | .356 | -0.600 | .350 |
| Advocacy | .003 | -1.000 | .003 | -1.000 | .017 |
| Critical (Alarm+Caution) | .072 | +0.771 | .103 | +0.800 | .133 |

## 2. Table S3 regenerated with deterministic per-cell seeds

**2021–2026 (submitted window)** — Spearman ρ (exact P): discourse +0.94 (.017); evaluative +0.77 (.103).

| genre | year | seed | printed % (CI) | corrected % (CI); n/N |
|---|---|---|---|---|
| discourse | 2021 | 42 | 30.2 (26.7–33.3) | 30.2 (26.8–33.6); 222/735 |
| discourse | 2022 | 43 | 31.2 (28.0–34.2) | 31.2 (28.0–34.4); 269/863 |
| discourse | 2023 | 44 | 35.3 (32.4–37.9) | 35.3 (32.7–38.0); 447/1267 |
| discourse | 2024 | 45 | 37.5 (35.3–39.5) | 37.5 (35.2–39.6); 713/1901 |
| discourse | 2025 | 46 | 35.4 (33.7–37.4) | 35.4 (33.7–37.3); 1016/2867 |
| discourse | 2026 | 47 | 37.8 (35.2–40.5) | 37.8 (35.3–40.6); 477/1261 |
| evaluative | 2021 | 48 | 14.6 (11.0–18.6) | 14.6 (11.0–18.6); 48/328 |
| evaluative | 2022 | 49 | 13.3 (10.2–16.7) | 13.3 (10.4–16.5); 64/480 |
| evaluative | 2023 | 50 | 22.5 (19.6–25.3) | 22.5 (19.8–25.4); 177/787 |
| evaluative | 2024 | 51 | 28.6 (26.5–30.8) | 28.6 (26.5–30.9); 515/1799 |
| evaluative | 2025 | 52 | 26.8 (25.1–28.4) | 26.8 (25.2–28.4); 812/3031 |
| evaluative | 2026 | 53 | 28.1 (25.8–30.5) | 28.1 (25.6–30.5); 401/1428 |

**2021–2025 (primary window)** — Spearman ρ (exact P): discourse +0.90 (.083); evaluative +0.80 (.133).

| genre | year | seed | printed % (CI) | corrected % (CI); n/N |
|---|---|---|---|---|
| discourse | 2021 | 42 | 30.2 (26.7–33.3) | 30.2 (26.8–33.6); 222/735 |
| discourse | 2022 | 43 | 31.2 (28.0–34.2) | 31.2 (28.0–34.4); 269/863 |
| discourse | 2023 | 44 | 35.3 (32.4–37.9) | 35.3 (32.7–38.0); 447/1267 |
| discourse | 2024 | 45 | 37.5 (35.3–39.5) | 37.5 (35.2–39.6); 713/1901 |
| discourse | 2025 | 46 | 35.4 (33.7–37.4) | 35.4 (33.7–37.3); 1016/2867 |
| evaluative | 2021 | 47 | 14.6 (11.0–18.6) | 14.6 (10.7–18.6); 48/328 |
| evaluative | 2022 | 48 | 13.3 (10.2–16.7) | 13.3 (10.6–16.5); 64/480 |
| evaluative | 2023 | 49 | 22.5 (19.6–25.3) | 22.5 (19.6–25.5); 177/787 |
| evaluative | 2024 | 50 | 28.6 (26.5–30.8) | 28.6 (26.5–30.7); 515/1799 |
| evaluative | 2025 | 51 | 26.8 (25.1–28.4) | 26.8 (25.2–28.4); 812/3031 |

Seeds: 42 + cell_index with cells sorted by genre then year; each cell resampled on its own (as the original design), replacing `42 + hash((genre, year)) % 10000`. Point estimates are unchanged.

## 3. Table S9 and Results region n's on the 16,747 denominator

Source: `outputs/T5_crosssectional_both_windows.csv`. The printed n's sum to 16,759 (before the 10 stance failures and 2 records dated 2020 were excluded); the percentages were already computed on 16,747.

| region | printed n | corrected n (16,747) | critical % (CI), unchanged |
|---|---|---|---|
| East Asia | 3,262 | 3,260 | 18.5 (17.2–19.9); 604/3,260 |
| Eastern Europe | 330 | 329 | 28.9 (24.1–34.4); 95/329 |
| Latin America / Oceania | 753 | 752 | 36.8 (33.3–40.2); 277/752 |
| Middle East / North Africa | 1,706 | 1,706 | 30.6 (28.4–32.8); 522/1,706 |
| North America | 4,964 | 4,961 | 35.1 (33.9–36.4); 1,743/4,961 |
| South/Southeast Asia | 785 | 782 | 24.6 (21.5–27.7); 192/782 |
| Sub-Saharan Africa | 68 | 68 | 45.6 (32.7–56.5); 31/68 |
| Unknown | 593 | 593 | 32.2 (28.4–36.1); 191/593 |
| Western Europe | 4,298 | 4,296 | 35.1 (33.6–36.5); 1,506/4,296 |

## 4–7. Single values

| # | item | printed | corrected | source |
|---|---|---|---|---|
| 4 | Commentary critical rate (Results; Table S10) | 53.9% | **53.8%** (56/104 = 53.85%) | T5 cross-sectional |
| 5 | Q1/Q2 share of eligible records (Methods) | 88.0% | **88.1%** (98,626/112,011 = 88.05%) | `output/sjr.log` |
| 7a | Failure-mode κ_max (Methods) | 0.76 | **0.755** (0.7549) | T3 |
| 7b | Model-type Gwet AC1 (Methods) | 0.89 | **0.885** (0.8847) | T3 |
| 8a | Prefilter κ 95% CI (Methods) | 0.35–0.68 | **0.345–0.646** (bootstrap, 1000, seed 42; original code not found) | T1 |
| 8b | Prefilter raw agreement / κ | 85.5% / 0.51 | unchanged (171/200; 0.511) | T1 |

## 6. Fabrication-involved share among hallucination-gated, abstract-present critical records, by year

Printed (Abstract; Results R29): "rose from 0% in 2021 to roughly 21–23% from 2023 onward". Corrected values (confabulation or both; source `outputs/T4_annual_all_domains.csv`):

| year | share (bootstrap 95% CI) | exact Clopper–Pearson 95% CI | n/N |
|---|---|---|---|
| 2021 | 0.0% (0.0–0.0) | 0.0–6.4 | 0/56 |
| 2022 | 1.6% (0.0–5.4) | 0.0–8.8 | 1/61 |
| 2023 | 15.8% (11.1–20.7) | 11.2–21.4 | 34/215 |
| 2024 | 23.4% (20.0–26.8) | 19.9–27.1 | 131/560 |
| 2025 | 20.6% (17.8–23.2) | 18.0–23.4 | 182/883 |
| 2026 (Jan–Apr) | 21.7% (18.0–25.4) | 18.0–25.8 | 98/451 |

## 8. Text-only corrections (no printed number changes)

- **Stance prompt (new in Batch 2b).** Supplementary Note 2 prints the v2 prompt (current `classify_stance_batch.py`, 8,164 characters); all reported stance labels come from the v1 prompt (SHA-256 `b3949917…`, `classify_stance.py` = `9c79cd5:classify_stance_batch.py`). The Methods' Advocacy definition ("both transformative language … and minimal or no acknowledged caveats") paraphrases v2; v1 reads "Advocacy: strongly pro-AI. Emphasises transformative potential, minimal caveats."
- Prefilter API: first 2,500 records synchronous, 94,992 via one Message Batch (Methods says Batch API).
- Prefilter failure defaults: 96 records defaulted to `application`.
- Pilot sampling design not documented; `make_pilot.py` does not match the committed pilot.
- SJR "unmatched" (7,922) includes 1,336 Q4 and 1,494 no-quartile titles.
- Regions (Table S9) come from `geography_classifications.csv`, not from grouping the 90.3%-resolved countries.
- Review subtype rule (PubMed Publication Type substrings; Scoping Review → narrative; Meta-Analysis has no rule).
- Stance validation sample drawn only from abstract-present records.
- Human stance codebook (`coding_instructions.txt`) shorter than the classifier prompt.
- Generative share for the specialty correlation computed among abstract-present critical records.
- Missing PubDate months are stored as January.

