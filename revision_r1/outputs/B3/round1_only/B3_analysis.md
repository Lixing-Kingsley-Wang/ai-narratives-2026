# B3 · Symmetric endorsement re-classification (X1, D2b)

Favourable records classified: 10,749 (2021–Apr 2026); flag yes 1,356, no 9,386, FAILED 7 (model wrote prose before the JSON within max_tokens 30; resubmission was refused by the API for insufficient credit). FAILED records stay in denominators and are not counted as Strong endorsement.

## 1. Symmetric scale distribution

| period | N | Alarm | Caution | Neutral | Cautious Optimism (flag no) | Strong endorsement (flag yes) | Favourable, flag FAILED |
|---|---|---|---|---|---|---|---|
| 2021–2025 | 14058 | 5.3% (749) | 25.1% (3,534) | 5.1% (721) | 56.0% (7,871) | 8.4% (1,179) | 0.0% (4) |
| 2021 | 1063 | 2.7% (29) | 22.7% (241) | 7.3% (78) | 56.3% (599) | 10.8% (115) | 0.1% (1) |
| 2022 | 1343 | 2.6% (35) | 22.2% (298) | 7.9% (106) | 54.1% (727) | 13.2% (177) | 0.0% (0) |
| 2023 | 2054 | 4.7% (97) | 25.7% (527) | 6.3% (130) | 53.5% (1,098) | 9.8% (202) | 0.0% (0) |
| 2024 | 3700 | 6.8% (253) | 26.4% (975) | 5.1% (189) | 53.7% (1,987) | 8.0% (295) | 0.0% (1) |
| 2025 | 5898 | 5.7% (335) | 25.3% (1,493) | 3.7% (218) | 58.7% (3,460) | 6.6% (390) | 0.0% (2) |
| Jan–Apr 2026 | 2689 | 6.2% (167) | 26.4% (711) | 4.3% (116) | 56.3% (1,515) | 6.6% (177) | 0.1% (3) |

## 2. Trend 2021–2025 (denominator: all analytic records in the year)

Annual %, bootstrap 95% CI (1000 joint resamples, seed 42), n/N.

| outcome | 2021 | 2022 | 2023 | 2024 | 2025 | Spearman ρ (exact P) | OR/yr (95% CI), P |
|---|---|---|---|---|---|---|---|
| Strong endorsement (flag yes) | 10.82 (9.05–12.72); 115/1063 | 13.18 (11.32–14.86); 177/1343 | 9.83 (8.57–11.03); 202/2054 | 7.97 (7.09–8.82); 295/3700 | 6.61 (5.97–7.28); 390/5898 | -0.90 (P=.083) | 0.834 (0.798–0.871), P<.001 |
| Strong endorsement, upper bound (FAILED as yes) | 10.91 (9.17–12.81); 116/1063 | 13.18 (11.32–14.86); 177/1343 | 9.83 (8.57–11.03); 202/2054 | 8.00 (7.12–8.85); 296/3700 | 6.65 (6.01–7.31); 392/5898 | -0.90 (P=.083) | 0.834 (0.798–0.871), P<.001 |
| Advocacy (production, T4) | 2.92 (1.93–4.01); 31/1063 | 2.01 (1.30–2.76); 27/1343 | 1.95 (1.37–2.60); 40/2054 | 1.46 (1.10–1.85); 54/3700 | 1.12 (0.88–1.40); 66/5898 | -1.00 (P=.017) | 0.793 (0.721–0.872), P<.001 |

## 3. Consistency checks

| production stance | period | flag yes | % | exact 95% CI | FAILED |
|---|---|---|---|---|---|
| Advocacy | 2021–Apr 2026 | 91/235 | 38.7 | 32.5–45.3 | 0 |
| Advocacy | 2021–2025 | 83/218 | 38.1 | 31.6–44.9 | 0 |
| Advocacy | 2021 | 10/31 | 32.3 | 16.7–51.4 | 0 |
| Advocacy | 2022 | 12/27 | 44.4 | 25.5–64.7 | 0 |
| Advocacy | 2023 | 16/40 | 40.0 | 24.9–56.7 | 0 |
| Advocacy | 2024 | 17/54 | 31.5 | 19.5–45.6 | 0 |
| Advocacy | 2025 | 28/66 | 42.4 | 30.3–55.2 | 0 |
| Advocacy | 2026 | 8/17 | 47.1 | 23.0–72.2 | 0 |
| Cautious Optimism | 2021–Apr 2026 | 1265/10514 | 12.0 | 11.4–12.7 | 7 |
| Cautious Optimism | 2021–2025 | 1096/8836 | 12.4 | 11.7–13.1 | 4 |
| Cautious Optimism | 2021 | 105/684 | 15.4 | 12.7–18.3 | 1 |
| Cautious Optimism | 2022 | 165/877 | 18.8 | 16.3–21.6 | 0 |
| Cautious Optimism | 2023 | 186/1260 | 14.8 | 12.8–16.8 | 0 |
| Cautious Optimism | 2024 | 278/2229 | 12.5 | 11.1–13.9 | 1 |
| Cautious Optimism | 2025 | 362/3786 | 9.6 | 8.6–10.5 | 2 |
| Cautious Optimism | 2026 | 169/1678 | 10.1 | 8.7–11.6 | 3 |

## 4. Agreement with existing human labels (model-favourable validation records)

| set | n | flag FAILED | 2×2 (TP, FN, FP, TN) human Advocacy vs flag yes | sensitivity | PPV | Cohen κ | human labels among flag yes |
|---|---|---|---|---|---|---|---|
| all model-favourable | 130 | 0 | 10, 14, 8, 98 | 10/24 = 0.417 (0.211–0.633) | 10/18 = 0.556 (0.316–0.800) | 0.378 (0.146–0.598) | Advocacy 10; Cautious Optimism 8 |
| in-scope (T2 layer A) | 112 | 0 | 10, 14, 8, 80 | 10/24 = 0.417 (0.238–0.633) | 10/18 = 0.556 (0.333–0.789) | 0.358 (0.141–0.574) | Advocacy 10; Cautious Optimism 8 |

For reference, production Advocacy vs human Advocacy on the same records is in T2 (§3, binary Advocacy view).

## 5. Secondary: misclassification-corrected prevalence (target: human Advocacy)

Batch 1 T2 estimator with strata = model stance × flag; P(human Advocacy | stratum) from all 300 validation records; bootstrap resamples validation records within strata and corpus records jointly (1000, seed 42). Strata with no validation record contribute 0 and are listed.

| stratum | validation n | human Advocacy in stratum | P(human Advocacy | stratum) | flag (<10 validation records) |
|---|---|---|---|---|
| Advocacy, flag no | 17 | 8 | 0.471 |  |
| Advocacy, flag yes | 13 | 9 | 0.692 |  |
| Alarm | 40 | 0 | 0.000 |  |
| Caution | 60 | 0 | 0.000 |  |
| Cautious Optimism, flag FAILED | 0 | 0 | no records | <10 |
| Cautious Optimism, flag no | 95 | 6 | 0.063 |  |
| Cautious Optimism, flag yes | 5 | 1 | 0.200 | <10 |
| Neutral | 70 | 0 | 0.000 |  |

| year | corrected human-Advocacy prevalence % (95% CI) |
|---|---|
| 2021 | 6.99 (3.02–11.79) |
| 2022 | 6.95 (2.71–12.70) |
| 2023 | 6.20 (2.63–10.54) |
| 2024 | 5.62 (2.39–9.60) |
| 2025 | 5.52 (2.36–9.26) |

