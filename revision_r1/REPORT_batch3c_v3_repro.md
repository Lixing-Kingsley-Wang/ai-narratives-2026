# Batch 3 · Prompt C: v3 commit and reproducibility check

## Commit

- `revision_r1/final/v3/` committed as **d181d7c** ("Final MA numbering and cleaned tables/figures (v3)"), 109 files. Nothing inside `final/v3/` was modified.
- Neither `_claude_transfer` folder was staged:
  - `revision_r1/final/_claude_transfer/` (worktree);
  - `_claude_transfer/` (main checkout).
- **`.gitignore` covers neither folder**, so both show as untracked. Per instruction, `.gitignore` was not edited. If Peter wants them ignored, a line `_claude_transfer/` would cover both.

## Reproducibility

- `revision_r1/final/` was copied, without `_claude_transfer`, to a scratch directory outside the repository. The seven scripts in the copy's `v3/scripts/` were then run in the README order: `v3_numbering`, `v3_units`, `v3_figures`, `v3_ma1`, `v3_main_tables`, `assemble_v3`, `v3_qa`.
- **Environment.** The scripts ran with `revision_r1/.venv` (Python 3.12; python-docx, PyYAML, scipy, Pillow and matplotlib already installed). The prompt named the project venv, but that venv lacks python-docx, and an earlier batch rule forbids modifying it, so it was not used.
- All seven steps completed.
- **Text outputs (67 files: `.md`, `.json`, `.csv`, `.yaml`, `.tsv`, `.txt`, `.py`): byte-identical** to the committed files.
- **Completeness:** no committed file was missing from the rebuild, and the rebuild produced no extra file.
- **PNG (17 files):**
  - 13 are byte-identical.
  - All have the same pixel size, except `ma/units/figures/advocacy_measures_fig.png`: 3240 x 1980 committed vs 3239 x 1980 rebuilt.
  - That one-pixel difference is consistent with tight-bounding-box rendering differences between environments.
- **DOCX, PDF and SVG** were not compared (timestamps and font embedding differ by design).
- **Same QA findings:** the rebuilt `v3_qa` reports the same five tokens in the Results draft that are not found in the book or the v3 tables: `12/293`, `245/831`, `28/1517`, `310/2453`, `364/891`. These are in the committed `QA_v3.md`, and Prompt D should check them.

## Checks

- `output/` checksums: worktree (189 files) and main checkout (174 files) are identical to the post-Batch 2c manifests.
- No API calls; nothing pushed.
