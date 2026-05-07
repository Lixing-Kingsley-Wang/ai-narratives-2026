# AI Narratives in Medicine: Temporal Bibliometric Analysis

A computational bibliometric study of stance and discourse toward AI in Q1/Q2 medical journals, 2021–2025.

**Authors:** Kingsley Wu, Dan Poenaru  
**Affiliation:** Harvey E. Beardmore Division of Pediatric Surgery, Montreal Children's Hospital / McGill University  
**Target journal:** Lancet Digital Health  
**Status:** Analysis complete; manuscript in preparation (May 2026)

## Key Findings
- Critical stance (Alarm + Caution) peaked in 2023 at 25.3%, declining to 22.0% by 2025
- Dominant concerns: patient safety (58–64%) and governance (38–62%), not replacement fears (3–8%)
- Hallucination concerns rose sharply 2021→2024 then plateaued
- Q1/Q2 journals showed higher critical rates than Q3 (up to 12pp gap in 2023)
- Critical stance highest in Psychiatry/Neurology (35.5%), lowest in Radiology (13.1%)

## Requirements
```
pip install anthropic python-dotenv requests aiohttp matplotlib numpy
```

## Pipeline
```
python fetch_pubmed_medical.py → sjr_filter.py → prefilter.py →
classify_stance.py → classify_themes.py → analyse_narratives.py
```

## Environmental Impact
~2.4 kg CO₂e (Luccioni et al. FAccT 2023 methodology)
