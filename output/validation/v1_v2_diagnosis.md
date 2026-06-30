# v1 vs v2 — diagnostic against human labels

_n = 300 validation records_

## Why is v2 κ ≈ v1 κ despite 19.9% of corpus relabelled?

Categorization:

| category | n | % |
|---|---:|---:|
| both_correct | 174 | 58.0% |
| v2_fixed_v1 | 33 | 11.0% |
| v2_broke_v1 | 26 | 8.7% |
| both_wrong_same | 56 | 18.7% |
| both_wrong_diff | 11 | 3.7% |
| v2_failed | 0 | 0.0% |

**Net v2_fixed − v2_broke = +7**

Read:
- v2_fixed_v1 = v2 corrected an error v1 made
- v2_broke_v1 = v2 introduced an error on a record v1 had correct
- A near-zero net difference means v2's gains and losses cancel out → κ unchanged.

## v2_broke_v1 — records v1 had right, v2 got wrong

n = 26

Flows (human stance → v2 stance):

| human | v2 | n |
|---|---|---:|
| Alarm | Caution | 7 |
| Advocacy | Cautious Optimism | 6 |
| Caution | Cautious Optimism | 4 |
| Cautious Optimism | Neutral | 3 |
| Caution | Neutral | 2 |
| Cautious Optimism | Caution | 2 |
| Neutral | Advocacy | 1 |
| Neutral | Cautious Optimism | 1 |

## v2_fixed_v1 — records v1 got wrong, v2 corrected

n = 33

Flows (v1 stance → human stance):

| v1 | human | n |
|---|---|---:|
| Cautious Optimism | Neutral | 9 |
| Advocacy | Cautious Optimism | 8 |
| Alarm | Caution | 6 |
| Caution | Cautious Optimism | 5 |
| Caution | Neutral | 4 |
| Advocacy | Neutral | 1 |

## Direction of v2's relabelling (independent of human)

All v2 changes among the 300 validation records (n=70):

| v1 | v2 | n |
|---|---|---:|
| Advocacy | Cautious Optimism | 17 |
| Cautious Optimism | Neutral | 15 |
| Alarm | Caution | 14 |
| Caution | Neutral | 10 |
| Caution | Cautious Optimism | 9 |
| Cautious Optimism | Caution | 2 |
| Advocacy | Neutral | 1 |
| Neutral | Advocacy | 1 |
| Neutral | Cautious Optimism | 1 |
