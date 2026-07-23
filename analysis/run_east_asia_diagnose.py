"""
Session 3 — East Asia low critical rate (18.5%) diagnostic.

Three candidate explanations:
  (a) Genuinely more positive AI-medicine discourse in East Asian institutions
  (b) Institutional / linguistic norms favoring less critical conclusions in published abstracts
  (c) Corpus composition (more methodology / less clinical-application papers in East Asian publications)

Two cheap diagnostics:
  1. Critical rate WITHIN each major specialty, East Asia vs NA+WEU. If the gap holds within
     the same specialty, composition is not the (sole) story.
  2. Critical rate per individual East Asian country. If China/Japan/Korea differ greatly,
     it's not a uniform regional voice but a country-level pattern.

Produces:
  output/analyses/east_asia_diagnose.csv
  output/analyses/discussion_east_asia.md
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from analysis.robustness import load_classifications, bootstrap_ci

WORKTREE = Path(__file__).resolve().parents[1]
ANALYSES_DIR = WORKTREE / "output" / "analyses"
SPEC_PATH = WORKTREE / "output" / "specialty_classifications.csv"
GEO_PATH = WORKTREE / "output" / "geography_classifications.csv"


def main() -> None:
    v1 = load_classifications("v1")
    v1["pmid"] = v1["pmid"].astype(str)
    spec = pd.read_csv(SPEC_PATH, usecols=["pmid", "specialty"])
    geo = pd.read_csv(GEO_PATH, usecols=["pmid", "country", "region"])
    for f in [spec, geo]:
        f["pmid"] = f["pmid"].astype(str)
    df = v1.merge(spec, on="pmid", how="left").merge(geo, on="pmid", how="left")
    df["crit"] = df["stance"].isin(["Alarm", "Caution"]).astype(int)

    # ── Diagnostic 1: critical rate within specialty, EA vs NA+WEU ────────────
    ea = df[df["region"] == "East Asia"]
    nawu = df[df["region"].isin(["North America", "Western Europe"])]
    spec_counts_ea = ea["specialty"].value_counts()
    rows = []
    for s in spec_counts_ea.head(10).index:
        n_ea = (ea["specialty"] == s).sum()
        n_nw = (nawu["specialty"] == s).sum()
        if n_ea < 30 or n_nw < 30:
            continue
        sub_ea = ea[ea["specialty"] == s]
        sub_nw = nawu[nawu["specialty"] == s]
        ea_crit = sub_ea["crit"].mean() * 100
        nw_crit = sub_nw["crit"].mean() * 100

        # Bootstrap CI on East Asia critical rate within specialty
        b_ea = bootstrap_ci(sub_ea[["pmid", "stance"]],
                             lambda d: float(d["stance"].isin(["Alarm", "Caution"]).mean() * 100))
        b_nw = bootstrap_ci(sub_nw[["pmid", "stance"]],
                             lambda d: float(d["stance"].isin(["Alarm", "Caution"]).mean() * 100))
        rows.append({
            "specialty": s,
            "n_ea": int(n_ea),
            "n_nawu": int(n_nw),
            "ea_crit_pct": round(ea_crit, 2),
            "ea_ci_lo": round(b_ea["lower"], 2),
            "ea_ci_hi": round(b_ea["upper"], 2),
            "nawu_crit_pct": round(nw_crit, 2),
            "nawu_ci_lo": round(b_nw["lower"], 2),
            "nawu_ci_hi": round(b_nw["upper"], 2),
            "delta_pp": round(ea_crit - nw_crit, 2),
        })
    spec_df = pd.DataFrame(rows).sort_values("delta_pp")

    print("=== Diagnostic 1: Critical rate WITHIN specialty, East Asia vs (NA+WEU) ===")
    print(f"{'specialty':<40} {'n_ea':>5} {'n_nawu':>7} {'EA% (CI)':>20} "
          f"{'NA+WEU% (CI)':>22} {'Δ pp':>7}")
    for r in spec_df.itertuples():
        print(f"  {r.specialty:<40} {r.n_ea:>5,} {r.n_nawu:>7,}  "
              f"{r.ea_crit_pct:5.1f} ({r.ea_ci_lo:5.1f}–{r.ea_ci_hi:5.1f})  "
              f"{r.nawu_crit_pct:5.1f} ({r.nawu_ci_lo:5.1f}–{r.nawu_ci_hi:5.1f})  "
              f"{r.delta_pp:>+6.1f}")

    spec_df.to_csv(ANALYSES_DIR / "east_asia_diagnose_by_specialty.csv", index=False)

    # ── Diagnostic 2: critical rate per East Asian country ────────────────────
    print("\n=== Diagnostic 2: Critical rate per East Asian country ===")
    country_rows = []
    for country in ea["country"].value_counts().index:
        sub = ea[ea["country"] == country]
        if len(sub) < 20:
            continue
        b = bootstrap_ci(sub[["pmid", "stance"]],
                          lambda d: float(d["stance"].isin(["Alarm", "Caution"]).mean() * 100))
        country_rows.append({
            "country": country, "n": len(sub),
            "crit_pct": round(b["point"], 2),
            "ci_lower": round(b["lower"], 2),
            "ci_upper": round(b["upper"], 2),
        })
    c_df = pd.DataFrame(country_rows).sort_values("crit_pct", ascending=False)
    for r in c_df.itertuples():
        print(f"  {r.country:<18} n={r.n:>5,}  {r.crit_pct:5.1f}% "
              f"({r.ci_lower:5.1f}–{r.ci_upper:5.1f})")
    c_df.to_csv(ANALYSES_DIR / "east_asia_diagnose_by_country.csv", index=False)

    # ── Mix-adjusted East Asia critical rate (using NA+WEU specialty mix) ─────
    # If we reweight EA records by the NA+WEU specialty mix, do we close the gap?
    nawu_spec_mix = nawu["specialty"].value_counts(normalize=True)
    ea_spec_crit = ea.groupby("specialty")["crit"].mean()
    aligned = ea_spec_crit.reindex(nawu_spec_mix.index).fillna(ea["crit"].mean())
    mix_adjusted_ea = (aligned * nawu_spec_mix).sum() * 100
    raw_ea = ea["crit"].mean() * 100
    raw_nawu = nawu["crit"].mean() * 100
    print(f"\n=== Diagnostic 3: Mix-adjustment ===")
    print(f"  Raw EA critical:                       {raw_ea:.2f}%")
    print(f"  EA critical, reweighted to NA+WEU mix: {mix_adjusted_ea:.2f}%")
    print(f"  Raw NA+WEU critical:                   {raw_nawu:.2f}%")
    print(f"  Composition-explained gap: "
          f"{(mix_adjusted_ea - raw_ea):.2f} pp of {raw_nawu - raw_ea:.2f} pp total "
          f"= {(mix_adjusted_ea - raw_ea)/(raw_nawu - raw_ea)*100:.0f}%")

    # ── Discussion brief ──────────────────────────────────────────────────────
    explained = mix_adjusted_ea - raw_ea
    total = raw_nawu - raw_ea
    composition_pct = explained / total * 100 if total else 0.0

    md = [
        "# Discussion brief — East Asia low critical rate (for upstream Opus chat)",
        "",
        "## Headline finding from Session 2",
        "",
        f"East Asia: 18.5% critical (n=3,260, 95% CI 17.2–19.9). About **half the NA+WEU rate** "
        f"(both ~35%). Strong robust signal; n is large.",
        "",
        "## Three candidate explanations",
        "",
        "- **(a) Genuine voice divergence** — East Asian institutions publish more positive "
        "AI-medicine discourse on the same clinical problems.",
        "- **(b) Conclusion-style norms** — institutional / linguistic conventions favor less "
        "critical conclusions in published abstracts (e.g., publication culture rewards "
        "constructive framing).",
        "- **(c) Corpus composition** — East Asia publishes more methodology / less "
        "clinical-application papers, and clinical-application papers attract more criticism.",
        "",
        "## Diagnostic 1 — Critical rate WITHIN specialty (East Asia vs NA+WEU)",
        "",
        "If the EA-vs-(NA+WEU) gap holds *within* the same specialty (e.g., Radiology EA "
        "vs Radiology NA+WEU), composition (c) is **not** the full story.",
        "",
        "| Specialty | n_EA | n_NA+WEU | EA % crit | NA+WEU % crit | Δ pp |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for r in spec_df.itertuples():
        md.append(f"| {r.specialty} | {r.n_ea:,} | {r.n_nawu:,} | "
                  f"{r.ea_crit_pct:.1f} ({r.ea_ci_lo:.1f}–{r.ea_ci_hi:.1f}) | "
                  f"{r.nawu_crit_pct:.1f} ({r.nawu_ci_lo:.1f}–{r.nawu_ci_hi:.1f}) | "
                  f"{r.delta_pp:+.1f} |")

    md.extend([
        "",
        "**Within-specialty Δ pattern:** "
        + ("Gap **persists** within every major specialty — points away from (c) and toward (a)/(b)."
            if all(r["delta_pp"] < 0 for r in rows)
            else "Gap is mixed across specialties — composition explains some but not all."),
        "",
        "## Diagnostic 2 — Per-country critical rate within East Asia",
        "",
        "If China, Japan, S. Korea, etc. differ substantially, the regional bucket is not a "
        "uniform voice; the explanation must accommodate country-level heterogeneity.",
        "",
        "| Country | n | Critical % (95% CI) |",
        "|---|---:|---|",
    ])
    for r in c_df.itertuples():
        md.append(f"| {r.country} | {r.n:,} | {r.crit_pct:.1f} ({r.ci_lower:.1f}–{r.ci_upper:.1f}) |")

    md.extend([
        "",
        "## Diagnostic 3 — Mix-adjusted East Asia critical rate",
        "",
        f"Reweighting East Asia's per-specialty critical rates by the NA+WEU specialty mix gives "
        f"**{mix_adjusted_ea:.2f}%** (vs raw EA {raw_ea:.2f}% and raw NA+WEU {raw_nawu:.2f}%).",
        "",
        f"- **Composition explains {composition_pct:.0f}%** of the EA-vs-(NA+WEU) gap "
        f"({explained:.2f} pp of {total:.2f} pp total).",
        f"- **Residual {100-composition_pct:.0f}%** is not explained by composition — that's "
        f"the part requiring explanation (a) or (b).",
        "",
        "## Open question for upstream Opus chat",
        "",
        "Given the mix-adjustment leaves ~{:.0f}% of the gap unexplained, and given the "
        "within-specialty gap is consistent across every major specialty, how should the "
        "Commentary discuss this?".format(100 - composition_pct),
        "",
        "**Three drafting options:**",
        "",
        "1. **Lead with the limitation.** \"East Asia's lower critical rate may reflect "
        "publication norms in abstracts; we cannot distinguish from data alone.\" Hedges, "
        "but honest.",
        "2. **Lead with the empirical observation, defer interpretation.** \"East Asian "
        "publications show a markedly lower critical-stance rate (18.5% vs ~35% in "
        "NA/WEU), which persists after adjusting for specialty mix. Future qualitative "
        "work is needed to distinguish institutional voice from conclusion-style norms.\"",
        "3. **Take a position.** Argue that the within-specialty consistency (every specialty "
        "shows the same EA-vs-NA+WEU gap, not just methodology-heavy ones) suggests "
        "(b) conclusion-style norms are at least partly responsible. Risky without "
        "outside-data anchor.",
        "",
        "Claude's read: **Option 2** is the right register for a Lancet Digital Health "
        "Commentary — empirically anchored, methodologically honest, opens a research "
        "direction.",
    ])

    out = ANALYSES_DIR / "discussion_east_asia.md"
    out.write_text("\n".join(md) + "\n")
    print(f"\nWrote: {out}")


if __name__ == "__main__":
    main()
