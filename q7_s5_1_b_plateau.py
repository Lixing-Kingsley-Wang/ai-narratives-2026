"""S5-1-b: did fabrication concern scale with LLM uptake, or plateau?

Pure analysis on q7_classified_alarm.csv. Reports strict vs broad confab
definitions, generative-share vs confab-among-generative over time, and tests
whether the latter is flat (plateau) while the former rises.
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import spearmanr
from robustness import bootstrap_ci

SEED = 42
BASE = os.path.dirname(os.path.abspath(__file__))
ALARM = os.path.join(BASE, "output", "analyses", "q7_classified_alarm.csv")
OUT_CSV = os.path.join(BASE, "output", "analyses", "q7_alarm_temporal_shares.csv")
OUT_PNG = os.path.join(BASE, "output", "figures", "q7_alarm_confab_plateau.png")

YEARS = ["2021","2022","2023","2024","2025","2026"]

# ── load ──────────────────────────────────────────────────────────────────────
df = pd.read_csv(ALARM, dtype={"pmid": str})
n0 = len(df)
df = df[df["failure_mode"] != "FAILED"].copy()
print(f"Loaded Alarm: {n0} → dropped {n0-len(df)} FAILED → {len(df)} rows.")

df["pub_year"] = df["pub_year"].astype(str)
df["gen"]    = df["model_type"].isin(["generative","both"]).astype(int)
df["confS"]  = (df["failure_mode"] == "confabulation").astype(int)
df["confB"]  = df["failure_mode"].isin(["confabulation","both"]).astype(int)

# ── helpers ───────────────────────────────────────────────────────────────────
def share_ci(sub: pd.DataFrame, col: str, n_boot: int = 1000):
    """% of sub where col==1, with bootstrap CI. Returns (point, lo, hi, n)."""
    if len(sub) == 0:
        return 0.0, np.nan, np.nan, 0
    pt = sub[col].mean() * 100
    b = bootstrap_ci(sub[[col]].reset_index(drop=True),
                     lambda s: float(s[col].mean()*100),
                     n_boot=n_boot, seed=SEED)
    return pt, b["lower"], b["upper"], len(sub)

# ── per-year shares ───────────────────────────────────────────────────────────
rows = []
for y in YEARS:
    sub = df[df["pub_year"] == y]
    n = len(sub)
    gen_pt,  gen_lo,  gen_hi,  _ = share_ci(sub, "gen")
    cs_pt,   cs_lo,   cs_hi,   _ = share_ci(sub, "confS")
    cb_pt,   cb_lo,   cb_hi,   _ = share_ci(sub, "confB")
    gsub = sub[sub["gen"] == 1]
    cag_pt, cag_lo, cag_hi, n_gen = share_ci(gsub, "confB")
    rows.append({
        "pub_year": y, "n_alarm": n, "n_generative": n_gen,
        "gen_share":            gen_pt, "gen_share_lo": gen_lo, "gen_share_hi": gen_hi,
        "confab_strict":        cs_pt,  "confab_strict_lo": cs_lo, "confab_strict_hi": cs_hi,
        "confab_broad":         cb_pt,  "confab_broad_lo":  cb_lo, "confab_broad_hi":  cb_hi,
        "confab_among_gen":     cag_pt, "confab_among_gen_lo": cag_lo, "confab_among_gen_hi": cag_hi,
    })
tab = pd.DataFrame(rows)

# ── print table ───────────────────────────────────────────────────────────────
print()
print("="*132)
print("Per-year shares (Alarm, n=915), bootstrap n=1000 percentile 95% CI")
print("="*132)
print(f"{'year':<6s} {'n':>4s} {'n_gen':>6s} | "
      f"{'gen-share':>22s} | {'confab STRICT':>22s} | {'confab BROAD':>22s} | "
      f"{'confab AMONG GEN':>22s}")
def fmt(v, lo, hi):
    if np.isnan(lo): return f"{v:>5.1f}% [   n/a       ]"
    return f"{v:>5.1f}% [{lo:>5.1f}-{hi:>5.1f}]"
for r in tab.itertuples():
    print(f"{r.pub_year:<6s} {r.n_alarm:>4d} {r.n_generative:>6d} | "
          f"{fmt(r.gen_share,         r.gen_share_lo,         r.gen_share_hi):>22s} | "
          f"{fmt(r.confab_strict,     r.confab_strict_lo,     r.confab_strict_hi):>22s} | "
          f"{fmt(r.confab_broad,      r.confab_broad_lo,      r.confab_broad_hi):>22s} | "
          f"{fmt(r.confab_among_gen,  r.confab_among_gen_lo,  r.confab_among_gen_hi):>22s}")

# ── strict vs broad summary, overall and post-2023 ────────────────────────────
def summarise(sub, label):
    n = len(sub); n_gen = int(sub["gen"].sum())
    gen_pt,  gen_lo,  gen_hi,  _ = share_ci(sub, "gen")
    cs_pt,   cs_lo,   cs_hi,   _ = share_ci(sub, "confS")
    cb_pt,   cb_lo,   cb_hi,   _ = share_ci(sub, "confB")
    cag_pt, cag_lo, cag_hi, _    = share_ci(sub[sub["gen"]==1], "confB")
    print(f"\n[{label}]  n={n}, n_generative={n_gen}")
    print(f"  generative-share          {fmt(gen_pt, gen_lo, gen_hi)}")
    print(f"  confab STRICT (==conf)    {fmt(cs_pt,  cs_lo,  cs_hi)}")
    print(f"  confab BROAD  (conf|both) {fmt(cb_pt,  cb_lo,  cb_hi)}")
    print(f"  confab AMONG GENERATIVE   {fmt(cag_pt, cag_lo, cag_hi)}")

print()
print("="*132)
print("STRICT vs BROAD summary (manuscript-ready)")
print("="*132)
summarise(df, "OVERALL 2021–2026")
summarise(df[df["pub_year"].isin(["2023","2024","2025","2026"])], "POST-2023 (2023–2026)")
summarise(df[df["pub_year"].isin(["2024","2025","2026"])], "POST-2023 strict (2024–2026)")

# ── spearman over years (n=6) ─────────────────────────────────────────────────
print()
print("="*132)
print("Spearman over 6 years (gen-share rising? confab-among-generative flat?)")
print("="*132)
yi = np.arange(len(YEARS))
rho_g, p_g = spearmanr(yi, tab["gen_share"].values)
rho_c, p_c = spearmanr(yi, tab["confab_among_gen"].values)
# also drop the 2021/2022 zero-gen anomaly: real LLM era starts 2023
post = tab[tab["pub_year"].isin(["2023","2024","2025","2026"])]
rho_gp, p_gp = spearmanr(np.arange(len(post)), post["gen_share"].values)
rho_cp, p_cp = spearmanr(np.arange(len(post)), post["confab_among_gen"].values)
print(f"  Across 2021–2026 (n=6 years):")
print(f"    generative-share        vs year : rho={rho_g:+.3f}  p={p_g:.3f}  → "
      f"{'RISING' if rho_g>0.5 and p_g<0.1 else 'no monotonic rise'}")
print(f"    confab-among-generative vs year : rho={rho_c:+.3f}  p={p_c:.3f}  → "
      f"{'PLATEAU/FLAT' if abs(rho_c)<0.5 or p_c>0.1 else 'monotonic trend'}")
print(f"  Across post-2023 (2023–2026, n=4 years — LLM era only):")
print(f"    generative-share        vs year : rho={rho_gp:+.3f}  p={p_gp:.3f}")
print(f"    confab-among-generative vs year : rho={rho_cp:+.3f}  p={p_cp:.3f}")

# ── write CSV ─────────────────────────────────────────────────────────────────
os.makedirs(os.path.dirname(OUT_CSV), exist_ok=True)
tab.to_csv(OUT_CSV, index=False)
print(f"\nSaved → {OUT_CSV}")

# ── figure ────────────────────────────────────────────────────────────────────
os.makedirs(os.path.dirname(OUT_PNG), exist_ok=True)
fig, ax = plt.subplots(figsize=(11, 7))
fig.subplots_adjust(left=0.09, right=0.97, top=0.84, bottom=0.26)
x = np.arange(len(YEARS))

# generative-share line with CI band
gen   = tab["gen_share"].values
gen_l = tab["gen_share_lo"].values
gen_h = tab["gen_share_hi"].values
cag   = tab["confab_among_gen"].values
cag_l = tab["confab_among_gen_lo"].values
cag_h = tab["confab_among_gen_hi"].values
cb    = tab["confab_broad"].values
cs    = tab["confab_strict"].values

# 2023 inflection (draw first, behind everything)
ax.axvline(2, color="0.55", linestyle="--", linewidth=0.9, zorder=0)
ax.text(2.02, 106, "ChatGPT (Nov 2022) →", fontsize=8.5, ha="left",
        va="top", color="0.4")

# two HERO lines (with CI bands)
ax.fill_between(x, gen_l, gen_h, color="#e377c2", alpha=0.16, linewidth=0, zorder=1)
ax.plot(x, gen, marker="o", color="#d6379b", linewidth=2.8, markersize=8, zorder=3,
        label="generative-share  (model_type ∈ {generative, both})")
ax.fill_between(x, cag_l, cag_h, color="#d62728", alpha=0.16, linewidth=0, zorder=1)
ax.plot(x, cag, marker="s", color="#c81e1e", linewidth=2.8, markersize=8, zorder=3,
        label="confab-share AMONG generative  (failure_mode ∈ {confab, both})")

# two faint REFERENCE lines (no CI band, muted, thin)
ax.plot(x, cb, marker="D", color="#8c564b", linewidth=1.3, markersize=4.5,
        linestyle="--", alpha=0.6, zorder=2,
        label="confab BROAD over all Alarm  (reference)")
ax.plot(x, cs, marker="v", color="#9a9a9a", linewidth=1.1, markersize=4.5,
        linestyle=":", alpha=0.6, zorder=2,
        label="confab STRICT over all Alarm  (reference)")

# value labels on the two hero lines only
for xi, v in zip(x, gen):
    ax.annotate(f"{v:.0f}%", (xi, v), xytext=(0, 11), textcoords="offset points",
                ha="center", fontsize=9, color="#d6379b", fontweight="bold")
for xi, v, n in zip(x, cag, tab["n_generative"]):
    txt = f"{v:.0f}%" if n >= 10 else f"{v:.0f}%*"
    ax.annotate(txt, (xi, v), xytext=(0, -16), textcoords="offset points",
                ha="center", fontsize=9, color="#c81e1e", fontweight="bold")

# divergence annotation — parked in the empty UPPER-LEFT, arrow to the plateau
ax.annotate(
    "Divergence\ngenerative-share rises ~80 pp,\nbut fabrication concern among\ngenerative-AI Alarm papers\nplateaus near 20%.",
    xy=(4.0, cag[4]), xytext=(0.12, 74),
    fontsize=9.5, color="0.15", va="center", ha="left",
    bbox=dict(boxstyle="round,pad=0.45", facecolor="#fff7c2",
              edgecolor="#c9b66b", linewidth=0.9),
    arrowprops=dict(arrowstyle="->", color="#888", lw=1.2,
                    connectionstyle="arc3,rad=-0.2"))

# x axis: clean year labels + a separate thin n-row beneath
ax.set_xticks(x)
ax.set_xticklabels(YEARS, fontsize=10)
ax.set_xlim(-0.4, 5.4)
for xi, n, ng in zip(x, tab["n_alarm"], tab["n_generative"]):
    ax.annotate(f"n={n}\ngen={ng}", (xi, 0), xytext=(0, -30),
                textcoords="offset points", ha="center", va="top",
                fontsize=7.5, color="0.45", annotation_clip=False)

ax.set_ylabel("% of papers", fontsize=11)
ax.set_ylim(-4, 110)
ax.set_yticks([0, 20, 40, 60, 80, 100])
ax.set_title("Q7 S5-1-b — fabrication concern did NOT scale with LLM uptake\n"
             "Alarm papers · bootstrap 95% CI shaded on the two hero lines · * = n_gen<10",
             fontsize=12, loc="left", pad=26)
# legend OUTSIDE the data, below the plot, 2 columns
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.20), ncol=2,
          fontsize=9, frameon=False, columnspacing=2.4, handlelength=2.6)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)

fig.text(0.5, 0.015,
         "Prompt: q7_failuremode_v1 · Alarm only (Caution pending) · "
         "ρ(generative-share, year)=%+.2f   ρ(confab-among-gen, year)=%+.2f"
         % (rho_g, rho_c),
         ha="center", fontsize=8, style="italic", color="gray")
fig.savefig(OUT_PNG, dpi=300, bbox_inches="tight")
print(f"Saved → {OUT_PNG}")

print()
print("="*132)
print("NOTE (print verbatim):")
print("  The temporal rise in generative-share is partly EXPECTED (generative AI is new); "
      "the informative result is the PLATEAU of confab-share-AMONG-GENERATIVE.")
print("="*132)
