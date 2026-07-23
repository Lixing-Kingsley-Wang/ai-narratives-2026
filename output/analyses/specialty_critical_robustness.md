# Robustness report — specialty_critical

- v1 records: 16,747
- v2 records: 16,753
- Bootstrap n = 1000, seed = 42, 95% CI
- Tolerance for 'robust' verdict: 3.0 pp

## Verdict summary
- Cells: 18, robust: 11, sensitive: 7
- Max |v1-v2| diff: **19.93 pp**, mean: 4.61 pp

## v1 vs v2 (point estimates with 95% CI)

| group | v1 | v2 | Δ (pp) | verdict |
|---|---|---|---:|---|
| Radiology / Diagnostic Imaging | 21.3 (19.6–22.9) | 19.2 (17.6–20.9) | -2.04 | robust |
| Pathology / Laboratory Medicine | 20.7 (17.1–24.4) | 17.9 (14.5–21.6) | -2.80 | robust |
| Cardiology | 16.8 (14.1–19.8) | 16.1 (13.3–19.1) | -0.66 | robust |
| Oncology | 19.7 (17.8–21.8) | 16.7 (14.9–18.6) | -2.95 | robust |
| Surgery | 28.9 (26.7–31.4) | 28.8 (26.6–31.3) | -0.14 | robust |
| Ophthalmology | 18.4 (15.7–21.2) | 18.1 (15.4–20.8) | -0.26 | robust |
| Dermatology | 36.5 (31.3–42.9) | 32.0 (26.9–37.1) | -4.54 | sensitive |
| Neurology / Neuroscience | 24.4 (20.3–28.8) | 22.4 (18.2–26.7) | -2.03 | robust |
| Mental Health / Psychiatry | 51.3 (46.8–55.5) | 42.5 (37.7–47.2) | -8.87 | sensitive |
| Internal Medicine / Primary Care | 22.5 (20.0–25.0) | 20.9 (18.5–23.1) | -1.52 | robust |
| Emergency Medicine / Critical Care | 28.5 (23.9–33.1) | 26.6 (22.2–31.2) | -1.90 | robust |
| Pediatrics | 25.5 (21.4–30.0) | 24.7 (20.5–28.9) | -0.77 | robust |
| Obstetrics / Gynecology | 26.7 (20.7–32.4) | 23.3 (18.1–28.9) | -3.39 | sensitive |
| Dentistry | 24.8 (21.9–28.1) | 25.4 (22.6–28.6) | +0.59 | robust |
| Medical Informatics / Digital Health | 44.9 (43.5–46.4) | 33.5 (32.1–34.9) | -11.43 | sensitive |
| Nursing | 43.0 (37.0–48.8) | 23.0 (18.5–28.1) | -19.93 | sensitive |
| Medical Education | 35.1 (32.4–38.0) | 22.0 (19.8–24.5) | -13.10 | sensitive |
| Multidisciplinary / Other | 32.8 (27.0–38.6) | 26.7 (20.9–32.4) | -6.03 | sensitive |
