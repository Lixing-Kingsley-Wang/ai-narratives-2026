"""v3 table units for Multimedia Appendix 2 (supplementary tables).

Starts from the latest Batch 2c/2d unit of each table (<id>_v2.json if present, else <id>.json),
applies the edits listed below and writes revision_r1/final/v3/ma/units/tables/<id>.json.
Edits are wording only (internal codes, revision notes, placeholders for cross-references);
every replacement asserts that its old text exists, so nothing is changed silently.
Two new units: corrected_prevalence (Batch 2d D3 + T2 values from the numbers book) and
lexicon_decomposition (Batch 2d D2 table). Extra rows for lexicon_and_terms come from the
numbers book (RES-B6-EMERG-31..60, RES-B6-STANCE-31..60).
"""
from __future__ import annotations

import json
import re

from scipy.stats import beta

from v3_common import SRC, V3, book, num, write_json

UT_IN = SRC / "ma" / "units" / "tables"
UT = V3 / "ma" / "units" / "tables"
UT.mkdir(parents=True, exist_ok=True)
B = book()
V2_NOTE = ("Version 2 (Batch 2d): every OR per year here comes from record-level logistic regression on publication year "
           "with journal cluster-robust SEs (95% CI and P from the cluster-robust covariance); point estimates are unchanged.")
OR_NOTE = "OR per year: record-level logistic regression on publication year with journal cluster-robust SEs."
LOG = []


def load(uid):
    p = UT_IN / f"{uid}_v2.json"
    src = p if p.exists() else UT_IN / f"{uid}.json"
    s = json.loads(src.read_text(encoding="utf-8"))
    s.setdefault("sub_rows", [])
    s["_source"] = src.name
    return s


def rep(s, field, old, new, row=None, col=None, count=1):
    """Replace text in caption / header / notes / rows, asserting it is present."""
    def sub(text):
        n = text.count(old)
        if n == 0:
            raise SystemExit(f"[{s['id'] if 'id' in s else '?'}] '{old}' not found in {field}")
        if count is not None and n != count:
            raise SystemExit(f"'{old}' found {n} times in {field}, expected {count}")
        return text.replace(old, new)
    if field == "caption":
        s["caption"] = sub(s["caption"])
    elif field == "header":
        hits = [i for i, h in enumerate(s["header"]) if old in h]
        if not hits:
            raise SystemExit(f"'{old}' not in header")
        for i in hits:
            s["header"][i] = s["header"][i].replace(old, new)
    elif field == "notes":
        hits = [i for i, x in enumerate(s["notes"]) if old in x]
        if len(hits) != 1:
            raise SystemExit(f"'{old}' in {len(hits)} notes")
        s["notes"][hits[0]] = sub(s["notes"][hits[0]])
    elif field == "rows":
        hits = [(i, j) for i, r in enumerate(s["rows"]) for j, c in enumerate(r) if old in str(c)
                and (row is None or i == row) and (col is None or j == col)]
        if not hits:
            raise SystemExit(f"'{old}' not in rows")
        if count is not None and len(hits) != count:
            raise SystemExit(f"'{old}' in {len(hits)} cells, expected {count}")
        for i, j in hits:
            s["rows"][i][j] = str(s["rows"][i][j]).replace(old, new)
    LOG.append((s["_uid"], field, old, new))


def drop_v2_note(s, replace=True):
    assert V2_NOTE in s["notes"], s["_uid"]
    i = s["notes"].index(V2_NOTE)
    if replace:
        s["notes"][i] = OR_NOTE
    else:
        s["notes"].pop(i)
    LOG.append((s["_uid"], "notes", "Version 2 (Batch 2d) note", OR_NOTE if replace else "(removed)"))


def insert_rows(s, at, new_rows, sub=False):
    """Insert rows before index `at`, shifting group/sub row indices."""
    s["rows"][at:at] = new_rows
    k = len(new_rows)
    s["group_rows"] = [g + k if g >= at else g for g in s["group_rows"]]
    s["sub_rows"] = [g + k if g >= at else g for g in s["sub_rows"]]
    if sub:
        s["sub_rows"] += list(range(at, at + k))
    LOG.append((s["_uid"], "rows", f"insert {k} row(s) at {at}", "; ".join(" | ".join(r) for r in new_rows)))


def replace_row(s, i, new_rows):
    old = s["rows"][i]
    assert i not in s["group_rows"]
    s["rows"][i:i + 1] = new_rows
    k = len(new_rows) - 1
    s["group_rows"] = [g + k if g > i else g for g in s["group_rows"]]
    s["sub_rows"] = [g + k if g > i else g for g in s["sub_rows"]]
    LOG.append((s["_uid"], "rows", " | ".join(old), " || ".join(" | ".join(r) for r in new_rows)))


def save(uid, s):
    s.pop("_source", None); s.pop("_uid", None)
    s["id"] = uid
    write_json(UT / f"{uid}.json", s)


# ----------------------------------------------------------------- edits to existing units
def edits():
    E = {}

    def u(uid):
        s = load(uid); s["_uid"] = uid; E[uid] = s; return s

    s = u("advocacy_by_specialty")
    rep(s, "rows", "nan% of 0", "N/A, no records")

    s = u("corpus_sensitivity")
    rep(s, "caption", "alternative corpora (B2), 2021-2025", "alternative corpora, 2021-2025")
    drop_v2_note(s)

    u("country")

    s = u("ea_vs_nawe_within_specialty")
    rep(s, "notes", " (run_east_asia_diagnose.py rule)", "")

    s = u("fda_mapping")
    rep(s, "caption", " (unchanged)", "")
    rep(s, "notes", "Counts are not corpus-dependent and are unchanged from the submission.", "Counts do not depend on the corpus.")

    u("fda_robustness")

    s = u("fv_tier_verdict")
    rep(s, "caption", " (unchanged)", "")
    rep(s, "notes", " (the evidence window predates the 2021-2025 analytic decision and is unchanged)", "")

    s = u("keep_rate")
    rep(s, "notes", "Spearman ρ ρ=", "Spearman ρ=")
    rep(s, "notes", "The R1 prefilter audit estimates", "The prefilter audit estimates")
    drop_v2_note(s)

    s = u("lexicon_and_terms")
    rep(s, "caption", "theme trends (B6), 2021-2025", "theme trends, 2021-2025")
    rep(s, "notes", "re-fetched from PubMed for the analytic records (Multimedia Appendix 1, Note 10)",
        "re-fetched from PubMed for the retained records ({{N:note_mesh_keywords}})")
    rep(s, "notes", "(verbatim in Note 10)", "(verbatim in {{N:note_mesh_keywords}})")
    rep(s, "notes", "(c-d) Weighted log-odds ratio", "(c-f) Weighted log-odds ratio")
    rep(s, "notes", "records = documents containing the term in each group.",
        "records = documents containing the term in each group (2024-2025 vs 2021-2022 in (c) and (e); critical vs "
        "favourable in (d) and (f)); a negative z in (e) or (f) means the term was relatively more frequent in "
        "2021-2022 or in favourable records.")
    drop_v2_note(s)
    for tag, title in (("EMERG", "(e) Terms most over-represented in 2021-2022 vs 2024-2025 (top 30)"),
                       ("STANCE", "(f) Terms most over-represented in favourable vs critical records (top 30)")):
        new = [[title, "", "", ""]]
        for i in range(31, 61):
            r = B[f"RES-B6-{tag}-{i:02d}"]
            term = r["item"].split(": ", 1)[1]
            parts = r["value"].split("; ")
            assert len(parts) == 4 and parts[0].startswith("z=-") and parts[2].startswith("records "), r["value"]
            new.append([term, parts[0], parts[1], parts[2]])
        at = len(s["rows"])
        s["rows"] += new
        s["group_rows"].append(at)
        LOG.append(("lexicon_and_terms", "rows", f"append panel {title[:3]}", f"30 terms from RES-B6-{tag}-31..60"))
    s.setdefault("book_ids", [])
    s["book_ids"] += [f"RES-B6-{t}-{i:02d}" for t in ("EMERG", "STANCE") for i in range(31, 61)]

    s = u("mechanism_confusion")
    # (c) class-specific precision, recall and F1, computed from panels (a) and (b) of this table; F1 values checked
    # against the committed T3 per-class F1 (Batch 1): 0.47, 0.69, 0.63, 0.82 and 0.98, 0.85, 0.75, 0.77.
    T3_F1 = {"confabulation": 0.47, "misclassification": 0.69, "both (a)": 0.63, "none or unclear": 0.82,
             "generative": 0.98, "discriminative": 0.85, "both (b)": 0.75, "unclear": 0.77}
    rows0 = [r[:] for r in s["rows"]]
    new_rows = [["(c) Class-specific agreement (model label against human code)", "", "", "", "", ""],
                ["Class", "Precision, % (k/n; exact 95% CI)", "Recall, % (k/n; exact 95% CI)", "F1", "", ""]]
    for panel, start, names in (("a", 1, ["confabulation", "misclassification", "both", "none or unclear"]),
                                ("b", 6, ["generative", "discriminative", "both", "unclear"])):
        M = [[int(x) for x in rows0[start + i][1:5]] for i in range(4)]
        assert [r[0] for r in rows0[start:start + 4]] == [f"Human: {n}" for n in names], rows0[start:start + 4]
        for k, nm in enumerate(names):
            tp = M[k][k]; col = sum(M[i][k] for i in range(4)); row = sum(M[k])
            pr, rc = tp / col, tp / row
            f1 = 2 * pr * rc / (pr + rc)
            key = nm if nm != "both" else f"both ({panel})"
            assert abs(round(f1, 2) - T3_F1[key]) < 0.006, (key, f1)
            lab = {"confabulation": "Fabrication (confabulation)", "misclassification": "Factual error (misclassification)",
                   "both": "Both", "none or unclear": "None or unclear", "generative": "Generative",
                   "discriminative": "Discriminative", "unclear": "Unclear"}[nm]
            ax = "failure mode" if panel == "a" else "model type"
            new_rows.append([f"{lab}, {ax}", cell(tp, col), cell(tp, row), f"{f1:.2f}", "", ""])
    at = len(s["rows"])
    s["rows"] += new_rows
    s["group_rows"].append(at)
    s["sub_rows"] = s.get("sub_rows", []) + [at + 1]
    s["notes"].append("(c) Precision: share of records with the model label that the coder gave the same label; recall: share "
                      "of records with the human code that the model gave the same label; both computed from panels (a) and (b). "
                      "F1 is their harmonic mean (point estimate).")
    LOG.append(("mechanism_confusion", "rows", "append panel (c)", "class-specific precision, recall, F1 from panels (a)-(b)"))

    s = u("missing_data")
    rep(s, "rows", "of which: prefilter failures defaulted to application (T1)", "of which: prefilter failures defaulted to application")
    rep(s, "rows", "First-author country (Figure 4 / Table S7 resolver)", "First-author country")
    rep(s, "rows", "First-author region (Table S9; geography_classifications.csv)", "First-author region")
    rep(s, "rows", "Unknown region is kept as its own level in regression (B4).", "Unknown region is kept as its own level in regression.")
    for old, new in (("raw (116,117)", "Raw records"), ("excluded conf/preprint", "Conference proceedings or preprints"),
                     ("SJR unmatched", "Not matched in SJR"), ("Q1/Q2 eligible (97,492)", "Q1/Q2 eligible"),
                     ("prefilter: application", "Prefilter: application"), ("prefilter: retained (16,759)", "Prefilter: retained"),
                     ("stance valid, 2021–2026 (16,747)", "Valid stance"), ("critical (5,161)", "Critical")):
        rep(s, "rows", old, new, col=0)

    u("precision")

    s = u("prefilter_validation")
    rep(s, "caption", "development pilot and R1 audit.", "development pilot and audit.")
    rep(s, "rows", "(b) R1 audit design", "(b) Audit design")
    rep(s, "rows", "(c) R1 audit estimates", "(c) Audit estimates")
    rep(s, "notes", "(b-f) R1 audit (frozen protocol, Multimedia Appendix 1, Note 9)",
        "(b-f) Audit (frozen protocol, {{N:note_validation_protocol}})")
    insert_rows(s, 1, [["Human code \\ model label", "Discourse", "Evaluative", "Application", "Row total"]], sub=True)
    s["notes"].append("Prespecified logistic test of year on the human label (KEEP) within the excluded strata, adjusted for "
                      "stratum: OR 1.263 per year (Wald 95% CI 0.898-1.776), P=.18; design-weighted OR 1.267 (bootstrap 95% CI "
                      "0.940-1.760). Source: revision_r1/REPORT_A3_prefilter_scoring.md.")
    LOG.append(("prefilter_validation", "notes", "append", "logistic test of year (REPORT_A3)"))

    u("pubtype")

    s = u("q3_arm")
    rep(s, "notes", "Spearman ρ ρ=", "Spearman ρ=")
    drop_v2_note(s)

    s = u("region")
    rep(s, "notes", "Regions from the first-author country (geography_classifications.csv); ", "Regions from the first-author country; ")

    s = u("regression_full")
    r1 = s["rows"][1]
    assert r1[0] == "Year, per 1 year" and r1[1].startswith("OR 1.077") and r1[2].startswith("OR 1.103"), r1
    replace_row(s, 1, [["Year, per 1 year: unadjusted OR", r1[1], "", ""],
                       ["Year, per 1 year: adjusted OR", r1[2].replace(" per year", ""), "", ""]])
    n_pub = sum(1 for r in s["rows"] if str(r[0]).find("pubtype: ") >= 0)
    rep(s, "rows", "pubtype: ", "publication type: ", col=0, count=n_pub)
    n_cty = sum(1 for r in s["rows"] if str(r[0]).find("country_g: ") >= 0)
    rep(s, "rows", "country_g: ", "country: ", col=0, count=n_cty)

    s = u("review_subtypes")
    rep(s, "rows", "Review (narrative)", "Review (non-systematic)")
    rep(s, "notes", "Subtype rule: PubMed Publication Type substring precedence (analysis/robustness.py::simplify_pubtype_7): ",
        "Subtype rule: PubMed Publication Type substring precedence: ")
    rep(s, "notes", "= narrative subtype", "= non-systematic subtype")

    s = u("run_to_run")
    rep(s, "caption", " (unchanged)", "")
    rep(s, "notes", "Clopper-Pearson for raw agreement (CIs added in R1).", "Clopper-Pearson for raw agreement.")

    s = u("sjr_sensitivity")
    rep(s, "caption", "medical-category restriction (B5), 2021-2025", "medical-category restriction, 2021-2025")
    rep(s, "header", "D1 Medicine area (primary)", "Medicine area (primary)")
    rep(s, "header", "D2 D1 minus Medicine (miscellaneous)", "Medicine area without Medicine (miscellaneous)")
    rep(s, "header", "D3 broad health sciences", "Broad health sciences")
    rep(s, "notes", "D1 (primary): any Medicine-area (ASJC 27xx) category. D2: D1 without 'Medicine (miscellaneous)'. D3: broad health sciences",
        "Medicine area (primary): any Medicine-area (ASJC 27xx) category. Medicine area without Medicine (miscellaneous): the "
        "primary definition without the 'Medicine (miscellaneous)' category. Broad health sciences")
    drop_v2_note(s)

    s = u("specialty_definitions")
    rep(s, "header", "Verbatim definition text from SPECIALTY_PROMPT", "Verbatim definition text from the classification prompt")
    old = s["notes"][0]
    assert old.startswith("Definitions are reproduced exactly as in the submitted Table S16") and len(s["notes"]) == 1, old
    s["notes"][0] = ("Definitions are reproduced exactly as in the specialty classification prompt ({{N:note_specialty_prompt}}), "
                     "including the disambiguation rules. The final column counts records with a valid specialty label in the "
                     "2021-2025 analytic corpus.")
    LOG.append(("specialty_definitions", "notes", old, s["notes"][0]))

    u("stance_confusion")

    s = u("stance_trend")
    rep(s, "notes", "(Multimedia Appendix 1, Note 2b)", "({{N:note_stance_prompts}}, part b)")
    drop_v2_note(s, replace=False)

    s = u("symmetric_endorsement")
    rep(s, "caption", "for strong endorsement (B3), 2021-2025", "for strong endorsement, 2021-2025")
    rep(s, "notes", "(verbatim in Multimedia Appendix 1, Note 8)", "(verbatim in {{N:note_endorsement_prompt}})")
    drop_v2_note(s)

    u("theme_by_format")

    s = u("theme_validation")
    rep(s, "notes", "(frozen protocol, Multimedia Appendix 1, Note 9)", "(frozen protocol, {{N:note_validation_protocol}})")
    names = {"safety_clinical": "Patient safety", "hallucination": "Hallucination / errors", "regulation": "Governance / regulation",
             "ethics_bias": "Ethics & bias", "education": "Medical education", "data_privacy": "Data privacy",
             "cognitive": "Cognitive offloading", "existential": "Existential threat", "replacement": "Replacement fears",
             "other": "Other"}
    for code, name in names.items():
        k = sum(1 for r in s["rows"] if re.match(rf"{code}\b", str(r[0])))
        assert k == 2, (code, k)
        for r in s["rows"]:
            if re.match(rf"{code}\b", str(r[0])):
                rest = str(r[0])[len(code):]
                r[0] = f"{name} ({code}; {rest[2:]}" if rest.startswith(" (") else f"{name} ({code}){rest}"
        LOG.append(("theme_validation", "rows", code, f"{name} ({code})"))

    s = u("themes")
    rep(s, "notes", "Annual values with CIs for every year are in the R1 numbers book; the six lower-prevalence themes are plotted in "
        "{{F:other_themes_fig}} and annual counts in {{F:theme_counts_fig}}.",
        "Annual values with 95% CIs are plotted in Figure 2 (headline themes) and {{F:other_themes_fig}} (other themes); "
        "annual counts are in {{F:theme_counts_fig}}.")
    drop_v2_note(s)

    u("update_2026")

    s = u("within_genre")
    rep(s, "notes", "Spearman ρ ρ=", "Spearman ρ=", count=2)
    rep(s, "notes", "; point estimates are unchanged from the submitted Table S3", "")
    drop_v2_note(s)
    return E


# ----------------------------------------------------------------- new unit: corrected_prevalence
def cp(k, n):
    lo = 0.0 if k == 0 else beta.ppf(0.025, k, n - k + 1)
    hi = 1.0 if k == n else beta.ppf(0.975, k + 1, n - k)
    return lo * 100, hi * 100


def cell(k, n, flag=""):
    lo, hi = cp(k, n)
    return f"{100 * k / n:.1f} ({k}/{n}; {lo:.1f}-{hi:.1f}){flag}"


def book_cell(id_):
    """'0.0% (0/7; exact Clopper-Pearson 0.0%-41.0%) [fewer than 10 validation records]' -> '0.0 (0/7; 0.0-41.0)*'."""
    v = B[id_]["value"]
    m = re.fullmatch(r"([\d.]+)% \((\d+)/(\d+); exact Clopper-Pearson ([\d.]+)%-([\d.]+)%\)( \[fewer than 10 validation records\])?", v)
    assert m, v
    return f"{m[1]} ({m[2]}/{m[3]}; {m[4]}-{m[5]})" + ("*" if m[6] else ""), int(m[2]), int(m[3])


def corr_vals(id_):
    v = B[id_]["value"]
    pat = r"(-?[\d.]+)(?:%| percentage points) \(95% CI (-?[\d.]+)%?(?: to |-)(-?[\d.]+)%?\)"
    m = re.fullmatch(r"period-specific " + pat + r"; constant-rate \(T2, pre-specified\) " + pat, v)
    assert m, v
    fmt = lambda a, b, c: f"{a} ({b} to {c})" if (b.startswith("-") or c.startswith("-")) else f"{a} ({b}-{c})"
    return fmt(m[4], m[5], m[6]), fmt(m[1], m[2], m[3])          # constant, period-specific


# pooled counts (all 300 validation records) from the stance confusion matrix, panel (b)
def pooled_from_confusion():
    s = json.loads((UT_IN / "stance_confusion.json").read_text(encoding="utf-8"))
    i0 = [r[0] for r in s["rows"]].index("(b) All 300 validation records")
    M = {}
    for r in s["rows"][i0 + 1:i0 + 6]:
        h = r[0].replace("Human: ", "")
        M[h] = [int(x) for x in r[1:6]]
    S = ["Alarm", "Caution", "Neutral", "Cautious Optimism", "Advocacy"]
    col = {m: sum(M[h][j] for h in S) for j, m in enumerate(S)}
    adv = {m: M["Advocacy"][j] for j, m in enumerate(S)}
    crit = {m: M["Alarm"][j] + M["Caution"][j] for j, m in enumerate(S)}
    assert col == {"Alarm": 40, "Caution": 60, "Neutral": 70, "Cautious Optimism": 100, "Advocacy": 30}, col
    s_a = json.loads((UT_IN / "stance_confusion.json").read_text(encoding="utf-8"))
    ia = [r[0] for r in s_a["rows"]].index("(a) In-scope records (n=225)")
    MA = {r[0].replace("Human: ", ""): [int(x) for x in r[1:6]] for r in s_a["rows"][ia + 1:ia + 6]}
    adv_col_in = sum(MA[h][4] for h in S)
    return S, col, adv, crit, M, MA, adv_col_in


def check_constant_rates(S, col, adv, crit):
    """The pooled rates must reproduce the T2 constant-rate estimates printed in the book."""
    for y in (2021, 2022, 2023, 2024, 2025):
        n = {}
        for st, key in zip(S, ("ALARM", "CAUT", "NEUT", "CO", "ADV")):
            r = B[f"RES-TMP-{key}-{y}"]
            n[st] = int(float(r["k"])); N = int(float(r["n"]))
        assert sum(n.values()) == N, (y, n, N)
        a = sum(n[st] / N * adv[st] / col[st] for st in S) * 100
        c = sum(n[st] / N * crit[st] / col[st] for st in S) * 100
        const_a = float(re.search(r"constant-rate \(T2, pre-specified\) ([\d.]+)%", B[f"VAL-ST-PER-CORR-ADVOCACY-{y}"]["value"])[1])
        const_c = float(re.search(r"constant-rate \(T2, pre-specified\) ([\d.]+)%", B[f"VAL-ST-PER-CORR-CRITICAL-{y}"]["value"])[1])
        assert abs(round(a, 2) - const_a) < 0.006 and abs(round(c, 2) - const_c) < 0.006, (y, a, const_a, c, const_c)
    return True


def corrected_prevalence():
    S, col, adv, crit, M, MA, adv_col_in = pooled_from_confusion()
    check_constant_rates(S, col, adv, crit)
    rows, groups, subs = [], [], []
    groups.append(len(rows)); rows.append(["(a) Corrected prevalence by year, % (95% CI)", "", "", "", ""])
    subs.append(len(rows)); rows.append(["Year", "Advocacy: constant rates (prespecified)", "Advocacy: period-specific rates (post hoc)",
                                         "Critical: constant rates (prespecified)", "Critical: period-specific rates (post hoc)"])
    ids = []
    for y in (2021, 2022, 2023, 2024, 2025):
        ca, pa = corr_vals(f"VAL-ST-PER-CORR-ADVOCACY-{y}"); cc, pc = corr_vals(f"VAL-ST-PER-CORR-CRITICAL-{y}")
        rows.append([str(y), ca, pa, cc, pc]); ids += [f"VAL-ST-PER-CORR-ADVOCACY-{y}", f"VAL-ST-PER-CORR-CRITICAL-{y}"]
    ca, pa = corr_vals("VAL-ST-PER-CORR-ADVOCACY-DELTA"); cc, pc = corr_vals("VAL-ST-PER-CORR-CRITICAL-DELTA")
    rows.append(["Change, 2025 minus 2021, percentage points", ca, pa, cc, pc])
    ids += ["VAL-ST-PER-CORR-ADVOCACY-DELTA", "VAL-ST-PER-CORR-CRITICAL-DELTA"]

    groups.append(len(rows)); rows.append(["(b) Conversion rates: validation records with each model label that the coder labelled "
                                           "Advocacy or critical, % (k/n; exact 95% CI)", "", "", "", ""])
    subs.append(len(rows)); rows.append(["Model label: human label", "All years (constant rates)", "2021-2023", "2024-2025",
                                         "Period difference, Fisher exact P"])
    key = {"Alarm": "ALARM", "Caution": "CAUTION", "Neutral": "NEUTRAL", "Cautious Optimism": "CAUTIOUSOPTIMISM", "Advocacy": "ADVOCACY"}
    for st in S:
        for tgt, cnt, tk in (("Advocacy", adv, "ADVOCACY"), ("critical", crit, "CRITICAL")):
            c1, k1, n1 = book_cell(f"VAL-ST-PER-CONV-{key[st]}-{tk}-P1")
            c2, k2, n2 = book_cell(f"VAL-ST-PER-CONV-{key[st]}-{tk}-P2")
            assert k1 + k2 <= cnt[st] + 47 and n1 + n2 <= col[st], (st, tgt)
            fp = B[f"VAL-ST-PER-FISHER-{key[st]}-{tk}"]["value"].replace("Fisher exact two-sided ", "")
            rows.append([f"Model {st}: human {tgt}", cell(cnt[st], col[st]), c1, c2, fp])
            ids += [f"VAL-ST-PER-CONV-{key[st]}-{tk}-P1", f"VAL-ST-PER-CONV-{key[st]}-{tk}-P2", f"VAL-ST-PER-FISHER-{key[st]}-{tk}"]

    groups.append(len(rows)); rows.append(["(c) Advocacy precision and recall, % (k/n; exact 95% CI)", "", "", "", ""])
    subs.append(len(rows)); rows.append(["Measure", "All years", "2021-2023", "2024-2025", ""])
    hum_adv_all = sum(M["Advocacy"]); hum_adv_in = sum(MA["Advocacy"])
    pooled = {("PREC", "ALL"): (adv["Advocacy"], col["Advocacy"]), ("REC", "ALL"): (M["Advocacy"][4], hum_adv_all),
              ("PREC", "INSCOPE"): (MA["Advocacy"][4], adv_col_in), ("REC", "INSCOPE"): (MA["Advocacy"][4], hum_adv_in)}
    assert pooled[("PREC", "INSCOPE")] == (17, 26) and pooled[("REC", "INSCOPE")] == (17, 24), pooled
    for lab, m, sc in (("Precision, all 300 records", "PREC", "ALL"), ("Recall, all 300 records", "REC", "ALL"),
                       ("Precision, 225 in-scope records", "PREC", "INSCOPE"), ("Recall, 225 in-scope records", "REC", "INSCOPE")):
        c1, _, _ = book_cell(f"VAL-ST-PER-ADV-{m}-{sc}-P1"); c2, _, _ = book_cell(f"VAL-ST-PER-ADV-{m}-{sc}-P2")
        rows.append([lab, cell(*pooled[(m, sc)]), c1, c2, ""])
        ids += [f"VAL-ST-PER-ADV-{m}-{sc}-P1", f"VAL-ST-PER-ADV-{m}-{sc}-P2"]
    meta = B["VAL-ST-PER-META"]["value"]
    assert meta.startswith("253 of 300; excluded by publication year: 46 dated 2026 and 1 dated 2020"), meta
    notes = [
        "Corrected prevalence for a year = sum over the five model-stance labels of (share of that year's records with the model "
        "label) x (share of validation records with that model label that the coder assigned the target label) "
        "({{N:note_correction_estimator}}). Target labels: Advocacy; critical (Alarm or Caution). Corpus: 14,058 records, 2021-2025.",
        "Constant rates (prespecified): rates from all 300 stance-validation records, applied to every year; records the coder judged "
        "not codable or out of scope count as human Neutral, as in {{T:stance_confusion}}. 95% CIs: 1000 bootstrap draws (seed 42) "
        "resampling validation records within model label and corpus records jointly. These are the estimates reported in the Results.",
        "Period-specific rates (post hoc): rates estimated separately from the 253 validation records published 2021-2023 or 2024-2025 "
        "(46 dated 2026 and 1 dated 2020 excluded) and applied to the years of the same period. 95% CIs: 1000 bootstrap draws (seed 42) "
        "resampling validation records within model label and period and corpus records jointly, with a Jeffreys Beta(k+1/2, n-k+1/2) "
        "draw for cells with no or all events. The validation sample was stratified by model stance, not by year, so period cells are "
        "small; * marks the one cell with fewer than 10 records.",
        "(b) and (c): exact Clopper-Pearson 95% CIs; Fisher exact two-sided test of the period difference within each model label. "
        "'All years' uses all 300 validation records, including the 47 dated outside 2021-2025 (counts from {{T:stance_confusion}}). "
        "Precision: share of model-Advocacy records the coder labelled Advocacy; recall: share of coder-Advocacy records the model "
        "labelled Advocacy; in scope: the 225 records the coder judged codable and in scope.",
        "The post hoc analysis followed a written plan committed to the repository before it was run ({{N:note_data_code}}). "
        "Critical stance was Alarm or Caution.",
    ]
    s = {"id": "corrected_prevalence", "caption": "Misclassification-corrected prevalence of Advocacy and critical stance: prespecified "
         "constant-rate correction and post hoc period-specific correction, 2021-2025.",
         "header": ["Item", "Column 1", "Column 2", "Column 3", "Column 4"], "rows": rows, "notes": notes,
         "group_rows": groups, "sub_rows": subs, "landscape": True, "book_ids": ids + ["VAL-ST-PER-META"] +
         [f"RES-TMP-{k}-{y}" for k in ("ALARM", "CAUT", "NEUT", "CO", "ADV") for y in (2021, 2022, 2023, 2024, 2025)]}
    write_json(UT / "corrected_prevalence.json", s)
    LOG.append(("corrected_prevalence", "new", "Batch 2d D3 table + T2 constant-rate values", f"{len(rows)} rows"))


# ----------------------------------------------------------------- new unit: lexicon_decomposition
def lexicon_decomposition():
    md = (SRC / "ma" / "new_tables" / "MA3_lexicon_decomposition.md").read_text(encoding="utf-8").splitlines()
    tab = [l for l in md if l.startswith("|")]
    hdr = [c.strip() for c in tab[0].strip("|").split("|")]
    assert hdr == ["Source or term", "2021", "2022", "2023", "2024", "2025", "OR per year (95% CI); P"], hdr
    rows, groups = [], []
    for l in tab[2:]:
        cells = [c.strip() for c in re.split(r"(?<!\\)\|", l.strip()[1:-1])]
        cells = [c.replace("*P*", "P").replace("\\|", "|") for c in cells]
        if cells[0].startswith("**") and all(c == "" for c in cells[1:]):
            groups.append(len(rows)); cells[0] = cells[0].strip("*")
        rows.append(cells)
    # spot-check against the numbers book
    assert rows[[r[0] for r in rows].index("(d) Classifier input (title + first 400 abstract characters)")][6] == "1.000 (0.903-1.107); P=.995"
    ho = [r for r in rows if r[0].strip() == "term 'human oversight' (title + abstract)"][0]
    assert ho[4] == "0.7 (0.3-1.1); 8/1228" and ho[5] == "3.2 (2.4-4.0); 58/1828", ho
    notes = [
        "Post hoc analysis; its plan was committed to the repository before the analysis was run ({{N:note_data_code}}). Critical "
        "records (Alarm or Caution) 2021-2025, n=4283. Lexicons, word-boundary matching and MeSH matching are those of the "
        "prespecified lexicon analysis ({{N:note_mesh_keywords}}). Row (a) reproduces the lexicon series in {{T:lexicon_and_terms}} "
        "exactly, and (a) is the union of (b) and (c) for every record. Rows (d) and (e) split the title + abstract text at the 400th "
        "abstract character, the input limit of the concern-theme classifier; a term that straddles character 400 is counted in neither.",
        "Cells: % (95% CI); n/N, with N = critical records of that year (2021 270; 2022 333; 2023 624; 2024 1228; 2025 1828). CIs: 95% "
        "percentile bootstrap, 1000 joint resamples of records, seed 42. OR per year: record-level logistic regression on publication "
        "year with journal cluster-robust SEs (1215 journals).",
        "Cells with no or all events show the exact Clopper-Pearson interval ('exact'). Single-term rows use the title + abstract text "
        "of row (b); 'human oversight' is an added phrase, not a lexicon term. Critical stance was Alarm or Caution.",
    ]
    src_notes = "\n".join(md)
    for frag in ("a term that straddles character 400 is counted in neither", "(1215 journals)", "'human oversight' is an added phrase"):
        assert frag in src_notes, frag
    s = {"id": "lexicon_decomposition", "caption": "Post hoc source decomposition of the lexicon mention shares among critical records, "
         "2021-2025.", "header": ["Source or term", "2021, % (95% CI); n/N", "2022, % (95% CI); n/N", "2023, % (95% CI); n/N",
                                  "2024, % (95% CI); n/N", "2025, % (95% CI); n/N", "OR per year (95% CI); P"],
         "rows": rows, "notes": notes, "group_rows": groups, "sub_rows": [], "landscape": True,
         "source": "revision_r1/final/ma/new_tables/MA3_lexicon_decomposition.md (Batch 2d D2)"}
    write_json(UT / "lexicon_decomposition.json", s)
    LOG.append(("lexicon_decomposition", "new", "Batch 2d D2 table", f"{len(rows)} rows, {len(groups)} groups"))


def main():
    E = edits()
    for uid, s in E.items():
        save(uid, s)
    corrected_prevalence()
    lexicon_decomposition()
    with open(V3 / "ma" / "units_v3_edit_log.tsv", "w", encoding="utf-8") as f:
        f.write("unit\tfield\told\tnew\n")
        for r in LOG:
            f.write("\t".join(str(x).replace("\t", " ").replace("\n", " ") for x in r) + "\n")
    print(f"{len(E)} edited units + 2 new; {len(LOG)} logged edits")


if __name__ == "__main__":
    main()
