# B6 · MeSH and keyword triangulation (D5)

Scripts `b6_fetch_mesh.py` (NCBI efetch, 84 batches of ≤200 PMIDs; raw XML gzipped locally in `outputs/B6/raw/`, SHA-256 manifest committed) and `b6_terms.py`. Retained records: 16,759; articles returned by NCBI: 16,756 (missing PMIDs listed in `b6_fetch_missing_pmids.txt`).

## Completeness by year (retained records)

| year | records | with_mesh | with_keywords | mesh_% | keywords_% |
|---|---|---|---|---|---|
| 2020 | 2.0 | 0.0 | 2.0 | 0.0 | 100.0 |
| 2021 | 1064.0 | 942.0 | 728.0 | 88.5 | 68.4 |
| 2022 | 1344.0 | 1147.0 | 959.0 | 85.3 | 71.4 |
| 2023 | 2055.0 | 1655.0 | 1460.0 | 80.5 | 71.0 |
| 2024 | 3704.0 | 2928.0 | 2720.0 | 79.0 | 73.4 |
| 2025 | 5899.0 | 4367.0 | 4815.0 | 74.0 | 81.6 |
| 2026 | 2691.0 | 1955.0 | 2222.0 | 72.6 | 82.6 |
| All | 16759.0 | 12994.0 | 12906.0 | 77.5 | 77.0 |

## Analysis 1 · Pre-specified lexicon trends (critical records, 2021–2025)

Match in title + abstract + author keywords (text lexicon) or MeSH descriptors. Annual shares with bootstrap CIs are in `B6_lexicon_annual.csv`.

| lexicon theme | records matched | 2021 → 2025 | Spearman ρ (exact P) | OR/yr (95% CI), P | LLM theme (T4) ρ / OR/yr | same direction | overlap: lexicon∩LLM / lexicon / LLM |
|---|---|---|---|---|---|---|---|
| Errors and hallucination | 801/4,283 | 8.1% (22/270) → 22.6% (414/1828) | +0.90 (P=.083) | 1.384 (1.284–1.492), P<.001 | +0.80 / 1.367 | yes | 588 / 801 / 1,971 |
| Patient safety | 727/4,283 | 13.7% (37/270) → 19.2% (351/1828) | +1.00 (P=.017) | 1.133 (1.056–1.215), P<.001 | +0.80 / 1.055 | yes | 551 / 727 / 2,755 |
| Regulation | 1,059/4,283 | 24.8% (67/270) → 29.9% (547/1828) | +0.00 (P=1.000) | 1.128 (1.062–1.198), P<.001 | -0.90 / 0.765 | no | 665 / 1,059 / 1,593 |
| Ethics and bias | 1,815/4,283 | 44.1% (119/270) → 44.8% (819/1828) | -0.20 (P=.783) | 1.008 (0.959–1.060), P=.753 | -0.80 / 0.915 | no | 1,140 / 1,815 / 1,483 |

## Analysis 2 · Emerging terms (2024–2025 vs 2021–2022)

records 2024–2025 / 2021–2022: 9,603 / 2,408; qualifying terms (≥20 records): 596. Weighted log-odds with informative Dirichlet prior (background = 16,759 retained records, α0 = 1,000); z = δ/σ.

| direction | term | z | df_group1 | df_group2 |
|---|---|---|---|---|
| more in 2024–2025 | large language models | 12.06 | 1416 | 0 |
| more in 2024–2025 | chatgpt | 11.26 | 1326 | 0 |
| more in 2024–2025 | male | 11.18 | 2003 | 212 |
| more in 2024–2025 | female | 10.90 | 2242 | 261 |
| more in 2024–2025 | generative artificial intelligence | 9.58 | 910 | 0 |
| more in 2024–2025 | adult | 9.56 | 1278 | 122 |
| more in 2024–2025 | middle aged | 9.34 | 1282 | 127 |
| more in 2024–2025 | surveys and questionnaires | 8.30 | 702 | 48 |
| more in 2024–2025 | language | 8.27 | 536 | 8 |
| more in 2024–2025 | large language model | 7.08 | 526 | 0 |
| more in 2024–2025 | aged | 5.53 | 866 | 119 |
| more in 2024–2025 | medical education | 5.51 | 253 | 11 |
| more in 2024–2025 | ai | 5.44 | 490 | 52 |
| more in 2024–2025 | attitude of health personnel | 5.38 | 243 | 11 |
| more in 2024–2025 | comprehension | 5.22 | 244 | 1 |
| more in 2024–2025 | chatbot | 5.09 | 205 | 7 |
| more in 2024–2025 | cross-sectional studies | 5.08 | 415 | 43 |
| more in 2024–2025 | patient education as topic | 5.07 | 266 | 0 |
| more in 2024–2025 | natural language processing | 4.99 | 576 | 73 |
| more in 2024–2025 | educational measurement | 4.97 | 226 | 1 |
| more in 2024–2025 | clinical competence | 4.85 | 268 | 21 |
| more in 2024–2025 | internet | 4.68 | 170 | 5 |
| more in 2024–2025 | patient education | 4.63 | 220 | 0 |
| more in 2024–2025 | young adult | 4.34 | 299 | 31 |
| more in 2024–2025 | generative ai | 4.26 | 189 | 0 |
| more in 2024–2025 | llm | 3.85 | 158 | 0 |
| more in 2024–2025 | chatbots | 3.69 | 111 | 1 |
| more in 2024–2025 | qualitative research | 3.68 | 179 | 16 |
| more in 2024–2025 | health literacy | 3.66 | 112 | 1 |
| more in 2024–2025 | practice guidelines as topic | 3.49 | 116 | 7 |
| more in 2021–2022 | machine learning | -17.75 | 1757 | 864 |
| more in 2021–2022 | deep learning | -16.51 | 1385 | 702 |
| more in 2021–2022 | covid-19 | -15.04 | 94 | 160 |
| more in 2021–2022 | algorithms | -14.01 | 658 | 385 |
| more in 2021–2022 | neural networks, computer | -12.58 | 226 | 188 |
| more in 2021–2022 | delivery of health care | -12.46 | 414 | 264 |
| more in 2021–2022 | sars-cov-2 | -8.82 | 56 | 67 |
| more in 2021–2022 | radiography | -8.76 | 89 | 82 |
| more in 2021–2022 | retrospective studies | -8.49 | 559 | 253 |
| more in 2021–2022 | forecasting | -8.44 | 61 | 66 |
| more in 2021–2022 | pandemics | -8.30 | 45 | 57 |
| more in 2021–2022 | health facilities | -8.12 | 32 | 49 |
| more in 2021–2022 | radiologists | -8.04 | 104 | 82 |
| more in 2021–2022 | big data | -7.76 | 54 | 57 |
| more in 2021–2022 | convolutional neural network | -7.62 | 48 | 53 |
| more in 2021–2022 | computers | -6.66 | 13 | 29 |
| more in 2021–2022 | endoscopy | -6.57 | 37 | 40 |
| more in 2021–2022 | image processing, computer-assisted | -6.54 | 185 | 100 |
| more in 2021–2022 | humans | -6.46 | 7195 | 1985 |
| more in 2021–2022 | lung | -6.17 | 30 | 34 |
| more in 2021–2022 | diabetic retinopathy | -6.13 | 68 | 51 |
| more in 2021–2022 | diagnosis, computer-assisted | -6.09 | 71 | 52 |
| more in 2021–2022 | technology | -5.99 | 85 | 57 |
| more in 2021–2022 | prognosis | -5.83 | 146 | 79 |
| more in 2021–2022 | diagnostic imaging | -5.71 | 138 | 75 |
| more in 2021–2022 | tomography, x-ray computed | -5.63 | 250 | 113 |
| more in 2021–2022 | colonic polyps | -5.60 | 33 | 32 |
| more in 2021–2022 | diabetes mellitus | -5.53 | 34 | 32 |
| more in 2021–2022 | neural network | -5.47 | 20 | 25 |
| more in 2021–2022 | morals | -5.46 | 16 | 23 |

## Analysis 3 · Terms separating stance (critical vs favourable, 2021–2025)

critical / favourable records: 4,283 / 9,054; qualifying terms (≥20 records): 665. Weighted log-odds with informative Dirichlet prior (background = 16,759 retained records, α0 = 1,000); z = δ/σ.

| direction | term | z | df_group1 | df_group2 |
|---|---|---|---|---|
| more in critical | delivery of health care | 16.15 | 477 | 327 |
| more in critical | ethics | 14.06 | 211 | 54 |
| more in critical | bias | 12.81 | 174 | 26 |
| more in critical | qualitative research | 9.25 | 134 | 78 |
| more in critical | health facilities | 8.66 | 85 | 28 |
| more in critical | trust | 8.41 | 104 | 56 |
| more in critical | mental health | 8.10 | 107 | 65 |
| more in critical | informed consent | 7.99 | 67 | 14 |
| more in critical | chatgpt | 7.61 | 599 | 877 |
| more in critical | privacy | 7.43 | 70 | 30 |
| more in critical | health equity | 6.93 | 60 | 25 |
| more in critical | health personnel | 6.57 | 101 | 83 |
| more in critical | decision making | 6.57 | 80 | 55 |
| more in critical | mental disorders | 6.53 | 67 | 39 |
| more in critical | confidentiality | 6.41 | 44 | 6 |
| more in critical | healthcare | 6.03 | 122 | 123 |
| more in critical | chatbot | 6.02 | 126 | 129 |
| more in critical | united states | 5.91 | 133 | 142 |
| more in critical | checklist | 5.86 | 36 | 7 |
| more in critical | bioethics | 5.86 | 36 | 7 |
| more in critical | regulation | 5.65 | 34 | 5 |
| more in critical | healthcare disparities | 5.62 | 34 | 9 |
| more in critical | morals | 5.56 | 37 | 3 |
| more in critical | medical ethics | 5.56 | 34 | 10 |
| more in critical | chatbots | 5.53 | 71 | 58 |
| more in critical | computer security | 5.52 | 33 | 9 |
| more in critical | health care | 5.45 | 68 | 55 |
| more in critical | implementation | 5.37 | 36 | 15 |
| more in critical | patient safety | 5.30 | 53 | 37 |
| more in critical | ai | 5.26 | 253 | 359 |
| more in favourable | deep learning | -16.95 | 358 | 2054 |
| more in favourable | retrospective studies | -7.88 | 177 | 751 |
| more in favourable | sensitivity and specificity | -7.59 | 80 | 443 |
| more in favourable | precision medicine | -6.66 | 55 | 320 |
| more in favourable | tomography, x-ray computed | -6.32 | 66 | 340 |
| more in favourable | predictive value of tests | -5.53 | 20 | 163 |
| more in favourable | neural networks, computer | -5.26 | 90 | 367 |
| more in favourable | convolutional neural network | -5.25 | 8 | 118 |
| more in favourable | aged | -5.09 | 238 | 762 |
| more in favourable | radiomics | -5.09 | 12 | 123 |
| more in favourable | machine learning | -5.07 | 812 | 2182 |
| more in favourable | forecasting | -4.91 | 15 | 126 |
| more in favourable | radiographic image interpretation, computer-assisted | -4.82 | 31 | 175 |
| more in favourable | drug discovery | -4.67 | 3 | 94 |
| more in favourable | biomarkers | -4.43 | 5 | 83 |
| more in favourable | prospective studies | -4.42 | 71 | 281 |
| more in favourable | endoscopy | -4.27 | 9 | 88 |
| more in favourable | magnetic resonance imaging | -4.26 | 74 | 284 |
| more in favourable | prostatic neoplasms | -4.23 | 23 | 132 |
| more in favourable | convolutional neural networks | -4.16 | 12 | 95 |
| more in favourable | meta-analysis | -4.00 | 10 | 84 |
| more in favourable | prognosis | -3.99 | 52 | 212 |
| more in favourable | screening | -3.89 | 9 | 78 |
| more in favourable | computed tomography angiography | -3.82 | 13 | 89 |
| more in favourable | coronary angiography | -3.81 | 4 | 62 |
| more in favourable | feasibility studies | -3.81 | 8 | 73 |
| more in favourable | mass screening | -3.75 | 17 | 100 |
| more in favourable | electrocardiography | -3.67 | 11 | 79 |
| more in favourable | coronary artery disease | -3.62 | 12 | 81 |
| more in favourable | diabetic retinopathy | -3.59 | 22 | 112 |

Figure: `revision_r1/figures/B6_terms_r1_draft.png|pdf` (dot plot; z printed beside each dot). Left: positive z = more frequent in 2024–2025. Right: positive z = more frequent in critical records.

