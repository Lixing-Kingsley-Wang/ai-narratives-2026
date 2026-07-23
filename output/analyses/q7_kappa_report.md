# Q7 validation — inter-rater agreement (human vs classifier)

Coded rows: **120/120**. Primary statistic: unweighted Cohen's κ (nominal). Also reported: Scott's π / Fleiss (pooled-marginal chance), **Gwet's AC1** (robust to the prevalence paradox), PABAK (uniform chance), and **κ_max** (best κ achievable given the two marginals — a bias/marginal mismatch caps it below 1). Weighted κ is intentionally NOT used: these categories are nominal, not ordinal. Strength labels per Landis & Koch (1977).


## failure_mode

- n = 120
- **Cohen's κ = +0.541** (moderate); raw agreement = 67.5% (chance p_e = 0.292)
- Scott's π / Fleiss = +0.535 · **Gwet's AC1 = +0.576** · PABAK = +0.567
- κ_max = 0.753 (κ/κ_max = 0.72) — marginal mismatch caps the achievable κ

Confusion matrix (rows = human, cols = model):

| | M:confabulation | M:misclassification | M:both | M:none_or_unclear |
|---|---|---|---|---|
| **H:confabulation** | 7 | 1 | 2 | 0 |
| **H:misclassification** | 5 | 26 | 9 | 2 |
| **H:both** | 2 | 0 | 11 | 0 |
| **H:none_or_unclear** | 8 | 10 | 0 | 37 |

Per-category one-vs-rest κ:

| category | κ | agreement |
|---|--:|--:|
| confabulation | +0.365 | 85.0% |
| misclassification | +0.492 | 77.5% |
| both | +0.570 | 89.2% |
| none_or_unclear | +0.657 | 83.3% |


## model_type

- n = 120
- **Cohen's κ = +0.798** (substantial); raw agreement = 87.5% (chance p_e = 0.382)
- Scott's π / Fleiss = +0.798 · **Gwet's AC1 = +0.843** · PABAK = +0.833
- κ_max = 0.946 (κ/κ_max = 0.84) — marginal mismatch caps the achievable κ

Confusion matrix (rows = human, cols = model):

| | M:generative | M:discriminative | M:both | M:unclear |
|---|---|---|---|---|
| **H:generative** | 62 | 1 | 1 | 0 |
| **H:discriminative** | 0 | 24 | 0 | 4 |
| **H:both** | 0 | 1 | 3 | 0 |
| **H:unclear** | 3 | 4 | 1 | 16 |

Per-category one-vs-rest κ:

| category | κ | agreement |
|---|--:|--:|
| generative | +0.916 | 95.8% |
| discriminative | +0.773 | 91.7% |
| both | +0.654 | 97.5% |
| unclear | +0.667 | 90.0% |
