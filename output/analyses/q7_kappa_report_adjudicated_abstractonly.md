# Q7 validation — inter-rater agreement (human vs classifier)

Coded rows: **108/108**. Primary statistic: unweighted Cohen's κ (nominal). Also reported: Scott's π / Fleiss (pooled-marginal chance), **Gwet's AC1** (robust to the prevalence paradox), PABAK (uniform chance), and **κ_max** (best κ achievable given the two marginals — a bias/marginal mismatch caps it below 1). Weighted κ is intentionally NOT used: these categories are nominal, not ordinal. Strength labels per Landis & Koch (1977).


## failure_mode

- n = 108
- **Cohen's κ = +0.796** (substantial); raw agreement = 85.2% (chance p_e = 0.274)
- Scott's π / Fleiss = +0.795 · **Gwet's AC1 = +0.805** · PABAK = +0.802
- κ_max = 0.860 (κ/κ_max = 0.93) — marginal mismatch caps the achievable κ

Confusion matrix (rows = human, cols = model):

| | M:confabulation | M:misclassification | M:both | M:none_or_unclear |
|---|---|---|---|---|
| **H:confabulation** | 13 | 0 | 0 | 0 |
| **H:misclassification** | 3 | 28 | 3 | 0 |
| **H:both** | 0 | 0 | 18 | 0 |
| **H:none_or_unclear** | 4 | 5 | 1 | 33 |

Per-category one-vs-rest κ:

| category | κ | agreement |
|---|--:|--:|
| confabulation | +0.752 | 93.5% |
| misclassification | +0.762 | 89.8% |
| both | +0.878 | 96.3% |
| none_or_unclear | +0.799 | 90.7% |


## model_type

- n = 108
- **Cohen's κ = +0.953** (almost perfect); raw agreement = 97.2% (chance p_e = 0.410)
- Scott's π / Fleiss = +0.953 · **Gwet's AC1 = +0.965** · PABAK = +0.963
- κ_max = 0.984 (κ/κ_max = 0.97) — marginal mismatch caps the achievable κ

Confusion matrix (rows = human, cols = model):

| | M:generative | M:discriminative | M:both | M:unclear |
|---|---|---|---|---|
| **H:generative** | 61 | 0 | 1 | 0 |
| **H:discriminative** | 0 | 26 | 0 | 1 |
| **H:both** | 0 | 0 | 3 | 0 |
| **H:unclear** | 0 | 1 | 0 | 15 |

Per-category one-vs-rest κ:

| category | κ | agreement |
|---|--:|--:|
| generative | +0.981 | 99.1% |
| discriminative | +0.951 | 98.1% |
| both | +0.852 | 99.1% |
| unclear | +0.927 | 98.1% |
