"""D2 · POST HOC (2026-10-31) source decomposition of the B6 lexicon trends
(JMIR R1 Batch 2d; D5). Plan: revision_r1/ANALYSIS_PLAN_batch2d.md (b8e1c7e).

Population, lexicons and matching are imported from b6_terms.py (LEX, term_regex,
mesh_list); nothing is retyped. Rows (a)-(e) and term rows as in the plan; annual
shares with boot_group_share (joint resample, 1000, seed 42); OR per year with the D1
journal cluster-robust SEs. Run with revision_r1/.venv.
Outputs: revision_r1/final/data/d2_*.csv
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from c_common import DATA, OUT, Y5, rc
from d1_cluster_or import journal_id, logit_trend_cluster

import b6_terms as B6

ROW_LABELS = {"a": "(a) All sources", "b": "(b) Title + abstract", "c": "(c) Keywords or MeSH only",
              "d": "(d) Classifier input (title + first 400 abstract characters)",
              "e": "(e) Later abstract only (characters 401 onward, no match in title + first 400)"}


def series(cr, hit):
    tab = rc.boot_group_share(cr["year"].to_numpy(), np.asarray(hit, float), Y5)
    lt = logit_trend_cluster(cr["year"], np.asarray(hit, float), cr["jid"])
    rho, p, _ = rc.spearman_exact(Y5, tab["point"].to_numpy())
    return tab, lt, rho, p


def main():
    v = rc.load_v1(year_range=(2021, 2025))
    v["year"] = v["pub_year"].astype(int); v["jid"] = journal_id(v["journal"])
    mk = rc.read_str(OUT / "B6/b6_mesh_keywords.csv")
    cr = v[v["critical"]].merge(mk[["pmid", "mesh", "keywords"]], on="pmid", how="left").reset_index(drop=True)
    cr[["mesh", "keywords"]] = cr[["mesh", "keywords"]].fillna("")
    title, abstract = cr["title"].fillna(""), cr["abstract"].fillna("")
    kw = cr["keywords"].str.replace("|", " ; ")
    meshes = cr["mesh"].map(B6.mesh_list)
    t_all = title + " " + abstract + " " + kw
    t_ta = title + " " + abstract
    t_d = title + " " + abstract.str[:400]
    t_late = abstract.str[400:]
    assert len(cr) == 4283

    ref = pd.read_csv(OUT / "B6/B6_lexicon_annual.csv")
    rows, terms_rows, repro = [], [], []
    for name, (terms, mesh_terms, llm_lab) in B6.LEX.items():
        rx = B6.term_regex(terms)
        mesh_hit = meshes.apply(lambda ms: any(m in mesh_terms for m in ms))
        kw_hit = kw.str.contains(rx)
        h = {"a": t_all.str.contains(rx) | mesh_hit,
             "b": t_ta.str.contains(rx),
             "d": t_d.str.contains(rx)}
        h["c"] = (kw_hit | mesh_hit) & ~h["b"]
        h["e"] = t_late.str.contains(rx) & ~h["d"]
        for key in "abcde":
            tab, lt, rho, p = series(cr, h[key])
            for r in tab.itertuples():
                rows.append({"theme": name, "row": key, "label": ROW_LABELS[key], "year": int(r.level), "k": int(r.k),
                             "n": int(r.n), "pct": r.point, "lo": r.lo, "hi": r.hi})
            rows.append({"theme": name, "row": key, "label": ROW_LABELS[key], "year": "trend", "OR": lt["OR"],
                         "OR_lo": lt["OR_lo"], "OR_hi": lt["OR_hi"], "P": lt["P"], "rho": rho, "P_rho": p,
                         "clusters": lt["clusters"], "k": int(np.asarray(h[key]).sum()), "n": len(cr)})
            if key == "a":
                r0 = ref[ref["lexicon theme"] == name].sort_values("year")
                same = (r0["k"].to_list() == tab["k"].astype(int).to_list()) and (r0["n"].to_list() == tab["n"].astype(int).to_list())
                repro.append({"theme": name, "reproduces_B6_k_and_n": same,
                              "max_abs_pct_diff": float(np.max(np.abs(r0["pct"].to_numpy() - tab["point"].to_numpy())))})
        # (a) vs (b) or (c): union identity check
        union_ok = bool(((h["b"] | h["c"]) == h["a"]).all())
        repro[-1]["a_equals_b_or_c"] = union_ok
        for term in terms + (["human oversight"] if name == "Regulation" else []):
            ht = t_ta.str.contains(B6.term_regex([term]))
            tab, lt, rho, p = series(cr, ht)
            for r in tab.itertuples():
                terms_rows.append({"theme": name, "term": term, "year": int(r.level), "k": int(r.k), "n": int(r.n),
                                   "pct": r.point, "lo": r.lo, "hi": r.hi})
            terms_rows.append({"theme": name, "term": term, "year": "trend", "OR": lt["OR"], "OR_lo": lt["OR_lo"],
                               "OR_hi": lt["OR_hi"], "P": lt["P"], "rho": rho, "P_rho": p, "k": int(ht.sum()), "n": len(cr)})
    pd.DataFrame(rows).to_csv(DATA / "d2_lexicon_rows.csv", index=False)
    pd.DataFrame(terms_rows).to_csv(DATA / "d2_lexicon_terms.csv", index=False)
    pd.DataFrame(repro).to_csv(DATA / "d2_reproduction_check.csv", index=False)
    ab = cr.assign(L=abstract.str.len())
    med = []
    for y in Y5:
        a = ab[ab.year == y]
        med.append({"year": y, "n_all": len(a), "median_len_all": float(a["L"].median()),
                    "n_abstract_present": int((a["L"] > 0).sum()), "median_len_abstract_present": float(a.loc[a["L"] > 0, "L"].median())})
    pd.DataFrame(med).to_csv(DATA / "d2_abstract_length.csv", index=False)
    print(pd.DataFrame(repro).to_string())
    d = pd.DataFrame(rows)
    reg = d[(d.theme == "Regulation") & (d.year != "trend")]
    print(reg.pivot(index="row", columns="year", values="pct").round(1).to_string())
    t = pd.DataFrame(terms_rows)
    print(t[(t.term.isin(["oversight", "human oversight"])) & (t.year != "trend")].pivot(index="term", columns="year", values="pct").round(1).to_string())
    print(pd.DataFrame(med).to_string())


if __name__ == "__main__":
    main()
