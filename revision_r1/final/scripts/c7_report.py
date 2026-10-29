"""Write revision_r1/REPORT_batch2c.md (JMIR R1 Batch 2c). Headline numbers are read
from the numbers book; nothing is retyped. Run with revision_r1/.venv after c1-c6.
"""

from __future__ import annotations

import csv

from c_common import FINAL, R1, c_book

B = c_book()
v = lambda i: B[i]["value"]


def main():
    nmap = list(csv.DictReader(open(FINAL / "ma" / "ma_numbering_map.csv", encoding="utf-8")))
    qa = (FINAL / "QA_batch2c.md").read_text()
    tok = qa.split("Tokens left for review: ")[1].split(".")[0]
    L = [
        "# Batch 2c report · final figures, tables, appendices and numbers book (JMIR #109710, R1)", "",
        "Branch `jmir-r1-major-revision`. Everything new is under `revision_r1/final/` except this report. No LLM API calls, "
        "no data fetches, no manuscript edits, nothing deleted or overwritten outside `final/`, nothing pushed.", "",
        "## 1. Files", "",
        "| Path (under `revision_r1/`) | Contents |", "|---|---|",
        f"| `final/NUMBERS_BOOK_R1.md`, `final/NUMBERS_BOOK_R1.csv` | C1 numbers book: {len(B):,} numbers with stable IDs, JMIR format, window and source file; ends with the superseded-numbers list and the B7 corrections verbatim |",
        "| `final/data/*.csv`, `*.json` | 2021-2025 recomputations behind the book (flow, subsets, missing data, specialty, region, country, publication type, review subtypes, FDA robustness, East Asia within specialty, theme by format, Advocacy by specialty, validation CIs, v2 trend, pooled themes, Q3, B5 annual, B2 recovered vs retained, confusion matrices, forward-validation counts) |",
        "| `final/figures/Fig1-Fig6.{png,pdf}`, `Fig*_caption.md` | C2 main figures (PNG 600 dpi + vector PDF) and factual captions; `figure_ids_used.csv` lists the book IDs each figure plots |",
        "| `final/tables/Table1-3.{docx,md}` | C3 main tables as real Word tables with footnotes; `table_ids_used.csv` |",
        "| `final/ma/units/` | C4 units: 29 table specs (`tables/*.json`) and 10 figures (`figures/*.png/.pdf/_caption.md`) with the book IDs used |",
        "| `final/ma/ma_order.yaml`, `final/ma/assemble.py` | Default order and the assembler |",
        "| `final/ma/Multimedia_Appendix_2_R1.{docx,md}`, `Multimedia_Appendix_3_R1.{docx,md}`, `ma_numbering_map.csv` | Assembled appendices and the unit -> number map |",
        "| `final/ma/Multimedia_Appendix_1_R1.{docx,md}`, `ma1_prompt_hashes.txt` | C5 corrected Supplementary Notes 1-10 |",
        "| `final/QA_batch2c.md`, `final/QA_unmatched_tokens.csv` | C6 QA |",
        "| `final/scripts/c_common.py`, `c_docx.py`, `c1_compute.py`, `c1_numbers_book.py`, `c2_figures.py`, `c3_tables.py`, `c4_units.py`, `c5_ma1.py`, `c6_qa.py`, `c7_report.py` | Scripts (c1_compute, c2, c4: project venv; others: `revision_r1/.venv`) |",
        "| `final/requirements_batch2c.txt` | python-docx, lxml, PyYAML added to `revision_r1/.venv` (pinned) |",
        "| `final/checksums/*_post_batch2c.sha256` | `output/` manifests after Batch 2c |", "",
        "Run order: `c1_compute.py` -> `c1_numbers_book.py` -> `c2_figures.py` -> `c3_tables.py` -> `c4_units.py` -> "
        "`ma/assemble.py` -> `c5_ma1.py` -> `c6_qa.py` -> `c7_report.py`.", "",
        "## 2. Analytic N and headline numbers (2021-2025)", "",
        f"- **Analytic N:** {v('COR-23')} records with a valid stance (discourse {v('COR-24')}, evaluative {v('COR-25')}); from "
        f"{v('COR-16')} eligible Q1/Q2 records, {v('COR-19')} retained by the prefilter, {v('COR-22')} stance FAILED. "
        f"January-April 2026: {v('COR-2026-N')} records, descriptive table only.",
        f"- **Prefilter audit:** estimated AI-engaged among excluded records {v('COR-AUDIT-FN')}; about {v('COR-AUDIT-MISSED')} records.",
        f"- **Overall:** critical {v('RES-OVR-CRITICAL')}; Cautious Optimism {v('RES-OVR-CAUTIOUSOPTIMISM')}; Advocacy {v('RES-OVR-ADVOCACY')}.",
        f"- **Critical trend:** {v('RES-TMP-CRIT-2021')} (2021) to {v('RES-TMP-CRIT-2025')} (2025); {v('RES-TMP-CRIT-RHO')}; "
        f"unadjusted {v('RES-TMP-CRIT-OR')}; adjusted {v('RES-TMP-CRIT-AOR')}.",
        f"- **Advocacy trend:** {v('RES-TMP-ADV-2021')} to {v('RES-TMP-ADV-2025')}; {v('RES-TMP-ADV-RHO')}; unadjusted "
        f"{v('RES-TMP-ADV-OR')}; adjusted {v('RES-TMP-ADV-AOR')}. Strong endorsement (B3): {v('RES-TMP-SE-2021')} to "
        f"{v('RES-TMP-SE-2025')}; {v('RES-TMP-SE-OR')}.",
        f"- **Themes (among {int(float(B['COR-SUB-01']['point']))} critical records), OR per year:** patient safety {v('RES-TMP-TH-PATIENTSAFETY-OR')}; "
        f"hallucination/errors {v('RES-TMP-TH-HALLUCINATIONERRORS-OR')}; regulation {v('RES-TMP-TH-GOVERNANCEREGULATION-OR')}; "
        f"ethics & bias {v('RES-TMP-TH-ETHICSANDBIAS-OR')}. Lexicon direction agrees for safety and errors, not for regulation "
        f"({v('RES-THM-LEX-GOVERNANCEREGULATION-OR')}) or ethics ({v('RES-THM-LEX-ETHICSANDBIAS-OR')}).",
        f"- **Mechanism:** hallucination-gated n={v('COR-SUB-07').split(' ')[0]}; fabrication-involved {v('RES-TMP-FAB-GATED-2021')} (2021) "
        f"to {v('RES-TMP-FAB-GATED-2025')} (2025); generative share {v('RES-TMP-GENSHARE-2021')} to {v('RES-TMP-GENSHARE-2025')}.",
        f"- **Specialty:** {v('RES-SPC-RANGE')}; FDA (exploratory ecological): all 18 {v('RES-SPC-FDA-RHO18')}; 11 non-zero "
        f"{v('RES-SPC-FDA-RHO11')}.",
        f"- **Geography:** United States {v('RES-GEO-CTY-UNITEDSTATES')} vs China {v('RES-GEO-CTY-CHINA')}; adjusted {v('RES-GEO-USCN-AOR')}. "
        f"East Asia {v('RES-GEO-REG-EASTASIA')}; adjusted vs North America {v('RES-GEO-AOR-EASTASIA')}. Countries with >=50 records: "
        f"{v('RES-GEO-NCTY50')}.",
        f"- **Publication format:** Reviews critical {v('RES-FMT-REVIEW-CRITICAL')}, favourable {v('RES-FMT-REVIEW-FAVOURABLE')}; "
        f"adjusted Review vs Research Article {v('RES-FMT-REVIEW-AOR')}; opinion vs research {v('RES-FMT-CHISQ')}.",
        f"- **Validation:** stance quadratic κ {v('VAL-ST-QK-225')} (in scope); themes micro-F1 {v('VAL-TH-MICRO-200-UN')} (N=200); "
        f"prefilter audit sensitivity {v('VAL-PF-AUDIT-PROD2X2SENSITIVITY')}, κ {v('VAL-PF-AUDIT-PROD2X2KAPPA')}; model type κ "
        f"{v('VAL-MX-MT-K')}; failure mode κ {v('VAL-MX-FM-K')}; specialty κ {v('VAL-SP-K')}.", "",
        "## 3. Multimedia Appendix order", "",
        "Default order (Methods, then Results):", "",
        "| Number | Unit ID | Title |", "|---|---|---|",
    ] + [f"| {r['appendix'].replace('Multimedia Appendix ', 'MA')} {r['number']} | `{r['unit_id']}` | {r['title']} |" for r in nmap] + [
        "",
        "**To change it:** reorder the unit IDs in `final/ma/ma_order.yaml` (each ID once; no renaming), then run "
        "`revision_r1/.venv/bin/python revision_r1/final/ma/assemble.py`. The assembler renumbers S1, S2, ..., resolves every "
        "`{{F:id}}` / `{{T:id}}` cross-reference in captions and footnotes, rewrites both appendices (.docx and .md) and "
        "`ma_numbering_map.csv`, and stops if an ID is missing, duplicated or unresolved.", "",
        "## 4. QA results (details: `final/QA_batch2c.md`)", "",
        f"1. **Numbers:** every numeric token in Tables 1-3, the 29 MA3 units and all 16 figure captions was matched against the book "
        f"rows its builder read (strict per-unit check), with derived differences verified arithmetically. Tokens left for review: "
        f"{tok} (the FDA device column total, 1430, a sum of 18 book values that equals the submitted total). Figure values are "
        "plotted from book IDs.",
        "2. **Figure rules:** no simple bar graphs; exact values printed on every panel (in the B2/B5 robustness figure for the "
        "reference series and strong endorsement, the other series' values are in MA3 tables); no asterisks; no in-figure titles; "
        "PNG 600 dpi plus PDF; base font 7 pt at final width, no smaller font set; Okabe-Ito palette, fixed stance colours; maps use "
        "a diverging RdYlBu scale. Exception: the unchanged forward-validation Sankey (below).",
        "3. **2026:** no figure plots 2026 data. Figure 1 prints the retrieval period and the window-step exclusion counts "
        "(January-April 2026 n=10,757; May 2026 or later n=1134); the Sankey keeps its 2024-April 2026 evidence window.",
        "4. **Word tables:** Tables 1-3 one real table each; MA3 29 real tables; MA1 4 (Notes 1, 9 and 10); no table is an image.",
        "5. **Note 2(a) hash:** `b3949917…` equals the production prompt hash (recomputed from `9c79cd5:classify_stance_batch.py`).",
        "6. **Format scan:** no lowercase p, no leading zero in P, no 'Cohen's', no em dash in a caption, no comma in a 4-digit "
        "number, no en dash in a range.", "",
        "## 5. Not produced, deviations, and items for Peter", "",
        "- **Advocacy categorical-year ORs:** not produced. B4 fitted the categorical-year model (S1) for the critical outcome only; "
        "fitting it for Advocacy would be a new analysis. Book row `RES-TMP-ADV-CAT` says so.",
        "- **Sankey resolution:** reproduced unchanged from the submitted manuscript (1484 x 1139 px; about 225 pixels per inch at "
        "6.6 in), below the 300 dpi rule. The repository SVG is supplied, but it carries an in-figure title the submitted image "
        "cropped out, and no SVG renderer is installed here. A 300 dpi version needs a re-render without the title.",
        "- **Table 3:** B2 corpora and B5 have stance/region/publication-type values only where those analyses exist; recovered "
        "B2 records carry no theme, specialty or region label, and B5 did not recompute country, so those cells are '—' "
        "(footnoted).",
        "- **Old Table S16 (specialty definitions):** definitions verbatim; the n column is updated to 2021-2025 (the submitted "
        "column counted the retired set). Old Table S2 (17 records of 2026) is replaced by the January-April 2026 descriptive table.",
        f"- **v2 rubric on 2021-2025 (Table S1 v2 column):** Cautious Optimism {v('RES-V2-CAUTIOUSOPTIMISM')} vs v1 "
        f"{v('RES-TMP-CO-RHO')} (opposite direction); Advocacy {v('RES-V2-ADVOCACY')} (same direction). Reported only.",
        f"- **B5 removed count:** {v('RES-SEN-B5D1-REMOVED')} records in 2021-2025 for D1 (the Batch 2b report's 2781 includes January-April 2026).",
        "- **Two CIs for the unadjusted year OR:** Table 2 prints B4's cluster-robust interval (1.038-1.116); the temporal results "
        "and Table 3 print the record-level Wald interval (1.046-1.108). Same point estimate (1.077).",
        "- **Within-genre CIs** use the B7 deterministic per-cell seeds (the corrected Table S3), not the T4 joint bootstrap; point "
        "estimates are identical.",
        "- **Intra-rater κ interval** spans 0 to 1 (1 disagreement in 20); footnoted in Table 1.",
        "- **Working title:** the appendices' title block uses 'Infoveillance Study of 14,058 High-Quartile Journal Abstracts, "
        "2021-2025' with a note that the revised manuscript title may differ.",
        "- **Q3 count:** 5463 Q3 records before the cutoff; the Q3 arm analysed in 2021-2025 has 853 records with a valid stance.",
        "- **Main Figure 1 mentions 2026** only as exclusion counts of the window step, which the brief requires; flagged here because "
        "decision 2 says no 2026 element in any figure.", "",
        "## 6. Checks", "",
        "- `output/` checksums: worktree (189 files) and main checkout (174 files) identical to the post-Batch 2b manifests; new "
        "manifests in `final/checksums/`.",
        "- No tracked file outside `revision_r1/final/` and this report was changed; `revision_r1/inputs/` read only (the submitted "
        "Sankey image and the MA1 Notes 3-7 text were read from the submitted .docx files).",
        "- No LLM API call; no network data fetch (python-docx and PyYAML were installed into `revision_r1/.venv` from PyPI).",
        "- Nothing pushed.",
    ]
    (R1 / "REPORT_batch2c.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("report written")


if __name__ == "__main__":
    main()
