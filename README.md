# AI Narratives in Medicine: Temporal Bibliometric Analysis

A computational bibliometric study of stance and discourse toward AI in Q1/Q2 medical journals, January 2021 – April 2026.

**Authors:** Kingsley Wang, Dan Poenaru  
**Affiliation:** Harvey E. Beardmore Division of Pediatric Surgery, Montreal Children's Hospital / McGill University  
**Target journal:** Lancet Digital Health  
**Status:** Corpus rebuild May 2026 — sole-investigator re-run for Lancet Digital Health Commentary submission.

> The May 2026 pipeline run (corpus fetch, prefilter, stance and thematic classification, validation export) was conducted by Kingsley as sole lead investigator; Dan Poenaru remains senior author. The query was expanded to include newer model names (`GPT-5`, `GPT-4o`, `GPT-4.5`) that postdate the original pipeline. Prior to running the prefilter on the full corpus, a 50-record pilot validation will be conducted (Kingsley's hand-codes vs. Haiku 4.5) to support the Methods section.

## Key Findings (from prior pipeline run, May 2026 — to be replaced after re-run completes)
- Critical stance (Alarm + Caution) peaked in 2023 at 25.3%, declining to 22.0% by 2025
- Dominant concerns: patient safety (58–64%) and governance (38–62%), not replacement fears (3–8%)
- Hallucination concerns rose sharply 2021→2024 then plateaued
- Q1/Q2 journals showed higher critical rates than Q3 (up to 12pp gap in 2023)
- Critical stance highest in Psychiatry/Neurology (35.5%), lowest in Radiology (13.1%)

## Requirements
```
pip install anthropic python-dotenv requests aiohttp pandas openpyxl matplotlib numpy
```

## Pipeline
```
python fetch_pubmed_medical.py → sjr_filter.py → prefilter.py →
classify_stance.py → classify_themes.py → analyse_narratives.py
```

## Environmental Impact
~2.4 kg CO₂e (Luccioni et al. FAccT 2023 methodology)
