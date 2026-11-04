# revision_r1/final/v3/ — final-numbering build (2026-11-02, Claude)

New folder; nothing outside it was written or changed. Inputs (read-only): revision_r1/final/ (Batch 2c/2d units,
tables, figures, NUMBERS_BOOK_R1_v2.csv) and the accepted text of Methods v2, Results v3, Discussion v2 (manuscript_text/).

Build order (scripts/, Python 3 with python-docx, matplotlib, scipy, PyYAML, Pillow; run from scripts/):
1. v3_numbering.py   -> ma/ma_order_v3.yaml, token_label_map_v3.csv (first-citation order; MA1 notes, MA2 tables, MA3 figures)
2. v3_units.py       -> ma/units/tables/*.json (cleaned copies + corrected_prevalence + lexicon_decomposition), ma/units_v3_edit_log.tsv
3. v3_figures.py     -> figures/Fig1_v3.*, ma/units/figures/* (temporal_robustness, terms, advocacy_measures redrawn/new; others copied)
4. v3_ma1.py         -> ma/Multimedia_Appendix_1_R1_v3.{docx,md}
5. v3_main_tables.py -> tables/Table{1,2,3}_v3.{docx,md}
6. assemble_v3.py    -> ma/Multimedia_Appendix_2_R1_v3.* (tables), ma/Multimedia_Appendix_3_R1_v3.* (figures), ma/ma_numbering_map_v3.csv
7. v3_qa.py          -> QA_v3.md

Every number comes from NUMBERS_BOOK_R1_v2.csv or from the Batch 2c/2d units; edits are wording only and each is asserted
and logged (ma/units_v3_edit_log.tsv). Figures 2-6 are unchanged copies. No API calls.
Also here: Results_r1_Claude_v3_tracked.docx, Discussion_r1_Claude_v2_tracked.docx, r1_token_replacement_list_v3.md.
