"""Multimedia Appendix 1 (Supplementary Notes), v3.

Input: revision_r1/final/ma/Multimedia_Appendix_1_R1.{docx,md} (Batch 2c; not modified).
Changes: notes reordered by first citation; headings renumbered; internal codes and
revision wording removed (each replacement asserted); new Note 10 on the
misclassification-corrected prevalence; cross-references resolved to the v3 numbering.
Verbatim prompt text is not touched (it lives in Notes 2-8, which only change heading).
Output: revision_r1/final/v3/ma/Multimedia_Appendix_1_R1_v3.{docx,md}
"""
from __future__ import annotations

import copy
import re

import yaml
from docx import Document
from docx.text.paragraph import Paragraph

from v3_common import AUTHORS, SRC, TITLE_FINAL, V3, resolver

ORDER = yaml.safe_load((V3 / "ma" / "ma_order_v3.yaml").read_text())
NNUM = {u: i for i, u in enumerate(ORDER["ma1_notes"], 1)}
TNUM = {u: i for i, u in enumerate(ORDER["ma2_tables"], 1)}
FNUM = {u: i for i, u in enumerate(ORDER["ma3_figures"], 1)}
RES = resolver(FNUM, TNUM, NNUM, "MA1", jmir=False)   # MA1 holds verbatim prompts: placeholders only, no reformatting
# old note number -> unit id
OLD = {1: "note_data_code", 2: "note_stance_prompts", 3: "note_prefilter_prompt", 4: "note_theme_prompt",
       5: "note_mechanism_prompt", 6: "note_specialty_prompt", 7: "note_forward_validation", 8: "note_endorsement_prompt",
       9: "note_validation_protocol", 10: "note_mesh_keywords"}
TITLE = {"note_data_code": "Data and code availability", "note_prefilter_prompt": "AI-engagement prefilter prompt",
         "note_stance_prompts": "Stance classification prompts",
         "note_endorsement_prompt": "Symmetric-endorsement prompt (sensitivity analysis)",
         "note_theme_prompt": "Ten-theme codebook prompt", "note_mechanism_prompt": "Mechanism (failure-mode × model-type) prompt",
         "note_specialty_prompt": "Specialty classification prompt", "note_forward_validation": "Forward-validation prompts",
         "note_validation_protocol": "Validation protocol for the concern-theme classifier and the prefilter audit",
         "note_correction_estimator": "Misclassification-corrected prevalence",
         "note_mesh_keywords": "MeSH and keyword re-fetch and term triangulation"}
N = lambda u: NNUM[u]

# (old text, new text, expected count) applied to every paragraph and table cell (docx) and to the md
REPL = [
    ("For the R1 revision, all analyses use the 14,058 records", "All analyses use the 14,058 records", 1),
    ("The R1 components are in the repository's revision_r1/ directory; their outputs are listed in the second part of the table.",
     "Components added during peer review are in the repository's revision_r1/ directory and are listed in the second part of the table.", 1),
    ("the sensitivity analyses reported in Tables S3, S4, S6 and S10 (Multimedia Appendix 3) and Figure S2 (Multimedia Appendix 2)",
     "the sensitivity analyses reported in {{T:within_genre}}, {{T:keep_rate}}, {{T:fda_robustness}} and {{T:pubtype}} and in {{F:within_genre_fig}}", 1),
    ("R1 shared helpers and statistics", "Shared helpers and statistics for the revised analyses", 1),
    ("R1 re-analyses of the submitted pipeline (Batch 1)", "Re-analyses of the original pipeline outputs", 1),
    ("Full-abstract prefilter re-run (A2)", "Full-abstract prefilter reclassification", 1),
    ("R1 validation protocol and coding instruments (A1, A3)", "Validation protocol and coding instruments (theme validation, prefilter audit)", 1),
    ("Frozen protocol (Note 9)", f"Frozen protocol (Note {N('note_validation_protocol')})", 1),
    ("R1 validation scoring (A4, B1)", "Validation scoring", 1),
    ("Stance of recovered records (B2)", "Stance of recovered records", 1),
    ("Symmetric endorsement re-classification (B3)", "Symmetric endorsement reclassification", 1),
    ("Strong-endorsement prompt (Note 8)", f"Strong-endorsement prompt (Note {N('note_endorsement_prompt')})", 1),
    ("Multivariable regression (B4)", "Multivariable regression", 1),
    ("SJR medical-category sensitivity (B5)", "SJR medical-category sensitivity", 1),
    ("restricted corpora D1-D3", "three restricted corpora", 1),
    ("MeSH and keyword triangulation (B6)", "MeSH and keyword triangulation", 1),
    ("PubMed re-fetch (Note 10)", f"PubMed re-fetch (Note {N('note_mesh_keywords')})", 1),
    ("Pre-specified R1 analysis plan", "Pre-specified analysis plans", 1),
    ("revision_r1/ANALYSIS_PLAN_batch2b.md", "revision_r1/ANALYSIS_PLAN_batch2b.md; revision_r1/ANALYSIS_PLAN_batch2d.md", 1),
    ("Committed before any Batch 2b computation", "Each committed before the analyses it describes were run", 1),
    ("Numeric corrections (B7)", "Numeric corrections", 1),
    ("Old -> corrected values for the submitted manuscript", "Old and corrected values for numbers changed during peer review", 1),
    ("R1 numbers, figures, tables and appendices", "Numbers, figures, tables and appendices", 1),
    ("revision_r1/final/scripts/c1_*.py to c5_*.py; revision_r1/final/ma/assemble.py; revision_r1/final/NUMBERS_BOOK_R1.csv",
     "revision_r1/final/scripts/c1_*.py to c5_*.py and d1_*.py to d7_*.py; revision_r1/final/v3/scripts/*.py; "
     "revision_r1/final/NUMBERS_BOOK_R1_v2.csv", 1),
    ("Every reported R1 number with its source; figure, table and appendix builders",
     "Every reported number with its source; figure, table and appendix builders; journal cluster-robust trend ORs (d1), "
     "lexicon source decomposition (d2) and period-specific misclassification correction (d3)", 1),
    # Note 3 (stance prompts)
    ("sensitivity analysis of the per-stance trends (Multimedia Appendix 3)", "sensitivity analysis of the per-stance trends ({{T:stance_trend}})", 1),
    ("they enter only the v2 column of the per-stance trend table (Multimedia Appendix 3)",
     "they enter only the v2 column of the per-stance trend table ({{T:stance_trend}})", 1),
    # Note 7 (specialty)
    ("used by the prefilter step (§ Note 3)", f"used by the prefilter step (§ Note {N('note_prefilter_prompt')})", 1),
    # Note 9 (validation protocol)
    ("Design. Two human-coding validations were added in R1: (A1) the concern-theme classifier and (A3) the AI-engagement prefilter, "
     "the latter preceded by a full-abstract re-run of the prefilter on all eligible records (A2).",
     "Design. Two human-coding validations followed a written protocol frozen before coding: the concern-theme classifier and the "
     "AI-engagement prefilter audit, the latter preceded by a full-abstract reclassification of all eligible records by the prefilter.", 1),
    ("A1 (themes): 200 critical records", "Theme validation: 200 critical records", 1),
    ("A2 (full-abstract re-run): all 97,492", "Full-abstract reclassification: all 97,492", 1),
    ("A3 (prefilter audit): 370 records", "Prefilter audit: 370 records", 1),
    ("re-run scripts, A1 key, manifest and workbook, committed before the A1 workbook was released",
     "re-run scripts, theme-validation key, manifest and workbook, committed before the theme-validation workbook was released", 1),
    ("A3 key, manifest and workbook, generated after A2 by the unchanged Freeze-1 script and committed before the A3 workbook was released",
     "prefilter-audit key, manifest and workbook, generated after the full-abstract reclassification by the unchanged Freeze-1 script "
     "and committed before the prefilter-audit workbook was released", 1),
    ("1 (A1)", "1 (themes)", 1), ("2 (A3)", "2 (prefilter audit)", 1), ("3 (A3)", "3 (prefilter audit)", 1),
    ("before any A3 result was computed", "before any audit result was computed", 1),
    ("after the A3 primary results were known", "after the primary audit results were known", 1),
    ("sheet: A1 theme-validation workbook", "sheet: theme-validation workbook", 1),
    ("sheet: A3 prefilter-audit workbook", "sheet: prefilter-audit workbook", 1),
    # Note 11 (MeSH)
    ("The top 30 terms per comparison are tabulated in Multimedia Appendix 3.",
     "The top 30 terms in each direction of each comparison are tabulated in {{T:lexicon_and_terms}}.", 1),
]

NEW_NOTE = [
    "Purpose. Advocacy is rare, and every in-scope disagreement between the stance classifier and the human coder that involved "
    "Advocacy was with Cautious Optimism ({{T:stance_confusion}}). The correction estimates, for each year, the share of records "
    "that the human coder would have assigned to a target label: Advocacy, or critical (Alarm or Caution).",
    "Estimator. For year y and target label h, corrected prevalence = Σ_c s_y(c) × p(h | c), where c runs over the five model stance "
    "labels, s_y(c) is the share of year-y records in the 14,058-record analytic corpus with model label c, and p(h | c) is the share "
    "of stance-validation records with model label c that the coder assigned to h. Because the validation sample was stratified by "
    "model stance (Alarm 40, Caution 60, Neutral 70, Cautious Optimism 100, Advocacy 30), p(h | c) is estimated within each stratum. "
    "Records the coder judged not codable or out of scope count as human Neutral, as in panel (b) of {{T:stance_confusion}}.",
    "Prespecified version (constant rates). p(h | c) is estimated from all 300 validation records and applied to every year, which "
    "assumes that the rates at which model labels convert to human labels did not change over 2021-2025. All records were classified "
    "with the same prompt and settings, each in an independent request. 95% CIs come from 1000 bootstrap draws (seed 42) that "
    "resample validation records within model-label strata and corpus records jointly. These are the estimates reported in the "
    "Results. Code: revision_r1/scripts/t2_stance_perclass.py.",
    "Post hoc version (period-specific rates). Because the validation sample was not stratified by year, p(h | c) was also estimated "
    "separately from the validation records published 2021-2023 and 2024-2025 (253 records; 46 dated 2026 and 1 dated 2020 were "
    "excluded) and applied to the years of the same period. 95% CIs come from 1000 bootstrap draws (seed 42) that resample validation "
    "records within model label and period and corpus records jointly, with a Jeffreys Beta(k+1/2, n-k+1/2) draw for cells with no or "
    "all events. Period differences in p(h | c) were tested with Fisher exact tests. The analysis plan "
    "(revision_r1/ANALYSIS_PLAN_batch2d.md) was committed before the analysis was run. Code: "
    "revision_r1/final/scripts/d3_period_correction.py.",
    "Assumptions and results. All validation records had an abstract, so applying p(h | c) to title-only records assumes that they "
    "are misclassified like abstract-present records. Both versions, the conversion rates by period, and Advocacy precision and "
    "recall by period are in {{T:corrected_prevalence}}.",
]


# ------------------------------------------------------------------ docx
def para_replace(p, old, new):
    """Replace old by new in one paragraph; returns the number of replacements."""
    if old not in p.text:
        return 0
    for r in p.runs:
        if old in r.text:
            k = r.text.count(old)
            r.text = r.text.replace(old, new)
            return k
    full = p.text
    k = full.count(old)
    runs = p.runs
    runs[0].text = full.replace(old, new)
    for r in runs[1:]:
        r._r.getparent().remove(r._r)
    return k


def all_paragraphs(d):
    for p in d.paragraphs:
        yield p
    for t in d.tables:
        for row in t.rows:
            seen = set()
            for c in row.cells:
                if id(c._tc) in seen:
                    continue
                seen.add(id(c._tc))
                for p in c.paragraphs:
                    yield p


def set_text(p, text):
    runs = p.runs
    if runs:
        runs[0].text = text
        for r in runs[1:]:
            r._r.getparent().remove(r._r)
    else:
        p.add_run(text)


def build_docx():
    d = Document(str(SRC / "ma" / "Multimedia_Appendix_1_R1.docx"))
    body = d.element.body
    kids = list(body.iterchildren())
    sect = kids[-1]
    assert sect.tag.endswith("sectPr")
    heads = {}
    for i, el in enumerate(kids):
        if el.tag.endswith("}p"):
            t = Paragraph(el, d).text
            m = re.match(r"Supplementary Note (\d+)\. ", t)
            if m:
                heads[int(m[1])] = i
    assert sorted(heads) == list(range(1, 11)), heads
    pre = kids[:heads[1]]
    blocks = {}
    for k in range(1, 11):
        end = heads[k + 1] if k < 10 else len(kids) - 1
        blocks[OLD[k]] = kids[heads[k]:end]
    # preamble: appendix name, final title, authors (working-title note dropped)
    texts = [Paragraph(e, d).text for e in pre]
    assert texts[0] == "Multimedia Appendix 1. Supplementary Notes" and texts[3].startswith("Working title"), texts
    set_text(Paragraph(pre[1], d), TITLE_FINAL)
    assert Paragraph(pre[2], d).text == AUTHORS
    body.remove(pre[3])
    # new note 10: heading copied from an existing Heading 1, body from a Normal paragraph of Note 1
    h_src = blocks["note_data_code"][0]
    n_src = [e for e in blocks["note_data_code"] if e.tag.endswith("}p") and Paragraph(e, d).style.name == "Normal"][0]
    new = [copy.deepcopy(h_src)] + [copy.deepcopy(n_src) for _ in NEW_NOTE]
    set_text(Paragraph(new[0], d), "Supplementary Note 0. placeholder")
    for e, t in zip(new[1:], NEW_NOTE):
        set_text(Paragraph(e, d), t)
    blocks["note_correction_estimator"] = new
    # detach all note blocks, then append in the new order before sectPr
    for u, els in blocks.items():
        for e in els:
            if e.getparent() is not None:
                body.remove(e)
    for u in ORDER["ma1_notes"]:
        for e in blocks[u]:
            sect.addprevious(e)
        set_text(Paragraph(blocks[u][0], d), f"Supplementary Note {NNUM[u]}. {TITLE[u]}")
    # text replacements
    counts = {o: 0 for o, _, _ in REPL}
    for p in all_paragraphs(d):
        for o, nw, _ in REPL:
            counts[o] += para_replace(p, o, nw)
    bad = {o: c for (o, _, k) in REPL for c in [counts[o]] if c != k}
    if bad:
        raise SystemExit(f"docx replacement counts off: {bad}")
    for p in all_paragraphs(d):
        if "{{" in p.text:
            if any("{{" in r.text and "}}" in r.text for r in p.runs):
                for r in p.runs:
                    r.text = RES(r.text)
            else:
                set_text(p, RES(p.text))
            assert "{{" not in p.text, p.text
    out = V3 / "ma" / "Multimedia_Appendix_1_R1_v3.docx"
    d.save(out)
    return out


# ------------------------------------------------------------------ md
def build_md():
    md = (SRC / "ma" / "Multimedia_Appendix_1_R1.md").read_text(encoding="utf-8")
    parts = re.split(r"(?m)^(?=## Supplementary Note \d+\. )", md)
    pre, notes = parts[0], parts[1:]
    assert len(notes) == 10
    blocks = {}
    for b in notes:
        k = int(re.match(r"## Supplementary Note (\d+)\. ", b)[1])
        blocks[OLD[k]] = re.sub(r"^## Supplementary Note \d+\. [^\n]*", "", b, count=1)
    blocks["note_correction_estimator"] = "\n\n" + "\n\n".join(NEW_NOTE) + "\n\n"
    pre_lines = pre.strip().splitlines()
    assert pre_lines[0] == "**Multimedia Appendix 1. Supplementary Notes**", pre_lines[:2]
    pre = f"**Multimedia Appendix 1. Supplementary Notes**\n\n*{TITLE_FINAL}*\n\n{AUTHORS}\n\n"
    out = pre + "".join(f"## Supplementary Note {NNUM[u]}. {TITLE[u]}" + blocks[u] for u in ORDER["ma1_notes"])
    for o, nw, k in REPL:
        c = out.count(o)
        if c != k:
            raise SystemExit(f"md: '{o[:60]}' found {c}, expected {k}")
        out = out.replace(o, nw)
    out = RES(out)
    path = V3 / "ma" / "Multimedia_Appendix_1_R1_v3.md"
    path.write_text(out, encoding="utf-8")
    return path


if __name__ == "__main__":
    print(build_docx()); print(build_md())
