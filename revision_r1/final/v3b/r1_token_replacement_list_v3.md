# 正文小引用替换清单 v3（MA 最终编号）

编号规则：JMIR 首次引用顺序（Methods → Results → Discussion）。MA1 = Supplementary Notes，MA2 = Supplementary Tables，MA3 = Supplementary Figures（表先于图被引用，所以和投稿版相反）。

## A. 必须先处理的 4 件事（否则数字或编号会错）

1. **Results，Advocacy by specialty 一句：** “fell in 11 of the 18 specialty and domain categories” 改为 **“fell in 12 of the 18”**。这是我之前数错了：Surgery 是 1/56 = 1.79% → 9/512 = 1.76%，一位小数都显示 1.8%，我当成没变。精确比较是 12 个下降、4 个从 0 上升、2 个两年都是 0。（Table S25 可核对）

2. **Methods，Compute and Carbon Footprint：** “68.9 million tokens in the additional runs of this revision” 改为 **“81.4 million tokens”**。68.9M 只是 A2 的 input。三次修订 API 运行（committed 的 outputs/*/actual_cost.json）：A2 68,925,231 + 2,356,458；B2 2,637,329 + 68,429；B3 7,282,930 + 129,306；合计 81,399,683（input + output）。两个 [X]：若碳足迹指原分析 + 修订（124.5M + 81.4M = 205.9M），0.12 g/1000 tokens → **24.7 kg CO₂e**，0.45 g → **92.7 kg CO₂e**。若只算修订：9.8 / 36.6 kg。原来的 124.5M 是否含 output token 我查不到，请你按原稿口径确认。

3. **三个建议新增的引用**（编号是按“你加上”算的；不加的话告诉我，我删掉 Figure S5/S6 并重排）：
   - Methods → Quality of Measurements，“One author (LW) coded every validation sample, blind to the model labels and sampling strata.” 句末加 **(Multimedia Appendix 1, Note 9)**（验证 protocol 和 Amendments 1–3 都在 Note 9，目前全文没引用它）。
   - Results → 关键趋势段，“…from 31.0% to 28.6% in 2025 ([[MA:corpus_sensitivity]])” 改为 **(Multimedia Appendix 2, Table S20; Multimedia Appendix 3, Figure S5)**。
   - 同段，“…P=.106; [[MA:q3_arm]])” 改为 **P=.106; Multimedia Appendix 2, Table S22; Multimedia Appendix 3, Figure S6)**。

4. **Methods 里 [[MA:period_correction]] 和 Results/Discussion 里 [[MA:corrected_prevalence]] 是同一张表**（Table S11），两个都替换成 Table S11。

## B. 逐个替换（按正文首次出现顺序）

| 正文里的 token | 替换为 | 首次出现 |
|---|---|---|
| `[[MA:note_data_code]]` | Multimedia Appendix 1, Note 1 | Methods |
| `[[MA:sjr_sensitivity]]` | Multimedia Appendix 2, Table S1 | Methods |
| `[[MA:update_2026]]` | Multimedia Appendix 2, Table S2 | Methods |
| `[[MA:note_prefilter_prompt]]` | Multimedia Appendix 1, Note 2 | Methods |
| `[[MA:keep_rate]]` | Multimedia Appendix 2, Table S3 | Methods |
| `[[MA:precision]]` | Multimedia Appendix 2, Table S4 | Methods |
| `[[MA:note_stance_prompt_v1]]` | Multimedia Appendix 1, Note 3(a) | Methods |
| `[[MA:run_to_run]]` | Multimedia Appendix 2, Table S5 | Methods |
| `[[MA:note_endorsement_prompt]]` | Multimedia Appendix 1, Note 4 | Methods |
| `[[MA:note_stance_prompt_v2]]` | Multimedia Appendix 1, Note 3(b) | Methods |
| `[[MA:note_theme_prompt]]` | Multimedia Appendix 1, Note 5 | Methods |
| `[[MA:note_mechanism_prompt]]` | Multimedia Appendix 1, Note 6 | Methods |
| `[[MA:note_specialty_prompt]]` | Multimedia Appendix 1, Note 7 | Methods |
| `[[MA:specialty_definitions]]` | Multimedia Appendix 2, Table S6 | Methods |
| `[[MA:country_map_20]]` | Multimedia Appendix 3, Figure S1 | Methods |
| `[[MA:fda_mapping]]` | Multimedia Appendix 2, Table S7 | Methods |
| `[[MA:note_forward_validation]]` | Multimedia Appendix 1, Note 8 | Methods |
| `[[MA:forward_validation_sankey]]` | Multimedia Appendix 3, Figure S2 | Methods |
| `[[MA:fv_tier_verdict]]` | Multimedia Appendix 2, Table S8 | Methods |
| `[[MA:prefilter_validation]]` | Multimedia Appendix 2, Table S9 | Methods |
| `[[MA:stance_confusion]]` | Multimedia Appendix 2, Table S10 | Methods |
| `[[MA:note_correction_estimator]]` | Multimedia Appendix 1, Note 10 | Methods |
| `[[MA:period_correction]]` | Multimedia Appendix 2, Table S11 | Methods |
| `[[MA:theme_validation]]` | Multimedia Appendix 2, Table S12 | Methods |
| `[[MA:mechanism_confusion]]` | Multimedia Appendix 2, Table S13 | Methods |
| `[[MA:missing_data]]` | Multimedia Appendix 2, Table S14 | Methods |
| `[[MA:stance_trend]]` | Multimedia Appendix 2, Table S15 | Methods |
| `[[MA:themes]]` | Multimedia Appendix 2, Table S16 | Methods |
| `[[MA:regression_full]]` | Multimedia Appendix 2, Table S17 | Methods |
| `[[MA:fda_robustness]]` | Multimedia Appendix 2, Table S18 | Methods |
| `[[MA:ea_vs_nawe_within_specialty]]` | Multimedia Appendix 2, Table S19 | Methods |
| `[[MA:corpus_sensitivity]]` | Multimedia Appendix 2, Table S20 | Methods |
| `[[MA:symmetric_endorsement]]` | Multimedia Appendix 2, Table S21 | Methods |
| `[[MA:q3_arm]]` | Multimedia Appendix 2, Table S22 | Methods |
| `[[MA:within_genre]]` | Multimedia Appendix 2, Table S23 | Methods |
| `[[MA:note_mesh_keywords]]` | Multimedia Appendix 1, Note 11 | Methods |
| `[[MA:lexicon_vs_llm_fig]]` | Multimedia Appendix 3, Figure S3 | Methods |
| `[[MA:terms_fig]]` | Multimedia Appendix 3, Figure S4 | Methods |
| `[[MA:lexicon_and_terms]]` | Multimedia Appendix 2, Table S24 | Methods |
| `[[MA:corrected_prevalence]]` | Multimedia Appendix 2, Table S11 | Results |
| `[[MA:within_genre_fig]]` | Multimedia Appendix 3, Figure S7 | Results |
| `[[MA:advocacy_measures_fig]]` | Multimedia Appendix 3, Figure S8 | Results |
| `[[MA:advocacy_by_specialty]]` | Multimedia Appendix 2, Table S25 | Results |
| `[[MA:other_themes_fig]]` | Multimedia Appendix 3, Figure S9 | Results |
| `[[MA:theme_counts_fig]]` | Multimedia Appendix 3, Figure S10 | Results |
| `[[MA:lexicon_decomposition]]` | Multimedia Appendix 2, Table S26 | Results |
| `[[MA:generative_share_fig]]` | Multimedia Appendix 3, Figure S11 | Results |
| `[[MA:country]]` | Multimedia Appendix 2, Table S27 | Results |
| `[[MA:region]]` | Multimedia Appendix 2, Table S28 | Results |
| `[[MA:pubtype]]` | Multimedia Appendix 2, Table S29 | Results |
| `[[MA:review_subtypes]]` | Multimedia Appendix 2, Table S30 | Results |
| `[[MA:theme_by_format]]` | Multimedia Appendix 2, Table S31 | Results |

同一 token 在后文再出现时用同一编号。Note 3 有 (a) v1 和 (b) v2 两部分，所以 v1 写 Note 3(a)，v2 写 Note 3(b)。

## C. 正文 Figure 1–6 与 Table 1–3

- 首次引用顺序已核对：Figure 1、Table 1、Figure 2、Table 2（Methods），Table 3、Figure 3–6（Results），无需改号。
- **Figure 1 换图**：用 Fig1_v3.png/pdf。只改了图里 3 处 “R1”（“R1 analysis window” → “Analysis window”；“(R1 audit)” → “(prefilter audit)”；“Prefilter, R1 audit” → “Prefilter, audit”），数字和版式不变。Figure 2–6 图片没有内部代码，原样使用。
- **Table 1–3 用 v3 版本**（数字不变，见下方 D）。

## D. 我自己决定的小事（reviewer 没问，按规则直接做了）

- MA1 Notes 按首次引用重排：1 数据与代码、2 prefilter prompt、3 stance prompts、4 symmetric-endorsement prompt、5 theme、6 mechanism、7 specialty、8 forward-validation、9 验证 protocol、**10 新增：misclassification-corrected prevalence 的估计方法**、11 MeSH/keyword。Note 1 的文件对照表去掉了 A/B/T 代码（文件路径保留），补上 ANALYSIS_PLAN_batch2d.md 和 d1–d3 脚本。
- **Table S11（新）**：(a) 逐年校正患病率，constant-rate（预设，Results 用的就是这列）和 period-specific（post hoc）并排；(b) 按期 conversion rates + Fisher P；(c) 按期 Advocacy precision/recall。新增的 “All years” 列是从 Table S10 的 300 条混淆矩阵算的；脚本已断言它能把 T2 的 10 个 constant-rate 值精确复现到小数点后两位。
- **Table S26（新）**：lexicon 来源分解（CC 的 D2 表原样搬入，只清理脚注）。
- **Figure S8（新）**：三种 unqualified promotion 测量（Advocacy 标签、strong endorsement、constant-rate 校正值），数字全部来自 numbers book。
- **Figure S4 重画 + Table S24 增加 (e)(f) 两栏**：原图和原表只列“上升”的词，但 Results 写了 “machine learning and deep learning fell most” 和 “deep learning in favourable records”，原 MA 里没有支持数据。数据在 numbers book（RES-B6-EMERG/STANCE-31…60），现在图和表两个方向都列出。
- Figure S5 重画：只改标签（B2/B5/D1–D3 → 描述性名称），数据不变。
- 全部 MA 表注去掉 “Version 2 (Batch 2d)…”（换成一句 cluster-robust SE 说明）、“(unchanged)”、“R1”、B/A/T 代码、脚本和 csv 文件名、“submitted Table S16/S3”；narrative → non-systematic；SJR D1/D2/D3 → Medicine area / Medicine area without Medicine (miscellaneous) / Broad health sciences；回归表变量名 pubtype/country_g → publication type/country；一个 “nan%” 单元格 → “N/A, no records”；Table S12 主题代码前加显示名。
- Table S17：原来年份那一行把 adjusted OR 放在 “Cut-point ORs” 列下，拆成 unadjusted / adjusted 两行。Table S9：pilot 混淆矩阵补了一行列名（Discourse / Evaluative / Application / Row total），原来只有 Value 1–4。
- 正文 Table 1：删掉脚注 “The development pilot … CI could not be reproduced from the original code…”（改为中性的 CI 说明）；Table 2：删掉 “Version 2” 句和 “Not included: model type … FDA count …”；Table 3：列名和脚注去掉 B 代码。删掉的两条都放进回信。

## E. 只提醒，不改

- Discussion 的 Conclusions 你删了 guardrail 句；Principal Results 段末仍有 “These findings characterize published discourse, not AI capability…”，锁定要求仍满足。
- Results 的 Figure 5 图注写 “indexes publication discourse”，Discussion 写 “publication metadata”，要统一可以都用 metadata。
- MA1 Note 1 仍写仓库数据集 “n = 16,749”（那是 2021–2026 年 4 月的完整文件），下一段已说明分析用 14,058。
