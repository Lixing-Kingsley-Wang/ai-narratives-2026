# Chi-square test — opinion (Editorial+Commentary+Letter) vs Research Article

v1 (canonical):

Contingency table (counts):

| | Opinion (Ed+Com+Let) | Research Article |
|---|---|---|
| Alarm | 58 | 799 |
| Caution | 355 | 2596 |
| Neutral | 149 | 578 |
| Cautious Optimism | 370 | 6261 |
| Advocacy | 56 | 81 |

- chi² = 430.53, dof = 4, p = 7.017e-92
- n_opinion = 988  vs  n_research = 10,315
- Critical (Alarm+Caution): opinion **41.8%** vs research **32.9%** (Δ +8.9 pp)

## v2 (robustness)

| | Opinion (Ed+Com+Let) | Research Article |
|---|---|---|
| Alarm | 35 | 519 |
| Caution | 322 | 2334 |
| Neutral | 266 | 2016 |
| Cautious Optimism | 312 | 5393 |
| Advocacy | 52 | 57 |

- chi² = 350.93, dof = 4, p = 1.104e-74
- Critical (Alarm+Caution): opinion **36.2%** vs research **27.6%** (Δ +8.5 pp)
