"""T7 · SJR quartile feasibility (D6). Read-only; nothing downstream is rerun.

Re-matches every included Q1/Q2 record to its SJR row with the exact matching
rules of sjr_filter.py (normalise + ALIAS_PATCH, publication-year file, 2024
fallback for years without a file), then compares the best quartile with the
best quartile among medicine-related categories under three candidate
definitions (none is chosen here).
Outputs: revision_r1/outputs/T7_*.csv, T7_sjr_quartile.md
"""

from __future__ import annotations

import csv
import re
import sys
from collections import defaultdict

import pandas as pd

from r1_common import DATA_ROOT, OUT, REPO, load_v1, md_table, read_str

sys.path.insert(0, str(REPO))
import sjr_filter as SF  # noqa: E402  (module constants and functions only; main not run)

SJR_DIR = REPO / "input" / "sjr"
QRANK = {"Q1": 1, "Q2": 2, "Q3": 3, "Q4": 4}
CAT_RE = re.compile(r"^(.*?)\s*\((Q[1-4])\)\s*$")


def load_rows(year):
    rows = {}
    with open(SJR_DIR / f"sjr_{year}.csv", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f, delimiter=";"):
            title = row.get("Title", "").strip()
            q = row.get("SJR Best Quartile", "").strip()
            if title and q and q != "-":
                n = SF.normalise(title)
                if n:
                    rows[n] = row  # last wins, as in load_sjr
    return rows


def parse_cats(s):
    out = []
    for part in (s or "").split(";"):
        part = part.strip()
        if not part:
            continue
        m = CAT_RE.match(part)
        out.append((m.group(1).strip(), m.group(2)) if m else (part, None))
    return out


def main():
    years = ["2021", "2022", "2023", "2024", "2025", "2026"]
    cache = {y: load_rows(y) for y in years}
    # category → area map from single-area journals (all years)
    cat_area = defaultdict(lambda: defaultdict(int))
    all_cats = defaultdict(int)
    for y in years:
        for row in cache[y].values():
            areas = [a.strip() for a in (row.get("Areas") or "").split(";") if a.strip()]
            for c, _ in parse_cats(row.get("Categories")):
                all_cats[c] += 1
                if len(areas) == 1:
                    cat_area[c][areas[0]] += 1
    cat_main_area = {c: (max(d, key=d.get) if d else "unknown (only in multi-area journals)") for c, d in
                     ((c, cat_area.get(c, {})) for c in all_cats)}

    MED_AREA = {c for c, a in cat_main_area.items() if a == "Medicine"}
    HEALTH_AREAS = {"Medicine", "Nursing", "Dentistry", "Health Professions", "Neuroscience",
                    "Pharmacology, Toxicology and Pharmaceutics", "Immunology and Microbiology", "Psychology"}
    HEALTH = {c for c, a in cat_main_area.items() if a in HEALTH_AREAS}
    defs = {
        "D1 Medicine area (ASJC 27xx) categories": MED_AREA,
        "D2 D1 minus 'Medicine (miscellaneous)'": MED_AREA - {"Medicine (miscellaneous)"},
        "D3 broad health sciences (Medicine, Nursing, Dentistry, Health Professions, Neuroscience, "
        "Pharmacology, Immunology & Microbiology, Psychology)": HEALTH,
    }

    q12 = read_str(DATA_ROOT / "filtered_medical_all_Q1Q2.csv")
    ana = load_v1(year_range=(2021, 2026))
    ana_ids = set(ana["pmid"])
    recs = []
    for r in q12.itertuples():
        y = (r.year or "")[:4]
        rows = cache.get(y, cache["2024"])
        n = SF.ALIAS_PATCH.get(SF.normalise(r.journal), SF.normalise(r.journal))
        row = rows.get(n)
        if row is None:
            recs.append({"pmid": r.pmid, "journal": r.journal, "year": y, "matched": False})
            continue
        cats = parse_cats(row.get("Categories"))
        rec = {"pmid": r.pmid, "journal": row["Title"], "year": y, "matched": True,
               "best_q": row["SJR Best Quartile"], "areas": row.get("Areas", ""),
               "categories": row.get("Categories", ""), "file_q": r.sjr_quartile}
        for dname, dset in defs.items():
            mq = [QRANK[q] for c, q in cats if c in dset and q]
            rec[dname] = f"Q{min(mq)}" if mq else "none"
        recs.append(rec)
    R = pd.DataFrame(recs)
    R["in_analytic"] = R["pmid"].isin(ana_ids)

    # Q4-in-unmatched check
    unm = read_str(DATA_ROOT / "filtered_medical_all_unmatched.csv")
    full_cache = {}
    for y in years:
        d = {}
        with open(SJR_DIR / f"sjr_{y}.csv", encoding="utf-8-sig") as f:
            for row in csv.DictReader(f, delimiter=";"):
                n = SF.normalise(row.get("Title", "").strip())
                if n:
                    d[n] = row.get("SJR Best Quartile", "").strip()
        full_cache[y] = d
    uq = []
    for r in unm.itertuples():
        y = (r.year or "")[:4]
        n = SF.ALIAS_PATCH.get(SF.normalise(r.journal), SF.normalise(r.journal))
        uq.append(full_cache.get(y, full_cache["2024"]).get(n, "title not in SJR file"))
    unm_q = pd.Series(uq).replace({"-": "listed, no quartile ('-')", "": "listed, empty quartile"}).value_counts()

    # ---- outputs -----------------------------------------------------------
    cat_tab = (pd.DataFrame([{"category": c, "rows_across_years": n, "main_area (from single-area journals)": cat_main_area[c],
                              **{d.split(" ")[0]: c in s for d, s in defs.items()}} for c, n in all_cats.items()])
               .sort_values(["main_area (from single-area journals)", "category"]))
    # restrict category list to categories carried by included journals
    inc_cats = set()
    for s in R.loc[R.matched, "categories"].dropna():
        inc_cats.update(c for c, _ in parse_cats(s))
    cat_inc = cat_tab[cat_tab["category"].isin(inc_cats)].copy()
    cat_inc["included_records"] = cat_inc["category"].map(
        lambda c: int(R.loc[R.matched, "categories"].str.contains(re.escape(c) + r" \(", regex=True).sum()))
    cat_inc.to_csv(OUT / "T7_categories_in_included_journals.csv", index=False)

    summ, tops = [], {}
    M = R[R.matched]
    for d in defs:
        dep = M[d].isin(["Q3", "Q4", "none"])
        for scope, mask in [("eligible Q1/Q2 (97,492)", pd.Series(True, index=M.index)), ("analytic set (16,747)", M["in_analytic"])]:
            sub = M[mask]
            dsub = dep[mask]
            summ.append({"definition": d, "scope": scope, "records": len(sub),
                         "records whose Q1/Q2 depends only on a non-medical category": int(dsub.sum()),
                         "%": round(dsub.mean() * 100, 2),
                         "  of which medical best = Q3": int((sub[d] == "Q3").sum()),
                         "  of which medical best = Q4": int((sub[d] == "Q4").sum()),
                         "  of which no medical category": int((sub[d] == "none").sum()),
                         "journals (journal-title × any year)": int(sub.loc[dsub, "journal"].nunique()),
                         "journals total": int(sub["journal"].nunique())})
        top = (M[dep].groupby("journal").agg(records=("pmid", "size"), analytic_records=("in_analytic", "sum"),
                                             best_q=("best_q", lambda s: "/".join(sorted(set(s)))),
                                             medical_best=(d, lambda s: "/".join(sorted(set(s)))),
                                             categories=("categories", "last"))
               .sort_values("records", ascending=False).head(20).reset_index())
        tops[d] = top
        top.to_csv(OUT / f"T7_top20_{d.split(' ')[0]}.csv", index=False)
    summ = pd.DataFrame(summ)
    summ.to_csv(OUT / "T7_summary.csv", index=False)
    R.drop(columns=["categories"]).to_csv(OUT / "T7_record_level_quartiles.csv", index=False)

    L = ["# T7 · SJR quartile feasibility (D6)\n",
         "Script: `revision_r1/scripts/t7_sjr_quartile.py`. Matching reuses `sjr_filter.py` (`normalise`, `ALIAS_PATCH`, "
         "publication-year file with 2024 fallback). Nothing downstream was rerun.\n",
         "## 1. What the SJR files contain\n",
         f"- `input/sjr/sjr_2021.csv` … `sjr_2026.csv` (semicolon-delimited). Columns include `SJR Best Quartile`, "
         "**`Categories`** (each category with its own quartile, e.g. `Hematology (Q1); Oncology (Q1)`), and **`Areas`** "
         "(subject areas, e.g. `Medicine`). `sjr_filter.py` reads only `Title` and `SJR Best Quartile`.",
         f"- `sjr_2026.csv` is identical to `sjr_2025.csv` (Methods source-of-truth §1c).",
         f"- Re-matched {int(R.matched.sum()):,}/{len(R):,} included Q1/Q2 records to an SJR row "
         f"({int((~R.matched).sum())} unmatched on re-run). Best quartile on re-match equals the stored `sjr_quartile` for "
         f"{int((M.best_q == M.file_q).sum()):,}/{len(M):,}.",
         "- The `Areas` field is journal-level; categories are not tagged with an area in the file. Category → area was "
         "therefore inferred from single-area journals (column `main_area` in the csv); categories that only ever appear in "
         "multi-area journals are marked unknown.\n",
         "## 2. Categories carried by included journals\n",
         f"{len(cat_inc)} distinct categories; full list with inferred area, record counts and membership in each candidate "
         "definition: [T7_categories_in_included_journals.csv](T7_categories_in_included_journals.csv). By inferred area:\n",
         md_table(cat_inc.groupby("main_area (from single-area journals)").agg(categories=("category", "size"),
                                                                               included_records=("included_records", "sum"))
                  .sort_values("included_records", ascending=False).reset_index(), "{:.0f}"), "",
         "## 3. Candidate definitions of 'medicine-related' (none chosen)\n"]
    for d, s in defs.items():
        L.append(f"- **{d}**: {len(s & inc_cats)} categories among included journals.")
    L += ["\n## 4. Records and journals whose Q1/Q2 status depends only on a non-medical category\n",
          "A record 'depends only on a non-medical category' when its journal is Q1/Q2 by best quartile but its best quartile "
          "among medicine-related categories is Q3, Q4, or the journal has no medicine-related category.\n",
          md_table(summ), ""]
    for d, top in tops.items():
        L.append(f"### Top 20 journals by record count — {d}\n")
        t = top.copy()
        t["categories"] = t["categories"].str.slice(0, 110)
        L.append(md_table(t, "{:.0f}"))
        L.append("")
    L += ["## 5. Side finding: Q4 journals are counted as 'unmatched'\n",
          "`sjr_filter.py` routes any quartile other than Q1/Q2/Q3 (including **Q4** and `-`) to the unmatched file "
          "(`filter_file`, `else:` branch, lines 207–210). Methods calls the 7,922 'unmatched'. Re-looking up the 7,922 "
          "with the same rules:\n", md_table(unm_q.reset_index().rename(columns={"index": "SJR status", 0: "records"}), "{:.0f}"), ""]
    (OUT / "T7_sjr_quartile.md").write_text("\n".join(L) + "\n")
    print("\n".join(L[:30]))
    print(summ.to_string())
    print(unm_q)


if __name__ == "__main__":
    main()
