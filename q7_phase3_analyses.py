"""Q7 Phase 3 — gate-independent analyses on q7_classified_ac.csv.

Parts:
 1. GATE AUDIT — among old "hallucination" theme-gated papers, failure_mode ×
    pub_year (composition shift), + gate-recall (confab among NOT-flagged).
 2. GATE-INDEPENDENT TREND — % per year confab & generative, bootstrap 95% CI.
 3. S4-1 DISENTANGLEMENT — generative-share per specialty; Spearman + partial
    Spearman(critical_rate, FDA | generative_share); attenuation; Dermatology.
 4. DIVERGENCE — generative-not-confab vs confab-not-generative, with examples.

Figures: output/figures/q7_gate_composition.png, q7_s41_disentangle.png
Conventions: drop FAILED, seed=42, bootstrap n=1000 percentile 95% CI.
"""
import os, csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import spearmanr
from robustness import bootstrap_ci

import argparse
ap = argparse.ArgumentParser()
ap.add_argument("--abstract-only", action="store_true",
                help="QC: restrict to A+C papers carrying an abstract (drop title-only)")
ARGS = ap.parse_args()
SUF = "_abstractonly" if ARGS.abstract_only else ""

SEED = 42
BASE = os.path.dirname(os.path.abspath(__file__))
AC    = os.path.join(BASE, "output", "analyses", "q7_classified_ac.csv")
SRC   = os.path.join(BASE, "output", "classified_medical_Q1Q2.csv")
THEME = os.path.join(BASE, "output", "analysis", "thematic_alarm.csv")
SPEC  = os.path.join(BASE, "output", "specialty_classifications.csv")
ADOPT = os.path.join(BASE, "output", "analyses", "specialty_aiadoption.csv")
FIGDIR = os.path.join(BASE, "output", "figures")
YEARS = ["2021","2022","2023","2024","2025","2026"]
os.makedirs(FIGDIR, exist_ok=True)

# ── load + join hallucination gate ────────────────────────────────────────────
ac = pd.read_csv(AC, dtype={"pmid": str})
ac = ac[ac["failure_mode"] != "FAILED"].copy()
ac["pub_year"] = ac["pub_year"].astype(str)
print(f"A+C valid rows (FAILED dropped): {len(ac)}")

if ARGS.abstract_only:
    ab = pd.read_csv(SRC, dtype={"pmid": str})[["pmid", "abstract"]]
    ab["has_ab"] = ab["abstract"].fillna("").astype(str).str.strip().str.len() > 0
    keep_pmids = set(ab.loc[ab["has_ab"], "pmid"])
    before = len(ac)
    ac = ac[ac["pmid"].isin(keep_pmids)].copy()
    print(f"QC --abstract-only: dropped {before - len(ac)} title-only papers; "
          f"kept {len(ac)} abstract-present.")

th = pd.read_csv(THEME, dtype={"pmid": str})[["pmid","themes"]]
th["hallu_gate"] = th["themes"].fillna("").str.lower().str.contains("hallucination").astype(int)
ac = ac.merge(th[["pmid","hallu_gate"]], on="pmid", how="left")
ac["hallu_gate"] = ac["hallu_gate"].fillna(0).astype(int)
print(f"hallucination-gated within A+C: {int(ac['hallu_gate'].sum())}")

ac["confab_inv"] = ac["failure_mode"].isin(["confabulation","both"]).astype(int)
ac["misc_inv"]   = ac["failure_mode"].isin(["misclassification","both"]).astype(int)
ac["gen_inv"]    = ac["model_type"].isin(["generative","both"]).astype(int)

FM = ["confabulation","misclassification","both","none_or_unclear"]

# =============================================================================
# PART 1 — GATE AUDIT
# =============================================================================
print("\n" + "="*100)
print("PART 1 — GATE AUDIT: failure_mode × pub_year AMONG old 'hallucination'-gated papers")
print("="*100)
gated = ac[ac["hallu_gate"] == 1]
print(f"n gated = {len(gated)}")
ct  = pd.crosstab(gated["failure_mode"], gated["pub_year"]).reindex(index=FM, columns=YEARS, fill_value=0)
pct = ct.div(ct.sum(axis=0), axis=1) * 100
print("\nCounts:")
print(ct.to_string())
print("\n% within year:")
print(pct.round(1).to_string())

# collapse to confab-involved vs misclassification-dominant for the headline
gci = gated.groupby("pub_year")["confab_inv"].mean().reindex(YEARS) * 100
gmi = gated.groupby("pub_year")["misc_inv"].mean().reindex(YEARS) * 100
print("\nHeadline within gated papers (confab-involved vs misclassification-involved, % by year):")
for y in YEARS:
    print(f"  {y}: confab-involved={gci[y]:5.1f}%   misclassification-involved={gmi[y]:5.1f}%")

# GATE-RECALL: confab the new classifier finds among NOT-gated, by year
print("\n" + "-"*100)
print("GATE-RECALL: confab-involved papers the new classifier finds AMONG papers NOT 'hallucination'-gated")
print("-"*100)
notgated = ac[ac["hallu_gate"] == 0]
rec = (notgated.groupby("pub_year")
       .agg(n_notgated=("pmid","size"), n_confab=("confab_inv","sum"))
       .reindex(YEARS).fillna(0))
rec["pct_confab"] = rec["n_confab"] / rec["n_notgated"] * 100
print(rec.to_string(float_format=lambda v: f"{v:.1f}"))
total_missed = int(rec["n_confab"].sum())
print(f"\nTotal confab-involved papers MISSED by the old gate: {total_missed} "
      f"(of {int(rec['n_notgated'].sum())} not-gated). "
      f"Gate recall for confabulation = "
      f"{ac[(ac.confab_inv==1)&(ac.hallu_gate==1)].shape[0]}/{ac[ac.confab_inv==1].shape[0]} "
      f"= {ac[(ac.confab_inv==1)&(ac.hallu_gate==1)].shape[0]/ac[ac.confab_inv==1].shape[0]*100:.1f}%.")

# ── Figure 1: gate composition (single enlarged panel) ───────────────────────
from matplotlib.patches import Patch
import matplotlib.patheffects as pe
HALO = [pe.withStroke(linewidth=1.8, foreground="white")]   # black text stays legible on any colour
fig, axL = plt.subplots(figsize=(11, 7.2))
fig.subplots_adjust(top=0.88, bottom=0.16, left=0.09, right=0.97)
x = np.arange(len(YEARS))
FM_COL = {"confabulation":"#d62728","both":"#9467bd",
          "misclassification":"#1f77b4","none_or_unclear":"#bcbd22"}
order = ["confabulation","both","misclassification","none_or_unclear"]
# stacked COUNTS: bar height = that year's gated n (∝ volume); segment
# proportions still show the failure_mode composition. Labels give the % within
# the year so composition stays readable.
year_tot = np.array([int(ct[y].sum()) for y in YEARS])
bottom = np.zeros(len(YEARS))
for fm in order:
    cnt = ct.loc[fm, YEARS].values.astype(float)
    pc  = pct.loc[fm, YEARS].values
    axL.bar(x, cnt, bottom=bottom, color=FM_COL[fm], width=0.7,
            edgecolor="white", linewidth=0.5, label=fm)
    for j in range(len(YEARS)):
        # main bars: label % only for 2024–2026 (j>=3); 2021–2023 read from inset
        if pc[j] >= 8 and j >= 3:
            axL.text(j, bottom[j]+cnt[j]/2, f"{pc[j]:.0f}%", ha="center", va="center",
                     fontsize=9, color="black", fontweight="bold", path_effects=HALO)
    bottom += cnt
YTOP = year_tot.max()*1.12
# total-n label atop each bar
for j in range(len(YEARS)):
    axL.text(j, year_tot[j] + year_tot.max()*0.015, f"n={year_tot[j]}",
             ha="center", va="bottom", fontsize=9, color="black", fontweight="bold")
axL.set_xticks(x); axL.set_xticklabels(YEARS, fontsize=10)
# 2026 is a partial year (corpus ends Apr 2026)
axL.annotate("Jan–Apr only\n(2026.1–4 incl.)", xy=(5, 0), xytext=(0, -30),
             textcoords="offset points", ha="center", va="top", fontsize=7.5,
             color="0.4", style="italic", annotation_clip=False)
axL.set_ylim(0, YTOP); axL.set_ylabel("# hallucination-gated papers", fontsize=11)
axL.set_title("")
for s in ("top","right"): axL.spines[s].set_visible(False)

# ── inset: zoom on the small early years so their composition is readable ─────
ins = axL.inset_axes([0.045, 0.44, 0.40, 0.50])   # upper-left, clear of the 2024 bar
zoom_years = ["2021", "2022", "2023"]
zx = np.arange(len(zoom_years))
zbottom = np.zeros(len(zoom_years))
for fm in order:
    zc = ct.loc[fm, zoom_years].values.astype(float)
    zp = pct.loc[fm, zoom_years].values
    ins.bar(zx, zc, bottom=zbottom, color=FM_COL[fm], width=0.72,
            edgecolor="white", linewidth=0.5)
    for j in range(len(zoom_years)):
        if zp[j] >= 1.5:   # label ALL non-trivial segments (incl. the ~2% slices)
            ins.text(j, zbottom[j]+zc[j]/2, f"{zp[j]:.0f}%", ha="center", va="center",
                     fontsize=7, color="black", fontweight="bold", path_effects=HALO)
    zbottom += zc
ztot = np.array([int(ct[y].sum()) for y in zoom_years])
for j in range(len(zoom_years)):
    ins.text(j, ztot[j] + ztot.max()*0.02, f"n={ztot[j]}",
             ha="center", va="bottom", fontsize=7.5, color="black", fontweight="bold")
# call out that 2022's 2% slice is confabulation (too thin to read the colour)
_conf22 = ct.loc["confabulation", "2022"]
ins.annotate("2% = confabulation", xy=(1, _conf22/2), xytext=(0.05, 150),
             fontsize=6.5, ha="left", va="center", color="#d62728", fontweight="bold",
             path_effects=HALO,
             arrowprops=dict(arrowstyle="->", color="#d62728", lw=1.0, shrinkB=2))
ins.set_xticks(zx); ins.set_xticklabels(zoom_years, fontsize=8)
ins.set_ylim(0, ztot.max()+20)
ins.set_yticks([0, 100, 200])
ins.tick_params(axis="y", labelsize=7.5)
ins.set_title("Zoom: 2021–2023", fontsize=9, fontweight="bold")
for s in ("top","right"): ins.spines[s].set_visible(False)

# failure_mode legend BELOW the panel, outside the bars (no occlusion)
handles = [Patch(facecolor=FM_COL[fm], label=fm) for fm in order]
axL.legend(handles=handles, fontsize=10, frameon=False, ncol=4,
           loc="upper center", bbox_to_anchor=(0.5, -0.09))
fig.suptitle(
    "Heterogeneity of Hallucination-Flagged Papers by Underlying Failure Mode,\n"
    "2021–2026 (n=%d)" % int(year_tot.sum()),
    fontsize=12, fontweight="bold", y=0.975,
)
fig.text(
    0.5, 0.01,
    "Bar height: count of hallucination-flagged papers per year; "
    "segments: failure-mode share (% within year). *2026 partial year (Jan–Apr only).",
    ha="center", va="bottom", fontsize=7.5, color="#444444",
)
f1 = os.path.join(FIGDIR, f"q7_gate_composition{SUF}.png")
fig.savefig(f1, dpi=300, bbox_inches="tight"); plt.close(fig)
print(f"\nSaved → {f1}")

# =============================================================================
# PART 2 — GATE-INDEPENDENT TREND
# =============================================================================
print("\n" + "="*100)
print("PART 2 — GATE-INDEPENDENT TREND (all A+C, not conditioned on old gate)")
print("="*100)
def share_ci(sub, col):
    if len(sub)==0: return (0.0,np.nan,np.nan)
    b = bootstrap_ci(sub[[col]].reset_index(drop=True),
                     lambda s: float(s[col].mean()*100), n_boot=1000, seed=SEED)
    return (sub[col].mean()*100, b["lower"], b["upper"])
trend_rows=[]
for y in YEARS:
    sub = ac[ac["pub_year"]==y]
    cf = share_ci(sub, "confab_inv")   # broad: confab or both
    cs = sub["failure_mode"].eq("confabulation").mean()*100
    gn = share_ci(sub, "gen_inv")
    trend_rows.append({"pub_year":y,"n":len(sub),
                       "confab_broad":cf[0],"confab_broad_lo":cf[1],"confab_broad_hi":cf[2],
                       "confab_strict":cs,
                       "gen_share":gn[0],"gen_share_lo":gn[1],"gen_share_hi":gn[2]})
trend = pd.DataFrame(trend_rows)
print(trend.round(1).to_string(index=False))
rho_c,p_c = spearmanr(np.arange(6), trend["confab_broad"])
rho_g,p_g = spearmanr(np.arange(6), trend["gen_share"])
print(f"\nSpearman over years: confab-broad rho={rho_c:+.3f} p={p_c:.3f} | "
      f"generative-share rho={rho_g:+.3f} p={p_g:.3f}")
trend.to_csv(os.path.join(BASE,"output","analyses",f"q7_ac_temporal_trend{SUF}.csv"), index=False)

# =============================================================================
# PART 3 — S4-1 DISENTANGLEMENT
# =============================================================================
print("\n" + "="*100)
print("PART 3 — S4-1 DISENTANGLEMENT")
print("="*100)
spec = pd.read_csv(SPEC, dtype={"pmid":str})[["pmid","specialty"]]
acs = ac.merge(spec, on="pmid", how="left").dropna(subset=["specialty"])
gen_by_spec = acs.groupby("specialty")["gen_inv"].agg(["mean","size"])
gen_by_spec["gen_share"] = gen_by_spec["mean"]*100
adopt = pd.read_csv(ADOPT)
m = adopt.merge(gen_by_spec[["gen_share","size"]].rename(columns={"size":"n_critical"}),
                left_on="specialty", right_index=True, how="left")
m = m.dropna(subset=["critical_rate_pct","fda_device_count","gen_share"]).reset_index(drop=True)
print(f"specialties in disentanglement: {len(m)}")

def partial_spearman(x, y, z):
    """partial Spearman of x,y controlling z: Pearson on ranks via partial formula."""
    rx = pd.Series(x).rank().values; ry = pd.Series(y).rank().values; rz = pd.Series(z).rank().values
    def pear(a,b): return np.corrcoef(a,b)[0,1]
    rxy, rxz, ryz = pear(rx,ry), pear(rx,rz), pear(ry,rz)
    pr = (rxy - rxz*ryz)/np.sqrt((1-rxz**2)*(1-ryz**2))
    n=len(x); df=n-3
    t = pr*np.sqrt(df/(1-pr**2)); from scipy.stats import t as tdist
    p = 2*(1-tdist.cdf(abs(t), df))
    return pr, p

crit = m["critical_rate_pct"].values
fda  = m["fda_device_count"].values
gen  = m["gen_share"].values
rho_cf, p_cf = spearmanr(crit, fda)
rho_cg, p_cg = spearmanr(crit, gen)
rho_fg, p_fg = spearmanr(fda, gen)
pr_cf_g, pp_cf_g = partial_spearman(crit, fda, gen)
atten = (rho_cf - pr_cf_g)
print(f"  Spearman(critical_rate, FDA_adoption)               rho={rho_cf:+.3f}  p={p_cf:.3f}")
print(f"  Spearman(critical_rate, generative_share)           rho={rho_cg:+.3f}  p={p_cg:.3f}")
print(f"  Spearman(FDA_adoption, generative_share)            rho={rho_fg:+.3f}  p={p_fg:.3f}")
print(f"  PARTIAL Spearman(critical_rate, FDA | gen_share)    pr ={pr_cf_g:+.3f}  p={pp_cf_g:.3f}")
print(f"  Attenuation of |rho| once gen_share controlled: {abs(rho_cf):.3f} → {abs(pr_cf_g):.3f} "
      f"(Δ={abs(rho_cf)-abs(pr_cf_g):+.3f}, {(1-abs(pr_cf_g)/abs(rho_cf))*100:.0f}% reduction)")
derm = m[m["specialty"]=="Dermatology"]
if len(derm):
    d=derm.iloc[0]
    print(f"\n  DERMATOLOGY: critical_rate={d['critical_rate_pct']:.1f}%, FDA_devices={int(d['fda_device_count'])}, "
          f"generative_share(A+C)={d['gen_share']:.1f}%, n_critical={int(d['n_critical'])}")
print("\n  CAVEAT (verbatim): generative-share is computed on critical papers only → endogenous to")
print("  criticality, tends to OVER-attenuate (bias toward technology reading). Treat as suggestive;")
print("  a full-discourse covariate is the robustness upgrade.")

# ── Figure 2: disentangle scatter + rho table ────────────────────────────────
fig, ax = plt.subplots(figsize=(11,7.5))
fig.subplots_adjust(right=0.97, bottom=0.1, top=0.9)
sizes = np.clip(m["n_critical"].values*0.6+40, 50, 600)
ax.scatter(m["gen_share"], m["critical_rate_pct"], s=sizes, c="#7b3294",
           alpha=0.7, edgecolor="white", linewidth=1, zorder=3)
for r in m.itertuples():
    lab=r.specialty if len(r.specialty)<=26 else r.specialty[:24]+"…"
    fw="bold" if r.specialty=="Dermatology" else "normal"
    col="#c81e1e" if r.specialty=="Dermatology" else "0.2"
    ax.annotate(lab,(r.gen_share,r.critical_rate_pct),xytext=(6,4),
                textcoords="offset points",fontsize=8.5,fontweight=fw,color=col)
ax.set_xlabel("generative-share over critical (A+C) papers  (model_type ∈ {generative, both}) %")
ax.set_ylabel("critical_rate (% Alarm+Caution of all specialty papers)")
ax.set_title("Q7 Phase 3 · Part 3 — S4-1 disentanglement: criticality vs generative-share by specialty\n"
             "(point size ∝ n critical papers)", fontsize=11.5, loc="left")
tbl = (f"Spearman(crit, FDA)          ρ = {rho_cf:+.3f}  (p={p_cf:.3f})\n"
       f"Spearman(crit, gen-share)    ρ = {rho_cg:+.3f}  (p={p_cg:.3f})\n"
       f"Spearman(FDA, gen-share)     ρ = {rho_fg:+.3f}  (p={p_fg:.3f})\n"
       f"PARTIAL(crit, FDA | gen)     ρ = {pr_cf_g:+.3f}  (p={pp_cf_g:.3f})\n"
       f"attenuation |ρ|: {abs(rho_cf):.3f} → {abs(pr_cf_g):.3f}")
ax.text(0.98,0.04,tbl,transform=ax.transAxes,ha="right",va="bottom",fontsize=9,
        family="monospace",bbox=dict(boxstyle="round,pad=0.5",facecolor="#f3eef7",
        edgecolor="#b9a7c9",linewidth=0.8))
for s in ("top","right"): ax.spines[s].set_visible(False)
fig.text(0.5,0.005,"CAVEAT: gen-share computed on critical papers only → endogenous to criticality, tends to OVER-attenuate. Suggestive only.",
         ha="center",fontsize=8,style="italic",color="#c81e1e")
f2 = os.path.join(FIGDIR,f"q7_s41_disentangle{SUF}.png")
fig.savefig(f2,dpi=300,bbox_inches="tight"); plt.close(fig)
print(f"\nSaved → {f2}")

# =============================================================================
# PART 4 — DIVERGENCE
# =============================================================================
print("\n" + "="*100)
print("PART 4 — DIVERGENCE (the two axes carry independent information)")
print("="*100)
title_by = {}
with open(AC, encoding="utf-8") as f:
    pass
src = pd.read_csv(os.path.join(BASE,"output","classified_medical_Q1Q2.csv"),
                  dtype={"pmid":str})[["pmid","title"]]
tmap = dict(zip(src["pmid"], src["title"]))

gen_not_confab = ac[(ac["gen_inv"]==1) & (ac["confab_inv"]==0)]
confab_not_gen = ac[(ac["confab_inv"]==1) & (ac["gen_inv"]==0)]
print(f"generative but NOT confabulation: {len(gen_not_confab)} "
      f"({len(gen_not_confab)/len(ac)*100:.1f}% of A+C)")
print(f"confabulation but NOT generative: {len(confab_not_gen)} "
      f"({len(confab_not_gen)/len(ac)*100:.1f}% of A+C)")
print("\n— Examples: generative but NOT confabulation (LLM tested for accuracy/bias, not fabrication) —")
for r in gen_not_confab.sample(min(6,len(gen_not_confab)), random_state=SEED).itertuples():
    print(f"  [{r.pub_year}] fm={r.failure_mode:<17s} mt={r.model_type:<12s} | {str(tmap.get(r.pmid,''))[:80]}")
print("\n— Examples: confabulation but NOT generative (rare; fabrication tied to non-LLM system) —")
ex = confab_not_gen if len(confab_not_gen)<=8 else confab_not_gen.sample(8, random_state=SEED)
for r in ex.itertuples():
    print(f"  [{r.pub_year}] fm={r.failure_mode:<17s} mt={r.model_type:<12s} | {str(tmap.get(r.pmid,''))[:80]}")
    print(f"            rationale: {r.rationale}")

print("\nDONE — Phase 3 parts 1–4. Figures + q7_ac_temporal_trend.csv written.")
