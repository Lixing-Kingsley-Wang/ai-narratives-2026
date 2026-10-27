# Prefilter audit scores (REAL LABELS — secondary: originally pre-specified, blank excluded)

Coded rows usable: 369; unusable (blank/invalid label): 1; borderline=Y: 8.

### 3-class: human (rows) × production label (columns), coded sample, unweighted

|  | discourse | evaluative | application |
|---|---|---|---|
| discourse | 24 | 1 | 25 |
| evaluative | 0 | 23 | 38 |
| application | 1 | 1 | 236 |

### 3-class: human (rows) × full-abstract label (columns), coded sample, unweighted

|  | discourse | evaluative | application |
|---|---|---|---|
| discourse | 46 | 0 | 4 |
| evaluative | 0 | 53 | 8 |
| application | 6 | 10 | 222 |

## Variant: primary

| year | 1−NPV, % (excluded) | missed AI-engaged records | PPV retained, % | full-abstract precision (EX-F), % |
|---|---|---|---|---|
| 2021 | 2.0 (1.5–2.5) | 202 (147–257) | 100.0 (100.0–100.0) | 73.3 (53.3–93.3) |
| 2022 | 4.4 (1.9–9.1) | 518 (220–1071) | 90.0 (70.0–100.0) | 80.0 (60.0–100.0) |
| 2023 | 6.7 (1.9–13.4) | 804 (229–1609) | 90.0 (70.0–100.0) | 71.4 (42.9–92.9) |
| 2024 | 2.6 (1.9–3.3) | 404 (293–514) | 100.0 (100.0–100.0) | 73.3 (53.2–93.3) |
| 2025 | 7.9 (3.4–14.3) | 1812 (773–3281) | 100.0 (100.0–100.0) | 93.3 (80.0–100.0) |
| pooled | 5.2 (3.2–7.4) | 3740 (2336–5369) | 97.6 (93.7–100.0) | 81.2 (71.9–89.5) |

1−NPV 2021–2022: 3.3 (1.8–6.0)%; 2024–2025: 5.7 (3.0–9.5)%; difference (2024–25 minus 2021–22): 2.5 (-1.4 to 6.6) pp.
Logistic, year on human KEEP within excluded strata: unweighted OR/yr 1.261 (Wald 0.897–1.771, P=0.182; stratum adjusted); weighted OR/yr 1.268 (bootstrap 0.957–1.773).

| population-weighted 2×2 | production prefilter | full-abstract re-run |
|---|---|---|
| sensitivity | 78.6 (71.8–85.4) | 82.0 (72.1–92.2) |
| specificity | 99.5 (98.7–100.0) | 99.3 (99.0–99.6) |
| PPV | 97.6 (93.7–100.0) | 96.9 (95.4–98.2) |
| NPV | 94.8 (92.6–96.8) | 95.6 (92.7–98.2) |
| kappa | 0.842 (0.785–0.896) | 0.863 (0.785–0.935) |
| AC1 | 0.933 (0.904–0.958) | 0.940 (0.904–0.971) |

## Variant: borderline→application

| year | 1−NPV, % (excluded) | missed AI-engaged records | PPV retained, % | full-abstract precision (EX-F), % |
|---|---|---|---|---|
| 2021 | 1.8 (1.1–2.4) | 183 (110–238) | 100.0 (100.0–100.0) | 66.7 (40.0–86.7) |
| 2022 | 4.2 (1.7–8.9) | 496 (198–1048) | 90.0 (70.0–100.0) | 73.3 (53.2–93.3) |
| 2023 | 6.7 (1.9–13.4) | 804 (229–1609) | 90.0 (70.0–100.0) | 71.4 (42.9–92.9) |
| 2024 | 2.6 (1.9–3.3) | 404 (293–514) | 100.0 (100.0–100.0) | 73.3 (53.2–93.3) |
| 2025 | 5.8 (3.1–10.3) | 1322 (714–2361) | 100.0 (100.0–100.0) | 93.3 (80.0–100.0) |
| pooled | 4.4 (2.9–6.4) | 3210 (2137–4628) | 97.6 (93.7–100.0) | 79.6 (70.7–87.9) |

1−NPV 2021–2022: 3.1 (1.6–5.8)%; 2024–2025: 4.5 (2.9–7.3)%; difference (2024–25 minus 2021–22): 1.4 (-2.0 to 5.0) pp.
Logistic, year on human KEEP within excluded strata: unweighted OR/yr 1.296 (Wald 0.922–1.823, P=0.135; stratum adjusted); weighted OR/yr 1.159 (bootstrap 0.922–1.559).

| population-weighted 2×2 | production prefilter | full-abstract re-run |
|---|---|---|
| sensitivity | 81.0 (74.7–86.5) | 84.4 (74.1–93.5) |
| specificity | 99.5 (98.8–100.0) | 99.3 (99.0–99.6) |
| PPV | 97.6 (93.7–100.0) | 96.6 (95.1–98.0) |
| NPV | 95.6 (93.6–97.1) | 96.3 (93.8–98.5) |
| kappa | 0.861 (0.808–0.904) | 0.879 (0.802–0.940) |
| AC1 | 0.942 (0.916–0.961) | 0.948 (0.918–0.975) |

## Variant: borderline→KEEP

| year | 1−NPV, % (excluded) | missed AI-engaged records | PPV retained, % | full-abstract precision (EX-F), % |
|---|---|---|---|---|
| 2021 | 2.4 (1.8–2.7) | 238 (183–275) | 100.0 (100.0–100.0) | 86.7 (66.7–100.0) |
| 2022 | 4.4 (1.9–9.1) | 518 (220–1071) | 90.0 (70.0–100.0) | 80.0 (60.0–100.0) |
| 2023 | 7.1 (2.6–13.6) | 861 (315–1638) | 90.0 (70.0–100.0) | 85.7 (64.3–100.0) |
| 2024 | 2.6 (1.9–3.3) | 404 (293–514) | 100.0 (100.0–100.0) | 73.3 (53.2–93.3) |
| 2025 | 8.2 (3.9–14.6) | 1871 (892–3340) | 100.0 (100.0–100.0) | 100.0 (100.0–100.0) |
| pooled | 5.4 (3.5–7.5) | 3893 (2515–5462) | 97.6 (93.7–100.0) | 87.5 (80.2–94.2) |

1−NPV 2021–2022: 3.5 (2.0–6.1)%; 2024–2025: 5.9 (3.2–9.7)%; difference (2024–25 minus 2021–22): 2.4 (-1.3 to 6.5) pp.
Logistic, year on human KEEP within excluded strata: unweighted OR/yr 1.236 (Wald 0.850–1.799, P=0.267; stratum adjusted); weighted OR/yr 1.252 (bootstrap 0.958–1.711).

| population-weighted 2×2 | production prefilter | full-abstract re-run |
|---|---|---|
| sensitivity | 77.9 (71.3–84.6) | 82.2 (72.3–92.3) |
| specificity | 99.5 (98.7–100.0) | 99.6 (99.3–99.8) |
| PPV | 97.6 (93.7–100.0) | 97.9 (96.7–99.1) |
| NPV | 94.6 (92.5–96.5) | 95.6 (92.7–98.2) |
| kappa | 0.837 (0.780–0.890) | 0.870 (0.792–0.940) |
| AC1 | 0.930 (0.902–0.955) | 0.943 (0.906–0.974) |

## Intra-rater agreement (PILOT rows: original my_label vs new code)

n = 20; 3-class agreement 19/20 = 95.0%, κ = 0.780; KEEP/DROP agreement 19/20 = 95.0%, κ = 0.773.

