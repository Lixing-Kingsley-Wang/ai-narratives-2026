"""Main-text Tables 1-3, v3: same values as the Batch 2c/2d tables; internal codes, revision
notes and defensive notes removed; Multimedia Appendix references resolved to the v3 numbering.

Input: revision_r1/final/tables/Table1.md, Table2_v2.md, Table3_v2.md (not modified).
Output: revision_r1/final/v3/tables/Table{1,2,3}_v3.{md,docx}
"""
from __future__ import annotations

import re

import yaml
from docx.enum.section import WD_ORIENT

from v3_common import SRC, V3, add_runs, md_table, md_text, new_doc, para, resolver, table

ORDER = yaml.safe_load((V3 / "ma" / "ma_order_v3.yaml").read_text())
RES = resolver({u: i for i, u in enumerate(ORDER["ma3_figures"], 1)}, {u: i for i, u in enumerate(ORDER["ma2_tables"], 1)},
               {u: i for i, u in enumerate(ORDER["ma1_notes"], 1)}, "MAIN")
OUT = V3 / "tables"; OUT.mkdir(parents=True, exist_ok=True)


def parse(path):
    lines = path.read_text(encoding="utf-8").split("\n")
    cap = re.fullmatch(r"\*\*(.+)\*\*", lines[0].strip())[1]
    tab = [l for l in lines if l.startswith("|")]
    i_end = max(i for i, l in enumerate(lines) if l.startswith("|"))
    notes = [l.strip() for l in lines[i_end + 1:] if l.strip()]

    def cells(l):
        parts = re.split(r"(?<!\\)\|", l)[1:-1]
        out = []
        for c in parts:
            c = c[1:] if c.startswith(" ") else c
            c = c.rstrip().replace("\\|", "|").replace("*P*", "P")
            out.append(c)
        return out
    header = cells(tab[0])
    rows, groups = [], []
    for l in tab[2:]:
        c = cells(l)
        if c[0].startswith("**") and c[0].endswith("**") and all(x == "" for x in c[1:]):
            groups.append(len(rows)); c[0] = c[0].strip("*")
        rows.append(c)
    notes = [n.replace("*P*", "P") for n in notes]
    return {"caption": cap, "header": header, "rows": rows, "group_rows": groups, "notes": notes}


def rep_list(lst, old, new, count=1):
    hits = [i for i, x in enumerate(lst) if old in x]
    assert len(hits) == count, (old, len(hits))
    for i in hits:
        lst[i] = lst[i].replace(old, new)


def rep_rows(t, old, new, count=1):
    hits = [(i, j) for i, r in enumerate(t["rows"]) for j, c in enumerate(r) if old in c]
    assert len(hits) == count, (old, hits)
    for i, j in hits:
        t["rows"][i][j] = t["rows"][i][j].replace(old, new)


def drop_note(t, startswith):
    hits = [i for i, x in enumerate(t["notes"]) if x.startswith(startswith)]
    assert len(hits) == 1, startswith
    t["notes"].pop(hits[0])


def table1():
    t = parse(SRC / "tables" / "Table1.md")
    rep_rows(t, "Prefilter, R1 audit", "Prefilter, audit")
    rep_rows(t, "frozen protocol (Multimedia Appendix 1, Note 9)", "frozen protocol ({{N:note_validation_protocol}})")
    rep_list(t["notes"], "seed 42; Amendment 3)", "seed 42; Amendment 3, {{N:note_validation_protocol}})")
    rep_list(t["notes"], "frame-weighted estimates and per-theme values are in Multimedia Appendix 3.",
             "frame-weighted estimates and per-theme values are in {{T:theme_validation}}.")
    drop_note(t, "The development pilot preceded the production run and its CI could not be reproduced")
    t["notes"].append("Development-pilot CIs are percentile bootstrap intervals over records (1000 resamples, seed 42).")
    return t, True


def table2():
    t = parse(SRC / "tables" / "Table2_v2.md")
    rep_list(t["notes"], " Version 2 (Batch 2d): values unchanged from Batch 2c, because every OR in this table already used journal "
                         "cluster-robust SEs.", "")
    drop_note(t, "Not included: model type")
    rep_list(t["notes"], "the ordinal model with its proportional-odds check and the Advocacy model are in Multimedia Appendix 3.",
             "the ordinal model with its proportional-odds check and the Advocacy model are in {{T:regression_full}}.")
    return t, False


def table3():
    t = parse(SRC / "tables" / "Table3_v2.md")
    hdr = {"Adjusted (B4)": "Adjusted", "Within journal (B4 S3)": "Within journal", "Augmented corpus (B2 b)": "Augmented corpus",
           "Full-abstract corpus (B2 d)": "Full-abstract corpus", "SJR medical corpus (B5 D1)": "SJR Medicine corpus",
           "Symmetric scale (B3)": "Symmetric stance scale"}
    for o, nw in hdr.items():
        rep_list(t["header"], o, nw)
    assert t["notes"][0].startswith("Primary: 2021-2025 analytic corpus") and t["notes"][2].startswith("— not applicable") \
        and t["notes"][3].startswith("Full values with exact P"), t["notes"]
    t["notes"][0] = (
        "Primary: 2021-2025 analytic corpus, unadjusted; OR per year from record-level logistic regression on publication year with "
        "journal cluster-robust SEs (2278 clusters; 95% CI and P). Adjusted: multivariable model in Table 2 (journal cluster-robust "
        "SEs); for the specialty row, adjusted average marginal probabilities. Within journal: sensitivity model with journal fixed "
        "effects (journals with at least 10 records and outcome variation; n=8529). Augmented: analytic corpus plus 2453 records "
        "dated 2021-2025 that the production prefilter excluded but the full-abstract reclassification kept, stance-classified with "
        "the same v1 prompt. Full abstract: corpus defined by the full-abstract prefilter labels, which adds the same 2453 records "
        "and drops 1587 production records. SJR Medicine: records in journals that are Q1/Q2 in at least one SCImago Medicine-area "
        "category (2325 records removed from 2021-2025). Symmetric stance scale: 'strong endorsement' flag from a reclassification "
        "of favourable records that drops the transformative-language requirement.")
    t["notes"][2] = (
        "— not applicable or not estimated: the multivariable models covered the critical and Advocacy outcomes only (no theme "
        "models), and the FDA count is an ecological variable that was not modelled; the journal fixed-effects model was fitted for "
        "the critical outcome only; recovered records carry a stance label but no theme, specialty or region label, so the augmented "
        "and full-abstract corpora were used for the stance trends only; first-author country was not recomputed for the SJR "
        "Medicine corpus; the symmetric scale applies to the favourable end only.")
    t["notes"][3] = ("Full values with exact P and n/N are in {{T:corpus_sensitivity}}, {{T:sjr_sensitivity}}, "
                     "{{T:symmetric_endorsement}} and {{T:regression_full}}.")
    return t, True


def write(name, t, landscape):
    cap = RES(t["caption"]); hdr = [RES(h) for h in t["header"]]
    rows = [[RES(c) for c in r] for r in t["rows"]]; notes = [RES(n) for n in t["notes"]]
    d = new_doc()
    sec = d.sections[0]
    if landscape:
        sec.orientation = WD_ORIENT.LANDSCAPE
        sec.page_width, sec.page_height = sec.page_height, sec.page_width
    m = re.match(r"(Table \d+\.) (.*)", cap)
    p = d.add_paragraph(); r = p.add_run(m[1] + " "); r.bold = True
    add_runs(p, m[2], bold=True)
    table(d, hdr, rows, size=7 if landscape else 8, group_rows=set(t["group_rows"]))
    for n in notes:
        para(d, n, 8, space_after=2)
    d.save(OUT / f"{name}_v3.docx")
    L = [f"**{md_text(cap)}**", "", md_table(hdr, rows, set(t["group_rows"])), ""] + [md_text(n) + "\n" for n in notes]
    (OUT / f"{name}_v3.md").write_text("\n".join(L), encoding="utf-8")
    txt = "\n".join(L)
    for pat in (r"\bR1\b", r"\b[AB][1-7]\b", r"Batch [0-9]", r"\{\{", r"Version 2"):
        assert not re.search(pat, txt), (name, pat)


if __name__ == "__main__":
    for name, fn in (("Table1", table1), ("Table2", table2), ("Table3", table3)):
        t, land = fn()
        write(name, t, land)
        print(name, "ok", len(t["rows"]), "rows")
