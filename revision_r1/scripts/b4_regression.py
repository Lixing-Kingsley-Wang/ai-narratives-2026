"""B4 · Record-level multivariable regression with journal clustering
(JMIR R1 Batch 2b; D4a, X3, D3). Pre-specified in ANALYSIS_PLAN_batch2b.md.
Run with revision_r1/.venv (statsmodels).

Outputs: revision_r1/outputs/B4/*.csv and B4_regression.md
"""

from __future__ import annotations

import sys
import warnings

import numpy as np
import pandas as pd
import patsy
import statsmodels.api as sm
from scipy import stats
from statsmodels.miscmodels.ordinal_model import OrderedModel

from r1_common import OUT, REPO, REPO_OUT, STANCES, load_v1, md_table

sys.path.insert(0, str(REPO))
from analysis.robustness import simplify_pubtype_5  # noqa: E402
import sjr_filter as SF  # noqa: E402

warnings.filterwarnings("ignore")
B4 = OUT / "B4"
FACTORS = ["genre", "pubtype", "specialty", "region"]


def jmir_p(p):
    if pd.isna(p):
        return "NA"
    return "<.001" if p < 0.001 else f"{p:.3f}".lstrip("0")


def load(years):
    v = load_v1(year_range=(2021, 2026))
    v = v[v["pub_year"].isin(years)].copy()
    spec = pd.read_csv(REPO_OUT / "specialty_classifications.csv", dtype={"pmid": str}, usecols=["pmid", "specialty"])
    geo = pd.read_csv(REPO_OUT / "geography_classifications.csv", dtype={"pmid": str}, usecols=["pmid", "region"])
    cty = pd.read_csv(B4 / "b4_country_resolved.csv", dtype={"pmid": str})
    v = v.merge(spec, on="pmid", how="left").merge(geo, on="pmid", how="left").merge(cty, on="pmid", how="left")
    v["specialty"] = v["specialty"].where(v["specialty"].notna() & (v["specialty"] != "FAILED"), "Unassigned")
    v["region"] = v["region"].fillna("Unknown").replace({"": "Unknown"})
    v["pubtype"] = v["pub_type"].fillna("").map(simplify_pubtype_5)
    v["genre"] = v["paper_type"]
    v["journal_id"] = v["journal"].fillna("").map(lambda j: SF.ALIAS_PATCH.get(SF.normalise(j), SF.normalise(j)))
    v["year"] = v["pub_year"].astype(int)
    v["critical"] = v["critical"].astype(int)
    v["advocacy"] = (v["stance"] == "Advocacy").astype(int)
    v["stance_ord"] = v["stance"].map({s: i for i, s in enumerate(STANCES)})
    return v.reset_index(drop=True)


def refs(d, factors):
    return {f: d[f].value_counts().index[0] for f in factors}


def formula(outcome, d, factors, year_term="year_c", extra=""):
    r = refs(d, factors)
    terms = [year_term] + [f'C({f}, Treatment(reference="{r[f]}"))' for f in factors]
    return f"{outcome} ~ " + " + ".join(terms) + extra, r


def fit_logit(fml, d):
    groups = pd.factorize(d["journal_id"])[0]
    y, X = patsy.dmatrices(fml, d, return_type="dataframe")
    res = sm.GLM(y, X, family=sm.families.Binomial()).fit(cov_type="cluster", cov_kwds={"groups": groups})
    res.design_info_ = X.design_info
    return res


def or_table(res, label=""):
    ci = res.conf_int()
    t = pd.DataFrame({"term": res.params.index, "OR": np.exp(res.params.values), "lo": np.exp(ci[0].values),
                      "hi": np.exp(ci[1].values), "P": res.pvalues.values})
    t = t[t.term != "Intercept"].reset_index(drop=True)
    t["model"] = label
    return t


def pretty(term):
    if term.startswith("C("):
        f = term[2:term.index(",")]
        lev = term.split("[T.")[1].rstrip("]")
        return f, lev
    return term, ""


def amp(res, d, var, levels, year_mean):
    """Average marginal predicted probability for each level of var (delta method, cluster-robust V)."""
    di = res.design_info_
    V = res.cov_params().values
    rows = []
    for lev in levels:
        dd = d.copy()
        if var == "year":
            dd["year_c"] = lev - year_mean
        else:
            dd[var] = lev
        X = np.asarray(patsy.build_design_matrices([di], dd, return_type="dataframe")[0])
        p = 1 / (1 + np.exp(-(X @ res.params.values)))
        g = (p * (1 - p))[:, None] * X
        grad = g.mean(axis=0)
        se = float(np.sqrt(grad @ V @ grad))
        est = float(p.mean())
        # delta-method CI on the logit scale, back-transformed (stays inside 0–100%)
        se_l = se / (est * (1 - est))
        lg = np.log(est / (1 - est))
        lo, hi = 1 / (1 + np.exp(-(lg - 1.96 * se_l))), 1 / (1 + np.exp(-(lg + 1.96 * se_l)))
        rows.append({"variable": var, "level": lev, "n_records_at_level": int((d[var] == lev).sum()) if var != "year" else int((d["year"] == lev).sum()),
                     "AMP_%": est * 100, "lo": lo * 100, "hi": hi * 100, "se_prob": se})
    return pd.DataFrame(rows)


def describe(res, d, outcome):
    return {"n": int(res.nobs), "events": int(d[outcome].sum()), "clusters": int(d["journal_id"].nunique())}


def main():
    d = load([2021, 2022, 2023, 2024, 2025])
    ym = d["year"].mean()
    d["year_c"] = d["year"] - ym
    assert len(d) == 14058, len(d)
    L = ["# B4 · Multivariable regression (D4a, X3, D3)\n",
         "Script `revision_r1/scripts/b4_regression.py` (statsmodels 0.15.0, `revision_r1/.venv`). Records: 2021–2025 "
         f"analytic set (n = {len(d):,}). Year continuous, centred on {ym:.3f}. Cluster-robust SEs by journal "
         "(normalised SJR-matching title). Not included: model type (defined only among critical records) and FDA "
         "cleared-device count (18-unit ecological variable).\n"]

    # ---------------- primary logistic: critical ----------------------------
    fml, r = formula("critical", d, FACTORS)
    res = fit_logit(fml, d)
    info = describe(res, d, "critical")
    L.append("## Primary: logistic, critical (Alarm or Caution) vs not\n")
    L.append(f"n = {info['n']:,}; events = {info['events']:,}; clusters (journals) = {info['clusters']:,}. "
             f"Reference levels (most frequent): " + "; ".join(f"{k} = {v}" for k, v in r.items()) + ".\n")
    adj = or_table(res, "adjusted")
    # unadjusted: one covariate at a time, same clustering
    unadj = []
    for f in ["year_c"] + FACTORS:
        fm = ("critical ~ year_c" if f == "year_c" else f'critical ~ C({f}, Treatment(reference="{r[f]}"))')
        unadj.append(or_table(fit_logit(fm, d), "unadjusted"))
    unadj = pd.concat(unadj)
    tab = adj.merge(unadj[["term", "OR", "lo", "hi", "P"]], on="term", how="left", suffixes=("_adj", "_unadj"))
    tab["variable"], tab["level"] = zip(*tab["term"].map(pretty))
    tab.to_csv(B4 / "B4_primary_critical_ORs.csv", index=False)
    show = pd.DataFrame({"variable": tab["variable"], "level": tab["level"],
                         "adjusted OR (95% CI)": [f"{a:.2f} ({b:.2f}–{c:.2f})" for a, b, c in zip(tab.OR_adj, tab.lo_adj, tab.hi_adj)],
                         "P (adj.)": tab["P_adj"].map(jmir_p),
                         "unadjusted OR (95% CI)": [f"{a:.2f} ({b:.2f}–{c:.2f})" for a, b, c in zip(tab.OR_unadj, tab.lo_unadj, tab.hi_unadj)],
                         "P (unadj.)": tab["P_unadj"].map(jmir_p)})
    show.loc[show.variable == "year_c", "variable"] = "year (per 1 year)"
    L += [md_table(show), ""]
    amps = pd.concat([amp(res, d, "year", [2021, 2022, 2023, 2024, 2025], ym)] +
                     [amp(res, d, f, sorted(d[f].unique()), ym) for f in ["specialty", "region", "pubtype", "genre"]])
    amps.to_csv(B4 / "B4_primary_critical_AMP.csv", index=False)
    L.append("Average marginal predicted probability of critical stance (%, 95% CI; delta method on the logit scale, cluster-robust):\n")
    for var in ["year", "specialty", "region", "pubtype", "genre"]:
        a = amps[amps.variable == var]
        L.append(f"**{var}**: " + "; ".join(f"{lv} {x:.1f} ({lo:.1f}–{hi:.1f})" for lv, x, lo, hi in zip(a.level, a["AMP_%"], a.lo, a.hi)) + "\n")
    L.append("")

    # ---------------- ordinal ---------------------------------------------------
    L.append("## Secondary 1: ordinal proportional-odds model (Alarm < Caution < Neutral < Cautious Optimism < Advocacy)\n")
    rhs = fml.split("~", 1)[1]
    X = patsy.dmatrix(rhs, d, return_type="dataframe").drop(columns="Intercept")
    groups = pd.factorize(d["journal_id"])[0]
    om = OrderedModel(d["stance_ord"].values, X, distr="logit")
    try:
        ores = om.fit(method="bfgs", maxiter=2000, disp=False, cov_type="cluster", cov_kwds={"groups": groups})
        cov_note = "cluster-robust (journal)"
    except Exception as e:  # pragma: no cover
        ores = om.fit(method="bfgs", maxiter=2000, disp=False)
        cov_note = f"model-based (cluster-robust failed: {type(e).__name__})"
    k = X.shape[1]
    ob, ose = ores.params[:k], ores.bse[:k]
    ord_tab = pd.DataFrame({"term": X.columns, "beta": ob.values, "lo": (ob - 1.96 * ose).values, "hi": (ob + 1.96 * ose).values,
                            "P": ores.pvalues[:k].values})
    # cut-point binary logits: Y > k  (positive beta = more favourable, as in the ordinal model)
    cuts = []
    for kcut, name in enumerate(STANCES[:-1]):
        dd = d.assign(y_gt=(d["stance_ord"] > kcut).astype(int))
        rr = fit_logit("y_gt ~" + rhs, dd)
        ci = rr.conf_int()
        cuts.append(pd.DataFrame({"term": rr.params.index, f"b_gt_{name}": rr.params.values,
                                  f"lo_gt_{name}": ci[0].values, f"hi_gt_{name}": ci[1].values}).query("term != 'Intercept'"))
    po = ord_tab.copy()
    for c in cuts:
        po = po.merge(c, on="term", how="left")
    fails = []
    for _, rw in po.iterrows():
        outside = [n for n in STANCES[:-1] if not (rw[f"lo_gt_{n}"] <= rw["beta"] <= rw[f"hi_gt_{n}"])]
        signs = {np.sign(rw[f"b_gt_{n}"]) for n in STANCES[:-1]}
        fails.append("; ".join(([f"outside CI at >{','.join(outside)}"] if outside else []) + (["sign change"] if len(signs) > 1 else [])))
    po["PO_check"] = fails
    po.to_csv(B4 / "B4_ordinal_and_cutpoints.csv", index=False)
    L.append(f"n = {len(d):,}; covariance: {cov_note}. Coefficients are log-odds of a more favourable category "
             "(positive = more favourable).\n")
    sh = pd.DataFrame({"variable/level": [" ".join(pretty(t)).strip().replace("year_c", "year (per 1 year)") for t in po.term],
                       "ordinal OR (95% CI)": [f"{np.exp(b):.2f} ({np.exp(lo):.2f}–{np.exp(hi):.2f})" for b, lo, hi in zip(po.beta, po.lo, po.hi)],
                       "P": po.P.map(jmir_p)})
    for n in STANCES[:-1]:
        sh[f"OR >{n}"] = [f"{np.exp(x):.2f}" for x in po[f"b_gt_{n}"]]
    sh["proportional-odds check"] = po["PO_check"].replace("", "holds")
    L += [md_table(sh), "",
          f"Proportional odds fails (by the pre-specified rule) for {int((po.PO_check != '').sum())} of {len(po)} terms.\n"]

    # ---------------- advocacy logistic -----------------------------------------
    L.append("## Secondary 2: logistic, Advocacy vs not\n")
    da = d.copy()
    collapsed = {}
    for f in ["specialty", "region", "pubtype"]:
        ev = da.groupby(f)["advocacy"].sum()
        small = ev[ev < 5].index.tolist()
        if small:
            collapsed[f] = small
            da[f] = da[f].where(~da[f].isin(small), "Other (<5 events)")
    fa, ra = formula("advocacy", da, FACTORS)
    resa = fit_logit(fa, da)
    ia = describe(resa, da, "advocacy")
    ta = or_table(resa, "adjusted")
    ta["variable"], ta["level"] = zip(*ta["term"].map(pretty))
    ta.to_csv(B4 / "B4_advocacy_ORs.csv", index=False)
    L.append(f"n = {ia['n']:,}; events = {ia['events']}; clusters = {ia['clusters']:,}. Reference levels: "
             + "; ".join(f"{k} = {v}" for k, v in ra.items()) + ". Levels with <5 Advocacy events collapsed into "
             "'Other (<5 events)': " + ("; ".join(f"{k}: {', '.join(v)}" for k, v in collapsed.items()) or "none") + ".\n")
    L += [md_table(pd.DataFrame({"variable": ta.variable.replace({"year_c": "year (per 1 year)"}), "level": ta.level,
                                 "adjusted OR (95% CI)": [f"{a:.2f} ({b:.2f}–{c:.2f})" for a, b, c in zip(ta.OR, ta.lo, ta.hi)],
                                 "P": ta.P.map(jmir_p)})), ""]
    amp_adv = amp(resa, da, "year", [2021, 2022, 2023, 2024, 2025], ym)
    L.append("Average marginal predicted probability of Advocacy by year (%): " + "; ".join(
        f"{lv} {x:.2f} ({lo:.2f}–{hi:.2f})" for lv, x, lo, hi in zip(amp_adv.level, amp_adv["AMP_%"], amp_adv.lo, amp_adv.hi)) + "\n")

    # ---------------- sensitivity models ---------------------------------------
    L.append("## Sensitivity models (critical outcome)\n")
    sens = []
    f1, _ = formula("critical", d, FACTORS, year_term='C(year, Treatment(reference=2021))')
    r1 = fit_logit(f1, d)
    t1 = or_table(r1, "S1 year categorical"); sens.append(t1)
    d26 = load([2021, 2022, 2023, 2024, 2025, 2026])
    f2, _ = formula("critical", d26, FACTORS, year_term='C(year, Treatment(reference=2021))')
    r2 = fit_logit(f2, d26)
    t2 = or_table(r2, "S2 with Jan–Apr 2026"); sens.append(t2)
    jn = d.groupby("journal_id").agg(n=("critical", "size"), k=("critical", "sum"))
    keep = jn[(jn.n >= 10) & (jn.k > 0) & (jn.k < jn.n)].index
    dfe = d[d.journal_id.isin(keep)].copy()
    f3, _ = formula("critical", dfe, FACTORS, extra=" + C(journal_id)")
    r3 = fit_logit(f3, dfe)
    t3 = or_table(r3, "S3 journal fixed effects"); t3 = t3[~t3.term.str.startswith("C(journal_id")]; sens.append(t3)
    dc = d.copy()
    cc = dc["country"].fillna("Unresolved")
    big = cc.value_counts()
    dc["country_g"] = cc.where(cc.isin(big[big >= 100].index) | (cc == "Unresolved"), "Other")
    fac4 = ["genre", "pubtype", "specialty", "country_g"]
    f4, r4ref = formula("critical", dc, fac4)
    r4 = fit_logit(f4, dc)
    t4 = or_table(r4, "S4 country instead of region"); sens.append(t4)
    S = pd.concat(sens)
    S["variable"], S["level"] = zip(*S["term"].map(pretty))
    S.to_csv(B4 / "B4_sensitivity_ORs.csv", index=False)

    def row(t, term):
        x = t[t.term == term]
        if x.empty:
            return "n/a"
        pp = jmir_p(x.P.iloc[0])
        return f"{x.OR.iloc[0]:.3f} ({x.lo.iloc[0]:.3f}–{x.hi.iloc[0]:.3f}), P{pp if pp.startswith('<') else '=' + pp}"
    yr_terms = {y: f"C(year, Treatment(reference=2021))[T.{y}]" for y in range(2022, 2027)}
    L.append("| model | n | events | journals | year effect |\n|---|---|---|---|---|")
    L.append(f"| Primary (continuous year) | {info['n']:,} | {info['events']:,} | {info['clusters']:,} | OR/yr {row(adj, 'year_c')} |")
    L.append(f"| S1 year categorical (ref 2021) | {int(r1.nobs):,} | {int(d.critical.sum()):,} | {d.journal_id.nunique():,} | "
             + "; ".join(f"{y}: {row(t1, yr_terms[y])}" for y in range(2022, 2026)) + " |")
    L.append(f"| S2 adding Jan–Apr 2026 (ref 2021) | {int(r2.nobs):,} | {int(d26.critical.sum()):,} | {d26.journal_id.nunique():,} | "
             + "; ".join(f"{y}: {row(t2, yr_terms[y])}" for y in range(2022, 2027)) + " |")
    L.append(f"| S3 journal fixed effects (≥10 records, outcome varies) | {int(r3.nobs):,} | {int(dfe.critical.sum()):,} | {len(keep):,} | "
             f"OR/yr {row(t3, 'year_c')} |")
    us = 'C(country_g, Treatment(reference="{}"))[T.United States]'.format(r4ref["country_g"])
    cn = 'C(country_g, Treatment(reference="{}"))[T.China]'.format(r4ref["country_g"])
    L.append(f"| S4 country (≥100 records; reference {r4ref['country_g']}) | {int(r4.nobs):,} | {int(dc.critical.sum()):,} | {dc.journal_id.nunique():,} | OR/yr {row(t4, 'year_c')} |")
    # US vs China contrast
    names = list(r4.params.index)
    c = np.zeros(len(names))
    if us in names: c[names.index(us)] += 1
    if cn in names: c[names.index(cn)] -= 1
    if r4ref["country_g"] == "United States": c[names.index(cn)] = -1
    if r4ref["country_g"] == "China": c[names.index(us)] = 1
    est = float(c @ r4.params.values); se = float(np.sqrt(c @ r4.cov_params().values @ c))
    pz = 2 * stats.norm.sf(abs(est / se))
    L.append(f"\nAdjusted United States vs China (S4): OR {np.exp(est):.2f} ({np.exp(est - 1.96*se):.2f}–{np.exp(est + 1.96*se):.2f}), "
             f"P{jmir_p(pz) if jmir_p(pz).startswith('<') else '=' + jmir_p(pz)}. Countries kept as their own level: {', '.join(sorted(set(dc.country_g) - {'Other', 'Unresolved'}))}.\n")
    (B4 / "B4_regression.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
