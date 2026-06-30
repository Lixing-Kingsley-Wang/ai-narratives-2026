# Q7 validation — inter-rater agreement (human vs classifier)

Coded rows: **108/108**. Primary statistic: unweighted Cohen's κ (nominal). Also reported: Scott's π / Fleiss (pooled-marginal chance), **Gwet's AC1** (robust to the prevalence paradox), PABAK (uniform chance), and **κ_max** (best κ achievable given the two marginals — a bias/marginal mismatch caps it below 1). Weighted κ is intentionally NOT used: these categories are nominal, not ordinal. Strength labels per Landis & Koch (1977).


## failure_mode

- n = 108
- **Cohen's κ = +0.574** (moderate); raw agreement = 69.4% (chance p_e = 0.282)
- Scott's π / Fleiss = +0.570 · **Gwet's AC1 = +0.600** · PABAK = +0.593
- κ_max = 0.755 (κ/κ_max = 0.76) — marginal mismatch caps the achievable κ

Confusion matrix (rows = human, cols = model):

| | M:confabulation | M:misclassification | M:both | M:none_or_unclear |
|---|---|---|---|---|
| **H:confabulation** | 7 | 1 | 2 | 0 |
| **H:misclassification** | 5 | 26 | 9 | 2 |
| **H:both** | 2 | 0 | 11 | 0 |
| **H:none_or_unclear** | 6 | 6 | 0 | 31 |

Per-category one-vs-rest κ:

| category | κ | agreement |
|---|--:|--:|
| confabulation | +0.392 | 85.2% |
| misclassification | +0.534 | 78.7% |
| both | +0.562 | 88.0% |
| none_or_unclear | +0.718 | 87.0% |


## model_type

- n = 108
- **Cohen's κ = +0.843** (almost perfect); raw agreement = 90.7% (chance p_e = 0.409)
- Scott's π / Fleiss = +0.843 · **Gwet's AC1 = +0.885** · PABAK = +0.877
- κ_max = 0.984 (κ/κ_max = 0.86) — marginal mismatch caps the achievable κ

Confusion matrix (rows = human, cols = model):

| | M:generative | M:discriminative | M:both | M:unclear |
|---|---|---|---|---|
| **H:generative** | 60 | 1 | 1 | 0 |
| **H:discriminative** | 0 | 23 | 0 | 4 |
| **H:both** | 0 | 1 | 3 | 0 |
| **H:unclear** | 1 | 2 | 0 | 12 |

Per-category one-vs-rest κ:

| category | κ | agreement |
|---|--:|--:|
| generative | +0.943 | 97.2% |
| discriminative | +0.802 | 92.6% |
| both | +0.740 | 98.1% |
| unclear | +0.736 | 93.5% |
