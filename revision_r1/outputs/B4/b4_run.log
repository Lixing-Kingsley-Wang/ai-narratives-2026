# B4 · Multivariable regression (D4a, X3, D3)

Script `revision_r1/scripts/b4_regression.py` (statsmodels 0.15.0, `revision_r1/.venv`). Records: 2021–2025 analytic set (n = 14,058). Year continuous, centred on 2023.856. Cluster-robust SEs by journal (normalised SJR-matching title). Not included: model type (defined only among critical records) and FDA cleared-device count (18-unit ecological variable).

## Primary: logistic, critical (Alarm or Caution) vs not

n = 14,058; events = 4,283; clusters (journals) = 2,278. Reference levels (most frequent): genre = discourse; pubtype = Research Article; specialty = Medical Informatics / Digital Health; region = North America.

| variable | level | adjusted OR (95% CI) | P (adj.) | unadjusted OR (95% CI) | P (unadj.) |
|---|---|---|---|---|---|
| genre | evaluative | 0.54 (0.48–0.61) | <.001 | 0.63 (0.55–0.71) | <.001 |
| pubtype | Commentary | 1.79 (0.98–3.26) | .056 | 2.63 (1.34–5.15) | .005 |
| pubtype | Editorial | 0.73 (0.56–0.95) | .018 | 1.21 (0.94–1.57) | .140 |
| pubtype | Letter | 1.16 (0.90–1.51) | .249 | 1.40 (1.11–1.78) | .005 |
| pubtype | Review | 0.47 (0.41–0.54) | <.001 | 0.66 (0.58–0.75) | <.001 |
| specialty | Cardiology | 0.28 (0.21–0.36) | <.001 | 0.23 (0.18–0.30) | <.001 |
| specialty | Dentistry | 0.52 (0.42–0.64) | <.001 | 0.40 (0.33–0.50) | <.001 |
| specialty | Dermatology | 0.76 (0.59–0.98) | .037 | 0.72 (0.56–0.94) | .015 |
| specialty | Emergency Medicine / Critical Care | 0.53 (0.40–0.69) | <.001 | 0.47 (0.36–0.61) | <.001 |
| specialty | Internal Medicine / Primary Care | 0.41 (0.34–0.49) | <.001 | 0.33 (0.27–0.41) | <.001 |
| specialty | Medical Education | 0.58 (0.47–0.71) | <.001 | 0.65 (0.52–0.81) | <.001 |
| specialty | Mental Health / Psychiatry | 1.22 (0.94–1.60) | .140 | 1.22 (0.93–1.62) | .155 |
| specialty | Multidisciplinary / Other | 0.59 (0.42–0.83) | .002 | 0.57 (0.41–0.80) | <.001 |
| specialty | Neurology / Neuroscience | 0.44 (0.32–0.61) | <.001 | 0.38 (0.27–0.52) | <.001 |
| specialty | Nursing | 0.85 (0.60–1.20) | .349 | 0.86 (0.61–1.20) | .368 |
| specialty | Obstetrics / Gynecology | 0.46 (0.33–0.65) | <.001 | 0.41 (0.29–0.57) | <.001 |
| specialty | Oncology | 0.35 (0.30–0.42) | <.001 | 0.28 (0.23–0.34) | <.001 |
| specialty | Ophthalmology | 0.36 (0.30–0.44) | <.001 | 0.28 (0.22–0.34) | <.001 |
| specialty | Pathology / Laboratory Medicine | 0.37 (0.29–0.47) | <.001 | 0.31 (0.24–0.40) | <.001 |
| specialty | Pediatrics | 0.42 (0.32–0.55) | <.001 | 0.38 (0.29–0.50) | <.001 |
| specialty | Radiology / Diagnostic Imaging | 0.40 (0.34–0.46) | <.001 | 0.31 (0.26–0.37) | <.001 |
| specialty | Surgery | 0.54 (0.46–0.64) | <.001 | 0.50 (0.42–0.59) | <.001 |
| specialty | Unassigned | 0.16 (0.02–1.45) | .104 | 0.13 (0.02–1.07) | .058 |
| region | East Asia | 0.44 (0.38–0.51) | <.001 | 0.40 (0.34–0.47) | <.001 |
| region | Eastern Europe | 0.80 (0.61–1.04) | .098 | 0.72 (0.55–0.96) | .025 |
| region | Latin America / Oceania | 1.11 (0.93–1.33) | .237 | 1.16 (0.97–1.39) | .109 |
| region | Middle East / North Africa | 0.79 (0.68–0.91) | .001 | 0.79 (0.68–0.92) | .002 |
| region | South/Southeast Asia | 0.57 (0.46–0.71) | <.001 | 0.60 (0.49–0.74) | <.001 |
| region | Sub-Saharan Africa | 1.11 (0.60–2.06) | .731 | 1.40 (0.75–2.63) | .295 |
| region | Unknown | 0.74 (0.57–0.98) | .034 | 0.89 (0.62–1.28) | .538 |
| region | Western Europe | 1.06 (0.95–1.19) | .296 | 0.98 (0.87–1.12) | .796 |
| year (per 1 year) |  | 1.10 (1.07–1.14) | <.001 | 1.08 (1.04–1.12) | <.001 |

Average marginal predicted probability of critical stance (%, 95% CI; delta method on the logit scale, cluster-robust):

**year**: 2021 25.3 (23.3–27.5); 2022 27.1 (25.4–28.8); 2023 28.8 (27.5–30.2); 2024 30.7 (29.5–31.8); 2025 32.6 (31.3–33.9)

**specialty**: Cardiology 17.6 (14.3–21.4); Dentistry 28.1 (24.4–32.1); Dermatology 35.9 (30.7–41.6); Emergency Medicine / Critical Care 28.2 (23.7–33.2); Internal Medicine / Primary Care 23.4 (20.6–26.5); Medical Education 30.1 (26.5–33.9); Medical Informatics / Digital Health 42.0 (39.6–44.4); Mental Health / Psychiatry 46.7 (40.6–52.9); Multidisciplinary / Other 30.6 (24.2–37.7); Neurology / Neuroscience 25.0 (20.0–30.7); Nursing 38.2 (30.9–45.9); Obstetrics / Gynecology 25.7 (20.1–32.3); Oncology 21.1 (18.8–23.7); Ophthalmology 21.6 (18.7–24.8); Pathology / Laboratory Medicine 21.8 (18.2–25.9); Pediatrics 24.0 (19.8–28.8); Radiology / Diagnostic Imaging 23.0 (20.9–25.3); Surgery 28.7 (26.3–31.3); Unassigned 11.1 (1.4–51.7)

**region**: East Asia 19.3 (17.3–21.6); Eastern Europe 29.4 (24.7–34.7); Latin America / Oceania 36.2 (32.7–39.8); Middle East / North Africa 29.3 (26.9–31.8); North America 33.9 (32.4–35.5); South/Southeast Asia 23.5 (20.4–27.0); Sub-Saharan Africa 36.2 (24.4–49.9); Unknown 28.2 (23.5–33.3); Western Europe 35.2 (33.1–37.5)

**pubtype**: Commentary 48.0 (35.2–61.2); Editorial 29.2 (24.8–34.0); Letter 38.6 (33.5–43.8); Research Article 35.4 (33.9–36.9); Review 21.5 (19.6–23.6)

**genre**: discourse 36.0 (34.1–37.9); evaluative 24.3 (23.1–25.7)


## Secondary 1: ordinal proportional-odds model (Alarm < Caution < Neutral < Cautious Optimism < Advocacy)

n = 14,058; covariance: cluster-robust (journal). Coefficients are log-odds of a more favourable category (positive = more favourable).

| variable/level | ordinal OR (95% CI) | P | OR >Alarm | OR >Caution | OR >Neutral | OR >Cautious Optimism | proportional-odds check |
|---|---|---|---|---|---|---|---|
| genre evaluative | 1.36 (1.22–1.51) | <.001 | 0.19 | 1.84 | 1.70 | 0.16 | outside CI at >Alarm,Caution,Neutral,Cautious Optimism; sign change |
| pubtype Commentary | 0.59 (0.39–0.87) | .009 | 0.38 | 0.56 | 0.60 | 0.82 | holds |
| pubtype Editorial | 1.33 (1.04–1.68) | .021 | 1.07 | 1.37 | 1.19 | 3.33 | outside CI at >Cautious Optimism |
| pubtype Letter | 0.65 (0.51–0.83) | <.001 | 0.66 | 0.86 | 0.42 | 3.49 | outside CI at >Caution,Neutral,Cautious Optimism; sign change |
| pubtype Review | 2.10 (1.85–2.37) | <.001 | 2.61 | 2.13 | 2.42 | 0.89 | outside CI at >Neutral,Cautious Optimism; sign change |
| specialty Cardiology | 3.47 (2.80–4.32) | <.001 | 2.16 | 3.59 | 3.97 | 1.49 | outside CI at >Cautious Optimism |
| specialty Dentistry | 1.85 (1.51–2.27) | <.001 | 1.44 | 1.91 | 2.08 | 0.38 | outside CI at >Cautious Optimism; sign change |
| specialty Dermatology | 1.32 (1.00–1.74) | .048 | 0.95 | 1.31 | 1.49 | 1.02 | sign change |
| specialty Emergency Medicine / Critical Care | 1.84 (1.43–2.37) | <.001 | 1.12 | 1.90 | 2.18 | 0.23 | outside CI at >Cautious Optimism; sign change |
| specialty Internal Medicine / Primary Care | 2.52 (2.12–2.99) | <.001 | 1.85 | 2.47 | 2.93 | 0.95 | outside CI at >Cautious Optimism; sign change |
| specialty Medical Education | 1.77 (1.48–2.11) | <.001 | 2.51 | 1.73 | 1.99 | 0.57 | outside CI at >Cautious Optimism; sign change |
| specialty Mental Health / Psychiatry | 0.91 (0.72–1.14) | .399 | 1.08 | 0.82 | 1.02 | 0.12 | outside CI at >Cautious Optimism; sign change |
| specialty Multidisciplinary / Other | 1.72 (1.26–2.35) | <.001 | 1.13 | 1.69 | 2.00 | 1.01 | holds |
| specialty Neurology / Neuroscience | 2.24 (1.69–2.98) | <.001 | 1.17 | 2.26 | 2.52 | 1.35 | outside CI at >Alarm |
| specialty Nursing | 1.22 (0.90–1.66) | .194 | 1.29 | 1.18 | 1.40 | 0.33 | sign change |
| specialty Obstetrics / Gynecology | 2.31 (1.67–3.20) | <.001 | 1.79 | 2.17 | 2.64 | 1.09 | holds |
| specialty Oncology | 2.69 (2.31–3.14) | <.001 | 2.17 | 2.83 | 3.01 | 1.04 | outside CI at >Cautious Optimism |
| specialty Ophthalmology | 2.50 (2.10–2.98) | <.001 | 2.12 | 2.75 | 2.93 | 0.22 | outside CI at >Cautious Optimism; sign change |
| specialty Pathology / Laboratory Medicine | 2.37 (1.93–2.91) | <.001 | 1.63 | 2.72 | 2.68 | 0.62 | outside CI at >Cautious Optimism; sign change |
| specialty Pediatrics | 2.37 (1.86–3.03) | <.001 | 1.71 | 2.39 | 2.78 | 0.44 | outside CI at >Cautious Optimism; sign change |
| specialty Radiology / Diagnostic Imaging | 2.30 (2.03–2.62) | <.001 | 2.13 | 2.53 | 2.53 | 0.52 | outside CI at >Cautious Optimism; sign change |
| specialty Surgery | 1.95 (1.65–2.30) | <.001 | 1.20 | 1.85 | 2.25 | 1.17 | outside CI at >Alarm,Cautious Optimism |
| specialty Unassigned | 3.44 (0.94–12.62) | .062 | 1.19 | 6.21 | 3.82 | 0.00 | outside CI at >Cautious Optimism; sign change |
| region East Asia | 1.90 (1.70–2.14) | <.001 | 1.98 | 2.28 | 1.97 | 0.78 | outside CI at >Caution,Cautious Optimism; sign change |
| region Eastern Europe | 1.17 (0.93–1.48) | .177 | 0.79 | 1.25 | 1.20 | 0.85 | sign change |
| region Latin America / Oceania | 0.89 (0.75–1.05) | .154 | 1.06 | 0.90 | 0.87 | 0.68 | sign change |
| region Middle East / North Africa | 1.30 (1.13–1.49) | <.001 | 1.02 | 1.27 | 1.32 | 1.67 | holds |
| region South/Southeast Asia | 1.81 (1.48–2.22) | <.001 | 1.59 | 1.74 | 1.77 | 2.28 | holds |
| region Sub-Saharan Africa | 0.98 (0.55–1.75) | .947 | 0.77 | 0.90 | 0.96 | 2.06 | sign change |
| region Unknown | 1.21 (0.97–1.51) | .088 | 0.95 | 1.34 | 1.15 | 1.36 | sign change |
| region Western Europe | 0.95 (0.86–1.05) | .300 | 1.12 | 0.94 | 0.95 | 0.45 | outside CI at >Cautious Optimism; sign change |
| year (per 1 year) | 0.94 (0.92–0.97) | <.001 | 0.94 | 0.91 | 0.97 | 0.84 | outside CI at >Caution,Cautious Optimism |

Proportional odds fails (by the pre-specified rule) for 27 of 32 terms.

## Secondary 2: logistic, Advocacy vs not

n = 14,058; events = 218; clusters = 2,278. Reference levels: genre = discourse; pubtype = Research Article; specialty = Medical Informatics / Digital Health; region = North America. Levels with <5 Advocacy events collapsed into 'Other (<5 events)': specialty: Dentistry, Emergency Medicine / Critical Care, Mental Health / Psychiatry, Nursing, Obstetrics / Gynecology, Ophthalmology, Pathology / Laboratory Medicine, Pediatrics, Unassigned; region: Eastern Europe, Sub-Saharan Africa; pubtype: Commentary.

| variable | level | adjusted OR (95% CI) | P |
|---|---|---|---|
| genre | evaluative | 0.17 (0.10–0.27) | <.001 |
| pubtype | Editorial | 3.31 (1.96–5.61) | <.001 |
| pubtype | Letter | 3.48 (2.18–5.54) | <.001 |
| pubtype | Other (<5 events) | 0.81 (0.17–3.89) | .788 |
| pubtype | Review | 0.90 (0.62–1.31) | .571 |
| specialty | Cardiology | 1.47 (0.79–2.72) | .220 |
| specialty | Dermatology | 1.02 (0.40–2.60) | .972 |
| specialty | Internal Medicine / Primary Care | 0.95 (0.52–1.71) | .855 |
| specialty | Medical Education | 0.57 (0.31–1.06) | .077 |
| specialty | Multidisciplinary / Other | 1.02 (0.41–2.52) | .966 |
| specialty | Neurology / Neuroscience | 1.34 (0.58–3.09) | .493 |
| specialty | Oncology | 1.03 (0.60–1.79) | .902 |
| specialty | Other (<5 events) | 0.36 (0.21–0.63) | <.001 |
| specialty | Radiology / Diagnostic Imaging | 0.51 (0.29–0.92) | .026 |
| specialty | Surgery | 1.16 (0.70–1.93) | .565 |
| region | East Asia | 0.78 (0.49–1.23) | .283 |
| region | Latin America / Oceania | 0.67 (0.32–1.40) | .284 |
| region | Middle East / North Africa | 1.66 (1.00–2.74) | .049 |
| region | Other (<5 events) | 1.06 (0.47–2.37) | .895 |
| region | South/Southeast Asia | 2.25 (1.32–3.84) | .003 |
| region | Unknown | 1.35 (0.71–2.57) | .360 |
| region | Western Europe | 0.45 (0.30–0.70) | <.001 |
| year (per 1 year) |  | 0.84 (0.75–0.94) | .002 |

Average marginal predicted probability of Advocacy by year (%): 2021 2.37 (1.78–3.16); 2022 2.02 (1.64–2.47); 2023 1.71 (1.48–1.98); 2024 1.45 (1.25–1.69); 2025 1.23 (0.99–1.53)

## Sensitivity models (critical outcome)

| model | n | events | journals | year effect |
|---|---|---|---|---|
| Primary (continuous year) | 14,058 | 4,283 | 2,278 | OR/yr 1.103 (1.066–1.141), P<.001 |
| S1 year categorical (ref 2021) | 14,058 | 4,283 | 2,278 | 2022: 1.001 (0.827–1.211), P=.993; 2023: 1.305 (1.093–1.558), P=.003; 2024: 1.532 (1.302–1.803), P<.001; 2025: 1.446 (1.232–1.698), P<.001 |
| S2 adding Jan–Apr 2026 (ref 2021) | 16,747 | 5,161 | 2,453 | 2022: 0.997 (0.825–1.206), P=.978; 2023: 1.298 (1.088–1.548), P=.004; 2024: 1.529 (1.300–1.798), P<.001; 2025: 1.441 (1.229–1.690), P<.001; 2026: 1.610 (1.349–1.921), P<.001 |
| S3 journal fixed effects (≥10 records, outcome varies) | 8,529 | 2,728 | 275 | OR/yr 1.082 (1.030–1.137), P=.002 |
| S4 country (≥100 records; reference United States) | 14,058 | 4,283 | 2,278 | OR/yr 1.110 (1.073–1.149), P<.001 |

Adjusted United States vs China (S4): OR 2.81 (2.26–3.48), P<.001. Countries kept as their own level: Australia, Brazil, Canada, China, France, Germany, India, Iran, Israel, Italy, Japan, Netherlands, Saudi Arabia, Singapore, South Korea, Spain, Sweden, Switzerland, Taiwan, Turkey, United Kingdom, United States.

