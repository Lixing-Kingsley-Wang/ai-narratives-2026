# C.1 — Hallucination × patient_safety co-occurrence

Subset: A+C (Alarm + Caution) records from v1, 2021–2026, n=5,161.
Themes from `output/analysis/thematic_alarm.csv` (v1-only theme classification).
Mapping: plan's `patient_safety` = `safety_clinical` flag in the themes column.

## Headline

- Records flagged **hallucination**: 2,450 (47.5%)
- Records flagged **safety_clinical**: 3,372 (65.3%)
- Records flagged **BOTH**: 2,041 (39.5%)
- **Pearson r = +0.359** (p = 8.99e-157)
- P(safety_clinical | hallucination) = **0.833**
- P(hallucination | safety_clinical) = **0.605**
- Co-occurrence lift over independence: **1.28×** (observed 2041 vs expected 1601)

## Interpretation

Moderate positive coupling. r=+0.359, lift 1.28×. Some co-occurrence above independence baseline, but the asymmetric conditional probabilities (P(safety|hallu)=0.83 vs P(hallu|safety)=0.61) suggest hallucination papers often raise safety concerns, but safety papers don't always invoke hallucination — two overlapping rather than identical clusters.

## Year-by-year prevalence within A+C

| year | n | hallucination % | safety_clinical % | both % |
|---:|---:|---:|---:|---:|
| 2021 | 270 | 23.7% | 59.3% | 21.5% |
| 2022 | 333 | 21.9% | 63.1% | 19.8% |
| 2023 | 624 | 42.1% | 61.7% | 33.0% |
| 2024 | 1,228 | 51.9% | 66.2% | 42.2% |
| 2025 | 1,828 | 51.1% | 64.9% | 42.3% |
| 2026 | 878 | 54.6% | 70.3% | 47.8% |

Note: percentages are within the A+C subset, not the full corpus. Both themes rise sharply post-ChatGPT (2022→2023); the BOTH-flag rate is the most discriminating signal — its slope indicates whether the two themes are fusing into one cluster over time.
