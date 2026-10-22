"""Cross-sectional analyses on both windows (rule 12), feeding the T5 ledger.

Computes, for the submitted analytic set (2021 to April 2026) and for 2021–2025
side by side: overall stance distribution, specialty critical rate, FDA and
generative-share correlations, first-author country and region critical
rates, East Asia specialty-mix reweighting, publication type × stance,
opinion vs research χ² / Cramér's V, review subtypes.

Reuses the original functions (imported, not modified):
  analysis.robustness.simplify_pubtype_5 / simplify_pubtype_7
  analysis.run_country_critical_map.resolve_country
  analysis.run_specialty_aiadoption.load_fda_device_counts, ALL_SPECIALTIES
No figures are produced (cross-sectional figure regeneration is pending).
"""

from __future__ import annotations

import sys

import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency, spearmanr

from r1_common import (OUT, REPO, REPO_OUT, STANCES, boot_group_share, boot_indices, load_v1,
                       md_table)

sys.path.insert(0, str(REPO))
from analysis.robustness import simplify_pubtype_5, simplify_pubtype_7  # noqa: E402
from analysis.run_country_critical_map import resolve_country  # noqa: E402
from analysis.run_specialty_aiadoption import ALL_SPECIALTIES, load_fda_device_counts  # noqa: E402

WINDOWS = {"2021–Apr 2026 (submitted)": (2021, 2026), "2021–2025": (2021, 2025)}
OPINION = ["Commentary", "Letter", "Editorial"]


def boot_share_ci(x):
    x = np.asarray(x, float)
    d = [x[i].mean() * 100 for i in boot_indices(len(x))]
    lo, hi = np.percentile(d, [2.5, 97.5])
    return x.mean() * 100, lo, hi


def main():
    base = load_v1(year_range=(2021, 2026))
    spec = pd.read_csv(REPO_OUT / "specialty_classifications.csv", dtype={"pmid": str},
                       usecols=["pmid", "specialty"])
    geo = pd.read_csv(REPO_OUT / "geography_classifications.csv", dtype={"pmid": str},
                      usecols=["pmid", "country", "region"])
    ac = pd.read_csv(REPO_OUT / "analyses/q7_classified_ac.csv", dtype={"pmid": str},
                     usecols=["pmid", "model_type"])
    base = base.merge(spec, on="pmid", how="left").merge(geo.rename(columns={"country": "country_geo"}),
                                                         on="pmid", how="left").merge(ac, on="pmid", how="left")
    base["country_map"] = base["first_affiliation"].map(resolve_country)
    base["pt5"] = base["pub_type"].fillna("").map(simplify_pubtype_5)
    base["pt7"] = base["pub_type"].fillna("").map(simplify_pubtype_7)
    fda = load_fda_device_counts(ALL_SPECIALTIES)

    rows = []  # long: window, analysis, group, metric, value, lo, hi, k, n

    def add(w, analysis, group, metric, value, lo=np.nan, hi=np.nan, k=np.nan, n=np.nan):
        rows.append({"window": w, "analysis": analysis, "group": group, "metric": metric,
                     "value": value, "lo": lo, "hi": hi, "k": k, "n": n})

    for w, (a, b) in WINDOWS.items():
        df = base[base["pub_year"].between(a, b)].reset_index(drop=True)
        N = len(df)
        add(w, "Overall", "All", "records", N, n=N)
        # overall stance distribution (joint bootstrap over all records)
        for s in STANCES + ["Critical", "Favourable"]:
            succ = (df["critical"] if s == "Critical" else df["favourable"] if s == "Favourable"
                    else df["stance"] == s).to_numpy()
            p, lo, hi = boot_share_ci(succ)
            add(w, "Overall stance", s, "pct", p, lo, hi, int(succ.sum()), N)

        # specialty
        sp = df[df["specialty"].notna() & (df["specialty"] != "FAILED")].reset_index(drop=True)
        add(w, "Specialty", "valid", "records", len(sp), n=len(sp))
        add(w, "Specialty", "FAILED or missing", "records", N - len(sp), n=N)
        # resample all records (FAILED/missing included, excluded from denominators), as
        # bootstrap_ci(v1, critical_by_specialty) in run_specialty_critical.py
        tab = boot_group_share(df["specialty"].fillna("NA").to_numpy(), df["critical"].to_numpy(),
                               ALL_SPECIALTIES)
        keep = tab[tab["n"] >= 30]
        for _, r in tab.iterrows():
            add(w, "Specialty critical", r["level"], "pct", r["point"], r["lo"], r["hi"], r["k"], r["n"])
        crit = keep.set_index("level")["point"]
        f = fda.reindex(crit.index)
        rho, p = spearmanr(crit, f)
        add(w, "Specialty × FDA", "all categories (n≥30)", "spearman_rho", rho, n=len(crit))
        add(w, "Specialty × FDA", "all categories (n≥30)", "P_two_sided", p, n=len(crit))
        nz = f > 0
        rho2, p2 = spearmanr(crit[nz], f[nz])
        add(w, "Specialty × FDA", "structural zeros dropped", "spearman_rho", rho2, n=int(nz.sum()))
        add(w, "Specialty × FDA", "structural zeros dropped", "P_two_sided", p2, n=int(nz.sum()))
        cr = sp[sp["critical"] & sp["has_abstract"]]  # abstract-present, as q7_ac_by_specialty_abstractonly
        gshare = cr.groupby("specialty")["model_type"].apply(lambda s: s.isin(["generative", "both"]).mean() * 100)
        gshare = gshare.reindex(crit.index)
        rho3, p3 = spearmanr(crit, gshare)
        add(w, "Specialty × generative share", "all categories (n≥30)", "spearman_rho", rho3, n=len(crit))
        add(w, "Specialty × generative share", "all categories (n≥30)", "P_two_sided", p3, n=len(crit))

        # country (resolver used for Figure 4 / Table S7; per-country bootstrap, seed 42)
        cty = df[df["country_map"].notna()]
        add(w, "Country", "resolved", "records", len(cty), n=N)
        add(w, "Country", "resolved", "pct_resolved", len(cty) / N * 100, k=len(cty), n=N)
        for c, sub in cty.groupby("country_map"):
            if len(sub) >= 20:
                p_, lo_, hi_ = boot_share_ci(sub["critical"].to_numpy())
                add(w, "Country critical", c, "pct", p_, lo_, hi_, int(sub["critical"].sum()), len(sub))
        add(w, "Country", "countries with n≥50", "count", int((cty["country_map"].value_counts() >= 50).sum()))
        add(w, "Country", "countries with n≥20", "count", int((cty["country_map"].value_counts() >= 20).sum()))

        # region (joint bootstrap, as run_region_critical.py)
        regs = sorted(df["region"].dropna().unique())
        tab = boot_group_share(df["region"].fillna("NA").to_numpy(), df["critical"].to_numpy(), regs)
        for _, r in tab.iterrows():
            add(w, "Region critical", r["level"], "pct", r["point"], r["lo"], r["hi"], r["k"], r["n"])
        # East Asia reweighting (run_east_asia_diagnose.py logic)
        e = df[df["specialty"].notna() & (df["specialty"] != "FAILED")]
        ea = e[e["region"] == "East Asia"]
        nw = e[e["region"].isin(["North America", "Western Europe"])]
        mix = nw["specialty"].value_counts(normalize=True)
        ea_spec = ea.groupby("specialty")["critical"].mean().reindex(mix.index).fillna(ea["critical"].mean())
        adj = (ea_spec * mix).sum() * 100
        raw_ea = ea["critical"].mean() * 100; raw_nw = nw["critical"].mean() * 100
        add(w, "East Asia reweighting", "EA raw", "pct", raw_ea, n=len(ea))
        add(w, "East Asia reweighting", "EA reweighted to NA+WEU specialty mix", "pct", adj, n=len(ea))
        add(w, "East Asia reweighting", "NA+WEU raw", "pct", raw_nw, n=len(nw))
        add(w, "East Asia reweighting", "share of gap closed", "pct", (adj - raw_ea) / (raw_nw - raw_ea) * 100)

        # publication type
        pts = ["Research Article", "Review", "Letter", "Editorial", "Commentary"]
        for pt in pts:
            sub = df[df["pt5"] == pt]
            for s in STANCES + ["Critical", "Favourable"]:
                succ = (sub["critical"] if s == "Critical" else sub["favourable"] if s == "Favourable"
                        else sub["stance"] == s).to_numpy()
                p_, lo_, hi_ = boot_share_ci(succ)
                add(w, f"Pub type: {pt}", s, "pct", p_, lo_, hi_, int(succ.sum()), len(sub))
        op = df[df["pt5"].isin(OPINION)]
        p_, lo_, hi_ = boot_share_ci(op["critical"].to_numpy())
        add(w, "Pub type: opinion pooled (Comm+Letter+Ed)", "Critical", "pct", p_, lo_, hi_,
            int(op["critical"].sum()), len(op))
        two = df[df["pt5"].isin(OPINION + ["Research Article"])]
        ct = pd.crosstab(two["pt5"].isin(OPINION), two["stance"]).reindex(columns=STANCES, fill_value=0)
        chi2, pchi, dof, _ = chi2_contingency(ct)
        v = np.sqrt(chi2 / (ct.values.sum() * (min(ct.shape) - 1)))
        add(w, "Opinion vs Research Article stance", "χ²", "chi2", chi2, n=int(ct.values.sum()))
        add(w, "Opinion vs Research Article stance", "df", "df", dof)
        add(w, "Opinion vs Research Article stance", "P", "P", pchi)
        add(w, "Opinion vs Research Article stance", "Cramér's V", "V", v)
        # review subtypes (7-bucket: Systematic Review vs Review)
        for st in ["Systematic Review", "Review"]:
            sub = df[df["pt7"] == st]
            for s in ["Critical", "Alarm", "Caution", "Cautious Optimism", "Advocacy", "Neutral"]:
                succ = (sub["critical"] if s == "Critical" else sub["stance"] == s).to_numpy()
                p_, lo_, hi_ = boot_share_ci(succ)
                add(w, f"Review subtype: {st if st != 'Review' else 'Review (narrative)'}", s, "pct",
                    p_, lo_, hi_, int(succ.sum()), len(sub))

    out = pd.DataFrame(rows)
    out.to_csv(OUT / "T5_crosssectional_both_windows.csv", index=False)

    # side-by-side markdown
    W1, W2 = list(WINDOWS)
    piv = []
    for (an, gr, me), g in out.groupby(["analysis", "group", "metric"], sort=False):
        r = {"analysis": an, "group": gr, "metric": me}
        for w in (W1, W2):
            x = g[g.window == w]
            if not len(x):
                r[w] = ""; continue
            x = x.iloc[0]
            if me == "pct":
                r[w] = (f"{x.value:.1f}" + (f" ({x.lo:.1f}–{x.hi:.1f})" if not np.isnan(x.lo) else "")
                        + (f"; {int(x.k):,}/{int(x.n):,}" if not np.isnan(x.k) else (f"; n={int(x.n):,}" if not np.isnan(x.n) else "")))
            elif me in ("records", "count", "df"):
                r[w] = f"{int(x.value):,}"
            elif me == "P" or me == "P_two_sided":
                r[w] = f"{x.value:.4f}" if x.value >= 1e-4 else f"{x.value:.1e}"
            else:
                r[w] = f"{x.value:.3f}" + (f" (n={int(x.n)})" if not np.isnan(x.n) else "")
        piv.append(r)
    piv = pd.DataFrame(piv)
    piv.to_csv(OUT / "T5_crosssectional_side_by_side.csv", index=False)
    L = ["# Cross-sectional analyses on both windows (rule 12)\n",
         "Script: `revision_r1/scripts/t5_crosssectional.py`. Left column = submitted analytic set "
         "(2021 to April 2026, 16,747 records); right column = 2021–2025 only. CIs: 95% percentile bootstrap "
         "(1000 resamples, seed 42); specialty and region use a joint resample of all records (as "
         "run_specialty_critical.py / run_region_critical.py), country and publication type resample within "
         "group. Country uses the resolver behind Figure 4 / Table S7 (`resolve_country`), region uses "
         "`output/geography_classifications.csv`. No figures regenerated.\n",
         md_table(piv)]
    (OUT / "T5_crosssectional_both_windows.md").write_text("\n".join(L) + "\n")
    print(f"{len(out)} rows")


if __name__ == "__main__":
    main()
