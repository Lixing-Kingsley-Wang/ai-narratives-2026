# T6 · Missing-data accounting (E14; feeds E10 flowchart)

Script: `revision_r1/scripts/t6_missing_data.py`. Counts are recomputed from the pipeline files; log-derived counts (retrieval, pre-cutoff SJR totals, batch failures) are parsed from `output/*.log`.

## 1. Stage table

| stage | records in | records out | excluded/missing | reason | source |
|---|---|---|---|---|---|
| 1. PubMed retrieval (monthly windows, Jan 2021–Apr 2026) |  | 129557 |  |  | output/fetch.log |
| 2. PMID de-duplication | 129557 | 116117 | 13440 | same PMID retrieved in more than one monthly window | fetch.log; raw_medical_all.csv |
| 3. Conference proceedings / preprints | 116117 | 112011 | 4106 | journal on EXCLUDE_JOURNALS / EXCLUDE_KEYWORDS (sjr_filter.py) | filtered_medical_all_excluded.csv |
| 4. SJR title matching | 112011 | 104089 | 7922 | normalised journal title not found in SCImago file for that year (unmatched) | filtered_medical_all_unmatched.csv |
| 4b. SJR quartile Q3 (comparison arm, not primary) |  | 5463 | 5463 | best quartile Q3; analysed separately (pre-cutoff count) | sjr.log; filtered_medical_all_Q3.csv |
| 5. April 2026 cover-date cutoff (Q1/Q2) | 98626 | 97492 | 1134 | PubDate May 2026 or later (records not retained on disk; per-year counts = sjr.log Q1+Q2 minus post-cutoff file) | sjr.log; filtered_medical_all_Q1Q2.csv |
| 5b. Q3 cutoff | 5463 | 5433 | 30 | same cutoff applied to Q3 | filtered_medical_all_Q3.csv |
| 6. AI-engagement prefilter | 97492 | 16759 | 80733 | classified application (AI as method), incl. failure-branch defaults | prefiltered_application.csv |
| 6a. of which: prefilter failures defaulted to application (T1) |  |  | 96 | non-succeeded batch result (9) or synchronous-path failure after 3 retries (87); see T1 | prefiltered_application.csv (type_confidence=Low) |
| 7. Stance classification | 16759 | 16749 | 10 | unparseable / empty response → FAILED | classified_medical_Q1Q2.csv |
| 8. Year window 2021–2026 | 16749 | 16747 | 2 | pub_year 2020 (PubDate earlier than retrieval PDAT) | classified_medical_Q1Q2.csv |
| 8b. Primary temporal window 2021–2025 (R1) | 16747 | 14058 | 2689 | Jan–Apr 2026 partial year: descriptive only |  |
| 9. Critical subset (Alarm or Caution) | 16747 | 5161 |  | theme and mechanism analyses run on critical records | thematic_alarm.csv |
| 10. Theme classification | 5161 | 5161 | 0 | no record dropped; 1 non-succeeded batch result defaulted to ['other'] (log). Records whose only theme is 'other': 51 (upper bound for fallbacks) | themes_batch_poll.log; thematic_alarm.csv |
| 11. Mechanism classification | 5161 | 5159 | 2 | FAILED after 3 retries | q7_classified_ac.csv |
| 12. Title-only records within the parsed critical set | 5159 | 4747 | 412 | empty abstract (mechanism analyses restricted to abstract-present records) | q7_classified_ac.csv + abstract |
| 13. Specialty classification (analytic set) | 16747 | 16734 | 13 | specialty = FAILED (no JSON / outside vocabulary) | specialty_classifications.csv |
| 14a. First-author country (Figure 4 / Table S7 resolver) | 16747 | 15119 | 1628 | affiliation empty (274) or no country string matched (1354) | analysis/run_country_critical_map.py::resolve_country |
| 14b. First-author region (Table S9; geography_classifications.csv) | 16747 | 16154 | 593 | region 'Unknown' in geography_classifications.csv | geography_classifications.csv |
| 15. Publication type mapping | 16747 | 16747 | 0 | no record unmapped: every record falls to a bucket. Default bucket 'Research Article' (no Editorial/Letter/Review/Comment/News tag) = 10,315; News folded into Research Article = 0; empty pub_type = 0 | analysis/robustness.py::simplify_pubtype_7/5 |

## 2. Losses by publication year

Columns are stages from the table above (only stages with a per-year breakdown). 'missing' = no parseable year.

| pub_year | 3. Conference proceedings / preprints | 4. SJR title matching | 5. April 2026 cover-date cutoff (Q1/Q2) | 6. AI-engagement prefilter | 6a. of which: prefilter failures defaulted to application (T1) | 7. Stance classification | 8. Year window 2021–2026 | 11. Mechanism classification | 12. Title-only records within the parsed critical set | 13. Specialty classification (analytic set) | 14a. First-author country (Figure 4 / Table S7 resolver) | 14b. First-author region (Table S9; geography_classifications.csv) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2018 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 2020 | 41 | 0 | 0 | 32 | 1 | 0 | 2 | 0 | 0 | 0 | 0 | 0 |
| 2021 | 409 | 822 | 0 | 10127 | 87 | 1 | 0 | 0 | 25 | 0 | 80 | 46 |
| 2022 | 438 | 1190 | 0 | 11792 | 0 | 1 | 0 | 0 | 48 | 2 | 99 | 48 |
| 2023 | 615 | 1156 | 0 | 12073 | 0 | 1 | 0 | 1 | 80 | 1 | 207 | 94 |
| 2024 | 1006 | 1598 | 0 | 15668 | 2 | 4 | 0 | 1 | 151 | 2 | 396 | 163 |
| 2025 | 1429 | 2255 | 0 | 22974 | 6 | 1 | 0 | 0 | 71 | 5 | 531 | 153 |
| 2026 | 168 | 901 | 1134 | 8066 | 0 | 2 | 0 | 0 | 37 | 3 | 315 | 89 |
| Total | 4106 | 7922 | 1134 | 80733 | 96 | 10 | 2 | 2 | 412 | 13 | 1628 | 593 |

## 3. Title-only (empty abstract) records at each stage

Cells are empty-abstract records / all records in that year.

| stage | N | empty abstract | % | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|---|---|
| raw (116,117) | 116117 | 1696 | 1.5 | 180/12996 | 233/15403 | 359/16827 | 484/23207 | 235/34047 | 205/13560 |
| excluded conf/preprint | 4106 | 2 | 0.0 | 0/409 | 1/438 | 0/615 | 1/1006 | 0/1429 | 0/168 |
| SJR unmatched | 7922 | 132 | 1.7 | 20/822 | 20/1190 | 27/1156 | 33/1598 | 18/2255 | 14/901 |
| Q1/Q2 eligible (97,492) | 97492 | 1468 | 1.5 | 155/11191 | 203/13136 | 311/14128 | 417/19372 | 205/28873 | 177/10757 |
| prefilter: application | 80733 | 465 | 0.6 | 81/10127 | 83/11792 | 101/12073 | 90/15668 | 44/22974 | 66/8066 |
| prefilter: retained (16,759) | 16759 | 1003 | 6.0 | 74/1064 | 120/1344 | 210/2055 | 327/3704 | 161/5899 | 111/2691 |
| stance valid, 2021–2026 (16,747) | 16747 | 1003 | 6.0 | 74/1063 | 120/1343 | 210/2054 | 327/3700 | 161/5898 | 111/2689 |
| critical (5,161) | 5161 | 412 | 8.0 | 25/270 | 48/333 | 80/624 | 151/1228 | 71/1828 | 37/878 |

## 4. Other missing-data items

- Specialty FAILED in `specialty_classifications.csv` overall: 13 (of 16,759); within the 16,747 analytic set: 13. Specialty labels exist only for the 16,759 retained records (see T9).
- First-author country: two resolvers exist. The Figure 4 / Table S7 resolver (`resolve_country`) leaves 1,628/16,747 (9.7%) unresolved, i.e. 90.3% resolved (manuscript: 90.3%). `geography_classifications.csv` (Table S9 regions) has region Unknown for 593 (3.5%). Empty first-affiliation field: 274.
- Stance batch: one retrieval crashed on an empty `content` list (IndexError in `classify_stance_batch.py`, `output/stance_batch_poll.log`) and was resumed; final FAILED = 10.
- Theme batch: succeeded 5,160, errored 1 (`themes_batch_poll.log`); the errored record received ['other'] and cannot be distinguished from genuine 'other'-only records (51).
- SJR log reports Q1+Q2 = 98,626 as 88.1% of eligible (98,626/112,011 = 88.05%); the manuscript says 88.0%.
- Year field: retrieval used PDAT monthly windows; `pub_year` comes from `PubDate/Year` (or MedlineDate). Two records dated 2020 and one dated 2018 entered through PDAT windows (see T9).

## 5. Nested flow list (for a JARS flowchart)

- Records identified in PubMed (monthly windows): 129,557
  - Excluded: duplicate PMIDs across windows: 13,440
- Unique records: 116,117
  - Excluded: conference proceedings / preprints: 4,106
- Records eligible for SJR matching: 112,011
  - Excluded: journal not matched in SCImago: 7,922
  - Set aside: Q3 journals (comparison arm): 5,463 (after cutoff 5,433)
- Q1/Q2 records: 98,626
  - Excluded: cover date after April 2026: 1,134
- Q1/Q2 records screened by the AI-engagement prefilter: 97,492
  - Excluded: application (AI as method): 80,733 (of which 96 failure-branch defaults)
- Discourse or evaluative records: 16,759 (discourse 8,899; evaluative 7,860)
  - Excluded: stance unparseable: 10
- Valid stance labels: 16,749
  - Excluded: dated 2020: 2
- Analytic set, 2021–April 2026: 16,747
  - Reported separately (descriptive): January–April 2026: 2,689
  - Primary temporal set, 2021–2025: 14,058
  - Specialty analyses: 16,734 (excluded: specialty FAILED 13)
  - Country analyses: 15,119 resolved (unresolved 1,628; 9.7%)
  - Critical (Alarm or Caution): 5,161 → theme analysis 5,161 (fallback to ['other'] in 1 per batch log)
    - Mechanism classification: parsed 5,159 (excluded: unparseable 2)
      - Excluded: title-only: 412
      - Abstract-present critical records: 4,747
        - Hallucination-gated subset: 2,226
