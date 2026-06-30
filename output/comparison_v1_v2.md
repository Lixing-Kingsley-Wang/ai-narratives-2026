# v1 vs v2 stance classification — descriptive comparison

- v1 file: `output/classified_medical_Q1Q2.csv`
- v2 file: `output/classified_medical_Q1Q2_v2.csv`
- v1 rows: 16,759
- v2 rows: 16,759
- joined on pmid: 16,759

## 1. Stance distribution

| Stance | v1 n | v1 % | v2 n | v2 % | Δ n | Δ % |
|---|---:|---:|---:|---:|---:|---:|
| Alarm | 916 | 5.5% | 588 | 3.5% | -328 | -2.0pp |
| Caution | 4,245 | 25.3% | 3,667 | 21.9% | -578 | -3.4pp |
| Neutral | 838 | 5.0% | 2,916 | 17.4% | +2,078 | +12.4pp |
| Cautious Optimism | 10,515 | 62.7% | 9,397 | 56.1% | -1,118 | -6.7pp |
| Advocacy | 235 | 1.4% | 187 | 1.1% | -48 | -0.3pp |
| FAILED | 10 | 0.1% | 4 | 0.0% | -6 | -0.0pp |
| **Total** | **16,759** | 100.0% | **16,759** | 100.0% | | |

## 2. Migration matrix (v1 → v2)

Rows = v1 stance, columns = v2 stance. Diagonal = unchanged.

| v1 ↓ \ v2 → | Alarm | Caution | Neutral | Cautious Optimism | Advocacy | FAILED | row total |
|---|---|---|---|---|---|---|---|
| **Alarm** | 578 | 305 | 30 | 2 | 0 | 1 | 916 |
| **Caution** | 6 | 3,063 | 763 | 413 | 0 | 0 | 4,245 |
| **Neutral** | 2 | 20 | 792 | 21 | 1 | 2 | 838 |
| **Cautious Optimism** | 0 | 277 | 1,322 | 8,863 | 53 | 0 | 10,515 |
| **Advocacy** | 1 | 0 | 9 | 91 | 133 | 1 | 235 |
| **FAILED** | 1 | 2 | 0 | 7 | 0 | 0 | 10 |
| **col total** | 588 | 3,667 | 2,916 | 9,397 | 187 | 4 | 16,759 |

- Unchanged (diagonal): **13,429** (80.1%)
- Changed: **3,330** (19.9%)

## 3. Largest migration flows (top 5, off-diagonal)

### 1. Cautious Optimism → Neutral  (n = 1,322)

| pmid | pub_year | title (first 100 chars) |
|---|---|---|
| 40985091 | 2025 | Standardisation of an AI-based vocal fold assessment tool on a recurrent respiratory papillomatosis  |
| 41193978 | 2025 | A methodology for developing dermatological datasets: lessons from retrospective data collection for |
| 41469047 | 2025 | Evaluation of visual patient predictive for enhancing level 3 situation awareness: protocol for a mu |
| 41326304 | 2025 | A benchmark of text embedding models for semantic harmonization of Alzheimer's disease cohorts. |
| 40035038 | 2025 | The application of artificial intelligence in insomnia, anxiety, and depression: A bibliometric anal |

### 2. Caution → Neutral  (n = 763)

| pmid | pub_year | title (first 100 chars) |
|---|---|---|
| 40323320 | 2025 | Adoption of artificial intelligence in healthcare: survey of health system priorities, successes, an |
| 32380551 | 2021 | Reflection on modern methods: generalized linear models for prognosis and intervention-theory, pract |
| 41118646 | 2025 | Improving Large Language Model Applications in the Medical and Nursing Domains With Retrieval-Augmen |
| 40997490 | 2026 | Trust when the healthcare ecosystem is integrated with Artificial Intelligence. |
| 39629551 | 2024 | An Early Snapshot of Attitudes Toward Generative Artificial Intelligence in Physical Therapy Educati |

### 3. Caution → Cautious Optimism  (n = 413)

| pmid | pub_year | title (first 100 chars) |
|---|---|---|
| 40816978 | 2025 | Exploring the potential of generative artificial intelligence in medical image synthesis: opportunit |
| 35681603 | 2022 | Machine Learning Tools for Image-Based Glioma Grading and the Quality of Their Reporting: Challenges |
| 40589366 | 2025 | Diagnostic Performance of ChatGPT-4o and DeepSeek-3 Differential Diagnosis of Complex Oral Lesions:  |
| 41057716 | 2025 | Comparative analysis of generic vision-language models in detecting and diagnosing inherited retinal |
| 39873858 | 2025 | Can surgeons trust AI? Perspectives on machine learning in surgery and the importance of eXplainable |

### 4. Alarm → Caution  (n = 305)

| pmid | pub_year | title (first 100 chars) |
|---|---|---|
| 39446672 | 2025 | Performance of ChatGPT and Dental Students on Concepts of Periodontal Surgery. |
| 40055532 | 2025 | Red teaming ChatGPT in medicine to yield real-world insights on model behavior. |
| 39622288 | 2025 | Comparative Analysis of Large Language Models and Spine Surgeons in Surgical Decision-Making and Rad |
| 42054485 | 2026 | Large language models and statistical calculations: a cautionary note. |
| 39952325 | 2025 | American Academy of Orthopaedic Surgeons OrthoInfo provides more readable information regarding rota |

### 5. Cautious Optimism → Caution  (n = 277)

| pmid | pub_year | title (first 100 chars) |
|---|---|---|
| 41424220 | 2025 | Artificial intelligence in rehabilitation: a living systematic mapping review - first release. |
| 36270953 | 2023 | Artificial intelligence in musculoskeletal oncology imaging: A critical review of current applicatio |
| 40882392 | 2025 | Artificial intelligence as treatment support in breast cancer: current perspectives. |
| 40234594 | 2025 | ChatGPT-4 for addressing patient-centred frequently asked questions in age-related macular degenerat |
| 39084480 | 2024 | Rare disease diagnosis using knowledge guided retrieval augmentation for ChatGPT. |

## 4. predictive_claim flag flips

- predictive_claim=yes in v1: **9,399** (56.1%)
- predictive_claim=yes in v2: **1,333** (8.0%)
- Unchanged: 8,685
- Flipped yes → no: 8,070
- Flipped no → yes: 4

## 5. v2 stance distribution by year

| year | Alarm | Caution | Neutral | Cautious Optimism | Advocacy | FAILED | total |
|---|---|---|---|---|---|---|---|
| 2020 | 0 | 0 | 2 | 0 | 0 | 0 | 2 |
| 2021 | 23 | 180 | 253 | 591 | 17 | 0 | 1,064 |
| 2022 | 25 | 238 | 308 | 757 | 16 | 0 | 1,344 |
| 2023 | 59 | 461 | 426 | 1,075 | 33 | 1 | 2,055 |
| 2024 | 160 | 881 | 609 | 1,999 | 53 | 2 | 3,704 |
| 2025 | 213 | 1,277 | 904 | 3,450 | 55 | 0 | 5,899 |
| 2026 | 108 | 630 | 414 | 1,525 | 13 | 1 | 2,691 |

## 6. meta_discourse (v2 only, new field)

- meta_discourse=yes: **1,076** (6.4%)

Stance of meta-discourse papers (per v2 rubric: default Neutral unless authors editorialize):

| stance_v2 | n |
|---|---:|
| Caution | 89 |
| Neutral | 888 |
| Cautious Optimism | 99 |

