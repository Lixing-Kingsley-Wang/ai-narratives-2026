# Q7 validation — inter-rater agreement (human vs classifier)

Coded rows: **120/120**. Cohen's κ (unweighted, nominal). Strength labels per Landis & Koch (1977).


## failure_mode

- n = 120
- **Cohen's κ = +0.541** (moderate)
- raw agreement = 67.5%

Confusion matrix (rows = human, cols = model):

| | M:confabulation | M:misclassification | M:both | M:none_or_unclear |
|---|---|---|---|---|
| **H:confabulation** | 7 | 1 | 2 | 0 |
| **H:misclassification** | 5 | 26 | 9 | 2 |
| **H:both** | 2 | 0 | 11 | 0 |
| **H:none_or_unclear** | 8 | 10 | 0 | 37 |


## model_type

- n = 120
- **Cohen's κ = +0.798** (substantial)
- raw agreement = 87.5%

Confusion matrix (rows = human, cols = model):

| | M:generative | M:discriminative | M:both | M:unclear |
|---|---|---|---|---|
| **H:generative** | 62 | 1 | 1 | 0 |
| **H:discriminative** | 0 | 24 | 0 | 4 |
| **H:both** | 0 | 1 | 3 | 0 |
| **H:unclear** | 3 | 4 | 1 | 16 |
