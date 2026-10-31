"""D1 · Journal cluster-robust CIs for every unadjusted record-level OR per year
(JMIR R1 Batch 2d; E12, E13, D4a, X3). Plan: revision_r1/ANALYSIS_PLAN_batch2d.md (b8e1c7e).

`logit_trend_cluster` is a copy of r1_common.logit_trend with journal cluster-robust
SEs (statsmodels GLM, cov_type="cluster"); the point estimate is the same maximum-
likelihood estimate. The journal identifier is the B4 one (sjr_filter.normalise +
ALIAS_PATCH, imported). Record sets are rebuilt exactly as in T4, B2, B3, B5 and B6.
Run with revision_r1/.venv.
Output: revision_r1/final/data/d1_cluster_or.csv
"""

from __future__ import annotations

import re

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats

from c_common import DATA, OUT, Y5, c_book, rc

import sjr_filter as SF  # noqa: E402  (repository root on sys.path via c_common)

BOOK = c_book()
ROWS = []


def journal_id(s):
    return s.fillna("").map(lambda j: SF.ALIAS_PATCH.get(SF.normalise(j), SF.normalise(j)))


def logit_trend_cluster(year, outcome, groups, weights=None, centre=None):
    """Copy of r1_common.logit_trend: outcome ~ year (continuous, centred), with journal
    cluster-robust SEs. Returns OR per year, 95% CI, two-sided Wald P."""
    year = np.asarray(year, dtype=float); y = np.asarray(outcome, dtype=float)
    c = np.mean(year) if centre is None else centre
    X = np.column_stack([np.ones_like(year), year - c])
    g = pd.factorize(pd.Series(groups).astype(str))[0]
    if weights is None:
        res = sm.GLM(y, X, family=sm.families.Binomial()).fit(cov_type="cluster", cov_kwds={"groups": g})
        b, se = res.params[1], res.bse[1]
    else:   # statsmodels does not fully support cluster covariance with freq_weights: explicit weighted sandwich
        b_all, V = weighted_cluster_sandwich(X, y, np.asarray(weights, float), g)
        b, se = b_all[1], np.sqrt(V[1, 1])
    return {"OR": float(np.exp(b)), "OR_lo": float(np.exp(b - 1.959963984540054 * se)),
            "OR_hi": float(np.exp(b + 1.959963984540054 * se)), "P": float(2 * stats.norm.sf(abs(b / se))),
            "n": int(len(y)), "events": float((y * (np.asarray(weights, float) if weights is not None else 1)).sum()),
            "clusters": int(len(np.unique(g)))}


def weighted_cluster_sandwich(X, y, w, g):
    """Weighted logistic MLE with a cluster-robust sandwich, using the same small-sample factor as statsmodels'
    cluster covariance: G/(G-1) * (N-1)/(N-K). Verified against statsmodels for w = 1 in check_sandwich()."""
    beta = sm.GLM(y, X, family=sm.families.Binomial(), freq_weights=w).fit().params
    p = 1 / (1 + np.exp(-X @ beta))
    bread = np.linalg.inv((X * (w * p * (1 - p))[:, None]).T @ X)
    sc = X * (w * (y - p))[:, None]
    S = np.zeros((X.shape[1], X.shape[1]))
    for gi in np.unique(g):
        s_ = sc[g == gi].sum(0); S += np.outer(s_, s_)
    G, N, K = len(np.unique(g)), len(y), X.shape[1]
    return beta, (G / (G - 1)) * ((N - 1) / (N - K)) * bread @ S @ bread


def check_sandwich(year, y, groups):
    year = np.asarray(year, float); X = np.column_stack([np.ones_like(year), year - year.mean()])
    g = pd.factorize(pd.Series(groups).astype(str))[0]; y = np.asarray(y, float)
    se_sm = sm.GLM(y, X, family=sm.families.Binomial()).fit(cov_type="cluster", cov_kwds={"groups": g}).bse[1]
    se_mn = np.sqrt(weighted_cluster_sandwich(X, y, np.ones(len(y)), g)[1][1, 1])
    return se_sm, se_mn


def book_or(id_):
    """Batch 2c (v1) OR for a book row: numeric field if present, else parsed from the value text."""
    r = BOOK[id_]
    m = re.search(r"OR ([0-9.]+) per year", r["value"])
    if r["point"] not in ("", None) and id_.endswith("-OR"):
        return float(r["point"])
    return float(m[1]) if m else np.nan


def add(key, ids, year, y, journals, weights=None):
    r = logit_trend_cluster(year, y, journals, weights)
    v1 = book_or(ids[0])
    ROWS.append({"series": key, "book_ids": ";".join(ids), **r, "OR_v1": v1, "abs_diff": abs(r["OR"] - v1),
                 "printed_equal": f"{r['OR']:.3f}" == f"{v1:.3f}"})


def slug(s):
    s = re.sub(r"[^A-Za-z0-9]+", "", s.replace("&", "and").replace("/", " ").title())
    return s[:24].upper()


def main():
    allv = rc.load_v1(year_range=None)
    jmap = dict(zip(allv["pmid"], journal_id(allv["journal"])))
    v = rc.load_v1(year_range=(2021, 2025)).reset_index(drop=True)
    v["jid"] = journal_id(v["journal"]); v["year"] = v["pub_year"].astype(int)
    print("analytic clusters:", v["jid"].nunique())
    print("sandwich check (statsmodels SE, manual SE):", check_sandwich(v.year, v.critical, v.jid))

    # stance
    for code, s in (("ALARM", "Alarm"), ("CAUT", "Caution"), ("NEUT", "Neutral"), ("CO", "Cautious Optimism"), ("ADV", "Advocacy")):
        add(f"Stance: {s}", [f"RES-TMP-{code}-OR"], v.year, v.stance == s, v.jid)
    add("Stance: critical", ["RES-TMP-CRIT-OR"], v.year, v.critical, v.jid)
    add("Stance: favourable", ["RES-TMP-FAV-OR"], v.year, v.favourable, v.jid)
    for g in ("discourse", "evaluative"):
        d = v[v.paper_type == g]
        add(f"Within genre: {g}", [f"RES-TMP-GEN{g[:4].upper()}-OR"], d.year, d.critical, d.jid)

    # themes (T4: thematic_alarm.csv, its own pub_year, 2021-2025)
    th = pd.read_csv(rc.REPO_OUT / "analysis/thematic_alarm.csv", dtype={"pmid": str}, low_memory=False)
    th["pub_year"] = pd.to_numeric(th["pub_year"], errors="coerce")
    th5 = th[th["pub_year"].between(2021, 2025)].copy()
    tl = th5["themes"].fillna("").str.split("|")
    for t in rc.THEMES:
        lab = rc.THEME_LABELS[t]
        add(f"Theme: {lab}", [f"RES-TMP-TH-{slug(lab)}-OR"], th5["pub_year"], tl.apply(lambda l: t in l), journal_id(th5["journal"]))

    # mechanism (T4 logic)
    ac = pd.read_csv(rc.REPO_OUT / "analyses/q7_classified_ac.csv", dtype={"pmid": str})
    ac = ac[(ac["failure_mode"] != "FAILED") & (ac["model_type"] != "FAILED")].copy()
    ac = ac.merge(allv[["pmid", "has_abstract"]], on="pmid", how="left")
    ac = ac[ac["has_abstract"] == True].copy()  # noqa: E712
    th6 = th[th["pub_year"].between(2021, 2026)]
    gate = th6.assign(g=th6["themes"].fillna("").str.lower().str.contains("hallucination"))[["pmid", "g"]]
    ac = ac.merge(gate, on="pmid", how="left"); ac["g"] = ac["g"].fillna(False).astype(bool)
    ac["pub_year"] = ac["pub_year"].astype(int); ac = ac[ac.pub_year.isin(Y5)]
    ac["jid"] = ac["pmid"].map(jmap)
    ac["fab"] = ac["failure_mode"].isin(["confabulation", "both"]); ac["gen"] = ac["model_type"].isin(["generative", "both"])
    gt = ac[ac.g]
    for fm, code in (("confabulation", "FM-CONF"), ("misclassification", "FM-MIS"), ("both", "FM-BOTH"), ("none_or_unclear", "FM-NONE")):
        add(f"Mechanism gated: {fm}", [f"RES-TMP-{code}-OR"], gt.pub_year, gt.failure_mode == fm, gt.jid)
    add("Mechanism gated: fabrication-involved", ["RES-TMP-FAB-GATED-OR"], gt.pub_year, gt.fab, gt.jid)
    add("Mechanism: generative share", ["RES-TMP-GENSHARE-OR"], ac.pub_year, ac.gen, ac.jid)
    add("Mechanism: fabrication share", ["RES-TMP-FAB-ALL-OR"], ac.pub_year, ac.fab, ac.jid)
    gn = ac[ac.gen]
    add("Mechanism: fabrication among generative", ["RES-TMP-FAB-GEN-OR"], gn.pub_year, gn.fab, gn.jid)

    # keep rate (eligible records; year = first 20xx in pub_date)
    de = rc.read_str(rc.DATA_ROOT / "prefiltered_discourse_eval.csv"); ap = rc.read_str(rc.DATA_ROOT / "prefiltered_application.csv")
    el = pd.concat([de[["pmid", "pub_date", "journal"]].assign(kept=True), ap[["pmid", "pub_date", "journal"]].assign(kept=False)],
                   ignore_index=True)
    el["y"] = el["pub_date"].str.extract(r"\b(20\d{2})\b")[0].astype(float)
    el = el[el["y"].isin(Y5)]
    add("Prefilter keep rate", ["RES-TMP-KEEP-OR"], el.y, el.kept, journal_id(el["journal"]))

    # Q3 arm
    q3 = pd.read_csv(rc.DATA_ROOT / "classified_medical_Q3.csv", low_memory=False, dtype={"pmid": str})
    q3["pub_year"] = pd.to_numeric(q3["pub_year"], errors="coerce")
    q3 = q3[(q3["stance"] != "FAILED") & q3["pub_year"].between(2021, 2025)]
    qj = journal_id(q3["journal"])
    add("Q3: critical", ["RES-TMP-Q3-CRIT-OR"], q3.pub_year, q3.stance.isin(["Alarm", "Caution"]), qj)
    for code, s in (("ALARM", "Alarm"), ("CAUT", "Caution"), ("NEUT", "Neutral"), ("CO", "Cautious Optimism"), ("ADV", "Advocacy")):
        add(f"Q3: {s}", [f"RES-TMP-Q3-{code}-OR"], q3.pub_year, q3.stance == s, qj)

    # B3 strong endorsement
    fl = rc.read_str(OUT / "B3/b3_endorsement_labels.csv")[["pmid", "strong_endorsement", "failed"]]
    s3 = v.merge(fl, on="pmid", how="left")
    add("B3 strong endorsement", ["RES-TMP-SE-OR"], s3.year, s3.strong_endorsement == "yes", s3.jid)
    add("B3 strong endorsement, upper bound", ["RES-TMP-SEUB-OR"], s3.year,
        (s3.strong_endorsement == "yes") | (s3.failed == "1"), s3.jid)

    # B6 lexicon series (row a of D2; b6_terms matching imported)
    import b6_terms as B6
    mk = rc.read_str(OUT / "B6/b6_mesh_keywords.csv")
    cr = v[v["critical"]].merge(mk[["pmid", "mesh", "keywords"]], on="pmid", how="left")
    cr[["mesh", "keywords"]] = cr[["mesh", "keywords"]].fillna("")
    text = cr["title"].fillna("") + " " + cr["abstract"].fillna("") + " " + cr["keywords"].str.replace("|", " ; ")
    meshes = cr["mesh"].map(B6.mesh_list)
    lexslug = {"Errors and hallucination": "HALLUCINATIONERRORS", "Patient safety": "PATIENTSAFETY",
               "Regulation": "GOVERNANCEREGULATION", "Ethics and bias": "ETHICSANDBIAS"}
    for name, (terms, mesh_terms, _) in B6.LEX.items():
        hit = text.str.contains(B6.term_regex(terms)) | meshes.apply(lambda ms: any(m in mesh_terms for m in ms))
        add(f"Lexicon: {name}", [f"RES-THM-LEX-{lexslug[name]}-OR"], cr.year, hit, cr.jid)

    # B2 corpora
    import b2_analysis as B2
    prod = v[["pmid", "year", "stance", "jid"]]
    a2 = rc.read_str(OUT / "A2/a2_fullabstract_labels.csv")
    b2 = rc.read_str(OUT / "B2/b2_stance_labels.csv").merge(a2[["pmid", "year"]], on="pmid")
    b2 = b2[b2.failed != "1"].copy(); b2["year"] = pd.to_numeric(b2["year"], errors="coerce"); b2 = b2[b2.year.isin(Y5)]
    b2["year"] = b2["year"].astype(int)
    ajour = dict(zip(ap["pmid"], journal_id(ap["journal"])))
    b2["jid"] = b2["pmid"].map(ajour)
    assert b2["jid"].notna().all()
    rec = b2[["pmid", "year", "stance", "jid"]]
    full_keep = set(a2.loc[a2.label_fullabstract.isin(["discourse", "evaluative"]), "pmid"])
    aug = pd.concat([prod, rec], ignore_index=True)
    corp = {"A": (prod, None), "B": (aug, None),
            "C": (aug, np.r_[np.ones(len(prod)), rec["year"].map(B2.EXF_PRECISION).to_numpy()]),
            "D": (pd.concat([prod[prod.pmid.isin(full_keep)], rec], ignore_index=True), None)}
    for c, (d, w) in corp.items():
        add(f"B2 corpus ({c.lower()}): critical", [f"RES-SEN-B2{c}-CRITICAL"], d.year, d.stance.isin(["Alarm", "Caution"]), d.jid, w)
        add(f"B2 corpus ({c.lower()}): Advocacy", [f"RES-SEN-B2{c}-ADVOCACY"], d.year, d.stance == "Advocacy", d.jid, w)

    # B5 corpus definitions
    import b5_sjr_medical_sensitivity as B5
    q = pd.read_csv(OUT / "T7_record_level_quartiles.csv", dtype={"pmid": str})
    w5 = v.merge(q.drop(columns=["journal", "year"]), on="pmid", how="left").merge(th[["pmid", "themes"]], on="pmid", how="left")
    for name, col in B5.DEFS.items():
        code = name.split(" ")[0] if name.startswith("D") else "FULL"
        d = w5 if col is None else w5[w5[col].isin(["Q1", "Q2"])]
        ids_c = [f"RES-B5X-{code}-TREND20212-CRITICAL"] + ([f"RES-SEN-B5{code}-CRITICAL"] if code != "FULL" else [])
        ids_a = [f"RES-B5X-{code}-TREND20212-ADVOCACY"] + ([f"RES-SEN-B5{code}-ADVOCACY"] if code != "FULL" else [])
        add(f"B5 {code}: critical", ids_c, d.year, d.critical, d.jid)
        add(f"B5 {code}: Advocacy", ids_a, d.year, d.stance == "Advocacy", d.jid)
        cr5 = d[d.critical]; tl5 = cr5["themes"].fillna("").str.split("|")
        for t, lab in B5.THEMES4.items():
            s_ = slug(lab)
            ids = [f"RES-B5X-{code}-THEMETREND-{s_}"] + ([f"RES-SEN-B5{code}-{s_}"] if code != "FULL" else [])
            add(f"B5 {code}: theme {lab}", ids, cr5.year, tl5.apply(lambda l: t in l), cr5.jid)

    out = pd.DataFrame(ROWS)
    out.to_csv(DATA / "d1_cluster_or.csv", index=False)
    print(len(out), "series; max |OR - OR_v1| =", out.abs_diff.max(), "; printed differences:", int((~out.printed_equal).sum()))
    print(out[["series", "n", "clusters", "OR", "OR_lo", "OR_hi", "P"]].head(8).to_string())


if __name__ == "__main__":
    main()
