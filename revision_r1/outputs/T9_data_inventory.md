# T9 · Data inventory for Batch 2 (read-only)

Script: `revision_r1/scripts/t9_data_inventory.py`. No API calls.

## 1. Publication dates (D3)

Field used: `fetch_pubmed_medical.py::parse_pubmed_xml` (lines 179–187) reads `PubDate/Year` and `PubDate/Month` **with default `"Jan"` when Month is absent**, falling back to `PubDate/MedlineDate` (year = first 4 characters). `ArticleDate` (electronic publication date) and `PubDate/Day` are not read. Retrieval windows used `[PDAT]` month by month; `pub_year` (analysis) is from PubDate. Stored as the string `pub_date` (e.g. `2023 Mar`).

Format of `pub_date` in the 16,747 analytic records, by year:

| pub_year | MedlineDate range | MedlineDate season/year range | PubDate Year+Month (Jan may be the parser default) | other | All |
|---|---|---|---|---|---|
| 2021 | 5 | 0 | 1058 | 0 | 1063 |
| 2022 | 2 | 0 | 1341 | 0 | 1343 |
| 2023 | 8 | 0 | 2046 | 0 | 2054 |
| 2024 | 15 | 0 | 3685 | 0 | 3700 |
| 2025 | 26 | 3 | 5868 | 1 | 5898 |
| 2026 | 36 | 1 | 2652 | 0 | 2689 |
| All | 92 | 4 | 16650 | 1 | 16747 |

Month distribution (records with a month), by year; January share is the check for the parser default (expected ≈ 8.3% if months were uniform; for 2026 the window is Jan–Apr):

| pub_year | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | Jan share % |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2021 | 174 | 59 | 85 | 68 | 69 | 95 | 92 | 81 | 79 | 78 | 68 | 115 | 16.4 |
| 2022 | 253 | 107 | 105 | 82 | 110 | 91 | 90 | 88 | 108 | 101 | 109 | 99 | 18.8 |
| 2023 | 355 | 105 | 121 | 92 | 127 | 138 | 143 | 156 | 187 | 238 | 172 | 220 | 17.3 |
| 2024 | 658 | 224 | 231 | 258 | 274 | 271 | 254 | 273 | 312 | 334 | 295 | 315 | 17.8 |
| 2025 | 1096 | 303 | 392 | 376 | 374 | 405 | 399 | 410 | 491 | 535 | 501 | 612 | 18.6 |
| 2026 | 845 | 568 | 631 | 644 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 31.4 |

Records per quarter, 2021–2025 (analytic set; month as stored, so Q1 includes any Jan defaults):

| pub_year | 1 | 2 | 3 | 4 | All |
|---|---|---|---|---|---|
| 2021 | 318 | 232 | 252 | 261 | 1063 |
| 2022 | 465 | 283 | 286 | 309 | 1343 |
| 2023 | 581 | 357 | 486 | 630 | 2054 |
| 2024 | 1113 | 803 | 839 | 944 | 3699 |
| 2025 | 1791 | 1155 | 1300 | 1648 | 5894 |
| All | 4268 | 2830 | 3163 | 3792 | 14053 |

Smallest quarter: 232 records; critical records per quarter range 62–527. Records without a month: 5 (2021–2025).

## 2. Journal identifiers (D4a)

Stored columns: ['pmid', 'year', 'pub_date', 'title', 'abstract', 'journal', 'journal_abbr', 'pub_type', 'first_author', 'first_affiliation', 'doi']. **No NLM Unique ID and no ISSN** are stored (the parser reads `Journal/Title` and `Journal/ISOAbbreviation` only). ISSN is available indirectly from the SJR files (`Issn` column) through the same title match used for quartiles.

Unique journals in the analytic set (exact `journal` string, case-folded): **2,462**; by ISO abbreviation: 2,462.

| statistic | value |
|---|---|
| journals | 2462 |
| records | 16747 |
| mean | 7 |
| min | 1 |
| 25% | 1 |
| median | 2 |
| 75% | 6 |
| 90% | 13 |
| 99% | 85 |
| max | 457 |
| journals with 1 record | 845 |
| journals with ≥10 | 353 |
| journals with ≥50 | 49 |
| records in top 20 journals | 3320 |

Top 15 journals by records:

| journal | records |
|---|---|
| journal of medical internet research | 457 |
| scientific reports | 343 |
| diagnostics (basel, switzerland) | 242 |
| european radiology | 209 |
| npj digital medicine | 175 |
| journal of clinical medicine | 175 |
| journal of the american medical informatics association : jamia | 152 |
| international journal of medical informatics | 140 |
| plos one | 139 |
| digital health | 135 |
| bmc medical education | 134 |
| frontiers in public health | 132 |
| jmir medical education | 121 |
| european journal of radiology | 120 |
| frontiers in medicine | 117 |

## 3. MeSH headings and author keywords (D5)

**Not stored.** No MeSH or keyword column in any corpus CSV (has_mesh_column = False); the parser does not read `MeshHeadingList` or `KeywordList`, and the raw PubMed XML was not saved (0 .xml files in the repository). Completeness by year therefore cannot be measured locally; it requires an E-utilities `efetch` of the 16,759 retained PMIDs (not done).

## 4. Affiliations (D5)

Only the **first author's first affiliation** is stored (`first_affiliation`: `authors[0]` → first `AffiliationInfo/Affiliation`, `fetch_pubmed_medical.py` lines 193–201). Other authors' affiliations, secondary affiliations of the first author, and the author count are not stored, and no raw XML is available locally. Empty `first_affiliation` in the analytic set: 274.

## 5. Excluded `application` records (D1, X2)

- Q1/Q2 records labelled `application`: **80,733** (of which 96 are failure-branch defaults, T1).
- Full abstracts stored locally: 80,268 (99.4%) have a non-empty abstract; 465 are title-only. Abstracts are stored untruncated (identical to the pre-prefilter corpus for 100.0% of records; truncation to 300 characters happened only in the prompt). Abstract length: median 1,738 characters, 95th percentile 2,660.

By year:

| pub_year | records | with_abstract |
|---|---|---|
| 2018 | 1 | 1 |
| 2020 | 32 | 32 |
| 2021 | 10127 | 10046 |
| 2022 | 11792 | 11709 |
| 2023 | 12073 | 11972 |
| 2024 | 15668 | 15578 |
| 2025 | 22974 | 22930 |
| 2026 | 8066 | 8000 |

**Cost estimate for re-running the prefilter on title + full abstract** (model `claude-haiku-4-5-20251001`, Batch API, same system prompt, max_tokens 120):

| item | value |
|---|---|
| requests | 80,733 |
| input tokens (est.) | 63.1 M |
|   per request, median | 772 |
| output tokens (est., 25/request) | 2.02 M |
| price (Haiku 4.5, per MTok) | $1.00 in / $5.00 out |
| standard cost | $73 |
| Batch API cost (50%) | **$37** |
| for comparison: input tokens with 300-char truncation | 33.3 M |

Assumptions: tokens ≈ characters / 4 (heuristic; `messages.count_tokens` would give exact counts but was not called); 25 output tokens per JSON reply; no prompt caching (the system prompt, 1,156 characters, is below the minimum cacheable prefix). Prices are Anthropic first-party list prices for Claude Haiku 4.5 ($1/$5 per MTok) with the 50% Batch discount; confirm before running. A run on all 97,492 eligible records would cost roughly $44 (Batch).

## 6. Specialty labels

`output/specialty_classifications.csv` has 16,759 rows; PMID set equals the 16,759 retained (discourse + evaluative) records: **True**. Overlap with the 80,733 application records: 0. So specialty labels exist only for retained records (confirmed).

