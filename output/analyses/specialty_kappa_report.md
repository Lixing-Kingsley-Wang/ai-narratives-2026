# Specialty validation — inter-rater agreement (human vs classifier)

Coded rows: **120/120**. Primary statistic: unweighted Cohen's κ (nominal — specialty labels are unordered). Also reported: Scott's π / Fleiss (pooled-marginal chance), **Gwet's AC1** (robust to the prevalence paradox), PABAK (uniform chance), and **κ_max** (best κ achievable given the two marginals — a bias/marginal mismatch caps it below 1). Weighted κ is intentionally NOT used. Strength labels per Landis & Koch (1977).


## specialty — including 'Unclear' as a category

Human 'Unclear / cannot determine from abstract' is treated as its own category. The model never emits it, so its model column is all-zero.

- n = 120
- **Cohen's κ = +0.753** (substantial); raw agreement = 76.7% (chance p_e = 0.056)
- Scott's π / Fleiss = +0.752 · **Gwet's AC1 = +0.754** · PABAK = +0.754
- κ_max = 0.850 (κ/κ_max = 0.89) — marginal mismatch caps the achievable κ

Confusion matrix (rows = human, cols = model):

| | M:Radiology / Diagnostic Imaging | M:Pathology / Laboratory Medicine | M:Cardiology | M:Oncology | M:Surgery | M:Ophthalmology | M:Dermatology | M:Neurology / Neuroscience | M:Mental Health / Psychiatry | M:Internal Medicine / Primary Care | M:Emergency Medicine / Critical Care | M:Pediatrics | M:Obstetrics / Gynecology | M:Dentistry | M:Medical Informatics / Digital Health | M:Nursing | M:Medical Education | M:Multidisciplinary / Other | M:Unclear / cannot determine from abstract |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **H:Radiology / Diagnostic Imaging** | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| **H:Pathology / Laboratory Medicine** | 0 | 6 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| **H:Cardiology** | 0 | 0 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **H:Oncology** | 2 | 1 | 0 | 7 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 0 |
| **H:Surgery** | 0 | 0 | 0 | 0 | 5 | 0 | 0 | 2 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **H:Ophthalmology** | 0 | 0 | 0 | 0 | 0 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **H:Dermatology** | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| **H:Neurology / Neuroscience** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **H:Mental Health / Psychiatry** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 6 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **H:Internal Medicine / Primary Care** | 0 | 0 | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **H:Emergency Medicine / Critical Care** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 6 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| **H:Pediatrics** | 0 | 0 | 0 | 0 | 1 | 3 | 0 | 0 | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **H:Obstetrics / Gynecology** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 5 | 0 | 0 | 0 | 0 | 0 | 0 |
| **H:Dentistry** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 6 | 0 | 0 | 0 | 0 | 0 |
| **H:Medical Informatics / Digital Health** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 4 | 0 | 0 | 0 | 0 |
| **H:Nursing** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 5 | 2 | 0 | 0 |
| **H:Medical Education** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 4 | 0 | 0 |
| **H:Multidisciplinary / Other** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 7 | 0 |
| **H:Unclear / cannot determine from abstract** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

Per-category one-vs-rest κ:

| category | κ | agreement |
|---|--:|--:|
| Radiology / Diagnostic Imaging | +0.714 | 97.5% |
| Pathology / Laboratory Medicine | +0.787 | 97.5% |
| Cardiology | +1.000 | 100.0% |
| Oncology | +0.605 | 93.3% |
| Surgery | +0.645 | 95.8% |
| Ophthalmology | +0.715 | 97.5% |
| Dermatology | +0.425 | 95.8% |
| Neurology / Neuroscience | +0.825 | 98.3% |
| Mental Health / Psychiatry | +0.919 | 99.2% |
| Internal Medicine / Primary Care | +0.866 | 98.3% |
| Emergency Medicine / Critical Care | +0.848 | 98.3% |
| Pediatrics | +0.431 | 94.2% |
| Obstetrics / Gynecology | +0.756 | 97.5% |
| Dentistry | +0.919 | 99.2% |
| Medical Informatics / Digital Health | +0.715 | 97.5% |
| Nursing | +0.697 | 96.7% |
| Medical Education | +0.715 | 97.5% |
| Multidisciplinary / Other | +0.929 | 99.2% |
| Unclear / cannot determine from abstract | +nan | 100.0% |


## specialty — excluding 'Unclear' (sensitivity)

Sensitivity analysis: the 0 row(s) the human marked 'Unclear / cannot determine from abstract' are excluded; only the 18 canonical categories are scored.

- n = 120
- **Cohen's κ = +0.753** (substantial); raw agreement = 76.7% (chance p_e = 0.056)
- Scott's π / Fleiss = +0.752 · **Gwet's AC1 = +0.753** · PABAK = +0.753
- κ_max = 0.850 (κ/κ_max = 0.89) — marginal mismatch caps the achievable κ

Confusion matrix (rows = human, cols = model):

| | M:Radiology / Diagnostic Imaging | M:Pathology / Laboratory Medicine | M:Cardiology | M:Oncology | M:Surgery | M:Ophthalmology | M:Dermatology | M:Neurology / Neuroscience | M:Mental Health / Psychiatry | M:Internal Medicine / Primary Care | M:Emergency Medicine / Critical Care | M:Pediatrics | M:Obstetrics / Gynecology | M:Dentistry | M:Medical Informatics / Digital Health | M:Nursing | M:Medical Education | M:Multidisciplinary / Other |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **H:Radiology / Diagnostic Imaging** | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| **H:Pathology / Laboratory Medicine** | 0 | 6 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| **H:Cardiology** | 0 | 0 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **H:Oncology** | 2 | 1 | 0 | 7 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 1 | 0 | 0 | 0 |
| **H:Surgery** | 0 | 0 | 0 | 0 | 5 | 0 | 0 | 2 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **H:Ophthalmology** | 0 | 0 | 0 | 0 | 0 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **H:Dermatology** | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| **H:Neurology / Neuroscience** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **H:Mental Health / Psychiatry** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 6 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| **H:Internal Medicine / Primary Care** | 0 | 0 | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **H:Emergency Medicine / Critical Care** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 6 | 0 | 0 | 0 | 0 | 1 | 0 | 0 |
| **H:Pediatrics** | 0 | 0 | 0 | 0 | 1 | 3 | 0 | 0 | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 0 |
| **H:Obstetrics / Gynecology** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 5 | 0 | 0 | 0 | 0 | 0 |
| **H:Dentistry** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 6 | 0 | 0 | 0 | 0 |
| **H:Medical Informatics / Digital Health** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 4 | 0 | 0 | 0 |
| **H:Nursing** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 5 | 2 | 0 |
| **H:Medical Education** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 4 | 0 |
| **H:Multidisciplinary / Other** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 7 |

Per-category one-vs-rest κ:

| category | κ | agreement |
|---|--:|--:|
| Radiology / Diagnostic Imaging | +0.714 | 97.5% |
| Pathology / Laboratory Medicine | +0.787 | 97.5% |
| Cardiology | +1.000 | 100.0% |
| Oncology | +0.605 | 93.3% |
| Surgery | +0.645 | 95.8% |
| Ophthalmology | +0.715 | 97.5% |
| Dermatology | +0.425 | 95.8% |
| Neurology / Neuroscience | +0.825 | 98.3% |
| Mental Health / Psychiatry | +0.919 | 99.2% |
| Internal Medicine / Primary Care | +0.866 | 98.3% |
| Emergency Medicine / Critical Care | +0.848 | 98.3% |
| Pediatrics | +0.431 | 94.2% |
| Obstetrics / Gynecology | +0.756 | 97.5% |
| Dentistry | +0.919 | 99.2% |
| Medical Informatics / Digital Health | +0.715 | 97.5% |
| Nursing | +0.697 | 96.7% |
| Medical Education | +0.715 | 97.5% |
| Multidisciplinary / Other | +0.929 | 99.2% |
