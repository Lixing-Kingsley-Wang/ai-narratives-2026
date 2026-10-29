"""C5 · Multimedia Appendix 1 (Supplementary Notes), corrected (JMIR R1 Batch 2c;
X1, D1, D2a, D5).

Built as a new file from the submitted MA1 (revision_r1/inputs/, read only):
  Note 1   methods component -> repository file table, with revision_r1/ rows added
  Note 2   "Stance classification prompts": (a) canonical v1, verbatim from
           classify_stance.py (SHA-256 asserted = production hash), (b) v2, verbatim
           from the current classify_stance_batch.py (sensitivity analysis only)
  Notes 3-7 copied paragraph by paragraph from the submitted docx, unchanged
  Note 8   B3 symmetric-endorsement prompt, verbatim, SHA-256, run configuration
  Note 9   R1 validation protocol: design, estimands, freeze commits, Amendments 1-3,
           verbatim "Read me first" sheets of both coding workbooks
  Note 10  B6 MeSH/keyword re-fetch, lexicons verbatim, Monroe et al. procedure
Prompts are read programmatically (ast, never retyped). Run with revision_r1/.venv.
Outputs: revision_r1/final/ma/Multimedia_Appendix_1_R1.docx and .md
"""

from __future__ import annotations

import hashlib
import subprocess

from docx import Document
from docx.shared import Pt
from openpyxl import load_workbook

from c_common import AUTHORS, MA, R1, REPO, TITLE_NOTE, TITLE_R1, c_book
from c_docx import table as docx_table, md_table

import r1_coding

BOOK = c_book()
V1_SHA = "b3949917159ea546ce7eb4c21224659be98c646aa937287d376f68c67992a39f"
B3_SHA = "27d28077cd7485fddcdfe4f0da3f4a3c13ad36a310bcd23f1544a5a89db50cf6"
SRC = R1 / "inputs" / "Multimedia appendix 1 Supplementary Notes.docx"
MD = []


def sha(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def git(*a):
    return subprocess.run(["git", *a], cwd=REPO, capture_output=True, text=True, check=True).stdout.strip()


def v(id_):
    return BOOK[id_]["value"]


class Doc:
    def __init__(self):
        self.d = Document()
        st = self.d.styles["Normal"]; st.font.name = "Arial"; st.font.size = Pt(10)

    def p(self, text, bold=False, italic=False, size=None, style=None, mono=False):
        par = self.d.add_paragraph(style=style) if style else self.d.add_paragraph()
        r = par.add_run(text); r.bold = bold; r.italic = italic
        if size:
            r.font.size = Pt(size)
        if mono:
            r.font.name = "Courier New"; r.font.size = Pt(8.5)
        MD.append(("```\n" + text + "\n```") if mono else (f"**{text}**" if bold else f"*{text}*" if italic else text))
        return par

    def h(self, text):
        self.d.add_heading(text, level=1)
        MD.append(f"## {text}")

    def h2(self, text):
        self.d.add_heading(text, level=2)
        MD.append(f"### {text}")

    def bullets(self, items):
        for it in items:
            self.d.add_paragraph(it, style="List Bullet")
        MD.append("\n".join(f"- {it}" for it in items))

    def table(self, header, rows, widths=None):
        docx_table(self.d, header, rows, widths=widths, size=8)
        MD.append(md_table(header, rows))


def copy_paragraph(dst, p):
    """Copy a source paragraph with its style and run-level bold/italic."""
    style = p.style.name if p.style.name in ("Heading 1", "Heading 2") else None
    q = dst.add_heading("", level=1 if style == "Heading 1" else 2) if style else dst.add_paragraph()
    for r in p.runs:
        nr = q.add_run(r.text); nr.bold = r.bold; nr.italic = r.italic
    MD.append(("## " if style == "Heading 1" else "### " if style else "") + p.text)


def main():
    D = Doc()
    src = Document(str(SRC))
    paras = src.paragraphs
    idx = {p.text.split(".")[0]: i for i, p in enumerate(paras) if p.text.startswith("Supplementary Note")}

    # title block in the submitted style
    D.p("Multimedia Appendix 1. Supplementary Notes", bold=True)
    D.p(TITLE_R1, italic=True)
    D.p(AUTHORS)
    D.p(TITLE_NOTE, italic=True, size=8)

    # ---------------- Note 1 ----------------
    D.h("Supplementary Note 1. Data and code availability")
    for i in range(idx["Supplementary Note 1"] + 1, idx["Supplementary Note 1"] + 5):
        if paras[i].text.strip():
            D.p(paras[i].text, bold=paras[i].runs[0].bold if paras[i].runs else False)
    D.p(f"For the R1 revision, all analyses use the {v('COR-23')} records with a valid stance published 2021-2025; "
        f"{v('COR-2026-N')} records published January-April 2026 are reported in one descriptive supplementary table only. The R1 "
        "components are in the repository's revision_r1/ directory; their outputs are listed in the second part of the table.")
    t = src.tables[0]
    rows = [[c.text for c in r.cells] for r in t.rows]
    header, orig = rows[0], rows[1:]
    R1ROWS = [
        ["R1 shared helpers and statistics", "revision_r1/scripts/r1_common.py; r1_coding.py",
         "Data loaders, percentile bootstrap (1000, seed 42), Cohen κ, Gwet AC1, κ_max, exact-permutation Spearman, logistic trend"],
        ["R1 re-analyses of the submitted pipeline (Batch 1)", "revision_r1/scripts/t1_*.py to t9_*.py; revision_r1/outputs/T1_* to T9_*",
         "Prefilter pilot metrics, stance per-class metrics, mechanism confusion matrices, 2021-2025 temporal and cross-sectional "
         "re-analysis, missing-data accounting, SJR quartile audit, review-subtype rule, data inventory"],
        ["Full-abstract prefilter re-run (A2)", "revision_r1/scripts/a2_prefilter_fullabstract_batch.py; revision_r1/outputs/A2/",
         "Copy of prefilter_batch.py with the full abstract and no failure default; diff committed"],
        ["R1 validation protocol and coding instruments (A1, A3)",
         "revision_r1/coding/PROTOCOL_r1_validation.md; revision_r1/scripts/a1_theme_sample.py, a3_prefilter_sample.py; "
         "revision_r1/coding/*_key.csv, *_manifest.csv",
         "Frozen protocol (Note 9), sampling scripts, keys and manifests; coding workbooks hold no model labels"],
        ["R1 validation scoring (A4, B1)",
         "revision_r1/scripts/a4_score_theme.py, a4_score_theme_n200.py, a4_score_prefilter.py, a4_score_prefilter_blankerror.py, "
         "a4_prefilter_exact_ci.py; revision_r1/outputs/A4_*, B1/",
         "Frozen scorers and amended primary analyses; Jeffreys and Clopper-Pearson intervals"],
        ["Stance of recovered records (B2)", "revision_r1/scripts/b2_stance_recovered_batch.py, b2_analysis.py, b_batch_engine.py; "
         "revision_r1/outputs/B2/", "v1 stance for records recovered by the full-abstract re-run; corpus sensitivity"],
        ["Symmetric endorsement re-classification (B3)", "revision_r1/scripts/b3_prompt.txt, b3_endorsement_batch.py, b3_analysis.py, "
         "b3_analysis_after_resubmit.py; revision_r1/outputs/B3/", "Strong-endorsement prompt (Note 8), labels and analysis"],
        ["Multivariable regression (B4)", "revision_r1/scripts/b4_prep_country.py, b4_regression.py; revision_r1/outputs/B4/",
         "Logistic, ordinal and sensitivity models with journal-clustered SEs"],
        ["SJR medical-category sensitivity (B5)", "revision_r1/scripts/t7_sjr_quartile.py, b5_sjr_medical_sensitivity.py; "
         "revision_r1/outputs/T7_*, B5/", "Category-level quartile re-match and restricted corpora D1-D3"],
        ["MeSH and keyword triangulation (B6)", "revision_r1/scripts/b6_fetch_mesh.py, b6_terms.py; revision_r1/outputs/B6/",
         "PubMed re-fetch (Note 10), lexicon trends, weighted log-odds term comparisons"],
        ["Pre-specified R1 analysis plan", "revision_r1/ANALYSIS_PLAN_batch2b.md", "Committed before any Batch 2b computation"],
        ["Numeric corrections (B7)", "revision_r1/scripts/b7_corrections.py; revision_r1/outputs/B7_corrections.md",
         "Old -> corrected values for the submitted manuscript"],
        ["R1 numbers, figures, tables and appendices", "revision_r1/final/scripts/c1_*.py to c5_*.py; revision_r1/final/ma/assemble.py; "
         "revision_r1/final/NUMBERS_BOOK_R1.csv", "Every reported R1 number with its source; figure, table and appendix builders"],
    ]
    D.table(header, orig + R1ROWS, widths=[1.7, 2.3, 2.6])

    # ---------------- Note 2 ----------------
    v1 = r1_coding.read_system_prompt("classify_stance.py")
    assert sha(v1) == V1_SHA, "v1 prompt hash differs from the production hash"
    prod = git("show", "9c79cd5:classify_stance_batch.py")
    import ast
    tree = ast.parse(prod)
    prod_prompt = next(ast.literal_eval(n.value) for n in tree.body if isinstance(n, ast.Assign)
                       and any(getattr(t_, "id", None) == "SYSTEM_PROMPT" for t_ in n.targets))
    assert sha(prod_prompt) == V1_SHA
    v2 = r1_coding.read_system_prompt("classify_stance_batch.py")
    v1c, v2c = git("log", "-1", "--format=%H", "--", "classify_stance.py"), git("log", "-1", "--format=%H", "--", "classify_stance_batch.py")
    D.h("Supplementary Note 2. Stance classification prompts")
    D.p("Two stance prompts exist in the repository. The canonical v1 prompt in (a) produced every stance label reported in the "
        "article. The stricter, conclusion-anchored v2 prompt in (b) was used only for the sensitivity analysis of the per-stance "
        "trends (Multimedia Appendix 3). Both prompts are reproduced verbatim as supplied to the classifier; they were extracted "
        "programmatically from the source files (Python ast), and no text has been edited.")
    D.h2("(a) Canonical v1 prompt: produced every reported stance label")
    D.p(f"Source: classify_stance.py at commit {v1c}; SHA-256 of the prompt text {V1_SHA} ({len(v1)} characters). The production "
        "Batch API run used the identical prompt (classify_stance_batch.py at commit 9c79cd5; same SHA-256).", size=9)
    D.p(v1, mono=True)
    D.p("User message template, as constructed by the classifier's build_prompt function (variable slots marked with braces):")
    D.p("Title: {title}\nAbstract: {abstract}", mono=True)
    D.p("The Abstract line is included only when the record has a non-empty abstract; the full abstract is sent with no character "
        "truncation. The title is always sent in full.")
    D.p("Run configuration", bold=True)
    D.bullets(["Model / model string: claude-sonnet-4-6",
               "API mode: Batch (Anthropic Message Batches API)",
               "Temperature: not set in code (omitted from the request parameters); provider default, T = 1.0",
               "max_tokens: 120",
               "System prompt: verbatim above (v1)",
               "Input fields sent to the model: title (full) + full abstract, no truncation; title only when the abstract is empty",
               "Output fields: stance, confidence, predictive_claim",
               "Retry / failure-handling rule: a non-'succeeded' batch result, empty response, JSON-parse failure, or a stance outside the "
               "five labels is recorded as FAILED; an invalid confidence is set to Medium and an invalid predictive_claim to no. No "
               f"retries. FAILED: 10 of 16,759 retained records overall; {v('COR-22')} of the {v('COR-19')} records published 2021-2025."])
    D.h2("(b) v2 prompt: stricter rubric, sensitivity analysis only")
    D.p(f"Source: classify_stance_batch.py at commit {v2c}; SHA-256 {sha(v2)} ({len(v2)} characters). Its labels were not used for "
        "any primary estimate; they enter only the v2 column of the per-stance trend table (Multimedia Appendix 3).", size=9)
    D.p(v2, mono=True)
    D.p("User message template: identical to (a) (title + full abstract).")
    D.p("Run configuration", bold=True)
    D.bullets(["Model / model string: claude-sonnet-4-6", "API mode: Batch (Anthropic Message Batches API)",
               "Temperature: not set in code; provider default, T = 1.0", "max_tokens: 120", "System prompt: verbatim above (v2)",
               "Input fields: title (full) + full abstract, no truncation",
               "Output fields: stance, confidence, predictive_claim, meta_discourse",
               "Failure handling: as (a); FAILED records are excluded from the v2 shares"])

    # ---------------- Notes 3-7 (verbatim copy) ----------------
    a, b = idx["Supplementary Note 3"], len(paras)
    for p in paras[a:b]:
        if p.text.strip() == "":      # layout spacing only (no content)
            continue
        copy_paragraph(D.d, p)
    MD.append("")

    # ---------------- Note 8 ----------------
    b3 = (R1 / "scripts" / "b3_prompt.txt").read_text()
    assert sha(b3) == B3_SHA
    D.h("Supplementary Note 8. Symmetric-endorsement prompt (R1 sensitivity analysis)")
    D.p(f"Source: revision_r1/scripts/b3_prompt.txt (commit {git('log', '-1', '--format=%H', '--', 'revision_r1/scripts/b3_prompt.txt')}); "
        f"SHA-256 {B3_SHA}, asserted at runtime by b3_endorsement_batch.py. Reproduced verbatim; no text has been edited. The prompt "
        "keeps the Advocacy endorsement criterion of the v1 rubric but drops its transformative-language requirement, so that the "
        "favourable end of the scale is defined symmetrically with the critical end.")
    D.p(b3, mono=True)
    D.p("User message template (the v1 input format): Title: {title} / Abstract: {abstract}, with the Abstract line only when the "
        "abstract is non-empty and no truncation.")
    D.p("Run configuration", bold=True)
    D.bullets(["Model / model string: claude-sonnet-4-6", "API mode: Batch (Anthropic Message Batches API)",
               "Temperature: explicitly set to 0", "max_tokens: 30",
               "Records: every record with production stance Cautious Optimism or Advocacy dated 2021 to April 2026 (10,749)",
               "Output: {\"strong_endorsement\": \"yes\" | \"no\"}; any other output (including prose before the JSON) is FAILED",
               "Retry rule: FAILED records were resubmitted once with identical settings; 7 failed in round 1, 1 was recovered, 6 "
               "stayed FAILED and remain in all denominators, not counted as strong endorsement",
               "Cost gate: exact token count on a 1,000-record sample before submission (ceiling USD 25)"])

    # ---------------- Note 9 ----------------
    pr = (R1 / "coding" / "PROTOCOL_r1_validation.md").read_text()
    D.h("Supplementary Note 9. R1 validation protocol")
    D.p("Design. Two human-coding validations were added in R1: (A1) the concern-theme classifier and (A3) the AI-engagement "
        "prefilter, the latter preceded by a full-abstract re-run of the prefilter on all eligible records (A2). One author (L.W.) "
        "coded both samples. Coding workbooks showed only a row ID, the title and the full abstract; PMID, year, journal, stance, "
        "model labels and sampling stratum were kept in separate key files, never in the workbook. Each codebook is the classifier's "
        "own system prompt, extracted programmatically, with only the machine output-format line omitted.")
    D.bullets([
        "A1 (themes): 200 critical records 2021-2025, 40 per year by simple random sampling within year (numpy default_rng(42)); "
        "frame 4283. Estimands: per-theme precision, recall and F1; micro- and macro-F1, exact match, Hamming loss and Jaccard, "
        "unweighted and weighted to the frame; bootstrap CIs within year (1000, seed 42).",
        "A2 (full-abstract re-run): all 97,492 eligible Q1/Q2 records re-classified with the identical prefilter prompt, model and "
        "settings but the full abstract and no failure default (FAILED, resubmitted once); 0 FAILED.",
        "A3 (prefilter audit): 370 records, stratified by prefilter outcome x year 2021-2025 (excluded by production but kept by the "
        "full-abstract re-run, 15 per year; excluded by both, 45 per year; retained, 10 per year) plus 20 pilot records recoded for "
        "intra-rater agreement. Estimands: false-negative rate among excluded records (1-NPV) by year and pooled, the estimated "
        "number of missed AI-engaged records, PPV among retained records, a population-weighted 2x2 for the production and "
        "full-abstract classifiers (sensitivity, specificity, PPV, NPV, Cohen κ, Gwet AC1), a logistic test of year, and intra-rater "
        "agreement; weights = frame size / sample size per stratum-year cell; borderline-coded records analysed both ways as "
        "sensitivity analyses."])
    f1, f2 = git("log", "-1", "--format=%h %ad", "--date=short", "0d21f6c"), git("log", "-1", "--format=%h %ad", "--date=short", "47cf6fe")
    D.p(f"Freeze commits. Freeze 1 ({f1}): protocol, sampling and re-run scripts, A1 key, manifest and workbook, committed before the "
        f"A1 workbook was released. Freeze 2 ({f2}): A3 key, manifest and workbook, generated after A2 by the unchanged Freeze-1 "
        "script and committed before the A3 workbook was released.")
    D.p("Amendments (all disclosed in the protocol's change log)", bold=True)
    D.table(["Amendment", "Change", "Timing", "Effect on the estimates"], [
        ["1 (A1)", "Primary analysis uses all 200 sampled records; a record with no human theme counts as an empty set (every model "
                   "theme on it is a false positive). The pre-specified rule (exclude such records; N=187) becomes secondary.",
         "Made after the coded sheet was returned and after the pre-specified analysis had been run.",
         f"Conservative: micro-F1 {v('VAL-TH-MICRO-187-UN')} (N=187) -> {v('VAL-TH-MICRO-200-UN')} (N=200)."],
        ["2 (A3)", "An unlabelled audit row counts as an error of the classifier being evaluated (1 of 370 rows); the pre-specified "
                   "rule (exclude) becomes secondary.", "Decided when the sheet was returned, before any A3 result was computed.",
         "Negligible: pooled 1-NPV 5.2% in both analyses; estimated missed records 3747 vs 3740; production sensitivity 78.5% vs "
         "78.6%; full-abstract precision 80.4% vs 81.2%."],
        ["3 (A3)", "Adds Jeffreys intervals for weighted combinations of cells and Clopper-Pearson intervals for single cells, because "
                   "five cells have no variation and the within-cell bootstrap cannot vary them; the bootstrap is kept alongside.",
         "Made after the A3 primary results were known.",
         "CIs only; point estimates unchanged. 25 of 29 intervals widen (all 1-NPV, missed-record and production-prefilter "
         f"intervals); pooled 1-NPV {v('VAL-PF-AUDIT-FNRATEPOOLED')}. Not used for the full-abstract 2x2 (sub-cells too small)."],
    ], widths=[0.8, 2.4, 1.6, 1.8])
    for name, f_ in (("A1 theme-validation workbook", "theme_validation_TEMPLATE.xlsx"),
                     ("A3 prefilter-audit workbook", "prefilter_audit_TEMPLATE.xlsx")):
        ws = load_workbook(R1 / "coding" / f_)["Read me first"]
        text = "\n".join("" if c is None else str(c) for (c,) in ws.iter_rows(min_col=1, max_col=1, values_only=True)).rstrip()
        D.p(f"Verbatim 'Read me first' sheet: {name} (revision_r1/coding/{f_})", bold=True)
        D.p(text, mono=True)

    # ---------------- Note 10 ----------------
    import b6_terms
    D.h("Supplementary Note 10. MeSH and keyword re-fetch and term triangulation (R1)")
    D.p("Re-fetch. On 28 October 2026, MeSH descriptors and author keywords were re-fetched for the 16,759 retained records with "
        "NCBI E-utilities efetch (db=pubmed, retmode=xml; 84 requests of at most 200 PMIDs, at most 3 requests per second; script "
        "revision_r1/scripts/b6_fetch_mesh.py). NCBI returned 16,756 of 16,759 records; the 3 missing PMIDs are listed in "
        "revision_r1/outputs/B6/b6_fetch_missing_pmids.txt. Raw XML is kept locally with a committed SHA-256 manifest.")
    D.table(["Year", "Records with MeSH / with author keywords"], [[str(y), v(f"RES-B6-COMP-{y}")] for y in range(2021, 2026)])
    D.p("Lexicons (verbatim from revision_r1/scripts/b6_terms.py, as pre-specified in ANALYSIS_PLAN_batch2b.md). A record matches a "
        "theme if its title, abstract or author keywords contain a text term (case-insensitive, word boundary; * = any ending) or its "
        "MeSH descriptors include a listed descriptor. Matching is among critical records 2021-2025.")
    D.table(["Lexicon theme", "Text terms", "MeSH descriptors", "Compared with LLM theme"],
            [[k, "; ".join(t), "; ".join(m), lab] for k, (t, m, lab) in b6_terms.LEX.items()])
    D.p(f"Term comparisons. Weighted log-odds ratios with an informative Dirichlet prior (Monroe, Colaresi and Quinn, 2008): for each "
        f"term w, δ_w = log((y_iw + α_w) / (n_i + α0 - y_iw - α_w)) - log((y_jw + α_w) / (n_j + α0 - y_jw - α_w)), with y the number "
        f"of records in each group containing the term (document frequency), n the sum of y over all ranked terms in the group, "
        f"prior α_w = α0 x (the term's share of document frequencies in the background of all 16,759 retained records) and α0 = {b6_terms.ALPHA0:,.0f}; variance σ² = 1/(y_iw + α_w) + 1/(y_jw + α_w); "
        f"z = δ/σ. Terms are MeSH descriptors and author keywords (lower-cased); only terms present in at least {b6_terms.MIN_DF} records "
        "are ranked. Comparisons: records published 2024-2025 vs 2021-2022, and critical vs favourable records, 2021-2025. "
        "The top 30 terms per comparison are tabulated in Multimedia Appendix 3.")

    D.d.save(MA / "Multimedia_Appendix_1_R1.docx")
    (MA / "Multimedia_Appendix_1_R1.md").write_text("\n\n".join(MD) + "\n", encoding="utf-8")
    (MA / "ma1_prompt_hashes.txt").write_text(f"v1 (Note 2a)\t{sha(v1)}\nv1 production 9c79cd5\t{sha(prod_prompt)}\nv2 (Note 2b)\t{sha(v2)}\n"
                                              f"B3 (Note 8)\t{sha(b3)}\n")
    print("MA1 written; v1 hash matches production:", sha(v1) == sha(prod_prompt) == V1_SHA)


if __name__ == "__main__":
    main()
