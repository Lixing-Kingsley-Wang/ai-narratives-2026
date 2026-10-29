"""C1 step 1 · Recompute, on 2021-2025, the analyses that Batch 1-2b did not
already produce for that window (JMIR R1 Batch 2c; E2/E8, E12, E14).

No new inferential analyses: every quantity below re-runs an existing analysis
(the submitted pipeline, Batch 1 T1-T8 or Batch 2a/2b) on the 2021-2025 window,
or adds a CI to an existing estimate with the study's CI method. Run with the
project venv (geopandas is needed by the imported country resolver).

Outputs (revision_r1/final/data/):
  flow_2021_2025.csv, missing_2021_2025.csv, title_only_2021_2025.csv,
  subsets_2021_2025.csv, ea_vs_nawe_within_specialty.csv, theme_by_format.csv,
  advocacy_by_specialty.csv, fda_robustness.csv, specialty_fda.csv,
  validation_ci.csv, fv_tier_verdict.csv, fv_counts.csv, country_2021_2025.csv,
  review_subtypes.csv, pubtype_stance.csv, region_2021_2025.csv,
  specialty_2021_2025.csv
"""

from __future__ import annotations

import json

import numpy as np
import pandas as pd
from scipy.stats import beta, spearmanr, t as tdist

from c_common import DATA, OUT, REPO, Y5, rc

from analysis.robustness import bootstrap_ci, simplify_pubtype_5, simplify_pubtype_7  # noqa: E402
from analysis.run_country_critical_map import resolve_country  # noqa: E402
from analysis.run_specialty_aiadoption import (ALL_SPECIALTIES, FDA_STRUCTURAL_ZERO,  # noqa: E402
                                               load_fda_device_counts, spearman_report)

REPO_OUT = rc.REPO_OUT
DATA_ROOT = rc.DATA_ROOT
SEED = 42


def cp(k, n):
    lo = 0.0 if k == 0 else beta.ppf(0.025, k, n - k + 1)
    hi = 1.0 if k == n else beta.ppf(0.975, k + 1, n - k)
    return lo * 100, hi * 100


def boot_share(x):
    x = np.asarray(x, float)
    d = [x[i].mean() * 100 for i in rc.boot_indices(len(x))]
    lo, hi = np.percentile(d, [2.5, 97.5])
    return x.mean() * 100, lo, hi


def base_2125():
    v = rc.load_v1(year_range=(2021, 2025)).reset_index(drop=True)
    spec = pd.read_csv(REPO_OUT / "specialty_classifications.csv", dtype={"pmid": str}, usecols=["pmid", "specialty"])
    geo = pd.read_csv(REPO_OUT / "geography_classifications.csv", dtype={"pmid": str}, usecols=["pmid", "country", "region"])
    v = v.merge(spec, on="pmid", how="left").merge(geo.rename(columns={"country": "country_geo"}), on="pmid", how="left")
    v["country_map"] = v["first_affiliation"].map(resolve_country)
    v["pt5"] = v["pub_type"].fillna("").map(simplify_pubtype_5)
    v["pt7"] = v["pub_type"].fillna("").map(simplify_pubtype_7)
    v["year"] = v["pub_year"].astype(int)
    return v


# ---------------------------------------------------------------------------
def flow(v):
    """Record flow with the 2021-2025 window step in place of the April 2026 cutoff."""
    st = pd.read_csv(OUT / "T6_stage_table.csv")
    get = lambda s: st[st["stage"].str.startswith(s)].iloc[0]
    de = rc.read_str(DATA_ROOT / "prefiltered_discourse_eval.csv")
    ap = rc.read_str(DATA_ROOT / "prefiltered_application.csv")
    for d in (de, ap):  # year as in cv2_keep_rate.py / A3 frames: first 20xx in pub_date
        d["y"] = d["pub_date"].str.extract(r"\b(20\d{2})\b")[0].astype(float)
    elig_y = pd.concat([de["y"], ap["y"]])
    in5 = elig_y.isin(Y5)
    n_2026 = int((elig_y == 2026).sum()); n_other = int((~elig_y.isin(Y5 + [2026])).sum())
    de5, ap5 = de[de["y"].isin(Y5)], ap[ap["y"].isin(Y5)]
    los = pd.read_csv(OUT / "T6_losses_by_year.csv")
    los["pub_year"] = los["pub_year"].astype(str)
    l5 = los[los["pub_year"].isin([str(y) for y in Y5])]
    fallback5 = int(l5["6a. of which: prefilter failures defaulted to application (T1)"].sum())
    stance_failed5 = int(l5["7. Stance classification"].sum())
    rows = [
        ("identified", "Records identified in PubMed (monthly windows, January 2021-April 2026)", int(get("1.")["records out"])),
        ("dup", "Excluded: duplicate PMIDs across monthly windows", int(get("2.")["excluded/missing"])),
        ("unique", "Unique records", int(get("2.")["records out"])),
        ("conf", "Excluded: conference proceedings or preprints", int(get("3.")["excluded/missing"])),
        ("sjr_screened", "Records screened for SJR quartile", int(get("3.")["records out"])),
        ("unmatched", "Excluded: not Q1/Q2 in SJR (unmatched)", int(get("4.")["excluded/missing"])),
        ("unmatched_notinsjr", "  of which journal title not in SJR file", 5092),
        ("unmatched_noq", "  of which listed with no quartile", 1494),
        ("unmatched_q4", "  of which best quartile Q4", 1336),
        ("q3", "Set aside: best quartile Q3 (comparison arm)", int(get("4b.")["records out"])),
        ("q1q2", "Q1/Q2 records", int(get("5.")["records in"])),
        ("window_out", "Excluded: outside the 2021-2025 window", int(get("5.")["excluded/missing"]) + n_2026 + n_other),
        ("window_after_apr26", "  of which cover date May 2026 or later (not retained on disk)", int(get("5.")["excluded/missing"])),
        ("window_2026", "  of which published January-April 2026", n_2026),
        ("window_pre2021", "  of which dated before 2021", n_other),
        ("eligible", "Q1/Q2 records eligible, 2021-2025 (screened by the AI-engagement prefilter)", int(in5.sum())),
        ("pref_excl", "Excluded: application (AI used as a method)", len(ap5)),
        ("pref_fallback", "  of which prefilter failures defaulted to application", fallback5),
        ("retained", "AI-engaged records retained", len(de5)),
        ("retained_disc", "  discourse", int((de5["paper_type"] == "discourse").sum())),
        ("retained_eval", "  evaluative", int((de5["paper_type"] == "evaluative").sum())),
        ("stance_failed", "Excluded: stance unparseable (FAILED)", stance_failed5),
        ("analytic", "Included in analysis (valid stance, 2021-2025)", len(v)),
        ("analytic_disc", "  discourse", int((v["paper_type"] == "discourse").sum())),
        ("analytic_eval", "  evaluative", int((v["paper_type"] == "evaluative").sum())),
    ]
    f = pd.DataFrame(rows, columns=["key", "label", "n"])
    k = dict(zip(f.key, f.n))
    assert k["identified"] - k["dup"] == k["unique"]
    assert k["unique"] - k["conf"] == k["sjr_screened"]
    assert k["unmatched_notinsjr"] + k["unmatched_noq"] + k["unmatched_q4"] == k["unmatched"]
    assert k["q1q2"] - k["window_out"] == k["eligible"], (k["q1q2"], k["window_out"], k["eligible"])
    assert k["eligible"] - k["pref_excl"] == k["retained"]
    assert k["retained_disc"] + k["retained_eval"] == k["retained"]
    assert k["retained"] - k["stance_failed"] == k["analytic"] == 14058
    f.to_csv(DATA / "flow_2021_2025.csv", index=False)
    return f


def subsets(v):
    th = pd.read_csv(REPO_OUT / "analysis/thematic_alarm.csv", dtype={"pmid": str}, usecols=["pmid", "themes"])
    ac = pd.read_csv(REPO_OUT / "analyses/q7_classified_ac.csv", dtype={"pmid": str},
                     usecols=["pmid", "failure_mode", "model_type"])
    crit = v[v["critical"]]
    t = crit.merge(th, on="pmid", how="left")
    a = crit.merge(ac, on="pmid", how="left")
    parsed = a[(a["failure_mode"].notna()) & (a["failure_mode"] != "FAILED") & (a["model_type"] != "FAILED")]
    ab = parsed[parsed["has_abstract"]]
    gated = ab.merge(th, on="pmid", how="left")
    gated = gated[gated["themes"].fillna("").str.lower().str.contains("hallucination")]
    sp = v[v["specialty"].notna() & (v["specialty"] != "FAILED")]
    rows = [
        ("critical", "Critical records (Alarm or Caution)", len(crit), len(v)),
        ("theme_labelled", "Critical records with a theme label", int(t["themes"].fillna("").ne("").sum()), len(crit)),
        ("mech_failed", "Mechanism classification FAILED", len(crit) - len(parsed), len(crit)),
        ("mech_parsed", "Critical records with a parsed mechanism label", len(parsed), len(crit)),
        ("title_only_crit", "Title-only records among parsed critical records", len(parsed) - len(ab), len(parsed)),
        ("abstract_crit", "Abstract-present critical records (mechanism analyses)", len(ab), len(crit)),
        ("gated", "Hallucination-gated, abstract-present critical records", len(gated), len(ab)),
        ("specialty_valid", "Records with a valid specialty label", len(sp), len(v)),
        ("specialty_failed", "Specialty classification FAILED", len(v) - len(sp), len(v)),
        ("country_resolved", "Records with a resolved first-author country", int(v["country_map"].notna().sum()), len(v)),
        ("country_unresolved", "First-author country unresolved", int(v["country_map"].isna().sum()), len(v)),
        ("affil_empty", "  of which first-author affiliation empty", int(v["first_affiliation"].fillna("").str.strip().eq("").sum()), len(v)),
        ("region_known", "Records with a known first-author region", int((v["region"].notna() & (v["region"] != "Unknown")).sum()), len(v)),
        ("region_unknown", "First-author region Unknown", int(((v["region"] == "Unknown") | v["region"].isna()).sum()), len(v)),
        ("title_only_all", "Title-only records in the analytic set", int((~v["has_abstract"]).sum()), len(v)),
    ]
    s = pd.DataFrame(rows, columns=["key", "label", "n", "denominator"])
    s.to_csv(DATA / "subsets_2021_2025.csv", index=False)
    return s


def missing():
    """T6 accounting restricted to 2021-2025 (sums of the T6 per-year breakdowns)."""
    los = pd.read_csv(OUT / "T6_losses_by_year.csv")
    los["pub_year"] = los["pub_year"].astype(str)
    l5 = los[los["pub_year"].isin([str(y) for y in Y5])].set_index("pub_year")
    rows = []
    for c in l5.columns:
        rows.append({"stage": c, **{str(y): int(l5.loc[str(y), c]) for y in Y5}, "total_2021_2025": int(l5[c].sum())})
    m = pd.DataFrame(rows)
    m.to_csv(DATA / "missing_2021_2025.csv", index=False)
    to = pd.read_csv(OUT / "T6_title_only_by_stage.csv")
    out = []
    for _, r in to.iterrows():
        ks = ns = 0; cells = {}
        for y in Y5:
            a, b = str(r[str(y)]).split("/")
            ks += int(a); ns += int(b); cells[str(y)] = f"{int(a)}/{int(b)}"
        out.append({"stage": r["stage"], **cells, "empty_abstract": ks, "N": ns, "pct": ks / ns * 100})
    t = pd.DataFrame(out)
    t.to_csv(DATA / "title_only_2021_2025.csv", index=False)
    return m, t


# ---------------------------------------------------------------------------
def cross_sectional(v):
    """Specialty, region, country, publication type and review subtypes on 2021-2025,
    with the same CI schemes as T5 (joint resample for specialty/region; within group
    for country/publication type)."""
    tab = rc.boot_group_share(v["specialty"].fillna("NA").to_numpy(), v["critical"].to_numpy(), ALL_SPECIALTIES)
    tab = tab.rename(columns={"level": "specialty"})
    fda = load_fda_device_counts(ALL_SPECIALTIES)
    tab["fda_devices"] = tab["specialty"].map(fda).astype(int)
    tab["structural_zero"] = tab["specialty"].isin(FDA_STRUCTURAL_ZERO)
    tab.to_csv(DATA / "specialty_2021_2025.csv", index=False)

    regs = sorted(v["region"].dropna().unique())
    rt = rc.boot_group_share(v["region"].fillna("NA").to_numpy(), v["critical"].to_numpy(), regs)
    rt.rename(columns={"level": "region"}).to_csv(DATA / "region_2021_2025.csv", index=False)

    cty = v[v["country_map"].notna()]
    rows = []
    for c, sub in cty.groupby("country_map"):
        if len(sub) >= 20:
            p, lo, hi = boot_share(sub["critical"].to_numpy())
            rows.append({"country": c, "k": int(sub["critical"].sum()), "n": len(sub), "point": p, "lo": lo, "hi": hi,
                         "set": ">=50" if len(sub) >= 50 else "20-49"})
    ct = pd.DataFrame(rows).sort_values(["n", "country"], ascending=[False, True])
    ct.to_csv(DATA / "country_2021_2025.csv", index=False)

    rows = []
    for pt in ["Research Article", "Review", "Letter", "Editorial", "Commentary"]:
        sub = v[v["pt5"] == pt]
        for s in rc.STANCES + ["Critical", "Neutral (as reported)", "Favourable"]:
            if s == "Neutral (as reported)":
                continue
            succ = (sub["critical"] if s == "Critical" else sub["favourable"] if s == "Favourable"
                    else sub["stance"] == s).to_numpy()
            p, lo, hi = boot_share(succ)
            rows.append({"pubtype": pt, "outcome": s, "k": int(succ.sum()), "n": len(sub), "point": p, "lo": lo, "hi": hi})
    pd.DataFrame(rows).to_csv(DATA / "pubtype_stance.csv", index=False)

    rows = []
    for st, lab in (("Systematic Review", "Systematic Review"), ("Review", "Review (narrative)")):
        sub = v[v["pt7"] == st]
        for s in ["Critical", "Alarm", "Caution", "Neutral", "Cautious Optimism", "Advocacy", "Favourable"]:
            succ = (sub["critical"] if s == "Critical" else sub["favourable"] if s == "Favourable"
                    else sub["stance"] == s).to_numpy()
            p, lo, hi = boot_share(succ)
            rows.append({"subtype": lab, "outcome": s, "k": int(succ.sum()), "n": len(sub), "point": p, "lo": lo, "hi": hi})
    pd.DataFrame(rows).to_csv(DATA / "review_subtypes.csv", index=False)
    return tab


def fda_robustness(v, spec_tab):
    """Old Table S6 on 2021-2025: same functions (spearman_report from
    run_specialty_aiadoption.py; partial Spearman as q7_phase3_analyses.py)."""
    ac = pd.read_csv(REPO_OUT / "analyses/q7_classified_ac.csv", dtype={"pmid": str}, usecols=["pmid", "model_type"])
    keep = spec_tab[spec_tab["n"] >= 30].set_index("specialty")
    crit = keep["point"]; fda = keep["fda_devices"].astype(float)
    cr = v[v["critical"] & v["has_abstract"] & v["specialty"].notna() & (v["specialty"] != "FAILED")].merge(ac, on="pmid", how="left")
    gen = cr.groupby("specialty")["model_type"].apply(lambda s: s.isin(["generative", "both"]).mean() * 100).reindex(crit.index)
    evs = v.assign(ev=v["paper_type"].eq("evaluative")).groupby("specialty")["ev"].mean().reindex(crit.index) * 100

    def partial_spearman(x, y, z):  # identical formula to q7_phase3_analyses.py::partial_spearman
        rx, ry, rz = (pd.Series(a).rank().values for a in (x, y, z))
        pear = lambda a, b: np.corrcoef(a, b)[0, 1]
        rxy, rxz, ryz = pear(rx, ry), pear(rx, rz), pear(ry, rz)
        pr = (rxy - rxz * ryz) / np.sqrt((1 - rxz ** 2) * (1 - ryz ** 2))
        df = len(x) - 3
        tt = pr * np.sqrt(df / (1 - pr ** 2))
        return pr, 2 * (1 - tdist.cdf(abs(tt), df))

    rows = []
    r = spearman_report(crit.values, fda.values)
    rows.append({"relationship": "Critical rate vs FDA cleared-device count (zero-order)", "rho": r["rho"],
                 "p_two": r["p_two"], "p_one": r["p_one"], "p_perm_one": r["p_perm_one"], "n": r["n"]})
    rho, p = spearmanr(crit.values, gen.values)
    rows.append({"relationship": "Critical rate vs generative-model share", "rho": rho, "p_two": p, "n": len(crit)})
    rho, p = spearmanr(fda.values, gen.values)
    rows.append({"relationship": "FDA cleared-device count vs generative-model share", "rho": rho, "p_two": p, "n": len(crit)})
    pr, pp = partial_spearman(crit.values, fda.values, gen.values)
    rows.append({"relationship": "Partial: critical rate vs FDA count, controlling generative-model share", "rho": pr,
                 "p_two": pp, "n": len(crit)})
    nz = fda > 0
    r2 = spearman_report(crit[nz].values, fda[nz].values)
    rows.append({"relationship": "Critical rate vs FDA count, structural zeros dropped", "rho": r2["rho"], "p_two": r2["p_two"],
                 "p_one": r2["p_one"], "p_perm_one": r2["p_perm_one"], "n": r2["n"]})
    r3 = spearman_report(evs.values, crit.values)
    rows.append({"relationship": "(sensitivity) Critical rate vs in-corpus evaluation-share proxy", "rho": r3["rho"],
                 "p_two": r3["p_two"], "p_one": r3["p_one"], "p_perm_one": r3["p_perm_one"], "n": r3["n"]})
    pd.DataFrame(rows).to_csv(DATA / "fda_robustness.csv", index=False)
    pd.DataFrame({"specialty": crit.index, "critical_pct": crit.values, "fda_devices": fda.values,
                  "generative_share_pct": gen.values, "evaluative_share_pct": evs.values,
                  "n_records": keep["n"].values, "n_critical_abstract": cr.groupby("specialty").size().reindex(crit.index).values
                  }).to_csv(DATA / "specialty_fda.csv", index=False)


def ea_within_specialty(v):
    """Old Table S8 on 2021-2025 (run_east_asia_diagnose.py logic: the ten most
    frequent East Asian specialties with >= 30 records in both groups)."""
    e = v[v["specialty"].notna() & (v["specialty"] != "FAILED")]
    ea = v[v["region"] == "East Asia"]; nw = v[v["region"].isin(["North America", "Western Europe"])]
    rows = []
    for s in ea["specialty"].value_counts().head(10).index:
        a, b = ea[ea["specialty"] == s], nw[nw["specialty"] == s]
        if len(a) < 30 or len(b) < 30:
            continue
        ba = bootstrap_ci(a[["pmid", "stance"]], lambda d: float(d["stance"].isin(["Alarm", "Caution"]).mean() * 100))
        bb = bootstrap_ci(b[["pmid", "stance"]], lambda d: float(d["stance"].isin(["Alarm", "Caution"]).mean() * 100))
        rows.append({"specialty": s, "n_ea": len(a), "k_ea": int(a["critical"].sum()), "ea_pct": a["critical"].mean() * 100,
                     "ea_lo": ba["lower"], "ea_hi": ba["upper"], "n_nawe": len(b), "k_nawe": int(b["critical"].sum()),
                     "nawe_pct": b["critical"].mean() * 100, "nawe_lo": bb["lower"], "nawe_hi": bb["upper"]})
    t = pd.DataFrame(rows)
    t["delta_pp"] = t["ea_pct"] - t["nawe_pct"]
    t.sort_values("delta_pp").to_csv(DATA / "ea_vs_nawe_within_specialty.csv", index=False)
    mix = nw[nw["specialty"].notna() & (nw["specialty"] != "FAILED")]["specialty"].value_counts(normalize=True)
    eas = ea[ea["specialty"].notna() & (ea["specialty"] != "FAILED")]
    adj = (eas.groupby("specialty")["critical"].mean().reindex(mix.index).fillna(eas["critical"].mean()) * mix).sum() * 100
    return {"ea_raw": eas["critical"].mean() * 100, "ea_reweighted": adj,
            "nawe_raw": nw[nw["specialty"].notna() & (nw["specialty"] != "FAILED")]["critical"].mean() * 100,
            "n_ea": len(eas), "n_nawe": int(len(nw[nw["specialty"].notna() & (nw["specialty"] != "FAILED")]))}


def theme_by_format(v):
    """Old Table S12 on 2021-2025 (theme prevalence among critical records, Reviews vs
    Research Articles; run_reviews_positivity_why.py H3), with within-group bootstrap CIs."""
    th = pd.read_csv(REPO_OUT / "analysis/thematic_alarm.csv", dtype={"pmid": str}, usecols=["pmid", "themes"])
    c = v[v["critical"]].merge(th, on="pmid", how="left")
    tl = c["themes"].fillna("").str.split("|")
    rows = []
    for t in rc.THEMES:
        has = tl.apply(lambda l: t in [x.strip() for x in l]).to_numpy()
        r = {"theme": rc.THEME_LABELS[t]}
        for pt, key in (("Review", "rev"), ("Research Article", "res")):
            m = (c["pt5"] == pt).to_numpy()
            p, lo, hi = boot_share(has[m])
            r.update({f"{key}_k": int(has[m].sum()), f"{key}_n": int(m.sum()), f"{key}_pct": p, f"{key}_lo": lo, f"{key}_hi": hi})
        r["delta_pp"] = r["rev_pct"] - r["res_pct"]
        rows.append(r)
    pd.DataFrame(rows).sort_values("delta_pp", ascending=False).to_csv(DATA / "theme_by_format.csv", index=False)


def advocacy_by_specialty(v):
    rows = []
    for y in (2021, 2025):
        a = v[(v["year"] == y) & (v["stance"] == "Advocacy")]
        tot = v[v["year"] == y]
        for s in ALL_SPECIALTIES + ["FAILED"]:
            k = int((a["specialty"] == s).sum()); n_s = int((tot["specialty"] == s).sum())
            rows.append({"year": y, "specialty": s, "advocacy_k": k, "advocacy_total": len(a),
                         "share_of_advocacy_pct": k / len(a) * 100 if len(a) else np.nan,
                         "records_in_specialty": n_s, "advocacy_rate_in_specialty_pct": k / n_s * 100 if n_s else np.nan})
    pd.DataFrame(rows).to_csv(DATA / "advocacy_by_specialty.csv", index=False)


# ---------------------------------------------------------------------------
def validation_ci():
    """Bootstrap CIs (1000 record resamples, seed 42) for agreement statistics that
    were reported without one, recomputed from the committed validation files."""
    out = []

    def boot_stat(n, fn_):
        d = [fn_(i) for i in rc.boot_indices(n)]
        d = [x for x in d if not np.isnan(x)]
        return np.percentile(d, [2.5, 97.5])

    from t2_stance_perclass import load_validation
    val = load_validation()
    for lab, d in (("in-scope (n=225)", val[~val["out_of_layerA"]]), ("all records (n=300)", val)):
        d = d.reset_index(drop=True)
        h, m = d["human"].to_numpy(), d["model"].to_numpy()
        q = lambda idx: rc.cohen_kappa_cm(rc.confusion(h[idx], m[idx], rc.STANCES), "quadratic")
        pt = q(np.arange(len(d))); lo, hi = boot_stat(len(d), q)
        out.append({"step": "stance", "set": lab, "statistic": "quadratic-weighted Cohen κ", "point": pt, "lo": lo, "hi": hi,
                    "n": len(d), "k": int((h == m).sum())})
        u = lambda idx: rc.cohen_kappa_cm(rc.confusion(h[idx], m[idx], rc.STANCES))
        lo, hi = boot_stat(len(d), u)
        out.append({"step": "stance", "set": lab, "statistic": "unweighted Cohen κ", "point": u(np.arange(len(d))),
                    "lo": lo, "hi": hi, "n": len(d), "k": int((h == m).sum())})
        lo_, hi_ = cp(int((h == m).sum()), len(d))
        out.append({"step": "stance", "set": lab, "statistic": "raw agreement %", "point": (h == m).mean() * 100,
                    "lo": lo_, "hi": hi_, "n": len(d), "k": int((h == m).sum()), "ci": "Clopper-Pearson"})

    import t3_mechanism_confusion as T3
    d, _, _ = T3.load()
    for axis, col, labs in (("failure mode", "failure_mode", T3.FM), ("model type", "model_type", T3.MT)):
        dd = d[d[f"human_{col}"].isin(labs) & d[col].isin(labs)].reset_index(drop=True)
        h, m = dd[f"human_{col}"].to_numpy(), dd[col].to_numpy()
        for st, f_ in (("Cohen κ", lambda c: rc.cohen_kappa_cm(c)), ("Gwet AC1", rc.gwet_ac1_cm)):
            g = lambda idx: f_(rc.confusion(h[idx], m[idx], labs))
            lo, hi = boot_stat(len(dd), g)
            out.append({"step": f"mechanism, {axis}", "set": "abstract-present (n=108)", "statistic": st,
                        "point": g(np.arange(len(dd))), "lo": lo, "hi": hi, "n": len(dd), "k": int((h == m).sum())})
        lo_, hi_ = cp(int((h == m).sum()), len(dd))
        out.append({"step": f"mechanism, {axis}", "set": "abstract-present (n=108)", "statistic": "raw agreement %",
                    "point": (h == m).mean() * 100, "lo": lo_, "hi": hi_, "n": len(dd), "k": int((h == m).sum()),
                    "ci": "Clopper-Pearson"})
        cm = rc.confusion(h, m, labs)
        out.append({"step": f"mechanism, {axis}", "set": "abstract-present (n=108)", "statistic": "κ_max",
                    "point": rc.kappa_max_cm(cm), "n": len(dd)})

    sv = pd.read_excel(REPO_OUT / "analyses/specialty_validation_sample.xlsx", sheet_name="Coding", dtype={"pmid": str})
    sv["human_specialty"] = sv["human_specialty"].fillna("").astype(str).str.strip()
    key = pd.read_csv(REPO_OUT / "analyses/specialty_validation_key.csv", dtype={"pmid": str})[["pmid", "model_specialty"]]
    s = sv[["pmid", "human_specialty"]].merge(key, on="pmid", how="left")
    UNC = "Unclear / cannot determine from abstract"
    labs = list(ALL_SPECIALTIES) + [UNC]
    s = s[s["human_specialty"].isin(labs)].reset_index(drop=True)
    h, m = s["human_specialty"].to_numpy(), s["model_specialty"].astype(str).str.strip().to_numpy()
    for st, f_ in (("Cohen κ", lambda c: rc.cohen_kappa_cm(c)), ("Gwet AC1", rc.gwet_ac1_cm)):
        g = lambda idx: f_(rc.confusion(h[idx], m[idx], labs))
        lo, hi = boot_stat(len(s), g)
        out.append({"step": "specialty", "set": "all coded (n=120)", "statistic": st, "point": g(np.arange(len(s))),
                    "lo": lo, "hi": hi, "n": len(s), "k": int((h == m).sum())})
    lo_, hi_ = cp(int((h == m).sum()), len(s))
    out.append({"step": "specialty", "set": "all coded (n=120)", "statistic": "raw agreement %", "point": (h == m).mean() * 100,
                "lo": lo_, "hi": hi_, "n": len(s), "k": int((h == m).sum()), "ci": "Clopper-Pearson"})
    out.append({"step": "specialty", "set": "all coded (n=120)", "statistic": "κ_max",
                "point": rc.kappa_max_cm(rc.confusion(h, m, labs)), "n": len(s)})

    rr = pd.read_csv(REPO_OUT / "revision_checks/rep1_stance_stability_sample.csv")
    a, b = rr["rerun_A_stance"].to_numpy(), rr["rerun_B_stance"].to_numpy()
    q = lambda idx: rc.cohen_kappa_cm(rc.confusion(a[idx], b[idx], rc.STANCES), "quadratic")
    lo, hi = boot_stat(len(rr), q)
    out.append({"step": "stance run-to-run", "set": "300 validation records, two re-inferences", "statistic": "quadratic-weighted Cohen κ",
                "point": q(np.arange(len(rr))), "lo": lo, "hi": hi, "n": len(rr), "k": int((a == b).sum())})
    lo_, hi_ = cp(int((a == b).sum()), len(rr))
    out.append({"step": "stance run-to-run", "set": "300 validation records, two re-inferences", "statistic": "raw agreement %",
                "point": (a == b).mean() * 100, "lo": lo_, "hi": hi_, "n": len(rr), "k": int((a == b).sum()), "ci": "Clopper-Pearson"})

    import a4_score_prefilter as P
    key = pd.read_csv(rc.R1 / "coding/prefilter_key.csv", dtype={"pmid": str}, keep_default_na=False)
    df = key.merge(P.read_completed(rc.R1 / "coding/completed/prefilter_audit_COMPLETED.xlsx"), on="row_id", how="left")
    pil = df[df["stratum"] == "PILOT"].reset_index(drop=True)
    hb = pil["pilot_my_label"].isin(P.KEEP).to_numpy()
    nb = np.where(pil["human_label"].isin(P.LAB3), pil["human_label"].isin(P.KEEP), ~hb)
    k2 = lambda idx: rc.cohen_kappa_cm(np.array([[(hb[idx] & nb[idx]).sum(), (hb[idx] & ~nb[idx]).sum()],
                                                 [(~hb[idx] & nb[idx]).sum(), (~hb[idx] & ~nb[idx]).sum()]]))
    lo, hi = boot_stat(len(pil), k2)
    out.append({"step": "prefilter intra-rater", "set": "20 pilot records recoded", "statistic": "KEEP/DROP Cohen κ",
                "point": k2(np.arange(len(pil))), "lo": lo, "hi": hi, "n": len(pil), "k": int((hb == nb).sum())})
    lo_, hi_ = cp(int((hb == nb).sum()), len(pil))
    out.append({"step": "prefilter intra-rater", "set": "20 pilot records recoded", "statistic": "KEEP/DROP agreement %",
                "point": (hb == nb).mean() * 100, "lo": lo_, "hi": hi_, "n": len(pil), "k": int((hb == nb).sum()), "ci": "Clopper-Pearson"})
    h3 = pil["human_label"].where(pil["human_label"].isin(P.LAB3), "unlabelled").to_numpy()
    o3 = pil["pilot_my_label"].to_numpy()
    lo_, hi_ = cp(int((h3 == o3).sum()), len(pil))
    out.append({"step": "prefilter intra-rater", "set": "20 pilot records recoded", "statistic": "3-class agreement %",
                "point": (h3 == o3).mean() * 100, "lo": lo_, "hi": hi_, "n": len(pil), "k": int((h3 == o3).sum()), "ci": "Clopper-Pearson"})
    o = pd.DataFrame(out)
    o["ci"] = o.get("ci", pd.Series(dtype=str)).fillna("percentile bootstrap, 1000 record resamples, seed 42")
    o.loc[o["statistic"] == "κ_max", "ci"] = "not applicable (bound)"
    o.to_csv(DATA / "validation_ci.csv", index=False)


def forward_validation():
    # human verdicts live in the adjudication workbook (the csv twin has the machine columns only)
    w = pd.read_excel(REPO_OUT / "analyses/prophecy/phase2_prophecy_verdicts_worksheet.xlsx", sheet_name="adjudicate",
                      dtype=str)
    cand = pd.read_csv(REPO_OUT / "analyses/prophecy/prophecy_panel_candidates_2021_2023.csv", dtype=str)
    fr = pd.read_csv(REPO_OUT / "analyses/prophecy/phase1_signature_claims_FROZEN.csv", dtype=str)
    ct = pd.crosstab(w["tier"], w["verdict"], margins=True, margins_name="Total")
    ct.to_csv(DATA / "fv_tier_verdict.csv")
    silent = pd.crosstab(w["tier"], w["corpus_silent"].str.lower())
    silent.to_csv(DATA / "fv_tier_silent.csv")
    c = {"candidates": len(cand), "frozen_papers": int(fr["pmid"].nunique()), "claims": len(w),
         "tier_counts": w["tier"].value_counts().sort_index().to_dict(), "verdicts": w["verdict"].value_counts().to_dict()}
    (DATA / "fv_counts.json").write_text(json.dumps(c, indent=2))


# ---------------------------------------------------------------------------
def extras(v):
    """Inputs for the Multimedia Appendix 3 units (all existing analyses on 2021-2025)."""
    # v2 rubric: Spearman over the 2021-2025 annual shares in the committed v2 temporal file
    t2 = pd.read_csv(REPO_OUT / "analyses/temporal_stance_v2.csv")
    t2 = t2[t2.pub_year.between(2021, 2025)]
    rows = []
    for s in rc.STANCES + ["Critical"]:
        if s == "Critical":
            x = t2[t2.stance.isin(["Alarm", "Caution"])].groupby("pub_year")["point"].sum()
        else:
            x = t2[t2.stance == s].set_index("pub_year")["point"]
        x = x.reindex(Y5)
        rho, p, _ = rc.spearman_exact(Y5, x.to_numpy())
        rows.append({"stance": s, "v2_2021": x.iloc[0], "v2_2025": x.iloc[-1], "rho": rho, "P_exact": p})
    pd.DataFrame(rows).to_csv(DATA / "v2_trend.csv", index=False)

    # pooled theme prevalence among critical records, 2021-2025
    th = pd.read_csv(REPO_OUT / "analysis/thematic_alarm.csv", dtype={"pmid": str}, usecols=["pmid", "themes"])
    c = v[v["critical"]].merge(th, on="pmid", how="left")
    tl = c["themes"].fillna("").str.split("|")
    rows = []
    for t in rc.THEMES:
        has = tl.apply(lambda l: t in [x.strip() for x in l]).to_numpy()
        p, lo, hi = boot_share(has)
        rows.append({"theme": rc.THEME_LABELS[t], "k": int(has.sum()), "n": len(has), "point": p, "lo": lo, "hi": hi})
    pd.DataFrame(rows).to_csv(DATA / "theme_pooled.csv", index=False)

    # Q3 arm pooled 2021-2025 stance distribution
    q3 = pd.read_csv(DATA_ROOT / "classified_medical_Q3.csv", low_memory=False, dtype={"pmid": str})
    q3 = q3.loc[:, ~q3.columns.duplicated()]
    q3["pub_year"] = pd.to_numeric(q3["pub_year"], errors="coerce")
    q3 = q3[(q3["stance"] != "FAILED") & q3["pub_year"].between(2021, 2025)]
    rows = []
    for s in rc.STANCES + ["Critical", "Favourable"]:
        succ = (q3["stance"].isin(["Alarm", "Caution"]) if s == "Critical" else q3["stance"].isin(["Cautious Optimism", "Advocacy"])
                if s == "Favourable" else q3["stance"] == s).to_numpy()
        p, lo, hi = boot_share(succ)
        rows.append({"stance": s, "k": int(succ.sum()), "n": len(succ), "point": p, "lo": lo, "hi": hi})
    pd.DataFrame(rows).to_csv(DATA / "q3_pooled.csv", index=False)

    # B5 annual critical and Advocacy shares by corpus definition (b5_sjr_medical_sensitivity.py restriction)
    import b5_sjr_medical_sensitivity as B5
    q = pd.read_csv(OUT / "T7_record_level_quartiles.csv", dtype={"pmid": str})
    w = v.merge(q.drop(columns=["journal", "year"]), on="pmid", how="left")
    rows = []
    for name, col in B5.DEFS.items():
        keep = pd.Series(True, index=w.index) if col is None else w[col].isin(["Q1", "Q2"])
        d = w[keep].reset_index(drop=True)
        for out, succ in (("Critical", d["critical"]), ("Advocacy", d["stance"] == "Advocacy")):
            tab = rc.boot_group_share(d["year"].to_numpy(), succ.to_numpy(), Y5)
            for r in tab.itertuples():
                rows.append({"definition": name, "outcome": out, "year": int(r.level), "k": int(r.k), "n": int(r.n),
                             "point": r.point, "lo": r.lo, "hi": r.hi})
    pd.DataFrame(rows).to_csv(DATA / "b5_annual.csv", index=False)

    # B2: recovered vs retained stance distribution, 2021-2025
    a2 = rc.read_str(OUT / "A2/a2_fullabstract_labels.csv")
    b2 = rc.read_str(OUT / "B2/b2_stance_labels.csv").merge(a2[["pmid", "year"]], on="pmid")
    b2 = b2[(b2.failed != "1") & b2.year.isin([str(y) for y in Y5])]
    rows = []
    for name, st in (("Retained (production corpus)", v["stance"]), ("Recovered (B2)", b2["stance"])):
        for s in rc.STANCES + ["Critical"]:
            succ = (st.isin(["Alarm", "Caution"]) if s == "Critical" else st == s).to_numpy()
            p, lo, hi = boot_share(succ)
            rows.append({"set": name, "stance": s, "k": int(succ.sum()), "n": len(succ), "point": p, "lo": lo, "hi": hi})
    pd.DataFrame(rows).to_csv(DATA / "b2_recovered_vs_retained.csv", index=False)

    # validation confusion matrices (stance S18 a/b)
    from t2_stance_perclass import load_validation
    val = load_validation()
    for tag, d in (("inscope225", val[~val["out_of_layerA"]]), ("all300", val)):
        cm = rc.confusion(d["human"], d["model"], rc.STANCES)
        pd.DataFrame(cm, index=rc.STANCES, columns=rc.STANCES).to_csv(DATA / f"stance_confusion_{tag}.csv")


def main():
    v = base_2125()
    assert len(v) == 14058
    flow(v); subsets(v); missing()
    tab = cross_sectional(v)
    fda_robustness(v, tab)
    ea = ea_within_specialty(v)
    (DATA / "ea_reweighting.json").write_text(json.dumps(ea, indent=2))
    theme_by_format(v)
    advocacy_by_specialty(v)
    validation_ci()
    forward_validation()
    extras(v)
    print("c1_compute done")


if __name__ == "__main__":
    main()
