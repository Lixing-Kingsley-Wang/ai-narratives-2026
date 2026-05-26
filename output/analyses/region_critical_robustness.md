# Robustness report — region_critical

- v1 records: 16,747
- v2 records: 16,753
- Bootstrap n = 1000, seed = 42, 95% CI
- Tolerance for 'robust' verdict: 3.0 pp

## Verdict summary
- Cells: 9, robust: 1, sensitive: 8
- Max |v1-v2| diff: **19.12 pp**, mean: 6.78 pp

## v1 vs v2 (point estimates with 95% CI)

| group | v1 | v2 | Δ (pp) | verdict |
|---|---|---|---:|---|
| North America | 35.1 (33.9–36.4) | 29.1 (27.9–30.3) | -6.08 | sensitive |
| Western Europe | 35.1 (33.6–36.5) | 28.0 (26.7–29.3) | -7.05 | sensitive |
| East Asia | 18.5 (17.2–19.9) | 15.9 (14.7–17.2) | -2.62 | robust |
| Middle East / North Africa | 30.6 (28.4–32.8) | 26.6 (24.5–28.7) | -4.03 | sensitive |
| South/Southeast Asia | 24.6 (21.5–27.7) | 19.0 (16.5–21.7) | -5.52 | sensitive |
| Latin America / Oceania | 36.8 (33.3–40.2) | 30.8 (27.6–34.2) | -6.03 | sensitive |
| Eastern Europe | 28.9 (24.1–34.4) | 23.0 (18.4–27.6) | -5.85 | sensitive |
| Sub-Saharan Africa | 45.6 (32.7–56.5) | 26.5 (15.8–36.8) | -19.12 | sensitive |
| Unknown | 32.2 (28.4–36.1) | 27.5 (23.9–31.1) | -4.72 | sensitive |
