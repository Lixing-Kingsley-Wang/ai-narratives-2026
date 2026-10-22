# T2 · Stance per-class performance and Advocacy robustness (D2b; supports X1)

Script: `revision_r1/scripts/t2_stance_perclass.py`. Validation inputs: `output/validation/kingsly_coding_sheet.xlsx` (human) joined to `kingsly_validation_full.csv` (model) on `record_id`; in-scope layer = compute_kappa.py 'Sensitivity A' (excludes NO_STANCE, OUT_OF_SCOPE, DATA_INSUFFICIENT flags in `human_notes`).

## 1. Reproduction of Table S18

- (a) in-scope, n=225: **reproduced exactly**
- (b) all records, n=300: **reproduced exactly**

Table S18(c) exact and adjacent counts recomputed from (a): Alarm 31/36 exact, 4 adjacent; Caution 33/58 exact, 11 adjacent; Neutral 10/14 exact, 4 adjacent; Cautious Optimism 61/93 exact, 19 adjacent; Advocacy 17/24 exact, 7 adjacent.

## 2. Per-class precision, recall, F1 (bootstrap 95% CI, 1000 resamples, seed 42)

Precision = share of model-assigned labels that the human agreed with; recall = share of human-coded records the model labelled the same. Support = human row total.

**Primary: in-scope records (n=225)**

| class | support (human) | n (model) | precision | recall | F1 |
|---|---|---|---|---|---|
| Alarm | 36 | 40 | 0.78 (0.62–0.89) | 0.86 (0.73–0.97) | 0.82 (0.70–0.90) |
| Caution | 58 | 50 | 0.66 (0.53–0.79) | 0.57 (0.44–0.68) | 0.61 (0.49–0.71) |
| Neutral | 14 | 23 | 0.43 (0.23–0.65) | 0.71 (0.44–0.93) | 0.54 (0.32–0.71) |
| Cautious Optimism | 93 | 86 | 0.71 (0.61–0.80) | 0.66 (0.55–0.75) | 0.68 (0.59–0.76) |
| Advocacy | 24 | 26 | 0.65 (0.46–0.83) | 0.71 (0.50–0.89) | 0.68 (0.51–0.81) |
| macro-F1 | 225 | 225 |  |  | 0.67 (0.59–0.73) |

**Secondary: all records (n=300)**

| class | support (human) | n (model) | precision | recall | F1 |
|---|---|---|---|---|---|
| Alarm | 36 | 40 | 0.78 (0.64–0.90) | 0.86 (0.74–0.97) | 0.82 (0.71–0.90) |
| Caution | 59 | 60 | 0.57 (0.44–0.69) | 0.58 (0.45–0.69) | 0.57 (0.46–0.67) |
| Neutral | 88 | 70 | 0.81 (0.72–0.90) | 0.65 (0.55–0.74) | 0.72 (0.64–0.79) |
| Cautious Optimism | 93 | 100 | 0.61 (0.51–0.70) | 0.66 (0.56–0.74) | 0.63 (0.55–0.71) |
| Advocacy | 24 | 30 | 0.57 (0.38–0.75) | 0.71 (0.53–0.88) | 0.63 (0.45–0.77) |
| macro-F1 | 300 | 300 |  |  | 0.67 (0.62–0.73) |

## 3. Collapsed views

### 3-class (critical / neutral / favourable), in-scope (n=225)

| Human \ Model | critical | neutral | favourable | Row total |
|---|---|---|---|---|
| critical | 76 | 3 | 15 | 94 |
| neutral | 1 | 10 | 3 | 14 |
| favourable | 13 | 10 | 94 | 117 |
| Column total | 90 | 23 | 112 | 225 |

Raw agreement 180/225 = 80.0%; Cohen κ (unweighted) = 0.648; quadratic-weighted κ = 0.684; Gwet AC1 = 0.721.

| class | support (human) | n (model) | precision | recall | F1 |
|---|---|---|---|---|---|
| critical | 94 | 90 | 0.84 (0.76–0.92) | 0.81 (0.73–0.88) | 0.83 (0.76–0.88) |
| neutral | 14 | 23 | 0.43 (0.23–0.65) | 0.71 (0.44–0.93) | 0.54 (0.32–0.71) |
| favourable | 117 | 112 | 0.84 (0.77–0.90) | 0.80 (0.72–0.87) | 0.82 (0.76–0.87) |
| macro-F1 | 225 | 225 |  |  | 0.73 (0.64–0.80) |

### Binary: Advocacy vs not Advocacy, in-scope (n=225)

TP=17, FN=7, FP=9, TN=192 (rows human, positive = Advocacy).

| metric | n/N | estimate (95% CI) |
|---|---|---|
| sensitivity | 17/24 | 0.708 (0.500–0.889) |
| specificity | 192/201 | 0.955 (0.922–0.980) |
| PPV | 17/26 | 0.654 (0.464–0.833) |
| NPV | 192/199 | 0.965 (0.938–0.990) |
| F1 |  | 0.680 (0.512–0.812) |
| accuracy | 209/225 | 0.929 (0.893–0.964) |
| kappa |  | 0.640 (0.460–0.790) |
| AC1 |  | 0.911 (0.860–0.955) |
| prevalence_human | 24/225 | 0.107 (0.067–0.147) |

### Binary: Critical (Alarm+Caution) vs not critical, in-scope (n=225)

TP=76, FN=18, FP=14, TN=117 (rows human, positive = Critical (Alarm+Caution)).

| metric | n/N | estimate (95% CI) |
|---|---|---|
| sensitivity | 76/94 | 0.809 (0.725–0.881) |
| specificity | 117/131 | 0.893 (0.839–0.944) |
| PPV | 76/90 | 0.844 (0.763–0.918) |
| NPV | 117/135 | 0.867 (0.810–0.920) |
| F1 |  | 0.826 (0.762–0.879) |
| accuracy | 193/225 | 0.858 (0.809–0.898) |
| kappa |  | 0.706 (0.606–0.791) |
| AC1 |  | 0.725 (0.632–0.807) |
| prevalence_human | 94/225 | 0.418 (0.356–0.484) |

### 3-class (critical / neutral / favourable), all (n=300)

| Human \ Model | critical | neutral | favourable | Row total |
|---|---|---|---|---|
| critical | 77 | 3 | 15 | 95 |
| neutral | 10 | 57 | 21 | 88 |
| favourable | 13 | 10 | 94 | 117 |
| Column total | 100 | 70 | 130 | 300 |

Raw agreement 228/300 = 76.0%; Cohen κ (unweighted) = 0.635; quadratic-weighted κ = 0.644; Gwet AC1 = 0.643.

| class | support (human) | n (model) | precision | recall | F1 |
|---|---|---|---|---|---|
| critical | 95 | 100 | 0.77 (0.69–0.85) | 0.81 (0.73–0.89) | 0.79 (0.73–0.85) |
| neutral | 88 | 70 | 0.81 (0.72–0.90) | 0.65 (0.55–0.74) | 0.72 (0.64–0.79) |
| favourable | 117 | 130 | 0.72 (0.65–0.80) | 0.80 (0.73–0.87) | 0.76 (0.70–0.82) |
| macro-F1 | 300 | 300 |  |  | 0.76 (0.71–0.81) |

### Binary: Advocacy vs not Advocacy, all (n=300)

TP=17, FN=7, FP=13, TN=263 (rows human, positive = Advocacy).

| metric | n/N | estimate (95% CI) |
|---|---|---|
| sensitivity | 17/24 | 0.708 (0.526–0.880) |
| specificity | 263/276 | 0.953 (0.924–0.975) |
| PPV | 17/30 | 0.567 (0.375–0.750) |
| NPV | 263/270 | 0.974 (0.955–0.989) |
| F1 |  | 0.630 (0.453–0.767) |
| accuracy | 280/300 | 0.933 (0.907–0.957) |
| kappa |  | 0.593 (0.406–0.741) |
| AC1 |  | 0.920 (0.885–0.951) |
| prevalence_human | 24/300 | 0.080 (0.050–0.113) |

### Binary: Critical (Alarm+Caution) vs not critical, all (n=300)

TP=77, FN=18, FP=23, TN=182 (rows human, positive = Critical (Alarm+Caution)).

| metric | n/N | estimate (95% CI) |
|---|---|---|
| sensitivity | 77/95 | 0.811 (0.733–0.888) |
| specificity | 182/205 | 0.888 (0.846–0.930) |
| PPV | 77/100 | 0.770 (0.688–0.850) |
| NPV | 182/200 | 0.910 (0.870–0.947) |
| F1 |  | 0.790 (0.725–0.849) |
| accuracy | 259/300 | 0.863 (0.823–0.900) |
| kappa |  | 0.689 (0.599–0.771) |
| AC1 |  | 0.756 (0.682–0.824) |
| prevalence_human | 95/300 | 0.317 (0.263–0.370) |

## 4. Non-adjacent disagreements (≥2 steps on the ordinal scale)

| layer | n | disagreements | adjacent (1 step) | 2 steps | 3 steps | 4 steps | non-adjacent total |
|---|---|---|---|---|---|---|---|
| in-scope (n=225) | 225 | 73 | 45 | 26 | 2 | 0 | 28 |
| all (n=300) | 300 | 100 | 68 | 30 | 2 | 0 | 32 |

Pairs (all 300): human Alarm → model Cautious Optimism: 1; human Caution → model Cautious Optimism: 14; human Cautious Optimism → model Alarm: 1; human Cautious Optimism → model Caution: 12; human Neutral → model Advocacy: 4.

## 5. Agreement by publication-year band (descriptive)

| layer | years | n | exact agreement | quadratic κ | unweighted κ | critical: human/model | Advocacy: human/model/both |
|---|---|---|---|---|---|---|---|
| in-scope (n=225) | 2021–2022 | 38 | 24/38 (63.2%) | 0.781 | 0.490 | 14/7 | 5/7/4 |
| in-scope (n=225) | 2023 | 25 | 14/25 (56.0%) | 0.623 | 0.409 | 10/11 | 1/3/1 |
| in-scope (n=225) | 2024–2026 | 161 | 113/161 (70.2%) | 0.809 | 0.595 | 70/72 | 18/16/12 |
| in-scope (n=225) | 2022 | 21 | 11/21 (52.4%) | 0.723 | 0.375 | 8/3 | 3/4/2 |
| in-scope (n=225) | 2024 | 53 | 39/53 (73.6%) | 0.822 | 0.648 | 27/26 | 6/5/5 |
| in-scope (n=225) | 2025 | 71 | 52/71 (73.2%) | 0.841 | 0.630 | 25/29 | 10/9/6 |
| in-scope (n=225) | 2026 | 37 | 22/37 (59.5%) | 0.710 | 0.438 | 18/17 | 2/2/1 |
| all (n=300) | 2021–2022 | 55 | 34/55 (61.8%) | 0.706 | 0.488 | 14/8 | 5/9/4 |
| all (n=300) | 2023 | 36 | 22/36 (61.1%) | 0.579 | 0.479 | 10/11 | 1/4/1 |
| all (n=300) | 2024–2026 | 208 | 143/208 (68.8%) | 0.783 | 0.594 | 71/81 | 18/17/12 |
| all (n=300) | 2021 | 22 | 15/22 (68.2%) | 0.767 | 0.560 | 6/4 | 2/4/2 |
| all (n=300) | 2022 | 33 | 19/33 (57.6%) | 0.658 | 0.418 | 8/4 | 3/5/2 |
| all (n=300) | 2024 | 67 | 48/67 (71.6%) | 0.801 | 0.634 | 27/29 | 6/5/5 |
| all (n=300) | 2025 | 95 | 67/95 (70.5%) | 0.806 | 0.615 | 26/33 | 10/10/6 |
| all (n=300) | 2026 | 46 | 28/46 (60.9%) | 0.694 | 0.482 | 18/19 | 2/2/1 |

Validation sample year distribution (all 300): 2020: 1, 2021: 22, 2022: 33, 2023: 36, 2024: 67, 2025: 95, 2026: 46. Single years shown where n≥20.

## 6. Misclassification-corrected annual prevalence, 2021–2025

**Sampling design (confirmed from `export_validation.py`):** stratified by model-assigned stance with fixed targets Alarm 40, Caution 60, Neutral 70, Cautious Optimism 100, Advocacy 30 (`STANCE_TARGETS`, `random.seed(42)`), from records with a valid stance **and a non-empty abstract** in `classified_medical_Q1Q2.csv` (all years, including 2020). Pool sizes below are recomputed from the current file.

| model stratum | sampling pool (valid stance, abstract present, all years) | sampled | sampling fraction | in-scope (layer A) |
|---|---|---|---|---|
| Alarm | 844 | 40 | 4.74% | 40 |
| Caution | 3905 | 60 | 1.54% | 50 |
| Neutral | 635 | 70 | 11.02% | 23 |
| Cautious Optimism | 10184 | 100 | 0.98% | 86 |
| Advocacy | 178 | 30 | 16.85% | 26 |

**Estimator.** For year y and human class h: corrected prevalence = Σ_c (share of year-y corpus records with model label c) × P(human = h | model = c). P(h | c) is estimated within each model-label stratum of the validation set (stratified sampling makes this conditional unbiased within stratum). CIs: 1000 joint bootstrap draws (seed 42) resampling validation records within model strata and corpus records (2021–2025 set as a whole).

**Assumptions (stated plainly):** (i) P(human | model) is constant across years; (ii) the validation pool excluded title-only records, so applying P to all corpus records assumes title-only records are misclassified like abstract-present ones (an abstract-present-only corpus row is given as a check); (iii) in the primary analysis, records the human judged not codable/out of scope count as human Neutral (as in Table S18b).

P(human | model), primary: all 300:

|  | human:Alarm | human:Caution | human:Neutral | human:Caut. Opt. | human:Advocacy |
|---|---|---|---|---|---|
| model:Alarm | 0.775 | 0.200 | 0.000 | 0.025 | 0.000 |
| model:Caution | 0.067 | 0.567 | 0.167 | 0.200 | 0.000 |
| model:Neutral | 0.000 | 0.043 | 0.814 | 0.143 | 0.000 |
| model:Caut. Opt. | 0.010 | 0.140 | 0.170 | 0.610 | 0.070 |
| model:Advocacy | 0.000 | 0.000 | 0.133 | 0.300 | 0.567 |

P(human | model), sensitivity: in-scope 225:

|  | human:Alarm | human:Caution | human:Neutral | human:Caut. Opt. | human:Advocacy |
|---|---|---|---|---|---|
| model:Alarm | 0.775 | 0.200 | 0.000 | 0.025 | 0.000 |
| model:Caution | 0.080 | 0.660 | 0.020 | 0.240 | 0.000 |
| model:Neutral | 0.000 | 0.130 | 0.435 | 0.435 | 0.000 |
| model:Caut. Opt. | 0.012 | 0.163 | 0.035 | 0.709 | 0.081 |
| model:Advocacy | 0.000 | 0.000 | 0.000 | 0.346 | 0.654 |

**primary: all 300; corpus = all records**

| outcome | year | N (year) | observed % (95% CI) | corrected % (95% CI) |
|---|---|---|---|---|
| Advocacy | 2021 | 1063 | 2.92 (2.00 to 4.07) | 6.16 (3.13 to 9.65) |
| Critical | 2021 | 1063 | 25.40 (22.90 to 28.09) | 26.99 (21.82 to 32.64) |
| Advocacy | 2022 | 1343 | 2.01 (1.35 to 2.78) | 5.71 (2.75 to 8.99) |
| Critical | 2022 | 1343 | 24.80 (22.59 to 27.27) | 26.73 (21.70 to 32.49) |
| Advocacy | 2023 | 2054 | 1.95 (1.35 to 2.59) | 5.40 (2.67 to 8.50) |
| Critical | 2023 | 2054 | 30.38 (28.53 to 32.42) | 30.33 (25.13 to 35.53) |
| Advocacy | 2024 | 3700 | 1.46 (1.07 to 1.85) | 5.04 (2.40 to 8.10) |
| Critical | 2024 | 3700 | 33.19 (31.70 to 34.77) | 32.61 (27.71 to 37.96) |
| Advocacy | 2025 | 5898 | 1.12 (0.85 to 1.41) | 5.13 (2.33 to 8.41) |
| Critical | 2025 | 5898 | 30.99 (29.85 to 32.16) | 31.36 (26.25 to 36.75) |
| Advocacy | Δ 2025−2021 (pp) |  | -1.80 (-2.95 to -0.79) | -1.03 (-1.79 to -0.42) |
| Critical | Δ 2025−2021 (pp) |  | 5.59 (2.52 to 8.29) | 4.37 (2.61 to 5.99) |

**primary: all 300; corpus = abstract-present records only**

| outcome | year | N (year) | observed % (95% CI) | corrected % (95% CI) |
|---|---|---|---|---|
| Advocacy | 2021 | 989 | 2.63 (1.67 to 3.64) | 6.12 (3.00 to 9.77) |
| Critical | 2021 | 989 | 24.77 (22.36 to 27.32) | 26.75 (21.34 to 32.51) |
| Advocacy | 2022 | 1223 | 1.47 (0.83 to 2.17) | 5.59 (2.41 to 9.26) |
| Critical | 2022 | 1223 | 23.30 (20.94 to 25.85) | 26.10 (20.55 to 31.53) |
| Advocacy | 2023 | 1844 | 1.41 (0.92 to 1.98) | 5.31 (2.32 to 8.85) |
| Critical | 2023 | 1844 | 29.50 (27.36 to 31.52) | 30.12 (24.88 to 35.91) |
| Advocacy | 2024 | 3373 | 0.86 (0.56 to 1.17) | 4.92 (1.87 to 8.25) |
| Critical | 2024 | 3373 | 31.93 (30.26 to 33.44) | 32.21 (26.79 to 37.92) |
| Advocacy | 2025 | 5737 | 1.10 (0.83 to 1.39) | 5.18 (2.06 to 8.60) |
| Critical | 2025 | 5737 | 30.63 (29.40 to 31.77) | 31.19 (25.69 to 36.80) |
| Advocacy | Δ 2025−2021 (pp) |  | -1.53 (-2.53 to -0.53) | -0.94 (-1.61 to -0.35) |
| Critical | Δ 2025−2021 (pp) |  | 5.85 (2.92 to 8.56) | 4.44 (2.79 to 6.08) |

**sensitivity: in-scope 225; corpus = all records**

| outcome | year | N (year) | observed % (95% CI) | corrected % (95% CI) |
|---|---|---|---|---|
| Advocacy | 2021 | 1063 | 2.92 (1.93 to 3.99) | 7.14 (3.83 to 10.94) |
| Critical | 2021 | 1063 | 25.40 (23.13 to 28.15) | 31.62 (25.89 to 37.57) |
| Advocacy | 2022 | 1343 | 2.01 (1.30 to 2.76) | 6.63 (3.27 to 10.36) |
| Critical | 2022 | 1343 | 24.80 (22.54 to 27.18) | 31.38 (25.62 to 37.48) |
| Advocacy | 2023 | 2054 | 1.95 (1.37 to 2.56) | 6.27 (3.06 to 9.77) |
| Critical | 2023 | 2054 | 30.38 (28.29 to 32.56) | 35.12 (29.39 to 40.98) |
| Advocacy | 2024 | 3700 | 1.46 (1.10 to 1.85) | 5.86 (2.73 to 9.20) |
| Critical | 2024 | 3700 | 33.19 (31.76 to 34.70) | 37.34 (31.71 to 43.01) |
| Advocacy | 2025 | 5898 | 1.12 (0.88 to 1.41) | 5.96 (2.44 to 9.66) |
| Critical | 2025 | 5898 | 30.99 (29.83 to 32.25) | 35.95 (30.22 to 41.88) |
| Advocacy | Δ 2025−2021 (pp) |  | -1.80 (-2.89 to -0.81) | -1.19 (-2.02 to -0.48) |
| Critical | Δ 2025−2021 (pp) |  | 5.59 (2.60 to 8.25) | 4.33 (2.39 to 6.15) |

**sensitivity: in-scope 225; corpus = abstract-present records only**

| outcome | year | N (year) | observed % (95% CI) | corrected % (95% CI) |
|---|---|---|---|---|
| Advocacy | 2021 | 989 | 2.63 (1.71 to 3.69) | 7.10 (3.58 to 11.25) |
| Critical | 2021 | 989 | 24.77 (22.11 to 27.47) | 31.30 (25.05 to 37.80) |
| Advocacy | 2022 | 1223 | 1.47 (0.82 to 2.20) | 6.49 (2.95 to 10.67) |
| Critical | 2022 | 1223 | 23.30 (21.09 to 25.76) | 30.62 (24.41 to 37.64) |
| Advocacy | 2023 | 1844 | 1.41 (0.92 to 1.98) | 6.17 (2.87 to 10.15) |
| Critical | 2023 | 1844 | 29.50 (27.39 to 31.66) | 34.76 (28.70 to 41.28) |
| Advocacy | 2024 | 3373 | 0.86 (0.58 to 1.17) | 5.71 (2.54 to 9.56) |
| Critical | 2024 | 3373 | 31.93 (30.31 to 33.49) | 36.78 (30.64 to 43.31) |
| Advocacy | 2025 | 5737 | 1.10 (0.84 to 1.38) | 6.02 (2.79 to 9.95) |
| Critical | 2025 | 5737 | 30.63 (29.43 to 31.84) | 35.73 (29.62 to 42.29) |
| Advocacy | Δ 2025−2021 (pp) |  | -1.53 (-2.63 to -0.53) | -1.09 (-1.88 to -0.39) |
| Critical | Δ 2025−2021 (pp) |  | 5.85 (3.12 to 8.68) | 4.43 (2.64 to 6.33) |

## 7. Records coded Advocacy by the human or the model (for Peter's review)

37 records: both Advocacy 17, human only 7, model only 13.

| pmid | year | human | model | excluded_from_inscope_layer |
|---|---|---|---|---|
| 32974930 | 2021 | Neutral | Advocacy | True |
| 33731170 | 2021 | Advocacy | Advocacy | False |
| 34082064 | 2021 | Advocacy | Advocacy | False |
| 34527076 | 2021 | Cautious Optimism | Advocacy | False |
| 34972616 | 2022 | Advocacy | Advocacy | False |
| 35031822 | 2022 | Neutral | Advocacy | True |
| 35302963 | 2022 | Cautious Optimism | Advocacy | False |
| 35385184 | 2022 | Advocacy | Cautious Optimism | False |
| 35691440 | 2022 | Cautious Optimism | Advocacy | False |
| 35872988 | 2022 | Advocacy | Advocacy | False |
| 37055885 | 2023 | Cautious Optimism | Advocacy | False |
| 37459906 | 2023 | Cautious Optimism | Advocacy | False |
| 37574841 | 2023 | Neutral | Advocacy | True |
| 38259001 | 2023 | Advocacy | Advocacy | False |
| 37945100 | 2024 | Advocacy | Advocacy | False |
| 38284287 | 2024 | Advocacy | Advocacy | False |
| 39147901 | 2024 | Advocacy | Advocacy | False |
| 39175590 | 2024 | Advocacy | Cautious Optimism | False |
| 39186000 | 2024 | Advocacy | Advocacy | False |
| 39895671 | 2024 | Advocacy | Advocacy | False |
| 39473198 | 2025 | Cautious Optimism | Advocacy | False |
| 39847582 | 2025 | Neutral | Advocacy | True |
| 39851128 | 2025 | Advocacy | Advocacy | False |
| 39894601 | 2025 | Advocacy | Advocacy | False |
| 40095966 | 2025 | Cautious Optimism | Advocacy | False |
| 40214219 | 2025 | Advocacy | Cautious Optimism | False |
| 40246249 | 2025 | Advocacy | Advocacy | False |
| 40516520 | 2025 | Advocacy | Advocacy | False |
| 40540146 | 2025 | Advocacy | Advocacy | False |
| 40631924 | 2025 | Cautious Optimism | Advocacy | False |
| 40648241 | 2025 | Advocacy | Cautious Optimism | False |
| 40687630 | 2025 | Advocacy | Cautious Optimism | False |
| 40974075 | 2025 | Advocacy | Advocacy | False |
| 41256318 | 2025 | Advocacy | Cautious Optimism | False |
| 41667642 | 2026 | Advocacy | Advocacy | False |
| 41694518 | 2026 | Cautious Optimism | Advocacy | False |
| 41713400 | 2026 | Advocacy | Cautious Optimism | False |

## Output files

- [T2_perclass_inscope225.csv](T2_perclass_inscope225.csv)
- [T2_perclass_all300.csv](T2_perclass_all300.csv)
- [T2_collapsed_views.csv](T2_collapsed_views.csv)
- [T2_nonadjacent_records.csv](T2_nonadjacent_records.csv)
- [T2_agreement_by_year.csv](T2_agreement_by_year.csv)
- [T2_sampling_fractions.csv](T2_sampling_fractions.csv)
- [T2_corrected_prevalence.csv](T2_corrected_prevalence.csv)
- [T2_advocacy_records_for_review.csv](T2_advocacy_records_for_review.csv)
