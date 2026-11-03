**Multimedia Appendix 1. Supplementary Notes**

*Evaluative Stance Toward Artificial Intelligence in High-Quartile Medical Journal Abstracts, 2021-2025: Infoveillance Study*

Lixing Wang, Dan Poenaru

## Supplementary Note 1. Data and code availability

All prompts, classification code, mapping tables, PubMed identifiers, and committed analysis outputs supporting this study are available in the public repository:

**https://github.com/Lixing-Kingsley-Wang/ai-narratives-2026**

The analytic dataset, consisting of one row per record with its PubMed identifier and the assigned stance, theme, mechanism, specialty, and first-author region labels (n = 16,749), is included in the repository. Because hosted large-language-model behaviour drifts over time, the committed model outputs in the repository, rather than re-inference, are the basis for exact reproduction. Analyses were run in Python 3.12; package versions are pinned in requirements.txt.

The table below maps each Methods component to the file(s) that implement it, so any reported number can be located and re-run.

All analyses use the 14,058 records with a valid stance published 2021-2025; 2689 records published January-April 2026 are reported in one descriptive supplementary table only. Components added during peer review are in the repository's revision_r1/ directory and are listed in the second part of the table.

| Methods component | Repository file(s) | Contents |
|---|---|---|
| Corpus retrieval & quartile filtering | fetch_pubmed_medical.py; sjr_filter.py; input/sjr/sjr_2021…2026.csv | Verbatim PubMed query, monthly-window retrieval loop, English/date restrictions, PMID de-duplication, SCImago Q1/Q2 matching |
| Publication-type mapping (5 categories) | robustness.py | PubMed publication-type → 5-category collapse rules |
| Prefilter (isolating AI-engaged literature) | prefilter_batch.py; output/pilot_200.xlsx; output/pilot_200_full_haiku.csv | Verbatim prefilter prompt, KEEP/DROP parsing, and the 200-record human-vs-model pilot |
| Stance classification & validation | classify_stance.py (v1); classify_stance_batch.py (v2); compute_kappa.py; output/validation/*; output/comparison_v1_v2.md | Verbatim stance prompts and few-shot examples, human-coder instructions, κ at all sensitivity layers, v1→v2 comparison |
| Thematic classification | classify_themes_batch.py | Verbatim ten-theme codebook prompt and multilabel cap logic |
| Mechanism re-classification (failure mode / model type) | classify_q7_failuremode.py; output/analyses/q7_kappa_report_abstractonly.md; q7_validation_* | Verbatim mechanism prompt, calibration examples, both 4×4 confusion matrices, Cohen κ / Gwet AC1 |
| Specialty classification | analysis/classify_specialty.py; output/analyses/specialty_kappa_report.md; specialty_validation_* | 18-category specialty taxonomy prompt, 18×18 confusion matrix, κ |
| First-author geography (8 regions) | analysis/extract_geography.py | Country → 8-region table, alias table, ambiguity-resolution rules |
| FDA cleared-device mapping | output/external/fda_aiml_devices.csv; analysis/run_specialty_aiadoption.py | FDA AI/ML device list (1995–2025) and FDA-panel → specialty mapping, structural-zero list |
| Forward-validation  | prophecy_phase1_*.py; prophecy_phase2_*.py; output/analyses/prophecy/*; prophecy_panel_preregistration.md | Pre-registered protocol, frozen 74-paper/78-claim manifest, retrieval + adjudication, verdicts with cited evidence PMIDs |
| Statistics & robustness checks | robustness.py (bootstrap_ci); analysis/run_country_critical_map.py; analysis/revision_checks/*.py; output/revision_checks/* | Bootstrap CI method (n = 1000, seed 42) and the sensitivity analyses reported in Multimedia Appendix 2, Tables S3, S18, S23 and S29 and in Multimedia Appendix 3, Figure S7 |
| Shared helpers and statistics for the revised analyses | revision_r1/scripts/r1_common.py; r1_coding.py | Data loaders, percentile bootstrap (1000, seed 42), Cohen κ, Gwet AC1, κ_max, exact-permutation Spearman, logistic trend |
| Re-analyses of the original pipeline outputs | revision_r1/scripts/t1_*.py to t9_*.py; revision_r1/outputs/T1_* to T9_* | Prefilter pilot metrics, stance per-class metrics, mechanism confusion matrices, 2021-2025 temporal and cross-sectional re-analysis, missing-data accounting, SJR quartile audit, review-subtype rule, data inventory |
| Full-abstract prefilter reclassification | revision_r1/scripts/a2_prefilter_fullabstract_batch.py; revision_r1/outputs/A2/ | Copy of prefilter_batch.py with the full abstract and no failure default; diff committed |
| Validation protocol and coding instruments (theme validation, prefilter audit) | revision_r1/coding/PROTOCOL_r1_validation.md; revision_r1/scripts/a1_theme_sample.py, a3_prefilter_sample.py; revision_r1/coding/*_key.csv, *_manifest.csv | Frozen protocol (Note 9), sampling scripts, keys and manifests; coding workbooks hold no model labels |
| Validation scoring | revision_r1/scripts/a4_score_theme.py, a4_score_theme_n200.py, a4_score_prefilter.py, a4_score_prefilter_blankerror.py, a4_prefilter_exact_ci.py; revision_r1/outputs/A4_*, B1/ | Frozen scorers and amended primary analyses; Jeffreys and Clopper-Pearson intervals |
| Stance of recovered records | revision_r1/scripts/b2_stance_recovered_batch.py, b2_analysis.py, b_batch_engine.py; revision_r1/outputs/B2/ | v1 stance for records recovered by the full-abstract re-run; corpus sensitivity |
| Symmetric endorsement reclassification | revision_r1/scripts/b3_prompt.txt, b3_endorsement_batch.py, b3_analysis.py, b3_analysis_after_resubmit.py; revision_r1/outputs/B3/ | Strong-endorsement prompt (Note 4), labels and analysis |
| Multivariable regression | revision_r1/scripts/b4_prep_country.py, b4_regression.py; revision_r1/outputs/B4/ | Logistic, ordinal and sensitivity models with journal-clustered SEs |
| SJR medical-category sensitivity | revision_r1/scripts/t7_sjr_quartile.py, b5_sjr_medical_sensitivity.py; revision_r1/outputs/T7_*, B5/ | Category-level quartile re-match and three restricted corpora |
| MeSH and keyword triangulation | revision_r1/scripts/b6_fetch_mesh.py, b6_terms.py; revision_r1/outputs/B6/ | PubMed re-fetch (Note 11), lexicon trends, weighted log-odds term comparisons |
| Pre-specified analysis plans | revision_r1/ANALYSIS_PLAN_batch2b.md; revision_r1/ANALYSIS_PLAN_batch2d.md | Each committed before the analyses it describes were run |
| Numeric corrections | revision_r1/scripts/b7_corrections.py; revision_r1/outputs/B7_corrections.md | Old and corrected values for numbers changed during peer review |
| Numbers, figures, tables and appendices | revision_r1/final/scripts/c1_*.py to c5_*.py and d1_*.py to d7_*.py; revision_r1/final/v3/scripts/*.py; revision_r1/final/NUMBERS_BOOK_R1_v2.csv | Every reported number with its source; figure, table and appendix builders; journal cluster-robust trend ORs (d1), lexicon source decomposition (d2) and period-specific misclassification correction (d3) |

## Supplementary Note 2. AI-engagement prefilter prompt

## Reproduced verbatim as supplied to the classifier. No text has been edited.

You are classifying medical journal articles into one of three categories based on whether and how they engage with artificial intelligence (AI) as a subject.

CATEGORIES:

– discourse: AI/LLM is the MAIN SUBJECT of discussion. The paper reflects on, debates, or analyses AI’s role, safety, ethics, implications, governance, risks, or future in medicine. Includes editorials, perspectives, opinion pieces, and narrative reviews WHERE THE CENTRAL TOPIC IS AI ITSELF.

– evaluative: The paper TESTS or BENCHMARKS a specific AI system (especially LLMs like ChatGPT, GPT-4) and draws explicit conclusions about its accuracy, safety, reliability, limitations, or clinical readiness.

– application: The paper USES AI/ML as a technical tool to solve a clinical problem. AI is a method, not the subject. When in doubt, classify as application.

CRITICAL RULES:

– Only classify as discourse if AI/LLM is clearly the CENTRAL topic

– Only classify as evaluative if there is explicit testing of an AI system with clinical conclusions

– Everything else = application

Return ONLY valid JSON:

{"paper_type": "...", "type_confidence": "..."}

No preamble, no explanation.

User message template, as constructed by the classifier’s build_prompt function (variable slots marked with braces):

Classify this paper:

Title: {title}

Abstract: {abstract[:300]}

The Abstract line is included only when the record has a non-empty abstract; the abstract is truncated to its first 300 characters. The title is always sent in full and is never truncated.

Run configuration

– Model / model string: claude-haiku-4-5-20251001

– API mode: Batch (Anthropic Message Batches API)

– Temperature: not set in code (omitted from the request parameters); defaults to the provider default, T = 1.0

– max_tokens: 120

– System prompt: verbatim above

– Input fields sent to the model: title (full) + first 300 characters of the abstract; title only when the abstract is empty

– Retry / failure-handling rule: on a non-“succeeded” batch result, empty response text, or a JSON-parse failure, the record defaults to paper_type = “application”, type_confidence = “Low”; a returned paper_type outside {discourse, evaluative, application} is forced to “application”; a returned type_confidence outside {High, Medium, Low} is forced to “Medium”. No retries are attempted — each record is submitted once as part of the batch.

## Supplementary Note 3. Stance classification prompts

Two stance prompts exist in the repository. The canonical v1 prompt in (a) produced every stance label reported in the article. The stricter, conclusion-anchored v2 prompt in (b) was used only for the sensitivity analysis of the per-stance trends (Multimedia Appendix 2, Table S15). Both prompts are reproduced verbatim as supplied to the classifier; they were extracted programmatically from the source files (Python ast), and no text has been edited.

### (a) Canonical v1 prompt: produced every reported stance label

Source: classify_stance.py at commit 95fdc366121c282b1f9bd1e241c3f2cd58539eb6; SHA-256 of the prompt text b3949917159ea546ce7eb4c21224659be98c646aa937287d376f68c67992a39f (1833 characters). The production Batch API run used the identical prompt (classify_stance_batch.py at commit 9c79cd5; same SHA-256).

```
Classify the stance of a medical AI article toward AI/LLM technology.

STANCES (Q1/Q2 journals use measured language — calibrate accordingly):
- Alarm: primarily critical/skeptical. Emphasises dangers, failures, hallucinations, safety risks, ethical problems, or argues AI is not ready. Papers showing AI performs WORSE than clinicians = Alarm.
- Caution: acknowledges both promise AND significant concerns, balance tilts toward concern. Recommends safeguards before deployment.
- Neutral: purely descriptive. Reports metrics without taking a position. No evaluative language.
- Cautious Optimism: broadly positive with caveats. Supports careful deployment.
- Advocacy: strongly pro-AI. Emphasises transformative potential, minimal caveats.

PREDICTIVE CLAIM: explicit forward-looking claim about AI's future role (yes/no).

EXAMPLES:
"ENT specialists vs ChatGPT: 1-0" → {"stance":"Alarm","confidence":"High","predictive_claim":"yes"}
"ChatGPT fails safety standards for medication advice" → {"stance":"Alarm","confidence":"High","predictive_claim":"no"}
"Implications of LLMs for dental medicine" (balanced, concern-leaning) → {"stance":"Caution","confidence":"High","predictive_claim":"no"}
"AI in echocardiography: promising results, validation needed" → {"stance":"Cautious Optimism","confidence":"High","predictive_claim":"no"}
"AI will transform radiology within five years" → {"stance":"Advocacy","confidence":"High","predictive_claim":"yes"}
"Performance benchmarking of segmentation algorithm" → {"stance":"Neutral","confidence":"High","predictive_claim":"no"}

KEY RULES:
- AI performs worse than humans = Alarm, not Neutral
- AI risks/ethics/governance as main topic = Alarm or Caution, not Neutral
- Do NOT default to Cautious Optimism

Return ONLY valid JSON: {"stance":"...","confidence":"...","predictive_claim":"..."}
```

User message template, as constructed by the classifier's build_prompt function (variable slots marked with braces):

```
Title: {title}
Abstract: {abstract}
```

The Abstract line is included only when the record has a non-empty abstract; the full abstract is sent with no character truncation. The title is always sent in full.

**Run configuration**

- Model / model string: claude-sonnet-4-6
- API mode: Batch (Anthropic Message Batches API)
- Temperature: not set in code (omitted from the request parameters); provider default, T = 1.0
- max_tokens: 120
- System prompt: verbatim above (v1)
- Input fields sent to the model: title (full) + full abstract, no truncation; title only when the abstract is empty
- Output fields: stance, confidence, predictive_claim
- Retry / failure-handling rule: a non-'succeeded' batch result, empty response, JSON-parse failure, or a stance outside the five labels is recorded as FAILED; an invalid confidence is set to Medium and an invalid predictive_claim to no. No retries. FAILED: 10 of 16,759 retained records overall; 8 of the 14,066 records published 2021-2025.

### (b) v2 prompt: stricter rubric, sensitivity analysis only

Source: classify_stance_batch.py at commit 2559e6b6102830c2f608309f6820003213eb3f01; SHA-256 63761ee886a2de26f274b3148ca1886a69dd3ae52c26e7668467efd23315d254 (8164 characters). Its labels were not used for any primary estimate; they enter only the v2 column of the per-stance trend table (Multimedia Appendix 2, Table S15).

```
You are an expert classifier of academic medical literature. Your task is to classify the STANCE of medical journal articles toward AI/LLM technology in medicine. Read the title and abstract, then assign ONE of the following five stance labels.

=== STANCE DEFINITIONS ===

Alarm
  The paper is primarily CRITICAL or SKEPTICAL of AI. Emphasises dangers, failures, hallucinations, safety risks, ethical problems, or argues AI is not ready/safe for clinical use. Papers showing AI performs WORSE than clinicians = Alarm.
  Example: "ChatGPT fails safety standards for medication advice"

Caution
  Acknowledges both promise AND significant concerns, with the balance tilting toward concern. Recommends safeguards or further validation before deployment.
  Example: "Implications of LLMs for dental medicine" (mixed but concern-leaning)

Neutral
  The authors do not take a clear evaluative position on AI. Includes:
  - Methodology papers presenting algorithms/pipelines without endorsing AI broadly
  - Application papers using AI as a tool without evaluating AI itself
  - Bibliometric reviews, scoping reviews, workshop summaries, protocols
  - Performance benchmarks reporting metrics descriptively
  - Papers whose only positive/negative language appears in background framing

  Key diagnostic question: Do the authors themselves argue for or against AI's value in their conclusion? If they only describe, summarize, or report methodology without an evaluative interpretation, it is Neutral — even if the background contains positive framing.
  Example: "Performance benchmarking of segmentation algorithm"

Cautious Optimism
  BROADLY POSITIVE about AI with some caveats. Emphasises potential benefits, supports deployment with appropriate safeguards. May contain transformative-sounding language but ALSO acknowledges substantial caveats, limitations, or open challenges.
  Example: "AI in echocardiography: promising results, validation needed"

Advocacy
  STRONGLY and UNAMBIGUOUSLY pro-AI. Requires BOTH:
  (a) Transformative language (e.g., "revolutionize", "paradigm shift", "transform", "completely reinvent", "herald a new era") AND
  (b) Minimal or no acknowledged caveats.

  Strongly positive findings or endorsement language WITHOUT transformative claims are Cautious Optimism, not Advocacy. Transformative language WITH substantial caveats is also Cautious Optimism. Both conditions must hold for Advocacy.
  Example: "AI will revolutionise radiology within five years"

=== WHERE TO FIND THE AUTHORS' STANCE ===

Medical AI abstracts typically follow a structured pattern:
- BACKGROUND/OBJECTIVE/INTRODUCTION: sets up the topic. Often contains positive field-level framing ("AI is revolutionizing medicine", "transformative potential", "rapid advancements have shown promise"). This is the *convention* of the field, NOT the paper's stance. Do not classify based on background language alone.
- METHODS/RESULTS: describes what was done and found.
- CONCLUSION/DISCUSSION/FUTURE DIRECTIONS: where the authors interpret findings and take a position.

The stance you assign should reflect the authors' position as expressed in the CONCLUSION and DISCUSSION (typically the last 30-40% of the abstract). For evaluative studies, the stance comes from how the authors interpret their findings, not from background framing. For perspective/review papers, the stance comes from the explicit position the authors take at the end.

If the conclusion is descriptive, methodological, or scope-defining ("we present X", "we review Y", "this provides a framework for Z") and contains no explicit authorial evaluation of AI's value, classify as Neutral — regardless of how positive the background language is.

=== META-DISCOURSE / SURVEY PAPERS ===

Some papers measure attitudes, perceptions, knowledge, literacy, acceptance, or readiness toward AI among patients, students, clinicians, or other populations. These papers REPORT what surveyed populations think about AI; they do not themselves take a stance on AI.

For such papers:
- The findings of the survey (e.g., "70% of clinicians were positive about AI", "patients expressed concerns about data privacy") describe the population's views, NOT the authors' stance.
- The presence of words like "positive", "optimistic", "concerned", or "skeptical" in the conclusion typically describes the surveyed population.
- Classify these as Neutral by default and set meta_discourse to "yes".

Exception: If the authors editorialize in the conclusion or future-directions beyond reporting the findings — e.g., "These results urgently demand regulatory action" or "We strongly recommend immediate AI integration" — apply the rubric to that explicit authorial position (still set meta_discourse to "yes").

Common signals that a paper is meta-discourse:
- Title contains "perception", "attitude", "acceptance", "readiness", "literacy", "knowledge", "perspectives", "views"
- Methods describe a survey, questionnaire, interview, or cross-sectional attitudinal study
- Findings report what a sampled population thinks rather than what AI does

=== COMMON PITFALLS TO AVOID ===

1. BACKGROUND FRAMING: Sentences like "AI is revolutionizing medicine" or "transformative advances in AI" at the start of abstracts are field convention. They do NOT constitute the paper's stance.

2. WORD-LEVEL OVERREADING: A single occurrence of "transformative", "promising", or "revolutionary" in the background does not make a paper Advocacy or CO. The full abstract — especially the conclusion — must support the stance.

3. METHODOLOGICAL FEASIBILITY FINDINGS: Findings like "X was feasible" or "the algorithm achieved 80% accuracy" are descriptive results, not evaluative stances. Without the authors interpreting the feasibility as supporting deployment, these are Neutral, not CO.

4. ADVOCACY THRESHOLD: Strongly positive findings or measured endorsement language ("can outperform", "improves accuracy", "should be considered as adjunct") without transformative language are Cautious Optimism, not Advocacy. Advocacy requires both transformative claims AND minimal caveats — both conditions.

5. SURVEY FINDINGS ARE NOT AUTHORS' STANCE: When a paper measures attitudes, the surveyed population's views are NOT the authors' stance. The authors of an attitudinal survey are Neutral unless they editorialize beyond their findings.

=== KEY RULES ===

- Base classification only on title and abstract.
- If the paper tests AI and finds it performs WORSE than clinicians, code as Alarm.
- For papers showing AI better than clinicians, classify by the strength of the authors' interpretation: measured findings = CO; transformative framing + minimal caveats = Advocacy.
- Pick the stance that best reflects the OVERALL MESSAGE of the authors in their conclusion.

=== EXAMPLES ===

"ENT specialists vs ChatGPT: 1-0" → {"stance":"Alarm","confidence":"High","predictive_claim":"yes","meta_discourse":"no"}
"ChatGPT fails safety standards for medication advice" → {"stance":"Alarm","confidence":"High","predictive_claim":"no","meta_discourse":"no"}
"Implications of LLMs for dental medicine" (balanced, concern-leaning) → {"stance":"Caution","confidence":"High","predictive_claim":"no","meta_discourse":"no"}
"AI in echocardiography: promising results, validation needed" → {"stance":"Cautious Optimism","confidence":"High","predictive_claim":"no","meta_discourse":"no"}
"AI will transform radiology within five years" → {"stance":"Advocacy","confidence":"High","predictive_claim":"yes","meta_discourse":"no"}
"Performance benchmarking of segmentation algorithm" → {"stance":"Neutral","confidence":"High","predictive_claim":"no","meta_discourse":"no"}

=== OUTPUT FORMAT ===

Output field definitions:
- predictive_claim: explicit forward-looking claim about AI's future role (yes/no).
- meta_discourse: paper measures attitudes/perceptions/acceptance/literacy about AI in a population (yes/no). See META-DISCOURSE section above.

Respond ONLY with valid JSON in this exact format:
{"stance":"<Alarm|Caution|Neutral|Cautious Optimism|Advocacy>","confidence":"<High|Medium|Low>","predictive_claim":"<yes|no>","meta_discourse":"<yes|no>"}

```

User message template: identical to (a) (title + full abstract).

**Run configuration**

- Model / model string: claude-sonnet-4-6
- API mode: Batch (Anthropic Message Batches API)
- Temperature: not set in code; provider default, T = 1.0
- max_tokens: 120
- System prompt: verbatim above (v2)
- Input fields: title (full) + full abstract, no truncation
- Output fields: stance, confidence, predictive_claim, meta_discourse
- Failure handling: as (a); FAILED records are excluded from the v2 shares

## Supplementary Note 4. Symmetric-endorsement prompt (sensitivity analysis)

Source: revision_r1/scripts/b3_prompt.txt (commit f6f8c6defb692479bce91d6a91726705176a2fa3); SHA-256 27d28077cd7485fddcdfe4f0da3f4a3c13ad36a310bcd23f1544a5a89db50cf6, asserted at runtime by b3_endorsement_batch.py. Reproduced verbatim; no text has been edited. The prompt keeps the Advocacy endorsement criterion of the v1 rubric but drops its transformative-language requirement, so that the favourable end of the scale is defined symmetrically with the critical end.

```
You are classifying medical journal abstracts that discuss or evaluate artificial intelligence (AI). Every abstract you see has already been judged broadly favourable toward AI. Decide whether the authors' own conclusion is a STRONG ENDORSEMENT of AI.

STRONG ENDORSEMENT = "yes" when the authors' evaluative conclusion is strongly positive about AI's benefit, performance, or readiness for use, with minimal or no acknowledged caveats. The wording does not matter: transformative language such as "revolutionize" or "paradigm shift" is NOT required. A plainly worded report that AI matched or outperformed clinicians counts as "yes" if the conclusion endorses AI with minimal or no acknowledged caveats.

STRONG ENDORSEMENT = "no" when the conclusion acknowledges substantive caveats, limitations, risks, or open challenges (for example, the need for further validation before clinical use, human oversight, bias, specific failure modes, or limited generalizability), or when the abstract reaches no evaluative conclusion about AI.

Judge the authors' own evaluative commitment in their discussion and conclusion, not the sentiment of the background framing.

Return ONLY valid JSON: {"strong_endorsement": "yes"} or {"strong_endorsement": "no"}
```

User message template (the v1 input format): Title: {title} / Abstract: {abstract}, with the Abstract line only when the abstract is non-empty and no truncation.

**Run configuration**

- Model / model string: claude-sonnet-4-6
- API mode: Batch (Anthropic Message Batches API)
- Temperature: explicitly set to 0
- max_tokens: 30
- Records: every record with production stance Cautious Optimism or Advocacy dated 2021 to April 2026 (10,749)
- Output: {"strong_endorsement": "yes" | "no"}; any other output (including prose before the JSON) is FAILED
- Retry rule: FAILED records were resubmitted once with identical settings; 7 failed in round 1, 1 was recovered, 6 stayed FAILED and remain in all denominators, not counted as strong endorsement
- Cost gate: exact token count on a 1,000-record sample before submission (ceiling USD 25)

## Supplementary Note 5. Ten-theme codebook prompt

## Reproduced verbatim as supplied to the classifier. No text has been edited.

Identify concern themes in critical medical AI papers.

THEMES (return 1-3 most prominent):

– replacement: AI replacing physicians/clinicians/jobs; job displacement fears

– hallucination: AI errors, hallucinations, factual inaccuracies, unreliable outputs

– safety_clinical: patient safety risks, clinical harm, diagnostic errors

– ethics_bias: algorithmic bias, fairness, equity, ethical problems, discrimination

– cognitive: cognitive offloading, deskilling, over-reliance, loss of clinical skills

– education: medical education, student learning, training, residency, examinations

– regulation: governance, regulation, oversight, policy, liability, accountability

– existential: existential threat to medicine, disruption of doctor-patient relationship

– data_privacy: data privacy, security, consent, patient data misuse

– other: critical concern not fitting above

Return ONLY valid JSON:

{"themes": ["theme1", "theme2"]}

User message template, as constructed by the classifier’s build_prompt function (variable slots marked with braces):

Identify concern themes:

Title: {title}

Abstract: {abstract[:400]}

The Abstract line is included only when the record has a non-empty abstract; the abstract is truncated to its first 400 characters. The title is always sent in full. This classifier runs only on records whose stance is Alarm or Caution.

Run configuration

– Model / model string: claude-sonnet-4-6

– API mode: Batch (Anthropic Message Batches API)

– Temperature: not set in code (omitted from the request parameters); defaults to the provider default, T = 1.0

– max_tokens: 150

– System prompt: verbatim above

– Input fields sent to the model: title (full) + first 400 characters of the abstract; title only when the abstract is empty

– Retry / failure-handling rule: on a non-“succeeded” batch result, empty response text, or a JSON-parse failure, the record defaults to themes = [“other”]; any returned theme outside the ten-item vocabulary is dropped, and if no valid theme remains the record falls back to [“other”]; the retained list is capped at 3 themes (themes[:3]) even if more were returned. No retries are attempted — each record is submitted once as part of the batch.

## Supplementary Note 6. Mechanism (failure-mode × model-type) prompt

## Reproduced verbatim as supplied to the classifier. No text has been edited.

Classify an AI/medical paper on two independent axes from the MECHANISM described, not from brand names (GPT/ChatGPT/etc).

Axis A — failure_mode:

– “confabulation”: AI GENERATES fabricated/unfaithful content — invented citations or references, made-up facts, plausible-but-false text, hallucinated entities, unfaithful summaries.

– “misclassification”: AI produces a wrong label/score/prediction/detection — false positives/negatives, misdiagnosis, miscalibration, poor generalization, dataset shift, biased predictions.

– “both”: both mechanisms explicitly described.

– “none_or_unclear”: no specific mechanism, or general “AI risks” framing.

Axis B — model_type:

– “generative”: LLM, chatbot, text/image/code generator.

– “discriminative”: predictive / classification / detection / segmentation / risk-scoring model.

– “both”: both families explicitly evaluated.

– “unclear”: cannot tell.

CALIBRATION EXAMPLES:

1. "ChatGPT scored 85% on USMLE-style questions"  →

{"failure_mode":"misclassification","model_type":"generative","confidence":0.9,"rationale":"accuracy of LLM responses, not fabrication"}

2. "DL classifier produced false-negative mammograms"  →

{"failure_mode":"misclassification","model_type":"discriminative","confidence":0.95,"rationale":"predictive model with classification errors"}

3. "LLM discharge summary fabricated a drug and an invented citation"  →

{"failure_mode":"confabulation","model_type":"generative","confidence":0.95,"rationale":"explicit fabrication of content and references"}

4. "Measured GPT-4 hallucinated references AND diagnostic accuracy"  →

{"failure_mode":"both","model_type":"generative","confidence":0.9,"rationale":"both fabrication and accuracy measured"}

5. "AI errors threaten safety, need oversight" (no mechanism)  →

{"failure_mode":"none_or_unclear","model_type":"unclear","confidence":0.6,"rationale":"general risk framing, no mechanism specified"}

Output STRICT JSON only, no prose, no code fences:

{"failure_mode":"confabulation|misclassification|both|none_or_unclear","model_type":"generative|discriminative|both|unclear","confidence":0.0-1.0,"rationale":"<=20 words"}

User message template, as constructed by the classifier’s build_prompt function (variable slots marked with braces; no truncation applied):

Title: {title}

Abstract: {abstract}

The Abstract line is included only when the record has a non-empty abstract; the full abstract is sent with no character truncation. This classifier runs on the two phases specified in classify_q7_failuremode.py: all stance == Alarm records and all stance == Caution records (pub_year restricted to 2021–2026), producing q7_classified_alarm.csv and q7_classified_cautious.csv respectively.

Run configuration

– Model / model string: claude-sonnet-4-6

– API mode: synchronous (AsyncAnthropic client.messages.create calls under an asyncio.Semaphore, concurrency = 5) — not the Batch API

– Temperature: explicitly set in code: TEMPERATURE = 0.0

– max_tokens: 200

– System prompt: verbatim above

– Input fields sent to the model: title (full) + full abstract, no truncation; title only when the abstract is empty

– Retry / failure-handling rule: up to 3 attempts per record (MAX_RETRIES = 3), with a 12-second base retry delay that scales with attempt number for non-JSON/validation exceptions (SLEEP_RETRY × attempt); on final failure both failure_mode and model_type are recorded as the literal string “FAILED” with confidence 0.0. A response whose failure_mode or model_type falls outside the four-value vocabulary for that axis raises a ValueError and is retried.

## Supplementary Note 7. Specialty classification prompt

## Reproduced verbatim as supplied to the classifier. No text has been edited.

You are classifying medical research papers by clinical specialty.

Read the title and abstract, then assign ONE of the following 18 categories:

1. Radiology / Diagnostic Imaging

2. Pathology / Laboratory Medicine

3. Cardiology

4. Oncology

5. Surgery (general and surgical subspecialties — orthopedic, ENT/otolaryngology, urology, neurosurgery, plastic, etc.)

6. Ophthalmology

7. Dermatology

8. Neurology / Neuroscience (non-surgical)

9. Mental Health / Psychiatry

10. Internal Medicine / Primary Care / Family Medicine (includes gastroenterology, endocrinology, rheumatology, nephrology, pulmonology, infectious disease — all non-surgical internal subspecialties)

11. Emergency Medicine / Critical Care

12. Pediatrics

13. Obstetrics / Gynecology

14. Dentistry

15. Medical Informatics / Digital Health / AI Methodology

16. Nursing

17. Medical Education

18. Multidisciplinary / Other

CLASSIFICATION RULES:

– Single best-fit by dominant specialty. Classify by the clinical specialty being applied to or studied, not by the AI methodology used.

– “ChatGPT for cardiology questions” → Cardiology, not Medical Informatics.

– “Deep learning for chest X-ray classification” → Radiology.

– “Survey of medical students’ AI literacy” → Medical Education.

– Medical Informatics (#15) is reserved for papers ABOUT AI itself — frameworks, taxonomies, methodology development, benchmarks not tied to a specific clinical specialty, or general “AI in medicine” overviews that don’t focus on one clinical domain.

– Multidisciplinary / Other (#18) is for:

– Papers spanning 2+ specialties with no dominant focus

– Bibliometric reviews across medicine

– Veterinary medicine

– Rehabilitation medicine, anesthesiology when not clearly fitting elsewhere

– Public health when not clearly Internal Medicine

– Any paper genuinely cross-cutting without a clinical anchor

– Pediatrics (#12) takes priority over organ system. “AI for pediatric cardiology” → Pediatrics.

– Oncology (#4) takes priority over organ system EXCEPT when the paper is about a single non-cancer aspect of that organ system. “AI for breast cancer detection” → Oncology. “AI for breast lesion characterization (benign and malignant)” → Radiology if imaging-focused.

– Surgical subspecialties all fold into Surgery (#5). Don’t split out orthopedics, ENT, urology, plastic surgery as separate.

OUTPUT FORMAT:

Respond ONLY with valid JSON. Use the SHORT category name (everything before the first parenthetical) exactly as shown:

– “Radiology / Diagnostic Imaging”

– “Pathology / Laboratory Medicine”

– “Cardiology”

– “Oncology”

– “Surgery”

– “Ophthalmology”

– “Dermatology”

– “Neurology / Neuroscience”

– “Mental Health / Psychiatry”

– “Internal Medicine / Primary Care”

– “Emergency Medicine / Critical Care”

– “Pediatrics”

– “Obstetrics / Gynecology”

– “Dentistry”

– “Medical Informatics / Digital Health”

– “Nursing”

– “Medical Education”

– “Multidisciplinary / Other”

Format:

{"specialty": "<short name>", "confidence": "<low|medium|high>"}

Respond with the JSON object and NOTHING ELSE. No code fences, no rationale, no preamble. Just the JSON.

User message template, as constructed by the classifier’s build_prompt function (variable slots marked with braces; no truncation applied):

Title: {title}

Abstract: {abstract}

The Abstract line is included only when the record has a non-empty abstract; the full abstract is sent with no character truncation. The title is always sent in full.

Run configuration

– Model / model string: claude-haiku-4-5 — note: this is a different API model string than the dated alias claude-haiku-4-5-20251001 used by the prefilter step (§ Note 2); both nominally refer to Haiku 4.5

– API mode: Batch (Anthropic Message Batches API)

– Temperature: not stated in the manuscript; not set in code (omitted from the request parameters) — defaults to the provider default, T = 1.0

– max_tokens: 80

– System prompt: verbatim above

– Input fields sent to the model: title (full) + full abstract, no truncation; title only when the abstract is empty

– Retry / failure-handling rule: on a non-“succeeded” batch result, empty response text, no JSON object found in the response, a JSON-parse failure, or a returned specialty outside the 18-category vocabulary, the record is recorded as specialty = “FAILED”, confidence = “low”; a returned confidence outside {low, medium, high} is forced to “medium”. No retries are attempted — each record is submitted once as part of the batch.

## Supplementary Note 8. Forward-validation prompts

## Reproduced verbatim as supplied to the classifier. No text has been edited.

(a) Phase 1 — claim extraction, flag validation, and tier assignment

You are adjudicating, for a PRE-REGISTERED forward-validation study, the predictive content of a 2021-2023 medical-AI paper. You are given ONLY that paper’s own title and (sometimes) abstract.

ABSOLUTE BLINDNESS RULE — read carefully:

– Use ONLY the paper’s own text shown to you. Judge the claim purely on what THIS 2021-2023 paper says.

– Do NOT use any knowledge of what happened after 2023. Do NOT let any belief about whether the prediction “came true” influence the flag, the signature claim, or the tier.

– Tier is a function of the CLAIM’S STRUCTURE, never of its real-world outcome.

Your job has five parts.

1) VALIDATE THE PREDICTIVE-CLAIM FLAG.

Does the text contain a SPECIFIC, FORWARD-LOOKING claim about AI’s future role (a prediction/bet about what AI will do, become, replace, enable, or transform)?

– flag_confirmed = “yes” only if a specific forward-looking claim is present.

– flag_confirmed = “no” for purely descriptive/retrospective work, a bland descriptive title with no forward claim, or vague aspiration with no claim content.

– For TITLE-ONLY records (no abstract), judge from the title alone. A descriptive title with no forward claim => “no”.

– flag_reason: one short line justifying yes/no, quoting/pointing to the forward-looking language (or noting its absence).

2) EXTRACT THE SIGNATURE CLAIM.

The single MOST SPECIFIC, MOST FALSIFIABLE prediction the paper makes, as one verbatim-or-close sentence.

– If flag_confirmed = “no”, set signature_claim = “” (empty).

– If the paper makes TWO genuinely independent major predictions, put the primary in signature_claim and the secondary in signature_claim_2. Most papers leave signature_claim_2 = “”.

3) ASSIGN TIER by claim STRUCTURE (frozen definitions):

– Tier 1 — Specific superiority / replacement: a testable head-to-head or displacement claim (AI will outperform / replace clinicians, or has done so in a way predicted to generalize). Highest falsifiability.

– Tier 2 — Capability deployment: a concrete mechanism entering clinical use / drug development / workflow (will be deployed, adopted, embedded, accelerate a pipeline). Medium falsifiability.

– Tier 3 — Diffuse transformation: “revolutionize / paradigm shift / next frontier” with NO mechanism and NO horizon. Lowest falsifiability.

TIE-BREAKERS (apply in order):

– If a claim has ANY concrete, testable element, it is NOT Tier 3.

– If it names a comparison/benchmark against humans, it is Tier 1.

– If flag_confirmed = “no”, set tier = “”.

4) TOPIC: a short free-text specialty/theme tag (e.g. “dermatology imaging”, “drug discovery”, “clinical NLP”). Secondary attribute only.

5) HORIZON: any explicit timeframe stated in the claim (“by 2025”, “within five years”, “next decade”). If none is stated, output “open-ended”.

Return ONLY a JSON object, no prose, no markdown fences, with EXACTLY these keys:

{"flag_confirmed":"yes|no","flag_reason":"...","signature_claim":"...","signature_claim_2":"...","tier":"1|2|3 or empty string","topic":"...","horizon":"..."}

User message template, as constructed by the classifier’s build_user_msg function (variable slots marked with braces). When the record has a non-empty abstract:

TITLE:

{title}

ABSTRACT:

{abstract}

Return the JSON object now.

When the record has no abstract (title-only record):

TITLE-ONLY RECORD (no abstract available). Judge from the title alone.

TITLE:

{title}

Return the JSON object now.

No character truncation is applied to either the title or the abstract.

Run configuration

– Model / model string: claude-sonnet-4-6

– API mode: synchronous (AsyncAnthropic client.messages.create calls under an asyncio.Semaphore, concurrency = 5) — not the Batch API

– Temperature: explicitly set in code: TEMPERATURE = 0.0

– max_tokens: 700

– System prompt: verbatim above

– Input fields sent to the model: title (full) + full abstract when available, no truncation; a title-only template variant is used when no abstract is available (see above)

– Retry / failure-handling rule: up to 3 attempts per record (MAX_RETRIES = 3), with a retry delay of 12 seconds × attempt number (SLEEP_RETRY × attempt); a response whose flag_confirmed is outside {yes, no}, or whose tier (after stripping a leading “Tier” prefix) is outside {1, 2, 3, empty string}, raises an exception and is retried. On final failure, flag_confirmed, flag_reason, signature_claim, signature_claim_2, tier, topic, and horizon are all written as blank, with the error message recorded in flag_reason.

(b) Phase 2 — neutral evidence-status summarization

You are given a prediction made in 2021-2023 and a set of 2024-2026 medical-literature abstracts retrieved as potentially relevant. Summarize, in 2-4 sentences, what these abstracts indicate about the real-world status of the prediction as of the evidence cutoff (April 2026).

Rules:

(a) Use ONLY the provided abstracts; do not use any outside or post-training knowledge.

(b) Do NOT state whether the prediction was right or wrong, and do NOT assign any verdict.

(c) Distinguish OUTCOME evidence (a study reporting what actually happened - a deployment, a validation, a head-to-head result, a workforce/market fact) from MERE RESTATEMENT (a later paper simply repeating the same prediction or advocacy). Continued advocacy is NOT evidence the prediction came true; note it as restatement, not outcome.

(d) If the abstracts do not actually address the prediction’s real-world status, state that the retrieved corpus does not speak to it.

(e) List the up-to-5 most relevant abstracts, each tagged [outcome] or [restatement]. Cite only abstracts that genuinely bear on the prediction.

Return ONLY a JSON object, no markdown fences:

{"status_summary":"2-4 sentence neutral summary","corpus_silent":true|false,"key_evidence":[{"pmid":"...","finding":"one-line finding","tag":"outcome|restatement"}]}

corpus_silent = true if the retrieved abstracts do not genuinely address the prediction’s real-world status. key_evidence may be empty if nothing genuinely bears on the prediction.

User message template, as constructed by the classifier’s build_user_msg function (variable slots marked with braces):

PREDICTION (made 2021-2023):

{claim}

RETRIEVED 2024-2026 ABSTRACTS ({len(abstracts)}):

[PMID {pid} | {year}] {title}

{abstract[:2200]}

... (repeated for each retrieved abstract, blocks joined by a blank line)

Return the JSON object now.

Each abstract is truncated to its first 2,200 characters (ABS_TRIM); title and publication year are taken from the corpus record and are not truncated. Up to 20 retrieved abstracts per claim are passed — the top 20 by retrieval score from the MedCPT retrieval step (phase2_retrieval.csv).

Run configuration

– Model / model string: claude-sonnet-4-6

– API mode: synchronous (AsyncAnthropic client.messages.create calls under an asyncio.Semaphore, concurrency = 5) — not the Batch API

– Temperature: explicitly set in code: TEMPERATURE = 0.0

– max_tokens: 1100

– System prompt: verbatim above

– Input fields sent to the model: the frozen claim’s signature_claim text, plus up to 20 retrieved 2024–2026 abstracts (title and publication year in full; abstract truncated to the first 2,200 characters)

– Retry / failure-handling rule: up to 3 attempts per claim (MAX_RETRIES = 3), with a retry delay of 12 seconds × attempt number (SLEEP_RETRY × attempt); on final failure evidence_status_summary is recorded as the error message, model_corpus_silent = False, and key_evidence is left empty. Independently of the model’s own corpus_silent judgement, the output worksheet also flags a claim corpus_silent if its retrieval top_score falls below the 10th percentile (SILENCE_PCTILE) of all claims’ top_scores.

Notes 3–7 above were extracted verbatim from the referenced files at https://github.com/Lixing-Kingsley-Wang/ai-narratives-2026.



## Supplementary Note 9. Validation protocol for the concern-theme classifier and the prefilter audit

Design. Two human-coding validations followed a written protocol frozen before coding: the concern-theme classifier and the AI-engagement prefilter audit, the latter preceded by a full-abstract reclassification of all eligible records by the prefilter. One author (L.W.) coded both samples. Coding workbooks showed only a row ID, the title and the full abstract; PMID, year, journal, stance, model labels and sampling stratum were kept in separate key files, never in the workbook. Each codebook is the classifier's own system prompt, extracted programmatically, with only the machine output-format line omitted.

- Theme validation: 200 critical records 2021-2025, 40 per year by simple random sampling within year (numpy default_rng(42)); frame 4283. Estimands: per-theme precision, recall and F1; micro- and macro-F1, exact match, Hamming loss and Jaccard, unweighted and weighted to the frame; bootstrap CIs within year (1000, seed 42).
- Full-abstract reclassification: all 97,492 eligible Q1/Q2 records re-classified with the identical prefilter prompt, model and settings but the full abstract and no failure default (FAILED, resubmitted once); 0 FAILED.
- Prefilter audit: 370 records, stratified by prefilter outcome x year 2021-2025 (excluded by production but kept by the full-abstract re-run, 15 per year; excluded by both, 45 per year; retained, 10 per year) plus 20 pilot records recoded for intra-rater agreement. Estimands: false-negative rate among excluded records (1-NPV) by year and pooled, the estimated number of missed AI-engaged records, PPV among retained records, a population-weighted 2x2 for the production and full-abstract classifiers (sensitivity, specificity, PPV, NPV, Cohen κ, Gwet AC1), a logistic test of year, and intra-rater agreement; weights = frame size / sample size per stratum-year cell; borderline-coded records analysed both ways as sensitivity analyses.

Freeze commits. Freeze 1 (0d21f6c 2026-10-23): protocol, sampling and re-run scripts, theme-validation key, manifest and workbook, committed before the theme-validation workbook was released. Freeze 2 (47cf6fe 2026-10-23): prefilter-audit key, manifest and workbook, generated after the full-abstract reclassification by the unchanged Freeze-1 script and committed before the prefilter-audit workbook was released.

**Amendments (all disclosed in the protocol's change log)**

| Amendment | Change | Timing | Effect on the estimates |
|---|---|---|---|
| 1 (themes) | Primary analysis uses all 200 sampled records; a record with no human theme counts as an empty set (every model theme on it is a false positive). The pre-specified rule (exclude such records; N=187) becomes secondary. | Made after the coded sheet was returned and after the pre-specified analysis had been run. | Conservative: micro-F1 0.919 (95% CI 0.897-0.940) (N=187) -> 0.885 (95% CI 0.855-0.914) (N=200). |
| 2 (prefilter audit) | An unlabelled audit row counts as an error of the classifier being evaluated (1 of 370 rows); the pre-specified rule (exclude) becomes secondary. | Decided when the sheet was returned, before any audit result was computed. | Negligible: pooled 1-NPV 5.2% in both analyses; estimated missed records 3747 vs 3740; production sensitivity 78.5% vs 78.6%; full-abstract precision 80.4% vs 81.2%. |
| 3 (prefilter audit) | Adds Jeffreys intervals for weighted combinations of cells and Clopper-Pearson intervals for single cells, because five cells have no variation and the within-cell bootstrap cannot vary them; the bootstrap is kept alongside. | Made after the primary audit results were known. | CIs only; point estimates unchanged. 25 of 29 intervals widen (all 1-NPV, missed-record and production-prefilter intervals); pooled 1-NPV 5.2% (95% CI 4.1%-8.9%). Not used for the full-abstract 2x2 (sub-cells too small). |

**Verbatim 'Read me first' sheet: theme-validation workbook (revision_r1/coding/theme_validation_TEMPLATE.xlsx)**

```
Theme validation — coding instructions

1. Task
Every paper on the Coding tab was classified as critical toward AI (Alarm or Caution). Read the title and the full abstract. Tick the 1 to 3 most prominent concern themes.

2. Theme list (verbatim from the classifier's SYSTEM_PROMPT)
Source: classify_themes_batch.py, commit 9c79cd5d0f5b0b3a364866ec57f9edf0f17998b2; SHA-256 of the full SYSTEM_PROMPT: b1bf54eddab15ab05418d5a2eb52de425047d87998bed1dd34abc837448f9584

Identify concern themes in critical medical AI papers.

THEMES (return 1-3 most prominent):
- replacement: AI replacing physicians/clinicians/jobs; job displacement fears
- hallucination: AI errors, hallucinations, factual inaccuracies, unreliable outputs
- safety_clinical: patient safety risks, clinical harm, diagnostic errors
- ethics_bias: algorithmic bias, fairness, equity, ethical problems, discrimination
- cognitive: cognitive offloading, deskilling, over-reliance, loss of clinical skills
- education: medical education, student learning, training, residency, examinations
- regulation: governance, regulation, oversight, policy, liability, accountability
- existential: existential threat to medicine, disruption of doctor-patient relationship
- data_privacy: data privacy, security, consent, patient data misuse
- other: critical concern not fitting above

3. How to fill the sheet
• Tick a theme by typing 1 in its column; leave other theme cells blank.
• Tick at least 1 and at most 3 themes. The n_themes cell turns red unless the count is 1, 2 or 3.
• Use 'other' only when no listed theme fits.
• Code each paper independently, and do not look papers up.
• Write any ambiguity in 'notes' rather than inventing a rule.
• Save the finished file as theme_validation_COMPLETED.xlsx (do not overwrite the template).

4. Note
The classifier saw only the title and the first 400 characters of the abstract; you read the full abstract. This is intended.
```

**Verbatim 'Read me first' sheet: prefilter-audit workbook (revision_r1/coding/prefilter_audit_TEMPLATE.xlsx)**

```
Prefilter audit — coding instructions

1. Categories and rules (verbatim from the production prefilter's SYSTEM_PROMPT)
Source: prefilter_batch.py, commit 9c79cd5d0f5b0b3a364866ec57f9edf0f17998b2; SHA-256 of the full SYSTEM_PROMPT: 3fdfbbadbd5aeac5b49cb22ae53f4b51e96cb41c1c4f566eccf65dc7bd2071f4

You are classifying medical journal articles into one of three categories based on whether and how they engage with artificial intelligence (AI) as a subject.

CATEGORIES:

- discourse: AI/LLM is the MAIN SUBJECT of discussion. The paper reflects on, debates, or analyses AI's role, safety, ethics, implications, governance, risks, or future in medicine. Includes editorials, perspectives, opinion pieces, and narrative reviews WHERE THE CENTRAL TOPIC IS AI ITSELF.

- evaluative: The paper TESTS or BENCHMARKS a specific AI system (especially LLMs like ChatGPT, GPT-4) and draws explicit conclusions about its accuracy, safety, reliability, limitations, or clinical readiness.

- application: The paper USES AI/ML as a technical tool to solve a clinical problem. AI is a method, not the subject. When in doubt, classify as application.

CRITICAL RULES:
- Only classify as discourse if AI/LLM is clearly the CENTRAL topic
- Only classify as evaluative if there is explicit testing of an AI system with clinical conclusions
- Everything else = application

2. How to fill the sheet
• Read the title and the full abstract.
• Choose human_label from the drop-down: discourse, evaluative, or application.
• Code each paper independently, and do not look papers up.
• Use 'borderline' (Y) and 'notes' for uncertainty: mark Y when you were torn, or when you applied the "when in doubt" rule.
• Save the finished file as prefilter_audit_COMPLETED.xlsx (do not overwrite the template).

3. Note
The production classifier saw only the title and the first 300 characters of the abstract; you read the full abstract. This is intended.
```

## Supplementary Note 10. Misclassification-corrected prevalence

Purpose. Advocacy is rare, and every in-scope disagreement between the stance classifier and the human coder that involved Advocacy was with Cautious Optimism (Multimedia Appendix 2, Table S10). The correction estimates, for each year, the share of records that the human coder would have assigned to a target label: Advocacy, or critical (Alarm or Caution).

Estimator. For year y and target label h, corrected prevalence = Σ_c s_y(c) × p(h | c), where c runs over the five model stance labels, s_y(c) is the share of year-y records in the 14,058-record analytic corpus with model label c, and p(h | c) is the share of stance-validation records with model label c that the coder assigned to h. Because the validation sample was stratified by model stance (Alarm 40, Caution 60, Neutral 70, Cautious Optimism 100, Advocacy 30), p(h | c) is estimated within each stratum. Records the coder judged not codable or out of scope count as human Neutral, as in panel (b) of Multimedia Appendix 2, Table S10.

Prespecified version (constant rates). p(h | c) is estimated from all 300 validation records and applied to every year, which assumes that the rates at which model labels convert to human labels did not change over 2021-2025. All records were classified with the same prompt and settings, each in an independent request. 95% CIs come from 1000 bootstrap draws (seed 42) that resample validation records within model-label strata and corpus records jointly. These are the estimates reported in the Results. Code: revision_r1/scripts/t2_stance_perclass.py.

Post hoc version (period-specific rates). Because the validation sample was not stratified by year, p(h | c) was also estimated separately from the validation records published 2021-2023 and 2024-2025 (253 records; 46 dated 2026 and 1 dated 2020 were excluded) and applied to the years of the same period. 95% CIs come from 1000 bootstrap draws (seed 42) that resample validation records within model label and period and corpus records jointly, with a Jeffreys Beta(k+1/2, n-k+1/2) draw for cells with no or all events. Period differences in p(h | c) were tested with Fisher exact tests. The analysis plan (revision_r1/ANALYSIS_PLAN_batch2d.md) was committed before the analysis was run. Code: revision_r1/final/scripts/d3_period_correction.py.

Assumptions and results. All validation records had an abstract, so applying p(h | c) to title-only records assumes that they are misclassified like abstract-present records. Both versions, the conversion rates by period, and Advocacy precision and recall by period are in Multimedia Appendix 2, Table S11.

## Supplementary Note 11. MeSH and keyword re-fetch and term triangulation

Re-fetch. On 28 October 2026, MeSH descriptors and author keywords were re-fetched for the 16,759 retained records with NCBI E-utilities efetch (db=pubmed, retmode=xml; 84 requests of at most 200 PMIDs, at most 3 requests per second; script revision_r1/scripts/b6_fetch_mesh.py). NCBI returned 16,756 of 16,759 records; the 3 missing PMIDs are listed in revision_r1/outputs/B6/b6_fetch_missing_pmids.txt. Raw XML is kept locally with a committed SHA-256 manifest.

| Year | Records with MeSH / with author keywords |
|---|---|
| 2021 | MeSH 88.5% (942/1064); keywords 68.4% (728/1064) |
| 2022 | MeSH 85.3% (1147/1344); keywords 71.4% (959/1344) |
| 2023 | MeSH 80.5% (1655/2055); keywords 71.0% (1460/2055) |
| 2024 | MeSH 79.0% (2928/3704); keywords 73.4% (2720/3704) |
| 2025 | MeSH 74.0% (4367/5899); keywords 81.6% (4815/5899) |

Lexicons (verbatim from revision_r1/scripts/b6_terms.py, as pre-specified in ANALYSIS_PLAN_batch2b.md). A record matches a theme if its title, abstract or author keywords contain a text term (case-insensitive, word boundary; * = any ending) or its MeSH descriptors include a listed descriptor. Matching is among critical records 2021-2025.

| Lexicon theme | Text terms | MeSH descriptors | Compared with LLM theme |
|---|---|---|---|
| Errors and hallucination | hallucinat*; confabulat*; fabricat*; inaccura*; misinformation; error*; incorrect; factual* | Diagnostic Errors; Medical Errors | Hallucination / errors |
| Patient safety | patient safety; safety; harm*; adverse | Patient Safety; Patient Harm | Patient safety |
| Regulation | regulat*; governance; oversight; liability; legislat*; policy; policies; accountab* | Government Regulation; Legislation as Topic; Health Policy | Governance / regulation |
| Ethics and bias | ethic*; bias*; fairness; equit*; discriminat*; justice | Ethics, Medical; Bias | Ethics & bias |

Term comparisons. Weighted log-odds ratios with an informative Dirichlet prior (Monroe, Colaresi and Quinn, 2008): for each term w, δ_w = log((y_iw + α_w) / (n_i + α0 - y_iw - α_w)) - log((y_jw + α_w) / (n_j + α0 - y_jw - α_w)), with y the number of records in each group containing the term (document frequency), n the sum of y over all ranked terms in the group, prior α_w = α0 x (the term's share of document frequencies in the background of all 16,759 retained records) and α0 = 1,000; variance σ² = 1/(y_iw + α_w) + 1/(y_jw + α_w); z = δ/σ. Terms are MeSH descriptors and author keywords (lower-cased); only terms present in at least 20 records are ranked. Comparisons: records published 2024-2025 vs 2021-2022, and critical vs favourable records, 2021-2025. The top 30 terms in each direction of each comparison are tabulated in Multimedia Appendix 2, Table S24.
