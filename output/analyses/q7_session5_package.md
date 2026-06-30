# Q7 Session-5 package — full-abstract (abstract-present) analyses & figures

Everything here is computed on the **abstract-present** subset (title-only papers
dropped as QC) and, for the temporal/specialty analyses, on the **full A+C
critical corpus** (Alarm + Caution), not Alarm-only. Classifier:
`q7_failuremode_v1`, `claude-sonnet-4-6`, temperature 0. Conventions: drop FAILED,
seed=42, bootstrap n=1000 percentile 95% CI.

Corpus sizes: A+C valid = 5,159; **abstract-present A+C = 4,747** (843 Alarm +
3,904 Caution). Validation set = 120 papers → 108 abstract-present.

---

## Read these first
| file | what |
|---|---|
| `q7_summary.md` | Narrative writeup — gate audit, trend, S4-1 disentanglement, divergence, validation, decision owed to Dan. **Start here.** |
| `q7_session5_package.md` | This manifest. |

## Classified data (the base table)
| file | what |
|---|---|
| `q7_classified_ac.csv` | 5,161 critical papers (Alarm+Caution) with failure_mode + model_type + confidence + rationale. The source for all A+C analyses. Filter `abstract`-present via pmid join to `output/classified_medical_Q1Q2.csv`. |

## Figures (all abstract-present; @300 dpi)
| figure | scope | shows |
|---|---|---|
| `q7_ac_temporal_abstractonly.png` | A+C | failure_mode & model_type composition by year + key shares (3 panels). |
| `q7_gate_composition_abstractonly.png` | A+C | Part 1 gate audit: heterogeneous "hallucination" gate + gate-recall miss. |
| `q7_s41_disentangle_abstractonly.png` | A+C | Part 3 S4-1: criticality vs generative-share per specialty + ρ table. |
| `q7_ac_failuremode_by_specialty_abstractonly.png` | A+C | failure_mode composition per specialty + gen-share vs confab-share scatter (2 panels). |
| `q7_ac_confab_plateau_abstractonly.png` | A+C | fabrication concern did NOT scale with LLM uptake (generative-share vs confab-among-generative). |

## Tables / CSVs (all abstract-present)
| file | what |
|---|---|
| `q7_ac_temporal_trend_abstractonly.csv` | Part 2: % per year confab (broad/strict) & generative-share, bootstrap 95% CI. |
| `q7_ac_by_specialty_abstractonly.csv` | per-specialty failure_mode composition + gen/confab share + FDA/criticality link. |
| `q7_ac_temporal_shares_abstractonly.csv` | per-year gen-share, confab-strict/broad, confab-among-generative + CI. |

## Validation (independent human coding)
| file | what |
|---|---|
| `q7_kappa_report_adjudicated_abstractonly.md` | Final κ: model_type 0.953, failure_mode 0.796 (adjudicated, abstract-present n=108). |
| `q7_kappa_report_abstractonly.md` | Blind (pre-adjudication) κ: model_type 0.843, failure_mode 0.574 (abstract-present n=108). Added in S5-9 (initially omitted). |
| `q7_kappa_report.md` | Blind κ on all 120 (no abstract QC): model_type 0.798, failure_mode 0.541. |
| `q7_validation_coding.xlsx` | 120 blind-coded papers (human labels). |
| `q7_adjudication.xlsx` | 46 disagreements adjudicated. |

---

## Headline numbers (abstract-present, A+C)

**1. The old "hallucination" theme gate is heterogeneous.** Inside the gate,
misclassification is the majority every year (56–90%); confab-involved is 0–1%
pre-2023, ~21–23% post-2023. The theme rise is partly a composition shift, not
pure fabrication growth. Gate recall for confabulation = 89.7%, precision poor.

**2. Gate-independent trend.** confab-broad rises 0→14% (ρ=+0.94) while
generative-share climbs 2.5→63% (ρ=+0.94). The generative rise is partly expected
(new tech); the informative result is that fabrication concern plateaus.

**3. S4-1 disentanglement (familiarity, not technology).**
Spearman(critical_rate, FDA) = −0.647 (p=0.004); partial controlling
generative-share = −0.647 → **0% attenuation**; critical_rate vs generative-share
flat (ρ=−0.011). Gradient is FAMILIARITY-driven. Dermatology gen-share 40.7%,
below median. *Caveat: gen-share is endogenous to criticality → biased toward the
technology reading, yet still no attenuation → familiarity reading is robust.*

**4. Divergence.** generative-not-confab = 1,858 (39%); confab-not-generative = 1.
The two axes carry independent information; generative ≠ confabulation.

**5. Fabrication did not scale (S5-1-b, A+C).** generative-share rises ~80 pp
(ρ=+0.94) but confab-share-among-generative plateaus near 20–23%. Most critical
generative-AI papers are about accuracy/bias/judgement, not fabrication.

**6. Validation.** model_type κ = 0.953 (almost perfect); failure_mode κ = 0.796
(substantial), Gwet AC1 0.81. Residual disagreement is the human being more
conservative about fabrication than the classifier → confab figures are upper
bounds, which only strengthens (5).

---

## Open items for Dan / the write-up
- **Decision owed to Dan:** present Q7 as a supplementary reinterpretation of the
  hallucination-theme rise, vs. replacing the theme gate (which restates session
  1–3 numbers). See `q7_summary.md` § "Decision owed to Dan".
- Critical-only scope (A+C); a full-discourse generative covariate is the
  robustness upgrade for the S4-1 disentanglement.
- A `task_type` axis (diagnostic / text-generation / …) was discussed as a
  possible third axis; not yet built.
