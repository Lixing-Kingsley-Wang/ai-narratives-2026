# Validation κ Report — v2 (revised prompt), EXPLORATORY

**This is an exploratory κ pass on the v2 re-classification.** The official, pre-registered validation κ stands at the v1 value (see `kappa_report.md`). This pass is for diagnostic purposes only and was NOT used to select the v2 prompt — the 300-record validation set was sampled before v2 existed.

_LLM stance source: `classified_medical_Q1Q2_v2_pre_predclaim_fix.csv` (revised prompt, batch v2a)._
_Human stance source: `kingsly_coding_sheet.xlsx`._

## Sample

- Total records (after dropping v2 FAILED): **300**
- Flag counts:
    - NO_STANCE: 73
    - OUT_OF_SCOPE: 2
    - DATA_INSUFFICIENT: 0
    - META_DISCOURSE: 14
- Records with more than one flag: **7**

## Distribution

| Stance | LLM v2 | Human (Kingsley) |
|---|---:|---:|
| Alarm | 26 | 36 |
| Caution | 57 | 59 |
| Neutral | 94 | 88 |
| Cautious Optimism | 110 | 93 |
| Advocacy | 13 | 24 |

## κ values

All 95% CIs are bootstrap percentile (n_boot=1000, seed=42).

| Layer | n | Unweighted κ | Linear κ | Quadratic κ |
|---|---:|---|---|---|
| Primary | 300 | 0.583 (0.511–0.651) | 0.675 (0.616–0.736) | 0.766 (0.710–0.825) |
| Sensitivity A | 225 | 0.548 (0.460–0.631) | 0.683 (0.608–0.746) | 0.790 (0.724–0.843) |
| Sensitivity B | 218 | 0.548 (0.464–0.631) | 0.686 (0.611–0.752) | 0.792 (0.725–0.848) |

## Confusion matrices (v2 LLM)

### Primary (n=300)

```
Human \ LLM  |    Alarm |  Caution |  Neutral | Cautious | Advocacy | Total
---------------------------------------------------------------------------
Alarm        |       24 |       11 |        0 |        1 |        0 |    36
Caution      |        2 |       34 |        8 |       15 |        0 |    59
Neutral      |        0 |        6 |       69 |       12 |        1 |    88
Cautious Optimism|        0 |        6 |       17 |       69 |        1 |    93
Advocacy     |        0 |        0 |        0 |       13 |       11 |    24
---------------------------------------------------------------------------
Total        |       26 |       57 |       94 |      110 |       13 |   300
```

### Sensitivity A (n=225)

```
Human \ LLM  |    Alarm |  Caution |  Neutral | Cautious | Advocacy | Total
---------------------------------------------------------------------------
Alarm        |       24 |       11 |        0 |        1 |        0 |    36
Caution      |        2 |       33 |        8 |       15 |        0 |    58
Neutral      |        0 |        0 |       14 |        0 |        0 |    14
Cautious Optimism|        0 |        6 |       17 |       69 |        1 |    93
Advocacy     |        0 |        0 |        0 |       13 |       11 |    24
---------------------------------------------------------------------------
Total        |       26 |       50 |       39 |       98 |       12 |   225
```

### Sensitivity B (n=218)

```
Human \ LLM  |    Alarm |  Caution |  Neutral | Cautious | Advocacy | Total
---------------------------------------------------------------------------
Alarm        |       24 |       11 |        0 |        1 |        0 |    36
Caution      |        2 |       32 |        6 |       15 |        0 |    55
Neutral      |        0 |        0 |       11 |        0 |        0 |    11
Cautious Optimism|        0 |        6 |       16 |       69 |        1 |    92
Advocacy     |        0 |        0 |        0 |       13 |       11 |    24
---------------------------------------------------------------------------
Total        |       26 |       49 |       33 |       98 |       12 |   218
```

## Top disagreement patterns (Primary layer)

| Human | LLM v2 | n |
|---|---|---:|
| Cautious Optimism | Neutral | 17 |
| Caution | Cautious Optimism | 15 |
| Advocacy | Cautious Optimism | 13 |
| Neutral | Cautious Optimism | 12 |
| Alarm | Caution | 11 |
| Caution | Neutral | 8 |
| Cautious Optimism | Caution | 6 |
| Neutral | Caution | 6 |
| Caution | Alarm | 2 |
| Alarm | Cautious Optimism | 1 |

## Per-stance metrics (Primary layer)

| Stance | Human n | LLM n | Precision | Recall | Agreement |
|---|---:|---:|---:|---:|---:|
| Alarm | 36 | 26 | 0.923 | 0.667 | 0.667 |
| Caution | 59 | 57 | 0.596 | 0.576 | 0.576 |
| Neutral | 88 | 94 | 0.734 | 0.784 | 0.784 |
| Cautious Optimism | 93 | 110 | 0.627 | 0.742 | 0.742 |
| Advocacy | 24 | 13 | 0.846 | 0.458 | 0.458 |
