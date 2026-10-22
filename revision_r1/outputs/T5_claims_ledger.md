# T5 · Claims ledger (E12, E4, E13)

Script: `revision_r1/scripts/t5_claims_ledger.py` (sentence extraction `t5_extract.py`; cross-sectional recomputation `t5_crosssectional.py`, both windows side by side in [T5_crosssectional_both_windows.md](T5_crosssectional_both_windows.md)). Source text: the submitted manuscript converted with macOS `textutil`. Full ledger: [T5_claims_ledger.csv](T5_claims_ledger.csv).

- Quantitative statements (Abstract, Results, captions): **81**.
- Reproduced Y: 66; partial: 5; not re-checked: 2.
- Sentences with a percentage but no CI: **32**; with a percentage but no n/N: **34** (heuristic on the sentence text; see section 2).

## 1. Statements not fully reproduced

- **A08** (Abstract): Partial: 2,226 and 56–90% (recomputed 56.3–90.2%) reproduce; gated fabrication-involved share is 15.8% in 2023, 23.4%, 20.6%, 21.7% in 2024–2026, so '21–23% from 2023 onward' does not hold for 2023
- **R07** (Results): Not re-checked in Batch 1 (v2 is a sensitivity analysis)
- **R13** (Results): 17 Y; '5 drug discovery' is a manual reading of Table S2, not recomputed
- **R29** (Results): gated fabrication-involved share is 15.8% in 2023, 23.4%, 20.6%, 21.7% in 2024–2026, so '21–23% from 2023 onward' does not hold for 2023
- **R46** (Results): Partial: % and CIs reproduce; n does not (recomputed NA 35.1% (33.9–36.4) [1,743/4,961], WEU 35.1% (33.6–36.5) [1,506/4,296])
- **R47** (Results): Partial: % and CI reproduce; n does not (recomputed 18.5% (17.2–19.9) [604/3,260]; 3,262 appears in the older session2_summary.md with 19.5%)
- **R52** (Results): Partial: Commentary critical = 56/104 = 53.85% → 53.8% (manuscript 53.9% = sum of rounded Alarm 8.7 + Caution 45.2); others Y
- **C07** (Figure caption): Partial: Figure 1a asterisks agree with exact permutation P (Neutral exact P=.033, Advocacy .003), but Table S1 lists scipy asymptotic P for every row except Advocacy (Alarm/Caution/critical .072 vs exact .103; Neutral .019 vs exact .033)
- **C16** (Figure caption): Not checked (figure)

## 2. Percentages lacking a CI or n/N (E12, E4)

| ID | section | missing | sentence (truncated) |
|---|---|---|---|
| A04 | Abstract | n/N | Every LLM step was validated against blinded human coding (prefilter Cohen kappa 0.51; stance quadratic-weighted kappa 0.79, 95% CI 0.72-0.8… |
| A05 | Abstract | CI + n/N | Cautious Optimism was the majority stance (62.8%) and 30.8% of records were critical. |
| A06 | Abstract | n/N | Advocacy fell monotonically from 2.9% (2021) to 0.6% (partial 2026; Spearman rho -1.00), while critical share rose modestly from 25.4% (95% … |
| A08 | Abstract | CI | Within the hallucination-gated subset (n=2226), factual error was the majority mechanism every year (56% to 90%), while fabrication-involved… |
| A09 | Abstract | CI + n/N | Critical rate varied roughly threefold across 18 specialty and domain categories (51.3% in Mental Health and Psychiatry to 16.8% in Cardiolo… |
| A10 | Abstract | CI + n/N | Reviews were the least critical (24.9%) and most favourable (73.1%) format. |
| R04 | Results | CI + n/N | Overall, 30.8% were critical, comprising 916 Alarm and 4,245 Caution records, and 69.2% were non-critical. |
| R05 | Results | CI | Cautious Optimism was the majority stance at 62.8% (n=10,514), with Neutral at 5.0% (n=837) and Advocacy rare at 1.4% (n=235; Figure 1A). |
| R06 | Results | n/N | Critical share rose from 25.4% [22.9–28.1] in 2021 to 32.6% [30.9–34.4] in the partial 2026 stratum, a net increase of 7.25 percentage point… |
| R09 | Results | CI + n/N | Alarm rose from 2.7% in 2021 to 6.8% in 2024, and was 6.2% in partial 2026; Caution rose from 22.7% to 26.4% (Figure 1A). |
| R10 | Results | CI + n/N | Cautious Optimism remained the majority every year, ranging from 60.2% to 65.3%. |
| R12 | Results | CI + n/N | Advocacy fell from 2.9% in 2021 to 0.6% in 2026 (Spearman ρ=−1.00). |
| R16 | Results | CI + n/N | Critical share in discourse papers rose from 30.2% to 37.8% (Spearman ρ=+0.94), while the evaluative-paper share rose from 14.6% to 28.1% (ρ… |
| R24 | Results | CI + n/N | Regulation fell by 22.0 percentage points, while ethics/bias fell by 8.1 percentage points, from 36.7% in 2021 to 28.6% in 2026. |
| R28 | Results | CI + n/N | Within the hallucination-gated subset of 2,226 abstract-present records, factual error was the majority mechanism in every year, accounting … |
| R29 | Results | CI + n/N | Fabrication-involved papers, defined as fabrication alone or with factual error, rose from 0% in 2021 to roughly 21–23% from 2023 onward. |
| R30 | Results | CI + n/N | Across all 4,747 abstract-present critical records, the generative-model share rose from 5.3% in 2021 to 62.8% in partial 2026 (Spearman ρ=+… |
| R31 | Results | CI + n/N | Fabrication share also rose gradually (ρ=+0.94) but plateaued in the low teens, reaching 13.8% in 2026. |
| R32 | Results | CI + n/N | Among generative-model papers, fabrication remained near 20% across the period (21.8%, 22.9%, 19.7%, and 22.0%, in 2023-2026, respectively). |
| R33 | Results | CI + n/N | In total, 1,858 records (39.1%) concerned generative models without a fabrication concern; most instead assessed accuracy, bias, or judgment… |
| R37 | Results | n/N | It was highest in Mental Health/Psychiatry at 51.3% (46.8–55.5), Medical Informatics/Digital Health at 44.9% (43.5–46.4), and Nursing at 43.… |
| R38 | Results | n/N | It was lowest in Cardiology at 16.8% (14.1–19.8), Ophthalmology at 18.4% (15.7–21.2), and Oncology at 19.7% (17.8–21.8). |
| R44 | Results | CI + n/N | Rates were at or above 40% in several northern and western European countries and Australia, including the Netherlands at 44.4%, Denmark at … |
| R45 | Results | CI + n/N | Rates were near or below 20% in several East and South Asian countries and parts of the Middle East, including Japan at 18.3%, Iran at 18.0%… |
| R48 | Results | CI + n/N | Reweighting East Asia’s specialty mix to match North America and Western Europe raised its rate from 18.5% to 19.9%, compared with 35.1% for… |
| R49 | Results | CI + n/N | Within East Asia, rates were 31.6% in Hong Kong, 26.7% in Singapore, and 16.2% in China. |
| R52 | Results | CI + n/N | Critical rates were 53.9% for Commentaries, 42.1% for Letters, 38.4% for Editorials, 32.9% for Research Articles, and 24.9% for Reviews (Fig… |
| R53 | Results | CI + n/N | Pooling Commentaries, Letters, and Editorials, opinion formats were more critical than Research Articles (41.8% vs 32.9%). |
| R55 | Results | CI + n/N | Letters also had a larger neutral share of approximately 22%, compared with approximately 2–9% in most other formats. |
| R56 | Results | CI + n/N | Reviews were the most favourable format at 73.1%, followed by Research Articles at 61.5%, Editorials at 52.2%, Commentaries at 39.4%, and Le… |
| R57 | Results | CI | Systematic reviews were more critical than narrative reviews (29.3%, n=980 vs 23.9%, n=4,464; Multimedia Appendix 3, Table S11), while the l… |
| R63 | Results | CI + n/N | Of the 78 claims, two, both Tier 2, were borne out; 54 (69.2%) were partially borne out; eight were not borne out; and 14 were too early/unf… |
| C03 | Figure caption | CI + n/N | Bars show annual estimates with 95% percentile bootstrap CIs (1000 resamples, seed=42). |
| C05 | Figure caption | CI + n/N | Themes were multilabel, with one to three per paper, so prevalence does not sum to 100%. |
| C06 | Figure caption | CI + n/N | Lines show annual estimates; shaded bands show 95% percentile bootstrap CIs. |
| C11 | Figure caption | CI | Each bar sums to 100%. b) Annual generative-model exposure and confabulation rate in the full abstract-present critical corpus (n=4,747). |
| C15 | Figure caption | CI + n/N | Bars show category estimates with 95% percentile bootstrap CIs. b) Critical rate versus FDA-cleared AI/ML device count across the same 18 ca… |
| C24 | Figure caption | n/N | Error bars show 95% CIs. |

Other E12 items without CIs (not percentages): Spearman ρ values (A06, R12, R16, R19, R30, R31, R39–R41), differences in percentage points (A07, R06, R22–R24), the discourse:evaluative ratio (R17), κ values in the Abstract other than stance (A04), and the flag precision 0.80 (R60).

## 3. Ledger (abridged: ID, values, reproduced, 2021–2025 value)

| ID | value(s) | reproduced | 2021–2025 value |
|---|---|---|---|
| A02 |  | not a quantitative result (method/reference) |  |
| A03 | 97,492 eligible; 16,759 retained; 16,749 valid labels | Y (FAILED stance = 10) | stance set 2021–2025: 14,058 records |
| A04 | κ 0.51; quadratic κ 0.79 (0.72–0.84); κ 0.75; κ 0.84; κ 0.57 | Y for prefilter, stance, model type, failure mode (T1–T3); specialty κ not recomputed in Batch 1 (report file only) |  |
| A05 | Cautious Optimism 62.8%; critical 30.8% | Y | CO 62.9% (62.0–63.7) [8,836/14,058]; critical 30.5% (29.7–31.2) [4,283/14,058] |
| A06 | Advocacy 2.9%→0.6%, ρ −1.00; critical 25.4% (22.9–28.1)→32.6% (30.9–34.4) | Y | Advocacy 2.9% (1.9–4.0) [31/1063] → 1.1% (0.9–1.4) [66/5898], ρ=-1.00 (exact P=.017), OR/yr 0.793 (0.721–0.872), P=<.001; critical 25.4% (22.8–28.0) [270/1063] → 31.0% (29.8–32.3) [1828/5898], ρ=+0.80 (exact P=.133), OR/yr 1.077 (1.046–1.108), P=<.001 |
| A07 | +11.0, +30.9, −22.0 pp | Y | safety +5.7; errors +27.4; regulation -23.1 pp |
| A08 | n=2226; factual error 56%–90%; fabrication-involved ~21%–23% from 2023 | Partial: 2,226 and 56–90% (recomputed 56.3–90.2%) reproduce; gated fabrication-involved share is 15.8% in 2023, 23.4%, 20.6%, 21.7% in 2024–2026, so '21–23% from 2023 onward' does not hold for 2023 | gated n=1,775; factual error 56.3–90.2%; fabrication-involved 2023–2025: 15.8%, 23.4%, 20.6% |
| A09 | 51.3% Mental Health; 16.8% Cardiology; ρ −0.65, P=.004; US 34.5%; China 16.2% | Y | Mental Health 50.3% (45.7–55.2) [196/390]; Cardiology 16.1% (12.8–19.2) [87/542]; FDA ρ -0.608, P 0.007; US 34.2% (32.7–35.7) [1,226/3,586]; China 14.9% (13.2–16.6) [230/1,540] |
| A10 | Reviews critical 24.9%, favourable 73.1% | Y | critical 24.3% (23.1–25.5) [1,120/4,611]; favourable 73.6% (72.3–75.0) [3,395/4,611] |
| R01 | 97,492; 16,759; 8,899; 7,860 | Y |  |
| R02 | 16,749 valid; 10 unparseable | Y (10 FAILED) |  |
| R03 | 16,747; 2 dated 2020 | Y (2 dated 2020) | 14,058 dated 2021–2025; 2,689 dated 2026 |
| R04 | 30.8% critical; 916 Alarm; 4,245 Caution; 69.2% non-critical | Y | critical 30.5% (29.7–31.2) [4,283/14,058]; Alarm 5.3% (5.0–5.7) [749/14,058]; Caution 25.1% (24.4–25.9) [3,534/14,058] |
| R05 | CO 62.8% (n=10,514); Neutral 5.0% (n=837); Advocacy 1.4% (n=235) | Y | CO 62.9% (62.0–63.7) [8,836/14,058]; Neutral 5.1% (4.8–5.5) [721/14,058]; Advocacy 1.6% (1.4–1.8) [218/14,058] |
| R06 | 25.4% [22.9–28.1] (2021) → 32.6% [30.9–34.4] (2026); Δ 7.25 pp | Y | 25.4% (22.8–28.0) [270/1063] → 31.0% (29.8–32.3) [1828/5898]; Δ +5.59 pp; ρ=+0.80 (exact P=.133); OR/yr 1.077 (1.046–1.108), P=<.001 |
| R07 | v2 direction (Table S1) | Not re-checked in Batch 1 (v2 is a sensitivity analysis) |  |
| R09 | Alarm 2.7%→6.8% (2024)→6.2% (2026); Caution 22.7%→26.4% | Y | Alarm 2.7% (1.8–3.8) [29/1063] → 6.8% (6.1–7.8) [253/3700] (2024) → 5.7% (5.1–6.2) [335/5898], ρ=+0.80 (exact P=.133), OR/yr 1.202 (1.126–1.282), P=<.001; Caution 22.7% (20.3–25.2) [241/1063] → 25.3% (24.2–26.5) [1493/5898], ρ=+0.60 (exact P=.350), OR/yr 1.038 (1.007–1.070), P=.016 |
| R10 | CO 60.2%–65.3% each year | Y | 60.2–65.3% (2021–2025); ρ=-0.60 (exact P=.350); OR/yr 0.999 (0.973–1.027), P=.962 |
| R12 | Advocacy 2.9%→0.6%, ρ −1.00 | Y | 2.9% (1.9–4.0) [31/1063] → 1.1% (0.9–1.4) [66/5898]; ρ=-1.00 (exact P=.017); OR/yr 0.793 (0.721–0.872), P=<.001 |
| R13 | 17 Advocacy records in 2026; 5 drug discovery | 17 Y; '5 drug discovery' is a manual reading of Table S2, not recomputed | 2026 only (descriptive table) |
| R15 | 16,747 | Y | 14,058 |
| R16 | discourse 30.2%→37.8% (ρ +0.94); evaluative 14.6%→28.1% (ρ +0.77) | Y (points, ρ). Table S3 CIs are not reproducible: per-cell seed = 42 + hash((genre, year)) % 10000 uses Python's salted string hash | discourse 30.2% (26.8–33.7) [222/735] → 35.4% (33.7–37.1) [1016/2867], ρ=+0.90 (exact P=.083), OR/yr 1.061 (1.024–1.099), P=.001; evaluative 14.6% (10.9–18.3) [48/328] → 26.8% (25.1–28.4) [812/3031], ρ=+0.80 (exact P=.133), OR/yr 1.209 (1.147–1.274), P=<.001 |
| R17 | ratio 2.24 → 0.88 | Y | 2.24 (2021) → 0.95 (2025) [2,867/3,031] |
| R19 | keep rate ρ +1.00 | Y | 9.5% (8.9–10.0) [1064/11191] → 20.4% (20.0–20.9) [5899/28873]; ρ=+1.00 (exact P=.017); OR/yr 1.273 (1.256–1.291), P=<.001 |
| R20 | 5,161 critical records | Y | 4,283 (2021–2025) |
| R22 | +11.0 pp | Y | 59.3% (53.5–64.8) [160/270] → 64.9% (62.7–67.2) [1187/1828] (Δ +5.7 pp); ρ=+0.80 (exact P=.133); OR/yr 1.055 (1.002–1.111), P=.041 |
| R23 | +30.9 pp | Y | 23.7% (18.6–28.5) [64/270] → 51.1% (48.7–53.3) [934/1828] (Δ +27.4 pp); ρ=+0.80 (exact P=.133); OR/yr 1.367 (1.296–1.442), P=<.001 |
| R24 | regulation −22.0 pp; ethics/bias −8.1 pp (36.7%→28.6%) | Y | regulation 54.8% (49.1–60.7) [148/270] → 31.7% (29.6–34.0) [580/1828], ρ=-0.90 (exact P=.083); ethics 36.7% (30.9–42.8) [99/270] → 33.0% (30.8–35.2) [604/1828], ρ=-0.80 (exact P=.133), OR/yr 0.915 (0.869–0.963), P=<.001 |
| R26 | 5,159 of 5,161 parsed; 2 dropped | Y (5,159/5,161) |  |
| R27 | 4,747 abstract-present | Y (4,747) | 3,906 |
| R28 | 2,226 gated; factual error 56%–90% | Y (2,226; 56.3–90.2%) | 1,775; 56.3–90.2%; misclassification ρ=-0.50 (exact P=.450) |
| R29 | fabrication-involved 0% (2021) → ~21%–23% from 2023 | gated fabrication-involved share is 15.8% in 2023, 23.4%, 20.6%, 21.7% in 2024–2026, so '21–23% from 2023 onward' does not hold for 2023 | 0.0% (0.0–0.0) [0/56] → 20.6% (18.0–23.4) [182/883]; ρ=+0.90 (exact P=.083); OR/yr 1.347 (1.174–1.544), P=<.001 |
| R30 | generative share 5.3%→62.8% (ρ +0.94) | Y | 5.3% (2.8–8.2) [13/245] → 57.8% (55.5–60.0) [1015/1757]; ρ=+0.90 (exact P=.083); OR/yr 2.026 (1.893–2.168), P=<.001 |
| R31 | fabrication share ρ +0.94; 13.8% in 2026 | Y | 0.0% (0.0–0.0) [0/245] → 11.4% (10.0–13.0) [201/1757]; ρ=+0.90 (exact P=.083); OR/yr 1.552 (1.381–1.745), P=<.001 |
| R32 | 21.8%, 22.9%, 19.7%, 22.0% (2023–2026) | Y (21.8, 22.9, 19.7, 22.0) | 2023: 21.8% (15.9–27.6) [39/179], 2024: 22.9% (19.5–26.2) [140/612], 2025: 19.7% (17.3–22.0) [200/1015]; OR/yr 0.977 (0.839–1.136), P=.759 |
| R33 | 1,858 (39.1%) | Y (1,858; 39.1%) | 1,446/3,906 (37.0%) |
| R34 | κ=0.57 | Y (T3: 0.574) |  |
| R35 | 16,734 valid; 18 categories ≥30; 13 FAILED | Y | 14,048 valid; 10 FAILED |
| R37 | Mental Health 51.3% (46.8–55.5); Medical Informatics 44.9% (43.5–46.4); Nursing 43.0% (37.0–48.8) | Y | 50.3% (45.7–55.2) [196/390]; 45.2% (43.6–46.9) [1,674/3,701]; 41.4% (34.5–47.5) [94/227] |
| R38 | Cardiology 16.8% (14.1–19.8); Ophthalmology 18.4% (15.7–21.2); Oncology 19.7% (17.8–21.8) | Y | 16.1% (12.8–19.2) [87/542]; 18.5% (15.7–21.6) [124/669]; 18.7% (16.5–21.0) [227/1,211] |
| R39 | ρ −0.65, two-sided P=.004 | Y (-0.647, P=0.004) | ρ -0.608, P=0.007 |
| R40 | ρ −0.58, n=11, P=.062 | Y | ρ -0.579, P=0.062 |
| R41 | ρ −0.01 | Y (-0.011; generative share among abstract-present critical records) | ρ 0.009 |
| R43 | US 34.5% [33.0–36.0] n=4,222; China 16.2% [14.6–17.8] n=1,904 | Y | US 34.2% (32.7–35.7) [1,226/3,586]; China 14.9% (13.2–16.6) [230/1,540] |
| R44 | Netherlands 44.4%; Denmark ~42.6%; Australia ~42.5%; Ireland 41.1%; UK ~40.6% | Y | Netherlands 44.2% (38.4–50.0) [130/294]; Denmark 41.8% (32.7–51.0) [41/98]; Australia 43.8% (38.1–49.2) [155/354]; Ireland 41.4% (30.0–52.9) [29/70]; United Kingdom 40.0% (37.1–42.9) [420/1,049] |
| R45 | Japan 18.3%; Iran 18.0%; South Korea 20.5%; India 20.6% | Y | Japan 18.3% (14.7–22.6) [60/327]; Iran 17.6% (12.4–22.9) [30/170]; South Korea 19.5% (15.6–23.7) [75/384]; India 19.7% (15.9–23.9) [77/390] |
| R46 | NA 35.1% [33.9–36.4] n=4964; WEU 35.1% [33.6–36.5] n=4,298 | Partial: % and CIs reproduce; n does not (recomputed NA 35.1% (33.9–36.4) [1,743/4,961], WEU 35.1% (33.6–36.5) [1,506/4,296]) | NA 34.9% (33.5–36.3) [1,472/4,221]; WEU 34.5% (33.0–36.1) [1,274/3,693] |
| R47 | East Asia 18.5% [17.2–19.9] n=3,262 | Partial: % and CI reproduce; n does not (recomputed 18.5% (17.2–19.9) [604/3,260]; 3,262 appears in the older session2_summary.md with 19.5%) | 17.7% (16.3–19.3) [478/2,702] |
| R48 | 18.5%→19.9% vs 35.1%; 8% of gap | Y (EA 18.5% [n=3,256] → 19.9% [n=3,256]; NA+WEU 35.1% [n=9,253]; gap closed 8.3%) | EA 17.7% [n=2,700] → 19.1% [n=2,700]; NA+WEU 34.7% [n=7,910]; gap closed 8.2% |
| R49 | Hong Kong 31.6%; Singapore 26.7%; China 16.2% | Y | Hong Kong 30.1% (20.5–41.0) [25/83]; Singapore 27.0% (19.9–34.0) [38/141]; China 14.9% (13.2–16.6) [230/1,540] |
| R51 | RA 10,315; Reviews 5,444; Letters 480; Editorials 404; Commentaries 104 | Y | Research Article 8,556, Review 4,611, Letter 429, Editorial 364, Commentary 98 |
| R52 | Commentaries 53.9%; Letters 42.1%; Editorials 38.4%; RA 32.9%; Reviews 24.9% | Partial: Commentary critical = 56/104 = 53.85% → 53.8% (manuscript 53.9% = sum of rounded Alarm 8.7 + Caution 45.2); others Y | Commentary 56.1% (45.9–66.3) [55/98]; Letter 40.6% (36.1–45.5) [174/429]; Editorial 37.1% (32.1–42.0) [135/364]; Research Article 32.7% (31.6–33.7) [2,799/8,556]; Review 24.3% (23.1–25.5) [1,120/4,611] |
| R53 | opinion 41.8% vs RA 32.9% | Y | opinion 40.9% (37.7–44.1) [364/891]; RA 32.7% (31.6–33.7) [2,799/8,556] |
| R54 | N=11,303; χ²₄=430.5; P<.001; Cramér's V=0.195 | Y | N=9,447; χ²₄=376.059; V=0.200 |
| R55 | Letters neutral ~22%; 2%–9% other formats | Y (21.7%; others 2.0–9.4%) | Letters neutral 21.7% (17.7–25.4) [93/429] |
| R56 | favourable: Reviews 73.1%; RA 61.5%; Editorials 52.2%; Commentaries 39.4%; Letters 36.3% | Y (Letters 174/480 = 36.25% → 36.3% half-up) | Review 73.6% (72.3–75.0) [3,395/4,611]; Research Article 61.5% (60.5–62.6) [5,266/8,556]; Editorial 53.3% (48.4–58.5) [194/364]; Commentary 37.8% (28.6–48.0) [37/98]; Letter 37.8% (33.1–42.4) [162/429] |
| R57 | systematic 29.3% (n=980) vs narrative 23.9% (n=4,464) | Y | systematic 29.5% (26.2–32.7) [245/831]; narrative 23.1% (21.7–24.5) [875/3,780] |
| R58 | Commentary n=104 | Y | 98 |
| R59 | 92 Advocacy papers 2021–2023 with predictive flag | Y (counts recomputed: frozen 74 PMIDs / 78 claims; verdict × tier matrix = Table S13) | n/a (forward validation; window fixed by design) |
| R60 | 18 false positives; precision 0.80 | Y (counts recomputed: frozen 74 PMIDs / 78 claims; verdict × tier matrix = Table S13) | n/a (forward validation; window fixed by design) |
| R61 | 74 papers; 78 claims; Tier 1/2/3 = 7/36/35 | Y (counts recomputed: frozen 74 PMIDs / 78 claims; verdict × tier matrix = Table S13) | n/a (forward validation; window fixed by design) |
| R63 | 2 borne out; 54 (69.2%) partially; 8 not; 14 too early | Y (counts recomputed: frozen 74 PMIDs / 78 claims; verdict × tier matrix = Table S13) | n/a (forward validation; window fixed by design) |
| R64 | Tier 1: 5/7 not borne out; 0 borne out | Y (counts recomputed: frozen 74 PMIDs / 78 claims; verdict × tier matrix = Table S13) | n/a (forward validation; window fixed by design) |
| R65 | Tier 2: 23/36 partially | Y (counts recomputed: frozen 74 PMIDs / 78 claims; verdict × tier matrix = Table S13) | n/a (forward validation; window fixed by design) |
| R66 | Tier 3: 30/35 partially | Y (counts recomputed: frozen 74 PMIDs / 78 claims; verdict × tier matrix = Table S13) | n/a (forward validation; window fixed by design) |
| C02 | 16,747 of 16,749 | Y | 14,058 (2021–2025) |
| C03 | 1000 resamples, seed 42 | Y (method) |  |
| C04 | n=5161 critical | Y | 4,283 |
| C05 |  | not a quantitative result (method/reference) |  |
| C06 |  | not a quantitative result (method/reference) |  |
| C07 | *P<.05; **P<.01 by exact two-sided permutation | Partial: Figure 1a asterisks agree with exact permutation P (Neutral exact P=.033, Advocacy .003), but Table S1 lists scipy asymptotic P for every row except Advocacy (Alarm/Caution/critical .072 vs exact .103; Neutral .019 vs exact .033) | Asterisks removed in draft; exact P in caption (T4_figure_captions.md) |
| C09 | n=2226 | Y | 1,775 |
| C11 | n=4,747 | Y | 3,906 |
| C14 | 16,734 valid; 13 failed | Y | 14,048 |
| C15 |  | not a quantitative result (method/reference) |  |
| C16 | structural zeros plotted at 0.5 | Not checked (figure) |  |
| C19 | 36 countries ≥50 records | Y (36) | 32 countries |
| C20 |  | not a quantitative result (method/reference) |  |
| C23 | 16,747 | Y | 14,058 |
| C24 |  | not a quantitative result (method/reference) |  |
| C27 | 78 predictions; 74 papers | Y | n/a |

## 4. Numbers in the Discussion (editor: remove unless compared directly with published literature)

None of these numbers is compared numerically with a published estimate; the literature-citing sentences (D07, D08, D12, D13) carry citation numbers only, not data.

| ID | numbers | cites literature | sentence |
|---|---|---|---|
| D02 | 2.9%; 0.6%; −1.00 | no | The clearest change was the reduction of unqualified promotion: explicit Advocacy fell from 2.9% in 2021 to 0.6% in 2026 (Spearman ρ=−1.00), while qualified favourable framing remained the majority stance and explicit scrutiny increased only modestly. |
| D04 | 78 | no | The boldest early claims fared worst: five of seven Tier-1 superiority-or-replacement claims were not borne out and none were confirmed, and only two of 78 claims were decisively borne out. |
| D09 | −0.65; 0.004 | no | We found an inverse association between critical stance and mapped FDA device counts (Spearman ρ=−0.65, two-sided p=0.004). |
| D10 | 11 | no | The direction persisted after specialties with structural zeros were removed, but the reduced analysis was no longer statistically significant at n=11 (Multimedia Appendix 3, Table S6). |
| D11 | 12 | no | One legible reason is theme emphasis: reviews foreground governance and ethics, whereas primary research foregrounds concrete error and safety, and within reviews the more favourable narrative subtype outnumbers the more critical systematic subtype (Multimedia Appendix 3, Tables S11 and S12). |
| D14 | 0.79; 0.75; 0.84; 0.57; 0.51 | no | Agreement was substantial for stance (quadratic-weighted κ=0.79) and specialty (κ=0.75), almost perfect for model type (κ=0.84), and moderate for failure mode (κ=0.57) and the prefilter (κ=0.51). |
| D15 | 300 | no | It also read only the first 300 characters of each abstract, so a paper whose engagement with AI is stated only in its conclusion could be missed, which is consistent with the moderate prefilter agreement. |
| D17 | 1; 2 | no | The corpus was restricted to English-language, PubMed-indexed Q1/Q2 journals. |
