# AI Narratives in Medicine: Temporal Bibliometric Analysis

A computational bibliometric study of stance and discourse toward AI in Q1/Q2 medical journals, January 2021 – April 2026.

**Authors:** Kingsley Wang, Dan Poenaru
**Affiliation:** Harvey E. Beardmore Division of Pediatric Surgery, Montreal Children's Hospital / McGill University
**Target:** Lancet Digital Health, Commentary

This repository contains the prompts, code, PubMed identifiers, and committed outputs behind the manuscript. Package versions are pinned in [requirements.txt](requirements.txt) for Python 3.12.

For a fully-cited, verbatim provenance record of prompts/codebooks/model settings behind each reported number, see [METHODS_SOURCE_OF_TRUTH.md](METHODS_SOURCE_OF_TRUTH.md).

## Setup

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Scripts that call the Anthropic API expect an `ANTHROPIC_API_KEY` in a local `.env` file (never committed; see `.gitignore`).

## Analytic dataset

[data/analytic_dataset.csv](data/analytic_dataset.csv) is one row per classified record (pmid, pub_year, stance, theme(s), mechanism, specialty, region) — the single joined table backing the manuscript's figures and tables. `theme(s)` and `mechanism` are populated only for Alarm/Caution ("critical") records, since only those were theme- and Q7 mechanism-coded. The full raw corpus (titles/abstracts) is not committed; regenerate `output/classified_medical_Q1Q2.csv` locally by running the retrieval → prefilter → stance steps below.

## Methods steps → files

| Methods step | Script(s) | Key output(s) |
|---|---|---|
| **Retrieval** | [fetch_pubmed_medical.py](fetch_pubmed_medical.py) (PubMed medical corpus), [fetch_scopus_legal.py](fetch_scopus_legal.py) + [run_legal_pipeline.py](run_legal_pipeline.py) (Scopus legal comparator) | `output/raw_medical_*.csv`, `output/raw_legal_*.csv` (gitignored — regenerate locally) |
| **Prefilter** | [sjr_filter.py](sjr_filter.py) (SJR quartile, using [input/sjr/](input/sjr/)), [prefilter.py](prefilter.py) / [prefilter_batch.py](prefilter_batch.py) / [prefilter_split.py](prefilter_split.py), [split_corpus.py](split_corpus.py) | `output/prefiltered_discourse_eval.csv` |
| **Stance classification** | [classify_stance.py](classify_stance.py) / [classify_stance_batch.py](classify_stance_batch.py), [compute_kappa.py](compute_kappa.py) / [compute_kappa_v2.py](compute_kappa_v2.py) (validation), [compare_v1_v2.py](compare_v1_v2.py), [diagnose_v1_v2_vs_human.py](diagnose_v1_v2_vs_human.py) | `output/classified_medical_Q1Q2.csv` (v1, canonical; gitignored, regenerate locally), `output/validation/kappa_report.md`, `output/comparison_v1_v2.md` |
| **Themes** | [classify_themes.py](classify_themes.py) / [classify_themes_batch.py](classify_themes_batch.py) | `output/analysis/thematic_alarm.csv` |
| **Mechanism / Q7** | [classify_q7_failuremode.py](classify_q7_failuremode.py), [q7_abstract_filter.py](q7_abstract_filter.py), [q7_build_validation.py](q7_build_validation.py), [q7_kappa.py](q7_kappa.py) / [q7_kappa_compare.py](q7_kappa_compare.py), [q7_phase1_summary.py](q7_phase1_summary.py) / [q7_phase1_figure.py](q7_phase1_figure.py), [q7_phase2_concat.py](q7_phase2_concat.py), [q7_phase3_analyses.py](q7_phase3_analyses.py), [q7_s5_1_a_specialty.py](q7_s5_1_a_specialty.py) / [q7_s5_1_b_plateau.py](q7_s5_1_b_plateau.py) | `output/analyses/q7_classified_ac.csv`, `output/analyses/q7_summary.md`, `output/figures/q7_*.png` |
| **Specialty** | [analysis/classify_specialty.py](analysis/classify_specialty.py), [analysis/compute_specialty_kappa.py](analysis/compute_specialty_kappa.py), [specialty_build_validation.py](specialty_build_validation.py) | `output/specialty_classifications.csv`, `output/analyses/specialty_kappa_report.md` |
| **Geography** | [analysis/extract_geography.py](analysis/extract_geography.py) (canonical 8-region parser), [analysis/run_country_critical_map.py](analysis/run_country_critical_map.py), [analysis/run_region_critical.py](analysis/run_region_critical.py) / [analysis/run_region_temporal.py](analysis/run_region_temporal.py), [analysis/run_east_asia_diagnose.py](analysis/run_east_asia_diagnose.py) | `output/geography_classifications.csv`, `output/figures/world_critical_map.png` |
| **FDA (AI/ML device adoption proxy)** | [analysis/run_specialty_aiadoption.py](analysis/run_specialty_aiadoption.py), [analysis/revision_checks/stat8_fda_drop_zero.py](analysis/revision_checks/stat8_fda_drop_zero.py) | `output/external/fda_aiml_devices.csv` (input), `output/figures/specialty_aiadoption_vs_critical.png` |
| **Prophecy panel** | [prophecy_phase1_extract_claims.py](prophecy_phase1_extract_claims.py) → [prophecy_phase1_build_review_xlsx.py](prophecy_phase1_build_review_xlsx.py) → [prophecy_phase1_freeze_from_xlsx.py](prophecy_phase1_freeze_from_xlsx.py) → [prophecy_phase2_embed_retrieve.py](prophecy_phase2_embed_retrieve.py) → [prophecy_phase2_summarize.py](prophecy_phase2_summarize.py) → [prophecy_phase2_build_verdict_xlsx.py](prophecy_phase2_build_verdict_xlsx.py); [prophecy_sankey.py](prophecy_sankey.py) | `output/analyses/prophecy/phase1_signature_claims_FROZEN.csv`, `output/analyses/prophecy/phase2_prophecy_verdicts_worksheet.csv`; protocol: [prophecy_panel_preregistration.md](prophecy_panel_preregistration.md) |
| **Stats / robustness** | [analysis/robustness.py](analysis/robustness.py) (shared helpers: `bootstrap_ci`, `load_classifications`), [analysis/revision_checks/cv1_within_genre.py](analysis/revision_checks/cv1_within_genre.py), [analysis/revision_checks/cv2_keep_rate.py](analysis/revision_checks/cv2_keep_rate.py), [analysis/revision_checks/rep1_stance_stability.py](analysis/revision_checks/rep1_stance_stability.py), [analysis/revision_checks/stat2_cramers_v.py](analysis/revision_checks/stat2_cramers_v.py), [analysis/revision_checks/stat8_fda_drop_zero.py](analysis/revision_checks/stat8_fda_drop_zero.py) | `output/revision_checks/wave1_summary.md` and per-check CSVs |

Earlier/diagnostic scripts from initial pipeline development (`diagnose_*.py`, `debug_*.py`, `test_*.py`, `inspect_pilot*.py`, `check_*.py`, `analyse_industry.py`, `analyse_narratives.py`, `analyse_obsolescence.py`, etc.) are retained at the repo root for provenance but are not part of the canonical pipeline above.

## Repository layout

- `input/` — reference data (SJR journal quartiles)
- `output/analysis/`, `output/analyses/` — analysis results (CSV/MD)
- `output/figures/` — figures at 300 DPI
- `output/external/` — third-party reference data (FDA device list, Natural Earth country boundaries)
- `output/validation/`, `output/revision_checks/` — human-coding validation and reviewer-requested robustness checks
- `data/` — the single committed analytic dataset (see above)

## License

Code is licensed under [MIT](LICENSE). The analytic dataset (`data/analytic_dataset.csv`) and other committed output tables/figures are licensed under [CC-BY-4.0](LICENSE).
