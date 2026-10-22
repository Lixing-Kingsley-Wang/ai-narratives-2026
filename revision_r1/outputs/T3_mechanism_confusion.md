# T3 · Failure-mode and model-type confusion matrices (X4a)

Script: `revision_r1/scripts/t3_mechanism_confusion.py`. Human codes: blind coding sheet `output/analyses/q7_validation_coding.xlsx` (sheet `Coding`), **not** the adjudicated labels. Model labels: `output/analyses/q7_classified_ac.csv`. Same join and abstract filter as `q7_kappa.py --require-abstract`: 120 validation records, 12 title-only dropped, n = 108.

## 1. Reproduction of reported statistics

| axis | statistic | recomputed | manuscript | status |
|---|---|---|---|---|
| failure_mode | Cohen κ | 0.574 | 0.570 | match |
| failure_mode | Gwet AC1 | 0.600 | 0.600 | match |
| failure_mode | raw agreement % | 69.444 | 69.400 | match |
| failure_mode | κ_max | 0.755 | 0.760 | match only via 3-dp intermediate rounding (0.75493 → 0.755 → 0.76) |
| failure_mode | κ/κ_max | 0.761 | 0.760 | match |
| model_type | Cohen κ | 0.843 | 0.840 | match |
| model_type | Gwet AC1 | 0.885 | 0.890 | match only via 3-dp intermediate rounding (0.88468 → 0.885 → 0.89) |
| model_type | raw agreement % | 90.741 | 90.700 | match |
| model_type | κ_max | 0.984 |  | n/a (not reported) |
| model_type | κ/κ_max | 0.857 | 0.860 | match |

## 2. Failure mode: 4×4 confusion matrix (n=108)

| Human code \ Model label | Confabulation (fabrication) | Misclassification (factual error) | Both | None or unclear | Row total |
|---|---|---|---|---|---|
| Confabulation (fabrication) | 7 | 1 | 2 | 0 | 10 |
| Misclassification (factual error) | 5 | 26 | 9 | 2 | 42 |
| Both | 2 | 0 | 11 | 0 | 13 |
| None or unclear | 6 | 6 | 0 | 31 | 43 |
| Column total | 20 | 33 | 22 | 33 | 108 |

PABAK = 0.593.

Per-class precision, recall, F1 (bootstrap 95% CI, 1000 resamples of the 108 records, seed 42):

| class | support (human) | n (model) | precision | recall | F1 |
|---|---|---|---|---|---|
| confabulation | 10 | 20 | 0.35 (0.14–0.56) | 0.70 (0.38–1.00) | 0.47 (0.21–0.67) |
| misclassification | 42 | 33 | 0.79 (0.64–0.93) | 0.62 (0.46–0.76) | 0.69 (0.55–0.81) |
| both | 13 | 22 | 0.50 (0.29–0.72) | 0.85 (0.61–1.00) | 0.63 (0.40–0.80) |
| none_or_unclear | 43 | 33 | 0.94 (0.85–1.00) | 0.72 (0.59–0.85) | 0.82 (0.71–0.90) |
| macro-F1 | 108 | 108 |  |  | 0.65 (0.55–0.75) |

## 2. Model type: 4×4 confusion matrix (n=108)

| Human code \ Model label | Generative | Discriminative | Both | Unclear | Row total |
|---|---|---|---|---|---|
| Generative | 60 | 1 | 1 | 0 | 62 |
| Discriminative | 0 | 23 | 0 | 4 | 27 |
| Both | 0 | 1 | 3 | 0 | 4 |
| Unclear | 1 | 2 | 0 | 12 | 15 |
| Column total | 61 | 27 | 4 | 16 | 108 |

PABAK = 0.877.

Per-class precision, recall, F1 (bootstrap 95% CI, 1000 resamples of the 108 records, seed 42):

| class | support (human) | n (model) | precision | recall | F1 |
|---|---|---|---|---|---|
| generative | 62 | 61 | 0.98 (0.94–1.00) | 0.97 (0.92–1.00) | 0.98 (0.94–1.00) |
| discriminative | 27 | 27 | 0.85 (0.71–0.97) | 0.85 (0.70–0.97) | 0.85 (0.73–0.94) |
| both | 4 | 4 | 0.75 (0.00–1.00) | 0.75 (0.00–1.00) | 0.75 (0.00–1.00) |
| unclear | 15 | 16 | 0.75 (0.50–0.94) | 0.80 (0.56–1.00) | 0.77 (0.56–0.92) |
| macro-F1 | 108 | 108 |  |  | 0.84 (0.66–0.94) |

## 3. Direction of fabrication disagreement

Fabrication-involved = confabulation or both.

|  | Model: fabrication-involved | Model: not fabrication | Row total |
|---|---|---|---|
| Human: fabrication-involved | 22 | 1 | 23 |
| Human: not fabrication | 20 | 65 | 85 |
| Column total | 42 | 66 | 108 |

- Model said fabrication-involved, human did not: **20** (human misclassification: 14, human none_or_unclear: 6).
- Human said fabrication-involved, model did not: **1** (model misclassification: 1).
- Fabrication-involved prevalence in the validation set: human 23/108 (21.3%), model 42/108 (38.9%).
- Exact McNemar (binomial) test of the discordant pairs 20 vs 1: P < .001 (exact P = 2.10e-05).
- Strict confabulation only: model yes / human no = 13; human yes / model no = 3.

Validation-set sampling (from Methods): 120 records stratified by year and assigned failure mode, so these prevalences are not corpus prevalences.

## 4. Draft supplementary table (Table S18 style)

**Table S19 (draft). Human versus model mechanism labels in the validation sample (n = 108 abstract-present records).** Rows give the blinded human code and columns the model label. (a) Failure mode. (b) Model type. (c) Per-class precision, recall, and F1 with 95% percentile bootstrap CIs (1000 resamples, seed 42). Confabulation is reported in the main text as fabrication and misclassification as factual error.

a)

| Human code \ Model label | Confabulation (fabrication) | Misclassification (factual error) | Both | None or unclear | Row total |
|---|---|---|---|---|---|
| Confabulation (fabrication) | 7 | 1 | 2 | 0 | 10 |
| Misclassification (factual error) | 5 | 26 | 9 | 2 | 42 |
| Both | 2 | 0 | 11 | 0 | 13 |
| None or unclear | 6 | 6 | 0 | 31 | 43 |
| Column total | 20 | 33 | 22 | 33 | 108 |

b)

| Human code \ Model label | Generative | Discriminative | Both | Unclear | Row total |
|---|---|---|---|---|---|
| Generative | 60 | 1 | 1 | 0 | 62 |
| Discriminative | 0 | 23 | 0 | 4 | 27 |
| Both | 0 | 1 | 3 | 0 | 4 |
| Unclear | 1 | 2 | 0 | 12 | 15 |
| Column total | 61 | 27 | 4 | 16 | 108 |

c)

| Axis | class | support (human) | n (model) | precision | recall | F1 |
|---|---|---|---|---|---|---|
| Failure mode | Confabulation (fabrication) | 10 | 20 | 0.35 (0.14–0.56) | 0.70 (0.38–1.00) | 0.47 (0.21–0.67) |
| Failure mode | Misclassification (factual error) | 42 | 33 | 0.79 (0.64–0.93) | 0.62 (0.46–0.76) | 0.69 (0.55–0.81) |
| Failure mode | Both | 13 | 22 | 0.50 (0.29–0.72) | 0.85 (0.61–1.00) | 0.63 (0.40–0.80) |
| Failure mode | None or unclear | 43 | 33 | 0.94 (0.85–1.00) | 0.72 (0.59–0.85) | 0.82 (0.71–0.90) |
| Failure mode | macro-F1 | 108 | 108 |  |  | 0.65 (0.55–0.75) |
| Model type | Generative | 62 | 61 | 0.98 (0.94–1.00) | 0.97 (0.92–1.00) | 0.98 (0.94–1.00) |
| Model type | Discriminative | 27 | 27 | 0.85 (0.71–0.97) | 0.85 (0.70–0.97) | 0.85 (0.73–0.94) |
| Model type | Both | 4 | 4 | 0.75 (0.00–1.00) | 0.75 (0.00–1.00) | 0.75 (0.00–1.00) |
| Model type | Unclear | 15 | 16 | 0.75 (0.50–0.94) | 0.80 (0.56–1.00) | 0.77 (0.56–0.92) |
| Model type | macro-F1 | 108 | 108 |  |  | 0.84 (0.66–0.94) |

## Output files

- [T3_confusion_failure_mode.csv](T3_confusion_failure_mode.csv)
- [T3_confusion_model_type.csv](T3_confusion_model_type.csv)
- [T3_perclass_metrics.csv](T3_perclass_metrics.csv)
- [T3_fabrication_direction.csv](T3_fabrication_direction.csv)
