"""T5 · Claims ledger (E12, E4, E13).

Every sentence containing a digit in the Abstract, Results body and figure
captions of the submitted manuscript is listed with: values, n, N, CI and
method, source script and output, reproduced (Y/N/partial), the 2021–2025
value where the quantity is temporal or cross-sectional, and flags for
percentages without a CI or without n/N. Discussion numbers are listed
separately. Recomputed values come from the T1–T4 outputs and
t5_crosssectional.py; nothing in the manuscript is edited.
"""

from __future__ import annotations

import re

import numpy as np
import pandas as pd

from r1_common import OUT, REPO_OUT, load_v1, read_str, DATA_ROOT
from t5_extract import quantitative_sentences

ANN = pd.read_csv(OUT / "T4_annual_all_domains.csv")
TR = pd.read_csv(OUT / "T4_trend_tests.csv")
X = pd.read_csv(OUT / "T5_crosssectional_both_windows.csv")
W5, W6 = "2021–2025", "2021–2026 (submitted)"
XW6, XW5 = "2021–Apr 2026 (submitted)", "2021–2025"


def a(dom, out, year, w=W5):
    r = ANN[(ANN.domain == dom) & (ANN.outcome == out) & (ANN.window == w) & (ANN.year == year)].iloc[0]
    return r


def ap(dom, out, year, w=W5, ci=True):
    r = a(dom, out, year, w)
    s = f"{r.pct:.1f}%"
    if ci:
        s += f" ({r.lo:.1f}–{r.hi:.1f})"
    return s + f" [{int(r.k)}/{int(r.N)}]"


def tr(dom, out, w=W5):
    r = TR[(TR.domain == dom) & (TR.outcome == out) & (TR.window == w)].iloc[0]
    p = r.P_exact_perm
    ps = "<.001" if p < .001 else f"{p:.3f}".lstrip("0")
    return f"ρ={r.rho:+.2f} (exact P={ps})"


def orr(dom, out, w=W5):
    r = TR[(TR.domain == dom) & (TR.outcome == out) & (TR.window == w)].iloc[0]
    p = r.P_wald
    ps = "<.001" if p < .001 else f"{p:.3f}".lstrip("0")
    return f"OR/yr {r.OR_per_year:.3f} ({r.OR_lo:.3f}–{r.OR_hi:.3f}), P={ps}"


def x(an, grp, metric="pct", w=XW5, ci=True):
    r = X[(X.analysis == an) & (X.group == grp) & (X.metric == metric) & (X.window == w)].iloc[0]
    if metric == "pct":
        s = f"{r.value:.1f}%"
        if ci and not np.isnan(r.lo):
            s += f" ({r.lo:.1f}–{r.hi:.1f})"
        if not np.isnan(r.k):
            s += f" [{int(r.k):,}/{int(r.n):,}]"
        elif not np.isnan(r.n):
            s += f" [n={int(r.n):,}]"
        return s
    if metric in ("records", "count"):
        return f"{int(r.value):,}"
    return f"{r.value:.3f}"


S, TH, GATE, MECH, GEN = ("Stance", "Theme (among critical)", "Mechanism, hallucination-gated (failure-mode composition)",
                          "Mechanism, all abstract-present critical", "Mechanism, generative-model papers")
FAB = "Mechanism, hallucination-gated"
CRIT = "Critical (Alarm+Caution)"
BOOT = "95% percentile bootstrap, 1000 resamples, seed 42"


def build_annotations():
    v1all = load_v1(year_range=None, drop_failed=False)
    n_failed = int((v1all.stance == "FAILED").sum())
    n2020 = int(((v1all.stance != "FAILED") & (v1all.pub_year == 2020)).sum())
    yr_gated = {y: a(FAB, "Fabrication-involved (confabulation or both)", y, W6).pct for y in range(2021, 2027)}
    gen_fab = {y: a(GEN, "Fabrication share among generative", y, W6).pct for y in range(2021, 2027)}
    misc_rng6 = [a(GATE, "Misclassification (factual error)", y, W6).pct for y in range(2021, 2027)]
    misc_rng5 = misc_rng6[:5]
    mf = __import__("json").loads((OUT / "T4_mechanism_facts.json").read_text())
    co5 = [a(S, "Cautious Optimism", y).pct for y in range(2021, 2026)]
    ratio = pd.read_csv(OUT / "T4_genre_ratio.csv")
    t1 = pd.read_csv(OUT / "T1_binary_keep_drop_metrics.csv")

    A = {}
    A["A03"] = dict(values="97,492 eligible; 16,759 retained; 16,749 valid labels", n="16,759; 16,749", N="97,492",
                    script="sjr_filter.py; prefilter_batch.py; classify_stance_batch.py",
                    output="filtered_medical_all_Q1Q2.csv; prefiltered_discourse_eval.csv; classified_medical_Q1Q2.csv",
                    rep=f"Y (FAILED stance = {n_failed})", new="stance set 2021–2025: 14,058 records")
    A["A04"] = dict(values="κ 0.51; quadratic κ 0.79 (0.72–0.84); κ 0.75; κ 0.84; κ 0.57", ci="0.72–0.84 (stance only)",
                    method=BOOT + " (stance); prefilter CI not given here", script="compute_kappa.py; q7_kappa.py; T1/T3 scripts",
                    output="output/validation/kappa_report.md; output/analyses/q7_kappa_report_abstractonly.md; specialty_kappa_report.md",
                    rep="Y for prefilter, stance, model type, failure mode (T1–T3); specialty κ not recomputed in Batch 1 (report file only)",
                    note="Only the stance κ carries a CI; prefilter κ CI 0.35–0.68 in Methods does not reproduce (T1: 0.345–0.646).")
    A["A05"] = dict(values="Cautious Optimism 62.8%; critical 30.8%", n="10,514; 5,161", N="16,747",
                    ci=f"recomputed {x('Overall stance','Cautious Optimism',w=XW6)}; {x('Overall stance','Critical',w=XW6)}",
                    method=BOOT, script="analysis/robustness.py (load_classifications)", output="data/analytic_dataset.csv",
                    rep="Y", new=f"CO {x('Overall stance','Cautious Optimism')}; critical {x('Overall stance','Critical')}")
    A["A06"] = dict(values="Advocacy 2.9%→0.6%, ρ −1.00; critical 25.4% (22.9–28.1)→32.6% (30.9–34.4)",
                    n="Advocacy 31; 17. Critical 270; 878", N="1,063 (2021); 2,689 (2026)", ci="critical only", method=BOOT + " (joint resample)",
                    script="analysis/run_temporal_stance.py", output="output/analyses/temporal_stance_v1.csv; temporal_stance_trends.csv",
                    rep="Y", new=f"Advocacy {ap(S,'Advocacy',2021)} → {ap(S,'Advocacy',2025)}, {tr(S,'Advocacy')}, {orr(S,'Advocacy')}; critical {ap(S,CRIT,2021)} → {ap(S,CRIT,2025)}, {tr(S,CRIT)}, {orr(S,CRIT)}",
                    note="ρ has no P in Abstract; no test named (E4).")
    A["A07"] = dict(values="+11.0, +30.9, −22.0 pp", N="critical records per year (270; 878)", script="analysis/run_theme_prevalence.py",
                    output="output/analyses/theme_prevalence_trends.csv", rep="Y",
                    new=f"safety {a(TH,'Patient safety',2025).pct-a(TH,'Patient safety',2021).pct:+.1f}; errors {a(TH,'Hallucination / errors',2025).pct-a(TH,'Hallucination / errors',2021).pct:+.1f}; regulation {a(TH,'Governance / regulation',2025).pct-a(TH,'Governance / regulation',2021).pct:+.1f} pp",
                    note="Differences in pp without CI or endpoints.")
    A["A08"] = dict(values="n=2226; factual error 56%–90%; fabrication-involved ~21%–23% from 2023", n="2,226",
                    script="q7_phase3_analyses.py --abstract-only", output="output/figures/q7_gate_composition_abstractonly.png (no csv)",
                    rep=f"Partial: 2,226 and 56–90% (recomputed {min(misc_rng6):.1f}–{max(misc_rng6):.1f}%) reproduce; "
                        f"gated fabrication-involved share is {yr_gated[2023]:.1f}% in 2023, {yr_gated[2024]:.1f}%, {yr_gated[2025]:.1f}%, {yr_gated[2026]:.1f}% in 2024–2026, so '21–23% from 2023 onward' does not hold for 2023",
                    new=f"gated n={mf[W5]['n_gated']:,}; factual error {min(misc_rng5):.1f}–{max(misc_rng5):.1f}%; fabrication-involved 2023–2025: {yr_gated[2023]:.1f}%, {yr_gated[2024]:.1f}%, {yr_gated[2025]:.1f}%")
    A["A09"] = dict(values="51.3% Mental Health; 16.8% Cardiology; ρ −0.65, P=.004; US 34.5%; China 16.2%",
                    n="249; 106; 1,455; 308", N="485; 631; 4,222; 1,904", script="analysis/run_specialty_critical.py; run_specialty_aiadoption.py; run_country_critical_map.py",
                    output="specialty_critical_v1.csv; specialty_aiadoption.csv; country_critical.csv", rep="Y",
                    new=f"Mental Health {x('Specialty critical','Mental Health / Psychiatry')}; Cardiology {x('Specialty critical','Cardiology')}; FDA ρ {x('Specialty × FDA','all categories (n≥30)','spearman_rho')}, P {x('Specialty × FDA','all categories (n≥30)','P_two_sided')}; US {x('Country critical','United States')}; China {x('Country critical','China')}")
    A["A10"] = dict(values="Reviews critical 24.9%, favourable 73.1%", n="1,353; 3,981", N="5,444", script="analysis/run_pubtype_stance.py",
                    output="output/analyses/pubtype_stance_v1.csv", rep="Y",
                    new=f"critical {x('Pub type: Review','Critical')}; favourable {x('Pub type: Review','Favourable')}")
    # ---- Results ----
    A["R01"] = dict(values="97,492; 16,759; 8,899; 7,860", script="prefilter_batch.py", output="prefiltered_discourse_eval.csv", rep="Y",
                    note="T1: 96 of the 80,733 application records are failure-branch defaults, not model decisions.")
    A["R02"] = dict(values="16,749 valid; 10 unparseable", script="classify_stance_batch.py", output="classified_medical_Q1Q2.csv",
                    rep=f"Y ({n_failed} FAILED)")
    A["R03"] = dict(values="16,747; 2 dated 2020", rep=f"Y ({n2020} dated 2020)", new="14,058 dated 2021–2025; 2,689 dated 2026")
    A["R04"] = dict(values="30.8% critical; 916 Alarm; 4,245 Caution; 69.2% non-critical", n="5,161; 11,586", N="16,747",
                    ci=f"recomputed critical {x('Overall stance','Critical',w=XW6)}", method=BOOT, rep="Y",
                    new=f"critical {x('Overall stance','Critical')}; Alarm {x('Overall stance','Alarm')}; Caution {x('Overall stance','Caution')}")
    A["R05"] = dict(values="CO 62.8% (n=10,514); Neutral 5.0% (n=837); Advocacy 1.4% (n=235)", N="16,747", rep="Y",
                    new=f"CO {x('Overall stance','Cautious Optimism')}; Neutral {x('Overall stance','Neutral')}; Advocacy {x('Overall stance','Advocacy')}")
    A["R06"] = dict(A["A06"], values="25.4% [22.9–28.1] (2021) → 32.6% [30.9–34.4] (2026); Δ 7.25 pp",
                    new=f"{ap(S,CRIT,2021)} → {ap(S,CRIT,2025)}; Δ {a(S,CRIT,2025).pct-a(S,CRIT,2021).pct:+.2f} pp; {tr(S,CRIT)}; {orr(S,CRIT)}",
                    note="Δ has no CI.")
    A["R07"] = dict(values="v2 direction (Table S1)", script="analysis/run_temporal_stance.py (v2 overlay)", output="output/analyses/temporal_stance_v2.csv",
                    rep="Not re-checked in Batch 1 (v2 is a sensitivity analysis)")
    A["R09"] = dict(values="Alarm 2.7%→6.8% (2024)→6.2% (2026); Caution 22.7%→26.4%", n="29; 253; 167 | 241; 711", N="1,063; 3,700; 2,689",
                    script="analysis/run_temporal_stance.py", output="temporal_stance_v1.csv", rep="Y",
                    new=f"Alarm {ap(S,'Alarm',2021)} → {ap(S,'Alarm',2024)} (2024) → {ap(S,'Alarm',2025)}, {tr(S,'Alarm')}, {orr(S,'Alarm')}; Caution {ap(S,'Caution',2021)} → {ap(S,'Caution',2025)}, {tr(S,'Caution')}, {orr(S,'Caution')}")
    A["R10"] = dict(values="CO 60.2%–65.3% each year", rep="Y", new=f"{min(co5):.1f}–{max(co5):.1f}% (2021–2025); {tr(S,'Cautious Optimism')}; {orr(S,'Cautious Optimism')}")
    A["R12"] = dict(A["A06"], values="Advocacy 2.9%→0.6%, ρ −1.00",
                    new=f"{ap(S,'Advocacy',2021)} → {ap(S,'Advocacy',2025)}; {tr(S,'Advocacy')}; {orr(S,'Advocacy')}", note="ρ given without P.")
    A["R13"] = dict(values="17 Advocacy records in 2026; 5 drug discovery", n="17; 5", N="2,689; 17", script="analysis/run_advocacy_2021_vs_2026.py",
                    output="output/analyses/advocacy_2026_records.csv; Table S2",
                    rep="17 Y; '5 drug discovery' is a manual reading of Table S2, not recomputed", new="2026 only (descriptive table)")
    A["R15"] = dict(values="16,747", rep="Y", new="14,058")
    A["R16"] = dict(values="discourse 30.2%→37.8% (ρ +0.94); evaluative 14.6%→28.1% (ρ +0.77)", n="222; 477 | 48; 401", N="735; 1,261 | 328; 1,428",
                    script="analysis/revision_checks/cv1_within_genre.py", output="output/revision_checks/cv1_within_genre_trends.csv",
                    rep="Y (points, ρ). Table S3 CIs are not reproducible: per-cell seed = 42 + hash((genre, year)) % 10000 uses Python's salted string hash",
                    new=f"discourse {ap('Within genre: discourse',CRIT,2021)} → {ap('Within genre: discourse',CRIT,2025)}, {tr('Within genre: discourse',CRIT)}, {orr('Within genre: discourse',CRIT)}; evaluative {ap('Within genre: evaluative',CRIT,2021)} → {ap('Within genre: evaluative',CRIT,2025)}, {tr('Within genre: evaluative',CRIT)}, {orr('Within genre: evaluative',CRIT)}")
    A["R17"] = dict(values="ratio 2.24 → 0.88", n="735/328; 1,261/1,428", script="cv1_within_genre.py", output="cv1_genre_ratio_by_year.csv", rep="Y",
                    new=f"{ratio.ratio.iloc[0]:.2f} (2021) → {ratio[ratio.year==2025].ratio.iloc[0]:.2f} (2025) [{int(ratio[ratio.year==2025].n_discourse.iloc[0]):,}/{int(ratio[ratio.year==2025].n_evaluative.iloc[0]):,}]")
    A["R19"] = dict(values="keep rate ρ +1.00", script="analysis/revision_checks/cv2_keep_rate.py", output="output/revision_checks/cv2_keep_rate_by_year.csv",
                    rep="Y", new=f"{ap('Prefilter keep rate','Kept (discourse or evaluative)',2021)} → {ap('Prefilter keep rate','Kept (discourse or evaluative)',2025)}; {tr('Prefilter keep rate','Kept (discourse or evaluative)')}; {orr('Prefilter keep rate','Kept (discourse or evaluative)')}",
                    note="No P given.")
    A["R20"] = dict(values="5,161 critical records", rep="Y", new="4,283 (2021–2025)")
    for rid, lab, txt in [("R22", "Patient safety", "+11.0 pp"), ("R23", "Hallucination / errors", "+30.9 pp")]:
        A[rid] = dict(values=txt, N="critical records 2021 (270), 2026 (878)", script="analysis/run_theme_prevalence.py",
                      output="theme_prevalence_trends.csv", rep="Y",
                      new=f"{ap(TH,lab,2021)} → {ap(TH,lab,2025)} (Δ {a(TH,lab,2025).pct-a(TH,lab,2021).pct:+.1f} pp); {tr(TH,lab)}; {orr(TH,lab)}")
    A["R24"] = dict(values="regulation −22.0 pp; ethics/bias −8.1 pp (36.7%→28.6%)", N="270; 878", script="analysis/run_theme_prevalence.py",
                    output="theme_prevalence_trends.csv", rep="Y",
                    new=f"regulation {ap(TH,'Governance / regulation',2021)} → {ap(TH,'Governance / regulation',2025)}, {tr(TH,'Governance / regulation')}; ethics {ap(TH,'Ethics & bias',2021)} → {ap(TH,'Ethics & bias',2025)}, {tr(TH,'Ethics & bias')}, {orr(TH,'Ethics & bias')}")
    A["R26"] = dict(values="5,159 of 5,161 parsed; 2 dropped", script="classify_q7_failuremode.py", output="q7_classified_ac.csv",
                    rep=f"Y ({mf['counts']['parsed']:,}/{mf['counts']['q7_records']:,})")
    A["R27"] = dict(values="4,747 abstract-present", rep=f"Y ({mf[W6]['n_abstract_present_critical']:,})", new=f"{mf[W5]['n_abstract_present_critical']:,}")
    A["R28"] = dict(values="2,226 gated; factual error 56%–90%", rep=f"Y ({mf[W6]['n_gated']:,}; {min(misc_rng6):.1f}–{max(misc_rng6):.1f}%)",
                    script="q7_phase3_analyses.py --abstract-only", output="figure only",
                    new=f"{mf[W5]['n_gated']:,}; {min(misc_rng5):.1f}–{max(misc_rng5):.1f}%; misclassification {tr(GATE,'Misclassification (factual error)')}")
    A["R29"] = dict(values="fabrication-involved 0% (2021) → ~21%–23% from 2023", script="q7_phase3_analyses.py", rep=A["A08"]["rep"].split(";", 1)[-1].strip(),
                    new=f"{ap(FAB,'Fabrication-involved (confabulation or both)',2021)} → {ap(FAB,'Fabrication-involved (confabulation or both)',2025)}; {tr(FAB,'Fabrication-involved (confabulation or both)')}; {orr(FAB,'Fabrication-involved (confabulation or both)')}")
    A["R30"] = dict(values="generative share 5.3%→62.8% (ρ +0.94)", n="13; 528", N="245; 841", script="q7_s5_1_b_plateau.py --abstract-only",
                    output="q7_ac_temporal_shares_abstractonly.csv", rep="Y",
                    new=f"{ap(MECH,'Generative-model share (generative or both)',2021)} → {ap(MECH,'Generative-model share (generative or both)',2025)}; {tr(MECH,'Generative-model share (generative or both)')}; {orr(MECH,'Generative-model share (generative or both)')}")
    A["R31"] = dict(values="fabrication share ρ +0.94; 13.8% in 2026", n="116", N="841", output="q7_ac_temporal_shares_abstractonly.csv", rep="Y",
                    new=f"{ap(MECH,'Fabrication share (confabulation or both)',2021)} → {ap(MECH,'Fabrication share (confabulation or both)',2025)}; {tr(MECH,'Fabrication share (confabulation or both)')}; {orr(MECH,'Fabrication share (confabulation or both)')}")
    A["R32"] = dict(values="21.8%, 22.9%, 19.7%, 22.0% (2023–2026)", output="q7_ac_temporal_shares_abstractonly.csv (confab_among_gen)",
                    rep="Y (" + ", ".join(f"{gen_fab[y]:.1f}" for y in range(2023, 2027)) + ")",
                    new=", ".join(f"{y}: {ap(GEN,'Fabrication share among generative',y)}" for y in (2023, 2024, 2025)) + f"; {orr(GEN,'Fabrication share among generative')}")
    A["R33"] = dict(values="1,858 (39.1%)", n="1,858", N="4,747", rep=f"Y ({mf[W6]['gen_without_fab']:,}; {mf[W6]['gen_without_fab_pct']:.1f}%)",
                    new=f"{mf[W5]['gen_without_fab']:,}/{mf[W5]['n_abstract_present_critical']:,} ({mf[W5]['gen_without_fab_pct']:.1f}%)")
    A["R34"] = dict(values="κ=0.57", rep="Y (T3: 0.574)")
    A["R35"] = dict(values="16,734 valid; 18 categories ≥30; 13 FAILED", rep="Y",
                    new=f"{x('Specialty','valid','records')} valid; {x('Specialty','FAILED or missing','records')} FAILED")
    A["R37"] = dict(values="Mental Health 51.3% (46.8–55.5); Medical Informatics 44.9% (43.5–46.4); Nursing 43.0% (37.0–48.8)",
                    n="249; 1,949; 125", N="485; 4,337; 291", method=BOOT + " (joint resample of all records)", script="analysis/run_specialty_critical.py",
                    output="specialty_critical_v1.csv", rep="Y",
                    new=f"{x('Specialty critical','Mental Health / Psychiatry')}; {x('Specialty critical','Medical Informatics / Digital Health')}; {x('Specialty critical','Nursing')}")
    A["R38"] = dict(values="Cardiology 16.8% (14.1–19.8); Ophthalmology 18.4% (15.7–21.2); Oncology 19.7% (17.8–21.8)",
                    n="106; 139; 280", N="631; 755; 1,424", method=BOOT, script="analysis/run_specialty_critical.py", output="specialty_critical_v1.csv", rep="Y",
                    new=f"{x('Specialty critical','Cardiology')}; {x('Specialty critical','Ophthalmology')}; {x('Specialty critical','Oncology')}")
    A["R39"] = dict(values="ρ −0.65, two-sided P=.004", N="18 categories", script="analysis/run_specialty_aiadoption.py",
                    output="specialty_aiadoption.csv", rep=f"Y ({x('Specialty × FDA','all categories (n≥30)','spearman_rho',XW6)}, P={x('Specialty × FDA','all categories (n≥30)','P_two_sided',XW6)})",
                    new=f"ρ {x('Specialty × FDA','all categories (n≥30)','spearman_rho')}, P={x('Specialty × FDA','all categories (n≥30)','P_two_sided')}", note="ρ without CI.")
    A["R40"] = dict(values="ρ −0.58, n=11, P=.062", script="analysis/revision_checks/stat8_fda_drop_zero.py", output="stat8_fda_drop_zero_sensitivity.csv",
                    rep="Y", new=f"ρ {x('Specialty × FDA','structural zeros dropped','spearman_rho')}, P={x('Specialty × FDA','structural zeros dropped','P_two_sided')}")
    A["R41"] = dict(values="ρ −0.01", script="analysis/run_specialty_aiadoption.py / q7_s5_1_a_specialty.py", output="q7_ac_by_specialty_abstractonly.csv",
                    rep=f"Y ({x('Specialty × generative share','all categories (n≥30)','spearman_rho',XW6)}; generative share among abstract-present critical records)",
                    new=f"ρ {x('Specialty × generative share','all categories (n≥30)','spearman_rho')}")
    A["R43"] = dict(values="US 34.5% [33.0–36.0] n=4,222; China 16.2% [14.6–17.8] n=1,904", method=BOOT + " (within country)",
                    script="analysis/run_country_critical_map.py", output="output/analyses/country_critical.csv", rep="Y",
                    new=f"US {x('Country critical','United States')}; China {x('Country critical','China')}")
    cl = lambda c, w=XW5: x("Country critical", c, w=w)
    A["R44"] = dict(values="Netherlands 44.4%; Denmark ~42.6%; Australia ~42.5%; Ireland 41.1%; UK ~40.6%", n="144; 49; 172; 37; 492",
                    N="324; 115; 405; 90; 1,212", script="analysis/run_country_critical_map.py", output="country_critical.csv", rep="Y",
                    new="; ".join(f"{c} {cl(c)}" for c in ["Netherlands", "Denmark", "Australia", "Ireland", "United Kingdom"]))
    A["R45"] = dict(values="Japan 18.3%; Iran 18.0%; South Korea 20.5%; India 20.6%", n="68; 35; 92; 95", N="371; 194; 449; 461",
                    script="analysis/run_country_critical_map.py", output="country_critical.csv", rep="Y",
                    new="; ".join(f"{c} {cl(c)}" for c in ["Japan", "Iran", "South Korea", "India"]))
    A["R46"] = dict(values="NA 35.1% [33.9–36.4] n=4964; WEU 35.1% [33.6–36.5] n=4,298", method=BOOT + " (joint resample)",
                    script="analysis/run_region_critical.py", output="output/analyses/region_critical_v1.csv",
                    rep=f"Partial: % and CIs reproduce; n does not (recomputed NA {x('Region critical','North America',w=XW6)}, WEU {x('Region critical','Western Europe',w=XW6)})",
                    new=f"NA {x('Region critical','North America')}; WEU {x('Region critical','Western Europe')}")
    A["R47"] = dict(values="East Asia 18.5% [17.2–19.9] n=3,262", method=BOOT, script="analysis/run_region_critical.py", output="region_critical_v1.csv",
                    rep=f"Partial: % and CI reproduce; n does not (recomputed {x('Region critical','East Asia',w=XW6)}; 3,262 appears in the older session2_summary.md with 19.5%)",
                    new=x("Region critical", "East Asia"))
    A["R48"] = dict(values="18.5%→19.9% vs 35.1%; 8% of gap", script="analysis/run_east_asia_diagnose.py", output="console only",
                    rep=f"Y (EA {x('East Asia reweighting','EA raw',w=XW6,ci=False)} → {x('East Asia reweighting','EA reweighted to NA+WEU specialty mix',w=XW6,ci=False)}; NA+WEU {x('East Asia reweighting','NA+WEU raw',w=XW6,ci=False)}; gap closed {x('East Asia reweighting','share of gap closed',w=XW6,ci=False)})",
                    new=f"EA {x('East Asia reweighting','EA raw',ci=False)} → {x('East Asia reweighting','EA reweighted to NA+WEU specialty mix',ci=False)}; NA+WEU {x('East Asia reweighting','NA+WEU raw',ci=False)}; gap closed {x('East Asia reweighting','share of gap closed',ci=False)}",
                    note="Reweighting uses records with valid specialty (EA n=3,256 in submitted window).")
    A["R49"] = dict(values="Hong Kong 31.6%; Singapore 26.7%; China 16.2%", n="30; 43; 308", N="95; 161; 1,904", rep="Y",
                    new="; ".join(f"{c} {cl(c)}" for c in ["Hong Kong", "Singapore", "China"]))
    pt = lambda p, s="Critical", w=XW5: x(f"Pub type: {p}", s, w=w)
    A["R51"] = dict(values="RA 10,315; Reviews 5,444; Letters 480; Editorials 404; Commentaries 104", rep="Y",
                    new=", ".join(f"{p} {X[(X.analysis==f'Pub type: {p}')&(X.window==XW5)].n.iloc[0]:,.0f}" for p in ["Research Article", "Review", "Letter", "Editorial", "Commentary"]))
    A["R52"] = dict(values="Commentaries 53.9%; Letters 42.1%; Editorials 38.4%; RA 32.9%; Reviews 24.9%", n="56; 202; 155; 3,395; 1,353",
                    N="104; 480; 404; 10,315; 5,444", script="analysis/run_pubtype_stance.py", output="pubtype_stance_v1.csv",
                    rep="Partial: Commentary critical = 56/104 = 53.85% → 53.8% (manuscript 53.9% = sum of rounded Alarm 8.7 + Caution 45.2); others Y",
                    new="; ".join(f"{p} {pt(p)}" for p in ["Commentary", "Letter", "Editorial", "Research Article", "Review"]))
    A["R53"] = dict(values="opinion 41.8% vs RA 32.9%", n="413; 3,395", N="988; 10,315", rep="Y",
                    new=f"opinion {x('Pub type: opinion pooled (Comm+Letter+Ed)','Critical')}; RA {pt('Research Article')}")
    A["R54"] = dict(values="N=11,303; χ²₄=430.5; P<.001; Cramér's V=0.195", script="analysis/revision_checks/stat2_cramers_v.py",
                    output="stat2_pubtype_chisq_effect_size.csv", rep="Y",
                    new=f"N={X[(X.analysis=='Opinion vs Research Article stance')&(X.metric=='chi2')&(X.window==XW5)].n.iloc[0]:,.0f}; χ²₄={x('Opinion vs Research Article stance','χ²','chi2')}; V={x('Opinion vs Research Article stance',chr(67)+'ramér'+chr(39)+'s V','V')}")
    A["R55"] = dict(values="Letters neutral ~22%; 2%–9% other formats", n="104", N="480", rep="Y (21.7%; others 2.0–9.4%)",
                    new=f"Letters neutral {pt('Letter','Neutral')}")
    A["R56"] = dict(values="favourable: Reviews 73.1%; RA 61.5%; Editorials 52.2%; Commentaries 39.4%; Letters 36.3%", rep="Y (Letters 174/480 = 36.25% → 36.3% half-up)",
                    new="; ".join(f"{p} {pt(p,'Favourable')}" for p in ["Review", "Research Article", "Editorial", "Commentary", "Letter"]))
    A["R57"] = dict(values="systematic 29.3% (n=980) vs narrative 23.9% (n=4,464)", n="287; 1,066", N="980; 4,464", script="analysis/robustness.py simplify_pubtype_7 (see T8)",
                    output="Table S11", rep="Y",
                    new=f"systematic {x('Review subtype: Systematic Review','Critical')}; narrative {x('Review subtype: Review (narrative)','Critical')}")
    A["R58"] = dict(values="Commentary n=104", rep="Y", new="98")
    for rid, vals in [("R59", "92 Advocacy papers 2021–2023 with predictive flag"), ("R60", "18 false positives; precision 0.80"),
                      ("R61", "74 papers; 78 claims; Tier 1/2/3 = 7/36/35"), ("R63", "2 borne out; 54 (69.2%) partially; 8 not; 14 too early"),
                      ("R64", "Tier 1: 5/7 not borne out; 0 borne out"), ("R65", "Tier 2: 23/36 partially"), ("R66", "Tier 3: 30/35 partially")]:
        A[rid] = dict(values=vals, script="prophecy_phase1_*.py; prophecy_phase2_*.py",
                      output="output/analyses/prophecy/phase1_signature_claims_FROZEN.csv; phase2_prophecy_verdicts_worksheet.xlsx (sheet adjudicate)",
                      rep="Y (counts recomputed: frozen 74 PMIDs / 78 claims; verdict × tier matrix = Table S13)", new="n/a (forward validation; window fixed by design)")
    A["R60"]["note"] = "0.80 = 74/92 (post-hoc flag precision) has no CI."
    A["R63"]["note"] = "69.2% = 54/78; no CI."
    # captions
    A["C02"] = dict(values="16,747 of 16,749", rep="Y", new="14,058 (2021–2025)")
    A["C03"] = dict(values="1000 resamples, seed 42", rep="Y (method)")
    A["C04"] = dict(values="n=5161 critical", rep="Y", new="4,283")
    A["C07"] = dict(values="*P<.05; **P<.01 by exact two-sided permutation", rep="Partial: Figure 1a asterisks agree with exact permutation P (Neutral exact P=.033, Advocacy .003), but Table S1 lists scipy asymptotic P for every row except Advocacy (Alarm/Caution/critical .072 vs exact .103; Neutral .019 vs exact .033)",
                    new="Asterisks removed in draft; exact P in caption (T4_figure_captions.md)")
    A["C09"] = dict(values="n=2226", rep="Y", new=f"{mf[W5]['n_gated']:,}")
    A["C11"] = dict(values="n=4,747", rep="Y", new=f"{mf[W5]['n_abstract_present_critical']:,}")
    A["C14"] = dict(values="16,734 valid; 13 failed", rep="Y", new=f"{x('Specialty','valid','records')}")
    A["C16"] = dict(values="structural zeros plotted at 0.5", rep="Not checked (figure)")
    A["C19"] = dict(values="36 countries ≥50 records", rep=f"Y ({x('Country','countries with n≥50','count',XW6)})", new=f"{x('Country','countries with n≥50','count')} countries")
    A["C23"] = dict(values="16,747", rep="Y", new="14,058")
    A["C27"] = dict(values="78 predictions; 74 papers", rep="Y", new="n/a")
    return A


def flags(sentence):
    n_pct = len(re.findall(r"\d+(?:\.\d+)?\s?%", sentence))
    has_ci = bool(re.search(r"95% CI|\[\d|\(\d+(?:\.\d+)?[–-]\d", sentence))
    has_nN = bool(re.search(r"\bn\s?=|\(n=|\d+ (?:of|out of) \d+|\d/\d", sentence))
    return n_pct, has_ci, has_nN


REF = re.compile(r"(Multimedia Appendix \d|Tables? S\d+(?:[-–]S\d+)?|Figures? S?\d+[A-Za-z]?|\b20\d\d\b|\[\d+(?:[,-]\d+)*\]|Tier[- ]?\d|"
                 r"\b(?:a|b)\)|Figure \d\.)")


def main():
    A = build_annotations()
    rows, disc = [], []
    for sid, sec, sent in quantitative_sentences():
        if sec == "Discussion":
            stripped = REF.sub("", sent)
            if re.search(r"\d", stripped) or "ρ" in sent:
                lit = bool(re.search(r"\[\d+", sent))
                disc.append({"ID": sid, "verbatim sentence": sent,
                             "numbers": "; ".join(re.findall(r"[−-]?\d+(?:[.,]\d+)?%?", stripped)),
                             "cites published literature in the same sentence": "yes" if lit else "no",
                             "direct numeric comparison with literature": "no"})
            continue
        stripped = REF.sub("", sent)
        quant = bool(re.search(r"\d", stripped))
        n_pct, has_ci, has_nN = flags(sent)
        ann = A.get(sid, {})
        if not quant and not ann:
            continue
        rows.append({"ID": sid, "section": sec, "verbatim sentence": sent,
                     "value(s)": ann.get("values", ""), "numerator n": ann.get("n", ""), "denominator N": ann.get("N", ""),
                     "95% CI": ann.get("ci", "as stated" if has_ci else ""), "CI method": ann.get("method", BOOT if has_ci else ""),
                     "source script": ann.get("script", ""), "source output": ann.get("output", ""),
                     "reproduced": ann.get("rep", "not a quantitative result (method/reference)" if not ann else ""),
                     "2021–2025 value": ann.get("new", ""), "note": ann.get("note", ""),
                     "n percentages": n_pct, "flag: % without CI": "FLAG" if n_pct and not has_ci else "",
                     "flag: % without n/N": "FLAG" if n_pct and not has_nN else ""})
    led = pd.DataFrame(rows)
    led.to_csv(OUT / "T5_claims_ledger.csv", index=False)
    dd = pd.DataFrame(disc)
    dd.to_csv(OUT / "T5_discussion_numbers.csv", index=False)

    L = ["# T5 · Claims ledger (E12, E4, E13)\n",
         "Script: `revision_r1/scripts/t5_claims_ledger.py` (sentence extraction `t5_extract.py`; cross-sectional "
         "recomputation `t5_crosssectional.py`, both windows side by side in "
         "[T5_crosssectional_both_windows.md](T5_crosssectional_both_windows.md)). Source text: the submitted "
         "manuscript converted with macOS `textutil`. Full ledger: [T5_claims_ledger.csv](T5_claims_ledger.csv).\n",
         f"- Quantitative statements (Abstract, Results, captions): **{len(led)}**.",
         f"- Reproduced Y: {led['reproduced'].str.startswith('Y').sum()}; partial: {led['reproduced'].str.startswith('Partial').sum()}; "
         f"not re-checked: {led['reproduced'].str.contains('Not').sum()}.",
         f"- Sentences with a percentage but no CI: **{(led['flag: % without CI']=='FLAG').sum()}**; with a percentage but no n/N: "
         f"**{(led['flag: % without n/N']=='FLAG').sum()}** (heuristic on the sentence text; see section 2).\n",
         "## 1. Statements not fully reproduced\n"]
    bad = led[~led["reproduced"].str.startswith("Y") & (led["reproduced"] != "not a quantitative result (method/reference)")]
    for _, r in bad.iterrows():
        L.append(f"- **{r.ID}** ({r.section}): {r['reproduced']}")
    L.append("\n## 2. Percentages lacking a CI or n/N (E12, E4)\n")
    fl = led[(led["flag: % without CI"] == "FLAG") | (led["flag: % without n/N"] == "FLAG")]
    L.append("| ID | section | missing | sentence (truncated) |\n|---|---|---|---|")
    for _, r in fl.iterrows():
        miss = " + ".join(m for m, c in [("CI", r["flag: % without CI"]), ("n/N", r["flag: % without n/N"])] if c)
        L.append(f"| {r.ID} | {r.section} | {miss} | {r['verbatim sentence'][:140]}{'…' if len(r['verbatim sentence'])>140 else ''} |")
    L.append("\nOther E12 items without CIs (not percentages): Spearman ρ values (A06, R12, R16, R19, R30, R31, R39–R41), "
             "differences in percentage points (A07, R06, R22–R24), the discourse:evaluative ratio (R17), κ values in "
             "the Abstract other than stance (A04), and the flag precision 0.80 (R60).\n")
    L.append("## 3. Ledger (abridged: ID, values, reproduced, 2021–2025 value)\n")
    L.append("| ID | value(s) | reproduced | 2021–2025 value |\n|---|---|---|---|")
    for _, r in led.iterrows():
        L.append(f"| {r.ID} | {r['value(s)']} | {r['reproduced']} | {r['2021–2025 value']} |")
    L.append("\n## 4. Numbers in the Discussion (editor: remove unless compared directly with published literature)\n")
    L.append("None of these numbers is compared numerically with a published estimate; the literature-citing sentences "
             "(D07, D08, D12, D13) carry citation numbers only, not data.\n")
    L.append("| ID | numbers | cites literature | sentence |\n|---|---|---|---|")
    for _, r in dd.iterrows():
        L.append(f"| {r.ID} | {r['numbers']} | {r['cites published literature in the same sentence']} | {r['verbatim sentence']} |")
    (OUT / "T5_claims_ledger.md").write_text("\n".join(L) + "\n")
    print("\n".join(L[:12]))


if __name__ == "__main__":
    main()
