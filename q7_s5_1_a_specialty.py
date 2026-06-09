"""S5-1-a: failure_mode × specialty on q7_classified_alarm.csv.

Pure analysis. Joins alarm classifications with specialty mapping, computes
per-specialty composition and bootstrap-CI on confab-share and generative-share,
ranks specialties, links to S4-1 adoption table, and produces a 2-panel figure.

No new classification calls.
"""
import os, sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from robustness import bootstrap_ci

SEED  = 42
BASE  = os.path.dirname(os.path.abspath(__file__))
ALARM = os.path.join(BASE, "output", "analyses", "q7_classified_alarm.csv")
SPEC  = os.path.join(BASE, "output", "specialty_classifications.csv")
ADOPT = os.path.join(BASE, "output", "analyses", "specialty_aiadoption.csv")
OUT_CSV = os.path.join(BASE, "output", "analyses", "q7_alarm_by_specialty.csv")
OUT_PNG = os.path.join(BASE, "output", "figures", "q7_alarm_failuremode_by_specialty.png")

# ── load ──────────────────────────────────────────────────────────────────────
alarm = pd.read_csv(ALARM, dtype={"pmid": str})
n0 = len(alarm)
alarm = alarm[alarm["failure_mode"] != "FAILED"].copy()
print(f"Loaded Alarm: {n0} rows → dropped {n0-len(alarm)} FAILED → {len(alarm)} rows.")

spec = pd.read_csv(SPEC, dtype={"pmid": str})[["pmid","specialty"]]
df   = alarm.merge(spec, on="pmid", how="left")
miss = df["specialty"].isna().sum()
print(f"Specialty join: {len(df)-miss}/{len(df)} matched (missing={miss}).")
df = df.dropna(subset=["specialty"]).copy()

df["confab_involved"] = df["failure_mode"].isin(["confabulation","both"]).astype(int)
df["generative_involved"] = df["model_type"].isin(["generative","both"]).astype(int)
df["misc_involved"] = df["failure_mode"].isin(["misclassification","both"]).astype(int)

# ── per-specialty composition with bootstrap CI ────────────────────────────────
def composition(sub: pd.DataFrame) -> pd.Series:
    n = len(sub)
    if n == 0:
        return pd.Series({"confab_share": 0.0, "misc_share": 0.0, "gen_share": 0.0})
    return pd.Series({
        "confab_share":   sub["confab_involved"].mean()    * 100,
        "misc_share":     sub["misc_involved"].mean()      * 100,
        "gen_share":      sub["generative_involved"].mean()* 100,
    })

rows = []
for sp, g in df.groupby("specialty"):
    n = len(g)
    fm_pct = g["failure_mode"].value_counts(normalize=True) * 100
    mt_pct = g["model_type"  ].value_counts(normalize=True) * 100
    # bootstrap CIs for the two ranked shares (n_boot=1000, seed=42)
    if n >= 20:
        b = bootstrap_ci(g.reset_index(drop=True), composition, n_boot=1000, seed=SEED)
        lo, hi = b["lower"], b["upper"]
    else:
        lo = hi = pd.Series({"confab_share": np.nan, "misc_share": np.nan, "gen_share": np.nan})
    rows.append({
        "specialty": sp,
        "n_alarm":   n,
        "confab_pct":           fm_pct.get("confabulation", 0.0),
        "misc_pct":             fm_pct.get("misclassification", 0.0),
        "both_fm_pct":          fm_pct.get("both", 0.0),
        "none_unclear_pct":     fm_pct.get("none_or_unclear", 0.0),
        "confab_share_incl_both": fm_pct.get("confabulation",0.0) + fm_pct.get("both",0.0),
        "confab_share_ci_lo":  lo["confab_share"],
        "confab_share_ci_hi":  hi["confab_share"],
        "gen_pct":              mt_pct.get("generative", 0.0),
        "discr_pct":            mt_pct.get("discriminative", 0.0),
        "both_mt_pct":          mt_pct.get("both", 0.0),
        "unclear_mt_pct":       mt_pct.get("unclear", 0.0),
        "gen_share_incl_both":  mt_pct.get("generative",0.0) + mt_pct.get("both",0.0),
        "gen_share_ci_lo":  lo["gen_share"],
        "gen_share_ci_hi":  hi["gen_share"],
        "low_confidence":   n < 20,
    })
sp_df = pd.DataFrame(rows).sort_values("n_alarm", ascending=False).reset_index(drop=True)

# ── print full per-specialty table ─────────────────────────────────────────────
print()
print("="*120)
print("Per-specialty composition (Alarm only). Specialties with n<20 flagged low-confidence (no CI).")
print("="*120)
hdr = (f"{'specialty':<40s} {'n':>4s} | "
       f"{'confab':>7s} {'misc':>6s} {'bothF':>6s} {'unclr':>6s} | "
       f"{'CONFAB+bothF [95%CI]':>22s} | "
       f"{'GEN+bothM [95%CI]':>22s}")
print(hdr)
print("-"*len(hdr))
for r in sp_df.itertuples():
    flag = " *" if r.low_confidence else "  "
    ci_c = f"[{r.confab_share_ci_lo:5.1f}-{r.confab_share_ci_hi:5.1f}]" if not np.isnan(r.confab_share_ci_lo) else "[   n/a       ]"
    ci_g = f"[{r.gen_share_ci_lo:5.1f}-{r.gen_share_ci_hi:5.1f}]"       if not np.isnan(r.gen_share_ci_lo)    else "[   n/a       ]"
    print(f"{r.specialty[:38]:<38s}{flag} {r.n_alarm:>4d} | "
          f"{r.confab_pct:>6.1f}% {r.misc_pct:>5.1f}% {r.both_fm_pct:>5.1f}% {r.none_unclear_pct:>5.1f}% | "
          f"{r.confab_share_incl_both:>5.1f}% {ci_c} | "
          f"{r.gen_share_incl_both:>5.1f}% {ci_g}")

# ── rankings (only n>=20 interpretable) ────────────────────────────────────────
keep = sp_df[~sp_df["low_confidence"]].copy()
print()
print("="*120)
print(f"Rankings (interpretable specialties only, n>=20: {len(keep)} of {len(sp_df)})")
print("="*120)
print("\nBy confab-involved share (confabulation + both):")
for r in keep.sort_values("confab_share_incl_both", ascending=False).itertuples():
    print(f"  {r.specialty[:42]:<42s}  n={r.n_alarm:>3d}  "
          f"confab+both={r.confab_share_incl_both:>5.1f}% "
          f"[{r.confab_share_ci_lo:>5.1f}-{r.confab_share_ci_hi:>5.1f}]  "
          f"(gen+both={r.gen_share_incl_both:>5.1f}%)")
print("\nBy generative-share (generative + both):")
for r in keep.sort_values("gen_share_incl_both", ascending=False).itertuples():
    print(f"  {r.specialty[:42]:<42s}  n={r.n_alarm:>3d}  "
          f"gen+both={r.gen_share_incl_both:>5.1f}% "
          f"[{r.gen_share_ci_lo:>5.1f}-{r.gen_share_ci_hi:>5.1f}]  "
          f"(confab+both={r.confab_share_incl_both:>5.1f}%)")

# ── join with S4-1 adoption ───────────────────────────────────────────────────
adopt = pd.read_csv(ADOPT)
adopt = adopt.rename(columns={
    "critical_rate_pct": "critical_rate_pct",
    "fda_device_count":  "fda_devices",
})
merged = sp_df.merge(adopt[["specialty","n_papers","critical_rate_pct","fda_devices"]],
                     on="specialty", how="left")

print()
print("="*120)
print("Link to S4-1 (FDA adoption × criticality × generative/confab exposure)")
print("="*120)
print(f"{'specialty':<40s} {'n_all':>6s} {'crit%':>6s} {'FDA':>5s} | {'n_alarm':>7s} {'gen%':>6s} {'confab%':>8s}")
for r in merged.dropna(subset=["critical_rate_pct"]).sort_values("critical_rate_pct", ascending=False).itertuples():
    print(f"{r.specialty[:38]:<38s}  {int(r.n_papers):>6d} "
          f"{r.critical_rate_pct:>5.1f}% {int(r.fda_devices):>5d} | "
          f"{r.n_alarm:>7d} {r.gen_share_incl_both:>5.1f}% {r.confab_share_incl_both:>7.1f}%")

# explicit Dermatology call-out
derm = merged[merged["specialty"]=="Dermatology"]
if len(derm):
    d = derm.iloc[0]
    print()
    print(f"DERMATOLOGY explicit: critical_rate={d['critical_rate_pct']:.1f}% (rank #2 overall), "
          f"FDA_devices={int(d['fda_devices'])}, n_alarm={d['n_alarm']}, "
          f"gen+both={d['gen_share_incl_both']:.1f}%, confab+both={d['confab_share_incl_both']:.1f}%.")

# Spearman: critical_rate vs gen-share / confab-share across n>=20 specialties present in both tables
joint = merged.dropna(subset=["critical_rate_pct"])
joint = joint[~joint["low_confidence"]]
if len(joint) >= 4:
    from scipy.stats import spearmanr
    rho_g, p_g = spearmanr(joint["critical_rate_pct"], joint["gen_share_incl_both"])
    rho_c, p_c = spearmanr(joint["critical_rate_pct"], joint["confab_share_incl_both"])
    rho_f, p_f = spearmanr(joint["critical_rate_pct"], joint["fda_devices"])
    print()
    print(f"Spearman across {len(joint)} specialties (n>=20, in both tables):")
    print(f"  critical_rate vs generative-share : rho={rho_g:+.3f}  p={p_g:.3f}")
    print(f"  critical_rate vs confab-share     : rho={rho_c:+.3f}  p={p_c:.3f}")
    print(f"  critical_rate vs FDA_devices      : rho={rho_f:+.3f}  p={p_f:.3f}  (reference S4-1)")

# ── write the per-specialty table ─────────────────────────────────────────────
os.makedirs(os.path.dirname(OUT_CSV), exist_ok=True)
out_cols = ["specialty","n_alarm","low_confidence",
            "confab_pct","misc_pct","both_fm_pct","none_unclear_pct",
            "confab_share_incl_both","confab_share_ci_lo","confab_share_ci_hi",
            "gen_pct","discr_pct","both_mt_pct","unclear_mt_pct",
            "gen_share_incl_both","gen_share_ci_lo","gen_share_ci_hi"]
merged_out = merged[out_cols + ["critical_rate_pct","fda_devices","n_papers"]].copy()
merged_out.to_csv(OUT_CSV, index=False)
print(f"\nSaved → {OUT_CSV}")

# ── figure: 2 panels ─────────────────────────────────────────────────────────
os.makedirs(os.path.dirname(OUT_PNG), exist_ok=True)
fig = plt.figure(figsize=(15, 10))
gs  = fig.add_gridspec(1, 2, width_ratios=[1.3, 1.0], wspace=0.28)
axA = fig.add_subplot(gs[0])
axB = fig.add_subplot(gs[1])

# Panel A: stacked bars by specialty, sorted by confab-share. All specialties shown,
# n<20 plotted in muted alpha and tick label suffixed with *.
order = sp_df.sort_values("confab_share_incl_both", ascending=True).reset_index(drop=True)
y = np.arange(len(order))
def vals(col): return order[col].values

cats   = ["confab_pct","both_fm_pct","misc_pct","none_unclear_pct"]
labels = ["confabulation","both","misclassification","none_or_unclear"]
colors = ["#d62728","#9467bd","#1f77b4","#bcbd22"]
left = np.zeros(len(order))
for cat, lbl, col in zip(cats, labels, colors):
    v = vals(cat)
    alphas = [0.35 if lc else 0.95 for lc in order["low_confidence"]]
    for i in range(len(order)):
        axA.barh(y[i], v[i], left=left[i], color=col, edgecolor="white",
                 linewidth=0.5, alpha=alphas[i], label=lbl if i==0 else None)
    left += v

axA.set_yticks(y)
axA.set_yticklabels([f"{s} (n={n}){' *' if lc else ''}"
                     for s,n,lc in zip(order["specialty"], order["n_alarm"], order["low_confidence"])],
                    fontsize=9)
axA.set_xlabel("% of specialty's Alarm papers")
axA.set_xlim(0, 100)
axA.set_title("A. failure_mode composition by specialty (Alarm, sorted by confab+both)",
              fontsize=11, fontweight="bold", loc="left")
handles = [Patch(facecolor=c, label=l) for c,l in zip(colors, labels)]
axA.legend(handles=handles, loc="lower right", fontsize=8, frameon=False)
axA.text(0.99, 0.02, "* n<20 → exploratory, plotted faded", transform=axA.transAxes,
         ha="right", va="bottom", fontsize=7, color="gray", style="italic")
for s in ("top","right"): axA.spines[s].set_visible(False)

# Panel B: scatter gen-share vs confab-share, labeled, sized by n_alarm.
# n>=20 solid, n<20 hollow.
sub = sp_df.copy()
sizes = np.clip(sub["n_alarm"]*4 + 40, 50, 600)
for r in sub.itertuples():
    fc = "#7b3294" if not r.low_confidence else "white"
    ec = "#7b3294"
    axB.scatter(r.gen_share_incl_both, r.confab_share_incl_both,
                s=max(50, min(600, r.n_alarm*4+40)), facecolor=fc, edgecolor=ec,
                linewidth=1.5, alpha=0.85, zorder=3)
    label = r.specialty
    if len(label) > 24: label = label[:22] + "…"
    axB.annotate(label, (r.gen_share_incl_both, r.confab_share_incl_both),
                 xytext=(6, 5), textcoords="offset points", fontsize=8, zorder=4)

axB.set_xlabel("generative-share (model_type ∈ {generative, both}) %")
axB.set_ylabel("confab-share (failure_mode ∈ {confabulation, both}) %")
axB.set_title("B. generative-share vs confab-share per specialty\n"
              "(point size ∝ n_alarm; hollow = n<20)",
              fontsize=11, fontweight="bold", loc="left")
axB.axhline(sub[~sub["low_confidence"]]["confab_share_incl_both"].mean(),
            color="#d62728", linestyle=":", linewidth=1, alpha=0.5)
axB.axvline(sub[~sub["low_confidence"]]["gen_share_incl_both"].mean(),
            color="#e377c2", linestyle=":", linewidth=1, alpha=0.5)
axB.set_xlim(-5, 105); axB.set_ylim(-2, max(sub["confab_share_incl_both"].max()+5, 40))
for s in ("top","right"): axB.spines[s].set_visible(False)

fig.suptitle("Q7 S5-1-a — failure_mode × model_type by specialty (Alarm only)",
             fontsize=12, y=0.995)
fig.text(0.5, 0.005,
         "Prompt: q7_failuremode_v1 · n=914 Alarm w/ specialty · bootstrap n=1000 percentile 95% CI",
         ha="center", fontsize=8, style="italic", color="gray")
fig.savefig(OUT_PNG, dpi=300, bbox_inches="tight")
print(f"Saved → {OUT_PNG}")

print()
print("="*120)
print("CAVEAT (print verbatim):")
print("  Alarm-only; per-specialty n is small (several <20, flagged with *) → this is "
      "EXPLORATORY only. To be confirmed once Cautious (Phase 2) is added and, if approved, "
      "a task_type axis is introduced. This is downstream analysis S5-1-a.")
print("="*120)
