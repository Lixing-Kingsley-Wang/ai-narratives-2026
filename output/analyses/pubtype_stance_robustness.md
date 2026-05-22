# Robustness report — pubtype_stance

- v1 records: 16,747
- v2 records: 16,753
- Bootstrap n = 1000, seed = 42, 95% CI
- Tolerance for 'robust' verdict: 3.0 pp

## Verdict summary
- Cells: 25, robust: 12, sensitive: 13
- Max |v1-v2| diff: **21.15 pp**, mean: 5.44 pp

## v1 vs v2 (point estimates with 95% CI)

| row | col | v1 | v2 | Δ (pp) | verdict |
|---|---|---|---|---:|---|
| Research Article | Alarm | 7.7 (7.2–8.3) | 5.0 (4.6–5.4) | -2.72 | robust |
| Research Article | Caution | 25.2 (24.3–26.1) | 22.6 (21.8–23.5) | -2.55 | robust |
| Research Article | Neutral | 5.6 (5.2–6.0) | 19.5 (18.7–20.3) | +13.93 | sensitive |
| Research Article | Cautious Optimism | 60.7 (59.8–61.6) | 52.3 (51.2–53.2) | -8.44 | sensitive |
| Research Article | Advocacy | 0.8 (0.6–0.9) | 0.6 (0.4–0.7) | -0.23 | robust |
| Editorial | Alarm | 3.2 (1.7–5.0) | 1.7 (0.5–3.1) | -1.49 | robust |
| Editorial | Caution | 35.1 (30.3–39.5) | 31.4 (27.0–35.8) | -3.71 | sensitive |
| Editorial | Neutral | 9.4 (6.6–12.2) | 23.5 (19.4–27.7) | +14.11 | sensitive |
| Editorial | Cautious Optimism | 46.0 (41.6–50.8) | 36.9 (32.5–41.6) | -9.16 | sensitive |
| Editorial | Advocacy | 6.2 (3.8–8.7) | 6.4 (4.2–8.8) | +0.25 | robust |
| Review | Alarm | 1.1 (0.8–1.4) | 0.6 (0.4–0.9) | -0.46 | robust |
| Review | Caution | 23.8 (22.7–24.9) | 18.6 (17.5–19.6) | -5.21 | sensitive |
| Review | Neutral | 2.0 (1.6–2.4) | 11.6 (10.8–12.4) | +9.58 | sensitive |
| Review | Cautious Optimism | 71.3 (70.1–72.5) | 67.8 (66.5–68.9) | -3.55 | sensitive |
| Review | Advocacy | 1.8 (1.5–2.2) | 1.4 (1.1–1.7) | -0.37 | robust |
| Commentary | Alarm | 8.7 (3.8–14.0) | 3.8 (0.9–7.6) | -4.81 | sensitive |
| Commentary | Caution | 45.2 (36.0–54.8) | 39.4 (30.6–48.6) | -5.77 | sensitive |
| Commentary | Neutral | 6.7 (2.3–11.7) | 27.9 (20.0–36.4) | +21.15 | sensitive |
| Commentary | Cautious Optimism | 37.5 (28.4–47.2) | 26.0 (18.1–33.7) | -11.54 | sensitive |
| Commentary | Advocacy | 1.9 (0.0–4.9) | 2.9 (0.0–6.7) | +0.96 | robust |
| Letter | Alarm | 7.5 (5.3–10.1) | 5.0 (3.1–7.0) | -2.49 | robust |
| Letter | Caution | 34.6 (30.2–39.2) | 32.2 (28.3–36.2) | -2.43 | robust |
| Letter | Neutral | 21.7 (17.8–25.5) | 29.6 (25.5–33.9) | +7.98 | sensitive |
| Letter | Cautious Optimism | 30.2 (26.0–34.5) | 28.4 (24.5–32.4) | -1.82 | robust |
| Letter | Advocacy | 6.0 (3.9–8.3) | 4.8 (2.8–6.8) | -1.24 | robust |
