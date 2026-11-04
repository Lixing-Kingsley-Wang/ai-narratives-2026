# revision_r1/final/v3b (2026-11-03)

Copy of `final/v3/` with three changes to Multimedia Appendix 2. Built by Claude in its workspace; no API calls.
`final/v3/` is untouched and stays as committed (d181d7c).

## What changed against v3
1. MA2 numbering follows first citation in Peter's 2026-11-02 Methods: lexicon decomposition = **Table S25**,
   Advocacy by specialty = **Table S26** (swapped). Order file: `ma/ma_order_v3.yaml`.
2. **Table S13** (mechanism confusion) gains panel (c): class-specific precision, recall (exact 95% CIs) and F1,
   computed from panels (a) and (b); F1 asserted against Table 3 values.
3. **Table S9** note adds the prespecified year test within the excluded strata: OR 1.263 per year
   (Wald 95% CI 0.898-1.776), P=.18; design-weighted OR 1.267 (bootstrap 95% CI 0.940-1.760)
   (source: `revision_r1/REPORT_A3_prefilter_scoring.md`).

MA1, MA3, Figures 1-6 and Tables 1-3 are unchanged from v3 (MA3 was re-assembled; same content).

## Scripts
`scripts/` = v3 scripts with two edits: `v3_common.py` (V3 now points to this folder) and `v3_units.py`
(items 2 and 3 above). Run order as in `README_v3.md`: v3_numbering, v3_units, v3_figures, v3_ma1,
v3_main_tables, assemble_v3, v3_qa. Reads `revision_r1/final/` read-only; writes only inside `final/v3b/`.
In v3b only `v3_units.py` and `assemble_v3.py` were re-run.

**Do not re-run `v3_numbering.py` here.** Its inputs in `manuscript_text/` are the 2026-11-01 drafts, so it would
restore the v3 order (S25/S26 swapped back). `ma/ma_order_v3.yaml` was edited by hand for v3b. To redraw a figure,
run `v3_figures.py` (or the figure's source script) and then `assemble_v3.py` only.
