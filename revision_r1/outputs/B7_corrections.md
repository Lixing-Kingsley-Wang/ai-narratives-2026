# B7 · Numeric corrections (E13, D8)

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

