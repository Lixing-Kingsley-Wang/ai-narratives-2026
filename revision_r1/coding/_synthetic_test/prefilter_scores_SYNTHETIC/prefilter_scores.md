# Prefilter audit scores (SYNTHETIC TEST — random labels)

Coded rows usable: 360; unusable (blank/invalid label): 10; borderline=Y: 52.

### 3-class: human (rows) × production label (columns), coded sample, unweighted

|  | discourse | evaluative | application |
|---|---|---|---|
| discourse | 3 | 1 | 35 |
| evaluative | 1 | 6 | 28 |
| application | 21 | 18 | 227 |

### 3-class: human (rows) × full-abstract label (columns), coded sample, unweighted

|  | discourse | evaluative | application |
|---|---|---|---|
| discourse | 4 | 6 | 29 |
| evaluative | 2 | 11 | 22 |
| application | 47 | 46 | 173 |

## Variant: primary

| year | 1−NPV, % (excluded) | missed AI-engaged records | PPV retained, % | full-abstract precision (EX-F), % |
|---|---|---|---|---|
| 2021 | 18.5 (7.3–30.0) | 1867 (741–3030) | 40.0 (10.0–70.0) | 13.3 (0.0–33.3) |
| 2022 | 22.8 (11.5–36.2) | 2681 (1352–4255) | 30.0 (0.0–60.0) | 6.7 (0.0–20.0) |
| 2023 | 19.1 (9.4–30.6) | 2301 (1135–3682) | 20.0 (0.0–50.0) | 33.3 (13.3–60.0) |
| 2024 | 31.9 (20.2–45.6) | 4984 (3156–7125) | 10.0 (0.0–30.0) | 13.3 (0.0–33.3) |
| 2025 | 19.2 (9.2–30.6) | 4397 (2108–7020) | 10.0 (0.0–30.0) | 33.3 (13.3–53.3) |
| pooled | 22.4 (17.2–28.1) | 16230 (12476–20383) | 15.6 (6.5–26.7) | 23.0 (12.8–33.8) |

1−NPV 2021–2022: 20.8 (12.5–29.7)%; 2024–2025: 24.3 (15.8–33.0)%; difference (2024–25 minus 2021–22): 3.5 (-8.7 to 15.3) pp.
Logistic, year on human KEEP within excluded strata: unweighted OR/yr 1.119 (Wald 0.917–1.364, P=0.269; stratum adjusted); weighted OR/yr 1.030 (bootstrap 0.811–1.305).

| population-weighted 2×2 | production prefilter | full-abstract re-run |
|---|---|---|
| sensitivity | 11.9 (5.3–19.9) | 12.9 (6.5–20.9) |
| specificity | 82.6 (80.7–84.7) | 81.8 (79.3–84.4) |
| PPV | 15.6 (6.5–26.7) | 16.1 (7.7–26.9) |
| NPV | 77.6 (71.9–82.8) | 77.6 (71.8–82.8) |
| kappa | -0.060 (-0.152 to 0.050) | -0.057 (-0.150 to 0.052) |
| AC1 | 0.533 (0.439–0.615) | 0.524 (0.424–0.610) |

## Variant: borderline→application

| year | 1−NPV, % (excluded) | missed AI-engaged records | PPV retained, % | full-abstract precision (EX-F), % |
|---|---|---|---|---|
| 2021 | 18.3 (7.1–29.8) | 1849 (723–3011) | 30.0 (0.0–60.0) | 6.7 (0.0–20.0) |
| 2022 | 22.8 (11.5–36.2) | 2681 (1352–4255) | 20.0 (0.0–50.0) | 6.7 (0.0–20.0) |
| 2023 | 12.1 (3.6–21.8) | 1461 (431–2626) | 20.0 (0.0–50.0) | 26.7 (6.7–53.3) |
| 2024 | 27.4 (15.9–40.6) | 4282 (2492–6350) | 10.0 (0.0–30.0) | 13.3 (0.0–33.3) |
| 2025 | 18.9 (8.9–30.4) | 4338 (2050–6959) | 10.0 (0.0–30.0) | 26.7 (6.7–46.7) |
| pooled | 20.2 (15.1–25.7) | 14611 (10919–18607) | 13.9 (4.9–24.7) | 18.7 (9.2–29.6) |

1−NPV 2021–2022: 20.7 (12.4–29.6)%; 2024–2025: 22.4 (13.8–31.0)%; difference (2024–25 minus 2021–22): 1.6 (-10.7 to 13.4) pp.
Logistic, year on human KEEP within excluded strata: unweighted OR/yr 1.107 (Wald 0.898–1.364, P=0.341; stratum adjusted); weighted OR/yr 1.027 (bootstrap 0.798–1.323).

| population-weighted 2×2 | production prefilter | full-abstract re-run |
|---|---|---|
| sensitivity | 11.8 (4.4–20.0) | 13.8 (6.6–22.4) |
| specificity | 82.7 (80.9–84.7) | 82.2 (79.7–84.6) |
| PPV | 13.9 (4.9–24.7) | 15.4 (7.0–26.4) |
| NPV | 79.8 (74.3–84.9) | 80.1 (74.5–85.5) |
| kappa | -0.058 (-0.156 to 0.052) | -0.043 (-0.142 to 0.067) |
| AC1 | 0.565 (0.476–0.643) | 0.560 (0.460–0.643) |

## Variant: borderline→KEEP

| year | 1−NPV, % (excluded) | missed AI-engaged records | PPV retained, % | full-abstract precision (EX-F), % |
|---|---|---|---|---|
| 2021 | 34.8 (21.4–48.6) | 3524 (2169–4916) | 50.0 (20.0–80.0) | 33.3 (13.3–60.0) |
| 2022 | 25.8 (14.3–39.4) | 3035 (1684–4631) | 30.0 (0.0–60.0) | 33.3 (13.3–60.0) |
| 2023 | 34.8 (21.1–49.2) | 4197 (2545–5929) | 30.0 (0.0–60.0) | 33.3 (13.3–60.0) |
| 2024 | 41.3 (27.9–55.0) | 6460 (4356–8601) | 20.0 (0.0–50.0) | 26.7 (6.7–53.3) |
| 2025 | 31.1 (18.0–44.5) | 7138 (4121–10214) | 20.0 (0.0–50.0) | 53.3 (26.7–80.0) |
| pooled | 33.6 (27.4–40.0) | 24353 (19829–29010) | 24.7 (12.5–38.7) | 39.1 (26.8–51.2) |

1−NPV 2021–2022: 30.0 (20.8–39.9)%; 2024–2025: 35.3 (25.1–44.9)%; difference (2024–25 minus 2021–22): 5.3 (-8.2 to 19.2) pp.
Logistic, year on human KEEP within excluded strata: unweighted OR/yr 1.063 (Wald 0.895–1.263, P=0.484; stratum adjusted); weighted OR/yr 1.023 (bootstrap 0.833–1.268).

| population-weighted 2×2 | production prefilter | full-abstract re-run |
|---|---|---|
| sensitivity | 12.5 (6.6–18.9) | 14.6 (8.7–20.8) |
| specificity | 82.0 (79.1–85.0) | 81.7 (78.4–85.3) |
| PPV | 24.7 (12.5–38.7) | 27.4 (15.7–41.4) |
| NPV | 66.4 (60.0–72.6) | 66.9 (60.4–73.2) |
| kappa | -0.064 (-0.162 to 0.046) | -0.042 (-0.141 to 0.065) |
| AC1 | 0.363 (0.246–0.471) | 0.366 (0.246–0.475) |

## Intra-rater agreement (PILOT rows: original my_label vs new code)

n = 20; 3-class agreement 13/20 = 65.0%, κ = 0.014; KEEP/DROP agreement 14/20 = 70.0%, κ = 0.118.

