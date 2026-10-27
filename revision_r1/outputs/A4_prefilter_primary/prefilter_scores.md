# Prefilter audit scores — PRIMARY (amendment 2: unlabelled rows counted as errors)

Rows: 370; unlabelled: 1 (by stratum: {'EX-F': 1}); borderline=Y: 9.

### 3-class: human (rows) × production label (columns), coded sample, unweighted

|  | discourse | evaluative | application |
|---|---|---|---|
| discourse | 24 | 1 | 25 |
| evaluative | 0 | 23 | 38 |
| application | 1 | 1 | 236 |
| unlabelled | 0 | 0 | 1 |

### 3-class: human (rows) × full-abstract label (columns), coded sample, unweighted

|  | discourse | evaluative | application |
|---|---|---|---|
| discourse | 46 | 0 | 4 |
| evaluative | 0 | 53 | 8 |
| application | 6 | 10 | 222 |
| unlabelled | 1 | 0 | 0 |

## Variant: primary

| year | 1−NPV, % (excluded) | missed AI-engaged records | PPV retained, % | full-abstract precision (EX-F), % |
|---|---|---|---|---|
| 2021 | 2.0 (1.3–2.5) | 202 (128–257) | 100.0 (100.0–100.0) | 73.3 (46.7–93.3) |
| 2022 | 4.4 (1.9–9.1) | 518 (220–1071) | 90.0 (70.0–100.0) | 80.0 (60.0–100.0) |
| 2023 | 6.7 (2.0–13.6) | 812 (241–1642) | 90.0 (70.0–100.0) | 66.7 (40.0–93.3) |
| 2024 | 2.6 (1.6–3.3) | 404 (257–514) | 100.0 (100.0–100.0) | 73.3 (46.7–93.3) |
| 2025 | 7.9 (3.4–14.1) | 1812 (773–3222) | 100.0 (100.0–100.0) | 93.3 (80.0–100.0) |
| pooled | 5.2 (3.2–7.4) | 3747 (2332–5398) | 97.6 (93.7–100.0) | 80.4 (71.7–89.0) |

1−NPV 2021–2022: 3.3 (1.8–5.9)%; 2024–2025: 5.7 (3.0–9.4)%; difference (2024–25 minus 2021–22): 2.5 (-1.6 to 6.4) pp.
Logistic, year on human KEEP within excluded strata: unweighted OR/yr 1.263 (Wald 0.898–1.776, P=0.180; stratum adjusted); weighted OR/yr 1.267 (bootstrap 0.940–1.760).

| population-weighted 2×2 | production prefilter | full-abstract re-run |
|---|---|---|
| sensitivity | 78.5 (71.7–85.6) | 82.0 (72.1–91.9) |
| specificity | 99.5 (98.7–100.0) | 99.3 (99.0–99.6) |
| PPV | 97.6 (93.7–100.0) | 96.8 (95.2–98.2) |
| NPV | 94.8 (92.6–96.8) | 95.6 (92.9–98.1) |
| kappa | 0.842 (0.782–0.897) | 0.862 (0.785–0.931) |
| AC1 | 0.933 (0.903–0.958) | 0.940 (0.905–0.970) |

## Variant: borderline→application

| year | 1−NPV, % (excluded) | missed AI-engaged records | PPV retained, % | full-abstract precision (EX-F), % |
|---|---|---|---|---|
| 2021 | 1.8 (1.1–2.4) | 183 (110–238) | 100.0 (100.0–100.0) | 66.7 (40.0–86.7) |
| 2022 | 4.2 (1.5–8.9) | 496 (176–1049) | 90.0 (70.0–100.0) | 73.3 (53.3–93.3) |
| 2023 | 6.7 (2.0–13.6) | 812 (241–1642) | 90.0 (70.0–100.0) | 66.7 (40.0–93.3) |
| 2024 | 2.6 (1.6–3.3) | 404 (257–514) | 100.0 (100.0–100.0) | 73.3 (46.7–93.3) |
| 2025 | 5.8 (3.1–10.3) | 1322 (714–2361) | 100.0 (100.0–100.0) | 93.3 (80.0–100.0) |
| pooled | 4.4 (2.9–6.3) | 3217 (2085–4578) | 97.6 (93.7–100.0) | 78.8 (70.1–87.2) |

1−NPV 2021–2022: 3.1 (1.6–5.8)%; 2024–2025: 4.5 (2.9–7.2)%; difference (2024–25 minus 2021–22): 1.4 (-2.4 to 4.9) pp.
Logistic, year on human KEEP within excluded strata: unweighted OR/yr 1.299 (Wald 0.923–1.829, P=0.134; stratum adjusted); weighted OR/yr 1.158 (bootstrap 0.916–1.567).

| population-weighted 2×2 | production prefilter | full-abstract re-run |
|---|---|---|
| sensitivity | 81.0 (74.8–86.7) | 84.4 (74.7–93.5) |
| specificity | 99.5 (98.7–100.0) | 99.3 (99.0–99.5) |
| PPV | 97.6 (93.7–100.0) | 96.5 (95.1–97.9) |
| NPV | 95.6 (93.7–97.1) | 96.3 (93.8–98.5) |
| kappa | 0.860 (0.810–0.907) | 0.878 (0.803–0.940) |
| AC1 | 0.942 (0.917–0.963) | 0.948 (0.917–0.974) |

## Variant: borderline→KEEP

| year | 1−NPV, % (excluded) | missed AI-engaged records | PPV retained, % | full-abstract precision (EX-F), % |
|---|---|---|---|---|
| 2021 | 2.4 (1.8–2.7) | 238 (183–275) | 100.0 (100.0–100.0) | 86.7 (66.7–100.0) |
| 2022 | 4.4 (1.9–9.1) | 518 (220–1071) | 90.0 (70.0–100.0) | 80.0 (60.0–100.0) |
| 2023 | 7.2 (2.7–13.8) | 865 (321–1668) | 90.0 (70.0–100.0) | 80.0 (60.0–100.0) |
| 2024 | 2.6 (1.6–3.3) | 404 (257–514) | 100.0 (100.0–100.0) | 73.3 (46.7–93.3) |
| 2025 | 8.2 (3.9–14.6) | 1871 (892–3340) | 100.0 (100.0–100.0) | 100.0 (100.0–100.0) |
| pooled | 5.4 (3.4–7.6) | 3897 (2471–5532) | 97.6 (93.7–100.0) | 86.5 (79.6–93.2) |

1−NPV 2021–2022: 3.5 (2.0–6.1)%; 2024–2025: 5.9 (3.2–9.6)%; difference (2024–25 minus 2021–22): 2.4 (-1.4 to 6.3) pp.
Logistic, year on human KEEP within excluded strata: unweighted OR/yr 1.238 (Wald 0.850–1.804, P=0.266; stratum adjusted); weighted OR/yr 1.252 (bootstrap 0.934–1.703).

| population-weighted 2×2 | production prefilter | full-abstract re-run |
|---|---|---|
| sensitivity | 77.9 (71.1–84.8) | 82.2 (72.3–91.9) |
| specificity | 99.5 (98.7–100.0) | 99.5 (99.3–99.8) |
| PPV | 97.6 (93.7–100.0) | 97.8 (96.5–98.9) |
| NPV | 94.6 (92.4–96.6) | 95.6 (92.9–98.1) |
| kappa | 0.837 (0.778–0.889) | 0.869 (0.792–0.937) |
| AC1 | 0.930 (0.900–0.955) | 0.943 (0.908–0.973) |

## Intra-rater agreement (PILOT rows: original my_label vs new code; unlabelled = disagreement)

n = 20 (unlabelled: 0); 3-class agreement 19/20 = 95.0%; KEEP/DROP agreement 19/20 = 95.0%, κ = 0.773. 3-class κ on labelled rows only (κ is undefined for a missing category): 0.780 (n = 20).

