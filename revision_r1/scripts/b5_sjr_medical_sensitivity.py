"""B5 · SJR medical-category sensitivity (JMIR R1 Batch 2b; D6).
Pre-specified in ANALYSIS_PLAN_batch2b.md. Restriction only: an analytic
record is kept when its journal-year is Q1/Q2 in at least one category of the
definition (Batch 1 T7 record-level quartiles); nothing is re-classified.
Outputs: revision_r1/outputs/B5/
"""

from __future__ import annotations

import sys

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

from r1_common import (OUT, REPO, REPO_OUT, STANCES, boot_group_share, boot_indices, fmt_p, load_v1,
                       logit_trend, md_table, spearman_exact)

sys.path.insert(0, str(REPO))
from analysis.robustness import simplify_pubtype_5  # noqa: E402
from analysis.run_specialty_aiadoption import ALL_SPECIALTIES, load_fda_device_counts  # noqa: E402

B5 = OUT / "B5"; B5.mkdir(parents=True, exist_ok=True)
Y5 = [2021, 2022, 2023, 2024, 2025]
DEFS = {"Full corpus": None,
        "D1 Medicine area (primary)": "D1 Medicine area (ASJC 27xx) categories",
        "D2 D1 minus Medicine (misc.)": "D2 D1 minus 'Medicine (miscellaneous)'",
        "D3 broad health sciences": "D3 broad health sciences (Medicine, Nursing, Dentistry, Health Professions, "
                                    "Neuroscience, Pharmacology, Immunology & Microbiology, Psychology)"}
THEMES4 = {"safety_clinical": "Patient safety", "hallucination": "Hallucination / errors",
           "regulation": "Governance / regulation", "ethics_bias": "Ethics & bias"}


def pe(p):
    """JMIR-style P: 'P<.001' or 'P=.xxx'."""
    f = fmt_p(p)
    return f"P{f}" if f.startswith("<") else f"P={f}"


def share_ci(x):
    x = np.asarray(x, float)
    d = [x[i].mean() * 100 for i in boot_indices(len(x))]
    return x.mean() * 100, *np.percentile(d, [2.5, 97.5])


def trend(years, success):
    tab = boot_group_share(years, success, Y5)
    rho, p, _ = spearman_exact(Y5, tab["point"].to_numpy())
    lt = logit_trend(years, success)
    return tab, rho, p, lt


def main():
    v = load_v1(year_range=(2021, 2026))
    q = pd.read_csv(OUT / "T7_record_level_quartiles.csv", dtype={"pmid": str})
    v = v.merge(q.drop(columns=["journal", "year"]), on="pmid", how="left")
    spec = pd.read_csv(REPO_OUT / "specialty_classifications.csv", dtype={"pmid": str}, usecols=["pmid", "specialty"])
    geo = pd.read_csv(REPO_OUT / "geography_classifications.csv", dtype={"pmid": str}, usecols=["pmid", "region"])
    th = pd.read_csv(REPO_OUT / "analysis/thematic_alarm.csv", dtype={"pmid": str}, usecols=["pmid", "themes"])
    v = v.merge(spec, on="pmid", how="left").merge(geo, on="pmid", how="left").merge(th, on="pmid", how="left")
    v["pt5"] = v["pub_type"].fillna("").map(simplify_pubtype_5)
    v["year"] = v["pub_year"].astype(int)
    fda = load_fda_device_counts(ALL_SPECIALTIES)

    rows, removed = [], []
    for name, col in DEFS.items():
        keep = pd.Series(True, index=v.index) if col is None else v[col].isin(["Q1", "Q2"])
        d = v[keep].reset_index(drop=True)
        if col is not None:
            rm = v[~keep]
            removed.append({"definition": name, **{str(y): int((rm.year == y).sum()) for y in Y5 + [2026]},
                            "total removed": len(rm), "kept": len(d)})
        add = lambda sec, item, val, extra="": rows.append({"definition": name, "section": sec, "item": item,
                                                             "value": val, "detail": extra})
        for win, ys in (("2021–Apr 2026", Y5 + [2026]), ("2021–2025", Y5)):
            dw = d[d.year.isin(ys)]
            for s in STANCES + ["Critical", "Favourable"]:
                succ = dw["critical"] if s == "Critical" else dw["favourable"] if s == "Favourable" else dw["stance"] == s
                p, lo, hi = share_ci(succ)
                add(f"Stance distribution, {win}", s, f"{p:.1f}% ({lo:.1f}–{hi:.1f}); {int(succ.sum()):,}/{len(dw):,}")
        d5 = d[d.year.isin(Y5)]
        for lab, succ in (("Critical", d5["critical"]), ("Advocacy", d5["stance"] == "Advocacy")):
            tab, rho, p, lt = trend(d5["year"].to_numpy(), succ.to_numpy())
            ann = "; ".join(f"{int(r.level)} {r.point:.1f}% ({int(r.k)}/{int(r.n)})" for r in tab.itertuples())
            add("Trend 2021–2025", lab, f"ρ={rho:+.2f} (exact {pe(p)}); OR/yr {lt['OR']:.3f} ({lt['OR_lo']:.3f}–{lt['OR_hi']:.3f}), {pe(lt['P_wald'])}", ann)
        cr = d5[d5["critical"]]
        tl = cr["themes"].fillna("").str.split("|")
        for t, lab in THEMES4.items():
            has = tl.apply(lambda l: t in l).to_numpy()
            tab, rho, p, lt = trend(cr["year"].to_numpy(), has)
            add("Theme trend 2021–2025 (among critical)", lab,
                f"{tab.point.iloc[0]:.1f}% → {tab.point.iloc[-1]:.1f}% (Δ {tab.point.iloc[-1]-tab.point.iloc[0]:+.1f} pp); "
                f"ρ={rho:+.2f} (exact {pe(p)}); OR/yr {lt['OR']:.3f} ({lt['OR_lo']:.3f}–{lt['OR_hi']:.3f})")
        # cross-sectional, 2021–Apr 2026 analytic set as in the manuscript, and 2021–2025
        for win, ys in (("2021–Apr 2026", Y5 + [2026]), ("2021–2025", Y5)):
            dw = d[d.year.isin(ys)]
            sp = dw[dw["specialty"].notna() & (dw["specialty"] != "FAILED")]
            tab = boot_group_share(dw["specialty"].fillna("NA").to_numpy(), dw["critical"].to_numpy(), ALL_SPECIALTIES)
            ok = tab[tab.n >= 30]
            rho, p = spearmanr(ok.set_index("level")["point"], fda.reindex(ok.level))
            hi_, lo_ = ok.sort_values("point").iloc[-1], ok.sort_values("point").iloc[0]
            add(f"Specialty, {win}", "range (n≥30 categories)",
                f"{hi_.level} {hi_.point:.1f}% ({int(hi_.k)}/{int(hi_.n)}) to {lo_.level} {lo_.point:.1f}% ({int(lo_.k)}/{int(lo_.n)})",
                f"{len(ok)} categories with n≥30")
            add(f"Specialty, {win}", "FDA Spearman ρ", f"{rho:+.2f} (two-sided {pe(p)}, n={len(ok)})")
            for r in tab.itertuples():
                rows.append({"definition": name, "section": f"Specialty detail, {win}", "item": r.level,
                             "value": f"{r.point:.1f}% ({r.lo:.1f}–{r.hi:.1f})", "detail": f"{int(r.k)}/{int(r.n)}"})
            regs = sorted(dw["region"].dropna().unique())
            rt = boot_group_share(dw["region"].fillna("NA").to_numpy(), dw["critical"].to_numpy(), regs)
            for r in rt.itertuples():
                add(f"Region, {win}", r.level, f"{r.point:.1f}% ({r.lo:.1f}–{r.hi:.1f}); {int(r.k):,}/{int(r.n):,}")
            for pt in ["Research Article", "Review", "Letter", "Editorial", "Commentary"]:
                s_ = dw[dw.pt5 == pt]
                p_, lo, hi = share_ci(s_["critical"])
                add(f"Publication type, {win}", pt, f"{p_:.1f}% ({lo:.1f}–{hi:.1f}); {int(s_['critical'].sum()):,}/{len(s_):,}")
    R = pd.DataFrame(rows)
    R.to_csv(B5 / "B5_long.csv", index=False)
    RM = pd.DataFrame(removed)
    RM.to_csv(B5 / "B5_removed_by_year.csv", index=False)

    L = ["# B5 · SJR medical-category sensitivity (D6)\n",
         "Script `revision_r1/scripts/b5_sjr_medical_sensitivity.py`. Restricted corpora keep an analytic record only if its "
         "journal-year is Q1/Q2 in at least one category of the definition (Batch 1 T7). D1 is primary; D2 and D3 are bounds. "
         "CIs: 95% percentile bootstrap, 1000 resamples, seed 42. Long table: [B5_long.csv](B5_long.csv).\n",
         "## Records removed, by year\n", md_table(RM, "{:.0f}"), ""]
    secs = [s for s in R.section.unique() if not s.startswith("Specialty detail")]
    for sec in secs:
        sub = R[R.section == sec]
        piv = sub.pivot_table(index="item", columns="definition", values="value", aggfunc="first", sort=False)
        piv = piv[[c for c in DEFS if c in piv.columns]]
        L += [f"## {sec}\n", md_table(piv.reset_index()), ""]
    (B5 / "B5_sjr_sensitivity.md").write_text("\n".join(L) + "\n")
    print("\n".join(L[:40]))


if __name__ == "__main__":
    main()
